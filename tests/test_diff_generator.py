"""Diff generator tests."""
import pytest
from netcompare.evaluator import diff_generator
from netcompare.runner import extract_values_from_output
from .utility import load_mocks, ASSERT_FAIL_MESSAGE


exact_match_of_global_peers_via_napalm_getter = (
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

exact_match_of_bgp_peer_caps_via_api = (
    "api",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,state,bgpPeerCaps]",
    [],
    {"7.7.7.7": {"state": {"new_value": "Connected", "old_value": "Idle"}}},
)

exact_match_of_bgp_neigh_via_textfsm = (
    "textfsm",
    "",
    # "result[*].[$bgp_neigh$,state]",
    [],
    {"10.17.254.2": {"state": {"new_value": "Up", "old_value": "Idle"}}},
)

raw_diff_of_interface_ma1_via_api_value_exclude = (
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

raw_diff_of_interface_ma1_via_api_novalue_exclude = (
    "raw_novalue_exclude",
    None,
    ["interfaceStatistics", "interfaceCounters"],
    {
        "result": {
            "interfaces": {
                "Management1": {
                    "lastStatusChangeTimestamp": {"new_value": 1626247821.123456, "old_value": 1626247820.0720868},
                    "interfaceAddress": {
                        "primaryIp": {"address": {"new_value": "10.2.2.15", "old_value": "10.0.2.15"}}
                    },
                }
            }
        }
    },
)

raw_diff_of_interface_ma1_via_api_novalue_noexclude = (
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

exact_match_missing_item = (
    "napalm_getter_missing_peer",
    None,
    [],
    {"global": {"peers": {"7.7.7.7": "missing"}}},
)

exact_match_additional_item = (
    "napalm_getter_additional_peer",
    None,
    [],
    {"global": {"peers": {"8.8.8.8": "new"}}},
)

exact_match_changed_item = (
    "napalm_getter_changed_peer",
    None,
    [],
    {"global": {"peers": {"7.7.7.7": "missing", "8.8.8.8": "new"}}},
)

exact_match_multi_nested_list = (
    "exact_match_nested",
    "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes]",
    [],
    {
        "10.1.0.0": {"accepted_prefixes": {"new_value": -1, "old_value": -9}},
        "10.2.0.0": {"accepted_prefixes": {"new_value": -1, "old_value": -9}},
    },
)

eval_tests = [
    # exact_match_of_global_peers_via_napalm_getter,
    # exact_match_of_bgp_peer_caps_via_api,
    exact_match_of_bgp_neigh_via_textfsm,
    # raw_diff_of_interface_ma1_via_api_value_exclude,
    # raw_diff_of_interface_ma1_via_api_novalue_exclude,
    # raw_diff_of_interface_ma1_via_api_novalue_noexclude,
    # exact_match_missing_item,
    # exact_match_additional_item,
    # exact_match_changed_item,
    # exact_match_multi_nested_list,
]


@pytest.mark.parametrize("folder_name, path, exclude, expected_output", eval_tests)
def test_eval(folder_name, path, exclude, expected_output):
    """Run tests."""
    pre_data, post_data = load_mocks(folder_name)
    pre_value = extract_values_from_output(pre_data, path, exclude)
    post_value = extract_values_from_output(post_data, path, exclude)
    output = diff_generator(pre_value, post_value)

    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)
