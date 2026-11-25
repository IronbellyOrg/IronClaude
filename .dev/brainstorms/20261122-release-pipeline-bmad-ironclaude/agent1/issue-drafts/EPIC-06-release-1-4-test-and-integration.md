Title: [EPIC] Release 1.4: testing and integration (Zellij and Coder canvas, per the EPIC-05 decision)
Draft id: EPIC-06
Parent: umbrella #727 (native sub-issue)
Labels: enhancement, epic (new), release:1.4 (new)
Issue type: Feature
Complexity (proposed): Complex
Release: Release 1.4
Schedule state: UNSCHEDULED; conditional on EPIC-05
Status: DRAFT on disk. Do not file until the owner schedules this release.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727. Owner's item, close to verbatim: Planning testing and integration for a 1.4 release

State read on 2026-11-22 (so the next person starts from facts): the observer dashboard (`superclaude observe`) is read-only by design and keeps no database; questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder (issue #727, section "State read"). The observer code is on origin/master under `src/superclaude/cli/observe/` with tests in `tests/observe/`.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`

## Done when

- The testing and integration plan is written and approved.
- The integrations the owner approved are built and tested; release 1.4 is recorded.

## Pick-up note

Conditional features are dropped when the EPIC-05 record says no-go or later. The owner's wording names planning only; building is proposed here because a release needs it. Confirm with the owner when scheduling.

Do not build anything from this epic before the owner says go (owner's order in issue #727). Release 2 prep (EPIC-01) takes precedence over every other epic.

## Features (sub-issues, in order)

- `EPIC-06-STORY-01` Release 1.4: plan the testing and integration
- `EPIC-06-STORY-02` Release 1.4: run the dashboard in Zellij (only if EPIC-05 says go)
- `EPIC-06-STORY-03` Release 1.4: add the Coder workspace canvas button (only if EPIC-05 says go)
- `EPIC-06-STORY-04` Release 1.4: integration tests for what 1.4 adds
- `EPIC-06-STORY-05` Release 1.4: cut the release and run the retrospective

Each feature body names the BMAD workflow that starts its user-story planning and the hand-off to IronClaude.

## How this epic is planned and run

Split of work (proposed in the pipeline; final text in shared/CONSENSUS.md): BMAD owns the higher-level planning (PRD feature groups, architecture invariants, epics, user stories with acceptance criteria, order, the sprint-status ledger). IronClaude owns implementation planning and execution (design brainstorm, `/sc:workflow` tasklist, `/sc:implement`, tests, PR review, closeout) and rapid iteration. IronClaude does not contradict an architecture `AD-n`; a needed change goes back through `/bmad-correct-course`.

BMAD run for this epic (details in agent1/RELEASE-PLAN.md S4.2):
1. `/bmad-help` to orient.
2. `/bmad-correct-course` when the previous cycle changed scope; `/bmad-prd` (Update) when requirements change; `/bmad-architecture` (Update) when an invariant changes.
3. `/bmad-create-epics-and-stories` for this epic only (stories written just in time from the previous cycle's output; see risk R1 and R2 in the plan).
4. `/bmad-check-implementation-readiness`, then `/bmad-sprint-planning`.
5. Hand-off per feature (packet, story issues, IronClaude chain), write-back as stories finish.
6. `/bmad-sprint-status` any time; `/bmad-retrospective` at epic end.

## Progress

- [ ] Owner scheduled this release (recorded in chat)
- [ ] Epic and feature issues filed; native sub-issue links made
- [ ] Stories written and ready

- [ ] All features closed; `/bmad-retrospective` done; open action items filed
