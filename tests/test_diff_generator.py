import pytest
from .utility import load_json_file
from netcompare.evaluator import diff_generator
from netcompare.runner import extract_values_from_output


assertion_failed_message = """Test output is different from expected output.
output: {output}
expected output: {expected_output}
"""

exact_match_of_global_peers_via_napalm_getter = ("napalm_getter.json", "global.$peers$.*.[is_enabled,is_up]", [])

exact_match_of_bgpPeerCaps_via_api = (
    "api.json",
    "result[0].vrfs.default.peerList[*].[$peerAddress$,state,bgpPeerCaps]",
    [],
)

exact_match_of_bgp_neigh_via_textfsm = ("textfsm.json", "result[*].[$bgp_neigh$,state]", [])

raw_diff_of_interface_ma1_via_api_value_exclude = (
    "raw_value_exclude.json",
    "result[*]",
    ["interfaceStatistics", "interfaceCounters"],
)

raw_diff_of_interface_ma1_via_api_novalue_exclude = (
    "raw_novalue_exclude.json",
    None,
    ["interfaceStatistics", "interfaceCounters"],
)

raw_diff_of_interface_ma1_via_api_novalue_noexclude = ("raw_novalue_noexclude.json", None, [])

exact_match_missing_item = ("napalm_getter_missing_peer.json", None, [])

exact_match_additional_item = ("napalm_getter_additional_peer.json", None, [])

exact_match_changed_item = ("napalm_getter_changed_peer.json", None, [])

exact_match_multi_nested_list = (
    "exact_match_nested.json",
    "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes]",
    [],
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


@pytest.mark.parametrize("filename, path, exclude", eval_tests)
def test_eval(filename, path, exclude):

    pre_data = load_json_file("pre", filename)
    post_data = load_json_file("post", filename)
    expected_output = load_json_file("results", filename)
    pre_value = extract_values_from_output(pre_data, path, exclude)
    post_value = extract_values_from_output(post_data, path, exclude)
    output = diff_generator(pre_value, post_value)

    assert expected_output == output, assertion_failed_message.format(output=output, expected_output=expected_output)
