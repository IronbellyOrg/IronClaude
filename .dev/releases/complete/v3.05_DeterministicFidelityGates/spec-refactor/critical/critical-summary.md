# Critical Issues — Synthesis & Execution Plan

> Synthesized from brainstorm proposals for ISS-001, ISS-002, ISS-003
> Date: 2026-03-20

---

## Executive Summary

All three CRITICAL issues share the same root cause: the v3.05 spec was written before v3.0 shipped. It describes three modules as greenfield CREATE operations that already exist with substantial implementations. Implementing as-written would overwrite working code.

---

## Per-Issue: Selected Proposal & Rationale

### ISS-001: convergence.py (FR-7)

**Selected**: Proposal #2 — Add v3.0 Baseline Section Before FR-7

**Rationale**: Establishes a reusable pattern (baseline inventory table) that ISS-002 and ISS-003 can follow. Slightly more work than the minimal reword (#1) but creates consistency across all three fixes. Combined with Proposal #1's one-sentence description edit and Proposal #3's frontmatter `module_disposition` table.

**Spec sections to modify**:
- FR-7 Description paragraph (2 sentences changed)
- New "FR-7 Baseline" subsection inserted before FR-7
- YAML frontmatter: add `module_disposition` key

**Code changes required**: None (spec-only fix)

---

### ISS-002: semantic_layer.py (FR-4)

**Selected**: Proposal #1 — Reclassify FR-4 from "Build" to "Complete"

**Rationale**: Minimal disruption. Adds an "Existing baseline" note to FR-4's description and marks already-satisfied ACs as `[x]` with source references in FR-4.1 and FR-4.2. Self-contained within FR-4 — no structural reorganization needed.

**Spec sections to modify**:
- FR-4 Description: add "Existing baseline" paragraph
- FR-4.1 Acceptance Criteria: mark 3 items as `[x]`, add 2 new items for validate_semantic_high() and run_semantic_layer()
- FR-4.2 Acceptance Criteria: mark 5 items as `[x]`, add TRUNCATION_MARKER heading fix item

**Code changes required**: Yes (minor)
- `semantic_layer.py` line 28: TRUNCATION_MARKER must include heading name parameter
- `_truncate_to_budget()` signature updated to accept heading name

---

### ISS-003: remediate_executor.py (FR-9)

**Selected**: Proposal #1 — Reclassify to MODIFY with Surgical Delta List

**Rationale**: Preserves all existing acceptance criteria verbatim (they already describe the correct target state). Replaces only the FR-9 description paragraph with one that acknowledges the v3.0 baseline and lists the explicit delta. Handles overlap with HIGH issues ISS-004/005/006 by listing them inline in the delta.

**Spec sections to modify**:
- FR-9 Description: replace with extended version containing v3.0 Baseline inventory + Delta list

**Code changes required**: Yes (demanded by spec regardless of which proposal)
- `_DIFF_SIZE_THRESHOLD_PCT`: 50 → 30 (ISS-004)
- `_check_diff_size()`: per-file → per-patch granularity (ISS-005)
- `_handle_failure()`: all-or-nothing → per-file rollback (ISS-006)
- New: `RemediationPatch`, `apply_patches()`, `fallback_apply()`, `check_morphllm_available()`

---

## Cross-Issue Conflicts

### Conflict 1: Baseline Documentation Strategy — Resolved

All three issues propose adding baseline documentation to the spec. Two strategies emerged:

| Strategy | Used By | Approach |
|----------|---------|----------|
| **Per-FR baseline subsection** | ISS-001 (#2), ISS-003 (#1) | Each FR gets its own baseline inventory inline |
| **Global Section 0 preamble** | ISS-002 (#2, alt), ISS-003 (#3, alt) | One centralized baseline section before FR-1 |

**Resolution**: Use **per-FR baseline subsections** (the selected proposals). This keeps each FR self-contained — a reader doesn't need to cross-reference a separate section. Supplement with the **frontmatter `module_disposition` table** (ISS-001 Proposal #3) for machine-parseable disposition at the spec level.

No contradiction between selected proposals.

### Conflict 2: AC Marking Convention — Resolved

ISS-001 (#4) and ISS-002 (#1) both mark existing ACs as `[x]`. ISS-003 (#1) leaves ACs unchanged because they already describe the target state correctly.

**Resolution**: This is not a conflict. ISS-003's ACs describe future state (e.g., "per-patch diff-size guard") that doesn't match current code (per-file). ISS-001 and ISS-002's ACs describe behaviors that ARE already implemented. The `[x]` marking is appropriate where the code already satisfies the criterion; leaving `[ ]` is appropriate where the code must still change.

### No Other Conflicts Detected

The three selected proposals are complementary. They share a common pattern (baseline acknowledgment + delta specification) applied consistently across FR-4, FR-7, and FR-9.

---

## Recommended Execution Order

### Phase 1: Frontmatter Update (affects all three)

Add `module_disposition` YAML key to spec frontmatter. This is a single, atomic change that signals intent for all three modules.

**File**: `deterministic-fidelity-gate-requirements.md` (YAML frontmatter)
**Risk**: LOW — additive YAML, non-aware parsers ignore it

### Phase 2: FR-9 Refactor (ISS-003) — Do First

FR-9 is the most complex change and overlaps with three HIGH issues (ISS-004/005/006). Completing it first:
- Validates the baseline/delta pattern on the hardest case
- Establishes the delta list format that FR-4 and FR-7 will follow
- Surfaces any cross-reference issues early

**File**: `deterministic-fidelity-gate-requirements.md` (FR-9 Description block)
**Risk**: LOW — description replacement only, all ACs preserved

### Phase 3: FR-4 Refactor (ISS-002)

Apply the baseline note + AC marking pattern established in Phase 2. FR-4 is moderate complexity (three subsections: FR-4, FR-4.1, FR-4.2).

**File**: `deterministic-fidelity-gate-requirements.md` (FR-4, FR-4.1, FR-4.2)
**Risk**: LOW — additive baseline paragraph + `[x]` marks on verified ACs

### Phase 4: FR-7 Refactor (ISS-001)

FR-7 is the simplest change — one description sentence edit plus a baseline subsection. Do last because it benefits from the pattern being proven on FR-9 and FR-4.

**File**: `deterministic-fidelity-gate-requirements.md` (FR-7 + new baseline subsection)
**Risk**: LOW — additive section + 2-sentence edit

### Phase 5: Validation

After all four phases, verify:
- [ ] All three FR descriptions acknowledge "extends existing" not "create new"
- [ ] `module_disposition` frontmatter lists all 6 modules with correct actions
- [ ] FR-4.1 and FR-4.2 have `[x]`/`[ ]` split that matches code reality
- [ ] FR-9 delta list covers ISS-004, ISS-005, ISS-006 explicitly
- [ ] FR-7 baseline subsection lists all 7 existing components with line refs
- [ ] No dangling "create" or "build new" language remains for these 3 modules
- [ ] Cross-references from other FRs (FR-6 → FR-9, FR-8 → FR-7) still resolve

---

## Proposal Files

| Issue | File |
|-------|------|
| ISS-001 | `critical/ISS-001-proposals.md` |
| ISS-002 | `critical/ISS-002-proposals.md` |
| ISS-003 | `critical/ISS-003-proposals.md` |
| Summary | `critical/critical-summary.md` (this file) |
