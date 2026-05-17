# Section 9: Open Questions & Section 10: Evidence Trail

**Synthesis Date**: 2026-04-04
**Sources**: All research files (01-08), web research files (web-01, web-02), gaps-and-questions.md
**Status**: Complete

---

## Section 9: Open Questions

### 9.1 Unresolved Gaps from gaps-and-questions.md

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q-01 | Step numbering inconsistency in executor.py comments (duplicate "Step 8" for test-strategy and spec-fidelity) | LOW | Fix comments: renumber spec-fidelity as Step 9 and all subsequent steps accordingly |
| Q-02 | `convergence_enabled` has no CLI flag -- programmatic only. Should it be exposed? | MEDIUM | Add `--convergence` flag to CLI, or document as internal-only if not ready for users |
| Q-03 | `--input-type` CLI accepts `auto/tdd/spec` but not `prd`. Users cannot force PRD classification if auto-detection misclassifies. | MEDIUM | Add `prd` to `--input-type` Choice list in commands.py |
| Q-04 | TDD/PRD section references in prompts use hardcoded section numbers (e.g., "S7", "S15", "S19"). Template changes will break references. | MEDIUM | Replace hardcoded section numbers with section-name-based references or make them configurable |
| Q-05 | Neither `build_diff_prompt` nor `build_debate_prompt` accept tdd_file/prd_file parameters -- is this intentional? | MEDIUM | User decision needed: either add TDD/PRD context to diff/debate for enriched comparison, or document the intentional scoping |
| Q-06 | Latent frontmatter parser bug -- `_parse_frontmatter` (roadmap/gates.py) requires FM at byte 0, `_check_frontmatter` (pipeline/gates.py) allows FM after preamble. Both are applied in STRICT gates. | HIGH | Unify parsers: adopt the pipeline/gates.py regex-based parser for all frontmatter reads, or ensure `_sanitize_output()` always strips preamble before semantic checks run |
| Q-07 | Field name mismatch in DEVIATION_ANALYSIS_GATE: frontmatter requires `ambiguous_count` but semantic check reads `ambiguous_deviations` (known bug B-1) | HIGH | Fix field name to be consistent: either rename the frontmatter field or the semantic check function |

### 9.2 Open Design Questions from gaps-and-questions.md

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q-08 | What is the optimal incremental writing strategy -- subprocess tool-use (Sprint pattern) vs streaming output with checkpoints? | HIGH | Research finding: tool-use file writing is lowest effort (web-01 Finding 3). Sprint already uses this. Recommend tool-use approach with `stream-json` for observability. |
| Q-09 | Should extraction be removed entirely for TDD/PRD or retained as optional with a bypass flag? | HIGH | User decision needed. Extraction is lossy (file 03 analysis), but TDD extraction preserves more structure than spec extraction. Recommend: bypass for TDD primary input, retain for spec-only. |
| Q-10 | How should the roadmap output template handle variable-length content (many phases vs few)? | MEDIUM | Adopt tiered usage model from TDD template (file 07): Lightweight (3-5 phases), Standard (5-8), Heavyweight (8+). Each tier has section requirements. |
| Q-11 | Should tasklist generation move from skill-only to CLI pipeline, or should the skill be enhanced? | HIGH | User decision needed. `build_tasklist_generate_prompt()` exists but is never called by CLI (file 06). Options: (A) add `tasklist generate` CLI subcommand, (B) keep skill-only but fix protocol merge directives, (C) both. |
| Q-12 | What is the migration path -- can template-driven output coexist with current output during transition? | MEDIUM | Yes. Template can be opt-in via `--template` flag. Default behavior unchanged. Gates validate both formats if template emits required frontmatter. |

### 9.3 UNVERIFIED Claims from Research Files

| # | Claim | Source | Impact | Suggested Resolution |
|---|-------|--------|--------|----------------------|
| Q-13 | ~112 discrete work items get bundled into 44 R-items in TDD+PRD roadmap (2.5:1 bundling ratio) | File 08, H5 | HIGH | Cannot verify against code -- depends on LLM output behavior. Re-run pipeline with current (partially fixed) prompts to measure actual bundling ratio. |
| Q-14 | TDD+PRD produces 5 standalone test tasks vs baseline's 28 (5.6:1 testing absorption ratio) | File 08, H3 | MEDIUM | Output-level observation. Cannot verify without re-running pipeline. New test fixtures needed under current prompts. |
| Q-15 | Section 3.x framing in SKILL.md primes consolidation behavior | File 08, G8 | LOW | LLM-behavioral claim, not code-structural. May be mitigated by anti-consolidation guards if added. |
| Q-16 | `--file` flag is a cloud download mechanism and does not inject local file content | File 04, executor.py comment | MEDIUM | May be stale. Verify against current `claude --help` output. If fixed, `--file` could replace inline embedding and solve the 120KB prompt size limit. |
| Q-17 | `--print` mode non-streaming fallback caps at 64k tokens with 300s timeout | File web-01, Finding 3.4 | HIGH | Based on GitHub issue #14888 and support docs. Verify against current Claude CLI version. If true, this is the root cause of output truncation for large artifacts. |

### 9.4 Questions Raised in Research File "Gaps and Questions" Sections

| # | Question | Source | Impact | Suggested Resolution |
|---|----------|--------|--------|----------------------|
| Q-18 | Should `build_merge_prompt` append `_INTEGRATION_ENUMERATION_BLOCK` like `build_generate_prompt` does? | File 03, Gap 1 | HIGH | Yes. Merge currently drops integration wiring tasks that generate preserved. Add the block to merge prompt. |
| Q-19 | Should `build_merge_prompt` include explicit "Preserve ALL IDs" instruction? | File 03, Gap 2 | HIGH | Yes. Generate has this instruction; merge does not. IDs can be silently dropped during merge. |
| Q-20 | Should there be a defined task table schema (columns, required fields) enforced by both generate and merge prompts? | File 03, Gap 3 | HIGH | Yes. This is the single largest structural gap. No prompt defines what columns a task row must have. The LLM invents its own table structure per run. |
| Q-21 | Should extract prompts instruct the LLM to preserve original table/code-block formats rather than rewriting into prose? | File 03, Gap 5 | MEDIUM | Yes for TDD inputs (which contain structured tables/code). Less critical for prose-heavy specs. |
| Q-22 | Is `build_wiring_verification_prompt` producing useful output? It asks for code-level static analysis from a planning document. | File 03, Gap 5 (wiring) | LOW | Likely producing unreliable results. The prompt's 3 defect classes are code-level concerns inferred from planning text. Consider removing or reclassifying as advisory. |
| Q-23 | Certify step (step 13) is dead code -- `build_certify_step()` is defined but never called. Should it be removed or wired in? | File 01, Gap 1 | MEDIUM | User decision needed. Either wire `build_certify_step()` into `execute_roadmap()` after remediate, or remove the dead code. |
| Q-24 | Single-agent mode runs diff/debate/score on identical outputs. Should this be detected and skipped? | File 01, Gap 5 | LOW | Add guard: if `len(config.agents) == 1`, skip steps 3-5 (diff, debate, score) and use the single variant as the merged roadmap. |
| Q-25 | `_EMBED_SIZE_LIMIT` = 120KB may cause E2BIG errors on Linux. Should the pipeline fail-fast or switch to tool-use? | File 01, Gap 6; File 04, Gap 3 | HIGH | Fail-fast with actionable error message. Long-term: switch to tool-use file writing which bypasses the kernel arg length limit entirely. |
| Q-26 | No truncation detection for Claude subprocess output. A step could produce syntactically incomplete output that passes LIGHT gate. | File 04, Gap 1 | HIGH | Add truncation detection: check if output ends mid-sentence or mid-YAML-block. Add a `content_complete` semantic check to STRICT gates. |
| Q-27 | Retry without learning -- retries re-send identical prompt. If the task was too large, retry will fail identically. | File 04, Gap 2 | MEDIUM | On retry, append prior failure context (e.g., "Previous attempt was truncated at section X. Focus output on remaining sections.") |
| Q-28 | Why was `text` output format chosen over `stream-json` for roadmap? Sprint uses `stream-json` successfully. | File 04, Gap 4 | MEDIUM | Historical decision. `stream-json` would enable progress monitoring, tool-call visibility, and early failure detection. Recommend switching. |
| Q-29 | No CLI generate subcommand for tasklist. Why does `build_tasklist_generate_prompt()` exist if never called? | File 06, Gap 1 | MEDIUM | Prompt builder exists as reference for the skill protocol. Either add `tasklist generate` CLI subcommand or remove/deprecate the unused function. |
| Q-30 | R-item identity gap: generator assigns R-IDs, validator re-derives them independently. No shared registry. | File 06, Gap 2 | HIGH | Add R-item registry as pipeline artifact. Generator writes it; validator reads it. Eliminates identity divergence. |
| Q-31 | No extraction step for tasklist validation. Should structured intermediary precede both generation and validation? | File 06, Gap 3 | MEDIUM | Yes. A roadmap-to-structured-items extraction would enable systematic comparison. Mirrors the roadmap pipeline's extraction step. |
| Q-32 | Tasklist fidelity prompt says "Do NOT compare against original specification" but adds supplementary TDD/PRD checks. Is this a contradiction? | File 06, Gap 6 | LOW | Not a contradiction: the base comparison is roadmap-to-tasklist only; TDD/PRD checks are supplementary dimensions, not spec-to-tasklist comparisons. Document this distinction explicitly. |
| Q-33 | 100KB embedding limit for tasklist -- logged warning but embedding proceeds. What happens when composed prompt exceeds model context? | File 06, Gap 7 | MEDIUM | Model silently truncates context. Add fail-fast check: if composed prompt exceeds 80% of model context window, abort with actionable error. |
| Q-34 | No existing roadmap output template. Should one be created? | File 07, Gap 1 | HIGH | Yes. Adopt PART 1/PART 2 pattern from MDTM template. PART 1 = generation rules. PART 2 = output skeleton with `{{SC_PLACEHOLDER:*}}` sentinels. |
| Q-35 | No existing tasklist output template. Should one be created? | File 07, Gap 2 | HIGH | Yes. Same pattern as roadmap template. Include Sprint CLI compatibility requirements (heading format, file naming convention). |
| Q-36 | Should sentinel convention be `{{SC_PLACEHOLDER:*}}` or roadmap-specific `{{ROADMAP:*}}`? | File 07, Gap Q2 | LOW | Use `{{SC_PLACEHOLDER:*}}` for consistency with Release Spec template. Prefix the descriptor name for namespace (e.g., `{{SC_PLACEHOLDER:roadmap_title}}`). |
| Q-37 | How should tiered usage model map to roadmaps? By spec count, complexity class, or feature count? | File 07, Gap Q3 | MEDIUM | Use complexity_class from extraction (LOW/MEDIUM/HIGH). This is already computed and available in frontmatter. Maps cleanly to Lightweight/Standard/Heavyweight tiers. |
| Q-38 | Should roadmap template enforce section ordering or allow LLM to organize by theme/priority? | File 07, Gap Q4 | MEDIUM | Enforce ordering. Template-driven generation requires predictable structure for gate validation and downstream tasklist consumption. |
| Q-39 | When were the roadmap prompt fixes (TDD phasing, PRD phase count protection) applied? Before or after test fixture runs? | File 08, Q6 | HIGH | If before: the 3-phase collapse should not have occurred in fixtures. If after: new test runs needed. Determine by checking git blame on prompts.py TDD/PRD blocks. |
| Q-40 | Are the partial roadmap prompt fixes sufficient, given tasklist prompt (G1, G9, G10) and SKILL.md (G2, G3, G12) remain unfixed? | File 08, Q7 | HIGH | Likely not. Even if roadmap is now granular, tasklist merge directives can still over-consolidate. Both layers need fixing. |
| Q-41 | Test fixture staleness: do fixtures in `.dev/test-fixtures/results/` predate roadmap prompt fixes? | File 08, Q8 | MEDIUM | Check fixture timestamps vs prompts.py modification date. If stale, new fixtures needed to validate current behavior. |
| Q-42 | Should `--bare` mode be adopted for pipeline subprocesses? Anthropic recommends it for scripted/SDK calls. | File web-01, Finding 5.4 | LOW | Yes, eventually. `--bare` skips CLAUDE.md, hooks, skills, plugins, MCP servers -- cleaner isolation. But verify no pipeline steps depend on these. |
| Q-43 | Should roadmap steps switch from `output_format="text"` to `output_format="stream-json"` for observability? | File web-01, Rec 2 | MEDIUM | Yes. Sprint already uses `stream-json`. Enables progress monitoring, tool-call visibility, and early failure detection. Medium effort. |
| Q-44 | Should Anthropic's structured outputs (`output_config` with JSON schema) be used for intermediate artifacts? | File web-02, Finding 4.1 | MEDIUM | Yes for extraction and base-selection (structured data). No for roadmap/tasklist (large markdown content). |

---

## Section 10: Evidence Trail

### 10.1 Codebase Research Files

| File | Topic | Agent Type |
|------|-------|------------|
| `research/01-pipeline-step-map.md` | Complete pipeline step trace: CLI entry through 12-step execution, step builder, step runner, generic pipeline executor, gate evaluation, data flow, architectural patterns | Code Tracer |
| `research/02-input-routing.md` | Input routing: `detect_input_type()` weighted scoring, `_route_input_files()` 12-step algorithm, `_embed_inputs()` inline embedding, TDD-as-spec_file semantic confusion, propagation through all pipeline steps | Code Tracer |
| `research/03-prompt-architecture.md` | All 10 prompt-building functions: format requested, granularity impact assessment (REDUCES/DESTROYS/NEUTRAL/PRESERVES/MEASURES), shared constants, per-prompt minimum counts, template references, 6 critical gaps identified | Code Tracer |
| `research/04-claude-process-output.md` | ClaudeProcess subprocess wrapper: CLI flags, output capture mechanism (one-shot stdout), input embedding (120KB limit), token limits, retry without learning, incremental writing feasibility assessment, sprint vs roadmap comparison | Code Tracer + Architecture Analyst |
| `research/05-gate-architecture.md` | All 15 gate constants: per-gate enforcement tier, frontmatter fields, semantic checks, format migration risk assessment (YES/MAYBE/NO), 31 checker function inventory, latent frontmatter parser bug, field name mismatch bug B-1 | Code Tracer |
| `research/06-tasklist-pipeline.md` | Tasklist pipeline: CLI validate-only vs skill generate, `build_tasklist_generate_prompt()` dead code, R-item parsing (LLM-driven non-deterministic), phase bucketing, task decomposition, multi-file output, R-item identity gap, one-shot output limits | Code Tracer |
| `research/07-template-patterns.md` | 4 existing templates analyzed: TDD (tiered usage, completeness checklist, contract table), Release Spec (SC_PLACEHOLDER sentinels, conditional sections), PRD (SCOPE NOTE comments, anti-persona), MDTM (PART 1/PART 2 separation, 6-element checklist pattern, handoff conventions). 5 cross-template patterns synthesized. Recommended roadmap/tasklist template structures. | Pattern Investigator |
| `research/08-prior-research-context.md` | Prior tasklist-quality research (2026-04-03): 49% task count regression root causes (5 hypotheses), 12-gap registry with verification status, pipeline trace (collapse at Stage 2), partial fix assessment (roadmap prompts partially fixed, tasklist prompts/SKILL.md unfixed), CODE-VERIFIED/UNVERIFIED/CODE-CONTRADICTED tagging | Doc Analyst |
| `research/research-notes.md` | Research planning notes: file inventory (5,470 lines roadmap CLI, 861 lines pipeline framework, 738 lines tasklist CLI), patterns and conventions, solution research areas, recommended outputs, suggested phases | Research Planner |

### 10.2 Web Research Files

| File | Topic |
|------|-------|
| `research/web-01-claude-cli-output.md` | Claude CLI `--output-format` options (text/json/stream-json), model output token limits by tier (Opus 4.6: 128k, Sonnet 4.6: 64k, Haiku 4.5: 64k), tool-use mode with `--tools default` + `--dangerously-skip-permissions`, `--max-turns` behavior, `--print` multi-turn capability, `--continue`/`--resume` session continuation, `--bare` mode recommendation |
| `research/web-02-incremental-generation.md` | Incremental generation patterns: chunk-based decomposition (Addy Osmani), hierarchical chunking strategies, template-driven hybrid generation (iEcoreGen), skeleton-of-thought prompting, prompt chaining, prefill/anchor technique, Claude Code agentic write pattern, function calling as format enforcement, constrained decoding, Anthropic structured outputs, ICLR 2025 long-form benchmarks |

### 10.3 Gaps Log

| Artifact | Path |
|----------|------|
| Gaps and Questions file | `.dev/tasks/to-do/TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/gaps-and-questions.md` |

### 10.4 Complete Research Directory Listing

All `*.md` files produced in the `research/` directory:

| # | File | Type |
|---|------|------|
| 1 | `research/01-pipeline-step-map.md` | Codebase research |
| 2 | `research/02-input-routing.md` | Codebase research |
| 3 | `research/03-prompt-architecture.md` | Codebase research |
| 4 | `research/04-claude-process-output.md` | Codebase research |
| 5 | `research/05-gate-architecture.md` | Codebase research |
| 6 | `research/06-tasklist-pipeline.md` | Codebase research |
| 7 | `research/07-template-patterns.md` | Codebase research |
| 8 | `research/08-prior-research-context.md` | Codebase research |
| 9 | `research/web-01-claude-cli-output.md` | Web research |
| 10 | `research/web-02-incremental-generation.md` | Web research |
| 11 | `research/research-notes.md` | Research planning |

### 10.5 Synthesis Files Produced

| # | File | Sections Covered |
|---|------|-----------------|
| 1 | `synthesis/synth-03-external-findings.md` | S5 External Research Findings |
| 2 | `synthesis/synth-06-questions-evidence.md` | S9 Open Questions, S10 Evidence Trail |
