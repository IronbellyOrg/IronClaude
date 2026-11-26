"""Pin how /sc:post-release resolves the default branch and checks the tag lineage (issue 826).

The skill must resolve the default branch live from the remote, compare the tag with the remote
ref (never a bare local branch that can be far behind), report an unverified check as unverified,
and name no branch. CI-safe, no network.
"""

import re
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parents[2] / "src" / "superclaude"
_SKILL = _SRC / "skills" / "sc-post-release-protocol" / "SKILL.md"
_COMMAND = _SRC / "commands" / "post-release.md"


def _lines() -> list[str]:
    return _SKILL.read_text(encoding="utf-8").splitlines()


def _line_starting(prefix: str) -> str:
    (line,) = [ln for ln in _lines() if ln.startswith(prefix)]
    return line


def _paragraph() -> str:
    return _line_starting("**Anchor the scan to the tagged commit.**")


def _guardrails() -> str:
    text = "\n".join(_lines())
    return text[text.index("## Guardrails") :]


@pytest.mark.parametrize(
    "required",
    [
        "git ls-remote --symref origin HEAD",
        "git fetch origin <default-branch> --tags",
        "git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>",
        "unverified",
        "git fetch origin '+refs/heads/*:refs/remotes/origin/*' --tags",
        "git branch -r --contains <tag>",
    ],
)
def test_paragraph_names_live_resolution_and_remote_check(required):
    assert required in _paragraph()


def test_old_local_branch_comparison_is_gone():
    text = _SKILL.read_text(encoding="utf-8")
    assert "git merge-base --is-ancestor <tag> <default-branch>" not in text


def test_paragraph_names_no_branch():
    # The word "mainline" is allowed; a literal branch name is not.
    assert re.search(r"\b(main|master|integration)\b", _paragraph()) is None


def test_output_and_exit_lines_say_resolved_with_source():
    output = _line_starting("**Output:** resolved tag")
    exit_criteria = _line_starting("**Exit criteria:** tag anchored")
    assert "default branch (resolved live, with its source)" in output
    assert "default branch resolved and its source recorded" in exit_criteria


def test_warn_line_still_ends_with_the_tag():
    (line,) = [ln for ln in _lines() if "then continue, anchored to the tag" in ln]
    assert line.rstrip().rstrip(".").endswith("then continue, anchored to the tag")


def test_guardrails_name_the_offline_fallback_and_ask_the_user():
    guardrails = _guardrails()
    assert "offline fallback" in guardrails
    assert "ask the user" in guardrails


def test_post_release_command_has_no_base_flag():
    # A static guard on a file the release work never edits: the command takes no new flag.
    assert "--base" not in _COMMAND.read_text(encoding="utf-8")
