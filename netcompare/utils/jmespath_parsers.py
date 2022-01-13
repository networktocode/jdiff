"""jmespath expression parsers and related utilities."""
import re
from typing import Mapping, List, Optional


def jmespath_value_parser(path: str):
    """
    Get the jmespath value path from 'path'.

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
    Get the jmespath reference key path from 'path'.

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
    """Associate each key defined in path to every value found in output."""
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


def keys_cleaner(wanted_reference_keys: Mapping) -> Optional[List[Mapping]]:
    """Get every required reference key from output."""
    if isinstance(wanted_reference_keys, list):
        return wanted_reference_keys

    if isinstance(wanted_reference_keys, dict):
        my_keys_list = []

        if isinstance(wanted_reference_keys, dict):
            for key in wanted_reference_keys.keys():
                my_keys_list.append(key)
        else:
            raise TypeError(
                f"Must be a dictionary. You have type:{type(wanted_reference_keys)} output:{wanted_reference_keys}'."
            )

        return my_keys_list

    return None


def keys_values_zipper(list_of_reference_keys: List, wanted_value_with_key: List) -> List:
    """Build dictionary zipping keys with relative values."""
    final_result = []

    if len(list_of_reference_keys) != len(wanted_value_with_key):
        raise ValueError("Keys len != from Values len")

    for my_index, my_key in enumerate(list_of_reference_keys):
        final_result.append({my_key: wanted_value_with_key[my_index]})

    return final_result
