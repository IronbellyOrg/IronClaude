# Position CLAY (D05): started workers run without the launch guard

Written 2026-11-20 as the strongest honest case for Clay's line. Same short names as the other paper: "the guard" is `launch-level-guard.sh` (L1), "L2" is `launch-level-pre-push.sh`, "D:nnn" is a line of `docs/designs/orchestrator.md` on origin/master (snapshot `/home/coder/.cache/ic-snap-20261120/master`), "LD:nnn" is a line of `docs/designs/sc-issue-launch-level-hook.md` in the same snapshot.

## Claim

Workers the orchestrator starts with `worker-start` do not need the launch-level guard or the L2 pre-push hook, and the design must not make them wait for it. The guard was built for sessions the claim script launches; it does not govern a coordinator-started worker today (and never did), its live proof is unfinished, and the controls Clay's design adds sit where the work actually happens: the worker's written contract, the orchestrator's closed "may do" list, a merge gate pinned to the head commit, and an audit after each merge. The risk of an unguarded worker is named, graded and left for the owner (DQ7 and K12, decision OD1).

## Mechanism

1. The guard binds only a session whose first prompt carries `[sc-launch:v1:<32 hex>]` plus a pending nonce; an unbound session with no marker is allowed (LD:77, "Unbound with no marker: allow"). A `worker-start` worker has no marker, so the guard never sees it (D:117).
2. The orchestrator never launches through the claim's levels. The skill claims at `--pipeline none` and starts the worker itself (R9, D:81); a test fails if the skill launches through `orca_worktree.py launch` (K4, D:1226; DQ7, D:117).
3. What bounds the worker instead: the handoff prompt, the "Orchestrated issue flow" section of the worker contract (ADD1, D:135), and the rule that only the orchestrator merges, with `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>` and never `--auto`, `--admin` or `--delete-branch` (DQ8, D:118). The orchestrator's own verbs pass through one function `refuse(argv)` that holds the "may never" patterns as data (5.9, D:767), and an audit after landing checks force pushes, dismissed reviews, threads resolved with no reply, conflict markers, loosened tests and changes to merge-safety files such as `src/superclaude/hooks/` (5.11, D:801-828).
4. The live test of the first worker records `ls ~/.claude/state/launch-level/sessions/` before and after the worker starts, and what the worker can reach (D:975, K12 mitigation D:1234).

## Cited facts

1. The guard's own scope excludes this worker, and the owner wrote that. LD:23: "A worker that a coordinator starts after a `--pipeline none` claim (the coordinator handoff, amended 2026-11-17) is not launched by the claim script, so this guard does not govern it." The G2 note says the owner accepted the guard-less worker for the first test issue (`docs/designs/issue-pipeline-guard-g2.md:9`). DQ7 states the same scope; it adds no new exposure that the owner's own text did not already describe.
2. The guard is not proven live. Its status line says "full enforcement not runtime-approved" and "no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass" (LD:6, LD:10, LD:17). Issue 442 (the live observations) is still open and PR 685 (the runbook and results) is still open. The results (`observation-results.md` in worktree `issue-442-runbook`): OB-H1 item 8 FAIL (line 267; issue 678, a bare `claude "<prompt>"` runs a turn outside the limits, open), OB-H2 FAIL (line 353), protected push never exercised, the agent declined twice (lines 537, 550), and the `/sc:pr-submit --monitor 3` cycle at level FS was not observed (a plain feature-branch push and `gh pr create` at FS did run in session E, pull request 654, lines 508-514, so the gap is the monitor cycle, not push or PR creation). "Required for every worker" would put the whole orchestrated flow behind an unfinished gate.
3. Under the owner's own plan nothing real is governed today. R33 (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` line 59, `src/superclaude/cli/issue_watch/launch.py:48` in worktree `claim-handoff-planb`) sets `GOVERNED_LEVELS_ALLOWED = False`: only `--pipeline none` launches. A `--pipeline none` claim writes no launch record (IR-1, LD:349: "nothing for `--pipeline none`"), so the one launch that runs is ungoverned. "The guard governs every launch" is true on paper; in practice both lines run an unguarded worker at the only level that launches.
4. The guard is a limited tool and says so. "Same-user guardrail, not a sandbox"; targets honest drift and one-step workarounds, "not TH3 (deliberate evasion)"; "Coverage is the explicitly checked routes, not universal prevention" (LD:32). Identity loss is a declared fail-open (LD:81). Pinned leaks stay allowed (`bash ./push.sh`, `G=gi; ${G}t push origin main`, LD:122). The earlier acceptance matrix has AC-6 (merge and protected-push coverage) "NOT MET" (LD:331, historical). The real fix for "master unprotected" is not a hook.
5. The guard and the pull-request workflow rub against each other. `/sc:pr-submit` resolves review threads with `gh api graphql ... resolveReviewThread` and replies with `gh api --method POST` (`src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh:131`, `:141`), a class the guard blocks at every level when typed inline (GHWRITE, LD:116). It works only because the call sits inside a script, a route the guard pins as an allowed gap (`bash ./push.sh`, LD:122). Compound pushes are refused too (LL-PUSH-FORM, LD:283), and in the 442 run a blocked command was re-issued in split form (observation-results.md line 540).
6. Binding a `worker-start` worker has never been observed. The G2 facts 1 to 4 are UNVERIFIED (`issue-pipeline-guard-g2.md:40-43`): how to read the worker's session id, that `send` and `ask` reach the guard with full text, that an omitted `--to` reaches the coordinator, that a `.ok` file changes the next call. FU-1 precondition f (does `worker-start` deliver a bound first prompt) was not tried (`docs/designs/issue-pipeline-fu1.md`, cited at g2.md:22).
7. The design has controls the guard lacks and states them in tests. `refuse(argv)` has a failing case for every "may never" pattern (D:1117); the merge gate refuses `threads_open`, `changes_requested`, a moved head and an unreadable state (D:118, D:801-818); the audit grades AU1 to AU8 and escalates only the violations that can leave a merge broken or unreviewed (D:822-828). Master has nothing equivalent (H-design681-map.md row 5.9, 5.11: "NEW. Nothing equivalent on master").
8. The risk is recorded and given a decision owner, not hidden. K12 (D:1234) is graded M / H with its mitigations; OD1 (D:1152) is marked Decided by ruling 3 (2026-11-19 01:25 UTC); D:970 sends the permission-mode and guard-less condition to "settled before the first real issue". The design says plainly "This is a risk and not a question" (D:117).
9. The guard change in PR 682 was kept narrow and reviewed. Guard rule 1 (a TAMPER class for verbs that no longer exist) was removed because the verbs are gone; rule 2 stays; the PR carries an independent review result PASS (E-pr682.md; D:1004).

## What it costs

- A worker that ignores its prompt can push to `master`: nothing on GitHub stops it (`protected: false`, no rulesets, D:118; live value re-read today, `false`). L2 is not installed for that worker (`install_l2` runs only in the claim's launch step, D:117).
- The prompt and contract text are the only brake on the worker (K12). The audit reads pull requests, so a direct push to `master` with no pull request is outside its reach.
- WC-9 is overridden by a contract section (ADD1), a text change on a security-flavoured rule.

## What it risks

- The `refuse` list binds the orchestrator's verbs, "not a command the model types itself" (K22, D:1244); U42 (D:1300) is open.
- Standing risk grows with scale: the orchestrator runs up to three issues at once (D:698-718), each with a worker holding push rights on its own branch.
- If the guard is later extended to these workers, the live test of this design that records "unbound" (D:975) would be wrong.

## What it gets right

- It does not wait on a gate that is not finished (442, 678 open) and it does not claim a protection nobody has observed on this worker.
- It puts controls at the point of use: the merge, the push to a named branch, the audit.
- It states the exposure in the design, with a grade and a mitigation, and says it needs the owner's decision.
- It keeps the guard's design intact (guard rule 2 and the whole of the L1 script stay) while removing only what pointed at deleted verbs.
