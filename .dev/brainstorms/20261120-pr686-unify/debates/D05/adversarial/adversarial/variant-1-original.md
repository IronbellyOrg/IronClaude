# Position OURS (D05): the launch guard governs every started worker

Written 2026-11-20 as the strongest honest case for the owner's line. Short names: "the guard" is `src/superclaude/hooks/scripts/launch-level-guard.sh` (L1, a hook that blocks a governed agent's commit, push, merge and similar calls); "L2" is the git pre-push hook `launch-level-pre-push.sh`; "D:nnn" is a line of Clay's `docs/designs/orchestrator.md` on origin/master (snapshot `/home/coder/.cache/ic-snap-20261120/master`); "LD:nnn" is a line of `docs/designs/sc-issue-launch-level-hook.md` in the same snapshot.

## Claim

Every agent session the system starts to work on an issue must be bound to the launch-level guard before it runs, including a worker the orchestrator starts with `orca orchestration worker-start`. Clay's rule DQ7 (D:117) and risk K12 (D:1234) leave that worker held back by a written prompt only, on a repo whose `master` is unprotected. The guard exists to replace exactly that ("without relying on prompt instructions alone", issue 394, the issue that asked for the guard). Issues 394 (the guard), 442 (its live observations), PR 685 (the runbook and results for 442) and rule R33 (the closed ship gate `GOVERNED_LEVELS_ALLOWED = False`) all assume nothing the system starts runs ungoverned at a level that can push.

## Mechanism

1. A governed session carries `[sc-launch:v1:<nonce>]` in its first prompt and a matching `pending/<nonce>` record in `~/.claude/state/launch-level/` (LD:75-77). The hook binds the session id and then applies one level grid per tool call (LD:91-98).
2. The helper that writes the record for a coordinator-started worker is still on master after PR 682: `cmd_pending` and `publish_pending` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1488` and `:1515`. The deleted worker-brief builder had an optional `nonce` slot that added the marker line (`git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/brief.py`, function `build`, and `templates/worker-brief.txt` section `[marker]`). Binding an orchestrator worker is therefore one marker line in the brief plus one `pending` call, not new code in the hook.
3. Level `FS` (full with `--submit`) allows commit, push of a feature branch and `gh pr create --repo`, and blocks everything else that matters (LD:25-30, grid LD:91-98). That is word for word Clay's own policy for the worker (OD1, D:1152: "pushes its own feature branch and opens its pull request ... never merges and never force pushes"). The guard enforces each of the three prohibitions mechanically: PUSHFORM refuses `--force` and non-plain pushes (LD:113), PROTECTED refuses a push to `master` or `main` (LD:114), MERGE refuses `git merge`, `gh pr merge` and MCP merge tools (LD:115).
4. The guard fails open for anything it does not govern: an unbound session is allowed silently, and "Ordinary sessions are never blocked by a failure" (LD:81, LD:206). Requiring it for orchestrator workers cannot break the orchestrator's own session or a person's session.

## Cited facts

1. Clay's design records the exposure itself. K12 (D:1234) is graded M / H (medium likelihood, high impact): workers run "with no launch-level guard and no L2 pre-push hook, and with push rights on their own branch; IronClaude `master` is not protected, so only the worker's written prompt ... holds it back". DQ8 (D:118) adds `protected: false`, `rules/branches/master` and `rulesets` both `[]`. I re-read the live value today: `gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false`.
2. The owner's acceptance was for one issue, not for the design. D:117 says "The owner already accepted the same condition for the first test issue of the coordinator handoff ("G1")". The G2 note (`docs/designs/issue-pipeline-guard-g2.md:9`) says the guard-less worker was accepted "for the one first test issue" and "Before any other issue runs through the flow, the worker must be bound to the guard (G2)". DQ7 stretches a one-issue acceptance into the standing rule for every issue.
3. Clay's design itself keeps the door open to this. D:970 (row 5d) says the guard-less condition "stays open ... settled before the first real issue"; D:975 says the #442 checks "stay required ... for the orchestrator if the owner chooses to bind its workers (OD1, option B)"; D:1002 keeps guard rule 2 (a bound worker sends and asks with no `--to`) "by every worker if the owner binds orchestrated workers (OD1, option B)". The rule-2 code and its tests survived PR 682 for this reason.
4. Clay's own enforcement has a stated hole that the guard already fills. K22 (D:1244) says the "may never" list "binds the verbs, not a command the model types itself"; U42 (D:1300) asks "whether a hook can run `refuse` on the Bash calls of an orchestrator session only (not on every session of the host)". That is a session-scoped hook, which is what the guard is (LD:23, LD:75-77), already built and registered (`src/superclaude/hooks/hooks.json`, installer list `_FRESHNESS_SCRIPTS`).
5. Clay's detective control cannot see a direct push to `master`. The audit (D:801-828, checks AU1 to AU8) is `superclaude orchestrator audit --repo <R> --pr <N>` and reads one landed pull request. A worker that pushes to `master` with no pull request has no pull request to audit, so the only thing between the worker and `master` is the prompt.
6. The guard has live evidence. In the real-session observations of issue 442 (`observation-results.md` in worktree `issue-442-runbook`, lines 530-541, 549): implement blocked (LL-IMPL), four commit attempts blocked (LL-COMMIT: two in session B, one each in C and D), a bare `approved` did not unlock, a typed `/sc:implement` did, and `git merge` was blocked (LL-MERGE, run 2, line 549). OB-CTX passed (lines 553-563): the selector told a governed `sleep 241` from an ordinary `sleep 242` and from a person's terminal in the same worktree.
7. The owner already treats unproven levels honestly. R33 (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` line 59 in worktree `claim-handoff-planb`; `src/superclaude/cli/issue_watch/launch.py:48`) holds the constant `GOVERNED_LEVELS_ALLOWED = False`, so only `--pipeline none` launches until a reviewed commit flips it and un-skips the observations. The rule is "no governed launch until it is proven", not "the guard is proven".
8. The contract already says outward actions are off for a worker. WC-9 (`src/superclaude/core/WORKER-CONTRACT.md:41`): every outward default (push, merge, PR, GitHub post) is off and "no brief can turn it on". Clay's ADD1 (D:135) turns it on by adding a contract section. A written rule changed by a written rule is the same layer of defence; the guard is the second layer.
9. The guard change in PR 682 was reviewed and kept rule 2: `git show 01e7a9e23 --stat` shows 7 lines changed in each copy of the guard, and E-pr682.md records the independent review as PASS.

## What it costs

- One marker line and one `pending` call per started worker, and the claim preflight (jq present, hooks registered, W-ENFORCEMENT-ABSENT refusal; OB-H2 lines 471-472) must run before the first worker.
- Friction for the worker. The guard blocks compound pushes (`git push origin f 2>&1 | tail -5` is LL-PUSH-FORM, LD:283) and inline `gh api` writes (GHWRITE, LD:116). In the 442 run a blocked compound command was re-issued in split form (observation-results.md line 540).
- A level has to be chosen for implementation workers. G2 was written for the plan-writing worker; `FS` fits OD1, `F` fits WC-9, and neither mapping is written down yet.
- Fail-closed for a bound worker: LL-BROKEN if `jq` is missing (LD:208-215).

## What it risks

- False assurance. The guard is "a same-user guardrail, not a sandbox", aims at honest drift and one-step workarounds, "not TH3 (deliberate evasion)" (LD:32). A bare `claude "<prompt>"` runs a turn outside the limits (issue 678, OB-H1 item 8 FAIL, still open). Pinned leaks stay allowed: `bash ./push.sh`, `G=gi; ${G}t push origin main` (LD:122).
- Binding of a `worker-start` worker has never been observed live. G2 facts 1 to 4 are UNVERIFIED (`issue-pipeline-guard-g2.md:40-43`) and FU-1 precondition f was not tried. The first-prompt delivery by `worker-start` (marker anywhere in the first prompt) is the open question.
- Issue 442 is still open; OB-H2 is a FAIL on a verbatim-detail check (the refusal itself matched; lines 471-472), the protected-push observation was never exercised because the agent declined twice (lines 537, 550), and the guard's own status line says "full enforcement not runtime-approved" (LD:6, LD:17).

## What it gets right

- It treats a prompt as a request, not a control, and says where the enforcement lives.
- It maps onto Clay's own OD1 policy with no new rule: the level `FS` is the policy.
- It keeps the cost where the risk is: only a bound session is ever blocked.
- It does not claim more than it has: the ship gate R33 is closed until the observations pass.
