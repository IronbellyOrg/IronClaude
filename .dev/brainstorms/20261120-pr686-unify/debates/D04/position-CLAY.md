# Position CLAY (D04: claim level and grants)

Question: should the watcher always claim at level none with a standing `grants` list, or should the issue's Pipeline field choose the launch level, with one grant row per issue?

## Claim

The claim is always at `--pipeline none`. It assigns, checks accuracy, writes the summary and two comments, and creates no worktree and launches no agent. Then the orchestrator itself starts one supervised worker with `orca orchestration worker-start` in a worktree of the issue's own repo. The claim's own launch levels are never used (R9, `docs/designs/orchestrator.md:81`). The orchestrator's outward writes are bounded by one standing `grants` list in `repos.yaml` (DQ6, D:116), changed only on the owner's recorded word.

## Mechanism

1. Wave 1 claims with `Skill sc:issue --claim <N> --pipeline none` in the issue's own checkout (D:544); wave 4 starts the worker (D:519, 5.3).
2. The worker reports through the Run mailbox (`worker_done`, `ask`, heartbeat), so the orchestrator sees it, checks in, and handles one message once per id (test row "PR B: Orca orchestration", D:1104).
3. The `grants` list is `[issue.assign, issue.comment, issue.body.append_plan_sections, issue.hold, pr.merge, issue.close]` (D:291, D:872). The code refuses a write outside the list with `E-NO-GRANT`, and every write logs the grant it used (D:696). Deleting a branch, force push and settings changes have no grant (D:696).
4. The list changes only through the `superclaude orchestrator repos` verbs, which refuse without an `--answer-ref` that `answer-check` accepts: an answer relayed by another agent, naming another entry, older than the entry, or from an unknown source is refused (D:688, N1 at D:758).
5. A closed "may do" list and `refuse(argv)` (5.9, D:736) refuse listed commands whatever the grant says.

## Cited facts

1. The owner's own decision matches R9. Q35 "B1b", 2026-11-14 (owner-answers.md line 184): "the watcher claims with `--pipeline none`; the coordinator runs the existing worktree step and starts the worker". Built code agrees: `PROMPT_PATTERN = ^/sc:issue --claim N --pipeline none$` (master `src/superclaude/cli/issue_watch/launch.py:33`, builder at line 92) and `commands/issue.md:48`: "The issue watcher never relies on the default: it always passes `--pipeline none`".
2. The governed levels cannot ship, by the owner's own gate. `GOVERNED_LEVELS_ALLOWED = False` (R33, requirements.md line 59); 12 observations skipped (`tests/hooks/test_launch_level_observations.py`, `_PENDING`, 9 + OB-H2 + OB-H3 + OB-CTX); `SKILL.md:92` and the claim doc line 4: no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass; issue 442 is open. R23 and R25 therefore deliver nothing live.
3. The Pipeline-level route is a second launch path with weaker supervision. A launched agent reports only through `.dev/issues/<N>/result.md` (R24, requirements.md line 50; `issue-watcher-status-pipelines.md:73`); a `worker-start` worker answers on the mailbox and falls under the WORKER-CONTRACT rules WC-6 to WC-16. One route is simpler to test and to supervise.
4. The levels multiply the design surface. R23 gives four Statuses, R25 four Pipeline values, and R32 (P-8) requires a decision for each pair on whether the command runs, is limited or is refused; R33 and R34 add a gate, a Status move table, a guard tamper token and a coordinator-only verb. The none-only route needs none of it.
5. The per-issue grant row is a heavy control that the owner accepted only for now. Q36 (line 185): "Latency approved for now". The design's reason for the standing list: "A standing grant is needed because there is no person at each step: the old per-issue 'grant row' came from the approval flow that this issue retires" (D:116).
6. The grant row is a file the owner writes (owner-answers.md line 130: "written by the owner, not by an agent"). The owner's order of 2026-11-17 says approvals are given in chat and the agent records them (memory `approvals-through-chat-never-files`). The standing list has a written, tested change rule instead (`answer-check`, D:688).
7. The standing list is enforced by code and logged, not by convention: `E-NO-GRANT` rows in the test table (D:1111), a text scan that no listed command appears outside the denylist (D:1117), and a rule that the orchestrator never adds a line to `grants` (N1, D:758).
8. Project reads are removed on purpose (R1, R3; "no board column and no Project is read anywhere", D:256). That removes a GraphQL read surface and a failure class the poll had (R31 and R36 needed a value-time observation and a withdrawal).

## What it costs

- The per-issue throttle of the Pipeline field is gone. The orchestrator takes any assigned issue to merge and close; the only brake found is `hold:backlog` (D:445).
- Workers run with no L1 guard and no L2 pre-push hook, with `master` unprotected (DQ7, K12; D:117). The owner accepted this "for the first test issue" only (D:117).
- A standing grant covers `pr.merge` and `issue.close` on every routed issue. That reverses WORKER-CONTRACT lines 23, 70 and 239-246 (coordinator opened by a person; acts on the person's named go). The design says it rewrites them in PR B (ADD1, D:135).
- The identity that records the "word" is "Clay" (D:688); the repository owner is `ironbelly`, and the design never names a login for "the owner" (FULL-REPORT section 4).

## What it risks

- The orchestrator edits the file that holds its own grants. The verb and a test protect it, nothing else (D:688, "ours are inside it").
- Over-reach: one bad routing, an unlisted repo or a mis-assigned issue becomes a merge.

## What it gets right

- The claim step is one fixed, tested, already-built command; nothing to flip, nothing waiting on observations.
- One supervised route for every issue, with a mailbox, heartbeats and an audit trail.
- Standing grants remove a person from every low-stakes step and replace a hand-written row with a verb that refuses an unrecorded change and logs each use.
- It matches the owner's own Q35 and the code on master today.
