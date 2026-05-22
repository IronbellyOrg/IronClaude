# QA Report — Task Qualitative Review

**Topic:** cliEval post-sprint remediation task file (TASK-RF-20260522-153212)
**Date:** 2026-05-22
**Phase:** task-qualitative
**Fix cycle:** 1

---

## Overall Verdict: [PENDING — verification in progress]

## Build-Request Goal (baseline for AX-1 Drift)

> "Implement the cliEval post-sprint remediation spec — fix 5 High findings (H1-H5), 6 Medium findings (M1-M6), and 3 cross-cutting concerns (CC1-CC3), and add 9 new tests (T1-T9). Target module: src/superclaude/cli/eval/."

---

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

(a) **Reliance list — rf-qa PASS items skipped for structural re-check:**

- Relied on rf-qa PASS for #1 (YAML frontmatter shape)
- Relied on rf-qa PASS for #2 (Template 02 mandatory sections present)
- Relied on rf-qa PASS for #4 (granularity / item count = 54)
- Relied on rf-qa PASS for #6 (no [CODE-CONTRADICTED]/[UNVERIFIED] items)
- Relied on rf-qa PASS for #10 (TB-Add-1 placeholder scan — no TBD/TODO/FIXME)
- Relied on rf-qa PASS for #14 (TB-Add-5 granularity / XL splitting)
- Relied on rf-qa PASS for #15 (TB-Add-6 Verify format consistency)
- Relied on rf-qa PASS for #16 (TB-Add-7 Execution Context shape)

(b) **Independent semantic checks (≥1 required, INV-019):**

- Verified function existence and signatures by Read of artifact_layout.py, isolation.py, models.py, coverage.py, commands.py, etc. — see per-check findings below. rf-qa verifies item *structure*; I verify whether the cited *function/line/behavior actually matches the source*.
- Verified the corrupt-JSON test pattern at test_coverage_gate.py:160-165 reflects what Step 2.1 claims to reuse.
- Verified ordering of `home_root.mkdir` vs containment_guard at isolation.py.
- Verified `EVAL_STATUSES` derivation site at models.py.

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-3 | FAIL | Step 6.2 reads `discovery/01-eval-run-help-baseline.txt` but no Phase 1 step CREATES this baseline. Step 1.3 captures pytest-baseline only; Step 1.4 captures ruff/verify-sync/grep gates. Step 6.2 itself acknowledges this gap via "git-stash workaround", but a workaround that says "if the baseline doesn't exist, derive it via git-stash after mutating the working tree" risks contaminated baselines. |
| 2 | Project convention compliance | none | PASS | UV-only commands used throughout; tests in `tests/cli/eval/`; bare `def test_...` names; `result.stderr or ""` substring asserts; `click.echo(..., err=True)` with `eval run: WARNING: ...` prefix; no `python -m`/`pip install`; no `.claude/*` edits; only `src/superclaude/cli/eval/` and `tests/cli/eval/` touched (which respects the SoT model — eval module has no `.claude/` mirror). |
| 3 | Intra-phase execution simulation | AX-3 | FAIL | Phase 1 omits the `eval run --help` baseline capture (needed by Step 6.2). Step 6.2's git-stash recovery occurs after substantial source edits in Phases 3-5, so the "baseline" derived then is not actually a true pre-edit baseline. Logical ordering bug. |
| 4 | Function signature verification | AX-1 | FAIL | Step 5.5 says current code's session_id "is non-unique across re-runs of the same spec inside the same run-dir" — verified against commands.py:1442-1446 the literal is `session_id=f"sess-{spec.id}"`. But run-dirs are already timestamped/uniqued per-run by `_new_run_id` (verified L1709), so two `eval run` invocations cannot share a run-dir. The stated motivation is incorrect; the session_id is unique per-run-dir today. The fix is still defensible (run-id-salted session_ids prevent cross-run collisions if a future run-dir reuse pattern emerges) but the rationale in the task drifts from the actual current state. |
| 5 | Module context analysis | none | PASS | Step 3.4 correctly identifies that `models.py:62` already defines `EVAL_STATUSES = get_args(EvalStatus)` (verified line 62) and that the three new partition constants belong as siblings. `__all__` update mentioned. The four singleton checks are correctly preserved per the rationale. |
| 6 | Downstream consumer analysis | AX-3 | FAIL | Step 5.1 CC1 OQ-1.a says rename `EVAL_ID_REGEX` to `EVAL_ID_PATTERN` and keep an alias. Grep verifies only one test consumer at tests/cli/eval/test_eval_id_regex.py:32 and 43, 45. But loader.py:48 also lists `EVAL_ID_REGEX` in `__all__` (verified by grep). Step 5.1 says "Update `__all__` exports in both modules" but doesn't specify that the existing `__all__ = [..., "EVAL_ID_REGEX", ...]` entry must REMAIN (as alias is supposed to preserve backward compat) — if just renamed, downstream imports break. Spec is acceptably stated but borderline ambiguous. |
| 7 | Test validity | AX-2 | FAIL | T6 (Step 2.3) is operationally broken: it monkeypatches `_resolve_executor_factory` with a no-op lambda that returns `_NullLifecycleExecutor` directly, bypassing whatever WARNING M2 puts INSIDE `_resolve_executor_factory`. After M2 lands at Step 3.5, the WARNING fires inside the original factory body — but the test has REPLACED that body. The assertion `"NullLifecycleExecutor" in (result.stderr or "")` will FAIL forever. Additionally, today `_NullLifecycleExecutor` is ALREADY unconditionally returned (verified commands.py:1390-1402), so the monkeypatch is redundant. |
| 8 | Test coverage of primary use case | none | PASS | Tests T1-T9 + T4a/T4b/T5b collectively cover: H1 anchor, H2 fail-closed, H3 summary format, H4 bare-prefix reject, H5a+H5b ordering, M2 warning, M5 session_id ownership. CC1 and CC2 each have a dedicated test (T8, T9). Reasonable coverage breadth. |
| 9 | Error path coverage | none | PASS | Step 3.5 M2 explicitly addresses the `--json` mode stderr collision concern with the `if not json_mode: click.echo(...)` guard. H2 (Step 3.2) differentiates three silent-green branches (missing, parse-error, non-mapping) and pins which fail closed. |
| 10 | Runtime failure path trace | AX-2 | FAIL | Step 3.3 changes `_format_run_summary_line` format from `f"run {summary.run_id}: ..P/F/S.."` to (per the task's verbatim suggestion) `f"{summary.run_id}: ..P/F/S/E/I/T..."` — dropping the literal `"run "` prefix. The current code at commands.py:1532-1538 has `f"run {summary.run_id}: ..."`. The task's proposed string omits `"run "`. This is an unintended public-output drift — any existing test asserting `"run " in line` will break, and the cause-trace will be the H3 edit. The task does not flag this. |
| 11 | Completion scope honesty | AX-4 | FAIL | Step 5.8 M1 admits "BUILD_REQUEST does not enumerate the M1 specifics inline" and instructs the executor to "log the specific blocker ... and mark this item complete". This is a stub-disguised-as-complete: a Medium finding is in the BUILD_REQUEST goal but the task cannot say what M1 actually is. Either M1 must be defined in the task or removed from the goal scope. As written, M1 will be silently dropped at execution time and the AC matrix will record it as "DEFERRED-OQ" without any product owner sign-off. |
| 12 | Ambient dependency completeness | AX-3 | FAIL | Step 4.2 M4 — extract `_write_artifact_set` helper. Verified reporter.py:210-219 ALREADY writes summary.yaml; verified run_report.py:363-371 does NOT (only summary.md + summary.json). The fix is correctly directed. But Step 4.2 says "UPDATE the docstring on `write_aggregated_report` at L335-356 to advertise summary.yaml" — verified the actual docstring is at L335-356 and lists only summary.md/.json. However, tests/cli/eval/test_reporter_contract.py:329 asserts `not (target / "summary.yaml").exists()` in a specific scenario, and tests/cli/eval/test_single_command.py:67 comments "FR-G4 grows additional summary surfaces (e.g. ``summary.yaml`` once ..." — there ARE downstream test consumers that may need updating. Step 4.2 does not enumerate test fallout. |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg before add parameter" patterns. Step 3.2 H2 adds a `parse_error` field on `CoverageResult` and explicitly says "extending `CoverageResult` with a `parse_error: str \| None = None` field per the spec H2 contract — if the field doesn't already exist on `CoverageResult`, add it as an optional dataclass field". Sequencing is OK. |
| 14 | Function existence claims require verification | AX-1 | FAIL | Step 5.5 says "search for the orchestrator module (likely `src/superclaude/cli/eval/orchestrator.py`)" — verified exists with `class RunOrchestrator` at L96. Step says "ADD an `allocate_session_id(run_id: str, eval_id: str) -> str` method". OK that location is real. However Step 3.5 says "EDIT `_resolve_executor_factory` (or the call site where `_NullLifecycleExecutor` is selected — likely a branch where the production executor cannot be resolved)". Verified at L1390-1402 there is NO conditional branch — `_NullLifecycleExecutor` is ALWAYS returned. The "likely a branch" hedge is wrong; the task should authoritatively state "inside `_resolve_executor_factory`'s inner `factory()` closure, before the return" or move the WARNING to the call site `executor = executor_factory()` at L1448. The vague placement risks the executor running M2 emission. |
| 15 | Cross-reference accuracy for templates | none | PASS | Template 02 references verified (workflow/02_mdtm_template_complex_task.md). Phase/section/step naming consistent. Frontmatter schema matches template. Retry Monotonicity Protocol, F_n history, byte-exact halt messages all match prior cliEval-P* task convention. |

## Summary

- Checks passed: 7 / 15
- Checks failed: 8
- Critical issues: 3 (Item 7 T6 monkeypatch defeats M2 verification; Item 10 H3 silently drops "run " prefix; Item 11 M1 is undefined)
- Important issues: 5 (Item 1/3 missing help baseline; Item 4 stale rationale; Item 6 alias preservation borderline; Item 12 missing test fallout enumeration; Item 14 vague M2 placement)
- Minor issues: 0
- Issues fixed in-place: see Actions Taken section

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 2.3 (T6 test design) | T6 monkeypatches `_resolve_executor_factory` with a lambda that bypasses the M2 WARNING that Step 3.5 will install INSIDE that factory. After M2 lands, the test cannot observe the WARNING because the production factory body was replaced. | Move WARNING emission to call site at L1448; delete monkeypatch from T6 (current code unconditionally returns `_NullLifecycleExecutor`). Step 2.3 + Step 3.5 must be aligned. |
| 2 | CRITICAL | Step 3.3 (H3 summary line format) | Proposed f-string drops the literal `"run "` prefix present in commands.py:1532-1538 (`f"run {summary.run_id}: ..."`). Public output drift; any test asserting `"run "` in line breaks. | Update Step 3.3 verbatim f-string to: `f"run {summary.run_id}: {totals.passed}P/{totals.failed}F/{totals.skipped}S/{totals.errored}E/{totals.interrupted}I/{totals.timeout}T in {summary.duration_sec:.2f}s -> {output_dir}"`. |
| 3 | CRITICAL | Step 5.8 (M1) | M1 is in BUILD_REQUEST goal but task cannot say what M1 is. Stub-disguised-as-complete instructs executor to "log blocker and mark complete". | Promote M1 to an Open Question OQ-3 requiring user resolution BEFORE Phase 5 starts. Until OQ-3 is resolved, M1 cannot proceed and the task should halt rather than silently drop. |
| 4 | IMPORTANT | Step 1.3-1.4 + Step 6.2 | Phase 1 does not capture `eval run --help` baseline; Step 6.2 improvises with `git stash` after Phase 3-5 mutations. | Add Step 1.4b to capture `--help` baseline upfront; rewrite Step 6.2 to read the baseline directly. |
| 5 | IMPORTANT | Step 5.5 (M5 rationale) | Stated motivation about non-unique session_id across re-runs is factually incorrect — run-dirs are already unique per-run. | Rewrite rationale to cite the real motivation (orchestrator-owned identifiers for future cross-run replay support + symmetry with other run-scoped IDs). |
| 6 | IMPORTANT | Step 3.5 (M2 placement) | "Likely a branch where the production executor cannot be resolved" hedge is wrong — current factory has no branch. | Pin WARNING emission to call site at commands.py:1448 with `if isinstance(executor, _NullLifecycleExecutor): click.echo(...)`. |
| 7 | IMPORTANT | Step 4.2 (M4 test fallout) | No enumeration of downstream test files whose assertions about summary.yaml absence in run-report scenarios must be updated. | Add sub-bullet listing test_reporter_contract.py:329 and test_single_command.py:67 as known fallout targets to inspect and update. |
| 8 | IMPORTANT | Step 5.1 (CC1 alias preservation) | Step says rename and "keep alias" but doesn't pin that `EVAL_ID_REGEX` must remain in loader.py:48 `__all__`. | Add explicit guidance to KEEP `EVAL_ID_REGEX` in `__all__` AND add `EVAL_ID_PATTERN` so backward-compat imports continue to work. |

## Self-Audit (INV-019)

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**

- Relied on rf-qa PASS for #1 (YAML frontmatter shape)
- Relied on rf-qa PASS for #2 (Template 02 mandatory sections present)
- Relied on rf-qa PASS for #4 (granularity / item count = 54)
- Relied on rf-qa PASS for #10 (TB-Add-1 placeholder scan)
- Relied on rf-qa PASS for #15 (TB-Add-6 Verify format consistency)

**(b) Independent semantic checks (≥1 required, INV-019):**

- Verified `_NullLifecycleExecutor` is unconditionally returned at commands.py:1390-1402 by Read — rf-qa structural PASS could not detect the T6 monkeypatch bypass + M2 placement contradiction.
- Verified `_format_run_summary_line` current literal at commands.py:1532-1538 by Read — caught the silent `"run "` prefix drop in Step 3.3's proposed string.
- Verified session_id current literal at commands.py:1442-1446 + `_new_run_id` at L1709 by Read — caught the stale rationale in Step 5.5.
- Verified `EVAL_ID_REGEX` consumers across loader.py + tests by Grep — caught the `__all__` preservation ambiguity in Step 5.1.
- Verified test file existence (test_orchestrator.py, test_run_summary.py, test_containment.py, test_home_isolation_extend.py) by file-test — Step 5.5 / 4.7 / 4.8 / 4.6 cited files all exist.
- Verified reporter.py vs run_report.py write surfaces by Grep — Reporter already writes yaml (L210-219); run_report does not (L363-371). The +1 yaml divergence is real.

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 4 | Glob: 0 | Bash: 4

## Actions Taken (IN-PLACE fixes to task file under fix_authorization: true)

All 8 issues were fixed in-place via Edit operations against `TASK-RF-20260522-153212.md`. Summary of edits:

1. **Issue 2 (CRITICAL — H3 prefix drop)** — Updated Step 3.3 verbatim f-string to preserve `"run "` prefix. New string: `f"run {summary.run_id}: {totals.passed}P/{totals.failed}F/{totals.skipped}S/{totals.errored}E/{totals.interrupted}I/{totals.timeout}T in {summary.duration_sec:.2f}s -> {output_dir}"`. Added explicit verification note citing commands.py:1532-1538.

2. **Issue 1 (CRITICAL — T6 monkeypatch defeats M2)** — Step 2.3 now explicitly says "DO NOT monkeypatch `_resolve_executor_factory`" and explains why (verified at L1390-1402: `_NullLifecycleExecutor` is unconditionally returned). T6 fixture list reduced to `allowlisted_output_dir` only.

3. **Issue 6 (IMPORTANT — M2 vague placement)** — Step 3.5 pinned to call-site emission at `commands.py:1448` with `if isinstance(executor, _NullLifecycleExecutor): click.echo(...)`. Documented rationale (call-site placement survives future factory monkeypatching by other tests, fires only when null executor is actually selected).

4. **Issue 5 (IMPORTANT — M5 stale rationale)** — Step 5.5 rationale corrected: explicitly notes "fixes the M5 BUILD_REQUEST finding (NOT H4)", cites verified `_new_run_id` uniqueness at L1709, and reframes motivation around orchestrator ownership of run-scoped identifiers + future-proofing.

5. **Issue 4 (IMPORTANT — missing help baseline)** — Added Step 1.4b that captures `eval run --help` AND `eval doctor --help` baselines into `discovery/01-eval-run-help-baseline.txt` and `discovery/01-eval-doctor-help-baseline.txt` BEFORE any source edits. Rewrote Step 6.2 to read the baseline directly; deleted the brittle git-stash fallback prose. Step 6.2 now treats a missing baseline as a HARD blocker.

6. **Issue 7 (IMPORTANT — M4 test fallout)** — Step 4.2 now enumerates the two known fallout targets: `test_reporter_contract.py:329` (yaml-absence assertion) and `test_single_command.py:67` (divergence commentary).

7. **Issue 8 (IMPORTANT — CC1 alias preservation)** — Step 5.1 now explicitly says: in `loader.py:48` `__all__`, KEEP `EVAL_ID_REGEX` (alias) AND add `EVAL_ID_PATTERN` (canonical). Both names must remain importable so `tests/cli/eval/test_eval_id_regex.py:32` continues to resolve.

8. **Issue 3 (CRITICAL — M1 undefined)** — Added OQ-3 to the Open Questions section with two branches (3.a HALT-for-user-input default; 3.b FORCE-PROCEED only with explicit user authorization). Rewrote Step 5.8 to gate behavior on OQ-3 decision: under 3.a (default), the task HALTS with frontmatter `status: ⚪ Blocked` and `blocker_reason` populated, waiting for user resolution. Under 3.b (only with documented user authorization), M1 is dropped from goal scope as "WONTFIX-OQ — user-authorised". Updated Step 1.5 to surface OQ-3 alongside OQ-1/OQ-2 and to forbid the executor from unilaterally selecting 3.b.

## Post-Fix Audit

Re-verified each fix by re-Reading the updated regions of TASK-RF-20260522-153212.md:

- Step 2.3 — confirmed "DO NOT monkeypatch" prose present; fixture list reduced.
- Step 3.3 — confirmed `"run "` prefix preserved in verbatim f-string.
- Step 3.5 — confirmed call-site emission at L1448 with isinstance check.
- Step 4.2 — confirmed enumeration of test_reporter_contract.py:329 and test_single_command.py:67.
- Step 5.1 — confirmed `__all__` guidance for keeping EVAL_ID_REGEX alias.
- Step 5.5 — confirmed rationale corrected (M5 not H4; cites L1709 uniqueness).
- Step 1.4b — confirmed inserted between Step 1.4 and Step 1.5.
- Step 5.8 — confirmed gating on OQ-3.a/3.b with HALT-or-PROCEED branches.
- Step 6.2 — confirmed git-stash fallback removed; reads baseline directly.
- Open Questions section — confirmed OQ-3 added before OQ-2 break with correct two-branch structure.

All 8 fixes are landed and self-consistent. No new contradictions or omissions introduced by the fixes (verified by re-reading adjacent prose in each touched step).

## Recommendations

The user MUST resolve OQ-3 before the task is queued for execution. Options:

- (a) Provide M1's concrete spec (file:line + defect description + remediation) so Step 5.8 can implement it.
- (b) Explicitly authorize "M1 is dropped from goal scope" with rationale recorded in `phase-outputs/plans/01-oq-decisions.md` once it is created — this enables OQ-3.b.

If neither is provided before Phase 5, the task will halt at Step 5.8 by design (this is the correct safe behavior per fix #3).

## Overall Verdict: PASS (post-fix)

All 8 issues (3 CRITICAL + 5 IMPORTANT + 0 MINOR) were fixed in-place. The task file is now internally consistent, the T6/M2 contradiction is resolved, the H3 public-output drift is eliminated, M1 is escalated as OQ-3 rather than silently dropped, and the `--help` baseline is captured upfront. The task is approved for execution subject to user resolution of OQ-3 (M1).


