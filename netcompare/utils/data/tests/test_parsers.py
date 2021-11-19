#!/usr/bin/env python3

import pytest
import sys
from ..parsers import exclude_filter
sys.path.append("..")


assertion_failed_message = """Test output is different from expected output.
output: {output}
expected output: {expected_output}
"""

exclude_filter_case_1 = (
    ["interfaceStatistics"],
    {
        "interfaces": {
        "Management1": {
            "name": "Management1",
            "interfaceStatus": "connected",
            "autoNegotiate": "success",
            "interfaceStatistics": {
                "inBitsRate": 3403.4362520883615,
                "inPktsRate": 3.7424095978179257,
                "outBitsRate": 16249.69114419833,
                "updateInterval": 300,
                "outPktsRate": 2.1111866059750692
                }
            }
        }
    },
    {
        "interfaces": {
        "Management1": {
            "name": "Management1",
            "interfaceStatus": "connected",
            "autoNegotiate": "success"
            }
        }
    }
)

exclude_filter_tests = [
    exclude_filter_case_1,
]


@pytest.mark.parametrize("exclude, data, expected_output", exclude_filter_tests)
def test_exclude_filter(exclude, data, expected_output):
    exclude_filter(data, exclude)
    assert expected_output == data, assertion_failed_message.format(output=data, expected_output=expected_output)
