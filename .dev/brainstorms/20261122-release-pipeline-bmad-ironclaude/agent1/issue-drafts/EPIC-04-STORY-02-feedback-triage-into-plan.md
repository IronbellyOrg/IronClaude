Title: [FEATURE] Release 1.2: triage the feedback into the PRD and the release scope
Draft id: EPIC-04-STORY-02
Parent: EPIC-04 (Release 1.2); grandparent umbrella #727
Labels: enhancement, release:1.2 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.2.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Filing Feedback based on current usage with a version 1.2 release'.

Why this feature exists: Not all feedback belongs in 1.2. The triage decides what is built now, later or never, and records why.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`

## Done when

- Each feedback item is: in 1.2, later (with the release), or declined (with the reason).
- The PRD is updated for requirement changes; a change proposal exists for epics and architecture impact.

## Who it is for

The owner (supervises the coordinators and makes the decisions) decides; a BMAD session facilitates.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-04` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-correct-course`
   - Say first: feedback list as the change trigger; assess impact on PRD, epics, architecture, UX
   - Produces: `sprint-change-proposal-<date>.md`
   - Done check: proposal approved by the owner
2. `/bmad-prd`
   - Say first: update the PRD for the accepted requirement changes
   - Produces: updated `prd.md`, `.memlog.md`
   - Done check: changes logged with reasons

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want each feedback item sorted into now, later or never with a reason, so that the 1.2 scope is deliberate.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-correct-course
- [ ] Step 2: /bmad-prd
