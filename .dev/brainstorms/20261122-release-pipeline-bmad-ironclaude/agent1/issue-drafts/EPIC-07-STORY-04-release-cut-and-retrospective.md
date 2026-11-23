Title: [FEATURE] Release 1.5: cut the release and run the retrospective
Draft id: EPIC-07-STORY-04
Parent: EPIC-07 (Release 1.5); grandparent umbrella #727
Labels: enhancement, release:1.5 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Simple
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.5.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item for release 1.5.

Why this feature exists: A release is only real when it is recorded, its ledger is closed and the lessons feed the next cycle.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- How a dashboard release is recorded (tag, document, version string) is not known yet; the package version in pyproject.toml is 5.0.0, so the dashboard 1.x numbers are a separate scheme (open question Q3 in agent1/RELEASE-PLAN.md S5.2)

## Done when

- `/bmad-sprint-status` (data mode) shows every story of this epic `done` and no `review` or `in-progress` left.
- Release 1.5 is recorded where the owner decides, with the list of changes.
- The retrospective is done; its action items are in `sprint-status.yaml` and are inputs of the next cycle.

## Who it is for

The owner (supervises the coordinators and makes the decisions); BMAD facilitates the retrospective.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-07` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-sprint-status`
   - Say first: data mode: counts and risks for this epic
   - Produces: status summary
   - Done check: all stories of this epic `done`
2. `/bmad-retrospective`
   - Say first: retro the epic of release 1.5
   - Produces: retrospective document and action items
   - Done check: action items have owners

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want the release recorded with what changed, so that the next validation cycle knows what to test.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-sprint-status
- [ ] Step 2: /bmad-retrospective
