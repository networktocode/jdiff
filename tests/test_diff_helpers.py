"""DIff helpers unit tests."""
from jdiff.utils.diff_helpers import dict_merger, group_value, fix_deepdiff_key_names, get_diff_iterables_items


def test_dict_merger():
    """Tests that dict is merged as expected and duplicates identified."""
    original_dict = dict(key_1="my_key_1", key_5="my_key_5")
    dict_to_merge = dict(key_1="my_key_1", key_2="my_key_2", key_3="my_key_3")
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
    assert group_value(tree_list, value) == {"10.1.0.0": {"is_enabled": {"new_value": False, "old_value": True}}}


def test_fix_deepdiff_key_names():
    """Tests that deepdiff return is parsed properly."""
    deepdiff_object = {"root[0]['10.1.0.0']['is_enabled']": {"new_value": False, "old_value": True}}
    assert fix_deepdiff_key_names(deepdiff_object) == {
        "10.1.0.0": {"is_enabled": {"new_value": False, "old_value": True}}
    }


def test_get_diff_iterables_items():
    """Tests that deepdiff return is parsed properly."""
    diff_result = {
        "values_changed": {"root['Ethernet1'][0]['port']": {"new_value": "518", "old_value": "519"}},
        "iterable_item_added": {
            "root['Ethernet3'][1]": {"hostname": "ios-xrv-unittest", "port": "Gi0/0/0/0"},
        },
    }
    result = get_diff_iterables_items(diff_result)

    assert list(dict(result).keys())[0] == "['Ethernet3']"
    assert list(list(dict(result).values())[0].values())[0] == [{"hostname": "ios-xrv-unittest", "port": "Gi0/0/0/0"}]
