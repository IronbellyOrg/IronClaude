"""Deterministic pins on the plan-route producer contract (remediation source -> sc:workflow).

The end-to-end contract (a generated TASK-WF tasklist exposes the intended tasks to
``/sc:implement``) needs an LLM run and is covered by the ``workflow_vs_task_builder``
eval, not here. These tests pin the part that is checkable offline: the source templates
the handoff refs tell the model to write must themselves satisfy the ``sc:workflow``
list-syntax gate, must re-include review feedback, and each ref must point the workflow
at the file it actually prepares. Reads SOURCE files, not the ``.claude/`` mirror.
"""

from __future__ import annotations

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3] / "src/superclaude/skills"
_GATE = (_ROOT / "sc-workflow-protocol/refs/quality-gates.md").read_text()
_REFLECT = (_ROOT / "sc-reflect-protocol/refs/remediation-handoff.md").read_text()
_TROUBLE = (_ROOT / "sc-troubleshoot-protocol/refs/remediation-handoff.md").read_text()
_AUGGIE = (_ROOT / "sc-auggie-review-protocol/refs/remediation-handoff.md").read_text()
_DIAG = (_ROOT / "sc-troubleshoot-protocol/refs/diagnosability-audit.md").read_text()

# Mirrors quality-gates.md: no checkbox (`- [ ]`, `- [x]`, `* [ ]`) or numbered (`1.`, `1)`) line.
_LIST_LINE = re.compile(r"^\s*(?:\d+[.)]\s|[-*]\s\[[ xX]\])")
_FENCE = re.compile(r"```text\n(.*?)```", re.DOTALL)


def _template(ref: str) -> str:
    blocks = [b for b in _FENCE.findall(ref) if "# Remediation:" in b]
    assert len(blocks) == 1, "expected exactly one remediation source template"
    return blocks[0]


def test_gate_still_rejects_list_lines():
    # If the workflow gate stops rejecting list syntax, the flatten rule is obsolete: revisit.
    assert "no checkbox" in _GATE and "numbered" in _GATE


def test_source_templates_have_no_gate_rejected_lines():
    for name, ref in (("reflect", _REFLECT), ("troubleshoot", _TROUBLE)):
        bad = [ln for ln in _template(ref).splitlines() if _LIST_LINE.match(ln)]
        assert not bad, (
            f"{name} source template has list lines the workflow gate rejects: {bad}"
        )


def test_source_templates_reinclude_review_feedback():
    for name, ref in (("reflect", _REFLECT), ("troubleshoot", _TROUBLE)):
        tpl = _template(ref)
        assert "## Review Feedback" in tpl, name
        assert tpl.index("## Review Feedback") < tpl.index("## References"), name
        assert "remediation-review-notes.md" in ref, name
        # Appending to the file Phase A rewrites from scratch would lose the feedback.
        assert not re.search(r"append[^.\n]{0,60}to `remediation-source\.md`", ref), (
            name
        )


def test_auggie_invokes_workflow_on_the_prepared_source():
    assert (
        "`<output_dir>/remediation-workflow-source.md` (not on the bare spec)"
        in _AUGGIE
    )
    assert "on `<output_dir>/remediation-spec.md` with `--depth" not in _AUGGIE
    assert "never delete a line" in _AUGGIE
    assert "remediation-review-notes.md" in _AUGGIE


def test_flattening_never_deletes_lines():
    for name, text in (
        ("reflect", _REFLECT),
        ("troubleshoot", _TROUBLE),
        ("diag", _DIAG),
    ):
        assert "never delete a line" in text, name
    assert "Strip checkbox" not in _DIAG
