"""CheckType Implementation."""
import re
from typing import Mapping, Tuple, List, Dict, Any, Union
from abc import ABC, abstractmethod
import jmespath
from .utils.jmespath_parsers import (
    jmespath_value_parser,
    jmespath_refkey_parser,
    associate_key_of_my_value,
    keys_values_zipper,
)
from .utils.data_normalization import exclude_filter, flatten_list
from .evaluators import diff_generator, parameter_evaluator, regex_evaluator, operator_evaluator


# pylint: disable=arguments-differ
class CheckType(ABC):
    """Check Type Base Abstract Class."""

    @staticmethod
    def init(check_type: str):
        """Factory pattern to get the appropriate CheckType implementation.

        Args:
            check_type: String to define the type of check.
        """
        if check_type == "exact_match":
            return ExactMatchType()
        if check_type == "tolerance":
            return ToleranceType()
        if check_type == "parameter_match":
            return ParameterMatchType()
        if check_type == "regex":
            return RegexType()
        if check_type == "operator":
            return OperatorType()

        raise NotImplementedError

    @staticmethod
    def get_value(output: Union[Mapping, List], path: str, exclude: List = None) -> Any:
        """Return data from output depending on the check path. See unit test for complete example.

        Get the wanted values to be evaluated if JMESPath expression is defined,
        otherwise use the entire output if jmespath is not defined in check. This covers the "raw" diff type.
        Exclude data not desired to compare.

        Notes:
            https://jmespath.org/ shows how JMESPath works.

        Args:
            output: json data structure
            path: JMESPath to extract specific values
            exclude: list of keys to exclude
        Returns:
            Evaluated data, may be anything depending on JMESPath used.
        """
        if exclude and isinstance(output, Dict):
            if not isinstance(exclude, list):
                raise ValueError(f"Exclude list must be defined as a list. You have {type(exclude)}")

            exclude_filter(output, exclude)  # exclude unwanted elements

        if not path:
            return output  # return if path is not specified

        values = jmespath.search(jmespath_value_parser(path), output)

        if not any(isinstance(i, list) for i in values):  # check for multi-nested lists if not found return here
            return values

        for element in values:  # process elements to check is lists should be flatten
            # TODO: Not sure how this is working because from `jmespath.search` it's supposed to get a flat list
            # of str or Decimals, not another list...
            for item in element:
                if isinstance(item, dict):  # raise if there is a dict, path must be more specific to extract data
                    raise TypeError(
                        f'Must be list of lists i.e. [["Idle", 75759616], ["Idle", 75759620]].' f"You have {values}'."
                    )
                if isinstance(item, list):
                    values = flatten_list(values)  # flatten list and rewrite values
                    break  # items are the same, need to check only first to see if this is a nested list

        paired_key_value = associate_key_of_my_value(jmespath_value_parser(path), values)

        # We need to get a list of reference keys - list of strings.
        # Based on the expression or output type we might have different data types
        # therefore we need to normalize.
        if re.search(r"\$.*\$", path):
            wanted_reference_keys = jmespath.search(jmespath_refkey_parser(path), output)

            if isinstance(wanted_reference_keys, dict):  # when wanted_reference_keys is dict() type
                list_of_reference_keys = list(wanted_reference_keys.keys())
            elif any(
                isinstance(element, list) for element in wanted_reference_keys
            ):  # when wanted_reference_keys is a nested list
                list_of_reference_keys = flatten_list(wanted_reference_keys)[0]
            elif isinstance(wanted_reference_keys, list):  # when wanted_reference_keys is a list
                list_of_reference_keys = wanted_reference_keys
            else:
                raise ValueError("Reference Key normalization failure. Please verify data type returned.")

            return keys_values_zipper(list_of_reference_keys, paired_key_value)

        return values

    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Tuple[Dict, bool]:
        """Return the result of the evaluation and a boolean True if it passes it or False otherwise.

        This method is the one that each CheckType has to implement.

        Args:
            *args: arguments specific to child class implementation
            **kwargs: named arguments

        Returns:
            tuple: Dictionary representing check result, bool indicating if differences are found.
        """
        # This method should call before any other logic the validation of the arguments
        # self.validate(**kwargs)

    @staticmethod
    @abstractmethod
    def validate(**kwargs) -> None:
        """Method to validate arguments that raises proper exceptions."""


class ExactMatchType(CheckType):
    """Exact Match class docstring."""

    @staticmethod
    def validate(**kwargs) -> None:
        """Method to validate arguments."""
        # reference_data = getattr(kwargs, "reference_data")

    def evaluate(self, value_to_compare: Any, reference_data: Any) -> Tuple[Dict, bool]:
        """Returns the difference between values and the boolean."""
        self.validate(reference_data=reference_data)
        evaluation_result = diff_generator(reference_data, value_to_compare)
        return evaluation_result, not evaluation_result


class ToleranceType(CheckType):
    """Tolerance class docstring."""

    @staticmethod
    def validate(**kwargs) -> None:
        """Method to validate arguments."""
        # reference_data = getattr(kwargs, "reference_data")
        tolerance = kwargs.get("tolerance")
        if not tolerance:
            raise ValueError("'tolerance' argument is mandatory for Tolerance Check Type.")
        if not isinstance(tolerance, int):
            raise ValueError(f"Tolerance argument's value must be an integer. You have: {type(tolerance)}.")

    def evaluate(self, value_to_compare: Any, reference_data: Any, tolerance: int) -> Tuple[Dict, bool]:
        """Returns the difference between values and the boolean. Overwrites method in base class."""
        self.validate(reference_data=reference_data, tolerance=tolerance)
        diff = diff_generator(reference_data, value_to_compare)
        self._remove_within_tolerance(diff, tolerance)
        return diff, not diff

    def _remove_within_tolerance(self, diff: Dict, tolerance: int) -> None:
        """Recursively look into diff and apply tolerance check, remove reported difference when within tolerance."""

        def _make_float(value: Any) -> float:
            """Make float, treat non-convertable as 0."""
            try:
                return float(value)
            except ValueError:
                return 0

        def _within_tolerance(*, old_value: Union[str, int, float], new_value: Union[str, int, float]) -> bool:
            """Return True if new value is within the tolerance range of the previous value."""
            tolerance_factor = tolerance / 100
            old_value, new_value = _make_float(old_value), _make_float(new_value)
            max_diff = old_value * tolerance_factor
            return (old_value - max_diff) < new_value < (old_value + max_diff)

        for key, value in list(diff.items()):  # casting list makes copy, so we don't modify object being iterated.
            if isinstance(value, dict):
                if "new_value" in value.keys() and "old_value" in value.keys() and _within_tolerance(**value):
                    diff.pop(key)
                else:
                    self._remove_within_tolerance(diff[key], tolerance)
                if not value:
                    diff.pop(key)


class ParameterMatchType(CheckType):
    """Parameter Match class implementation."""

    @staticmethod
    def validate(**kwargs) -> None:
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        params = kwargs.get("params")
        if not params:
            raise ValueError("'params' argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(params, dict):
            raise ValueError(f"'params' argument must be a dict. You have: {type(params)}.")

        mode = kwargs.get("mode")
        if not mode:
            raise ValueError("'mode' argument is mandatory for ParameterMatch Check Type.")
        if mode not in mode_options:
            raise ValueError(
                f"'mode' argument should be one of the following: {', '.join(mode_options)}. You have: {mode}"
            )

    def evaluate(self, value_to_compare: Mapping, params: Dict, mode: str) -> Tuple[Dict, bool]:
        """Parameter Match evaluator implementation."""
        self.validate(params=params, mode=mode)
        # TODO: we don't use the mode?
        evaluation_result = parameter_evaluator(value_to_compare, params, mode)
        return evaluation_result, not evaluation_result


class RegexType(CheckType):
    """Regex Match class implementation."""

    @staticmethod
    def validate(**kwargs) -> None:
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        regex = kwargs.get("regex")
        if not regex:
            raise ValueError("'regex' argument is mandatory for Regex Check Type.")
        if not isinstance(regex, str):
            raise ValueError(f"'regex' argument must be a string. You have: {type(regex)}.")

        mode = kwargs.get("mode")
        if not mode:
            raise ValueError("'mode' argument is mandatory for Regex Check Type.")
        if mode not in mode_options:
            raise ValueError(f"'mode' argument should be {mode_options}. You have: {mode}")

    def evaluate(self, value_to_compare: Mapping, regex: str, mode: str) -> Tuple[Mapping, bool]:
        """Regex Match evaluator implementation."""
        self.validate(regex=regex, mode=mode)
        diff = regex_evaluator(value_to_compare, regex, mode)
        return diff, not diff


class OperatorType(CheckType):
    """Operator class implementation."""

    @staticmethod
    def validate(**kwargs) -> None:
        """Validate operator parameters."""
        in_operators = ("is-in", "not-in", "in-range", "not-range")
        bool_operators = ("all-same",)
        number_operators = ("is-gt", "is-lt")
        # "equals" is redundant with check type "exact_match" an "parameter_match"
        # equal_operators = ("is-equal", "not-equal")
        string_operators = ("contains", "not-contains")
        valid_options = (
            in_operators,
            bool_operators,
            number_operators,
            string_operators,
            # equal_operators,
        )

        # Validate "params" argument is not None.
        if not kwargs or list(kwargs.keys())[0] != "params":
            raise ValueError(f"'params' argument must be provided. You have: {list(kwargs.keys())[0]}.")

        params_key = kwargs["params"].get("mode")
        params_value = kwargs["params"].get("operator_data")

        if not params_key or not params_value:
            raise ValueError(
                f"'mode' and 'operator_data' arguments must be provided. You have: {list(kwargs['params'].keys())}."
            )

        # Validate "params" value is legal.
        if all(params_key not in sub_element for element in valid_options for sub_element in element):
            raise ValueError(
                f"'params' value must be one of the following: {[sub_element for element in valid_options for sub_element in element]}. You have: {params_key}"
            )

        if params_key in in_operators:
            # "is-in", "not-in", "in-range", "not-range" requires an iterable
            if not isinstance(params_value, (list, tuple)):
                raise ValueError(
                    f"check options {in_operators} must have value of type list or tuple. i.e: dict(not-in=('Idle', 'Down'). You have: {params_value} of type {type(params_value)}."
                )

            # "in-range", "not-range" requires int or float where value at index 0 is lower than value at index 1
            if params_key in ("in-range", "not-range"):
                if (
                    len(params_value) != 2
                    or not isinstance(params_value[0], (int, float))
                    or not isinstance(params_value[1], (float, int))
                ):
                    raise ValueError(
                        f"'range' check-option {params_key} must have value of type list or tuple with items of type float or int. i.e: dict(not-range=(70000000, 80000000). You have: {params_value}."
                    )
                if not params_value[0] < params_value[1]:
                    raise ValueError(
                        f"'range' and 'not-range' must have value at index 0 lower than value at index 1. i.e: dict(not-range=(70000000, 80000000). You have: {params_value}."
                    )

        # "is-gt","is-lt"  require either int() or float()
        elif params_key in number_operators and not isinstance(params_value, (float, int)):
            raise ValueError(
                f"check options {number_operators} must have value of type float or int. You have: {params_value} of type {type(params_value)}"
            )

        # "contains", "not-contains" require string.
        elif params_key in string_operators and not isinstance(params_value, str):
            raise ValueError(
                f"check options {string_operators} must have value of type string. You have: {params_value} of type {type(params_value)}"
            )

        # "all-same" requires boolean True or False
        elif params_key in bool_operators and not isinstance(params_value, bool):
            raise ValueError(
                f"check option all-same must have value of type bool. You have: {params_value} of type {type(params_value)}"
            )

    def evaluate(self, value_to_compare: Any, params: Any) -> Tuple[Mapping, bool]:
        """Operator evaluator implementation."""
        self.validate(**params)
        # For name consistency.
        reference_data = params
        return operator_evaluator(reference_data["params"], value_to_compare)
