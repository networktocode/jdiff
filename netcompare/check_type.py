"""CheckType Implementation."""
from typing import Mapping, Iterable, Tuple
from .evaluator import diff_generator


class CheckType:
    """Check Type Class."""

    def __init__(self, *args):
        """Check Type init method."""
        pass

    @staticmethod
    def init(*args):
        """Factory pattern to get the appropiate CheckType implementation."""
        check_type = args[0]
        if check_type == "exact_match":
            return ExactMatchType(*args)
        elif check_type == "tolerance":
            return ToleranceType(*args)
        else:
            raise NotImplementedError

    def evaluate(self, pre_value: Mapping, post_value: Mapping, path: Mapping) -> Tuple[Mapping, bool]:
        """Return a diff of the comparison and a boolean True if it passes or False otherwise."""
        self.diff = diff_generator(pre_value, post_value, path)
        # self.diff may get modified by a child class when self.check_logic is called.
        logic_check = self.check_logic()
        return (self.diff, logic_check)

    def check_logic(self) -> bool:
        """docstring placeholder."""
        raise NotImplementedError


class ExactMatchType(CheckType):
    """Exact Match class docstring."""

    def check_logic(self) -> bool:
        """Return True if diff is empty indicating an exact match."""
        return not self.diff


class ToleranceType(CheckType):
    """Tolerance class docstring."""

    def __init__(self, *args):
        """Tollerance init method."""
        self.tolerance_factor = float(args[1]) / 100
        super().__init__()

    def check_logic(self) -> bool:
        """Return True if the changed values are within tolerance."""
        self.diff = self._get_outliers()
        return not self.diff

    def _get_outliers(self) -> Mapping:
        """Return a mapping of values outside the tolerance threshold."""
        result = {
            key: {sub_key: values for sub_key, values in obj.items() if not self._within_tolerance(**values)}
            for key, obj in self.diff.items()
        }
        return {key: obj for key, obj in result.items() if obj}

    def _within_tolerance(self, *, old_value: float, new_value: float) -> bool:
        """Return True if new value is within the tolerance range of the previous value."""
        max_diff = old_value * self.tolerance_factor
        return (old_value - max_diff) < new_value < (old_value + max_diff)


def compare(
    pre_obj: Mapping, post_obj: Mapping, path: Mapping, type_info: Iterable, options: Mapping
) -> Tuple[Mapping, bool]:
    """Entry point function.

    Returns a diff object and the boolean of the comparison.
    """

    type_info = type_info.lower()

    try:
        type_obj = CheckType.init(type_info, options)
    except Exception:
        # We will be here if we can't infer the type_obj
        raise

    return type_obj.evaluate(pre_obj, post_obj, path)
