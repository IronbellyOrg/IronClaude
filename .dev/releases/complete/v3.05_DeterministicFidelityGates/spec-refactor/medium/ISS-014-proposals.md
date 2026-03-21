# ISS-014: validate_semantic_high() Referenced in Docstring but Never Defined

**Issue**: `validate_semantic_high()` is referenced in the docstring of `wire_debate_verdict()` at `semantic_layer.py:321` but no function definition exists anywhere in the codebase. The spec (FR-4.1) describes the protocol this function should implement but never specifies a function signature or acceptance criterion for its existence.

**Severity**: MEDIUM (omission-type: spec assumes the function exists but does not specify it)

**Affected Spec Section**: FR-4.1 (Lightweight Debate Protocol), lines 194-239

**Source of Truth**: `src/superclaude/cli/roadmap/semantic_layer.py` at commit `f4d9035`

**Relationship to ISS-002**: ISS-002 (CRITICAL) reclassifies semantic_layer.py from CREATE to MODIFY and adds `validate_semantic_high()` to the list of functions to implement. ISS-014 is the complementary issue: it addresses the *spec text gap* that omits the function's signature, contract, and acceptance criterion. ISS-002 says "this function must be added"; ISS-014 says "the spec must define what this function does."

---

## Proposal #1: Add validate_semantic_high() Signature and AC to FR-4.1 (RECOMMENDED)

**Rationale**: The most targeted fix. FR-4.1 already describes the debate protocol in prose (roles, protocol steps 1-7, scoring rubric, token budget, YAML parse failure handling). What is missing is an explicit function specification and an acceptance criterion. This proposal adds both without restructuring the spec.

### Spec Text Changes

**Change 1 — Insert function specification after FR-4.1 Protocol table (after line 216)**

The current spec goes directly from the protocol steps (lines 209-216) to the scoring rubric (lines 218-226). Insert the function specification between them.

BEFORE (lines 216-218):
```
7. Write debate output YAML to `output_dir/debates/{finding.stable_id}/debate.yaml`

**Scoring Rubric** (4 criteria, each 0-3 points):
```

AFTER:
```
7. Write debate output YAML to `output_dir/debates/{finding.stable_id}/debate.yaml`

**Orchestrator Function**:

```python
def validate_semantic_high(
    finding: Finding,
    registry: DeviationRegistry,
    output_dir: Path,
    *,
    claude_process_factory: Callable | None = None,
) -> str:
    """Orchestrate lightweight adversarial debate for a semantic HIGH finding.

    Implements FR-4.1 protocol steps 1-7:
    1. Build prosecutor + defender prompts from finding context
    2. Execute both via ClaudeProcess in parallel (2 LLM calls)
    3. Parse YAML responses; default scores to 0 on parse failure
    4. Score both via score_argument() against 4-criterion rubric
    5. Compute verdict via judge_verdict()
    6. Write debate YAML to output_dir/debates/{stable_id}/debate.yaml
    7. Call wire_debate_verdict() to update registry

    Args:
        finding: The semantic HIGH finding to validate.
        registry: Active deviation registry for verdict recording.
        output_dir: Directory for debate output artifacts.
        claude_process_factory: Optional factory for ClaudeProcess creation
            (default: None uses standard ClaudeProcess). Enables testing
            without live LLM calls.

    Returns:
        Verdict string: "CONFIRM_HIGH", "DOWNGRADE_TO_MEDIUM", or
        "DOWNGRADE_TO_LOW".
    """
```

**Scoring Rubric** (4 criteria, each 0-3 points):
```

**Change 2 — Add acceptance criterion to FR-4.1 AC list (after line 239)**

BEFORE (lines 234-239):
```
**Acceptance Criteria** (FR-4.1):
- [ ] Prosecutor and defender execute in parallel (2 LLM calls, not sequential)
- [ ] Judge is deterministic Python — same scores always produce the same verdict
- [ ] Conservative tiebreak: margin within ±0.15 always produces CONFIRM_HIGH
- [ ] Debate output YAML written per finding with rubric scores, margin, and verdict
- [ ] Registry updated with `debate_verdict` and `debate_transcript` reference after each debate
```

AFTER:
```
**Acceptance Criteria** (FR-4.1):
- [ ] `validate_semantic_high()` exists in semantic_layer.py and implements protocol steps 1-7
- [ ] `validate_semantic_high()` accepts a `claude_process_factory` parameter for test injection
- [ ] Prosecutor and defender execute in parallel (2 LLM calls, not sequential)
- [ ] Judge is deterministic Python — same scores always produce the same verdict
- [ ] Conservative tiebreak: margin within ±0.15 always produces CONFIRM_HIGH
- [ ] Debate output YAML written per finding with rubric scores, margin, and verdict
- [ ] Registry updated with `debate_verdict` and `debate_transcript` reference after each debate
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-4.1: insert function spec + 2 new acceptance criteria)

### Risk: **LOW**
Additive only. Inserts a function specification and two acceptance criteria. No existing text is changed. The function signature matches the existing calling convention implied by `wire_debate_verdict()` (which expects a registry, finding, verdict, and transcript_path). The `claude_process_factory` parameter follows the established pattern from `executor.py` and `remediate_executor.py`.

### Requires Code Changes: **YES**
- Implement `validate_semantic_high()` in `semantic_layer.py`. The function body must orchestrate the protocol already described in FR-4.1 prose, connecting existing primitives (`score_argument()`, `judge_verdict()`, `wire_debate_verdict()`) with new parallel ClaudeProcess calls.

### Interaction with ISS-002
If ISS-002 Proposal #1 is also adopted, its FR-4.1 AC change (adding `validate_semantic_high() orchestrator function exists and is callable`) should be replaced by this proposal's more specific criteria. The two are compatible but this proposal supersedes ISS-002's one-line AC for ISS-014's scope.

---

## Proposal #2: Fix the Docstring Reference + Add Minimal AC

**Rationale**: A lighter-touch approach. Rather than specifying the full function signature in the spec, fix the dangling docstring reference in the code and add a single acceptance criterion to FR-4.1. The spec describes *what* the function must do (protocol steps 1-7) but leaves the *how* (signature, parameters) to the implementer.

### Spec Text Changes

**Change 1 — Add one acceptance criterion to FR-4.1 (after line 239)**

BEFORE (line 234):
```
**Acceptance Criteria** (FR-4.1):
```

AFTER:
```
**Acceptance Criteria** (FR-4.1):
- [ ] `validate_semantic_high()` orchestrator exists in semantic_layer.py, implementing protocol steps 1-7 and callable from `run_semantic_layer()`
```

(All other existing criteria remain unchanged.)

**Change 2 — Add implementation note to FR-4 description (after line 178)**

BEFORE (lines 177-178):
```
triggers a lightweight adversarial debate to validate the rating.

**Semantic/structural boundary**:
```

AFTER:
```
triggers a lightweight adversarial debate to validate the rating.

**Implementation note**: The debate orchestration function `validate_semantic_high()`
is called by `run_semantic_layer()` for each semantic HIGH finding. It connects
the existing scoring primitives (`score_argument()`, `judge_verdict()`,
`wire_debate_verdict()`) with parallel ClaudeProcess execution per FR-4.1.

**Semantic/structural boundary**:
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-4 description + FR-4.1 AC)

### Code Changes Required: **YES**
- Implement `validate_semantic_high()` in `semantic_layer.py`
- Update docstring of `wire_debate_verdict()` at line 321 to remove the forward-reference or mark it as "see validate_semantic_high() above"

### Risk: **VERY LOW**
Two small additive text insertions. No restructuring. The implementation note makes the docstring reference coherent without requiring the spec to carry a full function signature.

### Interaction with ISS-002
Fully compatible. ISS-002 Proposal #1 adds a similar AC line; this proposal's wording is slightly more specific (names the caller `run_semantic_layer()` and the connection to existing primitives).

---

## Proposal #3: Elevate validate_semantic_high() to a Named Sub-Requirement (FR-4.3)

**Rationale**: The function is complex enough (parallel LLM orchestration, YAML parsing, error handling, artifact output, registry wiring) that it warrants its own sub-requirement rather than being buried in FR-4.1's acceptance criteria. This gives it explicit scope, its own acceptance criteria, and a clear dependency chain.

### Spec Text Changes

**Change 1 — Insert new sub-requirement after FR-4.2 (after line 274)**

INSERT:
```markdown
#### FR-4.3: Semantic HIGH Validation Orchestrator

**Description**: `validate_semantic_high()` is the orchestration function that
implements the FR-4.1 lightweight debate protocol. It connects the existing
scoring primitives with parallel ClaudeProcess execution and produces auditable
debate artifacts.

**Function Contract**:

| Parameter | Type | Purpose |
|-----------|------|---------|
| finding | Finding | Semantic HIGH finding to validate |
| registry | DeviationRegistry | For recording verdict via wire_debate_verdict() |
| output_dir | Path | Parent dir for debate artifacts |
| claude_process_factory | Callable \| None | Test injection point (default: standard ClaudeProcess) |
| **Returns** | str | Verdict: CONFIRM_HIGH, DOWNGRADE_TO_MEDIUM, or DOWNGRADE_TO_LOW |

**Error Handling**:
- YAML parse failure on either side: all rubric scores default to 0 for that side (per FR-4.1)
- ClaudeProcess timeout: treat as YAML parse failure (scores = 0)
- Both sides fail: conservative default → CONFIRM_HIGH

**Acceptance Criteria** (FR-4.3):
- [ ] `validate_semantic_high()` exists in semantic_layer.py
- [ ] Calls ClaudeProcess in parallel for prosecutor and defender (2 concurrent calls)
- [ ] Parses YAML responses; handles parse failures by zeroing scores
- [ ] Calls `score_argument()` and `judge_verdict()` for deterministic verdict
- [ ] Writes debate YAML to `output_dir/debates/{finding.stable_id}/debate.yaml`
- [ ] Calls `wire_debate_verdict()` to update registry with verdict and transcript path
- [ ] Returns verdict string usable by `run_semantic_layer()` caller
- [ ] Accepts `claude_process_factory` for test injection without live LLM

**Dependencies**: FR-4.1 (protocol definition), FR-6 (registry)
```

**Change 2 — Update FR-4 Dependencies line (line 274)**

BEFORE:
```
**Dependencies**: FR-1 (structural findings as input), FR-6 (deviation registry)
```

AFTER:
```
**Dependencies**: FR-1 (structural findings as input), FR-6 (deviation registry), FR-4.3 (semantic HIGH orchestrator)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (new FR-4.3 section + FR-4 dependency update)

### Risk: **LOW-MEDIUM**
Additive (new sub-requirement). Slightly increases spec surface area. The function contract is detailed enough to be directly implementable but rigid enough that signature changes would require a spec amendment. This is appropriate for a function that sits on the critical path of the debate protocol.

### Requires Code Changes: **YES**
- Implement `validate_semantic_high()` per the contract in `semantic_layer.py`

### Interaction with ISS-002
Supersedes ISS-002's one-line AC addition for `validate_semantic_high()`. If both are adopted, ISS-002's AC line should reference FR-4.3 instead of inlining the criterion.

---

## Ranking Summary

| Rank | Proposal | Disruption | Correctness | Completeness | Recommendation |
|------|----------|-----------|-------------|--------------|----------------|
| 1 | **#1: Signature + AC in FR-4.1** | Low | High | High | **Best balance: specifies the function without over-structuring** |
| 2 | **#2: Minimal AC + impl note** | Very Low | High | Medium | Best if ISS-002 is already doing the heavy lifting |
| 3 | **#3: New FR-4.3 sub-requirement** | Medium | Highest | Highest | Best if the function warrants its own requirement scope |

**Recommended approach**: **Proposal #1**. It provides a concrete function signature (making the implementation unambiguous), adds testability via the factory parameter, and integrates cleanly into FR-4.1 without creating new sub-requirement numbering. If ISS-002 Proposal #1 is also adopted, this proposal's AC lines replace ISS-002's single `validate_semantic_high()` AC with more specific criteria.

**If ISS-002 is NOT being resolved**: Proposal #1 still works standalone -- it does not depend on ISS-002's baseline acknowledgment. The function specification is self-contained within FR-4.1.
