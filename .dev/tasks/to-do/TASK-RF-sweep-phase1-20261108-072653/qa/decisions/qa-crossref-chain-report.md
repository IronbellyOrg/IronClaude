# QA Report - Cross-reference chain (item 7.27, rf-qa-qualitative)

**Date:** 2026-11-12
**Phase:** decisions gate, cross-reference lens
**Fix authorization:** false (report only)

Convention used for the table: a check is FAIL only when a BLOCKING or MAJOR finding attaches to it. A check with only MINOR notes is PASS and the note is cited.

Paths below are relative to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/` (call it `P`) unless they start with `src/`, `tests/` or `docs/`. `TASK` means `P/TASK-RF-sweep-phase1-20261108-072653.md`. `PLANS` means `P/phase-outputs/plans/`. `DESIGN` means `docs/designs/orchestrator-mode.md`. No `## Inherited Structural Verdict` block was in my prompt, so I ran standalone and re-checked links myself.

## Checks

| Check | What was traced | Result |
|-------|-----------------|--------|
| C1 | OQ-1 record `Applied by` <-> items 6.1 to 6.4 and gate 6.5 to 6.22 <-> the DESIGN R5 edit surface (note L-4) | PASS |
| C2 | OQ-2 Blocks (9.1) <-> item 7.1 Blocks <-> item 7.2 halt text <-> item 9.1 Context | PASS |
| C3 | OQ-3 Blocks (12.1 to 12.3) <-> items 7.3/7.4 <-> item 12.1 gate; items 12.2 and 12.3 only transitive (note L-3) | PASS |
| C4 | OQ-4 Blocks (8.12) <-> items 7.5/7.6 <-> item 8.12 gate | PASS |
| C5 | OQ-5 Blocks (8.12, 9.1, 10.5) <-> items 7.7/7.8 <-> items 8.12 and 9.1 cite it; item 10.5 does not (note L-2) | PASS |
| C6 | OQ-6 historical Blocks (8.12, 11.3) <-> item 7.9 request <-> item 7.10 halt <-> items 8.12 and 11.3 gates; record and item 7.9 left unchanged, as the lens requires | PASS |
| C7 | OQ-6 additive revision chain: 7.10 style -> 7.13 -> 7.20 -> 7.21 to 7.28 -> 8.12 -> 11.3 skill -> 11.4 tests -> 11.5, and the delta-manifest rows for those labels | PASS |
| C8 | OQ-7 Blocks (8.4 and every later item) <-> items 7.11/7.12 <-> item 8.4 gate and Action | PASS |
| C9 | OQ-8 Blocks (7.16, the 1.0a items, 9.3) <-> items 7.14/7.15 <-> items 7.16 and 9.3 Context | PASS |
| C10 | OQ-17 Blocks (7.17, step 1.2 and later, 8.10, 10.3) <-> item 7.17 branch text <-> Execution Log HALT row <-> 1.0a-facts refusal line <-> items 8.10 and 10.3 (note L-3) | PASS |
| C11 | OQ-18 absent <-> facts "outcome (b) does not fire" <-> item 7.20 SKIP rule | PASS |
| C12 | `owner-decisions.md` seven rows and their "Steps it unblocks" cells <-> the Blocks line of each record OQ-1 to OQ-7 | PASS |
| C13 | `owner-decisions.md` <-> the RESOLVED OQ-17 record, as items 7.22 and 7.25 require (finding X-1) | FAIL |
| C14 | Anchors the records cite: DESIGN lines 559, 822, 836, 894, 995, 1012; probe section 3 at line 461; research/09 line 98; probe headings used by the facts file | PASS |
| C15 | Gate-chain file names: items 7.21 to 7.28 Output <-> item 7.29 list <-> items 7.30 to 7.37 <-> item 8.1 `qa/decisions/gate-decision.md` | PASS |
| C16 | `### Open Questions` entries OQ-1 to OQ-8, OQ-17, OQ-18 <-> records and Execution Log (note L-1) | PASS |
| C17 | Fixture chain: item 7.18 -> `SOURCES.md` rows -> probe sections -> item 10.1 synthetic-file rule -> item 10.3 no-binding case | PASS |
| C18 | Style file seven table sites <-> item 7.10 Action <-> design-addendum common rule <-> item 11.3 required clauses <-> item 11.4 required pins | PASS |
| C19 | Authorization chain: item 7.10 `## Execution authorization (verbatim)` <-> result file <-> item 7.20 checks S5 to S7 <-> Execution Log row <-> `owner-decisions.md` GQ-63 section (existence and path links only) | PASS |

## Findings

### X-1 (MAJOR): `owner-decisions.md` has no row for the RESOLVED OQ-17 record, and its closing sentence is now false

- Evidence, record side: `PLANS/OQ-17-cursor-template-decision.md:3` is `status: RESOLVED`; lines 35 to 40 hold `Chosen:` (refuse the extra cursor command), `Decided by:` and `Decision source:` quoting "Keep the 10 commands (Recommended)"; line 33 says it blocks item 7.17, step 1.2 and every later item, including 8.10 and 10.3.
- Evidence, plan side: `TASK:1307` (item 7.22) requires `owner-decisions.md` to hold "seven decision rows, plus one row for each resolved OQ-17 or OQ-18 decision file that exists"; `TASK:1328` (item 7.25) says the same for the decision-fidelity lens. `PLANS/OQ-17-cursor-template-decision.md` exists and is RESOLVED (`P/phase-outputs/test-results/decisions-mechanical.md:27`, C2 PASS).
- Evidence, index side: `P/artifacts/owner-decisions.md:5` is headed "Decisions (seven rows)" and rows 9 to 15 are OQ-1 to OQ-7 only. Line 55 reads "Still open and not recorded here as decisions: OQ-8 (the Run id, item 7.14) and the optional OQ-17 and OQ-18 (only if step 1.0a fires them)". That was true when item 7.13 ran. It is not true now: OQ-8 is RESOLVED (`PLANS/OQ-8-run-id-decision.md:3`), and OQ-17 fired (`P/phase-outputs/discovery/1.0a-facts.md:54`) and is RESOLVED.
- Why it matters: the OQ-17 outcome (keep `ALLOWED_ORCA` at exactly 10, no paging by cursor) is carried to item 8.10 only through the facts file (`1.0a-facts.md:56`). The decisions index that every later reader is told to use does not list it, so the record-to-index link the lens checks is missing.
- Nothing in item 7.17's resume text (`TASK:1272`) or item 7.13 tells anyone to add the row, so no later step will add it by itself.
- Smallest fix: append one row to the table in `P/artifacts/owner-decisions.md` for OQ-17 (option: refuse the extra cursor command, allowlist stays 10; words: "Keep the 10 commands (Recommended)"; decider Ryan Wiancko, owner, 2026-11-11; source `PLANS/OQ-17-cursor-template-decision.md:35-40`; unblocks: item 7.17 resume, step 1.2 and later, 8.10 and 10.3 keep 10 templates). Replace the line 55 sentence so it says OQ-8 and OQ-17 are RESOLVED and OQ-18 was not written. Item 7.30 lets the fix agent edit this file (`TASK:1363`). Do not change any `Chosen:` line.
- This finding overlaps the record-form lens (item 7.22) and the decision-fidelity lens (item 7.25); the consolidation step (item 7.29) should merge duplicates.

## MINOR notes (never fail the gate)

### L-1 (MINOR): Open Questions bullets still read PENDING

`TASK:2989` to `TASK:2995` show OQ-2 to OQ-6 as "OWNER DECISION PENDING", OQ-7 as pending and OQ-8 as "PERSON INPUT PENDING"; `TASK:3004` shows OQ-17 as "OWNER DECISION PENDING only if it fires". All eight records are RESOLVED and the Execution Log has the resolution rows (`TASK:2806`, `2808`, `2812`, `2817`, `2819`, `2821`, `2823`, `2815`). Item numbers inside the bullets are right (7.1/7.2, 7.3/7.4, 7.5/7.6, 7.7/7.8, 7.9/7.10, and the 9.3 mention for OQ-8). The delta-manifest says stale Open Questions rows are kept as history (`revisions/chat-output-exception-20261109-133150/delta-manifest.md:121`), and no Phase 7 item tells the executor to update them, so this is by design. Fix, if wanted: add "RESOLVED, see Execution Log" to each bullet.

### L-2 (MINOR): OQ-5 names item 10.5 but item 10.5 never cites OQ-5

`PLANS/OQ-5-GQ-61-window-decision.md:29` and item 7.7 (`TASK:1189`) say OQ-5 blocks items 8.12, 9.1 and 10.5. Items 8.12 (`TASK:1501`) and 9.1 (`TASK:1631`) cite it. Item 10.5 (`TASK:1812`) cites OQ-4 and OQ-6 and says nothing of OQ-5, GQ-61 or a window. The DESIGN `test_report.py` row (`DESIGN:761`) has no window case either. So the dependency is either phantom or a window test is unspecified. It is covered in practice: item 10.5 tests `report.py` from item 8.12, and the item 7.8 clause makes a 72 h answer apply to every later item. Fix, if wanted: add "window default per the OQ-5 record" to item 10.5 Context.

### L-3 (MINOR): three blocked items rely on a gate item instead of citing the record

- OQ-3 names items 12.1 to 12.3 (`PLANS/OQ-3-GQ-11-rule-id-decision.md:30`). Only item 12.1 cites OQ-3 (`TASK:2111`, `2112`). Items 12.2 and 12.3 follow 12.1 in order, and `DESIGN:949` and `DESIGN:950` gate steps 1.18 and 1.19 on 1.17.
- OQ-17 names items 8.10 and 10.3 (`PLANS/OQ-17-cursor-template-decision.md:33`). Item 8.10 (`TASK:1487`) gates on "step 1.0a facts (item 7.17)" and checks that `ALLOWED_ORCA` has 10 entries (`TASK:1490`); item 10.3 (`TASK:1798`) pins ten templates and a gated no-binding fixture. Neither cites OQ-17. Item 8.10 lists "the cursor field" as an input (`TASK:1487`) without the "do not page by it" rule, which sits only in `1.0a-facts.md:56` and `TASK:1272`. The 10-entry check blocks a wrong build, so this is a clarity gap, not a defect.
- Fix, if wanted: one clause in item 8.10 Context, "OQ-17 refused a cursor template: do not page by the cursor field".

### L-4 (MINOR): the R5 edit surface is listed three ways

The OQ-1 record `Applied by` names DESIGN sections 7.3, 11, 13, 15.1 and the GQ-109 row (`PLANS/OQ-1-agent-wait-decision.md:41`). Item 6.3 Output names sections 4, 7.3, 11, 12, 13, 15.1, the GQ-109 row and the Fix cycle 3 table (`TASK:1000`). The Context of items 7.21 to 7.28 names sections 7.3, 11, 12, 13, 15.1, the GQ-109 row and the Fix cycle 3 row, and leaves out section 4 (for example `TASK:1299`). The section 4 edit is live (`DESIGN:221`). Phase 6 Findings R-12 (`TASK:2947`) added section 4 to the Phase 6 lists but not to Phase 7. The R5 gate already passed, and the record is a frozen owner record, so this is a note.

### L-5 (MINOR, informational): consumers of OQ-2 and OQ-5 that the records do not list

Item 11.1 (`TASK:1958`) takes its `--output` and `--window` defaults from the OQ-2 and OQ-5 records, and item 10.5 takes its layout from OQ-4. The records list only 9.1 / 8.12 (and 10.5 for OQ-5). All of them follow the listed items, so the chain holds. The lens does not ask for edits to resolved records.

## Link traces that held (evidence)

- Blocks lines match the Phase 7 record items word for word: OQ-2 (`TASK:1147`, record line 27), OQ-3 (`TASK:1161`, record line 30), OQ-4 (`TASK:1175`, record line 36), OQ-5 (`TASK:1189`, record line 29), OQ-6 (`TASK:1203`, record line 28), OQ-7 (`TASK:1217`, record line 36), OQ-8 (`TASK:1237` and `TASK:1244` name items 9.3 and 7.16; record line 22), OQ-17 (`TASK:1267`, record line 33).
- Each HALT item names the record it reads and each record names its HALT item: 7.2 and OQ-2 line 29; 7.4 and OQ-3 line 32; 7.6 and OQ-4 line 36; 7.8 and OQ-5 line 29; 7.10 and OQ-6 line 28; 7.12 and OQ-7 lines 28 and 36; 7.15 and OQ-8 line 22.
- Revision-path rules named in the records match the HALT items: OQ-2 sections 1, 3, 10, 12; OQ-3 sections 8, 9, 10, 12, 15, 16; OQ-7 sections 7.2, 11, 13, 14.
- Blocked items cite the right record with the right item range: 8.4 -> OQ-7 (7.11); 8.12 -> OQ-4, OQ-5, OQ-6 "items 7.5 to 7.10"; 9.1 -> OQ-2, OQ-5; 9.3 -> OQ-8 (7.15); 11.3 -> OQ-6 "items 7.9 and 7.10"; 12.1 -> OQ-3 "items 7.3 and 7.4".
- OQ-6 additive chain, with historical text untouched: the record keeps its Blocks line "Items 8.12 and 11.3" (line 28) and its `Chosen:` text (lines 32 to 35); item 7.9 (`TASK:1201`) is unchanged. The revision path is item 7.10 (`TASK:1209`, reads the addendum, the revision `BUILD-REQUEST.md`, `delta-manifest.md`, `qa/research-gate-cycle1.md`, the four research files; writes the result file) -> items 7.13, 7.20 and 7.21 to 7.28 (each adds the same revision inputs) -> 8.12 (`TASK:1501`, reads addendum and result file, renderer unchanged) -> 11.3 (`TASK:1972`/`1973`, HALT text "Step 1.15 needs the checked and separately authorized OQ-6 (b) style exception") -> 11.4 (`TASK:1979`, reads style, skill, addendum, research/01, research/04, the unchanged OQ-6 record and the 7.10 result) -> 11.5 (`TASK:1986`, reads `test-sweep-command-summary.md`, which 11.4 writes at `TASK:1981`). The `delta-manifest.md` execution chain at line 11 and the 7.27 row at line 30 describe exactly this chain.
- The style file carries every clause the later items must repeat: lines 22 (primary rule) and 57, 62, 64, 73, 84, 94 (six qualified restatements; count 6 from `decisions-mechanical.md` S1), 23 to 26 (assignment, exclusions, "Formatting never authorizes advice the sweep skill prohibits", "not a runtime detector"). Item 11.3 Action and item 11.4 Action name the same clauses, and 11.4 does not demand a runtime-detector absence.
- All anchors cited in the records resolve: DESIGN line 559 (cursor template sentence), 822 (section 13 heading), 836 (row D9), 894 (step 1.0a runs against a named Run), 995 (open item 5), 1012 (open item 22), 1015 (`Total: 23 open items.`), 839 (`Total: 10 deviations.`); `readonly-probe.md` headings at the line numbers the facts file gives (12, 441, 455, 461, 475, 735, 785, 830, 910, 964, 968, 982, 997, 1015); `research/09-gap-fill.md:98`; the design reference to the revision at `DESIGN:1051`.
- The Execution Log has one row matching the item 7.17 PENDING pattern (`TASK:2807`), and the resume row follows it (`TASK:2806`).
- Fixtures: `SOURCES.md` has 19 rows for the 19 `captured-*.json` files in `tests/sweep/fixtures/`; every row names a probe section that exists; all eight templates 1 to 8 have a captured file, so item 10.1 writes no synthetic file.
- Gate file names agree end to end: the eight reports named in item 7.29 equal the eight Output paths of items 7.21 to 7.28 (this report is the item 7.27 one); item 8.1 reads `qa/decisions/gate-decision.md`, which item 7.37 writes.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. The prompt carried no `## Inherited Structural Verdict`; I ran standalone and relied on no earlier QA report. I did read `decisions-mechanical.md` as an input only and re-ran none of its commands.

**(b) Independent semantic checks (at least one required, INV-019):**
- Record-to-index completeness for OQ-17: read `OQ-17-cursor-template-decision.md` in full, then `owner-decisions.md` in full, then `TASK:1307` and `TASK:1328`; found the row missing (finding X-1).
- Reverse-citation test for every Blocks entry: grepped the task file for each OQ/GQ id (output of `-o` hits by line) and read items 8.4, 8.10, 8.12, 9.1, 9.3, 10.3, 10.5, 11.1, 11.3, 11.4, 11.5, 12.1 to 12.3 to see which cite the record (notes L-2, L-3).
- Additive OQ-6 chain: read the delta-manifest rows for 7.27, 8.12, 11.3, 11.4, 11.5, then the Context/Action text of each task item and the style file lines 22 to 26 to confirm the same clauses appear in each.
- Anchor test: grepped DESIGN for headings and rows the records quote and compared line numbers.

Web research: none; no Tavily or fallback call was made.

## Summary

- Checks passed: 18 / 19
- Checks failed: 1 (C13)
- BLOCKING findings: 0
- MAJOR findings: 1 (X-1)
- MINOR notes: 5 (L-1 to L-5)
- Confidence: Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (scope: the cross-reference lens only; the transcript match behind item 7.20 S7 and the line-by-line APPROVED quotes belong to other lenses and were not re-run)
- Tool engagement (approximate, counted from this session): Read: 38 | Grep: 15 | Glob: 5 | Bash: 4

Verdict: FAIL
Blocking count: 1
