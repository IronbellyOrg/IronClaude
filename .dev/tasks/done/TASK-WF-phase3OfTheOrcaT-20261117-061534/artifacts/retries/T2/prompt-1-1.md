3031cf07db86649200ac687b1fbdf0e9d0588ae5
Review one task for spec compliance.

Task brief: Task 2 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md ("## Task 2: Parse the question payload behind a link switch", read that section). Acceptance criteria, ids T2.AC1 to T2.AC4 in source order: T2.AC1 tests/observe/test_parse.py has new tests that pin: a linked row gets ask, dispatch_id and link == "linked"; each of the four unlinked reasons gets its exact link text with ask still set when the payload had a readable question; a payload with a dispatchId from a sender that is not dispatch:<id> (for example term_synthetic) reads sender mismatch; a dispatchId that is a number or fails the id pattern reads payload has no dispatchId; a blank, whitespace-only or escape-only question leaves ask UNKNOWN; a 1,000-character question ends in ... at 400 characters; with link=False the fields stay at their defaults and existing tests pass; markup such as [bold] and an escape sequence in question come out as inert text with no ESC, C1 or format character; a payload of nested depth over the interpreter limit, a 70 KiB payload, a list payload and a number payload each give an unlinked row and never raise. T2.AC2 test_no_parsed_object_keeps_a_body_payload_or_recipient (tests/observe/test_parse.py) is rewritten to assert that no attribute of a parsed Question holds the raw body, the raw payload, to_handle or options, and that only ask and dispatch_id carry payload-derived text; the test row carries a distinctive body and to_handle. T2.AC3 tests/observe/test_deep_nesting.py gains one test where a deeply nested payload gives an unlinked row and the question list still parses. T2.AC4 `uv run pytest tests/observe/test_parse.py tests/observe/test_deep_nesting.py tests/observe/test_questions.py -q` passes, and src/superclaude/cli/observe/questions.py needs no change because QuestionRecord stores the Question as it is.
Global constraints: the plan's "## Constraints" and "## Out of scope" content in the plan file above (read that section).
Start sha: 3031cf07db86649200ac687b1fbdf0e9d0588ae5
Diff against the start snapshot: the full diff is in the file /tmp/impl-T2-diff.patch (read it; it covers src/superclaude/cli/observe/parse.py, tests/observe/conftest.py, tests/observe/test_parse.py and tests/observe/test_deep_nesting.py). Codegraph context: index_state: fresh; checked_at: 2026-11-17T07:27:40Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp. Call codegraph only when index_state: fresh, never to widen scope. Dependents of the changed symbols (Q2b, Grep floor and graph): parse_questions has 19 callers (collector.py _question_fields and tests), all call it without the new keyword so they keep working; Question is built only inside parse_questions and in tests; questions.py stores Question objects unchanged.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
