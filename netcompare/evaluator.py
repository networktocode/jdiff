"""Diff evaluator."""
import re
import sys
from collections import defaultdict
from functools import partial
from typing import Mapping, List, Dict
from deepdiff import DeepDiff


sys.path.append(".")


def diff_generator(pre_result: Mapping, post_result: Mapping) -> Dict:
    """Generates diff between pre and post data based on check definition."""
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
    """Return a dict with new and missing values where the values are in a list."""
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
    pattern = r"'([A-Za-z0-9_\./\\-]*)'"

    result = {}
    # root[2]['10.64.207.255']['accepted_prefixes']
    for key, value in obj.items():
        key_parts = re.findall(pattern, key)
        partial_res = group_value(key_parts, value)
        dict_merger(result, partial_res)
    return result


def group_value(tree_list: List, value: Mapping) -> Mapping:
    """Build dictionary based on value's key and reference key."""
    if tree_list:
        return {tree_list[0]: group_value(tree_list[1:], value)}
    return value


def dict_merger(original_dict: Mapping, merged_dict: Mapping):
    """Merge dictionaries to build final result."""
    for key in merged_dict.keys():
        if key in original_dict and isinstance(original_dict[key], dict) and isinstance(merged_dict[key], dict):
            dict_merger(original_dict[key], merged_dict[key])
        else:
            original_dict[key] = merged_dict[key]


def parameter_evaluator(values: Mapping, parameter: Mapping) -> Mapping:
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
