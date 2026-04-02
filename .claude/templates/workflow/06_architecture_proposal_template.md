# Architecture Proposal: [PROJECT_NAME]

> **This is a planning artifact, NOT an MDTM task file.**
> Produced during Phase 0 (Planning) of the `/rf:project` pipeline.
> Template: `.claude/templates/workflow/06_architecture_proposal_template.md`
>
> **CRITICAL**: The "Suggested Phases" section at the end of this document directly drives
> the project plan's phase breakdown. The team lead uses it to create the project plan
> (template 03). Be specific and actionable in that section.

---

**Version:** [1.0]
**Status:** [Draft | In Review | Approved]
**Date:** [YYYY-MM-DD]

## References

- **Feature Brief**: [path to phase-outputs/reports/feature-brief.md]
- **PRD**: [path to phase-outputs/reports/prd.md]
- **Codebase Inventory**: [path to phase-outputs/discovery/codebase-inventory.md]
- **Research Notes**: [path to research notes file]

---

## Executive Summary

[2-3 paragraphs providing a high-level overview of the proposed architecture. What is being built, what approach was chosen, and why. A reader should understand the overall shape of the solution after reading this section.]

---

## System Context

### Existing System

[Describe the relevant parts of the existing codebase/system that this project integrates with. What already exists that we build on, connect to, or must not break.]

### Integration Points

| Integration Point | Type | Description |
|-------------------|------|-------------|
| [Component/system name] | [API/import/event/file] | [How this project connects to it] |
| [...] | [...] | [...] |

---

## Component Architecture

### Component: [COMPONENT_1_NAME]

- **Responsibility**: [What this component does]
- **Key Interfaces**: [Public API, events emitted, data consumed/produced]
- **Files to Create/Modify**:
  - `[path/to/new_file.ext]` — [purpose]
  - `[path/to/existing_file.ext]` — [what changes and why]
- **Dependencies**:
  - Internal: [other components this depends on]
  - External: [libraries, services]

### Component: [COMPONENT_2_NAME]

- **Responsibility**: [What this component does]
- **Key Interfaces**: [Public API, events emitted, data consumed/produced]
- **Files to Create/Modify**:
  - `[path/to/file.ext]` — [purpose]
- **Dependencies**:
  - Internal: [...]
  - External: [...]

<!-- Add more components as needed -->

---

## Directory / File Structure

```
[Proposed file layout for new/modified files]

project-root/
├── [path/to/new-directory/]
│   ├── [file1.ext]          # [purpose]
│   ├── [file2.ext]          # [purpose]
│   └── [file3.ext]          # [purpose]
├── [path/to/existing-dir/]
│   ├── [existing-file.ext]  # [modification description]
│   └── [new-file.ext]       # [purpose]
└── [tests/]
    └── [test-files.ext]     # [what they test]
```

---

## Data Flow

[Describe how data moves through the system. Can be a text description of the flow, a numbered sequence, or an ASCII diagram.]

```
[Input Source] → [Component A] → [Component B] → [Output/Storage]
                      ↓
              [Side Effect/Event]
```

1. [Step 1: Data enters the system via...]
2. [Step 2: Component A processes it by...]
3. [Step 3: Result is passed to Component B which...]
4. [Step N: Final output is...]

---

## Technology Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| [What decision was made] | [What was chosen] | [Why this choice] | [What else was considered] |
| [...] | [...] | [...] | [...] |

---

## Implementation Considerations

### Patterns to Follow

- [Existing pattern in the codebase to be consistent with, e.g., "Follow the handler pattern in src/handlers/"]
- [Design pattern to use, e.g., "Repository pattern for data access"]
- [...]

### Error Handling

- [Error handling approach, e.g., "Use existing error middleware for API errors"]
- [Edge cases to handle, e.g., "Graceful degradation when external service is unavailable"]

### Testing Strategy

- [Unit testing approach, e.g., "One test file per module in tests/unit/"]
- [Integration testing approach, e.g., "API tests using test fixtures in tests/integration/"]
- [What to test, e.g., "All public interfaces, error paths, edge cases"]

---

## Suggested Phases

> **CRITICAL**: This section drives the project plan (template 03). The team lead reads this
> to create concrete execution phases. Be specific about what each phase delivers and what
> it depends on.

### Phase 1: [PHASE_NAME]

- **Goal**: [What this phase accomplishes — be specific]
- **Key Deliverables**:
  - [File or component created/modified]
  - [File or component created/modified]
- **Dependencies**: [What must exist before this phase can start, e.g., "None — first implementation phase"]
- **Outputs**: [What this phase produces that later phases need]
- **Suggested Template**: [01 or 02 — 01 for straightforward file creation, 02 if phase needs discovery/testing/review]
- **Estimated Complexity**: [Low/Medium/High]

### Phase 2: [PHASE_NAME]

- **Goal**: [What this phase accomplishes]
- **Key Deliverables**:
  - [...]
- **Dependencies**: [e.g., "Phase 1 outputs: core module must exist"]
- **Outputs**: [...]
- **Suggested Template**: [01 or 02]
- **Estimated Complexity**: [Low/Medium/High]

<!-- Add more phases as needed. Common progression:
Phase 1-N: Core Implementation (one phase per major component or layer)
Phase N+1: Testing & Validation
Phase N+2: Integration & Polish
Phase N+3: Documentation
-->

### Phase [N+1]: Testing & Validation

- **Goal**: Run tests, validate all components work together
- **Key Deliverables**:
  - [Test files, test results, coverage reports]
- **Dependencies**: [All implementation phases complete]
- **Outputs**: [Test results, identified issues]
- **Suggested Template**: 02 (needs test execution + conditional flows)
- **Estimated Complexity**: [Medium/High]

### Phase [N+2]: Documentation

- **Goal**: Create/update documentation for the new feature
- **Key Deliverables**:
  - [Documentation files]
- **Dependencies**: [Implementation and testing complete]
- **Outputs**: [Documentation artifacts]
- **Suggested Template**: 01 (straightforward file creation)
- **Estimated Complexity**: [Low/Medium]

---

## Risks & Technical Debt

| # | Risk/Debt | Type | Impact | Mitigation/Plan |
|---|-----------|------|--------|-----------------|
| 1 | [What could go wrong or what debt this introduces] | [Risk/Debt] | [Low/Med/High] | [How to handle] |
| 2 | [...] | [...] | [...] | [...] |

---

## Alternatives Considered

### Alternative 1: [APPROACH_NAME]

- **Description**: [What this approach would look like]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Why Rejected**: [Specific reason this wasn't chosen]

### Alternative 2: [APPROACH_NAME]

- **Description**: [...]
- **Pros**: [...]
- **Cons**: [...]
- **Why Rejected**: [...]
