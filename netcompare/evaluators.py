"""Evaluators."""
import sys
from typing import Any, Mapping, Dict
from deepdiff import DeepDiff
from .utils.diff_helpers import get_diff_iterables_items, fix_deepdiff_key_names

sys.path.append(".")


def diff_generator(pre_result: Any, post_result: Any) -> Dict:
    """Generates diff between pre and post data based on check definition.

    Args:
        pre_result: dataset to compare
        post_result: dataset to compare

    Returns:
        differences between two datasets
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

    result = fix_deepdiff_key_names(result)
    return result


def parameter_evaluator(values: Mapping, parameter: Mapping) -> Dict:
    """Parameter Match evaluator engine."""
    # value: [{'7.7.7.7': {'peerAddress': '7.7.7.7', 'localAsn': '65130.1100', 'linkType': 'external'}}]
    # parameter: {'localAsn': '65130.1100', 'linkType': 'external'}
    result = {}
    if not isinstance(values, list):
        raise TypeError("Something went wrong during JMSPath parsing. values must be of type list.")

    for value in values:
        # item: {'7.7.7.7': {'peerAddress': '7.7.7.7', 'localAsn': '65130.1101', 'linkType': 'externals
        temp_dict = {}

        inner_key = list(value.keys())[0]
        # inner_key: '7.7.7.7'
        inner_value = list(value.values())[0]
        # inner_value: [{'peerAddress': '7.7.7.7', 'localAsn': '65130.1101', 'linkType': 'externals'}]

        for p_key, p_value in parameter.items():
            if inner_value[p_key] != p_value:
                temp_dict[p_key] = inner_value[p_key]

        if temp_dict:
            result[inner_key] = temp_dict

    return result
