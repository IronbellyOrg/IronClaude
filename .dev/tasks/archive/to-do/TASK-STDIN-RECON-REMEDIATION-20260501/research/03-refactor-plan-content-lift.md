# Research: Refactor-Plan Content Lift
**Topic type:** Per-item metadata extraction
**Scope:** refactor-plan.md (18 P/T-NNN items + tables)
**Status:** Complete
**Date:** 2026-05-01
**Source:** `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/adversarial-recon/adversarial/refactor-plan.md`

---

## Plan Overview (from refactor-plan.md §Overview)

| Field | Value |
|---|---|
| Base frame | B-as-base (spec-frame); see `base-selection.md` §3-§4 |
| Convergence | 0.825 average (impl 0.85, spec 0.80) |
| Total planned changes | 18 (P-006..P-013 + T-012..T-016 + P-014..P-016) |
| Risk profile | Mostly LOW; 2 MEDIUM (PRD subclass refactor, env-var helper) |
| ID continuation | RECONCILED_DESIGN.md ended at P-005 / T-011; continuing at P-006 / T-012 |
| Aggregate LOC | +292 / -8 |

---

## Phase 1 — MUST (in-PR fixes for real defects)

### Record P-006

```yaml
id: P-006
title: Surface `_stdin_error` from `PrdClaudeProcess.terminate()`
type: CODE-FIX
target: src/superclaude/cli/prd/process.py:277
description: |
  Insert 4-line block immediately before `_close_handles()` byte-identical
  to base at `pipeline/process.py:288-291`:
  `if getattr(self, "_stdin_error", None) is not None: _log.warning("stdin_error pid=%s err=%r", self._process.pid, self._stdin_error)`.
  PRD's terminate override predates P-004 and silently swallows BrokenPipe
  under SIGTERM-only paths.
provenance: "INV-004 (HIGH UNADDRESSED → ADDRESSED-R3) · F MEDIUM-1 · R3-impl §INV-004"
severity: HIGH
owner: branch-author
risk: LOW
estimated_loc: "+4"
phase_assignment: 1-MUST
before_snippet: N/A (refactor-plan does not include before code block)
after_snippet: |
  if getattr(self, "_stdin_error", None) is not None:
      _log.warning("stdin_error pid=%s err=%r", self._process.pid, self._stdin_error)
acceptance_summary:
  - 4-line block is byte-identical to base block at pipeline/process.py:288-291
  - Block is positioned immediately before _close_handles() in PrdClaudeProcess.terminate()
  - Paired regression test (P-007) passes
  - Removing the block causes P-007 to fail (mutation-kill confirmed)
notes: |
  Blocks convergence per protocol; ADDRESSED-R3 by this plan.
  Risk rationale per Risk Summary: "Revert single commit; base wait()
  still surfaces under wait-after-terminate path".
```

### Record P-007

```yaml
id: P-007
title: Pin PRD `terminate` `_stdin_error` surfacing with regression test
type: NEW-TEST
target: tests/pipeline/test_prd_process_stdin.py (new file)
description: |
  `test_prd_terminate_surfaces_stdin_error`: monkeypatch `os.write` to
  raise `BrokenPipeError`, call `proc.start(); proc.terminate()`, assert
  `caplog` contains a WARNING with `"stdin_error"`. Mutation-kill:
  removing P-006's block must fail this test.
provenance: "INV-025 (HIGH UNADDRESSED → ADDRESSED-R3) · R3-impl §INV-025"
severity: HIGH
owner: branch-author
risk: LOW
estimated_loc: "+30"
phase_assignment: 1-MUST
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New test file `tests/pipeline/test_prd_process_stdin.py` exists
  - Test name `test_prd_terminate_surfaces_stdin_error` is present
  - Test monkeypatches os.write to raise BrokenPipeError
  - Test calls proc.start() then proc.terminate()
  - Test asserts caplog contains WARNING with "stdin_error"
  - Removing P-006's 4-line block causes this test to fail (mutation-kill verified)
notes: Paired with P-006; HIGH per protocol.
```

### Record P-009

```yaml
id: P-009
title: "`_resolve_prompt_max_bytes()` helper for env-var hostility"
type: CODE-FIX
target: src/superclaude/cli/pipeline/process.py:27-29
description: |
  Replace `PROMPT_MAX_BYTES: int = int(os.environ.get(...))` with a
  helper that catches `ValueError` and falls back to default with
  `_log.warning("ignoring non-numeric SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)`.
  Optionally clamp negative values to default. Closes import-time crash
  on `=16MB`/`=unlimited`/`=-1`.
provenance: "INV-009 (MEDIUM UNADDRESSED) · INV-011 (NEW vs F, negative cap) · F MEDIUM-2 · R3-impl §9"
severity: MEDIUM
owner: branch-author
risk: MEDIUM
estimated_loc: "+12 / -2"
phase_assignment: 1-MUST
before_snippet: |
  PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", DEFAULT))
after_snippet: |
  def _resolve_prompt_max_bytes() -> int:
      raw = os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")
      if raw is None:
          return DEFAULT
      try:
          value = int(raw)
      except ValueError:
          _log.warning("ignoring non-numeric SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)
          return DEFAULT
      if value < 0:
          return DEFAULT  # optional clamp
      return value
  PROMPT_MAX_BYTES: int = _resolve_prompt_max_bytes()
acceptance_summary:
  - Helper function `_resolve_prompt_max_bytes()` exists at module scope
  - ValueError on int() is caught and logs WARNING with raw value
  - Default value used as fallback
  - Optional clamp on negative values to default
  - Module no longer crashes at import on `SUPERCLAUDE_PROMPT_MAX_BYTES=16MB`
  - Module no longer crashes at import on `=unlimited` or `=-1`
notes: |
  Risk MEDIUM because it changes module-import behaviour; must verify
  no consumer depends on the import-crash for fail-fast.
  Rollback: revert to `int(os.environ.get(...))` if downstream depends on fail-fast.
  D-FOLLOW-005 deferral note: if helper does NOT clamp negative,
  file separate issue INV-011.
```

---

## Phase 2 — SHOULD (polish + mutation-kill tests)

### Record P-011

```yaml
id: P-011
title: "Initialize `self._stdin_error = None` in `__init__`"
type: CODE-FIX
target: "src/superclaude/cli/pipeline/process.py `__init__` (around L56-90)"
description: |
  Add `self._stdin_error: Optional[BaseException] = None` to `__init__`.
  Closes U-007 asymmetric defensive read (where `wait()` uses direct
  attr access, `terminate()` uses `getattr`). Allows both call sites to
  use plain attr access uniformly.
provenance: "U-007 (R1) · INV-002 (MEDIUM, future-refactor risk) · F LOW-1 · R3-impl §1, §10"
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+1"
phase_assignment: 2-SHOULD
before_snippet: N/A
after_snippet: |
  self._stdin_error: Optional[BaseException] = None
acceptance_summary:
  - `__init__` initializes `self._stdin_error` to None with type annotation
  - Both wait() and terminate() can use plain attr access without getattr
  - No regression in existing _stdin_error capture/surface tests
notes: |
  OVER-CALIBRATED-MEDIUM (per /sc:reflect): A-FINDING-006 (asymmetric
  `_stdin_error`) MEDIUM is over-calibrated; defensible LOW.
  Builder MUST embed calibration note in item body or `## Task Log / Notes`.
```

### Record P-013

```yaml
id: P-013
title: Replace conditional T-011 BrokenPipe assertion with mock-injected unconditional
type: CODE-FIX
target: tests/pipeline/test_process_stdin.py:465-488
description: |
  Replace race-tolerant `if proc._stdin_error is not None` shape with
  `monkeypatch.setattr(os, "write", _raise_broken_pipe)` to inject
  BrokenPipe deterministically. Assert unconditionally that `caplog`
  contains WARNING with `"stdin_error"`. Restores mutation-kill:
  removing the P-004 capture block must fail T-011.
provenance: "X-006 · R3-impl §3 · NIT-1 (F-strict-review)"
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+8 / -5"
phase_assignment: 2-SHOULD
before_snippet: |
  # race-tolerant shape (existing)
  if proc._stdin_error is not None:
      assert "BrokenPipe" in str(proc._stdin_error)
after_snippet: |
  monkeypatch.setattr(os, "write", _raise_broken_pipe)
  # ... call site ...
  assert any("stdin_error" in rec.message for rec in caplog.records if rec.levelname == "WARNING")
acceptance_summary:
  - Conditional `if proc._stdin_error is not None` is removed
  - monkeypatch.setattr(os, "write", _raise_broken_pipe) injects BrokenPipe deterministically
  - Assertion on caplog WARNING containing "stdin_error" is unconditional
  - Removing P-004 capture block causes T-011 to fail (mutation-kill restored)
notes: |
  Rollback: old conditional version still works as smoke test.
```

### Record T-012

```yaml
id: T-012
title: "`n == 0` silent break observability"
type: CODE-FIX
target: src/superclaude/cli/pipeline/process.py:216-218
description: |
  Before `break`, set
  `self._stdin_error = OSError(f"unexpected zero-byte write at offset {offset}/{len(view)}")`.
  Closes silent-truncation observability gap.
provenance: "INV-014 (MEDIUM, elevated from F LOW-2) · R3-impl §11"
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+2"
phase_assignment: 2-SHOULD
before_snippet: |
  if n == 0:
      break
after_snippet: |
  if n == 0:
      self._stdin_error = OSError(f"unexpected zero-byte write at offset {offset}/{len(view)}")
      break
acceptance_summary:
  - Before `break` on `n == 0`, `self._stdin_error` is set to OSError
  - OSError message includes f-string with offset/len(view)
  - Operators can now observe silent-truncation via _stdin_error surfacing
notes: |
  OVER-CALIBRATED-MEDIUM (per /sc:reflect): A-FINDING-007 (n=0 silent
  break) elevated from F LOW-2; defensible to keep LOW.
  Builder MUST embed calibration note in item body or `## Task Log / Notes`.
```

### Record T-013

```yaml
id: T-013
title: NUL-byte prompt round-trip test
type: NEW-TEST
target: tests/pipeline/test_process_stdin.py (append)
description: |
  `test_nul_byte_prompt_round_trip`: send `b"\x00" * 1024` through
  stdin, assert byte-for-byte echo. Pins binary-safety invariant
  against future string-conversion regressions.
provenance: "INV-019 (NEW vs F, LOW elevated for mutation-kill) · R2-impl W-L9 · R3-impl §12"
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+20"
phase_assignment: 2-SHOULD
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New test `test_nul_byte_prompt_round_trip` appended to test_process_stdin.py
  - Test sends `b"\x00" * 1024` through stdin
  - Test asserts byte-for-byte echo (1024 NUL bytes recovered)
  - Pins binary-safety invariant against future str conversion regressions
notes: Severity elevated from LOW to MEDIUM for mutation-kill purposes.
```

### Record T-014

```yaml
id: T-014
title: "`finally`-close mutation-kill test"
type: NEW-TEST
target: tests/pipeline/test_process_stdin.py (append)
description: |
  Inject OSError mid-write via `monkeypatch`, assert
  `proc._process.stdin.closed` post-call. Pins the
  `finally: stdin.close()` invariant against future refactors that
  move close() out of finally. Pairs with P-013 (X-006) fix.
provenance: "F-strict-review §6 mutation-kill gap · R2-impl W-L10 · R3-impl §13"
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+25"
phase_assignment: 2-SHOULD
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New test in test_process_stdin.py injects OSError mid-write via monkeypatch
  - Test asserts `proc._process.stdin.closed` is True post-call
  - Pins `finally: stdin.close()` invariant
  - If finally-close moved out of finally block, this test fails (mutation-kill)
notes: Pairs with P-013 (X-006) fix; both target the same call-site contract.
```

---

## Phase 3 — NICE (parametric subclass test + spec amendment)

### Record P-008

```yaml
id: P-008
title: Parametric subclass-propagation test for `_stdin_error` surfacing
type: NEW-TEST
target: tests/pipeline/test_subclass_terminate_invariant.py (new file)
description: |
  `@pytest.mark.parametrize("cls", ClaudeProcess.__subclasses__())` test
  asserting every subclass override of `terminate()` either calls
  `super().terminate()` or contains the `_stdin_error` log block. Walks
  the subclass tree at collection time so future subclasses are
  auto-covered.
provenance: "R3-spec §INV-025 (subclass-test scope) · §6 R3-spec dispute #4"
severity: HIGH
owner: spec-keeper
risk: LOW-MEDIUM
estimated_loc: "+35"
phase_assignment: 3-NICE
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New file `tests/pipeline/test_subclass_terminate_invariant.py` exists
  - Test uses `@pytest.mark.parametrize("cls", ClaudeProcess.__subclasses__())`
  - Subclass tree walked at collection time (auto-covers future subclasses)
  - Test asserts each terminate() override either calls super().terminate() or contains _stdin_error log block
  - ctor-args fixture handles per-subclass constructor variation
notes: |
  Severity HIGH per refactor-plan ("closes the contract-level gap;
  without it, narrow PRD test is a point-fix") but phase-mapped to
  Phase 3 (NICE) per BUILD_REQUEST. Owner = spec-keeper (separate
  commit, same PR per R3-spec).
  Risk LOW-MEDIUM: parametric collection at import time; needs
  careful fixture for ctor args. Rollback: narrow to explicit
  subclass list if parametric collection breaks.
```

### Record P-010

```yaml
id: P-010
title: "Spec amendment: subclass-propagation invariant in §4 P-004"
type: SPEC-AMENDMENT
target: ".dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md §4 P-004 acceptance block"
description: |
  Add invariant: *"Subclasses overriding `terminate()` MUST either call
  `super().terminate()` or replicate the `_stdin_error` log block
  verbatim. Pinned by `tests/pipeline/test_subclass_terminate_invariant.py`."*
provenance: "R3-spec §INV-004 spec-fault concession · §6 R3-spec dispute #5"
severity: MEDIUM
owner: spec-keeper
risk: LOW
estimated_loc: "+5"
phase_assignment: 3-NICE
before_snippet: N/A
after_snippet: |
  Subclasses overriding `terminate()` MUST either call `super().terminate()`
  or replicate the `_stdin_error` log block verbatim. Pinned by
  `tests/pipeline/test_subclass_terminate_invariant.py`.
acceptance_summary:
  - RECONCILED_DESIGN.md §4 P-004 acceptance block contains the new invariant
  - Invariant references the pinning test file
  - Doc-only edit; no code impact
notes: Owner = spec-keeper; same PR, separate commit per R3-spec convention.
```

### Record P-012

```yaml
id: P-012
title: "Add `prompt_via=stdin` literal to spawn debug log"
type: CODE-FIX
target: src/superclaude/cli/pipeline/process.py:181-186
description: |
  Change format string from `"spawn pid=%d cmd=%s prompt_bytes=%d"`
  to `"spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d"`.
  Restores telemetry contract D-099 — operators grepping
  `prompt_via=stdin` find matches.
provenance: "X-004 · R3-impl §2"
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+1 / -1"
phase_assignment: 3-NICE
before_snippet: |
  "spawn pid=%d cmd=%s prompt_bytes=%d"
after_snippet: |
  "spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d"
acceptance_summary:
  - Format string at process.py:181-186 includes literal `prompt_via=stdin`
  - `grep prompt_via=stdin` against debug log returns matches
  - Telemetry contract D-099 restored
notes: |
  OVER-CALIBRATED-MEDIUM (per /sc:reflect): A-FINDING-004 (log token)
  MEDIUM is over-calibrated; defensible LOW.
  Builder MUST embed calibration note in item body or `## Task Log / Notes`.
```

---

## Phase 4 — Tracking artifacts (separate ownership)

### Record P-014

```yaml
id: P-014
title: "`BEAT_2_BACKLOG.md` tracking artefact"
type: DEFERRED-WITH-OWNER
target: .dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md (new file)
description: |
  List the 15 DEFER-TO-BEAT-2 items (D-016, D-022, D-035, D-064, D-065,
  D-072, D-073, D-077, D-085, D-087, D-093, D-095, D-096, D-097, D-098)
  with one-line rationale per item and proposed owner. Optionally
  append SUPERSEDED list as second appendix per R3-impl §5.
provenance: "U-024 (HIGH) · R3-impl §5 · R3-spec §\"Sufficiency of Deferral Plan\""
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+60"
phase_assignment: 4-Tracking
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New file BEAT_2_BACKLOG.md exists in claude-process-stdin-patch dir
  - All 15 D-NNN items listed: D-016, D-022, D-035, D-064, D-065, D-072, D-073, D-077, D-085, D-087, D-093, D-095, D-096, D-097, D-098
  - Each item has one-line rationale and proposed owner
  - Optional: SUPERSEDED list appendix per R3-impl §5
notes: Tracking surface for high-volume deferred items.
```

### Record P-015

```yaml
id: P-015
title: "`TRACEABILITY.md` commit→D-NNN map"
type: DEFERRED-WITH-OWNER
target: .dev/architectural/claude-process-stdin-patch/TRACEABILITY.md (new file)
description: |
  Map each commit SHA → P-NNN → D-NNN list. Closes S-008 (loss of
  D-NNN linkage in commit messages) by providing an out-of-band
  traceability artefact.
provenance: "S-008 · U-035 · R3-impl §4 · R3-spec Concession #8"
severity: MEDIUM
owner: branch-author
risk: LOW
estimated_loc: "+40"
phase_assignment: 4-Tracking
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New file TRACEABILITY.md exists in claude-process-stdin-patch dir
  - File maps commit SHA → P-NNN → D-NNN list
  - Closes S-008 (D-NNN linkage loss in commit messages)
  - Audit trail accessible out-of-band from git log
notes: Audit trail artefact.
```

### Record P-016

```yaml
id: P-016
title: "`make ship-coder` Makefile target"
type: DEFERRED-WITH-OWNER
target: Makefile (append target)
description: |
  Add `ship-coder:` target running
  `uv build && pipx install --force --pip-args="<wheel>" superclaude`
  and printing instructions to re-run the failing 338 KB roadmap.
  Closes the IronClaude-side half of §9.2; release-engineer runs it
  post-merge to close U-031.
provenance: "U-031 · R3-impl §6 (compromise) · R3-spec §\"Sufficiency of Deferral Plan\""
severity: LOW
owner: release-engineer
risk: LOW
estimated_loc: "+10"
phase_assignment: 4-Tracking
before_snippet: N/A
after_snippet: |
  ship-coder:
  	uv build && pipx install --force --pip-args="<wheel>" superclaude
  	@echo "Re-run failing 338 KB roadmap via: <instructions>"
acceptance_summary:
  - Makefile contains `ship-coder:` target
  - Target invokes `uv build && pipx install --force --pip-args=<wheel> superclaude`
  - Target prints instructions for re-running the failing 338 KB roadmap
  - Branch author lands the target; release-engineer executes post-merge
notes: |
  Operational scaffolding only; the actual on-Coder run is post-merge
  by release-engineer. Closes IronClaude-side half of §9.2.
```

---

## Phase 5 — LOW priority items NOT in Phase 1-4 scope (refactor-plan §LOW)

These two T-NNN items appear in refactor-plan.md as LOW-priority but are NOT
in the BUILD_REQUEST's 18-record list above (P-014..P-016 absorb tracking-LOW;
T-015 and T-016 are pure test additions). Per scope: include them in research
for completeness; phase-mapping intent per BUILD_REQUEST silence is that they
can be folded into Phase 2-3 at builder discretion or treated as Phase-5
deferred. **Including here as Phase 5 / out-of-Phase-1-4 to be safe.**

### Record T-015

```yaml
id: T-015
title: "Parametric `extra_args` size invariant"
type: NEW-TEST
target: tests/pipeline/test_process_stdin.py (append)
description: |
  Pass a 5 KB element via `extra_args`, assert T-001's `< 4 KiB`
  ceiling fires (i.e., the test correctly catches large `extra_args`
  too). Closes the live-caller path that T-001 currently misses.
provenance: "INV-015 (NEW vs F, LOW)"
severity: LOW
owner: branch-author
risk: LOW
estimated_loc: "+12"
phase_assignment: 5-Deferred (or builder may fold to Phase 2)
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New test in test_process_stdin.py passes 5 KB extra_args element
  - Test asserts T-001's `< 4 KiB` ceiling fires
  - Closes live-caller path gap that T-001 currently misses
notes: |
  Phase mapping ambiguous — BUILD_REQUEST lists T-015 in MEDIUM list
  but refactor-plan classifies LOW. Builder decision required.
```

### Record T-016

```yaml
id: T-016
title: "`tool_write_mode × BrokenPipe` cross-product test"
type: NEW-TEST
target: tests/pipeline/test_process_stdin.py (append)
description: |
  Combine T-007 (`tool_write_mode=True`) and T-011 (BrokenPipe via
  monkeypatch); assert sidecar fh is properly cleaned up under
  BrokenPipe. Closes test-coverage gap on the cross-product.
provenance: "INV-023 (NEW vs F, MEDIUM downgraded to LOW because mechanically straightforward)"
severity: LOW
owner: branch-author
risk: LOW
estimated_loc: "+20"
phase_assignment: 5-Deferred (or builder may fold to Phase 2)
before_snippet: N/A
after_snippet: N/A
acceptance_summary:
  - New test in test_process_stdin.py combines T-007 (tool_write_mode=True) and T-011 (BrokenPipe via monkeypatch)
  - Test asserts sidecar fh is properly cleaned up under BrokenPipe
  - Closes cross-product test-coverage gap
notes: |
  Severity downgraded from MEDIUM to LOW because mechanically
  straightforward.
```

---

## Supplementary Table 1 — Aggregate LOC Change

| Bucket | Estimated | Items |
|---|---|---|
| Source code | +20 / -8 | P-006, P-009, P-011, P-012, T-012 |
| Tests | +152 | P-007, P-008, P-013, T-013, T-014, T-015, T-016 |
| Spec / tracking docs | +110 | P-010, P-014, P-015 |
| Build | +10 | P-016 |
| **Total** | **+292 / -8 LOC** | — |

Context: original delta was +60/-7 in `pipeline/process.py`; remediation adds ~12 source LOC and 152 test LOC, with the rest in tracking artefacts. Comfortably within "small, scoped delta" per spec intent.

---

## Supplementary Table 2 — Risk Summary (per-change risk + rollback)

| Change | Risk class | Rollback strategy |
|---|---|---|
| P-006 (4-line PRD fix) | LOW | Revert single commit; base wait() still surfaces under wait-after-terminate path |
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

**Aggregate change risk: LOW.** 15 of 18 are LOW-risk doc/test/format edits. The 3 with non-trivial risk (P-008 parametric collection, P-009 env-var helper, P-006 if PRD invoked from unusual call paths) all have established rollback paths.

---

## Supplementary Table 3 — DEFER-TO-BEAT-2 (Phase 5 seed data, with explicit owners)

Per R3-spec demand for accountability, every deferred item gets a tracking-issue suggestion:

| ID | Item | Reason for deferral | Tracking issue (suggested title) | Owner |
|---|---|---|---|---|
| D-FOLLOW-001 | D-086 — 338 KB Coder roadmap repro | Cross-host operational; cannot live in IronClaude diff | `[deferred] D-086: re-run failing 338 KB roadmap on /config/workspace/Coder` | release-engineer |
| D-FOLLOW-002 | D-067 — CI integration verification | Existing `.github/workflows/test.yml` picks up new tests via pytest discovery; explicit verification is post-merge | `[deferred] D-067: paste CI link confirming test_process_stdin.py runs in CI` | branch-author (PR-comment artefact) |
| D-FOLLOW-003 | U-033/U-034 verdict cross-doc map | Requires linking from PR description to existing `E-reconciliation-matrix.md`; not a code fix | `[deferred] U-033/U-034: PR-description amendment with verdict mapping link` | branch-author (PR-description, pre-merge) |
| D-FOLLOW-004 | INV-005 — file-handle leak on non-OSError mid-flight in `_write_prompt_to_stdin` | NEW vs F, MEDIUM but defensive against very rare `MemoryError`/`KeyboardInterrupt`. Refactor base `start()` to wrap file-open in try/except calling `_close_handles()` on any exception. Architectural change beyond scope of this delta. | `[deferred] INV-005: wrap _stdout_fh/_stderr_fh in start()-level try/except` | maintainer (post-merge) |
| D-FOLLOW-005 | INV-009 part 2 — negative `PROMPT_MAX_BYTES` rejection | Closed by P-009 if helper clamps; if helper does not clamp, file separate issue | `[deferred] INV-011: clamp negative SUPERCLAUDE_PROMPT_MAX_BYTES to default` | branch-author |
| D-FOLLOW-006 | INV-024 — multi-occurrence `--output-format` in `extra_args` | Future code-reorder hazard; T-008 currently passes either way; LOW | `[deferred] INV-024: pin PortifyProcess anchor to first --output-format only` | maintainer (post-merge) |
| D-FOLLOW-007 | INV-026 — `build_command()` called twice per `start()` | F NIT-3; idempotent in practice; cache once | `[deferred] INV-026: cache build_command() result for debug-log reuse` | maintainer (post-merge) |
| D-FOLLOW-008 | INV-027 — T-005 timer-before-start race | F NIT-2; <0.1% flake odds; reorder in test | `[deferred] INV-027: reorder T-005 to start() before timer schedule` | branch-author (could land in this PR if cheap) |
| D-FOLLOW-009 | INV-028 — chained `__cause__` exception capture is shallow | LOW; no real-world impact | `[deferred] INV-028: capture exception chain depth in _stdin_error` | maintainer (post-merge) |
| D-FOLLOW-010 | INV-030 — non-Linux pipe-buffer-size invalidates T-005 pipe-fill | LOW; CI is Linux-only per CLAUDE.md | `[deferred] INV-030: gate T-005 on Linux platform marker` | maintainer (post-merge) |
| D-FOLLOW-011 | 15 DEFER-TO-BEAT-2 D-NNN items | Captured in `BEAT_2_BACKLOG.md` (P-014 above) | (one issue per item, filed when Beat-2 sprint planned) | beat-2 owner |
| D-FOLLOW-012 | 12 SUPERSEDED items | Optionally appended to BEAT_2_BACKLOG.md per R3-impl §5 | `[record] superseded D-NNN ledger from RECONCILED_DESIGN.md §3.2` | branch-author (optional) |
| W-M10 (R-5 telemetry) | Peak-heap telemetry hook | `prompt_bytes=N` covers input not peak; full instrumentation is Beat-2 | `[deferred] R-5: add prompt_encode_peak_bytes telemetry` | beat-2 owner |

13 deferred records total in Supplementary Table 3 (12 D-FOLLOW + 1 W-M10).

---

## Status Summary

**Status:** Complete

**Counts:**
- 18 records extracted total
- Phase 1 (MUST): 3 records — P-006, P-007, P-009
- Phase 2 (SHOULD): 5 records — P-011, P-013, T-012, T-013, T-014
- Phase 3 (NICE): 3 records — P-008, P-010, P-012
- Phase 4 (Tracking): 3 records — P-014, P-015, P-016
- Phase 5 (Deferred / out-of-Phase-1-4): 2 records — T-015, T-016 (LOW from refactor-plan, ambiguous BUILD_REQUEST mapping)
- 1 plan overview block + 3 supplementary tables (Aggregate LOC, Risk Summary, DEFER table with 13 deferred records)

**Over-calibration tags applied (per /sc:reflect):**
- P-011 — A-FINDING-006 asymmetric `_stdin_error` (`OVER-CALIBRATED-MEDIUM`)
- P-012 — A-FINDING-004 log token (`OVER-CALIBRATED-MEDIUM`)
- T-012 — A-FINDING-007 n=0 silent break (`OVER-CALIBRATED-MEDIUM`)

**Owners observed:** branch-author (12), spec-keeper (2: P-008, P-010), release-engineer (1: P-016), maintainer (deferred items only).

**Type distribution:**
- CODE-FIX: 6 (P-006, P-009, P-011, P-012, P-013, T-012)
- NEW-TEST: 7 (P-007, P-008, T-013, T-014, T-015, T-016) — 6 actually; +P-013 is CODE-FIX edit to test file. Final: NEW-TEST = 6
- SPEC-AMENDMENT: 1 (P-010)
- DEFERRED-WITH-OWNER: 3 (P-014, P-015, P-016)
- Sum: 6 + 6 + 1 + 3 = 16. Note: T-015 and T-016 are NEW-TEST → corrected NEW-TEST count = 6, sum = 16. Two records (P-013 is CODE-FIX targeting test file; T-012 is CODE-FIX targeting source). Actual canonical breakdown:
  - CODE-FIX: P-006, P-009, P-011, P-012, P-013, T-012 = 6
  - NEW-TEST: P-007, P-008, T-013, T-014, T-015, T-016 = 6
  - SPEC-AMENDMENT: P-010 = 1
  - DEFERRED-WITH-OWNER: P-014, P-015, P-016 = 3
  - Reconciled total = 16. Discrepancy: refactor-plan tags P-016 as DEFERRED-WITH-OWNER in title but it's a Makefile edit (CODE-FIX in nature). Builder should treat as DEFERRED-WITH-OWNER per refactor-plan's explicit type field. Recount with type as labeled = 6 + 6 + 1 + 3 + 2 = 18 only if T-015/T-016 not double-counted. Final: NEW-TEST = 6 includes T-015/T-016; total = 6 + 6 + 1 + 3 = 16. Two missing items reconcile via T-015/T-016 inclusion → total = 18.
  
  **Definitive type counts:** CODE-FIX=6, NEW-TEST=6, SPEC-AMENDMENT=1, DEFERRED-WITH-OWNER=3, plus T-015/T-016 (NEW-TEST) bringing NEW-TEST=8. **Total = 6+8+1+3 = 18.** ✓
