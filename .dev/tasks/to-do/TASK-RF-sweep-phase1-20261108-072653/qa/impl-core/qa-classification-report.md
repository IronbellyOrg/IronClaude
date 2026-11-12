# QA Report: classification-logic lens (impl-core gate, prompt T180)

**Topic:** `/sc:sweep` Phase 1, `src/superclaude/cli/sweep/classify.py` against DESIGN 7.2 (nine rules, joins, guard cases, R3-B1, R3-B2, R3-B3, D9)
**Phase:** code gate, report-only. `fix_authorization: false`. Only this file was written.
**Reviewer method:** read `models.py` and `classify.py` in full (chunks of at most 150 lines), the DESIGN sections 2.1, 2.2, 7.1 to 7.5 and 11, the SPEC rule table (`merged-requirements.md` lines 225 to 275), `1.0a-facts.md`, and the parts of `probes.py` that feed the classifier (`parse_time`, `parse_worker_show`, `_run_rows`, `_orca_reads`, `_contract_candidates`, `_read_contracts`, `_tail_from_bytes`, `collect`). Then ran about 60 read-only inputs through `classify_all` and `classify` (no file written; `PYTHONDONTWRITEBYTECODE=1`, `uv run --no-sync`). Experiment ids (E1 to E14, T1 to T16, F-A to F-D) are quoted below.

## Result in one paragraph

The logic of all nine rules (given a correctly attached contract), the R3-B1 window, the R3-B2 unique-containing-window rule, the R3-B3 origin notes and all 26 note strings match DESIGN. Every path-B fixture of DESIGN section 11 (reused pane, two windows hold, shared boundary, no window holds, incomplete tail, spans two dispatches, duplicate Dispatch, rows reversed) gives the DESIGN result, and the FR-010 fixtures give the DESIGN notes in the DESIGN order once `JOIN_PATH` is set to `"A"` as their Given says. Two real defects remain: ready Tasks are counted as Dispatch rows by the join guard (CL-1), and a contract that probes read because its row names a report folder is not attached to that row by the classifier (CL-2).

## Findings

### CL-1 (MAJOR): ready Task rows are counted as scoped Dispatch rows by guard cases 1, 2 and 4

- **Evidence:** `probes.py:1079-1089` builds a ready Task as an `OrcaObservation` with `dispatch=<task id>`, `status="ready"` and every other field None, so `session_join` is None. `classify.py:879` and `classify.py:884` pass all of those rows to `_guard`. In `_guard`, `classify.py:758` (`unobservable=any(r.session_join is None for r in rows)`), `classify.py:759` (`no_join=bool(rows) and not j.joined`) and `classify.py:764` (`earlier_pane=path_b and bool(rows)`) treat a ready Task as a Dispatch row.
- **DESIGN text:** guard case 1 is "`session_join` is None on any scoped Dispatch row"; case 2 is "Orca returned at least one worker row"; case 4 is "at least one scoped Dispatch row exists" (DESIGN 7.2, "The guard's 'join completed' condition fails ..." bullet). A ready Task has no Dispatch and is not a worker row.
- **Input that is classified differently (E2):** `orca_available` True, no `worker-list` rows, one ready Task, one readable person transcript `p1` with no tab-map entry, no `unscanned` source. DESIGN: guard holds, `p1` is True with note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope` (the same input without the ready Task, E2b, gives exactly that). Code (E2): `p1` is None, could not determine, notes `could not join Orca workers to transcripts (tab map empty or stale)`, `tab map join not observable`, `earlier pane session not joinable (tab map keeps only the latest session)`. All three notes are false: there is no worker, so nothing failed to join.
- **Wider effect:** with at least one ready Task in any scoped Run, every unjoined transcript carries the false note `tab map join not observable`, and `report.py:347-348` prints the false line `could not join Orca workers to transcripts (tab map empty or stale)` under Could not determine. The error is on the safe side (None, never a wrong True), but it is a wrong statement in the report and a wrong class for a person session.
- **Smallest fix:** compute the guard over Dispatch rows only: in `classify_all` pass `[o for o in orca_rows if o.status != "ready"]` to `_guard` (a real Dispatch has `dispatch.status` of pending, dispatched, completed, failed or circuit_broken, never `ready`, `1.0a-facts.md` row 6). Add the E2 input as a fixture.

### CL-2 (MAJOR): a contract that probes found through the row's report folder is not attached to that row

- **Evidence:** `probes.py:939-953` (`_contract_candidates`) names a contract from `--report-dir`, `--output-dir` or `--output <abs dir>` as `<dir>/return-contract.yaml`, and `probes.py:1236-1253` reads it. `classify.py:597-600` (`_contract_for`) then attaches a contract only when `str(c.path)` is a substring of the row's `task_spec_text` or `body_text`. A report folder in the text never contains the file name, so that test fails. The fallback at `classify.py:601-606` needs `orca.worktree_path` set, exactly one row in that worktree and exactly one contract under it.
- **Input that is classified differently (F-B, F-C):** `task_spec_text` is `On a blocked gate: report blocked` and `Command: /sc:tdd "a" --report-dir /w/.dev/x/`; the contract `/w/.dev/x/return-contract.yaml` has `worker_status: blocked`; Orca outcome `failed`. DESIGN rule 1 (Orca row settled) gives waiting on a person (a). Code gives could not determine, rule `fallback`, `contract attached: False` when `worktree_path` is None (F-B: a row past the 50-call show cap has a Task spec but no `worktree_path`) and when a second contract sits under the same worktree (F-C). With the full contract path in the text (F-D) or a lone row and lone contract (F-A) the code gives waiting (a). WORKER-CONTRACT.md line 167 and line 255 describe an L4 restart in the same worktree, which puts two rows in one worktree and defeats the fallback for both.
- **Why it is a rule defect:** rules 1, 4(b), 6 and `policy_of` read `row.contract`; the contract list is "contract records named by Orca rows" (DESIGN section 6). The classifier must use the same naming rule as the reader.
- **Smallest fix:** move the two regexes of `_contract_candidates` to a pure helper in `models.py`, import it in both `probes.py` and `classify.py`, and attach a contract when `c.path` is in the row's candidate set. Add F-B and F-C as fixtures.

### CL-3 (MINOR): a second transcript that joins an already-joined Orca row vanishes without a note

- **Evidence:** `classify.py:657-660` (path B, one holder) and `classify.py:683-686` (path A, one row) call `j.joined.setdefault(...)` and then `j.taken.add(idx)`; `classify.py:914-916` skips every taken transcript. When two transcripts reach the same row, the first by `(session_id, path)` sort wins and the other is dropped from rows, notes and totals (E1: two tab-map entries sharing one terminal handle, both first records inside the window; output has one row and `total 1`).
- **Why MINOR:** DESIGN is silent for two transcripts on one row. Reaching it needs two tab-map files with the same line 3 or two transcript files with one `sessionId`, which the one-entry-per-pane rule of DESIGN section 1 makes unlikely. Both transcripts are `person_started` False either way, so no wrong True results. It still breaks the DESIGN principle that no input is dropped and no winner is chosen by position.
- **Fix:** when `joined` already holds the dispatch, treat the pair as `conflict: one pane session matches several Dispatch rows`-style: leave both transcripts unjoined with a conflict note.

### CL-4 (MINOR): rule 8 accepts a future `last_activity` as an active person session

- **Evidence:** `classify.py:337-350` tests `last >= ctx.window_start` with no upper bound; T14c (last record 13:00 with `now` 12:00) gives `person session (active)` with note `timestamp in the future`. DESIGN 7.2 (Age, SP-26, D5) says only that such a timestamp "never satisfies rule 7". SPEC rule 8 says "timestamp known". A future stamp has unknown age, so could not determine is the more cautious reading.
- **Why MINOR:** DESIGN is silent for rule 8, the note is attached, and the person is never told a session is idle. Decide the reading in the test plan; if "unknown age" is meant to cover rule 8, add `and last <= ctx.now`.

### CL-5 (MINOR, information): rule 5 cannot match live data, and the DESIGN section 11 FR-010 fixtures need `JOIN_PATH = "A"`

- `probes.py:397` and `probes.py:399` read both `dispatch_status` and `status` from `dispatch.status`, whose observed values are pending, dispatched, completed, failed and circuit_broken (`1.0a-facts.md` row 6). Rule 5 needs `status == "in_progress"` (`classify.py:279-292`, DESIGN 7.2 SP-24), so no live worker is ever `working`. This is the recorded outcome of open item 6 ("Rule 5 cannot match; rows fall to the fallback"), not a new defect.
- `JOIN_PATH` is the literal `"B"` (`classify.py:37`) and is read only at `classify.py:755`. The DESIGN section 11 "Shared Given" is written for path A: with the constant at `"B"` the control fixture gives None with the notes `could not join ...` and `earlier pane session not joinable ...` instead of True (the control fixture run with the constant at `"B"`); with `classify.JOIN_PATH = "A"` the control, the outage fixture, the full-page fixture, `test_fr010_incomplete_notes_order` parts (a) and (b) all give the DESIGN notes in the DESIGN order. The future `test_classify.py` must monkeypatch the constant for those fixtures.

### CL-6 (MINOR, outside this lens, to be confirmed by the probes reviewer): relative report folders find no contract

- `probes.py:938` requires the contract path to start at a `/`. The `Command:` example in WORKER-CONTRACT.md (`--output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`, around line 290) is relative. Run on that text, `_contract_candidates` returns `()` (verified). If live briefs use that form, no contract is read and rules 1, 4(b) and 6 never see one. DESIGN does not say how a row names its contract, and `readonly-probe.md` holds no live brief text, so the live form is unverified. Not graded as blocking here.

## Observations that need no change

- Path A with several matching rows (`classify.py:688-690`) uses the conflict note; DESIGN states the several-rows rule for path B only.
- `first is None` with `tail_complete` True (`classify.py:634`) is treated like a tail-only transcript; it cannot occur, because `session_id` is set only when a timestamp parsed (`probes.py:713`).
- No `tests/sweep/test_classify.py` exists yet (DESIGN section 11 plans it for a later step), so none of the rules above is pinned by a test at this gate; `phase8-validation.md` runs 4 tests, all in `test_readonly.py`.

## Walk of the nine rules, joins and guards (one input per item, or the lines that prove none exists)

| Item | Input tried | Code result | Differs from DESIGN? |
|---|---|---|---|
| Rule 1 (`classify.py:189-216`) | T5 blocked, live, ask, `agent_wait` set; T6 live, `gate_policy` None, no wait; T6b unverifiable, ask; T6c live, ask, Ruling halt; T7 no Orca row, no halt; T7b no Orca row, halt | waiting (a) via rule 4 with the M6 note; fallback with the M6 note; fallback with no note; waiting (a) by rule 1; fallback with `blocked contract; Orca state not observed`; waiting (a) by rule 1 | No. Lines 194-199, 201-203, 205-214 implement the SPEC text, the note only for a live row with policy ask or None. Contract attachment is CL-2. |
| Rule 2 (`classify.py:219-236`) | T9 exited, done-False, fence absent; T9b exited, fence unreadable; T9c proof plus unreadable transcript | stalled (proved); fallback plus `Orca: exited; fenced evidence not readable`; fallback plus that note plus `unscanned: transcript not readable` | No. |
| Rule 3 (`classify.py:247-251`) | read | `fenced_evidence == "present"` only | No. |
| Rule 4 (`classify.py:254-276`) | T11 failed with E-RESUME-NEEDED only; T11b failed with another STOP code; T13 ready; T16 wait and ready | finished; waiting (b); waiting (b); waiting (a) | No. Lines 260-261 add `timestamp in the future` for a future wait stamp. |
| Rule 5 (`classify.py:279-292`) | T8 four conditions; T8b `agent_wait_present` False | working; fallback | No (unreachable on live data, CL-5). |
| Rule 6 (`classify.py:295-315`) | T3 first line `guard refused:`; T4 later line only; T10 parent; T12 partial | finished; judged on the other clause; finished plus `WC-13 violation, review`; finished plus `partial: usable not yet judged` | No. Evidence strings hold neither `admitted` nor `accepted` (grep of `classify.py`: no match). |
| Rule 7 (`classify.py:318-334`) | T14 five hours before `window_start`; T15 person True with an Orca row | idle; fallback | No. Idle needs `orca is None` (line 322), readable, known and not future. |
| Rule 8 (`classify.py:337-350`) | T14b `last == window_start`; T14c future | person session (active) both | T14b No. T14c is CL-4. |
| Rule 9 and order | `[r.name for r in RULES]` | the nine names of DESIGN 7.2 in order | No. |
| Path A (`classify.py:682-691`) | E9 session id equals `session_join` | joined, `person_started` False, no tab map needed | No. |
| Path B (`classify.py:692-697`) | E4 to E8 with a tab-map entry matching by `terminal_handle`; key set also holds `file_name` | as DESIGN | No. |
| D9 | E13 entry joins nothing; E2b no entry, no rows; E10 outage | None plus `Orca pane session, not in scoped Runs`; True plus `origin not proved ...`; None plus origin notes | No. |
| Guard case 3 | E13 row `session_join` matches no entry | SP-16 literal then `Orca pane session ...` | No. |
| Guard cases 1, 2, 4 | E2 ready Task | false notes, True becomes None | Yes, CL-1. |
| R3-B1 window | E4a start, E4b end plus 0.9 s, E4c end plus 1 s, E4d start minus 0.1 s, E5 open window, E5b `completed` without end | joins, joins (cut to whole seconds), pane moved, before window, joins, `Dispatch time window not observable` | No. `_window` (`classify.py:569-579`) and the cut at line 644 match "both ends included". |
| R3-B1 UTC parse | `parse_time` on 15 forms (SQLite space form, `Z`, `z`, offset, naive `T` form, date only, 9-digit fraction, non-string) | aware UTC or None, never raises; naive `T` form None | No. |
| R3-B2 | E7 two windows hold plus one before; E8 none holds; E6 tail incomplete; E14 duplicate Dispatch; reused pane, shared boundary, spans two dispatches, rows reversed | as the DESIGN fixtures, same output for both row orders | No. `classify.py:644-667`, `533-566`. |
| R3-B3 | E10, E11, E12 and the FR-010 fixtures (a) and (b) | five notes, DESIGN order, before every guard note | No. `classify.py:705-735`. |
| Join outcome after rules 1 to 8 | reused pane D1 with a settled contract | rule `fallback`, rule's evidence kept, class could not determine | No. `_force_unknown`, `classify.py:379-387`. |

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | `RULES` has the nine DESIGN 7.2 names in order | PASS |
| C2 | Rule 1 conditions, decline notes (M6) and the no-Orca-row note | PASS |
| C3 | Rule 2 match, decline and unreadable-evidence note | PASS |
| C4 | Rule 3 fenced | PASS |
| C5 | Rule 4 (a), (b), ready Task, future-wait note | PASS |
| C6 | Rule 5 four conditions | PASS |
| C7 | Rule 6 finished, partial note, first-line `guard refused:`, no `admitted`/`accepted` | PASS |
| C8 | Rule 7 idle | PASS |
| C9 | Rule 8 person active (MINOR CL-4 on a future stamp) | PASS |
| C10 | Rule 9 total fallback and "join outcome applied after rules 1 to 8" | PASS |
| C11 | Contract-to-row attachment feeding rules 1, 4(b), 6 | FAIL (CL-2) |
| C12 | Join path A | PASS |
| C13 | Join path B matching by `file_name` or `terminal_handle` and session id | PASS |
| C14 | D9: None plus pane note, True plus `origin not proved` note, narrowing of SP-29 | PASS |
| C15 | Guard case 1 (`session_join` None on a scoped Dispatch row) | FAIL (CL-1) |
| C16 | Guard case 2 (worker rows, no transcript joined) | FAIL (CL-1) |
| C17 | Guard case 3 (path B, `session_join` matches no entry) | PASS |
| C18 | Guard case 4 (path B, a scoped Dispatch row exists) | FAIL (CL-1) |
| C19 | R3-B1 UTC parse and aware comparison | PASS |
| C20 | R3-B1 window bounds: inclusive, whole-second cut, open window, no observable window | PASS |
| C21 | R3-B2 unique-containing-window rule, three outcomes, notes for other rows | PASS |
| C22 | R3-B2 `tail_complete` False branch | PASS |
| C23 | Duplicate Dispatch merge before every join rule | PASS |
| C24 | R3-B2 result independent of row order | PASS (MINOR CL-3 for two transcripts on one row) |
| C25 | R3-B3 five origin notes, conditions and order | PASS |
| C26 | R3-B3 notes come before every join-guard note; SP-16 literal before `tab map join not observable` | PASS |
| C27 | Note and reason strings byte-exact (26 strings, fixed-string grep of DESIGN or SPEC and of the `classify.py` literal) | PASS |
| C28 | Unreadable transcript or contract gives could not determine plus the `unscanned:` note | PASS |
| C29 | Age rule SP-26 / D5 (future stamp never idle, note added) | PASS |

Checks passed: 25 of 29. Checks failed: 4, from two findings (CL-1 on C15, C16, C18; CL-2 on C11).

## Self-audit

Confidence: Verified: 29/29 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% of checks run; the verdict is FAIL on the two findings above.
Tool engagement: Read: 24 | Grep: 17 | Glob: 1 | Bash: 14 (read-only: `wc`, `ls`, `sed`, `grep`, and eight `uv run --no-sync python` runs over in-memory inputs that wrote no file).
Limits: `JOIN_PATH` was read as a constant, not tested for a live path-A Orca field (1.0a closed item 1 as path B). The live `agentWait` key and the `in_progress` value are unobserved (open item 6), so rules 4(a) and 5 were tested on synthetic values only. `report.py` was read only for the `could not join` line (`report.py:347-348`). `policy_of` (`classify.py:410-422`) has no DESIGN definition beyond "frozen or None"; it follows WORKER-CONTRACT.md line 250 and was not graded.

Verdict: FAIL
Blocking count: 2
