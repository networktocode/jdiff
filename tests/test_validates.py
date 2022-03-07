"""Unit tests for validator CheckType method."""
import pytest
from netcompare.check_types import CheckType
from .utility import load_mocks

tolerance_wrong_argumet = (
    "tolerance",
    {"gt": 10},
    "'tolerance' argument is mandatory for Tolerance Check Type.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [tolerance_wrong_argumet])
def test_tolerance_key_name(check_type_str, evaluate_args,expected_results):
    """Validate that CheckType tolerance has `tolerance` key."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


tolerance_wrong_value = (
    "tolerance",
    {"tolerance": "10"},
    "Tolerance argument's value must be an integer. You have: <class 'str'>.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [tolerance_wrong_value])
def test_tolerance_value_type(check_type_str, evaluate_args,expected_results):
    """Validate that CheckType tolerance has `tolerance` value of type int"""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results
