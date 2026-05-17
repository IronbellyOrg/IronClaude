# Sections 6-7: Options Analysis and Recommendation

**Synthesis Date**: 2026-04-04
**Sources**: All 11 research files (01-08, web-01, web-02, research-notes) + gaps-and-questions.md
**Research Question**: Replacing extraction-based one-shot architecture with template-driven incremental writing for roadmap and tasklist generation
**Status**: Complete

---

## Section 6: Options Analysis

Three options are evaluated below, ranging from full architectural replacement to minimal prompt-level fixes. Each option addresses the three structural failures identified in research:

1. **Extraction destroys granularity** -- lossy summarization of spec/TDD into prose sections (research file 03, `build_extract_prompt` assessment: "REDUCES"; `build_extract_prompt_tdd` assessment: "REDUCES (less loss)")
2. **One-shot output architecture** -- `claude --print --output-format text` captures only final stdout blob with no incremental writing, no truncation detection, no continuation (research file 04, Section 3; web-02 Finding F6: non-streaming fallback caps at 64k tokens)
3. **No output templates** -- no task table schema, no minimum row counts, no structural enforcement on LLM-generated roadmap/tasklist content (research file 03, Gap #1: "No task table schema anywhere"; research file 07, Gap #1: "No Existing Roadmap Output Template")

---

### Option A: Full Template-Driven Incremental Writing

#### Description

Replace the extraction-based one-shot pipeline with a template-driven, tool-use-mode architecture. The subprocess writes output files incrementally via Write/Edit tools (already available per web-01 Finding 3) instead of capturing stdout. Output templates define the structural skeleton; the LLM fills dynamic slots section by section.

#### How It Works

| Step | Current Behavior | Proposed Behavior |
|------|-----------------|-------------------|
| **Extraction** | LLM summarizes spec/TDD into 8-14 prose sections via `build_extract_prompt[_tdd]()` (file 03, Sections 2-3). All downstream steps consume `extraction.md`. | **Bypassed for TDD/PRD inputs.** Structured inputs (TDD, PRD) pass directly to the generate step. Extraction retained only for unstructured specs as a fallback with `--input-type auto` detection (file 02, Section 3). |
| **Generate** | `build_generate_prompt()` produces free-form roadmap with no task table schema (file 03, Section 4: "DESTROYS without TDD / REDUCES with TDD"). Output via `--output-format text` stdout capture. | LLM receives an output template file (PART 1/PART 2 pattern from MDTM, file 07, Template 4) defining required sections, table columns, and `{{SC_PLACEHOLDER:*}}` sentinels. Subprocess uses `--tools default` to write sections incrementally via Write tool. Each section is a bounded tool call. |
| **Merge** | `build_merge_prompt()` lacks ID preservation, lacks `_INTEGRATION_ENUMERATION_BLOCK`, no granularity floor (file 03, Section 8: "Missing from merge that exists in generate"). Output via stdout. | Merge operates on template-structured variants. Template enforces table schema preservation. Merge prompt includes ID preservation instructions and integration enumeration block. Output via tool-use. |
| **Output format** | `output_format="text"` (file 04, Section 3.2). Only final text response captured. | `output_format="stream-json"` (matching Sprint, file 04, Section 9). Parent process observes tool_use events for progress tracking and error detection. |
| **Gates** | Validate YAML frontmatter + semantic checks on stdout-captured file (file 05). | Same gate logic, same `GateCriteria` objects, but validate tool-written files instead of stdout-captured files. 6 gates marked "YES -- would break" need frontmatter field updates to match template (file 05, Summary Table). |
| **Tasklist generation** | Inference-only via `/sc:tasklist` skill (file 06, Section 1: "no `tasklist generate` CLI subcommand"). `build_tasklist_generate_prompt()` is dead code from CLI perspective. | New `superclaude tasklist generate` CLI subcommand backed by template-driven pipeline. Tasklist output template enforces Sprint CLI compatibility (`# Phase N -- <Name>` heading format, file 06, Section 3.5). |

#### Assessment

| Dimension | Assessment |
|-----------|------------|
| **Effort** | HIGH. Requires: (1) 2 new template files (roadmap + tasklist output), (2) rewrite of `roadmap_run_step()` to use stream-json + tool-use output capture, (3) new `tasklist generate` CLI subcommand + executor, (4) prompt rewrites for extract/generate/merge to reference templates, (5) gate updates for 6 "YES -- would break" gates (EXTRACT, EXTRACT_TDD, MERGE, TEST_STRATEGY, SPEC_FIDELITY per file 05), (6) removal/refactoring of `_sanitize_output()` (no longer needed per file 04, Section 7.3). |
| **Risk** | MEDIUM-HIGH. Template design must be correct on first iteration -- a bad template locks in bad structure. Gate updates are mechanical but must maintain all 36 semantic check instances (file 05). The 4 deterministic steps (anti-instinct, wiring, deviation-analysis, remediate) depend on upstream output formats as INPUT (file 05, Key Insight) -- format changes cascade. |
| **Reuse** | HIGH. Output templates reusable across all pipeline runs. Template pattern established for future pipeline artifacts. `stream-json` monitoring infrastructure shared with Sprint. Tasklist CLI subcommand fills the generation gap identified in file 06. |
| **Files affected** | ~15 files. `src/superclaude/cli/roadmap/executor.py` (2,897 lines), `prompts.py` (942 lines), `gates.py` (1,139 lines), `pipeline/process.py` (202 lines). New: 2 template files, tasklist executor, tasklist commands update. Modified: `models.py`, `commands.py`, potentially `pipeline/executor.py`. |
| **Pros** | Eliminates all 3 structural failures simultaneously. Template enforcement prevents granularity collapse (file 03 Gaps #1-#6). Tool-use bypasses 64k token stdout cap (web-02 Finding F6). Enables progress monitoring via stream-json (file 04, Section 7.5). Fills tasklist generation CLI gap (file 06). Aligns roadmap pipeline with Sprint pipeline patterns. |
| **Cons** | Largest scope of work. Template design is a new artifact that must be maintained. Breaks backward compatibility with existing roadmap output consumers. Requires re-running all test fixtures. The 120KB prompt size limit remains (file 04, `_EMBED_SIZE_LIMIT`) -- templates add to prompt overhead. Risk of over-engineering if template is too rigid. |

---

### Option B: Hybrid Approach (Template + Incremental for TDD/PRD; Keep Extraction for Unstructured Specs)

#### Description

Split the pipeline into two paths based on input type. For structured inputs (TDD, PRD), bypass extraction and use template-driven incremental writing. For unstructured specs, keep the current extraction-based one-shot architecture with prompt improvements. This preserves backward compatibility for spec-only workflows while addressing the primary granularity loss for TDD/PRD inputs.

#### How It Works

| Step | Unstructured Spec Path (input_type="spec") | Structured Input Path (input_type="tdd" or TDD+PRD) |
|------|-------------------------------------------|------------------------------------------------------|
| **Extraction** | Retained as-is. `build_extract_prompt()` runs with current 13-field YAML frontmatter (file 03, Section 2). Prompt improvements added: instruction to preserve table/code-block formats (file 03, Gap #5). | **Bypassed.** TDD/PRD content passes directly to generate step. The 14-section TDD extraction (file 03, Section 3) is replaced by direct TDD consumption. Saves 300-1800s timeout (file 01, Step Table row 1). |
| **Generate** | Current `build_generate_prompt()` with added task table schema (columns: Task ID, Phase, Description, Dependencies, Acceptance Criteria, Effort). Addresses file 03 Gap #1. Still uses `--output-format text` stdout capture. | Template-driven generation. Roadmap output template (PART 1/PART 2 pattern, file 07) defines the task table schema. LLM writes output via Write tool. `--output-format stream-json` for observability. |
| **Merge** | Add ID preservation instruction + `_INTEGRATION_ENUMERATION_BLOCK` to `build_merge_prompt()` (file 03, Section 8 gaps). Still stdout-based. | Template-enforced merge. Task table schema preserved through merge. Tool-use output. |
| **Gates** | No gate changes needed for spec path -- current gates continue to work. | Gates for TDD path need updates: EXTRACT gate bypassed (no extraction step), GENERATE/MERGE gates validate template-structured output. Estimated 4 gate updates (file 05). |
| **Tasklist** | No change. Skill-based generation continues as-is. | New `tasklist generate` CLI subcommand for TDD/PRD inputs, template-driven. Skill path remains available as alternative. |

**Routing mechanism:** The existing `_route_input_files()` (file 02, Section 4) already resolves `input_type` as `"spec"` or `"tdd"`. The `_build_steps()` function (file 01, Section 4) already conditionally selects `EXTRACT_GATE` vs `EXTRACT_TDD_GATE` based on `input_type`. This branching point is extended to select between one-shot and template-driven step configurations.

#### Assessment

| Dimension | Assessment |
|-----------|------------|
| **Effort** | MEDIUM. Requires: (1) 1-2 output template files, (2) conditional path in `_build_steps()` for TDD inputs, (3) prompt improvements for spec-path generate/merge (3 prompt functions), (4) tool-use output capture for TDD-path steps only, (5) 4 gate updates for TDD-path gates. Spec-path gates unchanged. |
| **Risk** | MEDIUM. Two code paths increase maintenance burden and testing surface. The branching logic in `_build_steps()` is already conditional on `input_type` (file 01, Section 4) so the extension is natural. Risk that spec-path falls further behind as TDD-path improves. Deterministic steps (anti-instinct, wiring, etc.) must handle both output formats as input. |
| **Reuse** | MEDIUM. Templates reusable for TDD/PRD runs. Prompt improvements to spec-path benefit all spec-only runs. But two separate architectures limits cross-pollination. |
| **Files affected** | ~10 files. `src/superclaude/cli/roadmap/executor.py` (conditional step building), `prompts.py` (prompt improvements + template references), `gates.py` (4 gate updates). New: 1-2 template files. Modified: `_build_steps()`, `roadmap_run_step()` (conditional output mode). |
| **Pros** | Addresses primary granularity loss for TDD/PRD (the documented 49% task reduction from file 08, Section 1). Preserves backward compatibility for spec-only workflows. Smaller scope than Option A. Leverages existing `input_type` branching infrastructure. Prompt improvements to spec-path provide immediate partial benefit. |
| **Cons** | Two code paths to maintain. Spec-path still suffers from one-shot output limitations (truncation risk for large specs, no progress monitoring). Does not fill the tasklist generation CLI gap for spec-only inputs. Template-to-spec-path divergence may widen over time. The 4 deterministic steps must parse two different input formats, increasing complexity in `_run_deviation_analysis()`, `_run_anti_instinct_audit()`, etc. (file 01, Section 6). |

---

### Option C: Minimal Fix (Prompt Improvements + Output Schema Only)

#### Description

Keep the one-shot `--output-format text` architecture entirely. Address granularity loss through prompt engineering only: add task table schemas to generate/merge prompts, add ID preservation to merge, add anti-consolidation guards, fix the PRD suppression language in tasklist prompts. No template files, no tool-use mode change, no new CLI subcommands.

#### How It Works

| Component | Current | Proposed Change |
|-----------|---------|-----------------|
| **`build_extract_prompt()`** | 8 prose sections, no table preservation instruction (file 03, Section 2) | Add instruction: "Preserve original table structures and code blocks verbatim. Do not rewrite tables into prose bullet lists." (Addresses file 03 Gap #5) |
| **`build_extract_prompt_tdd()`** | 14 sections with per-item IDs but no table format preservation (file 03, Section 3) | Same table preservation instruction. Add explicit minimum count: "The number of ### headings in Data Models section must equal `data_models_identified` frontmatter count." |
| **`build_generate_prompt()`** | No task table schema (file 03 Gap #1: "task table row" undefined). TDD block says "MORE roadmap task rows" but no format. | Add explicit task table schema: `\| Task ID \| Phase \| Description \| Dependencies \| AC \| Effort \|`. Add minimum row count: "Output must contain at least as many task table rows as extracted requirement IDs." Add `_INTEGRATION_ENUMERATION_BLOCK` appendage (already present for generate, confirmed in file 03 Section 4). |
| **`build_merge_prompt()`** | Missing ID preservation, missing `_INTEGRATION_ENUMERATION_BLOCK`, no granularity floor (file 03 Gaps #2-#4) | Add: "Preserve ALL IDs from both variants. Do NOT renumber, relabel, or consolidate." Append `_INTEGRATION_ENUMERATION_BLOCK`. Add: "The merged roadmap must contain at least as many task table rows as the base variant." |
| **`build_score_prompt()`** | Section 5 "specific improvements" is free-form prose (file 03, Section 7) | Add structured format for improvement list: `\| # \| Improvement \| Source Variant \| Task IDs Affected \|` |
| **Tasklist `prompts.py`** | PRD suppression at lines 221-223 (file 08, Section 4 H2: "strongest single cause") | Remove: "PRD context... does NOT generate standalone implementation tasks." Replace with: "PRD personas, compliance requirements, and success metrics should appear as ADDITIONAL task rows." (Prior research Option C, Step 1) |
| **SKILL.md protocol** | 3+ merge directives with vague criteria (file 08, Section 4 H4) | Tighten merge criteria: "Merge ONLY when two tasks operate on the same file AND the same function/class AND produce the same deliverable type." Add task count floor: "total_tasks >= R-items * 1.0" (Prior research Option C, Steps 3-8) |
| **Gates** | No changes. All 14 gates remain as-is. | No changes. Existing gates continue to validate the same frontmatter fields. The output still hits the same gate criteria. |

#### Assessment

| Dimension | Assessment |
|-----------|------------|
| **Effort** | LOW. Requires: (1) modifications to 5-6 prompt builder functions in `prompts.py` (~50-100 lines of prompt text changes), (2) 3 lines removed + 3 lines added in `tasklist/prompts.py`, (3) SKILL.md protocol tightening (~20 lines). No new files, no architectural changes, no gate updates. |
| **Risk** | LOW. Prompt changes are additive (instructions appended, not restructured). No architectural changes means no cascading breakage through deterministic steps. Gate compatibility guaranteed since output format is unchanged. Behavioral risk: LLM compliance with prompt instructions is probabilistic, not guaranteed (web-02 Finding F2: template enforcement is more reliable than prompt-only enforcement). |
| **Reuse** | LOW. Prompt text improvements are specific to each function. No reusable infrastructure created. The task table schema could be extracted into a shared constant (similar to `_INTEGRATION_ENUMERATION_BLOCK`). |
| **Files affected** | 3 files. `src/superclaude/cli/roadmap/prompts.py` (942 lines -- prompt text changes only), `src/superclaude/cli/tasklist/prompts.py` (237 lines -- PRD suppression removal), `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (~800 lines -- merge criteria tightening). |
| **Pros** | Fastest to implement. Zero architectural risk. Zero gate breakage. Directly addresses the 5 unfixed gaps from prior research (file 08, Section 6: G1 PRD suppression, G2 merge directives, G3 task count floor, G9 anti-consolidation, G12 subjective merge criteria). Can be shipped, validated with test fixtures, and iterated before committing to architectural changes. |
| **Cons** | Does NOT address the one-shot output truncation problem (web-02 Finding F6: 64k token cap). Does NOT address the extraction granularity loss for spec-only inputs (file 03 Sections 2-3). Prompt-only enforcement is probabilistic -- the LLM may ignore task table schema instructions on some runs (web-02 Finding F2). Does NOT fill the tasklist generation CLI gap (file 06). Does NOT enable progress monitoring. Does not create reusable template infrastructure. The "output exceeds limits" failure mode persists (file 04, Section 5: "no truncation detection, no continuation, no partial output preservation"). |

---

### Option D: Phased Migration (Option C First, Then Option B)

#### Description

Execute Option C immediately as a quick-win to address the most impactful granularity gaps, then execute Option B as a follow-up phase to address architectural limitations. This combines the speed of prompt fixes with the structural benefits of template-driven output.

#### How It Works

**Phase 1 (Option C -- immediate):** All prompt improvements from Option C. Ship, run test fixtures, validate the 49% task reduction is mitigated. Estimated 1-2 days of implementation.

**Phase 2 (Option B -- follow-up):** Template-driven incremental writing for TDD/PRD inputs. Build on Phase 1's prompt improvements, which remain valid in the template-driven architecture (task table schema constants, ID preservation instructions become template enforcement rules). Estimated 5-8 days of implementation.

**Phase 1 to Phase 2 bridge:** The task table schema constant added in Phase 1 (e.g., `_TASK_TABLE_SCHEMA`) becomes the column definition in the Phase 2 output template. The anti-consolidation guards added in Phase 1 become PART 1 instructions in the Phase 2 template. The gate criteria remain unchanged across both phases.

#### Assessment

| Dimension | Assessment |
|-----------|------------|
| **Effort** | LOW then MEDIUM. Phase 1: same as Option C (~1-2 days). Phase 2: Option B minus the prompt work already done in Phase 1 (~5-8 days). Total: ~6-10 days, front-loaded with quick wins. |
| **Risk** | LOW then MEDIUM. Phase 1 has zero architectural risk. Phase 2 risk is mitigated by having validated prompt improvements as a baseline -- if Phase 2 fails, Phase 1 improvements remain. |
| **Reuse** | MEDIUM-HIGH. Phase 1 artifacts (schema constants, anti-consolidation text) feed directly into Phase 2 templates. Phase 2 creates reusable template infrastructure. |
| **Files affected** | Phase 1: 3 files (same as Option C). Phase 2: additional ~7 files (same as Option B minus prompt changes). |
| **Pros** | Fastest path to measurable improvement (Phase 1). Validated baseline before architectural change. Phase 1 work is not throwaway -- it feeds Phase 2. Risk-gated: can stop after Phase 1 if results are sufficient. |
| **Cons** | Total effort is higher than Option B alone (Phase 1 prompt changes are partially redundant with Phase 2 template enforcement). Two implementation cycles means two review/test cycles. |

---

### Options Comparison Table

| Dimension | Option A (Full Template) | Option B (Hybrid) | Option C (Prompt Only) | Option D (Phased C+B) |
|-----------|-------------------------|-------------------|------------------------|----------------------|
| **Effort** | HIGH (~10-15 days) | MEDIUM (~5-8 days) | LOW (~1-2 days) | LOW+MEDIUM (~6-10 days) |
| **Risk** | MEDIUM-HIGH | MEDIUM | LOW | LOW then MEDIUM |
| **Reuse** | HIGH | MEDIUM | LOW | MEDIUM-HIGH |
| **Files affected** | ~15 | ~10 | 3 | 3 then ~7 more |
| **Structural failures addressed** | 3/3 | 2/3 (spec-path: 1/3) | 1/3 (granularity only, probabilistic) | 1/3 immediately, 2/3 after Phase 2 |
| **Fixes 49% task reduction (file 08)** | Yes | Yes (TDD/PRD path) | Partially (prompt-dependent) | Yes (Phase 1 partial, Phase 2 full) |
| **Fixes one-shot truncation (web-01)** | Yes | Yes (TDD/PRD path) | No | No then Yes (Phase 2) |
| **Fills tasklist CLI gap (file 06)** | Yes | Yes (TDD/PRD path) | No | No then Yes (Phase 2) |
| **Enables progress monitoring** | Yes (stream-json) | Partial (TDD path only) | No | No then Partial (Phase 2) |
| **Gate breakage** | 6 gates need updates | 4 gates need updates | 0 gates | 0 then 4 gates |
| **Backward compatible** | No | Yes (spec-path unchanged) | Yes | Yes then Yes (spec-path) |
| **Time to first measurable improvement** | 10-15 days | 5-8 days | 1-2 days | 1-2 days |
| **Prior research gaps addressed (file 08 Sec 6)** | 5/5 HIGH gaps + architectural | 5/5 HIGH gaps + architectural (TDD path) | 5/5 HIGH gaps (prompt-level) | 5/5 HIGH gaps immediately + architectural later |
| **Deterministic step cascade risk (file 05)** | HIGH -- all 4 steps affected | MEDIUM -- conditional on input path | NONE | NONE then MEDIUM |

---

## Section 7: Recommendation

### Recommended Approach: Option D (Phased Migration)

#### Rationale

Option D is recommended because it combines the fastest path to measurable improvement with a structured migration toward the target architecture. The rationale rests on three evidence-backed arguments:

**1. The highest-impact gaps are prompt-level, not architectural.**

The prior research (file 08, Section 4) identified 5 root causes for the 49% task reduction. The two rated "HIGH impact -- strongest single cause" are:
- H2: PRD suppression language in `tasklist/prompts.py` lines 221-223 (code-verified, still present)
- H4: Protocol merge directives in SKILL.md lines 233, 255, 259 (code-verified, still present)

Both are fixable with prompt text changes (Option C scope). The architectural failures (one-shot truncation, no templates) contribute to quality variance but are not the primary drivers of the documented 49% regression. Addressing H2 and H4 first provides the highest ROI per implementation hour.

**2. Prompt improvements feed directly into template infrastructure.**

The task table schema constant (e.g., `_TASK_TABLE_SCHEMA = "| Task ID | Phase | Description | Dependencies | AC | Effort |"`) created in Phase 1 becomes the table definition in the Phase 2 output template. The anti-consolidation guard text becomes PART 1 instructions (file 07, Template 4 pattern). The ID preservation instruction added to `build_merge_prompt()` becomes a template enforcement rule. Phase 1 work is investment, not throwaway.

**3. Risk-gated decision: Phase 2 is contingent on Phase 1 validation.**

After Phase 1 ships and test fixtures are re-run (file 08, Section 9 Question 8: "New test runs are needed"), the results determine whether Phase 2 is necessary. If prompt improvements alone bring the TDD+PRD task count from 44 to 80+ (close to the spec-only baseline of 87), the architectural investment of Phase 2 may be deferrable. If the count remains below 70, the data justifies the Phase 2 investment. This is a data-driven decision gate, not a speculative commitment.

#### Key Trade-offs Accepted

| Trade-off | Accepted Because |
|-----------|-----------------|
| Phase 1 prompt enforcement is probabilistic (web-02 Finding F2) | Prompt improvements address the 5 highest-impact gaps (file 08). Even probabilistic enforcement is better than the current zero enforcement on task table schema (file 03 Gap #1). Phase 2 templates provide deterministic enforcement as follow-up. |
| Total effort is marginally higher than Option B alone | The 1-2 day Phase 1 cost is justified by the 5-8 day earlier delivery of measurable improvement. The data from Phase 1 de-risks the Phase 2 investment. |
| Spec-path one-shot truncation is not addressed in Phase 1 | Typical roadmap artifacts are 5k-20k tokens (web-01, Section 2: "well within limits"). Truncation is a tail risk for large specs, not a systemic failure. Phase 2 addresses this for TDD/PRD inputs where document size is larger. |
| Tasklist CLI generation gap persists through Phase 1 | The `/sc:tasklist` skill protocol (file 06, Section 3) continues to function for generation. Phase 2 adds the CLI subcommand. This is a convenience improvement, not a blocking deficiency. |

#### Implementation Sequence

**Phase 1 targets** (Option C scope, ~1-2 days):

| # | File | Change | Gap Addressed |
|---|------|--------|---------------|
| 1 | `src/superclaude/cli/tasklist/prompts.py` | Remove PRD suppression at lines 221-223, add anti-consolidation guard | G1, G9 (file 08) |
| 2 | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Tighten merge criteria (lines 233, 255, 259), add task count floor | G2, G3, G12 (file 08) |
| 3 | `src/superclaude/cli/roadmap/prompts.py` | Add task table schema to `build_generate_prompt()`, add ID preservation + `_INTEGRATION_ENUMERATION_BLOCK` to `build_merge_prompt()` | File 03 Gaps #1-#4 |
| 4 | Test fixture runs | Re-run pipeline with TDD+PRD input, compare task counts | File 08 Section 9 Question 8 |

**Phase 2 targets** (Option B scope, ~5-8 days, contingent on Phase 1 results):

| # | File | Change | Gap Addressed |
|---|------|--------|---------------|
| 5 | New: `src/superclaude/examples/roadmap_output_template.md` | PART 1/PART 2 roadmap output template with `{{SC_PLACEHOLDER:*}}` sentinels | File 07 Gaps #1-#2 |
| 6 | New: `src/superclaude/examples/tasklist_output_template.md` | PART 1/PART 2 tasklist output template with Sprint CLI compatibility | File 07 Gap #2, File 06 Section 3.5 |
| 7 | `src/superclaude/cli/roadmap/executor.py` | Conditional step building: TDD/PRD path uses template+tool-use, spec path uses current architecture | File 01 Section 4, File 02 Section 4 |
| 8 | `src/superclaude/cli/roadmap/executor.py` | `roadmap_run_step()` conditional: `output_format="stream-json"` for TDD path | File 04 Section 9 |
| 9 | `src/superclaude/cli/roadmap/gates.py` | Update 4 gates for template-structured output (EXTRACT bypass, GENERATE, MERGE, TEST_STRATEGY) | File 05 Summary Table |
| 10 | `src/superclaude/cli/tasklist/commands.py` | New `tasklist generate` CLI subcommand | File 06 Section 1 |
| 11 | `src/superclaude/cli/tasklist/executor.py` | Tasklist generation executor (template-driven) | File 06 Gap #4 |

---

### Decision Gate Between Phases

After Phase 1 implementation and test fixture validation:

| Metric | Proceed to Phase 2 | Defer Phase 2 |
|--------|--------------------|-----------------------|
| TDD+PRD task count | < 70 tasks (vs 87 spec-only baseline) | >= 70 tasks |
| Task granularity (manual review) | R-items still bundled (>1.5:1 work-item-to-R-item ratio) | R-items are granular (~1:1) |
| Output truncation incidents | Any truncation observed in test runs | No truncation |
| Stakeholder priority | Architectural improvement prioritized | Other features take priority |
