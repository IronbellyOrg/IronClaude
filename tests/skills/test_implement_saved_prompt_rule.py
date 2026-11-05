"""Pin the saved-reviewer-prompt rules of the sc-implement-protocol refs.

Rule A: the comparison of a saved prompt with the reviewer template is stated once,
        in "## FINAL derived test", and a difference only in blank lines or trailing
        whitespace is a note.
Rule B: a defective saved prompt is recovered by a template-exact re-review and an
        unchanged move to superseded-prompts/, started from step 6 of the archive gate.
The plugin copy of each ref must stay byte-identical to the source copy.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_SRC = _REPO / "src/superclaude/skills/sc-implement-protocol/refs"
_PLUGIN = _REPO / "plugins/superclaude/skills/sc-implement-protocol/refs"
_REFS = ("qa.md", "ledger.md", "managed-workspace.md")


def _read(root: Path, name: str) -> str:
    return (root / name).read_text(encoding="utf-8")


@pytest.fixture(params=[_SRC, _PLUGIN], ids=["src", "plugin"])
def root(request) -> Path:
    return request.param


def test_old_when_they_differ_wording_is_gone(root):
    assert "when they differ" not in _read(root, "qa.md")


@pytest.mark.parametrize(
    "phrase",
    [
        "differs only in blank lines or trailing whitespace",
        "after the start-sha header",
        "### Defective saved prompt (recovery)",
        "next unused `j` of the same `k`",
        "appends the task's `complete` line again",
        "moved unchanged",
        "In a legacy run",
        "is not a confirmed blocker",
        "is an unfinished re-review",
        "after the `FINAL:` line that flagged the prompt",
    ],
)
def test_qa_has_rule_wording(root, phrase):
    assert phrase in _read(root, "qa.md"), phrase


def test_ledger_has_re_review_complete_line_section(root):
    assert "## Re-review complete line" in _read(root, "ledger.md")


def test_step_six_of_the_archive_gate_starts_the_recovery(root):
    lines = [
        line
        for line in _read(root, "managed-workspace.md").splitlines()
        if line.startswith("6. `pass` → run the helper")
    ]
    assert len(lines) == 1
    assert "every `issues` item of the FINAL concerns a saved prompt" in lines[0]
    assert "`issues` → STOP `E-ARCHIVE-BLOCKED`" in lines[0]


def test_managed_workspace_names_superseded_prompts(root):
    assert "superseded-prompts/" in _read(root, "managed-workspace.md")


@pytest.mark.parametrize("name", _REFS)
def test_plugin_copy_is_byte_identical_to_source(name):
    assert (_SRC / name).read_bytes() == (_PLUGIN / name).read_bytes(), name
