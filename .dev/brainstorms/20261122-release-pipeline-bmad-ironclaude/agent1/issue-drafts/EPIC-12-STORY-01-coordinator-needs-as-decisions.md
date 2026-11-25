Title: [FEATURE] Release 1.8: boil the coordinator's needs down to binary, multiple-choice or 'you are needed' decisions
Draft id: EPIC-12-STORY-01
Parent: EPIC-12 (Release 1.8); grandparent umbrella #727
Labels: enhancement, release:1.8 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.8.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Planning, brainstorming and implementation of first write/Respond features for a 1.8 release'.

Why this feature exists: The owner wants the coordinators' questions turned into digestible multiple-choice or binary decisions, or a notice that the person is needed in the session for a longer conversation.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Question data today: `src/superclaude/cli/observe/questions.py` (origin/master); the Decision Desk shows questions but cannot answer them
- Owner goal: owner goal: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail)

## Done when

- A catalogue of real coordinator question types taken from real sessions, each classified: binary, multiple choice, needs-the-session (with an example for each).
- For each class, the answer format and what the coordinator does with the answer.
- Questions that fit no class are listed with the reason.

## Who it is for

The owner (supervises the coordinators and makes the decisions) with coordinators' history as evidence; brainstorm plus BMAD session.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-12` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/sc:brainstorm "turn coordinator questions into binary, multiple-choice or needs-the-session decisions for the dashboard" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-decision-shapes/`
   - Say first: run ATTENDED in a person's own session; pass real question samples (redacted) and the owner goal
   - Produces: brainstorm package
   - Done check: catalogue and classification in the merged result
2. `/bmad-forge-idea`
   - Say first: pressure-test the classification against the questions that fit no class
   - Produces: optional `forged-idea.md`
   - Done check: leftover questions have a stated route

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want each question type reduced to the smallest answer possible, so that most decisions are one key.
- As a coordinator agent, I want to state a question in a fixed shape (options, default, consequence of each), so that the dashboard can show it as a decision.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /sc:brainstorm "turn coordinator questions into binary, multiple-choice or needs-the-session decisions for the dashboard" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-decision-shapes/
- [ ] Step 2: /bmad-forge-idea
