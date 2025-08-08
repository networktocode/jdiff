"""Unit tests for validator CheckType method."""

import pytest

from jdiff import CheckType

tolerance_wrong_argumet = (
    "tolerance",
    {"gt": 10},
    "'tolerance' argument is mandatory for Tolerance Check Type.",
)
tolerance_wrong_value = (
    "tolerance",
    {"tolerance": "10"},
    "Tolerance argument's value must be a number. You have: <class 'str'>.",
)
parameter_no_params = (
    "parameter_match",
    {"mode": "match", "wrong_key": {"localAsn": "65130.1100", "linkType": "external"}},
    "'params' argument is mandatory for ParameterMatch Check Type.",
)
parameter_wrong_type = (
    "parameter_match",
    {"mode": "match", "params": [{"localAsn": "65130.1100", "linkType": "external"}]},
    "'params' argument must be a dict. You have: <class 'list'>.",
)
parameter_no_mode = (
    "parameter_match",
    {"mode-no-mode": "match", "params": {"localAsn": "65130.1100", "linkType": "external"}},
    "'mode' argument is mandatory for ParameterMatch Check Type.",
)
parameter_mode_value = (
    "parameter_match",
    {"mode": ["match"], "params": {"localAsn": "65130.1100", "linkType": "external"}},
    "'mode' argument should be one of the following: match, no-match. You have: ['match']",
)
regex_no_params = (
    "regex",
    {"regexregex": ".*UNDERLAY.*", "mode": "match"},
    "'regex' argument is mandatory for Regex Check Type.",
)
regex_wrong_type = (
    "regex",
    {"regex": [".*UNDERLAY.*"], "mode-no-mode": "match"},
    "'regex' argument must be a string. You have: <class 'list'>.",
)
regex_no_mode = (
    "regex",
    {"regex": ".*UNDERLAY.*", "mode-no-mode": "match"},
    "'mode' argument is mandatory for Regex Check Type.",
)
regex_mode_value = (
    "regex",
    {"regex": ".*UNDERLAY.*", "mode": "match-no-match"},
    "'mode' argument should be ['match', 'no-match']. You have: match-no-match",
)
operator_params = (
    "operator",
    {"my_params": {"mode": "not-in", "operator_data": [20, 40, 60]}},
    "'params' argument must be provided. You have: my_params.",
)
operator_params_mode = (
    "operator",
    {"params": {"no-mode": "not-in", "not-operator_data": [20, 40, 60]}},
    "'mode' and 'operator_data' arguments must be provided. You have: ['no-mode', 'not-operator_data'].",
)
operator_params_wrong_operator = (
    "operator",
    {"params": {"mode": "random", "operator_data": [20, 40, 60]}},
    "'params' value must be one of the following: ['is-in', 'not-in', 'in-range', 'not-in-range', 'all-same', 'is-gt', 'is-lt', 'is-ge', 'is-le', 'contains', 'not-contains']. You have: random",
)
operator_params_in = (
    "operator",
    {"params": {"mode": "in-range", "operator_data": "string"}},
    "check options ('is-in', 'not-in', 'in-range', 'not-in-range') must have value of type list or tuple. i.e: dict(not-in=('Idle', 'Down'). You have: string of type <class 'str'>.",
)
operator_params_in_range = (
    "operator",
    {"params": {"mode": "in-range", "operator_data": (0, "1")}},
    "'range' check-option in-range must have value of type list or tuple with items of type float or int. i.e: dict(not-in-range=(70000000, 80000000). You have: (0, '1').",
)
operator_params_in_range_lower_than = (
    "operator",
    {"params": {"mode": "in-range", "operator_data": (1, 0)}},
    "'range' and 'not-in-range' must have value at index 0 lower than value at index 1. i.e: dict(not-in-range=(70000000, 80000000). You have: (1, 0).",
)
operator_params_number = (
    "operator",
    {"params": {"mode": "is-gt", "operator_data": "1"}},
    "check options ('is-gt', 'is-lt', 'is-ge', 'is-le') must have value of type float or int. You have: 1 of type <class 'str'>",
)
operator_params_contains = (
    "operator",
    {"params": {"mode": "contains", "operator_data": 1}},
    "check options ('contains', 'not-contains') must have value of type string. You have: 1 of type <class 'int'>",
)
operator_params_bool = (
    "operator",
    {"params": {"mode": "all-same", "operator_data": 1}},
    "check option all-same must have value of type bool. You have: 1 of type <class 'int'>",
)

all_tests = [
    tolerance_wrong_argumet,
    tolerance_wrong_value,
    parameter_no_params,
    parameter_wrong_type,
    parameter_no_mode,
    parameter_mode_value,
    regex_no_params,
    regex_wrong_type,
    regex_no_mode,
    regex_mode_value,
    operator_params,
    operator_params_mode,
    operator_params_wrong_operator,
    operator_params_in,
    operator_params_in_range,
    operator_params_in_range_lower_than,
    operator_params_number,
    operator_params_contains,
    operator_params_bool,
]


@pytest.mark.parametrize("check_type_str, evaluate_args, expected_results", all_tests)
def test_validate_arguments(check_type_str, evaluate_args, expected_results):
    """Test CheckType validate method for each check-type."""
    check = CheckType.create(check_type_str)

    with pytest.raises(ValueError) as exc_info:
        if check_type_str == "tolerance":
            check._validate(evaluate_args.get("tolerance"))
        elif check_type_str == "parameter_match":
            check._validate(params=evaluate_args.get("params"), mode=evaluate_args.get("mode"))
        elif check_type_str == "regex":
            check._validate(regex=evaluate_args.get("regex"), mode=evaluate_args.get("mode"))
        elif check_type_str == "operator":
            check._validate(evaluate_args)

    assert exc_info.type is ValueError and exc_info.value.args[0] == expected_results
