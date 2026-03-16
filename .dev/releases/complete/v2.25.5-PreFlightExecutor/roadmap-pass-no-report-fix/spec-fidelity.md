---
high_severity_count: 3
medium_severity_count: 6
low_severity_count: 2
total_deviations: 11
validation_complete: true
tasklist_ready: false
---

## Deviation Report

---

**ID**: DEV-001
**Severity**: HIGH
**Deviation**: Roadmap omits T-005 (OSError unit test) from Phase 1 exit criteria and test list
**Spec Quote**: "T-005: `OSError` on write → returns `False`, no exception raised, WARNING logged" (§6, test list); "NFR-003: All existing tests must pass without modification"
**Roadmap Quote**: "Unit Tests (T-001, T-002, T-002b, T-005) — Add to `tests/sprint/test_executor.py`: T-001 ... T-002 ... T-002b ... T-005: `OSError` on write → returns `False`, no exception raised, WARNING logged"
**Impact**: T-005 appears in the Phase 1 test list in the roadmap but has no test body provided — unlike T-001 through T-002b which are fully specified in the spec. The roadmap lists T-005 but omits its implementation guidance and does not include it in the acceptance criteria matrix (SC column). This creates an ambiguity: implementers may skip it or produce an incorrect test. The spec explicitly requires this test as part of NFR-003 and the acceptance criteria.
**Recommended Correction**: Add T-005 to the roadmap Phase 1 implementation steps with its full test body as specified in §6 of the spec. Include it in the success criteria table with its own SC entry.

---

**ID**: DEV-002
**Severity**: HIGH
**Deviation**: Roadmap omits NFR-007 (Option A compliance telemetry / return value logging) from implementation requirements
**Spec Quote**: "NFR-007: The sprint log SHOULD record which path produced the result file for each phase: `agent-written` (Option A) or `executor-preliminary` (Option D). Implementation: `_write_preliminary_result()` SHOULD return a boolean indicating whether it wrote the file. The call site in `execute_sprint()` logs the outcome at DEBUG level." (§4, NFR-007)
**Roadmap Quote**: "Log at DEBUG level using combined terminology: primary labels `executor-preliminary` / `agent-written` (operator-readable), with `option_d` / `option_a_or_noop` as parenthetical context in the DEBUG message body" (Phase 2)
**Impact**: NFR-007 requires `_write_preliminary_result()` to return a boolean AND that the call site logs this. The roadmap addresses the logging in Phase 2 but does not include the boolean return contract as part of the Phase 1 function definition. The function signature in Change 1 of the spec returns `bool`, but the roadmap Phase 1 signature specification omits the return type annotation and return value requirement. An implementer following only Phase 1 would produce a `-> None` function, breaking Phase 2's telemetry logging. There is a cross-phase dependency gap.
**Recommended Correction**: In Phase 1 implementation steps, explicitly specify `-> bool` return type and document the `True`/`False` return semantics. The Phase 2 logging step already correctly references `_wrote_preliminary`, but the Phase 1 contract must be consistent.

---

**ID**: DEV-003
**Severity**: HIGH
**Deviation**: Roadmap's Success Criteria table maps SC-006 to "Zero-byte file overwritten" but the spec's §9 Acceptance Criteria lists SC-006 implicitly under T-002b — the roadmap numbering diverges from the spec's acceptance criteria list, and SC-009b is not mapped to any test
**Spec Quote**: "SC-009b" is not listed in the spec's §9 acceptance criteria. The spec lists: `_write_preliminary_result()` importable, T-003 passes, T-002b passes, T-006 passes, sprint re-run reports `pass`, sprint re-run in same output directory with stale files produces `pass`, `PASS_NO_REPORT` remains in enum, direct-call tests pass, full suite 0 regressions, pre-implementation baseline green. (§9)
**Roadmap Quote**: "SC-009b: Python/skip preflight phases still yield `PREFLIGHT_PASS`" (Phase 4 architect checks); "SC-006: Zero-byte file overwritten — P1 (T-002b)" (success criteria table)
**Impact**: The roadmap introduces `SC-009b` (a new success criterion not present in the spec's §9) and renumbers several criteria. SC-006 in the roadmap maps to "Zero-byte file overwritten" while SC-006 in the spec maps to TIMEOUT/ERROR/INCOMPLETE/PASS_RECOVERED unchanged. This numbering mismatch means validators using the roadmap's SC table cannot cross-reference spec §9 correctly, risking acceptance criteria gaps. The preflight isolation requirement from Implication 9 is correctly identified but adding it as `SC-009b` without a corresponding spec acceptance criterion could cause it to be treated as optional.
**Recommended Correction**: Align success criteria IDs with spec §9 exactly. Document SC-009b as an architecturally-derived validation step (from §5, Implication 9) rather than a new numbered spec requirement. Correct the SC-006 numbering discrepancy.

---

**ID**: DEV-004
**Severity**: MEDIUM
**Deviation**: Roadmap omits FR-008 (ordering invariant as a formal requirement) — referenced in Phase 2 as "FR-008" but the spec does not define FR-008; the ordering invariant appears only within FR-001 and FR-002
**Spec Quote**: "Ordering invariant (see FR-002): This function MUST always be called BEFORE `_determine_phase_status()` and BEFORE `_write_executor_result_file()`." (§3, FR-001); "These three operations form an ordered triple; their relative order MUST NOT be changed by refactoring." (§3, FR-001)
**Roadmap Quote**: "Verify ordering invariant (FR-008) — Confirm the three calls appear in this exact order" (Phase 2)
**Impact**: The roadmap references `FR-008` which does not exist in the spec. The ordering invariant is defined within FR-001 and FR-002. An implementer checking "FR-008" against the spec will find nothing, potentially treating it as a non-normative note. This creates a traceability gap.
**Recommended Correction**: Replace `FR-008` with `(FR-001 ordering invariant)` in the Phase 2 verification step.

---

**ID**: DEV-005
**Severity**: MEDIUM
**Deviation**: Roadmap omits NFR-006 (sentinel contract comment in `_determine_phase_status()`) from Phase 1 exit criteria
**Spec Quote**: "NFR-006: The string `EXIT_RECOMMENDATION: CONTINUE` is a sentinel value in the `_determine_phase_status()` parsing protocol. Any future modification to that parsing logic MUST remain compatible with this exact string. This sentinel contract MUST be documented as a comment in `_determine_phase_status()` at the point where it checks for `CONTINUE`." (§4, NFR-006)
**Roadmap Quote**: "Add sentinel contract comment in `_determine_phase_status()` (NFR-006) — At the `CONTINUE` sentinel parsing point, add a comment documenting the contract. Place here in Phase 1 while implementation context is fully loaded — do not defer." (Phase 1)
**Impact**: NFR-006 is mentioned in Phase 1 implementation steps, but absent from the Phase 1 exit criteria and the success criteria table. It has no SC entry in the roadmap's validation matrix. Without an explicit SC entry, the sentinel comment may be skipped or deferred during validation. This is a gap in the acceptance criteria coverage.
**Recommended Correction**: Add NFR-006 to the success criteria table and Phase 1 exit criteria as a checkable item.

---

**ID**: DEV-006
**Severity**: MEDIUM
**Deviation**: Roadmap's T-005 description ("OSError on write → returns False, no exception raised, WARNING logged") omits the spec's logger module requirement
**Spec Quote**: "Failure is non-fatal: wrap in `try/except OSError` — on `OSError`, emit a WARNING via the module logger before continuing: `logger.warning(\"preliminary result write failed: %s; phase may report PASS_NO_REPORT\", e)`" (§3, FR-001); Change 1 uses `_logging.getLogger(__name__).warning(...)` inline import
**Roadmap Quote**: "T-005: `OSError` on write → returns `False`, no exception raised, WARNING logged" (Phase 1 unit tests)
**Impact**: The roadmap does not specify the logger is the module logger (`logging.getLogger(__name__)`), nor does it mention the exact warning message format. The spec's Change 1 uses an inline `import logging as _logging` pattern, which is unusual. A test verifying "WARNING logged" without asserting it targets the module logger or specific message could pass with incorrect behavior.
**Recommended Correction**: T-005 description should specify that the test asserts the WARNING is logged via the module logger with the exact message format from FR-001.

---

**ID**: DEV-007
**Severity**: MEDIUM
**Deviation**: Roadmap Phase 3 prompt injection does not include the `as_posix()` format verification or the `prompt.rindex("## Result File") > prompt.rindex("## Important")` assertion as part of T-005
**Spec Quote**: "Verify attribute name: The attribute `self.phase` in `build_prompt()` must match the actual attribute name set in `ClaudeProcess.__init__`. Confirm against the constructor before implementing — do not assume `self.phase` if the constructor uses a different name." (§3, FR-006); "Constraint: The injected path MUST use `config.result_file(self.phase).as_posix()` — the exact path the executor reads, formatted as a POSIX string" (§3, FR-006)
**Roadmap Quote**: "Verify `prompt.rindex(\"## Result File\") > prompt.rindex(\"## Important\")` (SC-013) — Verify path is absolute and uses POSIX separators" (Phase 3); "Verify no existing sections repositioned" (Phase 3)
**Impact**: The roadmap's Phase 3 says "verify path is absolute and uses POSIX separators" but the spec requires specifically `as_posix()` formatting. "Absolute" is a weaker assertion — a relative POSIX path could satisfy the roadmap's check but violate the spec. Additionally, the roadmap does not explicitly gate Phase 3 on OQ-001 resolution (the `self.phase` attribute name check), though it mentions it was done in M0. The cross-reference is implicit rather than explicit.
**Recommended Correction**: Phase 3 should explicitly assert `config.result_file(self.phase).as_posix()` (using `as_posix()` specifically, not just "POSIX separators"). Include an explicit forward reference confirming OQ-001 was resolved before this phase begins.

---

**ID**: DEV-008
**Severity**: MEDIUM
**Deviation**: Roadmap omits NFR-002's TOCTOU documentation requirement from Phase 1 exit criteria
**Spec Quote**: "NFR-002: ... If the executor is ever parallelized to run phases concurrently, replace the `exists()`/`stat()` check with `os.open(..., os.O_WRONLY | os.O_CREAT | os.O_EXCL)` for atomic exclusive creation. Document this constraint in `_write_preliminary_result()`'s docstring." (§4, NFR-002)
**Roadmap Quote**: "Document single-threaded concurrency assumption; `O_EXCL` follow-up note; no premature redesign" (RISK-008, Phase 1 docstring)
**Impact**: The concurrency documentation is listed as a risk mitigation item in the risk table but is not in the Phase 1 exit criteria. NFR-002 explicitly requires this in the docstring. If a reviewer checks Phase 1 exit criteria to verify the docstring, they will not find this requirement listed and may mark Phase 1 complete without verifying the TOCTOU note.
**Recommended Correction**: Add "TOCTOU/concurrency limitation documented in docstring per NFR-002" to Phase 1 exit criteria.

---

**ID**: DEV-009
**Severity**: MEDIUM
**Deviation**: Roadmap omits NFR-001's negative exit code requirement (`exit_code < 0`) from Phase 2 verification steps
**Spec Quote**: "NFR-001: Negative exit codes: On Linux, a subprocess killed by a signal returns a negative `returncode` (e.g., `-9` for SIGKILL, `-15` for SIGTERM). These are non-zero and are excluded by the `exit_code == 0` guard. Verify that `_determine_phase_status()` handles `exit_code < 0` without exception — it must fall through to `ERROR` or `INCOMPLETE`, not raise." (§4, NFR-001)
**Roadmap Quote**: "Verify non-zero exit paths untouched (FR-005, NFR-001) — Trace TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED paths — none should reach `_write_preliminary_result()`" (Phase 2)
**Impact**: The roadmap's NFR-001 verification step covers "TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED" but does not explicitly address negative exit codes (`exit_code < 0`) as a distinct verification target. OQ-005 in Phase 0 asks to "Verify `_determine_phase_status()` handles `exit_code < 0` correctly; if it raises, flag as blocking prerequisite" — but this is framed as an open question, not a mandatory post-implementation verification. If OQ-005 discovers a problem but the Phase 2 checklist doesn't explicitly require re-verification, it could be missed.
**Recommended Correction**: Phase 2 verification steps should explicitly include: "Verify `exit_code < 0` falls through to ERROR/INCOMPLETE without raising, per NFR-001."

---

**ID**: DEV-010
**Severity**: LOW
**Deviation**: Roadmap Success Criteria table uses different column header ("Verified In") vs spec's acceptance criteria format (checkbox list)
**Spec Quote**: "- [ ] `_write_preliminary_result()` exists and is importable from `executor.py` [...] - [ ] Pre-implementation baseline: `uv run pytest tests/sprint/ -v` passes before any code changes" (§9, Acceptance Criteria — 14 checklist items)
**Roadmap Quote**: "| SC-001 | `_write_preliminary_result()` importable with correct signature | P1 |" (Success Criteria table)
**Impact**: The roadmap table has 13 SC entries; the spec has 14 checklist items. The missing item is the explicit "Pre-implementation baseline passes before any code changes" — while covered by SC-012 ("Pre-implementation baseline green — P0"), the roadmap table omits the "before any code changes" temporal qualifier that the spec explicitly calls out. This is a minor traceability gap.
**Recommended Correction**: Add "before any code changes" qualifier to SC-012 description in the success criteria table.

---

**ID**: DEV-011
**Severity**: LOW
**Deviation**: Roadmap uses "phase-days" as timeline unit; spec uses no timeline estimates
**Spec Quote**: (No timeline estimates appear in the spec; the spec is a patch specification, not a roadmap.)
**Roadmap Quote**: "Timeline: 0.25 phase-days" (Phase 0); "Total: 2.0 phase-days" (Timeline Estimates table)
**Impact**: The roadmap's timeline estimates are a valid addition for planning purposes. The spec does not prescribe timelines, so this represents an additive element rather than a contradiction. No implementation risk.
**Recommended Correction**: No action required. This is an acceptable roadmap addition not present in the spec.

---

## Summary

**Total deviations**: 11 (3 HIGH, 6 MEDIUM, 2 LOW)

**Tasklist ready**: NO — 3 HIGH severity deviations block readiness.

### High Severity (3)

- **DEV-001**: T-005 test body absent from Phase 1 despite being listed — no test body or SC entry means OSError handling may be implemented incorrectly.
- **DEV-002**: `_write_preliminary_result()` return type (`-> bool`) missing from Phase 1 definition — Phase 2's telemetry logging depends on this return value but Phase 1 doesn't specify it.
- **DEV-003**: Success criteria numbering diverges from spec §9; SC-009b introduced without spec backing; SC-006 maps to different content than spec — cross-validation against spec acceptance criteria is unreliable.

### Medium Severity (6)

- **DEV-004**: Non-existent `FR-008` referenced (ordering invariant lives in FR-001/FR-002).
- **DEV-005**: NFR-006 sentinel comment requirement absent from exit criteria and SC table.
- **DEV-006**: T-005 logging assertion insufficient — module logger and exact message format not specified.
- **DEV-007**: `as_posix()` requirement weakened to "POSIX separators"; OQ-001 cross-reference implicit.
- **DEV-008**: NFR-002 TOCTOU docstring requirement absent from Phase 1 exit criteria.
- **DEV-009**: NFR-001 negative exit code verification not explicitly required in Phase 2.

### Low Severity (2)

- **DEV-010**: "Before any code changes" qualifier missing from SC-012.
- **DEV-011**: Timeline unit ("phase-days") is a roadmap addition not in spec — acceptable.
