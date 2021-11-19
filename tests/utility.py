"""Utitlity code for running tests."""

import json
import os


dirname = os.path.dirname(os.path.abspath(__file__))


def load_json_file(folder, filename):
    filepath = os.path.join(dirname, "mock", folder, filename)
    with open(filepath) as filehandle:
        return json.load(filehandle)
