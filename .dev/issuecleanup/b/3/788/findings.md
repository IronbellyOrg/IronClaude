# #788 (C7) round 2: Worker start: Task, worker-start, issue link, Dispatch id, worktree check, unknown-outcome handling

Checked against master f2894fc44 (2026-11-24). Round 1: /home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/3/788/findings.md. Static run (Command line): /home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/3/analyze/analyze-report.md (target `src/superclaude/cli/issue_pipeline`, architecture, quick). Plan files read read-only from /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/; owner records R36 to R38 from /home/coder/workspaces/worktrees/IronClaude/Realign/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md.

## Alignment with architectural decisions
Searched DECISIONS.md, SPEC.md, the VERDICT files D03, D07, D15, QG1, the owner records R36 to R38 and WORKER-CONTRACT.md. Verdicts:

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`), part C (one standing coordinator per project): ALIGNED. The coordinator starts workers: `WORKER-CONTRACT.md:71` ("plans, creates Tasks, starts workers") and `:299` (worktree, then `worker-start`).
- **R38, general sentence** ("no element of Clay's orchestrator design ... is adopted"; it "supersedes the 'Clay strengths adopted' rows of the unification spec"): IN CONFLICT on the record name. The per-issue file `issues/<repo-key>__<N>.json` (SPEC.md:231, FR-29) comes from D07 item 7 (`DECISIONS.md:330`, "exclusive-create state file per issue") and D15 row C4 (`DECISIONS.md:579`, "adopt with change"); both are Clay strengths. R38's part C list (registry, cap, idle end, wake file, tier keys, report, merge gate, flags) does not name the file, so the owner has not ruled on it by name. Master keeps the owner-built adoption row: `approval_record.py:235` (`adopt_create`), `:268` (`adopt_mark`), contract `:298`.
- **#716 backlog review, 2026-11-24, next step 2**: "Keep the existing claim/store path as the baseline rather than adding a competing state store". IN CONFLICT with a new per-issue file and with S06-F9 (`orca reference add/find` as a second store).
- **SPEC FR-29 and FR-84** (SPEC.md:231, :244; the adoption row "not kept"): PARTLY ALIGNED. They were written before R38; master (after PR 700, `DECISIONS.md:21`) still has the rows and `WORKER-CONTRACT.md:298` still names `adopt-create`. R38 voids the Clay-derived rows, so the plan text is stale here and master stands.
- **WC-8 and WC-13** (`WORKER-CONTRACT.md:40`, `:63`): ALIGNED. A worker never calls `worker-start`; only the coordinator session does. The issue's own watch-out is correct on this. Its other watch-out line (only a person-opened coordinator may run it) and **FR-27** (SPEC.md:229) are IN CONFLICT with master after PR 736 (`WORKER-CONTRACT.md:71`): stale, master wins.
- **WC-6** (`WORKER-CONTRACT.md:75`, `:78`) and the duty at `:298` ("Never start again for an `uncertain` row: settle it by reading `worker-list`"): PARTLY ALIGNED, and this is new since round 1. S02-F25 asks `request-show` once, then a retry with the same request id. `request-show` is read-only (its `--help` note), so asking is allowed. `--retry-request` is a different flag from `--retry-of` (both in `orca orchestration worker-start --help`), so WC-6's ban on `--retry-of` does not name it. But a retry is a "start again" for an uncertain row, which `:298` forbids, and `:78` says "No retry while the earlier attempt is not settled or reads unverifiable". The contract needs an explicit amendment first. UNVERIFIED: what Orca does when `--retry-request` replays a request.
- **FR-21** (SPEC.md:211, "an unknown launch receipt never relaunches"): PARTLY ALIGNED; same answer, a same-id replay is not a relaunch only if Orca treats it as the same request (UNVERIFIED).
- **Project CLAUDE.md, Orca paragraph** (`/home/coder/workspaces/worktrees/IronClaude/Realign/CLAUDE.md:54` and `:313`: no Orca link flags such as `--issue` and `--pr` for this repo until the project id is the fork's): S06-F9 is IN CONFLICT as worded, because `orca reference add` attaches an issue URL to a worktree and is a link operation. Orca still reports the upstream project id (open #780). UNVERIFIED whether `reference add` resolves through that id.
- **D07 item 8** (`DECISIONS.md:331`, one live agent per worktree) and the Orca rule that every worktree gets an agent: ALIGNED with S06-F10 (`worktree ps` before start).
- **SEC-16** (SPEC.md:305, no GitHub text in a typed line) and `brief.py:1-10`: ALIGNED if `--task` is filled from `brief.build`, which holds closed slots only. UNVERIFIED how the coordinator reaches `brief.build`: it has no CLI verb and no production caller (analyze report, finding 1).
- **Contract status-to-command table** (`WORKER-CONTRACT.md:297`): ALIGNED; C7 starts only research, spec, plan and debug workers.

## Complementary issues
- **#786 (C5, Run lifecycle)**: C7 completes it, C5 enables C7. A `worker-start` fails with `consumer_fenced` unless the coordinator is bound to the Run (observed in #755). Interface: the Run id that #755 decides, stored in the same record as the Dispatch id.
- **#782 (C1), #785 (C4), #787 (C6)**: the skill skeleton, the Orca guide load and the per-step verb list; C7's steps live in that skeleton.
- **#770 (watcher hands each claim to the coordinator)**: supplies the trigger. Nothing tells the coordinator a claim exists today, so C7 has no start event until #770 lands (R38 closed the wake-file route, #796).
- **#800 (C19)**: settles what C7 starts; reads the Dispatch id C7 stores.
- **#789 (C8)** stores `body_sha` in C7's record; **#790 (C9)** builds the brief C7 passes to `--spec` or `--task`; **#792 (C11)** validates the `worker_done` that C7's Dispatch later sends.
- **#699 (claim script makes the worktree without an agent)**: the step right before `worker-start`; S06-F10 is a guard for the same one-live-agent-per-worktree problem.
- **#819 (W11)**: the same Orca operation-id retry for the watcher's launch; the retry form should be decided once for both.
- **#780**: blocks S06-F9. **#771** follows C7 (finish). **#755** decides the Run rule C7's record must hold.

## Closest overlap
**#786 (C5: Orca Run lifecycle: create once, rebind after a restart).**

Shared: restart safety. C5's second check ("kills the coordinator mid-issue, resumes it ... no second claim, no second worker") overlaps C7's third check (after a restart no second worktree or worker); both need the Run id in the record and both sit behind `consumer_fenced`. Estimate: about 25% of #788's done-when (the restart half of one of its three checks, reached through Run state instead of `orca reference find`). C5 does not cover the fixture start (check 1) or the unknown-outcome path (check 2).

Next two: **#819 (W11)**, about 15%: same Orca operation-id retry idea as check 2, but for the watcher's launch, a different caller. **#699**, about 10%: the one-live-agent-per-worktree concern behind S06-F10; it is a design question, not a done-when check.

## Standalone or merge
**Verdict: stand alone.** Tested against #786:

- **Owner**: same (the coordinator skill, one owner ruling needed for the record name). Not a reason to merge or split.
- **Acceptance test**: different. C5 passes when `run-current` shows the same Run and the next `worker-start` is not fenced. C7 passes on a fixture start (Task, Dispatch `ready`, record), a fault-injected unknown outcome (never two Dispatches, an escalation entry on the second failure) and a record-based restart.
- **Files touched**: C5 touches the Run-lifecycle step and one Run id field; C7 touches the start step, the adoption record, calls to `request-show` and `worktree ps`, and needs a fake Orca runner for fault injection.
- **Build phase**: both are in the Phase 2 cluster (#716 closing review, point 2), built together, but C5 goes first because `worker-start` fails without it.
- **Risk if merged**: one XL item would mix two open owner decisions (the Run rule in #755 and the record name) and bury the unknown-outcome path, the worst failure (two agents in one worktree), inside a larger review.

Merging would be right in one direction only: if the owner settles #755 as "one Run per project", C5 shrinks to two verbs (`run-current`, `run-use`) and should merge into C7 as its first step. C7 should not merge into C5.

## Closed issues and merged PRs checked
- **PR #584** (merged 2026-11-17): adds the adoption rows (`adopt-create`, `adopt-mark`), the `uncertain` state and `brief.py`. Delivers the "no second Dispatch" and "Dispatch id stored" parts of C7's done-when, in the adoption row and not in `issues/<repo-key>__<N>.json` (test `tests/issue_pipeline/test_approval_crash.py:45`, a kill between `worker-start` and `adopt-mark` blocks a second start).
- **PR #591** (merged 2026-11-17): adds the coordinator duties at `WORKER-CONTRACT.md:296-303` (reserve before starting, worktree then worker), WC-17 and the launch guard G2. Delivers the start procedure as prose.
- **PR #701** (merged 2026-11-20): re-applies the no `--to` duty and rewords the worktree-then-worker duty. No change to C7's scope.
- **PR #449** (merged 2026-11-08): a hook requires `--agent` on every worktree create; the claim script keeps no `--agent` on purpose (owner-approved). Context for S06-F10 and #699.
- **PR #736** (merged 2026-11-23): a coordinator need not be person-opened. Contradicts the issue's watch-out and SPEC FR-27.
- **PR #707** (merged 2026-11-20): the watcher launches the claim agent; no coordinator start. **PR #693 and issue #691** (completed 2026-11-21): `launch-result.json` of the claim launch; a different launch from the coordinator's `worker-start`, delivers nothing for C7.
- **#796 (C15)**: closed not planned 2026-11-24, because R38 rejects the wake file and the plan check. **#806 (C25)**: merged into #782 the same day; C7's tests stay its own. **#809 (W1)**: merged into #716.
- **#507** (completed 2026-11-11): `--unattended` and one report directory on every worker `Command:` line; already applies to the brief rows C7 passes. **#450** (completed 2026-11-24): watcher rollout; delivers nothing for C7.

## Updated recommendation
- **Action**: keep open with changes. (1) Replace `issues/<repo-key>__<N>.json` with the adoption row on master (`adopt_mark started` with the Dispatch id, `approval_record.py:268`), until the owner rules otherwise by name (R38 and the #716 review point that way). (2) Park S06-F9 (`orca reference add/find`) until #780 is fixed and the owner rules whether `reference add` is a link flag. (3) For S02-F25, say that the retry is `--retry-request` with the same id after one `request-show`, amend `WORKER-CONTRACT.md:298` and the WC-6 wording at `:78` in the same change, and prove Orca's replay behaviour live first. (4) Delete the stale watch-out about a person-opened coordinator (PR #736). (5) State whether `--task` is wanted at all: the contract's `--spec` route works today. (6) Name #770 as its trigger.
- **Priority**: P2, unchanged from round 1.
- **Complexity and size**: complex, M. Changed from round 1 (complex, L): the record already exists on master and S06-F9 is parked, so what is left is two contract steps (`request-show`, `worktree ps`), the skill step and fault-injection tests. Complex stays because of the fault injection and the live Orca check.
- **What is new since round 1**: the direct conflict with the duty at `WORKER-CONTRACT.md:298` and WC-6 `:78`; R38's general sentence and the #716 review point as the reason the record name conflicts; #796, #804 and #806 closed or merged by the owner on 2026-11-24.

## Scan record
- Lists read in full (titles; the closed list with its state column): open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Title search terms: worker, start, Run, orca, dispatch, adopt, coordinator, handoff, brief, worktree, claim, launch, retry, unknown, restart, state, record, closeout, watcher, unattended.
- Opened with `gh issue view` / `gh pr view` (bodies read to their first 1500 to 1900 characters, C-items from their `###` heading; text beyond that is UNVERIFIED): open 786, 755, 819, 699, 770, 771, 800, 780, 792, 782, 785, 761, 777, 773, 446 (15); closed 796, 806, 809, 691, 507, 450 (6); merged PRs 584, 591, 449, 693, 736, 701, 707 (7). Also read: #788 and #716 (body, closing review, all 5 comments); comments of #796, #798, #804, #806, #809.
- Not opened with gh: PR #700 (read through `DECISIONS.md:5-39` and the #716 review), #655, #665, #444.
- Master check: Command line `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/3/analyze`, succeeded; Orca flags checked by `--help` only (`worker-start`, `request-show`, `reference add`, `worktree ps`), nothing run. Live Orca behaviour of `--retry-request` and `reference add` is UNVERIFIED.
