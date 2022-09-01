"""Extract data from JSON. Based on custom JMSPath implementation."""
import re
import warnings
from typing import Mapping, List, Dict, Any, Union
import jmespath
from .utils.data_normalization import exclude_filter, flatten_list
from .utils.jmespath_parsers import (
    jmespath_value_parser,
    jmespath_refkey_parser,
    associate_key_of_my_value,
    keys_values_zipper,
)


def extract_data_from_json(data: Union[Mapping, List], path: str = "*", exclude: List = None) -> Any:
    """Return wanted data from outpdevice data based on the check path. See unit test for complete example.

    Get the wanted values to be evaluated if JMESPath expression is defined,
    otherwise use the entire data if jmespath is not defined in check. This covers the "raw" diff type.
    Exclude data not desired to compare.

    Notes:
        https://jmespath.org/ shows how JMESPath works.

    Args:
        data: json data structure
        path: JMESPath to extract specific values
        exclude: list of keys to exclude
    Returns:
        Evaluated data, may be anything depending on JMESPath used.
    """
    if exclude and isinstance(data, Dict):
        if not isinstance(exclude, list):
            raise ValueError(f"Exclude list must be defined as a list. You have {type(exclude)}")
        # exclude unwanted elements
        exclude_filter(data, exclude)

    if not path:
        warnings.warn("JMSPath cannot be empty string or type 'None'. Path argument reverted to default value '*'")
        path = "*"

    if path == "*":
        # return if path is not specified
        return data

    values = jmespath.search(jmespath_value_parser(path), data)

    if values is None:
        raise TypeError("JMSPath returned 'None'. Please, verify your JMSPath regex.")

    # check for multi-nested lists if not found return here
    if not any(isinstance(i, list) for i in values):
        return values

    # process elements to check if lists should be flattened
    for element in values:
        for item in element:
            # raise if there is a dict, path must be more specific to extract data
            if isinstance(item, dict):
                raise TypeError(
                    f'Must be list of lists i.e. [["Idle", 75759616], ["Idle", 75759620]]. You have "{values}".'
                )
            if isinstance(item, list):
                values = flatten_list(values)  # flatten list and rewrite values
                break  # items are the same, need to check only first to see if this is a nested list

    paired_key_value = associate_key_of_my_value(jmespath_value_parser(path), values)

    # We need to get a list of reference keys - list of strings.
    # Based on the expression or data we might have different data types
    # therefore we need to normalize.
    if re.search(r"\$.*\$", path):
        wanted_reference_keys = jmespath.search(jmespath_refkey_parser(path), data)

        if isinstance(wanted_reference_keys, dict):  # when wanted_reference_keys is dict() type
            list_of_reference_keys = list(wanted_reference_keys.keys())
        elif any(
            isinstance(element, list) for element in wanted_reference_keys
        ):  # when wanted_reference_keys is a nested list
            list_of_reference_keys = flatten_list(wanted_reference_keys)[0]
        elif isinstance(wanted_reference_keys, list):  # when wanted_reference_keys is a list
            list_of_reference_keys = wanted_reference_keys
        else:
            raise ValueError("Reference Key normalization failure. Please verify data type returned.")

        return keys_values_zipper(list_of_reference_keys, paired_key_value)

    return values
