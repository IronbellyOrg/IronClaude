# Verdict D03: PR 682, the deletion of the issue pipeline

## Question

PR 682 (Clay, merged 2026-11-20 00:02 UTC) deleted `src/superclaude/cli/issue_pipeline/` (plan hash, approval-line check, adoption/approval stores, release-worker), WC-17 and the "Issue pipeline duties" section in WORKER-CONTRACT.md, and guard G2 rule 1. Should the owner REVERT it, KEEP it, or RESTORE parts on top of master? The owner's PRs 584 (Plan A) and 591 (Plan B) built it on 2026-11-17 for owner decision 6 = B. Weigh the "never ran live" argument, protections the old tests pinned (one winner on a race, a killed start blocks a second, refusal of bot or edited approvals), and what the owner's local branch `ironbelly/issue-watcher-zero-setup-plan` still depends on.

## Winner

HYBRID (OURS in substance: revert PR 682, keeping three small separable pieces from CLAY); the revert is the default until topic D01 (whether any plan-approval gate should exist) rules, and PR 682 stands only if D01 goes to CLAY under three conditions.

## Winning recommendation

The spec must say all of the following (each is testable):

1. **Revert as one new PR.** `git revert 01e7a9e23` on top of master as a new PR (never a force-push), so `src/superclaude/cli/issue_pipeline/`, WC-17, "Issue pipeline duties" and guard G2 rule 1 return. Test: after the PR, `uv run superclaude issue-pipeline --help` works and the rule-1 tamper tests in `tests/hooks/test_launch_level_guard_worker.py` pass again. Size: 4,599 lines (2,969 test lines, 1,618 source lines; the package is 1,597). Only 3 of the 36 files changed later on master; the real textual conflict is `CHANGELOG.md` only (`git merge-tree`, per the fault-finder), the other two auto-merge.
2. **Keep the no `--to` bullet by hand.** After the revert, re-apply PR 682's standalone worker-duties bullet "ask and send carry no `--to`" and its assertions in `tests/skills/test_worker_contract.py` (lines 426-429 and 3220 on master). A bare revert drops both silently and tests still pass. The sentence will appear twice (WC-17 line 59 and the bullet), or WC-17 is reworded to point at the bullet.
3. **PR 686 must not merge ahead of this decision (mandatory precondition).** Git merges the revert and PR 686 (head 8e5ae29ad) with no conflict beyond `CHANGELOG.md`, but the result is broken: `superclaude --help` crashes and 29 test modules fail at collection, because PR 686 deletes `issue_watch` names the restored package imports (`EditEvidence`, `LabelEvent`, `CommentEdit`, `_argv_rest_page`, `github.edits`, `github.events`, `cycle.validate_approvers`). If the revert lands first, PR 686 needs a revision that keeps those names or a shim. A merge condition: run `superclaude --help` and import the package. The order is for topic D14.
4. **Same PR, or a named follow-up, amends the design.** `docs/designs/orchestrator.md` rule R1 (line 73) and section 7 (lines 987-1004, 1017, 1095, 1381) say the gate is retired; PRs A, B, E build against that text. Amend R1 and section 7 to say "the plan-approval gate is kept until the owner rules" or name the follow-up.
5. **After the revert lands, hosts run `superclaude install`** (installed guard, `WORKER-CONTRACT.md` and CLI still differ from both versions on the checked host). The guard needs its independent review (the G2 design note requires one for any guard change). The guard version stamp stays 1; raising it to 2 is a guard change that belongs to owner row R33.
6. **Keep the creation-time plan sections** of `/sc:issue --create` (Priority, Fix approach, Test plan; PRs 651 and 661) as an extra layer. They do not replace approval: `hold.py` only checks the headings are filled in.
7. **Conditional on D01.** If D01 ends with "assignment is the only trigger, no gate", PR 682 stands under three conditions both advocates accepted: (a) PR B and its named tests (kill after each `intent` and before `done` resumes without repeating the act; exclusive create refuses a second state file; two orchestrators given one issue create one state file; `orchestrator.md:1108-1112`) exist and pass before the watcher is enabled; (b) R33 (the closed ship gate `GOVERNED_LEVELS_ALLOWED = False`) is BUILT before R18 (default-on generated config) is built; today it is not built (no hit on master, the three snapshots or the owner branch commits), and the only hold is `cycle.py:228` `raw.get("enabled", False)`; (c) the owner gives a written ruling naming decisions 2, 3, 6 and Q35 to Q38, given in the owner's chat and recorded by the agent (a GitHub comment "by ironbelly" cannot prove who acted, because the host login is `ironbelly`).

## Strongest points

**OURS (revert):**
1. The deleted code is the owner's merged work from 2026-11-17 (PR 584 +4355/-6 and PR 591 +8786/-80, `git log` on the path shows only these two commits) and implements recorded decisions (`owner-answers.md:139`, "Go with B now"; Q35 to Q37 at lines 184-186). Source: E-pr682.md, `gh pr view 584/591 --repo IronbellyOrg/IronClaude`.
2. The protections exist only in the deleted tests (`tests/issue_pipeline/test_approval_concurrency.py:60,71`; `test_approval_crash.py:45`; `test_stage_predicates.py:291,339`; `test_approval_record.py:336`) and the replacement is design text only: `docs/designs/orchestrator.md:568, 1108-1112`; the PR 686 snapshot has no `worker-start` call in `issue_watch`. Source: `git show 01e7a9e23^`, snapshot pr-a.
3. The deletion was fast and thin: PR 682 opened 22:56:28Z and merged 00:02:36Z (66 minutes) with one automated review, 3 seconds after PR 681 (the design it relies on), both merged by `clayphi`. Source: `gh pr view 681/682 --repo IronbellyOrg/IronClaude`.

**CLAY (keep):**
1. The design on master states R1 and a file-by-file removal plan (`orchestrator.md:73, 978-1004`) and PR D first (line 1030); the removal order is real: the package imports the `issue_watch` symbols PR 686 removes (`orchestrator.md:982`; verified: INV-001 shows the break).
2. The gate had a known limit and a real cost: one login serves the owner and the agents (FU-1 record j, `issue-pipeline-fu1.md:117`; owner risk L-1, `owner-answers.md:126`) and Q36 "latency approved for now" (`owner-answers.md:185`): a person-opened coordinator, a grant row per issue, two sessions per approval.
3. Plan quality is now checked at creation (`sc-issue-protocol/SKILL.md:102`, PRs 651 and 661) and PR 682 was scoped with care (guard rule 2 kept, independent guard review recorded, E-pr682.md line 61).

## Clay strengths to adopt

- **What:** the standalone "ask and send carry no `--to`" contract bullet with its test assertion. **Why:** it states the worker side of guard rule 2 for every bound worker; WC-17 carries the sentence only inside the plan-approval flow. **How:** re-apply by hand after the revert (recommendation item 2). Note: the sentence already existed in WC-17 at `01e7a9e23^` (line 59), so PR 682 relocated it; this is a small gain, not a new protection.
- **What:** the creation-time plan sections (PRs 651, 661) and the plan hold as an extra layer. **Why:** independent of the gate and cheap. **How:** keep as is; never as a replacement for approval.
- **What:** the removal plan of design section 7.2/7.3 and the PR B test rows. **Why:** they are the sequencing input and the bar for any replacement protection if D01 goes to CLAY. **How:** referenced in recommendation item 7; override R1 text per item 4.
- **What:** the honest statement of the gate's cost and its same-login limit. **Why:** both are verified (Q36; record j). **How:** the spec records L-1 as accepted risk, not hidden.

## Our strengths that must be kept

- The approval package (plan hash, exact-line approval check, locked write-ahead adoption and approval rows, `release-worker`) with its 117 test functions and the recorded real GitHub replies from throwaway issue 452.
- Decision 6 = B and Q35 to Q38 as the owner's recorded line; WC-17 and "Issue pipeline duties" in WORKER-CONTRACT.md; guard G2 rule 1 (TAMPER class for coordinator-side verbs).
- The FU-1 live record (eleven RECORDED lines a to k) as evidence that the handoff steps ran.
- The owner's local branch can then rebase: its tracked uncommitted changes (1,767-line patch over 13 files) pass `git apply --check` on the revert tree and fail on current master for all 13 files.

## Actions

| Action | Type | Target | Order or dependency |
|--------|------|--------|---------------------|
| Open one revert PR for commit 01e7a9e23 (with `/sc:pr-submit --monitor 3`, `--repo IronbellyOrg/IronClaude`), resolving the CHANGELOG.md conflict | PR REVERT (recommendation only; not executed here) | PR 682 (merged, commit 01e7a9e23) | After the owner's go; before PR 686 merges; subject to D01 and D14 |
| Re-apply the standalone no `--to` bullet and its test assertions after the revert | LOCAL CHANGE | `src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py` | Inside the revert PR |
| Amend R1 and section 7 of the design (or open a named follow-up) | DOC | `docs/designs/orchestrator.md` lines 73, 987-1004, 1017, 1095, 1381 | Same PR or named follow-up; D14 decides |
| Hold PR 686 until the revert or the D01 ruling settles; if the revert lands first, revise PR 686 to keep the imported `issue_watch` names or add a shim; add a merge check (`superclaude --help`, package import) | DECISION | PR 686 (open, head 8e5ae29ad) | Before any merge of PR 686; owner topic D14 |
| Keep the creation-time plan sections | PR KEEP | PRs 651 and 661 (merged) | None |
| Independent review of the guard change; run `superclaude install` on hosts after merge | LOCAL CHANGE | `src/superclaude/hooks/scripts/launch-level-guard.sh` and plugin copy; hosts | After the revert merges |
| Owner records, in chat, whether the gate stays (decision D01) and names decisions 2, 3, 6, Q35 to Q38 if PR 682 is to stand | DECISION | Owner (ironbelly) | Before D14 |
| Build R33 (closed ship gate) before R18 (default-on config) | LOCAL CHANGE | owner branch `ironbelly/issue-watcher-zero-setup-plan` | Before the watcher is enabled |
| Update the figures: owner branch size (stale 53; 223 status entries), restored tests (117 functions, 222 cases) | DOC | analysis files E-pr682.md line 67 and the spec | With the spec |

## Implications

- **Watcher and coordinator.** The coordinator duties of Q35 to Q38 come back in WORKER-CONTRACT.md (adopt, reserve before start, plan approval via `ask` and `reply`, never post without a grant row). The watcher stays `enabled: false`; the owner branch keeps building on `issue_pipeline` (`complete.py`, `brief.py`).
- **Claim pipeline.** `commands/issue.md:85`, `SKILL.md:140` and `refs/claim.md:96` stop being dangling. A `--pipeline none` claim again has a consumer.
- **What breaks.** PR 686 as it stands (it deletes names the package imports); the design text (R1, section 7) until amended; the idea of "assignment is the only trigger" until D01 rules.
- **Dashboard and observer.** None directly. The restored approval rows add a store that the sweep and observer do not read (not checked here).
- **What the owner must know.** (a) The revert and PR 686 look clean to git and are broken together; (b) a bare revert silently drops the no `--to` bullet; (c) the written ruling by "ironbelly" cannot be proven by a GitHub comment alone while one login serves the person and the agents; (d) the owner's branch is the main reason to revert, and it has 223 status entries, not 53.

## Confidence

78 percent for HYBRID (revert, conditional on D01). It would drop to about 50 percent if D01 rules for assignment-only, because then PR 682 stands and the revert becomes churn (about 4,600 lines). It would rise to about 90 percent if the owner confirms in chat that the approval gate stays. The diff-point agreement of the two advocates was 88.9 percent (16 of 18). Debate status: partial, because one HIGH invariant finding (INV-001) was found at the end and standard depth has no Round 3; the verdict makes it a mandatory precondition.

## Unverified

- Whether the restored test `test_the_watcher_record_module_is_not_edited` passes in a real checkout (failed in the fault-finder's non-git scratch copy; INV-009).
- Whether the revert tree passes the full test suite and `tests/hooks/test_launch_level_guard.py` (neither finished in the fault-finder's time limit).
- Behaviour of the restored approval rows against PR 686's `record.py` schema 2 (INV-013).
- The owner branch rebase itself, and the untracked `complete.py` and its tests against the revert tree (E-pr682.md line 67).
- Who "the owner" is in the design (design says Clay; decisions are recorded under ironbelly; ironbelly is the only admin collaborator).
- Clay's claim that assignment is safe (issue 655, UNVERIFIED there; design open question OQ6 finds two gaps).
- Whether the owner saw issue 450 or 655 outside GitHub (chat, calls); the host login is shared, so GitHub alone cannot show which person acted.
- That `/sc:issue` text and runbooks banners (PR E) are unbuilt: taken from the design, not re-checked on a PR.

## Debate artifacts

- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/merged-output.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/invariant-probe.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/return-contract.yaml`
