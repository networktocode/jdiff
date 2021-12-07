from typing import Mapping, List


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

        if isinstance(wanted_reference_keys, dict): 
            for key in wanted_reference_keys.keys():
                my_keys_list.append(key)
        else:
            raise TypeError(f'Must be a dictionary. You have type:{type(wanted_reference_keys)} output:{wanted_reference_keys}\'.')
                    
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
