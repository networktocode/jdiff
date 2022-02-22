"""Check Type unit tests."""
import pytest
from netcompare.check_types import CheckType, ExactMatchType, OperatorType, ToleranceType, ParameterMatchType, RegexType
from .utility import load_json_file, load_mocks, ASSERT_FAIL_MESSAGE
import pdb

def test_child_class_raises_exception():
    """Tests that exception is raised for child class when abstract methods are not implemented."""

    class CheckTypeChild(CheckType):
        """Test Class."""

    with pytest.raises(TypeError) as error:
        CheckTypeChild()  # pylint: disable=E0110

    assert (
        "Can't instantiate abstract class CheckTypeChild"
        " with abstract methods evaluate, validate" in error.value.__str__()
    )


def test_child_class_proper_implementation():
    """Test properly implemented child class can be instantiated."""

    class CheckTypeChild(CheckType):
        """Test Class."""

        @staticmethod
        def validate(**kwargs):
            return None

        def evaluate(self, *args, **kwargs):
            return {}, True

    check = CheckTypeChild()
    assert isinstance(check, CheckTypeChild) and check.validate() is None and check.evaluate() == ({}, True)


@pytest.mark.parametrize(
    "check_type_str, expected_class",
    [
        ("exact_match", ExactMatchType),
        ("tolerance", ToleranceType),
        ("parameter_match", ParameterMatchType),
        ("regex", RegexType),
        ("operator", OperatorType)
    ],
)
def test_check_init(check_type_str, expected_class):
    """Validate that the returned class is the expected one."""
    assert isinstance(CheckType.init(check_type_str), expected_class)


exception_tests_init = [
    ("does_not_exist", NotImplementedError, ""),
]
@pytest.mark.parametrize("check_type_str, exception_type, expected_in_output", exception_tests_init)
def tests_exceptions_init(check_type_str, exception_type, expected_in_output):
    """Tests exceptions when check object is initialized."""
    with pytest.raises(exception_type) as error:
        CheckType.init(check_type_str)
    assert expected_in_output in error.value.__str__()


exception_tests_eval = [
    (
        "parameter_match",
        {"value_to_compare": {}, "mode": "some mode", "params": {"some": "thing"}},
        ValueError,
        "Mode argument should be",
    ),
    (
        "regex",
        {"value_to_compare": {}, "mode": "some mode", "regex": "some regex"},
        ValueError,
        "Mode argument should be",
    ),
]
@pytest.mark.parametrize("check_type_str, evaluate_args, exception_type, expected_in_output", exception_tests_eval)
def tests_exceptions_eval(check_type_str, evaluate_args, exception_type, expected_in_output):
    """Tests exceptions when calling .evaluate() method."""
    with pytest.raises(exception_type) as error:
        check = CheckType.init(check_type_str)
        check.evaluate(**evaluate_args)
    assert expected_in_output in error.value.__str__()


exact_match_test_values_no_change = (
    "exact_match",
    {},
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]",
    ({}, True),
)
exact_match_test_values_changed = (
    "exact_match",
    {},
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
    "tolerance",
    {"tolerance": 10},
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]",
    ({}, True),
)
tolerance_test_values_within_threshold = (
    "tolerance",
    {"tolerance": 10},
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    ({}, True),
)
tolerance_test_values_beyond_threshold = (
    "tolerance",
    {"tolerance": 10},
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
@pytest.mark.parametrize("check_type_str, evaluate_args, folder_name, path, expected_results", check_type_tests)
def test_check_type_results(check_type_str, evaluate_args, folder_name, path, expected_results):
    """Validate that CheckType.evaluate returns the expected_results."""
    check = CheckType.init(check_type_str)
    pre_data, post_data = load_mocks(folder_name)
    pre_value = check.get_value(pre_data, path)
    post_value = check.get_value(post_data, path)
    actual_results = check.evaluate(post_value, pre_value, **evaluate_args)
    assert actual_results == expected_results, ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=expected_results
    )


napalm_bgp_neighbor_status = (
    "napalm_get_bgp_neighbors",
    "exact_match",
    {},
    "global.$peers$.*.[is_enabled,is_up]",
    (
        {
            "7.7.7.7": {
                "is_enabled": {"new_value": False, "old_value": True},
                "is_up": {"new_value": False, "old_value": True},
            }
        },
        False,
    ),
)
napalm_bgp_neighbor_prefixes_ipv4 = (
    "napalm_get_bgp_neighbors",
    "tolerance",
    {"tolerance": 10},
    "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes,sent_prefixes]",
    ({"10.1.0.0": {"accepted_prefixes": {"new_value": 900, "old_value": 1000}}}, False),
)
napalm_bgp_neighbor_prefixes_ipv6 = (
    "napalm_get_bgp_neighbors",
    "tolerance",
    {"tolerance": 10},
    "global.$peers$.*.*.ipv6.[accepted_prefixes,received_prefixes,sent_prefixes]",
    ({"10.64.207.255": {"received_prefixes": {"new_value": 1100, "old_value": 1000}}}, False),
)
napalm_get_lldp_neighbors_exact_raw = (
    "napalm_get_lldp_neighbors",
    "exact_match",
    {},
    None,
    (
        {
            "Ethernet1": {
                "port": {"new_value": "518", "old_value": "519"},
                "missing": [{"hostname": "ios-xrv-unittest", "port": "Gi0/0/0/0"}],
            },
            "Ethernet3": {
                "new": [
                    {"hostname": "ios-xrv-unittest", "port": "Gi0/0/0/0"},
                    {"hostname": "ios-xrv-unittest", "port": "Gi0/0/0/1"},
                ]
            },
        },
        False,
    ),
)
tolerance_no_path = (
    "tolerance",
    "tolerance",
    {"tolerance": 10},
    "",
    (
        {
            "interfaces": {
                "Ethernet1": {"power_level": {"new_value": 4, "old_value": -4}},
                "Ethernet3": {"power_level": {"new_value": 3, "old_value": -3}},
            }
        },
        False,
    ),
)

tolerance_path = (
    "tolerance",
    "tolerance",
    {"tolerance": 10},
    "interfaces",
    (
        {
            "Ethernet1": {"power_level": {"new_value": 4, "old_value": -4}},
            "Ethernet3": {"power_level": {"new_value": 3, "old_value": -3}},
        },
        False,
    ),
)

tolerance_deep_path = (
    "tolerance",
    "tolerance",
    {"tolerance": 10},
    "interfaces.Ethernet1",
    (
        {"power_level": {"new_value": 4, "old_value": -4}},
        False,
    ),
)

check_tests = [
    napalm_bgp_neighbor_status,
    napalm_bgp_neighbor_prefixes_ipv4,
    napalm_bgp_neighbor_prefixes_ipv6,
    napalm_get_lldp_neighbors_exact_raw,
    tolerance_no_path,
    tolerance_path,
    tolerance_deep_path,
]


@pytest.mark.parametrize("folder_name, check_type_str, evaluate_args, path, expected_result", check_tests)
def test_checks(folder_name, check_type_str, evaluate_args, path, expected_result):
    """Validate multiple checks on the same data to catch corner cases."""
    check = CheckType.init(check_type_str)
    pre_data, post_data = load_mocks(folder_name)
    pre_value = check.get_value(pre_data, path)
    post_value = check.get_value(post_data, path)
    actual_results = check.evaluate(post_value, pre_value, **evaluate_args)

    assert actual_results == expected_result, ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=expected_result
    )


parameter_match_api = (
    "pre.json",
    "parameter_match",
    {"mode": "match", "params": {"localAsn": "65130.1100", "linkType": "external"}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,localAsn,linkType]",
    (
        {
            "7.7.7.7": {"localAsn": "65130.1010", "linkType": "the road to seniority"},
            "10.1.0.0": {"localAsn": "65130.8888"},
        },
        False,
    ),
)


@pytest.mark.parametrize("filename, check_type_str, evaluate_args, path, expected_result", [parameter_match_api])
def test_param_match(filename, check_type_str, evaluate_args, path, expected_result):
    """Validate parameter_match check type."""
    check = CheckType.init(check_type_str)
    # There is not concept of "pre" and "post" in parameter_match.
    data = load_json_file("parameter_match", filename)
    value = check.get_value(data, path)
    actual_results = check.evaluate(value, **evaluate_args)
    assert actual_results == expected_result, ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=expected_result
    )


regex_match_include = (
    "pre.json",
    "regex",
    {"regex": ".*UNDERLAY.*", "mode": "match"},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
    (
        {
            "7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE"},
        },
        False,
    ),
)

regex_match_exclude = (
    "pre.json",
    "regex",
    {"regex": ".*UNDERLAY.*", "mode": "no-match"},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
    (
        {
            "10.1.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE"},
            "10.2.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE"},
            "10.64.207.255": {"peerGroup": "IPv4-UNDERLAY-MLAG-PEER"},
        },
        False,
    ),
)

regex_match = [
    regex_match_include,
    regex_match_exclude,
]


@pytest.mark.parametrize("filename, check_type_str, evaluate_args, path, expected_result", regex_match)
def test_regex_match(filename, check_type_str, evaluate_args, path, expected_result):
    """Validate regex check type."""
    check = CheckType.init(check_type_str)
    # There is not concept of "pre" and "post" in parameter_match.
    data = load_json_file("api", filename)
    value = check.get_value(data, path)
    actual_results = check.evaluate(value, **evaluate_args)
    assert actual_results == expected_result, ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=expected_result
    )

operator_all_same = (
    "pre.json",
    "operator",
    {"params": {"all-same": True}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup,vrf,state]",
    (
        {},     #TBD
        False,  #TBD
    ),
)
operator_all_tests = [
#     # type() == str(), int(), float()
    operator_all_same,
#     operator_is_equal,
#     operator_not_equal,
#     operator_contains,
#     operator_not_contains,
#     # type() == int(), float()
#     operator_is_gt,
#     operator_is_lt,
#     operator_in_operator,
#     operator_not_operator,
#     # type() == dict()
#     operator_is_in,
#     operator_not_in,
]

@pytest.mark.parametrize("filename, check_type_str, evaluate_args, path, expected_result", operator_all_tests)
def test_operator(filename, check_type_str, evaluate_args, path, expected_result):
    """Validate all operator check types."""
    check = CheckType.init(check_type_str)
    # There is not concept of "pre" and "post" in operator.
    data = load_json_file("api", filename)
    value = check.get_value(data, path)
    actual_results = check.evaluate(value, **evaluate_args)
    assert actual_results == expected_result, ASSERT_FAIL_MESSAGE.format(
        output=actual_results,
        expected_output=expected_result
    )

# # operator_is_equal = (
# #     "api",
# #     "operator",
# #     ("operator", {"is-equal": 100}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_not_equal = (
# #     "api",
# #     ("operator", {"not-equal": "internal"}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,linkType]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_contains = (
# #     "api",
# #     ("operator", {"contains": "EVPN"}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_not_contains = (
# #     "api",
# #     ("operator", {"not-contains": "OVERLAY"}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_is_gt = (
# #     "api",
# #     ("operator", {"is-gt": 70000000}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,bgpPeerCaps]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_is_lt = (
# #     "api",
# #     ("operator", {"is-lt": 80000000}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,bgpPeerCaps]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_in_operator = (
# #     "api",
# #     ("operator", {"in-operator": (70000000, 80000000)}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,bgpPeerCaps]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_not_operator = (
# #     "api",
# #     ("operator", {"not-range": (70000000, 80000000)}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,bgpPeerCaps]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_is_in = (
# #     "api",
# #     ("operator", {"is-in": ("Idle", "Down")}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,state]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )

# # operator_not_in = (
# #     "api",
# #     ("operator", {"not-in": ("Idle", "Down")}),
# #     "result[0].vrfs.default.peerList[*].[$peerAddress$,state]",
# #     (
# #         {},     #TBD
# #         False,  #TBD
# #     ),
# # )



