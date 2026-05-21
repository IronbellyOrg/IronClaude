# D-0105 — Evidence

## Direct verification commands

```bash
# 1) Count signed_off_by lines (expect 8 ADR + 1 D-10 = 9)
grep -c '^\*\*signed_off_by:\*\* RyanW' .dev/releases/current/cliEval/decisions.md

# 2) Count signed_off_date lines (expect 9)
grep -c '^\*\*signed_off_date:\*\* 2026-05-20' .dev/releases/current/cliEval/decisions.md

# 3) Count Roadmap cross-reference lines on ADR sections (expect 8 for D-1..D-8)
grep -c '^\*\*Roadmap cross-reference:\*\*' .dev/releases/current/cliEval/decisions.md

# 4) Confirm Sign-off table shows APPROVED for all 9 rows
grep -c '🟢 APPROVED (R5)' .dev/releases/current/cliEval/decisions.md

# 5) Confirm OQ-1 row flipped to RESOLVED with explicit resolution text
grep -E 'OQ-1.*RESOLVED.*2026-05-20' .dev/releases/current/cliEval/decisions.md
```

Expected output of the four counts: 9, 9, 8, 9.

## Per-ADR sign-off verification

| ADR | signed_off_by | signed_off_date | Roadmap cross-reference present |
|-----|---------------|-----------------|---------------------------------|
| D-1 | RyanW | 2026-05-20 | yes (NFR-MAINT1, AC10, COMP-007) |
| D-2 | RyanW | 2026-05-20 | yes (COMP-010, FR-EXP1, COMP-010.1..6) |
| D-3 | RyanW | 2026-05-20 | yes (FR-ISO1, COMP-006, FR-ISO2) |
| D-4 | RyanW | 2026-05-20 | yes (DM-011, DM-002, FR-SCH1, COMP-002) |
| D-5 | RyanW | 2026-05-20 | yes (FR-G5, TEST-013, MIG-002) |
| D-6 | RyanW | 2026-05-20 | yes (NFR-PERF4, COMP-003) |
| D-7 | RyanW | 2026-05-20 | yes (FR-SCH2, FR-ISO2, AC12, NFR-SEC1) |
| D-8 | RyanW | 2026-05-20 | yes (COMP-008, FR-RPT1, COMP-003) |
| D-10 | RyanW | 2026-05-20 | (D-10 carries its own attribution clause; cross-references named in its Consequences block: NFR-MAINT1, DOC-OQ4, AC10) |

## OQ-1 resolution evidence

`decisions.md` §"OPS-001 Closure" §B, row OQ-1:

> **RESOLVED — 2026-05-20.** `resolution:` RyanW signed off D-1..D-8 (and
> D-10) in R5 sign-off pass; see Sign-off table above for per-ADR
> signatures + dates. OPS-001 queue cleared; SC1 acceptance criterion
> satisfied.

## SC1 acceptance crosscheck

Roadmap row 348 (SC1 / R-104) AC: "decisions.md contains 8 ADR entries
with sign-off date; OQ-1 resolution recorded; ADRs cross-reference
roadmap deliverables."

| AC element | Satisfied at |
|------------|--------------|
| 8 ADR entries with sign-off date | Sign-off table (9 rows with `2026-05-20`); per-ADR `signed_off_date` metadata (8 ADRs). |
| OQ-1 resolution recorded | OPS-001 §B row OQ-1 (RESOLVED with explicit `resolution:` text). |
| ADRs cross-reference roadmap deliverables | Per-ADR `Roadmap cross-reference:` line (8 ADRs), each citing 2–4 roadmap rows by stable ID + numeric position. |

All three SC1 AC bullets resolved.

## Cross-link

- Evidence summary: `.dev/releases/current/cliEval/evidence/T06.01/summary.md`
- ADR log: `.dev/releases/current/cliEval/decisions.md` (R5)
- Companion spec: `artifacts/D-0105/spec.md`
- Design rationale: `artifacts/D-0105/notes.md`
