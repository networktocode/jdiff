"""Unit tests for operator check-type."""
import pytest
from jdiff import CheckType, extract_data_from_json
from .utility import load_json_file, ASSERT_FAIL_MESSAGE

operator_all_same = (
    "pre.json",
    "operator",
    {"params": {"mode": "all-same", "operator_data": True}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup,vrf,state]",
    (
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
        False,
    ),
)
operator_contains = (
    "pre.json",
    "operator",
    {"params": {"mode": "contains", "operator_data": "EVPN"}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
    (
        [
            {"10.1.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE"}},
            {"10.2.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE"}},
            {"10.64.207.255": {"peerGroup": "IPv4-UNDERLAY-MLAG-PEER"}},
        ],
        False,
    ),
)
operator_not_contains = (
    "pre.json",
    "operator",
    {"params": {"mode": "not-contains", "operator_data": "EVPN"}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
    (
        [
            {"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE"}},
        ],
        False,
    ),
)
operator_is_gt = (
    "pre.json",
    "operator",
    {"params": {"mode": "is-gt", "operator_data": 20}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    ([], True),
)
operator_is_lt = (
    "pre.json",
    "operator",
    {"params": {"mode": "is-lt", "operator_data": 60}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    ([], True),
)
operator_is_in = (
    "pre.json",
    "operator",
    {"params": {"mode": "is-in", "operator_data": [20, 40, 50]}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    ([], True),
)
operator_not_in = (
    "pre.json",
    "operator",
    {"params": {"mode": "not-in", "operator_data": [20, 40, 50]}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        [
            {"7.7.7.7": {"prefixesSent": 50}},
            {"10.1.0.0": {"prefixesSent": 50}},
            {"10.2.0.0": {"prefixesSent": 50}},
            {"10.64.207.255": {"prefixesSent": 50}},
        ],
        False,
    ),
)
operator_in_range = (
    "pre.json",
    "operator",
    {"params": {"mode": "in-range", "operator_data": (20, 60)}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    ([], True),
)
operator_not_in_range = (
    "pre.json",
    "operator",
    {"params": {"mode": "not-in-range", "operator_data": (20, 60)}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesSent]",
    (
        [
            {"7.7.7.7": {"prefixesSent": 50}},
            {"10.1.0.0": {"prefixesSent": 50}},
            {"10.2.0.0": {"prefixesSent": 50}},
            {"10.64.207.255": {"prefixesSent": 50}},
        ],
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
    check = CheckType.create(check_type_str)
    # There is not concept of "pre" and "post" in operator.
    data = load_json_file("api", filename)
    value = extract_data_from_json(data, path)
    print(evaluate_args, value)
    actual_results = check.evaluate(evaluate_args, value)
    assert actual_results == expected_result, ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=expected_result
    )


@pytest.mark.parametrize(
    "value, operator_data, expected_result",
    [
        (
            [
                {"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                {"10.1.0.0": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
            ],
            True,
            ([], True),
        ),
        (
            [
                {"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                {"10.1.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE", "vrf": "default", "state": "Connected"}},
            ],
            True,
            (
                [
                    {"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                    {"10.1.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                ],
                False,
            ),
        ),
        (
            [
                {"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                {"10.1.0.0": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
            ],
            False,
            (
                [
                    {"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                    {"10.1.0.0": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                ],
                False,
            ),
        ),
        (
            [
                {"7.7.7.7": {"peerGroup": "EVPN-OVERLAY-SPINE", "vrf": "default", "state": "Connected"}},
                {"10.1.0.0": {"peerGroup": "IPv4-UNDERLAY-SPINE", "vrf": "default", "state": "Connected"}},
            ],
            False,
            ([], True),
        ),
    ],
)
def test_all_same(value, operator_data, expected_result):
    check_args = {"params": {"mode": "all-same", "operator_data": operator_data}}
    check = CheckType.create("operator")
    assert check.evaluate(check_args, value) == expected_result
