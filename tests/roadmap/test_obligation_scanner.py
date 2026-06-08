"""Unit tests for obligation_scanner.py.

Tests cover:
1. Scaffold term detection for all 11 terms (FR-MOD1.1)
2. Cross-milestone discharge matching (FR-MOD1.3, FR-MOD1.5)
3. `# obligation-exempt` comment parsing (FR-MOD1.7)
4. Code-block severity demotion to MEDIUM (FR-MOD1.8)
5. cli-portify regression case SC-002

All tests use real content fixtures, no mocks.
"""

import pytest

from superclaude.cli.roadmap.obligation_scanner import (
    scan_obligations,
)

# --- Real content fixtures ---

MULTI_MILESTONE_ROADMAP = """\
## M1: Skeleton Implementation

Build the executor skeleton with **mocked steps** for initial testing.
Use `placeholder` config values for database connections.
Create a stub authentication module.

## M2: Core Logic

Implement the core processing engine with temporary hardcoded thresholds.
Add a dummy logger for debugging. Use a fake service client for external calls.
The scaffolding for the CLI will use a no-op handler initially.

## M3: Integration

Replace mock steps with real implementations.
Wire up the `placeholder` config to actual environment variables.
Integrate the real authentication module, replacing the stub.
Connect the real service client, swap out the fake.
Fill in the no-op handler with actual logic.
"""

UNDISCHARGED_ROADMAP = """\
## M1: Setup

Build executor with **mocked steps** for the pipeline.

## M2: Features

Add feature A and feature B.

## M3: Testing

Run integration tests.
"""

EXEMPT_ROADMAP = """\
## M1: Test Infrastructure

Set up test doubles with mocked services. # obligation-exempt
Use stub clients for unit tests. # obligation-exempt

## M2: Implementation

Implement the actual services.
"""

CODE_BLOCK_ROADMAP = """\
## M1: Design

Here is the test approach:

```python
# Use mocked database for testing
db = MockDatabase()
stub_client = StubClient()
```

## M2: Implementation

Build the real database layer.
"""

CLI_PORTIFY_REGRESSION = """\
## M1: Foundation

Set up project structure and configuration.

## M2: Executor Shell

Implement executor: sequential execution only, `--dry-run`, `--resume <step-id>`, signal handling.

Milestone M2: Sequential pipeline runs end-to-end with **mocked steps**.

## M3: CLI Polish

Add rich output formatting and progress display.
"""


class TestScaffoldTermDetection:
    """FR-MOD1.1: All 11 scaffold terms detected."""

    def test_detects_mock(self):
        content = "## M1: Setup\nUse mock data for testing.\n## M2: Build\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1
        terms = [o.term.lower() for o in report.obligations]
        assert any("mock" in t for t in terms)

    def test_detects_mocked(self):
        content = "## M1\nWith mocked steps.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_stub(self):
        content = "## M1\nCreate stub module.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_stubbed(self):
        content = "## M1\nUse stubbed endpoint.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_skeleton(self):
        content = "## M1\nBuild skeleton framework.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_placeholder(self):
        content = "## M1\nAdd placeholder values.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_scaffold(self):
        content = "## M1\nSet up scaffolding.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_temporary(self):
        content = "## M1\nUse temporary storage.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_hardcoded(self):
        content = "## M1\nWith hardcoded limits.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_noop(self):
        content = "## M1\nUse no-op handler.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_dummy(self):
        content = "## M1\nAdd dummy logger.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_fake(self):
        content = "## M1\nUse fake client.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_hardwired(self):
        content = "## M1\nHardwired config.\n## M2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1


class TestDischargeMatching:
    """FR-MOD1.3, FR-MOD1.5: Cross-milestone discharge with dual condition."""

    def test_discharged_obligations_in_later_milestone(self):
        report = scan_obligations(MULTI_MILESTONE_ROADMAP)
        discharged = [o for o in report.obligations if o.discharged]
        assert len(discharged) > 0
        # At least mock, placeholder, stub should be discharged
        discharged_terms = {o.term.lower() for o in discharged}
        assert any("mock" in t for t in discharged_terms)

    def test_undischarged_when_no_later_discharge(self):
        report = scan_obligations(UNDISCHARGED_ROADMAP)
        assert report.has_undischarged
        undischarged = [o for o in report.obligations if not o.discharged]
        assert len(undischarged) >= 1
        # "mocked steps" should be undischarged since M2/M3 don't discharge it
        terms = [o.term.lower() for o in undischarged]
        assert any("mock" in t for t in terms)

    def test_discharge_milestone_recorded(self):
        report = scan_obligations(MULTI_MILESTONE_ROADMAP)
        discharged = [o for o in report.obligations if o.discharged]
        for o in discharged:
            assert o.discharge_phase is not None

    def test_all_discharged_in_complete_roadmap(self):
        report = scan_obligations(MULTI_MILESTONE_ROADMAP)
        # Most obligations should be discharged in this well-structured roadmap
        assert report.discharged > 0


class TestExemptComments:
    """FR-MOD1.7: `# obligation-exempt` comment parsing (OQ-003)."""

    def test_exempt_obligations_detected(self):
        report = scan_obligations(EXEMPT_ROADMAP)
        exempt = [o for o in report.obligations if o.exempt]
        assert len(exempt) >= 2  # both mock and stub lines are exempt

    def test_exempt_excluded_from_undischarged_count(self):
        report = scan_obligations(EXEMPT_ROADMAP)
        # Exempt obligations should not count toward undischarged_count
        assert report.undischarged_count == 0

    def test_non_exempt_counted(self):
        content = """\
## M1: Setup
Use mocked data for testing.

## M2: Done
Ship it.
"""
        report = scan_obligations(content)
        non_exempt = [o for o in report.obligations if not o.exempt]
        assert len(non_exempt) >= 1


class TestCodeBlockSeverityDemotion:
    """FR-MOD1.8: Code-block severity demotion to MEDIUM (OQ-004)."""

    def test_code_block_scaffold_is_medium(self):
        report = scan_obligations(CODE_BLOCK_ROADMAP)
        code_block_obs = [o for o in report.obligations if o.severity == "MEDIUM"]
        assert len(code_block_obs) >= 1

    def test_non_code_block_scaffold_is_high(self):
        content = "## M1\nUse mocked data.\n## M2\nDone."
        report = scan_obligations(content)
        high = [o for o in report.obligations if o.severity == "HIGH"]
        assert len(high) >= 1

    def test_medium_excluded_from_undischarged_count(self):
        report = scan_obligations(CODE_BLOCK_ROADMAP)
        # MEDIUM obligations should not count toward undischarged_count
        medium_undischarged = [
            o for o in report.obligations if not o.discharged and o.severity == "MEDIUM"
        ]
        # undischarged_count should not include these
        for o in medium_undischarged:
            assert o.severity == "MEDIUM"
        # Verify the property works correctly
        high_undischarged = sum(
            1
            for o in report.obligations
            if not o.discharged and not o.exempt and o.severity != "MEDIUM"
        )
        assert report.undischarged_count == high_undischarged


class TestObjectiveParagraphExemption:
    """Scaffold terms in **Objective:** paragraphs are declarative, not obligations."""

    def test_scaffold_in_objective_not_detected(self):
        content = """\
## M1: Foundation

**Objective:** Provision data stores, scaffold orchestrator interfaces, and resolve open questions

## M2: Core Logic

Implement all backend auth flows.
"""
        report = scan_obligations(content)
        scaffold_obs = [o for o in report.obligations if "scaffold" in o.term.lower()]
        assert len(scaffold_obs) == 0, (
            f"Expected no scaffold obligations from objective paragraph, "
            f"got: {[o.context for o in scaffold_obs]}"
        )

    def test_scaffolded_in_objective_not_detected(self):
        content = """\
## M1: Setup

Build the skeleton. # obligation-exempt

## M2: Core Backend

**Objective:** Implement all flows through the scaffolded orchestrators and expose endpoints

## M3: Polish

Finalize the system.
"""
        report = scan_obligations(content)
        scaffold_obs = [o for o in report.obligations if "scaffold" in o.term.lower()]
        assert len(scaffold_obs) == 0

    def test_scaffold_outside_objective_still_detected(self):
        """Scaffold in normal task text must still be flagged."""
        content = """\
## M1: Setup

Set up scaffolding for the CLI module.

## M2: Done

Ship it.
"""
        report = scan_obligations(content)
        assert report.total_obligations >= 1
        terms = [o.term.lower() for o in report.obligations]
        assert any("scaffold" in t for t in terms)

    def test_mock_in_objective_not_detected(self):
        """All scaffold terms in objective paragraphs should be exempt."""
        content = """\
## M1: Setup

**Objective:** Deploy mock service layer and placeholder configs for initial validation

## M2: Real

Implement real services.
"""
        report = scan_obligations(content)
        objective_obs = [
            o for o in report.obligations if "objective" in o.context.lower()
        ]
        assert len(objective_obs) == 0


class TestCliPortifyRegression:
    """SC-002: Detects 'mocked steps' without discharge at >= 85% confidence."""

    def test_detects_mocked_steps_without_discharge(self):
        report = scan_obligations(CLI_PORTIFY_REGRESSION)
        # The roadmap mentions "mocked steps" in M2 but never discharges
        assert report.has_undischarged
        undischarged = [
            o for o in report.obligations if not o.discharged and o.severity == "HIGH"
        ]
        assert len(undischarged) >= 1
        # Verify "mocked" is among undischarged terms
        terms = [o.term.lower() for o in undischarged]
        assert any("mock" in t for t in terms)

    def test_undischarged_count_nonzero(self):
        report = scan_obligations(CLI_PORTIFY_REGRESSION)
        assert report.undischarged_count >= 1


class TestObligationReportProperties:
    """Test ObligationReport dataclass properties."""

    def test_empty_content_produces_empty_report(self):
        report = scan_obligations("")
        assert report.total_obligations == 0
        assert report.undischarged == 0
        assert report.discharged == 0
        assert not report.has_undischarged

    def test_report_counts_consistent(self):
        report = scan_obligations(MULTI_MILESTONE_ROADMAP)
        assert report.total_obligations == report.discharged + report.undischarged


class TestPhaseParsing:
    """FR-MOD1.2: Milestone-section parser with H2/H3 fallback."""

    def test_h2_milestones_detected(self):
        report = scan_obligations(MULTI_MILESTONE_ROADMAP)
        phases = {o.phase for o in report.obligations}
        assert len(phases) >= 2  # At least M1 and M2

    def test_h3_fallback(self):
        content = """\
### Section A
Use mocked data.

### Section B
Replace mock with real.
"""
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_no_headings_fallback(self):
        content = "Use mocked data for testing."
        report = scan_obligations(content)
        assert report.total_obligations >= 1
        assert report.obligations[0].phase == "entire-document"


class TestScaffoldingDescriptiveUseNotDetected:
    """`scaffold(ing|ed)?` as a descriptive noun is not an obligation.

    Mirrors the existing skeleton-imperative-verb filter. Only flag when the
    term is the direct object of an imperative verb.
    """

    def test_ownership_context_not_detected(self):
        """'team owns scaffolding' is organizational, not a scaffold artifact."""
        content = """\
## M1: Foundation
- Personnel: PT provisions infra; auth-team owns scaffolding; sec-reviewer signs off.

## M2: Done
Ship it.
"""
        report = scan_obligations(content)
        scaffold_obs = [
            o for o in report.obligations if o.term.lower().startswith("scaffold")
        ]
        assert scaffold_obs == [], (
            f"Expected no scaffold obligations, got: "
            f"{[o.context for o in scaffold_obs]}"
        )

    def test_descriptive_noun_context_not_detected(self):
        """'scaffolding work' / 'for scaffolding' is descriptive, not an
        actionable obligation. Post Fix 3, the descriptor noun 'fallback'
        causes Layer 4 to demote to MEDIUM (which is excluded from
        ``undischarged_count``); prior behavior dropped it entirely. Both
        outcomes satisfy the test's intent: descriptive use does NOT
        contribute to the undischarged gate.
        """
        content = """\
## M1: Setup
Fallback to dev-managed instances for scaffolding work if provisioning slips.

## M2: Done
Ship it.
"""
        report = scan_obligations(content)
        scaffold_obs = [
            o for o in report.obligations if o.term.lower().startswith("scaffold")
        ]
        # Either dropped entirely OR demoted to MEDIUM is acceptable —
        # both keep it out of the undischarged_count.
        for o in scaffold_obs:
            assert o.severity == "MEDIUM", (
                f"descriptive 'scaffolding' must not be HIGH-severity, got {o.severity}"
            )
        assert report.undischarged_count == 0

    def test_imperative_build_still_detected(self):
        """'Build scaffolding' is a real obligation and must still be flagged."""
        content = """\
## M1: Setup
Build scaffolding for the CLI module.

## M2: Done
Ship it.
"""
        report = scan_obligations(content)
        terms = [o.term.lower() for o in report.obligations]
        assert any("scaffold" in t for t in terms)

    def test_imperative_set_up_still_detected(self):
        """Existing 'Set up scaffolding' behavior preserved."""
        content = "## M1\nSet up scaffolding for CLI.\n## M2\nDone."
        report = scan_obligations(content)
        assert any(o.term.lower().startswith("scaffold") for o in report.obligations)

    def test_imperative_stand_up_detected(self):
        """'Stand up scaffolding' is an obligation (newly supported verb)."""
        content = "## M1\nStand up scaffolding for the CLI.\n## M2\nDone."
        report = scan_obligations(content)
        assert any(o.term.lower().startswith("scaffold") for o in report.obligations)


class TestFieldLabelComponentExtraction:
    """Fix 3: field-label words should not be used as component identity.

    When a scaffold term appears in a Markdown list item whose label is
    'Personnel:', 'Decisions:', etc., the label is document metadata, not a
    component — the discharge search cannot succeed if we use it.
    """

    def test_personnel_label_not_used_as_component(self):
        """Personnel label must not become the component name."""
        # Note: this uses an imperative verb so the scaffold filter doesn't
        # skip it — we specifically want to test component extraction.
        content = """\
## M1: Foundation
- Personnel: auth-team will build scaffolding for `AuthExecutor` this sprint.

## M2: Integration
Wire up `AuthExecutor` to the real token service.
"""
        report = scan_obligations(content)
        scaffold_obs = [
            o for o in report.obligations if o.term.lower().startswith("scaffold")
        ]
        assert len(scaffold_obs) == 1
        o = scaffold_obs[0]
        # Component should be the backtick term (priority 1), not 'personnel'
        assert o.component == "authexecutor"
        # And since the later phase references AuthExecutor with a discharge
        # verb, it should be discharged.
        assert o.discharged

    def test_decisions_label_not_used_as_component(self):
        """Decisions label must not become the component name."""
        content = """\
## M1: Foundation
- Decisions: team will build scaffolding module before freeze.

## M2: Integration
Wire up the scaffolding module into the pipeline.
"""
        report = scan_obligations(content)
        scaffold_obs = [
            o for o in report.obligations if o.term.lower().startswith("scaffold")
        ]
        # At least one real obligation exists; its component must not be
        # 'decisions'.
        for o in scaffold_obs:
            assert o.component != "decisions"

    def test_regression_anti_instinct_false_positive(self):
        """Real-world regression: M1 'Personnel: ... owns scaffolding' was
        falsely flagged as undischarged because the component extracted was
        'personnel', which never appears in later technical content.
        """
        content = """\
## M1: Foundation & Infrastructure
- External: PST license approval; Redis cluster; SendGrid account.
- Decisions: CONFLICT-1 closed before M1 exit.
- Personnel: PT provisions infra; auth-team owns scaffolding; sec-reviewer signs off.

## M2: Auth Core
Wire up `TokenService` to Redis. Integrate JWT signer.

## M3: Features
Implement real password reset flow.

## M4: Hardening
Run load tests and finalize RBAC.
"""
        report = scan_obligations(content)
        assert report.undischarged_count == 0, (
            f"Expected no undischarged obligations, got: "
            f"{[(o.phase, o.term, o.component, o.context) for o in report.obligations if not o.discharged]}"
        )


class TestFix1TailSectionTermination:
    """Fix 1: tail-section H2s (Risk Register, Decision Summary, etc.) must
    terminate the last milestone's section so scaffold mentions in those
    template tails are excluded from scanning entirely.
    """

    def test_fix1_tail_section_excluded(self):
        """A 'Stub' mention inside `## Risk Register` after the last
        milestone must NOT be flagged — tail sections are out of scope.

        Note: uses ``Stub handler`` (not the allowlisted ``Stub transport``)
        so the tail-section exclusion is the active path. Layer 6 (R0.2)
        would otherwise absorb the row before tail-section logic engages.
        """
        content = """\
## M1: Foundation

Build the executor module.

## Risk Register

|R-01|Stub handler retained as mitigation for unavailable upstream|Low|Medium|
"""
        report = scan_obligations(content)
        assert report.undischarged_count == 0, (
            "Tail-section Risk Register content must be excluded from "
            f"scanning, got: {[(o.phase, o.term, o.line_number) for o in report.obligations if not o.discharged]}"
        )


class TestFix3DescriptiveContext:
    """Fix 3: Layer 4 descriptor-noun adjacency demotes descriptive prose
    (outcome/result/mitigation/fallback/etc.) to MEDIUM severity. The
    discharge-intent guard ensures real obligations remain HIGH.
    """

    def test_fix3_dummy_value_remains_high(self):
        """Documents the accepted Fix-2 gap: `(dummy value)` has no
        descriptor noun adjacent AND no existing Layer 3b coverage
        (Layer 3b's `_PAREN_PHASE_LABEL_RE` covers only scaffold/mock/
        stub lexemes inside parentheticals). So Layer 4 does NOT fire
        and severity stays HIGH. If real roadmaps surface this pattern,
        revisit Fix 2 (widened parenthetical regex).
        """
        content = """\
## M1: Foundation

Inject a (dummy value) for the API key during early dev.

## M2: Hardening

Run the test suite.
"""
        report = scan_obligations(content)
        dummy_obs = [o for o in report.obligations if o.term.lower() == "dummy"]
        assert dummy_obs, "expected at least one dummy obligation"
        # No descriptor noun + no Layer 3b match → HIGH severity preserved.
        assert all(o.severity == "HIGH" for o in dummy_obs)

    def test_fix3_stub_tested_mitigation_demoted(self):
        """A per-milestone Risk subsection line containing
        `stub-tested fallback` matches BOTH 'mitigation'-style adjacency
        words (via 'mitigation' or 'fallback' in the descriptor list).
        Severity must be demoted to MEDIUM.
        """
        content = """\
## M1: Foundation

Build the executor module.

### Risk Assessment and Mitigation — M1

- Mitigated by stub-tested fallback for offline mode.

## M2: Hardening

Run the test suite.
"""
        report = scan_obligations(content)
        stub_obs = [o for o in report.obligations if o.term.lower().startswith("stub")]
        assert stub_obs, "expected at least one stub obligation"
        # Layer 4 fires via 'mitigation' + 'fallback' nouns.
        assert all(o.severity == "MEDIUM" for o in stub_obs), (
            f"expected MEDIUM, got: {[(o.term, o.severity, o.context) for o in stub_obs]}"
        )

    def test_fix3_discharge_guard_preserves_obligation(self):
        """A line that simultaneously contains a descriptor noun AND a
        discharge-intent verb MUST stay HIGH — the discharge guard
        prevents Layer 4 from masking real obligations.

        Fixture: "outcome: stub needs replacement in M3" — has both
        'outcome' (descriptor) and 'replacement' (discharge intent).
        Without the guard, Layer 4 would demote to MEDIUM; with it,
        severity stays HIGH.
        """
        content = """\
## M1: Foundation

outcome: stub needs replacement in M3.

## M2: Filler

Other work happens here.
"""
        report = scan_obligations(content)
        stub_obs = [
            o
            for o in report.obligations
            if o.term.lower().startswith("stub") and "M1" in o.phase
        ]
        assert stub_obs, "expected stub obligation in M1"
        # Discharge-intent guard preserves HIGH severity.
        high_obs = [o for o in stub_obs if o.severity == "HIGH"]
        assert high_obs, (
            "expected HIGH-severity M1 stub obligation, got: "
            f"{[(o.term, o.severity, o.context) for o in stub_obs]}"
        )


class TestFix1Fix3RegressionPreservesTrueCatches:
    """Regression: a genuine undischarged scaffold mention in a milestone
    body (NOT in a tail section, NOT adjacent to descriptor nouns) must
    still be flagged. Both fixes preserve true-catch detection.
    """

    def test_regression_genuine_undischarged_mock_handler(self):
        """M2 says 'Build mock handler for auth'; M3 does NOT discharge it.
        The scanner must flag this as undischarged.
        """
        content = """\
## M2: Auth Foundation

Build mock handler for auth flows during prototype phase.

## M3: Feature Wave

Implement password reset and email verification flows.
"""
        report = scan_obligations(content)
        assert report.undischarged_count >= 1, (
            "Genuine mock-handler obligation must remain flagged, got: "
            f"{[(o.phase, o.term, o.severity, o.discharged) for o in report.obligations]}"
        )


class TestLayer5H3SubsectionContext:
    """Layer 5: H3 subsection-context demotion. Scaffold terms inside
    Risk Assessment / Integration Points / Milestone Dependencies / Open
    Questions H3 subsections are demoted to MEDIUM, guarded by the
    discharge-intent check that mirrors Layer 4.
    """

    def test_layer5_risk_assessment_h3_demotes_scaffold_to_medium(self) -> None:
        """Happy path: stub mentions inside a Risk Assessment H3 demote to MEDIUM.

        Note: this fixture uses ``stub handler`` (not the MultiModelSwarm
        allowlist phrase ``stub transport``) so the Layer 5 demotion path
        remains reachable. Layer 6 (R0.2 Contract #10 allowlist) takes
        precedence over Layer 5 for documented permanent-fixture phrases —
        see ``test_anti_instinct_recurrence.py`` for that path.
        """
        content = """## M2: Auth Layer

**Objective:** ship the auth surface.

### Risk Assessment and Mitigation — M2

| # | Risk | Likelihood | Impact | Detection | Mitigation | Owner |
|---|------|-----------|--------|-----------|------------|-------|
| 1 | Stub handler drifts from real semantics | Med | Low | tests pass | Pin stub to documented shape | backend |
"""
        report = scan_obligations(content)
        stub_obs = [o for o in report.obligations if o.term.lower().startswith("stub")]
        assert stub_obs, "Expected stub obligation to be detected"
        assert all(o.severity == "MEDIUM" for o in stub_obs), (
            "All stub findings inside Risk Assessment H3 must demote to MEDIUM, "
            f"got: {[(o.term, o.severity, o.context) for o in stub_obs]}"
        )
        assert report.undischarged_count == 0, (
            "Risk-Assessment-only stub mentions must not contribute to "
            f"undischarged_count, got: {report.undischarged_count}"
        )

    def test_layer5_h3_context_resets_at_next_h2_milestone(self) -> None:
        """H3 demotion state must NOT bleed across the next H2 milestone.

        Note: M2 fixture row uses ``stub handler`` (not the allowlisted
        phrase ``stub transport``) so Layer 5 demotion is the active path.
        """
        content = """## M2: Auth Layer

**Objective:** ship the auth surface.

### Risk Assessment and Mitigation — M2

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | Stub handler drifts | Med | Low | Pin stub to shape |

## M3: Lens Registry

**Objective:** register lenses.

| # | Step | Dep |
|---|------|-----|
| 3.1 | Build stub registry component | DM-100 |
"""
        report = scan_obligations(content)
        m2_stubs = [
            o
            for o in report.obligations
            if o.term.lower() == "stub" and "M2" in o.phase
        ]
        m3_stubs = [
            o
            for o in report.obligations
            if o.term.lower() == "stub" and "M3" in o.phase
        ]
        assert all(o.severity == "MEDIUM" for o in m2_stubs), (
            "M2 stub findings inside Risk Assessment H3 must be MEDIUM, "
            f"got: {[(o.severity, o.context) for o in m2_stubs]}"
        )
        assert m3_stubs, "Expected M3 stub finding"
        assert any(o.severity == "HIGH" for o in m3_stubs), (
            "M3 finding must NOT inherit M2's H3 demotion — H3 state must "
            f"reset at the M3 H2 boundary, got: {[(o.severity, o.context) for o in m3_stubs]}"
        )
        assert report.undischarged_count >= 1, (
            "Expected at least one HIGH undischarged from M3 body line, "
            f"got: {report.undischarged_count}"
        )

    @pytest.mark.parametrize(
        "h3_text",
        [
            "Risk Assessment and Mitigation — M2",
            "Risk Assessment and Mitigation - M2",  # ASCII hyphen-minus path
            "Integration Points — M2",
            "Milestone Dependencies — M2",
            "Open Questions — M2",
        ],
    )
    def test_layer5_demotes_in_demote_target_h3(self, h3_text: str) -> None:
        """Parameterized across all 4 demote-target H3 prefixes.

        Open Questions is included prospectively per round-3 gap-fill governance —
        no current FP in the 8-FP corpus sits under an OQ H3 at task-creation
        time; the branch ships with synthetic coverage only.

        One ASCII-hyphen-minus variant is exercised alongside the canonical
        em-dash forms because ``_normalize_h3_for_match``'s regex
        ``[—-]`` tolerates both U+2014 and U+002D — if a future refactor
        narrowed the class to em-dash only, hyphen-minus roadmaps would
        silently fail to normalize and zero tests would catch it.
        """
        content = (
            f"## M2: Foo\n\n### {h3_text}\n\n- Reference to M1 stub for context.\n"
        )
        report = scan_obligations(content)
        stubs = [o for o in report.obligations if o.term.lower() == "stub"]
        assert all(o.severity == "MEDIUM" for o in stubs), (
            f"Expected MEDIUM under '### {h3_text}', got "
            f"{[(o.severity, o.context) for o in stubs]}"
        )

    def test_layer5_discharge_intent_keeps_high_inside_risk_assessment(self) -> None:
        """Discharge-intent guard SKIPS the Layer 5 demote, so the line
        stays HIGH inside a demote-target H3. Mirrors the Layer 4
        discharge guard. Uses the task overview's canonical "stub needs
        replacement" shape (term-before-verb) — the alternative shape
        "replace the X stub" (verb-before-term) is independently demoted
        by the pre-existing Layer 2 ``_NEGATION_PREFIX_RE`` check and so
        cannot exercise the Layer 5 guard. See Phase 3 Findings for the
        deviation rationale.

        Mechanism note: Layer 5's branch is
        ``if _is_demoted_h3(h3_text) and not _is_discharge_intent_line(context_line)``;
        when discharge intent is present, the second clause short-circuits
        to False and the ``severity = "MEDIUM"`` assignment is skipped
        entirely. The line stays HIGH because no layer demotes it — NOT
        because a fired demote was retroactively vetoed.
        """
        content = """## M2: Transport Layer

**Objective:** ship the transport.

### Risk Assessment and Mitigation — M2

- Mitigation: stub needs replacement with real transport by M5.
"""
        report = scan_obligations(content)
        stubs = [o for o in report.obligations if o.term.lower() == "stub"]
        assert stubs, "Expected stub obligation"
        assert any(o.severity == "HIGH" for o in stubs), (
            "Discharge-intent line must remain HIGH even inside Risk "
            f"Assessment subsection, got: {[(o.severity, o.context) for o in stubs]}"
        )


class TestEndToEndMultiModelSwarmRoadmap:
    """E2E: post-Layer-5 contract on the MultiModelSwarm roadmap.

    Two assertions:
      1. None of the original 6 false-positive lines (311, 519, 529, 541,
         553, 600) is flagged — Fix 1 + Fix 3 preservation.
      2. `undischarged_count == 0` overall — Layer 5 demotes the 8
         in-milestone H3-subsection surfacings (Risk Assessment /
         Integration Points / Milestone Dependencies) that Fix 1 + Fix 3
         revealed but did not demote on their own.
    """

    def test_e2e_multimodelswarm_original_six_fps_resolved(self):
        from pathlib import Path

        roadmap_path = Path(".dev/releases/Current/MultiModelSwarm/roadmap.md")
        if not roadmap_path.exists():
            pytest.skip(f"MultiModelSwarm roadmap fixture missing at {roadmap_path}")

        content = roadmap_path.read_text()
        report = scan_obligations(content)

        original_fp_lines = {311, 519, 529, 541, 553, 600}
        flagged_lines = {
            o.line_number
            for o in report.obligations
            if not o.discharged and not o.exempt and o.severity != "MEDIUM"
        }
        # None of the original 6 false-positive lines should remain in the
        # undischarged set.
        remaining_originals = original_fp_lines & flagged_lines
        assert not remaining_originals, (
            "Original false-positive lines still flagged: "
            f"{sorted(remaining_originals)}"
        )

        # Layer 5 contract: zero undischarged findings overall.
        undischarged = [
            o
            for o in report.obligations
            if not o.discharged and not o.exempt and o.severity != "MEDIUM"
        ]
        diagnostic = "\n".join(
            f"  L{o.line_number:>4}  {o.term:<12}  phase={o.phase!r}  ctx={o.context[:80]!r}"
            for o in undischarged
        )
        assert report.undischarged_count == 0, (
            f"Expected undischarged_count == 0 on MultiModelSwarm roadmap, "
            f"got {report.undischarged_count}. Remaining undischarged:\n{diagnostic}"
        )
