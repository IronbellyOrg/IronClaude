"""The review-loop rules file carries the findings-block, fix-map and panel text exactly once (PN1, C4.3 and section E)."""

from __future__ import annotations

from pathlib import Path

RULES = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
)
TEXT = RULES.read_text(encoding="utf-8")

INS_A = '- **Findings block**: end the report with the findings block described under "Findings block" below, one line per finding, blocking or not.'
INS_B = '- **Findings block**: end the report with the findings block described under "Findings block" below: one line per finding you report and one prior line per prior blocking finding.'
INS_C = (
    '- **Fix map**: end your output with the fix map described under "Fix map" below.'
)
HEAD_D = "### Findings block"
HEAD_FIX = "### Fix map"
HEAD_E = "### Review panel"
E_FIRST = "Run each review with the reviewers that `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` prints"


def lines():
    return TEXT.splitlines()


def test_each_insertion_is_present_exactly_once():
    for needle in (INS_A, INS_B, INS_C, HEAD_D, HEAD_FIX, HEAD_E):
        assert TEXT.count(needle) == 1, needle
    assert TEXT.count(E_FIRST) == 1


def test_insertions_a_b_c_follow_their_brief_lines():
    ls = lines()
    for prefix, ins in (
        ('- First-review brief: "', INS_A),
        ('- Re-review brief: "', INS_B),
        ('- Revise brief: "', INS_C),
    ):
        i = next(n for n, line in enumerate(ls) if line.startswith(prefix))
        assert ls[i + 1] == ins, prefix


def test_d_then_fix_map_then_e_come_before_never():
    ls = lines()
    never = ls.index("## Never")
    d = ls.index(HEAD_D)
    fix = ls.index(HEAD_FIX)
    e = ls.index(HEAD_E)
    assert d < fix < e < never
    assert ls[d - 1] == "" and ls[never - 1] == ""
    assert ls[e - 1] == ""
    assert "only that script changes a finding's status" in "\n".join(ls[e:never])
    assert (
        "If the `superclaude` command is not installed, run one reviewer and say so in the loop summary."
        in TEXT
    )
    fix_para = ls[fix + 2]
    assert fix_para.startswith("The reviser ends its output with `## Fix map`")
    assert ls[fix + 3] == ""


def test_d_text_is_the_contract_text():
    for token in (
        "The last section of every review report is `## Findings block`: one fenced code block whose info string is `findings-v1`",
        '{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "<text copied exactly from the candidate>", "anchor2": "<optional second exact quote>", "refs": ["AC-0.4"], "claim": "<one sentence naming the wrong outcome>"}',
        '{"prior": "L3", "status": "resolved"}',
        "The block restates the findings discussed above it and adds none. The verdict line stays the reviewer's verdict.",
        '{"id": "L3", "action": "applied", "reason": "<one sentence>"}',
    ):
        assert token in TEXT, token


def test_older_pins_still_hold_and_no_source_path():
    for token in (
        "FIRST-REVIEW prompt",
        "RE-REVIEW prompt",
        "REVISE prompt",
        "## When to use which prompt",
        "## Values to fill",
        "## Never",
        "| ROLE | FILE VALUE | MEANING |",
        "Step 1, the evidence block",
        "`diff -w BASELINE CANDIDATE`",
        "you swapped roles: redo Step 1",
    ):
        assert token in TEXT, token
    for label in ("First-review brief", "Re-review brief", "Revise brief"):
        assert f'- {label}: "' in TEXT
    assert "src/superclaude" not in TEXT
