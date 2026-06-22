# TDD Presentation Summary (Step 7.1) — TASK-TDD-20260619-235400

**Date:** 2026-06-20

## Final document
- **Path (pinned):** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md`
- **Line count:** 1,773 — WITHIN the Heavyweight budget (1,200-1,800). ✅
- **Tier:** Heavyweight (HIGH complexity 0.82; cross-subsystem cli/reflect + cli/swarm + /sc:adversarial + test harness).

## Sections: 25 populated / 3 N/A
- **Populated:** §1-8, §11-15, §17-28.
- **N/A (backend CLI library, no client surface):** §9 State Management, §10 Component Inventory, §16 Accessibility.
- **Light (CLI infra):** §17 Performance Budgets, §25 Operational Readiness, §26 Cost.

## Load-bearing deliverable
- **OI-1 swarm `ResultContract` → reflect contract field-correspondence table** at §8.3 (~22 rows), explicitly called out as the **§22 Q1 BLOCKING gate** that sizes `ensemble.py`'s mapping layer. Status: PRODUCED in the TDD; must be re-validated against the shipped diff before FR-RH2.3 code lands (per §22 Q1). Key finding: the swarm DM-012 contract and the reflect verdict contract are DISJOINT schemas (share only `status`, with divergent semantics) → most reflect verdict fields must be SYNTHESIZED in `ensemble.py` (only `reviewer_count`←M maps directly).

## Artifact locations
- Research (11 + reuse-audit.yaml): `${TASK_DIR}/research/`
- Synthesis (9): `${TASK_DIR}/synthesis/`
- QA reports + gate plans: `${TASK_DIR}/qa/`, `${TASK_DIR}/phase-outputs/plans/`

## QA gate outcomes
- Research gate (M3): PASS (1 fix cycle — added research/09 config/CLI surface).
- Synthesis gate: PASS (1 fix cycle — 5xx-backoff contradiction + 2 minor).
- Report-validation (Gate A, M3): PASS (1 fix cycle — 12 citation/consistency fixes).
- Source-fidelity (Gate B, M4): PASS (clean, 0 cycles).
- Qualitative (Gate C): PASS (2 cosmetic fixes).

## Residual Open Questions for the implementer (all in §22, none block the TDD)
- **Q1 (OI-1, BLOCKING):** re-validate the §8.3 correspondence table against the shipped diff before FR-RH2.3 code.
- **Q6 (D3):** `ensemble-empty` M==0 slug does NOT exist in `contract.py` today → reconcile vs FR-RH2.7 "verdict map unchanged" (new branch = recorded amendment, or map onto existing BLOCKED trigger).
- **Q5 (OI-4):** `--suspect-source` emitted by bare-review but unparsed by sc-adversarial Mode A → teach Mode A to parse, or pass via `--compare`.
- **Q7:** `_resolve_run_transport_factory` is a PRIVATE cross-package symbol → import private vs recompose `read_env`+transports (coupling decision).
- Recipe binding: reuse `bare-review-v1` (validator assertions 2&6 satisfied, zero recipe edits) — recommended default.

**No gaps requiring manual review beyond the §22 Open Questions, which are by-design implementation-time decisions.**
