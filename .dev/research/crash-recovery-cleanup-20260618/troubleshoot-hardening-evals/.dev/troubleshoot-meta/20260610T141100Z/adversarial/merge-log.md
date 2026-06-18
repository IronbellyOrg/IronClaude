# Merge Log

## Metadata

- **Base variant:** Variant C (blind) — combined score 0.930
- **Executor:** merge-executor (timed out on first attempt mid-read; re-dispatched with scoped reads + inlined binding facts + single-write → success)
- **Merge date:** 2026-06-10
- **Merged output:** `../EFFICACY-REPORT-MERGED.md` (253 lines)
- **Status:** success
- **Changes applied:** 10 of 10 planned · 0 failed · fabricated content rejected per plan

## Changes Applied

| # | Change | Status | Provenance tag | Validation |
|---|--------|--------|----------------|------------|
| 1 | Honest G1-status header & posture | ✅ | `Variant C spine` | Status line present; matches git (unbuilt) |
| 2 | Corrected executive verdict | ✅ | `Variant C + A/B corrected, BC-3/BC-4` | No "nothing fixed"/"validated"; metric labeled as mean |
| 3 | Canonical crosswalk table | ✅ | `round3-resolution; BC-2` | Verbatim; E4≠PRD-E04 caveat present |
| 4 | 3-bucket committed/unbuilt ledger | ✅ | `round3-resolution; BC-3` | All 3 buckets; honest one-sentence claim |
| 5 | Per-stage theatre scorecard (relabeled) | ✅ | `Variant B + scorecard source; BC-1/BC-4` | Run-result tokens stripped; `NOT YET PROVEN` per cell |
| 6 | Would-have-caught matrix (predicted) | ✅ | `Variant A/B; BC-1` | Every cell `NOT YET PROVEN (pre-build)`; no events asserted |
| 7 | Corrected lone-catch attribution + caveat | ✅ | `Variant C + A/B; X-001` | Two catches; debate caught neither; unproven-actor caveat |
| 8 | Analytical primitives as design rationale | ✅ | `Variant A U-001/U-002/§7` | Framed as lenses, not run outcomes |
| 9 | Contract Identity Ledger (E4 + M6 rows) | ✅ | `Variant B; M6 inlined facts` | E4 & M6 distinct rows; M6 blame corrected |
| 10 | Hardening-spec linkage + halt posture | ✅ | `Variant C` | H0–H5 + paste-ready G1 prompt + sync-dev note |

### Rejected (per refactor-plan "Changes NOT Being Made")

- Variant A §6 "rollback-replay 8/8 / 100%" — **DELETED** (fabricated, X-007).
- Variant B "7/7 rollback-replay" + "implemented" claims — **DELETED** (fabricated, X-007).
- A's 6.25% / B's 3.0% theatre ratios as headline — **dropped** (self-built denominators; only grounded 59%/41% mean retained, never as catch rate).
- A's 8 / B's 7 as canonical SET — **demoted to instances** under E1–E5.
- "PR #158-equivalent" (B) — **dropped** (no #158).
- "M6 committed in #149" — **corrected** to `27962ddb2`/`09e2ccc0d`.
- Blanket "nothing was fixed" — **rejected** (point-fixes shipped).

## Post-Merge Validation

- **Structural integrity:** PASS — H1→H2→H3, no level gaps/orphans; 11 sections, logical order.
- **Internal references:** PASS — §-cross-references (§5, §8, §10) resolve; crosswalk/ledger IDs consistent.
- **Contradiction re-scan:** PASS — no new contradictions; the source contradictions (X-001..X-008) are resolved or carried as explicit caveats, not conflicts.
- **BC-1 grep gate** (`grep -nE '8/8|7/7|100%|rollback-replay|did_catch|✓ caught|round 2'`): **PASS** — single match is the line-252 negation "No rollback-replay or coverage claim is asserted"; zero asserted run-result tokens.
- **BC-3 phrase check** (`nothing was fixed` / `refactor validated`): PASS — only occurrence is the BC-3 rule quoted inside a provenance HTML comment (documentation, not assertion).

## Summary

- Planned: 10 · Applied: 10 · Failed: 0 · Skipped: 0
- Fabrication removed: 2 sections (A §6, B replay)
- Integrity constraints (BC-1..BC-4): all enforced and independently re-verified by orchestrator.

## Post-Merge Addendum — Research-Informed Refinements (2026-06-10)

Source: `../researchFindings.md` (deep-research pass, 23 sources, 24/25 claims confirmed 3-0, 1 refuted). Applied as **additive** edits only; no existing finding altered.

- **§10 expanded** — added "Research-informed gate-design refinements": (a) waiver-policy anti-theatre invariant (waived runtime probe → `partial`, never re-greened to `success`); (b) H1/H2 Pact/CDC contract-record fields; (c) H3 allow-list grammars + named near-miss negatives; (d) H5/ledger retry/resume/resubmit distinction feeding emitted step IDs into `prd resume`.
- **§11 Caveats** — added #6 (corroboration is analogical, not literal — §5 stays NOT YET PROVEN) and #7 (research provenance: run against sibling copy `.dev/troubleshoot/meta-efficacy-pipeline/EFFICACY-REPORT.md`; 1 refuted claim quarantined).
- **Appendix A added** — element→external-practice→source corroboration table; framed as design corroboration, NOT efficacy proof; the 1 refuted claim explicitly quarantined.
- **Integrity preserved:** BC-1 grep gate re-run = PASS (only the negation line); `NOT YET PROVEN` stamps 12→16; provenance tags 13→15. No forbidden run-result token introduced; corroboration deliberately not allowed to imply the unbuilt hardening works.
