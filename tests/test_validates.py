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



parameter_no_params = (
    "parameter_match",
    {"mode": "match", "wrong_key": {"localAsn": "65130.1100", "linkType": "external"}},
    "'params' argument is mandatory for ParameterMatch Check Type.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [parameter_no_params])
def test_parameter_param(check_type_str, evaluate_args,expected_results):
    """Validate that CheckType parameter has 'params' key."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


parameter_wrong_type = (
    "parameter_match",
    {"mode": "match", "params": [{"localAsn": "65130.1100", "linkType": "external"}]},
    "'params' argument must be a dict. You have: <class 'list'>.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [parameter_wrong_type])
def test_parameter_value_type(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType parameter 'params' value type."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


parameter_no_mode = (
    "parameter_match",
    {"mode-no-mode": "match", "params": {"localAsn": "65130.1100", "linkType": "external"}},
    "'mode' argument is mandatory for ParameterMatch Check Type.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [parameter_no_mode])
def test_parameter_mode(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType parameter has mode key."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


parameter_mode_value = (
    "parameter_match",
    {"mode": ["match"], "params": {"localAsn": "65130.1100", "linkType": "external"}},
    "'mode' argument should be one of the following: match, no-match. You have: ['match']",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [parameter_mode_value])
def test_parameter_mode_value(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType parameter 'mode' has value of typ str."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


regex_no_params = (
    "regex",
    {"regexregex": ".*UNDERLAY.*", "mode": "match"},
    "'regex' argument is mandatory for Regex Check Type.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [regex_no_params])
def test_regex_param(check_type_str, evaluate_args,expected_results):
    """Validate that CheckType regex has 'params' key."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


regex_wrong_type = (
    "regex",
    {"regex": [".*UNDERLAY.*"], "mode-no-mode": "match"},
    "'regex' argument must be a string. You have: <class 'list'>.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [regex_wrong_type])
def test_regex_value_type(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType regex 'params' value type."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


regex_no_mode = (
    "regex",
    {"regex": ".*UNDERLAY.*", "mode-no-mode": "match"},
    "'mode' argument is mandatory for Regex Check Type.",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [regex_no_mode])
def test_regex_mode(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType regex has 'mode' key."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results


regex_mode_value = (
    "regex",
    {"regex": ".*UNDERLAY.*", "mode": "match-no-match"},
    "'mode' argument should be ['match', 'no-match']. You have: match-no-match",
)
@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [regex_mode_value])
def test_regex_mode_value(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType regex 'mode' has value of typ str."""
    check = CheckType.init(check_type_str)
    
    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)
    
    assert exc_info.type is ValueError and  exc_info.value.args[0] == expected_results