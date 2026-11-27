# Tier 1 reflection card (UC-1, pre-execution)

Spec: .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/source.md
Plan: .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md
Author of the plan (executor): the orchestrating session, model claude-gw-tier1b (the `sonnet` alias class).
hypothesis_source: inline-fallback (no separate Tier 1 agent was spawned; the orchestrator wrote this card).

## Root-cause / deviation findings

- C1 (Grounded). The plan has a task for each part of the scope change: scenario tests (Tasks 1 to 3, plan lines 29-83), the controlled-run harness and runs (Tasks 4 to 8, plan lines 85-161), the evidence and verdict (Task 9, plan line 163), the gates (Task 10, plan line 180) and the pull request notes (Task 11, plan line 191). The spec asks for exactly these in source.md:43.
- C2 (Grounded). Tasks 1 to 3 put a counting function `questions_for` inside the new test module (plan line 47). The spec warns against "a second copy of the decision rule that only tests itself" (source.md:35). The plan reduces that risk with a rule-text agreement test (Task 2) and a docstring that says the tests check the notes contract and not model behavior (Task 3). The residual risk: acceptance criterion 5 ("regression coverage exercises ... notes") is met in CI only at the notes-contract level, and the behavioral evidence of Tasks 6 to 8 is one-off, not repeatable.
- C3 (Grounded). Task 3 asserts that `refs/create.md` holds the sentence "The issue is filed with the user's flags when the user gave them". It does: src/superclaude/skills/sc-issue-protocol/refs/create.md:38 (Wave 2), and the rule at create.md:86 cites it.
- C4 (Grounded). The 17 existing focused tests that Task 3 must keep passing do pass today: `uv run pytest tests/skills/test_issue_protocol.py -k "contradiction or draft_notes or create_question or additions or evidence"` printed "17 passed, 186 deselected".
- C5 (Grounded). Task 6 and Task 7 rely on `create_issue.py` not existing: src/superclaude/skills/sc-issue-protocol/scripts/ holds only clickup_claim.py, orca_worktree.py and origin_repo.py.
- C6 (Grounded). The plan states that the installed user copy of the skill differs from src/ (plan line 23) and tells the runs to load the src/ copy. The installed copy does differ (a recursive diff of ~/.claude/skills/sc-issue-protocol against src/superclaude/skills/sc-issue-protocol lists SKILL.md, refs/claim.md, refs/create.md and templates/draft-notes.md).
- C7 (INFERRED). Tasks 6 to 8 are eight model runs, each with a worker that runs a codebase analysis, and the plan sets no time or cost ceiling for them. The only abort rule is an unknown `gh` call (plan line 159).
- C8 (INFERRED). If Task 4 finds that questions cannot be observed or writes cannot be blocked, the plan does not say that Tasks 5 to 8 stop and the lead is told. The spec says the estimate "must be revisited" in that case (source.md:35); the plan only says the decision section "says what that limits" (plan line 98).

## Coverage / acceptance findings

- C9 (Grounded). Mechanical coverage is 6 of 13 inferred requirement rows matched (coverage_pct_union 0.4615, S_dev_density 0.5385; artifacts/coverage-matrix.json). The single-task containment rule undercounts rows whose coverage spans several tasks (INF-001, INF-009) or sits in the plan's Constraints section, which is not a matchable task item (INF-003 reopening, INF-005 claim boundary). Read by hand, every unmapped row has coverage somewhere in the plan except the "revisit the estimate" half of INF-007 (see C8).
- C10 (Grounded). The plan keeps the secret-material exception as a qualification and does not remove it (plan line 20, Task 3 and Task 9), as source.md:11 requires.
- C11 (Grounded). The plan opens the pull request with `Refs #834` unless every criterion is delivered with run evidence, and leaves `Fixes #834` to the lead (Task 11), as source.md:43 requires.
- C12 (INFERRED). Task 1 says the reader "drops the empty marker `None`" but does not say it must ignore the HTML comment block inside each section of src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md (lines 7 and 13), whose text contains words that look like items. An implementer may count comment text as items.
- C13 (INFERRED). Task 9 asks for a verdict on "the six acceptance criteria of the issue" quoted "through the summary", but the summary only paraphrases them; the exact criterion text is in the issue body on GitHub, not in source.md.
