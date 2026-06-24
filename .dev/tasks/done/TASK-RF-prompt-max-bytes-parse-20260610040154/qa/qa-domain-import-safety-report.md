# QA Report — Task Integrity (Domain Lens: Python module-import safety)

**Topic:** PROMPT_MAX_BYTES env parse — module-import safety
**Date:** 2026-06-10
**Phase:** task-integrity (domain lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Adversarial Stance

Assume there is STILL at least 1 import-time failure path. Goal: find it.

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No import-time path raises on bad env value | PASS | `process.py` L56-58: only module-level evaluation is `PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES"))`. The sole `int()` call (L33) lives inside the helper's `try` (L32-34). Read whole module: no other module-level `int(...)`/`os.environ` evaluation. Live repro: 8 env values (incl. `16MB`, `0`, `-5`, `  `, `1.5`, huge int, unset) all exit 0. |
| 2 | Helper never propagates ValueError/TypeError for ANY string | PASS | Branch trace: `None`→L31 return; `int(raw)` raise→`except (TypeError, ValueError)`→L41 return default; `value<=0`→L49 return default; else→L50 return value. No bare/un-caught path. Exhaustively probed 24 inputs (whitespace `" 16 "`/`"  "`/`"\t\n"`, unicode `１６`/`٤٢`, `+5`, `0x10`, `0b10`, `1.5`, `inf`, `nan`, 26-digit int, `1_000`, `" +0 "`): every case returned an int, ZERO raises. |
| 3 | Non-positive values cannot slip through as valid size | PASS | L42-49 guards `value <= 0`. Live: `"0"`,`"-1"`,`"-3"`,`"-999999"`,`"-5"`,`" +0 "` (parses to 0) → all default 16777216. |
| 4 | `ClaudeProcess.start()` contract: PROMPT_MAX_BYTES is int | PASS | L56 annotation preserved `: int`. Consumer `start()` L169 `len(prompt_bytes) > PROMPT_MAX_BYTES` (numeric compare) and L172 f-string — both satisfied by int. Repro asserted `isinstance(PROMPT_MAX_BYTES, int)` true for all env values. No consumer code touched (diff: process.py + test only). |
| 5 | Absent-var path → default | PASS | `os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")` (no default arg) returns `None` when unset → helper L30-31 returns default. Live repro env=UNSET → 16777216, exit 0. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Confidence Gate
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 1 | Glob: 0 | Bash: 2
- Each Bash call directly executed the helper / imported the module to verify specific checks (points 1-3,5 via the exhaustive probe; points 1,4,5 via the import+isinstance repro).

## Adversarial Probe — Attempts to Find an Escaping Raise
Searched specifically for inputs where Python's `int()` (the only operation that can raise) could escape the `try`:
- Unicode digits (`'１６'`→16, `'٤٢'`→42): parse to POSITIVE ints, returned as valid sizes — benign (a valid size), NOT an import-safety defect. The `try` still wraps the conversion.
- Underscore separators (`'1_000'`→1000), leading `+`, surrounding whitespace: all parsed inside the `try`.
- `int()` itself only raises `ValueError`/`TypeError`, both caught. No input produced an uncaught exception. `os.environ.get` with no default cannot raise. Module-level type annotation evaluation under `from __future__ import annotations` (L12) is a no-op string — cannot raise.

**Conclusion:** No remaining import-time failure path found despite targeted adversarial probing of 24 string inputs plus 8 live import invocations.

## Issues Found
None.

## Recommendations
- None. The core defect (bad `SUPERCLAUDE_PROMPT_MAX_BYTES` hard-failing module import) is fully resolved. Green light from the import-safety domain lens.

## QA Complete

---

VERDICT: PASS
