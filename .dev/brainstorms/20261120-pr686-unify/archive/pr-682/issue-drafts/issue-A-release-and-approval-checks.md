## What was tried
Review of PR 697 (the revert of PR 682, which had deleted the plan-approval package `issue_pipeline`) raised two findings on code that the revert restores byte for byte (`git diff 01e7a9e23^ HEAD -- src/superclaude/cli/issue_pipeline` is empty). The code comes from the owner's PRs 584 and 591 of 2026-11-17. Neither finding is caused by PR 682 or by the revert, so neither was fixed in PR 697: a guard change needs its own independent review (the G2 design note), and the approval rule is a design choice. The review threads were answered and left open. Nothing runs these paths live today, because the issue watcher is switched off (`enabled: false`). Neither finding was exercised: no bypass was tried and no approval was forged.

1. Launch-guard bypass (Augment, high). The guard blocks a bound worker by reading the command text for `release-worker`, `issue-pipeline ... adopt-` and similar words (`launch-level-guard.sh` lines 441 to 444). A worker can build the call from pieces, for example `"re" + "lease-worker"`, or import the Click group and call `issue_pipeline_group.main([...])`, so the text never appears. The `release-worker` command creates `sessions/<session_id>.ok` (`release.py` lines 38 to 66). That file lifts the worker from the plan-only level to "worktree (approved)". The command does not check that an approval exists (`cli.py` lines 200 to 214), so the text guard is the only barrier. The worker also holds the same GitHub login as the owner, so it could post the approval itself (`docs/designs/issue-pipeline-fu1.md` line 32). The bypass is a second route to the same result.

2. Approver rule (Codex security, P2). `_is_allowed_actor` (`stage_predicates.py` lines 130 to 137) accepts a comment author whose login is in the issue's current assignee list OR whose account id is in the owner-managed approvers file. A previously posted, unedited "approved" comment from someone who was not an approver becomes valid later if that person becomes an assignee. `assignee_is_host_login` (line 300) is only reported (`cli.py` line 322), never enforced.

## Relevant files and links
- `src/superclaude/hooks/scripts/launch-level-guard.sh` lines 441 to 444 and its mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh`
- `src/superclaude/cli/issue_pipeline/release.py`, `cli.py` (`release-worker`, line 200), `stage_predicates.py` (lines 130 to 137, call sites at lines 180 and 208, line 300)
- `docs/designs/issue-pipeline-fu1.md` (same-login limit, line 32), `docs/designs/issue-pipeline-guard-g2.md` and `issue-pipeline-guard-g2-no-to.md`
- PR 697 (the revert) review threads: https://github.com/IronbellyOrg/IronClaude/pull/697; PR 682 (the deletion, commit `01e7a9e23`) saved under the tag `archive/pr-682-issue-pipeline-removal`; PRs 584 and 591 (the original work)
- Unification work: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md (INV-025: the guard only narrows honest mistakes; SEC-08 and FR-84: approval comes from the owner's chat, recorded by the agent), debates D03 and D05

## Done when
1. The owner chooses how release is protected, and the choice is tested. One of: (a) the guard also catches the Python and Click-group routes, with an independent review of the guard change; (b) `release-worker` itself refuses unless an approval record exists; (c) the store is not writable by the worker's account; or (d) the owner records that the guard is only a seatbelt against honest mistakes and the docs say so. A test proves whichever behaviour is chosen.
2. The approver rule is decided and tested: either approval counts only from an account id in the approvers file and is bound to the assignee set at approval time (compare the `assigned` event time with the approval comment time), or the owner records that the assignee branch is accepted. The result is stated in `issue-pipeline-fu1.md`.

## Pick-up note
- Do not change either piece inside a revert or a refactor of another area. A guard change needs its own independent review.
- A text-matching guard cannot be fully closed. Options (b) and (c) are stronger, but the approval rows are written by commands that the same guard protects, so only (c) or a different account closes it.
- Decide the approver rule together with the spec's approval-in-chat design (SEC-08, FR-84), which makes the comment path secondary.
- The owner's accepted login limit L-1 (one GitHub login for the owner and the agents) applies to both pieces. Whether the owner accepted the assignee branch itself is UNVERIFIED.
