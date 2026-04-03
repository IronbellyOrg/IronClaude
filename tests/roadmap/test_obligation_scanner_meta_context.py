"""Meta-context false positive suppression tests for obligation scanner.

Tests the 2-layer meta-context classification system:
- Layer 1: Structural exemptions (inline code, completed checklists)
- Layer 2: Negation/meta-context classification (_is_meta_context)
"""

from __future__ import annotations

import textwrap

import pytest

from superclaude.cli.roadmap.obligation_scanner import _is_meta_context, scan_obligations


class TestLayer1InlineCode:
    """Layer 1a: Scaffold terms inside backtick spans are MEDIUM."""

    def test_inline_code_scaffold_term_is_medium(self):
        """E4: Inline code reference demoted to MEDIUM."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Implementation
            - Build the auth module

            ## Phase 2: Verification
            - Remove all `placeholder` values from config
        """
        )
        report = scan_obligations(content)
        phase2_obs = [
            o
            for o in report.obligations
            if "placeholder" in o.term.lower() and "phase 2" in o.phase.lower()
        ]
        assert phase2_obs
        assert all(o.severity == "MEDIUM" for o in phase2_obs)

    def test_inline_code_does_not_affect_plain_text(self):
        """E1: Plain scaffold term without backticks stays HIGH."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Setup
            - Create placeholder config files
        """
        )
        report = scan_obligations(content)
        assert any(o.severity == "HIGH" for o in report.obligations)


class TestLayer1CompletedChecklist:
    """Layer 1b: Completed checklist items are MEDIUM."""

    def test_completed_checklist_is_medium(self):
        """E5: Completed checklist items demoted to MEDIUM."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Setup
            - Create scaffold structure

            ## Phase 2: Completion
            - [x] All scaffold replaced with real implementations
            - [x] Mock services removed
        """
        )
        report = scan_obligations(content)
        phase2_obs = [
            o
            for o in report.obligations
            if o.severity == "MEDIUM" and "phase 2" in o.phase.lower()
        ]
        assert phase2_obs

    def test_unchecked_checklist_stays_high(self):
        """Unchecked checklist items stay HIGH."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Setup
            - [ ] Create mock handler
        """
        )
        report = scan_obligations(content)
        assert any(o.severity == "HIGH" for o in report.obligations)


class TestIsMetaContext:
    """Parameterized tests for _is_meta_context() classification."""

    @pytest.mark.parametrize(
        "line,term_pos,expected,reason",
        [
            ("Create mocked step runners", 7, False, "affirmative"),
            ("No template sentinel placeholders present", 27, True, "negation_prefix"),
            ("Must not contain placeholder values", 21, True, "negation_prefix"),
            ("Ensure no mock data remains", 10, True, "negation_prefix"),
            ("Removed the stub endpoint in v2.1", 12, True, "past_tense"),
            ("grep -rn '<placeholder>' src/", 11, True, "shell_command"),
            ("find . -name '*mock*' -delete", 17, True, "shell_command"),
            ("Zero placeholder values found", 5, True, "gate_criteria"),
            ("Risk: placeholder data could leak", 6, True, "risk_description"),
            ("Use placeholder config for now", 4, False, "affirmative"),
            (
                "The placeholder should not be committed",
                4,
                False,
                "negation_after_term",
            ),
            ("Do not remove the mock yet", 18, True, "double_negation"),
            ("## Phase 1: Skeleton Setup", 13, False, "heading_affirmative"),
            (
                "Remove old stubs and add new placeholder",
                11,
                True,
                "negation_prefix",
            ),
            (
                "Remove old stubs and add new placeholder",
                30,
                True,
                "affirmative_second_term",
            ),
            (
                "Ensure the system has no residual temporary files",
                32,
                True,
                "negation_prefix",
            ),
            ("Never deploy with hardcoded credentials", 18, True, "negation_prefix"),
        ],
    )
    def test_is_meta_context(self, line, term_pos, expected, reason):
        result = _is_meta_context(line, term_pos)
        assert result == expected, f"Failed for {reason}: {line!r}"


class TestMetaContextFalsePositiveSuppression:
    """Integration: meta-context false positives do not block the gate."""

    def test_verification_criteria_not_counted(self):
        """Gate criteria mentioning scaffold terms are MEDIUM, not HIGH."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Implementation
            - Build the authentication module

            ## Phase 2: Verification
            - No template sentinel placeholders present
            - Ensure no mock data remains in production config
            - Zero stub endpoints found in final build
        """
        )
        report = scan_obligations(content)
        assert report.undischarged_count == 0

    def test_shell_commands_not_counted(self):
        """Shell commands searching for scaffold terms are MEDIUM."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Setup
            - Initialize project structure

            ## Phase 2: QA Checks
            - grep -rn 'placeholder' src/superclaude/
        """
        )
        report = scan_obligations(content)
        assert report.undischarged_count == 0

    def test_affirmative_obligations_still_detected(self):
        """Real scaffolding obligations remain HIGH and counted."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Skeleton Setup
            - Create mocked step runners for initial testing
            - Build placeholder dispatch table
            - Implement stub executor

            ## Phase 2: Core Logic
            - Implement pipeline logic
        """
        )
        report = scan_obligations(content)
        assert report.undischarged_count >= 3
        high_count = len([o for o in report.obligations if o.severity == "HIGH"])
        assert high_count >= 3

    def test_mixed_real_and_meta_same_document(self):
        """Real obligations counted, meta-references excluded, in same doc."""
        content = textwrap.dedent(
            """\
            ## Phase 1: Bootstrap
            - Create placeholder config files
            - Build skeleton API layer

            ## Phase 2: Implement
            - Replace placeholder config with real values
            - Wire skeleton into production router

            ## Phase 3: Verify
            - Ensure no placeholder values remain
        """
        )
        report = scan_obligations(content)
        assert report.undischarged_count <= 1


class TestExistingBehaviorPreserved:
    """Regression: existing scanner behavior is not degraded."""

    def test_exempt_comment_still_works(self):
        content = textwrap.dedent(
            """\
            ## Phase 1
            - Create mock handler  # obligation-exempt
        """
        )
        report = scan_obligations(content)
        exempt_obs = [o for o in report.obligations if o.exempt]
        assert exempt_obs

    def test_code_block_still_medium(self):
        content = "## Phase 1\n```python\nmock = {}\n```\n"
        report = scan_obligations(content)
        code_obs = [o for o in report.obligations if o.severity == "MEDIUM"]
        assert code_obs

    def test_discharge_mechanism_unchanged(self):
        content = textwrap.dedent(
            """\
            ## Phase 1
            - Create stub handler

            ## Phase 2
            - Replace stub handler with real implementation
        """
        )
        report = scan_obligations(content)
        discharged = [o for o in report.obligations if o.discharged]
        assert discharged
