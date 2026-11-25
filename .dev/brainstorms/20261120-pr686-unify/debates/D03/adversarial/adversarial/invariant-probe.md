# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis

An independent fault-finder subagent (not an advocate) probed the emerging consensus ("revert PR 682, keep the no `--to` bullet, conditional on D01") in six categories. It worked in scratch copies of a simulated revert tree under `/tmp` and wrote no ref, index or working-tree change. Verified again by the orchestrator: INV-001 (symbols missing from the PR 686 snapshot: `EditEvidence`, `LabelEvent`, `CommentEdit`, `_argv_rest_page`, `validate_approvers` have no hit in `/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/*.py`; `main.py` of the pre-682 tree imports `issue_pipeline` at line 581) and INV-003 (`git grep GOVERNED_LEVELS_ALLOWED origin/master -- src tests` finds nothing).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | The revert and PR 686 are separable and only need sequencing | UNADDRESSED | HIGH | The old package's imports all exist on master but not on PR 686's head 8e5ae29ad. `git merge-tree` of the revert result with PR 686 reports no conflict beyond CHANGELOG.md, yet the merged tree fails to import (`_argv_rest_page`), `superclaude --help` crashes because `main.py` imports `issue_pipeline` eagerly, and 29 test modules fail at collection. Git gives no warning in either merge order. |
| INV-002 | sufficiency_challenge | "Revert, but keep the no `--to` bullet" happens inside a bare revert | UNADDRESSED | MEDIUM | The simulated revert tree has no standalone bullet (the sentence lives only in WC-17 line 59, which covers pipeline workers) and loses the assertions at `tests/skills/test_worker_contract.py` lines 426-429 and 3220; tests still pass, so nothing signals the loss. Keeping it needs a hand edit and the sentence then appears twice. |
| INV-003 | guard_conditions | The condition "R18 default-on config stays blocked by R33 (`GOVERNED_LEVELS_ALLOWED = False`)" holds today | UNADDRESSED | MEDIUM | No hit for `GOVERNED_LEVELS_ALLOWED` in src or tests on master, the three snapshots or the owner branch commits; only `requirements.md` row R33 ("decided (not built)"). The only real hold is `cycle.py:228`, `raw.get("enabled", False)`. |
| INV-004 | state_variables | Once the revert lands, the host runs the restored code | UNADDRESSED | MEDIUM | `/home/coder/.claude/hooks/launch-level-guard.sh` matches neither the pre-682 nor the master guard; `/home/coder/.claude/WORKER-CONTRACT.md` still has WC-17; `/usr/local/bin/superclaude` still lists `issue-pipeline`. Hosts that installed between 00:02Z and the revert have a guard without rule 1 beside restored coordinator-only verbs. |
| INV-005 | guard_conditions | The guard version stamp tells which guard behaviour is installed | UNADDRESSED | MEDIUM | `# launch-level-guard-version: 1` is on line 10 before PR 682 and on master; `orca_worktree.py:839,986-987` checks only that line. PR 682 removed rule 1 without bumping it and the revert leaves it at 1, so nothing mechanical separates a rule-1 guard from a stale one. Owner row R33 item 6 plans stamp 2 (itself a guard change needing independent review). |
| INV-006 | guard_conditions | "Ironbelly gives a written ruling" is a checkable gate | UNADDRESSED | MEDIUM | `gh api repos/IronbellyOrg/IronClaude/collaborators`: ironbelly is the only admin; `branches/master/protection` returns 404 (unprotected); `gh api user` on this host returns `ironbelly`, so a GitHub comment "by ironbelly" can come from an agent. The channel must be named (the owner's chat, recorded by the agent) and who merges. |
| INV-007 | count_divergence | "3 of 36 files conflict" | UNADDRESSED | LOW | 36 files and 3 later-changed files are correct, but `git merge-tree --write-tree --merge-base=01e7a9e23 origin/master 01e7a9e23^` reports one textual conflict (CHANGELOG.md); WORKER-CONTRACT.md and `test_worker_contract.py` auto-merge. The error is on the cautious side. |
| INV-008 | count_divergence | The quoted counts match the repo | UNADDRESSED | LOW | Consistent: 36 files, 4,599 lines (2,969 tests + 1,618 src), package 1,597, 11 RECORDED lines. Divergent: restored tests are 117 test functions (222 collected cases), not "about 80"; the owner worktree shows 223 status entries (70 outside `.dev/`), not 53; 687 and 689 are issues not PRs (open PRs: 685, 686, 690). |
| INV-009 | collection_boundaries | A differing plugin guard or an absence-assertion test would break the revert | ADDRESSED | LOW | After the simulated revert source and plugin guards are byte-identical; `git grep -E 'issue[-_]pipeline' origin/master -- tests` returns nothing; rule-1 tamper tests return and pass (115). One restored test, `test_the_watcher_record_module_is_not_edited`, failed in the non-git scratch copy (needs `git diff HEAD`), unconfirmed. |
| INV-010 | interaction_effects | The owner's local branch rebases onto a reverted master | ADDRESSED | LOW | Its tracked uncommitted changes (1,767-line patch over 13 files) pass `git apply --check` on the revert tree and fail on current master for all 13 files. Its 3 committed commits conflict identically on both in 3 unrelated files. Untracked `complete.py` and its tests not covered. |
| INV-011 | sufficiency_challenge | `git revert` alone gives a consistent state | UNADDRESSED | MEDIUM | PR 681's design is not reverted and says the opposite: `orchestrator.md` line 73 (R1), 987-991, 997-1004, 1017, 1095, 1381 describe the gate as retired; PRs A, B, E build against it. R1 and section 7 need an explicit amendment in the revert PR or a named follow-up. |
| INV-012 | interaction_effects | Merged 683, 684, 688 and open 685, 690 do not interact | ADDRESSED | LOW | Only CHANGELOG.md, WORKER-CONTRACT.md and `test_worker_contract.py` changed later; PR 690 overlaps CHANGELOG.md only; PR 685 touches none of the 36. |
| INV-013 | state_variables | Restored approval rows stay compatible with PR 686's `record.py` schema 2 | ADDRESSED | LOW | The package uses only `FileStore.lock()`, `LockError`, `LockHeld` and `write_prepared_bytes`, all present in the PR 686 snapshot; no persisted rows exist (watcher never ran live). Behaviour against PR 686 itself is unverified because of INV-001. |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 4
- **UNADDRESSED**: 9
  - HIGH: 1 (INV-001)
  - MEDIUM: 6 (INV-002, INV-003, INV-004, INV-005, INV-006, INV-011)
  - LOW: 2 (INV-007, INV-008)

## Gate result

CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant detected. Blocking item: INV-001.
Standard depth has no Round 3, so it could not be debated again. The orchestrator records it as an acknowledged risk and makes it a mandatory precondition in the refactor plan (see `refactor-plan.md`, change 1); the return contract keeps it in `unaddressed_invariants`. MEDIUM items are warnings and are all planned for in `refactor-plan.md`.
