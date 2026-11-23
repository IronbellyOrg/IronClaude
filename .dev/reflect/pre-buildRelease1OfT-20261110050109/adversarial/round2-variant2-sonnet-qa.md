# Round 2 rebuttal: Variant 2 advocate (sonnet:qa)

Persisted verbatim by the debate-orchestrator from the advocate's returned text.

## Response to criticisms

1. **QA-04 (confirm what survives).** P:118 keeps the previous snapshot after a failed cycle. P:86 covers `ShapeError` at the parser. What survives is narrow. No Task 6 criterion (P:100-106) pins that `poll` turns a missing `result`, `result.workers` or `result.page.hasMore`, or a second JSON envelope, into `FAILED (shape)`. P:97 names the label in the instruction, and T32 is cited there. Minor, an unpinned detail.

2. **QA-08.** Conceded for the pinned items. P:182 asserts `NOT AVAILABLE`, and P:126 lists the strip cells. These survive, because P:126 instructs them but P:129-136 never asserts them:
   - `not reobserved`, the second half of T41. P:135 covers only the baseline.
   - The `selected <id> no longer in source window` placeholder.
   - The `scope unknown` and `one Run only` header text.
   - The filter text `filter <expr>: k of n collected`.

   Minor.

3. **QA-11.** Conceded almost entirely. P:126 has `as of <HH:MM>` in the header, which meets S:334's "qualified `as of`". P:148 renders STALE as a word. Only the seconds-level per-value qualifier is unbuilt. I downgrade it to a nit.

4. **QA-12.** The deviation half is rejected. P:33 gives its reason inline, and P:20 cites owner-decisions item 5. Only a wording conflict survives. P:39 lets the artifact record "blocked pending the owner" as a valid decision, so the criterion can pass on a recorded fail. P:33 says the task stops as blocked. The plan should say that a recorded fail leaves Task 1 blocked, not passed. Minor.

## Final positions on split points

**R1-04: minor (narrowed), not blocking.**
- N:77 and N:103 read together mean "no credentials" governs which fields exist. The same SNAP freezes `stage.detail` and `stage.activity`, so it cannot also intend to scrub their content.
- P:163 tests exactly that reading: it asserts that no terminal handle or ownership field name appears.
- P:157 does over-state. A free-text field cannot guarantee "no credentials" when P:45 strips only controls.
- A printable-credential detector is not in S:337, whose sanitizer is control-only. It would be a speculative guess-based addition.
- The fix is wording: "no credential field; free-text fields are control-sanitized only". P:60 already shows the author knows free text is the risk, since it redacts it in fixtures.
- That is wording, with no wrong behaviour in the specified code.

**QA-09: I concede. Blocking, narrowed to the inspector half.**
- S:352 requires that "help and the inspector say so".
- P:173 assigns the help text.
- P:142's inspector spec ("lists every field untruncated", plus failed-poll stderr) has no caps statement. P:126 has none either.
- This meets the severity definition of a missing required deliverable.
- This is consistent with QA-10, which I keep minor. S:45 ties `read k of N Runs since start` to the B view and the R2 rotation set, so it is not clearly R1.
- The fix is one inspector line plus one assertion.

## Final assessment of missed items

- **(a) T16: holds, blocking.**
  - S:373 names T16 as 27 renders, and the plan neither cites nor excludes it. P:71 sizes `base` at about 12 rows, and no task builds 50, 80 or 100-row fixtures.
  - The opponent's point is right: synthetic worker rows can exercise sessions x widths with `k of n` and `x/y shown`, and T17 is the per-owner test.
  - I concede the orchestrators axis (5, 8, 10) has no R1 source, so the plan may legitimately scale only the sessions x widths part.
  - The overflow behaviour is instructed (P:142), but nothing pins the matrix and arithmetic.
- **(b) T22 view texts: holds, blocking.**
  - P:88 tests the flags and counters on the model only.
  - Neither P:126 (the T-list omits T22) nor P:142 assigns `k duplicate rows ignored`, `order unknown` or `conflict (time went back)` to any screen. S:375 says T22 "shows" them, and S:328 requires `k duplicate rows ignored`.
  - The T22 row of that test is unassigned at view or render level.
- **(c) Export versus hidden rows: holds, minor.**
  - I withdraw my Round 1 "REJECT" of A-003 as an assumption and make it a minor finding.
  - P:157 says "every ledger row", so the plan states the intent. S:189 forbids deleting rows from the snapshot.
  - The risk is that `export_*(view)` inherits the hidden-historical and local-filter state, because P:161 requires a shared `ViewModel`.
  - No data loss is specified. Pin it with an all-collected-rows regression test.

## Updated per-finding changes

| id | Round 1 | Final | Reason |
|---|---|---|---|
| QA-09 | minor | blocking (inspector half only) | S:352 requires the statement in the inspector, and neither P:126 nor P:142 assigns it. |
| QA-11 | minor, narrowed | minor, nit | P:126 `as of <HH:MM>` meets S:334; only the seconds-level qualifier is unbuilt. |
| QA-08 | minor, narrowed | minor, narrowed further | Surviving items are `not reobserved`, the placeholder, `scope unknown` / `one Run only` and the filter text. |
| QA-12 | minor, narrowed | minor, wording | The surviving point is that P:39 allows a recorded fail while P:33 says stop. |
| R1-04 | minor | minor (unchanged) | The fix is to qualify the P:157 sentence; redaction is not required by the SPEC. |
| T16 (new) | missed | blocking | S:373 names it; the plan neither cites it nor excludes it. |
| T22 view texts (new) | missed | blocking | The plan covers the model only (P:88); the display texts are unassigned. |
| Export vs hidden rows (A-003, new) | rejected assumption | minor | P:157 says "every ledger row"; the shared view-model dependency needs a regression test. |

I made no edits, and I checked the plan, SPEC and SNAP text only. I did not run code.
