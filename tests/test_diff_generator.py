"""Diff generator tests."""
import pytest
from netcompare.evaluator import diff_generator
from netcompare.runner import extract_values_from_output
from .utility import load_mocks


exact_match_of_global_peers_via_napalm_getter = ("napalm_getter", "global.$peers$.*.[is_enabled,is_up]", [])

exact_match_of_bgpPeerCaps_via_api = ("api", "result[0].vrfs.default.peerList[*].[$peerAddress$,state,bgpPeerCaps]", [])

exact_match_of_bgp_neigh_via_textfsm = ("textfsm", "result[*].[$bgp_neigh$,state]", [])

raw_diff_of_interface_ma1_via_api_value_exclude = (
    "raw_value_exclude",
    "result[*]",
    ["interfaceStatistics", "interfaceCounters"],
)

raw_diff_of_interface_ma1_via_api_novalue_exclude = (
    "raw_novalue_exclude",
    None,
    ["interfaceStatistics", "interfaceCounters"],
)

raw_diff_of_interface_ma1_via_api_novalue_noexclude = ("raw_novalue_noexclude", None, [])

exact_match_missing_item = ("napalm_getter_missing_peer", None, [])

exact_match_additional_item = ("napalm_getter_additional_peer", None, [])

exact_match_changed_item = ("napalm_getter_changed_peer", None, [])

exact_match_multi_nested_list = (
    "exact_match_nested",
    "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes]",
    [],
)

eval_tests = [
    exact_match_of_global_peers_via_napalm_getter,
    exact_match_of_bgpPeerCaps_via_api,
    exact_match_of_bgp_neigh_via_textfsm,
    raw_diff_of_interface_ma1_via_api_value_exclude,
    raw_diff_of_interface_ma1_via_api_novalue_exclude,
    raw_diff_of_interface_ma1_via_api_novalue_noexclude,
    exact_match_missing_item,
    exact_match_additional_item,
    exact_match_changed_item,
    exact_match_multi_nested_list,
]

ASSERT_FAILED_MESSAGE = """Test output is different from expected output.
output: {output}
expected output: {expected_output}
"""


@pytest.mark.parametrize("folder_name, path, exclude", eval_tests)
def test_eval(folder_name, path, exclude):
    """Run tests."""
    pre_data, post_data, expected_output = load_mocks(folder_name)
    pre_value = extract_values_from_output(pre_data, path, exclude)
    post_value = extract_values_from_output(post_data, path, exclude)
    output = diff_generator(pre_value, post_value)

    assert expected_output == output, ASSERT_FAILED_MESSAGE.format(output=output, expected_output=expected_output)
