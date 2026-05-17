"""
Spec-presence tests for /sc:reflect Recommendation Re-scrutiny Phase.

Verifies that src/superclaude/commands/reflect.md carries the Re-scrutiny
phase additions specified by .dev/releases/current/sc-reflect-rescrutiny-design.md
(§7.0–§7.6 directives).

If a future edit removes phase 4, downgrades the frontmatter, or reverts
the §3.4-vs-§7.3 Grep-as-file-anchored fix, these tests fail.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
REFLECT_MD = REPO_ROOT / "src" / "superclaude" / "commands" / "reflect.md"


@pytest.fixture(scope="module")
def reflect_text() -> str:
    assert REFLECT_MD.exists(), f"missing canonical spec at {REFLECT_MD}"
    return REFLECT_MD.read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    """Return the YAML frontmatter block (between the opening and closing ---)."""
    parts = text.split("---", 2)
    assert len(parts) >= 3, "reflect.md must start with a YAML frontmatter block"
    return parts[1]


class TestRescrutinyPhasePresence:
    """Direct content checks against reflect.md."""

    def test_frontmatter_declares_context7(self, reflect_text):
        fm = _frontmatter(reflect_text)
        assert "mcp-servers:" in fm
        # context7 is the conditional dependency added by design §7.0
        assert "context7" in fm, "frontmatter must list context7 (design §7.0)"
        assert "serena" in fm, "frontmatter must keep serena"

    def test_behavioral_flow_has_six_phases(self, reflect_text):
        # Phase 4 must be Re-scrutinize; Document/Optimize must shift to 5/6
        for needle in (
            "1. **Analyze**",
            "2. **Validate**",
            "3. **Reflect**",
            "4. **Re-scrutinize**",
            "5. **Document**",
            "6. **Optimize**",
        ):
            assert needle in reflect_text, f"missing phase line: {needle!r}"

    def test_mcp_integration_includes_context7_entry(self, reflect_text):
        assert "**Context7 MCP**" in reflect_text, (
            "MCP Integration must include a Context7 MCP entry (design §7.2)"
        )

    def test_tool_coordination_grep_is_file_anchored(self, reflect_text):
        # Post-B1: Grep description must NOT be the original transcript-scan wording
        assert "Conversation-transcript scan" not in reflect_text, (
            "Grep description still uses the pre-B1 transcript-scan wording"
        )
        assert "**Grep**: File-anchored augmentation" in reflect_text, (
            "Grep entry must use the file-anchored description (design §7.3, post-B1)"
        )

    def test_tool_coordination_includes_websearch(self, reflect_text):
        assert "**WebSearch**: Fallback CLI precondition lookup" in reflect_text, (
            "WebSearch entry missing from Tool Coordination (design §7.3)"
        )

    def test_key_patterns_include_rescrutiny(self, reflect_text):
        assert "**Recommendation Re-scrutiny**" in reflect_text, (
            "Key Patterns must include the Recommendation Re-scrutiny pattern (design §7.4)"
        )

    def test_boundaries_will_has_three_new_bullets(self, reflect_text):
        for bullet in (
            "Re-scrutinize executable artifacts emitted by the reflection itself",
            "Block reflection-emitted recommendations that contradict facts",
            "Annotate every cleared recommendation with the basis on which it was cleared",
        ):
            assert bullet in reflect_text, (
                f"Boundaries — Will is missing the bullet starting with: {bullet!r}"
            )

    def test_boundaries_will_not_uses_stratified_hedge_wording(self, reflect_text):
        """
        The Will-Not 'Block on hedge cases' bullet MUST be qualified to LOW/MEDIUM
        stakes — the unqualified version contradicts the design §3.6 stakes table
        (HIGH-stakes verbs DO block on hedge).
        """
        assert "Block on hedge cases for LOW/MEDIUM stakes" in reflect_text, (
            "Will-Not 'Block on hedge cases' bullet must be qualified to "
            "LOW/MEDIUM stakes (matches design §3.6 + §7.6)"
        )
        assert "Maintain a persistent cross-session entity registry" in reflect_text
        assert "Validate non-executable commentary" in reflect_text


@pytest.mark.confidence_check
def test_rescrutiny_spec_confidence(confidence_checker, reflect_text):
    """
    Confidence-check marker test for the Re-scrutiny spec.

    Asserts the spec is in a high-confidence state for downstream consumers
    (commands/skills that read reflect.md to decide phase 4 behavior).

    The five confidence dimensions, mapped to this spec:
      - duplicate_check_complete: phase 4 is the only Re-scrutinize section
      - architecture_check_complete: 6-phase numbered list intact
      - official_docs_verified: context7 declared in frontmatter
      - oss_reference_complete: design doc is the OSS reference
      - root_cause_identified: B1's transcript-scan bug is removed
    """
    duplicate_ok = reflect_text.count("4. **Re-scrutinize**") == 1
    six_phase_ok = all(f"{n}. **" in reflect_text for n in (1, 2, 3, 4, 5, 6))
    context7_ok = "context7" in _frontmatter(reflect_text)
    design_ref_ok = (
        REPO_ROOT / ".dev" / "releases" / "current" / "sc-reflect-rescrutiny-design.md"
    ).exists()
    b1_root_cause_ok = "Conversation-transcript scan" not in reflect_text

    context = {
        "test_name": "test_rescrutiny_spec_confidence",
        "duplicate_check_complete": duplicate_ok,
        "architecture_check_complete": six_phase_ok,
        "official_docs_verified": context7_ok,
        "oss_reference_complete": design_ref_ok,
        "root_cause_identified": b1_root_cause_ok,
    }

    confidence = confidence_checker.assess(context)
    assert confidence >= 0.9, (
        f"Re-scrutiny spec confidence {confidence:.2f} is below the "
        f"≥0.9 threshold required to ship. Failing checks: "
        f"{[c for c in context['confidence_checks'] if c.startswith('❌')]}"
    )
