"""JMSPath expresion parsers."""
import re


def jmspath_value_parser(path: str):
    """
    Get the JMSPath value path from 'path'.

    Args:
        path: "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
    Return:
        "result[0].vrfs.default.peerList[*].[prefixesReceived]"
    """
    regex_match_value = re.search(r"\$.*\$\.|\$.*\$,|,\$.*\$", path)

    if not regex_match_value:
        return path
    # $peers$. --> peers
    regex_normalized_value = re.search(r"\$.*\$", regex_match_value.group())
    if regex_normalized_value:
        normalized_value = regex_match_value.group().split("$")[1]
        return path.replace(regex_normalized_value.group(), normalized_value)

    return path


def jmspath_refkey_parser(path: str):
    """
    Get the JMSPath reference key path from 'path'.

    Args:
        path: "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
    Return:
        "result[0].vrfs.default.peerList[*].[$peerAddress$]"
    """
    splitted_jmspath = path.split(".")

    for number, element in enumerate(splitted_jmspath):
        regex_match_anchor = re.search(r"\$.*\$", element)

        if regex_match_anchor:
            splitted_jmspath[number] = regex_match_anchor.group().replace("$", "")

        if regex_match_anchor and not element.startswith("[") and not element.endswith("]"):
            splitted_jmspath = splitted_jmspath[: number + 1]

    return ".".join(splitted_jmspath)
