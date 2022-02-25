import pytest
from netcompare.check_types import CheckType, ExactMatchType, OperatorType, ToleranceType, ParameterMatchType, RegexType
from .utility import load_json_file, ASSERT_FAIL_MESSAGE
import pdb

operator_all_same = (
    "pre.json",
    "operator",
    {"params": {"all-same": True}},
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
    {"params": {"contains": "EVPN"}},
    "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]",
    (
        (
            False,
            [
                {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE'}},
                {'10.2.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE'}},
                {'10.64.207.255': {'peerGroup': 'IPv4-UNDERLAY-MLAG-PEER'}}
            ]
        ),
        False
    )
)


operator_all_tests = [
    operator_all_same,
    operator_contains,
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



