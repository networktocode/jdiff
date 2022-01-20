"""CheckType Implementation."""
import re
from typing import Mapping, Tuple, List, Dict, Any, Union
import jmespath

from netcompare.arguments import (
    CheckArguments,
    CheckArgumentsExactMatch,
    CheckArgumentsParameterMatch,
    CheckArgumentsRegexMatch,
    CheckArgumentsToleranceMatch,
)

from .utils.jmespath_parsers import (
    jmespath_value_parser,
    jmespath_refkey_parser,
    associate_key_of_my_value,
    keys_cleaner,
    keys_values_zipper,
)
from .utils.data_normalization import exclude_filter, flatten_list
from .evaluators import diff_generator, parameter_evaluator, regex_evaluator
from .check_types import *


class CheckType:
    """Check Type Class."""

    class_args = CheckArguments

    def __init__(self, *args):
        """Check Type init method."""

    @staticmethod
    def init(check_type):
        """Factory pattern to get the appropriate CheckType implementation.

        Args:
            *args: Variable length argument list.
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
            # TODO: Not sure how this is working becasyse from `jmespath.search` it's supposed to get a flat list
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

    def hook_evaluate(self, reference_value: CheckArguments, value_to_compare: Any) -> Tuple[Dict, bool]:
        """Return the result of the evaluation and a boolean True if it passes it or False otherwise.

        This method is the one that each CheckType has to implement.

        Args:
            reference_value: Can be any structured data or just a simple value.
            value_to_compare: Similar value as above to perform comparison.

        Returns:
            tuple: Dictionary representing check result, bool indicating if differences are found.
        """
        raise NotImplementedError

    def evaluate(self, reference_value: dict, value_to_compare: Any) -> Tuple[Dict, bool]:

        return self.hook_evaluate(self.args_class(reference_value), value_to_compare)


class ExactMatchType(CheckType):
    """Exact Match class docstring."""

    args_class = CheckArgumentsExactMatch

    def evaluate(self, reference_value: CheckArgumentsExactMatch, value_to_compare: Any) -> Tuple[Dict, bool]:
        """Returns the difference between values and the boolean."""
        evaluation_result = diff_generator(reference_value.reference_data, value_to_compare)
        return evaluation_result, not evaluation_result


class ToleranceType(CheckType):
    """Tolerance class docstring."""

    def __init__(self, *args):
        """Tolerance init method."""
        super().__init__()

        try:
            tolerance = float(args[1])
        except IndexError as error:
            raise IndexError(f"Tolerance parameter must be defined as float at index 1. You have: {args}") from error
        except ValueError as error:
            raise ValueError(f"Argument must be convertible to float. You have: {args[1]}") from error

        self.tolerance_factor = tolerance / 100

    def hook_evaluate(
        self, reference_value: CheckArgumentsToleranceMatch, value_to_compare: Mapping
    ) -> Tuple[Dict, bool]:
        """Returns the difference between values and the boolean. Overwrites method in base class."""
        diff = diff_generator(reference_value.reference_data, value_to_compare)
        self._remove_within_tolerance(diff, reference_value.tolerance)
        return diff, not diff

    def _remove_within_tolerance(self, diff: Dict, tolerance: int) -> None:
        """Recursively look into diff and apply tolerance check, remove reported difference when within tolerance."""

        def _within_tolerance(*, old_value: float, new_value: float) -> bool:
            """Return True if new value is within the tolerance range of the previous value."""
            max_diff = old_value * tolerance
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

    def hook_evaluate(
        self, reference_value: CheckArgumentsParameterMatch, value_to_compare: Mapping
    ) -> Tuple[Dict, bool]:
        """Parameter Match evaluator implementation."""
        if not isinstance(value_to_compare, dict):
            raise TypeError("check_option must be of type dict()")

        # TODO: update this
        evaluation_result = parameter_evaluator(reference_value, value_to_compare)
        return evaluation_result, not evaluation_result


class RegexType(CheckType):
    """Regex Match class implementation."""

    def hook_evaluate(
        self, reference_value: CheckArgumentsRegexMatch, value_to_compare: Mapping
    ) -> Tuple[Mapping, bool]:
        """Regex Match evaluator implementation."""
        # Check that check value_to_compare is dict.
        if not isinstance(value_to_compare, dict):
            raise TypeError("check_option must be of type dict().")

        # Check that value_to_compare has 'regex' and 'mode' dict keys.
        if any(key not in value_to_compare.keys() for key in ("regex", "mode")):
            raise KeyError(
                "Regex check-type requires check-option. Example: dict(regex='.*UNDERLAY.*', mode='no-match')."
            )

        # Assert that check option has 'regex' and 'mode' dict keys.\
        if value_to_compare["mode"] not in ["match", "no-match"]:
            raise ValueError(
                "Regex check-type requires check-option. Example: dict(regex='.*UNDERLAY.*', mode='no-match')."
            )

        # TODO: update this
        diff = regex_evaluator(reference_value, value_to_compare)
        return diff, not diff
