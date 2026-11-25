# Decisions made without the owner (each settled by a quick adversarial debate unless noted)

## Update after PR 700 (2026-11-20 16:15 UTC)

Every entry below was written before the events in this section. Each entry's original text is kept intact, and a one-line "Status after PR 700" now sits under it. Facts here were verified by the coordinator on 2026-11-20, except where marked UNVERIFIED.

**What happened.** Clay opened PR 700 at 14:46 UTC and merged it themself at 15:07 UTC: 63 files, +4599 -11935, commit `471f10511`, no owner review, 21 minutes from open to merge. Its title (from the banner result file) is "revert: roll back the issue 655 orchestrator build (PRs 681, 682, 684), keep /sc:closeout". It rolled back:
- PR 681 (the design document `docs/designs/orchestrator.md`): the file is deleted from master.
- PR 682 (the deletion of the issue pipeline): the `issue_pipeline` package, WC-17 and guard G2 rule 1 are restored. 33 of PR 682's 36 files now equal the pre-682 tree; the other 3 differ only by `/sc:closeout` lines.
- PR 684 (the `agent-work-report` skill): removed.
It kept `/sc:closeout` (PR 683). The archive branch `clayphi/archive-orchestrator-655-20261120` (commit `d7d645ddd`) holds the rolled-back work. PRs 686 and 690 stay drafts. Master is now `471f10511`.

**Not on master after PR 700:** the "Messages carry no `--to`" contract bullet and its tests, and `--issue <N>` on the WC-17 `check-approval` step.

**The owner's revert PR 697** (opened 12:36 UTC) was closed at 16:14 UTC as superseded; its branch `ironbelly/revert-pr-682` is kept. A small replacement PR on branch `ironbelly/restore-gaps-after-pr-700` re-adds those two gaps. When this was written `gh pr list --head ironbelly/restore-gaps-after-pr-700 --state all` found no PR, it is PR 701 (https://github.com/IronbellyOrg/IronClaude/pull/701, open). The banner task for the PR 681 design document was dropped because the file is gone. Issues 698 ("Release-worker and plan-approval checks rest on text matching and an assignee shortcut") and 699 ("The claim script creates the issue worktree without an agent, against the every-worktree-gets-an-agent rule") were filed from the PR 697 review, with no labels or assignees.

**What this does to the verdicts.** The verdicts cite lines of `docs/designs/orchestrator.md` and of the report skill that are no longer on master (the snapshot used in the debates is the older master `61ac2c2e6`). Any recommendation to edit that design file is moot until the owner decides to restore it; the archive branch keeps the text. The recommendations themselves (the rules the owner's line won) stand.

| Entry | Old status (what it recommended) | New status |
|---|---|---|
| D03 | Revert PR 682 as one new PR, as the default | DONE BY PR 700 in substance (Clay's own rollback, not the owner's PR 697). Two gaps remain: the no-`--to` bullet and tests, and `--issue <N>` on WC-17; the small replacement PR is PR 701 (https://github.com/IronbellyOrg/IronClaude/pull/701, open) |
| D05, item 6 and the "keep PR 682's guard edit" action | G2 rule 1 stays removed | SUPERSEDED BY PR 700: rule 1 is back, the guard equals its pre-682 text. A guard change still needs independent review |
| D08 | Fix `agent-work-report/SKILL.md:12` in a PR 684 follow-up | SUPERSEDED BY PR 700 (skill removed). The naming decision itself is UNCHANGED |
| D11 | Keep PR 684; adopt the report skill as the work-item layer, the living report, silent-loss gate, transcript reader and item template; follow-up PR on the skill | SUPERSEDED BY PR 700 for every action that builds on the skill. The sweep-as-source and observer parts are UNCHANGED |
| D13 | Keep `/sc:closeout` (PR 683) | UNCHANGED: closeout is kept on master. Its step that settles a work-report entry depended on the removed skill (effect UNVERIFIED) |
| D14, PR 681 | KEEP, with a banner and a design amendment PR | SUPERSEDED BY PR 700 (rolled back; banner task dropped; amendment PR moot) |
| D14, PR 682 | REVERT as one new PR | DONE BY PR 700 |
| D14, PR 684 | KEEP-ADAPT in a follow-up PR | SUPERSEDED BY PR 700 (removed) |
| D14, PR 683 | KEEP | UNCHANGED (kept on master) |
| D14, PRs 686 and 690 | Hold as drafts (step H0) and adapt | UNCHANGED: still drafts; the ruleset part of H0 is still an owner action |
| D14, owner's PR 697 | (created after D14, as the revert PR) | SUPERSEDED BY PR 700: closed as superseded |
| D15, row A13 | Revert PR 682 | DONE BY PR 700 |
| D15, rows E1 to E5 | Adopt the work-report skill, living report, silent-loss gate, transcript reader, item template | SUPERSEDED BY PR 700 (skill removed) |
| D15, rows G4 to G6 and every DOC row whose carrier is `docs/designs/orchestrator.md` | Keep or amend the design text | SUPERSEDED BY PR 700: moot until the design is restored |
| OD-5, OD-9, OA-9, OA-17a, OA-17b, OA-25a | Answers that rely on the work report, the living report or its entry lines | UNCHANGED answers; their carrier (PR 684's report) is gone from master. Restoring it is an owner decision |
| OD-2 | Re-plan then re-approve; the restored WC-17 flow "may serve as the gate" | UNCHANGED; its open dependency (WC-17 restored) is now met on master |
| D16 | Hold PRs 686 and 690; the review rule | UNCHANGED. PR 700 was again self-merged by its author with no owner review, the pattern this verdict addresses |
| Q02 | Cleanup script may run `git branch -d` | UNCHANGED: it touches nothing PR 700 changed |
| All other entries (D01, D02, D04, D06, D07, D09, D10, D12, Q01, Q03, Q04, OD-1, OD-3, OD-4, OD-6, OD-7, OD-8, OD-10 to OD-13, OA-13a to OA-13c, OA-25b, OA-28a, OA-28b) | Their recommendations | UNCHANGED. Only their actions that edit the deleted design file are moot |


Written 2026-11-20. Status: complete (43 entries, plus coordinator decisions, owner actions and verdict disagreements).

Owner order (verbatim intent): "Anything you need confirmation or have a question, invoke a quick adversarial debate and proceed with the winning suggestion. Record the original question for me, the winning recommendation and its implications to an .md file and present it to me when this exercise is complete."

## What the numbers and short names mean

Every PR (pull request, a proposed code change on GitHub) and issue number used below, in plain words. All come from the verdicts; where a verdict corrected the question's wording, the correction is used. "The owner" is the repository owner (GitHub account `ironbelly`). "Clay" is the account `clayphi`. "OURS" means the owner's line of work (merged work, open work, the unpushed zero-setup plan and recorded decisions). "CLAY" means Clay's design and PRs.

| Number or name | What it is |
|---|---|
| PR 584, PR 591 | The owner's "Plan A" and "Plan B" PRs of 2026-11-17 that built the issue-pipeline package (plan hash, approval-line check, adoption and approval stores, release-worker) |
| PR 585 | The owner's PR that narrowed the "Ruling in chat" rule |
| PR 539 | The owner's `/sc:sweep`, a read-only report of Orca sessions |
| PR 409 and issue 409 | The owner's dashboard design package, and the issue for a terminal (TUI) dashboard design |
| Issue 651, PR 661 | Clay's request for plan sections in issue templates (651, an issue) and the merged PR that did it (661) |
| PR 670 | Clay's merged daily log of merged PRs |
| PR 681 | Clay's merged design document `docs/designs/orchestrator.md` (the design; "D:nnn" means line nnn of it) (rolled back from master by PR 700) |
| PR 682 | Clay's merged deletion of the owner's issue-pipeline package, rule WC-17 and guard rule 1 (rolled back from master by PR 700, so the package is restored) |
| PR 683 | Clay's merged `/sc:closeout` command |
| PR 684 | Clay's merged move of the `agent-work-report` skill into IronClaude (rolled back from master by PR 700) |
| PR 685 | The owner's open PR with the runbook and results for issue 442 |
| PR 686 | Clay's open rewrite of the issue watcher (head `8e5ae29ad`, 59 files) |
| Issue 687, issue 689 | Clay's requests (issues, not PRs): a daily worktree cleanup (687) and moving brainstorm and design into issue creation (689). Nothing is built for either |
| PR 690 | Clay's open PR (branch `issue-655-pr-p`) adding `/sc:issue --plan` and `--remaining` |
| PR 693, issue 691 | The owner's open PR that saves the claim launch result file, and its issue |
| PR 697 | The owner's revert of PR 682 (opened 12:36 UTC on 2026-11-20, closed 16:14 UTC as superseded by PR 700; branch `ironbelly/revert-pr-682` kept) |
| PR 700 | Clay's PR (opened 14:46, merged by Clay at 15:07 UTC on 2026-11-20, commit `471f10511`, no owner review) that rolled back PRs 681, 682 and 684 and kept `/sc:closeout` |
| Issues 698, 699 | Issues filed from the PR 697 review: text-matching and assignee-shortcut checks in the release-worker and plan-approval code (698), and the claim script creating the issue worktree without an agent (699) |
| PR 662, PR 658 | The owner's revert PR and the release 6.1.0 PR it reverted |
| Issue 290 | An open issue (since 2026-10-29, assigned to Clay) about contribution rules; the owner answered "only file issues until we have an eval framework" |
| Issue 302 | The owner's original design of the claim chain (claim checks the issue against fresh code, then builds the chain) |
| Issue 339 | The owner's "orchestrator mode" issue: one coordinator for all sessions, with `sc:close`, worktree and branch cleanup and an hourly sweep |
| Issue 394, issue 442 | 394 asked for the launch-level guard; 442 holds the guard's live observations and is still open |
| Issue 423, issue 444 | The owner's issues on a knowledge layer ("Orchestrator v2", 423) and a sub-coordinator (`--sub`, 444) |
| Issue 450 | The owner's roll-out issue for the watcher; Clay commented on it on 2026-11-18 and has no recorded answer |
| Issue 655 | Clay's tracking issue for the watcher and orchestrator series ("replaces 450") |
| Coder issues 477, 515, 516 | Issues in the owner's other repo `IronbellyOrg/Coder`: a listener in every workspace (477), installing cron at boot (515), and a Coordinator branch, worktree and session per project (516) |
| "planb" | The owner's unpushed local branch `ironbelly/issue-watcher-zero-setup-plan` in worktree `claim-handoff-planb` |
| "PR B", "PR E" | Clay's planned, unbuilt PRs: the orchestrator skill (B) and the runbook rewrite (E) |
| R-numbers (R9, R19, R25, R33 and so on) | Rows of the owner's zero-setup requirements file, which lives only in the unpushed planb worktree |
| WC-nn | Numbered rules in `src/superclaude/core/WORKER-CONTRACT.md` |
| Guard, G1, G2, L1, L2 | `launch-level-guard.sh`, a hook that blocks a governed agent's commit, push and merge; G1 is the owner's acceptance of one guard-less test issue; G2 is the guard note; L2 is the git pre-push hook |
| K12, DQ7, NG-2 | K12 is Clay's risk row that workers run unguarded with `master` unprotected; DQ7 is his rule that workers start without the guard; NG-2 is the owner's rule that the poll never writes to GitHub |
| Poll, coordinator, orchestrator | The poll is the unattended watcher that looks for assigned issues. The coordinator (Clay's name: orchestrator) is the long-running session that takes the work (see D08) |
| Spec, SEC-nn, FR-nn, S-nn, F-nn, G-nn, H-nn | The unified spec `spec/SPEC.md` has numbered requirement rows (FR), security rows (SEC), build stages (S) and owner-action rows; F, G and H numbers are findings of spec panel reviews 1, 2 and 3 (listed in `spec/FOLLOW-UPS.md`) |
| OA-n | An owner action from section 7 of the brainstorm's merged requirements file (34 of them, OA-1 to OA-34); sorted by `debates/OA-TRIAGE.md` |
| K-rows, INV-rows, RK-rows | Rows of that merged requirements file: decision rows (K9 is the rule for an issue waiting for a go, K15 for a hand-back waiting for re-approval, K19 puts the sweep JSON beside the report, K24 the `auto_enable` default), invariant findings (INV-023: cap 1 plus owner silence) and risks (RK-30: numbers nobody can source) |
| S17, `first_run`, `auto_enable` | S17 is the stage "live tests, then enable one throwaway repo"; `first_run` is planb's per-repo setup check (six checks, then it writes `enabled: true`); `auto_enable` is the defaults key that decides whether a passing repo switches itself on |


## Summary table

Legend. Winner: OURS (the owner's line), CLAY (Clay's design) or HYBRID (a mix, stated in the entry). Debate status: "partial" means the verdict or the progress log flags partial convergence or HIGH findings left open; "full" means the verdict does not flag partial (the depth, standard or quick, is in each entry). For the open questions OD-1 to OD-13 and the owner-action questions OA-9, OA-13, OA-17, OA-25 and OA-28 the winner is the answer's winner; the group debate's overall verdict is stated in each entry. OA-13c was agreed input and not contested. No entry was won outright by CLAY.

| ID | Question in 8 words | Winner | Confidence | Debate status |
|---|---|---|---|---|
| D01 | Does assignment alone start work, or approval? | HYBRID | 78% | partial |
| D02 | Poll scheduler: cron dispatcher or Orca automation? | HYBRID | 62% | partial |
| D03 | Revert or keep PR 682's issue-pipeline deletion? | HYBRID | 78% | partial |
| D04 | Claim always at level none, or per-issue level? | HYBRID | 75% | partial |
| D05 | Must orchestrator-started workers run under launch guard? | HYBRID | 78% | partial |
| D06 | Who merges: orchestrator, or a person's go? | HYBRID | 85% | partial |
| D07 | Coordinators per project, or a registry repo? | HYBRID | 80% | partial |
| D08 | What to name the role and the command? | HYBRID | 85% | full |
| D09 | May the poll write labels to GitHub? | HYBRID | 78% | partial |
| D10 | How should the poll wake the coordinator? | HYBRID | 75% | full |
| D11 | How to unify work report, sweep, observer, dashboard? | HYBRID | 72% | full |
| D12 | Keep, adapt or reject Clay's /sc:issue plan changes? | HYBRID | 72% | partial |
| D13 | Are closeout, cleanup and PR log duplicates? | HYBRID | 80% | full |
| D14 | Final disposition of PR 686 and the PR stack | HYBRID | 80% | partial |
| D15 | Which Clay elements to adopt, and how? | HYBRID | 72% | partial |
| D16 | Which process package prevents a repeat incident? | HYBRID | 75% | partial |
| Q01 | Who writes a per-issue grant row? | HYBRID | 75% | partial |
| Q02 | May the cleanup script delete local branches? | HYBRID | 85% | full |
| Q03 | Keep, strip or replace dormant label code? | HYBRID | 70% | partial |
| Q04 | Does one typed go cover fix-round pushes? | HYBRID | 80% | partial |
| OD-1 | Default depth of the plan call | OURS | 66% | full |
| OD-2 | How hand-back round 2 starts | OURS | 78% | full |
| OD-3 | Scope of the naming rule | OURS | 75% | partial |
| OD-4 | Refused mandatory escalation: fail open or closed? | OURS | 75% | partial |
| OD-5 | Channel for audit escalations | OURS | 60% | partial |
| OD-6 | Coordinator never tags or publishes | OURS | 89% | full |
| OD-7 | Interrupt a running worker | OURS | 85% | full |
| OD-8 | Build the lease comment now | OURS | 75% | full |
| OD-9 | List newly assignable issues; streams off | OURS | 85% | full |
| OD-10 | Authority for the post-merge issue close | OURS | 77% | full |
| OD-11 | Default grants of a fresh install | OURS | 71% | full |
| OD-12 | Protecting the per-repo config | HYBRID | 69% | full |
| OD-13 | Waiting hand-back versus the in-flight count | OURS | 70% | full |
| OA-13a | Does a recorded merge go expire by clock? | OURS | 80% | full |
| OA-13b | Merge-time hold for a silent reviewer? | OURS | 70% | full |
| OA-13c | Does `changes_requested` stay a hard refusal? | OURS | 95% | full |
| OA-25a | Does a waiting go get a reminder? | OURS | 75% | full |
| OA-25b | What does owner silence mean on waiting go? | OURS | 85% | full |
| OA-9 | Where is the sweep JSON saved? | OURS | 85% | full |
| OA-17a | May the observer show entry text? | HYBRID | 72% | full |
| OA-17b | Is the questions panel an exception? | OURS | 75% | full |
| OA-28a | Should a repo passing first_run switch itself on? | HYBRID | 70% | partial |
| OA-28b | Does NG-2 cover only the poll cycle? | OURS | 88% | partial |


## Entries

### D01 Trigger and approval gate

**Original question:** Should a newly assigned issue alone start the work (CLAY R1: assignment is the only trigger, no trigger label, no approver list, no plan-approval gate, D:73), or must a human approval stay as the gate (OURS R19, R22, R35, R36: approval label plus the issue Status or `Approved` field)? Which code in `src/superclaude/cli/issue_watch/` (predicates.py, github.py, cycle.py) survives?

**Winner:** HYBRID (the owner's rule decides the trigger; Clay's plan check and `hold:backlog` veto are added as read-only skip reasons).

**Winning recommendation:**
1. Assignment alone never starts work. A worker starts only when: the issue is open and assigned only to the watcher's login; an allowed approver's approval (the `Approved` = `Yes` issue field, or the `issue-watch:approved` label until that field is live) is present and unedited since; the Project Status is in the allow-list Research, Spec, Plan, Debug; the label `hold:backlog` is absent; and Clay's `plan_check(body)` passes.
2. Add two new read-only skip reasons, `plan_incomplete` (from Clay's `hold.py`) and `held_backlog`. The watcher writes no label for them.
3. MR-1 (HIGH): the check made at the moment of start must repeat the approval, the "unedited since" test and the Status allow-list, not only the plan check and `hold:backlog`. Clay's PR 686 re-checks only the last two.
4. MR-2 (HIGH): keep the claim-marker guard, so a hand-run `/sc:issue --claim` plus a watcher start cannot run two workers.
5. The plan must exist before the approval, because editing the issue body after approval voids the approval. Document and test it.
6. Assignment alone may be reconsidered only when all four hold: the launch guard refuses to start when not effective; workers cannot push or merge; the watcher skips an issue that already has a claim record or worktree; the owner records the reversal in chat.
7. Keep the separate `issue-watch:trigger` label for now; dropping it is the owner's decision.

**Implications:**
- PR 686 (Clay's rewrite of the watcher) removes the approval, trigger, Project and approver code, so it cannot merge as it stands. It must be rebased onto the owner's code or split. PR 686 and the owner's local branch edit the same files and no tree holds both rule sets.
- Issues assigned before switch-on are marked "seen" in PR 686 and never woken; an approved one needs `--take`.
- Two new skip reasons must appear in the audit reasons that the observer and dashboard read.
- A hand claim assigns the issue, so "assigned" cannot be shown as "approved".
- Dropping approval would remove the only code that ties a person's yes to the issue content (14 predicate symbols, about 30 in `github.py`).
- Clay's comment on the owner's issue 450 (roll-out of the watcher) has no recorded owner answer yet.
- Docs to correct: design lines 73, 111, 488 (after the owner confirms), and FULL-REPORT section 7 (R36 withdraws R31 only, not the Status gate).

**Caveats:** Partial convergence: two HIGH invariant findings (crash after ack, abandoned wake) were not settled by the advocates and were turned into requirements. Confidence 78 percent. UNVERIFIED: whether a read-only user can self-assign an issue; the shape of `Approved` field timeline events on live GitHub (fixtures were assumed); whether the trigger label can be dropped without changing `approval_of`; whether the owner's R19 approval came before or after Clay's comment on issue 450; the base-selection scores are single-evaluator estimates; `orchestrator.md:1234` was verified by the orchestrator only.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D02 Scheduler: cron or Orca automation

**Original question:** Should the poll run from cron with one dispatcher (OURS R6, R16, Coder issue 515 "cron"), or from an Orca automation named `orchestrator-poll` with a no-agent "precheck" step (CLAY R4, spec 4.8, D:76 and D:343-354)? The owner states Orca automations "start an agent session with a prompt on each run" and that this was debated and rejected. Test CLAY's precheck claim against `waker.py` and the Orca automation docs/CLI help (`orca-ide automations --help`, read-only; do NOT create or run an automation).

**Winner:** HYBRID (cron with one dispatcher stays the scheduler; the owner's written reason is wrong in one place and must be corrected; Clay's precheck automation is kept as a tested-first fallback).

**Winning recommendation:**
1. Scheduler of record is one cron entry every 5 minutes (`*/5 * * * *`), wrapped in `/usr/bin/flock -n <lock file>`, absolute paths for `superclaude` and the Orca shim, output appended to `~/.aidev/logs/issue-watch.log`. The template (Coder issue 515, which installs cron and starts it at boot) must make the entry exist exactly once after every boot.
2. The spec must name which poll command the entry runs. Master and PR 686 have `issue-watch once` reading `repos.yaml`; `run-all` (one dispatcher over `orca repo list`) exists only in the unpushed owner branch. Settle this together with D07.
3. Replace the false reason "an Orca automation starts an agent session on each run" with: it is true only when the precheck exits 0; an automation can still start a session through "Run now" or a dropped `exit 1`; it needs one creation step per Orca host and no boot script exists; one cron entry plus one dispatcher covers all repos with no per-project step.
4. Fallback only: an automation created `--disabled`, enabled after a scheduled (not Run now) shadow run, with a precheck that always returns 1 (code with a unit test), prompt "do nothing and stop", created by the owner.
5. The two existing report automations (`coordinator-morning-wake`, `coordinator-missed-check`) stay as they are.
6. Fix the six-field cron line in `docs/designs/issue-watcher-setup.md` to five fields.
7. Do not claim the scheduler settles zero setup: it still needs Coder issue 515, a one-time `superclaude install --force` per host, the owner-created `Approved` field, and Coder issue 516 (the `Coordinator` worktree).

**Implications:**
- The poll runs unchanged under cron; the scheduler does not block PR 686's code.
- Enrolment follows the poll command: `run-all` auto-enrols a new project, `once` with `repos.yaml` does not.
- A sweep can last up to about 525 seconds against a 300-second tick (arithmetic from two constants, not measured).
- Neither scheduler leaves a "no sweep ran in N minutes" signal; add a last-sweep-time field for the observer. Orca keeps only the last 100 automation runs.
- Design lines R4, 4.8, DQ10 and the "cron dropped" rows contradict this verdict and must change; Clay's runbook steps O3, O4 (create `orchestrator-poll`) would be replaced.
- The owner must know: the sentence "automations start an agent on each run" is true only when the precheck exits 0; "debated and rejected" is not backed by the zero-setup folder; cron is not in the image yet (installed by hand on 2026-11-18), so the choice depends on the Coder repository; both advocates called it a toss-up (about 50 and 55 percent).

**Caveats:** Partial. Confidence 62 percent (about 95 percent that the rationale text must be corrected). Decisive fact that would reverse the choice: a headless `*/5` automation with a `; exit 1` precheck fires for 1 to 24 hours with only skipped rows, survives an Orca restart, and a boot script creates exactly one automation. UNVERIFIED: that an automation fires headless on this host; the 100-row cap, 720-minute catch-up and survival of an image update (read from minified code by an advocate); that a boot script can create it once; the six-field line failing under cron 3.0pl1 (not run); whether PR 686 touches cron or automation text. A debate subagent printed the local Orca auth token into its own transcript (see "Coordinator decisions made without a debate", item g).

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D03 PR 682: the deletion of the issue pipeline

**Original question:** PR 682 (Clay, merged 2026-11-20 00:02 UTC) deleted `src/superclaude/cli/issue_pipeline/` (plan hash, approval-line check, adoption/approval stores, release-worker), WC-17 and the "Issue pipeline duties" section in WORKER-CONTRACT.md, and guard G2 rule 1. Should the owner REVERT it, KEEP it, or RESTORE parts on top of master? The owner's PRs 584 (Plan A) and 591 (Plan B) built it on 2026-11-17 for owner decision 6 = B. Weigh the "never ran live" argument, protections the old tests pinned (one winner on a race, a killed start blocks a second, refusal of bot or edited approvals), and what the owner's local branch `ironbelly/issue-watcher-zero-setup-plan` still depends on.

**Winner:** HYBRID (OURS in substance: revert PR 682, keeping three small separable pieces from Clay). The revert is the default until D01 rules; PR 682 stands only if D01 goes to Clay, under three conditions.

**Winning recommendation:**
1. Revert PR 682 (commit 01e7a9e23) as one new PR, never a force-push. The package, WC-17, "Issue pipeline duties" and guard G2 rule 1 return. Size 4,599 lines. Only `CHANGELOG.md` conflicts.
2. After the revert, re-apply by hand PR 682's standalone worker-duties bullet "ask and send carry no `--to`" and its test assertions. A bare revert drops them silently while tests still pass.
3. PR 686 must not merge ahead of this decision (mandatory). Git merges the revert and PR 686 cleanly, but the result is broken: `superclaude --help` crashes and 29 test modules fail at collection, because PR 686 deletes `issue_watch` names the restored package imports. Merge check: run `superclaude --help` and import the package.
4. The same PR or a named follow-up amends `docs/designs/orchestrator.md` rule R1 (line 73) and section 7, which say the gate is retired.
5. After the revert lands, hosts run `superclaude install`. The guard needs its independent review; its version stamp stays 1.
6. Keep the creation-time plan sections of `/sc:issue --create` (PRs 651 and 661) as an extra layer, never as a replacement for approval.
7. Conditional on D01: if D01 ends with "assignment is the only trigger", PR 682 stands under three conditions: PR B and its named crash and race tests exist and pass before the watcher is enabled; the closed ship gate R33 (`GOVERNED_LEVELS_ALLOWED = False`) is built before the default-on config R18; the owner gives a written ruling naming decisions 2, 3, 6 and Q35 to Q38, given in chat and recorded by the agent.

**Implications:**
- The coordinator duties of Q35 to Q38 return to WORKER-CONTRACT.md; the watcher stays `enabled: false`; the owner branch keeps building on `issue_pipeline`.
- A `--pipeline none` claim again has a consumer; the dangling references in `commands/issue.md:85`, `SKILL.md:140`, `refs/claim.md:96` are fixed.
- What breaks: PR 686 as it stands; design text R1 and section 7 until amended; "assignment is the only trigger" until D01 rules.
- The owner must know: the revert and PR 686 look clean to git and are broken together; a bare revert drops the no `--to` bullet; a GitHub comment "by ironbelly" cannot prove who acted because one login serves the person and the agents; the owner branch has 223 status entries, not 53.

**Caveats:** Partial (one HIGH finding came at the end and standard depth has no third round); 88.9 percent agreement of the advocates. Confidence 78 percent (about 50 if D01 rules for assignment-only, about 90 if the owner confirms the gate stays). UNVERIFIED: whether the restored test `test_the_watcher_record_module_is_not_edited` passes in a real checkout; whether the revert tree passes the full test suite; behaviour of restored approval rows against PR 686's `record.py` schema 2; the owner-branch rebase itself; who "the owner" is in the design; whether the owner saw issues 450 or 655 outside GitHub.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/VERDICT.md

**Status after PR 700:** DONE BY PR 700 in substance. The package, WC-17, "Issue pipeline duties" and guard rule 1 are back on master through Clay's own rollback (commit `471f10511`); the owner's revert PR 697 was closed as superseded. Still missing on master: the "Messages carry no `--to`" bullet and tests, and `--issue <N>` on WC-17 `check-approval`; a small replacement PR on branch `ironbelly/restore-gaps-after-pr-700` is PR 701 (https://github.com/IronbellyOrg/IronClaude/pull/701, open).

### D04 Claim level and grants

**Original question:** When the watcher claims an issue, should it always claim at level none (CLAY R9, D:81) with a standing `grants` list in repos.yaml (DQ6, D:116), or should the issue's Pipeline field choose the launch level (OURS R23, R25, widened 2026-11-19) with one grant row per issue? Include the `/sc:issue --claim` flag semantics (`--pipeline none|worktree|full`, `--submit`) in `src/superclaude/skills/sc-issue-protocol/` and `docs/designs/sc-issue-claim-pipeline-flag.md`.

**Winner:** HYBRID (live claim is level none with one supervised worker, which is Clay's rule and also the owner's own Q35 of 2026-11-14; the owner's Pipeline-level design stays as the named, gated, later design; grants split into four standing and two per-PR).

**Winning recommendation:**
1. Whatever starts a claim passes exactly `--pipeline none` (watcher launch prompt pinned in `launch.py:33`; Clay's wave 1). After the claim, one supervised worker is started with `orca orchestration worker-start`.
2. The Pipeline field is not read while no governed level is allowed. This defers R23 and R25, it does not drop them.
3. The gate-open design belongs to the owner: Pipeline picks the level (None, Worktree, Full, Full Submit). Preconditions: the 12 live observations pass (issue 442, open today); a reviewed owner commit amends R9, the K4 test and DQ7; the change states how a launched agent that reports only through `.dev/issues/<N>/result.md` is watched; the change replaces the protection R36 removed. Until then, replace "never used" with "not used until the owner opens the gate".
4. `/sc:issue --claim` flag semantics stay unchanged (`--submit` only with `--pipeline full`; error codes `E-SUBMIT-NEEDS-FULL`, `E-CLAIM-ONLY-FLAG`; missing guard refuses with `W-ENFORCEMENT-ABSENT`).
5. Grants: four standing (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold`); `pr.merge` and `issue.close` are not standing and are released per PR and head sha by a go the owner gives in chat, the agent records, and an `answer-check` style verb accepts, with the owner identity as a parameter. No file row written by the owner.
6. `E-NO-GRANT` covers only the orchestrator's own verbs; the merge gate gets one added reason, "no recorded merge go".
7. Fail closed: absent or malformed `grants` means no grants; the grants file must sit outside the orchestrator's write reach or be guarded by a hook.
8. No second issue runs on the unguarded worker route until the owner rules on the guard (see D05).

**Implications:**
- The poll stays a claim-at-none trigger; the Pipeline read and per-Status prompt (zero-setup Tasks 3, 7, 10) become dormant code.
- One worker route, one watch path; the observer needs one data source for now.
- Changes: Clay's default `grants` list loses two entries; `answer-check` must be parameterised (it is hardwired to Clay); any test pinning the Pipeline read in the owner branch breaks.
- The owner must know: R9 and R10 are Clay's rulings, not the repository owner's; `ironbelly` is a login shared by the owner and every session, so a chat go does not prove who gave it; the fault-finder found 5 HIGH conditions that the spec must state before unattended claiming is called safe.

**Caveats:** Partial (convergence 78.9 percent against 80 percent; 5 HIGH unaddressed invariants). Confidence 75 percent. UNVERIFIED: whether Clay's design holds any other per-issue stop; whether R10's author is Clay alone; the order of R9 and R25; whether `E-NO-GRANT` covers `issue.comment` for the result comment; `answer-check` was read from design text, not run; `GOVERNED_LEVELS_ALLOWED` exists only in the unpushed worktree.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D05 Launch guard for started workers

**Original question:** CLAY DQ7 and K12 (D:117, D:1234) start workers with `worker-start` and no launch-level guard or L2 pre-push hook, with master unprotected. OURS (issues 394, 442, PR 685, R33 `GOVERNED_LEVELS_ALLOWED=False`) assume the guard governs every launch. Which wins, and should the guard be required for orchestrator-started workers? Include guard G2 rule 1 that PR 682 removed.

**Winner:** HYBRID (OURS wins the central question: the guard is required for orchestrator-started workers, staged behind a live probe; Clay's orchestrator-side controls are adopted beside it).

**Winning recommendation:**
1. The guard (`launch-level-guard.sh`, a hook that blocks a governed agent's commit, push and merge calls) is required for every worker the orchestrator starts, staged and not exempted. Provisional level FS ("full with `--submit`": commit, push a feature branch, open a PR; never merge, never push to `master`). DQ7 changes from "decided: runs unbound" to "required; open owner item G2".
2. Binding steps written down: run `orca_worktree.py pending --level full-submit`, put `[sc-launch:v1:<nonce>]` in the first prompt (a new line in `templates/handoff-prompt.md`), run a preflight, then check the `pending/<nonce>` file is gone within a stated timeout; if not, stop the worker and escalate.
3. Staging is a code switch (a constant in the orchestrator skill, like R33's `GOVERNED_LEVELS_ALLOWED`) that keeps real issues unbound-and-flagged until a reviewed commit flips it. The first bound worker runs on a throwaway issue and records a receipt, `send` and `ask` with no `--to`, a full `/sc:pr-submit --monitor 3` cycle at FS, a scripted push to `master` that is refused, and refusal of a bare push and a compound `git add && git commit`. Until it passes, K12 stays at medium likelihood / high impact.
4. The design must not claim the guard closes K12 (workers run with no guard and `master` is unprotected). FS covers plain pushes to `master` and `main` only; a script run, a push to `integration`, a new session id and tools outside the hook matcher pass. Wording: "mitigates K12 for honest drift on master and main".
5. Adopt Clay's `refuse(argv)`, the head-pinned merge and the audit rows AU1 to AU8 beside the guard, with a test that fails if the design says the audit covers a push that has no PR.
6. G2 rule 1 stays removed; G2 rule 2 stays (a bound worker may `send` and `ask` only as one plain call with no `--to`). If a coordinator-side verb that writes an approval or release file returns, a tamper class for it must come back.

**Implications:**
- The orchestrator (PR B, the orchestrator skill PR, not yet built) can no longer start a worker with a plain spec: it needs the marker line, the `pending` step, a preflight and a receipt check.
- R33's staging switch has no counterpart in PR 686, so it moves into the orchestrator skill. A `--pipeline none` claim writes no launch record, so any worker started after it is unbound unless the bind step runs.
- Guard denials print only to the worker's stderr and leave no record, so a dashboard cannot show "blocked by guard" without a new log.
- Friction: the summary-thread step of `/sc:pr-submit` at FS; compound pushes; branch names with `+`, `@`, `#`; the guard fails closed if `jq` is missing.
- The owner must know: "owner" in Clay's design means the account `clayphi`, and ruling 3 does not undo the owner's G2 sentence; binding does not close K12, only a server-side rule on `master` and `integration` does and nobody owns that action; the first orchestrated issue runs unbound unless the owner says otherwise; the guard protects only `master` and `main`; seven HIGH findings are carried as stated limits.

**Caveats:** Partial (convergence 82.4 percent). Confidence 78 percent for the central answer, about 60 percent on staging details. UNVERIFIED: that `worker-start` delivers the task as a first prompt that fires the guard's hook event with the marker intact (never tried); whether Claude Code issues a new session id on `/clear` or resume; whether L2 would classify a `worker-start` worker as governed; the contents of Clay's `RULINGS.md`; whether the login that runs the orchestrator can create a ruleset. Seven HIGH findings left unaddressed (INV-003, -015, -019, -027, -034, -035, -037).

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D05/VERDICT.md

**Status after PR 700:** Item 6 and the action "keep the guard edit of PR 682" are SUPERSEDED BY PR 700: guard rule 1 is back on master (the guard equals its pre-682 text). The rest is UNCHANGED. A guard change still needs the independent review the G2 design note requires.

### D06 Authority: merging, script-started coordinators, reviewer hold

**Original question:** CLAY lets the orchestrator merge (DQ8, D:118), lets a script start the coordinator and a worker run `/sc:pr-submit` (ADD1, D:135), and holds a PR when a reviewer shows no activity (ADD4, D:138). OURS: WORKER-CONTRACT lines 23, 70, 239-246 (coordinator opened by a person, acts only on the person's named go, never merges on its own, `/sc:pr-submit` never as a worker), `/sc:pr-submit` skip rule for a silent reviewer, and the owner rule that approvals are given in chat. Which authority model should the unified design use, and what safe subset of CLAY's automation (merge on explicit go, typed answers) can be adopted?

**Winner:** HYBRID (the authority model is OURS; the separable, evidenced parts of Clay are adopted on top).

**Winning recommendation:**
1. No merge without a person's typed go for that PR. The go names repo, PR number, the full 40-character head sha, the merge method, the word "merge" and the gate output it refers to; it is typed in live chat after the gate output, recorded, one-shot, expires (the number is an owner decision), and void on a head change or any new gate reason. A passing gate never triggers a merge.
2. The `merge-gate` verb (13 closed reasons) is a read-only check shown before the go and run again just before `gh pr merge --match-head-commit <sha>` (never `--auto`, `--admin`, `--delete-branch`). Merge is refused if anything differs from what the person saw. The gate is design only today (not built).
3. A go may never override: head moved, draft, not mergeable, snapshot incomplete, changes requested, review stalled, no reviewer present, checks pending, review pending, threads open, worker not done. A go may override only with that reason's own question key: checks failing, merge-safety hold. Owner confirms that changes-requested is a hard refusal.
4. `/sc:pr-submit` keeps its silent-reviewer skip rule inside its fix loop. A separate merge-time hold is added: an owner-set per-repo `reviewers` list, a re-request of review on the final head, a wait (default 60 minutes, UNVERIFIED), then escalation to the person.
5. `/sc:pr-submit` is never run by an Orca `worker-start` worker; Clay's "Orchestrated issue flow" (ADD1) is not adopted. The automated route to a PR is the top-level launch `/sc:issue --claim <N> --pipeline full --submit`, which never merges.
6. A script may start the coordinator at depth 0 only when the launch prompt cites an authorization the owner gave in chat and an agent recorded. State that this is self-attested.
7. Contract amendments (owner chat approval first; none in force): WORKER-CONTRACT line 70 allows a coordinator started at depth 0 by the owner's installed watcher under a recorded standing authorization; line 245 lets a Full Submit push of a feature branch count as the person's go for that issue's push and PR only. Lines 23 and 244 stay.
8. Keep Clay's `E-NO-GRANT` refusal, but its list never holds `pr.merge` or `issue.close`; the merge goes through one verb that demands the go entry.
9. `answer-check` is adopted as a validator of entry, question key, head sha and freshness only; it cannot tell a person from a script.
10. Every gate is described as "narrows" a risk, not "closes" it. The nine-row "what reaches the person" list is adopted only as an inventory, as an owner decision.

**Implications:**
- The poll's `grants` key must not carry merge or close.
- The coordinator prepares, checks and waits; Clay's wave 7 autonomous merge becomes "show the gate output and wait for the go". Clay's throughput gain is given up (no measured figure exists).
- R25 and R17 do not count until the owner approves them in chat and the two contract lines are amended.
- Breaks: Clay's wave 7 autonomous merge, ADD1's worker flow, risk K7's "merge when every condition holds", PR B's planned contract section; design text OD1, OD3, OD4 must be rewritten.
- The owner must know: none of the adopted gates is built; seven HIGH invariants stay open until built; a person's typed go cannot be told from script-typed text; Clay's design was approved by Clay only and no owner approval of PR 681 is on GitHub (taken from FULL-REPORT section 4, not re-checked).

**Caveats:** Partial (the adversarial convergence gate ended blocked by seven HIGH items). About 85 percent on the model, about 60 percent on the specific numbers (go expiry, 60 minutes). UNVERIFIED: whether Codex reviews on every push; the 60-minute default and the go expiry (no source); whether the harness marks `orca terminal send` text differently from typed text; whether a terminal plus `ccsession` start is depth 0 in Orca; that `merge-gate` and `answer-check` exist nowhere; the memory note on a late Codex security review is 15 days old and was not re-verified.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D07 State, registry and topology

**Original question:** CLAY keeps a registry `.orchestrator/orchestrators.json` in a separate repo `IronbellyOrg/IronOrchestrator`, one orchestrator per repo, three in flight, multi-org search (ADD3, D:137, D:267-305, D:698-718). OURS (Q26 final in the `issue-339-orchestrator-mode` worktree brainstorm, Coder issue 516, requirements R5/R8/R13/R16): coordinators live in each project (a `Coordinator` branch and worktree, `.dev/coordinators/` layout), one dispatcher loops over `orca repo list`, configs in `~/.config/superclaude/issue-watch.d/`, session named `COORD-<RepoName>`. Which topology wins?

**Winner:** HYBRID (the topology is OURS: project-local coordinators and one dispatcher; five separable Clay capabilities are adopted inside it).

**Winning recommendation:**
1. Coordinator session, branch, worktree and records live in each project. One cron entry runs one dispatcher over `orca repo list` (a failed list is an error, never "zero repos"), with one config per project in `~/.config/superclaude/issue-watch.d/` and one child cycle per project with its own lock, state directory, kill switch and day cap.
2. Remove the separate registry repo `IronbellyOrg/IronOrchestrator`, `.orchestrator/orchestrators.json`, the hand-kept `repos.yaml` allow list, the 30-minute idle end, extra poll-started orchestrators per repo, the `wrong_target` refusal and the `cd <checkout> &&` step.
3. Adopt Clay's in-flight cap: key `max_in_flight` (default 3) in the per-repo config, checked inside the child cycle after the sweep, per coordinator id, counting `pending`, `launched`, `unknown` store entries plus open claim files once per issue, `pending` written before anything is sent, unreadable file counts as in flight, a full repo records the reason `coordinator_full`. "In flight" needs a named closing writer and an expiry (not yet designed).
4. Adopt guarded restart with a resume wake (bounded to 3 attempts, counter in the store, unreadable terminal list restarts nothing). Until Coder issue 516 creates `COORD-<RepoName>`, the duty holder is `ORCH-IronClaude`.
5. Adopt an optional per-repo `merge` settings block (`merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`), overridden by the live GitHub role at merge time.
6. Org-wide search is optional, off in the first build, fails open.
7. State keyed on `owner/name`, short names unique, exclusive-create state file per issue; add a `name_collision` skip reason.
8. Defect in the owner's plan found by the debate: claim agents launch into the same `Coordinator` worktree as the standing coordinator, against "one live agent per worktree". Give each claim agent its own worktree, or keep the cap at 1.
9. Prerequisites: Coder issue 515 (cron), Coder issue 516 (Coordinator branch, worktree, session), the branch-name decision, a push grant, and a worktree path read from `orca worktree list`. Until 516 lands, the built dispatcher serves no repo (`worktree_invalid`).
10. The owner decided the direction (OWNER-ANSWERS line 23), not the layout or names. The spec must not say otherwise.

**Implications:**
- The built dispatcher is the base. PR 686's poll and the owner's dispatcher cannot both run (they rewrite the same six files).
- `ORCH-IronClaude` holds the duties today, so a restart rule must not start a second duty holder.
- The new skip reason `coordinator_full` should show in the sweep and observer.
- Breaks: Clay's design sections 4.4, 5.7 and 6.2, the `repo_not_listed` and `registry_invalid` reasons and the wake `target` field.
- The owner must know: the direction was decided, not the layout; the debate found a defect in the owner's plan; Clay's rulings 8 and 9 are Clay's, not the repository owner's.

**Caveats:** Partial (five HIGH findings stayed unaddressed at standard depth; closing writer not designed). Confidence 80 percent. UNVERIFIED: the state of Coder issues 515 and 516 (not opened); session detection by tag or name (design U25); that `/sc:issue` keeps the current directory across steps; the Orca launch-route start time; the `WORKTREES_DIR` literal on other hosts; the findings rest on code reading, no test run. Process note: the debate agent made two read-only GitHub calls naming `IronbellyOrg/IronOrchestrator` (one returned `private: true`); nothing was written and nothing touched SuperClaude-Org.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D08 Naming and identity of the primitive

**Original question:** CLAY names the command `/sc:orchestrator` (D:65) while OURS says "coordinator, not orchestrator" (R10, Coder 516), and issues 339 (orchestrator mode), 444 (`/sc:orchestrator --sub`) and 423 (Orchestrator v2, knowledge layer) already use the word for other purposes. The owner's own wording says "coordinator (aka orchestrator)". Decide one name for the session role, one for the command, and how 339, 423, 444 and Clay's design nest into one family.

**Winner:** HYBRID (the names are OURS: role "coordinator", command `/sc:coordinator`; five Clay pieces are kept inside it).

**Winning recommendation:**
1. The session role is "coordinator". No session, tag, key, schema, folder or verb about this system is named "orchestrator".
2. Command and skill: `/sc:coordinator` and `sc-coordinator-protocol`, with Clay's flags `--wake <wake_id>`, `--hourly`, `--resume`, `--take <owner/repo#N>` and `--sub` (issue 444, evaluation only). No `commands/orchestrator.md` or `sc-orchestrator-protocol`.
3. Kinds by qualifier: "person-opened coordinator", "standing-grant coordinator", "project coordinator", "all-sessions coordinator" (issue 339), "sub-coordinator" (issue 444), "report coordinator".
4. Authority comes from a recorded authorization, never from a name or flag. A flag-less `/sc:coordinator` is person-opened mode: it creates no grant and starts no merge (a test pins this).
5. "Orchestrated issue flow" names the process; the folder `.dev/coordinator/orchestrated/` stays. "Orchestration" names Orca's layer only.
6. The report session keeps its names (tag `coordinator`, prefix `coordinator-`, state `.dev/coordinator/`).
7. `Coordinator` is the project coordinator's working branch and worktree; `coordinators` is the shared records branch. Two things, stated in one sentence. The owner may overrule.
8. Persisted names are renamed before PR 686 merges: wake schemas `orchestrator-wake/1` and `-ack/1`, mailbox kind, key `orchestrator_tier`, `orchestrators.json`, `.orchestrator/`, the golden fixture, the typed line, and the design-only `superclaude orchestrator ...` verbs. Cost is zero on master today and grows after merge.
9. Nesting: 339 = all-sessions coordinator; 423 = a knowledge layer over coordinators, not a role; 444 = sub-coordinator, deferred; 655 and Clay's design = the standing-grant project coordinator reached by `/sc:coordinator --wake`. Issue titles stay; a glossary line goes in `HOW-WE-WORK.md` and the command text, with a pinned test.
10. The word "orchestrator" may still appear only for Orca's layer, the parent-session sense in 63 installed files, quotes of issue titles, and "orchestrated issue flow".
11. If "coordinator (aka orchestrator)" is the owner's real wording (not found in any source read), the glossary carries it as an alias for one role.

**Implications:**
- The poll's wake message, mailbox kind, tier key and tag change word before merge.
- Grants have one door (`--wake` or `--take`) and always rest on a recorded authorization.
- The design doc on master (759 uses of "orchestrator"), issue 655's text, and Clay's open PRs 689 and 690 need edits or a glossary; installed copies on other hosts keep old text until next install; the pinned test `tests/core/test_orca_session_launch_guidance.py` lines 33 and 53 must change in the same PR as the `core/CLAUDE.md:58` edit.
- The owner must know: the name `/sc:orchestrator` was never an owner decision (OQ5 has Owner column "no"; none of OD1 to OD15 covers it).

**Caveats:** The verdict gives no partial flag; two-advocate agreement with a concession by Clay's advocate. Confidence 85 percent on role noun and command name, 70 percent on branch-name ruling and tag form. UNVERIFIED: Coder issue 516 text (other repo, unreadable); the owner's wording "coordinator (aka orchestrator)" (found only in TOPICS.md); whether `COORD-<RepoName>` is a ccsession tag or only an Orca terminal name (U25); the "orchestrator" allowlist test's feasibility; scores are judge estimates with no position-bias run.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/VERDICT.md

**Status after PR 700:** PARTLY SUPERSEDED BY PR 700. The fix of `agent-work-report/SKILL.md:12` and the PR 684 follow-up are moot (the skill is gone from master). The naming decision stands, and the persisted-name rename still applies to PR 686 and to the coordinator skill.

### D09 Watcher writes to GitHub

**Original question:** CLAY's poll writes labels `hold:plan` and `hold:backlog`, a plan check, a plan request after one hour and a lease comment (D:410, D:436-495, DQ3). OURS: `docs/designs/issue-watcher.md` NG-2 and owner decision D2 say the poller never assigns, comments or moves Project items. Is the plan hold a clear benefit worth adopting, and if so under which rule change (which writes are allowed, by whom)?

**Winner:** HYBRID (take Clay's read-only plan check, the `held_incomplete` skip and the person-set `hold:backlog` stop now; keep the owner's rule that the poll writes nothing to GitHub, because the one write Clay adds, the `hold:plan` label, has no evidenced benefit yet).

**Winning recommendation:**
1. Adopt now, read-only: the poll runs `plan_check` (a text-only test that the issue body has Priority, Fix approach and Test plan filled in) on the body it already fetches and skips a failing issue with the reason `held_incomplete`. Nothing is written to GitHub.
2. Only a person places `hold:backlog` (the poll only reads it). The per-repo init creates both labels once. The poll never creates a label and never comments about a hold.
3. The label write is deferred, not rejected. If the owner later wants a visible mark, the only poll write allowed is add or remove of the existing `hold:plan` label, only in a repo holding the `issue.hold` grant, and NG-2 is amended at that time to name exactly those two calls. Until then NG-2 stays as written.
4. Switch-on gate for item 3: a 24-hour `--dry-run` shadow run showed the holds, and a test showed `gh` can add and remove a label under cron's minimal environment.
5. Every other write stays with the coordinator under a grant row. The plan body write, the one-hour plan request (a wake-file item) and the lease comment are not poll writes and wait for D07.
6. Fixes found by the debate: `plan_check` runs before the approval read; a placeholder-only section like `<...>` counts as empty (today the unfilled issue template passes); with no grant a failing issue is skipped silently and a leftover label is ignored (today it warns every cycle); the body read stays in memory and never enters the audit log, store, argv or a typed line; one poll per repo; a failed write is remembered for the cycle.
7. The spec names which commit it describes. Master's poll still calls `approval_of`; PR 686's head does not, so "no human approval gate" describes PR 686 and PR 681 (Clay's design), not master.

**Implications:**
- The poll stays read-only on GitHub (the check adds a body read, no write). PR 686's design rows 3 to 6, the `holds` map and `hand_removed` matter only if the label write is switched on.
- With no label, a held issue shows only in `issue-watch status` and the audit log; the sweep and the observer should read that, or a plan-less issue is invisible (point for D11).
- A held issue is never sent to a coordinator, so plans come from a person or from `/sc:issue --plan` (PR 690).
- Breaks: PR 686's NG-2 test pins three label calls and must change; two workspaces polling one repo would re-add a hand-removed label unless one poll per repo is enforced.
- The owner must know: PR 686's poll removes the claim-time approval that master's poll still has, so on that tree the plan check is the only gate; the three writes in the question are not all poll writes; the owner's own local branch already writes a label once per repo at first run.

**Caveats:** Partial (convergence 0.93, one unresolved point: whether the dormant label code ships in PR 686; settled later by Q03). Confidence 78 percent. UNVERIFIED: whether anyone reads `hold:plan`; label-write scope under cron (only the login was tested); whether the per-repo init runs unattended; several probe items were agent-reported and not re-read; the "about 22 of 58 tests" figure is a rough count.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D10 Wake transport

**Original question:** How should the poll wake the coordinator: CLAY's wake files, mailbox message, typed line and session start (D:143-237, PR 686 `wake.py`, which copies about 100 lines of `orca_term.py`), the owner's open Coder issue 477 (listener) which CLAY NG-1 rejects, or OURS claim handoff with a launched session? Include the "no GitHub text reaches a typed line" rule as a candidate strength.

**Winner:** HYBRID (the transport is Clay's durable wake file with an acknowledgment, wrapped in the owner's rules: no listener, id-only rule, one-verb start, no copied terminal code; plus two mandatory fixes neither line has).

**Winning recommendation:**
1. Truth is a file: the poll writes `<orchestrator-repo>/.orchestrator/wakes/<wake_id>.json` (temp file plus rename, mode 0600, at most 64 KiB) before anything is sent; the coordinator writes the `.ack.json`; the poll never writes the ack. A wake gets 3 deliveries (first plus two resends, 10 minutes apart), then the Orca workspace is marked unread and the poll exits 7.
2. Mailbox message and typed line are nudges only, carrying the wake id and nothing else. The mailbox send is optional (it depends on unverified Orca behavior U5).
3. The typed line goes only to an idle person-opened session or one the poll just started (idle, empty draft, 60 seconds without output, main input prompt on screen). Never into a busy session.
4. The coordinator also pulls: it reads the wake directory at every return of its bounded `check --wait` (at most every 5 minutes).
5. The wake file carries ids only (`repo`, `number`, `url`); no title, label or comment text.
6. Keep the rule "no GitHub text reaches a typed line", credited to the owner's D3, widened: only a pattern-checked builder's value reaches a prompt, typed line, mailbox subject or argv.
7. No listener. Coder issue 477 stays open as narrowed on 2026-11-13 (read-only status, no prompt routing); the listener is out by the owner's own decision, not only Clay's non-goal.
8. Session start: if no live session of the target tag exists, the poll starts one, preferably by `orca agent launch` after a live spike shows it carries the ccsession tag; until then the typed ccsession start. An unreadable process table means "unknown", never "none" (today PR 686 starts a duplicate).
9. No copied terminal code: one shared helper with a parity test; Clay's K16 ("accepted for now") is not accepted.
10. Mandatory M1: the coordinator lists an assigned item as taken only after that item's state file exists (today a crash between the two loses the issue).
11. Mandatory M2: an abandoned wake is recoverable, by re-targeting to the next coordinator with a new wake id or by staying visible to a named reader (today it is never woken again).
12. The ack bucket rename (`taken` to `accepted`) happens only with both readers and a pinned schema version.
13. Live-test gate: mailbox from outside a Run, the meaning of `tui-idle`, the `orca agent launch` tag spike and the screen-tail check are proven before the poll is enabled.

**Implications:**
- The poll writes only local files and nudges; NG-2 holds. D10 does not decide who claims.
- The coordinator gains one duty (read the wake directory) and one rule (ack after the state file). The tag and command name in the wake line must follow D08.
- Merging PR 686 as it stands would ship a transport where one crash loses an issue, an abandoned wake cannot be recovered, issue titles reach the model, a blind lookup starts a duplicate session, and a copied terminal helper has no parity test.
- The owner must know: Clay's rejection of the listener is the owner's own decision; the typed line is a nudge, not the guarantee; the two HIGH problems are in Clay's code today; nothing in either line has run live.

**Caveats:** The verdict gives no partial flag; two HIGH defects (INV-001, INV-002) were made mandatory conditions. Confidence 75 percent. UNVERIFIED: U5 (mailbox from outside a Run), U25 (ccsession accepts the tag), the meaning of `tui-idle`, whether the orchestrator skill will accept the loop-read step (PR B does not exist), the 64 KiB cap with long repo names (a fault-finder measured 77,271 bytes), findings other than INV-001, -002, -007, -008 were not re-read. Process note: read-only `gh issue view` calls were made against `IronbellyOrg/Coder` (issues 477, 515, 516) instead of IronClaude; no write.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D10/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D11 Observability stack: work report, sweep, observer, TUI dashboard

**Original question:** Clay's PR 684 moved the `agent-work-report` skill and a living work report into IronClaude. OURS built `/sc:sweep` (PR 539, read-only report, WC-16), `superclaude observe` (the observer behind the issue 409 TUI dashboard design) and the dashboard design package (PR 409). The design 681 never mentions sweep, observe or 409. How should the three be unified (one data source, one report, one dashboard) and which of Clay's report features (living report, nine-row "what reaches Clay" table, cap of 5 notices a day) should be adopted?

**Winner:** HYBRID (the sweep stays the one source of session facts, the work report stays as the plain-English work-item layer, and the owner's read-only rules govern the sweep and the observer).

**Winning recommendation:**
1. One data source: the sweep JSON (schema v1) is the only source of session state; the report and the observer read it. The sweep row gains `session_id` and `worktree_path` (empty allowed) with a reviewed edit to the golden test. The JSON is saved beside the Markdown report, or each reader runs its own sweep (owner decides). Exception: the observer's questions panel calls Orca itself, so "one data source" is false until the owner accepts that or the sweep gains a questions block.
2. One report: the work report is the one plain-English report (per issue: done, left, needs the person, links). Two HIGH rules: it reads transcripts for the sweep's session ids plus every not-done session of the previous report, even if its worktree is gone; its own terminal-to-session map is removed only after one live side-by-side run shows the sweep finds every session the old map finds. "Orca unavailable" writes `read: false`, never "sessions ended".
3. One dashboard: the observer is the one screen; it carries no Options, no Recommendation, no write; entry text passes `observe/sanitize.py`; empty folder, zero rows and "could not read" show as three states.
4. Clay's features: living report adopted with change (per-user state path, entries store only `session_id`); nine-row table adopted with change ("the person" instead of Clay, notice step only, keep the "exactly nine rows" test); cap of 5 notices a day adopted only as a PROPOSAL (default stays 0 until the owner records a ruling); silent-loss rules and `check.py` gate adopted as is; plain-English item template adopted with generic wording.

**Implications:**
- The poll does not read sweep or observer files. WC-16 keeps running `/sc:sweep` on each wake.
- Two question channels remain (observer questions and report "Needs you") until the owner decides and one shared question id exists.
- Breaks if done wrong: removing the report's old session map before the side-by-side run could drop sessions silently; reading only sweep ids drops sessions of removed worktrees; a cap default written as 5 would pass as settled.
- The owner must know: ruling 39 (the cap) is Clay's, not the owner's; `docs/designs/observe-sweep-contract.md` has been unwritten since 2026-11-13 and every join depends on it; PR 684 stays merged.

**Caveats:** Confidence 72 percent (no partial flag in the verdict). UNVERIFIED: which terminal-to-session map covers more sessions; whether a transcript file name always equals its session id; whether the observer may show entry text word for word (owner decision); whether Clay uses the daily report and whether its waker automations were re-pointed after PR 684; the tech reference for the observer did not exist when this debate ran, so code was read directly; the fault-finder reviewed master only.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/VERDICT.md

**Status after PR 700:** PARTLY SUPERSEDED BY PR 700. Every action that builds on PR 684's report skill (keep PR 684, the report follow-up PR, the living report, the silent-loss gate, the transcript reader, the item template) is SUPERSEDED: the skill was removed from master. Sweep as the one source of session facts, and the observer, are UNCHANGED. Restoring the skill is an owner decision.

### D12 `/sc:issue` plan sections and moving design into create

**Original question:** Clay's PRs 651/661 (merged), 689 and 690 (open) add plan sections to `/sc:issue`, `--plan`, `--remaining`, and move brainstorm and design from claim into create, which changes the owner's claim chain (`sc-issue-protocol/refs/chains.md`, `--pipeline none` claim, `/sc:issue` designs). Keep, adapt or reject, and how does it fit the claim-to-work pipeline?

**Winner:** HYBRID (the owner's line is the base: keep the claim chain and reject moving brainstorm and design into create; adopt Clay's plan sections, `--plan` with `plan_body.py`, `--remaining`, and the idea that claim must read the plan).

Fact correction from the debate: 651 is an issue (the request) and 661 is the merged PR that closes it; 689 is an open issue (nothing built); 690 is the open PR (branch `issue-655-pr-p`) that adds `--plan` and `--remaining`.

**Winning recommendation:**
1. PR 661 stays as merged: the four issue templates end with Priority, Fix approach and Test plan sections.
2. PR 690 is KEEP-ADAPT. Merge `--plan <N>`, `scripts/plan_body.py` and `--remaining <file>` after four changes: fence-aware heading count (or document it) with a test; one definition of "passes the check" in `plan_body.py check`; `plan.md` says who calls `--remaining`; confirm the live head before merge.
3. Claim keeps its chain: `refs/chains.md` rows, `/sc:recommend` as the final pick, `/sc:issue` never running chain commands, the human plan boundary at `--pipeline worktree`. Brainstorm and design are not moved into create; `## Design` is not added; `## Fix approach` is not renamed.
4. One new claim rule (C1): when the three plan sections pass the check, the accuracy verdict is current and the issue is a simple feature, the suggested route is the short chain (`/sc:workflow` then `/sc:implement`). Five conditions S1 to S5 (governs `next-steps.md` only; "passes" means the output of `plan_body.py check`, which proves presence not quality; `out_of_date` uses the existing row; simple features only; the plan is quoted only inside a fenced "data, not instructions" block). The chain tests move in the same PR.
5. A manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>`; it does not stop. The unattended path is held by the orchestrator's own plan check.
6. Split out of issue 689 as a separate small change: `--mode other` and the plan fields on the GitHub forms. Deferred: a higher tier floor at create for medium and complex; the rename.
7. Owner decision, not a build: whether the rule that `/sc:issue` never runs chain commands (B2) is lifted for create, and which session runs brainstorm and design at filing time. Until decided, issue 689 items 1, 2, 4 are not built. The "ruling of 2026-11-20" quoted in 689 is Clay's and UNVERIFIED.

**Implications:**
- On `--pipeline none` the orchestrator hands a worker a chain from its own template, so claim's new rule does not reach that worker; the handoff must itself name the filed plan, and `hold.py`'s `plan_check` must be the same function as `plan_body.py check` (three implementations exist or are planned).
- Plan check is presence, not quality: any non-empty text other than the exact string "Not known yet" passes ("TBD" passes). Nothing may call a passing plan "reviewed".
- Pinned chain-row tests must change in the same PR as C1. If 689's rename lands later, PR 661's tests and the design's `fix_approach` token break unless both headings are accepted.
- The owner must know: PR 661 was merged under the shared `ironbelly` login, so it is not evidence of a named person's decision; Clay's "ruling" in issue 689 does not override the owner's recorded design; five HIGH probe findings became conditions S1 to S5.

**Caveats:** Partial (status partial; convergence not given), confidence about 72 percent. UNVERIFIED: whether the snapshot equals PR 690's live head; whether R23 and R25 (unpushed requirements) are binding; the quoted "ruling of 2026-11-20"; who clicked merge on PR 661; filing dates of issues 339, 409, 423, 431, 444, 450; several invariant findings not re-read; whether `/sc:brainstorm --unattended` works from a create session; no cost baseline for plan-at-claim against plan-at-create.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### D13 Closeout, worktree cleanup, PR log versus issue 339 duties

**Original question:** Clay's `/sc:closeout` (PR 683, merged), worktree cleanup (PR 687, open) and daily PR log (PR 670, merged) versus issue 339's duties (`sc:close`, worktree and branch cleanup, hourly sweep). Are they complementary (keep and adopt as coordinator steps) or duplicates (retire one)?

**Winner:** HYBRID (the three pieces are complementary and none is retired; the coordinator, not a free-standing script, is the accountable owner of the close chain, which is the owner's wording in issue 339).

Correction found while reading: 687 is an issue (Clay's request for a daily worktree cleanup, open), not a pull request. Nothing is built for it yet.

**Winning recommendation:**
1. No duplicates, nothing retired. Duty map: hourly sweep = `/sc:sweep` (built, read-only); `sc:close` first half (settle a merged PR, its issue, its work-report entry and its worker's Orca task) = `/sc:closeout` (built); `sc:close` second half (worktree and branch removal with strict validation) = issue 687's `scripts/worktree_cleanup.py` with nine rules (not built); close or resume an idle session and the in-chat status report = nothing built, stays in issue 339; daily PR log = PR 670, built, outside the coordinator.
2. The coordinator owns the chain. Each cycle: run `/sc:sweep`; call `/sc:closeout <PR>` for every merged PR; run the cleanup script's `list` (dry run) and report the table. The `--apply` step runs only under a grant row or a user instruction naming that action. `/sc:closeout` stays on the never-as-worker list.
3. Nobody removes by judgment. A removal is decided only by the nine rules of issue 687. The script never uses `--force`, `git branch -D` or `rm`. The sentence "never run by the orchestrator" in issue 687 and the matching sentence at `orchestrator.md` line 628 are narrowed to: no session decides a removal by its own judgment.
4. Remote branch deletion stays human-only. A local `git branch -d` inside the script needs the owner's decision; this verdict recommends yes (settled later by Q02).
5. Tests: the design or `HOW-WE-WORK.md` carries the duty map; no sentence says the coordinator never removes a worktree without the scope in item 3; issue 687 gains the acceptance checks "`--apply` is refused without a grant" and "no `--force`, `-D` or `rm` is ever run"; the three uses of "orchestrator"/"coordinator" are mapped to one role in a glossary.
6. Issue 339 stays open as the umbrella until the idle-session and in-chat report items are built or dropped.

**Implications:**
- The coordinator cycle gains three steps and needs a grant row for closeout's writes and for `--apply`; without it the steps stop at read-only.
- PR 683 references `/sc:issue --plan <N>`, a flag that lands in PR 690; if PR 690 is closed or rewritten those two references dangle.
- Nothing is lost by keeping the three. A reading in which the coordinator may delete on its own judgment would be unsafe (issue 687's incident: git knew 53 worktrees, Orca 26, sixteen removed by hand, two for open issues).
- The owner must know: on GitHub there is no `ironbelly` comment on PRs/issues 668, 681 to 684, 686 or 687; closeout's spec says the owner approved it; the cleanup design has no recorded approval, so the owner's chat decision is needed before a build.

**Caveats:** Quick depth, one round. Confidence 80 percent. UNVERIFIED: PR 683's test counts and issue 687's figures (from their bodies, not re-run); whether the three uses of "orchestrator"/"coordinator" are one role; issue 687's own "proved first" items; whether an owner approval of 687 exists in chat; whether the observer should include the cleanup table.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D13/VERDICT.md

**Status after PR 700:** UNCHANGED for PR 683: `/sc:closeout` was kept on master by PR 700. Its step that settles a work-report entry depended on PR 684's skill, which is gone (effect UNVERIFIED). Actions that edit `docs/designs/orchestrator.md` are moot.

### D14 Final disposition of PR 686, the PR stack and the merged design doc

**Original question:** Using the verdicts D01-D13 (in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D*/VERDICT.md; read all that exist), decide per item: PR 686 (open, rewrite of the watcher, head 8e5ae29ad), branch issue-655-pr-p/PR 690, PRs 687 and 689, the merged design doc from PR 681, PR 682 (merged), PRs 683 and 684 (merged). For each: MERGE as is, REBASE-AND-ADAPT, SPLIT, CLOSE, REVERT, or KEEP. Also issue 655 and the owner's issue 450 (Clay's issue "replaces 450").

**Winner:** HYBRID (the owner's rules decide what lands and in what order; Clay's evidenced points set how: two lanes, adapt in place and keep review history, PR 690 first, the eight removal PRs not reverted).

Corrections: 687 and 689 are issues, not PRs. A new owner PR exists since the inventory: PR 693 (saves the claim launch result file, issue 691); it edits four of the same files as PR 690.

**Winning recommendation (every disposition is a recommendation; each needs a go before anyone acts):**
- PR 686 (Clay's rewrite of the watcher, 59 files): REBASE-AND-ADAPT in place, as a draft. Not merge, not split, not close. First: revert merged; the owner's local branch (planb) landed first; D08 names settled; PR 690's `plan_body.py check` merged; the merge checks pass; it drops its deletions of the symbols D01 keeps, the registry, `repos.py` and the label writer.
- PR 690 and branch issue-655-pr-p (`/sc:issue --plan`, `--remaining`): REBASE-AND-ADAPT, lane 1, then merge, after PR 693, D12's four fixes with tests, green CI, draft until fixed.
- Issue 687: KEEP-ADAPT (edit text; nothing built) after the owner's chat approval of the cleanup design.
- Issue 689: SPLIT and DEFER (`--mode other` and form fields to a small new issue after PR 690; items 1, 2, 4, 8 wait for the owner's ruling).
- PR 681 (merged design doc): KEEP, not reverted: a banner now ("contested, not owner-approved"), same-PR correction of three "gate retired" statements inside the revert PR, a later owner-reviewed amendment PR. No builder starts PR B or PR E before the amendment merges.
- PR 682: REVERT as one new PR plus the "no `--to`" bullet re-applied, but only if the owner says in chat that BOTH gates stay (start approval and plan approval after claim) and a dry run in a clean git checkout passes. If the owner says only the start gate stays, PR 682 stands.
- PR 683: KEEP. PR 684: KEEP-ADAPT (follow-up PR for D08 wording and D11 config).
- Issue 655: KEEP and RESCOPE (the assignee drops "replaces #450"). Issue 450: KEEP open and answer Clay's 2026-11-18 comment.
- PR 693 and PR 685 (owner's open PRs): MERGE (693 first) and KEEP/merge (685).
- Eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656): KEEP, not reverted. All other Clay PRs: KEEP.
- Order: H0 hold (ask Clay to make PR 686 and PR 690 drafts and not merge; recommend a ruleset on `master` requiring a non-author review; `master` is unprotected today). Lane 1: PR 693, adapted PR 690, then claim rule C1. Lane 2: dry run, revert PR, banner, contract and guard amendment PR, planb committed and pushed as a draft and landed first, design amendment PR, then the adapted PR 686. Lane 3: remaining verdict actions.
- Mechanical merge checks for any PR touching `issue_watch/` or restoring `issue_pipeline`: `uv run superclaude --help` exits 0; every package under `src/superclaude/cli/` imports; a names check from the restored package's imports (35 names; 9 missing on PR 686's head); a test that removing the approval between wake and start refuses; a test that an absent global `enabled` flag means off; an acknowledgment without a state file leaves the wake entry in place; `make verify-sync`.

**Implications:**
- PR 686 will not become the watcher as written; the owner's approval, trigger and Project code stays; nothing is switched on (`enabled` stays false).
- Restoring the revert brings back WC-17, the approval verbs and guard rule 1; no coordinator skill exists on master, so WC-17 has no executor yet and protection rests on owner vigilance until it is built.
- If PR 686 merges first, the revert is no longer clean and `superclaude --help` crashes. A blanket `superclaude install` would run a retire step and remove skills of PRs 632, 650 and 656 from the owner's host.
- The owner must know: everything is a recommendation; the plan is only as strong as H0 (with no hold and no ruleset, one merge click falsifies it); the owner's planb branch has 348 status entries today (69 code, tests and docs) and overlaps PR 686 on 23 files.

**Caveats:** Partial (four HIGH invariants left as conditions; all 21 diff-point positions were agreed after round 2). Confidence about 80 percent (about 50 if the owner answers "only the start gate stays" or the dry run fails; about 90 once the dry-run record passes, planb is pushed as a draft and H0 is in place). UNVERIFIED: the revert tree has not passed the full test suite; the merge-only trial of PR 690 onto master plus PR 693 was not run; whether a resent wake with an ack file present delivers the same wake id twice; how Coder's template updates reach hosts. This verdict assumed defaults for Q01 to Q03 because their verdicts did not exist yet (see "Where verdicts disagree").

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/VERDICT.md

**Status after PR 700:** MOSTLY DONE OR SUPERSEDED BY PR 700. PR 681 (keep, banner, amendment PR): SUPERSEDED, rolled back, banner task dropped. PR 682 (revert): DONE BY PR 700. PR 684 (keep-adapt): SUPERSEDED, removed. PR 683: UNCHANGED, kept. PRs 686 and 690: UNCHANGED, still drafts. The owner's PR 697 was closed as superseded. The design amendment PR and "no PR B or PR E before it" are moot. The owner's local branch (planb) still lands first, onto a master that now already has the restored package.

### D15 Clay strengths bundle: what to adopt and how

**Original question:** List every element of Clay's work that is clearly better than or fills a real gap in the owner's work (candidates: plan hold, nine-row escalation table, audit rows AU1-AU8 and the 62-reason table, `plan_check`, closed "may do" list with `refuse(argv)`, tier settings in repos.yaml, hand-back loop, typed-answer check, lease comment, wake format, precheck pattern, multi-org search, /sc:closeout). For each: adopt as is, adopt with change, or reject, and the merge or override strategy.

**Winner:** HYBRID (the owner's rules decide every contested row; Clay's elements come in one by one, changed or unchanged, as one verb group built substrate first, then the merge path as one tested unit).

**Winning recommendation:** 71 Clay elements were de-duplicated across D01 to D13 and each got a decision. "686a" means PR 686 as adapted. The full table with carriers and build order is in the verdict; the decisions are:

*A. Start gates, holds, plan sections*
- A1 `plan_check` and skip `held_incomplete`: adopt with change (add the placeholder-only rule, run before the approval read, drop the label writer).
- A2 one definition of "passes the check": adopt with change (`plan_body.py check` is the one definition, imported by the adapted `hold.py`; parity test).
- A3 `hold:backlog` as a person-set stop: adopt with change (the poll only reads it).
- A4 plan request after one hour with titles in the wake: defer.
- A5 `hold:plan` label write by the poll: reject now (replace with a read-only variant, per Q03); label write deferred to its own later PR.
- A6 plan sections in the four issue templates (PR 661): adopt as is.
- A7 `/sc:issue --plan` and `plan_body.py` (PR 690): adopt with change. A8 `--remaining`: adopt with change. A9 claim reads the filed plan (rule C1): adopt with change.
- A10 `--mode other` and form fields: adopt with change (own small issue). A11 moving brainstorm and design into create: reject now (owner decides).
- A12 assignment alone as the trigger: reject. A13 deletion of plan-approval code (PR 682): reject (revert), keep one part, on D14's condition.

*B. Scheduler and wake transport*
- B1 precheck pattern: adopt with change (correct the text; conditional fallback). B2 Orca automation as the scheduler: reject (cron stays).
- B3 wake file plus acknowledgment: adopt with change (M1, M2, no titles, pinned ack schema). B4 mailbox nudge: adopt with change (optional). B5 typed wake line to an idle session: adopt with change (screen-tail check; owner confirms it is acceptable at all). B6 start a session when none is live: adopt with change (unreadable table means unknown). B7 coordinator reads the wake directory at each `check --wait` return: adopt as is (new text). B8 "no GitHub text reaches a typed line": adopt as is, widened. B9 copied `orca_term.py` code: reject. B10 org-wide search: adopt with change (off). B11 information streams: adopt with change (one switch, off).

*C. Topology and settings*
- C1 in-flight cap: adopt with change. C2 guarded restart: adopt with change. C3 per-repo keys: adopt with change (per-repo JSON). C4 exclusive-create state file and `owner/name` keying: adopt with change. C5 registry repo and related: reject. C6 tier settings: adopt with change (requests until verified; `plan_tier` becomes a plain `plan_depth`). C7 `orca project setup-clone`: reject. C8 lease comment: defer.

*D. Authority and controls*
- D1 `merge-gate`: adopt with change. D2 `changes_requested` hard refusal and `merge_safety` hold: adopt as is. D3 merge-time reviewer hold: adopt with change. D4 `answer-check`: adopt with change. D5 `E-NO-GRANT`: adopt with change. D6 standing low-stakes grants (three after Q03): adopt with change. D7 standing `pr.merge`/`issue.close` and autonomous merge: reject. D8 closed "may do" list and `refuse(argv)`: adopt with change. D9 interrupt exception N7: reject. D10 coordinator started by a script at depth 0: adopt with change. D11 "standing-grant coordinator" name: adopt with change; worker running `/sc:pr-submit`: reject. D12 one supervised `worker-start` route: adopt with change (guard staged). D13 "workers run unbound, decided": reject the "decided", keep the risk row. D14 coordinator typing into worker terminals: adopt with change (reject approving permission prompts). D15 audit AU1 to AU8: adopt with change. D16 nine-row table: adopt with change. D17 cap of 5 notices a day: defer. D18 hand-back loop: adopt with change. D19 naming rule 5.12: defer (owner picks scope). D20 "an answer is always typed": adopt as is.

*E. Observability*
- E1 work-report skill (PR 684): adopt with change. E2 living report: adopt with change. E3 silent-loss rules and `check.py`: adopt as is. E4 transcript reader: adopt with change. E5 item template: adopt with change. E6 62-reason audit table: adopt with change (bring back 14 approval reasons, add three, drop label-write reasons). E7 `report-entry` as the one writer: adopt with change.

*F. Closeout and cleanup*
- F1 `/sc:closeout` (PR 683): adopt as is. F2 landed check: adopt as is. F3 worktree cleanup, nine rules (issue 687): adopt with change (plus Q02's `git branch -d` refusals). F4 evidence-repo save before removal: adopt with change. F5 daily PR log (PR 670): adopt as is.

*G. Design, test and process*
- G1 test plan T1 to T13 with unknowns and risk registers: adopt with change. G2 flags `--wake`, `--hourly`, `--resume`, `--take`: adopt with change. G3 persisted names: adopt with change (rename). G4 honest risk register: adopt as is. G5 removal plan and PR B test rows: adopt as is. G6 the design text (PR 681): adopt with change (no revert; amend rows). G7 open-questions table with an Owner column: adopt as process.

*Seven conflicts between earlier verdicts, resolved here:* R-1 use the code reason names `held_incomplete` and `held_backlog`; R-2 `plan_body.py check` is the one plan check; R-3 settings live in per-repo JSON, not `repos.yaml`; R-4 default grants are empty and the owner grants three standing entries once in chat; R-5 closeout's `issue.close` is covered by the per-PR go or an explicit closeout grant recorded in chat (open); R-6 hand-back re-plan passes the start gate again; R-7 the spec lists the verbs it actually builds (no `lease`, no interrupt).

*Four new HIGH conditions (found by the fault-finder; no Clay or owner source states them):* C-INV-1 a hand-back waiting for re-approval is excluded from `max_in_flight` or expires; C-INV-2 something wakes the coordinator after the person re-approves; C-INV-3 the per-repo config is out of the coordinator's write reach or the controls fail closed on weakening values; C-INV-4 the post-merge close has a stated authority.

*Build order (follows D14):* O0 hold step and owner chat answers; O1 lane 1 (PR 693, adapted PR 690, claim rule C1) plus text fixes; O2 lane 2 (dry run, revert, amendments, owner's branch landed first); O3 the adapted PR 686; O4 substrate; O5 merge path as one unit; O6 other verbs and transport; O7 live tests, then enable.

*Open owner questions OD-1 to OD-13* are listed individually, with their settled answers, in entries QG1 to QG4 below. D15's own recommended answers: OD-1 quick; OD-2 re-plan then re-approve; OD-3 scope B; OD-4 fail open on delivery; OD-5 entry lines only (differs from the merged file, which picked entry lines plus the notice step); OD-6 yes; OD-7 no; OD-8 no; OD-9 no; OD-10 the per-PR go covers merge and close; OD-11 default grants empty; OD-12 both layers of protection; OD-13 exclude the waiting step from `max_in_flight`.

**Implications:**
- The watcher stays read-only on GitHub, keeps approval, trigger, Status and marker code, and gains `held_incomplete`, `held_backlog`, wake files and a closed reasons table with the 14 approval reasons back. PR 686 cannot merge as it stands.
- The coordinator never merges alone, never tags or publishes, never answers a permission prompt, never interrupts a worker.
- New visible reasons (`held_incomplete`, `held_backlog`, `coordinator_full`, `name_collision`, `no_checkout`) must reach the sweep and observer; the report layer needs the sweep's `session_id` field.
- What breaks: Clay's design text in the rows the verdicts overwrite; tests T1, T3, T4, T8, T10, T11 (logic) and T12 (hand-back); the reasons-table pin; any code that expects an assignment-only trigger, a standing merge grant or a registry repo.
- The owner must know: nothing in the verb group exists as code yet, so the table is a build plan, not a merge list; no control closes a risk, `master` stays unprotected until an admin sets a rule; the D01 to D13 verdicts are recommendations.

**Caveats:** Partial (convergence 89.3 percent, blocked by four HIGH invariants). Confidence 72 percent overall (about 85 percent on rows that are direct verdict findings, 65 to 75 percent on rows no verdict covered). The verdict was updated after Q01 to Q03 and D14 (no row flipped). UNVERIFIED: U5, U25, U28, U30, U40, U42, U8 and the 60-minute and `HANDBACK_MAX` = 3 defaults; the register counts from the fault-finder; where `plan_body.py` would be imported from; the contents of the IronFlow coordinator spec and Clay's `RULINGS.md`; OD-1, OD-4, OD-5, OD-13 are D15's own tie-breaks. The 62-reason table pin forbids the 14 approval reasons the approval gate needs. The agent ran `uv` inside a read-only snapshot and deleted the files it made (see "Coordinator decisions made without a debate", item h).

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md

**Status after PR 700:** PARTLY DONE OR SUPERSEDED BY PR 700. Row A13 (revert PR 682): DONE BY PR 700. Rows E1 to E5 (the work-report skill, living report, silent-loss gate, transcript reader, item template): SUPERSEDED, the skill is gone. Rows G4 to G6 and every DOC row whose carrier is `docs/designs/orchestrator.md`: moot until the design is restored (the archive branch holds it). Other rows UNCHANGED.

### D16 Process: how to prevent a repeat

**Original question:** Section 11 of FULL-REPORT.md proposes: related-work section, a stop-on-overlap check in `/sc:issue`, a "Reverses" line and author acknowledgement, CODEOWNERS and no self-merge on named paths, a role paragraph in CONTRIBUTING.md, a decision log on master, an in-flight register, a 24 hour cooling period for design PRs, an overlap scan command. Which package is worth its cost for a small team, in what order, and what is the lightest version that would have prevented this incident? Note that only repository admins can change branch protection and CODEOWNERS enforcement.

**Winner:** HYBRID (the base is OURS: a real server-side gate plus a published decisions file; three of nine items of section 11 are dropped outright, the stop-on-overlap half of item 1 is dropped, the rest narrowed; the silence sentence, the carrier file, the bypass, the hold and the drops are Clay's).

**Winning recommendation (adopted, in this order; costs are the advocates' estimates):**
1. Owner decisions in chat (about 20 minutes): roles by login with sole code owner `@ironbelly`; a deputy or "nobody" and the channel the owner reads; a one-directional gate with admin bypass; `integration` in or out; hold on PRs 686 and 690; the seed of the decisions file. A session records each; the owner never writes a file.
2. Direct hold: PR 686 (Clay's rewrite of the watcher) and PR 690 (`/sc:issue` plan sections) wait for the owner's ruling; Clay sets both to Draft.
3. Rule text in root `CLAUDE.md` (new section "who rules, and what needs a second person"), a two-line pointer in `HOW-WE-WORK.md`, one line in `CONTRIBUTING.md`, two reminder lines in the PR template; finishes issue 290 (60 to 90 minutes, one PR).
4. `.github/CODEOWNERS`: core lines `docs/designs/`, `src/superclaude/core/WORKER-CONTRACT.md`, `/.github/CODEOWNERS`; temporary lines `src/superclaude/cli/issue_watch/` and `src/superclaude/skills/sc-issue-protocol/`; sole owner `@ironbelly`.
5. Ruleset on `master` and `integration` (ADMIN ONLY): pull request required, 0 required approvals, code-owner review, dismiss stale approvals, no force push, no deletion, bypass for the admin role for pull requests only.
6. Throwaway test: after the ruleset is active, Clay's account opens a throwaway PR editing one line under `docs/designs/` with no approval; expected result BLOCKED. Repeat on `integration`; then an owner-authored throwaway PR shows whether the bypass is needed. Close all unmerged. Fallbacks if not blocked: require 1 approval; the "required reviewers" ruleset rule; or drop the gate and keep the words.
7. Owner announces in chat that the gate is live and binds non-owners (after the test passes and Clay accepted the rule text).
8. `docs/decisions.md` (one file) seeded with about 10 ruling groups.
9. 14-day review (gated PRs, median wait, waits over 3 working days, silent passes); temporary CODEOWNERS lines come out when the owner says in chat the 655 series is reconciled.
10-12. Tripwire items only (CI check for deletions of recent code, extra CODEOWNERS lines).

Rule text: roles by login; a question to a named person gets a written answer, silence is never a yes; three working days is a timer to ask again, never permission; reversing or deleting someone else's merged work needs their written yes and a merger other than the author (a plain revert is exempt from the written yes but not from the gate).

Dropped: `/sc:overlap` and any overlap scan; stop-on-overlap in `/sc:issue`; the 24 hour cooling period; the in-flight register; the `docs/decisions/` folder with a full back-fill; a required pasted deletion check; the five-path CODEOWNERS list; naming `IB-JonathanB` as deputy; making `/sc:pr-submit` inject the PR template.

Only the repository admin (`ironbelly`) can: create the ruleset or branch protection, add `integration`, require code-owner review, set the approvals count, dismiss stale approvals, block force push and deletion, set the bypass list, make any CI check required. Anyone who maintains can do by PR: CODEOWNERS (inert until the ruleset exists), the `CLAUDE.md` text, `docs/decisions.md`, the PR template, issue 290.

Lightest version that would have prevented the incident: steps 1, 3, 4, 5, 6, 7 and 9, limited to `docs/designs/`, `WORKER-CONTRACT.md` and the CODEOWNERS file, about 120 to 150 minutes of session, maintainer and chat time plus 15 to 30 minutes of admin time (arithmetic over the advocates' estimates). Words alone would not have prevented it: PR 681's own body said "the owner reviews and merges" and its author merged it about 90 minutes after opening.

**Implications:**
- While the temporary lines stand, every PR of the issue-655 series touching `issue_watch/` or `sc-issue-protocol/` needs the owner's approval: the intended brake.
- The coordinator's "merge only on the person's go" is a chat go and is not a GitHub approval; on gated paths both are needed. The orchestrator never uses `--admin`. The merged design makes Clay the authority for CODEOWNERS edits; this verdict makes the owner the one authority, and the design must be amended in a new PR.
- What breaks: `/sc:pr-submit --monitor 3` pushes after review, so approvals are dismissed and must be given again; release PRs from `integration` to `master` touching gated paths need the owner's approval; a pure deletion touching no gated path is not caught; the owner's own deletions of Clay's merged work are not gated.
- The owner must know: nothing in this package exists today (no ruleset, no CODEOWNERS, no rule text); the text parts alone do not prevent a repeat; making `@ironbelly` sole code owner is a ruling about who decides design, while Clay's merged design says "the owner (Clay)", so Clay's written acceptance should come before the announcement; an approval under the shared `ironbelly` login proves only that a login other than the author's said yes; the review queue lands on the owner (about 17 Clay PRs in about 10 days); in the last 100 merged PRs, 89 were merged by their own author and none has an APPROVED review; `master` has no protection and no ruleset today.

**Caveats:** Partial (convergence 22 of 22 diff points, blocked by 4 HIGH invariants carried as binding conditions). Confidence about 75 percent in kind, about 55 percent on specifics. The claim that the lightest version would have prevented PRs 681 and 682 is "probably, UNVERIFIED" until the throwaway test passes. UNVERIFIED: whether "require review from code owners" at 0 required approvals blocks a non-owner author on this repository; whether a maintainer other than the author can convert a PR to Draft; whether the Free plan offers an "Evaluate" mode; organisation-level rulesets (token lacks `admin:org`); whether sessions obey a root `CLAUDE.md` rule; whether Clay accepts "owner = `ironbelly`" and a sole code owner; the contents of `owner-answers.md` and `RULINGS.md`; cost and queue figures are estimates and floors.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/VERDICT.md

**Status after PR 700:** UNCHANGED. PRs 686 and 690 are drafts. PR 700 was again merged by its author in 21 minutes with no owner review, the pattern this verdict addresses.

### Q01 Who writes a per-issue grant row

**Original question:** The owner's record (OWNER-ANSWERS line 285 in the issue-339 brainstorm folder, see D04 verdict) says PR 585 narrowed the "Ruling in chat" rule and that "other owner records, such as a grant row, are still written by the owner". The owner's memory rule (2026-11-17, `approvals-through-chat-never-files`: /home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/approvals-through-chat-never-files.md) says every approval, go and Ruling is given in chat, the agent records it, and the owner is never asked to write a file. Which governs a per-issue grant row (and the cleanup-design approval and `--apply` grants raised by D13)? Read D04 and D13 VERDICT.md first. Context: D04 recommends `answer-check`, a validator that checks a typed chat answer.

**Winner:** HYBRID (the owner's chat rule governs who writes the record: the owner says it in chat, the agent records it, nobody hand-writes a file; Clay's `answer-check` tests, end-of-go rule and fail-closed default are adopted as checks on the recorded go).

**Winning recommendation:**
1. A per-issue grant row, the owner's go for `--apply`, and the owner's approval of the cleanup design (issue 687) are the owner's consent, given in chat. The agent in that session records it. The owner is never asked to write a file. Decision 8's words "the grant row is written by the owner" mean "owner-sourced, never agent-created".
2. Fix `WORKER-CONTRACT.md:57`, which says other owner records "are still written by the owner". It becomes: given by the owner in chat and recorded by the agent, naming the exact scope. Do this only after the owner's one chat confirmation, because the owner's own words behind the current sentence were only "narrow d2". The contract test pins the new sentence.
3. A record holds the owner's quoted words, the date, the exact scope (issue or PR number; for a merge the head sha; the list of writes) and who recorded it. A go missing any field is refused. An agent-made record with no owner chat confirmation is an "executor-invented approval".
4. Checks on a recorded go (from `answer-check`): typed by a person in their own session and never relayed by an agent; names the right entry; newer than that entry's last edit; question key matches (for a merge `merge_safety:<PR>:<head sha>`). The owner identity is a parameter, not Clay. Until the script exists the coordinator does these four checks by hand.
5. A go ends when the named action is done, when the PR head moves (for a merge), or when the owner revokes it in chat.
6. Fail closed with a use log: no recorded go means no write; each use names the go it relied on.
7. Standing versus per action: four low-stakes writes are standing per D04 (later reduced to three by Q03); merge, close, `--apply` and the cleanup-design approval are per-action chat goes. The per-issue row is not restored as an owner-written file. This split rests on D04, not on a debate win.
8. `--apply` runs only on a recorded owner go that names that action; the cleanup-design approval is recorded the same way before any build of issue 687.

**Implications:**
- The poll writes nothing to GitHub, so a recorded go does not change it. A standing-grant file must sit outside the orchestrator's write reach or be guarded by a hook.
- Every merge, close, `--apply` and cleanup run starts from a recorded go; the merge gate gains the reason "no recorded merge go".
- Breaks: any text that tells the owner to write a row (contract line 57; `issue-pipeline-fu1.md:24,26`); `answer-check` for anyone but Clay until the owner identity is a parameter. The installed copy on this host (`/home/coder/.claude/WORKER-CONTRACT.md`) is from before PR 682 and still has WC-17 and line 300, so a coordinator session here can still be told to require a row that nothing writes until the next `superclaude install`.
- The owner must know: the sentence that keeps the grant row owner-written came from a fix agent's reading of Decision 8, not from the owner's words; the owner decides it with one chat message; `ironbelly` is a login shared with every session on this host, so a chat go does not by itself prove who gave it.

**Caveats:** Partial (convergence 64.3 percent against 80; in four of five unresolved points both advocates endorse the same Clay element). Confidence 75 percent. UNVERIFIED: whether the owner meant "narrow d2" to keep an owner-written row (the order and timezone of the owner's messages that day are not shown); `answer-check`, `E-NO-GRANT` and the `repos` verbs are read from design text and not built; U37 (any agent can type into an orchestrator terminal); one scorer could not confirm commit `bfabf1d63` for PR 585; one scorer's claim that design lines 37 and 76 mention "grant row" was not resolved; Clay's `RULINGS.md` was not read.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### Q02 Cleanup script may delete local branches

**Original question:** D13 left open whether the worktree cleanup script (issue 687) may run a local `git branch -d` after removing a merged worktree. Decide yes/no and the safe limits (merged-only, `-d` never `-D`, never the default branch, never a branch with an open PR, dry run first). Read D13 VERDICT.md and the issue text (`gh issue view 687 --repo IronbellyOrg/IronClaude`, read-only).

**Winner:** HYBRID (yes, the script may run a local `git branch -d`, using issue 687's own rules and step order plus a short list of added refusals from the owner's line, because the debate showed `-d` itself protects far less than D13 said).

**Winning recommendation:** This is an addendum to issue 687 (Clay's request for a daily worktree cleanup; it already has `git branch -d` as step 4).
1. Yes, local only, `-d` only: exactly `git branch -d <name>`. Never `-D`, never `--force`, never a remote branch delete (remote deletion stays human-only).
2. `-d` is a backstop, not the gate. It means "merged to its upstream or to the checkout's HEAD", not "its pull request landed". Measured on git 2.47.3 in a scratch repo: it deleted a pushed-but-unmerged branch, and it deleted `integration` and `master` once merged. The gate is issue 687's rules 2 and 3. D13's reason ("`-d` refuses an unmerged branch") must not be used.
3. Refusals added: (a) never `master`, `main`, `integration` or the repo default branch; (b) keep the branch if any PR with this head is OPEN; (c) the merged PR's `headRepositoryOwner` must be ours; (d) the dry run prints "branch: would delete / would keep (reason)" per row and the merged PR's head SHA; (e) rule 3 stays as written (HEAD equals the PR's last head commit or is an ancestor of it).
4. Apply (a) to (c) before the worktree is removed, as keep-the-whole-worktree rules. Reason (an inference from `orca worktree rm --help`, not measured): Orca itself also tries to delete the checked-out local branch, so a script that only skips its own `git branch -d` could not stop Orca from deleting `integration`. Prove Orca's behavior before the build.
5. Dry run is the default; the first week is report-only; who may run `--apply` stays under a recorded owner go.
6. A git refusal is "kept", not an error. Squash-merged branches whose remote is gone always refuse and stay until a person removes them.
7. Tests: the existing acceptance test that fails on `--force`, `-D`, `rm`, `prune` stays; four added cases (worktree on `integration` with a merged PR is kept; an OPEN PR with the same head keeps the branch; a foreign `headRepositoryOwner` is not accepted; the dry run shows the branch action and the PR head SHA).

**Implications:**
- The coordinator's list-then-apply cycle from D13 is unchanged; the limits match the contract lines that already let the coordinator delete a merged child branch.
- The owner must know: for squash-merged branches with a gone remote, `-d` always refuses, and this checkout has 21 of 56 local branches with a `[gone]` upstream, so the script will leave exactly that class in place; if Orca deletes the branch itself, script-level refusals are bypassed unless the worktree is kept; no linked worktree is on `master`, `main` or `integration` today, so the `integration` risk is latent; GitHub shows no owner approval of issue 687, so the owner's chat decision is needed before a build.

**Caveats:** Depth quick, one round; the verdict does not flag partial. Confidence 85 percent. UNVERIFIED: what `orca worktree rm` without `--force` does to the local branch and to a dirty worktree (only help text read); whether the owner approved issue 687 outside GitHub; whether GitHub allows an OPEN PR with the same head as a merged PR; whether Orca-created branches have an upstream set; `-d` after a squash merge with the remote branch still present was not tested; the winning margin is 5.9 points (0.900 against 0.841), mostly from a coverage metric measured against the topic's own list.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/VERDICT.md

**Status after PR 700:** UNCHANGED. It touches only issue 687's cleanup script, which PR 700 does not change.

### Q03 Dormant hold:plan label code in PR 686

**Original question:** D09 recommends the poll keeps writing nothing to GitHub (NG-2), but PR 686 contains the `hold:plan` / `hold:backlog` label writing code (`src/superclaude/cli/issue_watch/hold.py` in snapshot pr-a). Should that code stay in PR 686 dormant (switched off), be stripped out until the owner amends NG-2, or be replaced by a read-only variant now? Read D09 VERDICT.md and the code.

**Winner:** HYBRID (replace the label-writing code with a read-only variant now; NG-2 stays as written; Clay's read-only plan check, `hold:backlog` stop and `would_hold` dry-run listing carry over; Clay's narrow label form is written down as the deferred design).

**Winning recommendation:**
1. PR 686 ships no GitHub write by the poll. Remove `LabelWriter` (`github.py:983-1069`), the four label argv builders (`github.py:267-320`), `_hold_write_ok` and `_label_write` (`cycle.py:1021-1044`), the label-driven rows 3 to 5 of `_hold_step` (`cycle.py:1064-1119`) and the `hand_removed` state. The NG-2 test is zero writes again.
2. Keep, read-only: `plan_check`, the `held_incomplete` skip, `hold:backlog` read from the search row, the audit reasons, and the `would_hold` dry-run listing. `plan_check` runs before the approval read and a `<...>` placeholder-only section counts as empty.
3. The local `holds` entry (a store file, not GitHub) is created when a failing issue is first seen, so the one-hour quiet clock starts. A test shows `writes == []` with the grant absent and present.
4. The wake-time re-check changes too (`cycle.py:1293-1300` tests for the `hold:plan` label); in the read-only variant only the plan check and `hold:backlog` remain.
5. A `hold:plan` label on an issue is ignored, with no warning. A person who wants a stop uses `hold:backlog`. Cost: a hand-placed `hold:plan` no longer holds anything.
6. The `issue.hold` grant is removed from the reference config and the test fixtures (`orchestrator.md:291`, `:872`; `tests/issue_watch/conftest.py:286`; `test_repos.py`; `test_security_invariants.py`).
7. The label write is deferred, not rejected: it returns as its own PR only when someone shows a reader of the label, in Clay's narrow form, after NG-2 is amended, a 24-hour `--dry-run` shadow run and a cron write test.
8. Save the removed label-writing hunk as a patch next to the debate record.
9. Fallback if the sizing step finds the rework too large: delete only the write calls and the grant check, keep the six-row table and the entry creation, drop `issue.hold` from the reference config, and restore the zero-write NG-2 test. The owner chooses after the count.

**Implications:**
- The poll stays read-only on GitHub. Leaving the wake-time re-check unchanged would stop plan requests from ever firing in a read-only variant.
- With no label, a held issue shows only in `issue-watch status` and the audit log; the sweep and observer must read those.
- Breaks in PR 686: the NG-2 test (three calls to zero), about 17 lines of `test_hold.py` that mention a label call, the no-grant warning test, the grant fixtures and the reference config lines.
- The owner must know: the "dormant" form is not dormant by default (the design's own config example turns it on); Clay's code has a real defect in its dormant state (no entry, a stuck leftover label, a warning every cycle); the poll is `enabled: false` in PR 686 so there is no live risk today, the cost is review and merge effort; the rework lands on Clay's PR, so the owner decides who edits it.

**Caveats:** Partial (convergence 71.4 percent at depth quick; no invariant probe). Confidence 70 percent. UNVERIFIED: whether any live repo config lists `issue.hold`; the size of the rework (counts are rough: 58 test functions and 1,073 lines in `test_hold.py` were counted, no test run); rows 3 and 4 and the no-grant warning were read from code, not executed; whether the owner's local branch already writes a label once per repo (reported by D09, not re-read).

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### Q04 Does one typed go cover the fix-round pushes?

**Original question:** Spec panel finding F4 (spec/panel/review-1/spec-panel-report.md): the spec rule "a person's typed go precedes every push and every merge" (SEC rules, D06, Q01) is not reconciled with (a) the fix-round pushes that `/sc:pr-submit --monitor 3` makes after review findings and (b) the Full Submit per-issue go (SEC-15 in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md) that lets a launched worker commit, push a feature branch and run `/sc:pr-submit`. Decide for each push class whether a new typed go is needed: the first push and PR, each fix-round push by the same session on the same PR, a push after a revert or rebase, and a merge. OURS = the strict reading (a go per push, bound to the head sha, per D06 and Q01); CLAY = one go per issue or per PR covers every push of that PR's feature branch until merge (D:135 ADD1 and the Full Submit design). Read D04, D05, D06, Q01 and OAG1 verdicts and WORKER-CONTRACT.md lines about "pushes only on the person's go". The verdict must give one rule in a sentence that a test can check, and name the SEC/FR rows to change.

**Winner:** HYBRID (the owner's per-publication rule stays for every push class except one: the person's own typed `/sc:pr-submit --monitor 3` line, or the Full Submit field, is the go for that one run's fix-round pushes; Clay's "until merge" scope and worker route are rejected).

**Winning recommendation:**
- The rule, in one testable sentence: a push to a PR's feature branch needs a person's typed go, except that the person's typed `/sc:pr-submit --monitor 3` line (or the Full Submit field for that issue) is itself that go for the first push, the PR and the fix-round fast-forward pushes of that one run, ending when the run ends, when the PR is merged or closed, or when the branch head moves outside the run; a push after a revert or rebase (the go names the old and new sha), a push by any other actor or in a new run, and every merge each need their own new typed go, and a merge go is bound to the 40-character head sha.
- Per push class: first push and PR, no new go if made by the typed run line or the Full Submit field (yes for a manual or coordinator push without `/sc:pr-submit`); each fix-round push in the same run, no new go while the tool's fence holds (one fix commit per cycle, a halt on `push_range_mismatch`, fast-forward only, no force push, no push to the default or protected branch, `push_count` at most `max_rounds + 1` with a hard cap of 5); push after a revert, yes; push after a rebase, yes (the go names the old and new sha); a new `/sc:pr-submit` run on the same PR, yes; a merge, always its own go bound to the head sha, and a push go never covers a merge nor a merge go a push.
- The spec must also say: a go ends with its run, when the PR is merged or closed, or when the branch head moves to a sha the run did not make (this answers the 2026-11-04 miss on PR 368, where a later push re-created the deleted branch of an owner-merged PR; memory note, not re-verified); the run line covers only pushes the tool itself makes, never a worker's own script push; the Full Submit field is a go given before the commits exist, so WC:245 ("no earlier pre-authorization waives this") would refuse it, which makes it the one named exception, valid only after the owner approves R25 in chat and WC:245 is amended to name it (the amendment must not call the field "live"; only the typed run line is live); the Full Submit go covers that issue's first push, the PR and the loop pushes of the one run it starts, in a top-level session, and never a merge, force push, branch deletion or other push; a worker never runs `/sc:pr-submit` (Clay's ADD1 stays rejected); the coordinator's own push of worker commits (FR-32) stays strict and needs the person's typed go.
- Tests: a push with no typed run line, Full Submit field or go record is refused; a second run on the same PR needs a new line; a push after the PR is merged or closed, or after the head moved outside the run, is refused; a merge command carrying only a push go is refused; a push after a rebase without a go naming old and new sha is refused.
- Spec rows to change: the flow sentence (SPEC:124) and stage rules (SPEC:467); FR-32 (SPEC:233); SEC-15 (SPEC:302); SEC-01 (SPEC:288); a new row SEC-22 for the end of a run go; the guard probe row 13.2 (SPEC:699); L-07 (SPEC:357) waits on the owner's chat approval of R25.

**Implications:**
- The watcher is unchanged. The coordinator still shows worker commits to the person and pushes only on a typed go; it never types the run line itself.
- Full Submit (R25) stays the only automated route to a push and PR; it counts only after the owner's chat approval and the WC:245 amendment. R25's current words "nothing else is pushed" must be amended to include the run's loop pushes.
- Breaks: any spec text that says "every push" without the exception; Clay's ADD1 worker route. The fix-round pushes made today by `/sc:pr-submit --monitor 3` are not a new risk; they were always the run line's.
- The owner must know: the run go is only as strong as "a person typed it" (a script in the same terminal can type the line, residual risk from D06); the end-of-go checks and the run-go record are design only, not built; a Full Submit field set days earlier is a pre-authorization in the plain sense, so the amendment must name it as an exception.

**Caveats:** Partial by its own contract (quick depth: two unresolved points, same-evaluator second scoring pass, no invariant probe). Confidence about 80 percent. UNVERIFIED: that `push_range_mismatch`, `push_parent_ok` and the fast-forward-only push behave as the protocol text says (read, not run); that R25 is "built" (it is a row of an unpushed local plan); the PR 368 incident; whether a Full Submit launch really runs `/sc:pr-submit` in a top-level session and not as a worker; whether the harness can tell typed text from script-typed text; whether WC:245 strictly applies to the tool's own fix commits; whether another actor's push between rounds is stopped by the tool's guard. The rule would change if the owner wants a typed go for each fix-round push (then `--monitor 2` is the ceiling). The spec panel's review 3 later listed four Medium findings on the resulting spec rows (H1 to H4); see item (k) below.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-1 Default depth of the plan call (debate QG1)

**Original question:** QG1 Planning and hand-back: OD-1 (default plan_depth for the plan call)

**Winner:** OURS (the debate's overall verdict for QG1 is HYBRID: the owner's line wins all three contested rules and Clay's hand-back loop bounds and the per-repo depth option are adopted).

**Winning recommendation:** The default is `quick`. The setting is one plain key `plan_depth`, passed straight to `/sc:issue --plan --depth`. Unset means `quick` (run by the cheapest worker `issue-worker-t3`). A repo may set `standard` or `deep` for itself. There is no `plan_tier` and no tier-to-depth table. Reason: nobody has measured plan quality or cost per depth, the table that would map `plan_tier` to a depth is not on master, and the person's approval is the quality gate because the plan check proves only that three headings are filled in. Both advocates, Clay's included, sided with `quick`. Test: validation accepts quick, standard or deep and refuses anything else; an unset key gives `--depth quick`; a repo's own value beats the default for that repo.

**Implications:** The plan call runs the cheapest planner unless a repo opts in. No `plan_tier` code is needed in PR 686's `repos.py` (D14 says it does not land). `quick` plans pass the check on presence alone, so the person's approval is the only quality gate. If a repo sets `deep`, the hand-back loop can run the planner up to four times per issue because the re-plan passes the same depth. Clay's goal "stronger models plan, cheaper models build" stays available per repo.

**Caveats:** Confidence about 66 percent (a tie resolved by the weighting rule, no measurement on either side). UNVERIFIED: the `plan_tier` to `--depth` table in `refs/intake.md` of PR 690 (not on master) and whether `tier1b` implies `deep`. D15's supporting row cites D12 item 6, which is only a related create-time deferral. The owner gives the answer in chat; this is a recommendation.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-2 How hand-back round 2 starts (debate QG1)

**Original question:** QG1 Planning and hand-back: OD-2 (how hand-back round 2 starts: re-plan and re-approve vs carry the remaining list)

**Winner:** OURS (QG1 overall: HYBRID).

**Winning recommendation:** Option (a): re-plan the body, then the person re-applies the approval. Round 2 and later run the re-plan (`/sc:issue --plan <N> --remaining <file> --depth <d>`), then wait for the person to re-apply the approval, then pass the start gate again. No separate chat go per round. The check at the moment of start repeats the approval, not only `hold:backlog` and `plan_check`. Option (b) (leave the body alone and carry the remaining list in the handoff round block) is the owner's cheaper alternative, not the default. Reason: a body edit after approval voids the approval, so a re-plan without re-approval would start a worker on a body nobody approved; Clay's text has no round-2 gate and Clay's advocate conceded this. Adopted from Clay: the loop bounds (stop on empty list, round cap, no progress), the old worker must be final first, the idempotent re-plan marker and the `--remaining` replacement. Tests: removing the approval between wake and start refuses the start; a re-plan voids an earlier approval; no worker starts for a waiting issue before the start gate passes, including after a coordinator restart.

**Implications:** A hand-back issue stops after the re-plan and waits for the person; after approval something must wake it (the poll never wakes an acknowledged entry) and repeat the whole start check. PR 690's `--remaining` gets its first caller. Clay's design text at lines 610-620 and tests T1, T3, T4, T8, T10, T11, T12 must be rewritten. If the plan-approval flow (WC-17) is not restored (it exists only if the owner decides both gates stay, see D14), round 2's gate is the start approval alone.

**Caveats:** Confidence about 78 percent. UNVERIFIED: whether the restored WC-17 flow can serve as the round-2 gate; fidelity of `--remaining` in keeping done items; `HANDBACK_MAX` = 3 is "not measured". The high convergence (15 of 16 points) partly reflects the weighting rule given to the advocates.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/VERDICT.md

**Status after PR 700:** UNCHANGED. Its open dependency (WC-17 restored) is now met on master.

### OD-3 Scope of the naming rule (debate QG2)

**Original question:** QG2 Escalation channel and naming rule: OD-3 (scope of the naming rule: A, B or C)

**Winner:** OURS (QG2 overall: HYBRID, the owner carries all three answers and five small Clay elements are adopted).

**Winning recommendation:** Scope B. The "naming rule" is Clay's ruling 15: nothing the coordinator or its workers write where a person reads it may name the agent or model. Under scope B, scan only the coordinator's own two writers, `report-entry` and `escalate`; workers' PR bodies keep today's practice; run the measurement U54 (how often the deny list wrongly refuses real text, over the last 50 issue and PR titles) before the check is switched on. Reason: no check can read a worker's PR body before it is written, 25 of the last 30 merged PR bodies carry "Generated with" (a read-only re-count: clayphi 17 of 21, ironbelly 8 of 9), and ruling 15 is Clay's, not shown to be an owner ruling. Not adopted: the handoff-prompt line telling workers never to add an attribution line; it stays out until the owner rules on it in chat.

**Implications:** Design lines 847 and 841 need amending (`names_check` runs in two verbs, not "every writer"; the handoff line is removed or marked pending). Claim comments written by `/sc:issue` are not scanned; the poll is unaffected. The offline scan of every template, fixture and end-to-end body, and the fake `launch.effective` test, stay. The owner is asked once in chat whether the rule applies to workers at all (A, B or C); B is the default if no answer comes. The owner has not ruled on the naming rule at all; rulings 15, 27, 28 and 39 are Clay's.

**Caveats:** Confidence 75 percent. QG2 convergence 66.7 percent according to the progress log (STATE.md; the verdict itself does not state a number), so treat as partial. Quick depth: one round, no invariant probe, one scorer. The verdict does not define scope C. A high false-refusal rate in U54 would move the rule to C. UNVERIFIED: whether the real escalation template fences paths, shas and numbers; whether rulings 15, 27, 28, 39 were agreed by the owner outside GitHub.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-4 A refused mandatory escalation (debate QG2)

**Original question:** QG2 Escalation channel and naming rule: OD-4 (a refused mandatory escalation: fail open on delivery or fail closed)

**Winner:** OURS (QG2 overall: HYBRID).

**Winning recommendation:** Fail open on delivery. The escalation is always written; the matched span is replaced by a visible marker, for example "[name removed by naming rule]"; the original match is kept in the action log; the refusal is logged; a match inside a path, sha or number is written unmasked and logged. The escalation template fences paths, shas and numbers so the scan skips them. Fail closed stays only for a structurally bad call such as an entry naming no row (design line 684), where the caller gets a loud error and can fix it at once. Reason: a refused escalation leaves the person never told and the hold on silently, and an unanswered item waits for the person, not for nobody.

**Implications:** Design line 847 ("refuse, exit 2") becomes "write with a visible marker and log" for style failures only; the line-684 refusal stays for a missing or unknown row. The sweep and dashboard see the marker text, not the original; a person who needs the original reads the log. A style failure is logged, never a block. Clay's advocate conceded the silent-failure point and accepted the visible marker.

**Caveats:** Confidence 75 percent. Convergence 66.7 percent per STATE.md (partial in effect). UNVERIFIED: that template fencing works against the real template.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-5 Channel for audit escalations (debate QG2)

**Original question:** QG2 Escalation channel and naming rule: OD-5 (channel for audit escalations: entry lines only, or entry lines plus the notice step with the nine-row list and a cap)

**Winner:** OURS (QG2 overall: HYBRID; the notice element is Clay's, reserved).

**Winning recommendation:** Entry lines only in the first build, with a reserved notice. The three post-merge findings (AU4a merged over a change request, AU4c merged with an unresolved review thread, AU5 conflict markers in the merge) are written as lines of the issue's own entry in the living report, marked so the sweep lists them as waiting on a person. Rules of this channel (adopted from Clay): one escalation per pull request, never one per finding; warnings never reach the person; the entry is always written; a cap never drops an entry. The push notice (ClickUp message or Orca unread mark) is reserved for these three findings only and is built only when all three triggers hold: the owner says in chat that a push is wanted and gives the cap number (the design recommends 5); a notice sender is built and tested (none exists in master, pr-a or pr-p); the escalation verb accepts row 8 of the nine-row table without a ruling on the other eight (UNVERIFIED).

**Implications:** The sweep must list entries with a "waiting on a person" status. A conflict marker found by AU5 can sit until the report is read (known limit). The cap key stays at 0 (no cap) until the owner records a number; the design default 5 differs from the parser default 0. This is narrower than D15's OD-5 wording, which waited on the whole nine-row list.

**Caveats:** Confidence 60 percent (the lowest of the three QG2 answers). Convergence 66.7 percent per STATE.md. UNVERIFIED: whether any notice sender exists or works; whether `escalate` accepts row 8 alone; whether Clay's rulings were agreed by the owner outside GitHub.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/VERDICT.md

**Status after PR 700:** UNCHANGED answer, but its carrier (the living report of PR 684) is gone from master; restoring it is an owner decision.

### OD-6 Coordinator never tags or publishes (debate QG3)

**Original question:** QG3 Authority and config: OD-6 (coordinator never tags or publishes)

**Winner:** OURS (QG3 overall: HYBRID; the owner's line wins OD-6, OD-10 and OD-11, and both advocates conceded all three).

**Winning recommendation:** Yes. The coordinator never tags or publishes a release. Clay's rule N6 becomes an unconditional refusal with no `--answer-ref` pass path. It refuses `git tag`, `git push --tags`, `git push origin <tag>`, `gh release create`, `gh release edit`, `gh release delete`, `uv publish`, `twine upload` and `npm publish`, with one denylist test per command and a test that an `--answer-ref` does not change the result. Merging a release pull request stays allowed on the per-PR go. Reason: Clay's own table calls release "something that cannot be undone", and the pass path rests on `answer-check`, which cannot tell a person from a script (open in Clay's register as U57).

**Implications:** The coordinator never runs a tag or publish command; a person or the release flow tags. N6's pass path and the release rows of Clay's test T13 and the argv tests break. `refuse(argv)` sees only commands the verbs run, so a tag typed in the coordinator's own shell stays unseen (UNVERIFIED how to cover it). The claim pipeline is unaffected.

**Caveats:** Confidence 89 percent. Quick depth; no invariant probe. UNVERIFIED: that three entries (`git push --tags`, `gh release edit`, `gh release delete`) match design line 763 exactly; U57.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG3/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-7 Interrupt a running worker (debate QG4)

**Original question:** QG4 Build now or reserve: OD-7 (interrupt a running worker)

**Winner:** OURS (QG4 overall: OURS; all three answers follow the owner's line and the reserve text takes six small improvements from Clay).

**Winning recommendation:** No. `escalate --interrupt` (Clay's rule N7, the one exception that lets the coordinator interrupt a worker) is not built. Reason: no incident is cited; Orca gives no receipt that the interrupt landed (U40); and the contract's next liveness nudge ("If your turn ended before worker_done, continue with your next Command: line now", WC:164) would undo the stop, with no rule in the design that suppresses it. Clay's own paper concedes it is not shown to work. Keep one part: the verb `escalate` writes the escalation first and sends nothing if the escalation is refused. Do not cite WC:137 as a general ban on interrupts: it governs typing the copy of an answer. N7 is "closed unless the owner asks"; a later build needs a contract exception written like the context-exhaustion one, the five coordinator-spec changes C25 to C29, a nudge-suppression rule and a check of whether `--interrupt` has its own receipt.

**Implications:** The verb list loses the interrupt option. A coordinator that sees a worker about to take an irreversible action has the escalation and the person's go only; it never presses interrupt. The brake for an irreversible worker action is the launch guard and the person's go. Design text at lines 749, 764, 925-928 needs edits; nothing is built.

**Caveats:** Confidence 85 percent. UNVERIFIED: whether `--interrupt` has its own receipt (U40 covers text sends only). Cheap check before any later decision: `orca terminal send --help`, then one local send into a busy worker; that send writes into a session, so it needs the owner's go.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-8 Build the lease comment now (debate QG4)

**Original question:** QG4 Build now or reserve: OD-8 (build the lease comment now)

**Winner:** OURS (QG4 overall: OURS).

**Winning recommendation:** No. The lease comment (Clay's fourth layer against a double claim: a comment `<!-- sc:orchestrator:lease ... -->`, lowest comment id wins) is a reserved design with a recorded trigger. Reason: the lease arbitrates only two hosts that each run a poll, two users' orchestrators, a hand-run `--take` or a restored backup; the settled topology is one cron entry and one dispatcher on one host, and no double claim is cited. The lease as designed also wedges an issue when its owner crashes before releasing it, and the design has no stale-lease rule. The risk is real (the design rates it medium/medium as K13, and master's claim allows a re-claim by the same login), so the reserve rests on the absent trigger. Reopen when a second host or a second user runs a poll. Before building: add a stale-lease rule, rename the marker `sc:coordinator:lease`, rewrite test T4, and reserve the state step names `plan_rechecked`, `lease_posted`, `claim_started`, `claim_done`.

**Implications:** No new comment per issue, no new grant-bound write, no change to the claim chain. If a second host or user polls, two coordinators of one login can both start, and no detector notices a second poller (UNVERIFIED that none exists); the trigger is a written rule, not an alarm. The reserve is a bet on the one-host topology holding. A time-based stale-lease rule would give up the "no clock agreement between hosts" property.

**Caveats:** Confidence 75 percent. UNVERIFIED: that no stale-lease rule exists anywhere in the design (some long design lines were cut in earlier searches); that no detector of a second poller exists; the cost of a later lease migration (asserted by Clay's side, not measured).

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-9 List newly assignable issues; keep info streams off (debate QG4)

**Original question:** QG4 Build now or reserve: OD-9 (list newly assignable issues; keep info streams off)

**Winner:** OURS (QG4 overall: OURS).

**Winning recommendation:** Keep the info streams off; the report does not list newly assignable issues now. The "info streams" are three extra GitHub searches (`could_assign`, `mentions`, `affects`). Reason: the replies of the three searches were never captured (U8), and two of the three are subsets of what the report skill already collects with one `involves` search per org (`collect.py:200-210`). Only `could_assign` is new, and it is awareness, never a claim. If the owner ever turns them on, enable `could_assign` alone, after the U8 capture. New finding of this debate: in PR 686 the streams are not behind any switch today and a failed search stops the whole discovery cycle, so "keep off" needs a code change: add an explicit off switch (default off) around the loop at `cycle.py:922-935`, make a failed or rate-limited info search a warning and not a stop of the cycle, and fetch only `could_assign` when enabled.

**Implications:** The report keeps the `involves` list and has no "newly assignable" line. The poll is globally `enabled: false` today, so nothing runs, but "off" is not true in the code until the switch is added (a fifth action on the adapted PR 686). `could_assign` rows are kept only for repos in a list that comes from the registry file D15 removes, so that filter needs a new source. Cost if enabled: about 8 of 35 calls per cycle.

**Caveats:** Confidence 85 percent that the answer is "off", 70 percent that the code change is the smallest fix. UNVERIFIED: the reply shapes of the three searches (PR 686 tests use assumed-shape fixtures); whether a malformed (not failed) reply also stops the cycle.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/VERDICT.md

**Status after PR 700:** UNCHANGED answer. The report skill it mentions is gone from master, so its "report" line is moot until the skill is restored.

### OD-10 Authority for the post-merge issue close (debate QG3)

**Original question:** QG3 Authority and config: OD-10 (authority for the post-merge issue close)

**Winner:** OURS (QG3 overall: HYBRID).

**Winning recommendation:** One per-PR go, bound to the head sha, covers both the merge and the close of that PR's issue; there is no standing `issue.close`. The go is worded "merge PR N at sha X, then close issue M if closeout's verdict is done" and ends when both are done, the head moves, or the owner revokes it in chat. A `Fixes` line in the PR body still closes the issue at merge with no coordinator write. Reason: `E-NO-GRANT` covers only writes made through the orchestrator's own verbs and closeout writes the close through `scripts/settle.sh` (the verbs likely do not see it: the verdict's own inference), so a standing entry would be a permission and not a control; `WORKER-CONTRACT.md:241` allows an outward action only when the user's instruction names that action.

**Implications:** Every merge go must name the close, or the close has no go. A restart between merge and closeout must read the recorded go. Wave 8 changes so closeout runs only under a go that names the close. Whether the dashboard or sweep shows open goes is not decided. This closes D15's condition C-INV-4.

**Caveats:** Confidence 77 percent. UNVERIFIED: that no other check stops closeout's close; whether the verbs see closeout's write.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG3/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-11 Default grants of a fresh install (debate QG3)

**Original question:** QG3 Authority and config: OD-11 (default grants of a fresh install: empty, or the standing entries)

**Winner:** OURS (QG3 overall: HYBRID).

**Winning recommendation:** A fresh install has an empty `grants` list. The owner grants the three standing entries once in chat and the agent records it. The three are `issue.assign`, `issue.comment` and `issue.body.append_plan_sections` (`issue.hold` was removed by Q03). The refusal text names the missing entry and the sentence the owner can say, and the first run lists the three entries once so one chat answer grants them. The record holds the owner's quoted words, the date, the scope and who recorded it. Reason: Clay's own parser reads a missing `grants` key as an empty list; the six-entry list is an example; a fresh install holding `pr.merge` would be a standing merge on an unprotected `master`.

**Implications:** A fresh install refuses the plan call's body write and every assign and comment write until the owner says the one chat answer. The watcher is unaffected. Breaks: Clay's six-entry example and any fixture that lists `pr.merge`, `issue.close` or `issue.hold`. A host where the owner never answers works in a degraded way and the refusal must say why. The verdict flags the risk that the owner counts the one chat answer as manual setup under the zero-setup rule.

**Caveats:** Confidence 71 percent. UNVERIFIED: which planb file holds the per-repo keys; the body of the zero-setup memory was not readable by one advocate.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG3/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-12 Protecting the per-repo config from the coordinator (debate QG3)

**Original question:** QG3 Authority and config: OD-12 (protecting the per-repo config from the coordinator)

**Winner:** HYBRID (the owner's two layers, with Clay's verb refusal as layer 1).

**Winning recommendation:** Both layers, and both only narrow the gap. Layer 1: the `repos` verbs refuse to write `reach_daily_max`, `grants`, `merge_safety_files` and `reviewers` without an accepted answer record (with tests), plus a hook on Write and Edit of the config path. Layer 2: the controls fail closed on values that weaken them (`merge_safety_files: []`, `reviewers: none`, a bad `reach_daily_max`) unless an accepted answer record names the value. Reason: the coordinator runs as the same OS user, so the file cannot be put out of its reach, and the parser accepts every weakening value today. Adding `reviewers` to the guarded keys is this debate's recommendation, not Clay's text (which names three keys).

**Implications:** Neither layer prevents a write by the coordinator's own shell. The merge gate's controls (merge safety files, reviewers, the daily notice cap) are only as strong as the accepted answer record. `merge_safety_files: []` is a valid choice for a repo that wants no hold, so it needs an owner-recorded value to count as deliberate. This closes D15's condition C-INV-3.

**Caveats:** Confidence 69 percent. UNVERIFIED: whether the `repos` verb refusal and its tests are built (D15 records the verbs as design text only); U57 (whether a recorded go can be told from a session's words).

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG3/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OD-13 A hand-back waiting for re-approval versus the in-flight count (debate QG1)

**Original question:** QG1 Planning and hand-back: OD-13 (a hand-back waiting for re-approval versus the in-flight count)

**Winner:** OURS (QG1 overall: HYBRID).

**Winning recommendation:** Do not count it. A waiting step does not count toward `max_in_flight`, shows a visible waiting reason, and gets an expiry only if waiting issues pile up. Recommended carrier (side effects UNVERIFIED): the state file takes status `escalated` with step `handback_awaiting_approval(body_sha)`, which the in-flight counter already skips; on re-approval a wake path repeats the full start check and sets the file back to `in_progress` at wave 4. Reason: a waiting issue has no worker, and counting it means three waiting issues make the repo answer `coordinator_full` to new work while nobody works. Clay's own design already frees the place for an issue that waits on a person. Test: with three issues waiting for re-approval, a new issue of the same repo is not refused with `coordinator_full`; a waiting issue returns to counting only when set back to `in_progress`. If the owner picks option (b) at OD-2, this question does not arise.

**Implications:** `max_in_flight` is untouched. A new visible reason "waiting for approval" must reach the sweep and observer. The wave-0 restart rule resumes `in_progress` files, so an `escalated` waiting file is not resumed by a restart; its entry is `stalled` if its coordinator is down and `--take` refuses it. Using `escalated` is not stated in Clay's design (line 616 says nothing is escalated for a hand-back), so this is a recommendation with checks.

**Caveats:** Confidence about 70 percent on the answer, about 50 percent on the carrier. UNVERIFIED: side effects of status `escalated` (row 9 notices, `stalled`, `--take`); the set-back can overshoot `max_in_flight` if new work took the place; which component runs the wake path.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OA-13a Does a recorded merge go expire by the clock? (debate OAG1)

**Original question:** OA-13a Does a recorded merge go expire by the clock? OURS: no clock expiry; a go ends only when the named action is done, the PR head moves or the owner revokes it in chat (Q01 item 5); merge automation stays off until the owner records a number. CLAY or alternative: a go dies after N hours even if the head did not move (24 hours suggested by the merged design, UNVERIFIED), so a go typed days ago cannot fire.

**Winner:** OURS (OAG1 overall: HYBRID; the owner's line decides all four contested answers, and two Clay elements stay in).

**Winning recommendation:** No, not in the first build. A go ends (a) when the named action is done, (b) when the PR head moves or any new gate reason appears (the go is void), or (c) when the owner revokes it in chat. No age refusal exists today. The build of merge automation (a script or a restarted session acting on a stored go) must include a go age check and must refuse to start until the owner records either a number of hours or the explicit value "none". That is a requirement on a future build, not a setting added now, and no default number is given (24 hours is UNVERIFIED). Reason: the go is bound to a 40-character head sha, the read-only gate runs again just before `gh pr merge --match-head-commit`, and WC:241 requires the instruction to be in the live conversation or confirmed at the moment of action. No source gives a number and no stale-go incident is cited. Test: a merge go for head X recorded days ago, with the head and every gate reason unchanged and the instruction confirmed in the live conversation, is accepted; a go for head X never releases a merge of head Y; with merge automation built and no recorded number or "none", the automation refuses to start.

**Implications:** The merge verb has no age refusal in the first build. A coordinator session open for days can hold a go typed in that same live conversation, which WC:241 does not re-confirm, so the real guards are the head pin, the second gate run and the owner's revoke. Nothing built is affected. Wording rule for the spec: "ends", "void" or "consumed" for an event close of a go; "expires" only for a clock close. The owner must know that D06 item 1 ("expires") and Q01 item 5 (no clock) are worded differently; the spec follows Q01 as the default and keeps D06's number as the owner's open option.

**Caveats:** Confidence about 80 percent. UNVERIFIED: the 24-hour figure and any other number (no source); whether a long-open coordinator session re-confirms a go typed in the same conversation; the go entry and the merge verb are DESIGN ONLY, nothing shown to run. OAG1 is quick depth: one round, no invariant probe; both advocates conceded heavily, so agreement is partly produced by the weighting rule.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OA-13b Merge-time hold for a reviewer that shows no activity (debate OAG1)

**Original question:** OA-13b Is there a merge-time hold for a reviewer that shows no activity, and for how long? OURS: `/sc:pr-submit` keeps its own skip rule for a silent reviewer inside its fix loop; the merge-time hold exists only as D06 item 4 adopts it (owner-set per-repo `reviewers` list, re-request on the final head, wait 60 minutes UNVERIFIED, then escalate to the person). CLAY or alternative: Clay ADD4 holds the PR when a reviewer is silent with no stated wait; or a different number, or none (recorded as an explicit exception).

**Winner:** OURS (OAG1 overall: HYBRID). The hold is the one D06 item 4 already adopted from Clay's ADD4, confirmed here.

**Winning recommendation:** Yes, as D06 item 4 has it, 60 minutes (UNVERIFIED default, owner-settable). The owner sets a per-repo `reviewers` list (`none` is allowed as an explicit, recorded exception); a review of the final head is requested from each listed reviewer; the gate waits up to 60 minutes counted from when the final head's checks finish; then it escalates to the person and the PR stays held. `review_stalled` and `review_none_present` are not overridable by a go. `/sc:pr-submit` keeps its own skip rule inside its fix loop, unchanged. Reason: the loop reads one finished plus one absent reviewer as clean and declares absence on a clock, so the merge decision needs its own stop. The topic's claim that Clay's ADD4 gives "no stated wait" is wrong: ADD4 states 60 minutes after the head's checks finished. Test: a listed reviewer with no activity 59 minutes after the checks finished leaves the PR held; at 60 minutes the escalation is raised; a repo with `reviewers: none` records the exception; no go overrides `review_stalled`.

**Implications:** The merge gate gains the held state and the 60-minute wait. PR 686 already parses a per-repo `reviewers` key; write protection for that key is still needed. `/sc:pr-submit` is untouched. A repo whose listed reviewer never reviews dead-waits 60 minutes at each merge until the owner sets `reviewers` correctly. ADD4's own sentence that a silent reviewer "is no longer skipped" stays overridden. ADD4's "owner ruling 6" is Clay's ruling, not the repository owner's.

**Caveats:** Confidence about 70 percent (the 60 minutes has no source and Codex review timing is unknown). UNVERIFIED: the 60-minute default; whether Codex reviews on every push. A wrong number only delays a merge, it never causes one.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OA-13c `changes_requested` stays a hard refusal (debate OAG1)

**Original question:** OA-13c (settled input, not debated) `changes_requested` stays a hard refusal (D06 item 3). The debate only confirms it is carried unchanged.

**Winner:** OURS (agreed by both sides; no contest).

**Winning recommendation:** No go overrides a PR with an open "changes requested" review. The gate refuses and lists `changes_requested`, with no override key. Reason: both sides agree (D06 item 3, design line 583); Clay's position paper simply never mentioned it.

**Implications:** No change from D06. The gate reason `changes_requested` stays unoverridable. This is still listed as an owner confirmation in the owner-actions section.

**Caveats:** Confidence about 95 percent. Nothing in this item is built.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OA-25a Does a waiting go get a reminder? (debate OAG1)

**Original question:** OA-25a Does a waiting go get a reminder, and at what interval? OURS: no push reminder in the first build (QG2/OD-5 reserves the notice; OA-16 default is no cap); a waiting go keeps its slot and is shown as "waiting on a person" in the report. CLAY or alternative: a reminder every N hours through the notice step (nine-row table, `reach_daily_max`) so a stalled cap-1 repo is not quiet.

**Winner:** OURS (OAG1 overall: HYBRID).

**Winning recommendation:** No push notice in the first build; the wait is shown with its age. A PR waiting for a go is shown as "waiting on a person" with the age of the wait (since when it has waited), in the report entry lines that QG2/OD-5 sets as the first-build channel, and listed by the sweep and the observer. The push notice (a ClickUp message or an Orca unread mark) stays reserved behind the three triggers of QG2/OD-5 (the owner says in chat that a push is wanted and gives a cap number; a notice sender is built and tested; the escalation verb accepts the needed row). When the owner records an interval it is the owner's number; the only cadence with a source in the repository is daily (the 07:00 report wake), which is UNVERIFIED as a reminder interval. Reason: no escalation notice sender exists in master, PR 686's head or branch `issue-655-pr-p`; the cap of 5 notices a day is Clay's ruling 39 and the owner has no record of ruling on it. Test: with a go waiting 3 days, the report entry and the sweep show it as waiting on a person with its age and no message is sent.

**Implications:** Today the sweep lists Orca session row ids only, with no age and no go entries, so "shown with its age" is a requirement on the entry-line writer and the display, not an existing feature. Merged-requirements wording "with a reminder" (K9, S15b, INV-023, OA-25) is to be rewritten as "shown with the age of the wait; push notice reserved". The work report is configured for one named person (`"person": "clayphi"`), so for the owner the sweep and observer are the surfaces. INV-023 (cap 1 plus owner silence) stays a MEDIUM risk, narrowed by display, not closed.

**Caveats:** Confidence about 75 percent. UNVERIFIED: whether the sweep or observer will show a waiting go with its age; whether an idle coordinator session waiting for a go is classified as waiting by the sweep; whether `clickup.py dm` could reach the repository owner.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/VERDICT.md

**Status after PR 700:** UNCHANGED answer, but "shown in the report entry lines" depends on PR 684's report, which is gone from master; restoring it is an owner decision.

### OA-25b What owner silence means on a waiting go (debate OAG1)

**Original question:** OA-25b What does owner silence mean on a waiting go? OURS: silence is never a yes and no expiry drops committed work (INV-023, K9); a waiting go counts toward `max_in_flight`. CLAY or alternative: an expiry moves a long-waiting go or `waiting_reapproval` to `stopped` (K15), freeing the slot.

**Winner:** OURS (OAG1 overall: HYBRID; Clay's K15 expiry is kept for one state only).

**Winning recommendation:** Silence is never a yes. There are two waiting states and the spec names both. (i) A waiting merge go: the worker has finished and the PR is open; it keeps its slot, counts toward `max_in_flight`, never expires, and nothing moves it to `stopped`, because that would abandon committed work. (ii) Waiting re-approval (`waiting_reapproval`): no worker, no PR; per QG1/OD-13 it does not count toward the cap, and K15 lets it expire to `stopped` after an owner-set limit; with no limit recorded it never expires. Because state (ii) is outside the cap, its expiry frees nothing; it only cleans up a stale waiting entry (this corrects Clay's wording "freeing the slot"). Reason: Clay's own design says an unanswered question waits and no default is taken (section 5.6, ruling 24), and Clay's report skill keeps an unanswered "Needs you" entry until answered. Test: three issues in `waiting_reapproval` do not make a new issue answer `coordinator_full`; one issue with an unanswered merge go at cap 1 stays counted and is shown waiting with its age.

**Implications:** At cap 1 one unanswered merge go holds the only slot and the repo stalls visibly but quietly. Raising the cap is OA-14 and needs the isolation, closing-writer and concurrency tests. A hand-back waiting for re-approval is carried by status `escalated` with step `handback_awaiting_approval` (QG1, side effects UNVERIFIED); its expiry has no default number. This resolves the apparent clash between K9 and QG1's OD-13 (see "Where verdicts disagree").

**Caveats:** Confidence about 85 percent. The owner's only inputs for all of OAG1 are three numbers or choices (go age, hold minutes, push notice), and none blocks the spec.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/VERDICT.md

**Status after PR 700:** UNCHANGED. The recommendation stands; any action in it that edits `docs/designs/orchestrator.md` or the report skill is moot until the owner restores them (see the update section at the top).

### OA-9 Where the sweep JSON is saved (debate OAG2)

**Original question:** OA-9 Where does the sweep JSON live? OURS: saved beside the Markdown report as `<UTC>-sweep.json`; one file all readers share; S5 adds the write; WC-16 stands (K19). CLAY or alternative: each reader (report, observer) runs its own sweep and no file is kept; readers may disagree within a minute and WC-16 must change.

**Winner:** OURS (OAG2 overall: HYBRID; five separable Clay conditions are added). The file is kept; "each reader sweeps" is not adopted.

**Winning recommendation:**
1. The sweep saves `<UTC>-sweep.json` beside its Markdown report in `.dev/sweeps/`, from the same `to_json` call, with the same temp-file-then-link, never-overwrite pattern (today the JSON goes to standard output only). Test: after one run both files exist; a second run in the same second overwrites neither.
2. The JSON pairs with its Markdown by the same stem and suffix (`<UTC>-sweep-2.json` with `<UTC>-sweep-2.md`). The `.md` link stays the commit point.
3. No new field is needed to record the window and root: JSON v1 already holds `observed_at`, `scope.root` and `window`. D11's `session_id` and `worktree_path` stay a separate item.
4. The observer reads the newest `*-sweep.json` whose `scope.root` equals its own root and shows `window`, `observed_at` and the age. A missing or old file is its own screen state, never "no sessions". The spec sets what "old" means.
5. The work report does not read a file whose `window` is shorter than the time since its previous report; it runs `superclaude sweep run --window <that time>` itself, which also saves a file.
6. The coordinator keeps WC-16 unchanged: at most one sweep per 5 minutes.
7. The contract note `docs/designs/observe-sweep-contract.md` (unwritten since 2026-11-13) names the file, its name pattern, the selection rules and one owner.
8. The spec says the 90-second sweep budget "is not guaranteed to fit" the observer's 15-second cycle, not that it "cannot fit": 90 seconds is a cap, not a measured time.

**Implications:** The poll is unaffected. The work report now makes its own sweep run with its own window, outside the coordinator's five-minute cap (WC-16 binds the coordinator's loop, not the report). The observer needs a new reader (it has none today). Risk: a JSON and Markdown pair with different suffixes would give a reader the wrong pair; the pairing test guards it. The file sits under one checkout root while the watcher serves many repos: recorded as an open item.

**Caveats:** Confidence about 85 percent. Quick depth: one round, no invariant probe. UNVERIFIED: how long a sweep really takes; whether a retention rule for `.dev/sweeps/` exists; whether a watcher serving many repos can read each repo's `.dev/sweeps/`; Clay's own views on OA-9 (no text by Clay found; the Clay side was argued from TOPICS.md and Clay's merged work).

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/VERDICT.md

**Status after PR 700:** UNCHANGED answer for the sweep file and the observer. The part where the work report runs its own sweep is moot while PR 684's skill is gone.

### OA-17a May the observer show entry text? (debate OAG2)

**Original question:** OA-17a May the observer show entry text? OURS (merged design default): show entry text from the living report, always passed through `observe/sanitize.py`; the three states (empty folder, zero rows, could not read) stay distinct. CLAY or alternative: titles and links only, no entry text on the screen (the work report keeps the text).

**Winner:** HYBRID (OURS on showing text; Clay's field allowlist, length cap and titles-and-links fallback are added).

**Winning recommendation:**
1. The observer shows entry fields only from a named allowlist (the owner or the spec fills it). `recommend` and `suggested` are never shown, because entry files hold those model-written slots and the observer is navigation only. `how` stays hidden until the owner has reviewed what it holds.
2. Every shown field goes through `sanitize()` and is built as `rich.Text` from data, never parsed as markup. Block fields have a length cap the spec sets (the sanitizer removes terminal controls only and has no cap).
3. While the entry writer `superclaude orchestrator report-entry` is absent (it is: it appears only in the report skill and the closeout scripts, and `cli/main.py` has no orchestrator group), the observer shows titles and links only. The three states stay distinct.
4. Tests: a fixture with `recommend` and `suggested` filled shows neither; a 5,000-character field shows at most the cap; `[bold red]x[/]` shows literally.

**Implications:** The first observer release shows titles and links and the empty-folder state, because the entry writer (Clay's unbuilt PR B) is absent. The owner names the allowlist contents, the cap value, whether `how` may show, and what "old" means before the matching code. Clay's permanent titles-only position is not adopted.

**Caveats:** Confidence about 72 percent. UNVERIFIED: what the entry field `how` holds and whether it is safe to show; that `sanitize.py` is enough for every kind of text (tested only on terminal-control, bidi, zero-width and CR samples). It would drop if the owner wants titles and links only.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/VERDICT.md

**Status after PR 700:** UNCHANGED answer, but the entry text it shows comes from the living report of PR 684, which is gone from master; restoring it is an owner decision.

### OA-17b Is the observer questions panel an exception to "one data source"? (debate OAG2)

**Original question:** OA-17b Is the observer questions panel an exception to "one data source"? OURS: keep the panel's own Orca call, labelled as an exception, until a shared questions block exists. CLAY or alternative: end the exception now; design a shared questions block (one shared question id, also ending the two question channels of D11) before the observer ships.

**Winner:** OURS on timing (keep the labelled exception); Clay's label wording and a follow-up for one shared question id are added, and the follow-up does not block the observer release.

**Winning recommendation:**
1. The panel keeps its fixed read (`orchestration check --all --types question --run <id> --json`) with its shape check and forbidden-verb list.
2. The screen label reads "questions read from Orca directly; a question already handled can appear as open", because the ledger cannot tell handled from open.
3. The spec and the screen say "one source for session facts (the sweep); the questions panel is the one exception", never the unqualified "one data source".
4. A tracked follow-up exists for one shared question id (which would also end the two question channels of D11). The owner names who owns it. It is not a precondition of the observer release; the sweep JSON has no questions block today.

**Implications:** D11's sentence "one data source" is replaced by the qualified one. Two question channels (observer questions and report "Needs you") remain until the follow-up is done. A handled question can show as open on the observer.

**Caveats:** Confidence about 75 percent. UNVERIFIED: that the observer's questions read is non-consuming (from the technical reference, not tested live). OAG2's overall confidence is 78 percent; its agreement is weaker evidence than it looks because the Clay advocate was told a separable Clay benefit counts.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/VERDICT.md

**Status after PR 700:** UNCHANGED. The questions-panel exception does not depend on the removed skill; the follow-up for a shared question id still stands.

### OA-28a Should a repo that passes `first_run` switch itself on? (debate OAG3)

**Original question:** OA-28a Should a new repo that passes `first_run`'s checks switch itself on? OURS (the owner's recorded line, planb R18): default-on after the throwaway run, so zero setup stays true for every later repo. CLAY or alternative (the merged design's default, K24): `auto_enable` false; a new repo gets a config and its checks but stays off until the owner names it in chat (one recorded go per repo).

**Winner:** HYBRID (the owner's end state, reached through Clay's key that ships false until the throwaway run passes).

**Winning recommendation:**
1. Staged default-on. The defaults key `auto_enable` ships false (in code and in the shipped defaults file). No config is switched on before S17 (the stage "live tests, then enable one throwaway repo"). After S17 passes, the owner turns the key on once in `~/.config/superclaude/issue-watch-defaults.json` (one recorded chat go). From then on a repo that passes the six `first_run` checks switches itself on with no per-repo go. Reason: the owner's recorded rule is "nothing in the setup is manual" (R17, R18), and the merged design says no config is switched on before S17; planb today has no key and enables unconditionally on a pass. Tests: `test_first_run_keeps_config_off_while_auto_enable_false`; `test_dry_run_generates_nothing`.
2. The S17 pass list is a proposal, not an owner rule (UNVERIFIED): the six `first_run` checks green on the throwaway repo, a 24-hour `run-all --dry-run` shadow run that generated and wrote nothing, the X-001 live check (do claim agents share one `Coordinator` worktree?) run, and the owner's go in chat.

**Implications:** `run-all` is still not scheduled before S17 and nothing switches on before the owner's flip. After the flip every in-scope repo (allowed owner, one Project, readable approvers, a `Coordinator` worktree) that passes the checks self-enables; a repo that fails stays off with a report. Enabling launches nothing by itself; each issue still needs a person's approval. Planb's `first_run` today creates the label at step 2 before the dry-run, lock and restart checks, so a repo that later fails already has its label. An owner-visible report of self-enabled repos is a proposal with no mechanism. Cite symbols, not line numbers, after the planb rebase.

**Caveats:** Partial (convergence 68.4 percent, 13 of 19 points, not converged; six points unresolved). Confidence about 70 percent. It would go to Clay's side if the owner says each repo must be named in chat even after S17. UNVERIFIED: the S17 pass list; that every later repo has the same shape as the throwaway repo; whether the owner accepts the S17 flip as a class-level go.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/VERDICT.md

**Status after PR 700:** UNCHANGED. Planb's `complete.py` and `repo_init.py` build on the restored `issue_pipeline`, which is back on master.

### OA-28b Does NG-2 cover only the poll cycle, so init may create labels? (debate OAG3)

**Original question:** OA-28b Does NG-2 ("the poll never writes to GitHub") cover only the poll cycle, so init may create the trigger and `hold:backlog` labels once per repo? OURS: yes, NG-2 covers the poll cycle only; init creates the two labels once (D09 rule 2, as planb already does), still behind the owner's chat OK before the first real run. CLAY or alternative: NG-2 means no GitHub write anywhere in setup; labels are created by hand and init only checks that they exist (Clay's design D:410, D:436-495 allows a poll label write, so the strict reading is the narrower end).

**Winner:** OURS (NG-2 covers the poll cycle only); Clay's advocate conceded the point (about 82 percent).

**Winning recommendation:**
1. Yes. NG-2 means the poll cycle (`issue-watch once`) makes no GitHub write. `repo_init.py` is the one setup module allowed to write, and only a `gh label create`. Reason: the design says the NG-2 test "covers the poller only"; planb's code already splits the cycle's read (`trigger_label_state`) from the init write (`ensure_trigger_label`); and the owner's own planb test allows exactly `complete.py` and `repo_init.py` as the only writers.
2. The label write needs the owner's chat OK, and that OK is the same recorded go that turns `auto_enable` on (a class-level go for the trigger label of later repos). Before that go, with the key false, the label step only reads and reports `would_create` without failing the check; with the key true it calls `ensure_trigger_label`. The `would_create` result is a design proposal, not existing code (UNVERIFIED). This fixes a self-contradiction in the OURS paper, which said both "behind the owner's chat OK" and "without a fresh chat go".
3. `hold:backlog` creation is not part of this decision. Planb creates only the trigger label. `hold:backlog` stays by hand until the owner asks for init to create it; nothing shows a reader of that label yet (see also Q03).

**Implications:** NG-2's scope sentence is written into the spec with no new write allowed. A read-only label step means a new repo's label check does not fail setup but also does not create the label until the key is on; a label made by hand stays valid at any time. No change to what the coordinator or the observer reads. Clay's own design is not a strict reading either (the poll writes `hold:plan` in lines 436-445), so the strict reading would have been narrower than Clay's own rule.

**Caveats:** Partial (OAG3 convergence 68.4 percent). Confidence about 88 percent. UNVERIFIED: whether the owner accepts the S17 flip as a class-level go for later repos' label creation (the merged design says each label creation needs the owner's chat OK and does not say it can be class-level); the `would_create` result; planb line numbers will move after the rebase.

**Evidence:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/VERDICT.md

**Status after PR 700:** UNCHANGED. Planb's `complete.py` and `repo_init.py` build on the restored `issue_pipeline`, which is back on master.

## Coordinator decisions made without a debate

These were made by the coordinating session while running the exercise. Each has a reason and an implication. Items (e) to (h) come from the coordinator's own brief and progress log, not from a verdict.

**(a) The tech-reference was run for two built subsystems only (the issue-to-work pipeline; the observer, sweep and dashboard), not for the coordinator.**
- Reason: no coordinator code exists on master, so there is nothing built to document.
- Implication: every verdict about the coordinator (D04 to D10, D15 and the OD answers) rests on Clay's design text and the PR 686 code, not on a reference of built behavior. Their UNVERIFIED lists reflect that. The two references that were made carry their own limits (progress log): the pipeline reference is 2,436 lines and did not verify runtime behavior; the observer reference is 1,399 lines, has 40 UNVERIFIED rows, and flags one defect candidate (the `prefs.py` answer rejects an `orca://` session url) for which no fix task was made. D11 ran before the observer reference existed and read code directly.

**(b) Debate depth was standard for the conflicts D01 to D12, D14 to D16, and quick for D13, Q01 to Q03 and the four open-question debates QG1 to QG4.**
- Reason: quick was judged enough for narrow follow-up questions.
- Implication: a quick debate has one round, no third round and (in QG1 to QG4) no invariant probe. Standard depth also has no third round, so HIGH findings that appear at the end are carried as conditions, not argued out (this is why many verdicts are "partial"). QG2 ended at 66.7 percent convergence (progress log), below the 80 percent bar.

**(c) The 13 open questions OD-1 to OD-13 were grouped into four debates: QG1 (OD-1, OD-2, OD-13), QG2 (OD-3, OD-4, OD-5), QG3 (OD-6, OD-10, OD-11, OD-12), QG4 (OD-7, OD-8, OD-9).**
- Reason: questions on the same subject were settled by one pair of advocates.
- Implication: the answers are recommendations; D15 said some of its own first answers were tie-breaks (OD-1, OD-4, OD-5, OD-13) and the QG debates tested them. Each is listed as its own entry above. The owner still gives each answer in chat.

**(d) Server-side protection of `master` was not debated; it is an owner action.**
- Reason: only the repository admin can set a branch ruleset, so no agent or debate can decide it.
- Implication: until it is set, `master` and `integration` are unprotected (verified read-only on 2026-11-20 by D01 and D16: not protected, no rulesets), Clay's risk K12 stays open, D14's plan can be broken by one merge click, and D16's gate does not exist. See "Actions only the owner can take".

**(e) The owner replied "No" to two questions (pause the claim-handoff-planb session; publish the report), and the coordinator read that as covering both, so neither was done.**
- Reason: the reply was a single "No" to a two-part question.
- Implication: the planb session was not paused and the report was not published. If the "No" was meant for only one of them, the owner should say which. The progress log records planb as uncommitted and unpushed at 04:11Z, and D14 wants it committed and pushed as a draft after the revert.

**(f) Some debate agents ran read-only `gh` calls against the owner's own repository `IronbellyOrg/Coder` (issues 477, 515, 516) instead of `IronbellyOrg/IronClaude`.**
- Reason: the topics name those Coder issues. D10 says so openly; D02 read Coder issue 515 the same way. D07 also made two read-only calls naming `IronbellyOrg/IronOrchestrator` (one returned `private: true`).
- Implication: the brief said every `gh` call names IronClaude, so this broke the letter of that rule. Nothing was written to GitHub or Orca and nothing touched `SuperClaude-Org`. The facts about Coder issues in D02, D07 and D10 come from those reads and from requirement quotes; D07 says it did not open 515 or 516.

**(g) A debate agent printed this host's Orca runtime auth token into its own transcript.**
- Reason: reported by the D02 verdict (the token is in the local Orca runtime file, field `authToken`).
- Implication: the progress log checked that the token value is in no file under `.dev/brainstorms`, `.dev/tasks` or `.dev/analyze`. It may still sit in that agent's transcript. The owner may want to rotate it; the coordinator did not.

**(h) D15 ran `uv` inside a read-only snapshot and deleted the files it made.**
- Reason: it counted audit reasons by running `uv run python -I` inside the export of PR 686 (`/home/coder/.cache/ic-snap-20261120/pr-a`).
- Implication: `uv` created `.venv` and `uv.lock` there; D15 deleted both and a later `find` showed no other new file, but the directory timestamps of that snapshot changed. The progress log records a similar timestamp touch on a snapshot root from a tech-reference QA probe file (created and deleted; file hash identical). File contents are unaffected; the snapshots are no longer byte-for-byte untouched in timestamps.


**(i) The 34 owner actions from the brainstorm were sorted into SETTLED, OWNER-ONLY and DEBATE, and only the 5 DEBATE ones were debated (in three quick debates OAG1 to OAG3).**
- Reason: 20 were already decided by a verdict, a built-in default or an owner standing rule, and 9 can only be answered by the owner (consent, admin setting, credential or a fact only the owner knows). Debating them would have invented answers.
- Implication: the spec is written to the SETTLED answers and to a named safe default for each OWNER-ONLY item. The triage is the coordinator's own classification: its OA-2 fallback (an owner session adapts a new draft if Clay does not act) comes from the triage, not from a verdict, and it treats OA-1 as settled although D14 asks for the owner's chat answer (X-19). Like (b), the OA debates ran at quick depth.


**(j) After the owner said "yes" to a third spec pass, the spec author fixed panel findings F6, F10 and F14 directly, and F4 through debate Q04.**
- Reason: these four findings touched the owner's rules (typed go, approvals in chat, poll writes nothing, no standing merge grant) and were only Medium, so the review loop would not have fixed them; the owner asked for the fix.
- Implication: for F10 the spec author required a per-repo chat OK for label creation instead of OAG3's class-level cover (the spec records this as its own X-18; in this record it is X-20 to avoid a clash with the earlier X-18). The owner can still choose the class-level cover at the S17 flip (OA-28b). The spec panel's process note says the third pass edited text that no blocking finding named, and added FR-84 and SEC-22, at the owner's request.

**(k) The spec panel ran three reviews.**
- Result: review 1 FAIL (1 blocking finding, F1, fixed); review 2 PASS (scoped); review 3 PASS (scoped), 0 blocking, 8 Medium findings. The review rule allows no fourth review, so any further fix is a spec edit by the owner's choice and carries no new PASS.
- Implication: the remaining Medium findings are listed in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/FOLLOW-UPS.md`. Four of them (H1 to H4) touch the typed-go rule and the file says they should be fixed before any build: the run line is not tied to FR-32's duty to show worker commits first; the SEC-22 push bound misses CI, sync and merge-commit pushes (a run can make 4 pushes against a stated bound of 3); the five new SEC-22 checks have no stage or component that could refuse a push made by `/sc:pr-submit`; the Full Submit field is stated as an unconditional go in three places and only SEC-15 says it waits on the owner. No issue was filed (the reviews ran unattended). The spec is not a plan of record until the owner confirms the owner actions in its section 10.

**(l) On the owner's chat go, the coordinator saved PR 682 and started a revert PR for it.**
- What was done (from the coordinator's report): the pre-revert state is saved as the tag `archive/pr-682-issue-pipeline-removal`, pushed to origin, plus patch files in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/archive/pr-682/`. A revert PR for PR 682 was started in the Orca worktree `revert-pr-682`. PRs 686 and 690 were checked and were already drafts.
- State on disk when this record was written: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/archive/pr-682/REVERT-RESULT.md` records base sha `7f0919345479007ad72724dd16b4e4cf08136e65`, branch `ironbelly/revert-pr-682`, worktree `/home/coder/workspaces/worktrees/IronClaude/revert-pr-682`, and, in its first version, "PR: not opened yet". The file has since been updated: the PR is #697 (see item (m)). The revert is still subject to D14's conditions (no merge of PR 686 ahead of it; the "no `--to`" bullet re-applied by hand; the same-PR design correction) and to `/sc:pr-submit --monitor 3` for opening the PR.
- Implication (superseded by item (n) and the update at the top: PR 697 was closed and PR 700 did the revert): the first step of D14's lane 2 had begun, which makes the owner's earlier chat answer "both gates stay" (D14's Q1) a live dependency; if that answer was only "start gate stays", PR 682 would stand and this revert should be dropped.


**(m) PR 697 (https://github.com/IronbellyOrg/IronClaude/pull/697, the revert of PR 682) got three review findings on restored owner text, and the coordinator decided how to treat each.**
- Facts (from the revert result file, `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/archive/pr-682/REVERT-RESULT.md`): PR 697 has two commits: `a6d0889c2`, a pure revert of commit `01e7a9e23` (36 files, +4612/-24, only `CHANGELOG.md` conflicted, with the "no `--to`" bullet and its tests re-applied by hand), and `fd23c01a9`, a separate fix commit. CI passed on both heads (6 of 6 checks on the second). The full local suite had 2 failures (`tests/cli/eval/test_claude_process_adapter.py`, "No module named ruff"), which also fail on a clean export of `origin/master`. Codex and Augment each reviewed both heads; after the fix commit neither raised anything new. The PR was open and was not to be merged until the owner said so (superseded: PR 697 was later closed, see item (n)).
- Decision: on the owner's chat order "monitor that new PR, fix any CI issues or reviewer comments", the coordinator ordered a separate commit fixing `WORKER-CONTRACT.md:59` (WC-17 step 4: `check-approval` now passes `--issue <N>`, which the code already accepts and which refuses a record whose id does not match the issue) and `WORKER-CONTRACT.md:298` (the "Worktree, then worker" duty). The agent first stopped after round 0 because the findings touched restored owner text, then continued on the coordinator's go. The Augment thread on line 59 was replied to and resolved.
- Left for a separate reviewed change: the finding on `launch-level-guard.sh:444` (a bound worker can reach the release command through Python, `issue_pipeline_group.main([...])`, past the guard's literal matchers). The reason is that the G2 design note requires an independent review of any guard change; the guard version stamp stays 1. The thread was replied to ("real, out of scope for a revert, recorded as follow-up") and left open.
- DEVIATION by the agent from the coordinator's order: the order said the contract must say the worktree is created WITH an agent. `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (docstring lines 30 to 38) deliberately runs `orca worktree create` without `--agent` so the claim can copy the issue folder into the worktree before any agent starts, then closes Orca's plain first tab. Saying "created with an agent" would be false. The contract now states the true thing: the worktree is created without an agent of its own for the copy, and the worker started straight after by `worker-start` is that worktree's agent. The code is unchanged.
- Implication: the two threads on line 298 (Codex and Augment, about the "every worktree gets an agent" rule) stay open; three threads in total remain open. The standing rule that every Orca worktree gets an agent and the claim script's behavior still differ in letter until the owner decides.


**(n) On the owner's chat "yes", the coordinator commented on and closed PR 697 and had the replacement PR opened.**
- Reason: PR 700 made the revert of PR 682 unnecessary (see the update section at the top).
- Implication: PR 697 was closed at 16:14 UTC as superseded, and its branch `ironbelly/revert-pr-682` is kept. The replacement is a small PR on branch `ironbelly/restore-gaps-after-pr-700` that adds only what master lacks (the "Messages carry no `--to`" bullet and tests, and the `--issue <N>` fix on WC-17 `check-approval`). The replacement is PR 701 (https://github.com/IronbellyOrg/IronClaude/pull/701, open). Item (m) above describes PR 697 as open; that is superseded.

**(o) The owner's earlier "Yes" to drafting issues led to issues 698 and 699 being filed, with no labels or assignees.**
- Reason: the owner agreed to file the findings of the PR 697 review that were left for a separate change.
- Implication: issue 698 is titled "Release-worker and plan-approval checks rest on text matching and an assignee shortcut" and issue 699 "The claim script creates the issue worktree without an agent, against the every-worktree-gets-an-agent rule". Issue 699 matches the claim-worktree finding in item (m). Which review threads issue 698 covers is UNVERIFIED (its title names the text-matching and assignee-shortcut checks). Both are open and unassigned, so nobody owns them yet.

**(p) The banner task on the PR 681 design document was started on the owner's order and dropped, because PR 700 deleted the file.**
- Reason: `docs/designs/orchestrator.md` does not exist on master after PR 700, so there is nothing to put the banner on.
- Implication: D14's banner row and its same-PR design correction are moot. The task's result file (`archive/pr-682/BANNER-681-RESULT.md`) records branch `ironbelly/banner-681-design`, no commit and no PR. If the owner restores the design from the archive branch, the banner question comes back.

**(q) Two verification reports were written about the revert.**
- `archive/pr-682/INDEPENDENT-REVIEW.md`: an independent review of PR 697 with verdict PASS (reported by the coordinator): 33 of the 36 files identical to the pre-682 tree, the other three differing only by declared lines, the saved patch complete, and the PR mergeable with CI green at the time.
- `archive/pr-682/INSTALL-TEST.md`: plain `superclaude install` skips files that already exist and never reads the guard's version stamp, so a host that installed between 00:02 and 15:07 UTC on 2026-11-20 (after PR 682 and before PR 700) keeps the stale guard and contract (the contract gets a "differs, NOT updated" warning; the guard is skipped silently). Only `superclaude install --force` or `superclaude update` replaces them. Not run through the real CLI (it runs network and Orca steps); the test called the same two install functions against a fake home. Which command the owner's hosts run was not checked.
- Implication: hosts in that window need `superclaude update`. Bumping the guard's version stamp would not make the installer overwrite anything.

## How the brainstorm's 34 owner questions were handled

The brainstorm run produced a merged requirements file whose section 7 holds 34 owner actions (OA-1 to OA-34). Each was sorted into one of three classes (source: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OA-TRIAGE.md`): 20 SETTLED (an earlier verdict, a built-in default or an owner standing rule already decides it), 9 OWNER-ONLY (only the owner can act, so the spec records a safe default and never asks again) and 5 DEBATE (settled by a quick debate, entries above). Where a SETTLED item still needs an owner go for an outward action (a post, a PR, a push), that go is listed under "Actions only the owner can take" and does not block the spec.

### SETTLED (20)

| OA | Question in short | Settled by (the spec follows this) |
|---|---|---|
| OA-1 | Do both gates stay (start approval, and plan approval after the claim)? | D01 and D03: both stay and PR 682 is reverted, per the triage. D14 still wants the owner's own chat answer first (see the disagreement list, X-19); the go to open the revert PR is a separate owner go |
| OA-2 | Who adapts PR 686 and PR 690? | D14: adapt in place as drafts, Clay edits each PR and the owner reviews each push. Fallback written by the triage, not by a verdict: if Clay does not act, an owner session adapts a new draft |
| OA-3 | Which poll command does cron run? | D07 and D02 item 2: `issue-watch run-all`, one dispatcher over `orca repo list`, per-repo JSON config |
| OA-4 | Order of planb and the revert | D14 and D15 order O2: revert first, then contract and guard amendment, then planb landed, then design amendment, then adapted PR 686 |
| OA-8 | Keep the trigger label? | D01 item 7: keep `issue-watch:trigger` for now; dropping it is a later owner decision |
| OA-10 | Branch names `Coordinator` and `coordinators` | D08 item 7: two things, stated in one sentence; the owner may overrule |
| OA-12 | Close authority after merge | OD-10 (QG3): one per-PR go bound to the head sha covers merge and close; no standing `issue.close` |
| OA-14 | Hand-back and capacity | OD-2 and OD-13 (QG1); cap 1 first (design row K9 and D07 item 8) until claim agents get their own worktree |
| OA-15 | Local `git branch -d` in cleanup | Q02: yes, with the added refusals and a report-only first week. Approval of the issue 687 cleanup design is a consent and stays an owner action; each `--apply` still needs its own go |
| OA-16 | Notice cap | D11 item 4 and OD-5: the cap of 5 is a proposal; absent or 0 means no cap; the owner may record a number any time |
| OA-22 | Answer Clay on issue 450; rescope issue 655; split issue 689 | D14 and D12 rule 6; the posts are owner or assignee actions and block no stage |
| OA-24 | Where the interim ledger lives and who commits it | Owner standing rules: `.dev/tasks/` is always staged, commit only when asked, approvals are recorded by the agent |
| OA-26 | Does each push of the `coordinators` records branch need a go? | Yes, a go per push (design row K5, risk INV-024 and `WORKER-CONTRACT.md:241`) |
| OA-27 | Which `plan_depth` the planner uses | OD-1 (QG1): `quick` by default |
| OA-29 | Scope of the naming rule | OD-3 (QG2): scope B |
| OA-30 | A refused mandatory escalation | OD-4 (QG2): fail open on delivery |
| OA-31 | Channel for audit escalations | OD-5 (QG2): entry lines only in the first build |
| OA-32 | Tags, publication and interrupts | OD-6 (QG3): never tag or publish; OD-7 (QG4): no interrupt |
| OA-33 | Build the lease comment now | OD-8 (QG4): no; reserved design |
| OA-34 | List newly assignable issues | OD-9 (QG4): no; info streams off, plus an off switch in the adapted PR 686 |

### OWNER-ONLY (9), each with the safe default the spec uses

| OA | Question in short | Safe default until the owner acts |
|---|---|---|
| OA-5 | Server-side ruleset on `master` and `integration` | Assume NO ruleset: every control is written as "narrows" and a person's go is a procedure. D16 supplies the recommended settings as ready-to-say text |
| OA-6 | Who counts as "the owner" for typed answers on the shared login `ironbelly` | Leave it unnamed, so `answer-check` cannot pass and every merge is typed by hand |
| OA-7 | Wording of WORKER-CONTRACT lines 57, 70 and 245 | The line 57 fix is prepared as its own commit and shipped only after the owner's one chat confirmation; lines 70 and 245 are drafted but not in force; `coordinator_autostart` can never be true |
| OA-11 | Which of the three standing grants | `grants` empty and fail closed; the refusal names the missing entry and the sentence the owner can say; the agent records the owner's words |
| OA-18 | Per repo: `coordinator_autostart`, and whether a typed wake line is acceptable | `coordinator_autostart` false (`coordinator_absent` is reported); typed wake line refused, file pull and mailbox only; both paths built behind the flag |
| OA-19 | Per repo: switch on | Every repo off (`enabled: false`, `auto_enable` false); at most one throwaway repo after the `--dry-run` shadow run, cap 1, `claim_by: poll` |
| OA-20 | Flip `WORKER_BINDING_PROVEN` after the probe; later open level FS for workers | Not flipped; no worker starts on a real issue; probe issues only |
| OA-21 | Confirm the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656) | Not confirmed; per-host diff of installed guard, contract and skills before every `superclaude install`, never a blanket `--force` |
| OA-23 | The claim route after the X-001 live check | Poll-launched claims only on a throwaway issue, cap 1, real rollout off; both `claim_by` values specified (`poll` default, `coordinator` reserved) |

### DEBATE (5), settled by the three new debates

| OA | Debate | Entries above |
|---|---|---|
| OA-9 | OAG2 | OA-9 |
| OA-13 | OAG1 | OA-13a, OA-13b, OA-13c |
| OA-17 | OAG2 | OA-17a, OA-17b |
| OA-25 | OAG1 | OA-25a, OA-25b |
| OA-28 | OAG3 | OA-28a, OA-28b |

## Actions only the owner can take

Collected from every verdict, de-duplicated. "Chat" means the owner says it in chat and an agent records it; the owner never writes a file (owner rule of 2026-11-17, confirmed for grants by Q01 once the owner agrees). Every verdict is a recommendation until the owner says so.

### A. Admin settings (only `ironbelly` is a repository admin)

| Action | Needed by |
|---|---|
| Set a ruleset on `master` and `integration`: PR required, 0 required approvals, require code-owner review, dismiss stale approvals, no force push, no deletion, bypass for the admin role for PRs only; add `integration` as a target | D05, D14, D15, D16 |
| Make any CI check required (for example `.github/workflows/boundary-guard.yml`) | D16 |
| Decide whether branch protection or required review on `master` is wanted at all, and check whether organization-level rulesets exist (the token cannot read them) | D06, D16 |

### B. Security and host housekeeping

| Action | Needed by |
|---|---|
| Rotate the local Orca runtime auth token that a debate agent printed | D02 and item (g) above |
| Before any `superclaude install`, diff the installed guard and contract against both versions on each host; no blanket install until the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656) are confirmed; run `superclaude install` after the revert lands | D03, D14 |
| Land Coder issue 515 (cron at boot) and Coder issue 516 (Coordinator branch, worktree and session) before the dispatcher serves any repo; correct the "not a fit for a plain command" wording in 515; post the drafted narrowing of Coder issue 477 | D02, D07, D10 |
| Optionally run the decisive automation test (create `orchestrator-poll --disabled`, enable, watch 1 to 24 hours) and create any fallback automation | D02 |

### C. Rulings in chat (the agent records each)

| Action | Needed by |
|---|---|
| Say that approval (not assignment) stays the start gate, and whether the `issue-watch:trigger` label stays; answer Clay's 2026-11-18 comment on issue 450 | D01, D14, D15 |
| Say whether BOTH gates stay (start approval and plan approval after the claim). Yes: PR 682 is reverted. Only the start gate: PR 682 stands under three conditions, with a written ruling naming decisions 2, 3, 6 and Q35 to Q38 | D03, D14 |
| Confirm that grant rows, `--apply` goes and the cleanup-design approval are given in chat and recorded by the agent, and that "narrow d2" did not restore an owner-written row; then `WORKER-CONTRACT.md:57` is fixed | Q01, D13 |
| Approve the cleanup design for issue 687, and confirm the script may run a local `git branch -d` under Q02's refusals | D13, Q01, Q02 |
| Rule on Clay's R10 (orchestrator merges and closes) against contract lines 239 to 246; say who "the owner" is for `answer-check` and for changing grants | D04, D06, D16 |
| Approve R25 (Full Submit as a per-issue go) and R17/R9 (launch-prompt authorization) as amendments to contract lines 245 and 70 | D06, D14 |
| Merge-go numbers: how long a go lasts; confirm `changes_requested` is a hard refusal; the 60-minute reviewer wait; whether the nine-row list is only an inventory | D06 |
| Guard: say when binding starts (is the first orchestrated issue the one guard-less test issue?), whether one more real issue may run unbound, and the L2 position | D05, D04 |
| Say whether a typed wake line into an idle session is acceptable at all | D10, D15 |
| Choose the poll command contract (`once` with `repos.yaml`, or one dispatcher over `orca repo list`) | D02, D07 |
| Branch roles (`Coordinator` working branch, `coordinators` records branch), one `COORD-<RepoName>` per project, the closing writer and expiry for "in flight"; optionally retitle issues 339, 423, 444, 655 | D07, D08 |
| Ruling on whether the dormant label code is replaced now, a sizing count, and who edits PR 686 (Clay, or a follow-up) | Q03, D09 |
| Observability rulings: the notice cap value and who rules, whether the observer may show entry text, whether the questions panel is an exception, where the sweep JSON is saved | D11, QG2 |
| Rule on whether `/sc:issue` may run chain commands at create (B2) and which session runs brainstorm and design at filing time | D12 |
| Answer OD-1 to OD-13 (grouped): OD-1, OD-2, OD-13 (plan depth, round 2, waiting count); OD-3, OD-4, OD-5 (naming rule scope, refused escalation, audit channel, and whether a push notice is wanted and its cap number); OD-6, OD-10, OD-11, OD-12 (no tag or publish, the close, default grants and which of the three to grant once, config protection); OD-7, OD-8, OD-9 (no interrupt, no lease, streams off) | D15, QG1 to QG4 |
| D16 package decisions: roles by login and sole code owner `@ironbelly`; a deputy or "nobody" and the channel the owner reads; a one-directional gate with admin bypass; `integration` in or out; the hold on PRs 686 and 690; wording of `docs/decisions.md`; later, guard files on CODEOWNERS; say in chat that the gate is live and binds non-owners; the 14-day review; when the temporary CODEOWNERS lines come out | D16 |
| Go age for merge automation: record a number of hours or "none" before any automation is built; keep the 60-minute merge-time reviewer hold or give another number; say whether a push notice is wanted and at what interval | OAG1 (OA-13, OA-25) |
| Decide whether to restore the `agent-work-report` skill and the PR 681 design text from the archive branch (see section G) | PR 700, D11, D14 |
| Approve R25 (the Full Submit field) in chat so that `WORKER-CONTRACT.md:245` can name the Full Submit field as the one exception to "no earlier pre-authorization waives this"; the amendment must not call the field "live", and R25's "nothing else is pushed" must include the loop pushes of the one `/sc:pr-submit --monitor 3` run it starts | Q04, D06 (OA-7) |
| Decide whether `orca_worktree.py` should create the claim worktree with an agent (the issue-folder copy would then have to happen another way), or whether the contract wording stays as it now reads on PR 697; the two open threads on `WORKER-CONTRACT.md:298` wait on this | PR 697 (item (m)) |
| Schedule the follow-up change for the guard bypass at `launch-level-guard.sh:444` (a bound worker reaching the release command through Python), with the independent review the G2 design note requires | PR 697 (item (m)), D05 |
| Observer rulings: contents of the entry-field allowlist, the length cap, whether `how` may show, what counts as an "old" sweep file; name who owns the follow-up for one shared question id; name the owner of the contract note | OAG2 (OA-9, OA-17) |
| Planb first run: after the throwaway repo run (S17) passes, turn `auto_enable` on once in the defaults file and say in chat that this also covers creating the trigger label for later repos; confirm or amend the proposed S17 pass list; say whether init should ever create `hold:backlog` | OAG3 (OA-28) |

### D. Go for named actions (each needs the owner's go before anyone acts)

| Action | Needed by |
|---|---|
| Ask Clay to make PRs 686 and 690 drafts and not merge until told (hold step H0) | D14, D15, D16 |
| Open the revert PR for PR 682 (after the "both gates" answer and a clean dry run); merge PR 693, then adapted PR 690; merge PR 685 | D03, D14 |
| Commit and push the planb branch as a draft and land it first; do not resume its half-finished `/sc:implement` ledger across the rebase | D14, D15 |
| Throwaway test PRs (they write to GitHub): two from Clay's account, one owner-authored | D16 |
| One local send into a busy worker (U40) and the other live checks (U5, U25, U28, U8) before the poll is enabled | QG4, D10, D15 |
| Post to issues 450, 655, 687, 689 (assignees edit; agents write nothing) | D14 |
| Run the S17 throwaway-repo stage and record its pass list (after Coder issues 515 and 516 land and the X-001 check is run) | OAG3 |

### E. Design approvals

| Action | Needed by |
|---|---|
| Review and approve the design amendment PR (`docs/designs/orchestrator.md`, still marked "approved by the owner (Clay)"); no builder starts PR B or PR E before it merges | D01, D03, D06, D14 |
| Accept or amend each verdict: they are recommendations, not rulings | all |

### F. Owner-only items from the brainstorm triage (the spec uses the safe default until the owner acts)

| OA | What only the owner can do | Safe default meanwhile |
|---|---|---|
| OA-5 | Set the server-side ruleset on `master` and `integration` | No ruleset assumed; controls say "narrows" |
| OA-6 | Name what counts as "the owner" for typed answers on the shared login | Unnamed; every merge typed by hand |
| OA-7 | Confirm the new wording of `WORKER-CONTRACT.md` lines 57, 70 and 245 in one chat message | Line 57 fix prepared, not shipped; lines 70 and 245 not in force |
| OA-11 | Grant which of the three standing entries (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`) | `grants` empty and fail closed |
| OA-18 | Per repo: consent to script-started coordinators (`coordinator_autostart`) and to a typed wake line | Both off; file pull and mailbox only |
| OA-19 | Per repo: switch the watcher on | Every repo off; one throwaway repo at most, cap 1 |
| OA-20 | Flip `WORKER_BINDING_PROVEN` after the live binding probe; later open level FS | Not flipped; no worker on a real issue |
| OA-21 | Confirm the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656) | Not confirmed; per-host diff before every install |
| OA-23 | Choose the claim route after the X-001 live check (and any change to Coder issue 516) | Poll-launched claims on a throwaway issue only, cap 1 |

### G. Changes caused by PR 700 (2026-11-20)

| Action | Needed by |
|---|---|
| Decide whether to restore the `agent-work-report` skill (PR 684) and the design text (PR 681) from the archive branch `clayphi/archive-orchestrator-655-20261120`, in a later owner-approved PR. Until then, the verdict actions that depend on them (D11's report work, D14's banner and design amendment, D15 rows E1 to E5 and the design DOC rows) stay parked | D11, D14, D15 |
| Note: PR 700 was again merged by its author (Clay) with no owner review, 21 minutes after opening, . Master had no server-side protection when D16 checked (not re-checked). The review rule of D16 (an owner approval on named paths, gated by a ruleset) would apply; whether it would have stopped this merge is UNVERIFIED, and it is not in place until the owner sets the ruleset | D16, D14 |
| Per host: run `superclaude update` on any host that installed between 00:02 and 15:07 UTC on 2026-11-20 (after PR 682, before PR 700) | INSTALL-TEST result, D03 |
| Earlier actions now moot or done: "open the revert PR for PR 682" (done by PR 700; PR 697 closed); "banner on the design document" and "design amendment PR" (the file is gone); "ask Clay to make PRs 686 and 690 drafts" (they are drafts; the ruleset part remains) | D03, D14, D15 |

## Where verdicts disagree

D15 resolved seven conflicts between earlier verdicts (R-1 to R-7); they are listed first. The rest were found while reading all 42 entries and the triage. Where two verdicts differ, the spec should follow the one named.

### Resolved by D15

| # | Conflict | Follow |
|---|---|---|
| R-1 | The skip reason for a missing plan is `plan_incomplete` (D01), `held_incomplete` (D09 and the code) or `plan_missing` (design line 543) | `held_incomplete` and `held_backlog`; retire the others and recompute the reasons-table pin |
| R-2 | The plan check lives in `hold.py` (D01, D09) or `plan_body.py` imported by `hold.py` (D12) | `plan_body.py check` is the single definition (D14 agreed) |
| R-3 | Settings home: `repos.yaml` keys (D04, D06) or per-repo JSON (D07) | Per-repo JSON in the project-local config; PR 686's `repos.py` supplies key names only |
| R-4 | Default `grants`: none (D04 item 7) or four standing entries (D04 action row) | Empty; the owner grants the standing entries once in chat (see OD-11) |
| R-5 | Closeout needs `issue.close` (design, D13) but no standing `issue.close` is allowed (D04, D06) | The per-PR go covers the close (OD-10 settled it) |
| R-6 | Hand-back re-plans the body, which voids the approval (D01 item 5) | Round 2 passes the start gate again (OD-2 settled it) |
| R-7 | The design lists 12 verbs including a deferred lease and an interrupt, and no merge verb | The spec lists the verbs it builds: wake-check, wake-ack, state, plan-check, repos, a merge verb, merge-gate, answer-check, audit, report-entry, escalate (no interrupt), handback |

### Found while writing this record (X-1 to X-13 from the first 32 entries, X-14 to X-19 from the OA debates and triage, X-20 to X-22 from the spec pass and Q04, X-23 from the PR 700 update)

| # | Disagreement | Follow |
|---|---|---|
| X-1 | D04 and Q01 list four standing grants including `issue.hold`; Q03 removes `issue.hold` with the label code | Three standing entries (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`), default empty (Q03, D15, QG3) |
| X-2 | D13 says `git branch -d` "refuses an unmerged branch"; Q02 measured that it deleted a pushed, unmerged branch and the merged `integration` and `master` | Q02: `-d` is a backstop, the nine rules are the gate; use Q02's added refusals |
| X-3 | D14 assumed `git branch -d` was still open and that the label writer is left out; Q01, Q02, Q03 were not written yet | Q02 (yes with refusals) and Q03 (read-only variant); D14's rows for issue 687 and PR 686 follow them |
| X-4 | D09 left open whether the dormant label code ships in PR 686 | Q03: replace it with the read-only variant now |
| X-5 | D15's OD-5 says entry lines only until the owner rules on the whole nine-row list and cap; QG2's OD-5 says entry lines first plus a reserved push notice for AU4a, AU4c and AU5 that no longer waits on the other eight rows if the verb accepts row 8 alone (UNVERIFIED) | QG2 (the later and narrower answer) |
| X-6 | D03 says PR 682 stands only if D01 ends with "assignment is the only trigger, no gate"; D14 says PR 682 stands also if the owner says only the start gate stays (D01 itself says the start approval and the plan approval after the claim are different gates and does not decide PR 682) | D14: the revert needs the owner to say BOTH gates stay |
| X-7 | D10 uses the typed line `/sc:orchestrator --wake <id>` and the tag `orchestrator-<short>-<n>`; D08 renames them to coordinator names | D08, before PR 686 merges |
| X-8 | D02 says the poll command (`once` or `run-all`) must be named before the scheduler; D14 still lists the poll command contract as open; D07 already chose one dispatcher over `orca repo list` (`run-all`) | D07's topology, but the owner still has to confirm it (see Actions, section C) |
| X-9 | D15 and the debate papers assume the info-stream searches "fail open"; QG4 found in PR 686's code that they have no off switch and a failed search stops the whole discovery cycle | QG4: add an off switch and make a failed search a warning (a fifth action on the adapted PR 686) |
| X-10 | D15's OD-1 row cites D12 item 6 as its source; QG1 says the direct source is D15's own merged position G-2 | QG1 (a minor citation fix, low priority) |
| X-11 | D03 says the owner's planb branch has 223 status entries; D14 says 348 today (69 code, tests and docs) and that an earlier analysis said 225 | D14 (the latest count; the figure changes as the branch is edited) |
| X-12 | The progress log says planb "finished FINAL: pass at 03:34Z"; D14 and D15 say not to resume its "half-finished `/sc:implement` ledger" across the rebase | UNVERIFIED which is current; the owner should confirm the planb state before it is rebased |
| X-13 | D16 makes the owner the one authority for CODEOWNERS edits; Clay's merged design (lines 288 and 593) makes Clay the authority; D16 and D06 also note the design says "approved by the owner (Clay)" | D16, with the design amended in a new PR; Clay's written acceptance should come before the gate is announced |
| X-14 | D06 item 1 says a merge go "expires" (number an owner decision); Q01 item 5 says it ends only on the action, a head move or a revoke | OAG1: follow Q01 as the default (no clock in the first build), keep D06's number as the owner's open option, and require an age check before any merge automation is built |
| X-15 | The OA topic text says Clay's ADD4 holds a PR with "no stated wait"; ADD4 states 60 minutes after the head's checks finish | OAG1: ADD4 as written (60 minutes, owner-settable, UNVERIFIED) |
| X-16 | The brainstorm's K9 says a waiting go counts toward `max_in_flight`; QG1's OD-13 says a hand-back waiting for re-approval does not | OAG1: both stand; a waiting merge go (worker finished, PR open) counts and never expires, a `waiting_reapproval` hand-back (no worker, no PR) does not count and may expire on an owner-set limit |
| X-17 | D11 says "one data source"; OAG2 finds the observer's questions panel reads Orca directly | OAG2: say "one source for session facts (the sweep); the questions panel is the one exception" |
| X-18 | D09 rule 2 and D15 row A3 have per-repo init create both labels; OAG3 finds planb creates only the trigger label and sets `hold:backlog` aside | OAG3: init creates only the trigger label, and only once the owner turns `auto_enable` on (read-only `would_create` before that); `hold:backlog` stays by hand until the owner asks |
| X-19 | OA-TRIAGE treats OA-1 (both gates stay, PR 682 reverted) as SETTLED; D01 says it does not decide PR 682, and D14 makes the revert depend on the owner saying in chat that BOTH gates stay | D14: the owner's chat answer is still needed (listed in Actions, section C) |
| X-20 | The spec (per the coordinator's report) requires a per-repo chat OK for creating the trigger label (spec row X-18, finding F10), while OAG3 lets one S17 flip cover label creation for later repos (class-level); the spec's X-18 is a different number from this record's X-18 | The spec's stricter per-repo OK is the current default; the owner can still choose OAG3's class-level cover at the S17 flip (OA-28b) |
| X-21 | D06 item 7 says a Full Submit push counts as the person's go "for that issue's push and pull request only"; Q04 says it also covers the fix-round pushes of the one `/sc:pr-submit --monitor 3` run it starts, and that R25's "nothing else is pushed" must be amended to say so | Q04 (the WC:245 amendment names both, after the owner approves R25 in chat) |
| X-22 | Q04's debate text said the Full Submit field is "given in the live session at the time of the run"; the verdict finds that wrong, because the field is set before the commits exist and WC:245 forbids earlier pre-authorization | The Q04 verdict: the field is a named exception; only the typed run line is live |
| X-23 | D05 item 6 and its action say guard G2 rule 1 "stays removed" (keep PR 682's guard edit); D03 and D14 recommend reverting PR 682, which brings rule 1 back, and PR 700 has now restored it | The restored state (D03, D14). The guard change still needs the independent review the G2 design note requires |

Contradictions found: 30 (7 resolved by D15, 23 found while writing). Where a contradiction was found between a verdict and a claim in a topic or an issue (for example TOPICS.md calls issues 687 and 689 pull requests; D12, D13 and D14 corrected this to issues), the verdicts' correction was used.
