---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-wantToScanOfAllP-20261125-135851
version: "1"
priority: Medium
created_date: "2026-11-25"
---

# Correct the "dashboard does not replace the coordinator" sentence everywhere it lives

Source: ./source.md
Goal: No file in the release-planning folder tells a planner that the dashboard is not meant to replace talking to the coordinator sessions, and none still calls issue 726's read-only question open. The 89 issue drafts are regenerated from corrected generator sources, nothing is filed on GitHub, and the correction is recorded.

## Constraints

- Scan result and blast-radius reasoning for this plan: ./artifacts/scan-and-blast-radius.md (every place, its count, why the rest were left alone). Grounding note: ./artifacts/codegraph-grounding.md.
- Every path below is relative to `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` (the planning folder), which is tracked on branch `ironbelly/orch-ledger-20261122` of the main checkout and is absent from master and from the Coordinator branch. Run `/sc:implement` from the checkout that has that branch checked out.
- Corrected wording of the sentence (same meaning as the corrected issue 727): the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).
- Corrected wording of the 726 text: the owner answered in chat on 2026-11-22, recorded as a comment on issue 726, that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote still waits for the architecture and storage evaluation in issue 727.
- Do not edit the 89 files under `agent1/issue-drafts/` by hand; they are output of `agent1/tools/render.py`. Do not edit the owner's verbatim text (`OWNER-INSTRUCTIONS.md`, the quote in issue 727 and in `.dev/issues/727/issue-body.md`). Do not file, edit or close any GitHub issue. Commit and push nothing.
- `PIPELINE-RECORD.md` is append-only and has an uncommitted change in that checkout: add one row at the end and keep every existing line and the uncommitted change.

## Phase 1: Fix the generator sources

## Task 1: Correct the goal and 726 constants in plan_common.py

Edit `agent1/tools/plan_common.py`: replace the `GOAL` constant (line 28, "owner goal: the dashboard does not replace talking to the coordinator sessions; ...") with the corrected wording of the Constraints, keeping the `owner goal:` prefix style used by its one consumer (`agent1/tools/plan_unique.py` line 240, the EPIC-12-STORY-01 link). Replace the `L726` constant (line 10, "... its open decision is whether the read-only rule may be relaxed") with the corrected 726 text. `L726` is imported by `agent1/tools/plan_e01.py` and `agent1/tools/plan_unique.py` and reaches 9 rendered drafts.

Acceptance criteria:
- `grep -n "does not replace\|open decision is whether" agent1/tools/plan_common.py` prints nothing.
- `uv run python -c "import sys; sys.path.insert(0,'agent1/tools'); import plan_common"` exits 0, so `plan_e01.py` and `plan_unique.py` still import `GOAL` and `L726`.
- `GOAL` still reads as one link bullet (no newline inside the string).

## Task 2: Correct the "Before step 1" paragraph in render.py

Edit `agent1/tools/render.py`, function `render_feature` (template line 137): replace "the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands ..." with the corrected wording of the Constraints. Keep `{epic['draft_id']}` and the rest of the line. This template is rendered into 73 story drafts (all stories; none of the 15 epics).

Acceptance criteria:
- `grep -n "not meant to replace" agent1/tools/render.py` prints nothing.
- The line still starts with "Before step 1: read `{epic['draft_id']}`" and still ends the sentence with "(for example ponytail)."
- `uv run python -c "import ast; ast.parse(open('agent1/tools/render.py').read())"` exits 0.

## Task 3: Correct the stale relax-the-read-only-rule item in plan_e01.py

Edit `agent1/tools/plan_e01.py` line 65, the `done` item of the EPIC-01 feature "two-way requirements and UX" (rendered into `agent1/issue-drafts/EPIC-01-STORY-03-two-way-requirements-and-ux.md`): "The decision to relax the read-only rule is recorded by the owner in a dated record (house pattern: `.dev/issues/409/owner-decisions-<date>.md`); issue #726 is told." The decision was given in chat on 2026-11-22. Reword to: the owner's 2026-11-22 decision (read-only rule relaxed, dashboard two-way) is copied into the owner-decisions record in the house pattern `.dev/issues/409/owner-decisions-<date>.md`, with the exact write paths this PRD allows still to be decided by the owner.

Acceptance criteria:
- `grep -n "issue #726 is told" agent1/tools/plan_e01.py` prints nothing.
- The item still names `.dev/issues/409/owner-decisions-<date>.md`.
- The other three `done` items of that feature are unchanged (`git diff -U0 agent1/tools/plan_e01.py` shows one changed line).

## Task 4: Add the open owner question to the EPIC-12-STORY-05 data in plan_unique.py

Edit `agent1/tools/plan_unique.py`, the data of the feature "Release 1.8: a notice when the person is needed in the coordinator session" (title line 286, `done` list line 289): append one `done` item saying that the owner's open question from issue 727 (2026-11-25) is answered or deferred in the record: should longer conversations with a coordinator move into the dashboard too, and in which release. Do not change the other items, the title or the steps.

Acceptance criteria:
- The `done` list of that feature has the two original items plus the new one, in that order.
- `git diff -U0 agent1/tools/plan_unique.py` shows only that added item.
- `uv run python -c "import ast; ast.parse(open('agent1/tools/plan_unique.py').read())"` exits 0.

## Phase 2: Regenerate the drafts

## Task 5: Re-run render.py and check that only the intended lines changed

Depends on: Task 1, Task 2, Task 3, Task 4

Run `uv run python agent1/tools/render.py` from the planning folder. It overwrites only `agent1/issue-drafts/` (89 files). Expected change: the "Before step 1" paragraph in 73 story drafts, the `- Owner goal:` bullet in `EPIC-12-STORY-01-coordinator-needs-as-decisions.md`, the `Related: #726` bullet in 9 drafts, the EPIC-01-STORY-03 done item, and the added done item in `EPIC-12-STORY-05-you-are-needed-notice.md`. If `git diff` shows any other hunk, a draft was edited by hand after the last render: stop, report the file and hunk, and restore it with `git checkout -- <file>` only after the owner decides.

Acceptance criteria:
- `ls agent1/issue-drafts | wc -l` prints 89 and no draft file was added or removed (`git status --short -- agent1/issue-drafts` shows only `M` lines).
- `grep -rlE "not meant to replace|does not replace|NOT meant to replace" agent1/issue-drafts` prints nothing.
- `grep -rl "open decision is whether the read-only rule may be relaxed" agent1/issue-drafts` prints nothing.
- Every changed hunk is one of the five kinds above (check with `git diff -U0 -- agent1/issue-drafts | grep '^[-+][^-+]'` and read each distinct line pair).
- The 15 epic drafts and `agent1/issue-drafts/README.md` are unchanged: `git diff --stat -- agent1/issue-drafts/README.md agent1/issue-drafts/EPIC-0[1-9]-release*.md agent1/issue-drafts/EPIC-1[0-5]-release*.md` prints nothing.

## Phase 3: Correct the hand-held copies

## Task 6: Correct the goal paragraph in RELEASE-PLAN.md

Edit `agent1/RELEASE-PLAN.md` line 69, the paragraph "Goal text that every epic must keep (owner, issue 727): the dashboard is NOT meant to replace talking to the coordinator sessions; ...". Replace the wrong sentence with the corrected wording of the Constraints, and replace the tail "issue 726 (vote on each question) is the first small step and its open decision is whether the read-only rule may be relaxed" with the corrected 726 text. Keep the other facts of that paragraph (observer read-only today, no database, questions in process memory, export record and snapshot).

Acceptance criteria:
- `grep -n "NOT meant to replace\|open decision is whether" agent1/RELEASE-PLAN.md` prints nothing.
- `git diff -U0 agent1/RELEASE-PLAN.md` shows one changed line (69).
- The paragraph still says the observer is read-only by design today.

## Task 7: Refresh the local copy of the issue 727 body

Unlike Tasks 1 to 6 and 8, this task's path is relative to the repository root of that checkout, not to the planning folder: run its commands from the repository root. Replace the content of `.dev/issues/727/issue-body.md` (tracked) with the live body of issue 727: run `gh issue view 727 --repo IronbellyOrg/IronClaude --json body -q .body` and write its output to that file. `OWNER-INSTRUCTIONS.md` tells planning agents to read this file first, so it must match the corrected issue. The command is read-only on GitHub.

Acceptance criteria:
- `diff <(gh issue view 727 --repo IronbellyOrg/IronClaude --json body -q .body) .dev/issues/727/issue-body.md` prints nothing.
- The file contains "Correction (owner, 2026-11-25)" and still contains the owner's quote "The ultimate goal is NOT to replace interacting with the coordinator sessions" unchanged below that correction.
- `git status --short -- .dev/issues/727/issue-body.md` shows the file as modified and no other `.dev/issues/` path changed.

## Phase 4: Record the correction

## Task 8: Append the correction row to PIPELINE-RECORD.md

Depends on: Task 5, Task 6, Task 7

Append one row at the end of the table in `PIPELINE-RECORD.md` (after row 24), numbered 25: date 2026-11-25; phase Correction; entry: the owner corrected the goal sentence of issue 727 (the dashboard replaces direct communication with the coordinators; the 1.8 release is where responses and answers start going through it), naming the old rows it changes (row 1, the roadmap input, and row 4, the 88 drafts written with the wrong sentence) and listing what was fixed (render.py, plan_common.py, plan_e01.py, plan_unique.py, RELEASE-PLAN.md, `.dev/issues/727/issue-body.md`, 89 drafts regenerated, nothing filed) and the open owner question about longer conversations; decided by: owner in chat; evidence: issue 727 body, `agent1/RELEASE-PLAN.md`; status: changed. Use the table's existing column order and `|` format.

Acceptance criteria:
- `git diff -U0 PIPELINE-RECORD.md` shows the added row 25 and no removed line of the existing rows; the uncommitted change that was already in the file is still there.
- The row has the same number of `|` separators as row 24.
- Rows 1 and 4 are not edited (append-only rule).
