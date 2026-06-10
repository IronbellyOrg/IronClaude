# QA Report — Operational Falsification Review (reflect-wrapper auto-fix tests)

**Topic:** reflect-wrapper AUTO-FIX evolution — do the tests actually falsify the safety properties they claim?
**Date:** 2026-06-10
**Phase:** task-qualitative (operational lens / adversarial)
**Fix cycle:** N/A (report only)
**Reviewer stance:** Adversarial — assume the tests rubber-stamp the happy path until proven otherwise.

---

## Overall Verdict: PASS (with ONE MINOR robustness gap, non-blocking to the safety claims)

All five operational questions resolve in the tests' favor under empirical falsification. The carve-out test is genuinely adversarial, the marker negative-control genuinely catches the truthiness bug, the call-count arithmetic matches the spec for N=2, and all nine §8 ACs are each covered by at least one test that fails on the corresponding regression. The one gap (Q2) is a test-design robustness note, not a falsification failure: the non-convergence test *does* assert exit 10 and *does* fail if the bound is removed — but it fails by **hanging** (caught only by an external timeout) rather than by a bounded assertion. That is a MINOR finding, documented below.

---

## Items Reviewed

| # | Operational question | Result | Evidence |
|---|----------------------|--------|----------|
| Q1 | AC-3 carve-out tests fail if a human-required contract were made auto-fixable? | PASS | `classify_fix` short-circuits human-required on each hard signal; tests assert `== "human-required"` per-row; making any branch auto-fixable flips the asserted string → test fails |
| Q2 | Non-convergence test PROVES termination (would hang/fail if bound removed)? | PASS w/ MINOR | Mutation probe: removing `if iteration > max_iters: break` → test HANGS (terminated at 30s, RC=143). It catches the regression, but via hang not assertion |
| Q3 | Marker negative-control catches a too-loose `bool(os.environ.get(...))` bug? | PASS | Mutation probe: `bool(os.environ.get(...))` → `test_marker_zero_does_not_suppress` AND `test_marker_two_does_not_suppress` both FAIL (2 failed, 3 passed) |
| Q4 | Call-count arithmetic matches spec `(iterations+1)` audits + `iterations` applies for N=2? | PASS | Spec §6 / contract §7. Test asserts `call_count == 5` for non-convergence (3 audits + 2 applies) and `== 3` for convergence (2 audits + 1 apply). Both match (N+1)+N |
| Q5 | Each of the nine §8 ACs covered by ≥1 test that fails on regression? | PASS | Full mapping below; 75 passed / 1 xfailed empirically |

---

## Empirical baseline

`uv run pytest tests/cli/reflect/ -q` → **75 passed, 1 xfailed** (the deliberate `test_layer_a` generator-side decouple, per your note — confirmed `strict=False` xfail at `test_no_nesting_guard.py:63-74`, not a gap).

Two source mutation probes were run and **both source files restored byte-identical** (`diff -q` clean after each).

---

## Per-AC falsification analysis

**AC-1 (marker self-suppress exit 0).** `test_marker_suppression.py`. `test_marker_one_suppresses_before_launch` asserts exit 0 + `ClaudeProcess` never constructed + message present. The guard lives in the **group callback** (`commands.py:69`), which fires at Click parse time *before* the `exists=True` arg validation — `test_marker_one_suppresses_since_moved_file` proves this with a `/no/such/...` path that still exits 0. **Falsifies:** if the guard moved into `run()`'s body, the since-moved test would hit Click's path validation and exit non-zero → fail. ✅

**AC-2 (auto-fixable + present path → /task + re-audit → exit 0).** `test_fix_loop.py::test_convergence_exit0_three_launches`. Asserts `Verdict.PASS`, `fix_converged True`, `fix_iterations == 1`, `call_count == 3`, apply launch `env_vars == {_MARKER: "1"}` AND `prompt.startswith("/task ")`, and the sidecar mirrors. **Falsifies:** drop the apply, or skip the re-audit, or fail to export the marker into the apply child → a different call_count / env_vars / verdict → fail. ✅

**AC-3 (regression/needs_human/user_decision/non-empty gaps → terminal HALT, no /task, no promote).** Two layers:
- *Pure unit* `test_classify_fix.py`: one row per §3 trigger. `test_regression_present_is_human_required`, `test_needs_human_decision_is_human_required`, `test_user_decision_required_is_human_required`, `test_unauthorized_deviation_is_human_required`, `test_regression_count_is_human_required`, and the critical `test_mixed_drift_and_regression_human_wins` (drift=3 AND regression=1 → human-required, proving "solely drift/necessary" is enforced, not "drift present anywhere").
- *e2e* `test_fix_loop.py::test_human_required_halts_no_apply`: `needs_human_decision` fixture → `Verdict.HALTED`, exit 10, `call_count == 1` (NO apply), `fix_iterations == 0`.

**Is the carve-out test ADVERSARIAL (would it fail if someone made a human-required contract auto-fixable)?** YES. `classify_fix` (contract.py:356-366) short-circuits `human-required` on ANY hard signal *before* the `auto-fixable` branch. The unit tests assert the exact string `"human-required"` per row. If a maintainer accidentally moved (e.g.) `regression_present` out of the human-required disjunction, `test_regression_present_is_human_required` would observe `"auto-fixable"` ≠ `"human-required"` → FAIL. The mixed-row test specifically defends the "solely" semantics — a naive `if drift>0: return auto-fixable` ordering would flip it. This is not happy-path assertion; it pins the dangerous direction (the `feedback_human_decision_items_must_halt` invariant). Note on grounding-gaps: the wrapper does NOT re-parse `grounding-gaps.yaml`; it relies on reflect's contract guarantee that `needs_human_decision is True` IFF gaps non-empty (documented load-bearing invariant, contract.py:346-354). The test correctly exercises the surfaced boolean, which is the only signal the wrapper sees — appropriate given the thinness boundary. ✅

**AC-4 (non-convergence after max → exit 10, fix_converged: false).** `test_non_convergence_exit10_five_launches`: 5-step sequence all returning `autofixable_drift.yaml`, `max_fix_iterations=2` → `Verdict.HALTED`, exit 10, `fix_converged False`, `fix_iterations == 2`, `call_count == 5`.

**Does it PROVE termination?** Empirically yes — and I falsified it. Mutation probe: neutralizing `if iteration > max_iters: break` (runner.py:558-559) caused the test to **hang** (the sequence factory defaults to `(None,0)` past exhaustion → audit returns no contract → BLOCKED, but with the bound gone the loop only breaks on non-HALTED... actually the loop runs forever re-auditing; `timeout 30` Terminated, RC=143). So the test *does* catch a removed bound — the suite would not pass with an unbounded loop. **MINOR gap:** it catches it by hanging, not by a fast assertion. A genuinely bound-proving test would cap iterations structurally (e.g. assert the loop cannot exceed `max+1` audits even if every audit stays HALTED, which the `call_count == 5` assertion *does* encode when the bound is present). The `call_count == 5` assertion is the real termination proof: it pins exactly `(N+1)` audits, so an off-by-one or removed bound changes the count. The hang only manifests under the *removed*-bound mutation because the sequence is finite-then-default; under CI the bound is present and the count assertion fires. Net: termination IS proven for the in-tree code; the test is just not hang-proof under a hostile mutation. Non-blocking. ✅ (with MINOR note)

**AC-5 (O1 promote default; O2 --no-promote → exit 0 verified-not-promoted).** `test_promote_plumbing.py`. `test_o1_default_prompt_omits_no_promote` (promote=True → prompt has no `--no-promote`), `test_o2_no_promote_prompt_contains_no_promote`, and `test_default_promote_is_on_regression_guard` (bare CLI `run <file>` → no `--no-promote` in printed prompt, pinning the FR-5 default flip). Correctly scoped to prompt-plumbing, not the reflect-internal Wave-7 dir move (thinness boundary, contract §5). **Falsifies:** flip the `--promote` default back to False → the regression-guard test sees `--no-promote` emitted → fail. ✅

**AC-6 (--base > start_commit > merge-base; --diff single ref).** `test_base_precedence.py`. `test_base_override_beats_frontmatter`, `test_frontmatter_start_commit_beats_merge_base`, `test_merge_base_fallback` (each precedence branch), `test_diff_arg_is_single_ref_no_range` + `test_base_override_range_value_stored_verbatim_not_split` (F3 de-range: no `..` splitting). **Falsifies:** reorder precedence → the "beats" assertions fail; introduce `<base>..HEAD` range form → the `".." not in diff_value` assertion fails. ✅

**AC-7 (reflect emits `remediation_task_path` 1.4.0; wrapper reads it).** Consumed via fixtures: `autofixable_drift.yaml` (path present → auto-run) vs `autofixable_drift_no_path.yaml` (null → `test_cannot_repair_absent_path_halts_no_apply`: HALTED, exit 10, `call_count == 1`, `fix_iterations == 0`). `_make_result` reads `c.get("remediation_task_path")` (contract.py:126). **Falsifies:** if the wrapper guessed a dir instead of reading the field, the null-path test would still apply something → call_count ≠ 1 → fail. ✅

**AC-8 (no cli.sprint/cli.roadmap import; no async; only ClaudeProcess; pipx exposes command).** `test_no_nesting_guard.py`: `test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg`, `test_no_async_await_anywhere_in_reflect_pkg`, `test_apply_remediation_launches_only_via_claudeprocess`, `test_layer_b_wrapper_module_has_no_agent_imports`. Anchored regexes correctly avoid docstring false-positives (verified the `_RAW_SUBPROCESS_CALL_RE` requires `(` so prose doesn't trip; `commands.py:267-274` subprocess.run for --tmux is deliberately out of scope — guard is runner.py-scoped). CLI exposure proven by `test_cli_smoke.py::test_run_help_shows_all_spec9_flags` (all 14 flags incl. `--fix/--no-fix/--max-fix-iterations/--base`). **Falsifies:** add a `from superclaude.cli.sprint import ...` → regex matches → fail. ✅

**AC-9 (all v1 fail-closed tests remain green).** `test_verdict_mapping.py` (19 passed), `test_writeback.py` (3), `test_runner_e2e.py` (10). Plus auto-fix-era fail-closed falsifiers in `test_fix_loop.py`: `test_degraded_with_drift_never_autofixed` (DEGRADED carrying drift>0 → exit 11, NO apply), `test_blocked_with_drift_never_autofixed` (BLOCKED+drift → exit 2, NO apply), `test_failed_apply_fails_closed_no_reaudit` (apply rc=1 → stays HALTED exit 10, NEVER PASS, `call_count == 2`, sidecar reason carries `fix-apply-failed` + `rc=1`). The `test_malformed_boolean_routes_blocked_upstream` proves the F2 strict-`is True` guard routes a stringy `"true"` to BLOCKED before the classifier is ever consulted — closing the "untrusted contract reaches classify_fix" hole. ✅

---

## Call-count arithmetic trace (Q4, against spec NFR-2 / contract §7 "(iterations+1) audits + iterations applies")

- **Convergence (1 fix iteration):** audit#1 (HALTED auto-fixable) → apply#1 → audit#2 (PASS). = 2 audits + 1 apply = **3 launches**. Test asserts `call_count == 3`, `fix_iterations == 1`. `(iterations+1)=2` audits + `iterations=1` apply ✅.
- **Non-convergence (N=2):** audit#1 → apply#1 → audit#2 → apply#2 → audit#3 (iteration=3 > max=2 → break). = 3 audits + 2 applies = **5 launches**. Test asserts `call_count == 5`, `fix_iterations == 2`. `(N+1)=3` audits + `N=2` applies ✅.

The runner sets `fix_iterations = iteration - 1` (runner.py:575). At loop exit on non-convergence, `iteration == 3` (incremented after apply#2's success, then audit#3 HALTED, then `iteration(3) > max(2)` breaks). `3 - 1 = 2` = N. Arithmetic is exact for N=2. ✅

---

## Summary

- Operational questions resolved in tests' favor: 5 / 5
- Falsification failures (test that would NOT catch its regression): 0
- Mutation probes run: 2 (loop-bound removal; marker too-loose truthiness) — both caught by the suite
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (AC-4 non-convergence proves termination by hang, not by bounded assertion — the in-tree `call_count == 5` assertion is the real proof; the test is not hostile-mutation-hang-proof)

## Issues Found

| # | Severity | Location | Issue | Required Fix (optional, non-blocking) |
|---|----------|----------|-------|----------------------------------------|
| 1 | MINOR | `test_fix_loop.py::test_non_convergence_exit10_five_launches` | Termination is proven by the `call_count == 5` assertion when the bound is present, but if the `iteration > max_iters` break were removed the test would HANG rather than fail fast (caught only by an external timeout, not by the assertion). | Optionally add `@pytest.mark.timeout(...)` (pytest-timeout) or a defensive upper-bound sequence so a removed-bound regression fails as a bounded assertion instead of a hang. Not required — the count assertion already pins the (N+1) bound for the shipped code. |

## Self-Audit

**(a) Reliance list — structural checks I did NOT re-run (rf-qa territory):** section numbering, frontmatter schema conformance, template cross-refs. None inherited via an Inherited Structural Verdict block (standalone review).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Carve-out adversarial-ness — verified by reading `classify_fix` short-circuit ordering (contract.py:356-366) + the `test_mixed_drift_and_regression_human_wins` row, not by trusting the test name.
- Loop termination — verified by **source mutation** (removed `runner.py:558-559` bound) + `timeout 30 uv run pytest` → RC=143 hang observed, then restored byte-identical.
- Marker truthiness negative-control — verified by **source mutation** (`bool(os.environ.get(...))` at `commands.py:69`) → 2 negative-control tests failed, then restored byte-identical.
- Call-count arithmetic — traced `iteration`/`fix_iterations` against runner.py:534-576 and the fixtures, computed (N+1)+N independently for N=1 and N=2.

**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 4 (1 suite run + 2 mutation probes + 1 fixture dump). Tool calls (13) ≥ questions verified (5) — not suspect.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

No web research performed (entirely local-file + source-mutation bound).

## QA Complete
