#!/usr/bin/env python3
"""Inspect Task 4 product preservation and real native output, not process-exit claims."""

import argparse
import hashlib
import json
import re
import runpy
import subprocess
import time
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
RUNTIME = OUT / "task4-runtime"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blocks(event):
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    return [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []


def model_of(event):
    message = event.get("message")
    return message.get("model", "") if isinstance(message, dict) else ""


def main():
    global RUNTIME
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", default="task4-runtime")
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()
    RUNTIME = OUT / args.runtime
    if RUNTIME.parent != OUT:
        parser.error("runtime must be an immediate evidence child")
    baseline = json.loads((OUT / "task4-baseline.json").read_text())
    contract = json.loads((OUT / "plugin-contract.json").read_text())
    checks = {}
    cwd_guard = runpy.run_path(str(OUT / "task4-cwd-audit.py"))
    cwd_guard["self_check"]()

    def check(name, passed, details):
        checks[name] = {"pass": bool(passed), "details": details}

    changed = [path for path, digest in baseline["sha256"].items() if path != "commands/sc-reflect.md" and (not (ROOT / path).is_file() or sha(ROOT / path) != digest)]
    check("all_other_commands_resources_and_protected_bytes_preserved", not changed, {"checked": len(baseline["sha256"]) - 1, "changed": changed})
    command = (ROOT / "commands/sc-reflect.md").read_text()
    required = ("Skill sc:sc-reflect-protocol", "${CLAUDE_PLUGIN_ROOT}/skills/sc-reflect-protocol/SKILL.md", "--type task --analyze", "--type task --validate", "--commit-range", "sc:confidence-calibrator", "sc:evidence-validator", "sc:reflect-reviewer", "sc:merge-executor", "--no-promote", "remediation_unavailable: true", "superclaude` package executable", "stopped-precondition")
    forbidden = ("<200ms", "<1s", "task|session|completion", "Serena MCP**: Mandatory", "~/.claude/")
    check("root_entrypoint_modern_contract_and_local_binding", all(token in command for token in required) and not any(token in command for token in forbidden), {"missing": [token for token in required if token not in command], "obsolete": [token for token in forbidden if token in command]})
    retired = list(contract["producer_retirement"]) + ["commands/sc-estimate.md", "commands/sc-sc.md", "commands/sc-select-tool.md"]
    check("retired_producer_and_commands_remain_absent", not any((ROOT / path).exists() for path in retired), retired)
    expected = {row["path"] for row in contract["commands"]} | {row["path"] for row in contract["existing_agents"]} | {row["destination"] for row in contract["candidate_resources"]} | {path for path in contract["protected_sha256"] if path.startswith("skills/")} | {".claude-plugin/plugin.json"}
    actual = {str(path.relative_to(ROOT)) for folder in ("commands", "agents", "skills", ".claude-plugin") for path in (ROOT / folder).rglob("*") if path.is_file()}
    check("exact_bounded_product_inventory", actual == expected, {"unexpected": sorted(actual - expected), "missing": sorted(expected - actual)})
    index = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True)
    check("index_unchanged", not index.strip(), index)
    check("head_unchanged", subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == baseline["head"], baseline["head"])
    fixture = json.loads((RUNTIME / "fixture-contents.json").read_text())
    copy_drift = [path for path, digest in fixture["actual_plugin_copy_sha256"].items() if not (RUNTIME / "plugin" / path).is_file() or sha(RUNTIME / "plugin" / path) != digest or sha(ROOT / path) != digest]
    check("actual_isolated_copy_matches_current_product", not copy_drift, copy_drift)
    case_results = {}
    for name in args.case:
        case = RUNTIME / "runs" / name
        execution = json.loads((case / "execution.json").read_text())
        init = json.loads((case / "native-init.json").read_text())
        artifacts = case / "artifacts"
        raw_events = []
        trace_paths = [case / "stdout.jsonl", *sorted(case.glob("stdout-resume-*.jsonl"))]
        for trace_path in trace_paths:
            for line in trace_path.read_text().splitlines():
                try:
                    raw_events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        calls = [{"parent_tool_use_id": event.get("parent_tool_use_id"), "tool": block["name"], "input": block.get("input", {})} for event in raw_events for block in blocks(event) if block.get("type") == "tool_use"]
        continuation_records = [json.loads(path.read_text()) for path in sorted(case.glob("resume-*-execution.json"))]
        agent_calls = {block["id"]: block["input"] for event in raw_events for block in blocks(event) if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task")}
        agent_returns = {block["tool_use_id"]: block for event in raw_events for block in blocks(event) if block.get("type") == "tool_result" and block.get("tool_use_id") in agent_calls}
        successful_roles = [spec.get("subagent_type") for identity, spec in agent_calls.items() if identity in agent_returns and not agent_returns[identity].get("is_error") and agent_returns[identity].get("content")]
        roles = [row["input"].get("subagent_type") for row in calls if row["tool"] in ("Agent", "Task")]
        skills = [row["input"].get("skill") for row in calls if row["tool"] == "Skill"]
        mode = execution["case"]
        negative = mode in ("missing-pre", "missing-post", "unsafe-output", "readiness-unavailable", "invalid-commit-range")
        paths = [artifacts / "return-contract.yaml"] if (artifacts / "return-contract.yaml").is_file() else []
        parsed = []
        for path in paths:
            try:
                value = yaml.safe_load(path.read_text())
                if isinstance(value, dict):
                    parsed.append({"path": str(path), "value": value})
            except yaml.YAMLError:
                pass
        returns = {block["tool_use_id"]: block for event in raw_events for block in blocks(event) if block.get("type") == "tool_result"}
        out_of_scope_reads = []
        for event in raw_events:
            for block in blocks(event):
                if block.get("type") != "tool_use" or block.get("name") != "Read":
                    continue
                path = Path(block.get("input", {}).get("file_path", "."))
                result = returns.get(block.get("id"), {})
                if path.is_absolute() and not any(path.is_relative_to(allowed) for allowed in (RUNTIME / "fixtures/project", RUNTIME / "plugin", case, Path(execution["cwd"]))) and result and not result.get("is_error"):
                    out_of_scope_reads.append({"path": str(path), "parent_tool_use_id": event.get("parent_tool_use_id")})
        shell_transitions = []
        for index, event in enumerate(raw_events):
            for block in blocks(event):
                if block.get("type") == "tool_use" and block.get("name") == "Bash" and block.get("id") in returns and not returns[block["id"]].get("is_error"):
                    command_text = block.get("input", {}).get("command", "")
                    transitions = cwd_guard["shell_transitions"](command_text)
                    if transitions:
                        shell_transitions.append({"event": index, "parent": event.get("parent_tool_use_id"), "commands": transitions, "command": command_text})
        actual_cwd_records = []
        seen_cwd_records = set()
        for transcript in (case / "config").rglob("*.jsonl"):
            for line in transcript.read_text().splitlines():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("cwd") and (str(transcript), row["cwd"]) not in seen_cwd_records:
                    seen_cwd_records.add((str(transcript), row["cwd"]))
                    actual_cwd_records.append({"transcript": str(transcript), "cwd": row["cwd"], "pass": cwd_guard["persisted_cwd_allowed"](row["cwd"], execution["cwd"], RUNTIME / "fixtures/project")})
        result_text = json.dumps(execution.get("native_result", {}))
        case_checks = {
            "native_exited_zero": execution["state"] == "exited" and execution["returncode"] == 0 and all(row.get("state") == "exited" and row.get("returncode") == 0 and not row.get("changed_plugin_files") and not row.get("changed_audit_inputs") for row in continuation_records),
            "inputs_plugin_unmodified": not execution["changed_plugin_files"] and not execution["changed_audit_inputs"] and not execution.get("added_plugin_files", []) and not execution.get("fixture_staged_files", []) and not execution.get("fixture_head_created", False),
            "isolated_native_environment": not init.get("mcp_servers") and Path(execution["cwd"]).parent == Path("/tmp") and execution["framework_executable_absent"] and "--bare" not in execution["command"] and "--restricted" in execution["command"],
            "root_command_dispatched": execution["command"][-1].startswith("/sc:sc-reflect "),
            "actual_launch_bytes_match_frozen_final_product": execution.get("plugin_sha256_at_launch") == fixture["actual_plugin_copy_sha256"] and all(row.get("plugin_sha256_at_launch") == fixture["actual_plugin_copy_sha256"] for row in continuation_records),
            "no_successful_file_reads_outside_isolated_roots": not out_of_scope_reads,
            "no_successful_shell_directory_transitions": not shell_transitions,
            "actual_all_role_cwd_exactly_launch_or_audit_root": bool(actual_cwd_records) and all(row["pass"] for row in actual_cwd_records),
            "declared_native_cwd_deny_profile": all(rule in execution["command"] for rule in ("Bash(cd *)", "Bash(cd)", "Bash(pushd *)", "Bash(popd *)")),
        }
        if negative:
            case_checks["no_audit_roles_started_for_refusal"] = not any(role in {"sc:confidence-calibrator", "sc:evidence-validator", "sc:reflect-reviewer", "sc:sc-root-cause-analyst", "sc:sc-requirements-analyst"} for role in roles)
            case_checks["refusal_not_misreported_as_success"] = not parsed or all(row["value"].get("status") not in ("success", "partial") for row in parsed)
            case_checks["honest_refusal_or_unavailable"] = bool(re.search(r"stop|refus|unavailable|invalid|missing|cannot|require", result_text, re.IGNORECASE))
            if mode == "unsafe-output":
                case_checks["unsafe_destination_never_created"] = not (RUNTIME / "plugin/skills/forbidden-runtime-output").exists()
        else:
            case_checks["bundled_protocol_called"] = "sc:sc-reflect-protocol" in skills
            case_checks["real_report_and_contract_exist"] = (artifacts / "REPORT.md").is_file() and bool(parsed)
            case_checks["independent_calibrator_called"] = "sc:confidence-calibrator" in successful_roles
            case_checks["independent_evidence_validator_called"] = "sc:evidence-validator" in successful_roles
            calibrator_spot_checks = []
            for identity, spec in agent_calls.items():
                if spec.get("subagent_type") != "sc:confidence-calibrator":
                    continue
                reads = [Path(block["input"]["file_path"]) for event in raw_events if event.get("parent_tool_use_id") == identity for block in blocks(event) if block.get("type") == "tool_use" and block.get("name") == "Read" and block.get("input", {}).get("file_path") and block.get("id") in returns and not returns[block["id"]].get("is_error")]
                actual_sources = [str(path) for path in reads if path.is_relative_to(RUNTIME / "fixtures/project") or path.is_relative_to(artifacts / "reviewer-snapshot/root")]
                card_paths = [path for path in reads if path.is_relative_to(artifacts) and "card" in path.name and path.suffix in (".md", ".yaml", ".yml", ".json")]
                references = set()
                for card_path in card_paths:
                    references.update(re.findall(r"[A-Za-z0-9_./-]+\.(?:py|md|yaml|yml|json|patch|log):[0-9]+", card_path.read_text()))
                cited_keys = set()
                for reference in references:
                    path = Path(reference.rsplit(":", 1)[0])
                    for source_root in (RUNTIME / "fixtures/project", artifacts / "reviewer-snapshot/root"):
                        if path.is_absolute() and path.is_relative_to(source_root):
                            cited_keys.add(str(path.relative_to(source_root)))
                    if not path.is_absolute():
                        cited_keys.add(str(path).removeprefix("./").removeprefix("root/"))
                matched_sources = []
                for source in map(Path, actual_sources):
                    for source_root in (RUNTIME / "fixtures/project", artifacts / "reviewer-snapshot/root"):
                        if source.is_relative_to(source_root) and str(source.relative_to(source_root)) in cited_keys:
                            matched_sources.append(str(source))
                calibrator_spot_checks.append({"model": spec.get("model"), "input_cards": list(map(str, card_paths)), "cited_source_keys": sorted(cited_keys), "source_reads": actual_sources, "matched_cited_source_reads": sorted(set(matched_sources)), "pass": bool(matched_sources)})
            case_checks["calibrators_actually_spot_check_cited_sources"] = bool(calibrator_spot_checks) and all(row["pass"] for row in calibrator_spot_checks)
            calibration_math = []
            dimension_names = ("Citation grounding", "Coverage completeness", "Deviation-classification clarity", "Risk surface coverage", "Recommendation actionability")
            dimension_keys = ("citation_grounding", "coverage_completeness", "deviation_classification_clarity", "risk_surface_coverage", "recommendation_actionability")
            for calibration_path in artifacts.rglob("*"):
                if "reviewer-snapshot" in calibration_path.relative_to(artifacts).parts or ("calibrat" not in str(calibration_path.relative_to(artifacts)) and calibration_path.name != "reflection-card.yaml") or not calibration_path.is_file() or calibration_path.suffix not in (".md", ".yaml", ".yml", ".json"):
                    continue
                calibration_text = calibration_path.read_text()
                if calibration_path.name == "reflection-card.yaml" and not re.search(r"^(?:calibrator|calibrator_agent):", calibration_text, re.MULTILINE):
                    continue  # Canonical calibration output only, not the unscored author input card.
                scores = []
                claimed = None
                if calibration_path.suffix == ".md":
                    plain = calibration_text.replace("**", "")
                    for dimension in dimension_names:
                        match = re.search(r"^\|\s*" + re.escape(dimension) + r"\s*\|\s*([01](?:\.\d+)?)\s*\|", plain, re.MULTILINE)
                        if match:
                            scores.append(float(match.group(1)))
                    match = re.search(r"\bCalibrated(?:\s*\([^)]+\))?\s*:\s*([01](?:\.\d+)?)", plain, re.IGNORECASE)
                    claimed = float(match.group(1)) if match else None
                else:
                    data = yaml.safe_load(calibration_text)
                    if isinstance(data, dict):
                        if data.get("author_agent") and not data.get("calibrator_agent"):
                            continue  # Input card, not the calibrator's returned scoring report.
                        dimensions = data.get("dimensions", data.get("per_dimension", data.get("dimension_scores", data.get("per_dimension_scores", data.get("scores", {})))))
                        if set(dimensions) == set(dimension_keys):
                            scores = [float(dimensions[key].get("score") if isinstance(dimensions[key], dict) else dimensions[key]) for key in dimension_keys]
                        claimed = data.get("confidence_calibrated", data.get("C_reported_by_calibrator", data.get("calibrated_confidence", data.get("calibrated", data.get("C", data.get("arithmetic_mean_C", data.get("arithmetic_mean")))))))
                calibration_math.append({"path": str(calibration_path), "scores": scores, "claimed": claimed, "pass": len(scores) == 5 and all(0 <= score <= 1 for score in scores) and isinstance(claimed, (int, float)) and abs(sum(scores) / 5 - claimed) <= 0.005001})
            case_checks["calibration_five_dimension_math_verified"] = bool(calibration_math) and all(row["pass"] for row in calibration_math)
            validation_records = []
            for path in artifacts.rglob("*validat*"):
                if not path.is_file() or path.suffix not in (".md", ".yaml", ".yml", ".json"):
                    continue
                if path.suffix == ".md":
                    text = path.read_text().lower()
                    if "verified" in text and "dropped" in text:
                        validation_records.append(str(path))
                else:
                    data = yaml.safe_load(path.read_text())
                    if isinstance(data, dict):
                        summary = data.get("final", data)
                        total = summary.get("citations_total", summary.get("citations_grounded_occurrences"))
                        dropped = summary.get("citations_dropped", summary.get("dropped"))
                        revalidated = summary.get("citations_revalidated")
                        explicit_rows = summary.get("citations")
                        if revalidated is None and isinstance(explicit_rows, list) and all(isinstance(row, dict) and row.get("verdict") in {"verified", "line-mismatch", "file-missing", "snippet-mismatch"} for row in explicit_rows):
                            revalidated = len(explicit_rows)
                            if total != revalidated or dropped != sum(row["verdict"] != "verified" for row in explicit_rows):
                                revalidated = None
                        dropped_count = len(dropped) if isinstance(dropped, list) else dropped
                        if isinstance(total, int) and isinstance(revalidated, int) and isinstance(dropped_count, int) and 0 <= dropped_count <= revalidated <= total:
                            validation_records.append(str(path))
            case_checks["actual_validator_record_exists"] = bool(validation_records)
            snapshot_result = None
            reviewer_tools = []
            if parsed:
                value = parsed[-1]["value"]
                case_checks["contract_real_fields"] = all(key in value for key in ("contract_version", "status", "mode", "tier_reached", "confidence_calibrated", "evidence_validator_ran", "report_path"))
                case_checks["citation_gate_reports_actual_run"] = value.get("evidence_validator_ran") is True
                case_checks["no_promotion"] = value.get("promotion_action") in ("skipped", "not-applicable")
                if value.get("tier_reached") == 1:
                    case_checks["contract_confidence_matches_actual_calibration"] = any(row["pass"] and isinstance(value.get("confidence_calibrated"), (int, float)) and (row["claimed"] == value["confidence_calibrated"] or abs(sum(row["scores"]) / 5 - value["confidence_calibrated"]) < 0.000001) for row in calibration_math)
                case_checks["mcp_absence_reported_honestly"] = bool(value.get("degraded_components", value.get("telemetry", {}).get("degraded_components")))
                if mode == "post-tier2":
                    case_checks["forced_tier2_reached"] = value.get("tier_reached") == 2
                if value.get("tier_reached") == 2:
                    reviewers = [row for row in calls if row["tool"] in ("Agent", "Task") and row["input"].get("subagent_type") == "sc:reflect-reviewer"]
                    case_checks["distinct_restricted_reviewers"] = len(reviewers) >= 2 and len({row["input"].get("model") for row in reviewers}) >= 2
                    case_checks["real_adversarial_skill_and_merge_executor"] = "sc:sc-adversarial-protocol" in skills and "sc:debate-orchestrator" in successful_roles and "sc:merge-executor" in successful_roles
                    merge_returns = [index for index, event in enumerate(raw_events) for block in blocks(event) if block.get("type") == "tool_result" and agent_calls.get(block.get("tool_use_id"), {}).get("subagent_type") == "sc:merge-executor" and not block.get("is_error")]
                    final_validator_calls = [index for index, event in enumerate(raw_events) for block in blocks(event) if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task") and block.get("input", {}).get("subagent_type") == "sc:evidence-validator"]
                    case_checks["final_citation_gate_after_actual_merge"] = bool(merge_returns) and any(index > max(merge_returns) for index in final_validator_calls)
                    required_merge_artifacts = ("diff-analysis.md", "debate-transcript.md", "base-selection.md", "refactor-plan.md", "merge-log.md")
                    case_checks["actual_full_debate_merge_artifacts_exist"] = all(any(path.is_file() and path.stat().st_size > 100 for path in artifacts.rglob(filename)) for filename in required_merge_artifacts)
                    case_checks["every_card_independently_calibrated"] = successful_roles.count("sc:confidence-calibrator") >= len(reviewers) + 1 and len(calibration_math) >= len(reviewers) + 1
                    snapshot_root = artifacts / "reviewer-snapshot/root"
                    snapshot_manifest = artifacts / "reviewer-snapshot/provenance-manifest.json"
                    snapshot_result = None
                    try:
                        protocol_path = RUNTIME / "plugin/skills/sc-reflect-protocol/SKILL.md"
                        if sha(protocol_path) != baseline["task3_resource_sha256"]["skills/sc-reflect-protocol/SKILL.md"]:
                            raise ValueError("Changed snapshot recipe resource is not executed")
                        protocol = protocol_path.read_text()
                        snapshot_code = protocol.split("<!-- native-snapshot-recipe:start -->\n```python\n", 1)[1].split("\n```\n<!-- native-snapshot-recipe:end -->", 1)[0]
                        verification = subprocess.run([str(RUNTIME / "runtime-bin/uv"), "run", "--no-project", "python", "-", "--verify", str(snapshot_manifest)], input=snapshot_code, cwd=execution["cwd"], env=execution["environment"], text=True, capture_output=True, timeout=120)
                        snapshot_result = json.loads(verification.stdout.strip())
                        if verification.returncode != 0:
                            snapshot_result["status"] = "failed"
                    except Exception as error:
                        snapshot_result = {"status": "failed", "reason": str(error)}
                    case_checks["real_snapshot_source_copy_and_membership_verified"] = snapshot_result.get("status") == "verified" and snapshot_root.is_dir() and snapshot_root != RUNTIME / "fixtures/project"
                    reviewer_tools = []
                    for identity, spec in agent_calls.items():
                        if spec.get("subagent_type") != "sc:reflect-reviewer":
                            continue
                        nested = [block for event in raw_events if event.get("parent_tool_use_id") == identity for block in blocks(event) if block.get("type") == "tool_use"]
                        read_paths = [Path(block["input"]["file_path"]) for block in nested if block.get("name") == "Read" and block.get("input", {}).get("file_path")]
                        procedural_refs = {RUNTIME / "plugin" / row["destination"] for row in contract["candidate_resources"] if row["destination"].startswith("skills/sc-reflect-protocol/refs/") and sha(RUNTIME / "plugin" / row["destination"]) == baseline["task3_resource_sha256"][row["destination"]]}
                        allowed_reads = all(path.is_relative_to(snapshot_root) or path.is_relative_to(artifacts / "reviewer-briefs") or path in procedural_refs for path in read_paths)
                        reviewer_tools.append({"model": spec.get("model"), "observed_models": sorted({model_of(event) for event in raw_events if event.get("parent_tool_use_id") == identity} - {""}), "tools": sorted({block["name"] for block in nested}), "read_paths": list(map(str, read_paths)), "pass": bool(read_paths) and allowed_reads and all(block["name"] in {"Read", "Grep", "Glob"} for block in nested)})
                    case_checks["actual_reviewers_readonly_and_snapshot_grounded"] = len(reviewer_tools) >= 2 and all(row["pass"] for row in reviewer_tools)
                    case_checks["actual_provider_reviewer_models_distinct"] = len({tuple(row["observed_models"]) for row in reviewer_tools if row["observed_models"]}) >= 2
                    case_checks["tier2_real_disk_gate"] = value.get("tier_reached") == 2 and value.get("merge_method") == "adversarial" and (artifacts / "adversarial/merged-verdict.yaml").is_file() and len(value.get("reviewer_cards", [])) >= 2
                if mode == "remediation-unavailable":
                    case_checks["explicit_missing_handoff_no_executor"] = value.get("remediation_unavailable") is True and all(value.get(key) is None for key in ("remediation_task_path", "remediation_plan_path", "task_file_path", "handoff_memory_key")) and not any(row.get("input", {}).get("subagent_type") in {"task-builder", "rf-task-builder"} or row.get("input", {}).get("skill") in {"sc:workflow-protocol", "sc:sc-workflow-protocol", "task-builder", "task", "sc:sc-implement"} for row in calls if row["tool"] in ("Skill", "Agent", "Task"))
        case_results[name] = {"checks": case_checks, "pass": all(case_checks.values()), "roles": roles, "skills": skills, "contracts": parsed, "calibration_math": calibration_math if not negative else [], "calibrator_spot_checks": calibrator_spot_checks if not negative else [], "snapshot_verification": snapshot_result if not negative else None, "reviewer_tools": reviewer_tools if not negative else [], "out_of_scope_reads": out_of_scope_reads, "successful_cwd_transitions": shell_transitions, "actual_cwd_records": actual_cwd_records, "trace_paths": list(map(str, trace_paths)), "continuations": continuation_records, "execution": str(case / "execution.json")}
        check("runtime:" + name, all(case_checks.values()), case_results[name])
    expected_cases = {"pre-smoke", "pre-default", "post-default", "post-tier1", "post-tier2", "legacy-pre", "legacy-post", "post-log-only", "missing-pre", "missing-post", "unsafe-output", "remediation-unavailable", "readiness-unavailable", "invalid-commit-range"}
    if args.require_all:
        observed = {json.loads((RUNTIME / "runs" / name / "execution.json").read_text())["case"] for name in args.case}
        check("all_required_case_types_observed", expected_cases <= observed, {"missing": sorted(expected_cases - observed)})
    failed = [name for name, row in checks.items() if not row["pass"]]
    observed_cases = {json.loads((RUNTIME / "runs" / name / "execution.json").read_text())["case"] for name in args.case}
    case_outcomes = []
    for name, result in case_results.items():
        execution = json.loads(Path(result["execution"]).read_text())
        verdict = result["contracts"][-1]["value"] if result["contracts"] else {}
        case_outcomes.append({"case": execution["case"], "attempt": name, "native_exit": execution["returncode"], "status": verdict.get("status"), "mode": verdict.get("mode"), "tier": verdict.get("tier_reached"), "confidence": verdict.get("confidence_calibrated"), "stop_reason": verdict.get("stop_reason"), "merge_method": verdict.get("merge_method"), "evidence_validator_ran": verdict.get("evidence_validator_ran"), "producer_checks_pass": result["pass"], "output_directory": str(Path(result["execution"]).parent / "artifacts")})
    record = {"case_outcomes": case_outcomes, "runtime_case_types_missing": sorted(expected_cases - observed_cases), "all_cases_required_in_this_run": args.require_all, "verdict": "FAIL" if failed else "PASS", "checks": checks, "failed_checks": failed, "independent_review": "NOT CLAIMED; producer check only", "positive_commit_range_runtime": "Not claimed: synthetic Git fixture has no commits; invalid range refusal and static alternatives tested"}
    history = OUT / "task4-check-history"
    history.mkdir(exist_ok=True)
    current = OUT / "task4-check-output.json"
    if current.exists():
        previous = current.read_text()
        (history / f"{time.time_ns()}-previous.json").write_text(previous)
    record["runtime_fixture"] = str(RUNTIME)
    record["checker_sha256"] = sha(Path(__file__))
    encoded = json.dumps(record, indent=2) + "\n"
    (history / f"{time.time_ns()}-{RUNTIME.name}.json").write_text(encoded)
    current.write_text(encoded)
    print(json.dumps({"verdict": record["verdict"], "checks": len(checks), "failed_checks": failed}, indent=2))
    raise SystemExit(bool(failed))


if __name__ == "__main__":
    main()
