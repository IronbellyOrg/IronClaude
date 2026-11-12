# QA Report: R3-B2 SPEC-fidelity lens

**Topic:** R3-B2 several-rows rule (DESIGN `docs/designs/orchestrator-mode.md`, 1026 lines at review time) against SPEC FR-010 and SP-29
**Date:** 2026-11-09
**Phase:** fix-cycle gate review (design-fix gate r3-b2), SPEC-fidelity lens
**Fix authorization:** false (report only; no file other than this report was written)

Files read (all in chunks of at most 150 lines): SPEC `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` lines 97-104; DESIGN lines 1-20, 51-80, 449-557, 728-753, 766-769, 805-860, 967-1026; research/04 lines 115-179; research/09 lines 139-201; `phase-outputs/test-results/r3-b2-mechanical.md` lines 1-117. I did not read any other QA report.

## Findings

### F1 (MAJOR): the several-rows rule ignores `tail_complete`, so a multi-row match can join a transcript whose session start is not observable

- DESIGN line 498 (tail rule, earlier in the same bullet): "When the window is observable but the transcript has `tail_complete` False, the session start is not observable: `first_record_ts` is only the first record of the tail, so it can place a later session inside the window or an earlier one outside it. That match does not join: the row is could not determine with note `session start not observable: transcript tail only`, and that transcript is None with the same note."
- DESIGN line 498 (R3-B2 sentences, later in the same bullet): "If exactly one matching row's window holds the transcript, the transcript joins that row only and is False ..." and "If no matching row's window holds it, every matching row is could not determine with its note, and the transcript is None with `pane moved to a later session` ...". Neither sentence mentions `tail_complete`, and "holds" is evaluated on `first_record_ts`.
- DESIGN line 459: `tail_complete` is False for "every file over 256 KiB", the normal case for a long worker session.
- DESIGN line 743, R3-B2 fixtures: none sets `tail_complete` False. The tail-rule fixture (`test_path_b_incomplete_tail_has_no_session_start`) has a single row.
- SPEC FR-010 (line 104): "A positive transcript-to-worker join makes it False. Only when ... the join completed may an unjoined transcript be True. Otherwise it is None." The tail rule exists so that no join is made from an untrustworthy `first_record_ts`.

What is wrong: for a long transcript and two or more matching rows, one reading of line 498 ("exactly one window holds it, so join") makes an unproved join (False, shown as `orca:D2`), and the other reading ("that match does not join") makes none. The text does not say which wins. It also does not say which note the rows and the transcript carry when the tail rule and the `pane moved` / `conflict:` notes both apply. That is a join treated as proved on evidence the DESIGN itself calls unobservable, and the fixtures cannot catch it. Research/04 section 3.3 (lines 148-153) was written without `tail_complete` (grep of 04 for `tail_complete`: no match). R3-B1 added the field later, and the R3-B2 edit was copied across without being reconciled with it.

Smallest fix: add one sentence to line 498 after the R3-B2 text: "The several-rows rule applies only when `tail_complete` is True. With `tail_complete` False, no matching row is joined: every matching row with an observable window is could not determine with `session start not observable: transcript tail only`, every matching row without one is could not determine with `Dispatch time window not observable`, and the transcript is None with `session start not observable: transcript tail only`." Add fixture `test_path_b_several_rows_incomplete_tail_no_join` to the `test_classify.py` row (line 743): the first R3-B2 fixture with S `tail_complete` False gives no join and S None, never False.

### F2 (MINOR): "exactly one window holds it" counts only observable windows, so a row with no observable window is silently treated as not holding

- DESIGN line 498: "each other matching row is could not determine with note `pane moved to a later session` (or `Dispatch time window not observable` when it has no observable window)". Research/04 line 144 lists "a terminal row with no end time" as one source of overlapping windows, but the rule resolves that case to a join, not to `conflict:`.
- FR-010 treats unproved as None, not as a positive. Here the join to D2 is as strong as the single-row join the DESIGN already accepts (line 498: "a person rerun inside the window cannot be told apart"), and the result is False, never True. No person session is hidden that was not already hidden, and no True path opens. The risk is attribution of S to D2 when D1 (window unknown) owns it.
- No fixture covers it: no fixture has one row with an observable window that holds S plus one row with no observable window. The branch "None with `Dispatch time window not observable` when no matching row has an observable window" (line 498) has no fixture either.
- Smallest fix: state in one sentence that a matching row with no observable window is not counted as holding the transcript and that this is deliberate (reason: no evidence either way), or make that case conflict. Add one fixture per branch.

### F3 (MINOR): a row forced to "could not determine" by a join note sits outside the ordered rule table

- DESIGN line 498: "each of those rows is could not determine with note `conflict: ...`". SPEC FR-006: "Each session row gets exactly one class from section 7, chosen by the ordered rule table." DESIGN lines 476-486 list rules 1 to 9, with rule 1 (`blocked_contract`) first.
- The text can be read as letting a join note override rules 1 to 5, so a row with a blocked contract (waiting on a person) would drop out of `waiting on a person (a)` into `could not determine`. The same wording already exists for the single-row `pane moved` case (R2-B1/R3-B1), and R3-B2 extends it to the new `conflict:` case. The row stays visible, so nothing is hidden outright.
- Smallest fix: one sentence in line 498: "A join note does not change the class that rules 1 to 8 give; the class is could not determine only when no earlier rule matches (rule 9)." Or state the opposite on purpose and record it as a deviation.

### F4 (MINOR): D9 "Source" column does not name the R3 reviews, and "R3-B2 rule" is a fix-cycle label used as design prose

- DESIGN line 819 (D9): Source cell "Review 1 B2; review 2 R2-B1 and R2-B2", but the D9 text now carries the R3-B1 window rule and the R3-B2 several-rows rule.
- DESIGN line 498: "Several matching rows follow the R3-B2 rule below." R3-B2 is defined only in section 1 (line 10) and section 18 (line 1026).
- Smallest fix: add "review 3 R3-B1 and R3-B2" to the D9 Source cell and replace "the R3-B2 rule below" with "the several-rows rule below".

### F5 (MINOR): scope and ordering gaps in "matching rows"

- "Matching rows" can only be scoped Dispatch rows (DESIGN line 552, no allowlisted verb lists the rows of other Runs; D9 line 819). "Exactly one" is therefore exactly one scoped row, and a worker of an unscoped Run on a reused pane can join a scoped row as False. SP-29 holds (never True), but the text does not say so. Fix: write "scoped matching row".
- The rule covers path B only. Two scoped rows sharing one `session_join` session id under path A (DESIGN line 497) are not addressed. The outcome is False either way, so FR-010 and SP-29 hold, but the shown row (`orca:<dispatch>`) is undefined.
- The order of the duplicate-Dispatch merge (line 509) and the several-rows rule is not stated: two rows with one Dispatch id and one pane would count as "several rows" and give two identical `row_id` values. Fix: one sentence saying the merge runs first.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | No R3-B2 outcome yields `person_started` True for a transcript with a tab-map entry (exactly-one gives False, conflict gives None, none-holds gives None); SPEC FR-010 guard intact | PASS |
| C2 | SP-29 "tab map marks it as an Orca worker session ... is never True" holds for all three outcomes (DESIGN lines 498-501) | PASS |
| C3 | SP-29 other-Run fixture (SPEC line 104: R2 transcripts never True, never Historical) is unaffected: unmatched entries stay None with `Orca pane session, not in scoped Runs` (DESIGN line 499) | PASS |
| C4 | No new Orca read: DESIGN 7.3 allowlist is still the 8 templates (lines 525-534); the rule uses only `dispatch_started`, `dispatch_ended`, `dispatch_status` from the existing `worker-show` (line 457); no forbidden verb added | PASS |
| C5 | No person session hidden by R3-B2: conflict and none-holds leave the transcript visible as None; exactly-one hides only a within-window rerun, which line 498 already accepts and notes | PASS |
| C6 | No unproved join treated as proved when `tail_complete` is False | FAIL (F1) |
| C7 | "Exactly one window holds it" is safe when another matching row has no observable window; every rule branch has a fixture | FAIL (F2, minor) |
| C8 | Row class stays chosen by the ordered rule table (FR-006, NFR-010) | FAIL (F3, minor) |
| C9 | FR-010 row (line 768), D9 (line 819) and SP-29 row (line 857) carry the same several-rows wording | PASS |
| C10 | Each of the three outcomes has a fixture in section 11 (line 743): `..._pane_reused_joins_later_row_only`, `..._two_windows_hold_session_is_conflict` and `..._shared_boundary_second_is_conflict`, `..._no_matching_window_holds`; order independence and the terminal-handle variant are also present | PASS |
| C11 | Research/04 section 3.3 edits 1 to 5 are all present in the DESIGN (line 498, line 743, line 768, lines 819 and 857, line 1026) | PASS |
| C12 | Result does not depend on row order and no row wins by position | PASS |
| C13 | Mechanical file claims reproduce: re-run gave em-dash count 0, no `TODO`/`TBD` (exit 1), 1026 lines, one `Total: 9 deviations.` (line 821), one `Total: 23 open items.` (line 997). The mechanical file's Command 5 shows "no output expected", not an observed result | PASS |
| C14 | D9 source and prose-label hygiene | FAIL (F4, minor) |
| C15 | Scope of "matching rows" (scoped only), path A and the duplicate-merge order are stated | FAIL (F5, minor) |

## Summary

- Checks passed: 10 / 15. Checks failed: 5 (1 backing a MAJOR finding, 4 backing MINOR findings).
- BLOCKING: 0. MAJOR: 1 (F1). MINOR: 4 (F2 to F5), recorded as notes.
- The rule does not contradict SPEC FR-010 or SP-29 on the True side (nothing it produces is True) and adds no Orca read. The one defect is the unresolved collision with the `tail_complete` rule, which lets a multi-row match read as a join on an unobservable session start.

Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 14 | Grep: 7 | Glob: 0 | Bash: 2

Verdict: FAIL
Blocking count: 1
