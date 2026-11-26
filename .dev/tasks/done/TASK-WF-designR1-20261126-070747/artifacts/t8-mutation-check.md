# Task 8 mutation check

Done once by hand (script run with the package folder as the working directory). The skill file was restored by copying the saved file back after every mutation; no `git checkout`, `git restore`, `git reset --hard` or `git stash` was used. The `--base` assertion on `src/superclaude/commands/post-release.md` is a static guard on a file this plan never edits: it runs with the other assertions, passes on the unedited file and gets no mutation.

- checksum before the first mutation: `a816b59954a47c29ffdf57c2c688e48f0c958601b5a1195759b9e1983c7b4288` (`./artifacts/t8-skill.sha256`; copy `./artifacts/t8-skill.pre-mutation`)
- checksum after the last restore: `a816b59954a47c29ffdf57c2c688e48f0c958601b5a1195759b9e1983c7b4288`
- `sha256sum -c ./artifacts/t8-skill.sha256`: /home/coder/workspaces/worktrees/IronClaude/issue-826/src/superclaude/skills/sc-post-release-protocol/SKILL.md: OK (exit 0)
- Task 8 tests on the restored file: ============================== 11 passed in 0.04s ==============================

| Assertion group | Mutation (reverts the matching Task 7 edit unless marked extra) | Failing test(s) | `cmp` after mutation (1 = file changed) | `cmp` after restore (0 = identical) | Result |
|---|---|---|---|---|---|
| the paragraph | put the old detection command `git symbolic-ref refs/remotes/origin/HEAD` back in place of `git ls-remote --symref origin HEAD` (reverts the live-resolution part of the line 91 edit) | `test_paragraph_names_live_resolution_and_remote_check[git` | 1 | 0 | failed as required |
| the paragraph | replace `unverified` with `uncertain` (reverts the unverified rule of the line 91 edit) | `test_paragraph_names_live_resolution_and_remote_check[unverified]` | 1 | 0 | failed as required |
| the old command | put the old comparison `git merge-base --is-ancestor <tag> <default-branch>` back at the end of the paragraph | `test_old_local_branch_comparison_is_gone` | 1 | 0 | failed as required |
| the regular expression | put the old sentence fragment "do not assume `main`/`master`" back at the end of the paragraph | `test_paragraph_names_no_branch` | 1 | 0 | failed as required |
| the Output and Exit criteria lines | revert the Output line to "auto-detected default branch" | `test_output_and_exit_lines_say_resolved_with_source` | 1 | 0 | failed as required |
| the Output and Exit criteria lines | revert the Exit criteria line to "default branch auto-detected" | `test_output_and_exit_lines_say_resolved_with_source` | 1 | 0 | failed as required |
| the WARN line and Guardrails text | revert the Guardrails PR-target addition (Task 7 edit of line 348) | `test_guardrails_name_the_offline_fallback_and_ask_the_user` | 1 | 0 | failed as required |
| the WARN line and Guardrails text | extra: alter the WARN line (line 74, which Task 7 leaves unchanged) so it no longer ends with the tag | `test_warn_line_still_ends_with_the_tag` | 1 | 0 | failed as required |
