# Round 1 advocate statement: Variant 1 (OURS) on D10, wake transport

Exports: M = /home/coder/.cache/ic-snap-20261120/master, A = .../pr-a (PR 686), W = /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb. "D:n" = line n of M/docs/designs/orchestrator.md. Every citation below was re-read in this round unless marked UNVERIFIED.

## Position summary

The poll should add no delivery channel. It launches one claim session through the single Orca verb `orca agent launch` with an integer-only prompt, and the coordinator reads the claim's files at its own gates. The wake file, mailbox and typed line solve a problem (reaching a busy coordinator) that OURS avoids by not pushing at all. I concede OURS has no acknowledgment and no answer for a down coordinator, so the honest recommendation is: keep OURS as the transport, and take from Clay the durable-file-plus-acknowledgment idea as an optional later layer, not the typed line.

## Steelman of Variant 2

Strongest version: a poll that only starts a session is fire-and-forget. If the session dies, is never read, or the coordinator is down, nothing notices. Clay's design makes the durable JSON file the truth, so a busy, crashed or restarted coordinator loses nothing (D:112, D:151). It is at-least-once with an acknowledgment, three resends, then exit 7 and an unread mark (D:112; `wake.py` `mark_unread`). Its security rule is wider than ours: wake id only in the typed line and mailbox subject, and every `gh`/`orca` argv built from a wake field is pattern-checked (D:234 point 2). It also stays script-only until a session reads the wake: "an idle poll is a script that costs no tokens" (D:120). The typed-line wake is not invented: the report waker on master already finds a session by running process, checks `draft` and fresh output, and sends with a receipt (M `orca_term.py`, header lines 1-6). Clay discloses its weak points (K11, K16, U5, U25) rather than hiding them. Last, the transport carries ids only, so it does not depend on the contested trigger rules. Where OURS says "nothing starts while the coordinator is down" (M issue-watcher.md:43), Clay has a defined answer.

## Strengths claimed (OURS)

1. No new surface. D1 option A is "No listener, inbound port or address registry" (M issue-watcher.md:47); non-goal NG-1 is "push designs B/C/D" (:76). A typed wake into a terminal is a push design in all but name.
2. One integer reaches the prompt, built and tested. `PROMPT_PATTERN` (M `launch.py:33`), `build_claim_prompt` (:84-92), `launch_argv` raises on any other prompt (:94-118). D3 is the owner's rule (issue-watcher.md:39, :49).
3. Launch is one Orca verb with an operation id: `orca agent launch ... --json` (`launch.py:96-117`) plus `--retry-launch <id>` (`launch.py:120-132`), and a durable `pending` write before the spawn (issue-watcher.md:23, RC3). Clay's launcher instead creates a terminal, types `ccsession`, and waits for the text "Session name" (A `launch.py:50`, docstring at :329 marks the fresh-terminal behaviour UNVERIFIED, U9).
4. No copied terminal code. M `orca_term.py:3` says "FR-26: reused, never copied". A `wake.py` says "It duplicates that script on purpose" (A `wake.py:12`) and Clay's own register accepts it "for now" (K16, D:1238).
5. The owner already narrowed the listener: Q3 "narrow Coder#477 to read-only status and identity with no prompt routing" (W owner-answers.md:25). On the listener, both lines agree.
6. Clay's mechanism rests on unproven shapes by Clay's own register: K11 "The wake mechanism is unproven here" (D:1233), U5 (D:1263), U25 (D:1283). Its fixtures for send, read and idle are `_assumed_shape` with "UNVERIFIED" in each `source` field (A `tests/issue_watch/fixtures/_assumed_shape/orca_terminal_*.json`).
7. Typing into a terminal races a person. The guard is a screen read plus 60 s of quiet (D:112; A `wake.py:64`, `_unsafe` at :746). Clay's own paper says the race is narrowed, not closed.

## Weaknesses identified in Variant 2

1. Two of three channels may not work: the mailbox send from outside any Run is U5, unverified (D:163, D:1263); if refused, only the typed line is left, which a busy session never takes (Clay's own paper, risk 1).
2. A copy of about 100 lines of Orca terminal code with no parity test against `orca_term.py`. `find_orca` and origin check have parity tests (A `test_find_orca_parity.py`, `test_origin_parity.py`; both also exist on master). The terminal port has unit tests (A `test_wake.py:495` onward) but they run on assumed-shape fixtures, so they prove the code matches a guess.
3. The wake file carries an issue title (D:185; `wake.py:103-113`), and `clean_title` strips control characters only. A rule that keeps text out of the typed line does not keep it out of the model that reads the file. This is a larger prompt-injection surface than OURS, where the claim session sees only an integer and reads GitHub itself under the claim skill.
4. Larger surface for the same hand-off: PR 686 is 8,322 lines (Clay's paper). Nothing reads the wake until PR B exists and the poll stays `enabled: false`, so no part of the wake path is yet useful.
5. Starting a session is an extra mutating act by a script with no human in the loop (C-008). That is also its advantage; it is a trade, not a free win.

## Concessions

1. My cited fact 4 overreaches. Decision 6 (W owner-answers.md:139) and `WORKER-CONTRACT.md:300` (W `src/superclaude/core/WORKER-CONTRACT.md`) forbid typed text to a worker for plan approval. They do not forbid a typed wake line to an orchestrator session. C-006 is therefore a design preference, not an owner ruling.
2. OURS has no acknowledgment loop and no delivery guarantee. If the claim session dies after assigning the issue, only the `pending` record and the next cycle recover it.
3. OURS has no push to a running coordinator. Coder issue 516's gap, "nothing provisions that coordinator", is real, and "nothing starts while the coordinator is down" (issue-watcher.md:43) is a cost.
4. OURS is also unproven live: launch reply shapes are `_assumed_shape` until FU-1 (issue-watcher.md:33; `launch.py:38-47` marks the operation-id paths `[PROPOSAL, UNVERIFIED]`).
5. Cost per claim is one model session; Clay's idle path is script-only.
6. The report waker is real practice on master. Clay's K11 "copied from a pattern that runs" is fair; what is unproven is the orchestrator variant, not the idea.

## Shared-assumption responses

- A-001 (poll must push a signal): QUALIFY. OURS does not assume it: the coordinator pulls from `dispatch.json` and the claim files. But OURS has no timer that makes the coordinator look, which is the real gap. A coordinator `check --wait` loop that reads one local file would make the typed line and mailbox optional accelerators. Neither paper tests this.
- A-002 (Orca screen state is reliable enough to decide typing is safe): REJECT as a premise to build on today. Every fixture for it is `_assumed_shape` and marked UNVERIFIED (A fixtures; `wake.py:746-790`), and Clay's own paper says the race with a person is not closed.
- A-003 (single host): ACCEPT. Both need it: Clay's `/proc` lookup and local wake file, OURS's `--worktree path:<local path>` (`launch.py:104`). It is a limit on both, not a differentiator.
- A-004 (transport separable from trigger and plan-hold rules): QUALIFY. The typed line and subject carry only a wake id, so separable there. The wake file carries `plan_requests[]` with an issue title (D:185), so the transport is not purely ids and the plan-hold content rides on it.

## Per-point verdicts

| Point | Winner | Confidence | One-line evidence |
|---|---|---|---|
| S-001 | none (not a merit point) | 90% | 3 steps vs 5 reflects scope, not quality |
| C-001 | OURS | 60% | No new channel; but it does not solve reaching a running coordinator |
| C-002 | CLAY | 85% | Ack, 3 resends, unread mark (D:112); OURS has only the `pending` guard |
| C-003 | tie | 95% | Both reject the listener (issue-watcher.md:47, :55; D:66) |
| C-004 | OURS | 70% | `launch_argv` one verb with operation id vs terminal create plus "Session name" wait (A `launch.py:50`) |
| C-005 | OURS | 80% | `orca_term.py:3` "never copied" vs `wake.py:12` "duplicates ... on purpose" |
| C-006 | OURS (weak) | 50% | Owner dropped typing for approvals only (concession 1); typing here is guarded and id-only |
| C-007 | CLAY | 75% | Idle poll costs no tokens (D:120); OURS starts a model session per claim |
| C-008 | CLAY | 70% | Poll starts a session when none is live (D:112); OURS idles (issue-watcher.md:43) |
| X-001 | split | 65% | Report waker exists on master; the orchestrator wake has no live run (D:1233, D:1263) |
| X-002 | OURS on origin, CLAY on breadth | 75% | D3 is the owner's (issue-watcher.md:39); Clay widens it to every channel (D:155, D:234), which is an improvement |
| U-001 | OURS | 75% | Q3 narrows 477; decision 6 is about approvals, so limited weight on wake typing |
| U-002 | OURS | 65% | Pending write, operation id retry (`launch.py:120-132`); live replies still assumed |
| U-003 | CLAY | 85% | Durable file plus ack makes a lost wake loud (K14, D:1236) |
| U-004 | CLAY | 70% | Rule on every argv (D:234) is real; the title-in-file weakness is disclosed |

## Corrections to either paper

1. Variant 1 fact 7 says "PR 686 adds parity tests for `find_orca` and the origin check". Those test files already exist on master (M `tests/issue_watch/test_find_orca_parity.py`, `test_origin_parity.py`), so PR 686 did not add them. Variant 2's risk 3 has the same framing.
2. Variant 1 fact 7 says `orca_term` "appears only in a comment (`test_wake.py:495`)". Wrong as worded: it also appears in each `_assumed_shape` fixture's `source` field and in the fixture names `orca_terminal_*.json`. The substance holds: no test compares the copy to `orca_term.py`, and the section at `test_wake.py:495` does unit-test the port.
3. Variant 1 fact 4 cites `WORKER-CONTRACT.md` for "types nothing into a worker's terminal". The line (W `src/superclaude/core/WORKER-CONTRACT.md:300`) is about plan approval to a worker, not about waking a coordinator (see concession 1).
4. Diff-analysis C-006 treats decision 6 as ruling out Clay's typed line. It does not.
5. Variant 2 fact 4 cites `orca_term.py:34-58, :94-133` and `waker.py:2-16`. I checked only the module header (lines 1-6, matches); the line ranges themselves are UNVERIFIED.
6. Variant 2 fact 8 cites issue-watcher.md:43 as "Nothing starts while the coordinator is down". The sentence continues "so this change merges only with or after the coordinator rules", so it is a merge-ordering note about worker start, not a statement that the poll cannot start a session.
