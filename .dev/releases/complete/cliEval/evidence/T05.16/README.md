# T05.16 Evidence — E11 SubagentStop hook body

**Task:** T05.16 (Phase 5)
**Deliverable:** D-0095 (E11 body per OQ-2 resolution)
**Date:** 2026-05-21
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E11 entry)

## Evidence files

| File | Purpose |
|---|---|
| `describe-E11.txt` | `uv run superclaude eval describe --suite real --eval E11` output — proves the OQ-2-frozen body is rendered by the CLI. |
| `list-with-E11.txt` | `uv run superclaude eval list --json` output — proves the suite enumerates 17 evals (E1, E2.1-3, E3-E15 = 4+13). |
| `list-default.txt` | `uv run superclaude eval list` plain output — sibling sanity check (suite registers, 17 evals). |
| `expect-roundtrip.txt` | Python round-trip of every `expects[]` row through `Expect.from_mapping` — proves declarative DSL resolution for all 3 assertions, plus suite-wide eval enumeration with capability tags. |

## Acceptance criteria mapping

T05.16 acceptance criteria (phase-5-tasklist.md:786-791):

| AC | Evidence |
|---|---|
| File `suites/real.yaml` contains entry `id: E11` matching the OQ-2 resolution | `describe-E11.txt` — title, category, inputs, expects match D-0082 §4 row E11 |
| `uv run superclaude eval run --suite real --eval E11` exits 0 deterministically across 3 runs | Blocked by pre-existing runner `NameError` in `commands.py:1418` (documented in T05.07-T05.15 evidence and D-0095 §8); deferred to runner-completion task (CP-P05-T13-T17 dependency) |
| E11 outcome is reproducible across 3 consecutive runs | Determinism analysis in D-0095 §5; full run pending runner fix |
| Eval body runs against a freshly-isolated per-eval HOME (FR-ISO2) and does not read/write outside `EvalContext.scratch_root` | `isolation.home_strategy: ephemeral` (per `describe-E11.txt`); paths resolve via `_resolve_path` against ctx.home_path (D-0095 §6); Explore sub-agent's glob runs under the per-eval HOME via the cwd default set by the PTY harness |
| `TASKLIST_ROOT/artifacts/D-0095/spec.md` records the eval body summary | `artifacts/D-0095/spec.md` ✅ |

## Out-of-scope (deferred)

- Full `eval run --eval E11` PTY execution + 3-run determinism proof — blocked
  by runner `NameError` (pre-existing across T05.07..T05.15; tracked at
  CP-P05-T13-T17 / runner-completion task).
- `freshness-subagent-stop.sh` telemetry update so the script emits to
  `logs/freshness.jsonl` with the OQ-2 field name (`type:"subagent_stop"`)
  instead of the current bare-integer decrement at
  `state/bg-agents/<sid>.txt`. Pre-existing gap; no sibling shares this
  script. See D-0095 §8.1.
- Strict `jsonl.event_count(logs/freshness.jsonl, type=subagent_start) ==
  jsonl.event_count(logs/freshness.jsonl, type=subagent_stop)` symmetry
  predicate — not expressible in declarative DSL; binary substring
  presence used as operational proxy (exact on the single-spawn input
  shape). See D-0095 §3 footnote.

## Source references

- OQ-2 resolution: `.dev/releases/current/cliEval/decisions.md` §"OQ-2 Resolution — E3..E15 eval body shapes frozen (T05.01)"
- Body shape source: `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` §4 row E11
- Sibling evals: D-0087 (E3), D-0088 (E4), D-0089 (E5), D-0090 (E6), D-0091 (E7), D-0092 (E8), D-0093 (E9)
- Paired eval: D-0094 (E10 SubagentStart) — T05.15
- Manifest schema: `src/superclaude/cli/eval/suites/suite.schema.json`
- Expect primitives: `src/superclaude/cli/eval/expect.py`
- Hook script: `src/superclaude/hooks/scripts/freshness-subagent-stop.sh`
- Hook routing: `src/superclaude/hooks/hooks.json` (SubagentStop block)
