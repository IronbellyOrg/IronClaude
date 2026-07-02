# Diff Analysis — Detection Contract Setup Variants

## Metadata

- Variants compared: 3
- Variant 1: architect
- Variant 2: refactorer
- Variant 3: qa
- Total substantive differences: 8

## Structural Differences

| ID | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Ownership boundary | Shared helper + reflect status + pr-submit guidance | Shared helper, but reflect initially diagnose-only | Shared helper with stronger validation/status taxonomy | Medium |
| S-002 | Implementation sequencing | Full architecture from start | Smallest safe slices, defer capture | Validation/test-first sequencing | Medium |

## Content Differences

| ID | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | `/sc:reflect` role | Formal contract-status surface can validate | Diagnose/recommend first; avoid writes initially | Diagnose/validate status without payload leakage | Medium |
| C-002 | Automated GitHub capture | Include as part of design, with no side effects | Defer until file-based validation works | Allow capture, but heavily test wrong/stale cases | Medium |
| C-003 | Decline evidence | Defaults may be carried if not exercised | Defaults can remain baked values, validation note | Strict default: decline validation preferred for locking | High |
| C-004 | Freshness threshold | Warn/block on repo/PR/hash mismatch; age policy open | 30-day warning suggested | 7-day default suggested; stronger stale rejection | Medium |

## Contradictions / Tensions

| ID | Point | Positions | Impact |
|---|---|---|---|
| X-001 | Can `/sc:reflect` write a locked contract? | V1 allows optional orchestration; V2 recommends read-only first; V3 permits setup but emphasizes confirmation | Must resolve to prevent scope creep |
| X-002 | Is decline evidence required for `locked: true`? | V1/V2 allow defaults with unexercised warning; V3 prefers strict lock block | Determines v1 operator friction vs correctness |

## Unique Contributions

| ID | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Explicit metadata extension for validation hash/report and `validated_surfaces` | High |
| U-002 | V2 | Minimal first slice: file-based payload validation before live capture | High |
| U-003 | V3 | Detailed stale/wrong/cross-PR evidence rejection matrix and acceptance criteria | High |

## Shared Assumptions

| ID | Assumption | Classification | Promoted |
|---|---|---|---|
| A-001 | `DetectionContract.for_arming()` remains fail-closed and is not weakened | STATED | No |
| A-002 | Repo-specific locked contract belongs under `.dev/pr-monitor/`, not shipped refs or `.claude/` | STATED | No |
| A-003 | Existing classifier/poll seam should be reused for validation | STATED | No |
| A-004 | Setup must not arm monitor, post comments, push, retry, or retrigger | STATED | No |

## Summary

The variants converge on a shared-helper design. Remaining tensions are scope (`/sc:reflect` diagnose-only vs orchestrating writes), decline-evidence strictness, and freshness threshold. The merged design chooses a conservative v1: shared helper, `/sc:reflect` read-only status plus optional future orchestration, file-based validation first, live capture second, and lock only on observed identity/surface/locus/completion with classifier success.
