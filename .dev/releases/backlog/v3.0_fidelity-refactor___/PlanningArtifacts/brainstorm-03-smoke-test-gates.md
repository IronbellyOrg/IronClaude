---
type: brainstorm
id: brainstorm-03
title: Smoke Test and Integration Test Fidelity Gates
date: 2026-03-17
context: cli-portify-executor-noop-forensic-report.md
scope: Spec-to-Roadmap test preservation + Roadmap-to-Tasklist test task coverage
solutions_count: 10
---

# Brainstorm 03: Smoke Test and Integration Test Fidelity Gates

## Problem Statement

The v2.25 cli-portify spec defined `test_programmatic_step_routing` and E2E smoke test requirements, but these were silently dropped during Spec-to-Roadmap generation and never appeared as executable tasklist tasks. The `SPEC_FIDELITY_GATE` (LLM-driven semantic comparison with deterministic frontmatter enforcement) did not detect this omission. The `TASKLIST_FIDELITY_GATE` passed vacuously because its parent (the roadmap) was already missing the requirements. The result: a no-op executor shipped as "complete" because no test was ever created to verify real step dispatch.

This brainstorm produces 10 solutions across two validation phases.

---

## Section A: Spec-to-Roadmap -- E2E/Smoke Test Preservation

These 5 solutions target the SPEC_FIDELITY_GATE and the roadmap generation pipeline to ensure that test requirements defined in specs survive into roadmap phases.

---

### A1: Test Requirement ID Extraction and Cross-Reference Gate

**Summary**: Parse all test identifiers from the spec extraction and programmatically verify each appears in the roadmap output.

**How it works**: A new semantic check function is added to the `SPEC_FIDELITY_GATE` in `roadmap/gates.py`. During the extract step, a regex pass identifies all test-like identifiers from the spec: function names matching `test_*`, named test scenarios (e.g., "E2E sample run N"), and explicit test requirement IDs (e.g., `IT-NNN`, `ST-NNN`). These are emitted as a `test_requirements` list in the extraction frontmatter. The new semantic check on the fidelity report then verifies that every entry in `test_requirements` appears somewhere in the merged roadmap body text. Missing entries cause the gate to fail with a list of unpreserved test requirements.

**What it would catch**: The exact failure observed -- `test_programmatic_step_routing` was defined in the v2.25 spec Section 6 but absent from the roadmap. Any named test, E2E scenario, or smoke test requirement that gets dropped during roadmap generation would trigger a blocking failure.

**Integration point**: Two changes: (1) `roadmap/gates.py` EXTRACT_GATE gets a new `test_requirements` frontmatter field; the extraction prompt is updated in `roadmap/prompts.py` to emit this field. (2) `SPEC_FIDELITY_GATE` gets a new `SemanticCheck` that cross-references spec `test_requirements` against roadmap content.

**Limitations**: Depends on the extraction prompt correctly identifying test requirements from free-form spec text. Tests described in prose without identifiable names (e.g., "verify the pipeline works") may not be captured. Only catches named/identifiable test requirements, not implicit testing expectations.

---

### A2: Test Strategy Section Mandatory Inclusion Gate

**Summary**: Require the merged roadmap to contain an explicit "Test Strategy" or "Validation Plan" section that accounts for every spec-defined test category (unit, integration, E2E, smoke).

**How it works**: A new semantic check is added to the `MERGE_GATE` in `roadmap/gates.py`. The check scans the merged roadmap for a heading matching `Test Strategy`, `Validation Plan`, or `Testing Requirements` (case-insensitive). Under this heading, the check verifies the presence of subsections or bullet items covering at least three test tiers: unit, integration/E2E, and smoke. The existing `TEST_STRATEGY_GATE` already requires `validation_milestones` and `interleave_ratio` in frontmatter, but it does not verify that spec-defined tests are enumerated. This solution strengthens it by requiring explicit test enumeration.

**What it would catch**: Roadmaps that reduce testing to vague statements like "mocked steps" without enumerating the specific tests the spec requires. The cli-portify roadmap's Milestone M2 said "sequential pipeline runs end-to-end with mocked steps" -- this would fail because it lacks an enumerated test plan that accounts for the spec's `test_programmatic_step_routing`.

**Integration point**: New `SemanticCheck` on `MERGE_GATE` or `TEST_STRATEGY_GATE` in `roadmap/gates.py`. Prompt update in `roadmap/prompts.py` to instruct the generation step to preserve and enumerate all spec-defined tests in the test strategy section.

**Limitations**: Structural check only -- verifies the section exists and mentions test tiers, but cannot deeply verify that every individual spec test is listed. A roadmap author (or LLM) could satisfy the gate with generic test categories while still omitting specific test names.

---

### A3: Spec Test Manifest with Diff-Based Fidelity Enforcement

**Summary**: Generate a structured test manifest from the spec, then diff it against the roadmap's test plan and block on any deletions.

**How it works**: A new pipeline micro-step runs between extraction and generation. It produces a `test-manifest.yaml` file listing every test requirement from the spec in structured form:

```yaml
tests:
  - id: test_programmatic_step_routing
    type: integration
    spec_section: "Section 6, Executor Design"
    description: "Programmatic steps call Python functions, not Claude subprocesses"
  - id: e2e_sample_run_1
    type: e2e
    spec_section: "Section 8, Validation"
    description: "Run pipeline against minimal workflow fixture"
```

After roadmap generation, a second micro-step diffs the test manifest against the roadmap. Each manifest entry must map to at least one roadmap phase, key action, or milestone. Unmapped entries produce a diff report. The spec fidelity gate checks this diff report: any unmapped test with type `integration` or `e2e` is classified as HIGH severity.

**What it would catch**: Any test requirement that is present in the spec but not mapped to a roadmap phase. This is the most precise solution because it operates on structured data rather than free-text matching. It would have caught `test_programmatic_step_routing` as an unmapped integration test.

**Integration point**: New micro-step between extract and generate in the roadmap pipeline (`roadmap/steps.py` or equivalent). New artifact `test-manifest.yaml` with its own `LIGHT`-tier gate for existence. Fidelity diff logic added as a semantic check on `SPEC_FIDELITY_GATE`.

**Limitations**: Adds pipeline complexity (new step, new artifact, new gate). The manifest generation itself is LLM-driven and could miss tests. Requires prompt engineering to reliably extract structured test data from free-form specs. The diff step must handle renamed or restructured tests without false positives.

---

### A4: Dual-Pass Fidelity Check with Test-Specific Prompt

**Summary**: Run two separate fidelity checks -- one for functional requirements (existing) and one specifically for test/validation requirements (new).

**How it works**: The current `SPEC_FIDELITY_GATE` runs a single LLM comparison across 5 dimensions. This solution splits it into two passes. Pass 1 is the existing general fidelity check (signatures, data models, gates, CLI options, NFRs). Pass 2 is a new test-specific fidelity check with a dedicated prompt that instructs the LLM to: (a) enumerate every test, validation scenario, and smoke test defined in the spec extraction, (b) for each, find its corresponding coverage in the roadmap, (c) classify any missing test as HIGH severity. Both passes produce separate fidelity reports. The gate requires both reports to have `high_severity_count == 0`.

**What it would catch**: Test requirements that get lost in the noise of a general fidelity comparison. The current single-pass approach evaluates tests alongside dozens of other requirements; the LLM may deprioritize test completeness when the functional design largely matches. A dedicated test-fidelity pass focuses LLM attention exclusively on test preservation, making omissions like `test_programmatic_step_routing` far more likely to be flagged.

**Integration point**: New prompt template in `roadmap/prompts.py` (`build_test_fidelity_prompt`). New `SemanticCheck` or second gate invocation in the spec-fidelity pipeline step. The pipeline executor in `pipeline/gates.py` would need to support compound gates (two reports, both must pass).

**Limitations**: Doubles LLM invocations for fidelity checking, increasing token cost and latency. Still LLM-dependent -- the test-specific prompt improves focus but does not guarantee completeness. Two reports mean two potential failure modes in gate enforcement logic.

---

### A5: Roadmap Phase Coverage Matrix with Test Row Enforcement

**Summary**: Require the roadmap to include a coverage matrix that explicitly maps every spec requirement category (including tests) to a roadmap phase, and enforce that the "Test/Validation" row is non-empty.

**How it works**: The roadmap generation prompt is updated to require a "Coverage Matrix" section in the merged roadmap. This matrix is a markdown table with rows for each requirement category (Functional, Data Models, CLI Interface, Gates, NFRs, Tests/Validation) and columns for each roadmap phase. Each cell indicates which specific requirements are addressed in that phase. A new semantic check on `MERGE_GATE` parses this table and verifies: (1) a "Tests" or "Validation" row exists, (2) the row contains at least one non-empty cell, (3) every test identifier from the spec extraction's `test_requirements` field appears in at least one cell.

**What it would catch**: Roadmaps that satisfy functional requirements but silently defer or drop testing. The coverage matrix makes omissions visible as empty cells. In the cli-portify case, the "Tests/Validation" row would have been empty or would have listed only "mocked steps" without `test_programmatic_step_routing`, triggering a gate failure.

**Integration point**: Prompt update in `roadmap/prompts.py` for the generation step. New `SemanticCheck` function in `roadmap/gates.py` on `MERGE_GATE` that parses the coverage matrix table. Optionally, the coverage matrix could be emitted as a separate artifact with its own gate.

**Limitations**: The coverage matrix is generated by the LLM and could be inaccurate (mapping a test to a phase where it is not actually addressed). Table parsing is fragile if the LLM deviates from the expected markdown table format. Adds structural requirements to the roadmap that may conflict with simpler specs.

---

## Section B: Roadmap-to-Tasklist -- Integration Test Task Coverage

These 5 solutions target the TASKLIST_FIDELITY_GATE and the tasklist generation pipeline to ensure that every integration test referenced in the roadmap becomes a concrete, executable tasklist task.

---

### B1: Test Task Enumeration Gate with Acceptance Criteria Validation

**Summary**: Parse all test references from the roadmap and verify each has a corresponding tasklist task with executable acceptance criteria (not just a mention).

**How it works**: A new semantic check is added to `TASKLIST_FIDELITY_GATE` in `tasklist/gates.py`. The check operates in two stages. Stage 1: scan the roadmap for test references -- function names matching `test_*`, phrases like "integration test", "E2E test", "smoke test", milestone validation criteria, and test strategy items. Build a set of expected test tasks. Stage 2: scan all generated tasklist files for tasks that correspond to each expected test. A "corresponding task" must satisfy three criteria: (a) the test name or equivalent appears in the task title or description, (b) the task has acceptance criteria (not just a description), (c) at least one acceptance criterion is executable (contains a verifiable assertion, command, or measurable outcome -- not "verify it works"). Missing or under-specified test tasks cause the gate to fail.

**What it would catch**: The exact Link 2 failure: the roadmap's test strategy items being reproduced in the tasklist only as vague descriptions without executable acceptance criteria. In the cli-portify case, even if the roadmap had preserved `test_programmatic_step_routing`, the tasklist's T11.05 acceptance criteria ("check outcomes only, not artifact content") would have failed the executability check.

**Integration point**: New `SemanticCheck` functions added to `TASKLIST_FIDELITY_GATE` in `tasklist/gates.py`. The check functions receive the content of the fidelity report (which compares roadmap to tasklist) and verify test task completeness. May require the fidelity prompt in `tasklist/prompts.py` to enumerate test tasks explicitly.

**Limitations**: Regex-based test reference extraction from the roadmap may miss tests described in prose. "Executable acceptance criteria" is a judgment call -- the check can verify structural markers (commands, assertions, file paths) but cannot determine if the criteria truly validate the feature.

---

### B2: Tasklist Test Task Template Injection

**Summary**: Automatically inject skeleton test tasks into the tasklist for every integration/E2E test referenced in the roadmap, ensuring they cannot be omitted.

**How it works**: During tasklist generation, after the LLM produces the initial tasklist, a deterministic post-processing step runs. It parses the roadmap's test strategy section and any test references in phase milestones. For each identified test, it checks whether a matching task exists in the generated tasklist. If not, it injects a template task:

```markdown
### T{NN}.{MM}: {test_name}
- **Type**: Integration Test / E2E Test / Smoke Test
- **Source**: Roadmap Phase {N}, {reference}
- **Acceptance Criteria**:
  - [ ] Test file `tests/{path}/{test_name}.py` exists
  - [ ] Test function `{test_name}` is callable
  - [ ] Test passes against non-mocked execution path
  - [ ] INJECTED: This task was auto-generated because the roadmap references this test but no tasklist task was found. Review and refine acceptance criteria.
```

The injection is deterministic (no LLM involved) and runs before the tasklist fidelity gate, so the gate validates the complete tasklist including injected tasks.

**What it would catch**: Any test that appears in the roadmap but is silently omitted by the LLM during tasklist generation. The injected template ensures the test exists as a task; the "INJECTED" marker flags it for human review. In the cli-portify case, `test_programmatic_step_routing` would have been injected as a task even if the LLM omitted it.

**Integration point**: New post-processing function in the tasklist generation pipeline (likely in `tasklist/steps.py` or equivalent), running after LLM generation but before the fidelity gate. The function parses roadmap content and tasklist content, performing injection as needed.

**Limitations**: Injected tasks have generic acceptance criteria that may not match the spec's intent. The injection logic must avoid duplicating tasks that the LLM already created under a different name. Template tasks may be treated as "noise" by sprint executors if not reviewed. Injection cannot fix a roadmap that already dropped the test (depends on Section A solutions).

---

### B3: Bidirectional Traceability ID Enforcement

**Summary**: Require every roadmap test reference to carry a traceability ID and verify that every ID appears in exactly one tasklist task.

**How it works**: The roadmap generation prompt is updated to require traceability IDs on all test references using the pattern `VT-NNN` (Validation/Test). Example: `VT-001: test_programmatic_step_routing (integration)`. The tasklist generation prompt is updated to require that every `VT-NNN` ID appears in a tasklist task title or acceptance criteria. The `TASKLIST_FIDELITY_GATE` gets two new deterministic semantic checks: (1) `_all_vt_ids_present`: extract all `VT-NNN` IDs from the roadmap, extract all `VT-NNN` IDs from the tasklist files, verify every roadmap ID appears in the tasklist. (2) `_no_orphan_vt_ids`: verify every tasklist `VT-NNN` ID exists in the roadmap (no invented test tasks).

**What it would catch**: Any test requirement that is assigned an ID in the roadmap but does not appear in the tasklist. This is a deterministic check (regex-based ID matching) that does not depend on LLM judgment. In the cli-portify case, `VT-001: test_programmatic_step_routing` would have been flagged as missing from the tasklist.

**Integration point**: Prompt updates in `roadmap/prompts.py` and `tasklist/prompts.py` to require `VT-NNN` IDs. Two new `SemanticCheck` functions in `tasklist/gates.py` on `TASKLIST_FIDELITY_GATE`. The ID extraction is pure regex, following the same pattern as `_routing_ids_valid` in `roadmap/gates.py`.

**Limitations**: Depends on the LLM consistently generating `VT-NNN` IDs in the roadmap. If the roadmap generation omits an ID (same failure as Section A), this gate cannot catch it. Only as strong as Link 1 -- this solution hardens Link 2 but assumes Link 1 is already fixed. ID format must be enforced by a separate gate on the roadmap side.

---

### B4: Test Task Completeness Score with Minimum Threshold

**Summary**: Compute a test task completeness score comparing roadmap test references to tasklist test tasks, and block the pipeline if the score falls below a configurable threshold.

**How it works**: A new scoring function is added to the tasklist fidelity pipeline. It computes:

```
test_completeness = (tasklist_test_tasks_with_executable_criteria / roadmap_test_references) * 100
```

Where:
- `roadmap_test_references` = count of distinct test names, E2E scenarios, and smoke test items in the roadmap
- `tasklist_test_tasks_with_executable_criteria` = count of tasklist tasks that (a) reference a test from the roadmap and (b) have at least one acceptance criterion containing a file path, command, assertion, or measurable outcome

The score is emitted as a `test_completeness_score` field in the tasklist fidelity report frontmatter. A new semantic check on `TASKLIST_FIDELITY_GATE` verifies `test_completeness_score >= threshold` (default: 100, configurable per complexity class). Scores below threshold block the pipeline with a report listing which tests lack tasklist coverage.

**What it would catch**: Partial test coverage -- where some tests are preserved but others are dropped. A threshold of 100 requires all tests to be covered. A lower threshold (e.g., 90) allows minor omissions for simple specs while still catching major gaps. In the cli-portify case, the score would have been 0% (zero test tasks with executable criteria for `test_programmatic_step_routing`), far below any reasonable threshold.

**Integration point**: New scoring logic in the tasklist fidelity prompt (`tasklist/prompts.py`) or as a deterministic post-processing step. New frontmatter field `test_completeness_score` on the fidelity report. New `SemanticCheck` in `tasklist/gates.py` that parses and validates the score.

**Limitations**: The score denominator (roadmap test references) is only as complete as the roadmap itself. If the roadmap dropped tests (Link 1 failure), the denominator is wrong and 100% completeness is achievable while still missing spec tests. The numerator assessment ("executable criteria") requires either LLM judgment or heuristic pattern matching, both of which can be inaccurate.

---

### B5: Shadow Tasklist Generation with Test-Only Focus

**Summary**: Generate a second, independent tasklist focused exclusively on test tasks, then diff it against the primary tasklist to find missing test coverage.

**How it works**: After the primary tasklist is generated, a parallel "shadow" generation runs with a specialized prompt: "Given this roadmap, generate ONLY the test, validation, and verification tasks. For each, provide the test name, test type, the roadmap phase it validates, and executable acceptance criteria." This produces a `test-tasklist-shadow.md` artifact. A deterministic diff step then compares the shadow tasklist against the primary tasklist. For each shadow task, it checks whether a matching task exists in the primary tasklist (fuzzy name matching + phase matching). Unmatched shadow tasks are reported as test coverage gaps. The fidelity gate blocks if any integration or E2E test from the shadow list is absent from the primary tasklist.

**What it would catch**: Tests that the primary LLM generation dropped due to attention dilution (focusing on implementation tasks at the expense of test tasks). The shadow generation's test-only focus eliminates this dilution. In the cli-portify case, the shadow generator would have produced a task for `test_programmatic_step_routing` because it is an explicit integration test in the roadmap's test strategy. The diff would have flagged it as missing from the primary tasklist.

**Integration point**: New pipeline step after primary tasklist generation in the tasklist pipeline. New artifact `test-tasklist-shadow.md` with a `LIGHT`-tier gate. Diff logic as a new semantic check or standalone validation step. The diff result feeds into `TASKLIST_FIDELITY_GATE` as additional context.

**Limitations**: Doubles the LLM cost for tasklist generation. The shadow generator may produce different test interpretations than the primary generator, causing false-positive diffs. Fuzzy matching between shadow and primary tasks can miss matches or produce spurious gaps. Adds significant pipeline latency.

---

## Cross-Cutting Considerations

### Solution Pairing Recommendations

The strongest defense combines one solution from Section A with one from Section B:

| Pairing | Strength | Cost |
|---------|----------|------|
| A1 + B3 (ID extraction + bidirectional traceability) | Deterministic end-to-end chain; regex-based, no LLM dependency in enforcement | Medium: requires prompt updates and two new semantic checks |
| A3 + B1 (test manifest + enumeration gate) | Most precise; structured data through both links | High: new pipeline step, new artifact, complex gate logic |
| A5 + B4 (coverage matrix + completeness score) | Human-readable audit trail; configurable threshold | Medium: prompt updates, one new semantic check per gate |

### What None of These Solutions Address

All 10 solutions operate within the Spec-to-Roadmap and Roadmap-to-Tasklist validation phases. They do not address:

1. **Link 3 (Tasklist-to-Code)**: Even with perfect test task preservation, no gate verifies that the code actually implements the test. This requires a separate code fidelity gate (see forensic report Section 10, Mitigation 3).
2. **No-op detection**: Tests that exist but pass trivially (e.g., mocked steps returning success) require runtime assertion verification, not pipeline document gates.
3. **Spec completeness**: If the original spec does not define tests, none of these gates can invent them. Spec-level test requirement enforcement is a separate concern.
