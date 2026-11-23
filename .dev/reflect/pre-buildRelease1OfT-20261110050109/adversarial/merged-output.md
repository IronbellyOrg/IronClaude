<!-- Produced by /sc:adversarial (Step 5 merge-executor) -->
<!-- Base variant: Variant 2 (variant-2-original.md, reviewer-2 card, opus:qa); incorporated: Variant 1 (variant-1-original.md, reviewer-1 card, haiku:analyzer) -->
<!-- Merge date: 2026-11-10 -->

# Merged findings: pre-execution review of the Release 1 plan

- Counts: 16 merged findings (blocking 6, minor 10); 0 card findings rejected outright; 4 partial rejections inside narrowed findings.
- Convergence 0.91 (10 of 11 diff points, threshold 0.80); invariant-gate status BLOCKED_BY_INVARIANTS (INV-001 and INV-002, both HIGH, resolved by incorporation into the M-01 and M-02 fixes, not by a further round).
- Severity definition used: blocking = wrong behaviour, false claim, security or data-loss risk, or a genuinely absent required deliverable or unmet gate; minor = instructed behaviour with a missing assertion, a requirement that applies only to an excluded view, or wording and task bookkeeping (judge ruling 1).

## Judge rulings

1. Severity rule for every finding. Blocking when (a) the plan has wrong behaviour, a false claim, or a security or data-loss risk; or (b) a required deliverable is genuinely absent: a SPEC section 10 test that applies to R0/R1 and that no task maps or excludes, whose required output no task names explicitly; or a SPEC requirement that no task instructs, even through a SPEC section the task tells the executor to follow; or a SPEC gate condition the plan leaves unmet. Minor when the behaviour is instructed (explicitly, or through a referenced SPEC section) and only its assertion is missing, when the requirement applies only to a view the plan excludes, or when the problem is wording or task bookkeeping. Both advocates adopted this rule in Round 2 (X-002).
2. T33 (R1-06 minor vs QA-02 blocking): blocking. SPEC:172 requires the `empty` variant text and SPEC:385 makes it test T33; the plan maps T33 to no task and does not exclude it; plan:75 builds the data only. The Variant 1 advocate conceded in Round 1.
3. R1-04 constraint wording: minor (narrowed). SPEC:337 defines the sanitizer as control-only, SPEC:138 allows `stage.activity` and `.detail` to be shown sanitized and labelled `worker-reported`, and SNAP:103 freezes those fields, so the planned behaviour matches the SPEC; plan:25 and plan:157 only promise more than the design delivers. Redaction of printable secrets would be a new owner requirement, not a plan defect.
4. R1-01 and QA-05 are one finding (M-01). QA-05 carries the T5 citation (SPEC:369). Fault-finder items INV-001 and INV-002 (HIGH, unaddressed) are added to its fix, because the per-call min() rule alone is not sufficient.
5. R1-03 (snapshot only on success): confirmed blocking. Plan:173 writes "after each successful cycle in live mode"; SNAP:79 has one envelope per cycle and SNAP:88 freezes `source.status` as OK, STALE, ERROR or UNKNOWN, so STALE and ERROR can never be published. Plan:118 covers only the collector's in-memory snapshot. Both advocates agreed.
6. QA-09: blocking, narrowed to the inspector half. SPEC:352 requires "help and the inspector say so"; plan:173 covers help; no task instructs the inspector line and no task references SPEC section 9 "Several observers". Both advocates agreed after Round 2.
7. Partial rejections inside narrowed findings (none of the 19 card findings is rejected outright): QA-04's "last good snapshot is not kept" half (plan:118 keeps it); QA-08's NOT AVAILABLE item (plan:182 asserts it) and its STALE/FAILED strip cells (plan:126); QA-11's "no task builds this" for the STALE and FAILED cells (plan:126); QA-12's "undocumented deviation" half (plan:33 gives the reason, and plan:20 cites owner-decisions item 5).

## Merged findings

<!-- Source: Variant 2 (reviewer-2 card), finding QA-05 as base, merged with Variant 1, finding R1-01 — merged per Change #1 -->
### M-01

```yaml
id: M-01
sources: [R1-01, QA-05]
severity: blocking
plan_task: "Tasks 6 and 7"
claim: "The plan bounds each `worker-list` call (DEFAULT_TIMEOUT_S under 15 s) but never the cycle, so five sequential calls can run far past the 15 s budget that T5 requires, and no criterion checks total cycle time."
evidence_file_line:
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:369"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:322"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:104"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:106"
suggested_fix: "Pass a monotonic cycle deadline (15 s from cycle start) and an injectable clock into `poll`; give each call a timeout of min(DEFAULT_TIMEOUT_S, time left) and stop paging when the budget is spent. Name the outcome of a budget-truncated cycle (recommended: pages already parsed are published as PARTIAL with `cycle overran (Ns)` and count as a successful poll for STALE only if at least one page parsed; a cycle with no parsed page is `FAILED (timeout)`), and make T5 (plan:104) and T40 (plan:116) use the same label. Keep binary discovery outside the cycle (M-02) or count it against both the budget and the 5-subprocess cap. Add a fake-clock test in which every call is close to the timeout and the cycle still ends within 15 s."
disposition: "confirmed. Both cards and both advocates agree. QA-05's SPEC:369 citation is the stronger basis. Fix extended with fault-finder items INV-001 (discovery's two 10 s probes, `install_user_setup.py:35` and `:213`) and INV-002 (undefined outcome of a truncated cycle)."
```

<!-- Source: Variant 1 (reviewer-1 card), finding R1-02 — merged per Change #2 -->
### M-02

```yaml
id: M-02
sources: [R1-02]
severity: blocking
plan_task: "Task 6; Constraints; Task 11"
claim: "The constraint that the only live Orca call is `worker-list` is false, because the plan reuses `_find_orca()`, which runs a live `skills list --json` subprocess outside the injectable runner, so T36 (subprocess patched to raise) and the fake-runner tests cannot isolate it."
evidence_file_line:
  - "src/superclaude/cli/install_user_setup.py:209"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:23"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:105"
suggested_fix: "Keep `_find_orca()` (SPEC section 9 prescribes it), but correct plan:23 to name its `skills list --json` probe as the one other approved read-only call. Run discovery once per process before the first cycle, outside the 15 s budget and the 5-call cap, with a stated bound (two candidates at 10 s each can take about 20 s). Inject discovery separately from `Runner` so T36 and the fake-runner tests run without Orca, skip discovery in `--fixture` mode, and say whether the Task 11 argv trace includes the probe."
disposition: "narrowed. Reusing `_find_orca()` is not the defect (SPEC:312 prescribes it); the defect is the false \"only live Orca call\" claim at plan:23 and discovery sitting outside the test seam. Both advocates agreed in Round 2."
```

<!-- Source: Variant 1 (reviewer-1 card), finding R1-03 — merged per Change #3 -->
### M-03

```yaml
id: M-03
sources: [R1-03]
severity: blocking
plan_task: "Tasks 10 and 11"
claim: "`--snapshot` is written only after successful cycles, so the file never publishes the frozen `source.status` values STALE or ERROR and a consumer keeps reading an old snapshot as OK."
evidence_file_line:
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:173"
  - ".dev/issues/409/tuibbs-review/architecture-options.md:79"
  - ".dev/issues/409/tuibbs-review/architecture-options.md:88"
suggested_fix: "Write the snapshot atomically at the end of every live cycle (and on a failed `--once`), keeping last-good rows and `source.observedAt` while updating `source.status` and `source.error`, and rewrite it when the 45 s STALE threshold passes during backoff. Pin the precedence when ERROR and STALE both hold (keeping `source.error`), whether the 45 s boundary is inclusive (SNAP says \"older than 45 s\", SPEC says \"3 intervals ... pass\"), and what a first-cycle failure writes (no rows; page and counts `UNKNOWN`). Test a good poll followed by a failure, and the 45 s threshold."
disposition: "confirmed. Plan:118 keeps the last good snapshot in the collector's memory only; it does not make the file report failure. Fix extended with fault-finder item INV-003."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-01 — merged per Change #4 -->
### M-04

```yaml
id: M-04
sources: [QA-01]
severity: blocking
plan_task: "Tasks 3, 5 and 6"
claim: "The missing, stale and contradictory golden fixtures are created but no contract test consumes them, although SPEC section 7 keeps the R1 data gate closed until all four kinds are pinned in a contract test."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:215"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:222"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:63-65"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:86"
suggested_fix: "Add Task 6 or Task 7 acceptance criteria that run each of the four fixture files through a fake runner and assert: success parses; missing gives `scope unknown`, `reported unknown` and per-field `UNKNOWN`; stale gives old evidence age with the source still OK; contradictory gives duplicates ignored, time-went-back and `changed during read`. Name the contradictory second page file in Task 3's file list and its redaction test, and give its first page `hasMore=true` and a `nextCursor` so a two-page traversal is possible."
disposition: "confirmed. Task 5 (plan:86) tests missing fields by mutating the success data, not by loading `worker_list_missing.json`. Fix extended with fault-finder item INV-005."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-02 as base, merged with Variant 1, finding R1-06 — merged per Change #5 -->
### M-05

```yaml
id: M-05
sources: [R1-06, QA-02]
severity: blocking
plan_task: "Tasks 8 and 9"
claim: "No task builds or pins the T33 empty states (`no observed items in this source window; not proof none exist` for the `empty` variant, and `worker-list returned 0 workers in scope=bound`), although the plan neither maps nor excludes T33."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:172"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:75"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:385"
suggested_fix: "Add both strings to the Task 8 view model, map T33 to Tasks 8 and 9, and add criteria for the `empty` variant (exact text) and for a bound scope with zero rows. Say which minimum row the empty-state line occupies at 80 columns, and what `j`, `k`, Enter and `e` do with zero rows."
disposition: "confirmed; severity decided as blocking (judge ruling 2). R1-06 rated it minor; QA-02's blocking holds because a required SPEC acceptance test and its output are absent. Fix extended with fault-finder item INV-010."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-09 — merged per Change #6 -->
### M-06

```yaml
id: M-06
sources: [QA-09]
severity: blocking
plan_task: "Tasks 9 and 11"
claim: "SPEC section 9 requires both help and the inspector to say that caps are per observer process; Task 11 puts it in `--help` only, its criterion checks only option names, and no task gives the inspector the statement."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:352"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:173"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:177"
suggested_fix: "Add a per-process caps line to the inspector in a source-level section that is reachable even with zero rows (Task 9) and assert it; extend the Task 11 help criterion to check the three help statements (read-only, caps per process with no singleton lock, `--include-remote` not available)."
disposition: "narrowed to the inspector half (help is covered at plan:173); severity raised from the card's minor to blocking (judge ruling 6), agreed by both advocates."
```

<!-- Source: Variant 1 (reviewer-1 card), finding R1-04 — merged per Change #7 -->
### M-07

```yaml
id: M-07
sources: [R1-04]
severity: minor
plan_task: "Constraints; Tasks 2, 9 and 10"
claim: "The constraint that no absolute path, token or credential is ever printed, and Task 10's \"no credentials\" rule, promise more than the design delivers, because worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown and exported after control-only sanitizing."
evidence_file_line:
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:25"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:45"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:157"
suggested_fix: "Narrow plan:25 and plan:157 to what the plan guarantees: nothing raw is committed or logged, no credential or terminal-handle field is exported, and worker free text and stderr are control-sanitized but not redacted and are labelled `worker-reported`. Keep the SNAP-frozen stage fields. If printable-secret redaction is wanted, raise it with the owner as a new requirement."
disposition: "narrowed; severity decided as minor (judge ruling 3). The card's fix of suppressing the stage fields is withdrawn because SNAP:103 freezes them (the Variant 1 advocate withdrew it in Round 2)."
```

<!-- Source: Variant 1 (reviewer-1 card), finding R1-05 — merged per Change #8 -->
### M-08

```yaml
id: M-08
sources: [R1-05]
severity: minor
plan_task: "Task 5"
claim: "Task 5's acceptance criteria use the `duplicate-out-of-order` variant that Task 4 creates, but Task 5 depends only on Task 3."
evidence_file_line:
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:71"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:80"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:88"
suggested_fix: "Add Task 4 to Task 5's dependencies, or use the contradictory golden fixture for that test. Fix it together with the same gap in Task 10 (N-06)."
disposition: "confirmed. Harmless under sequential execution but wrong on reorder or per-task resume (A-004 label left unresolved; outcome agreed)."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-06 as base, merged with Variant 1, finding R1-07 — merged per Change #9 -->
### M-09

```yaml
id: M-09
sources: [R1-07, QA-06]
severity: minor
plan_task: "Tasks 6, 8 and 9"
claim: "The PARTIAL disclosure `(newest first; oldest rows not read; long-running active workers may be among them)` and the `reported T (page k)` form appear in no instruction token list or criterion."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:158"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:103"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:349"
suggested_fix: "Carry the last-read page and the cap-stop reason into the view model, add the full text and the page form to the Task 8 COUNTS tokens, and assert both at view level and in the screen and export tests."
disposition: "confirmed. Minor because Task 8 tells the executor to follow SPEC section 4, which contains the text, and T4 (plan:103) is mapped; only the explicit token and the assertion are missing."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-03 — merged per Change #10 -->
### M-10

```yaml
id: M-10
sources: [QA-03]
severity: minor
plan_task: "Task 6"
claim: "Task 6 names `PARTIAL (empty page k)`, `reported T1-T2 (changed during read)` and `collected n / reported T (mismatch)`, but its acceptance criteria pin only T4 and T18."
evidence_file_line:
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:100-106"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:158"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:331"
suggested_fix: "Add fake-runner criteria for the empty-page, total-changed and mismatch outcomes."
disposition: "narrowed; severity lowered from the card's blocking to minor. Plan:97 instructs all three outcomes; only the assertions are missing (both advocates agreed)."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-04 — merged per Change #11 -->
### M-11

```yaml
id: M-11
sources: [QA-04]
severity: minor
plan_task: "Task 6"
claim: "No Task 6 criterion pins that `poll` turns a missing required field (`result`, `result.workers`, `result.page.hasMore`) or a second JSON envelope into `FAILED (shape)`; Task 5 tests `ShapeError` only at parser level."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:378"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:325"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:118"
suggested_fix: "Add a Task 6 criterion mapping a shape error and a two-envelope response to `FAILED (shape)`."
disposition: "narrowed; severity lowered from blocking to minor. The \"last good snapshot is kept\" half is rejected: plan:118 already requires \"A failed cycle keeps the previous snapshot readable and marks it with the failure\". The card's own citation of plan:118 refutes that half; the citation is kept verbatim."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-07 — merged per Change #12 -->
### M-12

```yaml
id: M-12
sources: [QA-07]
severity: minor
plan_task: "Tasks 8 and 9"
claim: "T31 (cost renders `cost unavailable`, never `$0`) is not excluded, and no acceptance criterion pins it, although Task 8 lists the `cost unavailable` token."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:377"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:129-136"
suggested_fix: "Add a Task 8 criterion: the COUNTS tokens contain `cost unavailable` and no variant's output contains `$0`."
disposition: "confirmed. Minor because the token is instructed explicitly at plan:126."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-08 — merged per Change #13 -->
### M-13

```yaml
id: M-13
sources: [QA-08]
severity: minor
plan_task: "Task 8"
claim: "Several Task 8 texts are instructed but unpinned: `not reobserved` for a dropped row (second half of T41), the `selected <id> no longer in source window` placeholder, `filter <expr>: k of n collected`, `scope unknown`, `one Run only`, and the `NOT POLLED` strip cell."
evidence_file_line:
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:135"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:393"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:55"
suggested_fix: "Add Task 8 criteria for each of these texts, and decide which applies to a worker row that drops out of the source: the placeholder (plan:126) or `not reobserved` (SPEC:349); as written one of them is unreachable."
disposition: "narrowed. The NOT AVAILABLE item is rejected (plan:182 asserts it) and the STALE/FAILED strip cells are defined at plan:126. Fix extended with fault-finder item INV-006."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-10 — merged per Change #14 -->
### M-14

```yaml
id: M-14
sources: [QA-10]
severity: minor
plan_task: "Task 8"
claim: "SPEC section 9 says the header shows `read k of N Runs since start` and T45 pins it with the start-up view choice, but the plan neither builds it nor lists T45 as excluded."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:355"
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:397"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126"
suggested_fix: "Add T45 and the header token to the plan's stated exclusions with the reason (SPEC section 2 ties the token to the B view, and release 1 builds only the A ledger), or add the token and a never-switches test."
disposition: "narrowed. SPEC:45 adds the token only \"In the B view\", which plan:21 excludes, so it is scope-ambiguous for release 1; the gap is the missing exclusion statement."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-11 — merged per Change #15 -->
### M-15

```yaml
id: M-15
sources: [QA-11]
severity: minor
plan_task: "Tasks 7, 8 and 9"
claim: "SPEC section 4 requires that when the source is STALE every value keeps its last-known reading with an `as of HH:MM:SS` qualifier; the plan has only the header `as of <HH:MM>`, and no criterion renders a STALE or FAILED snapshot through the view."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:154"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:116"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:129-136"
suggested_fix: "Add a Task 8 criterion: a STALE snapshot renders the `STALE <age>` cell and the `as of HH:MM:SS` qualifier on last-known values; a FAILED snapshot renders `FAILED (exit 2) 1m`."
disposition: "narrowed. The STALE and FAILED strip cells are already defined at plan:126 and T26 (plan:148) renders STALE as a word; only the per-value qualifier and a view-level render test are missing."
```

<!-- Source: Variant 2 (reviewer-2 card), finding QA-12 — merged per Change #16 -->
### M-16

```yaml
id: M-16
sources: [QA-12]
severity: minor
plan_task: "Task 1"
claim: "Task 1's spike criterion can be met by an artifact that records a failure, so it never fails on its own."
evidence_file_line:
  - ".dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:298"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:33"
  - ".dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:39"
suggested_fix: "State that a recorded spike failure leaves Task 1 blocked, not passed, and assert a minimum number of Live repaints and decoded keys in one pty run."
disposition: "narrowed. The \"undocumented deviation from the Textual switch rule\" half is rejected: plan:33 gives the reason inline (\"switching to Textual changes the stack the owner confirmed\"), plan:20 cites owner-decisions items 1 and 5, and item 5 confirmed Python + Rich after the SPEC was written."
```

## Missed by both cards

<!-- Source: refactor-plan.md Change #17 (orchestrator-verified citations, not card citations) -->

| N | Item | Severity | Evidence (verified) | Suggested fix |
|---|------|----------|---------------------|---------------|
| N-01 | T16 scenario matrix (sessions x widths, with `k of n` and `x/y shown` arithmetic) is neither mapped nor excluded; fixtures are fixed-size (`base` about 12 rows) | blocking | `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:373`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:71`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:142` | Map T16 to Task 9 for the 50/80/100-row x 160/116/80 part (the orchestrators axis has no R1 source and can be listed as excluded); add sized fixtures and a fixed terminal height so `x/y shown` can be asserted (INV-012). |
| N-02 | T22's visible texts (`k duplicate rows ignored`, `order unknown`, `conflict (time went back)`) are tested only in the model, never shown by the view | blocking | `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:375`; `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:328`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:88`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126` | Add the three texts to the Task 8 view model and map T22's display half to Task 8 with a criterion. |
| N-03 | Binary discovery can take about 20 s (two candidates, 10 s each) and adds 1-2 subprocesses; the plan does not say whether it runs once or per cycle (INV-001) | blocking (tracked in M-01 and M-02) | `src/superclaude/cli/install_user_setup.py:35`; `src/superclaude/cli/install_user_setup.py:213`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97`; `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:322` | See M-01 and M-02. |
| N-04 | The outcome of a cycle cut off by the budget is undefined, and T5 says `FAILED (timeout)` while T40 says `cycle overran` (INV-002) | blocking (tracked in M-01) | `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:104`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:116`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:112`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:118` | See M-01. |
| N-05 | Exports are built from the same view model that hides historical rows and applies the local filter; nothing pins that exports carry every collected row | minor | `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:126`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:157`; `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md:189` | State that `export_text` and `export_json` include every collected row regardless of `h` and the filter, and add a regression test. |
| N-06 | Task 10 depends only on Task 8, but its T27/T48 criterion needs the Task 9 renderer | minor | `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:155`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:161` | Add Task 9 to Task 10's dependencies (fix with M-08). |
| N-07 | The contradictory "second page file" is not named in Task 3's file list or redaction check, and a single real capture has no `nextCursor` (INV-005) | minor (tracked in M-04) | `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:60`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:63` | See M-04. |
| N-08 | Guard gaps: `hasMore=true` with a missing `nextCursor`, uncaught errors ending the daemon poll thread, and stdout a tty while stdin is not (INV-009) | minor | `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:97`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:112`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:173`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:33` | End paging as PARTIAL on a missing or repeated cursor; catch and report every cycle exception as `FAILED (<reason>)`; check stdin as well as stdout before entering interactive mode. |
| N-09 | The `e` export writes a predictable, second-resolution file name in the current directory without exclusive creation (two presses in one second collide; a planted symlink is followed) (INV-011) | minor | `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:173`; `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md:157` | Create the file exclusively (or add a unique suffix) with mode 0600. |

## Severity counts

| Category | Count | Entries |
|---|---|---|
| Blocking | 6 | M-01, M-02, M-03, M-04, M-05, M-06 |
| Minor | 10 | M-07, M-08, M-09, M-10, M-11, M-12, M-13, M-14, M-15, M-16 |
| Rejected outright | 0 | none |
| Partial rejections | 4 | QA-04 (in M-11), QA-08 (in M-13), QA-11 (in M-15), QA-12 (in M-16) |
