# D-0105 — SC1 ADR sign-offs D-1..D-8 spec

**Task:** T06.01 (Phase 6, Roadmap SC1 / R-104)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR sign-off)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## SC1 contract

Roadmap row 348 (SC1 / R-104) requires:

1. `decisions.md` contains 8 ADR entries with sign-off date.
2. OQ-1 resolution recorded.
3. ADRs cross-reference roadmap deliverables.

The authoritative satisfaction site is the R5 update applied to
`.dev/releases/current/cliEval/decisions.md` in this task. R5 (a) appends
`signed_off_by` + `signed_off_date` metadata blocks to each of D-1..D-8,
(b) appends a `Roadmap cross-reference` line citing roadmap row IDs that
consume each decision, (c) flips the Sign-off table from QUEUED → APPROVED
for D-1..D-8 plus D-10 (D-10 piggy-backs on the same sign-off pass per the
R4 → R5 expectation in `D-10 Consequences`), (d) flips OQ-1 from OPEN to
RESOLVED in the OPS-001 §B table because the queued sign-off pass was
OQ-1's resolution gate.

## Sign-off summary

| ADR | Decision summary | signed_off_by | signed_off_date | Roadmap rows referenced |
|-----|------------------|---------------|-----------------|--------------------------|
| D-1 | Fork ptytest, vendor under `cli/eval/pty/` | RyanW | 2026-05-20 | NFR-MAINT1 (23), AC10 (25), COMP-007 (36) |
| D-2 | Port `Expect.*` DSL as Python primitives | RyanW | 2026-05-20 | COMP-010 (12), FR-EXP1 (64), COMP-010.1..6 (65–70) |
| D-3 | `HomeIsolation` composes `IsolationLayers` | RyanW | 2026-05-20 | FR-ISO1 (28), COMP-006 (32), FR-ISO2 (29) |
| D-4 | YAML manifest + Python callback escape hatch | RyanW | 2026-05-20 | DM-011 (2), DM-002 (3), FR-SCH1 (4), COMP-002 (6) |
| D-5 | Hook-matcher coverage gate (G5 falsifiable) | RyanW | 2026-05-20 | FR-G5 (75), TEST-013 (101), MIG-002 (103) |
| D-6 | `--max-disk-mb` poller (R4 enforcement) | RyanW | 2026-05-20 | NFR-PERF4 (60), COMP-003 (57) |
| D-7 | Three-layer path-traversal hardening | RyanW | 2026-05-20 | FR-SCH2 (5), FR-ISO2 (29), AC12 (16), NFR-SEC1 (7) |
| D-8 | Reporter consumes N' + status taxonomy | RyanW | 2026-05-20 | COMP-008 (55), FR-RPT1 (54), COMP-003 (57) |
| D-10 | NOTICE/LICENSE attribution for vendored ptytest | RyanW | 2026-05-20 | NFR-MAINT1 (23), DOC-OQ4 (24), AC10 (25) |

(D-9 is a reconciliation note, not a release ADR; it does not carry a SC1 sign-off requirement.)

## OQ-1 resolution

| OQ | Prior status | New status | `resolution:` text |
|----|--------------|------------|--------------------|
| OQ-1 | OPEN (queued at T01.25 / OPS-001) | **RESOLVED — 2026-05-20** | RyanW signed off D-1..D-8 (and D-10) in R5 sign-off pass; see Sign-off table in `decisions.md` for per-ADR signatures + dates. OPS-001 queue cleared; SC1 acceptance criterion satisfied. |

OQ-7 was independently resolved at T04.15 (see `decisions.md` §"DOC-OQ7 Closure").
OQ-3, OQ-8, OQ-10 remain DEFERRED per design — they are tracked separately and do not block M6 exit.

## Acceptance-criteria → site map (T06.01)

| AC bullet (T06.01) | Where satisfied |
|--------------------|-----------------|
| `decisions.md` contains 8 ADR entries (D-1..D-8) with `signed_off_by` + `signed_off_date` populated. | Each ADR section in `decisions.md` now begins with a metadata block carrying both fields; Sign-off table reflects 🟢 APPROVED (R5) for all 8 rows with RyanW + 2026-05-20. |
| OQ-1 entry shows `resolution:` field populated. | `decisions.md` §"OPS-001 Closure" §B row OQ-1 updated; explicit `resolution:` text quoted in the table. |
| Each ADR cross-references at least one roadmap deliverable ID. | Each ADR section gained a `Roadmap cross-reference:` line naming the consuming roadmap row IDs (see summary table above). |
| `artifacts/D-0105/spec.md` records the sign-off summary. | This file. |

## Out of scope for T06.01

- Substantive edits to D-1..D-8 decision bodies — sign-off ratifies the existing R2 + R3 text; the Reject/revise rule in `decisions.md` governs any future textual amendments.
- D-9 (validation reconciliation note) — not a release ADR; no SC1 sign-off requirement.
- Roadmap or roadmap-state edits — out of scope for SC1 row 348.
- Closing OQ-3 / OQ-8 / OQ-10 — deferred-by-design; tracked elsewhere.
