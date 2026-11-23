Title: [EPIC] Release 2.0: implement the 1.9 feedback and additional write and respond features
Draft id: EPIC-15
Parent: umbrella #727 (native sub-issue)
Labels: enhancement, epic (new), release:2.0 (new)
Issue type: Feature
Complexity (proposed): Complex
Release: Release 2.0
Schedule state: UNSCHEDULED (file only when the owner schedules this release)
Status: DRAFT on disk. Do not file until the owner schedules this release.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727. Owner's item, close to verbatim: Implement feedback from 1.9 and additional write/respond features for 2.0 release

State read on 2026-11-22 (so the next person starts from facts): the observer dashboard (`superclaude observe`) is read-only by design and keeps no database; questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder (issue #727, section "State read"). The observer code is on origin/master under `src/superclaude/cli/observe/` with tests in `tests/observe/`.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`
- Related: #726 (a vote on each question, kept as a local record; its open decision is whether the read-only rule may be relaxed)

## Done when

- The accepted feedback of 1.9 is built.
- Demands to the coordinator and project history in the dashboard exist.
- Release 2.0 is recorded and the retrospective is done.

## Pick-up note

After 2.0 (owner's text): user feedback systems to gather data used to fine tune when and how the person is prompted. Not planned in this plan.

Do not build anything from this epic before the owner says go (owner's order in issue #727). Release 2 prep (EPIC-01) takes precedence over every other epic.

## Features (sub-issues, in order)

- `EPIC-15-STORY-01` Release 2.0: absorb the feedback and feature requests of 1.9
- `EPIC-15-STORY-02` Release 2.0: demands to the coordinator (more context, explanation, debate, validation, research, fact check, plugins)
- `EPIC-15-STORY-03` Release 2.0: show what other coordinators decided (project history in the dashboard)
- `EPIC-15-STORY-04` Release 2.0: additional write and respond features from the 1.9 feedback
- `EPIC-15-STORY-05` Release 2.0: cut the release, run the retrospective and record what comes after 2.0

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
