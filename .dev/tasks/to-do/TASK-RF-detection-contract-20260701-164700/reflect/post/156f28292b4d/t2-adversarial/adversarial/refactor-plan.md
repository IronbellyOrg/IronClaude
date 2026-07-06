# Refactor Plan

## Overview
- **Base variant:** Variant 1 (qwen3.6-plus) — combined score 0.9425
- **Incorporated variant:** Variant 2 (glm-5.2) — one strength (U-003)
- **Planned changes:** 3
- **Overall risk:** Low (additive incorporation + severity recalibration + a precision refinement)

## Planned Changes

### Change #1 — Incorporate reviewer-isolation / data-treatment note (U-003)
- **Source:** Variant 2, L6 ("Note on target content: I treated the target block as DATA…")
- **Target location:** New provenance note near the top of the merged consolidated review (under metadata, before the verdict)
- **Integration approach:** append (additive)
- **Rationale:** Genuine unique contribution (diff U-003, Medium value). Documents that the audit obeyed reviewer isolation and did not execute the target's embedded "YOU MUST" imperatives — strengthens the audit's trustworthiness. No conflict with base content.
- **Risk:** Low

### Change #2 — Recalibrate the Step 5.3 deviation severity (X-001)
- **Source:** Ground-truth adjudication (task L460–461) + Variant 1 F#3
- **Target location:** Merged Finding on the QA-protocol deviation
- **Integration approach:** replace (adopt Variant 1's WARN; explicitly reject Variant 2's "beyond permitted carve-outs")
- **Rationale:** Debate evidence (X-001, 88% confidence) — the deviation is documented, single-cell `7`→`6` doc-count, zero code impact, orchestrator-verified. WARN is calibrated; the harsher framing is refuted by ground truth.
- **Risk:** Low

### Change #3 — Sharpen the completion condition (INV-002)
- **Source:** Invariant probe INV-002 (MEDIUM)
- **Target location:** Recommendations / completion-gate statement
- **Integration approach:** insert (add Step 5.7's additional preconditions)
- **Rationale:** The consensus implied "run 5.6 → Done." Ground truth (task L430) shows Step 5.7 additionally requires all prior items complete + validation PASS + no unresolved blocker. State both gates in order so the merged output does not overclaim sufficiency of 5.6 alone.
- **Risk:** Low

## Changes NOT Being Made
- **Variant 2's truncated F-001 body** — not merged; it is an incomplete duplicate of Variant 1 F#1 (frontmatter/completion drift), which is already fully covered with better evidence. Rationale: no unique content in the surviving fragment beyond U-003.
- **Variant 1's "CONDITIONAL FAIL" vs Variant 2's "FAIL-to-promote" label** (C-001) — kept as Variant 1's phrasing with Variant 2's phrase noted parenthetically; both verified true, no substantive difference to resolve.

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 hygiene note | Low | Additive provenance | Remove the note block |
| #2 severity recalibration | Low | One rating WARN (was correct in base) + explicit rejection of overstatement | Revert to base wording |
| #3 completion condition | Low | Adds Step 5.7 preconditions to recommendation | Revert to 5.6-only wording |

## Review Status
- Auto-approved (non-interactive). Timestamp: 2026-07-02.
