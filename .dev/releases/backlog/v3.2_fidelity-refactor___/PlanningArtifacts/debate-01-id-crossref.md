# Adversarial Debate 01: Two-Pass Validation (Brainstorm 01, Solution A3)

**Date**: 2026-03-17
**Proposal**: Two-Pass Validation: Programmatic Sweep Then LLM Deep Dive
**Source**: `brainstorm-01-id-crossref.md`, Solution A3
**Scoring Framework**: `scoring-framework.md`
**Forensic Reference**: `docs/generated/cli-portify-executor-noop-forensic-report.md`

---

## Proposal Summary

Split `SPEC_FIDELITY_GATE` into two sequential passes:

- **Pass 1** (programmatic, ~0 tokens): Regex-extract all `FR-NNN`/`NFR-NNN`/`SC-NNN` IDs from spec extraction. Scan roadmap for each. Missing IDs flagged as HIGH severity. Pass 1 has veto power.
- **Pass 2** (LLM, existing cost): Run existing `build_spec_fidelity_prompt()` but inject Pass 1 findings as context. LLM verifies and adds semantic deviations.
- **Integration**: Extend `gate_passed()` to support `pre_checks` on `GateCriteria`, or add as a new step between roadmap generation and spec-fidelity.

---

## Advocate's Opening Argument

### 1. Specific Bug Scenarios Caught

The cli-portify forensic report (Section 5, "Link 1: Spec to Roadmap -- FAILED") documents the exact failure this proposal targets. The v2.24 and v2.25 specs defined:

- Three-way dispatch: `_run_programmatic_step()`, `_run_claude_step()`, `_run_convergence_step()`
- `PROGRAMMATIC_RUNNERS` dictionary mapping step IDs to Python functions
- `test_programmatic_step_routing` integration test
- Module dependency graph: `executor.py --> steps/validate_config.py`, etc.

If these were tagged with formal IDs (e.g., `FR-012: Three-way dispatch`, `FR-013: PROGRAMMATIC_RUNNERS`, `SC-007: test_programmatic_step_routing`), Pass 1 would have performed the following check:

```
spec_ids = {FR-012, FR-013, SC-007, ...}  # extracted from extraction.md
roadmap_ids = {FR-001, FR-002, ...}        # found in roadmap.md
missing = spec_ids - roadmap_ids           # {FR-012, FR-013, SC-007}
```

Result: **immediate gate failure** with a deterministic, enumerated list of missing requirements. The roadmap's reduction to "sequential execution with mocked steps" would have been blocked before the LLM fidelity check even ran. The corruption that propagated through the entire pipeline (Section 9, "Primary: Spec-to-Roadmap Fidelity Failure") would have been stopped at its origin.

Beyond the cli-portify case, this gate catches the entire class of "silent requirement dropping" bugs. The forensic report's Section 7 ("The Systemic Blind Spot") identifies that every gate follows the signature `(content: str) -> bool` and validates document structure, not content completeness. Pass 1 introduces the first content-completeness check in the pipeline -- a deterministic floor that the LLM cannot override.

The forensic report's Appendix B confirms the vulnerability: "No programmatic parsing of requirement IDs from source document. No cross-reference verification (every FR-NNN in spec exists in roadmap). No enumeration completeness check." This proposal directly addresses all three gaps.

### 2. Integration Path

The integration is minimal and follows existing patterns. The current architecture in `src/superclaude/cli/pipeline/models.py` defines:

```python
@dataclass
class SemanticCheck:
    name: str
    check_fn: Callable[[str], bool]
    failure_message: str

@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
```

And `gate_passed()` in `src/superclaude/cli/pipeline/gates.py` iterates `criteria.semantic_checks` at the STRICT tier, calling each `check_fn(content)`.

**Option A (minimal change)**: Add a new `SemanticCheck` to `SPEC_FIDELITY_GATE.semantic_checks` in `src/superclaude/cli/roadmap/gates.py`. The check function receives the fidelity report content. The spec extraction step would embed a `## Requirement ID Manifest` YAML block in the fidelity report frontmatter listing all extracted IDs, and the check function would parse this manifest against roadmap ID references also embedded in the report. This requires modifying `build_spec_fidelity_prompt()` to instruct the LLM to include the manifest. Estimated: ~40 lines of new code in `gates.py`, ~15 lines of prompt modification.

**Option B (cleaner, slightly more work)**: Add a `pre_checks` field to `GateCriteria`:

```python
@dataclass
class GateCriteria:
    # ... existing fields ...
    pre_checks: list[Callable[[Path, Path], tuple[bool, str | None]]] | None = None
```

Where `pre_checks` are functions that receive the upstream and downstream file paths and run before the main semantic checks. `gate_passed()` gains 5-8 lines to iterate `pre_checks` before reading file content. The Pass 1 function receives the spec extraction path and roadmap path directly, eliminating the need to embed manifests in prompts. Estimated: ~60 lines of new code across `models.py`, `gates.py`, and `roadmap/gates.py`.

Both options are well within the 50-200 line range for a 7-8 implementation complexity score. No new dependencies. No new infrastructure. The regex extraction function (`extract_requirement_ids`) is a pure function with trivial test coverage.

### 3. Composability with Other Proposals

This proposal directly enables and strengthens the other four proposals being debated:

- **Brainstorm 02 (Wiring Verification)**: The `extract_requirement_ids()` function and the `pre_checks` infrastructure are directly reusable. Wiring verification needs to cross-reference spec identifiers against roadmap content -- the same extraction pipeline this proposal builds.
- **Brainstorm 03 (Smoke Test Gates)**: Test requirement IDs (`SC-NNN`, `test_*` identifiers) are a subset of the IDs this proposal extracts. Pass 1 catches missing test requirements alongside missing functional requirements, making a dedicated test-requirement gate partially redundant or allowing it to build on the extracted ID set.
- **Brainstorm 04 (Hybrid Gates)**: This proposal IS a hybrid gate -- it establishes the pattern of "deterministic floor + LLM ceiling" that Brainstorm 04 generalizes. The `pre_checks` infrastructure introduced here becomes the insertion point for all Brainstorm 04 hybrid checks.
- **Brainstorm 05 (Link 3 Code Fidelity)**: The ID registry concept from A4 in Brainstorm 01 extends naturally from this proposal's extraction. If Pass 1 produces a structured ID set, downstream gates (including Link 3) can consume it to verify IDs at later pipeline stages.

The `pre_checks` extension to `GateCriteria` is the key composability contribution: it creates a general-purpose mechanism for injecting deterministic pre-checks before any gate's semantic evaluation. Every other proposal can use this pattern.

---

## Skeptic's Opening Argument

### 1. Failure Modes Where This Gate Would NOT Catch the Bug

The Advocate's argument contains a critical conditional: "If these were tagged with formal IDs." Let me examine whether this condition held in the actual cli-portify failure.

The forensic report (Section 4) describes the spec's dispatch design using prose and code blocks:

> Three-way dispatch: `_run_programmatic_step()`, `_run_claude_step()`, `_run_convergence_step()`
> `PROGRAMMATIC_RUNNERS` dictionary mapping step IDs to real Python functions
> Module dependency graph: `executor.py --> steps/validate_config.py`

These are architectural descriptions, not formal requirements with `FR-NNN` tags. The forensic report never mentions specific `FR-NNN` IDs for these features -- they were described in specification prose and pseudocode blocks. If the spec extraction step did not assign formal IDs to these elements (and the extraction prompt does not currently mandate exhaustive ID assignment), then Pass 1's regex scanner would find nothing to cross-reference. The gate would pass. The bug would ship.

This is not a hypothetical concern. The brainstorm document itself acknowledges the limitation: "Only catches IDs that follow the exact `FR-NNN`/`NFR-NNN`/`SC-NNN` naming convention. Specs that use prose descriptions without formal IDs would not benefit."

The cli-portify specs were produced by the pipeline's own spec extraction and generation prompts. Unless those prompts are also modified to guarantee exhaustive ID assignment to every architectural commitment, Pass 1 has no IDs to scan. The proposal addresses the *symptom* (missing cross-referencing) but depends on an *upstream prerequisite* (exhaustive ID tagging) that does not currently exist and is not part of this proposal's scope.

**Failure mode 1**: Specs with prose-only requirements produce empty or incomplete ID sets. Pass 1 finds no missing IDs. Gate passes. Bug ships.

**Failure mode 2**: The spec extraction step itself drops requirements before ID assignment. If `build_extract_prompt()` fails to extract the three-way dispatch from the source spec, the extraction output has no corresponding ID, and Pass 1 has nothing to cross-reference against.

**Failure mode 3**: Requirements addressed under different names. The roadmap could describe the dispatch functionality using different terminology (e.g., "step execution router" instead of "three-way dispatch") without referencing the original `FR-NNN` ID. Pass 1 would flag this as missing; Pass 2 context injection might clarify it, but the proposal gives Pass 1 veto power, meaning the LLM cannot override a false positive from Pass 1.

### 2. False Positive Scenarios

Pass 1's veto power creates a significant false positive risk:

**Scenario A: Intentional deferral.** A spec defines `FR-045: Performance optimization` but the team decides to defer it to a future release. The roadmap intentionally omits `FR-045`. Pass 1 flags it as HIGH severity. The gate blocks. There is no override mechanism described in the proposal. The team must either (a) add a deferred-requirements list that Pass 1 respects, (b) mention `FR-045` in the roadmap in a "deferred" section, or (c) modify the spec to remove `FR-045`. All three add friction to a common workflow.

**Scenario B: Requirement decomposition.** A spec defines `FR-020: User authentication`. The roadmap decomposes this into `FR-020a: OAuth flow`, `FR-020b: Session management`, `FR-020c: Token refresh` -- using sub-IDs. Pass 1's regex (`FR-\d{3}`) would not match `FR-020a` to `FR-020`, and might flag `FR-020` as missing even though it is fully addressed under sub-IDs. The regex would need to be more sophisticated, but the proposal does not specify how decomposition is handled.

**Scenario C: ID format evolution.** If a future spec uses `REQ-NNN` or `FEAT-NNN` instead of `FR-NNN`, Pass 1 silently becomes ineffective (no IDs extracted) rather than failing loudly. The gate degrades without warning.

### 3. Maintenance Burden Over 5+ Releases

Over the course of 5+ releases, this gate introduces the following maintenance costs:

- **Regex pattern maintenance**: Every new ID scheme (`REQ-NNN`, `FEAT-NNN`, `API-NNN`) requires updating the regex patterns in `extract_requirement_ids()`. If the team introduces a new pattern and forgets to update the extractor, the gate silently loses coverage.
- **Prompt coupling**: The Pass 2 context injection ("The following IDs were programmatically determined to be missing: [list]") adds a maintenance coupling between the programmatic pass and the LLM prompt. Prompt changes in `build_spec_fidelity_prompt()` must account for the injected context. If the prompt is refactored without updating the injection point, the LLM may ignore or misinterpret the injected findings.
- **Pre-checks infrastructure**: If Option B is chosen (`pre_checks` on `GateCriteria`), every change to `gate_passed()` must consider the `pre_checks` flow. The interaction between `pre_checks` and `semantic_checks` (ordering, short-circuiting, error aggregation) becomes a maintenance surface.
- **False positive tuning**: As new spec formats are adopted and new projects use the pipeline, the false positive rate from Pass 1 will fluctuate. Each new project may need a calibration pass to ensure the gate does not block legitimate pipelines.

The brainstorm's own cross-cutting observation #4 acknowledges: "Formal ID conventions are a prerequisite. Projects that use prose-only requirements without formal identifiers would not benefit. This suggests a complementary investment in spec extraction prompts that enforce ID assignment." This complementary investment is unbounded in scope and not costed in the implementation estimate.

### 4. Whether Simpler Alternatives Achieve the Same Benefit

**Alternative 1: Strengthen the existing LLM prompt.** Instead of a two-pass architecture, add a structured checklist section to `build_spec_fidelity_prompt()` that instructs the LLM to enumerate every requirement ID in the spec, then check each against the roadmap. This achieves most of Pass 1's benefit without any code changes to the gate infrastructure. The LLM already has access to both documents. Cost: ~20 lines of prompt modification, 0 lines of Python.

**Alternative 2: A1 (Pre-Gate ID Extraction and Set-Difference Check).** This is a simpler version of A3 that skips the LLM context injection entirely. It runs the same programmatic cross-reference but does not modify the LLM prompt. It achieves the same deterministic floor as Pass 1 without the complexity of two-pass coordination, context injection, or veto arbitration. If Pass 1 is the high-value component (as the Advocate argues), then Pass 2 injection is unnecessary overhead.

**Alternative 3: A2 (Bidirectional ID Manifest with Coverage Matrix).** This achieves a stronger guarantee (mapping IDs to specific roadmap phases, not just string presence) without requiring changes to `gate_passed()`. The manifest and coverage matrix are embedded in the existing document flow. The tradeoff is higher token cost but lower infrastructure complexity.

A3 is a middle-ground proposal that is more complex than A1 but less thorough than A2. The question is whether the context injection into Pass 2 justifies the additional architecture over A1's simpler set-difference approach.

---

## Advocate's Rebuttal

The Skeptic raises valid concerns about ID coverage, but overstates the dependency on pre-existing formal IDs. Three counterpoints:

**On the ID prerequisite**: The brainstorm's recommended implementation order (Section: "Cross-Cutting Observations", item 5) explicitly calls for A1 first, then A3. This proposal is designed to layer on top of a system that already has ID extraction. The spec extraction prompt (`build_extract_prompt()`) can be modified in the same release to mandate exhaustive ID assignment. This is a 15-line prompt change, not an unbounded investment. The Skeptic treats a co-requisite as a missing prerequisite.

**On false positives from veto power**: The veto can be implemented with an escape hatch. Pass 1 flags missing IDs as `PROGRAMMATIC_HIGH` in a structured findings block. Pass 2 can downgrade a `PROGRAMMATIC_HIGH` to `ACKNOWLEDGED_DEFERRAL` if the LLM confirms the omission is intentional and the roadmap contains a "Deferred Requirements" section referencing that ID. The veto is not absolute -- it requires the LLM to explicitly acknowledge the programmatic finding. This is the "two-pass" value: neither pass alone has full authority, but together they cover each other's blind spots.

**On A1 being simpler**: A1 and A3 share the same Pass 1. The difference is that A3 injects Pass 1 findings into the LLM prompt, which serves two purposes: (1) it forces the LLM to address each programmatic finding rather than potentially overlooking them, and (2) it allows the LLM to provide semantic context for programmatic failures (e.g., "FR-012 is addressed under a different name in Phase 3"). The context injection cost is ~10 lines of string formatting. The architectural overhead is marginal.

**On the cli-portify case specifically**: Even without formal IDs, the spec contained backtick-quoted identifiers (`_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing`). While the proposal's core mechanism uses `FR-NNN` regex, the `extract_requirement_ids()` function can be extended to also extract backtick-quoted identifiers from spec code blocks -- a 5-line enhancement that catches the exact cli-portify failure pattern. The Skeptic assumes the regex is frozen at `FR-\d{3}`, but the extraction function is a natural extension point.

---

## Skeptic's Rebuttal

The Advocate's rebuttal introduces scope creep that undermines the implementation complexity argument:

**On the "co-requisite" prompt change**: If the proposal requires modifying `build_extract_prompt()` to mandate exhaustive ID assignment, that is additional scope that must be costed. The "15-line prompt change" needs testing across multiple spec formats to verify it does not degrade extraction quality. Prompt changes are notoriously unpredictable in their effects on LLM output -- a change that improves ID assignment may cause regressions in other extraction dimensions.

**On the escape hatch**: The Advocate now proposes a three-state system: `PROGRAMMATIC_HIGH` -> LLM may downgrade to `ACKNOWLEDGED_DEFERRAL` if justified. This is no longer "veto power" -- it is a negotiation protocol between passes. The complexity of implementing this correctly (parsing the LLM's acknowledgment, distinguishing genuine deferrals from LLM hand-waving, preventing the LLM from systematically downgrading all programmatic findings) is higher than the Advocate's estimate suggests. It also introduces a new failure mode: the LLM might learn to produce boilerplate acknowledgments that always pass the negotiation.

**On extending to backtick-quoted identifiers**: This extension broadens the false positive surface considerably. Specs routinely mention identifiers in comparison contexts ("unlike `_run_sync()`, which blocks..."), rejection contexts ("we considered `BatchRunner` but..."), and reference contexts ("see `executor.py` for the base class"). A naive backtick extractor would flag all of these as "requirements," producing false positives on every spec that discusses design alternatives. The A5 (Structural Signature Fingerprinting) proposal from Brainstorm 01 addresses this concern and rates it as a high false-positive risk. The Advocate is absorbing A5's scope without its caveats.

**The core question remains**: Does the two-pass architecture justify its complexity over the simpler A1 set-difference check? The Advocate's strongest argument -- context injection -- adds ~10 lines of code but introduces a coupling between the programmatic pass and the LLM prompt that must be maintained through every prompt revision. If the value is primarily in Pass 1 (the deterministic floor), then A1 delivers that value with less maintenance surface.

---

## Final Scoring

### Dimension 1: Likelihood to Succeed (Weight: 0.35)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 8 | Pass 1 provides a deterministic floor that catches any ID-level omission. Pass 2 context injection forces the LLM to address programmatic findings. Together they catch the cli-portify failure (assuming IDs exist) and the broader "silent requirement dropping" class. Minor deduction for the ID prerequisite dependency. |
| Skeptic | 6 | The proposal catches ID-level omissions IF formal IDs exist in the spec. The cli-portify specs used prose and code blocks, not formal FR-NNN tags. The gate would not have caught the actual bug without an upstream prompt change that is not part of this proposal. Catches the pattern class but depends on formatting conventions that are not currently enforced. |

**Score difference: 2.** At the boundary. The Advocate's counterpoint about extending to backtick-quoted identifiers is plausible but introduces scope creep. The Skeptic's point about the actual cli-portify specs lacking formal IDs is factually grounded in the forensic report. **Tiebreaker**: The proposal's core mechanism (regex ID extraction + set difference) is sound and would definitively catch the bug IF the prerequisite is met. The prerequisite (exhaustive ID assignment in extraction prompts) is a tractable co-requisite. Score reflects the mechanism's strength tempered by the dependency.

**Final Score: 7**

### Dimension 2: Implementation Complexity (Weight: 0.25)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 8 | Option A: ~55 lines across gates.py and prompts.py. Option B: ~60 lines across models.py, gates.py, and roadmap/gates.py. No new dependencies. Test coverage is trivial for the pure regex function. Follows existing SemanticCheck pattern. |
| Skeptic | 6 | Base implementation is small, but the Advocate's rebuttal introduces additional scope: prompt modification for ID assignment, escape hatch negotiation protocol, backtick extraction extension. True cost including testing across spec formats and false positive tuning is closer to 200-300 lines. Two-pass coordination adds interaction complexity beyond line count. |

**Score difference: 2.** At the boundary. The Advocate's base estimate for the core mechanism is credible. The Skeptic correctly identifies that the "complete" implementation (with escape hatch, prompt changes, and backtick extension) is larger. **Tiebreaker**: Scoring the core A3 proposal as described in the brainstorm, not the Advocate's rebuttal extensions. The base proposal is ~60-100 lines of production code with 2-3 files modified.

**Final Score: 7**

### Dimension 3: False Positive Risk (Weight: 0.15)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 7 | Pass 1 is deterministic against a well-defined ID set. False positives are limited to intentional deferrals (addressable with a deferred-requirements section) and ID format mismatches (addressable with regex tuning). The two-pass architecture allows Pass 2 to provide context for ambiguous cases. |
| Skeptic | 5 | Pass 1's veto power means any false positive blocks the pipeline with no LLM override. Intentional deferrals, requirement decomposition (sub-IDs), and ID format evolution all produce false positives. The Advocate's escape hatch adds complexity and is not in the base proposal. Backtick extension would significantly increase false positive rate. |

**Score difference: 2.** At the boundary. The Advocate's point about the deferred-requirements section is a reasonable mitigation. The Skeptic's point about veto-without-override is valid for the base proposal as written. **Tiebreaker**: The base proposal specifies veto power for Pass 1, which means false positives from intentional omissions will block pipelines. An override mechanism is needed but not specified.

**Final Score: 6**

### Dimension 4: Maintainability (Weight: 0.15)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 7 | The regex patterns auto-discover IDs from document content. No manual configuration per release. Updates only needed when ID schema changes (rare). The extraction function is a pure function, easily unit-tested. Pre-checks infrastructure is a stable extension point. |
| Skeptic | 5 | Regex patterns need updates for new ID schemes. Prompt coupling between Pass 1 and Pass 2 adds a maintenance surface. False positive tuning is ongoing. The interaction between pre_checks and semantic_checks must be maintained through gate_passed() evolution. Over 5+ releases, the ID format will evolve and the gate must track it. |

**Score difference: 2.** At the boundary. The Advocate correctly notes that ID schema changes are infrequent. The Skeptic correctly notes that prompt coupling and format evolution are real maintenance costs. **Tiebreaker**: The core mechanism (regex + set difference) is inherently low-maintenance. The prompt coupling is the primary risk but is bounded.

**Final Score: 6**

### Dimension 5: Composability (Weight: 0.10)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 9 | Directly enables 4 other proposals. The pre_checks infrastructure is reusable. The extract_requirement_ids() function is consumed by multiple downstream gates. Establishes the "deterministic floor + LLM ceiling" pattern used by Brainstorm 04. Fits the existing GateCriteria/SemanticCheck pattern with a natural extension. |
| Skeptic | 7 | Composability benefits are real but shared with the simpler A1 proposal. The pre_checks infrastructure is useful but Option A (embedding in SemanticCheck) would not provide it. The context injection into Pass 2 is A3-specific and not reusable by other proposals. Composability score should reflect A3's unique contribution over A1, which is modest. |

**Score difference: 2.** At the boundary. The Advocate's composability argument is strong regardless of A1 comparison -- the pre_checks extension point (Option B) is genuinely enabling infrastructure. The Skeptic's point that A1 shares some composability benefits is valid but does not diminish A3's contribution.

**Final Score: 8**

---

## Weighted Score Calculation

```
Final Scores:
  Likelihood to Succeed:    7
  Implementation Complexity: 7
  False Positive Risk:       6
  Maintainability:           6
  Composability:             8

Weighted Score = (7 * 0.35) + (7 * 0.25) + (6 * 0.15) + (6 * 0.15) + (8 * 0.10)
               = 2.45 + 1.75 + 0.90 + 0.90 + 0.80
               = 6.80
```

**Final Weighted Score: 6.80**

**Interpretation**: Good candidate -- implement after high-priority items (6.0-7.9 range). The proposal's deterministic floor mechanism is sound and its composability is strong, but its effectiveness depends on an upstream prerequisite (formal ID assignment) that is not currently in place. The false positive risk from Pass 1's veto power without an override mechanism is a concrete concern that should be resolved before implementation.

---

## Recommendations

1. **If implementing A3**: Pair it with a prompt modification to `build_extract_prompt()` that mandates exhaustive `FR-NNN`/`NFR-NNN`/`SC-NNN` assignment. Without this, Pass 1 operates on an incomplete ID set.
2. **Consider A1 first**: If implementation bandwidth is limited, A1 (set-difference check without LLM context injection) captures most of A3's value at lower complexity. A3 can layer on top later.
3. **Add an override mechanism**: Pass 1's veto power should support a `## Deferred Requirements` section in the roadmap that explicitly lists IDs the team chose not to address. Pass 1 excludes deferred IDs from the missing set.
4. **Use Option B for integration**: The `pre_checks` extension to `GateCriteria` is more composable than embedding manifests in prompts (Option A). The marginal implementation cost is justified by reuse across proposals 02-05.
