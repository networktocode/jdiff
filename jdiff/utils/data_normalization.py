"""Data Normalization utilities."""
from typing import List, Generator, Union, Dict


def flatten_list(my_list: List) -> List:
    """
    Flatten a multi level nested list and returns a list of lists.

    This normalization step is required since jmespath can return nested lists containing the
    wanted value. This depends how much nested is the wanted value in the json output.

    Having a list of lists will help us to assert that we have the number of values we have, will
    match the number of reference keys found in json object.

    Args:
        my_list: nested list to be flattened.

    Return:
        [[-1, 0], [-1, 0], [-1, 0], ...]

    Example:
        >>> my_list = [[[[-1, 0], [-1, 0]]]]
        >>> flatten_list(my_list)
        [[-1, 0], [-1, 0]]
    """

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

    if not isinstance(my_list, list):
        raise ValueError(f"Argument provided must be a list. You passed a {type(my_list)}")
    if is_flat_list(my_list):
        return my_list
    return list(iter_flatten_list(my_list))


def exclude_filter(data: Union[Dict, List], exclude: List):
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
            if isinstance(data[key], (dict, list)):
                exclude_filter(data[key], exclude)

    elif isinstance(data, list):
        for element in data:
            if isinstance(element, (dict, list)):
                exclude_filter(element, exclude)
