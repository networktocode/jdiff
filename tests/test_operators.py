import pytest
from netcompare.check_types import CheckType
from .utility import load_json_file, ASSERT_FAIL_MESSAGE

operator_all_same = (
    "pre.json",
    "operator",
    {"params": {"mode": "all-same", "operator_data": True}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup,vrf,state]",
    (
        (
            False,
            [
                {
                    "7.7.7.7": {
                        "peerGroup": "EVPN-OVERLAY-SPINE",
                        "state": "Idle",
                        "vrf": "default",
                    }
                },
                {
                    "10.1.0.0": {
                        "peerGroup": "IPv4-UNDERLAY-SPINE",
                        "state": "Idle",
                        "vrf": "default",
                    }
                },
                {
                    "10.2.0.0": {
                        "peerGroup": "IPv4-UNDERLAY-SPINE",
                        "state": "Idle",
                        "vrf": "default",
                    }
                },
                {
                    "10.64.207.255": {
                        "peerGroup": "IPv4-UNDERLAY-MLAG-PEER",
                        "state": "Idle",
                        "vrf": "default",
                    }
                },
            ],
        ),
        False,
    ),
)
operator_contains = (
    "pre.json",
    "operator",
    {"params": {"mode": "contains", "operator_data": "EVPN"}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
    ((True, [{"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE"}}]), False),
)
operator_not_contains = (
    "pre.json",
    "operator",
    {"params": {"not-contains": "EVPN"}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
    (
        (
            True,
            [
                {"10.1.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE"}},
                {"10.2.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE"}},
                {"10.64.207.255": {"peerGroup": "IPv4-UNDERLAY-MLAG-PEER"}},
            ],
        ),
        False,
    ),
)
operator_is_gt = (
    "pre.json",
    "operator",
    {"params": {"mode": "is-gt", "operator_data": 20}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        (
            True,
            [
                {"7.7.7.7": {"prefixesSent": 50}},
                {"10.1.0.0": {"prefixesSent": 50}},
                {"10.2.0.0": {"prefixesSent": 50}},
                {"10.64.207.255": {"prefixesSent": 50}},
            ],
        ),
        False,
    ),
)
operator_is_lt = (
    "pre.json",
    "operator",
    {"params": {"mode": "is-lt", "operator_data": 60}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        (
            True,
            [
                {"7.7.7.7": {"prefixesSent": 50}},
                {"10.1.0.0": {"prefixesSent": 50}},
                {"10.2.0.0": {"prefixesSent": 50}},
                {"10.64.207.255": {"prefixesSent": 50}},
            ],
        ),
        False,
    ),
)
operator_is_in = (
    "pre.json",
    "operator",
    {"params": {"mode": "is-in", "operator_data": [20, 40, 50]}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        (
            True,
            [
                {"7.7.7.7": {"prefixesSent": 50}},
                {"10.1.0.0": {"prefixesSent": 50}},
                {"10.2.0.0": {"prefixesSent": 50}},
                {"10.64.207.255": {"prefixesSent": 50}},
            ],
        ),
        False,
    ),
)
operator_not_in = (
    "pre.json",
    "operator",
    {"params": {"mode": "not-in", "operator_data": [20, 40, 60]}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        (
            True,
            [
                {"7.7.7.7": {"prefixesSent": 50}},
                {"10.1.0.0": {"prefixesSent": 50}},
                {"10.2.0.0": {"prefixesSent": 50}},
                {"10.64.207.255": {"prefixesSent": 50}},
            ],
        ),
        False,
    ),
)
operator_in_range = (
    "pre.json",
    "operator",
    {"params": {"mode": "in-range", "operator_data":(20, 60)}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        (
            True,
            [
                {"7.7.7.7": {"prefixesSent": 50}},
                {"10.1.0.0": {"prefixesSent": 50}},
                {"10.2.0.0": {"prefixesSent": 50}},
                {"10.64.207.255": {"prefixesSent": 50}},
            ],
        ),
        False,
    ),
)
operator_not_in_range = (
    "pre.json",
    "operator",
    {"params": {"mode": "not-range", "operator_data": (20, 40)}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        (
            True,
            [
                {"7.7.7.7": {"prefixesSent": 50}},
                {"10.1.0.0": {"prefixesSent": 50}},
                {"10.2.0.0": {"prefixesSent": 50}},
                {"10.64.207.255": {"prefixesSent": 50}},
            ],
        ),
        False,
    ),
)

operator_all_tests = [
    operator_all_same,
    operator_contains,
    operator_not_contains,
    operator_is_gt,
    operator_is_lt,
    operator_is_in,
    operator_not_in,
    operator_in_range,
    operator_not_in_range,
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
        output=actual_results, expected_output=expected_result
    )
