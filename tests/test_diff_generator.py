#!/usr/bin/env python3

import pytest
import sys
from .utility import load_json_file
from netcompare.evaluator import diff_generator

sys.path.append("..")


assertion_failed_message = """Test output is different from expected output.
output: {output}
expected output: {expected_output}
"""

exact_match_of_global_peers_via_napalm_getter = (
    "napalm_getter.json",
    {
        "check_type": "exact_match",
        "path": "global.$peers$.*.[is_enabled,is_up]",
        # "reference_key_path": "global.peers",
    },
)

exact_match_of_bgpPeerCaps_via_api = (
    "api.json",
    {
        "check_type": "exact_match",
        "path": "result[0].vrfs.default.peerList[*].[$peerAddress$,state,bgpPeerCaps]",
        # "reference_key_path": "result[0].vrfs.default.peerList[*].peerAddress",
    },
)

exact_match_of_bgp_neigh_via_textfsm = (
    "textfsm.json",
    {
        "check_type": "exact_match",
        "path": "result[*].[$bgp_neigh$,state]",
        # "reference_key_path": "result[*].bgp_neigh"
    },
)

raw_diff_of_interface_ma1_via_api_value_exclude = (
    "raw_value_exclude.json",
    {"check_type": "exact_match", "path": "result[*]", "exclude": ["interfaceStatistics", "interfaceCounters"]},
)

raw_diff_of_interface_ma1_via_api_novalue_exclude = (
    "raw_novalue_exclude.json",
    {"check_type": "exact_match", "exclude": ["interfaceStatistics", "interfaceCounters"]},
)

raw_diff_of_interface_ma1_via_api_novalue_noexclude = (
    "raw_novalue_noexclude.json",
    {"check_type": "exact_match"},
)

exact_match_missing_item = (
    "napalm_getter_missing_peer.json",
    {"check_type": "exact_match"},
)

exact_match_additional_item = ("napalm_getter_additional_peer.json", {"check_type": "exact_match"})

exact_match_changed_item = (
    "napalm_getter_changed_peer.json",
    {"check_type": "exact_match"},
)

exact_match_multi_nested_list = (
    "exact_match_nested.json",
    {
        "check_type": "exact_match",
        "path": "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes]",
        # "reference_key_path": "global.peers",
    },
)

eval_tests = [
    exact_match_of_global_peers_via_napalm_getter,
    # exact_match_of_bgpPeerCaps_via_api,
    # exact_match_of_bgp_neigh_via_textfsm,
    # raw_diff_of_interface_ma1_via_api_value_exclude,
    # raw_diff_of_interface_ma1_via_api_novalue_exclude,
    # raw_diff_of_interface_ma1_via_api_novalue_noexclude,
    # exact_match_missing_item,
    # exact_match_additional_item,
    # exact_match_changed_item,
    # exact_match_multi_nested_list,
]


@pytest.mark.parametrize("filename, path", eval_tests)
def test_eval(filename, path):

    pre_data = load_json_file("pre", filename)
    post_data = load_json_file("post", filename)
    expected_output = load_json_file("results", filename)

    output = diff_generator(pre_data, post_data, path)

    assert expected_output == output, assertion_failed_message.format(output=output, expected_output=expected_output)
