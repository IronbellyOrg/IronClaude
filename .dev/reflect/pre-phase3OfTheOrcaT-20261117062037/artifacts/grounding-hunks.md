# Grounding hunks (Wave 1A), UC-1 pre-execution review of the phase 3 plan

Repo root: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp (checkout of origin/master at commit a98541153 plus the plan package).
Codegraph run state: index_state fresh, checked_at 2026-11-17T06:17:54Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp, projectPath the same. Call codegraph only if index_state is fresh; the floor is Grep and Read. Re-Read every range before you cite it.

Plan under review: .dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md
Driving spec (the request): .dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/source.md
Real-traffic evidence behind the request (read-only facts, do not re-read message bodies): the coordinator Run run_93bfa00cae2b has 41 question messages; 39 carry a `payload` that is a JSON STRING with keys dispatchId, taskId, question, options; payload.dispatchId equals the sender `from_handle` of the form `dispatch:<id>` in 39 of 39; 18 of 18 distinct dispatch ids match worker-list rows, and each row carries resource.worktreeId (11 distinct worktrees); 2 messages come from a plain terminal with payload null and a `thread_id` of null.

Code ranges the plan touches (all under src/superclaude/cli/observe/ unless noted):

- parse.py:416-435 `Question` frozen dataclass; docstring says "``body``, ``payload`` and ``to_handle`` are not kept". parse.py:450-458 `_QUESTION_FIELDS` has no payload entry. parse.py:461-541 `parse_questions(obj, namespace, cycle, run_id=None)` builds `Question(namespace=..., created_epoch=..., flags=..., **values)`.
- collector.py:135-156 `Collector.__init__(..., run_id=None, questions=False)` sets `self._questions = bool(questions and run_id)`. collector.py:203-243 `_question_fields` is the one caller of `parse_questions` (line 217). collector.py:125-129 `FixtureSource.read_questions` returns FAILED "no-question-fixture".
- questions.py:27-37 `QuestionRecord(key, question, first_seen_cycle, last_seen_cycle, in_window)`; questions.py:81-137 `merge_questions` keeps records by key `(run_id, qid)`.
- view.py:113-127 `Session` (fields focus, selected, selected_row, filter_text, show_historical, baseline, mark_wall_time, marked, inspector_scroll). view.py:184-192 `QuestionLine(qid, text, created_at, age_seconds, in_window)`. view.py:196-237 `QuestionsPanel` incl. `window(capacity)` (oldest first, cut text). view.py:250-284 `View` (last field `questions: QuestionsPanel | None = None`). view.py:588-742 `_questions_panel`; the per-question line is built at 665-691 as `parts = [shown_age]; ... parts += [text_of(q.subject), QUESTIONS_REASON]`. view.py:762 `build_view`. view.py:992-1038 `apply_key`: keys handled are ctrl_c, up/k, down/j, d/u (inspector), q, e, m, escape (inspector), enter, `/`, h.
- render.py:304-323 `_panel_lines` (clips each `q.text` to the width). render.py:326-430 `screen_lines`; the questions-versus-ledger height budget is at 369-395 (`spare = policy.height - (...)`; `if spare >= 1: gap_part = _panel_lines(panel, policy, spare)` else the one-line summary).
- export.py:89-108 `_question_lines` writes `f"{q.qid} | {q.text}"`; export.py:148-170 `_questions_dict` exports ids, createdAt, ageSeconds, inWindow only; its docstring says "ids, times and counts only (never subject or body)".
- commands.py:67 `QUESTION_GATE_PASSED = True  # owner record: ...  # fmt: skip`; commands.py:168-170 `_questions_on`; commands.py:355 `questions=_questions_on(options)`.
- tests/observe/test_commands.py:746-757 guard test (regex over the source line, existing file, text contains `release-gates.md` and `Task 18`). tests/observe/test_parse.py:586 `test_no_parsed_object_keeps_a_body_payload_or_recipient`. tests/observe/test_session.py:359 `test_no_key_can_reach_the_adapter_or_collector`. tests/observe/golden_release1_surface.json is the pinned R1 surface.
- snapshot.schema.json:65-66 `questions` group description: "No subject, body, handle or payload is ever exported."

Spec statements the plan edits or relies on (.dev/issues/409/bmad/spec-orca-observer/):

- adapter-contract.md:41 "`body`, `payload` and `to_handle` are not kept."
- rendering-rules.md:50 "Lines are listed, not selectable; `m` marks worker rows only." rendering-rules.md:51 the oldest-first cut rule; rendering-rules.md:78 "questions are listed, not individually selectable, in R2".
- release-gates.md section "QUESTION-LINK (before R3)" (added 2026-11-17): dispatch-level link passed; worktree is evidence only.
- acceptance-tests.md: the last row is T56; AC-7 (no one-to-one session and worktree assumption) is row at line 29.
