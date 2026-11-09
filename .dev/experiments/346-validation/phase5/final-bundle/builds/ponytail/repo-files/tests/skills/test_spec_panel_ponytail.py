"""Static pins for the /sc:spec-panel-ponytail variant and the sc-fix-audit skill (issue 346).

Enforcement type: STATIC - assertions over the text of the variant, its 472-line
base fixture, the original spec-panel.md and the sc-fix-audit skill files. They
prove the text is present and unchanged, not that a session obeys it.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

from tests.skills.test_review_severity_rule import AT_CAP_CLAUSES, CANONICAL_CAP_TEXT

_REPO = Path(__file__).resolve().parents[2]
VARIANT = _REPO / "src/superclaude/commands/spec-panel-ponytail.md"
ORIGINAL = _REPO / "src/superclaude/commands/spec-panel.md"
BASE = _REPO / "tests/skills/fixtures/spec-panel-post427-base.md"
SKILL_DIR = _REPO / "src/superclaude/skills/sc-fix-audit"
BASE_SHA256 = "c8d80346a96cb528fce6cff3bcadfed5bc95d1eee48dea0ac275404314b8df2f"

FIX_USAGE = (
    "/sc:spec-panel-ponytail [@file] --fix-audit --re-review <prior-findings-file>"
    " --baseline <saved-copy> [--dispositions <file>]"
)
# (variant line, base line): the enumerated one-line replacements
REPLACEMENTS = (
    ("name: spec-panel-ponytail", "name: spec-panel"),
    (
        'description: "Multi-expert specification review and improvement using renowned'
        " specification and software engineering experts (variant: adds the --fix-audit"
        ' step, issue 346)"',
        'description: "Multi-expert specification review and improvement using renowned'
        ' specification and software engineering experts"',
    ),
    (
        "# /sc:spec-panel-ponytail - Expert Specification Review Panel",
        "# /sc:spec-panel - Expert Specification Review Panel",
    ),
)
FIX_AUDIT_LITERALS = (
    "--fix-audit",
    "review: 2 of 3",
    "audit: not-triggered",
    "audit: skipped",
    "Skill ponytail:ponytail-review",
    "~/.claude/skills/sc-fix-audit/SKILL.md",
    "the run is not a review",
)


def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _section(lines: list[str], heading: str) -> list[str]:
    start = lines.index(heading) + 1
    end = next(
        (i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines)
    )
    return lines[start:end]


def fix_audit_text() -> list[str]:
    """The literal `## Fix Audit` block of the plan's source.md section 3.2 (fence lines dropped).

    The plan package moves from to-do/ to done/ when archived; it is tracked in either.
    """
    sources = sorted(_REPO.glob(".dev/tasks/*/TASK-WF-spec-20261108-181547/source.md"))
    assert sources, "the plan package source.md is missing from this checkout"
    src = _lines(sources[0])
    start = src.index("### 3.2 New section text for file 1 (literal)")
    open_ = src.index("```markdown", start)
    return src[open_ + 1 : src.index("```", open_ + 1)]


def strip_planned(lines: list[str]) -> list[str]:
    """The variant minus its enumerated differences; raises when one is not where planned."""
    out = list(lines)
    rl = out.index("## Review Loop")
    fa = out.index("## Fix Audit")
    of = out.index("## Output Formats")
    following = next(i for i in range(rl + 1, len(out)) if out[i].startswith("## "))
    if following != fa or not fa < of:
        raise ValueError("## Fix Audit is not directly after ## Review Loop")
    if out[fa:of] != fix_audit_text() + [""]:
        raise ValueError("## Fix Audit is not the literal source.md section 3.2 text")
    del out[fa:of]  # the Fix Audit heading through its trailing blank line
    usage = out.index(FIX_USAGE)
    if not out[usage - 1].startswith("/sc:spec-panel-ponytail ["):
        raise ValueError(
            "the --fix-audit Usage line does not follow the renamed Usage line"
        )
    del out[usage]
    out[usage - 1] = out[usage - 1].replace(
        "/sc:spec-panel-ponytail [", "/sc:spec-panel [", 1
    )
    for new, old in REPLACEMENTS:
        out[out.index(new)] = old
    return out


def test_base_fixture_is_the_472_line_arm_b_file():
    data = BASE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == BASE_SHA256
    assert len(data.decode("utf-8").splitlines()) == 472


def test_variant_minus_planned_changes_equals_base():
    assert strip_planned(_lines(VARIANT)) == _lines(BASE)


def _drop_fix_audit_heading(lines):
    return [ln for ln in lines if ln != "## Fix Audit"]


def _edit_review_loop_bullet(lines):
    i = next(i for i, ln in enumerate(lines) if ln.startswith("4. **Cap**"))
    return lines[:i] + [lines[i] + " (edited)"] + lines[i + 1 :]


def _add_stray_line(lines):
    i = lines.index("## Output Formats")
    return lines[:i] + ["stray line"] + lines[i:]


@pytest.mark.parametrize(
    "mutate", [_drop_fix_audit_heading, _edit_review_loop_bullet, _add_stray_line]
)
def test_drift_check_catches_a_scratch_copy_change(mutate):
    scratch = mutate(_lines(VARIANT))
    with pytest.raises((ValueError, AssertionError)):
        assert strip_planned(scratch) == _lines(BASE)


def test_review_loop_bullets_unchanged():
    bullets = [ln for ln in _section(_lines(VARIANT), "## Review Loop") if ln.strip()]
    assert len(bullets) == 7
    assert bullets == [
        ln for ln in _section(_lines(BASE), "## Review Loop") if ln.strip()
    ]
    assert bullets == [
        ln for ln in _section(_lines(ORIGINAL), "## Review Loop") if ln.strip()
    ]


def test_fix_audit_section_once_directly_after_review_loop():
    lines = _lines(VARIANT)
    assert lines.count("## Fix Audit") == 1
    headings = [ln for ln in lines if ln.startswith("## ")]
    assert headings[headings.index("## Review Loop") + 1] == "## Fix Audit"
    body = "\n".join(_section(lines, "## Fix Audit"))
    for literal in FIX_AUDIT_LITERALS:
        assert literal in body, literal


def test_variant_has_no_unattended_mode():
    text = VARIANT.read_text(encoding="utf-8")
    assert "## Unattended mode" not in text
    assert "--unattended" not in text


def test_cap_text_and_at_cap_clause_present():
    flat = " ".join(VARIANT.read_text(encoding="utf-8").split())
    assert CANONICAL_CAP_TEXT in flat
    assert AT_CAP_CLAUSES[1] in flat


def test_variant_adds_no_src_superclaude_path():
    def hits(path):
        return [ln for ln in _lines(path) if "src/superclaude" in ln]

    assert hits(VARIANT) == hits(BASE)


@pytest.mark.parametrize(
    "rel", ["SKILL.md", "refs/auditor-brief.md", "scripts/fix_audit.py"]
)
def test_skill_files_have_no_src_superclaude_path(rel):
    assert "src/superclaude" not in (SKILL_DIR / rel).read_text(encoding="utf-8")


def test_skill_md_frontmatter_steps_and_lookup():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith(
        '---\nname: sc-fix-audit\ndescription: "Script and auditor brief for'
        ' /sc:spec-panel-ponytail --fix-audit"\n---\n'
    )
    for sub in ("prepare", "check", "apply", "verdict"):
        assert (
            f'uv run --no-project python "<skill base>/scripts/fix_audit.py" {sub}'
            in text
        ), sub
    home = text.index("~/.claude/skills/sc-fix-audit/")
    project = re.search(r"(?<!~/)\.claude/skills/sc-fix-audit/", text)
    assert project and home < project.start()
    assert not re.search(r"^\s*[-*] \[[ xX]\]", text, re.M)


def test_original_spec_panel_has_no_fix_audit():
    assert "--fix-audit" not in ORIGINAL.read_text(encoding="utf-8")
