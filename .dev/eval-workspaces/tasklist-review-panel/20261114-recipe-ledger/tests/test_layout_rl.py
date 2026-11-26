"""K7: the code folders of RL exist and `.gitignore` matches none of them; no folder is named lib/ (TESTING 4)."""

import subprocess
from pathlib import Path

import pytest

RL = Path(__file__).resolve().parents[1]
REPO = RL.parents[3]
CODE_FOLDERS = ("bin", "tests", "scaffold", "rl", "analysis")


def code_files(folder):
    return [
        str(p.relative_to(REPO))
        for p in sorted((RL / folder).rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    ]


@pytest.mark.parametrize("folder", CODE_FOLDERS)
def test_no_ignored_folder_names(folder):
    assert (RL / folder).is_dir()
    paths = [str((RL / folder).relative_to(REPO))] + code_files(folder)
    r = subprocess.run(
        ["git", "check-ignore", "--stdin"],
        input="\n".join(paths),
        cwd=REPO,
        capture_output=True,
        text=True,
    )  # without -v: -v also reports a path that only matches a negated (!) pattern, and exits 0 for it
    assert r.returncode == 1, (
        f"ignored by .gitignore: {r.stdout}"
    )  # 1 = none of the paths is ignored


def test_no_lib_folder():
    assert not [p for p in RL.rglob("*") if p.is_dir() and p.name in {"lib", "lib64"}]
