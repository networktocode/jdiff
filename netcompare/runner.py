"""Library wrapper for output parsing."""
import re
from typing import Mapping, List, Union, Any
import jmespath
from .utils.jmspath_parsers import jmspath_value_parser, jmspath_refkey_parser
from .utils.filter_parsers import exclude_filter
from .utils.refkey import keys_cleaner, keys_values_zipper, associate_key_of_my_value
from .utils.flatten import flatten_list


def extract_values_from_output(output: Union[Mapping, List], path: str, exclude: List = None) -> Any:
    """Return data from output depending on the check path. See unit test for complete example.

    Get the wanted values to be evaluated if JMESPath expression is defined,
    otherwise use the entire output if jmespath is not defined in check. This covers the "raw" diff type.
    Exclude data not desired to compare.

    Notes:
        https://jmespath.org/ shows how JMESPath works.

    Args:
        output: json data structure
        path: JMESPath to extract specific values
        exclude: list of keys to exclude
    Returns:
        Evaluated data, may be anything depending on JMESPath used.
    """
    if exclude:
        exclude_filter(output, exclude)  # exclude unwanted elements

    if not path:
        return output  # return if path is not specified

    values = jmespath.search(jmspath_value_parser(path), output)

    if not any(isinstance(i, list) for i in values):  # check for multi-nested lists if not found return here
        return values

    for element in values:  # process elements to check is lists should be flatten
        for item in element:
            if isinstance(item, dict):  # raise if there is a dict, path must be more specific to extract data
                raise TypeError(
                    f'Must be list of lists i.e. [["Idle", 75759616], ["Idle", 75759620]].' f"You have {values}'."
                )
            if isinstance(item, list):
                values = flatten_list(values)  # flatten list and rewrite values
                break  # items are the same, need to check only first to see if this is a nested list

    paired_key_value = associate_key_of_my_value(jmspath_value_parser(path), values)

    if re.search(r"\$.*\$", path):  # normalize
        wanted_reference_keys = jmespath.search(jmspath_refkey_parser(path), output)
        list_of_reference_keys = keys_cleaner(wanted_reference_keys)
        return keys_values_zipper(list_of_reference_keys, paired_key_value)

    return values
