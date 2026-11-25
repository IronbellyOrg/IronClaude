# Position CLAY (D06): authority for merging, script-started coordinators, reviewer hold

Status: complete. "D:nnn" is a line of `docs/designs/orchestrator.md` in the read-only export /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6; merged by PR 681, Clay's design). Written as Clay's strongest honest case.

## The claim

An orchestrator session that owns an issue from handoff to merge is only useful if it can finish the job. So it may merge when a closed, mechanical gate passes (DQ8, ruling 5), it may be started by a script (DQ2, ruling 4; ADD1), its worker may open the PR through `/sc:pr-submit` in its own top-level session (ADD1, ruling 3), and a review agent that never ran or never finished holds the PR instead of being skipped (ADD4, ruling 6). Everything that is not on a short closed list of nine human reasons (5.6) is decided by the orchestrator and recorded. Typed, checked human answers replace trust in a relayed approval.

## The mechanism

1. Wave 6 runs `superclaude orchestrator merge-gate`, which decides with the existing `superclaude.pr_submit` core and has a closed set of thirteen reasons (`checks_failing`, `review_stalled`, `changes_requested`, `merge_safety`, `head_moved` and others; wave 6 at D:578-583).
2. Wave 7 re-runs the gate within 2 minutes of the merge, runs `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>` and never `--auto`, `--admin` or `--delete-branch` (D:118, D:586-590). After a restart the PR state is read first, so there is never a second merge (D:591).
3. A pull request that changes a merge-safety file (CI, CODEOWNERS, hooks) or has an open "changes requested" review is a hard hold; a recorded OK for a failing check never clears either (D:583, D:586, D:593; ruling 35).
4. Human answers go through `superclaude orchestrator answer-check`: source typed in the orchestrator's own terminal or a ClickUp DM from Clay's id, "an answer relayed by another agent never counts", entry id named, newer than the notice, and bound to a question key such as `merge_safety:<PR>:<head sha>` (D:694).
5. The start of the coordinator is a terminal plus `ccsession orchestrator-<short>-<n> --tier <orchestrator_tier>`, the pattern `waker.py` already uses, not `worker-start` (D:112).

## Cited facts

1. The merge gate and the PR-state read-back are specified to the command line, with every `gh` call pinned and no merge rights escalated as "gated" (row 9) rather than retried or bypassed (D:118, D:586-591; risk K7 at D:1229 lists the mitigations: head-pinned merge, no `--auto`/`--admin`/`--delete-branch`, no merge over a failing check without a recorded OK).
2. The reviewer hold has a source in the code: `merge_wait` in `src/superclaude/pr_submit/reviewers.py:395-427` (master) returns `no_response` when all listed reviewers are absent, and the design maps that to a hold (D:138). It adds a 60 minute bound after the checks finish, then escalates under row 9 (D:138, D:1155).
3. The skip rule does lose late reviews. `/sc:pr-submit` records an absent reviewer as "sticky" and "ignored for the rest of the run" (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:29-32` (master)), and the owner's own memory notes a Codex security review that posted "minutes after its code review reported clean" (memory `pr-submit-check-pr-open-before-push`). A merge-time check on the final head covers that gap.
4. The design records, per repo, which reviewers actually run: Augment and Codex on IronClaude PR 641 (an ordinary merged PR), Augment alone on IronFlow PRs 1 and 3, Codex alone on IronOrca PR 11 and none on PR 8, so a `reviewers` list per repo (and `none` for a repo with no agent) is the honest way to say what to wait for (D:138).
5. The typed-answer rule is stricter than the contract text. WORKER-CONTRACT.md D2 and the 2026-11-17 chat-approval order are prose; `answer-check` makes four results checkable and writes the source, time and results to an action log (D:694). The same check guards changes to `grants`, `merge_safety_files` and `reach_daily_max` (D:688: those keys change only with an `--answer-ref` that `answer-check` accepts).
6. The nine-row table states when the orchestrator may reach the human, and the rule "an unanswered question waits, no default": "nothing that needs Clay is decided for him" (D:664-696). Merging over a failing check and a merge-safety change both wait for his explicit OK (row 8; ruling 35).
7. A script can start the coordinator without breaking D5's depth reason. The start is a terminal with `ccsession`, not a `worker-start` (D:112), the pattern runs today in `waker.py` (design U3, D:1261 cites `waker.py:144-169`), so the session is depth 0. D5's reason about depth (`.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md:9`) is about a coordinator started by `worker-start`.
8. The design names its own conflict and decides it, rather than hiding it: ADD1 lists WORKER-CONTRACT.md:23, :44-47 and :239-246, and decides to add one new "Orchestrated issue flow" section for a worker with a brief line `Flow: orchestrated-issue`, which may push its own branch and open its PR but "must never merge, delete a branch or force push" (D:135, OD1 at D:1152).
9. Risk is written down with mitigations: K12 names the unguarded worker and the unprotected `master`; D:117 says the owner accepted the same condition for the first coordinator-handoff test issue ("G1"), and the live test records what the worker can reach (D:1234).

## What it costs

- Machinery. A merge-gate verb with 13 reasons, `answer-check`, a `grants` list, state files and restart rules, all unbuilt: no `merge-gate` or `answer-check` exists in master, PR 686 or the branch `issue-655-pr-p` (searched `src/` in the three exports; PR 686 only parses `merge_method`, `release_merge_method` and `merge_safety_files` in `issue_watch/repos.py`).
- A contract section (ADD1) that overrides three rules of WORKER-CONTRACT.md for one flow, and a rewrite of the coordinator spec's human-only list (D:911, C13).

## What it risks

- An orchestrator that merges without a per-PR human go, on a default branch that is not protected (D:118, D:1234); the only guard against a wrong merge is the gate it runs itself plus an audit afterwards (AU4a).
- `answer-check --source` is an argument the calling session passes; the design's own wake path types lines into the same terminal with `orca terminal send` (D:143-160), so a "typed by a person" source cannot be told from typed-by-script by the verb. The design calls this FR-17's "accepted v1 guard" (D:694).
- The authority changes were approved by Clay only; no `ironbelly` approval of PR 681 is on GitHub (FULL-REPORT.md section 4).

## What it gets right

- It makes the merge conditions testable instead of prose, ties an OK to one question and one head SHA, and fails closed (a missing or short file list holds the merge; a restart never merges twice).
- It sees a real hole in the skip rule: a reviewer that is merely late is treated as absent for the rest of a run.
- It limits what reaches the human to a closed list and never decides for an unanswered question.

