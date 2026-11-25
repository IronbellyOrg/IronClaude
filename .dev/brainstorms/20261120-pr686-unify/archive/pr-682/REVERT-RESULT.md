# Revert of PR 682: result

- Base sha (origin/master): 7f0919345479007ad72724dd16b4e4cf08136e65
- Branch: ironbelly/revert-pr-682
- Worktree: /home/coder/workspaces/worktrees/IronClaude/revert-pr-682
- PR: #697 https://github.com/IronbellyOrg/IronClaude/pull/697 (base master, not merged, not to be merged without the owner)
- Pre-PR checks: origin = https://github.com/IronbellyOrg/IronClaude; gh repo view = IronbellyOrg/IronClaude; branch is level with origin/master.
- Commits: a6d0889c2 (the revert, 36 files, +4612/-24). Reverted commit: 01e7a9e23.
- Conflict: only CHANGELOG.md; resolved (kept the later /sc:closeout entry; replaced PR 682's "Removed" entry with a "Restored" entry).
- No-`--to` bullet: dropped by the bare revert (bullet, test entry `messages-carry-no-to`, test `test_the_no_to_rule_sits_in_the_worker_session_duties`); re-applied by hand. No plugin copy of WORKER-CONTRACT.md exists. Nothing else gained after 682 was lost (clean apply except CHANGELOG).
- Local tests: restored issue_pipeline tests + test_issue_pipeline_registered + test_launch_level_guard_worker + test_worker_contract: 1013 passed. `uv run superclaude --help` lists issue-pipeline. `make lint` passed. `make verify-sync` failed at first only because a fresh worktree has no .claude/ copies; passed after `make sync-dev` (nothing under .claude/ staged).
- Full suite `uv run pytest -q` (23 min): 23580 passed, 44 skipped, 2 failed: tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval and ::test_ruff_passes_on_real_adapter_module ("No module named ruff" in the local venv). Pre-existing: both fail identically on a clean `git archive origin/master` export.
- Deviations: PR body passed with `gh pr create --body-file` (same as --body).

## Status 2026-11-20 ~12:50 UTC
PR #697 open, mergeable, no conflicts (Tier 0), head a6d0889c2 = local HEAD. Waiting for Augment and Codex reviews and CI.

## Status 2026-11-20 ~13:00 UTC (round 0 review done)
- CI on PR #697: all checks pass (Lint/Plugin/Sync, Doctor, Swarm imm and inv, Test on Python 3.10, Test Summary).
- Reviews on a6d0889c2: Codex (code review done, security review completed) and Augment both reviewed. 4 open threads, none fixed, none resolved:
  - Codex P1 + Augment medium (same issue), WORKER-CONTRACT.md:298, "Worktree, then worker" creates a worktree with no agent vs the "every worktree gets an agent" rule. SKIPPED: text restored unchanged from owner PRs 584/591; rewording it is an owner design decision (needs owner).
  - Augment medium, WORKER-CONTRACT.md:59 (WC-17): check-approval lacks `--issue`. SKIPPED: original owner design; owner decision.
  - Augment high, launch-level-guard.sh:444: guard text matching misses a call through Python `issue_pipeline_group.main([...])`. SKIPPED: pre-existing in the guard as restored; a guard change needs its own independent review (G2 design note); belongs in a separate change.
- Findings fixed: none. Pushes after the revert commit: none. A PR comment summarising the above and the full-suite result was posted on #697.
- Stopped per the instruction "if a finding says the revert is wrong or needs an owner decision, STOP and write it down": the three findings above need the owner.
- Not merged. Not to be merged until the owner says so.

## Status 2026-11-20 ~12:58 UTC (round 1: coordinator's go to fix)
- Coordinator order received in chat: do not stop; fix the two text findings in a separate commit; do not touch the guard; reply on the guard thread and leave it open; list the commits and follow-up on the PR.
- Commits on PR #697: a6d0889c2 (pure revert + re-applied no-`--to` bullet and tests); fd23c01a9 (separate docs+test commit: WC-17 step 4 passes `--issue <N>` to check-approval; the "Worktree, then worker" duty says the worker is the worktree's agent).
- Verified before editing: `check-approval` has `--issue` (cli.py, optional); `approval_line.check` refuses when the record id does not start with `ap-<issue>-plan-` (approval_line.py:60). The worker knows N from the brief's `Report directory: .dev/issues/{N}/worker-plan` line.
- Tests after fix: test_worker_contract + tests/issue_pipeline + test_launch_level_guard_worker + test_issue_pipeline_registered: 1013 passed. make lint passed. make verify-sync passed (after make sync-dev; nothing under .claude/ staged).
- Findings fixed: Augment medium WORKER-CONTRACT.md:59 (--issue). Thread replied and RESOLVED.
- DEVIATION from the coordinator's wording: the order said the worktree step "must create the worktree WITH an agent". `orca_worktree.py` (src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, docstring lines 30-38) deliberately runs `orca worktree create` WITHOUT `--agent` because the claim must copy the issue folder into the worktree before any agent starts, then closes Orca's plain first tab. Making the contract say "created with an agent" would be false. So the contract now states the true thing (created without an agent of its own for the copy; the worker started straight after by `worker-start` is that worktree's agent). The code is unchanged. Therefore the two 298 threads (Codex P1 FN1, Augment L4i) got a reply and were left OPEN, not resolved.
- Follow-ups (not done, owner or separate change):
  1. Augment high, launch-level-guard.sh:444: a bound worker can reach release_worker_command through Python (`issue_pipeline_group.main([...])`), past the literal matchers. Thread L4X replied ("real, out of scope for a revert, recorded as follow-up") and left open. Needs its own independent guard review (G2 design note); guard version stamp stays 1.
  2. orca_worktree.py creates the claim worktree without `--agent`; change it only if the owner wants the script to create with an agent (the copy must then happen another way).
- Review round on fd23c01a9: Augment "Review completed with 0 suggestions". Codex "Didn't find any major issues. Bravo." (12:55 UTC). CI: 6 of 6 checks pass.
- PR comments posted: full-suite result and skipped findings; commit list and follow-ups.
- Open threads: 3 (Codex FN1, Augment L4i = worktree agent; Augment L4X = guard). Both reviewers flagged nothing new. Not merged; do not merge until the owner says so.

## Status 2026-11-20 ~13:10 UTC (round 2: Codex security P2)
- New Codex security P2, thread PRRT_kwDOPOT5c865_mbP, `src/superclaude/cli/issue_pipeline/stage_predicates.py:138`: plan approval treats current assignee membership as approval even when the account id is not in the owner-managed approvers file.
- Verified: `git diff 01e7a9e23^ HEAD -- src/superclaude/cli/issue_pipeline` is empty (0 lines), so the code is the restored original, not introduced by the revert. `_is_allowed_actor` is lines 130-137 (`login in assignees OR account_id in approvers`), called at lines 180 (label channel) and 208 (comment channel); `assignee_is_host_login` is line 300 and only reported (cli.py:322). Design notes in docs/designs/issue-pipeline-*.md do not mention assignee membership as an approver rule (grep of issue-pipeline-fu1.md: no match); L-1 (same login for owner and agents) is recorded in the owner's answers file, per D03 VERDICT.md, not in docs/designs. I did not confirm the owner explicitly accepted the assignee branch: UNVERIFIED.
- Action: replied on the thread (real, design question for the owner, follow-up), left it OPEN; no code change. PR comment listing the follow-ups posted.

### Follow-ups (all open, none done here)
1. Guard bypass through Python `issue_pipeline_group.main([...])`: `src/superclaude/hooks/scripts/launch-level-guard.sh:444` (thread L4X). Needs its own independent guard review (G2 design note); stamp stays 1.
2. `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` creates the claim worktree without `--agent` (docstring lines 30-38); contract text now accurate (WORKER-CONTRACT.md line ~298). Threads FN1 and L4i open.
3. Approval membership: `src/superclaude/cli/issue_pipeline/stage_predicates.py:130-137` (used at 180 and 208). Suggested tightening: require the account id in the approvers file (drop the assignee branch), and bind approval to the assignee set at approval time (compare the `assigned` event time with the approval comment time). Thread mbP open. Owner decision: accept L-1 as is, or tighten.
- Open review threads on PR 697: 4 (FN1, L4i, L4X, mbP), all deliberate. Not merged.
