"""Evaluators."""
import re
from typing import Any, Mapping, Dict, Tuple
from deepdiff import DeepDiff
from .utils.diff_helpers import get_diff_iterables_items, fix_deepdiff_key_names
from .operator import Operator


def diff_generator(pre_result: Any, post_result: Any) -> Dict:
    """Generates diff between pre and post data based on check definition.

    Args:
        pre_result: dataset to compare
        post_result: dataset to compare

    Returns:
        dict: differences between two datasets with the following keys:
            - "values_changed": Item values that have changed
            - "missing": Item keys that have been removed
            - "new": Item keys that have been added
    """
    diff_result = DeepDiff(pre_result, post_result)

    result = diff_result.get("values_changed", {})

    if diff_result.get("dictionary_item_removed"):
        result.update({k: "missing" for k in diff_result["dictionary_item_removed"]})

    if diff_result.get("dictionary_item_added"):
        result.update({k: "new" for k in diff_result["dictionary_item_added"]})

    iterables_items = get_diff_iterables_items(diff_result)
    if iterables_items:
        result.update(iterables_items)

    return fix_deepdiff_key_names(result)


def parameter_evaluator(values: Mapping, parameters: Mapping, mode: str) -> Dict:
    """Parameter Match evaluator engine.

    Args:
        values: List of items what we will check the parameters against
        parameters: Dict with the keys and reference values to check

    Example:
        values: [{'7.7.7.7': {'peerAddress': '7.7.7.7', 'localAsn': '65130.1100', 'linkType': 'external'}}]
        parameters: {'localAsn': '65130.1100', 'linkType': 'external'}

    Returns:
        Dictionary with all the items that have some value not matching the expectations from parameters
    """
    if not isinstance(values, list):
        raise TypeError("Something went wrong during jmespath parsing. 'values' must be of type List.")

    result = {}
    for value in values:
        # value: {'7.7.7.7': {'peerAddress': '7.7.7.7', 'localAsn': '65130.1101', 'linkType': 'externals
        if not isinstance(value, dict):
            raise TypeError(
                "Something went wrong during jmespath parsing. ",
                f"'value' ({value}) must be of type Dict, and it's {type(value)}",
            )

        result_item = {}

        # TODO: Why the 'value' dict has always ONE single element? we have to explain
        # inner_key: '7.7.7.7'
        inner_key = list(value.keys())[0]
        # inner_value: [{'peerAddress': '7.7.7.7', 'localAsn': '65130.1101', 'linkType': 'externals'}]
        inner_value = list(value.values())[0]

        for parameter_key, parameter_value in parameters.items():
            if mode == "match" and inner_value[parameter_key] != parameter_value:
                result_item[parameter_key] = inner_value[parameter_key]
            elif mode == "no-match" and inner_value[parameter_key] == parameter_value:
                result_item[parameter_key] = inner_value[parameter_key]

        if result_item:
            result[inner_key] = result_item

    return result


def regex_evaluator(values: Mapping, regex_expression: str, mode: str) -> Dict:
    """Regex Match evaluator engine."""
    # values: [{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE'}}]
    # parameter: {'regex': '.*UNDERLAY.*', 'mode': 'include'}
    result = {}
    if not isinstance(values, list):
        raise TypeError("Something went wrong during JMSPath parsing. 'values' must be of type List.")

    for item in values:
        for founded_value in item.values():
            for value in founded_value.values():
                match_result = re.search(regex_expression, value)
                # Fail if there is not regex match
                if mode == "match" and not match_result:
                    result.update(item)
                # Fail if there is regex match
                elif mode == "no-match" and match_result:
                    result.update(item)

    return result


def operator_evaluator(reference_data: Mapping, value_to_compare: Mapping) -> Tuple[Dict, bool]:
    """Operator evaluator call."""
    # reference_data
    # {'mode': 'all-same', 'operator_data': True}
    operator_mode = reference_data["mode"].replace("-", "_")
    operator = Operator(reference_data["operator_data"], value_to_compare)
    return getattr(operator, operator_mode)()
