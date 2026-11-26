# Round 2 findings: issue 823 (W15, update the owner runbook to the unified design after the live test)

Checked 2026-11-24 against master f2894fc44 in `/home/coder/workspaces/worktrees/IronClaude/Realign`. Sources: issue 823, round 1 findings (`/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/5/823/findings.md`), umbrella #717 and its closing review (items 3 and 6, and the internal-order line), `.dev/issuecleanup/b/12/analyze/analyze-report.md`.

New facts since round 1: (a) **#813 (W5) was closed on 2026-11-24 and its closing comment hands the optional manual restart proof to this item** ("make it a one-time runbook check recorded in W15"); (b) #809 (W1) was merged into #716; (c) #823's trigger "after the S17 live tests" rests on a plan stage that the owner's R38 ruling made obsolete (below).

## Alignment with architectural decisions

- **R18 and R28** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:44`, `:54`) and its notes (`requirements.md:106-107`): the shadow run, lock test and restart test became the automatic first-run check; "only the live-test record (`docs/designs/issue-watcher-setup.md` sections 7 and 8) stays an owner check, done once before the first real cycle". Partly aligned. W15's goal (a runbook a person can follow) agrees; its trigger and its "S17 record names the PR" do not, because the manual steps are now a fallback (`issue-watcher-setup.md:713`, section 17).
- **R38** (`requirements.md:64`): the merged watcher is the design, and the plan's "Clay strengths adopted" rows are superseded. In conflict with the item's wording: "PR E" is Clay's planned runbook-rewrite PR (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/DECISIONS.md:80`), and the plan's gate "no builder starts PR B or PR E before the design amendment merges" (`SPEC.md:569`, `DECISIONS.md:1347`) points at `docs/designs/orchestrator.md`, which PR 700 removed (`SPEC.md:325`, FR-68 "SUPERSEDED BY PR 700"). So "PR E", its gate and `SPEC.md:69` are not live instructions.
- **S17** (`SPEC.md:501`, "S17 live tests, then enable one throwaway repo", and `SPEC.md:45`, "The watcher is not switched on before S17"): the S17 stage depends on S14 to S16 (coordinator and merge stages that are Clay-derived). Master and #450 say the watcher has been live since 2026-11-23. In conflict as a gate; the goal survives as "after a real first-run and enable record exists".
- **FR-69 and L-02** (`SPEC.md:326`, `:355`): the plan already assigns the six-field cron line fix in `issue-watcher-setup.md` to a text change; the six-field line `0 */5 * * * *` is still on master (`issue-watcher-setup.md:281`, `:669`). Aligned, and W15 inherits it as owner of the rewrite.
- **D02** (`DECISIONS.md:99`, cron dispatcher with one entry, hybrid; `SPEC.md:200`, FR-10 five-field `*/5`): the runbook must describe one `run-all` entry. Aligned target. The live cadence is every minute per #450's closing; a Coder PR 526 is cited by #774 A.8 (UNVERIFIED: outside the repo allowed for reads).
- **WORKER-CONTRACT.md**: the contract's issue pipeline duties are not runbook text; none apply. Round 1's "issue 442 runbook" doubt is confirmed: `.dev/issues/442/observation-runbook.md` exists and is the launch-level guard observation runbook (#442 is still open), not a switch-on and switch-off guide. UNVERIFIED which text the issue author meant.

## Complementary issues

- **#774** (docs refresh): edits the other docs and files (status line of `issue-watcher.md:3`, cadence in `issue-watcher.md:15` and the Coder handoff doc); its Out of Scope gives W15 the 14.1 versus 17 rewrite of `issue-watcher-setup.md` and its acceptance criterion links the contradiction to W15 "without taking over its runbook rewrite". Interface: file split, no order needed; W15 takes the cadence and cron wording where they appear in the setup runbook.
- **#775** (comment cancels approval): option (a) edits the same file at lines 566 and 645. Interface: one file, two PRs; they need one stated order.
- **#822 (W14)**: when W14 lands, runbook lines 98, 283 and 679 change; W15 writes them.
- **#813 (W5, closed)**: its manual restart proof is now an optional section of this item.
- **#815 (W7)** and **#811 (W3)**: W7's done-when says "`check-config` or the runbook states the scopes"; W3 changes the cron instruction in section 8.7. Both add runbook lines that W15 must not overwrite.
- **#777** (map the chain): a written map of the owner steps feeds the runbook; **#716** (coordinator): the coordinator steps the runbook describes change as C-items land.
- **#442** (open, guard observations): the item names its runbook; no blocker.

## Closest overlap

- **#774: "[FEATURE] Docs refresh for the issue watcher and coordinator: stale statements and one contradiction in the worker contract"**. Shared: same documentation family, the same stale statements (never run live, five-minute cadence, "nothing manual"), the same owner and the same docs-only PR style. It covers about 10 to 15 percent of W15's done-when (cadence and status wording in sibling files) and none of the 14.1 versus 17 rewrite or the captured steps.
- Next two: **#775** (same file, lines 566 and 645; about 5 percent) and **#822 (W14)** (three lines of runbook text; about 5 percent). **#777** is a looser fourth.

## Standalone or merge

Verdict: **stand alone**, with one condition that would reverse it. Against #774:
- Owner: same owner.
- Acceptance test: #774 is a grep of listed old phrases across about ten files plus byte-copy tests for the routing guide (`tests/skills/test_issue_protocol.py:878-880`, per #774). W15 is a person following the runbook with captured steps. Different tests.
- Files touched: #774 many files across `docs/`, `src/superclaude/core/` and a plugin copy; W15 two runbook files.
- Build phase: #774 can go as soon as the owner confirms its restart rule; W15 waits on a live record.
- Risk if merged: the docs-only change set that fixes ten stale statements would wait for a live capture; or the runbook would be rewritten without captured steps.
Merging would be right if the owner drops the "real captured steps" requirement: then W15 becomes "fix the 14.1 versus 17 contradiction, the six-field cron line and the cadence wording in one file", which is docs-only like #774 and could be its part A.9. Today the owner's closing of #813 keeps the captured-steps idea alive, so the issue stays separate.

## Closed issues and merged PRs checked

- **#450**, closed 2026-11-24: watcher live, cron installed, 284 cycles; lists the runbook contradiction and the missing live-test record as leftovers (items 2 and 3). `docs/designs/issue-watcher-live-test.md` named there does not exist (checked with `ls`).
- **#813 (W5)**, closed not planned: hands the manual proof to W15.
- **#809 (W1)**, closed, merged into #716: no runbook effect.
- **PR 707** (merged 2026-11-20): wrote runbook section 17 and the `Approved` field text.
- **PR 485** (merged 2026-11-10): rollout checklist, cron section 8.7, capture sheet 14.1.1.
- **PR 548** (merged 2026-11-14): option 3 claim-level decision in the runbook.
- **PR 754** (merged 2026-11-23): wording of "person-opened" in the runbook.
- **PR 729** (merged): records R38.
- **PR 700** (merged): removed `docs/designs/orchestrator.md`, which is why PR E's gate is dead.
- **PR 759 and #751**: first-run failure retry; the runbook's failure text may need a line.
None is a rewrite from a captured live run.

## Updated recommendation

Keep open with changes, **P2**, **medium**, size **M**. Unchanged from round 1 on action, priority, complexity and size. Changes to the changes:
1. Replace the gate "after the S17 live tests" with "after a real first-run and enable record from a live host exists"; drop "PR E" and the dependency on the deleted orchestrator design.
2. Say this item owns the 14.1 versus 17 contradiction, the six-field cron line (`issue-watcher-setup.md:281`, `:669`), the cadence wording and, new in round 2, the optional one-time restart-persistence check handed over by the #813 closing.
3. Ask the owner which #442 text was meant and keep it as a target only if confirmed.
4. Name an order with #775 option (a) for lines 566 and 645.
The owner decides.

## Scan record

Lists read in full: open-issues.tsv 134 of 134, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508. Search terms: runbook, setup, docs, watcher, live, enable, cron, cadence, rollout, first-run, W-numbers, 442, 450. Opened with gh: open #717, #716, #770, #774, #775, #777, #761, #811, #815, #816, #820, #822, #442 (13); closed #450, #751, #809, #813 (4) and merged PRs #447, #485, #548, #707, #729, #754, #759 (7, which with the closed issues gives 11). Local reads: runbook structure, `ls` of the live-test record and the 442 runbook. Command run: the `/sc:analyze` report named above. UNVERIFIED: Coder PR 526 (cadence), whether any S17 or first-run capture exists outside the repo, the true meaning of "the issue 442 runbook".
