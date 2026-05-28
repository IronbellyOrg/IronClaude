#!/usr/bin/env python3
"""Compare live sc-brainstorm runs against the iteration-2 baseline.

Acceptance scope (this script's default): cases 4-11.

Case 12 (`architecture-graphql-public-api`) is INTENTIONALLY EXCLUDED from the
comparison. Live invocation of case 12 is blocked by the command/skill registry
error `Unknown skill: sc:brainstorm-protocol`. Bringing case 12 into the
comparison requires a separate scope decision and a registry-compatibility task;
do NOT broaden `CASE_IDS` to include 12 without that decision.

The script reports missing quality scores and missing live timing/token
telemetry as EXPLICIT AVAILABILITY GAPS in the summary (counts of unavailable
quality + telemetry, plus the `quality.status` and `timing.status` on each case)
rather than silently treating absence as a pass. Inflating the structural pass
rate by counting unavailable as available is a documented anti-pattern; the
summary fields `quality_unavailable_count` and `telemetry_unavailable_count`
exist so downstream readers can distinguish "covered and passing" from
"not yet covered".
"""
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from grader import check_assertion, parse_yaml_simple, read_text

ROOT = Path(__file__).resolve().parent
ITERATION_DIR = ROOT / "iterations" / "iteration-2"
LIVE_ROOT = ROOT / "live-runs"

# Default acceptance scope: cases 4-11. Case 12 is excluded; see module docstring.
CASE_IDS = set(range(4, 12))
EXCLUDED_CASE_IDS = {12}
EXCLUDED_CASE_REASON = (
    "Case 12 (architecture-graphql-public-api) is excluded because live invocation "
    "is blocked by the command/skill registry error `Unknown skill: sc:brainstorm-protocol`. "
    "Bringing case 12 into the comparison requires a separate scope decision and a "
    "registry-compatibility task."
)


def _validate_evals_sync(evals_data: dict[str, Any]) -> None:
    """Confirm `evals.json`'s remediation acceptance scope matches this script's CASE_IDS.

    Prints a warning to stderr if the keys are absent OR present-and-different.
    Missing keys are treated as a sync FAILURE (not a silent pass) so the docstring
    contract about metadata-level enforcement holds even when evals.json is edited
    by someone who doesn't know these keys exist. A `None` sentinel distinguishes
    "absent" from "present-but-empty".
    """
    raw_declared = evals_data.get("remediation_acceptance_scope")
    raw_deferred = evals_data.get("remediation_deferred_cases")
    if raw_declared is None:
        print(
            "WARNING: evals.json is missing key `remediation_acceptance_scope`. "
            f"Add it as a list matching compare_live_runs.py CASE_IDS={sorted(CASE_IDS)} "
            "so future scope edits stay in sync.",
            file=sys.stderr,
        )
    elif set(raw_declared) != CASE_IDS:
        print(
            f"WARNING: evals.json remediation_acceptance_scope={sorted(set(raw_declared))} "
            f"differs from compare_live_runs.py CASE_IDS={sorted(CASE_IDS)}. "
            "Update one to match the other before relying on this comparison.",
            file=sys.stderr,
        )
    if raw_deferred is None:
        print(
            "WARNING: evals.json is missing key `remediation_deferred_cases`. "
            f"Add it as a list matching compare_live_runs.py EXCLUDED_CASE_IDS={sorted(EXCLUDED_CASE_IDS)}.",
            file=sys.stderr,
        )
    elif set(raw_deferred) != EXCLUDED_CASE_IDS:
        print(
            f"WARNING: evals.json remediation_deferred_cases={sorted(set(raw_deferred))} "
            f"differs from compare_live_runs.py EXCLUDED_CASE_IDS={sorted(EXCLUDED_CASE_IDS)}. "
            "Resolve the discrepancy before relying on this comparison.",
            file=sys.stderr,
        )


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def load_evals() -> list[dict[str, Any]]:
    """Load eval cases scoped to CASE_IDS. Validates evals.json's declared
    remediation_acceptance_scope and remediation_deferred_cases against this
    script's constants before returning."""
    data = read_json(ROOT / "evals" / "evals.json")
    _validate_evals_sync(data)
    return [case for case in data["evals"] if int(case["id"]) in CASE_IDS]


def load_benchmark_runs() -> dict[tuple[str, str], dict[str, Any]]:
    benchmark = read_json(ITERATION_DIR / "benchmark.json")
    runs = {}
    for run in benchmark["runs"]:
        runs[(run["eval_name"], run["configuration"])] = run
    return runs


def quality_score_for(eval_name: str) -> dict[str, Any]:
    quality_path = ITERATION_DIR / "quality-grading.json"
    if not quality_path.exists():
        return {"status": "unavailable", "reason": "quality-grading.json not found"}

    quality = read_json(quality_path)
    for output in quality.get("outputs", {}).values():
        if f"eval-{eval_name}/with_skill" in output.get("file_path", ""):
            return {
                "status": "available",
                "total": output["total"],
                "scores": output["scores"],
                "rubric_version": quality.get("rubric_version"),
            }

    return {
        "status": "unavailable",
        "reason": "strict quality grading currently covers cases 1-3 only",
    }


def live_assertion(assertion: dict[str, Any]) -> dict[str, Any] | None:
    target = assertion.get("target", "")
    if target.startswith("old_skill/"):
        return None
    if not target.startswith("with_skill/outputs/"):
        return None

    adjusted = copy.deepcopy(assertion)
    adjusted["target"] = target.removeprefix("with_skill/outputs/")
    return adjusted


def grade_live_assertions(case: dict[str, Any], live_dir: Path) -> dict[str, Any]:
    metadata_path = ITERATION_DIR / f"eval-{case['name']}" / "eval_metadata.json"
    metadata = read_json(metadata_path)
    expectations = []
    passed = 0

    for assertion in metadata.get("assertions", []):
        adjusted = live_assertion(assertion)
        if adjusted is None:
            continue
        ok, evidence = check_assertion(adjusted, live_dir)
        expectations.append({
            "text": adjusted["text"],
            "passed": ok,
            "evidence": evidence,
            "target": adjusted["target"],
        })
        if ok:
            passed += 1

    total = len(expectations)
    return {
        "passed": passed,
        "failed": total - passed,
        "total": total,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "expectations": expectations,
    }


def artifact_completeness(case: dict[str, Any], live_dir: Path) -> dict[str, Any]:
    required_paths = [
        "seed-brief.md",
        "merged-requirements.md",
        "return-contract.yaml",
        "adversarial",
    ]
    if case.get("handoff") in {"tasklist", "task", "design"}:
        required_paths.append("handoff")

    artifacts = []
    present = 0
    for rel in required_paths:
        path = live_dir / rel
        exists = path.exists()
        artifacts.append({"path": rel, "present": exists})
        if exists:
            present += 1

    return {
        "present": present,
        "total": len(required_paths),
        "complete": present == len(required_paths),
        "artifacts": artifacts,
    }


def live_contract(live_dir: Path) -> dict[str, Any]:
    path = live_dir / "return-contract.yaml"
    if not path.exists():
        return {"status": "missing"}
    return parse_yaml_simple(read_text(path))


def live_timing(live_dir: Path) -> dict[str, Any]:
    timing_paths = sorted(live_dir.glob("**/timing.json"))
    if not timing_paths:
        return {
            "status": "unavailable",
            "reason": "live run artifacts do not include timing.json/token telemetry",
        }
    timing = read_json(timing_paths[0])
    return {
        "status": "available",
        "time_seconds": timing.get("total_duration_seconds"),
        "tokens": timing.get("total_tokens"),
        "tool_calls": timing.get("tool_uses", 0),
        "source": str(timing_paths[0].relative_to(ROOT)),
    }


def note_for(case: dict[str, Any], contract: dict[str, Any], timing: dict[str, Any], quality: dict[str, Any]) -> str:
    notes = []
    expected_proposals = str(case.get("expected_proposal_count"))
    actual_proposals = contract.get("proposal_count")
    if actual_proposals and str(actual_proposals) != expected_proposals:
        notes.append(f"proposal_count {actual_proposals} vs expected {expected_proposals}")
    expected_domain = case.get("expected_domain")
    actual_domain = contract.get("domain")
    if actual_domain and actual_domain != expected_domain:
        notes.append(f"domain {actual_domain} vs expected {expected_domain}")
    if timing["status"] == "unavailable":
        notes.append("live runtime/token telemetry unavailable")
    if quality["status"] == "unavailable":
        notes.append("quality score unavailable")
    return "; ".join(notes) if notes else "none"


def compare_case(case: dict[str, Any], runs: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any]:
    eval_name = case["name"]
    live_dir = LIVE_ROOT / f"eval-{eval_name}"
    baseline_run = runs.get((eval_name, "with_skill"))
    baseline_result = baseline_run["result"] if baseline_run else None
    live_summary = grade_live_assertions(case, live_dir) if live_dir.exists() else None
    contract = live_contract(live_dir)
    timing = live_timing(live_dir) if live_dir.exists() else {"status": "missing"}
    quality = quality_score_for(eval_name)

    live_pass_rate = live_summary["pass_rate"] if live_summary else None
    baseline_pass_rate = baseline_result["pass_rate"] if baseline_result else None
    pass_rate_delta = None
    if live_pass_rate is not None and baseline_pass_rate is not None:
        pass_rate_delta = round(live_pass_rate - baseline_pass_rate, 4)

    return {
        "eval_id": case["id"],
        "eval_name": eval_name,
        "topic": case["topic"],
        "live_dir": str(live_dir.relative_to(ROOT)),
        "baseline": baseline_result,
        "live": {
            "exists": live_dir.exists(),
            "contract": contract,
            "assertions": live_summary,
            "artifact_completeness": artifact_completeness(case, live_dir) if live_dir.exists() else None,
            "timing": timing,
            "quality": quality,
        },
        "deltas": {
            "pass_rate": pass_rate_delta,
            "time_seconds": None,
            "tokens": None,
        },
        "notes": note_for(case, contract, timing, quality),
    }


def summarize(cases: list[dict[str, Any]]) -> dict[str, Any]:
    live_cases = [case for case in cases if case["live"]["exists"]]
    assertion_cases = [case for case in live_cases if case["live"]["assertions"]]
    complete_cases = [case for case in live_cases if case["live"]["artifact_completeness"]["complete"]]
    baseline_rates = [case["baseline"]["pass_rate"] for case in cases if case["baseline"]]
    live_rates = [case["live"]["assertions"]["pass_rate"] for case in assertion_cases]

    quality_available = sum(1 for case in cases if case["live"]["quality"]["status"] == "available")
    quality_unavailable = sum(1 for case in cases if case["live"]["quality"]["status"] == "unavailable")
    timing_available = sum(1 for case in cases if case["live"]["timing"]["status"] == "available")
    timing_unavailable = sum(1 for case in cases if case["live"]["timing"]["status"] in {"unavailable", "missing"})

    return {
        "case_count": len(cases),
        "compared_case_ids": sorted(CASE_IDS),
        "excluded_case_ids": sorted(EXCLUDED_CASE_IDS),
        "excluded_case_reason": EXCLUDED_CASE_REASON,
        "live_artifact_cases": len(live_cases),
        "complete_artifact_cases": len(complete_cases),
        "mean_baseline_pass_rate": round(sum(baseline_rates) / len(baseline_rates), 4) if baseline_rates else None,
        "mean_live_pass_rate": round(sum(live_rates) / len(live_rates), 4) if live_rates else None,
        "quality_scores_available": quality_available,
        "quality_unavailable_count": quality_unavailable,
        "live_timing_available": timing_available,
        "telemetry_unavailable_count": timing_unavailable,
        "availability_gaps": {
            "quality": (
                "explicit gap: strict quality grading not yet covering compared cases"
                if quality_unavailable
                else "covered"
            ),
            "timing_tokens": (
                "explicit gap: live runs do not write timing.json / token telemetry; comparison "
                "cannot validate telemetry assertions until this lands"
                if timing_unavailable
                else "covered"
            ),
        },
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    s = report["summary"]
    compared_ids = ", ".join(str(i) for i in s["compared_case_ids"])
    excluded_ids = ", ".join(str(i) for i in s["excluded_case_ids"]) or "none"
    mean_baseline = s["mean_baseline_pass_rate"]
    mean_live = s["mean_live_pass_rate"]
    baseline_text = "n/a" if mean_baseline is None else f"{mean_baseline:.2%}"
    live_text = "n/a" if mean_live is None else f"{mean_live:.2%}"

    lines = [
        "# sc-brainstorm live-run comparison against iteration-2 baseline",
        "",
        f"Generated: {report['metadata']['generated_at']}",
        "",
        "## Scope",
        "",
        f"- Compared cases: {compared_ids}",
        f"- Excluded cases: {excluded_ids}",
        f"- Exclusion rationale: {s['excluded_case_reason']}",
        "",
        "## Summary",
        "",
        f"- Cases compared: {s['case_count']} (ids {compared_ids})",
        f"- Live artifact cases present: {s['live_artifact_cases']}",
        f"- Complete artifact cases: {s['complete_artifact_cases']}",
        f"- Mean baseline structural pass rate: {baseline_text}",
        f"- Mean live structural pass rate: {live_text}",
        f"- Quality scores available: {s['quality_scores_available']} of {s['case_count']}",
        f"- Quality unavailable (explicit gap): {s['quality_unavailable_count']} of {s['case_count']}",
        f"- Live timing/token telemetry available: {s['live_timing_available']} of {s['case_count']}",
        f"- Telemetry unavailable (explicit gap): {s['telemetry_unavailable_count']} of {s['case_count']}",
        "",
        "### Availability gaps",
        "",
        f"- Quality: {s['availability_gaps']['quality']}",
        f"- Timing/tokens: {s['availability_gaps']['timing_tokens']}",
        "",
        "Availability gaps are reported as explicit shortfalls rather than silent passes; "
        "unavailable quality and unavailable telemetry MUST NOT be treated as remediation acceptance.",
        "",
        "## Case comparison",
        "",
        "| # | Eval | Baseline pass | Live pass | Δ pass | Artifacts | Baseline time | Live time | Baseline tokens | Live tokens | Contract | Quality | Notes |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]

    for case in report["cases"]:
        baseline = case["baseline"] or {}
        live_assertions = case["live"]["assertions"] or {}
        completeness = case["live"]["artifact_completeness"] or {"present": 0, "total": 0}
        contract = case["live"]["contract"]
        quality = case["live"]["quality"]
        timing = case["live"]["timing"]
        delta = case["deltas"]["pass_rate"]
        delta_text = "n/a" if delta is None else f"{delta:+.2%}"
        quality_text = quality.get("total", quality["status"])
        live_time = timing.get("time_seconds", timing["status"])
        live_tokens = timing.get("tokens", timing["status"])
        lines.append(
            f"| {case['eval_id']} | `{case['eval_name']}` | "
            f"{baseline.get('passed', 0)}/{baseline.get('total', 0)} | "
            f"{live_assertions.get('passed', 0)}/{live_assertions.get('total', 0)} | "
            f"{delta_text} | "
            f"{completeness['present']}/{completeness['total']} | "
            f"{baseline.get('time_seconds', 'n/a')} | "
            f"{live_time} | "
            f"{baseline.get('tokens', 'n/a')} | "
            f"{live_tokens} | "
            f"{contract.get('status', 'missing')} | "
            f"{quality_text} | "
            f"{case['notes']} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    runs = load_benchmark_runs()
    cases = [compare_case(case, runs) for case in load_evals()]
    report = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "baseline": str(ITERATION_DIR.relative_to(ROOT)),
            "live_root": str(LIVE_ROOT.relative_to(ROOT)),
            "path_mapping": "live run directory = live-runs/eval-{eval.name}",
        },
        "summary": summarize(cases),
        "cases": cases,
    }
    json_path = LIVE_ROOT / "comparison-against-iteration-2.json"
    md_path = LIVE_ROOT / "comparison-against-iteration-2.md"
    write_json(json_path, report)
    write_markdown(md_path, report)
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
