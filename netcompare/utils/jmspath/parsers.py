import re
from typing import Mapping, List

def jmspath_value_parser(path: Mapping):
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


def jmspath_refkey_parser(path: Mapping):
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