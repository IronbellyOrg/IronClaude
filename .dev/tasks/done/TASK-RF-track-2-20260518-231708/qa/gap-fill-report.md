# Track 2 Gap-Fill Report (FU-002 reflexion writer test pollution)

**Date**: 2026-05-18
**Trigger**: A.8 quality-gate finding — 5 issues (1 critical env-var contradiction, 3 important data drifts, 1 minor prose count).
**Files updated**: `research/01-file-inventory.md`, `research/02-test-fixtures.md`
**Verification method**: Direct `grep -rE` on `src/superclaude/` for env-var precedent; `grep -n "ReflexionPattern()" tests/unit/test_reflexion.py` for bypass count; `wc -l` / `ls | wc -l` for pollution baseline.

## Issues addressed

1. **CRITICAL — Env-var contradiction (`REFLEXION_OUTPUT_DIR` vs `SUPERCLAUDE_REFLEXION_MEMORY_DIR`)**: Resolved per precedent rule. `grep -rE 'os\.environ\.get\("SUPERCLAUDE_|os\.getenv\("SUPERCLAUDE_' src/superclaude/` returned **zero matches** — no `SUPERCLAUDE_*` namespace exists in `src/superclaude/cli/` or `src/superclaude/pm_agent/`. Per gap-fill rule, **canonical name is `REFLEXION_OUTPUT_DIR`**. Replaced every occurrence of `SUPERCLAUDE_REFLEXION_MEMORY_DIR` in `02-test-fixtures.md` (replace_all). Added "CANONICAL ENV-VAR NAME DECISION" block at top of `01-file-inventory.md` documenting the choice + evidence.

2. **IMPORTANT — Bypass count (was 6 of 8, actually 7 of 9)**: Re-verified via `grep -n "ReflexionPattern()" tests/unit/test_reflexion.py` → 7 matches at L17, L25, L39, L52, L73, L118, L165. Updated §2 root-cause prose, §4 rationale, and Summary in `02-test-fixtures.md` from "6 of 8" to "7 of 9" with explicit line citations.

3. **IMPORTANT — Pollution baseline drift (jsonl was cited 292 lines, actual 588)**: Re-measured `wc -l /config/workspace/IronClaude/docs/memory/solutions_learned.jsonl` → **588 lines**. `ls -1 docs/mistakes/ | wc -l` → 84 files (unchanged). Updated §2 §5 and Summary in `02-test-fixtures.md` with re-measured values + added a strong note that the regression test MUST use a **dynamic** pre-fix snapshot (not hard-coded numbers).

4. **IMPORTANT — Both files missing "Gaps and Questions"**: Appended structured Gaps sections to both `01-file-inventory.md` and `02-test-fixtures.md` listing OQ-1 (env-var name — resolved to `REFLEXION_OUTPUT_DIR`), OQ-2 (preserve cwd default — recommendation: YES), OQ-3 (Phase 1 baseline cleanse — recommendation: YES, include), OQ-4 (dynamic regression snapshot — confirmed).

5. **MINOR — L59 prose said "Eight tests total" but table shows 9 rows**: Fixed to "Nine tests total" in §2 of `02-test-fixtures.md`.

## Values used after re-verification

| Field | Old (research) | New (gap-fill 2026-05-18) |
|---|---|---|
| Env-var name | `REFLEXION_OUTPUT_DIR` (01) vs `SUPERCLAUDE_REFLEXION_MEMORY_DIR` (02) | `REFLEXION_OUTPUT_DIR` (both) |
| Bare-constructor count | 6 of 8 | 7 of 9 (L17, L25, L39, L52, L73, L118, L165) |
| `solutions_learned.jsonl` lines | 292 | 588 |
| `docs/mistakes/` file count | 84 | 84 (unchanged) |
| L59 prose | "Eight tests total" | "Nine tests total" |

## Sign-off

Track 2 research files are now internally consistent (one env-var name across both files) and quantitatively accurate as of 2026-05-18. The builder may consume `01-file-inventory.md` and `02-test-fixtures.md` directly. All four Open Questions are recommended-resolved; builder defaults documented in the Gaps sections.
