Title: [FEATURE] Release 2 prep: evaluate state persistence and data storage for a two-way dashboard
Draft id: EPIC-01-STORY-04
Parent: EPIC-01 (Release 2 prep); grandparent umbrella #727
Labels: enhancement, release:2-prep (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2 prep.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, paragraph "Release 2 prep" and "Deliverable 1" (evaluate needs for state persistence and data storage; deliverable 1: /sc:brainstorm --depth deep).

Why this feature exists: Today the dashboard keeps nothing but an export record and a snapshot. A platform where decisions are made must keep questions, votes, answers and an audit trail, and several coordinators and developers will read and write the same state.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, guide `docs/user-guide/observer.md`
- Related: #726 (a vote on each question, kept as a local record; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote waits for the architecture and storage evaluation in #727)
- Brainstorm output folder convention: `.dev/brainstorms/<date>-<topic>/`

## Done when

- A list of what must persist (questions, votes from #726, answers, demands to the coordinator, escalations, audit trail, snapshots), who writes and reads each item, and the consistency each needs.
- A deep brainstorm result on architecture, data storage and database needs for releases 1.1 to 2.0, with the options considered and the rejected ones recorded.
- The decision is in the architecture spine as `AD-n` entries (new ids only, existing ids not renumbered) with Binds, Prevents and Rule.

## Who it is for

The owner (supervises the coordinators and makes the decisions) decides; BMAD architect (Winston, `/bmad-agent-architect`) and an IronClaude brainstorm contribute.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-technical-research`
   - Say first: state persistence and data storage options for a bidirectional dashboard over agent sessions (files, SQLite, Postgres), consistency and concurrency
   - Produces: technical research document under `_bmad-output/planning-artifacts/research/`
   - Done check: options compared with sources; web search available
2. `/sc:brainstorm "architecture, data storage and database needs of dashboard releases 1.1 to 2.0 incl. a Postgres database per project and organised session and decision history @.dev/issues/727/issue-body.md" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-dashboard-storage/`
   - Say first: owner's deliverable 1 asks for exactly this deep brainstorm; run it ATTENDED in a person's own session (under --unattended the Socratic dialogue and deep research are skipped); pass the research document too
   - Produces: brainstorm package under the output folder
   - Done check: package has proposals, merged result and the open decisions; BMAD decides from it
3. `/bmad-architecture`
   - Say first: update the existing spine (keep AD ids stable) with the persistence decisions; coaching path
   - Produces: updated `ARCHITECTURE-SPINE.md`, `.memlog.md`
   - Done check: lint and reviewer gate of the skill pass; new `AD-n` have Binds, Prevents, Rule

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want to know exactly what the dashboard must remember, so that storage is sized to real needs and not guessed.
- As a coordinator agent, I want questions and answers stored where the dashboard and I both reach them, so that an answer given in the dashboard arrives without copying text.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-technical-research
- [ ] Step 2: /sc:brainstorm "architecture, data storage and database needs of dashboard releases 1.1 to 2.0 incl. a Postgres database per project and organised session and decision history @.dev/issues/727/issue-body.md" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-dashboard-storage/
- [ ] Step 3: /bmad-architecture
