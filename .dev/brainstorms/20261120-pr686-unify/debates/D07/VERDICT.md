# Verdict D07: State, registry and topology

## Question

CLAY keeps a registry `.orchestrator/orchestrators.json` in a separate repo `IronbellyOrg/IronOrchestrator`, one orchestrator per repo, three in flight, multi-org search (ADD3, D:137, D:267-305, D:698-718). OURS (Q26 final in the `issue-339-orchestrator-mode` worktree brainstorm, Coder issue 516, requirements R5/R8/R13/R16): coordinators live in each project (a `Coordinator` branch and worktree, `.dev/coordinators/` layout), one dispatcher loops over `orca repo list`, configs in `~/.config/superclaude/issue-watch.d/`, session named `COORD-<RepoName>`. Which topology wins?

## Winner

HYBRID: the topology is OURS (project-local coordinators, one dispatcher over the Orca repo list), with five separable CLAY capabilities adopted inside it under stated conditions.

## Winning recommendation

The unified spec must say the following. Each line can be checked against a file or a test.

1. **Topology (OURS).** Coordinator session, branch, worktree and records live in each project. One cron entry runs one dispatcher; it lists projects with `orca repo list` (a failed list is an error exit, never "zero repos"), keeps one config per project under `~/.config/superclaude/issue-watch.d/`, and runs one child cycle per project with its own lock, state directory, kill switch and day cap. Test: `tests/issue_watch/test_dispatch.py` on the owner's branch already covers the loop, the rotation and the 270 s cap.
2. **No registry repo.** The spec removes the separate `IronbellyOrg/IronOrchestrator` repo, the git-ignored `.orchestrator/orchestrators.json`, the hand-kept `repos.yaml` allow list, the 30-minute idle end, the poll starting extra orchestrators for one repo, the `wrong_target` refusal and the `cd <checkout> &&` step. Test: a grep of the unified spec for `orchestrators.json` and `repos.yaml` finds only the "rejected" table.
3. **In-flight cap, adopted (CLAY), with these conditions.** Key `max_in_flight` (default 3) in the per-repo config. The check runs inside the child cycle after the sweep, not as a dispatcher pre-check (a skipped repo never runs the orphan sweep; `dispatch.py` 269-304 and 432-435, `record.sweep` in `record.py` 627-651). The cap is per coordinator id. "In flight" counts store entries in `pending`, `launched`, `unknown` plus claim files not closed, counts each issue once, writes `pending` before anything is sent, treats an unreadable file as in flight, and limits only new launches (resends and resume still run). A full repo records the visible reason `coordinator_full`. "In flight" must have a named closing writer and an expiry, because `unknown` entries leave only by a manual `reset N` (`record.py` 448, 706-720); the spec says this is not yet designed. Tests: a full repo drains after an orphaned `pending` entry; one issue with a store entry and a claim file counts once; three `unknown` entries do not block forever.
4. **Guarded restart, adopted (CLAY).** A dead coordinator with acknowledged work in flight is restarted with a resume wake; an unreadable terminal list restarts nothing; an unacknowledged wake is left to the resend; restarts are bounded (3 attempts, DESIGN line 710) with a counter kept in the store; a restart counts against the 270 s sweep budget; until Coder issue 516 creates `COORD-<RepoName>`, the duty holder is `ORCH-IronClaude`, so nothing restarts a name that does not hold the duties. Session detection by name or tag is UNVERIFIED on both sides (DESIGN U25). The 30-minute idle end is not adopted (REQ R9: every project has a running session).
5. **Per-repo settings keys, adopted (CLAY).** Optional `merge` block in the per-repo config: `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`. The coordinator reads them at merge time; the watcher never does. `can_merge` and the safety list are overridden by the live GitHub role at merge time, because the config directory "is not tamper-protected" (`launch.py` 48-53); the safety list changes only on the owner's recorded word. Merge authority itself is decided in D06.
6. **Org-wide search, optional and off in the first build (CLAY).** One search per (login, org) as a pre-check; it fails open (a failed search, 100 or more results, a missing field skips nothing), runs after the restart check, and never skips a repo with work in flight. Gain is small with six repos.
7. **State keyed on `owner/name`, short names unique, exclusive-create state file per issue (CLAY).** Today the config, store and worktree are keyed on the Orca display name (`generate.py` 197-210, 245-254; `dispatch._config_path` 206-207), so two repos with one name collide; the spec adds a `name_collision` skip reason.
8. **Worktree separation (found by the debate, a defect of OURS).** Claim agents are launched into the same `Coordinator` worktree where the standing coordinator works (`launch.py` `launch_argv` 136-157; REQ R10), against the rule "one worktree holds one live agent at a time" (`merged-requirements.md` line 1145). The spec gives each claim agent its own worktree, or keeps the cap at 1 until it does.
9. **Prerequisites stated, not "alone".** Coder issue 515 (cron), Coder issue 516 (Coordinator branch, worktree and session), the branch-name decision, a push grant, and a worktree path read from `orca worktree list` rather than the literal `/home/coder/workspaces/worktrees` (`generate.py` line 40, UNVERIFIED beyond the probe's read). Until 516 lands, `dispatch.py` 279-280 returns `worktree_invalid` for every repo, so the built dispatcher serves none.
10. **Narrow the owner-decision wording.** The owner decided the direction ("a Coordinator branch, worktree and `.dev/coordinators/` directory in all projects", OWNER-ANSWERS line 23: "direction accepted. The naming convention is NOT decided"). The spec must not say the owner decided the layout or the names. Open owner decision (topic D08): branch `coordinators` (exists on the fork) or `Coordinator` (REQ R10, R20), and one `COORD-<RepoName>` per project against Q26's coordinators per scope.

## Strongest points

**OURS**
1. CLAY's own design needs `cd <checkout> &&` before every claim step because the orchestrator session sits in another repo, and marks whether `/sc:issue` keeps that directory "UNVERIFIED and ... the first local end-to-end check" (DESIGN line 136, ADD2). OURS starts in a worktree whose origin is the project and checks it before every launch (REQ R10; `dispatch.py` `_precheck`). CLAY's advocate conceded this point at 85 percent.
2. CLAY needs a hand-made clone of the orchestrator repo at an absolute path on each host (DESIGN lines 866, 893). On this host `/home/coder/workspaces/IronOrchestrator` does not exist and `orca repo list` does not show it, although the private repo exists on GitHub. REQ R17 says "Nothing in the setup is manual."
3. CLAY's registry and state files are git-ignored and host-local (DESIGN lines 863, 704) and the design falls back on a lease comment for two hosts (line 708, layer 4). OURS puts shared records on a branch with create-once claim files (Q26, proposal B). Related: the design's own header says "approved by the owner (Clay)" and defines "the user" as Clay (DESIGN lines 3 and 11), so its rulings (8 and 9, OD8) are not the repository owner's decisions on topology.

**CLAY**
1. A cap on work in flight exists in CLAY and nowhere in OURS: grep for `max_in_flight`, `in_flight` and `.dev/coordinators` in the owner's `src/superclaude/cli` finds nothing (CLAY advocate, Round 1); CLAY's rules are at DESIGN lines 700-702 and `route.py` `in_flight`. OURS answers a burst only with "one launch per sweep" (REQ R5), a rate brake.
2. Restart of a dead session with a resume wake, and its guards (an unreadable session list decides nothing; resume only for acknowledged work): DESIGN line 710 and `route.py` `end_finished` lines 562-603. The owner's `issue_watch/` has no `COORD-`, `wake`, `terminal` or `resume` string (probe INV-005, grep count 0).
3. A per-repo settings table (merge method, release branch, reviewers, role, safety files; DESIGN lines 879-889) for the work after the claim; OURS has no home for these keys. Also an org-wide search at about 8 calls against up to 65 (DESIGN line 137, observed once), though that gain is small at six repos.

## Clay strengths to adopt

- **In-flight cap with a fail-closed count.** Why: OURS has no cap (grep zero) and Clay's rules protect against a damaged file causing an extra start (DESIGN line 702). How: adopt as spec item 3 above, inside the child cycle, with the six safety properties from CLAY's rebuttal and the probe fixes INV-001, INV-002, INV-003, INV-008. Override: the cap is per coordinator id, not per repo, and nothing starts extra orchestrators.
- **Guarded restart with resume.** Why: fills the gap that Coder 516 says only "restart a stopped session" with no method. How: spec item 4, with guards from `route.py` `end_finished` and the probe fixes INV-005, INV-006. Override: no idle end.
- **Per-repo settings keys.** Why: the coordinator needs them at merge time and OURS has none. How: spec item 5, in the per-repo config, with the tamper fix INV-011. Override: the keys live in `issue-watch.d/<repo>.json`, not in a separate repo.
- **Exclusive-create state file per issue and the short-name check.** Why: exclusion on one host without the manual `reset`; fixes a real collision found by the probe (INV-009). How: spec item 7. Override: keyed on `owner/name`.
- **Org-wide search, optional.** Why: cheaper if the repo count grows. How: spec item 6, off in the first build, fail-open. Override: never the discovery gate.

## Our strengths that must be kept

- Project-local session, branch, worktree and records (OWNER-ANSWERS line 23; REQ R9, R10, R17).
- One cron entry, one dispatcher over `orca repo list`, per-repo config outside the project (REQ R16; `dispatch.py` 479 lines, built).
- A failed `orca repo list` is an error exit, not "zero repos" (REQ R15; `repos.py` `RepoListError`).
- Per-launch origin check (REQ R10, R13).
- Per-repo skip reasons that show "seen but not allowed" (`SKIP_REASONS`), per-repo day cap, rotation, one launch per sweep, first-run check leaving a failing repo `enabled: false` (REQ R5, R14, R18).
- Shared-branch create-once claim files as the cross-host lock (Q26), stated as design with its limit: it acts at push time.
- No manual setup (REQ R17).

## Actions

| Action | Type | Target | Order or dependency |
|--------|------|--------|---------------------|
| Replace the registry topology in the unified spec with the merged text | DOC | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/adversarial/merged-output.md` (source text for the spec) | First; feeds D14 |
| Rewrite sections 4.4, 5.7 and 6.2 of Clay's design (registry, `.orchestrator/`, orchestrator repo) to the project-local layout | DOC | `docs/designs/orchestrator.md` | After the owner accepts this verdict; owner decision on who edits |
| Keep the counting and restart rules of `route.py`, drop the registry and the orchestrator-repo paths | PR KEEP-ADAPT | PR 686 (the poll that wakes the orchestrator, open) | Final disposition belongs to D14; do not merge as is |
| Add the in-flight cap inside the child cycle, with a closing writer and expiry | LOCAL CHANGE | `src/superclaude/cli/issue_watch/cycle.py`, `record.py`, `dispatch.py` on branch `ironbelly/issue-watcher-zero-setup-plan` | After the closing-writer decision below |
| Design the closing writer and the expiry for "in flight" | DECISION | Owner (record in chat); `record.py` 448, 706-720 | Before the cap code |
| Add guarded restart with a store counter | LOCAL CHANGE | same branch | After the cap; needs session detection check (U25) |
| Key config, store and worktree on `owner/name`; add `name_collision` skip | LOCAL CHANGE | `generate.py`, `dispatch._config_path` | Independent |
| Separate claim worktrees from the standing coordinator's, or hold the cap at 1 | LOCAL CHANGE | `launch.py`, REQ R10 | Before the cap exceeds 1 |
| Decide the branch name and one-per-project against per-scope | DECISION | Owner; topic D08 | Before Coder 516 creates branches |
| Coder 515 (cron) and 516 (Coordinator branch, worktree, session) must land first | DECISION | Coder issues 515 and 516 | Before the dispatcher serves any repo |
| Leave `IronbellyOrg/IronOrchestrator` unused by the watcher; owner decides whether to keep it for the report session | DECISION | the private repo | Not blocking |

## Implications

- **Watcher.** The built dispatcher is the base. It serves no repo until Coder 516 creates the `Coordinator` worktree (`worktree_invalid`). PR 686's poll and the owner's dispatcher cannot both run; the rewrite of the same six files is the collision (analysis FULL-REPORT section 1).
- **Coordinator or orchestrator.** One standing coordinator per project, restartable under guards. `ORCH-IronClaude` holds the duties today (REQ R9), so a restart rule must not start a second duty holder.
- **Dashboard and report.** The org search and the cap add a skip reason `coordinator_full` that the sweep and observer should show; this is for D11.
- **Claim pipeline.** The worktree-sharing defect (INV-004) affects the claim procedure of Q26 ("no other unpushed commit"); it was in the owner's own plan and nobody had addressed it before this debate.
- **What breaks.** Clay's design 681 sections 4.4, 5.7 and 6.2, the `repo_not_listed` and `registry_invalid` reasons, and the wake `target` field assume the registry; they change. The "one orchestrator per repo" wording is replaced.
- **Owner must know.** (a) The owner decided direction, not layout or names (OWNER-ANSWERS line 23); the draft statement "the owner decided the topology" in OURS' paper is too strong. (b) The debate found a defect in the owner's plan (shared worktree). (c) The design's rulings 8 and 9 are Clay's (DESIGN lines 3 and 11), not the repository owner's.

## Confidence

80 percent. Raised by: both advocates agreeing on 23 of 24 points, CLAY's advocate conceding that no part of CLAY's topology still wins, and the code checks I made myself (dispatcher order, store states, worktree launch, tamper comment). Lowered by: the five HIGH probe findings stayed unaddressed at standard depth, the closing writer is not designed, and session detection is unproven on both sides. It would change if: the owner rules for a separate registry repo, a second host runs a poll, Coder 516 cannot create the worktree, or a test shows session detection by tag fails.

## Unverified

- States of Coder issues 515 and 516: I did not open them; the facts come from REQ quotes (`R6`, `R9`).
- Who issued rulings 8 and 9 beyond DESIGN lines 3, 11, 874 and 877 and analysis G-history line 42 (the DESIGN lines are long and my reads were partial).
- Session detection by ccsession tag or name (DESIGN U25) and the org search index delay (U8).
- That `/sc:issue` keeps the current directory across steps (DESIGN ADD2): this is CLAY's own unverified premise, not tested here.
- The measured 22.5 to 27.1 s start time applies to the ccsession path; the Orca launch route is UNVERIFIED (probe INV-006).
- `WORKTREES_DIR` literal against Orca's default location on another host layout (probe INV-012 falsifier 5, from code reading only).
- The probe findings rest on code reading; no test was run. Four of them I spot-checked: INV-001, INV-002, INV-004, INV-011.
- Process note: to check that the private orchestrator repo exists I made two read-only GitHub calls that name `IronbellyOrg/IronOrchestrator` (one failed on an unsupported flag, one `gh api repos/IronbellyOrg/IronOrchestrator` returned `private: true`). The brief asks that `gh api` paths spell `repos/IronbellyOrg/IronClaude/...`; these two did not. Nothing was written, and nothing touched SuperClaude-Org.
- The adversarial skill ran in full (nested advocates, fault-finder, independent scoring pass, merge-executor). Standard depth has no third round, so convergence is formally BLOCKED_BY_INVARIANTS and the return contract status is `partial`.

## Debate artifacts

- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/adversarial/merged-output.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/adversarial/return-contract.yaml`
- In `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/adversarial/adversarial/`: `diff-analysis.md`, `debate-transcript.md`, `round-1-advocate-1-OURS.md`, `round-1-advocate-2-CLAY.md`, `round-2-rebuttal-1-OURS.md`, `round-2-rebuttal-2-CLAY.md`, `invariant-probe.md`, `scoring-pass-2.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`, `variant-1-original.md`, `variant-2-original.md`
