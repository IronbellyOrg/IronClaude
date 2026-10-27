# ISS-011 Refactoring Proposals

> **Issue**: `spec_patch.py` not mentioned in v3.05 spec at all.
>
> **Spec Says**: No mention -- not in `relates_to` frontmatter, not in any FR, not in scope boundary, not in resolved questions.
>
> **Reality**: `spec_patch.py` is active production code (305 lines). Two import sites:
> - `commands.py:210` -- `prompt_accept_spec_change` (the `accept-spec-change` CLI subcommand)
> - `executor.py:1397` -- `scan_accepted_deviation_records` (auto-resume after spec-fidelity failure)
>
> **What spec_patch.py does**: Handles the accepted-deviation workflow -- when a spec changes during a pipeline run, deviation records (`dev-*-accepted-deviation.md`) with `spec_update_required: true` allow the spec hash to be reconciled without re-running the full cascade. This is a spec-hash reconciliation layer that sits between the spec-fidelity gate and the resume mechanism.
>
> **Why it matters for v3.05**: The v3.05 spec introduces `spec_hash`-based registry resets (FR-6 AC: "Registry resets when `spec_hash` changes") and convergence-mode gate authority (FR-7). Both interact with spec_patch.py's hash reconciliation. If the spec is silent about this module, implementers may accidentally break the accepted-deviation workflow when wiring the new convergence engine.
>
> **Upstream check**: No CRITICAL or HIGH resolutions address this. ISS-023 (LOW) covers a related gap (`prompts.py:build_spec_fidelity_prompt()` role undocumented) but does not mention spec_patch.py.

---

## Proposal #1: Add spec_patch.py to Scope Boundary as Preserved Coexisting Module (RECOMMENDED)

**Strategy**: Add spec_patch.py to two locations: (1) the `relates_to` frontmatter, and (2) the Scope Boundary section (Section 1.2) as explicitly preserved and coexisting with v3.05. This is the minimal correct change -- it makes the spec aware of the module without requiring any FR changes.

### Exact Spec Text Changes

**Frontmatter `relates_to` list (lines 11-23) -- add one entry:**

BEFORE:
```yaml
relates_to:
  - src/superclaude/cli/roadmap/executor.py
  - src/superclaude/cli/roadmap/prompts.py
  - src/superclaude/cli/roadmap/gates.py
  - src/superclaude/cli/roadmap/remediate.py
  - src/superclaude/cli/roadmap/remediate_executor.py
  - src/superclaude/cli/roadmap/fidelity.py
  - src/superclaude/cli/roadmap/convergence.py
  - src/superclaude/cli/roadmap/semantic_layer.py
  - src/superclaude/cli/roadmap/deviation_registry.py
  - src/superclaude/cli/roadmap/structural_checkers.py
  - src/superclaude/cli/roadmap/spec_parser.py
  - src/superclaude/cli/roadmap/models.py
  - src/superclaude/cli/roadmap/commands.py
```

AFTER:
```yaml
relates_to:
  - src/superclaude/cli/roadmap/executor.py
  - src/superclaude/cli/roadmap/prompts.py
  - src/superclaude/cli/roadmap/gates.py
  - src/superclaude/cli/roadmap/remediate.py
  - src/superclaude/cli/roadmap/remediate_executor.py
  - src/superclaude/cli/roadmap/fidelity.py
  - src/superclaude/cli/roadmap/convergence.py
  - src/superclaude/cli/roadmap/semantic_layer.py
  - src/superclaude/cli/roadmap/deviation_registry.py
  - src/superclaude/cli/roadmap/structural_checkers.py
  - src/superclaude/cli/roadmap/spec_parser.py
  - src/superclaude/cli/roadmap/models.py
  - src/superclaude/cli/roadmap/commands.py
  - src/superclaude/cli/roadmap/spec_patch.py
```

**Section 1.2 Scope Boundary (lines 54-58) -- add preserved-module clause:**

BEFORE:
```
### 1.2 Scope Boundary

**In scope**: Refactoring the fidelity comparison, severity classification,
deviation tracking, remediation editing, and convergence control subsystems.

**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step.
```

AFTER:
```
### 1.2 Scope Boundary

**In scope**: Refactoring the fidelity comparison, severity classification,
deviation tracking, remediation editing, and convergence control subsystems.

**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step.

**Preserved and coexisting**: `spec_patch.py` (305 lines) handles the
accepted-deviation workflow -- spec-hash reconciliation and auto-resume after
spec-fidelity failure. It is imported by `commands.py:210`
(`prompt_accept_spec_change`) and `executor.py:1397`
(`scan_accepted_deviation_records`). This module is NOT modified by v3.05 but
coexists with the new convergence engine. Specifically:
- In legacy mode (`convergence_enabled=false`): spec_patch.py operates exactly
  as in v3.0 -- the `_apply_resume_after_spec_patch()` flow in executor.py
  detects accepted deviations and triggers auto-resume.
- In convergence mode (`convergence_enabled=true`): spec_patch.py is still
  available for the `accept-spec-change` CLI subcommand, but the auto-resume
  flow is superseded by the convergence engine's own 3-run budget (FR-7). The
  `_apply_resume_after_spec_patch()` code path is not reached because the
  convergence engine handles spec-fidelity internally.
- The `spec_hash` field used by spec_patch.py (in `.roadmap-state.json`) is
  the same field referenced by FR-6's registry reset condition. No conflict
  exists: spec_patch.py reads/writes the state file hash; FR-6's registry
  resets when the hash changes. Both mechanisms respond to spec changes but
  operate on different artifacts (state file vs. deviation registry).
```

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Add 1 frontmatter entry + expand Section 1.2 |

### Risk: LOW

- No FR renumbering. No acceptance criteria changes. No new dependencies.
- The added text is purely descriptive -- it documents existing behavior, not new requirements.
- Makes the interaction between `spec_hash` in spec_patch.py and FR-6's registry reset explicit, preventing implementer confusion.
- The convergence-mode behavior statement ("auto-resume flow is superseded") is verifiable from executor.py's `spec_fidelity_failed` check -- in convergence mode, spec-fidelity is never invoked (FR-7), so the condition at executor.py:1335-1340 is never true.

### Requires Code Changes: NO

spec_patch.py is preserved as-is. The proposal documents existing behavior.

---

## Proposal #2: Add FR-7 Acceptance Criterion for spec_patch.py Coexistence

**Strategy**: In addition to Proposal #1's scope boundary text, add an explicit acceptance criterion to FR-7 that requires the convergence engine to not break the spec_patch.py workflow. This makes the coexistence requirement testable.

### Exact Spec Text Changes

**All changes from Proposal #1, PLUS:**

**FR-7 Acceptance Criteria (after line 365) -- add one item:**

BEFORE:
```
- [ ] `convergence_enabled: bool = False` field on pipeline config (default preserves legacy behavior)
```

AFTER:
```
- [ ] `convergence_enabled: bool = False` field on pipeline config (default preserves legacy behavior)
- [ ] In legacy mode, the `spec_patch.py` accepted-deviation workflow (`_apply_resume_after_spec_patch` in executor.py) operates unchanged -- spec-fidelity failure triggers deviation-file scan and optional auto-resume
- [ ] In convergence mode, the `_apply_resume_after_spec_patch` code path is unreachable (spec-fidelity gate is never invoked, so the `spec_fidelity_failed` condition at executor.py:1335 is always false)
```

**FR-6 Acceptance Criteria (after line 327) -- add one item:**

BEFORE:
```
- [ ] Registry resets when `spec_hash` changes (new spec version)
```

AFTER:
```
- [ ] Registry resets when `spec_hash` changes (new spec version)
- [ ] Registry reset uses the same `spec_hash` field in `.roadmap-state.json` that `spec_patch.py` reads/writes -- no duplicate or conflicting hash storage
```

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Proposal #1 changes + 3 new AC items across FR-6 and FR-7 |

### Risk: MEDIUM

- Adds testable acceptance criteria, which is stronger than Proposal #1.
- However, the AC items reference specific executor.py line numbers and internal function names (`_apply_resume_after_spec_patch`), which is more implementation-specific than other AC items in the spec.
- If the convergence engine implementation restructures executor.py (e.g., extracting the convergence loop into its own orchestrator), these AC items may need updating.
- The FR-6 AC about shared `spec_hash` is arguably already implied by "Registry resets when `spec_hash` changes" -- making it explicit may be redundant.

### Requires Code Changes: NO

Same as Proposal #1 -- spec_patch.py is preserved as-is.

---

## Proposal #3: Add Resolved Question Documenting the spec_patch.py Decision

**Strategy**: Add a new Resolved Question (Q#12) that explicitly documents the decision to preserve spec_patch.py. Combine with a minimal scope boundary addition (shorter than Proposal #1). This follows the spec's existing pattern for design decisions.

### Exact Spec Text Changes

**Frontmatter `relates_to` -- same addition as Proposal #1.**

**Section 1.2 Scope Boundary -- minimal addition:**

BEFORE:
```
**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step.
```

AFTER:
```
**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step.

**Preserved legacy**: `spec_patch.py` (accepted-deviation workflow) -- see
Resolved Question #12.
```

**Section 6 Resolved Questions (after Q#11, line 552) -- add Q#12:**

```
| 12 | How does spec_patch.py interact with v3.05? | **Preserved and coexisting.** `spec_patch.py` handles the accepted-deviation workflow (spec-hash reconciliation, auto-resume after spec-fidelity failure). It is active in production with two call sites: `commands.py:210` and `executor.py:1397`. In legacy mode, it operates unchanged. In convergence mode, its auto-resume path is unreachable (spec-fidelity gate is never invoked per FR-7), but the `accept-spec-change` CLI subcommand remains available. The `spec_hash` field in `.roadmap-state.json` is shared between spec_patch.py and FR-6's registry reset -- both respond to spec changes but operate on different artifacts. No modification to spec_patch.py is required. |
```

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Add 1 frontmatter entry + 1 scope boundary line + 1 resolved question |

### Risk: LOW

- Follows the spec's existing pattern -- Resolved Questions is where design decisions are documented (Q#1-11 cover analogous scoping decisions).
- Keeps the scope boundary section concise (one line + cross-reference vs. Proposal #1's multi-paragraph addition).
- The resolved question format naturally accommodates the "legacy mode vs. convergence mode" dual-path explanation.
- Slightly less discoverable than Proposal #1 -- an implementer scanning Section 1.2 sees only a one-line reference, not the full rationale.

### Requires Code Changes: NO

Same as Proposals #1 and #2 -- spec_patch.py is preserved as-is.

---

## Summary Comparison

| # | Proposal | Disruption | Testable | Self-Contained | Risk |
|---|----------|-----------|----------|----------------|------|
| 1 | Scope boundary + frontmatter | Low | No (descriptive only) | Yes | LOW |
| 2 | Scope boundary + FR-6/FR-7 AC items | Medium | Yes (3 new AC items) | Yes | MEDIUM |
| 3 | Resolved Question #12 + minimal scope boundary | Low | No (descriptive only) | Yes (via cross-ref) | LOW |

**Recommendation**: Proposal #1. It is the most direct fix for an omission-type issue: the spec simply needs to acknowledge spec_patch.py exists and explain how it coexists with v3.05. The scope boundary is the natural location for "this module is preserved" statements. Proposal #2 adds testable AC but at the cost of implementation-specific references that may become stale. Proposal #3 is a good alternative if the team prefers the Resolved Questions pattern for design rationale.
