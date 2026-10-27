# LOW Severity Issues — Resolution Summary

> Source: `issues-classified.md` ISS-020 through ISS-024
> Generated: 2026-03-20

## Overview

| ID | Title | Status | Selected Proposal |
|----|-------|--------|-------------------|
| ISS-020 | fidelity.py is dead code | **RESOLVE** | Remove from `relates_to` frontmatter |
| ISS-021 | RunMetadata dataclass dead in convergence.py | **RESOLVE** | Add typed run metadata criterion to FR-6 |
| ISS-022 | Spec uses "create" for modules that need "extend" | **PARTIALLY SUPERSEDED** | FR-8 acknowledgment only (FR-4/7/9 covered by ISS-001/002/003) |
| ISS-023 | prompts.py role undocumented in v3.05 context | **RESOLVE** | Add parenthetical + sentence in FR-7 legacy mode |
| ISS-024 | Finding dataclass missing v3.05 fields | **RESOLVE** | Add "Finding Dataclass Extension" subsection to FR-6 |

---

## Per-Issue Resolutions

### ISS-020: fidelity.py is dead code
**Selected**: Proposal A — Remove `fidelity.py` from `relates_to` frontmatter.

Zero imports across the codebase; superseded by Finding + DeviationRegistry. The `relates_to` field is a navigation aid, not a historical record. Traceability is served by the git commit and this issue's record.

**Spec section**: YAML frontmatter `relates_to` (line 16)

---

### ISS-021: RunMetadata dataclass dead in convergence.py
**Selected**: Proposal A — Add typed run metadata acceptance criterion to FR-6.

The `RunMetadata` dataclass already has exactly the fields FR-6 requires (including BF-3 split counts). Wiring it into `begin_run()` costs one AC line and eliminates both the dead-code smell and type-safety gap.

**Spec section**: FR-6 acceptance criteria (after line 325)

---

### ISS-022: Spec uses "create" for modules that need "extend"
**Selected**: Proposal A — FR-8 acknowledgment only (contingent).

ISS-001/002/003 (CRITICAL) fully cover FR-4, FR-7, and FR-9. The sole remaining gap is FR-8, which describes temp dir isolation without acknowledging `convergence.py`'s existing implementation (lines 278-323).

**Contingency**: If ISS-001 adopts a proposal with a baseline section listing temp dir isolation, ISS-022 can be closed as fully SUPERSEDED.

**Spec sections**: FR-8 description (lines 373-378), isolation mechanism (lines 380-384), cleanup protocol (lines 386-390)

---

### ISS-023: prompts.py:build_spec_fidelity_prompt() role undocumented
**Selected**: Proposal A — Expand FR-7 legacy mode sentence with parenthetical naming `build_spec_fidelity_prompt()`, plus one sentence on convergence-mode role.

**Spec section**: FR-7 Gate Authority Model (lines 350-352)

---

### ISS-024: Finding dataclass missing v3.05 fields
**Selected**: Proposal B — Add "Finding Dataclass Extension" subsection to FR-6.

Groups all field additions (`rule_id`, `spec_quote`, `roadmap_quote`) in FR-6 alongside the existing `source_layer` paragraph. Explicitly documents that `stable_id` is computed (not stored) and that all new fields have defaults for backward compatibility.

**Spec section**: FR-6, after Source Layer Tracking paragraph (line 312)

---

## Batch Edit Plan

Edits are grouped by spec section for single-pass application.

### Pass 1: YAML Frontmatter (lines 1-24)

| Edit | Issue | Action |
|------|-------|--------|
| Line 16 | ISS-020 | **Delete** `  - src/superclaude/cli/roadmap/fidelity.py` |

### Pass 2: FR-6 — Deviation Registry (lines 296-331)

| Edit | Issue | Action |
|------|-------|--------|
| After line 312 | ISS-024 | **Insert** "Finding Dataclass Extension" subsection with field table |
| After line 325 | ISS-021 | **Insert** new AC: `- [ ] Run metadata uses a typed dataclass (RunMetadata) — not raw dicts — to ensure field presence and type safety at construction time` |

### Pass 3: FR-7 — Convergence Gate (lines 335-366)

| Edit | Issue | Action |
|------|-------|--------|
| Lines 350-352 | ISS-023 | **Replace** legacy mode sentence with expanded version naming `build_spec_fidelity_prompt()` and convergence-mode role |

### Pass 4: FR-8 — Regression Detection (lines 371-407)

| Edit | Issue | Action |
|------|-------|--------|
| Lines 373-378 | ISS-022 | **Replace** description to add "extends the existing temp dir isolation mechanism in `convergence.py`" |
| Lines 380-384 | ISS-022 | **Replace** isolation mechanism to add "reusing and extending the temp dir + atexit cleanup pattern" |
| Lines 386-390 | ISS-022 | **Replace** cleanup protocol header to add "(extends existing `atexit` cleanup in `convergence.py:310-323`)" |

---

## Proposal Files

- [ISS-020-proposals.md](ISS-020-proposals.md)
- [ISS-021-proposals.md](ISS-021-proposals.md)
- [ISS-022-proposals.md](ISS-022-proposals.md)
- [ISS-023-proposals.md](ISS-023-proposals.md)
- [ISS-024-proposals.md](ISS-024-proposals.md)
