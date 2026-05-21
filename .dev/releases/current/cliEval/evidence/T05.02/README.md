# T05.02 — Evidence (E1 manifest body authoring)

**Task:** Author E1 auggie-first sticky lifecycle eval body
**Deliverable:** D-0083
**Date:** 2026-05-20
**Status:** ✅ authored + schema/DSL/coverage round-trip verified

## Captured commands

| # | File | Command | Result |
|---|---|---|---|
| 01 | `01-eval-describe.log` | `uv run superclaude eval describe --suite real --eval E1` | PASS — new inputs/expects rendered |
| 02 | `02-eval-run-no-mcp.log` | `uv run superclaude eval run --suite real --eval E1 --no-mcp` | BLOCKED — pre-existing `NameError: _new_run_id` in `commands.py:1418`, unrelated to T05.02 |
| 03 | `03-eval-run-no-pty.log` | `uv run superclaude eval run --suite real --eval E1 --no-pty` | BLOCKED — same pre-existing `NameError` |
| 04 | `04-loader-and-expect-roundtrip.log` | direct python: `validate_manifest()` + `Expect.from_mapping()` per row + `_iter_eval_tool_calls(E1)` | PASS on all three |

## Headline confirmation (from 04)

```
=== E1 parsed ===
  inputs=({'prompt': 'Use mcp__auggie__codebase-retrieval ...', 'expect_tool_call': 'mcp__auggie__codebase-retrieval'},)
  expects=({'file': {'path': 'logs/auggie-first.jsonl', 'exists': True, 'contains': '"event":"sticky_cleared"'}},
           {'exit_code': {'equals': 0}})
=== Expect.from_mapping per expects[] row ===
  [0] -> file  (callable: True)
  [1] -> exit_code  (callable: True)
=== _iter_eval_tool_calls(E1) ===
  ['mcp__auggie__codebase-retrieval']
```

This proves:

1. **Schema-valid** — `validate_manifest()` accepts the post-edit YAML.
2. **DSL-valid** — both `expects[]` rows resolve through
   `Expect.from_mapping` to live `ExpectCallable`s.
3. **Coverage-gate reachable** — `_iter_eval_tool_calls(E1)` yields the
   auggie tool name, so the FR-COV1 gate will credit E1 with covering
   the `mcp__auggie__*` PostToolUse matcher.

## Pre-existing blocker (NOT in scope of T05.02)

`uv run superclaude eval run --suite real --eval E1 [...]` fails on
`commands.py:1418` with:

```
NameError: name '_new_run_id' is not defined
```

This is a wiring gap in the in-development runtime (the entire
`src/superclaude/cli/eval/` tree is untracked on this branch).
T05.02 authors the manifest body; the runtime invocation path is the
responsibility of the runner-completion task downstream. The blocker
is flagged in `.dev/releases/current/cliEval/artifacts/D-0083/spec.md`
§6 and should be tracked separately on the runner track.

## AC mapping (per phase-5-tasklist.md T05.02)

| AC | Verified via | Status |
|---|---|---|
| E1 invokes `mcp__auggie__codebase-retrieval` | `inputs[0].expect_tool_call` round-trip in 04 | ✅ |
| Asserts `logs/auggie-first.jsonl` gains `sticky_cleared` event | `expects[0]` round-trip in 04 + D-0083 §2 (hook contract) | ✅ |
| Asserts `state/auggie-first-pending/<sid>.txt` exists pre-call & removed post-call | D-0083 §4 (deferred, documented gap; covered transitively by `sticky_cleared` proxy per hook script line 25) | ⚠️ documented gap |
| `spec.md` documents contract + `--no-mcp` skip behavior | D-0083/spec.md §2, §5 | ✅ |
| `hook-lifecycle` tag | unchanged from existing E1 scaffold (`category: hook-lifecycle`) | ✅ |
| `--no-mcp` soft-skip | wired via `requires: [mcp_server.auggie]` + suite-level `optional_capabilities` | ✅ (config); blocked from runtime proof by pre-existing `_new_run_id` NameError |
