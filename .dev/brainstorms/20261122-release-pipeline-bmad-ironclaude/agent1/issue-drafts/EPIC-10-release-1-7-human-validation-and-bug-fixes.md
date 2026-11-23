Title: [EPIC] Release 1.7: human validation, bug filing and fixes
Draft id: EPIC-10
Parent: umbrella #727 (native sub-issue)
Labels: enhancement, epic (new), release:1.7 (new)
Issue type: Feature
Complexity (proposed): Complex
Release: Release 1.7
Schedule state: UNSCHEDULED (file only when the owner schedules this release)
Status: DRAFT on disk. Do not file until the owner schedules this release.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727. Owner's item, close to verbatim: Human testing, Bug filing a fixing for version 1.7.

State read on 2026-11-22 (so the next person starts from facts): the observer dashboard (`superclaude observe`) is read-only by design and keeps no database; questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder (issue #727, section "State read"). The observer code is on origin/master under `src/superclaude/cli/observe/` with tests in `tests/observe/`.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`
- Cycle template: validation cycle (agent1/RELEASE-PLAN.md S3.4)
- BMAD precedent on origin/master: `.dev/issues/409/bmad/` (prd-orca-observer, ux-orca-observer, architecture-orca-observer, spec-orca-observer with SPEC.md and 11 companions, final-review, handoff-step1.md to handoff-step5.md, `final-review/workflow-input.md`)

## Done when

- The release 1.6 build is validated by hand against a written guide; every failure is filed or dismissed with a reason.
- No high or medium bug is open (or the owner recorded an exception); every fix has a regression test.
- Release 1.7 is recorded and the retrospective is done.

## Pick-up note

Starts only after the owner schedules this release. Inputs: the build under test and the previous cycle's retrospective action items. The next tests cycle uses this epic's bug list.

Do not build anything from this epic before the owner says go (owner's order in issue #727). Release 2 prep (EPIC-01) takes precedence over every other epic.

## Features (sub-issues, in order)

- `EPIC-10-STORY-01` Release 1.7: human test pass of the release 1.6 build
- `EPIC-10-STORY-02` Release 1.7: file and triage bugs from the test pass
- `EPIC-10-STORY-03` Release 1.7: fix the high and medium bugs
- `EPIC-10-STORY-04` Release 1.7: cut the release and run the retrospective

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
