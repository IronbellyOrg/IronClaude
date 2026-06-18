# Post-Completion Cross-Phase QA — Consolidated Findings (PC.3)

**Date:** 2026-06-18 · **6 lenses** (3 structural rf-qa + 3 content rf-qa-qualitative) on the FINAL integrated state.

**Fidelity gate:** Not applicable — code-modifying task derived from a behavior design spec, not a source-document-to-document transform (I21). No M4 fidelity gate required.

## Lens verdicts (cycle 1)

| Lens | Verdict (cycle 1) | Finding |
|------|-------------------|---------|
| structural template-conformance | PASS | 0 issues (13 checks; live import OK; tui dicts cover all 14 members). |
| structural internal-consistency | **FAIL** | **CRITICAL** per-task path never halts the sprint on provider-exhaustion. |
| structural completeness | PASS* | IMPORTANT: PC.2 tui fix had no render test. |
| content domain-accuracy | **FAIL** | Same CRITICAL root cause (rated IMPORTANT): per-task halt-UX dead. |
| content crossref-chain | **FAIL** | Same CRITICAL root cause: hand-off #5 dangling (per-task → SprintResult halt). |
| content actionability | **FAIL** | IMPORTANT: single-session retry+cap untested; MINOR: P6 events untested; MINOR: e2e persistence. |

**Consolidated cycle-1 verdict: FAIL** (3 lenses converged on one CRITICAL root cause + coverage gaps).

## Deduplicated findings

1. **[CRITICAL] Per-task path does not halt the sprint on provider-exhaustion.**
   `executor.py` per-task block (`if tasks:` … 1882-1917): set `status=PhaseStatus.ERROR`, derived `phase_result.halt_reason="provider_exhaustion"`, then **unconditionally `continue`d** — never setting `sprint_result.outcome=HALTED`/`halt_phase`. Consequences: (a) the sprint keeps running subsequent phases against an exhausted pool (no fast-path halt, spec §4); (b) `SprintResult._exhaustion_halt` gates on `halt_phase is not None`, so the P5 exhaustion-aware halt UX (`account_exhaustion_output` / model-switch `resume_command`) was DEAD on the per-task path — the realistic path (task transcripts are per-task). The single-session path was correct; only the per-task path was incomplete. Surfaced by 3 convergent lenses; missed by per-phase gates (they ran targeted subsets via the single-session path only).
2. **[IMPORTANT] Single-session SINGLE_ACCOUNT_LIMIT retry→cap→halt untested** (spec §6 single-session case) — mutation-proven (disabling the branch → 0 tests failed).
3. **[MINOR] P6 events (`write_session_reset`/`write_account_exhaustion_halt`) had no test.**
4. **[MINOR] PC.2 tui.py PROVIDER_EXHAUSTED mapping had no render test.**
5. **[MINOR] e2e single-session JSON persistence not asserted via the real `execute_sprint` path** (the cap test hand-built the PhaseResult).

## Fixes applied (executor as serialized fixer — see `phase-outputs/plans/final-fixes-applied.md`)

- **F1 (CRITICAL):** per-task block now sets a `_provider_exhausted` flag and, after the phase result is persisted, `if _provider_exhausted: sprint_result.outcome=HALTED; sprint_result.halt_phase=phase.number; break` (mirrors the single-session PROVIDER_EXHAUSTED halt); non-exhaustion outcomes keep the existing `continue`. `tui.py`/`executor.py` only.
- **F2 (CRITICAL guard):** `tests/sprint/test_executor.py::...test_execute_sprint_per_task_provider_exhaustion_halts_and_surfaces_ux` — drives `execute_sprint` over a task-bearing phase, asserts HALTED + halt_phase==1 + halt_reason + `account_exhaustion_output()` non-empty (would be "" before the fix) + the halt event emitted.
- **F3 (IMPORTANT + MINOR P6 events):** `...test_execute_sprint_single_session_single_account_retries_then_halts` — max_session_resets=2 + single-account 429 every attempt → retry then cap-halt; asserts PROVIDER_EXHAUSTED + `write_session_reset.call_count>=1` + `write_account_exhaustion_halt.call_count==1`. Covers the untested single-session retry branch AND the P6 events (both spawn paths' events now asserted, F2 covers per-task).
- **F4 (MINOR tui):** `tests/sprint/test_tui.py::...test_render_phase_table_provider_exhausted` — renders a PROVIDER_EXHAUSTED phase row, asserts no exception + `EXHAUSTED`.
- **F5 (MINOR e2e persistence):** the new F3 single-session test + F2 per-task test both drive the real `execute_sprint` path (which persists via `_write_phase_result_json`), and the existing exit-zero test asserts `provider_exhausted` in the result file — persistence now covered end-to-end.

## Post-fix verification (pre-agent)

- New/changed tests: 3 new pass; `tests/sprint/test_tui.py` 11 passed.
- Full `tests/sprint/` (minus 2 pre-existing e2e fileno failures): **1231 passed** (+3 vs pre-fix 1228). No regression.
- Changed files (`executor.py`, `tui.py`, `test_executor.py`, `test_tui.py`): ruff check + format clean.

→ Proceed to PG-style verification round (2 agents) to independently confirm.

## Verification round (fix cycle 1) — PASS

- **rf-qa (structural):** PASS, 10/10 checks. The CRITICAL fix sets HALTED + halt_phase + break gated ONLY on `_provider_exhausted` (executor.py:1927-1930), mirrors the single-session halt (2307-2310), `SprintOutcome` imported (:37), phase result still persisted before the halt. All 3 new tests real; `test_executor.py + test_tui.py` → 117 passed.
- **rf-qa-qualitative (content):** PASS. All 5 findings addressed; spec intent delivered (`_exhaustion_halt` gates on halt_phase+halt_reason → `account_exhaustion_output()` flips "" → non-empty); no over-correction (non-exhaustion failures still `continue`). 5-file target suite → 300 passed. **Mutation-proved** the per-task guard: neutering the F1 halt → the per-task test FAILS, then restored byte-identical.

**POST-COMPLETION GATE: PASS (fix cycle 1 of max 3).** The 3-cycle cap was not approached. Both verification verdicts PASS. Task may proceed to PC.4 (summary) → PC.5 (reflect gate) → PC.6 (Done).

(Cosmetic, non-blocking: the fix log's prose referenced the test class loosely; the actual class is `TestExecuteSprintIntegrationCoverage` — both agents located the tests correctly.)
