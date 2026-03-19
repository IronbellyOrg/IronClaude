---
stage: 3
stage_name: generate-B
depth: quick
gate: GENERATE_B_GATE
verdict: ADEQUATE
---

# Stage 3: generate-B -- Adversarial Review

## Q1: Meaningful Output

The eval spec will produce meaningful output at this stage. Generate-B receives the same extraction as generate-A but uses a different agent (typically `haiku:architect` vs. `opus:architect` per `RoadmapConfig` defaults). The GENERATE_B_GATE is structurally identical to GENERATE_A_GATE: 3 frontmatter fields (`spec_source`, `complexity_score`, `primary_persona`), min_lines=100, and the same 2 semantic checks (`frontmatter_values_non_empty`, `has_actionable_content`).

The gate will not trivially pass or fail. The same analysis from stage 2 applies: the MEDIUM-complexity eval spec provides sufficient material for a 100+ line roadmap, but the output depends on the agent's capability. The key difference is that generate-B typically uses a less capable model (haiku), which increases the probability of:
- Thinner output (closer to the 100-line threshold)
- Less structured content (potentially failing `has_actionable_content` if the model produces only prose paragraphs)
- Frontmatter field omission (haiku follows complex multi-field instructions less reliably than opus)

This model-capability differential is by design: the adversarial pipeline *wants* variant diversity for the downstream diff/debate stages. A generate-B that produces a meaningfully different roadmap is more valuable than one that mirrors generate-A.

**Risk of trivial pass**: moderate. The gate bar is the same as generate-A, but haiku's instruction-following variance is higher. The eval spec's MEDIUM complexity (6 FRs, 3 NFRs) is within haiku's reliable extraction range, so trivial failure is unlikely. But haiku is more likely than opus to produce borderline outputs (e.g., 95-105 lines, or a roadmap without bulleted lists).

## Q2: v3.0 Changes

The GENERATE_B_GATE definition is identical between master and v3.0. The `build_generate_prompt()` function is reused for both variants with different `AgentSpec` inputs. The parallel step group construction in `_build_steps()` is unchanged for generate-A/B.

Indirect v3.0 changes:

1. **Output sanitization**: Identical impact to stages 1 and 2. This is potentially *more* impactful for generate-B because haiku is more likely to emit conversational preamble ("Sure! Here is the roadmap...") before the `---` delimiter. On master, this would be a hard gate failure. In v3.0, `_sanitize_output()` rescues these outputs. This means generate-B's effective pass rate is meaningfully higher in v3.0 than on master.

2. **Embed size limit**: Same as stage 2. Irrelevant for this eval spec's extraction size.

3. **Downstream impact**: Generate-B's output feeds into stage 4 (diff). If generate-B produces a low-quality or thin roadmap, the diff stage will have less material to analyze. This cascading quality effect is not a v3.0 change, but it is worth noting for eval analysis: a weak generate-B does not block the pipeline (the gate is structural, not qualitative) but degrades downstream stage value.

## Q3: Artifact Verification

**Artifact**: `{output_dir}/roadmap-{agent_id}.md` (e.g., `roadmap-haiku-architect.md`)

| Check | Method | Automated? |
|-------|--------|------------|
| Frontmatter fields present | Parse YAML, verify `spec_source`, `complexity_score`, `primary_persona` | Yes (gate) |
| Frontmatter values non-empty | All values have content | Yes (semantic check) |
| Actionable content exists | At least one bulleted/numbered list item | Yes (semantic check) |
| Minimum length | >= 100 lines | Yes (gate) |
| Variant differentiation | Content differs meaningfully from generate-A output | Manual |
| Persona consistency | `primary_persona` matches the agent's declared persona | Manual |
| Complexity score propagation | `complexity_score` matches extraction's value (not independently derived) | Manual |

A critical third-party verification that the gate does *not* perform: **variant independence**. The pipeline's value proposition depends on generate-A and generate-B producing genuinely different roadmaps. If both variants are near-identical (possible if both agents interpret the eval spec the same way), the downstream diff/debate stages produce trivial output. The eval spec does not measure variant divergence at this stage.

## Q4: Most Likely Failure Mode

**Insufficient line count from the weaker model.** Generate-B uses the secondary agent (default: haiku). For a MEDIUM-complexity spec, haiku may produce a roadmap that hovers around the 100-line threshold. Specific scenarios:

1. **Terse phase descriptions**: Haiku tends to be more concise. A 5-phase roadmap with 15-20 lines per phase = 75-100 lines, right at the boundary.
2. **Missing sections**: The prompt requests 6 sections (executive summary, phased plan, risk assessment, resource requirements, success criteria, timeline). Haiku may omit or collapse sections, reducing total output.
3. **Frontmatter inflation**: If the model emits verbose frontmatter (comments, extra fields), the 100-line count includes those lines but the body may still be thin.

The mitigation is the eval spec's inherent richness: 6 FRs with acceptance criteria, 3 NFRs with targets, risk tables, and dependency references give even haiku enough material to expand upon.

**Second most likely**: `frontmatter_values_non_empty` failing because haiku emits `complexity_score:` with no value, or `primary_persona:` as an empty string. The `_parse_frontmatter()` implementation splits on `:` and strips whitespace, so `complexity_score: ` (trailing space, no value) would produce an empty string and fail the check.

## Q5: Eval Spec Coverage

v3.0 does not change the generate-B stage. The eval spec's coverage requirements are identical to stage 2, with one additional consideration:

1. **Parallel timing accuracy**: FR-EVAL-001.1 requires "parallel steps (generate-A, generate-B) produce independent entries with correct timing." This is the most eval-relevant concern for stage 3. Generate-B starts simultaneously with generate-A, and each must have independent `duration_ms` values. If generate-B (haiku) completes in 30 seconds and generate-A (opus) completes in 90 seconds, the progress file must reflect both durations accurately, not assign both the wall-clock time of the slower step.

2. **Output sanitization asymmetry**: v3.0's preamble stripping is more likely to activate for generate-B (haiku) than generate-A (opus). If the eval measures "steps that required sanitization," this asymmetry is observable. The eval spec does not track sanitization events in progress.json, which is acceptable -- sanitization is an internal implementation detail, not a progress-reporting concern.

3. **Gate verdict symmetry**: GENERATE_B_GATE is defined as a separate constant from GENERATE_A_GATE, but with identical criteria. The eval should verify that the progress reporter records the correct gate name for each step (not aliasing B's verdict to A's). The eval spec does not explicitly test gate name accuracy in progress entries, but this is implied by FR-EVAL-001.1's `gate_verdict` field.

**Coverage assessment**: The eval spec adequately exercises stage 3. The parallel execution focus is the correct concern. The model-capability differential (opus vs. haiku) introduces natural variance that makes the eval more realistic than a single-agent pipeline would.

## Verdict

**ADEQUATE.** The eval spec handles stage 3 correctly. The GENERATE_B_GATE is unchanged in v3.0, the eval spec explicitly addresses parallel step progress reporting (the key challenge), and the MEDIUM-complexity eval spec provides sufficient material for even the weaker agent to produce gate-passing output. The model-capability differential between generate-A and generate-B introduces healthy variance for downstream stages.

One observation for the eval design (not a revision blocker): the eval spec could benefit from asserting that generate-A and generate-B progress entries have *different* `duration_ms` values as a signal of genuine independent timing, rather than both being stamped with the parallel group's wall-clock time. This is a test-design improvement, not a spec-coverage gap.
