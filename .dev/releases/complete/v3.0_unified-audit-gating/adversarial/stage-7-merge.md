---
stage: 7
stage_name: merge
depth: quick
gate: MERGE_GATE
verdict: ADEQUATE
---

# Stage 7: merge -- Adversarial Review

## Q1: Meaningful Output

The eval spec (FR-EVAL-001) is a MEDIUM complexity new-feature spec with 6 functional requirements, 3 NFRs, clear architecture sections, and a well-defined dependency graph. This is substantial enough to produce a meaningful merged roadmap that exercises all three MERGE_GATE semantic checks:

- **no_heading_gaps**: The spec's architecture (4.1-4.6), requirements (3.x), and appendices produce a heading hierarchy rich enough that a merged roadmap will include H2/H3/H4 levels. An LLM synthesizing two variant roadmaps from this spec has a real chance of introducing a heading gap (e.g., jumping from H2 to H4 when merging a deep subsection from one variant into the other).
- **cross_refs_resolve**: The spec contains cross-references between sections (e.g., FR-EVAL-001.4 references convergence.py, Section 4.6 references implementation order). Merged roadmaps will likely include "See section X" references that must resolve. However, `_cross_refs_resolve` is in warning-only mode (always returns True per OQ-001), so this check cannot cause a gate failure regardless of content quality.
- **no_duplicate_headings**: With two roadmap variants being merged, there is a realistic chance of duplicate H2/H3 headings (e.g., both variants having "## Risk Assessment" or "## Implementation Plan"). This check is genuinely exercised.

The 150-line minimum is realistic for a MEDIUM-complexity spec with 6 FRs -- both variants should individually exceed 100 lines, and the merge should exceed 150.

The gate will not trivially pass: the structural checks on heading hierarchy and duplicate headings are genuine constraints the LLM must satisfy. It will not trivially fail either: the spec is well-structured enough that a competent merge should pass.

**Assessment**: Meaningful -- the eval spec exercises the gate non-trivially.

## Q2: v3.0 Changes

Stage 7 (merge) itself is **unchanged in v3.0**. The `MERGE_GATE` definition (3 required frontmatter fields, 150 min lines, 3 semantic checks) is identical between master and v3.0. The `build_merge_prompt()` function is unchanged. The step construction in `_build_steps()` is unchanged.

**Indirect effects from upstream v3.0 changes**: None material. The upstream stages that feed into merge (score, generate-A, generate-B, debate) are also structurally unchanged in v3.0. The v3.0 changes primarily affect stages 8+ (spec-fidelity convergence, wiring verification, deviation analysis, remediate, certify).

**Indirect effects from downstream v3.0 changes**: The merged roadmap (`roadmap.md`) becomes the input to spec-fidelity (stage 8+), which now has a convergence loop in v3.0. The quality of the merge output therefore has amplified downstream impact in v3.0 -- a low-quality merge that passes the merge gate but contains subtle spec infidelities will trigger more convergence iterations downstream. However, this does not change what the eval spec must exercise at stage 7 itself.

**One executor-level v3.0 change does affect this stage indirectly**: the new `_sanitize_output()` function (added in v3.0) runs on all step outputs before gate validation. This strips conversational preamble before the `---` frontmatter delimiter. On master, if an LLM produced preamble text before the frontmatter, the gate would fail on missing frontmatter. In v3.0, the sanitizer rescues this case. This is a leniency increase, not a strictness increase, so the eval spec's merge output is more likely to pass in v3.0 than master.

## Q3: Artifact Verification

**Artifact**: `{output_dir}/roadmap.md` -- the final merged roadmap.

**Third-party verification checklist**:

1. **Frontmatter completeness**: Verify the file starts with `---` and contains `spec_source`, `complexity_score`, and `adversarial: true`. These are machine-parseable.
2. **Min line count**: `wc -l roadmap.md` >= 150.
3. **No heading gaps**: Parse heading levels sequentially; verify no level jumps > 1. This is a deterministic check a third party can replicate with the `_no_heading_gaps()` function or a simple script.
4. **No duplicate headings**: Extract all H2 and H3 heading text; verify uniqueness within each level. Deterministic.
5. **Cross-refs resolve**: Extract "See section X" patterns; verify matching headings exist. Note: currently warning-only, so this is informational.
6. **Content quality (subjective)**: Verify the roadmap synthesizes elements from both variants and reflects debate outcomes. This requires reading the variant roadmaps and debate transcript. Not automatable but a third party with access to the pipeline artifacts can verify.

**Automation level**: Checks 1-5 are fully automatable. Check 6 is subjective but bounded (compare section headings and themes across variants + merge).

## Q4: Most Likely Failure Mode

**Duplicate H2/H3 headings from variant merge conflict.**

When the merge prompt instructs the LLM to "use the selected base variant as foundation and incorporate the best elements from the other variant," the LLM commonly produces duplicate section headings. For example:
- Base variant has `## Risk Assessment` with risks A, B, C
- Other variant has `## Risk Assessment` with risks D, E, F
- LLM merges by including both sections verbatim, producing two `## Risk Assessment` headings

The `_no_duplicate_headings` check catches this and fails the gate. With `retry_limit=1`, the step gets one retry, but the retry prompt is the same as the original (no targeted fix instruction), so the LLM may produce the same structural error.

This failure mode is not specific to the eval spec -- it affects any merge -- but the eval spec's 6 FR sections, NFR section, risk section, and test plan section provide multiple opportunities for heading collisions.

**Mitigation present in the pipeline**: The merge prompt explicitly says "Do not duplicate heading text at H2 or H3 level," which reduces but does not eliminate this risk.

## Q5: Eval Spec Coverage

Since stage 7 is unchanged in v3.0, the question is whether the eval spec adequately exercises the existing merge gate.

**Covered**:
- `spec_source` frontmatter: The eval spec has a clear filename that should propagate through extraction to variants to merge.
- `complexity_score`: 0.45 -- propagated from extraction.
- `adversarial: true`: Set by the merge prompt, independent of spec content.
- Heading hierarchy: The eval spec's structure (numbered sections 1-12 with subsections) will produce roadmaps with multi-level headings.
- Min 150 lines: MEDIUM complexity with 6 FRs should produce sufficient output.

**Not specifically exercised but not required**:
- The eval spec does not specifically test the cross-refs semantic check's warning-only behavior, but since that check always returns True, it cannot affect gate pass/fail regardless.

**Gap**: The eval spec does not exercise the `_sanitize_output()` preamble stripping that v3.0 adds. If the LLM produces conversational preamble before frontmatter at the merge stage, v3.0 silently rescues it while master would fail. The eval spec does not distinguish these behaviors. This is a minor gap -- the sanitizer is a general-purpose executor enhancement, not a merge-specific feature.

**Assessment**: The eval spec adequately covers what MERGE_GATE requires. No revision needed for stage 7.

## Verdict

**ADEQUATE** -- Stage 7 is unchanged in v3.0, and the eval spec's structure (MEDIUM complexity, 6 FRs, multi-level sections) exercises all three MERGE_GATE semantic checks non-trivially. The most likely failure mode (duplicate headings) is a known LLM behavioral issue mitigated by prompt instruction and retry. No eval spec revision needed for this stage.
