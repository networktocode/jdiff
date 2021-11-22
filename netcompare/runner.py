#!/ur/bin/env python3
import re
import jmespath
from typing import Mapping, List, Union
from .utils.jmspath_parsers import jmspath_value_parser, jmspath_refkey_parser
from .utils.filter_parsers import exclude_filter, get_values
from .utils.refkey_utils import keys_cleaner, keys_values_zipper


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




