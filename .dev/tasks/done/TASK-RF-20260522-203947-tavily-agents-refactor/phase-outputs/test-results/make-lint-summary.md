# make lint summary

**Timestamp:** 2026-05-22 21:36
**Exit code:** 2 (Ruff exited non-zero)
**Overall result:** PRE-EXISTING FAIL (none caused by this task)

## Scope-bounded verdict

**No new failings introduced by the 10 edited agent files.**

- Total ruff findings: 442 errors (147 categorized findings)
- Findings in the 10 edited `src/superclaude/agents/*.md` files: **0**
- All findings touch Python files in `src/superclaude/cli/sprint/`, `src/superclaude/cli/eval/`, `tests/sprint/`, `.dev/eval-roadmap/`, `.dev/eval-workspaces/`, `.dev/research/`, and similar — i.e., **unrelated to this task**.
- 110 unique `.py` files reported; **zero** `.md` files reported (ruff is a Python linter; it does not lint markdown).

## Project-scope note

Per the BUILD_REQUEST / task spec: "agent definitions are markdown — markdown-lint findings in the 10 edited files are in scope, but pre-existing lint findings in unrelated files are not."

This pre-existing Python lint failure is documented as a follow-up for the project but does NOT block staging of the 10 agent refactors.

## Tail of lint output

```
F821 Undefined name `SprintConfig`
   --> tests/sprint/test_preflight.py:914:7
...
Found 442 errors.
[*] 172 fixable with the `--fix` option (110 hidden fixes can be enabled with the `--unsafe-fixes` option).
make: *** [Makefile:50: lint] Error 1
```
