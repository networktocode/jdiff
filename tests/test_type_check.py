import sys
import pytest
from .utility import load_json_file
from netcompare.check_type import CheckType, ExactMatchType, ToleranceType

sys.path.append("..")


@pytest.mark.parametrize(
    "args, expected_class",
    [(["exact_match"], ExactMatchType), (["tolerance", 10], ToleranceType)],
)
def test_check_init(args, expected_class):
    """Validate that the returned class is the expected one."""
    assert isinstance(CheckType.init(*args), expected_class)


def test_CheckType_raises_NotImplementedError_for_invalid_check_type():
    """Validate that CheckType raises a NotImplementedError when passed a non-existant check_type."""
    with pytest.raises(NotImplementedError):
        CheckType.init("does_not_exist")


def test_CheckType_raises_NotImplementedError_when_calling_check_logic_method():
    """Validate that CheckType raises a NotImplementedError when passed a non-existant check_type."""
    with pytest.raises(NotImplementedError):
        CheckType().check_logic()


exact_match_test_values_no_change = (
    ("exact_match",),
    "api.json",
    {
        "path": "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]",
        # "reference_key_path": "result[0].vrfs.default.peerList[*].peerAddress",
    },
    ({}, True),
)

exact_match_test_values_changed = (
    ("exact_match",),
    "api.json",
    {
        "path": "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
        # "reference_key_path": "result[0].vrfs.default.peerList[*].peerAddress",
    },
    (
        {
            "10.1.0.0": {"prefixesSent": {"new_value": 52, "old_value": 50}},
            "7.7.7.7": {"prefixesSent": {"new_value": 52, "old_value": 50}},
        },
        False,
    ),
)

tolerance_test_values_no_change = (
    ("tolerance", 10),
    "api.json",
    {
        "path": "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]",
        # "reference_key_path": "result[0].vrfs.default.peerList[*].peerAddress",
    },
    ({}, True),
)

tolerance_test_values_within_threshold = (
    ("tolerance", 10),
    "api.json",
    {
        "path": "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
        # "reference_key_path": "result[0].vrfs.default.peerList[*].peerAddress",
    },
    ({}, True),
)

tolerance_test_values_beyond_threshold = (
    ("tolerance", 10),
    "api.json",
    {
        "path": "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]",
        # "reference_key_path": "result[0].vrfs.default.peerList[*].peerAddress",
    },
    (
        {
            "10.1.0.0": {"prefixesReceived": {"new_value": 120, "old_value": 100}},
            "10.64.207.255": {"prefixesReceived": {"new_value": 60, "old_value": 100}},
        },
        False,
    ),
)

check_type_tests = [
    exact_match_test_values_no_change,
    exact_match_test_values_changed,
    tolerance_test_values_no_change,
    tolerance_test_values_within_threshold,
    tolerance_test_values_beyond_threshold,
]


@pytest.mark.parametrize("check_type_args, filename, path, expected_results", check_type_tests)
def test_check_type_results(check_type_args, filename, path, expected_results):
    """Validate that CheckType.evaluate returns the expected_results."""
    check = CheckType.init(*check_type_args)
    pre_data = load_json_file("pre", filename)
    post_data = load_json_file("post", filename)
    actual_results = check.evaluate(pre_data, post_data, path)
    assert actual_results == expected_results


napalm_bgp_neighbor_status = (
    "napalm_get_bgp_neighbors.json",
    ("exact_match",),
    {
        "path": "global.$peers$.*.[is_enabled,is_up]",
        # "reference_key_path": "global.peers"
    },
    0,
)

napalm_bgp_neighbor_prefixes_ipv4 = (
    "napalm_get_bgp_neighbors.json",
    ("tolerance", 10),
    {
        "path": "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes,sent_prefixes]",
        # "reference_key_path": "global.peers",
    },
    1,
)

napalm_bgp_neighbor_prefixes_ipv6 = (
    "napalm_get_bgp_neighbors.json",
    ("tolerance", 10),
    {
        "path": "global.$peers$.*.*.ipv6.[accepted_prefixes,received_prefixes,sent_prefixes]",
        # "reference_key_path": "global.peers",
    },
    2,
)

napalm_get_lldp_neighbors_exact_raw = ("napalm_get_lldp_neighbors.json", ("exact_match",), {}, 0)

check_tests = [
    napalm_bgp_neighbor_status,
    napalm_bgp_neighbor_prefixes_ipv4,
    napalm_bgp_neighbor_prefixes_ipv6,
    napalm_get_lldp_neighbors_exact_raw,
]


@pytest.mark.parametrize("filename, check_args, path, result_index", check_tests)
def test_checks(filename, check_args, path, result_index):
    """Validate multiple checks on the same data to catch corner cases."""
    pre_data = load_json_file("pre", filename)
    post_data = load_json_file("post", filename)
    result = load_json_file("results", filename)

    check = CheckType.init(*check_args)
    check_output = check.evaluate(pre_data, post_data, path)
    assert list(check_output) == result[result_index]
