# Adversarial Debate: Prompt 6 -- Scoring + Conditional Improvement Proposals

**Date**: 2026-03-19
**Format**: 3-round structured debate (standard depth)
**Expert A**: Advocate (defends fidelity of the generated prompt to the original objective)
**Expert B**: Skeptic (identifies deviations, gaps, over-specifications, and failure modes)

**Artifacts under review**:
- Generated Prompt 6 (in eval-prompts.md, lines 248-299)
- Original user objective for Prompt 6 (from 6PromptV3-Eval.md)
- Upstream dependencies: scoring-framework.md (P5), eval-runs/ (P5), eval-spec.md (P1)

---

## ROUND 1: Initial Positions

### Expert A (Advocate)

I will defend the generated Prompt 6 on each of the six debate axes.

**1. Fidelity to the original objective**

The original says: "utilizes the instruction in the scoring framework .md file to evaluate the results." The generated prompt opens with "Read the scoring framework at .dev/.../scoring-framework.md and apply it to the eval run results." Step 1.3 explicitly says "Apply the scoring framework metrics to compute per-stage scores." This is faithful. The prompt does not invent its own scoring methodology -- it defers to the framework document. Steps 1.1 and 1.2 (artifact inventory, gate pass/fail determination) are prerequisite data collection that any scoring application would require. They are not alternative scoring -- they are inputs to the framework's metrics.

The generated prompt does add structural specificity (4 runs named local-A/B and global-A/B, 13 stages, delta computation formulas) but these are concretizations of what Prompt 5 established, not deviations from the original objective. The original assumes these details are inherited from the eval suite design.

**2. Conditional brainstorm fidelity**

The original says "only in the event that poor results/deltas were produced." The generated prompt defines four trigger conditions: (a) overall delta negative or neutral, (b) any individual stage delta negative, (c) reproducibility < 80%, (d) new v3.0 stages produced no meaningful output. Conditions (a) and (b) are direct operationalizations of "poor deltas." Condition (d) -- new stages producing nothing -- is a reasonable interpretation of "poor results" since a stage that produces no output is definitionally a poor result. Condition (c) -- reproducibility -- is the only stretch, but I argue it is a faithful interpretation: if results are not reproducible, they are unreliable, and unreliable results are poor results regardless of their magnitude.

The disjunctive structure (any one condition triggers brainstorm) is appropriately conservative. The original says "poor results/deltas" with a slash, suggesting these are two facets of the same concern. The generated prompt captures both.

**3. Code-specific proposals**

The original says "5 actionable proposals at improvements of the relevant code." The generated prompt requires: (1) "Reference specific files and line numbers in src/superclaude/cli/roadmap/ and src/superclaude/cli/audit/", (2) "Each proposal must target a specific negative delta from the eval report", (3) "expected impact on the specific metric, and a testable acceptance criterion." This is strong. The file/line requirement prevents vague suggestions. The metric-targeting requirement ensures proposals address measured problems, not hypothetical ones. The acceptance criterion requirement makes proposals falsifiable.

**4. Report exhaustiveness**

The original says "exhaustive report." The generated prompt defines 6 sections: per-stage scoring table, delta summary, overall impact score, reproducibility assessment, artifact inventory with paths, and before/after comparison for new stages. This covers quantitative results (sections 1-3), reliability (section 4), verifiability (section 5), and v3.0-specific impact (section 6). An exhaustive report for an A/B eval of a 13-stage pipeline should contain exactly these dimensions.

**5. Dependency chain resilience**

The generated prompt assumes scoring-framework.md and eval-runs/ exist. This is appropriate -- Prompt 6 is Step 6 in a sequential pipeline. If upstream artifacts are missing, the prompt will fail visibly (the framework file will not be found, the eval-runs directory will be empty). This is fail-fast behavior, which is better than silent degradation.

**6. Happy path addition**

The generated prompt adds "IF all deltas are positive and reproducibility is >= 80%: Report validation pass and skip the brainstorm." The original does not mention this, but the original's conditional ("only in the event that poor results/deltas were produced") logically implies there is a non-poor case where the brainstorm is not invoked. The generated prompt makes this implicit case explicit. This is a clarifying addition, not a deviation.

### Expert B (Skeptic)

I will challenge each claim with specific evidence.

**1. Fidelity: The prompt does NOT purely defer to the scoring framework**

Expert A claims the prompt "defers to the framework document." This is misleading. Step 2 defines its own delta computation methodology: "Local average score vs Global average score = delta" and "Local A vs Local B consistency = reproducibility score." These are not instructions to apply the scoring framework -- they are instructions that may or may not align with whatever the scoring framework specifies.

The original objective says "utilizes the instruction in the scoring framework .md file." This means the scoring framework should be the authoritative source for how to compute deltas, what thresholds to use, and how to interpret results. But the generated prompt pre-specifies all of this. If the scoring framework defines a weighted delta computation (which Prompt 5 instructs it to do -- see line 203: "Define how to compute v3.0-vs-master delta for each metric"), and the generated Prompt 6 says "just average local vs global," there is a conflict. The prompt should say "follow the delta computation method defined in the scoring framework" rather than prescribing its own.

This is not a minor point. The entire purpose of generating the scoring framework in Prompt 5 (with adversarial review) was to produce a rigorous, reviewed methodology. Prompt 6 then partially ignores it by hardcoding a simpler approach.

**2. Conditional brainstorm: Condition (c) is an over-specification**

The original says "poor results/deltas." Reproducibility at < 80% is not a "poor result" in the sense the user intended. The user was asking about v3.0 vs master impact. If v3.0 consistently produces better deltas but with 75% reproducibility, that is a noisy-but-positive signal, not a trigger for "propose code improvements." The brainstorm is supposed to address "poor results" -- meaning v3.0 did not improve things. High variance is a different problem (it suggests LLM non-determinism, not code bugs).

Furthermore, condition (b) -- "any individual stage delta is negative" -- is too hair-trigger. If 12 out of 13 stages show positive deltas and one stage shows -0.01, triggering a full brainstorm of 5 code improvements is disproportionate. The original says "poor results/deltas" not "any single negative data point." A threshold or significance test would be more appropriate.

Condition (d) -- new stages producing no output -- is actually well-grounded. If spec-fidelity or wiring-verification produces nothing, that is unambiguously a poor result for v3.0.

**3. Code proposals: Anchored but not guaranteed**

The generated prompt says "Reference specific files and line numbers." This is an instruction, not a guarantee. The brainstorm command is /sc:brainstorm, which is a generative command. Nothing in the prompt verifies that the brainstorm output actually contains file/line references. The original says "actionable proposals at improvements of the relevant code" -- this implies code-level specificity, but the generated prompt relies entirely on the brainstorm command honoring its instructions. There is no validation step.

More critically, the prompt says "in src/superclaude/cli/roadmap/ and src/superclaude/cli/audit/" -- this scopes proposals to only two directories. But the pipeline depends on code in other locations: `src/superclaude/execution/parallel.py` (wave orchestration), `src/superclaude/pm_agent/` (confidence checks), and potentially the skill files themselves. If the root cause of a poor delta is in parallel.py, the scope restriction would prevent the brainstorm from proposing the correct fix.

**4. Report exhaustiveness: Missing critical sections**

Six sections is not exhaustive. What is missing:

- **Error/failure log**: If any run crashed, errored, or timed out, where is that recorded? The report assumes all 4 runs completed successfully. There is no section for partial failures.
- **Timing comparison**: Prompt 5 records wall-clock time for each run. Prompt 6's report has no timing section. Performance is a dimension of pipeline quality.
- **Stage-level artifact quality assessment**: The report has artifact inventory (exists/missing, line count) but no quality assessment. A spec-fidelity report could exist, have 50 lines, and contain nothing but boilerplate headers. Line count is not quality.
- **Methodology section**: An exhaustive report should describe how it was produced, what framework was applied, what the inputs were. A third party reading eval-report.md should not need to also read scoring-framework.md to understand the methodology.
- **Raw data appendix**: The report should include or link to the raw scoring data so the conclusions can be independently verified.

**5. Dependency chain: Fail-fast is not enough**

Expert A says missing upstream artifacts will cause "visible failure." But "visible" to whom? If Prompt 6 is run by a Claude agent, a missing file will produce a tool error, and the agent may improvise -- generating a report based on whatever it can find rather than failing cleanly. The prompt should include an explicit precondition check: "Before proceeding, verify that all 4 eval-run directories exist and contain artifacts, and that scoring-framework.md exists. If any are missing, STOP and report which prerequisites are unmet."

Furthermore, if scoring-framework.md exists but is malformed (e.g., the adversarial review in Prompt 5 Phase 3 identified critical issues that were not fixed), the prompt has no validation step. It says "Read the scoring framework and apply it" -- but what if the framework is self-contradictory or incomplete?

**6. Happy path: Useful but under-specified**

The happy path says: "Report 'v3.0 Unified Audit Gating validated' and skip the brainstorm." This is a single sentence. If results are genuinely all positive, the report is the deliverable, not the brainstorm. But the happy path produces no additional analysis. An exhaustive report for positive results should still include: confidence intervals on the deltas, which stages showed the largest improvement, and recommendations for what to test next. "All good, skip brainstorm" is premature closure.

The original does not mention a happy path because the original frames Prompt 6 as a reporting prompt. The report is always produced regardless of results. The brainstorm is conditional. The happy path in the generated prompt conflates "skip brainstorm" with "stop working," when it should mean "produce the full report, then skip the brainstorm."

---

## ROUND 2: Rebuttals

### Expert A (Rebuttal)

**On fidelity (point 1)**: Expert B raises a legitimate concern about Step 2 pre-specifying delta computation. I concede that Step 2's "Local average score vs Global average score = delta" could conflict with the scoring framework's methodology. However, I note that Prompt 5 instructs the framework to "Define how to compute v3.0-vs-master delta for each metric" (line 203). The generated Prompt 6's Step 2 is describing the same operation in less precise language. The intent is aligned; the phrasing creates ambiguity about authority. The fix is simple: change Step 2 to say "Apply the delta computation method defined in the scoring framework" rather than prescribing a specific formula. This is a wording defect, not a design defect.

**On condition (c) -- reproducibility**: Expert B argues that low reproducibility is not a "poor result." I disagree. If v3.0 produces wildly different outputs on consecutive runs with the same input, that is a regression in pipeline reliability. The user's original objective includes evaluating "impact" -- and negative impact on reliability is impact. However, I concede that 80% as a threshold is arbitrary. The scoring framework should define reproducibility thresholds, and Prompt 6 should reference them rather than hardcoding 80%.

**On condition (b) -- any single negative delta**: Expert B's objection is valid. A single -0.01 delta should not trigger a full brainstorm. However, I note that the brainstorm's requirement 2 says "Each proposal must target a specific negative delta from the eval report." If there is only one trivially negative delta, the brainstorm would need to produce 5 proposals targeting it, which is wasteful. A materiality threshold would improve this. But the original objective says "poor results/deltas" without defining materiality, so the generated prompt is at least consistent with the original's lack of precision.

**On code proposal scope (point 3)**: Expert B notes the scope is limited to two directories. This is a valid observation. The pipeline orchestration logic in `executor.py` calls into other modules. If the root cause is in `parallel.py`, the brainstorm would be artificially constrained. I concede this should say "in the superclaude package, particularly src/superclaude/cli/roadmap/ and src/superclaude/cli/audit/" rather than exclusively scoping to those directories.

**On exhaustiveness (point 4)**: Expert B identifies 5 missing sections. I concede that error/failure logging and timing comparison are genuine gaps. However, "methodology section" and "raw data appendix" are meta-sections that any reporting agent would naturally include. The prompt does not need to enumerate every section of a report to get a good report -- it needs to specify the sections that are non-obvious or domain-specific. The 6 specified sections cover the domain-specific requirements; general report quality is an agent capability, not a prompt requirement.

**On dependency validation (point 5)**: Expert B's suggestion of an explicit precondition check is a genuine improvement. I concede this point. The prompt should include a Phase 0 that validates upstream artifacts exist before beginning scoring.

**On happy path (point 6)**: Expert B argues the happy path conflates "skip brainstorm" with "stop working." Re-reading the generated prompt, Step 3 (produce exhaustive report) is unconditional. Step 4 is the conditional. The happy path only applies to Step 4. The report is always produced. Expert B's concern that "the report is the deliverable" is already addressed by the prompt's structure. However, I concede that the happy-path message is too terse. A validation-pass declaration should include a summary of the evidence (which deltas, what reproducibility scores) rather than a single sentence.

### Expert B (Rebuttal)

**On fidelity**: Expert A concedes the wording defect. I accept this as a convergence point. The fix is clear: Prompt 6 Step 2 should defer to the scoring framework's computation methodology rather than prescribing its own. This is the single most important finding of this debate because it determines whether the adversarial review of the scoring framework (Prompt 5, Phase 3) has any downstream effect. If Prompt 6 ignores the framework and uses its own formula, the entire Phase 3 adversarial review was wasted effort.

**On reproducibility**: Expert A's argument that unreliable results are poor results has merit. I maintain that the threshold should come from the scoring framework, not be hardcoded. We converge on this.

**On condition (b)**: Expert A concedes the any-single-negative trigger is too sensitive but defends it as consistent with the original's imprecision. I accept that the original objective is vague here. The generated prompt made a reasonable operationalization choice, even if it errs on the side of over-triggering. The downstream effect is manageable: the brainstorm will be invoked more often than necessary, but the proposals must target specific deltas, so they will at least be grounded.

**On exhaustiveness**: Expert A argues that general report sections are "agent capability." This is a dangerous assumption. The reason Prompt 6 exists as a detailed prompt rather than "score the evals and write a report" is precisely because relying on agent capability produces inconsistent results. The previous eval attempt (rejected -- 168 pytest tests, zero real artifacts) demonstrated that agents optimize for what is specified and skip what is not. If timing is not specified, it will not appear in the report. If error handling is not specified, partial failures will be silently ignored.

I maintain that the following sections should be explicitly required:
- **Errors and partial failures**: What happened if a run did not complete all 13 stages?
- **Timing**: Wall-clock per run, per stage if available.

I withdraw the objection on "methodology section" and "raw data appendix" as those are presentation concerns.

**On dependency validation**: Expert A concedes. We converge.

**On happy path**: Expert A clarifies that Step 3 is unconditional and Step 4 is conditional. Re-reading, this is correct. The report is always produced. My concern was based on a misreading of the flow. I withdraw the structural objection but maintain that the happy-path declaration should include evidence citations from the report, not just a bare assertion.

---

## ROUND 3: Convergence Assessment

### Agreed Findings (Converged)

| # | Finding | Severity | Recommendation |
|---|---------|----------|----------------|
| F1 | Step 2 pre-specifies delta computation instead of deferring to scoring framework | HIGH | Change Step 2 to: "Apply the delta computation and threshold definitions from the scoring framework" rather than prescribing "Local avg vs Global avg = delta" |
| F2 | Condition thresholds (80% reproducibility, any single negative delta) should come from the scoring framework, not be hardcoded | MEDIUM | Replace hardcoded thresholds with references to scoring-framework.md thresholds |
| F3 | Code proposal scope is artificially limited to two directories | MEDIUM | Change "in src/superclaude/cli/roadmap/ and src/superclaude/cli/audit/" to "in the superclaude package (particularly cli/roadmap/ and cli/audit/)" |
| F4 | No precondition check for upstream artifacts | MEDIUM | Add a Step 0: verify eval-runs/{local-A,local-B,global-A,global-B}/ and scoring-framework.md exist before proceeding |
| F5 | Report missing error/failure and timing sections | MEDIUM | Add two required report sections: (7) errors and partial failures per run, (8) wall-clock timing per run |
| F6 | Happy-path declaration is too terse | LOW | Require the happy-path message to cite specific evidence (overall delta value, reproducibility percentages, stage counts) |

### Contested Findings (Not Converged)

| # | Finding | Expert A Position | Expert B Position |
|---|---------|-------------------|-------------------|
| C1 | Condition (b) "any individual stage negative delta" triggers brainstorm | Consistent with original's imprecision; over-triggering is acceptable since proposals must target specific deltas | A materiality threshold (e.g., delta < -5% or -0.1) should be added to avoid wasting brainstorm on noise |
| C2 | No validation that brainstorm output actually contains file/line references | Agent capability -- the instruction is clear enough | Should include a post-brainstorm verification step: check each proposal for file path and line number |
| C3 | Report does not require stage-level quality assessment beyond line counts | Line count + gate pass/fail is sufficient signal for a scoring report; quality is subjective | A qualitative grade (A/B/C/D/F per artifact) based on the scoring framework's quality indicators would make the report genuinely exhaustive |

### Overall Fidelity Verdict

**Score: 7.5/10 -- Faithful with material gaps**

The generated Prompt 6 captures the original objective's intent: apply the scoring framework, produce an exhaustive report, conditionally brainstorm improvements. The structural flow (score -> delta -> report -> conditional brainstorm) is correct. The conditional brainstorm logic is a reasonable operationalization of "poor results/deltas." The code-specificity requirements for proposals are strong.

The most significant defect is F1: the prompt partially overrides the scoring framework it is supposed to apply. This undermines the entire purpose of Prompt 5's adversarial review of the framework. If the framework specifies weighted deltas and Prompt 6 uses simple averages, the reviewed methodology is discarded. This is a design-level fidelity gap, not a cosmetic one.

The secondary defects (F2-F6) are implementable fixes that would bring the prompt to 9/10. The contested findings (C1-C3) represent judgment calls where the original objective is genuinely ambiguous.

### Recommended Revised Prompt 6 (Summary of Changes)

1. Add Step 0: precondition validation (F4)
2. Rewrite Step 2 to defer to scoring framework methodology (F1)
3. Replace hardcoded thresholds with framework references (F2)
4. Expand code proposal scope (F3)
5. Add error/timing sections to report requirements (F5)
6. Strengthen happy-path evidence citation (F6)
