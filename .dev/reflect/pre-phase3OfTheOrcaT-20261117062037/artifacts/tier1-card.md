# Tier 1 reflection card (Wave 1), UC-1 pre-execution

Plan: .dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md (7 tasks, 5 phases, depth standard)
Spec: .dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/source.md (one inline prompt; no labeled requirement ids)

## Extraction

Pass 1 (deterministic labeled ids): 0 rows. Pass 2 (inference, quote-pinned, citation source.md:1): 13 rows.
parsed_count 0, inferred_count 13, so the parse-density guard fires: coverage_degraded: parsed-sparse (table-wide pre-filter, forbids a Tier 1 stop).

## Coverage matrix (union set)

| Id | Quote from source.md (verbatim) | Mapped to | Result |
|---|---|---|---|
| INF-001 | "parse each coordinator question message's payload, a JSON string holding dispatchId, taskId, question and options; show payload.question (sanitized, never raw) instead of the generic subject 'Question'" | Task 2 (parse), Task 4 (screen_text), Task 5 (draw) | covered |
| INF-002 | "a payload that is not valid JSON or has no dispatchId reads as unlinked, never an error" | Task 2 | covered |
| INF-003 | "show the one linked session, found by joining payload.dispatchId to the worker-list row" | Task 4, Task 5 | covered |
| INF-004 | "that row's resource.worktreeId shown as evidence only, never as an inferred set of affected sessions" | Task 4, Task 5, Constraints | covered |
| INF-005 | "a message with no dispatchId reads 'affected scope unknown'" | Task 4, Task 5 | covered |
| INF-006 | "no one-to-one session and worktree assumption (AC-7)" | Task 4 (shared-worktree test) | covered |
| INF-007 | "the Decision Desk composition from rendering-rules.md (C) behind the gate" | Task 1, Task 4, Task 5 | covered with a deliberate narrowing: one stacked block, the two-column C layout is listed out of scope |
| INF-008 | "Gate status: QUESTION-LINK passed 2026-11-17 at dispatch level, see ... release-gates.md section QUESTION-LINK" | Task 3 (guard), Task 7 | covered |
| INF-009 | "Read-only: no write path into Orca; keep the forbidden verb set" | Constraints only; no task acceptance check asserts the argv log | covered by constraint, weak check |
| INF-010 | "the snapshot and export carry no message bodies, prompts or credentials, so check whether question text may be exported and keep it out of the snapshot unless the owner says otherwise" | Task 6, Constraints | covered |
| INF-011 | "Contract: ... SPEC.md (CAP-12), rendering-rules.md, adapter-contract.md, acceptance-tests.md, unverified-register.md" | Task 1, Task 7 | covered |
| INF-012 | "Code: src/superclaude/cli/observe/ (questions.py, collector.py, adapter.py, view.py, render.py, parse.py, export.py) and tests/observe/" | Tasks 2 to 6 | covered; questions.py and adapter.py are deliberately untouched |
| INF-013 | "Rebase on origin/master before pushing." | Constraints | covered by constraint (delivery action, not a code task) |

coverage_pct (parsed-only): null (no parsed rows). coverage_pct_union: 13/13 mapped, 1 with a deliberate narrowing (INF-007), 1 weak check (INF-009).

## Signals

S_scope 7 tasks; S_domains 3 (code in src/, tests in tests/, docs in .dev/); S_dev_density: unmapped union rows 0/13.
Rubric note: coverage_degraded (parsed-sparse) and S_domains >= 3 each force Tier 2 (rules pre-filter and 4).

## Tier 1 findings (for the reviewers to confirm or reject)

- T1-a: Task 2 adds a `link` argument to `parse_questions` and Task 3 passes it from `Collector`; the one src caller is `Collector._question_fields`.
- T1-b: Task 4 touches view.py `Session`, `QuestionLine`, `View`, `build_view`, `apply_key`; every one is read by render.py or commands.py.
- T1-c: The guard line in commands.py is pinned by a regex test; the plan tells the executor how to keep it on one line.
- T1-d: Task 6 keeps the snapshot byte-identical; acceptance asserts it.
- T1-e: INF-009 has only a constraint, no acceptance check on the argv log.
