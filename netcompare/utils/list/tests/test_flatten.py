#!/usr/bin/env python3

import pytest
import sys
import pdb
from ..flatten import flatten_list
sys.path.append("..")


assertion_failed_message = """Test output is different from expected output.
output: {output}
expected output: {expected_output}
"""

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
    assert expected_output == output, assertion_failed_message.format(output=output, expected_output=expected_output)
