# D-0086 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 141-148 (pre-edit), 141-172 (post-edit) | E2.3 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 186-265 (Expect.file), 640-669 (from_mapping) | Primitive surface |
| `src/superclaude/cli/eval/coverage.py` | 99-107 (`_DEFAULT_MCP_TOOL_PREFIXES`), 227-258 (`_iter_eval_tool_calls`, `eval_covers_pattern`) | Coverage gate path |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 22-32 (case branch), 25-30 (sticky→jsonl emit) | Hook contract — emits `sticky_cleared` + `tool=<TOOL_NAME>` IFF sticky pre-existed |
| `src/superclaude/hooks/hooks.json` | 60 | PostToolUse matcher registration `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*` |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | full | Sibling resolution — Expect.*-only constraint, soft-skip constraint |
| `.dev/releases/current/cliEval/artifacts/D-0083/spec.md` | full | Sibling deliverable (E1 body) — sticky-clear hook contract analysis carried forward |
| `.dev/releases/current/cliEval/artifacts/D-0084/spec.md` | (empty at write-time; pattern reconstructed from real.yaml E2.1 entry + evidence/T05.03) | Sibling deliverable (E2.1 body) — triad assertion shape origin |
| `.dev/releases/current/cliEval/artifacts/D-0085/spec.md` | full | Sibling deliverable (E2.2 body) — directly mirrored by this deliverable |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.05 block (lines 201-248) | Source task spec |

## Manifest delta

Pre-edit (`real.yaml:141-148`):

```yaml
- id: E2.3
  title: "auggie matcher coverage — mcp__airis-mcp-gateway__auggie_*"
  category: hook-coverage
  requires: [mcp_server.airis-mcp-gateway]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # Body landed by T05.05 / D-0086. Scaffolding only at T05.03 time.
```

Post-edit (`real.yaml:141-172`):

```yaml
- id: E2.3
  title: "auggie matcher coverage — mcp__airis-mcp-gateway__auggie_*"
  category: hook-coverage
  requires: [mcp_server.airis-mcp-gateway]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.05 / D-0086 — body shape. E2.3 covers the
  # `mcp__airis-mcp-gateway__auggie_.*` branch of the PostToolUse
  # matcher (hooks.json) by issuing a real
  # `mcp__airis-mcp-gateway__auggie_search` call. Same JSONL contract
  # as E2.1 / E2.2: the `tool` field on the `sticky_cleared` event
  # records the matched tool name, so asserting
  # `"tool":"mcp__airis-mcp-gateway__auggie_search"` in
  # `logs/auggie-first.jsonl` proves the matcher branch fired for the
  # `mcp__airis-mcp-gateway__auggie_*` prefix specifically (vs. the
  # sibling auggie / auggie-mcp prefixes covered by E2.1 / E2.2).
  # Note the trailing `auggie_` in the matcher: only gateway tools
  # whose name starts with `auggie_` (e.g. `auggie_search`,
  # `auggie_history`) fire this branch — generic gateway tools
  # (`tavily_search`, `context7_*`) do not.
  inputs:
    - prompt: "Use mcp__airis-mcp-gateway__auggie_search to summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."
      expect_tool_call: mcp__airis-mcp-gateway__auggie_search
  expects:
    - file:
        path: logs/auggie-first.jsonl
        exists: true
        contains: '"event":"sticky_cleared"'
    - file:
        path: logs/auggie-first.jsonl
        exists: true
        contains: '"tool":"mcp__airis-mcp-gateway__auggie_search"'
    - exit_code:
        equals: 0
```

## Verification runs

Captured under `.dev/releases/current/cliEval/evidence/T05.05/`:

| File | Command | Outcome |
|---|---|---|
| `describe-E2.3.txt` | `uv run superclaude eval describe --suite real --eval E2.3` | exit 0; renders the new inputs/expects rows; proves manifest body is loadable and round-trips through `Expect.from_mapping`. |
| `coverage-map.txt` | `uv run python -c "from superclaude.cli.eval.loader import SuiteLoader; …"` (same idiom as T05.04 evidence) | Lists `E2.3: covers ['mcp__airis-mcp-gateway__auggie_.*']` alongside `E1` / `E2.1` for `mcp__auggie__.*` and `E2.2` for `mcp__auggie-mcp__.*`. Confirms the v1 triad is now complete. |
| `run-E2.3-no-mcp.txt` | `uv run superclaude eval run --suite real --eval E2.3 --no-mcp` | Hits the same pre-existing `NameError: name '_new_run_id' is not defined` in `cli/eval/commands.py:1418` documented in evidence/T05.03 + T05.04. Not introduced by this deliverable. Soft-skip behavior is *verified at the gate / capability layer* (capability decl present in `optional_capabilities` and the `requires:` tag references it), not via this run. |

## Schema validation

The post-edit YAML loads cleanly under `SuiteLoader().load(...)`
(proof: `coverage-map.txt` succeeds — it parses every eval to compute
coverage). Each `expects[]` row has exactly one primitive key
(`file`, `file`, `exit_code`) which matches `PRIMITIVE_NAMES`
(`expect.py:56-64`). No `jsonschema` `additionalProperties: false`
violation; `eval describe` round-trips the body to YAML.

## Coverage gate evidence

Post-edit, `_iter_eval_tool_calls(spec_E2.3)` yields
`mcp__airis-mcp-gateway__auggie_search`, which matches the
`mcp__airis-mcp-gateway__auggie_.*` branch of the PostToolUse
matcher in `src/superclaude/hooks/hooks.json:60` (regex compiled
from `_DEFAULT_MCP_TOOL_PREFIXES[2]` per `coverage.py:103-107`).
E2.3 therefore registers as the sole covering eval for the
`mcp__airis-mcp-gateway__` prefix at the time of this writing — and
completes the v1 matcher-coverage triad, confirmed by the
`coverage-map.txt` output:

```
=== All matchers ===
E1: covers ['mcp__auggie__.*']
E2.1: covers ['mcp__auggie__.*']
E2.2: covers ['mcp__auggie-mcp__.*']
E2.3: covers ['mcp__airis-mcp-gateway__auggie_.*']
```

The CP-P05-T01-T05 checkpoint (T05.06) verifies that all three rows
present green together; T05.05 unblocks that checkpoint.

## Pre-existing runner bug (not in scope for T05.05)

`uv run superclaude eval run --suite real --eval E2.3 --no-mcp`
exits 1 with:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

This is the same failure documented in T05.03 evidence
(`run-E2.1-no-mcp.txt`) and T05.04 evidence (`run-E2.2-no-mcp.txt`)
and is **not introduced** by D-0086. It predates this deliverable;
fixing it is the responsibility of the runner-completion task that
is already a Phase-5 dependency of the CP-P05-T01-T05 checkpoint
(T05.06). T05.05's acceptance criteria (manifest body landed,
FR-SCH2-valid id, matcher contract documented, spec recorded) are
met by the describe / coverage-map evidence above.
