# QA Report — Task Integrity (Phase 2-3 Gate)

**Topic:** sc-recommend lookup-cache — classifier prompt, cold-path runbook, cache seed, foundation tests
**Date:** 2026-06-03
**Phase:** task-integrity
**Fix cycle:** N/A (cycle 1 — no fixes required)

---

## Overall Verdict: PASS

Zero-trust verification of all 4 acceptance criteria against the real files. Every
claim in the inventory was independently re-derived from source (digests recomputed,
flags re-read from command Usage lines, runbook diffed against SKILL.md, test suite
re-run). No fabrication, no drift, no fix required.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Classifier closed-enum + one-pass top-2 delta | PASS | `prompts.py:50-65` CLOSED-ENUM-KEYS block: "You may emit ONLY one of these keys… emit 'unknown'… Do NOT invent a key outside this set." `prompts.py:89-96` SCORING: "confidence_top2_delta = (top_score - runner_up_score)… computed in THIS single pass — do NOT make an extra LLM call." CLASSIFICATION_KEYS tuple (`:28-39`) is the 10-key closed enum (4 eval-backed + 6 surface-derived, flagged). |
| 2 | Cold-path runbook preserves all load-bearing guarantees, cites refs, no fabricated rules | PASS | Phase-0 gate A/B/C (`prompts.py:119-133`) maps to SKILL.md Step A/B/C. R1-R4 (`:165-178`) map to SKILL.md R1-R4; R3 "No protocol reimplementation (load-bearing)… Invoke, don't reimplement — duplication causes drift" matches SKILL.md `:174-181` near-verbatim. PHASE-1 native-first anti-bloat (`:144-151`) matches SKILL.md Phase 1. Graceful degradation (`:135-142`) covers all 4 SKILL.md cases. Return contract (`:180-187`) = the 7 SKILL.md fields + `cache_update` (legitimate writeback contract, not fabrication). Cites all 3 refs (surface-enumeration.md, delegation-vs-native-heuristics.md, plugin-ecosystem-sources.md) rather than inlining; all 3 ref files confirmed to exist. No rule fabricated beyond SKILL.md. |
| 3 | 4 seeded rows: flags VERIFIED, R3 envelopes, full-digest source_hash, schema 2, native_fallback false, best_model null | PASS | See "Per-row verification" below. spec-panel 5 flags match `commands/spec-panel.md:22` Usage + `:25` focus-enum line. tasklist 3 flags match `commands/tasklist.md:23` Usage. Two flag-less rows correct (skill/agent + native pattern). source_hash for spec-panel and tasklist recomputed via `sha256sum` = EXACT match to seeded values. All rows: `schema_version: 2`, `native_fallback: false`, `best_model: null`. Each `prompt_envelope_template` is a hand-off envelope ("Hand-off only — …owns its… logic"), no protocol restatement. |
| 4 | Foundation tests cover required areas + Phase 3 run all-passing | PASS | `tests/recommend/test_cache.py`: round-trip (`test_save_and_reload`), surface_hash invalidation (`test_surface_hash_invalidation_resets_rows`), full-digest (`test_source_hash_full_digest`, `test_surface_hash_is_full_digest`), atomic-write crash safety (`test_atomic_write_no_partial_on_crash` — patches `os.replace` to OSError, asserts original intact + no stray temp). `test_telemetry.py`: 5-field shape (`test_append_event_writes_exactly_five_fields`), 6-value enum (`test_invalid_cache_result_rejected` ×6 + `test_all_six_valid_cache_results_accepted`). RE-RAN `uv run pytest tests/recommend/ -v` → **17 passed, 0 failed, 0 skipped, 0.18s** — matches the Phase 3 summary's claimed 17/17 exactly. |

## Per-row verification (Criterion 3)

| Row | candidate | flags | source check |
|---|---|---|---|
| spec-generation | /sc:spec-panel | --mode / --experts / --focus / --iterations / --format | All 5 present in `spec-panel.md:22` Usage; `--focus` enum (requirements\|architecture\|testing\|compliance\|correctness) sourced from `:25`. No extra/fabricated flag. source_hash `655dd70…1bffd` = `sha256sum spec-panel.md` ✓ |
| codebase-research | tech-research skill (or deep-research agent…) | [] (flag-less) | Correctly flag-less — invoked by prompt envelope, not a flagged command. |
| tasklist-generation | /sc:tasklist (or task-builder) | <roadmap-path> / --spec / --output | All 3 present in `tasklist.md:23` Usage + Arguments table `:36-38`. No extra flag. source_hash `f3cd47a…ce052` = `sha256sum tasklist.md` ✓ |
| parallel-agent-fanout | parallel Agent fan-out | [] (flag-less) | Correctly flag-less — native harness pattern. Sourced from `refs/delegation-vs-native-heuristics.md:64` ("Special case — parallel agent fan-out… single message with multiple Agent tool calls"). Confirmed present at that line. |

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Issues Found

None.

## Actions Taken

No fixes applied — all criteria passed on cycle 1. Verification actions performed:
- Recomputed `sha256sum` of spec-panel.md and tasklist.md → both match seeded source_hash byte-for-byte.
- Re-read both command Usage lines → confirmed every seeded flag exists; no fabricated flag.
- Diffed COLD_PATH_RUNBOOK against SKILL.md Phase 0 / Phase 1 / R1-R4 / degradation / return contract → full fidelity, R3 near-verbatim, no invented rules.
- Confirmed all 3 cited ref files exist (refs are cited, not inlined).
- Re-ran the full `tests/recommend/` suite → 17/17 pass, matching the Phase 3 summary.
- Confirmed `__init__.py` is empty (correct package marker) and conftest fixtures are tmp_path-scoped (never touch real `.claude/cache/`).

## Recommendations

- Criterion-side: green light for the boundary-independent Phase 2-3 outputs.
- Out of scope for this gate (do NOT block on these): the inventory's HARD-HALT on Step 2.1 (Python-vs-skill-prose boundary) remains PENDING — Phase 4 (dispatch wiring) and Phase 5 (--eval + plugin eval) stay BLOCKED until a human selects Option H / P / Hybrid. This gate verified only the boundary-independent artifacts, which are sound.
- Note (informational, not a defect): keys 5-10 in CLASSIFICATION_KEYS are surface-derived and lack iteration-1 eval coverage; this is explicitly documented in the code comment (`prompts.py:23-27`) and flagged as Risk #1 — correctly surfaced, not hidden.

---

## Confidence Gate

- **Confidence:** "Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 11 | Grep: 0 | Glob: 0 | Bash: 3"

All 4 criteria marked [x] VERIFIED with cited tool output (Read of every in-scope
file + source files; Bash sha256sum digest recomputation; Bash pytest re-run).
Tool-call count (14) exceeds checklist-item count (4) — not suspect. No UNCHECKED,
no UNVERIFIABLE items. No web research performed (all claims were local/source-truth).

## QA Complete
