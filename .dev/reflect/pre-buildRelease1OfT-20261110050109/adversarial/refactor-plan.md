# Refactoring Plan

## Overview
- Base variant: Variant 2 (`variant-2-original.md`, reviewer-2 card, opus:qa)
- Incorporated variant: Variant 1 (`variant-1-original.md`, reviewer-1 card, haiku:analyzer)
- Output: ONE de-duplicated findings list, `merged-output.md`, in this same folder (`.../adversarial/merged-output.md`). Nothing is written outside this folder.
- Planned changes: 16 merged findings (M-01 to M-16) plus a "missed by both cards" list (N-01 to N-09)
- Overall risk: Low (text assembly only; no citation may be invented or altered)
- Review status: auto-approved (non-interactive), 2026-11-10

## Judge rulings (decided with evidence; record these in merged-output.md)

1. **Severity rule applied to every finding.** Blocking when (a) the plan has wrong behaviour, a false claim, or a security or data-loss risk; or (b) a required deliverable is genuinely absent: a SPEC section 10 test that applies to R0/R1 and that no task maps or excludes, whose required output no task names explicitly; or a SPEC requirement that no task instructs, even through a SPEC section the task tells the executor to follow; or a SPEC gate condition the plan leaves unmet. Minor when the behaviour is instructed (explicitly, or through a referenced SPEC section) and only its assertion is missing, when the requirement applies only to a view the plan excludes, or when the problem is wording or task bookkeeping. Both advocates adopted this rule in Round 2 (X-002).
2. **T33 (R1-06 minor vs QA-02 blocking): blocking.** SPEC:172 says the `empty` variant "must render `no observed items in this source window; not proof none exist`" and SPEC:385 makes it test T33. Plan:126 maps T6, T8, T9, T13-T15, T18, T20, T21, T25, T34, T38, T41 and T42 to Task 8, never T33, and its explicit token list has neither empty-state string; plan:21 does not exclude it. Plan:75 builds the data only. Rule 1(b) applies. The V1 advocate conceded in Round 1.
3. **R1-04 constraint wording: minor (narrowed).** The V1 advocate held blocking (SNAP:77 forbids credentials and the control-only sanitizer at plan:45 cannot stop a printable one in `stage.detail`); the V2 advocate held minor. Ruling: minor. SPEC:337 defines the trust-boundary sanitizer as control-only, SPEC:138 allows `stage.activity`/`.detail` to be shown sanitized and labelled `worker-reported`, and SNAP:103 freezes those fields, so the planned behaviour matches the SPEC and the frozen contract. What is wrong is that plan:25 and plan:157 promise more than the design delivers; no acceptance criterion depends on the over-broad sentence. That is wording. Any redaction of printable secrets would be a new requirement for the owner, not a plan defect.
4. **R1-01 and QA-05 are one finding (M-01).** Same claim, same severity; QA-05 carries the T5 citation (SPEC:369). The fault-finder's INV-001 and INV-002 (HIGH, unaddressed) are added to its fix, because the per-call min() rule alone is not sufficient.
5. **R1-03 (snapshot only on success): confirmed blocking.** Plan:173 writes "after each successful cycle in live mode"; SNAP:79 has one envelope per cycle and SNAP:88 freezes `source.status` as OK, STALE, ERROR or UNKNOWN, so STALE and ERROR can never be published and a consumer reads a stale file as OK. Plan:118 (collector keeps the last good snapshot in memory) does not cover the file. Both advocates agreed.
6. **QA-09: blocking, narrowed to the inspector half.** SPEC:352 requires "help and the inspector say so"; plan:173 covers help; no task (plan:126, plan:142) instructs the inspector line, and no task references SPEC section 9 "Several observers". Rule 1(b). Both advocates agreed after Round 2.
7. **Partial rejections inside narrowed findings** (none of the 19 card findings is rejected outright): QA-04's "last good snapshot is not kept" half (plan:118 keeps it); QA-08's NOT AVAILABLE item (plan:182 asserts it) and its STALE/FAILED strip cells (plan:126); QA-11's "no task builds this" for the STALE and FAILED cells (plan:126); QA-12's "undocumented deviation" half (plan:33 gives the reason, and plan:20 cites owner-decisions item 5, which confirms the stack).

## Planned Changes

Each change produces one merged entry. Copy every `evidence_file_line` value **verbatim** from the card finding named in "Sources" (open `variant-1-original.md` / `variant-2-original.md` and copy the strings exactly, in card order, R1 citations first then QA citations for merged pairs; drop exact duplicates only). Do not add, shorten, renumber or reformat any citation. Severity, plan task, claim, fix and disposition are given below and are copied as written.

### Change #1 → M-01
- Sources: R1-01, QA-05 | Severity: blocking | Plan task: Tasks 6 and 7
- Claim: The plan bounds each `worker-list` call (DEFAULT_TIMEOUT_S under 15 s) but never the cycle, so five sequential calls can run far past the 15 s budget that T5 requires, and no criterion checks total cycle time.
- Suggested fix: Pass a monotonic cycle deadline (15 s from cycle start) and an injectable clock into `poll`; give each call a timeout of min(DEFAULT_TIMEOUT_S, time left) and stop paging when the budget is spent. Name the outcome of a budget-truncated cycle (recommended: pages already parsed are published as PARTIAL with `cycle overran (Ns)` and count as a successful poll for STALE only if at least one page parsed; a cycle with no parsed page is `FAILED (timeout)`), and make T5 (plan:104) and T40 (plan:116) use the same label. Keep binary discovery outside the cycle (M-02) or count it against both the budget and the 5-subprocess cap. Add a fake-clock test in which every call is close to the timeout and the cycle still ends within 15 s.
- Disposition: confirmed. Both cards and both advocates agree. QA-05's SPEC:369 citation is the stronger basis. Fix extended with fault-finder items INV-001 (discovery's two 10 s probes, `install_user_setup.py:35` and `:213`) and INV-002 (undefined outcome of a truncated cycle).
- Integration: base QA-05 entry, merged with R1-01 citation. Risk: Low.

### Change #2 → M-02
- Sources: R1-02 | Severity: blocking | Plan task: Task 6; Constraints; Task 11
- Claim: The constraint that the only live Orca call is `worker-list` is false, because the plan reuses `_find_orca()`, which runs a live `skills list --json` subprocess outside the injectable runner, so T36 (subprocess patched to raise) and the fake-runner tests cannot isolate it.
- Suggested fix: Keep `_find_orca()` (SPEC section 9 prescribes it), but correct plan:23 to name its `skills list --json` probe as the one other approved read-only call. Run discovery once per process before the first cycle, outside the 15 s budget and the 5-call cap, with a stated bound (two candidates at 10 s each can take about 20 s). Inject discovery separately from `Runner` so T36 and the fake-runner tests run without Orca, skip discovery in `--fixture` mode, and say whether the Task 11 argv trace includes the probe.
- Disposition: narrowed. Reusing `_find_orca()` is not the defect (SPEC:312 prescribes it); the defect is the false "only live Orca call" claim at plan:23 and discovery sitting outside the test seam. Both advocates agreed in Round 2.
- Integration: insert from Variant 1. Risk: Low.

### Change #3 → M-03
- Sources: R1-03 | Severity: blocking | Plan task: Tasks 10 and 11
- Claim: `--snapshot` is written only after successful cycles, so the file never publishes the frozen `source.status` values STALE or ERROR and a consumer keeps reading an old snapshot as OK.
- Suggested fix: Write the snapshot atomically at the end of every live cycle (and on a failed `--once`), keeping last-good rows and `source.observedAt` while updating `source.status` and `source.error`, and rewrite it when the 45 s STALE threshold passes during backoff. Pin the precedence when ERROR and STALE both hold (keeping `source.error`), whether the 45 s boundary is inclusive (SNAP says "older than 45 s", SPEC says "3 intervals ... pass"), and what a first-cycle failure writes (no rows; page and counts `UNKNOWN`). Test a good poll followed by a failure, and the 45 s threshold.
- Disposition: confirmed. Plan:118 keeps the last good snapshot in the collector's memory only; it does not make the file report failure. Fix extended with fault-finder item INV-003.
- Integration: insert from Variant 1. Risk: Low.

### Change #4 → M-04
- Sources: QA-01 | Severity: blocking | Plan task: Tasks 3, 5 and 6
- Claim: The missing, stale and contradictory golden fixtures are created but no contract test consumes them, although SPEC section 7 keeps the R1 data gate closed until all four kinds are pinned in a contract test.
- Suggested fix: Add Task 6 or Task 7 acceptance criteria that run each of the four fixture files through a fake runner and assert: success parses; missing gives `scope unknown`, `reported unknown` and per-field `UNKNOWN`; stale gives old evidence age with the source still OK; contradictory gives duplicates ignored, time-went-back and `changed during read`. Name the contradictory second page file in Task 3's file list and its redaction test, and give its first page `hasMore=true` and a `nextCursor` so a two-page traversal is possible.
- Disposition: confirmed. Task 5 (plan:86) tests missing fields by mutating the success data, not by loading `worker_list_missing.json`. Fix extended with fault-finder item INV-005.
- Integration: base QA-01. Risk: Low.

### Change #5 → M-05
- Sources: R1-06, QA-02 | Severity: blocking | Plan task: Tasks 8 and 9
- Claim: No task builds or pins the T33 empty states (`no observed items in this source window; not proof none exist` for the `empty` variant, and `worker-list returned 0 workers in scope=bound`), although the plan neither maps nor excludes T33.
- Suggested fix: Add both strings to the Task 8 view model, map T33 to Tasks 8 and 9, and add criteria for the `empty` variant (exact text) and for a bound scope with zero rows. Say which minimum row the empty-state line occupies at 80 columns, and what `j`, `k`, Enter and `e` do with zero rows.
- Disposition: confirmed; severity decided as blocking (judge ruling 2). R1-06 rated it minor; QA-02's blocking holds because a required SPEC acceptance test and its output are absent. Fix extended with fault-finder item INV-010.
- Integration: base QA-02, merged with R1-06 citations. Risk: Low.

### Change #6 → M-06
- Sources: QA-09 | Severity: blocking | Plan task: Tasks 9 and 11
- Claim: SPEC section 9 requires both help and the inspector to say that caps are per observer process; Task 11 puts it in `--help` only, its criterion checks only option names, and no task gives the inspector the statement.
- Suggested fix: Add a per-process caps line to the inspector in a source-level section that is reachable even with zero rows (Task 9) and assert it; extend the Task 11 help criterion to check the three help statements (read-only, caps per process with no singleton lock, `--include-remote` not available).
- Disposition: narrowed to the inspector half (help is covered at plan:173); severity raised from the card's minor to blocking (judge ruling 6), agreed by both advocates.
- Integration: base QA-09. Risk: Low.

### Change #7 → M-07
- Sources: R1-04 | Severity: minor | Plan task: Constraints; Tasks 2, 9 and 10
- Claim: The constraint that no absolute path, token or credential is ever printed, and Task 10's "no credentials" rule, promise more than the design delivers, because worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown and exported after control-only sanitizing.
- Suggested fix: Narrow plan:25 and plan:157 to what the plan guarantees: nothing raw is committed or logged, no credential or terminal-handle field is exported, and worker free text and stderr are control-sanitized but not redacted and are labelled `worker-reported`. Keep the SNAP-frozen stage fields. If printable-secret redaction is wanted, raise it with the owner as a new requirement.
- Disposition: narrowed; severity decided as minor (judge ruling 3). The card's fix of suppressing the stage fields is withdrawn because SNAP:103 freezes them (the V1 advocate withdrew it in Round 2).
- Integration: insert from Variant 1. Risk: Low.

### Change #8 → M-08
- Sources: R1-05 | Severity: minor | Plan task: Task 5
- Claim: Task 5's acceptance criteria use the `duplicate-out-of-order` variant that Task 4 creates, but Task 5 depends only on Task 3.
- Suggested fix: Add Task 4 to Task 5's dependencies, or use the contradictory golden fixture for that test. Fix it together with the same gap in Task 10 (N-06).
- Disposition: confirmed. Harmless under sequential execution but wrong on reorder or per-task resume (A-004 label left unresolved; outcome agreed).
- Integration: insert from Variant 1. Risk: Low.

### Change #9 → M-09
- Sources: R1-07, QA-06 | Severity: minor | Plan task: Tasks 6, 8 and 9
- Claim: The PARTIAL disclosure `(newest first; oldest rows not read; long-running active workers may be among them)` and the `reported T (page k)` form appear in no instruction token list or criterion.
- Suggested fix: Carry the last-read page and the cap-stop reason into the view model, add the full text and the page form to the Task 8 COUNTS tokens, and assert both at view level and in the screen and export tests.
- Disposition: confirmed. Minor because Task 8 tells the executor to follow SPEC section 4, which contains the text, and T4 (plan:103) is mapped; only the explicit token and the assertion are missing.
- Integration: base QA-06, merged with R1-07 citations. Risk: Low.

### Change #10 → M-10
- Sources: QA-03 | Severity: minor | Plan task: Task 6
- Claim: Task 6 names `PARTIAL (empty page k)`, `reported T1-T2 (changed during read)` and `collected n / reported T (mismatch)`, but its acceptance criteria pin only T4 and T18.
- Suggested fix: Add fake-runner criteria for the empty-page, total-changed and mismatch outcomes.
- Disposition: narrowed; severity lowered from the card's blocking to minor. Plan:97 instructs all three outcomes; only the assertions are missing (both advocates agreed).
- Integration: base QA-03. Risk: Low.

### Change #11 → M-11
- Sources: QA-04 | Severity: minor | Plan task: Task 6
- Claim: No Task 6 criterion pins that `poll` turns a missing required field (`result`, `result.workers`, `result.page.hasMore`) or a second JSON envelope into `FAILED (shape)`; Task 5 tests `ShapeError` only at parser level.
- Suggested fix: Add a Task 6 criterion mapping a shape error and a two-envelope response to `FAILED (shape)`.
- Disposition: narrowed; severity lowered from blocking to minor. The "last good snapshot is kept" half is rejected: plan:118 already requires "A failed cycle keeps the previous snapshot readable and marks it with the failure". The card's own citation of plan:118 refutes that half; the citation is kept verbatim.
- Integration: base QA-04. Risk: Low.

### Change #12 → M-12
- Sources: QA-07 | Severity: minor | Plan task: Tasks 8 and 9
- Claim: T31 (cost renders `cost unavailable`, never `$0`) is not excluded, and no acceptance criterion pins it, although Task 8 lists the `cost unavailable` token.
- Suggested fix: Add a Task 8 criterion: the COUNTS tokens contain `cost unavailable` and no variant's output contains `$0`.
- Disposition: confirmed. Minor because the token is instructed explicitly at plan:126.
- Integration: base QA-07. Risk: Low.

### Change #13 → M-13
- Sources: QA-08 | Severity: minor | Plan task: Task 8
- Claim: Several Task 8 texts are instructed but unpinned: `not reobserved` for a dropped row (second half of T41), the `selected <id> no longer in source window` placeholder, `filter <expr>: k of n collected`, `scope unknown`, `one Run only`, and the `NOT POLLED` strip cell.
- Suggested fix: Add Task 8 criteria for each of these texts, and decide which applies to a worker row that drops out of the source: the placeholder (plan:126) or `not reobserved` (SPEC:349); as written one of them is unreachable.
- Disposition: narrowed. The NOT AVAILABLE item is rejected (plan:182 asserts it) and the STALE/FAILED strip cells are defined at plan:126. Fix extended with fault-finder item INV-006.
- Integration: base QA-08. Risk: Low.

### Change #14 → M-14
- Sources: QA-10 | Severity: minor | Plan task: Task 8
- Claim: SPEC section 9 says the header shows `read k of N Runs since start` and T45 pins it with the start-up view choice, but the plan neither builds it nor lists T45 as excluded.
- Suggested fix: Add T45 and the header token to the plan's stated exclusions with the reason (SPEC section 2 ties the token to the B view, and release 1 builds only the A ledger), or add the token and a never-switches test.
- Disposition: narrowed. SPEC:45 adds the token only "In the B view", which plan:21 excludes, so it is scope-ambiguous for release 1; the gap is the missing exclusion statement.
- Integration: base QA-10. Risk: Low.

### Change #15 → M-15
- Sources: QA-11 | Severity: minor | Plan task: Tasks 7, 8 and 9
- Claim: SPEC section 4 requires that when the source is STALE every value keeps its last-known reading with an `as of HH:MM:SS` qualifier; the plan has only the header `as of <HH:MM>`, and no criterion renders a STALE or FAILED snapshot through the view.
- Suggested fix: Add a Task 8 criterion: a STALE snapshot renders the `STALE <age>` cell and the `as of HH:MM:SS` qualifier on last-known values; a FAILED snapshot renders `FAILED (exit 2) 1m`.
- Disposition: narrowed. The STALE and FAILED strip cells are already defined at plan:126 and T26 (plan:148) renders STALE as a word; only the per-value qualifier and a view-level render test are missing.
- Integration: base QA-11. Risk: Low.

### Change #16 → M-16
- Sources: QA-12 | Severity: minor | Plan task: Task 1
- Claim: Task 1's spike criterion can be met by an artifact that records a failure, so it never fails on its own.
- Suggested fix: State that a recorded spike failure leaves Task 1 blocked, not passed, and assert a minimum number of Live repaints and decoded keys in one pty run.
- Disposition: narrowed. The "undocumented deviation from the Textual switch rule" half is rejected: plan:33 gives the reason inline ("switching to Textual changes the stack the owner confirmed"), plan:20 cites owner-decisions items 1 and 5, and item 5 confirmed Python + Rich after the SPEC was written.
- Integration: base QA-12. Risk: Low.

### Change #17 → "Missed by both cards" section

Add this list after M-16. These citations were read by the orchestrator (they are not card citations); copy them as given.

| N | Item | Severity | Evidence (verified) | Suggested fix |
|---|------|----------|---------------------|---------------|
| N-01 | T16 scenario matrix (sessions x widths, with `k of n` and `x/y shown` arithmetic) is neither mapped nor excluded; fixtures are fixed-size (`base` about 12 rows) | blocking | `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:373`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:71`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:126`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:142` | Map T16 to Task 9 for the 50/80/100-row x 160/116/80 part (the orchestrators axis has no R1 source and can be listed as excluded); add sized fixtures and a fixed terminal height so `x/y shown` can be asserted (INV-012). |
| N-02 | T22's visible texts (`k duplicate rows ignored`, `order unknown`, `conflict (time went back)`) are tested only in the model, never shown by the view | blocking | `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:375`; `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:328`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:88`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:126` | Add the three texts to the Task 8 view model and map T22's display half to Task 8 with a criterion. |
| N-03 | Binary discovery can take about 20 s (two candidates, 10 s each) and adds 1-2 subprocesses; the plan does not say whether it runs once or per cycle (INV-001) | blocking (tracked in M-01 and M-02) | `src/superclaude/cli/install_user_setup.py:35`; `src/superclaude/cli/install_user_setup.py:213`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:97`; `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:322` | See M-01 and M-02. |
| N-04 | The outcome of a cycle cut off by the budget is undefined, and T5 says `FAILED (timeout)` while T40 says `cycle overran` (INV-002) | blocking (tracked in M-01) | `...TASK-WF-buildRelease1OfT-20261110-045742.md:104`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:116`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:112`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:118` | See M-01. |
| N-05 | Exports are built from the same view model that hides historical rows and applies the local filter; nothing pins that exports carry every collected row | minor | `...TASK-WF-buildRelease1OfT-20261110-045742.md:126`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:157`; `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:189` | State that `export_text` and `export_json` include every collected row regardless of `h` and the filter, and add a regression test. |
| N-06 | Task 10 depends only on Task 8, but its T27/T48 criterion needs the Task 9 renderer | minor | `...TASK-WF-buildRelease1OfT-20261110-045742.md:155`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:161` | Add Task 9 to Task 10's dependencies (fix with M-08). |
| N-07 | The contradictory "second page file" is not named in Task 3's file list or redaction check, and a single real capture has no `nextCursor` (INV-005) | minor (tracked in M-04) | `...TASK-WF-buildRelease1OfT-20261110-045742.md:60`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:63` | See M-04. |
| N-08 | Guard gaps: `hasMore=true` with a missing `nextCursor`, uncaught errors ending the daemon poll thread, and stdout a tty while stdin is not (INV-009) | minor | `...TASK-WF-buildRelease1OfT-20261110-045742.md:97`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:112`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:173`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:33` | End paging as PARTIAL on a missing or repeated cursor; catch and report every cycle exception as `FAILED (<reason>)`; check stdin as well as stdout before entering interactive mode. |
| N-09 | The `e` export writes a predictable, second-resolution file name in the current directory without exclusive creation (two presses in one second collide; a planted symlink is followed) (INV-011) | minor | `...TASK-WF-buildRelease1OfT-20261110-045742.md:173`; `...TASK-WF-buildRelease1OfT-20261110-045742.md:157` | Create the file exclusively (or add a unique suffix) with mode 0600. |

In the merged output, write every plan path in full: `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:<line>` (the `...` above is shorthand for this plan only).

## Changes NOT Being Made

| Diff point / finding | Non-base approach | Rationale |
|---|---|---|
| R1-04 suggested fix (suppress `stage.detail` / `stage.activity`) | Suppress or redact the fields | SNAP:103 freezes them; V1 withdrew the suppression remedy in Round 2. |
| R1-06 severity minor | Keep T33 minor | Judge ruling 2: a required SPEC test and its output are absent. |
| QA-03 / QA-04 severity blocking | Keep blocking | Judge ruling 1: instructed at plan:97; only assertions missing. |
| QA-09 severity minor (card) | Keep minor | Judge ruling 6. |
| INV-006 to INV-008 as merged findings | Add as rows | Recorded in `invariant-probe.md`; INV-006 is reflected in M-13's fix; INV-007 (wall clock not injectable) and INV-008 (definition of `collected n` / `shown x/y`) are minor details left to the invariant record to keep the list short. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| All | Low | Text assembly; a citation typo would misstate evidence | Re-copy from the variant files; this plan and the variants are kept on disk |

## Review Status
- Approval: auto-approved
- Timestamp: 2026-11-10T05:40:00Z

## Required layout of merged-output.md

1. Provenance header (HTML comments): produced by /sc:adversarial, base Variant 2 (reviewer-2 card, opus:qa), merge date.
2. Title and a 3-line summary: counts (blocking 6, minor 10, rejected 0 outright with 4 partial rejections), convergence 0.91 with the invariant-gate status, and the severity definition used.
3. "Judge rulings" section restating rulings 1-7 briefly.
4. "Merged findings" section: one block per M-01..M-16 with fields, in this order: `id`, `sources`, `severity`, `plan_task`, `claim`, `evidence_file_line` (YAML-style list, verbatim), `suggested_fix`, `disposition`. Add a provenance HTML comment above each block (`<!-- Source: Variant N (...), finding X — merged per Change #N -->`).
5. "Missed by both cards" section: the N-01..N-09 table, with full plan paths.
6. "Severity counts" table: blocking, minor, rejected (outright), partial rejections.
