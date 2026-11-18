# Codegraph grounding

## Run state

- index_state: fresh (status: 3792 files, 0 added, 0 modified, 0 removed)
- checked_at: 2026-11-17T21:02:53Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-review-translation
- projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-review-translation
- access: mcp
- tokens: none (markdown files are not indexed: the doc, command and skill targets are resolved with Grep and Read, which is the permanent floor)

## Resolved symbols

- `codegraph_search review_translation`: only `tests/unit/test_review_translation.py` (file) and `P2_NEW_BRIEF_ROWS` (`tests/skills/test_worker_contract.py:1002`). No function, class or import in `src/superclaude/` names the item.
- `tests/skills/test_worker_contract.py` symbols touched: `P2_COMMANDS` (:496), `UNATTENDED_EXPECT` (:518, entry at :679), `P2_NEW_BRIEF_ROWS` (:1002), `_check_p2_set` (:1667, the 15 and 31 literals), `P2_GATES` (:1791, two review-translation tuples).
- Docs and routing text (markdown, not indexed): resolved with `git grep` in `.dev/cleanup/review-translation/dependency-map.md`.

## Dependents

- `P2_COMMANDS`: `_check_p1_set`:1466, `_check_p2_brief`:1027, `test_p2_command_set_is_complete`:1680, `_P2_SET_DEFECTS`:1684, `test_p1_set_check_fails_on_a_missing_extra_or_repeated_command`:1574, `test_p2_set_check_fails_when_a_command_file_is_missing`:1712 (impact, depth 1; resolution: def-line, all in the same test file).
- `_check_p2_set`: callers `test_p2_command_set_is_complete`:1680, `test_p2_set_check_fails_on_a_missing_extra_or_repeated_command`:1707, `test_p2_set_check_fails_when_a_command_file_is_missing`:1712 (resolution: def-line). They read the 15/31 literals, so those literals change in the same task as the tuples.
- `P2_NEW_BRIEF_ROWS`: `_check_p2_brief`:1027 and `test_p2_brief_check_fails_when_a_row_is_removed`:1066 (parametrized; loses one case).
- `tests/skills/test_worker_contract.py` reads `src/superclaude/core/WORKER-CONTRACT.md`, so the contract text edit must land before the test edit is run.

## Pre-check

Read-only check at 2026-11-17T21:06Z (git grep and sed, plus the codegraph results above):

- Tasks 1 to 11: every named file exists; the named lines were re-read (HOW-WE-WORK.md 252 and 383, WORKER-CONTRACT.md 330/334/350, the fixture S07 case at lines 175 to 193 and inputs at 32 and 33, test_worker_contract.py 504/679/1006/1667/1813-1824, test_cli_install.py 118 and 288, commands.md 95 and 587-615, the three generated docs).
- S07 spans lines 175 to 193 (the plan says "about 175 to 195"; harmless).
- Dependents of the touched symbols that no task names: none found. `P2_COMMANDS` dependents are all inside `tests/skills/test_worker_contract.py` and follow from the tuple edit in Task 5.
- Count: 11 tasks, 11 resolved, 0 unresolved.
