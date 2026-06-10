# /sc:reflect — UC-2 Post Audit (mitigations 1–3)

**Mode:** post · **Depth:** standard → **Tier 1** (Rule 1 STOP) · **Verdict:** ✅ **PASS**
**Diff:** `HEAD` working tree — `commands.py` (+3/−3), `config.py` (+1/−1), plus the untracked `tests/cli/reflect/test_docs_cli_parity.py` (NEW, audited directly + via execution)
**Calibrated confidence:** 0.95 · **Citations:** 8 / 8 re-Read / **0 dropped** · **Promotion:** skipped (`--no-promote`)

## Intent → work map

The user authorized mitigations 1–3 from the post-#160 root-cause proposal:

| # | Intent | Delivered | Class |
|---|--------|-----------|-------|
| 1 | CLI⇆docs parity test | `tests/cli/reflect/test_docs_cli_parity.py` — 2 tests (flag-set parity + CLI-derived default coupling), both PASS | Authorized |
| 2 | Facts-sheet fan-out process memory | `feedback_doc_fanout_facts_sheet.md` + MEMORY.md pointer (outside repo, not in git diff) | Authorized |
| 3 | Fix upstream docstrings/help | `commands.py` ×3 help strings + `config.py` ×1 docstring | Authorized |

## Grounded findings (all changes correct)

- **`commands.py:110`** `--output` help `<sha>` → `<short-sha>` — matches `config.py` `head[:12]`. ✅ Grounded.
- **`commands.py:115`** `--allow-single-vendor` "Do not HALT" → "Do not flag DEGRADED (exit 11)" — matches `contract.py` `_degraded_reason` (single-vendor is a DEGRADED trigger) + `models.py:47` (DEGRADED=11, distinct from HALTED=10). ✅ Grounded.
- **`commands.py:131`** `--fix` "gate default --fix" → "Click default --no-fix; the O1/O2 gates pass --fix" — matches `default=False` at `commands.py:130`; removes the misleading source the CHANGELOG agent had copied (the C1 root cause). ✅ Grounded.
- **`config.py:149`** docstring `<sha>` → `<short-sha>` (`HEAD[:12]`) — matches the implementation at `config.py:212` and the inline comment at `config.py:207`. Corrects the imprecise docstring the guide had inherited (the C2 root cause). ✅ Grounded.
- **Parity test** — introspects `run.params` (Click source of truth) and asserts (a) the guide's option bullets == the CLI flag set (catches the `--executor-model` phantom-flag class, C5), and (b) the guide's stated defaults are CLI-derived (catches the `--fix` default mismatch class, C1). 2/2 pass. ✅ Grounded via execution.

## Verification triangle (default-on, UC-2)

- `uv run pytest tests/cli/reflect/` → **77 passed, 1 xfailed** (baseline was 75+1; +2 new parity tests, **zero regressions** in the prior 75).
- `ruff check` + `ruff format --check` on changed files → clean.

## Deviation taxonomy

| Class | Count | Detail |
|-------|-------|--------|
| Regression | **0** | No test broke; no spec criterion contradicted. |
| Drift | **0** | Every hunk maps to the authorized mitigation intent. |
| Necessary | **1** | The parity test's default-coupling deliberately **excludes** `--timeout` and `--output` (their effective defaults — 3600, the path template — are applied downstream in `config.py`, not as the Click default). Documented inline in the test docstring with rationale. |
| Authorized | (all of the above changes) | User explicitly requested mitigations 1–3. |

## Disposition

**PASS.** The mitigations are correctly implemented, grounded, and verification-green. The parity test is a durable regression guard for exactly the doc⇆code drift class that produced the 5 Augment comments; the help/docstring fixes remove the contaminated upstream sources so future docs can't re-inherit them. Nothing blocks commit.
