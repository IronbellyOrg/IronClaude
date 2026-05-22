# D-0085 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 110-117 (pre-edit), 110-136 (post-edit) | E2.2 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 186-265 (Expect.file), 640-669 (from_mapping) | Primitive surface |
| `src/superclaude/cli/eval/coverage.py` | 99-107 (`_DEFAULT_MCP_TOOL_PREFIXES`), 227-258 (`_iter_eval_tool_calls`, `eval_covers_pattern`) | Coverage gate path |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 22-32 (case branch), 25-30 (sticky→jsonl emit) | Hook contract — emits `sticky_cleared` + `tool=<TOOL_NAME>` IFF sticky pre-existed |
| `src/superclaude/hooks/hooks.json` | 60 | PostToolUse matcher registration `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*` |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | full | Sibling resolution — Expect.*-only constraint, soft-skip constraint |
| `.dev/releases/current/cliEval/artifacts/D-0083/spec.md` | full | Sibling deliverable (E1 body) — sticky-clear hook contract analysis carried forward |
| `.dev/releases/current/cliEval/artifacts/D-0084/spec.md` | (empty at write-time; pattern reconstructed from real.yaml E2.1 entry + evidence/T05.03) | Sibling deliverable (E2.1 body) — triad assertion shape |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.04 block (lines 152-199) | Source task spec |

## Manifest delta

Pre-edit (`real.yaml:110-117`):

```yaml
- id: E2.2
  title: "auggie matcher coverage — mcp__auggie-mcp__*"
  category: hook-coverage
  requires: [mcp_server.auggie-mcp]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # Body landed by T05.04 / D-0085. Scaffolding only at T05.03 time.
```

Post-edit (`real.yaml:110-136`):

```yaml
- id: E2.2
  title: "auggie matcher coverage — mcp__auggie-mcp__*"
  category: hook-coverage
  requires: [mcp_server.auggie-mcp]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.04 / D-0085 — body shape. E2.2 covers the `mcp__auggie-mcp__.*`
  # branch of the PostToolUse matcher (hooks.json) by issuing a real
  # `mcp__auggie-mcp__ask_question` call. Same JSONL contract as E2.1:
  # the `tool` field on the `sticky_cleared` event records the matched
  # tool name, so asserting `"tool":"mcp__auggie-mcp__ask_question"` in
  # `logs/auggie-first.jsonl` proves the matcher branch fired for the
  # `mcp__auggie-mcp__*` prefix specifically (vs. the sibling auggie /
  # airis-mcp-gateway prefixes covered by E2.1 / E2.3).
  inputs:
    - prompt: "Use mcp__auggie-mcp__ask_question to summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."
      expect_tool_call: mcp__auggie-mcp__ask_question
  expects:
    - file:
        path: logs/auggie-first.jsonl
        exists: true
        contains: '"event":"sticky_cleared"'
    - file:
        path: logs/auggie-first.jsonl
        exists: true
        contains: '"tool":"mcp__auggie-mcp__ask_question"'
    - exit_code:
        equals: 0
```

## Verification runs

Captured under `.dev/releases/current/cliEval/evidence/T05.04/`:

| File | Command | Outcome |
|---|---|---|
| `describe-E2.2.txt` | `uv run superclaude eval describe --suite real --eval E2.2` | exit 0; renders the new inputs/expects rows; proves manifest body is loadable and round-trips through `Expect.from_mapping`. |
| `coverage-map.txt` | `python -c "from superclaude.cli.eval.loader import SuiteLoader; …"` (same idiom as T05.03 evidence) | Lists `E2.2: covers ['mcp__auggie-mcp__.*']` alongside `E1` / `E2.1` for `mcp__auggie__.*`. Proves coverage-gate registration is wired correctly. |
| `run-E2.2-no-mcp.txt` | `uv run superclaude eval run --suite real --eval E2.2 --no-mcp` | Hits a pre-existing `NameError: name '_new_run_id' is not defined` in `cli/eval/commands.py:1418` — same failure observed and documented under `evidence/T05.03/run-E2.1-no-mcp.txt`. This is a runner-side bug not introduced by this deliverable; soft-skip behavior is *verified at the gate / capability layer* (capability decl present in `optional_capabilities` and the `requires:` tag references it), not via this run. Re-run is gated on the runner-fix follow-up. |

## Schema validation

The post-edit YAML loads cleanly under `SuiteLoader().load(...)`
(proof: `coverage-map.txt` succeeds — it parses every eval to compute
coverage). Each `expects[]` row has exactly one primitive key
(`file`, `file`, `exit_code`) which matches `PRIMITIVE_NAMES`
(`expect.py:56-64`). No `jsonschema` `additionalProperties: false`
violation; `eval describe` round-trips the body to YAML.

## Coverage gate evidence

Post-edit, `_iter_eval_tool_calls(spec_E2.2)` yields
`mcp__auggie-mcp__ask_question`, which matches the
`mcp__auggie-mcp__.*` branch of the PostToolUse matcher in
`src/superclaude/hooks/hooks.json:60` (regex compiled from
`_DEFAULT_MCP_TOOL_PREFIXES[1]` per `coverage.py:103-107`). E2.2
therefore registers as the sole covering eval for the
`mcp__auggie-mcp__` prefix at the time of this writing — confirmed
by the `coverage-map.txt` output:

```
=== All matchers ===
E1: covers ['mcp__auggie__.*']
E2.1: covers ['mcp__auggie__.*']
E2.2: covers ['mcp__auggie-mcp__.*']
```

E2.3 will land the `mcp__airis-mcp-gateway__auggie_.*` row under
T05.05 / D-0086, completing the v1 triad. The CP-P05-T01-T05
checkpoint (T05.06) verifies that all three rows present green
together.

## Pre-existing runner bug (not in scope for T05.04)

`uv run superclaude eval run --suite real --eval E2.2 --no-mcp` exits
1 with:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

This is the same failure documented in T05.03 evidence
(`run-E2.1-no-mcp.txt`) and is **not introduced** by D-0085. It
predates this deliverable; fixing it is the responsibility of the
runner-completion task that is already a Phase-5 dependency of the
CP-P05-T01-T05 checkpoint (T05.06). T05.04's acceptance criteria
(manifest body landed, FR-SCH2-valid id, matcher contract documented,
spec recorded) are met by the describe / coverage-map evidence above.
