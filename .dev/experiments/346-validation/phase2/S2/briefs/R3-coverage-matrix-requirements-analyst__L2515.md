You are building the spec-to-tasklist coverage matrix for a pre-execution review (sc:reflect UC-1, Wave 1B, Step 1B.0). Read-only: do not run uv, python or any command that writes files; write only the one output file below. Assume the plan has mistakes and look for them.

Repo root: /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (paths below relative to it).
- Spec: .dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-053741/source.md
- Tasklist: .dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-053741/TASK-WF-removeTheAnyIssu-20261102-053741.md
- Site lists the tasks rely on: .dev/review-severity-rule/inventory.md (severity), .dev/review-severity-rule/cap-edits.yaml (161 literal cap/at-cap edit rows; already mechanically verified: applying all rows leaves every old absent and every new present, no overlapping rows).
- Earlier blocking findings the plan must have fixed: .dev/reflect/pre-removeTheAnyIssu-20261101225845/adversarial/merged-verdict.md (B-01..B-11) and .dev/reflect/pre-removeTheAnyIssu-20261102042426/REPORT.md (P2-B1..P2-B7).

Algorithm:
- Pass 1: parsed ids match \b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b in the spec; each owns its list item; match exactly by literal token in task text.
- Pass 2: requirement-shaped content outside the parsed items becomes INF-001.. with verbatim quote and spec file:line; match by content-word containment (>= 0.6 inside one task); note whether Constraints carry it.
- Substance: for each R-id, each B-01..B-11 and each P2-B1..P2-B7, does a task deliver it and would its acceptance catch a failure? Check that every acceptance command can pass: grep patterns that would also match text the task keeps or that another task owns, tests reading .claude mirrors, and ordering (tasks run in number order). Cite tasklist line numbers and repo file:line.

Write /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule/.dev/reflect/pre-removeTheAnyIssu-20261102054021/artifacts/coverage-matrix.yaml with: parsed_count, inferred_count, rows (requirement_id, source, quote for INF rows, citation, matched_task_ids, match_method, substance_gaps), prior_findings_check (B-01..B-11, P2-B1..P2-B7: task id, landed yes/no, note), coverage_pct, coverage_pct_union, unmapped_requirements, unmapped_requirements_union. Create the file with a header first, then fill it. Return an 8-line summary listing every substance gap graded blocking (a check that cannot pass or cannot detect its failure, a missing deliverable, wrong behaviour) or minor, with citations.