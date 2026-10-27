# Adversarial Debate: Prompt 3 Fidelity Review

**Date**: 2026-03-19
**Format**: Structured adversarial debate (6 axes)
**Expert A**: Defender (argues the generated prompt faithfully serves the original intent)
**Expert B**: Challenger (identifies deviations, omissions, and structural risks)
**Subject**: Generated Prompt 3 vs. original objective from 6PromptV3-Eval.md

---

## Axis 1: Skill Chain Fidelity

**Original specifies**: /sc:analyze -> /sc:brainstorm -> /sc:design -> /sc:reflect
**Generated prompt chains**: /sc:analyze -> /sc:brainstorm -> /sc:design -> /sc:reflect

### Expert A (Defender)

The chain ordering is exact. The generated prompt invokes all four skills in the correct sequence with explicit "After X completes, invoke Y" transitions. Each skill receives a distinct payload: analyze gets file references and a question, brainstorm gets a topic string and constraints, design gets a type/format/deliverable, reflect gets a file reference for verification. This is a faithful rendering.

### Expert B (Challenger)

The ordering is correct, but the generated prompt converts what the original describes as a *flowing* sequence into a *scripted batch* with rigid "After X, invoke Y" imperatives. The original reads as a narrative workflow: "After the analysis is done, /sc:brainstorm must be invoked." The generated prompt reads as a four-stage script with explicit post-conditions. This is not a fidelity problem per se, but it changes the failure mode: the original allows an agent to adaptively decide when "analysis is done," while the generated prompt implies a hard handoff. In practice, Claude Code will treat both the same way -- but the prescriptive phrasing in the generated prompt increases the risk that an agent will mechanically trigger the next skill even if the preceding output was incomplete or low-quality.

### Resolution

**Verdict: PASS with caveat.** Chain order is faithful. The shift from narrative to imperative framing is a minor style change, not a fidelity violation. However, the prescriptive framing does reduce adaptive resilience (see Axis 6).

---

## Axis 2: "3 Issues It Mitigates"

**Original says**: "determines the top 3 biggest impacts it serves, summarize 3 issues that it mitigates against the most"
**Generated prompt says**: "Determine the top 3 biggest impacts... For each impact: 1. What specific pipeline behavior changed 2. What failure mode does it mitigate 3. What measurable evidence would demonstrate the impact"

### Expert A (Defender)

The original uses two phrases: "top 3 biggest impacts" and "3 issues that it mitigates." These are semantically entangled -- an "impact" in the context of a gating release *is* a mitigation of a failure mode. The generated prompt correctly unifies them by asking for 3 impacts and requiring each to specify "what failure mode does it mitigate." This is a structural improvement: it eliminates the ambiguity of whether "3 impacts" and "3 issues" are the same list or different lists. The answer to "what failure mode does it mitigate" *is* the "issue it mitigates."

### Expert B (Challenger)

This is the most significant fidelity deviation in the entire prompt. The original says TWO things:

1. "determines the top 3 biggest impacts it serves" -- what v3.0 adds
2. "summarize 3 issues that it mitigates against the most" -- what problems existed before

These could be the same 3 items, but the original phrasing treats them as separate deliverables: first identify impacts, then summarize the issues those impacts address. The generated prompt collapses this into a single list where mitigation is a sub-property of each impact. This matters because:

- The original could have intended 3 impacts + 3 separate issues (6 items total). The "summarize 3 issues" clause is grammatically distinct.
- Even if the same 3 items, the original wants a *summary of issues* as a distinct output artifact, not just a sub-bullet. A summary of "issues the pipeline had before v3.0" frames the analysis around *problems*, while "failure mode each impact mitigates" frames it around *solutions*.

The framing difference propagates downstream: the brainstorm and design steps build on the analyze output. If the analyze step produces solution-framed output instead of problem-framed output, the evals may test "does v3.0 work" rather than "does v3.0 prevent the specific failures we identified."

### Resolution

**Verdict: MINOR DEVIATION.** The merger is defensible as a structural improvement -- it avoids the ambiguity of whether 6 or 3 items were intended. But it does sacrifice the problem-framing lens that the original's "summarize 3 issues" clause intended. The downstream effect is non-trivial: evals designed around "impacts" are naturally success-oriented, while evals designed around "issues mitigated" are naturally failure-detection-oriented. For an audit gating system, failure-detection framing is more valuable.

**Recommendation**: Add to the /sc:analyze section: "For each impact, also provide a standalone summary of the pre-v3.0 issue it addresses -- what went wrong, how frequently, and what evidence existed of the failure."

---

## Axis 3: Brainstorm Scope Boundary

**Original says**: "This should be a brief spec, not the actual design."
**Generated prompt says**: "Brief spec only, not the full design" (in brainstorm requirements)

### Expert A (Defender)

The generated prompt explicitly states "Brief spec only, not the full design" as a constraint in the brainstorm requirements list. It also provides concrete boundaries: every eval must invoke `superclaude roadmap run`, must produce disk artifacts, must be A/B-comparable, must use the eval spec from Prompt 1, and must write to specific output paths. These constraints define the brainstorm's scope without allowing it to become a design. The boundary is well-enforced.

### Expert B (Challenger)

The phrase "Brief spec only, not the full design" is present, but the five requirements that follow it are already design-level constraints:

- "Every eval MUST invoke `superclaude roadmap run` with real Claude subprocess calls" -- this is an implementation constraint, not a spec-level concern
- "Output artifacts go to .dev/.../eval-runs/local/ and eval-runs/global/" -- specifying output paths is design work

A brainstorm that must conform to 5 rigid requirements is not a brainstorm. It is a constrained design brief. The original intended the brainstorm to *explore* the best ways to measure v3.0's impact, then hand off to /sc:design for the structured work. The generated prompt pre-loads the brainstorm with design decisions (subprocess calls, disk paths, A/B structure) that should have been discovered *during* the brainstorm or deferred to design.

This is a scope leak in the wrong direction: rather than the brainstorm bleeding into design, the design has bled *backwards* into the brainstorm, constraining the exploration space.

### Expert A (Rebuttal)

These constraints come from the broader eval context -- specifically the rejection of previous evals for being mocked unit tests. Without these constraints, the brainstorm could produce a spec that repeats the same mistake. The constraints are guardrails, not design decisions. They say *what kind* of evals are acceptable, not *how* to build them.

### Resolution

**Verdict: ACCEPTABLE DEVIATION.** The constraints are contextually necessary to prevent the known failure mode (mocked evals). However, the brainstorm's exploratory value is diminished. A purer approach would state: "The brainstorm must assume all evals invoke the real pipeline and produce real artifacts" as a premise, then let the brainstorm explore *how* -- rather than dictating subprocess calls and output paths.

---

## Axis 4: Design vs. "Design and Build"

**Original says**: "invoked /sc:design to design and build 3 evals"
**Generated prompt says**: "Build 3 end-to-end evals that demonstrate the top 3 v3.0 impacts" (design topic) + "Write the design to: ...eval-e2e-design.md" (output)

### Expert A (Defender)

The generated prompt's /sc:design invocation says "Build 3 end-to-end evals" in its topic string, which captures the "build" intent. The `--type component --format spec` flags tell the skill to produce a component-level specification. The output is written to a .md file, which is a design document. The /sc:design skill is a *design* skill -- it produces specifications and architecture documents, not executable code. Asking it to "build" Python scripts would be a misuse of the skill. The correct interpretation is that "design and build" in the original means "design the evals completely enough that they can be built," not "write the Python files in this step."

The generated prompt also specifies that evals must "be runnable as: `uv run python scripts/eval_{N}.py --branch local`" -- this is an interface contract, not the implementation itself. The actual implementation would happen in a subsequent step (Prompt 5 spawns agents to run the evals, implying they need to exist by then).

### Expert B (Challenger)

The original says "design and build." That is a compound verb. If the intent were design-only, it would say "design 3 evals." The word "build" means produce the artifacts. Looking at the prompt suite holistically:

- Prompt 3: design AND build the evals
- Prompt 5: run the evals

If Prompt 3 only designs, then who builds? There is no Prompt 3.5. Prompt 4 is /sc:reflect for validation -- it does not build. Prompt 5 assumes the evals exist and runs them. The generated prompt creates a gap: it produces eval-e2e-design.md but no eval_1.py, eval_2.py, eval_3.py. Either the generated prompt needs to also produce the scripts, or the prompt suite has a gap.

The generated prompt references `scripts/eval_{N}.py` as a runnable path, implicitly assuming these files will exist. But it never creates them.

### Expert A (Rebuttal)

The /sc:design skill should produce a specification that is detailed enough to be directly implementable. The `--format spec` flag explicitly requests a specification document, not executable code. If the intent is to also produce Python files, that is a /sc:implement invocation, not /sc:design. The generated prompt is correct to scope /sc:design to its intended purpose. The gap -- who writes the actual scripts -- is a prompt-suite-level issue, not a Prompt 3 issue.

### Resolution

**Verdict: DEVIATION -- AMBIGUOUS SEVERITY.** The generated prompt captures the "design" half but drops the "build" half. This is defensible if /sc:design should only design, but it creates a real gap in the prompt suite: no step between Prompt 3 and Prompt 5 produces the actual eval scripts. Either:

1. Prompt 3's /sc:design should be followed by a code-generation step (possibly /sc:implement or direct file writing), or
2. The eval-e2e-design.md must be detailed enough that Prompt 5's agents can self-implement from the spec.

The generated prompt partially addresses option 2 by specifying detailed runnable interface contracts (`uv run python scripts/eval_{N}.py --branch local`), but this is insufficient for agents to produce working scripts without additional design details (imports, assertion logic, artifact parsing).

**Recommendation**: Either add an explicit implementation step after /sc:design, or add to the design requirements: "Each eval design must include: complete Python pseudocode, expected CLI invocations, artifact schemas, and assertion criteria -- sufficient for direct implementation without further design decisions."

---

## Axis 5: Reflect Scope and Nuance

**Original says**: "verify the designs to ensure they do not deviate in the spec, unless those deviations are deemed a better approach"
**Generated prompt says**: "Verify the 3 eval designs do not deviate from the brainstorm spec, and that any deviations are improvements"

### Expert A (Defender)

The generated /sc:reflect invocation captures both halves of the original's nuance: (1) check for deviations from the spec, and (2) determine if deviations are improvements. It also provides the file reference (@eval-e2e-design.md) as concrete input for the reflection. The phrasing "any deviations are improvements" is a faithful compression of "unless those deviations are deemed a better approach."

### Expert B (Challenger)

The generated prompt narrows the reflection scope by specifying "do not deviate from the brainstorm spec." The original says "do not deviate in the spec" -- which is ambiguous but could mean the *overall* eval spec (from Prompt 1), not just the brainstorm output. If /sc:reflect only checks against the brainstorm, it misses drift from the Prompt 1 eval spec entirely.

Additionally, the generated /sc:reflect only receives one file reference (eval-e2e-design.md). To properly verify non-deviation, it should also receive the brainstorm output and the original eval spec. Without those references, the reflect agent must either recall them from context (unreliable across skill boundaries) or operate with incomplete information.

### Expert A (Rebuttal)

The brainstorm spec *subsumes* the eval spec -- it was produced by brainstorming against the eval spec as input. Checking against the brainstorm is checking against a refined version of the eval spec. As for file references, the /sc:reflect skill will have the full conversation context, including all prior skill outputs.

### Resolution

**Verdict: MINOR DEVIATION.** The generated prompt's reflect scope is slightly narrower than intended. The original's "in the spec" likely means the brainstorm spec, so the generated prompt's interpretation is reasonable. However, the single file reference is a weakness -- adding the brainstorm output and Prompt 1 eval spec as additional @ references would make the reflection more robust.

**Recommendation**: Add file references to the reflect invocation: `@.dev/.../eval-spec.md` (from Prompt 1) and the brainstorm output path.

---

## Axis 6: Cascading Failure Risk

### Expert B (Challenger -- opening)

This is the most serious structural risk in Prompt 3. The chain is: analyze -> brainstorm -> design -> reflect. Each step depends on the quality of the preceding step's output. The failure modes are:

**Failure Mode 1: Weak /sc:analyze output**
If /sc:analyze produces generic impacts (e.g., "v3.0 improves pipeline quality") instead of specific, measurable ones (e.g., "spec-fidelity gate catches frontmatter field omissions that previously caused silent gate passes in 23% of roadmap runs"), then:
- The brainstorm has no concrete targets to design around
- The design produces evals that test vague properties
- The reflect step finds no deviations because there was nothing specific to deviate from

**Failure Mode 2: Brainstorm scope leak**
If the brainstorm ignores the "brief spec only" constraint and produces a full design, then:
- /sc:design has nothing to add -- it either duplicates the brainstorm or contradicts it
- /sc:reflect compares two nearly-identical documents and finds no deviations

**Failure Mode 3: Context window pressure**
By the time /sc:reflect fires, the conversation contains:
- 5 @ file references from /sc:analyze (merged-spec.md alone is ~47K characters)
- Full analyze output
- Full brainstorm output with constraints
- Full design output written to eval-e2e-design.md
- The reflect prompt itself

This is substantial context pressure. The @ references in /sc:analyze (merged-spec.md at ~47K chars, gates.py at ~29K, executor.py size unknown, convergence.py at ~12K, wiring_gate.py at ~38K) total roughly 130K+ characters of source material before any skill output is generated. By the fourth skill invocation, important details from the analyze phase may be outside the effective attention window.

**Failure Mode 4: No intermediate checkpoints**
There is no mechanism to validate intermediate outputs before proceeding. If /sc:analyze identifies the wrong 3 impacts, the entire downstream chain is poisoned. The original prompt suite design assumes each prompt is run as a separate conversation -- but Prompt 3 runs 4 skills *within* a single conversation with no human checkpoint between them.

### Expert A (Defender)

These are legitimate concerns, but they apply to *any* multi-skill chain, not specifically to this prompt. The mitigations are:

1. **Specificity of analyze input**: The generated prompt provides 5 specific file references, not vague instructions. The analyze step has concrete code to examine.
2. **Brainstorm constraints**: The "brief spec only" boundary is explicitly stated.
3. **Context window**: Claude Code with Opus 4.6 (1M context) can handle this volume. The @ references are loaded as tool results, not inline text.
4. **Reflect as catch-all**: The final /sc:reflect step exists precisely to catch cascade failures. If the design deviated from what the brainstorm specified, reflect flags it.

### Expert B (Rebuttal)

Reflect cannot catch what analyze got wrong. If analyze identifies the wrong 3 impacts, reflect only checks whether the design matches the brainstorm -- which was built on the wrong impacts. Reflect validates internal consistency, not external correctness.

The real mitigation would be to structure the prompt so that /sc:analyze produces a constrained, verifiable output (e.g., "for each impact, cite the specific gate function, the specific failure it catches, and the specific test gap it fills") rather than leaving the output format open-ended. The generated prompt partially does this with its 3-part structure (behavior change, failure mode, measurable evidence), but "measurable evidence" is vague enough to invite hand-waving.

### Resolution

**Verdict: SIGNIFICANT RISK.** The 4-skill chain has no intermediate validation and no recovery path if early steps produce weak output. The generated prompt mitigates this better than the original (by providing structured output requirements for analyze), but the fundamental risk remains.

**Recommendations**:
1. Add to the /sc:analyze requirements: "Each impact must cite specific function names, file paths, and line numbers in the referenced code. Generic statements like 'improves quality' are not acceptable."
2. Add a validation gate between analyze and brainstorm: "Before proceeding to brainstorm, verify that each of the 3 impacts has a concrete code reference and a testable failure condition."
3. Consider splitting Prompt 3 into two conversations: analyze+brainstorm in one, design+reflect in another (with the brainstorm output as input to the second).

---

## Summary Scorecard

| Axis | Verdict | Severity |
|------|---------|----------|
| 1. Skill chain fidelity | PASS | None |
| 2. "3 issues it mitigates" | MINOR DEVIATION | Low-Medium |
| 3. Brainstorm scope boundary | ACCEPTABLE DEVIATION | Low |
| 4. Design vs. "design and build" | DEVIATION | Medium |
| 5. Reflect scope | MINOR DEVIATION | Low |
| 6. Cascading failure risk | SIGNIFICANT RISK | High |

**Overall assessment**: The generated Prompt 3 is a competent rendering of the original objective with one structural gap (missing "build" step) and one significant risk (cascading failure in a 4-skill chain with no intermediate checkpoints). The merging of "impacts" and "issues mitigated" is defensible but shifts the eval framing from failure-detection to success-validation, which is suboptimal for an audit gating system.

**Top 3 recommended fixes (priority order)**:

1. **Address the build gap**: Either add an implementation step after /sc:design or require the design spec to include complete pseudocode sufficient for direct implementation.
2. **Add specificity constraints to /sc:analyze**: Require code-level citations (function names, file paths) for each identified impact to prevent vague outputs from poisoning the chain.
3. **Restore problem-framing for issue mitigation**: Add a distinct "summarize the pre-v3.0 issue" requirement to each impact, separate from the "failure mode mitigated" sub-bullet, to ensure the analyze output captures the problem space independently.
