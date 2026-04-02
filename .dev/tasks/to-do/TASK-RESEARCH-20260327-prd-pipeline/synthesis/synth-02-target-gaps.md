# Synthesis Report: Target State & Gap Analysis

**Sections:** 3 (Target State), 4 (Gap Analysis)
**Research question:** How to add `--prd-file` as a supplementary input to roadmap and tasklist CLI pipelines
**Date:** 2026-03-27
**Sources:** 01-roadmap-cli-integration-points.md, 02-prompt-enrichment-mapping.md, 03-tasklist-integration-points.md, 04-skill-reference-layer.md, 05-prd-content-analysis.md, web-01-prd-driven-roadmapping.md, gaps-and-questions.md

---

## Section 3: Target State

### 3.1 Desired Behavior

The `--prd-file` flag provides **supplementary PRD enrichment** across both the roadmap and tasklist CLI pipelines. It follows the established TDD integration pattern: an optional file path is accepted via CLI flag, resolved to an absolute path, stored on the pipeline config dataclass, passed into the executor's step builder, appended to step input lists for file embedding, and forwarded as a keyword argument to prompt builders that conditionally append PRD-aware instruction blocks.

PRD content enriches the pipeline by injecting business context ("why/who") that specification and TDD files ("what/how") do not carry. The enrichment is advisory -- PRD content informs prioritization, fidelity checks, and test strategy but never overrides technical dependency ordering or specification authority.

**End-to-end data flow (both pipelines):**

```
CLI invocation
  |
  v
--prd-file <path>                    click.Path(exists=True, path_type=Path)
  |
  v
Config dataclass                     prd_file: Path | None = None
  |
  v
Executor _build_steps()
  |
  +---> step.inputs.append(prd_file) file content embedded via _embed_inputs()
  |
  +---> prompt_builder(prd_file=...) conditional supplementary block activated
  |
  v
Claude subprocess receives:
  - Embedded PRD file content (fenced code block in prompt)
  - Supplementary PRD instruction block (numbered checks + severity guidance)
```

**Roadmap pipeline enrichment targets (by step):**

| Step | Prompt Builder | PRD Enrichment | Priority |
|------|---------------|----------------|----------|
| extract | `build_extract_prompt` | Business objectives, personas, scope boundaries, compliance, JTBD | P1 |
| extract (TDD mode) | `build_extract_prompt_tdd` | Personas, compliance, success metrics (subset of above) | P2 |
| generate-A/B | `build_generate_prompt` | Value-based phasing, persona-driven sequencing, compliance gates, scope guardrails | P1 |
| diff | `build_diff_prompt` | Business alignment comparison (indirect -- benefits from richer generate) | P3 |
| debate | `build_debate_prompt` | Business value evaluation criterion | P3 |
| score | `build_score_prompt` | Business value delivery, persona coverage, compliance alignment scoring | P2 |
| merge | `build_merge_prompt` | Persona and metric preservation verification | P3 |
| test-strategy | `build_test_strategy_prompt` | Persona acceptance tests, journey E2E tests, KPI validation, compliance test category, edge cases | P1 |
| spec-fidelity | `build_spec_fidelity_prompt` | Persona coverage (dim 12), metric traceability (dim 13), compliance coverage (dim 14), scope boundary enforcement (dim 15) | P1 |
| wiring-verification | `build_wiring_verification_prompt` | None -- structural code verification, no PRD relevance | Skip |

**Tasklist pipeline enrichment targets:**

| Step | Prompt Builder | PRD Enrichment | Priority |
|------|---------------|----------------|----------|
| tasklist-fidelity | `build_tasklist_fidelity_prompt` | Persona flow coverage, KPI instrumentation tasks, compliance tasks, UX flow alignment | P1 |

**PRD sections most referenced across all prompt blocks (from File 02 analysis):**

| PRD Section | # of Prompt Builders Referencing It |
|-------------|-------------------------------------|
| S7: User Personas | 8 of 9 |
| S19: Success Metrics | 7 of 9 |
| S17: Legal & Compliance | 6 of 9 |
| S12: Scope Definition | 4 of 9 |
| S22: Customer Journey Map | 3 of 9 |
| S6: JTBD | 2 of 9 (but highest value in extract) |

### 3.2 Success Criteria

| # | Criterion | Verification Method |
|---|-----------|-------------------|
| SC-1 | **Backward compatible**: All pipeline commands produce identical output when `--prd-file` is not provided | Run existing test suite; all tests pass without modification |
| SC-2 | **No new mode**: `--input-type` choices remain `["auto", "tdd", "spec"]`; `detect_input_type()` is unchanged | Code inspection; no new enum values or detection signals added |
| SC-3 | **PRD sections accessible in prompts**: When `--prd-file` is provided, the embedded PRD file content appears in the Claude subprocess prompt for targeted steps | Integration test: invoke pipeline with `--prd-file`, inspect generated prompt for `## Supplementary PRD` heading |
| SC-4 | **Both-files coexistence**: `--prd-file` and `--tdd-file` (tasklist) or `--retrospective` (roadmap) can be provided simultaneously without conflict | Test: provide both flags; verify both supplementary blocks appear in prompt |
| SC-5 | **File validation**: `--prd-file` with a nonexistent path fails with Click's standard error before pipeline execution | Test: invoke with nonexistent path; verify Click error |
| SC-6 | **Advisory guardrail in all prompt blocks**: Every supplementary PRD block includes the phrase "do NOT treat PRD content as hard requirements" | Grep prompt builder source for guardrail text |
| SC-7 | **TDD pattern fidelity**: The `--prd-file` integration follows the exact 4-layer wiring pattern (CLI flag -> config field -> executor inputs + prompt kwarg -> conditional prompt block) demonstrated by `--tdd-file` in the tasklist pipeline | Code review against `src/superclaude/cli/tasklist/` reference implementation |

### 3.3 Constraints

| # | Constraint | Rationale | Source |
|---|-----------|-----------|--------|
| C-1 | **Must follow TDD integration pattern** | The `--tdd-file` wiring in `src/superclaude/cli/tasklist/` is the established, tested pattern for supplementary inputs. Deviation introduces inconsistency and testing risk. | Files 01, 03 |
| C-2 | **No `detect_input_type()` changes** | PRD is supplementary context, not a primary input mode. Adding a "prd" detection mode would require a three-way classifier and break the existing auto/tdd/spec routing. | File 01 (executor.py L59-117), gaps-and-questions.md (Resolved #1) |
| C-3 | **No new `--input-type` choices** | `Literal["auto", "tdd", "spec"]` remains unchanged. PRD input type is determined solely by presence of `--prd-file` flag. | File 01 (models.py L114) |
| C-4 | **PRD file must exist when specified** | Use `click.Path(exists=True)` (not `exists=False` like `--retrospective`). A specified PRD that does not exist is a user error. | File 01 (commands.py pattern analysis) |
| C-5 | **No prompt builders for wiring-verification gain `prd_file`** | `build_wiring_verification_prompt` performs structural code verification with zero PRD relevance. Adding the parameter would be dead code. | File 02 (builder analysis) |
| C-6 | **Supplementary blocks must not restructure phases** | PRD context annotates and enriches but never overrides technical dependency ordering. Industry consensus: engineering roadmap = How/When; PRD provides Why annotations. | web-01 (Section 3.1, 3.2) [EXTERNAL] |
| C-7 | **`prd_file` must be wired end-to-end** | The existing `tdd_file` on `RoadmapConfig` (models.py L115) is dead code -- no CLI flag, no executor reference. `prd_file` must not replicate this mistake. Every config field must have a CLI flag and executor consumer. | File 01 (gap finding) |
| C-8 | **PRD content is advisory** | All supplementary prompt blocks must include the guardrail: "do NOT treat PRD content as hard requirements unless also stated in the specification/TDD." | File 02 (design decision #1) |

---

## Section 4: Gap Analysis

### 4.1 Gap Analysis Table

| # | Gap | Current State | Target State | Severity | Notes |
|---|-----|--------------|--------------|----------|-------|
| **G-1** | **Model field missing: `RoadmapConfig.prd_file`** | `RoadmapConfig` has `tdd_file: Path \| None = None` at L115 of `src/superclaude/cli/roadmap/models.py` but NO `prd_file` field. `tdd_file` is dead code (no CLI flag, no executor ref). | Add `prd_file: Path \| None = None` after `tdd_file` at L115. Follow same type pattern. | HIGH | Trivial change. Note: existing `tdd_file` is dead code -- consider wiring it up or removing it as separate tech debt. [CODE-VERIFIED: File 01] |
| **G-2** | **Model field missing: `TasklistValidateConfig.prd_file`** | `TasklistValidateConfig` has `tdd_file: Path \| None = None` at L25 of `src/superclaude/cli/tasklist/models.py` but NO `prd_file` field. | Add `prd_file: Path \| None = None` after `tdd_file` at L25. | HIGH | Trivial change. [CODE-VERIFIED: File 03] |
| **G-3** | **CLI flag missing: roadmap `run` command lacks `--prd-file`** | `src/superclaude/cli/roadmap/commands.py` has `--retrospective` (L96-104) and `--input-type` (L106-110) but no `--prd-file` option. | Add `@click.option("--prd-file", type=click.Path(exists=True, path_type=Path), default=None, ...)` to the `run` command. Wire into `config_kwargs` with `.resolve()`. | HIGH | Use `exists=True` (unlike `--retrospective` which uses `exists=False`). [CODE-VERIFIED: File 01] |
| **G-4** | **CLI flag missing: tasklist `validate` command lacks `--prd-file`** | `src/superclaude/cli/tasklist/commands.py` has `--tdd-file` (L61-66) but no `--prd-file` option. | Add `@click.option("--prd-file", ...)` immediately after `--tdd-file`. Add `prd_file: Path \| None` to function signature (L74). Wire into `TasklistValidateConfig` with `.resolve()`. | HIGH | Direct clone of `--tdd-file` pattern. [CODE-VERIFIED: File 03] |
| **G-5** | **Executor wiring missing: roadmap `_build_steps()` does not pass `prd_file`** | `src/superclaude/cli/roadmap/executor.py` `_build_steps()` (L843-1012) passes `retrospective_content` to extract prompt builders and assembles `inputs` lists, but has no `prd_file` handling. `config.tdd_file` is never read in `_build_steps()`. | Pass `prd_file=config.prd_file` to prompt builder calls at 10 call sites (L888, L893, L908, L918, L930, L940, L950, L960, L980, L990). Add `config.prd_file` to `step.inputs` lists for P1 and P2 steps. | HIGH | 10 call sites need `prd_file=config.prd_file` kwarg. P1 steps (extract, generate, spec-fidelity, test-strategy) and P2 steps (extract_tdd, score) should also get the file in `inputs` for embedding. P3 steps (diff, debate, merge) get the kwarg but NOT the file embedding (prompt references PRD indirectly through extraction output). [CODE-VERIFIED: File 02, executor wiring table] |
| **G-6** | **Executor wiring missing: tasklist `_build_steps()` does not pass `prd_file`** | `src/superclaude/cli/tasklist/executor.py` `_build_steps()` (L188-211) appends `config.tdd_file` to `all_inputs` and passes `tdd_file=config.tdd_file` to prompt builder, but has no `prd_file` handling. | After TDD block (L193-194), add: `if config.prd_file is not None: all_inputs.append(config.prd_file)`. Pass `prd_file=config.prd_file` to `build_tasklist_fidelity_prompt()` call. | HIGH | 2 changes in one function. Both-files behavior: `all_inputs = [roadmap, *tasklists, tdd, prd]`. [CODE-VERIFIED: File 03] |
| **G-7** | **Prompt enrichment missing: `build_extract_prompt` (roadmap)** | `src/superclaude/cli/roadmap/prompts.py` L82-85: signature has `retrospective_content` but no `prd_file`. Already uses `base = (...)` pattern -- no refactoring needed. | Add `prd_file: Path \| None = None` parameter. Append conditional `## Supplementary PRD Context` block with 5 check items: business objectives (S19), personas (S7), scope boundaries (S12), compliance (S17), JTBD (S6). Include advisory guardrail. | HIGH | P1 builder. No refactoring needed -- already uses base pattern. [CODE-VERIFIED: File 02] |
| **G-8** | **Prompt enrichment missing: `build_extract_prompt_tdd` (roadmap)** | `src/superclaude/cli/roadmap/prompts.py` L161-164: same as G-7 but for TDD extraction mode. Already uses `base = (...)` pattern. | Add `prd_file: Path \| None = None` parameter. Append conditional block with 3 check items: success metrics (S19), personas (S7), compliance (S17). Include advisory guardrail. | MEDIUM | P2 builder. Fewer items than G-7 because TDD already captures most technical content. [CODE-VERIFIED: File 02] |
| **G-9** | **Prompt enrichment missing: `build_generate_prompt` (roadmap)** | `src/superclaude/cli/roadmap/prompts.py` L288: signature takes `(agent, extraction_path)` only. Returns single concatenated expression (L295-335). | Add `prd_file: Path \| None = None` parameter. **Requires refactoring** from single return expression to `base = (...); if prd_file: base += ...; return base + blocks` pattern. Append 4 check items: value-based phasing (S5, S19), persona-driven sequencing (S7, S22), compliance gates (S17), scope guardrails (S12). | HIGH | P1 builder. Refactoring adds complexity but pattern is identical to `build_extract_prompt`. [CODE-VERIFIED: File 02] |
| **G-10** | **Prompt enrichment missing: `build_spec_fidelity_prompt` (roadmap)** | `src/superclaude/cli/roadmap/prompts.py` L448-451: signature takes `(spec_file, roadmap_path)`. Returns single expression. Has 11 existing comparison dimensions (L489-500). | Add `prd_file: Path \| None = None`. **Requires refactoring.** Append dimensions 12-15: persona coverage (S7), metric traceability (S19), compliance coverage (S17, HIGH severity), scope boundary enforcement (S12). | HIGH | P1 builder. Dimensions numbered 12-15 continuing from existing 11. Compliance gaps flagged as HIGH severity (all others MEDIUM). [CODE-VERIFIED: File 02] |
| **G-11** | **Prompt enrichment missing: `build_test_strategy_prompt` (roadmap)** | `src/superclaude/cli/roadmap/prompts.py` L586-589: signature takes `(roadmap_path, extraction_path)`. Returns single expression. | Add `prd_file: Path \| None = None`. **Requires refactoring.** Append 5 check items: persona acceptance tests (S7), customer journey E2E tests (S22), KPI validation tests (S19), compliance test category (S17), edge case coverage (S23). | HIGH | P1 builder. Highest unique-value PRD enrichment -- personas, journeys, and edge cases are not in specs or TDDs. [CODE-VERIFIED: File 02] |
| **G-12** | **Prompt enrichment missing: `build_score_prompt` (roadmap)** | `src/superclaude/cli/roadmap/prompts.py` L390-394: signature takes `(debate_path, variant_a_path, variant_b_path)`. Returns single expression. | Add `prd_file: Path \| None = None`. **Requires refactoring.** Append 3 scoring dimensions: business value delivery (S19), persona coverage (S7), compliance alignment (S17). | MEDIUM | P2 builder. Adds business value layer to technical scoring. WSJF framework (User-Business Value + Time Criticality + Risk Reduction) is industry best practice for combined scoring. [EXTERNAL: web-01 Section 2.2] |
| **G-13** | **Prompt enrichment missing: `build_diff_prompt`, `build_debate_prompt`, `build_merge_prompt` (roadmap)** | Three builders at L338, L363, L416 of `src/superclaude/cli/roadmap/prompts.py`. All return single expressions. None accept supplementary inputs. | Add `prd_file: Path \| None = None` to all three. **All require refactoring.** Append minimal blocks (1-2 check items each). | LOW | P3 builders. Diminishing returns -- PRD context already absorbed at extraction and generation. These get the parameter for completeness but file is NOT embedded in step inputs. [CODE-VERIFIED: File 02] |
| **G-14** | **Prompt enrichment missing: `build_tasklist_fidelity_prompt` (tasklist)** | `src/superclaude/cli/tasklist/prompts.py` L17-21: signature has `tdd_file` but no `prd_file`. Already uses `base = (...)` pattern with conditional TDD block at L110-123. | Add `prd_file: Path \| None = None` parameter. Append conditional `## Supplementary PRD Validation` block after TDD block with 4 check items: persona flow coverage, KPI instrumentation, stakeholder/compliance tasks, UX flow alignment. | HIGH | No refactoring needed -- follows existing TDD conditional block pattern exactly. Both blocks stack independently when both files provided. [CODE-VERIFIED: File 03] |
| **G-15** | **Skill/reference layer missing: `extraction-pipeline.md` has no PRD content** | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` (441 lines) has TDD-specific extraction steps (Steps 9-15) but no PRD extraction steps. | Add PRD-specific extraction guidance (Steps 16-22 or equivalent supplementary section) covering: user_personas, user_stories, success_metrics, market_constraints, release_strategy, stakeholder_priorities, acceptance_scenarios. Mark as supplementary-only (not a new mode). | MEDIUM | This is an inference-protocol doc, not CLI code. Changes inform the `/sc:roadmap` skill behavior. The CLI pipeline uses prompt blocks (G-7 through G-13), not these extraction steps. [DOC-SOURCED: File 04, Section 1] |
| **G-16** | **Skill/reference layer missing: `scoring.md` has no PRD scoring guidance** | `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` (196 lines) has TDD 7-factor formula and type match lookup but no PRD equivalent. | Add PRD detection rule, recommend standard 5-factor formula for initial implementation (Option B), add `product` row to Type Match Lookup table. Defer PRD-specific 7-factor formula (Option A) until production usage data available. | LOW | Inference-protocol doc. Initial recommendation: no PRD-specific scoring formula -- use standard 5-factor. Revisit after production data. [File 04, Section 2.2-2.3] |
| **G-17** | **Skill/reference layer missing: `tasklist SKILL.md` has no PRD supplementary context** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (599+ lines) has Section 4.1a (TDD supplementary context) and Section 4.4a (TDD task generation) but no PRD equivalents. | Add Section 4.1b (PRD supplementary context: user_personas, user_stories, success_metrics, release_strategy, stakeholder_priorities, acceptance_scenarios) and Section 4.4b (PRD task generation patterns). | MEDIUM | Inference-protocol doc. PRD task generation is weaker than TDD (PRDs describe "what/why" not "how") -- enrichment rather than 1:1 task creation. [File 04, Section 3] |
| **G-18** | **PRD content mapping missing: only 5 of 28 PRD sections reach the pipeline today** | The TDD PRD extraction agent extracts S12, S14, S19, S21 (epics + stories) -- ~18% of PRD content. 23 sections are lost including business rationale (S1-S5), user context (S6-S7, S16, S22), compliance (S17), risk (S10, S20), edge cases (S23), API contracts (S25). | With `--prd-file`, the pipeline gains access to all 28 sections via file embedding. Prompt blocks should prioritize 9 Tier-1 sections: S6 (JTBD), S7 (Personas), S10 (Constraints), S11 (Dependencies), S17 (Compliance), S20 (Risk), S22 (Journey), S23 (Edge Cases), S25 (API Contracts). This raises effective coverage from ~18% to ~50%. | HIGH | The prompt blocks (G-7 through G-14) already reference the correct Tier-1 sections. File embedding via `_embed_inputs()` makes all sections accessible; prompt blocks direct the LLM to the highest-value ones. [File 05, Section 4.1-4.2] |
| **G-19** | **Prompt builder refactoring required for 7 of 9 roadmap builders** | 7 builders use single `return (...)` expression pattern: `build_generate_prompt` (L295-335), `build_diff_prompt` (L345-360), `build_debate_prompt` (L374-387), `build_score_prompt` (L399-413), `build_merge_prompt` (L426-445), `build_spec_fidelity_prompt` (L461-525), `build_test_strategy_prompt` (L596-629). Only `build_extract_prompt` and `build_extract_prompt_tdd` already use `base = (...)` pattern. | Refactor each to: `base = (...); if prd_file: base += ...; return base + _OUTPUT_FORMAT_BLOCK`. Behavior is identical when `prd_file=None`. | MEDIUM | Structural prerequisite for PRD integration. Refactoring changes code shape but not behavior. Add parametrized tests verifying identical output when `prd_file=None`. [CODE-VERIFIED: File 02] |
| **G-20** | **`spec-panel.md` has no PRD input handling** | `src/superclaude/commands/spec-panel.md` has Step 6a (TDD detection) and Step 6b (downstream roadmap frontmatter) but no PRD equivalent. | Add Step 6c (PRD input detection) and Step 6d (downstream roadmap frontmatter for PRD). Add "Output -- When Input Is a PRD" section. | LOW | Inference-only command -- no Python CLI backing. PRD additions are protocol doc changes only, no code impact. [File 04, Section 4] |

### 4.2 Gap Severity Distribution

| Severity | Count | Gaps |
|----------|-------|------|
| HIGH | 12 | G-1, G-2, G-3, G-4, G-5, G-6, G-7, G-9, G-10, G-11, G-14, G-18 |
| MEDIUM | 5 | G-8, G-12, G-15, G-17, G-19 |
| LOW | 3 | G-13, G-16, G-20 |

### 4.3 Implementation Dependency Map

```
                    G-1 (RoadmapConfig.prd_file)
                   /                              \
                  v                                v
        G-3 (roadmap --prd-file)          G-5 (roadmap executor wiring)
                  |                        /    |    |    |    \
                  v                       v     v    v    v     v
            config_kwargs          G-7  G-8  G-9  G-10  G-11  (+ G-12, G-13)
                                 extract  tdd  gen  fid  test   score/diff/etc

                    G-2 (TasklistConfig.prd_file)
                   /                              \
                  v                                v
        G-4 (tasklist --prd-file)          G-6 (tasklist executor wiring)
                  |                                |
                  v                                v
            config with prd_file             G-14 (tasklist prompt)


        G-19 (refactoring) --blocks--> G-9, G-10, G-11, G-12, G-13
                                       (builders requiring base pattern)

        G-15, G-16, G-17, G-20 (skill/reference docs) -- independent of code gaps
```

### 4.4 Contradictions and Discrepancies Found

| # | Contradiction | Sources | Resolution |
|---|--------------|---------|------------|
| 1 | File 01 says "9-step pipeline" but File 05 counts 11 step entries (includes anti-instinct + certify). | File 01 (executor.py docstring), File 05 (Section 3.1) | Both correct at different scopes. `_build_steps()` returns 9 `Step` objects; the full pipeline also includes non-LLM anti-instinct and post-pipeline certify for 11 total entries. Cosmetic discrepancy. |
| 2 | File 04 originally proposed extending `detect_input_type()` for PRD mode, contradicting File 01's finding that PRD is supplementary-only. | File 04 (original), File 01 (Section 3) | Resolved in QA fix-cycle 1 (gaps-and-questions.md Resolved #1). PRD is supplementary only. No `detect_input_type()` changes. |
| 3 | File 02 proposes PRD enrichment for ALL 9 non-wiring prompt builders (including P3 diff/debate/merge). File 05 recommends injecting PRD content only into steps that need it (extract, generate, test-strategy, spec-fidelity). | File 02 (full mapping), File 05 (Section 4.3) | Not a true contradiction -- both agree P3 builders have "diminishing returns." Recommendation: add `prd_file` parameter to all 9 for API consistency, but only embed the PRD file in `step.inputs` for P1/P2 steps. P3 steps get the parameter but no file embedding. |
| 4 | `extraction-pipeline.md` TDD detection rule describes a 3-rule boolean OR. Actual code (`executor.py` L57-117) uses a weighted scoring system with different thresholds. | File 04 (Section 1.1), File 01 (Section 3) | Stale doc. The code's scoring-based approach is authoritative. Doc should be updated to reflect weighted scoring. [CODE-CONTRADICTED] |
| 5 | Tasklist `SKILL.md` references `--spec` flag with auto-detection. CLI uses `--tdd-file` with no auto-detection. | File 04 (Section 3.1) | Expected divergence: SKILL.md describes inference-based protocol; CLI is programmatic. Different interfaces for same concept. Not a bug. [CODE-CONTRADICTED, expected] |

### 4.5 Open Questions Deferred to Implementation

| # | Question | Recommendation | Source |
|---|----------|---------------|--------|
| 1 | Should the dead `tdd_file` on `RoadmapConfig` be wired up or removed? | Separate tech debt task. Do not conflate with PRD integration. | File 01, gaps-and-questions.md Q#1 |
| 2 | Should `--prd-file` be added to `superclaude roadmap validate`? | Defer. `ValidateConfig` currently has no supplementary inputs. Add after `run` integration is proven. | File 01 (Section 2, validate command) |
| 3 | PRD template file (`src/superclaude/examples/prd_template.md`) section numbering -- cross-validate against actual template? | Yes -- verify before finalizing prompt block section references (S6, S7, etc.). File 02 and 05 used `prd/SKILL.md` as source. | gaps-and-questions.md Q#7 |
| 4 | Token budget impact of embedding full PRD in multiple steps? | Cap at P1/P2 steps only. The `_EMBED_SIZE_LIMIT` (100KB) already guards against oversized prompts. Log warning if PRD exceeds threshold. | File 03 (Section 6, Q#2), File 05 (Section 4.3) |
| 5 | PRD staleness relative to TDD -- should pipeline check consistency? | Defer. Trust both documents as-is for initial implementation. Add lightweight consistency check as future enhancement. | File 05 (Gaps Q#5) |
| 6 | Circular dependency risk: PRD skill output format vs. pipeline input expectations? | Define schema contract between PRD skill output sections and prompt block section references. Not blocking for initial implementation. | File 04 (Gaps Q#7) |

---

**End of Sections 3-4.**
