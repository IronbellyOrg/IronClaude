Title: [FEATURE] Release 2 prep: requirements and UX of the two-way dashboard (decisions, demands, notices)
Draft id: EPIC-01-STORY-03
Parent: EPIC-01 (Release 2 prep); grandparent umbrella #727
Labels: enhancement, release:2-prep (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2 prep.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, paragraph "Release 2 prep" and "Deliverable 1" and the goal paragraph (binary or multiple choice; demands to the coordinator when that fails).

Why this feature exists: The product goal changes from showing information to making decisions. The PRD, the UX contract and the read-only rule must change together, and that needs the owner's recorded decision.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Related: #726 (a vote on each question, kept as a local record; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote waits for the architecture and storage evaluation in #727)
- BMAD precedent on origin/master: `.dev/issues/409/bmad/` (prd-orca-observer, ux-orca-observer, architecture-orca-observer, spec-orca-observer with SPEC.md and 11 companions, final-review, handoff-step1.md to handoff-step5.md, `final-review/workflow-input.md`)
- Existing spec companion on origin/master: `.dev/issues/409/bmad/spec-orca-observer/write-back-future-stage.md`

## Done when

- The PRD (Update of the 409 PRD) has feature groups with globally numbered FR ids for: decision cards (binary and multiple choice), demands to the coordinator (more context, better explanation, debate of several proposals, extra validation, research, fact checking, use of named plugins or tools such as ponytail), and the notice that the person is needed in a coordinator session.
- The UX pair (DESIGN.md, EXPERIENCE.md) covers those screens at the terminal widths the 409 package fixed (160, 116 and 80 columns).
- The owner's 2026-11-22 decision (read-only rule relaxed, dashboard two-way) is copied into the owner-decisions record in the house pattern `.dev/issues/409/owner-decisions-<date>.md`, with the exact write paths this PRD allows still to be decided by the owner.
- An independent review of the PRD and UX passed before anything is handed to IronClaude (the 409 review needed 63 blocking fixes).

## Who it is for

The owner (supervises the coordinators and makes the decisions); BMAD product manager (John, `/bmad-agent-pm`) and UX designer (Sally, `/bmad-agent-ux-designer`) personas are available.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-forge-idea`
   - Say first: pressure-test this idea: the dashboard is where decisions are made; coordinator questions become binary or multiple choice; the fallback is a demand to the coordinator
   - Produces: optional `forged-idea.md`; sessions are interactive only
   - Done check: assumptions that did not survive are written down
2. `/bmad-prd`
   - Say first: update the PRD copied from `.dev/issues/409/bmad/prd-orca-observer/` for the two-way dashboard to release 2.0; change signal: the owner text of issue 727
   - Produces: `prd.md`, `addendum.md`, `.memlog.md` in a new run folder
   - Done check: feature groups and FR ids exist; open questions triaged; validation report written
3. `/bmad-ux`
   - Say first: two-way screens: decision card, demand menu, 'you are needed' notice; extend the 409 DESIGN.md and EXPERIENCE.md
   - Produces: `DESIGN.md` and `EXPERIENCE.md` under `_bmad-output/planning-artifacts/ux-designs/`
   - Done check: screens render as text mockups at 160, 116 and 80 columns
4. `/bmad-review-adversarial-general`
   - Say first: review the new PRD and UX at their paths; report only concrete defects with consequences
   - Produces: review report next to each document
   - Done check: blocking findings fixed or recorded; independent review passes (then `/sc:spec-panel @<prd path>` once, first on one file; a folder is not known to work)

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want each coordinator question shown as a decision I can answer with one key, so that I stop typing answers in the coordinator terminal.
- As the owner (supervises the coordinators and makes the decisions), when a question cannot be reduced, I want one-key demands to the coordinator (more context, better explanation, debate, validation, research, fact check, run a named plugin), so that the coordinator does the work before I decide.
- As a developer who runs coordinator sessions and uses the dashboard, I want a notice that I am needed in the coordinator session for a longer conversation, so that I do not miss it.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-forge-idea
- [ ] Step 2: /bmad-prd
- [ ] Step 3: /bmad-ux
- [ ] Step 4: /bmad-review-adversarial-general
