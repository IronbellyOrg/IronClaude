Title: [FEATURE] Release 1.6: UX contract and acceptance criteria for the picked screens
Draft id: EPIC-09-STORY-02
Parent: EPIC-09 (Release 1.6); grandparent umbrella #727
Labels: enhancement, release:1.6 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.6.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Review addition screens from initial tui mockups and Clays html dashboards, picking 2-4 more to recreate in TUI for version 1.6'.

Why this feature exists: Each picked screen needs a text rendering at the three fixed widths and acceptance criteria before code.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Rendering rules and golden fixtures from the observer visual parity work (#606, closed)

## Done when

- For each picked screen: DESIGN.md and EXPERIENCE.md sections, text mockups at 160, 116 and 80 columns, data fields and their source, empty and error states.
- An independent review passed.

## Who it is for

The owner (supervises the coordinators and makes the decisions) approves; BMAD UX session.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-09` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-ux`
   - Say first: update the UX pair for the picked screens
   - Produces: `DESIGN.md` and `EXPERIENCE.md`
   - Done check: text mockups at three widths exist
2. `/bmad-review-adversarial-general`
   - Say first: review the UX pair at its path
   - Produces: review report
   - Done check: blocking findings fixed

## Story seeds (turn these into user stories with BMAD; edit freely)

- As a developer who runs coordinator sessions and uses the dashboard, I want each new screen to render correctly at 160, 116 and 80 columns, so that it works in any terminal width I use.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-ux
- [ ] Step 2: /bmad-review-adversarial-general
