Title: [EPIC] Release 2 prep: evaluate the dashboard and decide the architecture, storage and Postgres database for a two-way platform
Draft id: EPIC-01
Parent: umbrella #727 (native sub-issue)
Labels: enhancement, epic (new), release:2-prep (new)
Issue type: Feature
Complexity (proposed): Complex
Release: Release 2 prep
Schedule state: OWNER MARKED FIRST (precedence over the release list); file when the owner says go
Status: DRAFT on disk. Do not file until the owner schedules this release.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727. Owner's item, close to verbatim: First step is usage and evaluation of current version and evaluation and research of requirements, best approaches and any similar github projects ... Evaluate needs for state persistence and data storage related to the dashboard becoming a central bidirectional communication platform ... This architectural and prelim eval takes precedence over the release 2 roadmap below. Priority is evaluating the needs and validating or building/changing what is needed to support those and future needs, including the creation of a postgres database per project with the eventual goal of having current and past sessions and decisions vectorized (or organized in whatever way provides most benefit for least work) of all coordinators within a project, across all human developers.

State read on 2026-11-22 (so the next person starts from facts): the observer dashboard (`superclaude observe`) is read-only by design and keeps no database; questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder (issue #727, section "State read"). The observer code is on origin/master under `src/superclaude/cli/observe/` with tests in `tests/observe/`.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Related: #726 (a vote on each question, kept as a local record; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote waits for the architecture and storage evaluation in #727)
- Related open issues: #409 (TUI dashboard), #706 (observer follow-up), #604 (observer remote fleet), #716 (coordinator next release), #717 (issue watcher), #718 (dashboard items from the 655 split)
- BMAD precedent on origin/master: `.dev/issues/409/bmad/` (prd-orca-observer, ux-orca-observer, architecture-orca-observer, spec-orca-observer with SPEC.md and 11 companions, final-review, handoff-step1.md to handoff-step5.md, `final-review/workflow-input.md`)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`

## Done when

- Deliverable 1 of issue 727 is finished: the written review of the release list, and the `/sc:brainstorm --depth deep` result on architecture, data storage and database needs.
- Release 2 prep items are done: use and evaluation of the current version; research of requirements, best approaches and similar GitHub projects; the state and storage needs of a two-way dashboard.
- The owner has recorded in chat which releases are scheduled; each scheduled release has its own epic issue (this epic closes when they exist or the owner drops them).

## Pick-up note

The architecture and preliminary evaluation come first (owner's order). The program-level BMAD run (project context, investigate, research, PRD update, UX, architecture update, spec, review, epics, readiness, sprint planning) happens in this epic once, with the owner in the session; later releases reuse its outputs. Planning only until the owner says go; the Postgres provisioning and schema stories are the first code and need an explicit go.

Do not build anything from this epic before the owner says go (owner's order in issue #727). Release 2 prep (EPIC-01) takes precedence over every other epic.

## Features (sub-issues, in order)

- `EPIC-01-STORY-01` Release 2 prep: evaluate the current dashboard and set the BMAD project baseline
- `EPIC-01-STORY-02` Release 2 prep: research requirements, best approaches and similar GitHub projects
- `EPIC-01-STORY-03` Release 2 prep: requirements and UX of the two-way dashboard (decisions, demands, notices)
- `EPIC-01-STORY-04` Release 2 prep: evaluate state persistence and data storage for a two-way dashboard
- `EPIC-01-STORY-05` Release 2 prep: a Postgres database per project (schema, provisioning, lifecycle)
- `EPIC-01-STORY-06` Release 2 prep: organise session and decision history across coordinators and developers
- `EPIC-01-STORY-07` Release 2 prep: review the release list and plan the program epics and stories

Each feature body names the BMAD workflow that starts its user-story planning and the hand-off to IronClaude.

## How this epic is planned and run

Split of work (proposed in the pipeline; final text in shared/CONSENSUS.md): BMAD owns the higher-level planning (PRD feature groups, architecture invariants, epics, user stories with acceptance criteria, order, the sprint-status ledger). IronClaude owns implementation planning and execution (design brainstorm, `/sc:workflow` tasklist, `/sc:implement`, tests, PR review, closeout) and rapid iteration. IronClaude does not contradict an architecture `AD-n`; a needed change goes back through `/bmad-correct-course`.

Program run order (details in agent1/RELEASE-PLAN.md S4.1): `/bmad-help`, `/bmad-generate-project-context`, `/bmad-investigate`, `/bmad-market-research` and `/bmad-technical-research`, `/bmad-forge-idea`, `/bmad-prd` (Update), `/bmad-ux`, `/bmad-architecture` (Update) with `/sc:brainstorm ... --depth deep`, `/bmad-spec`, an independent review, `/bmad-create-epics-and-stories` (EPIC-01 and EPIC-02 only), `/bmad-check-implementation-readiness`, `/bmad-sprint-planning`.

## Progress

- [ ] Owner scheduled this release (recorded in chat)
- [ ] Epic and feature issues filed; native sub-issue links made
- [ ] Stories written and ready
- [ ] Program PRD, UX and architecture spine reviewed and final
- [ ] SPEC and companions derived and reviewed
- [ ] Epics for EPIC-01 and EPIC-02 and sprint-status.yaml created
- [ ] All features closed; `/bmad-retrospective` done; open action items filed
