"""Launcher for the `ic` bash script (model-alias claude wrapper).

Registered as a console script in pyproject.toml so `pipx install superclaude`
puts `ic` on the user's PATH alongside `superclaude`.
"""

import os
import sys
from importlib.resources import as_file, files


def main() -> None:
    script_ref = files("superclaude.scripts").joinpath("ic")
    with as_file(script_ref) as script_path:
        os.execvp("bash", ["bash", str(script_path), *sys.argv[1:]])
