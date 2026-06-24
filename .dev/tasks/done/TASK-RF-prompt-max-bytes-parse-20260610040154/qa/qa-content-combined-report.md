# QA Report — task-qualitative (combined-content lens)

**Topic:** SUPERCLAUDE_PROMPT_MAX_BYTES env-parse coverage
**Date:** 2026-06-10
**Phase:** task-qualitative
**Lens:** combined-content (actionability + numbers/metrics + crossref-chain)
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: PASS

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | All 6 env-parse paths covered, none dropped | none | PASS | `TestPromptMaxBytesEnvParse` has exactly 6 methods (test L422-470). (a) non-integer `"16MB"` L422; (b) empty `""` L431; (c) `"0"` L440; (d) `"-1"` L447; (e) valid `"2048"` L454; (f) `None` L463. Branch routing confirmed by running helper directly — empty string routes through the int() ValueError branch, 0/-1 through the `<=0` branch. |
| 2 | caplog scoped to module logger + meaningful substrings | none | PASS | All 6 use `caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process")`. Substrings: `SUPERCLAUDE_PROMPT_MAX_BYTES` (a/b), `non-positive` (c/d). `rec.message` confirmed populated by pytest's LogCaptureHandler (tests pass). See Observation O-1 (level-scope vs record-filter nuance — informational, not a defect). |
| 3 | Default value consistent (no divergent magic number) | none | PASS | Helper `default: int = 16 * 1024 * 1024` (process.py L24); tests `_DEFAULT = 16 * 1024 * 1024` (test L420). Both resolve to 16777216 (verified by eval). No divergence. |
| 4 | Warning messages coherent, reference env var, distinguish non-integer vs non-positive | none | PASS | Non-integer msg (process.py L36): "Invalid SUPERCLAUDE_PROMPT_MAX_BYTES=%r (not an integer)". Non-positive msg (L44): "SUPERCLAUDE_PROMPT_MAX_BYTES=%d is non-positive". Distinct, coherent, both reference the var. Captured live: see Evidence E-1. |
| 5 | "No warning" cases assert ABSENCE of env-var warning, not just return value | none | PASS | Valid (L459-461) and None (L468-470) both assert `result == ...` AND `not any("SUPERCLAUDE_PROMPT_MAX_BYTES" in rec.message ...)`. Negative-assertion teeth confirmed: a leaked warning carrying the substring would flip the assertion to fail. |
| 6 | No test fabricates unimplemented behavior | none | PASS | Every assertion maps to live helper behavior: valid `"2048"`→2048 (verified), None→16777216 (verified), all four invalid inputs→16777216+warning (verified). No phantom return values, exceptions, or codepaths asserted. |

<!-- task-qualitative Axis column: closed set {AX-1..AX-5, none}.
     AX-1 Drift is INACTIVE this review (no BUILD_REQUEST.GOAL verbatim
     in spawn prompt and the task file body was not provided — only the
     inventory). drift-axis-inactive recorded in Summary block per spec.
     AX-2..AX-5 applied; all checks passed -> `none` on every row. -->

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status:
drift-axis-inactive

## Issues Found
None. (See Observation O-1 below — informational, sub-threshold, not an issue requiring remediation.)

## Observations (informational, not findings)
- **O-1 — caplog `logger=` is level-scope, not record-filter.** `caplog.at_level(..., logger="superclaude.pipeline.process")`
  sets the WARNING level on that named logger; it does NOT filter `caplog.records` to only that
  logger. The assertions rely on substring matching (`SUPERCLAUDE_PROMPT_MAX_BYTES` / `non-positive`)
  rather than `rec.name == "superclaude.pipeline.process"`. This is functionally correct here because
  the substrings are unique to this module and the tests exercise the helper in isolation (no other
  logger emits these tokens). Not a defect — recording only so the "scoped to the logger" framing in
  the verification request is understood precisely: level-scoped yes, record-filtered no, compensated
  by module-unique substrings.

## Evidence Trail
- **E-1 — Live branch + message capture** (`uv run python` against the worktree helper):
  - `'16MB'` -> 16777216 | "Invalid SUPERCLAUDE_PROMPT_MAX_BYTES='16MB' (not an integer); falling back to default 16777216 bytes."
  - `''`     -> 16777216 | "Invalid SUPERCLAUDE_PROMPT_MAX_BYTES='' (not an integer); ..."
  - `'0'`    -> 16777216 | "SUPERCLAUDE_PROMPT_MAX_BYTES=0 is non-positive; ..."
  - `'-1'`   -> 16777216 | "SUPERCLAUDE_PROMPT_MAX_BYTES=-1 is non-positive; ..."
  - `None`   -> 16777216 (no warning); `'2048'` -> 2048 (no warning).
- **E-2 — Test run:** `pytest TestPromptMaxBytesEnvParse` -> 6 passed in 0.13s.
- **E-3 — Mutation test (proves non-positive assertions have teeth):** deleted the `_log.warning(...)`
  call in the `value <= 0` branch -> `test_zero_*` and `test_negative_*` FAILED (`assert any("non-positive" ...)`
  -> False); restored helper, re-ran -> 6 passed; `git diff --stat` confirms only the legitimate PR
  delta (+32/-3) remains, no mutation residue.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was supplied in the spawn prompt; this is a standalone
combined-content review. Standalone behavior applied — no reliance on machine-verified structural
PASS items; every check below was independently verified with my own tool engagement (Read of both
worktree files, live Python execution of the helper, pytest run, and a mutation test).

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No Inherited Structural Verdict was provided; nothing was relied upon.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Env-parse path coverage — verified by reading test L413-470 + executing the helper against all 6 inputs (E-1) and confirming exactly 6 methods route to the correct branch.
- Default-value consistency — verified by reading process.py:24 + test:420 and evaluating `16*1024*1024 == 16777216` for both.
- Assertion teeth — verified by mutation test (E-3): removed the non-positive warning, observed `test_zero_*`/`test_negative_*` fail, then restored.

## Confidence Gate
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 (inventory, process.py, test_process_stdin.py) | Grep: 0 | Glob: 0 | Bash: 5 (logrecord probe, pytest run x2, branch/message capture, mutation+restore)
- No UNCHECKED items. No UNVERIFIABLE items. Tool-call count (8) >= checklist items (6).
- No web research performed (review is fully local-file-bound); Tavily not required.

## Self-Audit (Confidence questions)
1. Factual claims verified against source: all 6 — env-parse path coverage, caplog scoping, default-value consistency, message coherence, no-warning absence assertions, and no-fabrication — each confirmed by reading the worktree files AND live execution.
2. Files read: `qa/final-output-inventory.md`, `src/superclaude/cli/pipeline/process.py` (worktree), `tests/pipeline/test_process_stdin.py` (worktree).
3. Why trust a low/zero issue count: I did not stop at reading. I executed the helper directly against all 6 inputs (E-1), ran the test class (E-2), and ran a mutation test that PROVED the warning assertions fail when the warning is removed (E-3). The adversarial "5 errors" hunt actively probed: (i) `rec.message` population timing — found it requires formatting, then confirmed pytest's caplog populates it; (ii) non-integer/non-positive message discrimination — found the non-integer tests use a non-discriminating substring but confirmed the inputs pin the branch so it is sound; (iii) caplog logger level-scope vs record-filter — surfaced as O-1, sub-threshold. None rose to a CRITICAL/IMPORTANT/MINOR finding.
4. Web research: none performed; not applicable, so Tavily-first was not triggered.

## QA Complete

---

VERDICT: PASS

All 6 verification points pass with no CRITICAL/IMPORTANT/MINOR issues. One informational observation
(O-1: caplog `logger=` is level-scope not record-filter, compensated by module-unique substrings) is
recorded for precision but does not constitute a finding. Mutation testing confirms the warning
assertions are not trivially-passing.
