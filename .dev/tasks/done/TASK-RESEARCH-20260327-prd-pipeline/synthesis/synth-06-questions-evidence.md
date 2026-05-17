# Synthesis: Open Questions & Evidence Trail

**Sections:** 9 (Open Questions), 10 (Evidence Trail)
**Research question:** How to add `--prd-file` as a supplementary input to roadmap and tasklist CLI pipelines
**Date:** 2026-03-27
**Sources:** All research files (01-05, web-01), all synthesis files (synth-01 through synth-05), gaps-and-questions.md

---

## Section 9: Open Questions

The following questions remain unresolved across the research investigation. They are compiled from the gaps-and-questions.md log, the "Gaps and Questions" sections of each research file, and any [UNVERIFIED] claims found in the research corpus.

### 9.1 Unresolved Questions from Gaps Log

These questions were surfaced during QA review and remain open for synthesis or implementation to address.

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q1 | `tdd_file` on `RoadmapConfig` (models.py:115) is dead code -- never referenced by executor or CLI. Should PRD integration clean this up? | MEDIUM -- if both `tdd_file` and `prd_file` exist on `RoadmapConfig` but only `prd_file` is wired, it creates confusion and precedent for more dead fields. | Clean up as a separate preparatory commit. Either wire `tdd_file` end-to-end or remove it. Do not replicate the mistake for `prd_file`. Source: gaps-and-questions.md #1, 01-roadmap-cli-integration-points.md Section 1 |
| Q2 | 7 of 9 roadmap prompt builders need refactoring from single-return expression to `base = (...); if prd_file: ...; return` pattern before PRD blocks can be added. Does this increase implementation scope? | MEDIUM -- refactoring is mechanical but touches 7 functions across ~300 lines. Risk of introducing bugs in existing behavior during refactoring. | Yes, it increases scope. Mitigate by adding parametrized tests verifying identical output when `prd_file=None` before and after refactoring. Refactor as a dedicated phase before adding PRD blocks. Source: gaps-and-questions.md #2, 02-prompt-enrichment-mapping.md Section "Refactoring Required" |
| Q3 | PRD supplementary task generation is inherently weaker than TDD -- PRDs describe "what/why" not "how", so PRD content informs task descriptions but does not generate 1:1 implementation tasks as cleanly. Is this acceptable? | LOW -- expected by design. PRD enrichment is advisory, not generative. | Accept as a known limitation. Document in the implementation that PRD enrichment improves task quality (descriptions, prioritization) rather than task quantity. Source: gaps-and-questions.md #3, 04-skill-reference-layer.md Section 3.2 |
| Q4 | spec-panel is inference-only (no Python CLI backing). PRD additions to spec-panel only update the protocol doc, not Python code. Is this sufficient? | LOW -- spec-panel PRD behavior is exercised via `/sc:spec-panel` inference, not the CLI pipeline. Protocol doc updates are the correct mechanism. | Sufficient. No CLI code changes needed for spec-panel. Update `src/superclaude/commands/spec-panel.md` only. Source: gaps-and-questions.md #4, 04-skill-reference-layer.md Section 4.2 |
| Q5 | Deferred TDD generate prompt comment at prompts.py:309-316 references planned but unimplemented TDD-aware generate enrichment. Should this be addressed alongside PRD integration? | LOW -- the deferred TDD work and PRD integration are independent concerns. | Acknowledge the existing comment during implementation. Either implement TDD generate enrichment in the same PR or explicitly re-defer it with an updated comment. Do not silently ignore. Source: gaps-and-questions.md #5, 02-prompt-enrichment-mapping.md "Stale Documentation Found" |
| Q6 | `gates.py` received minimal investigation -- only noted as "no new gates needed" with no cited gate constants. Is this verified? | LOW -- likely correct since PRD is supplementary (no new pipeline steps requiring gates), but the assertion is unverified against actual gate constant definitions. | Confirm during implementation by reading `gates.py` gate constants (EXTRACT_GATE, GENERATE_A_GATE, etc.). No new gates should be needed, but verify no existing gate conditions break when PRD is present. Source: gaps-and-questions.md #6, 01-roadmap-cli-integration-points.md Section 3 |
| Q7 | PRD template file (`src/superclaude/examples/prd_template.md`) was never directly read by any research agent. PRD section inventory was sourced from `prd/SKILL.md` instead. Could section numbering diverge? | IMPORTANT -- if the template and SKILL.md have different section numbers, the prompt blocks referencing specific sections (e.g., "S7", "S19") would be wrong. | Cross-validate PRD section numbering between `src/superclaude/examples/prd_template.md` and `src/superclaude/skills/prd/SKILL.md` before drafting final prompt blocks. Source: gaps-and-questions.md #7, 05-prd-content-analysis.md Section 1 |
| Q8 | File 01 describes "9-step pipeline" but actual executor has 11 step entries (including anti-instinct and certify). Is this a discrepancy? | LOW -- cosmetic. The "9 steps" count refers to `_build_steps()` LLM steps, while 11 includes non-LLM steps (anti-instinct) and post-pipeline steps (certify). Both counts are correct at different scopes. | Clarify in implementation documentation that _build_steps() produces 9 LLM steps, with anti-instinct (non-LLM) and certify (post-pipeline) bringing the total to 11. Source: gaps-and-questions.md #8, 05-prd-content-analysis.md Section 3.1 |

### 9.2 Unresolved Questions from Research Files

These questions were raised within individual research files and not resolved by the gaps log or other research.

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| Q9 | Should PRD context flow only into extraction (step 1), or also into spec-fidelity (step 8b) and other downstream steps? | MEDIUM -- determines implementation scope. Extraction-only is minimal; multi-step injection maximizes value but increases complexity. | Implement P1 steps (extract, generate, spec-fidelity, test-strategy) and P2 steps (extract_tdd, score). Defer P3 steps (diff, debate, merge) to a follow-up. Source: 01-roadmap-cli-integration-points.md "Gaps and Questions" #2, 02-prompt-enrichment-mapping.md Summary |
| Q10 | Content embedding vs file reference: should PRD content be loaded as a string into the prompt (retrospective pattern) or added to `inputs` list for subprocess reading (tasklist TDD pattern)? | MEDIUM -- affects token consumption and subprocess architecture. | Use the `inputs` file path pattern since PRDs can be large. The subprocess reads the file via `_embed_inputs()`. This is consistent with how TDD files are handled in the tasklist pipeline. Source: 01-roadmap-cli-integration-points.md "Gaps and Questions" #3 |
| Q11 | Should `--prd-file` also be added to `superclaude roadmap validate`? The validate command currently has no supplementary input mechanism. | LOW -- validation is a separate subcommand with different concerns. | Defer to follow-up. Focus initial implementation on `roadmap run` and `tasklist validate`. Source: 01-roadmap-cli-integration-points.md "Gaps and Questions" #4 |
| Q12 | State persistence: if `prd_file` needs to persist across `--resume` cycles, should state serialization be updated? | LOW -- `retrospective_file` is also not persisted in state, establishing precedent for supplementary inputs not surviving resume. | Do not persist initially. Document as a known limitation. If resume support is needed later, add `prd_file` to `_save_state()` / `_restore_from_state()`. Source: 01-roadmap-cli-integration-points.md "Gaps and Questions" #5 |
| Q13 | When both PRD + TDD + spec are provided (triple input), how should extraction handle three supplementary contexts? | LOW -- rare scenario but architecturally important. | Stack both blocks: TDD block first (technical "how"), then PRD block (business "why"). Each is self-contained and non-overlapping. The `inputs` list simply includes both files. Source: 02-prompt-enrichment-mapping.md "Gaps and Questions" #2 |
| Q14 | With both TDD and PRD files embedded, the composed prompt could exceed `_EMBED_SIZE_LIMIT` (100KB). Is this a functional concern? | LOW -- the executor logs a warning but proceeds. No functional failure. | Acceptable for initial implementation. If large PRDs cause problems in practice, add a PRD content summarization pre-step. Source: 03-tasklist-integration-points.md "Gaps and Questions" #2 |
| Q15 | PRD extraction timing: should PRD supplementary content be extracted once at pipeline start and cached, or re-read at each step? | MEDIUM -- single extraction is more efficient; per-step allows step-specific summarization. | Single extraction (at the `extract` step) is recommended for efficiency. The structured extraction output is then referenced by downstream steps. Source: 05-prd-content-analysis.md "Gaps and Questions" #2 |
| Q16 | PRD-TDD consistency: should the pipeline include a lightweight check that the PRD and TDD are consistent (not stale relative to each other)? | LOW -- adds complexity with limited value for initial release. | Defer. Trust both documents as-is for initial implementation. Revisit if users report problems with stale PRDs. Source: 05-prd-content-analysis.md "Gaps and Questions" #5 |
| Q17 | Circular dependency risk: the PRD skill creates PRDs, the roadmap pipeline consumes them. If PRD skill outputs do not conform to expected structure, extraction fails silently. Should a schema contract exist? | MEDIUM -- silent failures are hard to debug. | Add a lightweight PRD structure validation at pipeline start (check for expected section headings). Log warnings for missing sections rather than failing. Source: 04-skill-reference-layer.md "Gaps and Questions" #7 |
| Q18 | PRD scoring formula: should PRDs get a custom 7-factor scoring formula (Option A) or reuse the standard 5-factor formula (Option B)? | LOW -- affects scoring accuracy but standard formula is adequate for initial release. | Use standard 5-factor formula (Option B) initially. PRD data enriches roadmap content without affecting complexity scoring. Revisit after production usage data is available. Source: 04-skill-reference-layer.md Section 2.2-2.3 |

### 9.3 Unverified Claims

The following claims were marked [UNVERIFIED] in the research corpus and should be confirmed during implementation.

| # | Claim | Source | Risk if Wrong | Suggested Verification |
|---|-------|--------|---------------|----------------------|
| U1 | Standard 5-factor scoring formula (requirement_count 0.25, dependency_depth 0.25, domain_spread 0.20, risk_severity 0.15, scope_size 0.15) and TDD 7-factor formula are implemented in the inference-based roadmap skill, not in deterministic CLI code. No `scoring.py` was found. | 04-skill-reference-layer.md Section 2.1 | LOW -- if scoring IS in CLI code, PRD may need CLI scoring changes | Grep for scoring factor names in `src/superclaude/cli/` to confirm no CLI scoring implementation exists |
| U2 | Tasklist SKILL.md Section 4.4a supplementary task generation (seven patterns from TDD context) is inference-based protocol behavior, not implemented in the programmatic CLI pipeline. | 04-skill-reference-layer.md Section 3.1 | LOW -- if task generation IS in CLI code, PRD task patterns would need CLI changes | Confirm `tasklist/executor.py` only does validation, not task generation |
| U3 | The PRD template file at `src/superclaude/examples/prd_template.md` has 28 sections matching the inventory in `prd/SKILL.md`. | 04-skill-reference-layer.md Section 1.2, 05-prd-content-analysis.md Section 1 | IMPORTANT -- section numbering in prompt blocks depends on this | Read `src/superclaude/examples/prd_template.md` and cross-validate section numbers |
| U4 | PRD detection rule signals (## Product Overview, ## User Personas, YAML frontmatter type containing "Product Requirements Document") are sufficient to distinguish PRDs from generic specs. | 04-skill-reference-layer.md Section 5 | LOW -- detection rules are documented for future reference only; current design uses explicit `--prd-file` flag, bypassing detection | No immediate verification needed; document for future reference if PRD-as-mode is reconsidered |

---

## Section 10: Evidence Trail

### 10.1 Codebase Research Files

All codebase research was conducted on 2026-03-27 against the current state of the `feat/tdd-spec-merge` branch.

| File | Full Path | Topic | Agent Type |
|------|-----------|-------|------------|
| research-notes.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/research-notes.md` | Research planning: file inventory, patterns, solution approach, recommended outputs, phase plan | Research Lead |
| 01-roadmap-cli-integration-points.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/01-roadmap-cli-integration-points.md` | Where `--prd-file` connects in roadmap commands.py, models.py, executor.py; dead `tdd_file` finding; step injection points | Code Tracer |
| 02-prompt-enrichment-mapping.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/02-prompt-enrichment-mapping.md` | Supplementary PRD text for each of 10 prompt builders; refactoring requirements; executor call site inventory | Code Tracer + Doc Analyst |
| 03-tasklist-integration-points.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/03-tasklist-integration-points.md` | Where `--prd-file` connects in tasklist commands.py, models.py, executor.py, prompts.py; full TDD pattern trace | Code Tracer |
| 04-skill-reference-layer.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/04-skill-reference-layer.md` | PRD-aware updates to extraction-pipeline.md, scoring.md, tasklist SKILL.md, spec-panel.md | Doc Analyst |
| 05-prd-content-analysis.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/05-prd-content-analysis.md` | Full 28-section PRD inventory; TDD extraction loss analysis; pipeline touchpoint matrix; tiered section recommendation | Architecture Analyst |

### 10.2 Web Research Files

| File | Full Path | Topic |
|------|-----------|-------|
| web-01-prd-driven-roadmapping.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/web-01-prd-driven-roadmapping.md` | Industry patterns for PRD-informed roadmapping: RICE/WSJF/MoSCoW frameworks, product vs engineering roadmap boundary, JTBD as bridge, context engineering for LLM pipelines |

### 10.3 Synthesis Files

| File | Full Path | Report Sections Covered | Source Research |
|------|-----------|------------------------|-----------------|
| synth-01-problem-current-state.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/synthesis/synth-01-problem-current-state.md` | S1 Problem Statement, S2 Current State | 01, 02, 03, 04, 05 |
| synth-02-target-gaps.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/synthesis/synth-02-target-gaps.md` | S3 Target State, S4 Gap Analysis | All research files |
| synth-03-external-findings.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/synthesis/synth-03-external-findings.md` | S5 External Research Findings | web-01 |
| synth-04-options-recommendation.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/synthesis/synth-04-options-recommendation.md` | S6 Options Analysis, S7 Recommendation | All research files |
| synth-05-implementation-plan.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/synthesis/synth-05-implementation-plan.md` | S8 Implementation Plan | 01, 02, 03, 04 |
| synth-06-questions-evidence.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/synthesis/synth-06-questions-evidence.md` | S9 Open Questions, S10 Evidence Trail | All files |

### 10.4 Gaps Log

| File | Full Path | Purpose |
|------|-----------|---------|
| gaps-and-questions.md | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/gaps-and-questions.md` | Consolidated gap tracking compiled from analyst-completeness-report.md, qa-research-gate-report.md, and qa-research-gate-fix-cycle-1.md. Contains 4 resolved issues and 8 open questions. |

### 10.5 Stale Documentation Findings

The following documentation inconsistencies were identified across the research and should be corrected during or after implementation.

| # | Location | Finding | Severity | Source |
|---|----------|---------|----------|--------|
| D1 | `RoadmapConfig` docstring (models.py:98-99) | Does not mention `convergence_enabled`, `allow_regeneration`, `input_type`, or `tdd_file` fields added after original documentation | LOW | 01-roadmap-cli-integration-points.md "Stale Documentation" #1 |
| D2 | `_build_steps()` docstring/comments (executor.py) | Says "9-step pipeline" but function produces 10-11 step entries depending on scope counted | LOW | 01-roadmap-cli-integration-points.md "Stale Documentation" #2 |
| D3 | extraction-pipeline.md TDD detection rule (L145) | Describes simple three-rule boolean OR; actual code uses weighted scoring system with threshold | MEDIUM | 04-skill-reference-layer.md "Stale Documentation" #1 |
| D4 | tasklist SKILL.md `--spec` flag (Section 4.1a) | Protocol describes `--spec` flag; actual CLI uses `--tdd-file` flag | LOW | 04-skill-reference-layer.md "Stale Documentation" #2 |
| D5 | tasklist SKILL.md Section 4.4a task generation | Describes seven TDD task generation patterns; CLI only implements three validation checks | MEDIUM | 04-skill-reference-layer.md "Stale Documentation" #3 |
| D6 | TDD detection rule duplication | Same detection rule stated in 4 different files with textual variations; should reference single canonical definition | LOW | 04-skill-reference-layer.md "Stale Documentation" #4 |
| D7 | `build_generate_prompt` deferred work comment (prompts.py:309-316) | References planned TDD-aware generate enrichment that was never implemented | LOW | 02-prompt-enrichment-mapping.md "Stale Documentation" #1 |
