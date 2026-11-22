# Inventory: Clay's pull requests against the owner's work

Read-only inventory, written 2026-11-20 (UTC). "Clay" is the GitHub account `clayphi` (they/them). "Owner" is the account `ironbelly` (the repository owner; note that sessions on this host also act under that login, so a GitHub action under it does not show which person acted). All GitHub reads used `gh ... --repo IronbellyOrg/IronClaude` or `repos/IronbellyOrg/IronClaude/...`. Nothing was written to GitHub or to the repository, except this file.

Sections (filled in order):

1. Scope and method
2. Table 1: every clayphi PR in scope
3. Clay branches with no PR
4. What changed on PR 686 since 4e7f12b1a
5. Table 2: the owner's own recent related work
6. Preliminary dispositions
7. Not verified

## 1. Scope and method

- Source of the PR list: `gh pr list --repo IronbellyOrg/IronClaude --author clayphi --state all` (84 PRs since 2026-06). In scope: every one that is open, or was merged or closed on or after 2026-11-10 (UTC), plus any older one touching the watcher, issue pipeline, orchestrator/coordinator, observer/dashboard, `/sc:issue`, worker contract, sweep or work reports.
- File counts and paths come from `gh api repos/IronbellyOrg/IronClaude/pulls/N/files --paginate` (every page), not from the PR text.
- Older PRs (June to 2026-11-09, 39 of them checked by file path): none touches `issue_watch`, `issue_pipeline`, orchestrator, observe, sweep, `WORKER-CONTRACT.md`, `sc-issue-protocol` or the launch guard. Two are adjacent only: #285 and #287 (pr-submit, which the design of #681 reuses). No older PR is in the table.
- One PR that is NOT by Clay but was merged by Clay: #664 (release 6.1.0 re-merge, authored by `ironbelly`, merged by `clayphi` 2026-11-19 01:47Z, 181 files) after the owner reverted the mistaken squash merge #658 with #662. Listed in the notes under table 1.
- "Merged by" shows the GitHub login. Sessions on this host also act as `ironbelly`, so a merge by `ironbelly` does not prove the person looked at it. Where the owner's own hand is established elsewhere (for example the #571 thread) I say so.
- Dispositions are PRELIMINARY. A conflict is only named where a file, PR, issue or ledger line shows it.

Corrections to the brief:

1. `clayphi/issue-655-pr-p`, `-pr-c`, `-pr-d` and `-spec-pr` all HAVE pull requests: #690 (open), #684, #682 and #681 (merged 2026-11-20). The only Clay branch of the recent set with no PR at all is `clayphi/v61-part-b-map` (see section 3).
2. Per-PR sizes below differ slightly from FULL-REPORT.md for #686: the head moved from `4e7f12b1a` to `8e5ae29ad` (+50 added lines net, still 59 files).

## 2. Table 1: every clayphi PR in scope

Legend. Disposition: KEEP = nothing found that conflicts with owner work, leave as is. KEEP-ADAPT = keep, but change or re-point something named in the row. REVERT-CANDIDATE = deletes or replaces owner work with evidence of a conflict; the owner should rule on a revert or a restore. NEEDS-DEBATE = cannot be settled without an owner ruling on a named question. Owner-work status: COMPLETE = merged; IN PROGRESS = open PR, open issue with a live worktree or branch, or local uncommitted plan; NONE = no owner work found.

### 2A. Watcher, pipeline, orchestrator, worker contract (the area of PR 686)

| PR and title | State, date (UTC), merged by | Size and main paths | Owner work it relates to, and its status | Relation | Evidence | Preliminary disposition |
|---|---|---|---|---|---|---|
| #686 feat(issue-watch): the poll wakes the repo's orchestrator (issue 655, PR A) | OPEN. Opened 2026-11-20 00:25Z. Head `8e5ae29ad`. All 6 CI checks pass, mergeable CLEAN. Reviews: bots and Clay only, no owner review. | 59 files, +14,306/-16,637. `src/superclaude/cli/issue_watch/` (new files `hold.py`, `repos.py`, `route.py`, `wake.py` and their tests; edits to `audit.py`, `cli.py`, `cycle.py`, `github.py`, `launch.py`, `predicates.py`, `record.py`), `tests/issue_watch/` (25 fixtures). | Issue watcher #447/#448 (COMPLETE, merged 11-08, `enabled:false`, never live); rollout issue #450 (open, assigned `ironbelly`); zero-setup watcher plan in worktree `claim-handoff-planb` (IN PROGRESS, unpushed, see table 2). | Replaces the claim-session launch, approval, trigger and Project reads of #447; extends (reuses runner, audit log, lock, call budget). | `gh pr view 686`; `git diff --stat`; FULL-REPORT.md sections 2 and 5; conflicts in H-design681-map.md. | NEEDS-DEBATE. Two rulings are needed first: trigger and approval gate (assignment only, against the `Approved` field), and scheduler (Orca automation, against cron). The registry, hold, audit and wake pieces look reusable (KEEP-ADAPT) once those are decided. |
| #690 feat(issue): /sc:issue --plan and --remaining (issue 655, PR P) | OPEN. Opened 2026-11-20 00:57Z. Head `f3bc77981`. CI 6 of 6 pass, mergeable CLEAN. Bot reviews only. | 13 files, +2,811/-39. `skills/sc-issue-protocol` (SKILL.md, new `refs/plan.md`, `refs/tiers.md`, new `scripts/plan_body.py`), `agents/issue-worker-t1..t3`, `commands/issue.md`, `docs/user-guide/`. | `/sc:issue` claim and create (#373, #425, #486, #636: COMPLETE); plan sections in templates (#661: COMPLETE); issue #689 (open, Clay's: renames `## Fix approach`). | Extends. Adds a third mode; claim chain not edited. | `git diff` file list; PR body ("one edit of the issue body and nothing else"). | KEEP-ADAPT. Heading names must agree with `hold.py` in #686, which accepts only `## Fix approach`, while #689 would rename it (B-open-issues.md). |
| #684 feat(agent-work-report): move the report skill into IronClaude and add the living report (issue 655, PR C) | MERGED 2026-11-20 02:01Z by clayphi. No human review. | 28 files, +10,488. `skills/agent-work-report/` (25 files), `tests/skills/test_agent_work_report.py`, +8 lines in `tests/skills/test_worker_contract.py`. | `/sc:sweep` #539 and observer `superclaude observe` #503/#514/#577/#673 (all COMPLETE, merged); dashboard issue #409 (open; now assigned to `clayphi`). Neither is named in #684. | Independent in code (no shared files). Overlaps in purpose: both show what sessions are doing. | PR body; no `sweep` or `observe` path in the file list. | KEEP-ADAPT. Fold the report into sweep and observer, or state in one place which one answers what. The skill reads `orchestrator_repo` of `~/.config/superclaude/issue-watch.json`, so it is coupled to the #686 design. |
| #683 feat(closeout): add /sc:closeout and the sc-closeout-protocol skill (issue 668) | MERGED 2026-11-20 01:16Z by clayphi (opened 2026-11-19 23:07Z). Bot reviews and Clay's own comments only. | 27 files, +6,889/-6. `skills/sc-closeout-protocol/` (13 files), `commands/closeout.md`, `docs/designs/sc-closeout.md`, `core/WORKER-CONTRACT.md` (one list entry: adds `/sc:closeout` to the never-as-worker list), `NOTICE`. | Owner issue #339 lists a `sc:close` session-close duty (not built); no owner PR for PR or issue close. Status: NONE built. | Independent / extends. Adds a command; edits one list in the worker contract. | `git diff 8b2ce556c~1 8b2ce556c -- WORKER-CONTRACT.md` shows one-line list change. | KEEP. Check the name against #339's `sc:close` before the next release. |
| #682 refactor: retire the old plan-approval gate (issue 655, PR D) | MERGED 2026-11-20 00:02Z by clayphi, about 66 minutes after opening (opened 2026-11-19 22:56Z; merged 00:02:36Z). Only a bot review (augmentcode). | 36 files, +35/-4,599. Deletes `cli/issue_pipeline/` (about 1,600 lines), `tests/issue_pipeline/`, `tests/cli/test_issue_pipeline_registered.py`; edits `core/WORKER-CONTRACT.md` (WC-17 and section "Issue pipeline duties" removed), `launch-level-guard.sh` (rule G2.1 removed), `cli/main.py`, CHANGELOG, tech reference. | Owner PRs #584 (Plan A) and #591 (Plan B), merged 2026-11-17, COMPLETE; they implement owner Decision 6 = B and Q35 to Q41 (E-pr682.md). Owner worktree `claim-handoff-planb` extends `issue_pipeline/` (IN PROGRESS, 52 modified files, several under `issue_pipeline/`). | DELETES. | Merge commit `01e7a9e23`; `gh api .../pulls/682/files`; `git status` in planb shows modified `issue_pipeline/brief.py`, `cli.py`, `reads.py`; PR body: "Nothing runs this code ... `enabled: false`". Neither the PR nor #655 names #584, #591 or Decision 6. | REVERT-CANDIDATE. Reason in a few words: removes merged owner work and a recorded decision with no owner review, and the owner's next plan builds on the removed package. Counter-point: the code never ran live. Not an automatic revert; the owner decides between a revert and restoring the package in a new PR. |
| #681 docs(design): approved orchestrator design for issue 655 (docs only) | MERGED 2026-11-20 00:02Z by clayphi. No human review. | 1 file, +1,412: `docs/designs/orchestrator.md`. | Owner decisions in the zero-setup plan (R1, R6, R9, R16, R19, R22, R23, R35, R36), owner PRs #587 to #589 (alignment, merged 11-17), #339, #444 (open). | Independent as code (docs only). In substance it replaces the owner design of the watcher and sets rules the owner's contract does not allow. | H-design681-map.md and FULL-REPORT.md section 5 (ten conflict rows). The design says "approved by the owner (Clay)". | NEEDS-DEBATE. Docs only, so an amendment is cheap. The question is who rules on the ten rows. |
| #661 feat(sc-issue): require Priority, Fix approach and Test plan in every issue template | MERGED 2026-11-19 01:29Z by ironbelly. | 12 files, +307/-61. `sc-issue-protocol` templates and `refs/create.md`, `agents/issue-worker-*`, `docs/designs/sc-issue-command.md`, 2 tests. | Owner `/sc:issue` (#373, #486, #509: COMPLETE). | Extends. | PR file list. | KEEP. The plan headings it adds feed the hold check in #686. |
| #670 feat(scripts): opt-in daily log of merged pull requests per person (#669) | MERGED 2026-11-19 19:16Z by ironbelly. | 38 files, +2,573. `scripts/merged_pr_log*` (+ Orca automation note), `tests/merged_pr_log/`. | None found (body says unrelated to report or orchestrator). | Independent. | PR file list. | KEEP. |
| #499 fix(pr-submit): name an Augment review whose status marker is unreadable instead of polling silently (#382, #456) | MERGED 2026-11-11 16:20Z by ironbelly. | 57 files, +3,561/-11. `src/superclaude/pr_submit/` (3), `skills/` (4), `tests/pr_submit/`, `.dev/issues/381-382-456/` (44). | Owner `/sc:pr-submit` work (#378, #424, #428: COMPLETE). The #681 design reuses the pr-submit poll scripts. | Extends. | PR file list. | KEEP. |

Notes on 2A.
- Reviews: none of #681, #682, #683, #684, #686, #690 has a review or comment by `ironbelly` on GitHub (gh `reviews` list read for each; FULL-REPORT.md section 1 point 7 says the same for comments). That is not proof the owner did not see them elsewhere (chat), UNVERIFIED.
- PR B (the orchestrator skill) and PR E (live test) of the #655 plan do not exist: no open or merged PR and no `origin/clayphi/issue-655-pr-b` or `-pr-e` branch. Open PRs in the whole repo are only #685 (owner's #442 runbook docs), #686 and #690.

### 2B. The 6.0.0 and 6.1.0 removal and release PRs (all authored by Clay; all targeted `integration` unless noted)

Common facts for this block. Plan and thread: issue #571 (open, Clay's, "Release 6.0.0 ... plan for review"). The owner's recorded approval in that thread (comment of 2026-11-17 07:27Z) covers wave 1 only (#615, #616, #617: the prd CLI, the cleanup-audit runner, `/sc:spawn`). The owner also removed swarm from the removal list (2026-11-17 13:06Z, so Clay dropped PR 3). I found no recorded owner approval of waves 2 to 6 or of the 6.1.0 bundle in the comments read (comment texts were read from the first 380 to 420 characters for most; so UNVERIFIED, not "absent"). Owner PR #613 (merged 2026-11-17 20:35Z, "stop recommending /sc:task") agrees in direction with #650, #653, #656. None of these PRs touches `issue_watch`, `issue_pipeline`, `sweep`, `observe` or the launch guard; the watcher-area paths they do touch are `core/WORKER-CONTRACT.md` (command names dropped from lists), `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` and, in #632 and #639, `skills/sc-issue-protocol/refs/chains.md` and `refs/claim.md` (references to removed commands). Related owner work for all of them: the unattended worker contract for 16 and 15 commands (#411, #422, COMPLETE), which these removals narrow by deleting those commands.

| PR and title | State, date (UTC), merged by | Size and main paths | Relation | Preliminary disposition |
|---|---|---|---|---|
| #615 refactor(cli): remove the cleanup-audit headless runner (6.0.0) | MERGED 2026-11-17 20:25Z, clayphi | 72 files, +555/-2,140. `cli/cleanup_audit` | Deletes a command family; owner approved (wave 1). | KEEP |
| #616 refactor(cli): remove the prd command-line pipeline (6.0.0) | MERGED 2026-11-17 20:41Z, clayphi | 75 files, +770/-10,969. `cli/prd`, `tests/cli/prd` | Deletes; owner approved (wave 1). A file named `sweep-edits.yaml` appears in its list (name match only, a review-severity fixture, not the Orca sweep). | KEEP |
| #617 refactor(commands): remove /sc:spawn (6.0.0) | MERGED 2026-11-17 20:49Z, clayphi | 51 files, +434/-515. commands, `core/WORKER-CONTRACT.md`, tech reference | Deletes; owner approved (wave 1). Narrows owner contract lists. | KEEP |
| #620 refactor(commands): remove /sc:save and /sc:load (6.0.0) | MERGED 2026-11-17 21:38Z, clayphi | 53 files, +449/-868 | Deletes; approval UNVERIFIED. | KEEP (confirm approval) |
| #621 refactor(commands): remove /sc:review-translation, moved to the snapshot fork (6.0.0) | MERGED 2026-11-17 21:50Z, clayphi | 38 files, +539/-1,069 | Deletes; the owner said the destination can be their fork (#571 comment 2026-11-17 18:32Z), so the move is on record as wanted. | KEEP |
| #622 refactor(commands): remove /sc:build (6.0.0) | MERGED 2026-11-17 22:16Z, clayphi | 55 files, +494/-452 | Deletes; approval UNVERIFIED. | KEEP (confirm approval) |
| #625 fix(ic): launcher alias, preset and help fixes (6.0.0) | MERGED 2026-11-17 22:57Z, clayphi | 18 files, +1,113/-11. `cli` (1), `scripts` (1), tests | Independent. | KEEP |
| #626 fix(help): correct help text and messages (6.0.0) | MERGED 2026-11-17 22:56Z, clayphi | 44 files, +646/-68. commands, `cli` (3) | Independent. | KEEP |
| #627 refactor(commands): remove /sc:improve (6.0.0) | MERGED 2026-11-17 23:52Z, clayphi | 73 files, +628/-613 | Deletes; approval UNVERIFIED. | KEEP (confirm approval) |
| #629 refactor(cli): remove cli-portify (6.0.0) | MERGED 2026-11-18 00:25Z, clayphi | 123 files, +517/-23,663. `cli/cli_portify` (31 files), skills, `scripts` | Deletes; approval UNVERIFIED. | KEEP (confirm approval) |
| #631 refactor(commands): remove /sc:index and /sc:index-repo (6.0.0) | MERGED 2026-11-18 01:22Z, clayphi | 61 files, +833/-991 | Deletes; approval UNVERIFIED. | KEEP (confirm approval) |
| #632 refactor(cli): remove the roadmap, tasklist and sprint family (6.0.0) | MERGED 2026-11-18 02:05Z, clayphi | 605 files, +2,487/-148,187. `cli` (134), `tests/roadmap`, skills (37), `tests/sprint` | Deletes the largest family. `sc-issue-protocol/refs/chains.md` edited. `issue_watch/record.py` uses `swarm.atomic`, which stays. Approval UNVERIFIED. | KEEP (confirm approval) |
| #633 feat(install): retire commands and skills that 6.0.0 no longer ships (6.0.0) | MERGED 2026-11-18 03:08Z, clayphi | 24 files, +1,744/-17. `cli` (3), docs | Extends the installer (owner installer work #419, #480 COMPLETE). | KEEP |
| #634 chore(release): 6.0.0 version, changelog and release notes | MERGED 2026-11-18 14:50Z, clayphi | 37 files, +2,714/-14. `.dev/releases/current` (31), CHANGELOG, `pyproject.toml`, `tests/observe/golden_release1_surface.json` (version string) | Independent. | KEEP |
| #639 chore(release): merge master into integration for 6.0.0 (resolve the routing-guide conflict) | MERGED 2026-11-18 15:46Z, clayphi | 101 files, +5,065/-98. Merge of master; carries `sc-issue-protocol` files from master | Independent (a merge). | KEEP |
| #640 release: 6.0.0 (removals, retire step, eight fixes), base `master` | MERGED 2026-11-18 16:30Z, clayphi | 1,146 files, +13,671/-189,325 | The release of all the above. Merge commit `3f3b34a26`, tag `v6.0.0` (per #571 comment). | KEEP (covered by the rows above) |
| #646 fix(install): stop filecmp from returning a stale "identical" answer | MERGED 2026-11-18 17:11Z, clayphi | 3 files, +42/-10. `cli` (2) | Extends the installer (owner #419). | KEEP |
| #649 docs: post-release sync and install runs for 6.0.0 | MERGED 2026-11-18 18:31Z, clayphi | 27 files, +4,849/-115. `docs/testing/v6.0.0` (6) | Independent. | KEEP |
| #650 refactor(skills): remove the prd, tdd, tech-research, tech-reference, operational-guide and readme skills and /sc:tdd (6.1.0) | MERGED 2026-11-18 21:17Z, clayphi | 76 files, +1,070/-13,954. skills (26), `plugins/` (6) | Deletes; the owner reversed one item of this plan (swarm) but no approval of Part B found. UNVERIFIED. | KEEP (confirm approval) |
| #652 refactor(commands): remove /sc:task and /sc:validate-tests with their skills (6.1.0) | CLOSED 2026-11-18 19:55Z, not merged | 44 files, +179/-2,437. Base was `clayphi/v61-pr1-doc-skills` | Withdrawn when "Ryan's list" could not be verified (F-clay-inventory.md). | KEEP (nothing to do; closed) |
| #653 refactor(routes): re-point every task-file route to /sc:workflow then /sc:implement (6.1.0) | MERGED 2026-11-18 21:31Z, clayphi | 45 files, +591/-784. skills (17), `tests/cli/reflect`, `sc-issue-protocol/refs/chains.md` | Edits wording in the owner's claim chains (`sc-issue-protocol/refs/chains.md`, also edited by #632). Consistent with owner PR #613. | KEEP |
| #656 refactor(skills): remove the task, task-builder and roadmap skills and level 4 of the routing guide (6.1.0) | MERGED 2026-11-18 21:56Z, clayphi | 78 files, +229/-14,068 | Deletes the MDTM executors and level 4 of `HOW-WE-WORK.md` (owner's routing guide, merged #265). | KEEP (confirm approval) |
| #657 chore(release): 6.1.0 version, changelog, release notes and upgrade guide | MERGED 2026-11-18 22:16Z, clayphi | 7 files, +257/-15 | Independent. | KEEP |
| #658 release: 6.1.0 (task and documentation bundle removed, ccsession agent sessions), base `master` | MERGED 2026-11-18 22:33Z by ironbelly (a squash merge by mistake, per F-clay-inventory.md) | 181 files, +6,918/-28,826 | Reverted by the owner's #662 (2026-11-19 01:20Z), then re-merged as #664. | KEEP (settled by #662 and #664) |
| #659 docs(install): say the installer raises cleanupPeriodDays to 90, not 365 | MERGED 2026-11-18 22:53Z, clayphi | 2 files, +12/-10 | Independent. | KEEP |
| #663 chore(release): merge master (6.1.0 squash) into integration | CLOSED 2026-11-19 01:24Z, not merged | 0 files | Independent. | KEEP (closed, empty) |
| #667 docs: post-release sync and install runs for 6.1.0 | MERGED 2026-11-19 03:35Z, clayphi, into `integration` only (`integration` is 2 commits ahead of master, so this is NOT on master yet) | 25 files, +5,026/-108. `docs/testing/v6.1.0` (6) | Independent. | KEEP |

Note: #664 (not by Clay): "release: 6.1.0 ..." authored by `ironbelly`, merged by `clayphi` 2026-11-19 01:47Z, 181 files. Listed for completeness; disposition KEEP.

### 2C. ccsession, docs, help and styles (no watcher area)

| PR and title | State, date (UTC), merged by | Size and main paths | Related owner work | Relation | Preliminary disposition |
|---|---|---|---|---|---|
| #481 fix(ccsession): retry server errors then switch, including named models (#392) | MERGED 2026-11-10 02:38Z, ironbelly | 77 files, +6,652/-58. 71 files in `.dev/issues/392`, 4 skills files | Owner ccsession tiers (#416, #493, #518: COMPLETE). | Extends. | KEEP |
| #494 docs(testing): fix the Part 4 upgrade-survey check in leandro.md (#354) | MERGED 2026-11-11 14:49Z, clayphi | 1 file, +4/-2. `docs/testing/v5.0.0` | Owner post-release #353 (COMPLETE). | Extends. | KEEP |
| #570 fix(ccsession): head lists with the repo name, keep named sessions for a year | MERGED 2026-11-16 18:13Z, clayphi | 9 files, +936/-11. `skills/ccsession-tag` (5), `cli` (1), CHANGELOG, 2 tests | Owner #350 (session list follows the worktree: COMPLETE). | Extends. | KEEP |
| #608 docs(style): define plain English and give the wrap-up a fixed five-part body | MERGED 2026-11-18 03:34Z, ironbelly | 3 files, +97/-12. `output-styles` (1), `tests/commands/test_pragmatic_plain_english.py`, `tests/commands/test_sweep_command.py` (one test file, edit not read) | Owner sweep command #539 (COMPLETE); only a test file touched. | Independent. | KEEP |
| #619 docs(how-we-work): drop built-in and local review steps from the shipping flow | MERGED 2026-11-18 03:34Z, ironbelly | 4 files, +22/-35. `core/HOW-WE-WORK.md`, onboarding deck, one test | Owner routing guide #265 (COMPLETE). | Extends. | KEEP |
| #628 perf(ccsession): build the saved-session list without a process per saved name (#607, stage 1) | MERGED 2026-11-18 03:31Z, ironbelly | 11 files, +819/-12 | Owner #350. | Extends. | KEEP |
| #630 perf(ccsession): find every transcript and start folder of the worktree list in one process (#607, stage 2) | MERGED 2026-11-18 03:33Z, ironbelly | 6 files, +647/-17 | Owner #350. | Extends. | KEEP |
| #641 feat(ccsession): tell human-saved sessions from agent-saved ones and keep them for different times | MERGED 2026-11-18 20:59Z, clayphi | 20 files, +4,463/-72. skills (8), `.dev/specs`, CHANGELOG | Owner ccsession work (#386 agents at the name prompt: COMPLETE). | Extends. | KEEP |
| #666 feat(ccsession): ask for a typed confirmation before --prune --apply deletes | MERGED 2026-11-19 19:15Z, ironbelly | 7 files, +382/-16 | Owner ccsession. | Extends. | KEEP |

## 3. Clay's branches on origin, with and without a PR

There are 24 branches named `origin/clayphi/*`, plus `origin/integration` (Clay's long-lived release branch). All were read with `git log origin/master..<branch>`, `git rev-list --count`, and a file-by-file diff of the files each branch changed against `origin/master` (`61ac2c2e6`, 2026-11-20 02:26Z). Because every PR was squash-merged, "commits not on master" is always more than zero for a merged PR; the useful number is "files the branch changed that still differ from master" (0 means the content is on master).

**Branches that hold the issue 655 work (the ones you asked about):**

| Branch | PR | Holds | Commits beyond master | Content on master? |
|---|---|---|---|---|
| `clayphi/issue-655-pr-a` | #686, OPEN | PR A: poll core (`issue_watch/`) | 24 | NO. All 59 files differ. Not on master. |
| `clayphi/issue-655-pr-p` | #690, OPEN (it has a PR; it is not PR-less) | PR P: `/sc:issue --plan` and `--remaining` | 15 | NO. All 13 files differ. Not on master. |
| `clayphi/issue-655-pr-c` | #684, MERGED 11-20 02:01Z | PR C: agent-work-report skill | 17 | YES. 0 of 28 files differ (squash-merged). Branch tip `29b3f6921` of 01:45Z is the content merged. |
| `clayphi/issue-655-pr-d` | #682, MERGED 11-20 00:02Z | PR D: deletes `issue_pipeline`, WC-17, G2 rule 1 | 5 | YES, except 3 of 36 files differ (`CHANGELOG.md`, `core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`). #683 and #684 edited the same three files after it, so this is almost certainly later master edits (not diffed line by line). |
| `clayphi/issue-655-spec-pr` | #681, MERGED 11-20 00:02Z | The design file `docs/designs/orchestrator.md` | 1 | YES. 0 of 1 file differs. |
| `clayphi/issue-668-build-p3` | #683, MERGED 11-20 01:16Z | `/sc:closeout` | 30 | YES, except 2 of 27 files differ (`CHANGELOG.md`, `tests/skills/test_worker_contract.py`; later master edits by #684). |

There is no `issue-655-pr-b` or `-pr-e` branch, and no PR for them. Also no `clayphi/issue-655-spec` branch on origin (the design source `8bd180ba7` named in #681 is not a remote branch; UNVERIFIED where it lives).

**Other Clay branches:**

| Branch | PR | Holds | Beyond master | Still differs from master |
|---|---|---|---|---|
| `clayphi/v61-part-b-map` | NONE (no PR in any state) | Planning documents for the 6.1.0 removal bundle: dependency map, reference index, retention table, plan, under `.dev/cleanup/bundle/` and one `TASK-WF-planThe610Remova...` task file (8 files, +750). Two commits, 2026-11-18 17:10Z and 17:25Z. | 2 | 6 of 8 files. Not in `integration` either. Planning records only, nothing that runs. |
| `clayphi/release-6.0.0` | #634 MERGED into integration | The 6.x release orchestrator's records branch. Tip 2026-11-19 03:37Z "docs(release): v6.1.0 records, #647 was closed by Clay". | 52 | 25 of 53 files (UNVERIFIED how many are Clay content never merged versus later master edits; the diff listing shows owner `.dev/issues/409` and `.dev/issues/606` files, which are master moving ahead). |
| `clayphi/v61-pr1-doc-skills`, `-pr3-mdtm-routes`, `-pr4-mdtm`, `-pr5-release`, `-docs-retention-90`, `v6-post-release`, `v61-post-release` | #650, #653, #656, #657, #659, #649, #667 (all MERGED into `integration`) | The 6.0.0 and 6.1.0 work | 2 to 6 each | Differences are the integration-versus-master gap and later master edits. `integration` is 2 commits ahead of master (#667 and a merge) and 10 behind it. |
| `clayphi/v61-pr2-sc-task` | #652 CLOSED | The withdrawn `/sc:task` removal | 6 | 74 of 101 files differ. Not merged anywhere. Do not revive without the owner's list. |
| `clayphi/v61-merge-master` | #663 CLOSED | Empty merge | 1 | 0 files. |
| `clayphi/ccsession-saved-sessions` | #641 MERGED | ccsession human-saved sessions | 9 | 7 of 20 differ (master moved). |
| `clayphi/ccsession-repo-heading-retention`, `433-ccsession-orca-resume`, `ccsession-failover-392`, `docs-v5-impact-validation` | #570, #355, #481, #377 (all MERGED) | ccsession and v5 test docs | 1 to 3 | Squash-merged; remaining differences are later master edits. |
| `clayphi/help-472-473`, `clayphi/issue-651-plan-fields` | #475, #661 (MERGED) | Small fixes | 0 | Fully on master (ancestors of it). |

`origin/integration`: 2 commits ahead of master (#667 post-release docs and a merge of master), 10 behind. Not a conflict with the watcher area.

## 4. What changed on PR 686 since `4e7f12b1a`

`git log 4e7f12b1a..origin/clayphi/issue-655-pr-a --stat --oneline` (head now `8e5ae29ad`, GitHub `updatedAt` 2026-11-20 03:00Z; CI all green, mergeable CLEAN):

| Commit | Time (UTC) | Files | What it does |
|---|---|---|---|
| `6ee9c6df3` fix(issue-watch): review finding of PR A round 11 (#655) | 02:47 | `cli/issue_watch/cycle.py` (+9/-4), `tests/issue_watch/test_route.py` (+26) | When the poll's call allowance is used up, the registry probe makes no Orca call and reads the orchestrator session as "unknown" (not dead, not ended). |
| `8e5ae29ad` fix(issue-watch): review finding of PR A round 12 (#655) | 02:53 | `cli/issue_watch/cycle.py` (+5), `tests/issue_watch/test_hold.py` (+18) | A plan-request resend is dropped when its repo is no longer listed, is disabled, or fails the origin check. |

Total: 2 commits, 3 files, +54/-4. PR size now 59 files, +14,306/-16,637 (was +14,256).

Does it touch the conflicts in FULL-REPORT.md section 5? NO. Both commits are review-round fixes inside `cycle.py`. They do not touch the trigger (assignment only), the scheduler (no cron), the claim level, the grant list, the launch guard, the worker contract, or the state location. One note: the round 12 fix reads the repo list kept in the orchestrator repo (`repos.yaml`), which is the design's "state in another repo" choice (section 5.7), against the owner's in-project `.dev/coordinators/` layout (Q26); the commit follows the existing design and does not add a new conflict. `cycle.py` is also one of the six files the `claim-handoff-planb` worktree has modified, so the two lines keep drifting apart (see table 2).

## 5. Table 2: the owner's own recent related work (for comparison)

Sources: `gh pr list --state merged --search "merged:>=2026-11-01"` (all merged PRs since 2026-11-01; the related ones are picked below), `gh pr list --state open` (3 open PRs in the whole repo: #685 owner, #686 and #690 Clay), `gh issue list --state open --author ironbelly` (55 open), and the local worktrees. Authorship is by GitHub login; PRs by `ironbelly` may have been written by agent sessions on this host. Status: COMPLETE = merged; IN PROGRESS = open PR, open issue with live work, or local uncommitted work.

### 5A. Merged PRs (COMPLETE) since 2026-11-01

| Area | PR (merged, UTC) and title | What Clay's work does to it |
|---|---|---|
| Watcher | #447 (11-08 06:27Z) feat(cli): add issue-watch poller for issue #331, 459 files. #448 (11-08 07:01Z) approvers-file race fix. #451 (11-08 07:32Z) brainstorm records. #485 (11-10 06:10Z) design drift fixes and owner rollout checklist. #548 (11-14 17:42Z) owner's "option 3" claim-level decision | #686 rewrites #447 (removes claim launch, approval, trigger, Project reads; reuses runner, audit, lock, budget). #681 row R9 (claim only at level none) conflicts with the option 3 decision in #548. Poller built but `enabled:false`, never run live. |
| Claim pipeline and `/sc:issue` | #373 (11-04 21:27Z) the command; #380; #388; #425 (11-07 14:16Z) `--pipeline` and `--submit`; #455, #459 (11-08) tab-title shim check; #486 (11-10) issue types and Complexity; #509 (11-11) t1 worker tier; #583 (11-17 03:34Z) remove the plain approved route; #636 (11-18 07:39Z) default pipeline level from the issue; #661 (11-19, authored by Clay) plan sections | #690 and open issue #689 extend it (plan mode, heading rename). #681 R9 and R23 differ from #636 (level picked from the issue). |
| Issue pipeline (Plan A and Plan B) | #584 (11-17 04:00Z) approval core, 32 files; #591 (11-17 17:28Z) coordinator handoff, 100 files | DELETED by #682. Implemented owner Decision 6 = B. |
| Launch-level guard | #432 (11-08 01:53Z) hook for claim-launched agents (#394), 201 files; #414 (11-07) session identity for governed Bash jobs; #457 (11-08) speed-limit test; #449 (11-08) Orca worktree needs an agent; #677 (11-19 23:09Z) record of the #442 live run | #682 removed guard rule G2.1 (issue-pipeline tamper class) and WC-17; design DQ7 says the guard does not apply to orchestrator workers. |
| Worker contract and coordinator | #411 (11-06 21:41Z) P1 unattended contract for 16 commands; #422 (11-07 14:15Z) P2 for 15 commands; #434 (11-08) liveness rules; #508 (11-11) `--unattended` default for coordinators; #532 (11-12) supervised-orchestration tech reference; #587, #588, #589 (11-17) orchestrator, observer and watcher alignment decisions; #585 (11-17) | #682 and #617 to #656 edit `WORKER-CONTRACT.md`; #683 adds a list entry; the design adds an "orchestrated issue flow" section (PR B, not built). #587 marks the watcher-to-orchestrator handoff DEFERRED, not rejected. |
| Sweep | #539 (11-14 17:41Z) read-only `superclaude sweep` and `/sc:sweep`, 2,290 files; #579 (11-17) fix | Not touched by #686. #684 overlaps in purpose. |
| Observer and dashboard | #503 (11-11 19:54Z) observer release 1; #514 (11-12) release 2; #577 (11-17 00:40Z); #586; #592 (11-17 14:19Z); #598; #673 (11-19 19:16Z) visual parity | Not touched by #686. #684 overlaps in purpose. |

### 5B. Open owner work (IN PROGRESS)

| Item | State and date | Status | Relation to Clay's work | Evidence |
|---|---|---|---|---|
| PR #685 docs(dev): add the issue #442 launch-level observation runbook, scripts and results | OPEN, opened 2026-11-20 00:04Z by `ironbelly` | IN PROGRESS | Independent. Design DQ7 exempts orchestrator workers from the same gate. | `gh pr list --state open` |
| Issue #450 Roll out the issue watcher: live test, shadow run, cron (follow-up to #331) | OPEN, assigned `ironbelly`, last updated 2026-11-18 18:25Z | IN PROGRESS (open; live work is in `claim-handoff-planb`) | #655 says "replaces #450" and plans to close it. Clay's 11-18 17:00:32Z comment to `@ironbelly` on it has no answer on GitHub. | `gh issue view 450`; FULL-REPORT.md |
| Issue #339 Orchestrator mode | OPEN, assigned `ironbelly` | IN PROGRESS (Phase 1 sweep built) | #681 takes the name `/sc:orchestrator`; owner R10 wants the word "coordinator". | B-open-issues.md |
| Issues #423 (orchestrator v2), #444 (sub-orchestrator), #468 (check spam), #534 and #590 (sweep follow-ups), #604 (observer remote fleet) | OPEN | NONE built (follow-ups) | #444 asks the same name and nesting question #681 settles in its own way. | B-open-issues.md |
| Issue #409 TUI dashboard (observer) | OPEN. Assigned `clayphi` (checked 2026-11-20; the issue was authored by `ironbelly`). Last update 2026-11-18 03:30Z | Observer releases 1 and 2 COMPLETE; item 9 (show watcher state) open | #684 builds a living report with the same audience; #409 item 9 has no source yet. | `gh issue view 409` |
| Issues #442 (live guard observations), #678 (guard misses a bare `claude <prompt>`), #546 (model policy hook), #691 (write the claim launch result to a file) | OPEN | IN PROGRESS or NONE | #655 says the orchestrator is "gated by #442". | B-open-issues.md; `gh issue list` |
| Coder #515 (cron in the image) and #516 (`COORD-<repo>` session per project) | OPEN (other repo, `IronbellyOrg/Coder`), last updated 2026-11-18 | NONE built | #515 is made obsolete if the #681 design (Orca automation) wins; #516 overlaps with "the poll starts an orchestrator". | C-worktrees.md (not re-read) |

### 5C. Local, unpushed owner work: worktree `claim-handoff-planb`

- Path: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`. Branch `ironbelly/issue-watcher-zero-setup-plan`, no upstream, not pushed. Based on master `e3e9d636a` (2026-11-17), so it predates #681 and #682. Three local commits beyond master; the last is `d0a0a433b` (2026-11-19 15:29Z) "zero-setup requirements R1-R34 and plan v5".
- Requirements: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (36 rows R1 to R36) plus `amendment-r36-withdraw-r31.md`. Key owner decisions in it: R1 central config saved in the Coder template (2026-11-18); R6 and R16 cron is the scheduler, one dispatcher (2026-11-18); R10 the branch and worktree are named `Coordinator` and "the term is coordinator, not orchestrator, everywhere" (2026-11-18); R19, R22, R23, R25 approval stays the gate, Project Status gate, per-status pipeline, launch levels (2026-11-18 and 11-19); R35 approval is the `Approved` issue field (2026-11-19); R36 withdraws R31 ("Yes, withdraw", 2026-11-20).
- Working tree: 223 entries (52 modified, 142 staged additions, 4 renames, 25 untracked), read at about 04:00Z. Modified files include `src/superclaude/cli/issue_watch/{audit,cli,cycle,github,launch,predicates}.py`, `src/superclaude/cli/issue_pipeline/{brief,cli,reads}.py` (the package #682 deleted), `src/superclaude/core/WORKER-CONTRACT.md` and `src/superclaude/hooks/scripts/launch-level-guard.sh` (both also edited by #682), and new `issue_pipeline/complete.py`.
- Status: IN PROGRESS but at its end. The `/sc:implement` ledger `.dev/tasks/done/TASK-WF-requirements-20261119-143917-2/progress.md` (last written 2026-11-20 03:34Z) records T28 complete, then `FINAL: pass` and `ARCHIVE: start`. That is the run's own record; I did not run its tests, and nothing is committed or pushed. FULL-REPORT.md (written about 02:50Z) described the run as still building; it has finished since.
- Collision with Clay's line, from evidence: both sides edit `issue_watch/{audit,cli,cycle,github,launch,predicates}.py`; planb adds a `repos.py` with a different job from #686's `repos.py` (read from `orca repo list` against `repos.yaml` of the orchestrator repo, per C-worktrees.md); planb edits files in `issue_pipeline/`, which master no longer has (a modify/delete conflict on rebase, not tried: UNVERIFIED), and both edit `WORKER-CONTRACT.md` and `launch-level-guard.sh`.
- Other local work with no overlap (C-worktrees.md): `issue-409-mvp` (observer, 1 unpushed commit), `open-decisions` (stale), `issue-624`, `blocker-classification-stage3b/3c`, `eval-tasklist-review-panel`, `issue-442-runbook` (backs open PR #685). The main checkout is on branch `docs/409-orca-dashboard-designs` (the #409 dashboard design package).

## 6. Preliminary dispositions, in one place

| Disposition | PRs | Reason in a few words |
|---|---|---|
| REVERT-CANDIDATE | #682 | Deletes merged owner PRs #584 and #591 and WC-17 with no owner review; the owner's next plan (`claim-handoff-planb`) builds on the deleted package. Against a revert: the code never ran live and the owner may drop the approval step anyway. Needs a revert-or-restore ruling, not an automatic revert. |
| NEEDS-DEBATE | #681, #686 | #681 is "approved" by its author and holds ten rows that disagree with recorded owner decisions (trigger and gate, cron, claim level, grants, guard, name, state location). #686 implements those rows, so it waits on two rulings: assignment-only against the `Approved` field, and Orca automation against cron. CI is green and the diff is clean, so the wait is about decisions, not code quality. |
| KEEP-ADAPT | #684, #690 (and the registry, hold, audit and wake parts of #686 after the rulings) | #684 overlaps sweep and observer and is coupled to the #686 config file. #690 is complementary but must agree with the plan headings (`## Fix approach` in `hold.py`, against the rename in #689). |
| KEEP | #683, #661, #670, #499 and every row of tables 2B and 2C except those marked "confirm approval" | No conflict with owner work found. #683 only adds one list entry to the worker contract. |
| KEEP (confirm approval) | #620, #622, #627, #629, #631, #632, #650, #656 | The owner's approval on record covers wave 1 only; later waves were posted for review and the owner engaged on them (swarm reversal, #613, the fork for review-translation), but I found no explicit approval line. These are released in v6.0.0 and v6.1.0, so reversal would be expensive; the question is whether to confirm, not to revert. |

What is complementary and independent of the dispute: #661, #670, #683, #499, the ccsession PRs, the help and docs fixes, and #690 as a mode of `/sc:issue`.

Order of decisions that settles most rows: (1) rule on #682 (restore or accept the deletion), because #686 and the planb plan both depend on it; (2) rule on the trigger/gate and scheduler questions, which fixes #681 and #686; (3) then #684 and #690 follow.

## 7. Not verified, and limits

- Any chat, call or ClickUp agreement between the owner and Clay. No GitHub reply by `ironbelly` exists on #655, #681 to #684, #686, #690; the shared login weakens even that finding.
- The IronFlow repo (Clay's coordinator spec), `RULINGS.md` and the orchestrator repo were not read.
- Whether the owner approved removal waves 2 to 6 and the 6.1.0 bundle: the comment on #571 that records wave 1 was read in full; the other comments were read only up to the first 380 to 420 characters.
- Current content of Coder #515 and #516 (taken from C-worktrees.md, last updated 2026-11-18).
- The `claim-handoff-planb` run's own pass record was read but its tests were not run, and no merge or rebase against master was tried.
- Line-by-line equality of the three files that differ on the `issue-655-pr-d` and `issue-668-build-p3` branches (listed as "later master edits").
- The percentage of deleted lines in #686 that are tests (88%, from FULL-REPORT.md) was not re-measured.
- All reads were read-only: `gh pr list`, `gh pr view`, `gh issue view`, `gh issue list`, `gh api repos/IronbellyOrg/IronClaude/pulls/N/files`, local `git log`, `git diff`, `git status`, `git rev-list`. Nothing was written to GitHub. Scratch files are in `/tmp/clay-inv/`. The repository was not edited. A first `uv run python` call rebuilt the local editable package metadata; later calls used `uv run --no-project python -I`.

