# Web Research: PRD-Driven Roadmapping Patterns

**Topic:** PRD-driven roadmapping and value-based phasing
**Status:** Complete
**Date:** 2026-03-27

---

## 1. PRD Business Context Shaping Technical Prioritization

### 1.1 Modern PRD Structure and Engineering-Relevant Sections

**Source:** [Aha! - PRD Templates](https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template)
**Source:** [Perforce - How to Write a PRD](https://www.perforce.com/blog/alm/how-write-product-requirements-document-prd)
**Source:** [Productboard - PRD Guide](https://www.productboard.com/blog/product-requirements-document-guide/)
**Reliability:** HIGH (established PM tooling vendors)
**Relevance:** HIGH

Modern PRDs have evolved from monolithic documents to leaner, iterative artifacts. The sections most relevant to engineering roadmap enrichment are:

- **Purpose and Goals**: What the product aims to achieve -- provides the "why" behind technical decisions
- **User Needs / Personas**: Customer interaction patterns -- informs API design priorities, UX-critical paths
- **Prioritization and Constraints**: Must-haves vs. nice-to-haves -- directly maps to phasing decisions
- **Success Metrics / KPIs**: Measurable outcomes -- enables engineering to prioritize features that move key metrics
- **Timeline and Release Plan**: High-level milestones -- provides business-driven schedule constraints

Key insight: PRDs structure requirements hierarchically using **themes** (high-level strategic goals spanning years), **initiatives/epics** (large-scale projects), and **features/user stories** (specific functionalities). This hierarchy maps naturally to roadmap phases.

**Relation to our codebase:** Our extraction pipeline currently works with TDD/spec inputs that describe *what* to build technically. PRD sections like personas, success metrics, and prioritization constraints provide the *why* layer that can enrich phase ordering without changing the technical content of phases.

### 1.2 AI-Assisted PRD Processing (2025-2026 Patterns)

**Source:** [Chisel - How to Write PRD Using AI](https://chisellabs.com/blog/how-to-write-prd-using-ai/)
**Source:** [Kuse.ai - PRD Document Template 2025](https://www.kuse.ai/blog/tutorials/prd-document-template-in-2025-how-to-write-effective-product-requirements)
**Reliability:** MEDIUM (newer tooling vendors, but reflects current practice)
**Relevance:** MEDIUM

AI tools now help product managers auto-generate first drafts, summarize user feedback, and suggest requirements based on customer data. This validates our approach of using LLM pipelines to process PRD content alongside TDD specs.

**Relation to our codebase:** Supports the `--prd-file` supplementary input approach. PRDs are increasingly machine-parseable, making LLM extraction of business context (personas, JTBD, KPIs) feasible as a pipeline step.

---

## 2. Value-Based Prioritization Frameworks

### 2.1 RICE Framework (Intercom)

**Source:** [Fygurs - Prioritization Frameworks Compared](https://www.fygurs.com/blog/product-prioritization-frameworks-compared)
**Source:** [Centercode - RICE vs WSJF](https://www.centercode.com/blog/rice-vs-wsjf-prioritization-framework)
**Source:** [Atlassian - Prioritization Frameworks](https://www.atlassian.com/agile/product-management/prioritization-framework)
**Reliability:** HIGH (Atlassian, established PM practice)
**Relevance:** HIGH

**RICE** = (Reach x Impact x Confidence) / Effort

- **Reach**: How many users/customers affected in a time period
- **Impact**: How much each user is affected (scale: 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
- **Confidence**: How confident in estimates (100%=high, 80%=medium, 50%=low)
- **Effort**: Person-months of engineering work

Best for: Ranking 20-50 features at team level. Quarterly scoring using product analytics for reach, user research for impact, engineering assessments for effort.

**Relation to our codebase:** RICE directly maps to PRD-enriched roadmapping. Reach and Impact come from PRD personas/KPIs. Effort comes from TDD complexity. Confidence is assessable from both sources. Our scoring pipeline could incorporate RICE dimensions as supplementary scoring signals.

### 2.2 WSJF Framework (SAFe)

**Source:** [PPM Express - 13 Prioritization Techniques](https://www.ppm.express/blog/13-prioritization-techniques)
**Source:** [Nauka Online - Comparative Analysis](https://nauka-online.com/en/publications/economy/2025/9/06-29/)
**Reliability:** HIGH (SAFe is widely adopted enterprise framework)
**Relevance:** HIGH

**WSJF** = (User-Business Value + Time Criticality + Risk Reduction) / Job Duration

- **User-Business Value**: Revenue, customer satisfaction, market share impact
- **Time Criticality**: Urgency, competitive pressure, regulatory deadlines
- **Risk Reduction / Opportunity Enablement**: Technical debt reduction, platform capabilities
- **Job Duration**: Engineering effort in sprints/weeks

Best for: Portfolio-level prioritization in large organizations (50+ in product).

**Relation to our codebase:** WSJF is the strongest candidate for PRD-enriched scoring because its numerator components (User-Business Value, Time Criticality, Risk Reduction) are **exactly** the business context we'd extract from PRDs. Job Duration maps to our existing complexity assessment from TDD specs. This framework provides a principled way to combine PRD business signals with TDD technical signals.

### 2.3 MoSCoW Method

**Source:** [AltexSoft - Popular Prioritization Techniques](https://www.altexsoft.com/blog/most-popular-prioritization-techniques-and-methods-moscow-rice-kano-model-walking-skeleton-and-others/)
**Source:** [Plane - Feature Prioritization Frameworks](https://plane.so/blog/feature-prioritization-frameworks-rice-moscow-and-kano-explained)
**Reliability:** HIGH (well-established method)
**Relevance:** MEDIUM

**MoSCoW** = Must-have / Should-have / Could-have / Won't-have (for now)

Best for: Release scope negotiation within sprints. Product manager classifies sprint items, giving the team clear guidance on what to cut if they run out of time.

**Relation to our codebase:** MoSCoW is less quantitative than RICE/WSJF but useful for the **phasing** step. PRD "must-have" requirements should cluster into earlier phases; "could-have" items into later phases. Our phase generation could use MoSCoW as a constraint: items in Phase 1 must not include any "Could-have" or "Won't-have" items from the PRD.

### 2.4 Layered Framework Usage (Key Pattern)

**Source:** [ProductLift - 10 Prioritization Frameworks 2026](https://www.productlift.dev/blog/product-prioritization-framework)
**Source:** [Product School - 9 Prioritization Frameworks](https://productschool.com/blog/product-fundamentals/ultimate-guide-product-prioritization)
**Reliability:** HIGH
**Relevance:** HIGH

Large organizations layer frameworks: WSJF for portfolio-level, RICE for team-level backlog, MoSCoW for release scope. This pattern validates our approach of using PRD context as a **supplementary scoring signal** rather than replacing the technical scoring.

**Relation to our codebase:** Our scoring pipeline already computes technical scores. PRD enrichment should add a parallel "business value" dimension, not replace technical scoring. The final prioritization should be a weighted combination, with the weighting configurable.

---

## 3. Product Roadmap vs. Engineering Roadmap Boundary

### 3.1 The What/Why vs. How/When Distinction

**Source:** [Fibery - Engineering Roadmap vs Product Roadmap](https://fibery.io/blog/product-management/engineering-roadmap-vs-product-roadmap/)
**Source:** [Amoeboids - Technical vs Product Roadmap](https://amoeboids.com/blog/product-vs-technology-roadmaps-whats-the-difference/)
**Source:** [Aha! - Product Roadmap vs Technology Roadmap](https://www.aha.io/blog/the-product-roadmap-vs-the-technology-roadmap)
**Source:** [LaunchNotes - Technical vs Product Roadmap](https://www.launchnotes.com/blog/technical-roadmap-vs-product-roadmap-understanding-the-differences-and-importance)
**Reliability:** HIGH (established PM/engineering tooling vendors)
**Relevance:** HIGH

The industry consensus on the boundary:

| Dimension | Product Roadmap | Engineering Roadmap |
|-----------|----------------|-------------------|
| Focus | What and Why | How and When |
| Audience | Cross-functional, external stakeholders | Engineering team, technical leads |
| Language | Business/customer-centric, jargon-free | Technical, implementation-specific |
| Timeframe | Quarters to years | Weeks to sprints |
| Content | Strategic themes, customer value, market positioning | Tasks, dependencies, architecture decisions |
| Owner | Product Manager | Engineering Lead / CTO |

Key insight: The two roadmaps are **complementary, like two sides of the same coin**. Features in the technical roadmap feed the product roadmap and determine when features can be released.

**Relation to our codebase:** This validates our design: the engineering roadmap stays technical (How/When), but we inject business context (What/Why) from the PRD to **inform prioritization** without changing the roadmap's nature. The PRD provides the "Why" annotations on phases, not the phases themselves.

### 3.2 Maintaining the Boundary

**Source:** [CloudBees - Prioritizing Technical vs Product Roadmap](https://www.cloudbees.com/blog/prioritizing-technical-roadmap-product-roadmap)
**Source:** [ProductPlan - Engineering Roadmap Guide](https://www.productplan.com/learn/engineering-roadmap/)
**Reliability:** HIGH
**Relevance:** HIGH

Key practices for maintaining separation while sharing context:

1. **Engineers participate in PRD review but don't own it**: Technical feasibility informs product decisions
2. **Business rationale annotates, doesn't dictate, technical ordering**: Technical dependencies still govern sequence
3. **Shared vocabulary through user stories/JTBD**: Bridge between business intent and technical implementation
4. **Dual scoring**: Business value and technical complexity scored independently, combined for final prioritization
5. **Technical debt has its own track**: Infrastructure work lives on the engineering roadmap even without PRD backing

**Relation to our codebase:** This is the exact pattern we need. PRD context should:
- Annotate phases with business rationale (but not restructure phases)
- Provide a business value score that combines with technical complexity
- Never override technical dependency ordering
- Allow pure infrastructure phases to exist without PRD justification

---

## 4. PRD Sections Most Valuable for Engineering Enrichment

### 4.1 JTBD as the Bridge Between PRD and Engineering Roadmap

**Source:** [THRV - JTBD vs Personas Ultimate Guide](https://www.thrv.com/blog/jobs-to-be-done-vs-personas-the-ultimate-guide-to-unified-customer-understanding-in-product-development)
**Source:** [Agile Seekers - JTBD in Tech Product Discovery](https://agileseekers.com/blog/applying-jobs-to-be-done-jtbd-framework-to-tech-product-discovery)
**Source:** [Product School - JTBD Framework](https://productschool.com/blog/product-fundamentals/jtbd-framework)
**Source:** [THRV - 7 Steps to Improve Planning with JTBD](https://www.thrv.com/blog/7-steps-to-improve-annual-planning-with-jobs-to-be-done)
**Reliability:** HIGH (JTBD is an established framework from Tony Ulwick / Strategyn)
**Relevance:** HIGH

JTBD begins with what customers are trying to accomplish (the "job"), not who customers are (the "persona"). This distinction is critical for engineering roadmap enrichment:

- **JTBD is a decision tool** with evidence-backed situations, motivations, and outcomes that drive roadmaps, specs, and metrics
- **Personas are communication tools** that provide role, context, and shared language
- **Both are valuable** but serve different purposes in the pipeline

For feature prioritization, each potential feature should be evaluated by how it helps different personas accomplish their primary jobs. Features that enable multiple personas to complete high-importance jobs get prioritization.

**PRD sections ranked by engineering roadmap value:**

| PRD Section | Engineering Value | What It Provides |
|------------|------------------|-----------------|
| JTBD / User Stories | HIGH | Prioritization signal -- which features unlock the most user jobs |
| Success Metrics / KPIs | HIGH | Measurable targets for phasing -- what moves the needle |
| Personas | MEDIUM | Context for API/UX priority -- who uses what |
| Compliance / Regulatory | HIGH | Hard constraints on phase ordering -- non-negotiable sequencing |
| Business Model / Revenue | MEDIUM | Revenue-weighted prioritization signal |
| Market Positioning | LOW | Strategic context, rarely changes technical ordering |
| Stakeholder Map | LOW | Communication context, not engineering-relevant |

**Relation to our codebase:** The PRD extraction step should prioritize JTBD, KPIs, compliance requirements, and personas in that order. Market positioning and stakeholder maps can be ignored for engineering roadmap purposes. This gives us a focused extraction target rather than parsing the entire PRD.

### 4.2 Dual-Track Agile as Organizational Pattern

**Source:** [Productboard - Dual-Track Agile](https://www.productboard.com/glossary/dual-track-agile/)
**Source:** [SVPG - Dual-Track Agile](https://www.svpg.com/dual-track-agile/)
**Source:** [Lumenalta - Build Less Deliver More](https://lumenalta.com/insights/build-less-deliver-more-the-case-for-dual-track-agile)
**Source:** [Jeff Patton - Dual Track Development](https://jpattonassociates.com/dual-track-development/)
**Reliability:** HIGH (SVPG/Marty Cagan is authoritative in product management)
**Relevance:** MEDIUM

Dual-track agile divides work into Discovery (validate what to build) and Delivery (build it). The key insight for our pipeline:

- **Discovery track** produces validated backlog items (PRD content = validated requirements)
- **Delivery track** consumes validated items (engineering roadmap = delivery plan)
- The tracks sync through shared rituals and a common backlog

Engineers get "well-informed, user-validated stories" rather than "loosely defined specs or shifting requirements."

**Relation to our codebase:** Our `--prd-file` flag is essentially the interface between discovery and delivery tracks. The PRD represents validated discovery output. The roadmap pipeline represents delivery planning. The PRD enrichment step bridges the two tracks programmatically.

---

## 5. Supplementary Context Injection in LLM Pipelines

### 5.1 Context Engineering Patterns (2025-2026)

**Source:** [Prompt Engineering Guide - Context Engineering](https://www.promptingguide.ai/guides/context-engineering-guide)
**Source:** [Deepset - Context Engineering: Next Frontier](https://www.deepset.ai/blog/context-engineering-the-next-frontier-beyond-prompt-engineering)
**Source:** [Addy Osmani - Context Engineering](https://addyo.substack.com/p/context-engineering-bringing-engineering)
**Reliability:** HIGH (established AI/ML engineering sources)
**Relevance:** HIGH

Context engineering has emerged as the successor to prompt engineering. Key principles:

1. **Structured context injection**: Use prompt templates with placeholders for supplementary documents. Structuring external knowledge as bullet points or Q&A pairs is more effective than dumping long paragraphs
2. **Signal-to-noise ratio**: Maintain high relevance in injected context. NotebookLM-style document synthesis helps
3. **Multi-stage pipelines**: Raw inputs undergo initial analysis, chunking, and structured representation before being surfaced to the LLM
4. **Retrieval + Synthesis**: Documents are processed into structured representations, then selectively injected based on relevance to the current generation step

### 5.2 Multi-Document Pipeline Architecture

**Source:** [arXiv - Context Engineering for Multi-Agent LLM Code Assistants](https://arxiv.org/html/2508.08322v1)
**Source:** [APXML - Context Injection Methods](https://apxml.com/courses/getting-started-rag/chapter-4-rag-generation-augmentation/context-injection-methods)
**Reliability:** HIGH (academic paper + established course material)
**Relevance:** HIGH

A validated multi-document context pipeline:

1. **Intent Translator**: Clarifies user requirements (in our case: parse the TDD spec)
2. **Semantic Retrieval**: Injects domain knowledge (in our case: extract PRD business context)
3. **Document Synthesis**: Contextual understanding (in our case: merge TDD + PRD signals)
4. **Multi-Agent Generation**: Code generation and validation (in our case: variant generation, debate, scoring)

Key pattern: **Supplementary documents should be pre-processed into structured summaries** before injection into the main generation pipeline. Raw PRD text should not be passed directly; instead, extract and structure the relevant fields first.

**Relation to our codebase:** This maps directly to our pipeline architecture:

| Pipeline Step | Current (TDD-only) | With PRD Enrichment |
|--------------|--------------------|--------------------|
| Extract | Parse TDD spec sections | Parse TDD + Extract PRD business context |
| Generate Variants | Technical variants only | Variants informed by business priorities |
| Diff / Debate | Technical merit debate | Technical + business value debate |
| Score | Technical complexity score | Combined technical + business value score |
| Merge | Best technical approach | Best approach weighted by business impact |
| Validate | Spec fidelity check | Spec + PRD fidelity check |

The PRD extraction should produce a **structured summary** (not raw text) containing:
- Extracted JTBD list with priority weights
- KPI targets with measurability indicators
- Compliance/regulatory hard constraints
- Persona-feature mappings
- MoSCoW classification of requirements

This structured summary is then injected into the prompt at each pipeline step as supplementary context.

---

## Key External Findings

### Finding 1: WSJF is the best-fit framework for PRD-enriched scoring
WSJF's numerator (User-Business Value + Time Criticality + Risk Reduction) maps exactly to PRD business context, while its denominator (Job Duration) maps to existing TDD complexity scores. This provides a principled, industry-standard formula for combining business and technical signals. RICE is a strong alternative for team-level prioritization.

### Finding 2: PRD extraction should target 4 high-value sections, not the entire document
Ranked by engineering roadmap value: (1) JTBD/User Stories, (2) Success Metrics/KPIs, (3) Compliance/Regulatory constraints, (4) Personas. Market positioning, stakeholder maps, and business model sections provide diminishing returns for engineering prioritization.

### Finding 3: The product/engineering roadmap boundary is well-defined in industry
Product roadmap = What/Why (business-facing, quarterly+). Engineering roadmap = How/When (team-facing, sprint-level). PRD context should **annotate** engineering phases with business rationale, not restructure them. Technical dependency ordering must never be overridden by business priority.

### Finding 4: Supplementary documents must be pre-processed before injection
Raw PRD text should not be passed into generation prompts. Industry best practice is to extract and structure relevant fields into a compact, typed summary that is injected at each pipeline step. This maintains signal-to-noise ratio and avoids context window pollution.

### Finding 5: Layered prioritization is the norm in mature organizations
Teams layer WSJF (portfolio), RICE (team backlog), MoSCoW (release scope). Our PRD enrichment is analogous to adding the portfolio-level business signal to the team-level technical signal. The two should be scored independently and combined via configurable weighting.

### Finding 6: Dual-track agile validates the `--prd-file` pattern
The PRD file represents validated "discovery" output. The roadmap pipeline represents "delivery" planning. The `--prd-file` flag is the programmatic bridge between discovery and delivery tracks, consistent with how product-led engineering teams operate.

---

## Recommendations from External Research

### R1: Implement PRD extraction as a structured pre-processing step
Add a new `prd_extract` step (or sub-step of the existing `extract` step) that parses the PRD file and produces a `PRDContext` dataclass containing: JTBD list, KPI targets, compliance constraints, persona-feature mappings, and MoSCoW classifications. This structured object -- not raw text -- gets injected into subsequent pipeline prompts.

### R2: Add WSJF-inspired business value scoring
Extend the scoring model to include a `business_value_score` computed from PRD signals:
- `user_business_value`: Derived from JTBD importance and persona reach
- `time_criticality`: Derived from compliance deadlines and market timing
- `risk_reduction`: Derived from regulatory requirements and platform enablement

The combined score = `(technical_score * tech_weight) + (business_value_score * biz_weight)` where weights are configurable (default: 0.6 tech, 0.4 biz).

### R3: Use MoSCoW as a phase constraint
PRD MoSCoW classifications should act as constraints on phase generation:
- Phase 1: Must-have items only
- Phase 2: Must-have + Should-have items
- Phase 3+: Could-have items allowed
- Won't-have items excluded from all phases

This does not override technical dependency ordering but provides business-driven bounds.

### R4: Annotate phases with business rationale
Each roadmap phase should optionally include a `business_rationale` field populated from PRD context. This provides the "Why" without changing the technical "How/When." Infrastructure phases without PRD backing should be annotated as "Technical Foundation" rather than flagged as gaps.

### R5: Keep PRD enrichment strictly optional
The `--prd-file` flag should be fully optional. All pipeline steps must work identically without it. When absent, business value scores default to neutral (1.0) so technical scoring dominates. This ensures backward compatibility and matches the supplementary-input design intent.

### R6: Pre-process PRD into bullet-point summaries per pipeline step
Rather than injecting the full PRD context at every step, tailor the injection:
- **Extract step**: Full PRD context for comprehensive parsing
- **Variant generation**: JTBD + KPI summaries only (what outcomes matter)
- **Debate step**: Business value arguments alongside technical arguments
- **Scoring step**: Quantified WSJF components
- **Validation step**: PRD fidelity checklist (did phases cover all must-have JTBD?)

---

## Sources Index

All sources used in this research, grouped by section:

**Section 1 - PRD Structure:**
- https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template
- https://www.perforce.com/blog/alm/how-write-product-requirements-document-prd
- https://www.productboard.com/blog/product-requirements-document-guide/
- https://chisellabs.com/blog/how-to-write-prd-using-ai/
- https://www.kuse.ai/blog/tutorials/prd-document-template-in-2025-how-to-write-effective-product-requirements

**Section 2 - Prioritization Frameworks:**
- https://www.fygurs.com/blog/product-prioritization-frameworks-compared
- https://www.centercode.com/blog/rice-vs-wsjf-prioritization-framework
- https://www.atlassian.com/agile/product-management/prioritization-framework
- https://www.ppm.express/blog/13-prioritization-techniques
- https://nauka-online.com/en/publications/economy/2025/9/06-29/
- https://www.altexsoft.com/blog/most-popular-prioritization-techniques-and-methods-moscow-rice-kano-model-walking-skeleton-and-others/
- https://plane.so/blog/feature-prioritization-frameworks-rice-moscow-and-kano-explained
- https://www.productlift.dev/blog/product-prioritization-framework
- https://productschool.com/blog/product-fundamentals/ultimate-guide-product-prioritization

**Section 3 - Roadmap Boundary:**
- https://fibery.io/blog/product-management/engineering-roadmap-vs-product-roadmap/
- https://amoeboids.com/blog/product-vs-technology-roadmaps-whats-the-difference/
- https://www.aha.io/blog/the-product-roadmap-vs-the-technology-roadmap
- https://www.launchnotes.com/blog/technical-roadmap-vs-product-roadmap-understanding-the-differences-and-importance
- https://www.cloudbees.com/blog/prioritizing-technical-roadmap-product-roadmap
- https://www.productplan.com/learn/engineering-roadmap/

**Section 4 - JTBD and Dual-Track:**
- https://www.thrv.com/blog/jobs-to-be-done-vs-personas-the-ultimate-guide-to-unified-customer-understanding-in-product-development
- https://agileseekers.com/blog/applying-jobs-to-be-done-jtbd-framework-to-tech-product-discovery
- https://productschool.com/blog/product-fundamentals/jtbd-framework
- https://www.thrv.com/blog/7-steps-to-improve-annual-planning-with-jobs-to-be-done
- https://www.productboard.com/glossary/dual-track-agile/
- https://www.svpg.com/dual-track-agile/
- https://lumenalta.com/insights/build-less-deliver-more-the-case-for-dual-track-agile
- https://jpattonassociates.com/dual-track-development/

**Section 5 - LLM Context Injection:**
- https://www.promptingguide.ai/guides/context-engineering-guide
- https://www.deepset.ai/blog/context-engineering-the-next-frontier-beyond-prompt-engineering
- https://addyo.substack.com/p/context-engineering-bringing-engineering
- https://arxiv.org/html/2508.08322v1
- https://apxml.com/courses/getting-started-rag/chapter-4-rag-generation-augmentation/context-injection-methods
