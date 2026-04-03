# Synthesis Mapping Reference

> Output Structure reference and Synthesis Mapping Table, loaded during Stage A.7 by the builder subagent.
> Extracted verbatim from SKILL.md lines 969-1106.

---

## Output Structure

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The final PRD follows the template at `src/superclaude/examples/prd_template.md`. The synthesis agents produce sections that are assembled into this format.

```markdown
---
[frontmatter from template]
---

# [Product Name] - Product Requirements Document (PRD)

> HOW TO USE THIS DOCUMENT: [preamble blockquote]

---

## Document Information
Project specifics table: Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence.

## Table of Contents
[Generated from section headers]

---

## 1. Executive Summary
2-3 paragraph summary with Key Success Metrics.

## 2. Problem Statement
Core problem, why existing solutions fall short, market opportunity.

## 3. Background & Strategic Fit
Why now, company objective alignment, strategic bets.

## 4. Product Vision
One-sentence vision statement with expansion.

## 5. Business Context
Market opportunity (TAM/SAM/SOM), business objectives, KPIs.

## 6. Jobs To Be Done (JTBD)
Primary jobs in When/I want/So that format, related jobs table.

## 7. User Personas
Primary, secondary, tertiary personas with attribute tables; anti-personas.

## 8. Value Proposition Canvas
Customer profile, value map (pain relievers + gain creators), fit assessment.

## 9. Competitive Analysis
Competitive landscape table, feature comparison matrix, positioning statement, response plan.

## 10. Assumptions & Constraints
Technical, business, and user assumptions with risk-if-wrong; constraints table.

## 11. Dependencies
External, internal, and cross-team dependency tables.

## 12. Scope Definition
In scope, out of scope, permanently out of scope.

## 13. Open Questions
Question tracking table with owner, status, resolution.

## 14. Technical Requirements
Architecture, performance, security, scalability, data & analytics requirements.

## 15. Technology Stack
Backend, frontend, infrastructure technology tables.

## 16. User Experience Requirements
Onboarding metrics, core user flows, accessibility, localization.

## 17. Legal & Compliance Requirements
Regulatory compliance, data privacy, terms & policies.

## 18. Business Requirements
Monetization strategy, pricing tiers, go-to-market, support requirements.

## 19. Success Metrics & Measurement
Product, business, and technical metrics with targets and measurement frequency.

## 20. Risk Analysis
Technical, business, and operational risk matrices with mitigations.

## 21. Implementation Plan
Consolidated delivery plan: 21.1 Epics, Features & Stories (epic summary, user stories with acceptance criteria), 21.2 Product Requirements (core features, RICE matrix), 21.3 Implementation Phasing, 21.4 Release Criteria & DoD, 21.5 Timeline & Milestones.

## 22. Customer Journey Map
Journey stages table, moments of truth.

## 23. Error Handling & Edge Cases
Error categories, edge case scenarios, graceful degradation plan.

## 24. User Interaction & Design
Wireframes/mockups table, design system checklist, prototype links.

## 25. API Contract Examples
Key endpoint request/response examples.

## 26. Contributors & Collaboration
Contributor table, how to contribute guidelines.

## 27. Related Resources
Customer research, technical docs, design assets, business documents.

## 28. Maintenance & Ownership
Document ownership, review cadence, update process.

## Appendices
Glossary, Acronyms, Technical Architecture Diagrams, User Research Data, Financial Projections.

## Document Approval
Approval signature table.
```

---

## Synthesis Mapping Table (Reference)

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

This is the standard mapping of synthesis files to PRD template sections. Adjust based on product complexity — small features can combine more sections per synth file, large platform PRDs may need additional synth files for additional product areas.

| Synth File | Template Sections | Source Research Files |
|------------|-------------------|----------------------|
| `synth-01-exec-problem-vision.md` | 1. Executive Summary, 2. Problem Statement, 3. Background & Strategic Fit, 4. Product Vision | product capabilities, web research (market context), existing docs |
| `synth-02-business-market.md` | 5. Business Context, 6. JTBD, 7. User Personas, 8. Value Proposition Canvas | user flows, web research (market context), product capabilities |
| `synth-03-competitive-scope.md` | 9. Competitive Analysis, 10. Assumptions & Constraints, 11. Dependencies, 12. Scope Definition | web research (competitive landscape), technical stack, integration points |
| `synth-04-stories-requirements.md` | 13. Open Questions, 21.1 Epics Features & Stories, 21.2 Product Requirements | per-area research files, user flows, gaps log |
| `synth-05-technical-stack.md` | 14. Technical Requirements, 15. Technology Stack | technical stack, architecture research, web research (technology trends) |
| `synth-06-ux-legal-business.md` | 16. UX Requirements, 17. Legal & Compliance, 18. Business Requirements | user flows, product capabilities, web research (compliance, market) |
| `synth-07-metrics-risk-impl.md` | 19. Success Metrics, 20. Risk Analysis, 21.3 Implementation Phasing, 21.4 Release Criteria & DoD, 21.5 Timeline & Milestones | all research files, web research, technical stack |
| `synth-08-journey-design-api.md` | 22. Customer Journey, 23. Error Handling, 24. User Interaction, 25. API Contracts | user flows, per-area research, technical stack |
| `synth-09-resources-maintenance.md` | 26. Contributors, 27. Related Resources, 28. Maintenance & Ownership | existing docs, all research files, gaps log |
