# v3.8 RigorFlow Merger — Tasklist Analysis Package

**Generated**: 2026-04-02
**Purpose**: Complete architectural analysis of SC tasklist/adversarial and RF taskbuilder/pipeline systems for the v3.8 RigorFlow merger initiative.
**Source repos**: SuperClaude (`/config/.claude/`), llm-workflows (`/config/workspace/llm-workflows/`)
**Status**: Analysis complete. Start with [FINAL-REPORT.md](FINAL-REPORT.md).

---

## Documents

### 0. [FINAL REPORT](FINAL-REPORT.md) **(start here)**
Complete synthesis: executive summary, method, framework internals with source-line citations, comparative matrix, proposal portfolio, adversarial outcomes, final refactor plan (5 changes, ~110 lines), phased implementation sequencing with test plans, open risks and assumptions. Every major claim cites source file evidence. Facts and inferences explicitly distinguished.

### 1. [File Inventory](file-inventory.md)
Exhaustive inventory of every file participating in both frameworks, grouped by category. **20 SC static files** across commands, skill packages, and Python CLI modules. **58 RF static files** across commands, agents, templates, scripts, rules, and prompts. Plus ~14 runtime artifacts per RF batch execution. Includes line counts, sizes, and one-line purpose descriptions for each file.

### 2. [Dependency Map](dependency-map.md)
Full dependency chains showing how commands invoke protocols, protocols invoke agents, and agents produce artifacts. ASCII tree diagrams for `/sc:tasklist` (command → skill → generation stages → validation), `/sc:adversarial` (command → skill → 5-step pipeline → return contract), `superclaude tasklist validate` (Python CLI → gate criteria → fidelity report), and `/rf:pipeline` (command → team → researcher → builder → executor → `automated_qa_workflow.sh` inner loop). Includes cross-framework integration map.

### 3. [Pipeline Stages](pipeline-stages.md)
Stage-by-stage pipeline diagrams with full technical detail. SC tasklist: 10 stages with deterministic algorithms for parsing, phase bucketing, task conversion, tier scoring, registry assembly, file emission, drift detection, patching, and validation. SC adversarial: 5-step protocol with variant generation, diff analysis, multi-round debate (L1/L2/L3 taxonomy), hybrid scoring (quantitative + qualitative), and merge execution. RF pipeline: 9 outer phases + 10 inner sub-stages per batch, including PABLOV evidence collection, DNSP recovery, correction loops, and session management. Includes batch state machine diagram and session lifecycle model.

### 4. [Architecture Comparison](architecture-comparison.md)
Side-by-side tables across 8 dimensions: execution architecture, control flow & gating, agent delegation model, validation & self-check model, artifact schema & output contracts, error handling & fallback behavior, determinism guarantees, and throughput & token/cost drivers. Concludes with cross-framework strengths analysis and 5 convergence opportunities for the merger.

### 5. [Design: RF Merger Proposals](design-rfmerger-proposals.md) **(primary deliverable)**
Strengths/weaknesses matrix (7 SC strengths, 6 SC weaknesses, 6 RF strengths, 5 RF weaknesses). Compatibility map rating each RF strength for import effort (Low/Medium/High/N/A). **5 refactor proposals** with exact file locations, borrowed RF mechanisms, quality/complexity/speed/cost/risk analysis, and rollback strategies. Prioritized adoption roadmap in 3 phases (quick wins → core improvements → long-term evolution) with dependency graph. Includes before/after examples for each proposal.

### 6. [Adversarial Validation](adversarial-validation.md) **(Phase 4 output)**
5 parallel adversarial agents validated each proposal against baseline and conservative alternatives across 5 focus areas. Results: 1 ADOPT (P3), 4 REVISE. Consolidated scoring matrices, debate outcomes, unresolved conflicts, refactored proposals, and revised priority roadmap. **Net complexity reduced 45%** from pre-adversarial estimates (200+ lines → 110 lines). Key pattern: 4/5 original proposals were over-engineered; conservative alternatives delivered 70-90% of value at 10-30% of complexity.

### 7. [Strategy: LW Task Builder](strategy-lw-task-builder.md) *(pre-existing)*
Prior analysis of the RF task builder component, covering rigor mechanisms (self-contained items, session rollover protection, completion gates), bloat/cost concerns (context duplication, 3-stage interview overhead), and merge considerations.

---

## Proposal Summary (Post-Adversarial)

| # | Proposal | Pre-Adversarial | Post-Adversarial | Verdict | Effort | Risk |
|---|----------|----------------|------------------|---------|--------|------|
| P3 | DNSP for Validation Agents | ~20 lines | ~25 lines (+guards) | **ADOPT** | Very Low | Very Low |
| P1 | Context-Armed Steps | Per-step template | Per-task block | **REVISE** | Low | Low |
| P2 | Bounded Patch Loop | Auto loop (3 passes) | Human checkpoint + guarded auto | **REVISE** | Low | Low |
| P4 | Evidence-Anchored Validation | New Stage 6.5 + JSON | Gate results passthrough | **REVISE** | Very Low | Very Low |
| P5 | Feedback-Driven Tier Calibration | Auto tier modification | Read-only advisory | **REVISE** | Low | Low |

---

## Key Numbers

| Metric | SC Tasklist | SC Adversarial | RF Pipeline |
|--------|------------|----------------|-------------|
| Static file count | 20 | (included in 20) | 58 |
| Protocol/skill size | 51KB | 123KB | 5,997 lines (main script) |
| Typical LLM calls | 2-4 | 8-35+ | 9-25+ |
| Typical token consumption | 50-80K | 200-400K | 500K-1M+ |
| Typical wall-clock | 2-15 min | 3-60 min | 15-45 min (per task) |
| Determinism level | Full (generation) | Partial (formulas) | Structural only |
| Max parallel agents | 0 | 10 | 15 (5 tracks × 3) |
| Correction capability | 1 pass (patch+spot-check) | None (debate IS correction) | 5 cycles per batch |

## Convergence Opportunities for v3.8

1. **SC tier classification → RF task enrichment**: RF tasks currently have no compliance tier. SC's deterministic STRICT/STANDARD/LIGHT/EXEMPT classification with confidence scoring could drive verification routing in RF execution
2. **RF PABLOV evidence → SC validation strengthening**: SC Stages 7-10 use LLM-only drift detection. RF's filesystem snapshots, conversation mining, and programmatic handoffs provide machine-verifiable evidence that could make SC validation more robust
3. **SC adversarial → RF opinion upgrade**: RF's `/rf:opinion` is a simple anti-sycophancy tool. SC adversarial's multi-model steelman debate is a much more powerful accuracy mechanism
4. **RF session management → SC Pipeline Mode resilience**: SC Pipeline Mode has manifest-based resume but no session recovery. RF's dual-threshold rollover, batch state persistence, and DNSP protocol handle real-world failures
5. **SC traceability → RF task lineage**: RF tasks have no formal traceability from requirements to deliverables. SC's R-### → T<PP>.<TT> → D-#### matrix could provide this
