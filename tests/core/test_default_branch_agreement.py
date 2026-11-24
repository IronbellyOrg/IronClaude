"""CLAUDE.md, the PR template, the L2 pre-push hook and the reflect default must name one base branch."""

import re
from pathlib import Path

from superclaude.cli.reflect.config import _DEFAULT_BASE_BRANCH

ROOT = Path(__file__).resolve().parents[2]


def _find(path: str, pattern: str) -> str:
    match = re.search(pattern, (ROOT / path).read_text(), re.M)
    assert match, f"{path}: no match for {pattern!r}"
    return match.group(1)


def test_base_branch_is_the_same_everywhere() -> None:
    claude_md = _find("CLAUDE.md", r"^gh pr create .*--base (\S+) ")
    template = _find(
        ".github/PULL_REQUEST_TEMPLATE.md", r"rebased onto `origin/([^`]+)`"
    )
    assert claude_md == template == _DEFAULT_BASE_BRANCH, (
        f"CLAUDE.md={claude_md} PR template={template} reflect={_DEFAULT_BASE_BRANCH}"
    )
    hook = _find(
        "src/superclaude/hooks/scripts/launch-level-pre-push.sh",
        r"^L2_PROTECTED=\((.*)\)$",
    )
    assert f"refs/heads/{_DEFAULT_BASE_BRANCH}" in hook.split(), hook
