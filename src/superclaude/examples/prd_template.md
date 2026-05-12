---
id: "[PROJECT-ID]-PRD-CORE"
title: "[Product Name] - Product Requirements Document (PRD)"
description: "Foundational cross-cutting requirements, product principles, user stories, and core platform standards"
version: "1.0"
status: "🟡 Draft"
type: "📋 Product Requirements"
priority: "🔥 Highest"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "product-team"
autogen: false
autogen_method: ""
coordinator: "product-manager"
parent_task: ""
depends_on:
- "[list dependent documents]"
related_docs:
- "[list related documents]"
tags:
- prd
- requirements
- product-core
- user-stories
- acceptance-criteria
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: "static"
---

# [Product Name] - Product Requirements Document (PRD)

> **WHAT:** [One sentence — what this document contains, e.g., "Foundational product requirements, user stories, and acceptance criteria for [Product Name]."]
> **WHY:** [One sentence — why this document exists, e.g., "Serves as the single source of truth for product scope, priorities, and success criteria."]
> **HOW TO USE:** [One sentence — who should use it and when, e.g., "Product, engineering, and design teams reference this PRD throughout the development lifecycle."]

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| **Requirements** | **This PRD** | **Product** | **[Status]** |
| Design | TDD | Engineering | [Status] |
| Implementation | Tech Reference | Engineering | [Status] |

### Tiered Usage

| Tier | When to Use | Sections to Skip |
|------|-------------|------------------|
| **Lightweight** | Single-feature PRD, <10 sections | Value Proposition Canvas, Customer Journey Map, API Contract Examples, Appendices, Document History (first version) |
| **Standard** | Multi-feature product, most PRDs | None — complete all sections |
| **Heavyweight** | Platform PRD, 28 sections, cross-team | None — complete all sections, add additional appendices as needed |

---

## Document Information

| Field | Value |
|-------|-------|
| **Product Name** | [Product Name] |
| **Product Type** | [Platform PRD / Feature PRD / Component PRD] |
| **Product Owner** | [Name] |
| **Engineering Lead** | [Name] |
| **Design Lead** | [Name] |
| **Maintained By** | [Team or person responsible for keeping this PRD current] |
| **Stakeholders** | [List all stakeholders] |
| **Status** | [Draft / In Review / Approved / Active] |
| **Target Release** | [Target date/quarter] |
| **Last Verified** | [Date and context — e.g., "2026-03-08 against current product state"] |

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | [Name] | __________ | [Date] |
| Engineering Lead | [Name] | __________ | [Date] |
| Design Lead | [Name] | __________ | [Date] |
| Executive Sponsor | [Name] | __________ | [Date] |

---

## Completeness Status

**Completeness Checklist:**
- [ ] Section 1: Executive Summary — **Status**
- [ ] Sections 2-5: Problem, Background, Vision, Business Context — **Status**
- [ ] Sections 6-9: JTBD, Personas, Value Proposition, Competitive Analysis — **Status**
- [ ] Sections 10-13: Assumptions, Dependencies, Scope, Open Questions — **Status**
- [ ] Sections 14-15: Technical Requirements, Technology Stack — **Status**
- [ ] Sections 16-18: UX, Legal/Compliance, Business Requirements — **Status**
- [ ] Sections 19-20: Success Metrics, Risk Analysis — **Status**
- [ ] Section 21: Implementation Plan (Epics/Stories, Product Reqs, Phasing, DoD, Timeline) — **Status**
- [ ] Sections 22-25: Customer Journey, Error Handling, Design, API Contracts — **Status**
- [ ] Sections 26-28: Contributors, Related Resources, Maintenance & Ownership — **Status**
- [ ] All links verified — **Status**
- [ ] Reviewed by [team] — **Status**

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | [Docs/systems this PRD depends on] |
| **Upstream** | Feeds from: [market research, customer interviews, business strategy] |
| **Downstream** | Feeds to: [TDD, Tech Reference, implementation tickets] |
| **Change Impact** | Notify: [engineering, design, QA, stakeholders] |
| **Review Cadence** | [Quarterly / Monthly / As-needed] |
| **Living Document** | This PRD evolves as the product learns and iterates — see Document History for change log |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Background & Strategic Fit](#3-background--strategic-fit)
4. [Product Vision](#4-product-vision)
5. [Business Context](#5-business-context)
6. [Jobs To Be Done (JTBD)](#6-jobs-to-be-done-jtbd)
7. [User Personas](#7-user-personas)
8. [Value Proposition Canvas](#8-value-proposition-canvas)
9. [Competitive Analysis](#9-competitive-analysis)
10. [Assumptions & Constraints](#10-assumptions--constraints)
11. [Dependencies](#11-dependencies)
12. [Scope Definition](#12-scope-definition)
13. [Open Questions](#13-open-questions)
14. [Technical Requirements](#14-technical-requirements)
15. [Technology Stack](#15-technology-stack)
16. [User Experience Requirements](#16-user-experience-requirements)
17. [Legal & Compliance Requirements](#17-legal--compliance-requirements)
18. [Business Requirements](#18-business-requirements)
19. [Success Metrics & Measurement](#19-success-metrics--measurement)
20. [Risk Analysis](#20-risk-analysis)
21. [Implementation Plan](#21-implementation-plan)
22. [Customer Journey Map](#22-customer-journey-map)
23. [Error Handling & Edge Cases](#23-error-handling--edge-cases)
24. [User Interaction & Design](#24-user-interaction--design)
25. [API Contract Examples](#25-api-contract-examples)
26. [Contributors & Collaboration](#26-contributors--collaboration)
27. [Related Resources](#27-related-resources)
28. [Maintenance & Ownership](#28-maintenance--ownership)

---

## 1. Executive Summary

[2-3 paragraph summary of the product, its purpose, and key value proposition]

**Key Success Metrics:**
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
- [Metric 3]: [Target value]
- [Metric 4]: [Target value]

---

## 2. Problem Statement

<!-- SCOPE NOTE: For feature/component PRDs, do NOT include a "Market Opportunity" subsection with
     TAM/SAM/SOM data. Instead, include a "Why This Feature is Required" subsection explaining
     how this feature is critical to the platform. Reference the Platform PRD for market context. -->

### 2.1 The Core Problem

**[One sentence stating the core problem]**

[Detailed explanation of the problem, including:]
- What is the current state?
- Who is affected?
- What is the impact/cost of not solving this?
- What barriers exist today?

### 2.2 Why Existing Solutions Fall Short

**[Solution Category 1]** (e.g., Existing tools, competitors):
- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

**[Solution Category 2]**:
- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

**[Solution Category 3]**:
- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

### 2.3 The Market Opportunity

[Explain the market unlock - what becomes possible by solving this problem]

---

## 3. Background & Strategic Fit

<!-- SCOPE NOTE: For product PRDs, include platform-level trends, company objectives, and competitive moat.
     For feature/component PRDs, focus on why THIS FEATURE is needed now (what enablers exist,
     what dependencies are ready) and what bets it makes. Reference the Platform PRD for
     platform-level strategic context. Do not repeat market trends or company revenue projections. -->

### 3.1 Why Now?

1. **[Trend/Enabler 1]**: [Explanation]
2. **[Trend/Enabler 2]**: [Explanation]
3. **[Trend/Enabler 3]**: [Explanation]
4. **[Trend/Enabler 4]**: [Explanation]

### 3.2 How This Fits Company Objectives

- **Mission Alignment**: [How this supports company mission]
- **Revenue Goal**: [Revenue target and timeline]
- **Market Position**: [Target market position]
- **Competitive Moat**: [Sustainable competitive advantage]

### 3.3 Strategic Bets

1. **[Bet 1]**: [Hypothesis being tested]
2. **[Bet 2]**: [Hypothesis being tested]
3. **[Bet 3]**: [Hypothesis being tested]
4. **[Bet 4]**: [Hypothesis being tested]

---

## 4. Product Vision

**"[One sentence product vision statement]"**

[1-2 paragraph expansion of the vision, describing the future state when the product succeeds]

---

## 5. Business Context

<!-- SCOPE NOTE: For product PRDs, include full TAM/SAM/SOM, revenue projections, and business KPIs.
     For feature/component PRDs, skip market sizing, revenue projections, and KPI tables (those belong
     in the Platform PRD). Instead, include: (1) why this feature matters to the business (justification,
     cost drivers, strategic value), and (2) a forward reference to Section 19 (Success Metrics &
     Measurement) for all KPIs. Do NOT duplicate KPIs here — Section 19 is the single source of truth
     for metrics. -->

### 5.1 Market Opportunity

| Market | Size | Notes |
|--------|------|-------|
| **Total Addressable Market (TAM)** | $[X]B | [Description] |
| **Serviceable Addressable Market (SAM)** | $[X]B | [Description] |
| **Serviceable Obtainable Market (SOM)** | $[X]B | [Description] |

### 5.2 Business Objectives

1. **Revenue Growth**: [Target]
2. **Market Position**: [Target]
3. **Customer Acquisition**:
   - Year 1: [Target]
   - Year 2: [Target]
   - Year 3: [Target]
4. **Retention**: [Target]

**Revenue Milestones:**
- Year 1: $[X] ARR
- Year 2: $[X] ARR
- Year 3: $[X] ARR

### 5.3 Key Performance Indicators (KPIs)

| Category | KPI | Target | Measurement Method |
|----------|-----|--------|-------------------|
| **Business** | Monthly Recurring Revenue (MRR) | $[X] | [How measured] |
| **Business** | Customer Acquisition Cost (CAC) | $[X] | [How measured] |
| **Business** | Lifetime Value (LTV) | $[X] | [How measured] |
| **Product** | Daily Active Users (DAU) | [X] | [How measured] |
| **Product** | Time to First Value | [X] | [How measured] |
| **Product** | Feature Adoption Rate | [X]% | [How measured] |
| **Technical** | API Response Time | <[X]ms | [How measured] |
| **Technical** | System Uptime | [X]% | [How measured] |
| **Technical** | Error Rate | <[X]% | [How measured] |

---

## 6. Jobs To Be Done (JTBD)

> **Framework:** Jobs To Be Done focuses on the underlying motivation and desired outcome, not the solution. Format: "When [situation], I want to [motivation], so I can [expected outcome]."

### 6.1 Primary Jobs

**Job 1: [Job Name]**
- **When**: [Situation/trigger]
- **I want to**: [Motivation/action]
- **So I can**: [Expected outcome/benefit]
- **Current alternatives**: [How users solve this today]
- **Pain with alternatives**: [Why current solutions are inadequate]

**Job 2: [Job Name]**
- **When**: [Situation/trigger]
- **I want to**: [Motivation/action]
- **So I can**: [Expected outcome/benefit]
- **Current alternatives**: [How users solve this today]
- **Pain with alternatives**: [Why current solutions are inadequate]

**Job 3: [Job Name]**
- **When**: [Situation/trigger]
- **I want to**: [Motivation/action]
- **So I can**: [Expected outcome/benefit]
- **Current alternatives**: [How users solve this today]
- **Pain with alternatives**: [Why current solutions are inadequate]

### 6.2 Related Jobs

| Job | Frequency | Importance | Satisfaction with Current Solutions |
|-----|-----------|------------|-------------------------------------|
| [Job 1] | [Daily/Weekly/Monthly] | [Critical/High/Medium/Low] | [1-10 score] |
| [Job 2] | [Daily/Weekly/Monthly] | [Critical/High/Medium/Low] | [1-10 score] |
| [Job 3] | [Daily/Weekly/Monthly] | [Critical/High/Medium/Low] | [1-10 score] |

---

## 7. User Personas

### 7.1 Primary Persona: [Name] - [Role]

| Attribute | Details |
|-----------|---------|
| **Demographics** | [Age, background, experience level] |
| **Goals** | [What they want to achieve] |
| **Pain Points** | [Current frustrations and challenges] |
| **Technical Proficiency** | [Low / Medium / High] |
| **Budget Authority** | [Yes / No / Influences] |
| **Success Metrics** | [How they measure success] |

**Quote:** "[Representative quote capturing their perspective]"

**A Day in Their Life:**
[2-3 sentences describing typical workflow and where product fits]

### 7.2 Secondary Persona: [Name] - [Role]

| Attribute | Details |
|-----------|---------|
| **Demographics** | [Age, background, experience level] |
| **Goals** | [What they want to achieve] |
| **Pain Points** | [Current frustrations and challenges] |
| **Technical Proficiency** | [Low / Medium / High] |
| **Budget Authority** | [Yes / No / Influences] |
| **Success Metrics** | [How they measure success] |

**Quote:** "[Representative quote capturing their perspective]"

### 7.3 Tertiary Persona: [Name] - [Role]

| Attribute | Details |
|-----------|---------|
| **Demographics** | [Age, background, experience level] |
| **Goals** | [What they want to achieve] |
| **Pain Points** | [Current frustrations and challenges] |
| **Technical Proficiency** | [Low / Medium / High] |
| **Budget Authority** | [Yes / No / Influences] |
| **Success Metrics** | [How they measure success] |

**Quote:** "[Representative quote capturing their perspective]"

### 7.4 Anti-Personas (Who This Is NOT For)

| Anti-Persona | Why Not Target |
|--------------|----------------|
| [Type 1] | [Reason this user is not a fit] |
| [Type 2] | [Reason this user is not a fit] |

---

## 8. Value Proposition Canvas

<!-- SCOPE NOTE: For product PRDs, include full customer profiles with pains/gains and value map.
     For feature/component PRDs, this section is typically N/A — the feature's value contribution
     is captured in the Problem Statement (S2) and Product Vision (S4). Reference the Platform PRD
     for platform-level value proposition. -->

> **Framework:** Maps customer pains and gains to product pain relievers and gain creators.

### 8.1 Customer Profile: [Primary Persona]

**Customer Jobs:**
1. [Functional job 1]
2. [Functional job 2]
3. [Social job]
4. [Emotional job]

**Pains:**
| Pain | Severity (1-10) | Frequency |
|------|-----------------|-----------|
| [Pain 1] | [X] | [How often experienced] |
| [Pain 2] | [X] | [How often experienced] |
| [Pain 3] | [X] | [How often experienced] |
| [Pain 4] | [X] | [How often experienced] |

**Gains:**
| Gain | Importance (1-10) | Current Satisfaction |
|------|-------------------|---------------------|
| [Gain 1] | [X] | [1-10 score] |
| [Gain 2] | [X] | [1-10 score] |
| [Gain 3] | [X] | [1-10 score] |
| [Gain 4] | [X] | [1-10 score] |

### 8.2 Value Map

**Pain Relievers:**
| Pain | How We Relieve It | Measurement |
|------|-------------------|-------------|
| [Pain 1] | [Product feature/capability] | [How we measure relief] |
| [Pain 2] | [Product feature/capability] | [How we measure relief] |
| [Pain 3] | [Product feature/capability] | [How we measure relief] |

**Gain Creators:**
| Gain | How We Create It | Measurement |
|------|------------------|-------------|
| [Gain 1] | [Product feature/capability] | [How we measure creation] |
| [Gain 2] | [Product feature/capability] | [How we measure creation] |
| [Gain 3] | [Product feature/capability] | [How we measure creation] |

### 8.3 Fit Assessment

| Fit Type | Score (1-10) | Evidence |
|----------|--------------|----------|
| **Problem-Solution Fit** | [X] | [Evidence from research] |
| **Product-Market Fit** | [X] | [Evidence from research] |

---

## 9. Competitive Analysis

<!-- SCOPE NOTE: For product PRDs, include full competitive landscape, feature comparison matrix, and positioning.
     For feature/component PRDs, this is typically N/A unless the feature competes directly with a standalone
     product category. Most features reference the Platform PRD for competitive context. -->

### 9.1 Competitive Landscape

| Competitor | Type | Target Market | Key Strengths | Key Weaknesses |
|------------|------|---------------|---------------|----------------|
| [Competitor 1] | [Direct/Indirect/Substitute] | [Target] | [Strengths] | [Weaknesses] |
| [Competitor 2] | [Direct/Indirect/Substitute] | [Target] | [Strengths] | [Weaknesses] |
| [Competitor 3] | [Direct/Indirect/Substitute] | [Target] | [Strengths] | [Weaknesses] |
| [Competitor 4] | [Direct/Indirect/Substitute] | [Target] | [Strengths] | [Weaknesses] |

### 9.2 Feature Comparison Matrix

| Feature | Our Product | Competitor 1 | Competitor 2 | Competitor 3 |
|---------|-------------|--------------|--------------|--------------|
| [Feature 1] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] |
| [Feature 2] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] |
| [Feature 3] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] |
| [Feature 4] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] |
| [Feature 5] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] |

**Legend:** ✅ Full support | ⚠️ Partial/Limited | ❌ Not supported

### 9.3 Competitive Positioning

**Our Unique Differentiation:**
1. [Differentiator 1]: [Why this matters]
2. [Differentiator 2]: [Why this matters]
3. [Differentiator 3]: [Why this matters]

**Positioning Statement:**
"For [target customer] who [statement of need], [product name] is a [product category] that [key benefit]. Unlike [competitive alternative], our product [key differentiator]."

### 9.4 Competitive Response Plan

| If Competitor Does... | Our Response |
|-----------------------|--------------|
| [Competitive action 1] | [Our planned response] |
| [Competitive action 2] | [Our planned response] |
| [Competitive action 3] | [Our planned response] |

---

## 10. Assumptions & Constraints

### 10.1 Technical Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| TA-1 | [Technical assumption] | [Impact] | [How we'll validate] |
| TA-2 | [Technical assumption] | [Impact] | [How we'll validate] |
| TA-3 | [Technical assumption] | [Impact] | [How we'll validate] |

### 10.2 Business Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| BA-1 | [Business assumption] | [Impact] | [How we'll validate] |
| BA-2 | [Business assumption] | [Impact] | [How we'll validate] |
| BA-3 | [Business assumption] | [Impact] | [How we'll validate] |

### 10.3 User Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| UA-1 | [User assumption] | [Impact] | [How we'll validate] |
| UA-2 | [User assumption] | [Impact] | [How we'll validate] |
| UA-3 | [User assumption] | [Impact] | [How we'll validate] |

### 10.4 Constraints

| Type | Constraint | Impact on Product | Mitigation |
|------|------------|-------------------|------------|
| **Technology** | [Constraint] | [Impact] | [Mitigation] |
| **Budget** | [Constraint] | [Impact] | [Mitigation] |
| **Timeline** | [Constraint] | [Impact] | [Mitigation] |
| **Regulatory** | [Constraint] | [Impact] | [Mitigation] |
| **Resource** | [Constraint] | [Impact] | [Mitigation] |

---

## 11. Dependencies

### 11.1 External Dependencies

| Dependency | Type | Owner | Risk Level | Contingency |
|------------|------|-------|------------|-------------|
| [External API/Service] | API | [Provider] | [High/Medium/Low] | [Backup plan] |
| [Cloud Provider] | Infrastructure | [Provider] | [High/Medium/Low] | [Backup plan] |
| [Third-party Tool] | Tool | [Provider] | [High/Medium/Low] | [Backup plan] |

### 11.2 Internal Dependencies

| Dependency | Type | Owner | Status | Target Date |
|------------|------|-------|--------|-------------|
| [Internal system] | System | [Team] | [Status] | [Date] |
| [Internal service] | Service | [Team] | [Status] | [Date] |
| [Internal component] | Component | [Team] | [Status] | [Date] |

### 11.3 Cross-Team Dependencies

| Team | Dependency | What We Need | When Needed | Status |
|------|------------|--------------|-------------|--------|
| [Team 1] | [What they provide] | [Specific deliverable] | [Date] | [Status] |
| [Team 2] | [What they provide] | [Specific deliverable] | [Date] | [Status] |
| [Team 3] | [What they provide] | [Specific deliverable] | [Date] | [Status] |

---

## 12. Scope Definition

### 12.1 In Scope (Phase 1 / MVP)

| Category | Included | Notes |
|----------|----------|-------|
| [Category 1] | [Feature/capability list] | [Details] |
| [Category 2] | [Feature/capability list] | [Details] |
| [Category 3] | [Feature/capability list] | [Details] |

### 12.2 Out of Scope (Phase 1 / MVP)

| Item | Reason | Target Phase |
|------|--------|--------------|
| ❌ [Feature 1] | [Why excluded] | Phase [X] |
| ❌ [Feature 2] | [Why excluded] | Phase [X] |
| ❌ [Feature 3] | [Why excluded] | Phase [X] |
| ❌ [Feature 4] | [Why excluded] | Phase [X] |

### 12.3 Permanently Out of Scope

| Item | Reason |
|------|--------|
| ❌ [Feature 1] | [Why this will never be built] |
| ❌ [Feature 2] | [Why this will never be built] |

---

## 13. Open Questions

| # | Question | Owner | Target Date | Status | Resolution |
|---|----------|-------|-------------|--------|------------|
| 1 | [Question] | [Owner] | [Date] | 🔴 Urgent / 🟡 Researching / 🟢 Resolved | [Answer if resolved] |
| 2 | [Question] | [Owner] | [Date] | 🔴 Urgent / 🟡 Researching / 🟢 Resolved | [Answer if resolved] |
| 3 | [Question] | [Owner] | [Date] | 🔴 Urgent / 🟡 Researching / 🟢 Resolved | [Answer if resolved] |

---

## 14. Technical Requirements

### 14.1 Architecture Requirements

| Requirement | Description | Rationale |
|-------------|-------------|-----------|
| [Architecture pattern] | [Description] | [Why this approach] |
| [Architecture pattern] | [Description] | [Why this approach] |

### 14.2 Performance Requirements

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| API Response Time | < [X]ms (p95) | [Tool/method] |
| Page Load Time | < [X]s | [Tool/method] |
| System Uptime | [X]% | [Tool/method] |
| Concurrent Users | [X]+ | [Tool/method] |
| Throughput | [X] req/sec | [Tool/method] |

### 14.3 Security Requirements

| Requirement | Implementation | Compliance |
|-------------|----------------|------------|
| Authentication | [Method] | [Standard] |
| Authorization | [Method] | [Standard] |
| Data Encryption | [Method] | [Standard] |
| Audit Logging | [Method] | [Standard] |

### 14.4 Scalability Requirements

| Dimension | Current Target | Future Target | Approach |
|-----------|----------------|---------------|----------|
| Users | [X] | [X] | [How we'll scale] |
| Data | [X] | [X] | [How we'll scale] |
| Transactions | [X] | [X] | [How we'll scale] |

### 14.5 Data & Analytics Requirements

| Data Type | What to Collect | Why | Storage/Retention |
|-----------|-----------------|-----|-------------------|
| [User behavior] | [Specific events] | [Purpose] | [Duration] |
| [Performance metrics] | [Specific metrics] | [Purpose] | [Duration] |
| [Business metrics] | [Specific metrics] | [Purpose] | [Duration] |

**Analytics Tools:**
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

---

## 15. Technology Stack

### 15.1 Backend

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Language | [Language] | [X.X] | [Notes] |
| Framework | [Framework] | [X.X] | [Notes] |
| Database | [Database] | [X.X] | [Notes] |
| Cache | [Cache] | [X.X] | [Notes] |
| Queue | [Queue] | [X.X] | [Notes] |

### 15.2 Frontend

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Framework | [Framework] | [X.X] | [Notes] |
| Language | [Language] | [X.X] | [Notes] |
| State Management | [Library] | [X.X] | [Notes] |
| Styling | [Approach] | [X.X] | [Notes] |

### 15.3 Infrastructure

| Component | Technology | Notes |
|-----------|------------|-------|
| Containerization | [Technology] | [Notes] |
| Orchestration | [Technology] | [Notes] |
| CI/CD | [Technology] | [Notes] |
| Monitoring | [Technology] | [Notes] |
| Logging | [Technology] | [Notes] |

---

## 16. User Experience Requirements

<!-- SCOPE NOTE: For product PRDs, include all subsections (onboarding metrics, user flows,
     accessibility, localization).
     For feature/component PRDs, include only feature-specific user flows (16.2). Onboarding
     experience (16.1), accessibility (16.3), and localization (16.4) are platform-level concerns —
     reference the Platform PRD for those. -->

### 16.1 Onboarding Experience

| Metric | Target |
|--------|--------|
| Time to complete onboarding | < [X] minutes |
| Time to first value | < [X] minutes |
| Onboarding completion rate | > [X]% |
| User activation rate | > [X]% |

### 16.2 Core User Flows

| Flow | Steps | Success Criteria |
|------|-------|------------------|
| [Flow 1] | [Step sequence] | [What success looks like] |
| [Flow 2] | [Step sequence] | [What success looks like] |
| [Flow 3] | [Step sequence] | [What success looks like] |

### 16.3 Accessibility Requirements

| Requirement | Standard | Implementation |
|-------------|----------|----------------|
| WCAG Compliance | [Level] | [How achieved] |
| Keyboard Navigation | Full support | [How achieved] |
| Screen Reader Support | Full support | [How achieved] |
| Color Contrast | [Ratio] | [How achieved] |

### 16.4 Localization Requirements

| Language | Priority | Target Date | Status |
|----------|----------|-------------|--------|
| [Language 1] | P0 | [Date] | [Status] |
| [Language 2] | P1 | [Date] | [Status] |
| [Language 3] | P2 | [Date] | [Status] |

---

## 17. Legal & Compliance Requirements

<!-- SCOPE NOTE: For product PRDs, include full regulatory compliance tables, data privacy policies,
     terms & policies checklists, and penalty exposure.
     For feature/component PRDs, include only feature-specific data handling requirements (what data
     this feature stores, retention, deletion cascades). Reference the Platform PRD for SOC 2, GDPR,
     CCPA, EU AI Act, and other platform-level compliance obligations. -->

### 17.1 Regulatory Compliance

| Regulation | Requirement | Implementation | Status |
|------------|-------------|----------------|--------|
| GDPR | [Specific requirements] | [How implemented] | [Status] |
| CCPA | [Specific requirements] | [How implemented] | [Status] |
| SOC 2 | [Specific requirements] | [How implemented] | [Status] |
| [Other] | [Specific requirements] | [How implemented] | [Status] |

### 17.2 Data Privacy

| Data Type | Collection Purpose | Retention | User Rights |
|-----------|-------------------|-----------|-------------|
| [Data type 1] | [Purpose] | [Duration] | [Rights granted] |
| [Data type 2] | [Purpose] | [Duration] | [Rights granted] |

### 17.3 Terms & Policies Required

- [ ] Terms of Service
- [ ] Privacy Policy
- [ ] Cookie Policy
- [ ] Acceptable Use Policy
- [ ] Data Processing Agreement (DPA)
- [ ] [Other policies]

---

## 18. Business Requirements

<!-- SCOPE NOTE: For product PRDs, include monetization strategy, pricing tiers, GTM, and support requirements.
     For feature/component PRDs, this is typically N/A — the feature is part of the platform and does not
     have independent pricing or GTM. Include only a brief note on feature-specific cost drivers
     (e.g., LLM token consumption, storage costs) that affect platform-level usage billing.
     Reference the Platform PRD for pricing, GTM, and support. -->

### 18.1 Monetization Strategy

**Pricing Model:** [Freemium / Subscription / Usage-based / One-time / Hybrid]

**Pricing Tiers:**

| Tier | Price | Included | Target Segment |
|------|-------|----------|----------------|
| [Tier 1] | $[X]/mo | [What's included] | [Target users] |
| [Tier 2] | $[X]/mo | [What's included] | [Target users] |
| [Tier 3] | $[X]/mo | [What's included] | [Target users] |
| [Enterprise] | Custom | [What's included] | [Target users] |

**Usage-Based Costs (if applicable):**

| Resource | Price | Notes |
|----------|-------|-------|
| [Resource 1] | $[X] per [unit] | [Notes] |
| [Resource 2] | $[X] per [unit] | [Notes] |

### 18.2 Go-to-Market Strategy

| Phase | Focus | Timeline | Key Activities |
|-------|-------|----------|----------------|
| Phase 1 | [Focus] | [Timeline] | [Activities] |
| Phase 2 | [Focus] | [Timeline] | [Activities] |
| Phase 3 | [Focus] | [Timeline] | [Activities] |

### 18.3 Support Requirements

| Tier | Channel | Response Time | Availability |
|------|---------|---------------|--------------|
| [Tier 1] | [Channel] | [SLA] | [Hours] |
| [Tier 2] | [Channel] | [SLA] | [Hours] |
| [Enterprise] | [Channel] | [SLA] | [Hours] |

---

## 19. Success Metrics & Measurement

### 19.1 Product Metrics

| Metric | Definition | Target | Measurement Frequency |
|--------|------------|--------|----------------------|
| [Metric 1] | [How calculated] | [Target] | [Daily/Weekly/Monthly] |
| [Metric 2] | [How calculated] | [Target] | [Daily/Weekly/Monthly] |
| [Metric 3] | [How calculated] | [Target] | [Daily/Weekly/Monthly] |

### 19.2 Business Metrics

| Metric | Definition | Target | Measurement Frequency |
|--------|------------|--------|----------------------|
| [Metric 1] | [How calculated] | [Target] | [Daily/Weekly/Monthly] |
| [Metric 2] | [How calculated] | [Target] | [Daily/Weekly/Monthly] |
| [Metric 3] | [How calculated] | [Target] | [Daily/Weekly/Monthly] |

### 19.3 Technical Metrics

| Metric | Definition | Target | Alerting Threshold |
|--------|------------|--------|-------------------|
| [Metric 1] | [How calculated] | [Target] | [When to alert] |
| [Metric 2] | [How calculated] | [Target] | [When to alert] |
| [Metric 3] | [How calculated] | [Target] | [When to alert] |

---

## 20. Risk Analysis

### 20.1 Technical Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |
| [Risk 3] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |

### 20.2 Business Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |
| [Risk 3] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |

### 20.3 Operational Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |
| [Risk 3] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] |

---

## 21. Implementation Plan

> This section consolidates the full delivery plan: what to build (epics, stories, requirements), how to phase it, what "done" means per phase, and when it lands. Read top to bottom for the complete implementation picture.

### 21.1 Epics, Features & Stories

> **Format:** Each epic contains user stories in the format: "As a [persona], I want [goal] so that [benefit]"

#### 21.1.1 Epic Summary

| Epic # | Epic Name | Features | Stories | Priority | Phase |
|--------|-----------|----------|---------|----------|-------|
| 1 | [Epic Name] | [X] | [X] | P0/P1/P2 | [Phase] |
| 2 | [Epic Name] | [X] | [X] | P0/P1/P2 | [Phase] |
| 3 | [Epic Name] | [X] | [X] | P0/P1/P2 | [Phase] |

---

#### Epic 1: [Epic Name]

**Description:** [Brief description of epic scope and purpose]

**US-1.1: [Story Title]**
- **As a** [persona]
- **I want** [goal/desire]
- **So that** [benefit/value]

**Acceptance Criteria:**
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

**Success Metrics:**
- [Metric 1]: [Target]
- [Metric 2]: [Target]

---

**US-1.2: [Story Title]**
- **As a** [persona]
- **I want** [goal/desire]
- **So that** [benefit/value]

**Acceptance Criteria:**
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

**Success Metrics:**
- [Metric 1]: [Target]
- [Metric 2]: [Target]

---

#### Epic 2: [Epic Name]

[Repeat structure for each epic]

---

### 21.2 Product Requirements

#### 21.2.1 Core Features

##### Feature 1: [Feature Name]

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) / P1 (Should Have) / P2 (Could Have) |
| **Description** | [What the feature does] |
| **User Value** | [Why users care] |
| **Dependencies** | [What this depends on] |

**Acceptance Criteria:**
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

**Success Metrics:**
- [Metric]: [Target]

---

##### Feature 2: [Feature Name]

[Repeat structure for each feature]

---

#### 21.2.2 Feature Prioritization Matrix

> **Framework:** Use RICE (Reach, Impact, Confidence, Effort) or MoSCoW (Must/Should/Could/Won't)

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| [Feature 1] | [X] | [1-3] | [%] | [person-weeks] | [Score] | P0/P1/P2 |
| [Feature 2] | [X] | [1-3] | [%] | [person-weeks] | [Score] | P0/P1/P2 |
| [Feature 3] | [X] | [1-3] | [%] | [person-weeks] | [Score] | P0/P1/P2 |

**RICE Formula:** (Reach × Impact × Confidence) / Effort

---

### 21.3 Implementation Phasing

| Phase | Features | Rationale |
|-------|----------|-----------|
| Phase 1 | [Feature list] | [Why this phase] |
| Phase 2 | [Feature list] | [Why this phase] |
| Phase 3 | [Feature list] | [Why this phase] |

---

### 21.4 Release Criteria & Definition of Done

#### 21.4.1 Phase/Release Criteria

**Phase 1 Release Criteria:**

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | [Criterion] | [How validated] | ⬜ |
| **Performance** | [Criterion] | [How validated] | ⬜ |
| **Security** | [Criterion] | [How validated] | ⬜ |
| **Quality** | [Criterion] | [How validated] | ⬜ |
| **Documentation** | [Criterion] | [How validated] | ⬜ |
| **Operations** | [Criterion] | [How validated] | ⬜ |

#### 21.4.2 Definition of Done (Feature Level)

A feature is considered "Done" when:
- [ ] All acceptance criteria met
- [ ] Unit tests written and passing (coverage > [X]%)
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Accessibility requirements met
- [ ] Product owner acceptance

#### 21.4.3 Rollback & Contingency Plans

| Scenario | Detection Method | Rollback Procedure | Decision Maker |
|----------|------------------|-------------------|----------------|
| [Scenario 1] | [How detected] | [Steps to rollback] | [Who decides] |
| [Scenario 2] | [How detected] | [Steps to rollback] | [Who decides] |
| [Scenario 3] | [How detected] | [Steps to rollback] | [Who decides] |

---

### 21.5 Timeline & Milestones

#### 21.5.1 High-Level Timeline

```
[Phase 1: Name] ─────────────────── [Start Date] - [End Date]
    ├── Milestone 1.1: [Name]      [Date]
    ├── Milestone 1.2: [Name]      [Date]
    └── Milestone 1.3: [Name]      [Date]

[Phase 2: Name] ─────────────────── [Start Date] - [End Date]
    ├── Milestone 2.1: [Name]      [Date]
    ├── Milestone 2.2: [Name]      [Date]
    └── Milestone 2.3: [Name]      [Date]

[Phase 3: Name] ─────────────────── [Start Date] - [End Date]
    ├── Milestone 3.1: [Name]      [Date]
    └── Milestone 3.2: [Name]      [Date]
```

#### 21.5.2 Detailed Phase Breakdown

##### Phase 1: [Phase Name] (Months X-Y)

**Focus:** [What this phase accomplishes]

**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

**Success Criteria:**
- [Criterion 1]
- [Criterion 2]

**Target Completion:** [Date]

---

##### Phase 2: [Phase Name] (Months X-Y)

[Repeat structure]

---

## 22. Customer Journey Map

### 22.1 Journey Stages

| Stage | User Goal | Actions | Touchpoints | Emotions | Pain Points | Opportunities |
|-------|-----------|---------|-------------|----------|-------------|---------------|
| **Awareness** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |
| **Consideration** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |
| **Acquisition** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |
| **Onboarding** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |
| **First Value** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |
| **Engagement** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |
| **Retention** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |
| **Advocacy** | [Goal] | [Actions] | [Touchpoints] | [Emotions] | [Pains] | [Opportunities] |

### 22.2 Moments of Truth

| Moment | Description | Success Criteria | Failure Recovery |
|--------|-------------|------------------|------------------|
| [Moment 1] | [What happens] | [What success looks like] | [How to recover if failed] |
| [Moment 2] | [What happens] | [What success looks like] | [How to recover if failed] |
| [Moment 3] | [What happens] | [What success looks like] | [How to recover if failed] |

---

## 23. Error Handling & Edge Cases

### 23.1 Error Categories

| Category | Examples | User Experience | Recovery |
|----------|----------|-----------------|----------|
| **Validation Errors** | [Examples] | [How shown to user] | [How user recovers] |
| **System Errors** | [Examples] | [How shown to user] | [How user recovers] |
| **Integration Errors** | [Examples] | [How shown to user] | [How user recovers] |
| **Timeout Errors** | [Examples] | [How shown to user] | [How user recovers] |

### 23.2 Edge Cases

| Scenario | Expected Behavior | Test Case |
|----------|-------------------|-----------|
| [Edge case 1] | [How system should behave] | [How to test] |
| [Edge case 2] | [How system should behave] | [How to test] |
| [Edge case 3] | [How system should behave] | [How to test] |

### 23.3 Graceful Degradation

| Component Failure | Degraded Experience | User Communication |
|-------------------|--------------------|--------------------|
| [Component 1] | [What still works] | [How user is informed] |
| [Component 2] | [What still works] | [How user is informed] |
| [Component 3] | [What still works] | [How user is informed] |

---

## 24. User Interaction & Design

### 24.1 Wireframes & Mockups

| Screen/Flow | Link | Status | Notes |
|-------------|------|--------|-------|
| [Screen 1] | [Link to design] | [Draft/Review/Final] | [Notes] |
| [Screen 2] | [Link to design] | [Draft/Review/Final] | [Notes] |
| [Screen 3] | [Link to design] | [Draft/Review/Final] | [Notes] |

### 24.2 Design System

- [ ] Component library documented
- [ ] Design tokens defined (colors, spacing, typography)
- [ ] Icon set selected
- [ ] Responsive breakpoints defined
- [ ] Animation/motion guidelines

### 24.3 Prototype Links

| Prototype | Purpose | Link |
|-----------|---------|------|
| [Prototype 1] | [What it demonstrates] | [Link] |
| [Prototype 2] | [What it demonstrates] | [Link] |

---

## 25. API Contract Examples

### 25.1 Key API Endpoints

#### [Endpoint 1]: [Purpose]

**Request:**
```http
[METHOD] /api/v1/[endpoint]
Content-Type: application/json
Authorization: Bearer {token}

{
  "field1": "value1",
  "field2": "value2"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "data": {
    "id": "123",
    "field1": "value1"
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

---

## 26. Contributors & Collaboration

### 26.1 Document Contributors

| Role | Name | Contribution |
|------|------|--------------|
| Product Manager | [Name] | Product vision, user stories, business requirements |
| Engineering Lead | [Name] | Technical architecture, feasibility assessment |
| Design Lead | [Name] | UX flows, wireframes, accessibility requirements |
| QA Lead | [Name] | Acceptance criteria, testing requirements |
| [Other Role] | [Name] | [Contribution] |

### 26.2 How to Contribute

- **Comment inline** for questions, suggestions, or clarifications
- **Tag relevant team members** using @ mentions
- **Update Open Questions table** when decisions are made
- **Link related documents** (user research, technical specs, designs)
- **Review quarterly** and flag outdated sections

---

## 27. Related Resources

### 27.1 Customer Research

| Resource | Link | Description |
|----------|------|-------------|
| Customer Interviews | [Link] | [Description] |
| User Surveys | [Link] | [Description] |
| Competitive Analysis | [Link] | [Description] |
| Market Research | [Link] | [Description] |

### 27.2 Technical Documentation

| Document | Link | Description |
|----------|------|-------------|
| Technical Requirements | [Link] | [Description] |
| System Architecture | [Link] | [Description] |
| API Documentation | [Link] | [Description] |

### 27.3 Design Assets

| Asset | Link | Description |
|-------|------|-------------|
| Design Files | [Link] | [Description] |
| Wireframes | [Link] | [Description] |
| Component Library | [Link] | [Description] |

### 27.4 Business Documents

| Document | Link | Description |
|----------|------|-------------|
| Business Case | [Link] | [Description] |
| Financial Model | [Link] | [Description] |
| GTM Plan | [Link] | [Description] |

---

## 28. Maintenance & Ownership

### 28.1 Document Ownership

| Role | Name | Responsibility |
|------|------|----------------|
| **Primary Owner** | [Name] | Overall document accuracy and updates |
| **Technical Owner** | [Name] | Technical sections accuracy |
| **Backup Owner** | [Name] | Coverage when primary unavailable |

### 28.2 Review Schedule

> **Note:** High-level review cadence is defined in the Contract Table (Completeness Status section). This section captures the detailed scheduling for each review type.

| Review Type | Next Date | Participants |
|-------------|-----------|--------------|
| **Full Review** | [Date] | [Participants] |
| **Technical Review** | [Date] | [Participants] |
| **Ad-Hoc Review** | - | Triggered by major changes |

### 28.3 Update Process

1. **Propose Changes**: Comment on specific sections or create issue
2. **Review with Stakeholders**: Relevant leads review
3. **Update Document**: Incorporate approved changes
4. **Increment Version**: Update version number and history
5. **Notify Team**: Announce changes with summary
6. **Archive Old Version**: Keep previous versions for reference

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| [Term 1] | [Definition] |
| [Term 2] | [Definition] |
| [Term 3] | [Definition] |

### Appendix B: Acronyms

| Acronym | Meaning |
|---------|---------|
| [Acronym 1] | [Meaning] |
| [Acronym 2] | [Meaning] |
| [Acronym 3] | [Meaning] |

### Appendix C: Technical Architecture Diagrams

[Include or link to detailed architecture diagrams]

### Appendix D: User Research Data

[Include or link to user research findings]

### Appendix E: Financial Projections

[Include or link to financial models]

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
| [X.X] | [Date] | [Author] | [Summary of changes] |

---

<!--
================================================================================
TEMPLATE USAGE INSTRUCTIONS (Remove this block when creating a PRD from this template)
================================================================================

## How to Use This Template

1. **Copy this file** and rename following the PRD naming convention (kebab-case):
   - Pattern: `[product-name]-prd.md` (e.g., `gameframe-ai-prd.md`)

2. **Fill in the YAML frontmatter** with actual values:
   - `id`: Use `"[PROJECT-ID]-PRD-CORE"` format
   - `title`: Human-readable product name + "Product Requirements Document (PRD)"
   - `status`: Start with `"🟡 Draft"`, update to `"🟢 Approved"` after sign-off
   - `template_schema_doc`: Set to `"src/superclaude/examples/prd_template.md"`

3. **Adapt the section structure** per Tiered Usage:
   - Lightweight: Skip Value Proposition Canvas, Customer Journey Map, API Contract Examples
   - Standard: Complete all sections
   - Heavyweight: Complete all sections, add additional appendices as needed

4. **Callout conventions** (use throughout the PRD):
   > **Note:** Informational context that is helpful but not critical
   > **Important:** Something the reader must be aware of
   > **CRITICAL:** Something that will cause project failure if ignored
   > **Tip:** Best practice or recommendation

5. **Content rules**:
   - PRD defines WHAT to build and WHY — not HOW (that belongs in the TDD)
   - User stories use "As a [persona], I want [goal] so that [benefit]" format
   - Every feature needs acceptance criteria and success metrics
   - Keep scope boundaries clear — use "Out of Scope" sections aggressively
   - Requirements should be testable and measurable

6. **Remove all template guidance** (HTML comments and placeholder text) from your
   final PRD. Keep only actual content.

================================================================================
-->

<!--
LINE BUDGET — Target line counts per tier:
- Lightweight (single-feature PRD): 400–600 lines
- Standard (multi-feature product): 800–1200 lines
- Heavyweight (platform PRD, 28 sections): 1200–1800 lines

These are guidelines, not hard limits. Prioritize completeness over brevity.
-->

<!--
CONTENT RULES:
- PRD defines WHAT to build and WHY — technical HOW belongs in the TDD
- Every requirement should be testable and have clear acceptance criteria
- User stories follow: "As a [persona], I want [goal] so that [benefit]"
- Competitive analysis should be evidence-based, not aspirational
- Scope sections should clearly delineate MVP vs future phases
- Risk analysis should include both probability and impact assessments
-->

<!--
FILE NAMING CONVENTION:
- Pattern: [product-name]-prd.md (kebab-case)
- Examples: gameframe-ai-prd.md, pixel-streaming-prd.md, wizard-system-prd.md
-->

<!--
CALLOUT CONVENTIONS:
> **Note:** Informational context — helpful but not critical
> **Important:** Something the reader must be aware of to avoid issues
> **CRITICAL:** Something that will cause project failure if ignored
> **Tip:** Best practice, recommendation, or time-saving suggestion
-->

> **See also:**
> - [TDD Template](tdd_template.md) — For component/system-level Technical Design Documents
> - [Technical Reference Template](technical_reference_template.md) — For documenting implemented features and systems
> - [Operational Guide Template](operational_guide_template.md) — For installation, setup, and deployment guides
> - [Supplemental Doc Template](supplemental_doc_template.md) — For process standards and reference documents

---

> **Template Version:** 1.0
> **Template Created:** 2025-11-27
> **Template Updated:** 2026-03-11
> **Template Type:** Product PRD (Strategic/Business-focused)
> **Based On:** GFxAI PRD with additions for comprehensive coverage
