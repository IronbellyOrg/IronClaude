# Build Inventory — sc:pr-submit V1.0

**Generated:** 2026-06-11 11:18
**Step:** 1.4 (L1 discovery)
**Sources:** `research/01-component-inventory.md`, `research/04-test-infra-and-deterministic-core.md`, `research/08-runlog-recovery-fsm-validation.md`, and the authoritative task-file checklist items.

> **NAMING AUTHORITY:** The research files use the EARLIER names `submit_pr` / `sc-submit-pr-protocol` / `tests/submit_pr/` / `commands/submit-pr.md` / `severity.py`. The TASK FILE is authoritative and corrects these to **`pr_submit`** (underscored Python pkg), **`sc-pr-submit-protocol`** (hyphenated skill dir), **`tests/pr_submit/`**, **`commands/pr-submit.md`**, **`severity_router.py`**, plus a dedicated **`recovery.py`** module. All paths below use the CORRECTED authoritative names.

## Summary Counts

| Group | Count | Detail |
|-------|------:|--------|
| Skill SKILL.md | 1 | `sc-pr-submit-protocol/SKILL.md` |
| Skill refs | 8 | state-machine, detection-contract, augment-poll, severity-routing, finding-verify, troubleshoot-dispatch, thread-reply, loop-guard |
| Skill scripts (bash) | 2 | poll-augment-review.sh, reply-resolve-thread.sh |
| Python core modules | 9 | `__init__` + models, fsm, severity_router, loop_guard, classifier, detection, run_log, recovery |
| Command | 1 | `commands/pr-submit.md` |
| Hook EDIT | 1 | `hooks/scripts/offer-pr-review.sh` |
| pyproject EDIT | 1 | 4 markers: loop_guard, autonomy, recovery, p0 |
| Test modules | 21 | + `__init__.py` + `conftest.py` (23 files total) |
| Test fixtures (JSON) | 18 | 10 finding-* + 8 review/sequence/crash/drift |
| **Total NEW files** | **62** | 11 skill + 9 python + 1 cmd + 23 test + 18 fixtures |
| **Total EDIT files** | **2** | hook + pyproject |
| **REUSE (no edit)** | **2** | severity-rubric.md, evidence-validator agent / troubleshoot SKILL.md |

## Skill Package — `src/superclaude/skills/sc-pr-submit-protocol/`

| Path | C-ID | Status | Spec §-or-line | Primary test | Build step |
|------|------|--------|----------------|--------------|-----------|
| `SKILL.md` | C1 | NEW | §1.1, §5, FR-1/FR-2, §10 (VAL) | test_skill_parse, test_static_grep | 4.4 (4.4/6.3/7.4 extend) |
| `refs/state-machine.md` | C1/FSM | NEW (core-pure) | §5.1–5.4, INV-016 | test_static_grep T-N50 | 4.1 (6.3 extend) |
| `refs/detection-contract.md` | DET | NEW (`locked:false`) | §7 (lines 473–500) | test_detection_contract T-210 | 2.1 |
| `refs/augment-poll.md` | C2 | NEW | FR-2.1/2.3/2.5 | test_timeout, test_rate_limit | 6.1 |
| `refs/severity-routing.md` | C3 | NEW (core-pure) | FR-3.1/3.2 | test_severity_router, test_static_grep T-N50 | 5.1 |
| `refs/finding-verify.md` | C3a | NEW | FR-3.5 (lines 193,195–207) | test_finding_verify | 5.2 |
| `refs/troubleshoot-dispatch.md` | C3b | NEW | FR-3.2/3.3/3.4 | test_troubleshoot_seed | 5.3 |
| `refs/thread-reply.md` | C4 | NEW | FR-6.1/6.5 (lines 234,238) | test_reply_resolve | 7.2 |
| `refs/loop-guard.md` | LG | NEW (core-pure) | FR-6.3 INV-001, §11 | test_loop_guard, test_static_grep T-N50 | 8.1 |
| `scripts/poll-augment-review.sh` | C2 | NEW | §6.3 / R06 §2.1 | test_static_grep T-104 | 7.1 |
| `scripts/reply-resolve-thread.sh` | C4 | NEW | R06 §2.2/2.3 | test_static_grep T-104 | 7.3 |

## Python Deterministic Core — `src/superclaude/pr_submit/` (UNDERSCORED, importable)

| Path | C-ID | Status | Spec §-or-line | Primary test | Build step |
|------|------|--------|----------------|--------------|-----------|
| `__init__.py` | core | NEW | R04 §C (top-level re-exports) | (all imports) | 2.2 / 4.3 / 5.1 |
| `models.py` | core | NEW | §11.3 + §12.1 (33 events), enums | test_run_log, all | 2.2 |
| `detection.py` | DET | NEW (core-pure) | §7, FR-2.1/2.2 | test_detection_contract, test_timeout | 2.3 |
| `classifier.py` | DET | NEW (core-pure) | §7 classify() | test_detection_contract, test_autonomy_gates | 2.3 |
| `fsm.py` | C1 | NEW (core-pure) | §5.2/5.3, §10, INV-016 | test_autonomy_gates, test_validation_gate | 4.2 (6.2/7.4 extend) |
| `severity_router.py` | C3 | NEW (core-pure) | FR-3.1/3.2 | test_severity_router | 5.1 |
| `loop_guard.py` | LG | NEW (core-pure, P0) | FR-6.3 INV-001 | test_loop_guard T-626-OFF-BY-ONE | 8.2 |
| `run_log.py` | §11 | NEW (core-pure) | §11.1–11.4 | test_run_log, test_idempotency | 8.3 (NFR-7 redaction) |
| `recovery.py` | §12 | NEW (core-pure) | §12.1 INV-007 | test_crash_recovery | 8.4 |

## Command + Hook + pyproject

| Path | C-ID | Status | Spec §-or-line | Primary test | Build step |
|------|------|--------|----------------|--------------|-----------|
| `src/superclaude/commands/pr-submit.md` | C1 | NEW | FR-1.1, R02 §4 | (architecture lint) | 9.1 |
| `src/superclaude/hooks/scripts/offer-pr-review.sh` | C5 | **EDIT** (src/-only) | FR-7.1 | test_hook_update T-701 | 9.2 |
| `pyproject.toml` (markers) | markers | **EDIT** | R04 §E (4 markers) | (collection) | 9.3 |

## Test Suite — `tests/pr_submit/`

| Path | Status | Test IDs | Build step |
|------|--------|----------|-----------|
| `__init__.py` | NEW | — | 10.1 |
| `conftest.py` | NEW | mock_gh, mock_monitor, fixture_findings, tmp_skill_dir, load_fixture | 10.1 |
| `test_detection_contract.py` | NEW | T-201,202,203,210,211,212 | 2.4 |
| `test_skill_parse.py` | NEW | T-101,102,103,111,112,113 | 4.5 |
| `test_monitor_arm.py` | NEW | T-109,110,230 | 4.6 |
| `test_autonomy_gates.py` | NEW | T-401,402,410,411,412,413,420,430,ZERO-EDIT-NO-PUSH | 4.7 |
| `test_severity_router.py` | NEW | T-301,302,310,311,312,N30 | 5.4 |
| `test_finding_verify.py` | NEW | T-340,341,342 | 5.5 |
| `test_troubleshoot_seed.py` | NEW | T-320,330,331 | 5.6 |
| `test_validation_gate.py` | NEW | T-501,502,510,511,520,521,522 | 6.4 |
| `test_timeout.py` | NEW | T-220,221,222,231 | 6.5 |
| `test_rate_limit.py` | NEW | T-N10,N11 | 6.6 |
| `test_reply_resolve.py` | NEW | T-601,602,603,610,611,630,640,641,642,FRESH-COMMENT-NO-DOUBLE-FIX | 7.5 |
| `test_loop_guard.py` | NEW | T-620..629,626-OFF-BY-ONE,VANISHED-MONO | 8.5 |
| `test_run_log.py` | NEW | T-N20,N21,N22 (+ NFR-7 T-N51, NFR-8 T-N52) | 8.6 |
| `test_idempotency.py` | NEW | T-N01,N02,FRESH-COMMENT-NO-DOUBLE-FIX | 8.7 |
| `test_crash_recovery.py` | NEW | FM-1..12,CRASH-WINDOW-NO-DOUBLE-PUSH | 8.8 |
| `test_validated_not_verified.py` | NEW | VALIDATED-NOT-VERIFIED (INV-015/AC-13) | 8.9 |
| `test_edge_cases.py` | NEW | EC-1..EC-16 | 8.10 |
| `test_hook_update.py` | NEW | T-701,702,703 | 9.4 |
| `test_static_grep.py` | NEW | T-104,N40,N41,N50 (+ NFR-7 T-N51) | 9.5 |
| `test_pre_pr_checks.py` | NEW | T-106,107,108 | 9.6 |

## Test Fixtures — `tests/pr_submit/fixtures/` (18, synthetic per §18.4)

| Group | Fixtures | Build step |
|-------|----------|-----------|
| finding-* (10) | finding-medium, finding-high, finding-medium-high, finding-empty, finding-max (50), finding-duplicate, finding-fresh-comment-id, finding-needs-human, finding-malformed, finding-ungroundable | 10.2 |
| review/seq/crash/drift (8) | review-clean, review-with-findings, review-non-augment, review-interleaved, round-sequence-2, round-sequence-residual-x3, crash-after-push-before-completed, behavioral-drift | 10.3 |

## REUSE-by-reference (NO edit)

| Path | Reused for | Build step |
|------|-----------|-----------|
| `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` | C3 severity-routing DEFERS-TO (5-step remap + floor/ceiling table) | 5.1 |
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` + `evidence-validator` agent | C3a/C3b grounding floor + dispatch flag surface | 5.2, 5.3 |

**Verdict:** Build surface enumerated. 62 NEW files + 2 EDITs + 2 REUSE targets. Every C1–C6/DET/LG path, every `pr_submit/*.py` module, and every `tests/pr_submit/` module+fixture is captured with the authoritative corrected naming. Downstream build items read this inventory by path.
