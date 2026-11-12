---
title: Orca Read-Only Terminal Observer - PRD Addendum
slug: orca-observer
parent: prd.md
created: 2026-11-08
updated: 2026-11-08
---

# PRD Addendum: Orca Read-Only Terminal Observer

This addendum holds the traceability matrix and points to the technical detail. It does not copy that detail: each item has one source of truth in the spec folder `_bmad-output/specs/spec-orca-observer/`, and later steps (UX, architecture) read it there.

## A. Where the technical detail lives

| Detail | Single source | PRD section that depends on it |
|---|---|---|
| Adapter argv templates, forbidden set, cycle budget, caps, back-off, error forms | `adapter-contract.md` | NFR-7, NFR-9, FR-9 |
| Snapshot fields, `schemaVersion`, additive rule, `UNKNOWN`, withheld fields (PROPOSED) | `snapshot-export-schema.md` | FR-16, NFR-10, NFR-11 |
| Geometry per width, COUNTS strip, notice text, row grammar, exact pinned strings | `rendering-rules.md` | FR-3 to FR-15, NFR-1 to NFR-6 |
| Key map | `rendering-rules.md` (copied once into NFR-5) | NFR-5 |
| Stack facts and the key-reader spike | `stack.md` | FR-2, NFR-12 |
| Test list T1-T51 and AC mapping | `acceptance-tests.md` | Section 9 |
| Release gates and the four data-gate sample kinds | `release-gates.md` | Section 4 |
| Owner decisions, risks, dissents | `owner-decisions-and-risks.md` | Sections 4, 10, 12.2 |
| Unverified register | `unverified-register.md` | Section 13.2 |
| Write-back future stage | `write-back-future-stage.md` | Section 11 |

## B. Traceability matrix: capability to requirement to test

| Spec capability | Release | PRD requirement | Spec tests |
|---|---|---|---|
| CAP-1 Fixture replay | R0 | FR-1, FR-2 | T6, T7, T16, T50 |
| CAP-2 Worker ledger | R1 | FR-3, FR-4, FR-5, FR-6 | T9, T13, T17, T20, T21, T22, T32, T39, T45 |
| CAP-3 Question-source notice | R1 | FR-7 | T9, T33, T47 |
| CAP-4 Completeness and freshness | R1 | FR-8, FR-9, FR-10 | T4, T5, T18, T35, T38, T40, T42 |
| CAP-5 Separate facts, no inference | R1 | FR-11, FR-12 | T13, T14, T15, T31, T34; FR-12 issue-sourced items have no test |
| CAP-6 Selection and inspector | R1 | FR-13 | T24, T25, T43; no test for `selected <id> no longer in source window` (OI-6) |
| CAP-7 Changes since last look | R1 | FR-14 | T8, T10, T41 |
| CAP-8 Terminal safety and legibility | all | NFR-1 to NFR-6 | T3, T23, T25, T26, T28, T29, T30, T35, T44, T49, manual CJK check |
| CAP-9 Text export | R1 | FR-15 | T27, T48 |
| CAP-10 JSON snapshot | R1 | FR-16 | snapshot schema test, ID not assigned (OI-6) |
| CAP-11 Attention Ledger | R2 | FR-17 | T10, T11, T12, T19, T46, T51 |
| CAP-12 Decision Desk | R3 | FR-18 | none (OI-6) |
| Spec Constraints | all | NFR-7 to NFR-14 | T1, T2, T4, T5, T6, T11, T13, T27, T29, T36, T37, T38, T40; NFR-12 and NFR-14 have no test |

Coverage check (2026-11-08, by search): every test ID T1-T51 in `acceptance-tests.md` is cited at least once in `prd.md`. Every CAP-1 to CAP-12 maps to at least one FR or NFR.

## C. Counts

- Functional requirements: 18 (FR-1 to FR-18). R0: 2. R1: 14. R2: 1. R3: 1.
- Non-functional requirements: 14 (NFR-1 to NFR-14).
- Open questions carried verbatim: 15 (OQ-1 to OQ-15). Other open items: 13 (OI-1 to OI-13).
