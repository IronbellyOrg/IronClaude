# Phase 4 Dispatch Inventory

**Date:** 2026-06-03
**Boundary option implemented:** **Option P (Python-heavy / thin Haiku)** — see `phase-outputs/plans/boundary-resolved.md`.

## Edits & additions

| File | Change | Option-P role |
|---|---|---|
| `src/superclaude/cli/recommend/dispatch.py` (NEW, 135 lines) | Pure `dispatch()` + `DispatchResult`: native short-circuit → unknown/empty key → `confidence_top2_delta < 0.10` gate → table scan → `native_fallback` skip → source_hash validation (Read+sha256) → budget gate → HIT (emit `prompt_envelope_template` + best_model hint). No Agent spawn, no telemetry write, no cache write. | CLI owns the deterministic scan/validate/budget half of the hot path |
| `src/superclaude/cli/recommend/commands.py` | Added `recommend dispatch` subcommand (`--key/--native-likely/--delta/--cache-path/--budget-used/--budget-limit`) → prints JSON `DispatchResult` | The skill shells to this |
| `.claude/cache/sc-recommend-lookup.yaml` | Re-seeded with a `source_path` field per row (needed for deterministic Option-P source_hash validation); source_hash unchanged | data the dispatch validates against |
| `src/superclaude/skills/sc-recommend/SKILL.md` | Added "Hot-Path Cache Lookup" section (before Phase 0): spawn ONE Haiku classifier Agent → shell `recommend dispatch` → interpret hit/native/4-miss; and "Cold-Path Write-Back" section (after Phase 3): spawn 2nd Haiku with `COLD_PATH_RUNBOOK` → parent commits `cache_update` via `recommend cache put` → optional `--eval` → emit + telemetry | the skill (thin wrapper) owns ONLY the Agent spawns + interpretation |
| `src/superclaude/commands/recommend.md` | Added `--eval <mode>` flag-table row (opt-in default `none`; quick/normal/deep panels); revised "No other flags" → "`--plugin` and `--eval` are the only flags"; updated argument-hint + Usage | documents the opt-in eval surface |

## Verification (smoke-tested via CliRunner)

All 5 dispatch outcomes confirmed:
- HIT (spec-generation, delta 0.5) → `outcome: hit` + filled recommendation
- `miss_low_confidence` (delta 0.05)
- `miss_no_key` (key=unknown)
- `native` (`--native-likely`)
- `miss_budget_exceeded` (budget-used 20000 > 10000)

`ruff check src/superclaude/cli/recommend/` → clean.

## Criteria mapping

- Hot path spawns exactly ONE Haiku subagent (the classifier) — SKILL.md step 1.
- All 5 cache-miss fall-throughs handled: 4 `miss_*` (→ cold path) + `native` (→ native, no cold path).
- source_hash validated deterministically by the CLI (Read+sha256), never a Haiku-computed hash.
- Cold path uses `COLD_PATH_RUNBOOK` as the 2nd-Haiku system context, NOT the full SKILL.md.
- Parent commits `cache_update` via `recommend cache put` → `LookupCache.save()` atomic writer.
- Return-contract parity hot-vs-cold (both emit the same contract shape).
- R3 preserved: emitted recommendation reuses the row's hand-off envelope; no protocol restatement.
- `--eval` documented with opt-in default `none`.
