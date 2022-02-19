"""Tests for typical software upgrade device state check."""
import pytest
from netcompare.check_types import CheckType
from .utility import load_json_file


@pytest.mark.parametrize(
    "platform, command, jpath, expected, test_result",
    [
        ("arista_eos", "show_version", "[*].[$image$,image]", {"image": "4.14.7M"}, True),
        ("arista_eos", "show_version", "[*].[$image$,image]", {"image": "no-match"}, False),
        ("cisco_ios", "show_version", "[*].[$version$,version]", {"version": "12.2(54)SG1"}, True),
        ("cisco_ios", "show_version", "[*].[$version$,version]", {"version": "no-match"}, False),
    ],
)
def test_show_version(platform, command, jpath, expected, test_result):
    """Test expected version."""
    filename = f"{platform}_{command}.json"
    command = load_json_file("sw_upgrade", filename)

    check = CheckType.init("parameter_match")
    value = check.get_value(command, jpath)
    result = check.evaluate(value, expected, "match")  # pylint: disable=E1121
    assert result[1] is test_result


@pytest.mark.parametrize(
    "platform, command, jpath, test_result",
    [
        ("arista_eos", "show_interface", "[*].[$interface$,link_status,protocol_status]", True),
        ("cisco_ios", "show_interface", "[*].[$interface$,link_status,protocol_status]", True),
        ("arista_eos", "show_interface", "[*].[$interface$,link_status,protocol_status]", False),
        ("cisco_ios", "show_interface", "[*].[$interface$,link_status,protocol_status]", False),
    ],
)
def test_show_interfaces_state(platform, command, jpath, test_result):
    """Test the interface status."""
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")

    if test_result is False:
        command_post[0]["link_status"] = "down"
        command_post[1]["protocol_status"] = "down"

    check = CheckType.init("exact_match")
    pre_value = CheckType.get_value(command_pre, jpath)
    post_value = CheckType.get_value(command_post, jpath)
    result = check.evaluate(post_value, pre_value)
    assert result[1] is test_result


@pytest.mark.parametrize(
    "platform, command",
    [
        ("arista_eos", "show_ip_route"),
        ("cisco_ios", "show_ip_route"),
    ],
)
def test_show_ip_route_exact_match(platform, command):
    """Test identical route table pass the test."""
    command_pre = command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")

    check = CheckType.init("exact_match")
    result = check.evaluate(command_post, command_pre)
    assert result[1] is True


@pytest.mark.xfail(reason="./utils/diff_helpers.py:32: AttributeError, list of dicts with different elem number.")
@pytest.mark.parametrize(
    "platform, command",
    [
        ("arista_eos", "show_ip_route"),
        ("cisco_ios", "show_ip_route"),
    ],
)
def test_show_ip_route_missing_and_additional_routes(platform, command):
    """Test missing or additional routes fail the test."""
    command_pre = command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    check = CheckType.init("exact_match")
    result_missing_routes = check.evaluate(command_post[:30], command_pre)
    result_additional_routes = check.evaluate(command_post, command_pre[:30])
    assert result_missing_routes[1] is False and result_additional_routes[1] is False


@pytest.mark.parametrize(
    "platform, command, jpath, test_result",
    [
        ("arista_eos", "show_ip_bgp_summary", "[*].[$bgp_neigh$,state]", True),
        ("arista_eos", "show_ip_bgp_summary", "[*].[$bgp_neigh$,state]", False),
        ("cisco_ios", "show_ip_bgp_neighbors", "[*].[$neighbor$,bgp_state]", True),
        ("cisco_ios", "show_ip_bgp_neighbors", "[*].[$neighbor$,bgp_state]", False),
    ],
)
def test_bgp_neighbor_state(platform, command, jpath, test_result):
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")

    if test_result is False:
        state_key = "state" if "arista" in platform else "bgp_state"
        command_post[0][state_key] = "Idle"

    check = CheckType.init("exact_match")
    pre_value = CheckType.get_value(command_pre, jpath)
    post_value = CheckType.get_value(command_post, jpath)
    result = check.evaluate(post_value, pre_value)
    assert result[1] is test_result


@pytest.mark.parametrize(
    "platform, command, jpath, test_result",
    [
        ("arista_eos", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", True),
        ("arista_eos", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", False),
        ("cisco_ios", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", True),
        ("cisco_ios", "show_ip_ospf_neighbors", "[*].[$neighbor_id$,state]", False),
    ],
)
def test_ospf_neighbor_state(platform, command, jpath, test_result):
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")

    if test_result is False:
        command_post[0]["state"] = "2WAY"
        command_post = command_post[:1]
        pytest.xfail("./utils/diff_helpers.py:32: AttributeError")

    check = CheckType.init("exact_match")
    pre_value = CheckType.get_value(command_pre, jpath)
    post_value = CheckType.get_value(command_post, jpath)
    result = check.evaluate(post_value, pre_value)
    assert result[1] is test_result


@pytest.mark.skip(reason="Command output not available")
def test_pim_neighbors():
    pass


@pytest.mark.parametrize(
    "platform, command, test_result",
    [
        ("arista_eos", "show_lldp_neighbors", True),
        ("arista_eos", "show_lldp_neighbors", False),
        ("cisco_ios", "show_lldp_neighbors", True),
        ("cisco_ios", "show_lldp_neighbors", False),
    ],
)
def test_lldp_neighbor_state(platform, command, test_result):
    command_pre = load_json_file("sw_upgrade", f"{platform}_{command}.json")
    command_post = load_json_file("sw_upgrade", f"{platform}_{command}.json")

    if test_result is False:
        command_post = command_post[:2]
        pytest.xfail("./utils/diff_helpers.py:32: AttributeError")

    check = CheckType.init("exact_match")
    result = check.evaluate(command_post, command_pre)
    assert result[1] is test_result
