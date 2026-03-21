# ISS-001 Refactoring Proposals

**Issue**: FR-7 (Convergence Gate) describes building a convergence engine as if greenfield, but `convergence.py` already exists (323 lines, commit `f4d9035`) with DeviationRegistry, compute_stable_id(), ConvergenceResult, _check_regression(), and temp dir isolation.

**Source**: Compatibility Report Section 1 (Module Existence Conflicts)

---

## Proposal #1: Minimal Reword — Change FR-7 Description Verb (RECOMMENDED)

**Rationale**: The smallest possible change. Replace the implication of creation with explicit acknowledgment of extension. Preserves all acceptance criteria unchanged since they are already correct (they describe behaviors, not creation acts).

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`, lines 335-348

**Before** (lines 337-338):
```
**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
```

**After**:
```
**Description**: The fidelity gate extends the existing convergence engine
(`convergence.py`, added in v3.0) to evaluate convergence based on registry
state with these criteria:
```

**Before** (lines 344-346):
```
**Gate Authority Model**: In convergence mode (`convergence_enabled=true`),
the convergence engine is the **sole authority** for pass/fail, evaluating
only the DeviationRegistry (`registry.get_active_high_count() == 0`).
```

**After**:
```
**Gate Authority Model**: In convergence mode (`convergence_enabled=true`),
the existing convergence engine (which already provides DeviationRegistry,
ConvergenceResult, _check_regression(), and temp dir isolation) becomes the
**sole authority** for pass/fail, evaluating only the DeviationRegistry
(`registry.get_active_high_count() == 0`).
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-7 Description + Gate Authority Model paragraphs only)

### Risk: **LOW**
Two sentences change. All acceptance criteria remain identical. No downstream FR references break because no FR references FR-7's description text verbatim.

### Requires Code Changes: **No**
Pure spec language fix. The code already exists and the acceptance criteria already describe the correct target behaviors.

---

## Proposal #2: Add v3.0 Baseline Section Before FR-7

**Rationale**: Rather than editing FR-7 inline, add a "v3.0 Baseline" subsection that explicitly inventories what already exists. This is the approach recommended by the Compatibility Report (Priority 2 in Section 8). Slightly more disruptive than Proposal #1 but provides a reusable pattern for ISS-002 (semantic_layer.py) and ISS-003 (remediate_executor.py).

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`, insert between line 334 (the `---` separator) and line 335 (`### FR-7`)

**Insert**:
```markdown
### FR-7 Baseline (v3.0 Pre-existing Code)

The following components already exist in `src/superclaude/cli/roadmap/convergence.py` (323 lines, commit `f4d9035`). FR-7 extends — does not recreate — this code.

| Component | Lines | Status |
|-----------|-------|--------|
| `compute_stable_id()` | 24-32 | Complete, no changes needed |
| `DeviationRegistry` (full lifecycle: load/save/merge) | 50-225 | Complete, no changes needed |
| `ConvergenceResult` dataclass | 228-237 | Complete, no changes needed |
| `_check_regression()` (structural-only, BF-3) | 240-272 | Complete, no changes needed |
| Temp dir isolation + atexit cleanup (FR-8) | 278-323 | Complete, no changes needed |
| `get_prior_findings_summary()` (FR-10) | 179-192 | Complete, no changes needed |
| `RunMetadata` dataclass | 36-46 | Dead code (never instantiated) — candidate for removal |

**New code required by FR-7** (to be added to convergence.py):
- `execute_fidelity_with_convergence()` — 3-run convergence loop orchestrator
- `handle_regression()` — full regression flow (spawn agents, validate, debate, update)
```

**Also change** FR-7 description (line 337-338) from:
```
**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
```
To:
```
**Description**: The fidelity gate extends the v3.0 convergence engine (see
baseline above) to evaluate convergence based on registry state with these
criteria:
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (new subsection + FR-7 Description edit)

### Risk: **LOW**
Additive change (new section) plus a one-line description edit. No acceptance criteria change. Establishes a pattern reusable for ISS-002 and ISS-003.

### Requires Code Changes: **No**
Pure spec clarification. Optionally, the dead `RunMetadata` dataclass could be removed in a separate cleanup commit, but this is not required by the spec change.

---

## Proposal #3: Reclassify FR-7 Frontmatter — Add Module Disposition Table

**Rationale**: The spec's YAML frontmatter (lines 11-23) lists `convergence.py` in `relates_to` without distinguishing CREATE vs MODIFY. Adding a disposition table to the frontmatter makes the intent machine-parseable and prevents future misreads by implementers or tasklist generators.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`, after line 23 (end of `relates_to` list)

**Insert**:
```yaml
module_disposition:
  - file: src/superclaude/cli/roadmap/convergence.py
    action: MODIFY
    note: "v3.0 pre-existing (323 lines). Extend with execute_fidelity_with_convergence(), handle_regression()"
  - file: src/superclaude/cli/roadmap/semantic_layer.py
    action: MODIFY
    note: "v3.0 pre-existing (336 lines). Add validate_semantic_high(), run_semantic_layer()"
  - file: src/superclaude/cli/roadmap/remediate_executor.py
    action: MODIFY
    note: "v3.0 pre-existing (563 lines). Add patch format, threshold change, per-file rollback"
  - file: src/superclaude/cli/roadmap/spec_parser.py
    action: CREATE
    note: "Genuinely new module"
  - file: src/superclaude/cli/roadmap/structural_checkers.py
    action: CREATE
    note: "Genuinely new module"
  - file: src/superclaude/cli/roadmap/fidelity.py
    action: DELETE
    note: "Dead code, zero imports"
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (YAML frontmatter only)

### Risk: **LOW-MEDIUM**
The frontmatter change is safe and additive. However, this proposal alone does NOT fix the FR-7 body text, so it should be combined with Proposal #1 or #2 for completeness. Slight risk that downstream tooling (e.g., `/sc:tasklist`) may not parse the new `module_disposition` key — but since it is additive YAML, non-aware parsers will simply ignore it.

### Requires Code Changes: **No**
Spec-only. However, if `/sc:tasklist` or `/sc:roadmap` generators consume frontmatter, they may need updates to recognize `module_disposition`. This is a tooling concern, not a code concern.

---

## Proposal #4: Rewrite FR-7 Acceptance Criteria with MODIFY Prefix

**Rationale**: Go further than Proposal #1 by prefixing each acceptance criterion with whether it is EXISTING (already passing) or NEW (to be implemented). This gives implementers a checklist they can immediately skip-or-work.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`, lines 354-366

**Before**:
```
**Acceptance Criteria**:
- [ ] Gate reads deviation registry, not raw fidelity output
- [ ] Pass requires: `active_high_count == 0` (total: structural + semantic)
- [ ] Monotonic progress check uses `structural_high_count` only
- [ ] Semantic HIGH count increases are logged as warnings, not regressions
- [ ] Run 2 must have `structural_high_count <= run_1.structural_high_count` or trigger FR-8
- [ ] Run 3 is final: pass or halt with full report
- [ ] If budget exhausted without convergence: halt, write diagnostic report, exit non-zero
- [ ] Progress proof logged with split counts: `structural: {n} → {n+1}, semantic: {n} → {n+1}`
- [ ] In convergence mode, `SPEC_FIDELITY_GATE` is never invoked
- [ ] In legacy mode, behavior is byte-identical to pre-v3.05
- [ ] `convergence_enabled: bool = False` field on pipeline config (default preserves legacy behavior)
```

**After**:
```
**Acceptance Criteria**:

*Already implemented in v3.0 (verify, do not rebuild):*
- [x] Gate reads deviation registry, not raw fidelity output — `DeviationRegistry.get_active_high_count()` exists
- [x] Pass requires: `active_high_count == 0` (total: structural + semantic) — `get_active_high_count()` implemented
- [x] Monotonic progress check uses `structural_high_count` only — `_check_regression()` structural-only
- [x] Semantic HIGH count increases are logged as warnings, not regressions — `_check_regression()` logs warning
- [x] In convergence mode, `SPEC_FIDELITY_GATE` is never invoked — `executor.py:521` conditional bypass
- [x] `convergence_enabled: bool = False` field on pipeline config — `models.py:107`

*New implementation required:*
- [ ] Run 2 must have `structural_high_count <= run_1.structural_high_count` or trigger FR-8
- [ ] Run 3 is final: pass or halt with full report
- [ ] If budget exhausted without convergence: halt, write diagnostic report, exit non-zero
- [ ] Progress proof logged with split counts: `structural: {n} → {n+1}, semantic: {n} → {n+1}`
- [ ] In legacy mode, behavior is byte-identical to pre-v3.05
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-7 Acceptance Criteria section)

### Risk: **MEDIUM**
More invasive edit. The `[x]` vs `[ ]` distinction changes the semantics of the acceptance criteria from "all must be built" to "some verified, some must be built." Risk: if any "already implemented" item is marked `[x]` but actually has a subtle gap, it could be missed. Mitigation: each `[x]` item includes a code location reference for verification.

### Requires Code Changes: **No**
Spec-only, but implementers should verify each `[x]` item against the referenced code locations before trusting the classification.

---

## Proposal #5: Full FR-7 Rewrite with "Extend Existing" Frame

**Rationale**: The most complete fix. Rewrites the entire FR-7 section to frame convergence.py as an existing module being extended. Combines elements of Proposals #1, #2, and #4.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`, replace lines 335-367

**Before**: (entire FR-7 section as currently written)

**After**:
```markdown
### FR-7: Convergence Gate (Extend Existing)

**Baseline**: `convergence.py` (323 lines, v3.0, commit `f4d9035`) already
provides: DeviationRegistry with full lifecycle, compute_stable_id(),
ConvergenceResult, _check_regression() with structural-only enforcement,
temp dir isolation, run-to-run memory via get_prior_findings_summary().
Pipeline wiring: gate bypass in executor.py:521, convergence_enabled config
field in models.py:107.

**Description**: Extend the existing convergence engine to orchestrate multi-run
fidelity evaluation based on registry state with these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED) — includes both structural AND semantic HIGHs
- **Monotonic progress**: Each run must have <= structural HIGHs than previous run. Semantic HIGH fluctuations are logged as warnings but do NOT constitute regression.
- **Hard budget**: Maximum 3 runs (catch -> verify -> backup)
- **Regression detection**: If run N+1 has MORE structural HIGHs than run N, trigger parallel validation (see FR-8)

**Gate Authority Model**: In convergence mode (`convergence_enabled=true`),
the convergence engine is the **sole authority** for pass/fail, evaluating
only the DeviationRegistry (`registry.get_active_high_count() == 0`). The
existing `SPEC_FIDELITY_GATE` is NOT invoked (bypass already wired in
executor.py:521). The `spec-fidelity.md` report is still written as a
human-readable summary but is not gated.

In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
exactly as in pre-v3.05, validating the LLM-generated report frontmatter.
The two authorities never coexist in the same execution mode.

**New Code Required** (add to convergence.py):
- `execute_fidelity_with_convergence()` — 3-run loop orchestrator
- `handle_regression()` — spawn parallel validation agents, merge, debate, update registry

**Acceptance Criteria (v3.0 baseline — verify only)**:
- [x] Gate reads deviation registry, not raw fidelity output
- [x] Pass requires: `active_high_count == 0` (total: structural + semantic)
- [x] Monotonic progress check uses `structural_high_count` only
- [x] Semantic HIGH count increases are logged as warnings, not regressions
- [x] In convergence mode, `SPEC_FIDELITY_GATE` is never invoked
- [x] `convergence_enabled: bool = False` field on pipeline config (default preserves legacy behavior)

**Acceptance Criteria (new for v3.05)**:
- [ ] `execute_fidelity_with_convergence()` implements 3-run budget loop
- [ ] Run 2 must have `structural_high_count <= run_1.structural_high_count` or trigger FR-8
- [ ] Run 3 is final: pass or halt with full report
- [ ] If budget exhausted without convergence: halt, write diagnostic report, exit non-zero
- [ ] Progress proof logged with split counts: `structural: {n} -> {n+1}, semantic: {n} -> {n+1}`
- [ ] In legacy mode, behavior is byte-identical to pre-v3.05

**Dependencies**: FR-6 (registry), FR-8 (regression handling)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (full FR-7 section replacement)
- Appendix A "Proposed (to-be)" diagram (line 593) should add "(extends existing)" annotation — optional

### Risk: **MEDIUM-HIGH**
Largest edit surface. Risk of introducing errors in the rewrite. Mitigation: the before/after is fully specified above and can be diff-reviewed. Also risk that the `[x]` baseline items may have subtle gaps (same concern as Proposal #4).

### Requires Code Changes: **No**
Spec-only rewrite. The code referenced already exists. The new functions (`execute_fidelity_with_convergence`, `handle_regression`) are acknowledged as gaps that must be built — which aligns with Compatibility Report Section 4.

---

## Ranking Summary

| Rank | Proposal | Disruption | Correctness | Completeness | Recommendation |
|------|----------|-----------|-------------|--------------|----------------|
| 1 | #1 (Minimal reword) | Very Low | High | Partial | Best if only ISS-001 is being fixed in isolation |
| 2 | #2 (Baseline section) | Low | High | High | Best if ISS-001/002/003 are being fixed together (reusable pattern) |
| 3 | #3 (Frontmatter disposition) | Low | High | Partial | Best as a supplement to #1 or #2, not standalone |
| 4 | #4 (AC reclassification) | Medium | High | High | Good standalone but risky if baseline verification is skipped |
| 5 | #5 (Full rewrite) | High | Highest | Highest | Best if FR-7 is being substantially reworked anyway |

**Recommended approach**: Combine **#1 + #2 + #3** — minimal body text change, baseline inventory section (reusable for ISS-002/003), and frontmatter disposition table. Total edit surface is small, all additive except one sentence change, and covers the issue completely.
