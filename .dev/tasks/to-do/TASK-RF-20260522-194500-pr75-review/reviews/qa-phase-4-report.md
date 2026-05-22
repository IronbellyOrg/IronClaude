# QA Report — Phase 4 (Issue 3: executor_factory probe-and-discard)

**Topic:** PR #75 review — commands.py probe-and-discard remediation
**Date:** 2026-05-22
**Phase:** report-validation (adversarial fix-verification)
**Fix cycle:** N/A (first pass)
**Target file:** `src/superclaude/cli/eval/commands.py`

---

## Overall Verdict: PASS

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `_resolve_executor_factory` docstring extended with `produces_null_executor` rationale | PASS | Lines 1402-1406 contain the explicit explanation: "The returned factory is tagged with ``produces_null_executor = True`` so the one-shot WARNING probe in ``run_eval`` can classify it without instantiating an executor. Constructor side-effects in future real executors (PTY descriptors, helper threads, scratch dirs) would otherwise leak resources before orchestration starts." |
| 2 | `factory.produces_null_executor = True` tag set immediately before `return factory` | PASS | Line 1412: `factory.produces_null_executor = True  # type: ignore[attr-defined]` directly precedes `return factory` on line 1413. Inner function `factory` defined at 1409-1410. |
| 3 | WARNING block uses `getattr(...)` attribute introspection | PASS | Line 1889: `if getattr(executor_factory, "produces_null_executor", False) and not as_json:` — exact match to spec. |
| 4 | `_executor_probe = executor_factory()` removed | PASS | `grep -c _executor_probe commands.py` returns 0. Zero references anywhere in file. |
| 5 | `del _executor_probe` removed | PASS | `grep -c "del _executor_probe"` returns 0 (grep exits 1 = no matches). |
| 6 | `isinstance(_executor_probe, ...)` removed | PASS | `grep -c "isinstance(_executor_probe"` returns 0. |
| 7 | `click.echo(...)` WARNING content preserved verbatim | PASS | Lines 1890-1895 preserve the exact WARNING string: `"eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative."` plus `err=True`. |
| 8 | Comment block above `if getattr(...)` explains attribute introspection rationale | PASS | Lines 1880-1888 contain the rationale: "We classify by inspecting the ``produces_null_executor`` attribute the factory carries (set in ``_resolve_executor_factory``) rather than by calling ``executor_factory()`` and discarding the result. When M5 / M6 lands ``ClaudeProcessAdapter + PtyDriver`` the real executor's constructor will allocate PTY descriptors / helper threads / scratch dirs; instantiating-and-discarding here would leak those resources before per-spec orchestration even starts. Test monkeypatches that inject real executors simply won't set the attribute, so the WARNING correctly suppresses." Covers constructor side-effects (M5/M6 PTY) AND test monkeypatch contract — both required elements present. |
| 9 | FACTORY-TAG grep gate | PASS | `grep -c "factory.produces_null_executor = True" commands.py` = 1 |
| 10 | GETATTR grep gate | PASS | `grep -c 'getattr(executor_factory, "produces_null_executor", False)' commands.py` = 1 |
| 11 | PROBE-REMOVED grep gate | PASS | `grep -c "_executor_probe" commands.py` = 0 |
| 12 | DEL-PROBE-REMOVED grep gate | PASS | `grep -c "del _executor_probe" commands.py` = 0 |
| 13 | Forward-compatibility: monkeypatched factory without attr suppresses WARNING | PASS | `getattr(factory, "produces_null_executor", False)` returns `False` for any factory the tests inject that does NOT set this attribute. A real-executor-returning factory (no attr set) → `False` → `and not as_json` short-circuits → WARNING suppressed. Logic is correct. |
| 14 | Adversarial sweep: no stray `_executor_probe` remnants | PASS | Full-file grep of `_executor_probe` returns 0 hits. Only `_NullLifecycleExecutor` references remain (lines 1365, 1399, 1410, 1871, 1891) and all are legitimate (class def, docstring references, instantiation in factory, comment, WARNING string). |
| 15 | Type-ignore comment present on factory tag | PASS | Line 1412: `# type: ignore[attr-defined]` — required because attaching attributes to function objects triggers mypy attr-defined errors. |
| 16 | `--json` guard preserved on WARNING emission | PASS | `and not as_json` clause on line 1889 preserves machine-readable stdout discipline (matches preserved comment at lines 1876-1879). |

## Summary

- Checks passed: 16 / 16
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (no fixes needed — implementation is correct)

## Confidence

**Verified:** 16/16 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 3 | Grep: 5 (via Bash) | Glob: 0 | Bash: 2

Tool-call-to-check ratio: 10 tool calls / 16 checks. Several checks were verified from the same Read call (lines 1380-1430 and 1855-1910 each covered multiple checks), which is legitimate co-location verification (the relevant code occupies <60 lines total).

## Issues Found

None.

## Adversarial Probes Attempted

1. **Stale probe artifact hunt:** `grep -n "_executor_probe\|_NullLifecycleExecutor" commands.py` → only `_NullLifecycleExecutor` legitimate references survive. No probe variable, no `del`, no isinstance check.
2. **Docstring honesty check:** docstring at 1395-1407 claims the factory is "tagged with `produces_null_executor = True`" — verified that line 1412 actually does this. Docstring matches implementation.
3. **WARNING content verbatim check:** compared the WARNING string at 1891-1893 against the spec — "eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative." Preserved exactly, including em-dash and `err=True` keyword.
4. **Forward-compat reasoning:** walked through three scenarios:
   - (a) Default factory from `_resolve_executor_factory()` → has attr → `getattr` returns `True` → WARNING fires (correct).
   - (b) Test monkeypatch returns plain callable without attr → `getattr` returns default `False` → WARNING suppressed (correct).
   - (c) Future M5/M6 real-executor factory that explicitly sets `produces_null_executor = False` → `getattr` returns `False` → WARNING suppressed (correct).
   - All three branches behave correctly without instantiating an executor.
5. **`as_json` interaction:** `and not as_json` preserves prior `--json` cleanliness guarantee. No regression.

## Recommendations

None. Phase 4 implementation is correct and complete. Green light for Phase 5.

## QA Complete
