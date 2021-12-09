"Reference key unit tests."
import pytest
from netcompare.utils.refkey import keys_cleaner, keys_values_zipper, associate_key_of_my_value


ASSERTION_FAILED_MESSAGE = """Test output is different from expected output.
output: {output}
expected output: {expected_output}
"""

keys_cleaner_case_1 = (
    {"10.1.0.0": {"address_family": "ipv4"}},
    ["10.1.0.0"],
)

keys_zipper_case_1 = (
    ["10.1.0.0", "10.2.0.0"],
    [{"is_enabled": False, "is_up": False}, {"is_enabled": True, "is_up": True}],
    [{"10.1.0.0": {"is_enabled": False, "is_up": False}}, {"10.2.0.0": {"is_enabled": True, "is_up": True}}],
)

keys_association_case_1 = (
    "global.peers.*.[is_enabled,is_up]",
    [[True, False], [True, False]],
    [{"is_enabled": True, "is_up": False}, {"is_enabled": True, "is_up": False}],
)

keys_cleaner_tests = [
    keys_cleaner_case_1,
]

keys_zipper_tests = [
    keys_zipper_case_1,
]

keys_association_test = [
    keys_association_case_1,
]


@pytest.mark.parametrize("wanted_key, expected_output", keys_cleaner_tests)
def test_keys_cleaner(wanted_key, expected_output):
    output = keys_cleaner(wanted_key)
    assert expected_output == output, ASSERTION_FAILED_MESSAGE.format(output=output, expected_output=expected_output)


@pytest.mark.parametrize("ref_keys, wanted_values, expected_output", keys_zipper_tests)
def test_keys_zipper(ref_keys, wanted_values, expected_output):
    output = keys_values_zipper(ref_keys, wanted_values)
    assert expected_output == output, ASSERTION_FAILED_MESSAGE.format(output=output, expected_output=expected_output)


@pytest.mark.parametrize("path, wanted_values, expected_output", keys_association_test)
def test_keys_association(path, wanted_values, expected_output):
    output = associate_key_of_my_value(path, wanted_values)
    assert expected_output == output, ASSERTION_FAILED_MESSAGE.format(output=output, expected_output=expected_output)
