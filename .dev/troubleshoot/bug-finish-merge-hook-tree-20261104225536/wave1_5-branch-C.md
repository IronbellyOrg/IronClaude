# Wave 1.5 Branch C (semantic restrictions), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

| source_file:line | quoted_text | applies_to |
|---|---|---|
| tests/pr_submit/test_conflict_scripts.py:1143-1144 | exactly one `git commit` match and one `git commit -F "$MESSAGE_FILE"` | no new text may contain "git commit" |
| tests/pr_submit/test_conflict_scripts.py:1146-1155 | bans git push, stash, force, git config, --no-verify, --amend, commit -a/--all/--only, src/superclaude, git checkout/switch/reset/add/worktree/rebase/merge, gh | `git write-tree` and `rev-parse HEAD^{tree}` match none |
| tests/pr_submit/test_conflict_scripts.py:930-957 | test_f7, test_f8 assert tree_dirty | pin the token, not its site |
| tests/pr_submit/test_conflict_scripts.py:960-979 | test_f9 failing pre-commit hook -> hook_rejected | no test for a hook that changes the commit |
| tests/pr_submit/test_conflict_scripts.py:4 | docstring "cases F1 to F12" | update if a new case is named |
| tests/pr_submit/test_conflict_sync_protocol.py:594-607 | one probe, one finish-merge commit-mode command, one push | no second commit-mode line in the ref |
| tests/pr_submit/test_conflict_sync_protocol.py:336-340 | E12 pins SKILL.md:331 | do not change SKILL.md:331 |
| src/superclaude/pr_submit/conflicts.py:161, :167 | merge_preflight_dirty, sync_commit_failed in HALT_REASONS | reuse needs no set change |
| grep tests/pr_submit | no pin on "only through that one commit", "HEAD^{tree}"; "write-tree" only as `merge-tree --write-tree` | header text free to change |
| scripts/finish-merge.sh:9-10 | "only through that one commit" | git write-tree adds a tree object (no ref or index change; the same object the commit writes when no hook interferes); needs no unmerged entries (step 2 guarantees it) |
