<!-- Merged output for debate D14 (final disposition of PR 686 and related items). Base: Variant 1 (OURS, ADV/variant-1-original.md). Non-base: Variant 2 (CLAY). Merge date: 2026-11-20. Produced by the merge-executor from ADV/refactor-plan.md (changes 1 to 9). -->
# D14 merged disposition: PR 686 and the items around it

Status: a set of recommendations. No GitHub, Orca or git action is carried out by this document or by the task that wrote it. Every disposition below stays a recommendation until the owner gives it in chat and the agent records it.

## 1. Terms and notation

<!-- Source: Base modified (the base paper's term list was extended to cover lanes, "go", invariants and the number glosses; sources: ADV/refactor-plan.md changes 1 and 4, ADV/rounds/round2-rebuttal-OURS.md notation line, ADV/invariant-probe.md header) -->

- **Dnn**: the verdict file `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Dnn/VERDICT.md` for topic nn (D01 to D13). All thirteen are HYBRID with the owner's rule as the base on every contested rule.
- **planb**: the owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan`, in the worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`.
- **lane**: a run of steps that can proceed without waiting for the other runs. Lane 1 is the small `/sc:issue` changes. Lane 2 is the revert, the amendments, planb and the adapted PR 686. Lane 3 is the verdict actions that do not need PR 686. A "hold step" comes before all three.
- **go**: the owner's approval for one named action, given in the owner's chat and recorded by the agent as a quote with the date (INV-009: one login serves the owner and every host session, so a GitHub comment under that login proves nothing). Nothing outward happens without a go for that action and that head.
- **the gate**: a person's approval before work starts. There are two: the start approval (owner requirements R19, R22, R35, R36) and the plan approval after the claim (WC-17, the reply to a worker's own ask).
- **INV-nnn**: a finding in `ADV/invariant-probe.md` (28 findings, 4 of them HIGH and unaddressed before this merge).
- **ADV, ROU, RCL**: ADV is the folder `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/`. ROU and RCL are the round 2 rebuttal files of OURS and CLAY in `ADV/rounds/`. "R-1 to R-5" are the five open differences settled there; "X-nnn", "C-nnn" and "A-nnn" are diff-analysis points. "D03 INV-001" is the fault-finder item inside verdict D03, not a probe item of this debate.
- **PR A to PR E, PR P, PR B and PR E**: the labels in issue 655's plan. PR A is PR 686, PR C is PR 684, PR D is PR 682, PR P is PR 690. PR B (the orchestrator skill) and PR E (the live test) are unbuilt: no branch or PR exists.
- **Row labels**: R-numbers such as R19 and R33 are owner requirement rows in planb; K12, DQ7, ADD1 and OD1 are row labels in the design file; "Q01" is a separate owner-question paper cited by the rebuttals (its file was not read for this merge, UNVERIFIED).
- **Rule A and Rule B**: the two halves of the fix for the wake-acknowledgment defect M1. Rule A is on the writer (state file first, then the acknowledgment). Rule B is on the reader (the poll accepts an acknowledgment only when the state file exists).
- "Recommend" means advice to the owner. "Condition" means something that must be true before a step starts.

Numbers used in this document, each with its meaning:

- PR 686: Clay's rewrite of the issue watcher (head `8e5ae29ad`, open, 59 files). PR 690: adds `/sc:issue --plan` and `--remaining` (branch `issue-655-pr-p`, head `f3bc77981`, open, 13 files). PR 693: the owner's change that saves the claim launch result file (for issue 691, head `563df6839`, open).
- PR 681: the merged design file `docs/designs/orchestrator.md`. PR 682: the merged deletion of the old plan-approval package `issue_pipeline` (commit `01e7a9e23`). PR 683: the merged `/sc:closeout` command. PR 684: the merged move of the work-report skill. PR 685: the owner's open docs PR with the issue 442 runbook and results.
- Issue 655: Clay's tracking issue for the orchestrator work (says "replaces #450"). Issue 450: the owner's rollout issue for the watcher. Issue 687: a proposal for daily cleanup of merged worktrees. Issue 689: a proposal to plan everything at issue creation. Issue 442: the owner's live-test issue for the launch guard. Issue 339: the owner's umbrella for session-close duties.
- PRs 584 and 591: the owner's merged plan-approval package (Plan A and Plan B, merged 2026-11-17) that PR 682 deleted. PR 633: the merged install change whose retire step removes commands and skills that 6.0.0 no longer ships. PR 661: the merged change that adds plan sections to issue templates.
- Coder issues 515 (cron wording), 516 (Coordinator branch, worktree and session) and 477 (listener narrowing) are in the separate Coder repository and are unread by this debate.

## 2. Decision in one paragraph

<!-- Source: Base modified (replaces the base claim "split PR 686 and close the original" with the converged position; sources: ADV/rounds/round2-rebuttal-OURS.md section 2 R-1 to R-3, ADV/rounds/round2-rebuttal-CLAY.md section 2; refactor-plan change 1 and change 2) -->

Recommend that, first, the owner asks Clay in chat to make PR 686 and PR 690 drafts and not merge them until the owner says, and considers a ruleset on `master` that requires a review by someone other than the author (today `master` is unprotected, so one merge click could undo the plan). Then run two independent lanes. Lane 1: merge the owner's PR 693, then rebase and adapt PR 690 (four fixes from D12), then the claim rule C1. Lane 2: on the owner's go that both gates stay, revert PR 682 as one new PR (with a dry run in a clean git checkout bound to a master head, and with the same PR correcting the three design statements that say the gate is retired), then a contract and guard amendment PR, then a later design amendment PR after the owner's rulings; planb is pushed as a draft and lands first; PR 686 is not merged as it stands, it is adapted in place as a draft on top of planb, with the owner's rules as the base, the D01 names kept, and the merge checks in section 5. Keep PRs 681 (banner now, amendment later), 683, 684 and 685, keep issue 450 open, rescope issue 655, split and defer issue 689, and keep the eight "confirm approval" removal PRs, which block only the host install step. The one condition that would flip the lane 2 rows: if the owner answers Q1 "only the start gate stays", PR 682 stands under D03 item 7. The debate reached 21 of 21 positions in agreement; the status is partial because four HIGH invariants (INV-006, INV-018, INV-026, INV-027) were not covered by either side and are turned here into the conditions in sections 3 and 4.

## 3. Disposition table

<!-- Source: Variant 2 / ADV/rounds/round2-rebuttal-OURS.md section 4 and ADV/rounds/round2-rebuttal-CLAY.md section 4 (refactor-plan change 3), conditions tightened by ADV/invariant-probe.md (INV-005, 006, 007, 009, 018, 019, 026, 027) and rows from change 8 (ADV/rounds/round2-rebuttal-CLAY.md section 3 item 1; inventory/clay-prs.md tables 2A to 2C) -->

Every row is a recommendation. "Go" is defined in section 1. Every merge also needs a go for that PR and that head, and green CI (INV-006: `master` is unprotected, so red CI blocks a merge only if someone obeys it). "NEW PR" is not one of the eight standard labels; it marks a change that does not exist yet and would be written after the step it names. Dispositions that carry two words (for example KEEP and RESCOPE, SPLIT and DEFER) apply both in the order given.

| Item | Disposition | Why (one line, cited) | Conditions that must hold first |
|---|---|---|---|
| PR 686 (Clay's watcher rewrite, open, head `8e5ae29ad`) | REBASE-AND-ADAPT in place, as a draft; not merged as it stands | It deletes 14 symbols in `predicates.py` and about 30 in `github.py` that D01 keeps, and the revert plus 686 gives a crashing `superclaude --help` (D03 INV-001); no verdict says CLOSE, nine say KEEP-ADAPT (CLAY round 1 strength 4); no 686 module runs on post-revert master by itself (10 of 13 `predicates` names missing, ROU R-2) | Hold step done (step H0); revert merged (L2.2); planb pushed and landed first (Q4, L2.6); D08 glossary and names note done (L2.7); PR 690's `plan_body.py check` merged (L1.2); who adapts decided (Q2); every merge check in section 5; the diff drops the D01-name deletions, `repos.py`, the registry and the label writer; Rule B and the M2 fix are in; shared terminal helper with a parity test (D10); owner decision on the dormant label writer (D09) and the typed wake line (D10) |
| PR 690 (`/sc:issue --plan` and `--remaining`, branch issue-655-pr-p, open, head `f3bc77981`) and the branch `issue-655-pr-p` | REBASE-AND-ADAPT, lane 1 | Independent of the revert and of 686 (only `CHANGELOG.md` is shared with each; no path under `src/superclaude/cli/`), D12 rates it KEEP-ADAPT with four fixes, and it ships the `plan_body.py check` that D01 and D12 want imported (ROU R-1; CLAY round 1 strength 1) | PR 693 merged first (four shared files: `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`; INV-016, correcting the earlier "three text files"); a merge-only trial of 690 onto master plus 693 (UNVERIFIED: not run); D12's four fixes with tests (fence-aware heading count, one definition of "passes the check", document the `--remaining` caller, confirm live head); green CI on the rebased head; made a draft in the hold step and marked ready only after the fixes (INV-026); go |
| Issue 687 (proposal for daily cleanup of merged worktrees; an issue, not a PR) | KEEP-ADAPT (edit the text; nothing is built) | D13: replace "never run by the orchestrator" with the coordinator-runs-under-grant rule, add the `--apply` grant check and the test that records no `--force`, `-D` or `rm` | The owner approves the cleanup design in chat before any build; ruling on local `git branch -d` (D13 recommends yes, local only); the assignee makes the edit |
| Issue 689 (plan everything at creation; an issue, not a PR) | SPLIT and DEFER | D12: `--mode other` and the form fields go to a small new issue; items 1, 2, 4 and 8 wait for the owner's answer on B2; the "ruling of 2026-11-20" quoted in it is UNVERIFIED | Split after PR 690 merges; the owner answers B2 and who runs brainstorm and design at filing; the assignee makes the edit |
| PR 681 (merged design doc `docs/designs/orchestrator.md`) | KEEP with a banner now, plus a same-PR correction in the revert PR, plus a later owner-reviewed amendment PR; not reverted | The file calls Clay's rulings "the owner" (lines 3, 1030, 1035) and no review or comment by `ironbelly` exists on PRs 681 to 684, 686 or 690 (checked 2026-11-20, inventory line 48); a banner alone does not stop builders (INV-027) | Banner reads "contested, not owner-approved" and states the 2026-11-20 check; the revert PR also corrects the three statements that the gate is retired (R1 at `docs/designs/orchestrator.md:73`, lines 987-1004, line 1017); the other nine rows wait for the owner's chat rulings on D01 to D13 in the design amendment PR; no builder starts PR B or PR E (the unbuilt orchestrator skill and the live test) before that amendment merges |
| PR 682 (merged deletion of `issue_pipeline`, WC-17 and guard rule 1) | REVERT (recommendation only) as one new PR, plus the "no `--to`" bullet re-applied | Deleted the owner's PRs 584 and 591 (merged 3 days before) and was itself merged 66 minutes after opening, with a bot review only (D03 strongest points OURS 1 and 3; inventory 2A); the owner's planb builds on the deleted package; the restored package imports names that PR 686 deletes (D03 INV-001) | The owner says in chat that both gates stay (Q1); the dry run passes in a clean git checkout (INV-015), is bound to a master head sha and is repeated if master moves (INV-005), and its output is attached; the same PR corrects the three gate-retired design statements (INV-027); go; opened with `/sc:pr-submit --monitor 3`. If Q1 is "no", PR 682 stands under D03 item 7 and the 682, 686 and contract rows flip |
| PR 683 (merged `/sc:closeout`) | KEEP | Independent code; adds one list entry to the worker contract (inventory 2A); D13 keeps it | Its `/sc:issue --plan` reference resolves once PR 690 merges (D13); after the revert, line 300 returns, so closeout's issue writes need a standing grant or a recorded chat go, and closeout is named in the amendment PR's test list (RCL section 3 item 5) |
| PR 684 (merged move of the work-report skill) | KEEP-ADAPT (follow-up PR) | D11 keeps it and rules no revert; D08 finds the "orchestrator" wording at `agent-work-report/SKILL.md:12` | Follow-up PR for D08 (`SKILL.md:12`) and D11 (person-specific config out, state path configurable); after D08's names are settled |
| Issue 655 (Clay's tracking issue, "replaces #450") | KEEP and RESCOPE | The issue is a useful tracker, but "replaces #450" is rejected because 450's live test, shadow run and cron stay required under every verdict (D01, D02) | The assignee `clayphi` edits the body: drop "replaces #450", link 450's live test, shadow run and cron as the checklist; the owner approves the wording in chat |
| Issue 450 (the owner's rollout issue, assignee `ironbelly`) | KEEP open and answered | Clay's 2026-11-18 17:00:32Z comment with an `@ironbelly` mention has no reply on GitHub; a notice is not consent (X-004) | The owner answers in chat; the agent records the answer; nothing blocks on it |
| PR 693 (the owner's change that saves the claim launch result file, for issue 691, open, head `563df6839`) | MERGE first | The owner's small change goes first so that PR 690's 1,789 added test lines rebase once (ROU R-1) | Its own `/sc:pr-submit --monitor 3` loop clean; go; CI green |
| PR 685 (the owner's open docs PR with the issue 442 runbook and results) | KEEP and merge | It is the evidence for D05's staging probe; open and MERGEABLE (D05 action; RCL section 3 item 6) | The owner's own go; independent of both lanes |
| Contract and guard amendment PR (new) | NEW PR after the revert | The revert returns guard rule 1 and the owner-written grant-row text (line 300); the wording must say "recorded by the agent from the owner's chat go" (ROU R-5; Q01 fix 2) | Revert merged; Q5 recorded as answered (owner order of 2026-11-17, memory "Approvals through chat, never files"); owner chat approval of R25, R17 and R9 before the D06 edits at `WORKER-CONTRACT.md` lines 70 and 245; edits at lines 57, 70, 245, 298 and 300, guard comment at lines 441-443, `core/CLAUDE.md:58`; `tests/skills/test_worker_contract.py` pinned; planb edits the same lines (INV-019), so the owner answers Q4 knowing that cost |
| Design amendment PR (new) | NEW PR, named follow-up of the revert PR | The 681 text conflicts with ten owner rules (FULL-REPORT section 5, ten conflict rows) and several verdicts name design rows to rewrite (D01, D02, D03, D06, D07, D08, D10); INV-027 | The owner's chat rulings on D01 to D13; carries the nine rows not fixed in the revert PR (R1 line 73 and lines 987-1004 and 1017 are fixed there); no PR B or PR E starts before this merges; owner-reviewed |
| The eight "confirm approval" removal PRs: 620 (removes `/sc:save` and `/sc:load`), 622 (`/sc:build`), 627 (`/sc:improve`), 629 (cli-portify), 631 (`/sc:index`), 632 (roadmap, tasklist and sprint family, 605 files), 650 (six skills), 656 (`/task`, task-builder, level 4 of `HOW-WE-WORK.md`) | KEEP (not reverted); confirm in chat | The owner's approval on record covers wave 1 only (inventory 2B and section 6); they shipped in 6.0.0 and 6.1.0, so the question is "confirm", not "revert"; the revert does not depend on them (RCL section 3 item 1, coupling check) | Blocks nothing except the host install step (INV-018, section 4 step L2.9); the owner is asked once (non-blocking question NB-1) |
| Every other Clay PR in `inventory/clay-prs.md` tables 2A to 2C (31 PRs: 3 in table 2A, 19 in 2B after the eight above, 9 in 2C) | KEEP (one row) | No conflict with owner work found (inventory section 6); includes the closed PR 652 and the settled PR 658 (reverted by the owner's PR 662, re-merged as PR 664) | None; PR 664 is not by Clay and is also KEEP |

## 4. Order of operations

<!-- Source: Variant 2 and base merged (refactor-plan change 4): the three-lane list is ADV/rounds/round2-rebuttal-OURS.md section 5 merged with ADV/rounds/round2-rebuttal-CLAY.md section 4; the hold step and invariant fixes are from ADV/invariant-probe.md (INV-002, 003, 005, 006, 007, 008, 009, 017, 018, 019, 020, 026, 027, 028); lane 3 is refactor-plan change 7 -->

Every step is a recommendation to the owner. Every merge needs a go for that PR and that head (section 1) and green CI. A step with no outward effect (a local dry run, drafting) needs no go. Lane 1 and lane 2 are independent: the file lists of PR 682 and PR 690 overlap on `CHANGELOG.md` only, PR 686 and PR 690 overlap on `CHANGELOG.md` only (ROU R-1). Residual: whichever of the revert and PR 690 merges second resolves one small `CHANGELOG.md` hunk.

### Hold step (before everything)

- **H0. Hold PR 686 and PR 690, and consider a ruleset on `master`.** Recommend that the owner asks Clay in chat to turn PR 686 and PR 690 into drafts and not merge them until the owner says. Recommend (not take) a ruleset or branch protection on `master` that requires a review by someone other than the author (D05 and D06 both recommend it; the owner has admin; `protected` is `false` and there are 0 rulesets today). Both are GitHub writes that need the owner's go; this task does neither.
  - Needs: the owner's answer to Q3.
  - Pass check: `gh pr view 686 --repo IronbellyOrg/IronClaude --json isDraft` and the same for 690 print `true`; if the ruleset is chosen, `gh api repos/IronbellyOrg/IronClaude/branches/master` prints `protected` true or a ruleset requires a non-author review (exact output UNVERIFIED).
  - Why it is a step, not a footnote (INV-006, INV-026, HIGH): both PRs are open, non-draft, CLEAN with 6 of 6 checks green and no review decision; `clayphi` has `maintain` rights; merging PR 686 before the revert gives the crashing `superclaude --help` and failing test modules (D03 INV-001) and the revert is then no longer clean. One merge click falsifies the plan.
  - Limits (INV-008, INV-009): the hold is a request, not a rule. Both branches are in the same repository (`isCrossRepository` false), so any write collaborator can push to them, including sessions on this host under the shared login; "nobody else pushes to Clay's branches" cannot be kept by a promise. A ruleset that requires "someone other than the author" does not prove a different person reviewed while one login serves everyone.

### Lane 1 (independent of the revert and of PR 686)

- **L1.1. Merge PR 693.** Needs: its own `/sc:pr-submit --monitor 3` review loop clean; go. Pass check: merged; its head had 6 of 6 checks green.
- **L1.2. Rebase and adapt PR 690, then merge.** Needs: L1.1 merged; H0 (the PR is a draft until the fixes are in, then marked ready); a merge-only trial of 690 onto master plus 693 (UNVERIFIED, not run; if conflict-free the order is immaterial, if not then 693 first, and there are four shared files so it is never zero conflicts, INV-016); D12's four fixes with tests; Q2 if Clay is not the one who adapts. Note (INV-020): planb touches 5 of PR 690's files. Pass check: `uv run pytest tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py` pass on the rebased head; CI green.
- **L1.3. D12 claim rule C1 and the manual-claim warning.** C1 edits `refs/claim.md`, `refs/chains.md`, `templates/next-steps.md` and `tests/skills/test_issue_protocol.py`, and uses `plan_body.py check`. Needs: L1.1 and L1.2 merged. Pass check: the updated tests pass; the claim step calls `plan_body.py check`.

### Lane 2 (the revert, the amendments, planb, the adapted PR 686)

- **L2.1. Dry run of the revert in a clean git checkout; nothing is pushed.** Needs: nothing, no go. The checkout must be a real git checkout, not a scratch copy, because the restored test `test_the_watcher_record_module_is_not_edited` (`tests/issue_pipeline/test_approval_record.py:299-318`) runs `git diff --stat HEAD -- .../record.py` with `check=True` and fails outside git or with a dirty `record.py` (INV-015). The dry run is bound to one master head sha and is repeated whenever master moves, which includes every lane 1 merge (INV-005, MEDIUM). Expected conflicts: `CHANGELOG.md` (1 hunk); `WORKER-CONTRACT.md` and `tests/skills/test_worker_contract.py` auto-merge (INV-014). Pass check: a record that names the head sha and shows exit 0 or pass for: `uv run superclaude --help`; import of every package under `src/superclaude/cli/`; `tests/hooks/test_launch_level_guard.py`; `tests/issue_pipeline`; `tests/skills/test_worker_contract.py`; the full suite; `make verify-sync`. The full run on the revert tree did not finish in D03, so this is UNVERIFIED until the record exists.
- **L2.2. Open the revert PR for PR 682.** One new PR: `git revert 01e7a9e23`, resolve `CHANGELOG.md`, re-apply the standalone "ask and send carry no `--to`" bullet and its test assertions (D03 items 1 and 2), and, in the same PR, correct the three statements in `docs/designs/orchestrator.md` that say the gate is retired (R1 at line 73, lines 987-1004, line 1017; INV-027, HIGH). Opened with `/sc:pr-submit --monitor 3` against `--repo IronbellyOrg/IronClaude`; verify the returned URL is on the fork. Needs: Q1 answered "both gates stay"; H0; L2.1 passing on the current master head; go. Pass check: required checks green; after merge `uv run superclaude --help` exits 0 on `master`. Release note: `git tag --contains 01e7a9e23` is empty, so PR 682 is unreleased and the revert is not a release event (RCL section 3 item 3).
- **L2.3. Banner PR for PR 681 (docs only).** The banner reads "contested, not owner-approved" and states the fact "no owner review or comment recorded on GitHub (checked 2026-11-20)". It may run beside L2.2 or inside it. Needs: a go. Pass check: the design file contains the banner with the check date.
- **L2.4. Contract and guard amendment PR (new).** Needs: L2.2 merged; Q5 recorded as answered (owner order of 2026-11-17, memory "Approvals through chat, never files", pending Q01); the owner's chat approval of R25, R17 and R9 before the D06 edits at lines 70 and 245. Text (ROU R-5): line 57 becomes "other owner records, such as a grant row or a pass record, are given by the owner in chat and recorded by the agent from that confirmation, naming the exact scope"; line 300 becomes "post an issue write that is neither a standing grant nor covered by the owner's recorded chat go for that issue"; line 298's "write the row" gains "from the owner's chat approval"; guard comment at lines 441-443: "run only by an unbound coordinator; a bound worker is refused"; D06's two sentences at lines 70 and 245; D08's `core/CLAUDE.md:58` edit and its test lines in the same PR. The consistent rule set after the revert: only the owner consents, in chat; an unbound coordinator or the session the owner is talking to records that consent; a bound worker can never run `record-*`, `adopt-*` or `release-worker` (guard rule 1 returns); guard rule 2 (a bound worker sends and asks with no `--to`) stays; an issue write needs one of the four standing grants (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold`) or a per-action chat go. Pass check: `tests/skills/test_worker_contract.py` pins the new sentences and finds no "still written by the owner"; the rule-1 tamper tests in `tests/hooks/test_launch_level_guard_worker.py` pass; `make verify-sync`; closeout is named in the test list. Note (INV-019): planb edits the same text (contract hunks at line 245, line 298 plus a new "only under that issue's grant row" bullet, the guard TAMPER lines near 445-455, and the guard version 1 to 2), and planb's grant-row wording contradicts "standing grant or recorded chat go"; the owner answers Q4 knowing this.
- **L2.5. Design amendment PR (new).** Carries the nine rows not fixed in L2.2 (for example 1095, 1381, DQ7, ADD1, names, M1 text at lines 229 and 536), per D03, D06, D08 and D10. Needs: L2.2 merged; the owner's chat rulings on D01 to D13; owner review. Condition (INV-027): no builder starts PR B (the unbuilt orchestrator skill) or PR E (the unbuilt live test) before this PR merges. Pass check: no statement in `docs/designs/orchestrator.md` says the plan-approval gate is retired or deleted unless the owner has ruled so.
- **L2.6. planb: commit, push as a draft, rebase onto post-revert master, land first.** Needs: Q4 yes; L2.2 merged (planb's 13-file tracked patch passes `git apply --check` on the revert tree and fails on current master for all 13 files, D03); lane 1 landed or the owner accepts its cost (INV-020: planb touches 7 files of PR 693 and 5 of PR 690, for example `refs/claim.md` and `orca_worktree.py`, and C1 edits `refs/claim.md` a third time). Before rebasing (INV-002, MEDIUM): commit planb; do not resume the half-finished `/sc:implement` ledger `.dev/implement/apply-owner-decision-r36-223ffc4c/progress.md` across the rebase, because its recorded start shas are tree objects pinned in the shared `.git`, a retry revert (`~/.claude/skills/sc-implement-protocol/refs/retry.md:199`) computes from a fresh snapshot and restores toward the old start, and `.dev/implement/` is untracked so a pushed draft does not carry it. Slow-planb trigger (replaces a date): if L2.2 has merged and planb is still unpushed, the owner chooses then between waiting and reversing the order; the reversal price is 23 overlapping files with PR 686, 7 of them source, not "225 entries". Pass check: `git ls-remote origin ironbelly/issue-watcher-zero-setup-plan` prints a ref (it is empty today); after the rebase `uv run superclaude --help` exits 0 and CI is green. Inside planb: R33 (the closed ship gate) is built before R18 (default-on config) (D03).
- **L2.7. Glossary and names note (D08, D13).** Both verdicts say it comes first; it needs nothing. It must exist before any edit of PR 686. Pass check: the note lists the D08 names ("coordinator" for the session, `COORD-RepoName` tag, renamed wake schema, mailbox kind, tier key, state folder, typed line and golden fixture) and the three-name glossary; a grep of the adapted PR 686 persisted names for "orchestrator" finds none outside the test allowlist.
- **L2.8. Adapted PR 686, in place, as a draft.** Needs: L1.2, L2.2, L2.6, L2.7, Q2, Q4, and every check in section 5. The adapted diff drops the deletions of D01's must-keep symbols, `repos.py` (it parses the registry file D07 removes and collides by name with planb's `repos.py`), the registry and `hold.py`'s label writer. It keeps and renames the wake envelope and acknowledgment code (D08 names, no titles per D10, M1 Rule B and M2 fixed), the plan-check skip and `held_backlog` idea, and the `launch.py` wake-line builder. Pass check: section 5 list passes; the diff removes none of the D01 names; CI green.
- **L2.9. Per-host precheck, then install (INV-018, HIGH; INV-003, INV-017, INV-028).** `superclaude install` on a host is not "just refresh the guard": since PR 633 the install, update and `update.sh` end with a retire step that removes commands and skills that 6.0.0 no longer ships when their sha256 matches v5.0.0. This host still has `task`, `task-builder`, `prd`, `tdd`, `roadmap`, `readme` and `tech-reference` in `~/.claude/skills`, so a blanket install would carry out the removals of PRs 650, 656 and 632 on the owner's host. So: for each host, diff the installed `~/.claude/hooks/launch-level-guard.sh` and `~/.claude/WORKER-CONTRACT.md` against the repo first; this host's guard already carries rule 1 (line 444) and differs from the pre-682 file by 4 lines and from master by 11, so for this host an install adds nothing for the guard; run no blanket install until the owner has confirmed the eight removal PRs. Until the revert merges no host should install from `master`, because master's source guard has no rule 1. Needs: L2.2 merged; L2.4 merged for the contract; NB-1 answered for any host that would run the retire step. Pass check: the diff is empty for the guard and the contract, or the owner states which hosts get which install. Limit (INV-003): both guard versions carry `version: 1` (`GUARD_VERSION_LINE`, master `orca_worktree.py:839`), so the claim preflight cannot tell them apart and the check stays a manual diff until the stamp is raised (owner row R33); planb raises it to 2, so every host needs a second install after planb lands. UNVERIFIED: how Coder's template updates reach hosts, and which other hosts exist.

### Lane 3 (verdict actions that do not need PR 686)

Lane 3 holds the verdict actions that no consensus step carried (INV list, RCL section 3 item 6). The full list, each marked "after" something or "independent", is in section 8. The items with outward effect, such as the D05 server-side rule, are tied to H0.

### Where each invariant is handled

| INV | Severity | Handled in |
|---|---|---|
| INV-006, INV-026 | HIGH | H0 (hold on PR 686 and PR 690; ruleset recommendation); the "red CI blocks a merge" rule in the preface of section 3 |
| INV-018 | HIGH | L2.9 (per-host precheck; no blanket install until the eight removal PRs are confirmed; this blocks only the host install step) |
| INV-027 | HIGH | L2.2 (same-PR correction of three statements), L2.3 (banner), L2.5 (design amendment; no PR B or PR E before it) |
| INV-005 | MEDIUM | L2.1 (dry run bound to a head sha, repeated if master moves, clean git checkout) |
| INV-002 | MEDIUM | L2.6 (commit planb before rebasing; do not resume the `/sc:implement` ledger) |
| INV-003, INV-017, INV-028 | MEDIUM | L2.9 and the Unresolved list (stamp is 1 in both guards; manual diff; WC-17 has no executor until a coordinator skill exists) |
| INV-007 | MEDIUM | Section 5, check 3 (names derived from imports) |
| INV-008, INV-009 | MEDIUM | H0 limits; the "go" definition in section 1 (a quote with date in the owner's chat) |
| INV-019, INV-020 | MEDIUM | L2.4 and L2.6, and Q4 (the owner answers the planb order knowing both costs) |
| INV-004 | LOW, addressed | Section 5, check 5 (the test names the global `enabled` flag) |

### Figures corrected in this merge

- planb status entries: the rebuttals said 225; the probe re-count today is 348 (146 under `.dev/tasks`, 81 under `.dev/implement`, 48 under `.dev/reflect`); code, tests, docs and plugins are 69 (INV-010). The order does not change, because CLAY's rebuttal already priced the cost at the overlap, not the entries.
- planb overlap with PR 686: CLAY said 22 files; the probe re-count is 23, the same 7 source files (INV-011).
- PR 693 and PR 690 shared files: the task text said three text files; the shared set is four (two protocol text files and two test files; INV-016, ROU R-1). `refs/claim.md` is in PR 693 only.
- "29 test modules fail collection": this is fallout from the CLI import crash (D03 INV-001), not a file list; the pre-682 `tests/issue_pipeline` has 10 test modules plus `tests/cli/test_issue_pipeline_registered.py` (INV-012). Gate on `superclaude --help` exit 0, not on a count.
- "No deleted names" check: the 10-name list is replaced by the import-derived set in section 5 (INV-007).

## 5. Merge checks (mechanical)

<!-- Source: Variant 2 (ADV/rounds/round2-rebuttal-CLAY.md round 1 X-001 invariant checks i to iv, section 2 R-2 and R-4) merged with the base (ADV/rounds/round2-rebuttal-OURS.md section 4 row for PR 686 and R-4 Rule B); the import-derived names check is modified per ADV/invariant-probe.md INV-007 and INV-004 -->

The list below is the exact set for any PR that touches `src/superclaude/cli/issue_watch/` or restores `issue_pipeline`. All seven must pass on the head that is to be merged. Each is a command or a test the PR author runs and attaches; red CI on any of them blocks the merge (INV-006: this holds only if someone obeys the result, because `master` is unprotected).

1. `uv run superclaude --help` exits 0. This is the check that catches the revert-plus-686 break; gate on it, not on a count of failing modules (INV-012).
2. Import of every package under `src/superclaude/cli/` succeeds.
3. The import-derived names check. Derive the list of names from the imports of the restored `issue_pipeline` package and its tests: 35 names are imported from `issue_watch`; 0 are missing on master and 9 are missing on the PR 686 head (`validate_approvers`, `EVENTS_JQ`, `_argv_rest_page`, `argv_edits`, `edits`, `events`, `CommentEdit`, `EditEvidence`, `LabelEvent`; INV-007). Because `gh.edits` and `gh.events` are attribute accesses, an import test alone misses them, so the check also resolves attribute access on the `github` module. Add the D01 must-keep symbols as a test that they exist (`approval_of`, `unchanged_since`, `project_check`, `marker_in_window`, `eligibility_order`; D01 MR-2 for `marker_in_window`). The earlier 10-name list omitted `EVENTS_JQ`, `argv_edits`, `github.edits` and `github.events` and listed 5 names the package never imports, so it is replaced.
4. A test that removing the approval between wake and start refuses (D01 MR-1). The start-time re-check covers the approval, `unchanged_since`, the Status allow-list, `plan_check` and `hold:backlog`.
5. A test that `enabled` absent means off. It must name the global flag: master `cycle.py:228` reads `raw.get("enabled", False)`; planb `dispatch.py:419` skips unless `enabled is True`; PR 686's per-repo `repos.py:326` makes `enabled` mandatory (an error when absent) and `cycle.py:640` lets a dry run past `not_enabled`, so a test on the per-repo key alone would not pin the default (INV-004). A non-boolean value is an error (`cycle.py:229-230`).
6. The Rule B test. Reader side of M1: `_ack_step` accepts a `taken` item only when its state file exists; otherwise the entry stays `woken`, the ack file stays, and a decision line records `ack_without_state`. Test: an ack lists X, no state file exists, run the cycle, X stays `woken`. Add CLAY's second test: run cycles past the lease; X is resent, then abandoned with exit 7 after `MAX_WAKE_ATTEMPTS`, and is never counted done; assert exactly one delivery (UNVERIFIED whether a resend with the ack file still present delivers the same wake id twice).
7. `make verify-sync`.

Also required for the adapted PR 686 only (from the verdicts, not part of the seven): the M2 fix with its test (an abandoned wake is re-woken, and a new coordinator does not reject it as `wrong_target`; `cycle.py:994`, `route.py:407-413`); a screen-tail check and an unknown-is-not-none session lookup so a blind lookup does not start a duplicate (`wake.py:609-621`); one shared terminal helper with a parity test (D10); R33 built before R18 before any config that sets `enabled: true`; the 24-hour dry-run shadow run (D09) and D02's cron tests before the poll is ever enabled.

Also required for the revert PR only: the dry-run record of step L2.1, the "no `--to`" bullet and its assertions, and the same-PR correction of the three gate-retired design statements. The revert PR is not safe to merge if the record is not attached, if `make verify-sync` fails, if the bullet and its assertions are missing, or if it merges on red CI (RCL section 3 item 3).

## 6. Owner questions, in order

<!-- Source: Variant 2 / ADV/rounds/round2-rebuttal-OURS.md section 6 corrected by ADV/rounds/round2-rebuttal-CLAY.md section 4 (refactor-plan change 5); Q3 widened to the hold and ruleset per ADV/invariant-probe.md INV-006 and INV-026; Q4 widened per INV-020 -->

Minimum set. Only questions that block a step are blocking. Each answer is given in the owner's chat and recorded by the agent.

**Q1. Do both approval gates stay: the start approval, and the plan approval after the claim (WC-17)?** Blocks L2.2, L2.4, L2.8.
- Yes, both: the revert PR (L2.2) is prepared from the dry-run record, and the adapted PR 686 keeps the approval code.
- Only the start gate: PR 682 stands under D03 item 7, the revert is dropped, and the PR 686 and contract rows flip.
- Neither: PR 686 keeps its deletions and the D01 rows reverse; the restored-package rows fall away.

**Q2. Who adapts PR 690 and PR 686: Clay on his own branches, or a session you supervise on new branches with `Co-Authored-By`?** Blocks L1.2 (if not Clay) and L2.8.
- Clay: the change list is handed to Clay and the plan asks that nobody else pushes to his branches (a request only; INV-008).
- A supervised session: it works on new branches; Clay's PRs are linked and closed after those merge, with credit to Clay.
- Undecided: both steps wait; lane 1 steps that need no adaptation (L1.1) still run.

**Q3. May the hold (H0) go ahead: ask Clay in chat to make PR 686 and PR 690 drafts and not merge until you say, and do you want a ruleset on `master` that requires a review by someone other than the author?** Blocks H0. A step that lists H0 may still proceed after a "No to both" answer, with the risk stated below.
- Yes to both: H0 is done as a chat request plus an owner admin change; the hold stops being only a promise.
- Hold only, no ruleset: the request is made, but any collaborator with write access can still merge (INV-006); the plan then relies on the dry-run rechecks and on obeying red CI.
- No to both: the plan accepts that one merge click falsifies it; the owner is told this in the answer line.

**Q4. Does planb land before the adapted PR 686, will you push planb as a draft branch now, and are you willing to take the file-overlap cost with the lane 1 and amendment PRs?** Blocks L2.6 and L2.8.
- Yes to all: Clay has a real target and L2.8 follows planb. Cost stated: planb edits the same lines as the amendment PR (INV-019) and touches 7 files of PR 693 and 5 of PR 690 (INV-020); resolved once, by whoever lands second.
- Pushed, but the order reversed (adapted PR 686 first, planb rebases onto it): possible with a known price of 23 overlapping files, 7 of them source; the plan advises against it.
- Not pushed: L2.8 waits as a draft; planb stays on one disk (base `e3e9d636a`, 57 commits behind `origin/master`); if the revert has merged and planb is still unpushed, you choose then between waiting and reversing the order.

Non-blocking:

**NB-1. Do you confirm the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656)?** Blocks only the host install step L2.9.
- Confirm all: L2.9 may run per host after the precheck.
- Confirm some or none: this plan does not revert them; reversing any is a separate owner decision outside this plan, and L2.9 stays blocked.

**NB-2. Do you answer Clay's 2026-11-18 comment on issue 450?** Blocks nothing.
- Yes: the answer is recorded and the owner or the assignee posts it; agents post nothing.
- No: issue 450 stays open with the comment unanswered.

Recorded as answered, pending your Q01 confirmation: the earlier Q5 (are grant rows and approval rows given by the owner in chat and recorded by the agent, never hand-written) is answered by the owner's order of 2026-11-17 (memory "Approvals through chat, never files"). L2.4 applies it. If you say no, the owner-written-file wording stays and D04 and Q01 reopen.

## 7. Cross-verdict tensions and how each is settled

<!-- Source: Variant 2 / ADV/rounds/round1-advocate-OURS.md (T1 to T4) and ADV/rounds/round2-rebuttal-OURS.md R-2, R-4, R-5, extended by ADV/rounds/round2-rebuttal-CLAY.md section 3 item 6 and ADV/invariant-probe.md INV-022, INV-023 (refactor-plan change 6) -->

| Tension | Settlement | Where it lands |
|---|---|---|
| D03 vs D05: D03's revert restores guard rule 1; D05 says keep PR 682's guard edit (rule 1 removed, rule 2 kept) | D05's "keep" is void once the revert merges; D05 itself says rule 1 must return if a coordinator-side approval verb returns, and the revert returns them. Reword D05's row to "rule 2 stays, rule 1 returns with the revert; K12 and the staging probe are untouched". Rule 1 applies only to governed (bound) sessions, so an unbound coordinator is untouched (RCL R-5 evidence) | L2.2, L2.4 |
| D03 vs D04: D03's revert restores the grant-row line 300; D04 says the per-issue grant row "cannot be restored" because PR 682 removed it | The premise is gone once the revert merges. Reword lines 57, 298 and 300 so the row is given by the owner in chat and recorded by the agent; the four standing grants stay (D04) | L2.4 |
| D01 vs D03: D01 decides the start approval; D03's revert is about the plan approval after the claim (WC-17); they are two different gates | Q1 asks both; D01 does not by itself decide PR 682 (D01 action row) | Q1, L2.2 |
| D07 vs D04, D06 and D11: PR 686's `repos.py` parses the registry file D07 removes, and it collides by name with planb's untracked `repos.py` (which lists Orca repositories, R15) | The file cannot land; its ideas survive: D06's `reviewers` and merge keys (`repos.py:47-84`), D04's four standing `grants`, D11's `reach_daily_max` default 0, carried into planb's project-local config. UNVERIFIED which planb file will hold them (planb has `defaults.py` and `generate.py`) | L2.8 |
| D09 vs PR 686: the label writer (`hold.py`, `LabelWriter` in `github.py`) contradicts NG-2 ("the poll writes nothing to GitHub") | Left out of the adapted PR 686; the owner may overrule at L2.8 (D09 "ship dormant" option; open owner call) | L2.8 |
| D12 vs D13 vs PR 693: three PRs touch the same `/sc:issue` files; PR 683 refers to `/sc:issue --plan`, which exists only after PR 690 | Order: PR 693, PR 690, then rule C1 | L1.1 to L1.3 |
| D06 amendments to `WORKER-CONTRACT.md` lines 70 and 245 are not in the base paper's list (lines 57, 298, 300) | Added to the amendment PR after the owner's chat approval of R25, R17 and R9; D08's `core/CLAUDE.md:58` edit goes in the same PR | L2.4 |
| D08 renames vs PR 686: wake schemas, mailbox kind, tier key, state folder, typed line and golden fixture carry "orchestrator" | Rename before any 686 edit: D08 says "must land before any merge of it"; the names are pinned by `orchestrator_wake_golden.json` and `test_wake.py`, so they are cheapest to change before merge | L2.7, L2.8 |
| D10 M1 (acknowledgment can precede the state file; `cycle.py:777-810`) and M2 (an abandoned wake is never re-woken; `cycle.py:994`) | Two rules: Rule A on the writer (a requirement on the unbuilt coordinator skill, PR B, and design lines 229 and 536 next to 539; state file first, then the acknowledgment; "take" is idempotent) and Rule B on the reader (code in the adapted 686, testable today); the M2 fix is code in the adapted 686 | L2.5, L2.8, section 5 check 6 |
| D08 rename vs D01 restore (checked, no clash): "orchestrator" count in the restored contract, guard and `issue_pipeline` is 0 | No tension (INV-022) | none |
| Restored `issue_pipeline` verbs vs PR 686's `record.py` schema 2 (checked, no collision found) | `approval_record.py:32` imports `FileStore`, `LockError`, `LockHeld`, which PR 686's `record.py` still has; approval rows live in a separate directory (INV-023) | none |

## 8. Verdict actions placed in lane 3

<!-- Source: Variant 2 / ADV/rounds/round2-rebuttal-CLAY.md section 3 item 6 and section 4 (lane 3), completed from the Actions tables of the verdicts D01 to D13 and the "Verdict ACTIONs that no consensus step carries" list in ADV/invariant-probe.md (refactor-plan change 7) -->

These are actions the verdicts name that neither side's ordered list placed. Each is a recommendation. "After" names what must come first; "independent" means it does not wait for PR 686 or the revert.

| Verdict action | After | Independent |
|---|---|---|
| D11: write the contract note for the three readers (sweep, observer, report), naming `session_id` as the join key (`docs/designs/observe-sweep-contract.md`) | nothing | yes |
| D11: add `session_id` and `worktree_path` to the sweep JSON v1 row with the reviewed golden-test edit | the contract note | yes |
| D11 (HIGH report rules, INV list): read previous not-done sessions; keep the old terminal map until a live side-by-side run | the `session_id` field and the side-by-side run | yes |
| D11: owner rulings on the cap value, observer entry text, questions panel and where the sweep JSON lives | nothing; before the matching code | yes |
| D05: merge PR 685 (the issue 442 runbook and results) | the owner's own go | yes |
| D05: decide when binding starts; staging probe on a throwaway issue; close issue 442's pending rows (protected push, `/sc:pr-submit --monitor 3` at FS) | the binding-start decision; before any real orchestrated issue | yes |
| D05: server-side rule on `master` and `integration` (the only control that closes K12; INV-019 and INV-037 of D05) | the owner's go; the same recommendation as H0 | yes |
| D05: decide the L2 position (install it for `worker-start` worktrees or not) | the staging probe | yes |
| D05 and D06 in PR B: marker line and preflight in `cmd_pending`; `refuse(argv)`, head-pinned merge, audit AU1 to AU8 | the design amendment PR (L2.5) | yes of PR 686; no of L2.5 |
| D10: live spike U5 (mailbox from outside a Run, `tui-idle` meaning, `orca agent launch` carrying the ccsession tag and prompt) | nothing; before the poll is ever enabled | yes |
| D10: post the drafted narrowing of Coder issue 477 (the owner's own post) | the owner's own grant | yes |
| D10: decide whether a typed wake line into an idle session is acceptable | before the adapted PR 686 is merged | no (gates L2.8) |
| D02: change the six-field cron line to five fields in `docs/designs/issue-watcher-setup.md` (section 8.7 and FU-2) | nothing | yes |
| D02: correct the Coder issue 515 wording ("not a fit for a plain command") | the owner accepts the verdict; the owner posts it | yes |
| D02: decide the poll command contract (`once` plus `repos.yaml`, or `run-all` plus per-repo configs) | settled with D07 and D01; before any scheduler text is final | yes |
| D02: rotate the local Orca auth token that a debate subagent printed into its own transcript | nothing; soon; host, owner only | yes |
| D07: rewrite design sections 4.4, 5.7 and 6.2 to the project-local layout | the owner accepts the verdict; goes in L2.5 | yes |
| D07: in-flight cap in the child cycle with a closing writer and expiry; guarded restart; `owner/name` keys and the `name_collision` skip | on planb; after the closing-writer decision | yes |
| D07: Coder issues 515 and 516 land first | before any dispatcher serves a repo | yes |
| D08: glossary and "orchestrator" to "coordinator" edits (`core/CLAUDE.md:58`, `ccsession-tag/README.md:423`, `tests/core/test_orca_session_launch_guidance.py` lines 33 and 53) | glossary first (L2.7); the edits go with the amendment PR (L2.4) | partly |
| D08: fix `agent-work-report/SKILL.md:12`; check the `COORD-RepoName` tag against ccsession | with the PR 684 follow-up; before the launcher is built | yes |
| D13: owner's chat approval of the cleanup design; ruling on local `git branch -d`; issue 339 stays open as umbrella | before any build of issue 687 | yes |
| D13: the closeout wave 8 call depends on a grant row | the verdict on merge and close authority; the amendment PR (L2.4) | yes |
| D12: manual-claim warning that prints `/sc:issue --plan` with the issue number | with C1 (L1.3) | yes of PR 686; needs L1.3 |
| D06: ask the owner for the open items (go expiry number, `changes_requested` hard refusal, 60-minute default, nine-row list) and approval of R25, R17, R9 | the first owner session; before any contract edit | yes |
| D04: put the grants file out of the orchestrator's write reach; parameterise the owner identity in `answer-check`; rule on R10 | before PR B is built; the R10 ruling before `pr.merge` or `issue.close` can be standing | yes |
| D09: decide whether the dormant label-write code ships; amend NG-2 only if it is enabled | before the adapted PR 686 merges | no (gates L2.8) |
| D03: build R33 (closed ship gate) before R18 (default-on config) | on planb; before the watcher is enabled | no (part of L2.6) |
| D01: start-time re-check (MR-1, MR-2) and the `plan_incomplete` and `held_backlog` skip reasons on planb; mark the trigger sentence of R1 (lines 73, 111, 488) superseded | after the running `/sc:implement` plan finishes; after the owner confirms R19 | no (part of L2.6 and L2.5) |

## 9. What each side got right, and which Clay pieces are adopted

<!-- Source: Base modified (the base "What it gets right" list was widened to both sides and cut to three points each; sources: ADV/rounds/round1-advocate-OURS.md strengths, ADV/rounds/round1-advocate-CLAY.md strengths and concessions, ADV/rounds/round2-rebuttal-OURS.md and round2-rebuttal-CLAY.md section 1, ADV/debate-transcript.md; adopted-pieces list from base variant-1-original.md "What it gets right" first bullet plus CLAY round 1 strength 8) -->

### OURS (the owner's line)

1. The owner's rules decide every contested rule: all thirteen verdicts are HYBRID with the owner's rule as base, and PR 686 implements the opposite on at least seven of them (it removes the approval, trigger and Project code, adds a registry, a label writer, "orchestrator" wake names and a copied terminal helper). Merge-and-fix-forward would re-add what it deleted. Sources: round 1 OURS strength 1; D01 "Our strengths that must be kept"; `gh pr view 686` file stats (`predicates.py` +114/-207, `github.py` +535/-426, `cycle.py` +1478/-652).
2. The order is forced by facts, not taste: the revert plus PR 686 is clean in git and crashes `superclaude --help` at import (D03 INV-001); the names are cheapest to change before merge (D08 action "must land before any merge of it"); planb's 13-file tracked patch applies only to the revert tree (D03).
3. The process facts: PR 682 merged 66 minutes after opening with a bot review only; no review or comment by `ironbelly` exists on PRs 681 to 684, 686 or 690; `master` is unprotected (`protected: false`, 2026-11-20). A notice on issue 450 is not consent (X-004). Sources: D03 strongest points OURS 1 and 3; inventory 2A notes; round 1 CLAY concession 4.

OURS gave up three weak parts of its own paper: "close the original" (no verdict says CLOSE), the strict serial order, and missing start conditions (round 2 OURS section 1).

### CLAY (Clay's line)

1. Independent work should not wait behind the hardest item: PR 690 and PR 693 share no code with the revert or PR 686 (only `CHANGELOG.md`, and four shared text and test files between 693 and 690), so they go in lane 1. Sources: round 1 CLAY strengths 1 to 3; round 2 OURS R-1 conceded.
2. No verdict says CLOSE for PR 686: nine verdict rows say KEEP-ADAPT, and almost no piece of it runs alone (10 of 13 `predicates` names it needs are missing on master). So adapt in place, keeping the review history (64 Clay comments, 27 Augment, 24 Codex reviews) and the 3,182 new test lines on `hold`, `wake`, `route` and `repos` as reusable evidence. Sources: round 1 CLAY strengths 4 and 5; round 2 OURS R-2.
3. The things both sides missed: the eight "confirm approval" removal PRs, the install step as a hidden prerequisite, mechanical checks in place of decisions (restored tests as the canary, a clean git checkout for the dry run, a head-bound trial), and the verdict actions no step carried. Source: round 2 CLAY section 3 (the install point is raised to HIGH by INV-018).

### Clay pieces adopted (all separable benefits)

- From PR 690: `plan_body.py check` as the single plan check, imported by the adapted `hold.py` (D12); `/sc:issue --plan` and `--remaining` after the four fixes.
- From PR 686: the wake envelope and acknowledgment code, renamed (D10, D08); `plan_check` and `hold:backlog` as read-only skip reasons (D01); the merge-gate keys `reviewers` and `merge_method` and the four standing `grants` (D06, D04); the in-flight cap and guarded restart as ideas carried into planb (D07); the `launch.py` wake-line builder; the reach cap key with default 0 (D11).
- Merged work kept: PR 683 `/sc:closeout` (D13), PR 684 report layer (D11), PR 681 sequencing and risk register as amended text.
- Not adopted: the registry and the orchestrator repo (D07), the label writer (D09, NG-2), the deletions of D01's must-keep symbols, "orchestrator" as the session name (D08), the copied terminal code (D10), autonomous merge (D06), and issue 655's "replaces #450".

## 10. Changes not made (rejected alternatives)

<!-- Source: Variant 2 and base (refactor-plan "Changes NOT being made" list; reasons from ADV/rounds/round2-rebuttal-OURS.md R-1 to R-3, ADV/rounds/round2-rebuttal-CLAY.md section 2, ADV/rounds/round1-advocate-CLAY.md concessions, ADV/invariant-probe.md) -->

| Alternative | Origin | Why it is not recommended |
|---|---|---|
| Merge PR 686 as it stands and fix forward | CLAY opening claim | It deletes 14 `predicates.py` symbols and about 30 `github.py` symbols that D01 keeps and gives a crashing CLI with the revert (D03 INV-001); fix-forward means re-adding deleted code. CLAY withdrew it in round 1 |
| Keep PR 682 and do not revert | CLAY opening claim | The deletion is merged owner work (PRs 584 and 591) with no recorded owner review, and planb depends on it. CLAY withdrew it in round 1. It stands only if the owner answers Q1 "only the start gate" (D03 item 7 conditions) |
| Split PR 686 into pieces and close the original after re-filing | OURS opening claim | No PR 686 module runs on post-revert master by itself (10 of 13 `predicates` names missing; `hold.py` needs the schema-2 `record.py`; `route.py` needs `record.StoreDoc` and `repos`; `wake.py` needs `launch.build_wake_line`); no verdict says CLOSE; a split loses review history and needs someone to re-file (ROU R-2). A split stays acceptable only if the owner prefers it; a tie goes to the owner's line |
| Serial order with the revert first | OURS opening claim | PR 690 and PR 693 share no code with the revert or PR 686 (only `CHANGELOG.md`), so they go in lane 1 (ROU R-1) |
| Close issue 450 into issue 655 ("replaces #450") | CLAY opening claim | Issue 450's live test, shadow run and cron remain required under every verdict (D01, D02); issue 655 is rescoped instead |
| Revert PR 681 (the design doc) | considered in the plan | Docs only and it holds the sequencing and the risk register; amend instead (banner now, same-PR correction of three statements, later amendment PR) |
| A banner on PR 681 alone | OURS round 2 row for PR 681 | Not enough: the doc orders the deletion of a gate the repo would have again after the revert (INV-027) |
| A date after which the planb order is reconsidered | OURS R-3 | Replaced by a mechanical trigger (planb pushed as a draft; revert merged and planb still unpushed) with a priced exit of 23 overlapping files (RCL R-3) |
| A blanket `superclaude install` on every host after the revert | OURS round 2 step 11 and CLAY round 1 step 3 | Would run the PR 633 retire step and carry out removals 632, 650 and 656 on the owner's host before they are confirmed (INV-018) |
| The 10-name "no deleted names" list | CLAY round 2 R-2 | Replaced by the import-derived set of 35 names plus attribute access (INV-007) |
| Reverting the eight "confirm approval" removal PRs | not proposed by either side | They shipped in 6.0.0 and 6.1.0 and the revert does not depend on them (RCL section 3 item 1); they get one non-blocking question |

## 11. Unresolved, Unverified, Confidence

<!-- Source: Variant 2 and base (refactor-plan change 9): "Still unresolved" from ADV/rounds/round2-rebuttal-CLAY.md, not-verified list from ADV/invariant-probe.md, Unverified items from ADV/debate-transcript.md and the base paper's risks (variant-1-original.md "What it risks"); confidence from the debate transcript scoring matrix -->

### Unresolved (owner calls, not debate points)

1. What the owner does if planb stays unpushed after the revert merges: wait, or reverse the order at the priced cost (23 overlapping files, 7 of them source). Only the owner can choose (Q4).
2. Whether a resent wake with the acknowledgment file still present delivers the same wake id twice. The Rule B test must assert one delivery.
3. The dormant label writer (D09) and the typed wake line into an idle session (D10). Both are owner calls; the default in this plan is "left out" for the label writer, and the typed line must be decided before the adapted PR 686 merges.
4. How Coder's template updates reach hosts. This decides whether the install prerequisite (L2.9) is real for each host.
5. How red CI is enforced while `master` is unprotected. The mechanical checks work only if someone obeys the result; the ruleset recommendation in H0 is the only server-side answer.
6. The revert tree's full test run. The full suite and `tests/hooks/test_launch_level_guard.py` did not finish in D03; step L2.1 produces the record.
7. After L2.4, contract, guard and hosts agree only on paper (INV-028): the contract and guard are fixed in the repo, each host is stale until a per-host install (INV-003, INV-017, INV-018), "grant row" is prose only (no code reads it), and no coordinator skill or `commands/coordinator` exists on master, so WC-17 has no executor. Protection holds by the owner's vigilance until one exists.

### Unverified

- The merge-only trial of PR 690 onto master plus PR 693 has not been run (RCL R-1).
- Whether other hosts exist and what they have installed; PR 686 merge behaviour beyond D03's recorded result (INV not-verified list).
- Which planb file will hold the surviving ideas from PR 686's `repos.py`.
- The "ruling of 2026-11-20" quoted in issue 689 (D12).
- Whether the process was independent: the two position papers were written by the session that ran the debate, and the advocates and evaluators are same-family agents; the evaluators saw the final debate state when scoring the opening papers (debate-transcript process notes). The per-criterion disagreement log between the two evaluator passes was not itemised.
- Verdict confidences the plan leans on are 62 to 85 percent; D02 (cron) is the thinnest at 62.
- Not an owner decision: every disposition and every owner answer above. None is made until the owner gives it in chat.

### Confidence

Debate status: 21 of 21 diff-point positions agreed after round 2 (threshold 80 percent); the invariant gate is BLOCKED_BY_INVARIANTS because 4 HIGH invariants (INV-006, INV-018, INV-026, INV-027) were unaddressed, so the debate result is partial. This merge converts those four into conditions (H0, L2.9, L2.2 with L2.5), so the document is complete as a plan, but the conditions are not yet true.

Confidence in the disposition set: about 80 percent (an estimate from the scoring matrix, whose per-point confidences run 75 to 90 percent; not a measurement). The set holds under the owner weighting rule and under both sides' final tables. What would change it:

- Lower, to about 50 percent: the owner answers Q1 "only the start gate" (D03 puts confidence near 50 percent for the revert then), or the dry run in L2.1 fails.
- Lower: the owner declines the hold (Q3), because one merge click then falsifies the plan (INV-026).
- Higher, to about 90 percent: the dry-run record exists and passes, planb is pushed as a draft, and the hold and ruleset are in place.

