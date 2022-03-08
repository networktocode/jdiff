"""Unit tests for validator CheckType method."""
import pytest
from netcompare.check_types import CheckType

tolerance_wrong_argumet = (
    "tolerance",
    {"gt": 10},
    "'tolerance' argument is mandatory for Tolerance Check Type.",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [tolerance_wrong_argumet])
def test_tolerance_key_name(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType tolerance has `tolerance` key."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


tolerance_wrong_value = (
    "tolerance",
    {"tolerance": "10"},
    "Tolerance argument's value must be an integer. You have: <class 'str'>.",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [tolerance_wrong_value])
def test_tolerance_value_type(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType tolerance has `tolerance` value of type int"""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


parameter_no_params = (
    "parameter_match",
    {"mode": "match", "wrong_key": {"localAsn": "65130.1100", "linkType": "external"}},
    "'params' argument is mandatory for ParameterMatch Check Type.",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [parameter_no_params])
def test_parameter_param(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType parameter has 'params' key."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


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

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


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

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


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

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


regex_no_params = (
    "regex",
    {"regexregex": ".*UNDERLAY.*", "mode": "match"},
    "'regex' argument is mandatory for Regex Check Type.",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [regex_no_params])
def test_regex_param(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType regex has 'params' key."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


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

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


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

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


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

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params = (
    "operator",
    {"my_params": {"mode": "not-in", "operator_data": [20, 40, 60]}},
    "'params' argument must be provided. You have: my_params.",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params])
def test_operator_params(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'params' argument."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_mode = (
    "operator",
    {"params": {"no-mode": "not-in", "not-operator_data": [20, 40, 60]}},
    "'mode' and 'operator_data' arguments must be provided. You have: ['no-mode', 'not-operator_data'].",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_mode])
def test_operator_params_mode(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_wrong_operator = (
    "operator",
    {"params": {"mode": "random", "operator_data": [20, 40, 60]}},
    "'params' value must be one of the following: ['is-in', 'not-in', 'in-range', 'not-range', 'all-same', 'is-gt', 'is-lt', 'contains', 'not-contains']. You have: random",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_wrong_operator])
def test_operator_params_wrong_operator(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_in = (
    "operator",
    {"params": {"mode": "in-range", "operator_data": "string"}},
    "check options ('is-in', 'not-in', 'in-range', 'not-range') must have value of type list or tuple. i.e: dict(not-in=('Idle', 'Down'). You have: string of type <class 'str'>.",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_in])
def test_operator_params_in(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_in_range = (
    "operator",
    {"params": {"mode": "in-range", "operator_data": (0, "1")}},
    "'range' check-option in-range must have value of type list or tuple with items of type float or int. i.e: dict(not-range=(70000000, 80000000). You have: (0, '1').",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_in_range])
def test_operator_params_in_range(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_in_range_lower_than = (
    "operator",
    {"params": {"mode": "in-range", "operator_data": (1, 0)}},
    "'range' and 'not-range' must have value at index 0 lower than value at index 1. i.e: dict(not-range=(70000000, 80000000). You have: (1, 0).",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_in_range_lower_than])
def test_operator_params_in_range_lower_than(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_number = (
    "operator",
    {"params": {"mode": "is-gt", "operator_data": "1"}},
    "check options ('is-gt', 'is-lt') must have value of type float or int. You have: 1 of type <class 'str'>",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_number])
def test_operator_params_in_params_number(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_contains = (
    "operator",
    {"params": {"mode": "contains", "operator_data": 1}},
    "check options ('contains', 'not-contains') must have value of type string. You have: 1 of type <class 'int'>",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_contains])
def test_operator_params_contains(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results


operator_params_bool = (
    "operator",
    {"params": {"mode": "all-same", "operator_data": 1}},
    "check option all-same must have value of type bool. You have: 1 of type <class 'int'>",
)


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", [operator_params_bool])
def test_operator_params_bool(check_type_str, evaluate_args, expected_results):
    """Validate that CheckType operator if has 'mode' and 'operator_data' arguments."""
    check = CheckType.init(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        check.validate(**evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results
