import hashlib, json, sys, datetime, subprocess
from pathlib import Path
P = Path(sys.argv[1]); PR = P/"fixtures/project"; OUT = P/"runs/post-default-attempt-1/artifacts"
snap = json.loads((OUT/"artifacts/input-snapshot.json").read_text())
fl = sorted([(r["path"], hashlib.sha256((PR/r["path"]).read_bytes()).hexdigest()) for r in snap["file_list"]])
th = hashlib.sha256(json.dumps(fl).encode()).hexdigest()
drift = th != snap["input_tree_sha256"]
status = subprocess.run(["git","-C",str(PR),"status","--porcelain","--untracked-files=all"],capture_output=True,text=True).stdout
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
(OUT/"artifacts/evidence-validation.yaml").write_text(json.dumps({
 "validator": "sc:evidence-validator", "requested_slot": "haiku", "returned_model": "grok-4.7[1m]", "agentId": "a72b02fa8be5da603",
 "draft": str(OUT/"REPORT.draft.md"), "citation_budget_policy": "full_reread",
 "citations_total": 19, "citations_revalidated": 19, "citations_verified": 18, "citations_dropped": 1, "citations_inferred": 1,
 "dropped": [{"id": "C17", "location": "tests/test_greeting.py:8-13", "original_claim": "the test asserts only the exception type, which is enough for R-003",
   "reason": "span is test_empty only; R-003 (spec.md:12) also requires the ordinary case; adequacy was inference stated as grounded"}],
 "coverage_recompute": "no affected coverage field (C17 was advisory; tasklist_completion_pct unchanged at 0.67)"}, indent=2) + "\n")
(OUT/"artifacts/confidence-check.yaml").write_text(json.dumps({
 "skill": "sc:confidence-check", "full_score": 0.525,
 "checks": {"no_duplicates": "pass (reuse-audit distinct)", "architecture": "partial: audited repo has no CLAUDE.md/PLANNING.md/pyproject.toml (explicit absence; ancestor config not read)",
   "official_docs": "fail: Context7 unavailable", "oss_reference": "fail: Tavily/WebSearch not used", "root_cause": "pass (GG-1, GG-2 explicit)"},
 "lightweight_form": {"R-001": "paths verified by Read", "R-002": "command [UNVERIFIED] — executing would write caches into audited repo", "R-003": "path verified by Read"},
 "disposition": "recommendations surfaced with R-002 marked [UNVERIFIED]; blocked_by_low_confidence=false (not every rec gated)"}, indent=2) + "\n")
contract = {
 "contract_version": "1.8.0", "status": "partial", "mode": "post", "tier_reached": 1,
 "report_path": str(OUT/"REPORT.md"), "audit_log_path": str(OUT/"audit.log"),
 "confidence_calibrated": 0.896, "escalation_rule_matched": 2, "onboarding_ran": False,
 "coverage_pct": None, "coverage_pct_union": None, "coverage_undefined": False, "coverage_degraded": None,
 "unmapped_requirements": [], "unmapped_requirements_union": [], "best_practice_grade": None,
 "implementation_coverage_pct": None, "missing_implementations": [], "hierarchy_slice_path": None, "hierarchy_coverage_pct": None,
 "tasklist_completion_pct": 0.67,
 "deviation_count_by_class": {"authorized": 0, "necessary": 0, "drift": 0, "regression": 0},
 "deviation_register_path": str(OUT/"deviation-ledger.yaml"), "grounding_gaps_path": str(OUT/"grounding-gaps.yaml"),
 "hunk_to_declaration_map_path": None, "third_party_api_grounding": [], "third_party_api_verified": False,
 "serena_summary_corroboration": "unavailable",
 "verification_ran": False, "verification_invocations": 0, "verification_failures": 0, "verification_regressions_detected": 0,
 "verification_skip_reason": "tool-unavailable",
 "runtime_surface_requirements": [], "runtime_surface_sweep_ran": False, "runtime_surface_ledger_path": None,
 "runtime_surface_unreached": 0, "runtime_surface_degraded": False, "unreached_surfaces": [],
 "reachability_gate_ran": False, "reachability_ledger_path": None, "reachability_requirements_scanned": 0,
 "reachability_unreachable": 0, "reachability_unproven": 0, "reachability_real_boot_ran": False,
 "reachability_skip_reason": "no-side-effect-requirements",
 "reuse_sweep_ran": True, "reuse_audit_path": str(OUT/"artifacts/reuse-audit.yaml"), "reuse_miss_blocking": 0, "reuse_miss_advisory": 0,
 "reuse_verdict_count_by_type": {"reuse_by_import": 0, "mirror_shape": 0, "extract_shared": 0, "distinct": 1},
 "reuse_grounding_gap_count": 0, "neighbour_search_sampled": False, "neighbour_search_degraded": True, "max_overlap_score": 0.0,
 "input_sha256": {"tasklist": dict(fl)["completed.md"], "spec": dict(fl)["spec.md"]},
 "input_tree_sha256": th, "input_tree_file_count": len(fl), "input_tree_snapshot_path": str(OUT/"artifacts/input-snapshot.json"),
 "input_drift_detected": drift, "input_drift_diff": None if not drift else "see audit.log",
 "citations_total": 19, "citations_revalidated": 19, "citations_dropped": 1, "citations_dropped_extrapolated": 1, "citations_inferred": 1,
 "citation_budget_policy": "full_reread", "evidence_validator_ran": True, "citation_revalidation_at_promotion": False,
 "reviewer_cards": [], "adversarial_artifacts_dir": None, "adversarial_convergence_score": None, "adversarial_unavailable": False,
 "merge_method": None, "t2_model_class_diversity": "full", "t2_vendor_diversity": "multi", "t2_effective_diversity": "full",
 "calibrator_diversity": "full",
 "remediation_offered": False, "remediation_accepted": None, "task_file_path": None, "remediation_task_path": None,
 "remediation_plan_path": None, "handoff_memory_key": None,
 "cannot_validate_without_user_input": True, "regression_present": False, "unauthorized_deviation_present": False,
 "blocked_by_low_confidence": False, "spec_is_wrong": False, "user_decision_required": True, "needs_human_decision": True,
 "per_task_verdicts": [
   {"task_id": "T-101", "status": "success", "deviation_class": "none", "citations_dropped": 0, "per_task_validation_strength": 0.896, "evidence_anchor": str(PR/"src/greeting.py")+":4"},
   {"task_id": "T-102", "status": "success", "deviation_class": "none", "citations_dropped": 0, "per_task_validation_strength": 0.896, "evidence_anchor": str(PR/"src/greeting.py")+":2-3"},
   {"task_id": "T-103", "status": "partial", "deviation_class": "none", "citations_dropped": 1, "per_task_validation_strength": None, "evidence_anchor": str(PR/"tests/test_greeting.py")+":4-13"}],
 "per_task_validation_strength_note": "T-101/T-102 carry the run-level calibrated C (no per-task calibration run); T-103 null because its evidence is unattributable (GG-1)",
 "interaction_effects_scanned": False, "interaction_effects_findings": 0,
 "budget_forced_tier_downgrade": False, "budget_forced_stop": False, "budget_check_skipped": True, "forced_tier": None,
 "promotion_action": "skipped", "promotion_adapter": None, "promotion_source": None, "promotion_destination": None,
 "promotion_log_path": None, "promotion_gate_passed": None, "promotion_skip_reason": "user-flag", "promotion_fail_reason": None,
 "promotion_override_used": None, "promotion_rollback_command": None, "promotion_checkpoint_path": None,
 "promotion_cross_fs": False, "promotion_pending": False,
 "telemetry": {
   "reviewer_models": [], "role_models": {
     "card_author": {"agent": "sc:sc-root-cause-analyst", "requested_slot": "sonnet", "returned": "claude-sonnet-5-5[1m]"},
     "reuse_auditor": {"agent": "sc:reuse-auditor", "requested_slot": "sonnet", "returned": "claude-sonnet-5-5[1m]"},
     "calibrator": {"agent": "sc:confidence-calibrator", "requested_slot": "opus", "returned": "claude-opus-5-5[1m]"},
     "evidence_validator": {"agent": "sc:evidence-validator", "requested_slot": "haiku", "returned": "grok-4.7[1m]"}},
   "degraded_components": ["serena", "auggie", "get_current_config", "serena:onboarding-parse", "context7", "tavily", "execute_shell_command", "neighbour-search:auggie_unavailable"],
   "fallback_path": None, "executor_class_source": "unknown", "executor_class_resolved": False, "executor_exclusion_degraded": False,
   "onboarding_status": "unknown", "serena_version": "unknown", "deviation_aggregation_mode": "per-hunk",
   "audit_repo_root": str(PR), "git_status_at_finalize": status.splitlines(),
   "not_written": "global .dev/reflect/runs.jsonl (outside the permitted output root); serena memory (unavailable)"}}
(OUT/"return-contract.yaml").write_text(json.dumps(contract, indent=2) + "\n")
print("drift:", drift, th); print(status)
