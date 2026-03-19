#!/usr/bin/env python3
"""
Eval 2: Verify convergence-controlled spec-fidelity produces stable
deviation tracking with structural/semantic HIGH separation.

Phase A: Convergence-disabled run → verify SPEC_FIDELITY_GATE applies normally
Phase B: Convergence-enabled run → verify DeviationRegistry is created and populated
Phase C: Stable ID determinism → verify compute_stable_id() is pure
Phase D: Regression detection → verify _check_regression() distinguishes structural regressions from noise
"""
from __future__ import annotations

import argparse
import hashlib
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


def phase_a_convergence_disabled(output_dir: Path, spec_file: Path, eval_start_time: float) -> EvalResult:
    """Phase A: Run without convergence → SPEC_FIDELITY_GATE applies."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-2", phase="A-convergence-disabled", passed=False)

    run_pipeline(spec_file, output_dir, convergence_enabled=False)

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

    # 4. Assert: seeded ambiguity detection
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

    # 5. Assert: high_severity_count is parseable
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

    # 6. Artifact provenance
    result.assertions.extend(verify_artifact_provenance(output_dir, eval_start_time))

    result.passed = all(a["passed"] for a in result.assertions)
    result.duration_seconds = time.monotonic() - start
    return result


def phase_b_convergence_enabled(output_dir: Path, spec_file: Path, eval_start_time: float) -> EvalResult:
    """Phase B: Run with convergence → DeviationRegistry created."""
    start = time.monotonic()
    result = EvalResult(eval_id="eval-2", phase="B-convergence-enabled", passed=False)

    run_pipeline(spec_file, output_dir, convergence_enabled=True)

    spec_fidelity = output_dir / "spec-fidelity.md"
    result.artifacts = [str(p) for p in output_dir.glob("*")]

    # 1. Assert: spec-fidelity.md exists
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

    # 7. Artifact provenance
    result.assertions.extend(verify_artifact_provenance(output_dir, eval_start_time))

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
            f"_check_regression() returned {is_regression} for structural 2->3",
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
            f"_check_regression() returned {is_regression_after_fix} for structural 3->2",
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
    eval_start_time = time.time()

    print(f"[eval-2] Running on current branch ('{args.branch}' is an artifact label, not a git operation)")

    report = ComparisonReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        branch=args.branch,
    )

    # Phase A: Convergence disabled
    out_a = Path(f"eval-results/eval-2-convergence/phase-a-disabled-{args.branch}-{timestamp}")
    out_a.mkdir(parents=True, exist_ok=True)
    print(f"[eval-2] Phase A: Convergence disabled ({args.branch})")
    phase_a = phase_a_convergence_disabled(out_a, spec_file, eval_start_time)
    report.phases.append(asdict(phase_a))

    # Phase B: Convergence enabled
    out_b = Path(f"eval-results/eval-2-convergence/phase-b-enabled-{args.branch}-{timestamp}")
    out_b.mkdir(parents=True, exist_ok=True)
    print(f"[eval-2] Phase B: Convergence enabled ({args.branch})")
    phase_b = phase_b_convergence_enabled(out_b, spec_file, eval_start_time)
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

    report_dir = Path("eval-results/eval-2-convergence")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"eval-2-report-{args.branch}-{timestamp}.json"
    report_path.write_text(json.dumps(asdict(report), indent=2))
    print(f"\n[eval-2] {'PASS' if report.overall_passed else 'FAIL'}: {report.summary}")
    print(f"[eval-2] Report: {report_path}")

    sys.exit(0 if report.overall_passed else 1)


if __name__ == "__main__":
    main()
