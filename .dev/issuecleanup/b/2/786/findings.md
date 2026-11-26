# Round 2 findings: issue #786 (C5) Orca Run lifecycle: create once, rebind after a restart

Checked against master `f2894fc44`, 2026-11-24. Read-only. Plan files: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`. R38 is at `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64` in this worktree. Round 1: `.../Analyze716/.dev/issuecleanup/a716/2/786/findings.md`. Umbrella #716, its backlog review and closing review were read.

## Alignment with architectural decisions

- **R38 (requirements.md:64), point C: aligned on need, in conflict on the old restart mechanism.** R38 keeps "one standing coordinator per project, `COORD-<RepoName>` in the `Coordinator` worktree (Coder issue 516)" and drops "wake file with acknowledgment". FR-34 (SPEC.md:236, restart a dead coordinator "with a resume wake, at most 3 times") and D07 verdict item 4 (debates/D07/VERDICT.md:18, "Guarded restart, adopted (CLAY)") are Clay rows that R38 voids. So the restart that triggers C5 is now Coder 516's session-start check (a new terminal), not a wake. C5's rebind rule is needed after any new terminal whatever starts it, so the item stands; its "Done when" must not name a wake or FR-34.
- **PR #735 (one coordinator per project, WORKER-CONTRACT.md:294): aligned.** One coordinator per project is the premise of "create or reuse one Run for its repo". It does not say one Run per project; that stays open (below).
- **WC-16 and "The wait" (WORKER-CONTRACT.md:102-105, :290: one wait per Run inbox):** aligned. The wait covers one Run's inbox, so a restarted coordinator that is unbound or bound to another Run cannot read worker messages.
- **WC-6 (WORKER-CONTRACT.md:75) and "never relaunch a dead worker by itself" (:303): aligned.** C5 rebinds the coordinator, not a worker. The item's second done-when ("no second claim, no second worker") fits WC-6. Memory note `orca-coordinator-rebind-after-resume.md` (2026-11-04): a closed terminal returns its Task to `ready`, so `--retry-of` is refused; that agrees with WC-6's "every retry is a new Task".
- **WC-8 / WC-13 (:40, :63): aligned.** Only the coordinator binds a Run; no command or worker does.
- **Observer and sweep read-only rule: aligned.** `src/superclaude/cli/observe/adapter.py:34-50` forbids `run-use` and `run-create` (lines 43-44); `src/superclaude/cli/sweep/probes.py:45-58` allows only `run-current`. C5's code must live outside both packages (my architecture pass in `analyze/analyze-report.md`).
- **FR-21 / FR-29 (SPEC.md:211, :231: unknown launch never relaunches; one adoption record per issue):** aligned; C5 keeps the Run id in the same coordinator state and adds no second store (see #755 and #716 review: "do not add a competing state store").
- **Open decision, not a conflict:** the plan has no Run-count rule. I searched SPEC.md, DECISIONS.md and all verdicts for `run-use`, `run-current`, `run-create`, `consumer_fenced`: the only hit is SPEC.md section 12.2 (U5, mailbox from outside a Run, UNVERIFIED). #755 holds that decision. C5's "creates a Run on first start" assumes the answer.
- **Live Orca facts (2026-11-24, `orca skills get orchestration`):** line 110 `run-create --objective`; line 116 "After a restart, resume your own Run with `run-use --id <run_id>`". The rebind rule is stated by Orca today, so the memory note's age (2026-11-04) no longer makes it uncertain. Whether a restart still ends in `consumer_fenced` on `worker-start`: seen in #755 on 2026-11-23, not re-run here (UNVERIFIED).

## Complementary issues

- **#755 (one Run per project or many):** supplies the Run rule that C5 implements. Interface: #755 decides and writes the rule in WORKER-CONTRACT.md plus a `run-use` switch test; C5 builds the coordinator behaviour (state record, `run-current` then `run-use` before any mutation) and the restart test.
- **#788 (C7, worker start):** C5's "next `worker-start` is not refused" half needs C7's worker start. C7 needs a bound Run.
- **#800 (C19, settle each worker) and #771 (closeout in the coordinator's finish):** both need a bound Run; closeout's `settle.sh:1128` reads `run-current` and escalates `no_orca` without one.
- **#785 (C4):** the loaded guide's Run text feeds C5's rule; C4 loads first.
- **#782 (C1):** the skill must exist for any of this.
- **#757, #765, #767:** each can force a restart (cron wake, killed watch, compaction), when the rebind matters. #757's scheduled task must stay read-only (no `run-use`).
- **#770 (watcher hands claims to the coordinator):** adoption needs a bound Run first.

## Closest overlap

**#755 "Coordinator created multiple Orca Runs by default; find why, set a Run rule, compare one Run per project vs many".** Shared: when a Run is created, reused or switched; that `run-current` and `run-list` come before any `run-create`; the `run-use` behaviour test; the restart rebind. Estimate: #755's done-when items 3 and 4 cover about 40 percent of #786's done-when (the rule and a switch test), but not the kill-and-restart test of the coordinator with `worker-start`, and not the stored Run id or the skill step.
Next two: **#788 (C7)**, about 20 percent (the "worker-start not refused" half of the test uses its worker start); **#800 (C19)**, about 10 percent (needs the same bound Run, checks `reclaimable` terminals at the end).

## Standalone or merge

**Verdict: stand alone, sequenced after #755's rule.** Tested against #755:
- Owner: #755 is an owner decision plus research (owner records the decision, item 5 consolidates three split Runs); #786 is a build item for whoever builds the skill. Different owner role.
- Acceptance test: #755 is a written comparison, a rule text with a keep-the-rule check, and a throwaway-project `run-use` experiment. #786 is a coordinator kill-and-restart test against a live Orca with a following `worker-start`.
- Files touched: #755 edits `src/superclaude/core/WORKER-CONTRACT.md` (and maybe `core/CLAUDE.md`). #786 adds a ref file, a state-record field and a test in the coordinator skill and its tests.
- Build phase: #755 can be done now, it needs no skill and was rated P1 (2026-11-24 backlog review on #755). #786 is Phase 2 of #716 and waits for C1 and C7.
- Risk if merged: #755 is ready today and would be held back by a skill that does not exist; or the skill item would carry an unmade owner decision.
Deciding reason: different owner decision versus build, and different phase. Merging would be right only if the owner decides #755's answer is "one Run per project, rule only", with no experiment; then #755's rule text and C5's test could be one pull request. Until then keep both and make #786 cite #755 as the source of the rule.

## Closed issues and merged PRs checked

- **#444 (closed, sub-orchestrator evaluation):** no Run rule came out of it.
- **#431 (closed, orchestrator waits on workers that went quiet):** introduced the liveness rules; nothing on Runs.
- **PR #434 (merged, v1 worker-liveness rules in the contract):** S0-S11 states and "The wait"; it assumes a bound Run, gives no bind rule.
- **PR #539 (merged, `/sc:sweep`):** reads `run-current` only (probes.py:304, :398); it never binds, which C5 must preserve.
- **PR #514 and #503 (merged, observer questions for one named Run):** the questions read uses `--run <runId>` and "no `run-use`, no rotation across Runs" (PR #514 body). So any cross-Run read is excluded by design.
- **PR #683 (merged, `/sc:closeout`):** `settle.sh:1128` needs a bound Run; the first live use is the proof that unbound sessions cannot settle.
- **PR #735 and #736 (merged):** one coordinator per project; script-started allowed, which is why a restart rebind cannot rely on a person typing `run-use`.
- **PR #591 (merged, Plan B):** coordinator duties "Reserve before starting", with no Run rule.
- **#796, #804, #806, #798, #809 (closed or merged on 2026-11-24):** none carries a Run rule. #796 (plan request, closed) removes one reader of the wake item that would have needed a bound Run.

## Updated recommendation

- **Action:** keep open with changes. (1) Cite #755 as the source of the Run rule; change "creates an Orca Run on first start" to "uses the Run its state record names; if none, applies the rule from #755 (check `run-current` and `run-list` before any `run-create`)". (2) Drop the "UNVERIFIED against today's Orca" note for the rebind rule: Orca's own guide (line 116) states it. (3) Remove any link to FR-34, a wake, or Clay's restart; the restart in scope is Coder 516's session-start check (R38 C). (4) Name C7 (#788) as blocker of the second done-when line. (5) Keep Run-binding code outside `cli/observe` and `cli/sweep`, and add a test that those packages still list `run-use` and `run-create` as forbidden.
- **Priority:** P2. **Complexity:** medium, size M.
- **Change from round 1:** priority, complexity and size unchanged. Changed: the restart trigger (Coder 516 check, not an FR-34 wake, from R38 which round 1 could not find), the sequencing against S13 to S15 (voided in part), and an explicit read-only test for sweep and observer.

## Scan record

- Lists read in full (titles): open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: Run, run-use, consumer_fenced, restart, resume, worker-start, coordinator, rebind, settle, closeout, sweep, observer, liveness.
- Opened in full: open #716, #755 (with its 2 comments), #782, #783, #788, #800, #793, #761, #770, #757, #771, #725, #794, #805, #807; closed #806, #796, #798, #804, #809, #444, #507. Merged PRs opened: #591, #514, #539, #735, #736, #683. #431 and #434 read by title only in the lists (not opened in full).
- Command run: `/sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/2/analyze` (shared by the three items).
- UNVERIFIED: whether a restart today still ends in `consumer_fenced`; whether Coder 516 has landed (other repository); whether the owner re-staged S15 after R38; no Run was created or rebound by me.
