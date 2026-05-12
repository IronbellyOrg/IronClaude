# Synthesis Report: Implementation Plan

**Report:** synth-05-implementation-plan
**Date:** 2026-04-04
**Sources:** research/01 through research/08, web-01, web-02
**Scope:** Template-driven incremental-write architecture for roadmap and tasklist generation

---

## Section 8: Implementation Plan

### Overview

This plan replaces the current extraction-based one-shot architecture with a template-driven incremental-write pipeline. Six phases execute sequentially; each phase has explicit dependencies, file targets, and verification criteria. All file paths are verified from research files against the live codebase.

### Architecture Change Summary

| Current State | Target State | Research Basis |
|---------------|-------------|----------------|
| Prompts embed all inputs inline via `_embed_inputs()` and capture stdout to file | Prompts instruct Claude subprocess to write output via `Write`/`Edit` tools to disk | research/04 Section 7.3; web-01 Finding 3 |
| `--output-format text` captures only final text blob | Keep `text` for backward compat; prompt instructs tool-use writing | web-01 Section 3; web-02 Finding F3 |
| No output templates; LLM invents structure per run | Template files define static scaffolding with dynamic slots | research/07 Pattern 2.1; web-02 Finding F2 |
| Extraction step lossy-summarizes TDD/PRD into prose | Structured inputs (TDD/PRD) bypass extraction; fed directly to generate step | research/02 Section 7; research/03 Section 2-3 |
| Gates check frontmatter of stdout-captured files | Gates check frontmatter of tool-written files (same mechanism, different source) | research/05 Impact Assessment |
| `build_generate_prompt()` has no task table schema | Template enforces table columns, minimum row counts, ID preservation | research/03 Section 13 Gap 1 |

### Key Constraints

| Constraint | Source | Mitigation |
|-----------|--------|------------|
| Linux `MAX_ARG_STRLEN` 128 KB for `-p` flag | research/04 Section 4 | Incremental write reduces prompt size by removing embedded prior outputs |
| `--no-session-persistence` prevents cross-invocation continuation | web-01 Section 5 | All incremental writes happen within a single `--print` invocation via tool-use turns |
| `--max-turns` default 100; each Write tool call costs 1 turn | web-01 Section 4 | Roadmap generation needs ~16-20 turns; well within budget |
| Non-streaming fallback caps at 64k tokens | web-02 Finding F6 | Tool-use file writing bypasses stdout token cap entirely |
| 4 deterministic steps (anti-instinct, wiring, deviation-analysis, remediate) generate own output | research/01 Section 6 | These steps are unaffected; no changes needed |

---

### Phase 1: Create Output Templates

**Goal:** Define static scaffolding templates for roadmap and tasklist output that enforce structure, table schemas, minimum content requirements, and ID preservation. Templates use the PART 1 / PART 2 pattern from the MDTM template (research/07, Template 4) and `{{SC_PLACEHOLDER:*}}` sentinels from the release-spec template (research/07, Template 2).

**Dependencies:** None (foundational phase).

**Design Decisions:**

| Decision | Rationale | Source |
|----------|-----------|--------|
| Use PART 1 (generation instructions in HTML comment) / PART 2 (output skeleton) | Prevents instruction leakage; same file serves as both prompt and schema | research/07 Pattern 4 (MDTM analysis) |
| Use `{{SC_PLACEHOLDER:*}}` sentinels for required fields | Only convention in codebase with automated validation (`grep -c` returns 0 = complete) | research/07 Pattern 3 (Release Spec) |
| Enforce task tables with explicit column schema | "No task table schema anywhere" is the #1 gap in current prompts; tables prevent granularity collapse | research/03 Section 13 Gap 1; research/07 Pattern "table-heavy structure" |
| Include anti-pattern FORBIDDEN section | MDTM Section B5 pattern; prevents known failure modes (tasks without AC, milestones without decomposition) | research/07 Template 4 Section B5 |
| Include completeness checklist + contract table | TDD/PRD pattern; enables both human review and automated checking | research/07 Pattern 2 |
| Include line budget per complexity class | TDD template pattern; prevents bloat and ensures minimum depth | research/07 Template 1 "line budget enforcement" |

**Step Table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 1.1 | Create roadmap output template | `src/superclaude/cli/roadmap/templates/roadmap-output.md` (new) | **PART 1:** Generation rules -- required sections, task table column schema (`Task ID \| Phase \| Description \| Source Req \| Dependencies \| Acceptance Criteria \| Complexity`), anti-patterns (FORBIDDEN: tasks without AC, milestones without task decomposition, themes not tracing to spec requirements, consolidation of multi-step work into single items), minimum row counts per complexity class (LOW: >=20 rows, MEDIUM: >=40 rows, HIGH: >=80 rows), ID preservation rule ("Preserve ALL IDs from extraction -- FR-xxx, NFR-xxx, DM-xxx, API-xxx, COMP-xxx, TEST-xxx, MIG-xxx, OPS-xxx. Do NOT renumber."), `_INTEGRATION_ENUMERATION_BLOCK` content (from `prompts.py` lines 38-49). **PART 2:** YAML frontmatter skeleton with `{{SC_PLACEHOLDER:*}}` sentinels for `spec_source`, `complexity_score`, `adversarial`, `total_task_rows`, `phases_count`; completeness checklist; contract table (upstream: spec/TDD/PRD, downstream: tasklist); 6 required sections (Executive Summary, Phased Implementation Plan with task tables, Risk Assessment, Resource Requirements, Success Criteria, Timeline Estimates); sentinel self-check command. |
| 1.2 | Create tasklist index output template | `src/superclaude/cli/tasklist/templates/tasklist-index-output.md` (new) | **PART 1:** Generation rules -- self-containment principle (each task carries enough context for independent execution, per MDTM Section B5), R-item granularity rules (1:1 default from roadmap items, split only for 2+ independently deliverable outputs per research/06 Section 3.3), Sprint CLI compatibility (`# Phase N -- <Name>` heading format, literal filenames in Phase Files table), task count floor (every phase has >= 1 and <= 25 tasks per research/06 Section 3.4), anti-consolidation guard (research/08 Gap G9 -- "Do NOT merge tasks that target different components, different API endpoints, or different data models"), PRD enrichment rule (research/08 Gap G1 fix -- "PRD personas, compliance requirements, and success metrics appear as ADDITIONAL task rows or acceptance criteria, not as reasons to consolidate existing tasks"). **PART 2:** YAML frontmatter with sentinels for `source_roadmap`, `total_phases`, `total_tasks`, `r_item_count`; Phase Files table; Deliverable Registry; Traceability Matrix (R-ID -> Task ID -> Phase); per-phase task table schema (`Task ID \| R-ID \| Name \| Type \| Complexity \| Dependencies \| Acceptance Criteria \| Status`). |
| 1.3 | Create tasklist phase file template | `src/superclaude/cli/tasklist/templates/phase-output.md` (new) | Sprint-compatible structure: `# Phase N -- <Name>` heading; YAML frontmatter with `phase_number`, `task_count`, `source_roadmap`; task detail sections per task (each with embedded acceptance criteria checkboxes per release-spec pattern research/07 Template 2); post-completion actions section. |
| 1.4 | Register templates in package data | `pyproject.toml` | Add `src/superclaude/cli/roadmap/templates/` and `src/superclaude/cli/tasklist/templates/` directories to package data so they are included in distribution. Verify with `importlib.resources` or `Path(__file__).parent / "templates"` pattern. |
| 1.5 | Add template loading utility | `src/superclaude/cli/pipeline/templates.py` (new) | Function `load_template(template_path: Path) -> tuple[str, str]` that splits PART 1 (HTML comment block) from PART 2 (output skeleton). Returns `(generation_instructions, output_skeleton)`. Also: `validate_sentinels(content: str) -> list[str]` that returns list of remaining `{{SC_PLACEHOLDER:*}}` sentinels (empty list = complete document). |

---

### Phase 2: Implement Incremental Writing

**Goal:** Modify the roadmap pipeline's LLM steps to use tool-use file writing instead of stdout capture. The subprocess writes its output to the target file via `Write`/`Edit` tools during the agentic session, rather than relying on stdout redirection.

**Dependencies:** Phase 1 (templates must exist for prompt construction).

**Design Decisions:**

| Decision | Rationale | Source |
|----------|-----------|--------|
| Keep `--output-format text` (do not switch to `stream-json`) | Minimizes blast radius; `stream-json` parsing adds complexity. The subprocess writes output via tools; stdout is ignored or used only for completion signal. | web-01 Section 3; research/04 Section 7.5 "hybrid approach" |
| Keep `--tools default` and `--dangerously-skip-permissions` | Already present in current pipeline; no flag changes needed. Claude subprocess already has Write/Edit access. | web-01 Finding 3; research/04 Section 2 |
| Instruct subprocess to write output file directly via prompt | Sprint pipeline already uses this pattern (`sprint/process.py` line 199). Prompt says "Write the result to `<path>`." | research/04 Section 7.2 |
| Remove `_sanitize_output()` for incremental-write steps | Tool-written files have no conversational preamble; sanitization is unnecessary and could corrupt structured output | research/04 Section 3.4 |
| Add post-subprocess file existence check | Parent process verifies the output file was written and is non-empty before gate evaluation | research/04 Section 7.3 point 3 |

**Step Table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.1 | Modify `build_generate_prompt()` to include template and Write instruction | `src/superclaude/cli/roadmap/prompts.py` (function `build_generate_prompt`, lines 398-506) | Load roadmap output template via `load_template()`. Compose prompt as: (a) PART 1 generation instructions, (b) existing persona and extraction instructions, (c) embedded input files, (d) explicit instruction: "Write your complete output to the file `{output_path}` using the Write tool. Structure your output according to the template below.", (e) PART 2 output skeleton with sentinels. Remove `_OUTPUT_FORMAT_BLOCK` append (YAML frontmatter is now enforced by the template skeleton). Add `output_path: str` parameter to function signature. |
| 2.2 | Modify `build_merge_prompt()` to include template, Write instruction, and ID preservation | `src/superclaude/cli/roadmap/prompts.py` (function `build_merge_prompt`, lines 619-681) | Same template-loading pattern as 2.1. Additionally: add "Preserve ALL IDs" instruction (currently missing per research/03 Section 8 Gap), append `_INTEGRATION_ENUMERATION_BLOCK` (currently missing per research/03 Section 8 Gap), add `output_path: str` parameter. This closes the two most critical merge prompt gaps identified in research/03. |
| 2.3 | Modify `build_extract_prompt()` and `build_extract_prompt_tdd()` for Write instruction | `src/superclaude/cli/roadmap/prompts.py` (functions at lines 82-205 and 208-395) | Add `output_path: str` parameter. Add Write instruction: "Write your complete output to `{output_path}` using the Write tool." Keep `_OUTPUT_FORMAT_BLOCK` for frontmatter enforcement (extraction frontmatter is consumed by gates with 13-19 required fields per research/05 Gate 1). No template needed for extraction -- it uses the existing prompt format with YAML frontmatter. |
| 2.4 | Modify remaining LLM prompt builders for Write instruction | `src/superclaude/cli/roadmap/prompts.py` (functions `build_diff_prompt`, `build_debate_prompt`, `build_score_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`, `build_wiring_verification_prompt`) | Add `output_path: str` parameter to each. Add Write instruction. These steps retain their current output format (no template needed) but switch from stdout to tool-use writing. |
| 2.5 | Modify `roadmap_run_step()` to pass output_path to prompt builders | `src/superclaude/cli/roadmap/executor.py` (function `roadmap_run_step`, lines 649-828) | At line 732 where the prompt is constructed, pass `output_path=str(step.output_file)` to each prompt builder call. The prompt now contains the target file path. |
| 2.6 | Modify `roadmap_run_step()` output validation | `src/superclaude/cli/roadmap/executor.py` (function `roadmap_run_step`, lines 649-828) | After subprocess completes (line 777-798): instead of relying on stdout file, check that `step.output_file` exists and is non-empty. If the file was not written by the subprocess (tool-use failure), attempt fallback: read stdout file (which may contain the output as text), write it to `step.output_file`, and apply `_sanitize_output()`. This provides backward compatibility if the subprocess falls back to text output. |
| 2.7 | Modify `ClaudeProcess` to handle tool-use output mode | `src/superclaude/cli/pipeline/process.py` (class `ClaudeProcess`, lines 24-203) | Add optional `tool_write_mode: bool = False` constructor parameter. When `True`: (a) stdout is still captured to a `.stdout` file (for debugging/fallback) but is NOT the primary output, (b) the primary output file path is passed via the prompt, (c) `output_file` on the `ClaudeProcess` now refers to the tool-written target, not stdout. When `False`: current behavior unchanged (backward compatible for sprint and other consumers). |
| 2.8 | Conditionally skip `_sanitize_output()` for tool-written files | `src/superclaude/cli/roadmap/executor.py` (lines 801-803, `_sanitize_output` call) | If `step.output_file` was written by the subprocess via tools (detected by: file exists AND stdout file is empty or contains only completion text), skip sanitization. Tool-written files have no conversational preamble. |

---

### Phase 3: Bypass Extraction for Structured Inputs

**Goal:** When the primary input is a TDD (a pre-structured document with numbered sections, data models, API specs, component inventory), skip the lossy extraction step and feed the TDD content directly to the generate step. Extraction remains for unstructured specs.

**Dependencies:** Phase 2 (incremental writing must be operational so the generate step can handle larger inputs via tool-use writing).

**Design Decisions:**

| Decision | Rationale | Source |
|----------|-----------|--------|
| Bypass extraction ONLY for `input_type == "tdd"` | TDDs are already structured (28 numbered sections, explicit IDs). Unstructured specs still need extraction to create a structured intermediate. PRDs alone are rejected by routing (research/02 Section 4 step 6). | research/02 Section 7 ("Extraction is never bypassed"); research/03 Section 3 ("REDUCES -- less than standard extract") |
| Generate step receives raw TDD content in place of extraction.md | Eliminates the primary granularity loss point. The TDD extraction prompt says to preserve field-level detail, but the output is still a rewrite -- not a passthrough (research/03 Section 3 "still reduces because"). | research/03 Section 2 ("REDUCES -- lossy summarization"); research/08 Section 7 Stage 1 |
| Produce a lightweight extraction summary for downstream metadata consumers | Steps like anti-instinct (reads spec_file), spec-fidelity, and gates (check extraction frontmatter fields like `complexity_score`) still need extraction metadata. Generate a frontmatter-only extraction stub via deterministic Python (no LLM). | research/01 Section 5 (anti-instinct reads spec_file); research/05 Gate 1 (13-19 FM fields) |
| Keep extraction as a fallback for malformed TDDs | If `detect_input_type()` returns "tdd" but the document lacks key structural markers (< 10 numbered headings), fall through to standard extraction. | research/02 Section 3b (TDD detection threshold >= 5) |

**Step Table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.1 | Add `_should_bypass_extraction()` helper function | `src/superclaude/cli/roadmap/executor.py` (new function, near `_route_input_files` at line 316) | Returns `True` when: (a) `config.input_type == "tdd"`, AND (b) the TDD file has >= 15 numbered headings (strong structural signal per research/02 Section 3b TDD detection weight +2/+3), AND (c) the TDD file has at least 3 of the 8 TDD-specific section names (`Data Models`, `API Specifications`, `Component Inventory`, `Testing Strategy`, `Migration`, `Operational Readiness`, `Architecture`, `Interface Contracts`). This is stricter than `detect_input_type()` (threshold 5) to ensure only well-formed TDDs bypass extraction. |
| 3.2 | Add `_build_extraction_stub()` helper function | `src/superclaude/cli/roadmap/executor.py` (new function) | Produces a minimal `extraction.md` with YAML frontmatter containing all 19 fields required by `EXTRACT_TDD_GATE` (research/05 Gate 1b). Counts are derived deterministically from the TDD: `functional_requirements` = count of `FR-` pattern matches, `data_models_identified` = count of headings containing "data model" or "interface" (case-insensitive), `api_surfaces_identified` = count of "endpoint" or "API" headings, etc. Sets `extraction_mode: "bypass-tdd"`. Body contains: `## Extraction Bypassed` with note that the TDD is consumed directly by downstream steps. |
| 3.3 | Modify `_build_steps()` to conditionally skip extract step | `src/superclaude/cli/roadmap/executor.py` (function `_build_steps`, lines 1299-1490) | At the extract step construction (line ~1310-1340): if `_should_bypass_extraction(config)` returns True, replace the LLM extract step with a deterministic step that calls `_build_extraction_stub()` and writes the stub to `extraction.md`. The step still has `EXTRACT_TDD_GATE` so the stub must satisfy all 19 frontmatter fields. Set timeout to 30s (deterministic, no LLM). |
| 3.4 | Modify `build_generate_prompt()` to handle direct TDD input | `src/superclaude/cli/roadmap/prompts.py` (function `build_generate_prompt`, lines 398-506) | Add `bypass_extraction: bool = False` parameter. When True: (a) replace extraction-referencing instructions with "The TDD document below is your PRIMARY input. It has not been extracted -- read it directly.", (b) strengthen the per-item decomposition instruction from the existing TDD block (lines 457-481), (c) include the full TDD content inline (it was previously in `tdd_file` supplementary position; now it is the primary embedded input), (d) do NOT embed `extraction.md` (it is a metadata stub only). |
| 3.5 | Modify `_build_steps()` generate step inputs for bypass mode | `src/superclaude/cli/roadmap/executor.py` (function `_build_steps`, lines ~1350-1390) | When bypass mode is active: generate step `inputs` list replaces `extraction.md` with `config.spec_file` (which holds the TDD per research/02 Section 4 step 7 -- "TDD becomes spec_file"). Also pass `bypass_extraction=True` to `build_generate_prompt()`. |
| 3.6 | Update `_embed_inputs()` semantic labels for bypass mode | `src/superclaude/cli/roadmap/executor.py` (function `roadmap_run_step`, lines 723-731) | When bypass mode is active, the label for `config.spec_file` changes from `"[Primary input - tdd]"` to `"[TDD - direct consumption, no extraction intermediary]"`. This gives the LLM accurate context about what it is receiving. |

---

### Phase 4: Update Gates for New Output Format

**Goal:** Ensure all gate criteria remain satisfied when output files are produced by tool-use writing with template-driven structure, and when the extraction step is bypassed for TDD inputs. Add new gate checks for template completeness (sentinel validation).

**Dependencies:** Phase 1 (templates define structure), Phase 2 (incremental writing produces output), Phase 3 (bypass mode produces extraction stubs).

**Design Decisions:**

| Decision | Rationale | Source |
|----------|-----------|--------|
| Keep existing gate infrastructure intact | `gate_passed()` in `src/superclaude/cli/pipeline/gates.py` reads from disk files regardless of how they were produced. Tool-written files are gated the same as stdout-written files. | research/05 "Gate Enforcement Engine" |
| Add sentinel validation as a new semantic check | `validate_sentinels()` from Phase 1 ensures no `{{SC_PLACEHOLDER:*}}` remains in final output | research/07 Pattern 3 (Release Spec sentinel check) |
| Update `EXTRACT_GATE` / `EXTRACT_TDD_GATE` for bypass stub | The extraction stub must satisfy all 19 frontmatter fields. Add `extraction_mode_valid` to accept `"bypass-tdd"` as a valid mode. | research/05 Gate 1b (EXTRACT_TDD_GATE requires 19 fields) |
| Add task row count validation to `MERGE_GATE` | Currently MERGE_GATE has no content granularity check. Add `minimum_task_rows` semantic check. | research/05 Gate 7 ("Would break: YES -- structural checks"); research/03 Section 13 Gap 4 |
| Do NOT change deterministic step gates | anti-instinct, wiring, deviation-analysis, remediate gates are immune to format changes (research/05 "Low Risk" gates) | research/05 Impact Assessment |

**Step Table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 4.1 | Update `_extraction_mode_valid()` to accept `"bypass-tdd"` | `src/superclaude/cli/roadmap/gates.py` (function `_extraction_mode_valid`) | Current check: `mode == "standard" or mode.startswith("chunked")`. Add: `or mode == "bypass-tdd"`. This allows the deterministic extraction stub from Phase 3 to pass the EXTRACT_TDD_GATE. |
| 4.2 | Add `_no_remaining_sentinels()` semantic check function | `src/superclaude/cli/roadmap/gates.py` (new function) | Reads file content, calls `validate_sentinels()` from `pipeline/templates.py` (Phase 1.5). Returns `(True, "")` if no sentinels remain; `(False, "N sentinels remaining: [list]")` otherwise. This enforces template completeness. |
| 4.3 | Add `_minimum_task_rows()` semantic check function | `src/superclaude/cli/roadmap/gates.py` (new function) | Counts markdown table data rows (lines matching `^\|[^|]+\|` that are NOT header separator rows `^\|[-:]+\|`). Reads `complexity_class` from frontmatter. Applies minimum: LOW >= 15 rows, MEDIUM >= 30 rows, HIGH >= 60 rows. Returns `(False, "Only N task rows for {complexity_class} complexity (minimum: M)")` on failure. Slightly below template minimums (20/40/80) to allow for table-less risk/summary sections. |
| 4.4 | Register new semantic checks on MERGE_GATE | `src/superclaude/cli/roadmap/gates.py` (constant `MERGE_GATE`, defined at ~line 898) | Add `_no_remaining_sentinels` and `_minimum_task_rows` to `MERGE_GATE.semantic_checks` list. MERGE_GATE currently has 3 semantic checks (`no_heading_gaps`, `cross_refs_resolve`, `no_duplicate_headings`); this adds 2 more. |
| 4.5 | Register sentinel check on GENERATE_A_GATE and GENERATE_B_GATE | `src/superclaude/cli/roadmap/gates.py` (constants at ~lines 837-859) | Add `_no_remaining_sentinels` to both generate gate `semantic_checks` lists. These gates currently have 2 checks each (`frontmatter_values_non_empty`, `has_actionable_content`). The sentinel check ensures the template was fully populated by the generate step. |
| 4.6 | Add `total_task_rows` and `phases_count` to MERGE_GATE frontmatter fields | `src/superclaude/cli/roadmap/gates.py` (constant `MERGE_GATE`) | MERGE_GATE currently requires 3 frontmatter fields (`spec_source`, `complexity_score`, `adversarial`). Add `total_task_rows` (integer, from template) and `phases_count` (integer). These are populated by the template-driven generate/merge steps. |
| 4.7 | Update GENERATE_A_GATE and GENERATE_B_GATE frontmatter fields | `src/superclaude/cli/roadmap/gates.py` (constants) | Add `total_task_rows` to required frontmatter. These gates currently require only 3 fields (`spec_source`, `complexity_score`, `primary_persona`). |

---

### Phase 5: Tasklist Pipeline Updates

**Goal:** Apply the same template-driven incremental-write pattern to the tasklist pipeline. Fix the PRD suppression language and protocol merge directives that are the strongest remaining root causes of task count regression.

**Dependencies:** Phase 1 (tasklist templates), Phase 2 (incremental write pattern established in roadmap), Phase 4 (gate pattern established).

**Design Decisions:**

| Decision | Rationale | Source |
|----------|-----------|--------|
| Fix PRD suppression language (Gap G1) | "PRD context... does NOT generate standalone implementation tasks" at `tasklist/prompts.py` lines 221-223 is the single strongest cause of task count regression | research/08 Section 4 H2 "[CODE-VERIFIED] still present" |
| Add anti-consolidation guard (Gap G9) | No guard prevents the LLM from merging tasks that target different components | research/08 Section 5 Gap Registry |
| Tighten SKILL.md merge directives (Gap G2, G12) | 3+ merge instructions with vague matching criteria cause over-consolidation | research/08 Section 4 H4 "[CODE-VERIFIED] still present" |
| Add task count floor (Gap G3) | No minimum task count exists anywhere in the pipeline | research/08 Section 5 Gap Registry |
| Create CLI `tasklist generate` subcommand | Currently generation is inference-only via `/sc:tasklist` skill; no programmatic path exists | research/06 Section 1 "no `tasklist generate` CLI subcommand" |
| Apply incremental-write to tasklist generate | Tasklist bundles can be 10+ files; one-shot output exceeds context limits for large roadmaps | research/06 Section 5.4 |

**Step Table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 5.1 | Remove PRD suppression language from `build_tasklist_generate_prompt()` | `src/superclaude/cli/tasklist/prompts.py` (lines 221-223) | Replace "PRD context informs task descriptions and priorities but does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them." with "PRD personas, compliance requirements, and success metrics generate ADDITIONAL task rows and acceptance criteria. PRD-derived tasks supplement the roadmap's engineering tasks -- they do NOT consolidate or replace them." This directly addresses Gap G1 (research/08 Section 4 H2). |
| 5.2 | Add anti-consolidation guard to `build_tasklist_generate_prompt()` | `src/superclaude/cli/tasklist/prompts.py` (after the PRD block, ~line 230) | Insert: "ANTI-CONSOLIDATION RULE: Do NOT merge tasks that target different components, different API endpoints, different data models, or different test categories. Each independently deliverable work item from the roadmap MUST appear as a separate task row. Consolidation is permitted ONLY when two roadmap items describe the exact same deliverable with different wording." This addresses Gap G9. |
| 5.3 | Add task count floor to `build_tasklist_generate_prompt()` | `src/superclaude/cli/tasklist/prompts.py` (near end of prompt, before `_OUTPUT_FORMAT_BLOCK`) | Insert: "TASK COUNT FLOOR: The total number of tasks generated MUST be >= the number of task table rows in the source roadmap. If the roadmap contains N task rows, the tasklist must contain >= N tasks. If a roadmap item decomposes into multiple tasks, the count increases. The tasklist MUST NOT have fewer tasks than the roadmap has task rows." This addresses Gap G3. |
| 5.4 | Tighten merge directives in SKILL.md protocol | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (lines 233, 255, 259) | At line 233 (Section 4.4a): Replace "Merge rather than duplicate if a generated task duplicates an existing task for the same component" with "Merge ONLY when two tasks have identical target component AND identical deliverable type AND identical acceptance criteria scope. Different components, different endpoints, or different data models MUST remain separate tasks." At line 255 (Section 4.4b): Replace "Merge rather than duplicate..." with the same tightened criteria plus "PRD-derived tasks that cover different personas or different compliance domains MUST remain separate even if they relate to the same feature area." At line 259: Replace "merge with existing feature task if one covers the same goal" with "merge with existing feature task ONLY if the goal, target component, and deliverable type are all identical." This addresses Gaps G2, G12. |
| 5.5 | Add standalone test task minimum to SKILL.md | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (after Section 4.4, new Section 4.4c) | Insert new section: "**4.4c Testing Task Minimum**: For each phase that contains >= 3 implementation tasks, at least 1 standalone testing task MUST be generated (not embedded as a [VERIFICATION] step within an implementation task). Testing tasks cover: unit test suites, integration test suites, E2E test scenarios, load/performance tests. The testing task MUST reference the specific test artifacts from the TDD (TEST-xxx IDs) when available." This addresses Gap G6 (research/08 Section 4 H3). |
| 5.6 | Rewrite `build_tasklist_generate_prompt()` for template-driven generation | `src/superclaude/cli/tasklist/prompts.py` (function `build_tasklist_generate_prompt`, currently ~40 lines) | The current function is a lightweight stub (research/06 Section 4). Rewrite to: (a) load tasklist-index-output template and phase-output template via `load_template()`, (b) include PART 1 generation instructions from index template, (c) embed roadmap content, (d) instruct Write tool usage: "For each phase, write a separate file `phase-N-tasklist.md` using the Write tool. After all phases are written, write `tasklist-index.md` with the cross-phase registry and traceability matrix.", (e) include PART 2 skeleton for both index and phase templates. Add `output_dir: str` parameter. |
| 5.7 | Add `tasklist generate` CLI subcommand | `src/superclaude/cli/tasklist/commands.py` (new command in `tasklist_group`) | New Click command `generate` under `tasklist_group` with arguments: `roadmap_file` (required Path), options `--tdd-file`, `--prd-file`, `--output` (directory), `--model`, `--max-turns`, `--debug`. Calls `execute_tasklist_generate()` in executor. |
| 5.8 | Add `execute_tasklist_generate()` executor function | `src/superclaude/cli/tasklist/executor.py` (new function) | Single-step pipeline: Step ID `"tasklist-generate"`, prompt from `build_tasklist_generate_prompt()`, inputs = [roadmap_file, tdd_file?, prd_file?], output = `{output_dir}/tasklist-index.md`, gate = new `TASKLIST_GENERATE_GATE`, timeout = 1800s (large output, multi-file write), retry_limit = 1. Uses `execute_pipeline()` with `tasklist_run_step`. After pipeline completes, verify all `phase-N-tasklist.md` files exist. |
| 5.9 | Add `TASKLIST_GENERATE_GATE` | `src/superclaude/cli/tasklist/gates.py` (new constant) | Required frontmatter fields: `source_roadmap`, `total_phases`, `total_tasks`, `r_item_count`. Min lines: 50. Enforcement tier: STRICT. Semantic checks: `_no_remaining_sentinels` (from Phase 4.2), `_task_count_floor` (new: total_tasks >= r_item_count from frontmatter), `_phase_files_exist` (new: verifies all phase files referenced in the Phase Files table exist on disk). |
| 5.10 | Sync SKILL.md changes to `.claude/skills/` | `.claude/skills/sc-tasklist-protocol/SKILL.md` | Run `make sync-dev` to propagate changes from `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` to the active skill directory. Verify with `make verify-sync`. |

---

### Phase 6: Testing and Regression Validation

**Goal:** Verify the new architecture produces equal or better output than the current pipeline across all input types (spec-only, TDD-only, TDD+PRD, spec+TDD+PRD). Validate that all gates pass, no regressions in task count, and incremental writing produces structurally valid output.

**Dependencies:** All prior phases (1-5).

**Design Decisions:**

| Decision | Rationale | Source |
|----------|-----------|--------|
| Re-run existing test fixtures through new pipeline | The test fixtures in `.dev/test-fixtures/results/test-fix-tdd-prd/` provide baseline comparison data | research/08 Section 8 "Test fixture staleness" |
| Compare task counts between old and new pipeline runs | The 87 vs 44 task count regression (research/08 Section 1) is the primary metric | research/08 Section 1 problem statement |
| Validate all 14 gates pass for each run | Gate failures would indicate template or format incompatibility | research/05 Summary Table (14 gates) |
| Test extraction bypass specifically with TDD inputs | Phase 3 is the highest-risk change; must validate that bypass produces equivalent or better results | research/02 Section 7; research/03 Section 3 |
| Test backward compatibility with `--resume` | The `--resume` flag reads `.roadmap-state.json` which may need schema updates for bypass mode | research/01 Section 3 step 2; research/02 Section 8 |

**Step Table:**

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 6.1 | Add unit tests for template loading | `tests/cli/pipeline/test_templates.py` (new) | Test `load_template()`: (a) correctly splits PART 1 / PART 2, (b) returns empty PART 1 for templates without HTML comment block, (c) handles nested HTML comments. Test `validate_sentinels()`: (a) returns empty list for complete document, (b) returns list of remaining sentinels, (c) handles escaped braces. |
| 6.2 | Add unit tests for extraction bypass | `tests/cli/roadmap/test_extraction_bypass.py` (new) | Test `_should_bypass_extraction()`: (a) returns True for well-formed TDD with >= 15 numbered headings and 3+ TDD section names, (b) returns False for spec input, (c) returns False for TDD with < 15 numbered headings. Test `_build_extraction_stub()`: (a) produces valid YAML frontmatter with all 19 EXTRACT_TDD_GATE fields, (b) sets `extraction_mode: "bypass-tdd"`, (c) frontmatter counts match regex-based counting of TDD content. |
| 6.3 | Add unit tests for updated gate checks | `tests/cli/roadmap/test_gates.py` (existing, extend) | Test `_extraction_mode_valid()` accepts `"bypass-tdd"`. Test `_no_remaining_sentinels()` with sentinel-containing and sentinel-free content. Test `_minimum_task_rows()` with various complexity classes and row counts. |
| 6.4 | Add unit tests for prompt builder changes | `tests/cli/roadmap/test_prompts.py` (existing, extend) | Test `build_generate_prompt()` with new `output_path` parameter: (a) prompt contains Write instruction with correct path, (b) prompt contains template PART 1 instructions when template exists, (c) prompt contains "bypass-tdd" instructions when `bypass_extraction=True`. Test `build_merge_prompt()`: (a) now contains "Preserve ALL IDs" instruction, (b) now contains `_INTEGRATION_ENUMERATION_BLOCK`. |
| 6.5 | Add integration test: spec-only pipeline run | `tests/cli/roadmap/test_pipeline_integration.py` (new or extend existing) | Run full pipeline with a spec-only input (use existing test fixture spec from `.dev/test-fixtures/`). Verify: (a) all gates pass, (b) `roadmap.md` was written by tool-use (check stdout file is empty or minimal), (c) `roadmap.md` contains no `{{SC_PLACEHOLDER:*}}` sentinels, (d) `roadmap.md` task table has >= minimum rows for complexity class, (e) all YAML frontmatter fields present. Compare task row count against baseline (should be >= 87 for the spec-only fixture). |
| 6.6 | Add integration test: TDD-only pipeline run with bypass | `tests/cli/roadmap/test_pipeline_integration.py` | Run full pipeline with TDD-only input. Verify: (a) extraction step was bypassed (check `extraction.md` contains `extraction_mode: "bypass-tdd"`), (b) generate step received raw TDD content (not extraction summary), (c) all gates pass, (d) task row count >= baseline (should be significantly higher than 44 -- the prior TDD+PRD result). |
| 6.7 | Add integration test: TDD+PRD pipeline run | `tests/cli/roadmap/test_pipeline_integration.py` | Run full pipeline with TDD+PRD input. Verify: (a) extraction bypassed for TDD, (b) PRD content enriches generate step without suppressing task count, (c) task row count >= TDD-only count (PRD should ADD tasks, not consolidate), (d) all gates pass. |
| 6.8 | Add integration test: tasklist generate from roadmap | `tests/cli/tasklist/test_tasklist_generate.py` (new) | Run `execute_tasklist_generate()` with a roadmap produced by the new pipeline. Verify: (a) `tasklist-index.md` exists and passes `TASKLIST_GENERATE_GATE`, (b) all `phase-N-tasklist.md` files exist, (c) task count >= roadmap task row count (task count floor enforced), (d) no `{{SC_PLACEHOLDER:*}}` sentinels remain. |
| 6.9 | Add regression test: `--resume` compatibility | `tests/cli/roadmap/test_resume.py` (new or extend) | Verify that `--resume` works correctly after: (a) a normal run (no bypass) -- should restore from `.roadmap-state.json` and skip passing steps, (b) a bypass run -- state file must record `extraction_mode: "bypass-tdd"` so resume knows to skip extraction, (c) resuming a bypass run from a non-bypass state (should re-detect and route correctly). |
| 6.10 | Run full test suite and verify no regressions | (all test files) | `uv run pytest tests/ -v`. Verify zero failures in existing tests. Run `make lint && make format` to ensure code quality. Run `make verify-sync` to confirm src/ and .claude/ are in sync. |

---

### Integration Checklist

This checklist must be verified before the implementation is considered complete. Each item references the specific phase and step that addresses it.

| # | Check | Phase.Step | Verification Command |
|---|-------|-----------|---------------------|
| 1 | Roadmap output template exists and loads correctly | 1.1, 1.5 | `uv run python -c "from superclaude.cli.pipeline.templates import load_template; p1, p2 = load_template(Path('src/superclaude/cli/roadmap/templates/roadmap-output.md')); assert p1; assert p2"` |
| 2 | Tasklist index and phase templates exist | 1.2, 1.3 | `ls src/superclaude/cli/tasklist/templates/{tasklist-index-output.md,phase-output.md}` |
| 3 | `build_generate_prompt()` accepts `output_path` parameter and includes Write instruction | 2.1 | `uv run pytest tests/cli/roadmap/test_prompts.py -k "output_path" -v` |
| 4 | `build_merge_prompt()` includes ID preservation and `_INTEGRATION_ENUMERATION_BLOCK` | 2.2 | `uv run pytest tests/cli/roadmap/test_prompts.py -k "merge" -v` |
| 5 | `roadmap_run_step()` verifies tool-written output file with fallback to stdout | 2.6 | `uv run pytest tests/cli/roadmap/test_pipeline_integration.py -k "tool_write" -v` |
| 6 | `_should_bypass_extraction()` correctly identifies well-formed TDDs | 3.1 | `uv run pytest tests/cli/roadmap/test_extraction_bypass.py -v` |
| 7 | `_build_extraction_stub()` produces gate-passing YAML frontmatter with 19 fields | 3.2 | `uv run pytest tests/cli/roadmap/test_extraction_bypass.py -k "stub" -v` |
| 8 | `_extraction_mode_valid()` accepts `"bypass-tdd"` | 4.1 | `uv run pytest tests/cli/roadmap/test_gates.py -k "extraction_mode" -v` |
| 9 | MERGE_GATE includes `_minimum_task_rows` and `_no_remaining_sentinels` checks | 4.4 | `uv run pytest tests/cli/roadmap/test_gates.py -k "merge_gate" -v` |
| 10 | PRD suppression language removed from `tasklist/prompts.py` | 5.1 | `grep -c "does NOT generate standalone" src/superclaude/cli/tasklist/prompts.py` returns 0 |
| 11 | Anti-consolidation guard present in `tasklist/prompts.py` | 5.2 | `grep -c "ANTI-CONSOLIDATION" src/superclaude/cli/tasklist/prompts.py` returns 1 |
| 12 | Task count floor present in `tasklist/prompts.py` | 5.3 | `grep -c "TASK COUNT FLOOR" src/superclaude/cli/tasklist/prompts.py` returns 1 |
| 13 | SKILL.md merge directives tightened (no vague "same goal" matching) | 5.4 | `grep -c "covers the same goal" src/superclaude/skills/sc-tasklist-protocol/SKILL.md` returns 0 |
| 14 | SKILL.md has standalone test task minimum (Section 4.4c) | 5.5 | `grep -c "Testing Task Minimum" src/superclaude/skills/sc-tasklist-protocol/SKILL.md` returns 1 |
| 15 | `tasklist generate` CLI subcommand exists | 5.7 | `uv run superclaude tasklist generate --help` exits 0 |
| 16 | `TASKLIST_GENERATE_GATE` exists in `tasklist/gates.py` | 5.9 | `grep -c "TASKLIST_GENERATE_GATE" src/superclaude/cli/tasklist/gates.py` returns >= 1 |
| 17 | Component sync verified | 5.10 | `make verify-sync` exits 0 |
| 18 | Spec-only pipeline produces >= 80 task rows (near-baseline 87) | 6.5 | Integration test passes |
| 19 | TDD-only pipeline with bypass produces > 44 task rows (exceeds prior regression) | 6.6 | Integration test passes |
| 20 | TDD+PRD pipeline produces >= TDD-only count (PRD adds, not consolidates) | 6.7 | Integration test passes |
| 21 | Full test suite passes with zero regressions | 6.10 | `uv run pytest tests/ -v` exits 0 |
| 22 | All templates included in package distribution | 1.4 | `uv run python -c "import importlib.resources; list(importlib.resources.files('superclaude.cli.roadmap.templates').iterdir())"` |

---

### File Change Summary

| File | Change Type | Phase | Description |
|------|------------|-------|-------------|
| `src/superclaude/cli/roadmap/templates/roadmap-output.md` | NEW | 1.1 | Roadmap output template (PART 1/PART 2) |
| `src/superclaude/cli/tasklist/templates/tasklist-index-output.md` | NEW | 1.2 | Tasklist index output template |
| `src/superclaude/cli/tasklist/templates/phase-output.md` | NEW | 1.3 | Tasklist phase file template |
| `src/superclaude/cli/pipeline/templates.py` | NEW | 1.5 | Template loading and sentinel validation utilities |
| `pyproject.toml` | MODIFY | 1.4 | Add template directories to package data |
| `src/superclaude/cli/roadmap/prompts.py` | MODIFY | 2.1-2.4 | Add `output_path` param to all prompt builders; template integration for generate/merge |
| `src/superclaude/cli/roadmap/executor.py` | MODIFY | 2.5-2.8, 3.1-3.6 | Pass output_path to prompts; tool-write detection; bypass extraction functions |
| `src/superclaude/cli/pipeline/process.py` | MODIFY | 2.7 | Add `tool_write_mode` parameter to ClaudeProcess |
| `src/superclaude/cli/roadmap/gates.py` | MODIFY | 4.1-4.7 | Update extraction_mode_valid; add sentinel/task-row checks; register on gates |
| `src/superclaude/cli/tasklist/prompts.py` | MODIFY | 5.1-5.3, 5.6 | Remove PRD suppression; add anti-consolidation guard; add task count floor; rewrite generate prompt |
| `src/superclaude/cli/tasklist/commands.py` | MODIFY | 5.7 | Add `generate` subcommand |
| `src/superclaude/cli/tasklist/executor.py` | MODIFY | 5.8 | Add `execute_tasklist_generate()` function |
| `src/superclaude/cli/tasklist/gates.py` | MODIFY | 5.9 | Add `TASKLIST_GENERATE_GATE` constant |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | MODIFY | 5.4-5.5 | Tighten merge directives; add test task minimum |
| `.claude/skills/sc-tasklist-protocol/SKILL.md` | SYNC | 5.10 | Sync from src/ via `make sync-dev` |
| `tests/cli/pipeline/test_templates.py` | NEW | 6.1 | Template loading unit tests |
| `tests/cli/roadmap/test_extraction_bypass.py` | NEW | 6.2 | Extraction bypass unit tests |
| `tests/cli/roadmap/test_gates.py` | MODIFY | 6.3 | Extended gate check tests |
| `tests/cli/roadmap/test_prompts.py` | MODIFY | 6.4 | Extended prompt builder tests |
| `tests/cli/roadmap/test_pipeline_integration.py` | NEW | 6.5-6.7, 6.9 | Pipeline integration and resume tests |
| `tests/cli/tasklist/test_tasklist_generate.py` | NEW | 6.8 | Tasklist generate integration test |

**Total:** 8 new files, 12 modified files, 1 synced file.

