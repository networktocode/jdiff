"""Utility code for running tests."""

import json
import os


dirname = os.path.dirname(os.path.abspath(__file__))


def load_json_file(folder, filename):
    """Load mock data from json file."""
    filepath = os.path.join(dirname, "mock", folder, filename)
    with open(filepath, "r", encoding="utf-8") as filehandle:
        return json.load(filehandle)


def load_mocks(folder):
    """Load data from mock files."""
    pre = load_json_file(folder, "pre.json")
    post = load_json_file(folder, "post.json")
    results = load_json_file(folder, "results.json")
    return pre, post, results
