import re
from typing import Mapping


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
