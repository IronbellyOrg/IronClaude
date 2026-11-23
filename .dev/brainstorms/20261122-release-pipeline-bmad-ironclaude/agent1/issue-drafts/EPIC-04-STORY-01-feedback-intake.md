Title: [FEATURE] Release 1.2: collect feedback from current usage in one place
Draft id: EPIC-04-STORY-01
Parent: EPIC-04 (Release 1.2); grandparent umbrella #727
Labels: enhancement, release:1.2 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Simple
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.2.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Filing Feedback based on current usage with a version 1.2 release'.

Why this feature exists: The 1.2 release is built from feedback on real use, so the feedback needs one place and one format first.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, guide `docs/user-guide/observer.md`

## Done when

- One place and one format exist for usage feedback (who, what, where in the dashboard, how often it matters).
- At least the feedback the owner already has is entered; each item has a proposed class (bug, change, new feature, question).

## Who it is for

The owner (supervises the coordinators and makes the decisions) and the developers who use the dashboard.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-04` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-brainstorming`
   - Say first: turn raw usage feedback into a clean list (Facilitator stance: the person supplies the ideas)
   - Produces: brainstorming session under `_bmad-output/brainstorming/`
   - Done check: each item has class and evidence

## Story seeds (turn these into user stories with BMAD; edit freely)

- As a developer who runs coordinator sessions and uses the dashboard, I want to leave feedback in a fixed format while I use the dashboard, so that it is not lost in chat.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-brainstorming
