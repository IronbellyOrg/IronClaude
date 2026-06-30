# Refactor Plan — Merge into Base C (Reject), with A/B transfers

## Overview
- **Base variant:** C (reject) — score 0.940
- **Incorporated:** A's gap-localization (redirected) + B's precision/recall diagnosis
- **Change count:** 3 incorporations + 2 invariant-driven clarifications
- **Risk:** Low — the merged output is a *recommendation*, and it recommends the lowest-blast-radius outcome (no reflect wiring)

## Planned Changes

### Change #1 — Incorporate A's auggie-review gap as a real, narrow defect (HIGH)
- **Source:** Proposal A §"Integration point 1" + `context.md:7` existence proof
- **Target in base:** C's auggie-review section
- **Rationale (debate evidence):** A correctly identified that Wave-3 citation validation is a *same-context* inline Read (`SKILL.md:204–205`), a documented blind spot. C conceded this at ~68%. The gap is genuine.
- **Integration approach:** Keep the gap, but **redirect the fix**: per INV-012/INV-003, the fix is NOT importing `evidence-validator` (wrong mechanism class + contract-incompatible re-ground). It is strengthening auggie-review's *own* Wave-3 pass to a guaranteed **fresh-context** re-Read and routing failures through the **existing `needs-grounding` bucket** (`SKILL.md:203,207`), which already re-grounds via Grep/auggie then drops — the behavior `evidence-validator` forbids. Zero new dependency.
- **Risk:** Low (additive clarification to an existing pass; no new agent)

### Change #2 — Incorporate B's precision-vs-recall diagnosis (HIGH)
- **Source:** Proposal B §"Strength 3" + INV-012
- **Target in base:** C's "what reflect adds" framing
- **Rationale:** B's advocate presciently argued evidence-validator is precision-only; INV-012 confirmed it cannot reproduce the R0/PR#112 *recall* catch. This is *why* the cheap add fails, and it strengthens C's rejection with a mechanism-level reason rather than only the applied-vs-recommendation reason.
- **Integration approach:** Add a "precision vs recall" subsection to the merged verdict explaining that no proposed mechanism delivers the recall property that motivated the inquiry, and that the recall property (heterogeneous reviewers) is exactly what B's cost made unjustifiable for human-gated recommendations.
- **Risk:** Low (analytical addition)

### Change #3 — Incorporate the cleanup-audit non-citation-defect finding (MEDIUM)
- **Source:** INV-013 + INV-008 + `context.md:83,84`
- **Target in base:** C's cleanup-audit section
- **Rationale:** C rejected A-for-cleanup-audit on "it's a coverage knob, not a disjoint hole." The probe gives a stronger reason: the destructive defects that matter (CONSOLIDATE overlap-%, dynamic-loading false-negatives) are *non-citation* defects a citation/grep re-check cannot catch, and they partly live *outside* the DELETE/CONSOLIDATE bucket.
- **Integration approach:** State that any cleanup-audit hardening should target the *existing* `audit-validator`'s content checks (classification accuracy, dynamic-use checklist) — not a citation gate — and must recompute the FAIL denominator (INV-005) and fix the file-vs-finding counting base (INV-006) if coverage is raised. This is `audit-validator` tuning, still **not** a reflect integration.
- **Risk:** Low (scopes a possible follow-up; recommends no change now)

## Changes NOT Being Made (rejected alternatives)
- **A's `evidence-validator` import (both targets):** rejected. INV-012 (precision gate for a recall-motivated gap), INV-003 (re-ground contract-incompatible), INV-004 (paraphrase false-drop), INV-010 (irreversible across remediation interaction).
- **A's 100%-on-DELETE/CONSOLIDATE for cleanup-audit:** rejected. INV-013 (insufficient for non-citation defects), INV-008 (excludes worst case).
- **B's full `/sc:reflect` replacement (both targets):** rejected. U-003 (semantic-fit), X-003 (circular reuse), 5–10× cost for a human-gated stage.

## Risk Summary
| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| #1 redirect auggie fix | Low | auggie Wave-3 stays same-context | Drop the freshness clarification |
| #2 precision/recall framing | Low | weaker rejection rationale | Remove subsection |
| #3 cleanup-audit follow-up scoping | Low | cleanup-audit hardening mis-targeted | Remove follow-up note |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-06-04
