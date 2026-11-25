# Codegraph grounding

## Run state

- index_state: foreign for this plan. `codegraph_status` (checked 2026-11-25) shows an index of 3673 files for the Coordinator worktree, last indexed 2026-11-24T20:57:53Z, 0 changes pending. Every file this plan changes is a Markdown file or a small generator script under `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` on branch `ironbelly/orch-ledger-20261122` of the main checkout (`git rev-parse --show-toplevel` there: `/home/coder/workspaces/IronClaude`), a different working tree. None of those files is in this worktree's index.
- token: `graph:foreign`
- access mode: Grep, Glob and Read only (the permanent floor).

## Resolved symbols

Read directly from the target files (not graph rows):

- `agent1/tools/plan_common.py`: constants `L726` (line 10) and `GOAL` (line 28).
- `agent1/tools/render.py`: f-string template of `render_feature`, the "Before step 1" paragraph (line 137).
- `agent1/tools/plan_e01.py`: story data, the `done` item at line 65.
- `agent1/tools/plan_unique.py`: story data for EPIC-12-STORY-05, `done` list at line 289; `GOAL` is used as a link at line 240 (EPIC-12-STORY-01).
- Paths below are relative to `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/`.

## Dependents

Plain-text search (Grep, whole main checkout, run 2026-11-25):

- `GOAL` (plan_common.py) is imported by `plan_e01.py` and `plan_unique.py`; it reaches the rendered output only through plan_unique.py:240, i.e. one file: `agent1/issue-drafts/EPIC-12-STORY-01-coordinator-needs-as-decisions.md` (the `- Owner goal:` bullet).
- `L726` (plan_common.py) is used by 9 rendered drafts.
- The render.py paragraph is rendered into 73 of the 89 drafts (every story; none of the 15 epics).
- `agent1/RELEASE-PLAN.md` line 69 and `.dev/issues/727/issue-body.md` are hand-held copies that no generator touches.

## Pre-check

Read-only check against the main checkout (Grep, Read; no new readiness check), 2026-11-25:

- Files named by tasks: all 8 targets exist (plan_common.py, render.py, plan_e01.py, plan_unique.py, RELEASE-PLAN.md, PIPELINE-RECORD.md, `.dev/issues/727/issue-body.md`, and the `agent1/issue-drafts/` output folder). Line anchors match the plan: plan_common.py lines 10 and 28, render.py line 137, plan_e01.py line 65, plan_unique.py lines 286 and 289, RELEASE-PLAN.md line 69; PIPELINE-RECORD.md row 24 is the last row.
- Importers of the changed constants: `plan_e01.py` and `plan_unique.py` (both named by a task), `plan_cycles.py` imports plan_common but not `GOAL` or `L726` (unaffected); `render.py` imports `plan_cycles` and `plan_unique` (Task 5 runs it).
- Dependents no task names: none found. `OWNER-INSTRUCTIONS.md` points agents at `.dev/issues/727/issue-body.md` (covered by Task 7) and is left unchanged on purpose.
- Result: 0 gaps.
