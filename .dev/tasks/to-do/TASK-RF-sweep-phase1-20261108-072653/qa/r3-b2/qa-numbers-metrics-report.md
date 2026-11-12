# QA Report - Numbers and Metrics Lens (R3-B2 gate)

**Topic:** R3-B2 design fix (several scoped Dispatch rows match one pane session), DESIGN items 3.1 to 3.4
**Date:** 2026-11-09
**Phase:** doc-qualitative (numbers lens), single instance, no `assigned_files`
**Fix cycle:** N/A (first review of this lens)
**fix_authorization:** false (only this report was written)
**Inherited Structural Verdict:** none in the spawn prompt, so standalone behaviour (no structural PASS was relied on)

Design file at review time: `docs/designs/orchestrator-mode.md`, 1026 lines (`wc -l`). Section 7.2 spans lines 449-517, the worker bullet is line 498, section 11 spans 728-752, the `test_classify.py` row is line 743, the D9 row is line 819, the SP-29 row is line 857, the FR-010 row is line 768.

## Recounts (each from the file on disk, not from the mechanical report)

| Quantity | Expected | Counted | Evidence |
|---|---|---|---|
| R3-B2 fixture names in section 11 | 7 | 7, each once, all in DESIGN:743 | Grep `test_path_b_\w+` with `-o`: `pane_reused_joins_later_row_only`, `two_windows_hold_session_is_conflict`, `shared_boundary_second_is_conflict`, `no_matching_window_holds`, `multi_row_result_ignores_row_order`, `entry_failing_window_note_order`, `rows_share_terminal_handle`. The same grep also lists 5 R3-B1 `test_path_b_*` names (not R3-B2), 12 in all. Names equal research/04 lines 158-164 and research/09 line 157 |
| Outcome sentences in 7.2 | 3 | 3, each once, all in DESIGN:498 | Grep `If exactly one matching row`, `If two or more matching rows`, `If no matching row`: one hit each |
| Outcome-to-fixture coverage | one fixture per outcome | one holds: fixture 1; two or more hold: fixtures 2 and 3; none holds: fixture 4 | DESIGN:743 |
| D9 and SP-29 insertions | 2 | 2 (D9 line 819, SP-29 line 857), one each | Grep `exactly one window holding it`: hits at 819 and 857 only. `several rows match one pane session`: 819 and 857. The FR-010 row (768) carries the separate wording `several rows matching one pane session` once |
| `Total: 9 deviations.` | 1 line, 9 rows | 1 line (821); rows D1 to D9 = 9 | Read 805-821 |
| `Total: 23 open items.` | 1 line, 23 rows | 1 line (997); rows numbered 1 to 23 in sequence, no gap or repeat | Read 965-997 |
| Em-dash count | 0 | 0 (also 0 for en dash U+2013 and horizontal bar U+2015) | Grep count of `—\|–\|―` returned no match |
| `TODO` or `TBD` (whole word) | 0 | 0 | Grep `\bTODO\b\|\bTBD\b` returned no match |
| Sizing | 4 rf-qa + 4 rf-qa-qualitative + 1 domain lens = 9 | matches research/09 Gap 5 line 182 (500-1500 lines = 4 + 4) plus "all domain lenses" | DESIGN is now 1026 lines, still in the 500-1500 row (build time figure was 1013) |

## Timestamp audit against the inclusive whole-second rule

The rule (DESIGN:498): `first_record_ts`, cut to whole seconds, must fall inside the window from `dispatch_started` to `dispatch_ended`, both ends included, or to `collected_start` when `dispatch_ended` is None and status is `pending` or `dispatched`.

| Fixture (DESIGN:743) | Times | Hand evaluation | Matches stated result |
|---|---|---|---|
| `pane_reused_joins_later_row_only` | D1 09:00-10:00 completed; D2 from 10:30 dispatched; S 10:40 | D1: 10:40 > 10:00, no. D2: 10:30 <= 10:40 <= collected_start (needs collected_start >= 10:40, not stated, see M1). One holder, S joins D2 only | Yes |
| `two_windows_hold_session_is_conflict` | D1 from 09:00 dispatched; D2 from 10:00 pending; S 10:05 | Both open-ended rows hold 10:05 (collected_start not stated, see M1). Two holders, conflict | Yes |
| `shared_boundary_second_is_conflict` | D1 09:00:00-10:00:00 completed; D2 from 10:00:00 dispatched; S 10:00:00.400 | S cut to 10:00:00. D1: 10:00:00 <= end 10:00:00, held (end included). D2: 10:00:00 >= start, held. Two holders. Without the cut, 10:00:00.400 would miss D1's end, so the cut is what makes this a conflict, as the text says | Yes |
| `no_matching_window_holds` | D1 09:00-09:30, D2 10:00-10:30 both completed; S 11:00 | Neither holds | Yes |
| `multi_row_result_ignores_row_order` | first two fixtures reversed | No new times | Yes |
| `entry_failing_window_note_order` | one row D1 ended before S's first record | No times beyond the ordering; no holder, so `pane moved to a later session` | Yes |
| `rows_share_terminal_handle` | as fixture 1, matched by tab-map line 3 | `ccsession:590` builds `session`, `folder`, `ORCA_TERMINAL_HANDLE` as three lines, so line 3 is the terminal handle (also DESIGN:32, 460) | Yes |
| R3-B1 `window_inclusive_bounds` (same cell) | D1 10:00:00-11:00:00; S 10:00:00.700, 11:00:00.400, 11:00:01.000 | Cut: 10:00:00 held, 11:00:00 held, 11:00:01 > 11:00:00 not held. Two join, third does not | Yes |
| R3-B1 `window_open_row_joins` | D1 from 10:00 open; S 10:05; collected_start 12:00 | Held | Yes |
| R3-B1 `incomplete_tail`, `terminal_row_without_end`, `row_without_start` | 10:00:00-11:00:00, S 10:30:00 tail incomplete; D1 start 10:00 no end completed, S 10:30; start None | Each expected result follows the stated rule (incomplete tail wins over a held window; terminal row without end has no window; no start has no window) | Yes |
| `test_probes_allowlist.py` reader and parser fixtures (DESIGN:742) | 07:00:01Z, 07:00:05Z, 07:00:09Z; 07:00:05Z, 07:00:01Z, 07:00:09Z; 07:00:00Z before tail and 08:00:00Z first tail record; `2026-11-08 07:00:00`; `.123Z` | first = minimum (07:00:01), last = maximum (07:00:09), tail first record 08:00:00 not 07:00:00, SQLite form read as UTC, `Z` form parsed. All stated outputs agree | Yes |

Result of the audit: no fixture time contradicts the inclusive whole-second rule. Two softer gaps are recorded as M1 and M2.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Seven R3-B2 fixture names present in section 11, each once, equal to research/04 3.4 and research/09 Gap 4 | PASS |
| C2 | Three outcome sentences in 7.2 (one holds, two or more hold, none holds), each once | PASS |
| C3 | Each outcome has a fixture in section 11 (1, 2 and 3, 4) | PASS |
| C4 | D9 insertion present exactly once with the research/04 wording | PASS |
| C5 | SP-29 insertion present exactly once with the research/04 wording | PASS |
| C6 | FR-010 row carries the several-rows rule once, and agrees in meaning with D9 and SP-29 | PASS |
| C7 | `Total: 9 deviations.` once, and D1 to D9 = 9 rows | PASS |
| C8 | `Total: 23 open items.` once, and rows 1 to 23 sequential | PASS |
| C9 | Em-dash count 0 (and en dash, horizontal bar 0) | PASS |
| C10 | No `TODO` or `TBD` | PASS |
| C11 | Every R3-B2 fixture time is consistent with the inclusive whole-second rule | PASS |
| C12 | R3-B1 fixtures sharing the cell and the `test_probes_allowlist.py` fixtures are consistent with the rule and with research/04 | PASS |
| C13 | Fixture text in DESIGN equals research/04 3.4 Given/When/Then, including every time value | PASS |
| C14 | Revision-log row (DESIGN:1026) equals research/04 edit 5 and names sections 7.2, 11, 12, 13, 14 correctly | PASS |
| C15 | Mechanical report numbers (1026 lines; 7.2 = 449-517; worker bullet 498; section 11 = 728-752; note-literal lines 498, 743, 1015, 1026; check hit counts) match the file | PASS |
| C16 | Section 11 file counts (seven new `tests/sweep` files counting `conftest.py`, one new command test, three edited test files) agree with the table rows | PASS |
| C17 | Sizing 9 agents (4 + 4 + 1) matches research/09 Gap 5 for a design in the 500-1500 line row | PASS |
| C18 | Fixtures are deterministic from their own text (every open-ended row has a stated `collected_start`) | PASS with MINOR M1 (not stated for the R3-B2 fixtures) |

Checks passed: 18 / 18 (C18 carries a MINOR note). Failed: 0.

## Findings

No BLOCKING and no MAJOR finding. Four MINOR notes (never fail the gate).

| ID | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| M1 | MINOR | `docs/designs/orchestrator-mode.md:743`, R3-B2 fixtures 1, 2, 3 and 7, against the window rule at `:498` | Rows with no end time (`dispatched` or `pending`) have a window that ends at `collected_start`. The R3-B2 fixtures use such rows (D2 in fixtures 1, 3 and 7; D1 and D2 in fixture 2) but never state `collected_start`. The result "D2 holds S" is true only when `collected_start` is at or after S's time (10:40, 10:05, 10:00:00). The R3-B1 fixture `test_path_b_window_open_row_joins` in the same cell does state `collected_start` 12:00. research/04 3.4 has the same omission, so the producer copied it faithfully | In the lead-in "all under path B and all with aware UTC times" add "and `collected_start` 12:00". One clause, no other change |
| M2 | MINOR | `:498` ("`first_record_ts`, cut to whole seconds ... from `dispatch_started` to `dispatch_ended`") and `:742` (`dispatchedAt: "2026-11-08T07:00:00.123Z"`) | Only `first_record_ts` is cut to whole seconds. The window bounds are not said to be cut. The SQLite form is whole-second, but the ISO form the parser also accepts can carry a fraction. With `dispatch_started` 07:00:00.123, a first record at 07:00:00.500 (really inside) is cut to 07:00:00 and falls outside. No fixture uses a fractional bound for a join, and the failure direction is safe (could not determine, never True), so no stated result is wrong | Add "the bounds are compared as parsed; a fractional bound is not cut" or "cut both ends" to the sentence at `:498`. Optional |
| M3 | MINOR | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-b2-mechanical.md:80-84` and `:68-72`, `:110` | Command 5 (TODO or TBD) records "(no output expected ...)" and not a captured result, so the PASS on Check 5 rests on an expectation. Command 3 uses an OR pattern (`exactly one window holding it\|several rows matching one pane session`), so "1 1 1" cannot show that D9 and SP-29 carry the exact phrase and FR-010 the other. The claims are true (confirmed here: 768 has only the FR-010 wording, 819 and 857 have both D9/SP-29 phrases), so no result changes | Record real grep output for Command 5, and grep the two phrases separately in Command 3. Mechanical file only |
| M4 | MINOR | `research/09-gap-fill.md:157-160` and `:223` against `docs/designs/orchestrator-mode.md:743` | research/09 Gap 4 counts 4 R3-B1 path-B window fixtures in `test_classify.py` and 21 new fixtures in all. DESIGN now has 5 (it adds `test_path_b_incomplete_tail_has_no_session_start` from the r3-b1 fix cycle, absent from research/04). The R3-B2 count of 7 is unaffected. Informational for the R3-B1 gate and later task items | None needed for R3-B2. If a later item quotes "21", correct it to 22 |

Not findings, checked and clean: the three-outcome wording is not order dependent; `Several matching rows follow the R3-B2 rule below` (`:498`) points forward within the same bullet and the rule does follow; the m11 sentence points to "the bullet that follows this one", which is the line 499 `Orca pane session, not in scoped Runs` bullet.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was supplied, so no rf-qa PASS was relied on. The producer's mechanical report (`r3-b2-mechanical.md`) was treated as a claim to test, not as evidence.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Fixture time evaluation against the rule: each R3-B2 fixture and five R3-B1 fixtures were hand evaluated against `DESIGN:498` (rows C11, C12; table above). Verified by Read of DESIGN 449-517 and the full `:743` cell, plus Grep of every `hh:mm:ss(.f)` literal in the file (only lines 742 and 743 hold them).
- Phrase-level separation of the D9, SP-29 and FR-010 insertions: Grep `-o -n` for each phrase showed 768 / 819 / 857 carry different phrases, which the mechanical OR-grep could not show (M3).
- Tab-map "line 3" claim in fixture 7: read `src/superclaude/skills/ccsession-tag/ccsession:590`, which builds the file as session id, folder, terminal handle, so line 3 is the terminal handle.
- Row recounts: read the D1-D9 table and the 1-23 open-items table row by row rather than trusting the `Total:` lines.
- Line-number claims in the mechanical file (1026 lines, 449-517, 498, 728-752) re-derived from `wc -l`, the section map reads and the 7.3 heading at 518.

**Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 12 | Grep: 15 | Glob: 1 | Bash: 1 (Read + Grep + Glob = 28, at least the 18 checks)
**Web research:** none performed (no external claim in this lens), so no Tavily or fallback call.
**Unchecked items:** none. **Unverifiable items:** none.

Self-check: a "0 BLOCKING" result is credible here because every count was taken from the file with a command whose output is quoted above, and the review still produced four notes (M1 to M4) from the same evidence.

Verdict: PASS
Blocking count: 0
