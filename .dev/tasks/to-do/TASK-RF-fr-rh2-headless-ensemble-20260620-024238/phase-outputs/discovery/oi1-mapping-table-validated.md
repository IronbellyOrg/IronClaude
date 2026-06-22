# Validated OI-1 mapping table — swarm raw facts to reflect return contract

Status: In Progress
Date: 2026-06-20
Task step: 0.1b

## Verbatim acceptance references

### Spec §11 OI-1

> Does reflect's swarm contract already emit `reviewer_count`/`merge_method`/`t2_model_class_diversity` in the exact shape `contract.derive_verdict` reads, or must `ensemble.py` map them? Produce an explicit swarm-`ResultContract`-field → reflect-contract-field correspondence table.

Resolution: the validated answer is that `ensemble.py` MUST map/derive/synthesize a reflect-shaped contract. The swarm DM-012 contract is not reflect-shaped; the only shared key name is `status`, and the semantics differ.

### FR-RH2.3 acceptance bullets

> The downstream merge step consumes swarm's per-reviewer `final_path` artifacts (suspect-aware).
>
> No scoring/ranking/dedup logic is added to `swarm/merge.py` (the LOC ceiling + boundary tests stay green).
>
> The adversarial merge produces a convergence score recorded on the reflect contract.

### FR-RH2.7 acceptance bullet

> `derive_verdict` and the `Verdict` exit-code map (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are unchanged.

## Validated table

| Field | contract.py read-site | Provenance | Swarm source / derivation rule |
|---|---|---|---|
| `contract_version` | `contract.py:166-176` | SYNTHESIZED | Emit a reflect contract major-1 literal such as `"1.0"`. Do not blindly pass through swarm DM-012 `ResultContract.contract_version` (`models.py:997`), even though the literal value is also `"1.0"`, because it belongs to the swarm schema namespace. |
| `status` | `_make_result` `contract.py:116`; halted `contract.py:311-313`; PASS `contract.py:235` | DERIVED | Derive reflect status from M and downstream scoring result. Swarm `ResultContract.status` exists at `models.py:998` with `ResultStatus` values at `models.py:68`, but is the worker-count result, not reflect's post-audit status. Scratch drift: research line anchor `_make_result`:118 was off; shipped read-site is line 116. |
| `tier_reached` | raw read `contract.py:195`; result `contract.py:113/117`; PASS `contract.py:235`; degraded `contract.py:262-264`, `contract.py:283-285` | DERIVED | No swarm field. Derive `2` only for faithful M≥2 / sufficiently diverse reviewer outcomes; derive `1` for single-reviewer fallback outcomes. Scratch drift is line-anchor-only; no behavioral drift. |
| `degraded_components` | shape gate `contract.py:183-190`; trigger membership `contract.py:258-260` | SYNTHESIZED | Emit `[]` unless a chain-critical loss is intentionally surfaced. No swarm equivalent. |
| `deviation_count_by_class` | `_extract_deviations` `contract.py:90-101`; result via `contract.py:121`; halted `contract.py:323-326` | SYNTHESIZED | Emit `{}`/zero-equivalent inert default unless the adversarial/reflect domain supplies counts. No swarm equivalent. |
| `report_path` | `contract.py:119` | MAPPED | Map to the relevant human-readable report path, either the adversarial child report path or a derived path from swarm reduce artifacts such as `ResultContract.merged_path` (`models.py:1012`) / succeeded `WorkerResult.final_path` values (`models.py:1121`). Telemetry only, not a verdict driver. |
| `remediation_task_path` | `contract.py:126` | SYNTHESIZED | Omit or emit `None` in the swarm path unless a separate remediation child writes one. No swarm equivalent. |
| `regression_present` | bool shape `contract.py:47-57`, `contract.py:200-206`; halted `contract.py:315` | SYNTHESIZED | Omit or emit an explicit boolean only if the downstream adversarial/reflect domain produces it. No swarm equivalent. |
| `unauthorized_deviation_present` | bool shape `contract.py:47-57`, `contract.py:200-206`; halted `contract.py:317` | SYNTHESIZED | Omit or emit an explicit boolean only if the downstream adversarial/reflect domain produces it. No swarm equivalent. |
| `needs_human_decision` | bool shape `contract.py:47-57`, `contract.py:200-206`; halted `contract.py:319` | SYNTHESIZED | Omit or emit an explicit boolean only if the downstream adversarial/reflect domain produces it. No swarm equivalent. |
| `user_decision_required` | bool shape `contract.py:47-57`, `contract.py:200-206`; halted `contract.py:321` | SYNTHESIZED | Omit or emit an explicit boolean only if the downstream adversarial/reflect domain produces it. No swarm equivalent. |
| `adversarial_unavailable` | bool shape `contract.py:47-57`, `contract.py:200-206`; degraded `contract.py:275-277` | DERIVED | Derive from the adversarial child launch/parse outcome. This is not a swarm field. If adversarial scoring cannot run, set `True` so `derive_verdict` routes `adversarial-unavailable`. |
| `input_drift_detected` | bool shape `contract.py:47-57`, `contract.py:200-206`; degraded `contract.py:300-302` | SYNTHESIZED | Omit unless a reflect-domain input drift check produces it. No swarm equivalent. |
| `verification_ran` | bool shape `contract.py:47-57`, `contract.py:200-206`; degraded `contract.py:287-290` | SYNTHESIZED | Omit or set according to reflect-domain verification behavior; pair with `verification_skip_reason` when false. No swarm equivalent. |
| `verification_skip_reason` | `contract.py:289`; exemptions `contract.py:35-38` | SYNTHESIZED | Omit unless `verification_ran` is false and a reflect-domain skip reason is available. No swarm equivalent. |
| `t2_model_class_diversity` | degraded `contract.py:266-269` | DERIVED | Derive from distinct succeeded `WorkerResult.model_id` values (`models.py:1122`) among workers with `WorkerResult.status == "success"` (`models.py:1125`, literal values at `models.py:69`). Grep confirms no swarm field named `t2_model_class_diversity`. |
| `t2_vendor_diversity` | degraded `contract.py:271-273` | DERIVED | Derive from vendor/classification of each succeeded worker `model_id` (`models.py:1122`, `models.py:1125`). Grep confirms no swarm field named `t2_vendor_diversity`. |
| `merge_method` | degraded `contract.py:279-281` | DERIVED | Derive from M/adversarial outcome: `"single-reviewer-fallback"` for M==1; otherwise an adversarial method such as `"adversarial"` when scoring succeeds. Do not confuse with swarm `amalgamation_mode` (`models.py:1011`), which is a normalize/merge mode, not reflect's verdict method. |
| `adversarial_convergence_score` | degraded `contract.py:283-285` | MAPPED | Map from the adversarial child `convergence_score`, renaming it to reflect's `adversarial_convergence_score`. Grep confirms no swarm field named `adversarial_convergence_score`; `None` is only the graceful failure path and triggers null-convergence when `tier_reached == 2`. |
| `citations_dropped` | degraded `contract.py:294-297` | SYNTHESIZED | Omit or emit `0` unless the downstream reflect/adversarial domain produces a count. No swarm equivalent. |

## Provenance tally

- DERIVED (6): `status`, `tier_reached`, `adversarial_unavailable`, `t2_model_class_diversity`, `t2_vendor_diversity`, `merge_method`.
- MAPPED (2): `report_path`, `adversarial_convergence_score`.
- SYNTHESIZED (12): `contract_version`, `degraded_components`, `deviation_count_by_class`, `remediation_task_path`, `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `input_drift_detected`, `verification_ran`, `verification_skip_reason`, `citations_dropped`.

Exact split: **6 DERIVED + 2 MAPPED + 12 SYNTHESIZED = 20**.

## Drift carried forward from scratch

The scratch validation flagged two line-anchor drifts only: research cited `_make_result` line anchors for `status`/`tier_reached` that do not exactly match shipped line numbers. This artifact uses the shipped read-sites (`status` at `contract.py:116`; `tier_reached` at `contract.py:113/117` plus `contract.py:195`). No behavioral drift blocks implementation.

Status: Complete
