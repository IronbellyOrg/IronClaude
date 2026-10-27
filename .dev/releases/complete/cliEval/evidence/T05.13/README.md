# T05.13 Evidence — E8 PreToolUse serena matcher body

**Task:** T05.13 (Phase 5)
**Deliverable:** D-0092 (E8 body per OQ-2 resolution)
**Date:** 2026-05-20
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E8 entry)

## Evidence files

| File | Purpose |
|---|---|
| `describe-E8.txt` | `uv run superclaude eval describe --suite real --eval E8` output — proves the OQ-2-frozen body is rendered by the CLI. |
| `list-with-E8.txt` | `uv run superclaude eval list --json` output — proves the suite enumerates 17 evals (E1, E2.1-3, E3-E15 = 4+13). |
| `expect-roundtrip.txt` | Python round-trip of every `expects[]` row through `Expect.from_mapping` — proves declarative DSL resolution for all 5 assertions, plus suite-wide eval enumeration with capability tags. |

## Acceptance criteria mapping

T05.13 acceptance criteria (phase-5-tasklist.md:636-641):

| AC | Evidence |
|---|---|
| File `suites/real.yaml` contains entry `id: E8` matching the OQ-2 resolution | `describe-E8.txt` — title, requires, inputs, expects match D-0082 §4 row E8 |
| `uv run superclaude eval run --suite real --eval E8` exits 0 deterministically across 3 runs | Blocked by pre-existing runner `NameError` in `commands.py:1418` (documented in T05.07-T05.11 evidence and D-0092 §8); deferred to runner-completion task (CP-P05-T13-T17 dependency) |
| E8 outcome is reproducible across 3 consecutive runs | Determinism analysis in D-0092 §5; full run pending runner fix |
| Eval body runs against a freshly-isolated per-eval HOME (FR-ISO2) and does not read/write outside `EvalContext.scratch_root` | `isolation.home_strategy: ephemeral` (per `describe-E8.txt`); paths resolve via `_resolve_path` against ctx.home_path (D-0092 §6) |
| `TASKLIST_ROOT/artifacts/D-0092/spec.md` records the eval body summary | `artifacts/D-0092/spec.md` ✅ |

## Out-of-scope (deferred)

- Full `eval run --eval E8` PTY execution + 3-run determinism proof — blocked
  by runner `NameError` (pre-existing across T05.07..T05.11; tracked at
  CP-P05-T13-T17 / runner-completion task).
- `freshness-pre-edit.sh` telemetry update so the script emits to
  `logs/freshness.jsonl` with OQ-2 field names (`type`, `matcher`).
  Pre-existing gap shared with E6 / E7; one hook-script update unblocks
  all three sibling evals. See D-0092 §8.1.
- `mcp_server.serena` addition to `_DEFAULT_CAPABILITY_SPECS` for
  `eval doctor` probe coverage. Manifest declaration in
  `optional_capabilities` is sufficient for FR-CAP1 soft-skip with the
  default `PermissiveCapabilityResolver`; static-roster registration is
  a future capabilities task. See D-0092 §8.2.

## Source references

- OQ-2 resolution: `.dev/releases/current/cliEval/decisions.md` §"OQ-2 Resolution — E3..E15 eval body shapes frozen (T05.01)"
- Body shape source: `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` §4 row E8
- Sibling evals: D-0090 (E6 Edit), D-0091 (E7 Write)
- Manifest schema: `src/superclaude/cli/eval/suites/suite.schema.json`
- Expect primitives: `src/superclaude/cli/eval/expect.py`
- Hook script: `src/superclaude/hooks/scripts/freshness-pre-edit.sh`
- Hook routing: `src/superclaude/hooks/hooks.json` (PreToolUse matcher block)
