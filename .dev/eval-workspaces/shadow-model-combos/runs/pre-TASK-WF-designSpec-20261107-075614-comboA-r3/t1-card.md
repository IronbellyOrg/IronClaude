# Tier 1 reflection card (UC-1 pre-execution) — comboA-r3
subject: plan TASK-WF-designSpec-20261107-075614 vs design spec (pr-submit merge guard, issue #375)
vantage_note: HEAD c2e3347d is 6 days past the plan; the feature has landed (merge_guard.py exists, EventType==45). This audit targets the PLAN TEXT vs SPEC as of authoring (base e8db2fe6); repo HEAD is context only.
coverage: 23/23 parsed FRs mapped; 7/7 inferred rows mapped; coverage_pct 1.0, union 1.0; S_dev_density 0.0
structure: 13 tasks in 5 phases; dependency lines complete for the multi-dependency tasks (T5: T3+T4; T8: T1+T4+T7; T13: T2+T10+T11+T12)
top_risks (to be debated at T2):
  R1: T1 AC "O1 names one single place... or states that no id is minted today" — the disjunction lets the task pass either way; if O1's finding is "no id minted", the plan does not name which sentence will mint it downstream (spec 4.6 demands one source). Possible escape hatch.
  R2: T2/T13 pin len(EventType)==45 as absolute counts — but HEAD already has 45 members (feature landed); on the plan's own base commit it was 43->45. Absolute-count ACs rot (memory: shadow11 41-vs-45). At authoring time the base was 43 so the AC was correct; risk is stale-by-execution, not authoring defect.
  R3: Wave-8 CI-fix cycle engage/release — spec section 3 row "End of Wave 3 at L3... review-fix cycle, or CI-fix cycle from Wave 8"; plan T10 Wave 8 bullet + T4 cover it; no unmapped residue found.
  R4: guard_status mapping edge: mode==OFF with a HELD record from a previous run — plan T4 covers 'mode OFF at ordinal 3 with phase HELD returns REPORT_HELD' (resume row 2). Mapped.
self_reported_confidence: 0.86
