# Synthesis: Target State & Gap Analysis

**Date:** 2026-04-04
**Sources:** research/01 through research/08, research/web-01, research/web-02, gaps-and-questions.md
**Scope:** Sections 3 (Target State) and 4 (Gap Analysis) of the overhaul research report

---

## Section 3: Target State

### 3.1 Desired Behavior

The target architecture replaces the current extraction-based one-shot pipeline with a **template-driven incremental-write** system. The following table summarizes desired behaviors per pipeline phase.

| Phase | Current Behavior | Target Behavior | Source |
|-------|-----------------|-----------------|--------|
| **Input consumption** | Extraction step summarizes spec/TDD into lossy prose (8-14 sections) | Structured inputs (TDD/PRD) bypass extraction; spec-only inputs retain extraction with table-preserving instructions | research/02, research/03, research/08 |
| **Roadmap generation** | Single `claude --print` stdout capture; no task table schema; LLM invents output structure per run | Template file defines section headers, table schemas, required columns; LLM fills dynamic slots via tool-use Write calls | research/03, research/07, web-02 |
| **Merge step** | No ID preservation instruction; no integration enumeration block; no granularity floor | Merge prompt enforces same structural constraints as generate prompt; template schema carries through merge | research/03 |
| **Output capture** | `--output-format text` captures final text blob from stdout; no progress visibility | Subprocess writes output files directly via Write/Edit tools; orchestrator validates file existence and content | research/04, web-01 |
| **Gate validation** | Gates check YAML frontmatter fields and semantic rules on stdout-captured files | Gates check tool-written files; same frontmatter+semantic validation; templates guarantee structural compliance | research/05 |
| **Tasklist generation** | Inference-only via 800-line skill protocol; no CLI generate command; R-items parsed non-deterministically | CLI `tasklist generate` subcommand backed by template-driven subprocess pipeline; shared R-item registry between generation and validation | research/06 |
| **Output format** | Free-form markdown; structure varies per run and per agent persona | Template-enforced markdown with defined section order, table column schemas, and sentinel-validated completeness | research/07 |

### Target Architecture (ASCII Diagram)

```
                          +------------------+
                          |   Input Files    |
                          | (spec, TDD, PRD) |
                          +--------+---------+
                                   |
                          +--------v---------+
                          | Input Router     |
                          | (detect_input_   |
                          |  type + route)   |
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
                   |                              |
                   +---------- + -----------------+
                               |
                    +----------v-----------+
                    | Template-Driven      |
                    | Generate (per-agent) |
                    |                      |
                    | 1. Read template     |
                    | 2. Fill sections     |
                    |    via Write tool    |
                    | 3. Validate per-     |
                    |    section minimums  |
                    +----------+-----------+
                               |
                    +----------v-----------+
                    | Adversarial Steps    |
                    | (diff, debate,       |
                    |  score, merge)       |
                    | Merge uses same      |
                    | template constraints |
                    +----------+-----------+
                               |
                    +----------v-----------+
                    | Validation Steps     |
                    | (spec-fidelity,      |
                    |  anti-instinct,      |
                    |  wiring, deviation,  |
                    |  remediate)          |
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

| # | Criterion | Metric | Threshold | Source |
|---|-----------|--------|-----------|--------|
| SC-1 | No output truncation | Steps complete without hitting `--print` token cap | 0 truncated outputs per pipeline run | web-01 (Finding 3.4: 64k non-streaming cap) |
| SC-2 | Task count preservation | TDD+PRD input produces >= spec-only task count for same functional domain | R-item count(TDD+PRD) >= R-item count(spec-only) | research/08 (44 vs 87 regression) |
| SC-3 | Structural consistency | Roadmap output matches template section order and table schemas across runs | 100% section presence; 100% column compliance | research/03, research/07 |
| SC-4 | ID traceability | Every spec/TDD requirement ID appears in roadmap and traces to >= 1 tasklist item | 0 orphaned IDs | research/03 (generate prompt says "Each ID must appear as a separate task row") |
| SC-5 | Gate compatibility | All existing gates pass on template-driven output without gate definition changes | 0 gate regressions (gates that passed before still pass) | research/05 (gate break analysis) |
| SC-6 | Incremental progress visibility | Orchestrator can observe per-section completion during generation | >= 1 progress signal per template section | research/04, web-01 |
| SC-7 | Tasklist CLI generation | `superclaude tasklist generate` produces Sprint-compatible bundle from roadmap | Phase files pass `superclaude sprint run` input validation | research/06 |
| SC-8 | Table-format preservation | Tables, code blocks, and field-level definitions from TDD pass through to roadmap without lossy prose conversion | 0 table-to-prose conversions in extraction or generation | research/03 (extraction granularity impact) |
| SC-9 | Merge fidelity | Merged roadmap preserves all IDs and integration wiring from both variants | 0 ID drops; integration enumeration block present in merge prompt | research/03 (merge prompt gaps) |
| SC-10 | Sentinel validation | Template sentinels (`{{SC_PLACEHOLDER:*}}`) are zero after generation | `grep -c '{{SC_PLACEHOLDER:' output` returns 0 | research/07 (release-spec pattern) |

### 3.3 Constraints

| # | Constraint | Rationale | Source |
|---|-----------|-----------|--------|
| CON-1 | Must not break existing `--resume` workflow | State file `.roadmap-state.json` is the inter-session recovery mechanism; template migration cannot invalidate existing state files | research/01 (Section 6, state management) |
| CON-2 | Must preserve backward compatibility for spec-only inputs | Spec-only is the most common input type; extraction bypass is TDD/PRD-specific | research/02 (input routing) |
| CON-3 | Gate definitions for non-LLM steps (anti-instinct, wiring, deviation, remediate) must not change | These steps generate their own output format; gates validate self-produced content | research/05 (NO-break gates: 8, 11, 12, 13) |
| CON-4 | Linux `MAX_ARG_STRLEN` limit (128 KB) for `-p` prompt flag | Prompt size ceiling remains even with incremental output; input embedding must still fit | research/04 (Section 4, `_EMBED_SIZE_LIMIT`) |
| CON-5 | `--no-session-persistence` must remain for pipeline isolation | Cross-session state leakage would break parallel pipeline runs | web-01 (Section 5, session persistence) |
| CON-6 | Template files must be distributable via `superclaude install` | Templates live in `src/superclaude/` and deploy to `~/.claude/`; existing install path must work | CLAUDE.md (Component Sync section) |
| CON-7 | Sprint pipeline compatibility for tasklist output | Phase files must start with `# Phase N -- <Name>` (level 1 heading, em-dash separator) | research/06 (Section 3.5) |
| CON-8 | `--tools default` and `--dangerously-skip-permissions` remain the subprocess permission model | Changing permission flags would affect all pipelines, not just roadmap | web-01 (Section 3) |
| CON-9 | Coexistence during migration | Template-driven output must coexist with current output format during transition; a `--legacy` flag or automatic fallback is needed | gaps-and-questions.md (Q5) |
| CON-10 | Template versioning | Templates are versioned artifacts; changes to template structure must not silently break existing gate definitions | research/07 (Pattern 5: Downstream Awareness) |

---

## Section 4: Gap Analysis

### 4.1 Gap Table

| # | Gap | Current State | Target State | Severity | Notes |
|---|-----|--------------|-------------|----------|-------|
| **G-01** | **Extraction destroys structured data granularity** | `build_extract_prompt` produces 8 prose sections from spec input. Tables, code blocks, and field-level type/constraint definitions are rewritten as narrative text. TDD extraction (14 sections) is better but still lossy -- no instruction to preserve original table/code-block formats. | Structured inputs (TDD/PRD) bypass extraction entirely and feed directly to generation. Spec-only extraction includes explicit table-preservation instructions ("preserve markdown tables and code blocks in their original format"). | **Critical** | Primary granularity loss point. research/03 rates extraction as "REDUCES -- lossy summarization." The extraction-to-prose conversion is the root cause of downstream data fidelity problems. |
| **G-02** | **One-shot stdout capture architecture** | Each pipeline step runs `claude --print --output-format text`, capturing only the final text response to stdout. No intermediate output visibility. Non-streaming fallback caps at 64k tokens. No truncation detection. No continuation logic. Failed retries restart from zero. | Subprocess writes output files directly via Write/Edit tools within a single `--print` agentic session. Orchestrator validates file existence/content after subprocess exit. Optional `stream-json` for progress monitoring. | **Critical** | research/04 Section 7.3 confirms feasibility: subprocess already has `--tools default` + `--dangerously-skip-permissions`. web-01 Finding 3 confirms Claude CAN write files in current setup. web-01 Finding 3.4 identifies 64k non-streaming cap as root cause of truncation. |
| **G-03** | **No roadmap output template** | Roadmap structure is entirely LLM-invented. `build_generate_prompt` says "task rows" but defines no table columns. `build_merge_prompt` has no structural constraints. Output format varies per run and per agent persona. | Roadmap output template with PART 1 (generation instructions) / PART 2 (output skeleton) following MDTM pattern. Defined section order, table column schemas, sentinel validation. | **Critical** | research/07 Gap 1: "No Existing Roadmap Output Template." research/03 Gap 1: "No task table schema anywhere." The absence of a template is the architectural root cause of structural inconsistency. |
| **G-04** | **No tasklist output template** | Tasklist bundle format defined by convention in 800-line SKILL.md protocol. No enforceable template. No CLI generate command. `build_tasklist_generate_prompt()` is dead code (never called by CLI). | Tasklist output template with defined section structure. CLI `tasklist generate` subcommand backed by template-driven subprocess pipeline. | **Critical** | research/06 Gap 1, research/07 Gap 2. The skill protocol IS the template, but it runs in inference-only mode with no programmatic enforcement. |
| **G-05** | **Merge prompt lacks ID preservation** | `build_generate_prompt` says "Preserve ALL IDs... Do NOT renumber." `build_merge_prompt` has NO such instruction. Merge can silently consolidate or drop IDs. `_INTEGRATION_ENUMERATION_BLOCK` is appended to generate but NOT to merge. | Merge prompt includes identical ID preservation instructions and `_INTEGRATION_ENUMERATION_BLOCK` as generate prompt. Template schema enforces ID column presence in all task tables. | **High** | research/03 Gaps 2-3. The merge step is the most dangerous granularity bottleneck because it operates on already-reduced data with fewer safeguards than the generate step. |
| **G-06** | **No granularity floor in any prompt** | No prompt specifies minimum task row counts. The only approximation is the TDD block's "MORE roadmap task rows than a 312-line spec, not fewer" -- relative guidance, not a count-based floor. | Template defines per-section minimum content requirements. Gate semantic checks enforce minimum row counts in task tables (e.g., task_count >= extraction_requirement_count). | **High** | research/03 Gap 4. Without a floor, the LLM consolidates freely. research/08 H5 confirms ~112 work items bundled into 44 R-items with no enforcement. |
| **G-07** | **Gate fragility under format changes** | 5 gates will definitely break (EXTRACT, EXTRACT_TDD, MERGE, TEST_STRATEGY, SPEC_FIDELITY) if output format changes. These have 13-19 frontmatter fields and cross-field semantic consistency checks tightly coupled to one-shot LLM output format. | Template-driven output emits identical frontmatter keys. Gate definitions remain stable because templates guarantee the fields gates expect. Gate update path documented for each affected gate. | **High** | research/05 Summary Table: 5 YES-break gates, 4 MAYBE-break gates, 5 NO-break gates. Migration must include a gate compatibility matrix. |
| **G-08** | **PRD suppression in tasklist prompt** | `tasklist/prompts.py` lines 221-223: "PRD context... does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them." This is the single strongest root cause of task count regression. | PRD content generates additional task rows for compliance gates, persona acceptance tests, and success metric validation -- NOT just enrichment of existing tasks. Anti-consolidation guard added. | **High** | research/08 H2/G1. CODE-VERIFIED still present and unfixed. The prior research (2026-04-03) identified this as the highest-impact single cause of 49% task reduction. |
| **G-09** | **SKILL.md protocol merge directives** | 3+ merge instructions with vague matching criteria: "Merge rather than duplicate if a generated task duplicates an existing task for the same component" (line 233), "merge with existing feature task if one covers the same goal" (line 259). | Merge criteria tightened to require exact ID match or explicit justification. Merge count tracked in output metadata. Anti-pattern: merging tasks with different acceptance criteria. | **High** | research/08 H4/G2. CODE-VERIFIED still present. These directives cause the tasklist generator to over-consolidate. |
| **G-10** | **Diff step discards agreed content** | `build_diff_prompt` counts shared assumptions but does not preserve them in detail. If both variants correctly preserved a requirement, that preservation is reduced to a count, not reinforced. | Diff output includes a "Shared Structure" section preserving agreed-upon task tables verbatim. Divergence analysis operates on top of preserved base. | **Medium** | research/03 Section 5 rates diff as "REDUCES -- discards agreed content." The loss is moderate because the original variants are still available to the merge step. |
| **G-11** | **Score step's free-form improvement list** | Score step Section 5 ("specific improvements from non-base variant to incorporate") is free-form prose. Merge relies on this summary to know what to incorporate. Vaguely described improvements get lost. | Score output uses a structured table: Improvement ID, Source Variant, Section, Description, Priority. Merge prompt references improvements by ID. | **Medium** | research/03 Section 7: "the merge step relies on this summary to know what to incorporate." |
| **G-12** | **No task table schema defined anywhere** | Generate prompt says "task rows" and "task table row" but never defines columns. Merge prompt doesn't mention task rows at all. | Template defines a canonical task table schema: `| Task ID | Phase | Description | Dependencies | Acceptance Criteria | Complexity | Files |`. All prompts reference this schema. | **Medium** | research/03 Gap 1. The most fundamental missing artifact. Without a schema, every LLM run invents its own column structure. |
| **G-13** | **Tasklist R-item identity gap** | R-items (`R-001`, `R-002`) are assigned by the generation-time LLM. Validation-time LLM independently re-derives R-items from the roadmap. No shared registry. No guarantee of consistent parsing. | Roadmap output includes a machine-readable R-item registry section (table with R-ID, source heading, line number). Both generation and validation consume this registry. | **Medium** | research/06 Gap 2, Section 5.3. |
| **G-14** | **Tasklist one-shot output limits** | Generation skill produces N+1 files in a single session. Large roadmaps (10+ phases, 100+ tasks) push against context window limits. No chunking or phase-by-phase generation strategy. | Template-driven CLI pipeline generates one phase file per subprocess invocation. Each phase file is bounded. Index file assembled after all phases complete. | **Medium** | research/06 Section 5.4. |
| **G-15** | **Two frontmatter parsers with conflicting behavior** | `_parse_frontmatter` in `roadmap/gates.py` requires frontmatter at byte 0. `_check_frontmatter` in `pipeline/gates.py` uses `re.MULTILINE` and allows frontmatter after preamble. Semantic checks can fail on valid content if LLM emits preamble. | Single frontmatter parser used by all gates. Template-driven output eliminates preamble issue (Write tool produces clean content). | **Medium** | research/05 Gap 1. Latent bug for all STRICT gates. |
| **G-16** | **No anti-consolidation guard in tasklist prompts** | No instruction prevents the LLM from merging distinct tasks into single coarser items. The merge directives (G-09) actively encourage consolidation. | Explicit anti-consolidation guard: "Do NOT merge tasks that have different acceptance criteria, different deliverable types, or different dependency chains." Task count assertion: output task count >= input R-item count. | **Medium** | research/08 G9. CODE-VERIFIED absent. |
| **G-17** | **Testing task absorption** | TDD+PRD produces 5 standalone test tasks vs spec-only's 28 (5.6:1 ratio). Testing is absorbed into `[VERIFICATION]` steps within implementation tasks. | Minimum standalone test task count derived from extraction's `test_artifacts_identified`. Test tasks not eligible for merge with implementation tasks. | **Medium** | research/08 H3/G6. Output behavior observation -- cannot verify without re-running pipeline. |
| **G-18** | **`build_certify_step()` is dead code** | Function defined at `executor.py:1259` but never called anywhere. Step 13 (certify) is described in comments but not wired into `_build_steps()` or `execute_roadmap()`. | Either wire the certify step into the pipeline or remove the dead code. If retained, add to `_build_steps()` with appropriate gate. | **Low** | research/01 Gap 1. Confirmed via grep: zero callers in `src/superclaude/cli/roadmap/`. |
| **G-19** | **Deviation-analysis gate field name mismatch** | Gate requires frontmatter field `ambiguous_count` but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations`. Known bug B-1 in `gates.py`. | Fix field name to be consistent. Either both use `ambiguous_count` or both use `ambiguous_deviations`. | **Low** | research/05 Gap 2. |
| **G-20** | **Wiring-verification prompt asks for code analysis from a planning document** | Prompt's 3 defect classes (Optional[Callable] wiring, orphan modules, unregistered dispatch entries) are code-level concerns analyzed from a roadmap planning document. Results may be unreliable. | Scope wiring-verification to architectural wiring validation (does the roadmap include explicit wiring tasks?) rather than code-level static analysis it cannot actually perform. | **Low** | research/03 Section 10 anomaly. |
| **G-21** | **Stale step count documentation** | Module docstring says "9-step pipeline"; `roadmap_group` docstring says "8-step pipeline". Actual pipeline has 12+ steps. Duplicate "Step 8" comment for both test-strategy and spec-fidelity. | Update all docstrings and comments to reflect actual 12-step pipeline. | **Low** | research/01 Section 12. |

### 4.2 Gap Severity Distribution

```
Critical (4):  G-01, G-02, G-03, G-04
High (5):     G-05, G-06, G-07, G-08, G-09
Medium (8):   G-10, G-11, G-12, G-13, G-14, G-15, G-16, G-17
Low (4):      G-18, G-19, G-20, G-21
               _______________
Total: 21 gaps
```

### 4.3 Gap Dependency Map

The following gaps have ordering dependencies -- resolving one is a prerequisite or enabler for resolving others.

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

**Critical path**: G-03 (roadmap template) is the highest-fan-out dependency. It must be resolved first because 5 other gaps depend on having a defined output structure. G-02 (incremental write) is the highest-risk change but has only 1 direct dependent.

### 4.4 Cross-Reference: Gaps to Research Files

| Gap | Primary Research Source | Supporting Sources |
|-----|----------------------|-------------------|
| G-01 | `research/03-prompt-architecture.md` (Sections 2-3) | `research/02-input-routing.md`, `research/08-prior-research-context.md` |
| G-02 | `research/04-claude-process-output.md` (Sections 3, 7) | `research/web-01-claude-cli-output.md`, `research/web-02-incremental-generation.md` |
| G-03 | `research/07-template-patterns.md` (Gaps section) | `research/03-prompt-architecture.md` |
| G-04 | `research/06-tasklist-pipeline.md` (Section 1) | `research/07-template-patterns.md` |
| G-05 | `research/03-prompt-architecture.md` (Section 8, Gaps 2-3) | -- |
| G-06 | `research/03-prompt-architecture.md` (Gap 4) | `research/08-prior-research-context.md` (G3, G5) |
| G-07 | `research/05-gate-architecture.md` (Impact Assessment) | -- |
| G-08 | `research/08-prior-research-context.md` (Section 4, H2) | `research/06-tasklist-pipeline.md` |
| G-09 | `research/08-prior-research-context.md` (Section 4, H4) | -- |
| G-10 | `research/03-prompt-architecture.md` (Section 5) | -- |
| G-11 | `research/03-prompt-architecture.md` (Section 7) | -- |
| G-12 | `research/03-prompt-architecture.md` (Gap 1) | `research/07-template-patterns.md` |
| G-13 | `research/06-tasklist-pipeline.md` (Section 5.3) | -- |
| G-14 | `research/06-tasklist-pipeline.md` (Section 5.4) | `research/web-02-incremental-generation.md` |
| G-15 | `research/05-gate-architecture.md` (Gap 1) | -- |
| G-16 | `research/08-prior-research-context.md` (G9) | -- |
| G-17 | `research/08-prior-research-context.md` (H3/G6) | -- |
| G-18 | `research/01-pipeline-step-map.md` (Gap 1) | -- |
| G-19 | `research/05-gate-architecture.md` (Gap 2) | -- |
| G-20 | `research/03-prompt-architecture.md` (Section 10 anomaly) | -- |
| G-21 | `research/01-pipeline-step-map.md` (Section 12) | -- |
