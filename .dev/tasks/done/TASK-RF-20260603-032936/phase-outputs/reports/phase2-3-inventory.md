# Phase 2-3 Inventory

**Date:** 2026-06-03
**Phases:** 2 (boundary decision + classifier + cold-path runbook + cache seed) and 3 (foundation tests)

## ⚠️ Boundary decision status: PENDING (HARD-HALT)

Step 2.1 (Python-vs-skill-prose boundary) is **PENDING** — documented + halted, no
option implemented. **Phase 4 (dispatch wiring) and Phase 5 (--eval + plugin eval)
remain BLOCKED** until a human selects Option H / Option P / Option Hybrid and returns
the frontmatter status to "🟠 Doing". Marker: `phase-outputs/plans/boundary-decision-PENDING.md`.

## Phase 2 outputs (boundary-independent)

| File | Contains | Spec / research anchor |
|---|---|---|
| `src/superclaude/cli/recommend/prompts.py::CLASSIFIER_PROMPT` | Closed-enum hot-path classifier prompt; emits ONLY an in-set key (else `unknown`→cache_miss:no_key); top-2 delta in one pass (no extra LLM call); `<RETURN>` JSON contract; few-shots from verbatim iteration-1 eval requests for the 4 eval-backed keys | research/02 §4, research/04 §2.4 + §3 |
| `src/superclaude/cli/recommend/prompts.py::CLASSIFICATION_KEYS` | The 10-key closed enum (4 eval-backed + 6 surface-derived); comment flags keys 5-10 lack iteration-1 eval coverage (need synthetic few-shots) | research/04 §3.2, §3.3 |
| `src/superclaude/cli/recommend/prompts.py::COLD_PATH_RUNBOOK` | ~50-line condensed cold-path pipeline (system context for cold-path Haiku); preserves Phase-0 gate (enumerate→auggie→verify), R1–R4 (R3 near-verbatim), native-first net-value, graceful degradation, return contract; cites the 3 refs rather than inlining | research/04 §1.8 (load-bearing vs cuttable) |
| `.claude/cache/sc-recommend-lookup.yaml` | schema_version 2 cache seeded via `LookupCache.save()` (atomic, not hand-authored); 4 eval-backed rows (spec-generation, codebase-research, tasklist-generation, parallel-agent-fanout) with VERIFIED flags, hand-off-envelope templates (R3), full 64-char source_hash, `native_fallback: false`, `best_model: null`; `sort_keys=False` field order preserved | research/04 §2.5 + §3.1 |

Seed script (handoff artifact): `phase-outputs/discovery/seed_cache.py`.

### Row flag verification (R1 — no fabricated flags)

| Row | candidate | flags source |
|---|---|---|
| spec-generation | /sc:spec-panel | `commands/spec-panel.md` Usage line (`--mode`, `--experts`, `--focus`, `--iterations`, `--format`) |
| codebase-research | tech-research skill / deep-research agent | flag-less (skill/agent invoked by prompt) |
| tasklist-generation | /sc:tasklist (or task-builder) | `commands/tasklist.md` Usage/Arguments (`<roadmap-path>`, `--spec`, `--output`) |
| parallel-agent-fanout | parallel Agent fan-out | flag-less (native harness pattern; source = `refs/delegation-vs-native-heuristics.md` line 64) |

## Phase 3 outputs (boundary-independent foundation tests)

| File | Contains | Anchor |
|---|---|---|
| `tests/recommend/__init__.py` | empty package marker (mirrors `tests/roadmap/__init__.py`) | research/06 §1.1 |
| `tests/recommend/conftest.py` | lean `cache_path` + `events_path` tmp_path fixtures | research/06 §1.1 |
| `tests/recommend/test_cache.py` | YAML round-trip, surface_hash invalidation, full-digest hashes, row ops, atomic-write crash safety | research/06 §1.3 |
| `tests/recommend/test_telemetry.py` | exact-5-field shape, line-oriented append, 6-value enum validation | research/04 §2.8 |

## Phase 3 test gate

- `uv run pytest tests/recommend/ -v` → **17 passed, 0 failed, exit 0** (0.30s). Summary: `phase-outputs/test-results/phase3-pytest-summary.md`.

## Verification notes for the gate

- Classifier enforces the closed-enum key set; top-2 delta computed in one pass (no extra LLM call).
- Condensed runbook preserves all 5 load-bearing guarantees; cites refs, does not fabricate rules beyond source SKILL.md.
- 4 seeded rows have VERIFIED flags from source files; hand-off-envelope templates (R3); full-digest source_hash.
- Foundation tests cover round-trip, surface_hash invalidation, atomic-write crash safety, telemetry 5-field shape — all pass.
