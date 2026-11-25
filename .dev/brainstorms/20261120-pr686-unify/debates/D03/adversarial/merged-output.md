<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS) -->
<!-- Merge date: 2026-11-20 -->
<!-- Plan: refactor-plan.md (12 changes); executor: merge-executor -->

<!-- Source: Base (original, modified) - retitled from "Position paper OURS" to the merged position; scope pointer added -->
# Unified position (D03): revert PR 682 and restore the issue-pipeline gate, under conditions

Topic: PR 682 (Clay, merged 2026-11-20 00:02 UTC) deleted `src/superclaude/cli/issue_pipeline/`, WC-17 and "Issue pipeline duties" in WORKER-CONTRACT.md, and guard G2 rule 1.

<!-- Source: Base (original, modified) - pointer to the new sections added so the Claim and the D01 condition agree (cross-reference only, no new fact; Changes 1 and 5) -->
## Claim

Revert PR 682 (commit `01e7a9e23`) as one new PR on top of master, so the plan-approval package, WC-17, "Issue pipeline duties" and guard G2 rule 1 come back. The deletion removed merged, tested, live-measured work of the repository owner (`ironbelly`) three days after it merged, to make room for a design the owner never ruled on, and it left nothing in its place. Restoring is cheap; losing the protections is not.

The revert is the default until topic D01 (whether any plan-approval gate should exist) rules. It carries one mandatory precondition (the order against PR 686) and the conditions listed in "Conditions and sequencing".

<!-- Source: Base (original, modified) - steps 1 to 3 edited and steps 4 to 6 added per Changes 1, 2, 8, 9 and 10; see the tag on each step -->
## Mechanism

<!-- Source: Base (original) for the main text; Variant 2 (CLAY), Mechanism 2 and contribution U-007 plus invariant probe INV-002 - merged per Change 2 for the sub-bullet -->
1. `git revert 01e7a9e23` as a new PR (a revert PR, not a force-push). The old package imports only symbols that still exist on master, because `issue_watch` is unchanged there (PR 686 is open, not merged): the old imports are `issue_watch.cycle`, `predicates` (`EditEvidence`, `LabelEvent`, `valid_issue_number`), `github`, `runner` and `record` (`FileStore`, `LockError`, `LockHeld`), read with `git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/*.py`.
   - Keep the "ask and send carry no `--to`" contract bullet by hand. PR 682 made that sentence a standalone bullet in the worker duties of WORKER-CONTRACT.md and asserted it in `tests/skills/test_worker_contract.py`. A bare `git revert` drops both the bullet and the assertions (lines 426-429 and 3220 of that test file), the tests still pass, and nothing signals the loss (INV-002). Both advocates agree to keep them. Re-apply them by hand after the revert. The sentence then appears twice (in WC-17 at line 59 and in the bullet); the alternative is to reword WC-17 to point at the bullet.

<!-- Source: Base (original, modified) - conflict scope corrected per Change 10 (INV-007) -->
2. Only 3 of the 36 files PR 682 touched changed afterwards on master (`git diff --name-only 01e7a9e23 origin/master`, origin/master 61ac2c2e6): `CHANGELOG.md`, `src/superclaude/core/WORKER-CONTRACT.md` (one line, the `/sc:closeout` entry in the never-as-worker list, PR 683) and `tests/skills/test_worker_contract.py`. Of the three, only `CHANGELOG.md` is a textual conflict (`git merge-tree --write-tree --merge-base=01e7a9e23 origin/master 01e7a9e23^`); `WORKER-CONTRACT.md` and `test_worker_contract.py` merge on their own. The "Removed: the old plan-approval gate" entry in `CHANGELOG.md` is dropped or reworded. The conflict is textual and small.

<!-- Source: Base (original) -->
3. The owner's local branch `ironbelly/issue-watcher-zero-setup-plan` (worktree `claim-handoff-planb`) then rebases onto a master that still has the package it extends.

<!-- Source: Refactor plan (invariant probe INV-001, HIGH; Variant 2 fact 6 on removal order) - merged per Change 1 -->
4. Sequence the revert with PR 686 (mandatory precondition). A revert of PR 682 and PR 686 (head 8e5ae29ad) merge with no git conflict beyond `CHANGELOG.md`, in either order, and git gives no warning, yet the merged tree is broken: `superclaude --help` crashes and 29 test modules fail at collection (INV-001). PR 686 must not merge before the revert is settled. The reason, the repair options and the merge condition are in "Conditions and sequencing".

<!-- Source: Refactor plan (invariant probe INV-004, INV-005) - merged per Change 8 -->
5. Refresh the installed copies after the revert lands. Hosts hold copies of the guard, the contract and the commands made by `superclaude install`. On the fault-finder's host `/home/coder/.claude/hooks/launch-level-guard.sh` matches neither the pre-682 nor the master guard, `/home/coder/.claude/WORKER-CONTRACT.md` still has WC-17 and `/usr/local/bin/superclaude` still lists `issue-pipeline` (INV-004). Hosts must run `superclaude install` to replace them. The guard version stamp (`# launch-level-guard-version: 1`, line 10; `orca_worktree.py:839,986-987` checks only that line) stays 1 in the revert: it was 1 before PR 682 and on master, so nothing mechanical tells a guard with rule 1 from a stale one, and raising it is itself a guard change that needs the independent review (INV-005). Hosts that installed between 00:02Z on 2026-11-20 and the revert have a guard without rule 1 beside restored coordinator-only verbs, so the guard's independent review is also the check for them. Risk of this step: Medium, because it touches a security hook.

<!-- Source: Refactor plan (invariant probe INV-011) - merged per Change 9 -->
6. Amend the design in the same PR. PR 681's design (`docs/designs/orchestrator.md`) is not reverted and says the opposite of the restored code: rule R1 at line 73 and lines 987-991, 997-1004, 1017, 1095 and 1381 describe the gate as retired, and PRs A, B and E build against that text (INV-011). Either this revert PR amends R1 and section 7, or a named follow-up does. The D03 verdict names which.

<!-- Source: Base (original, modified) - facts 2, 3 and 7 corrected per Changes 11 and 7; facts 1, 4, 5, 6, 8 and 9 unchanged -->
## Cited facts

<!-- Source: Base (original) -->
1. The code is the owner's merged work. PR 584 "Plan A" (ironbelly, merged 2026-11-17 04:00:59Z, +4355/-6) and PR 591 "Plan B" (ironbelly, merged 2026-11-17 17:28:21Z, +8786/-80); `git log` on the path shows only those two commits. Both implement owner decision 6 = "Go with B now" (`.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md` on origin/master, line 139) and Q35 "B1b", Q36, Q37 "reco approved" (lines 184-186).

<!-- Source: Base (original, modified) - process facts added per Change 11 (PR 681 and PR 682 timing, one automated review, issue 450 question without reply); the issue 450 detail is from Variant 2 (CLAY) fact 2 -->
2. The deletion was fast and had no human review. PR 682 opened 2026-11-19 22:56:28Z and merged 2026-11-20 00:02:36Z (66 minutes; `gh pr view 682 --repo IronbellyOrg/IronClaude`), with one review by `augmentcode` (automated) and one comment by `chatgpt-codex-connector`. PR 681 (the design) merged at 2026-11-20T00:02:33Z, 3 seconds before PR 682, and both were merged by `clayphi`. Neither PR 682's body, issue 655 (Clay's plan for the orchestrator, "replaces #450") nor `docs/designs/orchestrator.md` names decision 6, route B or Q35 to Q41 (E-pr682.md line 56). The one written question to the owner is Clay's comment on issue 450 (2026-11-18 17:00:32, addressed to `@ironbelly`, ending "What do you think?"); issue 450 shows no reply from ironbelly, and a question with no reply is not consent.

<!-- Source: Base (original, modified) - scope of "never ran live" stated per Change 7 (X-001); the record f point is from the V1 concession in the debate transcript -->
3. "Never ran live" is only half true, and its scope must be stated. The handoff had a live first test on throwaway issue 452 on 2026-11-17: eleven `RECORDED:` lines (preconditions a to k) in `docs/designs/issue-pipeline-fu1.md:108-118`, including exactly one worker terminal created, the plan hash identical on both sides, `ask` resume after a timeout, and a real label event and comment read back from GitHub. What never ran live is the cron watcher, which is `enabled: false`; the pipeline was built to wait behind it. The live record does not cover guard G2 either: record f says the G2 session-id lookup "was not attempted". So the statement that nothing ran this code holds for the cron watcher and the G2 lookup, and does not hold for the handoff steps a to k.

<!-- Source: Base (original) -->
4. The old tests pin protections that no code on master has now: one winner when two callers race (`tests/issue_pipeline/test_approval_concurrency.py:60` and `:71`), a kill between `worker-start` and `adopt-mark` blocks a second start (`test_approval_crash.py:45`), a bot approval is ignored (`test_stage_predicates.py:291`), an edited approving comment does not count (`:339`), replayed evidence does not reopen a revoked row (`test_approval_record.py:336`), and the brief can hold no issue text (`test_brief.py:65`). Read with `git show 01e7a9e23^:tests/issue_pipeline/<file>`.

<!-- Source: Base (original) -->
5. The replacement is design text only. `docs/designs/orchestrator.md:568` and `:1108-1112` promise a write-ahead `intent`/`done` log and exclusive create (PR B), but no code reads them: the PR 686 snapshot has no `worker-start` call in `src/superclaude/cli/issue_watch/` (grep, snapshot pr-a), and PR B and E do not exist (FULL-REPORT.md section 2).

<!-- Source: Base (original) -->
6. Human approval before a worker builds is gone, not replaced. Design rule R1 (`orchestrator.md:73`): "no plan-approval gate after the claim". PR 686 `hold.py` (276 lines) only checks that three headings are filled in (E-pr682.md line 69). Clay marks "assignment is safe" as UNVERIFIED in issue 655 (E-pr682.md line 48).

<!-- Source: Base (original, modified) - the "53 changed files" figure marked stale per Change 7 (INV-008); all other content unchanged -->
7. The owner's line still depends on the deleted code. `requirements.md` rows R19, R22, R24, R29, R35 and R36 (in `claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/`) keep the approval, now the `Approved` issue field, as the gate. E-pr682.md line 67 gives the branch as 53 changed files; that figure is stale: the fault-finder (INV-008) counted 223 status entries in the owner worktree, 70 of them outside `.dev/`. The branch edits `brief.py`, `cli.py`, `reads.py` and five test files of the package, adds `complete.py` (424 lines) with 551 lines of tests, and edits the guard's G2 rule 1 case (`launch-level-guard.sh:445-455`, adding the coordinator-only `issue-pipeline complete` pattern), the exact case PR 682 removed.

<!-- Source: Base (original) -->
8. Master still points at the removed duties. `src/superclaude/commands/issue.md:85`, `skills/sc-issue-protocol/SKILL.md:140` and `refs/claim.md:96` say "When a coordinator owns the issue, it runs the worktree step"; `docs/designs/issue-watcher-setup.md:170` and `issue-watcher.md:43` describe the handoff. After PR 682 no coordinator duty exists to match them.

<!-- Source: Base (original) -->
9. The guard comment on master (`launch-level-guard.sh:496`) already says "the rule 1 text of that design is retired", so the code and `docs/designs/issue-pipeline-guard-g2.md` now disagree.

<!-- Source: Base (original, modified) - figures corrected per Change 7 (X-001, INV-007, INV-008); gate-cost bullet added per Change 4 -->
## What it costs

<!-- Source: Base (original, modified) - line counts and test counts corrected per Change 7 (INV-008) -->
- 4,599 lines return: 2,969 test lines and 1,618 source lines (the package itself is 1,597 of the source lines; the debate record does not split the other 12 lines). The restored tests are 117 test functions (222 collected cases). A small maintenance load for code with no production caller until the watcher is enabled.

<!-- Source: Base (original, modified) - conflict count corrected from three files to one per Change 10 (INV-007) -->
- A conflict fix in one file (`CHANGELOG.md`) and a re-run of the guard's independent review (the design note `issue-pipeline-guard-g2.md` requires one for any guard change).

<!-- Source: Base (original) -->
- It blocks the "no approval gate" rule of Clay's design until the owner rules otherwise (that is topic D01, not this one).

<!-- Source: Variant 2 (CLAY), Cited facts 4 (Q36, decision 8) - merged per Change 4 -->
- The gate itself is slow and heavy: the person approves in a coordinator session, which needs a person-opened coordinator, a grant row per issue (decision 8, E-pr682.md line 37) and two sessions per approval (E-pr682.md line 76). The owner accepted this as Q36 "Latency approved for now, approve in coordinator" (owner-answers.md:185); "for now" keeps the point open.

<!-- Source: Base (original, modified) - pointer added in the third bullet per Change 1; L-1 follow-on bullets added per Change 4 -->
## What it risks

<!-- Source: Base (original, modified) - pointer to the D01 conditions added (cross-reference only) -->
- If the owner later rules for assignment-only (D01 goes to CLAY), the package is dead again and the revert was wasted work. Mitigation: the revert is a single commit that can itself be reverted. The conditions under which PR 682 then stands are in "Conditions and sequencing".

<!-- Source: Base (original) -->
- Keeps accepted risk L-1: one GitHub login serves the owner and the agents, so an agent could apply the approval (owner-answers.md:126). The old safeguards (plan hash, plan reply unedited, label after reply) stay.

<!-- Source: Variant 2 (CLAY), Cited facts 3 - merged per Change 4 (C-004, C-010, U-009); records e and k are from the V1 rebuttal in the debate transcript -->
  - The same-login limit is real and is not hidden. FU-1 record j (`docs/designs/issue-pipeline-fu1.md:117`) shows actor `ironbelly`, id 7361222, type `User`, so the actor-type rule (the approver must be a User) cannot tell the owner from an agent that shares the login. The gate still blocks bare, edited and plan-hash-changed approvals (records e and k), so the restored code is a partial protection, not proof against an agent on the owner's login. L-1 stays an accepted risk (owner-answers.md:126).

<!-- Source: Refactor plan (invariant probe INV-006) - merged per Change 4 -->
  - A "written ruling by ironbelly" is not a checkable gate while one login serves the person and the agents. `gh api repos/IronbellyOrg/IronClaude/collaborators` shows ironbelly as the only admin, `branches/master/protection` returns 404 (master is unprotected), and `gh api user` on the fault-finder's host returns `ironbelly`, so a GitHub comment "by ironbelly" can come from an agent (INV-006). The ruling is therefore recorded through the owner's chat and the agent records it (decision D2 text in WORKER-CONTRACT.md).

<!-- Source: Base (original, modified) - pointer to the real failure mode added per Change 1 -->
- PR 686 and the restored package cannot both land as written: the design says PR 686 deletes the symbols the package imports (`orchestrator.md:982`). Git merges the two with no conflict beyond `CHANGELOG.md`, but the result does not work (Mechanism step 4 and "Conditions and sequencing").

<!-- Source: Base (original); Variant 2 (CLAY), Mechanism 3 - merged per Change 3 for the appended paragraph -->
## What it gets right (and what Clay's side gets right)

Clay's PR was careful in one respect: it kept guard rule 2, wrote a contract bullet for "no `--to`" and had an independent guard review. Those parts are worth keeping even if the package returns. The owner's line also concedes the gate is slow (two sessions and a grant row per approval, Q36 "latency approved for now").

<!-- Source: Variant 2 (CLAY), Mechanism 3 and Cited facts 3 (`sc-issue-protocol/SKILL.md:102`, PRs 651 and 661) - merged per Change 3 (U-006, C-003) -->
Clay's side also gets one thing right that stands apart from the gate: `/sc:issue --create` now requires the `Priority`, `Fix approach` and `Test plan` sections at every depth (`src/superclaude/skills/sc-issue-protocol/SKILL.md:102`, PRs 651 and 661 merged), and the PR 686 poll holds an issue that lacks them. That check is independent of the gate, so it stays as an extra layer. It does not replace human approval: `hold.py` checks only that the headings are filled in (fact 6), and the plan at creation is the author's own.

<!-- Source: Refactor plan (Changes 1, 5 and 6; invariant probe INV-001, INV-003, INV-006; Variant 2 (CLAY) Mechanism 4 and Cited facts 7) - new section merged per Changes 1, 5 and 6 -->
## Conditions and sequencing

The revert is the default until D01 rules. The invariant probe (Round 2.5) blocked convergence on one HIGH finding, INV-001. Standard depth has no Round 3, so the debate recorded it as an acknowledged risk and the plan makes it a mandatory precondition.

<!-- Source: Refactor plan (invariant probe INV-001) - merged per Change 1 -->
### Precondition: order against PR 686 (INV-001, HIGH)

- The problem. The restored package imports `issue_watch` symbols that PR 686 (head 8e5ae29ad) deletes: `EditEvidence`, `LabelEvent`, `CommentEdit`, `_argv_rest_page`, `github.edits`, `github.events` and `cycle.validate_approvers`. The orchestrator re-checked five of these by search (`EditEvidence`, `LabelEvent`, `CommentEdit`, `_argv_rest_page`, `validate_approvers`: no hit in the PR 686 snapshot). `main.py` of the pre-682 tree imports `issue_pipeline` at line 581, eagerly. A git merge of the revert and PR 686 reports no conflict beyond `CHANGELOG.md`, but the merged tree fails to import, `superclaude --help` crashes and 29 test modules fail at collection. Git gives no warning in either merge order.
- Rule 1. PR 686 must not merge before the revert is settled.
- Rule 2. If the revert lands first, PR 686 needs a revision that leaves those symbols in place, or a shim.
- Rule 3. A check that runs `superclaude --help` and imports the package is a merge condition.
- Which order is chosen belongs to topic D14, not this one.

<!-- Source: Variant 2 (CLAY), Mechanism 4, Cited facts 7 and design lines 978-1004 and 1108-1112 - merged per Change 5 (U-005, U-008); condition 2 reworded per Change 6 (INV-003); condition 3 channel per Change 4 (INV-006) -->
### If D01 ends assignment-only

PR 682 then stands, under three conditions that both advocates accepted in Round 2. The design's removal plan is the sequencing input: section 7.2 lists, file by file, what to delete (`docs/designs/orchestrator.md` lines 978-993) and 7.3 lists what guard G2 still needs (line 995 onward, to about line 1004); PR D goes first (line 1030). The three conditions:

1. PR B and its named tests exist and pass before the watcher is enabled. The bar is the set of PR B tests in the design (lines 1108-1112): a kill after each `intent` and before `done` resumes without repeating the act; exclusive create refuses a second state file; two orchestrators given one issue create one state file. The watcher's lock (`flock` on `state_dir/lock`, a second cycle exits 75; design lines 700-712) gives one winner per cycle, but not the per-issue crash-safe adoption that the old tests pinned (fact 4), so it does not stand in for these tests. Until they pass, equal double-start protection is UNVERIFIED (E-pr682.md line 68) and the replacement is design text only (fact 5).
2. R33 must be built before R18 default-on config is built. This corrects the earlier wording that R18 "stays blocked by R33 (`GOVERNED_LEVELS_ALLOWED = False`)". That constant is not built: it has no hit in src or tests on master, in the three snapshots or in the owner branch commits, and `requirements.md` row R33 says "decided (not built)" (INV-003). The only hold today is `cycle.py:228`, `raw.get("enabled", False)`, so the watcher is off by default and nothing else holds it off once R18 is built.
3. The owner gives a written ruling that names decisions 2, 3, 6 and Q35 to Q38. The ruling is given in the owner's chat and recorded by the agent, as set out under "What it risks" (INV-006).

<!-- Source: Refactor plan (Change 12; invariant probe INV-008, INV-009, INV-010, INV-013; debate transcript Rounds 1 and 2) - new section merged per Change 12 -->
## Unresolved and unverified

- UNVERIFIED: whether the restored test `test_the_watcher_record_module_is_not_edited` passes in a real checkout. It failed in the fault-finder's non-git scratch copy because it needs `git diff HEAD`; the result in a real checkout is unconfirmed (INV-009).
- Open by design: D01 decides the end state (revert stays, or PR 682 stands under the conditions above). Two diff points were split between the advocates and were settled by the orchestrator at 55% confidence: C-004 (the same-login limit) and C-008 (stale master text).
- UNVERIFIED: who "the owner" is in the design. The design calls Clay "the owner", while `owner-answers.md` records the answers of ironbelly; ironbelly is the only admin collaborator (E-pr682.md line 56). The real owner must say.
- Not checked: the untracked owner files `complete.py` and its tests against the revert tree. The tracked part of the owner's uncommitted changes (13 files, a 1,767-line patch) does pass `git apply --check` on the revert tree and fails on current master (INV-010). The owner branch figure of 53 files is stale (fact 7), and the edit list in fact 7 was not re-counted against the 223 status entries.
- Not checked: the owner branch rebase itself was not run (E-pr682.md line 67 marks it UNVERIFIED), and E-pr682.md names rows R9, R17, R24, R33 and R34 while fact 7 cites R19, R22, R24, R29, R35 and R36 (the orchestrator checked the second list).
- UNVERIFIED: behaviour of the restored approval rows against PR 686's `record.py` schema 2. The package uses only `FileStore.lock()`, `LockError`, `LockHeld` and `write_prepared_bytes`, all present in the PR 686 snapshot, and no persisted rows exist, but the behaviour against PR 686 itself cannot be confirmed while the INV-001 break stands (INV-013).
- UNVERIFIED: the full test suite and `test_launch_level_guard.py` did not finish within the fault-finder's time limit, so the revert tree has not had a complete test run.
- UNVERIFIED: Clay's claim "assignment is safe" in issue 655 (E-pr682.md line 48); the design's open question OQ6 finds two gaps.
