# ISS-004: Diff-size threshold mismatch — Proposals

## Issue Summary

FR-9 specifies a 30% diff-size threshold for the per-patch guard. The codebase uses `_DIFF_SIZE_THRESHOLD_PCT = 50` at `src/superclaude/cli/roadmap/remediate_executor.py:45`. The 30% value was a deliberate adversarial-reviewed decision (BF-5) during the v1.1.0 spec amendment process. The constant is referenced at three usage sites (lines 453, 458, 467) in the `_check_diff_size()` function.

## CRITICAL Dependency Check

**ISS-003 (CRITICAL) directly affects this issue.** ISS-003 addresses the broader problem that `remediate_executor.py` is listed as CREATE in the spec but already exists. The recommended ISS-003 resolution (Proposal #1: Reclassify to MODIFY with Surgical Delta List) explicitly includes the threshold change as Delta item 5:

> `5. MODIFY _DIFF_SIZE_THRESHOLD_PCT: 50 -> 30 (ISS-004)`

**Consequence**: If ISS-003's recommended proposal is adopted, the FR-9 description will already contain the 50-to-30 delta callout, and the spec text will already say "the threshold is reduced from 50% to 30%." In that case, the ISS-004 resolution reduces to verifying that the ISS-003 spec change adequately covers the threshold mismatch, and ensuring the acceptance criteria and NFR text are consistent.

If ISS-003 is resolved with a *different* proposal (e.g., Proposal #5 minimal patch), then ISS-004 must independently fix the spec text to make the 30% threshold unambiguous.

**ISS-001 and ISS-002** (convergence.py and semantic_layer.py CREATE-vs-MODIFY) do not affect this issue.

## Codebase Ground Truth

**File**: `src/superclaude/cli/roadmap/remediate_executor.py`

- **Line 44**: Comment `# FR-9: Diff-size threshold (percentage of file changed)`
- **Line 45**: `_DIFF_SIZE_THRESHOLD_PCT = 50`
- **Line 453**: `if diff_pct > _DIFF_SIZE_THRESHOLD_PCT:` — gate check
- **Line 454-462**: `allow_regeneration=True` path — logs WARNING with threshold value, proceeds
- **Line 463-471**: `allow_regeneration=False` path — logs ERROR with threshold value, rejects

The constant is used correctly at all three sites (453, 458, 467). Changing the constant value from 50 to 30 is a single-line code change with no structural refactoring required.

**Spec locations referencing 30%**:
- FR-9 AC bullet 5: "Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)"
- FR-9.1 AC bullet 3: "Without flag: patches exceeding 30% threshold are rejected (FAILED)"
- FR-9.1 AC bullet 4: "With flag: patches exceeding 30% threshold are applied with WARNING log"
- NFR-5: "No file changes >30% without user consent"
- US-4: "validated against the diff-size guard (<=30% changed lines)"
- Appendix A Remediation Flow: "(<=30% changed lines)"

The spec is internally consistent at 30%. The code is the sole outlier at 50%.

---

## Proposal A: Spec-Only Fix — Add Explicit Threshold Assertion to FR-9 Description

### Approach

The spec already says 30% in six places. The problem is that the FR-9 *description* paragraph never states the numeric threshold explicitly — it says "a configurable percentage" and defers the 30% to the acceptance criteria. This proposal adds the explicit value to the description so that the spec-vs-code mismatch is impossible to miss during implementation. No AC changes needed (they already say 30%).

This approach is designed for the case where ISS-003 is NOT resolved first or is resolved with a minimal approach (Proposal #5).

### Before (Current Spec Text)

```markdown
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

### After (Proposed Spec Text)

```markdown
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than 30% of the target
file (configurable; current code uses 50% and MUST be changed to 30% per
BF-5 adversarial review). Full document regeneration requires explicit user
consent.
```

### Trade-offs

**Pros**:
- Minimal spec change (one sentence modified)
- Makes the threshold visible in the description, not just buried in AC bullets
- Explicitly calls out the code-vs-spec delta, preventing implementers from assuming 50% is correct
- No renumbering, no structural changes

**Cons**:
- Does not address the broader ISS-003 CREATE-vs-MODIFY framing
- "MUST be changed" language in a requirements spec is unusual — specs normally state the target, not the delta
- If ISS-003 Proposal #1 is later adopted, the description will be overwritten anyway, making this change wasted effort

---

## Proposal B: No Spec Change — Defer to ISS-003 Resolution

### Approach

ISS-003's recommended resolution (Proposal #1) already incorporates the threshold change as an explicit delta item. Rather than making a redundant spec change, mark ISS-004 as "resolved by ISS-003" and validate that the ISS-003 resolution covers all ISS-004 concerns.

This approach treats ISS-004 as a *symptom* of the larger ISS-003 problem (spec claims CREATE for existing code with different behavior). Resolving ISS-003 inherently resolves ISS-004.

### Before (Current Spec Text)

No change to spec. FR-9 description remains as-is.

### After (Proposed Spec Text)

No change to spec. ISS-004 is closed as "resolved by ISS-003" with the following validation checklist:

```markdown
**ISS-004 resolved by ISS-003** — Validation checklist:
- [ ] ISS-003 resolution explicitly lists threshold delta (50 -> 30)
- [ ] FR-9 description (as rewritten by ISS-003) mentions 30% threshold
- [ ] FR-9 AC bullet 5 still says "default 30%" (unchanged)
- [ ] NFR-5 still says ">30%" (unchanged)
- [ ] Code change `_DIFF_SIZE_THRESHOLD_PCT = 50` -> `30` is in ISS-003's delta list
```

### Trade-offs

**Pros**:
- Zero additional spec edits — avoids redundant changes that ISS-003 will overwrite
- Respects the dependency chain: fix the root cause (ISS-003), not the symptom (ISS-004)
- Simplifies the spec-refactor workflow — one fewer independent change to review and merge

**Cons**:
- ISS-004 resolution is blocked by ISS-003. If ISS-003 stalls, ISS-004 remains unresolved
- If ISS-003 is resolved with a *different* proposal that does not mention the threshold explicitly (e.g., Proposal #5), ISS-004 silently regresses
- Requires discipline to verify ISS-003's resolution actually covers ISS-004 before closing

---

## Proposal C: Belt-and-Suspenders — Add Threshold to FR-9 Description AND Cross-Reference ISS-003

### Approach

Add the explicit 30% value to the FR-9 description (like Proposal A) AND add a cross-reference note to ISS-003. This ensures ISS-004 is self-contained even if ISS-003's resolution changes, while also flagging the dependency for coordinators.

This approach is designed to be robust regardless of how ISS-003 is resolved.

### Before (Current Spec Text)

```markdown
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

### After (Proposed Spec Text)

```markdown
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than 30% of the target
file (threshold is configurable via `_DIFF_SIZE_THRESHOLD_PCT`). Full document
regeneration requires explicit user consent.

> **Implementation note (ISS-004)**: The v3.0 codebase sets
> `_DIFF_SIZE_THRESHOLD_PCT = 50`. This MUST be changed to `30` to match
> this spec. The 30% value was established during adversarial design review
> (BF-5) and is referenced in NFR-5, US-4, and FR-9.1. See also ISS-003
> for the broader CREATE-vs-MODIFY remediate_executor.py refactoring.
```

### Trade-offs

**Pros**:
- Self-contained: ISS-004 is fully resolved regardless of ISS-003 outcome
- The implementation note is clearly separated from the normative spec text (blockquote)
- Cross-reference to ISS-003 alerts implementers to the broader context
- Preserves all existing AC text (which already correctly says 30%)

**Cons**:
- If ISS-003 Proposal #1 is adopted, the FR-9 description will be rewritten and this implementation note may need to be removed or relocated to avoid duplication
- Implementation notes in specs can become stale — they describe a point-in-time code state
- Slightly more editorial weight than Proposal A

---

## Recommended Proposal

**Proposal B (defer to ISS-003)** if ISS-003 is being resolved first and the recommended Proposal #1 is adopted. ISS-003's delta list already explicitly covers the threshold change, making a separate ISS-004 spec edit redundant.

**Proposal C (belt-and-suspenders)** if ISS-003 resolution is uncertain or delayed. Proposal C ensures the 30% threshold is explicit in the FR-9 description regardless of ISS-003's outcome, while the implementation note provides migration context that can be removed once the code change lands.

In either case, the required code change is identical and trivial: `_DIFF_SIZE_THRESHOLD_PCT = 50` to `_DIFF_SIZE_THRESHOLD_PCT = 30` at `src/superclaude/cli/roadmap/remediate_executor.py:45`.
