"""Text pins and drift test for /sc:spec-panel-ledger (issue 346, theme ledger).

The variant is a byte copy of the 472-line Arm B spec-panel.md (kept here as the
fixture ``fixtures/review-ledger/spec-panel-post427-base.md``) with three blocks
changed: the frontmatter name and description, the Usage line, and the review
loop section (``## Review Loop`` becomes ``## Review Ledger Loop``).

Enforcement type: STATIC - assertions over the command text read from disk.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from tests.skills.test_review_severity_rule import (
    AT_CAP_CLAUSES,
    BANNED_SEVERITY_PHRASES,
    CANONICAL_CAP_TEXT,
    CAP_REGRESSION,
    _phrase_hits,
    _sweep_hits,
    _zero_tolerance_unqualified,
)

_REPO = Path(__file__).resolve().parents[2]
VARIANT = _REPO / "src/superclaude/commands/spec-panel-ledger.md"
BASE = (
    Path(__file__).resolve().parent
    / "fixtures/review-ledger/spec-panel-post427-base.md"
)
BASE_SHA256 = "c8d80346a96cb528fce6cff3bcadfed5bc95d1eee48dea0ac275404314b8df2f"
NEW_FILES = (
    VARIANT,
    _REPO / "src/superclaude/skills/sc-review-ledger/SKILL.md",
    _REPO / "src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py",
)
BULLETS = (
    "Setup",
    "Find",
    "Verify",
    "Sweep",
    "Report",
    "Cap",
    "Reviser contract",
    "Precedence",
)


def _text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    start = lines.index(heading)
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
    return lines[start + 1 : end]


def comparable(text: str, loop_heading: str) -> str:
    """The text with the excluded blocks removed: frontmatter name and description,
    the Usage line and the review loop section."""
    lines = text.splitlines()
    fm_end = lines.index("---", 1)
    lines = [
        ln
        for i, ln in enumerate(lines)
        if not (i < fm_end and ln.startswith(("name:", "description:")))
    ]
    u = lines.index("## Usage")
    fence = lines.index("```text", u)
    del lines[fence + 1]
    start = lines.index(loop_heading)
    end = lines.index("## Output Formats")
    del lines[start:end]
    return "\n".join(lines)


def drift(variant: str, base: str) -> list[str]:
    a = comparable(base, "## Review Loop").splitlines()
    b = comparable(variant, "## Review Ledger Loop").splitlines()
    import difflib

    return [
        d
        for d in difflib.unified_diff(a, b, lineterm="", n=0)
        if d[:1] in "+-" and d[:3] not in ("+++", "---")
    ]


def test_base_fixture_is_the_arm_b_file():
    data = BASE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == BASE_SHA256
    assert len(data.decode("utf-8").splitlines()) == 472


def test_cap_text_and_at_cap_clause_present():
    flat = " ".join(_text(VARIANT).split())
    assert CANONICAL_CAP_TEXT in flat
    assert AT_CAP_CLAUSES[1] in flat


def test_severity_scans_over_the_new_files_on_disk():
    hits = scan_lines({str(p): _text(p) for p in NEW_FILES})
    assert not hits, hits


def scan_lines(files: dict[str, str]) -> list[str]:
    """Every per-line check of test_review_severity_rule.py, over working-tree text."""
    hits = []
    for path, text in files.items():
        for n, line in enumerate(text.splitlines(), 1):
            found = _phrase_hits(line, BANNED_SEVERITY_PHRASES)
            found += ["cap-regression"] if CAP_REGRESSION.search(line) else []
            found += _sweep_hits(line)
            found += ["zero-tolerance"] if _zero_tolerance_unqualified(line) else []
            if found:
                hits.append(f"{path}:{n}: {found}")
    return hits


def test_severity_scan_fires_on_an_old_cap_number():
    assert scan_lines({"scratch": "Run max 3 fix cycles before escalating."})


def test_loop_section_once_before_output_formats_with_eight_bullets():
    text = _text(VARIANT)
    lines = text.splitlines()
    assert lines.count("## Review Ledger Loop") == 1
    assert lines.index("## Review Ledger Loop") < lines.index("## Output Formats")
    assert "## Review Loop" not in lines
    body = [ln for ln in _section(text, "## Review Ledger Loop") if ln.strip()]
    refusal, bullets = body[0], body[1:]
    assert (
        "spec-panel-ledger has no unattended mode" in refusal
        and "`--unattended`" in refusal
    )
    assert len(bullets) == 8
    labels = [re.match(r"- \*\*(.+?)\*\*:", b).group(1) for b in bullets]
    assert tuple(labels) == BULLETS


def _bullet(name: str) -> str:
    body = _section(_text(VARIANT), "## Review Ledger Loop")
    return next(b for b in body if b.startswith(f"- **{name}**:"))


def test_names_and_flags_present_old_flags_absent():
    text = _text(VARIANT)
    section = "\n".join(_section(text, "## Review Ledger Loop"))
    for name in (
        "`init`",
        "`begin`",
        "`find`",
        "`verify`",
        "`close`",
        "`sweep --prepare`",
        "ledger-input",
    ):
        assert name in section, name
    for flag in ("--ledger", "--revert-unclaimed", "--sweep"):
        assert flag in text, flag
    assert "--re-review" not in text and "--baseline" not in text


def test_no_unattended_mode_heading():
    assert not re.search(r"^## Unattended mode", _text(VARIANT), re.M)


def test_no_added_src_superclaude_occurrence():
    assert _text(VARIANT).count("src/superclaude") == _text(BASE).count(
        "src/superclaude"
    )
    base_lines = [ln for ln in _text(BASE).splitlines() if "src/superclaude" in ln]
    var_lines = [ln for ln in _text(VARIANT).splitlines() if "src/superclaude" in ln]
    assert var_lines == base_lines


def test_setup_bullet_installed_copy_first():
    setup = _bullet("Setup")
    assert "Skill sc-review-ledger" in setup
    assert (
        0 <= setup.index("~/.claude/skills/") < setup.index("project `.claude/skills/")
    )
    assert "<doc dir>/<doc stem>.review-ledger/" in setup


def test_sweep_bullet_heartbeat_condition_and_fallback():
    sweep = _bullet("Sweep")
    assert "5-minute heartbeat" in sweep and "longer than 5 minutes" in sweep
    assert (
        "`--sweep`" in sweep
        and "sweep --prepare" in sweep
        and "never opens the ledger folder" in sweep
    )


def test_cap_and_reviser_bullets():
    cap = _bullet("Cap")
    assert (
        CANONICAL_CAP_TEXT in cap
        and AT_CAP_CLAUSES[1] in cap
        and "`review: N of 3`" in cap
    )
    assert "`--revert-unclaimed`" in _bullet(
        "Reviser contract"
    ) and "consent" in _bullet("Reviser contract")


def test_variant_equals_base_outside_the_changed_blocks():
    assert drift(_text(VARIANT), _text(BASE)) == []


def test_drift_check_fails_on_a_changed_word():
    mutated = _text(VARIANT).replace(
        "## Expert Panel System", "## Expert Panel Systems", 1
    )
    assert mutated != _text(VARIANT)
    assert drift(mutated, _text(BASE))
