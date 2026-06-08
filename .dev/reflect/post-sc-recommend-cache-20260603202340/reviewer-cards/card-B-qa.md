# Reviewer B Card — QA (sc-recommend lookup-cache POST-EXECUTION Audit)

**Date:** 2026-06-03
**Task:** TASK-RF-20260603-032936 (Option P: Python `cli/recommend/` owns deterministic dispatch; SKILL.md thin wrapper; anthropic SDK banned)
**Gold standard:** `.dev/brainstorms/sc-recommend-lookup-cache/merged-requirements.md`
**Reviewer:** B (qa persona), fix_authorization=false (diagnose only)

---

## Findings Table

| # | File:Line | Spec Section | Finding | Class | Rationale | Grounded |
|---|-----------|-------------|---------|-------|-----------|----------|
| 1 | `cache.py:52` | Spec lines 44-79 (row schema) | `compute_source_hash(path_bytes: bytes)` — parameter named `path_bytes` but receives file CONTENT bytes (`src.read_bytes()`), not a path. | DRIFT | Naming implies a path is hashed when actually content bytes are. No functional bug (both produce identical sha256), but the name is misleading for any future caller who passes a path string expecting it to be hashed. | `cache.py:52-58` vs `dispatch.py:121` (`compute_source_hash(src.read_bytes())`) |
| 2 | `commands/recommend.md:31-36` (Flags table) | Spec lines 224-277 (--eval flag) | `--eval` appears in the argument-hint line 8 (`[<goal description> [--plugin] [--eval <mode>]`) but is absent from the Flags table (rows only document `--plugin` and `--eval <mode>` in prose at line 34, not as a table row). | DRIFT | The table has two rows (plugin, eval) but the eval row is rendered as prose within the table cell rather than a distinct row entry. A reader scanning the table could miss the eval flag. The spec requires both flags to be clearly documented. | `commands/recommend.md:31-36` — eval flag is inline in the prose block under the table, not a dedicated `<td>` row |
| 3 | N/A (global) | Spec lines 290-308 (telemetry) | Telemetry writes exactly 5 fields (`ts, mode, cache_result, classification_key, duration_ms`) with a validated 6-value enum. `telemetry.py:17-29` matches spec exactly. | AUTHORIZED | No divergence. Implementation faithfully implements the spec. | `telemetry.py:17-29`, spec line 300 |
| 4 | `cache.py:113-150` | Spec line 412 (atomic write) | Atomic write via randomized tmp + `os.replace()` with `finally` cleanup on failure. Matches `convergence.py:DeviationRegistry` precedent exactly. | AUTHORIZED | No divergence. | `cache.py:113-150` |
| 5 | `commands.py:78-142` | Spec line 412 (cold-insert warm-up) | `cache put` recomputes `source_hash` on write (discards any Haiku-supplied hash, reads `source_path`, hashes content, stamps `last_validated_at`). Prevents the cold-insert→warm-to-stale bug. | AUTHORIZED | Matches spec: "the CLI's deterministic job, NOT the cold-path Haiku's." | `commands.py:117-136` |
| 6 | N/A (tests) | N/A | All 40 tests pass. `test_dispatch.py` covers the full dispatch hit/miss matrix (5 outcomes) AND the cold-insert→warm round-trip (cache put recomputes hash, dispatch then hits). No `assert True` — all assertions verify real behavior. | AUTHORIZED | Test quality is strong. | `tests/recommend/test_dispatch.py`, `uv run pytest tests/recommend/ -q` → 40 passed |
| 7 | `eval_aggregate.py:16-21` | Spec lines 230-235 (mode matrix) | `MODE_MATRIX` maps `none→[]x0`, `quick→[opus]x1`, `normal→[opus,sonnet]x2`, `deep→[opus,sonnet,haiku]x3`. Exact match to spec table. | AUTHORIZED | No divergence. | `eval_aggregate.py:16-21`, spec lines 230-235 |
| 8 | `plugin_eval.py:24-27,41-54` | Spec lines 280-288 (preconditions) | Reuses `install_mcp.check_mcp_server_installed` and `check_binary_available` (imported, not reimplemented). `failure_mode: hard` raises `PluginPreconditionError` (no degraded fallback). | AUTHORIZED | Matches spec: "reuse the install_mcp checks." | `plugin_eval.py:24-27`, `install_mcp.py:156,470` |
| 9 | `src/superclaude/cli/recommend/*.py` (all 12 modules) | Spec (anthropic ban) | `grep -rn "import anthropic" src/superclaude/cli/recommend/` — empty. Zero anthropic imports anywhere in the recommend package. | AUTHORIZED | Anthropic SDK ban enforced. | `grep` exit code 1 (no matches) |
| 10 | `cli/main.py:428,430` | Spec | `recommend_group` imported and added to `main` as `"recommend"`. CLI registration tests (5/5 pass) confirm `recommend` appears in `--help` with `cache`, `telemetry`, `eval`, `dispatch` subcommands. | AUTHORIZED | Registration complete. | `cli/main.py:428-430`, `uv run pytest tests/cli/test_cli_registration.py -q` → 5 passed |
| 11 | `.claude/cache/sc-recommend-lookup.yaml` (4 rows) | Spec lines 44-79 (row schema) | All 4 rows have all 9 required fields (key, candidate, flags, prompt_envelope_template, rationale, source_hash, last_validated_at, native_fallback, best_model). No extra fields. All source_hashes are 64-char valid hex. All flags verified against source files (spec-panel.md line 22, tasklist.md line 23). `best_model=null` on all rows (unevaluated, correct). | AUTHORIZED | Schema fidelity confirmed. | YAML parsed + `spec-panel.md:22`, `tasklist.md:23` |
| 12 | `.gitignore:119-126` | Spec lines 81-103 (Gitignore Exception) | Exact match: `!.claude/cache/`, `!.claude/cache/sc-recommend-lookup.yaml`, `!.claude/cache/sc-recommend-plugin.yaml`, `!.claude/cache/eval-runs/`, `!.claude/cache/eval-runs/**`, and `.claude/cache/sc-recommend-events.jsonl` (re-ignored). | AUTHORIZED | Byte-exact match to spec. | `.gitignore:119-126`, spec lines 87-101 |

---

## Deviation Counts by Class

| Class | Count |
|-------|-------|
| AUTHORIZED (no divergence) | 10 |
| NECESSARY | 0 |
| DRIFT | 2 |
| REGRESSION | 0 |

**Precedence applied:** REGRESSION > DRIFT > NECESSARY > AUTHORIZED. No regressions found.

---

## Test Pass/Fail Result

- `uv run pytest tests/recommend/ -q` → **40 passed in 0.22s** (6 test files)
- `uv run pytest tests/cli/test_cli_registration.py -q` → **5 passed in 0.15s**
- Total: **45/45 passed, 0 failures**
- Spot-checked 3+ tests for real assertions: `test_dispatch.py:119-157` (cold-insert→warm round-trip with actual hash recomputation + dispatch hit), `test_cache.py:111-139` (atomic-write crash simulation with patched `os.replace`), `test_best_model.py:83-94` (confidence suppression with near-identical fixtures). All assert real behavioral properties, none use `assert True`.
- Dispatch hit/miss matrix test: **present** (`test_dispatch.py` covers all 5 outcomes: hit, native, miss_no_key, miss_low_confidence, miss_validation_stale, miss_budget_exceeded).
- Cold-insert→warm round-trip test: **present** (`TestColdInsertWarmsToHit.test_cache_put_recomputes_source_hash_then_dispatch_hits`).

---

## Self-Reported Confidence: 0.95

**Evidence:** All 12 checklist items verified against real files using Read + Grep + Bash (pytest runs). 10 items showed zero divergence. 2 drift items identified (cosmetic naming, table formatting). No regressions found. No spec section was left unchecked. Confidence is 0.95 rather than 1.0 because the hot-path SKILL.md prose (Agent spawn orchestration) was not exhaustively verified against every sub-step of the spec's hot-path control flow — the Python surface was fully verified, but the skill-prose spawn sequence was sampled rather than line-by-line audited.

---

## One-Line Verdict

**PASS with 2 MINOR drift findings** — the implementation faithfully implements the spec's 12-step Implementation Order, schema, telemetry contract, atomic write, --eval pipeline, anthropic ban, and registration; the two drift items (parameter naming in `compute_source_hash`, eval flag placement in the command doc table) are cosmetic and do not affect runtime behavior.
