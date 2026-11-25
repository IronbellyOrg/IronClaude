<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (OURS), variant-1-original.md -->
<!-- Non-base: Variant B (CLAY), variant-2-original.md -->
<!-- Merge date: 2026-11-20T04:29:48Z -->

<!-- Source: Base (original, modified) - retitled and role line changed because the document is now a unified topology recommendation, not an advocate paper (refactor-plan Overview) -->
# Unified topology D07: coordinators live in each project, one dispatcher over the Orca repo list, with the CLAY capabilities adopted under conditions

Author role: merge of the D07 debate, base is the owner's line (OURS). Date 2026-11-20.

<!-- Source: Base (original, modified) - abbreviation key extended with the names the merged items cite (PROBE, route.py, issue_watch/); no base abbreviation changed -->
Abbreviations used below. REQ = `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (the owner's zero-setup watcher requirements, local and unpushed, branch `ironbelly/issue-watcher-zero-setup-plan`, commit `d0a0a433b`). DESIGN = `docs/designs/orchestrator.md` in the snapshot `/home/coder/.cache/ic-snap-20261120/master` (Clay's design, merged by PR 681). Q26 = `/home/coder/workspaces/worktrees/IronClaude/issue-624/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q26-coordinator-layout/final.md`. OWNER-ANSWERS = `.../20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md` in the same worktree. PROBE = the invariant probe of this debate (`invariant-probe.md`, finding ids `INV-nnn`). `route.py` = `/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/route.py` (PR 686 snapshot, Clay's code). `issue_watch/` = `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/` (the owner's code, local and unpushed).

<!-- Source: Base (original) -->
## 1. The claim

The place where an issue is worked is the project that owns the issue. So the coordinator session, its branch, its worktree and its records live inside each project. One cron entry runs one dispatcher that asks Orca (`orca repo list`) which projects exist, keeps one small config per project under `~/.config/superclaude/issue-watch.d/`, and runs each project's cycle in turn. The session is named `COORD-<RepoName>`. Nothing needs a second repository, a hand-kept list of repositories, or a registry file.

## 2. The mechanism

<!-- Source: Base (original) -->
1. Discovery. The dispatcher runs `orca repo list`, skips temporary and foreign-owner repos, and writes a config for any project that has none (REQ R8, R15, R16). Orca is already the place where a project is registered, so adding a project is one act, not two.
2. Per-project cycle. Each project gets its own config, `state_dir`, lock, kill switch and day cap; the dispatcher starts one child process per project, serially, with one rate-limit wait for the account, one launch per sweep and rotating order (REQ R5; built in `src/superclaude/cli/issue_watch/dispatch.py`, constants `LOOP_CAP_S = 270.0` and `CHILD_TIMEOUT_S = 255.0` at lines 52 and 53).

<!-- Source: Base (original, modified) - item 3 keeps its facts; "restarted if stopped" now points to the guarded restart (item 7, Change 2) and the worktree-separation condition is added (Change 6, INV-004). The base has no sentence about claim agents to replace, so the condition is added to this item. -->
3. Session. Every project has a `Coordinator` branch, a `Coordinator` worktree and a running session `COORD-<RepoName>`, created by the Orca template and restarted if stopped (the restart is guarded, see item 7), checked at boot and on every watcher run (REQ R9, R10, R17; Coder issue 516). Condition: claim agents never share the standing coordinator's worktree. `launch_argv` starts every claim agent with `--worktree path:<worktree>` (`issue_watch/launch.py` lines 136-157) and REQ R10 makes that the same `Coordinator` worktree where the coordinator session works, but the merged orchestrator spec says "one worktree holds one live agent at a time" (`/home/coder/workspaces/worktrees/IronClaude/issue-624/.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` line 1145, 6.4 rule 2), and Q26's claim procedure needs "no other unpushed commit" in the tree (PROBE INV-004, HIGH). With a cap of 3 there would be up to four live agents in one tree. The spec must either give each claim agent a worktree separate from the standing coordinator's, or keep the cap at 1 (one claim at a time) until it does.

<!-- Source: Base (original) -->
4. Records. Coordinator state lives in `.dev/coordinators/` on a branch shared by every developer's coordinators: `claims/` holds one create-once file per claimed item (git refuses the second creator), and each coordinator has its own folder as the only writer (Q26, "Recommended layout").
5. Origin check. The cycle checks that the worktree's `origin` names the project before every launch, so a session can never work in the wrong repository (REQ R10, R13; `launch.py` origin check).

<!-- Source: Variant B, mechanism 3 and 4, fact 5 (DESIGN lines 700-702; `route.py` `in_flight`), with the safety properties from the CLAY Round 2 rebuttal items 1, 2 and 6 and the probe conditions INV-001, INV-002, INV-003, INV-008 - merged per Change 1; the "until then the cap stays at 1" clause links it to the Change 6 condition in item 3 -->
6. In-flight cap with a fail-closed count (adopted from CLAY, new). The key `max_in_flight` (default 3, which applies only once the worktree condition in item 3 is met; until then the cap stays at 1) lives in the per-repo config `issue-watch.d/<repo>.json`. Rules:
   - Where it runs. The check runs inside the child cycle, after the sweep, not as a dispatcher pre-check that skips the repo. A repo skipped before the child never runs the orphan sweep (`record.sweep`, `record.py` lines 627-651) or the claim observation (`mark_claimed`, `cycle.py` line 959), so a repo full because of an orphaned `pending` entry would stay full for good (PROBE INV-001, HIGH; `dispatch.py` lines 269-304, 432-435).
   - Whose cap. The cap is per coordinator id, not per project. Claim files are project-wide (`claims/issue-<N>.md`, Q26), so the count must filter on the coordinator's own handle (from `gh api user`, Q26); otherwise one developer's issues block another's. The store, `DAY_CAP` and `rotation.json` are per host, so two hosts of one login each count only part of the claims (PROBE INV-008).
   - What counts. Store entries in `pending`, `launched` or `unknown`, plus claim files whose issue is not closed, dropped or escalated. `launched` entries count because a session that has been launched but has not yet pushed its claim file would otherwise be counted nowhere; `woken` is a CLAY state and is not in the owner's `ENTRY_STATES` (PROBE INV-003; `record.py` lines 34-36, 440-441).
   - Count once. An issue that has both a store entry and a claim file counts once (CLAY rebuttal item 1; `route.py` line 411, `key not in state_files`). Otherwise a double count fills the cap early.
   - Write before send. The entry is saved `pending` with its target before anything is sent (DESIGN line 706; `route.py` module docstring lines 6-9), so a poll killed between routing and delivery cannot double-route (DESIGN line 716).
   - Fail closed. A store or claim file that cannot be parsed counts as in flight, so a damaged file "can only stop new routing, never cause an extra issue" (DESIGN line 702).
   - New work only. At or above `max_in_flight` the cycle makes no new launch and records the reason `coordinator_full`, so the wait is visible and an issue does not sit silently. The sweep, the resend and a resume still run. An escalated issue that returns counts again and may exceed the cap without error, because the cap "limits new routing, not the resumption of work" (DESIGN line 702).
   - A closing writer and an expiry. "In flight" must end by a writer and by a time limit, or the count never falls. The owner's store has no closing state where the dispatcher reads: `claimed` is terminal, and `unknown` leaves only through a manual `reset N` (`record.py` lines 448, 706-720; `sweep` never touches `unknown`). Three `unknown` entries would fill the default cap until a person runs `reset`, which breaks REQ R17 "nothing manual". A claim file needs a writer that marks it closed, which is a push by the coordinator and needs the push grant (OWNER-ANSWERS decision 2); a dead or never-started coordinator never writes it. The spec must name this writer and the expiry. Neither is designed yet (PROBE INV-002, HIGH). CLAY has the writer in its `in_progress` to `done` state file (DESIGN line 702; `route.py` `in_flight`).

<!-- Source: Variant B, fact 6 (DESIGN line 710; `route.py` `end_finished` lines 562-603), with CLAY rebuttal items 3, 4 and 5 and the probe conditions INV-005 and INV-006 - merged per Change 2. The idle end is not adopted. -->
7. Restart of a dead coordinator with resume, guarded (adopted from CLAY, new). Rules:
   - Unknown decides nothing. If the terminal list cannot be read, nothing is restarted, so one failed `orca` read cannot start a second session beside a live one (`route.py` lines 582, 595-596; PROBE INV-005, HIGH).
   - Resume only for acknowledged work. A resume wake is sent only when acknowledged work is in flight. A dead session with only unacknowledged wakes is left to the resend (`route.py` lines 576-580).
   - Bounded. Restarts are bounded by a counter kept in the store, 3 attempts, as DQ2: "the start counts as delivery attempt 1" (DESIGN line 710). The owner's code has no wake file, no acknowledgment and no attempt counter today (`ENTRY_STATES`), so the counter and the wake channel are new (PROBE INV-006).
   - Counted against the sweep budget. A restart sits outside the existing brakes (it is not a `launched:` line, not in `consumed_at`, and the 270 s cap is checked only at the top of each repo; `dispatch.py` lines 398, 447-450; `record.py` lines 699-703), so it is counted against the 270 s sweep budget explicitly. A ccsession start path measured 22.5 to 27.1 s (`/home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/REPORT.md` line 23; the orca launch route is UNVERIFIED), so after a workspace restart six restarts would use about 150 s of the 270 s before any child runs (PROBE INV-006).
   - Name of the duty holder. Until Coder issue 516 creates `COORD-<RepoName>`, the session that holds the duties is `ORCH-IronClaude` (REQ R9). No restart targets a name that is not the duty holder, because a "restart" of `COORD-IronClaude` would create a second duty holder (PROBE INV-005).
   - Order. The restart check runs before the child, and before the optional pre-check in item 9.
   - UNVERIFIED. Detecting a session by name or tag is UNVERIFIED on both sides (DESIGN U25). `issue_watch/` has no `COORD-`, `wake`, `terminal` or `resume` string (grep count 0).
   - With nothing in flight, the dispatcher records the session as stopped and leaves recreation to the Coder issue 516 boot check. The 30-minute idle end is NOT adopted (section 8).

<!-- Source: Variant B, fact 4 (DESIGN lines 879-889), with probe condition INV-011 - merged per Change 3 -->
8. Per-repo settings keys (adopted from CLAY, new). The per-repo config `issue-watch.d/<repo>.json` takes an optional `merge` block with the keys `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers` and `merge_safety_files`. The generator fills only values it can read, such as `can_merge` from the collaborator role (REQ R4). Any value the owner has not named stays absent; DESIGN lines 879-889 mark the IronFlow and IronOrca values UNVERIFIED. The coordinator reads the keys at merge time; the watcher never does. Merge authority itself is decided in topic D06. Condition: the config directory is "not tamper-protected" (`issue_watch/launch.py` lines 48-53) and an agent can reach that path (REQ R33 item 4 had to add `*.config/superclaude*` to the launch-level guard tokens). So the safety list and `can_merge` are overridden by the live GitHub role at merge time, and the safety list changes only on the owner's recorded word (PROBE INV-011).

<!-- Source: Variant B, mechanism 1 and fact 3 (DESIGN line 137), with probe condition INV-010 - merged per Change 4, marked optional and off in the first build -->
9. Org-wide search as an optional pre-check (adopted from CLAY, optional, off in the first build). The dispatcher may run one search per (login, org) for open assigned issues, and a project absent from the result is skipped as `nothing_assigned`. It fails open: a failed search, a result of 100 or more, or a missing field skips nothing. A successful empty reply can still be wrong because of search index delay (DESIGN line 137, U8, UNVERIFIED), so it never skips a repo that has work in flight or a dead coordinator; the restart check in item 7 runs first (PROBE INV-010). The gain is small with six repos: `_precheck` makes about 6 calls per repo and the search saves them only for idle repos (PROBE INV-010; DESIGN line 137 gives 8 calls against up to 65, observed once).

<!-- Source: Variant B, facts 7 and 8 (DESIGN lines 702, 704; line 708 from Variant B mechanism 4), with probe condition INV-009 - merged per Change 5 -->
10. Exclusive-create state file per issue and a short-name check (adopted from CLAY, new). Each issue gets a state file beside the claim, created with exclusive create (`O_EXCL`), under a name that carries no coordinator id (DESIGN lines 702, 708). The config, the store, the approvers file and the worktree directory are keyed on `owner/name`, not on the Orca display name; today they are keyed on the display name (`issue_watch/generate.py` lines 197-210 and 245-254; `dispatch._config_path`, `dispatch.py` lines 206-207). Two repos with the same short name are refused. There is no `name_collision` skip reason today, so the spec must add one. Without the refusal the second repo finds `config_path.exists()` (`generate.py` lines 207-208), the dispatcher runs the first repo's config twice per sweep and never serves the second, and `COORD-<RepoName>` would name two sessions alike (PROBE INV-009; DESIGN line 704 has the same refusal in `repos.yaml` validation, `repos_invalid`).

<!-- Source: Base (original) -->
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

<!-- Source: Base (original) -->
- It is not on origin. The dispatcher, the repo parameter and the zero-setup plan exist only in the owner's local worktree; PR 686 rewrites six of the same files (analysis FULL-REPORT section 1, item 8). Landing it means pushing and rebasing.
- The layout under `.dev/coordinators/` is a design, not code: `.dev/coordinators/` does not exist in the master snapshot (`ls` of `/home/coder/.cache/ic-snap-20261120/master/.dev/coordinators` fails). Q26 states its own confidence as 70 percent and lists two unverified facts (Orca accepting `--base-branch origin/coordinators`, branch protection).

<!-- Source: Base (original, modified) - the base line "The names are not yet one ... The spec must pick one." is replaced by the open owner decision, per Change 8 (X-005, C-010, Round 2 OURS item (a)) -->
- The name is an open owner decision, decided in topic D08. The 2026-11-14 branch is `coordinators` (plural, exists on the fork; Q26), while REQ R10 and R20 (2026-11-18) name the branch and worktree `Coordinator` (singular, and R20 notes no remote `Coordinator` branch exists). Separately, REQ R9 and R10 name one `COORD-<RepoName>` per project, while Q26 allows several coordinators per project (`<dev>--<N>`, worktree `coord-<dev>-<kind>-<slug>`). OWNER-ANSWERS line 23 records the direction as "accepted" and the naming convention as NOT decided, so fact 1 in section 3 supports a coordinator in every project and nothing more; mechanism item 3 and fact 1 use both branch names for the same reason. Spec text: "Every project has one standing issue-pipeline coordinator, session `COORD-<RepoName>`, in worktree `Coordinator`. It is one of the coordinators Q26 allows; its records go under `.dev/coordinators/` on the shared branch. Whether that branch is `Coordinator` or `coordinators` is an open owner decision."

<!-- Source: Base (original) -->
- One launch per sweep (REQ R5) caps how fast a burst of assigned issues starts.

<!-- Source: Base (original, modified) - the base line "It has no in-flight cap and no idle end; both are in Clay's 5.7." is replaced per Change 7 (and Change 1, which removes "no in-flight cap"): the cap and the restart are now adopted rules, but they are rules without code; the idle end is not adopted -->
- The adopted cap (item 6) and restart (item 7) are rules, not code. Grep finds no in-flight cap in the owner's code (refactor-plan Change 1), and `issue_watch/` has no `COORD-`, `wake`, `terminal` or `resume` string (PROBE INV-005, grep count 0). The code that exists for them is Clay's `route.py` in PR 686, written for a different layout. There is no idle end, by decision (section 8).

<!-- Source: Base (original, modified) - new "Prerequisites" cost line, per Change 7 (PROBE INV-012, HIGH; REQ R6, R9, R10, R20, R21; `launch.py` `GOVERNED_LEVELS_ALLOWED = False`). The topology plus the adoptions does not work alone. -->
- Prerequisites. The topology plus the adopted items 6 to 10 does not work alone. It needs:
  - Coder issue 515, the cron entry and daemon (REQ R6; R21 is still open: only repo listing under cron is cleared).
  - Coder issue 516, the `Coordinator` branch, worktree and session (REQ R9, R10, R20). A project newly registered in Orca has no `Coordinator` worktree, so until 516 creates it every sweep returns `worktree_invalid` for it (`dispatch.py` lines 279-280, `_precheck`); `ls -d /home/coder/workspaces/worktrees/*/Coordinator` finds nothing today (PROBE INV-012 falsifier 1).
  - The branch name decision (the open owner decision above) and a push grant (OWNER-ANSWERS decision 2). Branch protection was dropped (OWNER-ANSWERS line 80), so no create-once claim works until the branch and the grant exist.
  - `GOVERNED_LEVELS_ALLOWED = False` (`issue_watch/launch.py` lines 48-53), so today only Pipeline None launches.
  - A worktree path read from `orca worktree list` instead of the literal `/home/coder/workspaces/worktrees` (`WORKTREES_DIR`, `issue_watch/generate.py` line 40). On a host with another layout every repo would skip. UNVERIFIED beyond the probe's read of the code (PROBE INV-012 falsifier 5).

<!-- Source: Base (original, modified) - new cost line for the worktree separation condition, per Change 6 (PROBE INV-004, HIGH). The condition itself is in mechanism item 3. -->
- Worktree separation is unbuilt. Item 3 requires that claim agents get a worktree separate from the standing coordinator's, or that the cap stays at 1. REQ R10 as written makes them share one tree, so this is a defect in the owner's own plan that the debate found, and nobody addressed it before the probe. If it is not fixed, a claim push can be refused or polluted, and under "no pushed claim, no dispatch" (Q26 line 97) the issue stalls.

## 5. What it risks

<!-- Source: Base (original) -->
- A standing session in every project: five real projects on this host today. Clay's design says of an ended session left at an idle prompt that it "costs no tokens" (DESIGN line 710), which supports the same reading for a waiting coordinator: the cost is memory and attention, not model tokens (UNVERIFIED for a coordinator that has long context).
- A bug in the dispatcher touches every project at once. The mitigations are in REQ R5 and R14: per-project locks and kill switches, a precheck before each child, and a first-run check that leaves a failing project `enabled: false`.

## 6. What it gets right (and what ours should take from the other side)

<!-- Source: Base (original) -->
- Both designs agree on the core: one poll or dispatcher as the only router, per-project origin check, per-project day cap, configs kept outside the project. The dispute is only where the session and the records live.
- Ours is the topology the owner already ruled on three times (Q26, R16, R9). A design that moves it needs a cited benefit, not a preference.

<!-- Source: Base (original, modified) - the base concession bullet listed the per-issue state file, the in-flight count, `wrong_target`, restart and the idle end as capabilities to carry over; the debate carried some and rejected `wrong_target` and the idle end, so the bullet now matches sections 7 and 8 (Changes 1 to 5 and the rejected table) -->
- Honest concession: Clay's in-flight count with `max_in_flight`, the restart of a dead session with resume, the per-repo settings keys, the per-issue exclusive-create state file, the short-name check and an optional org-wide search are real capabilities that ours had not written down. They do not depend on a separate repo and are carried into the per-project layout as mechanism items 6 to 10, under the conditions in section 4. The `wrong_target` refusal and the 30-minute idle end are not carried (section 8).

<!-- Source: Variant B, positions and Round 2 verdicts (C-004, C-005, C-007, C-003, U-011, U-013), plus the debate conditions behind Changes 6 to 8 - new section built from the refactor plan, per Changes 1 to 8 -->
## 7. Adopted from CLAY

Five capabilities come from CLAY. Each is adopted as a rule inside the per-project layout, not as CLAY's separate repository.

| Merged item | CLAY source | Debate result | Change |
|-------------|-------------|---------------|--------|
| Item 6, in-flight cap with fail-closed count | Mechanism 3 and 4, fact 5; DESIGN lines 700-702; `route.py` `in_flight` | C-004, CLAY (hybrid) 85% from both advocates; the safety properties come from the CLAY Round 2 rebuttal | 1 |
| Item 7, guarded restart with resume | Fact 6; DESIGN line 710; `route.py` `end_finished` lines 562-603 | C-005 split, restart to CLAY with guards, 73%; idle end to OURS | 2 |
| Item 8, per-repo settings keys | Fact 4; DESIGN lines 879-889 | C-007, CLAY keys, hybrid, 67% | 3 |
| Item 9, org-wide search pre-check, optional and off in the first build | Mechanism 1, fact 3; DESIGN line 137 | C-003 discovery, OURS with an optional org pre-check, 70%; the gain is small with six repos | 4 |
| Item 10, exclusive-create state file and short-name check | Facts 7 and 8; DESIGN lines 702, 704 | U-011 and U-013 | 5 |

Three conditions come from the invariant probe and the debate, not from CLAY. They are needed for the adopted items to work:

- Claim agents never share the standing coordinator's worktree (Change 6; PROBE INV-004, HIGH; mechanism item 3).
- Prerequisites are stated as dependencies, not as "alone" (Change 7; PROBE INV-012, HIGH; section 4).
- The unresolved branch and session name is an open owner decision, decided in topic D08 (Change 8; X-005, C-010; section 4).

<!-- Source: Refactor plan, "Changes NOT Being Made" table, with the CLAY Round 2 rebuttal positions - new section, per the plan (no change number; these are the items the merge does not make) -->
## 8. Rejected from CLAY and why

The diff-point ids are the debate's own. Three ids appear twice because the debate split the point: C-003 (allow list rejected, org search adopted in item 9), C-004 (extra orchestrator rejected, cap adopted in item 6) and C-005 (idle end rejected, restart adopted in item 7).

| Diff point | CLAY approach | Why the base stays | CLAY advocate in Round 2 |
|------------|---------------|--------------------|--------------------------|
| C-001 | Session in the orchestrator repo workspace with `cd <checkout> &&` | DESIGN line 136 marks the directory premise UNVERIFIED; ours starts in a worktree with the right origin | Conceded, 85% |
| C-002 | Git-ignored `.orchestrator/` registry in a separate repo | Host-local state; DESIGN line 708 itself falls back to a lease comment for two hosts | Both advocates agreed |
| C-003 (allow list) | Hand-kept `repos.yaml` allow list as the discovery gate | Manual per host (REQ R17); `SKIP_REASONS` already says "seen but not allowed"; the approval gate and first-run check do the safety job | Accepted |
| C-005 (idle end) | 30-minute idle end | REQ R9 requires a running coordinator in every project; DESIGN line 710 says an ended session costs no tokens, so the saving is small | Accepted |
| C-004 (extra orchestrator) | Poll starts another orchestrator when the first is full | REQ R17's standing authorization covers one named session; an extra session needs its own name and approval. A 4th issue waits, and the wait must be visible as a skip reason (item 6, `coordinator_full`) | Accepted, on that visibility condition |
| U-008 | `wrong_target` refusal | One coordinator per project plus the origin check leaves no wrong target; revisit if two hosts start one name | Accepted; the residual two-host case is not helped by `wrong_target` either |
| C-012 | `orgs` list in `repos.yaml` for two organizations | `allowed_owners` is already a list key in `defaults.py` (line 38; default `("IronbellyOrg",)` at line 30) | Moved to OURS, 65% |
| C-008 | Separate `IronbellyOrg/IronOrchestrator` repo | Manual clone and path per host; no benefit that a project-local layout lacks | Accepted |
