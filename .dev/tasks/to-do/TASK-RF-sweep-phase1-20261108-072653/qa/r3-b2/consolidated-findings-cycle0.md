# R3-B2 gate, cycle 0: consolidated findings

Inputs: the 9 reports found by Glob `qa-*-report.md` in this folder (item 3.15). Design file: `docs/designs/orchestrator-mode.md` (1026 lines at consolidation time).

Report short names: TC = qa-template-conformance (item 3.6), IC = qa-internal-consistency (3.7), EQ = qa-evidence-quality (3.8), CO = qa-completeness (3.9), AC = qa-actionability (3.10), NM = qa-numbers-metrics (3.11), CR = qa-crossref-chain (3.12), DA = qa-domain-accuracy (3.13), SF = qa-spec-fidelity (3.14).

Report verdicts (blocking counts): TC PASS 0, IC FAIL 3, EQ FAIL 1, CO PASS 0, AC FAIL 4, NM PASS 0, CR PASS 0, DA FAIL 3, SF FAIL 1. Raw total 12 BLOCKING or MAJOR findings; after dedup 9 (2 BLOCKING, 7 MAJOR).

## BLOCKING and MAJOR findings

### R3B2-F1 (BLOCKING, D9): the several-rows text bypasses the incomplete-tail guard
- Sources: DA D-1 (BLOCKING, kept). Merged duplicates: IC F1 (MAJOR), AC A2 (MAJOR), SF F1 (MAJOR), CR F2 (MINOR).
- Evidence: `docs/designs/orchestrator-mode.md:498` says a window match with `tail_complete` False does not join, then, a few sentences later, that exactly one window holding the transcript joins it; the several-rows sentences never mention `tail_complete`. `:459` says `tail_complete` is False for every file over 256 KiB. Fixture `test_path_b_incomplete_tail_has_no_session_start` (`:743`) uses one row; no R3-B2 fixture sets `tail_complete` False.
- Smallest fix: one sentence stating that the several-rows rule applies only when `tail_complete` is True; with it False no row joins and the rows and the transcript take the existing "session start not observable" and "Dispatch time window not observable" notes; add one fixture for several rows with an incomplete tail.

### R3B2-F2 (BLOCKING, D9): an open window has no upper bound and joins any later session in the pane as Orca-started
- Source: DA D-2.
- Evidence: `:498` ends the window of a `pending` or `dispatched` row with no end at `collected_start`; fixture `test_path_b_window_open_row_joins` (`:743`) pins the join as False. Owner sign-off items D9 (`:819`), SP-29 (`:857`) and open item 22 (`:994`) cover only True becoming None, not this False.
- Smallest fix: per DA, bound or qualify the open-window join (for example, state the residual risk in D9, SP-29 and open item 22 so the owner signs off on it, or add a stated bound), and make the fixture say what is signed off.

### R3B2-F3 (MAJOR): a live session spanning two Dispatches is attached to the older row, and "pane moved to a later session" is asserted when the session is earlier
- Sources: DA D-3 (MAJOR, kept). Merged duplicate: IC F5 (MINOR, the "pane moved" note is wrong when the transcript precedes the row).
- Evidence: `:498` (notes) and `:743` fixtures; `orca orchestration dispatch --to <handle>` delivers the next task into the agent already running in that terminal, so the Claude session does not change (DA report).
- Smallest fix: per DA, state that a transcript whose first record is earlier than the row's window start is a different case and gets a different note, and record the same-session-two-Dispatches limit.

### R3B2-F4 (MAJOR): "a retry" is stated as a cause of several rows, but research/04 marks retry pane reuse UNVERIFIED
- Source: EQ F1.
- Evidence: `:498` "(a reused pane, a retry, or two rows on one terminal handle)"; research/04:176 lists "whether a retry reuses its pane" as UNVERIFIED until step 1.0a; research/04:143 supports it only through the field name `retryOfDispatchId`.
- Smallest fix: `:498` "(a reused pane or two rows on one terminal handle)".

### R3B2-F5 (MAJOR): duplicate Dispatch rows against the several-rows count give two or three outcomes
- Source: IC F2.
- Evidence: `:509` merges rows that share one Dispatch id; `:498` counts "matching rows" and does not say the merge comes first; the merged row's start, end and status are undefined.
- Smallest fix: state that duplicate rows are merged first and what the merged row's window fields are.

### R3B2-F6 (MAJOR): guard case 2 (SP-16) against the new None outcomes
- Source: IC F3.
- Evidence: `:501` makes every transcript carry the SP-16 line when no transcript joined any row, a line that reads "tab map empty or stale", which is false here; the new "no window holds" and "conflict" outcomes and three fixtures assert only the pane note.
- Smallest fix: state which note wins when guard case 2 and a several-rows None outcome both apply, and adjust the fixtures.

### R3B2-F7 (MAJOR): fixtures 1 to 3 leave out `collected_start`
- Source: AC A1. Merged duplicates: IC F6 (MINOR), NM M1 (MINOR), CR F4 (MINOR, the `tail_complete` default and fixture setup are stated only under the R3-B1 fixtures).
- Evidence: `:498` ends an open row's window at `collected_start`; fixtures 1, 2 and 3 in `:743` use open rows and never state it (nor the date, `now`, window or Run id).
- Smallest fix: add "and `collected_start` 12:00" (or similar) and the other setup values to the three fixtures.

### R3B2-F8 (MAJOR): the Then of the conflict fixture cannot be asserted
- Source: AC A3.
- Evidence: `:743` `test_path_b_two_windows_hold_session_is_conflict` Then says "S not True, not idle, not Historical", which needs a class for S, a row-level Historical marker (DESIGN has none, `:465`) and S's activity time.
- Smallest fix: restate the Then in terms DESIGN defines (S's `person_started` is None and no `orca:` row carries S).

### R3B2-F9 (MAJOR): no stated precedence of the join-derived "could not determine" over rules 1 to 8
- Source: AC A4. Merged duplicate: SF F3 (MINOR, a row forced to could not determine sits outside the ordered rule table).
- Evidence: `:476-486` rule table; `:498` sets the class; the fixtures use bare rows that fall to rule 9 anyway, so an implementation that only adds the note would pass them.
- Smallest fix: state whether the join outcome overrides rules 1 to 8 or only adds a note, and add a fixture with a row that would match an earlier rule.

## MINOR findings (never fail the gate; left as notes)

| Id | Defect (sources) | Evidence |
|---|---|---|
| R3B2-F10 | The R3-B2 label is used as design prose, "follow the R3-B2 rule below", and "(m11)" is an undefined label (TC F1, EQ M3, SF F4 part, CR F6: `conflict:` is called a "note" in the new text and a "reason" at the duplicate-Dispatch bullet) | `:498`, `:509`, `:1026` |
| R3B2-F11 | Serial comma in "a reused pane, a retry, or two rows" (TC F2) | `:498` |
| R3B2-F12 | D9 Source cell omits the reviews that added R3 wording (TC F3, SF F4, CR F5) | `:819` |
| R3B2-F13 | FR-010 test column names fixtures for R3-B1 but not R3-B2 (TC F4) | `:768` |
| R3B2-F14 | Mechanical report evidence is weak: Command 5 has no captured output, grep output cut, Command 3 uses one OR pattern (TC F5, EQ M2, DA M-2, NM M3) | `phase-outputs/test-results/r3-b2-mechanical.md` |
| R3B2-F15 | Section 1 still lists R3-B2 as open (TC F6 part, CR F1) and `:743` still says "the four incomplete cases" (R3-B3 scope; TC F6 part, AC out-of-scope note) | `:7-11`, `:743` |
| R3B2-F16 | Two UNVERIFIED items from research/04 section 3.6 have no closing step in DESIGN (EQ M1) | open items `:973-995` |
| R3B2-F17 | The several-rows rule and the incomplete-tail rule are not combined in one sentence; branch coverage of the rule is thinner than the rule (a row with no observable window counted as not holding; the none-observable branch has no fixture) (CR F3, CR F4, IC F7, SF F2) | `:498`, `:743` |
| R3B2-F18 | D9, SP-29 and the Orca pane session note are stated unconditionally in `:499`, D9, SP-29 and the fixtures (IC F4, CR F3) | `:499`, `:819`, `:857` |
| R3B2-F19 | Only `first_record_ts` is cut to whole seconds, not the window bounds (IC F8, NM M2) | `:498` |
| R3B2-F20 | Path A with several rows (two rows sharing a session id) is unaddressed, and "matching rows" means scoped rows only (IC F9, SF F5) | `:498` |
| R3B2-F21 | Fixture wording and layout: no When column, fixture 5 to 7 phrasing, timestamps (AC minor notes m1 to m4 and the others in the AC "Minor findings" list, CO F1 to F3: the research "line 505" replaced by a section reference, the FR-010 insertion position, fixture 6 lacks the label) | `:743` |
| R3B2-F22 | Research counts 21 new fixtures, DESIGN has 22 because of the R3-B1 incomplete-tail fixture (NM M4) | research/09 lines 157 and 223 |
| R3B2-F23 | `ccsession:574-602` citation stops 3 lines before `orca_tab_session` closes at 605; completed rows are downgraded to could not determine when their join fails (DA M-1, DA M-3) | `:498` |
| R3B2-F24 | Report-form points: "PASS with note" cells, two DA minor notes without a fix, DA D-1 worded as a definite bypass although it is an ambiguity between two rules (TC, CO, IC, DA report notes) | the reports' `## Checks` tables |

Every finding of the nine reports is listed above under a kept id or as a named duplicate, or as part of the grouped minor rows (rows F10 to F24 name each source id).

## F_0 and |F_0|

F_0 = {R3B2-F1, R3B2-F2, R3B2-F3, R3B2-F4, R3B2-F5, R3B2-F6, R3B2-F7, R3B2-F8, R3B2-F9}

|F_0| = 9

## Cycle-0 PASS set

Every check id a report's `## Checks` table marks PASS (a result that starts with PASS, notes included), written `<report name>:C<n> (item <lens item id>)`. A FAIL-marked check is not in this set.

Count: 111 PASS checks (of 142 checks in the nine tables).

- qa-actionability-report:C1 (item 3.10)
- qa-actionability-report:C2 (item 3.10)
- qa-actionability-report:C6 (item 3.10)
- qa-actionability-report:C7 (item 3.10)
- qa-actionability-report:C8 (item 3.10)
- qa-actionability-report:C9 (item 3.10)
- qa-actionability-report:C10 (item 3.10)
- qa-actionability-report:C14 (item 3.10)
- qa-actionability-report:C15 (item 3.10)
- qa-actionability-report:C16 (item 3.10)
- qa-actionability-report:C17 (item 3.10)
- qa-completeness-report:C1 (item 3.9)
- qa-completeness-report:C2 (item 3.9)
- qa-completeness-report:C3 (item 3.9)
- qa-completeness-report:C4 (item 3.9)
- qa-completeness-report:C5 (item 3.9)
- qa-completeness-report:C6 (item 3.9)
- qa-completeness-report:C7 (item 3.9)
- qa-completeness-report:C8 (item 3.9)
- qa-completeness-report:C9 (item 3.9)
- qa-completeness-report:C10 (item 3.9)
- qa-completeness-report:C11 (item 3.9)
- qa-completeness-report:C12 (item 3.9)
- qa-completeness-report:C13 (item 3.9)
- qa-completeness-report:C14 (item 3.9)
- qa-completeness-report:C15 (item 3.9)
- qa-crossref-chain-report:C1 (item 3.12)
- qa-crossref-chain-report:C2 (item 3.12)
- qa-crossref-chain-report:C3 (item 3.12)
- qa-crossref-chain-report:C4 (item 3.12)
- qa-crossref-chain-report:C5 (item 3.12)
- qa-crossref-chain-report:C6 (item 3.12)
- qa-crossref-chain-report:C7 (item 3.12)
- qa-crossref-chain-report:C8 (item 3.12)
- qa-crossref-chain-report:C9 (item 3.12)
- qa-crossref-chain-report:C10 (item 3.12)
- qa-crossref-chain-report:C11 (item 3.12)
- qa-crossref-chain-report:C12 (item 3.12)
- qa-crossref-chain-report:C13 (item 3.12)
- qa-domain-accuracy-report:C1 (item 3.13)
- qa-domain-accuracy-report:C2 (item 3.13)
- qa-domain-accuracy-report:C3 (item 3.13)
- qa-domain-accuracy-report:C4 (item 3.13)
- qa-domain-accuracy-report:C5 (item 3.13)
- qa-domain-accuracy-report:C6 (item 3.13)
- qa-domain-accuracy-report:C7 (item 3.13)
- qa-domain-accuracy-report:C11 (item 3.13)
- qa-domain-accuracy-report:C13 (item 3.13)
- qa-evidence-quality-report:C1 (item 3.8)
- qa-evidence-quality-report:C2 (item 3.8)
- qa-evidence-quality-report:C4 (item 3.8)
- qa-evidence-quality-report:C5 (item 3.8)
- qa-evidence-quality-report:C6 (item 3.8)
- qa-evidence-quality-report:C7 (item 3.8)
- qa-evidence-quality-report:C9 (item 3.8)
- qa-evidence-quality-report:C11 (item 3.8)
- qa-evidence-quality-report:C12 (item 3.8)
- qa-evidence-quality-report:C13 (item 3.8)
- qa-evidence-quality-report:C14 (item 3.8)
- qa-evidence-quality-report:C15 (item 3.8)
- qa-internal-consistency-report:C1 (item 3.7)
- qa-internal-consistency-report:C2 (item 3.7)
- qa-internal-consistency-report:C3 (item 3.7)
- qa-internal-consistency-report:C4 (item 3.7)
- qa-internal-consistency-report:C8 (item 3.7)
- qa-internal-consistency-report:C9 (item 3.7)
- qa-internal-consistency-report:C10 (item 3.7)
- qa-internal-consistency-report:C11 (item 3.7)
- qa-internal-consistency-report:C12 (item 3.7)
- qa-internal-consistency-report:C13 (item 3.7)
- qa-internal-consistency-report:C14 (item 3.7)
- qa-numbers-metrics-report:C1 (item 3.11)
- qa-numbers-metrics-report:C2 (item 3.11)
- qa-numbers-metrics-report:C3 (item 3.11)
- qa-numbers-metrics-report:C4 (item 3.11)
- qa-numbers-metrics-report:C5 (item 3.11)
- qa-numbers-metrics-report:C6 (item 3.11)
- qa-numbers-metrics-report:C7 (item 3.11)
- qa-numbers-metrics-report:C8 (item 3.11)
- qa-numbers-metrics-report:C9 (item 3.11)
- qa-numbers-metrics-report:C10 (item 3.11)
- qa-numbers-metrics-report:C11 (item 3.11)
- qa-numbers-metrics-report:C12 (item 3.11)
- qa-numbers-metrics-report:C13 (item 3.11)
- qa-numbers-metrics-report:C14 (item 3.11)
- qa-numbers-metrics-report:C15 (item 3.11)
- qa-numbers-metrics-report:C16 (item 3.11)
- qa-numbers-metrics-report:C17 (item 3.11)
- qa-numbers-metrics-report:C18 (item 3.11)
- qa-spec-fidelity-report:C1 (item 3.14)
- qa-spec-fidelity-report:C2 (item 3.14)
- qa-spec-fidelity-report:C3 (item 3.14)
- qa-spec-fidelity-report:C4 (item 3.14)
- qa-spec-fidelity-report:C5 (item 3.14)
- qa-spec-fidelity-report:C9 (item 3.14)
- qa-spec-fidelity-report:C10 (item 3.14)
- qa-spec-fidelity-report:C11 (item 3.14)
- qa-spec-fidelity-report:C12 (item 3.14)
- qa-spec-fidelity-report:C13 (item 3.14)
- qa-template-conformance-report:C1 (item 3.6)
- qa-template-conformance-report:C2 (item 3.6)
- qa-template-conformance-report:C3 (item 3.6)
- qa-template-conformance-report:C4 (item 3.6)
- qa-template-conformance-report:C5 (item 3.6)
- qa-template-conformance-report:C8 (item 3.6)
- qa-template-conformance-report:C9 (item 3.6)
- qa-template-conformance-report:C10 (item 3.6)
- qa-template-conformance-report:C11 (item 3.6)
- qa-template-conformance-report:C12 (item 3.6)
- qa-template-conformance-report:C13 (item 3.6)
- qa-template-conformance-report:C16 (item 3.6)
