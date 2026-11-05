---
status: success
tier_reached: 1
confidence: 1.00
escalation_reason: none
caller: sc-pr-submit-protocol
---
# Troubleshoot report: a commit hook changes the merge commit after the finish gate (PR #378 finding C4)

## Summary
finish-merge.sh validates the index (steps 2-5), then commits with hooks on (step 6) and afterwards checks only the parents and a clean checkout (steps 7-8). A pre-commit hook that rewrites and stages a tracked file changes what is committed, leaves the checkout clean, and the script exits 0. A probe reproduced it: the commit's tree differed from the validated index tree and carried the hook's edit.

## Documentation Context
Design section 7.2 treats hooks only as something that can reject the commit; nothing ties the commit to the validated index (doc-context.md). Hooks must stay on and amend is banned, so the fix is a post-commit comparison reusing the `tree_dirty` token.

## Diagnosability Context
Verdict partial, complexity trivial: a hook-changed commit passed silently; a hermetic real-git test with a pre-commit hook makes it observable (diagnosability-context.md).

## Diagnosis
Missing post-condition: the gate proves the index, but publishes the commit, and a hook runs between the two.

## Evidence
- .dev/troubleshoot/bug-finish-merge-hook-tree-20261104225536/probe-c4.out:2 — `exit: 0`
- .dev/troubleshoot/bug-finish-merge-hook-tree-20261104225536/probe-c4.out:3-4 — validated index tree `75418c01...` vs committed tree `1eea654f...`
- .dev/troubleshoot/bug-finish-merge-hook-tree-20261104225536/probe-c4.out:5 — `unrelated.txt in HEAD: changed by hook`
- src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:124 — `tree_dirty` after the commit maps to `merge_preflight_dirty`: the local merge commit is named, nothing pushed

## Proposed Fix
After step 5, finish-merge.sh records the validated index as a tree object (`VALIDATED_TREE="$(git write-tree)"`, finish-merge.sh:274; no ref or index change). In step 8 it compares `HEAD^{tree}` with it (finish-merge.sh:296-298) and fails `tree_dirty` naming the new commit when they differ; nothing is pushed. One `git commit` remains, hooks stay on, no new token. refs/conflict-mechanical.md step 9 (:114), the token row (:124) and the `merge_preflight_dirty` row describe the check and its message. Regression tests: test_hook_that_changes_staged_content_is_tree_dirty_after_the_commit (fails on 62121669) and test_hook_that_changes_nothing_still_finishes (tests/pr_submit/test_conflict_scripts.py:989, :1015).

## Risk + Rollback
Hooks that legitimately reformat files now halt the cycle after a local commit (intended: validation must cover what is published); a failed write-tree reports `tree_dirty` before the commit. Rollback: revert the fix commit.

## Pipeline Hardening Closure
See hardening.md: applicable (CLI/subprocess, gate/status enum); verdict advisory (HC3, HC4 N/A with rationale).

## Next Steps
sc:pr-submit publishes the edit in round 2's single fix commit after VAL, replies on thread C4 with the fix SHA and resolves it.
