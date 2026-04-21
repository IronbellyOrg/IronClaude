---
id: "GFXAI-PRD-TASK-MGMT"
title: "GameFrame AI Scalable Task Management System - Product Requirements Document (PRD)"
description: "Foundational product requirements, user stories, acceptance criteria, and business context for the database-backed, AI-operated task management layer of the GameFrame AI SaaS platform"
version: "1.0"
status: "🟡 Draft"
type: "📋 Product Requirements"
priority: "🔥 Highest"
created_date: "2026-03-19"
updated_date: "2026-03-19"
assigned_to: "product-team"
autogen: true
autogen_method: "rf-assembler from 9 synthesis files, 7 research files, 2 research reports"
coordinator: "product-manager"
parent_task: ""
depends_on:
- "TASK-RESEARCH-20260317-160411 (Task Management Baseline Report)"
- "TASK-RESEARCH-20260319-103000 (AI-Operator Research Report)"
related_docs:
- ".claude/templates/documents/prd_template.md"
- "docs/docs-product/product/gdlc/gdlc-hub.md"
- "docs/archive/architecture/ARCHITECTURE.md"
tags:
- task-management
- ai-operated
- gdlc
- platform
- prd
template_schema_doc: ".claude/templates/documents/prd_template.md"
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
  next_review_date: "2026-06-19"
task_type: "static"
---

# GameFrame AI Scalable Task Management System - Product Requirements Document (PRD)

> **WHAT:** Foundational product requirements, user stories, acceptance criteria, and business context for the database-backed, AI-operated task management layer of the GameFrame AI SaaS platform.
> **WHY:** Serves as the single source of truth for product scope, priorities, success criteria, and implementation phasing of the task management system -- the structural backbone enabling AI agents to manage game development projects with persistence, auditability, and cross-project memory.
> **HOW TO USE:** Product, engineering, and design teams reference this PRD throughout the development lifecycle. AI agents (rf-task-builder, rf-task-executor) use this document to generate TDD and implementation task files.

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| **Requirements** | **This PRD** | **Product** | **Draft** |
| Design | TDD | Engineering | Not Started |
| Implementation | Tech Reference | Engineering | Not Started |

### Tiered Usage

This is a **Heavyweight** platform PRD (28 sections + appendices). All sections are completed.

---

## Document Information

| Field | Value |
|-------|-------|
| **Product Name** | GameFrame AI Scalable Task Management System |
| **Product Type** | Platform PRD |
| **Product Owner** | TBD |
| **Engineering Lead** | TBD |
| **Design Lead** | TBD |
| **Maintained By** | TBD + AI Agents (Claude Code) |
| **Stakeholders** | Product team, Engineering, AI Agent system, Future frontend team |
| **Status** | Draft |
| **Target Release** | Q2-Q3 2026 (11-15 week implementation) |
| **Last Verified** | 2026-03-19 against current codebase and 2 research reports |

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | TBD | __________ | __________ |
| Engineering Lead | TBD | __________ | __________ |
| Design Lead | TBD | __________ | __________ |
| Executive Sponsor | TBD | __________ | __________ |

---

## Completeness Status

**Completeness Checklist:**
- [x] Section 1: Executive Summary -- Complete
- [x] Sections 2-5: Problem, Background, Vision, Business Context -- Complete
- [x] Sections 6-9: JTBD, Personas, Value Proposition, Competitive Analysis -- Complete
- [x] Sections 10-13: Assumptions, Dependencies, Scope, Open Questions -- Complete
- [x] Sections 14-15: Technical Requirements, Technology Stack -- Complete
- [x] Sections 16-18: UX, Legal/Compliance, Business Requirements -- Complete
- [x] Sections 19-20: Success Metrics, Risk Analysis -- Complete
- [x] Section 21: Implementation Plan (Epics/Stories, Product Reqs, Phasing, DoD, Timeline) -- Complete
- [x] Sections 22-25: Customer Journey, Error Handling, Design, API Contracts -- Complete
- [x] Sections 26-28: Contributors, Related Resources, Maintenance & Ownership -- Complete
- [ ] All links verified -- Pending
- [ ] Reviewed by engineering -- Pending

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | PostgreSQL 15, Pinecone, OpenAI Embedding API, LangChain/LangGraph, pg_partman |
| **Upstream** | Feeds from: AI-Operator Research Report, Task Management Baseline Report, GDLC framework, CLAUDE.md market segments |
| **Downstream** | Feeds to: TDD, Tech Reference, implementation task files, agent tool definitions |
| **Change Impact** | Notify: engineering, AI agent team, frontend (when applicable), stakeholders |
| **Review Cadence** | Quarterly full review; per-phase technical review; monthly risk review during active development |
| **Living Document** | This PRD evolves as the product learns and iterates -- see Document History for change log |

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

**Appendices:**
- [Appendix A: Glossary](#appendix-a-glossary)
- [Appendix B: Acronyms](#appendix-b-acronyms)
- [Appendix C: Technical Architecture Diagrams](#appendix-c-technical-architecture-diagrams)
- [Appendix D: User Research Data](#appendix-d-user-research-data)
- [Appendix E: Financial Projections](#appendix-e-financial-projections)
- [Document History](#document-history)

---

## 1. Executive Summary

The GameFrame AI Scalable Task Management System is a database-backed, AI-operated task management layer for the GameFrame AI SaaS platform. It enables the platform's 8 specialist AI agents to create, query, update, and track game development tasks through structured tool calls rather than ephemeral conversation context. The system replaces the current file-based MDTM (Markdown Task Management) workflow -- which lacks persistence, querying, aggregation, and audit capabilities -- with a relational PostgreSQL core, event-sourced audit trail, and semantic memory pipeline that together provide the structured state management AI agents require to operate reliably at scale.

The architecture uses a hybrid data model: a relational PostgreSQL core with JSONB for extensible metadata, enhanced with an append-only audit event table, organization-level Row-Level Security, compound indexes for AI query patterns, and a Domain Facade API layer. AI agents are the primary operators, performing 95%+ of all task management operations. This inverts the typical project management tool design: instead of optimizing for human drag-and-drop interaction, every API surface -- zoom-level responses, bulk operations, cursor-based pagination, Domain Facade tool consolidation, and actionable error codes -- is engineered for token efficiency and machine consumption. Human users (solo indie developers, studio leads, educators, enterprise producers) consume the same data through dashboard views, roadmap canvases, and audit trail queries.

The system integrates deeply with GameFrame's existing Game Development Lifecycle (GDLC) framework: 7 phases, 9 areas, 66 subcategories, and 457 design decisions serve as the organizational taxonomy. GDLC templates contain ~791 checklist items (608 gate items + ~98 work order items + 291 genre-conditional) that seed project task trees. A single task tree with variable depth (configurable, default 6 levels) replaces fixed Agile terminology, and the database is the single source of truth -- markdown becomes a rendered view, not the canonical store.

**Key Success Metrics:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| API response time (p95) | < 200ms | Prometheus endpoint latency histograms |
| Template instantiation (500 tasks) | < 5 seconds | Bulk operation timing |
| Agent token efficiency | 85%+ reduction vs. naive approach | Zoom-level token savings (industry benchmark: 65-95%) |
| Dashboard query latency | < 50ms | Materialized view response time |
| Concurrent agent safety | Zero silent data loss | Optimistic concurrency conflict rate monitoring |
| Audit trail coverage | 100% of mutations | Event count vs. mutation count comparison |

---

## 2. Problem Statement

### 2.1 The Core Problem

**Game development projects using the GameFrame AI platform have no persistent, queryable, AI-accessible task management system -- forcing 8 specialist AI agents to operate without structured state, audit history, or cross-project memory.**

| Gap | Current State | Impact | Source |
|-----|--------------|--------|--------|
| No database persistence | Tasks exist only as markdown files in `.dev/tasks/`; state lost on session boundary | Agents cannot resume work, query progress, or aggregate across tasks | Capabilities 1.1-1.2 (all "Designed -- not yet built") |
| No AI-optimized API | Zero agent tools target PostgreSQL for task management; all 8 existing tools target UE Manager only | Agents have no structured way to create, query, or update tasks programmatically | Capability 2.1 (no DB-backed agent tools exist) |
| No audit trail | Every mutation commits directly with no history; no before/after diffs | AI agent actions are untraceable; no accountability, no debugging, no compliance | Capability 3.1 (zero audit infrastructure) |
| No semantic memory | Completed task knowledge is not vectorized; each project starts from zero | No cross-project learning; common mistakes repeated; no estimation calibration | Capability 4.1 (Pinecone exists for conversations but not tasks) |
| No multi-tenant isolation | No `Organization` model; existing tables use `owner_id` (user-level) | Cannot support SaaS multi-tenancy; data leakage risk between customers | Capability 5.1 (no organization_id on any table) |
| No real-time sync | Two WebSocket managers exist but neither serves task management; Redis has zero pub/sub usage | Multiple human users cannot see task changes live; agent work is invisible until page refresh | Capability 6.1 (no task event broadcasting) |

The entire task management capability matrix (Backend DB, Service Layer, API Routes, WebSocket, Frontend Integration, Agent Tools) shows `--` for every function. This is a greenfield build.

### 2.2 Why Existing Solutions Fall Short

**General-Purpose PM Tools** (Jira, Linear, Asana, Monday.com):
- Not designed for AI-agent-as-primary-operator (95%+ machine operations)
- No GDLC integration (7 phases, 9 areas, gate checklists)
- No token-efficient response formats (zoom levels, field projection, compact IDs)
- No game development taxonomy (500+ design decisions, genre-conditional items)
- Tool call overhead: generic APIs require multiple round-trips where domain-specific bulk operations need one

**No-Code Game Development Platforms** (GDevelop, Construct 3, Ludo.ai):
- Target 2D/casual development, not professional 3D/UE5.6+
- No multi-agent orchestration (LangGraph Swarm with 8 specialists)
- No structured task management -- focus on asset creation and visual scripting
- No GDLC-aware lifecycle management

**File-Based MDTM (Current State)**:
- Works for single-task execution but cannot aggregate across 500+ tasks
- No filtering, pagination, or compound queries
- No concurrent access control (file locks do not work across agent sessions)
- No audit trail, no dependency resolution, no gate readiness checks
- Cannot compute project-level progress or health metrics

### 2.3 Why This Feature is Required

The task management system is the structural backbone that enables the platform's core value proposition. Without it, AI agents cannot reliably manage multi-phase game development projects — they have no persistent state, no audit trail, no dependency tracking, and no cross-project memory. Every other platform capability (wizard configuration, agent orchestration, pixel streaming, GDLC lifecycle) depends on structured task management to coordinate and persist work.

> **Market context:** See Platform PRD for full market opportunity analysis (TAM/SAM/SOM, competitive positioning, market trends).

---

## 3. Background & Strategic Fit

> **Note:** Platform-level strategic context (market trends, company objectives, competitive moat) is in the Platform PRD. This section covers why this specific feature is needed now and what bets it makes.

### 3.1 Why This Feature Now?

| # | Enabler | Explanation |
|---|---------|-------------|
| 1 | **Agent system is operational but stateless** | 8 specialist agents are operational via LangGraph Swarm, but they have zero persistent task state. Every session starts from scratch. The agents exist — they just need a database to work from. |
| 2 | **GDLC taxonomy is codified but has no execution layer** | 7 phases, 9 areas, 66 subcategories, 457 design decisions exist in `frontend/app/roadmap/types/gdlc.ts`. The organizational structure is defined — but there's no way to instantiate it as a project task tree, track completion, or evaluate gate readiness. |
| 3 | **Token economics are proven** | Industry evidence (LAPIS 85.5% token reduction, MCP patterns 65-95% savings) validates that AI-optimized APIs dramatically reduce operating costs. Building the task API with zoom levels and Domain Facade from the start avoids expensive retrofitting later. |
| 4 | **Roadmap canvas has no persistence** | The 533-node taxonomy tree in the frontend has 6 independent status systems, all in-memory. Nothing survives a page refresh. The task management system provides the backend persistence that makes the roadmap canvas actually useful. |

### 3.2 Feature-Level Bets

| # | Bet | If Wrong |
|---|-----|----------|
| 1 | **AI agents can be the primary task operators (95%+)** | Need a full human PM UI (Kanban boards, drag-and-drop) — 3-6 months additional frontend work. Mitigation: human REST API is included in scope for fallback. |
| 2 | **GDLC templates provide sufficient task structure** | Customers need fully custom task hierarchies. Mitigation: variable-depth tree with configurable `max_depth` supports custom structures alongside templates. |
| 3 | **Database is the right source of truth (over markdown)** | File-based approach has benefits (git integration, human readability) we sacrifice. Mitigation: markdown becomes a rendered view, preserving readability while gaining queryability. |
| 4 | **Cross-project semantic memory drives retention** | Customers treat projects as independent. Mitigation: semantic memory is Phase 4, feature-flagged — can be deprioritized if bet fails without impacting core functionality. |

---

## 4. Product Vision

**"Every game development decision -- from initial concept to live operations -- is structured, persistent, auditable, and searchable, managed by AI agents that operate with the same rigor as a senior producer but at machine speed and scale."**

The GameFrame AI Scalable Task Management System establishes the database-backed execution layer that transforms AI agents from conversational assistants into accountable project operators. Today, the platform's 8 specialist agents can discuss game design and configure Unreal Engine parameters through natural language -- but they have no persistent memory of what was decided, no structured view of what remains to be done, and no audit trail of what they changed. The task management system closes this gap.

In the target state, a solo indie developer describes their game concept and the platform's agents autonomously instantiate a GDLC-structured task tree of ~500 items, work through phases with gate-quality checks, resolve dependencies as predecessors complete, and build cross-project institutional memory from every completed task. A studio lead sees real-time project health across all 9 GDLC areas without asking. An enterprise producer searches past projects semantically -- "How did we handle camera configuration for a third-person RPG?" -- and gets specific, structured answers drawn from vectorized completed tasks. An educator reviews the audit trail to grade student process, not just output.

The system is built for AI agents first and human users second -- not because humans are unimportant, but because the 95%+ of operations performed by machines must be token-efficient, concurrency-safe, and self-correcting. The same data serves both audiences through different lenses: agents through Domain Facade tools with zoom-level responses, humans through dashboard views and roadmap canvases. The database is the single source of truth. Markdown is a rendered view. Every mutation is an auditable event. Every completed task becomes searchable institutional memory.

---

## 5. Business Context

> **Note:** This is a feature/component PRD. Market sizing (TAM/SAM/SOM), platform pricing, and revenue projections are platform-level concerns documented in the Platform PRD.

### 5.1 Why This Feature Matters to the Business

The task management system is **required platform infrastructure** — without it, AI agents cannot persist state, track progress, audit decisions, or learn across projects. It is the structural backbone that enables every revenue-generating interaction on the platform.

**Business justification:**
- **Enables platform stickiness:** Projects with persistent task trees and audit trails create switching costs. Competitors without structured AI memory cannot replicate cross-project learning.
- **Unlocks Enterprise tier:** Enterprise buyers require audit trails, compliance-grade data handling, and multi-tenant isolation — all delivered by this system's core architecture.
- **Reduces support costs:** Persistent task state and audit trails eliminate the #1 category of support tickets ("what happened to my project?" / "what did the AI change?").
- **Drives adoption depth:** Semantic memory across completed tasks means the platform gets smarter with every project, increasing value over time.

**Feature-specific cost drivers:** Task management operations consume LLM tokens (via Domain Facade tool calls), audit event storage (PostgreSQL with tiered retention), and semantic memory storage (Pinecone embeddings). These costs scale with project count and task volume per organization.

**Feature KPIs and full measurement plan:** See Section 19 (Success Metrics & Measurement) for all product, business, and technical metrics with targets, measurement methods, frequencies, and alerting thresholds.

---

## 6. Jobs To Be Done (JTBD)

> **Framework:** Jobs To Be Done focuses on the underlying motivation and desired outcome, not the solution. Format: "When [situation], I want to [motivation], so I can [expected outcome]."

### 6.1 Primary Jobs

**Job 1: Navigate Project Complexity (AI Agent Operator)**
- **When**: I am an AI agent assigned to a GDLC project with 500+ tasks across 7 phases and 9 areas
- **I want to**: progressively drill down from project summary to specific task detail, with each step costing a predictable number of tokens
- **So I can**: find and execute my next action without exceeding my context window or wasting tokens on irrelevant data
- **Current alternatives**: Load all tasks into context (exceeds window); improvise from conversation history (no structured state); parse MDTM markdown files (cannot aggregate at scale)
- **Pain with alternatives**: Context rot degrades accuracy; no filtering or pagination; 500 individual file reads = ~100K-150K tokens in overhead alone

**Job 2: Execute Bulk Task Operations (AI Agent Operator)**
- **When**: I need to initialize a project (~500 tasks), pass a gate (mark 45+ tasks done), or resolve a dependency chain
- **I want to**: perform these operations in a single tool call with partial-success semantics
- **So I can**: minimize tool call overhead (~200-300 tokens/call) and complete routine operations in seconds, not minutes
- **Current alternatives**: Individual task creation/update calls (500 calls = ~100K-150K tokens in mechanics); manual markdown manipulation (no validation, no audit trail)
- **Pain with alternatives**: No task API currently exists targeting PostgreSQL for task management; agents have zero tools for bulk operations

**Job 3: Ship a Game Without Deep Technical Skills (Solo Indie Dev)**
- **When**: I have a game design vision but lack expertise across all 9 GDLC areas
- **I want to**: describe what I want in natural language and have specialized AI agents handle implementation, tracking their own progress
- **So I can**: focus on creative decisions while reducing development time by 10x
- **Current alternatives**: Learn each specialty (months per area); hire freelancers (expensive, coordination overhead); use game templates (limited customization)
- **Pain with alternatives**: Solo dev cannot master 9 specialties; freelancer quality is inconsistent; templates do not produce a truly custom game

**Job 4: Track Project Health at a Glance (Studio Lead, Enterprise Producer)**
- **When**: I am managing one or more game development projects
- **I want to**: see aggregate status across all GDLC phases and areas in a single view -- task counts by status, overdue items, next gate readiness
- **So I can**: identify bottlenecks, allocate resources, and make go/no-go decisions without drilling into individual tasks
- **Current alternatives**: Roadmap canvas frontend (state lost on refresh; no backend aggregation); spreadsheets (disconnected from dev state); MDTM files (manual scan, no aggregate view)
- **Pain with alternatives**: No persistence, no filtering across projects, manual data entry

**Job 5: Maintain Institutional Memory Across Projects (Enterprise Producer)**
- **When**: my studio has completed multiple projects and is starting a new one
- **I want to**: semantically search completed tasks from past projects to find relevant solutions, common blockers, and proven approaches
- **So I can**: ensure new projects benefit from accumulated knowledge and teams do not repeat past mistakes
- **Current alternatives**: Team wikis (prose, not structured; decays quickly); ask team members (knowledge leaves when people leave); no cross-project memory exists
- **Pain with alternatives**: Each project starts from zero; same mistakes repeated across projects

### 6.2 Related Jobs

| Job | Frequency | Importance | Satisfaction with Current Solutions |
|-----|-----------|------------|-------------------------------------|
| Review development process via audit trail (Educator, Enterprise) | Per project | High | 2/10 -- git history shows code changes but not design decisions or task progression |
| Ensure agent accountability with before/after diffs (All humans) | Every session | Critical | 1/10 -- no audit trail exists; every AI mutation is untraceable |
| Manage concurrent multi-agent writes without data loss (AI Agent) | Every session | Critical | 1/10 -- no concurrent access control exists; no conflict resolution |
| Auto-document every design decision for knowledge transfer (Enterprise) | Continuous | High | 3/10 -- manual documentation is expensive and always incomplete |

---

## 7. User Personas

### 7.1 Primary Persona: AI Agent Operator

> This is the unique and most critical persona. The AI Agent Operator is not a human -- it is any of the 8 specialist agents (Project Architect, Movement Specialist, Combat Designer, Inventory Architect, World Builder, Game Designer, Performance Optimizer, Deployment Specialist) operating within the LangGraph Swarm orchestration. 95%+ of all task management operations are performed by this persona.

| Attribute | Details |
|-----------|---------|
| **Demographics** | Software entity running within LangGraph StateGraph. Has `session_id`, `project_id`, `user_id` in AgentState. Operates 24/7. Multiple instances run concurrently on the same project. |
| **Goals** | Execute assigned tasks within token budget constraints. Navigate from project overview to task detail with minimal tool calls. Complete checklist items, update statuses, report progress. Learn from past projects via semantic memory. |
| **Pain Points** | Context window decay (~50% effective utilization per JetBrains 2025 research). Cannot hold 500+ tasks in memory. Token budget per tool call (~2000 tokens max response). Tool call overhead (~200-300 tokens/call). No interactive confirmation -- needs idempotency keys and actionable errors. Concurrent write conflicts from parallel agents. |
| **Technical Proficiency** | Absolute within domain. Consumes structured JSON. Follows state machine rules. Cannot interpret ambiguous UI or prose-heavy responses. Needs enumerated error codes with prescribed actions. |
| **Budget Authority** | None. Operates within human user's subscription tier. Token consumption is a direct cost driver. |
| **Success Metrics** | Tasks completed per session. Token efficiency (tasks per 1K tokens). Error rate (invalid transitions, concurrent conflicts). Percentage of tool calls returning actionable data on first attempt. |

**Quote:** "Give me a 150-token project summary so I can decide which phase needs attention, then let me drill into blocked tasks at 50 tokens each, then give me full detail on the one I need to act on."

**A Day in Their Life:**
An AI agent wakes with a session context containing project_id and assigned_area. It calls the Dashboard endpoint (Level 0, ~150 tokens) to assess project health. It identifies a blocked phase, drills to the List view (Level 1, ~50 tokens/task) to find the specific blocker, resolves a dependency chain via bulk operation, marks tasks complete, and logs every mutation to the audit trail with before/after diffs. This cycle repeats hundreds of times per day across multiple concurrent agent instances.

### 7.2 Secondary Persona: Solo Indie Developer ("Alex")

| Attribute | Details |
|-----------|---------|
| **Demographics** | Solo developer, 20-35 years old, working from home or co-working space. Self-funded or micro-funded. One-person team wearing all hats. |
| **Goals** | Ship a professional-quality game without years of engine programming. Translate game design vision into playable builds quickly. Maintain momentum as a solo operator. |
| **Pain Points** | Limited technical skills across the full stack (art, code, audio, networking). Time pressure -- must ship before savings run out. Overwhelmed by 500+ design decisions across 9 GDLC areas. Cannot afford specialists. |
| **Technical Proficiency** | Intermediate -- understands game design concepts but may lack deep UE, networking, or systems programming expertise. Comfortable with natural language interaction. |
| **Budget Authority** | Full authority but severely constrained. Indie Tier ($99/mo). Every dollar must justify itself in shipped features. |
| **Success Metrics** | Time-to-playable-prototype. GDLC phases completed per month. Reduction in "blocked" tasks due to knowledge gaps. |

**Quote:** "I know exactly what game I want to make -- I just need something that turns my ideas into working builds without requiring me to learn 9 different specialties."

**A Day in Their Life:**
Alex opens GameFrame AI, checks the Dashboard for project health, then describes a new feature in natural language ("add a double-jump with stamina cost"). The AI agents translate this into tasks, implement the configuration, and Alex sees the result via Pixel Streaming within minutes. Alex rarely touches individual task fields -- the agents handle execution while Alex focuses on creative direction.

### 7.3 Tertiary Persona: Small Studio Lead ("Jordan")

| Attribute | Details |
|-----------|---------|
| **Demographics** | Lead developer or technical director at a 2-10 person studio. 28-45 years old. Manages 1-5 developers plus contractors. |
| **Goals** | Multiply team productivity without hiring. Eliminate knowledge silos -- any team member should be able to pick up any area. Track progress across GDLC phases with real-time visibility. |
| **Pain Points** | Developer bottlenecks when specialized team members are unavailable. Onboarding takes weeks. No single view of project health across all areas and phases. Studio Tier ($499/mo) must demonstrably save more than one developer-month per quarter. |
| **Technical Proficiency** | High -- deep expertise in 2-3 areas, working knowledge of most. Comfortable with structured workflows, git, CI/CD. |
| **Budget Authority** | Shared with co-founders or studio head. Must justify ROI. Studio Tier ($499/mo). Can approve annual commitments. |
| **Success Metrics** | Team velocity (tasks per sprint). Gate pass rate (% passed on first attempt). Onboarding time for new members. Reduction in blocked tasks from knowledge silos. |

**Quote:** "I need to see at a glance which GDLC phases are on track, which areas are blocked, and which agent is working on what -- across all 9 areas simultaneously."

### 7.4 Quaternary Persona: Educator ("Dr. Reyes")

| Attribute | Details |
|-----------|---------|
| **Demographics** | University professor or bootcamp instructor, 30-55 years old. Teaches game design, interactive media, or CS. Manages classes of 15-60 students. |
| **Goals** | Focus curriculum on game design principles, not engine programming. Enable portfolio-ready projects within a semester (12-16 weeks). Reduce skill variance across students. Grade development process, not just final output. |
| **Pain Points** | Curriculum complexity (UE alone requires months to learn). Limited timeframes. Skill variance across students (CS majors vs. art students). Cannot provide 1:1 mentoring for every project. Grading requires visibility into decision-making process. |
| **Technical Proficiency** | Variable -- may be seasoned developer or design-focused academic. Comfortable with educational tools and LMS integration. |
| **Budget Authority** | Institutional. Requires department approval. May need educational/multi-seat pricing beyond standard tiers. |
| **Success Metrics** | Student project completion rate. Portfolio quality scores. Student satisfaction/NPS. Reduction in "I'm stuck" support requests. Ability to grade process via audit trail. |

**Quote:** "I want my students to learn the GDLC process by doing it, with AI agents handling the technical implementation so they can focus on design decisions."

> **MVP Scope Note:** The Educator persona is included for product vision completeness but is **explicitly deferred to post-MVP**. No MVP user stories address classroom-specific workflows (multi-seat pricing, LMS integration, grading via audit trail). The `query_audit_trail` tool (needed for process grading) is Phase 3, not available at launch. Educational pricing is undefined (Q27). If user research (Q28) validates demand, educator-specific stories will be added in a future phase.

### 7.5 Quinary Persona: Enterprise Producer ("Morgan")

| Attribute | Details |
|-----------|---------|
| **Demographics** | Producer or technical PM at a mid-to-large studio (50-500+ people). 30-50 years old. Manages multiple concurrent projects. Reports to VP of Production or CTO. |
| **Goals** | Rapid prototype validation -- test game concepts in hours, not months. Automatic documentation of every design decision. Cross-project institutional memory. Reduce prototyping cost by 10x. |
| **Pain Points** | Slow prototyping (3-6 months to validate a concept). Documentation overhead. Knowledge loss when team members leave. Multiple concurrent projects with no unified visibility. Enterprise Tier ($2,499/mo) must save more than one senior developer's time per month. Requires SOC 2, data residency, GDPR compliance for procurement. |
| **Technical Proficiency** | Moderate to high -- understands game dev deeply but may not write code daily. Expert in project management and production pipelines. |
| **Budget Authority** | Significant. Can approve Enterprise Tier ($2,499/mo) with usage-based add-ons. Requires demonstrable ROI for procurement. Needs security/compliance review (SOC 2, data residency). |
| **Success Metrics** | Prototype-to-decision time. Documentation completeness (auto-generated). Cross-project knowledge reuse rate. Cost per validated prototype. Gate pass predictability. |

**Quote:** "I need to validate three game concepts this quarter. I also need every decision documented automatically so the production team can take over without a two-week knowledge transfer."

### 7.6 Anti-Personas (Who This Is NOT For)

| Anti-Persona | Why Not Target |
|--------------|----------------|
| **Manual Task Board User** | Wants to manually drag-and-drop tasks on a Kanban board and create tasks one at a time through a GUI. This product is AI-agent-primary -- the task system is optimized for machine operators, not a Jira/Trello replacement. |
| **Non-Game Developer** | Web, mobile, or enterprise software teams looking for general-purpose project management. The system is deeply integrated with GDLC (7 phases, 9 areas), UE5 plugins, and game design taxonomy. It is not a general-purpose tool. |
| **Hobbyist Without Shipping Intent** | Wants to experiment casually without a goal of shipping. The GDLC framework adds overhead that only pays off with a meaningful project. Subscription pricing ($99-$2,499/mo) assumes commercial or educational intent. |
| **AAA Studio with Existing Pipeline** | 500+ person studio with established internal tools (Shotgun, Perforce, custom pipelines). Unlikely to adopt an external AI-operated system that requires replacing existing workflow. Platform targets studios that do NOT have sophisticated tooling. |
| **Pure Prompt Engineer** | Wants AI for one-off tasks (generate a texture, write a shader) without structured project management. The task system adds value for multi-phase, multi-area projects, not isolated tool calls. |

---

## 8. Value Proposition Canvas

> **N/A for feature PRD.** Value proposition is defined at the platform level. The task management system's value contribution is captured in Section 2 (Problem Statement) and Section 4 (Product Vision). For platform-level value proposition, see the Platform PRD when available.

---

## 9. Competitive Analysis

> **N/A for feature PRD.** Competitive analysis is a platform-level concern. See the Platform PRD when available. Research artifacts with detailed competitive data are preserved at `.dev/tasks/to-do/TASK-PRD-20260319-143000/research/04-competitive-landscape.md`.

---

## 10. Assumptions & Constraints

### 10.1 Technical Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| TA-1 | PostgreSQL 15 with uuid-ossp and pgcrypto extensions is available in all environments | Migration fails; need extension installation or cloud provider config | Verify extension availability during Phase 1 environment setup |
| TA-2 | pg_partman extension is available or installable for monthly audit event partitioning | Must implement manual partition management or native PG declarative partitioning | Check cloud provider extension list during Phase 1 |
| TA-3 | TEXT `hierarchy_path` with B-tree index provides sub-millisecond rollup queries for ~500 nodes | Must upgrade to ltree sooner than planned (adds 1-2 weeks, non-breaking) | Benchmark during Phase 5 integration testing |
| TA-4 | `fillfactor=70` on hot tables enables HOT-eligible checkbox updates without index maintenance | Bulk checkbox performance degrades; may need different tuning | Load test during Phase 2 with 500-task trees |
| TA-5 | SQLAlchemy 2.0+ async session model supports `SET LOCAL app.organization_id` for RLS | Must use raw SQL or connection-level hooks; adds complexity | Test with FastAPI middleware + async_session before committing to RLS approach |
| TA-6 | Existing Alembic migration chain can accommodate standalone task migrations | May need migration chain cleanup before task models can be added | Inspect chain integrity in Phase 1; create standalone migrations if drifted |
| TA-7 | The 8 existing LangGraph agents can accept new tool descriptors without workflow restructuring | Agent refactoring needed; increases Phase 5 effort | Validate tool registration via Pattern A during Phase 2 |
| TA-8 | AI agents can operate effectively within ~2000 tokens per tool response | Zoom level token budgets need recalibration; may need more aggressive filtering | Build token counting utility into API response metadata |

### 10.2 Business Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| BA-1 | AI agents are the primary operators (95%+ of task management operations) | Architecture over-optimizes for AI; human UX suffers | Monitor agent vs. human operation ratios post-launch; human REST API (Phase 2) provides fallback |
| BA-2 | GDLC framework (7 phases, 9 areas) is stable during implementation | Template seeder output becomes invalid; re-seeding needed | Slug-based IDs and ON CONFLICT idempotency limit blast radius of changes |
| BA-3 | Multi-tenant SaaS model with organization-level isolation is the deployment model | RLS and org-level isolation are unnecessary overhead for single-tenant | RLS adds minimal overhead; provides security value regardless of tenant count |
| BA-4 | Platform targets 10,000+ concurrent users per instance | Scale infrastructure (partitioning, RLS, connection pooling) can be deferred if actual usage is lower | Start with RLS (low cost, high value); defer partitioning until audit_events table size justifies it |
| BA-5 | Event retention is configurable per subscription tier | Uniform retention simplifies implementation but may not meet enterprise needs | Start with uniform defaults (90-day hot, 1-year warm); add tier-based overrides as configuration |

### 10.3 User Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| UA-1 | Game developers interact with tasks primarily through the AI chat interface, not a traditional task board | Frontend task panel becomes primary interface; needs more investment | User research / beta feedback on interaction patterns |
| UA-2 | Human users need real-time visibility into AI agent task operations but do not manually edit tasks frequently | Must build full CRUD frontend earlier than planned | Monitor manual edit frequency post-launch |
| UA-3 | The 533-node taxonomy tree in the roadmap frontend maps naturally to the GDLC task hierarchy | Mapping layer between frontend nodes and backend tasks is more complex than expected | Prototype mapping during Phase 5 integration |

### 10.4 Constraints

| Type | Constraint | Impact on Product | Mitigation |
|------|------------|-------------------|------------|
| **Technology** | Python 3.11+ / FastAPI backend only | All new service code, models, and API routes must be Python/FastAPI; no new backend languages | N/A -- aligned with existing stack |
| **Technology** | SQLAlchemy 2.0+ ORM with AsyncPG; `Column()` legacy style required | Models must inherit from shared `Base` in `database.py:240`; only `AgentSession` uses newer `mapped_column()` style | Follow existing conventions exactly |
| **Technology** | PostgreSQL 15 as primary data store; no additional database engines for task state | pgvector and pg_partman acceptable as PostgreSQL extensions. Redis is permitted for async messaging only (vectorization pipeline trigger via Redis Stream, existing RQ task queue). Redis is NOT used for task state storage, pub/sub broadcasting, or real-time sync in MVP. No Kafka or EventStoreDB. | Real-time sync deferred post-Phase 5 |
| **Technology** | Existing agent tool Pattern A (agent-internal `get_available_tools()` + `execute_tool()`) | New task tools must follow proven pattern; not standalone class pattern | Pattern A is simpler and more stable than alternatives |
| **Technology** | No Agile terminology in data model | Task hierarchy uses depth-based labels (`item_type`), GDLC terminology only; no sprints, boards, story points | Deliberate product differentiation, not a limitation |
| **Timeline** | 11-15 weeks estimated total (5 phases) | Phase 1 (Data Model, 2-3 weeks) blocks everything; Phase 2 (AI Tool Layer, 3-4 weeks) is critical path | Phases 3-4 parallelizable after Phase 2 stabilizes |
| **Resource** | Solo developer + AI agents | No dedicated frontend developer; frontend integration deferred | Backend-first approach; REST API as stable interface contract |
| **Resource** | Zero team experience with event sourcing | Phase 3 carries learning curve risk | Additive approach (not CQRS) limits scope; reference implementations available |
| **Budget** | Alembic migration chain is drifted from ORM models | Must create standalone migrations; cannot depend on existing chain accuracy | Explicit `op.create_table()` calls; no dependency on `001_initial` |

---

## 11. Dependencies

### 11.1 External Dependencies

| Dependency | Type | Owner | Risk Level | Contingency |
|------------|------|-------|------------|-------------|
| **PostgreSQL 15** | Database engine | Platform infrastructure | Low | No alternative; core dependency. Already deployed and verified |
| **Pinecone** (Phase 4) | Vector database for semantic task memory | Pinecone Inc. | Low | Existing platform integration for conversation memory. `search_task_memory` tool stubbed in Phase 2; Pinecone integration deferred to Phase 4. Feature-flagged via `TASK_MEMORY_ENABLED` |
| **OpenAI Embedding API** (Phase 4) | `text-embedding-3-small` for task vectorization | OpenAI | Low | Existing provider via langchain-openai. Model-agnostic interface (`embed(text) -> List[float]`); store model name + version in metadata for re-embedding on model change |
| **LangChain / LangGraph** | Agent orchestration framework | LangChain Inc. | Medium | Framework actively evolving; version updates could break tool registration patterns. Mitigation: pin versions, follow Pattern A (proven stable) |
| **pg_partman** | PostgreSQL extension for automated audit partition management | PostgreSQL community | Medium | May not be available in all cloud providers. Fallback: manual declarative partitioning with cron-based script creating monthly partitions 3 months ahead |

### 11.2 Internal Dependencies

| Dependency | Type | Owner | Status | Target Date |
|------------|------|-------|--------|-------------|
| **Auth Service** (`backend/app/core/security.py`) | JWT verification, `get_current_user_id` | Backend | Functional | Phase 1 (existing) |
| **Project Service** (`backend/app/services/project_manager.py`) | Project CRUD, ownership verification | Backend | Functional | Phase 1 (existing) |
| **Database Infrastructure** (`backend/app/core/database.py`) | `Base` declarative base, `async_session`, `get_db_context()` | Backend | Functional | Phase 1 (existing) |
| **Agent System** (`backend/app/agents/base_agent.py`) | LangGraph workflow, `AgentState`, tool registration | Backend | Functional (8 agents) | Phase 2 |
| **Swarm Orchestrator** (`backend/app/agents/swarm_orchestrator.py`) | Multi-agent coordination, keyword routing | Backend | Functional | Phase 2 |
| **Session Context** (`backend/app/agents/session_context.py`) | `SessionAwareToolMixin`, `SessionContextManager` | Backend | Defined but unused (no current consumers) | Phase 2 |
| **Alembic Migration System** (`backend/alembic/`) | Schema migration management | Backend | Drifted from ORM models | Phase 1 (standalone migrations) |
| **Activity Cache Service** (`backend/app/services/activity_cache.py`) | In-memory write batching pattern reference | Backend | Functional, feature-flagged | Phase 5 (pattern reference) |
| **GDLC Frontend Types** (`frontend/app/roadmap/types/gdlc.ts`) | `AreaId` type, Phase Focus Matrix, `GDLC_PHASE_LABELS` | Frontend | Authoritative source | Phase 5 (template seeder input) |

### 11.3 Cross-Team Dependencies

| Team | Dependency | What We Need | When Needed | Status |
|------|------------|--------------|-------------|--------|
| **Frontend** (future) | Zustand store slices, task panel component, WebSocket consumer | Stable REST API contract as interface | Post-Phase 5 | Not started; deferred |
| **DevOps** | pg_partman installation, PgBouncer configuration, monitoring dashboards | Extension availability confirmation; Prometheus dashboard config | Phase 1 (pg_partman), Phase 5 (dashboards) | Infrastructure exists; extensions may need provisioning |
| **GDLC Content** | Phase 7 (Live Ops) work order completion | Complete work order document or confirmation it is intentionally empty | Phase 5 (template seeder) | Missing; seeder handles gracefully with placeholder |

---

## 12. Scope Definition

### 12.1 In Scope (Full System — Phases 1-5, 11-15 weeks)

| Category | Included | Notes |
|----------|----------|-------|
| **Core Task Tree** | Hierarchical task model with `parent_task_id` self-referential FK, `depth` column (0-3+), `hierarchy_path` TEXT with B-tree index, adjacency list pattern | Foundation for all other capabilities |
| **GDLC Taxonomy Integration** | `gdlc_phase` (Integer), `area_id` (String, 9 stable IDs from `gdlc.ts`), Phase Focus Matrix mapping | Tasks tie to taxonomy via metadata columns, not a separate hierarchy |
| **Task Dependencies** | `TaskDependency` model with `dependent_task_id` + `required_task_id` FKs, composite unique constraint, `dependency_type` column | Separate from `related_docs` (informational links) |
| **State Machine** | 5-state model (To Do / Doing / Done / Blocked / Cancelled) with 9 allowed transitions, 11 forbidden, 1 idempotent. Done and Cancelled are terminal (zero outbound transitions). Cancellation permission-gated to orchestrator + human only. See US-1.2. | Full 5x5 matrix, side-effect table, error catalog in Crit1 remediation |
| **Checklists** | Relational `ChecklistItemInstance` table with `is_checked`, `checked_at`, `checked_by`, `blocker_reason`, `completion_type`; `fillfactor=70` for HOT-eligible bulk updates | Per-item audit fields for gate verification |
| **Templates** | `TaskTemplate` + `ChecklistItemTemplate` with `content_snapshot` JSONB; GDLC template seeder parsing ~608 gate + ~98 work order items; slug-based IDs; `ON CONFLICT` idempotency | Copy-on-create with date remapping |
| **Domain Facade API** | ~5 agent-facing tools (`query_tasks`, `mutate_tasks`, `bulk_operations`, `search_task_memory` stub, `query_audit_trail` stub) consolidating ~60 granular operations. `project_id` REQUIRED on all tool calls (injected from AgentState). No org-level aggregation via agent tools — org dashboards served by REST API. | Tool definitions <2K tokens total |
| **Zoom Levels** | 4 levels (Dashboard ~120-180 tokens, List ~40-55/task, Detail ~500-2000/task, Full ~2000-10000/task); `detail` parameter on all list endpoints; `fields` parameter overrides zoom presets | Optimized for LLM context windows |
| **Bulk Operations** | `create_task_tree` (~500 tasks, single transaction), `batch_update_status`, `batch_check_items`, `resolve_dependencies`, `check_gate_readiness`; partial-success semantics | Novel API pattern -- no competitor reference implementation |
| **Cursor Pagination** | Keyset pagination via `(sort_col, id)` encoding; stable across concurrent inserts/deletes; page sizes 1-500; response envelope with `total_count`, `has_more`, `next_cursor` | Designed for AI agent iteration |
| **Audit Events** | Append-only `audit_events` table in `audit` schema; 14 event types; RFC 6902 JSON Patch diffs; `agent_id`, `session_id`, `metadata` JSONB; monthly range partitions via pg_partman | Compliance and debugging foundation |
| **Row-Level Security** | `organization_id` UUID on every table; RLS policies enforcing tenant isolation; FastAPI middleware sets `SET LOCAL app.organization_id` per request | Multi-tenant isolation at database level |
| **Human REST API** | Standard REST endpoints calling shared `TaskService`; auth via JWT; offset pagination for backward compatibility with existing endpoints | Same service layer as agent tools |

### 12.2 Out of Scope (Not in Phases 1-5)

| Item | Reason |
|------|--------|
| Real-Time Collaboration | Requires `TaskConnectionManager` (WebSocket), Redis pub/sub for cross-instance bridging, frontend WebSocket consumer. No Redis pub/sub exists today. Deferred post-Phase 5. |
| Frontend Integration | Zustand store slices, task panel component, roadmap canvas hooks, optimistic updates. Depends on REST API + WebSocket being stable. Deferred post-Phase 5. |
| Advanced Analytics | Burndown charts, velocity tracking, predictive completion. Requires sufficient historical data that won't exist until the system is in production. |
| Third-Party Integrations | GitHub Issues, Jira, Linear import/export. Platform must stabilize its own task model first. |
| Template Upgrade-in-Place | Applying template version changes to existing project instances. Complex migration logic. Deferred until usage patterns reveal which upgrade paths are actually needed. |
| ltree Hierarchy Upgrade | PostgreSQL ltree extension for advanced tree queries. TEXT LIKE is sufficient for ~500 nodes. Non-breaking upgrade when needed. |
| pgvector for Local Search | Task-local semantic search within PostgreSQL. Evaluate whether Pinecone alone is sufficient. |
| Mobile Interface | No mobile frontend exists. Platform is browser-first. Not planned. |

### 12.3 Permanently Out of Scope

| Item | Reason |
|------|--------|
| **Agile Terminology** | System uses GDLC terminology (phases, areas, gate checklists), not Scrum/Kanban terminology (sprints, boards, story points). This is a deliberate product differentiation -- the task system speaks game development, not generic software project management |
| **Standalone PM Tool** | This is NOT a general-purpose project management tool. It is a domain-specific task layer for the GameFrame AI platform, operated primarily by AI agents. It will never compete with Linear/Jira/Asana as a standalone product |
| **CQRS as Primary Store** | Event-sourced primary store (Option D) was evaluated and rejected. Audit events are additive alongside mutable relational tables, not the source of truth for current state |

---

## 13. Open Questions

> Research phase resolved all 20 original design questions. This section documents those resolutions and surfaces remaining gaps from PRD-level synthesis.

### 13.1 Resolved Questions (from AI-Operator Research)

| # | Question | Owner | Target Date | Status | Resolution |
|---|----------|-------|-------------|--------|------------|
| 1 | Should the task hierarchy use fixed Agile levels or variable depth? | Product | 2026-03-19 | RESOLVED | Variable-depth tree with configurable `max_depth` (default 6). `item_type` enum for depth labels. No Agile terminology -- uses GDLC phase/area/subcategory. |
| 2 | What is the event retention policy? | Product | 2026-03-19 | RESOLVED | Configurable per subscription tier. Hot 0-90 days (full retention), Warm 90-365 days (reduced indexes), Cold 1-3 years (S3/GCS Parquet archive), 3+ years (delete unless compliance requires). |
| 3 | Is the DB event log or MDTM markdown the source of truth? | Engineering | 2026-03-19 | RESOLVED | Database event log is the single source of truth. MDTM markdown is a rendered view -- useful for human readability but not authoritative for state. |
| 4 | What is the audit table named? | Engineering | 2026-03-19 | RESOLVED | `audit_events` (broader scope than task-only). Located in dedicated `audit` schema. |
| 5 | How do zoom levels map to token budgets? | Engineering | 2026-03-19 | RESOLVED | L0 Dashboard ~120-180 tokens total, L1 List ~40-55 tokens/task, L2 Detail ~500-2000 tokens/task, L3 Full ~2000-10000 tokens/task. Default is L1 for list endpoints. |
| 6 | How many domain facade tools? | Engineering | 2026-03-19 | RESOLVED | ~5 primary tools (`query_tasks`, `mutate_tasks`, `bulk_operations`, `search_task_memory` stub, `query_audit_trail` stub). The ~9 figure from some sources includes sub-commands within facades. |
| 7 | Should templates be immutable or editable after publish? | Product | 2026-03-19 | RESOLVED | Immutable once published. New versions use SemVer (MAJOR.MINOR.PATCH). Patch = safe auto-apply, Minor = review recommended, Major = manual review required. |
| 8 | What conflict resolution strategy for concurrent agent writes? | Engineering | 2026-03-19 | RESOLVED | Per-operation policies: checklist items = no conflict (independent rows), status updates = last-write-wins (state machine validates), field updates = optimistic locking + retry once then escalate, bulk ops = advisory locks. |
| 9 | Cursor-based or offset-based pagination? | Engineering | 2026-03-19 | RESOLVED | Cursor-based for all new task endpoints. Existing endpoints retain offset-based for backward compatibility. |
| 10 | Per-operation concurrency policies? | Engineering | 2026-03-19 | RESOLVED | Defined per operation type (see Q8). `CONCURRENT_MODIFICATION` error code with re-read-and-retry guidance for agents. |
| 11 | How are GDLC gate decisions modeled? | Product | 2026-03-19 | RESOLVED | Ternary outcome: Go / No-Go / Conditional Pass. `check_gate_readiness` bulk operation aggregates across full phase subtree. Phase 7 uses continuous Health Check (Green/Yellow/Red). |
| 12 | How many task states? | Product | 2026-03-19 | RESOLVED | 4 primary states (To Do, Doing, Done, Blocked) + `cancelled` as 5th DB-only state. MDTM files remain 4-state. |
| 13 | What fields does each zoom level return? | Engineering | 2026-03-19 | RESOLVED | L0: aggregate counts by status/phase. L1: id, title, status, priority, phase, area, assigned_to, progress, due_date, blocked flag. L2: all frontmatter + checklist summary + next unchecked + recent log. L3: everything including all items, full log, review info. |
| 14 | What is the maximum hierarchy depth? | Product | 2026-03-19 | RESOLVED | Configurable `max_depth` with default 6. Most projects will use 3-4 levels. |
| 15 | How are genre-conditional items handled? | Product | 2026-03-19 | RESOLVED | 291 genre-conditional items (of ~791 total) included/excluded at template instantiation time based on wizard output. Copy-on-create -- instances are independent of template after creation. |
| 16 | What is the Organization model? | Engineering | 2026-03-19 | RESOLVED | `organization_id UUID NOT NULL` FK on every task table. RLS enforced at DB level. Pool pattern (shared schema + tenant_id) for Indie/Studio; Silo option for Enterprise. |
| 17 | How do agents authenticate to task endpoints? | Engineering | 2026-03-19 | RESOLVED | Session context (`session_id`, `project_id`, `user_id`) injected from `AgentState` by `base_agent.execute_tools()`. No separate agent auth -- agents operate within user's session. |
| 18 | What is the vectorization trigger? | Engineering | 2026-03-19 | RESOLVED | Triggered by `task.status_changed` event when status becomes "done". Async via Redis Stream + background worker. Does not block status transition (<200ms). Feature-flagged `TASK_MEMORY_ENABLED`. |
| 19 | What embedding model for task memory? | Engineering | 2026-03-19 | RESOLVED | OpenAI `text-embedding-3-small` (1536 dimensions). Model-agnostic interface stores model name + version in metadata for re-embedding on model change. |
| 20 | How are bulk operation side effects reported? | Engineering | 2026-03-19 | RESOLVED | Bulk responses include side effects (newly unblocked tasks, gate readiness changes) in response payload. Parent + child audit events linked via `parent_event_id`. |

### 13.2 Remaining Open Questions (from PRD Synthesis)

| # | Question | Owner | Target Date | Status | Resolution |
|---|----------|-------|-------------|--------|------------|
| 21 | Organization model does not exist in codebase. Must be created or stubbed as FK target before task tables. `organization_id` appears on every table, RLS policies reference it, FastAPI middleware extracts it from JWT — but no `organizations` table schema, no CRUD, no relationship to existing `User` model (which uses `owner_id`). This is a Phase 1 blocker. | Engineering | Phase 1 | OPEN | Decision needed: (a) minimal stub table (`id`, `name`, `created_at`) sufficient as FK target + RLS anchor, or (b) full Organization CRUD with membership, billing, settings. Recommendation: minimal stub for Phase 1, full model in a separate Organization Service PRD. Migration path from `owner_id` to `organization_id` must be defined. |
| 22 | Complete enum values for MDTM `type` and `priority` fields are not fully enumerated. Templates show examples but not the exhaustive valid set. | Product | Phase 1 | OPEN | Audit all existing MDTM files in `.dev/tasks/` to extract full enum values before schema creation. |
| 23 | Dynamic content marker syntax for `task_type: dynamic` is undocumented. | Engineering | Phase 1 | OPEN | Define syntax specification before implementing dynamic task item insertion. |
| 24 | `AgentProviderService` integration path not investigated. May affect how task tools surface in CoPilotKit chat interface. | Engineering | Phase 2 | OPEN | Investigate during Phase 2 AI Tool Layer implementation. |
| 25 | Phase 7 (Live Ops) work order is missing from GDLC docs. Only 6 of 7 phases have work orders. | Product | Phase 1 | OPEN | Template seeder must handle gracefully -- empty phase with placeholder items. |
| 26 | Frontend field mapping: 5 MDTM-to-TaskNode gaps identified (status enum mismatch, priority format, estimation type, no `blocks` reverse reference, no `progress` percentage). | Engineering | Phase 5 | OPEN | Resolve during frontend integration phase. Define adapter layer. |
| 27 | Educational pricing tier undefined. Three tiers exist (Indie $99, Studio $499, Enterprise $2,499) but no multi-seat classroom pricing. | Product | Pre-launch | OPEN | Define educational pricing before targeting educator persona. |
| 28 | No user research validation. All personas derived from CLAUDE.md segments and technical constraints, not interviews. | Product | Pre-launch | OPEN | Plan user research sessions to validate persona assumptions. Flag as assumption in PRD. |
| 29 | Multi-region deployment missing from scope despite Enterprise compliance needs. | Engineering | Phase 2+ | OPEN | Add as Enterprise-tier requirement. Not MVP blocker. |
| 30 | Regulatory/compliance risks (EU AI Act, GDPR) not fully quantified in risk matrix. | Legal/Product | Pre-launch | OPEN | Add compliance risk items with revenue-percentage impact estimates. |
| 31 | What are the specific Pixel Streaming hour caps per tier? | Product | Pre-launch | OPEN | Pricing -- highest marginal cost item needs defined limits (see Platform PRD — Business Requirements). |
| 32 | What LLM token usage caps apply per tier? | Product | Pre-launch | OPEN | Margin protection -- AI compute costs must be bounded (see Platform PRD — Business Requirements). |
| ~~33~~ | ~~Is there an educational pricing tier?~~ | -- | -- | DUPLICATE | Duplicate of Q27 (educational pricing). |
| 34 | What is the free tier / reverse trial design? | Product | Pre-launch | OPEN | Market expects free entry point; conversion funnel depends on this (see Platform PRD — Business Requirements). |
| 35 | What WCAG compliance level is targeted for the roadmap canvas? | Engineering | Pre-launch | OPEN | Canvas-based UIs are inherently challenging for accessibility; may need text-alternative view (S16.3). |
| 36 | How does Art. 22 (automated decision-making) apply when AI agents make task management decisions that indirectly affect employment outcomes? | Legal/Product | Pre-launch | OPEN | If task assignment based on developer performance metrics creeps into the system, classification may shift to high-risk under EU AI Act (S17.1). |
| 37 | What is the data retention policy for closed/churned accounts? | Legal/Product | Pre-launch | OPEN | GDPR right to deletion vs. compliance audit trail preservation creates tension (S17.1, see also Platform PRD — Data Privacy). |
| 38 | Should enterprise pricing be hidden behind "Contact Sales"? | Product | Pre-launch | OPEN | Current published $2,499/mo limits negotiation flexibility but increases transparency (see Platform PRD — Business Requirements). |

---

## 14. Technical Requirements

### 14.1 Architecture Requirements

| Requirement | Description | Rationale |
|-------------|-------------|-----------|
| **Option C Hybrid Data Model** | Relational core (typed columns for all 22 MDTM frontmatter fields) with JSONB columns reserved for extensible metadata and template snapshots | Balances query performance and schema evolution; Option B (JSONB-Heavy) failed 4 of 8 AI-operator constraints; Option D (full event-sourced) rejected as overkill -- audit/replay achievable additively |
| **4 Additive Enhancements** | (1) `audit_events` append-only table, (2) `organization_id` + RLS on all tables from day one, (3) compound indexes `(project_id, status, priority)`, (4) scale infrastructure in Phase 1 | Retrofitting tenant isolation is 4-5x more expensive than designing in; compound indexes serve the 3 most common agent query patterns |
| **Domain Facade Pattern** | ~5 facade tools (`query_tasks`, `mutate_tasks`, `bulk_operations`, `search_task_memory`, `query_audit_trail`) replacing ~60 granular tools | Reduces tool-definition token overhead from ~12K to ~2K tokens (83% reduction); AI agents are primary operators (95%+ of mutations) |
| **Zoom-Level API** | 4 response levels: L0 Dashboard (~150 tokens), L1 List (~50 tokens/task), L2 Detail (~500-2K tokens/task), L3 Full (~2K-10K tokens/task) | Controls response token cost per query; agents select minimum zoom level needed, reducing context window consumption by 65-95% |
| **Cursor-Based Pagination** | Keyset pagination via `(sort_col, id) > (:cursor_sort_val, :cursor_id)` with Base64-encoded cursors; up to 500 items/page | Stable across concurrent inserts/deletes (unlike offset); critical for multi-agent concurrent access |
| **CQRS Read Models (Additive)** | Materialized views (`agent_active_tasks`, `project_health_summary`, `gate_readiness`) + projection tables updated via LISTEN/NOTIFY | Pre-compute answers agents commonly need; reduces token cost 10-100x vs ad-hoc aggregation queries |
| **TEXT Hierarchy Path** | `hierarchy_path` TEXT column with B-tree index; dot-separated slugs, `LIKE 'gameplay.cs.%'` for subtree queries | Lightweight alternative to ltree extension; deferrable upgrade path; supports variable-depth task trees |
| **Status State Machine** | 4 primary states (`to_do` -> `doing` -> `done`, `blocked` side-state) + `cancelled`; transitions validated in `TaskService` | Single `status` column avoids dual-track anti-pattern; actionable error codes on invalid transitions |
| **Event Sourcing (Additive)** | Append-only `audit_events` in same PostgreSQL instance, separate `audit` schema; co-transactional with entity mutations | No dual-write problem; full audit trail with RFC 6902 diffs; agent self-reflection via `query_audit_trail` tool |
| **Semantic Memory Pipeline** | Task completion triggers async vectorization -> Pinecone `task-memory` index; `search_task_memory` tool for cross-project learning | Enables agents to learn from past task completions; namespace-per-organization isolation |

> **Source:** Research `03-architecture-technical.md` Sections 1.1-1.5

### 14.2 Performance Requirements

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Agent tool call (single CRUD) | < 200ms (p95) | Prometheus histogram on FastAPI endpoint latency |
| Dashboard query (zoom L0) | < 50ms | Pre-aggregated materialized view; Prometheus |
| List query (zoom L1, 25 tasks) | < 100ms | Compound B-tree index scan with cursor pagination; Prometheus |
| Batch checkbox update (50 items) | < 200ms | Single UPDATE on HOT-eligible table (`fillfactor=70`); Prometheus |
| Status transition | < 200ms | Single-row UPDATE + audit event INSERT in one transaction; Prometheus |
| Bulk tree creation (~500 tasks) | < 5 seconds | Batch INSERT via `executemany()`; load test benchmark |
| Semantic search (Pinecone) | < 500ms | External API call, async, not on critical path; Pinecone dashboard |
| LISTEN/NOTIFY projection update | < 1 second | PostgreSQL trigger -> async worker -> projection table; lag monitor |
| Gate readiness check | < 50ms | Direct SQL aggregation; add materialized view if P95 exceeds target |
| Vectorization (post-completion) | < 30 seconds | Async background worker; does not block status transition |
| System uptime | 99.9% | Prometheus + Grafana alerting |
| Concurrent users | 10,000+ per instance | Load testing with k6 or Locust |

**Throughput Targets:**

| Metric | Target | Basis |
|--------|--------|-------|
| Concurrent AI agents per project | 8+ | Current agent swarm architecture |
| Audit events/sec (sustained) | 110-555 | 8 agents x 10-50 actions/session x 10K users |
| Audit events/sec (burst) | > 1,000 | Bulk operations generate hundreds of events per transaction |
| PostgreSQL demonstrated capacity | 8,586 events/sec | Benchmark with 50 concurrent writers |

**Write Optimization:**

| Technique | Target Table | Purpose |
|-----------|-------------|---------|
| `fillfactor=70` | `task_instance_items` | HOT-eligible checkbox updates (bypass index maintenance) |
| Aggressive autovacuum (`scale_factor=0.001`) | High-update tables | Prevent bloat on frequently-updated rows |
| Batch INSERT (`executemany()`) | `task_instances`, `task_instance_items` | Template instantiation performance |
| Bulk UPDATE (`WHERE id IN`) | `task_instance_items` | Batch status changes |
| Advisory locks `(project_id, op_type)` | Bulk operations | Serialize concurrent bulk ops per project |

> **Source:** Research `03-architecture-technical.md` Sections 2.1-2.4

### 14.3 Security Requirements

| Requirement | Implementation | Compliance |
|-------------|----------------|------------|
| **Multi-Tenant Isolation** | `organization_id UUID NOT NULL` on every task table; PostgreSQL Row-Level Security (`ENABLE ROW LEVEL SECURITY` + `FORCE ROW LEVEL SECURITY`); `tenant_isolation` policy: `USING (organization_id = current_setting('app.organization_id')::uuid)` | SOC 2 data isolation; GDPR data segregation |
| **RLS Session Binding** | FastAPI middleware extracts `organization_id` from JWT, executes `SET LOCAL app.organization_id = '{uuid}'` per request; `SET LOCAL` scopes to current transaction and auto-clears | Prevents cross-tenant data leakage at DB level |
| **Authentication** | OAuth2 + JWT via `Depends(get_current_user_id)` on all task endpoints; existing python-jose + passlib/bcrypt stack | OWASP Authentication |
| **Authorization** | Ownership verification via `select().where(organization_id == current_org_id)`; RLS enforces at DB level as additional safety net | Defense-in-depth (application + database layer) |
| **Agent Authentication** | `agent_id` and `session_id` tracked on every `audit_events` record; all agent mutations attributable | Full agent accountability |
| **Audit Logging** | Every mutation generates immutable `audit_events` record: `agent_id`, `session_id`, `before_state`/`after_state` JSONB, RFC 6902 `diff`; append-only (no UPDATE/DELETE on `audit_events`) | SOC 2 audit trail; GDPR right-to-audit |
| **Optimistic Concurrency** | `stream_version` per entity prevents silent overwrites; retry once, then escalate to orchestrator | Prevents data loss from concurrent agent writes |
| **Idempotency Keys** | `idempotency_key` on destructive operations in `audit_events.metadata` | Prevents replay attacks and accidental double-execution |
| **Data Encryption** | TLS in transit (existing); PostgreSQL pgcrypto extension available for at-rest encryption of sensitive fields | OWASP Data Protection |

**Tenant Isolation Escalation Path:**

| Tier | Isolation Model | Target Scale | Use Case |
|------|----------------|-------------|----------|
| Default (all tiers) | Shared table + RLS | Millions of tenants | Standard SaaS multi-tenancy |
| Enterprise | Schema-per-tenant | < 100 tenants | Stronger isolation for compliance-sensitive customers |
| Compliance | Database-per-tenant | < 10 tenants | Strongest isolation; highest operational cost |

**Cross-Tenant Operations:** `platform_admin` database role bypasses RLS for platform-level agents only (not customer-facing).

> **Source:** Research `03-architecture-technical.md` Sections 3.1-3.3

### 14.4 Scalability Requirements

| Dimension | Current Target | Future Target | Approach |
|-----------|----------------|---------------|----------|
| **Users** | 10,000 concurrent | 100,000+ | Horizontal API scaling + PgBouncer connection pooling + read replicas |
| **Tasks per project** | ~500 (GDLC template) | ~5,000 | Compound indexes; cursor pagination; no schema changes needed |
| **Tasks per organization** | ~50,000 (100 projects) | ~500,000 | Hash partitioning by `organization_id` when table exceeds 10M rows |
| **Tasks platform-wide** | ~50,000,000 (1000 orgs) | ~500,000,000 | Distributed PostgreSQL (Citus) with `organization_id` as distribution key |
| **Audit events (monthly)** | ~200,000,000 | Billions | Monthly range partitions via pg_partman; `DROP TABLE` on detached partition (instant) |
| **Vectors (Pinecone)** | ~50,000 per org | ~500,000 per org | Namespace-per-organization; Pinecone scales horizontally |

**Scaling Progression Path:**

| Stage | Scale | Actions |
|-------|-------|---------|
| 1. Single PG instance | MVP, < 1,000 users | SQLAlchemy async pool (`pool_size=20, max_overflow=20`) |
| 2. Connection pooling + read replicas | 1,000-10,000 users | PgBouncer (`NullPool` + `statement_cache_size=0` in asyncpg); route reads to replicas |
| 3. Native partitioning | 10,000-100,000 users | Hash/composite partition large tables; pg_partman for audit events |
| 4. Distributed PG (Citus) | 100,000+ users | Distribute tables across worker nodes by `organization_id` |

**Partition Strategy:**

| Table | Method | Trigger | Details |
|-------|--------|---------|---------|
| `audit_events` | `RANGE (created_at)` | From Phase 1 | Monthly partitions; `p_premake => 3`; hot partition in memory; cold on slower storage |
| `task_instances` | `HASH (organization_id)` | Deferred until > 10M rows | Composite PK `(organization_id, id)` designed in from Phase 1 for future partitioning |

**Concurrency Model:**

| Operation | Conflict Resolution |
|-----------|-------------------|
| Checklist items | No conflict -- independent rows, any agent can check any item |
| Status updates | Last-write-wins -- state machine validates transition legality |
| Field updates | Optimistic locking (`stream_version`) + retry once, then escalate |
| Bulk operations | Advisory locks on `(project_id, operation_type)` |
| Template instantiation | Single transaction, no conflict possible |

> **Source:** Research `03-architecture-technical.md` Sections 4.1-4.5

### 14.5 Data & Analytics Requirements

| Data Type | What to Collect | Why | Storage/Retention |
|-----------|-----------------|-----|-------------------|
| **Audit events** | Every task mutation: `agent_id`, `session_id`, `action_type`, `before_state`/`after_state` JSONB, RFC 6902 `diff`, `metadata` (correlation_id, causation_id, tool_name, reasoning_summary) | Agent accountability, compliance audit trail, state reconstruction, agent self-reflection | Hot: 90 days (PostgreSQL); Warm: 1 year (PostgreSQL cold partition); Cold: 7 years (S3/GCS Parquet) |
| **Entity snapshots** | Full entity state every 50-100 events | Fast state reconstruction without replaying full event stream | Same retention as audit events |
| **Task completion vectors** | Embedding of 9 high-signal fields per completed task (OpenAI `text-embedding-3-small`, 1536 dimensions) | Cross-project semantic search; agents learn from past task patterns | Pinecone `task-memory` index; namespace-per-organization; indefinite retention |
| **Project health metrics** | Aggregated counts by status, phase, priority per project | Dashboard (zoom L0), gate readiness checks | Materialized view `project_health_summary`; trigger-refreshed, < 5s lag |
| **Agent activity** | Active assignments per agent, sorted by priority | Agent workload balancing, orchestrator decisions | Materialized view `agent_active_tasks`; trigger-refreshed |
| **Dependency status** | Blocked/unblocked status with blocker details per task | Dependency resolution, critical path analysis | Materialized view `task_dependency_status`; trigger-refreshed |

**14 Event Types (Audit Trail):**

| Event Type | Trigger | Key Fields |
|------------|---------|------------|
| `task.created` | New task instance | Full initial state |
| `task.status_changed` | Status transition | `before_state.status`, `after_state.status` |
| `task.field_updated` | Any field mutation | RFC 6902 diff |
| `task.deleted` | Task removal | Full final state |
| `item.checked` | Checklist item completed | `item_id`, `checked_by` |
| `item.blocked` | Item marked blocked | `item_id`, `blocker_reason` |
| `item.added` | New checklist item | Item content |
| `dependency.added` | New dependency edge | `dependent_task_id`, `required_task_id` |
| `dependency.resolved` | Dependency satisfied | `dependent_task_id`, `required_task_id` |
| `gate.decision` | Phase gate pass/fail | Gate criteria, decision |
| `assignment.changed` | Task reassigned | `before_state.assigned_to`, `after_state.assigned_to` |
| `bulk.status_update` | Batch status change | Parent event + child events linked via `causation_id` |
| `bulk.tree_created` | Template instantiation | Parent event + child events |
| `bulk.items_checked` | Batch checkbox update | Parent event + child events |

**Analytics Tools:**

| Tool | Purpose |
|------|---------|
| Prometheus + Grafana | API latency histograms, throughput monitoring, system health dashboards |
| PostgreSQL materialized views | Pre-computed agent query answers (5 views); trigger-refreshed |
| LISTEN/NOTIFY projection worker | Zero-lag update of `entity_current_state` and `project_task_summary` read models |
| Pinecone | Semantic search across completed tasks; cross-project learning |

> **Source:** Research `03-architecture-technical.md` Sections 1.4, 5.1-5.4

---

## 15. Technology Stack

> **Note:** The task management system requires zero new infrastructure for its core. All backend, frontend, and infrastructure technologies are already deployed in the existing platform. Only two small additive dependencies are introduced (pg_partman, jsonpatch).

### 15.1 Backend

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Language | Python | 3.11+ | Existing; async throughout |
| Framework | FastAPI | Latest | Existing; 14 routers in `backend/app/api/v1/` |
| Database | PostgreSQL | 15 | Existing; extensions: uuid-ossp, pgcrypto; RLS-capable |
| ORM | SQLAlchemy | 2.0+ | Existing; async DeclarativeBase, `Column()` style |
| DB Driver | asyncpg | Latest | Existing; requires `statement_cache_size=0` when paired with PgBouncer |
| Migrations | Alembic | Latest | Existing; 2 migrations in current chain |
| Cache / Queue | Redis | 7 | Existing; key-value store + RQ task queue |
| AI Orchestration | LangChain + LangGraph | Latest | Existing; 8 specialist agents, StateGraph, MemorySaver |
| Vector DB | Pinecone | Latest | Existing; conversation memory; extended for `task-memory` index |
| Auth | OAuth2 + JWT | python-jose, passlib/bcrypt | Existing; `Depends(get_current_user_id)` pattern |
| Logging | structlog | Latest | Existing; structured JSON logging |
| Metrics | Prometheus client | Latest | Existing; histogram/counter instrumentation |
| Error Tracking | Sentry | Latest | Existing |

**New Dependencies (Additive Only):**

| Dependency | Purpose | Risk Assessment |
|------------|---------|-----------------|
| pg_partman (PostgreSQL extension) | Automated monthly partition management for `audit_events` table | Low -- widely adopted PostgreSQL extension; no application code dependency |
| jsonpatch (Python library) | RFC 6902 JSON Patch diff computation for audit event `diff` field | Low -- stdlib-compatible, small dependency, well-maintained |
| OpenAI text-embedding-3-small | Task vectorization for semantic memory (1536 dimensions) | Low -- already using OpenAI via langchain-openai; incremental API usage |
| pgvector (PostgreSQL extension) | Task-local semantic search (deferred to post-MVP evaluation) | Deferred -- evaluate whether Pinecone alone is sufficient |

### 15.2 Frontend

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Framework | Next.js | 14.2.5 | Existing; App Router |
| Language | TypeScript | Strict mode | Existing |
| UI Runtime | React | 18+ | Existing |
| State Management | Zustand | 14 slices | Existing; new `task` slice needed for task management UI |
| Real-Time | Socket.io-client | Latest | Existing; extend for task mutation events |
| Canvas | React-based roadmap canvas | Custom | Existing in `frontend/app/roadmap/`; needs persistence layer to task DB |
| Styling | Tailwind CSS | Latest | Existing |
| Data Fetching | @tanstack/react-query | Latest | Existing; use for task API server state |
| Forms | React Hook Form + Zod | Latest | Existing; use for task creation/editing forms |

### 15.3 Infrastructure

| Component | Technology | Notes |
|-----------|------------|-------|
| Containerization | Docker Compose | Existing; 22 compose files |
| Orchestration (production) | Kubernetes + ArgoCD | Existing manifests in `k8s/`; Kustomize base + overlays |
| CI/CD | GitHub Actions | Existing; 6 workflows; gated pipeline with GHCR publishing |
| Container Registry | GHCR | Existing |
| IaC | Terraform (AWS) | Existing in `terraform/`; EKS, RDS, ElastiCache, S3, VPC |
| Helm Charts | Helm | Existing in `helm/` |
| Monitoring | Prometheus + Grafana | Existing; add task management dashboards |
| Logging | structlog -> stdout | Existing; container log aggregation |
| Secrets | HashiCorp Vault | Existing; policies in `vault/` |
| Networking | Tailscale | Existing; runner connectivity |

### 15.4 Codebase Integration Points

| Integration | Location | Pattern |
|-------------|----------|---------|
| Models | `backend/app/models/task.py` (new file) | Inherit `Base` from `database.py:240`; UUID PKs; `Column()` style; `__repr__()` |
| Model registration | `backend/app/models/__init__.py` | Add imports + `__all__` entries |
| Alembic registration | `backend/alembic/env.py:32-39` | Add model imports for autogenerate |
| Database init | `backend/app/core/database.py:283-290` | Add model import to `init_db()` |
| Schemas | `backend/app/schemas/task.py` (new file) | Pydantic v2: `TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskListResponse`; `from_attributes=True` |
| Service | `backend/app/services/task_service.py` (new file) | Module-level singleton; `structlog`; `session_scope()` for DB sessions |
| API Router | `backend/app/api/v1/tasks.py` (new file) | `APIRouter()`; prefix `/api/v1/tasks`; `Depends(get_current_user_id)` + `Depends(get_db)` |
| Router registration | `backend/app/main.py:140-153` | `app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])` |
| Agent tools | `backend/app/agents/tools/task_tools.py` (new file) | Domain Facade pattern; `get_available_tools()` + `execute_tool()` |
| Exceptions | `backend/app/core/exceptions.py` | `TaskException(GameFrameException)`; `TaskTransitionError` |
| Config | `backend/app/core/config.py` | `ENABLE_TASK_MANAGEMENT` feature flag in `Settings` class |
| Validation | `backend/app/core/api_validation.py` | Task-specific validators; `@validate_endpoint` decorator |

> **Source:** Research `03-architecture-technical.md` Sections 6.1-6.5

---

## 16. User Experience Requirements

GameFrame AI has two distinct UX surfaces: the **human dashboard** (browser-based UI for game developers) and the **AI agent interface** (programmatic API consumed by 8 specialist LLM agents). The AI agent interface is primary -- 95%+ of all task management operations are performed by AI agents, not humans. UX requirements must address both consumers.

### 16.1 Onboarding Experience

> **N/A for feature PRD.** Onboarding experience (account creation, wizard completion, pixel streaming setup) is a platform-level concern documented in the Platform PRD. The task management system's contribution to onboarding is the `create_task_tree` bulk operation that scaffolds ~500 GDLC tasks from a template in <5 seconds — this is covered in S21.1 (Epic 1, US-1.5).

### 16.2 Core User Flows

#### 16.2.1 Human User Flows

| Flow | Steps | Success Criteria |
|------|-------|------------------|
| **Project Creation** | Sign up > Complete wizard > Review generated task tree on roadmap canvas | User sees 500+ tasks organized by GDLC phase and area within 30 seconds of wizard completion |
| **Natural Language Game Modification** | Describe change in chat > Agent identifies relevant tasks > Agent executes changes > Preview updates via Pixel Streaming | Change reflected in preview within 60 seconds; task status updated; audit trail records agent actions |
| **Project Health Review** | Open dashboard > View phase/area status matrix > Identify blocked items > Drill into specific blocker | Dashboard loads in <50ms; blocked tasks show blocker_reason and blocking dependency |
| **Gate Review** | Navigate to gate checklist > Review completion status > Make go/no-go decision > Record gate decision | Gate readiness check aggregates across full phase subtree; decision recorded in audit trail with rationale |
| **Audit Trail Review** | Query agent activity log > Filter by time/agent/task > Review before/after diffs | Event history loads with cursor pagination; each event shows actor, action, timestamp, and RFC 6902 diff |

#### 16.2.2 AI Agent Flows (Primary UX Surface)

AI agents interact with the task management system through ~5 Domain Facade tools. The "UX" for agents is the API response design -- token efficiency, progressive detail, actionable errors, and predictable response structure.

| Flow | Tool Sequence | Token Budget | Success Criteria |
|------|---------------|-------------|------------------|
| **Orient to Project** | `query_tasks(detail="dashboard")` | ~120-180 tokens | Agent receives aggregate status counts by phase/area in a single call |
| **Find Next Task** | `query_tasks(detail="list", status="to_do", area=<agent_specialty>)` | ~40-55 tokens/task | Agent identifies highest-priority unblocked task in its specialty area |
| **Execute Task** | `query_tasks(detail="detail", task_id=X)` > work > `mutate_tasks(cmd="update_status")` > `mutate_tasks(cmd="check_item")` | ~500-2000 tokens read + ~100 tokens/mutation | Task status transitions validated; checklist items marked; audit events recorded |
| **Handle Blocker** | Receive `DEPENDENCY_NOT_MET` error > `query_tasks(detail="detail", task_id=<blocking_task>)` > complete prerequisite or escalate | Error response includes blocking task ID and suggested action | Agent self-corrects without human intervention using actionable error codes |
| **Bulk Phase Completion** | `bulk_operations(cmd="batch_update_status", scope={phase: 3, status: "done"})` | ~100-200 tokens response | 45+ tasks updated in one call with partial-success semantics; side effects reported |
| **Cross-Project Learning** | `search_task_memory(query="camera configuration for FPS genre")` | ~150-300 tokens for top-5 results | Semantic search returns relevant completed tasks from past projects with similarity scores |

**AI Agent UX Zoom Levels:**

| Level | Name | Token Cost | Use Case |
|-------|------|-----------|----------|
| L0 | Dashboard | ~120-180 tokens total | Project orientation -- "How is the project doing?" |
| L1 | List | ~40-55 tokens per task | Task discovery -- "Which tasks need attention?" |
| L2 | Detail | ~500-2000 tokens per task | Task execution -- "What exactly do I need to do?" |
| L3 | Full | ~2000-10000 tokens per task | Export/audit only -- complete task with all checklist text and full event log |

### 16.3 Accessibility Requirements

> **N/A for feature PRD.** Accessibility requirements (WCAG compliance, keyboard navigation, screen reader support, color contrast) are platform-level concerns documented in the Platform PRD. Task management API responses are machine-consumed (AI agents) and do not have direct accessibility considerations. The human dashboard surfaces that display task data inherit platform accessibility standards.

### 16.4 Localization Requirements

> **N/A for feature PRD.** Localization is a platform-level concern documented in the Platform PRD. Task management data (status labels, GDLC phase names, error codes) is English-only for machine consistency. Human-facing labels are localized at the frontend rendering layer, not in the task management data model.

---

## 17. Legal & Compliance Requirements

> **Note:** Platform-level compliance (SOC 2, GDPR, CCPA, EU AI Act, pricing, GTM) is documented in the Platform PRD. This section covers only task-management-specific data handling requirements.

### 17.1 Task-Specific Data Handling

| Data Type | Collection Purpose | Retention | User Rights |
|-----------|-------------------|-----------|-------------|
| **Task content** (titles, descriptions, checklist text) | Core service delivery -- task management for game development projects | Hot: 0-90 days (full access). Warm: 90-365 days (reduced indexes). Cold: 1-3 years (S3/GCS archive). 3+ years: delete unless compliance requires. | Access, correction, deletion, portability. Deletion cascades to embeddings in Pinecone. |
| **Agent session logs** (audit events with before/after diffs) | Accountability, debugging, compliance, agent improvement | Same tiered retention as task content. Monthly partitioned via pg_partman. | Access, portability. Deletion only after retention minimum (may conflict with compliance audit needs). |
| **Semantic embeddings** (Pinecone vectors from completed tasks) | Cross-project institutional memory, knowledge transfer | Retained while source task exists. Deleted when source task deleted (DSAR compliance). Re-embedded on model change. | Deletion via source task deletion. Access via `search_task_memory` results. |
| **Wizard configuration data** (genre, camera, movement selections) | Game configuration, template instantiation, genre-conditional task generation | Retained for project lifetime. Archived with project. | Access, correction, deletion, portability. |
| **User account data** (email, name, organization, subscription) | Authentication, authorization, billing | Active account: indefinite. Closed account: 90 days then delete (unless legal hold). | Access, correction, deletion (account closure), portability. |
| **LLM conversation history** (user prompts, agent responses) | Context maintenance, conversation continuity, project memory | Per-session: retained for session duration. Cross-session: vectorized to Pinecone for semantic search. Raw logs: 90-day retention. | Access, deletion. User prompts may contain personal data (EDPB guidance) -- treat with full GDPR protection. |
| **Usage metrics** (API calls, token consumption, streaming hours) | Billing, capacity planning, cost optimization | 7 years (financial records retention). Aggregated/anonymized after 1 year. | Access. Aggregated data not subject to deletion requests. |

**Task-specific compliance notes:**
- Organization-based RLS ensures tenant data isolation at the database level (relevant to SOC 2, GDPR data segregation)
- Audit event retention must comply with platform-level retention policies
- Semantic embeddings in Pinecone must be deleted when source task is deleted (GDPR right to deletion)
- AI agent audit trail provides the transparency record required by EU AI Act Art. 50

---

## 18. Business Requirements

> **N/A for feature PRD.** Monetization strategy, pricing tiers, go-to-market, and support requirements are platform-level concerns documented in the Platform PRD. The task management system is required platform infrastructure — it does not have independent pricing or a separate go-to-market strategy.

**Feature-specific cost note:** Task management operations consume LLM tokens (via Domain Facade tool calls), audit event storage (PostgreSQL), and semantic memory storage (Pinecone embeddings). These costs are tracked per-organization and contribute to platform-level usage-based billing.

---

## 19. Success Metrics & Measurement

### 19.1 Product Metrics

| Metric | Definition | Target | Measurement Method | Measurement Frequency |
|--------|------------|--------|-------------------|----------------------|
| Agent Task Completion Rate | Percentage of tasks created and completed by AI agents without human intervention | > 90% | Query `audit_events` for `task.created` -> `task.status_changed(done)` where `actor_type = agent`, divided by total agent-created tasks. Dashboard: Grafana panel on `project_health_summary` projection | Weekly |
| Template Instantiation Success Rate | Percentage of `create_task_tree` bulk operations that complete without error | > 99% | Prometheus counter `task_bulk_create_total{status="success"}` / `task_bulk_create_total`. Alert on < 95% over 1-hour window | Daily |
| Gate Pass Rate (First Attempt) | Percentage of GDLC phase gates passed on first `check_gate_readiness` call without requiring additional task completion | > 60% | Query `audit_events` for `gate.decision` events. First attempt = no prior `gate.decision` with outcome `no_go` for same phase/project | Per phase gate (monthly aggregate) |
| Checklist Completion Velocity | Average time from task `doing` to all checklist items `is_checked = true` | Baseline + 20% improvement after 3 months | Compute delta between `task.status_changed(doing)` timestamp and last `item.checked` timestamp per task from `audit_events` | Weekly |
| Zoom Level Distribution | Percentage of agent queries at each zoom level (0-3) | > 50% at Level 0-1 (efficient usage); < 10% at Level 3 | Prometheus histogram `task_query_detail_level{level}`. High Level 3 usage indicates agents are over-fetching | Weekly |
| Dependency Resolution Automation | Percentage of blocked tasks auto-unblocked by `resolve_dependencies` vs. manually unblocked | > 80% automated | Compare `dependency.resolved` events with `actor_type = agent` vs `actor_type = human` in `audit_events` | Monthly |
| Semantic Search Relevance | User satisfaction with `search_task_memory` results (top-5 relevance) | > 70% of results rated relevant | Implicit: track whether agents act on search results (subsequent `mutate_tasks` call referencing returned task_id within 60s). Explicit: periodic human evaluation of sample queries | Monthly (Phase 4+) |

### 19.2 Business Metrics

| Metric | Definition | Target | Measurement Method | Measurement Frequency |
|--------|------------|--------|-------------------|----------------------|
| Time to First Task Tree | Elapsed time from new project creation to first `create_task_tree` completion | < 30 seconds (system); < 5 minutes (user journey from wizard to populated project) | Timestamp delta between `project.created` event and first `bulk.tree_created` event for same `project_id` in `audit_events` | Weekly |
| Task Management Feature Adoption | Percentage of active projects using task management (at least 1 task created) vs. total active projects | > 50% within 3 months of launch; > 80% within 6 months | Count distinct `project_id` in `task_instances` with `created_date` in period / total active projects from `project_manager` service | Monthly |
| Enterprise Pipeline Conversion | Percentage of Enterprise tier prospects that cite task management / audit trail as a decision factor | > 30% of Enterprise conversions | CRM tagging during sales process. Track mentions of "audit trail," "compliance," "task management" in sales call notes | Quarterly |
| Agent Efficiency Gain | Reduction in average agent tool calls per user request after task system deployment | > 25% reduction in tool calls for project management intents | Compare average `tool_call_count` per agent session for project-management-classified intents (baseline: pre-task-system, current: post-deployment). Source: agent session metadata in `AgentState` logs | Monthly |
| Support Ticket Reduction | Decrease in support tickets related to "lost work," "forgotten tasks," or "what changed" after audit trail deployment | > 40% reduction vs. baseline | Categorize support tickets by topic. Baseline: 3 months pre-launch. Compare: 3 months post-Phase 3 (audit trail live) | Quarterly |
| GDLC Workflow Completion Rate | Percentage of projects that progress through at least 3 of 7 GDLC phases (indicating sustained engagement) | > 40% of projects with task trees | Count projects with `gate.decision` events for 3+ distinct phases / total projects with `bulk.tree_created` events | Quarterly |

### 19.3 Technical Metrics

| Metric | Definition | Target | Measurement Method | Alerting Threshold |
|--------|------------|--------|-------------------|-------------------|
| API Response Latency (p95) | 95th percentile response time for task API endpoints | < 200ms (CRUD), < 50ms (dashboard), < 100ms (list) | Prometheus histogram `task_api_duration_seconds{endpoint, method}`. Grafana dashboard with p50/p95/p99 panels per endpoint | ALERT: p95 > 300ms for 5 minutes |
| Bulk Tree Creation Latency | Time to complete `create_task_tree` for ~500 tasks | < 5 seconds | Prometheus histogram `task_bulk_create_duration_seconds`. Measure from request receipt to transaction commit | ALERT: p95 > 10 seconds |
| Audit Event Write Throughput | Sustained events written per second to `audit_events` table | > 1,000 events/sec burst; > 500 events/sec sustained | Prometheus counter `audit_events_written_total` with rate() function. PostgreSQL: `pg_stat_user_tables.n_tup_ins` for `audit_events` | ALERT: sustained rate < 100 events/sec (indicates write bottleneck) |
| RLS Query Overhead | Additional latency introduced by Row-Level Security policies | < 5ms overhead vs. non-RLS baseline | Benchmark: run identical queries with RLS enabled vs. disabled on test dataset. Periodic automated benchmark in CI | ALERT: overhead > 20ms (indicates policy or index issue) |
| Cursor Pagination Stability | Zero duplicate or missing items across paginated result sets under concurrent writes | 0 duplicates, 0 gaps | Integration test: concurrent write workload + paginating reader. Compare UNION of all pages to direct `SELECT *` result. Run nightly in CI | ALERT: any test failure (zero tolerance) |
| Projection Lag | Time between entity mutation and projection table update | < 5 seconds (p95); < 1 second (p50) | Prometheus gauge `projection_lag_seconds`. Computed: `NOW() - MAX(last_projected_at)` per projection table. LISTEN/NOTIFY latency tracked separately | ALERT: lag > 30 seconds |
| Vectorization Pipeline Backlog | Number of completed tasks pending vectorization | < 50 items in backlog | Count `task_instances WHERE status = 'done' AND vectorized = false`. Prometheus gauge `vectorization_backlog_count` | ALERT: backlog > 200 for 15 minutes (Phase 4+) |
| Database Connection Pool Utilization | Percentage of SQLAlchemy pool connections in use | < 80% sustained | Prometheus gauge from SQLAlchemy pool events: `pool_checkedout / (pool_size + max_overflow)`. Cross-reference with `pg_stat_activity` connection count | ALERT: > 90% for 5 minutes |
| Partition Health | Number of audit_events partitions, size per partition, partition creation schedule adherence | Monthly partitions created 3 months ahead; individual partition < 10GB | pg_partman monitoring: `SELECT * FROM partman.show_partitions()`. Partition size via `pg_total_relation_size()` | ALERT: next month's partition does not exist; any partition > 15GB |

---

## 20. Risk Analysis

### Risk Scoring Key

| Score | Probability | Impact |
|-------|-------------|--------|
| 1 | Unlikely (< 15%) | Minor -- workaround exists, < 1 week delay |
| 2 | Possible (15-40%) | Moderate -- requires component redesign, 1-2 week delay |
| 3 | Likely (40-70%) | Significant -- blocks a phase, 2-4 week delay |
| 4 | Very Likely (> 70%) | Critical -- threatens project viability or requires architectural pivot |

**Risk Score = Probability x Impact.** Scores 1-4: Low. Scores 5-8: Medium. Scores 9-12: High. Scores 13-16: Critical.

### 20.1 Technical Risks

| ID | Risk | Prob | Impact | Score | Mitigation | Contingency |
|----|------|:----:|:------:|:-----:|------------|-------------|
| TR1 | **Alembic migration chain drift** blocks new task model migrations. Existing chain does not match current ORM models (6+ models have columns with no migration). | 3 | 2 | **6 Med** | Create standalone migration using explicit `op.create_table()` calls that do NOT depend on `001_initial`. Validate migration on fresh DB before merging. | If chain is irrecoverable, create fresh migration from current model state with `--autogenerate` after manually verifying all tables. |
| TR2 | **Concurrent multi-agent writes** cause data corruption or deadlocks. 8+ agents writing to same project simultaneously. | 2 | 3 | **6 Med** | Per-operation conflict policies: independent item rows (no conflict), optimistic locking via `stream_version` for field updates, advisory locks for bulk ops. `CONCURRENT_MODIFICATION` error code with retry guidance. | Serialize agent writes per project via Redis-based lock. Performance degrades but correctness preserved. |
| TR3 | **RLS `SET LOCAL` incompatible with SQLAlchemy async session pooling.** `SET LOCAL` is transaction-scoped; session pool may share connections across requests. | 2 | 3 | **6 Med** | Test with FastAPI middleware + `async_session` before committing to RLS approach during Phase 1 Week 1. Use `asyncpg` connection-level `SET` if `SET LOCAL` is insufficient. | Fall back to application-level tenant filtering (`WHERE organization_id = :org_id`) on all queries. Less secure but functional; RLS added later when compatibility confirmed. |
| TR4 | **Event sourcing Phase 3 takes longer than estimated** due to zero team experience with append-only tables, RFC 6902 diffs, and projection workers. | 3 | 2 | **6 Med** | Additive approach (not full CQRS) limits scope. Reference PostgreSQL event sourcing implementation patterns. Timeboxed spike (2 days) at Phase 3 start to validate approach. | Reduce Phase 3 scope: implement basic event logging first (no projections, no snapshots). Add advanced features in later iteration. Extends Phase 5 by 1 week. |
| TR5 | **LangChain/LangGraph version update breaks tool registration pattern.** Framework is actively evolving; breaking changes in tool APIs have occurred in prior releases. | 2 | 3 | **6 Med** | Pin framework versions in `requirements.txt`. Follow Pattern A (agent-internal `get_available_tools()` + `execute_tool()`) which is the proven stable pattern -- less coupled to framework decorators. | Adapt to new tool registration API. Pattern A's simplicity (dict descriptors + if/elif routing) is less likely to break than decorator-based patterns. Budget 3-5 days for adaptation. |
| TR6 | **Token budget estimates for zoom levels are inaccurate.** Estimates (~50 tokens/task at List level) are directional but unvalidated with real data. | 3 | 1 | **3 Low** | Build token counting utility into API response metadata during Phase 2. Validate estimates against actual serialized responses. | Adjust zoom level field sets dynamically. Add `max_tokens` response truncation with `continuation_cursor`. |
| TR7 | **Bulk `create_task_tree` exceeds 5-second target** for ~500 tasks in single transaction with hierarchy + dependencies + items. | 2 | 2 | **4 Low** | Batch INSERT via `executemany()`. Defer index creation until after bulk load. Transaction-level advisory lock to prevent concurrent tree creation. | Increase timeout to 15s. Split into 2 transactions (tasks first, then items/dependencies). Accept degraded UX for initial template instantiation only. |
| TR8 | **pg_partman unavailable in target cloud environment.** Cloud PostgreSQL providers may not support this extension. | 2 | 2 | **4 Low** | Check provider extension list during Phase 1 environment setup. Native declarative partitioning (`PARTITION BY RANGE`) is always available without extensions. | Manual partition management with cron-based script creating monthly partitions 3 months ahead. Functionally equivalent, operationally heavier. |

### 20.2 Business Risks

| ID | Risk | Prob | Impact | Score | Mitigation | Contingency |
|----|------|:----:|:------:|:-----:|------------|-------------|
| BR1 | **AI-operator assumption is wrong.** If human operators end up doing > 20% of task operations, the API design (zoom levels, bulk ops, cursor pagination) may be over-optimized for agents and under-optimized for humans. | 1 | 3 | **3 Low** | Human REST API (Phase 2) shares `TaskService` with agent tools -- both interfaces are built on the same service layer. Usage telemetry tracks `actor_type` distribution from day one. | Invest in frontend task panel earlier. Add human-friendly list views, drag-and-drop, keyboard shortcuts. Service layer refactoring NOT required (dual interface already designed). |
| BR2 | **GDLC framework undergoes structural change** (new phases, areas, or hierarchy reorganization) during implementation. | 1 | 3 | **3 Low** | Template seeder uses slug-based IDs and `ON CONFLICT` idempotency. Framework changes trigger re-seed, not schema migration. `max_depth` is configurable; `item_type` enum is extensible. | If structural change is fundamental (e.g., hierarchy depth semantics change), adapt `hierarchy_path` encoding. Non-breaking; adds 1-2 weeks. |
| BR3 | **Scale targets (10K concurrent users) are premature.** If actual usage is 100-1,000 users, Phase 1 scale infrastructure (RLS, partitioning readiness, connection pooling design) is over-engineering. | 2 | 1 | **2 Low** | RLS and `organization_id` are low-cost additions to initial schema (< 2 days overhead). Partition-ready composite PKs add zero runtime overhead. Actual partitioning activation is deferred. | Skip PgBouncer and read replicas. RLS stays (low overhead, high security value). Reclaim 1-2 weeks of Phase 5 work. |
| BR4 | **No free tier creates acquisition barrier.** Every major competitor (GitHub Copilot, Cursor, Replit) offers a free plan. GameFrame at $99/mo minimum may deter price-sensitive indie developers who are the largest customer segment. | 2 | 2 | **4 Low** | Validate pricing through early adopter program before public launch. Consider reverse trial (full access 14 days, then downgrade). Monitor signup-to-paid conversion rates. | Introduce $49/mo entry tier or limited free tier with capped projects/tasks. Org-based pricing means free tier costs are bounded per-organization, not per-seat. |

### 20.3 Compliance & Regulatory Risks

| ID | Risk | Prob | Impact | Score | Mitigation | Contingency |
|----|------|:----:|:------:|:-----:|------------|-------------|
| CR1 | **GDPR Article 22 challenge.** AI agents as primary operators (95%+) performing automated task management decisions could be classified as "solely automated decision-making" under GDPR Art. 22, triggering right-to-human-review obligations. | 2 | 3 | **6 Med** | Document that task management decisions do not produce "legal or similarly significant effects" on data subjects. Implement human-in-the-loop review options via LangGraph interrupt mechanism. Maintain human override capability for all agent operations. | If classification challenged: add mandatory human approval gate for task deletion, assignment changes, and gate decisions. Increases latency for these operations but preserves compliance. |
| CR2 | **EU AI Act Art. 50 transparency obligations (Aug 2026 deadline).** Must disclose to users when they are interacting with AI agents and label AI-generated content. Failure: up to EUR35M or 7% of global turnover. | 3 | 2 | **6 Med** | Build transparency into agent tool responses from Phase 2: every agent-created/modified task carries `created_by_agent: true` metadata. Audit trail provides full provenance. Add UI indicators for AI-generated content in frontend (deferred workstream). | If deadline approaches without full implementation: add banner-level disclosure ("Tasks in this project are managed by AI agents") as interim measure while per-item labeling is completed. |
| CR3 | **CCPA 2026 Automated Decision-Making Technology (ADMT) oversight rules.** New regulations effective Jan 2026 require assessment of AI systems making decisions about consumers. Directly applicable to AI agent task operations. | 2 | 2 | **4 Low** | Conduct ADMT assessment during Phase 3 (audit trail provides the evidence base). Document that task management AI does not make decisions about consumers' rights, benefits, or access to services. | If ADMT rules are interpreted broadly: implement opt-out mechanism allowing users to disable AI agent operations for their projects. Significant UX degradation but legally compliant. |
| CR4 | **SOC 2 Type II certification required for Enterprise tier sales.** Enterprise game studios require SOC 2 as procurement prerequisite. Certification requires 6-12 months of operating history after controls are implemented. | 3 | 2 | **6 Med** | Begin SOC 2 preparation during Phase 5 (controls already in place: RLS, audit trail, encryption, access control). Engage SOC 2 readiness assessor. Budget 12-18 months from launch to certification. | Delay Enterprise tier launch until SOC 2 Type II achieved. Offer Enterprise prospects a "compliance roadmap" document with target dates during interim period. |
| CR5 | **Data residency requirements block Enterprise deals.** 65% of CIOs have rejected SaaS vendors over data residency. Pinecone embeddings derived from user content may constitute personal data requiring EU residency. | 2 | 3 | **6 Med** | Design multi-region deployment architecture during Phase 5. Require data residency guarantees from Pinecone and LLM providers in DPAs. Contractual specificity: exact AWS region, not just "in Europe." | Defer EU market Enterprise sales until multi-region deployment is operational. Indie/Studio tiers can launch with US-only hosting (lower compliance surface). |

### 20.4 Operational Risks

| ID | Risk | Prob | Impact | Score | Mitigation | Contingency |
|----|------|:----:|:------:|:-----:|------------|-------------|
| OR1 | **Audit event volume exceeds storage projections.** AI agents generating 100+ events/min per project at peak. With 1,000 orgs x 100 active projects, estimated ~200M events/month. | 2 | 2 | **4 Low** | Monthly partitioning with 90-day hot retention. Cold archival to S3/GCS Parquet. `MAXLEN` on Redis Streams for real-time channel. Monitor partition sizes via Prometheus. | Reduce event granularity (aggregate bulk operations into single events). Increase archival frequency from monthly to weekly. Tighten hot retention to 30 days. |
| OR2 | **No existing monitoring for task-specific metrics.** Prometheus infrastructure exists but no task dashboards. Issues may go undetected until user reports. | 3 | 1 | **3 Low** | Phase 5 adds Prometheus counters and histograms for all task operations. Grafana dashboards for latency, throughput, error rates, and projection lag. | Basic `structlog` logging provides fallback observability until dashboards are built. Alertmanager rules for error rate spikes on task API routes. |
| OR3 | **Cross-instance WebSocket gap in production.** All connection state is in-memory per process. Horizontal scaling silently drops real-time broadcasts to clients on different instances. | 3 | 2 | **6 Med** | Real-time sync is deferred post-Phase 5. When implemented, Redis Streams bridges instances (not in-memory pub/sub). Document limitation in release notes. | Accept single-instance WebSocket for MVP. Scale WebSocket via sticky sessions as interim. Full Redis Streams implementation in dedicated post-MVP sprint. |
| OR4 | **Solo developer bottleneck.** All 5 phases depend on a single developer + AI agents. Illness, burnout, or context-switching delays compound across the critical path. | 3 | 2 | **6 Med** | Phase 3 and Phase 4 are parallelizable (independent tracks). AI agents handle significant implementation volume. Detailed task files (MDTM) preserve context for resumption after breaks. | Extend timeline to 15-18 weeks (relaxed pace). Hire contract developer for Phase 5 integration work. Prioritize Phases 1-2 (core value) and defer Phases 3-4 if needed. |

### 20.5 Risk Summary

| Category | Critical (13-16) | High (9-12) | Medium (5-8) | Low (1-4) |
|----------|:-----------------:|:-----------:|:------------:|:---------:|
| Technical | 0 | 0 | 5 (TR1-TR5) | 3 (TR6-TR8) |
| Business | 0 | 0 | 0 | 4 (BR1-BR4) |
| Compliance | 0 | 0 | 4 (CR1, CR2, CR4, CR5) | 1 (CR3) |
| Operational | 0 | 0 | 2 (OR3, OR4) | 2 (OR1, OR2) |
| **Total** | **0** | **0** | **11** | **10** |

**Risk profile:** No Critical or High risks. 11 Medium risks with well-defined mitigations and contingencies. The highest-probability risks (TR1 migration drift, TR4 event sourcing learning curve, CR2 EU AI Act deadline, OR4 solo developer bottleneck) are all manageable with the documented mitigations. No risks require changes to the Option C Hybrid architecture.

---

## 21. Implementation Plan

> This section consolidates the full delivery plan: what to build (epics, stories, requirements), how to phase it, what "done" means per phase, and when it lands. Read top to bottom for the complete implementation picture.

### 21.1 Epics, Features & Stories


> **Format:** Each epic contains user stories in the format: "As a [persona], I want [goal] so that [benefit]"
>
> **Personas referenced:** Solo Indie Dev (Alex), Small Studio Lead (Jordan), AI Agent Operator (primary), Enterprise Producer (Morgan), Educator (Dr. Reyes)

#### 21.1.1 Epic Summary

| Epic # | Epic Name | Features | Stories | Priority | Phase |
|--------|-----------|----------|---------|----------|-------|
| 1 | Core Task Management | 7 | 5 | P0 | Phase 1 |
| 2 | GDLC Integration | 4 | 4 | P0 | Phase 1 |
| 3 | AI Agent Interface | 6 | 5 | P0 | Phase 2 |
| 4 | Event Sourcing & Audit Trail | 4 | 4 | P1 | Phase 3 |
| 5 | Semantic Memory | 2 | 3 | P1 | Phase 4 |
| 6 | Scale & Multi-Tenancy | 3 | 3 | P0 | Phase 1 |

---

#### Epic 1: Core Task Management

**Description:** Foundational task data model including hierarchical task tree, MDTM-compatible fields, state machine, checklist items, dependencies, and template system. This epic provides the database layer that all other epics build upon.

**US-1.1: Create Hierarchical Task Tree**
- **As a** AI Agent Operator
- **I want** to create a hierarchical task tree with variable depth (up to 6 levels) using parent-child relationships and a `hierarchy_path` for efficient subtree queries
- **So that** I can organize game development work from project-level epics down to individual checklist items, navigating the full hierarchy with prefix-match queries in <100ms for 500 nodes.

**Acceptance Criteria:**
- AC1: Tasks support self-referential `parent_task_id` FK with `depth` integer column (0 = root)
- AC2: `hierarchy_path` TEXT column enables subtree queries via `WHERE hierarchy_path LIKE 'path.%'` with B-tree index
- AC3: Configurable `max_depth` (default 6) enforced on task creation -- rejection with actionable error if exceeded
- AC4: `item_type` enum provides flexible depth labels (not fixed Agile terminology)
- AC5: Subtree rollup queries complete in <100ms for a project with 500 task nodes

**Success Metrics:**
- Subtree query p95 latency: <100ms for 500 nodes
- Hierarchy creation success rate: >99.9%

---

**US-1.2: Enforce Task Status State Machine**
- **As a** AI Agent Operator
- **I want** task status transitions enforced by a 5-state machine (To Do, Doing, Done, Blocked, Cancelled) with automatic side-effect field updates, terminal states, and permission-gated cancellation
- **So that** agents can rely on "done means done" and "cancelled means cancelled" invariants for planning, dependency resolution, and gate readiness — and invalid transitions are rejected with actionable error codes including valid alternatives and suggested actions.

**State Transition Matrix (5x5 — product decisions):**

| FROM \ TO | To Do | Doing | Done | Blocked | Cancelled |
|-----------|:-----:|:-----:|:----:|:-------:|:---------:|
| **To Do** | F | A | F | C | C |
| **Doing** | F | F | C | C | C |
| **Done** | F | F | F | F | F |
| **Blocked** | C | C | F | F | C |
| **Cancelled** | F | F | F | F | I |

A=Allowed, C=Conditional, F=Forbidden, I=Idempotent no-op. 9 allowed transitions, 11 forbidden, 1 idempotent.

**Key product decisions:**
- **Done is terminal.** No outbound transitions. Completed work is historical fact. Rework is handled by creating a new task with `metadata.recreated_from` link — not by reopening. (Admin-only `reopen_task` action may be specified as a future extension.)
- **Cancelled is terminal.** No outbound transitions (except idempotent Cancelled->Cancelled for retry safety). Revival is handled by creating a new task with `metadata.recreated_from` link.
- **Cancellation is permission-gated.** Only orchestrator agent and human operators with `task:cancel` permission can cancel tasks. Specialist agents cannot cancel — prevents rogue local-optimization cancellations.
- **Blocked exit routing is deterministic.** Blocked->To Do (if `start_date` is null, task was never started) or Blocked->Doing (if `start_date` is not null, task was previously in progress). Data-driven guard, not caller choice.
- **Cancelled tasks excluded from active counts.** Dashboard, list queries (by default), gate readiness denominator, and MDTM export all exclude cancelled tasks. Direct-by-ID queries and audit trail include them.

**Acceptance Criteria:**
- AC1: 5x5 state transition matrix enforced per the matrix above — 9 allowed (2 unconditional, 7 conditional), 11 forbidden, 1 idempotent no-op. Done and Cancelled are terminal with zero outbound transitions.
- AC2: `cancelled` state with defined lifecycle: entry from To Do, Doing, Blocked (requires `cancellation_reason` min 10 chars + `task:cancel` permission); terminal exit; visibility rules (excluded from dashboard active counts, default list queries, gate readiness, MDTM export; included in direct-by-ID queries and audit trail). MDTM files remain 4-state.
- AC3: Side effects auto-applied for all 9 allowed transitions. Key: To Do->Doing sets `start_date`; Doing->Done sets `completion_date`; entry to Blocked requires `blocker_reason` (min 3 chars); exit from Blocked clears `blocker_reason`; entry to Cancelled sets `cancellation_reason`, `cancelled_at`, `cancelled_by`. All side effects atomic within same DB transaction. `updated_date` and `stream_version` updated on every transition.
- AC4: Forbidden transitions return HTTP 409 `INVALID_STATUS_TRANSITION` with `valid_transitions` array, `reason` string, and `suggested_action` string. Guard failures return HTTP 400 `VALIDATION_ERROR` or HTTP 403 `PERMISSION_DENIED`.
- AC5: Doing->Done requires all checklist items in terminal state (`success`, `blocker_logged`, or `skipped`). Additionally requires all blocking dependencies resolved.
- AC6: `updated_date` set after every state transition and every field update.
- AC7: `stream_version` initialized to 1 on creation, incremented by 1 on every mutation. Required on all status transition and field update requests for optimistic concurrency. Omission returns `VALIDATION_ERROR`.
- AC8: Cancellation requires `task:cancel` permission + `cancellation_reason` (10-500 chars). New columns: `cancellation_reason` (TEXT), `cancelled_at` (TIMESTAMPTZ), `cancelled_by` (VARCHAR).
- AC9: Blocked exit routing: Blocked->To Do requires `start_date IS NULL`; Blocked->Doing requires `start_date IS NOT NULL`. Incorrect routing returns HTTP 409 with correct target in `valid_transitions`.
- AC10: Database CHECK constraints enforce state-field invariants (blocked requires blocker_reason, cancelled requires all 3 cancellation fields, done requires completion_date, doing requires start_date, stream_version >= 1).

**Success Metrics:**
- Invalid transition rejection rate: 100% (no invalid states reachable)
- Auto-field accuracy: 100% of side-effect fields correctly set on transition
- Exhaustive test coverage: all 25 state pairs tested (21 transitions + 4 identity rejections)

> **TDD Note:** Full side-effect field table, error response JSON payloads, SQL CHECK constraints, implementation pattern, and boundary condition specifications are in the Crit1 remediation file at `.dev/releases/backlog/task-management-v1/Crit1-FINAL-REMEDIATION.md` — these feed directly into the TDD.

---

**US-1.3: Track Checklist Items as Independent Rows**
- **As a** AI Agent Operator
- **I want** each checklist item stored as an independent database row with `is_checked`, `checked_at`, `checked_by`, `blocker_reason`, and `completion_type` fields
- **So that** I can query, filter, and batch-update individual items without parsing markdown, and distinguish success-completed items from blocker-logged items.

**Acceptance Criteria:**
- AC1: `task_instance_items` table with FK to `task_instances`, `is_checked` boolean, `checked_at` timestamp, `checked_by` string
- AC2: `completion_type` enum: success, blocker_logged, skipped
- AC3: `fillfactor=70` for HOT-eligible single-row checkbox updates (bypasses index maintenance)
- AC4: Item-level status extension: pending, in_progress, done, blocked, skipped
- AC5: Dynamic tasks (`task_type: dynamic`) allow runtime item insertion; static tasks reject insertion attempts
- AC6: Progress computation (checked/total) available as computed field

**Success Metrics:**
- Single checkbox update latency: <10ms (HOT-eligible)
- Progress computation accuracy: 100%

---

**US-1.4: Manage Inter-Task Dependencies**
- **As a** Small Studio Lead (Jordan)
- **I want** to define dependencies between tasks (blocks, parent_child, phase_gate types) with automatic successor unblocking when predecessors complete
- **So that** my team's work proceeds in the correct order and blocked tasks automatically become available when their dependencies are satisfied.

**Acceptance Criteria:**
- AC1: `task_dependencies` table with `dependent_task_id`, `required_task_id`, `dependency_type` enum
- AC2: Composite unique constraint prevents duplicate dependencies
- AC3: DAG validation prevents circular dependencies
- AC4: When predecessor completes, successors auto-transition from "blocked" to "to_do" (configurable via `auto_unblock`)
- AC5: `resolve_dependencies` bulk operation cascades unblocking across dependency chains

**Success Metrics:**
- Auto-unblock latency: <500ms after predecessor completion
- Circular dependency detection: 100%

---

**US-1.5: Instantiate Projects from GDLC Templates**
- **As a** Solo Indie Dev (Alex)
- **I want** to create a complete project task tree (~500 tasks with hierarchy, dependencies, and checklist items) from GDLC templates in a single operation
- **So that** I start every project with a structured game development lifecycle scaffold without manually creating hundreds of tasks.

**Acceptance Criteria:**
- AC1: `task_templates` table with SemVer versioning, `content_snapshot` JSONB, and `template_group_id`
- AC2: `task_template_items` table for individual checklist items within templates
- AC3: Copy-on-create: template fully duplicated at instantiation; instances are independent
- AC4: Genre-conditional items (291 of ~791) included/excluded based on wizard output
- AC5: Date remapping via relative offsets computed to absolute dates at instantiation
- AC6: `create_task_tree` operation creates ~500 instances in a single transaction in <5 seconds
- AC7: Template seeder with stable slug-based IDs and `ON CONFLICT` idempotency

**Success Metrics:**
- Template instantiation time: <5 seconds for ~500 tasks
- Genre-conditional accuracy: 100% correct inclusion/exclusion based on wizard output

---

#### Epic 2: GDLC Integration

**Description:** Deep integration of the task management system with the 7-phase, 9-area Game Development Lifecycle framework. Maps tasks to GDLC taxonomy, implements gate decision workflows, and ensures the Phase Focus Matrix drives task organization.

**US-2.1: Map Tasks to GDLC Phases and Areas**
- **As a** Small Studio Lead (Jordan)
- **I want** every task to carry `gdlc_phase` (Integer, 1-7) and `area_id` (String, 9 stable IDs: vf, cs, pe, mls, ms, nar, art, le, aud) columns
- **So that** I can filter and aggregate tasks by phase and area to understand progress across all 63 cells of the Phase Focus Matrix.

**Acceptance Criteria:**
- AC1: `gdlc_phase` Integer column (1-7) on `task_instances`
- AC2: `area_id` String(10) column using 9 stable AreaIds from `frontend/app/roadmap/types/gdlc.ts`
- AC3: Phase/area compound filters on all list endpoints (`?phase=2&area=cs,pe`)
- AC4: Dashboard (L0 zoom) aggregates by phase and area
- AC5: Template seeder seeds from code values (`gdlc.ts`), not documentation (which has 16+ discrepancies)

**Success Metrics:**
- Filter query p95 latency: <100ms for compound phase+area filters
- Phase/area coverage: 100% of seeded templates carry valid phase and area values

---

**US-2.2: Evaluate GDLC Gate Readiness**
- **As a** AI Agent Operator
- **I want** a `check_gate_readiness` operation that aggregates gate checklist completion across a full phase subtree and returns blocking items inline
- **So that** I can determine whether a GDLC phase gate can be passed and identify exactly which items remain incomplete, in a single tool call (~300-500 tokens).

**Acceptance Criteria:**
- AC1: `check_gate_readiness` accepts `project_id` and `phase` parameters
- AC2: Aggregates completion status across all gate checklist items for the specified phase
- AC3: Returns readiness outcome: Go (100% complete), No-Go (<80% complete), Conditional Pass (>=80% with documented exceptions), Not Evaluable (0 gate items in phase — phase has no tasks yet). Threshold is configurable per-phase with default 80%.
- AC3.1: Cancelled tasks excluded from gate readiness numerator AND denominator — if 100 tasks exist and 10 are cancelled, readiness is computed over 90.
- AC4: Blocking items returned inline with item text and assigned_to -- not just counts
- AC5: Response fits within ~300-500 tokens

**Success Metrics:**
- Gate readiness query latency: <200ms
- Blocking item completeness: 100% of incomplete items listed in response

---

**US-2.3: Record Gate Decisions**
- **As a** Enterprise Producer (Morgan)
- **I want** every GDLC gate decision (Go, No-Go, Conditional Pass) recorded as an immutable audit event with decision rationale
- **So that** I have a compliance-ready record of every phase transition decision, including who approved it and what conditions were attached.

**Acceptance Criteria:**
- AC1: `gate.decision` event type in audit_events table
- AC2: Event captures: phase, decision (Go/No-Go/Conditional Pass), rationale text, deciding actor (human or agent), conditions (if Conditional Pass)
- AC3: Gate decisions are immutable -- cannot be modified after recording
- AC4: Queryable by phase and project via `query_audit_trail` tool

**Success Metrics:**
- Gate decision recording: 100% of gate transitions produce audit events
- Decision traceability: every gate event links to the specific checklist items that were evaluated

---

**US-2.4: Handle Phase 7 Live Ops Continuous Review**
- **As a** AI Agent Operator
- **I want** Phase 7 (Live Ops) to use a continuous Health Check model (Green/Yellow/Red) instead of a one-time gate decision
- **So that** ongoing live operations are monitored with a recurring health assessment rather than a binary pass/fail.

**Acceptance Criteria:**
- AC1: Phase 7 supports Health Check status enum: Green, Yellow, Red
- AC2: Health Check can be re-evaluated at any time (not a one-shot gate)
- AC3: Template seeder handles missing Phase 7 work order gracefully (placeholder items)
- AC4: Health Check history stored in audit events for trend analysis

**Success Metrics:**
- Phase 7 Health Check recording: all evaluations persisted
- Graceful handling: system does not error when Phase 7 work order is empty

---

#### Epic 3: AI Agent Interface

**Description:** The primary consumer interface for the task management system. Consolidates ~60 granular operations into ~5 Domain Facade tools with zoom-level responses, bulk operations, cursor pagination, and actionable error handling -- all optimized for LLM token efficiency.

**US-3.1: Query Tasks with Zoom-Level Response Control**
- **As a** AI Agent Operator
- **I want** a `query_tasks` tool that accepts a `detail` parameter (dashboard, list, detail, full) controlling response density from ~120 tokens (project overview) to ~10K tokens (full export)
- **So that** I can navigate from project overview to specific task detail with predictable token cost at each step, never wasting context window on irrelevant data.

**Acceptance Criteria:**
- AC1: `detail` parameter accepts: dashboard, list, detail, full
- AC2: L0 Dashboard: aggregate counts by status/phase, ~120-180 tokens total, no individual tasks
- AC3: L1 List: id, title, status, priority, phase, area, assigned_to, progress, due_date, blocked flag (~40-55 tokens/task)
- AC4: L2 Detail: all frontmatter + checklist summary + next unchecked item + recent log (~500-2000 tokens/task)
- AC5: L3 Full: everything including all checklist items, full log, review info (~2000-10000 tokens/task)
- AC6: `fields` parameter overrides zoom presets when both specified
- AC7: `max_tokens` parameter (default 2000) with truncation and `continuation_cursor`

**Success Metrics:**
- Token budget accuracy: actual response within 20% of documented budget per zoom level
- Dashboard query latency: <50ms (from materialized view)
- List query latency: <100ms

---

**US-3.2: Execute Bulk Task Operations**
- **As a** AI Agent Operator
- **I want** five bulk operations (`create_task_tree`, `batch_update_status`, `batch_check_items`, `resolve_dependencies`, `check_gate_readiness`) each executable in a single tool call with partial-success semantics
- **So that** I can initialize a project (~500 tasks), complete a phase (45+ tasks), or resolve dependency chains without the ~100K-150K token overhead of individual calls.

**Acceptance Criteria:**
- AC1: `create_task_tree` instantiates ~500 tasks from template in single transaction, returns counts only (~150 tokens)
- AC2: `batch_update_status` accepts ID lists or scope-based filters, reports side effects (unblocked tasks, gate changes), ~100-200 tokens
- AC3: `batch_check_items` marks multiple checklist items complete, returns progress + next unchecked, ~100 tokens
- AC4: `resolve_dependencies` auto-unblocks successors, reports still-blocked with remaining deps, ~150-300 tokens
- AC5: `check_gate_readiness` evaluates gate across phase subtree, returns blocking items inline, ~300-500 tokens
- AC6: All bulk ops use partial-success semantics: valid operations commit, invalid return per-item errors
- AC7: Bulk operations create parent + child audit events linked via `parent_event_id`

**Success Metrics:**
- `create_task_tree` execution time: <5 seconds for ~500 tasks
- Batch status update: <200ms for 50 tasks
- Token savings vs. individual calls: >95% reduction for project initialization

---

**US-3.3: Page Through Large Result Sets with Cursor Pagination**
- **As a** AI Agent Operator
- **I want** cursor-based pagination via `(sort_col, id)` keyset encoding that is stable across concurrent inserts and deletes
- **So that** I can page through 500+ tasks without losing items to offset drift, with compound filters narrowing results precisely.

**Acceptance Criteria:**
- AC1: Cursor encodes `{"sort_key": <value>, "id": <uuid>}` as Base64
- AC2: Keyset pagination: `(sort_col, id) > (:cursor_sort_val, :cursor_id)` -- stable across concurrent mutations
- AC3: Parameters: `cursor` (null = first page), `limit` (1-500, default 25), `sort_by` (updated_date, created_date, priority, status, due_date, phase), `sort_order` (asc/desc)
- AC4: Response envelope: `{ items, pagination: { total_count, returned_count, has_more, next_cursor, prev_cursor }, filters_applied, sort }`
- AC5: 13 compound filter parameters (AND between types, OR within multi-value)
- AC6: Filters echoed back in every response
- AC7: `max_pages` safety limit (default 5) in LangGraph integration state

**Success Metrics:**
- Pagination stability: zero duplicates or gaps across 200 tasks with concurrent modifications
- Filter response accuracy: 100% of returned items match all applied filters

---

**US-3.4: Receive Actionable Error Responses**
- **As a** AI Agent Operator
- **I want** every error response to include a structured `error_code`, `error_message`, and `context` object with valid alternatives and suggested next action
- **So that** I can act on errors programmatically without additional tool calls or human intervention, enabling self-correcting behavior.

**Acceptance Criteria:**
- AC1: 8 enumerated error codes: INVALID_STATUS_TRANSITION, DEPENDENCY_NOT_MET, TASK_NOT_FOUND, PERMISSION_DENIED, GATE_NOT_READY, CONCURRENT_MODIFICATION, IDEMPOTENT_DUPLICATE, VALIDATION_ERROR
- AC2: Each error includes `context` with action-specific guidance (e.g., INVALID_STATUS_TRANSITION includes `valid_transitions` array)
- AC3: IDEMPOTENT_DUPLICATE returns original result (no action needed)
- AC4: CONCURRENT_MODIFICATION instructs re-read + retry with updated state
- AC5: No interactive confirmation flow -- agents decide or escalate via LangGraph interrupt

**Success Metrics:**
- Error actionability: 100% of error responses include programmatic next-action guidance
- Agent self-recovery rate: >80% of CONCURRENT_MODIFICATION errors resolved on first retry

---

**US-3.5: Access Task Operations Through Shared Service Layer**
- **As a** Small Studio Lead (Jordan)
- **I want** both the AI agent tools and human REST API endpoints to call the same `TaskService` class
- **So that** task operations are consistent regardless of whether an AI agent or a human performs them, and there is no divergence between interfaces.

**Acceptance Criteria:**
- AC1: Single `TaskService` class called by both agent tools and REST API routes
- AC2: Agent tools inject session context from `AgentState` (session_id, project_id, user_id)
- AC3: Human API routes use JWT via `Depends(get_current_user_id)`
- AC4: Rate limiting differs: per-agent-session (higher ceiling) vs per-user
- AC5: Every mutation accepts `agent_id` and `session_id` for audit tracing
- AC6: REST endpoints use standard HTTP verbs and response codes alongside agent tools

**Success Metrics:**
- Interface parity: 100% of operations available through both agent tools and REST API
- No data divergence: agent-created and human-created tasks indistinguishable in queries

---

#### Epic 4: Event Sourcing & Audit Trail

**Description:** Append-only audit event system that records every task mutation with before/after diffs, actor identification, and session traceability. Provides the accountability layer for AI-operated task management and enables compliance, debugging, and agent improvement.

**US-4.1: Record Every Task Mutation as an Audit Event**
- **As a** Enterprise Producer (Morgan)
- **I want** every task mutation (create, update, status change, checklist check, dependency change, gate decision) recorded as an immutable event with before/after state diffs
- **So that** I have a complete, tamper-proof record of every change for compliance, debugging, and knowledge transfer -- with zero manual documentation effort.

**Acceptance Criteria:**
- AC1: `audit_events` table in dedicated `audit` schema with BIGSERIAL id, transaction_id, entity_type, entity_id, agent_id, action, before_state/after_state/diff JSONB
- AC2: 14 event types: task.created, task.status_changed, task.field_updated, item.checked, item.blocked, item.added, dependency.added, dependency.resolved, gate.decision, assignment.changed, bulk.status_update, bulk.tree_created, bulk.items_checked, task.deleted
- AC3: Diffs use RFC 6902 JSON Patch format
- AC4: Metadata JSONB captures: session_id, correlation_id, causation_id, tool_name, idempotency_key, reasoning_summary
- AC5: Co-transactional: event recorded in same transaction as entity mutation
- AC6: Failed mutations do NOT create events

**Success Metrics:**
- Event coverage: 100% of mutations produce corresponding audit events
- Event write throughput: >1000 events/sec sustained
- Zero orphaned events: no events exist for mutations that were rolled back

---

**US-4.2: Handle Concurrent Agent Writes Safely**
- **As a** AI Agent Operator
- **I want** optimistic concurrency control via `stream_version` column with per-operation conflict resolution policies
- **So that** multiple specialist agents working on the same project simultaneously do not corrupt data or silently lose each other's changes.

**Acceptance Criteria:**
- AC1: `stream_version` column per entity, incremented on every mutation
- AC2: Concurrent writes detected via `WHERE stream_version = :expected` clause
- AC3: Per-operation policies: checklist items = no conflict (independent rows), status = last-write-wins (state machine validates), field updates = optimistic lock + retry once, bulk ops = advisory locks
- AC4: `CONCURRENT_MODIFICATION` error returned with re-read-and-retry instruction
- AC5: `idempotency_key` (unique, nullable) prevents duplicate operations on retry

**Success Metrics:**
- Data corruption incidents: zero
- Concurrent conflict resolution: >95% resolved without human intervention

---

**US-4.3: Manage Audit Event Retention**
- **As a** Enterprise Producer (Morgan)
- **I want** audit events partitioned monthly with configurable retention tiers (Hot 0-90d, Warm 90-365d, Cold 1-3y, Archive 3y+)
- **So that** recent events are fast to query, old events do not degrade performance, and storage costs are controlled while maintaining compliance-ready archives.

**Acceptance Criteria:**
- AC1: `audit_events` PARTITION BY RANGE (created_at) with monthly partitions via pg_partman
- AC2: `p_premake => 3` creates partitions 3 months ahead
- AC3: Hot retention (0-90 days): full retention, all indexes active
- AC4: Warm retention (90-365 days): retained in DB, reduced index coverage
- AC5: Cold retention (1-3 years): archived to S3/GCS Parquet
- AC6: Retention configurable per subscription tier (Enterprise gets longer hot retention)
- AC7: Old partitions detached and archived without affecting query performance on recent data

**Success Metrics:**
- Partition creation: automated, zero manual intervention
- Hot query performance: unaffected by cold data volume
- Archive reliability: 100% of cold partitions successfully archived

---

**US-4.4: Query Audit Trail for Agent Actions**
- **As a** Educator (Dr. Reyes)
- **I want** a `query_audit_trail` tool that lets me search event history by task_id, actor_id, event_type, and time range
- **So that** I can review student decision-making processes -- which design decisions they made, when, and why -- for grading based on process quality rather than just final output.

**Acceptance Criteria:**
- AC1: `query_audit_trail` tool with filters: task_id, actor_id, event_type, since, limit (default 20)
- AC2: Response includes: timestamp, event_type, actor, task_id, task_title, changes (before/after), reason
- AC3: Cursor-based pagination for long histories
- AC4: 6 query patterns supported via indexes: task history, agent activity, project timeline, event type, bulk operation trace, time range
- AC5: Bulk operation events traceable via `parent_event_id`

**Success Metrics:**
- Audit query latency: <200ms for recent 90-day window
- Query coverage: all 6 query patterns executable with acceptable performance

---

#### Epic 5: Semantic Memory

**Description:** Cross-project institutional memory via vectorization of completed tasks into Pinecone and semantic search capabilities for AI agents. Enables learning from past projects.

**US-5.1: Vectorize Completed Tasks Automatically**
- **As a** Enterprise Producer (Morgan)
- **I want** every task that transitions to "done" to be automatically vectorized and stored in Pinecone with rich metadata
- **So that** completed work becomes searchable institutional knowledge without any manual effort, building a cross-project knowledge base that grows with every completed task.

**Acceptance Criteria:**
- AC1: Triggered by `task.status_changed` event when status becomes "done"
- AC2: Async pipeline: publish to Redis Stream, background worker consumes and processes
- AC3: Embedding text constructed from 9 high-signal fields: title, description, tags, area+phase, type, blocker_reason, task summary, follow-up items, first 5 checklist item texts (truncated to 200 chars each)
- AC4: OpenAI `text-embedding-3-small` (1536 dimensions) with model name + version stored in metadata
- AC5: Pinecone namespace per organization (`org-{org_id}`) for tenant isolation
- AC6: `vectorized` boolean + `vector_id` + `vectorized_at` columns on `TaskInstance` with partial index
- AC7: Vectorization does not block status transition (<200ms regardless of embedding latency)
- AC8: Feature-flagged via `TASK_MEMORY_ENABLED`

**Success Metrics:**
- Vectorization latency: <30 seconds from task completion to searchable vector
- Vectorization success rate: >99.5%
- Zero impact on status transition latency

---

**US-5.2: Search Institutional Memory Across Projects**
- **As a** AI Agent Operator
- **I want** a `search_task_memory` tool that performs semantic search across completed tasks from all projects in my organization
- **So that** I can find relevant solutions, common blockers, and proven approaches from past projects to inform current work.

**Acceptance Criteria:**
- AC1: Input: natural language query, metadata filters (area, phase, genre, organization), top_k (default 5), include_task_detail flag
- AC2: Response: task_id, project_name, title, similarity_score, summary_excerpt, completion_date, area, phase (~150-300 tokens for 5 results)
- AC3: When `include_task_detail: true`, each result includes Level 2 detail (~500-2000 tokens per result)
- AC4: Pinecone query with combined semantic + metadata filters
- AC5: Organization-level isolation via Pinecone namespace

**Success Metrics:**
- Search relevance: top-5 results contain at least 1 relevant match for domain-specific queries
- Search latency: <500ms for semantic query + metadata filter

---

**US-5.3: Calibrate Estimates from Historical Data**
- **As a** Small Studio Lead (Jordan)
- **I want** to query past task completion data (duration, blockers, phase) for similar tasks across previous projects
- **So that** I can provide more accurate time estimates for new projects based on actual historical performance rather than guesswork.

**Acceptance Criteria:**
- AC1: Semantic search returns completion_date and start_date (enabling duration calculation)
- AC2: Blocker_reason field included in vectorized metadata for pattern analysis
- AC3: Phase and area filters allow scoping to specific GDLC context
- AC4: Batch re-vectorization script available for backfilling pre-existing completed tasks (idempotent, batch of 50)

**Success Metrics:**
- Historical query coverage: >90% of completed tasks vectorized and searchable
- Duration data availability: start_date and completion_date present in >95% of search results

---

#### Epic 6: Scale & Multi-Tenancy

**Description:** Organization-level tenant isolation, row-level security, and schema design for future partitioning and horizontal scaling. Built into Phase 1 from day one to avoid costly retrofitting.

**US-6.1: Enforce Organization-Level Data Isolation**
- **As a** Enterprise Producer (Morgan)
- **I want** every task table to have `organization_id UUID NOT NULL` with PostgreSQL Row-Level Security policies enforcing tenant isolation at the database level
- **So that** there is zero possibility of cross-tenant data leakage, even if application-level checks have bugs.

**Acceptance Criteria:**
- AC1: `organization_id UUID NOT NULL` FK on every task table (task_instances, task_instance_items, task_dependencies, task_templates, audit_events)
- AC2: `ENABLE ROW LEVEL SECURITY` + `org_isolation` policy on all task tables
- AC3: FastAPI middleware sets `SET LOCAL app.organization_id` per request, extracted from JWT
- AC4: `platform_admin` database role bypasses RLS for platform-level operations only
- AC5: RLS is defense-in-depth alongside application-level `WHERE organization_id = :org_id` checks

**Success Metrics:**
- Cross-tenant leakage: zero (verified by integration tests with multiple organizations)
- RLS overhead: <5ms per query

---

**US-6.2: Design Schema for Future Partitioning**
- **As a** AI Agent Operator
- **I want** composite primary keys (`(organization_id, id)`) and `fillfactor` tuning on hot tables from day one
- **So that** partitioning can be activated later without schema migration when tables exceed ~100GB.

**Acceptance Criteria:**
- AC1: Composite PK `(organization_id, id)` on `task_instances` for future hash partitioning readiness
- AC2: `fillfactor=70` on `task_instance_items` (frequent checkbox updates)
- AC3: Aggressive autovacuum (`scale_factor=0.001`) on frequently-updated tables
- AC4: Compound indexes: `(project_id, status, priority)` on tasks, `(task_instance_id, is_checked)` on items, `(hierarchy_path, status)` for rollups

**Success Metrics:**
- Schema migration for partitioning: zero required when activating partitioning
- Autovacuum efficiency: table bloat <20% under sustained update load

---

**US-6.3: Support Scaling Progression**
- **As a** Enterprise Producer (Morgan)
- **I want** the system to support a clear scaling progression (single PG -> PgBouncer + read replicas -> native partitioning -> distributed PG/Citus) without architectural changes at each step
- **So that** the platform grows from 100 to 100,000+ concurrent users without requiring a rewrite.

**Acceptance Criteria:**
- AC1: PgBouncer configuration ready: `NullPool` + `statement_cache_size=0` in SQLAlchemy config, feature-flagged via `PGBOUNCER_ENABLED`
- AC2: Read-only queries (list, dashboard, audit trail) separable to read replicas
- AC3: Volume targets documented: per project ~500 tasks, per org ~50K tasks, platform ~50M tasks
- AC4: Performance targets: API <200ms p95, dashboard <50ms, list <100ms, audit write >1000 events/sec

**Success Metrics:**
- Single-instance: supports 1000 concurrent users with target latencies
- Documented scaling path: each transition step validated in architecture docs

---


### 21.2 Product Requirements


#### 21.2.1 Core Features

#### Feature 1: Hierarchical Task Data Model

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Description** | Self-referential task tree with adjacency list, hierarchy path, MDTM-compatible 22-field schema, 4+1 state machine, relational checklist items, inter-task dependency DAG, and template/instance separation with SemVer versioning |
| **User Value** | Enables structured game development workflow with enforced state transitions, dependency ordering, and one-click project scaffolding from GDLC templates |
| **Dependencies** | PostgreSQL 15, Alembic migrations, Auth service (JWT), Project service |

**Acceptance Criteria:**
- All 22 MDTM frontmatter fields represented as database columns or JSONB
- State machine enforces valid transitions with actionable errors
- Checklist items as independent rows with HOT-eligible updates
- Dependency DAG with cycle detection and auto-unblocking
- Template instantiation creates ~500 tasks in <5 seconds

**Success Metrics:**
- Schema completeness: 22/22 MDTM fields represented
- State machine coverage: 100% invalid transitions rejected

---

#### Feature 2: Domain Facade Agent Tools

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Description** | ~5 consolidated agent tools (query_tasks, mutate_tasks, bulk_operations, search_task_memory stub, query_audit_trail stub) with zoom-level response control, bulk operations, cursor pagination, field projection, and actionable error codes |
| **User Value** | AI agents perform 95%+ of task operations with predictable token budgets, minimal tool calls, and self-correcting error handling |
| **Dependencies** | Feature 1 (Task Data Model), Agent system (base_agent.py), Session context |

**Acceptance Criteria:**
- Tool definitions total <2K tokens (83% reduction from ~12K for ~60 granular tools)
- 4 zoom levels with documented token budgets
- 5 bulk operations with partial-success semantics
- Cursor-based pagination stable across concurrent mutations
- 8 enumerated error codes with agent-action guidance

**Success Metrics:**
- Token efficiency: 85%+ reduction vs. granular tool pattern
- Agent task completion rate: >95% of operations succeed on first tool call

---

#### Feature 3: Append-Only Audit Event System

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Description** | Immutable event log recording every task mutation with RFC 6902 diffs, actor identification, session traceability, optimistic concurrency control, monthly partitioning, and configurable retention |
| **User Value** | Complete accountability for AI agent actions, compliance-ready gate decision records, debugging capability, and automatic documentation of every change |
| **Dependencies** | Feature 1 (Task Data Model), pg_partman extension |

**Acceptance Criteria:**
- 14 event types covering all task mutations
- Co-transactional: event + mutation in same transaction
- Optimistic concurrency via stream_version
- Monthly partitioned with automated retention management
- Queryable via agent tool with 6 index-backed query patterns

**Success Metrics:**
- Event write throughput: >1000 events/sec
- Audit completeness: 100% of mutations produce events

---

#### Feature 4: Semantic Task Memory

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Description** | Async vectorization pipeline for completed tasks into Pinecone with semantic search tool for cross-project institutional memory |
| **User Value** | Cross-project knowledge reuse: find past solutions, common blockers, and proven approaches. Estimation calibration from historical data |
| **Dependencies** | Feature 1 (Task Data Model), Feature 3 (Audit Events for trigger), Pinecone, OpenAI Embedding API |

**Acceptance Criteria:**
- Async vectorization on task completion (<30s to searchable)
- 9 high-signal fields embedded per task
- Organization-level namespace isolation in Pinecone
- Semantic search with metadata filters
- Feature-flagged for gradual rollout

**Success Metrics:**
- Vectorization coverage: >99.5% of completed tasks vectorized
- Search relevance: top-5 contains relevant match for domain queries

---

#### Feature 5: Multi-Tenant Row-Level Security

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Description** | Organization-level tenant isolation via `organization_id` FK + PostgreSQL RLS policies on all task tables, with FastAPI middleware for automatic context injection |
| **User Value** | Enterprise-grade data isolation with zero cross-tenant leakage, defense-in-depth at database level |
| **Dependencies** | PostgreSQL 15, Organization model (must be created), Auth service (JWT with org claim) |

**Acceptance Criteria:**
- `organization_id` on every task table from day one
- RLS policies active on all task tables
- Middleware automatically sets tenant context per request
- Platform admin role bypasses RLS for operational needs

**Success Metrics:**
- Cross-tenant leakage: zero
- RLS overhead: <5ms per query

---

#### Feature 6: GDLC Template Seeder

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Description** | Script that parses GDLC work orders (~98 items) and gate checklists (~608 items) from markdown docs into TaskTemplate + ChecklistItemTemplate records, with genre-conditional item tagging and stable slug-based IDs |
| **User Value** | Structured GDLC lifecycle available out-of-the-box for every new project, with genre-appropriate task filtering |
| **Dependencies** | Feature 1 (Task Data Model), GDLC docs/code (gdlc.ts authoritative) |

**Acceptance Criteria:**
- Parses all 7 phases (handles missing Phase 7 work order gracefully)
- Seeds from code values, not documentation (16+ discrepancies known)
- Stable slug-based IDs with `ON CONFLICT` idempotency
- Genre-conditional items tagged for inclusion/exclusion at instantiation
- Idempotent: re-running produces identical results

**Success Metrics:**
- Template item count: ~791 items seeded (500 base + 291 genre-conditional)
- Idempotency: re-seed produces zero new records or errors

---

#### Feature 7: Human REST API

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Description** | Standard REST endpoints for task CRUD, list, filter, and status operations, calling shared TaskService, with JWT auth and offset pagination for backward compatibility |
| **User Value** | Human users can view and manage tasks through web interface or API clients, with the same data consistency as AI agent operations |
| **Dependencies** | Feature 1 (Task Data Model), Feature 2 (Shared TaskService), Auth service |

**Acceptance Criteria:**
- Standard CRUD endpoints: POST/GET/PUT/DELETE for tasks
- List endpoint with compound filters (phase, area, status, priority, assignee)
- Offset pagination for backward compatibility with existing frontend patterns
- JWT authentication via existing `Depends(get_current_user_id)`
- Same TaskService as agent tools -- no separate implementation

**Success Metrics:**
- API response time: <200ms p95
- Endpoint coverage: all task operations accessible via REST

---

#### 21.2.2 Feature Prioritization Matrix (RICE)

> **RICE Formula:** (Reach x Impact x Confidence) / Effort
>
> **Reach:** Number of users/agents affected per quarter (scale: 100-10000)
> **Impact:** Effect on user goals (1 = minimal, 2 = moderate, 3 = massive)
> **Confidence:** Certainty in estimates (50% = low, 80% = medium, 100% = high)
> **Effort:** Person-weeks to implement

| Feature | Reach | Impact | Confidence | Effort (pw) | RICE Score | Priority |
|---------|-------|--------|------------|-------------|------------|----------|
| F1: Hierarchical Task Data Model | 10000 | 3 | 90% | 3 | 9000 | P0 |
| F2: Domain Facade Agent Tools | 10000 | 3 | 85% | 4 | 6375 | P0 |
| F5: Multi-Tenant RLS | 10000 | 3 | 95% | 1.5 | 19000 | P0 |
| F6: GDLC Template Seeder | 10000 | 2 | 90% | 2 | 9000 | P0 |
| F3: Audit Event System | 5000 | 2 | 80% | 3 | 2667 | P1 |
| F4: Semantic Task Memory | 2000 | 2 | 70% | 2 | 1400 | P1 |
| F7: Human REST API | 5000 | 2 | 90% | 2 | 4500 | P1 |

**RICE Score Interpretation:**
- **>5000:** P0 -- Must have for MVP. Build in Phase 1-2.
- **2000-5000:** P1 -- Should have. Build in Phase 2-3.
- **<2000:** P2 -- Could have. Defer to Phase 4+.

**Notes on scoring:**
- Reach for all features is high because AI agents (primary operators) interact with every feature. F3 and F7 score lower reach because they primarily serve human personas (subset of total users).
- F5 (Multi-Tenant RLS) has the highest RICE score because it has very high reach, massive impact (security), high confidence (well-understood pattern), and low effort (schema-level addition during Phase 1).
- F4 (Semantic Memory) has lowest confidence because it depends on Pinecone integration and embedding quality -- both untested with task data.

---


### 21.3 Implementation Phasing

> **Note:** All 5 phases are in scope for this PRD. Phases 3-4 are parallelizable after Phase 2 stabilizes.

| Phase | Timeline | Features |
|-------|----------|----------|
| Phase 1: Data Model | 2-3 weeks | Core task tree, GDLC taxonomy, dependencies, state machine, checklists, templates, audit_events, RLS, organization_id |
| Phase 2: AI Tool Layer | 3-4 weeks | Domain Facade (~5 tools), zoom levels, bulk operations, cursor pagination, human REST API |
| Phase 3: Event Sourcing | 2-3 weeks | Append-only event store, RFC 6902 diffs, CQRS read models, projection workers. Parallelizable with Phase 4. |
| Phase 4: Semantic Memory | 2 weeks | Pinecone vectorization pipeline, `search_task_memory` implementation, cross-project memory. Parallelizable with Phase 3. |
| Phase 5: Integration | 2-3 weeks | GDLC template seeder, agent tool registration, swarm keyword routing, Prometheus dashboards, end-to-end testing |

### 21.4 Release Criteria & Definition of Done


#### 21.4.1 Phase Release Criteria

#### Phase 1: Data Model Foundation (Weeks 1-3)

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | All 6-7 task tables created with correct column types, constraints, and FKs | Alembic migration runs cleanly on fresh database; `\d+ task_instances` output matches schema spec | Pending |
| **Functionality** | `hierarchy_path` subtree queries return correct results for 3-level test hierarchy | SQL test: `SELECT * FROM task_instances WHERE hierarchy_path LIKE 'test.%'` returns expected subtree | Pending |
| **Functionality** | Status state machine rejects invalid transitions with actionable error codes | Unit test: attempt all 20 possible transitions (4x5 matrix minus valid), verify `INVALID_STATUS_TRANSITION` with `valid_transitions` array | Pending |
| **Security** | RLS policies enforce tenant isolation -- queries with Org A context return zero Org B rows | Integration test: insert rows for 2 organizations, `SET LOCAL app.organization_id` to each, verify complete isolation | Pending |
| **Performance** | Compound indexes exist: `(project_id, status, priority)`, `(task_instance_id, is_checked)`, `(hierarchy_path, status)` | `\di+ task_*` output shows all expected indexes; EXPLAIN ANALYZE confirms index usage on representative queries | Pending |
| **Quality** | Migration is standalone (does not depend on `001_initial`) | Run migration on empty database with no prior migrations; verify success | Pending |
| **Documentation** | Model docstrings on all classes and columns | Code review: every `Column()` has a `doc=` or adjacent comment explaining purpose | Pending |

#### Phase 2: AI Tool Layer (Weeks 3-7)

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | `TaskService` supports full CRUD: create, read (4 zoom levels), update, delete, transition status | Integration tests: 1 test per CRUD operation x 4 zoom levels for read = minimum 8 tests, all passing | Pending |
| **Functionality** | All 5 Domain Facade tools operational: `query_tasks`, `mutate_tasks`, `bulk_operations`, `search_task_memory` (stub), `query_audit_trail` (stub) | Agent integration test: each tool callable from test agent session with valid `AgentState` context | Pending |
| **Functionality** | `create_task_tree` instantiates ~500 tasks from GDLC template in single transaction | End-to-end test: call `bulk_operations(cmd="create_task_tree", template_id="gdlc-default")`, verify task count, hierarchy integrity, dependency edges | Pending |
| **Functionality** | Cursor pagination returns stable results under concurrent writes | Concurrency test: writer process inserts/deletes tasks while reader paginates through full result set; UNION of all pages matches direct query | Pending |
| **Performance** | Single-task CRUD < 200ms p95; dashboard < 50ms; list < 100ms; bulk tree < 5s | Load test: 100 concurrent requests per endpoint category. Prometheus histograms verify p95 targets | Pending |
| **Performance** | Total tool definition budget < 2K tokens for all 5 facade tools | Token count utility: serialize all tool JSON Schema descriptions, count tokens via tiktoken. Must be < 2,000 | Pending |
| **Security** | All endpoints require JWT auth via `Depends(get_current_user_id)` | Security test: unauthenticated requests to every task endpoint return 401. Invalid org_id requests return empty results (RLS) | Pending |
| **Quality** | 8 error codes return correct structure with actionable context | Unit test per error code: trigger condition, verify `error_code`, `error_message`, and `context` fields in response | Pending |

#### Phase 3: Event Sourcing & Audit (Weeks 7-10)

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | Every task mutation generates corresponding audit event with correct `before_state`/`after_state`/`diff` | Integration test: perform each of 14 event types, query `audit_events`, verify RFC 6902 diff is correct and reversible | Pending |
| **Functionality** | Failed mutations do NOT create audit events | Test: trigger validation error on status transition, verify zero new rows in `audit_events` | Pending |
| **Functionality** | Bulk operations create linked parent + child events via `causation_id` | Test: execute `batch_update_status` on 10 tasks, verify 1 parent event + 10 child events with matching `causation_id` | Pending |
| **Functionality** | `query_audit_trail` tool returns correct event history filtered by task_id, agent_id, event_type, time range | Agent integration test: create events, query with each filter type, verify result accuracy | Pending |
| **Performance** | Audit event writes sustain > 1,000 events/sec burst | Load test: 50 concurrent writers each inserting 20 events; measure total throughput. Must exceed 1,000/sec | Pending |
| **Performance** | Projection tables update within 5 seconds of mutation (p95) | Test: mutate task, poll projection table, measure lag. 100 iterations, p95 must be < 5s | Pending |
| **Security** | `audit_events` table is append-only -- UPDATE and DELETE rejected | Attempt `UPDATE audit_events SET ...` and `DELETE FROM audit_events WHERE ...` as application role; verify permission denied | Pending |
| **Operations** | Monthly partitions created 3 months ahead; partition pruning confirmed | Verify `pg_partman` config; run `EXPLAIN` on time-bounded query, confirm partition pruning in plan | Pending |

#### Phase 4: Semantic Memory (Weeks 8-10, parallel with Phase 3)

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | Completing a task triggers async vectorization within 30 seconds | End-to-end test: transition task to `done`, poll `vectorized` flag, verify `true` within 30s. Verify Pinecone upsert via `fetch()` | Pending |
| **Functionality** | `search_task_memory` returns relevant results for natural language queries | Relevance test: vectorize 20 tasks with known content, query with 5 natural language queries, verify top-3 results include expected tasks | Pending |
| **Functionality** | Pinecone namespace isolation prevents cross-organization leakage | Multi-tenant test: vectorize tasks for 2 orgs, search from each org's namespace, verify zero cross-org results | Pending |
| **Performance** | Vectorization does not block status transition (< 200ms for status change regardless of embedding latency) | Timing test: mock Pinecone with 5-second delay, verify status transition completes in < 200ms. Background worker handles vectorization independently | Pending |
| **Operations** | `vectorized` flag + partial index enable backfill script to find and process un-vectorized tasks | Test: mark 10 tasks as `vectorized = false`, run backfill script, verify all become `true` | Pending |

#### Phase 5: Integration & Validation (Weeks 10-13)

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | All 8 agents can discover and invoke task tools via `get_available_tools()` | Integration test: instantiate each of 8 agent types, verify task tools appear in available tools list with correct permission scoping | Pending |
| **Functionality** | GDLC template seeder populates ~608 gate + ~98 work order items with stable slug IDs | Seeder test: run seeder, verify template item counts match expected, run seeder again (idempotency), verify no duplicates | Pending |
| **Functionality** | `check_gate_readiness` correctly evaluates phase gate pass/fail across full subtree | End-to-end test: create task tree, complete all items for one phase, verify gate passes. Leave 1 item incomplete, verify gate fails with blocking items listed | Pending |
| **Performance** | All Phase 2 latency targets still hold under combined workload (CRUD + audit + vectorization) | Full-stack load test: simulate 8 concurrent agents performing mixed operations for 10 minutes. All p95 targets must hold | Pending |
| **Security** | End-to-end multi-tenant isolation validated across all data paths (tasks, audit events, vectors, projections) | Cross-tenant penetration test: attempt to access Org B data through every endpoint and tool while authenticated as Org A | Pending |
| **Operations** | Feature flag `ENABLE_TASK_MANAGEMENT = false` disables all task endpoints and tools without affecting existing platform functionality | Feature flag test: set flag to false, verify 404 on all task endpoints, verify all existing endpoints still functional | Pending |
| **Operations** | Prometheus metrics and Grafana dashboards deployed for all technical KPIs from Section 19.3 | Manual verification: confirm each metric from 19.3 Technical Metrics table has a corresponding Prometheus metric and Grafana panel | Pending |

#### 21.4.2 Definition of Done (Feature Level)

A feature is considered "Done" when ALL of the following are satisfied:

- [ ] All acceptance criteria from the relevant phase release criteria table are met
- [ ] Unit tests written and passing (coverage > 90% for new code)
- [ ] Integration tests passing (at least 1 per API endpoint and agent tool)
- [ ] Code reviewed and approved (self-review + AI agent review for solo developer)
- [ ] All new models, services, and endpoints have docstrings explaining purpose and usage
- [ ] Performance benchmarks run and targets met (latency, throughput per Section 19.3)
- [ ] Security review completed: RLS verified, JWT auth on all endpoints, no hardcoded secrets
- [ ] Conventional commit messages (`type(scope): message`) for all commits
- [ ] Feature flag tested in both enabled and disabled states
- [ ] No regressions in existing platform functionality (existing test suite passes)
- [ ] Alembic migration tested on fresh database AND on database with existing data

#### 21.4.3 Rollback & Contingency Plans

| Scenario | Detection Method | Rollback Procedure | Decision Maker | Max Time to Rollback |
|----------|------------------|-------------------|----------------|---------------------|
| **Migration breaks existing tables** | Alembic `upgrade` fails or existing endpoint tests fail post-migration | `alembic downgrade -1` to revert migration. If cascade damage: restore from pre-migration database backup | Developer | 15 minutes (migration revert); 1 hour (backup restore) |
| **RLS blocks legitimate queries** | Task API returns empty results for authenticated users who should see data; Prometheus error rate spike on task endpoints | `ALTER TABLE task_instances DISABLE ROW LEVEL SECURITY` on all task tables. Application-level `WHERE organization_id = :org_id` remains as fallback filtering | Developer | 5 minutes (single SQL command per table) |
| **Task tools degrade agent performance** | Agent session latency p95 exceeds 5s (vs. 2s baseline); agent error rate > 10% | Set `ENABLE_TASK_MANAGEMENT = false` in environment config. All task tools become unavailable; agents fall back to pre-task-system behavior. No data loss -- task data persists in PostgreSQL | Developer | 2 minutes (config change + service restart) |
| **Audit event volume causes disk pressure** | PostgreSQL disk usage alert > 85%; `audit_events` partition size > 15GB | Detach oldest partition: `ALTER TABLE audit_events DETACH PARTITION audit_events_YYYYMM`. Archive to S3 if needed. Reduce hot retention from 90 to 30 days | Developer | 10 minutes (partition detach is metadata-only operation) |
| **Vectorization pipeline failure** | `vectorization_backlog_count` > 200 for 15+ minutes; Pinecone upsert errors in logs | Disable vectorization worker. `search_task_memory` tool returns "Service temporarily unavailable" (graceful degradation). Tasks continue to function without semantic search | Developer | 2 minutes (worker stop) |
| **Full feature rollback required** | Multiple scenarios compound; platform stability at risk | 1. Set `ENABLE_TASK_MANAGEMENT = false` (immediate). 2. Stop vectorization worker. 3. Disable task WebSocket endpoint. 4. Task data preserved in database for future re-enablement. No schema rollback needed -- tables can remain dormant | Developer | 5 minutes |

---


### 21.5 Timeline & Milestones


#### 21.5.1 High-Level Timeline

```
Week   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
       |----|----|----|----|----|----|----|----|----|----|----|----|----|----|

Phase 1: Data Model Foundation ──────────── W1-W3
       ├── M1.1: Schema + migration        W1
       ├── M1.2: RLS + partition-ready PKs  W2
       └── M1.3: State machine + indexes    W3
                                    |
Phase 2: AI Tool Layer ─────────────────────────────── W3-W7
       ├── M2.1: TaskService CRUD            W4
       ├── M2.2: Domain Facade tools         W5
       ├── M2.3: Bulk ops + cursor pagination W6
       └── M2.4: Human REST API + load test   W7
                                              |
Phase 3: Event Sourcing ───────────────── W7-W10      |
       ├── M3.1: audit_events table + partitioning  W8 |
       ├── M3.2: Co-transactional event recording   W9 |
       └── M3.3: Projections + query_audit_trail   W10 |
                                                       |
Phase 4: Semantic Memory ──────────── W8-W10  (parallel with Phase 3)
       ├── M4.1: Vectorization pipeline     W8-W9
       └── M4.2: search_task_memory tool     W10
                                              |
Phase 5: Integration & Validation ─────────────── W10-W13
       ├── M5.1: Agent tool registration      W11
       ├── M5.2: GDLC template seeder         W12
       ├── M5.3: Full-stack load test + fix   W13
       └── M5.4: Monitoring dashboards + docs  W13

                                              |
Deferred Workstreams (post-Phase 5) ──────── W14+
       ├── Real-Time Sync (WebSocket + Redis Streams)
       ├── Frontend Integration (Zustand + task panel)
       └── Template Versioning (SemVer upgrade-in-place)
```

**Critical Path:** Phase 1 -> Phase 2 -> Phase 5 (sequential, 10+ weeks minimum)
**Parallel Opportunity:** Phase 3 + Phase 4 overlap after Phase 2 stabilizes (saves 2 weeks vs. sequential)
**Total Estimate:** 11-13 weeks (optimistic: strong parallel execution) to 15 weeks (conservative: sequential + buffer)

#### 21.5.2 Detailed Phase Breakdown

#### Phase 1: Data Model Foundation (Weeks 1-3)

**Focus:** Establish the relational schema, multi-tenant isolation, and migration infrastructure that all subsequent phases build upon.

**Deliverables:**
- [ ] 6-7 relational tables (`task_templates`, `task_template_items`, `task_instances`, `task_instance_items`, `task_dependencies`, `task_comments`, `audit_events` shell)
- [ ] Standalone Alembic migration (independent of existing chain)
- [ ] RLS policies on all task tables with `organization_id` enforcement
- [ ] Composite PKs for partition readiness (`(organization_id, id)`)
- [ ] Compound indexes: `(project_id, status, priority)`, `(task_instance_id, is_checked)`, `(hierarchy_path, status)`
- [ ] Status state machine with 4+1 states and transition validation
- [ ] `fillfactor=70` on `task_instance_items` for HOT-eligible updates

**Success Criteria:**
- Migration runs cleanly on fresh database AND on database with existing data
- RLS isolation test passes: zero cross-tenant data leakage
- All indexes confirmed via `EXPLAIN ANALYZE` on representative queries

**Dependencies:** ID1 (Auth Service), ID2 (Project Service), ID3 (Database Infrastructure), ID7 (Alembic)
**Blocks:** Phase 2, Phase 3, Phase 4, Phase 5

**Target Completion:** Week 3

---

#### Phase 2: AI Tool Layer (Weeks 3-7)

**Focus:** Build the primary interface for AI agents -- the Domain Facade tools, TaskService, zoom levels, bulk operations, and cursor pagination. This is the longest single phase and the critical path.

**Deliverables:**
- [ ] `TaskService` with full CRUD, zoom-level responses (4 levels), and state machine enforcement
- [ ] 5 Domain Facade tools: `query_tasks`, `mutate_tasks`, `bulk_operations`, `search_task_memory` (stub), `query_audit_trail` (stub)
- [ ] `create_task_tree` bulk operation (~500 tasks in single transaction, < 5s)
- [ ] `batch_update_status`, `batch_check_items`, `resolve_dependencies`, `check_gate_readiness`
- [ ] Cursor-based pagination with 13 compound filters
- [ ] Field projection via `fields` parameter and 7 field group shortcuts
- [ ] 8 actionable error codes with agent-action guidance in response
- [ ] Human REST API endpoints sharing `TaskService`
- [ ] Pydantic schemas: `TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskListResponse`

**Success Criteria:**
- All 5 tools callable from test agent session
- Tool definition budget < 2K tokens total
- Latency targets: CRUD < 200ms, dashboard < 50ms, list < 100ms, bulk tree < 5s (p95)
- Cursor pagination stable under concurrent writes (zero duplicates/gaps)

**Dependencies:** Phase 1, ID4 (Agent System), ID5 (Swarm Orchestrator), ID6 (Session Context)
**Blocks:** Phase 3, Phase 4, Phase 5

**Target Completion:** Week 7

---

#### Phase 3: Event Sourcing & Audit Trail (Weeks 7-10)

**Focus:** Add immutable audit trail for all task mutations. Append-only `audit_events` table with RFC 6902 diffs, monthly partitioning, projection worker, and agent self-reflection tool.

**Deliverables:**
- [ ] `audit_events` table in separate `audit` schema with monthly range partitions (pg_partman)
- [ ] Co-transactional event recording (entity mutation + event write in same transaction)
- [ ] 14 event types with `before_state`/`after_state`/`diff` JSONB
- [ ] Optimistic concurrency via `stream_version` column
- [ ] Idempotency keys on destructive operations
- [ ] LISTEN/NOTIFY trigger for projection updates
- [ ] Projection tables: `entity_current_state`, `project_task_summary`
- [ ] `query_audit_trail` tool (replacing Phase 2 stub)

**Success Criteria:**
- Every mutation type generates correct audit event (14 event types verified)
- Failed mutations produce zero audit events
- Bulk operations create linked parent + child events
- Projection lag < 5s p95
- Audit event write throughput > 1,000 events/sec burst

**Dependencies:** Phase 2, ED4 (pg_partman)
**Parallel with:** Phase 4

**Target Completion:** Week 10

---

#### Phase 4: Semantic Memory (Weeks 8-10, parallel with Phase 3)

**Focus:** Cross-project institutional memory via completed task vectorization and semantic search.

**Deliverables:**
- [ ] Async vectorization pipeline: task completion -> background worker -> Pinecone upsert
- [ ] 9 high-signal fields for embedding text construction
- [ ] `vectorized` boolean + `vector_id` + `vectorized_at` columns on `TaskInstance`
- [ ] Partial index for pending vectorization (backfill support)
- [ ] Pinecone `task-memory` index with namespace-per-organization isolation
- [ ] `search_task_memory` tool (replacing Phase 2 stub)
- [ ] Feature flag `TASK_MEMORY_ENABLED`

**Success Criteria:**
- Vectorization completes within 30s of task completion
- Status transition latency unaffected by vectorization (< 200ms regardless)
- Semantic search returns relevant results for natural language queries
- Zero cross-organization data leakage in Pinecone

**Dependencies:** Phase 2, ED1 (Pinecone), ED2 (OpenAI Embedding API)
**Parallel with:** Phase 3

**Target Completion:** Week 10

---

#### Phase 5: Integration & Validation (Weeks 10-13)

**Focus:** End-to-end validation across all phases. Agent tool registration, GDLC template seeder, performance benchmarks, monitoring, and compliance documentation groundwork.

**Deliverables:**
- [ ] Task tools registered in all 8 agents with permission-scoped access
- [ ] Swarm orchestrator keyword routing for task-related intents
- [ ] GDLC template seeder: ~608 gate + ~98 work order items with stable slug IDs, idempotent
- [ ] Full-stack load test: 8 concurrent agents x 10-minute mixed workload
- [ ] Prometheus counters and histograms for all technical KPIs (Section 19.3)
- [ ] Grafana dashboards: latency, throughput, error rates, projection lag, partition health
- [ ] Feature flag `ENABLE_TASK_MANAGEMENT` tested in both states
- [ ] End-to-end multi-tenant penetration test
- [ ] API documentation for all task endpoints
- [ ] Compliance groundwork: AI transparency metadata on all agent-created tasks, ROPA update for task data processing

**Success Criteria:**
- All 28 integration checklist verification points pass (IC-1 through IC-28)
- All Phase 2 latency targets hold under combined workload
- Template seeder is idempotent (run twice, no duplicates)
- Feature flag disables all task functionality without affecting existing platform

**Dependencies:** Phase 2 (required), Phase 3 (required), Phase 4 (required), ID9 (GDLC Types), CT2 (DevOps)
**Blocks:** Frontend Integration, Real-Time Sync (deferred)

**Target Completion:** Week 13

---

#### 21.5.3 Post-MVP Deferred Workstreams

These workstreams can proceed in parallel after Phase 5 is complete. They are independent of each other.

| Workstream | Estimated Duration | Dependencies | Priority |
|-----------|-------------------|--------------|----------|
| **Real-Time Sync** (WebSocket + Redis Streams + `TaskConnectionManager`) | 3-4 weeks | Phase 5 complete, Redis Streams setup | Medium -- needed for multi-user observability |
| **Frontend Integration** (Zustand task slice, task panel, roadmap persistence) | 4-6 weeks | Phase 5 complete, frontend developer availability | Medium -- required for human task management UX |
| **Template Versioning** (SemVer upgrade-in-place, diff preview, version migration) | 2-3 weeks | Phase 5 complete, template usage patterns established | Low -- optimize after initial template usage data |
| **SOC 2 Type II Preparation** (controls documentation, evidence collection, readiness assessment) | 6-12 months | Phase 3 (audit trail) operational | High -- gates Enterprise tier launch |
| **Multi-Region Deployment** (US + EU hosting, Pinecone region, LLM provider residency) | 4-8 weeks | Phase 5 complete, infrastructure team | Medium -- gates EU Enterprise sales |

#### 21.5.4 Timeline Risk Adjustments

| Risk | If Triggered | Timeline Impact | Adjusted Total |
|------|-------------|----------------|---------------|
| TR1 (Migration chain drift) | Phase 1 blocked by existing migration conflicts | +1 week to Phase 1 | 12-16 weeks |
| TR4 (Event sourcing learning curve) | Phase 3 takes 4 weeks instead of 2-3 | +1 week, but Phase 4 parallel absorbs some slack | 12-16 weeks |
| OR4 (Solo developer bottleneck) | Extended breaks or context-switching | +2-3 weeks spread across phases | 13-18 weeks |
| Multiple risks compound | TR1 + TR4 + OR4 all trigger | +4 weeks worst case | 15-19 weeks |

**Planning recommendation:** Budget 13 weeks as the target, 15 weeks as the commitment. Communicate 11-15 week range to stakeholders with the dependency graph showing where parallelism saves time.

---

## 22. Customer Journey Map

> **Note:** The GameFrame AI Task Management System has two distinct operator journeys that interleave: the **human developer journey** (strategic decisions, review, iteration) and the **AI agent journey** (decomposition, execution, reporting). Both journeys traverse the same task data through different interfaces.

### 22.1 Human Developer Journey

| Stage | User Goal | Actions | Touchpoints | Emotions | Pain Points | Opportunities |
|-------|-----------|---------|-------------|----------|-------------|---------------|
| **Discover** | Understand what the platform offers for project management | Browse marketing site, view demo, read docs | Landing page, documentation, wizard demo | Curiosity, skepticism | "Will AI actually manage my game dev tasks?" | Show GDLC-aware task generation in demo; highlight "hours not months" value prop |
| **Configure** | Set up a new game project with structured GDLC lifecycle | Run 10-stage wizard (Genre through Summary), confirm game design selections | Wizard UI (274 WebM video assets), genre/camera/movement/combat stage selectors | Excitement, slight overwhelm at choices | Too many options; unclear how selections map to development work | Wizard influence system auto-balances to 100%; skip-to-completion for experienced users |
| **Delegate** | Let AI agents scaffold and manage the development lifecycle | Confirm template instantiation; AI agents create ~500 tasks from GDLC templates in one bulk operation | CoPilot Kit chat interface, task dashboard (zoom level 0), roadmap canvas | Relief, trust-building | "What did the AI just create? Is it correct?" | Dashboard shows aggregate counts immediately (~120-180 tokens); drill-down available |
| **Review** | Monitor progress, review agent work, make gate decisions | Check dashboard, review task details (zoom level 2), evaluate GDLC gate readiness, approve/reject gate decisions | Task dashboard, gate readiness view, audit trail, notification system | Confidence or concern depending on progress | Information overload if viewing all 500 tasks; unclear which tasks need attention | Zoom levels filter noise; gate readiness aggregation highlights blockers inline |
| **Iterate** | Refine, adjust priorities, handle blockers, advance through GDLC phases | Reassign tasks, adjust priorities, resolve blockers, advance to next phase, request agent re-work | Task panel (side panel with checklist checkboxes, status/priority dropdowns), chat interface, roadmap canvas | Satisfaction as phases complete; frustration at blockers | Manual status changes feel tedious; dependency chains unclear | Bulk status operations; auto-unblock on dependency resolution; visual dependency indicators on roadmap |

### 22.2 AI Agent Journey

| Stage | Agent Goal | Actions | Interface | Constraints | Error Handling |
|-------|-----------|---------|-----------|-------------|----------------|
| **Receive** | Understand user intent from natural language | Parse NL request via LangGraph orchestrator; identify target agent(s) among 8 specialists | LangGraph Swarm orchestration, `AgentState` with session context | Effective context window ~50% of advertised; tool definitions budget ~2K tokens | Ambiguous intent -> request clarification via CoPilot Kit; unknown domain -> route to Game Designer agent |
| **Decompose** | Break work into actionable task operations | Query existing tasks (zoom level 1 for orientation, level 0 for dashboard); identify relevant tasks via compound filters (13 parameters) | `query_tasks` Domain Facade tool with cursor pagination | Token budget per query response; max 5 pages safety limit for cyclic graph pagination | `TASK_NOT_FOUND` -> verify ID, re-query; empty results -> broaden filters, suggest alternatives |
| **Execute** | Perform task mutations via Domain Facade | Create/update/delete tasks via `mutate_tasks`; batch operations via `bulk_operations`; check items via `batch_check_items` | Domain Facade tools (~5 tools, ~2K token definitions vs ~12K for granular) | State machine validates all transitions; optimistic concurrency via `stream_version`; idempotency keys prevent duplicates | `INVALID_STATUS_TRANSITION` -> check `valid_transitions` array; `CONCURRENT_MODIFICATION` -> re-read, retry; `DEPENDENCY_NOT_MET` -> query blocker, complete it first |
| **Report** | Communicate results back to user and audit trail | Return structured response to orchestrator; audit event written co-transactionally; projection worker updates dashboard within 1-5s | Audit trail (`audit_events` table), LISTEN/NOTIFY projections, CoPilot Kit chat response | Every mutation generates immutable event with before/after state, RFC 6902 diff | Failed mutations do NOT create audit events; partial-success bulk ops report per-item errors |
| **Learn** | Build institutional memory from completed work | On task completion -> async vectorization of 9 high-signal fields -> Pinecone `task-memory` index; future queries use `search_task_memory` tool | Background worker (Celery/RQ), Pinecone namespace per organization, OpenAI `text-embedding-3-small` (1536 dims) | Vectorization async (<30s), does not block status transition (<200ms); feature-flagged via `TASK_MEMORY_ENABLED` | Embedding failure -> retry queue; Pinecone unavailable -> log, skip (non-blocking); model version tracked in metadata for re-embedding |

### 22.3 Moments of Truth

| Moment | Description | Success Criteria | Failure Recovery |
|--------|-------------|------------------|------------------|
| **First Template Instantiation** | User confirms wizard output; AI creates ~500 GDLC tasks in one bulk operation (<5s) | Dashboard shows accurate aggregate counts within 5 seconds; user can drill down to any task | Bulk creation failure -> transaction rollback, no partial state; retry with same idempotency key; clear error message via CoPilot Kit |
| **First Agent Interaction** | User gives natural language instruction; agent queries, acts, and reports back | Agent completes action in <200ms tool call; user sees updated state on dashboard within 5s (projection lag) | Agent error -> actionable error code returned with suggested next action; user sees "Agent encountered issue: [human-readable message]" |
| **First Gate Decision** | User reviews GDLC phase gate readiness; decides Go/No-Go/Conditional Pass | Gate readiness check returns blocking items inline (<50ms); user has full context to decide | Incomplete gate data -> `GATE_NOT_READY` error with list of incomplete items; user can query specific blockers |
| **Cross-Project Memory Query** | User or agent asks "How did we handle X in the last project?" | Semantic search returns relevant completed tasks with similarity scores (~150-300 tokens for 5 results) | No relevant results -> clear "no matching tasks found" response; suggest broader query terms |
| **Concurrent Multi-Agent Work** | Multiple specialist agents work on tasks in same project simultaneously | No data corruption; optimistic concurrency detects conflicts; checklist items are independent (no conflicts) | `CONCURRENT_MODIFICATION` -> automatic re-read and retry (once); escalate to orchestrator if retry fails |

---

## 23. Error Handling & Edge Cases

### 23.1 Error Categories

| Category | Examples | User Experience | Recovery |
|----------|----------|-----------------|----------|
| **Validation Errors** | Invalid status transition (e.g., `to_do` -> `done` skipping `doing`); missing required fields on task create; `blocker_reason` empty when transitioning to `blocked`; invalid `detail` zoom level parameter; cursor pagination with expired/malformed cursor | Agent receives `VALIDATION_ERROR` with `context.validation_errors` containing field-level details; human API returns 422 with field-specific messages | Agent: read error context, fix fields, retry. Human: form highlights invalid fields with guidance. State machine errors include `valid_transitions` array showing legal next states |
| **System Errors** | PostgreSQL connection failure; Redis unavailable; Pinecone API timeout; Alembic migration conflict; PgBouncer `DuplicatePreparedStatementError` (asyncpg cache + transaction mode) | Agent receives generic system error with retry guidance; human sees "Service temporarily unavailable" with estimated recovery time | Circuit breaker pattern (existing in platform); graceful degradation -- task queries still work if vectorization/audit is down; retry with exponential backoff |
| **Concurrency Conflicts** | Two agents update same task field simultaneously; bulk operation conflicts with individual mutation; `stream_version` mismatch on optimistic lock | Agent receives `CONCURRENT_MODIFICATION` error with instruction to re-read task and retry with updated `stream_version` | Per-operation resolution: checklist items = no conflict (independent rows); status = last-write-wins (state machine validates); fields = retry once then escalate to LangGraph orchestrator; bulk ops = advisory locks serialize per `(project_id, operation_type)` |
| **Dependency Errors** | Task blocked by incomplete predecessor; circular dependency detected in DAG; gate readiness check fails due to incomplete subtree | Agent receives `DEPENDENCY_NOT_MET` with blocking task ID and title; `GATE_NOT_READY` with list of incomplete items inline | Agent: query blocking task, complete it first, then retry. Circular dependency: rejected at creation time with DAG validation error. Gate: surface blocking items so agent/human can prioritize |
| **Integration Errors** | OpenAI embedding API failure during vectorization; Pinecone upsert failure; LISTEN/NOTIFY channel disconnect | Vectorization failures are async and non-blocking -- task status transition completes regardless; projection lag increases but dashboard eventually catches up | Embedding retry queue with exponential backoff; Pinecone failure -> log and retry (task marked `vectorized=false`); LISTEN/NOTIFY reconnect automatically |
| **Timeout Errors** | Bulk tree creation exceeds 5s target; semantic search exceeds 500ms; long-running cursor pagination across 500+ tasks | Agent receives timeout with partial results if available; bulk ops use partial-success semantics | Bulk creation: increase transaction timeout for initial scaffolding (one-time); pagination: enforce `max_pages=5` safety limit; semantic search: return cached results or suggest narrower query |

### 23.2 Edge Cases

| Scenario | Expected Behavior | Test Case |
|----------|-------------------|-----------|
| **Circular dependency creation** | DAG validation rejects the dependency with descriptive error; no partial state persisted | Create tasks A->B->C, then attempt C->A dependency; verify rejection and existing deps unchanged |
| **Orphaned tasks after parent deletion** | Cascade policy: child tasks re-parented to grandparent (or become root-level) with audit event; never silently deleted | Delete a mid-level task with 3 children and verify children's `parent_task_id` and `hierarchy_path` updated |
| **Max depth exceeded** | Task creation rejected when `depth >= max_depth` (configurable, default 6) with error including current depth and limit | Attempt to create task at depth 7 with default config; verify 400 response with actionable message |
| **Partial bulk failure** | Valid operations within a bulk request commit; invalid operations return per-item errors in response; no all-or-nothing rollback for bulk status/checklist ops | Batch update 10 task statuses where 3 have invalid transitions; verify 7 succeed and 3 return specific error codes |
| **Template instantiation with missing genre conditions** | Genre-conditional items (291 of ~791 total) excluded when genre not selected; remaining items instantiated normally | Instantiate GDLC template with no genre selected; verify only non-conditional items created (~500 tasks) |
| **Concurrent gate decision** | First gate decision commits; subsequent attempts receive `CONCURRENT_MODIFICATION` if state changed | Two users submit gate decision simultaneously; verify one succeeds, other receives conflict with updated state |
| **Empty project dashboard** | Zoom level 0 returns valid response with all counts at zero; no error | Query dashboard for newly created project with zero tasks; verify structured response with zero counts |
| **Stale cursor pagination** | Cursor remains valid across concurrent inserts/deletes (keyset pagination stability); no duplicates or gaps | Insert 5 tasks while paginating through 50; verify all original tasks appear exactly once and new tasks appear in subsequent pages |
| **Idempotent duplicate operation** | `IDEMPOTENT_DUPLICATE` response returned with original result; no duplicate task/event created | Send same create request with same idempotency key twice; verify single task exists and second call returns original |
| **Vectorization of task with minimal content** | Tasks with very short descriptions still vectorize (embedding model handles short text); similarity scores may be lower | Complete a task with only a title and no description; verify vectorization succeeds and search returns it for relevant queries |

### 23.3 Graceful Degradation

| Component Failure | Degraded Experience | User Communication |
|-------------------|--------------------|--------------------|
| **Pinecone unavailable** | Semantic memory search (`search_task_memory`) returns empty results with service status indicator; all other task operations unaffected | Agent receives `"service_status": "semantic_memory_unavailable"`; human sees "Cross-project search temporarily unavailable" |
| **Redis unavailable** | Real-time sync (WebSocket broadcasts) stops; task CRUD continues via direct PostgreSQL; dashboard refreshes on page reload instead of live | Toast notification: "Real-time updates paused -- refresh for latest state" |
| **Projection worker down** | Dashboard (zoom level 0) serves stale data from last projection update; zoom levels 1-3 query live tables directly (slightly slower) | Dashboard shows "Last updated: [timestamp]" indicator; no blocking error |
| **Audit event write failure** | Audit is co-transactional: if the audit INSERT fails, the entire transaction (including entity mutation) rolls back. This is deliberate — an unaudited mutation is worse than a failed mutation. The mutation is retried with the audit INSERT. If audit failures persist (e.g., partition table missing), the circuit breaker trips and all mutations halt until audit infrastructure is restored. | Admin alert: "Audit write failure — mutations blocked until resolved." Ops runbook: verify pg_partman partition exists, check disk space, restart audit schema connection pool. |
| **Single agent failure** | LangGraph orchestrator routes to alternate agent or queues for retry; other agents continue operating on independent tasks | User sees "Agent [name] encountered an issue; rerouting..." in chat; no data loss |

---

## 24. User Interaction & Design

### 24.1 Wireframes & Mockups

| Screen/Flow | Link | Status | Notes |
|-------------|------|--------|-------|
| Task Dashboard (Zoom Level 0) | TBD -- design pending | Draft | Aggregate counts by status/phase/area; entry point for all task management; ~120-180 tokens equivalent data density |
| Task List View (Zoom Level 1) | TBD -- design pending | Draft | Filterable/sortable table with 13 compound filters; cursor pagination; columns: title, status, priority, phase, area, assigned_to, progress, due_date |
| Task Detail Panel (Zoom Level 2) | TBD -- design pending | Draft | Side panel overlay on roadmap canvas; all frontmatter fields + interactive checklist checkboxes + status/priority dropdowns + recent audit log |
| Gate Readiness View | TBD -- design pending | Draft | Per-phase gate completion summary; blocking items listed inline; Go/No-Go/Conditional Pass decision controls |
| Roadmap Canvas (Extended) | Existing at `frontend/app/roadmap/` | Existing -- needs persistence layer | 5 node types (ListNode, MenuNode, IconNode, plus new TaskNode); dependency connectors; viewport culling; lock/done/in-progress state |
| CoPilot Kit Chat Interface | Existing at `frontend/src/components/Chat/` | Existing -- needs task tool integration | Split-screen AI chat; agent responses include task operation results; natural language task management |

### 24.2 Design System

The platform uses an established multi-library design system. Task management UI extends existing patterns:

- [x] Component library documented -- Ant Design (primary component library) + Headless UI + Radix UI (accessible primitives)
- [x] Design tokens defined -- Tailwind CSS for colors, spacing, typography; `tailwind.config` as token source of truth
- [x] Icon set selected -- Heroicons + MUI Icons (both installed and in use)
- [x] Responsive breakpoints defined -- Tailwind default breakpoints (sm/md/lg/xl/2xl)
- [x] Animation/motion guidelines -- Framer Motion for transitions and animations

**Task-specific design considerations:**
- **Checklist interactions**: Checkbox components from Ant Design; optimistic UI update via Zustand with server rollback on rejection
- **Status badges**: Color-coded status indicators following existing badge patterns (`frontend/src/components/ui/badge`)
- **Priority indicators**: Visual weight hierarchy (P0 red/urgent through P2 subtle)
- **Progress bars**: Computed from checked/total checklist items; displayed in list and detail views
- **Dependency visualization**: Extend existing roadmap dependency connectors and indicators (`frontend/app/roadmap/`)
- **Forms**: React Hook Form + Zod schemas for task create/edit forms (existing pattern)
- **Data tables**: @tanstack/react-query for server state; Zustand for UI state (filter selections, sort order)
- **Toast notifications**: react-hot-toast for async operation feedback (existing)

### 24.3 Prototype Links

| Prototype | Purpose | Link |
|-----------|---------|------|
| Roadmap Canvas (Current) | Demonstrates existing canvas with 533 taxonomy nodes, dependency visualization, viewport culling | `frontend/app/roadmap/` (run locally) |
| Wizard System (Current) | Demonstrates 10-stage game configuration flow that feeds template instantiation | `frontend/app/wizard/` (run locally) |

> **Note:** No dedicated task management prototypes exist yet. The roadmap canvas and wizard system serve as the foundation -- task management extends both with backend persistence and real-time sync.

---

## 25. API Contract Examples

> **Note:** The task management system exposes two parallel interfaces to the same `TaskService`: (1) **Domain Facade agent tools** optimized for LLM token efficiency, and (2) **REST API endpoints** for human-facing frontend. The examples below show the Domain Facade tool interface, which is the primary interface (AI agents perform 95%+ of all task operations).

### 25.1 `task.create` -- Create a Task

**Agent Tool Call:**
```json
{
  "tool": "mutate_tasks",
  "input": {
    "cmd": "create",
    "title": "Implement character jump height adjustment",
    "description": "Configure GAS ability for variable jump height based on wizard movement settings",
    "status": "to_do",
    "type": "task",
    "priority": "P1",
    "parent_task_id": "mov-char-locomotion",
    "area_id": "mls",
    "gdlc_phase": 3,
    "assigned_to": "movement-specialist",
    "tags": ["movement", "GAS", "wizard-derived"],
    "estimation": "3d",
    "idempotency_key": "create-jump-height-2026-03-19-001"
  }
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "short_id": "a1b2c3d4",
    "title": "Implement character jump height adjustment",
    "status": "to_do",
    "hierarchy_path": "mls.char-locomotion.jump-height-adj",
    "depth": 3,
    "created_at": "2026-03-19T14:30:00Z"
  },
  "audit_event_id": 12345
}
```

**Response (Error -- Validation):**
```json
{
  "success": false,
  "error_code": "VALIDATION_ERROR",
  "error_message": "Task creation failed: 2 validation errors",
  "context": {
    "validation_errors": [
      {"field": "priority", "message": "Invalid priority 'P5'. Valid values: P0, P1, P2, P3"},
      {"field": "gdlc_phase", "message": "Phase must be between 1 and 7"}
    ],
    "suggested_action": "Fix the listed fields and retry"
  }
}
```

---

### 25.2 `task.query` -- Query Tasks with Zoom Levels

**Zoom Level 0 (Dashboard -- ~120-180 tokens total):**
```json
{
  "tool": "query_tasks",
  "input": {
    "cmd": "summary",
    "project_id": "proj-uuid-here",
    "detail": "dashboard"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "project_id": "proj-uuid-here",
    "total_tasks": 487,
    "by_status": {"to_do": 312, "doing": 45, "done": 118, "blocked": 12},
    "by_phase": {"1": 82, "2": 95, "3": 110, "4": 85, "5": 60, "6": 35, "7": 20},
    "by_priority": {"P0": 8, "P1": 67, "P2": 245, "P3": 167},
    "gate_status": {"phase_1": "passed", "phase_2": "ready", "phase_3": "not_ready"},
    "blocked_summary": {"count": 12, "top_blockers": ["Dependency on art pipeline", "Awaiting combat review"]},
    "last_updated": "2026-03-19T14:25:00Z"
  }
}
```

**Zoom Level 1 (List -- ~40-55 tokens/task):**
```json
{
  "tool": "query_tasks",
  "input": {
    "cmd": "list",
    "project_id": "proj-uuid-here",
    "detail": "list",
    "filters": {
      "status": ["doing", "blocked"],
      "area_id": "mls",
      "assigned_to": "movement-specialist"
    },
    "sort_by": "priority",
    "sort_order": "asc",
    "limit": 25
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "short_id": "a1b2c3d4",
        "title": "Implement character jump height adjustment",
        "status": "doing",
        "priority": "P1",
        "phase": 3,
        "area": "mls",
        "assigned_to": "movement-specialist",
        "progress": "3/8",
        "due_date": "2026-04-01",
        "is_blocked": false
      }
    ],
    "pagination": {
      "total_count": 7,
      "returned_count": 7,
      "has_more": false,
      "next_cursor": null,
      "prev_cursor": null
    },
    "filters_applied": {"status": ["doing", "blocked"], "area_id": "mls", "assigned_to": "movement-specialist"},
    "sort": {"by": "priority", "order": "asc"}
  }
}
```

---

### 25.3 `task.update` -- Update with Concurrency Control

**Agent Tool Call (Status Transition):**
```json
{
  "tool": "mutate_tasks",
  "input": {
    "cmd": "transition_status",
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "new_status": "done",
    "stream_version": 5
  }
}
```

**Response (Success -- with side effects):**
```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "done",
    "completion_date": "2026-03-19T15:00:00Z",
    "stream_version": 6,
    "side_effects": {
      "newly_unblocked": [
        {"id": "bbbb-cccc", "short_id": "bbbbcccc", "title": "Integration test for jump mechanics"}
      ],
      "gate_readiness_changed": false
    }
  },
  "audit_event_id": 12398
}
```

**Response (Error -- Concurrency Conflict):**
```json
{
  "success": false,
  "error_code": "CONCURRENT_MODIFICATION",
  "error_message": "Task was modified by another agent since your last read",
  "context": {
    "expected_version": 5,
    "current_version": 7,
    "last_modified_by": "combat-designer",
    "last_modified_at": "2026-03-19T14:58:00Z",
    "suggested_action": "Re-read the task to get current state (version 7), then retry your operation"
  }
}
```

**Response (Error -- Invalid Transition):**
```json
{
  "success": false,
  "error_code": "INVALID_STATUS_TRANSITION",
  "error_message": "Cannot transition from 'to_do' directly to 'done'",
  "context": {
    "current_status": "to_do",
    "requested_status": "done",
    "valid_transitions": ["doing"],
    "suggested_action": "Transition to 'doing' first, then to 'done' after completing all checklist items"
  }
}
```

---

### 25.4 `checklist.batch_update` -- Batch Checklist Item Operations

**Agent Tool Call:**
```json
{
  "tool": "bulk_operations",
  "input": {
    "cmd": "batch_check_items",
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "items": [
      {"item_id": "item-001", "is_checked": true, "completion_type": "success"},
      {"item_id": "item-002", "is_checked": true, "completion_type": "success"},
      {"item_id": "item-003", "is_checked": true, "completion_type": "blocker_logged", "blocker_reason": "Art assets not delivered; logged for follow-up"}
    ]
  }
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "items_updated": 3,
    "progress": {
      "checked": 6,
      "total": 8,
      "percentage": 75
    },
    "next_unchecked": {
      "item_id": "item-004",
      "text": "Validate jump height against wizard movement settings",
      "phase": 2,
      "step": 1
    },
    "blockers_logged": 1
  },
  "audit_event_ids": [12399, 12400, 12401]
}
```

**Response (Partial Failure):**
```json
{
  "success": true,
  "partial": true,
  "data": {
    "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "items_updated": 2,
    "items_failed": 1,
    "errors": [
      {
        "item_id": "item-003",
        "error_code": "VALIDATION_ERROR",
        "error_message": "Item item-003 not found on this task"
      }
    ],
    "progress": {
      "checked": 5,
      "total": 8,
      "percentage": 62
    },
    "next_unchecked": {
      "item_id": "item-real-003",
      "text": "Configure stamina drain multiplier",
      "phase": 1,
      "step": 4
    }
  },
  "audit_event_ids": [12399, 12400]
}

---

## 26. Contributors & Collaboration

### 26.1 Document Contributors

| Role | Name | Contribution |
|------|------|--------------|
| Product Owner / Solo Developer | TBD | Product vision, system requirements, architecture decisions, GDLC framework design, all implementation |
| AI Research Agents (rf-task-researcher) | Claude Code | Codebase analysis, external research, pattern extraction, gap identification across 7 research files |
| AI Synthesis Agents (rf-task-builder) | Claude Code | PRD synthesis from research artifacts, template compliance, cross-reference validation |
| AI Quality Agents (rf-analyst, rf-qa) | Claude Code | Completeness verification, zero-trust quality gates, cross-validation between research files |
| Architecture Validation | AI-Operator Research Report | AI-operator constraint analysis, Option C architecture confirmation, 20 open question resolutions |
| Baseline Investigation | Task Management Baseline Report | Existing codebase audit, gap analysis across 10 capability dimensions, 28 integration checkpoints |

### 26.2 How to Contribute

- **Comment inline** for questions, suggestions, or clarifications
- **Tag relevant team members** using @ mentions in the repository
- **Update Open Questions table** (Section 13) when decisions are made
- **Link related documents** -- research reports, TDD, architecture proposals
- **Review quarterly** and flag outdated sections (see Section 28.2 for schedule)
- **Cross-reference research artifacts** in `.dev/tasks/to-do/TASK-PRD-20260319-143000/research/` for evidence behind any claim

---

## 27. Related Resources

### 27.1 Research Reports (Primary Sources)

| Resource | Path | Description |
|----------|------|-------------|
| AI-Operator Research Report | `.dev/tasks/to-do/TASK-RESEARCH-20260319-103000/RESEARCH-REPORT-ai-operated-task-mgmt.md` | AI-operator constraint analysis: Domain Facade pattern, zoom levels, bulk operations, event sourcing, 20 resolved open questions |
| Task Management Baseline Report | `.dev/tasks/to-do/TASK-RESEARCH-20260317-160411/RESEARCH-REPORT-task-management-system.md` | Comprehensive codebase audit: 10 capability dimensions, gap analysis, Option C architecture recommendation, 28 integration checkpoints |

### 27.2 PRD Research Files

| Resource | Path | Description |
|----------|------|-------------|
| Product Capabilities Extraction | `.dev/tasks/to-do/TASK-PRD-20260319-143000/research/01-product-capabilities.md` | 26 capabilities across 6 groups with status, implementation approach, user value |
| Architecture & Technical Stack | `.dev/tasks/to-do/TASK-PRD-20260319-143000/research/03-architecture-technical.md` | Option C Hybrid architecture, performance targets, security requirements, technology stack |
| Risk, Scope & Dependencies | `.dev/tasks/to-do/TASK-PRD-20260319-143000/research/05-risk-scope-dependencies.md` | 14 MVP capabilities, 10 technical + 4 business + 4 operational risks, 17 dependencies |
| Gaps and Questions | `.dev/tasks/to-do/TASK-PRD-20260319-143000/gaps-and-questions.md` | 5 important gaps, 5 minor gaps from analyst/QA gate reports |

### 27.3 Platform Documentation

| Document | Path | Description |
|----------|------|-------------|
| Project Master Reference | `GFxAI/CLAUDE.md` | Comprehensive platform overview: architecture, tech stack, development standards, key directories |
| Architecture Overview | `GFxAI/docs/archive/architecture/ARCHITECTURE.md` | Platform architecture documentation |
| GDLC Framework Hub | `GFxAI/docs/docs-product/product/gdlc/gdlc-hub.md` | Game Development Lifecycle reference guide, 7 phases, 6 work orders, 7 gate checklists |
| GDLC TypeScript Types | `GFxAI/frontend/app/roadmap/types/gdlc.ts` | Authoritative source for AreaIds, Phase Focus Matrix (code > docs per Rule 12) |
| Agent Architecture | `GFxAI/docs/archive/agents/GameFrame-Agents-101.md` | 8 specialist AI agent descriptions and orchestration patterns |
| Plugin Integration | `GFxAI/docs/plugin-integration/plugin-integration.md` | 40+ UE5 plugin integration documentation |

### 27.4 Spec Panel Review & Remediations

> **Note:** These files contain TDD-ready specifications produced by an 11-expert spec panel review. Product decisions from the remediations have been integrated into this PRD. The full technical specifications (SQL schemas, error payloads, boundary conditions, implementation patterns) feed directly into the TDD.

| Document | Path | Description |
|----------|------|-------------|
| Spec Panel Review | `docs/docs-product/tech/task-management/PRD_TASK_MANAGEMENT_SYSTEM_SPEC_PANEL_REVIEW.md` | Full 11-expert review — 2 critical, 12 major, 8 minor findings |
| Crit1 — State Machine | `.dev/releases/backlog/task-management-v1/Crit1-FINAL-REMEDIATION.md` | Complete 5x5 transition matrix, side-effect table, error catalog, CHECK constraints, test requirements |
| Crit2 — project_id + Empty States | `.dev/releases/backlog/task-management-v1/Crit2-FINAL-REMEDIATION.md` | Empty-state behavior matrix, pagination boundaries, mid-transaction visibility, result_context enum |
| Major Issue Remediations (M1-M12) | `.dev/releases/backlog/task-management-v1/M{N}-FINAL-REMEDIATION.md` | Organization model, enum values, dependency cascades, educator persona, hierarchy_path, audit transactionality, gate thresholds, cancelled lifecycle, Redis constraints, load test spec, user research, guard boundaries |
| Remediation Pipeline Prompt | `.dev/releases/backlog/task-management-v1/PROMPT-major-issue-remediation.md` | Orchestration prompt used to generate M1-M12 remediations |

### 27.5 Template References

| Document | Path | Description |
|----------|------|-------------|
| PRD Template | `.claude/templates/documents/prd_template.md` | Template schema this PRD conforms to |
| TDD Template | `.claude/templates/documents/tdd_template.md` | For future Technical Design Document |
| Technical Reference Template | `.claude/templates/documents/technical_reference_template.md` | For documenting implemented features |

---

## 28. Maintenance & Ownership

### 28.1 Document Ownership

| Role | Name | Responsibility |
|------|------|----------------|
| **Primary Owner** | TBD | Overall document accuracy, architectural decisions, scope changes, priority adjustments |
| **Technical Owner** | TBD | Technical sections accuracy (Sections 14-15), performance targets, technology stack updates |
| **Backup Owner** | AI Agents (Claude Code) | Research updates, cross-reference validation, staleness detection via codebase analysis |

### 28.2 Review Schedule

> **Note:** High-level review cadence is defined in the Contract Table (Completeness Status section). This section captures the detailed scheduling for each review type.

| Review Type | Cadence | Next Date | Participants | Focus Areas |
|-------------|---------|-----------|--------------|-------------|
| **Full Review** | Quarterly | 2026-06-19 | Primary Owner | All sections; validate against implemented code; update scope/timeline based on actual progress |
| **Technical Review** | Per-Phase Completion | After Phase 1 completion | Primary Owner | Sections 14-15 (Technical Requirements, Tech Stack); validate assumptions TA1-TA8 against implementation reality |
| **Risk Review** | Monthly during active development | 2026-04-19 | Primary Owner | Section 20 (Risk Analysis); re-score risks based on new evidence; close mitigated risks |
| **Scope Review** | Per-Phase Gate | After each GDLC-style gate | Primary Owner | Section 12 (Scope Definition); move deferred items to in-scope or permanently out-of-scope based on learnings |
| **Ad-Hoc Review** | As needed | -- | Primary Owner | Triggered by: major architecture change, new dependency, GDLC framework update, or research report findings that invalidate assumptions |

### 28.3 Update Process

1. **Propose Changes**: Identify the section needing update and the evidence driving the change (code diff, research finding, user feedback, or phase completion)
2. **Cross-Reference Research**: Check if the change invalidates claims in research files (`.dev/tasks/to-do/TASK-PRD-20260319-143000/research/`). Update research artifacts if needed
3. **Update Document**: Incorporate approved changes. Use `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags on any claim derived from documentation rather than code inspection
4. **Increment Version**: Update version number in Document History (Appendix). Use SemVer: PATCH for typo/clarification, MINOR for scope/requirement changes, MAJOR for architectural pivots
5. **Notify Team**: Commit with conventional commit message `docs(prd): [change summary]`
6. **Archive Old Version**: Git history serves as version archive. Tag significant versions with `prd-vX.Y.Z` if needed

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **GDLC** | Game Development Lifecycle. A 7-phase framework (Concept, Pre-Production, Vertical Slice, Production, Polish, Release, Live Ops) with 9 areas and formal gate reviews governing the progression of game development projects on the GameFrame AI platform. |
| **MDTM** | Markdown-Driven Task Management. A task file format using YAML frontmatter (22 fields) and markdown checklists to define, track, and execute work items. Used by the Rigorflow agent framework and serving as the data model blueprint for the database-backed task system. |
| **Domain Facade** | An API design pattern that consolidates many granular tool definitions into a small number of facade tools (~5), each accepting a `cmd` parameter to select the specific operation. Reduces LLM tool-definition token overhead by ~83% (from ~12K to ~2K tokens). |
| **CQRS** | Command Query Responsibility Segregation. An architectural pattern that separates read and write models. In this system, used additively via projection tables (read models) derived from the append-only `audit_events` table, not as a full primary-store replacement. |
| **RLS** | Row-Level Security. A PostgreSQL feature that enforces tenant data isolation at the database engine level via policies. Each query is automatically filtered to the current organization's data, preventing cross-tenant data leakage even if application code has bugs. |
| **HOT** | Heap-Only Tuple. A PostgreSQL optimization where row updates that do not modify indexed columns can be performed without updating indexes. Enabled by setting `fillfactor=70` on frequently-updated tables like `task_instance_items`, allowing checkbox updates to bypass index maintenance. |
| **ltree** | A PostgreSQL extension providing a hierarchical label data type for tree-like structures. Deferred as a non-breaking future enhancement; the MVP uses TEXT `hierarchy_path` with B-tree index and LIKE queries for subtree operations. |
| **Zoom Level** | A response density control mechanism for AI agent tool responses. Four levels: Dashboard (aggregate counts, ~120-180 tokens), List (~40-55 tokens/task), Detail (~500-2000 tokens/task), Full (~2000-10000 tokens/task). Agents select the appropriate level to manage context window budget. |
| **Cursor Pagination** | A pagination method using opaque cursor tokens (Base64-encoded sort key + ID) instead of offset/limit. Provides stable results across concurrent inserts and deletes, unlike offset-based pagination where items can shift between pages. |
| **RFC 6902** | JSON Patch format (RFC 6902). A standard for expressing changes to a JSON document as an array of operations (add, remove, replace, move, copy, test). Used in the `audit_events` table `diff` column to record exact field-level changes for every task mutation. |

### Appendix B: Acronyms

| Acronym | Meaning |
|---------|---------|
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| DAG | Directed Acyclic Graph (used for task dependency ordering) |
| FK | Foreign Key |
| GAS | Gameplay Ability System (Unreal Engine framework) |
| GDLC | Game Development Lifecycle |
| HOT | Heap-Only Tuple (PostgreSQL optimization) |
| JWT | JSON Web Token |
| LWW | Last-Write-Wins (conflict resolution strategy) |
| MDTM | Markdown-Driven Task Management |
| MVP | Minimum Viable Product |
| ORM | Object-Relational Mapping |
| PK | Primary Key |
| PRD | Product Requirements Document |
| RLS | Row-Level Security |
| RQ | Redis Queue |
| SaaS | Software as a Service |
| SemVer | Semantic Versioning (MAJOR.MINOR.PATCH) |
| TDD | Technical Design Document |
| UE | Unreal Engine |
| UUID | Universally Unique Identifier |
| WebRTC | Web Real-Time Communication |

### Appendix C: Technical Architecture Diagrams

> Architecture diagrams are maintained in the research reports rather than inline in the PRD. See:
> - Option C Hybrid Architecture: `.dev/tasks/to-do/TASK-RESEARCH-20260318-130000/phase-outputs/reports/RESEARCH-REPORT-ai-operated-task-mgmt.md` Section 5
> - Data Model Schema: `.dev/tasks/to-do/TASK-PRD-20260319-143000/research/03-architecture-technical.md` Section 1.2
> - Phase Dependency Graph: `.dev/tasks/to-do/TASK-PRD-20260319-143000/research/05-risk-scope-dependencies.md` Section 4.4

### Appendix D: User Research Data

> **Note:** No formal user research (interviews, surveys) has been conducted. User personas and value propositions in this PRD are derived from the customer segments defined in CLAUDE.md (Solo Indie Developers, Small Game Studios, Educational Institutions, Enterprise Studios) and validated against the GameFrame AI platform's stated target market. Formal user research is flagged as gap I2 in the gaps-and-questions file and should be conducted before Phase 2 feature prioritization.

### Appendix E: Financial Projections

> **Note:** Financial projections for the task management system are embedded within the broader GameFrame AI SaaS platform pricing model (Indie $99/mo, Studio $499/mo, Enterprise $2,499/mo). Task management is a platform capability, not a separately priced feature. Usage-based costs specific to this system include: Pinecone vector storage (Phase 4), OpenAI embedding API calls (Phase 4), and PostgreSQL storage for audit events (configurable retention per subscription tier).

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-19 | TBD + Claude Code (rf-task-researcher, rf-task-builder, rf-analyst, rf-qa) | Initial draft. Synthesized from 2 research reports (AI-operator + baseline), 7 PRD research files, and 4 analyst/QA gate reports. Covers 26 capabilities across 6 groups. Option C Hybrid architecture. 5-phase implementation plan (11-15 weeks). |
