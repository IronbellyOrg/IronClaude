# Research Notes: CLI TDD Integration

**Date:** 2026-03-25
**Scenario:** A (explicit request — all goals, file locations, specific questions, and known facts provided)
**Depth Tier:** Deep (14+ files across 3 subsystems; architectural decisions; implementation plan required)
**Status:** Complete

---

## EXISTING_FILES

### Primary target: `src/superclaude/cli/roadmap/`

| File | Purpose | Lines (est.) | TDD-relevance |
|------|---------|-------------|---------------|
| `executor.py` | Orchestrates all 14 pipeline steps; calls `_embed_inputs()` to pass spec to Claude subprocesses; calls `_run_anti_instinct_audit()` and `_run_structural_audit()` as pure-Python hooks | ~800 | CRITICAL — spec_file flows through here |
| `commands.py` | Click CLI: `superclaude roadmap run <spec_file>` — positional arg only, no `--input-type` flag | ~150 | HIGH — entry point for TDD input |
| `prompts.py` | All prompt builders: `build_extract_prompt()`, `build_generate_prompt()`, `build_spec_fidelity_prompt()`, `build_wiring_verification_prompt()`, etc. | ~400 | CRITICAL — extract prompt hardcoded to "specification" language |
| `gates.py` | 14 GateCriteria definitions with STRICT/STANDARD/LIGHT tiers and semantic check functions | ~1100 | HIGH — all gates must be TDD-compatible |
| `models.py` | `RoadmapConfig`, `ValidateConfig`, `AgentSpec`, `Finding` typed data | ~200 | MEDIUM — may need new fields |
| `spec_parser.py` | Python parser: extracts YAML frontmatter, markdown tables, fenced code blocks, requirement IDs (FR-xxx pattern), function signatures, numeric thresholds, file paths | ~500 | HIGH — used by fidelity_checker; TDD-compatible? |
| `validate_executor.py` | Validate pipeline reads roadmap.md + test-strategy.md + extraction.md ONLY; does NOT read original spec | ~200 | LOW — no spec file; mostly unaffected |
| `validate_prompts.py` | `build_reflect_prompt()` validates roadmap against test-strategy + extraction across 7 dimensions; `build_merge_prompt()` for adversarial merge | ~150 | LOW — validates pipeline artifacts, not spec/TDD |
| `validate_gates.py` | REFLECT_GATE, ADVERSARIAL_MERGE_GATE | ~50 | LOW — artifact validation only |
| `fidelity_checker.py` | Uses spec_parser to extract FR IDs from spec, then searches codebase `.py` files via AST+string match for evidence of implementation | ~200 | MEDIUM — TDD FR format in §5 same as spec format |
| `obligation_scanner.py` | Pure Python; scans ROADMAP content for undischarged scaffolding obligations | ~150 | NONE — reads roadmap, not spec |
| `integration_contracts.py` | Pure Python; extracts dispatch patterns (7 regex categories) from SPEC text; verifies coverage in roadmap | ~300 | HIGH — reads spec; TDD §6 arch + §8 API have these patterns |
| `fingerprint.py` | Pure Python; extracts code-level identifiers from spec (backtick names, code-block defs, ALL_CAPS constants); checks ≥70% present in roadmap | ~200 | HIGH — reads spec; TDD has MORE identifiers than spec (TypeScript interfaces) |
| `spec_structural_audit.py` | Warning-only hook; checks extraction adequacy vs. spec structural indicators | ~150 | MEDIUM — TDD structural indicators different from spec |
| `convergence.py` | Budget accounting for convergence cycles using TurnLedger | ~150 | LOW — budget tracking only |
| `semantic_layer.py` | Adversarial validation with debate protocol; 30KB budget; works on spec+roadmap | ~400 | MEDIUM — spec content used in debate |
| `remediate.py`, `remediate_executor.py`, `remediate_parser.py`, `remediate_prompts.py` | Remediation pipeline for fixing deviation findings | ~400 | LOW — operates on roadmap/deviation artifacts |
| `certify_prompts.py` | Certification prompts | ~100 | LOW |
| `spec_patch.py` | Spec patching utilities | ~100 | LOW |
| `structural_checkers.py` | Structural checking functions | ~200 | MEDIUM |

### Primary target: `src/superclaude/cli/tasklist/`

| File | Purpose | TDD-relevance |
|------|---------|---------------|
| `commands.py` | CLI: `superclaude tasklist validate <output_dir>` — NO `--spec` flag; only `--roadmap-file`, `--tasklist-dir` | HIGH — spec flag gap confirmed at CLI level |
| `executor.py` | Embeds roadmap + tasklist inline; spawns Claude subprocess; validates roadmap→tasklist ONLY | MEDIUM — no TDD access at all |
| `prompts.py` | `build_tasklist_fidelity_prompt()` — explicit "VALIDATION LAYERING GUARD: roadmap→tasklist ONLY" | MEDIUM — prompt would need TDD enrichment option |
| `gates.py` | TASKLIST_FIDELITY_GATE | LOW — gate validates completeness of deviation report |
| `models.py` | `TasklistValidateConfig` | MEDIUM — would need `tdd_file` field for TDD enrichment |

### Primary target: `src/superclaude/cli/pipeline/`

| File | Purpose | TDD-relevance |
|------|---------|---------------|
| `executor.py` | Generic step sequencer: sequential+parallel, retry, gate checking | NONE — format-agnostic |
| `process.py` | `ClaudeProcess`: spawns `claude --print -p "<prompt>"`; strips CLAUDECODE env | NONE — format-agnostic |
| `gates.py` | `gate_passed()`: pure Python YAML/regex validation | NONE — format-agnostic |
| `models.py` | `Step`, `PipelineConfig`, `GateCriteria` | NONE — format-agnostic |
| `deliverables.py` | Classifies/decomposes deliverables from roadmap text | NONE — roadmap-only |

### Reference files (do not re-audit; use as context)

| File | Purpose |
|------|---------|
| `src/superclaude/examples/tdd_template.md` | TDD format: 28 sections, 27 frontmatter fields — the target input |
| `.dev/releases/current/tdd-spec-analysis/RESEARCH-REPORT-prd-tdd-spec-pipeline.md` | Prior research: skills/commands layer findings [CODE-VERIFIED]; treat as authoritative |

---

## PATTERNS_AND_CONVENTIONS

**Verified from direct source reading:**

1. **Spec file flows as embedded inline content** — `_embed_inputs([spec_file])` wraps file content in fenced code blocks and appends to prompt string. The `spec_file` path object is preserved separately for Python functions that read it directly.

2. **Two types of spec access**:
   - *LLM-mediated*: spec content embedded in prompt → Claude reads it via inference
   - *Programmatic*: Python functions read spec file directly — `_run_anti_instinct_audit()`, `_run_structural_audit()`, `fidelity_checker.py`, `spec_parser.py`

3. **Pure Python analysis modules** — `obligation_scanner`, `integration_contracts`, `fingerprint`, `spec_structural_audit` are all pure functions (no subprocess, no LLM). Content in, findings out. All invoked by executor as post-step hooks.

4. **Anti-instinct audit is 100% programmatic** — `_run_anti_instinct_audit(spec_file, roadmap_file, output_file)` calls 3 modules:
   - `scan_obligations(roadmap_text)` — scans roadmap, not spec
   - `extract_integration_contracts(spec_text)` + `check_roadmap_coverage(contracts, roadmap_text)` — extracts from spec, checks in roadmap
   - `check_fingerprint_coverage(spec_text, roadmap_text)` — extracts identifiers from spec, checks in roadmap

5. **`fingerprint.py` is format-agnostic** — extracts identifiers via: (a) backtick-delimited names ≥4 chars, (b) code-block function/class defs, (c) ALL_CAPS constants ≥4 chars. TDD has MORE of all three (TypeScript interfaces in backticks, code blocks, API method names) — so TDD input would produce MORE fingerprints and potentially different coverage ratios than spec input.

6. **`integration_contracts.py` is format-agnostic** — 7-category regex scanner for dispatch patterns: dict dispatch tables, plugin registries, callback injection, strategy pattern, middleware chains, event binding, inversion-of-control. These are found in code-heavy specs AND in TDD §6 Architecture and §8 API Specifications.

7. **`spec_parser.py` extracts from ANY markdown** — Produces YAML frontmatter, markdown tables, fenced code blocks, requirement IDs (FR-NNN pattern), function signatures from fenced blocks, numeric thresholds, file paths. TDD §5 Technical Requirements uses FR-xxx IDs. TDD §7-§8 have TypeScript interfaces in code blocks. TDD YAML frontmatter has 27 fields (different schema than spec template). All of this is parseable by `spec_parser.py` — but the **output schema mismatch** (TDD frontmatter vs. spec frontmatter field names) may cause downstream issues.

8. **`build_extract_prompt()` is the single chokepoint** — The generate step only receives the extraction output (not the spec file). If TDD sections §7, §8, §10, §14, §15, §19, §25 are not captured in extraction.md, they are permanently lost to all downstream steps.

9. **`spec_source` field injected by Python** — `_inject_provenance_fields()` injects `spec_source: <filename>` into test-strategy frontmatter. For TDD input, this would correctly inject the TDD filename.

10. **Validate pipeline does not read the spec** — `validate_executor.py` inputs: `_REQUIRED_INPUTS = ("roadmap.md", "test-strategy.md", "extraction.md")`. The spec/TDD file is NOT an input to the validate pipeline.

11. **CLI tasklist has NO `--spec` flag** — `tasklist/commands.py` validate command signature: `output_dir`, `--roadmap-file`, `--tasklist-dir`, `--model`, `--max-turns`, `--debug`. No spec-file parameter at any level.

---

## SOLUTION_RESEARCH

The user wants an implementation plan. Three approaches emerged from scope discovery:

**Option A: Dual extract prompt (spec vs. TDD modes)**
Add `--input-type [spec|tdd]` flag to `roadmap/commands.py`. In `executor.py`, branch based on input type: call `build_extract_prompt()` for spec or new `build_extract_prompt_tdd()` for TDD. New TDD prompt instructs Claude to produce the 8-section extraction body with TDD-specific additions (§7 data models as structured requirements, §8 API specs as API requirement items, §10 component inventory as task generation hints, §15 testing strategy as NFR test requirements, §19 migration as rollout phase requirements, §25 ops readiness as operational requirements). Update `build_spec_fidelity_prompt()` to reference TDD-specific sections. Minimal disruption to existing pipeline.

**Option B: Auto-detect TDD format**
In `executor.py`, detect TDD format by reading YAML frontmatter `type` field (TDD template has `type: "📐 Technical Design Document"`). Branch automatically without a flag. Same prompt changes as Option A. Risk: fragile if TDD frontmatter is incomplete or type field differs.

**Option C: TDD → extraction pre-processor**
Add a new `pre-extract` step that programmatically parses TDD sections using `spec_parser.py` (which can already read TDD tables and code blocks) and generates a richer intermediate representation before the LLM extraction step. This uses `spec_parser.py`'s table extraction to get structured data from §7, §8, §10 directly as Python objects, then formats them for the extraction prompt. Highest accuracy for structured TDD content; most complex.

All three options must also address:
- Pure Python modules: `integration_contracts.py` and `fingerprint.py` work on spec_text; TDD text works but produces different (potentially better) results — should be tested but not changed
- `build_anti_instinct_prompt()`: the ANTI_INSTINCT_GATE checks frontmatter fields produced by the anti-instinct LLM step — need to verify what inputs this gets
- `spec_structural_audit.py`: warning-only; needs to know about TDD structural indicators (§5 section headings count differently from spec `### FR-NNN` headings)

---

## RECOMMENDED_OUTPUTS

| File | Purpose |
|------|---------|
| `research/01-executor-data-flow.md` | Full executor data flow: which steps get spec_file, which get extraction, step-by-step spec_file consumption |
| `research/02-prompt-language-audit.md` | All prompt builders: spec-language assumptions, required changes for TDD, domain keyword gap |
| `research/03-pure-python-modules.md` | spec_parser, fidelity_checker, integration_contracts, fingerprint, obligation_scanner, spec_structural_audit — TDD compatibility analysis |
| `research/04-gate-compatibility.md` | All 14 gates: field requirements, semantic checks, TDD-compatibility verdict for each |
| `research/05-cli-entry-points.md` | roadmap/commands.py, tasklist/commands.py — existing flags, missing flags, extension points |
| `research/06-tdd-template-structure.md` | tdd_template.md sections vs. extraction capture map; what content is capturable with current vs. improved extraction |
| `synthesis/synth-01-problem-current-state.md` | §1 Problem Statement, §2 Current State Analysis |
| `synthesis/synth-02-target-gaps.md` | §3 Target State, §4 Gap Analysis |
| `synthesis/synth-03-external-findings.md` | §5 External Research Findings (N/A — codebase-scoped) |
| `synthesis/synth-04-options-recommendation.md` | §6 Options Analysis, §7 Recommendation |
| `synthesis/synth-05-implementation-plan.md` | §8 Implementation Plan |
| `synthesis/synth-06-questions-evidence.md` | §9 Open Questions, §10 Evidence Trail |
| `RESEARCH-REPORT-cli-tdd-integration.md` | Final assembled report |

---

## SUGGESTED_PHASES

### Phase 2 Research Agents (spawn in parallel — all 6)

**Agent 1 — Executor Data Flow Tracer (Code Tracer)**
- Topic: How `spec_file` flows through all 14 pipeline steps in `executor.py`
- Files: `src/superclaude/cli/roadmap/executor.py` (full file), `src/superclaude/cli/roadmap/spec_structural_audit.py`
- Key questions: Which `_build_*` functions embed spec_file as input? Which steps get extraction output only? What Python functions read spec_file directly (not via subprocess)? What does `_run_anti_instinct_audit` call sequence look like? What does the spec-fidelity step's `build_spec_fidelity_prompt()` receive?
- Output: `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/01-executor-data-flow.md`

**Agent 2 — Prompt Language Auditor (Code Tracer)**
- Topic: All prompt builders in roadmap/prompts.py — spec-language assumptions and required TDD changes
- Files: `src/superclaude/cli/roadmap/prompts.py` (full file)
- Key questions: Full text of `build_extract_prompt()` — what spec-specific language exists? What are the 8 body sections? What TDD sections are missing? Full text of `build_spec_fidelity_prompt()` — does it reference spec-specific fields? Full text of `build_wiring_verification_prompt()`, `build_anti_instinct_prompt()`, `build_generate_prompt()`, `build_test_strategy_prompt()`. For each: what must change to handle TDD input?
- Output: `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/02-prompt-language-audit.md`

**Agent 3 — Pure Python Analysis Modules (Code Tracer + Integration Mapper)**
- Topic: The 5 pure-Python analysis modules that process spec text programmatically
- Files: `src/superclaude/cli/roadmap/spec_parser.py` (full), `src/superclaude/cli/roadmap/fidelity_checker.py` (full), `src/superclaude/cli/roadmap/integration_contracts.py` (full), `src/superclaude/cli/roadmap/fingerprint.py` (full), `src/superclaude/cli/roadmap/obligation_scanner.py` (full)
- Key questions: Does `spec_parser.py` work correctly on TDD YAML frontmatter (27 fields, different field names)? Does `fidelity_checker.py` work with TDD FR format (§5 Technical Requirements uses FR-xxx IDs)? Does `integration_contracts.py` find dispatch patterns in TDD §6 Architecture + §8 API content? Does `fingerprint.py` produce meaningful coverage from TDD TypeScript interface names + code blocks? What changes (if any) are needed to each module for TDD compatibility?
- Output: `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/03-pure-python-modules.md`

**Agent 4 — Gate Compatibility Analyzer (Architecture Analyst)**
- Topic: TDD compatibility of all 14 gate definitions
- Files: `src/superclaude/cli/roadmap/gates.py` (full), `src/superclaude/cli/pipeline/gates.py` (full), `src/superclaude/cli/tasklist/gates.py` (full)
- Key questions: For each gate (EXTRACT, GENERATE_A/B, DIFF, DEBATE, SCORE, MERGE, ANTI_INSTINCT, TEST_STRATEGY, SPEC_FIDELITY, WIRING, DEVIATION_ANALYSIS, REMEDIATE, CERTIFY, TASKLIST_FIDELITY): what YAML fields are required? What semantic checks run? Would a Claude subprocess given TDD content produce these fields correctly? Does any gate have spec-format-specific assumptions that would fail on TDD input?
- Output: `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/04-gate-compatibility.md`

**Agent 5 — CLI Entry Points & Tasklist (Integration Mapper)**
- Topic: CLI extension points for TDD input at roadmap and tasklist levels
- Files: `src/superclaude/cli/roadmap/commands.py` (full), `src/superclaude/cli/tasklist/commands.py` (full), `src/superclaude/cli/roadmap/models.py` (full), `src/superclaude/cli/tasklist/models.py` (full)
- Key questions: Full signature of `superclaude roadmap run` — all flags; what would `--input-type [spec|tdd]` look like? Where in commands.py would TDD detection logic go? Full signature of `superclaude tasklist validate` — confirm no `--spec` flag exists; where would it go? What `RoadmapConfig`/`TasklistValidateConfig` model changes are needed to carry `input_type` and `tdd_file` through the pipeline? Are there any existing hooks for future extension?
- Output: `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/05-cli-entry-points.md`

**Agent 6 — TDD Template Structure Analyzer (Doc Analyst)**
- Topic: TDD sections vs. current CLI extraction capture — what's captured, what's missed, what format each section uses
- Files: `src/superclaude/examples/tdd_template.md` (full), prior research report for context: `.dev/releases/current/tdd-spec-analysis/RESEARCH-REPORT-prd-tdd-spec-pipeline.md` (sections 2.4 and 2.2 TDD Section Capture Analysis)
- Key questions: For each of the 28 TDD sections: what content format is used (behavioral "shall" statements? TypeScript interfaces? Endpoint tables? Rollout phase tables?)? Which sections would be fully captured by the current extract prompt? Which are missed? For the missed sections (§7, §8, §10, §14, §15, §19, §25) — what specific extraction instruction would the TDD extract prompt need to capture them? Cross-validate TDD §5 FR format against spec FR format — are they compatible with `spec_parser.py` extraction?
- Output: `.dev/tasks/to-do/TASK-RESEARCH-20260325-001/research/06-tdd-template-structure.md`

### Phase 4 Web Research (no web research needed)
N/A — this is a pure codebase investigation. No external research required. Phase 4 will be skipped.

### Phase 5 Synthesis Mapping

| Synth File | Report Sections | Source Research Files |
|------------|----------------|----------------------|
| `synth-01-problem-current-state.md` | §1 Problem Statement, §2 Current State Analysis | 01, 02, 03, 04, 05, 06 |
| `synth-02-target-gaps.md` | §3 Target State, §4 Gap Analysis | 01, 02, 03, 04, 05, 06, gaps log |
| `synth-03-external-findings.md` | §5 External Research Findings (mark N/A) | None |
| `synth-04-options-recommendation.md` | §6 Options Analysis, §7 Recommendation | 01, 02, 03, 04, 05, 06, gaps log |
| `synth-05-implementation-plan.md` | §8 Implementation Plan | 01, 02, 03, 04, 05, 06 |
| `synth-06-questions-evidence.md` | §9 Open Questions, §10 Evidence Trail | all gaps, all research file paths |

---

## TEMPLATE_NOTES

Template 02 (Complex Task). This investigation requires parallel subagent spawning (6 research agents), multi-phase workflow (research → analyst/QA gate → synthesis → assembly → validation), and conditional flows (gap-filling if QA fails). Template 01 is not appropriate.

Note: The MDTM templates referenced (`.gfdoc/templates/`) are from the GFxAI project and will not exist in IronClaude. The rf-task-builder should use the template content from the tech-research skill's BUILD_REQUEST directly, or use any available MDTM template in the project. If no template is found, the builder should construct the task file from the structure specified in the BUILD_REQUEST.

---

## AMBIGUITIES_FOR_USER

None — intent is clear from the research prompt and codebase scope discovery.

The following are open questions for the research itself (not user ambiguities):
- `spec_structural_audit.py` has not been fully read — agents must read it to understand what structural indicators it counts and whether TDD structure is compatible
- `build_anti_instinct_prompt()` — the actual LLM step for ANTI_INSTINCT_GATE was not confirmed in scope discovery; need to verify if it also receives spec_file or only the anti-instinct-audit.md produced by `_run_anti_instinct_audit()`
- `semantic_layer.py` — partially read; unclear exactly how it reads spec content or if it's invoked in the current pipeline
