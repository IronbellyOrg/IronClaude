# Position paper D07, OURS: coordinators live in each project, one dispatcher over the Orca repo list

Author role: advocate for the owner's line. Date 2026-11-20.

Abbreviations used below. REQ = `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (the owner's zero-setup watcher requirements, local and unpushed, branch `ironbelly/issue-watcher-zero-setup-plan`, commit `d0a0a433b`). DESIGN = `docs/designs/orchestrator.md` in the snapshot `/home/coder/.cache/ic-snap-20261120/master` (Clay's design, merged by PR 681). Q26 = `/home/coder/workspaces/worktrees/IronClaude/issue-624/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q26-coordinator-layout/final.md`. OWNER-ANSWERS = `.../20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md` in the same worktree.

## 1. The claim

The place where an issue is worked is the project that owns the issue. So the coordinator session, its branch, its worktree and its records live inside each project. One cron entry runs one dispatcher that asks Orca (`orca repo list`) which projects exist, keeps one small config per project under `~/.config/superclaude/issue-watch.d/`, and runs each project's cycle in turn. The session is named `COORD-<RepoName>`. Nothing needs a second repository, a hand-kept list of repositories, or a registry file.

## 2. The mechanism

1. Discovery. The dispatcher runs `orca repo list`, skips temporary and foreign-owner repos, and writes a config for any project that has none (REQ R8, R15, R16). Orca is already the place where a project is registered, so adding a project is one act, not two.
2. Per-project cycle. Each project gets its own config, `state_dir`, lock, kill switch and day cap; the dispatcher starts one child process per project, serially, with one rate-limit wait for the account, one launch per sweep and rotating order (REQ R5; built in `src/superclaude/cli/issue_watch/dispatch.py`, constants `LOOP_CAP_S = 270.0` and `CHILD_TIMEOUT_S = 255.0` at lines 52 and 53).
3. Session. Every project has a `Coordinator` branch, a `Coordinator` worktree and a running session `COORD-<RepoName>`, created by the Orca template and restarted if stopped, checked at boot and on every watcher run (REQ R9, R10, R17; Coder issue 516).
4. Records. Coordinator state lives in `.dev/coordinators/` on a branch shared by every developer's coordinators: `claims/` holds one create-once file per claimed item (git refuses the second creator), and each coordinator has its own folder as the only writer (Q26, "Recommended layout").
5. Origin check. The cycle checks that the worktree's `origin` names the project before every launch, so a session can never work in the wrong repository (REQ R10, R13; `launch.py` origin check).

## 3. Cited facts

1. The owner decided the topology on 2026-11-14: "a Coordinator branch and worktree and a `.dev/coordinators/` directory in every project" (Q26 line 3; OWNER-ANSWERS line 23, "direction accepted"; line 56 onward records decisions 2 to 7 "pasted unchanged" as the owner's answers). The branch `coordinators` exists on the fork: `git ls-remote --heads origin 'coordinators*'` printed `d2d8a2d166c945f556d921b31530a3673f00df89 refs/heads/coordinators` on 2026-11-20 (it holds master's commit only; OWNER-ANSWERS line 81 says no README was added).
2. The owner decided the dispatcher on 2026-11-18: "ONE cron entry runs ONE dispatcher ... which finds the repos with `orca repo list` on every tick ... Per-repo configs are written by the dispatcher ... to `~/.config/superclaude/issue-watch.d/<repo>.json` and are not stored inside the project checkouts. Rejected: one cron entry per project" (REQ R16, line 37), after an adversarial debate (REQ R5, line 31: V2 won 0.84 to 0.77, scores estimated, position-bias check not run).
3. The owner decided the name: session `COORD-<RepoName>`, restart a stopped session, nothing manual (REQ R9 line 40, R17 line 43, Coder issue 516, the owner's open issue in the Coder repo); and "the term is 'coordinator', not 'orchestrator', everywhere" (REQ R10, line 41).
4. This is built, not only planned: `dispatch.py` is 479 lines on the owner's branch, with `tests/issue_watch/test_dispatch.py` (31 test functions; the REQ ledger row for Task 23 counts 42 cases), a `run-all` command with `--dry-run` (REQ ledger, Task 25) and the repo parameter threaded into `github.py` and `launch.py` (REQ R13, ledger Tasks 15 and 16). It is unpushed: `git status --short` in that worktree lists 223 entries.
5. `orca repo list` works under cron's empty environment: "run with an empty environment and only HOME and PATH=/usr/bin:/bin worked (6 repos), so R16's risk is cleared for repo listing" (REQ R21, line 49). On 2026-11-20 the same command on this host lists six repos: IronClaude, Coder, IronOrca, Ironeye, Ironbrain and one temporary `coder-bmad-live-...` repo.
6. Clay's topology needs a workaround that ours does not. DESIGN ADD2 (line 136): the claim "takes its repo from `origin` of the current directory only", the orchestrator session runs in the orchestrator repo, so every shell step is prefixed with `cd <checkout> &&`, and "Whether `/sc:issue` keeps that directory for all its steps is UNVERIFIED and is the first local end-to-end check". In ours the session already sits in a worktree whose origin is the project.
7. Clay's topology needs a setup step that ours does not. `<orchestrator-repo>` is "created outside IronClaude, by the person with the rights to create a repository" (DESIGN line 866) and the poll's config holds its absolute path "on each host" (line 893). On this host `/home/coder/workspaces/IronOrchestrator` does not exist and `orca repo list` does not show it, although the private repo exists on GitHub (`gh api repos/IronbellyOrg/IronOrchestrator` returned `private: true`, `pushed_at 2026-11-19T03:14:05Z`). That is a manual step on every host, which REQ R17 ("Nothing in the setup is manual") forbids.
8. Clay's registry is host-local by construction: `.orchestrator/` is "(git-ignored)" and "orchestrators.json (the registry) ... written only by the poll" (DESIGN line 863 and line 704). Only one host's poll can see it. The design's own answer for two hosts is the claim lease comment (line 708, layer 4: "two hosts that each run a poll"). Ours puts shared coordinator state on a git branch where a create-once claim file is refused by git for the second creator (Q26, proposal B reasons: "Only B stops two coordinators dispatching the same issue ... with a lock git enforces across the whole project").
9. The "65 repositories" argument does not apply to ours. DESIGN ADD3 (line 137) says a per-repo list "would need up to 65 calls" against the cycle budget of 35 (`CALL_CAP = 35`, `github.py` line 46). That budget is per cycle, and ours runs one cycle per project, each with its own budget (REQ R5: "Each repo has its own config, state_dir, lock, kill switch and day cap"). And Clay's own allow list holds three repos (DESIGN line 879 table: IronClaude, IronFlow, IronOrca), not 65.
10. "One orchestrator per repo" is in practice many per repo. DESIGN 5.7 (lines 700 and 706): when a repo has more than three issues "the poll starts another orchestrator for the same repository", bounded only by the day cap of 6 new ids a day. Ours (one coordinator per developer and scope, Q26 `<dev>--<N>`) says the same thing plainly and already has the lock for it.

## 4. What it costs

- It is not on origin. The dispatcher, the repo parameter and the zero-setup plan exist only in the owner's local worktree; PR 686 rewrites six of the same files (analysis FULL-REPORT section 1, item 8). Landing it means pushing and rebasing.
- The layout under `.dev/coordinators/` is a design, not code: `.dev/coordinators/` does not exist in the master snapshot (`ls` of `/home/coder/.cache/ic-snap-20261120/master/.dev/coordinators` fails). Q26 states its own confidence as 70 percent and lists two unverified facts (Orca accepting `--base-branch origin/coordinators`, branch protection).
- The names are not yet one: the 2026-11-14 branch is `coordinators` (plural, exists), while REQ R10 and R20 (2026-11-18) name the branch and worktree `Coordinator` (singular, and R20 notes no remote `Coordinator` branch exists). The spec must pick one.
- One launch per sweep (REQ R5) caps how fast a burst of assigned issues starts.
- It has no in-flight cap per coordinator and no idle end; both are in Clay's 5.7.

## 5. What it risks

- A standing session in every project: five real projects on this host today. Clay's design says of an ended session left at an idle prompt that it "costs no tokens" (DESIGN line 710), which supports the same reading for a waiting coordinator: the cost is memory and attention, not model tokens (UNVERIFIED for a coordinator that has long context).
- A bug in the dispatcher touches every project at once. The mitigations are in REQ R5 and R14: per-project locks and kill switches, a precheck before each child, and a first-run check that leaves a failing project `enabled: false`.

## 6. What it gets right (and what ours should take from the other side)

- Both designs agree on the core: one poll or dispatcher as the only router, per-project origin check, per-project day cap, configs kept outside the project. The dispute is only where the session and the records live.
- Ours is the topology the owner already ruled on three times (Q26, R16, R9). A design that moves it needs a cited benefit, not a preference.
- Honest concession: Clay's per-issue state file (created with exclusive create), the in-flight count and `max_in_flight`, the `wrong_target` refusal, restart of a dead session and the 30-minute idle end are real capabilities that ours has not written down. They do not depend on a separate repo and can be carried into the per-project layout. So can the idea of an org-wide search as a cheap pre-check before starting a child.

