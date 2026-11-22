# Follow-up PR after PR 700: result

- Branch: ironbelly/restore-gaps-after-pr-700 (new, from origin/master 471f10511)
- Worktree: /home/coder/workspaces/worktrees/IronClaude/revert-pr-682
- PR: #701 https://github.com/IronbellyOrg/IronClaude/pull/701 (base master; not merged, not to be merged until the owner says so)
- Background: PR 697 closed (superseded by PR 700, merged 2026-11-20 15:07 UTC). This PR adds only what master lacks: the "Messages carry no `--to`" bullet and tests, and the fd23c01a9 review fixes.
- Pre-PR checks: origin = https://github.com/IronbellyOrg/IronClaude; gh repo = IronbellyOrg/IronClaude; fetched; branch from origin/master 471f10511.
- Gap check on master: "Messages carry no" has 0 matches in WORKER-CONTRACT.md and tests/skills/test_worker_contract.py.
- Commits: 78818366e (carry-over of the "Messages carry no --to" bullet, the messages-carry-no-to test entry and test_the_no_to_rule_sits_in_the_worker_session_duties; comment line reworded because the gate is no longer "retired"); 8f952bc54 (review fixes: WC-17 step 4 `--issue <N>`; "Worktree, then worker" reword; their test pins; short CHANGELOG entry).
- Tests: test_worker_contract + tests/issue_pipeline + test_launch_level_guard_worker + test_issue_pipeline_registered: 1012 passed. make lint passed. make verify-sync passed after make sync-dev and removing two stale local leftovers of agent-work-report (a gitignored .claude copy and an untracked src dir with only __pycache__, both from the earlier branch in this reused worktree; nothing tracked, nothing staged under .claude/).
- Issues 698 and 699 verified OPEN: 698 "Release-worker and plan-approval checks rest on text matching and an assignee shortcut"; 699 "The claim script creates the issue worktree without an agent, against the every-worktree-gets-an-agent rule".

## Status (PR opened)
PR #701 open on IronbellyOrg/IronClaude. Waiting for Augment, Codex and CI.

## Status 2026-11-20 ~16:40 UTC (round 1 done; loop finished)
- PR #701 https://github.com/IronbellyOrg/IronClaude/pull/701, head a17976c99, mergeable, NOT merged (do not merge until the owner says so). Commits: 78818366e, 8f952bc54, a17976c99.
- Round 1 review of 8f952bc54: Augment 2 suggestions (both medium), Codex code review clean.
  - FIXED: test pin did not cover "no agent before the issue-folder copy" (tests/skills/test_worker_contract.py:431). Added the pin in a17976c99. Thread PRRT_kwDOPOT5c866Ekg8 replied and RESOLVED.
  - SKIPPED, left OPEN with a reply pointing to issue 699: WORKER-CONTRACT.md:298 wording conflicts with core/CLAUDE.md "every worktree gets an agent" (thread PRRT_kwDOPOT5c866Ekg0). Reason: pre-existing conflict (the old text said "with no agent"); owner decision in issue 699 (change the script, or name the exception in core/CLAUDE.md).
- Round 2 review of a17976c99 (re-triggered both): Augment "0 suggestions"; Codex "Didn't find any major issues"; Codex security review "No security issues were found".
- CI on a17976c99: 6 of 6 pass (Lint/Plugin/Sync, Doctor, Swarm imm, Swarm inv, Test on Python 3.10, Test Summary).
- Local gates on the fix: 1012 tests passed; make lint passed; make verify-sync passed. `ruff format --check src/ tests/` reports 6 unrelated pre-existing files (e.g. src/superclaude/examples/release-spec-template.md); my files are formatted.
- Deviations: none from the order. Note: a transient git index.lock blocked the first commit once; it was gone on retry, nothing removed by hand. Removed two stale local leftovers of agent-work-report (gitignored .claude copy; untracked src dir with only __pycache__) to make verify-sync pass.
- Open threads: 1 (the issue 699 wording thread). Nothing else outstanding.
