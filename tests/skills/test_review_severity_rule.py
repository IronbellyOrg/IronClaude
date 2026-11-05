"""Static pins for the review severity rule and the 2-fix-cycle review cap.

Rule (``src/superclaude/output-styles/pragmatic.md``, bullets S1-S5): every
review finding is blocking or minor; minor findings are notes that never fail a
review, are never rechecked and never trigger a fix pass; a review loop runs at
most 2 fix cycles (3 reviews) and then escalates the open blocking findings to
the user. The edit tables ``fixtures/review_severity_cap_edits.yaml`` and
``fixtures/review_severity_sweep_edits.yaml`` are byte copies of the plan's
cap-edits.yaml and sweep-edits.yaml; every row must stay applied.

Enforcement type: STATIC - assertions over tracked primitive text.
"""

from __future__ import annotations

import functools
import re
import subprocess
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[2]
_FIXTURES = Path(__file__).resolve().parent / "fixtures"
STYLE = _REPO / "src/superclaude/output-styles/pragmatic.md"

_SCAN_TREES = ("src", "plugins", "commands", "agents", "skills")


def _flat(text: str) -> str:
    return " ".join(text.split())


@functools.lru_cache(maxsize=1)
def _tracked_text() -> dict[str, str]:
    """Every tracked text file under the scanned trees, read once."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "--", *_SCAN_TREES],
        cwd=_REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    texts: dict[str, str] = {}
    for rel in filter(None, out.split("\0")):
        try:
            texts[rel] = (_REPO / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
            continue
    return texts


def _files_under(*trees: str) -> dict[str, str]:
    prefixes = tuple(f"{t}/" for t in trees)
    return {p: t for p, t in _tracked_text().items() if p.startswith(prefixes)}


def _read(rel: str) -> str:
    cached = _tracked_text().get(rel)
    return cached if cached is not None else (_REPO / rel).read_text(encoding="utf-8")


# --- (b) canonical S1-S5, shared with the P1 pin ---------------------------

BINARY_VERDICT_BULLET = (
    "- Every review agent MUST produce a binary verdict: PASS or FAIL."
)
S_OPENINGS = (
    "- Grade every review finding as blocking or minor.",
    "- Minor findings never fail a review:",
    "- A review loop (review, fix, re-review) runs at most 2 fix cycles",
    "- A protocol that defines its own severity model,",
    "- On a CRITICAL / IMPORTANT / MINOR scale,",
)


@functools.lru_cache(maxsize=1)
def canonical_rule_bullets() -> tuple[str, str, str, str, str]:
    """Return S1-S5: the five bullets after the binary-verdict bullet of pragmatic.md.

    Each bullet is checked by its opening phrase. Used by this module and by the
    P1 pin in ``tests/skills/test_implement_severity_static.py``.
    """
    lines = STYLE.read_text(encoding="utf-8").splitlines()
    starts = [
        i for i, line in enumerate(lines) if line.startswith(BINARY_VERDICT_BULLET)
    ]
    assert len(starts) == 1, f"binary-verdict bullet found {len(starts)} times"
    bullets = tuple(lines[starts[0] + 1 : starts[0] + 6])
    assert len(bullets) == 5
    for n, (bullet, opening) in enumerate(zip(bullets, S_OPENINGS), 1):
        assert bullet.startswith(opening), (
            f"S{n} does not open with {opening!r}: {bullet!r}"
        )
    return bullets  # type: ignore[return-value]


def _rule_body(bullet: str) -> str:
    return _flat(bullet[2:] if bullet.startswith("- ") else bullet)


def test_b_canonical_bullets_follow_binary_verdict_bullet():
    bullets = canonical_rule_bullets()
    assert all(b.startswith("- ") for b in bullets)
    assert not any(re.search(r"\(S[1-5]\)", b) for b in bullets)
    assert not any("contains the canonical cap text" in b for b in bullets)


# --- (a) any-severity wording ----------------------------------------------

BANNED_SEVERITY_PHRASES = (
    "any issue of any severity",
    "issues of any severity",
    "gaps of any severity",
    "at any severity",
    "regardless of severity",
    "no severity level is exempt",
    "minor issues still pass",
    "must still be fixed",
    "still must be fixed",
    "must be perfect to pass",
    "ALL findings must be resolved",
    "CRITICAL, IMPORTANT, and MINOR issues",
)


def _phrase_hits(text: str, phrases) -> list[str]:
    low = text.lower()
    return [p for p in phrases if p.lower() in low]


def _scan_phrases(files: dict[str, str], phrases) -> list[str]:
    hits = []
    for path, text in sorted(files.items()):
        for n, line in enumerate(text.splitlines(), 1):
            for p in _phrase_hits(line, phrases):
                hits.append(f"{path}:{n}: {p!r}")
    return hits


@pytest.mark.parametrize(
    "scratch",
    [
        "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict",
        "Report issues of any severity.",
        "List gaps of any severity in the table.",
        "A finding at any severity blocks the gate.",
        "ALL findings regardless of severity must be resolved.",
        "No severity level is exempt from fixing.",
        "A 'minor issues still pass' allowance is PROHIBITED.",
        "Minor issues must still be fixed before PASS.",
        "Cosmetic gaps still must be fixed.",
        "Zero tolerance: The batch must be perfect to pass",
        "All findings must be resolved before the next phase.",
        "Send CRITICAL, IMPORTANT, and MINOR issues to gap-fill.",
    ],
)
def test_a_matcher_fires_on_any_severity_wording(scratch):
    assert _phrase_hits(scratch, BANNED_SEVERITY_PHRASES)


def test_a_matcher_ignores_the_new_rule_text():
    assert not _phrase_hits(
        "All blocking findings must be resolved; minor findings are recorded as notes.",
        BANNED_SEVERITY_PHRASES,
    )
    for bullet in canonical_rule_bullets():
        assert not _phrase_hits(bullet, BANNED_SEVERITY_PHRASES)


def test_a_no_any_severity_wording_in_tracked_primitives():
    hits = _scan_phrases(
        _files_under("src", "plugins", "commands", "agents"), BANNED_SEVERITY_PHRASES
    )
    assert not hits, "any-severity wording survives:\n" + "\n".join(hits)


# --- (c) S1-S3 / S5 copies in the ten-file set -----------------------------

S1_S3_FILES = (
    "src/superclaude/agents/rf-qa.md",
    "src/superclaude/agents/rf-qa-qualitative.md",
    "src/superclaude/templates/documents/agent_template_qa.md",
    "src/superclaude/templates/documents/skill_template.md",
    "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md",
    "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md",
    "src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md",
    "src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md",
    "src/superclaude/rules/prompts/documentation_expert_qa_prompt.md",
    "src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md",
)
S5_FILES = S1_S3_FILES[:6]


@pytest.mark.parametrize("rel", S1_S3_FILES)
def test_c_s1_s3_copied_verbatim(rel):
    flat = _flat(_read(rel))
    s1, s2, s3, _s4, s5 = canonical_rule_bullets()
    for n, bullet in ((1, s1), (2, s2), (3, s3)):
        assert _rule_body(bullet) in flat, f"S{n} missing from {rel}"
    if rel in S5_FILES:
        assert _rule_body(s5) in flat, f"S5 missing from {rel}"


@pytest.mark.parametrize("rel", S1_S3_FILES)
def test_c_no_inventory_labels_or_annotation(rel):
    text = _read(rel)
    assert not re.search(r"\(S[1-5]\)", text), rel
    assert "contains the canonical cap text" not in text, rel


# --- (d) canonical cap text and at-cap clause -------------------------------

CANONICAL_CAP_TEXT = "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"
AT_CAP_CLAUSES = (
    "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings",
    "HALT and escalate to the user with the open blocking findings",
)


@functools.lru_cache(maxsize=None)
def _rows(fixture: str) -> tuple[dict, ...]:
    data = yaml.safe_load((_FIXTURES / fixture).read_text(encoding="utf-8"))
    return tuple(data["rows"])


def test_d_canonical_cap_text_in_style():
    assert CANONICAL_CAP_TEXT in _flat(STYLE.read_text(encoding="utf-8"))
    assert CANONICAL_CAP_TEXT in canonical_rule_bullets()[2]


def test_d_at_cap_clause_present_where_cap_rows_add_it():
    expected: dict[str, set[str]] = {}
    for row in _rows("review_severity_cap_edits.yaml"):
        for clause in AT_CAP_CLAUSES:
            if clause in row["new"]:
                expected.setdefault(row["file"], set()).add(clause)
    assert expected, "no cap-edits row carries the at-cap clause"
    missing = [
        f"{rel}: {clause!r}"
        for rel, clauses in sorted(expected.items())
        for clause in sorted(clauses)
        if clause not in _read(rel)
    ]
    assert not missing, "at-cap clause missing:\n" + "\n".join(missing)


# --- (e) / (j) edit-table rows hold ----------------------------------------


def _failing_rows(fixture: str) -> list[str]:
    bad = []
    for row in _rows(fixture):
        text = _read(row["file"])
        if row["old"] in text or row["new"] not in text:
            bad.append(f"{row['id']} {row['file']}")
    return bad


def test_e_every_cap_edits_row_holds():
    rows = _rows("review_severity_cap_edits.yaml")
    assert len(rows) == 161
    bad = _failing_rows("review_severity_cap_edits.yaml")
    assert not bad, "cap-edits rows not applied:\n" + "\n".join(bad)


def test_j_every_sweep_edits_row_holds():
    rows = _rows("review_severity_sweep_edits.yaml")
    assert len(rows) == 139
    bad = _failing_rows("review_severity_sweep_edits.yaml")
    assert not bad, "sweep-edits rows not applied:\n" + "\n".join(bad)


def test_ej_fixtures_are_byte_copies_of_the_plan_tables():
    for fixture, source in (
        ("review_severity_cap_edits.yaml", "cap-edits.yaml"),
        ("review_severity_sweep_edits.yaml", "sweep-edits.yaml"),
    ):
        plan_copy = _REPO / ".dev/review-severity-rule" / source
        if not plan_copy.exists():
            pytest.skip(f"{plan_copy} not present in this checkout")
        assert (_FIXTURES / fixture).read_bytes() == plan_copy.read_bytes(), fixture


# --- (f) old cap numbers do not come back -----------------------------------

CAP_REGRESSION = re.compile(
    r"(max(imum)?|after|up to) [3-9] (fix|fix-verify|correction) (cycles?|loops?|attempts?)"
    r"|(failing|failed) [3-9] fix cycles|max-[3-9]-cycles?|\b[3-9]-(fix-)?cycles?\b"
    r"|fix cycles?: [3-9]\b|after [3-9] failed cycles",
    re.IGNORECASE,
)
# (path, text the line must contain): sc-cli-eval's manifest fix loop is not a review loop.
CAP_REGRESSION_ALLOW = {
    (
        "src/superclaude/skills/sc-cli-eval-protocol/SKILL.md",
        "Max 3 fix loops, then report blocked",
    ),
    (
        "src/superclaude/skills/sc-cli-eval-protocol/refs/create-pipeline.md",
        "(max 3 fix loops), then report blocked",
    ),
}


@pytest.mark.parametrize(
    "scratch",
    [
        "Max 3 fix cycles",
        "phase-gate QA failing 3 fix cycles",
        "after 3 failed cycles",
        "max-3-cycles",
    ],
)
def test_f_regression_matcher_fires(scratch):
    assert CAP_REGRESSION.search(scratch)


def test_f_no_old_cap_numbers_outside_implement_protocol():
    files = {
        p: t
        for p, t in _files_under("src", "plugins").items()
        if "sc-implement-protocol" not in p
    }
    hits, used = [], set()
    for path, text in sorted(files.items()):
        for n, line in enumerate(text.splitlines(), 1):
            if not CAP_REGRESSION.search(line):
                continue
            allowed = [a for a in CAP_REGRESSION_ALLOW if a[0] == path and a[1] in line]
            if allowed:
                used.update(allowed)
                continue
            hits.append(f"{path}:{n}: {line.strip()[:160]}")
    assert not hits, "old review-loop cap survives:\n" + "\n".join(hits)
    assert used == CAP_REGRESSION_ALLOW, (
        f"stale allowlist entries: {CAP_REGRESSION_ALLOW - used}"
    )


# --- (g) shared verdict suffixes kept ---------------------------------------

NO_CONDITIONAL_PASS = "Only PASS or FAIL — no conditional pass."


@pytest.mark.parametrize(
    "rel",
    [
        "src/superclaude/templates/documents/skill_template.md",
        "src/superclaude/skills/prd/refs/agent-prompts.md",
        "src/superclaude/skills/tdd/refs/agent-prompts.md",
        "src/superclaude/skills/tech-reference/SKILL.md",
        "src/superclaude/skills/tech-research/SKILL.md",
        "src/superclaude/skills/operational-guide/SKILL.md",
    ],
)
def test_g_no_conditional_pass_kept(rel):
    assert NO_CONDITIONAL_PASS in _read(rel)


def test_g_readme_remediation_suffix_kept():
    assert "List each with specific remediation." in _read(
        "src/superclaude/skills/readme/SKILL.md"
    )


# --- (h) sc-implement-protocol plugin twins ---------------------------------


def test_h_implement_protocol_plugin_twins_byte_equal():
    plugin_root = "plugins/superclaude/skills/sc-implement-protocol/"
    files = sorted(p for p in _tracked_text() if p.startswith(plugin_root))
    assert files, "no plugin sc-implement-protocol files tracked"
    diff = [
        p
        for p in files
        if (_REPO / p).read_bytes()
        != (
            _REPO
            / "src/superclaude/skills/sc-implement-protocol"
            / p[len(plugin_root) :]
        ).read_bytes()
    ]
    assert not diff, f"plugin twins differ from src: {diff}"


# --- (i) site-sweep wordings -------------------------------------------------

SWEEP_PHRASES = (
    "FAIL: Issues found",
    "strictly fewer issues",
    "logged for human review",
    "zero-tolerance policy for errors",
    "issues of any severity",
)
# Same patterns as .dev/review-severity-rule/sweep/fixloop_scan.py (F1-F6).
FIX_LOOP_PATTERNS = {
    "F1": r"\bif (any )?(findings|issues) (exist|are found|found)\b",
    "F2": r"\bfinds new issues\b",
    "F3": r"\bissues remain unfixed\b",
    "F4": r"\b(apply|applies|applying|applied) (all|ALL) (the )?(consolidated |collected |fidelity )?(fixes|findings|corrections)\b",
    "F5": r"(fix(-| )agent|fix_authorization: true)[^\n]*\bconsolidated\b|\bconsolidated\b[^\n]*(fix(-| )agent|fix_authorization: true)",
    "F6": r"\bif (any )?(unresolved )?(issues|findings) remain",
}
_FIX_LOOP_RES = {k: re.compile(p, re.IGNORECASE) for k, p in FIX_LOOP_PATTERNS.items()}
_PM_EXAMPLE_REASON = "pm-agent example: describes the PM agent's self-improvement doc update after a mistake, not a review fix loop"
SWEEP_ALLOW = {
    (
        "agents/sc-pm-agent.md",
        "- Adds prevention checklist if issues found",
    ): _PM_EXAMPLE_REASON,
    (
        "src/superclaude/agents/pm-agent.md",
        "- Adds prevention checklist if issues found",
    ): _PM_EXAMPLE_REASON,
    (
        "plugins/superclaude/agents/pm-agent.md",
        "- Adds prevention checklist if issues found",
    ): _PM_EXAMPLE_REASON,
}


def _sweep_hits(line: str) -> list[str]:
    ids = _phrase_hits(line, SWEEP_PHRASES)
    if "blocking" not in line.lower():
        ids += [k for k, rx in _FIX_LOOP_RES.items() if rx.search(line)]
    return ids


@pytest.mark.parametrize(
    "scratch",
    [
        "If findings exist, spawn ONE rf-qa agent",
        "If verification finds new issues, repeat",
        "FAIL: Issues found (list with specific fixes)",
        "logged for human review",
    ],
)
def test_i_sweep_matcher_fires(scratch):
    assert _sweep_hits(scratch)


def test_i_blocking_line_is_in_scope():
    assert not _sweep_hits("If blocking findings exist, spawn ONE rf-qa agent")


def test_i_no_swept_wording_in_tracked_primitives():
    hits, used = [], set()
    for path, text in sorted(_files_under(*_SCAN_TREES).items()):
        for n, line in enumerate(text.splitlines(), 1):
            ids = _sweep_hits(line)
            if not ids:
                continue
            key = (path, line.strip())
            if key in SWEEP_ALLOW:
                used.add(key)
                continue
            hits.append(f"{','.join(ids)} {path}:{n}: {line.strip()[:160]}")
    assert not hits, "swept wording survives:\n" + "\n".join(hits)
    assert used == set(SWEEP_ALLOW), (
        f"stale allowlist entries: {set(SWEEP_ALLOW) - used}"
    )
    assert all(SWEEP_ALLOW.values())


# --- (k) zero tolerance only with a site-sweep qualifier --------------------

ZERO_TOLERANCE = re.compile(r"zero[- ]tolerance", re.IGNORECASE)
ZERO_TOLERANCE_QUALIFIERS = re.compile(
    r"fabricat|forger|hallucinat|verification|verify|accuracy|dismissal|incremental writing|blocking"
    r'|The "Zero tolerance" closing line is VERBATIM',
    re.IGNORECASE,
)
# Lines whose qualifier is in their heading, not on the line (site-sweep reasons).
_FORGERY_REASON = "closes the 'Penalty for Forgery - ZERO TOLERANCE' rule (fabricated sources); fabrication is blocking"
ZERO_TOLERANCE_ALLOW = {
    (
        "src/superclaude/rules/core/anti_hallucination_task_completion_rules.md",
        "- This is a zero-tolerance rule with NO exceptions",
    ): _FORGERY_REASON,
    (
        "src/superclaude/rules/core/anti_sycophancy.md",
        "- This is a zero-tolerance rule with NO exceptions",
    ): _FORGERY_REASON,
}


def _zero_tolerance_unqualified(line: str) -> bool:
    return bool(ZERO_TOLERANCE.search(line)) and not ZERO_TOLERANCE_QUALIFIERS.search(
        line
    )


@pytest.mark.parametrize(
    "scratch",
    [
        "Zero tolerance: The batch must be perfect to pass",
        "You enforce a zero-tolerance policy for errors.",
    ],
)
def test_k_unqualified_zero_tolerance_fires(scratch):
    assert _zero_tolerance_unqualified(scratch)


def test_k_zero_tolerance_only_with_a_qualifier():
    hits, used = [], set()
    for path, text in sorted(_files_under(*_SCAN_TREES).items()):
        for n, line in enumerate(text.splitlines(), 1):
            if not _zero_tolerance_unqualified(line):
                continue
            key = (path, line.strip())
            if key in ZERO_TOLERANCE_ALLOW:
                used.add(key)
                continue
            hits.append(f"{path}:{n}: {line.strip()[:160]}")
    assert not hits, "unqualified zero tolerance:\n" + "\n".join(hits)
    assert used == set(ZERO_TOLERANCE_ALLOW), (
        f"stale allowlist entries: {set(ZERO_TOLERANCE_ALLOW) - used}"
    )
