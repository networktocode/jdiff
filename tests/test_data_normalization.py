"Flatten list unit test"
import pytest
from netcompare.utils.data_normalization import flatten_list
from .utility import ASSERT_FAIL_MESSAGE


flatten_list_case_1 = (
    [[[[-1, 0], [-1, 0]]]],
    [[-1, 0], [-1, 0]],
)

flatten_list_tests = [
    flatten_list_case_1,
]


@pytest.mark.parametrize("data, expected_output", flatten_list_tests)
def test_value_parser(data, expected_output):
    output = flatten_list(data)
    assert expected_output == output, ASSERT_FAIL_MESSAGE.format(output=output, expected_output=expected_output)
