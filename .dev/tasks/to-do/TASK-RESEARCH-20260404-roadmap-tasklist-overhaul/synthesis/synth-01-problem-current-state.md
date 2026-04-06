# Synthesis Report: Problem Statement & Current State Analysis

**Report:** synth-01-problem-current-state
**Date:** 2026-04-04
**Sources:** research/01 through research/08, gaps-and-questions.md
**Scope:** Roadmap and Tasklist Generation Architecture

---

## Section 1: Problem Statement

### The Question

Why does the Roadmap and Tasklist pipeline architecture produce systematically degraded output when given richer input, and what structural failures in the pipeline cause granularity loss, output truncation, and format instability?

### Why It Matters

The pipeline exhibits a paradoxical failure: 4.1x richer input (1,282 lines of TDD+PRD vs 312 lines of spec-only) produces 49% fewer actionable tasks (44 vs 87) for the same functional domain (research/08-prior-research-context.md, Section 1). The R-item-to-task ratio is a perfect 1:1 in both cases, confirming the tasklist generator is functioning correctly -- the loss occurs upstream in the roadmap generation pipeline (research/08, Section 2).

Three structural failures compound to produce this result:

| Failure | Mechanism | Evidence Source |
|---------|-----------|-----------------|
| **Extraction destroys granularity** | Spec/TDD tables, code blocks, and field-level definitions are summarized into prose sections. No instruction preserves original structured formats. | research/03, Section 2 ("REDUCES -- lossy summarization of spec into prose") |
| **One-shot output hits token limits** | Each pipeline step is a single `claude --print` subprocess with stdout capture. No continuation, no chunking, no partial output preservation. Output truncation is undetected. | research/04, Section 5.3 ("zero continuation logic") and Section 5.2 ("no detection or recovery for truncated output") |
| **No output templates** | Neither the generate nor merge prompts define a task table schema (columns, required fields). Output structure is LLM-invented and varies per run. The merge prompt lacks the ID preservation and integration enumeration instructions present in the generate prompt. | research/03, Section 13 ("No task table schema anywhere"), Section 8 ("Missing from merge that exists in generate") |

### Trigger

The prior tasklist-quality research (2026-04-03) identified that enrichment content IS present in the compressed output -- persona references, compliance markers, and +70% component references appear in the 44-task output (research/08, Section 1). The pipeline compresses rather than expands: richer context causes the LLM to adopt coarser organizational structures (3 delivery-milestone phases vs 5 technical-layer phases) and bundle multiple work items into narrative subsections instead of flat table rows.

Partial fixes have been applied to the roadmap generate prompt since that research: the TDD block now mandates technical-layer phasing and per-item decomposition, and the PRD block now prevents phase count reduction (research/08, Section 3, Loss Point 1). However, the tasklist prompt's PRD suppression language, the skill protocol's merge directives, and the absence of task count floors remain unfixed (research/08, Section 6).

---

## Section 2: Current State Analysis

All claims in this section are traced to source code reads performed during research. Claims tagged [CODE-VERIFIED] were confirmed against specific file paths and line numbers. Unverified behavioral observations are excluded per synthesis rules.

### 2.1 Roadmap Pipeline

**Source files:** `src/superclaude/cli/roadmap/executor.py`, `src/superclaude/cli/roadmap/commands.py`, `src/superclaude/cli/pipeline/executor.py`

The roadmap pipeline is a 12-step sequential-with-one-parallel-group pipeline orchestrated by `execute_roadmap()` (executor.py, lines 2245-2391). Steps are built upfront by `_build_steps()` (executor.py, lines 1299-1490) with no dynamic step injection during execution (research/01, Section 11, Gap 8).

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

A 13th step (certify) has a builder function `build_certify_step()` at executor.py:1259, but grep confirms it is never called anywhere -- confirmed dead code (research/01, Section 11, Gap 1; gaps-and-questions.md, I-2).

**Architectural patterns** [CODE-VERIFIED]:
- Inter-step communication is file-on-disk with YAML frontmatter (research/01, Section 10, Pattern 3)
- 4 of 12 steps are deterministic Python (no LLM): anti-instinct, wiring-verification, deviation-analysis, remediate (research/01, Section 10, Pattern 4)
- Only one parallel group exists: generate-A + generate-B (research/01, Section 10, Pattern 5)
- Single-agent mode runs both generate steps with the same agent; diff/debate/score still execute on identical outputs (research/01, Section 11, Gap 5)

### 2.2 Tasklist Pipeline

**Source files:** `src/superclaude/cli/tasklist/commands.py`, `src/superclaude/cli/tasklist/executor.py`, `src/superclaude/cli/tasklist/prompts.py`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

The tasklist pipeline is split across two execution paths (research/06, Section 1):

| Dimension | CLI Path | Skill Path |
|-----------|----------|------------|
| Command | `superclaude tasklist validate <dir>` | `/sc:tasklist` |
| Function | Validation only | Generation + validation |
| Executor | Subprocess (`claude --print`) | Interactive Claude session |
| Output | Single fidelity report | Multi-file tasklist bundle (N+1 files) |
| Gate enforcement | Programmatic (YAML FM + semantic checks) | Inference-only (self-check) |

**There is no CLI `tasklist generate` subcommand** [CODE-VERIFIED]. `build_tasklist_generate_prompt()` exists in `tasklist/prompts.py` but is never called by any CLI code (research/06, Section 1). Generation requires the `/sc:tasklist` skill protocol -- an 800-line inference-based prompt in SKILL.md.

The CLI validate path is a single-step pipeline: one `ClaudeProcess` subprocess runs `build_tasklist_fidelity_prompt()`, producing `tasklist-fidelity.md` validated by `TASKLIST_FIDELITY_GATE` (research/06, Section 2).

**R-item identity gap** [CODE-VERIFIED]: R-items (R-001, R-002, ...) are assigned by the generation-time LLM following SKILL.md Section 4.1 rules. The validation-time LLM independently reads the roadmap and must re-derive R-items. No shared registry exists between generation and validation runs (research/06, Section 5.3).

### 2.3 Input Routing

**Source files:** `src/superclaude/cli/roadmap/executor.py` (lines 63-316), `src/superclaude/cli/roadmap/commands.py`

Input routing is a 3-layer system [CODE-VERIFIED] (research/02, Summary):

```
Layer 1: Detection (detect_input_type, executor.py:63-185)
  Weighted scoring: PRD threshold >= 5 (max 21), TDD threshold >= 5 (max 17), fallback "spec"
  Content-based, not filename-based.

Layer 2: Routing (_route_input_files, executor.py:188-316)
  Assigns files to slots: spec_file, tdd_file, prd_file
  CRITICAL: When input_type == "tdd", the TDD occupies config.spec_file slot;
            the tdd_file slot is cleared (line 296)

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

The `--input-type` CLI flag accepts `["auto", "tdd", "spec"]` but NOT `"prd"`, even though `detect_input_type()` can return `"prd"` and `RoadmapConfig.input_type` accepts it (research/02, Section 1; gaps-and-questions.md, M-3).

Double-routing occurs in `execute_roadmap()` (line 2296) -- `_route_input_files()` is called a second time for `--resume` path consistency (research/02, Section 8).

### 2.4 Prompt Architecture

**Source file:** `src/superclaude/cli/roadmap/prompts.py` (942 lines, 10 prompt-building functions, 4 shared constants)

All prompts are pure Python string construction with no external template files [CODE-VERIFIED] (research/03, Section 15). Each function returns a string that becomes the `-p` argument to `claude`. File inputs are embedded inline by `_embed_inputs()` -- the `--file` flag is explicitly avoided per code comment at executor.py:719-721 (research/04, Section 4).

**Granularity flow through prompts** [CODE-VERIFIED]:

```
Spec/TDD (maximum granularity)
  |
  v  build_extract_prompt / build_extract_prompt_tdd
Extract ----> REDUCES: tables/code blocks become prose sections
  |            8 sections (spec) or 14 sections (TDD)
  v  build_generate_prompt (x2 agents, parallel)
Generate ---> DESTROYS (no TDD) / REDUCES (with TDD)
  |            No task table schema defined. Output structure LLM-invented.
  v  build_diff_prompt
Diff -------> REDUCES: discards agreed content, summarizes divergences only
  |
  v  build_debate_prompt
Debate -----> NEUTRAL: additive analysis, not summarization
  |
  v  build_score_prompt
Score ------> REDUCES: collapses variants into selection + improvement list
  |
  v  build_merge_prompt
Merge ------> PRESERVES-OR-DESTROYS: no ID preservation, no integration
  |            enumeration block, no granularity floor
  v  build_spec_fidelity_prompt
Fidelity ---> MEASURES: validation, catches some losses at dimension level
  |
  v  build_test_strategy_prompt
Test Strat -> PRESERVES (with TDD) / NEUTRAL (without)
```

(research/03, Section 15)

**Three critical prompt gaps** [CODE-VERIFIED] (research/03, Section 13):

1. **No task table schema anywhere.** `build_generate_prompt` says "task rows" and "task table row" but never defines columns. `build_merge_prompt` does not mention task rows at all.

2. **Merge prompt lacks ID preservation.** `build_generate_prompt` (prompts.py:443-444) says "Preserve ALL IDs... Do NOT renumber." `build_merge_prompt` (prompts.py:619-681) has no such instruction. IDs can be silently consolidated or dropped during merge.

3. **Merge prompt lacks `_INTEGRATION_ENUMERATION_BLOCK`.** The generate prompt appends this block (forcing explicit wiring task enumeration), but the merge prompt does not. Wiring tasks enumerated during generation can be lost during merge.

### 2.5 Output Mechanism

**Source files:** `src/superclaude/cli/pipeline/process.py` (lines 24-203), `src/superclaude/cli/roadmap/executor.py` (lines 649-830)

**ClaudeProcess architecture** [CODE-VERIFIED] (research/04, Sections 1-3):

```
[Prompt with all inputs inline]
  |
  v
claude --print --verbose --dangerously-skip-permissions \
       --no-session-persistence --tools default \
       --max-turns 100 --output-format text -p <prompt>
  |
  v
stdout redirected to output_file via OS pipe buffer
stderr redirected to error_file
  |
  v
_sanitize_output() strips conversational preamble before YAML frontmatter
  |
  v
Gate evaluation against output_file on disk
```

**Key constraints** [CODE-VERIFIED]:

| Constraint | Detail | Source |
|-----------|--------|--------|
| One-shot output | `--output-format text` captures only final text response. Tool calls and reasoning suppressed from stdout. | research/04, Section 3.2 |
| No continuation | `--no-session-persistence` always set. No `--continue`, `--session`, or `--resume`. Each step is isolated. | research/04, Section 5.3 |
| No truncation detection | If output hits token limit, file may be incomplete. No mechanism detects this. Gates catch some cases via min_lines. | research/04, Section 5.2 |
| Retry without learning | Retries re-send identical prompt. Partial output from failed attempt is overwritten (`open(file, "w")` truncates). | research/04, Section 8.2 |
| Prompt size ceiling | `_EMBED_SIZE_LIMIT` = 120 KB (executor.py:324). Exceeding logs warning but proceeds. Linux `MAX_ARG_STRLEN` = 128 KB is the hard limit. | research/04, Section 4 |
| Full tool access unused | `--tools default` gives subprocess Read/Write/Edit/Bash access, but all output must go through stdout. The Sprint pipeline uses `stream-json` and tool-use for file writing; the Roadmap pipeline does not. | research/04, Sections 2 and 9 |

**Incremental writing is feasible** but requires coordinated changes across prompt templates, output validation, and sanitization logic. The subprocess already has Write/Edit tool access. Sprint pipeline proves the pattern works (research/04, Section 7).

### 2.6 Gate Architecture

**Source files:** `src/superclaude/cli/roadmap/gates.py`, `src/superclaude/cli/audit/wiring_gate.py`, `src/superclaude/cli/pipeline/gates.py`, `src/superclaude/cli/pipeline/models.py`

The gate system enforces output quality via YAML frontmatter field presence, minimum line counts, and semantic check functions [CODE-VERIFIED] (research/05).

**Gate enforcement tiers** [CODE-VERIFIED] (pipeline/gates.py):

| Tier | Checks |
|------|--------|
| EXEMPT | Always passes |
| LIGHT | File exists + non-empty |
| STANDARD | LIGHT + min_lines + frontmatter field presence |
| STRICT | STANDARD + semantic check functions |

**Gate migration risk assessment** [CODE-VERIFIED] (research/05, Impact Assessment):

| Risk Level | Gates | Reason |
|-----------|-------|--------|
| HIGH (will break) | EXTRACT, EXTRACT_TDD, TEST_STRATEGY, SPEC_FIDELITY, MERGE | Many frontmatter fields and/or cross-field consistency checks tightly coupled to current one-shot output format |
| MEDIUM (might break) | GENERATE_A/B, DIFF, DEBATE, CERTIFY | Light requirements but still need specific frontmatter or body format |
| LOW (will not break) | ANTI_INSTINCT, WIRING, DEVIATION_ANALYSIS, REMEDIATE, SCORE | Non-LLM steps self-generate output, or STANDARD tier with minimal checks |

**Totals:** 15 gate constants, 36 semantic check instances, 31 unique checker functions (26 in roadmap/gates.py + 5 in audit/wiring_gate.py) (research/05, Summary Table).

**Latent bug** [CODE-VERIFIED]: Two frontmatter parsers exist with conflicting behavior. `_parse_frontmatter` in roadmap/gates.py requires frontmatter at byte 0. `_check_frontmatter` in pipeline/gates.py uses `re.MULTILINE` allowing frontmatter after preamble. A semantic check can fail on content where the enforcement engine succeeds (research/05, Gaps, item 1; gaps-and-questions.md, M-6).

**Known bug B-1** [CODE-VERIFIED]: DEVIATION_ANALYSIS_GATE requires frontmatter field `ambiguous_count` but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations` -- field name mismatch (research/05, Gaps, item 2; gaps-and-questions.md, M-7).

### Current State Summary

```
                        ROADMAP PIPELINE DATA FLOW
                        ==========================

  Input Files (spec/TDD/PRD)
       |
       v
  _route_input_files()          <-- 3-layer detection/routing/propagation
       |                             Only extract step diverges on input_type
       v
  +--[1. EXTRACT]--+            <-- FIRST GRANULARITY LOSS: tables/code -> prose
  |  Claude -p      |               One-shot, 300s/1800s timeout
  |  stdout -> file  |               13/19 FM fields required by gate
  +--------+--------+
           |
     +-----+-----+
     v             v
  [2a. GEN-A]  [2b. GEN-B]     <-- SECOND LOSS: no task table schema
  (parallel)   (parallel)           Output structure LLM-invented
     +-----+-----+
           |
           v
  [3. DIFF] -> [4. DEBATE] -> [5. SCORE]
           |                        <-- Diff discards agreements
           v                        <-- Score collapses to selection
  +--[6. MERGE]--+             <-- THIRD LOSS: no ID preservation,
  |  No _INTEGRATION_          |    no enumeration block, no granularity floor
  |  ENUMERATION_BLOCK         |
  +--------+--------+
           |
           v
  [7-12: Validation & Remediation Steps]
  (anti-instinct, test-strategy, spec-fidelity,
   wiring, deviation-analysis, remediate)

  === OUTPUT MECHANISM ===
  Every Claude step: claude --print --output-format text -p <prompt>
  - All inputs embedded inline in prompt (120KB limit)
  - stdout -> file, no streaming, no continuation
  - Truncation undetected; retry restarts from zero
  - Full tool access (--tools default) but unused for output

  === TASKLIST PIPELINE ===
  CLI: validate only (single-step fidelity report)
  Generation: /sc:tasklist skill protocol (800-line inference prompt)
  No CLI generate subcommand exists
  R-item registry not shared between generation and validation
```

**Cross-cutting findings from all research files:**

| Finding | Impact | Status |
|---------|--------|--------|
| Extraction is lossy for structured data (tables, code blocks, field definitions) | Downstream steps work from degraded input | Unfixed |
| No task table schema in generate or merge prompts | Output structure varies per run | Unfixed |
| Merge prompt missing ID preservation + integration enumeration | IDs and wiring tasks silently dropped | Unfixed |
| One-shot stdout capture with no truncation detection | Large outputs silently truncated | Unfixed |
| Tasklist PRD suppression language (prompts.py:221-223) | PRD enrichment blocked from generating tasks | Unfixed (research/08, Section 6) |
| SKILL.md merge directives (lines 233, 255, 259) | Over-consolidation of tasks | Unfixed (research/08, Section 6) |
| No task count floor anywhere in pipeline | No minimum output guarantee | Unfixed (research/08, Section 6) |
| Roadmap generate prompt TDD/PRD blocks updated with anti-consolidation language | Phasing paradigm now mandated | Partially fixed (research/08, Section 3) |
| Certify step (step 13) is dead code | build_certify_step() defined but never called | Stale code |
| Dual frontmatter parser bug | Semantic checks can fail on valid content | Latent bug |
