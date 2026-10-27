# D-0084 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 79-109 (post-edit) | E2.1 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 186-265 (Expect.file), 640-669 (from_mapping) | Primitive surface |
| `src/superclaude/cli/eval/coverage.py` | 99-107 (`_DEFAULT_MCP_TOOL_PREFIXES`), 227-258 (`_iter_eval_tool_calls`, `eval_covers_pattern`) | Coverage gate path |
| `src/superclaude/cli/eval/loader.py` | ~600 (`_expand_entry` docstring) | Confirms no `{{prefix}}` template substitution at v1 |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 22-32 (case branch), 25-30 (sticky→jsonl emit) | Hook contract — emits `sticky_cleared` + `tool=<TOOL_NAME>` IFF sticky pre-existed |
| `src/superclaude/hooks/hooks.json` | 60 | PostToolUse matcher registration `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*` |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | full | Sibling resolution — Expect.*-only constraint, soft-skip constraint |
| `.dev/releases/current/cliEval/artifacts/D-0083/spec.md` | full | Sibling deliverable (E1 body) — sticky-clear hook contract analysis |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.03 block (lines 103-150) | Source task spec |

## Manifest delta

Pre-edit (E2.1 scaffolding-only entry before T05.03):

```yaml
- id: E2.1
  title: "auggie matcher coverage — mcp__auggie__*"
  category: hook-coverage
  requires: [mcp_server.auggie]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # Body landed by T05.03 / D-0084. Scaffolding only before this task.
```

Post-edit (`real.yaml:79-109`):

```yaml
- id: E2.1
  title: "auggie matcher coverage — mcp__auggie__*"
  category: hook-coverage
  requires: [mcp_server.auggie]
  timeout_sec: 90
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.03 / D-0084 — body shape. E2.1 covers the `mcp__auggie__.*`
  # branch of the PostToolUse matcher (hooks.json) by issuing a real
  # `mcp__auggie__codebase-retrieval` call. The `auggie-flag-clear.sh`
  # hook (scripts/auggie-flag-clear.sh:22-32) records the matched tool
  # name in the `tool` field of the JSONL event when the sticky
  # pre-existed, so asserting `"tool":"mcp__auggie__codebase-retrieval"`
  # in `logs/auggie-first.jsonl` proves the matcher branch fired for
  # the `mcp__auggie__*` prefix specifically (vs. the sibling auggie-mcp
  # / airis-mcp-gateway prefixes covered by E2.2 / E2.3).
  inputs:
    - prompt: "Use mcp__auggie__codebase-retrieval to summarise the auggie-flag-clear hook in src/superclaude/hooks/scripts/."
      expect_tool_call: mcp__auggie__codebase-retrieval
  expects:
    - file:
        path: logs/auggie-first.jsonl
        exists: true
        contains: '"event":"sticky_cleared"'
    - file:
        path: logs/auggie-first.jsonl
        exists: true
        contains: '"tool":"mcp__auggie__codebase-retrieval"'
    - exit_code:
        equals: 0
```

## Verification runs

Captured under `.dev/releases/current/cliEval/evidence/T05.03/`:

| File | Command | Outcome |
|---|---|---|
| `describe-E2.1.txt` | `uv run superclaude eval describe --suite real --eval E2.1` | exit 0; renders the new inputs/expects rows; proves manifest body is loadable and round-trips through `Expect.from_mapping`. |
| `coverage-map.txt` | `python -c "from superclaude.cli.eval.loader import SuiteLoader; …"` (coverage enumeration idiom) | Lists `E1: covers ['mcp__auggie__.*']` and `E2.1: covers ['mcp__auggie__.*']` — proves coverage-gate registration is wired correctly for the `mcp__auggie__` prefix. |
| `run-E2.1-no-mcp.txt` | `uv run superclaude eval run --suite real --eval E2.1 --no-mcp` | Hits a pre-existing `NameError: name '_new_run_id' is not defined` in `cli/eval/commands.py:1418`. This is a runner-side bug not introduced by this deliverable; soft-skip behavior is *verified at the gate / capability layer* (capability decl present in `optional_capabilities` and the `requires:` tag references it), not via this run. Re-run is gated on the runner-fix follow-up. |

## Schema validation

The post-edit YAML loads cleanly under `SuiteLoader().load(...)`
(proof: `coverage-map.txt` succeeds — it parses every eval to compute
coverage). Each `expects[]` row has exactly one primitive key
(`file`, `file`, `exit_code`) which matches `PRIMITIVE_NAMES`
(`expect.py:56-64`). No `jsonschema` `additionalProperties: false`
violation; `eval describe` round-trips the body to YAML (see
`describe-E2.1.txt`).

## Coverage gate evidence

Post-edit, `_iter_eval_tool_calls(spec_E2.1)` yields
`mcp__auggie__codebase-retrieval`, which matches the
`mcp__auggie__.*` branch of the PostToolUse matcher in
`src/superclaude/hooks/hooks.json:60` (regex compiled from
`_DEFAULT_MCP_TOOL_PREFIXES[0]` per `coverage.py:103-107`). E2.1
therefore registers as a covering eval for the `mcp__auggie__`
prefix alongside E1 — confirmed by the `coverage-map.txt` output:

```
=== All matchers ===
E1: covers ['mcp__auggie__.*']
E2.1: covers ['mcp__auggie__.*']
```

E2.2 lands the `mcp__auggie-mcp__.*` row under T05.04 / D-0085;
E2.3 lands the `mcp__airis-mcp-gateway__auggie_.*` row under
T05.05 / D-0086. The CP-P05-T01-T05 checkpoint (T05.06) verifies
that all three rows present green together.

## Pre-existing runner bug (not in scope for T05.03)

`uv run superclaude eval run --suite real --eval E2.1 --no-mcp` exits
1 with:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

This failure is **not introduced** by D-0084; it predates this
deliverable and reproduces under E2.2 (D-0085 `evidence.md` §"Pre-
existing runner bug") and E1 alike. Fixing it is the responsibility
of the runner-completion task that is already a Phase-5 dependency
of the CP-P05-T01-T05 checkpoint (T05.06). T05.03's acceptance
criteria (manifest body landed, FR-SCH2-valid id, matcher contract
documented, spec recorded) are met by the describe / coverage-map
evidence above.
