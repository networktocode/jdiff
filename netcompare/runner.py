#!/ur/bin/env python3
import re
import jmespath
from typing import Mapping, List, Union
from .utils.jmspath.parsers import jmspath_value_parser, jmspath_refkey_parser
from .utils.data.parsers import exclude_filter, get_values
from .utils.refkey.utils import keys_cleaner, keys_values_zipper


def extract_values_from_output(value: Mapping, path: Mapping, exclude: List) -> Union[Mapping, List, int, str, bool]:
    """Return data from output depending on the check path. See unit text for complete example.

    Args:
        path: "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]",
        value: {
            "jsonrpc": "2.0",
            "id": "EapiExplorer-1",
            "result": [
                {
                "vrfs": {
                    "default": {
                    "peerList": [
                        { ...
        exclude: ["interfaceStatistics", "interfaceCounters"]

    Return:
        [{'7.7.7.7': {'prefixesReceived': 101}}, {'10.1.0.0': {'prefixesReceived': 120}}, ...
    """
    # Get the wanted values to be evaluated if jmspath expression is defined.
    if path:
        wanted_value = jmespath.search(jmspath_value_parser(path), value)
    # Take all the entir output if jmespath is not defined in check. This cover the "raw" diff type.
    else:
        wanted_value = value

    # Exclude filter implementation.
    if exclude:
        # Update list in place but assign to a new var for name consistency.
        exclude_filter(wanted_value, exclude)
        filtered_value = wanted_value

    filtered_value = get_values(path, wanted_value)

    if path and re.search(r"\$.*\$", path):
        wanted_reference_keys = jmespath.search(jmspath_refkey_parser(path), value)
        list_of_reference_keys = keys_cleaner(wanted_reference_keys)
        return keys_values_zipper(list_of_reference_keys, filtered_value)
    else:
        return filtered_value


def associate_key_of_my_value(paths: Mapping, wanted_value: List) -> List:
    """
    Associate each key defined in path to every value found in output.

    Args:
        paths: {"path": "global.peers.*.[is_enabled,is_up]"}
        wanted_value: [[True, False], [True, False], [True, False], [True, False]]

    Return:
        [{'is_enabled': True, 'is_up': False}, ...

    Example:
        >>> from runner import associate_key_of_my_value
        >>> path = {"path": "global.peers.*.[is_enabled,is_up]"}
        >>> wanted_value = [[True, False], [True, False], [True, False], [True, False]]
        {'is_enabled': True, 'is_up': False}, {'is_enabled': True, 'is_up': False}, ...
    """

    # global.peers.*.[is_enabled,is_up] / result.[*].state
    find_the_key_of_my_values = paths.split(".")[-1]

    # [is_enabled,is_up]
    if find_the_key_of_my_values.startswith("[") and find_the_key_of_my_values.endswith("]"):
        # ['is_enabled', 'is_up']
        my_key_value_list = find_the_key_of_my_values.strip("[]").split(",")
    # state
    else:
        my_key_value_list = [find_the_key_of_my_values]

    final_list = list()

    for items in wanted_value:
        temp_dict = dict()

        if len(items) != len(my_key_value_list):
            raise ValueError("Key's value len != from value len")

        for my_index, my_value in enumerate(items):
            temp_dict.update({my_key_value_list[my_index]: my_value})
        final_list.append(temp_dict)

    return final_list

