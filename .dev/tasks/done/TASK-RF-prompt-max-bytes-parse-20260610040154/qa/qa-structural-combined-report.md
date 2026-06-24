# QA Report — Task Integrity (Structural Combined)

**Topic:** prompt-max-bytes parse helper (PR #156)
**Date:** 2026-06-10
**Phase:** task-integrity
**Lens:** combined-structural (code-conformance + internal-consistency + evidence-quality)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Adversarial Stance

Assuming ≥5 structural errors exist until proven otherwise. Verifying each of the 7 criteria against the actual worktree files with tool evidence.

---

## Overall Verdict: PASS

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Helper placement (after `_log`, before `PROMPT_MAX_BYTES`) | PASS | `process.py` L21 `_log = logging.getLogger(...)`; helper def L24-50; `PROMPT_MAX_BYTES` assignment L56-58. Order is `_log` (21) → helper (24) → assignment (56). Correct. |
| 2 | No new imports added | PASS | `git show 3a2db5f0:...process.py` import block (L12-19) byte-identical to current (L12-19): `logging`, `os`, `signal`, `subprocess`, `Path`, `Callable`, `Optional`, plus `_log` L21. Helper uses only `Optional`, `int`, `_log`; all pre-existing. Test file base import block was `ClaudeProcess, PromptTooLargeForArgv`; diff added ONLY `_parse_prompt_max_bytes` to that tuple — `logging`, `caplog` (pytest fixture) already present. No new top-level imports either file. |
| 3 | `PROMPT_MAX_BYTES` still `int`; no redundant default at call site | PASS | L56 `PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(` — annotation `int` intact. L57 passes only `os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")` — single arg, no second `default=` positional/kwarg. The `16*1024*1024` default lives solely in helper signature L24. |
| 4 | Helper handles all 3 paths; `_log.warning` with `%`-args | PASS | L30-31 `None`→`return default`. L32-41 `int(raw)` in `try/except (TypeError, ValueError)`→`_log.warning("...%r...%d...", raw, default)`→`return default`. L42-49 `value <= 0`→`_log.warning("...%d...%d...", value, default)`→`return default`. L50 `return value`. All warnings use lazy `%`-style args (not f-strings). Exception tuple is exactly `(TypeError, ValueError)`. |
| 5 | Test imports helper from real path; concrete asserts; caplog scoped to `superclaude.pipeline.process` | PASS | L20-24 imports `_parse_prompt_max_bytes` from `superclaude.cli.pipeline.process` (the real module). All 6 methods in `TestPromptMaxBytesEnvParse` assert concrete values: `== self._DEFAULT` (L426,435,451,467), `== 2048` (L458), plus message/`non-positive`/negation assertions. No `assert True`/bare truthy (grep confirmed none). caplog scoped `logger="superclaude.pipeline.process"` at L424,433,442,449,456,465. NOTE: logger name (`superclaude.pipeline.process`) intentionally differs from module path (`superclaude.cli.pipeline.process`) because `_log` at L21 uses an explicit literal string, NOT `__name__` — so caplog scoping correctly matches the logger the helper actually emits to. Internally consistent. |
| 6 | No placeholder/TODO/FIXME; no leftover dead code | PASS | grep for `TODO\|FIXME\|XXX\|placeholder\|stub\|NotImplementedError` across both files → NONE FOUND. Old `int(os.environ.get(...))` bare assignment fully replaced by helper call (no orphaned expression at L56-58). `# Default 16 MiB` comment preserved L53-55. |
| 7 | `16 * 1024 * 1024` consistent, no divergent magic numbers | PASS | grep across both files: `process.py` L24 helper default `16 * 1024 * 1024`; test L420 `_DEFAULT = 16 * 1024 * 1024`. Identical form, identical value (16777216). No competing `16777216`, `16*1048576`, or differing literal anywhere. |

## Confidence Gate

- [x] 1 VERIFIED — Read process.py L21/24/56 + line-order inspection
- [x] 2 VERIFIED — `git show 3a2db5f0` base vs current import diff (both files)
- [x] 3 VERIFIED — Read L56-58 + grep for second-arg default
- [x] 4 VERIFIED — Read helper body L30-50
- [x] 5 VERIFIED — Read test L20-24, L413-470 + grep `assert True` + grep `logger=`
- [x] 6 VERIFIED — grep TODO/FIXME/placeholder (NONE) + Read L53-58
- [x] 7 VERIFIED — grep magic-number occurrences both files

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 9 (via Bash grep invocations) | Glob: 0 | Bash: 4

confidence = 7 / (7 - 0) * 100 = 100.0% — meets ≥95% threshold, UNCHECKED == 0 → eligible for PASS.

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Adversarial Self-Audit

The stance demanded I assume ≥5 errors. I actively hunted for:
- **New-import smuggling** — disproven by byte-identical base/current import diff via `git show`.
- **Redundant call-site default** (double-source-of-truth bug) — call site L57 passes exactly one arg.
- **`__name__` vs literal logger mismatch** — looked like a potential bug (logger string `superclaude.pipeline.process` ≠ module path `superclaude.cli.pipeline.process`), but L21 uses an explicit literal string so caplog scoping is correct and deliberate. NOT a defect.
- **f-string in logging call** (lazy-eval violation) — all warnings use `%`-style.
- **Off-by-one in `value <= 0` boundary** — `2048` test passes (positive), `0` and `-1` tests assert `non-positive` fallback. Boundary correct.
- **Divergent magic numbers** — identical `16 * 1024 * 1024` in both source default and test `_DEFAULT`.

No defects survived scrutiny. The change is structurally clean: surgical diff (+124/-18), single source of truth for the default, defensive 3-path parsing, durable test class with concrete assertions in the project test suite (`tests/pipeline/`), correct caplog scoping. The "0 issues" verdict is backed by 8 distinct tool invocations mapping 1:1 to the 7 criteria (with import-safety double-checked across both files).

## Issues Found

None.

## Actions Taken

None (fix_authorization: false — report-only).

## Recommendations

- Green light. The two changed files satisfy all 7 structural criteria. No remediation required before merge.

## QA Complete
