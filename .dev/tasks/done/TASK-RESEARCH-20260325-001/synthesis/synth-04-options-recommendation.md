---
synthesis_id: synth-04
title: "Options Analysis and Recommendation — TDD CLI Integration"
sections: ["§6 Options Analysis", "§7 Recommendation"]
source_research:
  - research/01-executor-data-flow.md
  - research/02-prompt-language-audit.md
  - research/03-pure-python-modules.md
  - research/04-gate-compatibility.md
  - research/05-cli-entry-points.md
  - research/06-tdd-template-structure.md
  - gaps-and-questions.md
date: 2026-03-25
status: complete
---

# §6 Options Analysis — TDD CLI Integration

## Framing

Three structurally distinct approaches were identified in scope discovery. All three must address the same two Critical findings from the research:

1. **Extract chokepoint** — `build_extract_prompt()` is the single point of failure. All downstream steps (`generate-*`, `diff`, `debate`, `score`, `merge`, `test-strategy`) receive only extraction output, never the original TDD file. Any TDD content not surfaced at extract time is unrecoverable. (Sources: `01-executor-data-flow.md` §b, `02-prompt-language-audit.md` §build_extract_prompt)

2. **DEVIATION_ANALYSIS_GATE structural incompatibility** — The only gate with hard structural incompatibility: `routing_update_spec` is explicitly spec-specific; `DEV-\d+` ID namespace assumes spec-deviation taxonomy. (Source: `04-gate-compatibility.md` §DEVIATION_ANALYSIS_GATE)

A third HIGH-severity finding is relevant but affects all three options equally:

3. **`spec_source` field name** — Appears in 5 gates (EXTRACT, GENERATE_A, GENERATE_B, MERGE, TEST_STRATEGY) and at least 2 prompt builders. If TDD-mode LLM outputs still emit `spec_source` (using the TDD filename), these gates can pass without field renaming. Aliasing is optional but semantically desirable. (Source: `04-gate-compatibility.md` Summary)

---

## Option A: Dual Extract Prompt (Explicit `--input-type` Flag)

### Description

Add `--input-type [spec|tdd]` as a Click option to `roadmap/commands.py`. Add `input_type: Literal["spec","tdd"] = "spec"` to `RoadmapConfig`. In `executor.py`, branch on `config.input_type`: call `build_extract_prompt()` for spec mode or a new `build_extract_prompt_tdd()` for TDD mode. The TDD prompt adds dedicated extraction sections for 8 missed TDD content areas (§7 Data Models, §8 API Specs, §9 State Management, §10 Component Inventory, §15 Testing Strategy, §25 Operational Readiness, §26 Cost Estimation, §28 Glossary). Update `build_spec_fidelity_prompt()` to add TDD comparison dimensions. Alias or update `spec_source` in 5 gates and 2 prompt builders. Redesign `DEVIATION_ANALYSIS_GATE` to replace `routing_update_spec` with `routing_update_source`.

### Assessment

| Aspect | Assessment |
|--------|-----------|
| Effort | M |
| Risk | Low |
| Backward compatible? | Yes — `--input-type` defaults to `"spec"`; all existing invocations unchanged |
| Files affected | `roadmap/commands.py`, `roadmap/models.py`, `roadmap/executor.py`, `roadmap/prompts.py` (2 functions), `roadmap/gates.py` (DEVIATION_ANALYSIS_GATE + 5 gates for `spec_source` alias) |
| Pros | - User intent is explicit and unambiguous; no parsing risk<br>- Follows established extension pattern: `convergence_enabled` and `allow_regeneration` were added as defaulted fields in the same model (confirmed: `05-cli-entry-points.md` §RoadmapConfig)<br>- TDD prompt fully decoupled from spec prompt — no risk of spec regression<br>- `spec_source` aliasing can be phased: gates will pass if LLM still emits `spec_source` with TDD filename, so aliasing is low-priority<br>- Clean branch point in `_build_steps()` that executor already visits |
| Cons | - Requires user to know and pass `--input-type tdd`; no auto-discovery<br>- `spec_file` positional argument name remains semantically awkward for TDD inputs (confirmed: `05-cli-entry-points.md` Gaps §2)<br>- Two prompt functions to maintain in parallel; drift risk if spec prompt evolves and TDD prompt is not updated |

---

## Option B: Auto-Detect TDD from Frontmatter

### Description

No new CLI flag. The executor reads the YAML `type` field from the input file before building the extract prompt. If `type == "📐 Technical Design Document"` (the exact value in the TDD template frontmatter), executor switches to TDD mode. All prompt and gate changes are identical to Option A, but the branch is triggered automatically rather than by user flag.

### Assessment

| Aspect | Assessment |
|--------|-----------|
| Effort | M |
| Risk | Medium — fragile detection dependency |
| Backward compatible? | Conditional — existing spec files without a `type` field default to spec mode; spec files with a `type` field that doesn't match the exact TDD string also default to spec mode. Spec regression only if a spec file accidentally contains `type: "📐 Technical Design Document"` |
| Files affected | Same as Option A, plus: `executor.py` needs a pre-step frontmatter read routine; `spec_parser.py` `parse_frontmatter()` is called before any step runs |
| Pros | - Zero user-facing change; no flag to document or explain<br>- TDD template frontmatter has the `type` field confirmed: `type: "📐 Technical Design Document"` (confirmed: `06-tdd-template-structure.md` §c)<br>- `spec_parser.parse_frontmatter()` is generic and will extract TDD frontmatter fields correctly (confirmed: `03-pure-python-modules.md` §spec_parser) |
| Cons | - Detection depends on exact frontmatter value including the emoji; fragile to TDD documents that omit or vary the `type` field<br>- TDD files created outside the template (or edited to remove frontmatter) would silently fall back to spec mode — producing a poor extraction with no error<br>- Silent failure mode: user running on a TDD with missing frontmatter would get spec-mode extraction and not know why output is incomplete<br>- Adds a file-read side-effect at pipeline startup before any step executes; slightly violates the step-driven execution model<br>- The `type` field contains an emoji (`📐`) — YAML parsing and string comparison edge cases possible across different YAML library versions |

---

## Option C: TDD Pre-Processor Step Using `spec_parser.py`

### Description

Add a new `pre-extract` pipeline step before the LLM extract step. This step uses `spec_parser.py` to programmatically parse TDD sections: `extract_tables()` captures endpoint overview tables and field tables; `extract_code_blocks()` captures TypeScript interfaces; `split_into_sections()` isolates §7, §8, §9, §10, §15, §25 by heading. The pre-processor generates a structured intermediate representation (IR) document that is then fed into the extract prompt alongside or in place of the raw TDD file. This IR enriches the extract prompt with structured, pre-parsed artifacts.

### Assessment

| Aspect | Assessment |
|--------|-----------|
| Effort | XL |
| Risk | High |
| Backward compatible? | Conditional — requires adding a new step to `_build_steps()` gated on `input_type`; pipeline step count changes; gate configuration must account for new step output |
| Files affected | `executor.py` (`_build_steps()` + new `_run_tdd_preprocessor()` function + step dispatch in `roadmap_run_step()`), `prompts.py` (extract prompt update to consume IR), new file `tdd_preprocessor.py`, `roadmap/commands.py`, `roadmap/models.py`, `roadmap/gates.py`, potentially `pipeline/gates.py` for new gate |
| Pros | - Highest potential accuracy for structured TDD content: TypeScript interfaces from `extract_code_blocks()` and endpoint tables from `extract_tables()` are captured deterministically before LLM sees the document<br>- Programmatic extraction is reproducible and testable<br>- Leverages existing `spec_parser.py` modules that are confirmed TDD-compatible for tables and code blocks (confirmed: `03-pure-python-modules.md` §spec_parser)<br>- Intermediate IR document is a concrete artifact that can be diffed and validated independently of LLM output |
| Cons | - `spec_parser.py` has critical gaps for TDD: `extract_function_signatures()` only parses Python `def/class` — TypeScript `interface Foo {}` is NOT extracted into `function_signatures` (confirmed: `03-pure-python-modules.md` §TypeScript interface extraction); endpoint paths do not match the backtick identifier regex (confirmed: `03-pure-python-modules.md` §fingerprint); requires new TypeScript interface parser or workaround<br>- The IR generation logic is speculative: which sections produce useful IR vs. noise is not verified against real TDD documents<br>- High implementation surface: new module + new pipeline step + new step dispatch + prompt changes + potentially new gate<br>- `split_into_sections()` uses `DIMENSION_SECTION_MAP` which encodes spec-oriented headings — may not map to TDD section headings without adaptation (confirmed: `03-pure-python-modules.md` §Schema mismatch risks)<br>- Two additional unknowns from gaps-and-questions.md (C-1, C-2): `semantic_layer.py` and `structural_checkers.py` are unverified — adding a pre-processor step before verifying these modules carries integration risk |

---

## §6.4 Cross-Option Comparison Table

| Dimension | Option A (Explicit Flag) | Option B (Auto-Detect) | Option C (Pre-Processor) |
|-----------|--------------------------|------------------------|--------------------------|
| Effort | M | M | XL |
| Risk | Low | Medium | High |
| Backward compatible? | Yes (default="spec") | Conditional (fragile detection) | Conditional (new step) |
| User experience | Explicit flag required | Transparent, no flag | Explicit flag required (or auto-detect) |
| Addresses extract chokepoint? | Yes — via `build_extract_prompt_tdd()` with 6+ new sections | Yes — same prompt changes | Partially — programmatic IR helps; TS interface gap remains |
| Addresses DEVIATION_ANALYSIS_GATE? | Yes — redesign `routing_update_spec` → `routing_update_source` | Yes — same gate changes | Yes — same gate changes |
| New files required | None | None | `tdd_preprocessor.py` (new module) |
| Files modified | 4 | 4 + executor startup read | 6+ |
| Silent failure mode? | No — unknown flag is a Click error | Yes — missing frontmatter falls back to spec mode silently | No — explicit mode |
| Dependency on `spec_parser.py` correctness | None | `parse_frontmatter()` only (low-risk) | Heavy — tables, code blocks, section splitting (medium-risk) |
| Matches established extension pattern? | Yes — additive defaulted field + Click option (confirmed: `05-cli-entry-points.md`) | Partial — frontmatter pre-read is novel pattern | No — new pipeline step type |
| TypeScript interface extraction? | LLM-driven (prompt instruction) | LLM-driven (prompt instruction) | Partial programmatic; TS parser absent |
| Verifiable/testable incrementally? | Yes — spec path unchanged; TDD path testable in isolation | Harder — detection logic is implicit | Harder — IR correctness requires TDD test fixtures |

---

# §7 Recommendation — TDD CLI Integration


## Recommended Option: Option A — Dual Extract Prompt with Explicit `--input-type` Flag

### Summary Verdict

Option A has the most favorable risk/effort/compatibility tradeoff. It addresses both Critical findings directly, follows the project's established extension pattern, and does not introduce fragile detection logic or unverified module dependencies.

---

### Rationale by Evaluation Criterion

#### 1. Risk/Effort/Compatibility Tradeoff

Option A is rated Low risk and M effort with confirmed backward compatibility. The backward-compatibility guarantee is not a design aspiration — it follows directly from the established pattern. `RoadmapConfig` has two prior examples of additive defaulted fields added for backward compatibility: `convergence_enabled: bool = False` and `allow_regeneration: bool = False` (confirmed: `05-cli-entry-points.md` §Existing backward-compatible extension pattern). Adding `input_type: Literal["spec","tdd"] = "spec"` uses the identical pattern.

Option B shares the same effort level but introduces Medium risk via the fragile detection dependency. The TDD frontmatter `type` field value is `"📐 Technical Design Document"` — an exact string match including a Unicode emoji (confirmed: `06-tdd-template-structure.md` §c). Documents that omit this field, use a different value, or are authored outside the template produce silent fallback to spec-mode extraction with no user-visible error. Silent failure in the extract step is particularly severe because extract is the single chokepoint — the resulting spec-mode extraction of a TDD document would propagate incomplete content through all downstream steps without any gate catching the failure mode.

Option C is rated XL effort and High risk. The high effort comes from: a new module (`tdd_preprocessor.py`), a new pipeline step type, new dispatch logic in `roadmap_run_step()`, and a new gate — all for a pre-processing step whose IR accuracy against real TDD documents is unverified. The high risk comes from two confirmed capability gaps: `extract_function_signatures()` does not parse TypeScript interfaces (confirmed: `03-pure-python-modules.md`), and endpoint URL paths do not match the identifier regex used by `fingerprint.py` (confirmed: `03-pure-python-modules.md`). Additionally, two uninvestigated modules (`semantic_layer.py` and `structural_checkers.py`) are flagged as Critical unknowns (confirmed: `gaps-and-questions.md` C-1, C-2) — adding a new pipeline step before these modules are understood carries integration risk that is unquantifiable from current research.

#### 2. Addressing the Extract Chokepoint

All three options require a new or updated extract prompt with TDD-specific sections. The research identified 8 MISSED TDD sections and 15 PARTIAL sections in the current prompt (confirmed: `06-tdd-template-structure.md` §Counts). For Options A and B, LLM-driven extraction with explicit section instructions is the mechanism. This is the same mechanism used for spec content today, and it is validated by the current pipeline design — the generate steps (`generate-{agent_a.id}`, `generate-{agent_b.id}`) receive ONLY the extraction output, making extract the single content gatekeeper (confirmed: `01-executor-data-flow.md` §b).

Option C's programmatic pre-processing would add deterministic accuracy for tabular content (`extract_tables()` for endpoint tables, `extract_code_blocks()` for TypeScript blocks) but the TypeScript interface semantic gap means interfaces would not be structurally parsed — only captured as raw code block text. For the purposes of the extraction chokepoint, a well-instructed LLM prompt (Option A/B approach) is more likely to produce complete semantic extraction from TypeScript interfaces than a Python parser with no TypeScript AST support.

The decisive evidence: `build_generate_prompt()` references specific extraction frontmatter fields by name (`functional_requirements`, `nonfunctional_requirements`, `total_requirements`, `complexity_score`, etc.) — confirmed at `02-prompt-language-audit.md` §build_generate_prompt. Option A adds TDD-specific count fields to the extraction frontmatter schema (`data_models_identified`, `api_surfaces_identified`, etc.) — these new fields then become available to `build_generate_prompt()` for TDD-aware roadmap generation. This chain works cleanly in Option A and equally in Option B, but requires additional IR-to-frontmatter mapping work in Option C.

#### 3. Addressing DEVIATION_ANALYSIS_GATE

This gate requires `routing_update_spec` — a field that is explicitly spec-specific and has no TDD analog — plus a `DEV-\d+` ID namespace that assumes spec-deviation tracking taxonomy (confirmed: `04-gate-compatibility.md` §DEVIATION_ANALYSIS_GATE). The gate also has a confirmed pre-existing bug: required field `ambiguous_count` while the semantic check reads `ambiguous_deviations` (confirmed: `gaps-and-questions.md` §Pre-Existing Codebase Bug). All three options require the same gate redesign: replace `routing_update_spec` with `routing_update_source`, reconsider the `DEV-\d+` pattern, and resolve the `ambiguous_count`/`ambiguous_deviations` mismatch. The pre-existing bug fix is a no-extra-cost bundled correction for whichever option is implemented.

This gate is the only gate with hard structural incompatibility — all other gates are either already TDD-compatible (DIFF, DEBATE, SCORE, WIRING, REMEDIATE) or conditionally compatible pending `spec_source` aliasing (confirmed: `04-gate-compatibility.md` Summary). This means gate remediation scope is contained and identical across all three options.

#### 4. Incremental Implementability

Option A can be implemented and tested in stages:
- Stage 1: Add `--input-type` flag + `input_type` field to `RoadmapConfig` — zero behavioral change, spec path untouched
- Stage 2: Implement `build_extract_prompt_tdd()` in `prompts.py` — testable independently against TDD fixture files
- Stage 3: Add branch in `executor.py` `_build_steps()` — narrow, single-location change at executor.py:809-820
- Stage 4: Update `build_spec_fidelity_prompt()` for TDD comparison dimensions
- Stage 5: Redesign DEVIATION_ANALYSIS_GATE

At no stage does the spec code path change until Stage 3, and even then only via a conditional branch. This incremental structure means regression risk to existing spec workflows is effectively zero.

---

### Constraints and Open Questions That Do Not Change the Recommendation

The following gaps from `gaps-and-questions.md` are noted but do not affect the Option A recommendation:

- **C-1, C-2** (`semantic_layer.py`, `structural_checkers.py`): These modules are uninvestigated but appear only as optional enrichment or validation passes. Option A's approach (LLM-driven extraction) is not dependent on either module for the extract step. If either module reads `spec_source` or similar fields, the aliasing work already in Option A's scope covers that.

- **I-3** (`spec_source` rename strategy): Because 5 gates check for `spec_source` by name, and a TDD-mode LLM can still emit `spec_source: <tdd_filename>` without any rename, the aliasing can be deferred to a follow-on task. The functional gates will pass. Renaming to `source_document` is a semantic improvement but not a gating requirement.

- **I-5** (ANTI_INSTINCT_GATE TDD performance hypothesis): The hypothesis is that TDD inputs produce more backtick-extractable identifiers than spec inputs, potentially improving `fingerprint_coverage` above the 0.7 threshold (confirmed: `03-pure-python-modules.md` §fingerprint). This is unverified but the failure direction is favorable — TDD might pass ANTI_INSTINCT_GATE more easily than spec, not less. This does not create a blocker.

---

### Implementation Priority Order (for Option A)

Based on severity ratings from the research:

| Priority | Change | Research Severity | Rationale |
|----------|--------|-------------------|-----------|
| 1 | `build_extract_prompt_tdd()` with TDD-specific sections | Critical | Single chokepoint; all downstream steps depend on it |
| 2 | DEVIATION_ANALYSIS_GATE redesign (`routing_update_spec` to `routing_update_source`) | Required | Only structurally incompatible gate; blocks TDD pipeline completion |
| 3 | `build_spec_fidelity_prompt()` generalization | High | Receives spec_file directly; current language is spec-bound |
| 4 | `build_generate_prompt()` TDD frontmatter field consumption | High | Inherits extract chokepoint; downstream of Priority 1 |
| 5 | `spec_source` aliasing in 5 gates | Important | Semantically desirable; functionally deferrable |
| 6 | `build_test_strategy_prompt()` TDD enrichment | Medium | Strengthens test derivation from TDD artifacts; not blocking |
| 7 | ANTI_INSTINCT_GATE failure message generalization | Low | "spec code-level identifiers" wording is inaccurate for TDD; functional gate behavior unaffected |
