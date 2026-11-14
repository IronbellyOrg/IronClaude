# QA Report: numbers and metrics lens (R3-B3 gate)

Date: 2026-11-09
Phase: doc-qualitative, numbers lens (domain lens, research/09 Gap 5)
Fix cycle: N/A (fix_authorization false)

Scope: recount of every number touched by items 4.1 to 4.5 of research/04 section 4, against `docs/designs/orchestrator-mode.md` (1030 lines on disk, `wc -l`), SPEC FR-010 (`merged-requirements.md:104`) and `phase-outputs/test-results/r3-b3-mechanical.md`. No file other than this report was written. No input was taken from the earlier QA reports in the gate folder.

## Recounts (my own tool output, not the producer's)

| Item | Expected | Found on disk | Evidence |
|---|---|---|---|
| SPEC FR-010 acceptance fixtures for incomplete cases | 3 (outage, full page after uncaptured continuation, incomplete list after `call_failed`) | 3 | `merged-requirements.md:104`, text "Incomplete cases [V3R3:33]: an older transcript during an outage; an older unjoined transcript after a full page with uncaptured continuation; an incomplete list after `call_failed`" |
| DESIGN names for those cases | 3 | 3 | `orchestrator-mode.md:746` ("the three SPEC incomplete cases"), `:771` ("three list-incomplete cases"), `:1030`, `:11` |
| `origin unknown:` literals | 3 | 3, in 7.2 and again in 11 | `grep -o` shows `:501` and `:746` each hold exactly `Orca unavailable`, `worker list truncated`, `worker list call failed`; `:1030` repeats the prefix only |
| Fixtures in the `test_classify.py` row | 4 | 4 distinct names | `grep -o 'test_fr010_...'` on `:746`: `outage_older_transcript_unknown_not_historical`, `full_page_uncaptured_continuation`, `call_failed_incomplete_list`, `incomplete_notes_order`; the same four names are at research/04 lines 197-200 |
| Row text "pinned by four fixtures" vs list | 4 = 4 | match | `:746` |
| Transcript age vs window | 8 h > 6 h | 8 h > 6 h | `:746` shared Given "`last_activity` 8 h before `now`", "window 6 h"; SPEC control "an 8 h old unmapped one is listed under Historical" |
| `WORKER_LIST_PAGE` | 100 | 100 | `:548`; fixture "exactly `WORKER_LIST_PAGE` (100) rows" `:746`; `:299` "<= 100 rows"; `:346` "a full 100-row page" |
| `Total: 9 deviations.` | 9 | 9 rows D1 to D9 (`:814-822`), one hit at `:824` | `grep -c '^| D[0-9]'` = 9 |
| `Total: 23 open items.` | 23 | 23 rows (`:976-998`), one hit at `:1000` | `sed -n 976,998p | grep -c '^| [0-9]'` = 23 |
| Em-dash count | 0 | 0 (en-dash also 0) | `grep -c` on the design |
| `four incomplete cases` | 1, only in section 18 | 1 at `:1030` | `grep -c` = 1 |
| Four join-incomplete cases | 4 | 4 (`:502` "in four cases" First to Fourth; `:771`, `:822`, `:860`) | read |
| Section ranges quoted by the mechanical file | 7.2 449-518, 7.4 559-598, 11 731-755 | match | `### 7.3` at 519, `### 7.5` at 599, `## 12` at 756 |
| Mechanical file: 9 commands, 9 checks, "9 of 9 PASS" | 9/9/9 | 9/9/9 | read of the file; I re-ran the greps for checks 3, 4, 6, 7, 8, 9 and got the same hits |
| SPEC size and id ranges quoted at DESIGN `:19` | 653 lines; FR 95-120 = 26; NFR 130-144 = 15 | 653; 26; 15 | `wc -l`, `grep -c '^| FR-'`, `grep -c '^| NFR-'` |
| Other counts in sections 11 and 12 near the edit | six path-B reader/parser fixtures; nine byte-limit boundaries; five exemptions; 7 new `tests/sweep` files incl. conftest; 3 edited test files; 8 templates / 7 verbs | all match | `:733`, `:745`, `:746`, `:771`, `:781`, `:526-535` |

No count in the edited text disagrees with the items it lists. No BLOCKING or MAJOR finding.

## Findings

All findings are MINOR. They never fail the gate.

### N1 (MINOR) Shared Given says the join guard holds, but the full-page fixture has 100 rows against a 50-call show cap
- Evidence: `docs/designs/orchestrator-mode.md:746` (shared Given: "the join guard otherwise holding (path A, `session_join` present on every scoped row)" and `test_fr010_full_page_uncaptured_continuation`: "exactly `WORKER_LIST_PAGE` (100) rows ... none joined to T"); `:341` (`worker-show` is `min(D, 50)`); `:976` and `:174` (open item 1: `session_join` is read from `worker-show`); `:502` (guard case 1 fires when `session_join` is None on any scoped row; case 2 fires when worker rows exist and no transcript joined).
- Problem: in a real run 50 of the 100 rows have no show result, so case 1 would fire and T would also carry `tab map join not observable`. If T is the only transcript, case 2 also fires and T carries the SP-16 literal. The asserted note still appears, so the test passes, but the Given is not true of a real page.
- Smallest fix: add to the fixture "built directly for `classify_all`, `session_join` set on all 100 rows, a second transcript joined to one row", or say the extra guard notes may follow the `origin unknown:` note.

### N2 (MINOR) "differ from the complete-negative-join control by one input" is looser than the fixtures
- Evidence: `:746`. The control has 2 transcripts, one mapped to an Orca row (SPEC `merged-requirements.md:104`); the new fixtures have one transcript T and no joined row. The call-failed fixture also adds a second Run.
- Smallest fix: change "by one input" to "by the list-completeness input only", or list the inputs.

### N3 (MINOR) SPEC FR-010 names four reasons, the design adds three notes; "tab map unreadable" has no rule
- Evidence: `merged-requirements.md:104` ("Orca unavailable, worker list truncated, worker list call failed or tab map unreadable"); DESIGN `:501` holds three notes; `grep -E 'tab map unreadable|tab map is read'` on the design finds nothing; `:401` `read_tab_map` has no failure result. research/04 line 187 quotes only the first three SPEC reasons.
- Scope: the SPEC wording is "such as" and the three acceptance fixtures are what R3-B3 restores, so this gate is met. It is a gap carried forward. A person-started True with an unreadable tab map and no worker rows is not excluded by the text.
- Smallest fix: record it as open item 24 (then change `Total: 23 open items.` at `:1000` to 24, and the mechanical check 9 string) or add a fourth note; do not leave the totals stale.

### N4 (MINOR) research/04 section 4 cites pre-edit DESIGN line numbers
- Evidence: research/04 line 207 cites DESIGN lines 739, 764, 497, 285, 973, 972, 1011. On disk those are `:746`, `:771`, `:502`, `:286`, `:980`, `:979`, `:1018`. The claims are true; only the numbers moved.
- Smallest fix: none needed, or re-anchor when the package is archived.

### N5 (MINOR) Cycle 3 row quotes cycle 2 without the inner quotes
- Evidence: `:1030` reads `cycle 2's "changed three to four incomplete cases"`; `:1018` reads `changed "three" to "four" incomplete cases`. The mechanical check 4 counts the `:1030` form (1 hit); the `:1018` form does not match the grep string, so the count of 1 is right only because of that quoting difference.
- Smallest fix: none needed.

### N6 (MINOR) `test_fr010_incomplete_notes_order` pairs an outage with guard case 1, which cannot hold together in a real run
- Evidence: `:746` ("outage together with guard case 1, `session_join` None"); the outage fixture sets `orca_rows` empty (`:746`, `:286`), and guard case 1 needs a scoped Dispatch row (`:502`).
- Smallest fix: say the fixture builds `SweepInput` directly with one row and `orca_available` False (a synthetic combination), or drop the outage half of the pair.

### N7 (note, not a defect) Design length
- `wc -l` gives 1030 lines; the task states 1013 at build time. Edits 4.1 to 4.5 add about 4 lines, so other fix-cycle edits landed in between. The sizing row (500 to 1500 lines, 9 agents) still holds.

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | SPEC FR-010 lists 3 incomplete-case fixtures (`merged-requirements.md:104`) | PASS |
| C2 | DESIGN names the 3 SPEC cases in the test row, FR-010 row, section 18 row and status list (`:746`, `:771`, `:1030`, `:11`) | PASS |
| C3 | Exactly 3 `origin unknown:` literals in 7.2 (`:501`), repeated identically in section 11 (`:746`) | PASS |
| C4 | Exactly 4 distinct `test_fr010_*` fixtures; row text "four fixtures" matches; names equal research/04 lines 197-200 | PASS |
| C5 | 8 h transcript age is over the 6 h window in every fixture Given (`:746`) and equals the SPEC control | PASS |
| C6 | `WORKER_LIST_PAGE` is 100 at `:548` and every use (`:299`, `:346`, `:746`) | PASS |
| C7 | `Total: 9 deviations.` equals 9 rows D1 to D9 | PASS |
| C8 | `Total: 23 open items.` equals 23 rows; cross-references to items 4, 5, 22, 23 land on the right rows | PASS |
| C9 | Em-dash count 0 (and en-dash 0); no TODO or TBD | PASS |
| C10 | `four incomplete cases` appears once, in section 18 only; four join-incomplete cases consistent at `:502`, `:771`, `:822`, `:860` | PASS |
| C11 | Mechanical file: 9 commands, 9 checks, section ranges and per-section counts match the file on disk | PASS |
| C12 | Counts adjacent to the edit (six path-B fixtures, nine byte-limit boundaries, five exemptions, 7 + 1 + 3 test files, 8 templates / 7 verbs, SPEC 653 lines, 26 FR, 15 NFR) | PASS |
| C13 | Fixture Givens are numerically coherent with the budget and guard rules (100 rows vs 50-call cap; outage with guard case 1) | FAIL (MINOR only: N1, N6) |
| C14 | The reason count in the design matches the SPEC reason count (SPEC 4, design 3) | FAIL (MINOR only: N3; the three acceptance fixtures are met) |

Fail rows C13 and C14 carry MINOR findings only, so they do not fail the gate.

## Self-audit

- Inputs read: DESIGN lines 1-36, 284-287, 340-349, 374-377, 398-403, 449-598, 695-716, 731-780, 780-870, 873-908, 968-1030; research/04 lines 170-219; SPEC line 104 and the line ranges counted above; the mechanical results file in full (137 lines).
- I did not rely on any earlier QA report in the gate folder.
- Independent counts made by tool: `wc -l` of design and SPEC, `grep -c` for em-dash, en-dash, `four incomplete cases`, D rows, open-item rows, FR and NFR rows; `grep -o` for the `origin unknown:` literals and the `test_fr010_*` names in both the design and research/04.
- Tools: Read 14, Grep 9, Bash 3, Glob 1.

Verdict: PASS

Blocking count: 0
