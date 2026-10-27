---
stage: 4
stage_name: diff
depth: quick
gate: DIFF_GATE
verdict: ADEQUATE
---

# Stage 4: diff -- Adversarial Review

## Q1: Meaningful Output

The DIFF_GATE is STANDARD tier with only two required frontmatter fields (`total_diff_points`, `shared_assumptions_count`) and a 30-line minimum. No semantic checks. For the eval spec (FR-EVAL-001, progress reporting), two roadmap variants will have been generated at stages 2-3 from the same spec. Both variants will address the same 6 functional requirements and produce overlapping architectural decisions (e.g., callback hook mechanism, progress.json format, --progress-file CLI option). The diff will identify genuine divergence points -- different decomposition of FR-001.4's undefined deviation sub-entry schema, different handling of FR-001.5's ambiguous "significant findings" threshold, and potentially different implementation ordering.

**Assessment**: The gate will pass non-trivially. The 30-line minimum is easily met by any substantive diff of two roadmap variants addressing 6 FRs. The frontmatter fields will be populated with real counts. However, the gate cannot distinguish between a diff that surfaces architecturally meaningful divergences and one that merely catalogs formatting differences. This is by design -- STANDARD tier gates are structural, not qualitative.

**Risk of trivial pass**: Low. Two independently generated roadmaps for a MEDIUM-complexity spec with seeded ambiguities will produce at least 5-10 genuine divergence points. The seeded ambiguities in FR-001.4 and FR-001.5 virtually guarantee that the variants will disagree on deviation sub-entry schema and remediation trigger thresholds, producing substantive diff content.

## Q2: v3.0 Changes

Stages 4-6 are unchanged in v3.0. The DIFF_GATE definition (`required_frontmatter_fields=["total_diff_points", "shared_assumptions_count"]`, `min_lines=30`, `enforcement_tier="STANDARD"`) is identical to master.

**Indirect effects from upstream v3.0 changes**: None material. The upstream changes (extraction, generation) are unchanged for stages 1-3. The diff stage consumes the output of generate-A and generate-B, which use the same GENERATE_A_GATE and GENERATE_B_GATE definitions as master.

**Indirect effects from downstream v3.0 changes**: The eval spec adds progress reporting, which means a `StepProgress` entry will be written after the diff step completes. This is purely additive -- the progress reporter is a post-step callback that reads the gate verdict but does not alter it. The diff stage's behavior and gate evaluation are unaffected.

## Q3: Artifact Verification

**Artifact produced**: `diff-analysis.md` -- a Markdown document with YAML frontmatter containing `total_diff_points` and `shared_assumptions_count`, followed by sections enumerating shared assumptions, divergence points, and relative strength assessments.

**Third-party verification**:
1. **Structural**: Parse YAML frontmatter, confirm both required fields are present and contain integer values. Count lines, confirm >= 30.
2. **Content quality**: Verify `total_diff_points` matches the actual number of divergence sections in the document body. Verify `shared_assumptions_count` matches the count of enumerated shared assumptions. Cross-reference each divergence point against the two input roadmap variants to confirm it reflects a genuine difference, not a hallucinated one.
3. **Completeness**: Check that the diff covers all major sections of both variants (requirements, architecture, phasing, risk). Absence of a diff point on a section where the variants actually diverge indicates an omission.

## Q4: Most Likely Failure Mode

**Inflated shared_assumptions_count**. The diff prompt asks the LLM to enumerate shared assumptions between two roadmap variants. For a MEDIUM-complexity spec with 6 functional requirements, the LLM may count trivially obvious agreements (e.g., "both variants agree Python is used," "both variants agree the spec has 6 FRs") alongside genuine architectural agreements. This inflates `shared_assumptions_count` without adding analytical value, but the gate cannot detect it because there is no semantic check validating the quality or non-triviality of shared assumptions.

This failure mode is silent -- the gate passes, the artifact looks complete, but the downstream debate stage receives a diff analysis that overstates convergence and understates the divergence space.

**Secondary failure mode**: The diff may fail to identify that the two variants handle FR-001.4's undefined schema differently, because both variants may paper over the ambiguity with similar placeholder language. If the diff misses this divergence, the seeded ambiguity propagates undetected through debate and merge, potentially reaching spec-fidelity as a surprise finding rather than a known tracked issue.

## Q5: Eval Spec Coverage

**v3.0 changes to this stage**: None. The DIFF_GATE is unchanged.

**What the eval spec must exercise**: The eval spec's progress reporting feature (FR-EVAL-001.1) requires that a `StepProgress` entry be written after the diff step with `step_id`, `status`, `duration_ms`, `gate_verdict`, and `output_file`. This is a test of the progress reporter callback, not the diff stage itself.

**Does the eval spec account for this?** Yes, adequately. The eval spec's data flow diagram (Section 2.2) explicitly shows `[diff] --> progress.json (step 4 entry)`. FR-EVAL-001.1's acceptance criteria require each entry to contain the specified fields. The diff step will produce a straightforward pass/fail gate verdict that the progress reporter can capture. No special handling is needed for the diff step's progress entry because DIFF_GATE is STANDARD tier with no semantic checks -- the progress entry's `gate_verdict` will be a simple pass/fail based on frontmatter presence and line count.

**Gap**: The eval spec does not specify whether the progress entry should record `total_diff_points` or `shared_assumptions_count` in the `metadata` dict of `StepProgress`. For stages 4-6 this is a minor omission because these values are informational, not gate-critical. For downstream stages (spec-fidelity, wiring-verification) where the eval spec defines specific fields like `unwired_count` and `blocking_count` in FR-001.6, the metadata schema is more important. The absence of per-stage metadata schema for stages 4-6 is acceptable given these stages are unchanged in v3.0.

## Verdict

**ADEQUATE**. The diff stage is unchanged in v3.0, the DIFF_GATE will pass non-trivially for this eval spec, and the eval spec's progress reporting requirement for this stage is straightforward and well-specified. The identified failure modes (inflated shared assumptions, missed seeded ambiguity) are inherent limitations of STANDARD-tier gates without semantic checks, not eval spec deficiencies. No revision needed for the eval spec's coverage of this stage.
