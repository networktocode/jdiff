"""Diff helpers."""

import re
from collections import defaultdict
from functools import partial, reduce
from operator import getitem
from typing import DefaultDict, Dict, List, Mapping

REGEX_PATTERN_RELEVANT_KEYS = r"'([A-Za-z0-9_\./\\-]*)'"


def get_diff_iterables_items(diff_result: Mapping) -> DefaultDict:
    """Helper function for diff_generator to postprocess changes reported by DeepDiff for iterables.

    DeepDiff iterable_items are returned when the source data is a list
    and provided in the format: `"root['Ethernet3'][1]"`
    or more generically: `root['KEY']['KEY']['KEY']...[numeric_index]`
    where the KEYs are dict keys within the original object
    and the `"[index]"` is appended to indicate the position within the list.

    Args:
        diff_result: iterable comparison result from DeepDiff
    Returns:
        Return a dict with new and missing values where the values are in a list.
    """
    get_dict_keys = re.compile(r"^root((\['\w.*'\])+)\[\d+\]$")

    defaultdict_list = partial(defaultdict, list)  # type: partial
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
            ```
            {
                "root[3]['7.7.7.7']['is_enabled']": {'new_value': False, 'old_value': True},
                "root[3]['7.7.7.7']['is_up']": {'new_value': False, 'old_value': True}
            }
            ```

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


def _parse_index_element_string(index_element_string):
    """Build out dictionary from the index element string."""
    result = {}
    pattern = r"\[\'(.*?)\'\]"
    match = re.findall(pattern, index_element_string)
    if match:
        for inner_key in match[1::]:
            result[inner_key] = ""
    return match, result


def set_nested_value(data, keys, value):
    """
    Recursively sets a value in a nested dictionary, given a list of keys.

    Args:
        data (dict): The nested dictionary to modify.
        keys (list): A list of keys to access the target value.
        value (str): The value to set.

    Returns:
        None (None): The function modifies the dictionary in place.  Returns None.
    """
    if not keys:
        return  # Should not happen, but good to have.
    if len(keys) == 1:
        data[keys[0]] = value
    else:
        if keys[0] not in data:
            data[keys[0]] = {}  # Create the nested dictionary if it doesn't exist
        set_nested_value(data[keys[0]], keys[1:], value)


def parse_diff(jdiff_evaluate_response, actual, intended, match_config):
    """Parse jdiff evaluate result into missing and extra dictionaries.

    Dict value in jdiff_evaluate_response can be:
    - 'missing'  ->  In the intended but missing from actual.
    - 'new'  -> In the actual missing from intended.

    Examples of jdiff_evaluate_response:
    - {'bar-2': 'missing', 'bar-1': 'new'}
    - {'hostname': {'new_value': 'veos-actual', 'old_value': 'veos-intended'}, 'domain-name': 'new'}
    - {'hostname': {'new_value': 'veos-0', 'old_value': 'veos'}, "index_element['ip name']": 'missing', 'domain-name': 'new'}
    - {'servers': {'server': defaultdict(<class 'list'>, {'missing': [{'address': '1.us.pool.ntp.org', 'config': {'address': '1.us.pool.ntp.org'}, 'state': {'address': '1.us.pool.ntp.org'}}]})}}
    """
    # Remove surrounding double quotes if present from jmespath/config-to-match match with - in the string.
    match_config = match_config.strip('"')
    extra = {}  # In the actual missing from intended.
    missing = {}  # In the intended but missing from actual.

    def process_diff(_map, extra_map, missing_map, previous_key=None):
        """Process the diff recursively."""
        for key, value in _map.items():
            if isinstance(value, dict) and all(nested_key in value for nested_key in ("new_value", "old_value")):
                extra_map[key] = value["new_value"]
                missing_map[key] = value["old_value"]
            elif isinstance(value, str):
                if "missing" in value and "index_element" in key:
                    key_chain, _ = _parse_index_element_string(key)
                    if len(key_chain) == 1:
                        missing_map[key_chain[0]] = intended.get(match_config, {}).get(key_chain[0])
                    else:
                        new_value = reduce(getitem, key_chain, intended)
                        set_nested_value(extra_map, key_chain[1::], new_value)
                elif "missing" in value:
                    missing_map[key] = intended.get(match_config, {}).get(key)
                else:
                    if "new" in value:
                        extra_map[key] = actual.get(match_config, {}).get(key)
            elif isinstance(value, defaultdict):
                value_dict = dict(value)
                if "new" in value_dict:
                    extra_map[previous_key][key] = value_dict.get("new", {})
                if "missing" in value_dict:
                    missing_map[previous_key][key] = value_dict.get("missing", {})
            elif isinstance(value, dict):
                extra_map[key] = {}
                missing_map[key] = {}
                process_diff(value, extra_map, missing_map, previous_key=key)
        return extra_map, missing_map

    extras, missing = process_diff(jdiff_evaluate_response, extra, missing)
    # Don't like this, but with less the performant way of doing it right now it works to clear out
    # Any empty dicts that are left over from the diff.
    final_extras = extras.copy()
    final_missing = missing.copy()
    for key, value in extras.items():
        if isinstance(value, dict) and not value:
            del final_extras[key]
    for key, value in missing.items():
        if isinstance(value, dict) and not value:
            del final_missing[key]
    # Pop the root "index_element" key.
    if final_extras.get("index_element"):
        final_extras.update(final_extras.pop("index_element"))
    if final_missing.get("index_element"):
        final_missing.update(final_missing.pop("index_element"))
    return final_extras, final_missing
