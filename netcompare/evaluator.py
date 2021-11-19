"""Diff evaluator."""
import re
import sys
from deepdiff import DeepDiff
from collections import defaultdict
from collections.abc import Mapping as DictMapping
from functools import partial
from typing import Mapping, List

from .runner import extract_values_from_output

sys.path.append(".")


def diff_generator(pre_data: Mapping, post_data: Mapping, check_definition: Mapping) -> Mapping:
    """
    Generates diff between pre and post data based on check definition.

    Args:
        pre_data: pre data result.
        post_data: post data result.
        check_definition: check definitions.

    Return:
        output: diff between pre and post data.

    Example:
        >>> from evaluator import diff_generator
        >>> pre_data = {"result": [{"bgp_neigh": "10.17.254.2","state": "Idle"}]}
        >>> post_data = {"result": [{"bgp_neigh": "10.17.254.2","state": "Up"}]}
        >>> check_definition = {"check_type": "exact_match", "value_path": "result[*].[state]", "reference_key_path": "result[*].bgp_neigh"}
        >>> print(diff_generator(check_definition, post_data, check_definition))
        {'10.17.254.2': {'state': {'new_value': 'Up', 'old_value': 'Idle'}}}
    """
    pre_result = extract_values_from_output(check_definition, pre_data)
    post_result = extract_values_from_output(check_definition, post_data)

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


def get_diff_iterables_items(diff_result: Mapping) -> Mapping:
    """
    Return a dict with new and missing values where the values are in a list.

    Args:
        diff_result: dict retruned from a DeepDiff compare.

    Return:
        defaultdict

    Example:
        >>> diff_result = {
            "iterable_item_added": {
                "root['Ethernet3'][1]": {
                    "hostname": "ios-xrv-unittest",
                    "port": "Gi0/0/0/0"
                },
                "root['Ethernet3'][2]": {
                    "hostname": "ios-xrv-unittest",
                    "port": "Gi0/0/0/1"
                }
            }
        }
        >>> get_diff_iterables_items(diff_result)
        defaultdict(functools.partial(<class 'collections.defaultdict'>, <class 'list'>),
            {"['Ethernet3']": defaultdict(list,
                {'new': [
                        {'hostname': 'ios-xrv-unittest', 'port': 'Gi0/0/0/0'},
                        {'hostname': 'ios-xrv-unittest', 'port': 'Gi0/0/0/1'}
                    ]}
            )}
        )
    """
    # DeepDiff iterable_items are returned when the source data is a list
    # and provided in the format: "root['Ethernet3'][1]"
    # or more generically: root['KEY']['KEY']['KEY']...[numeric_index]
    # where the KEYs are dict keys within the original object
    # and the "[index]" is appended to indicate the position within the list.
    get_dict_keys = re.compile(r"^root((\['\w.*'\])+)\[\d+\]$")

    defaultdict_list = partial(defaultdict, list)
    result = defaultdict(defaultdict_list)

    items_removed = diff_result.get("iterable_item_removed")
    if items_removed:
        for key, value in items_removed.items():
            key, *_ = get_dict_keys.match(key).groups()
            result[key]["missing"].append(value)

    items_added = diff_result.get("iterable_item_added")
    if items_added:
        for key, value in items_added.items():
            key, *_ = get_dict_keys.match(key).groups()
            result[key]["new"].append(value)

    return result


def fix_deepdiff_key_names(obj: Mapping) -> Mapping:
    """Return a dict based on the provided dict object where the brackets and quotes are removed from the string."""
    # sample keys:
    # root[2]['10.64.207.255']['accepted_prefixes']
    # root['Ethernet1'][0]['port']
    pattern = r"'([A-Za-z0-9_\./\\-]*)'"

    result = dict()
    for key, value in obj.items():
        key_parts = re.findall(pattern, key)
        partial_res = group_value(key_parts, value)
        dict_merger(result, partial_res)
    return result


def group_value(tree_list: List, value: Mapping) -> Mapping:
    """
    Build dictionary based on value's key and reference key.

    Args:
        tree_list: list of value's key and reference key
        value: value results

    Return:
        value: Mapping of the changed values associated to reference key

    Example:
        >>> tree_list = ['10.17.254.2', 'state']
        >>> value = {'new_value': 'Up', 'old_value': 'Idle'}
        {'10.17.254.2': {'state': {'new_value': 'Up', 'old_value': 'Idle'}}}
    """
    if tree_list:
        return {tree_list[0]: group_value(tree_list[1:], value)}
    return value


def dict_merger(original_dict: List, merged_dict: Mapping):
    """
    Merge dictionaries to build final result.

    Args:
        original_dict: empty dictionary to be merged
        merged_dict: dictionary containing returned key/value and associated reference key

    Example:
        >>> original_dict = {}
        >>> merged_dict = {'10.17.254.2': {'state': {'new_value': 'Up', 'old_value': 'Idle'}}}
        {'10.17.254.2': {'state': {'new_value': 'Up', 'old_value': 'Idle'}}}
    """
    for key in merged_dict.keys():
        if key in original_dict and isinstance(original_dict[key], dict) and isinstance(merged_dict[key], DictMapping):
            dict_merger(original_dict[key], merged_dict[key])
        else:
            original_dict[key] = merged_dict[key]
