# Task 6 mutation check

Done once by hand (script run with the package folder as the working directory). The page was restored by copying the saved file back after every mutation; no `git checkout`, `git restore`, `git reset --hard` or `git stash` was used.

- checksum before the first mutation: `7b7098103a9b4b27377a9f3a4d6a153b4badacee1f67cd99a25dc6b6f50ae68b` (`./artifacts/t6-page.sha256`; copy `./artifacts/t6-page.pre-mutation`)
- checksum after the last restore: `7b7098103a9b4b27377a9f3a4d6a153b4badacee1f67cd99a25dc6b6f50ae68b`
- `sha256sum -c ./artifacts/t6-page.sha256`: /home/coder/workspaces/worktrees/IronClaude/issue-826/docs/developer-guide/release-procedure.md: OK (exit 0)
- Task 6 tests on the restored page: ============================== 34 passed in 0.07s ==============================

| Test function | Mutation | Failing test(s) | `cmp` after mutation (1 = page changed) | `cmp` after restore (0 = identical) | Result |
|---|---|---|---|---|---|
| `test_required_command_is_on_the_page` | delete the `git switch --detach <reviewed-head-sha>` line of the detached-checkout block | `test_required_command_is_on_the_page[git` | 1 | 0 | failed as required |
| `test_required_command_is_on_the_page` | remove `--match-head-commit <reviewed-head-sha>` from the Step 2 merge line | `test_required_command_is_on_the_page[gh` | 1 | 0 | failed as required |
| `test_step2_has_its_own_commands` | delete the detached-checkout `make sync-dev` line of Step 2 | `test_step2_has_its_own_commands` | 1 | 0 | failed as required |
| `test_step2_has_its_own_commands` | delete the Step 2 precondition ancestry line | `test_step2_has_its_own_commands` | 1 | 0 | failed as required |
| `test_verify_tag_on_the_release_line` | remove `--verify-tag` from the `gh release create` line | `test_verify_tag_on_the_release_line` | 1 | 0 | failed as required |
| `test_every_gh_line_names_the_fork` | remove `--repo IronbellyOrg/IronClaude` from the `gh pr view` line | `test_required_command_is_on_the_page[gh`, `test_every_gh_line_names_the_fork` | 1 | 0 | failed as required |
| `test_banned_merge_options` | add `--delete-branch` to the fenced merge-back `gh pr merge` line | `test_banned_merge_options` | 1 | 0 | failed as required |
| `test_removed_text_is_gone` | append `--limit 3` to the G6 pass condition | `test_removed_text_is_gone[--limit` | 1 | 0 | failed as required |
| `test_contents_links_resolve` | change the Step 4 Contents anchor to `#step-4-tag` | `test_contents_links_resolve` | 1 | 0 | failed as required |
