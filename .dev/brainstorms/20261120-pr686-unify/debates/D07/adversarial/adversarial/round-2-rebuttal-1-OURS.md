# Round 2 rebuttal, Variant 1 (OURS), debate D07

Abbreviations as in Round 1 (REQ, DESIGN, Q26, OA). Read-only; no GitHub or Orca contact.

## Response to criticisms

- **W1, no `Coordinator` worktree.** Conceded as fact: no `Coordinator` folder exists under any of the five repo folders in `/home/coder/workspaces/worktrees/`, and `dispatch.py:279-280` returns `worktree_invalid`. It is a prerequisite, not a defect: REQ R10 says "does not exist yet" and R9 gives creation to the Orca template, Coder issue 516 (its state is UNVERIFIED; I did not open GitHub). CLAY has an equal prerequisite: `IronOrchestrator` must be cloned to an absolute path on each host (DESIGN 866, 893), it is absent here, and `repos.yaml` is filled by hand. One fair point for CLAY: DQ4 (DESIGN line 114) self-heals a missing repo checkout with `orca project setup-clone`. Ours self-heals only through 516.
- **W2, Q26 settles a different thing.** Conceded in part. Q26 line 6 defines a coordinator as a records keeper; the poll duties came from REQ R9 on 2026-11-18. The two fit as layers, but the layering was not tested.
- **W3, git exclusion untested.** Conceded: no code uses `.dev/coordinators/`. See (c).
- **W4, naming.** Conceded; see (a).
- **W5, single point of failure.** Equal: CLAY's one bad `repos.yaml` also stops every cycle (`registry_invalid`, DESIGN 341, 716).
- **Citations.** `CALL_CAP` is line 46 on master and line 49 on the owner's branch and PR-A; I cited master without saying so. "Built, not only planned" is true of the dispatcher only; I narrow it. R21 cleared only repo listing; the cron install is still open (Coder 515), and `gh` under cron stayed logged in on 2026-11-20 (REQ line 110).

**(a) Decided topology.** OA line 23 quotes the owner: "a Coordinator branch, worktree and `.dev/coordinators/` directory in all projects", recorded as "direction accepted. The naming convention is NOT decided." So "a coordinator in every project" is supported; "the owner decided the layout and names" is not. Decisions 2, 4 and 6 (OA 56-67) and the branch pushed at OA line 81 build on it. The conflict is real in names only: Q26 allows several coordinators per project (worktree `coord-<dev>-<kind>-<slug>`, branch `coordinators`), while REQ R9 and R10 name one `COORD-<RepoName>` in worktree and branch `Coordinator`. Spec text: "Every project has one standing issue-pipeline coordinator, session `COORD-<RepoName>`, in worktree `Coordinator`. It is one of the coordinators Q26 allows; its records go under `.dev/coordinators/` on the shared branch. Whether that branch is `Coordinator` or `coordinators`, and whether the worktree follows Q26's grammar, is an open owner decision."

**(b)** Answered above: a prerequisite owned by 516, with a manual equivalent in CLAY's topology.

**(c) Git create-once lock.** Mostly real in design. Q26 line 97 says "No pushed claim, no dispatch", so dispatch waits for a successful push; git refuses the second push of a path (general git behaviour, not tested here), and the pull-to-push window can only hurt the loser, who never dispatches. My Round 1 "REJECT" of A-004 was too strong. Limits: no code, no branch protection (OA line 80, written rule only), a push grant is needed (OA decision 2), and one host needs only the poll's local lock.

## Concessions and adoptable text

- **C-004, in-flight cap and fail-closed count (dispatcher precheck, per-project `state_dir`).** "Before a launch the dispatcher counts the project's issues in flight: store entries in pending, woken or unknown, plus claim files whose issue is not closed, dropped or escalated. A store or claim file it cannot parse counts as in flight. At `max_in_flight` (default 3, key in `issue-watch.d/<repo>.json`) the repo is skipped with reason `coordinator_full`; the issue waits for the next sweep."
- **C-005, restart with resume (dispatcher, before the child).** "If `COORD-<RepoName>` is not running and the project has work in flight, the dispatcher restarts it in the `Coordinator` worktree under the same name with a wake marked resume; with nothing in flight it records the session as stopped and leaves recreation to the 516 boot check." Tag detection is UNVERIFIED (DESIGN U25).
- **C-007, per-repo keys (`issue-watch.d/<repo>.json`, optional `merge` block).** "Keys: `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`. The generator fills only values it can read, such as `can_merge` from the collaborator role (R4). Any value not named by the owner stays absent. The coordinator reads them at merge time; the watcher never does." DESIGN 879-889 marks IronFlow and IronOrca values UNVERIFIED.
- **C-003, org search as pre-check (dispatcher, before the child loop).** "The dispatcher may run one search per (login, org) for open assigned issues; a project absent from the result is skipped as `nothing_assigned`. A failed search, a result of 100 or more or a missing field skips nothing." Fail-open also answers A-005. Benefit is call cost at scale only (8 against up to 65 calls, DESIGN 137, observed once), so make it optional.
- **C-002 hybrid, kept:** an exclusive-create state file per issue beside the claim.

## Rejections

- **Idle end after 30 minutes.** REQ R9: "Every project always has ... a running coordinator session." Idle end contradicts it.
- **Poll starts another coordinator when full (ruling 8).** R17's standing authorization covers one named `COORD-<RepoName>`; an extra session needs its own name and approval (UNVERIFIED whether the owner would allow it). Q26 coordinators are person-opened (OA 50).
- **`wrong_target`.** One coordinator per project, plus `check_origin` before every launch, leaves no wrong target to refuse.
- **Separate repo, hand-kept `repos.yaml` allow list, `cd <checkout> &&`.** Manual per host (R17); skip reasons already give "seen but not allowed" (`not_enabled`, `origin_mismatch`).

## New evidence

DQ4 `setup-clone` (above); REQ R9 says `ORCH-IronClaude` already runs on the main checkout; R20 (use an existing remote branch) is still open; OA line 80 drops branch protection.

## Shared assumptions

- **A-001 QUALIFY:** one host today; the git claim is the cross-host upgrade path, and the spec should say so.
- **A-002 ACCEPT:** six Orca repos; budget not binding.
- **A-003 QUALIFY:** restart needs a detection method neither side has proved.
- **A-004 QUALIFY (was REJECT):** see (c).
- **A-005 QUALIFY:** per-repo listing avoids truncation; the org pre-check fails open.

## Updated verdicts

| Point | Winner | Confidence |
|---|---|---|
| X-001 who decided | OURS on direction only; layout and names open | 70% |
| C-003 discovery | OURS, optional org pre-check | 70% |
| C-004 cap | CLAY, hybrid | 85% |
| C-005 lifecycle | Split: restart CLAY, idle end OURS | 70% |
| C-007 settings | CLAY keys, hybrid | 65% |
| C-009 cross-host | OURS in design, untested | 55% |
| X-005 branch naming | Neither, both open | 50% |

All other Round 1 verdicts stand.
