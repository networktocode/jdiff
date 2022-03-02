"""CheckType Implementation."""
import re
from typing import Mapping, Tuple, List, Dict, Any, Union
from abc import ABC, abstractmethod
import jmespath


from .utils.jmespath_parsers import (
    jmespath_value_parser,
    jmespath_refkey_parser,
    associate_key_of_my_value,
    keys_cleaner,
    keys_values_zipper,
)
from .utils.data_normalization import exclude_filter, flatten_list
from .evaluators import diff_generator, parameter_evaluator, regex_evaluator

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

        if re.search(r"\$.*\$", path):  # normalize
            wanted_reference_keys = jmespath.search(jmespath_refkey_parser(path), output)
            list_of_reference_keys = keys_cleaner(wanted_reference_keys)
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
    def validate(**kwargs):
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
    def validate(**kwargs):
        """Method to validate arguments."""
        # reference_data = getattr(kwargs, "reference_data")
        tolerance = kwargs.get("tolerance")
        if not tolerance:
            raise ValueError("Tolerance argument is mandatory for Tolerance Check Type.")
        if not isinstance(tolerance, int):
            raise ValueError(f"Tolerance argument must be an integer, and it's {type(tolerance)}.")

    def evaluate(self, value_to_compare: Any, reference_data: Any, tolerance: int) -> Tuple[Dict, bool]:
        """Returns the difference between values and the boolean. Overwrites method in base class."""
        self.validate(reference_data=reference_data, tolerance=tolerance)
        diff = diff_generator(reference_data, value_to_compare)
        self._remove_within_tolerance(diff, tolerance)
        return diff, not diff

    def _remove_within_tolerance(self, diff: Dict, tolerance: int) -> None:
        """Recursively look into diff and apply tolerance check, remove reported difference when within tolerance."""

        def _make_float(value):
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
    def validate(**kwargs):
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        params = kwargs.get("params")
        if not params:
            raise ValueError("Params argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(params, dict):
            raise ValueError(f"Params argument must be a dict, and it's {type(params)}.")

        mode = kwargs.get("mode")
        if not mode:
            raise ValueError("Mode argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(mode, str):
            raise ValueError(f"Mode argument must be a string, and it's {type(mode)}.")
        if mode not in mode_options:
            raise ValueError(f"Mode argument should be {mode_options}, and it's {mode}")

    def evaluate(self, value_to_compare: Mapping, params: Dict, mode: str) -> Tuple[Dict, bool]:
        """Parameter Match evaluator implementation."""
        self.validate(params=params, mode=mode)
        # TODO: we don't use the mode?
        evaluation_result = parameter_evaluator(value_to_compare, params)
        return evaluation_result, not evaluation_result


class RegexType(CheckType):
    """Regex Match class implementation."""

    @staticmethod
    def validate(**kwargs):
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        regex = kwargs.get("regex")
        if not regex:
            raise ValueError("Params argument is mandatory for Regex Match Check Type.")
        if not isinstance(regex, str):
            raise ValueError(f"Params argument must be a string, and it's {type(regex)}.")

        mode = kwargs.get("mode")
        if not mode:
            raise ValueError("Mode argument is mandatory for Regex Match Check Type.")
        if not isinstance(mode, str):
            raise ValueError(f"Mode argument must be a string, and it's {type(mode)}.")
        if mode not in mode_options:
            raise ValueError(f"Mode argument should be {mode_options}, and it's {mode}")

    def evaluate(self, value_to_compare: Mapping, regex: str, mode: str) -> Tuple[Mapping, bool]:
        """Regex Match evaluator implementation."""
        self.validate(regex=regex, mode=mode)
        diff = regex_evaluator(value_to_compare, regex, mode)
        return diff, not diff
