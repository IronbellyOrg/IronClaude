# Refactor Plan — Step 4 (Remediation Plan derived from R3 convergence)

## Overview

| Field | Value |
|---|---|
| Base frame | B-as-base (spec-frame); see `base-selection.md` §3-§4 |
| Convergence | 0.825 average (impl 0.85, spec 0.80) |
| Total planned changes | **18** (P-006..P-013 code/spec fixes + T-012..T-021 test additions) |
| Risk profile | Mostly LOW change risk; 2 MEDIUM risk (PRD subclass refactor and env-var helper) |
| ID continuation | RECONCILED_DESIGN.md ended at P-005 / T-011; continuing at P-006 / T-012 |

This plan is the merged remediation surface. It folds together:

- The 13 R3 concessions from the impl-advocate (code + tests + tracking artefacts).
- The 4 R3 concessions from the spec-advocate (parametric subclass test, §4 P-004 amendment, U-033/U-034 verification, enforcement mechanism for D-086).
- The 8 NEW vs F invariant findings the probe surfaced, of which 6 are deferred (LOW) and 2 are folded into MEDIUM-risk fixes.
- F-strict-review's MEDIUM-1 (PRD subclass) and MEDIUM-2 (env-var crash) — both confirmed by all three rounds.

---

## Planned Changes — HIGH priority

### P-006 — Surface `_stdin_error` from `PrdClaudeProcess.terminate()`

| Field | Value |
|---|---|
| Type | CODE-FIX |
| Target | `src/superclaude/cli/prd/process.py:277` |
| Description | Insert 4-line block immediately before `_close_handles()` byte-identical to base at `pipeline/process.py:288-291`: `if getattr(self, "_stdin_error", None) is not None: _log.warning("stdin_error pid=%s err=%r", self._process.pid, self._stdin_error)`. PRD's terminate override predates P-004 and silently swallows BrokenPipe under SIGTERM-only paths. |
| Provenance | INV-004 (HIGH UNADDRESSED → ADDRESSED-R3) · F MEDIUM-1 · R3-impl §INV-004 |
| Severity | HIGH (blocks convergence per protocol; ADDRESSED-R3 by this plan) |
| Owner | branch author |
| Risk | LOW (4-line copy of established base block) |
| Estimated lines | +4 |

### P-007 — Pin PRD `terminate` `_stdin_error` surfacing with regression test

| Field | Value |
|---|---|
| Type | NEW-TEST |
| Target | `tests/pipeline/test_prd_process_stdin.py` (new file) |
| Description | `test_prd_terminate_surfaces_stdin_error`: monkeypatch `os.write` to raise `BrokenPipeError`, call `proc.start(); proc.terminate()`, assert `caplog` contains a WARNING with `"stdin_error"`. Mutation-kill: removing P-006's block must fail this test. |
| Provenance | INV-025 (HIGH UNADDRESSED → ADDRESSED-R3) · R3-impl §INV-025 |
| Severity | HIGH (paired with P-006) |
| Owner | branch author |
| Risk | LOW (new test file, no existing-test impact) |
| Estimated lines | +30 (test file + fixtures) |

### P-008 — Parametric subclass-propagation test for `_stdin_error` surfacing

| Field | Value |
|---|---|
| Type | NEW-TEST |
| Target | `tests/pipeline/test_subclass_terminate_invariant.py` (new file) |
| Description | `@pytest.mark.parametrize("cls", ClaudeProcess.__subclasses__())` test asserting every subclass override of `terminate()` either calls `super().terminate()` or contains the `_stdin_error` log block. Walks the subclass tree at collection time so future subclasses are auto-covered. |
| Provenance | R3-spec §INV-025 (subclass-test scope) · §6 R3-spec dispute #4 |
| Severity | HIGH (closes the contract-level gap; without it, narrow PRD test is a point-fix) |
| Owner | spec-keeper (separate commit, same PR per R3-spec) |
| Risk | LOW-MEDIUM (parametric collection at import time; needs careful fixture for ctor args) |
| Estimated lines | +35 (parametric harness + ctor-args fixture) |

---

## Planned Changes — MEDIUM priority

### P-009 — `_resolve_prompt_max_bytes()` helper for env-var hostility

| Field | Value |
|---|---|
| Type | CODE-FIX |
| Target | `src/superclaude/cli/pipeline/process.py:27-29` |
| Description | Replace `PROMPT_MAX_BYTES: int = int(os.environ.get(...))` with a helper that catches `ValueError` and falls back to default with `_log.warning("ignoring non-numeric SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)`. Optionally clamp negative values to default. Closes import-time crash on `=16MB`/`=unlimited`/`=-1`. |
| Provenance | INV-009 (MEDIUM UNADDRESSED) · INV-011 (NEW vs F, negative cap) · F MEDIUM-2 · R3-impl §9 |
| Severity | MEDIUM |
| Owner | branch author |
| Risk | MEDIUM (changes module-import behaviour; must verify no consumer depends on the import-crash for fail-fast) |
| Estimated lines | +12 / -2 |

### P-010 — Spec amendment: subclass-propagation invariant in §4 P-004

| Field | Value |
|---|---|
| Type | SPEC-AMENDMENT |
| Target | `.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` §4 P-004 acceptance block |
| Description | Add invariant: *"Subclasses overriding `terminate()` MUST either call `super().terminate()` or replicate the `_stdin_error` log block verbatim. Pinned by `tests/pipeline/test_subclass_terminate_invariant.py`."* |
| Provenance | R3-spec §INV-004 spec-fault concession · §6 R3-spec dispute #5 |
| Severity | MEDIUM |
| Owner | spec-keeper (same PR, separate commit per R3-spec) |
| Risk | LOW (doc-only) |
| Estimated lines | +5 |

### P-011 — Initialize `self._stdin_error = None` in `__init__`

| Field | Value |
|---|---|
| Type | CODE-FIX |
| Target | `src/superclaude/cli/pipeline/process.py` `__init__` (around L56-90) |
| Description | Add `self._stdin_error: Optional[BaseException] = None` to `__init__`. Closes U-007 asymmetric defensive read (where `wait()` uses direct attr access, `terminate()` uses `getattr`). Allows both call sites to use plain attr access uniformly. |
| Provenance | U-007 (R1) · INV-002 (MEDIUM, future-refactor risk) · F LOW-1 · R3-impl §1, §10 |
| Severity | MEDIUM |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +1 |

### P-012 — Add `prompt_via=stdin` literal to spawn debug log

| Field | Value |
|---|---|
| Type | CODE-FIX |
| Target | `src/superclaude/cli/pipeline/process.py:181-186` |
| Description | Change format string from `"spawn pid=%d cmd=%s prompt_bytes=%d"` to `"spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d"`. Restores telemetry contract D-099 — operators grepping `prompt_via=stdin` find matches. |
| Provenance | X-004 · R3-impl §2 |
| Severity | MEDIUM |
| Owner | branch author |
| Risk | LOW (one-line format-string edit) |
| Estimated lines | +1 / -1 |

### P-013 — Replace conditional T-011 BrokenPipe assertion with mock-injected unconditional

| Field | Value |
|---|---|
| Type | CODE-FIX |
| Target | `tests/pipeline/test_process_stdin.py:465-488` |
| Description | Replace race-tolerant `if proc._stdin_error is not None` shape with `monkeypatch.setattr(os, "write", _raise_broken_pipe)` to inject BrokenPipe deterministically. Assert unconditionally that `caplog` contains WARNING with `"stdin_error"`. Restores mutation-kill: removing the P-004 capture block must fail T-011. |
| Provenance | X-006 · R3-impl §3 · NIT-1 (F-strict-review) |
| Severity | MEDIUM |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +8 / -5 |

### T-012 — `n == 0` silent break observability

| Field | Value |
|---|---|
| Type | CODE-FIX |
| Target | `src/superclaude/cli/pipeline/process.py:216-218` |
| Description | Before `break`, set `self._stdin_error = OSError(f"unexpected zero-byte write at offset {offset}/{len(view)}")`. Closes silent-truncation observability gap. |
| Provenance | INV-014 (MEDIUM, elevated from F LOW-2) · R3-impl §11 |
| Severity | MEDIUM |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +2 |

### T-013 — NUL-byte prompt round-trip test

| Field | Value |
|---|---|
| Type | NEW-TEST |
| Target | `tests/pipeline/test_process_stdin.py` (append) |
| Description | `test_nul_byte_prompt_round_trip`: send `b"\x00" * 1024` through stdin, assert byte-for-byte echo. Pins binary-safety invariant against future string-conversion regressions. |
| Provenance | INV-019 (NEW vs F, LOW elevated for mutation-kill) · R2-impl W-L9 · R3-impl §12 |
| Severity | MEDIUM |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +20 |

### T-014 — `finally`-close mutation-kill test

| Field | Value |
|---|---|
| Type | NEW-TEST |
| Target | `tests/pipeline/test_process_stdin.py` (append) |
| Description | Inject OSError mid-write via `monkeypatch`, assert `proc._process.stdin.closed` post-call. Pins the `finally: stdin.close()` invariant against future refactors that move close() out of finally. Pairs with P-013 (X-006) fix. |
| Provenance | F-strict-review §6 mutation-kill gap · R2-impl W-L10 · R3-impl §13 |
| Severity | MEDIUM |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +25 |

### P-014 — `BEAT_2_BACKLOG.md` tracking artefact

| Field | Value |
|---|---|
| Type | DEFERRED-WITH-OWNER (lands as in-tree tracking file) |
| Target | `.dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` (new file) |
| Description | List the 15 DEFER-TO-BEAT-2 items (D-016, D-022, D-035, D-064, D-065, D-072, D-073, D-077, D-085, D-087, D-093, D-095, D-096, D-097, D-098) with one-line rationale per item and proposed owner. Optionally append SUPERSEDED list as second appendix per R3-impl §5. |
| Provenance | U-024 (HIGH) · R3-impl §5 · R3-spec §"Sufficiency of Deferral Plan" |
| Severity | MEDIUM (tracking surface for high-volume deferred items) |
| Owner | branch author |
| Risk | LOW (doc-only) |
| Estimated lines | +60 (markdown) |

### P-015 — `TRACEABILITY.md` commit→D-NNN map

| Field | Value |
|---|---|
| Type | DEFERRED-WITH-OWNER (lands as in-tree tracking file) |
| Target | `.dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` (new file) |
| Description | Map each commit SHA → P-NNN → D-NNN list. Closes S-008 (loss of D-NNN linkage in commit messages) by providing an out-of-band traceability artefact. |
| Provenance | S-008 · U-035 · R3-impl §4 · R3-spec Concession #8 |
| Severity | MEDIUM (audit trail) |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +40 |

---

## Planned Changes — LOW priority

### P-016 — `make ship-coder` Makefile target

| Field | Value |
|---|---|
| Type | DEFERRED-WITH-OWNER |
| Target | `Makefile` (append target) |
| Description | Add `ship-coder:` target running `uv build && pipx install --force --pip-args="<wheel>" superclaude` and printing instructions to re-run the failing 338 KB roadmap. Closes the IronClaude-side half of §9.2; release-engineer runs it post-merge to close U-031. |
| Provenance | U-031 · R3-impl §6 (compromise) · R3-spec §"Sufficiency of Deferral Plan" |
| Severity | LOW (operational scaffolding; the actual on-Coder run is post-merge) |
| Owner | release-engineer (executes post-merge); branch author lands the target |
| Risk | LOW |
| Estimated lines | +10 |

### T-015 — Parametric `extra_args` size invariant

| Field | Value |
|---|---|
| Type | NEW-TEST |
| Target | `tests/pipeline/test_process_stdin.py` (append) |
| Description | Pass a 5 KB element via `extra_args`, assert T-001's `< 4 KiB` ceiling fires (i.e., the test correctly catches large `extra_args` too). Closes the live-caller path that T-001 currently misses. |
| Provenance | INV-015 (NEW vs F, LOW) |
| Severity | LOW |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +12 |

### T-016 — `tool_write_mode × BrokenPipe` cross-product test

| Field | Value |
|---|---|
| Type | NEW-TEST |
| Target | `tests/pipeline/test_process_stdin.py` (append) |
| Description | Combine T-007 (`tool_write_mode=True`) and T-011 (BrokenPipe via monkeypatch); assert sidecar fh is properly cleaned up under BrokenPipe. Closes test-coverage gap on the cross-product. |
| Provenance | INV-023 (NEW vs F, MEDIUM downgraded to LOW because mechanically straightforward) |
| Severity | LOW |
| Owner | branch author |
| Risk | LOW |
| Estimated lines | +20 |

---

## Changes NOT Being Made — DEFER-TO-BEAT-2 with explicit owners

Per R3-spec demand for accountability, every deferred item gets a tracking-issue suggestion:

| ID | Item | Reason for deferral | Tracking issue (suggested title) | Owner |
|---|---|---|---|---|
| D-FOLLOW-001 | D-086 — 338 KB Coder roadmap repro | Cross-host operational; cannot live in IronClaude diff | `[deferred] D-086: re-run failing 338 KB roadmap on /config/workspace/Coder` | release-engineer |
| D-FOLLOW-002 | D-067 — CI integration verification | Existing `.github/workflows/test.yml` picks up new tests via pytest discovery; explicit verification is post-merge | `[deferred] D-067: paste CI link confirming test_process_stdin.py runs in CI` | branch author (PR-comment artefact) |
| D-FOLLOW-003 | U-033/U-034 verdict cross-doc map | Requires linking from PR description to existing `E-reconciliation-matrix.md`; not a code fix | `[deferred] U-033/U-034: PR-description amendment with verdict mapping link` | branch author (PR-description, pre-merge) |
| D-FOLLOW-004 | INV-005 — file-handle leak on non-OSError mid-flight in `_write_prompt_to_stdin` | NEW vs F, MEDIUM but defensive against very rare `MemoryError`/`KeyboardInterrupt`. Refactor base `start()` to wrap file-open in try/except calling `_close_handles()` on any exception. Architectural change beyond scope of this delta. | `[deferred] INV-005: wrap _stdout_fh/_stderr_fh in start()-level try/except` | maintainer (post-merge) |
| D-FOLLOW-005 | INV-009 part 2 — negative `PROMPT_MAX_BYTES` rejection | Closed by P-009 if helper clamps; if helper does not clamp, file separate issue | `[deferred] INV-011: clamp negative SUPERCLAUDE_PROMPT_MAX_BYTES to default` | branch author |
| D-FOLLOW-006 | INV-024 — multi-occurrence `--output-format` in `extra_args` | Future code-reorder hazard; T-008 currently passes either way; LOW | `[deferred] INV-024: pin PortifyProcess anchor to first --output-format only` | maintainer (post-merge) |
| D-FOLLOW-007 | INV-026 — `build_command()` called twice per `start()` | F NIT-3; idempotent in practice; cache once | `[deferred] INV-026: cache build_command() result for debug-log reuse` | maintainer (post-merge) |
| D-FOLLOW-008 | INV-027 — T-005 timer-before-start race | F NIT-2; <0.1% flake odds; reorder in test | `[deferred] INV-027: reorder T-005 to start() before timer schedule` | branch author (could land in this PR if cheap) |
| D-FOLLOW-009 | INV-028 — chained `__cause__` exception capture is shallow | LOW; no real-world impact | `[deferred] INV-028: capture exception chain depth in _stdin_error` | maintainer (post-merge) |
| D-FOLLOW-010 | INV-030 — non-Linux pipe-buffer-size invalidates T-005 pipe-fill | LOW; CI is Linux-only per CLAUDE.md | `[deferred] INV-030: gate T-005 on Linux platform marker` | maintainer (post-merge) |
| D-FOLLOW-011 | 15 DEFER-TO-BEAT-2 D-NNN items | Captured in `BEAT_2_BACKLOG.md` (P-014 above) | (one issue per item, filed when Beat-2 sprint planned) | beat-2 owner |
| D-FOLLOW-012 | 12 SUPERSEDED items | Optionally appended to BEAT_2_BACKLOG.md per R3-impl §5 | `[record] superseded D-NNN ledger from RECONCILED_DESIGN.md §3.2` | branch author (optional) |
| W-M10 (R-5 telemetry) | Peak-heap telemetry hook | `prompt_bytes=N` covers input not peak; full instrumentation is Beat-2 | `[deferred] R-5: add prompt_encode_peak_bytes telemetry` | beat-2 owner |

---

## Risk Summary

| Change | Risk class | Rollback strategy |
|---|---|---|
| P-006 (4-line PRD fix) | LOW | Revert single commit; base `wait()` still surfaces under wait-after-terminate path |
| P-007 (PRD test) | LOW | New file; revert is removal |
| P-008 (parametric subclass test) | LOW-MEDIUM | If parametric collection breaks (e.g., subclass requires unusual ctor args), narrow to explicit subclass list |
| P-009 (env-var helper) | MEDIUM | Revert to `int(os.environ.get(...))` if a downstream consumer depends on import-time fail-fast |
| P-010 (spec amendment) | LOW | Doc revert |
| P-011 (init `_stdin_error`) | LOW | Revert one line |
| P-012 (log token) | LOW | Revert format string |
| P-013 (T-011 unconditional) | LOW | Old conditional version still works as smoke test |
| T-012 (`n=0` capture) | LOW | Revert two lines |
| T-013 (NUL-byte test) | LOW | New test; revert is removal |
| T-014 (finally-close mutation test) | LOW | New test; revert is removal |
| P-014/P-015 (tracking files) | LOW | Doc-only; trivial revert |
| P-016 (Makefile target) | LOW | Revert one target |
| T-015 / T-016 | LOW | New tests |

**Aggregate change risk: LOW.** Of 18 planned changes, 15 are LOW-risk doc/test/format edits. The 3 with non-trivial risk (P-008 parametric collection, P-009 env-var helper, possibly P-006 if PRD is invoked from unusual call paths) all have established rollback paths.

---

## Aggregate LOC change

| Bucket | Estimated |
|---|---|
| Source code | +20 / -8 (P-006, P-009, P-011, P-012, T-012) |
| Tests | +152 (P-007, P-008, P-013, T-013..T-016) |
| Spec / tracking docs | +110 (P-010, P-014, P-015) |
| Build | +10 (P-016) |
| **Total** | **+292 / -8 LOC** |

This is comfortably within the spec's intent of "small, scoped delta" — original delta was +60/-7 in `pipeline/process.py`; remediation adds another ~12 source LOC and 152 test LOC, with the rest in tracking artefacts.

---

**End of refactor-plan.md**
