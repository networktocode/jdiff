"""Tests for typical software upgrade device state check."""
from copy import deepcopy
import pytest
from jdiff.check_types import CheckType
from .utility import load_json_file


@pytest.mark.parametrize(
    "platform, command, jpath, expected_parameter, check_should_pass",
    [
        ("arista_eos", "show_version", "[*].[$image$,image]", {"image": "4.14.7M"}, True),
        ("arista_eos", "show_version", "[*].[$image$,image]", {"image": "no-match"}, False),
        ("cisco_ios", "show_version", "[*].[$version$,version]", {"version": "12.2(54)SG1"}, True),
        ("cisco_ios", "show_version", "[*].[$version$,version]", {"version": "no-match"}, False),
        ("cisco_nxos", "show_version", "[*].[$os$,os]", {"os": "6.1(2)I3(1)"}, True),
        ("cisco_nxos", "show_version", "[*].[$os$,os]", {"os": "no-match"}, False),
    ],
)
def test_show_version(platform, command, jpath, expected_parameter, check_should_pass):
    """Test expected version with parameter_match."""
    filename = f"{platform}_{command}.json"
    command = load_json_file("sw_upgrade", filename)

    check = CheckType.create("parameter_match")
    value = check.get_value(command, jpath)
    eval_results, passed = check.evaluate(value, expected_parameter, "match")  # pylint: disable=E1121
    assert passed is check_should_pass, f"FAILED, eval_result: {eval_results}"


@pytest.mark.parametrize(
    "platform, command, jpath, check_should_pass",
    [
        ("arista_eos", "show_interface", "[*].[$interface$,link_status,protocol_status]", True),
        ("cisco_ios", "show_interface", "[*].[$interface$,link_status,protocol_status]", True),
        ("arista_eos", "show_interface", "[*].[$interface$,link_status,protocol_status]", False),
        ("cisco_ios", "show_interface", "[*].[$interface$,link_status,protocol_status]", False),
        ("cisco_nxos", "show_interface", "[*].[$interface$,link_status,admin_state]", True),
        ("cisco_nxos", "show_interface", "[*].[$interface$,link_status,admin_state]", False),
    ],
)
def test_show_interfaces_state(platform, command, jpath, check_should_pass):
    """Test the interface status with exact_match."""
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = deepcopy(command_pre)

    if check_should_pass is False:
        if platform == "cisco_nxos":
            command_post[1]["admin_state"] = "down"
        else:
            command_post[0]["link_status"] = "down"
            command_post[1]["protocol_status"] = "down"

    check = CheckType.create("exact_match")
    pre_value = CheckType.get_value(command_pre, jpath)
    post_value = CheckType.get_value(command_post, jpath)
    eval_results, passed = check.evaluate(post_value, pre_value)
    assert passed is check_should_pass, f"FAILED, eval_result: {eval_results}"


@pytest.mark.parametrize(
    "platform, command",
    [
        ("arista_eos", "show_ip_route"),
        ("cisco_ios", "show_ip_route"),
        ("cisco_nxos", "show_ip_route"),
    ],
)
def test_show_ip_route_exact_match(platform, command):
    """Test identical route table pass the test with exact_match."""
    command_pre = command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")

    check = CheckType.create("exact_match")
    eval_results, passed = check.evaluate(command_post, command_pre)
    assert passed is True, f"FAILED, eval_result: {eval_results}"


@pytest.mark.parametrize(
    "platform, command",
    [
        ("arista_eos", "show_ip_route"),
        ("cisco_ios", "show_ip_route"),
        ("cisco_nxos", "show_ip_route"),
    ],
)
def test_show_ip_route_missing_and_additional_routes(platform, command):
    """Test missing or additional routes fail the test with exact_match."""
    command_pre = command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    check = CheckType.create("exact_match")
    print(len(command_pre))
    eval_results_missing, passed_missing = check.evaluate(command_post[:30], command_pre)
    eval_results_additional, passed_additional = check.evaluate(command_post, command_pre[:30])
    assert (
        passed_missing is False and passed_additional is False
    ), f"FAILED, eval_results_missing: {eval_results_missing}; eval_results_additional: {eval_results_additional}"


@pytest.mark.parametrize(
    "platform, command, jpath, check_should_pass",
    [
        ("arista_eos", "show_ip_bgp_summary", "[*].[$bgp_neigh$,state]", True),
        ("arista_eos", "show_ip_bgp_summary", "[*].[$bgp_neigh$,state]", False),
        ("cisco_ios", "show_ip_bgp_neighbors", "[*].[$neighbor$,bgp_state]", True),
        ("cisco_ios", "show_ip_bgp_neighbors", "[*].[$neighbor$,bgp_state]", False),
        ("cisco_nxos", "show_ip_bgp_neighbors", "[*].[$neighbor$,bgp_state]", True),
        ("cisco_nxos", "show_ip_bgp_neighbors", "[*].[$neighbor$,bgp_state]", False),
    ],
)
def test_bgp_neighbor_state(platform, command, jpath, check_should_pass):
    """Test bgp neighbors state with exact_match."""
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = deepcopy(command_pre)

    if check_should_pass is False:
        state_key = "state" if "arista" in platform else "bgp_state"
        command_post[0][state_key] = "Idle"

    check = CheckType.create("exact_match")
    pre_value = CheckType.get_value(command_pre, jpath)
    post_value = CheckType.get_value(command_post, jpath)
    eval_results, passed = check.evaluate(post_value, pre_value)
    assert passed is check_should_pass, f"FAILED, eval_result: {eval_results}"


@pytest.mark.parametrize(
    "platform, command, prfx_post_value, tolerance, check_should_pass",
    [
        ("cisco_ios", "show_ip_bgp_summary", "5457", 10, True),
        ("cisco_ios", "show_ip_bgp_summary", "5456", 10, False),
        ("cisco_ios", "show_ip_bgp_summary", "Idle", 10, False),
        ("cisco_nxos", "show_ip_bgp_summary", "502849", 10, True),
        ("cisco_nxos", "show_ip_bgp_summary", "502848", 10, False),
        ("cisco_nxos", "show_ip_bgp_summary", "Idle", 10, False),
    ],
)
def test_bgp_prefix_tolerance(platform, command, prfx_post_value, tolerance, check_should_pass):
    """Test bgp peer prefix count with tolerance."""
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = deepcopy(command_pre)

    command_post[1]["state_pfxrcd"] = command_post[1]["state_pfxrcd"] = prfx_post_value

    check = CheckType.create("tolerance")
    jpath = "[*].[$bgp_neigh$,state_pfxrcd]"
    pre_value = CheckType.get_value(command_pre, jpath)
    post_value = CheckType.get_value(command_post, jpath)

    eval_results, passed = check.evaluate(post_value, pre_value, tolerance)  # pylint: disable=E1121
    assert passed is check_should_pass, f"FAILED, eval_result: {eval_results}"


@pytest.mark.parametrize(
    "platform, command, jpath, check_should_pass",
    [
        ("arista_eos", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", True),
        ("arista_eos", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", False),
        ("cisco_ios", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", True),
        ("cisco_ios", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", False),
        ("cisco_nxos", "show_ip_ospf_neighbors", "[*].[$neighbor_ipaddr$,state]", True),
        ("cisco_nxos", "show_ip_ospf_neighbors", "[*].[$neighbor_ipaddr$,state]", False),
    ],
)
def test_ospf_neighbor_state(platform, command, jpath, check_should_pass):
    """Test ospf neighbors with exact_match."""
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = deepcopy(command_pre)

    if check_should_pass is False:
        command_post[0]["state"] = "2WAY"
        command_post = command_post[:1]

    check = CheckType.create("exact_match")
    pre_value = CheckType.get_value(command_pre, jpath)
    post_value = CheckType.get_value(command_post, jpath)
    eval_results, passed = check.evaluate(post_value, pre_value)
    assert passed is check_should_pass, f"FAILED, eval_result: {eval_results}"


@pytest.mark.skip(reason="Command output not available")
def test_pim_neighbors():
    pass


@pytest.mark.parametrize(
    "platform, command, check_should_pass",
    [
        ("arista_eos", "show_lldp_neighbors", True),
        ("arista_eos", "show_lldp_neighbors", False),
        ("cisco_ios", "show_lldp_neighbors", True),
        ("cisco_ios", "show_lldp_neighbors", False),
        ("cisco_nxos", "show_lldp_neighbors", True),
        ("cisco_nxos", "show_lldp_neighbors", False),
    ],
)
def test_lldp_neighbor_state(platform, command, check_should_pass):
    """Test LLDP neighbors with exact match."""
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = deepcopy(command_pre)

    if check_should_pass is False:
        command_post = command_post[:2]

    check = CheckType.create("exact_match")
    eval_results, passed = check.evaluate(command_post, command_pre)
    assert passed is check_should_pass, f"FAILED, eval_result: {eval_results}"
