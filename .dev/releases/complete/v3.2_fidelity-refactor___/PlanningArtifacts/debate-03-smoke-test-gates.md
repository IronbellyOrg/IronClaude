---
type: adversarial-debate
id: debate-03
title: "Test Requirement ID Extraction and Cross-Reference Gate (A1)"
date: 2026-03-17
source: brainstorm-03-smoke-test-gates.md
scoring_framework: scoring-framework.md
forensic_report: cli-portify-executor-noop-forensic-report.md
proposal: A1
---

# Adversarial Debate: Test Requirement ID Extraction and Cross-Reference Gate

## Proposal Under Review

**Solution A1** from brainstorm-03: Parse all test identifiers from spec extraction (`test_*` function names, E2E scenario names, `IT-NNN`/`ST-NNN` IDs) and emit as `test_requirements` list in extraction frontmatter. Add a new `SemanticCheck` on `SPEC_FIDELITY_GATE` that verifies every `test_requirements` entry appears in the merged roadmap body text. Missing entries cause blocking failure.

**Integration**: Two changes: (1) `EXTRACT_GATE` in `roadmap/gates.py` gets a new `test_requirements` frontmatter field; extraction prompt in `roadmap/prompts.py` updated. (2) `SPEC_FIDELITY_GATE` gets a new `SemanticCheck` cross-referencing `test_requirements` against roadmap content.

---

## Round 1: Opening Arguments

### Advocate

This proposal directly addresses the primary root cause identified in the forensic report (Section 9): the spec's `test_programmatic_step_routing` integration test was dropped at the Spec-to-Roadmap boundary and no gate caught it. A1 would have caught that exact failure. Here is why it should be implemented.

**1. Specific bug scenarios caught.**

The forensic report documents that the v2.25 spec defined `test_programmatic_step_routing` in Section 6 ("Executor Design") and E2E sample runs in Section 8 ("Validation"). The roadmap reduced this to "sequential pipeline runs end-to-end with mocked steps" (Milestone M2). The `SPEC_FIDELITY_GATE` missed the omission because it relies entirely on LLM-generated severity reports -- there are no programmatic cross-reference checks (forensic report Section 5, "What Neither Gate Does").

A1 closes this gap with a deterministic mechanism. During extraction, a regex pass identifies `test_programmatic_step_routing` as a `test_*` identifier. It enters the `test_requirements` list in extraction frontmatter. After roadmap generation and merge, the new `SemanticCheck` scans the merged roadmap body for each entry. The string `test_programmatic_step_routing` does not appear anywhere in the cli-portify roadmap -- the check fails, the gate blocks, and the pipeline halts with an explicit error listing the missing test requirement.

This catches the general pattern class: any named test, E2E scenario, or smoke test requirement that gets silently dropped during roadmap generation. The forensic report identifies this as the "defined but not wired" pattern (Section 7), which recurs across `DEVIATION_ANALYSIS_GATE`, trailing gate, and `SprintGatePolicy`. A1 would not catch all instances of "defined but not wired," but it catches the specific subclass where test requirements are the thing being dropped.

**2. Integration path into existing infrastructure.**

The integration is minimal and follows established patterns. The `EXTRACT_GATE` in `roadmap/gates.py:523-541` already requires 13 frontmatter fields including `functional_requirements`, `nonfunctional_requirements`, and `success_criteria_count`. Adding `test_requirements` as a 14th field is a one-line change to the `required_frontmatter_fields` list. The extraction prompt in `roadmap/prompts.py` already instructs the LLM to count functional and nonfunctional requirements -- adding an instruction to enumerate test identifiers is a prompt paragraph addition.

The new `SemanticCheck` on `SPEC_FIDELITY_GATE` follows the exact pattern used by `_high_severity_count_zero` and `_tasklist_ready_consistent` at `gates.py:644-655`. It receives the content string, parses frontmatter for `test_requirements`, reads the roadmap body, and returns a boolean. The `SemanticCheck` dataclass is already imported and used extensively -- the check function is approximately 20-30 lines of Python including frontmatter parsing and string matching.

Total estimated changes: 1 new frontmatter field on `EXTRACT_GATE`, 1 prompt paragraph in `prompts.py`, 1 new semantic check function (~30 lines), 1 new `SemanticCheck` instance on `SPEC_FIDELITY_GATE`. This is well within the 50-200 line range for a score of 7-8 on implementation complexity.

**3. Composability with other top proposals.**

A1 is the natural upstream complement to B3 (Bidirectional Traceability ID Enforcement). A1 extracts test requirement IDs at the Spec-to-Roadmap boundary; B3 enforces those same IDs at the Roadmap-to-Tasklist boundary. Together they form a deterministic end-to-end chain: spec test IDs are extracted, verified in the roadmap, then verified again in the tasklist. The brainstorm document itself identifies A1+B3 as the strongest pairing (Cross-Cutting Considerations table).

A1 also strengthens A2 (Test Strategy Section Mandatory Inclusion). If the roadmap is required to have a Test Strategy section (A2) and every extracted test ID must appear in the roadmap (A1), then the Test Strategy section becomes the natural home for those IDs, making both checks mutually reinforcing.

The `test_requirements` list emitted by A1 in extraction frontmatter is a reusable data structure. Any downstream gate -- B1, B3, B4 -- can consume it rather than re-parsing the spec. This makes A1 an infrastructure investment, not just a standalone check.

---

### Skeptic

A1 is a reasonable idea with a clean integration path, but its effectiveness is overstated and its maintenance trajectory is concerning. Let me challenge each claim.

**1. Failure modes where A1 would NOT catch bugs.**

A1 catches named test identifiers. The forensic report's primary root cause is not merely that `test_programmatic_step_routing` was dropped -- it is that the spec's three-way dispatch design (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`) was reduced to "sequential execution with mocked steps." This is a functional requirement failure, not a test requirement failure. The test was a symptom; the disease was the dropped dispatch architecture.

Consider the counterfactual: if A1 existed and caught the missing test name, the LLM could satisfy the gate by inserting a reference to `test_programmatic_step_routing` in the roadmap without actually preserving the dispatch design. The roadmap might say "Phase 4: Write test_programmatic_step_routing to verify step execution" while still specifying "mocked steps" as the execution model. The gate passes because the string appears in the roadmap text. The bug persists because the test, when written against the mocked-step design, would itself be a no-op.

More critically, A1 depends entirely on the extraction prompt correctly identifying test requirements from free-form spec text. The brainstorm document acknowledges this limitation: "Tests described in prose without identifiable names (e.g., 'verify the pipeline works') may not be captured." Many critical test requirements are expressed as prose descriptions or acceptance criteria, not as `test_*` function names. The v2.25 spec's E2E sample runs were described as narrative scenarios, not as named test functions. A regex for `test_*` would catch the function name but miss the broader testing intent.

The "defined but not wired" pattern class (forensic report Section 7) is about code component integration, not document-level test name preservation. `DEVIATION_ANALYSIS_GATE` being defined but unwired, trailing gate framework existing but uncalled, `SprintGatePolicy` existing as a stub -- none of these would be caught by test requirement ID extraction because they are not test requirements. A1 catches one narrow subclass of the broader problem.

**2. False positive scenarios.**

Consider a spec that defines `test_config_validation` as a unit test for a config parser. The roadmap restructures the implementation so that config validation is handled by a shared utility, and the test is renamed to `test_shared_config_validation` or folded into a broader `test_pipeline_setup` integration test. A1 would flag `test_config_validation` as missing from the roadmap, even though its intent is fully covered under a different name. This is a false positive that blocks the pipeline.

Specs often define aspirational tests that are later determined to be unnecessary or redundant. A roadmap author who intentionally omits a test because it duplicates another test's coverage would be blocked by A1 with no override mechanism described in the proposal. The gate treats all omissions as failures, with no distinction between accidental drops and intentional consolidation.

The string-matching approach is brittle. If the roadmap references `test_programmatic_step_routing` in a footnote, a "deferred to future release" note, or a "not applicable" justification, the gate passes because the string is present -- regardless of whether the test will actually be implemented. Conversely, if the roadmap paraphrases the test as "verify programmatic step routing" without the exact `test_*` prefix, the gate may fail depending on how fuzzy the matching is.

**3. Maintenance burden over 5+ releases.**

The `test_requirements` extraction depends on the LLM prompt correctly identifying test identifiers. As spec formats evolve, the prompt will need updating. Specs may adopt new test naming conventions (`scenario_*`, `verify_*`, `check_*`), new ID schemas (`TC-NNN`, `VAL-NNN`), or structured test tables instead of inline references. Each format change requires prompt maintenance.

The semantic check function uses string matching against roadmap body text. As roadmaps grow in complexity and adopt new structural conventions (collapsible sections, appendices, linked sub-documents), the check must evolve to handle these formats. A check that works for today's single-file roadmap may break when roadmaps span multiple artifacts.

Over 5 releases, the extraction prompt and the matching logic will accumulate special cases and format-specific handling. This is the maintenance pattern that leads to the "easy to let drift" category (score 3-4 on maintainability).

**4. Simpler alternatives.**

The same benefit can be achieved by strengthening the existing `SPEC_FIDELITY_GATE` prompt. Instead of a new extraction field and a new semantic check, update the fidelity comparison prompt to explicitly instruct the LLM: "For every test or validation requirement in the spec, verify it appears in the roadmap. Classify any missing test as HIGH severity." This is a prompt-only change -- zero code, zero new infrastructure. It relies on LLM judgment (same as today), but with focused attention on test preservation (similar to A4's approach but without a second LLM pass).

The forensic report's Section 10 Mitigation 1 proposes this exact approach for `FR-NNN` and `NFR-NNN` identifiers. A1 adds test identifiers to this same mechanism. But the mechanism itself (programmatic ID extraction + string matching) could be implemented once for all ID types rather than as a test-specific gate. A broader "requirement ID cross-reference" gate would subsume A1 and catch functional requirement drops too.

---

## Round 2: Rebuttals

### Advocate Rebuttal

The Skeptic raises valid points but overweights edge cases relative to the core value proposition.

**On the counterfactual (LLM inserting test name without preserving design):** This is a real risk but is mitigated by composability. A1 does not operate in isolation -- it is designed to work with B3 (traceability enforcement) and the existing `SPEC_FIDELITY_GATE` (functional requirement checking). If the roadmap mentions `test_programmatic_step_routing` but specifies "mocked steps," the existing fidelity check should flag the functional divergence. A1 catches the case where the test disappears entirely; the existing gate catches the case where the design is wrong. Defense in depth.

**On prose test descriptions:** The Skeptic is correct that regex alone will not catch all test requirements. However, the extraction prompt is LLM-driven, not regex-only. The prompt instructs the LLM to identify test requirements, and the regex validates the LLM's output format. This is the same hybrid approach used for `functional_requirements` and `nonfunctional_requirements` in the current `EXTRACT_GATE`. Nobody argues those fields are useless because they might miss some requirements -- they catch most requirements and the fidelity gate catches the rest.

**On false positives from test renaming:** The proposal should include a fuzzy matching option for the semantic check -- not just exact string matching but also stemmed/normalized matching (e.g., `test_programmatic_step_routing` matches "programmatic step routing test" or "test for programmatic step routing"). This reduces false positives from paraphrasing while keeping the deterministic character. Additionally, the gate could emit warnings (non-blocking) for partial matches and errors (blocking) for zero matches.

**On the simpler alternative (prompt-only change):** The forensic report explicitly identifies this as the current approach's weakness. The `SPEC_FIDELITY_GATE` already instructs the LLM to compare across 5 dimensions. The LLM missed `test_programmatic_step_routing` anyway. Adding another prompt instruction to "pay more attention to tests" is exactly the kind of LLM-dependent fix that the forensic report warns against. The value of A1 is that its enforcement is deterministic -- the Python `SemanticCheck` function does not depend on LLM judgment. This is a qualitative improvement, not an incremental prompt tweak.

**On broader "requirement ID cross-reference":** I agree that A1 should be designed as a specialization of a broader ID cross-reference mechanism. The `test_requirements` field can coexist with `functional_requirements` and `nonfunctional_requirements` in the extraction frontmatter, and the semantic check pattern can be generalized. But starting with test requirements is strategically correct because this is the specific class that failed in the cli-portify case and because test requirements are structurally easier to identify (they have `test_*` names and test-specific vocabulary).

---

### Skeptic Rebuttal

**On defense in depth:** The Advocate concedes that A1 alone would not prevent the cli-portify bug if the LLM satisfies the gate superficially. The claim that "the existing fidelity check should flag the functional divergence" is precisely the mechanism that already failed. Stacking A1 on top of a gate that already missed the bug provides incremental safety, not definitive safety. The Advocate's own scoring should reflect this -- A1 is a contributor to a solution, not a solution.

**On fuzzy matching:** Adding fuzzy matching to the semantic check significantly increases implementation complexity and introduces its own false positive/negative tradeoffs. Stemming "test_programmatic_step_routing" to "programmatic step routing" and then matching against roadmap prose is a natural language processing task, not a simple string search. This pushes the implementation from "30 lines of Python" toward "100+ lines plus a normalization library or custom stemmer." The Advocate's original complexity estimate was based on exact string matching; fuzzy matching changes the calculus.

**On the prompt-only alternative being insufficient:** I accept that deterministic enforcement is qualitatively better than prompt-only. My point is not that the prompt-only approach is sufficient, but that the broader requirement ID cross-reference gate (Mitigation 1 from the forensic report) would subsume A1 and catch functional requirement drops as well. Implementing A1 as a standalone test-specific gate creates technical debt if the broader gate is implemented later -- the test-specific logic would need to be refactored into the general mechanism.

**On maintenance:** The Advocate did not address the 5+ release maintenance trajectory. I maintain that extraction prompt maintenance and format evolution will accumulate complexity. The Advocate's comparison to `functional_requirements` is apt but cuts both ways: those fields already exist and have presumably already accumulated format-specific handling. Adding `test_requirements` adds another field subject to the same drift.

---

## Round 3: Final Positions

### Advocate Final Position

A1 is not a silver bullet. It is a targeted, low-cost, deterministic check that closes a specific gap in the fidelity chain: test requirement preservation at the Spec-to-Roadmap boundary. Its value lies in three properties:

1. **Deterministic enforcement**: The `SemanticCheck` function is Python code, not LLM judgment. This is a qualitative upgrade over the current prompt-only approach.
2. **Low implementation cost**: ~100-150 lines total across prompt, gate definition, and check function. Follows existing `GateCriteria`/`SemanticCheck` patterns exactly.
3. **Infrastructure reuse**: The `test_requirements` frontmatter field becomes a shared data structure consumed by downstream gates (B1, B3, B4).

It would have caught the cli-portify bug at Link 1. It would not have caught the bug by itself if the LLM satisfied the gate superficially, but combined with the existing fidelity check and downstream gates (B3), it creates a multi-layered defense that makes silent test requirement drops significantly harder.

### Skeptic Final Position

A1 is a reasonable incremental improvement with a clean integration path, moderate effectiveness, and manageable but real maintenance costs. Its main weaknesses are:

1. **Narrow scope**: Catches named test identifiers only. Does not catch prose test descriptions, functional requirement drops, or the broader "defined but not wired" pattern.
2. **Satisfiable without substance**: An LLM can insert the test name into the roadmap without preserving the design intent, passing the gate while leaving the bug intact.
3. **Maintenance trajectory**: Prompt and format dependencies will accumulate over 5+ releases.
4. **Should be generalized**: Better implemented as part of a broader requirement ID cross-reference mechanism than as a test-specific gate.

It is a good proposal but not a great one. I would score it in the "implement after high-priority items" range.

---

## Dimension Scores

### 1. Likelihood to Succeed (Weight: 0.35)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 7 | Would catch the specific cli-portify failure (missing `test_programmatic_step_routing` string). Would catch similar named-test drops. Minor blind spots: prose tests, superficial LLM satisfaction. Requires 1 assumption (extraction prompt identifies the test name). |
| Skeptic | 6 | Would catch the string absence but not the design absence. LLM can satisfy gate without preserving intent. Only catches named test identifiers, not the broader failure class. Depends on extraction prompt quality. |

**Delta: 1 (within threshold). Final: 6.5**

### 2. Implementation Complexity (Weight: 0.25)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 8 | ~100-150 lines. 2-3 files modified (gates.py, prompts.py). No new dependencies. Follows existing SemanticCheck pattern exactly. New test fixtures needed but straightforward. |
| Skeptic | 7 | Base implementation is ~100 lines, but fuzzy matching (which the Advocate conceded is needed to reduce false positives) pushes toward 200+ lines. Prompt engineering for reliable test extraction is nontrivial. Testing the semantic check requires mock extraction outputs and mock roadmaps. |

**Delta: 1 (within threshold). Final: 7.5**

### 3. False Positive Risk (Weight: 0.15)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 7 | Deterministic string matching has clear semantics. False positives from renaming can be mitigated with fuzzy matching or a warning-vs-error distinction. Override mechanism (marking intentional omissions) could be added. |
| Skeptic | 5 | Test renaming, consolidation, and intentional omission are common scenarios. Exact string matching is brittle; fuzzy matching introduces its own errors. No override mechanism is described in the proposal. Sensitivity to document formatting is moderate -- roadmap structure affects where strings appear. |

**Delta: 2 (within threshold). Final: 6.0**

### 4. Maintainability (Weight: 0.15)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 7 | Auto-discovers test requirements from extraction (no manual config). Prompt updates needed only when test naming conventions change. Check function is pure Python with no external dependencies. Can be meta-tested by running extraction on known specs. |
| Skeptic | 5 | Extraction prompt must evolve with spec format changes. String matching must evolve with roadmap structural changes. Over 5 releases, accumulated format-specific handling creates drift. Should be generalized into broader ID cross-reference mechanism rather than maintained as standalone. |

**Delta: 2 (within threshold). Final: 6.0**

### 5. Composability (Weight: 0.10)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 9 | Directly enables B3 (bidirectional traceability). Provides `test_requirements` data structure consumed by B1, B3, B4. Reinforces A2 (test strategy section). Fits existing GateCriteria/SemanticCheck pattern. Identified as strongest pairing component in brainstorm cross-cutting analysis. |
| Skeptic | 7 | Complements B3 well. But the `test_requirements` field is test-specific; a generalized requirement ID field would be more composable. Partial overlap with A3 (test manifest) -- if A3 is also implemented, A1's extraction becomes redundant. |

**Delta: 2 (within threshold). Final: 8.0**

---

## Final Weighted Score

```
Score = (Success * 0.35) + (Complexity * 0.25) + (FalsePositive * 0.15) + (Maintainability * 0.15) + (Composability * 0.10)
```

| Dimension | Final Score | Weight | Weighted |
|-----------|------------|--------|----------|
| Likelihood to Succeed | 6.5 | 0.35 | 2.275 |
| Implementation Complexity | 7.5 | 0.25 | 1.875 |
| False Positive Risk | 6.0 | 0.15 | 0.900 |
| Maintainability | 6.0 | 0.15 | 0.900 |
| Composability | 8.0 | 0.10 | 0.800 |

**Weighted Total: 6.75**

**Interpretation**: Good candidate -- implement after high-priority items. A1 provides meaningful deterministic reinforcement at the Spec-to-Roadmap boundary with low implementation cost and strong composability. Its main limitations (narrow scope, superficial satisfaction risk, maintenance trajectory) keep it below the "strong candidate" threshold. Best deployed as part of the A1+B3 pairing rather than as a standalone gate.

---

## Recommendations

1. **Implement as part of a broader requirement ID cross-reference mechanism** rather than as a test-specific gate. Design the extraction frontmatter and semantic check to handle `FR-NNN`, `NFR-NNN`, and test identifiers in a unified framework.
2. **Include normalized/fuzzy matching** from the start to reduce false positives from test renaming and paraphrasing.
3. **Add an override mechanism** (e.g., `test_requirements_excluded` frontmatter field) for intentional omissions, with required justification.
4. **Pair with B3** (Bidirectional Traceability ID Enforcement) for end-to-end deterministic coverage across both fidelity chain links.
