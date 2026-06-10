"""Bounded validation for the task-builder ``--reflect`` POST-gate dial (TASK-RF-20260608-194013).

Two test surfaces, mirroring the in-repo precedents:

1. **Rule re-implementation + fixture verdict matrix** (cf.
   ``tests/audit/test_evidence_bound_tb_add_8.py``): a small re-implementation of the
   rf-qa ``TB-Add-9`` MODE-MATCH assertions (spec §9.1 V5/V6/V7/V8/V9 + §9.3 MODE-MATCH)
   is run against fixture tasklists under ``tests/skills/fixtures/reflect_mode/`` to assert
   AT-VALIDATION-1, AT-MISMATCH-1, and AT-MODE-MATCH.

2. **Content-marker assertions** (cf. ``tests/skills/test_task_builder_merge.py``) over the
   source-of-truth markdown — the edited ``SKILL.md`` (AT-PLUMBING-1 precedence prose, the
   8-value oracle, the RESOLVE_AUTO predicate, the per-mode templates, the FR-3 Rule-19 fix)
   and the edited ``rf-qa.md`` (``TB-Add-9``, ``Checklist (29 items)``, the 8th value token).

The task-builder is an LLM-driven markdown emitter with no callable ``build_tasklist()``
entry point (research 06), so end-to-end emission is intentionally NOT driven here.

Run: ``uv run pytest tests/skills/test_reflect_mode_validation.py -v``
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"
RF_QA_PATH = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "reflect_mode"

# The 8-value oracle (OQ-1 resolution: the union including auto-resolved-2-degraded-halt).
EIGHT_VALUE_SET = (
    "none",
    "1",
    "2",
    "auto-resolved-1",
    "auto-resolved-2",
    "halt",
    "2-degraded-halt",
    "auto-resolved-2-degraded-halt",
)

_MODE_RE = re.compile(r'^reflect_post_mode:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_ITEM_RE = re.compile(r"^\s*-\s*\[[ x]\]\s*\*\*(.+?)\*\*")
_ACTION_RE = re.compile(r"^\s*-\s*\*\*Action\*\*\s*:\s*(.*)$")


# --------------------------------------------------------------------------- parsing


def parse_mode(text: str) -> str | None:
    """Extract the frontmatter ``reflect_post_mode`` value (quotes stripped)."""
    m = _MODE_RE.search(text)
    return m.group(1).strip() if m else None


def parse_items(text: str) -> list[tuple[str, str]]:
    """Return ``(header, action_text)`` for each ``- [ ] **...**`` checklist item."""
    lines = text.splitlines()
    items: list[tuple[str, str]] = []
    for idx, line in enumerate(lines):
        m = _ITEM_RE.match(line)
        if not m:
            continue
        header = m.group(1)
        action = ""
        for j in range(idx + 1, min(idx + 12, len(lines))):
            if _ITEM_RE.match(lines[j]):
                break
            am = _ACTION_RE.match(lines[j])
            if am:
                action = am.group(1)
                break
        items.append((header, action))
    return items


def post_reflect_item(items: list[tuple[str, str]]) -> tuple[str, str] | None:
    """The penultimate (reflect) item = the last item that is not Update-status-to-Done."""
    non_done = [it for it in items if "Update task status to Done" not in it[0]]
    return non_done[-1] if non_done else None


# --------------------------------------------------------------- TB-Add-9 re-implementation


def mode_match(text: str) -> tuple[str, str]:
    """Re-implement the rf-qa TB-Add-9 MODE-MATCH (spec §9.3) over a fixture tasklist.

    Returns ``(verdict, assertion)`` where ``verdict`` ∈ {"PASS", "MALFORMED"} and
    ``assertion`` names the first failing V# (or "" on PASS). Assertion ordering is
    chosen so the AT-VALIDATION-1 named failures surface (wrapper-in-Mode-1 → V6;
    remediate-in-Mode-1 → V9; inline-in-Mode-2 → V8).
    """
    mode = parse_mode(text)
    if mode is None or mode not in EIGHT_VALUE_SET:
        return ("MALFORMED", "V2")  # oracle absent / not in the 8-value set

    post = post_reflect_item(parse_items(text))

    if mode == "none":
        # V3: mode none → zero POST items.
        return ("MALFORMED", "V3") if post is not None else ("PASS", "")

    if post is None:
        # Non-none mode but no penultimate reflect item present.
        return ("MALFORMED", "V3")

    action = post[1]
    has_wrapper = "superclaude reflect run" in action
    has_inline = "/sc:reflect" in action
    has_inline_standard = "/sc:reflect --mode post --depth standard" in action
    has_remediate = "--remediate" in action
    has_agent = re.search(r"\b(Agent|Task|subagent)\b", action) is not None

    if mode in ("1", "auto-resolved-1"):
        if has_wrapper:
            return ("MALFORMED", "V6")  # Mode-1 must NOT contain wrapper shell-out
        if has_remediate:
            return ("MALFORMED", "V9")  # Mode-1 is audit-only
        if not has_inline_standard:
            return ("MALFORMED", "V5")  # Mode-1 must contain inline --depth standard
        return ("PASS", "")

    if mode in ("2", "auto-resolved-2"):
        if has_inline or has_agent:
            return ("MALFORMED", "V8")  # Mode-2 must NOT contain inline / Agent / Task
        if not has_wrapper:
            return ("MALFORMED", "V7")  # Mode-2 must contain the wrapper shell-out
        return ("PASS", "")

    # halt / 2-degraded-halt / auto-resolved-2-degraded-halt → V15/V16 (manual paste-ready)
    if "reflect_post: PENDING" in action and "--remediate" in action:
        return ("PASS", "")
    return ("MALFORMED", "V15")


def _read(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


# --------------------------------------------------------------------------- fixtures present


class TestFixturesPresent:
    @pytest.mark.parametrize(
        "name",
        [
            "mode1_ok.md",
            "mode1_with_wrapper.md",
            "mode1_with_remediate.md",
            "mode2_ok.md",
            "mode2_with_inline.md",
            "none_ok.md",
        ],
    )
    def test_fixture_exists(self, name: str) -> None:
        assert (FIXTURE_DIR / name).is_file(), f"missing fixture {name}"


# --------------------------------------------------------------------------- AT-VALIDATION-1


class TestAtValidation1:
    """AT-VALIDATION-1: mode/item shape mismatches fail the specific assertion."""

    def test_mode1_with_wrapper_fails_v6(self) -> None:
        assert mode_match(_read("mode1_with_wrapper.md")) == ("MALFORMED", "V6")

    def test_mode2_with_inline_fails_v8(self) -> None:
        assert mode_match(_read("mode2_with_inline.md")) == ("MALFORMED", "V8")

    def test_mode1_with_remediate_fails_v9(self) -> None:
        assert mode_match(_read("mode1_with_remediate.md")) == ("MALFORMED", "V9")


# ----------------------------------------------------------------- AT-MISMATCH-1 / AT-MODE-MATCH


class TestModeMatchVerdictMatrix:
    """AT-MISMATCH-1 + AT-MODE-MATCH: the oracle vs emitted Action-shape verdict matrix."""

    def test_verdict_matrix(self) -> None:
        matrix = {
            "mode1_ok.md": ("PASS", ""),
            "mode2_ok.md": ("PASS", ""),
            "none_ok.md": ("PASS", ""),
            "mode1_with_wrapper.md": ("MALFORMED", "V6"),
            "mode2_with_inline.md": ("MALFORMED", "V8"),
            "mode1_with_remediate.md": ("MALFORMED", "V9"),
        }
        observed = {name: mode_match(_read(name)) for name in matrix}
        assert observed == matrix, f"MODE-MATCH verdict matrix drifted: {observed}"

    def test_none_fixture_has_no_reflect_post_key(self) -> None:
        # FR-2: mode none omits the reflect_post: key entirely.
        assert not re.search(r"^reflect_post:", _read("none_ok.md"), re.MULTILINE)


# --------------------------------------------------------------------------- content markers


@pytest.fixture(scope="module")
def skill_text() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rf_qa_text() -> str:
    return RF_QA_PATH.read_text(encoding="utf-8")


class TestRfQaMarkers:
    def test_tb_add_9_present_and_regex_shaped(self, rf_qa_text: str) -> None:
        # The INV-010 enumeration regex must match the TB-Add-9 entry line exactly.
        assert re.search(r"^29\. \*\*TB-Add-9:", rf_qa_text, re.MULTILINE), (
            "TB-Add-9 missing or not INV-010-regex-shaped"
        )

    def test_checklist_count_bumped_to_29(self, rf_qa_text: str) -> None:
        assert "#### Checklist (29 items)" in rf_qa_text
        assert "#### Checklist (28 items)" not in rf_qa_text

    def test_region_heading_through_tb_add_9(self, rf_qa_text: str) -> None:
        assert "TB-Add-1 through TB-Add-9" in rf_qa_text
        assert "TB-Add-1 through TB-Add-7" not in rf_qa_text

    def test_eighth_value_present(self, rf_qa_text: str) -> None:
        assert "auto-resolved-2-degraded-halt" in rf_qa_text

    def test_mode_match_authored_here(self, rf_qa_text: str) -> None:
        assert "MODE-MATCH" in rf_qa_text


class TestSkillMarkers:
    def test_eight_value_oracle_in_frontmatter(self, skill_text: str) -> None:
        m = re.search(r"^reflect_post_mode:.*$", skill_text, re.MULTILINE)
        assert m, "reflect_post_mode frontmatter field missing"
        line = m.group(0)
        for token in EIGHT_VALUE_SET:
            assert token in line, f"8-value oracle missing token {token!r}"

    def test_at_plumbing_1_precedence_order(self, skill_text: str) -> None:
        # AT-PLUMBING-1: --reflect > REFLECT_POST_MODE field > legacy §5 alias map > default 2.
        # Anchor to the A.9 precedence sentence (these substrings recur elsewhere in the doc).
        anchor = skill_text.find("Precedence (§10.1, highest wins, first match):")
        assert anchor != -1, "A.9 precedence sentence missing"
        seg = skill_text[anchor : anchor + 600]
        i_flag = seg.find("explicit `--reflect <value>` flag")
        i_field = seg.find("`REFLECT_POST_MODE:` field")
        i_alias = seg.find("§5 alias map")
        i_default = seg.find("default `2`")
        assert -1 not in (i_flag, i_field, i_alias, i_default), (
            "precedence prose missing"
        )
        assert i_flag < i_field < i_alias < i_default, "precedence order is wrong"

    def test_resolve_auto_predicate_present(self, skill_text: str) -> None:
        assert "RESOLVE_AUTO(TCS, S5, S6, W)" in skill_text
        assert 'return "2-degraded-halt"' in skill_text

    def test_mode_templates_present(self, skill_text: str) -> None:
        assert (
            "Inline post-execution reflect audit (same session, audit-only, HALT)"
            in skill_text
        )
        assert (
            "Independent post-execution reflect gate (wrapper subprocess, HALT)"
            in skill_text
        )
        # §6.4 retains the byte-identical legacy title.
        assert (
            "Independent post-execution reflection gate (fresh session, HALT)"
            in skill_text
        )

    def test_rule_19_fr3_fix_conditions_inline_prohibition_on_mode(
        self, skill_text: str
    ) -> None:
        # FR-3 fix: the "MUST NOT run reflect inline" clause must NOT apply to Mode 1.
        assert "does **NOT** apply to Mode 1" in skill_text

    def test_rule_20_retargeted_to_oracle(self, skill_text: str) -> None:
        # Rule 20 (sibling, audit-F3) must SURVIVE and be RETARGETED onto the
        # reflect_post_mode oracle. Keying it on the retired `POST_REFLECT_GATE: ENABLED`
        # field would dead-trigger for the default `REFLECT_POST_MODE: 2` build and
        # silently re-open audit finding F3 (the PG5.2 CRITICAL fix guards exactly this).
        m = re.search(
            r"^20\. \*\*POST reflect gate persists `executor_model_class`.*?(?=\n\n)",
            skill_text,
            re.MULTILINE | re.DOTALL,
        )
        assert m, "Critical Rule 20 (sibling, audit-F3) must survive"
        rule20 = m.group(0)
        assert "reflect_post_mode" in rule20, (
            "Rule 20 must be retargeted onto the reflect_post_mode oracle (PG5.2 fix)"
        )
        assert "other than `none`" in rule20, (
            "Rule 20 trigger must be 'reflect_post_mode != none', "
            "not the retired POST_REFLECT_GATE: ENABLED"
        )
