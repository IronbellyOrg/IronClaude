Title: [FEATURE] Release 1.9: capture feedback and feature requests from the test pass
Draft id: EPIC-13-STORY-02
Parent: EPIC-13 (Release 1.9); grandparent umbrella #727
Labels: enhancement, release:1.9 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.9.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item for release 1.9 (feedback/feature requests).

Why this feature exists: The owner wants feedback and feature requests collected during validation of the first write and respond features, so release 2.0 is built from them.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Feedback intake: the previous feedback release (EPIC-04) defines the place and the format

## Done when

- Every feedback item and feature request is recorded once with: who, what, where in the dashboard, how often it matters, and a proposed class (bug, change, new feature, question).
- The list is the input of EPIC-15 (release 2.0), already sorted for `/bmad-correct-course`.

## Who it is for

The owner (supervises the coordinators and makes the decisions) and each tester.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-13` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-brainstorming`
   - Say first: session to turn raw feedback from the test pass into a clean list of requests (Facilitator stance; the person supplies the ideas)
   - Produces: brainstorming session under `_bmad-output/brainstorming/`
   - Done check: each item has class and evidence
2. `/bmad-correct-course`
   - Say first: assess the list's impact on PRD, epics and architecture; produce the change proposal
   - Produces: `sprint-change-proposal-<date>.md` in `planning-artifacts`
   - Done check: proposal names what moves into release 2.0 and what waits

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want feedback and feature requests collected in one list during validation, so that nothing said in passing is lost before release 2.0.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-brainstorming
- [ ] Step 2: /bmad-correct-course
