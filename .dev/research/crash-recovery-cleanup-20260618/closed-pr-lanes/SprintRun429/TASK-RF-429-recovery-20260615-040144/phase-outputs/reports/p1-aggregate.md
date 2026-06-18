# Phase 2 (P1 — Detection) Aggregate Manifest

**Phase:** P1 — Provider-Failure Detection (zero behavior change)
**Generated:** 2026-06-15 (Step PG2.1), files discovered via Glob/grep.

## Source files

| File | Purpose | Key symbols (verified line) |
|------|---------|------------------------------|
| `src/superclaude/cli/sprint/monitor.py` | Detector core + types added in the count_turns→OutputMonitor insertion zone | `from enum import Enum` + `from dataclasses import dataclass` imports (added); `_RE_ALL_ACCOUNT` (L41, named group `model`), `_RE_SINGLE_ACCOUNT` (L44); `class ProviderFailure(Enum)` (L263, 4 members NONE/SINGLE_ACCOUNT_LIMIT/ALL_ACCOUNT_COOLDOWN/OPERATION_TIMEOUT); `@dataclass(frozen=True) class ProviderFailureSignal` (L279, `kind` + `resolved_model: str\|None=None`); `_provider_failure_from_text` (L291, shared text core); `detect_provider_failure` (L341, path wrapper) |

## Test files

| File | Purpose |
|------|---------|
| `tests/sprint/test_monitor.py` | `TestDetectProviderFailure` (12 cases) appended; new imports + `_FIXTURES` path |

## Fixtures (`tests/sprint/fixtures/exhaustion/`)

| Fixture | Expected `ProviderFailure` kind | Notes |
|---------|--------------------------------|-------|
| `single_account_429.jsonl` | `SINGLE_ACCOUNT_LIMIT` | api_retry(attempt=3) + terminal 429 + "would exceed your account's rate limit"; subtype is "success" (trap) |
| `all_account_cooldown.jsonl` | `ALL_ACCOUNT_COOLDOWN` | resolved_model captured = `claude-opus-4-8`; ≥2 prior assistant usage lines |
| `operation_timeout.jsonl` | `OPERATION_TIMEOUT` | `api_error_status:null` + "API Error: The operation timed out." |
| `api_retry_maxed.jsonl` | `SINGLE_ACCOUNT_LIMIT` | attempt==max_retries==10; LAST result event is load-bearing (edge #6) |
| `task_failure_real.jsonl` | `NONE` | subtype error_during_execution, no 429 (false-positive guard) |
| `clean_pass.jsonl` | `NONE` | is_error:false success envelope |

## Test/lint evidence

- `phase-outputs/test-results/p1-pytest.txt` — 39 passed, 0 failed
- `phase-outputs/test-results/p1-summary.md` — pass summary (12 new + 27 existing, no regressions)
- `phase-outputs/test-results/p1-lint.txt` — P1 files pass ruff format + check (exit 0); repo-wide drift is pre-existing/out-of-scope
- `phase-outputs/test-results/p1-verify-sync.txt` — verify-sync exit 0 (after one-time `make sync-dev` populating the unsynced worktree `.claude/` mirror; no P1 `.claude/` edits)

## Load-bearing invariants to verify

1. Detector keys ONLY on `is_error` + `api_error_status` of the LAST `{"type":"result"}` event — NEVER `subtype` (a 429's subtype is `"success"`).
2. Four-way discrimination: 429+cooldown-body→ALL_ACCOUNT_COOLDOWN(+model); 429+single-body→SINGLE_ACCOUNT_LIMIT; 429+neither→SINGLE_ACCOUNT_LIMIT (conservative default); api_error_status==None+timeout-body→OPERATION_TIMEOUT; else→NONE.
3. `detect_provider_failure` mirrors `detect_error_max_turns` OSError/empty tolerance; takes only `output_path` (no error_path — stderr 0 bytes for 429).
4. `_provider_failure_from_text` is the shared core; path wrapper delegates to it after the OSError guard (no double parse).
5. `ProviderFailure` is string-valued Enum; `ProviderFailureSignal` is frozen dataclass.
