# QA Report: Actionability lens (R3-B3, items 4.1 to 4.5)

**Topic:** orchestrator-mode DESIGN, list-incomplete rule and the three SPEC FR-010 fixtures
**Date:** 2026-11-09
**Phase:** doc-qualitative, actionability lens (domain lens, research/09 Gap 5)
**Fix cycle:** N/A (fix_authorization: false; only this report was written)
**Design read:** `docs/designs/orchestrator-mode.md`, 1031 lines on disk now (the sizing note says 1013 at build time; the 500-1500 row still holds)

Stance: I am the developer who must write (a) the list-incomplete branch of `classify_all`, (b) the `collect` code that names the per-Run source row, (c) the four fixtures. Every point where I have to guess is a finding.

## What I read (all in chunks of at most 150 lines)

- DESIGN: 1-36, 218-223, 236-351, 353-452, 449-523, 519-618, 616-647, 731-772, 772-802, 846-852, 889-892, 970-1031.
- research/04 section 4: lines 170-219.
- SPEC `merged-requirements.md`: lines 98-113 (FR-005 to FR-019) and 318-323 (worker-list paging).
- `r3-b3-mechanical.md`: 1-136. I re-ran its literal greps against the design rather than trusting it.

## What is already actionable (so the findings below are not padded)

- The row name is stated exactly: `orca worker-list <run>` (DESIGN:595), and test 3 uses the instance `orca worker-list R2` (DESIGN:746).
- The three note literals match in DESIGN:501, DESIGN:746 and research/04 4.2 item 2, and they follow SPEC FR-010 (SPEC:104).
- `orca_available` and `truncated` are named `SweepInput` fields (DESIGN:456) and drive two of the three notes without doubt.
- The order inside the three-note family (unavailable, truncated, call failed) is stated (DESIGN:501) and pinned by test 4 (DESIGN:746).
- "Never idle or Historical" is stated for None (DESIGN:501; SPEC:104).
- The four research edits (4.2 items 1 to 4) are present at DESIGN:746, 501, 771 and 1030.

## Findings

### A-1 (MAJOR): the input that drives the `call failed` note is a proxy that also holds for an outage, so test 1 has two valid outputs

- Evidence: DESIGN:501 keys the note on "its `sources` row `orca worker-list <run>` has `unscanned` set". DESIGN:250-251 and DESIGN:749 (FR-019, also DESIGN:850) say that after an unavailable result every unscanned Orca source is marked `unscanned: orca unavailable`. DESIGN:287 makes a budget cut `call_failed` too, so a `unscanned: time budget reached` row also carries `unscanned`. `SweepInput` has no per-call kind (DESIGN:456), so `classify_all` cannot read `call_failed` itself.
- What is wrong: a faithful `collect` for the outage fixture (DESIGN:746 test 1, `--run R1`, first call unavailable, DESIGN:286) leaves `orca worker-list R1` with `unscanned` set. Read literally, DESIGN:501 then adds `origin unknown: worker list call failed` after `origin unknown: Orca unavailable`. Test 1 asserts the unavailable note and does not say whether `sources` holds that row or whether the call-failed note must be absent. I cannot tell which is right. The same row also blurs "call failed" with "never called because Orca went away".
- Smallest fix: in DESIGN:501 say the call-failed note fires for a `sources` row named `orca worker-list <run>` whose `unscanned` is non-null and is not `orca unavailable` (a budget cut counts, per DESIGN:287). In test 1 say `sources` holds `orca worker-list R1` with `unscanned` `orca unavailable` and that T carries exactly one `origin unknown:` note.

### A-2 (MAJOR): the shared Given says "the join guard otherwise holds", but tests 2 and 3 trip guard case 2, so the expected notes cannot be right as written

- Evidence: DESIGN:746 shared Given: T "joined to no Orca row, and the join guard otherwise holding (path A, `session_join` present on every scoped row)". Test 2 has 100 rows in R1 and "none joined to T"; test 3 has R1 `worker-list` ok. DESIGN:502, second case: the guard fails when "Orca returned at least one worker row and no transcript joined any Orca row (SPEC line 236, SP-16)". The only transcript the Givens name is T. The SPEC control (SPEC:104) uses two transcripts, one mapped to an Orca row, which is what keeps case 2 false.
- What is wrong: with T alone, case 2 holds in tests 2 and 3. DESIGN:502 then adds the SP-16 literal to T's notes and prints `could not join Orca workers to transcripts (tab map empty or stale)`. The Then columns list only the `origin unknown:` note. Whether the test asserts exact notes or membership is not said. In addition, DESIGN:746 claims "the first three each differ from the complete-negative-join control by one input". Test 1 changes two inputs (it sets `orca_available` False and empties `orca_rows`, which also removes the control's join), so the claim cannot be met, and the control has no test name to diff against.
- Smallest fix: add to the shared Given a second transcript T2, readable and in window, joined by path A to one scoped row (as in the control), so case 2 is false; name the control fixture; and state "T's notes equal exactly [the `origin unknown:` note]". For test 1, either drop the "one input" claim or say the control's row and join are removed together with the flag.

### A-3 (MAJOR): `test_fr010_incomplete_notes_order` cannot be built from the Givens, and its expected list drops a note the design says will be there

- Evidence: DESIGN:746 test 4: "outage together with guard case 1, `session_join` None". DESIGN:502 case 1 needs "`session_join` is None on any scoped Dispatch row", so at least one scoped row must exist. Test 1's outage shape has `orca_rows` empty. DESIGN:502 last sentences: when cases 1 and 2 hold together the SP-16 literal comes first, then `tab map join not observable`. DESIGN:501 puts `origin unknown:` notes before any join-guard note.
- What is wrong: (1) The outage-plus-row input is never described. It needs a partial outage (a successful `worker-list` kept, a later call unavailable; DESIGN:286, FR-019 test 3), and I have to invent it. (2) With a row present and no transcript joined, case 2 also holds, so by DESIGN:501 and DESIGN:502 the order is: `origin unknown: Orca unavailable`, the SP-16 literal, `tab map join not observable`. Test 4's Then lists only the first and the last. (3) "in that order when several hold" (DESIGN:501) can mean attach all or attach the first; only test 4 settles it, and only for two of the three families.
- Smallest fix: write test 4's Given as a partial outage (R1 `worker-list` ok with one row whose `session_join` is None, then `orca_available` False, T unjoined), and set the Then to the exact three-note list above, or add T2 as in A-2 so case 2 is false and the list is two notes. Add "all notes that hold are attached, in this order" to DESIGN:501.

### A-4 (MAJOR): the "synthetic full page" cannot be built: the fixture is a pure `classify_all` input but is described with a field only `collect` could read, and the truncation trigger disagrees

- Evidence: DESIGN:746 test 2: "exactly `WORKER_LIST_PAGE` (100) rows and `truncated` True from a synthetic page whose `page.nextCursor` is non-null". The test lives in `tests/sweep/test_classify.py`, which takes a `SweepInput` (DESIGN:420, DESIGN:456) and is AST-checked to import no `subprocess`, `click`, `os` or `shutil` (DESIGN:746). `SweepInput` has no page or cursor field. The trigger is count-based everywhere else: DESIGN:548 ("a full page sets truncated"), DESIGN:980 (open item 5: "no cursor template"), SPEC:320-321 ("a 100-row fixture sets `truncated`"). The cursor field name is UNVERIFIED (research/04 4.5; DESIGN:891 capture item 3).
- What is wrong: (a) I do not know if the fixture is a hand-built `SweepInput` (then `nextCursor` is meaningless and 100 rows are not needed) or a `collect` run over a fake `_orca` (then it belongs in `test_probes_allowlist.py`, and the page shape is unverified). (b) If `collect` reads `page.nextCursor`, it contradicts the count rule; if it does not, the Given misleads. (c) The 100 rows have no specified field values: Dispatch ids must be distinct or they merge into one row (DESIGN:510), `session_join` values must be distinct and differ from T's session id, and rows past the 50th have None Dispatch times (DESIGN:457), which changes `summary.bound_reached`. Nothing says what those rows are.
- Smallest fix: state test 2's Given as a hand-built `SweepInput`: 100 `OrcaObservation` rows `D001` to `D100` in Run R1, `session_join` `S001` to `S100` (none equal to T's session id), a fixed status such as `completed`, `truncated` True, `orca_available` True; delete `page.nextCursor` from the Given. Put the page-to-flag rule in a `collect` test (see A-5): a 100-row synthetic body sets `truncated`, a 99-row body does not.

### A-5 (MAJOR): nothing tests that `collect` produces the row name and flags that the `classify_all` branch matches on

- Evidence: `grep` for `orca worker-list` finds the name only at DESIGN:501 (rule), 595 (naming), 746 (a hand-built `sources` input to `classify_all`) and 1030 (log). `test_probes_allowlist.py` (DESIGN:745) lists no non-first `worker-list` `call_failed` and no 100-row page. FR-019 maps to `test_cli_contract.py` (DESIGN:780), which checks only the printed `unscanned: orca unavailable` (DESIGN:749). FR-026 maps to `test_probes_allowlist.py` (DESIGN:787) for result kinds only.
- What is wrong: the string name plus a non-null `unscanned` is the only channel from `collect` to `classify_all`. All four new fixtures write `sources` by hand, so a `collect` that names the row `orca-ide worker-list R2` (DESIGN:524 and DESIGN:606 make the resolved binary `orca-ide` prominent; DESIGN:595 says literal `orca`) or `orca worker-list  R2` passes every test, and in production an unproved transcript becomes True or Historical. That is the SPEC FR-010 defect the item was meant to close, and it fails open. I also cannot tell if the `orca` prefix is the literal word or `orca_binary()`.
- Smallest fix: add one case to `test_probes_allowlist.py`: `collect` over a fake `_orca` with R1 `worker-list` ok and R2 `call_failed` (second call) gives `sources` names exactly `orca worker-list R1` and `orca worker-list R2`, R2 `unscanned` non-null, R1 `unscanned` None; and one with a 100-row body giving `truncated` True. State in DESIGN:595 that the prefix is the literal `orca`, and define the name once as a shared constant in `models.py` (for example `WORKER_LIST_SOURCE = "orca worker-list "`), used by both `collect` and `classify_all`.

### A-6 (MINOR): note precedence for a transcript that has a tab-map entry is not given

- Evidence: DESIGN:499 gives such a transcript `Orca pane session, not in scoped Runs`; DESIGN:498 gives pane, window and tail notes instead of it; DESIGN:501 says "every unjoined transcript" gets the `origin unknown:` note "before any join-guard note"; DESIGN:502 suppresses the SP-16 line when every affected transcript "carries its pane or tail note only".
- What is wrong: under a truncated list, `Orca pane session, not in scoped Runs` is a claim the sweep cannot make, and the design does not say if it is added, replaced or dropped, nor whether `origin unknown:` counts as a "pane or tail note" for the SP-16 line. No fixture covers an entry-bearing transcript under an incomplete list.
- Smallest fix: one sentence in DESIGN:501: under an incomplete list the `Orca pane session, not in scoped Runs` and `earlier pane session not joinable` notes are not added, the pane and tail notes of DESIGN:498 follow the `origin unknown:` notes, and an `origin unknown:` note does not count as a pane or tail note for the SP-16 line.

### A-7 (MINOR): SPEC FR-010 also names "tab map unreadable" as a reason; the design has no input, note or fixture for it

- Evidence: SPEC:104 ("Orca unavailable, worker list truncated, worker list call failed or tab map unreadable"). No match for an unreadable-tab-map condition anywhere in the design; `read_tab_map` returns a bare tuple (DESIGN:401); research/04 4.2 and DESIGN:501 pick three reasons.
- What is wrong: the SPEC says "such as", so a fourth note is not required, but a developer writing the branch sees four reasons in the SPEC and three in the design with no statement of what happens to an unreadable tab map.
- Smallest fix: one line in DESIGN:501 or section 13 saying an unreadable tab map is carried by the tab-map `SourceCoverage` row and the guard, and has no `origin unknown:` note in Phase 1.

### A-8 (MINOR): the stored form of `unscanned` and the row's other fields are inconsistent or unstated

- Evidence: `OrcaResult.reason` example is `unscanned: time budget reached (90 s)` with the prefix (DESIGN:378); the `SourceCoverage.unscanned` value in DESIGN:595 and DESIGN:746 is `orca call failed (exit 1)` without it; FR-019 prints `unscanned: orca unavailable` (DESIGN:749, 850). `OrcaResult` has no exit-code field, so `(exit 1)` has no stated source. The `coverage` value for an ok, truncated or failed `worker-list` row is not given, and no name is given for the sibling Orca rows (`task-list`, `worker-show`, `worktree ps`) that FR-019 says must print `unscanned: orca unavailable`.
- Smallest fix: say that `SourceCoverage.unscanned` holds the text after `unscanned: `, that the renderer adds the prefix, that `_orca` writes `orca call failed (exit <n>)`, and list the `coverage` strings and the sibling row names in one sentence in DESIGN:595.

### A-9 (MINOR): unspecified fixture fields and a hard-to-use test cell

- Evidence: DESIGN:746 sets only `last_activity` 8 h before `now` and "readable" for T. `TranscriptTail` also has `mtime`, `first_record_ts`, `tail_complete`, `project_key` and `session_id` (DESIGN:459), and SPEC:101 says the record time wins over `mtime`. The `test_classify.py` cell is one table cell of roughly 11 KB with the shared Given placed after a colon inside a long sentence.
- Smallest fix: list all eight `TranscriptTail` fields of T in the shared Given (record time and `mtime` both 8 h before `now`, `tail_complete` True) and move the four FR-010 fixtures to a bullet list under the table.

## Checks

| ID | Check | Result | Basis |
|---|---|---|---|
| C1 | Research/04 4.2 edits 1 to 4 are present in the design (DESIGN:746, 501, 771, 1030) | PASS | Read of each line |
| C2 | The three `origin unknown:` literals agree across DESIGN:501, DESIGN:746, research/04 4.2 and SPEC:104 | PASS | Read of all four |
| C3 | The input behind the Orca-unavailable note (`orca_available`) and the truncated note (`truncated`) is named and unambiguous | PASS | DESIGN:456, 501 |
| C4 | The input behind the call-failed note is unambiguous | FAIL | A-1 |
| C5 | Order inside the three-note family is stated and pinned | PASS | DESIGN:501, 746 test 4 |
| C6 | Order across note families (`origin unknown:`, SP-16 literal, `tab map join not observable`) and the exact notes list in test 4 | FAIL | A-3 |
| C7 | The shared Given is consistent with guard case 2 of DESIGN:502 | FAIL | A-2 |
| C8 | `test_fr010_incomplete_notes_order` can be built from its Given | FAIL | A-3 |
| C9 | A synthetic full page can be built for test 2 | FAIL | A-4 |
| C10 | The per-Run source row name is determinable by the `collect` developer | PASS | DESIGN:595 gives the exact string |
| C11 | The `collect` to `classify_all` coupling (row name, non-null `unscanned`, `truncated`) is pinned by a test that runs `collect` | FAIL | A-5 |
| C12 | Note precedence for an entry-bearing transcript under an incomplete list | FAIL (MINOR) | A-6 |
| C13 | All SPEC FR-010 reasons are handled or explicitly excluded | FAIL (MINOR) | A-7 |
| C14 | Stored form of `unscanned` and the row's other fields | FAIL (MINOR) | A-8 |
| C15 | Fixture fields and the control are specified | FAIL (MINOR) | A-9, A-2 |
| C16 | Mechanical report literals reproduce on disk (0 em dashes, 0 TODO or TBD, `four incomplete cases` only at DESIGN:1030, the literals at 501 and 746) | PASS | `grep` counts and lines, this review |
| C17 | "Never idle or Historical" for None is stated | PASS | DESIGN:501, SPEC:104 |

## Self-Audit

**(a) Reliance list:** no `## Inherited Structural Verdict` block was in the spawn prompt, so I ran standalone and relied on no rf-qa PASS. I did not read the sibling reports in `qa/r3-b3/`.

**(b) Independent semantic checks:**
- Note drivers: read DESIGN:456 (`SweepInput`), 501, 595, then DESIGN:250-251, 287, 749, 850 to see what `collect` leaves in `sources` after an outage. This exposed A-1.
- Fixture consistency: read DESIGN:502 (guard cases) against the DESIGN:746 Givens and SPEC:104's two-transcript control. This exposed A-2 and A-3.
- Page build: read DESIGN:420, 456, 548, 746, 980, SPEC:320-321 and research/04 4.5. This exposed A-4.
- Coupling: `grep` for `orca worker-list`, `WORKER_LIST_PAGE`, `full page` (hits only at 501, 548, 595, 614, 746, 771, 891, 980, 1030) and read DESIGN:745, 749, 780, 787 to see whether any test runs `collect` on these inputs. None does. This exposed A-5.

**Counts:** claims checked against files: 31. Files read: DESIGN, research/04, SPEC, mechanical report. Zero-issue claim: not made; 9 findings.

## Summary

- Checks passed: 7 / 17
- Checks failed: 10 (6 tied to MAJOR findings: C4, C6, C7, C8, C9, C11; 4 tied to MINOR findings: C12 to C15; C6 and C8 share A-3)
- Findings: BLOCKING 0, MAJOR 5 (A-1 to A-5), MINOR 4 (A-6 to A-9)
- Confidence: Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (this is check coverage, not a pass signal)
- Tool engagement: Read: 19 | Grep: 10 | Glob: 1 | Bash: 0 (no Python run; this lens needed none)
- Web research: none, so no Tavily or fallback call applies.

The four research edits are applied and the note literals are right. The design still leaves five points where a developer has to guess, and in A-5 a wrong guess would not be caught by any listed test.

Verdict: FAIL
Blocking count: 5

