<!-- provenance: header. Base variant-1-original.md (analyzer) lines 1-4; verdict FAIL is shared by all three cards; confidence is not carried (debate S-002, debate-transcript.md "Points resolved in Round 2"). -->
persona: merged
model_class: n/a (merge of V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus)
verdict: FAIL
confidence: not carried (S-002: self-reported confidence is not merged)
convergence: debate CONVERGED on C-001 to C-015 (28 of 28 diff points); BLOCKED_BY_INVARIANTS on INV-008 and INV-021 (see "Invariant probe additions")

plan: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md (cited as "plan line N")
All code paths below are relative to /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/. Every file:line was re-Read for this merge on 2026-11-17. No tests were run.

findings:

<!-- provenance: C-001 = base variant-1 F1 (kept as is; no refactor-plan change targets it). Same finding: V2 F2, V3 F1. Fix text: round-2-v3.md section 4 item 1 (C-001 + C-015). -->
- C-001 | task 3 | BLOCKING | Gap | src/superclaude/cli/observe/commands.py:218-220
  plan_says: (plan line 62) "pass it as a new keyword `link=` to `Collector` at the call at line 355"
  reality: commands.py has two `Collector(...)` constructions and no others in the package: `run_once` at 218-220 (the `--once` path; width-bound screen at 224-228, else `record_text` at 230) and the interactive loop at 350-356 (line 355 is its `questions=` keyword). The plan names only the second. Constraints (plan line 21) say the record written by `e` and `--once` carries ids and the link state.
  wrong_outcome: `observe --once --run X --questions` never gets `link=True`: the subject "Question" stays on the width-bound screen, the record has no `dispatchId=`/`link=` suffix, and no acceptance check goes through `run_once` (the Task 3 collector test passes `link=True` itself).
  fix: in plan line 62 replace "pass it as a new keyword `link=` to `Collector` at the call at line 355" with "pass it as a new keyword `link=` to both `Collector(...)` calls: `run_once` (line 218) and the interactive loop (line 350)". Add a Task 3 acceptance criterion: "`tests/observe/test_commands.py` has a `--once` test whose fake reply is built with `question_message` and a distinctive `question`: the record contains `dispatchId=` and `link=linked` and not the question text; with `--width 116` the screen contains the question text; the argv log still holds one message call without `--peek` and one `worker-list` call."
  amended_by: INV-016 (linked fixture must use a `dispatch:<id>` sender), INV-017 (assert on the question line, not `dispatchId=` anywhere)
  supported_by: V1 F1, V2 F2, V3 F1; debate final ruling BLOCKING Gap (unanimous); invariant-probe INV-022 ADDRESSED (both sites named)

<!-- provenance: C-002 = base variant-1 F3, regraded MEDIUM -> BLOCKING Regression by refactor-plan.md change 1; acceptance check added by refactor-plan.md change 3 (source V2 F3, with V3's lighter option noted). Fix text: round-2-v3.md section 4 item 2. -->
- C-002 | task 4 (and task 5 AC) | BLOCKING | Regression | src/superclaude/cli/observe/view.py:914
  plan_says: (plan line 75) "Update `QUESTIONS_KEYS_LINE` (line 78) to list `n/p question`"; Constraints (plan line 24) "With the link switch off the observer behaves exactly as it does today"
  reality: view.py:914 picks `KEYS_LINE if panel is None else QUESTIONS_KEYS_LINE`, with no link input, so the constant (view.py:78-81, 107 characters) is the help line of every `--questions` screen, link on or off. Adding "  n/p question" makes it 121 characters: it wraps at widths 116 and 120 through `footer_height` (render.py:362-367) and costs one panel line through `spare` (render.py:382-384). The state is reachable with the rollback constant False and in every questions-on test collector built without `link`. No questions-on screen golden exists; test_render.py:753 compares the screen to the imported constant itself, so it moves with the edit.
  wrong_outcome: with link off the footer advertises dead `n`/`p` keys and the panel loses a line at 116/120 columns, breaking the named constraint, and no existing test catches it.
  fix: in plan line 75 replace "Update `QUESTIONS_KEYS_LINE` (line 78) to list `n/p question`" with "Leave `QUESTIONS_KEYS_LINE` unchanged; add `QUESTIONS_LINK_KEYS_LINE` (the same text plus `n/p question`) and select it in `build_view` (line 914) only when link is on (C-004)". Add an acceptance criterion (refactor-plan change 3, from V2 F3): "with questions on and link off, the view selects `QUESTIONS_KEYS_LINE`, whose text is pinned as a literal, and `screen_lines` at 160, 116 and 80 is byte-identical to a reference captured from the current code before Task 4." Lighter alternative (V3, noted, not chosen): pin only the literal keys-line text and the link-off selection of it.
  amended_by: INV-018 (name the capture step and file for the reference), INV-002 (LOW: link-on keys line can switch mid-session)
  supported_by: V2 F3 (BLOCKING), V1 F3 and V3 F3 (MEDIUM, both conceded BLOCKING in Round 2); debate final ruling BLOCKING Regression; invariant-probe INV-027 ADDRESSED with residual INV-018

<!-- provenance: C-003 = base variant-1 F6, regraded MEDIUM -> BLOCKING Gap by refactor-plan.md change 2; fix replaced with V2 F1's narrower fix; citation corrected from export.py:75-86 (record_text) to export.py:131-145 and :195 per change 2. Fix text: round-2-v3.md section 4 item 3. -->
- C-003 | task 6 | BLOCKING | Gap | src/superclaude/cli/observe/export.py:195
  plan_says: (plan line 103) the snapshot JSON "contains neither the `ask` string nor any dispatch id of a question"
  reality: `snapshot_dict` exports every worker row (export.py:195) and `_row_dict` (export.py:131-145) writes `dispatchId` for each from `_TEXT_FIELDS` (export.py:25-26). The `questions` group (`_questions_dict`, export.py:148-170) carries only `id`, `createdAt`, `ageSeconds`, `inWindow` per item. Task 4's found-worker acceptance case (plan line 78) puts the linked question's dispatch id among the worker rows, and Task 6 forbids changing `snapshot_dict` (plan line 99).
  wrong_outcome: the check cannot pass on the found-worker fixture: the executor either removes legitimate worker ids from the snapshot or leaves the matching worker out of the test, and the check then proves nothing about the found-worker case.
  fix: in the plan line 103 criterion replace "contains neither the `ask` string nor any dispatch id of a question" with "does not contain the `ask` string anywhere, has no dispatch id in its `questions` group, and keeps `rows[].dispatchId` of the linked worker, which the fixture includes". Keep schema validation and the byte-identity with the link-off snapshot.
  supported_by: V2 F1 (BLOCKING, fix adopted), V1 F6 and V3 F5 (MEDIUM, both conceded BLOCKING); debate final ruling BLOCKING Gap (unanimous); invariant-probe INV-032 ADDRESSED

<!-- provenance: C-004 = base variant-1 F2 (kept; no refactor-plan change targets it) merged with debate point A-002 (V1's per-focus table, V2's correction). Same finding: V3 F2. Fix text: round-2-v3.md section 4 item 4. -->
- C-004 | task 4 | MEDIUM | Gap | src/superclaude/cli/observe/collector.py:37-68
  plan_says: (plan line 75) build the desk only when "the link switch was on for this read"; `n`/`p` act "only when the view has a question panel with lines and the desk is on, resetting `inspector_scroll`"
  reality: `CycleResult` (collector.py:37-68), `Session` (view.py:114-127) and `View` (view.py:251-284) carry no link field, and `build_view(result, session, clock)` (view.py:762) has no other input for the switch. `View.desk` exists only once a question is selected, so gating `n` on it means the first `n` can never select. Focus routing: filter focus sends every key to `_filter_key` first (view.py:998-999), where text is appended and `Esc` returns to list (view.py:982-988); `n`/`p` are handled nowhere else; list-focus `Esc` falls through to `replace(session)` (view.py:1038); inspector `Esc` returns to list and resets `inspector_scroll` (view.py:1027-1028). test_session.py:359-393 checks return types and that only `e` exports and only `q`/`ctrl_c` quit; it does not prove `n`/`p` leave the selection unchanged.
  wrong_outcome: the executor gates `n` on `view.desk is not None` (the first press selects nothing) or invents a link flag; per-focus behaviour of `n`/`p`/`Esc` is untested.
  fix: add to Task 4: "Link is on for a read when any line of the question panel has a non-empty `link` (every value Task 2 sets is non-empty)." Replace "only when the view has a question panel with lines and the desk is on, resetting `inspector_scroll`" with "only in list focus, when the view has a question panel with lines and link is on; otherwise a new unchanged Session". Place the new branches inside `if not inspecting:` (view.py:1029). Add the per-focus rule below and one `test_session.py` assertion per focus.

  | Focus | `n` / `p` | `Esc` |
  |---|---|---|
  | list | select next / previous question (only with a panel with lines and link on); otherwise a new unchanged Session | clears `selected_question` |
  | filter | typed into the filter as text (`_filter_key`, view.py:982-984) | leaves the filter only (returns to list, view.py:987-988); selection unchanged |
  | inspector | ignored | returns to list (view.py:1027-1028) and keeps the selection |

  supported_by: V1 F2, V3 F2 (V2 raised it only as INF-008 "partial"); debate final ruling MEDIUM; A-002 resolved in Round 2 (V1, V2, V3 ACCEPT); invariant-probe INV-028, INV-031 ADDRESSED

<!-- provenance: C-005 = base variant-1 F4 (kept; no refactor-plan change targets it). Same finding: V3 F12 (selected-flag part). Fix text: round-2-v3.md section 4 item 5. -->
- C-005 | task 4, 5 | MEDIUM | Gap | src/superclaude/cli/observe/render.py:382-388
  plan_says: (plan line 88) `>` marker on the selected question's line; desk lines "count in the fixed part"; with no room the desk "is replaced by the one line `decision desk hidden: terminal too short`"
  reality: `_panel_lines(panel, policy, capacity)` (render.py:304-323) receives no selection and `QuestionLine` (view.py:185-192) has no selected flag. The fixed part `base` (render.py:377-379) is panel-only; when `spare` (render.py:382-384) falls below 1 the whole panel is replaced by its one-line summary (render.py:385-388).
  wrong_outcome: a tall desk counted in the fixed part pushes `spare` below 1 and the whole question list disappears instead of the desk being replaced; the marker has no data path.
  fix: Task 4: add `selected: bool = False` to `QuestionLine`, set in `build_view` for the selected `(run_id, qid)`. Task 5: replace "they count in the fixed part" with "compute the desk height first; when the list would get no line (`spare < 1`), draw `decision desk hidden: terminal too short` in place of the desk and keep the list; never let the desk collapse the panel".
  amended_by: INV-010 (the notice line itself must be budgeted), INV-013 (selection beyond the shown window), INV-003 (LOW: name the key form)
  supported_by: V1 F4, V3 F12 (NOTE, conceded MEDIUM); debate final ruling MEDIUM

<!-- provenance: C-006 = base variant-1 F5 (kept; no refactor-plan change targets it). Same finding: V3 F11. Fix text: round-2-v3.md section 4 item 6. -->
- C-006 | task 4 | MEDIUM | Gap | src/superclaude/cli/observe/view.py:447
  plan_says: (plan line 75) "find the row in `all_rows` whose `dispatch_id` equals the question's"
  reality: `RowView.dispatch_id` is display text, `text_of(row.dispatch_id)` (view.py:447): an absent id (the truthy UNKNOWN sentinel) reads `unknown` (view.py:324-325), while a source string `unknown` is quoted (view.py:329). The plan's id pattern (plan line 34) accepts the string `unknown`.
  wrong_outcome: a payload `dispatchId` of `unknown` joins a row whose id is absent, showing a false authoritative link; the export prints the sentinel via `q.dispatch_id or "unknown"` (plan line 99).
  fix: in plan line 75 replace "find the row in `all_rows` whose `dispatch_id` equals the question's" with "find the row whose `raw.dispatch_id` equals the question's typed `dispatch_id`; a question whose `dispatch_id` is UNKNOWN never joins, and `QuestionLine.dispatch_id` is `""` for it".
  amended_by: INV-015 (keep the words "in `all_rows`"), INV-014 (LOW: a literal `unknown` id)
  supported_by: V1 F5, V3 F11 (NOTE, conceded MEDIUM), V2 Round 1 BLOCKING (conceded MEDIUM); debate final ruling MEDIUM Gap; invariant-probe INV-024 ADDRESSED

<!-- provenance: C-009 = refactor-plan.md change 4 (source V2 F4; new finding added to base). Fix text: round-2-v3.md section 4 item 7. -->
- C-009 | task 4 | MEDIUM | Gap | plan line 78
  plan_says: (plan line 78) "a linked question whose dispatch is in the rows gives `session_fields` with exactly the nine labels above and the worktree note"; (plan line 75) worktree "through `text_of(row.raw.worktree_id)`" and "a STALE or `as of` note when the worker list is not fresh"
  reality: no acceptance check covers missing values in the desk or the STALE/`as of` note, though Constraints (plan line 23) say unknown is never zero, false or blank. `text_of` of an absent worktree reads bare `unknown`, while the inspector uses `_field` (view.py:380-384), which reads `unknown (absent in source)` (`ABSENT_IN_SOURCE`, view.py:83) for an UNKNOWN value or an absent field.
  wrong_outcome: the checks pass with a desk that shows a missing worktree blank or with different wording from the inspector, or that shows retained worker evidence without its freshness qualification.
  fix: add to the `test_view.py` criterion (plan line 78): "a selected linked question whose worker row lacks fields shows each as `unknown` and an absent `resource.worktreeId` as `unknown (absent in source)`, never blank; a stale or failed worker read adds the STALE or `as of` note." In plan line 75 replace `text_of(row.raw.worktree_id)` with the existing `_field` helper so the absent wording matches the inspector.
  amended_by: INV-001 (a not-reobserved row), INV-012 (no worker read yet)
  supported_by: V2 F4 (raised), V1, V3 (agreed in Round 1); debate final ruling MEDIUM Gap (unanimous)

<!-- provenance: C-011 = refactor-plan.md change 5 (source V3 F6; new finding added to base). Fix text: round-2-v3.md section 4 item 8. -->
- C-011 | task 7 | MEDIUM | Drift | .dev/issues/409/bmad/spec-orca-observer/ARCHITECTURE-SPINE.md:178
  plan_says: (plan line 112) Task 7 edits release-gates.md, SPEC.md, unverified-register.md and acceptance-tests.md only; the plan's export decision (plan line 21) keeps the snapshot unchanged
  reality: AD-18 [ADOPTED] (ARCHITECTURE-SPINE.md:178) says "Stage C (after QUESTION-LINK) adds a `links.py` module and an optional field group"; the CAP-12 row (ARCHITECTURE-SPINE.md:285) maps to "later `links.py`, snapshot field group". The plan puts the payload read in parse.py and the join in view.py and adds no field group. No task amends either line. The AD-18 rule the plan does rest on ("never by editing R1 contracts", line 174) still holds.
  wrong_outcome: built code contradicts the text of an adopted architecture decision; the next reader of the spine looks for `links.py`.
  fix: add to Task 7: "in `ARCHITECTURE-SPINE.md` amend AD-18 (line 178) and the CAP-12 row (line 285) to record that R3 puts the payload read in `parse.py` and the join in `view.py`, adds no `links.py` and no snapshot field group." Add it to Task 7's first criterion.
  supported_by: V3 F6 (raised), V1, V2 (V2 graded BLOCKING in Round 1, conceded MEDIUM); debate final ruling MEDIUM Drift

<!-- provenance: C-012 = refactor-plan.md change 6 (source V3 F8; new finding added to base). Fix text: round-2-v3.md section 4 item 9. -->
- C-012 | task 2 | MEDIUM | Drift | tests/observe/conftest.py:239-271
  plan_says: (plan line 50) add a builder `question_message(...)` "in the observed shape (id, run_id, from_handle, subject, type, thread_id, created_at and a `payload` JSON string ...)"; (plan line 54) the never-kept test asserts no parsed attribute holds the raw body, payload, `to_handle` or `options`
  reality: `make_question_rows` (conftest.py:239-271) already builds rows in the recorded shape with `to_handle` (260), `body` (262), `priority`, `delivery_contract`, `delivered_at` and `payload: None`. The planned builder lists neither `to_handle` nor `body`, though unverified-register.md:33 lists both keys in the observed message row.
  wrong_outcome: a second builder duplicates the first, and the rewritten never-kept test passes on rows that never carried `body` or `to_handle`, proving nothing about dropping them.
  fix: replace the `question_message(...)` builder sentence (plan line 50) with "Add `payload=` and `from_handle=` arguments to `make_question_rows` in `tests/observe/conftest.py` (or a thin `question_message` wrapper over it), so each row keeps `to_handle`, `body`, `priority`, `delivery_contract` and `delivered_at`." Add to the never-kept criterion (plan line 54): "the test row carries a distinctive `body` and `to_handle`."
  amended_by: INV-016 (the default sender `term_synthetic`, conftest.py:259, must not be the linked default)
  supported_by: V3 F8 (raised), V1, V2 (V2 "conditional"); debate final ruling MEDIUM Drift (unanimous)

<!-- provenance: C-013 = refactor-plan.md change 7 (source V3 F9, narrowed in Round 2: line 40 dropped, line-43 R3 clause folded in from X-004). Fix text: round-2-v3.md section 4 item 10. -->
- C-013 | task 1, 4 | MEDIUM | Gap | .dev/issues/409/bmad/spec-orca-observer/rendering-rules.md:21
  plan_says: (plan line 35) Task 1 edits rendering-rules.md lines 43 to 58 and line 78 only; (plan line 75) the selection "survives retention changes"
  reality: rendering-rules.md:21 (global key list) has no `n`/`p`; rendering-rules.md:24 sets the selection rule, which covers questions, that an identity that disappears shows `selected <id> no longer in source window`; the clause in rendering-rules.md:43 "the two-column layout above is design reference / R3 (QUESTION-LINK), not built in R2" sits inside Task 1's range but Task 1 gives no instruction for it, while the plan builds one stacked block (Constraints, plan line 25). The plan does not say what shows when the selected question is evicted (retention bound 1,000, questions.py:125-129). Line 40 ("R2 lists questions without individual selection") stays true for R2 and is not part of this finding.
  wrong_outcome: Task 1's checks pass with all three spec lines stale; after execution the spec says R3 is two-column and lists no question keys, and the evicted-selection case has no defined screen.
  fix: Task 1: also edit `rendering-rules.md` line 21 (add `n`/`p` and list-focus `Esc` with the link-switch qualification), reword the line-43 clause to "R3 builds one stacked Decision Desk block; the two-column layout stays design reference", and state the question form of the line-24 rule. Task 4: when `selected_question` is no longer among the panel's lines, the desk is replaced by `selected <qid> no longer in source window` until the user presses `n`, `p` or `Esc`.
  amended_by: INV-020 (LOW: the same words already mean "left the read window")
  supported_by: V3 F9 (raised), V1 (lines 21, 24), V2 (narrowed); debate final ruling MEDIUM Gap; X-004 folded in; invariant-probe INV-023 ADDRESSED

<!-- provenance: NOTES block. C-007 = base variant-1 F8 (V3 F7 regraded to NOTE; refactor-plan "Changes NOT Being Made" C-007). C-008 = base variant-1 F7 (V2's MEDIUM rejected; refactor-plan C-008). C-010 = V3 F4 (rejected as MEDIUM; refactor-plan C-010). C-014 = V3 F10 (refactor-plan C-014). C-015 = base uncovered INF-009 (refactor-plan C-015, folded into C-001). Marker clash, record-suffix assertion and register line 33 = round-2-v3.md section 4 notes line (V3 F12, V1 Round 1 new risk, S-003). -->
notes:
- C-007 | task 3 | NOTE | Gap | src/superclaude/cli/observe/commands.py:78-94
  Task 3 (plan line 62) says "the module docstring (line 87 to 95)"; commands.py:78-94 is the `HELP` constant. Its sentence "Message bodies are received by this process; subjects are shown, bodies are not kept" (commands.py:92-93) is pinned at tests/observe/test_commands.py:739-742. Fix: say the `HELP` constant; append one sentence that qualifies "subjects are shown" for link on (for example "with QUESTION-LINK on, the question text from the payload is shown on screen in place of the subject; it is not written to the record or snapshot"); keep the pinned sentence and its assertion. Supported by: V1 F8, V3 F7 (MEDIUM, conceded NOTE).
- C-008 | task 1, 2 | NOTE | Gap | plan line 50
  A `dispatchId` that is present but fails the id pattern or is not a string has no named `link` value. Any choice is unlinked (Constraints, plan line 23). Fix: Task 1's contract maps it to `payload has no dispatchId`. Supported by: V1 F7; V2 (MEDIUM, conceded NOTE).
- C-010 | task 4 | NOTE | Drift | plan line 75
  Task 4 changes seven types or functions (`QuestionLine`, `_questions_panel`, `DeskView` (new), `View`, `build_view`, `Session`, `apply_key`), one constant and two test files (corrected by the evidence validator: the draft said five). Splitting it (4a: `QuestionLine` fields, `screen_text`, Session selection, `apply_key`; 4b: `DeskView` and the `build_view` join; Task 6 depends on 4a only) is optional: reviewability, not correctness. Supported by: V3 F4 (MEDIUM, ruled NOTE by all three).
- C-014 | task 7 | NOTE | Necessary | .dev/issues/409/bmad/spec-orca-observer/release-gates.md:13
  The R3 row lists an "Optional owner re-confirm of the post-link default (B or C)". Fix: Task 7 records that B stays the default and the optional re-confirm was not taken. Supported by: V3 F10.
- C-015 | task 3 | NOTE | none | tests/observe/test_commands.py:652-668
  INF-009 (argv log unchanged) is already pinned: one message argv, one `worker-list` call, no `--peek`, with only `QUESTION_GATE_PASSED` monkeypatched, so it runs the link-on path once `QUESTION_LINK_PASSED = True` and C-001 is fixed. The linked-payload argv assertion is folded into C-001's fix. Supported by: V1, V2 (MEDIUM, conceded NOTE), V3 (conceded "only a constraint" was wrong).
- marker clash | task 1, 5 | NOTE | Gap | .dev/issues/409/bmad/spec-orca-observer/rendering-rules.md:25
  Task 5 (plan line 88) uses `>` for the selected question, but `>` already means truncation (rendering-rules.md:25; glyph `truncate`, src/superclaude/cli/observe/terminal.py:32) and `*` means changed (rendering-rules.md:64); a selected-row glyph exists (`▸`, ASCII `@`, terminal.py:31). Fix: Task 1 names a distinct marker. Supported by: V3 F12; round-2-v3.md notes; invariant-probe INV-019 (LOW).
- record-suffix assertion | task 6 | NOTE | Gap | src/superclaude/cli/observe/export.py:101
  With the link on, a payload-less question gets `link="no payload"`, so Task 6 (plan line 99) appends ` | dispatchId=unknown | link=no payload` to its record line (today `{q.qid} | {q.text}`, export.py:101). No existing test breaks (test_commands.py:669-674 counts substrings). Fix: one Task 6 assertion that a payload-less row yields `dispatchId=unknown | link=no payload`. Supported by: V1 Round 1 new risk; V1 and V2 Round 2 searches; invariant-probe INV-033 ADDRESSED.
- register line 33 correction | task 7 | NOTE | none | .dev/issues/409/bmad/spec-orca-observer/unverified-register.md:33
  unverified-register.md:33 exists today (envelope and message-row key list). What exists only after execution is the 39-of-41 payload-shape wording Task 7 adds (plan line 112). Rows T57 to T66 are genuinely future: acceptance-tests.md ends at T56 (line 62). This card does not repeat V3's `checked` claim that line 33 "exists only after execution". Supported by: V2 (S-003 correction), V3 (conceded).

uncovered_requirements:
<!-- provenance: base variant-1 uncovered_requirements, extended with V2 and V3 entries (same INF ids). -->
- INF-001: the `--once` path never gets the link (C-001). V1, V2, V3.
- INF-007: link-off question screen unchanged is not checked (C-002); the stacked-block narrowing is a Necessary deviation (X-004), its stale spec clause is C-013. V2, V3.
- INF-008: command-level link propagation not checked (C-001). V2.
- INF-009: pinned by test_commands.py:652-668 (C-015, NOTE). V1, V2, V3 (corrected).
- INF-010: the snapshot privacy check contradicts the exported worker ids (C-003). V2.
- INF-013: delivery action with no check. V1, V2, V3.

checked:
<!-- provenance: base variant-1 checked list, kept; register-line correction from S-003; re-Read list from this merge. -->
- Confirmed correct (V1, kept): plan line numbers; guard regex and release-gates strings; adapter-contract.md:41; rendering-rules.md:50; SPEC.md:66; unverified-register.md:33 (exists today, see the register note); acceptance-tests.md ending at T56; `Question` field order for new defaults; the test_parse.py:586 rewrite; `Collector` call compatibility; the R1 golden unaffected (panel is None).
- Re-Read for this merge: commands.py 60-99, 210-234, 344-359; view.py 74-85, 110-299, 318-452, 585-694, 760-879, 905-918, 972-1039; render.py 300-395; export.py 20-199; collector.py 30-69, 205-270; parse.py 652-665; questions.py 18-132; sanitize.py 1-48; terminal.py 26-37; adapter.py 55-60; tests/observe/conftest.py 235-274; test_commands.py 648-756; test_session.py 355-396; test_render.py 745-760; rendering-rules.md 1-80; ARCHITECTURE-SPINE.md 174-179, 282-287; release-gates.md 8-15; unverified-register.md 30-35; acceptance-tests.md (Grep for T55-T66); the plan (all 117 lines); Grep of src/superclaude/cli/observe for `Collector(` (two hits: commands.py:218, :350).
- Not run: no tests. Not re-verified here: adapter-contract.md, SPEC.md (cited from V1's checked list).

<!-- provenance: Invariant probe additions. Source invariant-probe.md (Round 2.5) findings table and Summary; not part of refactor-plan.md's 7 changes; added on the orchestrator's instruction for this merge. Smallest fixes: the probe's Summary names fixes for INV-008, INV-015, INV-016, INV-017, INV-018 and the evidence text for INV-021; fixes marked "derived" restate the gap the probe describes as the plan edit that closes it. -->
## Invariant probe additions

The probe tested the plan as it would read after round-2-v3.md section 4 edits 1 to 10. It found 21 UNADDRESSED items: HIGH 2, MEDIUM 11, LOW 8. All HIGH and MEDIUM items are listed here; severities are the probe's (HIGH/MEDIUM), not debate rulings. The 8 LOW items (INV-002, INV-003, INV-005, INV-006, INV-007, INV-014, INV-019, INV-020) are referenced from the findings above where they touch one and are not listed.

### Not converged (convergence: BLOCKED_BY_INVARIANTS)

The debate did not debate or rule on these two. Its CONVERGED status covers C-001 to C-015 only and must not be read as "the 10 edits are sufficient".

- INV-008 | task 1, 5 | probe HIGH | count_divergence | src/superclaude/cli/observe/render.py:317
  assumption: replacing the subject with the question text keeps the line's honesty labels.
  reality: `_panel_lines` clips the whole question line at its end (`clip(q.text, width, policy)`, render.py:317); the line is `age [status] subject reason unknown` (view.py:677-686), and Task 5 only swaps in `screen_text` (plan line 88), built "like `text`" (plan line 75). Real question texts are sentences, so ` reason unknown` is cut off at 80 and 116 columns on almost every linked line. rendering-rules.md:50 says "Only the subject is ever clipped", and Task 1 keeps that paragraph. No acceptance check reaches it.
  smallest fix (probe): clip only the question text so ` reason unknown` (and the bracketed state) stays: in Task 5, build the line from its parts and clip the subject or ask part to the width left after the fixed parts; add a Task 5 criterion that at 80 and 116 columns every linked question line ends with `reason unknown`.
  convergence: BLOCKED_BY_INVARIANTS (not debated)

- INV-021 | plan-wide | probe HIGH | sufficiency_challenge | plan lines 46-117
  assumption: edits 1 to 10 alone make the plan executable and correct. Falsified.
  reality: after the edits these hold: (a) INV-008; (b) edit 6 drops "in `all_rows`" (INV-015); (c) edit 9 drops the observed sender shape (INV-016); (d) edit 2 names no capture step (INV-018); (e) the round-2-v3 notes are not edits, so "module docstring" (C-007), the invalid-`dispatchId` reason (C-008) and the `>` marker stay open. The per-task reviewer passes on every added criterion while (a), (b), INV-009 and INV-011 to INV-013 ship; INV-017's checks pass without the suffix; the suite passes (all test `Collector(...)` calls default to link off).
  smallest fix (probe): apply the fixes of INV-008, INV-015, INV-016, INV-017 and INV-018 below together with edits 1 to 10, and promote the C-007, C-008 and marker notes to plan edits.
  convergence: BLOCKED_BY_INVARIANTS (not debated)

### MEDIUM

- INV-001 | task 4 | probe MEDIUM | state_variables | src/superclaude/cli/observe/parse.py:662
  A worker row missing from this cycle's pages is kept with `reobserved=False` (parse.py:657-662) and its last-known values; the `not reobserved` flag lives in `RowView.flags` (view.py:440-444), not among the desk's nine labels (plan line 75), and C-009's fix adds only a source-level STALE/`as of` note. With `QUESTION_PAGE_CAP` 4 (collector.py:32-34) this is a normal case.
  smallest fix (derived): Task 4 adds `not reobserved` to the desk's notes when the joined row has `reobserved` False, with one `test_view.py` assertion.
- INV-004 | task 1, 2 | probe MEDIUM | guard_conditions | plan line 50
  The sender check runs only when `from_handle` has the form `dispatch:<id>` (plan lines 34, 50); any other sender with a payload `dispatchId` is marked `linked` unchecked. The test default sender is `term_synthetic` (tests/observe/conftest.py:259).
  smallest fix (derived): Task 1 and Task 2 mark a payload from a sender that is not `dispatch:<id>` unlinked with `sender mismatch` (or, if the owner wants such senders linked, state the unchecked case in the contract and desk notes); add one `test_parse.py` case.
- INV-009 | task 2, 5 | probe MEDIUM | count_divergence | plan line 50
  Task 2 cuts `question` to 400 characters with no mark (plan line 50); the desk adds `...` only when its 4-line wrap overflows (plan line 88). At 160 columns 4 lines hold about 640 cells, so a 1,000-character question shows cut at 400 with no mark, against rendering-rules.md:25 (visible truncation mark) and the "full `ask` text" of `DeskView` (plan line 75).
  smallest fix (derived): Task 2 records that the text was cut (or keeps a marker character) and Task 5 shows `...` for it; add a Task 5 criterion with a 1,000-character question at 160 columns.
- INV-010 | task 5 | probe MEDIUM | count_divergence | src/superclaude/cli/observe/render.py:385-388
  The `decision desk hidden: terminal too short` line itself costs a line: with `spare` exactly 1 without the desk, the notice leaves 0 and the panel collapses (render.py:385-388); with `spare` already below 1 the panel and the notice vanish together, which Task 5 forbids ("never silently dropped", plan line 88). C-005's fix does not say whether the notice is budgeted.
  smallest fix (derived): count the notice line in `base` when a question is selected, and state that when the panel collapses to its summary (rendering-rules.md:55) the summary names the hidden desk; add short-height criteria at `spare` 1 and below 1.
- INV-011 | task 2, 4 | probe MEDIUM | collection_boundaries | src/superclaude/cli/observe/sanitize.py:44-48
  A `question` that is `""`, whitespace or only escape codes sanitizes to an empty or blank string (sanitize.py:41-48); Task 4 uses `ask` "when the question has an `ask`" (plan line 75) without excluding a blank one, so the list line and desk text can render blank, against rendering-rules.md:69.
  smallest fix (derived): Task 2 treats a blank sanitized `question` as no `ask` (the subject stays), and Task 4 names the desk wording for a linked question with no text; add one test each.
- INV-012 | task 4 | probe MEDIUM | collection_boundaries | src/superclaude/cli/observe/view.py:767
  With no successful worker-list read (snapshot `None`, view.py:767; `NO_READ_YET`, view.py:874-875) or a NOT_AVAILABLE source (collector.py:250-268), `all_rows` is empty and the desk says the dispatch was not found, as if a complete read lacked it. The PARTIAL note covers only partial coverage (plan line 75).
  smallest fix (derived): Task 4 gives the desk a distinct note when no worker-list read has succeeded (link not checked) instead of "not found"; add one `test_view.py` case.
- INV-013 | task 5 | probe MEDIUM | collection_boundaries | src/superclaude/cli/observe/view.py:221-237
  `QuestionsPanel.window` keeps the oldest `capacity` lines (view.py:221-237, owner decision) and, unlike `View.window` for workers (view.py:286-296), never pulls the selection in. `n` past the last shown question selects an invisible line; the marker never appears. The desk still names the question, so nothing false is shown.
  smallest fix (derived): keep the owner's oldest-first window and add to the cut line (or a note) that the selected question is not shown; add a Task 5 criterion with a selection beyond the shown window.
- INV-015 | task 4 | probe MEDIUM | interaction_effects | src/superclaude/cli/observe/view.py:839-847
  C-006's replacement text drops "in `all_rows`", the only place Task 4 names the row set. Joined over `visible_rows` (view.py:845-847), a linked worker that is `released`/`retained` (hidden by default, view.py:362-365) or outside the `/` filter reads "dispatch not found" though the record and snapshot list it.
  smallest fix (probe): restore "in `all_rows`" in C-006's replacement text: "find the row in `all_rows` whose `raw.dispatch_id` equals ...".
- INV-016 | task 2, 3 | probe MEDIUM | interaction_effects | tests/observe/conftest.py:259
  C-012's fix moves the builder onto `make_question_rows`, whose default sender is `term_synthetic` (conftest.py:259). Linked fixtures that do not pass `from_handle` exercise the unchecked-sender path (INV-004), so the real shape (`dispatch:<id>` equal to `dispatchId`) may never be the linked case under test, and C-001's `--once` test can pass the same way.
  smallest fix (probe): the builder's linked default sender is `dispatch:<dispatchId>`; C-001's and Task 3's linked tests use it.
- INV-017 | task 3, 6 | probe MEDIUM | interaction_effects | src/superclaude/cli/observe/export.py:53-68
  Every worker line of the record starts `dispatchId=` (export.py:53-68), so C-001's "record contains `dispatchId=`" holds with no suffix; with C-003's fixture (linked worker present) Task 6's "contains the dispatch id ... of every question" (plan line 102) holds through the worker line. Only `link=linked` is distinctive.
  smallest fix (probe): assert on the question line itself, `<qid> | ... | dispatchId=<id> | link=<state>` (export.py:101), in C-001's test and in the plan line 102 criterion.
- INV-018 | task 4 | probe MEDIUM | interaction_effects | tests/observe/test_render.py:753
  C-002's byte-for-byte check asks for a reference "captured from the current code before Task 4", but no task captures and stores it (file, widths, height, clock); Tasks 2 and 3 run first and Task 4 writes the test, so the reference can be generated from the new code and the comparison becomes tautological. The closest existing check compares to the imported constant (test_render.py:753).
  smallest fix (probe): name a capture step and file: before Task 4 edits view.py, write the link-off questions-on `screen_lines` at 160, 116 and 80 (with a named height and the fake clock) to a file the plan names, committed before the change.
