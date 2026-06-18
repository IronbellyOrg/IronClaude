# QA Verification — Content/Behavioral Fix-Cycle Report

**Date:** 2026-06-18 · **Phase:** fix-cycle (content/behavioral verification) · **fix_authorization:** false (report-only)
**Scope:** Verify the 5 consolidated post-completion findings were addressed, the CRITICAL fix delivers spec intent, no over-correction, tests green.

---

## Overall Verdict: PASS

All 5 consolidated findings are addressed by non-vacuous fixes/tests; the CRITICAL fix delivers the spec intent (per-task provider-exhaustion now halts the sprint AND surfaces the P5 halt UX); no over-correction (halt strictly gated on `_provider_exhausted`); 300/300 target tests pass; the CRITICAL guard is mutation-proven non-vacuous.

---

## Finding-by-finding verification

| # | Finding (severity) | Fix claimed | Verified in source | Verdict |
|---|--------------------|-------------|--------------------|---------|
| 1 | Per-task path never halts on provider-exhaustion; P5 halt-UX dead (CRITICAL) | executor F1: HALTED+halt_phase+break; test F2 | `executor.py:1896-1930` — `_provider_exhausted` flag set in the `failure_class` scan (1896-1902); after persist, `if _provider_exhausted: outcome=HALTED; halt_phase=phase.number; break` (1927-1930). Mirrors single-session path `2307-2309`. Test exists `test_executor.py:535`. | ADDRESSED |
| 2 | Single-session SINGLE_ACCOUNT_LIMIT retry→cap→halt untested (IMPORTANT) | test F3 | `test_executor.py:609` drives real `execute_sprint`, `max_session_resets=2`, single-account 429 every attempt → asserts HALTED + halt_phase==1 + status PROVIDER_EXHAUSTED + `write_session_reset.call_count>=1`. | ADDRESSED |
| 3 | P6 events (`write_session_reset`/`write_account_exhaustion_halt`) untested (MINOR) | call-count asserts in F2+F3 | F2 asserts `logger.write_account_exhaustion_halt.called` (`test_executor.py:606`); F3 asserts `write_session_reset.call_count>=1` + `write_account_exhaustion_halt.call_count==1` (`676-677`). Both spawn paths covered. | ADDRESSED |
| 4 | PC.2 tui PROVIDER_EXHAUSTED mapping had no render test (MINOR) | test F4 | `test_tui.py:98` renders a real PROVIDER_EXHAUSTED phase row through `tui.update`+`_render_to_string`, asserts no raise + `"EXHAUSTED"` in output (KeyError regression guard). | ADDRESSED |
| 5 | e2e single-session JSON persistence not asserted via real path (MINOR) | F2+F3 drive real `execute_sprint` | Both F2 and F3 call the real `execute_sprint` (not hand-built PhaseResult); `_write_phase_result_json` runs on the per-task path (`executor.py:1916`). Persistence exercised end-to-end. | ADDRESSED |

---

## Spec-intent delivery (CRITICAL)

Confirmed the full causal chain that revives the dead P5 UX:

1. **Halt:** `executor.py:1927-1930` sets `outcome=HALTED` + `halt_phase=phase.number` + `break` — re-route is exhausted, only a model switch helps, so the sprint stops (spec §4 fast-path halt). Gated on `_provider_exhausted`.
2. **halt_reason:** set to `"provider_exhaustion"` at `executor.py:1899` (the loop preceding the halt).
3. **UX revival:** `SprintResult._exhaustion_halt` (`models.py:847-874`) gates on `halt_phase is not None` (858) AND `halt_reason == "provider_exhaustion"` (864). Before the fix `halt_phase` was None on the per-task path → returned None → `account_exhaustion_output()` returned `""` and the model-switch `resume_command()` was never surfaced. The fix sets both, so `_exhaustion_halt` now returns `(halt_task_id, exhausted_model)`.
4. **Test asserts it:** `test_executor.py:603` asserts `result.account_exhaustion_output() != ""` (the exact "" → non-empty transition), `604` asserts the exhausted model `claude-opus-4-8` appears in the block, `599-601` assert HALTED + halt_phase==1 + halt_reason.

Fixture `tests/sprint/fixtures/exhaustion/all_account_cooldown.jsonl` confirmed to carry `claude-opus-4-8` + "cooling down" content, so line-604's model assertion is meaningful (not a tautology).

**Non-vacuity (mutation proof):** Temporarily neutered the F1 halt (replaced `outcome=HALTED; halt_phase; break` with a no-op `pass; continue`) on a working-tree copy → `test_execute_sprint_per_task_provider_exhaustion_halts_and_surfaces_ux` **FAILED**. Restored the file byte-identical (`cmp` match, no `MUTATION` leftover, F1 lines intact at 1928-1930). The test genuinely guards the fix.

---

## No over-correction

The per-task halt fires **only** when `_provider_exhausted` is True, which is set **only** inside `if _tr.failure_class == "provider_exhaustion":` (`executor.py:1898`). Any other per-task failure outcome leaves `_provider_exhausted=False`, skips the halt block, and falls through to the pre-existing `continue` (`executor.py:1931`) — unchanged ERROR-and-keep-going semantics. No behavior change for non-exhaustion per-task failures. Only `executor.py` + `tui.py` + two test files touched; no `.claude/` paths.

---

## Test execution (item 4)

`uv run pytest tests/sprint/test_executor.py tests/sprint/test_tui.py tests/sprint/test_rerun_tasks.py tests/sprint/test_aienv.py tests/sprint/test_models.py -q`

```
300 passed in 4.59s
```

Re-run after the mutation/restore: **300 passed in 4.53s** (no residue). Named-test isolation run: the 3 new tests (`per_task_provider_exhaustion`, `single_account_retries`, `render_phase_table_provider_exhausted`) all PASSED. (Note: the consolidated log named the class `TestExecuteSprint`; the actual class is `TestExecuteSprintIntegrationCoverage` — cosmetic doc discrepancy, not a defect.)

---

## Self-Audit

**(a) Reliance list — structural items not re-checked:**
- Relied on the prior structural rf-qa lenses (template-conformance PASS, tui dicts cover all 14 members) for live-import/structural conformance.

**(b) Independent semantic/behavioral checks (tool-verified):**
- Read `executor.py:1820-1980` — confirmed F1 control-flow placement, flag gating, and mirror of single-session halt at `2307-2309`.
- Read `models.py:847-926` — confirmed `_exhaustion_halt`/`account_exhaustion_output`/`resume_command` gate on `halt_phase is not None` + `halt_reason`, the exact chain the fix revives.
- Read both integration tests + tui test in full — confirmed real `execute_sprint` drive, the `account_exhaustion_output() != ""` assertion, and P6 call-count asserts.
- Grep-verified all 5 fixtures exist and the cooldown fixture carries `claude-opus-4-8`.
- Ran the full target suite (300 passed) AND a mutation test proving the CRITICAL guard fails when the fix is reverted.

## Confidence

- **Confidence:** Verified: 5/5 findings + spec-intent + over-correction + suite | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 5 | Grep: 4 | Glob: 0 | Bash: 6
- No web research performed (entirely local-file/test-bound); Tavily fallback path not exercised.

## QA Complete
