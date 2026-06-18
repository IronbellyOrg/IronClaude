# Final Aggregate Manifest — Sprint Run 429 / Account-Exhaustion Recovery (P1-P6)

Cross-phase inventory for the Post-Completion (I17) lens QA. Verifies the FINAL
integrated state of all six phases — the full flow
**detect → policy → executor re-spawn → persistence → resume → halt-UX → events →
nominator-exclusion** — holds together.

## Source files (by producing phase)

| File | Phase(s) | What it contributes |
|------|----------|---------------------|
| `src/superclaude/cli/sprint/monitor.py` | P1 | `ProviderFailure` enum, `ProviderFailureSignal`, `_RE_ALL_ACCOUNT`/`_RE_SINGLE_ACCOUNT`, `_provider_failure_from_text`, `detect_provider_failure`, `completed_before_overrun_from_text` (shared core). Keys on LAST result event `is_error`+`api_error_status` (NEVER `subtype`). |
| `src/superclaude/cli/sprint/models.py` | P2,P3,P4,P5 | `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (in `is_failure`); 3 `TaskResult` fields (`failure_class`,`session_resets`,`exhausted_model`) w/ `.get()` back-compat; `PhaseStatus.PROVIDER_EXHAUSTED` (in `is_terminal`, NOT `is_failure`); `PhaseResult.halt_reason`/`exhausted_model`; `build_account_exhaustion_halt`; `SprintResult._exhaustion_halt`/exhaustion-aware `resume_command`/`account_exhaustion_output`; `SprintConfig.max_session_resets=8`. |
| `src/superclaude/cli/sprint/recovery_policy.py` | P3 (NEW) | `Action` enum, `SessionResetPolicy` + pure `decide` truth table. |
| `src/superclaude/cli/sprint/executor.py` | P3,P4,P6 | Per-task re-spawn loop in `_run_one_task` (unlocked spawn / locked latch); single-session re-spawn loop + `PROVIDER_EXHAUSTED` short-circuit + diagnostic-bundle guard; `reset_policy` threaded both call sites; halt_reason/exhausted_model persistence; P6 event emits (4 sites, None-guarded). |
| `src/superclaude/cli/sprint/aienv.py` | P5 (NEW) | os.environ alias reader (OQ-1 option A) + `suggest_alternate_model` (None-safe). |
| `src/superclaude/cli/sprint/commands.py` | P5 | `--max-session-resets` option + `run()` param + `load_sprint_config` threading (hops 1-2). |
| `src/superclaude/cli/sprint/config.py` | P5 | `load_sprint_config` param + `SprintConfig(...)` pass-through (hop 3). |
| `src/superclaude/cli/sprint/logging_.py` | P5,P6 | `write_summary` exhaustion block (P5); `write_session_reset`/`write_account_exhaustion_halt` events (P6). |
| `src/superclaude/cli/sprint/rerun_tasks.py` | P2,P6 | `_classify_transcript` 429 branch (P2, shared core); `select_default_recoverable_tasks` exclusion guard + `run_rerun_tasks` fallback filter (P6). |
| `src/superclaude/cli/sprint/recovery.py` | P6 (READ-ONLY) | Nominators confirmed; no `DriftNominator`; no edit (exclusion lives in rerun_tasks.py). |
| `src/superclaude/cli/sprint/tui.py` | P4 (PC.2 fix) | `STATUS_STYLES`/`STATUS_ICONS` entries for `PhaseStatus.PROVIDER_EXHAUSTED` (magenta) — the PC.2 cross-phase regression fix. |

## Tests + fixtures + docs

| Path | Phase | Purpose |
|------|-------|---------|
| `tests/sprint/fixtures/exhaustion/*.jsonl` (6) | P1 | single_account_429, all_account_cooldown, operation_timeout, api_retry_maxed, task_failure_real, clean_pass. |
| `tests/sprint/test_monitor.py` | P1 | detector unit tests. |
| `tests/sprint/test_models.py` | P2,P4,P5 | taxonomy/serialization, PhaseStatus, halt golden-string. |
| `tests/sprint/test_recovery_policy.py` | P3 (NEW) | `decide` truth table. |
| `tests/sprint/test_executor.py` | P3,P4 | re-spawn loop factory scenarios, single-session. |
| `tests/sprint/test_resume.py` | P2 | resume re-runs provider-exhausted task. |
| `tests/sprint/test_rerun_tasks.py` | P2,P6 | classifier alignment; `TestProviderExhaustionNominationExclusion`. |
| `tests/sprint/test_aienv.py` | P5 (NEW) | suggester via `env=` seam. |
| `tests/sprint/test_cli_contract.py` | P5 | `--max-session-resets` in help. |
| `tests/sprint/test_sprint_docs_cli_parity.py` | P5 (NEW) | doc⇆CLI parity (`parents[2]`). |
| `docs/guides/sprint-cli-tools-release-guide.md` | P5 | `--max-session-resets` entry (Default `8`). |
| `KNOWLEDGE.md` | P6 | re-route-not-wait feature entry. |

## Integrated-state facts to verify (cross-phase)

1. **Full flow holds:** `detect_provider_failure` (P1) → `SessionResetPolicy.decide` (P3) → executor re-spawn/halt (P3/P4) → `failure_class`/`exhausted_model` persistence (P2/P3) → resume re-runs (P2) → exhaustion-aware halt UX (P5) → events (P6) → nominator exclusion (P6).
2. **Membership tuples:** `TaskStatus.FAIL_PROVIDER_EXHAUSTED ∈ is_failure`; `PhaseStatus.PROVIDER_EXHAUSTED ∈ is_terminal`, `∉ is_failure`; both have TUI style+icon (PC.2 fix).
3. **No broken imports** across the new modules (`recovery_policy`, `aienv`) and the shared `monitor` core.
4. **OQ-1 = option A** (os.environ reader), **OQ-2 = option a** (select_default filter + fallback completion). Both decided; rejected alternatives documented-not-shipped.
5. **Full suite:** 1228 sprint tests pass; 19 task files ruff-clean; 21 remaining full-suite failures are pre-existing/unrelated (evidence: `final-full-suite.txt`).
