# Technical Research Report: Roadmap & Tasklist Generation Architecture Overhaul

**Date:** 2026-04-04
**Depth:** Deep
**Research files:** 8 codebase + 2 web research
**Scope:** `src/superclaude/cli/roadmap/`, `src/superclaude/cli/tasklist/`, `src/superclaude/cli/pipeline/`, `src/superclaude/examples/`

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Current State Analysis](#2-current-state-analysis)
3. [Target State](#3-target-state)
4. [Gap Analysis](#4-gap-analysis)
5. [External Research Findings](#5-external-research-findings)
6. [Options Analysis](#6-options-analysis)
7. [Recommendation](#7-recommendation)
8. [Implementation Plan](#8-implementation-plan)
9. [Open Questions](#9-open-questions)
10. [Evidence Trail](#10-evidence-trail)

---

## 1. Problem Statement

### The Question

Why does the Roadmap and Tasklist pipeline architecture produce systematically degraded output when given richer input, and what structural failures in the pipeline cause granularity loss, output truncation, and format instability?

### Why It Matters

The pipeline exhibits a paradoxical failure: 4.1x richer input (1,282 lines of TDD+PRD vs 312 lines of spec-only) produces 49% fewer actionable tasks (44 vs 87) for the same functional domain (research/08, Section 1). The R-item-to-task ratio is a perfect 1:1 in both cases, confirming the tasklist generator is functioning correctly -- the loss occurs upstream in the roadmap generation pipeline (research/08, Section 2).

Three structural failures compound to produce this result:

| Failure | Mechanism | Evidence Source |
|---------|-----------|-----------------|
| **Extraction destroys granularity** | Spec/TDD tables, code blocks, and field-level definitions are summarized into prose sections. No instruction preserves original structured formats. | research/03, Section 2 |
| **One-shot output hits token limits** | Each pipeline step is a single `claude --print` subprocess with stdout capture. No continuation, no chunking, no partial output preservation. Output truncation is undetected. | research/04, Sections 5.2-5.3 |
| **No output templates** | Neither the generate nor merge prompts define a task table schema (columns, required fields). Output structure is LLM-invented and varies per run. The merge prompt lacks the ID preservation and integration enumeration instructions present in the generate prompt. | research/03, Sections 8, 13 |

### Trigger

The prior tasklist-quality research (2026-04-03) identified that enrichment content IS present in the compressed output -- persona references, compliance markers, and +70% component references appear in the 44-task output (research/08, Section 1). The pipeline compresses rather than expands: richer context causes the LLM to adopt coarser organizational structures (3 delivery-milestone phases vs 5 technical-layer phases) and bundle multiple work items into narrative subsections instead of flat table rows.

Partial fixes have been applied to the roadmap generate prompt since that research: the TDD block now mandates technical-layer phasing and per-item decomposition, and the PRD block now prevents phase count reduction (research/08, Section 3, Loss Point 1). However, the tasklist prompt's PRD suppression language, the skill protocol's merge directives, and the absence of task count floors remain unfixed (research/08, Section 6).

---

## 2. Current State Analysis

All claims in this section are traced to source code reads performed during research. Claims tagged [CODE-VERIFIED] were confirmed against specific file paths and line numbers.

### 2.1 Roadmap Pipeline

**Source files:** `executor.py`, `commands.py`, `pipeline/executor.py`

The roadmap pipeline is a 12-step sequential-with-one-parallel-group pipeline orchestrated by `execute_roadmap()` (executor.py:2245-2391). Steps are built upfront by `_build_steps()` (executor.py:1299-1490) with no dynamic step injection during execution.

**Pipeline step inventory** [CODE-VERIFIED]:

| # | Step ID | Execution Type | Gate | Timeout |
|---|---------|---------------|------|---------|
| 1 | extract | Claude subprocess | EXTRACT_GATE or EXTRACT_TDD_GATE (STRICT) | 300s / 1800s |
| 2a | generate-{agent_a} | Claude subprocess (parallel) | GENERATE_A_GATE (STRICT) | 900s |
| 2b | generate-{agent_b} | Claude subprocess (parallel) | GENERATE_B_GATE (STRICT) | 900s |
| 3 | diff | Claude subprocess | DIFF_GATE (STANDARD) | 300s |
| 4 | debate | Claude subprocess | DEBATE_GATE (STRICT) | 600s |
| 5 | score | Claude subprocess | SCORE_GATE (STANDARD) | 300s |
| 6 | merge | Claude subprocess | MERGE_GATE (STRICT) | 600s |
| 7 | anti-instinct | Deterministic Python | ANTI_INSTINCT_GATE (STRICT) | 30s |
| 8 | test-strategy | Claude subprocess | TEST_STRATEGY_GATE (STRICT) | 300s |
| 9 | spec-fidelity | Claude subprocess | SPEC_FIDELITY_GATE (STRICT) | 600s |
| 10 | wiring-verification | Deterministic Python | WIRING_GATE (TRAILING) | 60s |
| 11 | deviation-analysis | Deterministic Python | DEVIATION_ANALYSIS_GATE (STRICT) | 300s |
| 12 | remediate | Deterministic Python | REMEDIATE_GATE (STRICT) | 600s |

(research/01, Section 5)

A 13th step (certify) has a builder function `build_certify_step()` at executor.py:1259, but is never called -- confirmed dead code (research/01, Gap 1).

**Architectural patterns** [CODE-VERIFIED]:
- Inter-step communication is file-on-disk with YAML frontmatter (research/01, Section 10, Pattern 3)
- 4 of 12 steps are deterministic Python (no LLM): anti-instinct, wiring-verification, deviation-analysis, remediate
- Only one parallel group exists: generate-A + generate-B
- Single-agent mode runs both generate steps with the same agent; diff/debate/score still execute on identical outputs (research/01, Gap 5)

### 2.2 Tasklist Pipeline

**Source files:** `tasklist/commands.py`, `tasklist/executor.py`, `tasklist/prompts.py`, `sc-tasklist-protocol/SKILL.md`

The tasklist pipeline is split across two execution paths (research/06, Section 1):

| Dimension | CLI Path | Skill Path |
|-----------|----------|------------|
| Command | `superclaude tasklist validate <dir>` | `/sc:tasklist` |
| Function | Validation only | Generation + validation |
| Executor | Subprocess (`claude --print`) | Interactive Claude session |
| Output | Single fidelity report | Multi-file tasklist bundle (N+1 files) |
| Gate enforcement | Programmatic (YAML FM + semantic checks) | Inference-only (self-check) |

**There is no CLI `tasklist generate` subcommand** [CODE-VERIFIED]. `build_tasklist_generate_prompt()` exists in `tasklist/prompts.py` but is never called by any CLI code (research/06, Section 1).

**R-item identity gap** [CODE-VERIFIED]: R-items (R-001, R-002, ...) are assigned by the generation-time LLM following SKILL.md Section 4.1 rules. The validation-time LLM independently re-derives R-items. No shared registry exists (research/06, Section 5.3).

### 2.3 Input Routing

**Source files:** `executor.py` (lines 63-316), `commands.py`

Input routing is a 3-layer system [CODE-VERIFIED] (research/02):

```
Layer 1: Detection (detect_input_type, executor.py:63-185)
  Weighted scoring: PRD >= 5 (max 21), TDD >= 5 (max 17), fallback "spec"

Layer 2: Routing (_route_input_files, executor.py:188-316)
  Assigns files to slots: spec_file, tdd_file, prd_file
  CRITICAL: When input_type == "tdd", TDD occupies config.spec_file slot;
            tdd_file slot is cleared (line 296)

Layer 3: Propagation (_build_steps + prompt builders)
  input_type only diverges behavior at the extract step
  All other steps use identical prompts regardless of input_type
```

**Key routing behaviors** [CODE-VERIFIED]:

| Scenario | spec_file | tdd_file | prd_file | input_type |
|----------|-----------|----------|----------|------------|
| Single spec | spec | None | None | "spec" |
| Single TDD | **TDD** | None | None | "tdd" |
| Spec + TDD | spec | TDD | None | "spec" |
| Spec + TDD + PRD | spec | TDD | PRD | "spec" |
| Single PRD | **rejected** | -- | -- | -- |

(research/02, Section 4)

The `--input-type` CLI flag accepts `["auto", "tdd", "spec"]` but NOT `"prd"`, even though `detect_input_type()` can return `"prd"` and `RoadmapConfig.input_type` accepts it (research/02, Section 1).

### 2.4 Prompt Architecture

**Source file:** `prompts.py` (942 lines, 10 prompt-building functions, 4 shared constants)

All prompts are pure Python string construction with no external template files [CODE-VERIFIED] (research/03, Section 15). File inputs are embedded inline by `_embed_inputs()` -- the `--file` flag is explicitly avoided per code comment at executor.py:719-721 (research/04, Section 4).

**Granularity flow through prompts** [CODE-VERIFIED]:

```
Spec/TDD (maximum granularity)
  |
  v  build_extract_prompt / build_extract_prompt_tdd
Extract ----> REDUCES: tables/code blocks become prose sections
  |
  v  build_generate_prompt (x2 agents, parallel)
Generate ---> DESTROYS (no TDD) / REDUCES (with TDD)
  |            No task table schema defined. Output structure LLM-invented.
  v
Diff -------> REDUCES: discards agreed content, summarizes divergences only
  v
Debate -----> NEUTRAL: additive analysis, not summarization
  v
Score ------> REDUCES: collapses variants into selection + improvement list
  v
Merge ------> PRESERVES-OR-DESTROYS: no ID preservation, no granularity floor
  v
Fidelity ---> MEASURES: validation, catches some losses at dimension level
```

(research/03, Section 15)

**Three critical prompt gaps** [CODE-VERIFIED] (research/03, Section 13):

1. **No task table schema anywhere.** `build_generate_prompt` says "task rows" but never defines columns. `build_merge_prompt` does not mention task rows at all.
2. **Merge prompt lacks ID preservation.** Generate says "Preserve ALL IDs... Do NOT renumber." Merge has no such instruction.
3. **Merge prompt lacks `_INTEGRATION_ENUMERATION_BLOCK`.** Generate appends this block; merge does not. Wiring tasks can be lost during merge.

### 2.5 Output Mechanism

**Source files:** `pipeline/process.py` (lines 24-203), `executor.py` (lines 649-830)

**ClaudeProcess architecture** [CODE-VERIFIED] (research/04):

```
[Prompt with all inputs inline]
  --> claude --print --verbose --dangerously-skip-permissions
       --no-session-persistence --tools default
       --max-turns 100 --output-format text -p <prompt>
  --> stdout redirected to output_file via OS pipe buffer
  --> _sanitize_output() strips conversational preamble
  --> Gate evaluation against output_file on disk
```

**Key constraints** [CODE-VERIFIED]:

| Constraint | Detail | Source |
|-----------|--------|--------|
| One-shot output | `--output-format text` captures only final text response | research/04, Section 3.2 |
| No continuation | `--no-session-persistence` always set; each step isolated | research/04, Section 5.3 |
| No truncation detection | If output hits token limit, file may be incomplete | research/04, Section 5.2 |
| Retry without learning | Retries re-send identical prompt; partial output overwritten | research/04, Section 8.2 |
| Prompt size ceiling | `_EMBED_SIZE_LIMIT` = 120 KB; Linux `MAX_ARG_STRLEN` = 128 KB hard limit | research/04, Section 4 |
| Full tool access unused | `--tools default` gives Write/Edit/Bash access, but all output goes through stdout | research/04, Sections 2, 9 |

### 2.6 Gate Architecture

**Source files:** `roadmap/gates.py`, `audit/wiring_gate.py`, `pipeline/gates.py`, `pipeline/models.py`

**Gate enforcement tiers** [CODE-VERIFIED] (research/05):

| Tier | Checks |
|------|--------|
| EXEMPT | Always passes |
| LIGHT | File exists + non-empty |
| STANDARD | LIGHT + min_lines + frontmatter field presence |
| STRICT | STANDARD + semantic check functions |

**Gate migration risk assessment** [CODE-VERIFIED]:

| Risk Level | Gates | Reason |
|-----------|-------|--------|
| HIGH (will break) | EXTRACT, EXTRACT_TDD, TEST_STRATEGY, SPEC_FIDELITY, MERGE | Many frontmatter fields and/or cross-field consistency checks tightly coupled to current output format |
| MEDIUM (might break) | GENERATE_A/B, DIFF, DEBATE, CERTIFY | Light requirements but still need specific frontmatter or body format |
| LOW (will not break) | ANTI_INSTINCT, WIRING, DEVIATION_ANALYSIS, REMEDIATE, SCORE | Non-LLM steps self-generate output, or STANDARD tier with minimal checks |

**Totals:** 15 gate constants, 36 semantic check instances, 31 unique checker functions (research/05, Summary Table).

**Latent bug** [CODE-VERIFIED]: Two frontmatter parsers exist with conflicting behavior -- `_parse_frontmatter` (roadmap/gates.py) requires frontmatter at byte 0; `_check_frontmatter` (pipeline/gates.py) uses `re.MULTILINE` allowing frontmatter after preamble (research/05, Gap 1).

**Known bug B-1** [CODE-VERIFIED]: DEVIATION_ANALYSIS_GATE requires frontmatter field `ambiguous_count` but semantic check reads `ambiguous_deviations` -- field name mismatch (research/05, Gap 2).

### Current State Summary

```
                        ROADMAP PIPELINE DATA FLOW
                        ==========================

  Input Files (spec/TDD/PRD)
       |
       v
  _route_input_files()          <-- 3-layer detection/routing/propagation
       |
       v
  +--[1. EXTRACT]--+            <-- FIRST GRANULARITY LOSS
  |  stdout -> file  |
  +--------+--------+
           |
     +-----+-----+
     v             v
  [2a. GEN-A]  [2b. GEN-B]     <-- SECOND LOSS: no task table schema
  (parallel)   (parallel)
     +-----+-----+
           |
           v
  [3. DIFF] -> [4. DEBATE] -> [5. SCORE]
           |
           v
  +--[6. MERGE]--+             <-- THIRD LOSS: no ID preservation,
  |  No enumeration block      |    no granularity floor
  +--------+--------+
           |
           v
  [7-12: Validation & Remediation Steps]
```

**Cross-cutting findings:**

| Finding | Impact | Status |
|---------|--------|--------|
| Extraction is lossy for structured data | Downstream steps work from degraded input | Unfixed |
| No task table schema in generate or merge prompts | Output structure varies per run | Unfixed |
| Merge prompt missing ID preservation + integration enumeration | IDs and wiring tasks silently dropped | Unfixed |
| One-shot stdout capture with no truncation detection | Large outputs silently truncated | Unfixed |
| Tasklist PRD suppression language (prompts.py:221-223) | PRD enrichment blocked from generating tasks | Unfixed |
| SKILL.md merge directives (lines 233, 255, 259) | Over-consolidation of tasks | Unfixed |
| No task count floor anywhere in pipeline | No minimum output guarantee | Unfixed |
| Certify step (step 13) is dead code | `build_certify_step()` defined but never called | Stale code |
| Dual frontmatter parser bug | Semantic checks can fail on valid content | Latent bug |

---

## 3. Target State

### 3.1 Desired Behavior

The target architecture replaces the current extraction-based one-shot pipeline with a **template-driven incremental-write** system.

| Phase | Current Behavior | Target Behavior |
|-------|-----------------|-----------------|
| **Input consumption** | Extraction summarizes spec/TDD into lossy prose (8-14 sections) | Structured inputs (TDD/PRD) bypass extraction; spec-only inputs retain extraction with table-preserving instructions |
| **Roadmap generation** | Single `claude --print` stdout capture; no task table schema; LLM invents output structure | Template file defines section headers, table schemas, required columns; LLM fills dynamic slots via tool-use Write calls |
| **Merge step** | No ID preservation instruction; no integration enumeration block; no granularity floor | Merge prompt enforces same structural constraints as generate prompt; template schema carries through merge |
| **Output capture** | `--output-format text` captures final text blob from stdout; no progress visibility | Subprocess writes output files directly via Write/Edit tools; orchestrator validates file existence and content |
| **Gate validation** | Gates check YAML frontmatter on stdout-captured files | Gates check tool-written files; same validation; templates guarantee structural compliance |
| **Tasklist generation** | Inference-only via 800-line skill protocol; no CLI generate command | CLI `tasklist generate` subcommand backed by template-driven subprocess pipeline; shared R-item registry |
| **Output format** | Free-form markdown; structure varies per run and per agent persona | Template-enforced markdown with defined section order, table column schemas, and sentinel-validated completeness |

### Target Architecture

```
                          +------------------+
                          |   Input Files    |
                          | (spec, TDD, PRD) |
                          +--------+---------+
                                   |
                          +--------v---------+
                          | Input Router     |
                          +--------+---------+
                                   |
                    +--------------+---------------+
                    |                              |
            Structured (TDD/PRD)            Unstructured (spec)
                    |                              |
                    v                              v
          +------------------+          +--------------------+
          | Direct-to-       |          | Extraction Step    |
          | Generate         |          | (table-preserving) |
          | (bypass extract) |          +--------+-----------+
          +--------+---------+                   |
                   +----------+------------------+
                              |
                   +----------v-----------+
                   | Template-Driven      |
                   | Generate (per-agent) |
                   | Write tool output    |
                   +----------+-----------+
                              |
                   +----------v-----------+
                   | Adversarial Steps    |
                   | (diff, debate,       |
                   |  score, merge)       |
                   | Template constraints |
                   +----------+-----------+
                              |
                   +----------v-----------+
                   | Validation Steps     |
                   +----------+-----------+
                              |
                   +----------v-----------+
                   | Tasklist Generation   |
                   | (template-driven,    |
                   |  CLI pipeline,       |
                   |  shared R-item       |
                   |  registry)           |
                   +----------------------+
```

### 3.2 Success Criteria

| # | Criterion | Metric | Threshold |
|---|-----------|--------|-----------|
| SC-1 | No output truncation | Steps complete without hitting `--print` token cap | 0 truncated outputs per run |
| SC-2 | Task count preservation | TDD+PRD input produces >= spec-only task count | R-item count(TDD+PRD) >= R-item count(spec-only) |
| SC-3 | Structural consistency | Roadmap output matches template section order and table schemas | 100% section presence; 100% column compliance |
| SC-4 | ID traceability | Every spec/TDD requirement ID appears in roadmap and traces to >= 1 tasklist item | 0 orphaned IDs |
| SC-5 | Gate compatibility | All existing gates pass on template-driven output | 0 gate regressions |
| SC-6 | Incremental progress | Orchestrator can observe per-section completion | >= 1 progress signal per template section |
| SC-7 | Tasklist CLI generation | `superclaude tasklist generate` produces Sprint-compatible bundle | Phase files pass `superclaude sprint run` input validation |
| SC-8 | Table-format preservation | Tables, code blocks from TDD pass through without lossy prose conversion | 0 table-to-prose conversions |
| SC-9 | Merge fidelity | Merged roadmap preserves all IDs and integration wiring from both variants | 0 ID drops; integration enumeration block present |
| SC-10 | Sentinel validation | Template sentinels (`{{SC_PLACEHOLDER:*}}`) are zero after generation | `grep -c` returns 0 |

### 3.3 Constraints

| # | Constraint | Rationale |
|---|-----------|-----------|
| CON-1 | Must not break existing `--resume` workflow | `.roadmap-state.json` is the inter-session recovery mechanism |
| CON-2 | Must preserve backward compatibility for spec-only inputs | Spec-only is the most common input type |
| CON-3 | Gate definitions for non-LLM steps must not change | These steps generate their own output format |
| CON-4 | Linux `MAX_ARG_STRLEN` limit (128 KB) for `-p` prompt flag | Prompt size ceiling remains even with incremental output |
| CON-5 | `--no-session-persistence` must remain for pipeline isolation | Cross-session state leakage would break parallel runs |
| CON-6 | Template files must be distributable via `superclaude install` | Templates live in `src/superclaude/` and deploy to `~/.claude/` |
| CON-7 | Sprint pipeline compatibility for tasklist output | Phase files must start with `# Phase N -- <Name>` |
| CON-8 | `--tools default` and `--dangerously-skip-permissions` remain | Changing permission flags would affect all pipelines |
| CON-9 | Coexistence during migration | Template-driven output must coexist with current format during transition |
| CON-10 | Template versioning | Changes to template structure must not silently break existing gates |

---

## 4. Gap Analysis

### 4.1 Gap Table

| # | Gap | Severity | Current State | Target State |
|---|-----|----------|--------------|-------------|
| **G-01** | Extraction destroys structured data granularity | **Critical** | `build_extract_prompt` produces 8 prose sections. Tables, code blocks rewritten as narrative. TDD extraction (14 sections) still lossy. | Structured inputs bypass extraction. Spec-only extraction includes table-preservation instructions. |
| **G-02** | One-shot stdout capture architecture | **Critical** | `claude --print --output-format text`, no intermediate visibility. Non-streaming fallback caps at 64k tokens. No truncation detection or continuation. | Subprocess writes output via Write/Edit tools. Orchestrator validates file existence/content. |
| **G-03** | No roadmap output template | **Critical** | Roadmap structure entirely LLM-invented. No table columns defined. Output varies per run/agent. | PART 1/PART 2 template with defined sections, table schemas, sentinel validation. |
| **G-04** | No tasklist output template | **Critical** | Format defined by convention in 800-line SKILL.md. No enforceable template. No CLI generate. | Tasklist output template with CLI `tasklist generate` subcommand. |
| **G-05** | Merge prompt lacks ID preservation | **High** | Generate says "Preserve ALL IDs"; merge has NO such instruction. `_INTEGRATION_ENUMERATION_BLOCK` missing from merge. | Merge includes identical ID preservation and enumeration block. |
| **G-06** | No granularity floor in any prompt | **High** | No minimum task row counts. TDD block's "MORE roadmap task rows" is relative, not count-based. | Template defines per-section minimums. Gate semantic checks enforce minimum row counts. |
| **G-07** | Gate fragility under format changes | **High** | 5 gates will break if output format changes (EXTRACT, EXTRACT_TDD, MERGE, TEST_STRATEGY, SPEC_FIDELITY). | Templates guarantee fields gates expect. Gate update path documented. |
| **G-08** | PRD suppression in tasklist prompt | **High** | `tasklist/prompts.py` lines 221-223 block PRD from generating tasks. Strongest single root cause of task count regression. | PRD generates additional task rows for compliance, persona tests, success metrics. |
| **G-09** | SKILL.md protocol merge directives | **High** | 3+ merge instructions with vague matching criteria cause over-consolidation. | Merge criteria require exact ID match or explicit justification. |
| **G-10** | Diff step discards agreed content | **Medium** | Shared assumptions counted but not preserved in detail. | Diff includes "Shared Structure" section preserving agreed task tables verbatim. |
| **G-11** | Score step's free-form improvement list | **Medium** | Section 5 improvements are free-form prose. Merge relies on this vague summary. | Structured table: Improvement ID, Source Variant, Section, Description, Priority. |
| **G-12** | No task table schema defined anywhere | **Medium** | Generate says "task rows" but never defines columns. Merge doesn't mention task rows. | Canonical schema: `Task ID | Phase | Description | Dependencies | AC | Complexity | Files`. |
| **G-13** | Tasklist R-item identity gap | **Medium** | R-items assigned by generation LLM, re-derived by validation LLM independently. No shared registry. | Machine-readable R-item registry section in roadmap output. |
| **G-14** | Tasklist one-shot output limits | **Medium** | Generation produces N+1 files in single session. Large roadmaps push context limits. | Template-driven CLI pipeline generates one phase file per subprocess invocation. |
| **G-15** | Two frontmatter parsers with conflicting behavior | **Medium** | `_parse_frontmatter` requires FM at byte 0; `_check_frontmatter` allows FM after preamble. | Single frontmatter parser. Template-driven output eliminates preamble issue. |
| **G-16** | No anti-consolidation guard in tasklist prompts | **Medium** | No instruction prevents merging distinct tasks. Merge directives actively encourage consolidation. | Explicit guard: "Do NOT merge tasks with different AC, deliverable types, or dependency chains." |
| **G-17** | Testing task absorption | **Medium** | TDD+PRD produces 5 standalone test tasks vs spec-only's 28 (5.6:1 ratio). | Minimum standalone test task count derived from extraction data. |
| **G-18** | `build_certify_step()` is dead code | **Low** | Defined at executor.py:1259 but never called. | Wire into pipeline or remove. |
| **G-19** | Deviation-analysis gate field name mismatch | **Low** | Gate requires `ambiguous_count`; semantic check reads `ambiguous_deviations`. | Fix field name consistency. |
| **G-20** | Wiring-verification asks for code analysis from a planning document | **Low** | Prompt's 3 defect classes are code-level concerns analyzed from roadmap text. | Scope to architectural wiring validation. |
| **G-21** | Stale step count documentation | **Low** | Docstrings say "9-step" / "8-step" pipeline; actual is 12+ steps. | Update all docstrings. |

### 4.2 Gap Severity Distribution

```
Critical (4):  G-01, G-02, G-03, G-04
High (5):     G-05, G-06, G-07, G-08, G-09
Medium (8):   G-10, G-11, G-12, G-13, G-14, G-15, G-16, G-17
Low (4):      G-18, G-19, G-20, G-21
Total: 21 gaps
```

### 4.3 Gap Dependency Map

```
G-03 (output template) ---+---> G-05 (merge ID preservation)
                          |---> G-06 (granularity floor)
                          |---> G-07 (gate compatibility)
                          |---> G-12 (task table schema)
                          +---> G-10 (diff shared content)

G-02 (incremental write) ----> G-14 (tasklist output limits)

G-04 (tasklist template) ---+---> G-08 (PRD suppression)
                            |---> G-09 (merge directives)
                            |---> G-13 (R-item registry)
                            +---> G-16 (anti-consolidation)

G-01 (extraction bypass) ----> G-17 (testing task absorption)
```

**Critical path**: G-03 (roadmap template) is the highest-fan-out dependency -- 5 other gaps depend on it. G-02 (incremental write) is the highest-risk change but has only 1 direct dependent.

---

## 5. External Research Findings

> All findings in this section are supplementary. Codebase findings take precedence where conflicts exist.

### 5.1 Claude CLI Output Formats and Capabilities

**Sources:** [Claude CLI Reference](https://code.claude.com/docs/en/cli-reference), [Claude Headless Docs](https://code.claude.com/docs/en/headless), [CLI Protocol Spec](https://github.com/Roasbeef/claude-agent-sdk-go/blob/main/docs/cli-protocol.md), [Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)

| Finding | Relevance | Codebase Relationship |
|:--------|:----------|:----------------------|
| `--output-format` accepts `text`, `json`, `stream-json`. `stream-json` returns NDJSON with per-event granularity including tool_use events. | HIGH | **Supports** -- pipeline uses `text` for roadmap and `stream-json` for sprint; switching enables tool-use observability |
| Non-streaming fallback caps at 64k tokens with 300s timeout | HIGH | **Supports** -- directly explains observed truncation problem |
| Output token caps are NOT the bottleneck (Opus 4.6: 128k, Sonnet 4.6: 64k) -- typical roadmap artifacts are 5k-20k tokens | HIGH | **Supports** -- one-shot is not limited by model output caps; the `--print` fallback cap is the issue |

### 5.2 Print Mode and Agentic Capabilities

**Sources:** [Claude CLI Reference](https://code.claude.com/docs/en/cli-reference), [Claude Headless Docs](https://code.claude.com/docs/en/headless), [Instructa Blog](https://www.instructa.ai/blog/claude-code/how-to-use-allowed-tools-in-claude-code)

| Finding | Relevance | Codebase Relationship |
|:--------|:----------|:----------------------|
| `--print` mode is fully agentic when tools are available. With `--tools default`, Claude makes multiple tool calls across many turns. | HIGH | **Contradicts** assumption that `--print` is single-turn |
| Claude CAN write files directly in our current setup. `--tools default` + `--dangerously-skip-permissions` = full tool access. No flag changes needed. | HIGH | **Extends** -- only prompt changes needed to enable file-writing |
| Each tool invocation counts as a turn toward `--max-turns`. Pipeline default is 100 turns; incremental writing needs ~10-20 turns. | HIGH | **Supports** -- 100-turn budget is generous |
| `--bare` mode recommended for scripted/SDK calls; skips auto-discovery of hooks, skills, plugins, MCP servers | MEDIUM | **Extends** -- relevant for pipeline isolation |

### 5.3 Incremental Generation Patterns

**Sources:** [Addy Osmani AI Workflow](https://addyosmani.com/blog/ai-coding-workflow/), [PromptHub Content Creation](https://www.prompthub.us/blog/prompt-engineering-for-content-creation), [Taskade Prompt Chaining](https://www.taskade.com/blog/what-is-prompt-chaining), [Lakera Prompt Engineering](https://www.lakera.ai/blog/prompt-engineering-guide), [ICLR 2025 Staged Generation](https://proceedings.iclr.cc/paper_files/paper/2025/file/141304a37d59ec7f116f3535f1b74bde-Paper-Conference.pdf)

| Finding | Relevance | Codebase Relationship |
|:--------|:----------|:----------------------|
| Industry consensus: large monolithic LLM outputs fail. Break into iterative steps. | HIGH | **Supports** -- validates shift from one-shot to multi-step tool-use |
| Template skeleton + LLM fill yields higher quality than LLM-only (iEcoreGen pattern) | HIGH | **Supports** -- precisely the target architecture |
| Skeleton-of-Thought prompting: outline first, then fill each section | HIGH | **Extends** -- maps to two-phase: generate outline, fill sections |
| Prompt chaining decomposes large tasks into sequential subtasks | HIGH | **Supports** -- validates intra-step chaining (section by section) |
| Prefill/anchor technique steers LLM completion, reducing hallucination | HIGH | **Extends** -- each section fill can prefill with header and structural prefix |
| ICLR 2025 confirms staged generation outperforms single-pass for long-form content | MEDIUM | **Supports** -- academic validation |

### 5.4 Tool-Use File Writing and Format Enforcement

**Sources:** [Anthropic Claude Code](https://www.anthropic.com/product/claude-code), [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use), [Anthropic Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [Agenta Function Calling Guide](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms), [GitHub Issue #14888](https://github.com/anthropics/claude-code/issues/14888)

| Finding | Relevance | Codebase Relationship |
|:--------|:----------|:----------------------|
| Tool-based file writing is the standard agentic output pattern (Claude Code, AnythingLLM, LangChain) | HIGH | **Supports** -- Sprint already uses this; roadmap should adopt it |
| Function calling as format enforcement: define `write_section` tool with parameters, model must call it per section | HIGH | **Extends** -- most promising approach; each call is bounded, structured, observable |
| Anthropic structured outputs via `output_config` with JSON schema -- guaranteed compliance on first try | HIGH | **Extends** -- applicable for structured intermediates (extraction, base-selection); NOT for large markdown |
| Layered enforcement (structural + content + semantic + validation) is industry best practice. Pipeline currently uses only semantic layer. | HIGH | **Extends** -- comprehensive enforcement model |
| Files loaded via `@` syntax silently truncated at 2000 lines | HIGH | **Supports** -- confirms silent truncation as real issue |

### 5.5 Key Takeaways

| # | Takeaway | Impact |
|:--|:---------|:-------|
| 1 | **The `--print` non-streaming fallback 64k token cap is the root cause of truncation** -- not model output limits. Tool-use file writing bypasses this entirely. | CRITICAL |
| 2 | **No flag changes needed** -- pipeline already has `--tools default` + `--dangerously-skip-permissions`. Only prompt changes required. | HIGH |
| 3 | **Template-driven hybrid generation is a formally validated pattern** producing higher quality than LLM-only generation. | HIGH |
| 4 | **Function calling as format enforcement** naturally solves truncation, enforces structure, enables progress tracking. | HIGH |
| 5 | **Layered enforcement** is the industry best practice. Pipeline currently uses only the semantic layer (system prompts). | MEDIUM |

---

## 6. Options Analysis

Three options are evaluated, addressing the three structural failures identified in research. A fourth option (phased migration) combines Options C and B.

### Option A: Full Template-Driven Incremental Writing

Replace the extraction-based one-shot pipeline entirely with template-driven, tool-use-mode architecture. Subprocess writes output via Write/Edit tools; output templates define structural skeleton; LLM fills dynamic slots.

| Dimension | Assessment |
|-----------|------------|
| **Effort** | HIGH (~10-15 days). 2 new templates, rewrite `roadmap_run_step()`, new `tasklist generate` CLI, prompt rewrites, 6 gate updates, removal of `_sanitize_output()`. |
| **Risk** | MEDIUM-HIGH. Template design must be correct on first iteration. 4 deterministic steps depend on upstream output formats as INPUT -- format changes cascade. |
| **Reuse** | HIGH. Templates reusable. `stream-json` monitoring shared with Sprint. |
| **Pros** | Eliminates all 3 structural failures simultaneously. Fills tasklist CLI gap. Aligns roadmap with Sprint patterns. |
| **Cons** | Largest scope. Breaks backward compatibility. Requires re-running all test fixtures. 120KB prompt size limit remains. |

### Option B: Hybrid Approach (Template for TDD/PRD; Keep Extraction for Specs)

Split pipeline into two paths based on input type. Structured inputs get template-driven incremental writing; specs keep current architecture with prompt improvements.

| Dimension | Assessment |
|-----------|------------|
| **Effort** | MEDIUM (~5-8 days). 1-2 templates, conditional `_build_steps()` path, prompt improvements for spec-path, 4 gate updates. |
| **Risk** | MEDIUM. Two code paths increase maintenance. Deterministic steps must handle both output formats. |
| **Pros** | Addresses primary granularity loss for TDD/PRD (the documented 49% regression). Preserves backward compatibility for spec-only. Leverages existing `input_type` branching. |
| **Cons** | Two code paths. Spec-path still suffers one-shot limitations. Does not fill tasklist CLI gap for spec-only. |

### Option C: Minimal Fix (Prompt Improvements Only)

Keep one-shot `--output-format text` architecture. Address granularity loss through prompt engineering only: add task table schemas, ID preservation, anti-consolidation guards, fix PRD suppression language.

| Dimension | Assessment |
|-----------|------------|
| **Effort** | LOW (~1-2 days). 5-6 prompt builder modifications (~50-100 lines), 3 lines in `tasklist/prompts.py`, ~20 lines in SKILL.md. No new files, no architectural changes. |
| **Risk** | LOW. Prompt changes are additive. No cascading breakage. LLM compliance is probabilistic, not guaranteed (web-02 Finding F2). |
| **Pros** | Fastest to implement. Zero gate breakage. Directly addresses 5 unfixed gaps from prior research. Can be shipped and validated immediately. |
| **Cons** | Does NOT fix one-shot truncation (64k cap). Does NOT fix extraction granularity loss. Prompt enforcement is probabilistic. Does NOT fill tasklist CLI gap. Does NOT enable progress monitoring. |

### Option D: Phased Migration (Option C First, Then Option B)

Execute Option C immediately as quick-win, then Option B as follow-up. Phase 1 prompt improvements feed directly into Phase 2 template infrastructure.

| Dimension | Assessment |
|-----------|------------|
| **Effort** | LOW then MEDIUM (~6-10 days total, front-loaded with quick wins). |
| **Risk** | LOW then MEDIUM. Phase 1 has zero architectural risk. Phase 2 is de-risked by validated Phase 1 baseline. |
| **Pros** | Fastest path to measurable improvement. Phase 1 is investment, not throwaway. Risk-gated: can stop after Phase 1 if results sufficient. |
| **Cons** | Total effort marginally higher than Option B alone. Two implementation/review cycles. |

### Options Comparison

| Dimension | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| **Effort** | HIGH (~10-15d) | MEDIUM (~5-8d) | LOW (~1-2d) | LOW+MED (~6-10d) |
| **Risk** | MED-HIGH | MEDIUM | LOW | LOW then MED |
| **Structural failures fixed** | 3/3 | 2/3 (spec: 1/3) | 1/3 (probabilistic) | 1/3 then 2/3 |
| **Fixes 49% task reduction** | Yes | Yes (TDD/PRD) | Partially | Yes (partial then full) |
| **Fixes one-shot truncation** | Yes | Yes (TDD/PRD) | No | No then Yes |
| **Fills tasklist CLI gap** | Yes | Yes (TDD/PRD) | No | No then Yes |
| **Gate breakage** | 6 gates | 4 gates | 0 gates | 0 then 4 |
| **Backward compatible** | No | Yes | Yes | Yes |
| **Time to first improvement** | 10-15 days | 5-8 days | 1-2 days | 1-2 days |

---

## 7. Recommendation

### Recommended Approach: Option D (Phased Migration)

#### Rationale

Option D is recommended because it combines the fastest path to measurable improvement with a structured migration toward the target architecture. Three evidence-backed arguments:

**1. The highest-impact gaps are prompt-level, not architectural.**

The prior research (research/08, Section 4) identified 5 root causes for the 49% task reduction. The two rated "HIGH impact -- strongest single cause" are:
- H2: PRD suppression language in `tasklist/prompts.py` lines 221-223 (code-verified, still present)
- H4: Protocol merge directives in SKILL.md lines 233, 255, 259 (code-verified, still present)

Both are fixable with prompt text changes (Option C scope). The architectural failures contribute to quality variance but are not the primary drivers of the documented regression.

**2. Prompt improvements feed directly into template infrastructure.**

The task table schema constant created in Phase 1 becomes the table definition in the Phase 2 output template. Anti-consolidation guard text becomes PART 1 instructions. ID preservation instructions become template enforcement rules. Phase 1 work is investment, not throwaway.

**3. Risk-gated decision: Phase 2 is contingent on Phase 1 validation.**

After Phase 1 ships and test fixtures are re-run, the results determine whether Phase 2 is necessary. If prompt improvements alone bring TDD+PRD task count from 44 to 80+ (near the spec-only baseline of 87), Phase 2 may be deferrable. If the count remains below 70, the data justifies Phase 2 investment.

#### Key Trade-offs Accepted

| Trade-off | Accepted Because |
|-----------|-----------------|
| Phase 1 prompt enforcement is probabilistic | Even probabilistic enforcement is better than current zero enforcement. Phase 2 provides deterministic follow-up. |
| Total effort marginally higher than Option B alone | 1-2 day Phase 1 cost justified by 5-8 day earlier delivery of improvement. Phase 1 data de-risks Phase 2 investment. |
| Spec-path truncation not addressed in Phase 1 | Typical artifacts are 5k-20k tokens (well within limits). Truncation is a tail risk for large specs, not systemic. |
| Tasklist CLI gap persists through Phase 1 | `/sc:tasklist` skill protocol continues to function. Phase 2 adds CLI subcommand. |

#### Decision Gate Between Phases

| Metric | Proceed to Phase 2 | Defer Phase 2 |
|--------|--------------------|-----------------------|
| TDD+PRD task count | < 70 tasks (vs 87 spec-only baseline) | >= 70 tasks |
| Task granularity | R-items still bundled (>1.5:1 ratio) | R-items granular (~1:1) |
| Output truncation | Any truncation observed | No truncation |
| Stakeholder priority | Architectural improvement prioritized | Other features take priority |

---

## 8. Implementation Plan

> **Reading Context (per Section 7 Recommendation):** This implementation plan presents 6 sequential phases for the full template-driven architecture. Per the Option D (Phased Migration) recommendation, this plan should be read as follows:
> - **Phase 1 (Create Output Templates)** and **Phase 5 prompt fixes (Steps 5.1-5.5)** correspond to Option C quick fixes and should be executed first as the immediate deliverable (~1-2 days).
> - **Phases 2-4 and Phase 5 Steps 5.6-5.9** correspond to Option B architectural changes and are contingent on Phase 1 validation results.
> - A **data-driven decision gate** (Section 7) sits between these two groups. Proceed to the architectural phases only if Phase 1 prompt fixes do not achieve sufficient improvement (TDD+PRD task count >= 70).
> - **Phase 6 (Testing)** applies to both groups, with scope scaled to whichever phases were executed.

### Architecture Change Summary

| Current State | Target State | Research Basis |
|---------------|-------------|----------------|
| Prompts embed all inputs inline via `_embed_inputs()` and capture stdout | Prompts instruct Claude subprocess to write output via Write/Edit tools | research/04 Section 7.3; web-01 Finding 3 |
| `--output-format text` captures only final text blob | Keep `text` for compat; prompt instructs tool-use writing | web-01 Section 3 |
| No output templates; LLM invents structure per run | Template files define static scaffolding with dynamic slots | research/07 Pattern 2.1; web-02 Finding F2 |
| Extraction lossy-summarizes TDD/PRD into prose | Structured inputs bypass extraction; fed directly to generate | research/02 Section 7; research/03 Sections 2-3 |
| Gates check frontmatter of stdout-captured files | Gates check tool-written files (same mechanism, different source) | research/05 Impact Assessment |

### Key Constraints

| Constraint | Mitigation |
|-----------|------------|
| Linux `MAX_ARG_STRLEN` 128 KB for `-p` flag | Incremental write reduces prompt size by removing embedded prior outputs |
| `--no-session-persistence` prevents cross-invocation continuation | All incremental writes within a single `--print` invocation via tool-use turns |
| `--max-turns` default 100; each Write costs 1 turn | Roadmap generation needs ~16-20 turns; well within budget |
| Non-streaming fallback caps at 64k tokens | Tool-use file writing bypasses stdout token cap entirely |

### Phase 1: Create Output Templates

**Goal:** Define static scaffolding templates using PART 1 / PART 2 pattern (research/07, Template 4) with `{{SC_PLACEHOLDER:*}}` sentinels (research/07, Template 2).

**Dependencies:** None (foundational phase).

| Step | Action | Files |
|------|--------|-------|
| 1.1 | Create roadmap output template | `src/superclaude/cli/roadmap/templates/roadmap-output.md` (new) |
| 1.2 | Create tasklist index output template | `src/superclaude/cli/tasklist/templates/tasklist-index-output.md` (new) |
| 1.3 | Create tasklist phase file template | `src/superclaude/cli/tasklist/templates/phase-output.md` (new) |
| 1.4 | Register templates in package data | `pyproject.toml` |
| 1.5 | Add template loading utility | `src/superclaude/cli/pipeline/templates.py` (new) |

Key design decisions: task tables with explicit column schema (`Task ID | Phase | Description | Source Req | Dependencies | AC | Complexity`), anti-pattern FORBIDDEN section, completeness checklist + contract table, line budget per complexity class (LOW: >=20 rows, MEDIUM: >=40, HIGH: >=80).

### Phase 2: Implement Incremental Writing

**Goal:** Modify LLM steps to use tool-use file writing instead of stdout capture.

**Dependencies:** Phase 1.

| Step | Action | Files |
|------|--------|-------|
| 2.1 | Add template + Write instruction to `build_generate_prompt()` | `prompts.py` |
| 2.2 | Add template + Write + ID preservation to `build_merge_prompt()` | `prompts.py` |
| 2.3 | Add Write instruction to extract prompts | `prompts.py` |
| 2.4 | Add Write instruction to remaining LLM prompt builders | `prompts.py` |
| 2.5 | Pass `output_path` from `roadmap_run_step()` to prompt builders | `executor.py` |
| 2.6 | Add post-subprocess file existence check with stdout fallback | `executor.py` |
| 2.7 | Add `tool_write_mode` parameter to `ClaudeProcess` | `pipeline/process.py` |
| 2.8 | Conditionally skip `_sanitize_output()` for tool-written files | `executor.py` |

Key design decisions: keep `--output-format text` (minimize blast radius), keep `--tools default` + `--dangerously-skip-permissions` (already present), remove `_sanitize_output()` for tool-written files (no preamble to strip).

### Phase 3: Bypass Extraction for Structured Inputs

**Goal:** TDD inputs skip lossy extraction and feed directly to generate step. Extraction retained for unstructured specs.

**Dependencies:** Phase 2.

| Step | Action | Files |
|------|--------|-------|
| 3.1 | Add `_should_bypass_extraction()` helper | `executor.py` |
| 3.2 | Add `_build_extraction_stub()` for metadata consumers | `executor.py` |
| 3.3 | Conditionally skip extract step in `_build_steps()` | `executor.py` |
| 3.4 | Handle direct TDD input in `build_generate_prompt()` | `prompts.py` |
| 3.5 | Update generate step inputs for bypass mode | `executor.py` |
| 3.6 | Update `_embed_inputs()` labels for bypass mode | `executor.py` |

Key design decisions: bypass ONLY for `input_type == "tdd"` with structural validation (>= 15 numbered headings, 3+ TDD section names), produce frontmatter-only extraction stub for downstream metadata consumers (19 fields for EXTRACT_TDD_GATE).

### Phase 4: Update Gates for New Output Format

**Goal:** Ensure all gates pass on template-driven, tool-written output. Add sentinel validation.

**Dependencies:** Phases 1-3.

| Step | Action | Files |
|------|--------|-------|
| 4.1 | Accept `"bypass-tdd"` in `_extraction_mode_valid()` | `gates.py` |
| 4.2 | Add `_no_remaining_sentinels()` semantic check | `gates.py` |
| 4.3 | Add `_minimum_task_rows()` semantic check | `gates.py` |
| 4.4 | Register new checks on MERGE_GATE | `gates.py` |
| 4.5 | Register sentinel check on GENERATE gates | `gates.py` |
| 4.6 | Add `total_task_rows`, `phases_count` to MERGE_GATE FM fields | `gates.py` |
| 4.7 | Add `total_task_rows` to GENERATE gate FM fields | `gates.py` |

### Phase 5: Tasklist Pipeline Updates

**Goal:** Fix PRD suppression and merge directives (strongest root causes of regression). Apply template-driven incremental-write to tasklist pipeline. Add CLI generate subcommand.

**Dependencies:** Phases 1-2, 4.

| Step | Action | Files |
|------|--------|-------|
| 5.1 | Remove PRD suppression language | `tasklist/prompts.py` (lines 221-223) |
| 5.2 | Add anti-consolidation guard | `tasklist/prompts.py` |
| 5.3 | Add task count floor | `tasklist/prompts.py` |
| 5.4 | Tighten merge directives | `SKILL.md` (lines 233, 255, 259) |
| 5.5 | Add standalone test task minimum | `SKILL.md` (new Section 4.4c) |
| 5.6 | Rewrite `build_tasklist_generate_prompt()` for templates | `tasklist/prompts.py` |
| 5.7 | Add `tasklist generate` CLI subcommand | `tasklist/commands.py` |
| 5.8 | Add `execute_tasklist_generate()` executor | `tasklist/executor.py` |
| 5.9 | Add `TASKLIST_GENERATE_GATE` | `tasklist/gates.py` |
| 5.10 | Sync SKILL.md changes | `make sync-dev` |

> **Note (per Option D):** Steps 5.1-5.5 are prompt-level fixes that belong to the immediate Phase 1 (Option C) deliverable. Steps 5.6-5.9 are architectural changes contingent on the Phase 1 decision gate.

### Phase 6: Testing and Regression Validation

**Goal:** Verify new architecture produces equal or better output across all input types.

**Dependencies:** All prior phases.

| Step | Action | Verification |
|------|--------|-------------|
| 6.1 | Unit tests for template loading | `tests/cli/pipeline/test_templates.py` |
| 6.2 | Unit tests for extraction bypass | `tests/cli/roadmap/test_extraction_bypass.py` |
| 6.3 | Extended gate check tests | `tests/cli/roadmap/test_gates.py` |
| 6.4 | Extended prompt builder tests | `tests/cli/roadmap/test_prompts.py` |
| 6.5 | Integration: spec-only pipeline run | Verify >= 80 task rows (near baseline 87) |
| 6.6 | Integration: TDD-only with bypass | Verify > 44 task rows (exceeds prior regression) |
| 6.7 | Integration: TDD+PRD pipeline run | Verify >= TDD-only count (PRD adds, not consolidates) |
| 6.8 | Integration: tasklist generate | Verify task count >= roadmap task rows |
| 6.9 | Regression: `--resume` compatibility | State file records bypass mode correctly |
| 6.10 | Full test suite | `uv run pytest tests/ -v` -- zero failures |

### File Change Summary

| File | Change Type | Phase |
|------|------------|-------|
| `src/superclaude/cli/roadmap/templates/roadmap-output.md` | NEW | 1 |
| `src/superclaude/cli/tasklist/templates/tasklist-index-output.md` | NEW | 1 |
| `src/superclaude/cli/tasklist/templates/phase-output.md` | NEW | 1 |
| `src/superclaude/cli/pipeline/templates.py` | NEW | 1 |
| `pyproject.toml` | MODIFY | 1 |
| `src/superclaude/cli/roadmap/prompts.py` | MODIFY | 2 |
| `src/superclaude/cli/roadmap/executor.py` | MODIFY | 2, 3 |
| `src/superclaude/cli/pipeline/process.py` | MODIFY | 2 |
| `src/superclaude/cli/roadmap/gates.py` | MODIFY | 4 |
| `src/superclaude/cli/tasklist/prompts.py` | MODIFY | 5 |
| `src/superclaude/cli/tasklist/commands.py` | MODIFY | 5 |
| `src/superclaude/cli/tasklist/executor.py` | MODIFY | 5 |
| `src/superclaude/cli/tasklist/gates.py` | MODIFY | 5 |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | MODIFY | 5 |
| `.claude/skills/sc-tasklist-protocol/SKILL.md` | SYNC | 5 |
| Tests (6 new/extended files) | NEW/MODIFY | 6 |

**Total:** 8 new files, 12 modified files, 1 synced file.

---

## 9. Open Questions

### 9.1 Unresolved Bugs and Gaps

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q-06 | Latent frontmatter parser bug -- two parsers with conflicting byte-0 vs regex behavior in STRICT gates | HIGH | Unify parsers; adopt pipeline/gates.py regex-based parser for all reads |
| Q-07 | Field name mismatch in DEVIATION_ANALYSIS_GATE: `ambiguous_count` vs `ambiguous_deviations` (bug B-1) | HIGH | Fix field name consistency |

### 9.2 Design Decisions Requiring User Input

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q-05 | Neither `build_diff_prompt` nor `build_debate_prompt` accept tdd_file/prd_file -- intentional? | MEDIUM | User decision: add TDD/PRD context to diff/debate or document intentional scoping |
| Q-09 | Should extraction be removed entirely for TDD/PRD or retained as optional with bypass flag? | HIGH | Recommend: bypass for TDD primary input, retain for spec-only |
| Q-11 | Should tasklist generation move from skill-only to CLI pipeline, or should the skill be enhanced? | HIGH | User decision: (A) add CLI subcommand, (B) fix skill protocol only, (C) both |
| Q-23 | Certify step is dead code -- wire in or remove? | MEDIUM | User decision |

### 9.3 Unverified Claims Requiring Re-testing

| # | Claim | Source | Impact | Resolution |
|---|-------|--------|--------|------------|
| Q-13 | ~112 discrete work items bundled into 44 R-items (2.5:1 ratio) | research/08, H5 | HIGH | Re-run pipeline with current prompts to measure actual bundling |
| Q-14 | TDD+PRD produces 5 standalone test tasks vs baseline's 28 (5.6:1 absorption) | research/08, H3 | MEDIUM | Cannot verify without re-running pipeline |
| Q-16 | `--file` flag is a cloud download mechanism, not local injection | research/04, executor.py comment | MEDIUM | May be stale; verify against current `claude --help` |
| Q-17 | `--print` non-streaming fallback caps at 64k tokens | web-01, Finding 3.4 | HIGH | Based on GitHub issue #14888; verify against current CLI version |
| Q-39 | When were roadmap prompt fixes applied -- before or after test fixture runs? | research/08, Q6 | HIGH | Check `git blame` on prompts.py TDD/PRD blocks |
| Q-41 | Test fixture staleness: do fixtures predate roadmap prompt fixes? | research/08, Q8 | MEDIUM | Compare fixture timestamps vs prompts.py modification date |

### 9.4 Gaps Deferred to Phase 2 or Beyond

| # | Gap | Severity | Suggested Resolution |
|---|-----|----------|----------------------|
| G-10 | Diff step discards agreed content -- shared assumptions counted but not preserved | Medium | Add "Shared Structure" section to diff prompt preserving agreed task tables verbatim; address in Phase 2 prompt improvements |
| G-11 | Score step's free-form improvement list -- merge relies on vague summary | Medium | Add structured table format (Improvement ID, Source Variant, Section, Description, Priority) to score prompt; address in Phase 2 |
| G-20 | Wiring-verification asks for code analysis from a planning document | Low | Scope prompt to architectural wiring validation; address during Phase 4 gate updates |
| G-21 | Stale step count documentation ("9-step" / "8-step" pipeline) | Low | Update all docstrings referencing pipeline step counts; address as cleanup during any phase |

### 9.5 Implementation Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q-04 | TDD/PRD section references in prompts use hardcoded section numbers ("S7", "S15", "S19") | MEDIUM | Replace with section-name-based references |
| Q-08 | Optimal incremental writing strategy | HIGH | Tool-use file writing (Sprint pattern); lowest effort per web-01 Finding 3 |
| Q-10 | How should roadmap template handle variable-length content? | MEDIUM | Tiered usage model: Lightweight (3-5 phases), Standard (5-8), Heavyweight (8+) |
| Q-12 | Migration coexistence: can template-driven output coexist with current output? | MEDIUM | Yes. Opt-in via `--template` flag; default unchanged |
| Q-25 | `_EMBED_SIZE_LIMIT` = 120KB may cause E2BIG on Linux | HIGH | Fail-fast with actionable error; long-term: tool-use bypasses kernel limit |
| Q-26 | No truncation detection for subprocess output | HIGH | Check for incomplete output (mid-sentence, mid-YAML-block); add `content_complete` semantic check |

---

## 10. Evidence Trail

### 10.1 Codebase Research Files

| # | File | Topic |
|---|------|-------|
| 1 | `research/01-pipeline-step-map.md` | Complete pipeline step trace: 12-step execution, step builder, step runner, gate evaluation, data flow, architectural patterns |
| 2 | `research/02-input-routing.md` | Input routing: `detect_input_type()` weighted scoring, `_route_input_files()` algorithm, TDD-as-spec_file semantic confusion |
| 3 | `research/03-prompt-architecture.md` | All 10 prompt-building functions: granularity impact assessment (REDUCES/DESTROYS/NEUTRAL/PRESERVES/MEASURES), 6 critical gaps |
| 4 | `research/04-claude-process-output.md` | ClaudeProcess subprocess: output capture mechanism, token limits, retry without learning, incremental writing feasibility |
| 5 | `research/05-gate-architecture.md` | All 15 gate constants: per-gate enforcement tier, format migration risk (YES/MAYBE/NO), 31 checker functions, latent bugs |
| 6 | `research/06-tasklist-pipeline.md` | Tasklist: CLI validate-only vs skill generate, dead code, R-item identity gap, one-shot limits |
| 7 | `research/07-template-patterns.md` | 4 existing templates analyzed (TDD, Release Spec, PRD, MDTM), 5 cross-template patterns, recommended structures |
| 8 | `research/08-prior-research-context.md` | Prior research (2026-04-03): 49% regression root causes, 12-gap registry, partial fix assessment |

### 10.2 Web Research Files

| # | File | Topic |
|---|------|-------|
| 9 | `research/web-01-claude-cli-output.md` | Claude CLI output formats, model token limits, tool-use mode, session continuation, `--bare` mode |
| 10 | `research/web-02-incremental-generation.md` | Incremental generation patterns, template-driven hybrid generation, function calling as format enforcement, structured outputs |

### 10.3 Supporting Artifacts

| Artifact | Path |
|----------|------|
| Gaps and Questions file | `gaps-and-questions.md` |
| Research planning notes | `research/research-notes.md` |

### 10.4 Synthesis Files

| # | File | Sections Covered |
|---|------|-----------------|
| 1 | `synthesis/synth-01-problem-current-state.md` | S1 Problem Statement, S2 Current State Analysis |
| 2 | `synthesis/synth-02-target-gaps.md` | S3 Target State, S4 Gap Analysis |
| 3 | `synthesis/synth-03-external-findings.md` | S5 External Research Findings |
| 4 | `synthesis/synth-04-options-recommendation.md` | S6 Options Analysis, S7 Recommendation |
| 5 | `synthesis/synth-05-implementation-plan.md` | S8 Implementation Plan |
| 6 | `synthesis/synth-06-questions-evidence.md` | S9 Open Questions, S10 Evidence Trail |

All file paths are relative to the task directory: `.dev/tasks/to-do/TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/`
