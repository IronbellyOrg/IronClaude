# QA Report — Post-Completion Structural Gate (report-validation)

**Topic:** `superclaude sprint rerun-tasks` (v4.3.0) — full-task structural audit
**Date:** 2026-06-02
**Phase:** report-validation (FINAL full-task audit)
**Fix cycle:** 1
**Fix authorization:** true (max 3 cycles)
**Stance:** Adversarial / zero-trust — re-read all source + artifacts independently

---

## Overall Verdict: PENDING

(Filled at end after all 8 criteria + confidence gate.)

---

## Tool engagement
Read: 9 (recovery.py full, rerun_tasks.py full, models.py full, commands.py rerun block, executor.py ×3 sites, config.py ×2, 06-gate-resolutions.md, AC5 test) | Grep/Bash: 11 (line counts, import smoke, lint, stub scan, rename-residue, new-test run, test/assert counts, no-op scan, AC scan, source_sha trace, plus LOC scans below) | Glob: 0 (paths supplied verbatim).

Web research: none required — all claims are internal-source-bound (no external URL/standard/3rd-party-API claim in scope). tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.

---

## Criterion 1 — BUILD_REQUEST goals achieved — PASS

| Goal | Evidence | Result |
|------|----------|--------|
| `rerun-tasks` operational, 12 flags | commands.py:419-541 — `--phase, --tasks, --from-reflect-report, --merge-back/--no-merge-back, --dry-run, --include-transitive, --ignore-deps, --force-merge, --allow-loop, --no-verify-checkpoints, --bundle-dir, --restore` (12 distinct) all wired into `run_rerun_tasks(...)` call | PASS |
| `FAIL_RECOVERABLE` classification wired (§T6) | executor.py:1782 `_is_transient_failure` defined; used at executor.py:1020 → `status = TaskStatus.FAIL_RECOVERABLE` (1021); transient markers `api_retry`/`ConnectionRefused`/zero-output-tokens at 1793-1803 | PASS |
| `merge_recovery_bundle` 7-step engine present + sound | recovery.py:381-687 — steps 1-7 each labelled + debug_log traced; atomic tmp+replace writes; R-F3 sidecar-absent preservation (no silent data loss) at 616-652 | PASS |
| All 8 ACs covered by real tests | e2e AC1-AC3 (test_rerun_tasks_e2e.py:152,212,300); failure-modes AC4-AC8 (test_rerun_tasks_failure_modes.py:245,282,359,419,473) | PASS |
| `make lint` clean | `uv run ruff check` on all 8 files → "All checks passed!" | PASS |
| only pre-existing pytest failures | 35 new tests pass (test_recovery/rerun_tasks/e2e/failure_modes); 54 failures + 2 collection errors confirmed pre-existing per spawn brief, classification independently consistent (process.stdin / invoke_haiku) | PASS |
| recovery.py / rerun_tasks.py import cleanly | `uv run python -c "import ..."` → IMPORT_OK | PASS |

---

## Criterion 2 — Cross-phase consistency — PASS

| Producer (phase) | Consumer (phase) | Evidence | Result |
|---|---|---|---|
| `to_dict`/`from_dict` on TaskResult (Phase 1, models.py:184-234) | executor json write (Phase 4, executor.py:2065 `tr.to_dict()`) + rerun read (`from_dict` rerun_tasks.py:1146) + tests | round-trips; nested `task.task_id` shape consistent across writer and all readers | PASS |
| `phase_result_json` helper (Phase 1, models.py:570) | executor `_write_phase_result_json` (Phase 4, executor.py:2068) → read by `select_default_recoverable_tasks` (Phase 3, rerun_tasks.py:1083-1112) + `_load_phase_result_view` (1131) | path + JSON schema (`task_results[].status`, `task.task_id`) match end-to-end | PASS |
| `RecoveryStatus`/`RecoveryBundle` (recovery.py) | `run_rerun_tasks` step 12 (rerun_tasks.py:1371-1382) | constructed + merged; field names align | PASS |
| `PHASE_FILE_PATTERN` widen (config.py:27 `phase-(\d+)r-tasklist`) | `discover_phases` group extraction (config.py:127,141 `next(g for g in match.groups() if g is not None)`) | the multi-group `next(...)` idiom correctly returns the rerun group's digits — verified the added group is positionally compatible | PASS |

No orphaned outputs found (every helper added has a downstream consumer). No missing outputs (every referenced producer exists). `recovery_history` is written by executor (executor.py:2066) and read by `retry_count_for_task` (recovery.py:356) + `_load_phase_result_view`.

---

## Criterion 3 — "ensuring…" clauses satisfied (sampled per phase) — PASS

Representative spot-checks against real code:
- **Phase 1 (data model):** "ensuring existing logs deserialize" → `FAIL_TERMINAL="fail"` (models.py:49) keeps wire value; round-trip `from_dict(TaskStatus("fail"))` resolves to FAIL_TERMINAL. PASS.
- **Phase 1 (circular-import avoidance):** "ensuring models.py does not import recovery.py at runtime" → models.py:23-27 `TYPE_CHECKING` forward-ref only. PASS.
- **Phase 3 (extraction round-trip):** "ensuring malformed MDTM aborts before tokens spend" → rerun_tasks.py:160-170 round-trip validation raises ClickException pre-write. PASS.
- **Phase 3 (no silent data loss):** "ensuring affected tasks' prior entries are not dropped" → recovery.py:644-652 preserves prior entries + flags PARTIAL when sidecar absent. PASS.
- **Phase 4 (atomic persist):** "ensuring a crash mid-write never truncates" → executor.py:2070-2072 tmp+replace. PASS.
- **Phase 5 (lock always released):** "ensuring the lock releases on crash" → rerun_tasks.py:1416-1424 `finally` block releases lock + abort-restore. PASS.

---

## Criterion 4 — Resolutions 1-5 applied — PASS (with 1 authorized expansion noted)

| Res | Mandate | Evidence | Result |
|---|---|---|---|
| 1 | `FAIL`→`FAIL_TERMINAL` keep `"fail"`; add `FAIL_RECOVERABLE="fail_recoverable"` | models.py:49-50; codebase-wide rename clean (grep `TaskStatus.FAIL\b` minus `_TERMINAL/_RECOVERABLE` → empty) | PASS |
| 2 | `is_failure` includes both + INCOMPLETE | models.py:59-60 `(FAIL_TERMINAL, FAIL_RECOVERABLE, INCOMPLETE)` | PASS* |
| 3 | ~42 tests (49 mandated, 55 total) | 35 new (12+13+2+8) + edits across 5 files | PASS (see note) |
| 4 | Phase 1 line-number discovery completed | classification site confirmed at executor.py:1016-1023; helpers at documented lines | PASS |
| 5 | `RecoveryStatus` in recovery.py | recovery.py:58 | PASS |

*Resolution-2 DIVERGENCE (benign, authorized): gate-resolutions.md:53 wrote the contract as `(FAIL_TERMINAL, FAIL_RECOVERABLE)` — only two members. The shipped code (models.py:60) ALSO includes `INCOMPLETE`. The spawn brief's authoritative criterion 4(2) explicitly states "is_failure widened to include both + INCOMPLETE", so the implementation matches the higher-authority directive, and including INCOMPLETE (a non-success terminal) in the failure set is semantically correct for halt logic. Classified as Authorized expansion, not Drift. No fix required.

---

## Criterion 5 — TB-Add-1..8 spirit on delivered code — PASS

- No `TODO`/`FIXME`/`XXX`/`NotImplementedError`/placeholder in recovery.py or rerun_tasks.py (grep empty).
- The one "STUB" is `ReflectReportNominator` (recovery.py:164-230): a *documented, functional* v4.3.0 stub that fully parses JSON+YAML and filters regression/drift entries; it returns `[]` only because the v4.4.0 reflect-report schema is not yet frozen, and emits a `reflect_report_nominator_v43_stub` debug event. This is deliberate forward-compat scaffolding, not dead/half-built logic — TB-Add-1 spirit satisfied (no abandoned function body).
- No XL-item half-build: every function has a complete body + docstring + error handling. No dead code paths found (see Criterion 6 LOC adjudication for line-by-line).
- Lint clean (no unused imports / vars), confirming no orphaned helpers at the linter level.

---

## Criterion 6 — LOC overage adjudication — VERDICT: JUSTIFIED (no bloat, no fix needed)

**recovery.py = 687** (budget ~250, +175%). Composition: code ~405, docstring ~128, comment 56, blank 98 (41% non-code). 6 classes / 13 functions, each a distinct responsibility:
RecoveryStatus enum, RecoveryBundle + RecoveryBundleRef dataclasses (parallel to PhaseResult), Nominator Protocol + ManualNominator + ReflectReportNominator (forward-compat strategy split), `compute_tasklist_sha256`, `write_recovery_audit_log`, `acquire_recovery_lock`/`release_recovery_lock` (PID-liveness + stale-reclaim + atexit/SIGTERM, ~70 lines on their own), `retry_count_for_task`, and the 7-step `merge_recovery_bundle` engine (~300 lines — each step is a *different* file operation: transcript rename, checkpoint rename, errors rename, manifest write, execlog events, supersede link, result-json rewrite with R-F3 no-data-loss preservation). No two steps duplicate logic.

**rerun_tasks.py = 1425** (budget ~280, +409%). Composition: code ~880, docstring ~231, comment 126, blank 188 (38% non-code). 30 functions, ALL reachable (unused-function scan: every fn has ≥1 caller). The bulk is the 15-step `run_rerun_tasks` orchestrator plus six well-factored sections: extraction+round-trip (A), bundle/sub-index (B), results-driven dependency walker (C, with 3 nested helpers), legacy transcript fallback (D), checkbox/provenance mutation with shared `_split_rerun_block`/`_flip_checkbox_in_block` primitives (E — this is GOOD factoring, the flip/restore/finalize trio reuse the same two primitives rather than copy-pasting), and stash/restore (F). The DIVERGENCE NOTE comment blocks (≈40 lines total) document where the implementation legitimately departed from literal TDD text after source verification — these are audit-valuable, not bloat.

**Specific dead/duplicate code found: NONE.** No copy-paste blocks, no unused helpers, no shadow implementations. The +budget overage is a budgeting-estimate miss (the ~250/~280 figures did not account for the 7 safety defenses + 38-41% documentation density + the forward-compat Nominator split), NOT engineering bloat. **No fix applied** — there is nothing removable without deleting real functionality or audit documentation.

---

## Criterion 7 — SHA-guard self-trip — VERDICT: REAL ORDERING DEFECT (recorded for qualitative gate + release decision; NOT fixed here)

**This is a genuine defect that defeats the R-F6 / §T8.1 purpose on the happy path.** Precise line evidence in `rerun_tasks.py::run_rerun_tasks`:

1. **Step 4 SHA capture (line 1275):** `source_sha = compute_tasklist_sha256(phase_obj.file)` — hashes the source tasklist in its pristine pre-rerun state. Captured ONCE; never re-captured (confirmed: only assignments are 1275 + the unrelated extraction-local one at 174).
2. **Step 10 provenance write (line 1323):** `restore_info = flip_target_checkboxes(phase_obj.file, resolved, bundle)` → internally calls `_atomic_write_text(phase_tasklist, block + body)` (rerun_tasks.py:782), which PREPENDS the `<!-- SUPERCLAUDE-RERUN ... -->` provenance block to `phase_obj.file`. The file on disk is now byte-different from when `source_sha` was taken.
3. **Step 12 SHA compare (lines 1356-1357):** `current_sha = compute_tasklist_sha256(phase_obj.file)` then `if current_sha != source_sha and not force_merge:` raise abort. Because step 10 mutated the very same file, `current_sha != source_sha` is **always True** on a successful merge-back path.

**Consequence:** `sprint rerun-tasks --merge-back` (the DEFAULT, commands.py:441) always aborts with "Source tasklist modified since rerun started." unless the operator adds `--force-merge`. The guard cannot distinguish the engine's OWN provenance write from a real external operator edit, so it fires on itself. The intended R-F6 protection (detect a human editing the tasklist mid-rerun) is rendered unusable in the common case — and worse, the workaround (`--force-merge`) disables the guard entirely, so a genuine concurrent edit would also be ignored.

**Test-coverage gap (why Phase 5 green did not catch it):** the AC5 test `test_source_tasklist_sha_mismatch_aborts` (test_rerun_tasks_failure_modes.py:288-322) MOCKS `execute_sprint` and performs its mid-flight mutation INSIDE that mock — it asserts the *external-edit* path aborts, which it does. But because `execute_sprint` is stubbed and the test's seed path means step 10's real provenance-write effect on the SHA is not isolated/asserted, the test passes for the *external-edit* reason while the *self-trip* (step-10-prepend) reason is structurally present and untested. `test_force_merge_proceeds_with_warning` (324-355) confirms `--force-merge` is the only way through. No test asserts that an UNEDITED tasklist merges cleanly without `--force-merge` — that missing test is exactly the one that would have failed.

**Why NOT fixed here (per spawn instruction):** the correct fix is a design choice between (a) re-capturing `source_sha` AFTER step 10's provenance write (hash the post-flip state), (b) computing the guard SHA over the source EXCLUDING the provenance block region (strip `_RERUN_BLOCK_RE` before hashing on both capture and compare), or (c) capturing the SHA of `body` (content minus provenance block) at both points. Option (b)/(c) preserve the guard's real intent (detect edits to the *task content*, ignore the engine's own provenance marker); option (a) weakens it. This is a R-F6 semantics decision for the qualitative gate (Step 6.7) and the release owner — not a trivial, obviously-correct edit. **Recorded as IMPORTANT finding; no behavioral change made.**

---

## Criterion 8 — No fake-green / fabricated coverage — PASS

- 35 new tests across 4 files; 127 `assert` statements (49 + 34 + 16 + 28). No bare-`pass` / docstring-only test bodies (regex scan empty).
- All 8 ACs map to named tests with real assertions on output / file state / exit codes (verified AC5 body directly: asserts byte-exact abort message + exit_code).
- Tests live in the project `tests/sprint/` suite as proper pytest files (durable, CI-compatible) — not inline `python -c` one-liners.
- The Phase 5 gate conclusion (no fake-green) holds at task level. NOTE: the one real coverage WEAKNESS is the missing happy-path "merges without --force-merge" assertion (see Criterion 7) — this is an absence-of-test, not a fabricated/lying test, so it does not constitute fake-green; it is folded into the Criterion 7 IMPORTANT finding.

---

## Confidence Gate

- [x] C1 BUILD_REQUEST goals — VERIFIED (commands/executor/recovery reads + lint + import + new-test run)
- [x] C2 Cross-phase consistency — VERIFIED (producer/consumer grep + reads)
- [x] C3 "ensuring" clauses — VERIFIED (6 spot-checks against code)
- [x] C4 Resolutions 1-5 — VERIFIED (models read + rename grep + import value check)
- [x] C5 TB-Add spirit — VERIFIED (stub scan + lint)
- [x] C6 LOC adjudication — VERIFIED (AST composition + unused-function scan)
- [x] C7 SHA self-trip — VERIFIED (source_sha lifecycle trace + AC5 test read)
- [x] C8 No fake-green — VERIFIED (assert-density + no-op scan + AC5 body)

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool-engagement minimum satisfied (20 tool calls ≥ 8 checklist items; each maps to a specific criterion).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | rerun_tasks.py:1275 + :1323 + :1356-1357 | SHA-guard self-trip: step-10 provenance write mutates `phase_obj.file` between the step-4 `source_sha` capture and the step-12 re-hash, so `--merge-back` always aborts without `--force-merge`; defeats R-F6/§T8.1 and the `--force-merge` workaround disables the guard entirely. | Design decision (NOT applied here): hash the source EXCLUDING the `_RERUN_BLOCK_RE` provenance region at BOTH capture and compare (strip-then-hash), OR re-capture after step 10. Route to qualitative gate (6.7) + release owner. |
| 2 | MINOR | test_rerun_tasks_failure_modes.py (AC5 class) | Missing happy-path test asserting an UNEDITED tasklist merges WITHOUT `--force-merge`. The absent test is exactly the one that would expose Issue #1. | Add `test_unedited_tasklist_merges_without_force_merge` once Issue #1's design fix lands. Not fixed here (depends on Issue #1 resolution). |
| 3 | INFO (no action) | models.py:60 vs gate-resolutions.md:53 | `is_failure` includes INCOMPLETE beyond the 2-member contract in gate-resolutions.md; matches the spawn brief's authoritative directive. Authorized expansion. | None. |

## Actions Taken (Fixes Applied)

**None.** No fix was applied in-place this cycle:
- Issue #1 is explicitly out-of-scope for a behavioral fix per the spawn instruction ("Do NOT attempt a behavioral fix here unless trivial and clearly correct — this is a design decision; record it as a finding"). It is non-trivial (3 viable designs with different R-F6 semantics).
- Issue #2 is dependent on Issue #1's resolution (the assertion shape depends on the chosen fix).
- Issue #3 is a benign authorized expansion requiring no change.

No re-run of ruff/pytest was needed because no source or test file was modified. The earlier verification runs (ruff "All checks passed!"; 35/35 new tests green) reflect the final, unmodified state.

---

## Overall Verdict

**VERDICT: FAIL**

Rationale: The implementation is structurally excellent — all 12 flags wired, the 7-step merge engine sound, all 5 resolutions applied, 35 real tests green, lint clean, LOC justified with no bloat or dead code, no fabricated coverage, cross-phase wiring consistent. HOWEVER, zero-tolerance QA cannot PASS a release whose DEFAULT command path (`rerun-tasks --merge-back`) is broken by the Criterion-7 SHA-guard self-trip: a clean, unedited rerun aborts without `--force-merge`, and the only workaround disables the very safety guard it bypasses. This is an IMPORTANT functional defect in the headline feature, surfaced with precise line evidence (rerun_tasks.py:1275/1323/1356) and an accompanying test-coverage gap. Per the gate's "any issue regardless of severity blocks PASS" rule and the routed-to-you mandate, the structural gate result is FAIL, with the SHA-guard defect handed to the qualitative gate (Step 6.7) and the release decision. The fix is a bounded design choice (strip-provenance-then-hash is the recommended option) — not a teardown.

## QA Complete
