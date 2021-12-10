"Check Type unit tests."
import pytest
from netcompare.check_type import CheckType, ExactMatchType, ToleranceType
from .utility import load_mocks, ASSERT_FAIL_MESSAGE


@pytest.mark.parametrize(
    "args, expected_class",
    [(["exact_match"], ExactMatchType), (["tolerance", 10], ToleranceType)],
)
def test_check_init(args, expected_class):
    """Validate that the returned class is the expected one."""
    assert isinstance(CheckType.init(*args), expected_class)


def test_check_type_raises_not_implemented_error_for_invalid_check_type():
    """Validate that CheckType raises a NotImplementedError when passed a non-existant check_type."""
    with pytest.raises(NotImplementedError):
        CheckType.init("does_not_exist")


exact_match_test_values_no_change = (
    ("exact_match",),
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]",
    ({}, True),
)

exact_match_test_values_changed = (
    ("exact_match",),
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
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
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]",
    ({}, True),
)

tolerance_test_values_within_threshold = (
    ("tolerance", 10),
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    ({}, True),
)

tolerance_test_values_beyond_threshold = (
    ("tolerance", 10),
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]",
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


@pytest.mark.parametrize("check_type_args, folder_name, path, expected_results", check_type_tests)
def test_check_type_results(check_type_args, folder_name, path, expected_results):
    """Validate that CheckType.evaluate returns the expected_results."""
    check = CheckType.init(*check_type_args)
    pre_data, post_data, _ = load_mocks(folder_name)
    pre_value = check.get_value(pre_data, path)
    post_value = check.get_value(post_data, path)
    actual_results = check.evaluate(pre_value, post_value)
    assert actual_results == expected_results, ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=expected_results
    )


napalm_bgp_neighbor_status = (
    "napalm_get_bgp_neighbors",
    ("exact_match",),
    "global.$peers$.*.[is_enabled,is_up]",
    0,
)

napalm_bgp_neighbor_prefixes_ipv4 = (
    "napalm_get_bgp_neighbors",
    ("tolerance", 10),
    "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes,sent_prefixes]",
    1,
)

napalm_bgp_neighbor_prefixes_ipv6 = (
    "napalm_get_bgp_neighbors",
    ("tolerance", 10),
    "global.$peers$.*.*.ipv6.[accepted_prefixes,received_prefixes,sent_prefixes]",
    2,
)

napalm_get_lldp_neighbors_exact_raw = (
    "napalm_get_lldp_neighbors",
    ("exact_match",),
    None,
    0,
)

check_tests = [
    napalm_bgp_neighbor_status,
    napalm_bgp_neighbor_prefixes_ipv4,
    napalm_bgp_neighbor_prefixes_ipv6,
    napalm_get_lldp_neighbors_exact_raw,
]


@pytest.mark.parametrize("folder_name, check_args, path, result_index", check_tests)
def test_checks(folder_name, check_args, path, result_index):
    """Validate multiple checks on the same data to catch corner cases."""
    pre_data, post_data, results = load_mocks(folder_name)

    check = CheckType.init(*check_args)
    pre_data, post_data, results = load_mocks(folder_name)

    pre_value = check.get_value(pre_data, path)
    post_value = check.get_value(post_data, path)
    actual_results = check.evaluate(pre_value, post_value)

    assert list(actual_results) == results[result_index], ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=results[result_index]
    )


parameter_match_api = (
    "parameter_match.json",
    ("parameter_match", {"localAsn": "65130.1100", "linkType": "external"}),
    "result[0].vrfs.default.peerList[*].[$peerAddress$,localAsn,linkType]",
    (
        {
            "7.7.7.7": {"localAsn": "65130.1010", "linkType": "the road to seniority"},
            "10.1.0.0": {"localAsn": "65130.8888"},
        },
        False,
    ),
)


@pytest.mark.parametrize("filename, check_args, path, expected_result", [parameter_match_api])
def test_param_match(filename, check_args, path, expected_result):
    """Validate parameter_match check type."""
    check = CheckType.init(*check_args)
    # There is not concept of "pre" and "post" in parameter_match.
    data = load_json_file("pre", filename)
    value = check.get_value(data, path)
    actual_results = check.evaluate(value, check_args)
    assert actual_results == expected_result
