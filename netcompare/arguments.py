"""Classes for argument validation."""

# pylint: disable=too-few-public-methods


class CheckArguments:
    """Class to validate arguments."""

    @staticmethod
    def validate(**kwargs):
        """Method to validate arguments."""
        raise NotImplementedError


class CheckArgumentsExactMatch(CheckArguments):
    """Class to validate arguments."""

    @staticmethod
    def validate(**kwargs):
        """Method to validate arguments."""
        # reference_data = getattr(kwargs, "reference_data")


class CheckArgumentsToleranceMatch(CheckArguments):
    """Class to validate arguments."""

    @staticmethod
    def validate(**kwargs):
        """Method to validate arguments."""
        # reference_data = getattr(kwargs, "reference_data")
        tolerance = getattr(kwargs, "tolerance")
        if not tolerance:
            raise ValueError("Tolerance argument is mandatory for Tolerance Check Type.")
        if not isinstance(int, tolerance):
            raise ValueError(f"Tolerance argument must be an integer, and it's {type(tolerance)}.")


class CheckArgumentsParameterMatch(CheckArguments):
    """Class to validate arguments."""

    @staticmethod
    def validate(**kwargs):
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        params = getattr(kwargs, "params")
        if not params:
            raise ValueError("Params argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(dict, params):
            raise ValueError(f"Params argument must be a dict, and it's {type(params)}.")

        mode = getattr(kwargs, "mode")
        if not mode:
            raise ValueError("Mode argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(str, mode):
            raise ValueError(f"Mode argument must be a string, and it's {type(mode)}.")
        if mode not in mode_options:
            raise ValueError(f"Mode argument should be {mode_options}, and it's {mode}")


class CheckArgumentsRegexMatch(CheckArguments):
    """Class to validate arguments."""

    @staticmethod
    def validate(**kwargs):
        """Method to validate arguments."""
        mode_options = ["match", "no-match"]
        regex = getattr(kwargs, "regex")
        if not regex:
            raise ValueError("Params argument is mandatory for Regex Match Check Type.")
        if not isinstance(str, regex):
            raise ValueError(f"Params argument must be a string, and it's {type(regex)}.")

        mode = getattr(kwargs, "mode")
        if not mode:
            raise ValueError("Mode argument is mandatory for Regex Match Check Type.")
        if not isinstance(str, mode):
            raise ValueError(f"Mode argument must be a string, and it's {type(mode)}.")
        if mode not in mode_options:
            raise ValueError(f"Mode argument should be {mode_options}, and it's {mode}")
