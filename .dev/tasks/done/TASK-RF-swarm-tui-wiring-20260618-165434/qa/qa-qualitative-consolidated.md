# A.10.5 Qualitative Validation — Consolidated Findings (for single fix agent)

Source: `qa-qualitative-operational-report.md` (PASS, 3 MINOR fold-ins), `qa-qualitative-sufficiency-report.md` (FAIL, 2 IMPORTANT + 1 MINOR). Apply ALL fixes below — additive test-item / clarification edits only, NO structural rework. Preserve the 30-item structure, frontmatter, penultimate POST reflect gate, and every already-correct item.

## FIX-Q1 (IMPORTANT) — FR-4 corrupt-COMPLETE-line behavior unspecified + untested
Step 2.4 (`_tail_events`) implements TWO disciplines: (a) buffer a newline-less PARTIAL trailing line, and (b) tolerate `from_json` JSONDecodeError. But the behavior on a newline-TERMINATED-but-malformed JSON line is under-specified, and Step 3.3 tests only the partial-line branch.
FIX:
1. In Step 2.4, specify the semantics precisely: the byte offset advances past every COMPLETE (newline-terminated) line REGARDLESS of whether `from_json` succeeds — a malformed complete line is SKIPPED (logged/ignored) and the offset advances past it, so it is never re-parsed (no infinite reparse / no permanent stall). The "do NOT advance / buffer for next poll" rule applies ONLY to a newline-less PARTIAL trailing line. State this as explicit action+verification text.
2. In Step 3.3 (FR-4 `_tail_events` test in `tests/swarm/test_tail_events.py`), add a sub-assertion: feed a file containing a complete malformed JSON line followed by valid lines; assert `_tail_events` skips the malformed complete line, advances past it (offset moves), delivers the subsequent valid events exactly once, and does NOT stall/re-deliver. This is distinct from the partial-trailing-line case already covered.

## FIX-Q2 (IMPORTANT) — FR-4 iteration-ceiling backstop unverified
The `watch_max_iterations`-style ceiling is the only guard against a hung/never-joining worker hanging the CLI, but no test asserts it bounds the loop.
FIX:
1. In the threaded-poll-glue item (2.5), make the iteration ceiling CONCRETE (not "optional"): the poll loop carries a `max_iterations` bound (mirror `watch_max_iterations` from `swarm status --watch`, commands.py ~2533-2540/2583-2613) that, when exceeded, breaks the loop (the subsequent `join()` still runs so the worker completes and logs flush — the ceiling guards only the RENDER spin, never truncates the non-daemon worker). State the default + the break condition.
2. Add a verifying test (in `tests/swarm/test_run_tui_integration.py`): drive the poll path with a worker that stays alive longer than the ceiling (or a small injected ceiling) and assert the loop exits at the ceiling without hanging, then `join()` completes normally. Anti-spin guard is now verified, not just implemented.

## FIX-Q3 (MINOR) — FR-6 SIGINT exit-code assertion too loose
The FR-6 SIGINT sub-assertion currently checks only "non-zero ≠ EXIT_OK". The spec FR-6 wants "an exit code reflecting interruption" and research G3 fixed this at 130 (Click's KeyboardInterrupt convention).
FIX: tighten the FR-6 teardown test (Step 3.6) SIGINT branch to assert the exit code is specifically 130 (or whatever the G3-documented value is), not merely non-zero. Keep the clean/exception branches as-is.

## FIX-Q4 (MINOR, operational R1) — make `worker_results` re-bind explicit in 2.5
The post-dispatch continuation (commands.py ~1826/1910) reads `worker_results`. In the threaded design the dispatch return lands in the result-box, so Step 2.5 MUST state verbatim that after `join()` + the after-stop re-raise, `worker_results` is re-bound from the result-box (e.g. `worker_results = result_box["v"]`) so the downstream normalize_wave2/reduce_wave3 continuation is unchanged. Add this explicit instruction to Step 2.5's action + a verification clause.

## FIX-Q5 (MINOR, operational R2) — pin `.values()` iteration for `_project_workers`
`_project_workers(events)` returns `dict[int, WorkerSnapshot]` (tui.py:145). The "≥1 non-vacuous worker row" assertions in the FR-7 and FR-4 test items must iterate `_project_workers(...).values()` and assert at least one snapshot has `status != "pending"` (non-vacuous). Pin this exact shape in the FR-7 (3.7) and FR-4 (3.3) test items so the assertion is written correctly.

## NON-ISSUES (no action)
- A.10.25 F2 (state=None first-frame): NOT a hole — `_build_header` has a `"-"` fallback (tui.py:277-278, CODE-VERIFIED) and the path is exercised transitively by the FR-7 real run. Do NOT add a redundant test (operational + sufficiency lenses agree).
- QA_GATE_REQUIREMENTS: NONE — correctly NOT flagged by either lens (code task; verification = tests + ruff + POST reflect).
- All FR implementing+verifying items, frozen-signature double-proof, validation ordering, POST reflect exit-0 backstop — verified clean.

After applying FIX-Q1..FIX-Q5: re-confirm item count, that the FR-4 test item now covers BOTH partial-line AND corrupt-complete-line, the iteration-ceiling has an implementing AND verifying item, the FR-6 SIGINT asserts 130, Step 2.5 re-binds worker_results, and 3.3/3.7 use `.values()`.
