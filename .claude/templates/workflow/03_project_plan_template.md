# Project: [PROJECT_NAME]

> **This is a project management document, NOT an MDTM task file.**
> Created and maintained by the team lead throughout the `/rf:project` lifecycle.
> Template: `.claude/templates/workflow/03_project_plan_template.md`

---

## Project Goal

[Full description of what the user wants to build. Include the original request and any clarifications gathered during intake.]

## Project Context

- **Created**: [YYYY-MM-DD HH:MM]
- **Status**: [planning | active | complete | failed | cancelled]
- **Team**: [team name, e.g., rf-pipeline]
- **Tracks**: [single | multi — number of parallel work streams if applicable]

## Planning Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Feature Brief | [path, filled after Phase 0] | [pending/complete] |
| PRD | [path, filled after Phase 0] | [pending/complete] |
| Architecture Proposal | [path, filled after Phase 0] | [pending/complete] |

## Phases

### Phase 0: Planning — [pending|active|complete|failed]

- **Goal**: Produce feature brief, PRD, and architecture proposal
- **Task File**: [path, filled after builder creates it]
- **Template Used**: 02
- **Outputs**:
  - Feature Brief: [path]
  - PRD: [path]
  - Architecture Proposal: [path]
- **Fix Cycles**: 0
- **Notes**: [review notes, decisions made]

---

### Phase 1: [PHASE_NAME] — [pending|active|complete|failed|skipped]

- **Goal**: [What this phase accomplishes]
- **Inputs**: [Artifacts from planning + previous phases that this phase depends on]
- **Task File**: [path, filled after builder creates it]
- **Template Used**: [01 or 02]
- **Outputs**: [paths to files created, filled after execution]
- **Fix Cycles**: [count, 0 if clean pass]
- **Notes**: [review notes, issues encountered, decisions]

---

### Phase 2: [PHASE_NAME] — [pending|active|complete|failed|skipped]

- **Goal**: [What this phase accomplishes]
- **Inputs**: [Artifacts from previous phases]
- **Task File**: [path]
- **Template Used**: [01 or 02]
- **Outputs**: [paths]
- **Fix Cycles**: [count]
- **Notes**: [notes]

---

<!-- Add more phases as needed. Common progression:
Phase 0: Planning (always first)
Phase 1-N: Core Implementation (derived from architecture proposal)
Phase N+1: Testing & Validation
Phase N+2: Integration & Polish
Phase N+3: Documentation
-->

## Execution Log

| Phase | Started | Task File | Items | QA Passes | Fix Cycles | Status | Completed |
|-------|---------|-----------|-------|-----------|------------|--------|-----------|
| 0 - Planning | | | | | | pending | |
| 1 - [name] | | | | | | pending | |
| 2 - [name] | | | | | | pending | |

## Agent Roster

| Role | Agent Name | Spawned | Status |
|------|-----------|---------|--------|
| Researcher | researcher | [timestamp] | [active/idle/shutdown] |
| Builder | builder | [timestamp] | [active/idle/shutdown] |
| Executor | executor | [timestamp] | [active/idle/shutdown] |

> Agents are spawned ONCE during Phase 0 and reused across all phases via SendMessage.

## Cross-Phase Handoff Log

| From Phase | To Phase | Artifact | Path | Description |
|------------|----------|----------|------|-------------|
| 0 (Planning) | 1 | Architecture Proposal | [path] | Defines implementation approach |
| 0 (Planning) | 1 | PRD | [path] | Requirements reference |
| 1 | 2 | [artifact name] | [path] | [what it provides to next phase] |

## Issues & Blockers

| Phase | Issue | Resolution | Status |
|-------|-------|------------|--------|
| | | | |

## Final Summary

> Filled by team lead when project completes.

- **Total Phases**: [count]
- **Total Task Files**: [count]
- **Total Fix Cycles**: [sum across all phases]
- **All Outputs Created**:
  - [list of all deliverable files with paths]
- **Follow-Up Work Identified**:
  - [any remaining items not covered by this project]
