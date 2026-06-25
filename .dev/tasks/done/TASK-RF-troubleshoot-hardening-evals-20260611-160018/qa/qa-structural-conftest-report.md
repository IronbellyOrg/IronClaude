# QA Report — Structural Conftest Verification

**Topic:** Suite-local conftest fixtures (backtest harness + cli/eval) vs `_pollution_snapshot` guard
**Date:** 2026-06-12
**Phase:** task-integrity (structural conftest audit)
**Fix cycle:** N/A (report-only, `fix_authorization: false`)
**Stance:** ADVERSARIAL — assumed ≥5 errors present; hunted for them.

---

## Overall Verdict: PASS (with findings)

All four mandated checklist items are satisfied at the binary level. No
fixture writes under `docs/`, scratch dirs are uuid-unique with best-effort
`finally` teardown, `catch_rate_output_dir` is `tmp_path`-rooted, and
`from __future__ import annotations` is the first executable line in both
suite-local files. The verdict is **PASS** because none of the findings below
break a mandated criterion — but the adversarial pass DID surface real defects
(F1–F5) that should be fixed before this conftest is treated as a reference
template.

---

## Items Reviewed (mandated criteria)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Suite-local fixtures mint UNIQUE scratch dirs (uuid suffix) with `finally` teardown `shutil.rmtree(ignore_errors=True)` | PASS | `backtest/conftest.py:30` `f"backtest-replay-{uuid.uuid4().hex[:12]}"`; `:32-35` `try/finally` → `shutil.rmtree(root, ignore_errors=True)`. `cli/eval/conftest.py:34` `f"pytest-{uuid.uuid4().hex[:12]}"`; `:36-39` `try/finally` → `shutil.rmtree(root, ignore_errors=True)`. |
| 2 | `catch_rate_output_dir` is `tmp_path`-rooted and NEVER under `docs/` | PASS | `backtest/conftest.py:39` signature `(tmp_path: Path)`; `:46` `out = tmp_path / "catch-rate-out"`. No `docs/` segment. |
| 3 | `from __future__ import annotations` is the first line | PASS (qualified — see F4) | `backtest/conftest.py:8`; `cli/eval/conftest.py:15`. First *import/executable* statement in both; preceded only by the module docstring. |
| 4 | No fixture writes under `docs/`; teardown best-effort | PASS | grep `docs/` across both files → docstring mentions only (backtest lines 4,5,42,43); zero code paths build a `docs/`-rooted path. Both teardowns use `ignore_errors=True`. |

## Summary
- Checks passed: 4 / 4 (mandated criteria)
- Checks failed: 0
- Critical issues: 0
- Findings (non-blocking defects): 5 (IMPORTANT/MINOR)
- Issues fixed in-place: 0 (report-only)

## Issues Found (adversarial sweep — none break a mandated criterion)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| F1 | IMPORTANT | `backtest/conftest.py:19,39` and `cli/eval/conftest.py:25` | Return-type annotation on yield-fixtures is WRONG. `replay_scratch_root` and `allowlisted_output_dir` `yield` (generator fixtures) but are annotated `-> Path`. The correct annotation is `Iterator[Path]` / `Generator[Path, None, None]`. Not a runtime failure (pytest does not enforce fixture return types), but it is a real type defect that a strict mypy/pyright pass would flag, and it contradicts the file's own "yield … finally" semantics. `catch_rate_output_dir:39` correctly `return`s, so `-> Path` there is fine. | Change the two yield-fixtures to `-> Iterator[Path]` (add `from collections.abc import Iterator`). |
| F2 | IMPORTANT | `backtest/conftest.py:1-79` (whole file) vs root guard `tests/conftest.py:23-25,49-79` | DOCSTRING/COMMENT FACTUAL ERROR — overstated guard scope. Both the module docstring (`:4-5`) and the `catch_rate_output_dir` docstring (`:42-43`) claim `_pollution_snapshot` "fails the session on **any** `docs/` write." It does NOT. The guard at `tests/conftest.py:24-25` watches exactly two paths: `docs/mistakes/*.md` (file-name set) and `docs/memory/solutions_learned.jsonl` (byte size). A write to e.g. `docs/foo.md` or `docs/memory/other.json` would NOT be caught. The fixtures are still safe (they write nowhere near `docs/`), but the stated rationale is false and would mislead a future author into trusting a guard that is far narrower than described. | Reword to: "the `_pollution_snapshot` guard fails the session on writes to `docs/mistakes/` or `docs/memory/solutions_learned.jsonl`." Do not claim blanket `docs/` coverage. |
| F3 | MINOR | `cli/eval/conftest.py:34` and `backtest/conftest.py:30` | Scratch roots are NOT `tmp_path`-rooted; they live under the shared, non-per-test `/tmp/eval-runs/` and `tempfile.gettempdir()`. uuid suffix prevents collision, and `finally` teardown reaps them — but on a hard crash / SIGKILL between `mkdir` and teardown these leak persistently (pytest's `tmp_path` would be auto-reaped by pytest's own retention policy; these are not). For `allowlisted_output_dir` this is forced by the AC12 allowlist (`/tmp/eval-runs` is mandatory), so it is acceptable-by-constraint. For `replay_scratch_root` there is no such constraint — it could have used `tmp_path_factory` and did not. | For `replay_scratch_root`, prefer `tmp_path_factory.mktemp("backtest-replay")` so pytest manages retention; keeps uuid-style uniqueness for free. |
| F4 | MINOR | `backtest/conftest.py:8`; `cli/eval/conftest.py:15` | Criterion 3 wording ("first line") is satisfied only under the conventional reading "first statement after the module docstring." The literal first *line* of each file is the opening `"""` of the docstring. This is correct and idiomatic Python (a `__future__` import is only required to precede other code, and a docstring is permitted before it), so it PASSES — but flagging because an adversarial literalist reading of the criterion could be argued either way. No change needed. | None — documented for completeness. |
| F5 | MINOR | `backtest/conftest.py:30-31` | TOCTOU / reuse nit: `root.mkdir(parents=True, exist_ok=True)` uses `exist_ok=True` on a path that is supposed to be uuid-unique. If the directory already exists (astronomically unlikely, but the `exist_ok=True` silently tolerates it), a pre-existing dir's contents would be silently adopted and then `rmtree`'d in teardown — masking a collision rather than failing loud. `cli/eval/conftest.py:35` has the identical pattern. Low severity given 96-bit uuid entropy. | Optional: drop `exist_ok=True` (or assert non-existence) so a uuid collision fails loudly instead of silently reusing a dir. |

## Actions Taken
None — `fix_authorization: false`. No source file modified.

## Recommendations
- F2 is the highest-value fix: the false "any `docs/` write" claim is load-bearing documentation that future authors will trust. Correct it to name the two actually-guarded paths.
- F1 should be fixed if this file is held up as a template (the task docstring at `backtest/conftest.py:3` explicitly markets it as "Mirrors the `tests/cli/eval/conftest.py` convention" — both share the same annotation bug, so the bug will propagate).
- F3/F5 are hardening nits, optional.

## Confidence Gate

- **Confidence:** "Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 4 | Grep: 1 | Glob: 0 | Bash: 1"  (3 Read of source files + 1 Read of this report for the freshness hook; 1 Bash grep for `docs/` + annotation lines)
- All four mandated criteria verified with cited file:line tool output. The 5 findings are defects discovered ABOVE the mandated checklist (adversarial surplus), none of which flip a mandated criterion to FAIL.
- Tool-call count (6) ≥ mandated checklist items (4): not suspect.

## QA Complete
