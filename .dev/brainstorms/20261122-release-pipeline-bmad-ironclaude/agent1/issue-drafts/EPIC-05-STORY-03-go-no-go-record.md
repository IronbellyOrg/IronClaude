Title: [FEATURE] 1.3 slot: owner go or no-go record for Zellij and the canvas button, and the scope of 1.4
Draft id: EPIC-05-STORY-03
Parent: EPIC-05 (Release 1.3 slot (unnumbered in the owner's list)); grandparent umbrella #727
Labels: enhancement, release:1.3 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Simple
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.3 slot (unnumbered in the owner's list).
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Review porting dashboard to Zelij and accessing it directly from Coder Workspace canvas with a new button' (read as Zellij) and 'Planning testing and integration for a 1.4 release'.

Why this feature exists: Release 1.4 plans testing and integration; its scope depends on this decision, so the decision is a recorded gate and not a chat remark.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- House pattern for owner decisions: `.dev/issues/409/owner-decisions-<date>.md`

## Done when

- A dated owner decision record: Zellij go, no-go or later; canvas button go, no-go or later; each with the reason.
- The scope of EPIC-06 is updated to match (features dropped or kept).

## Who it is for

The owner (supervises the coordinators and makes the decisions)

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-05` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-forge-idea`
   - Say first: pressure-test the go case and the no-go case using the two research documents
   - Produces: optional `forged-idea.md`
   - Done check: the strongest objection to the chosen option is written down
2. `/bmad-correct-course`
   - Say first: update EPIC-06 scope from the decision (only if the decision removes or adds features)
   - Produces: change proposal
   - Done check: EPIC-06 draft matches the decision

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want one decision record, so that release 1.4 plans only what I approved.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-forge-idea
- [ ] Step 2: /bmad-correct-course
