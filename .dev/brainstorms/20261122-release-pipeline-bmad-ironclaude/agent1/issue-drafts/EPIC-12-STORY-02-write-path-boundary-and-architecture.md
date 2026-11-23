Title: [FEATURE] Release 1.8: change the read-only boundary: architecture and PRD for the write path
Draft id: EPIC-12-STORY-02
Parent: EPIC-12 (Release 1.8); grandparent umbrella #727
Labels: enhancement, release:1.8 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.8.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Planning, brainstorming and implementation of first write/Respond features for a 1.8 release' (write/Respond).

Why this feature exists: The dashboard is read-only by design; two-way needs the rule changed on purpose, with the allowed writes named, not by accident. The 409 spec already holds a future-stage note on write-back.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Related: #726 (a vote on each question, kept as a local record; its open decision is whether the read-only rule may be relaxed)
- `.dev/issues/409/bmad/spec-orca-observer/write-back-future-stage.md` (origin/master)
- Observer guide: `docs/user-guide/observer.md` (read-only statement to be changed)

## Done when

- The owner has recorded the boundary change (what writes are allowed: answers to coordinator questions, votes, demands) and what stays forbidden.
- PRD feature groups, the architecture spine (new `AD-n`: allowed writes, who may write, audit record) and the UX are updated and reviewed.
- Issue #726 and `docs/user-guide/observer.md` are on the update list.

## Who it is for

The owner (supervises the coordinators and makes the decisions) decides; BMAD PRD and architecture sessions.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-12` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-prd`
   - Say first: update the PRD for the write path: decision answers, votes, demands, notices
   - Produces: updated `prd.md`
   - Done check: feature groups and FRs for the write path exist
2. `/bmad-architecture`
   - Say first: update the spine: the write boundary, allowed writes, audit record (new AD ids)
   - Produces: updated spine
   - Done check: reviewer gate passes
3. `/bmad-ux`
   - Say first: decision card and demand menu behaviour: states, errors, confirmation
   - Produces: updated `EXPERIENCE.md`
   - Done check: states covered
4. `/bmad-review-adversarial-general`
   - Say first: review PRD, spine and UX at their paths; add `/bmad-review-edge-case-hunter` on the spine
   - Produces: review reports
   - Done check: blocking findings fixed

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the maintainer of IronClaude, I want the list of allowed writes explicit and tested, so that the dashboard can never do more than the owner approved.
- As the owner (supervises the coordinators and makes the decisions), I want every answer given in the dashboard recorded with who and when, so that a decision can be traced.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-prd
- [ ] Step 2: /bmad-architecture
- [ ] Step 3: /bmad-ux
- [ ] Step 4: /bmad-review-adversarial-general
