# Merge Log

## Metadata

- Base variant: V2 (sonnet:analyzer)
- Executor: orchestrator-inline (quick-depth probe run; no separate merge-executor dispatch)
- Changes planned: 13
- Changes applied: 13
- Changes failed: 0
- Changes skipped: 0
- Output: `../merged-requirements.md`
- Timestamp: 2026-05-25T19:32:45Z

## Changes Applied

| # | Description | Status | Provenance Tag | Validation |
|---|---|---|---|---|
| 1 | Add §3.5 Non-Functional Requirements (8 NFRs from V1) | ✓ Applied | Source: V1 §3 | NFR section present with NFR-001 through NFR-008 |
| 2 | Two-click discoverability rule | ✓ Applied | Source: V1 FR-004 | FR-006 in merged §3 |
| 3 | Audience-tag header convention | ✓ Applied | Source: V1 FR-006 | FR-008 in merged §3 |
| 4 | `superclaude doctor` as first diagnostic | ✓ Applied | Source: V1 FR-009 | FR-009 in merged §3 |
| 5 | Single-line command discipline | ✓ Applied | Source: V1 NFR-007 | NFR-007 in merged §3.5 |
| 6 | DM-as-doc-bug improvement loop | ✓ Applied | Source: V1 §7 residual | Merged into §6.5 (improvement loop subsection) |
| 7 | Brevity caps + `wc -l` enforceability | ✓ Applied | Source: V1 NFR-001 + M-005 | NFR-001 in §3.5 |
| 8 | Hybrid layout: `docs/contributing/` directory with 4 audience-tagged files | ✓ Applied | Hybrid V1 FR-003 + V2 FR-002 spirit | INT-5 added; FR-002 in §3 |
| 9 | Both Make targets (`make onboard` + `make onboard-check`) | ✓ Applied | Hybrid V1 FR-005 + V2 FR-003 | FR-003 + FR-004 in §3 |
| 10 | Explicit decisions on all 6 seed-brief open questions | ✓ Applied | Source: V1 §7 | New §7 in merged spec |
| 11 | Retain V2 diagnosis-first opening | ✓ Applied (no-op) | Source: V2 §1 base | §1 unchanged from base |
| 12 | Promote shared assumptions to §9 | ✓ Applied | Source: AD-2 protocol output | §9 with SA-001 through SA-003 |
| 13 | Failure recovery routing in `make onboard` | ✓ Applied | Source: V1 advocate critique of V2 INT-2 | FR-013 in §3 |

## Post-Merge Validation

### Structural Integrity

- ✅ Heading hierarchy consistent (H1 → H2 → H3 only; no orphans)
- ✅ Section ordering logical: Diagnosis → Interventions → FRs → NFRs → Falsification → Not-Doing → Adoption → Metrics → Open-Q decisions → Assumptions → Shared Assumptions
- ✅ Document starts with H1
- ✅ 11 top-level sections (vs 7 in either source variant — additions: §3.5 NFRs, §6.5 Metrics promoted to dedicated, §7 Open-Q decisions, §9 Shared Assumptions)

### Internal References

- Total references: 32 (FR-NNN, NFR-NNN, INT-N, RC-N, A-N, SA-NNN, NFR-001..008)
- Resolved: 32
- Broken: 0

### Contradiction Re-Scan

- Pre-merge contradictions (X-001 layout, X-002 Make name): both resolved via hybrid (Change #8 + Change #9)
- New contradictions introduced by merge: 0
- Cross-check: FR-003 (`make onboard`) and FR-004 (`make onboard-check`) coexist non-contradictorily; FR-004 may delegate to FR-003 via `--ci` flag (no semantic conflict)

### Provenance Annotations

- Document header annotation present (provenance + base + date + convergence)
- Per-section `<!-- Source: ... -->` tags on all 11 sections
- Hybrid sections explicitly tagged (e.g., "Hybrid V1 FR-003 + V2 FR-002 spirit")

### Falsifiability Coverage

Every FR and NFR has at least one of:

- Inline "Falsifiable: …" gate (V2 pattern retained)
- Explicit CI check (`make onboard-check`)
- Grep / wc / time / head command suitable for scripting

All FRs: ✅ falsifiable. All NFRs: ✅ falsifiable except NFR-006 (tone neutrality — necessarily subjective; documented as such).

## Summary

- Planned: 13
- Applied: 13
- Failed: 0
- Skipped: 0
- Status: **success**
- Convergence: 1.00 (16/16 diff points resolved)
- Unresolved conflicts: 0
