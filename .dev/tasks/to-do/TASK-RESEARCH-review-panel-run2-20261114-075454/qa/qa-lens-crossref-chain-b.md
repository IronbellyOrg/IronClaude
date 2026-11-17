# QA Report - Crossref-Chain Integrity, Instance b

**Topic:** one unified central Review Panel (shared core plus thin modules) from E1, E2 and E3 (run 2, report only)
**Date:** 2026-11-14
**Phase:** report-qualitative (lens: crossref-chain, instance b)
**Range reviewed:** lines 2115 to 5057 of `RESEARCH-REPORT-review-panel-unification-run2.md` (Sections 6 to 10, Appendix A pointer, Appendix B); MODE: SPLIT per `qa/report-size-and-partition.md`
**Grading:** `qa/grading-override.md` applies (BLOCKING only for decision/deliverable/safety; everything else MINOR with `(minor under grading override)`)
**Status:** Complete (Overall Verdict: FAIL, 1 blocking, 4 minor)

---

## Work log

### Checklist item d: 6.12 undecidable conflicts -> debate folder and result (PASS)

- 6.12.9 (lines 3458-3480) and 6.12.9.1 (lines 3482-3503) name 15 slots and 15 slugs. Glob `reviews/adversarial/*/ADJUDICATION-RESULT.md` returns 15 files and Glob `reviews/adversarial/*/proposal-[ab].md` returns 30 files; all 15 slugs match folder names. The merged-output file names listed in Section 10 (lines 4929-4943) match a Glob of `reviews/adversarial/*/merged*.md` (six slugs carry a slug-named file, nine carry `merged-output.md`). Three folders were Globbed under `adversarial/` and match the Section 10 listing.
- Routing closure: every `ROUTED: C-nn` cell (Grep, lines 3175-3346) maps to a slot whose Conflict IDs column lists the same ID (Table A 6, Table B 1, Table C 22, Table D 6, Table E 20 counting CO-31). The 6.12.10 arithmetic (189 total, 134 decided, 55 routed) re-adds correctly.
- Score and invariant counts: the HIGH counts quoted per slot in 6.12.9.1 and in the choices table agree with 7.3 and with the Q-41..Q-88 rows (total 60 HIGH re-added from the Q rows: C-01 1, C-02 3, C-03 2, C-05 7, C-06 4, C-07 1, C-08 13, C-10 5, C-11 6, C-12 2, C-13 2, C-14 12, C-15 2). Base-selection scores for all 15 slots are present in the 15 result files (Grep).

### Checklist item c: Section 7 recommendation -> Section 6 options and 6.12 outcomes (PASS)

- The 11 axes of the Section 7 rationale table map one to one onto 6.1..6.11; the option lists in each axis row match the option blocks of 6.1..6.11 (axis 3 four options = 6.3 options 1-4; axis 6 = 6.6; axis 8 = 6.8).
- "Adjudicated winners by axis" (6, lines 2997-3018), the adjudication register (7, lines 3825-3850), 6.12.9.1 and the A-3..A-20 table (7, lines 3627-3646) agree on winner, hybrid base and conflict slot for all 18 labels (12 overturned in whole or part, 6 confirmed: 12 + 6 = 18). Slot coverage line (3850: 15 slots, 18 rows) re-added correctly.
- Section 7 references to Section 9 resolve: Q-04, Q-09, Q-38..Q-46, Q-53..Q-61, Q-68..Q-70, Q-72..Q-74, Q-77, Q-78, Q-80..Q-85, Q-87, Q-89..Q-93 all exist; 9.10 coverage arithmetic (Q-38..Q-93 = 56 rows; 244 = 60 + 161 + 23) is consistent.

### Checklist item b: Section 6 options -> evidence (PASS with a convention note)

- A scripted count over lines 2115-3106 shows every one of the 43 option or comparison blocks carries at least 2 evidence keys (R01..R18, W01..W04); minimum is 6.10 Option 1 with 2. The evidence is cited through research-file keys (Reading guide, line 2127), not through direct "Section 2" or "Section 5" references; Section 2 and Section 5 summarise the same files. No option stands without evidence (see note N-4).

### Checklist item e: value inventory destinations (8.1) -> architecture in 7.1 (FAIL, see finding 1)

- Structural facts re-verified: synth-08 has 6,127 lines and 5,950 `VL-`/`DR-` rows; per-heading counts (CORE 948, MODULE-reflect 278, MODULE-tasklist 340, MODULE-spec 69, MODULE-pr-review 45, MODULE-rfqa 53, EVAL 1,365, HARNESS 467, KNOWLEDGE 416, DROP 1,969) equal 8.1.0 and 8.1.2; heading lines (45, 997, 1279, 1623, 1696, 1745, 1802, 3171, 3642, 4062) equal the 8.1.2 table.
- Semantic sample: 30 CORE rows (every 32nd from the 5th) plus 19 MODULE-spec / pr-review / rfqa / reflect rows were read against 7.1. 45 of 49 are consistent with 7.1 (tier file, panel resolution, limits repair, verdict as plug point, run record, brief hooks, PR/rf-qa exposures). The inconsistent rows are the blind-grader and E3i-script rows listed in finding 1.
- A targeted probe (not a sample) found 30 CORE rows about the installed-only variants (`stoprule.py`, `diffgate.py`, `review_ledger.py`, `sc-diffgate`, `sc-review-ledger`) and 6 CORE rows about the blind grader.

### Checklist items a and f

- Both start in Sections 2 to 4 (instance a range). Only their end points in my range were checked: Section 7 and Section 9 carry the resolution targets (see item c), and the OQ carry-over from 6.12.8 is covered in finding 3.

## Findings

| # | Severity | Section | Finding | Evidence | Proposed Fix |
|---|---|---|---|---|---|
| 1 | IMPORTANT (BLOCKING under the grading override: a value-inventory destination is wrong against the recommendation, rule 1) | 8.1 / Appendix A against 7.1 axes 4 and 10, 6.12.9.1 C-02, 7 adjudication register A-4 | The inventory routes the blind grader and the installed-only E3i scripts to CORE, but the recommendation keeps the grader out of the core and ports variant contracts, not scripts. Six rows send the grader or the computed-verdict script to CORE: VL-24-214 (artifact, "Verdict-computed-by-script and blind-grader contract"), VL-24-218 (`finding-grader.md`, "Blind grader dispatch role used by the verdict contract"), VL-24-268 (strategy, "Computed verdict with a blind heterogeneous grader"), VL-24-269 (`stoprule.py`, kind script), VL-24-295 (blocking-rule options) and VL-24-525, whose own Reason says "Slice proposes an optional MODULE stage; classified CORE here because the verdict contract needs it". Script rows VL-24-259 (`review_ledger.py`, "Script-kept ledger writer") and VL-24-278 (`diffgate.py`, "Script constants and blocking rule") are also CORE, and 30 CORE rows in all concern these scripts. Section 7 says the opposite: axis 4 (line 3614) "no category predicate and no blind grader in the core (the grader stays an optional instrument)"; register row A-4 (line 3832) "no module predicate, no grader in the core"; axis 10 (line 3620) "Port contracts, not scripts ... The blind grader and ledger sweep are optional modules or evaluation instruments". Nothing in Section 8 says the 8.1 destinations predate the adjudication fold: 8.1.4 limit 1 states only that rows with no cross-module signal "keep the destination its ledger gave and were not re-judged", and the only hit for "before the adjudication" in the report is the rename note at line 3555. A later plan that reads 8.1 as its input would put the grader and the variant scripts into the core. One row (VL-23-035, "Shared annotate must accept citation-only findings", CORE) and DR-113 ("Fix owner: CORE (one finding model, two locators)") also restate the withdrawn C-01 locator-agnostic `annotate`, but 7.1 element 1 already says DR-113 is avoided by engine separation, so those two are context, not part of the blocking claim | Report lines 3614, 3620, 3832, 3611-3612 (C-01), 4354-4362 (8.1.4); `synthesis/synth-08-value-inventory.md` lines 820, 822, 845, 852, 853, 860, 921 (read with awk, columns Kind, Destination, Reason); Grep of the report for "before the adjudication" returns line 3555 only | Add to 8.1.4 (and 8.1.3) a short table "Rows whose ledger destination differs from the adjudicated architecture" naming at least VL-24-214, 218, 268, 269, 295, 525, 259, 278 with the adjudicated destination (grader and stoprule: MODULE-spec optional stage or EVAL instrument; scripts: DROP as "contract ported, script not carried"), and state in 8.1.4 that all other rows keep pre-adjudication destinations; or re-route those rows in the synth-08 file and update the 8.1.0 counts and the 8.1.2 line ranges |
| 2 | MINOR (minor under grading override) | 6.12.9 coverage sentence (line 3480), Table B (3196-3219) | The coverage sentence lists FX-9, FX-10 and FX-13 among rows "whose Decision column says ROUTED", but Table B marks all three DECIDED-BY-EVIDENCE (only FX-15 is ROUTED, which the 6.12.10 count also says). The sentence also says each ROUTED row appears "in exactly the slot it names": FX-9 names "C-02 and C-03" but is listed only in C-03; FX-1 names C-06 but is listed in C-01 and C-06; FX-11 names C-02 and is listed in no slot. No outcome changes because the exposures themselves are decided | Report lines 3206-3213, 3475, 3480, 3511 | Reword the sentence to "exposure rows that name a slot in their Decision cell" and add FX-11 to C-02 or drop it from the sentence |
| 3 | MINOR (minor under grading override) | 6.12.8 / 6.12.10 / 8.2 / 2.9.8 | Four incompatible "open question" id schemes share the prefix: 2.9.8 `OQ-01..OQ-18`, Section 6 `OQ-1..OQ-15` (lines 3061-3075), 6.12.8 `OQ-1..OQ-25`, 8.2 `OQ1..OQ24`. G24 (line 4448) and axis 11 (line 3621) cite "OQ-18" for the PR per-round cost, which is 6.12.8 OQ-18; in 8.2 the same label without a hyphen is the Stage 2 exit question and in 2.9.8 it is the plugin skill allowlist. 6.12.10 (line 3537) says OQ-1..OQ-25 are "carried to Section 9", but Section 9 has no OQ ids (it keys rows to GQ ids), and at least OQ-1 (C-S12, tasklist skill names Tier-3 task-builder remediation while reflect defaults to the plan route, DR-065) has no Section 9 row (Grep for "C-S12" and "DR-065" finds lines 3186 and 3432 only). The content is low-stakes (a text fix) and the costs it raised appear under GQ ids | Report lines 1023-1040, 3061-3075, 3432-3456, 3537, 4448, 4623-4646; Grep results above | Qualify each id with its section (for example "6.12.8 OQ-18"), and add an OQ-to-Q map or one Section 9 row for OQ-1 |
| 4 | MINOR (minor under grading override) | 6.1..6.11 | Option blocks cite research files (R01..R18, W01..W04), not Sections 2 or 5 of the report, so the lens wording "references evidence from Section 2 or 5" is met by convention (Reading guide, line 2127), not by direct references. All 43 blocks carry at least 2 evidence keys | Scripted count over lines 2115-3106 | None required; optionally add "see Section 2.x" beside the main R-key cites |
| 5 | MINOR (minor under grading override) | 7.2 line 3762 against 7.1 element 6 | 7.2 says M4 (per-slot lens) is "reserved in element 6"; element 6 lists the per-slot `lens` key under "Not now ... (withdrawn in C-11)". "Reserved" and "withdrawn" are read differently by a later plan, but the C-11 outcome (no per-slot key in the first change) is stated the same way in both places | Report lines 3762, 3722, 3790 | Use one word ("withdrawn from the first change, reserved as a module parameter") in both places |

## Summary

- Links traced: d (15 of 15 undecidable conflicts to an existing folder and result, 55 of 55 routed rows to a slot), c (11 axes and 18 adjudicated labels against Section 6 and 6.12.9.1), b (43 of 43 option blocks), e (49 sampled rows plus 36 targeted rows; counts re-run on synth-08), plus Section 7 to Section 9 and Section 10 path checks (179 path tokens extracted; the 55 reported missing are bare file names, wildcard patterns or names relative to a listed folder, and the debate-folder files were then confirmed by Glob).
- Findings: 5 in total. Blocking under the grading override: 1 (finding 1). Minor under the grading override: 4 (findings 2 to 5), recorded as notes.
- Checks passed: 3 of 4 in-range lens items (b, c, d); failed: 1 (e). Items a and f begin in instance a range and were checked only at their end points in my range.
- Confidence: Verified: 4/6 | Unverifiable (start outside instance b range): 2 | Unchecked: 0 | Confidence: 100.0% on the in-range items. Verdict FAIL is driven by finding 1, not by confidence.
- Tool engagement: Read about 30 | Grep 17 | Glob 6 | Bash 6 (read-only: wc, grep, awk, test -e). Web research: none, so no Tavily call was needed.
- Self-audit: Verified against files: 15 ADJUDICATION-RESULT files, 30 proposal files, 15 merged files, three debate `adversarial/` subfolders, synth-08 (counts, headings, 49 sampled rows, 36 targeted rows), Sections 6.12, 7, 8, 9, 10 of the report. A review that reported zero here would have missed that Section 8.1 was built before the adjudication fold and was never re-checked against it (finding 1).

## Inherited Structural Verdict - Reliance Audit

No `## Inherited Structural Verdict` section was in the spawn prompt, so there is no reliance on an rf-qa verdict; every check above was verified directly.

## Self-Audit

**(a) Reliance list:** none (no inherited verdict supplied).

**(b) Independent semantic checks:**
- Value-inventory destination against the adjudicated architecture, verified by awk over `synthesis/synth-08-value-inventory.md` (rows at lines 820-921) and Section 7 lines 3614, 3620, 3832.
- Routing closure of every `ROUTED` cell against slot Conflict IDs, verified by Grep over report lines 3175-3346 and the table at 3462-3478.
- HIGH-invariant arithmetic across 6.12.9.1, 7.3 and Q-41..Q-88, re-added by hand from the Q rows.

## Recommendations

- Fix finding 1 before Gate 3 closes: either add the reconciliation table to 8.1.4 or re-route the listed rows in synth-08 and update 8.1.0 and 8.1.2.
- Findings 2 to 5 go on the follow-up list; do not fix them in the gate.

## QA Complete

**Overall Verdict: FAIL** (one blocking finding under the grading override)

**Status:** Complete
