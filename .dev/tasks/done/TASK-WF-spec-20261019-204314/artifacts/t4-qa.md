# Task 4 final independent compliance review

Final Q5 verdict: **compliant**. The reviewer re-read actual CLI/orchestration code and tests after the single gateway curl-preflight fix. No missing, extra-scope or misunderstood requirement remained. No commands/tests or edits were performed by the reviewer.

| AC | Status | Reviewer evidence |
|---|---|---|
| T4.AC1 | met | `src/superclaude/cli/main.py:233-298`; `src/superclaude/cli/install_mcp.py:1299-1329`; `tests/cli/test_install_codebase_memory.py:1178-1189` |
| T4.AC2 | met | `src/superclaude/cli/install_mcp.py:486-584`, `:1311-1314`; `tests/cli/test_install_codebase_memory.py:953-987`, `:1016-1038` |
| T4.AC3 | met | `src/superclaude/cli/install_mcp.py:1259-1271`, `:1321-1329`, `:1094-1108`; `tests/cli/test_install_codebase_memory.py:928-940`, `:1060-1085` |
| T4.AC4 | met | `src/superclaude/cli/install_mcp.py:499-503`, `:844-846`, `:1259-1263`, `:1315-1320`; `tests/cli/test_install_codebase_memory.py:881-892`, `:1052-1057` |
| T4.AC5 | met | `src/superclaude/cli/main.py:233-287`; `tests/cli/test_install_codebase_memory.py:839-878` |
| T4.AC6 | met | `src/superclaude/cli/install_mcp.py:822-828`, `:953-966`, `:1061-1066`, `:1094-1108`, `:1248-1258`, `:1321-1334`; `tests/cli/test_install_codebase_memory.py:1088-1164` |
| T4.AC7 | met after fix | `src/superclaude/cli/install_mcp.py:551-560`, `:1331-1359`; `tests/cli/test_install_codebase_memory.py:990-1005`, `:1219-1273` |
| T4.AC8 | met | `tests/cli/test_install_codebase_memory.py:839-1216`, `:1219-1273` |

Gateway selection now checks curl independently of native acquisition state, before the installer loop. Native-only reuse remains independent of acquisition-only curl/Bash. New cases use the real gateway function while intercepting external commands, checking gateway-only and mixed-order selections, missing curl, reused native binaries, no effects and mutation-free dry-run planning.

Default framework installation/update wiring remains outside Task 4; no Task 5 omission is implied by the unchanged installer.

## Coordinator post-review extras

Existing environment, explicit worktree imports, `PYTHONDONTWRITEBYTECODE=1`, no pytest cache provider:

- Focused native/registry/Tavily/update-command suite: **220 passed, 1 skipped in 35.43s**, exit 0. The skipped test is the existing API-key-gated live Tavily check.
- Ruff across the four Task 4 product/test files: exit 0, all checks passed.
- Scoped mypy on main.py/install_mcp.py: exit 1, exactly the two established legacy install_mcp diagnostics (return-Any at line 706, registry object/string at line 1209), no new diagnostics. Exact baseline comparison remains in `t4-checks.txt` / `t4-q5-checks.txt`; typechecking is not represented as green.

No real upstream installation/removal or developer configuration mutation was performed. The live release smoke gate remains pending.
