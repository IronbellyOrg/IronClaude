"""Run selected tier tests with origin/master's shim, without replacing working files.

Usage: uv run --extra dev python .dev/issues/392/check-baseline.py -k <expression>
"""

import pathlib
import subprocess
import sys
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[3]
SOURCE = ROOT / "src/superclaude/skills/ccsession-tag"
SHIM = "local-gateway-alias-proxy.py"


class Baseline:
    def __init__(self, folder):
        self.folder = folder

    def pytest_collection_modifyitems(self, items):
        for item in items:
            if hasattr(item.module, "SKILL_DIR"):
                item.module.SKILL_DIR = self.folder


with tempfile.TemporaryDirectory(prefix="ccsession-392-baseline-") as temp:
    folder = pathlib.Path(temp)
    for path in SOURCE.iterdir():
        if path.name != SHIM:
            (folder / path.name).symlink_to(path)
    (folder / SHIM).write_bytes(
        subprocess.check_output(
            [
                "git",
                "show",
                f"origin/master:src/superclaude/skills/ccsession-tag/{SHIM}",
            ],
            cwd=ROOT,
        )
    )
    print(
        "BASELINE: origin/master",
        subprocess.check_output(
            ["git", "rev-parse", "origin/master"], cwd=ROOT, text=True
        ).strip(),
    )
    code = pytest.main(
        [str(ROOT / "tests/unit/test_ccsession_tiers.py"), "-q", *sys.argv[1:]],
        plugins=[Baseline(folder)],
    )
    raise SystemExit(code)
