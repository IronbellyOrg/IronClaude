# QA Report: Task-Research Alignment (Cross-Validation)

**QA Mode:** task-integrity
**Lens:** task-research-alignment
**Stance:** ADVERSARIAL (assume builder dropped/misrepresented research findings)
**Date:** 2026-06-19
**Analyst:** rf-analyst (no team context — verdict returned to parent)

**Task file:** `.dev/tasks/to-do/TASK-RF-swarm-tui-fr1-regfix-20260619-021719/TASK-RF-swarm-tui-fr1-regfix-20260619-021719.md`
**Research files cross-validated:**
- `research/01-reg1-redirect-and-print-gating.md`
- `research/02-drift3-drift4-fr5-poll-loop.md`
- `research/03-fr1-audit-extension-and-pty-smoke.md`
- `research-notes.md`

---

## Method

For each research finding I located the corresponding task checklist item, then verified the task item encodes the SAME mechanism the research mandated (not a drifted alternative), and that no task item fabricates an action absent from research. Each checklist row below cites task line numbers and research line numbers.

---

## Alignment Checklist Results

### Item 1 — REG-1 cause 1 (Live redirect disarm) → Step 1.3

**Research:** research/01 §"Cause 1" (lines 14-31) mandates adding `redirect_stdout=False, redirect_stderr=False,` to the `Live(...)` constructor at `tui.py:221`. research-notes SUGGESTED_PHASES (line 53).

**Task:** Step 1.3 (task line 169) instructs: re-locate `self._live = Live(`, confirm no redirect args, then "use Edit to add `redirect_stdout=False,` and `redirect_stderr=False,` as additional keyword arguments to that single `Live(...)` constructor call". Preserves `screen=False` and other args verbatim; modifies only that one call.

**Verdict: ALIGNED.** Exact mechanism, exact file, exact kwargs, scoped to the single constructor. Faithful.

---

### Item 2 — REG-1 cause 2 silencing mechanism (class-attr `quiet`, NOT constructor kwarg) → Steps 1.4/1.5/1.6

**Research:** research/01 §"FROZEN-SIGNATURE CONSTRAINT" (lines 48-92) and research-notes GAPS_AND_QUESTIONS (line 39) are emphatic: silencing MUST be a **class-attribute default `quiet: bool = False`** + per-instance flip `executor.quiet = True` at dispatch.py + `if not self.quiet:` guards. A `quiet=` `__init__` kwarg WOULD break `test_frozen_signatures_unchanged` (which pins `__init__` params to EXACTLY `["self", "max_workers"]`).

**Task:**
- Step 1.4 (line 173): "add a class-level attribute `quiet: bool = False` to `ParallelExecutor` (placed at the top of the class body … as a class attribute — NOT as an `__init__` parameter and NOT assigned inside `__init__`), ensuring the `__init__` signature remains EXACTLY `def __init__(self, max_workers: int = 10):`". Explicitly forbids the constructor-kwarg drift.
- Step 1.5 (line 177): guard every `print(` in `plan()/execute()/_execute_group()` with `if not self.quiet:`; "NO unconditional `print(` remaining".
- Step 1.6 (line 181): "insert `executor.quiet = True`" at the dispatch call site, "regardless of whether `executor` was injected … or freshly constructed", "instance-attribute assignment, not a constructor change".

**Verdict: ALIGNED.** All three sub-items encode EXACTLY the class-attribute + guard + instance-flip mechanism. The constructor-kwarg anti-pattern is explicitly prohibited in 1.4. No drift. Faithful — this is the highest-risk drift point and the task got it right.

---

### Item 3 — DRIFT-3 reader guard → Step 2.1

**Research:** research/02 §DRIFT-3 (lines 39-58): wrap `read_state` + `_tail_events` in a guard scoped to `Exception` (or `(ValueError, OSError)`), keep last-good `state`/`events`, `continue` the loop, seed safe defaults before the loop, MUST NOT catch `BaseException`/`KeyboardInterrupt`, loop still reaches the `exc_box` re-raise. research-notes line 42.

**Task:** Step 2.1 (line 193): "wrap the two reader calls (`read_state` and `_tail_events`) in a defensive `try/except Exception:` that, on a reader exception, keeps the last-good `state`/`events`/`offset` snapshot bound and `continue`s the loop (seeding safe initial defaults BEFORE the loop …)", "scoped to `Exception` (or the specific `(ValueError, OSError)` reader set) and NEVER catches `BaseException`/`KeyboardInterrupt`", "the post-loop `exc_box` re-raise is still reached".

**Verdict: ALIGNED.** Every element present: wraps both readers, Exception-scoped, last-good seed, continue, pre-loop default seeding, KeyboardInterrupt still propagates, exc_box reachable. Faithful.

---

### Item 4 — DRIFT-4 precedence reorder → Step 2.2

**Research:** research/02 §DRIFT-4 (lines 60-72): place `if "e" in exc_box: raise exc_box["e"]` BEFORE `if interrupted: raise Exit(130)`; worker crash dominates concurrent interrupt; preserve original traceback; SIGINT-only still `Exit(130)`; FR-6 intact (stop+join in finally).

**Task:** Step 2.2 (line 197): "REORDER the two checks so the `exc_box` worker-crash re-raise is evaluated BEFORE the `interrupted` SIGINT exit — i.e. place `if "e" in exc_box: raise exc_box["e"]` ahead of `if interrupted: raise click.exceptions.Exit(130)`", "the SIGINT-only path … STILL surfaces as `Exit(130)`", "`tui.stop()`+`join()` … still run before either raise".

**Verdict: ALIGNED.** Exact reorder, original-traceback preservation, SIGINT-only invariant retained, FR-6 finally preserved. Faithful.

---

### Item 5 — DRIFT-2 audit extension → Steps 3.1/3.2

**Research:** research/03 §DRIFT-2 (lines 10-23): add stdout-write detector (`print(` Call nodes + `sys.stdout`/`sys.stderr` Attribute incl `.write`/`.flush`); guard-aware (option (a): flag only UNGUARDED writes; a print under `if not self.quiet:` is acceptable); keep existing import/name checks; MANDATORY vacuity guard preserved; mutation guard proving detector is not a no-op (synthetic `print('x')` + `sys.stdout.write('x')` MUST be flagged); preserve `_run_worker`-in-dispatch.py assertion.

**Task:**
- Step 3.1 (line 209): extend visitor to flag `print(...)` Call nodes + `sys.stdout`/`sys.stderr` Attribute (incl `.write`/`.flush`) "that are NOT guarded by a `self.quiet` conditional (per research file 03 option (a))", keep existing import/name checks, assert both worker surfaces have zero unguarded writes, "MANDATORY existing vacuity guard (≥1 module scanned) is preserved", "existing `_run_worker`-lives-in-dispatch.py assertion (around lines 690-695) is preserved", treats guarded prints as not-flagged.
- Step 3.2 (line 213): new `test_stdout_write_detector_is_not_a_noop` feeding synthetic source with unguarded `print('x')` + `sys.stdout.write('x')` asserting BOTH flagged, AND guarded versions NOT flagged; parses via `ast.parse`; self-contained; would FAIL if detector reverted to no-op.

**Verdict: ALIGNED.** Detector scope, guard-awareness (option a), vacuity guard, `_run_worker` assertion preservation, mutation guard (both positive AND negative cases) all present. Faithful — and Step 3.2 even adds the negative (guarded-not-flagged) case which research called for under guard-awareness.

---

### Item 6 — Real-PTY smoke → Step 3.3

**Research:** research/03 §"Real-PTY smoke" (lines 24-33): use `pty.openpty()` so `stream.isatty()` is True; run `swarm run --tui` (or drive `run_cmd` with slave as stdout); ensure worker emits stdout concurrently; assert no crash/`Traceback`/render-crash in master-fd output, terminal restored; `@pytest.mark.skipif(sys.platform == "win32" …)` (or `not hasattr(os, "openpty")`); deterministic & bounded (small worker count, `_TUI_POLL_MAX_ITERATIONS`, short timeout).

**Task:** Step 3.3 (line 217): new `test_tui_real_pty_no_crash_under_concurrent_worker_stdout` that "opens a real PTY (`pty.openpty()`)", runs `swarm run --tui`/drives `run_cmd` with PTY slave as stdout, "ensures the worker path actually emits stdout concurrently", "asserts the process completes with a non-crash exit and NO `Traceback`/render-crash text in the master-fd output with the terminal restored", guarded with `@pytest.mark.skipif(sys.platform == "win32" or not hasattr(os, "openpty"), …)`, "deterministic and bounded (small worker count, `_TUI_POLL_MAX_ITERATIONS` injection, short timeout)", "asserts on the ABSENCE of a crash rather than exact frame content".

**Verdict: ALIGNED.** Every design element — PTY mechanism, TTY seam, concurrent worker stdout, absence-of-crash assertion, win32+openpty skipif, bounded/deterministic — is faithfully encoded. Faithful.

---

### Item 7 — DRIFT-3 + DRIFT-4 regression tests → Steps 3.4/3.5

**Research:** research/02 lines 74-76 + research/03 §"FR-5 regression tests" (lines 35-39):
- DRIFT-3: monkeypatch `read_state` to raise `ValueError` once while `exc_box` holds a worker exception → assert the WORKER exception reaches the caller (not the ValueError, not a clean exit), terminal restored, `tui.stop()` ran. Would-fail-pre-fix / pass-post-fix.
- DRIFT-4: drive loop so `interrupted=True` AND `exc_box["e"]` set → assert worker exception surfaced/chained (NOT bare `Exit(130)`), original traceback preserved. Keep existing FR-6 SIGINT-only test green.

**Task:**
- Step 3.4 (line 221): `test_drift3_reader_error_does_not_mask_worker_crash` — drives loop so `read_state` raises `ValueError` once while a worker exception is seeded in `exc_box`, asserts worker exception propagates, "would FAIL against the pre-fix unguarded-reader code … and PASS against the Step 2.1 guard", verifies `tui.stop()` was called, does not hide FR-6.
- Step 3.5 (line 225): `test_drift4_sigint_does_not_mask_worker_crash` — seeds both `interrupted=True` and worker exception in `exc_box`, asserts worker exception (with original traceback) propagates rather than `Exit(130)`, "would FAIL against the pre-fix inverted precedence and PASS against the Step 2.2 reorder", leaves FR-6 SIGINT-only invariant to existing test.

**Verdict: ALIGNED.** Both regression tests match the research spec including the would-fail-pre-fix / pass-post-fix property, terminal-restoration check, and the explicit non-weakening of the existing FR-6 test. Faithful.

---

### Item 8 — Fabrication check (out-of-scope items NOTES-ONLY, not action items)

**Research:** research-notes AMBIGUITIES_FOR_USER (lines 65-67) explicitly scopes OUT: DRIFT-1 (eager `import TUI` at commands.py:1880) and NEC-1 (documented necessary deviation). DRIFT-2 is IN scope only folded into the FR-1 audit extension. Task fixes EXACTLY REG-1, DRIFT-3, DRIFT-4, DRIFT-2 audit hardening.

**Task scan for fabrication / scope-creep:**
- DRIFT-1 appears ONLY in: Key Constraints "Out of scope" (line 130), and the "Open Questions / Out-of-Scope Follow-Ups" section (line 317) — explicitly "NOT actioned here", recommended follow-up. NO checklist item (`- [ ]`) touches the commands.py:1880 eager import. CORRECT — notes-only.
- NEC-1 appears ONLY in line 130 + line 318 — "documented necessary deviation — no action". NO checklist item. CORRECT — notes-only.
- I scanned every `- [ ]` item (Steps 1.1–4.6). Every action item maps to one of: setup/handoff (1.1, 1.2), REG-1 (1.3–1.7), DRIFT-3/4 (2.1–2.3), DRIFT-2 audit + PTY + regressions (3.1–3.6), validation/completion/reflect (4.1–4.6). NONE references DRIFT-1's import, NEC-1, or any file/change absent from research. Source files touched (tui.py, parallel.py, dispatch.py, commands.py, state.py-as-context, test_inv012, test_run_tui_integration, test_tail_events) ALL appear in research-notes EXISTING_FILES (lines 18-25).

**Verdict: ALIGNED — NO FABRICATION.** DRIFT-1 and NEC-1 are correctly notes-only; no checklist item fabricates an out-of-scope or research-absent action.

---

### Item 9 — Frozen-signature constraint reflected in verification → Step 1.7

**Research:** research/01 lines 94-98 ("Acceptance evidence": `test_frozen_signatures_unchanged` still passes, `__init__` == `["self","max_workers"]"`). research-notes line 39 (load-bearing constraint).

**Task:** Step 1.7 (line 185): runs `uv run pytest tests/swarm/test_run_tui_integration.py::test_frozen_signatures_unchanged -v` to "confirm the Phase 1 edits … have NOT broken the frozen `ParallelExecutor.__init__(self, max_workers=10)` signature"; includes a remediation branch: "if the frozen-signature test FAILS, the silencing mechanism wrongly altered `__init__` — revert to the class-attribute approach from Step 1.4 and re-run". Also re-run in the full suite at Step 3.6 (line 229).

**Verdict: ALIGNED.** Frozen-signature is verified directly in Phase 1 AND swept again in the full suite, with an explicit corrective branch tied back to the class-attribute mechanism. Faithful.

---

### Item 10 — Validation surface (ruff check + ruff format --check SEPARATELY + full tests/swarm/) → Phase 4

**Research:** research/03 §"Validation surface" (lines 41-43): `uv run pytest tests/swarm/ -v` (full suite); `uv run ruff check src/ tests/` AND `uv run ruff format --check src/ tests/` (CI runs format --check SEPARATELY — green `make lint` ≠ green CI format). research-notes lines 56, 62.

**Task:**
- Step 3.6 (line 229): full `uv run pytest tests/swarm/ -v`.
- Step 4.1 (line 237): `uv run ruff check src/ tests/`.
- Step 4.2 (line 241): `uv run ruff format --check src/ tests/`, explicitly noting "CI runs `ruff format --check` separately, so a green `ruff check` alone is NOT sufficient".

**Verdict: ALIGNED.** All three validation surfaces present as SEPARATE steps; the format-check-is-separate nuance (and the project memory it derives from) is explicitly carried into Step 4.2. Faithful.

---

## Adversarial Deep Pass — Sub-Mechanism Gaps

The 10 headline mappings are all faithful. Per the adversarial mandate I drilled into research nuances that a one-shot builder commonly drops. The following are genuine, evidence-backed gaps where the task under-represents or omits a research-stated detail. None overturns the PASS, but each is a real degradation of the research's intent and should be acknowledged.

### GAP-1 (LOW severity) — Step 1.5/3.1 lose the research/03 caveat that gated `parallel.py` prints REMAIN `print(` calls, risking a self-contradicting audit

**Research:** research/03 lines 19-22 raises an explicit hazard: "After the fix, the gated `parallel.py` prints (`if not self.quiet:` guarded) are STILL `print(` calls in source, so the audit would flag them." It then resolves it via option (a): the detector must flag only an **UNGUARDED** print. This is the single most error-prone coupling in the whole task — the Phase 1 gating (1.5) and the Phase 3 detector (3.1) MUST agree on what "guarded" means or the suite is internally inconsistent (3.1 would flag the very prints 1.5 created).

**Task:** Step 3.1 (line 209) DOES encode option (a) and "treats prints reachable only via `if not self.quiet:` as guarded (not flagged)". GOOD. BUT: Step 1.5 (line 177) tells the executor to wrap prints in `if not self.quiet:` and says the gating must "exactly match the structural invariant the Phase 3 audit will assert" — WITHOUT stating the concrete guard-detection contract (that the audit recognizes specifically an `if not self.quiet:` test wrapper). The research's resolution depends on the guard SHAPE the detector recognizes. If the executor in 1.5 chooses a differently-shaped guard (e.g. `if self.quiet: return` early-exit at method top, or `if not self.quiet is True`) the 3.1 detector (which research/03 frames around an `if not self.quiet:` conditional) may not recognize it as guarded → 3.1 flags 1.5's prints → contradictory suite.

**Why this is a gap, not nitpick:** research/03 explicitly flagged this as THE coupling to resolve; the task split the two halves across Phase 1 and Phase 3 without pinning the shared guard-shape contract in BOTH steps. The hazard research called out can re-materialize from a guard-shape mismatch the task does not foreclose.

**Recommendation:** Add to Step 1.5 an explicit constraint that the guard MUST be a structural `if not self.quiet:` conditional wrapping the print(s) (the exact shape the Step 3.1 detector recognizes), and cross-reference 3.1's guard-detection contract. LOW because a careful executor reading both steps + research/03 will converge; but the task should not rely on that.

---

### GAP-2 (LOW severity) — research/01's "verify injected-executor tests don't assert on captured stdout" check is dropped

**Research:** research/01 line 90 carries a specific verification obligation: flipping `executor.quiet = True` on ANY instance dispatch receives means "The injected-executor test paths (`test_imm3_parallel.py`, `test_dispatch.py`) pass their own `ParallelExecutor`; if dispatch flips `.quiet=True` … those tests stay silent too (acceptable; they assert results, not stdout). **Verify they don't assert on captured stdout.**" This is an explicit research-mandated regression check on two named test files outside `tests/swarm/`.

**Task:** Step 1.6 (line 181) correctly instructs flipping quiet "regardless of whether `executor` was injected … or freshly constructed" — i.e. it ADOPTS the behavior research flagged as needing verification. But NO task item verifies that `test_imm3_parallel.py` / `test_dispatch.py` don't assert on captured stdout. Worse: the full-suite run in Step 3.6 is scoped to `tests/swarm/` only, and `test_imm3_parallel.py` / `test_dispatch.py` are NOT necessarily under `tests/swarm/` (they are referenced by bare filename in research, suggesting `tests/` or another subdir). The repo-wide ruff steps (4.1/4.2) lint them but do not RUN them.

**Why this is a gap:** The task deliberately silences injected executors (1.6) — the exact behavior research said requires verifying two specific test files don't break — yet provides no step that runs or inspects those files. If either asserts on captured stdout, the silencing introduces a regression that the `tests/swarm/`-scoped Step 3.6 would NOT catch.

**Recommendation:** Add a verification (read or run `test_imm3_parallel.py` + `test_dispatch.py`) confirming neither asserts on captured stdout, OR widen one validation run beyond `tests/swarm/` to cover the dispatch/parallel injected-executor tests. LOW because research itself judged the outcome "acceptable" and stdout assertions in those unit tests are unlikely — but the research explicitly asked to VERIFY, and the task does not.

---

### GAP-3 (LOW severity) — research/03's transitive / call-graph coverage limitation is silently dropped, not documented as the research directed

**Research:** research/03 line 17 (DRIFT-2 fix item 3) directs: "**(Transitive coverage)** At minimum, **document the per-file limitation** and assert the two known worker surfaces are clean; a full call-graph walk is optional…". research-notes line 23 reinforces that the existing audit is "per-file … NOT the transitive call graph FR-1's acceptance text demands ('any callable they invoke')". So research mandates a concrete deliverable: DOCUMENT the per-file limitation (even though the full walk is optional).

**Task:** Step 3.1 (line 209) implements the per-file stdout-write detector on the two known surfaces and preserves the `_run_worker`-in-dispatch.py assertion (so coverage "cannot silently move"). GOOD on the assertion. BUT the task NOWHERE instructs the executor to DOCUMENT the per-file (non-transitive) limitation — neither as a code comment in the audit test nor in a task-log note. The research's "at minimum, document the per-file limitation" sub-requirement has no corresponding task action.

**Why this is a gap:** This is a small but real dropped finding. research/03 framed FR-1's acceptance text ("any callable they invoke") as transitive, acknowledged the fix stays per-file, and required that the limitation be DOCUMENTED so a future reader knows the audit does not walk the call graph. The task delivers the narrowing (per-file detector) without the accompanying disclosure the research asked for — exactly the kind of finding-representation drop the adversarial lens targets.

**Recommendation:** Add to Step 3.1 an instruction to document the per-file (non-transitive) limitation as a comment in `test_worker_surfaces_have_zero_tui_reachability` (or its docstring), noting FR-1's "any callable they invoke" is approximated by the two known surfaces + the pinned `_run_worker` location. LOW (it is documentation, not behavior) but it is a literal research directive with zero task coverage.

---

## Summary of Gaps

| # | Severity | Research source | Gap | Task locus |
|---|----------|-----------------|-----|-----------|
| GAP-1 | LOW | research/03:19-22 | Guard-SHAPE contract not pinned in Step 1.5 to match Step 3.1 detector; risks self-contradicting audit | Steps 1.5 / 3.1 |
| GAP-2 | LOW | research/01:90 | "Verify `test_imm3_parallel.py`/`test_dispatch.py` don't assert on captured stdout" obligation dropped; not in `tests/swarm/` scope | Steps 1.6 / 3.6 |
| GAP-3 | LOW | research/03:17 | "Document the per-file (non-transitive) limitation" directive has no task action | Step 3.1 |

All three are LOW: each is a verification/documentation/contract-tightening omission, not a mechanism misrepresentation or fabrication. The four core deviations (REG-1, DRIFT-2, DRIFT-3, DRIFT-4), the frozen-signature constraint, the PTY smoke, and the validation surface are ALL faithfully and precisely encoded with no constructor-kwarg drift and no out-of-scope fabrication.

---

## VERDICT: PASS

**Rationale:** All 10 alignment checklist items map faithfully from research to task with the correct mechanisms. The highest-risk drift point (Item 2 — class-attribute `quiet` vs forbidden `__init__` kwarg) is encoded exactly per research, with the constructor-kwarg anti-pattern explicitly prohibited and double-verified (Steps 1.4 + 1.7 + 3.6). No checklist item fabricates an action absent from research; DRIFT-1 and NEC-1 are correctly notes-only. The three gaps found under the adversarial deep pass are all LOW-severity verification/documentation omissions of research sub-requirements — they degrade completeness slightly but do not misrepresent or contradict any research finding, and none blocks execution.

**Issues (all LOW, none blocking):**
- GAP-1 (LOW): pin the `if not self.quiet:` guard-shape contract in Step 1.5 to match the Step 3.1 detector.
- GAP-2 (LOW): add a verification that `test_imm3_parallel.py`/`test_dispatch.py` don't assert on captured stdout (research/01:90 obligation), since they fall outside the `tests/swarm/` run scope.
- GAP-3 (LOW): add a Step 3.1 instruction to document the per-file (non-transitive) audit limitation per research/03:17.

**Recommendation:** PASS as-is is defensible (gaps are LOW and the executor reading both the steps and the linked research will likely cover GAP-1 and GAP-2 organically). If a hardening pass is cheap, fold the three LOW recommendations into Steps 1.5, 1.6/3.6, and 3.1 respectively before execution.
