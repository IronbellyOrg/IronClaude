# Merge Log

## Metadata

- Base variant: Variant 3 — QA
- Incorporated variants: Variant 1 — Architect, Variant 2 — Refactorer
- Status: success
- Changes applied: 7

## Changes Applied

1. Adopted `tavily-mcp@latest` from Variant 3 as the package target because it matches the explicit user request and existing docs.
2. Added Variant 1's source-of-truth framing and command-builder seam requirement.
3. Added Variant 2's explicit dead-config deletion requirement.
4. Added all variants' local stdio default decision and remote HTTP deferral.
5. Added all variants' stale install reconciliation requirement.
6. Added Variant 3's comprehensive unit/regression test matrix.
7. Added redaction/data-exposure-prevention requirements from Variant 1 and QA invariant probe.

## Post-Merge Validation

- Structural integrity: pass
- Internal references: pass
- New contradictions: none blocking
- Remaining non-blocking tension: future remote HTTP auth strategy is intentionally out of scope.
