VERDICT: FAIL

# QA Report — Phase 2 Qualitative Domain Accuracy

**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md
**Lens:** domain-accuracy
**Fix authorization:** false

## Evidence

Read and verified the assigned domain files directly:

- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`: UX states (§3), setup questions (§4), safe locking policy (§6), validation checklist (§7), cross-PR shape-only requirement (§7 Freshness), acceptance criteria (§13).
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md`: `ContractState`, `FieldProvenance`, `CandidateContract`, safe-locking gate, validation pipeline, cross-PR shape-only behavior.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/states.py`: enum includes all nine state literals.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`: diagnosis transition implementation and next-command handling.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/candidate.py`: provenance sources, required-observed fields, Augment candidate selection, expected-result derivation.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`: non-`polling` validation, negative controls, freshness/cross-PR checks.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py`: 12 lock predicates and destination gate.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py`: report and lock writer gating.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py`: `DetectionContract` field semantics and local override behavior.
- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md` and `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`: missing-contract halt language and no-monitor boundary.

## Checklist Results

| Check | Result | Evidence |
|---|---|---|
| The nine UX states are handled | FAIL | `ContractState` declares all nine literals in `states.py`, but `diagnose()` only returns missing/unparseable/unlocked/evidence_missing/validation_missing/stale/validation_failed/ready; no implementation path produces or accepts `declined_by_user` for cancellation handling. |
| `FieldProvenance` distinguishes `observed`/`default_suggested`/`user` | PASS | `candidate.py` defines `PROVENANCE_OBSERVED`, `PROVENANCE_DEFAULT_SUGGESTED`, and `PROVENANCE_USER`, and `FieldProvenance.source` records them. |
| Required fields are not marked observed without payload backing | PASS | User-provided identity/emission/locus/signal values set `source=user` but `observed` is true only when the value resolves against observed payload data; unobserved required fields are returned by `required_unobserved()`. |
| Multiple Augment candidates require explicit selection | PASS | `_selected_identity()` only auto-selects when exactly one observed login exists; multiple observed candidates fall through to default_suggested/unobserved and therefore block required observed provenance. |
| `polling` is non-lockable | PASS | `LOCKABLE_RESULTS` excludes `polling`; `validate_candidate()` adds `expected_not_polling`; `LockGate._expected_not_polling()` requires `{clean, findings, declined}`. |
| Cross-PR evidence is shape-only | FAIL | `EvidenceBundle.cross_pr_shape_only` is recorded and summarized, but validation and lock gates do not prevent a cross-PR shape-only bundle from producing a passing validation/lock. `_freshness_checks()` always passes `cross_pr_shape_only_recorded`, and `LockGate` has no predicate constraining current-PR readiness when `cross_pr_shape_only=True`. |

## Findings

| # | Severity | Affected source file | Finding | Required correction |
|---|---|---|---|---|
| 1 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py` | The `declined_by_user` UX state is declared but not operationally handled. Requirements list it as one of the nine readiness states with the meaning “User cancels setup; leave existing contract untouched.” The implementation has no transition, helper, or public result path that can produce this state; `diagnose()` is read-only and returns only file/evidence/validation states. This means a cancellation flow cannot be represented in the same state vocabulary as the other eight states. | Add an explicit cancellation handling path in the setup helper surface, e.g. a pure helper/result constructor that returns `Diagnosis(state=ContractState.DECLINED_BY_USER, blockers=[...], ...)` or an equivalent setup-result type wired through the facade. Ensure cancellation leaves the existing contract untouched and is tested alongside the other eight states. |
| 2 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` | Cross-PR evidence is only recorded, not enforced as shape-only. Requirements say cross-PR evidence is explicit and can validate shape only, not current review state. Current code allows `EvidenceBundle.cross_pr_shape_only=True` to pass validation and then pass `write_lock()` if the classifier matches, negative controls pass, report passes, and confirmation is true. `_freshness_checks()` always emits a passing `cross_pr_shape_only_recorded` check, `LockGate.evaluate()` has no cross-PR/current-state predicate, and `writer.write_lock()` trusts that gate. This can incorrectly lock a contract using evidence from another PR as if it proved current-PR readiness. | Change validation/gating so `cross_pr_shape_only=True` cannot satisfy current review completion/readiness predicates. At minimum, validation should downgrade/segregate shape-only results so `report.passed` cannot mean current-PR readiness, and `LockGate` should include a predicate that either blocks lock writes from cross-PR evidence or requires an explicit shape-only mode that cannot assert `READY`/current review completion. Add a regression test where otherwise-valid cross-PR evidence is recorded as shape-only and cannot produce a current-readiness lock. |

## Additional PASS Details

- Provenance vocabulary is explicit: `observed`, `default_suggested`, and `user` are distinct constants and are assigned through `FieldProvenance.source`.
- User answers are not automatically treated as observed: selected identity/app/emission/path values are marked `observed=True` only when present in payload-derived candidate sets or path resolution succeeds.
- Multiple Augment identities do not auto-lock: more than one observed login causes `augment_bot_login` to remain unobserved unless the operator selects one, and even a selected one must match observed payload metadata to count as observed.
- `polling` is blocked at both validation and lock-gate layers.

## Confidence

Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool Engagement

Read: 13 | Bash: 0 | Web/Tavily: 0

No web research was performed; Tavily was not required because every verification target was local source, task, design, or requirements content.

## Required Corrections Before PASS

1. Implement a real `declined_by_user` handling path, not just an enum literal.
2. Enforce cross-PR shape-only semantics in validation and/or lock gating so cross-PR evidence cannot be treated as proof of current PR review readiness.

## QA Complete
