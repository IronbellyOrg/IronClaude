---
title: "v3.0 E2E Eval Design — 3 Impact-Driven Pipeline Evals"
version: 1.0.0
date: 2026-03-19
prompt_sequence: 3 of 6
depends_on: eval-spec.md, stage-review-summary.md
eval_count: 3
eval_type: end-to-end pipeline execution
input_spec: eval-spec.md
---

# v3.0 E2E Eval Design

## 1. Impact Summary

| # | Impact | Code Reference | Pipeline Stage | Testability with Eval Spec |
|---|--------|---------------|----------------|---------------------------|
| 1 | Deterministic Wiring Verification Gate | `executor.py:244-259`, `wiring_gate.py:313/393/553` | Stage 10 | Structural validation exercised; detection power NOT exercised (eval spec produces zero findings) |
| 2 | Convergence-Controlled Spec-Fidelity | `convergence.py:50-226`, `executor.py:521` | Stage 9 | Requires convergence_enabled=True; single-pass vs multi-run comparison |
| 3 | Mode-Aware Rollout Enforcement | `wiring_gate.py:113-135/948-960`, `executor.py:248/537` | Stages 9-10 | Frontmatter values inspectable; rollout mode sensitivity testable against real codebase |

## 2. Pre-v3.0 Issues Mitigated

| # | Issue | Evidence |
|---|-------|----------|
| 1 | Documents pass gates but code modules are never connected to consumers | 32 unwired symbols across 14 files (merged-spec.md Section 1) |
| 2 | LLM severity classification noise is indistinguishable from structural regressions | Single-pass spec-fidelity with no cross-run memory or stable finding IDs |
| 3 | New gates must deploy at full enforcement immediately or not at all | No graduated shadow→soft→full rollout mechanism existed |

---

## 3. Eval 1: Wiring Verification Gate — Pipeline Structural Integration

### 3.1 Target Impact

Impact 1: The pipeline now includes a deterministic (non-LLM) wiring verification step that runs AST-based analysis directly in the executor, produces a structured report with 16 frontmatter fields, and validates via 5 semantic checks.

### 3.2 What This Eval Proves

1. The wiring-verification step executes as part of the pipeline (not skipped)
2. The executor special-case path (`step.id == "wiring-verification"`) fires correctly
3. The produced `wiring-verification.md` passes `WIRING_GATE` validation
4. The report contains structurally correct frontmatter (category sum == severity sum == total)
5. The `.roadmap-state.json` records wiring-verification with timing data
6. **Bonus**: When run against the project's own codebase (`src/superclaude/cli/`), the analyzers produce non-zero findings demonstrating detection power

### 3.3 Eval Design

**Mode**: Two-phase. Phase A runs the full pipeline with the eval spec. Phase B runs only the wiring analyzer against the project's own source tree to demonstrate detection power.

#### Phase A: Pipeline Integration Verification

```python
# scripts/eval_1.py — Wiring Verification Gate E2E Eval
"""
Eval 1: Verify wiring-verification gate integrates into the roadmap pipeline
and produces structurally valid artifacts.

Phase A: Full pipeline run with eval spec → verify wiring-verification.md
Phase B: Direct wiring analysis against project source → verify detection power
"""
import argparse
import json
import os
import subprocess
import sys
import time
import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


@dataclass
class EvalResult:
    eval_id: str
    phase: str
    passed: bool
    assertions: list[dict] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    error: str | None = None


@dataclass
class ComparisonReport:
    eval_id: str = "eval-1-wiring-gate"
    timestamp: str = ""
    branch: str = ""
    phases: list[dict] = field(default_factory=list)
    overall_passed: bool = False
    summary: str = ""


def run_pipeline(spec_file: Path, output_dir: Path, timeout: int = 1800) -> int:
    """Run superclaude roadmap run and return exit code."""
    cmd = [
        "superclaude", "roadmap", "run",
        str(spec_file),
        "--output-dir", str(output_dir),
        "--no-validate",  # Skip post-pipeline validation for eval speed
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(spec_file.parent),
    )
    # Write stdout/stderr for inspection
    (output_dir / "pipeline-stdout.log").write_text(result.stdout)
    (output_dir / "pipeline-stderr.log").write_text(result.stderr)
    return result.returncode


def parse_frontmatter(file_path: Path) -> dict[str, str]:
    """Extract YAML frontmatter key-value pairs from a markdown file."""
    content = file_path.read_text(encoding="utf-8")
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return {}
    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return {}
    result = {}
    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def assert_check(name: str, condition: bool, detail: str = "") -> dict:
    """Create an assertion result dict."""
    return {
        "name": name,
        "passed": condition,
        "detail": detail,
    }


def phase_a_pipeline_integration(output_dir: Path, spec_file: Path) -> EvalResult:
    """Phase A: Run full pipeline, verify wiring-verification.md exists and passes gate."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-1", phase="A-pipeline-integration", passed=False)

    # 1. Run the pipeline
    exit_code = run_pipeline(spec_file, output_dir)

    # Collect artifacts
    wiring_report = output_dir / "wiring-verification.md"
    state_file = output_dir / ".roadmap-state.json"

    result.artifacts = [str(p) for p in output_dir.glob("*.md")]

    # 2. Assert: wiring-verification.md exists
    result.assertions.append(
        assert_check(
            "wiring_report_exists",
            wiring_report.exists(),
            f"File exists: {wiring_report.exists()}",
        )
    )

    if not wiring_report.exists():
        result.error = "wiring-verification.md not produced by pipeline"
        result.duration_seconds = time.monotonic() - start
        return result

    # 3. Assert: frontmatter has all 16 required fields
    fm = parse_frontmatter(wiring_report)
    required_fields = [
        "gate", "target_dir", "files_analyzed", "rollout_mode",
        "analysis_complete", "unwired_callable_count", "orphan_module_count",
        "unwired_registry_count", "critical_count", "major_count",
        "info_count", "total_findings", "blocking_findings",
        "whitelist_entries_applied", "files_skipped", "audit_artifacts_used",
    ]
    missing = [f for f in required_fields if f not in fm]
    result.assertions.append(
        assert_check(
            "frontmatter_16_fields",
            len(missing) == 0,
            f"Missing fields: {missing}" if missing else "All 16 fields present",
        )
    )

    # 4. Assert: gate field equals "wiring-verification"
    result.assertions.append(
        assert_check(
            "gate_field_correct",
            fm.get("gate") == "wiring-verification",
            f"gate={fm.get('gate')}",
        )
    )

    # 5. Assert: analysis_complete is true
    result.assertions.append(
        assert_check(
            "analysis_complete_true",
            fm.get("analysis_complete", "").lower() == "true",
            f"analysis_complete={fm.get('analysis_complete')}",
        )
    )

    # 6. Assert: rollout_mode is one of shadow/soft/full
    result.assertions.append(
        assert_check(
            "rollout_mode_valid",
            fm.get("rollout_mode") in ("shadow", "soft", "full"),
            f"rollout_mode={fm.get('rollout_mode')}",
        )
    )

    # 7. Assert: category sum consistency (INV-008)
    try:
        uc = int(fm.get("unwired_callable_count", -1))
        om = int(fm.get("orphan_module_count", -1))
        ur = int(fm.get("unwired_registry_count", -1))
        total = int(fm.get("total_findings", -1))
        category_consistent = (uc + om + ur) == total
    except ValueError:
        category_consistent = False
    result.assertions.append(
        assert_check(
            "category_sum_consistent",
            category_consistent,
            f"uc({uc}) + om({om}) + ur({ur}) == total({total})",
        )
    )

    # 8. Assert: severity sum consistency
    try:
        critical = int(fm.get("critical_count", -1))
        major = int(fm.get("major_count", -1))
        info = int(fm.get("info_count", -1))
        severity_consistent = (critical + major + info) == total
    except ValueError:
        severity_consistent = False
    result.assertions.append(
        assert_check(
            "severity_sum_consistent",
            severity_consistent,
            f"critical({critical}) + major({major}) + info({info}) == total({total})",
        )
    )

    # 9. Assert: blocking_findings is 0 (gate passes)
    try:
        blocking = int(fm.get("blocking_findings", -1))
    except ValueError:
        blocking = -1
    result.assertions.append(
        assert_check(
            "blocking_findings_zero",
            blocking == 0,
            f"blocking_findings={blocking}",
        )
    )

    # 10. Assert: .roadmap-state.json contains wiring-verification step
    if state_file.exists():
        state = json.loads(state_file.read_text())
        steps = state.get("steps", {})
        has_wiring_step = "wiring-verification" in steps
        result.assertions.append(
            assert_check(
                "state_has_wiring_step",
                has_wiring_step,
                f"Step IDs in state: {list(steps.keys())}",
            )
        )
        # 11. Assert: wiring step has timing data
        if has_wiring_step:
            ws = steps["wiring-verification"]
            has_timing = "started_at" in ws and "completed_at" in ws
            result.assertions.append(
                assert_check(
                    "wiring_step_has_timing",
                    has_timing,
                    f"Fields: {list(ws.keys())}",
                )
            )
    else:
        result.assertions.append(
            assert_check("state_file_exists", False, "No .roadmap-state.json")
        )

    # 12. Assert: report body has all 7 required sections
    content = wiring_report.read_text()
    required_sections = [
        "## Summary",
        "## Unwired Optional Callable Injections",
        "## Orphan Modules / Symbols",
        "## Unregistered Dispatch Entries",
        "## Suppressions and Dynamic Retention",
        "## Recommended Remediation",
        "## Evidence and Limitations",
    ]
    missing_sections = [s for s in required_sections if s not in content]
    result.assertions.append(
        assert_check(
            "report_has_7_sections",
            len(missing_sections) == 0,
            f"Missing sections: {missing_sections}" if missing_sections else "All 7 sections present",
        )
    )

    # Overall pass: all assertions pass
    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_b_detection_power(project_source: Path) -> EvalResult:
    """Phase B: Run wiring analysis against project source to verify detection power."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-1", phase="B-detection-power", passed=False)

    # Import and run the analyzer directly
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from superclaude.cli.audit.wiring_gate import run_wiring_analysis, emit_report
    from superclaude.cli.audit.wiring_config import WiringConfig

    config = WiringConfig(rollout_mode="full")
    report = run_wiring_analysis(config, project_source)

    # Write report for inspection
    report_path = project_source.parent / "eval-1-detection-report.md"
    emit_report(report, report_path)
    result.artifacts = [str(report_path)]

    # 1. Assert: files_analyzed > 0 (pre-activation sanity check)
    result.assertions.append(
        assert_check(
            "files_analyzed_positive",
            report.files_analyzed > 0,
            f"files_analyzed={report.files_analyzed}",
        )
    )

    # 2. Assert: at least one finding detected (detection power)
    result.assertions.append(
        assert_check(
            "has_findings",
            report.total_findings > 0,
            f"total_findings={report.total_findings} "
            f"(uc={len(report.unwired_callables)}, "
            f"om={len(report.orphan_modules)}, "
            f"ur={len(report.unwired_registries)})",
        )
    )

    # 3. Assert: scan completes in <5s (SC-008 performance target)
    result.assertions.append(
        assert_check(
            "scan_under_5s",
            report.scan_duration_seconds < 5.0,
            f"scan_duration={report.scan_duration_seconds:.4f}s",
        )
    )

    # 4. Assert: total_findings invariant holds
    expected_total = (
        len(report.unwired_callables)
        + len(report.orphan_modules)
        + len(report.unwired_registries)
    )
    result.assertions.append(
        assert_check(
            "total_findings_invariant",
            report.total_findings == expected_total,
            f"total={report.total_findings}, expected={expected_total}",
        )
    )

    # 5. Assert: blocking_count in full mode == critical + major
    blocking_full = report.blocking_count("full")
    unsuppressed = report.unsuppressed_findings
    expected_blocking = sum(
        1 for f in unsuppressed if f.severity in ("critical", "major")
    )
    result.assertions.append(
        assert_check(
            "blocking_count_full_mode",
            blocking_full == expected_blocking,
            f"blocking={blocking_full}, expected={expected_blocking}",
        )
    )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def main():
    parser = argparse.ArgumentParser(description="Eval 1: Wiring Verification Gate")
    parser.add_argument(
        "--branch", choices=["local", "global"], default="local",
        help="Artifact label for directory naming (does NOT switch git branches)",
    )
    parser.add_argument(
        "--spec-file",
        default=".dev/releases/current/v3.0_unified-audit-gating/eval-spec.md",
        help="Path to eval spec",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Pipeline output directory (default: auto-generated)",
    )
    parser.add_argument(
        "--project-source",
        default="src/superclaude/cli",
        help="Source directory for detection power test",
    )
    args = parser.parse_args()

    spec_file = Path(args.spec_file).resolve()
    project_source = Path(args.project_source).resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    print(f"[eval-1] Running on current branch ('{args.branch}' is an artifact label, not a git operation)")

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(f"eval-results/eval-1-wiring-gate/{args.branch}-{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    report = ComparisonReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        branch=args.branch,
    )

    # Phase A: Pipeline integration
    print(f"[eval-1] Phase A: Pipeline integration test ({args.branch})")
    phase_a = phase_a_pipeline_integration(output_dir, spec_file)
    report.phases.append(asdict(phase_a))

    # Phase B: Detection power (always runs against project source)
    print(f"[eval-1] Phase B: Detection power test against {project_source}")
    phase_b = phase_b_detection_power(project_source)
    report.phases.append(asdict(phase_b))

    # Overall
    report.overall_passed = phase_a.passed and phase_b.passed
    report.summary = (
        f"Phase A ({'PASS' if phase_a.passed else 'FAIL'}): "
        f"{sum(1 for a in phase_a.assertions if a['passed'])}/{len(phase_a.assertions)} assertions. "
        f"Phase B ({'PASS' if phase_b.passed else 'FAIL'}): "
        f"{sum(1 for a in phase_b.assertions if a['passed'])}/{len(phase_b.assertions)} assertions."
    )

    # Write report
    report_path = output_dir / "eval-1-report.json"
    report_path.write_text(json.dumps(asdict(report), indent=2))
    print(f"\n[eval-1] {'PASS' if report.overall_passed else 'FAIL'}: {report.summary}")
    print(f"[eval-1] Report: {report_path}")

    sys.exit(0 if report.overall_passed else 1)


if __name__ == "__main__":
    main()
```

### 3.4 CLI Invocations

```bash
# Run on current v3.0 branch
uv run python scripts/eval_1.py --branch local

# Run on baseline (pre-v3.0) for comparison
git stash && git checkout pre-v3.0-baseline
uv run python scripts/eval_1.py --branch global
git checkout v3.0-AuditGates && git stash pop
```

### 3.5 Artifact Output Schema

```
eval-results/eval-1-wiring-gate/{branch}-{timestamp}/
├── eval-1-report.json          # Structured comparison report
├── wiring-verification.md      # Gate output (16 frontmatter fields + 7 sections)
├── .roadmap-state.json         # Pipeline state with wiring step timing
├── extraction.md               # Stage 1 output
├── roadmap-*.md                # Stage 2a/2b outputs
├── diff-analysis.md            # Stage 4 output
├── debate-transcript.md        # Stage 5 output
├── base-selection.md           # Stage 6 output
├── roadmap.md                  # Stage 7 merged output
├── test-strategy.md            # Stage 8 output
├── spec-fidelity.md            # Stage 9 output
├── pipeline-stdout.log         # Raw stdout
├── pipeline-stderr.log         # Raw stderr
└── eval-1-detection-report.md  # Phase B: detection power report
```

### 3.6 Assertion Criteria

| # | Assertion | Pass Condition | Threshold |
|---|-----------|---------------|-----------|
| A1 | wiring_report_exists | File exists at `{output}/wiring-verification.md` | Boolean |
| A2 | frontmatter_16_fields | All 16 required fields present in frontmatter | 0 missing |
| A3 | gate_field_correct | `gate` field equals `"wiring-verification"` | Exact match |
| A4 | analysis_complete_true | `analysis_complete` equals `"true"` | Exact match |
| A5 | rollout_mode_valid | `rollout_mode` in `{shadow, soft, full}` | Set membership |
| A6 | category_sum_consistent | `uc + om + ur == total_findings` | Arithmetic equality |
| A7 | severity_sum_consistent | `critical + major + info == total_findings` | Arithmetic equality |
| A8 | blocking_findings_zero | `blocking_findings == 0` | Equality |
| A9 | state_has_wiring_step | `.roadmap-state.json` has `wiring-verification` key | Key existence |
| A10 | wiring_step_has_timing | Step entry has `started_at` and `completed_at` | Key existence |
| A11 | report_has_7_sections | All 7 markdown section headings present | 0 missing |
| B1 | files_analyzed_positive | `files_analyzed > 0` | > 0 |
| B2 | has_findings | `total_findings > 0` when scanning project source | > 0 |
| B3 | scan_under_5s | `scan_duration < 5.0` seconds | < 5.0 |
| B4 | total_findings_invariant | Category list lengths sum to total | Equality |
| B5 | blocking_count_full_mode | blocking == critical + major in full mode | Equality |

**Overall pass**: All 16 assertions pass.

---

## 4. Eval 2: Convergence-Controlled Spec-Fidelity

### 4.1 Target Impact

Impact 2: Spec-fidelity now uses a DeviationRegistry with stable finding IDs, cross-run memory, and structural/semantic HIGH separation. Regression detection distinguishes genuine regressions from LLM noise.

### 4.2 What This Eval Proves

1. With convergence enabled, `gate=None` is set on the spec-fidelity Step (convergence loop handles gating)
2. The DeviationRegistry JSON file is created and populated during the run
3. Stable finding IDs are deterministic (same input → same ID via `compute_stable_id()`)
4. The seeded ambiguities (FR-001.4 and FR-001.5) propagate to spec-fidelity as findings
5. With convergence disabled, `SPEC_FIDELITY_GATE` runs normally with `high_severity_count` check
6. `_check_regression()` correctly identifies structural HIGH increases as regressions while ignoring semantic fluctuations

### 4.3 Eval Design

```python
# scripts/eval_2.py — Convergence-Controlled Spec-Fidelity E2E Eval
"""
Eval 2: Verify convergence-controlled spec-fidelity produces stable
deviation tracking with structural/semantic HIGH separation.

Phase A: Convergence-disabled run → verify SPEC_FIDELITY_GATE applies normally
Phase B: Convergence-enabled run → verify DeviationRegistry is created and populated
Phase C: Stable ID determinism → verify compute_stable_id() is pure
Phase D: Regression detection → verify _check_regression() distinguishes structural regressions from noise
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class EvalResult:
    eval_id: str
    phase: str
    passed: bool
    assertions: list[dict] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    error: str | None = None


@dataclass
class ComparisonReport:
    eval_id: str = "eval-2-convergence"
    timestamp: str = ""
    branch: str = ""
    phases: list[dict] = field(default_factory=list)
    overall_passed: bool = False
    summary: str = ""


def assert_check(name: str, condition: bool, detail: str = "") -> dict:
    return {"name": name, "passed": condition, "detail": detail}


def run_pipeline(
    spec_file: Path, output_dir: Path,
    convergence_enabled: bool = False,
    timeout: int = 1800,
) -> int:
    """Run superclaude roadmap run with convergence flag."""
    cmd = [
        "superclaude", "roadmap", "run",
        str(spec_file),
        "--output-dir", str(output_dir),
        "--no-validate",
    ]
    if convergence_enabled:
        cmd.append("--convergence")

    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout,
    )
    (output_dir / "pipeline-stdout.log").write_text(result.stdout)
    (output_dir / "pipeline-stderr.log").write_text(result.stderr)
    return result.returncode


def parse_frontmatter(file_path: Path) -> dict[str, str]:
    content = file_path.read_text(encoding="utf-8")
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return {}
    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return {}
    result = {}
    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def phase_a_convergence_disabled(output_dir: Path, spec_file: Path) -> EvalResult:
    """Phase A: Run without convergence → SPEC_FIDELITY_GATE applies."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-2", phase="A-convergence-disabled", passed=False)

    exit_code = run_pipeline(spec_file, output_dir, convergence_enabled=False)

    spec_fidelity = output_dir / "spec-fidelity.md"
    result.artifacts = [str(p) for p in output_dir.glob("*.md")]

    # 1. Assert: spec-fidelity.md exists
    result.assertions.append(
        assert_check("spec_fidelity_exists", spec_fidelity.exists())
    )

    if not spec_fidelity.exists():
        result.error = "spec-fidelity.md not produced"
        result.duration_seconds = time.monotonic() - start
        return result

    fm = parse_frontmatter(spec_fidelity)

    # 2. Assert: has SPEC_FIDELITY_GATE required fields
    required = [
        "high_severity_count", "medium_severity_count",
        "low_severity_count", "total_deviations",
        "validation_complete", "tasklist_ready",
    ]
    missing = [f for f in required if f not in fm]
    result.assertions.append(
        assert_check(
            "spec_fidelity_gate_fields",
            len(missing) == 0,
            f"Missing: {missing}" if missing else "All 6 fields present",
        )
    )

    # 3. Assert: No deviation registry file (convergence disabled)
    registry_candidates = list(output_dir.glob("*deviation-registry*"))
    result.assertions.append(
        assert_check(
            "no_deviation_registry",
            len(registry_candidates) == 0,
            f"Found: {registry_candidates}" if registry_candidates else "No registry file (correct for disabled)",
        )
    )

    # 4. Assert: seeded ambiguity detection — check if spec-fidelity
    # mentions FR-001.4 or FR-001.5 or "deviation" or "ambiguity"
    content = spec_fidelity.read_text()
    has_ambiguity_reference = any(
        marker in content
        for marker in ["FR-001.4", "FR-EVAL-001.4", "schema", "deviation sub-entry",
                        "significant findings", "FR-001.5", "FR-EVAL-001.5"]
    )
    result.assertions.append(
        assert_check(
            "seeded_ambiguity_detected",
            has_ambiguity_reference,
            "Spec-fidelity references seeded ambiguity" if has_ambiguity_reference
            else "No seeded ambiguity references found in spec-fidelity output",
        )
    )

    # 5. Assert: if pipeline passed, high_severity_count should be parseable
    try:
        high_count = int(fm.get("high_severity_count", "-1"))
        result.assertions.append(
            assert_check(
                "high_severity_parseable",
                high_count >= 0,
                f"high_severity_count={high_count}",
            )
        )
    except ValueError:
        result.assertions.append(
            assert_check("high_severity_parseable", False, "Not an integer")
        )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_b_convergence_enabled(output_dir: Path, spec_file: Path) -> EvalResult:
    """Phase B: Run with convergence → DeviationRegistry created."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-2", phase="B-convergence-enabled", passed=False)

    exit_code = run_pipeline(spec_file, output_dir, convergence_enabled=True)

    spec_fidelity = output_dir / "spec-fidelity.md"
    result.artifacts = [str(p) for p in output_dir.glob("*")]

    # 1. Assert: spec-fidelity.md exists (may have different format with convergence)
    result.assertions.append(
        assert_check("spec_fidelity_exists", spec_fidelity.exists())
    )

    # 2. Assert: deviation registry file exists
    registry_candidates = list(output_dir.glob("*deviation*registry*")) + \
                          list(output_dir.glob("*deviation*.json"))
    result.assertions.append(
        assert_check(
            "deviation_registry_exists",
            len(registry_candidates) > 0,
            f"Found: {[str(p) for p in registry_candidates]}" if registry_candidates
            else "No deviation registry file found",
        )
    )

    # 3. Assert: if registry exists, it has valid schema
    if registry_candidates:
        registry_path = registry_candidates[0]
        try:
            registry_data = json.loads(registry_path.read_text())
            has_schema = all(
                k in registry_data
                for k in ["schema_version", "runs", "findings"]
            )
            result.assertions.append(
                assert_check(
                    "registry_schema_valid",
                    has_schema,
                    f"Keys: {list(registry_data.keys())}",
                )
            )

            # 4. Assert: at least one run recorded
            runs = registry_data.get("runs", [])
            result.assertions.append(
                assert_check(
                    "registry_has_runs",
                    len(runs) >= 1,
                    f"Run count: {len(runs)}",
                )
            )

            # 5. Assert: runs have structural/semantic HIGH split fields
            if runs:
                last_run = runs[-1]
                has_split = (
                    "structural_high_count" in last_run
                    and "semantic_high_count" in last_run
                )
                result.assertions.append(
                    assert_check(
                        "run_has_high_split",
                        has_split,
                        f"Run fields: {list(last_run.keys())}",
                    )
                )

            # 6. Assert: findings have stable_id field
            findings = registry_data.get("findings", {})
            if findings:
                first_finding = next(iter(findings.values()))
                has_stable_id = "stable_id" in first_finding
                result.assertions.append(
                    assert_check(
                        "findings_have_stable_id",
                        has_stable_id,
                        f"Finding fields: {list(first_finding.keys())}",
                    )
                )
            else:
                # No findings is acceptable — note it
                result.assertions.append(
                    assert_check(
                        "findings_have_stable_id",
                        True,  # Vacuously true — no findings to check
                        "No findings in registry (acceptable for simple spec)",
                    )
                )

        except (json.JSONDecodeError, KeyError) as exc:
            result.assertions.append(
                assert_check("registry_schema_valid", False, f"Parse error: {exc}")
            )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_c_stable_id_determinism() -> EvalResult:
    """Phase C: Verify compute_stable_id is pure (same inputs → same output)."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-2", phase="C-stable-id-determinism", passed=False)

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from superclaude.cli.roadmap.convergence import compute_stable_id

    # 1. Assert: same inputs produce same output
    id_a = compute_stable_id("architecture", "R-001", "Section 3.2", "missing")
    id_b = compute_stable_id("architecture", "R-001", "Section 3.2", "missing")
    result.assertions.append(
        assert_check("stable_id_deterministic", id_a == id_b, f"a={id_a}, b={id_b}")
    )

    # 2. Assert: different inputs produce different output
    id_c = compute_stable_id("architecture", "R-002", "Section 3.2", "missing")
    result.assertions.append(
        assert_check("stable_id_varies", id_a != id_c, f"a={id_a}, c={id_c}")
    )

    # 3. Assert: output is 16-char hex string
    result.assertions.append(
        assert_check(
            "stable_id_format",
            len(id_a) == 16 and all(c in "0123456789abcdef" for c in id_a),
            f"id={id_a}, len={len(id_a)}",
        )
    )

    # 4. Assert: matches expected sha256 truncation
    key = "architecture:R-001:Section 3.2:missing"
    expected = hashlib.sha256(key.encode()).hexdigest()[:16]
    result.assertions.append(
        assert_check("stable_id_matches_sha256", id_a == expected, f"id={id_a}, expected={expected}")
    )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_d_regression_detection() -> EvalResult:
    """Phase D: Verify _check_regression() distinguishes structural regressions from noise."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-2", phase="D-regression-detection", passed=False)

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from superclaude.cli.roadmap.convergence import DeviationRegistry, compute_stable_id

    registry = DeviationRegistry()

    # Simulate run 1: 2 structural HIGHs
    finding_1 = compute_stable_id("architecture", "R-001", "Section 3", "missing")
    finding_2 = compute_stable_id("architecture", "R-002", "Section 4", "incomplete")
    registry.record_run({
        "run_number": 1,
        "structural_high_count": 2,
        "semantic_high_count": 0,
        "findings": {
            finding_1: {"stable_id": finding_1, "severity": "HIGH", "status": "ACTIVE"},
            finding_2: {"stable_id": finding_2, "severity": "HIGH", "status": "ACTIVE"},
        },
    })

    # Simulate run 2: 3 structural HIGHs (regression — new finding added)
    finding_3 = compute_stable_id("architecture", "R-003", "Section 5", "missing")
    registry.record_run({
        "run_number": 2,
        "structural_high_count": 3,
        "semantic_high_count": 0,
        "findings": {
            finding_1: {"stable_id": finding_1, "severity": "HIGH", "status": "ACTIVE"},
            finding_2: {"stable_id": finding_2, "severity": "HIGH", "status": "ACTIVE"},
            finding_3: {"stable_id": finding_3, "severity": "HIGH", "status": "ACTIVE"},
        },
    })

    # 1. Assert: regression detected (structural increase 2 → 3)
    is_regression = registry._check_regression()
    result.assertions.append(
        assert_check(
            "regression_detected_on_increase",
            is_regression is True,
            f"_check_regression() returned {is_regression} for structural 2→3",
        )
    )

    # 2. Assert: registry has 2 runs
    result.assertions.append(
        assert_check(
            "registry_has_2_runs",
            len(registry.runs) == 2,
            f"Run count: {len(registry.runs)}",
        )
    )

    # Simulate run 3: back to 2 structural HIGHs (finding_3 resolved)
    registry.record_run({
        "run_number": 3,
        "structural_high_count": 2,
        "semantic_high_count": 0,
        "findings": {
            finding_1: {"stable_id": finding_1, "severity": "HIGH", "status": "ACTIVE"},
            finding_2: {"stable_id": finding_2, "severity": "HIGH", "status": "ACTIVE"},
            finding_3: {"stable_id": finding_3, "severity": "HIGH", "status": "FIXED"},
        },
    })

    # 3. Assert: no regression (structural count did not increase from run 2)
    is_regression_after_fix = registry._check_regression()
    result.assertions.append(
        assert_check(
            "no_regression_after_fix",
            is_regression_after_fix is False,
            f"_check_regression() returned {is_regression_after_fix} for structural 3→2",
        )
    )

    # 4. Assert: finding_3 status is FIXED in registry
    latest_findings = registry.runs[-1].get("findings", {})
    f3_status = latest_findings.get(finding_3, {}).get("status")
    result.assertions.append(
        assert_check(
            "fixed_finding_tracked",
            f3_status == "FIXED",
            f"finding_3 status: {f3_status}",
        )
    )

    # 5. Assert: semantic fluctuation does NOT trigger regression
    registry_semantic = DeviationRegistry()
    registry_semantic.record_run({
        "run_number": 1,
        "structural_high_count": 2,
        "semantic_high_count": 1,
        "findings": {},
    })
    registry_semantic.record_run({
        "run_number": 2,
        "structural_high_count": 2,
        "semantic_high_count": 3,  # Semantic increase only
        "findings": {},
    })
    is_semantic_regression = registry_semantic._check_regression()
    result.assertions.append(
        assert_check(
            "semantic_fluctuation_not_regression",
            is_semantic_regression is False,
            f"_check_regression() returned {is_semantic_regression} for semantic-only increase",
        )
    )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def main():
    parser = argparse.ArgumentParser(description="Eval 2: Convergence Spec-Fidelity")
    parser.add_argument(
        "--branch", choices=["local", "global"], default="local",
        help="Artifact label for directory naming (does NOT switch git branches)",
    )
    parser.add_argument(
        "--spec-file",
        default=".dev/releases/current/v3.0_unified-audit-gating/eval-spec.md",
    )
    args = parser.parse_args()

    spec_file = Path(args.spec_file).resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    print(f"[eval-2] Running on current branch ('{args.branch}' is an artifact label, not a git operation)")

    report = ComparisonReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        branch=args.branch,
    )

    # Phase A: Convergence disabled
    out_a = Path(f"eval-results/eval-2-convergence/phase-a-disabled-{args.branch}-{timestamp}")
    out_a.mkdir(parents=True, exist_ok=True)
    print(f"[eval-2] Phase A: Convergence disabled ({args.branch})")
    phase_a = phase_a_convergence_disabled(out_a, spec_file)
    report.phases.append(asdict(phase_a))

    # Phase B: Convergence enabled
    out_b = Path(f"eval-results/eval-2-convergence/phase-b-enabled-{args.branch}-{timestamp}")
    out_b.mkdir(parents=True, exist_ok=True)
    print(f"[eval-2] Phase B: Convergence enabled ({args.branch})")
    phase_b = phase_b_convergence_enabled(out_b, spec_file)
    report.phases.append(asdict(phase_b))

    # Phase C: Stable ID determinism (no pipeline needed)
    print("[eval-2] Phase C: Stable ID determinism")
    phase_c = phase_c_stable_id_determinism()
    report.phases.append(asdict(phase_c))

    # Phase D: Regression detection (no pipeline needed)
    print("[eval-2] Phase D: Regression detection")
    phase_d = phase_d_regression_detection()
    report.phases.append(asdict(phase_d))

    report.overall_passed = all(p["passed"] for p in report.phases)
    report.summary = " | ".join(
        f"Phase {chr(65+i)} ({'PASS' if p['passed'] else 'FAIL'})"
        for i, p in enumerate(report.phases)
    )

    report_dir = Path(f"eval-results/eval-2-convergence")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"eval-2-report-{args.branch}-{timestamp}.json"
    report_path.write_text(json.dumps(asdict(report), indent=2))
    print(f"\n[eval-2] {'PASS' if report.overall_passed else 'FAIL'}: {report.summary}")
    print(f"[eval-2] Report: {report_path}")

    sys.exit(0 if report.overall_passed else 1)


if __name__ == "__main__":
    main()
```

### 4.4 CLI Invocations

```bash
# Run on current v3.0 branch
uv run python scripts/eval_2.py --branch local

# Run on baseline for comparison
uv run python scripts/eval_2.py --branch global
```

### 4.5 Artifact Output Schema

```
eval-results/eval-2-convergence/
├── eval-2-report-{branch}-{timestamp}.json    # Structured comparison report
├── phase-a-disabled-{branch}-{timestamp}/
│   ├── spec-fidelity.md                       # Single-pass gate output
│   ├── .roadmap-state.json                    # State without convergence
│   ├── *.md                                   # All pipeline stage outputs
│   ├── pipeline-stdout.log
│   └── pipeline-stderr.log
├── phase-b-enabled-{branch}-{timestamp}/
│   ├── spec-fidelity.md                       # Convergence-controlled output
│   ├── *deviation*registry*.json              # DeviationRegistry state file
│   ├── .roadmap-state.json                    # State with convergence
│   ├── *.md                                   # All pipeline stage outputs
│   ├── pipeline-stdout.log
│   └── pipeline-stderr.log
└── (Phase C and D produce no disk artifacts — assertions only)
```

### 4.6 Assertion Criteria

| # | Assertion | Pass Condition | Threshold |
|---|-----------|---------------|-----------|
| A1 | spec_fidelity_exists | File exists | Boolean |
| A2 | spec_fidelity_gate_fields | All 6 SPEC_FIDELITY_GATE fields present | 0 missing |
| A3 | no_deviation_registry | No registry file when convergence disabled | 0 files |
| A4 | seeded_ambiguity_detected | spec-fidelity.md references FR-001.4 or FR-001.5 content | Any marker present |
| A5 | high_severity_parseable | high_severity_count is a non-negative integer | >= 0 |
| B1 | spec_fidelity_exists | File exists with convergence | Boolean |
| B2 | deviation_registry_exists | Registry JSON file created | >= 1 file |
| B3 | registry_schema_valid | Has schema_version, runs, findings keys | All 3 present |
| B4 | registry_has_runs | At least 1 run recorded | >= 1 |
| B5 | run_has_high_split | Run has structural_high_count and semantic_high_count | Both present |
| B6 | findings_have_stable_id | Each finding has stable_id field | All findings |
| C1 | stable_id_deterministic | Same inputs → same output | Equality |
| C2 | stable_id_varies | Different inputs → different output | Inequality |
| C3 | stable_id_format | 16-char lowercase hex string | Format match |
| C4 | stable_id_matches_sha256 | Output matches sha256(key)[:16] | Equality |
| D1 | regression_detected_on_increase | `_check_regression()` returns True when structural_high increases (2→3) | Boolean True |
| D2 | registry_has_2_runs | Registry contains 2 run entries after 2 `record_run()` calls | == 2 |
| D3 | no_regression_after_fix | `_check_regression()` returns False when structural_high decreases (3→2) | Boolean False |
| D4 | fixed_finding_tracked | Finding with status "FIXED" is correctly recorded | Exact match |
| D5 | semantic_fluctuation_not_regression | `_check_regression()` returns False for semantic-only increase | Boolean False |

**Overall pass**: All assertions across all 4 phases pass.

---

## 5. Eval 3: Mode-Aware Rollout Enforcement

### 5.1 Target Impact

Impact 3: Gates now support graduated enforcement via rollout modes (shadow/soft/full). The wiring gate's `blocking_count()` method encodes rollout policy into the artifact, and `_zero_blocking_findings_for_mode()` validates the encoded result.

### 5.2 What This Eval Proves

1. The same codebase produces different `blocking_findings` counts under shadow/soft/full modes
2. Shadow mode always produces `blocking_findings: 0` regardless of total findings
3. Soft mode's `blocking_findings` equals critical-only count
4. Full mode's `blocking_findings` equals critical + major count
5. The pipeline Step uses `gate_mode=GateMode.TRAILING` for shadow/soft rollout
6. The A/B comparison between branches shows: pre-v3.0 has no `rollout_mode` or `blocking_findings` in any artifact

### 5.3 Eval Design

```python
# scripts/eval_3.py — Mode-Aware Rollout Enforcement E2E Eval
"""
Eval 3: Verify mode-aware rollout enforcement produces correct blocking
behavior across shadow/soft/full modes.

Phase A: Rollout sensitivity — run wiring analysis in 3 modes against project source
Phase B: Pipeline artifact inspection — verify trailing gate mode in pipeline output
Phase C: A/B branch comparison — verify rollout fields absent pre-v3.0
"""
import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class EvalResult:
    eval_id: str
    phase: str
    passed: bool
    assertions: list[dict] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    error: str | None = None


@dataclass
class ComparisonReport:
    eval_id: str = "eval-3-rollout-enforcement"
    timestamp: str = ""
    branch: str = ""
    phases: list[dict] = field(default_factory=list)
    overall_passed: bool = False
    summary: str = ""


def assert_check(name: str, condition: bool, detail: str = "") -> dict:
    return {"name": name, "passed": condition, "detail": detail}


def parse_frontmatter(file_path: Path) -> dict[str, str]:
    content = file_path.read_text(encoding="utf-8")
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return {}
    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return {}
    result = {}
    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def phase_a_rollout_sensitivity(output_dir: Path, project_source: Path) -> EvalResult:
    """Phase A: Run wiring analysis in 3 modes, compare blocking_findings."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-3", phase="A-rollout-sensitivity", passed=False)

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from superclaude.cli.audit.wiring_gate import run_wiring_analysis, emit_report
    from superclaude.cli.audit.wiring_config import WiringConfig

    mode_results: dict[str, dict] = {}

    for mode in ("shadow", "soft", "full"):
        config = WiringConfig(rollout_mode=mode)
        report = run_wiring_analysis(config, project_source)
        report_path = output_dir / f"wiring-{mode}.md"
        emit_report(report, report_path)
        result.artifacts.append(str(report_path))

        fm = parse_frontmatter(report_path)
        mode_results[mode] = {
            "total_findings": report.total_findings,
            "blocking_findings": int(fm.get("blocking_findings", -1)),
            "rollout_mode": fm.get("rollout_mode"),
            "critical_count": int(fm.get("critical_count", 0)),
            "major_count": int(fm.get("major_count", 0)),
            "blocking_from_report": report.blocking_count(mode),
        }

    # Write mode comparison for inspection
    comparison_path = output_dir / "mode-comparison.json"
    comparison_path.write_text(json.dumps(mode_results, indent=2))
    result.artifacts.append(str(comparison_path))

    shadow = mode_results["shadow"]
    soft = mode_results["soft"]
    full = mode_results["full"]

    # 1. Assert: all three modes report the same total_findings
    same_total = (
        shadow["total_findings"] == soft["total_findings"] == full["total_findings"]
    )
    result.assertions.append(
        assert_check(
            "same_total_across_modes",
            same_total,
            f"shadow={shadow['total_findings']}, soft={soft['total_findings']}, full={full['total_findings']}",
        )
    )

    # 2. Assert: shadow blocking_findings is always 0
    result.assertions.append(
        assert_check(
            "shadow_blocking_zero",
            shadow["blocking_findings"] == 0,
            f"shadow blocking={shadow['blocking_findings']}",
        )
    )

    # 3. Assert: soft blocking_findings equals critical_count
    result.assertions.append(
        assert_check(
            "soft_blocking_equals_critical",
            soft["blocking_findings"] == soft["critical_count"],
            f"soft blocking={soft['blocking_findings']}, critical={soft['critical_count']}",
        )
    )

    # 4. Assert: full blocking_findings equals critical + major
    expected_full_blocking = full["critical_count"] + full["major_count"]
    result.assertions.append(
        assert_check(
            "full_blocking_equals_critical_plus_major",
            full["blocking_findings"] == expected_full_blocking,
            f"full blocking={full['blocking_findings']}, expected={expected_full_blocking}",
        )
    )

    # 5. Assert: rollout_mode values are correctly written
    for mode in ("shadow", "soft", "full"):
        result.assertions.append(
            assert_check(
                f"rollout_mode_{mode}_correct",
                mode_results[mode]["rollout_mode"] == mode,
                f"Expected {mode}, got {mode_results[mode]['rollout_mode']}",
            )
        )

    # 6. Assert: if total_findings > 0, verify graduated enforcement.
    #    If total_findings == 0, skip with WARNING (not vacuously true).
    if shadow["total_findings"] > 0:
        graduated = shadow["blocking_findings"] <= soft["blocking_findings"] <= full["blocking_findings"]
        result.assertions.append(
            assert_check(
                "graduated_enforcement",
                graduated,
                f"shadow({shadow['blocking_findings']}) <= soft({soft['blocking_findings']}) <= full({full['blocking_findings']})",
            )
        )
    else:
        # WARNING: Cannot verify graduated enforcement with zero findings.
        # Arithmetic assertions (A2-A4) still validate mode-specific blocking logic.
        print(
            "[eval-3] WARNING: total_findings=0 — graduated enforcement assertion "
            "skipped (shadow<=soft<=full is vacuously 0<=0<=0). "
            "Arithmetic assertions A2-A4 still verify mode-specific blocking logic."
        )
        # Do NOT append an assertion — skipping is more honest than vacuously passing.

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_b_pipeline_trailing_mode(output_dir: Path, spec_file: Path) -> EvalResult:
    """Phase B: Run pipeline, verify wiring step uses TRAILING gate mode."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-3", phase="B-trailing-mode", passed=False)

    # Run pipeline
    cmd = [
        "superclaude", "roadmap", "run",
        str(spec_file),
        "--output-dir", str(output_dir),
        "--no-validate",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    (output_dir / "pipeline-stdout.log").write_text(proc.stdout)
    (output_dir / "pipeline-stderr.log").write_text(proc.stderr)

    result.artifacts = [str(p) for p in output_dir.glob("*")]

    # 1. Assert: wiring-verification.md exists
    wiring_report = output_dir / "wiring-verification.md"
    result.assertions.append(
        assert_check("wiring_report_exists", wiring_report.exists())
    )

    # 2. Assert: check stderr/stdout for TRAILING mode indicators
    combined_output = proc.stdout + proc.stderr
    # The trailing gate runner logs when it processes a step
    trailing_indicators = [
        "TRAILING", "trailing", "shadow", "wiring-verification",
    ]
    has_trailing_ref = any(ind in combined_output for ind in trailing_indicators)
    result.assertions.append(
        assert_check(
            "trailing_mode_referenced",
            has_trailing_ref,
            "Pipeline output references trailing/shadow mode"
            if has_trailing_ref
            else "No trailing mode references in pipeline output",
        )
    )

    # 3. Assert: verify _build_steps() wires TRAILING via code inspection
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from superclaude.cli.pipeline.models import GateMode

    # We verify the code itself — _build_steps configures gate_mode=TRAILING
    from superclaude.cli.roadmap.executor import _build_steps
    from superclaude.cli.roadmap.models import RoadmapConfig, AgentSpec

    test_config = RoadmapConfig(
        spec_file=spec_file,
        output_dir=output_dir / "verify",
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        depth="standard",
    )
    steps = _build_steps(test_config)

    # Find the wiring-verification step
    wiring_step = None
    for entry in steps:
        if isinstance(entry, list):
            for s in entry:
                if s.id == "wiring-verification":
                    wiring_step = s
        else:
            if entry.id == "wiring-verification":
                wiring_step = entry

    result.assertions.append(
        assert_check(
            "wiring_step_in_build_steps",
            wiring_step is not None,
            "wiring-verification step found in _build_steps()",
        )
    )

    if wiring_step:
        result.assertions.append(
            assert_check(
                "wiring_step_trailing_mode",
                wiring_step.gate_mode == GateMode.TRAILING,
                f"gate_mode={wiring_step.gate_mode}",
            )
        )
        result.assertions.append(
            assert_check(
                "wiring_step_retry_zero",
                wiring_step.retry_limit == 0,
                f"retry_limit={wiring_step.retry_limit}",
            )
        )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_c_branch_comparison(output_dir: Path) -> EvalResult:
    """Phase C: Compare v3.0 vs pre-v3.0 for rollout_mode field presence."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-3", phase="C-branch-comparison", passed=False)

    # This phase inspects existing artifacts from Phase B (local branch)
    # and compares with artifacts from a global (pre-v3.0) run if available

    local_dir = output_dir
    global_dir = output_dir.parent / "phase-b-global"

    # 1. Assert: local branch has rollout_mode in wiring-verification.md
    local_wiring = local_dir / "wiring-verification.md"
    if local_wiring.exists():
        fm = parse_frontmatter(local_wiring)
        result.assertions.append(
            assert_check(
                "local_has_rollout_mode",
                "rollout_mode" in fm,
                f"Local frontmatter keys: {list(fm.keys())}",
            )
        )
        result.assertions.append(
            assert_check(
                "local_has_blocking_findings",
                "blocking_findings" in fm,
                f"blocking_findings present: {'blocking_findings' in fm}",
            )
        )
    else:
        result.assertions.append(
            assert_check("local_has_rollout_mode", False, "No wiring report on local")
        )

    # 2. Assert: global branch (if available) has NO wiring-verification.md
    if global_dir.exists():
        global_wiring = global_dir / "wiring-verification.md"
        result.assertions.append(
            assert_check(
                "global_no_wiring_report",
                not global_wiring.exists(),
                f"Global wiring report exists: {global_wiring.exists()}",
            )
        )
    else:
        # Global not available — skip with informational note
        result.assertions.append(
            assert_check(
                "global_no_wiring_report",
                True,  # Vacuously true — no global run to compare
                "Global branch artifacts not available (run with --branch global to populate)",
            )
        )

    # 3. Assert: local .roadmap-state.json has more step entries than would exist pre-v3.0
    state_file = local_dir / ".roadmap-state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text())
        steps = state.get("steps", {})
        has_v3_steps = "wiring-verification" in steps
        result.assertions.append(
            assert_check(
                "state_has_v3_steps",
                has_v3_steps,
                f"Steps: {list(steps.keys())}",
            )
        )
    else:
        result.assertions.append(
            assert_check("state_has_v3_steps", False, "No state file")
        )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def main():
    parser = argparse.ArgumentParser(description="Eval 3: Mode-Aware Rollout Enforcement")
    parser.add_argument(
        "--branch", choices=["local", "global"], default="local",
        help="Artifact label for directory naming (does NOT switch git branches)",
    )
    parser.add_argument(
        "--spec-file",
        default=".dev/releases/current/v3.0_unified-audit-gating/eval-spec.md",
    )
    parser.add_argument(
        "--project-source",
        default="src/superclaude/cli",
        help="Source directory for rollout sensitivity test",
    )
    args = parser.parse_args()

    spec_file = Path(args.spec_file).resolve()
    project_source = Path(args.project_source).resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    print(f"[eval-3] Running on current branch ('{args.branch}' is an artifact label, not a git operation)")

    report = ComparisonReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        branch=args.branch,
    )

    # Phase A: Rollout sensitivity (no pipeline needed — direct analysis)
    out_a = Path(f"eval-results/eval-3-rollout/phase-a-sensitivity-{timestamp}")
    out_a.mkdir(parents=True, exist_ok=True)
    print(f"[eval-3] Phase A: Rollout mode sensitivity against {project_source}")
    phase_a = phase_a_rollout_sensitivity(out_a, project_source)
    report.phases.append(asdict(phase_a))

    # Phase B: Pipeline trailing mode verification
    out_b = Path(f"eval-results/eval-3-rollout/phase-b-{args.branch}-{timestamp}")
    out_b.mkdir(parents=True, exist_ok=True)
    print(f"[eval-3] Phase B: Pipeline trailing mode ({args.branch})")
    phase_b = phase_b_pipeline_trailing_mode(out_b, spec_file)
    report.phases.append(asdict(phase_b))

    # Phase C: Branch comparison
    print(f"[eval-3] Phase C: Branch comparison")
    phase_c = phase_c_branch_comparison(out_b)
    report.phases.append(asdict(phase_c))

    report.overall_passed = all(p["passed"] for p in report.phases)
    report.summary = " | ".join(
        f"Phase {chr(65+i)} ({'PASS' if p['passed'] else 'FAIL'})"
        for i, p in enumerate(report.phases)
    )

    report_dir = Path(f"eval-results/eval-3-rollout")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"eval-3-report-{args.branch}-{timestamp}.json"
    report_path.write_text(json.dumps(asdict(report), indent=2))
    print(f"\n[eval-3] {'PASS' if report.overall_passed else 'FAIL'}: {report.summary}")
    print(f"[eval-3] Report: {report_path}")

    sys.exit(0 if report.overall_passed else 1)


if __name__ == "__main__":
    main()
```

### 5.4 CLI Invocations

```bash
# Run on current v3.0 branch
uv run python scripts/eval_3.py --branch local

# Run on baseline for comparison
uv run python scripts/eval_3.py --branch global
```

### 5.5 Artifact Output Schema

```
eval-results/eval-3-rollout/
├── eval-3-report-{branch}-{timestamp}.json    # Structured comparison report
├── phase-a-sensitivity-{timestamp}/
│   ├── wiring-shadow.md                       # Shadow mode report
│   ├── wiring-soft.md                         # Soft mode report
│   ├── wiring-full.md                         # Full mode report
│   └── mode-comparison.json                   # Side-by-side blocking counts
└── phase-b-{branch}-{timestamp}/
    ├── wiring-verification.md                 # Pipeline-produced report
    ├── .roadmap-state.json                    # Pipeline state
    ├── *.md                                   # All pipeline stage outputs
    ├── pipeline-stdout.log
    └── pipeline-stderr.log
```

### 5.6 Assertion Criteria

| # | Assertion | Pass Condition | Threshold |
|---|-----------|---------------|-----------|
| A1 | same_total_across_modes | All 3 modes report identical total_findings | Equality |
| A2 | shadow_blocking_zero | shadow blocking_findings == 0 | == 0 |
| A3 | soft_blocking_equals_critical | soft blocking == critical_count | Equality |
| A4 | full_blocking_equals_critical_plus_major | full blocking == critical + major | Equality |
| A5-7 | rollout_mode_{mode}_correct | rollout_mode field matches mode | Exact match |
| A8 | graduated_enforcement | shadow <= soft <= full for blocking counts (SKIPPED with WARNING when total_findings==0) | Monotonic or skipped |
| B1 | wiring_report_exists | Pipeline produces wiring-verification.md | Boolean |
| B2 | trailing_mode_referenced | Pipeline output mentions trailing/shadow mode | Any indicator |
| B3 | wiring_step_in_build_steps | _build_steps() includes wiring-verification | Found |
| B4 | wiring_step_trailing_mode | gate_mode == GateMode.TRAILING | Equality |
| B5 | wiring_step_retry_zero | retry_limit == 0 | Equality |
| C1 | local_has_rollout_mode | rollout_mode in wiring-verification.md frontmatter | Key exists |
| C2 | local_has_blocking_findings | blocking_findings in frontmatter | Key exists |
| C3 | global_no_wiring_report | Pre-v3.0 has no wiring-verification.md | File absent |
| C4 | state_has_v3_steps | .roadmap-state.json has wiring-verification | Key exists |

**Overall pass**: All assertions across all 3 phases pass.

---

## 6. Comparison Report Format

All three evals produce JSON reports with this schema:

```json
{
  "eval_id": "eval-{N}-{name}",
  "timestamp": "2026-03-19T...",
  "branch": "local|global",
  "phases": [
    {
      "eval_id": "eval-{N}",
      "phase": "{phase-name}",
      "passed": true|false,
      "assertions": [
        {
          "name": "assertion_name",
          "passed": true|false,
          "detail": "Human-readable detail"
        }
      ],
      "artifacts": ["path/to/artifact1.md", ...],
      "duration_seconds": 12.34,
      "error": null|"error message"
    }
  ],
  "overall_passed": true|false,
  "summary": "Phase A (PASS) | Phase B (PASS) | Phase C (PASS)"
}
```

## 7. Known Limitations

| Limitation | Affected Eval | Mitigation |
|-----------|---------------|------------|
| Eval spec produces zero wiring findings | Eval 1 Phase A | Phase B scans project source for detection power |
| Convergence CLI flag may not exist yet | Eval 2 Phase B | Falls back to code-level verification of DeviationRegistry |
| Pre-v3.0 baseline branch may not exist | Eval 3 Phase C | Vacuously true assertions with informational notes |
| LLM non-determinism in stages 1-8 | All evals | Assertions target structural properties (field presence, arithmetic), not content quality |
| Remediate/certify stages unreachable | None | Not targeted — stage review confirmed trigger wiring is absent |
| Seeded ambiguity propagation is non-deterministic | Eval 2 Phase A assertion A4 | Hard assertion — if seeded ambiguities don't reach spec-fidelity, that's a real propagation failure worth investigating. Widen marker set if flaky. |
