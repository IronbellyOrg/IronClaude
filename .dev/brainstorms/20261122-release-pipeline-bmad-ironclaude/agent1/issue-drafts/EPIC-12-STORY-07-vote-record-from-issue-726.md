Title: [FEATURE] Release 1.8: fold in the vote on each question (issue 726)
Draft id: EPIC-12-STORY-07
Parent: EPIC-12 (Release 1.8); grandparent umbrella #727
Labels: enhancement, release:1.8 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Simple
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.8.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Planning, brainstorming and implementation of first write/Respond features for a 1.8 release'.

Why this feature exists: Issue #726 is the first small step of this roadmap (a vote on each question, kept as a record). It must be folded in or replaced, not built twice.

## Relevant files and links

- Related: #726 (a vote on each question, kept as a local record; its open decision is whether the read-only rule may be relaxed)
- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)

## Done when

- The owner decided whether #726 is built as written, folded into the decision card, or closed as superseded, and the issue says so.

## Who it is for

The owner (supervises the coordinators and makes the decisions)

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-12` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-correct-course`
   - Say first: trigger: issue 726 versus the write-path PRD; decide fold-in or supersede
   - Produces: change proposal
   - Done check: owner decision recorded on #726

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want to record whether an intervention was the right call, so that prompting can be tuned later.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-correct-course
