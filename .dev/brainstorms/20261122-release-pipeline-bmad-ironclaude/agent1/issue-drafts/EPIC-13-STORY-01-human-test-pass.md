Title: [FEATURE] Release 1.9: human test pass of the release 1.8 build
Draft id: EPIC-13-STORY-01
Parent: EPIC-13 (Release 1.9); grandparent umbrella #727
Labels: enhancement, release:1.9 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (the pass itself is manual)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.9.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item for release 1.9.

Why this feature exists: The owner validates every feature and desired behaviour by hand. A written guide makes the pass repeatable and gives each finding evidence. The guide is the previous cycle's guide plus rows for what changed.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Acceptance tests and live guide on origin/master: `.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md`, `.dev/issues/409/live-test-guide.md`, `docs/user-guide/observer.md`
- Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, guide `docs/user-guide/observer.md`
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`

## Done when

- Every capability and every FR of this release has a row in the guide: what to do, expected result, pass or fail, evidence (screenshot or text export).
- The owner (or a named tester) ran the whole guide against the release 1.8 build; each failure is a finding with steps to reproduce.
- Rows that cannot be tested by hand are listed as such with the reason.

## Who it is for

The owner (supervises the coordinators and makes the decisions) or a tester the owner names; a BMAD session writes the guide.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-13` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-agent-tech-writer`
   - Say first: Write Document (menu WD): a human validation guide for the release 1.8 build, from the SPEC acceptance tests, the user guide and the FRs of this release; one row per capability
   - Produces: validation guide next to the SPEC
   - Done check: every capability and FR has a row
2. `/bmad-checkpoint-preview`
   - Say first: walk through what changed since the last validated release, from purpose into details (optional, for changed areas)
   - Produces: walkthrough notes
   - Done check: changed areas have extra guide rows
3. `Run the guide by hand (no command)`
   - Say first: against the release 1.8 build, record pass or fail with evidence per row
   - Produces: filled guide
   - Done check: no row left blank

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want a step-by-step guide that covers every feature, so that no feature is validated by memory.
- As the owner (supervises the coordinators and makes the decisions), I want each failed row to carry evidence, so that bug filing needs no second session.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-agent-tech-writer
- [ ] Step 2: /bmad-checkpoint-preview
- [ ] Step 3: Run the guide by hand (no command)
