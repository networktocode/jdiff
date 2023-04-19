"""jmespath parser unit tests."""
import pytest
from jdiff.utils.jmespath_parsers import (
    jmespath_value_parser,
    jmespath_refkey_parser,
    keys_values_zipper,
    associate_key_of_my_value,
    multi_reference_keys,
)
from .utility import load_json_file, ASSERT_FAIL_MESSAGE


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


value_parser_tests = [
    value_parser_case_1,
    value_parser_case_2,
    value_parser_case_3,
    value_parser_case_4,
]


@pytest.mark.parametrize("path, expected_output", value_parser_tests)
def test_value_parser(path, expected_output):
    output = jmespath_value_parser(path)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)


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
    "result[0]",
)
keyref_parser_case_5 = (
    "global.peers.$*$.*.ipv4.[accepted_prefixes,received_prefixes,sent_prefixes]",
    "global.peers",
)


keyref_parser_tests = [
    keyref_parser_case_1,
    keyref_parser_case_2,
    keyref_parser_case_3,
    keyref_parser_case_4,
    keyref_parser_case_5,
]


@pytest.mark.parametrize("path, expected_output", keyref_parser_tests)
def test_keyref_parser(path, expected_output):
    output = jmespath_refkey_parser(path)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)


keys_zipper_case_1 = (
    ["10.1.0.0", "10.2.0.0"],
    [{"is_enabled": False, "is_up": False}, {"is_enabled": True, "is_up": True}],
    [{"10.1.0.0": {"is_enabled": False, "is_up": False}}, {"10.2.0.0": {"is_enabled": True, "is_up": True}}],
)


keys_zipper_tests = [
    keys_zipper_case_1,
]


@pytest.mark.parametrize("ref_keys, wanted_values, expected_output", keys_zipper_tests)
def test_keys_zipper(ref_keys, wanted_values, expected_output):
    output = keys_values_zipper(ref_keys, wanted_values)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)


keys_association_case_1 = (
    "global.peers.*.[is_enabled,is_up]",
    [[True, False], [True, False]],
    [{"is_enabled": True, "is_up": False}, {"is_enabled": True, "is_up": False}],
)


keys_association_test = [
    keys_association_case_1,
]


@pytest.mark.parametrize("path, wanted_values, expected_output", keys_association_test)
def test_keys_association(path, wanted_values, expected_output):
    output = associate_key_of_my_value(path, wanted_values)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)


multi_ref_key_case_1 = (
    "$*$.peers.$*$.*.ipv4.[accepted_prefixes]",
    ["global.10.1.0.0", "global.10.2.0.0", "global.10.64.207.255", "global.7.7.7.7", "vpn.10.1.0.0", "vpn.10.2.0.0"],
)


multi_ref_key_case_2 = (
    "$*$.peers.$*$.address_family.$*$.[accepted_prefixes]",
    [
        "global.10.1.0.0.ipv4",
        "global.10.1.0.0.ipv6",
        "global.10.2.0.0.ipv4",
        "global.10.2.0.0.ipv6",
        "global.10.64.207.255.ipv4",
        "global.10.64.207.255.ipv6",
        "global.7.7.7.7.ipv4",
        "global.7.7.7.7.ipv6",
        "vpn.10.1.0.0.ipv4",
        "vpn.10.1.0.0.ipv6",
        "vpn.10.2.0.0.ipv4",
        "vpn.10.2.0.0.ipv6",
    ],
)


multi_ref_key_test_cases = [
    multi_ref_key_case_1,
    multi_ref_key_case_2,
]


@pytest.mark.parametrize("path, expected_output", multi_ref_key_test_cases)
def test_multi_ref_key(path, expected_output):
    data = load_json_file("napalm_get_bgp_neighbors", "multi_vrf.json")
    output = multi_reference_keys(path, data)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)
