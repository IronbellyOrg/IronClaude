# T05.14 Evidence — E9 PostToolUse Read async hook body

**Task:** T05.14 (Phase 5)
**Deliverable:** D-0093 (E9 body per OQ-2 resolution)
**Date:** 2026-05-20
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E9 entry)

## Evidence files

| File | Purpose |
|---|---|
| `describe-E9.txt` | `uv run superclaude eval describe --suite real --eval E9` output — proves the OQ-2-frozen body is rendered by the CLI. |
| `list-with-E9.txt` | `uv run superclaude eval list --json` output — proves the suite enumerates 17 evals (E1, E2.1-3, E3-E15 = 4+13). |
| `list-default.txt` | `uv run superclaude eval list` plain output — sibling sanity check (suite registers, 17 evals). |
| `expect-roundtrip.txt` | Python round-trip of every `expects[]` row through `Expect.from_mapping` — proves declarative DSL resolution for all 3 assertions, plus suite-wide eval enumeration with capability tags. |

## Acceptance criteria mapping

T05.14 acceptance criteria (phase-5-tasklist.md:686-691):

| AC | Evidence |
|---|---|
| File `suites/real.yaml` contains entry `id: E9` matching the OQ-2 resolution | `describe-E9.txt` — title, category, inputs, expects match D-0082 §4 row E9 |
| `uv run superclaude eval run --suite real --eval E9` exits 0 deterministically across 3 runs | Blocked by pre-existing runner `NameError` in `commands.py:1418` (documented in T05.07-T05.13 evidence and D-0093 §8); deferred to runner-completion task (CP-P05-T13-T17 dependency) |
| E9 outcome is reproducible across 3 consecutive runs | Determinism analysis in D-0093 §5; full run pending runner fix |
| Eval body runs against a freshly-isolated per-eval HOME (FR-ISO2) and does not read/write outside `EvalContext.scratch_root` | `isolation.home_strategy: ephemeral` (per `describe-E9.txt`); paths resolve via `_resolve_path` against ctx.home_path (D-0093 §6); `fixture.txt` lives under per-eval HOME (notes.md "Why `fixture.txt`") |
| `TASKLIST_ROOT/artifacts/D-0093/spec.md` records the eval body summary | `artifacts/D-0093/spec.md` ✅ |

## Out-of-scope (deferred)

- Full `eval run --eval E9` PTY execution + 3-run determinism proof — blocked
  by runner `NameError` (pre-existing across T05.07..T05.13; tracked at
  CP-P05-T13-T17 / runner-completion task).
- `freshness-post-read.sh` telemetry update so the script emits to
  `logs/freshness.jsonl` with the OQ-2 field name (`type:"post_read"`).
  Pre-existing gap; no sibling shares this script. See D-0093 §8.1.
- Strict `duration.less_than(post_read_event_ts - read_complete_ts, 2.0)`
  intra-eval timestamp-delta assertion — not expressible in declarative
  DSL; binary substring presence used as operational proxy. See D-0093
  §3 footnote.

## Source references

- OQ-2 resolution: `.dev/releases/current/cliEval/decisions.md` §"OQ-2 Resolution — E3..E15 eval body shapes frozen (T05.01)"
- Body shape source: `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` §4 row E9
- Sibling evals: D-0087 (E3), D-0088 (E4), D-0089 (E5), D-0090 (E6), D-0091 (E7), D-0092 (E8)
- Manifest schema: `src/superclaude/cli/eval/suites/suite.schema.json`
- Expect primitives: `src/superclaude/cli/eval/expect.py`
- Hook script: `src/superclaude/hooks/scripts/freshness-post-read.sh`
- Hook routing: `src/superclaude/hooks/hooks.json` (PostToolUse Read matcher block)
