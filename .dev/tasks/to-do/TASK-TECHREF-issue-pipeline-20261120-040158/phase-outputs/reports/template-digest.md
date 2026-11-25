# Template digest (technical_reference_template.md v1.0.2)

Source: /home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md (read in full, 707 lines).

## Frontmatter fields (in order)
id, title, description, version, status, type, priority, created_date, updated_date, assigned_to, autogen, autogen_method, coordinator, parent_doc, parent_task, related_prd, related_tdd, depends_on[], related_docs[], tags[], template_schema_doc, estimation, sprint, due_date, start_date, completion_date, blocker_reason, ai_model, model_settings, review_info{last_reviewed_by,last_review_date,next_review_date}, task_type (static).

## Front blocks before Section 1
Title, WHAT/WHY/HOW TO USE callout, Document Lifecycle Position table (Phase | Document | Ownership | Status), Tiered Usage table (Tier | When to Use | Sections Required), Document Information table (Field | Value: Feature Name, Feature Type, Tech Lead, Engineering Team, Maintained By, Source Location, Last Verified Against Code, Implementation Status), Living Document Contract list, Completeness Status checklist (Sections 1-16, links verified, reviewed) plus Contract Table (Element | Details: Dependencies, Upstream, Downstream, Change Impact, Review Cadence), Table of Contents (1-16).

## Sections and required tables
1. Overview: 2-3 paragraphs; What it does / Who uses it / Where it lives / Key numbers.
2. Architecture: 2.1 High-Level Architecture (diagram); 2.2 Subsystem Map (Subsystem | Purpose | Primary Directory | Key Files); 2.3 Key Design Decisions (As Built) (Decision | What Was Built | Rationale | TDD Divergence); 2.4 Technology Stack (Technology | Version | Purpose in This Feature).
3. Directory Structure: tree without file counts; 3.1 File Naming Conventions (Pattern | Convention | Example).
4. Data Flow: 4.1 Primary Data Flow (diagram + narrative); 4.2 Data Sources (Source | Type | Location | Description); 4.3 Data Transformations (Transformation | Input | Output | Location | Description).
5. Subsystem Reference: per subsystem 5.N: Purpose; Key Files (File | Purpose); How It Works; Public Interface; Dependencies (Depends On | Type | Description); Consumers (Used By | How); Conventions & Patterns. Depth 40-80 simple, 80-120 standard, 120-200 complex lines.
6. State Management (if applicable): 6.1 State Architecture (Store/Slice | Library | Scope | Primary Purpose); 6.2 State Shape (Slice | Key Fields | Notable Behavior); 6.3 Key State Transitions (Trigger | From State | To State | Side Effects); 6.4 Cross-Store Dependencies (Source Store | Consumer Store | Relationship | Description). Under 150 lines. For this feature: rendered as a table of the three on-disk stores (watcher state_dir files; ~/.claude/state/launch-level/{pending,sessions,requests,jobs}; .dev/issues/<N>/ claim artefacts).
7. Component Inventory (if applicable, frontend). For this feature: N/A, rationale "not a UI feature".
8. API & Integration Points: 8.1 API Endpoints Used (Endpoint | Method | Purpose | Request Shape | Response Shape); 8.2 Internal Integration Points (Integration | Direction | Mechanism | Description); 8.3 External Service Dependencies (Service | Purpose | Failure Mode | Fallback).
9. Configuration & Environment: 9.1 Configuration Files (File | Purpose | Key Settings); 9.2 Environment Variables (Variable | Purpose | Default | Required); 9.3 Feature Flags (Flag | Description | Default | Impact When Toggled).
10. Error Handling & Edge Cases: 10.1 Error Handling Patterns (Error Category | Handling Pattern | User Experience | Recovery); 10.2 Known Edge Cases (Scenario | Current Behavior | Notes); 10.3 Graceful Degradation (Failure | Impact | Degraded Experience).
11. Performance Characteristics: 11.1 Performance Profile (Metric | Measured Value | Measurement Method | Notes); 11.2 Performance-Critical Code (Area | Optimization | Why It Matters | Location); 11.3 Asset Management (if applicable).
12. Conventions & Patterns: 12.1 Code Conventions (Convention | Description | Example); 12.2 Architectural Patterns (Pattern | Where Used | Description); 12.3 Anti-Patterns (Anti-Pattern | Why It's Wrong | Do This Instead).
13. Extension Guide: 13.1 Common Extension Tasks (Task | Steps | Files to Touch | Pitfalls); 13.2 Testing Requirements for Changes (Change Type | Required Tests | Test Location).
14. Known Limitations & Technical Debt: 14.1 Current Limitations (Limitation | Impact | Workaround | Planned Fix); 14.2 Technical Debt (Item | Severity | Description | Effort to Fix); 14.3 Future Considerations (Item | Deferred Because | Revisit When). NOTE: the template's sub-sections are 14.1-14.3 as listed; synthesis prompts in this task may define extra sub-sections; the assembler must reconcile to the template names.
15. Verification & Accuracy (mandatory): 15.1 Verification Log (Date | Verified By | Code Version / Commit | Sections Verified | Issues Found); 15.2 Spot-Check Protocol (5 numbered checks).
16. Glossary (Term | Definition).
Appendices (Appendix A: Title ...); Document History (Version | Date | Author | Changes).

## Content rules
Tables over prose; no reproduced source code (summaries and key signatures only); key numbers stated once in Section 1; ASCII or Mermaid diagrams; inline evidence `path:line`; explicit Unverified / Open Question markers; each concept described in exactly one section; callout conventions Note / Important / CRITICAL / Tip; line budget Standard 800-1,200 lines (documents over 2,000 lines are a code smell).
