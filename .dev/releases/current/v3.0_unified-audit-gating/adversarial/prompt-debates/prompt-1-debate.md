---
title: "Adversarial Debate: Prompt 1 -- Eval Spec Generation"
depth: standard
debaters: [advocate, critic]
verdict: conditional-pass
date: 2026-03-19
---

# Adversarial Debate: Prompt 1 Fidelity and Quality

## 1. Fidelity Assessment

### Advocate

The generated prompt faithfully translates the original objective. The original asks for:
- Use of `/sc:brainstorm` -- present, with `--codebase --depth deep`
- Use of `/sc:spec-panel` -- present, with `--focus correctness,testability,architecture --mode critique`
- A small lightweight spec -- present, constrained to "< 15 minutes" and "MEDIUM" complexity
- Coverage of all 13 pipeline stages -- explicitly enumerated
- Conformance to the release-spec-template.md -- exact path provided with "Conform exactly" language

The prompt adds reasonable operationalization details (output path, sentinel check, intentional ambiguities) that are implied by the objective but not stated. These are constructive additions, not distortions.

### Critic

The prompt **adds significant requirements not present in the original objective**, which constitutes scope creep that risks prompt failure:

1. **"at least 5 functional requirements with testable acceptance criteria"** -- not in original. The original says "lightweight." Five FRs with acceptance criteria pushes toward a medium-weight spec.
2. **"at least 2 intentional ambiguities"** -- not in original. This is an engineering judgment about how to exercise deviation-analysis, but the original never asked for seeded defects. An eval spec could exercise deviation-analysis through naturally occurring ambiguities.
3. **"data model and architecture section that references real files in src/superclaude/cli/"** -- not in original. This constrains the brainstorm agent to a specific directory, which may not be the best choice for exercising wiring-verification.
4. **"complexity_class to MEDIUM so interleave_ratio maps to 1:2"** -- the original says "lightweight." MEDIUM complexity is an assumption about what exercises the pipeline best, not a stated requirement.
5. **Output path hardcoded** -- the original says nothing about where to write the spec.

These additions are individually defensible but collectively they transform a "generate and review a lightweight spec" objective into a detailed engineering specification. This narrows the brainstorm agent's latitude and risks the `/sc:brainstorm` invocation becoming a fill-in-the-blanks exercise rather than genuine brainstorming.

### Resolution

**Partial fidelity.** The core intent is preserved. The additions are reasonable engineering choices but should be marked as suggestions rather than hard requirements where possible. The "at least 2 intentional ambiguities" clause is the most defensible addition since without it, deviation-analysis and remediation stages may produce trivially empty output. The hardcoded output path is pragmatic but should be explicitly justified as an eval convention.

---

## 2. Completeness Assessment

### Advocate

Both required commands are invoked:
- `/sc:brainstorm` is the primary invocation with full context
- `/sc:spec-panel` is invoked as a quality gate after the spec is written

The spec-panel invocation uses `--focus correctness,testability,architecture --mode critique`, which aligns with the template's own quality gate recommendation: the template says specs should pass `/sc:spec-panel --focus correctness,architecture` and `/sc:spec-panel --mode critique`. The prompt combines these into a single invocation with an added `testability` focus, which is appropriate for an eval spec.

The sentinel check (`grep -c '{{SC_PLACEHOLDER:'`) follows the template's own recommendation and provides a mechanical verification that the brainstorm output is complete.

### Critic

There are two completeness gaps:

1. **The spec-panel invocation lacks sufficient context.** The prompt says "invoke /sc:spec-panel" but provides no guidance about what the panel should assess relative to eval fitness. The panel will default to reviewing the spec as if it were a real release spec, not an eval harness. It may flag the intentional ambiguities as defects rather than recognizing them as eval instrumentation. The prompt should instruct the panel to evaluate "fitness as an eval harness for the 13-stage pipeline" alongside standard quality dimensions.

2. **"Apply any critical findings" is vague.** What constitutes "critical"? If the spec-panel flags the intentional ambiguities (which it likely will, since that is literally its job), should they be preserved or fixed? The prompt creates a contradiction: it asks for intentional ambiguities AND asks the panel to critique them AND asks the operator to fix critical findings. This could result in the ambiguities being removed, defeating their purpose.

### Resolution

**Mostly complete, with one structural flaw.** The contradiction between "seed ambiguities" and "fix critical panel findings" must be resolved. The prompt should explicitly instruct the spec-panel to assess eval fitness and to preserve intentional ambiguities that are tagged as such. A practical fix: require the spec to mark intentional ambiguities with a `[EVAL-SEEDED]` tag so the panel can distinguish them from genuine defects.

---

## 3. Template Conformance

### Advocate

The prompt explicitly requires conformance: "Conform exactly to the template at /config/workspace/IronClaude/src/superclaude/examples/release-spec-template.md." This is the strongest possible conformance instruction. The sentinel check provides mechanical verification that all `{{SC_PLACEHOLDER:*}}` values have been populated.

The template has 12 major sections, conditional sections based on spec_type, YAML frontmatter with quality scores, and appendices. The prompt's requirements (5 FRs, data models, architecture referencing real files) align with sections the template demands for `new_feature` spec_type.

### Critic

"Conform exactly" is necessary but insufficient. Several conformance risks exist:

1. **Conditional sections are not addressed.** The template has sections marked `[CONDITIONAL: ...]` that should be included or excluded based on spec_type. The prompt never specifies what spec_type the eval spec should use. If the brainstorm agent picks `infrastructure`, it must include Section 5.3 (Phase Contracts) and Section 8.3 (Manual/E2E Tests). If it picks `new_feature`, it needs Section 4.5 (Data Models) and Section 5.1 (CLI Surface). The prompt asks for "a data model and architecture section" which implies `new_feature`, but this is never made explicit.

2. **Section 12 (Brainstorm Gap Analysis)** says it is "auto-populated by sc:cli-portify Phase 3c embedded brainstorm pass." Since this spec is being generated by `/sc:brainstorm` directly, it is unclear whether the brainstorm agent will populate this section or leave it as a placeholder. The sentinel check would catch an unpopulated placeholder, but the agent might simply omit the section.

3. **Section 10 (Downstream Inputs)** requires guidance for `sc:roadmap` and `sc:tasklist`. For an eval spec, these sections are meta-circular: the spec feeds into `sc:roadmap` which is what we are evaluating. The brainstorm agent may struggle to populate these meaningfully.

4. **Quality scores in frontmatter** (clarity, completeness, testability, consistency, overall) are self-assessed. A brainstorm agent will likely give itself high scores. The spec-panel should override these, but the prompt does not instruct this.

### Resolution

**Moderate conformance risk.** The "conform exactly" instruction plus sentinel check provides a floor, but the prompt should explicitly specify `spec_type: new_feature` to resolve conditional section ambiguity. The quality scores should be deferred to the spec-panel output.

---

## 4. Pipeline Coverage

### Advocate

The prompt is designed to exercise all 13 stages:
- **extract**: Any well-formed spec with FRs and architecture sections will produce meaningful extraction
- **generate-A/B**: Two roadmap variants will be generated from the extraction
- **diff**: Differences between variants will be identified
- **debate**: Debate rounds will assess variant trade-offs
- **score**: A winner will be selected
- **merge**: Best elements will be merged
- **test-strategy**: Test plan will be derived from the merged roadmap
- **spec-fidelity**: The merged roadmap will be compared against the original spec
- **wiring-verification**: Real file references in src/superclaude/cli/ will be verified against the codebase
- **deviation-analysis**: Intentional ambiguities will produce spec-fidelity deviations that feed deviation-analysis
- **remediate**: Deviation findings will produce remediation tasklists
- **certify**: The remediation results will be certified

The intentional ambiguities are specifically designed to ensure deviation-analysis, remediate, and certify do not produce trivially empty output. The real file references ensure wiring-verification has something to verify. This is thoughtful design.

### Critic

There are three significant pipeline coverage concerns:

1. **deviation-analysis is NOT a standalone step in `_build_steps()`.** Examining the executor code, `_build_steps()` produces exactly 10 step entries (including the parallel generate pair). The `_get_all_step_ids()` function lists 12 IDs: extract, generate-A, generate-B, diff, debate, score, merge, test-strategy, spec-fidelity, wiring-verification, remediate, certify. Neither function lists `deviation-analysis` as a discrete step. The `DEVIATION_ANALYSIS_GATE` exists in the gate registry, but deviation-analysis appears to be an implicit sub-process of the spec-fidelity/remediation flow, not a step with its own Claude subprocess invocation. The prompt claims 13 stages, but the pipeline may execute only 12 discrete steps with deviation-analysis being a logical phase within the spec-fidelity convergence loop. This needs verification -- if the eval claims to test 13 stages but only 12 are real steps, the eval's coverage claim is inflated.

2. **Trivial early stages.** A "lightweight" spec designed to complete in < 15 minutes will produce small extractions, short roadmap variants, and minimal diffs. The diff, debate, and score stages may produce output that is technically well-formed but evaluatively meaningless -- there is little to differentiate between two roadmaps for a 5-FR spec. The eval would pass its gates but not stress-test whether these stages function correctly under realistic load.

3. **remediate and certify depend on spec-fidelity producing FAIL.** If the spec-fidelity step passes (finding zero deviations), the pipeline skips remediate and certify entirely. The "2 intentional ambiguities" are supposed to trigger failures, but the spec-fidelity LLM might interpret them as acceptable and pass anyway. There is no guarantee that seeded ambiguities will produce the FAIL status needed to exercise the remediation pipeline. The prompt should consider requiring the ambiguities to be severe enough that spec-fidelity cannot reasonably pass.

### Resolution

**Significant coverage gap.** The deviation-analysis stage identity needs clarification against the actual codebase. If it is truly a sub-process rather than a discrete step, the prompt and the eval suite should acknowledge this (and the "13 stages" claim should be revised to "12 steps + 1 logical phase" or similar). The risk of trivial early-stage output is acceptable for a smoke-test eval but limits the eval's ability to detect regressions in diff/debate/score quality. The remediate/certify dependency on spec-fidelity FAIL is the most critical risk -- without it, 3 of the 5 new v3.0 stages are untested.

---

## 5. Risk Assessment

### Advocate

The prompt mitigates several key risks:
- **Timeout risk**: Constrained to < 15 minutes, MEDIUM complexity
- **Template drift risk**: Exact path reference and sentinel check
- **Empty stage risk**: Intentional ambiguities and real file references
- **Quality risk**: spec-panel critique pass required before completion

### Critic

Outstanding risks not mitigated:

1. **Brainstorm agent hallucination.** The prompt asks the agent to "target real code in this repository (src/superclaude/)." If the brainstorm agent has no codebase context (despite `--codebase`), it may hallucinate file paths. The wiring-verification step would then flag nonexistent files, which exercises wiring-verification but produces an eval that tests error-handling rather than normal operation. The prompt should list specific real files the spec should reference.

2. **Spec-panel overcorrection.** As noted in Section 2, the panel may "fix" the intentional ambiguities, defeating the eval design. There is no protection mechanism.

3. **Token budget.** The prompt invokes `/sc:brainstorm --depth deep`, which may consume substantial tokens generating the spec. Then `/sc:spec-panel` adds another pass. Then the actual `roadmap run` is a separate invocation. The total token cost across Prompts 1-6 may be prohibitive. The prompt does not discuss budget.

4. **Reproducibility.** LLM outputs are non-deterministic. Running this prompt twice may produce specs that exercise different pipeline behaviors. The eval lacks a deterministic baseline. This is inherent to LLM-based eval generation but should be acknowledged.

5. **Circular dependency.** The prompt asks `/sc:brainstorm` to produce a spec that will test the roadmap pipeline. But `/sc:brainstorm` itself may be affected by the v3.0 changes. If brainstorm is broken, it cannot produce a valid eval spec. This is a bootstrap problem the eval design does not address.

### Resolution

**Moderate risk profile.** The most actionable mitigation is to provide an explicit list of 3-5 real file paths from `src/superclaude/cli/` that the spec should reference, eliminating hallucination risk for wiring-verification. The spec-panel overcorrection risk should be addressed by tagging intentional ambiguities.

---

## 6. Recommended Improvements

### Critical (must-fix before execution)

1. **Tag intentional ambiguities.** Add to the prompt: "Mark each intentional ambiguity with an `<!-- EVAL-SEEDED-AMBIGUITY -->` HTML comment so /sc:spec-panel preserves them during critique."

2. **Specify spec_type explicitly.** Add: "Set spec_type to `new_feature` to ensure correct conditional section inclusion."

3. **Instruct spec-panel on eval context.** Change the spec-panel invocation to: `/sc:spec-panel --focus correctness,testability,architecture --mode critique` with added context: "This spec is an eval harness. Preserve sections marked EVAL-SEEDED-AMBIGUITY. Assess fitness for exercising all 13 pipeline stages."

### Important (should-fix)

4. **Clarify the deviation-analysis stage identity.** Add a note: "Note: deviation-analysis may execute as a logical phase within the spec-fidelity convergence loop rather than as a standalone subprocess. The spec should produce deviations that exercise whichever form it takes."

5. **Provide real file paths.** Replace "references real files in src/superclaude/cli/" with an explicit list, e.g.: "Reference these specific files: `src/superclaude/cli/roadmap/executor.py`, `src/superclaude/cli/roadmap/commands.py`, `src/superclaude/cli/roadmap/gates.py`, `src/superclaude/cli/main.py`."

6. **Ensure ambiguities are severe enough.** Add: "The intentional ambiguities must be significant enough to produce BLOCKING or WARNING findings in spec-fidelity, not merely INFO-level observations. Without this, remediate and certify stages will be skipped."

### Nice-to-have

7. **Add a smoke-test instruction.** After the sentinel check, add: "Run `superclaude roadmap run <spec> --dry-run` to verify the spec is accepted by the pipeline before committing to a full run."

8. **Acknowledge non-determinism.** Add a note that the eval spec should be reviewed and version-controlled after generation, since re-running the prompt may produce a different spec.

---

## Verdict

**Conditional pass.** Prompt 1 faithfully captures the core objective and demonstrates thoughtful engineering (intentional ambiguities for deviation-analysis, real file references for wiring-verification, sentinel check for template conformance). However, it has a structural flaw (the ambiguity-preservation vs. spec-panel-critique contradiction) and a coverage risk (deviation-analysis may not be a discrete step, remediate/certify depend on spec-fidelity producing FAIL). With the three critical fixes applied, the prompt is ready for execution.

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Fidelity | 7/10 | Core intent preserved; scope creep in added constraints |
| Completeness | 8/10 | Both commands invoked; spec-panel lacks eval-aware context |
| Template conformance | 7/10 | Sentinel check good; conditional sections unspecified |
| Pipeline coverage | 6/10 | deviation-analysis identity unclear; remediate/certify conditional |
| Risk mitigation | 5/10 | Ambiguity preservation flaw; hallucination risk for file paths |
| Overall | 6.5/10 | Solid foundation; needs the 3 critical fixes before execution |
