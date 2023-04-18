"""Test extract_data_from_json."""
import pytest
from jdiff import extract_data_from_json
from .utility import load_json_file


test_cases_extract_data_none = [
    "global[*]",
    'global.peers."1.1.1.1"',
]


@pytest.mark.parametrize("jmspath", test_cases_extract_data_none)
def test_jmspath_return_none(jmspath):
    """Handle exception when JMSPath returns None."""
    data = {"global": {"peers": {"10.1.0.0": "peer1", "10.2.0.0": "peer2"}}}
    with pytest.raises(TypeError) as error:
        extract_data_from_json(data=data, path=jmspath)

    assert "JMSPath returned 'None'. Please, verify your JMSPath regex." in error.value.__str__()


test_cases_extract_data_no_ref_key = [
    ("global.peers.*.*.ipv6.[accepted_prefixes]", [[1000], [1000], [1000], [1000]]),
    ("vpn.peers.*.*.ipv6.[accepted_prefixes]", [[1000], [1000]]),
    (
        "*.peers.*.*.*.[accepted_prefixes]",
        [[1000], [1000], [1000], [1000], [1000], [1000], [1000], [1000], [1000], [1000], [1000], [1000]],
    ),
]


test_cases_extract_data_with_ref_key = [
    (
        "global.peers.$*$.*.ipv6.[accepted_prefixes]",
        [
            {"10.1.0.0": {"accepted_prefixes": 1000}},
            {"10.2.0.0": {"accepted_prefixes": 1000}},
            {"10.64.207.255": {"accepted_prefixes": 1000}},
            {"7.7.7.7": {"accepted_prefixes": 1000}},
        ],
    ),
    (
        "vpn.peers.$*$.*.ipv6.[accepted_prefixes]",
        [{"10.1.0.0": {"accepted_prefixes": 1000}}, {"10.2.0.0": {"accepted_prefixes": 1000}}],
    ),
]


@pytest.mark.parametrize(
    "jmspath, expected_value", test_cases_extract_data_no_ref_key + test_cases_extract_data_with_ref_key
)
def test_extract_data_from_json(jmspath, expected_value):
    """Test JMSPath return value."""
    data = load_json_file("napalm_get_bgp_neighbors", "multi_vrf.json")
    value = extract_data_from_json(data=data, path=jmspath)

    assert value == expected_value
