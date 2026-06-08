# Phase 5 Eval-Pipeline Inventory

**Date:** 2026-06-03
**Boundary option:** Option P — Python owns grade/aggregate/select/write/patch; Agent fan-out is the skill's job.

## Eval-module files (`src/superclaude/cli/recommend/`)

| File | Contains | Spec / research anchor |
|---|---|---|
| `eval_grader.py` | Ported `check()` (5 assertion types: string_contains, string_not_contains, regex_match, regex_match_not, max_length_check) + `grade_run`/`grade_text` (grading.json shape) verbatim from `.dev` grader.py | research/03 §2 |
| `eval_aggregate.py` | `MODE_MATRIX` (none/quick/normal/deep panels), `make_run_record` (regrouped by `model`), ported `stats()`, `summarize()`, `aggregate_by_model()` | research/03 §2 + §4 |
| `best_model.py` | `select_best_model` — 4 deterministic tiers (quality/speed/cost/balanced) + 0.70 floor (speed/cost) + normalized confidence + `<0.5` suppression (model-agnostic); quality tie-break confidence from tokens | research/03 §4 (core R3, no precedent) |
| `eval_pipeline.py` | `collect_run_records` (grade per-(model,run) deliverables), `finalize_eval` (aggregate → select → write `row-<key>-results.json` → patch lookup row best_model + eval_history via atomic writer) | research/03 §4; research/04 §2.9 |
| `plugin_eval.py` | `run_preconditions` (reuses imported `install_mcp.check_mcp_server_installed`/`check_binary_available` + `Path.exists`; OQ2-RESOLVED HARD-BLOCK on `failure_mode: hard`, no degraded fallback); `evaluate_adoption` (+≥10pp OR −≤20% token, `must_not_regress: [pass_rate]`); `patch_plugin_row` (atomic writer → `.claude/cache/sc-recommend-plugin.yaml`) | research/02 §2; research/03 §5; round-4 124-135 |
| `commands.py::eval_run` | Wires the pipeline (collect + finalize) on `--mode != none` | research/04 §2.9 |

**Dispatch shim:** Option P's dispatch logic lives in `dispatch.py` (authored home), NOT a phantom `executor.py`. No subcommand imports a non-existent module (the lone "executor" hit is a docstring comment). No `import anthropic` anywhere.

## Eval-module tests (`tests/recommend/`)

| File | Tests | Covers |
|---|---|---|
| `test_best_model.py` | 8 | all 4 tiers, 0.70 floor + none-qualify suppression, quality tie-break confidence, balanced default, <0.5 suppression, based_on |
| `test_eval_pipeline.py` | 5 | 5 grader types, grade_text pass_rate, MODE_MATRIX, aggregate_by_model, finalize round-trip (results JSON + row patch) |
| `test_dispatch.py` | 7 | (Phase-4 hardening) 5 outcomes + cold-insert→warm-to-hit |

## Test gate

- `uv run pytest tests/recommend/` → **37 passed, 0 failed, exit 0**. Summary: `phase-outputs/test-results/phase5-pytest-summary.md`.

## Deferrals (logged in Phase 5 Findings)

- `generate_review.py` user-review-gate generator + Stage-1/2 synthetic-case generators: DEFERRED (confirmed-absent; ~250+ LoC Agent-orchestrated, out of scope for the core --eval/adoption path).
- Plugin-table per-row TTL invalidation: `patch_plugin_row` reuses the surface_hash-keyed `LookupCache` writer (satisfies 5.6); TTL-based per-row invalidation is a separate follow-up.

## Criteria mapping

- 5 grader assertion types ported faithfully (pure text over single markdown). ✓
- Aggregation re-grouped by model; MODE_MATRIX matches spec (quick=opus×1, normal=opus+sonnet×2, deep=opus+sonnet+haiku×3). ✓
- 4 best_model tiers + 70% floor + confidence-suppression implemented deterministically + unit-tested. ✓
- Plugin precondition reuses install_mcp checks + enforces OQ2-RESOLVED HARD-BLOCK. ✓
- Adoption gate threshold matches spec. ✓
- NO `import anthropic`. ✓ All eval-module tests pass. ✓
