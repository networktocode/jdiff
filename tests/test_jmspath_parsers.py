"""JMSPath parser unit tests."""
import pytest
from netcompare.utils.jmspath_parsers import jmspath_value_parser, jmspath_refkey_parser
from .utility import ASSERT_FAIL_MESSAGE


value_parser_case_1 = (
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]",
    "result[0].vrfs.default.peerList[*].[prefixesReceived]",
)
value_parser_case_2 = (
    "result[0].vrfs.default.peerList[*].[peerAddress,$prefixesReceived$]",
    "result[0].vrfs.default.peerList[*].[peerAddress]",
)
value_parser_case_3 = (
    "result[0].vrfs.default.peerList[*].[interfaceCounters,$peerAddress$,prefixesReceived]",
    "result[0].vrfs.default.peerList[*].[interfaceCounters,prefixesReceived]",
)
value_parser_case_4 = (
    "result[0].$vrfs$.default.peerList[*].[peerAddress,prefixesReceived]",
    "result[0].vrfs.default.peerList[*].[peerAddress,prefixesReceived]",
)

keyref_parser_case_1 = (
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]",
    "result[0].vrfs.default.peerList[*].peerAddress",
)
keyref_parser_case_2 = (
    "result[0].vrfs.default.peerList[*].[peerAddress,$prefixesReceived$]",
    "result[0].vrfs.default.peerList[*].prefixesReceived",
)
keyref_parser_case_3 = (
    "result[0].vrfs.default.peerList[*].[interfaceCounters,$peerAddress$,prefixesReceived]",
    "result[0].vrfs.default.peerList[*].peerAddress",
)
keyref_parser_case_4 = (
    "result[0].$vrfs$.default.peerList[*].[peerAddress,prefixesReceived]",
    "result[0].vrfs",
)


value_parser_tests = [
    value_parser_case_1,
    value_parser_case_2,
    value_parser_case_3,
    value_parser_case_4,
]

keyref_parser_tests = [
    keyref_parser_case_1,
    keyref_parser_case_2,
    keyref_parser_case_3,
    keyref_parser_case_4,
]


@pytest.mark.parametrize("path, expected_output", value_parser_tests)
def test_value_parser(path, expected_output):
    output = jmspath_value_parser(path)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)


@pytest.mark.parametrize("path, expected_output", keyref_parser_tests)
def test_keyref_parser(path, expected_output):
    output = jmspath_refkey_parser(path)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)
