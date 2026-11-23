persona: refactorer
model_class: opus
verdict: FAIL
confidence: 0.80

findings:
- F1 | task 3 | BLOCKING | Gap | src/superclaude/cli/observe/commands.py:218-219
  plan_says: pass `link=` to Collector at the call at line 355
  reality: a second Collector call in run_once (`--once`) at 218-219 is not named; plan Constraints line 21 says the record written by `e` and `--once` carries ids and link state.
  wrong_outcome: with --once the link stays off: no `dispatchId=`/`link=` suffix, `--once --width` draws the subject; no acceptance check goes through run_once.
  fix: pass link=_link_on(options) at both commands.py:218 and :355; add a test_commands check that --once with a payload reply prints link=linked in the record.
- F2 | task 3, 4 | MEDIUM | Gap | collector.py:37-68
  plan_says: build the desk only when the link switch was on for this read; n/p only when the desk is on
  reality: CycleResult has no link field; build_view(result, session, clock) (view.py:762) has no other input for the switch; View.desk exists only once a question is selected, so gating n/p on it means n can never make the first selection.
  fix: define "link on" as some line in panel.lines having a non-empty `link`.
- F3 | task 4 | MEDIUM | Regression | view.py:78-81, 914
  QUESTIONS_KEYS_LINE is used whenever the question panel exists; with link off the footer advertises dead n/p keys, breaking "exactly as today"; tests pass only because test_render.py:753 compares to the constant itself.
  fix: add n/p text only when link is on (a third keys line chosen in build_view).
- F4 | task 4 | MEDIUM | Drift | view.py:113-127, 184-192, 250-284, 762-917, 992-1038
  one task changes five types or functions and two test files with about 13 pinned behaviours; too big to review or roll back as one unit.
  fix: split: 4a QuestionLine fields and screen_text, Session selection, apply_key; 4b DeskView and the build_view join; Task 6 depends only on 4a.
- F5 | task 6 | MEDIUM | Drift | export.py:131-145, 173-190
  the snapshot exports every worker row's dispatchId; a linked question's dispatchId appears through the workers array, so the "no dispatch id" assertion fails on a natural fixture though nothing leaked; the byte-identical check already proves the property.
  fix: drop that clause or limit it to the `questions` group.
- F6 | plan-wide / 7 | MEDIUM | Drift | ARCHITECTURE-SPINE.md:178, 285
  AD-18 [ADOPTED]: "Stage C (after QUESTION-LINK) adds a links.py module and an optional field group"; CAP-12 row maps to "later links.py, snapshot field group"; no task amends either.
  wrong_outcome: built code contradicts an adopted architecture decision.
  fix: add to Task 7 an edit of AD-18 and line 285 recording that R3 puts the join in view.py and the payload read in parse.py with no field group; or move the join into a small links.py.
- F7 | task 3 | MEDIUM | Regression | commands.py:87-93; tests/observe/test_commands.py:739-742
  lines 78-94 are the HELP constant, not the module docstring; it says "subjects are shown, bodies are not kept", pinned at test_commands.py:740; with link on the question text is shown instead of the subject.
  fix: reword the sentence (question text from the payload is shown on screen only; bodies are not kept) and update the assertion at 740.
- F8 | task 2 | MEDIUM | Drift | tests/observe/conftest.py:239-271
  make_question_rows already builds message rows in the recorded shape (to_handle, body, priority, payload None); the planned question_message builder leaves out to_handle and body, so the rewritten never-kept test cannot prove they are dropped.
  fix: add payload= and from_handle= arguments to make_question_rows or a thin wrapper.
- F9 | task 1 | MEDIUM | Gap | rendering-rules.md:21, 24, 43
  line 43 says the two-column layout is "design reference / R3"; line 21 (global key list) has no n/p; line 24 sets the rule that an evicted selected identity shows `selected <id> no longer in source window`; no task addresses these.
  fix: Task 1 rewrites line 43 (R3 builds a stacked block), adds n/p to line 21; Task 4 shows the line 24 note when selected_question is no longer among retained lines.
- F10 | task 7 | NOTE | Necessary | release-gates.md:13; rendering-rules.md:8, 105
  C's contents are not defined (line 8), so the stacked block is a necessary choice; release-gates.md:13 lists an optional owner re-confirm of the post-link default (B or C) that stays unrecorded.
  fix: Task 7 adds one line that B remains the default and the optional re-confirm was not taken.
- F11 | task 4 | NOTE | Gap | view.py:322-329, 447
  RowView.dispatch_id is display text; the id pattern accepts `unknown`; compare row.raw.dispatch_id with Question.dispatch_id instead.
- F12 | task 5 | NOTE | Gap | render.py:304-317; rendering-rules.md:25
  _panel_lines gets no selection input; Task 4 adds no selected flag; `>` already means truncated in this spec. fix: add `selected: bool = False` to QuestionLine, pick another marker, name it in Task 1.

uncovered_requirements:
- INF-001: partly (run_once path; F1).
- INF-007: narrowed to a stacked block; rendering-rules.md:43 stays and the optional post-link re-confirm is unrecorded (F9, F10).
- INF-009: only a constraint.
- INF-013: delivery action, no check.

checked: read plan, source, tier-1 card, grounding hunks; parse.py 410-541, view.py 60-299 and 580-1038, render.py 255-430, export.py 60-190, collector.py 30-249, questions.py 20-138, commands.py 60-94, 160-229, 340-455, conftest.py 235-290, test_commands.py 735-756, test_session.py 359-384, test_golden_contract.py 365-433; spec files rendering-rules.md, release-gates.md, adapter-contract.md 36-45, SPEC.md 55-74, ARCHITECTURE-SPINE.md 174-178 and 282-287, acceptance-tests.md rows T50-T56 and AC-7. Nothing source.md requires is among the deliberate omissions (options, taskId, worktree-wide set, snapshot changes). Not checked: rows T57 to T66 and unverified-register.md line 33 (they exist only after execution). No files written.
