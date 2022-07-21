"""Test GitHub issues."""
import pytest
from netcompare import CheckType
from .utility import ASSERT_FAIL_MESSAGE


issue_67 = (
    {"global": {"peers": {"10.1.0.0": "peer1", "10.2.0.0": "peer2"}}},
    "TypeError: 'output' must be a valid JSON object. You have <class 'dict'>"
    )

issue_67_test = [
    issue_67,
]


@pytest.mark.parametrize("data, expected_output", issue_67_test)
def test_issue_67(data, expected_output):
    """Resolve issue 67: https://github.com/networktocode-llc/netcompare/issues/67"""
    my_jmspath = "global[*]"
    my_check = CheckType.init(check_type="exact_match")
    with pytest.raises(TypeError) as error:
        my_check.get_value(output=data, path=my_jmspath)()  # pylint: disable=E0110

    assert (
        "'output' must be a valid JSON object. You have <class 'dict'>" in error.value.__str__()
    )