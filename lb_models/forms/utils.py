"""Forms utilities."""


def add_blank_choice(choices):
    """Add a blank choice to the beginning of a choices list."""
    return ((None, "---------"),) + tuple(choices)
