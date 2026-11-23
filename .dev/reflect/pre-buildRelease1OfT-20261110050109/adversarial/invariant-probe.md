# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent agent on the sonnet model (not an advocate). Input: `consensus-after-round2.md`, `diff-analysis.md`, the four round transcripts, both cards, the plan, SPEC, SNAP and `install_user_setup.py`. The orchestrator re-read the load-bearing citations (`install_user_setup.py:35` `_ORCA_CLIS = ("orca-ide", "orca")`, `:209-213` the 10 s `skills list --json` probe; plan lines 60, 63, 82, 97, 104, 112, 116, 118, 126, 142, 155, 157, 161, 171, 173, 179; SPEC lines 55, 154, 189, 322, 328, 340, 349, 373, 375, 393) and confirmed the quoted text.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | The min(timeout, remaining) cycle-deadline fix alone meets T5, with discovery outside the budget | UNADDRESSED | HIGH | `_find_orca` takes no deadline (`install_user_setup.py:198`), probes two names (`:35`) at a fixed `timeout=10` (`:213`); plan:97 does not say whether discovery runs once or per cycle; SPEC:322 caps a cycle at 5 subprocesses |
| INV-002 | sufficiency_challenge | The C-001 fix is complete without naming the outcome of a budget-truncated cycle | UNADDRESSED | HIGH | plan:104 "`FAILED (timeout)`" vs plan:116 "`cycle overran`"; plan:112 STALE counts only successful polls; plan:118 keeps the previous snapshot on failure; `poll(runner, namespace, cap=5)` (plan:97) has no deadline parameter |
| INV-003 | sufficiency_challenge | Publishing snapshots on failure/STALE (R1-03 fix) needs no further rules | UNADDRESSED | MEDIUM | SNAP:88 exclusive enum and "older than 45 s" vs SPEC:154 "3 intervals ... pass"; first-cycle failure has no last-good values; plan:173 silent on failed `--once`; no write happens during backoff |
| INV-004 | interaction_effects | R1-05 is the only missing `Depends on` | UNADDRESSED | MEDIUM | plan:155 "Depends on: Task 8" while plan:161 needs "the 80-column screen render" (Task 9) |
| INV-005 | sufficiency_challenge | QA-01 can be fixed with the four named fixtures | UNADDRESSED | MEDIUM | plan:60 mentions "a second page file whose `page.total` differs" but does not name it; plan:63 checks "The four JSON files"; a one-page capture has no `nextCursor` |
| INV-006 | state_variables | The model already carries per-row state for `not reobserved`, `*` and T22 texts | UNADDRESSED | MEDIUM | plan:82 `WorkerRow` has no last-seen cycle or flags; plan:126 placeholder "when its row disappears" vs SPEC:349 / SPEC:393 dropped rows "stay listed as `not reobserved`"; SPEC:340 bounds only question retention |
| INV-007 | state_variables | Fixture-mode output is deterministic | UNADDRESSED | MEDIUM | plan:179 byte-identical runs; plan:126 header `as of <HH:MM>`; plan:112 only the monotonic clock is injectable |
| INV-008 | count_divergence | `collected n` and `shown x/y` have one definition | UNADDRESSED | MEDIUM | plan:97 `(mismatch)`; SPEC:328 dedup within a cycle; plan:103 `collected 500`; plan:142 footer `shown x/y` |
| INV-009 | guard_conditions | Cursor, shape errors and non-tty stdin always resolve | UNADDRESSED | MEDIUM | plan:97 follows `page.nextCursor` with no rule for a missing cursor; plan:112 daemon thread with no catch-all; plan:173 checks stdout only, plan:33 key reader needs a tty |
| INV-010 | collection_boundaries | T33 and the inspector caps line work with zero rows | UNADDRESSED | MEDIUM | plan:173 "Enter opens the detail inspector" on a selection; plan:142 minimum rows include "one ledger row" |
| INV-011 | collection_boundaries | The `e` export needs no extra bounds | UNADDRESSED | LOW | plan:173 `observe-<YYYYMMDD-HHMMSS>.txt` in the current directory, no exclusive create; plan:157 atomic write applies only to `write_snapshot` |
| INV-012 | sufficiency_challenge | The T16 fix only adds a test | UNADDRESSED | LOW | plan:71 fixtures are named, fixed-size (`base` about 12 rows); SPEC:373 fixes no terminal height |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 0
- **UNADDRESSED**: 12
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 8 (INV-003 to INV-010)
  - LOW: 2 (INV-011, INV-012)

## Invariant gate

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002
These invariant violations must be resolved before convergence can be declared.
Action taken: depth is standard, so no Round 3 runs. Both items are amendments to the already-blocking cycle-budget and discovery findings, not disputes between the advocates; the orchestrator incorporates them into the suggested fixes of M-01 and M-02 in the refactor plan and lists them in the return contract's `unaddressed_invariants` for transparency.

WARNING: 8 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-003, INV-004, INV-005, INV-006, INV-007, INV-008, INV-009, INV-010
INV-003 is folded into the M-03 fix, INV-005 into the M-04 fix, INV-010 into the M-05 and M-06 fixes; INV-004, INV-005 and INV-009 also appear in the "missed by both cards" list. INV-006, INV-007 and INV-008 are recorded here only.

## Fault-finder output (verbatim)

ID: INV-001
CATEGORY: interaction_effects
ASSUMPTION: The agreed cycle-deadline fix (R1-01/QA-05: per-call timeout = min(DEFAULT_TIMEOUT_S, time left in the 15 s budget)) is enough to meet T5 "cycle ends within the 15 s cycle budget". The R1-02 narrowing (discovery is SPEC-prescribed, so only the false "only live call" claim and the seam are defects) leaves discovery's cost out of the budget.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- `_find_orca` has no deadline parameter and cannot take the min() rule: `src/superclaude/cli/install_user_setup.py:198` "def _find_orca() -> str | None:".
- It probes up to two candidates, each with a fixed 10 s timeout: `install_user_setup.py:35` `_ORCA_CLIS = ("orca-ide", "orca")` and `install_user_setup.py:213` "timeout=10,". The worst case is about 20 s before the first `worker-list`, which is more than the whole 15 s budget.
- The plan does not say whether discovery runs once at startup or on every cycle. `poll` takes no orca path or discovery argument: plan:97 "`poll(runner, namespace, cap=5)`". `NOT AVAILABLE` is a per-result outcome: plan:97 "when none is found the result is `NOT AVAILABLE (orca binary not found)`".
- If discovery runs per cycle, it breaks the subprocess count as well as the time budget. SPEC:322 "A cycle runs at most 5 subprocesses". Five `worker-list` calls plus 1-2 `skills list` probes is 6-7.
- Both cards and the debate treat R1-02 as only a seam/wording problem and R1-01 as only a per-call timeout problem.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: blocking (amend the R1-01/R1-02 fix; not a new row). The fix must state that discovery runs once per process, outside the cycle, with its own budget. Or it must pass a deadline into discovery and count its subprocesses against the 5-call cap.

ID: INV-002
CATEGORY: sufficiency_challenge
ASSUMPTION: C-001 (R1-01+QA-05) is fixed by min(timeout, remaining) plus a fake-clock test that ends in `cycle overran`.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- The outcome class of a cycle cut off by the budget is undefined. For example, pages 1-3 succeed and page 4 is killed at the remaining-budget limit. It could be PARTIAL, FAILED (timeout) or `cycle overran`, and these decide what happens next:
  - STALE clock: plan:112 "STALE when 45 s ... pass with no successful poll".
  - Snapshot replacement: plan:118 "A failed cycle keeps the previous snapshot readable".
- Labels conflict. plan:104 "T5: a fake runner that overruns yields `FAILED (timeout)` and the child is killed". plan:116 "an overrunning call is killed and the state text contains `cycle overran`". SPEC:392 (T40) has the same overrun wording.
- If a budget-truncated cycle counts as failed, a fleet whose pages take more than 15 s in total never publishes rows. It reads STALE after 45 s while the last good snapshot ages out. If it counts as partial and successful, the 3 good pages are shown, but `cycle overran` is then a warning, not a failure state.
- `poll` has no clock or deadline parameter in the plan. plan:97 "`poll(runner, namespace, cap=5)`" and `Runner` is "(argv, timeout)". The fake-clock test therefore needs a signature change. Task 6 and Task 7 are separate tasks, so the contract between them has to be pinned.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: blocking (the C-001 fix must name the outcome class, the label and whether it resets STALE; this is not a new row)

ID: INV-003
CATEGORY: sufficiency_challenge
ASSUMPTION: R1-03 is fixed by publishing an atomic snapshot on failed cycles and STALE transitions (the suggested fix in the card).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The snapshot enum is exclusive, but the screen state is not. SNAP:88 "`OK`, `STALE` (older than 45 s), `ERROR` or `UNKNOWN`". plan:112 lists `FAILED (<reason>) <age>` and `STALE` as separate `latest()` states. After 45 s of continuous failure both conditions hold. The plan gives no precedence rule, and an ERROR/STALE choice loses the `source.error` code.
- The 45 s boundary differs between sources. SNAP:88 says "older than 45 s", which is strict. SPEC:154 says "3 intervals (45 s at the 15 s cycle) pass", which is inclusive. plan:116 says "STALE after 45 s". A fake-clock test at exactly 45.0 s cannot pass both readings.
- Initial state when the first cycle fails: there is no last-good snapshot, so `source.observedAt`, `page.total`, `counts` and the rows have no value. The plan does not say whether they are `UNKNOWN` or empty. plan:173 "write the JSON snapshot after each successful cycle in live mode, and once with `--once`" does not say whether a failed `--once` run still writes one.
- STALE is derived from the clock in `latest()` (plan:112). Writes happen at cycle end. During backoff of up to 60 s no cycle runs, so the file cannot report STALE at 45 s. A consumer cannot tell a dead producer from a quiet one.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (unpinned details of an already-blocking fix; no new row)

ID: INV-004
CATEGORY: interaction_effects
ASSUMPTION: A-004 / R1-05 is a one-off (Task 5 is missing Task 4). Numeric order makes the other `Depends on` lines harmless.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: I checked every `Depends on` line against the acceptance criteria. A second gap of the same class exists in Task 10, and I found no others.
- Task 10 declares only Task 8: plan:155 "Depends on: Task 8".
- Its T27/T48 criterion needs Task 9's `render`: plan:161 "an identifier that the 80-column screen render truncates with `>` appears in full in the export".
- Task 11 does list Task 9 and Task 10: plan:171 "Depends on: Task 1, Task 9, Task 10". Task 10 on its own breaks if run or resumed out of order.
- R1-05 itself: plan:80 "Depends on: Task 3" versus plan:88 "The `duplicate-out-of-order` variant" (Task 4).
- All other criteria use only direct or transitive dependencies. The over-declared lines (Tasks 2, 3, 4) are harmless.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (same class as R1-05; fix both together, or give A-004 one resolution)

ID: INV-005
CATEGORY: sufficiency_challenge
ASSUMPTION: QA-01 is fixed by adding Task 6/7 criteria that run all four golden fixtures through a fake runner. This includes asserting "changed during read" and "time went back" from the contradictory fixture.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The "second page file" is not in Task 3's file list, nor in its criteria. plan:60 "Create `.../worker_list_success.json`, `worker_list_missing.json`, `worker_list_stale.json`, `worker_list_contradictory.json` and `.../test_fixtures_redacted.py`". The sentence "plus a second page file whose `page.total` differs" appears only later in the same paragraph.
- plan:63 "The four JSON files exist". So the fifth file has no name and no redaction check.
- A two-page traversal needs page 1 to carry `hasMore=true` and a `nextCursor`. plan:60 captures one real envelope with `--limit 100`, which for a small fleet has `hasMore=false`. The edit instructions do not set a cursor.
- Without that, "changed during read" (SPEC:158, plan:97) cannot be produced from the golden files.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (the QA-01 fix cannot be implemented as worded until the file and cursor are named)

ID: INV-006
CATEGORY: state_variables
ASSUMPTION: Narrowing QA-08 to "unpinned text" and treating the T22 view texts as only a missing assignment. This assumes the declared model already carries the per-row state those texts need.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The declared `WorkerRow` has no last-seen cycle and no flag field: plan:82 "...plus `source_index` and a count of unrecognised keys". `Snapshot` has "flags such as `order unknown`" at snapshot level. plan:88 says "a row without timestamps is flagged `order unknown`", and `merge_rows` is the only place that flag is set.
- Task 8 needs per-row `not reobserved` and per-row `*`/removed state: plan:126 "rows on pages not read this cycle read `not reobserved`" and "added, removed or changed ... rows carry `*`". Removed rows must survive somewhere. `build_view` takes a single snapshot, so the union of rows across cycles must be inside it.
- Two instructions conflict. The placeholder fires "when its row disappears" (plan:126; SPEC:55). Dropped rows "stay listed as `not reobserved`" (SPEC:349; T41, SPEC:393). A dropped worker row never disappears, so one of the two is unreachable.
- Retention is bounded only for questions: SPEC:340 "Retention is bounded at 1,000 records". Worker rows kept as `not reobserved` grow without a bound.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (the model needs row-level `lastSeenCycle` and flags, a retention rule, and a decision on which of the two texts applies to workers; this affects the T22 and QA-08 fixes)

ID: INV-007
CATEGORY: state_variables
ASSUMPTION: Fixture mode and the collector have fixed, injectable time inputs, so the plan's deterministic-output criteria can pass reproducibly.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- plan:179 "T6: two `--fixture base --once` runs produce byte-identical output".
- The header carries wall time: plan:126 "`as of <HH:MM>`", and "(no I/O, no clock reads; times come from the snapshot and `ui_state`)". The strip carries ages such as `OK 4s`.
- The snapshot's wall and monotonic times come from the collector. plan:112 makes only the monotonic clock injectable: "counted only on an injectable monotonic clock (default `time.monotonic`); wall-clock time is used only to print `HH:MM`". A real wall clock makes two runs differ at a minute boundary.
- plan:71 makes `fixture(variant)` deterministic with no I/O, but the snapshot wrapper around it in `--fixture --once` is not covered.
- The stale-fixture check (QA-01 fix: "old evidence age with the source still OK") and T42 need an injected wall time. The plan does not provide one.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (give the collector an injectable wall clock, and fix the snapshot time in fixture mode)

ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: The denominators `collected n`, `shown x/y`, `filter k of n collected` and the `(mismatch)` check all use the same, defined n and y.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- `collected n` is not defined as before or after dedup. plan:97 "`collected n / reported T (mismatch)` when a finished traversal does not match". SPEC:328 "Rows are deduplicated by identity within a cycle". plan:88 requires `duplicates_ignored` greater than 0.
- Newest-first paging shifts between pages. A worker that changes state between page requests can appear twice. After dedup, n < T gives a spurious `(mismatch)`. Before dedup, n = T hides a real duplicate.
- T4 "collected 500" (plan:103) needs a fake with 500 distinct ids. A fake that repeats ids returns 100 after dedup.
- The footer denominator is not pinned either. plan:142 "`shown x/y | collected n / reported T`" and SPEC:373 (T16) "y equal to the fixture total". Hidden historical rows (`k historical hidden`, plan:126), the local filter and `not reobserved` rows (INV-006) can each change y without changing n.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (needs one stated definition of n and y)

ID: INV-009
CATEGORY: guard_conditions
ASSUMPTION: A cursor, a shape error or a non-tty fd always resolves to a defined result. Paging and the collector thread cannot misbehave on the boundary inputs.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- `hasMore=true` with a missing, blank or repeated `nextCursor` is undefined. The required fields are `result`, `result.workers` and `result.page.hasMore` only (plan:82). The plan only says "follows `page.nextCursor` up to 5 calls per cycle" (plan:97). A missing cursor leads `build_argv` to re-request page 1, so five calls return the same 100 rows and inflate duplicate counts.
- The rejection path is not mapped. plan:97 says an over-long cursor "is rejected before any process starts", and `parse_envelope` raises `ShapeError` (plan:82). The Task 7 loop runs in a daemon thread (plan:112) with no catch-all. An uncaught exception ends the thread silently and the screen drifts to STALE.
- The tty guard uses stdout, but the key reader needs a tty on stdin. plan:173 "When stdout is not a tty, or on a platform without `termios`, the command behaves as `--once`". plan:33 "When the descriptor is not a tty the context manager reports that it is unavailable". With stdout a tty and stdin not (for example `observe < /dev/null`), no behaviour is defined and there is no quit path.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor

ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: The agreed T33 (empty state) and QA-09 (inspector caps line) fixes work when the collection is empty.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- With zero workers there is no selectable row. The inspector is opened by Enter on a selection: plan:173 "Enter opens the detail inspector", and plan:142 "The detail inspector (Enter) lists every field untruncated". SPEC:59 describes the inspector as per-row fields.
- So the QA-09 inspector half (SPEC:352 "help and the inspector say so") is unreachable on the `empty` variant, on `worker-list NOT AVAILABLE`, and when a filter hides every row. plan:142's only source-level inspector content is "stderr of a failed poll".
- The T33 string needs a home. plan:142 "The minimum rows are ... one ledger row and the footer". It should say whether the empty-state line is that mandatory ledger row, or it competes with T49 and T35 at 80 columns. Keys `j`/`k`/Enter/`e` with zero rows are unspecified.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (extend the T33 and QA-09 fixes with a source-level inspector section and a zero-row selection rule)

ID: INV-011
CATEGORY: collection_boundaries
ASSUMPTION: The only R1-04 exposure is wording in the constraints (V2 position), or a field-suppression question (V1 position). The `e` export and the persisted free text need no further bounds.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE:
- `e` writes a predictable, second-resolution file name into the cwd: plan:173 "`e` writes the text record export to `observe-<YYYYMMDD-HHMMSS>.txt` in the current directory with mode 0600". Two presses in one second collide. The plan does not say exclusive creation, so a pre-planted symlink in a shared cwd would be followed. Task 10's `write_snapshot` is atomic (plan:157), but this path is not.
- The export carries unredacted free text: plan:157 "full identifiers, no truncation", and the sanitizer strips controls only (plan:45).
- Fixing the wording at plan:25 does not cover what the executor itself leaves behind. The task's `./artifacts/` files (plan:33, plan:97, plan:142) sit in the always-staged `.dev/tasks/<id>/artifacts/` (user CLAUDE.md core rule 4; no line number available). Task 11's live `--once` criterion (plan:182) also prints live ledger content.
MISSED_BY_BOTH_CARDS: yes, PROPOSED_SEVERITY: minor (require exclusive creation or a unique suffix for `e`, and say the artifact files hold measurements only)

ID: INV-012
CATEGORY: sufficiency_challenge
ASSUMPTION: The T16 fix (scenario matrix) only needs a test added. The plan's fixture API can already produce 50, 80 and 100 row cases.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE:
- Fixtures are chosen by name only, with fixed sizes: plan:71 "`fixture(variant)` ... `base` (about 12 rows across several runs and states)". plan:178 requires an unknown name to exit non-zero and list the valid names. The T16 sizes need a size parameter or new variants. Either one changes the Task 4 API and the `--fixture` name list that the consensus did not touch.
- SPEC:373 "{5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders)... every hidden overflow shows `x/y shown`". It fixes no terminal height, so `x/y shown` cannot be asserted without one.
- T16 appears in neither Task 8's nor Task 9's test list: plan:126 "T6, T8, T9, T13 to T15, T18, T20, T21, T25, T34, T38, T41 and T42" and plan:142 "T23 to T26, T28, T30, T35, T43 and T49".
MISSED_BY_BOTH_CARDS: no. Both advocates raised T16, but not the API and height gap. PROPOSED_SEVERITY: minor (a detail of the already-blocking T16 fix)

Summary (fault-finder): Twelve probes, all UNADDRESSED in the consensus. INV-001 and INV-002 change what the consensus fixes must say: `_find_orca` can spend up to 20 s on two fixed 10 s probes outside the budget and may breach the 5-subprocess cap, and a budget-truncated cycle has no defined outcome class or label. The rest are minor and do not change a merged disposition. Not probed: `merge_rows` timestamp-comparison edge cases and export order for rows with no timestamps (SNAP:109 versus screen source order). No code was run.
