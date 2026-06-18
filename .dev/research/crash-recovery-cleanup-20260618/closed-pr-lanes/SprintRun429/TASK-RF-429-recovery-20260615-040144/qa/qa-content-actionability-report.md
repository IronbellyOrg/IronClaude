# QA Report — Content Actionability Lens (P6 / Phase 7)

**Verdict: PASS**

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery — nominator exclusion of provider-exhausted tasks
**Date:** 2026-06-18
**Phase:** task-qualitative (single content lens: actionability)
**Lens scope:** ONLY the actionability of `tests/sprint/test_rerun_tasks.py::TestProviderExhaustionNominationExclusion` — i.e., does the P6 exclusion test genuinely catch a broken exclusion, or is it vacuous?
**Fix authorization:** false (report-only; no files edited)

---

## Adversarial premise (assigned)

> "Assume the P6 exclusion test would pass even if the exclusion were broken (vacuous test). Find the vacuity; don't confirm."

**Result of the hunt: I could not make the test pass with a broken exclusion.** Every guard the test claims to pin is load-bearing — proven by mutation testing (remove the guard → the corresponding assertion fails). The test is NON-VACUOUS on all three sub-tests. Verdict is PASS *because* the adversarial attack failed, not because the code "looked fine."

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | select_default test writes realistic phase-N-result.json with both an exhausted + a clean recoverable task; excludes exhausted, nominates recoverable | PASS | `test_rerun_tasks.py:356-376` — writes `phase-3-result.json` with T03.01 (`fail_recoverable`, class `""`) + T03.02 (`fail_provider_exhausted`, class `provider_exhaustion`); asserts `select_default_recoverable_tasks(result_path) == ["T03.01"]` (:376). Realistic shape confirmed against `TaskResult.to_dict` nesting (`task.task_id`). |
| 1b | The non-vacuous fail_recoverable+provider_exhaustion case exists and the failure_class guard is what excludes it | PASS | `test_rerun_tasks.py:378-400` — T03.10 carries `status: "fail_recoverable"` AND `failure_class: "provider_exhaustion"`; asserts `== []` (:400). Production guard at `rerun_tasks.py:1188-1189`. **Mutation 1** (below) proves it is the guard, not the status filter, doing the work. |
| 2 | transcript-fallback test writes FAIL_TERMINAL + a 429/FAIL_PROVIDER_EXHAUSTED transcript, classifies distinctly, exclusion keeps terminal / drops exhausted | PASS | `test_rerun_tasks.py:403-451` — asserts `statuses["T03.20"] is FAIL_TERMINAL` (:442), `statuses["T03.21"] is FAIL_PROVIDER_EXHAUSTED` (:443), then `nominated == ["T03.20"]` (:451). **Mutations 2 & 3** prove both halves non-vacuous. |
| 3 | Tests use real production functions, not stubs | PASS | Imports at `test_rerun_tasks.py:42-55`: `select_default_recoverable_tasks`, `discover_failed_tasks_from_transcripts` imported directly from `superclaude.cli.sprint.rerun_tasks`. No mock/patch on either function in this class (patches in this file are confined to `TestRunOrchestration`, lines 548-554/585-590). The 429 classification flows through the real `_classify_transcript` → real `_provider_failure_from_text` (`monitor.py:291`). |

---

## Summary

- Checks passed: 4 / 4 (3 sub-tests + the "real functions not stubs" check)
- Checks failed: 0
- Critical issues: 0
- Vacuity defects found: 0
- Issues fixed in-place: 0 (report-only)

---

## Mutation evidence (zero-trust vacuity probes)

Each guard was removed/disabled in a working copy, the test class re-run, then reverted. A guard is **load-bearing** iff its removal makes a previously-green assertion go red.

| # | Mutation | Target | Result | Proves |
|---|----------|--------|--------|--------|
| M1 | Delete `if entry.get("failure_class") == "provider_exhaustion": continue` (`rerun_tasks.py:1188-1189`) | select_default class guard | `test_select_default_failure_class_guard...` FAILED — `+ ['T03.10']` wrongly nominated | The failure_class guard is the gate for the fail_recoverable+exhaustion case. **This is exactly the non-vacuous case the prompt asked me to confirm.** |
| M2 | Force the 429 branch (`rerun_tasks.py:592-605`) to never fire (`if False and ...`) | _classify_transcript 429 interception | `test_transcript_fallback...` FAILED — `T03.21` classified `FAIL_TERMINAL` not `FAIL_PROVIDER_EXHAUSTED` | The 429 body genuinely drives classification; the distinct-classification assertion is real. |
| M3 | Break the test's own exclusion predicate (`if st is not None` instead of `is not FAIL_PROVIDER_EXHAUSTED`, test:449) | exclusion-predicate assertion | `test_transcript_fallback...` FAILED — `nominated` = `['T03.20','T03.21']` | The `nominated == ["T03.20"]` assertion is the gate, not decoration. |
| M4 | Broaden status filter to accept `fail_provider_exhausted` AND remove class guard | select_default status path | `test_select_default_excludes...` FAILED — `+ ['T03.02']` | Test #1 catches a broken status filter; the realistic exhausted-task case is wired correctly. |

All four mutations reverted. **Post-revert integrity:** current `rerun_tasks.py` is byte-identical to the pre-mutation working-tree backup (`diff` clean, "no residue"); the test file matches its backup; the full class re-runs `3 passed in 0.15s`.

### Why the test is not vacuous — the trace the prompt requested

The prompt's own concern: "provider-exhausted status is `fail_provider_exhausted`, so removing the failure_class guard alone wouldn't change the select_default result." **Confirmed and handled.** Two distinct exclusion mechanisms exist and the test pins BOTH:

1. **Status filter** (`rerun_tasks.py:1180`): a normal provider-exhausted task has `status == "fail_provider_exhausted"`, already rejected by the `!= "fail_recoverable"` check. Test #1 (T03.02) pins this path; M4 proves it.
2. **failure_class guard** (`rerun_tasks.py:1188-1189`): the *hypothetical* coupling-break case — `status == "fail_recoverable"` but `failure_class == "provider_exhaustion"` — is excluded ONLY by this guard. Test #1b (T03.10) is the dedicated non-vacuous case; **M1 proves removing the guard alone flips the result** (T03.10 leaks). This is precisely the case the prompt asked me to confirm exists and is non-vacuous. ✓

For test #2/#3: `select_default` returns `[]` when a phase has only provider-exhausted failures (correct — status filter rejects them), so the realistic auto-nomination LEAK is the legacy transcript fallback (`discover_failed_tasks_from_transcripts` surfaces ALL non-PASS). The production caller filters it at `rerun_tasks.py:1468-1474` (`if _status is not TaskStatus.FAIL_PROVIDER_EXHAUSTED`). The test's inline `nominated` comprehension (test:446-450) mirrors that production predicate **byte-for-byte**. The mirrored caller `run_rerun_tasks` is live, not dead code — wired into the Click `rerun-tasks` command at `commands.py:849-904` (and the resume path at :523-526).

---

## Production-source corroboration (facts independently verified)

- `select_default_recoverable_tasks` status filter `rerun_tasks.py:1180` + class guard `:1188-1189` — read, confirmed.
- `_classify_transcript` 429 interception `rerun_tasks.py:592-605` returns `FAIL_PROVIDER_EXHAUSTED` (or `PASS_RECOVERED` for completed-before-overrun) — read, confirmed; shares the live detector core `_provider_failure_from_text`.
- Detector `monitor.py:291,320,323` keys on `is_error and api_error_status == 429`; `_RE_SINGLE_ACCOUNT` (`monitor.py:44`) matches `"would exceed your account's rate limit"` — the test #3 T03.21 body contains `api_error_status: 429`, `is_error: true`, and `"exceed your account's rate limit"`, so the branch fires non-vacuously.
- TaskStatus wire values `models.py:50-53`: `FAIL_RECOVERABLE = "fail_recoverable"`, `FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"`, `FAIL_TERMINAL = "fail"` — the test's JSON strings match the status filter; the test asserts against enum *members* (not `.value`), so `FAIL_TERMINAL.value == "fail"` (not `"fail_terminal"`) is harmless.
- Caller fallback exclusion `rerun_tasks.py:1459-1475` — read; predicate identical to the test mirror.

One observation (NOT a finding against this lens): the production caller's exclusion (`rerun_tasks.py:1468-1474`) is tested via an inline *mirror* comprehension, not by invoking `run_rerun_tasks` directly. The mirror is byte-identical and the caller is provably reachable, so the actionability of THIS lens is satisfied. A direct end-to-end test of the caller's fallback nomination would be a coverage *strengthening*, not a correctness gap — outside this lens's scope and explicitly not gated here.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 9 — both production function bodies; the 429 detector + its regex; the TaskStatus enum wire values; the caller fallback predicate; the Click command wiring; the test imports; plus 4 mutation-test executions that empirically falsify vacuity.
2. **Specific files read:** `tests/sprint/test_rerun_tasks.py` (full), `src/superclaude/cli/sprint/rerun_tasks.py` (lines 1-1314 across reads), `src/superclaude/cli/sprint/models.py` (TaskStatus), `src/superclaude/cli/sprint/monitor.py` (detector), `src/superclaude/cli/sprint/commands.py` (caller wiring), and the P6 aggregate manifest.
3. **If I found 0 vacuity defects, why should the user trust I checked?** Because I did not merely *read* the guards and pronounce them sufficient — I **deleted/disabled each guard in a working copy and observed the matching assertion fail** (M1-M4), then reverted and confirmed byte-clean restore. A vacuous test would have stayed green under mutation; all four went red on the exact assertion the lens cares about. The adversarial premise was actively pursued and falsified.
4. **Web research performed?** None — this lens is entirely local-file/source-bound. Tavily not invoked (not required); no fallback occurred.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | grep(via Bash): 3 | Glob: 0 | Bash: 8 (incl. 4 mutation runs + baseline + integrity checks)

(Axis column omitted — single-lens content review, not a full task-qualitative phase. No `## Inherited Structural Verdict` section was supplied in the spawn prompt, so the reliance-audit subsection is N/A for this scoped lens.)

## QA Complete
