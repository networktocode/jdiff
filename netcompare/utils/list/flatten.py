from typing import List, Generator


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
        [[[[-1, 0], [-1, 0]]]]
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
