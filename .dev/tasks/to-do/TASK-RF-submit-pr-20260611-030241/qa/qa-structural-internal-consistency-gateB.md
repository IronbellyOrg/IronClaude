# QA Report — Phase Gate B (Lens: INTERNAL-CONSISTENCY)

**Topic:** sc:pr-submit final build — cross-file internal consistency
**Date:** 2026-06-11
**Phase:** report-validation (structural cross-file lens)
**Lens:** INTERNAL-CONSISTENCY
**Fix authorization:** false (report only)
**Adversarial stance:** Assumed ≥10 cross-file inconsistencies; cross-checked every pair with grep/python/import/test evidence.

---

## Overall Verdict: PASS

Every cross-file pair the manifest names was checked with tool evidence. Zero genuine inconsistencies found. Two items that *look* like mismatches on a surface read were proven to be intentional, documented adaptations (the primed/unprimed S4 constraint and the `S2B_VERIFY` identifier vs `"S2b_VERIFY"` value). The full 131-test suite passes, which is independent runtime corroboration that the artifacts are mutually consistent.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FSM states: `state-machine.md` vs `models.py` MonitorState | PASS | 19 MonitorState members; all 18 distinct `MonitorState.X` refs in fsm.py resolve to defined members (set difference = ∅). `runtime import` of all names OK. |
| 2 | Primed vs unprimed S4 (documented Key Constraint) | PASS | state-machine.md:15-17,32 retains `S4'_HALT_BEFORE_PUSH`; models.py:101 identifier is unprimed `S4_HALT_BEFORE_PUSH` (apostrophe occurs only in docstring lines 6,89 and the trailing `# spec` comment on line 101, NOT in any identifier). Matches the stated constraint exactly — NOT a finding. |
| 3 | `S2b_VERIFY` casing across ref / models / fsm | PASS | models.py:96 `S2B_VERIFY = "S2b_VERIFY"` — Python identifier uppercase-B, **string value** lowercase-b matches ref prose `S2b_VERIFY` (state-machine.md:27,65). fsm.py uses identifier `S2B_VERIFY` consistently (lines 592,593,595). No drift. |
| 4 | 33 event types: `models.py` vs `loop-guard.md` | PASS | models.py EventType = 33 members (no duplicate); loop-guard.md §11.3 listing = 33 unique tokens; set-symmetric-difference both directions = ∅. 32 §11.3 + `push_aborted_or_not_landed` (models.py:70) confirmed. |
| 5 | `run_log.py` validates events against the enum | PASS | run_log.py:35 `_VALID_EVENT_VALUES = frozenset(e.value for e in EventType)`; append() raises on non-member (lines 107-110), error text cites "33 §11.3 events". Single source = `models.EventType`. |
| 6 | 4 markers: `pyproject.toml` vs `@pytest.mark.*` usages | PASS | pyproject markers array contains loop_guard, autonomy, recovery, p0 (lines 140-143). tests/pr_submit usages: loop_guard×4, autonomy×7, recovery×15, p0×9. `loop` marker absent (grep `@pytest.mark.loop\b` → none). `integration`/`parametrize` are pre-existing/builtin, out of scope of the +4. |
| 7 | Route map: `severity-routing.md` vs `severity_router.py` | PASS | Router: Critical/High→`--depth deep --fix` (ROUTE_DEEP_FIX), Medium→`--fix` (ROUTE_FIX), Low/Nit→`report-only` (ROUTE_REPORT_ONLY) — route() lines 147-153. Ref table rows 41-45 identical mapping. |
| 8 | No `--depth quick --fix` anywhere | PASS | All occurrences in core + refs are negation/guard contexts only (router docstrings, the `STOP — never emit` ref note, and the `assert decision != "--depth quick --fix"` invariant guard at severity_router.py:155). No emitting code path produces it. |
| 9 | `__init__.py` re-exports vs test-body imports | PASS | `__all__` = 17 names. All names imported by tests from the package root resolve. The one flagged token `detection` (test_rate_limit.py:54 `from superclaude.pr_submit import detection`) is a **submodule import** (monkeypatches `detection._fetch_payload`), valid regardless of `__all__`; runtime import confirmed OK. Not a broken re-export. |
| 10 | 5 idempotency sets: `run_log.py` vs `loop-guard.md` | PASS | run_log.py IDEMPOTENCY_SETS = {processed_review_ids, processed_finding_ids, replied_comment_ids, resolved_thread_ids, pushed_commit_shas}; loop-guard.md §11.4 lists the identical 5. |
| 11 | `ROUTE_REPORT_ONLY` sentinel single-sourced (router→fsm) | PASS | Defined once at severity_router.py:56; fsm.py:27 imports it and consumes at fsm.py:392 (`route(f) != ROUTE_REPORT_ONLY`). No string-literal duplication / drift between filter and definition. |
| 12 | SKILL.md state references vs models | PASS | All S-/HALT-/TERMINAL- backtick state tokens in SKILL.md (de-primed) are members of MonitorState; orphan set = ∅. |
| 13 | Runtime corroboration: full suite | PASS | `uv run pytest tests/pr_submit/ -q` → **131 passed in 0.19s** (matches manifest's 131-passed claim). Cross-module wiring exercised end-to-end. |

## Summary

- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None. No state mismatch, no event-count drift, no marker mismatch, no broken re-export found. | — |

### Surface-read traps cleared (NOT findings)

These two were specifically interrogated because they look like inconsistencies on a fast read; both are intentional and documented:

1. **`S4_HALT_BEFORE_PUSH` (models) vs `S4'_HALT_BEFORE_PUSH` (refs)** — the documented Key Constraint (Python cannot have an apostrophe in an identifier). The prime survives only in prose/comments. Confirmed the enum identifier is unprimed and the ref prose primed, exactly as specified.
2. **`S2B_VERIFY` identifier vs `S2b_VERIFY` ref token** — the enum *value* string is `"S2b_VERIFY"` (lowercase b), matching the ref; only the Python attribute name is uppercase. fsm.py references the attribute consistently. No semantic drift.

## Confidence

Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 9 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 6 (each running targeted grep/python/uv per checklist item)

Tool-call count (15 Read+Bash invocations) ≥ 13 checklist items: review is not under-engaged. No web research performed (all claims are local-source-bound), so no Tavily/WebSearch lines apply.

## Recommendations

- Green light from the INTERNAL-CONSISTENCY lens. The five named cross-file contracts (FSM states, 33 events, 4 markers, route map, re-exports) plus the two derived contracts (5 idempotency sets, ROUTE_REPORT_ONLY single-source) are all mutually consistent and runtime-verified.

## QA Complete

## VERDICT: PASS
