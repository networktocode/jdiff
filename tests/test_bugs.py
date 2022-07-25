"""Test GitHub issues."""
import pytest
from netcompare import CheckType


issue_67 = {"global": {"peers": {"10.1.0.0": "peer1", "10.2.0.0": "peer2"}}}

issue_67_test = [
    issue_67,
]


@pytest.mark.parametrize("data", issue_67_test)
def test_issue_67(data):
    """Resolve issue 67: https://github.com/networktocode-llc/netcompare/issues/67"""
    my_jmspath = "global[*]"
    my_check = CheckType.init(check_type="exact_match")
    with pytest.raises(TypeError) as error:
        my_check.get_value(output=data, path=my_jmspath)()  # pylint: disable=E0110

    assert "JMSPath returned 'None'. Please, verify your JMSPath regex." in error.value.__str__()
