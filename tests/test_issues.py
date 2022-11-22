"""jdiff github issues unit tests."""
import pytest
import jdiff
from jdiff import extract_data_from_json, CheckType
from .utility import load_mocks, ASSERT_FAIL_MESSAGE

issue_91 = (
    "napalm_get_interfaces",
    "exact_match",
    {},
    "$*$.[is_up,is_enabled]",
    (
        {},
        False,
    ),
)

check_tests = [
    issue_91,
]


@pytest.mark.parametrize("folder_name, check_type_str, evaluate_args, path, expected_result", check_tests)
def test_checks(folder_name, check_type_str, evaluate_args, path, expected_result):
    """Validate multiple checks on the same data to catch corner cases."""
    check = CheckType.create(check_type_str)
    pre_data, post_data = load_mocks(folder_name)
    pre_value = extract_data_from_json(pre_data, path)
    post_value = extract_data_from_json(post_data, path)
    actual_results = check.evaluate(pre_value, post_value, **evaluate_args)

    assert actual_results == expected_result, ASSERT_FAIL_MESSAGE.format(
        output=actual_results, expected_output=expected_result
    )
