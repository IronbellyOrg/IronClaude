# QA Report — doc-qualitative (lens: determinism / first-run robustness)

**Topic:** P5 Tier Calibration Advisory — determinism + first-run robustness
**Date:** 2026-06-19
**Phase:** doc-qualitative (lens-based; report-only)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT-ONLY — nothing modified)

---

## Overall Verdict: FAIL

The advisory is correctly framed as best-effort/read-only and the §5.3 pure-function fence is sound, BUT the rendered advisory is NOT provably deterministic as written: the match/threshold algorithm references feedback-log fields that do not exist in the feedback-log schema, the ascending-order key is non-unique with no tie-break, the `Observed count` semantics are undefined, and the "absent on first run" graceful-omit is specified only for the absent-file case (not malformed/partial). These are determinism defects on the exact claims under review.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | feedback-log read is best-effort (absent first run → section omitted, no error) | PARTIAL-FAIL | SKILL.md:870-871 + :873 + :885 + index-template.md:136 all say "best-effort and READ-ONLY", "may be absent on the first run — when absent, the whole section is omitted, no error". Absent-file case is covered. BUT no specification for a PRESENT-BUT-MALFORMED / partial / empty feedback-log.md (truncated table, missing header row, corrupt rows). "best-effort" is asserted but the failure mode beyond absence is undefined → first-run-adjacent robustness gap. See I-1. |
| 2 | min-2 threshold + ascending ordering make rendered advisory deterministic for a fixed feedback-log | FAIL | Threshold prose at SKILL.md:873 references match keys `roadmap_item_id` / `task_signature` / `suggested_tier` that DO NOT EXIST in the feedback-log schema (SKILL.md:855-864: columns are `Task ID, Original Tier, Override Tier, Override Reason, Completion Status, Quality Signal, Time Variance`). Cannot deterministically compute "matching overrides" against fields the file does not contain (I-2, CRITICAL). Ascending key `T<PP>.<TT>` (SKILL.md:875) is NON-UNIQUE if a task has ≥2 matching feedback rows, with no tie-break specified → row order undefined (I-3). `Observed count` `<n>` (SKILL.md:880-882) has no defined counting semantics (I-4). |
| 3 | scored tiers deterministic independent of feedback-log (same roadmap → same scored tiers) | PASS (with caveat) | §5.3 fence at SKILL.md:569 is explicit and sound: "scored tiers are a pure function of the roadmap text — the §5.3/§5.4 scored-tier compute path takes NO calibration/feedback input (it MUST NOT read `feedback-log.md` ...)". Reinforced at :871, :885, index-template.md:136. Scored-tier determinism vs feedback-log holds. CAVEAT: SKILL.md:870 says the advisory is "emitted at Stage 4", and Stage 4 IS the Enrichment / scored-tier compute stage (SKILL.md:1684, 1712) that the §5.3 fence forbids from reading feedback-log — a stage-attribution contradiction that muddies the very separation the fence depends on (I-5). The invariant itself is correct; the stage label undermines its expression. |

## Summary

- Checks passed: 1 / 3 (with caveat)
- Checks failed: 2 (one PARTIAL-FAIL, one FAIL); plus a contradiction on check 3's stage attribution
- Critical issues: 1 (I-2)
- Issues fixed in-place: 0 (report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-2 | CRITICAL | SKILL.md:873 vs :855-864 | Match/threshold algorithm reads non-existent fields. The advisory matches a feedback row to a task "when its `roadmap_item_id` (preferred) or `task_signature` equals the task's roadmap item / signature" and counts a "matching override" as "a matched row whose `suggested_tier` differs from the deterministically scored tier." None of `roadmap_item_id`, `task_signature`, `suggested_tier` are columns in the feedback-log schema (which has `Task ID`, `Override Tier`, etc.). The rendered advisory therefore cannot be computed deterministically — an implementer must guess the mapping (`Task ID`→`roadmap_item_id`? `Override Tier`→`suggested_tier`? what is `task_signature`?). Different mappings yield different "matching overrides", different threshold outcomes (≥2 vs <2 → section present vs OMITTED entirely), and different rows. This breaks the min-2 determinism claim at its root. | Reconcile the two schemas: either (a) define the advisory's match keys in terms of the actual feedback-log columns (`Task ID` for match, `Override Tier` for `suggested_tier`), or (b) add `roadmap_item_id` / `task_signature` / `suggested_tier` columns to the Feedback Collection Template (SKILL.md:855) AND the index-template mirror (index-template.md:129). State the exact column-name→algorithm-field mapping verbatim so the match is reproducible. |
| I-3 | IMPORTANT | SKILL.md:875, :880-882 | Non-unique sort key, no tie-break. Rows are "ordered ascending by `T<PP>.<TT>`". If a single task has ≥2 matching feedback rows (entirely possible — multiple sessions logging the same task), multiple advisory rows share the same `T<PP>.<TT>` and the relative order among them is undefined → non-deterministic byte output, contradicting the line :885 claim "same inputs → byte-identical section." | Either collapse to one advisory row per task (one row per distinct `T<PP>.<TT>`, with `Observed count` aggregating) — which the single-row exemplar at :882 implies but does not state — or specify a fully-ordered composite tie-break key (e.g., ascending `T<PP>.<TT>`, then ascending `suggested_tier`, then feedback-log row index). |
| I-4 | IMPORTANT | SKILL.md:880-882 | `Observed count` semantics undefined. The column header is `Observed count` with value `<n>`, but the prose never defines what `<n>` counts (number of matching feedback rows for the task? number of overrides suggesting this specific tier? total feedback rows for the task incl. non-overrides?). Two implementers will produce different `<n>` for the same feedback-log → non-deterministic output. | Define `Observed count` precisely, e.g. "the number of matching feedback rows for this `T<PP>.<TT>` whose `suggested_tier` equals the Feedback-suggested tier shown in this row." Tie it to the I-3 collapse decision. |
| I-1 | IMPORTANT | SKILL.md:870-871; index-template.md:136 | First-run robustness specified only for the absent-file case. "best-effort and READ-ONLY (the file may be absent on the first run — when absent, the whole section is omitted, no error)". A genuinely best-effort read must also define behavior for a present-but-unparseable feedback-log (empty file, header-only table, malformed/short rows, non-UTF8). As written, the malformed case is undefined → a corrupt log could error or render garbage, defeating the "no error" robustness intent on the very first runs after a log is created. | Extend the best-effort clause: "If the file is absent OR present-but-unparseable (no valid table rows after the header), omit the whole section with no error." Mirror the same clause in index-template.md:136. |
| I-5 | MINOR | SKILL.md:870 vs :569, :1684, :1712 | Stage-attribution contradiction. The advisory is described as "emitted at Stage 4." Stage 4 is Enrichment — the scored-tier compute stage (SKILL.md:1684 "Enriching tasks with tier/effort/risk"; :1712 "Enrichment: all tasks have Effort/Risk/Tier/Confidence"). The §5.3 fence (:569) explicitly forbids the Stage-4 compute path from reading `feedback-log.md`. Placing the feedback-log-reading advisory "at Stage 4" textually co-locates it with the path the fence walls it off from — confusing the separation the determinism guarantee depends on. (The invariant is still correct; only the stage label is wrong/misleading.) | Re-attribute the advisory emission to Stage 5 (File Emission, SKILL.md:1685) — it is an index-level RENDERED section, not an enrichment computation — or add an explicit clause: "read/rendered at Stage 5 emission time, strictly after and separate from Stage-4 scored-tier compute." |

## Verification performed (anti-bias evidence)

- Read the phase-6 output summary (lines 1-30): claims under review = items 5 (determinism) + the §5.3/§5.4 non-mutation guarantee.
- Read SKILL.md:820-948 (advisory block at 866-885 + Feedback Collection Template schema at 845-864 + surrounding index section order).
- Read SKILL.md:555-634 (§5.3 fence at 567-569 + scored-tier compute algorithm — confirmed it consumes roadmap text only).
- Read index-template.md:120-153 (P5 mirror at 132-140; confirmed it carries the advisory placeholder per R-14, and that it inherits the SAME schema-mismatch silence — the mirror does not define match keys either).
- Grep `roadmap_item_id|task_signature|suggested_tier|Override Tier|Override Reason` across SKILL.md → confirmed the three advisory match-fields appear ONLY in the advisory prose (873) and NOWHERE in the schema (855-864). This is the I-2 CRITICAL.
- Grep `Tier Calibration Advisory|Stage 4|Feedback Collection|feedback-log` → located the Stage-4 emission claim (870) and the Stage-list (1680-1719); confirmed Stage 4 = Enrichment = scored-tier compute. This is I-5.

## Self-Audit (mandatory)

1. **How many factual claims independently verified against source:** 5 distinct claims — (a) absent-file omit text (verified, present at :871/:885/:136); (b) advisory match keys vs feedback schema (verified MISMATCH via grep + Read); (c) §5.3 fence wording + that compute path is roadmap-only (verified at :569 + :555-634); (d) ascending-only sort with single-key (verified at :875); (e) Stage-4 emission attribution vs Stage-list (verified at :870 vs :1684/:1712).
2. **Files read:** phase-6-output-summary.md (full); SKILL.md (555-634, 820-948, 1680-1719); index-template.md (120-153). Plus 2 grep sweeps over SKILL.md.
3. **Why trust the non-zero finding count:** the CRITICAL (I-2) is grep-provable — the three match-field names literally do not occur outside the advisory prose. Anyone can re-run `grep -n "roadmap_item_id\|task_signature\|suggested_tier" SKILL.md` and see they appear only at line 873, never in the schema at 855-864. This is not a judgment call.
4. **Web research:** none performed (all checks are local-file-bound); Tavily not invoked. No fallback occurred.

## Confidence

Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
(All three lens checks were resolved against source. The verdict is FAIL because checks 1 and 2 surfaced defects and check 3 carries a contradiction in its stated stage attribution.)

**Tool engagement:** Read: 5 | Grep: 2 | Glob: 0 | Bash: 0

## Recommendations

1. BLOCKING: Fix I-2 first — without a reconciled schema↔algorithm mapping, the min-2 threshold (and thus whether the section renders at all) is not computable, so no downstream determinism claim can hold. This is the single highest-leverage fix.
2. Then I-3 + I-4 together (row collapse / tie-break + `Observed count` definition) — they are coupled.
3. Then I-1 (malformed-log robustness) and I-5 (stage re-attribution).
4. Re-run this determinism lens after fixes; expect PASS once the rendered advisory is a provably total, byte-stable function of `(roadmap, feedback-log.md)`.

## QA Complete
