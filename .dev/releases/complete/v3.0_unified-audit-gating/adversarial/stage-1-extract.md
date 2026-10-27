---
stage: 1
stage_name: extract
depth: quick
gate: EXTRACT_GATE
verdict: ADEQUATE
---

# Stage 1: extract -- Adversarial Review

## Q1: Meaningful Output

The eval spec will produce meaningful output at this stage. The spec is a well-formed MEDIUM-complexity feature specification with 6 functional requirements, 3 NFRs, risk tables, dependency references, and two seeded ambiguities. This gives the extraction prompt substantive material to work with across all 8 required body sections (Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions).

The EXTRACT_GATE will not trivially pass or fail. The gate requires 13 frontmatter fields including `complexity_score`, `complexity_class`, `extraction_mode`, and counts for functional/nonfunctional requirements. These are all derivable from the eval spec content -- `complexity_class` should resolve to MEDIUM (matching the spec's own `complexity_class: MEDIUM`), and the requirement counts are enumerable (6 FR, 3 NFR). The two semantic checks (`complexity_class_valid`, `extraction_mode_valid`) are pass-by-construction for any well-formed LLM output that follows the prompt instructions, which specify exactly which values are valid.

**Risk of trivial pass**: moderate. The semantic checks only validate enum membership (LOW/MEDIUM/HIGH for complexity_class, standard/chunked for extraction_mode). They do not validate that the extracted complexity_class *matches* the spec's self-declared complexity_class. An extractor that emits `complexity_class: HIGH` for a MEDIUM spec would still pass the gate. This is a known limitation of structural gates -- semantic accuracy is not verified until spec-fidelity (stage 9+).

## Q2: v3.0 Changes

Stages 1-3 are structurally unchanged in v3.0. The EXTRACT_GATE definition, the `build_extract_prompt()` function, and the step wiring in `_build_steps()` are identical between master and v3.0 for this stage.

However, v3.0 introduces two indirect changes that affect this stage's behavior:

1. **Prompt enhancement**: `build_extract_prompt()` now accepts an optional `retrospective_content` parameter. If a retrospective file is provided via `RoadmapConfig.retrospective_file`, the extraction prompt includes advisory context framed as "areas to watch." For the eval spec, no retrospective is expected, so this code path is inert -- but it changes the function signature and the prompt builder's branching logic.

2. **Output sanitization**: v3.0 adds `_sanitize_output()` which strips conversational preamble before YAML frontmatter. This runs on all step outputs including extract. On master, LLM preamble before `---` would cause frontmatter parsing to fail (the gate's `_parse_frontmatter()` requires content to start with `---`). In v3.0, sanitization rescues outputs that would otherwise fail the gate. This is a meaningful behavioral change: the extract gate's effective pass rate is higher in v3.0 than on master.

3. **Embed size limit change**: v3.0 recalculates `_EMBED_SIZE_LIMIT` from kernel constants (128KB - 8KB overhead = ~120KB) vs. master's flat 100KB. For the eval spec (~8KB), this is irrelevant -- both limits accommodate the input. But the change exists in the executor code path that feeds stage 1.

## Q3: Artifact Verification

**Artifact**: `{output_dir}/extraction.md`

A third party can verify quality through the following checks:

| Check | Method | Automated? |
|-------|--------|------------|
| Frontmatter completeness | Parse YAML, verify all 13 required fields present | Yes (gate does this) |
| complexity_class validity | Check value in {LOW, MEDIUM, HIGH} | Yes (semantic check) |
| extraction_mode validity | Check value is "standard" or starts with "chunked" | Yes (semantic check) |
| Requirement count accuracy | Count FR-NNN and NFR-NNN IDs in body, compare to frontmatter integers | Manual (gate does not cross-validate) |
| Complexity score reasonableness | Verify 0.45 +/- tolerance matches spec's self-declared score | Manual |
| Section completeness | Verify all 8 sections exist with non-empty content | Manual (gate only checks min_lines=50) |
| Seeded ambiguity detection | Verify Open Questions section flags FR-EVAL-001.4 and FR-EVAL-001.5 | Manual |

The min_lines=50 threshold is easily met by any extraction of a spec with 6 FRs and 3 NFRs. It provides crash-detection (empty/truncated output) but not quality assurance.

## Q4: Most Likely Failure Mode

**Frontmatter field omission or misnaming.** The extract prompt lists all 13 required fields, but LLMs occasionally rename fields (e.g., `extraction_type` instead of `extraction_mode`, `risk_count` instead of `risks_identified`). The EXTRACT_GATE checks field presence by exact key name. A single misnaming fails the gate.

This is the most likely failure because:
- The prompt specifies 13 fields by name, which is a high count for LLM instruction-following fidelity
- YAML key names are not validated for close-match/typo (strict string equality)
- The `_OUTPUT_FORMAT_BLOCK` appended to the prompt adds formatting instructions but does not reinforce field names

The second most likely failure is frontmatter parsing failure due to malformed YAML (e.g., unquoted colons in values, list syntax that `_parse_frontmatter()` cannot handle since it uses naive `split(":", 1)` parsing).

## Q5: Eval Spec Coverage

v3.0 does not change the extract stage's gate criteria or prompt structure. The eval spec does not need to exercise any new extract-stage behavior because there is no new behavior.

However, the eval spec should be aware of two indirect effects:

1. **Output sanitization rescue**: If the eval is testing gate rejection scenarios, v3.0's `_sanitize_output()` will rescue outputs that master would reject. The eval spec does not account for this because it is focused on progress reporting, not gate behavior. This is acceptable -- the eval spec is not testing gate mechanics.

2. **Retrospective parameter**: The eval spec does not mention retrospective content. This means the `retrospective_content=None` code path is exercised (default). The `retrospective_content` branch is untested by this eval. This is acceptable for a progress-reporting eval but would be a gap in a gate-coverage eval.

3. **Seeded ambiguities are downstream-targeted**: The eval spec's two seeded ambiguities (FR-EVAL-001.4 schema omission, FR-EVAL-001.5 "significant findings") are designed to trigger findings in spec-fidelity (stage 9+), not in extract. A good extraction *should* flag these in its Open Questions section, but the extract gate does not verify Open Questions content. The eval spec correctly treats these as downstream triggers, not extract-stage concerns.

**Coverage assessment**: The eval spec adequately exercises stage 1 for its stated purpose (progress reporting). It does not claim to be a gate-coverage eval, and the extract stage's behavior is unchanged in v3.0.

## Verdict

**ADEQUATE.** The eval spec produces a well-formed input for stage 1, the gate criteria are meaningful (not trivially pass/fail), and v3.0 introduces no extract-stage changes that the eval spec must account for. The only gap is that output sanitization changes the effective gate pass rate, but this is orthogonal to the eval's progress-reporting focus. No revision needed for stages 1-3 review purposes.
