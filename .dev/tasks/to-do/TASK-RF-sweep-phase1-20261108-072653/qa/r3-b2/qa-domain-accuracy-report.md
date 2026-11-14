# QA Report: R3-B2 domain-accuracy lens (ccsession pane file movement)

**Topic:** R3-B2 several scoped Dispatch rows match one pane session (items 3.1 to 3.4)
**Date:** 2026-11-09 (host date in the task context; the mechanical file is stamped 2026-11-08)
**Phase:** doc-qualitative, domain-accuracy lens (research/09 Gap 5 domain row, 500-1500 line band)
**Fix cycle:** 0 (first review of this gate), `fix_authorization: false`
**Design file read:** `docs/designs/orchestrator-mode.md`, 1026 lines on disk (the task says 1013 at build time; the mechanical file also says 1026)

## Scope and method

I tried to break the rule with real ccsession sequences, not to re-check structure. Sources read from disk:

- `docs/designs/orchestrator-mode.md` lines 5-36, 449-517 (7.2, worker bullet is line 498), 728-752 (section 11), 764-768 (FR-010 row), 805-826 (D9), 851-857 (SP-29), 870-900 (15.1), 990-1026 (open items, revision log).
- `research/04-design-fixes-r3.md` lines 120-176, `research/09-gap-fill.md` lines 139-176, `phase-outputs/test-results/r3-b2-mechanical.md` (all 116 lines).
- ccsession source, `/home/coder/.local/bin/ccsession` lines 560-640 and 1860-1900 (byte-identical to the repo copy `src/superclaude/skills/ccsession-tag/ccsession` and to `~/.claude/skills/ccsession-tag/ccsession`, checked with `diff -q`), and the hook `~/.claude/skills/ccsession-tag/hooks/session-name.sh` lines 120-215.
- Orca 1.4.245 bundle `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` (dispatch insert at offset 1629300) and `orca-ide orchestration dispatch --help`.
- 300 most recent Claude Code transcripts under `~/.claude/projects` (jq scans, read-only).

Semantics used: `person_started` False means the transcript is a worker of an Orca row and is shown as `orca:<dispatch>` (DESIGN line 498; SPEC FR-010). A false join therefore hides a person's session inside an Orca row and attaches its activity to that row.

## Facts established about how the pane file moves

1. One file per pane key, three lines (session, folder, terminal handle), replaced as a whole (`ccsession:574-605`). The hook writes it at `SessionStart` and `UserPromptSubmit` only (`session-name.sh:177-181`), so `/clear` and `/resume` move it. A session id is removed from every other pane's file (`ccsession:590-602` region). The DESIGN's statements at lines 32 and 498 match this.
2. The same terminal handle means a person reran the command (`ccsession:607-613`). The pane key survives Orca restarts (comment at `ccsession:560-563`), so a pane key outlives any one worker.
3. A nested `claude -p` inside a launched session cannot overwrite the entry: the hook's `OWNER` check (`session-name.sh:144-163`) blocks it. A plain `claude` writes no entry (`session-name.sh:177`). Neither route can produce a false join.
4. No evidence that `/resume` copies old history under a new id: none of the 300 recent transcripts holds a foreign `sessionId` in its first 300 lines. 32 of 150 sampled files show a backward timestamp jump over 60 seconds; I opened one (`1779a921-...jsonl`): its first records are untimed metadata and its minimum timestamp equals its first timestamp, so no copied history there. I did not open the other 31, so this is a sample, not proof. D-1 to D-3 do not depend on it.
5. `orca orchestration dispatch --task <id> --to <handle> [--inject]` dispatches to an existing terminal. The bundle's error text says to "pick a terminal that already runs one" (an agent CLI) and otherwise deliver the prompt with `orca terminal send`. A second Dispatch to a live worker terminal therefore continues the same Claude session. Nothing in ccsession ties a new Dispatch to a new session.
6. The Orca insert refuses a new row only while another row on the same handle or pane key is `pending` or `dispatched` (bundle `$nt`). Completed rows followed by a new row on the same terminal are the normal sequential case.
7. 297 of the 300 most recent local transcripts are over 256 KiB, so `tail_complete` False is the usual case, not an edge case.

## Findings

### D-1 BLOCKING (D9): the several-rows paragraph bypasses the incomplete-tail guard, so a person's long session can join as Orca-started

- Evidence: `docs/designs/orchestrator-mode.md:498`. The single-row text says a match with `tail_complete` False "does not join" (`session start not observable: transcript tail only`). The next sentence then says "Several matching rows follow the R3-B2 rule below." The R3-B2 text that follows (from "Several scoped Dispatch rows can match one tab-map entry" to "instead of `Orca pane session, not in scoped Runs`") contains no mention of `tail_complete` (grep inside that span returns 0 hits). Section 11 has no several-rows fixture with `tail_complete` False; the only incomplete-tail fixture, `test_path_b_incomplete_tail_has_no_session_start` (line 743), uses one row D1.
- Real sequence:
  1. Pane K hosts worker W. D1 on K, 09:00 to 10:00, `completed`. A retry D2 on K, from 10:30, `dispatched`, no end. W exits without `worker_done`, so D2 stays open (the case rule 2 exists for).
  2. At 11:30 a person runs `ccsession` in tab K. The hook writes K to the new session S (first record 11:31).
  3. S runs for hours, so its transcript is over 256 KiB (the normal case, fact 7). The tail starts at 12:40, so `first_record_ts` is 12:40 with `tail_complete` False.
  4. Sweep at 13:00. D1 and D2 both match K. D1's window does not hold 12:40. D2's open window (to `collected_start`) does. Exactly one window holds it, so by the R3-B2 sentence S "joins that row only and is False", shown as `orca:D2`.
  5. With one matching row, the same S would have been None with `session start not observable`. The new paragraph turns a safe None into a false Orca join.
- Smallest fix: in the R3-B2 span add one sentence: "The `tail_complete` False rule above is applied first: a transcript with an incomplete tail joins none of the matching rows; each matching row whose window holds `first_record_ts` is could not determine with `session start not observable: transcript tail only`, and the transcript is None with that note." Add one fixture under `test_classify.py` (D1 closed, D2 open, S with `tail_complete` False inside D2's window; expect no join, S None) and name it in the 3.4 table and the section 11 row.

### D-2 BLOCKING (D9): an open window joins any later ccsession session in the pane as Orca-started, and the owner sign-off does not cover it

- Evidence: `docs/designs/orchestrator-mode.md:498` defines the window as `dispatch_started` to `collected_start` when `dispatch_ended` is None and `dispatch_status` is `pending` or `dispatched`. Fixture `test_path_b_window_open_row_joins` (line 743) pins the join. Line 498 admits "a person rerun inside the window cannot be told apart" but only as a limit of a bounded window. D9 (line 819), SP-29 (line 857) and open item 22 (line 994) ask the owner to sign off "the D9 narrowing of SP-29" (True becomes None). None of them states that an in-window person session is reported as Orca-started (False).
- Real sequence: worker session S1 on pane K, D1 `dispatched` from 10:00:00. Claude exits or the person closes it, no `worker_done`; D1 stays `dispatched` (this is exactly the exited-without-done state rule 2 classifies; whether Orca later closes the row is not verified in the DESIGN, and a `pending` row whose worker never started behaves the same). At 11:30 the person reruns `ccsession` in the same terminal (`ccsession:607-613`: same handle means a person rerun). The hook writes K to S2 (`session-name.sh:177-181`). With a complete tail S2's first record 11:31 lies in `[10:00:00, collected_start]`, so S2 joins D1 as False, shown as `orca:D1`. The person's active session leaves `person session (active)` and its recent activity becomes the stalled worker's `last_activity`. S1, the real worker, has no entry and is None (guard case 4).
- Why this goes past the disclosed limit: a closed window bounds the false-join period to the Dispatch's life; an open window has no upper bound, so the exposure grows with every hour after the worker died, which is the state the sweep is built to find.
- Smallest fix: join through an open window only while the worker is live. In the window sentence add: "An open window (`dispatch_ended` None) counts as observable only when `liveness_verdict` is `live`; otherwise the row has no observable window." Update `test_path_b_window_open_row_joins` to carry a live row and add a case with an `exited` row and a later session (expect `Dispatch time window not observable`, S None). Separately state in D9, SP-29 and open item 22 that a path-B join inside the window is False for a person rerun, so the owner signs off the residual too.

### D-3 MAJOR: "pane moved to a later session" is asserted when the session is earlier, and a live session that spans two Dispatches is attached to the older row

- Evidence: `docs/designs/orchestrator-mode.md:498` gives every non-holding matching row `pane moved to a later session`, whether `first_record_ts` is before or after its window. Fixture 1 (`test_path_b_pane_reused_joins_later_row_only`, line 743) assumes the second Dispatch starts a new session (S first 10:40, after D2's 10:30). Fact 5 says a second Dispatch to a live terminal continues the same session; fact 1 says the pane file moves only on a session change.
- Real sequence: persistent worker W, session S started 09:05 (complete tail), D1 09:00 to 10:00 `completed`. The coordinator runs `orca orchestration dispatch --task T2 --to <W's handle>` at 10:30, creating D2 `dispatched`. S continues, now executing D2. Both rows match K. Only D1's window holds 09:05, so S joins D1 (a completed row, now showing D2-era activity) and D2, the live row that S is working, becomes could not determine with a note that is false (no later session exists). If D2 is waiting on a person, it drops out of the waiting section.
- This is not a person session, so it is not D9-blocking, but it attributes the live session to the wrong Dispatch row and states a false cause.
- Smallest fix: count a matching row that is `pending` or `dispatched` and whose `dispatch_started` is later than `first_record_ts` as also holding the session (the session predates it and can be serving it), so this case becomes the `conflict:` result instead of a join to D1. Use a different note than `pane moved to a later session` when `first_record_ts` is earlier than `dispatch_started`. Add one fixture for this sequence and one 15.1 capture line: whether a second Dispatch to a live terminal keeps the same session (research/04 section 3.6 lists the related questions as UNVERIFIED but the DESIGN does not carry them).

### D-4 MINOR (notes, never fail the gate)

- M-1: `ccsession:574-602` (DESIGN line 498) stops before the end of `orca_tab_session`, which closes at line 605 (`exec 9>&-` is 603). The claims cited are still true.
- M-2: `r3-b2-mechanical.md` checks 1 and 2 prove that a sentence and a fixture name exist, not that the sequences behind them are real. Check 5 prints no command output ("no output expected"); I re-ran it (exit 1, no TODO or TBD) and the em-dash count (0), the several-rows sentence count (1) and the section line ranges (7.2 is 449-517, worker bullet 498, section 11 728-752). All agree with the file.
- M-3: every other matching row becomes could not determine, including a `completed` row with a parsed contract (fixture 1 pins D1 this way). A failed transcript join does not change rule 6 inputs, so a finished row is downgraded without evidence. This is conservative, not a false join, and was already the single-row behavior.

## Self-Audit

**(a) Reliance list: items taken from the mechanical file without re-deriving the sequence**
- Relied on `r3-b2-mechanical.md` checks 4 to 7 (em-dash, TODO/TBD, deviation total, open-item total) as presence checks; I re-ran 4 and 5 and the sentence count only (C13).

**(b) Independent semantic checks (INV-019)**
- ccsession pane-file movement checked against the source and the hook, not against the DESIGN's paraphrase: `ccsession:560-613`, `session-name.sh:144-181` (C2, C6, C7).
- Whether a second Dispatch starts a new session, checked in the Orca bundle and CLI help (C10, D-3).
- How common an incomplete tail is, measured on 300 local transcripts (297 over 256 KiB) (C9, D-1).
- Whether the several-rows span mentions `tail_complete`, checked by grep on the exact span of line 498 (0 hits) (C9).

Not verified, stated so nobody reads it as checked: that Orca leaves a row `dispatched` after the worker exits (D-2 also works with a `pending` row); that `dispatch --inject` never triggers a `/clear` (the CLI help and error text do not say it does); the live `worker-show` field names (the DESIGN already marks these UNVERIFIED, open item 23).

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Edit 3.1 is in 7.2 line 498 and gives one sentence per outcome (one holds, two or more hold, none holds) | PASS |
| C2 | ccsession facts the rule cites are true: one session per pane file, `/clear` and `/resume` move it, same terminal means a person rerun (`ccsession:574-613`) | PASS (cite range ends 3 lines early, M-1) |
| C3 | `/clear` sequence: S1 to S2 in the pane; S2 joins only inside the window; S1 is None through guard case 4 | PASS |
| C4 | `/resume` sequence: the entry moves; an id removed from other panes leaves the old row unjoined, not mis-joined; resumed session keeps its id in the sample | PASS |
| C5 | Retry reusing a pane with closed windows (fixture 1): later row only, earlier row could not determine | PASS |
| C6 | A nested `claude -p` cannot move the pane file (`OWNER` check) | PASS |
| C7 | A plain `claude` in a worker pane writes no entry, so it cannot be joined | PASS |
| C8 | A person rerun after the worker exits cannot be joined as Orca-started through an open window | FAIL (D-2) |
| C9 | Several rows with an incomplete tail keep the single-row "does not join" result | FAIL (D-1) |
| C10 | A live session that spans two Dispatches is not attached to the older row with a false note | FAIL (D-3) |
| C11 | Result does not depend on row order; shared boundary second yields `conflict:` | PASS |
| C12 | D9, SP-29, FR-010 and open item 22 disclose the residual in-window False for a person session so the owner signs off the real risk | FAIL (D-2) |
| C13 | `r3-b2-mechanical.md` facts match disk (line ranges 449-517, 498, 728-752; em-dash 0; no TODO/TBD; one several-rows sentence) | PASS |
| C14 | Section 11 fixtures cover the domain sequences (incomplete tail with several rows, open window on an exited row, session spanning two Dispatches) | FAIL (D-1, D-2, D-3) |

## Confidence Gate

- Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (all 14 checks were run with tool evidence; the three assumptions listed under Self-Audit are limits of the evidence, not unchecked items)
- Tool engagement: Read: 11 | Grep: 4 | Glob: 0 | Bash: 21
- Tool calls exceed the 14 checks. No web research was done, so no Tavily call was needed.

## Summary

- Checks passed: 9 / 14. Failed: 5 (C8, C9, C10, C12, C14).
- Findings: 2 BLOCKING (D-1, D-2), 1 MAJOR (D-3), 3 MINOR (M-1 to M-3).
- What passes: the closed-window retry case, `/clear`, `/resume`, nested launches and plain launches behave as the DESIGN says.
- What fails: the new several-rows text (a) skips the incomplete-tail guard, which is the normal case on this host, and (b) leaves the open-window join unbounded and outside the owner sign-off. Both give a false Orca join of a person's session. The pane-reuse fixtures also assume every Dispatch starts a new session, which `dispatch --to` on a running agent does not do.

## Recommended action

Send D-1 and D-2 back for a fix (one added sentence each, one new fixture each, and a line in D9, SP-29 and open item 22 for the residual). Fix D-3 in the same pass, since it edits the same sentence. Then re-review those three items only.

Verdict: FAIL
Blocking count: 3
