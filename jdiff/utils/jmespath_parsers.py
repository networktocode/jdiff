"""
jmespath expression parsers and related utilities.

This utility interfaces the custom jdiff jmespath expression with the jmespath library.
From one expression defined in jdiff, we will derive two expressions: one expression that traverse the json output and get the
evaluated bit of it, the second will target the reference key relative to the value to evaluate. More on README.md
"""
import re
from typing import Mapping, List, Union

import jmespath


def jmespath_value_parser(path: str):
    """
    Extract the jmespath value path from 'path' argument.

    This is required as we use custom anchors ($$) to identify the reference key.
    So the expression must be parsed and stripped of the reference key anchor. More info on README.md

    Two combinations are possible based on where reference key is defined. See example below.

    Args:
        path: "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
        path: "result[0].$vrfs$.default.peerList[*].[peerAddress, prefixesReceived]"

    Return:
        "result[0].vrfs.default.peerList[*].[prefixesReceived]"
        "result[0].vrfs.default.peerList[*].[peerAddress, prefixesReceived]"
    """
    regex_ref_key = re.compile(r"\$.*\$\.|\$.*\$,|,\$.*\$")
    regex_match_ref_key = regex_ref_key.search(path)
    path_suffix = path.split(".")[-1]

    if regex_match_ref_key:
        reference_key = regex_match_ref_key.group()
        if regex_ref_key.search(path_suffix):
            # [$peerAddress$,prefixesReceived] --> [prefixesReceived]
            return path.replace(reference_key, "")

        # result[0].$vrfs$.default... --> result[0].vrfs.default....
        regex_normalized_value = re.search(r"\$.*\$", reference_key)
        if regex_normalized_value:
            normalized_value = reference_key.split("$")[1]
            return path.replace(regex_normalized_value.group(), normalized_value)
    return path


def jmespath_refkey_parser(path: str):
    """
    Get the jmespath reference key path from 'path' argument.

    Reference key is define within $$ in 'path' and will be associated to the value/s to be evaluated.
    More on README.md.

    Args:
        path: "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
    Return:
        "result[0].vrfs.default.peerList[*].[$peerAddress$]"
    """
    splitted_jmespath = path.split(".")

    for number, element in enumerate(splitted_jmespath):
        regex_match_anchor = re.search(r"\$.*\$", element)

        if regex_match_anchor:
            splitted_jmespath[number] = regex_match_anchor.group().replace("$", "")

        if regex_match_anchor and not element.startswith("[") and not element.endswith("]"):
            splitted_jmespath = splitted_jmespath[:number]

    return ".".join(splitted_jmespath) or "@"


def associate_key_of_my_value(paths: str, wanted_value: List) -> List:
    """Associate each reference key (from: jmespath_refkey_parser) to every value found in output (from: jmespath_value_parser)."""
    # global.peers.*.[is_enabled,is_up] / result.[*].state
    find_the_key_of_my_values = paths.split(".")[-1]

    # [is_enabled,is_up]
    if find_the_key_of_my_values.startswith("[") and find_the_key_of_my_values.endswith("]"):
        # ['is_enabled', 'is_up']
        my_key_value_list = find_the_key_of_my_values.strip("[]").split(",")
    # state
    else:
        my_key_value_list = [find_the_key_of_my_values]

    final_list = []

    if not all(isinstance(item, list) for item in wanted_value) and len(my_key_value_list) == 1:
        for item in wanted_value:
            temp_dict = {my_key_value_list[0]: item}
            final_list.append(temp_dict)

    else:
        for items in wanted_value:
            if len(items) != len(my_key_value_list):
                raise ValueError("Key's value len != from value len")

            temp_dict = {my_key_value_list[my_index]: my_value for my_index, my_value in enumerate(items)}

            final_list.append(temp_dict)

    return final_list


def keys_cleaner(wanted_reference_keys: Union[Mapping, List]) -> List:
    """Get every required reference key from output and build a dictionary from it."""
    if isinstance(wanted_reference_keys, list):
        final_result = wanted_reference_keys
    elif isinstance(wanted_reference_keys, dict):
        final_result = list(wanted_reference_keys.keys())
    else:
        raise TypeError(
            f"Must be a dictionary. You have type:{type(wanted_reference_keys)} output:{wanted_reference_keys}'."
        )
    return final_result


def keys_values_zipper(list_of_reference_keys: List, wanted_value_with_key: List) -> List:
    """Build dictionary zipping keys with relative values."""
    final_result = []

    if len(list_of_reference_keys) != len(wanted_value_with_key):
        raise ValueError("Keys len != from Values len")

    for my_index, my_key in enumerate(list_of_reference_keys):
        final_result.append({my_key: wanted_value_with_key[my_index]})

    return final_result


def multi_reference_keys(jmspath, data):
    """Build a list of concatenated reference keys.

    Args:
        jmspath: "$*$.peers.$*$.*.ipv4.[accepted_prefixes]"
        data: tests/mock/napalm_get_bgp_neighbors/multi_vrf.json

    Returns:
        ["global.10.1.0.0", "global.10.2.0.0", "global.10.64.207.255", "global.7.7.7.7", "vpn.10.1.0.0", "vpn.10.2.0.0"]
    """
    ref_key_regex = re.compile(r"\$.*?\$")
    mapping = []
    split_path = jmspath.split(".")

    ref_key_index = -1  # -1 as the starting value, so it will match split path list indexes
    for index, element in enumerate(split_path):
        if ref_key_regex.search(element):
            ref_key_index += 1
            key_path = (
                ".".join(split_path[:index]).replace("$", "") or "@"
            )  # @ is for top keys, as they are stripped with "*"
            flat_path = f"{key_path}{' | []' * key_path.count('*')}"  # | [] to flatten the data, nesting level is eq to "*" count
            sub_data = jmespath.search(flat_path, data)  # extract sub-data with up to the ref key
            if isinstance(sub_data, dict):
                keys = list(sub_data.keys())
            elif isinstance(sub_data, list):
                keys = []
                for parent, children in zip(
                    mapping[ref_key_index - 1], sub_data
                ):  # refer to previous keys as they are already present in mapping
                    keys.extend(f"{parent}.{child}" for child in children.keys())  # concatenate keys
            else:
                raise ValueError("Ref key anchor must return either a dict or a list.")
            mapping.append(keys)
    return mapping[-1]  # return last element as it has all previous ref_keys concatenated.
