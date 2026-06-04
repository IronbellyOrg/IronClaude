# Boundary Decision — RESOLVED: Option P (Python-heavy / thin Haiku)

**Resolved:** 2026-06-03 (operator selection)
**Supersedes:** the PENDING state in `boundary-decision-PENDING.md`.

## Chosen layering

**Option P — the `cli/recommend/` Python module owns classify-dispatch-validate-commit;
the skill is a thin wrapper.**

### Hard reality under the anthropic-SDK ban (Constraint B)

The CLI process cannot spawn Agent subagents (only the Claude session can). So even
under "Python-heavy", the **Agent spawns must originate in SKILL.md prose**. Option P
therefore resolves concretely to:

| Operation | Owner | Where |
|---|---|---|
| Spawn Haiku classifier (Agent, `model: haiku`) | Claude session | SKILL.md (thin wrapper) |
| Load YAML, table scan, key-match | Python | `cli/recommend/` dispatch subcommand |
| `confidence_top2_delta < 0.10` ambiguity gate | Python | dispatch subcommand |
| `native_likely` short-circuit | Python (reads classifier output) | dispatch subcommand |
| source_hash validation Read + sha256 compare | Python (deterministic) | dispatch subcommand |
| Budget gate (>10K → cold) | Python | dispatch subcommand |
| Emit hot-hit recommendation via `prompt_envelope_template` | Python | dispatch subcommand |
| Telemetry append | Python | `telemetry append` subcommand |
| Spawn cold-path Haiku (Agent, condensed runbook) | Claude session | SKILL.md (thin wrapper) |
| Commit `cache_update` from cold path (atomic YAML write) | Python | `cache put` subcommand |
| `--eval` grading / aggregation / best_model / row patch | Python | Phase 5 eval modules |
| Spawn per-(model,run) eval Agents | Claude session | SKILL.md prose |

## Concrete implications for Steps 4.2–4.4

- **New CLI surface (this phase):** add a `recommend dispatch` subcommand to
  `cli/recommend/commands.py` plus a dispatch-logic module
  (`cli/recommend/dispatch.py`) implementing the ~150 LoC classify-dispatch-validate-
  commit core. It accepts the classifier output (`--key`, `--native-likely`, `--delta`)
  and the user request/cwd, performs the deterministic scan/validate/budget, and prints
  either the hot-hit recommendation (the row's `prompt_envelope_template` filled) or a
  structured `cache_miss: <reason>` so the skill knows to fall to the cold path.
- **Step 4.2 (hot path in SKILL.md):** the skill spawns ONE Haiku classifier Agent,
  then shells `Bash(uv run python -m superclaude.cli.recommend dispatch ...)`; on a
  `cache_miss` it proceeds to the cold path; the source_hash validation is the CLI's
  job (never a Haiku-computed hash). All 4 miss reasons (`miss_no_key`,
  `miss_low_confidence`, `miss_validation_stale`, `miss_budget_exceeded`) are handled by
  the CLI and route to the cold path; the 5th hot-path fall-through, `native` (from
  `native_likely` or a `native_fallback` row), exits without the cold path.
- **Step 4.3 (cold path in SKILL.md):** the skill spawns a SECOND Haiku Agent with the
  `COLD_PATH_RUNBOOK` as system context, receives `recommendation + cache_update`, and
  commits the update by shelling to `recommend cache put --row-json ...` (the parent/CLI
  commits because Haiku cannot write files).
- **Step 4.4:** add `--eval <mode>` to `/sc:recommend` command doc + revise "No other flags".

## Why the seam is documented carefully

The line-113 table-inlining is partly relaxed under Option P: the table lives in the
YAML the CLI loads, not inlined in the classifier prompt (the classifier only emits a
key; the CLI does the scan). The classifier prompt therefore needs the closed-enum KEY
LIST (already in `CLASSIFIER_PROMPT`) but not the full row table. This is the Option-P
round-trip the operator accepted.
