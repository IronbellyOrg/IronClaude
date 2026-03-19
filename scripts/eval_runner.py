#!/usr/bin/env python3
"""v3.0 Eval Runner — orchestrates parallel local + global eval runs.

Usage:
    uv run python scripts/eval_runner.py --mode local    # 2 local runs
    uv run python scripts/eval_runner.py --mode global   # 2 global runs (master worktree)
    uv run python scripts/eval_runner.py --mode full     # 4 runs + comparison
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

EVAL_FILES = [
    "tests/roadmap/test_eval_gate_rejection.py",
    "tests/roadmap/test_eval_finding_lifecycle.py",
    "tests/roadmap/test_eval_convergence_multirun.py",
    "tests/roadmap/test_eval_gate_ordering.py",
    "tests/audit/test_eval_wiring_multifile.py",
]

E2E_SCRIPTS = [
    "scripts/eval_1.py",
    "scripts/eval_2.py",
    "scripts/eval_3.py",
]

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / ".dev" / "releases" / "current" / "v3.0_unified-audit-gating" / "eval-results"


@dataclass
class RunResult:
    name: str
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration: float = 0.0
    failures: list[str] = field(default_factory=list)
    xml_path: str = ""


def run_pytest(label: str, cwd: Path, xml_path: Path) -> RunResult:
    """Run pytest and parse JUnit XML results."""
    cmd = [
        "uv", "run", "pytest",
        *EVAL_FILES,
        f"--junit-xml={xml_path}",
        "--tb=short", "-q",
    ]
    start = time.monotonic()
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
    duration = time.monotonic() - start

    result = RunResult(name=label, duration=round(duration, 3), xml_path=str(xml_path))

    if xml_path.exists():
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for suite in root.iter("testsuite"):
            result.passed += int(suite.get("tests", 0)) - int(suite.get("failures", 0)) - int(suite.get("errors", 0)) - int(suite.get("skipped", 0))
            result.failed += int(suite.get("failures", 0))
            result.errors += int(suite.get("errors", 0))
            result.skipped += int(suite.get("skipped", 0))

        for tc in root.iter("testcase"):
            failure = tc.find("failure")
            if failure is not None:
                result.failures.append(f"{tc.get('classname')}.{tc.get('name')}")
    else:
        # XML not created — parse from stdout
        result.errors = 1
        result.failures.append(f"pytest did not produce XML output. stderr: {proc.stderr[-500:]}")

    return result


def run_e2e_script(script: str, branch: str, cwd: Path) -> RunResult:
    """Run an E2E eval script and capture its result."""
    label = f"e2e-{Path(script).stem}-{branch}"
    cmd = ["uv", "run", "python", script, "--branch", branch]
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1800)
        duration = time.monotonic() - start
        result = RunResult(name=label, duration=round(duration, 3))
        if proc.returncode == 0:
            result.passed = 1
        else:
            result.failed = 1
            result.failures.append(f"Exit code {proc.returncode}: {proc.stderr[-500:]}")
        return result
    except subprocess.TimeoutExpired:
        return RunResult(
            name=label,
            errors=1,
            duration=round(time.monotonic() - start, 3),
            failures=["Timeout after 1800s"],
        )


def run_local(run_id: str) -> RunResult:
    """Run evals on current branch."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    xml = RESULTS_DIR / f"local-{run_id}.xml"
    return run_pytest(f"local-{run_id}", REPO_ROOT, xml)


def run_global(run_id: str) -> RunResult:
    """Run evals on master via git worktree."""
    worktree_path = REPO_ROOT.parent / "IronClaude-eval-master"

    # Create worktree if needed
    if not worktree_path.exists():
        subprocess.run(
            ["git", "worktree", "add", str(worktree_path), "master"],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )

    # Check if eval files exist on master
    missing = [f for f in EVAL_FILES if not (worktree_path / f).exists()]
    if missing:
        return RunResult(
            name=f"global-{run_id}",
            failures=[f"Eval files not on master: {missing}"],
            errors=len(missing),
        )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    xml = RESULTS_DIR / f"global-{run_id}.xml"
    result = run_pytest(f"global-{run_id}", worktree_path, xml)

    return result


def compare_runs(runs: list[RunResult]) -> dict:
    """Compare multiple runs for consistency and A/B delta."""
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "runs": [],
        "consistency": {},
        "comparison": {},
    }

    local_runs = [r for r in runs if r.name.startswith("local")]
    global_runs = [r for r in runs if r.name.startswith("global")]

    for r in runs:
        report["runs"].append({
            "name": r.name,
            "passed": r.passed,
            "failed": r.failed,
            "skipped": r.skipped,
            "errors": r.errors,
            "duration": r.duration,
            "failures": r.failures,
        })

    # Consistency check: local runs should be identical
    if len(local_runs) == 2:
        a, b = local_runs
        report["consistency"]["local_identical"] = (
            a.passed == b.passed and a.failed == b.failed and
            a.skipped == b.skipped and set(a.failures) == set(b.failures)
        )
        report["consistency"]["duration_variance_pct"] = (
            round(abs(a.duration - b.duration) / max(a.duration, b.duration, 0.001) * 100, 1)
        )

    # A/B comparison: local vs global
    if local_runs and global_runs:
        local = local_runs[0]
        glob = global_runs[0]
        if glob.errors == 0:
            local_failures = set(local.failures)
            global_failures = set(glob.failures)
            report["comparison"]["regressions"] = sorted(local_failures - global_failures)
            report["comparison"]["improvements"] = sorted(global_failures - local_failures)
            report["comparison"]["new_tests"] = local.passed + local.failed - glob.passed - glob.failed
        else:
            report["comparison"]["note"] = "Global run had errors; full comparison unavailable"
            report["comparison"]["new_tests"] = local.passed + local.failed

    return report


def print_report(report: dict) -> None:
    """Print human-readable comparison report."""
    print("\n" + "=" * 60)
    print("v3.0 Eval Results")
    print("=" * 60)

    for r in report["runs"]:
        status = "PASS" if r["failed"] == 0 and r["errors"] == 0 else "FAIL"
        print(f"  {r['name']:20s}  {r['passed']} passed / {r['failed']} failed / {r['skipped']} skipped  [{r['duration']:.3f}s]  {status}")
        for f in r["failures"]:
            print(f"    FAIL: {f}")

    if "local_identical" in report.get("consistency", {}):
        ident = report["consistency"]["local_identical"]
        var = report["consistency"]["duration_variance_pct"]
        print(f"\n  Consistency: {'PASS' if ident else 'FAIL'} (duration variance: {var}%)")

    comp = report.get("comparison", {})
    if comp:
        regs = comp.get("regressions", [])
        imps = comp.get("improvements", [])
        new = comp.get("new_tests", 0)
        print(f"\n  New tests (local only): {new}")
        print(f"  Regressions (pass→fail): {len(regs)}")
        for r in regs:
            print(f"    REGRESSION: {r}")
        print(f"  Improvements (fail→pass): {len(imps)}")
        note = comp.get("note")
        if note:
            print(f"  Note: {note}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="v3.0 Eval Runner")
    parser.add_argument("--mode", choices=["local", "global", "full"], default="full")
    args = parser.parse_args()

    runs: list[RunResult] = []
    e2e_runs: list[RunResult] = []

    if args.mode in ("local", "full"):
        print("Running local eval A...")
        runs.append(run_local("A"))
        print("Running local eval B...")
        runs.append(run_local("B"))

        # E2E pipeline evals (local branch)
        for script in E2E_SCRIPTS:
            script_path = REPO_ROOT / script
            if script_path.exists():
                print(f"Running E2E {script} (local)...")
                e2e_runs.append(run_e2e_script(script, "local", REPO_ROOT))

    if args.mode in ("global", "full"):
        print("Running global eval A...")
        runs.append(run_global("A"))
        print("Running global eval B...")
        runs.append(run_global("B"))

        # E2E pipeline evals (global branch)
        worktree_path = REPO_ROOT.parent / "IronClaude-eval-master"
        if worktree_path.exists():
            for script in E2E_SCRIPTS:
                script_path = worktree_path / script
                if script_path.exists():
                    print(f"Running E2E {script} (global)...")
                    e2e_runs.append(run_e2e_script(script, "global", worktree_path))

    all_runs = runs + e2e_runs
    report = compare_runs(all_runs)
    print_report(report)

    # Save JSON report
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = RESULTS_DIR / "eval-report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\nJSON report: {report_path}")

    # Exit code: non-zero if any failures
    if any(r.failed > 0 or r.errors > 0 for r in runs if r.name.startswith("local")):
        sys.exit(1)


if __name__ == "__main__":
    main()
