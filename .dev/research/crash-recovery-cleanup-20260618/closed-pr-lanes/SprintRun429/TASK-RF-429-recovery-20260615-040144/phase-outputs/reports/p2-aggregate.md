# Phase 3 (P2 — Taxonomy + Status) Aggregate Manifest

**Phase:** P2 — Taxonomy + status (FAIL_PROVIDER_EXHAUSTED). **Generated:** 2026-06-15 (Step PG3.1).

## Source files

| File | Edits | Verified lines |
|------|-------|----------------|
| `src/superclaude/cli/sprint/models.py` | `TaskStatus.FAIL_PROVIDER_EXHAUSTED` member (L53) added to `is_failure` (L66) ONLY — NOT is_success. 3 new `TaskResult` fields (L192-194 `failure_class`/`session_resets`/`exhausted_model`), serialized in `to_dict` (L222-224), read in `from_dict` with `.get()` defaults (L251-253). |
| `src/superclaude/cli/sprint/rerun_tasks.py` | `from .monitor import ProviderFailure, _provider_failure_from_text` (L42). New classifier branch (L588-593): `_sig = _provider_failure_from_text(text)`; if kind in (SINGLE_ACCOUNT_LIMIT, ALL_ACCOUNT_COOLDOWN) → return `FAIL_PROVIDER_EXHAUSTED`. Inserted ABOVE the existing is_error/transient/terminal ladder, BELOW the is_error computation. `discover_failed_tasks_from_transcripts` UNCHANGED. |

## Test files

| File | Additions |
|------|-----------|
| `tests/sprint/test_models.py` | `TestProviderExhaustedStatus` (membership/value/is_failure/is_success); `TestTaskResultExhaustionBackCompat` (2 `@backward_compat` round-trip tests) |
| `tests/sprint/test_rerun_tasks.py` | `TestClassifyTranscriptProviderExhaustion` (3 cases: 2 → FAIL_PROVIDER_EXHAUSTED, 1 → FAIL_TERMINAL). Also restored a pre-existing control-test assertion that the append had split. |
| `tests/sprint/test_resume.py` | `test_resume_reruns_provider_exhausted_task` (planner ZERO-EDIT auto-routing) |

## Test/lint evidence

- `phase-outputs/test-results/p2-pytest.txt` — targeted 193 passed; backward_compat marker 20 passed/1 skipped.
- `phase-outputs/test-results/p2-summary.md` — pass summary + note on the split-test fix.
- `phase-outputs/test-results/p2-lint.txt` — P2 files pass ruff format (exit 0) + check (exit 0).
- `phase-outputs/test-results/p2-verify-sync.txt` — verify-sync exit 0.

## Load-bearing facts to verify

1. `FAIL_PROVIDER_EXHAUSTED` is in `TaskStatus.is_failure` but NOT `is_success` (resume re-runs it; never a success).
2. 3 new `TaskResult` fields use `.get()` back-compat in `from_dict` (mirrors `HandoffRecord.from_dict`, NOT the hard-keyed style) — old `phase-N-result.json` round-trips.
3. The `_classify_transcript` branch reuses the shared `_provider_failure_from_text` core (no re-read, no dup parse) and is placed ABOVE the existing is_error ladder so it intercepts first.
4. Planner is ZERO-EDIT: proven by `test_resume_reruns_provider_exhausted_task` (the `_coerce_task_status → TaskStatus("fail_provider_exhausted")` lookup + `not is_success` filter re-runs the task; `_is_pass_family` tolerates the unknown phase status today and after P4).
5. `discover_failed_tasks_from_transcripts` left UNCHANGED (auto-covers via the non-PASS append).
6. **Carried from Phase 2 gate:** the `_provider_failure_from_text` docstring "called by both" is now literally true — `_classify_transcript` (rerun_tasks.py:588) delegates to it.
