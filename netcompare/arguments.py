class CheckArguments:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class CheckArgumentsExactMatch(CheckArguments):
    def __init__(self, *args, **kwargs):
        self.reference_data = getattr(kwargs, "raw_data")


class CheckArgumentsToleranceMatch(CheckArguments):
    def __init__(self, *args, **kwargs):
        self.reference_data = getattr(kwargs, "raw_data")
        self.tolerance = getattr(kwargs, "tolerance")
        if not self.tolerance:
            raise ValueError("Tolerance argument is mandatory for Tolerance Check Type.")
        if not isinstance(int, self.tolerance):
            raise ValueError(f"Tolerance argument must be an integer, and it's {type(self.tolerance)}.")


class CheckArgumentsParameterMatch(CheckArguments):
    MODE_OPTIONS = ["match", "no-match"]

    def __init__(self, *args, **kwargs):
        self.params = getattr(kwargs, "params")
        if not self.params:
            raise ValueError("Params argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(dict, self.params):
            raise ValueError(f"Params argument must be a dict, and it's {type(self.params)}.")

        self.mode = getattr(kwargs, "mode")
        if not self.mode:
            raise ValueError("Mode argument is mandatory for ParameterMatch Check Type.")
        if not isinstance(str, self.mode):
            raise ValueError(f"Mode argument must be a string, and it's {type(self.mode)}.")
        if self.mode not in self.MODE_OPTIONS:
            raise ValueError(f"Mode argument should be {self.MODE_OPTIONS}, and it's {self.mode}")


class CheckArgumentsRegexMatch(CheckArguments):
    MODE_OPTIONS = ["match", "no-match"]

    def __init__(self, *args, **kwargs):
        self.params = getattr(kwargs, "params")
        if not self.params:
            raise ValueError("Params argument is mandatory for Regex Match Check Type.")
        if not isinstance(str, self.params):
            raise ValueError(f"Params argument must be a string, and it's {type(self.params)}.")

        self.mode = getattr(kwargs, "mode")
        if not self.mode:
            raise ValueError("Mode argument is mandatory for Regex Match Check Type.")
        if not isinstance(str, self.mode):
            raise ValueError(f"Mode argument must be a string, and it's {type(self.mode)}.")
        if self.mode not in self.MODE_OPTIONS:
            raise ValueError(f"Mode argument should be {self.MODE_OPTIONS}, and it's {self.mode}")


class CheckArgumentsOptionsMatch(CheckArguments):
    MODE_OPTIONS = ["is-in", "???"]

    def __init__(self, *args, **kwargs):
        self.params = getattr(kwargs, "params")
        if not self.params:
            raise ValueError("Params argument is mandatory for Regex Match Check Type.")
        if not isinstance(list, self.params):
            raise ValueError(f"Params argument must be a list, and it's {type(self.params)}.")

        self.mode = getattr(kwargs, "mode")
        if not self.mode:
            raise ValueError("Mode argument is mandatory for Regex Match Check Type.")
        if not isinstance(str, self.mode):
            raise ValueError(f"Mode argument must be a string, and it's {type(self.mode)}.")
        if self.mode not in self.MODE_OPTIONS:
            raise ValueError(f"Mode argument should be {self.MODE_OPTIONS}, and it's {self.mode}")
