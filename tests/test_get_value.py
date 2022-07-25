"""Test GitHub issues."""
import pytest
from netcompare import CheckType


my_data = {"global": {"peers": {"10.1.0.0": "peer1", "10.2.0.0": "peer2"}}}


@pytest.mark.parametrize("data", [my_data])
def test_jmspath_return_none(data):
    """Habdle exception when JMSPath retunr None."""
    my_jmspath = "global[*]"
    my_check = CheckType.init(check_type="exact_match")
    with pytest.raises(TypeError) as error:
        my_check.get_value(output=data, path=my_jmspath)()  # pylint: disable=E0110

    assert "JMSPath returned 'None'. Please, verify your JMSPath regex." in error.value.__str__()
