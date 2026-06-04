# Reflect UC-2 Re-run Delta — post regression fixes (TASK-RF-20260602-135209)

**Date:** 2026-06-03 · **Mode:** post · **Tier:** 1 (rubric: confirmed 2-site fix → narrow scope/high confidence → T1 STOP) · **Verdict:** REGRESSIONS CLEARED.

## Context

The prior audit (`REPORT.md`, 2026-06-02) found 2 task-introduced regressions (F-1 HIGH, F-2 LOW) + 2 follow-ups (G-1, G-2). Between that audit and this re-run, all four were fixed (during a ~4.5h pause; the branch is now `feat/sc-reflect-v3-serena-low-impl` and medium-complexity FR-RV3-MED work also landed, moving the contract to v1.2.0). This delta confirms clearance by fresh re-Read of each site.

## Regression clearance (evidence-validated — sites re-Read fresh)

| # | Prior | Now | Site | Status |
|---|-------|-----|------|--------|
| **F-1** | C1 predicate `(slug_count−readonly)>20` — misses read-only-dominated case | `slug_count > 20 AND (slug_count − readonly_count) ≤ 20` → fires on 25/24 case (`1 ≤ 20`), matches eval `expected.yaml:21` | `SKILL.md:523` | **CLEARED** |
| **F-2** | enum `activation_message \| … \| none` | `activation_msg \| list_memories_proxy \| unknown` (spec FR-6.1 exact) — across SKILL.md:269, expected.yaml:20, diff.patch:11, evals.json:527 | `SKILL.md:269` + 3 eval files | **CLEARED** |
| G-1 | report-template.md `1.0.0` | `1.2.0` (consistent with §9.1 contract bump by the medium-complexity work) | `report-template.md:14` | RESOLVED |
| G-2 | `yaml_list_contains` indexed-scalar field_path (ids 22/24) | `regex_present` with explanatory note re grader list-only limitation | `evals.json` ids 22/24 | RESOLVED |

## Mechanical gates

- `make sync-dev`: PASS (exit 0). `make verify-sync`: PASS (`✅ All components in sync`).
- `evals.json`: valid JSON, 36 evals, no duplicate ids.
- markdownlint SKILL.md: HEAD 136 → current 142 (+6). The delta is attributable to the broader uncommitted low+medium FR-RV3-MED tables, NOT the F-1/F-2 fixes (token rename + predicate reword add no tables). Out of scope for this regression fix; flagged for the combined-branch owner.

## Deviation tally (post-fix, low-complexity scope)

```yaml
authorized: 0   # (FR-RV3-MED content present on the same files is separate authorized work, not audited here)
necessary: 0
drift: 0
regression: 0   # both prior regressions cleared
```

## Promotion verdict (Wave 7)

The §14.5.2 gate condition 4 (`no_drift_no_regression`) — which BLOCKED promotion in the prior run — now **PASSES** for the low-complexity scope. Full promotion eligibility additionally depends on the combined branch's `status: success` and the markdownlint/medium-complexity state being clean, which is outside this regression-clearance pass. No promotion mutation performed here (focused confirmation only).

## Note on scope

This re-run confirms the 2 low-complexity regressions are cleared. The files now also carry medium-complexity (FR-RV3-MED) content and a v1.2.0 contract — that is separate authorized work and was NOT audited against the low-complexity spec here (it would surface as Authorized expansion, not drift). A full UC-2 audit of the combined low+medium deliverable should run against the medium-complexity spec when that work is ready for review.
