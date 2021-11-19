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