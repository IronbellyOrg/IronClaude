# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** swarm --tui FR-1 regression remediation (REG-1 / DRIFT-2/3/4)
**Date:** 2026-06-19
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

Verifying every checklist item in the task file is SELF-CONTAINED per MDTM B2
(context + action + output + verification + completion gate), with the code-task
self-containment concerns layered on top (frozen-signature naming, Exception-scoped
guards, verbatim POST-reflect wrapper command, line-number resilience).

Findings appended incrementally below.

---

## Ground-Truth Verification (anchors the line-resilience checks)

Every search anchor that the items instruct the executor to re-locate by was
verified to exist in the live (uncommitted) tree:

| Anchor cited by item | Live location | Match |
|---|---|---|
| `self._live = Live(` (Step 1.3) | tui.py:221 | EXACT |
| `class ParallelExecutor` (Step 1.4) | parallel.py:80 | EXACT |
| `def __init__(self, max_workers` (Step 1.4) | parallel.py:100 | EXACT |
| `print(` in plan/execute/_execute_group (Step 1.5) | parallel.py 110,111,164,165,176,177,183,191,196-200,225,232 | EXACT (matches item enumeration verbatim) |
| `ParallelExecutor(max_workers=workers_requested)` (Step 1.6) | dispatch.py:424 | EXACT |
| `while True:`+`read_state(` poll loop (Step 2.1) | commands.py:1943-1945 | EXACT |
| readers OUTSIDE try/except (DRIFT-3 claim) | readers at 1944-1946 precede `try: tui_obj.update` at 1956-1957 | CONFIRMED |
| Exit(130) before exc_box re-raise (DRIFT-4 claim) | `if interrupted`→Exit(130) at 1989-1990 BEFORE `if "e" in exc_box`→raise at 1990-1991 | CONFIRMED inverted |
| `def read_state` raising (state.py) | state.py:178 | EXACT |
| `_TuiSymbolVisitor` / `test_worker_surfaces_have_zero_tui_reachability` | test_inv012_tui_opt_in.py:600 / 655 | EXACT |
| vacuity guard `scanned`/`>=1` | test_inv012_tui_opt_in.py:670,676 + comment 661 | CONFIRMED |
| `_run_worker` lives-in-dispatch assertion | test_inv012_tui_opt_in.py:691 | CONFIRMED |
| `should_enable_tui` / `_TUI_POLL_MAX_ITERATIONS` seams | test_run_tui_integration.py:193,559 | CONFIRMED |
| `test_frozen_signatures_unchanged` | test_run_tui_integration.py:622 | EXACT |
| DRIFT-1 eager import (out-of-scope note) | commands.py:1880 | EXACT |
| tui.py stop idempotent (NEC-1 note "tui.py:230-234") | stop() at 230, guard 232-234 | EXACT |
| Research/spec/deviation-register inputs | all present on disk | CONFIRMED |
| `superclaude reflect` binary (Step 4.5) | /config/.local/bin/superclaude | PRESENT |

Conclusion: the line-number-resilience self-containment requirement is SATISFIED —
every item that cites an approximate line ALSO supplies an exact search string, and
every search string resolves uniquely in the live tree.

---

## Items Reviewed (B2 7-point + code-task concerns)

| # | Item | Result | Evidence |
|---|------|--------|----------|
| 1.1 | Status → Doing + log | PASS | Context (frontmatter+log section), action, output, completion gate, exact format string. Self-contained. |
| 1.2 | Create handoff dirs | PASS | Exact absolute path + both subdirs named + fallback. Measurable. |
| 1.3 | Disarm Live redirect | PASS | Exact file + constructor + kwargs + invariant (only that call, screen=False verbatim, no other Live() touched) + re-locate-by-search. |
| 1.4 | quiet class-attr default | PASS | Restates FROZEN-SIGNATURE invariant inline, exact attribute + placement + "NOT an __init__ param". |
| 1.5 | Guard prints `if not self.quiet:` | PASS | Enumerates print lines AND Grep re-location; post-condition stated; module-level prints scoped OUT. Matches live code. |
| 1.6 | Flip executor.quiet=True | PASS | Exact call site + line to insert + invariant (injected OR fresh; no constructor change). |
| 1.7 | Phase 1 validation | PASS | Three exact commands, exact output path, measurable criteria, remediation branch. |
| 2.1 | DRIFT-3 reader guard | PASS (note I-1) | Restates masking mechanism, names readers, Exception-scope + FR-6 restated, last-good-seed instruction. |
| 2.2 | DRIFT-4 precedence reorder | PASS | Restates inverted precedence, exact reorder, FR-6 SIGINT-only + finally-ordering preserved. |
| 2.3 | Phase 2 validation | PASS | Two exact commands, exact append path, remediation branch. |
| 3.1 | Extend AST audit | PASS | Restates DRIFT-2, names visitor methods, exact detection rule, preserves vacuity + _run_worker, guard-awareness rule. |
| 3.2 | Mutation guard | PASS | Exact new-test name, synthetic source, positive+negative assertions, "would FAIL if reverted". |
| 3.3 | Real-PTY smoke | PASS (note I-2) | PTY rationale restated, exact skipif guard, boundedness, assert-on-absence-of-crash. |
| 3.4 | DRIFT-3 regression test | PASS (note I-3) | Restates spec, monkeypatch read_state→ValueError w/ exc_box seeded, FAIL-pre/PASS-post, tui.stop assertion. |
| 3.5 | DRIFT-4 regression test | PASS (note I-3) | Restates spec, seed interrupted+exc_box, assert worker exc not Exit(130), keeps FR-6 test green. |
| 3.6 | Full swarm suite | PASS | Exact command, two output paths, structured-summary contract, no-fabrication, fix-and-rerun loop, PTY pass-or-skip rule. |
| 4.1 | Repo-wide ruff check | PASS | Exact command, output path, success criterion, --fix remediation. |
| 4.2 | Repo-wide ruff format check | PASS | Exact command, output path, CI-parity rationale, remediation. |
| 4.3 | Verify outputs + items checked | PASS | Enumerates expected files, checks all [ ]→[x], logs gaps. |
| 4.4 | Task Summary | PASS | Points to in-file template, enumerates required content, no-fabrication rule. |
| 4.5 | POST reflect gate | PASS (note I-4) | VERBATIM flat wrapper command, recursion-breaker env guard, exit-code handling (0 vs 10/11/2), report path, "no --base/range" constraints, benign-exit-11 note. |
| 4.6 | Status → Done | PASS | Conditional on 4.5 (Done only if exit 0 or resolved; else Blocked+reason), exact log format. Honest gate. |

---

## B2 7-Point Checklist Verdict

1. All 5 B2 components present per item: PASS.
2. No item references prior context without restating: PASS — 1.4/1.5/2.1/2.2/3.1 restate the frozen-signature / FR-5 / FR-6 / DRIFT invariants inline rather than only pointing at research.
3. No vague "see SKILL.md / use the standard prompt": PASS — no agent fan-out; items point at research files only as READ inputs (exact absolute paths), never as a substitute for the embedded action.
4. File paths specific: PASS.
5. Verification measurable: PASS.
6. No batch items: PASS — 1.5 is a single contiguous-surface edit scoped to 3 named methods in one file (atomic unit, not cross-file batch).
7. No items on [CODE-CONTRADICTED]/[UNVERIFIED] findings: PASS — research 01 is [CODE-VERIFIED]; I independently re-verified every cited code location.

---

## Issues Found

Adversarial review surfaced the following self-containment soft-spots. NONE rises to a
B2 FAIL (every item still carries all 5 components and can be executed without scrolling
to another item), but they are real weaknesses an executor could trip on. Documented per
the no-leniency standard. fix_authorization=false → report-only, no edits applied.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| I-1 | MINOR | Step 2.1 (DRIFT-3) | The item instructs to "seed safe initial defaults BEFORE the loop … bind `state`/`events` to a last-good default" but does NOT restate the concrete pre-loop seam. Live code initializes `offset = 0` INSIDE the `try:` (commands.py:1948) and binds `state`/`events` only on the first loop iteration — there is no existing pre-loop `state`/`events` binding to reuse. The executor must invent the seed location; the item leaves the exact insertion point self-defined rather than self-contained. | Add an explicit clause naming where the pre-loop seed goes (e.g. "bind `state = None; events = []` immediately after `offset = 0` is hoisted above the `while True:`"), so the executor does not have to design the seam. Borderline against B2 component 4 (specificity of the change locus). |
| I-2 | MINOR | Step 3.3 (PTY smoke) | The item offers an "or" disjunction — "runs `swarm run --tui` (or drives `run_cmd` with the PTY slave as stdout)" — leaving the executor to choose the harness. The existing suite drives via `CliRunner().invoke(run_cmd, …)` (non-TTY) which the item itself says CANNOT reproduce the race, so the real choice (subprocess under a PTY vs in-process fd swap) is non-trivial and is NOT resolved by the item. Self-contained in intent, under-specified in mechanism. | Pick ONE harness and state it (research 03 should pin which). A two-way "or" inside a single atomic test item is a measurable-mechanism gap, though the absence-of-crash assertion remains testable either way. |
| I-3 | IMPORTANT | Steps 3.4 + 3.5 (DRIFT-3/4 regression tests) | Both items hinge on driving the poll loop so that `exc_box` holds a worker exception AND (3.5) `interrupted=True`. But `exc_box`, `interrupted`, and `result_box` are LOCAL variables inside `run_cmd` (commands.py:1901-1902, 1925) — there is NO injection seam, and the existing harness only reaches them indirectly via a monkeypatched `dispatch_wave1` that raises (seeds `exc_box`) plus a monkeypatched `read_state` (3.4) or a SIGINT-raising stream (3.5, to set `interrupted`). The items DO provide an escape hatch ("if unable … due to the harness not exposing an `exc_box`/`read_state` seam, log the blocker") — which keeps them B2-legal — but they describe the seed as if direct injection were available. An executor could waste a cycle hunting for a non-existent seam before falling back. The DRIFT-4 item in particular ("seed both `interrupted=True` and a worker exception") understates that `interrupted` can only be set by raising `KeyboardInterrupt` out of the render loop, which requires a monkeypatch that raises it from inside `tui_obj.update` or `read_state` — a non-obvious mechanism the item leaves to the executor. | Restate the concrete seeding mechanism inline: 3.4 → "monkeypatch `commands.read_state` to raise `ValueError` on the Nth call AND monkeypatch `dispatch_wave1` to raise the sentinel worker exception (which `_dispatch_worker` captures into `exc_box`)". 3.5 → "monkeypatch a poll-loop reader to raise `KeyboardInterrupt` (sets `interrupted` via the `except KeyboardInterrupt` at commands.py:1981) while `dispatch_wave1` raises the worker sentinel". This converts the items from intent-complete to mechanism-complete and removes the wasted-cycle risk. |
| I-4 | MINOR | Step 4.5 (POST reflect) | The item says non-zero exits "10, 11, or 2" are FAIL/degraded and must be surfaced, but the verbatim command uses `--fix --promote`. With `--fix` the wrapper may remediate and re-converge to exit 0 on its own; the item does not state whether a `--fix`-driven mutation to the tree (after the executor already wrote the Task Summary in 4.4) should re-trigger any earlier validation. Not a self-containment defect of the item itself (the command + exit-code handling are fully embedded), but the interaction with 4.4 ordering is unstated. | Add a one-line note: "if `--fix` modifies tracked source, re-run Step 4.1/4.2 ruff gates before 4.6." Optional hardening, not a B2 violation. |

### Why none of these is a B2 FAIL

- Each flagged item still contains all five B2 components and is executable as a standalone paragraph.
- I-1/I-2/I-4 are mechanism-precision gaps, not missing-context gaps — the executor is told WHAT and WHY, only the exact HOW-seam is left partly open.
- I-3 is the strongest finding (rated IMPORTANT) because two items share an under-described seam, but both carry an explicit blocker-logging escape hatch, so they cannot silently strand the executor — they degrade gracefully.

---

## Code-Task-Specific Self-Containment Checks

| Concern | Result | Evidence |
|---|--------|----------|
| Frozen `ParallelExecutor.__init__(self, max_workers=10)` named + protected per edit item | PASS | Steps 1.4/1.6/1.7 each restate "do NOT add a `quiet=` kwarg / NOT touch the constructor"; 1.7 re-runs `test_frozen_signatures_unchanged` as the gate. |
| Exception-scoped guards so KeyboardInterrupt propagates (FR-6) | PASS | Steps 2.1/2.2 explicitly require `Exception`/`(ValueError, OSError)` scoping and forbid `BaseException`; matches live code's `except KeyboardInterrupt` at commands.py:1981 staying intact. |
| POST reflect (4.5) carries full verbatim wrapper command + recursion-breaker + exit handling | PASS | `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` probe, verbatim `superclaude reflect run … --depth deep --fix --promote`, FLAT-form constraints, exit-code branch all embedded. |
| Line-number references resilient (re-locate by search) | PASS | Every line-citing item pairs the number with an exact search string; all strings resolve uniquely in the live tree (see Ground-Truth table). |

---

## Confidence Gate

- VERIFIED: 22/22 checklist items categorized with tool evidence (every anchor Grep/Read-confirmed against the live tree).
- UNVERIFIABLE: 0
- UNCHECKED: 0
- **Confidence:** Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 5 (multi-anchor grep batches) | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
  - Note: B2 self-containment is intrinsically a local-source verification; no external lookup was required, so Tavily-first did not apply.

---

## Summary

- Checks passed: 22 / 22 items pass the B2 5-component gate.
- B2 7-point checklist: 7/7 PASS.
- Code-task-specific concerns: 4/4 PASS.
- Issues found: 4 (IMPORTANT: 1 [I-3], MINOR: 3 [I-1, I-2, I-4]).
- Issues fixed in-place: 0 (fix_authorization=false — report-only).

All four findings are mechanism-precision soft-spots, not missing-context failures. Every
flagged item carries the explicit blocker-logging escape hatch, so none can silently
strand the executor. The task file is well-formed for B2 self-containment and the
line-number-resilience requirement is fully satisfied. The findings are recommendations
to harden the regression-test seam descriptions (I-3 most worthwhile) before execution.

## Overall Verdict: PASS

The B2 self-containment lens passes: every checklist item is independently executable with
all five components embedded, no item defers to external prompts, all file paths and search
anchors are exact and live-verified, and the frozen-signature / Exception-scope / verbatim-
wrapper code-task invariants are restated per item. The 4 issues are IMPORTANT/MINOR
hardening recommendations, not B2 violations.

## QA Complete
