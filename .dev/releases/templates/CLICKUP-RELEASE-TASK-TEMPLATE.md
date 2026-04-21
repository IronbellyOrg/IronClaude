# ClickUp Release Task Template

> **Usage:** Copy this template for each release in `.dev/releases/backlog/`. Fill in the bracketed placeholders. Delete any sections not applicable. This maps to a ClickUp task in User Story format, scoped to roadmap milestones/phases only (no granular tasklist breakdown).

---

## Title

`[Release ID]: [Short descriptive title]`

---

## User Story

**As a** [role — e.g., developer using the SuperClaude pipeline],
**I want** [what this release delivers — one sentence],
**So that** [the outcome / value it produces].

---

## Problem Statement

### What is broken or missing

[Describe the core problem in 2-4 sentences. Be specific about symptoms, not just root causes.]

### Pipeline stage affected

```
spec/prd/tdd  -->  roadmap  -->  tasklist  -->  sprint run
                   ^^^^^^^
              [Mark which stage(s) this release targets]
```

### Evidence

| Observation | Data / Source |
|-------------|---------------|
| [Key metric or symptom 1] | [Where this was measured or observed] |
| [Key metric or symptom 2] | [Source] |

---

## What Changes

### Pipeline modifications

| Stage | Change | How it improves the flow |
|-------|--------|-------------------------|
| [e.g., Extraction] | [What gets modified] | [Expected improvement] |
| [e.g., Roadmap Generation] | [What gets modified] | [Expected improvement] |

### Key architectural decisions

- [Decision 1 — one line each, e.g., "Switch from one-shot output to incremental tool-use writing"]
- [Decision 2]

---

## Milestones & Phases

| Phase | Description | Expected Outcome | Done when |
|-------|-------------|-------------------|----------|
| Phase 1 | [Name + short description] | [What is produced / measurable result] | [Acceptance criteria] |
| Phase 2 | [Name + short description] | [What is produced / measurable result] | [Acceptance criteria] |
| Phase 3 | [Name + short description] | [What is produced / measurable result] | [Acceptance criteria] |

> Add or remove rows as needed. Each phase should be independently verifiable.

---

## Dependencies & Risks

| Item | Type | Detail |
|------|------|--------|
| [e.g., "v3.5 prompt fixes"] | Dependency | [Must be completed before Phase X] |
| [e.g., "LLM output variability"] | Risk | [Mitigation approach] |

---

## Research & Artifacts

| Artifact | Location | Summary |
|----------|----------|---------|
| [e.g., Research report] | [Relative path or link] | [One-line summary] |
| [e.g., Test fixtures] | [Relative path or link] | [One-line summary] |

---

## Definition of Done

- [ ] [Primary acceptance criterion — measurable]
- [ ] [Secondary criterion]
- [ ] [Regression check — existing functionality not broken]

---

## Next Release

**[Next release ID]: [Title]**

[1-3 sentences describing what comes next and how this release feeds into it. Include the path to the next release's backlog folder if available.]

---

*Template version: 1.0 | Source: `.dev/releases/templates/CLICKUP-RELEASE-TASK-TEMPLATE.md`*
