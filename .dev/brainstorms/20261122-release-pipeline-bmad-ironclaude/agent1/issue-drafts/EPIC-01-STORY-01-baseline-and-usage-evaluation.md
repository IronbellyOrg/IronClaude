Title: [FEATURE] Release 2 prep: evaluate the current dashboard and set the BMAD project baseline
Draft id: EPIC-01-STORY-01
Parent: EPIC-01 (Release 2 prep); grandparent umbrella #727
Labels: enhancement, release:2-prep (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (usage session by the owner; BMAD menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2 prep.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, paragraph "Release 2 prep" and "Deliverable 1" (first step: usage and evaluation of the current version).

Why this feature exists: The owner wants the evaluation of the current version first, so the two-way design starts from observed facts, not from assumptions.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, guide `docs/user-guide/observer.md`
- User guide on origin/master: `docs/user-guide/observer.md` (states the dashboard never approves, retries, terminates, dispatches, merges or messages)
- BMAD precedent on origin/master: `.dev/issues/409/bmad/` (prd-orca-observer, ux-orca-observer, architecture-orca-observer, spec-orca-observer with SPEC.md and 11 companions, final-review, handoff-step1.md to handoff-step5.md, `final-review/workflow-input.md`)

## Done when

- `project-context.md` exists, points to CLAUDE.md for house rules instead of copying them, and lists only what BMAD workflows need (UV only, fork-only PR rule, `.dev/tasks/` staged, no `.claude/` staging).
- A case file from `/bmad-investigate` grades each finding Confirmed, Deduced or Hypothesis and records where the current dashboard stops short of a two-way platform.
- The owner has used the current version for a recorded session and the notes are attached (what helped, what was missing for making decisions).

## Who it is for

The owner (supervises the coordinators and makes the decisions), with a BMAD session (analyst persona Mary is available as `/bmad-agent-analyst`).

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-generate-project-context`
   - Say first: brownfield project IronClaude; focus on `src/superclaude/cli/observe/`; point to CLAUDE.md for house rules, do not copy them
   - Produces: `project-context.md` under `_bmad-output/`
   - Done check: file exists and lists no rule that contradicts CLAUDE.md
2. `/bmad-investigate`
   - Say first: map what `superclaude observe` does today and where it falls short of a two-way decision platform (read-only rule, no database, questions in process memory)
   - Produces: case file under `_bmad-output/implementation-artifacts/`
   - Done check: every finding carries a grade and a path:line or command output

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want a written evaluation of using `superclaude observe` today, so that the two-way design starts from facts.
- As the maintainer of IronClaude, I want a lean project-context file, so that every later BMAD workflow loads the house rules without re-asking.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-generate-project-context
- [ ] Step 2: /bmad-investigate
