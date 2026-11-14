# Q24: who runs the shared read-only capture and the join comparison?

## The question, verbatim

Spec row (merged-requirements.md section 3, line 551): "Who runs the shared read-only capture and the join comparison?"

Original wording (ADJ Part 7, line 794): "Who runs the shared read-only Orca capture (attention values for a live and a blocked worker, the agent row of a Run-less session, Orca's event help) and the one-time comparison of the observer's dispatch ids with a sweep's `row_id` list?"

## Spec's recommended answer

"The 409 session with live Orca, read-only, one sitting" (merged-requirements.md line 551; ADJ line 794). "The 409 session" is the agent session that owns the sibling worktree `issue-409-mvp`, where the observer (issue #409) was built.

## Default if unanswered

"PLAN INFERENCE: XC-03, XC-04, OB-03 do not run; V2-02 cannot pass" (merged-requirements.md line 551).

## What it gates

- XC-03, the shared read-only Orca capture (line 451): one sitting, read commands only, recording `projection.attention` values for one live and one blocked worker (open item D-8), the `worktree ps` agent row of a session with no Run, Orca's event help text, the full Orca build string, whether the per-call timeout holds; no `check` run and no message sent. Needs Q24, LIVE (a permitted live Orca session on this host, line 598), ORCA-AVAILABLE, XC-10 items (1) and (4), and its own permission row `GRANT(XC-03,live-read)`. Wave W1. Feeds V2-02, SW-14, OB-09 and softly XC-05.
- XC-04, the one real-id join comparison (line 452): on one real Run, compare the observer's `dispatchId` list with a sweep's `row_id` list; the sweep must be run as `superclaude sweep run --run <id>` on master code after PR #539 merges (SW-05), after the CLI on this host has the sweep (SWEEP-RUNNABLE) and after a ledger entry about the git-config risk (TB-GIT-ROW). Running the sweep writes one dated report file. Moved to wave W3 (line 861: "the JOIN comparison moved to W3, Change 7").
- OB-03, the observer's seeded consumption test (line 251): not read-only; it creates a throwaway Run and seeds messages, under its own row `GRANT(OB-03,seeded-write)`. "Q24's read capture does not authorize seeded message writes" (line 575).
- Through them: V2-02 (the gate check for issue #423, Orchestrator v2) cannot pass without XC-03; OB-06 (the observer's guard-flip PR) needs OB-03.

## Facts the question depends on

| Fact | Source |
|---|---|
| ADJ's recommendation pairs CAP and JOIN in "one sitting"; this spec later moved JOIN to W3 because it needs a merged sweep, so CAP (W1) and JOIN (W3) cannot be one sitting | merged-requirements.md lines 451, 452, 861 |
| W0 intake XC-10 item (1): "the Q24 runner is confirmed live (it exists, is reachable, and can run Orca read verbs from a terminal that holds no Run), else Q24's default is recorded" | merged-requirements.md line 458 |
| The `issue-409-mvp` worktree holds the observer's switch-on as two unpushed commits at `f104ca51a [409-Phase2]`; `origin/master` is not an ancestor of that HEAD; it must not be cleaned before the owner commits or archives its records (OB-01) | merged-requirements.md lines 71, 234, 249, 264 |
| Whether the 409 session is alive today is not checked here (no live Orca call was made for this file) | UNVERIFIED |
| Q-1 failed on 2026-11-11: a terminal not bound to a Run cannot read another terminal's Run; `run-use` on a live coordinator (Q-2) is forbidden for the observer | ADJ line 87 |
| 35 of 53 Runs had consumer_generation 2 or more, so rebinding is routine; the seeded test must run from a plain terminal that holds no Run, `run-create` only, never `run-use` | ADJ line 459 (INV-005) |
| The invariant probe and ADJ name "owner or 409 session" as the runner of the seeded test | ADJ lines 192, 459, 470 |
| The sweep writes its report to `<root>/.dev/sweeps/` | merged-requirements.md line 452 |
| Whether `orca agent launch` creates a Run for a new session is unknown (D-A) | merged-requirements.md line 128 |
| Worktrees are created only through Orca with an agent (`orca worktree create --agent`); the session that creates one owns its agent | ROOT/CLAUDE.md, "Parallel Development with Git Worktrees" |
