# QA Input Manifest — Phase Gate B (Final Build QA)

**Generated:** 2026-06-11 13:00
**Step:** PGB.1 (L6 aggregation over the COMPLETE build)
**Full-suite result:** 131 passed, 85% coverage of `superclaude.pr_submit` (`full-suite-summary.md`)

## Python deterministic core — `src/superclaude/pr_submit/` (C1/C3/LG/§11/§12)

| Path | Lines | Component | Spec |
|------|------:|-----------|------|
| `__init__.py` | 60 | top-level re-exports | R04 §C |
| `models.py` | 205 | EventType(33), Severity, MonitorState, Finding, SkillResult, PushDecision | §11.3+§12.1, §5.1 |
| `detection.py` | 155 | DetectionContract loader (T-210), poll_augment_review | §7, FR-2 |
| `classifier.py` | 86 | pure 3-state classify | §7, FR-2.2 |
| `fsm.py` | 802 | transition table, gates, INV-016, run_skill, validation, dispatch, push triad, reply, audits, pre-PR | §5/§10/§12 |
| `severity_router.py` | 156 | remap_severity (rubric by-reference), route | FR-3.1/3.2 |
| `loop_guard.py` | 78 | RoundCounter, should_halt (INV-001 P0) | FR-6.3 |
| `run_log.py` | 237 | write-ahead JSONL, 5 idempotency sets, NFR-7 redaction | §11 |
| `recovery.py` | 135 | crash-window 3-way (INV-007) | §12.1 |

## Skill package — `src/superclaude/skills/sc-pr-submit-protocol/`

| Path | Lines | Component |
|------|------:|-----------|
| `SKILL.md` | 132 | C1 orchestrator (FSM + ordinal gates + VAL) |
| `refs/state-machine.md` | 114 | C1/FSM (core-pure) |
| `refs/detection-contract.md` | 50 | DET (`locked:false`) |
| `refs/augment-poll.md` | 49 | C2 poller contract |
| `refs/severity-routing.md` | 55 | C3 (core-pure, DEFERS-TO rubric) |
| `refs/finding-verify.md` | 61 | C3a verify-before-remediate |
| `refs/troubleshoot-dispatch.md` | 51 | C3b dispatch |
| `refs/thread-reply.md` | 74 | C4 reply+resolve |
| `refs/loop-guard.md` | 73 | LG (core-pure) |
| `scripts/poll-augment-review.sh` | 61 | C2 poller (gh) |
| `scripts/reply-resolve-thread.sh` | 102 | C4 wrapper (gh) |

## Command + hook + markers

| Path | Lines | Component |
|------|------:|-----------|
| `src/superclaude/commands/pr-submit.md` | 80 | C1 command (Activation present) |
| `src/superclaude/hooks/scripts/offer-pr-review.sh` | 76 | C5 hook EDIT (both mentions) |
| `pyproject.toml` markers | +4 | loop_guard, autonomy, recovery, p0 |

## Test suite — `tests/pr_submit/` (21 modules + conftest + __init__, 18 fixtures)

`__init__.py`, `conftest.py`, `test_detection_contract.py`, `test_skill_parse.py`,
`test_monitor_arm.py`, `test_autonomy_gates.py`, `test_severity_router.py`,
`test_finding_verify.py`, `test_troubleshoot_seed.py`, `test_validation_gate.py`,
`test_timeout.py`, `test_rate_limit.py`, `test_reply_resolve.py`, `test_loop_guard.py`,
`test_run_log.py`, `test_idempotency.py`, `test_crash_recovery.py`,
`test_validated_not_verified.py`, `test_edge_cases.py`, `test_hook_update.py`,
`test_static_grep.py`, `test_pre_pr_checks.py`. Fixtures: 18 JSON (10 finding-* + 8 review/seq/crash/drift).

## Key spec corrections applied
1. Python core at `pr_submit/` (underscored, importable), NOT in the hyphenated skill dir.
2. `--cov=superclaude.pr_submit` (not the unresolvable hyphenated target).
3. EXACTLY 4 markers (loop_guard/autonomy/recovery/p0) — `loop` absent.
4. 33 run-log event types (32 §11.3 + `push_aborted_or_not_landed` §12.1).
5. No `--depth quick --fix` anywhere (T-N40 asserts).
