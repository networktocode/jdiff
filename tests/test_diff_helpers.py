"""DIff helpers unit tests."""

import pytest
from jdiff.utils.diff_helpers import (
    _parse_index_element_string,
    dict_merger,
    fix_deepdiff_key_names,
    get_diff_iterables_items,
    group_value,
    parse_diff,
)


def test_dict_merger():
    """Tests that dict is merged as expected and duplicates identified."""
    original_dict = {"key_1": "my_key_1", "key_5": "my_key_5"}
    dict_to_merge = {"key_1": "my_key_1", "key_2": "my_key_2", "key_3": "my_key_3"}
    dict_merger(original_dict, dict_to_merge)

    assert original_dict == {
        "key_1": "my_key_1",
        "key_1_dup!": "my_key_1",
        "key_2": "my_key_2",
        "key_3": "my_key_3",
        "key_5": "my_key_5",
    }


def test_group_value():
    """Tests that nested dict is recursively created."""
    tree_list = ["10.1.0.0", "is_enabled"]
    value = {"new_value": False, "old_value": True}
    assert group_value(tree_list, value) == {
        "10.1.0.0": {"is_enabled": {"new_value": False, "old_value": True}}
    }


def test_fix_deepdiff_key_names():
    """Tests that deepdiff return is parsed properly."""
    deepdiff_object = {
        "root[0]['10.1.0.0']['is_enabled']": {"new_value": False, "old_value": True}
    }
    assert fix_deepdiff_key_names(deepdiff_object) == {
        "10.1.0.0": {"is_enabled": {"new_value": False, "old_value": True}}
    }


def test_get_diff_iterables_items():
    """Tests that deepdiff return is parsed properly."""
    diff_result = {
        "values_changed": {
            "root['Ethernet1'][0]['port']": {"new_value": "518", "old_value": "519"}
        },
        "iterable_item_added": {
            "root['Ethernet3'][1]": {
                "hostname": "ios-xrv-unittest",
                "port": "Gi0/0/0/0",
            },
        },
    }
    result = get_diff_iterables_items(diff_result)

    assert list(dict(result).keys())[0] == "['Ethernet3']"
    assert list(list(dict(result).values())[0].values())[0] == [
        {"hostname": "ios-xrv-unittest", "port": "Gi0/0/0/0"}
    ]


# result = {'hostname': {'new_value': 'veos', 'old_value': 'veos-0'}, 'domain-name': 'missing'}
# result = {'domain-name': 'missing'}
# result = {'hostname': {'new_value': 'veos', 'old_value': 'veos-0'}, 'domain-name': 'missing', "index_element['openconfig-system:config']['ip name']": 'new'}
# result = {'domain-name': 'missing','hostname': 'missing', "index_element['openconfig-system:config']['ip name']": 'new'}
# result = {'servers': {'server': defaultdict(<class 'list'>, {'missing': [{'address': '1.us.pool.ntp.org', 'config': {'address': '1.us.pool.ntp.org'}, 'state': {'address': '1.us.pool.ntp.org'}}]})}}


index_element_case_1 = (
    "index_element['foo']['ip name']",
    {"ip name": ""},
)

index_element_case_2 = (
    "index_element['foo']['ip name']['ip domain']",
    {"ip name": "", "ip domain": ""},
)


index_element_tests = [index_element_case_1, index_element_case_2]


@pytest.mark.parametrize("index_element, result", index_element_tests)
def test__parse_index_element_string(index_element, result):
    """Test that index_element can be unpacked."""
    parsed_result = _parse_index_element_string(index_element)
    assert parsed_result == result


parse_diff_case_1 = (
    {
        "hostname": {"new_value": "veos", "old_value": "veos-0"},
        "domain-name": "missing",
    },
    {"openconfig-system:config": {"domain-name": "ntc.com", "hostname": "veos-0"}},
    {"openconfig-system:config": {"hostname": "veos"}},
    "openconfig-system:config",
    {"hostname": "veos-0"},
    {"hostname": "veos", "domain-name": "ntc.com"},
)


parse_diff_tests = [parse_diff_case_1]


@pytest.mark.parametrize(
    "jdiff_evaluate_response, actual, intended, match_config, extra, missing",
    parse_diff_tests,
)
def test_parse_diff(
    jdiff_evaluate_response, actual, intended, match_config, extra, missing
):
    """Test that index_element can be unpacked."""
    parsed_extra, parsed_missing = parse_diff(
        jdiff_evaluate_response,
        actual,
        intended,
        match_config,
    )
    assert (
        parsed_extra == extra
    )  # AssertionError: assert {'hostname': 'veos-0', 'domain-name': 'ntc.com'} == {'hostname': 'veos-0'}
    assert (
        parsed_missing == missing
    )  # AssertionError: assert {'hostname': 'veos'} == {'hostname': 'veos', 'domain-name': 'ntc.com'}
