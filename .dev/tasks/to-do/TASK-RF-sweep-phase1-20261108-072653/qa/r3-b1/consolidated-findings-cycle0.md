# R3-B1 gate, cycle 0: consolidated findings

Inputs: the 9 reports found by Glob `qa-*-report.md` in this folder (item 2.17). Design file: `docs/designs/orchestrator-mode.md` (1023 lines at consolidation time).

Report short names used below: TC = qa-template-conformance (item 2.8), IC = qa-internal-consistency (2.9), EQ = qa-evidence-quality (2.10), CO = qa-completeness (2.11), AC = qa-actionability (2.12), NM = qa-numbers-metrics (2.13), CR = qa-crossref-chain (2.14), DA = qa-domain-accuracy (2.15), SF = qa-spec-fidelity (2.16).

Report verdicts: TC PASS 0, IC PASS 0, EQ FAIL 2, CO FAIL 1, AC FAIL 2, NM FAIL 1, CR PASS 0, DA FAIL 1, SF PASS 0 (blocking counts). Raw total 7 BLOCKING or MAJOR findings, all MAJOR, after dedup also 7.

Scope note carried: the R3-B2 several-rows rule, the forward reference "Several matching rows follow the R3-B2 rule below." and the transcript outcome for a path-B match that does not join belong to item 3.1 and are not R3-B1 findings (line 741 "that later transcript is None" is the same item, recorded as R3B1-F21).

## BLOCKING and MAJOR findings

### R3B1-F1 (MAJOR): the `completedAt` shape claim at 15.1 item 4 is unsupported and contradicted
- Source: EQ F1. Merged duplicate: DA D-5 (MINOR, same line and same defect).
- Evidence: `docs/designs/orchestrator-mode.md:887` says the three Dispatch fields are present "with the shapes the static bundle read gives (SQLite `YYYY-MM-DD HH:MM:SS` UTC)". research/04:51 supports that shape only for `dispatched_at`; research/04:53 says the `completed_at` write was not found; the bundle writes `completed_at` with `new Date().toISOString()` at 12 lifecycle sites.
- Smallest fix: line 887 states the SQLite form for `dispatchedAt` only; `completedAt` form is UNVERIFIED (both forms possible, 7.2 accepts both); `status` is one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`.

### R3B1-F2 (MAJOR): the UNVERIFIED marker was dropped where the Dispatch field names are stated as confirmed
- Source: EQ F2. Merged duplicate: IC IC-6 (MINOR, lines 455 and 496).
- Evidence: `docs/designs/orchestrator-mode.md:455` ("confirmed by step 1.0a item 4, open item 23"), `:496` ("are confirmed by step 1.0a item 4") and `:993` (open item 23 has no UNVERIFIED label). research/04:128 requires the live names to stay UNVERIFIED until step 1.0a runs.
- Smallest fix: 455 "UNVERIFIED until step 1.0a item 4 (open item 23)"; 496 "are UNVERIFIED until step 1.0a item 4 confirms them (open item 23)"; 993 starts with "UNVERIFIED:".

### R3B1-F3 (MAJOR): fixture `test_path_b_window_open_row_joins` drops its path-B join setup
- Source: CO F1. Merged duplicates: SF F-1 (MINOR), NM m2 (MINOR, over-states the second fixture: research/04:115 has no such setup, so only the first fixture is affected).
- Evidence: `docs/designs/orchestrator-mode.md:741` against `research/04-design-fixes-r3.md:114`. The Given omits `session_join` pane P and the tab-map entry from P to session S, so "S joins D1" has no cause.
- Smallest fix: after "row D1" insert "with `session_join` pane P"; before "transcript S" insert "a tab-map entry from P to session S;".

### R3B1-F4 (MAJOR): the time parser and the `worker-show` parser have no name, module or signature
- Source: AC A1. Merged duplicates: TC m3, IC IC-5, CR M1, SF F-3, CO F2 (all MINOR; the same gap seen from the fixtures at 740 and the 7.1 signatures).
- Evidence: `docs/designs/orchestrator-mode.md:353-446` (7.1) has `collect` (390) and `read_transcript_tail` (398) but no time parser and no `worker-show` parser; the time rule at `:468` is owned by no module; the `probes.py` may-import row (about `:211`) omits `datetime`; the six fixtures at `:740` test "the `worker-show` parser".
- Smallest fix: add two signatures under `probes.py` in 7.1 (a never-raising `parse_time` and a `parse_worker_show` that builds `OrcaObservation`), state that `read_transcript_tail` and `collect` share `parse_time`, add `datetime` to the `probes.py` may-import row, and name the functions in the fixture cell at 740.

### R3B1-F5 (MAJOR): the timezone of `now`, `collected_start`, `collected_end` and `mtime` is not stated
- Source: AC A2. Merged duplicates: IC IC-2 (MINOR), DA D-4 (MINOR).
- Evidence: `docs/designs/orchestrator-mode.md:468` makes only parsed Orca and transcript times aware UTC; `:231` says `now (UTC, read once)`; `:454` gives `collected_start` and `collected_end` no type; `:457` gives `mtime: datetime` no zone; `:496` compares aware `first_record_ts` with `collected_start` (a naive value raises `TypeError` in Python 3.10).
- Smallest fix: extend the `:468` paragraph: `now`, `collected_start`, `collected_end` and `TranscriptTail.mtime` are aware UTC `datetime` values; `collected_start` is read once at the top of `collect`, before the first Orca call; the 741 fixtures say their times are UTC.

### R3B1-F6 (MAJOR): a truncated transcript tail cannot be told from a complete one, so `first_record_ts` can wrongly prove or disprove session start
- Source: DA D-1.
- Evidence: `docs/designs/orchestrator-mode.md:457` says "for a file over 256 KiB this is not the session start" but `TranscriptTail` has no truncation field; `:496` uses `first_record_ts` as the only session-identity test and, when it fails, states the fact `pane moved to a later session`. A worker transcript over 256 KiB is the normal case.
- Smallest fix: add `tail_complete: bool` (False when the first partial line was dropped) to the `TranscriptTail` row (457) and to the GQ-103(3) list (60); at 496 say that for `tail_complete` False the session start is not observable, the path-B match does not join, and the row and the transcript carry a distinct note; add one classify fixture for it (and keep section 11 and the revision log in step).

### R3B1-F7 (MAJOR): section 11 says "edits to four existing test files" but lists three
- Source: NM F1 (the defect predates R3-B1; the numbers lens reported it as a count that no longer matches its list).
- Evidence: `docs/designs/orchestrator-mode.md:728` against lines 746-747 and 696-700: `test_worker_contract.py`, `test_how_we_work_routing_table.py` and `test_routing_refresh.py` are edited; `test_routing_plugin_parity.py` is "unchanged, must pass".
- Smallest fix: line 728 "edits to three existing test files (`tests/commands/test_routing_plugin_parity.py` must also still pass, unchanged)".

## MINOR findings (never fail the gate; left as notes)

| Id | Defect (merged sources) | Evidence |
|---|---|---|
| R3B1-F8 | Section 1 still says the model "lacks" three time fields (there are four now); correct until the gate closes (IC IC-1, CR N1) | `docs/designs/orchestrator-mode.md:9` |
| R3B1-F9 | No rule for a path-B candidate whose `first_record_ts` is None (AC M3, IC IC-3, CR M5) | `:468`, `:496`, `:511` |
| R3B1-F10 | Whole-second cut applies to `first_record_ts` only; "compared as UTC instants" conflicts with it; the `iso_z` fixture has no expected value (AC M1, DA D-2, SF F-4) | `:496`, `:740` |
| R3B1-F11 | Section 11 wording looser than the rule ("earliest timestamp", "no observable start time"); section 12 FR-010 row traces the six parser fixtures but not the four window fixtures (IC IC-4, CR M2, CR M3) | `:741`, `:766` |
| R3B1-F12 | The Fix cycle 3 R3-B1 row omits the section 12 change, the m2 wording fix and the m5 note (TC m2, CR M4) | `:1023` |
| R3B1-F13 | The Fix cycle 3 intro lacks the review-file path and minor-notes sentence of the cycle 2 intro (TC m1) | `:1019`, `:1009` |
| R3B1-F14 | One sentence is long and nested (TC m4) | `:468` |
| R3B1-F15 | Section 11 cells now name test functions; earlier cells never did (TC m5; the names are required by research/09 Gap 4 and the later gates, so keep them) | `:740`, `:741` |
| R3B1-F16 | The mechanical log records "(exit 0)" for a grep that exits 1; recorded grep lines are cut to about 100 characters (TC m6; also the T11 notes) | `phase-outputs/test-results/r3-b1-mechanical.md:88` |
| R3B1-F17 | Three research/04 section 2.5 premises are not carried as UNVERIFIED in open item 23: where `completedAt` is written, `dispatchedAt` precedes the first transcript record, host clocks agree (EQ F3) | `:993`, `:887` |
| R3B1-F18 | The mechanical gate cannot catch F1 or F2 (EQ F4) | `phase-outputs/test-results/r3-b1-mechanical.md` |
| R3B1-F19 | Fixture realism: a terminal row without an end, and SQLite-form ends where real ends are ISO with milliseconds (EQ F5) | `:741` |
| R3B1-F20 | Accepted time forms wider than Python 3.10 `fromisoformat`; DESIGN:33 overstates the transcript record shape and does not say records without `timestamp` are skipped; 256 KiB edge cases; `last_record_ts` and `session_id` undefined; naive `T` form; `dispatch.createdAt` fallback dropped (DA D-3, DA D-6, AC M4 to M7) | `:468`, `:33`, `:457`, `:398` |
| R3B1-F21 | Line 741 still says the later transcript is None for the moved-pane case, and open item 23 says "its transcript is None"; item 3.1 closes both (CO F3, AC M8, CR deferred, IC out-of-scope note) | `:741`, `:993` |
| R3B1-F22 | The time-parsing rule says "every Orca and transcript time" and so reaches the `agentWait` timestamp; row-level "could not determine" is not tied to `classify.RULES` (SF F-2, SF F-5) | `:468`, `:496` |
| R3B1-F23 | Section 8 line anchors into `WORKER-CONTRACT.md` and `test_worker_contract.py` are stale (NM m1; moved line numbers on true quoted names) | `:665`, `:679` to `:688` |
| R3B1-F24 | Check marks inconsistent with minor notes in some reports ("PASS with notes", PASS next to an own minor note) (TC, CO, IC, EQ, DA report-form notes) | report `## Checks` tables |

## F_0 and |F_0|

F_0 = {R3B1-F1, R3B1-F2, R3B1-F3, R3B1-F4, R3B1-F5, R3B1-F6, R3B1-F7}

|F_0| = 7

## Cycle-0 PASS set

Every check id a report's `## Checks` table marks PASS (a result that starts with PASS, notes included), written `<report name>:C<n> (item <lens item id>)`. A FAIL-marked check is not in this set.

Count: 129 PASS checks (of 155 checks in the nine tables).

- qa-actionability-report:C1 (item 2.12)
- qa-actionability-report:C3 (item 2.12)
- qa-actionability-report:C4 (item 2.12)
- qa-actionability-report:C5 (item 2.12)
- qa-actionability-report:C6 (item 2.12)
- qa-actionability-report:C7 (item 2.12)
- qa-actionability-report:C9 (item 2.12)
- qa-actionability-report:C10 (item 2.12)
- qa-actionability-report:C11 (item 2.12)
- qa-actionability-report:C12 (item 2.12)
- qa-actionability-report:C13 (item 2.12)
- qa-actionability-report:C14 (item 2.12)
- qa-completeness-report:C1 (item 2.11)
- qa-completeness-report:C2 (item 2.11)
- qa-completeness-report:C3 (item 2.11)
- qa-completeness-report:C4 (item 2.11)
- qa-completeness-report:C5 (item 2.11)
- qa-completeness-report:C6 (item 2.11)
- qa-completeness-report:C7 (item 2.11)
- qa-completeness-report:C8 (item 2.11)
- qa-completeness-report:C9 (item 2.11)
- qa-completeness-report:C10 (item 2.11)
- qa-completeness-report:C11 (item 2.11)
- qa-completeness-report:C12 (item 2.11)
- qa-completeness-report:C13 (item 2.11)
- qa-completeness-report:C14 (item 2.11)
- qa-completeness-report:C15 (item 2.11)
- qa-completeness-report:C17 (item 2.11)
- qa-completeness-report:C18 (item 2.11)
- qa-completeness-report:C19 (item 2.11)
- qa-completeness-report:C20 (item 2.11)
- qa-completeness-report:C21 (item 2.11)
- qa-completeness-report:C22 (item 2.11)
- qa-crossref-chain-report:C1 (item 2.14)
- qa-crossref-chain-report:C2 (item 2.14)
- qa-crossref-chain-report:C3 (item 2.14)
- qa-crossref-chain-report:C4 (item 2.14)
- qa-crossref-chain-report:C5 (item 2.14)
- qa-crossref-chain-report:C6 (item 2.14)
- qa-crossref-chain-report:C7 (item 2.14)
- qa-crossref-chain-report:C8 (item 2.14)
- qa-crossref-chain-report:C9 (item 2.14)
- qa-crossref-chain-report:C11 (item 2.14)
- qa-crossref-chain-report:C12 (item 2.14)
- qa-crossref-chain-report:C13 (item 2.14)
- qa-crossref-chain-report:C14 (item 2.14)
- qa-crossref-chain-report:C16 (item 2.14)
- qa-crossref-chain-report:C20 (item 2.14)
- qa-crossref-chain-report:C21 (item 2.14)
- qa-crossref-chain-report:C22 (item 2.14)
- qa-crossref-chain-report:C23 (item 2.14)
- qa-domain-accuracy-report:C1 (item 2.15)
- qa-domain-accuracy-report:C2 (item 2.15)
- qa-domain-accuracy-report:C3 (item 2.15)
- qa-domain-accuracy-report:C7 (item 2.15)
- qa-domain-accuracy-report:C8 (item 2.15)
- qa-domain-accuracy-report:C9 (item 2.15)
- qa-domain-accuracy-report:C12 (item 2.15)
- qa-domain-accuracy-report:C14 (item 2.15)
- qa-domain-accuracy-report:C15 (item 2.15)
- qa-domain-accuracy-report:C16 (item 2.15)
- qa-evidence-quality-report:C1 (item 2.10)
- qa-evidence-quality-report:C2 (item 2.10)
- qa-evidence-quality-report:C3 (item 2.10)
- qa-evidence-quality-report:C4 (item 2.10)
- qa-evidence-quality-report:C6 (item 2.10)
- qa-evidence-quality-report:C10 (item 2.10)
- qa-evidence-quality-report:C12 (item 2.10)
- qa-evidence-quality-report:C13 (item 2.10)
- qa-evidence-quality-report:C14 (item 2.10)
- qa-internal-consistency-report:C1 (item 2.9)
- qa-internal-consistency-report:C2 (item 2.9)
- qa-internal-consistency-report:C3 (item 2.9)
- qa-internal-consistency-report:C4 (item 2.9)
- qa-internal-consistency-report:C5 (item 2.9)
- qa-internal-consistency-report:C6 (item 2.9)
- qa-internal-consistency-report:C7 (item 2.9)
- qa-internal-consistency-report:C8 (item 2.9)
- qa-internal-consistency-report:C9 (item 2.9)
- qa-internal-consistency-report:C10 (item 2.9)
- qa-internal-consistency-report:C11 (item 2.9)
- qa-internal-consistency-report:C12 (item 2.9)
- qa-internal-consistency-report:C13 (item 2.9)
- qa-internal-consistency-report:C14 (item 2.9)
- qa-internal-consistency-report:C15 (item 2.9)
- qa-internal-consistency-report:C16 (item 2.9)
- qa-numbers-metrics-report:C1 (item 2.13)
- qa-numbers-metrics-report:C2 (item 2.13)
- qa-numbers-metrics-report:C3 (item 2.13)
- qa-numbers-metrics-report:C4 (item 2.13)
- qa-numbers-metrics-report:C5 (item 2.13)
- qa-numbers-metrics-report:C6 (item 2.13)
- qa-numbers-metrics-report:C7 (item 2.13)
- qa-numbers-metrics-report:C8 (item 2.13)
- qa-numbers-metrics-report:C9 (item 2.13)
- qa-numbers-metrics-report:C10 (item 2.13)
- qa-numbers-metrics-report:C11 (item 2.13)
- qa-numbers-metrics-report:C12 (item 2.13)
- qa-numbers-metrics-report:C13 (item 2.13)
- qa-numbers-metrics-report:C14 (item 2.13)
- qa-numbers-metrics-report:C16 (item 2.13)
- qa-numbers-metrics-report:C18 (item 2.13)
- qa-spec-fidelity-report:C1 (item 2.16)
- qa-spec-fidelity-report:C2 (item 2.16)
- qa-spec-fidelity-report:C3 (item 2.16)
- qa-spec-fidelity-report:C4 (item 2.16)
- qa-spec-fidelity-report:C5 (item 2.16)
- qa-spec-fidelity-report:C6 (item 2.16)
- qa-spec-fidelity-report:C7 (item 2.16)
- qa-spec-fidelity-report:C9 (item 2.16)
- qa-spec-fidelity-report:C10 (item 2.16)
- qa-spec-fidelity-report:C11 (item 2.16)
- qa-spec-fidelity-report:C12 (item 2.16)
- qa-spec-fidelity-report:C13 (item 2.16)
- qa-spec-fidelity-report:C14 (item 2.16)
- qa-template-conformance-report:C1 (item 2.8)
- qa-template-conformance-report:C2 (item 2.8)
- qa-template-conformance-report:C3 (item 2.8)
- qa-template-conformance-report:C4 (item 2.8)
- qa-template-conformance-report:C5 (item 2.8)
- qa-template-conformance-report:C6 (item 2.8)
- qa-template-conformance-report:C7 (item 2.8)
- qa-template-conformance-report:C8 (item 2.8)
- qa-template-conformance-report:C9 (item 2.8)
- qa-template-conformance-report:C10 (item 2.8)
- qa-template-conformance-report:C11 (item 2.8)
- qa-template-conformance-report:C12 (item 2.8)
- qa-template-conformance-report:C13 (item 2.8)
- qa-template-conformance-report:C14 (item 2.8)
