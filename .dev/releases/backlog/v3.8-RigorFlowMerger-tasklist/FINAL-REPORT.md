# v3.8 RigorFlow Merger — Final Synthesis Report

**Date**: 2026-04-02
**Subject**: Importing RF execution-resilience mechanisms into `sc:tasklist-protocol`
**Status**: Analysis complete. 5 proposals validated. Implementation-ready.

---

## 1. Executive Summary

This report documents a multi-phase analysis of two AI task orchestration frameworks — SuperClaude's `sc:tasklist` (deterministic roadmap-to-tasklist generator) and Rigorflow's RF pipeline (agent-team execution engine) — to identify which RF execution-resilience mechanisms can strengthen `sc:tasklist`'s validation stages without compromising its determinism guarantee.

**Core finding**: RF's strengths lie in *execution resilience* (DNSP recovery, correction loops, PABLOV evidence, session management). SC's strengths lie in *generation determinism* (keyword-based scoring, traceability matrices, quality gates). These are complementary, not competing.

**Five proposals** were designed to import RF mechanisms into SC's validation pipeline (Stages 7-10). Adversarial validation — 5 parallel agents debating each proposal against baseline and conservative alternatives — found that **4 of 5 original proposals were over-engineered**. In each case, a lighter alternative delivered 70-90% of the value at 10-30% of the complexity.

**Final recommended plan**: 5 changes totaling ~110 lines of implementation across 3 phases. No architectural changes to `sc:tasklist-protocol`. All changes are additive to existing stages. Total estimated complexity reduction vs original proposals: 45%.

---

## 2. Method and Files Analyzed

### 2.1 Analysis Phases

| Phase | Method | Output |
|-------|--------|--------|
| 1. Inventory | Exhaustive file discovery via Glob/Grep across both repos | `file-inventory.md` — 78 static files catalogued |
| 2. Architecture | Read all primary source files, extract stage definitions, control flow, gating logic, artifact schemas | `dependency-map.md`, `pipeline-stages.md`, `architecture-comparison.md` |
| 3. Design | Strengths/weaknesses matrix, compatibility mapping, 5 refactor proposals with impact analysis | `design-rfmerger-proposals.md` |
| 4. Adversarial | 5 parallel agents, 3 variants each (baseline/proposed/conservative), quick-depth debate, 5 focus areas | `adversarial-validation.md` |
| 5. Synthesis | Consolidation with source-grounded evidence | This document |

### 2.2 Primary Source Files Analyzed

**SC side** (global config at `/config/.claude/`):

| File | Lines | Role in Analysis |
|------|-------|-----------------|
| `skills/sc-tasklist-protocol/SKILL.md` | 1,151 | Primary target. 10-stage pipeline definition, tier classification algorithm, quality gates, validation stages 7-10 |
| `skills/sc-tasklist-protocol/rules/tier-classification.md` | ~50 | Tier keyword lists, compound phrase overrides, priority order |
| `skills/sc-tasklist-protocol/rules/file-emission-rules.md` | ~40 | N+1 file convention, naming requirements |
| `skills/sc-tasklist-protocol/templates/index-template.md` | ~60 | Index file structure: metadata, registries, traceability matrix |
| `skills/sc-tasklist-protocol/templates/phase-template.md` | ~60 | Phase file structure: 13-field task metadata, steps, acceptance criteria |
| `skills/sc-adversarial-protocol/SKILL.md` | 2,935 | 5-step adversarial pipeline, scoring protocol, return contract |
| `skills/sc-adversarial-protocol/refs/*` | 4 files | Agent specs, artifact templates, debate protocol, scoring protocol |
| `commands/sc/tasklist.md` | 114 | Command wrapper: arg parsing, input validation, TASKLIST_ROOT derivation |
| `commands/sc/adversarial.md` | 167 | Command wrapper: mode parsing, parameter routing |
| `cli/tasklist/*.py` | 6 files | Python CLI: `superclaude tasklist validate` command, fidelity gate, prompts |

**RF side** (llm-workflows repo at `/config/workspace/llm-workflows/`):

| File | Lines | Role in Analysis |
|------|-------|-----------------|
| `commands/rf/taskbuilder.md` | 358 | 3-stage interview, self-contained item synthesis, pre-write validation |
| `commands/rf/pipeline.md` | 897 | 9-phase agent team orchestration, multi-track support, event-driven spawning |
| `agents/rf-task-builder.md` | 368 | Agent version of taskbuilder, template usage rules, handoff patterns |
| `agents/rf-task-researcher.md` | 447 | Codebase exploration, external research, solution research |
| `agents/rf-task-executor.md` | 370 | Workflow execution, progress reporting, error handling |
| `agents/rf-team-lead.md` | ~500 | Team coordination, track state management, message routing |
| `scripts/automated_qa_workflow.sh` | 5,997 | Core engine: batch management, PABLOV evidence, DNSP protocol, correction loops, session management |
| `templates/01_mdtm_template_generic_task.md` | — | Simple task template (PART 1 instructions + PART 2 structure) |
| `templates/02_mdtm_template_complex_task.md` | — | Complex task template with 6 handoff patterns (L1-L6) |
| `rules/core/ib_agent_core.md` | ~1,000 | Core execution principles, Five-step pattern |

**Total**: ~12,000 lines of primary source read and analyzed.

---

## 3. Framework Internals

### 3.1 SC Tasklist — Observed Architecture

**Fact** (SKILL.md:11-13): The protocol is a single-pass deterministic transform. One input (roadmap text) produces one output (multi-file bundle). Post-generation validation is mandatory.

**Fact** (SKILL.md:756-808): A 17-point quality gate runs before any file is written. Checks include structural (contiguous phases, valid IDs), semantic (non-empty fields, unique deliverable IDs, no orphan tasks), and specificity (named artifacts, imperative verbs, no pronoun references).

**Fact** (SKILL.md:816): Write atomicity — "all files are written only after the full bundle passes validation. No partial bundle writes are permitted."

**Fact** (SKILL.md:857-911): Validation Stages 7-10 spawn 2N parallel agents (2 per phase), each comparing a task subset against the source roadmap. Checks: drift, contradictions, omissions, weakened criteria, invented content.

**Fact** (SKILL.md:911): Agent failure handling is "retry once before reporting error." A single agent failure after retry aborts the entire validation stage.

**Fact** (SKILL.md:1005-1021): Stage 9 delegates patching to `sc:task-unified` via the Skill tool. The orchestrator does not apply patches itself.

**Fact** (SKILL.md:1026-1049): Stage 10 spot-checks findings. "Does NOT loop." UNRESOLVED findings are logged but not re-attempted.

**Inference**: The validation pipeline is brittle at the agent-failure boundary. The 2N-agent architecture provides good coverage parallelism but has no graceful degradation path — one flaky agent can void the work of all others.

**Inference**: The single-pass patch+spot-check model assumes patches are correct on first attempt. Given that patches are applied by an LLM-based tool (`sc:task-unified`), this assumption is optimistic.

### 3.2 RF Pipeline — Observed Architecture

**Fact** (automated_qa_workflow.sh:1-20): The script takes a task file, batch size, and max iterations. It orchestrates two Claude Code subprocess types: workers (create/modify files) and QA agents (validate against evidence).

**Fact** (automated_qa_workflow.sh:4234-4266): Session management uses dual-threshold rollover: messages >= 375 OR tokens >= 175K triggers a new session with rollover context.

**Fact** (automated_qa_workflow.sh:2353-2730): PABLOV evidence collection includes: filesystem snapshots before/after worker execution, conversation mining from JSONL, evidence binding to batch items, optional git diff collection.

**Fact** (automated_qa_workflow.sh:4698-4723): DNSP protocol for QA reports: if report missing after QA run, nudge once ("Write QA report now"), then synthesize minimal report from programmatic handoff if nudge fails.

**Fact** (automated_qa_workflow.sh:5377): `max_correction_cycles=5` — up to 5 worker/QA correction cycles per batch.

**Fact** (automated_qa_workflow.sh:4742-4755): Verdict normalization: "FAIL" with 0 failed item bullets is normalized to PASS (catches contradictory QA verdicts).

**Fact** (taskbuilder.md:182-183): "Context loaded in batch 1 will NOT be available in batch 3+. Therefore every checklist item embeds all context it needs." This is the self-contained item innovation.

**Fact** (pipeline.md:97-119): Track splitting criteria: "independent means ALL of these are true: distinct goals, different source files, different outputs, no cross-track output dependencies."

**Inference**: RF's resilience comes from its willingness to synthesize artifacts when agents fail, retry with targeted feedback, and recover from crashes via state files. This comes at a significant token cost (500K-1M+ per task execution vs SC's 50-80K).

**Inference**: RF's self-contained items solve a real problem (context loss across sessions) but at a high verbosity cost (30 copies of the same context reference in a 30-item task).

---

## 4. Comparative Matrix

| Dimension | sc:tasklist | RF pipeline | Source |
|-----------|------------|-------------|--------|
| **Determinism** | Full: same roadmap → same output. Keyword-based scoring, appearance-order IDs, explicit tiebreakers | None at generation level. Structural only at execution (batch numbering, UID tracking) | SKILL.md:30-43 vs pipeline.md (inherent to agent exploration model) |
| **Generation stages** | 10 (6 generation + 4 validation) | 9 outer phases + 10 inner sub-stages per batch | SKILL.md:122-1050 vs automated_qa_workflow.sh full file |
| **Quality gates** | 17-point pre-write gate (structural + semantic + specificity) | QA agent pass/fail per batch + 5 correction cycles | SKILL.md:756-808 vs automated_qa_workflow.sh:4628-4828 |
| **Agent failure handling** | Retry once, then abort validation stage | DNSP: nudge once → synthesize artifact → proceed | SKILL.md:911 vs automated_qa_workflow.sh:4698-4723 |
| **Correction capability** | 1 pass: patch + spot-check, log UNRESOLVED, stop | 5 cycles: worker retries with QA feedback | SKILL.md:1026-1049 ("does NOT loop") vs automated_qa_workflow.sh:5377 |
| **Evidence model** | Text-to-text comparison (roadmap vs tasklist). No programmatic evidence | PABLOV: fs snapshots, conversation mining, programmatic handoffs, git diffs | SKILL.md:882-901 (free-text prompts) vs automated_qa_workflow.sh:2353-2730 |
| **Session management** | N/A (stateless generation) | Dual-threshold rollover (375 msg / 175K tokens), crash recovery from batch state JSON | N/A vs automated_qa_workflow.sh:4234-4298 |
| **Traceability** | Full: R-### → T<PP>.<TT> → D-#### → artifact paths → Tier → Confidence | None formal. Per-item context references only | SKILL.md Section 5.7 vs (absence in RF) |
| **Tier classification** | Deterministic: compound phrases → keyword scan → context boosters. 4 tiers, confidence scoring | None. All items get equal treatment | SKILL.md Section 5.3 vs (absence in RF) |
| **Token cost** | Low: 50-80K typical (single-pass generation + validation) | Very high: 500K-1M+ (serial batching, context accumulation, correction loops) | Measured from architecture analysis |
| **Wall-clock** | 2-15 minutes | 15-45 minutes per task; hours for multi-phase projects | Measured from architecture analysis |

---

## 5. Proposal Portfolio with Impact Analysis

Five proposals were designed to import RF mechanisms into SC's validation pipeline. Each targets a specific weakness (W1-W6 from Section 3.1 analysis) with a specific RF mechanism (R1-R6).

| Proposal | SC Weakness Addressed | RF Mechanism Borrowed | Target Area in SKILL.md |
|----------|----------------------|----------------------|------------------------|
| P3: DNSP for Validation Agents | W1 (no execution resilience — agent failure aborts validation) | R3 (DNSP: Detect-Nudge-Synthesize-Proceed) | Stage 7, line 911 |
| P1: Context-Armed Steps | W4 (no context protection for Sprint executor) | R1 (self-contained items with embedded context) | Section 6B, lines 646-653 |
| P2: Bounded Patch Loop | W5 (single-pass correction) | R4 (correction loops with targeted feedback) | Stages 9-10, lines 1005-1049 |
| P4: Evidence-Anchored Validation | W6 (no PABLOV-style evidence) + W2 (LLM-only validation) | R2 (PABLOV programmatic evidence) | Stage 7, lines 882-901 |
| P5: Feedback-Driven Tier Calibration | W3 (no execution-time feedback loop) | RF agent memory + correction patterns | Section 5.3, lines 337-394 |

### Pre-Adversarial Impact Estimates

| Proposal | Lines of Change | Quality Gain | Token Impact | Risk |
|----------|----------------|--------------|-------------|------|
| P3 | ~20 | Medium | Neutral | Very Low |
| P1 | Template edit | Medium-High | +5-10% gen / -10-20% exec | Low |
| P2 | ~50 (loop) | Medium | +0-25% worst case | Low |
| P4 | New stage + schema | High | -10-15% validation | Low-Medium |
| P5 | New stage + parsing | Medium-High (cumulative) | Neutral gen / -5-10% exec | Medium |

---

## 6. Adversarial Validation Outcomes

Each proposal was debated by a dedicated adversarial agent examining 3 variants (Baseline / Proposed / Conservative Alternative) across 5 focus areas (Correctness, Complexity, Operational Cost, Maintainability, Determinism).

### 6.1 Aggregate Results

| Proposal | Proposed Score | Winner Score | Winner | Verdict | Convergence |
|----------|---------------|-------------|--------|---------|-------------|
| P3: DNSP | **39/50** | **39/50** | Proposed (B) | **ADOPT** | 0.80 |
| P1: Context Steps | 22/50 | 34/50 | Conservative (C) | **REVISE** | 0.75 |
| P2: Patch Loop | 20/50 | 39/50 | Conservative (C) | **REVISE** | 0.85 |
| P4: Evidence | 27/50 | 39/50 | Conservative (C) | **REVISE** | 0.82 |
| P5: Calibration | 23/50 | 40/50 | Conservative (C) | **REVISE** | 0.85 |

**Mean convergence**: 0.81 (strong agreement across focus areas).

### 6.2 Key Adversarial Findings

**F1: Per-step context references are unreliable** (P1, Correctness debate).
*Observed*: The generator operates on roadmap text, not the live codebase (SKILL.md:46-55: "Treat the roadmap as the only source of truth"). Roadmaps rarely name specific source file paths.
*Inferred*: Per-step `Context: src/middleware/` values would require the generator to hallucinate paths that may not exist or may change between generation and execution.
*Resolution*: Revise to task-level `## Execution Context` using "source areas" rather than specific paths. Roadmap item references (R-###) are the one high-value, low-risk context element — always known at generation time, never go stale.

**F2: Subset-only re-validation has an oscillation defect** (P2, Correctness debate).
*Observed*: The proposal re-validates only UNRESOLVED items after re-patching. Stage 9 delegates to `sc:task-unified` (SKILL.md:1009), which is LLM-based and non-deterministic.
*Inferred*: Patching item A can regress previously-RESOLVED item B. Because only the UNRESOLVED subset is re-checked, this regression goes undetected. Successive cycles can oscillate (fix A breaks B, fix B breaks A).
*Supporting evidence*: RF empirical data — 21 retry files across 18 batches in the llm-workflows repo (`.dev/tasks/TASK-RF-*/outputs/worker_session_batch*.retry.json`). RF mitigates with full re-QA of the entire batch, not just failed items.
*Resolution*: Prefer human checkpoint for interactive use. If automation required, mandate full-set re-validation + monotonicity guard (halt if |UNRESOLVED| doesn't strictly shrink).

**F3: The quality gate already catches what the evidence extraction would catch** (P4, Correctness debate).
*Observed*: The 17-point quality gate (SKILL.md:756-808) checks deliverable ID uniqueness (check 10), roadmap item coverage (check 12), task count bounds (check 13), and orphan detection (check 14). These are the same structural issues the proposed evidence JSON would surface.
*Inferred*: If the gate passes (which it must — write atomicity requires it), the evidence JSON's `orphan_deliverables` and `missing_roadmap_items` fields would be empty. The extraction is redundant with the gate.
*Resolution*: Pipe the gate's existing check results to validation agents rather than building a parallel extraction pipeline.

**F4: Automatic tier modification violates operational determinism** (P5, Determinism debate).
*Observed*: The protocol guarantees "same input -> same output" (SKILL.md:30) where input = roadmap text. Adding feedback-log.md as a second input that modifies tier scores means different feedback files produce different tiers for the same roadmap.
*Inferred*: A user running the generator expecting reproducibility from the roadmap alone gets surprising results if an unknown feedback-log.md exists in the working directory. This is a "hidden input" problem.
*Resolution*: Make feedback advisory-only. All scored tiers computed from roadmap text alone. Advisory section surfaces prior override patterns for human review without modifying scores.

### 6.3 Dominant Pattern

4 of 5 proposals directly ported RF mechanisms that are designed for RF's execution context (long-running sessions, stateful batch processing, non-deterministic agent behavior). When applied to SC's generation context (single-pass, stateless, determinism-first), the same mechanisms introduced unnecessary complexity. The conservative alternatives succeeded by adapting the *intent* of each RF mechanism to SC's architectural constraints rather than porting the *implementation*.

---

## 7. Final Recommended Refactor Plan for sc:tasklist

Five changes, all additive to existing stages. No rewrites. No new pipeline stages. No schema contracts.

### R1: DNSP for Validation Agents

**Target**: SKILL.md Stage 7 agent failure handling (line 911)
**Current**: "if an agent fails, retry once before reporting error"
**Change**: After retry failure, synthesize a conservative HIGH-severity finding flagging the affected task range for manual review. Proceed with 2N-1 agent findings. Add all-agents-fail guard (if zero agents succeeded, raise StageError as today). Add `source: "synthetic-dnsp"` metadata to synthesized findings.
**Implementation**: ~25 lines of conditional logic in the orchestrator merge step (after all 2N agents return).
**Files modified**: SKILL.md — Stage 7 section only.

### R2: Task Execution Context Block

**Target**: SKILL.md Section 6B — Phase File Template, after Steps list
**Current**: No explicit context section per task
**Change**: Add an optional `## Execution Context` section containing roadmap item refs (always), likely source areas (when inferable from roadmap), and key constraints. No specific file paths. No `Ensuring:` clause (verification stays in Acceptance Criteria).
**Implementation**: Template modification in SKILL.md Section 6B + `templates/phase-template.md`. No protocol logic changes.
**Files modified**: SKILL.md Section 6B, `templates/phase-template.md`.

### R3: Quality Gate Evidence Passthrough

**Target**: SKILL.md Stage 6 (quality gate) output + Stage 7 agent prompt context
**Current**: Quality gate runs silently; validation agents receive no structural check results
**Change**: Extend Stage 6 to emit `TASKLIST_ROOT/validation/gate-results.txt` — a plain-text summary of all 17 check results (PASS/FAIL per check). Inject into Stage 7 agent prompts: "All PASS items are machine-verified — do not re-check. All FAIL items are machine-verified defects — flag as HIGH. Focus on semantic quality."
**Implementation**: ~15 lines to format gate results + prompt append.
**Files modified**: SKILL.md — Stage 6 section (output addition) + Stage 7 section (agent prompt modification).

### R4: Dual-Mode Patch Recovery

**Target**: SKILL.md Stages 9-10 flow control
**Current**: Single-pass patch + spot-check. UNRESOLVED logged, not re-attempted.
**Change**:
- **Interactive mode**: If UNRESOLVED > 0, AskUserQuestion: "N findings remain unresolved. Re-attempt patches or accept as-is?"
- **Automated mode** (`--non-interactive`): One retry cycle with: full-set re-validation (not subset-only), monotonicity guard (halt if |UNRESOLVED| doesn't shrink), regression detection (halt if previously-RESOLVED item becomes UNRESOLVED). Cap at 2 total passes.
**Implementation**: ~30 lines (conditional branch + optional loop with guards).
**Files modified**: SKILL.md — between Stage 10 and Final Output Constraint sections.

### R5: Tier Calibration Advisory

**Target**: SKILL.md Section 5.3 (pre-generation) + `tasklist-index.md` output
**Current**: Feedback Collection Template exists (SKILL.md lines 575-591) but generator never reads it
**Change**: If `feedback-log.md` exists in TASKLIST_ROOT, parse override rows (min 2 matching entries), produce `## Tier Calibration Advisory` section in tasklist-index.md. Advisory only — all scored tiers remain roadmap-only. STRICT downgrade warnings.
**Implementation**: ~40 lines (file parsing + advisory rendering + conditional section in index).
**Files modified**: SKILL.md — new Stage 0 section. `templates/index-template.md` — advisory section placeholder. New `rules/tier-calibration-overrides.md` — feedback-log.md schema definition.

---

## 8. Implementation Sequencing Plan

### Phase 1: Quick Wins (1-2 days, zero-risk)

```
Week 1, Day 1-2
├── R1: DNSP for Validation Agents
│   ├── Edit: SKILL.md Stage 7 (~25 lines)
│   ├── Test: Simulate agent failure in Stage 7 → verify synthetic finding appears
│   │         with source: "synthetic-dnsp" and correct task range
│   ├── Test: Simulate ALL agents fail → verify StageError raised (same as today)
│   └── Verify: Successful runs produce identical output to pre-change baseline
│
└── R2: Task Execution Context Block
    ├── Edit: SKILL.md Section 6B + templates/phase-template.md
    ├── Test: Generate tasklist from known roadmap → verify ## Execution Context
    │         sections present, roadmap refs correct, no specific file paths
    ├── Test: Generate from roadmap with no inferable source areas → verify
    │         section omitted (optional field behavior)
    └── Verify: Sprint CLI still discovers and executes phase files (backward compat)
```

**Acceptance criteria**: Both changes pass. Existing test roadmaps produce identical tier scores, task IDs, deliverable IDs. Only new sections/behaviors are additive.

### Phase 2: Core Improvements (3-5 days, low risk)

```
Week 2, Day 1-3
├── R3: Quality Gate Evidence Passthrough
│   ├── Edit: SKILL.md Stage 6 (gate output) + Stage 7 (agent prompt)
│   ├── Test: Run with a roadmap known to produce a clean gate → verify
│   │         gate-results.txt shows 17/17 PASS
│   ├── Test: Run with a roadmap crafted to fail gate checks 10 and 12 →
│   │         verify gate-results.txt shows FAIL entries with details
│   ├── Test: Verify validation agents cite gate results in their findings
│   └── Verify: Gate failure still blocks writing (write atomicity preserved)
│
└── R4: Dual-Mode Patch Recovery
    ├── Edit: SKILL.md Stages 9-10 flow control (~30 lines)
    ├── Test (interactive): Craft a roadmap where patches leave 1 UNRESOLVED →
    │   verify AskUserQuestion fires with correct count
    ├── Test (automated): Same roadmap with --non-interactive →
    │   verify one retry cycle with full-set re-validation
    ├── Test (monotonicity): Craft scenario where |UNRESOLVED| grows →
    │   verify immediate halt with "non-convergent" message
    ├── Test (regression): Craft scenario where re-patch regresses item →
    │   verify halt with "regression detected" message
    └── Verify: Roadmaps with 0 UNRESOLVED produce identical output to baseline
```

**Acceptance criteria**: Gate results appear in validation artifacts. Patch recovery handles all 4 test scenarios correctly. Zero UNRESOLVED runs produce identical output.

### Phase 3: Long-Term (1-2 weeks, requires Sprint execution data)

```
Week 3+
└── R5: Tier Calibration Advisory
    ├── Create: rules/tier-calibration-overrides.md (feedback-log.md schema)
    ├── Edit: SKILL.md (Stage 0) + templates/index-template.md
    ├── Test: Run with no feedback-log.md → verify no advisory section
    ├── Test: Run with feedback-log.md containing 3 overrides (2 matching) →
    │   verify advisory table appears with correct patterns
    ├── Test: Run with feedback suggesting STRICT downgrade →
    │   verify WARNING appears
    ├── Test: Run same roadmap twice with different feedback files →
    │   verify tier scores are IDENTICAL (determinism preserved),
    │   only advisory section differs
    └── Prerequisite: At least 1 Sprint execution run to produce real
        feedback-log.md data for testing
```

**Acceptance criteria**: Tier scores are never modified by feedback. Advisory renders correctly. Determinism test passes (same roadmap → same tiers regardless of feedback file).

---

## 9. Open Risks and Assumptions

### Risks

| # | Risk | Severity | Mitigation | Status |
|---|------|----------|------------|--------|
| K1 | **Validation agent compliance with gate evidence** — agents may ignore injected gate-results.txt and re-derive structural facts anyway, negating R3's token savings | Low | R3 is supplementary — agents still run full validation. Worst case: no token savings, but no harm. Empirical measurement needed after deployment | Open — requires Sprint execution data |
| K2 | **Feedback-log.md population** — R5 depends on someone filling in the feedback table. If auto-populated by Sprint executor, schema and trigger need specification. If human-maintained, adoption is uncertain | Medium | R5 is Phase 3 (long-term). Defer schema specification until Sprint executor behavior is defined. Document feedback-log.md as optional | Open — deferred to Sprint CLI work |
| K3 | **DNSP synthetic findings masking real issues** — if a failed agent's task range contains critical issues, the synthetic "manual review required" finding understates the problem | Low | The synthetic finding is strictly more informative than the current behavior (total validation abort). Conservative HIGH severity ensures the flag is not overlooked | Accepted |
| K4 | **Patch loop regression in automated mode** — even with full-set re-validation and monotonicity guard, `sc:task-unified` could produce patches that pass re-validation but introduce subtle semantic regressions not caught by spot-check | Low | Cap at 2 total passes limits blast radius. Monotonicity guard halts on first sign of non-convergence. Human checkpoint is the preferred mode for high-stakes runs | Accepted |
| K5 | **Task Execution Context Block staleness** — even at task-level granularity (not per-step), source area references derived from roadmap text may not match the actual codebase at Sprint execution time | Low | Context block uses "source areas" not specific paths, and is explicitly optional. Executor resolves actual paths at runtime. Roadmap item refs (R-###) never go stale | Accepted |

### Assumptions

| # | Assumption | Basis | Impact if Wrong |
|---|-----------|-------|-----------------|
| A1 | The 17-point quality gate consistently catches orphan deliverables and missing roadmap items before writing | SKILL.md:756-808 defines the checks; write atomicity (line 816) prevents writing if checks fail | If gate has bugs, R3 (gate passthrough) would forward incorrect PASS results to validation agents. Mitigation: validation agents still run full comparison |
| A2 | UNRESOLVED findings in Stage 10 are uncommon in typical sc:tasklist runs | Inferred from protocol design (single-pass patching suggests expectation of high patch success rate) | If UNRESOLVED findings are common, R4's interactive mode adds friction. R4's automated mode with full re-validation becomes the primary path |
| A3 | Validation agent failure rate is low (<10% per agent per run) | No empirical data. Inferred from agent architecture (small task subsets, focused prompts) | If failure rate is high, R1 (DNSP) becomes critical rather than a nice-to-have. The all-agents-fail guard prevents degenerate cases |
| A4 | Sprint executor can populate feedback-log.md with tier override data | Assumed based on the Feedback Collection Template already existing in the index (SKILL.md lines 575-591) | If Sprint executor cannot or does not populate feedback-log.md, R5 has zero value. R5 is Phase 3 specifically to allow time for Sprint CLI integration |
| A5 | All changes are additive and do not require modifying existing generated output | Design constraint. Verified: no existing field, section, or artifact is removed or restructured | If a future change requires modifying the phase file template in a non-additive way, backward compatibility with existing Sprint CLI versions would need testing |

---

## Appendix: Document Manifest

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| `INDEX.md` | 6.4KB | 65 | Master index with summaries and proposal table |
| `file-inventory.md` | 20KB | 211 | Exhaustive file inventory (78 files catalogued) |
| `dependency-map.md` | 19KB | 384 | Full dependency chains with ASCII tree diagrams |
| `pipeline-stages.md` | 28KB | 421 | Stage-by-stage pipeline diagrams for all frameworks |
| `architecture-comparison.md` | 18KB | 119 | Side-by-side tables across 8 dimensions |
| `design-rfmerger-proposals.md` | 34KB | 484 | 5 proposals with impact analysis and examples |
| `adversarial-validation.md` | 18KB | 290 | 5 adversarial debate outcomes with refactored proposals |
| `strategy-lw-task-builder.md` | 6.5KB | 88 | Pre-existing RF task builder analysis |
| **`FINAL-REPORT.md`** | — | — | **This document** |
| **Total** | **~170KB** | **~2,200** | |
