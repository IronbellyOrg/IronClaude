# Wave 1.5 Branch B (architectural docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)
Paths under src/superclaude/skills/sc-pr-submit-protocol/; currency_verdict unknown for every row.

| source_file:line | quoted_text | applies_to |
|---|---|---|
| scripts/finish-merge.sh:5-7 | "conclude it with exactly one commit from the given message file (hooks on)." | hooks on by design |
| scripts/finish-merge.sh:9-12 | "the only conflict script that changes the repository, and only through that one commit. ... never skips hooks" | header the fix stays inside |
| scripts/finish-merge.sh:24-26 | exit token list incl. tree_dirty, parents_mismatch | no new token needed |
| scripts/finish-merge.sh:196 | "Step 3: no unstaged change to a tracked file (the index equals the validated work tree)." | index validated before step 6 |
| scripts/finish-merge.sh:271-272 | "Step 6: the one commit, with hooks on." | the gap |
| scripts/finish-merge.sh:288-292 | "Step 8: clean after the commit." | passes when a hook edited and staged |
| refs/conflict-mechanical.md:114 | "It commits only through one commit from the message file, with hooks on." | step 9 contract |
| refs/conflict-mechanical.md:124 | "`tree_dirty` (commit-mode step 8, after the commit) \| `merge_preflight_dirty` \| the local merge commit is named; nothing pushed" | row the fix reuses |
| refs/conflict-mechanical.md:131 | trust limit names the commit hooks | known trust surface |
| refs/conflict-mechanical.md:230 | merge left in progress only for L2 step 8 and hook_rejected | an after-commit failure leaves a commit |
| refs/conflict-mechanical.md:277 | "never skip hooks, never amend" | rules out --no-verify and amend |
| refs/conflict-mechanical.md:283 | "Your checkout has uncommitted changes to tracked files: <paths>. Nothing was merged or pushed." | wording does not fit an after-commit tree mismatch |
| refs/conflict-mechanical.md:294 | "commit-mode `tree_dirty` (step 3 before the commit, step 8 after it) ... Raised after the commit, the local merge commit is named" | must describe the tree check in step 8 |
| refs/conflict-mechanical.md:298 | `sync_commit_failed` for hook_rejected | only a rejecting hook covered |
| SKILL.md:331 | halt row (pinned byte for byte, E12) | do not change |
