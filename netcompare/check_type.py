"""CheckType Implementation."""
import re
from typing import Mapping, Tuple, List, Dict, Any, Union
import jmespath

from .utils.jmspath_parsers import jmspath_value_parser, jmspath_refkey_parser
from .utils.filter_parsers import exclude_filter
from .utils.refkey import keys_cleaner, keys_values_zipper, associate_key_of_my_value
from .utils.flatten import flatten_list
from .evaluators import diff_generator, parameter_evaluator


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
        if exclude:
            exclude_filter(output, exclude)  # exclude unwanted elements

        if not path:
            return output  # return if path is not specified

        values = jmespath.search(jmspath_value_parser(path), output)

        if not any(isinstance(i, list) for i in values):  # check for multi-nested lists if not found return here
            return values

        for element in values:  # process elements to check is lists should be flatten
            for item in element:
                if isinstance(item, dict):  # raise if there is a dict, path must be more specific to extract data
                    raise TypeError(
                        f'Must be list of lists i.e. [["Idle", 75759616], ["Idle", 75759620]].' f"You have {values}'."
                    )
                if isinstance(item, list):
                    values = flatten_list(values)  # flatten list and rewrite values
                    break  # items are the same, need to check only first to see if this is a nested list

        paired_key_value = associate_key_of_my_value(jmspath_value_parser(path), values)

        if re.search(r"\$.*\$", path):  # normalize
            wanted_reference_keys = jmespath.search(jmspath_refkey_parser(path), output)
            list_of_reference_keys = keys_cleaner(wanted_reference_keys)
            return keys_values_zipper(list_of_reference_keys, paired_key_value)

        return values

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
        evaluation_result = diff_generator(reference_value, value_to_compare)
        return evaluation_result, not evaluation_result


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
        evaluation_result = self._get_outliers(diff)
        return evaluation_result, not evaluation_result

    def _get_outliers(self, diff: Mapping) -> Dict:
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

    def evaluate(self, reference_value: Mapping, value_to_compare: Mapping) -> Tuple[Dict, bool]:
        """Parameter Match evaluator implementation."""
        try:
            parameter = value_to_compare[1]
        except IndexError as error:
            raise f"Evaluating parameter must be defined as dict at index 1. You have: {value_to_compare}" from error
        evaluation_result = parameter_evaluator(reference_value, parameter)
        return evaluation_result, not evaluation_result


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
