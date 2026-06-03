# QA Report — Task Integrity (Phase 4 Dispatch Wiring, Option P)

**Topic:** Phase 4 hot/cold dispatch wiring for sc-recommend (Option P — Python-heavy / thin Haiku)
**Date:** 2026-06-03
**Phase:** task-integrity
**Fix cycle:** 1 (of max 2)
**Gate type:** task-integrity, fix_authorization: true

---

## Overall Verdict: PASS (after 1 fix cycle)

The dispatch wiring is correct and consistent with Option P **after** a CRITICAL
round-trip defect was fixed in-place and re-verified by live CliRunner execution.
A pre-fix verdict would have been FAIL. All 8 acceptance criteria now hold against
the real files and real dispatch execution.

## Items Reviewed

| # | Acceptance Criterion | Result | Evidence |
|---|----------------------|--------|----------|
| 1 | Hot path spawns exactly ONE Haiku classifier in SKILL.md; scan/key-match/delta-gate/source_hash/budget live in `dispatch.py` (Python), not skill prose | PASS | SKILL.md L44 "Spawn exactly **one** `model: haiku` subagent"; the 8-step control flow is in `dispatch.py:74-135` (`dispatch()`), shelled via `recommend dispatch` (commands.py:202-251). SKILL.md L46-50 only shells the CLI. |
| 2 | All 5 cache-miss fall-throughs: 4 `miss_*` → cold path; `native` exits without cold path | PASS | Ran all 5 via CliRunner: `miss_no_key`(unknown + absent-row), `miss_low_confidence`(delta 0.05), `miss_validation_stale`(3 sub-cases), `miss_budget_exceeded`(20k>10k), and `native`(flag + `native_fallback` row). SKILL.md L53-55 interprets each; native has `needs_cold_path=false`. |
| 3 | source_hash validation deterministic in `dispatch.py` (Read source_path + `compute_source_hash` + compare), NOT Haiku-computed; mismatch → `miss_validation_stale` | PASS | `dispatch.py:114-122` Reads `row.source_path`, calls `compute_source_hash(src.read_bytes())`, compares to `row.source_hash`. Verified mismatch→`miss_validation_stale` via temp cache with bogus hash; also no-source_path and missing-file → same. All 4 seeded rows' source_hash MATCH live files (sha256 recomputed). |
| 4 | Cold path hands 2nd Haiku the `COLD_PATH_RUNBOOK` (not full SKILL.md); PARENT commits `cache_update` via `recommend cache put` → `LookupCache.save()` | PASS (post-fix) | SKILL.md L187 hands `COLD_PATH_RUNBOOK` (prompts.py:109) explicitly "**not** the full SKILL.md body". `cache put` (commands.py:78-) routes through `LookupCache.save()` (cache.py:113 atomic tmp+os.replace). **Round-trip was broken pre-fix (see Issues #1).** |
| 5 | Return-contract parity: hot-hit and cold path emit same Return Contract shape | PASS | SKILL.md Return Contract (L228-236, 7 fields) == COLD_PATH_RUNBOOK `<RETURN-CONTRACT>` (prompts.py:180-187, same 7 fields + `cache_update`). Both paths state "same Return Contract shape" (SKILL.md L57, L199). |
| 6 | R3 (no protocol reimplementation) preserved — emitted recommendation reuses row's `prompt_envelope_template`; no target protocol restated | PASS | Hit emits `row.prompt_envelope_template` verbatim (dispatch.py:132; CliRunner output is the hand-off `Run: /sc:spec-panel ... (Hand-off only ...)`). Runbook R3 restated (prompts.py:170-175). SKILL.md L57, L199 reaffirm. |
| 7 | `--eval` documented in recommend.md, opt-in default `none`, correct mode panels (quick=opus×1, normal=opus+sonnet×2, deep=opus+sonnet+haiku×3) | PASS | recommend.md L34 flag row matches exactly; "Auto-eval was rejected". commands.py:169 panel help string is byte-identical; `EVAL_MODES` (commands.py:31) = `[none,quick,normal,deep]`, default `none` (commands.py:168). |
| 8 | No `import anthropic` in `cli/recommend/`; `dispatch` subcommand imports cleanly and runs via CliRunner | PASS | `grep -rn "import anthropic\|from anthropic"` → 0 matches; only hit is the word in a docstring ("anthropic SDK is banned"). `anthropic` not in `sys.modules` after import. `dispatch --help` exit 0 with `--key`/`--native-likely`. All 5+native outcomes ran exit 0. |

## Summary

- Acceptance criteria passed: 8 / 8 (after fix)
- Criteria that would have FAILED pre-fix: 1 (AC#4 round-trip; AC#2/#3 hit-path functionally broken for every cold-inserted row)
- Critical issues found: 1 (fixed in-place)
- Minor issues: 1 (no durable test coverage for dispatch / cache-put — noted, not blocking this wiring gate)
- Issues fixed in-place: 1 CRITICAL (across 2 files + 1 doc-alignment)
- Existing recommend test suite: 17/17 PASS post-fix; ruff clean; verify-sync clean.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `cli/recommend/commands.py` `cache_put` (was L90-106) + `cli/recommend/prompts.py` `COLD_PATH_RUNBOOK` RETURN-CONTRACT (was L185-186) | **Cache never warms.** `cache put` did `upsert_row(row)` + `save()` with ZERO source_hash logic, contradicting SKILL.md L193's claim that "The CLI recomputes ... the full per-row `source_hash` on write." The runbook's `cache_update` contract also omitted `source_path`. Net effect: a cold-path insert wrote a row with no `source_path` and no `source_hash`, so the NEXT hot-path lookup of that key hit `dispatch.py:116/121` and returned `miss_validation_stale` **every time** — the 91K→5-10K amortization the cache exists for was defeated for all cold-inserted rows. Proven empirically: cold-insert → next dispatch = `miss_validation_stale`. | FIXED — see Actions Taken. |
| 2 | MINOR | `tests/recommend/` | No `test_dispatch.py` / `test_commands.py`: the dispatch 8-step flow and the new `cache put` source_hash recompute have no durable CI test. Verified here via ephemeral CliRunner scripts only. Recommend adding durable pytest coverage in a follow-up (not blocking this wiring gate). | Add `tests/recommend/test_dispatch.py` covering the 5 outcomes + the cold-insert→hot-hit round-trip. |

## Actions Taken

- **Fixed CRITICAL #1 (source_hash recompute on write):** rewrote `cache_put` in
  `src/superclaude/cli/recommend/commands.py` to deterministically (re)compute the
  per-row `source_hash` from `source_path` (Read + `compute_source_hash`) and stamp
  `last_validated_at` on write — consistent with Option P (hashing is the CLI's job,
  never Haiku's). It discards any Haiku-supplied `source_hash`, exempts
  `native_fallback` rows (no candidate source), and rejects non-native rows missing
  `source_path` with a clear error + exit 1.
- **Fixed CRITICAL #1 (runbook contract):** added `source_path` to the
  `COLD_PATH_RUNBOOK` `<RETURN-CONTRACT>` `cache_update` field list in
  `src/superclaude/cli/recommend/prompts.py`, with an explicit instruction that the
  Haiku supplies the Phase-0-Step-C path and does NOT compute source_hash. This
  aligns the runbook (the Haiku's authoritative system context) with SKILL.md L187,
  which already listed `source_path`.
- **Verified the fix by live CliRunner round-trip:** cold-insert row (with
  `source_path`, no `source_hash`) → `cache put` writes a 64-char `source_hash` +
  `last_validated_at` → the NEXT hot-path `dispatch` of that key now returns
  `outcome=hit` with the recommendation present (was `miss_validation_stale`
  pre-fix). Also verified: native_fallback exemption commits OK; bogus Haiku
  `source_hash` is discarded and recomputed; non-native row missing `source_path`
  is rejected.
- **Re-ran full outcome matrix** against the real seeded
  `.claude/cache/sc-recommend-lookup.yaml`: spec-generation→hit, codebase-research→hit,
  native→native. All 4 seeded rows' source_hash still MATCH live files.
- `uv run ruff check src/superclaude/cli/recommend/` → All checks passed.
- `uv run pytest tests/recommend/...` → 17 passed.
- `make sync-dev` + `make verify-sync` → All components in sync (SKILL.md change
  propagated; `cli/recommend/*.py` are non-synced Python in `src/` only — correct).

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 9 (CliRunner live dispatch
  across all 5 miss reasons + native + native_fallback + 3 stale sub-cases + round-trip
  + bogus-hash + missing-path + ruff + pytest + sync)
- All 8 acceptance criteria categorized [x] VERIFIED with cited tool output (file:line
  + CliRunner JSON). No item rests on agent claims — every outcome was executed.
- Tool-call count (23 verification calls) exceeds the 8-criterion minimum; no padding.

## Recommendations

- **Before proceeding past this gate:** none blocking — the CRITICAL defect is fixed
  and re-verified.
- **Follow-up (MINOR, non-blocking):** add `tests/recommend/test_dispatch.py` and a
  `cache put` source_hash round-trip test so the now-correct behavior is durable in CI
  (Issue #2). The wiring itself is correct.
- Note: the cross-file `cache_update` field-list consistency (SKILL.md L187 vs runbook)
  is now aligned; keep them in lockstep if the row schema changes.

## QA Complete
