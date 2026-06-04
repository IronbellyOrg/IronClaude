# QA Report — Post-Completion Qualitative / Operational Gate (task-qualitative)

**Topic:** `superclaude sprint rerun-tasks` (v4.3.0) — operational-outcome audit
**Date:** 2026-06-02
**Phase:** task-qualitative (post-completion, runs AFTER structural gate PASS cycle 2)
**Fix cycle:** 1
**Fix authorization:** true (max 3 cycles)
**Document type:** Executed Task File
**Stance:** Adversarial — assume the feature does NOT solve the operator pain end-to-end; trace each claim to real code/tests on disk.

---

## Overall Verdict: PASS (1 operational fix applied; 1 deferral CONCERN noted)

---

## Tool engagement
Read: 8 (structural cycle1 + cycle2 reports, help.txt, pytest-summary, ac-coverage, rerun_tasks.py full, recovery.py full, executor.py ×2 sites, commands.py rerun block, e2e tests, failure-mode tests, TDD merged-requirements) | Bash: 5 (pytest ×2, reflect-path trace ×2, lint+fix-verify) | Grep: 2 (TDD reflect/defer search) | Glob: 0.
Web research: none — all claims internal-source-bound. tavily_search: 0 | tavily_extract: 0 | web fallbacks: 0.

---

## Criterion 1 — Core pain solved (rerun ONLY T07.11+T07.12, not the 19 PASS) — PASS

**Operational question:** Can an operator rerun only the 2 transient-failed tasks of a 21-task phase WITHOUT re-executing the 19 PASS tasks, and merge back?

**Found:**
- `run_rerun_tasks` Step 5 (`rerun_tasks.py:1298`) calls `extract_phase_subset(phase_obj.file, nominated, bundle)` — extracts ONLY the nominated task blocks (`selected_blocks = [m.group(0) for m in matches if m.group(1) in target_set]`, `:156`) into `<bundle>/phase-7r-tasklist.md`. The 19 PASS tasks are never placed in the sub-tasklist.
- Step 11 (`:1344-1362`) builds a single-phase sub-index and runs `execute_sprint(sub_config)` where `sub_config` has `release_dir=bundle`, `phases=sub_phases` (re-discovered from the sub-index = the 2-task subset only), `start_phase=end_phase=phase`. Execution is fully ISOLATED to the bundle and the 2 tasks; the canonical results dir is untouched until merge.
- Merge-back (Step 12, `:1379-1404`) merges only `produced = phase-{phase}-*` artifacts from the bundle results into canonical via `merge_recovery_bundle`.
- E2E proof: `test_merge_back_succeeds_without_force_merge` (`test_rerun_tasks_e2e.py:333`) and `test_rerun_renames_originals_...` (`:215`) seed only T07.11/T07.12, run, and assert `{"T07.11","T07.12"} <= merged_task_ids` with originals renamed `*.failed-<ts>`. Ran on disk: PASS.

The 19 PASS tasks are structurally excluded from the sub-tasklist, so they cannot be re-executed. **The headline MultiModelSwarm pain is solved end-to-end.**

**Result: PASS**

---

## Criterion 2 — Happy-path merge works WITHOUT --force-merge (post-fix) — PASS

**Operational question:** After the SHA-guard fix, does a clean unedited rerun merge back without `--force-merge`? Is `--force-merge` now an escape hatch, not mandatory?

**Found:**
- The guard now hashes provenance-block-stripped content at BOTH capture (Step 4, `:1292` `source_sha = _content_sha256_excluding_rerun_block(phase_obj.file)`) and compare (Step 12, `:1373` `current_sha = _content_sha256_excluding_rerun_block(phase_obj.file)`). The helper (`:688-701`) strips the `SUPERCLAUDE-RERUN` block via `_split_rerun_block` before hashing, so the engine's own Step-10 provenance write is invisible to the guard.
- `test_merge_back_succeeds_without_force_merge` deliberately passes NO `--force-merge`, asserts exit 0, `"Source tasklist modified..." not in output`, `"Rerun merged" in output`, originals renamed, `recovery_history` appended. Ran on disk: **PASS**. This is the exact regression test the cycle-1 defect lacked.
- `--force-merge` remains an escape hatch: `test_force_merge_proceeds_with_warning` confirms it still bypasses a REAL mid-flight edit. The flag is now optional, not mandatory.
- The cycle-1 IMPORTANT blocking defect is genuinely resolved — confirmed independently by reading both call sites and running the test, not by relying on the structural cycle-2 report.

**Result: PASS** — the post-fix operator experience matches intent: clean reruns merge on the default path; `--force-merge` is reserved for real edits.

---

## Criterion 3 — Transient classification feeds default nomination — PASS

**Operational question:** Does `--tasks`-omitted default nomination pick the transient (recoverable) failures, matching operator intent, not the terminal ones?

**Found:**
- `executor.py:1016-1023` classification ladder: exit 0 → PASS; 124 (timeout) → INCOMPLETE; `_is_transient_failure(...)` True → `FAIL_RECOVERABLE`; else `FAIL_TERMINAL`. `_is_transient_failure` (`:1782-1804`) keys on `api_retry`/`ConnectionRefused`/(`is_error` AND zero output_tokens) — exactly the MultiModelSwarm transient-API-outage signature.
- `select_default_recoverable_tasks` (`rerun_tasks.py:1100-1129`) reads `phase-N-result.json` and returns ONLY task IDs whose serialized `status == "fail_recoverable"`. Terminal failures are excluded by construction.
- `run_rerun_tasks` Step 2 (`:1265-1276`): when `--tasks` omitted, nominates via `select_default_recoverable_tasks`; empty → legacy transcript fallback.
- The default nomination matches operator intent: rerun the transient failures, leave terminal failures for manual investigation (terminal fails need a code fix, not a retry).

**Result: PASS**

---

## Criterion 4 — --from-reflect-report v4.3.0 stub: documents/defers vs crashes — CONCERN (deferred) → FIXED operator-message defect

**Operational question:** Does `--from-reflect-report` correctly defer the v4.4.0 plan rather than silently no-op or crash?

**Found (adversarial trace on disk):**
- TDD is explicit this is an AUTHORIZED deferral: Resolution #2 (`merged-requirements.md:255`) — "`--from-reflect-report` flag co-ships with SprintRunReflect in v4.4.0"; Option A (recommended, `:245/:248`) ships v4.3.0 with **manual-nomination only**; co-dependency note (`:149`). So a non-functional reflect path in v4.3.0 is INTENDED, not a build miss. This is correctly a deferral, NOT a FAIL.
- HOWEVER, the structural gate's claim that it "correctly documents/defers ... rather than crashing" was **partially inaccurate**. I traced the actual operator experience:
  - `--from-reflect-report <path>` WITHOUT `--phase` (the DOCUMENTED usage; `--help`/docstring advertise it as "an alternative to --phase/--tasks") → `run_rerun_tasks` hits `if phase is None: raise ClickException("--phase is required for rerun-tasks.")` at `:1231` BEFORE ever reaching the `ReflectReportNominator` at `:1261`. Operator got the **misleading, self-contradictory** error "--phase is required" — directly contradicting the help text that calls reflect-report mutually exclusive WITH `--phase`.
  - `--from-reflect-report <path>` WITH `--phase` → blocked by the commands.py mutual-exclusion guard (`commands.py:515`). So there was NO path to a clean message; the stub's `nominate()` returning `[]` was unreachable.
- This is a genuine operator-experience defect on a deferred feature: a confusing dead-end rather than an honest "not yet available." Small, clearly-correct, in worktree source → **fixed in-place** (see Fixes Applied). After the fix the operator gets an honest "not available in v4.3.0 ... ships in v4.4.0. Use --phase/--tasks." message.

**Result: CONCERN (deferred feature, correctly deferred per TDD) — operator-message defect FIXED.** Not a FAIL: the deferral itself is authorized; the misleading error is now corrected.

---

## Criterion 5 — --restore botched-merge recovery — PASS

**Operational question:** Can an operator recover after a bad merge-back via `--restore`?

**Found:**
- Step 9 (`:1335`) `stash_and_restore_deliverables` copies each target's results artifacts + declared `**Artifacts (Intended Paths):**` deliverables into `<bundle>/preserved/` with a `manifest.json` BEFORE any mutation — so a recovery point always exists.
- `--restore` short-circuit (`:1248-1256`): resolves `bundle_dir or most_recent_bundle(config.results_dir)` (`:1084` newest `rerun-*` dir), calls `restore_from_bundle` (`:1039`) which reads the manifest and `shutil.copy2`s each preserved file back to its canonical path, returns the count, echoes "Restored N file(s)".
- Traced no-bundle path on disk: `--restore` with no bundle → honest `"No rerun bundle found to --restore from."` exit 1. Graceful, not a crash.
- Degrades gracefully: missing/unreadable manifest → `restore_from_bundle` returns 0 (`:1049`), no exception.

**Result: PASS** — an operator can recover stashed deliverables after a bad merge.

---

## Criterion 6 — Post-merge verify-checkpoints --recover auto-invoke — PASS

**Operational question:** Does verify-checkpoints --recover actually fire after merge to regenerate missing reports?

**Found:**
- Step 14 (`:1419-1430`): gated on `exit_code == 0 and merge_back and not no_verify_checkpoints`, runs `subprocess.run(["uv","run","superclaude","sprint","verify-checkpoints","--recover","--phase",str(phase),"--quiet"], check=False)`. `OSError` is caught and echoed, never masks the merge success.
- Test asserts the actual subprocess invocation: `test_rerun_renames_originals_...` (`:295-298`) asserts `mock_verify.called`, `"verify-checkpoints" in verify_argv`, `"--recover" in verify_argv`. Ran on disk: PASS.
- `--no-verify-checkpoints` opt-out wired and documented.

**Result: PASS** — the auto-invoke is real and asserted, not theater.

---

## Criterion 7 — Forensic trail sufficient for 3-strikes investigation — PASS

**Operational question:** Do the audit log + `.failed-<ts>` renames + retry-cap give enough trail to investigate a stuck task?

**Found:**
- `recovery-audit.log` (JSONL, append-mode, `recovery.py:250-267`) records every lifecycle event: `rerun_checkboxes_flipped/restored/finalized`, `deliverables_stashed/restored`, and `merge_recovery_bundle` (with `status`, `failures`, `rerun_attempt`). Shared across recovery verbs.
- Forensic renames: merge Steps 1-3 (`recovery.py:440-500`) rename prior canonical output/checkpoint/errors artifacts to `*.failed-<orig_mtime>.*` and record `artifacts_replaced` — the prior failing transcripts are preserved, never overwritten.
- Retry-cap (Step 8, `:1322-1332`): 4th attempt on a T-ID aborts with "Task {tid} has been rerun 3 times. Manual intervention required. Inspect bundles: {bundles}" — the abort message itself points to the bundle list for investigation. Confirmed by `test_fourth_attempt_aborts_with_cap_message` (on disk: PASS).
- `_print_investigation_summary` (`:1185`) prints last-PASS / recoverable / terminal / nominated derived from the authoritative result JSON.
- `recovery_history` on each merge accumulates `RecoveryBundleRef`s, so the full retry chain is reconstructable.

**Result: PASS** — a 3-strikes investigation has the audit log, the preserved `.failed-<ts>` transcripts of every prior attempt, the bundle list, and the result-JSON history.

---

## Criterion 8 — Safety defenses real, not theater — PASS

**Operational question:** Are lock / retry-cap / SHA-guard / stash-restore each enforced on a real path with a real abort?

**Found (each backed by a failure-mode test run on disk):**
- **Lock (concurrent abort):** `acquire_recovery_lock` (`recovery.py:275`) writes `{pid,timestamp}`, checks liveness via `os.kill(pid,0)`, reclaims stale, aborts on live PID; released in `finally` (`:1440`) + atexit + SIGTERM. `test_second_concurrent_invocation_aborts_with_lock_pid`: PASS (names the live PID).
- **Retry-cap-3:** real abort before executor; `test_fourth_attempt_aborts_with_cap_message` + `--allow-loop` bypass `test_allow_loop_bypasses_cap`: PASS.
- **SHA guard (now correct):** real external edit still aborts — `test_source_tasklist_sha_mismatch_aborts` appends plain content (outside the RERUN block) and asserts byte-exact abort: PASS. The fix keeps the guard live for real edits while blind to the engine's own write (Criterion 2).
- **Stash/restore on abort:** `finally` block (`:1433-1442`) calls `restore_checkboxes_on_abort` — `test_abort_before_merge_back_restores_source_tasklist` asserts the tasklist is byte-for-byte restored; `test_abort_clears_rerun_in_progress_flag` asserts no `SUPERCLAUDE-RERUN`/`rerun_in_progress` residue: both PASS.

All 11 e2e+failure-mode tests + 25 unit/recovery tests (36 total) ran green on disk this session.

**Result: PASS** — every safety defense is enforced on a real path with a real abort and a real assertion.

---

## Confidence Gate

- [x] C1 Core pain solved — VERIFIED (extract_phase_subset trace + 2 e2e tests run)
- [x] C2 Happy-path merge no-force — VERIFIED (both guard call-sites read + regression test run)
- [x] C3 Transient → nomination — VERIFIED (classification ladder + default-nominator read)
- [x] C4 Reflect stub — VERIFIED (TDD deferral grep + on-disk operator-experience trace ×2 + fix verified)
- [x] C5 --restore — VERIFIED (restore path read + no-bundle trace on disk)
- [x] C6 verify-checkpoints auto-invoke — VERIFIED (subprocess assertion in test run)
- [x] C7 Forensic trail — VERIFIED (audit log + rename steps + cap message read)
- [x] C8 Safety defenses — VERIFIED (all 11 failure-mode/e2e tests run green)

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool-engagement minimum satisfied (15 tool calls ≥ 8 criteria; each maps to a specific criterion).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT (operator-experience) | rerun_tasks.py:1231 vs commands.py:507-518 help text | `--from-reflect-report` without `--phase` (the documented usage) tripped the generic `"--phase is required"` guard before reaching the deferred stub — a self-contradictory message vs help text advertising reflect-report as an alternative to `--phase`. Structural gate's "documents/defers rather than crashing" claim was partially inaccurate. | FIXED in-place: honest "not available in v4.3.0; ships in v4.4.0; use --phase/--tasks" abort when reflect-report is the reason `--phase` is absent. |
| 2 | CONCERN (deferred, no fix) | recovery.py ReflectReportNominator + Resolution #2 | `--from-reflect-report` is a non-functional v4.3.0 stub. This is the AUTHORIZED Option-A deferral (TDD :245/:255) — reflect-report nomination co-ships with SprintRunReflect in v4.4.0. | None — correct deferral. Tracked for v4.4.0. |

---

## Actions Taken (Fixes Applied)

**1 fix applied** (Issue #1, worktree source only):
- **Edited** `src/superclaude/cli/sprint/rerun_tasks.py:1231` — replaced the bare `if phase is None: raise "--phase is required"` with a branch that, when `from_reflect_report is not None`, raises an honest deferral message: *"--from-reflect-report is not available in v4.3.0 (reflect-report nomination ships with SprintRunReflect in v4.4.0). Use --phase N --tasks T<PP>.<TT>[,...] to nominate tasks manually."* The generic `--phase is required` message is retained for the no-reflect case.
- **Verified the fix:** traced `--from-reflect-report` without `--phase` on disk → now emits the honest deferral message (was the misleading "--phase is required").
- **Lint:** `uv run ruff check rerun_tasks.py` → "All checks passed!"
- **Regression:** `uv run pytest` on e2e + failure-modes + unit + recovery → **36 passed**. No regression. (The fix touches only the `phase is None AND from_reflect_report set` path, which no existing test exercised; all manual-nomination and merge paths unchanged.)

No structural matters re-litigated. The SHA-guard fix and all 8 ACs were verified as operational outcomes only.

---

## Overall Verdict

**VERDICT: PASS**

Rationale: The feature solves the MultiModelSwarm operator pain end-to-end — an operator can rerun ONLY the 2 transient-failed tasks (T07.11+T07.12) of a 21-task phase without re-executing the 19 PASS tasks, and merge results back atomically. The cycle-1 blocking SHA-guard self-trip is genuinely resolved: the happy path now merges back WITHOUT `--force-merge` (independently verified by reading both stripped-hash call sites and running `test_merge_back_succeeds_without_force_merge`), and `--force-merge` is correctly demoted to an escape hatch while the guard still catches real operator edits. Transient classification feeds default nomination correctly (recoverable, not terminal). `--restore`, the post-merge `verify-checkpoints --recover` auto-invoke, the forensic trail (audit log + `.failed-<ts>` renames + retry-cap), and all safety defenses (lock, retry-cap-3, SHA guard, stash/restore) are each enforced on a real path with a real abort and a real test assertion (36 tests green on disk this session).

The only operational defect found — a misleading error message on the deferred `--from-reflect-report` path — was small, clearly-correct, and FIXED in-place. The reflect-report feature being non-functional in v4.3.0 is the AUTHORIZED Option-A deferral per the TDD (co-ships with SprintRunReflect in v4.4.0), correctly classified as CONCERN/deferred, not FAIL. With the operator-message fix applied and all issues resolved, the gate is PASS.

## QA Complete
