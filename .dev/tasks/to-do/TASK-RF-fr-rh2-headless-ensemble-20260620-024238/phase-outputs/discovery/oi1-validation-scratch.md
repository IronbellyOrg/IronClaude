# OI-1 validation scratch — swarm ResultContract → reflect verdict field correspondence

Status: In Progress
Date: 2026-06-20
Task step: 0.1a

## Acceptance gate checked

Spec §11 OI-1 asks: "Does reflect's swarm contract already emit `reviewer_count`/`merge_method`/`t2_model_class_diversity` in the exact shape `contract.derive_verdict` reads, or must `ensemble.py` map them? Produce an explicit swarm-`ResultContract`-field → reflect-contract-field correspondence table." It must be resolved before FR-RH2.3 code lands.

## Shipped-source field inventory

### Swarm source surface

- `src/superclaude/cli/swarm/models.py:68-69` defines `ResultStatus = Literal["success", "partial", "failed"]` and `WorkerStatus = Literal["success", "timeout", "parse_error", "proxy_error"]`.
- `src/superclaude/cli/swarm/models.py:997-1015` defines `ResultContract` fields: `contract_version`, `status`, `job_id`, `started`, `finished`, `elapsed_ms`, `caller`, `lens`, `lens_source`, `target`, `workers_requested`, `workers_succeeded`, `workers_failed`, `output_files`, `amalgamation_mode`, `merged_path`, `caller_metadata`, `recommended_next_command`, `artifacts`.
- `src/superclaude/cli/swarm/models.py:1117-1128` defines `WorkerResult` fields: `index`, `path`, `raw_path`, `meta_path`, `final_path`, `model_id`, `model_label`, `bytes`, `status`, `http_code`, `attempts`, `elapsed_ms`.
- Grep check against `src/superclaude/cli/swarm/` for `tier_reached|merge_method|t2_model_class_diversity|t2_vendor_diversity|reviewer_count|adversarial_convergence_score` returned zero matches. The named reflect verdict fields are absent from the swarm seam. The only shared key name among the load-bearing surfaces is `status`, but swarm `ResultContract.status` is a worker-count result status, not reflect's post-audit status.

### Reflect consumer surface

- `src/superclaude/cli/reflect/contract.py:47-57` declares load-bearing boolean fields whose malformed values block.
- `src/superclaude/cli/reflect/contract.py:90-101` reads `deviation_count_by_class` through `_extract_deviations`.
- `src/superclaude/cli/reflect/contract.py:104-127` reads telemetry into `ReflectResult`: `status` at line 116, `tier_reached` at lines 113/117, `report_path` at line 119, `deviation_count_by_class` via `_extract_deviations` at line 121, and `remediation_task_path` at line 126.
- `src/superclaude/cli/reflect/contract.py:147-246` implements `derive_verdict` with blocked → degraded → halted → pass ordering; `contract_version` gates at lines 166-176, `degraded_components` shape at lines 183-190, load-bearing bool shape at lines 200-206, and pass gate `status == "success" and tier_reached == expected_tier` at lines 234-238.
- `src/superclaude/cli/reflect/contract.py:249-304` implements degraded triggers, including model-class diversity at lines 266-269, vendor diversity at lines 271-273, adversarial unavailable at lines 275-277, single-reviewer fallback at lines 279-281, null convergence at lines 283-285, verification skipped at lines 287-290, citations dropped at lines 294-297, and input drift at lines 300-302.
- `src/superclaude/cli/reflect/contract.py:307-328` implements halted triggers: status failed/partial at lines 311-313, regression at line 315, unauthorized deviation at line 317, needs human decision at line 319, user decision required at line 321, and deviation counts at lines 323-326.

## Per-field validation results

| # | Reflect field | Result | Shipped-source confirmation / drift |
|---|---|---|---|
| 1 | `contract_version` | CONFIRMED-against-shipped | Reflect gates major-1 `contract_version` at `contract.py:166-176`. Swarm has `ResultContract.contract_version` at `models.py:997`, but this belongs to DM-012; research claim that reflect must synthesize its own major-1 contract literal is confirmed. |
| 2 | `status` | DRIFT-FLAGGED (line anchor only) | Reflect reads status at `_make_result` `contract.py:116`, halted checks at `contract.py:311-313`, and PASS gate at `contract.py:235`. Research cited `_make_result`:118, but shipped line 118 is `reason`; the field read is line 116. Provenance remains CONFIRMED: swarm `ResultContract.status` exists at `models.py:998` with `ResultStatus` values at `models.py:68`, but semantics differ, so reflect status must be derived rather than passed through. |
| 3 | `tier_reached` | DRIFT-FLAGGED (line anchor only) | Reflect reads raw `tier_reached` at `contract.py:195`, reports it through `_make_result` at `contract.py:113/117`, gates PASS at `contract.py:235`, degrades expected T2→T1 at `contract.py:262-264`, and null-convergence at `contract.py:283-285`. Swarm has no `tier_reached` grep hit; provenance DERIVED from M is confirmed. |
| 4 | `degraded_components` | CONFIRMED-against-shipped | Reflect reads and shape-checks `degraded_components` at `contract.py:183-190`; degraded trigger 1-5 membership is `contract.py:258-260`. No swarm equivalent exists in `ResultContract`/`WorkerResult`; SYNTHESIZED default `[]` confirmed. |
| 5 | `deviation_count_by_class` | CONFIRMED-against-shipped | Reflect reads it in `_extract_deviations` at `contract.py:90-101`, and halted uses regression/drift counts at `contract.py:323-326`; `_make_result` calls `_extract_deviations` at `contract.py:121`. No swarm equivalent exists; SYNTHESIZED `{}`/zero default confirmed. |
| 6 | `report_path` | CONFIRMED-against-shipped | Reflect telemetry reads `report_path` at `contract.py:119`. Swarm can supply a related path via `ResultContract.merged_path` at `models.py:1012` and/or per-worker `WorkerResult.final_path` at `models.py:1121`; mapping/derivation is required because there is no swarm `report_path`. |
| 7 | `remediation_task_path` | CONFIRMED-against-shipped | Reflect telemetry reads `remediation_task_path` at `contract.py:126`. No swarm equivalent exists; SYNTHESIZED `None`/omitted default confirmed. |
| 8 | `regression_present` | CONFIRMED-against-shipped | Reflect validates load-bearing bool shape via `contract.py:47-57` and `contract.py:200-206`, and halted trigger reads line `contract.py:315`. No swarm equivalent exists; SYNTHESIZED/omitted default confirmed. |
| 9 | `unauthorized_deviation_present` | CONFIRMED-against-shipped | Reflect validates load-bearing bool shape via `contract.py:47-57` and `contract.py:200-206`, and halted trigger reads `contract.py:317`. No swarm equivalent exists; SYNTHESIZED/omitted default confirmed. |
| 10 | `needs_human_decision` | CONFIRMED-against-shipped | Reflect validates load-bearing bool shape via `contract.py:47-57` and `contract.py:200-206`, and halted trigger reads `contract.py:319`. No swarm equivalent exists; SYNTHESIZED/omitted default confirmed. |
| 11 | `user_decision_required` | CONFIRMED-against-shipped | Reflect validates load-bearing bool shape via `contract.py:47-57` and `contract.py:200-206`, and halted trigger reads `contract.py:321`. No swarm equivalent exists; SYNTHESIZED/omitted default confirmed. |
| 12 | `adversarial_unavailable` | CONFIRMED-against-shipped | Reflect validates load-bearing bool shape via `contract.py:47-57` and `contract.py:200-206`; degraded trigger 9 reads `contract.py:275-277`. No swarm equivalent exists; DERIVED from adversarial child launch outcome rather than swarm. |
| 13 | `input_drift_detected` | CONFIRMED-against-shipped | Reflect validates load-bearing bool shape via `contract.py:47-57` and `contract.py:200-206`; degraded trigger 14 reads `contract.py:300-302`. No swarm equivalent exists; SYNTHESIZED/omitted default confirmed. |
| 14 | `verification_ran` | CONFIRMED-against-shipped | Reflect validates load-bearing bool shape via `contract.py:47-57` and `contract.py:200-206`; degraded trigger 12 reads `contract.py:287-290`. No swarm equivalent exists; SYNTHESIZED/omitted or reflect-child sourced default confirmed. |
| 15 | `verification_skip_reason` | CONFIRMED-against-shipped | Reflect reads paired skip reason at `contract.py:289` with exemptions at `contract.py:35-38`. No swarm equivalent exists; SYNTHESIZED/omitted default confirmed. |
| 16 | `t2_model_class_diversity` | CONFIRMED-against-shipped | Reflect degraded trigger 7 reads `t2_model_class_diversity` at `contract.py:266-269`. Grep over swarm found no same-named field; DERIVED from distinct succeeded `WorkerResult.model_id` at `models.py:1122` with success status at `models.py:1125` / status literal at `models.py:69`. |
| 17 | `t2_vendor_diversity` | CONFIRMED-against-shipped | Reflect degraded trigger 8 reads `t2_vendor_diversity` at `contract.py:271-273`. Grep over swarm found no same-named field; DERIVED from succeeded worker `model_id` vendor classification (`models.py:1122`, `models.py:1125`). |
| 18 | `merge_method` | CONFIRMED-against-shipped | Reflect degraded trigger 10 reads `merge_method` at `contract.py:279-281`. Grep over swarm found no same-named field; DERIVED by ensemble from M/adversarial outcome, not from swarm `amalgamation_mode` (`models.py:1011`) because swarm's field is normalize/merge mode rather than reflect verdict method. |
| 19 | `adversarial_convergence_score` | CONFIRMED-against-shipped | Reflect null-convergence trigger reads `adversarial_convergence_score` at `contract.py:283-285`. Grep over swarm found no same-named field; MAPPED from the adversarial child `convergence_score` per GAP-1, not swarm. |
| 20 | `citations_dropped` | CONFIRMED-against-shipped | Reflect degraded trigger 13 reads `citations_dropped` at `contract.py:294-297`. No swarm equivalent exists; SYNTHESIZED/omitted default confirmed. |

## Gate conclusion

- OI-1 table conclusion is confirmed: the swarm DM-012 contract is not reflect-shaped and `ensemble.py` must map/derive/synthesize a reflect return contract.
- Named reflect verdict fields absent from the swarm seam: `tier_reached`, `merge_method`, `t2_model_class_diversity`, `t2_vendor_diversity`, `reviewer_count`, `adversarial_convergence_score`.
- Only shared key name: `status`, with different semantics (`ResultStatus` worker-count result vs reflect post-audit status), so it is not a safe passthrough.
- Provenance split carried forward for Step 0.1b: 6 DERIVED (`status`, `tier_reached`, `adversarial_unavailable`, `t2_model_class_diversity`, `t2_vendor_diversity`, `merge_method`), 2 MAPPED-ish (`report_path`, `adversarial_convergence_score`), 12 SYNTHESIZED (`contract_version`, `degraded_components`, `deviation_count_by_class`, `remediation_task_path`, `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `input_drift_detected`, `verification_ran`, `verification_skip_reason`, `citations_dropped`).
- Drift flags are line-anchor-only for `status` and `tier_reached`; no behavioral drift blocks Step 0.1b.

Status: Complete
