Title: [FEATURE] Release 2.0: cut the release, run the retrospective and record what comes after 2.0
Draft id: EPIC-15-STORY-05
Parent: EPIC-15 (Release 2.0); grandparent umbrella #727
Labels: enhancement, release:2.0 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Simple
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2.0.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Implement feedback from 1.9 and additional write/respond features for 2.0 release' and 'Release 2 and beyond: more user feedback systems used to gather data to fine tune when and how the user is prompted'.

Why this feature exists: 2.0 is recorded. The owner's note about what comes after 2.0 (feedback systems that gather data to tune when and how the person is prompted) is captured as input for the next plan, not planned here.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Where a dashboard release is recorded is not known yet (question Q3 in agent1/RELEASE-PLAN.md S5.2)

## Done when

- Every story of this epic is `done`.
- Release 2.0 is recorded where the owner decides.
- Retrospective done; the beyond-2.0 note is filed as an input for the next roadmap.

## Who it is for

The owner (supervises the coordinators and makes the decisions)

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-15` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-sprint-status`
   - Say first: data mode: counts and risks for this epic
   - Produces: status summary
   - Done check: all stories of this epic `done`
2. `/bmad-retrospective`
   - Say first: retro the epic of release 2.0
   - Produces: retrospective and action items
   - Done check: action items have owners

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want 2.0 recorded and the next direction noted, so that planning continues from facts.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-sprint-status
- [ ] Step 2: /bmad-retrospective
