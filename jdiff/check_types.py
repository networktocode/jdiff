"""CheckType Implementation."""
from typing import Mapping, Tuple, Dict, Any, Union
from abc import ABC, abstractmethod
from .evaluators import diff_generator, parameter_evaluator, regex_evaluator, operator_evaluator


# pylint: disable=arguments-differ
class CheckType(ABC):
    """Check Type Base Abstract Class."""

    @staticmethod
    def create(check_type: str):
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
    # self._validate(**kwargs)
    @staticmethod
    @abstractmethod
    def _validate(*args) -> None:
        """Method to validate arguments that raises proper exceptions."""

    @staticmethod
    def result(evaluation_result) -> Tuple[Dict, bool]:
        """Result method implementation. Will return diff data and bool for checking failed result."""
        return evaluation_result, not evaluation_result


class ExactMatchType(CheckType):
    """Exact Match class docstring."""

    @staticmethod
    def _validate(reference_data):
        # No need for _validate method as exact-match does not take any specific arguments.
        pass

    def evaluate(self, reference_data: Any, value_to_compare: Any) -> Tuple[Dict, bool]:  # type: ignore
        """Returns the difference between values and the boolean."""
        evaluation_result = diff_generator(reference_data, value_to_compare)
        return self.result(evaluation_result)


class ToleranceType(CheckType):
    """Tolerance class docstring."""

    @staticmethod
    def _validate(tolerance) -> None:  # type: ignore[override]
        """Method to validate arguments."""
        # reference_data = getattr(kwargs, "reference_data")
        if not tolerance:
            raise ValueError("'tolerance' argument is mandatory for Tolerance Check Type.")
        if not isinstance(tolerance, (int, float)):
            raise ValueError(f"Tolerance argument's value must be a number. You have: {type(tolerance)}.")
        if tolerance < 0:
            raise ValueError(f"Tolerance value must be greater than 0. You have: {tolerance}.")

    def evaluate(self, reference_data: Any, value_to_compare: Any, tolerance: int) -> Tuple[Dict, bool]:  # type: ignore[override]
        """Returns the difference between values and the boolean. Overwrites method in base class."""
        self._validate(tolerance=tolerance)
        evaluation_result = diff_generator(reference_data, value_to_compare)
        self._remove_within_tolerance(evaluation_result, tolerance)
        return self.result(evaluation_result)

    def _remove_within_tolerance(self, diff: Dict, tolerance: Union[int, float]) -> None:
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
    def _validate(params, mode) -> None:  # type: ignore[override]
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        if not params:
            raise ValueError("'params' argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(params, dict):
            raise ValueError(f"'params' argument must be a dict. You have: {type(params)}.")

        if not mode:
            raise ValueError("'mode' argument is mandatory for ParameterMatch Check Type.")
        if mode not in mode_options:
            raise ValueError(
                f"'mode' argument should be one of the following: {', '.join(mode_options)}. You have: {mode}"
            )

    def evaluate(self, params: Dict, value_to_compare: Mapping, mode: str) -> Tuple[Dict, bool]:  # type: ignore[override]
        """Parameter Match evaluator implementation."""
        self._validate(params=params, mode=mode)
        # TODO: we don't use the mode?
        evaluation_result = parameter_evaluator(value_to_compare, params, mode)
        return self.result(evaluation_result)


class RegexType(CheckType):
    """Regex Match class implementation."""

    @staticmethod
    def _validate(regex, mode) -> None:  # type: ignore[override]
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        if not regex:
            raise ValueError("'regex' argument is mandatory for Regex Check Type.")
        if not isinstance(regex, str):
            raise ValueError(f"'regex' argument must be a string. You have: {type(regex)}.")

        if not mode:
            raise ValueError("'mode' argument is mandatory for Regex Check Type.")
        if mode not in mode_options:
            raise ValueError(f"'mode' argument should be {mode_options}. You have: {mode}")

    def evaluate(self, regex: str, value_to_compare: Mapping, mode: str) -> Tuple[Dict, bool]:  # type: ignore[override]
        """Regex Match evaluator implementation."""
        self._validate(regex=regex, mode=mode)
        evaluation_result = regex_evaluator(value_to_compare, regex, mode)
        return self.result(evaluation_result)


class OperatorType(CheckType):
    """Operator class implementation."""

    @staticmethod
    def _validate(params) -> None:  # type: ignore[override]
        """Validate operator parameters."""
        in_operators = ("is-in", "not-in", "in-range", "not-in-range")
        bool_operators = ("all-same",)
        number_operators = ("is-gt", "is-lt")
        string_operators = ("contains", "not-contains")
        valid_options = (
            in_operators,
            bool_operators,
            number_operators,
            string_operators,
        )

        # Validate "params" argument is not None.
        # {'params': {'mode': 'all-same', 'operator_data': True}}
        if not params or list(params.keys())[0] != "params":
            raise ValueError(f"'params' argument must be provided. You have: {list(params.keys())[0]}.")

        params_key = params.get("params", {}).get("mode")
        params_value = params.get("params", {}).get("operator_data")

        if not params_key or params_value is None:
            raise ValueError(
                f"'mode' and 'operator_data' arguments must be provided. You have: {list(params['params'].keys())}."
            )

        # Validate "params" value is legal.
        if all(params_key not in sub_element for element in valid_options for sub_element in element):
            raise ValueError(
                f"'params' value must be one of the following: {[sub_element for element in valid_options for sub_element in element]}. You have: {params_key}"
            )

        if params_key in in_operators:
            # "is-in", "not-in", "in-range", "not-in-range" requires an iterable
            if not isinstance(params_value, (list, tuple)):
                raise ValueError(
                    f"check options {in_operators} must have value of type list or tuple. i.e: dict(not-in=('Idle', 'Down'). You have: {params_value} of type {type(params_value)}."
                )

            # "in-range", "not-in-range" requires int or float where value at index 0 is lower than value at index 1
            if params_key in ("in-range", "not-in-range"):
                if (
                    len(params_value) != 2
                    or not isinstance(params_value[0], (int, float))
                    or not isinstance(params_value[1], (float, int))
                ):
                    raise ValueError(
                        f"'range' check-option {params_key} must have value of type list or tuple with items of type float or int. i.e: dict(not-in-range=(70000000, 80000000). You have: {params_value}."
                    )
                if not params_value[0] < params_value[1]:
                    raise ValueError(
                        f"'range' and 'not-in-range' must have value at index 0 lower than value at index 1. i.e: dict(not-in-range=(70000000, 80000000). You have: {params_value}."
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

    def evaluate(self, params: Any, value_to_compare: Any) -> Tuple[Dict, bool]:  # type: ignore[override]
        """Operator evaluator implementation."""
        self._validate(params)
        # For name consistency.
        reference_data = params
        evaluation_result = operator_evaluator(reference_data["params"], value_to_compare)
        return self.result(evaluation_result)

    def result(self, evaluation_result):
        """
        Operator result method overwrite.

        This is required as Opertor return its own boolean within result.
        """
        return evaluation_result[0], evaluation_result[1]
