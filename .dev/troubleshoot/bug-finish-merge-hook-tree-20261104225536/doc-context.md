# Documentation Context Card

## Release context
No release slug. Design section 7.2 (source.md:816-824) proves the index before the commit (steps 3-5), commits with hooks on (step 6), and after the commit checks only the parents (step 7) and a clean checkout (step 8); every hook mention is about a hook rejecting the commit (J-60, J-61, J-63, INV-032, OQ-19, F9). Nothing compares the committed tree with the validated index: a design gap the script follows (wave1_5-branch-A.md).

## Architectural docs consulted
- scripts/finish-merge.sh:5-12, :24-26, :196, :271-292 (CAUTION: currency unknown)
- refs/conflict-mechanical.md:114, :124, :131, :230, :277, :283, :294, :298 (CAUTION: currency unknown)
- SKILL.md:331 (pinned; CAUTION: currency unknown)

## Restrictions / decisions that constrain the fix
- Hooks stay on, no amend, no --no-verify (J-60, conflict-mechanical.md:277).
- Exactly one `git commit` text match in finish-merge.sh; banned command words unchanged (test_conflict_scripts.py:1143-1155).
- Reuse an existing token: `tree_dirty` after the commit maps to merge_preflight_dirty, "the local merge commit is named; nothing pushed" (conflict-mechanical.md:124); SKILL.md:331 unchanged.
- The ref keeps one commit-mode finish-merge.sh line (test_conflict_sync_protocol.py:594-607).

## Re-frame signals
- The gate proves a property of the index, but publishes a commit; the fix ties the published commit to the proven index.
- The halt message wording for an after-commit tree_dirty (conflict-mechanical.md:283) assumes a dirty checkout; it needs a clause for a hook-changed commit.
