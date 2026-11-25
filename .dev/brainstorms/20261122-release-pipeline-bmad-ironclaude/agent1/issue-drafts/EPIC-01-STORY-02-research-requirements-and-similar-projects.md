Title: [FEATURE] Release 2 prep: research requirements, best approaches and similar GitHub projects
Draft id: EPIC-01-STORY-02
Parent: EPIC-01 (Release 2 prep); grandparent umbrella #727
Labels: enhancement, release:2-prep (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2 prep.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, paragraph "Release 2 prep" and "Deliverable 1" (research of requirements, best approaches and any similar github projects).

Why this feature exists: The owner asked to learn from overlapping GitHub projects before building voting and responding from the dashboard.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Related: #726 (a vote on each question, kept as a local record; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote waits for the architecture and storage evaluation in #727)
- Licence rule carried over from the 409 packet: no AGPL code is copied, linked or imported (TUIBBS licence question stayed open in `.dev/issues/409/bmad/final-review/workflow-input.md`)

## Done when

- A research document lists each similar project with: link, what overlaps (voting, approving, answering agent questions, decision queues), what to take, what not to take, licence.
- A short list of best approaches for turning agent questions into binary or multiple-choice decisions, with the source of each.
- Every claim is labelled verified (source read) or UNVERIFIED.

## Who it is for

The owner (supervises the coordinators and makes the decisions); research is done by the BMAD session and may use IronClaude research tools in the same session.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-market-research`
   - Say first: comparable open-source projects for a two-way terminal or web dashboard over AI coding-agent sessions: voting, approvals, answering questions
   - Produces: research document under `_bmad-output/planning-artifacts/research/`
   - Done check: each project has link, overlap, take, avoid, licence
2. `/bmad-technical-research`
   - Say first: approaches and libraries for decision queues, approval flows and reducing free-text questions to choices
   - Produces: `technical-<slug>-research-<date>.md` under `_bmad-output/planning-artifacts/research/`
   - Done check: approaches are ranked with sources; web search was available (the skill aborts without it)

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want to know which existing projects already solve voting and responding for agent sessions, so that we reuse what works and avoid their mistakes.
- As the owner (supervises the coordinators and makes the decisions), I want the best approaches for reducing a coordinator question to a binary or multiple-choice decision, so that most interactions are one key press.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-market-research
- [ ] Step 2: /bmad-technical-research
