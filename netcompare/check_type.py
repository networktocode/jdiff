"""CheckType Implementation."""
from typing import Mapping, Tuple, Union, List
from .evaluator import diff_generator, parameter_evaluator
from .runner import extract_values_from_output


class CheckType:
    """Check Type Class."""

    def __init__(self, *args):
        """Check Type init method."""

    @staticmethod
    def init(*args):
        """Factory pattern to get the appropiate CheckType implementation."""
        check_type = args[0]
        if check_type == "exact_match":
            return ExactMatchType(*args)
        if check_type == "tolerance":
            return ToleranceType(*args)
        if check_type == "parameter_match":
            return ParameterMatchType(*args)

        raise NotImplementedError

    @staticmethod
    def extract_value_from_json_path(
        value: Mapping, path: Mapping, exclude: List = None
    ) -> Union[Mapping, List, int, str, bool]:
        """Return the value contained into a Mapping for a defined path."""
        return extract_values_from_output(value, path, exclude)

    # TODO: Refine this typing
    def evaluate(self, reference_value: Mapping, value_to_compare: Mapping) -> Tuple[Mapping, bool]:
        """Return the result of the evaluation and a boolean True if it passes it or False otherwise.

        This method is the one that each CheckType has to implement.
        """
        raise NotImplementedError


class ExactMatchType(CheckType):
    """Exact Match class docstring."""

    def evaluate(self, reference_value: Mapping, value_to_compare: Mapping) -> Tuple[Mapping, bool]:
        """Returns the difference between values and the boolean."""
        diff = diff_generator(reference_value, value_to_compare)
        return diff, not diff


class ToleranceType(CheckType):
    """Tolerance class docstring."""

    def __init__(self, *args):
        """Tollerance init method."""
        self.tolerance_factor = float(args[1]) / 100
        super().__init__()

    def evaluate(self, reference_value: Mapping, value_to_compare: Mapping) -> Tuple[Mapping, bool]:
        """Returns the difference between values and the boolean."""
        diff = diff_generator(reference_value, value_to_compare)
        diff = self._get_outliers(diff)
        return diff, not diff

    def _get_outliers(self, diff: Mapping) -> Mapping:
        """Return a mapping of values outside the tolerance threshold."""
        result = {
            key: {sub_key: values for sub_key, values in obj.items() if not self._within_tolerance(**values)}
            for key, obj in diff.items()
        }
        return {key: obj for key, obj in result.items() if obj}

    def _within_tolerance(self, *, old_value: float, new_value: float) -> bool:
        """Return True if new value is within the tolerance range of the previous value."""
        max_diff = old_value * self.tolerance_factor
        return (old_value - max_diff) < new_value < (old_value + max_diff)


class ParameterMatchType(CheckType):
    """Parameter Match class implementation."""

    def evaluate(self, reference_value: Mapping, value_to_compare: Mapping) -> Tuple[Mapping, bool]:
        """Parameter Match evaluator implementation."""
        # TO DO: remove arg index. from tollerance too
        diff = parameter_evaluator(reference_value, value_to_compare[1])
        return diff, bool(diff)


# TODO: compare is no longer the entry point, we should use the libary as:
#   netcompare_check = CheckType.init(check_type_info, options)
#   pre_result = netcompare_check.extract_value_from_json_path(pre_obj, path)
#   post_result = netcompare_check.extract_value_from_json_path(post_obj, path)
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
