"""Diff helpers."""
import re
from collections import defaultdict
from functools import partial
from typing import Mapping, Dict, List, DefaultDict

REGEX_PATTERN_RELEVANT_KEYS = r"'([A-Za-z0-9_\./\\-]*)'"


def get_diff_iterables_items(diff_result: Mapping) -> DefaultDict:
    """Helper function for diff_generator to postprocess changes reported by DeepDiff for iterables.

    DeepDiff iterable_items are returned when the source data is a list
    and provided in the format: "root['Ethernet3'][1]"
    or more generically: root['KEY']['KEY']['KEY']...[numeric_index]
    where the KEYs are dict keys within the original object
    and the "[index]" is appended to indicate the position within the list.

    Args:
        diff_result: iterable comparison result from DeepDiff
    Returns:
        Return a dict with new and missing values where the values are in a list.
    """
    get_dict_keys = re.compile(r"^root((\['\w.*'\])+)\[\d+\]$")

    defaultdict_list = partial(defaultdict, list)
    result = defaultdict(defaultdict_list)  # type: DefaultDict

    items_removed = diff_result.get("iterable_item_removed")
    if items_removed:
        for key, value in items_removed.items():
            re_key = get_dict_keys.match(key)
            if re_key:  # Change only if there is a match, otherwise retain the key.
                key, *_ = re_key.groups()
            result[key]["missing"].append(value)

    items_added = diff_result.get("iterable_item_added")
    if items_added:
        for key, value in items_added.items():
            re_key = get_dict_keys.match(key)
            if re_key:
                key, *_ = re_key.groups()
            result[key]["new"].append(value)

    return result


def fix_deepdiff_key_names(obj: Mapping) -> Dict:
    """Return a dict based on the provided dict object where the brackets and quotes are removed from the string.

    Args:
        obj (Mapping): Mapping to be fixed. For example:
            {
                "root[3]['7.7.7.7']['is_enabled']": {'new_value': False, 'old_value': True},
                "root[3]['7.7.7.7']['is_up']": {'new_value': False, 'old_value': True}
            }

    Returns:
        Dict: aggregated output, for example: {'7.7.7.7': {'is_enabled': {'new_value': False, 'old_value': True},
                                                'is_up': {'new_value': False, 'old_value': True}}}
    """
    result = {}  # type: Dict
    for key, value in obj.items():
        key_parts = re.findall(REGEX_PATTERN_RELEVANT_KEYS, key)
        if not key_parts:  # If key parts can't be find, keep original key so data is not lost.
            key_parts = [key.replace("root", "index_element")]  # replace root from DeepDiff with more meaningful name.
        partial_res = group_value(key_parts, value)
        dict_merger(result, partial_res)
    return result


def group_value(tree_list: List, value: Dict) -> Dict:
    """Function to create a nested Dict by recursively use the tree_list as nested keys."""
    if tree_list:
        return {tree_list[0]: group_value(tree_list[1:], value)}
    return value


def dict_merger(original_dict: Dict, dict_to_merge: Dict):
    """Function to merge a dictionary (dict_to_merge) recursively into the original_dict."""
    for key in dict_to_merge.keys():
        if key in original_dict and isinstance(original_dict[key], dict) and isinstance(dict_to_merge[key], dict):
            dict_merger(original_dict[key], dict_to_merge[key])
        elif key in original_dict.keys():
            original_dict[key + "_dup!"] = dict_to_merge[key]  # avoid overwriting existing keys.
        else:
            original_dict[key] = dict_to_merge[key]
