from typing import Mapping, List
from ..jmspath.parsers import jmspath_value_parser
from ..list.flatten import flatten_list
from ...runner import associate_key_of_my_value

def exclude_filter(data: Mapping, exclude: List):
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
                exclude_filter(data[key], exclude)

    elif isinstance(data, list):
        for element in data:
            if isinstance(element, dict) or isinstance(element, list):
                exclude_filter(element, exclude)


def get_values(path: Mapping, wanted_value):
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