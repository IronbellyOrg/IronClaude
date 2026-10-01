# sc:reflect UC-1 PRE Gate — Coverage/Gap Audit (FR-RSR tasklist)

**Mode:** pre (UC-1) | **Depth:** deep (TCS ≫ 35; item-count override O3 also floors deep) | **Tier reached:** 2
**Spec (driving doc):** `.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md` (+ spec.md §3/§6)
**Tasklist under audit:** `.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md`
**Run id:** `pre-uc2-reachability-20260620-0341`
**Execution note:** reflect `--mode pre` invoked via a fresh executor-disjoint subagent (Skill sc:reflect); the subagent was filesystem-write-restricted, so this report was persisted by the task-builder orchestrator from the subagent's returned coverage audit. The audit is independent of the build orchestration (separate context, grounded in the real TDD/spec/tasklist).

## Verdict

```yaml
status: pass
coverage_pct: 1.00          # 18/18 = (10 FRs + 8 TDD §24.1 DoD lines); floor 0.90
unmapped_requirements: []
blocker_ordering: preserved
best_practice_compliance: pass
```

## Coverage map — FR-RSR.1–10 (all COVERED)

Every FR has a discrete implementation item AND a verification item quoting its exact spec §3 acceptance-criteria line range + the spec §6 NFR where one exists:

| FR | Impl step | Verify step | AC (spec §3) | NFR (spec §6) | Verdict |
|----|-----------|-------------|--------------|---------------|---------|
| FR-RSR.1 tagger | 3.1 | 3.4 | L244–252,271–273 | NFR-RSR.1/.2 | COVERED |
| FR-RSR.2 sweep | 3.2 | 3.4 (+7.x) | L303–316 | NFR-RSR.1/.2 | COVERED |
| FR-RSR.3 oracle | 2.1+3.2 | 2.2+3.4 | L332–342 | NFR-RSR.3 | COVERED |
| FR-RSR.4 rootwalk | 2.1+3.2 | 2.2+3.4 | L361–370 | n/a | COVERED |
| FR-RSR.5 pre-filter | 4.1 | 4.2 | L392–403 | n/a | COVERED |
| FR-RSR.6 §10.9 modifier | 5.1+5.2 | 5.3 | L430–439 | D8 | COVERED |
| FR-RSR.7 contract 1.6.0 | 3.3 | 3.4 | L463–474 | NFR-RSR.4/.5 | COVERED |
| FR-RSR.8 fail-open | 6.2 | 6.3 | L486–493 | NFR-RSR.6 | COVERED |
| FR-RSR.9 reviewer-brief | 6.1 | 6.3 | L506–511 | 3-section check | COVERED |
| FR-RSR.10 eval | 7.1–7.8 | 7.9 | L527–539 | NFR-RSR.2 | COVERED |

## Coverage map — TDD §24.1 Definition of Done (8/8 COVERED)

All 8 DoD lines map to verification/Release-Checklist items (runtime-surface.md → 2.1/2.2; §6.1 4b'+4b → 3.1/3.2/3.4; §5.3 pre-filter+§5.4 → 4.1/4.2; §10.9 modifier → 5.1/5.3; §9.1 6 fields+1.6.0+§9.3 → 3.3/3.4; reviewer-spec.md entry → 6.1/6.3; deviation-taxonomy.md xref → 5.2/5.3; eval headline+companions+count-invariant+skeletons + sync/no-`.claude/`/UV → 7.x/8.1/8.2). The §24.2 Release Checklist maps 1:1 to Step 8.2(a–e).

## Blocker ordering — PRESERVED
T1 `runtime-surface.md` (Phase 2) blocks all later phases; oracle (FR-RSR.3) + rootwalk (FR-RSR.4) gate the sweep's UNREACHED path (Step 3.2: "no UNREACHED emittable without the oracle + rootwalk consult"); eval (Phase 7) is terminal.

## Best-practice compliance — all 6 (PASS)
Additive-minor contract (3 gate sites :663/:804/:1772 + 1 cosmetic literal :1641; :1558 auto-derives, not edited); symbol-anchored tagger (nullable requirement_id); degrade-default → Grounding Gap, never Regression; counter hygiene (only `deviation_count_by_class.regression`, never `verification_regressions_detected`, no 5th class/counter); src/-SoT + sync-dev/verify-sync + no `.claude/` staging + UV/ruff; eval cases under `cases/uc2-*/` with FAIL-pre/PASS-post.

## Findings (advisory — coverage remained 1.00)

- **A1 — RESOLVED by the orchestrator before presentation.** Step 7.1's count-invariant grading referenced a precomputed `unreached_surfaces_len` scalar that no Phase-3 producer step emits (and which would be a non-contract 7th field). Remediated: Step 7.1's PRIMARY mechanism is now the TDD §18.2-sanctioned minimal grader extension (`check_yaml_list_len_eq` reading full `yaml.safe_load`, computing the invariant from the two already-emitted contract fields — no producer change, no extra field); the emitted-scalar approach is retained only as a fallback with a matching Step 3.2 producer clause.
- **A2 (benign, accepted):** no eval fixture grades the UC-1 inert-default path (all 5 cases are `mode: post`); UC-1 defaults are read-verified (3.4), not graded. Acceptable per TDD scope (NG1 — UC-1 reachability is out of scope).
- **A3 (covered):** semantic stability of the `regression` field (new evidence source, same meaning) is argued in TDD prose and checked by the final M3 gate's evidence-citation/contract-additivity lens (PG.2).
- **A4 (benign):** FR-RSR.7 sits in Phase 3 (vs TDD §23.2 P5) and FR-RSR.8 has no §23.2 row — both are spec-§10-authorized / design-§5.1-mapped and are now self-documented as reconciliations in the tasklist (fixes F2/F3). Not gaps.

## Routing
coverage_pct 1.00 ≥ floor 0.90 AND status not failed → **verdict: pass**. No Tier-3 corrective MDTM task required. The one actionable seam (A1) was remediated in-build. Tasklist is cleared to execute.
