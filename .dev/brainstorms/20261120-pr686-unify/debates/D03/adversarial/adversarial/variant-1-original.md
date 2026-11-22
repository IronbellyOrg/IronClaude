# Position paper OURS (D03): revert PR 682 and restore the issue-pipeline gate

Topic: PR 682 (Clay, merged 2026-11-20 00:02 UTC) deleted `src/superclaude/cli/issue_pipeline/`, WC-17 and "Issue pipeline duties" in WORKER-CONTRACT.md, and guard G2 rule 1.

## Claim

Revert PR 682 (commit `01e7a9e23`) as one new PR on top of master, so the plan-approval package, WC-17, "Issue pipeline duties" and guard G2 rule 1 come back. The deletion removed merged, tested, live-measured work of the repository owner (`ironbelly`) three days after it merged, to make room for a design the owner never ruled on, and it left nothing in its place. Restoring is cheap; losing the protections is not.

## Mechanism

1. `git revert 01e7a9e23` as a new PR (a revert PR, not a force-push). The old package imports only symbols that still exist on master, because `issue_watch` is unchanged there (PR 686 is open, not merged): the old imports are `issue_watch.cycle`, `predicates` (`EditEvidence`, `LabelEvent`, `valid_issue_number`), `github`, `runner` and `record` (`FileStore`, `LockError`, `LockHeld`), read with `git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/*.py`.
2. Only 3 of the 36 files PR 682 touched changed afterwards on master (`git diff --name-only 01e7a9e23 origin/master`, origin/master 61ac2c2e6): `CHANGELOG.md`, `src/superclaude/core/WORKER-CONTRACT.md` (one line, the `/sc:closeout` entry in the never-as-worker list, PR 683) and `tests/skills/test_worker_contract.py`. The conflicts are textual and small.
3. The owner's local branch `ironbelly/issue-watcher-zero-setup-plan` (worktree `claim-handoff-planb`) then rebases onto a master that still has the package it extends.

## Cited facts

1. The code is the owner's merged work. PR 584 "Plan A" (ironbelly, merged 2026-11-17 04:00:59Z, +4355/-6) and PR 591 "Plan B" (ironbelly, merged 2026-11-17 17:28:21Z, +8786/-80); `git log` on the path shows only those two commits. Both implement owner decision 6 = "Go with B now" (`.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md` on origin/master, line 139) and Q35 "B1b", Q36, Q37 "reco approved" (lines 184-186).
2. The deletion was fast and had no human review. PR 682 opened 2026-11-19 22:56:28Z and merged 2026-11-20 00:02:36Z (66 minutes; `gh pr view 682 --repo IronbellyOrg/IronClaude`), with one review by `augmentcode` and one comment by `chatgpt-codex-connector`. Neither its body, issue 655 (Clay's plan for the orchestrator, "replaces #450") nor `docs/designs/orchestrator.md` names decision 6, route B or Q35 to Q41 (E-pr682.md line 56).
3. "Never ran live" is only half true. The handoff had a live first test on throwaway issue 452 on 2026-11-17: eleven `RECORDED:` lines (preconditions a to k) in `docs/designs/issue-pipeline-fu1.md:108-118`, including exactly one worker terminal created, the plan hash identical on both sides, `ask` resume after a timeout, and a real label event and comment read back from GitHub. What never ran is the cron watcher, which is `enabled: false`; the pipeline was built to wait behind it.
4. The old tests pin protections that no code on master has now: one winner when two callers race (`tests/issue_pipeline/test_approval_concurrency.py:60` and `:71`), a kill between `worker-start` and `adopt-mark` blocks a second start (`test_approval_crash.py:45`), a bot approval is ignored (`test_stage_predicates.py:291`), an edited approving comment does not count (`:339`), replayed evidence does not reopen a revoked row (`test_approval_record.py:336`), and the brief can hold no issue text (`test_brief.py:65`). Read with `git show 01e7a9e23^:tests/issue_pipeline/<file>`.
5. The replacement is design text only. `docs/designs/orchestrator.md:568` and `:1108-1112` promise a write-ahead `intent`/`done` log and exclusive create (PR B), but no code reads them: the PR 686 snapshot has no `worker-start` call in `src/superclaude/cli/issue_watch/` (grep, snapshot pr-a), and PR B and E do not exist (FULL-REPORT.md section 2).
6. Human approval before a worker builds is gone, not replaced. Design rule R1 (`orchestrator.md:73`): "no plan-approval gate after the claim". PR 686 `hold.py` (276 lines) only checks that three headings are filled in (E-pr682.md line 69). Clay marks "assignment is safe" as UNVERIFIED in issue 655 (E-pr682.md line 48).
7. The owner's line still depends on the deleted code. `requirements.md` rows R19, R22, R24, R29, R35 and R36 (in `claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/`) keep the approval, now the `Approved` issue field, as the gate. The branch has 53 changed files (E-pr682.md line 67), edits `brief.py`, `cli.py`, `reads.py` and five test files of the package, adds `complete.py` (424 lines) with 551 lines of tests, and edits the guard's G2 rule 1 case (`launch-level-guard.sh:445-455`, adding the coordinator-only `issue-pipeline complete` pattern), the exact case PR 682 removed.
8. Master still points at the removed duties. `src/superclaude/commands/issue.md:85`, `skills/sc-issue-protocol/SKILL.md:140` and `refs/claim.md:96` say "When a coordinator owns the issue, it runs the worktree step"; `docs/designs/issue-watcher-setup.md:170` and `issue-watcher.md:43` describe the handoff. After PR 682 no coordinator duty exists to match them.
9. The guard comment on master (`launch-level-guard.sh:496`) already says "the rule 1 text of that design is retired", so the code and `docs/designs/issue-pipeline-guard-g2.md` now disagree.

## What it costs

- About 4,600 lines return (about 1,600 source, about 2,900 tests). A small maintenance load for code with no production caller until the watcher is enabled.
- A conflict fix in three files and a re-run of the guard's independent review (the design note `issue-pipeline-guard-g2.md` requires one for any guard change).
- It blocks the "no approval gate" rule of Clay's design until the owner rules otherwise (that is topic D01, not this one).

## What it risks

- If the owner later rules for assignment-only (D01 goes to CLAY), the package is dead again and the revert was wasted work. Mitigation: the revert is a single commit that can itself be reverted.
- Keeps accepted risk L-1: one GitHub login serves the owner and the agents, so an agent could apply the approval (owner-answers.md:126). The old safeguards (plan hash, plan reply unedited, label after reply) stay.
- PR 686 and the restored package cannot both land as written: the design says PR 686 deletes the symbols the package imports (`orchestrator.md:982`).

## What it gets right (and what Clay's side gets right)

Clay's PR was careful in one respect: it kept guard rule 2, wrote a contract bullet for "no `--to`" and had an independent guard review. Those parts are worth keeping even if the package returns. The owner's line also concedes the gate is slow (two sessions and a grant row per approval, Q36 "latency approved for now").

