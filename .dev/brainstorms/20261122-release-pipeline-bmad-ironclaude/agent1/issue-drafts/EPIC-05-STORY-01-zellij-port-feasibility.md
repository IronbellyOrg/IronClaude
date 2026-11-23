Title: [FEATURE] 1.3 slot: review porting the dashboard to Zellij
Draft id: EPIC-05-STORY-01
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

Why this feature exists: The owner wants a review, not a port yet. Issue #606 (closed) holds an earlier Zellij go or no-go, which must be read first.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Prior decision record: issue #606 (visual parity, closed; holds the Zellij go or no-go, per issue 727)
- Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, guide `docs/user-guide/observer.md`
- Not known yet: how the terminal dashboard would run inside Zellij (plugin, pane running the existing command, or a rewrite); to be researched, not assumed

## Done when

- A research document states what 'port to Zellij' can mean here (run the existing command in a pane, a Zellij plugin, a rewrite), with effort, benefits, risks and sources for each.
- The earlier go or no-go in #606 is quoted with its reasons and checked against today's facts.

## Who it is for

The owner (supervises the coordinators and makes the decisions) decides; a BMAD research session informs.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-05` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-technical-research`
   - Say first: porting a Python terminal dashboard to Zellij: plugin versus pane, effort, limits; read #606 first
   - Produces: research document under `_bmad-output/planning-artifacts/research/`
   - Done check: each option has sources; UNVERIFIED claims labelled

## Story seeds (turn these into user stories with BMAD; edit freely)

- As a developer who runs coordinator sessions and uses the dashboard, I want the dashboard inside my Zellij layout, so that I see questions beside the coordinator session.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-technical-research
