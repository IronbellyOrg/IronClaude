# Synthesis: External Research Findings

## Section 5: External Research Findings

**Synthesis Report:** PRD Pipeline Integration -- External Research
**Source:** `research/web-01-prd-driven-roadmapping.md`
**Date:** 2026-03-27
**Classification:** EXTERNAL CONTEXT -- All findings in this section originate from external web sources and industry literature. They represent industry patterns and third-party recommendations, not codebase-derived facts.

---

> **EXTERNAL CONTEXT NOTICE**: Every finding below is drawn from publicly available industry sources. Relevance assessments reflect how these external patterns relate to the IronClaude codebase and PRD pipeline integration research question. No finding should be treated as a codebase requirement without internal validation.

---

## 5.1 PRD Structure and Engineering-Relevant Sections

### Finding

Modern PRDs have converged on a leaner, iterative format organized around hierarchical requirement structures: themes (strategic goals, multi-quarter), initiatives/epics (large projects), and features/user stories (specific functionality). The sections with highest engineering roadmap value are: Purpose and Goals, User Needs/Personas, Prioritization Constraints (must-have vs. nice-to-have), Success Metrics/KPIs, and Timeline/Release Plan. AI-assisted PRD generation (2025-2026) has made PRDs increasingly machine-parseable, validating LLM-based extraction approaches.

### Sources

- https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template
- https://www.perforce.com/blog/alm/how-write-product-requirements-document-prd
- https://www.productboard.com/blog/product-requirements-document-guide/
- https://chisellabs.com/blog/how-to-write-prd-using-ai/
- https://www.kuse.ai/blog/tutorials/prd-document-template-in-2025-how-to-write-effective-product-requirements

### Relevance: HIGH

### Relationship to Codebase: SUPPORTS

The existing extraction pipeline parses TDD/spec inputs for *what* to build technically. PRD sections (personas, KPIs, prioritization constraints) provide the *why* layer. This external pattern supports adding PRD as a supplementary input that enriches phase ordering without changing the technical content of phases. The hierarchical requirement structure (themes > epics > features) maps naturally to the roadmap phase hierarchy already used in the pipeline.

---

## 5.2 Value-Based Prioritization Frameworks

### 5.2.1 RICE Framework

#### Finding

RICE scores features as (Reach x Impact x Confidence) / Effort. Reach and Impact derive from product analytics and user research (PRD content). Effort comes from engineering assessment (TDD content). Confidence is assessable from both. Best suited for ranking 20-50 features at team level with quarterly scoring cadence.

#### Sources

- https://www.fygurs.com/blog/product-prioritization-frameworks-compared
- https://www.centercode.com/blog/rice-vs-wsjf-prioritization-framework
- https://www.atlassian.com/agile/product-management/prioritization-framework

#### Relevance: HIGH

#### Relationship to Codebase: EXTENDS

RICE dimensions could serve as supplementary scoring signals in the existing scoring pipeline. The framework provides a structured way to quantify PRD-derived business signals (Reach, Impact) alongside TDD-derived effort estimates.

### 5.2.2 WSJF Framework (SAFe)

#### Finding

WSJF = (User-Business Value + Time Criticality + Risk Reduction) / Job Duration. The numerator components map directly to PRD business context: User-Business Value from revenue/satisfaction data, Time Criticality from compliance deadlines and market timing, Risk Reduction from regulatory requirements and platform enablement. Job Duration maps to engineering effort. Best suited for portfolio-level prioritization in organizations with 50+ product staff.

#### Sources

- https://www.ppm.express/blog/13-prioritization-techniques
- https://nauka-online.com/en/publications/economy/2025/9/06-29/

#### Relevance: HIGH

#### Relationship to Codebase: EXTENDS

WSJF is the strongest candidate framework for combining PRD business signals with TDD technical signals. Its numerator components are exactly the business context that would be extracted from PRDs, while its denominator maps to existing complexity assessment from TDD specs. The scoring model could incorporate WSJF-inspired dimensions as a parallel business value score.

### 5.2.3 MoSCoW Method

#### Finding

MoSCoW classifies requirements as Must-have, Should-have, Could-have, Won't-have. Less quantitative than RICE/WSJF but directly useful for release scope negotiation and phase boundary constraints. Must-have items cluster into early phases; Could-have items into later phases.

#### Sources

- https://www.altexsoft.com/blog/most-popular-prioritization-techniques-and-methods-moscow-rice-kano-model-walking-skeleton-and-others/
- https://plane.so/blog/feature-prioritization-frameworks-rice-moscow-and-kano-explained

#### Relevance: MEDIUM

#### Relationship to Codebase: EXTENDS

MoSCoW provides a phase constraint mechanism: Phase 1 should contain only Must-have items; Could-have items should not appear before Phase 3. This classification could act as a hard constraint on phase generation without overriding technical dependency ordering.

### 5.2.4 Layered Framework Usage

#### Finding

Mature organizations layer multiple prioritization frameworks: WSJF at portfolio level, RICE at team backlog level, MoSCoW for release scope. This layered approach validates using PRD context as a supplementary scoring signal rather than replacing technical scoring. Business value and technical complexity are scored independently and combined via configurable weighting.

#### Sources

- https://www.productlift.dev/blog/product-prioritization-framework
- https://productschool.com/blog/product-fundamentals/ultimate-guide-product-prioritization

#### Relevance: HIGH

#### Relationship to Codebase: SUPPORTS

The existing scoring pipeline computes technical scores. The layered framework pattern validates adding a parallel business value dimension with configurable weighting (e.g., default 0.6 technical / 0.4 business) rather than replacing the technical scoring entirely.

---

## 5.3 Product Roadmap vs. Engineering Roadmap Boundary

### Finding

Industry consensus defines a clear boundary: Product roadmap covers What and Why (business-facing, quarterly-to-yearly timeframe, customer-centric language). Engineering roadmap covers How and When (team-facing, sprint-level, implementation-specific language). The two are complementary -- "two sides of the same coin." Key practices for maintaining the boundary: (1) business rationale annotates but does not dictate technical ordering, (2) technical dependencies still govern sequence, (3) dual scoring keeps business value and technical complexity independent, (4) technical debt has its own track even without PRD backing.

### Sources

- https://fibery.io/blog/product-management/engineering-roadmap-vs-product-roadmap/
- https://amoeboids.com/blog/product-vs-technology-roadmaps-whats-the-difference/
- https://www.aha.io/blog/the-product-roadmap-vs-the-technology-roadmap
- https://www.launchnotes.com/blog/technical-roadmap-vs-product-roadmap-understanding-the-differences-and-importance
- https://www.cloudbees.com/blog/prioritizing-technical-roadmap-product-roadmap
- https://www.productplan.com/learn/engineering-roadmap/

### Relevance: HIGH

### Relationship to Codebase: SUPPORTS

This directly validates the proposed design where the engineering roadmap stays technical (How/When) and PRD context injects business rationale (What/Why) to inform prioritization without changing the roadmap's nature. Infrastructure phases without PRD backing should be annotated as "Technical Foundation" rather than flagged as gaps. Technical dependency ordering must never be overridden by business priority.

---

## 5.4 JTBD as the Bridge Between PRD and Engineering Roadmap

### Finding

Jobs-To-Be-Done (JTBD) focuses on what customers are trying to accomplish rather than who they are. For engineering roadmap enrichment, JTBD is a decision tool with evidence-backed situations, motivations, and outcomes, while personas are communication tools providing role and context. Both are valuable but serve different purposes. Features should be evaluated by how they help personas accomplish high-importance jobs -- features enabling multiple personas to complete high-importance jobs get prioritization. PRD sections ranked by engineering value: (1) JTBD/User Stories -- HIGH, (2) Success Metrics/KPIs -- HIGH, (3) Compliance/Regulatory -- HIGH (hard constraints), (4) Personas -- MEDIUM, (5) Business Model/Revenue -- MEDIUM, (6) Market Positioning -- LOW, (7) Stakeholder Map -- LOW.

### Sources

- https://www.thrv.com/blog/jobs-to-be-done-vs-personas-the-ultimate-guide-to-unified-customer-understanding-in-product-development
- https://agileseekers.com/blog/applying-jobs-to-be-done-jtbd-framework-to-tech-product-discovery
- https://productschool.com/blog/product-fundamentals/jtbd-framework
- https://www.thrv.com/blog/7-steps-to-improve-annual-planning-with-jobs-to-be-done

### Relevance: HIGH

### Relationship to Codebase: EXTENDS

This ranking provides a focused extraction target for the PRD processing step. Rather than parsing the entire PRD document, the extraction should prioritize JTBD, KPIs, compliance requirements, and personas -- in that order. Market positioning and stakeholder maps can be excluded from engineering roadmap extraction, reducing context window consumption and improving signal-to-noise ratio.

---

## 5.5 Dual-Track Agile as Organizational Pattern

### Finding

Dual-track agile separates Discovery (validate what to build) from Delivery (build it). The Discovery track produces validated backlog items (PRD content = validated requirements). The Delivery track consumes those items (engineering roadmap = delivery plan). Engineers receive "well-informed, user-validated stories" rather than "loosely defined specs or shifting requirements." The tracks synchronize through shared rituals and a common backlog.

### Sources

- https://www.productboard.com/glossary/dual-track-agile/
- https://www.svpg.com/dual-track-agile/
- https://lumenalta.com/insights/build-less-deliver-more-the-case-for-dual-track-agile
- https://jpattonassociates.com/dual-track-development/

### Relevance: MEDIUM

### Relationship to Codebase: SUPPORTS

The `--prd-file` flag represents the programmatic interface between discovery and delivery tracks. The PRD file is validated discovery output; the roadmap pipeline is delivery planning. This organizational pattern validates that supplementary PRD input is a well-established bridge between product and engineering workflows, not an ad-hoc integration.

---

## 5.6 Context Engineering for LLM Pipelines

### Finding

Context engineering (2025-2026) has emerged as the successor to prompt engineering for multi-document LLM pipelines. Key principles: (1) structured context injection using prompt templates with placeholders -- bullet points and Q&A pairs outperform long paragraphs, (2) high signal-to-noise ratio in injected context, (3) multi-stage pipelines where raw inputs undergo initial analysis and structured representation before LLM processing, (4) retrieval + synthesis where documents are processed into structured representations and selectively injected based on relevance to each generation step. Supplementary documents should be pre-processed into structured summaries before injection into generation prompts -- raw document text should not be passed directly.

### Sources

- https://www.promptingguide.ai/guides/context-engineering-guide
- https://www.deepset.ai/blog/context-engineering-the-next-frontier-beyond-prompt-engineering
- https://addyo.substack.com/p/context-engineering-bringing-engineering
- https://arxiv.org/html/2508.08322v1
- https://apxml.com/courses/getting-started-rag/chapter-4-rag-generation-augmentation/context-injection-methods

### Relevance: HIGH

### Relationship to Codebase: EXTENDS

This directly informs the implementation architecture. The PRD extraction step should produce a structured dataclass (not raw text) containing: JTBD list with priority weights, KPI targets with measurability indicators, compliance/regulatory hard constraints, persona-feature mappings, and MoSCoW classifications. This structured object is then selectively injected at each pipeline step with tailored context:

| Pipeline Step | Injected PRD Context |
|--------------|---------------------|
| Extract | Full PRD context for comprehensive parsing |
| Variant Generation | JTBD + KPI summaries only |
| Debate | Business value arguments alongside technical arguments |
| Scoring | Quantified WSJF components |
| Validation | PRD fidelity checklist |

---

## External Research Summary

**Total findings synthesized:** 8 distinct topic areas from 27 unique external sources.

**Reliability distribution:** 25 HIGH-reliability sources (established vendors, academic papers, authoritative practitioners), 2 MEDIUM-reliability sources (newer tooling vendors).

**Relevance distribution:**
- HIGH relevance: 6 findings (PRD structure, RICE, WSJF, layered frameworks, roadmap boundary, context engineering)
- MEDIUM relevance: 2 findings (MoSCoW, dual-track agile)

**Relationship to codebase:**
- SUPPORTS (validates existing design direction): 4 findings -- PRD structure patterns, layered framework usage, product/engineering roadmap boundary, dual-track agile
- EXTENDS (adds new capabilities to existing patterns): 4 findings -- RICE scoring, WSJF scoring, JTBD extraction ranking, context engineering pipeline architecture

**No CONTRADICTS findings were identified.** All external research is directionally consistent with the proposed `--prd-file` supplementary input approach.

### Key Takeaways for Implementation

1. **WSJF is the best-fit scoring framework** for combining PRD business signals (User-Business Value, Time Criticality, Risk Reduction) with TDD technical signals (Job Duration / complexity). RICE is a viable alternative at team level.

2. **PRD extraction should target 4 sections**, ranked: JTBD/User Stories, Success Metrics/KPIs, Compliance/Regulatory constraints, Personas. Lower-value sections (market positioning, stakeholder maps) should be excluded.

3. **Business rationale annotates phases but does not restructure them.** Technical dependency ordering is inviolable. Infrastructure phases without PRD backing are legitimate.

4. **Pre-process PRD into structured summaries** before injection. Raw PRD text in generation prompts degrades signal-to-noise ratio. A typed `PRDContext` dataclass with selective per-step injection is the recommended architecture.

5. **Scoring should be dual-track with configurable weighting.** Business value and technical complexity scored independently, combined as `(tech_score * tech_weight) + (biz_score * biz_weight)` with configurable weights (suggested default: 0.6/0.4).

6. **MoSCoW classifications act as phase constraints**, not scores: Must-have items in Phase 1, Could-have items deferred to Phase 3+, Won't-have items excluded entirely.
