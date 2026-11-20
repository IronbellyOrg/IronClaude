persona: analyzer
model_class: sonnet

# Reviewer 1 card (saved verbatim summary of the agent's return)

Result: plan line numbers and symbols accurate (30+ cites matched). 1 blocking, 6 medium/note.

F1 blocking, contradiction: Task 13 auto-enables (R18, source.md:44) but source.md:60 says switching on stays the owner's decision. Nothing records that R18 supersedes line 60. Affected: Task 13 acceptance "all pass gives enabled: true".
F2 medium, coverage-gap: R20 (source.md:48) "must be verified"; Task 19 only records the question, and its acceptance asks for "the exact value" for R20, which cannot be met.
F3 medium, coverage-gap: source.md:62 lock test, restart test, live-test record unmapped; Task 20 does not list them as open.
F4 medium, ordering: Task 18 depends only on Task 17; Tasks 2, 4, 6 not in its chain; dangling link to Task 4's design note and edit overlap on issue-watcher.md. Fix: Depends on Task 2, 4, 6.
F5 medium, wrong-reference: Task 2 lists issue-watcher.md lines 21, 692, 884; a grep also hit line 15 (not read) [INFERRED].
F6 medium, wrong-reference: `--pipeline none` appears in about 24 files outside .dev; Task 6 names three tests but omits tests/skills/test_issue_protocol.py, tests/commands/test_issue_command.py, templates/next-steps.md, docs/user-guide/commands.md, docs/designs/sc-issue-*.md; its pytest run omits tests/commands. Task 6 does say to grep first, so not blocking.
F7 note, wrong-reference: Task 7 omits argv_events (github.py:218) and argv_comments (223), which call _argv_rest_page and need the repo parameter.

Not read by the reviewer: runner.py body, test_module_boundaries.py, full EDITS_QUERY, the launch-level hook source.
Note: cli.py "line 94" is the decorator line; def is at 95.
