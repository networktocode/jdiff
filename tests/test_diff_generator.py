"""Diff generator tests."""
import pytest
from netcompare.evaluators import diff_generator
from netcompare.check_types import CheckType
from .utility import load_mocks, ASSERT_FAIL_MESSAGE


# Diff test case 1.
global_peers = (
    "napalm_getter_peer_state_change",
    "global.$peers$.*.[is_enabled,is_up]",
    [],
    {
        "10.1.0.0": {
            "is_enabled": {"new_value": False, "old_value": True},
            "is_up": {"new_value": False, "old_value": True},
        },
        "7.7.7.7": {
            "is_enabled": {"new_value": True, "old_value": False},
            "is_up": {"new_value": True, "old_value": False},
        },
    },
)

# Diff test case 2.
bgp_peer_caps = (
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,state,bgpPeerCaps]",
    [],
    {"7.7.7.7": {"state": {"new_value": "Connected", "old_value": "Idle"}}},
)

# Diff test case 3.
bgp_neigh = (
    "textfsm",
    "result[*].[$bgp_neigh$,state]",
    [],
    {"10.17.254.2": {"state": {"new_value": "Up", "old_value": "Idle"}}},
)

# Diff test case 4. Exclude filter applied.
raw_diff_of_interface_ma1_value_exclude = (
    "raw_value_exclude",
    "result[*]",
    ["interfaceStatistics", "interfaceCounters"],
    {
        "interfaces": {
            "Management1": {
                "lastStatusChangeTimestamp": {"new_value": 1626247821.123456, "old_value": 1626247820.0720868},
                "interfaceAddress": {"primaryIp": {"address": {"new_value": "10.2.2.15", "old_value": "10.0.2.15"}}},
            }
        }
    },
)

# Diff test case 5. Raw diff (no jmspath expression defined) and exclude filter applied.
raw_diff_of_interface_ma1_novalue_exclude = (
    "raw_novalue_exclude",
    None,
    ["interfaceStatistics", "interfaceCounters"],
    {
        "result": {
            "interfaces": {
                "Management1": {
                    "interfaceStatus": {"new_value": "connected", "old_value": "down"},
                    "lastStatusChangeTimestamp": {"new_value": 1626247821.123456, "old_value": 1626247820.0720868},
                    "interfaceAddress": {
                        "primaryIp": {"address": {"new_value": "10.2.2.15", "old_value": "10.0.2.15"}}
                    },
                }
            }
        }
    },
)

# Diff test case 5. Raw diff (no jmspath expression defined) and no exclude filter applied.
raw_diff_of_interface_ma1_novalue_noexclude = (
    "raw_novalue_noexclude",
    None,
    [],
    {
        "result": {
            "interfaces": {
                "Management1": {
                    "lastStatusChangeTimestamp": {"new_value": 1626247821.123456, "old_value": 1626247820.0720868},
                    "interfaceStatistics": {
                        "inBitsRate": {"new_value": 3403.4362520883615, "old_value": 3582.5323982177174},
                        "inPktsRate": {"new_value": 3.7424095978179257, "old_value": 3.972702352461616},
                        "outBitsRate": {"new_value": 16249.69114419833, "old_value": 17327.65267220522},
                        "outPktsRate": {"new_value": 2.1111866059750692, "old_value": 2.216220664406746},
                    },
                    "interfaceCounters": {
                        "outUcastPkts": {"new_value": 853, "old_value": 840},
                        "counterRefreshTime": {"new_value": 1626247927.270532, "old_value": 1626247906.586039},
                        "inOctets": {"new_value": 173999, "old_value": 171537},
                        "outOctets": {"new_value": 801419, "old_value": 797728},
                        "inUcastPkts": {"new_value": 1508, "old_value": 1496},
                        "inTotalPkts": {"new_value": 1539, "old_value": 1527},
                        "outMulticastPkts": {"new_value": 7, "old_value": 6},
                    },
                    "interfaceAddress": {
                        "primaryIp": {"address": {"new_value": "10.2.2.15", "old_value": "10.0.2.15"}}
                    },
                }
            }
        }
    },
)

# Diff test case 6. Missing item in post.
missing_item = (
    "napalm_getter_missing_peer",
    None,
    [],
    {"global": {"peers": {"7.7.7.7": "missing"}}},
)

# Diff test case 7. Extra item in post.
additional_item = (
    "napalm_getter_additional_peer",
    None,
    [],
    {"global": {"peers": {"8.8.8.8": "new"}}},
)

# Diff test case 8. Item changed in post.
changed_item = (
    "napalm_getter_changed_peer",
    None,
    [],
    {"global": {"peers": {"7.7.7.7": "missing", "8.8.8.8": "new"}}},
)

# Diff test case 9. Value in multiple nested lists.
multi_nested_list = (
    "exact_match_nested",
    "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes]",
    [],
    {
        "10.1.0.0": {"accepted_prefixes": {"new_value": -1, "old_value": -9}},
        "10.2.0.0": {"accepted_prefixes": {"new_value": -1, "old_value": -9}},
    },
)

# Diff test case 10. JMSPath empty string.
ospf_int_br_raw = (
    "textfsm_ospf_int_br",
    "",
    [],
    {"state": {"new_value": "DOWN", "old_value": "P2P", "new_value_dup!": "DR", "old_value_dup!": "BDR"}},
)

# Diff test case 11. Extensive nu,ber of values.
ospf_int_br_normalized = (
    "textfsm_ospf_int_br",
    "[*].[$interface$,area,ip_address_mask,cost,state,neighbors_fc]",
    [],
    {
        "Se0/0/0.100": {"state": {"new_value": "DOWN", "old_value": "P2P"}},
        "Fa0/0": {"state": {"new_value": "DR", "old_value": "BDR"}},
    },
)

# Test GitLab Issues
# Test issue #44: https://github.com/networktocode-llc/netcompare/issues/44
test_issue_44_case_1 = (
    "raw_novalue_exclude",
    "result[*].interfaces.*.[$name$,interfaceStatus]",
    [],
    {"Management1": {"interfaceStatus": {"new_value": "connected", "old_value": "down"}}},
)

test_issue_44_case_2 = (
    "raw_novalue_exclude",
    "result[0].interfaces.*.[$name$,interfaceStatus]",
    [],
    {"Management1": {"interfaceStatus": {"new_value": "connected", "old_value": "down"}}},
)


eval_tests = [
    global_peers,
    bgp_peer_caps,
    bgp_neigh,
    raw_diff_of_interface_ma1_value_exclude,
    raw_diff_of_interface_ma1_novalue_exclude,
    raw_diff_of_interface_ma1_novalue_noexclude,
    missing_item,
    additional_item,
    changed_item,
    multi_nested_list,
    ospf_int_br_raw,
    ospf_int_br_normalized,
    test_issue_44_case_1,
    test_issue_44_case_2,
]


@pytest.mark.parametrize("folder_name, path, exclude, expected_output", eval_tests)
def test_eval(folder_name, path, exclude, expected_output):
    """Run tests."""
    pre_data, post_data = load_mocks(folder_name)
    pre_value = CheckType.get_value(pre_data, path, exclude)
    post_value = CheckType.get_value(post_data, path, exclude)
    output = diff_generator(pre_value, post_value)

    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)
