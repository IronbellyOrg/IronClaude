# Brainstorm 04: Hybrid LLM+Deterministic Gates

**Date**: 2026-03-17
**Context**: Forensic report `/docs/generated/cli-portify-executor-noop-forensic-report.md` demonstrated that current fidelity gates rely entirely on LLM-generated severity classifications. Deterministic Python code only validates YAML frontmatter metadata (`high_severity_count == 0`, `tasklist_ready` consistency) -- it never independently verifies what the LLM claims.
**Goal**: 10 hybrid solutions (5 per validation phase) where LLM identifies deviations and deterministic code validates the LLM's claims.

---

## Section A: Spec-to-Roadmap -- Hybrid LLM+Deterministic Gates

### A1. Requirement ID Enumeration Cross-Check

**Summary**: Parse all FR-NNN, NFR-NNN, SC-NNN identifiers from the spec extraction, then deterministically verify each appears in the roadmap body text.

**How it works**:
1. After the `extract` step produces `extraction.md`, deterministic code regex-scans it for all `FR-\d{3}`, `NFR-\d{3}`, `SC-\d{3}` identifiers and builds a canonical set (e.g., `{FR-001, FR-002, ..., FR-047}`).
2. After the `merge` step produces the final roadmap, deterministic code scans the roadmap body for occurrences of every ID in the canonical set.
3. Any IDs present in the extraction but absent from the roadmap are flagged as deterministic HIGH deviations -- regardless of what the LLM's fidelity report says.
4. The `SPEC_FIDELITY_GATE` semantic checks are extended with a new `_all_requirement_ids_covered` function that runs this cross-check and fails the gate if any IDs are missing.

**What it would catch**:
- The cli-portify bug: the spec defined `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, and `test_programmatic_step_routing` as requirements. If these were tagged with FR-NNN IDs during extraction, the cross-check would have flagged their absence from the roadmap's "sequential execution with mocked steps" description.
- Any case where the LLM fidelity reviewer misses an omitted requirement or classifies a missing FR as MEDIUM instead of HIGH.
- Bulk omissions where the LLM "rounds down" by saying "most requirements are covered" without checking each one.

**Integration point**: New semantic check function added to `src/superclaude/cli/roadmap/gates.py`, registered on `SPEC_FIDELITY_GATE.semantic_checks`. Requires the extraction file path be available at gate evaluation time -- either passed via `GateCriteria` metadata or resolved from the pipeline's step output registry.

**Limitations**:
- Only works if the extraction step assigns explicit IDs to requirements. If the spec is poorly structured or the LLM fails to tag requirements with FR-NNN IDs, the canonical set is incomplete.
- String matching is brittle: the roadmap might reference "FR-012" within a different context (e.g., "supersedes FR-012") without actually addressing it.
- Does not catch semantic misrepresentation -- a requirement ID can appear in the roadmap while the roadmap's description contradicts what the spec actually requires.

---

### A2. Section-Level Structural Correspondence Validator

**Summary**: Deterministically verify that every H2/H3 section in the spec extraction maps to at least one corresponding section or subsection in the roadmap.

**How it works**:
1. Parse the extraction document's heading hierarchy (all H2 and H3 headings) to produce a structural outline. For example: `["Functional Requirements", "Non-Functional Requirements", "Architectural Constraints", "Risk Inventory", ...]`.
2. Parse the roadmap's heading hierarchy similarly.
3. Build a mapping table: for each extraction section, find roadmap sections that contain keywords from the extraction heading or that reference content from that extraction section.
4. The LLM fidelity report is required to include an explicit "Coverage Matrix" section listing which roadmap section addresses each extraction section. Deterministic code parses this matrix and validates: (a) every extraction section appears in the matrix, (b) every roadmap section referenced in the matrix actually exists in the roadmap, (c) no extraction section is mapped to "[NOT ADDRESSED]" without a HIGH severity deviation entry.

**What it would catch**:
- Entire spec sections dropped silently during roadmap generation (e.g., "Architectural Constraints" section exists in extraction but has no corresponding roadmap coverage).
- The LLM claiming coverage exists when the referenced roadmap section does not actually exist (hallucinated section references).
- Structural drift where the roadmap reorganizes content so aggressively that traceability is lost.

**Integration point**: Two additions -- (1) modify `build_spec_fidelity_prompt()` in `src/superclaude/cli/roadmap/prompts.py` to require the "Coverage Matrix" output section; (2) add `_coverage_matrix_complete` semantic check to `SPEC_FIDELITY_GATE` in `src/superclaude/cli/roadmap/gates.py`.

**Limitations**:
- Heading-level granularity is coarse. A section could be "covered" at the heading level while omitting critical subsection details.
- Keyword matching between extraction headings and roadmap headings is fuzzy -- different naming conventions break the mapping.
- Adds a structured output requirement to the LLM prompt, which may reduce the LLM's ability to organize the fidelity report naturally.

---

### A3. Deviation Count Reconciliation Gate

**Summary**: Deterministically count the number of `DEV-NNN` entries in the fidelity report body and verify they match the frontmatter severity counts.

**How it works**:
1. Regex-scan the fidelity report body for all `DEV-\d{3}` entries.
2. For each entry, extract its declared severity (HIGH, MEDIUM, or LOW) from the structured format the prompt requires (`**Severity**: HIGH`).
3. Count occurrences per severity level: `body_high`, `body_medium`, `body_low`.
4. Compare against frontmatter values: `high_severity_count`, `medium_severity_count`, `low_severity_count`.
5. Fail the gate if any count mismatches (frontmatter says 0 HIGH but body contains 2 HIGH-severity DEV entries, or vice versa).
6. Also verify `total_deviations == body_high + body_medium + body_low`.

**What it would catch**:
- LLM arithmetic errors: the LLM lists 3 HIGH deviations in the report body but writes `high_severity_count: 0` in the frontmatter (the exact failure mode that lets the current gate pass).
- LLM self-contradiction: a deviation described as "this requirement is entirely missing from the roadmap" classified as MEDIUM instead of HIGH in the body -- while the body count would still match, combining this with A4 (severity definition enforcement) catches the misclassification.
- Truncation: the LLM runs out of context and stops listing deviations partway through, making the frontmatter counts higher than the actual listed entries.

**Integration point**: New `_deviation_counts_reconciled` semantic check function in `src/superclaude/cli/roadmap/gates.py`, added to `SPEC_FIDELITY_GATE.semantic_checks`. Pure function operating on content string.

**Limitations**:
- Only catches inconsistency between the LLM's body and its own frontmatter. If the LLM consistently misses a deviation (neither lists it in the body nor counts it in frontmatter), this gate cannot help.
- Depends on the LLM following the prescribed output format exactly. If the LLM uses `DEV-01` instead of `DEV-001`, or omits the `**Severity**:` label, the regex fails silently.
- Does not validate whether the deviations themselves are real -- only that the LLM's self-reported counts are internally consistent.

---

### A4. Severity Classification Spot-Check via Keyword Heuristics

**Summary**: Apply keyword heuristics to each LLM-reported deviation to flag likely misclassifications (e.g., a deviation containing "entirely missing" or "omitted" classified as anything other than HIGH).

**How it works**:
1. Parse each `DEV-NNN` entry from the fidelity report body, extracting: severity, deviation description, spec quote, and roadmap quote.
2. Apply a set of deterministic heuristic rules:
   - **Escalation triggers**: If roadmap quote is `[MISSING]` and severity is not HIGH, flag as likely misclassification. If deviation description contains "omit", "missing", "absent", "contradicts", "violates" and severity is LOW or MEDIUM, flag.
   - **De-escalation triggers**: If both spec and roadmap quotes are present and the deviation description contains "ordering", "formatting", "style", "terminology" and severity is HIGH, flag as likely over-classification.
3. Flagged deviations are reported as gate warnings (STANDARD tier) or gate failures (STRICT tier, configurable).
4. If any deviation is flagged with an escalation trigger (should-be-HIGH classified lower), the gate fails and requests LLM re-evaluation.

**What it would catch**:
- The cli-portify scenario: if the LLM's fidelity report listed the missing three-way dispatch as MEDIUM ("the roadmap simplifies the executor design") while the roadmap quote was `[MISSING]`, the keyword heuristic would catch the `[MISSING]` + non-HIGH combination and escalate.
- Systematic under-classification bias where the LLM tends to soften severity to produce a "cleaner" report.
- Cases where the spec explicitly says "MUST" or "SHALL" and the roadmap omits the requirement -- the `[MISSING]` roadmap quote is a strong signal.

**Integration point**: New `_severity_classifications_plausible` semantic check in `src/superclaude/cli/roadmap/gates.py`. The heuristic rules could be defined as a list of `(pattern, expected_min_severity)` tuples for maintainability. Added to `SPEC_FIDELITY_GATE.semantic_checks`.

**Limitations**:
- Keyword heuristics are inherently noisy. False positives will occur when the LLM uses dramatic language for genuinely low-severity issues.
- Cannot detect the case where the LLM completely misses a deviation (no entry at all) -- only catches misclassified entries that do exist.
- The heuristic rule set requires maintenance as the fidelity report format evolves.
- Language-dependent: assumes English keywords in deviation descriptions.

---

### A5. Dual-Pass LLM Comparison with Deterministic Consensus Enforcement

**Summary**: Run the spec-fidelity comparison twice with different LLM prompting strategies, then deterministically compare the two reports and fail the gate if they disagree on HIGH-severity findings.

**How it works**:
1. The pipeline runs `build_spec_fidelity_prompt()` as today, producing `fidelity-report-A.md`.
2. A second pass runs a modified prompt (`build_spec_fidelity_adversarial_prompt()`) that instructs the LLM to be maximally suspicious -- "assume every omission is intentional obfuscation and classify aggressively." This produces `fidelity-report-B.md`.
3. Deterministic code parses both reports' `DEV-NNN` entries:
   - Builds a union set of all deviations mentioned in either report.
   - For deviations mentioned in both: if report B classifies something as HIGH but report A classifies it as MEDIUM or LOW, this is a "contested HIGH" and fails the gate.
   - For deviations mentioned in only one report: deviations found only by the adversarial pass are flagged as "missed by standard pass" and treated as HIGH.
4. The gate passes only if the two reports agree that `high_severity_count == 0`, or if all contested HIGHs are resolved by a third tiebreaker pass.

**What it would catch**:
- The cli-portify bug: the adversarial pass, instructed to treat every omission as suspicious, would likely flag the missing three-way dispatch. Even if the standard pass missed it, the consensus enforcement would catch the disagreement.
- Systematic LLM blind spots: any deviation that one prompting strategy catches but the other misses surfaces as a finding.
- Over-confident LLM passes: if the standard pass says "all requirements covered, 0 HIGHs" but the adversarial pass finds 3 HIGHs, the gate blocks.

**Integration point**: Requires a new pipeline step `spec-fidelity-adversarial` inserted after `spec-fidelity` in the step list defined in `src/superclaude/cli/roadmap/pipeline.py` (or equivalent step builder). New prompt function `build_spec_fidelity_adversarial_prompt()` in `src/superclaude/cli/roadmap/prompts.py`. New `_dual_pass_consensus` semantic check in `src/superclaude/cli/roadmap/gates.py` that reads both report files.

**Limitations**:
- Doubles the LLM cost and latency for the fidelity check step.
- The adversarial prompt may produce excessive false positives, overwhelming the consensus mechanism.
- Deterministic matching between reports requires deviations to reference the same spec content, which is not guaranteed when two independent LLM passes describe the same issue differently.
- The tiebreaker (third pass) adds even more cost if disagreements are frequent.

---

## Section B: Roadmap-to-Tasklist -- Hybrid LLM+Deterministic Gates

### B1. Deliverable ID Traceability Cross-Check

**Summary**: Parse all deliverable IDs (D-NNNN) and risk IDs (R-NNN) from the roadmap, then deterministically verify each appears in at least one tasklist file.

**How it works**:
1. After the `merge` step, deterministic code regex-scans the final roadmap for all `D-\d{4}` and `R-\d{3}` identifiers, building a canonical deliverable set.
2. After tasklist generation, deterministic code scans all tasklist files (glob `T*.md`) for occurrences of every deliverable ID.
3. Any deliverable ID present in the roadmap but absent from all tasklist files is a deterministic HIGH deviation, regardless of the LLM's fidelity report.
4. Additionally, verify that each roadmap phase's deliverable list has at least one corresponding tasklist task group.

**What it would catch**:
- The cli-portify bug: if the roadmap contained deliverable IDs for the dispatch wiring (e.g., `D-0034: Three-way step dispatch`), the cross-check would flag their absence from the tasklist. However, note that in the actual bug, the roadmap itself already omitted the dispatch -- so this gate catches omissions introduced between roadmap and tasklist, not omissions already present in the roadmap (those are Section A's responsibility).
- Tasklist generation that covers high-level roadmap goals but drops specific deliverables during decomposition.
- Bulk tasklist truncation where the LLM runs out of context and stops generating tasks for later roadmap phases.

**Integration point**: New `_all_deliverable_ids_covered` semantic check in `src/superclaude/cli/tasklist/gates.py`, registered on `TASKLIST_FIDELITY_GATE.semantic_checks`. Requires access to the roadmap file path at gate evaluation time.

**Limitations**:
- Only works if the roadmap uses explicit deliverable IDs. If the roadmap describes deliverables in prose without IDs, the regex has nothing to match.
- String presence does not guarantee semantic coverage -- a tasklist could mention `D-0034` in a comment ("see D-0034 for context") without actually creating a task to implement it.
- Cannot catch the case where the roadmap itself is already missing a requirement (cascading from a Section A failure).

---

### B2. Acceptance Criteria Completeness Validator

**Summary**: Parse acceptance criteria from roadmap milestones, then verify every criterion has a corresponding acceptance check in the tasklist.

**How it works**:
1. Deterministic code parses the roadmap for milestone definitions, extracting acceptance criteria patterns: lines that begin with `- [ ]`, `- AC:`, `- Acceptance:`, or appear under "Acceptance Criteria" / "Success Criteria" headings.
2. Each extracted criterion is assigned a deterministic hash (normalized lowercase, stopwords removed, hashed to 8 chars) to produce a fingerprint set.
3. The tasklist fidelity prompt is modified to require the LLM to emit an "Acceptance Criteria Mapping" section that lists each roadmap criterion and its corresponding tasklist task(s).
4. Deterministic code parses this mapping and validates: (a) every roadmap criterion fingerprint appears in the mapping, (b) every tasklist task referenced in the mapping actually exists in the tasklist files, (c) criteria marked as "Not Mapped" trigger a HIGH deviation.

**What it would catch**:
- Roadmap milestones with acceptance criteria like "Sequential pipeline runs end-to-end with mocked steps" being decomposed into tasks but the more critical criteria like "Programmatic steps call Python functions, not Claude subprocesses" being dropped.
- Criteria that exist in the roadmap but are silently absorbed into overly-broad tasklist tasks without explicit mapping.
- LLM claiming coverage when the referenced task does not exist in any tasklist file (hallucinated task references).

**Integration point**: Modify `build_tasklist_fidelity_prompt()` in `src/superclaude/cli/tasklist/prompts.py` to require the acceptance criteria mapping. Add `_acceptance_criteria_mapped` semantic check to `TASKLIST_FIDELITY_GATE` in `src/superclaude/cli/tasklist/gates.py`.

**Limitations**:
- Acceptance criteria extraction is heuristic -- different roadmap authors use different formatting conventions.
- Fingerprint matching is approximate. Roadmap criteria and tasklist descriptions may use different wording for the same concept.
- Adds structured output burden to the LLM fidelity prompt, risking format compliance issues.
- Does not verify that the tasklist tasks, once executed, actually satisfy the criteria -- only that a mapping exists.

---

### B3. Task Count Proportionality Gate

**Summary**: Deterministically verify that the number of tasklist tasks per roadmap phase is proportional to the phase's complexity and deliverable count, flagging phases with suspiciously few tasks.

**How it works**:
1. Parse the roadmap to extract phase definitions, counting: number of deliverables per phase, number of requirements referenced per phase, and complexity indicators (e.g., "complex", "critical", "multi-component").
2. Parse the tasklist files to count tasks per phase (using phase ID prefixes like `T03.*` for Phase 3).
3. Compute expected task count ranges using heuristics: minimum 2 tasks per deliverable, minimum 3 tasks for any phase marked "complex" or "critical", at least 1 integration task per phase with cross-module dependencies.
4. If any phase falls below its minimum expected task count, flag it as a proportionality violation. This is surfaced as a gate warning (STANDARD) or failure (STRICT).

**What it would catch**:
- A roadmap phase describing 5 deliverables (executor, dispatch, registry, step wiring, integration tests) being decomposed into only 2 tasklist tasks ("build executor" and "add tests") -- the proportionality check would flag that 5 deliverables cannot be adequately covered by 2 tasks.
- Phases that are entirely empty in the tasklist (zero tasks for a non-trivial roadmap phase).
- The inverse problem: phases with excessive task counts that suggest the LLM is padding rather than decomposing meaningfully (upper bound check).

**Integration point**: New `_phase_task_proportionality` semantic check in `src/superclaude/cli/tasklist/gates.py`. Requires the roadmap file to compute expected counts. Could be registered on `TASKLIST_FIDELITY_GATE` or as a separate `TASKLIST_PROPORTIONALITY_GATE` in a new gate definition.

**Limitations**:
- Heuristic thresholds are arbitrary. Different project types have genuinely different task-to-deliverable ratios.
- Phase identification depends on consistent naming conventions between roadmap ("Phase 3") and tasklist (`T03.*`).
- Does not verify task content quality -- a phase could have the "right" number of tasks that are all trivial or redundant.
- False positives for phases that are intentionally lightweight (documentation phases, planning phases).

---

### B4. Integration Task Detection Gate

**Summary**: Deterministically verify that roadmap phases with cross-module dependencies have explicit integration/wiring tasks in the tasklist.

**How it works**:
1. Parse the roadmap for module dependency indicators: phrases like "imports from", "calls", "depends on", "integrates with", "wires to", module dependency graphs, or import chain specifications.
2. For each identified cross-module dependency pair (e.g., `executor.py --> steps/*.py`), check whether the tasklist contains at least one task whose description or acceptance criteria mentions both modules.
3. Additionally, scan for "integration" keyword patterns in tasklist tasks: "wire", "connect", "integrate", "dispatch", "route", "hook up", "link". If a roadmap phase describes 3+ cross-module dependencies but the tasklist has zero integration-keyword tasks for that phase, flag it.
4. The gate fails if any cross-module dependency pair from the roadmap has no corresponding integration task.

**What it would catch**:
- The exact cli-portify failure: the spec defined `executor.py --> steps/*.py` import chains. If the roadmap had carried this through (a Section A responsibility), this gate would catch the tasklist's failure to include a "wire executor to step implementations" task.
- The "two parallel tracks" anti-pattern: Track A (executor infrastructure) and Track B (step implementations) built independently with no integration task to connect them.
- Missing glue code tasks in any pipeline where components are designed separately but must be connected.

**Integration point**: New `_integration_tasks_present` semantic check in `src/superclaude/cli/tasklist/gates.py`, registered on `TASKLIST_FIDELITY_GATE.semantic_checks`. Alternatively, as a standalone `TASKLIST_INTEGRATION_GATE` since it serves a distinct purpose from fidelity checking.

**Limitations**:
- Dependency detection in the roadmap is heuristic. Not all roadmaps describe module dependencies explicitly -- many describe features at a higher abstraction level.
- Keyword matching ("wire", "connect", "integrate") is noisy and language-dependent. A task titled "Build step execution logic" might be an integration task without using any of the trigger keywords.
- Cannot detect the need for integration tasks that the roadmap itself does not describe (cascading from Section A failures).
- Over-triggers for monolithic codebases where "cross-module" is the norm and explicit integration tasks would be redundant.

---

### B5. Tasklist-to-Roadmap Bidirectional Consistency Audit

**Summary**: Run a deterministic bidirectional check -- every roadmap phase maps to tasklist tasks AND every tasklist task maps back to a roadmap phase -- flagging orphans in both directions.

**How it works**:
1. **Forward check (roadmap-to-tasklist)**: Parse roadmap phase identifiers (Phase 1, Phase 2, ..., Phase N) and milestone identifiers (M1, M2, ...). For each, verify at least one tasklist file or task group references it.
2. **Backward check (tasklist-to-roadmap)**: Parse all tasklist task IDs (T01.01, T03.04, ...) and extract their phase prefix. Verify the referenced phase exists in the roadmap. Also check for task descriptions that reference roadmap content not actually present in the roadmap (hallucinated roadmap references).
3. **Orphan detection**: A roadmap phase with zero tasklist coverage is a "forward orphan" (HIGH severity). A tasklist task referencing a nonexistent roadmap phase is a "backward orphan" (HIGH severity -- indicates hallucination or copy-paste from a different release).
4. The LLM fidelity report is still generated but now includes a required "Bidirectional Trace" section. Deterministic code independently performs the same trace and compares results.
5. Disagreements between the LLM's trace and the deterministic trace are flagged as "audit discrepancies" -- cases where the LLM claims coverage that the deterministic check cannot confirm.

**What it would catch**:
- Forward orphans: a roadmap phase on executor dispatch wiring with no tasklist tasks (the cli-portify pattern).
- Backward orphans: tasklist tasks that reference "Phase 7: Performance Optimization" when the roadmap only has 5 phases (LLM hallucination during tasklist generation).
- LLM fidelity report errors: the LLM claiming "all phases covered" when the deterministic trace shows Phase 4 has no tasks.
- Cross-release contamination: tasklist tasks copied from a previous release that reference phases or milestones not in the current roadmap.

**Integration point**: New `_bidirectional_trace_consistent` semantic check in `src/superclaude/cli/tasklist/gates.py`. Modify `build_tasklist_fidelity_prompt()` in `src/superclaude/cli/tasklist/prompts.py` to require the "Bidirectional Trace" section. The deterministic phase parsing logic could be factored into a shared utility in `src/superclaude/cli/pipeline/tracing.py`.

**Limitations**:
- Phase identification depends on consistent naming. If the roadmap uses "Sprint 1" and the tasklist uses "Phase 1", the mapping breaks.
- The backward check can only detect references to phases, not semantic coverage. A task might reference the correct phase but describe work that does not actually implement the phase's deliverables.
- Adds complexity to the fidelity prompt and the gate system. The bidirectional trace is a significant new structured output requirement for the LLM.
- Does not extend to the next link (tasklist-to-code) -- even a perfectly traced tasklist can produce code with no-op implementations if the acceptance criteria are weak.

---

## Cross-Cutting Observations

1. **Solutions A1-A4 and B1-B4 are composable.** They can be implemented independently as additional `SemanticCheck` entries on the existing `SPEC_FIDELITY_GATE` and `TASKLIST_FIDELITY_GATE` definitions. No architectural changes are needed -- just new pure functions in the existing gates modules.

2. **A5 and B5 require pipeline-level changes** (additional steps or modified step I/O), making them higher-effort but also higher-coverage.

3. **The ID-based solutions (A1, A3, B1) are the lowest-hanging fruit.** They require no prompt changes, operate purely on existing document content, and catch the most critical failure mode (missing requirements silently passing the gate).

4. **None of these solutions address Link 3 (tasklist-to-code).** That is a separate problem requiring code-level analysis gates, which is out of scope for this brainstorm but documented in the forensic report's Mitigation 3.

5. **All deterministic checks follow the existing `(content: str) -> bool` semantic check signature**, except where cross-file access is needed (A1 needs the extraction file, B1 needs the roadmap file). Those cases require extending `SemanticCheck` to accept additional file paths or using a closure pattern to capture the needed paths at gate construction time.
