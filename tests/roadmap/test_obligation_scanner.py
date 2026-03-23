"""Unit tests for obligation_scanner.py.

Tests cover:
1. Scaffold term detection for all 11 terms (FR-MOD1.1)
2. Cross-phase discharge matching (FR-MOD1.3, FR-MOD1.5)
3. `# obligation-exempt` comment parsing (FR-MOD1.7)
4. Code-block severity demotion to MEDIUM (FR-MOD1.8)
5. cli-portify regression case SC-002

All tests use real content fixtures, no mocks.
"""

from superclaude.cli.roadmap.obligation_scanner import (
    Obligation,
    ObligationReport,
    scan_obligations,
)


# --- Real content fixtures ---

MULTI_PHASE_ROADMAP = """\
## Phase 1: Skeleton Implementation

Build the executor skeleton with **mocked steps** for initial testing.
Use `placeholder` config values for database connections.
Create a stub authentication module.

## Phase 2: Core Logic

Implement the core processing engine with temporary hardcoded thresholds.
Add a dummy logger for debugging. Use a fake service client for external calls.
The scaffolding for the CLI will use a no-op handler initially.

## Phase 3: Integration

Replace mock steps with real implementations.
Wire up the `placeholder` config to actual environment variables.
Integrate the real authentication module, replacing the stub.
Connect the real service client, swap out the fake.
Fill in the no-op handler with actual logic.
"""

UNDISCHARGED_ROADMAP = """\
## Phase 1: Setup

Build executor with **mocked steps** for the pipeline.

## Phase 2: Features

Add feature A and feature B.

## Phase 3: Testing

Run integration tests.
"""

EXEMPT_ROADMAP = """\
## Phase 1: Test Infrastructure

Set up test doubles with mocked services. # obligation-exempt
Use stub clients for unit tests. # obligation-exempt

## Phase 2: Implementation

Implement the actual services.
"""

CODE_BLOCK_ROADMAP = """\
## Phase 1: Design

Here is the test approach:

```python
# Use mocked database for testing
db = MockDatabase()
stub_client = StubClient()
```

## Phase 2: Implementation

Build the real database layer.
"""

CLI_PORTIFY_REGRESSION = """\
## Phase 1: Foundation

Set up project structure and configuration.

## Phase 2: Executor Shell

Implement executor: sequential execution only, `--dry-run`, `--resume <step-id>`, signal handling.

Milestone M2: Sequential pipeline runs end-to-end with **mocked steps**.

## Phase 3: CLI Polish

Add rich output formatting and progress display.
"""


class TestScaffoldTermDetection:
    """FR-MOD1.1: All 11 scaffold terms detected."""

    def test_detects_mock(self):
        content = "## Phase 1: Setup\nUse mock data for testing.\n## Phase 2: Build\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1
        terms = [o.term.lower() for o in report.obligations]
        assert any("mock" in t for t in terms)

    def test_detects_mocked(self):
        content = "## Phase 1\nWith mocked steps.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_stub(self):
        content = "## Phase 1\nCreate stub module.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_stubbed(self):
        content = "## Phase 1\nUse stubbed endpoint.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_skeleton(self):
        content = "## Phase 1\nBuild skeleton framework.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_placeholder(self):
        content = "## Phase 1\nAdd placeholder values.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_scaffold(self):
        content = "## Phase 1\nSet up scaffolding.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_temporary(self):
        content = "## Phase 1\nUse temporary storage.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_hardcoded(self):
        content = "## Phase 1\nWith hardcoded limits.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_noop(self):
        content = "## Phase 1\nUse no-op handler.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_dummy(self):
        content = "## Phase 1\nAdd dummy logger.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_fake(self):
        content = "## Phase 1\nUse fake client.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1

    def test_detects_hardwired(self):
        content = "## Phase 1\nHardwired config.\n## Phase 2\nDone."
        report = scan_obligations(content)
        assert report.total_obligations >= 1


class TestDischargeMatching:
    """FR-MOD1.3, FR-MOD1.5: Cross-phase discharge with dual condition."""

    def test_discharged_obligations_in_later_phase(self):
        report = scan_obligations(MULTI_PHASE_ROADMAP)
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
        # "mocked steps" should be undischarged since Phase 2/3 don't discharge it
        terms = [o.term.lower() for o in undischarged]
        assert any("mock" in t for t in terms)

    def test_discharge_phase_recorded(self):
        report = scan_obligations(MULTI_PHASE_ROADMAP)
        discharged = [o for o in report.obligations if o.discharged]
        for o in discharged:
            assert o.discharge_phase is not None

    def test_all_discharged_in_complete_roadmap(self):
        report = scan_obligations(MULTI_PHASE_ROADMAP)
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
## Phase 1: Setup
Use mocked data for testing.

## Phase 2: Done
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
        content = "## Phase 1\nUse mocked data.\n## Phase 2\nDone."
        report = scan_obligations(content)
        high = [o for o in report.obligations if o.severity == "HIGH"]
        assert len(high) >= 1

    def test_medium_excluded_from_undischarged_count(self):
        report = scan_obligations(CODE_BLOCK_ROADMAP)
        # MEDIUM obligations should not count toward undischarged_count
        medium_undischarged = [
            o
            for o in report.obligations
            if not o.discharged and o.severity == "MEDIUM"
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


class TestCliPortifyRegression:
    """SC-002: Detects 'mocked steps' without discharge at >= 85% confidence."""

    def test_detects_mocked_steps_without_discharge(self):
        report = scan_obligations(CLI_PORTIFY_REGRESSION)
        # The roadmap mentions "mocked steps" in Phase 2 but never discharges
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
        report = scan_obligations(MULTI_PHASE_ROADMAP)
        assert report.total_obligations == report.discharged + report.undischarged


class TestPhaseParsing:
    """FR-MOD1.2: Phase-section parser with H2/H3 fallback."""

    def test_h2_phases_detected(self):
        report = scan_obligations(MULTI_PHASE_ROADMAP)
        phases = {o.phase for o in report.obligations}
        assert len(phases) >= 2  # At least Phase 1 and Phase 2

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
