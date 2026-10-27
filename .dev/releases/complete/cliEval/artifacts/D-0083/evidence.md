# D-0083 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 42-49 (pre-edit), 42-67 (post-edit) | E1 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 186-265 (Expect.file), 269-369 (Expect.jsonl), 640-669 (from_mapping) | Primitive surface |
| `src/superclaude/cli/eval/coverage.py` | 227-258 | `_iter_eval_tool_calls` reads `inputs[].expect_tool_call` |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 22-32 (matcher branch), 25 (`if -f $STICKY`) | Hook contract — fires `sticky_cleared` IFF sticky pre-existed |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | full | Sibling resolution (E3-E15 body shapes) — establishes Expect.*-only constraint |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.02 block | Source task spec |

## Manifest delta

Pre-edit (`real.yaml:42-49`):

```yaml
- id: E1
  title: "auggie-first sticky lifecycle — set then clear"
  category: hook-lifecycle
  requires: [mcp_server.auggie]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
```

Post-edit (`real.yaml:42-67`):

```yaml
- id: E1
  title: "auggie-first sticky lifecycle — set then clear"
  category: hook-lifecycle
  requires: [mcp_server.auggie]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.02 / D-0083 — body shape. Hook contract (auggie-flag-clear.sh):
  # the PostToolUse hook ONLY emits `{"event":"sticky_cleared"}` to
  # logs/auggie-first.jsonl if state/auggie-first-pending/<sid>.txt
  # existed before the matched tool call. Asserting the JSONL event is
  # therefore a sufficient proxy for the "set then clear" lifecycle —
  # the literal file_absent(state/.../<sid>.txt) assertion is deferred
  # (needs session_id template substitution; see D-0083 §4).
  inputs:
    - prompt: "Use mcp__auggie__codebase-retrieval to summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."
      expect_tool_call: mcp__auggie__codebase-retrieval
  expects:
    - file:
        path: logs/auggie-first.jsonl
        exists: true
        contains: '"event":"sticky_cleared"'
    - exit_code:
          equals: 0
```

## Verification runs

See `.dev/releases/current/cliEval/evidence/T05.02/` for the captured
transcripts of:

- `uv run superclaude eval describe --suite real --eval E1` (manifest
  shape proof — inputs/expects rendered)
- `uv run superclaude eval run --suite real --eval E1 --no-mcp` (FR-CAP1
  soft-skip proof — SKIPPED with `skip_reason="--no-mcp"`)
- `uv run superclaude eval run --suite real --eval E1 --no-pty`
  (R-077 short-circuit proof — SKIPPED with `skip_reason="--no-pty"`)

Full E1 execution (`eval run --suite real --eval E1`) is gated on the
downstream PTY-prompt-injection wiring task; the design-spec / phase-5
plan makes this explicit and the verification command is recorded
here to capture the current observable.

## Schema validation

The post-edit YAML loads under `loader.validate_manifest` and round-
trips through `Expect.from_mapping` for each `expects[]` row. Each
row has exactly one primitive key (`file`, `exit_code`) which matches
`PRIMITIVE_NAMES` (`expect.py:56-64`). No `jsonschema`
`additionalProperties: false` violation.

## Coverage gate evidence

After the edit, `_iter_eval_tool_calls(spec_E1)` yields
`mcp__auggie__codebase-retrieval`, which matches the PostToolUse
`mcp__auggie__|mcp__auggie-mcp__|mcp__airis-mcp-gateway__auggie_`
matcher in `src/superclaude/hooks/hooks.json` (per D-0082 §3 hook
surface coverage map). E1 therefore registers as covering the
"auggie" branch of the PostToolUse hook.
