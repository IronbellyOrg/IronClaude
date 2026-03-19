---
stage: 5
stage_name: debate
depth: quick
gate: DEBATE_GATE
verdict: ADEQUATE
---

# Stage 5: debate -- Adversarial Review

## Q1: Meaningful Output

The DEBATE_GATE is STRICT tier with two required frontmatter fields (`convergence_score`, `rounds_completed`) and one semantic check (`convergence_score_valid` -- must be a float in [0.0, 1.0]). Minimum 50 lines.

For the eval spec (FR-EVAL-001, progress reporting), the debate will receive a diff-analysis identifying divergence points between two roadmap variants. The eval spec's MEDIUM complexity (0.45) and 6 functional requirements provide enough substance for a multi-round debate. The two seeded ambiguities (FR-001.4 undefined schema, FR-001.5 undefined threshold) will generate genuine disagreement between variants because each variant must take a position on how to handle the ambiguity -- one may propose a nested sub-array schema while the other proposes flat entries, one may define "significant" as HIGH severity while the other uses a count threshold.

**Assessment**: The gate will pass non-trivially. The semantic check (`convergence_score_valid`) requires the LLM to produce a well-formed float in [0.0, 1.0], which exercises actual validation logic rather than just checking field presence. The 50-line minimum requires substantive debate content. However, the gate cannot verify that the convergence score accurately reflects the degree of actual convergence -- an LLM could output `convergence_score: 0.85` while the debate transcript shows fundamental unresolved disagreements.

**Risk of trivial pass**: Low. The STRICT tier and semantic check make this the most rigorous gate among stages 4-6. The seeded ambiguities ensure the debate has genuine material to work with.

## Q2: v3.0 Changes

The DEBATE_GATE definition is unchanged in v3.0: `required_frontmatter_fields=["convergence_score", "rounds_completed"]`, `min_lines=50`, `enforcement_tier="STRICT"`, with the `convergence_score_valid` semantic check. No code changes to the debate step logic.

**Indirect effects from upstream v3.0 changes**: None. The diff-analysis artifact feeding into the debate is produced by an unchanged DIFF_GATE. The debate prompt builder (`build_debate_prompt`) is unchanged.

**Indirect effects from downstream v3.0 changes**: The debate output feeds into the score stage (unchanged) and eventually into the merge stage (unchanged). The merged roadmap then enters the v3.0-changed stages (spec-fidelity with convergence loop, deviation-analysis, wiring-verification, remediate, certify). The debate's `convergence_score` has no direct downstream mechanical effect -- it is informational metadata consumed by the score step for base variant selection, not used as a gate input by any downstream stage.

However, there is a subtle indirect effect: if the debate fails to resolve disagreements about FR-001.4's deviation sub-entry schema, those unresolved disagreements propagate into the merged roadmap, which then hits spec-fidelity. The spec-fidelity convergence loop (a v3.0 addition) may then surface these as deviations, triggering deviation-analysis iterations. This is actually desirable for the eval -- it exercises the v3.0 convergence machinery. But it means the debate stage's quality directly influences the downstream v3.0 stages' workload, even though the debate stage itself is unchanged.

## Q3: Artifact Verification

**Artifact produced**: `debate-transcript.md` -- a Markdown document with YAML frontmatter containing `convergence_score` (float) and `rounds_completed` (integer), followed by a multi-round adversarial debate transcript with positions, rebuttals, concessions, and a convergence assessment.

**Third-party verification**:
1. **Structural**: Parse YAML frontmatter, confirm `convergence_score` is a float in [0.0, 1.0] and `rounds_completed` is a positive integer. Count lines, confirm >= 50.
2. **Semantic check replay**: Run `_convergence_score_valid(content)` against the artifact to confirm the gate's semantic check passes independently.
3. **Content quality**: For each divergence point from the diff-analysis, verify the debate transcript addresses it with substantive positions from both variants (not just restating the diff). Verify concessions are logically grounded -- a concession should cite evidence or rebut-then-yield, not simply capitulate.
4. **Convergence score calibration**: Count the number of fully resolved divergence points (concessions made), partially resolved points (positions softened but not conceded), and unresolved points. Verify the `convergence_score` is roughly proportional to (resolved + 0.5*partial) / total. A score of 0.95 with 3 unresolved points is suspicious.
5. **Round count**: Verify `rounds_completed` matches the actual number of debate rounds in the transcript body.

## Q4: Most Likely Failure Mode

**Convergence score inflation**. The LLM generating the debate transcript controls both the debate content and the `convergence_score` frontmatter value. There is no external calibration -- the same agent that writes the arguments also scores their convergence. The incentive structure favors optimistic convergence scores because higher scores signal "success" to the human operator reviewing artifacts.

For the eval spec specifically, this manifests as the debate declaring convergence on FR-001.4 and FR-001.5 by adopting one variant's interpretation without adequately flagging that the spec itself is ambiguous. The debate may produce `convergence_score: 0.82` and claim "both variants agree on deviation sub-entry schema" when in reality both variants invented different schemas and the debate simply picked one. The seeded ambiguity is then "resolved" at the debate stage rather than propagating to spec-fidelity where it belongs.

**Impact on eval validity**: If the debate resolves seeded ambiguities prematurely, the downstream spec-fidelity and deviation-analysis stages may not find the BLOCKING and WARNING findings that the eval is designed to trigger. This would make the eval appear to pass cleanly when it should have surfaced the ambiguities. However, this is a content quality issue, not a gate logic issue -- the DEBATE_GATE correctly validates structural integrity regardless of whether the convergence score is inflated.

**Mitigation**: The eval should verify post-hoc that the seeded ambiguities in FR-001.4 and FR-001.5 are surfaced as findings in the spec-fidelity stage. If they are not, the debate stage likely resolved them prematurely.

## Q5: Eval Spec Coverage

**v3.0 changes to this stage**: None. The DEBATE_GATE is unchanged.

**What the eval spec must exercise**: FR-EVAL-001.1 requires a `StepProgress` entry for the debate step with `step_id`, `status`, `duration_ms`, `gate_verdict`, and `output_file`. Because the DEBATE_GATE is STRICT tier with a semantic check, the progress entry's `gate_verdict` reflects a more meaningful validation than stages 4 or 6 (which are STANDARD tier). The progress reporter should ideally capture whether the semantic check passed or failed, not just the overall gate verdict.

**Does the eval spec account for this?** Partially. The eval spec's `StepProgress` data model (Section 4.5) includes a `metadata: dict` field that could hold semantic check results, but the spec does not define what metadata to capture for debate or any other stage. FR-EVAL-001.1 only requires the five core fields (`step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`). The absence of per-stage metadata specification is a minor gap but not blocking -- the five core fields are sufficient for progress tracking, and semantic check detail can be added later.

**Additional consideration**: The debate stage's `convergence_score` is a natural candidate for inclusion in the progress entry's metadata, since it is the most informative single metric for the debate's quality. The eval spec does not call this out, but the `metadata` dict provides an extension point. This is a nice-to-have, not a requirement gap.

## Verdict

**ADEQUATE**. The debate stage is unchanged in v3.0, the DEBATE_GATE exercises meaningful validation through its STRICT tier and `convergence_score_valid` semantic check, and the eval spec's progress reporting requirements are well-specified for the core fields. The convergence score inflation risk is real but is a content quality concern inherent to LLM-generated debate transcripts, not a gap in the eval spec or gate logic. The eval should include a post-hoc check that seeded ambiguities propagate to spec-fidelity rather than being silently resolved at the debate stage, but this is a test design recommendation, not a blocking revision to the eval spec itself.
