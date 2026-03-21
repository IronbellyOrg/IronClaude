# ISS-007: MorphLLM vs ClaudeProcess remediation model design gap -- Proposals

## Issue Summary

FR-9 describes "MorphLLM-compatible lazy edit snippets" as the remediation model and specifies MorphLLM as the patch applicator ("MorphLLM applies patches via semantic merging"). In reality, all remediation in the codebase uses `ClaudeProcess` -- the established subprocess pattern used across `executor.py`, `validate_executor.py`, and `remediate_executor.py`. MorphLLM exists only as an external MCP server (`morphllm-fast-apply`) requiring `MORPH_API_KEY` and has zero integration points in the roadmap pipeline.

The spec conflates two concerns: (1) the **patch data format** (JSON schema with `original_code`, `instruction`, `update_snippet`) and (2) the **execution engine** that applies patches. The format is engine-agnostic, but the spec reads as if MorphLLM is the primary applicator with a fallback, when in practice ClaudeProcess is the only available engine.

## CRITICAL Dependency Check

**ISS-003 (CRITICAL)** must be applied first. ISS-003 addresses the fundamental misframing of `remediate_executor.py` as a CREATE operation when it already exists (563 lines). ISS-003's recommended Proposal #1 rewrites the FR-9 Description block with a v3.0 baseline inventory and delta list. That rewrite is the **textual anchor** for all three proposals below -- each modifies the FR-9 Description, Patch Format subsection, or Acceptance Criteria, which ISS-003 also touches.

Specifically:
- ISS-003 Proposal #1 already adds `check_morphllm_available()` and `fallback_apply()` to the delta list but does NOT resolve the language around MorphLLM being the primary engine
- ISS-007 proposals below assume ISS-003's baseline/delta framing is in place and refine the MorphLLM-vs-ClaudeProcess language within that structure
- If ISS-003 is not applied first, the "Before" text in all proposals below matches the current spec; if ISS-003 IS applied first, the "Before" text needs to be read against ISS-003's "After" output instead

**ISS-004, ISS-005, ISS-006** (all HIGH) also affect FR-9 but are orthogonal to this issue -- they concern threshold values, granularity, and rollback scope, not the execution engine.

## Codebase Ground Truth

**Remediation execution model** (`src/superclaude/cli/roadmap/remediate_executor.py`):
- All remediation runs through `ClaudeProcess` (line 24: `from ..pipeline.process import ClaudeProcess`)
- `_run_agent_for_file()` (lines 161-211) builds a prompt, spawns a `ClaudeProcess`, and waits for completion
- The agent receives the full file content inline and edits it directly -- there is no structured patch intermediate format
- `_check_diff_size()` (lines 416-473) compares the `.pre-remediate` snapshot against the post-edit file as a whole-file diff
- No `RemediationPatch` dataclass exists anywhere in the codebase
- No `apply_patches()`, `fallback_apply()`, or `check_morphllm_available()` functions exist
- No MorphLLM import, integration, or reference exists in any Python source file

**MorphLLM existence** (documentation only):
- Referenced in docs as MCP server `morphllm-fast-apply` (user-guide, flags docs)
- Listed as optional MCP server requiring `MORPH_API_KEY`
- Zero call sites in pipeline code
- Zero test coverage

**ClaudeProcess usage pattern** (established across pipeline):
- `executor.py:281` -- main pipeline step execution
- `validate_executor.py:117` -- validation step execution
- `remediate_executor.py:198` -- remediation agent execution
- This is the only subprocess pattern in the pipeline; all LLM work goes through it

## Proposal A: ClaudeProcess-Primary with MorphLLM-Compatible Format (Adapter Pattern)

### Approach

Reframe FR-9 to make ClaudeProcess the primary (and currently only) execution engine. Retain the MorphLLM-compatible JSON patch schema as the **data format** but decouple it from the execution engine. Introduce an explicit adapter interface so that MorphLLM can be swapped in later without changing the patch generation or validation logic.

### Before (Current Spec Text)

FR-9 Description (lines 411-417):
```
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

FR-9 Patch Format subsection (lines 419-433):
```
**Patch Format (MorphLLM Lazy Snippets)**:
Patches use MorphLLM's semantic merging format, NOT unified diffs:
...
Context markers (`// ... existing code ...`) indicate unchanged regions.
MorphLLM applies edits via semantic understanding, tolerating minor
line-number or formatting discrepancies.
```

FR-9 Acceptance Criteria (lines 436-438):
```
- [ ] Remediation agents output MorphLLM-compatible lazy edit snippets per finding
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] MorphLLM (when available) applies patches via semantic merging
```

### After (Proposed Spec Text)

FR-9 Description (replaces lines 411-417, assumes ISS-003 baseline/delta is applied):
```
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Extends the existing `remediate_executor.py` (see v3.0 Baseline)
to produce structured patches in a MorphLLM-compatible JSON format, applied via
ClaudeProcess (the established pipeline execution engine). The patch format is
engine-agnostic: a future migration to MorphLLM requires only swapping the
applicator, not the patch generation or validation logic. The per-file diff-size
guard is narrowed to per-patch granularity with a reduced threshold (50% -> 30%),
and rollback is changed from all-or-nothing to per-file. Full document
regeneration requires explicit user consent.
```

FR-9 Patch Format subsection (replaces lines 419-433):
```
**Patch Format (Engine-Agnostic Lazy Snippets)**:
Patches use a JSON schema compatible with MorphLLM's semantic merging format.
This format is NOT tied to MorphLLM as execution engine -- it is a structured
intermediate representation that any applicator can consume:
{
  "target_file": "roadmap.md",
  "finding_id": "SIG-001",
  "original_code": "<relevant section from current file>",
  "instruction": "Replace phantom FR-009 reference with correct G-001 ID",
  "update_snippet": "// ... existing code ...\n<changed lines>\n// ... existing code ...",
  "rationale": "Roadmap references FR-009 which does not exist in spec ID set"
}
Context markers (`// ... existing code ...`) indicate unchanged regions.

**Applicator Selection**:
1. **Primary**: `ClaudeProcess` -- generates and applies patches via LLM subprocess
   (established pattern; same as executor.py and validate_executor.py)
2. **Fallback**: Deterministic Python text replacement using `original_code` as
   anchor (minimum anchor: 5 lines or 200 chars). Used when ClaudeProcess fails
   or for simple substitutions.
3. **Future**: MorphLLM MCP (`morphllm-fast-apply`) -- when integrated, replaces
   ClaudeProcess as applicator. `check_morphllm_available()` probes MCP runtime.
   Patch format requires zero changes for this migration.
```

FR-9 Acceptance Criteria (replaces lines 436-438):
```
- [ ] Remediation agents output structured lazy edit snippets per finding (MorphLLM-compatible JSON format)
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] ClaudeProcess applies patches as primary engine; fallback applicator handles failures
- [ ] `check_morphllm_available()` probes MCP runtime; when True, MorphLLM replaces ClaudeProcess as applicator
```

### Trade-offs

**Pros**:
- Matches codebase reality: ClaudeProcess is the only working engine
- Preserves the MorphLLM-compatible format for future migration
- Explicit adapter pattern makes the migration path concrete
- Three-tier applicator hierarchy (ClaudeProcess -> fallback -> future MorphLLM) is clear
- No speculative infrastructure -- does not require MorphLLM integration to ship

**Cons**:
- More text than current spec (adds Applicator Selection subsection)
- `check_morphllm_available()` is speculative -- MorphLLM may never be integrated
- Slightly more complex than Proposal B (retains MorphLLM future path)

---

## Proposal B: ClaudeProcess-Only with Format-Forward Design (Drop MorphLLM References)

### Approach

Remove all MorphLLM references from FR-9 entirely. Frame the patch format as a pipeline-internal structured format that happens to be compatible with external tools. This is the most honest representation of current reality and eliminates speculative infrastructure.

### Before (Current Spec Text)

Same as Proposal A (lines 411-417, 419-433, 436-438).

### After (Proposed Spec Text)

FR-9 Description:
```
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Extends the existing `remediate_executor.py` (see v3.0 Baseline)
to produce structured patches as typed JSON edit snippets instead of freeform
ClaudeProcess file rewrites. A per-patch diff-size guard rejects any individual
edit that modifies more than 30% of the target file. Full document regeneration
requires explicit user consent.
```

FR-9 Patch Format subsection:
```
**Patch Format (Structured Edit Snippets)**:
Patches use a typed JSON schema with semantic context markers:
{
  "target_file": "roadmap.md",
  "finding_id": "SIG-001",
  "original_code": "<relevant section from current file>",
  "instruction": "Replace phantom FR-009 reference with correct G-001 ID",
  "update_snippet": "// ... existing code ...\n<changed lines>\n// ... existing code ...",
  "rationale": "Roadmap references FR-009 which does not exist in spec ID set"
}
Context markers (`// ... existing code ...`) indicate unchanged regions.

**Application**:
1. **Primary**: `ClaudeProcess` generates patches via LLM subprocess, then applies
   them to the target file using the `original_code` field as an anchor.
2. **Fallback**: Deterministic Python text replacement using `original_code` as
   anchor (minimum anchor: 5 lines or 200 chars). Used when ClaudeProcess fails.
```

FR-9 Acceptance Criteria:
```
- [ ] Remediation agents output structured edit snippets per finding (typed JSON format)
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] ClaudeProcess applies patches as primary engine; deterministic fallback handles failures
```

Remove from Acceptance Criteria:
```
- [ ] MorphLLM (when available) applies patches via semantic merging  (DELETED)
```

Remove from Resolved Questions Q#3:
```
| 3 | What is the patch schema for MorphLLM integration? | **Lazy edit snippets with semantic merging.** ... |
```

Replace with:
```
| 3 | What is the patch schema for structured remediation? | **Lazy edit snippets with anchor-based application.** Remediation agents produce typed JSON patches with `original_code` anchors and `update_snippet` replacements. Context markers (`// ... existing code ...`) indicate unchanged regions. ClaudeProcess applies patches; deterministic Python fallback uses `original_code` as text-match anchor. |
```

### Trade-offs

**Pros**:
- Most honest: reflects exactly what exists and what will be built
- No speculative infrastructure (`check_morphllm_available()` dropped)
- Simpler spec -- fewer concepts, less conditional logic
- Eliminates the "MorphLLM (when available)" AC that can never be tested without external API key
- The JSON format is inherently compatible with MorphLLM if integration is desired later -- no spec change needed to adopt it

**Cons**:
- Loses explicit forward compatibility signal for MorphLLM migration
- If MorphLLM integration becomes a priority, the spec would need a follow-up amendment
- May feel like a regression to stakeholders who valued the MorphLLM integration story

---

## Proposal C: Pluggable Applicator Interface with Engine Registry

### Approach

Formalize the execution engine as a pluggable interface. Define an `ApplyEngine` protocol (Python Protocol class) with `apply(patch: RemediationPatch) -> bool`. Register `ClaudeProcessEngine` as the default, `DeterministicEngine` as fallback, and `MorphLLMEngine` as optional/future. This is the most architecturally complete approach.

### Before (Current Spec Text)

Same as Proposal A (lines 411-417, 419-433, 436-445).

### After (Proposed Spec Text)

FR-9 Description:
```
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Extends the existing `remediate_executor.py` (see v3.0 Baseline)
to produce structured patches as typed JSON edit snippets, applied through a
pluggable engine interface. The default engine is `ClaudeProcessEngine` (matching
the established pipeline pattern). A `DeterministicEngine` provides LLM-free
fallback. The patch format is engine-agnostic by design. The per-file diff-size
guard is narrowed to per-patch granularity with a reduced threshold (50% -> 30%),
and rollback is changed from all-or-nothing to per-file.
```

FR-9 new subsection (after Patch Format):
```
**Applicator Engine Interface**:

```python
class ApplyEngine(Protocol):
    def apply(self, patch: RemediationPatch, target_content: str) -> str | None:
        """Apply a single patch. Returns modified content or None on failure."""
        ...
```

| Engine | Type | When Used | LLM Calls |
|--------|------|-----------|-----------|
| `ClaudeProcessEngine` | Default | Always available | 1 per patch |
| `DeterministicEngine` | Fallback | ClaudeProcess failure, or simple substitutions | 0 |
| `MorphLLMEngine` | Optional | When `MORPH_API_KEY` set and MCP server available | 0 (API call) |

Engine selection: `ClaudeProcessEngine` unless overridden by config. Fallback
chain: configured engine -> `DeterministicEngine`. `MorphLLMEngine` is NOT
built in v3.05; the interface exists to enable future integration without
spec amendment.
```

FR-9 Acceptance Criteria:
```
- [ ] `ApplyEngine` Protocol defined with `apply(patch, target_content) -> str | None`
- [ ] `ClaudeProcessEngine` implements `ApplyEngine`, uses established ClaudeProcess subprocess pattern
- [ ] `DeterministicEngine` implements `ApplyEngine`, uses `original_code` as text-match anchor (minimum: 5 lines or 200 chars)
- [ ] Engine selection configurable via `RoadmapConfig.apply_engine: str = "claude"` (Literal["claude", "deterministic"])
- [ ] Remediation agents output structured edit snippets per finding (typed JSON format)
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
```

### Trade-offs

**Pros**:
- Most architecturally sound -- clean separation of concerns
- `ApplyEngine` Protocol makes the extension point explicit and testable
- Future engines (MorphLLM or others) can be added without modifying existing code
- Config-driven engine selection is the standard pattern in the pipeline (`PipelineConfig`)
- The Protocol is a single class with one method -- minimal interface surface

**Cons**:
- Most implementation work -- requires defining the Protocol, two concrete implementations, config field, and engine selection logic
- Over-engineering risk: if MorphLLM is never integrated, the interface is unused abstraction
- Adds a new config field (`apply_engine`) to `RoadmapConfig`, increasing configuration surface
- The `DeterministicEngine` may be rarely used in practice if ClaudeProcess is reliable
- Spec becomes more prescriptive about implementation patterns (Protocol class) than other FRs

---

## Recommended Proposal

**Proposal A: ClaudeProcess-Primary with MorphLLM-Compatible Format (Adapter Pattern)**.

Rationale:

1. **Matches codebase reality** without denying the MorphLLM integration path that was explicitly discussed in the adversarial design review (Resolved Question #3) and the Compatibility Report (Section 7c). Proposal B is more honest but discards context that stakeholders already reviewed and approved.

2. **Avoids over-engineering**. Proposal C's Protocol interface is architecturally clean but introduces abstraction that no current consumer needs. The pipeline has exactly one execution engine (ClaudeProcess) and the added indirection creates test surface without near-term value. If MorphLLM integration becomes real, a Protocol can be extracted then (YAGNI).

3. **ISS-003 alignment**. ISS-003's recommended Proposal #1 already lists `check_morphllm_available()` and `fallback_apply()` in the delta list. Proposal A's three-tier applicator hierarchy (ClaudeProcess -> fallback -> future MorphLLM) is consistent with that delta list without adding new functions beyond what ISS-003 already anticipates.

4. **Testability**. The primary path (ClaudeProcess) is testable with existing infrastructure. The fallback path (deterministic text replacement) is testable without any LLM. The MorphLLM path is explicitly marked as future and does not add untestable acceptance criteria.

**Dependency**: Apply ISS-003 first (reclassifies FR-9 from CREATE to MODIFY with baseline/delta). Then apply ISS-007 Proposal A to refine the MorphLLM-vs-ClaudeProcess language within ISS-003's rewritten FR-9 Description.
