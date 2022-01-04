"""Diff helpres."""
import re
from collections import defaultdict
from functools import partial
from typing import Mapping, Dict, List


def get_diff_iterables_items(diff_result: Mapping) -> Dict:
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


def fix_deepdiff_key_names(obj: Mapping) -> Dict:
    """Return a dict based on the provided dict object where the brackets and quotes are removed from the string.

    Args:
        obj: Example: {"root[3]['7.7.7.7']['is_enabled']": {'new_value': False, 'old_value': True},
                       "root[3]['7.7.7.7']['is_up']": {'new_value': False, 'old_value': True}}

    Returns:
        aggregated output Example: {'7.7.7.7': {'is_enabled': {'new_value': False, 'old_value': True},
                                                'is_up': {'new_value': False, 'old_value': True}}}
    """
    pattern = r"'([A-Za-z0-9_\./\\-]*)'"

    result = {}
    for key, value in obj.items():
        key_parts = re.findall(pattern, key)
        partial_res = group_value(key_parts, value)
        dict_merger(result, partial_res)
    return result


def group_value(tree_list: List, value: Dict) -> Dict:
    """Build dictionary based on value's key and reference key."""
    if tree_list:
        return {tree_list[0]: group_value(tree_list[1:], value)}
    return value


def dict_merger(original_dict: Dict, merged_dict: Dict):
    """Merge dictionaries to build final result."""
    for key in merged_dict.keys():
        if key in original_dict and isinstance(original_dict[key], dict) and isinstance(merged_dict[key], dict):
            dict_merger(original_dict[key], merged_dict[key])
        else:
            original_dict[key] = merged_dict[key]
