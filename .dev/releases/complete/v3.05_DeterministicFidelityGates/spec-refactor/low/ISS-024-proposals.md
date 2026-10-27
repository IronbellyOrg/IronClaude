# ISS-024: Finding dataclass missing v3.05 fields

**Issue**: FR-1 acceptance criteria require each finding to include `dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location`, and FR-6 requires each finding to have a `stable_id` derived from `(dimension, rule_id, spec_location, mismatch_type)`. The current `Finding` dataclass in `models.py` has `id`, `severity`, `dimension`, `description`, `location`, `evidence`, `fix_guidance`, `files_affected`, `status`, `agreement_category`, `deviation_class`, and `source_layer` -- but is missing `rule_id`, `spec_quote`, `roadmap_quote`, and `stable_id`.

The spec *describes* these fields in FR-1 and FR-6 acceptance criteria but never explicitly states they are NEW fields being added to an EXISTING dataclass. The compatibility reports (CompatibilityReport01 line 113, CompatibilityReport-Merged line 103) both flag this as: "Extend dataclass in models.py."

---

## Status Check
- Superseded by upstream? **PARTIALLY.** ISS-001/002/003 (CRITICAL -- reclassify CREATE to MODIFY) establish the pattern of acknowledging pre-existing modules and distinguishing MODIFY from CREATE. ISS-001 Proposal #3 includes a `module_disposition` entry for `models.py` as MODIFY. However, none of those proposals address the *specific field additions* to the Finding dataclass. ISS-024 is a distinct gap: the spec describes desired fields but does not call out that they must be added to the existing `Finding` dataclass (which already has 11 fields). This issue stands on its own.

---

## Proposal A: Add "New Fields" annotation to FR-1 acceptance criteria

**Rationale**: The most targeted fix. FR-1 is where the finding fields are first enumerated. Add a parenthetical note making explicit that `rule_id`, `spec_quote`, `roadmap_quote` are new fields to add to the existing `Finding` dataclass, and that `stable_id` (FR-6) is computed, not stored.

**Before** (spec line 108, FR-1 Acceptance Criteria):
> - [ ] Each finding includes: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location

**After**:
> - [ ] Each finding includes: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location. **New fields** to add to the existing `Finding` dataclass in `models.py`: `rule_id: str`, `spec_quote: str`, `roadmap_quote: str = "MISSING"`. Existing fields `dimension`, `severity`, `location` are already present.

Additionally, in FR-6 acceptance criteria:

**Before** (spec line 322):
> - [ ] Each finding has a stable ID derived from (dimension, rule_id, spec_location, mismatch_type)

**After**:
> - [ ] Each finding has a stable ID derived from (dimension, rule_id, spec_location, mismatch_type) via `compute_stable_id()` (already implemented in `convergence.py`). The `stable_id` is NOT stored on the Finding dataclass; it is computed on demand from the finding's fields.

---

## Proposal B: Add a "Finding Dataclass Extension" subsection to FR-6

**Rationale**: Since FR-6 (Deviation Registry) is the FR that defines the stable_id contract and the registry lifecycle, it is the natural home for an explicit dataclass extension specification. This groups all Finding field changes in one place rather than splitting them across FR-1 and FR-6.

**Before** (spec lines 309-312, FR-6 Source Layer Tracking paragraph):
> **Source Layer Tracking**: Each finding carries a `source_layer` field
> (`"structural"` or `"semantic"`) indicating which layer produced it. This
> enables split tracking for convergence (see FR-7). Default is `"structural"`
> for backward compatibility with pre-v3.05 registries.

**After**:
> **Source Layer Tracking**: Each finding carries a `source_layer` field
> (`"structural"` or `"semantic"`) indicating which layer produced it. This
> enables split tracking for convergence (see FR-7). Default is `"structural"`
> for backward compatibility with pre-v3.05 registries.
>
> **Finding Dataclass Extension**: The existing `Finding` dataclass in
> `models.py` (v3.0 baseline: `id`, `severity`, `dimension`, `description`,
> `location`, `evidence`, `fix_guidance`, `files_affected`, `status`,
> `agreement_category`, `deviation_class`, `source_layer`) must be extended
> with the following new optional fields for v3.05:
>
> | Field | Type | Default | Source FR | Purpose |
> |-------|------|---------|-----------|---------|
> | `rule_id` | `str` | `""` | FR-1, FR-3 | Links finding to a specific severity rule in the checker's rule table |
> | `spec_quote` | `str` | `""` | FR-1 | Exact text from spec that the finding references |
> | `roadmap_quote` | `str` | `"MISSING"` | FR-1 | Corresponding text from roadmap, or "MISSING" if absent |
>
> `stable_id` is NOT a stored field. It is computed on demand via
> `compute_stable_id(dimension, rule_id, spec_location, mismatch_type)` in
> `convergence.py` (already implemented in v3.0). The existing `id` field
> remains for human-readable identification; `stable_id` is used for
> cross-run matching in the deviation registry.
>
> All new fields default to empty/sentinel values to maintain backward
> compatibility with pre-v3.05 serialized findings.

---

## Recommendation

**Adopt Proposal B.**

Rationale:
1. **Self-contained**: Groups all Finding extension details in FR-6, which is the FR that owns the registry contract and is where `source_layer` (the only existing v3.05 field addition) is already specified. This follows the established pattern.
2. **Explicit about stable_id**: Clarifies that `stable_id` is computed (via existing code), not stored -- preventing an implementer from adding a redundant field to the dataclass.
3. **Backward compatibility**: Explicitly requires defaults on all new fields, protecting against deserialization failures with pre-v3.05 data.
4. **Low disruption**: Adds one paragraph and a table after an existing paragraph. No acceptance criteria rewording needed -- FR-1 line 108 and FR-6 line 322 remain valid as target-state descriptions; Proposal B just makes the implementation path explicit.
5. **Complements ISS-001/002/003**: If those proposals adopt a "v3.0 Baseline" section or `module_disposition` frontmatter, Proposal B's field table slots naturally under the models.py MODIFY entry.

Proposal A is acceptable as a lighter alternative if the team prefers inline annotations over a dedicated subsection, but it splits the information across two FRs and does not address backward compatibility defaults.
