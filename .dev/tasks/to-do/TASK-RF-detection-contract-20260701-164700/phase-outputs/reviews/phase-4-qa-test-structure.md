# QA Report — Task Integrity / Test-Structure Lens (Phase 4 Tests)

**Topic:** Detection-contract setup — Phase 4 test suite structural QA
**Date:** 2026-07-02
**Phase:** task-integrity (synthesis-gate-equivalent, lens: test-structure)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## VERDICT: PASS

All four checklist items verified with tool evidence across all seven assigned files.
81/81 tests collected and passing. No real-tree writes, no stub-shadowing, no
identity-only tautologies, no true duplicate tests. One MINOR observation is
recorded below (partial assertion overlap) but it does NOT meet the bar for a
duplicate-test FAIL — the overlapping test carries a distinct net-new behavioral
assertion the existing test lacks.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Tests assert BEHAVIOR, not identity/type (no `is not None`-only, no tautologies) | PASS | Read all 7 files. Assertions test state outcomes (`d.state is ContractState.X`), derived values (`d.next_command == "<exact string>"`), provenance flags (`prov.observed is False`), lock/refusal behavior (`pytest.raises(ContractSetupRefused)`), redaction (`SENTINEL not in summary`), FSM arm counts (`arm_recorder.calls == 0/1`), and CLI exit/output. The few `is not None` checks (diagnosis.py:216–218) are paired with behavioral assertions in the same test, not standalone. `test_report_type_and_fields_are_the_real_surface` uses `hasattr` but is explicitly a guard and also asserts `report.passed is (report.result == "passed")` — a real invariant, not a tautology. |
| 2 | Tests use tmp dirs / cwd redirection / monkeypatched override — NONE write the real `.dev/pr-monitor/` | PASS | diagnosis/questions/evidence/validation tests pass `cwd=tmp_path` or build probes under `tmp_path`. Writer tests use `repo_root` fixture = `monkeypatch.chdir(tmp_path)` (writer.py:117). Integration tests monkeypatch `detection._LOCAL_OVERRIDE_PATH` to a `tmp_path` file (documented seam, detection.py:41,51–53). CLI tests wrap every invoke in `CliRunner.isolated_filesystem()`. Source proof: `diagnose()` is read-only (`path.open("rb")`, diagnosis.py:302; no `write_text`/`open(...,"w")`) and `_override_path_for(base, cwd_provided=True)` scopes under supplied cwd. Runtime proof: `find .dev/pr-monitor -newermt "-2 minutes"` returned EMPTY immediately after the full 81-test run — the real tree was not modified. |
| 3 | Tests import REAL symbols from source package (no re-defined stubs) | PASS | Every import resolves to a real source symbol. Verified via grep: `ContractState`(states.py:8), `Diagnosis`/`diagnose`/`declined_by_user`/`render_pr_submit_missing_contract_halt`(diagnosis.py:25,63,207,233), `SETUP_QUESTIONS`/`SetupQuestion`/`SetupAnswers`(questions.py:119,37,15), `derive_candidate`/`FieldProvenance`/`CandidateContract`/`PROVENANCE_OBSERVED`/`LOCKABLE_RESULTS`(candidate.py:63,30,40,14,26), `validate_candidate`/`ValidationReport`(validation.py:68,27), `EvidenceBundle`/`load_evidence`(evidence.py:19,56), `write_lock`/`write_report`/`ContractSetupRefused`(writer.py:76,32,24), `_LOCAL_OVERRIDE_REL`/`_LOCAL_OVERRIDE_PATH`(detection.py:40,41), `classify`/`STATE_POLLING`(classifier.py), `contract_status`/`reflect_group`(commands.py:95,48). No local class/function redefines a production symbol. The one local helper class `_Recorder` (integration test) is a test double for a callable seam, not a shadow of production code. Tests actually execute (81 passed) — dead imports would fail collection. |
| 4 | No test duplicates an existing test in tests/pr_submit or tests/cli/reflect | PASS (1 MINOR note) | Cross-checked new tests against `test_detection_contract.py`, `test_monitor_arm.py`, `test_autonomy_gates.py`, `test_docs_cli_parity.py`. Only `test_detection_contract.py` and `tests/swarm/test_three_layer_artifacts.py` reference overlapping symbols. Overlap analysis below shows each new test exercises a distinct surface or adds a distinct assertion. No identical test found. |

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Overlap Analysis (Checklist #4 detail)

| Existing test | Nearest new test | Verdict |
|---|---|---|
| `test_detection_contract.py::test_contract_setup_next_commands_are_current_and_actionable` (calls `_next_command`/`_contract_status_next_command` helpers directly with `SimpleNamespace`) | `test_contract_setup_diagnosis.py` next_command assertions (asserts `next_command` on a REAL `Diagnosis` from `diagnose()` with on-disk override+evidence) | NOT a duplicate — unit-of-helper vs. integration-through-`diagnose()`. Complementary. |
| `test_detection_contract.py::test_t210_locked_false_halts` (`DetectionContract.load()` HALT) | `test_..._integration.py::test_missing_contract_for_arming_halts_before_monitor_arm` (`for_arming()` HALT + arm-count==0 via recorder through `run_skill`) | NOT a duplicate — different method + downstream arm-gate assertion. New diagnosis module explicitly leaves the loader arm-gate to `test_detection_contract` (docstring lines 116, 20–21). |
| `test_detection_contract.py::test_local_override_arms_without_touching_shipped_source` | `test_..._integration.py::test_post_lock_for_arming_returns_locked_contract` | MINOR overlap — both write a locked override, monkeypatch `_LOCAL_OVERRIDE_PATH`, assert `for_arming().locked is True` + `augment_bot_login == "augmentcode[bot]"` + default `load()` HALTs. The new test adds a distinct net-new assertion the existing one lacks: it drives `run_skill(...)` and asserts `arm_recorder.calls == 1` (the FSM actually arms exactly once). Net-new behavioral coverage → not a true duplicate, but the setup+first-half assertion block is redundant with the existing test. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR (observation, non-blocking) | `test_contract_setup_pr_submit_integration.py::test_post_lock_for_arming_returns_locked_contract` (lines 157–183) | The override-write + `for_arming().locked`/`augment_bot_login` + default-`load()`-HALT assertion block partially duplicates `test_detection_contract.py::test_local_override_arms_without_touching_shipped_source`. Only the trailing `run_skill` + `arm_recorder.calls == 1` assertion is net-new. | Optional: trim the redundant setup/assertions and keep only the net-new FSM-arm assertion, OR leave as-is (self-documenting integration test). Does NOT meet duplicate-test FAIL bar because it carries a distinct load-bearing assertion. No fix required for PASS. |

## Actions Taken
None (fix_authorization: false; report-only). No source or test files modified.

## Confidence Gate

- [x] Item 1 VERIFIED — Read all 7 files; behavioral assertions cited above.
- [x] Item 2 VERIFIED — source read-only proof (diagnosis.py:302) + runtime `find -newermt` empty result + seam grep.
- [x] Item 3 VERIFIED — grep-confirmed every imported symbol against source line numbers; 81 tests collect+pass.
- [x] Item 4 VERIFIED — cross-file grep + Read of the three candidate-overlap existing tests.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 7 | Glob: 0 | Bash: 8

No UNCHECKED items. No UNVERIFIABLE items. Tool-call count (24) exceeds the
4-item checklist floor; each call mapped to a specific verification (symbol
existence, seam scoping, real-tree mtime, duplicate scan, or test execution).

## Recommendations
- Green light. The Phase 4 test suite is structurally sound: real symbols,
  hermetic (tmp/cwd/monkeypatch/isolated-fs) with proven no real-tree writes,
  behavioral assertions throughout, and no duplicate tests.
- Optional (non-blocking): consider trimming the redundant assertion block in
  `test_post_lock_for_arming_returns_locked_contract` (Issue #1) in a future
  cleanup pass. Not required for this gate.

## QA Complete
