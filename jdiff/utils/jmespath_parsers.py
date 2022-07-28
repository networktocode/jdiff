"""
jmespath expression parsers and related utilities.

This utility interfaces the custom jdiff jmespath expression with the jmespath library.
From one expression defined in jdiff, we will derive two expressions: one expression that traverse the json output and get the
evaluated bit of it, the second will target the reference key relative to the value to evaluate. More on README.md
"""
import re
from typing import Mapping, List, Union


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
        if regex_ref_key.search(path_suffix):
            # [$peerAddress$,prefixesReceived] --> [prefixesReceived]
            reference_key = regex_match_ref_key.group()
            return path.replace(reference_key, "")

        # result[0].$vrfs$.default... --> result[0].vrfs.default....
        regex_normalized_value = re.search(r"\$.*\$", regex_match_ref_key.group())
        if regex_normalized_value:
            normalized_value = regex_match_ref_key.group().split("$")[1]
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
            splitted_jmespath = splitted_jmespath[: number + 1]

    return ".".join(splitted_jmespath)


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
