# T01.25 evidence — decisions.md content delta

**Task:** T01.25 (Phase 1, OPS-001 / R-021)
**Date:** 2026-05-20
**File touched:** `.dev/releases/current/cliEval/decisions.md`

## 1. Revision-log entry added

```diff
 **Revision log:**
 - R1 (2026-05-18): D-1..D-4 initial proposals.
 - R2 (2026-05-18): D-5..D-8 added to resolve the 4 CRITICAL findings from `spec-panel-review.md`.
+- R3 (2026-05-20): OPS-001 closure — D-5..D-8 status flipped to "queued for sign-off"; OQ-1/3/7/8/10 resolution-status block added; implementation gates cross-referenced to ADR IDs. See §OPS-001 Closure below; per-deliverable spec at `artifacts/D-0021/spec.md`.
```

## 2. Sign-off table rows updated

```diff
-| D-5: Hook-matcher coverage gate (G5 falsifiable) | 🟡 PROPOSED (R2) | — | — |
-| D-6: `--max-disk-mb` poller (R4 enforcement)     | 🟡 PROPOSED (R2) | — | — |
-| D-7: Three-layer path-traversal hardening        | 🟡 PROPOSED (R2) | — | — |
-| D-8: Reporter consumes N' + status taxonomy      | 🟡 PROPOSED (R2) | — | — |
+| D-5: Hook-matcher coverage gate (G5 falsifiable) | 🟠 QUEUED FOR SIGN-OFF (R3) | — | 2026-05-20 |
+| D-6: `--max-disk-mb` poller (R4 enforcement)     | 🟠 QUEUED FOR SIGN-OFF (R3) | — | 2026-05-20 |
+| D-7: Three-layer path-traversal hardening        | 🟠 QUEUED FOR SIGN-OFF (R3) | — | 2026-05-20 |
+| D-8: Reporter consumes N' + status taxonomy      | 🟠 QUEUED FOR SIGN-OFF (R3) | — | 2026-05-20 |
```

D-1..D-4 deliberately left at `🟡 PROPOSED` — OPS-001 only flips D-5..D-8; SC1 (M1 exit) signs off all eight together.

## 3. New section appended ("OPS-001 Closure")

Appended after the D-9 reconciliation section. Section structure:

- **§A. ADR queue status (D-5..D-8)** — confirms the Sign-off table rows; documents that D-1..D-4 remain 🟡 PROPOSED.
- **§B. Open Question resolution status (OQ-1, OQ-3, OQ-7, OQ-8, OQ-10)** — 5-row table with `OQ`, `Question`, `Owner`, `Target`, `Resolution status as of 2026-05-20`, `Blocks`.
- **§C. Implementation-gate → ADR cross-reference** — 8-row table mapping D-1..D-8 → implementation gate site + Phase / task ID.
- **§D. Acceptance-criteria → site map (T01.25)** — 4-row AC traceability table.
- **§E. Out of scope for T01.25** — explicit non-goals list.

Full text of the new section is the authoritative satisfaction site for T01.25 ACs 1–3; this file captures only the diff summary for fast review.

## 4. AC verification

| AC bullet                                                                                          | Status |
|----------------------------------------------------------------------------------------------------|--------|
| D-5..D-8 in decisions.md with status `queued for sign-off`                                         | PASS — see §2 above. |
| OQ-1/3/7/8/10 have resolution-status field or owner pointer                                        | PASS — see §B inside the new section. |
| Implementation gates reference decisions by ADR ID                                                  | PASS — see §C inside the new section. |
| `artifacts/D-0021/spec.md` records the update summary                                              | PASS — file created at `.dev/releases/current/cliEval/artifacts/D-0021/spec.md`. |

## 5. Reproducibility

To re-verify the content delta:

```bash
# Show R3 entry and Sign-off table
sed -n '/Revision log:/,/PROPOSED-R2/p' .dev/releases/current/cliEval/decisions.md

# Show OPS-001 Closure section
sed -n '/## OPS-001 Closure/,$p' .dev/releases/current/cliEval/decisions.md
```

No pytest target, CLI command, or Makefile gate is associated with T01.25 (EXEMPT tier).
