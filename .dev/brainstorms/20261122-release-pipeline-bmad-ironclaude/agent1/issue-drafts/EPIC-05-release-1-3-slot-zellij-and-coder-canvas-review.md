Title: [EPIC] Zellij port and Coder workspace canvas button: review and go or no-go
Draft id: EPIC-05
Parent: umbrella #727 (native sub-issue)
Labels: enhancement, epic (new), release:1.3 (new)
Issue type: Feature
Complexity (proposed): Medium
Release: Release 1.3 slot (unnumbered in the owner's list)
Schedule state: UNSCHEDULED (file only when the owner schedules it)
Status: DRAFT on disk. Do not file until the owner schedules this release.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727. Owner's item, close to verbatim: Review porting dashboard to Zelij and accessing it directly from Coder Workspace canvas with a new button

State read on 2026-11-22 (so the next person starts from facts): the observer dashboard (`superclaude observe`) is read-only by design and keeps no database; questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder (issue #727, section "State read"). The observer code is on origin/master under `src/superclaude/cli/observe/` with tests in `tests/observe/`.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`
- #606 (closed; holds the Zellij go or no-go)

## Done when

- Zellij and the canvas button are reviewed with sources.
- The owner has recorded go, no-go or later for each, and EPIC-06 scope matches.

## Pick-up note

Review only. Nothing is built. The version number of this slot is the draft's reading (owner gave none).

Do not build anything from this epic before the owner says go (owner's order in issue #727). Release 2 prep (EPIC-01) takes precedence over every other epic.

## Features (sub-issues, in order)

- `EPIC-05-STORY-01` 1.3 slot: review porting the dashboard to Zellij
- `EPIC-05-STORY-02` 1.3 slot: review opening the dashboard from the Coder workspace canvas with a new button
- `EPIC-05-STORY-03` 1.3 slot: owner go or no-go record for Zellij and the canvas button, and the scope of 1.4

Each feature body names the BMAD workflow that starts its user-story planning and the hand-off to IronClaude.

## How this epic is planned and run

Split of work (proposed in the pipeline; final text in shared/CONSENSUS.md): BMAD owns the higher-level planning (PRD feature groups, architecture invariants, epics, user stories with acceptance criteria, order, the sprint-status ledger). IronClaude owns implementation planning and execution (design brainstorm, `/sc:workflow` tasklist, `/sc:implement`, tests, PR review, closeout) and rapid iteration. IronClaude does not contradict an architecture `AD-n`; a needed change goes back through `/bmad-correct-course`.

Run order: `/bmad-help`, `/bmad-technical-research` (twice), `/bmad-forge-idea`, `/bmad-correct-course`. No stories or hand-off: the output is a decision.

## Progress

- [ ] Owner scheduled this release (recorded in chat)
- [ ] Epic and feature issues filed; native sub-issue links made
- [ ] Stories written and ready

- [ ] All features closed; `/bmad-retrospective` done; open action items filed
