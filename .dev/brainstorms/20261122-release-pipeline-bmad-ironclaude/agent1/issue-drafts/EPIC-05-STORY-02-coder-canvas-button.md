Title: [FEATURE] 1.3 slot: review opening the dashboard from the Coder workspace canvas with a new button
Draft id: EPIC-05-STORY-02
Parent: EPIC-05 (Release 1.3 slot (unnumbered in the owner's list)); grandparent umbrella #727
Labels: enhancement, release:1.3 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.3 slot (unnumbered in the owner's list).
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Review porting dashboard to Zelij and accessing it directly from Coder Workspace canvas with a new button' (read as Zellij).

Why this feature exists: The owner wants to reach the dashboard directly from the Coder Workspace canvas with a new button.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Not known yet: how a Coder workspace canvas button is defined (template app, link, extension), where the Coder template for this workspace lives, and what the button should open (a web page, a terminal session)

## Done when

- A research document states how a button on the Coder workspace canvas can be added, what it can open, who changes which repository, with sources.
- The dependency between this button and the Zellij review is stated (the button opens what?).

## Who it is for

The owner (supervises the coordinators and makes the decisions) decides; a BMAD research session informs.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-05` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-technical-research`
   - Say first: adding a button to a Coder workspace canvas that opens a terminal dashboard; Coder template and app options
   - Produces: research document
   - Done check: web search was available; sources listed

## Story seeds (turn these into user stories with BMAD; edit freely)

- As a developer who runs coordinator sessions and uses the dashboard, I want one button on my Coder workspace that opens the dashboard, so that I do not type the command.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-technical-research
