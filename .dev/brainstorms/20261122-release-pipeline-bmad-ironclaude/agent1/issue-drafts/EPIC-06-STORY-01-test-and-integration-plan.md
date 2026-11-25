Title: [FEATURE] Release 1.4: plan the testing and integration
Draft id: EPIC-06-STORY-01
Parent: EPIC-06 (Release 1.4); grandparent umbrella #727
Labels: enhancement, release:1.4 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.4.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Planning testing and integration for a 1.4 release'.

Why this feature exists: The owner lists planning first for 1.4. The plan says what is integrated (Zellij, canvas button, per the go record), how it is tested and in what order.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Input: the go or no-go record of EPIC-05
- CI workflows today: `.github/workflows/test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml`

## Done when

- A test and integration plan names each integration point, the check for each, and the order.
- Stories for the approved integrations exist, ready, with Given/When/Then criteria.

## Who it is for

The owner (supervises the coordinators and makes the decisions) approves; a BMAD session plans.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-06` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-architecture`
   - Say first: update the spine for the approved integration points (new AD ids only)
   - Produces: updated spine
   - Done check: reviewer gate passes
2. `/bmad-create-epics-and-stories`
   - Say first: stories for the approved integrations and their tests; epic number fixed to this EPIC number
   - Produces: story entries
   - Done check: FR coverage map complete
3. `/bmad-check-implementation-readiness`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: readiness report
   - Done check: no blocking gap
4. `/bmad-sprint-planning`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: refreshed `sprint-status.yaml`
   - Done check: story keys present

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want the integration and its tests planned before code, so that 1.4 does not discover its test needs late.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-architecture
- [ ] Step 2: /bmad-create-epics-and-stories
- [ ] Step 3: /bmad-check-implementation-readiness
- [ ] Step 4: /bmad-sprint-planning
