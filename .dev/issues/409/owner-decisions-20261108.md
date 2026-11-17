# Owner decisions, 2026-11-08 (issue 409, Orca observer MVP)

Recorded by an Orca worker (run run_93bfa00cae2b, task task_bfe724db1dac) from the coordinator's relay of the owner's order. Short record; the reasoning lives in the brainstorm package `.dev/brainstorms/20261108-132433-orca-observer-mvp/`.

1. **Staged direction chosen ("Stage it").** The owner accepted the brainstorm's staged recommendation:
   - Release 1: Signal Bridge's worker ledger, built on the verified worker-list source, carrying Attention Ledger's "question source UNVERIFIED" notice.
   - Attention Ledger comes after the QUESTION-OBSERVATION gate.
   - Decision Desk comes behind the QUESTION-LINK gate.
   - Whether this fully satisfies the DIRECTION-SELECTED gate is for the owner to say. What is recorded here: the owner chose the staged direction; the technology stack was NOT yet confirmed.

2. **Stack not confirmed; TUIBBS review first.** Python + Rich remains only a recommendation. The owner asked for a review of the TUIBBS codebase (IronbellyOrg/TUIBBS-scp) before the stack is confirmed. Output: `.dev/issues/409/tuibbs-review/`.

3. **New requirement: write-back from the BBS.** Users must be able to send confirmations or corrections from the BBS to their agents. This departs from issue 409, which lists approving, retrying, terminating, spawning, merging and instructing workers as out of scope and requires a read-only observer. It is recorded as a FUTURE stage that needs an explicit boundary change to issue 409. Release 1 does not do it.

4. **Background, not deciding for release 1.** The owner is also exploring TUIBBS as an internal communication tool and platform for all human staff who manage agent teams; the observer may become a TUIBBS module.

5. **Stack and release-1 scope CONFIRMED (2026-11-08, after the TUIBBS review).** The owner chose "Python + Rich with snapshot export" in reply to the coordinator's question: release 1 is the standalone Python + Rich observer (Signal Bridge worker ledger), and its `export(view)` writes a versioned, additive-only JSON snapshot with a schema test, in release-1 scope, so a read-only Go screen inside TUIBBS can read it later. This supersedes item 2 (stack no longer open). The key-reader spike stays the first task. Still open and NOT decided: write-back boundary change (summary.md decision 3), the licence opinion (decision 4), TUIBBS as the staff platform (decision 5).
