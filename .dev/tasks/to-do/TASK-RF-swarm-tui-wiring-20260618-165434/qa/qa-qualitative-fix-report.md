# A.10.5 Qualitative Findings — Fix Report (single serialized fix agent)

**Date:** 2026-06-18
**Task file:** `TASK-RF-swarm-tui-wiring-20260618-165434.md`
**Authorization:** `fix_authorization: true` — applied in-place (additive test/clarification edits only)
**Constraints honored:** No phase restructuring, frontmatter untouched, POST reflect gate kept penultimate, no `state=None` redundant test added (A.10.25 F2 confirmed non-issue), B2 self-containment preserved on every touched item.

---

## Fixes Applied

### FIX-Q1 (IMPORTANT) — FR-4 corrupt-COMPLETE-line behavior specified + tested
- **Step 2.4 action** (`_tail_events`): replaced the under-specified "tolerate JSONDecodeError by NOT advancing (treat as still-partial)" clause with a PRECISE two-discipline rule: (i) the byte offset ADVANCES past EVERY COMPLETE (newline-terminated) line even if `from_json` raises — a malformed COMPLETE line is SKIPPED and the offset advances past it (no infinite reparse / no stall); (ii) the buffer-and-do-not-advance rule applies ONLY to a newline-LESS PARTIAL trailing line. Verification clause updated to match.
- **Step 3.3 test** (`tests/swarm/test_tail_events.py`): added a SECOND distinct sub-assertion (corrupt-complete-line case) — a complete-but-malformed `{not valid json}\n` followed by valid records; asserts skip + offset-advance-past + subsequent valid events delivered exactly once + no stall on a follow-up no-new-bytes call. Distinct from the pre-existing partial-trailing-line case.

### FIX-Q2 (IMPORTANT) — FR-4 iteration-ceiling made concrete + verified
- **Step 2.5 action**: the render-loop ceiling changed from "optional `watch_max_iterations`-style ceiling for test determinism" to a CONCRETE `max_iterations` bound mirroring `watch_max_iterations` (commands.py ~2533-2540 / ~2583-2613, `iterations >= max_iterations: break`) that breaks the RENDER loop while the subsequent `join()` still runs the non-daemon worker to completion (ceiling never truncates the worker). Default + break condition specified. Verification clause updated.
- **NEW Step 3.7b** (verifying test, `tests/swarm/test_run_tui_integration.py`): drives the `--tui` poll path with a worker that outlives the ceiling (or an injected small ceiling); asserts (a) the loop exits at the ceiling WITHOUT hanging, (b) `join()` then completes normally (worker not truncated). Capture → `fr4-ceiling.txt`. This is a self-contained additive test item (not folded into 3.7) to preserve single-purpose B2 self-containment.

### FIX-Q3 (MINOR) — FR-6 SIGINT asserts exit 130
- **Step 3.6 (c) SIGINT branch**: tightened from "non-zero, distinct from `EXIT_OK`" to `result.exit_code == 130` (the G3-documented SIGINT value = 128+2, per `06-gapfill.md` G3). CLEAN and EXCEPTION branches left unchanged.

### FIX-Q4 (MINOR, operational R1) — explicit `worker_results` re-bind in Step 2.5
- **Step 2.5 clause (d)**: added verbatim instruction that after `join()` + the post-stop re-raise (when no exception captured), the main thread re-binds `worker_results = result_box["v"]` so the downstream `normalize_wave2`/`reduce_wave3` continuation (commands.py ~1827-1829) and the `len(worker_results)` success line (~1910) are byte-unchanged. Matching verification clause added.

### FIX-Q5 (MINOR, operational R2) — `.values()` iteration pinned for `_project_workers`
- **Step 3.3 (FR-4)** and **Step 3.7 (FR-7)**: both non-vacuous-row assertions now pin iteration to `_project_workers(records).values()` and assert ≥1 `WorkerSnapshot` has `status != "pending"` (per `_project_workers -> dict[int, WorkerSnapshot]`, tui.py:145). Verification clauses in both items updated.

---

## Resulting State

- **Checklist item count:** 31 (was 30; +1 = new Step 3.7b iteration-ceiling verifying test — the only structural change, an additive test item).
- **Phase structure:** unchanged. Phase 1 (1.1–1.3) → Phase 2 (2.1–2.6) → Phase 3 (3.1, 3.1b, 3.2–3.7, **3.7b**, 3.8) → Phase 4 (4.1–4.4) → Post-Completion. No phases moved; frontmatter untouched.
- **New deliverable wired:** `fr4-ceiling.txt` added to the Post-Completion deliverables verification list.

## Required Confirmations

- **(a) FR-4 test now covers partial-line AND corrupt-complete-line:** CONFIRMED — Step 3.3 retains the partial-trailing-line/exactly-once assertions and adds a distinct corrupt-COMPLETE-line skip+advance+no-stall sub-assertion.
- **(b) Iteration-ceiling has implementing + verifying items:** CONFIRMED — implementing in Step 2.5 (concrete `max_iterations`, not optional); verifying in new Step 3.7b (loop exits at ceiling without hang, `join()` completes).
- **(c) FR-6 SIGINT asserts 130:** CONFIRMED — Step 3.6 (c) asserts `result.exit_code == 130`.
- **(d) POST reflect gate still penultimate:** CONFIRMED — the reflect-gate item is the second-to-last checklist item, followed only by the final status→Done item.

## Verification Method

Source facts independently re-verified before editing (no fabricated citations):
- G3 exit-130 value: `research/06-gapfill.md` G3 (SIGINT = 128+2; `EXIT_OK = 0` @ commands.py:188).
- `_tail_events(path: Path, offset: int) -> tuple[list[EventRecord], int]`: `06-gapfill.md` G6.
- `watch_max_iterations` break precedent: read commands.py ~2533-2613 (`iterations += 1; if ... >= ...: break`).
- `_project_workers(events) -> dict[int, WorkerSnapshot]`: read tui.py:145-164 (`.values()` yields `WorkerSnapshot` with `status`).
- `worker_results` continuation: read commands.py ~1826-1829 (`normalize_wave2`/`reduce_wave3`) and ~1910 (`len(worker_results)` success line).

Post-edit structure (item count, step headers, reflect-gate penultimacy, deliverables list) re-verified via grep.
