persona: analyzer
model_class: sonnet
verdict: FAIL
confidence: 0.65

findings:
- F1 | task 3 | BLOCKING | Gap | src/superclaude/cli/observe/commands.py:218
  plan_says: pass `link=` to `Collector` at the call at line 355
  reality: commands.py has two Collector constructions: run_once at 218-220 (the `--once` path, with the width-bound screen at 224-228 and the record from record_text) and run_interactive at 350-356. The plan names only the second.
  wrong_outcome: `observe --once --run X --questions` never gets link=True: subject "Question" stays, no ask, no dispatch id, no link state; contradicts the plan's own constraint about the `--once` record.
  fix: pass `link=_link_on(options)` at both calls; add a test_commands test that `--once` with a linked reply gives `dispatchId=` and `link=linked` in the record and a screen showing the ask text.
- F2 | task 4 | MEDIUM | Gap | view.py:114-127, 251-284, 588-691
  plan_says: build the desk only when "the link switch was on for this read"; n/p only "when the desk is on"
  reality: CycleResult (collector.py:38-68), Session and View carry no link field; View.desk is None until a question is selected, so it cannot gate the first `n`.
  wrong_outcome: executor gates `n` on `view.desk is not None` (first press selects nothing) or invents a flag.
  fix: name the source: add `question_link: bool` to CycleResult and _carry, or define link-on as any QuestionLine.link != "".
- F3 | task 4 and 5 | MEDIUM | Regression | view.py:78-81
  plan_says: update QUESTIONS_KEYS_LINE to list `n/p question`; link off behaves exactly as today
  reality: that constant is the help line for every --questions screen (view.py:914), about 107 chars; adding the text makes about 121 chars = 2 lines at width 116 or 120; footer_height (render.py:362-367) counts it and `spare` (382-384) drops one.
  wrong_outcome: link off advertises dead keys and loses a screen line at width 116/120; height-pinned tests such as tests/observe/test_render.py:660 may change [INFERRED].
  fix: separate link-on help line; or state the link-off help is unchanged.
- F4 | task 5 | MEDIUM | Gap | render.py:304-323, 369-395
  plan_says: `>` marker on the selected question's line; desk lines count in the fixed part; no room replaces the desk by one line
  reality: `_panel_lines(panel, policy, capacity)` gets no selection; QuestionLine has no selected flag; base (377-379) is panel-only; `spare >= 1` else the whole panel collapses to the one-line summary (385-388).
  wrong_outcome: a tall desk pushes spare below 1 and the whole question list disappears instead of the desk being replaced.
  fix: add `selected: bool` to QuestionLine (or pass the key); compute desk height first, replace it with the one-line notice when spare would fall below 1, never remove the list.
- F5 | task 4 | MEDIUM | Gap | view.py:322-330, 447
  plan_says: find the row whose `dispatch_id` equals the question's; worktree through text_of(row.raw.worktree_id)
  reality: RowView.dispatch_id is display text (text_of): an absent id reads "unknown"; the id pattern accepts the string `unknown`; UNKNOWN is a truthy sentinel; _field() (380-384) gives "unknown (absent in source)" for an absent worktree.
  wrong_outcome: payload dispatchId `unknown` can join an identity-unknown row; export prints the sentinel via `q.dispatch_id or "unknown"`; desk shows bare "unknown" for the worktree.
  fix: join on typed `row.raw.dispatch_id` skipping UNKNOWN; map UNKNOWN to "" in QuestionLine; use _field for the worktree.
- F6 | task 6 | MEDIUM | Gap | export.py:75-86
  plan_says: snapshot contains no dispatch id of a question
  reality: snapshot and record list every worker row with dispatchId (_row_dict 131-145); in real traffic 18 of 18 question dispatch ids match worker rows.
  wrong_outcome: a test with matching fixture rows fails on the row ids, or the executor weakens the assertion.
  fix: use dispatch ids absent from the rows, or assert only the `questions` group plus byte-identity with the link-off snapshot.
- F7 | task 2 | NOTE | Gap | plan line 50
  no reason named for a dispatchId present but failing the pattern or not a string; fix: map to `payload has no dispatchId`.
- F8 | task 3 | NOTE | Gap | commands.py:78-94, tests/observe/test_commands.py:739-742
  plan says "module docstring (line 87 to 95)"; those lines are the HELP string; test pins "Message bodies are received by this process; subjects are shown, bodies are not kept". fix: say HELP string, append a sentence, do not edit the pinned one.

uncovered_requirements:
- INF-001: --once path never gets the link (F1).
- INF-009: no acceptance check on the argv log for the link path (only existing tests test_commands.py:652-667).
- INF-013: delivery action with no check.

checked: read plan, source, grounding hunks, tier 1 card; Read parse.py, sanitize.py, collector.py, questions.py, view.py, render.py, export.py, commands.py, spec files, test_parse.py:586, test_session.py:359, test_commands.py:600-756, test_render.py:455-760, test_golden_contract.py:380-560, conftest.py:235-314. Confirmed correct: plan line numbers, guard regex and release-gates strings, adapter-contract.md:41, rendering-rules.md:50, SPEC.md:66, unverified-register.md:33, acceptance-tests.md ending at T56, Question field order for new defaults, the test_parse.py:586 rewrite, Collector call compatibility, R1 golden unaffected (panel is None). No tests run.
