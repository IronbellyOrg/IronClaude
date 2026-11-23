Title: [FEATURE] Release 1.905: map each escaped bug to the automated check that would have caught it
Draft id: EPIC-14-STORY-01
Parent: EPIC-14 (Release 1.905); grandparent umbrella #727
Labels: enhancement, release:1.905 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.905.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item for release 1.905.

Why this feature exists: The owner wants automated tests or CI that would have caught the high and medium bugs of 1.9 without human validation.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Input: the high and medium bug list of EPIC-13 (release 1.9)
- Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, guide `docs/user-guide/observer.md`
- CI workflows today: `.github/workflows/test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml`

## Done when

- A table: bug, root cause area, the check that would have caught it (unit, golden render, terminal key test, schema test, CI job), why the present suite missed it.
- Every high or medium bug of the previous cycle has a row, none is skipped.
- Gaps are grouped so each group becomes one story.

## Who it is for

The maintainer of IronClaude with a BMAD session.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-14` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-investigate`
   - Say first: area exploration of `tests/observe/` and `.github/workflows/` against the bug list of release 1.9
   - Produces: case file with the gap table
   - Done check: each row cites path:line or test output
2. `/bmad-review-edge-case-hunter`
   - Say first: run on the SPEC and the acceptance tests paths to find paths no test covers
   - Produces: review report
   - Done check: findings merged into the gap table

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the maintainer of IronClaude, I want each escaped bug traced to the missing check, so that new tests target real gaps and not guesses.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-investigate
- [ ] Step 2: /bmad-review-edge-case-hunter
