#!/ur/bin/env python3
import re
import jmespath
from typing import Mapping, List, Generator, Union
from .utils.jmspath.parsers import jmspath_value_parser, jmspath_refkey_parser, exclude_filter


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

    pdb.set_trace()
    filtered_value = get_meaningful_values(path, wanted_value)

    if path and re.search(r"\$.*\$", path):
        wanted_reference_keys = jmespath.search(jmspath_refkey_parser(path), value)
        list_of_reference_keys = keys_cleaner(wanted_reference_keys)
        return keys_values_zipper(list_of_reference_keys, filtered_value)
    else:
        return filtered_value


def get_meaningful_values(path: Mapping, wanted_value):
    if path:
        # check if list of lists
        if not any(isinstance(i, list) for i in wanted_value):
            raise TypeError(
                "Catching value must be defined as list in jmespath expression i.e. result[*].state -> result[*].[state]. You have {}'.".format(
                    path
                )
            )
        for element in wanted_value:
            for item in element:
                if isinstance(item, dict):
                    raise TypeError(
                        'Must be list of lists i.e. [["Idle", 75759616], ["Idle", 75759620]]. You have {}\'.'.format(
                            wanted_value
                        )
                    )
                elif isinstance(item, list):
                    wanted_value = flatten_list(wanted_value)
                    break

        filtered_value = associate_key_of_my_value(jmspath_value_parser(path), wanted_value)
    else:
        filtered_value = wanted_value
    return filtered_value


def flatten_list(my_list: List) -> List:
    """
    Flatten a multi level nested list and returns a list of lists.

    Args:
        my_list: nested list to be flattened.

    Return:
        [[-1, 0], [-1, 0], [-1, 0], ...]

    Example:
        >>> my_list = [[[[-1, 0], [-1, 0]]]]
        >>> flatten_list(my_list)
        [[-1, 0], [-1, 0]]
    """
    if not isinstance(my_list, list):
        raise ValueError(f"Argument provided must be a list. You passed a {type(my_list)}")
    if is_flat_list(my_list):
        return my_list
    return list(iter_flatten_list(my_list))


def iter_flatten_list(my_list: List) -> Generator[List, None, None]:
    """Recursively yield all flat lists within a given list."""
    if is_flat_list(my_list):
        yield my_list
    else:
        for item in my_list:
            yield from iter_flatten_list(item)


def is_flat_list(obj: List) -> bool:
    """Return True is obj is a list that does not contain any lists as its first order elements."""
    return isinstance(obj, list) and not any(isinstance(i, list) for i in obj)


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


def keys_cleaner(wanted_reference_keys: Mapping) -> list:
    """
    Get every required reference key from output.

    Args:
        wanted_reference_keys: {'10.1.0.0': {'address_family': {'ipv4': ...

    Return:
        ['10.1.0.0', '10.2.0.0', '10.64.207.255', '7.7.7.7']

    Example:
        >>> from runner import keys_cleaner
        >>> wanted_reference_keys = {'10.1.0.0': {'address_family': 'ipv4'}}
        >>> keys_cleaner(wanted_reference_keys)
        ['10.1.0.0', '10.2.0.0', '10.64.207.255', '7.7.7.7']
    """
    if isinstance(wanted_reference_keys, list):
        return wanted_reference_keys

    elif isinstance(wanted_reference_keys, dict):
        my_keys_list = list()

        for key in wanted_reference_keys.keys():
            my_keys_list.append(key)

        return my_keys_list


def keys_values_zipper(list_of_reference_keys: List, wanted_value_with_key: List) -> List:
    """
    Build dictionary zipping keys with relative values.

    Args:
        list_of_reference_keys: ['10.1.0.0', '10.2.0.0', '10.64.207.255', '7.7.7.7']
        wanted_value_with_key: [{'is_enabled': True, 'is_up': False}, ...

    Return:
        [{'10.1.0.0': {'is_enabled': True, 'is_up': False}}, , ...

    Example:
        >>> from runner import keys_values_zipper
        >>> list_of_reference_keys = ['10.1.0.0']
        >>> wanted_value_with_key = [{'is_enabled': True, 'is_up': False}]
        >>> keys_values_zipper(list_of_reference_keys, wanted_value_with_key)
        [{'10.1.0.0': {'is_enabled': True, 'is_up': False}}]
    """
    final_result = list()

    if len(list_of_reference_keys) != len(wanted_value_with_key):
        raise ValueError("Keys len != from Values len")

    for my_index, my_key in enumerate(list_of_reference_keys):
        final_result.append({my_key: wanted_value_with_key[my_index]})

    return final_result
