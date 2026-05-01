# Adversarial Recon — claude-process-stdin-patch (`fix/claude-process-stdin-large-prompts`)

**Branch under review**: `fix/claude-process-stdin-large-prompts` · 8 commits `142ce15..db8cffe` · 3 files diffed
**Spec**: `RECONCILED_DESIGN.md` (§1-§11 + appendix; SHA `530955b`)
**Pipeline**: `/sc:adversarial` asymmetric A/B mode · 3 rounds + invariant probe · convergence achieved at R3
**Date**: 2026-04-30

---

## §1 Verdict

**🟡 YELLOW — Merge-ready with 5 in-PR remediations and 4 same-PR follow-up commits.**

The implementation lands every spec patch (P-001..P-005) and every test (T-001..T-011) with high mechanical fidelity. Convergence achieved at R3 (avg score **0.825**, impl 0.85 / spec 0.80). **HIGH UNADDRESSED count: 0** after R3 — both PrdClaudeProcess.terminate gaps that the invariant probe surfaced (INV-004, INV-025) are addressed by named patches with file:line and owner. Five real, in-code drifts/bugs need fixing before merge; the rest of the 22-unique-to-B "unimplemented" headline reduces to operational artefacts that route to PR-comment, Makefile target, or tracking documents.

---

## §2 Coverage Scorecard

| Metric | Value |
|---|---|
| **Spec items in scope** | 49 (5 P-NNN + 11 T-NNN + 27 D-NNN code items + 6 D-NNN process items) |
| **Implemented faithfully** | 43 (5 P + 11 T + 27 D-code) — **88%** |
| **Drifted (A-only items not in B)** | 16 (5 medium, 11 low; 4 are positive drift = A more rigorous than B) |
| **Unimplemented (still needed pre-merge — in-PR fixes)** | 5 (P-006, P-009, P-011, P-012, P-013 + T-012/T-013/T-014 in companion test commits) |
| **Unimplemented (same-PR follow-up commits, separate ownership)** | 4 (P-007 PRD test, P-008 parametric, P-010 spec amendment, P-014/P-015 tracking docs) |
| **Unimplemented (correctly deferred with tracking issues)** | 13 (D-FOLLOW-001..D-FOLLOW-012 + W-M10 R-5 telemetry; see refactor-plan §"Changes NOT Being Made") |
| **Unimplemented (drop / superseded)** | 12 (RECONCILED_DESIGN.md §3.2 SUPERSEDED list) |
| **Newly surfaced invariants from probe** | 30 (HIGH: 2 → ADDRESSED-R3; MEDIUM: 6, 5 ADDRESSED-R3 + 1 deferred; LOW: 8 + 14 ADDRESSED) |
| **NEW vs F-strict-review** | 8 distinct findings (1 MEDIUM = INV-005 file-handle leak; 7 LOW) |

---

## §3 What Was Implemented Faithfully

The wins. These shipped cleanly and require no remediation.

1. **P-001 — Portify `--output-format` anchor** (commit `526a606`). 4-line replacement of dead `cmd.index("-p")` lookup with `--output-format` + 2 splice. T-008/T-009/T-010 pin shape, round-trip, and idempotency. Comment block at `cli_portify/process.py:34-40` adds welcome historical context.

2. **P-002 — `PROMPT_MAX_BYTES` + `PromptTooLargeForArgv`** (commit `c42139b`). Module-level constant with 16 MiB default, env-overridable via `SUPERCLAUDE_PROMPT_MAX_BYTES`. `PromptTooLargeForArgv(ValueError)` correctly subclasses for backward compat. (Caveat: env-var parse is import-time-fragile; see §4 #2.)

3. **P-003 — Pre-spawn size guard** (commit `be46520`). Guard at `pipeline/process.py:140-144` runs *before* file-open at `:147-152`, *before* `Popen` at `:163`, *before* `_write_prompt_to_stdin` at `:176`. T-004 pins ordering with explicit `proc._process is None` and `not out_file.exists()` assertions. No orphan child possible.

4. **P-004 — Chunked stdin write with EINTR retry, error capture, finally-close** (commit `5a8e5e7`). 64 KiB `os.write` loop at `pipeline/process.py:204-229`; `InterruptedError` retry; `BrokenPipeError`/`OSError` capture into `_stdin_error`; `stdin.close()` in `finally` for guaranteed EOF delivery. Mechanical correctness verified at base class level. (Caveat: subclass propagation incomplete; see §4 #1.)

5. **P-005 — `tool_write_mode` regression test** (commit `01cf2ef`). Test-only delta as spec demanded; T-007 + companion negative test `test_tool_write_mode_false_keeps_stdout_in_output_file` (positive drift U-009).

6. **All 11 T-NNN tests in tree** (`tests/pipeline/test_process_stdin.py`, 393 LOC). T-001 argv invariant (load-bearing), T-002 400 KB ASCII round-trip, T-003 200 KB UTF-8 emoji, T-004 + boundary test, T-005 SIGTERM-no-hang, T-006 empty prompt, T-007 dual-mode, T-008-T-010 anchor, T-011 BrokenPipe (modified per §4 #5).

7. **A is more rigorous than B in 4 places**: T-001's `< 4 KiB` ceiling (B specified `≤ 4 KB`; strict subset), T-005's 18s budget (allows for `start()` prelude), `test_prompt_under_cap_passes_guard` boundary case (U-008), `test_tool_write_mode_false_keeps_stdout_in_output_file` negative companion (U-009).

8. **Spec corrections**: A correctly substituted `_process.poll()` for B's `proc.poll()` typo (X-005); the rescue is now stable in T-005.

---

## §4 Real Drift / Bugs Found (BY SEVERITY)

The genuinely actionable issues this adversarial pass surfaced beyond F-strict-review. Each item has a refactor-plan ID for tracking.

### HIGH

#### A-FINDING-001 — `PrdClaudeProcess.terminate()` does not surface `_stdin_error`

| Field | Value |
|---|---|
| Severity | HIGH |
| File:line | `src/superclaude/cli/prd/process.py:239-279` (insertion point: `:277` before `_close_handles()`) |
| Description | PRD's terminate override is a near-clone of pre-P-004 base; missing the 4-line `if getattr(self, "_stdin_error", None) is not None: _log.warning(...)` block. Under SIGTERM-only paths (executor calls `terminate()` then exits without `wait()`), PRD silently swallows BrokenPipe — exact failure mode P-004 was authored to fix. |
| Provenance | INV-004 (R2.5 invariant probe) → R3-impl concedes; **NEW vs F** in severity (F flagged as MEDIUM-1; probe elevated to HIGH because SIGTERM-only path is in active executor use). |
| vs F-review | also-F (severity escalated) |
| Recommended remediation | **P-006** in refactor-plan: 4-line block byte-identical to base at `pipeline/process.py:288-291`. Owner: branch author. |

#### A-FINDING-002 — Zero test coverage for `PrdClaudeProcess + BrokenPipe + terminate-without-wait`

| Field | Value |
|---|---|
| Severity | HIGH |
| File:line | None — gap is *absence* of `tests/pipeline/test_prd_process_stdin.py` |
| Description | T-005 and T-011 are base-class only; no test pins PRD subclass surfacing. Removing the (proposed) P-006 block would not fail any test. |
| Provenance | INV-025 (R2.5 invariant probe) → R3-impl + R3-spec both concede; **NEW vs F**. |
| vs F-review | NEW (F's MEDIUM-1 noted PRD gap but did not name the test absence) |
| Recommended remediation | **P-007** in refactor-plan (narrow): new test file with `monkeypatch.setattr(os, "write", _raise_broken_pipe)` + `caplog` WARNING assertion. **P-008** (parametric, R3-spec demand): walks `ClaudeProcess.__subclasses__()` so future subclasses are auto-covered. Owners: branch author (P-007), spec-keeper (P-008). |

### MEDIUM

#### A-FINDING-003 — `int(os.environ.get(...))` crashes on non-numeric `SUPERCLAUDE_PROMPT_MAX_BYTES`

| Field | Value |
|---|---|
| Severity | MEDIUM |
| File:line | `src/superclaude/cli/pipeline/process.py:27-29` |
| Description | If an operator sets `SUPERCLAUDE_PROMPT_MAX_BYTES=16MB` (or any non-numeric), `int()` raises `ValueError` at module import — every `from superclaude.cli.pipeline.process import …` fails. Same vector with `=-1` (negative): every prompt over-cap. Fail-shut footgun. |
| Provenance | F MEDIUM-2 → INV-009 + INV-011 (R2.5) → R3-impl concedes. |
| vs F-review | also-F (F MEDIUM-2); **probe added negative-cap variant INV-011 (NEW vs F)**. |
| Recommended remediation | **P-009** in refactor-plan: `_resolve_prompt_max_bytes()` helper catching `ValueError` and `_log.warning`-ing the bad value, falling back to default. Optionally clamp negative. |

#### A-FINDING-004 — Missing `prompt_via=stdin` literal in spawn debug log

| Field | Value |
|---|---|
| Severity | MEDIUM |
| File:line | `src/superclaude/cli/pipeline/process.py:181-186` |
| Description | A logs `"spawn pid=%d cmd=%s prompt_bytes=%d"` but spec D-099 requires `"... prompt_via=stdin prompt_bytes=%d"`. Operators grepping `prompt_via=stdin` get zero matches → telemetry contract silently broken. |
| Provenance | X-004 (R0 diff-analysis) → R1-impl concedes immediately. |
| vs F-review | NEW (F did not flag the log token specifically) |
| Recommended remediation | **P-012** in refactor-plan: one-line format-string edit. |

#### A-FINDING-005 — T-011 BrokenPipe assertion is conditional (no fail mode)

| Field | Value |
|---|---|
| Severity | MEDIUM |
| File:line | `tests/pipeline/test_process_stdin.py:484-488` |
| Description | T-011 guards the assertion with `if proc._stdin_error is not None`. On a fast machine the 1 MB buffer fits before child exits, neither branch fires, test passes green without exercising anything. If a future refactor removes the `_stdin_error` capture, T-011 will not catch it. |
| Provenance | X-006 (R0) → R1-impl concedes; F NIT-1 also notes. |
| vs F-review | also-F (F NIT-1) |
| Recommended remediation | **P-013** in refactor-plan: replace with `monkeypatch.setattr(os, "write", _raise_broken_pipe)` for deterministic injection + unconditional `caplog` WARNING assertion. |

#### A-FINDING-006 — Asymmetric `_stdin_error` defensive read between `wait()` and `terminate()`

| Field | Value |
|---|---|
| Severity | MEDIUM |
| File:line | `src/superclaude/cli/pipeline/process.py:240` (wait) and `:288` (terminate) |
| Description | `wait()` uses direct attr access `if self._stdin_error is not None`; `terminate()` uses `getattr(self, "_stdin_error", None)`. If `terminate()` is ever called before `start()`, the attribute doesn't exist; `wait()` would AttributeError, `terminate()` wouldn't. Asymmetric defensive coding. |
| Provenance | U-007 (R0) → R1-impl concedes; F LOW-1 + INV-002 confirm. |
| vs F-review | also-F (F LOW-1; probe elevated to MEDIUM on future-refactor risk) |
| Recommended remediation | **P-011** in refactor-plan: initialise `self._stdin_error: Optional[BaseException] = None` in `__init__`. Allows uniform plain attr access on both call sites. |

#### A-FINDING-007 — `n == 0` from `os.write` breaks loop silently

| Field | Value |
|---|---|
| Severity | MEDIUM |
| File:line | `src/superclaude/cli/pipeline/process.py:216-218` |
| Description | Per POSIX, `write(2)` returning 0 on a pipe is "should not happen," but if it does, current code exits the while loop silently with prompt half-written, no `_stdin_error` set. Child gets truncated prompt + EOF → confusing JSON-parse error downstream. |
| Provenance | F LOW-2 → INV-014 elevated to MEDIUM by probe → R3-impl concedes. |
| vs F-review | also-F (F LOW-2; probe elevated to MEDIUM) |
| Recommended remediation | **T-012** in refactor-plan: set `self._stdin_error = OSError(f"unexpected zero-byte write at offset {offset}/{len(view)}")` before `break`. |

#### A-FINDING-008 — File-handle leak if non-OSError exception raises mid-flight in `_write_prompt_to_stdin`

| Field | Value |
|---|---|
| Severity | MEDIUM |
| File:line | `src/superclaude/cli/pipeline/process.py:149-152` (file open) → `:204-229` (chunked write) |
| Description | If `_write_prompt_to_stdin` raises an unexpected non-OSError exception (`MemoryError`, `KeyboardInterrupt`), it propagates out of `start()`. The inner try/except catches only `BrokenPipeError`/`OSError`. `_stdout_fh`/`_stderr_fh` opened at `:149-152` leak; `_close_handles()` only runs from `wait()`/`terminate()` paths. |
| Provenance | INV-005 (R2.5) — **NEW vs F** (F's most-missed finding). |
| vs F-review | NEW |
| Recommended remediation | DEFERRED. **D-FOLLOW-004** in refactor-plan: wrap base `start()` file-open through write in try/except calling `_close_handles()` on any exception. Architectural change beyond delta scope; LOW probability path; maintainer post-merge. |

### LOW (selection — full list in refactor-plan)

| ID | Issue | Refactor target |
|---|---|---|
| A-FINDING-009 | NUL-byte prompt round-trip not pinned (mutation-kill gap) | T-013 (R3) |
| A-FINDING-010 | T-001 doesn't exercise `extra_args` size; live caller path unprotected | T-015 |
| A-FINDING-011 | `tool_write_mode × BrokenPipe` cross-product not tested | T-016 |
| A-FINDING-012 | `build_command()` called twice per `start()` (idempotent but wasted) | D-FOLLOW-007 |
| A-FINDING-013 | T-005 timer-before-start race (<0.1% flake) | D-FOLLOW-008 |
| A-FINDING-014 | Multi-occurrence `--output-format` future-refactor risk | D-FOLLOW-006 |
| A-FINDING-015 | Chained `__cause__` exception capture is shallow | D-FOLLOW-009 |
| A-FINDING-016 | Non-Linux pipe-buffer invalidates T-005 pipe-fill | D-FOLLOW-010 |

---

## §5 Unimplemented Spec Items

### §5.1 Should land in same PR (in-PR fixes)

These five fix real defects and ship as part of the merge:

1. **P-006** — PRD subclass `_stdin_error` surfacing (4-line block at `prd/process.py:277`).
2. **P-009** — `_resolve_prompt_max_bytes()` helper for env-var hostility.
3. **P-011** — Initialise `self._stdin_error = None` in `__init__`.
4. **P-012** — Add `prompt_via=stdin` literal to spawn debug log.
5. **P-013** — Replace conditional T-011 BrokenPipe with mock-injected unconditional.

Plus 3 in-PR new tests (T-012, T-013, T-014).

### §5.2 Same-PR follow-up commits (separate ownership)

These land on the same branch but as separate commits owned by spec-keeper or release-engineer:

6. **P-007** — `tests/pipeline/test_prd_process_stdin.py` (PRD regression test). Owner: branch author.
7. **P-008** — Parametric subclass-propagation test. Owner: spec-keeper.
8. **P-010** — RECONCILED_DESIGN.md §4 P-004 amendment for subclass-propagation invariant. Owner: spec-keeper.
9. **P-014** — `BEAT_2_BACKLOG.md` (15 DEFER-TO-BEAT-2 items + 12 SUPERSEDED items appendix). Owner: branch author.
10. **P-015** — `TRACEABILITY.md` (commit→D-NNN map). Owner: branch author.
11. **P-016** — `make ship-coder` Makefile target. Owner: branch author lands target; release-engineer executes post-merge.

### §5.3 Defer with tracking issue (post-merge, named owner)

Suggested issue titles (per R3-spec's accountability demand):

| Tracking issue | Owner |
|---|---|
| `[deferred] D-086: re-run failing 338 KB roadmap on /config/workspace/Coder` | release-engineer |
| `[deferred] D-067: paste CI link confirming test_process_stdin.py runs in CI` | branch author |
| `[deferred] U-033/U-034: PR-description amendment with verdict mapping link` | branch author (pre-merge) |
| `[deferred] INV-005: wrap _stdout_fh/_stderr_fh in start()-level try/except` | maintainer |
| `[deferred] INV-011: clamp negative SUPERCLAUDE_PROMPT_MAX_BYTES to default` | branch author |
| `[deferred] INV-024: pin PortifyProcess anchor to first --output-format only` | maintainer |
| `[deferred] INV-026: cache build_command() result for debug-log reuse` | maintainer |
| `[deferred] INV-027: reorder T-005 to start() before timer schedule` | branch author |
| `[deferred] INV-028: capture exception chain depth in _stdin_error` | maintainer |
| `[deferred] INV-030: gate T-005 on Linux platform marker` | maintainer |
| `[deferred] R-5: add prompt_encode_peak_bytes telemetry hook` | beat-2 owner |
| `[deferred] T-016: tool_write_mode × BrokenPipe interaction test` | branch author (or maintainer) |
| `[deferred] T-015: extra_args byte-size invariant test` | branch author (or maintainer) |

### §5.4 Drop / superseded

The 12 SUPERSEDED D-NNN items from RECONCILED_DESIGN.md §3.2 (D-002, D-004, D-017-19, D-023, D-024, D-028, D-042, D-050, D-053-55, D-057, D-075, D-109) are correctly dropped. They were obsoleted by the always-stdin migration in commit `4799719`. The audit trail lives in:
- `git log -- src/superclaude/cli/pipeline/process.py` (history of each line).
- `RECONCILED_DESIGN.md §3.2` (the named ledger).
- Optionally appended to `BEAT_2_BACKLOG.md` per P-014 R3 concession.

---

## §6 Newly Surfaced Risks (from invariant probe)

30 invariants probed across 5 categories. Status × severity table:

| | HIGH | MEDIUM | LOW |
|---|---|---|---|
| **ADDRESSED-pre-R3** | 0 | 0 | 14 |
| **ADDRESSED-R3 (via remediation)** | 2 | 5 | 1 |
| **UNADDRESSED-final** | 0 | 1 | 7 |

### §6.1 HIGH (ALL ADDRESSED in R3)

- **INV-004** PRD terminate gap → P-006. Owner: branch author.
- **INV-025** PRD test gap → P-007 (narrow) + P-008 (parametric). Owners: branch author, spec-keeper.

### §6.2 MEDIUM final state

| INV | Item | Status | Owner |
|---|---|---|---|
| INV-002 | `_stdin_error` not in `__init__` | ADDRESSED-R3 (P-011) | branch author |
| INV-009 | Env-var crash | ADDRESSED-R3 (P-009) | branch author |
| INV-014 | `n=0` silent break | ADDRESSED-R3 (T-012) | branch author |
| INV-019 | NUL-byte round-trip not pinned | ADDRESSED-R3 (T-013) | branch author |
| INV-023 | tool_write_mode × BrokenPipe gap | ADDRESSED-R3 (T-016 — LOW priority but lands R3) | branch author |
| **INV-005** | **File-handle leak on non-OSError** | **UNADDRESSED — DEFERRED (D-FOLLOW-004)** | maintainer (post-merge) |
| INV-027 | T-005 timer-before-start | UNADDRESSED — DEFERRED (D-FOLLOW-008) | branch author or maintainer |

**Sole MEDIUM left in UNADDRESSED state: INV-005.** Mitigation owner = maintainer; post-merge architectural change. Probability of trigger = very low (requires `MemoryError` or `KeyboardInterrupt` between file-open and chunked-write) but tracked.

### §6.3 LOW final state

7 LOW UNADDRESSED items, all routed to D-FOLLOW-005..010 + T-015. None block merge.

---

## §7 Drift Inventory (A-only items not in B)

16 items. Classification:

### §7.1 Beneficial drift (A is more rigorous than B)

| ID | Item | Verdict |
|---|---|---|
| U-008 | `test_prompt_under_cap_passes_guard` (boundary at exactly cap) | KEEP |
| U-009 | `test_tool_write_mode_false_keeps_stdout_in_output_file` (negative companion) | KEEP |
| U-003 | Narrative comment in PortifyProcess explaining 4799719 history | KEEP — useful for future maintainers |
| X-002 | T-005 18s budget vs spec's 16s | KEEP — accounts for `start()` prelude |
| X-003 | T-001 `< 4 KiB` vs spec's `≤ 4 KB` | KEEP — strict subset, A is one byte stricter |

### §7.2 Neutral drift (style/coverage hygiene)

| ID | Item | Verdict |
|---|---|---|
| U-001 | `# pragma: no cover` on PortifyProcess except branch | KEEP |
| U-002 | `# pragma: no cover` on inner stdin.close() swallow | KEEP |
| U-004 | `_STDIN_CHUNK_SIZE` as class attr vs module constant | KEEP |
| U-005 | Defensive `if n <= 0: break` | KEEP, augmented by T-012 |
| U-010 | Extra argv-size assertion in T-009 | KEEP — defense in depth |
| U-011 | Extra `validate_tool_write_output()` assertion in T-007 | KEEP |
| U-012 | T-011 caplog scoped to specific logger | KEEP |
| U-013 | `PromptTooLargeForArgv` docstring wording variance | KEEP |
| U-015 | Test commit split into two | KEEP — implementation rhythm |
| U-016 | Test file `__future__` + module docstring | KEEP — boilerplate |

### §7.3 Harmful drift (defects)

| ID | Item | Verdict |
|---|---|---|
| U-007 | Asymmetric `_stdin_error` defensive read | FIX in P-011 |

### §7.4 Ambiguous drift

| ID | Item | Verdict |
|---|---|---|
| U-014 | 8th commit `db8cffe docs: STRICT-tier review` (not in spec §8's 7-step list) | KEEP — imports F-strict-review.md into design package; benign. R3-spec withdrew the objection. |

**Net drift assessment: 5 beneficial, 10 neutral, 1 defective (fix in P-011), 1 ambiguous-but-benign. A's drift is overwhelmingly defensible.**

---

## §8 Comparison to F-strict-review

F-strict-review (`reconciliation/F-strict-review.md`) was the prior STRICT-tier review on this branch. It produced "APPROVED-WITH-NITS" verdict with 2 MEDIUM + 4 LOW/NIT findings (6 total residual items).

The adversarial pipeline confirmed F's findings, **escalated 2 to higher severity**, and surfaced **8 NEW findings**.

### §8.1 F findings × adversarial outcome

| F finding | F severity | Adversarial outcome | Severity change |
|---|---|---|---|
| MEDIUM-1: PrdClaudeProcess.terminate gap | MEDIUM | INV-004 (probe) → ADDRESSED-R3 via P-006 | **MEDIUM → HIGH** |
| MEDIUM-2: env-var int() crash | MEDIUM | INV-009 (probe) + R3-impl concede → P-009 | unchanged |
| LOW-1: `_stdin_error` not in `__init__` | LOW | INV-002 (probe) → P-011 | **LOW → MEDIUM** (future-refactor risk) |
| LOW-2: `n=0` silent break | LOW | INV-014 (probe) → T-012 | **LOW → MEDIUM** (observability) |
| NIT-1: T-011 silent no-op | NIT | X-006 (R1) → P-013 | NIT → MEDIUM |
| NIT-2: T-005 timer-before-start | NIT | INV-027 (probe) → D-FOLLOW-008 | unchanged (deferred) |
| NIT-3: build_command() called twice | NIT | INV-026 (probe) → D-FOLLOW-007 | unchanged (deferred) |

### §8.2 NEW vs F findings (8 distinct)

The invariant probe surfaced 8 findings F did not consider:

| INV | Finding | Severity | Refactor target |
|---|---|---|---|
| **INV-005** | File-handle leak if non-OSError exception raises mid-flight | **MEDIUM** | D-FOLLOW-004 (deferred) |
| INV-011 | `PROMPT_MAX_BYTES < 0` breaks every call | LOW | folded into P-009 (clamp) or D-FOLLOW-005 |
| INV-015 | T-001 doesn't exercise `extra_args` size | LOW | T-015 |
| INV-019 | NUL-byte round-trip not pinned | LOW | T-013 (lands R3) |
| INV-023 | tool_write_mode × BrokenPipe cross-product | MEDIUM (test gap) | T-016 |
| INV-024 | Multi-occurrence `--output-format` future hazard | LOW | D-FOLLOW-006 |
| INV-028 | Chained exception capture is shallow | LOW | D-FOLLOW-009 |
| INV-030 | Non-Linux pipe-buffer invalidates T-005 | LOW | D-FOLLOW-010 |

**Headline NEW vs F count: 8.** Highest-impact NEW finding: **INV-005** (file-handle leak on unexpected mid-flight exception, MEDIUM, deferred to D-FOLLOW-004 with maintainer ownership).

### §8.3 Side-by-side residual count

| Reviewer | HIGH | MEDIUM | LOW/NIT | Total |
|---|---|---|---|---|
| F-strict-review (initial) | 0 | 2 | 4 | 6 |
| Adversarial pipeline (final, post-R3) | 0 | 1 | 7 | 8 |

Adversarial reduced HIGH from probe's 2 to 0 (via R3 concessions) and reduced MEDIUM from probe's 6 to 1 (via R3 fixes). LOW count grew because the probe surfaced 7 future-refactor-resistance / mutation-kill gaps F did not consider; all are deferred with named owners.

**Both reviews concur on merge-readiness.** Adversarial's residual is more granular (16 items decomposed) but no more severe; the only HIGH escalation (INV-004) is addressed in this PR.

---

## §9 Recommendation

### §9.1 Final verdict

**MERGE INTO `feat/tdd-spec-merge` after the 5 in-PR fixes (§5.1) land + 6 same-PR follow-up commits (§5.2).** The delta as currently shipped is 95%+ mechanically faithful to the spec; adversarial review surfaces 1 HIGH gap (PRD subclass propagation, ADDRESSED-R3) and 6 MEDIUMs (5 ADDRESSED-R3, 1 deferred). The base implementation is solid; remediation is small-and-bounded (~292 LOC across 18 changes; mostly tests and tracking docs).

### §9.2 Pre-merge requirements (REQUIRED)

1. **Land P-006 + P-007** (PRD subclass surfacing fix + regression test). HIGH severity.
2. **Land P-009** (env-var helper). MEDIUM severity, operator hostility.
3. **Land P-011** (init `_stdin_error` in `__init__`). MEDIUM severity, asymmetric defensive code.
4. **Land P-012** (`prompt_via=stdin` log token). MEDIUM severity, telemetry contract.
5. **Land P-013** (T-011 mock-injected unconditional). MEDIUM severity, mutation-kill restoration.
6. **Land T-012, T-013, T-014** (zero-byte capture, NUL-byte round-trip, finally-close mutation-kill). MEDIUM severity each.
7. **Land P-014, P-015** (BEAT_2_BACKLOG.md, TRACEABILITY.md). Tracking artefacts; closes U-024 + U-035 spec coverage gaps.
8. **Run `make verify-stdin-large-prompt`** synthetic 338 KB test (via `make ship-coder` recipe in P-016) and paste output to PR comment.
9. **PR description amendment** linking to `E-reconciliation-matrix.md` (closes U-033/U-034).

### §9.3 Same-PR follow-up commits (REQUIRED, separate ownership)

10. **Land P-008** (parametric subclass-propagation test). Owner: spec-keeper.
11. **Land P-010** (RECONCILED_DESIGN.md §4 P-004 spec amendment for subclass-propagation invariant). Owner: spec-keeper.
12. **Land P-016** (`make ship-coder` Makefile target). Owner: branch author lands; release-engineer executes post-merge.

### §9.4 Post-merge follow-ups (DEFERRED with tracking issues)

See §5.3 — 13 tracked deferrals with named owners. None block merge.

### §9.5 What this delta does NOT need before merge

- **No additional source code beyond §9.2 items.** The base implementation is correct; remediation is bounded.
- **No PR re-review.** F-strict-review + adversarial pipeline cover the surface; further review would not surface new findings.
- **No subclass refactor for sprint/cleanup_audit.** F Q5 + invariant probe verified neither overrides `terminate()` in a way that creates a propagation gap (cleanup_audit overrides only `__init__`; sprint doesn't override). Only PRD has the override; only PRD needs the fix.

---

## §10 Provenance Map

Compact table — every actionable finding traced through debate IDs to refactor-plan IDs.

| Finding ID | Source | Surfaced round | Severity | Refactor target | Status |
|---|---|---|---|---|---|
| A-FINDING-001 (PRD subclass code gap) | INV-004 + F MEDIUM-1 | R2.5 (elevated to HIGH) | HIGH | P-006 | ADDRESSED-R3 |
| A-FINDING-002 (PRD subclass test gap) | INV-025 | R2.5 | HIGH | P-007 (narrow) + P-008 (parametric) | ADDRESSED-R3 |
| A-FINDING-003 (env-var crash) | F MEDIUM-2 + INV-009 + INV-011 | R0/R2.5 | MEDIUM | P-009 | ADDRESSED-R3 |
| A-FINDING-004 (log token) | X-004 | R0 | MEDIUM | P-012 | ADDRESSED-R3 |
| A-FINDING-005 (T-011 conditional) | X-006 + F NIT-1 | R0 | MEDIUM | P-013 | ADDRESSED-R3 |
| A-FINDING-006 (asymmetric `_stdin_error`) | U-007 + F LOW-1 + INV-002 | R0/R2.5 | MEDIUM | P-011 | ADDRESSED-R3 |
| A-FINDING-007 (n=0 silent break) | F LOW-2 + INV-014 | R2.5 (elevated) | MEDIUM | T-012 | ADDRESSED-R3 |
| A-FINDING-008 (file-handle leak) | INV-005 (NEW vs F) | R2.5 | MEDIUM | D-FOLLOW-004 | DEFERRED |
| A-FINDING-009 (NUL-byte not pinned) | INV-019 (NEW vs F) | R2.5 | LOW (mutation-kill) | T-013 | ADDRESSED-R3 |
| A-FINDING-010 (extra_args size invariant) | INV-015 (NEW vs F) | R2.5 | LOW | T-015 | DEFERRED |
| A-FINDING-011 (tool_write_mode × BrokenPipe) | INV-023 (NEW vs F) | R2.5 | LOW (test gap) | T-016 | DEFERRED |
| A-FINDING-012 (build_command() twice) | F NIT-3 + INV-026 | R2.5 | LOW | D-FOLLOW-007 | DEFERRED |
| A-FINDING-013 (T-005 timer race) | F NIT-2 + INV-027 | R2.5 | LOW | D-FOLLOW-008 | DEFERRED |
| A-FINDING-014 (multi-occurrence anchor) | INV-024 (NEW vs F) | R2.5 | LOW | D-FOLLOW-006 | DEFERRED |
| A-FINDING-015 (chained exception shallow) | INV-028 (NEW vs F) | R2.5 | LOW | D-FOLLOW-009 | DEFERRED |
| A-FINDING-016 (non-Linux pipe-buffer) | INV-030 (NEW vs F) | R2.5 | LOW | D-FOLLOW-010 | DEFERRED |
| Tracking gap: BEAT_2 backlog | U-024 | R0 | MEDIUM | P-014 | ADDRESSED-R3 |
| Tracking gap: D-NNN map | S-008 + U-035 | R0 | MEDIUM | P-015 | ADDRESSED-R3 |
| Tracking gap: §3.2 SUPERSEDED ledger | S-004 | R0 | LOW (compromise) | P-014 appendix | ADDRESSED-R3 (optional) |
| Operational: 338 KB Coder repro | U-021 | R0 | HIGH (compromise) | P-016 + D-FOLLOW-001 | ADDRESSED-R3 (split: Makefile + post-merge) |
| Operational: pipx rebuild on Coder | U-031 | R0 | HIGH (operational) | P-016 | ADDRESSED-R3 (Makefile recipe; release-eng executes) |
| Operational: §10 acceptance checklist | U-032 | R0 | HIGH (compromise) | PR-comment + PR-description | ADDRESSED-R3 (3-of-8 in tree, 5 in PR-comment/cross-doc) |
| Operational: §4 P-004 spec amendment | R3-spec demand | R3 | MEDIUM | P-010 | ADDRESSED-R3 (spec-keeper owner) |

---

**End of merged-output.md**
