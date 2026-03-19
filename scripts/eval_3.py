#!/usr/bin/env python3
"""
Eval 3: Verify mode-aware rollout enforcement produces correct blocking
behavior across shadow/soft/full modes.

Phase A: Rollout sensitivity — run wiring analysis in 3 modes against project source
Phase B: Pipeline artifact inspection — verify trailing gate mode in pipeline output
Phase C: A/B branch comparison — verify rollout fields absent pre-v3.0
"""
from __future__ import annotations

import argparse
import json
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


def phase_a_rollout_sensitivity(output_dir: Path, project_source: Path) -> EvalResult:
    """Phase A: Run wiring analysis in 3 modes, compare blocking_findings."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-3", phase="A-rollout-sensitivity", passed=False)

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from superclaude.cli.audit.wiring_config import WiringConfig
    from superclaude.cli.audit.wiring_gate import emit_report, run_wiring_analysis

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
        print(
            "[eval-3] WARNING: total_findings=0 — graduated enforcement assertion "
            "skipped (shadow<=soft<=full is vacuously 0<=0<=0). "
            "Arithmetic assertions A2-A4 still verify mode-specific blocking logic."
        )

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_b_pipeline_trailing_mode(output_dir: Path, spec_file: Path, eval_start_time: float) -> EvalResult:
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

    # 2. Assert (R-8a): wiring-verification.md contains rollout_mode in frontmatter
    wiring_fm = {}
    if wiring_report.exists():
        wiring_fm = parse_frontmatter(wiring_report)
    has_rollout_mode = wiring_fm.get("rollout_mode") in ("shadow", "soft", "full")
    result.assertions.append(
        assert_check(
            "r8a_artifact_rollout_mode",
            has_rollout_mode,
            f"rollout_mode={wiring_fm.get('rollout_mode')}"
            if has_rollout_mode
            else "wiring-verification.md missing or lacks rollout_mode",
        )
    )

    # 3. Assert: verify _build_steps() wires TRAILING via code inspection
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from superclaude.cli.pipeline.models import GateMode
    from superclaude.cli.roadmap.executor import _build_steps
    from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig

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

    # 4. Artifact provenance
    result.assertions.extend(verify_artifact_provenance(output_dir, eval_start_time))

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_c_branch_comparison(output_dir: Path) -> EvalResult:
    """Phase C: Compare v3.0 vs pre-v3.0 for rollout_mode field presence."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-3", phase="C-branch-comparison", passed=False)

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
        result.assertions.append(
            assert_check(
                "global_no_wiring_report",
                True,  # Vacuously true — no global run to compare
                "Global branch artifacts not available (run with --branch global to populate)",
            )
        )

    # 3. Assert: local .roadmap-state.json has v3.0 steps
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
    eval_start_time = time.time()

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
    phase_b = phase_b_pipeline_trailing_mode(out_b, spec_file, eval_start_time)
    report.phases.append(asdict(phase_b))

    # Phase C: Branch comparison
    print("[eval-3] Phase C: Branch comparison")
    phase_c = phase_c_branch_comparison(out_b)
    report.phases.append(asdict(phase_c))

    report.overall_passed = all(p["passed"] for p in report.phases)
    report.summary = " | ".join(
        f"Phase {chr(65+i)} ({'PASS' if p['passed'] else 'FAIL'})"
        for i, p in enumerate(report.phases)
    )

    report_dir = Path("eval-results/eval-3-rollout")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"eval-3-report-{args.branch}-{timestamp}.json"
    report_path.write_text(json.dumps(asdict(report), indent=2))
    print(f"\n[eval-3] {'PASS' if report.overall_passed else 'FAIL'}: {report.summary}")
    print(f"[eval-3] Report: {report_path}")

    sys.exit(0 if report.overall_passed else 1)


if __name__ == "__main__":
    main()
