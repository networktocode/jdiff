from typing import Mapping, List


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
