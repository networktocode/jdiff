#!/ur/bin/env python3
import re
import jmespath
from typing import Mapping, List, Generator, Union


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
        exclude: [...]

    TODO: This function should be able to return a list, or a Dict, or a Integer, or a Boolean or a String
    Return:
        [{'7.7.7.7': {'prefixesReceived': 101}}, {'10.1.0.0': {'prefixesReceived': 120}}, ...
    """

    if path:
        found_values = jmespath.search(jmspath_value_parser(path), value)
    else:
        found_values = value

    if exclude:
        my_value_exclude_cleaner(found_values, exclude)
        my_meaningful_values = found_values
    else:
        my_meaningful_values = get_meaningful_values(path, found_values)

    if path and re.search(r"\$.*\$", path):
        wanted_reference_keys = jmespath.search(jmspath_refkey_parser(path), value)
        list_of_reference_keys = keys_cleaner(wanted_reference_keys)
        return keys_values_zipper(list_of_reference_keys, my_meaningful_values)
    else:
        return my_meaningful_values


def jmspath_value_parser(path):
    """
    Get the JMSPath  value path from 'path'.

    Args:
        path: "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
    Return:
        "result[0].vrfs.default.peerList[*].[prefixesReceived]"
    """
    regex_match_value = re.search(r"\$.*\$\.|\$.*\$,|,\$.*\$", path)

    if regex_match_value:
        # $peers$. --> peers
        regex_normalized_value = re.search(r"\$.*\$", regex_match_value.group())
        if regex_normalized_value:
            normalized_value = regex_match_value.group().split("$")[1]
        value_path = path.replace(regex_normalized_value.group(), normalized_value)
    else:
        value_path = path

    return value_path


def jmspath_refkey_parser(path):
    """
    Get the JMSPath reference key path from 'path'.

    Args:
        path: "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
    Return:
        "result[0].vrfs.default.peerList[*].[$peerAddress$]"
    """
    splitted_jmspath = path.split(".")

    for n, i in enumerate(splitted_jmspath):
        regex_match_anchor = re.search(r"\$.*\$", i)

        if regex_match_anchor:
            splitted_jmspath[n] = regex_match_anchor.group().replace("$", "")

        if regex_match_anchor and not i.startswith("[") and not i.endswith("]"):
            splitted_jmspath = splitted_jmspath[: n + 1]

    return ".".join(splitted_jmspath)


def get_meaningful_values(path, found_values):
    if path:
        # check if list of lists
        if not any(isinstance(i, list) for i in found_values):
            raise TypeError(
                "Catching value must be defined as list in jmespath expression i.e. result[*].state -> result[*].[state]. You have {}'.".format(
                    path
                )
            )
        for element in found_values:
            for item in element:
                if isinstance(item, dict):
                    raise TypeError(
                        'Must be list of lists i.e. [["Idle", 75759616], ["Idle", 75759620]]. You have {}\'.'.format(
                            found_values
                        )
                    )
                elif isinstance(item, list):
                    found_values = flatten_list(found_values)
                    break

        my_meaningful_values = associate_key_of_my_value(jmspath_value_parser(path), found_values)
    else:
        my_meaningful_values = found_values
    return my_meaningful_values


def my_value_exclude_cleaner(data: Mapping, exclude: List):
    """
    Recusively look through all dict keys and pop out the one defined in "exclude".

    Update in place existing dictionary. Look into unit test for example.

    Args:
        data: {
                "interfaces": {
                "Management1": {
                    "name": "Management1",
                    "interfaceStatus": "connected",
                    "autoNegotiate": "success",
                    "interfaceStatistics": {
                        "inBitsRate": 3403.4362520883615,
                        "inPktsRate": 3.7424095978179257,
                        "outBitsRate": 16249.69114419833,
                        "updateInterval": 300,
                        "outPktsRate": 2.1111866059750692
                    },...
        exclude: ["interfaceStatistics", "interfaceCounters"]
    """
    if isinstance(data, dict):
        for exclude_element in exclude:
            try:
                data.pop(exclude_element)
            except KeyError:
                pass

        for key in data:
            if isinstance(data[key], dict) or isinstance(data[key], list):
                my_value_exclude_cleaner(data[key], exclude)

    elif isinstance(data, list):
        for element in data:
            if isinstance(element, dict) or isinstance(element, list):
                my_value_exclude_cleaner(element, exclude)


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


def associate_key_of_my_value(paths: Mapping, found_values: List) -> List:
    """
    Associate each key defined in path to every value found in output.

    Args:
        paths: {"path": "global.peers.*.[is_enabled,is_up]"}
        found_values: [[True, False], [True, False], [True, False], [True, False]]

    Return:
        [{'is_enabled': True, 'is_up': False}, ...

    Example:
        >>> from runner import associate_key_of_my_value
        >>> path = {"path": "global.peers.*.[is_enabled,is_up]"}
        >>> found_values = [[True, False], [True, False], [True, False], [True, False]]
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

    for items in found_values:
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


def keys_values_zipper(list_of_reference_keys: List, found_values_with_key: List) -> List:
    """
    Build dictionary zipping keys with relative values.

    Args:
        list_of_reference_keys: ['10.1.0.0', '10.2.0.0', '10.64.207.255', '7.7.7.7']
        found_values_with_key: [{'is_enabled': True, 'is_up': False}, ...

    Return:
        [{'10.1.0.0': {'is_enabled': True, 'is_up': False}}, , ...

    Example:
        >>> from runner import keys_values_zipper
        >>> list_of_reference_keys = ['10.1.0.0']
        >>> found_values_with_key = [{'is_enabled': True, 'is_up': False}]
        >>> keys_values_zipper(list_of_reference_keys, found_values_with_key)
        [{'10.1.0.0': {'is_enabled': True, 'is_up': False}}]
    """
    final_result = list()

    if len(list_of_reference_keys) != len(found_values_with_key):
        raise ValueError("Keys len != from Values len")

    for my_index, my_key in enumerate(list_of_reference_keys):
        final_result.append({my_key: found_values_with_key[my_index]})

    return final_result
