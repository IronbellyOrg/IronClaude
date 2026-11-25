Title: [EPIC] Release 1.8: first write and respond features (decision cards, notices, answer delivery)
Draft id: EPIC-12
Parent: umbrella #727 (native sub-issue)
Labels: enhancement, epic (new), release:1.8 (new)
Issue type: Feature
Complexity (proposed): Complex
Release: Release 1.8
Schedule state: UNSCHEDULED (file only when the owner schedules this release)
Status: DRAFT on disk. Do not file until the owner schedules this release.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727. Owner's item, close to verbatim: Planning, brainstorming and implementation of first write/Respond features for a 1.8 release. This will involve boiling the coordinators needs into digestible multiple choice or binary decisions to the user or notifications that the user is needed in the coordinator session for a q&a or longer conversation

State read on 2026-11-22 (so the next person starts from facts): the observer dashboard (`superclaude observe`) is read-only by design and keeps no database; questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder (issue #727, section "State read"). The observer code is on origin/master under `src/superclaude/cli/observe/` with tests in `tests/observe/`.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Related: #726 (a vote on each question, kept as a local record; the owner ruled in chat on 2026-11-22 that the read-only rule is relaxed and the dashboard is meant to become two-way; the vote waits for the architecture and storage evaluation in #727)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`
- Related open issues: #409 (TUI dashboard), #706 (observer follow-up), #604 (observer remote fleet), #716 (coordinator next release), #717 (issue watcher), #718 (dashboard items from the 655 split)

## Done when

- Coordinator questions are classified into binary, multiple-choice and needs-the-session.
- A person can answer a binary or multiple-choice question in the dashboard, the answer reaches the coordinator and is stored; a needed-in-session notice exists.
- Release 1.8 is recorded and the retrospective is done.

## Pick-up note

Planning, brainstorming and implementation are all in the owner's text; the first two features are planning and decision features and must pass an independent review before any code story is handed over.

Do not build anything from this epic before the owner says go (owner's order in issue #727). Release 2 prep (EPIC-01) takes precedence over every other epic.

## Features (sub-issues, in order)

- `EPIC-12-STORY-01` Release 1.8: boil the coordinator's needs down to binary, multiple-choice or 'you are needed' decisions
- `EPIC-12-STORY-02` Release 1.8: change the read-only boundary: architecture and PRD for the write path
- `EPIC-12-STORY-03` Release 1.8: decision cards: answer binary and multiple-choice questions in the dashboard
- `EPIC-12-STORY-04` Release 1.8: deliver the answer to the coordinator session
- `EPIC-12-STORY-05` Release 1.8: a notice when the person is needed in the coordinator session
- `EPIC-12-STORY-06` Release 1.8: keep decisions in the project database (builds on Release 2 prep)
- `EPIC-12-STORY-07` Release 1.8: fold in the vote on each question (issue 726)
- `EPIC-12-STORY-08` Release 1.8: cut the release and run the retrospective

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
