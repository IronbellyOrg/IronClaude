# Phase 1 Foundation Inventory

**Date:** 2026-06-03
**Phase:** 1 — Preparation, Baseline & Boundary-Independent Foundation
**Boundary decision (Step 2.1):** not yet reached (Phase 2) — all Phase 1 work is boundary-INDEPENDENT.

## New Python module: `src/superclaude/cli/recommend/`

| File | Lines | Contains | Spec / research anchor |
|---|---|---|---|
| `__init__.py` | 20 | Lazy `__getattr__` exporting `recommend_group` + `__all__` | Mirrors `cli/tasklist/__init__.py` exactly (research/01 §3) |
| `commands.py` | 199 | `@click.group("recommend")` + `cache get/put`, `telemetry append`, `eval run` (stub) subcommands; deferred body imports to `.cache`/`.telemetry`; `--mode` constrained to `click.Choice(["none","quick","normal","deep"])` default `none` | Mirrors `cli/tasklist/commands.py` deferred-body-import idiom (research/01 §3.2, research/04 §2.9) |
| `models.py` | 40 | `RecommendConfig` dataclass — cache/plugin/telemetry/eval-runs `Path` fields, all defaulted (standalone, NOT extending `PipelineConfig`) | research/01 §3 (config dataclass convention; pipeline machinery optional) |
| `cache.py` | 150 | `LookupCache` dataclass: `load_or_create` (surface_hash reset + YAMLError guard), `save` (atomic randomized-tmp + os.replace + finally cleanup, `yaml.safe_dump` `sort_keys=False`/`default_flow_style=False`/`allow_unicode=True`), `get_row`/`upsert_row`; `compute_surface_hash` + `compute_source_hash` helpers (full sha256 digest) | research/02 §1b–1e (convergence.py atomic write), research/06 §1.3 (randomized tmp from install_hooks), research/04 §2.5/§2.7 (row schema, surface_hash defn) |
| `telemetry.py` | 62 | `append_event(path, *, mode, cache_result, classification_key, duration_ms)` — writes exactly 5 fields (`ts` stamped), validates `cache_result` against the closed 6-value `CACHE_RESULTS` frozenset (raises `ValueError` on invalid), newline-terminated append | research/04 §2.8 (telemetry contract + 6-value enum) |

## Edited files (boundary-independent prerequisites)

| File | Change | Anchor |
|---|---|---|
| `.gitignore` | Appended R3 tracked-cache exception block after line 118 (`!.claude/settings.json`): dir-negation `!.claude/cache/` FIRST, per-file YAML/eval-runs negations, then `.claude/cache/sc-recommend-events.jsonl` re-ignore LAST | research/06 §4.3, research/01 §2 (last-match-wins ordering) |
| `src/superclaude/skills/sc-recommend/SKILL.md` | `allowed-tools` line gained `Edit, Write, Agent, Task` (appended; existing tools/order preserved) | research/04 §1.1, research/07 D5 |

## Gates passed in Phase 1

- **Step 1.3 baseline `make verify-sync`:** exit 0 (CLEAN) — any later drift is task-introduced.
- **Step 1.11 lint + import:** `ruff check src/superclaude/cli/recommend/` exit 0; import of all 4 modules exit 0.

## Verification notes for the gate

- `cache.py` `save()` uses `yaml.safe_dump` with `sort_keys=False`, `default_flow_style=False`, `allow_unicode=True`, and a randomized same-dir temp name (`.<name>.tmp.<pid>.<id>`) with `finally` temp cleanup → satisfies atomic-write crash safety (Step 3.3 test target).
- `load_or_create` resets `rows` when stored `surface_hash != surface_hash` and guards `yaml.YAMLError` → fresh-create.
- `telemetry.append_event` writes exactly the 5 named fields and validates against the 6-value enum.
- `.gitignore` negation block ordering: dir-negation first, events-jsonl re-ignore last, placed after line 118; line-103 `.claude/cache/` left intact (overridden by later negation, last-match-wins).
- `allowed-tools` gained `Edit/Write/Agent/Task` (4 additions, no duplicates).
- Integrity hashes (`compute_surface_hash`, `compute_source_hash`) return the FULL 64-char sha256 hexdigest (not truncated).
