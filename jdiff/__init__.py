"""Initialization file for library."""

from importlib import metadata

from .check_types import CheckType
from .extract_data import extract_data_from_json

__version__ = metadata.version(__name__)
__all__ = ["CheckType", "extract_data_from_json"]
