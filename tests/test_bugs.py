"""Test GitHub issues."""
import pytest
from netcompare import CheckType
from .utility import ASSERT_FAIL_MESSAGE


issue_67 = (
    {"global": {"peers": {"10.1.0.0": "peer1", "10.2.0.0": "peer2"}}},
    []
    )

issue_67_test = [
    issue_67,
]


@pytest.mark.parametrize("data, expected_output", issue_67_test)
def test_issue_67(data, expected_output):
    """Resolve issue 67: https://github.com/networktocode-llc/netcompare/issues/67"""
    my_jmspath = "global[*]"
    my_check = CheckType.init(check_type="exact_match")
    pre_value = my_check.get_value(output=data, path=my_jmspath)
    assert pre_value == pre_value, ASSERT_FAIL_MESSAGE.format(output=pre_value, expected_output=expected_output)
