#!/usr/bin/env python3
"""
Eval 1: Verify wiring-verification gate integrates into the roadmap pipeline
and produces structurally valid artifacts.

Phase A: Full pipeline run with eval spec → verify wiring-verification.md
Phase B: Direct wiring analysis against project source → verify detection power
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
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


def verify_artifact_provenance(output_dir: Path, start_time: float) -> list[dict]:
    """Verify all artifacts in output_dir have mtime after start_time."""
    assertions = []
    artifacts = list(output_dir.glob("*"))
    if not artifacts:
        assertions.append(assert_check(
            "provenance_artifacts_exist", False, "No artifacts in output directory"
        ))
        return assertions

    stale = []
    for artifact in artifacts:
        if artifact.is_file():
            mtime = artifact.stat().st_mtime
            if mtime < start_time:
                stale.append(f"{artifact.name} (mtime={mtime:.0f} < start={start_time:.0f})")
    assertions.append(assert_check(
        "provenance_all_artifacts_fresh",
        len(stale) == 0,
        f"Stale artifacts: {stale}" if stale else f"All {len(artifacts)} artifacts post-date eval start",
    ))
    return assertions


def phase_a_pipeline_integration(output_dir: Path, spec_file: Path, eval_start_time: float) -> EvalResult:
    """Phase A: Run full pipeline, verify wiring-verification.md exists and passes gate."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-1", phase="A-pipeline-integration", passed=False)

    # 1. Run the pipeline
    run_pipeline(spec_file, output_dir)

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

    # 13. Artifact content integrity checks
    lines = [l for l in content.splitlines() if l.strip()]
    result.assertions.append(
        assert_check(
            "content_min_10_lines",
            len(lines) > 10,
            f"Non-empty lines: {len(lines)}",
        )
    )
    has_headings = any(l.startswith("## ") or l.startswith("### ") for l in content.splitlines())
    result.assertions.append(
        assert_check(
            "content_has_section_headings",
            has_headings,
            "Has markdown section headings" if has_headings else "No section headings found",
        )
    )

    # 14. Artifact provenance: verify mtimes post-date eval start
    result.assertions.extend(verify_artifact_provenance(output_dir, eval_start_time))

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
    from superclaude.cli.audit.wiring_config import WiringConfig
    from superclaude.cli.audit.wiring_gate import emit_report, run_wiring_analysis

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
    eval_start_time = time.time()

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
    phase_a = phase_a_pipeline_integration(output_dir, spec_file, eval_start_time)
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
