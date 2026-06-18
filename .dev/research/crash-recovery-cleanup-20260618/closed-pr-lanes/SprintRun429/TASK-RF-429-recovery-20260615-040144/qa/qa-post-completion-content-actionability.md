# QA Report — Post-Completion Cross-Phase (Content / Actionability lens)

**Verdict: FAIL** — 3 integrated-behavior coverage gaps (1 IMPORTANT, 2 MINOR). All 5 audited claims are *substantially* true, but the single-session (P4) re-spawn/cap path and the P6 observability events have no executable guard; a regression there ships green.

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery
**Date:** 2026-06-18
**Phase:** task-qualitative (post-completion actionability)
**Fix authorization:** false (report-only)
**Suite status:** 388 passed (the 10 named files), confirmed green before and after mutation probing; tree restored byte-exact.

---

## Self-Audit (INV-019)

**(a) Reliance list — structural facts taken as given (not re-verified):**
- Relied on the prior rf-qa structural pass for section numbering / file-existence of the manifest and task tree.

**(b) Independent semantic checks (tool-verified, ≥1 required):**
- Re-ran the full 10-file suite myself → 388 passed (Bash).
- Read the executor re-spawn loop source (executor.py:983-1145 per-task; 2119-2150 single-session) and confirmed the seam tests drive the REAL production loop, not a parallel test path.
- **Mutation probes** (the load-bearing evidence): disabled the single-session retry branch → 0 failures (gap); neutered the per-task latch → storm test failed as it should (claimed-green item is genuinely non-vacuous). Restored byte-exact.
- Grepped the entire `tests/sprint/` tree for the P6 event emitters → zero references.

---

## Items Reviewed (the 5 audited claims)

| # | Claim | Result | Evidence |
|---|-------|--------|----------|
| 1 | Re-spawn loop tested via `subprocess_factory` with realistic 429 scenarios | **PASS (per-task) / PARTIAL (single-session)** | Per-task: test_executor.py:770-956 cover single-429→clean, cooldown-fast-halt, cap, real-failure-fallthrough, parallel-latch-storm-bound, exact-cap. These drive the real `execute_phase_tasks(reset_policy=...)`. Single-session: only `all_account_cooldown` (fast halt) — see Gap #1. |
| 2 | Detector tests load real fixtures + four-way + subtype-trap | **PASS** | test_monitor.py:243-343 — six fixtures, four-way discrimination, resolved-model capture, subtype-trap (308), conservative-default (322), shared-core equivalence (337). Fixtures match ground-truth bodies verbatim. |
| 3 | Resume re-runs a provider-exhausted task | **PASS** | test_resume.py:155-193 — phase-3-result.json with `fail_provider_exhausted` ⇒ `"T03.02" in plan.rerun_task_ids`, phase status `provider_exhausted` (not COMPLETE). Non-vacuous. |
| 4 | Halt golden-string / aienv / CLI-help / doc⇆CLI parity are non-vacuous | **PASS** | Golden-string: test_models.py:403-438 asserts single `--resume` line + `--model sonnet` + exhausted-model + CLIProxyAPI rationale, and None-suggested never fabricates `--model`. aienv: test_aienv.py covers resolved-id match, alias match, proxy-slot rotation, None-safety, identical-resolves-to-None. Parity: test_sprint_docs_cli_parity.py asserts BOTH phantom and missing directions + a real `Default: \`8\`` check. CLI help: test_cli_contract.py:51. |
| 5 | Nominator-exclusion would fail if exclusion removed | **PASS** | test_rerun_tasks.py:348-451 pins BOTH surfaces; source-verified the real caller filters (`rerun_tasks.py:1468-1474`, not just a test-side mirror), and a control asserts the terminal task IS still kept. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | **IMPORTANT** | executor.py:2119-2150 (single-session phase path) / tests/sprint/test_executor.py | **Single-session SINGLE_ACCOUNT_LIMIT re-spawn + cap→halt is untested.** Every single-session integration test (`_run_single_session_provider_cooldown`, lines 437-532) feeds `all_account_cooldown.jsonl`, which takes the fast-path `break` at 2138 on attempt 1. The `RETRY_NEW_SESSION` `continue` branch (2127-2137) and the single-account-429×cap→`PROVIDER_EXHAUSTED` halt — which **spec §6 explicitly lists** as a single-session case ("single-session cooldown → halt; single-429×cap → halt") — have zero coverage. **Mutation-proven:** disabling the single-session retry branch (`if False and action is Action.RETRY_NEW_SESSION`) caused **0 test failures** (307 passed). The per-task path covers retry+cap; the single-session path does not. | Add a single-session integration test using a scripted single-account-429 transcript that asserts (a) ≥1 re-spawn (`continue` taken), and (b) cap-exhaustion ⇒ `PhaseStatus.PROVIDER_EXHAUSTED` with the resolved `exhausted_model`. |
| 2 | **MINOR** | logging_.py:251/273 + executor.py:2130-2148, 1090-1100 (4 P6 emit sites) | **P6 observability events have no test.** `write_session_reset` / `write_account_exhaustion_halt` exist and are wired at 4 sites, but grep of the entire `tests/sprint/` tree finds **zero** references to these emitters or to `session_reset` / `account_exhaustion_halt` events in `execution-log.jsonl`. The manifest's P6 gate is "Events emitted" — that gate has no executable guard, and the manifest's own Tests table lists no P6 event test. A regression that drops either event ships green. | Add a test asserting `execution-log.jsonl` receives a `session_reset` event on a re-routed attempt and an `account_exhaustion_halt` event on final halt (per-task and/or single-session). |
| 3 | **MINOR** | executor.py:2244-2246, 2819 vs test_executor.py:846-883 | **End-to-end single-session JSON persistence of `exhausted_model`/`halt_reason` not asserted via the real path.** The cap test hand-builds a `PhaseResult` and calls `_write_phase_result_json` directly (846-878), bypassing the production wiring that copies `exhausted_model` onto the phase result (2244-2246) and serializes it (2819). The single-session integration test asserts in-memory `status==PROVIDER_EXHAUSTED` but never reads back `exhausted_model`/`halt_reason` from a `phase-N-result.json` produced by `execute_sprint`. Resume/halt-UX both consume those persisted fields, so the seam matters. | Have the single-session cooldown integration test read `config.phase_result_json(phase)` after `execute_sprint` and assert `halt_reason=="provider_exhaustion"` and `exhausted_model=="claude-opus-4-8"`. |

---

## Actions Taken

Report-only (`fix_authorization: false`). No files modified. All mutation probes restored; executor.py confirmed byte-identical to the pre-probe working tree, logging_.py clean vs HEAD, 388 tests green.

---

## Confidence

Verified: 5/5 audited claims | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
Tool engagement: Read: 7 | Grep: 6 | Bash (incl. 3 mutation probes + 3 suite runs): 9 | Glob: 0

The mutation probes are the decisive evidence: a claimed-green item (latch) failed under mutation as required, while the flagged single-session retry path survived mutation untouched — calibrating that these gaps are real, not uniform alarmism.

## Recommendations

- Resolve Gap #1 before relying on single-session (whole-phase, non-per-task) sprints for 429 recovery — that path's retry/cap logic is currently unguarded. The per-task (parallel) path is well-covered and trustworthy.
- Gaps #2/#3 are observability/persistence seams; lower risk but both feed downstream consumers (log forensics, resume, halt-UX) and the manifest's P6 gate is currently unfalsifiable.
- No regressions found in the 4 PASS claims; the detector, per-task loop, resume routing, golden-string/aienv/parity, and nominator-exclusion are all genuinely exercised.

## QA Complete
