# QA Report: domain accuracy lens (R3-B3, list-incomplete cases)

**Topic:** the three FR-010 list-incomplete cases (Orca unavailable, worker list truncated, worker list call failed) in `docs/designs/orchestrator-mode.md` after items 4.1 to 4.5
**Phase:** doc-qualitative, domain-accuracy lens (research/09 Gap 5)
**fix_authorization:** false (only this report was written)
**Question asked:** are the three cases the only ways the scoped worker list can be incomplete for a read-only sweep that never follows `page.nextCursor`? Find a fourth case the text mishandles.

## Summary

The three cases are NOT the only ways. I found one BLOCKING fourth case (an unknown Run id), one MAJOR fifth case (a scoped Run whose `worker-list` is never attempted), and three MINOR notes. The R3-B3 edits themselves are faithful to SPEC FR-010 and internally consistent (C1 to C4, C10, C11 pass). The defects are gaps in what the three-case rule covers, and one false premise carried from the SPEC into the design.

I made six read-only calls to the live Orca (`orca orchestration worker-list` four times, `task-list` twice) plus one `--help`. They changed nothing. Their output is quoted in F1 and F3 as evidence.

## Findings

### F1 (BLOCKING): an unknown Run id is not an error in `worker-list`; it is a complete, empty list

**Evidence (live, read-only, this checkout's Orca runtime):**

- `orca orchestration worker-list --run run_does_not_exist_zz --json` returns exit 0 with `"ok": true`, `"workers": []`, `"counts": {}`, and `"page": {"limit": 100, "total": 0, "hasMore": false, "nextCursor": null}`. No error object.
- `orca orchestration task-list --run run_does_not_exist_zz --json` and the `--ready` form both return `"ok": false` with `"error": {"code": "run_not_found", ...}`.

**What the design says:**

- DESIGN `:245` (sequence diagram): "unknown-Run shape: call_failed for R, next Run" on the `worker-list` call.
- DESIGN `:896` (capture item 8) and `:979` (open item 4): the unknown-Run case is an error shape; until captured, "any nonzero `worker-list` exit on call one is `unavailable`".
- DESIGN `:972`: "The design names the safe behaviour that holds until it is closed."
- SPEC FR-002 (`merged-requirements.md:96`): a nonzero exit matching the unknown-Run shape is `call_failed (unknown run)`.
- DESIGN `:501` (the new R3-B3 bullet) fires only on `orca_available` False, `truncated` True, or a `worker-list` `call_failed`.

**What is wrong:** none of those fires for an unknown Run. `worker-list` returns a clean empty page, so `orca_available` stays True, `truncated` stays False, and the `orca worker-list <run>` source row has no `unscanned`. The list counts as complete. The guard holds. Every unjoined transcript with no tab-map entry then becomes `person_started` True (path A), and under path B with zero rows the fourth guard case (`:502`, "at least one scoped Dispatch row exists") does not apply either. A mistyped Run id, or a Run id from another Orca runtime, therefore reports workers' transcripts as person-started sessions. That is the exact false-negative join FR-010 forbids ("Only when every scoped Run's worker list is complete"), and the "safe behaviour until closed" claim at `:972` is false for this input. The design's only `run_not_found` signal is the `task-list` call, and no rule reads it.

**Smallest fix:**
1. In 7.2, add a fourth trigger to the `:501` bullet: a scoped Run whose `worker-list` returned zero rows and whose `task-list --run <run>` result is `call_failed`. Give it a fourth note, `origin unknown: Run not confirmed`, placed after the other three in the note order.
2. Add one fixture to `test_classify.py`, `test_fr010_unknown_run_empty_list_unknown` (`--run BAD`, `worker-list` ok with zero rows, `task-list` `call_failed`, T older than the window: T None, could not determine, not Historical). Add the same input to `test_fr010_incomplete_notes_order`.
3. Reword `:245`, `:896`, `:979` and the research/04 4.3 fixture 3 ("a nonzero exit on call one is `unavailable`") to say the unknown-Run signal is a zero-row `worker-list` plus a `run_not_found` `task-list`. Record this as a reword of open item 4, not a new deviation, so the totals stay 9 and 23.

### F2 (MAJOR): a scoped Run whose `worker-list` is never attempted is not covered

**Evidence:** DESIGN `:501` triggers on a `worker-list` "result" that is `call_failed`, "its `sources` row `orca worker-list <run>` has `unscanned` set". DESIGN `:595` says "Each scoped Run's `worker-list` call has its own source row", and a `call_failed` result sets `unscanned`. DESIGN `:349` covers only "the remaining rows" cut by the budget, which keep their identity. The Budget defaults are `total_s=90.0`, `per_call_s=10.0` (`:367`), and `call_timeout()` returns None below 1 s left (`:371`). The sequence at `:244-249` is labelled "per Run" and does not say whether every Run's `worker-list` runs before any `worker-show`.

**What is wrong:** with two or more Runs, R1's `task-list` and `worker-show` calls can use up the 90 s budget (a slow `worker-show` costs up to 10 s each, 25 per Run) before R2's `worker-list` is reached. R2 then has no result and possibly no source row, so no rule marks the list incomplete. A transcript of an R2 worker is unjoined and can become True. The `:287` rule ("a budget-cut timeout is `call_failed`") covers a call that started and timed out, not one never started. The exhausted-budget case also differs from the `:250-251` "later unavailable" path, which does set `orca_available` False.

**Smallest fix:** state in 7.2 `:501` and 7.4 `:595` that every Run in `ctx.runs` has a source row `orca worker-list <run>`, and that a Run never reached because of the budget carries `unscanned: time budget reached (90 s)` and counts as `call_failed` for this rule. Add one fixture: two Runs, budget exhausted before R2's `worker-list`, T None with `origin unknown: worker list call failed`.

### F3 (MINOR): truncation is detected by row count only; the live page has a direct flag

**Evidence:** DESIGN `:548` ("a full page sets truncated"), `:501` ("a full page of `WORKER_LIST_PAGE` rows"), `:980` (open item 5). The live page object carries `limit`, `total`, `hasMore` and `nextCursor` (observed: `limit` 100 by default, `total` 27, `hasMore` false for a real Run; `limit` 1, `total` 319, `hasMore` true when forced short). `grep` finds no `hasMore` or `page.total` anywhere in the DESIGN or SPEC.

**What is wrong:** a Run with exactly 100 Dispatches gives `hasMore` false but is treated as truncated, which hides every unjoined transcript as None (conservative, but wrong). The reverse case, a short page with `hasMore` true, would be missed. Nothing contradicts the SPEC, which itself defines the case as a "full page".

**Smallest fix:** set `truncated` when `page.hasMore` is true, or when the page holds `WORKER_LIST_PAGE` rows and `hasMore` is absent. Reading the flag does not follow the cursor. Update the capture-item 3 and open-item 5 text; the live shape is now known.

### F4 (MINOR): a worker started after the list was read looks unjoined

**Evidence:** Orca reads come first and disk reads last (`:244-260`). `collected_start` is read before the first Orca call (`:470`), and `first_record_ts` is already in `TranscriptTail` (`:459`). Neither is compared in a list-incomplete rule.

**What is wrong:** a Dispatch created during the sweep has a transcript but no list row, so it can be True (shown as `person session (active)` with the `origin not proved` note). The sweep is a snapshot, the effect lasts one sweep, and nothing is destroyed, so I grade it a note, not a blocker.

**Smallest fix:** an unjoined transcript whose `first_record_ts` is at or after `collected_start` gets None with `origin unknown: started after the worker list was read`.

### F5 (MINOR): the zero-row Run that really exists is correct but unstated

**Evidence:** a real Run with no Dispatch rows gives the same empty page as F1. Under the current text the list is complete and the guard may hold, which is right. Nothing states it and no fixture pins it.

**Smallest fix:** one sentence in 7.2 and one control fixture (`worker-list` zero rows, `task-list` ok: T True with the `origin not proved` note). Without it, the F1 fix can over-trigger.

### Notes (not findings)

- N1: `--include-remote` is a forbidden token (`:537`), so rows from connected servers are never listed. Their transcripts are not on this disk either, and DESIGN `:517` already marks `remote hosts` coverage `unknown`. Accepted.
- N2: the default `worker-list` includes `terminalState: released` rows (first live row had it), so there is no hidden default filter. `--terminal-state` is not used by the design.
- N3: rows are returned newest first, so truncation drops the oldest Dispatches, which are the ones the "older transcript" fixture is about. The text handles this (note, not Historical).

## Self-Audit

**(a) Reliance:** I did not rely on the mechanical report `r3-b3-mechanical.md` for any verdict. I read it (it claims 9 of 9 checks pass) and it is consistent with what I read in the DESIGN, but its checks are grep presence checks and cannot see F1 or F2.

**(b) Independent semantic checks:**
- Three-case rule against SPEC FR-010: read DESIGN `:501` and SPEC `:104`; reasons and literals match.
- Unknown-Run behaviour: ran `worker-list --run run_does_not_exist_zz --json` (exit 0, `ok` true, zero rows) and `task-list --run run_does_not_exist_zz --json` (`run_not_found`); compared with DESIGN `:245`, `:896`, `:979`, `:972` and SPEC `:96`.
- Truncation signal: ran `worker-list --limit 1 --json` and a real-Run call; compared the page object with DESIGN `:548`, `:501`, `:980`.
- Budget path: read DESIGN `:244-251`, `:287`, `:349`, `:367-371`, `:595`.
- Default filter: first live row had `terminalState: released`, so released rows are in the default list.

## Checks

| Check | What it verifies | Result |
|---|---|---|
| C1 | DESIGN `:501` lists the three SPEC FR-010 reasons (outage, truncated, call_failed) with SPEC wording (SPEC `:104`) | PASS |
| C2 | The three `origin unknown:` literals and their order agree across 7.2 (`:501`), section 11 (`:746`) and research/04 4.2 | PASS |
| C3 | "Outage" covers call-one unavailable and later unavailable (`orca_available` False; `:250-251`, `:286`) | PASS |
| C4 | "Truncated" matches the live page shape (`limit` 100 default, rows newest first) for the full-page case | PASS (F3 is a MINOR note) |
| C5 | "call_failed" covers every scoped Run whose `worker-list` did not complete, including a Run never attempted | FAIL (F2) |
| C6 | An unknown Run id is detected as an incomplete list | FAIL (F1) |
| C7 | A real Run with zero rows is treated as a complete list and does not break the guard | PASS (F5 is a MINOR note) |
| C8 | No snapshot race lets a just-started worker be proved unjoined | PASS (F4 is a MINOR note; not a blocker) |
| C9 | No default `worker-list` filter hides released Dispatches (live: `released` rows present) | PASS |
| C10 | `--include-remote` exclusion does not hide a local transcript's worker (N1, `:517`) | PASS |
| C11 | Research/04 4.2 edits 1 to 3 are reflected in DESIGN `:746` and the FR-010 row `:771` (three incomplete cases kept distinct from the four join-incomplete cases) | PASS |
| C12 | The DESIGN premise that an unknown Run gives a `worker-list` error (`:245`, `:896`, `:979`) matches live Orca | FAIL (F1) |
| C13 | The "safe behaviour until closed" claim (`:972`) holds for open items 4 and 5 | FAIL (F1 breaks item 4; item 5 holds) |

A check passes when it has no BLOCKING or MAJOR finding. MINOR notes F3, F4 and F5 are listed beside their checks and never fail the gate.

## Confidence and tool engagement

**Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The page-shape and unknown-Run results are from one live Orca runtime on 2026-11-08; a different Orca version could differ (the SPEC pins Orca 1.4.245).
**Tool engagement:** Read: 12 | Grep: 9 | Glob: 0 | Bash: 6 (all read-only Orca calls or `--help`).

Answer to the question asked: the three cases are not the only ways. The unknown Run id is a BLOCKING fourth case, and a Run whose `worker-list` is never attempted is a MAJOR fifth. The zero-row Run is correctly complete and is a note.

Verdict: FAIL
Blocking count: 2
