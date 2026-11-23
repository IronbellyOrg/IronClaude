"""Preserve specific issue-501 captures without exempting other evidence."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ".dev/tasks/archive/TASK-WF-planTheFixForIss-20261123-180531"
DONE = ".dev/tasks/done/TASK-WF-planTheFixForIss-20261123-185337"
DIAGNOSIS = (
    ".dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314"
)
CAPTURES = {
    "trailing-whitespace": [
        f"{DONE}/artifacts/{name}"
        for name in (
            "plan.diff",
            "task-1.diff",
            "task-2.diff",
            "task-3.diff",
            "task-4.diff",
            "lens-template.txt",
            "regression-before.txt",
        )
    ],
    "end-of-file-fixer": [
        f"{ARCHIVE}/source.md",
        f"{DONE}/artifacts/repaired-cli/manifest.json",
        f"{DIAGNOSIS}/stub-run/manifest.json",
    ],
    "yamllint": [
        f"{ARCHIVE}/artifacts/reflect-pre-20261123181244/artifacts/input-snapshot.yaml",
        f"{ARCHIVE}/artifacts/reflect-pre-20261123181244/return-contract.yaml",
        f"{DONE}/artifacts/repaired-cli/return-contract.yaml",
        f"{DIAGNOSIS}/stub-run/return-contract.yaml",
    ],
}
CASES = [(hook, path) for hook, paths in CAPTURES.items() for path in paths]


@pytest.fixture(scope="module")
def hooks():
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
    # The additional hardcoded-secret hook shares check-yaml's ID but has a name.
    return {
        hook.get("name", hook["id"]): hook
        for repo in config["repos"]
        for hook in repo["hooks"]
    }


def excluded(hook, path):
    return bool(re.search(hook.get("exclude", r"(?!)"), path))


@pytest.mark.parametrize(("hook", "path"), CASES)
def test_specific_capture_excluded(hooks, hook, path):
    assert (ROOT / path).is_file()
    assert excluded(hooks[hook], path)


@pytest.mark.parametrize(("hook", "path"), CASES)
def test_capture_exception_is_exact_and_issue_specific(hooks, hook, path):
    for other in (
        path.replace("20261123", "20261124"),
        path + ".copy",
        "other/" + path,
        str(Path(path).parent / ("other-" + Path(path).name)),
    ):
        # Existing trailing-whitespace policy already excludes every .md file.
        if hook == "trailing-whitespace" and other.endswith(".md"):
            continue
        assert not excluded(hooks[hook], other), other


@pytest.mark.parametrize("hook", list(CAPTURES))
@pytest.mark.parametrize(
    "path",
    [
        "src/example.py",
        "config/example.yaml",
        ".pre-commit-config.yaml",
        ".dev/other/manifest.json",
        ".dev/tasks/done/TASK-WF-other-20261123-185337/artifacts/result.txt",
        ".dev/troubleshoot/other-issue/result.yaml",
        f"{DONE}/artifacts/new-capture.txt",
    ],
)
def test_ordinary_and_other_evidence_files_still_checked(hooks, hook, path):
    assert not excluded(hooks[hook], path)


@pytest.mark.parametrize(
    "hook", ["trailing-whitespace", "end-of-file-fixer", "mixed-line-ending"]
)
def test_existing_fixture_exclusions_preserved(hooks, hook):
    assert excluded(hooks[hook], "tests/troubleshoot/fixtures/output.txt")


def test_existing_markdown_whitespace_policy_preserved(hooks):
    assert excluded(hooks["trailing-whitespace"], "docs/example.md")


@pytest.mark.parametrize(
    "hook",
    [
        "detect-secrets",
        "detect-private-key",
        "Check for hardcoded secrets",
        "check-yaml",
        "check-json",
        "check-merge-conflict",
        "check-added-large-files",
        "check-case-conflict",
        "mixed-line-ending",
    ],
)
def test_evidence_not_excluded_from_safety_and_syntax_checks(hooks, hook):
    for _, path in CASES:
        assert not excluded(hooks[hook], path), path
