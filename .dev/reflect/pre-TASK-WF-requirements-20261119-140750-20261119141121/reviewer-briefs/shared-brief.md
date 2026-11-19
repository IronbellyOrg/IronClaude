# Shared reviewer brief: plan v4 (UC-1 pre-execution review)

Repo root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb. All paths below are relative to it.

Plan under review: `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md` (28 tasks, 8 phases). Driving spec: `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/source.md` (requirements R1 to R33; R33 is new and adopts the remediation proposal). Grounding note: `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/artifacts/codegraph-grounding.md`.

Context: this is the fourth version of the plan. Version 3 was reviewed on 2026-11-19; its register Q-1 to Q-10 and the validated remediation are in `.dev/remediation/watcher-plan-v3/remediation-proposal.md` (read its sections for Q-1 to Q-10, "Decisions the owner must make" and "What changes in the plan task list"). The owner answered the six decisions: ship gate closed (constant), run the updatedAt observation, self-approval warn-only, add `*.config/superclaude*` to the guard tamper tokens, all four pipelines end at In review, extra guard refusals confirmed. The old v3 review is at `.dev/reflect/pre-TASK-WF-requirements-20261119-012839-20261119013121/adversarial/merged-output.md`.

Your job (read-only; do not edit any file except your own card):
1. Check that every finding Q-1 to Q-10 and every decision of the remediation proposal is now implemented in the right task with an acceptance check that would fail if it were missing. Report each as FIXED, PARTIAL or MISSING with plan line evidence.
2. Check every requirement R1 to R33 in source.md maps to at least one task (coverage), and that no task is orphaned.
3. Look for new defects: wrong dependencies or ordering (same-file edits), tasks that cannot pass their own acceptance, a safety boundary left open (writes to GitHub by launched agents, approval provenance, ship gate bypass), false or unsupported claims about the code. Verify claims by reading the real files (guard script, cycle.py, predicates.py, launch.py, github.py, tests). Re-Read every file:line before you cite it.
4. Grade each finding by consequence: Blocking only when it changes a named decision, a required behaviour or acceptance check (Decision), a required deliverable is absent (Missing), or following the plan would break a safety boundary (Safety). Everything else is Medium (real weakness) or Note (form only). Do not invent findings to fill a quota; a zero-finding result is valid if you say what you checked.
5. Tag unsupported claims `[INFERRED]`.

Write your card to the path named in your assignment: header lines `persona:` and `model_class:`, then a short summary, then findings (id, grade, task, evidence with file:line, fix), then `Checked:` and `Not checked:` lines. Keep it under 120 lines. Return only the card path and a 3-line summary.
