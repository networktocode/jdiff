"""CheckType Implementation."""
from typing import Mapping, Tuple, List, Dict, Any
from .evaluator import diff_generator, parameter_evaluator
from .runner import extract_values_from_output


class CheckType:
    """Check Type Class."""

    def __init__(self, *args):
        """Check Type init method."""

    @staticmethod
    def init(*args):
        """Factory pattern to get the appropriate CheckType implementation.

        Args:
            *args: Variable length argument list.
        """
        check_type = args[0]
        if check_type == "exact_match":
            return ExactMatchType(*args)
        if check_type == "tolerance":
            return ToleranceType(*args)
        if check_type == "parameter_match":
            return ParameterMatchType(*args)

        raise NotImplementedError

    @staticmethod
    def get_value(output: Mapping, path: str, exclude: List = None) -> Any:
        """Return the value contained into a Mapping for a defined path."""
        return extract_values_from_output(output, path, exclude)

    def evaluate(self, reference_value: Any, value_to_compare: Any) -> Tuple[Dict, bool]:
        """Return the result of the evaluation and a boolean True if it passes it or False otherwise.

        This method is the one that each CheckType has to implement.

        Args:
            reference_value: Can be any structured data or just a simple value.
            value_to_compare: Similar value as above to perform comparison.

        Returns:
            tuple: Dictionary representing check result, bool indicating if differences are found.
        """
        raise NotImplementedError


class ExactMatchType(CheckType):
    """Exact Match class docstring."""

    def evaluate(self, reference_value: Any, value_to_compare: Any) -> Tuple[Dict, bool]:
        """Returns the difference between values and the boolean."""
        diff = diff_generator(reference_value, value_to_compare)
        return diff, not diff


class ToleranceType(CheckType):
    """Tolerance class docstring."""

    def __init__(self, *args):
        """Tolerance init method."""
        try:
            tolerance = args[1]
        except IndexError as error:
            raise f"Tolerance parameter must be defined as float at index 1. You have: {args}" from error

        self.tolerance_factor = float(tolerance) / 100
        super().__init__()

    def evaluate(self, reference_value: Mapping, value_to_compare: Mapping) -> Tuple[Dict, bool]:
        """Returns the difference between values and the boolean. Overwrites method in base class."""
        diff = diff_generator(reference_value, value_to_compare)
        self._remove_within_tolerance(diff)
        return diff, not diff

    def _remove_within_tolerance(self, diff: Dict) -> None:
        """Recursively look into diff and apply tolerance check, remove reported difference when within tolerance."""
        for key, value in list(diff.items()):  # casting list makes copy, so we don't modify object being iterated.
            if isinstance(value, dict):
                if "new_value" in value.keys() and "old_value" in value.keys() and self._within_tolerance(**value):
                    diff.pop(key)
                else:
                    self._remove_within_tolerance(diff[key])
                if not value:
                    diff.pop(key)

    def _within_tolerance(self, *, old_value: float, new_value: float) -> bool:
        """Return True if new value is within the tolerance range of the previous value."""
        max_diff = old_value * self.tolerance_factor
        return (old_value - max_diff) < new_value < (old_value + max_diff)


class ParameterMatchType(CheckType):
    """Parameter Match class implementation."""

    def evaluate(self, reference_value: Mapping, value_to_compare: Mapping) -> Tuple[Dict, bool]:
        """Parameter Match evaluator implementation."""
        try:
            parameter = value_to_compare[1]
        except IndexError as error:
            raise f"Evaluating parameter must be defined as dict at index 1. You have: {value_to_compare}" from error
        diff = parameter_evaluator(reference_value, parameter)
        return diff, not diff


# TODO: compare is no longer the entry point, we should use the libary as:
#   netcompare_check = CheckType.init(check_type_info, options)
#   pre_result = netcompare_check.get_value(pre_obj, path)
#   post_result = netcompare_check.get_value(post_obj, path)
#   netcompare_check.evaluate(pre_result, post_result)
#
# def compare(
#     pre_obj: Mapping, post_obj: Mapping, path: Mapping, type_info: Iterable, options: Mapping
# ) -> Tuple[Mapping, bool]:
#     """Entry point function.

#     Returns a diff object and the boolean of the comparison.
#     """

#     type_info = type_info.lower()

#     try:
#         type_obj = CheckType.init(type_info, options)
#     except Exception:
#         # We will be here if we can't infer the type_obj
#         raise

#     return type_obj.evaluate(pre_obj, post_obj, path)
