"""Test GitHub issues."""
import pytest
from jdiff import extract_data_from_json


my_data = [{"global": {"peers": {"10.1.0.0": "peer1", "10.2.0.0": "peer2"}}}]


@pytest.mark.parametrize("data", my_data)
def test_jmspath_return_none(data):
    """Handle exception when JMSPath retunr None."""
    my_jmspath = "global[*]"
    with pytest.raises(TypeError) as error:
        extract_data_from_json(data=data, path=my_jmspath)()  # pylint: disable=E0110

    assert "JMSPath returned 'None'. Please, verify your JMSPath regex." in error.value.__str__()

