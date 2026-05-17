# Research Notes: PR3 — E741 + N806 + N811 + F811 manual renames

**Date:** 2026-05-17
**Scenario:** A (explicit)
**Depth Tier:** Standard (manual renames need per-occurrence judgment)
**Track Count:** 5 (this is track 3)
**Order:** PR1 → PR2 → PR3 → PR4 → PR5

---

## EXISTING_FILES

Manual-fix violation counts from CI log (`25979540639/76365604439`):
- E741 (ambiguous variable name): 11 occurrences
- N806 (variable in function should be lowercase): 20 occurrences
- N811 (constant imported as non-constant): 3 occurrences
- F811 (redefinition of unused name): 2 occurrences
- **Total manual fixes: 36**

Known E741 occurrences from BUILD_REQUEST (3 confirmed):
- `src/superclaude/cli/audit/budget.py:146` — `l.value for l in self.active_degradation_levels`
- `src/superclaude/cli/audit/budget.py:294` — `CAPABILITY_NAMES[l] for l in self._protected_levels`
- `src/superclaude/cli/audit/budget.py:350` — `len([l for l in self._effective_order if l in self._active])`

Other 8 E741 + 25 N806/N811/F811 occurrences — locations recoverable via `uv run ruff check src/ tests/ --select E741,N806,N811,F811` after PR1+PR2 merge (when most noise is gone).

## PATTERNS_AND_CONVENTIONS

- In `audit/budget.py`, `l` is shorthand for "level" (degradation level) — natural rename: `lvl` or `level`.
- N806 violations are typically `UPPERCASE` locals in functions; rename to `lowercase_with_underscores`.
- N811 violations are typically `from X import lowercase as UPPERCASE` aliases; either drop the alias or use lowercase.
- F811 (redefinition) requires deleting the earlier dead binding, not renaming.

## GAPS_AND_QUESTIONS

- **Whole-list discovery**: Other 8 E741 locations + N806/N811/F811 not enumerated upfront. The task file must include a "discovery" phase that runs `ruff check --select E741,N806,N811,F811` and produces the full per-rename list before executing.
- **Test coverage for budget.py**: NFR2 says "verify via test suite after each rename." Need to identify which tests cover `audit/budget.py` to scope verification. `tests/audit/test_budget.py` is the likely target; confirm in task.
- **Rename collisions**: Renaming `l` → `level` could shadow an outer-scope `level` variable. Each rename needs local inspection to ensure no shadowing.

## RECOMMENDED_OUTPUTS

- Branch: `fix/ci-rot-pr3-manual-renames`
- Single task file: `TASK-RF-track-3-20260517-032112.md`
- PR title: `fix(lint): rename ambiguous identifiers (E741) and naming-convention violations (N806/N811/F811)`

## SUGGESTED_PHASES

1. Preparation: confirm PR1+PR2 merged + branch from master + dev-deps install
2. Discovery: enumerate ALL E741/N806/N811/F811 occurrences with `ruff check --select E741,N806,N811,F811 --output-format=concise`
3. Execute renames: per-file rename + per-rename test verification (NFR2)
4. Final verify: `ruff check src/ tests/` exits 0; full test suite passes; `make verify-sync` clean
5. Commit + PR

## TEMPLATE_NOTES

- Template 02 (complex) — requires discovery before execute
- QA_GATE_REQUIREMENTS: PER_PHASE (after discovery, after each rename batch, final)
- VALIDATION_REQUIREMENTS: ruff check on the touched rules, full test suite, make verify-sync, behavioral test for budget.py (degradation levels still work)
- TESTING_REQUIREMENTS: UNIT (run existing test suite after each rename batch; NFR2 enforcement)

## AMBIGUITIES_FOR_USER

- Should N806/N811/F811 be a separate PR from E741? Decision: NO — all are "manual rename" mechanical class, bundling into one PR reduces overhead. If discovery reveals >40 total renames, escalate to splitting per NFR4.

---
**Status:** Complete
