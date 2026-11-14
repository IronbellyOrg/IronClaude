# QA Report — Synthesis Fix Verification (Qualitative, fix cycle 2: repeat cycle 1)

**Topic:** Orchestrator mode Phase 1 (issue #339), synthesis gate, last allowed review
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 2 (repeat cycle 1; |F_0| = 15, |F_1| = 3)
**Fix authorization:** false (report only; no synthesis file edited)

**Inputs read:** `qa/qa-consolidated-findings-phase5-cycle1.md` (C1-01 to C1-03), `qa/qa-synthesis-fix-log-cycle1.md`, `qa/qa-synthesis-verification-qualitative.md` (previous qualitative report; N-1 = C1-02, N-2 = C1-03), `synthesis/synth-01` to `synth-06` (read in chunks of at most 120 lines).

**Scope of re-check:** all three open findings trace to the qualitative reports (C1-01 is B-12, first raised by qu-1 #3; C1-02 is B-14 / N-1; C1-03 is B-13 / N-2). Each is re-checked, plus the spill-over edit to `synth-02` 4.8 and the five global checks (no new cross-file contradiction, Section 8 plans the Section 7 option, WC-10, A4, later phases recorded not designed). Adversarial stance: at least five fixes were assumed wrong until each was disproved by a re-read.

---

## Original findings, re-checked

| ID | Origin | Result | Evidence (re-read this cycle) |
|---|---|---|---|
| C1-01 | B-12 (qu-1 #3), structural B-12 OPEN | RESOLVED | S3 `:114` now reads "Phase 1 keeps person-wait time out of activity ages and the 6 h activity window; the waiting-on-a-person list prints the time since the wait began (R4)." This agrees with R4 `:216` ("prints and sorts on the question's original age, the time since the wait began") and R7 `:219` (sort by time since the wait began). The old "out of any age it prints" claim is gone. |
| C1-02 | B-14 (qu-1 #5, qu-2 M-1), qualitative N-1 | RESOLVED | S5 `:10` now reads "(waiting on a person, working, stalled (proved), finished, could not determine, idle: the research question's six; Section C adds fenced as a seventh, the working default, OQ-13)". Same six names and attribution as S3 `:7`. Header check of S1, S4, S6 is below. |
| C1-03 | B-13 (qu-1 #4), qualitative N-2 | RESOLVED | S3 `:183` now says four external patterns contradict WC-10 (D5, D6, D1, D2 in part) and that D3 and D4 are rejected as naming or actions. This matches S3 `:81` (D1 "is what WC-10 forbids"), `:95` (Nagios "partly contradicts"), `:100` (Grafana "partly contradicts"), `:108` (Harmonograf "contradicts in naming"), `:118` (agents-fleet "contradicts WC-10"). "Kubernetes node status at the status layer" stays in the supporting list, consistent with `:81` "WC-10 consistent at the status layer". The S3 D1-D4 numbering equals web-01's (`web-01:181-184`), so S2's "web-01 D1, D3, D4" labels point at the same patterns. |
| C1-03 spill-over | S2 4.8 `:290` | RESOLVED | Row now names Kubernetes taint/eviction (D1) and liveness-probe restart (D4), and Harmonograf "stuck" with UI alert only (D3), and says "Only D1 contradicts WC-10; D3 is naming and D4 an action (synth-03 5.9)". Scoped to the three web-01 patterns in that row, this matches S3 `:183`. Grafana (D5) has its own 4.8 row `:289`. S2 `:153-154` (D3 note only; D1, D4 rejected, no action) also agree. |

## Global checks (full sweep of synth-01 to synth-06)

| # | Check | Result | Evidence |
|---|---|---|---|
| G-1 | No fix introduced a contradiction between synthesis files | PASS | Grep over `synthesis/` for "three external", "contradicts WC-10", "any age it prints", "act on a timeout": the only hits are the fixed S3 `:183`, S2 `:290`, and the unchanged Grafana/agents-fleet lines (S3 `:118`, `:201`; S2 `:317`; S6 `:144`, `:215`), all consistent with the new count of four. S6 rows 94-97 (`:140-143`) rule every web-01 D1-D4 "codebase wins", which matches S3 `:183` rejecting all six D-patterns. S6 `:184` and `:214` still map D1-D4 to rows 94-97. The person-wait wording in S2 `:152` ("exclude person-wait time from activity ages and the 6 h activity window (the waiting list still sorts on time since the wait began)") and S2 `:90` match the new S3 `:114`, as do S4 `:242` and S5 step 1.5 `:63`. The six-class header wording is the same in S3 `:7`, S4 `:3`, S5 `:10` and S6 `:3`. S2 `:65` and S6 row 98a `:145` keep fenced as the seventh class and the working default, matching S5 OQ-13 `:225`. |
| G-2 | Section 8 plans the option Section 7 recommends | PASS | S4 `:191` "Recommended option: A1"; S5 `:6` plans A1 (CLI `superclaude sweep`, `/sc:sweep`, `sc-sweep-protocol`, WC-14). S2 `:16` and `:183` also target A1. None of the edited lines touch option choice. |
| G-3 | WC-10 (absence is never proof of death) kept | PASS | S5 1.3 `:61` (unverifiable, late heartbeat, stale status, missing row give could not determine); S2 rule 7 `:49-51`, SC-5 `:115`, constraint `:134`. The new S3 `:183` strengthens WC-10 by naming D1 eviction-after-`Unknown` as a contradiction. The new S2 `:290` keeps "only Orca stall proofs count". |
| G-4 | Option A4 not recommended | PASS | S4 `:150` "(REJECTED, [CODE-CONTRADICTED])", R-1 to R-4 `:160-163`, excluded from comparison `:174`; S1 `:143`; S2 `:144`, `:183`, `:197`; S3 `:185`; S5 `:18`; S6 `:15`, rows 15 and 50. |
| G-5 | Later phases recorded, not designed | PASS | S2 `:143` and R-2 `:172` record `/sc:close`, resume, trust layer, orchestrator of orchestrators, management-server relay as recorded only; S4 `:246` and S2 `:161` keep restart/kill/evict/retry as later phase only; S5 `:116-124` one line each. No fix added later-phase design. |

## New blocking findings

None. Each fix was read in place and against every other mention of the same subject in the six files. No fix introduced a contradiction, a scope change or a WC-10 break.

## Minor notes (do not fail the review; not rechecked)

| # | Location | Note |
|---|---|---|
| M-8 | S3 `:183` | Says D3 and D4 are "rejected as actions or naming". The 5.9 table outcomes for D3 and D4 read as "note column only" and "later phase only", so "rejected" is slightly stronger than the table. Wording only. |
| M-9 | S2 `:290` | "Only D1 contradicts WC-10" is scoped to the three web-01 patterns in that row. Read alone, it could seem to clash with S3's count of four (D5 has its own row `:289`; D2 and D6 are not in S2 4.8). Adding "of these three" would remove the doubt. Not a contradiction. |
| M-10 | S4 `:246` | Groups "evict" with "later phases only", while S3 D1 `:169` rejects eviction after `Unknown` outright. Consistent with `web-01:198`, `:206` (any later action is gated on Orca stall proof, never on `unverifiable`), but the line could say "on stall proof only". Pre-existing, not a fix. |
| M-11 | S6 `:223` | Lists synth-05 as "planned; not yet written". Stale now that synth-05 exists. Pre-existing, not a fix. |
| M-3, M-4 | S5 `:61`; S1 `:15` | Carried from the previous report (S5 cites "8.2"; S1 "The question." still lists seven classes; the fix log `:13` records that this optional alignment was not done). Not rechecked. |

## Items that PASS

C1-01, C1-02, C1-03, the C1-03 spill-over in S2 4.8 `:290`, and global checks G-1 to G-5.

## Summary

- Original blocking findings re-checked: 3 (plus 1 spill-over edit). Resolved: 3. Open: 0.
- New blocking findings: 0. New minor notes: 4 (M-8 to M-11).
- |F_0| = 15, |F_1| = 3, |F_2| = 0. The count fell each cycle.
- Adversarial stance: at least five fixes were assumed wrong. None was confirmed wrong after reading each edited line, its neighbours, and every other line in the six files on the same subject.

## Confidence

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (9 items = 4 finding rows + 5 global checks.)
- **Tool engagement:** Read: 22 | Grep: 7 | Glob: 0 | Bash: 0 (approximate, counted over both context windows of this review). Every synthesis file was read in chunks of at most 120 lines. `research/web-01` was checked by grep at `:136`, `:159`, `:181-184`, `:196-206`.
- Web research: none was needed and none was done. Tavily was not used, and no fallback was used.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No Inherited Structural Verdict was provided, so this review ran standalone. No rf-qa PASS was relied on. The fix log's "fixed" statuses were treated as claims and re-read, not trusted.

**(b) Independent semantic checks (at least one required, INV-019):**
- D-numbering identity: S2's "web-01 D1, D3, D4" labels were checked against `web-01:181-184` and S3 `:169-174`, which confirmed that they name the same patterns. Read and Grep.
- The four-contradiction count in S3 `:183` was checked line by line against S3 `:81`, `:95`, `:100`, `:108`, `:118` and `web-01:136`, `:159`, `:163`. Read and Grep.
- The person-wait wording was checked across S2 `:90`, `:152`, S3 `:114`, `:216`, `:219`, S4 `:242` and S5 `:63`. Read.
- The later-phase "evict" wording in S4 `:246` was checked against `web-01:198`, `:206`. Grep. This gave M-10, not a blocker.

## Recommendations

- Proceed past the synthesis gate. Optionally fold in M-8 to M-11 and M-3 and M-4 in the assembly pass. None is required.

## QA Complete

## Verdict: PASS
