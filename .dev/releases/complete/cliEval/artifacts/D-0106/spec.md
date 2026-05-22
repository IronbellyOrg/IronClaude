# D-0106 — DOC-OQ9 macOS support roadmap entry spec

**Task:** T06.02 (Phase 6, Roadmap DOC-OQ9 / R-105)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## DOC-OQ9 contract

Roadmap row 349 (DOC-OQ9 / R-105) requires:

1. `decisions.md` contains a macOS follow-up entry naming **owner** and **target date**.
2. AC1 (Linux-only declaration, R-109, roadmap row 353) is reaffirmed for v1.
3. OQ-9 status flips OPEN → RESOLVED.

The authoritative satisfaction site is the R6 revision applied to
`.dev/releases/current/cliEval/decisions.md`, which adds a new
`DOC-OQ9 Closure` section that (a) records the macOS follow-up owner,
target date, and re-evaluation triggers, (b) cross-references AC1 as
the reciprocal Linux-only declaration, (c) explicitly flips OQ-9 to
`RESOLVED — 2026-05-20`, and (d) names downstream consumers (T06.07,
T06.09, T06.13, T06.15).

## macOS follow-up summary

| Field | Value |
|---|---|
| **v1 platform scope** | Linux only (AC1, roadmap row 353; design-spec.md:30, §16:812). |
| **macOS status (v1)** | NON-GOAL. No `Darwin` support in v1. `eval doctor` refuses non-Linux platforms (AC1 wiring, T06.07). |
| **macOS follow-up owner** | RyanW (architect; matches MIG-003 owner, roadmap row 360). |
| **macOS follow-up target date** | 2026-Q3. Re-evaluation at v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30. |
| **Re-evaluation triggers (whichever first)** | (a) v2 planning gate 2026-07-01; (b) first formal macOS-platform support request filed against this repo; (c) Anthropic documents Claude Code TTY behaviour on macOS to be Linux-equivalent for the hook surface exercised by E1..E15. |
| **Out-of-scope for the macOS follow-up** | Windows. Windows remains a non-goal beyond v2 per design-spec.md:812. |

## OQ-9 resolution

| OQ | Prior status | New status | `resolution:` text |
|----|--------------|------------|--------------------|
| OQ-9 | OPEN (M6 entry blocker per roadmap row 380) | **RESOLVED — 2026-05-20** | Deferred to v2. v1 ships Linux-only per AC1. macOS follow-up owner: RyanW; target date: 2026-Q3 (re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30); re-evaluation triggers enumerated in `decisions.md` §"DOC-OQ9 Closure". |

OQ-9 was the only M6-scoped OQ outside the OPS-001 §B table; T06.02 closes it. The SC5 OQ-1..OQ-10 ledger (T06.09) inherits this resolution verbatim.

## AC1 cross-reference

AC1 (R-109, roadmap row 353) declares what v1 IS (Linux-only); DOC-OQ9 declares what v1 IS NOT (macOS/Windows) and names the deferred-capability owner + target.

- **AC1 declaration site (v1):** `README.md` (added by T06.07) + `decisions.md` AC1 entry (added by T06.07) + `eval doctor` non-Linux refusal (wired by T06.07).
- **DOC-OQ9 declaration site (v1):** `decisions.md` §"DOC-OQ9 Closure" (this artifact).
- **Cross-link mechanism:** the DOC-OQ9 closure section explicitly cites AC1 by roadmap row ID; T06.07's AC1 entry, when it lands, will cross-reference §"DOC-OQ9 Closure" in return. The two sections are intentionally redundant on the "Linux-only for v1" assertion so the next SC5 OQ-ledger sweep (T06.09) catches any drift.

## Acceptance-criteria → site map (T06.02)

| AC bullet (T06.02) | Where satisfied |
|--------------------|-----------------|
| File `decisions.md` contains a `DOC-OQ9` entry naming the macOS follow-up owner and target date. | `decisions.md` §"DOC-OQ9 Closure" §Decision table — `macOS follow-up owner: RyanW` + `macOS follow-up target date: 2026-Q3`. |
| Entry cross-references AC1 Linux-only declaration. | `decisions.md` §"DOC-OQ9 Closure" §Cross-reference to AC1 subsection, citing roadmap row 353 (R-109). |
| OQ-9 status changes from `open` to `resolved` in `decisions.md`. | `decisions.md` §"DOC-OQ9 Closure" §Closure of OQ-9 subsection — `Resolution status: RESOLVED — 2026-05-20`. |
| `artifacts/D-0106/spec.md` records the macOS follow-up summary. | This file. |

## Out of scope for T06.02

- Authoring the AC1 declaration content for `README.md` or wiring the `eval doctor` non-Linux refusal — owned by T06.07.
- Writing the v2 follow-up roadmap entry for MIG-003 (`docs/eval/v2-followups.md` or equivalent) — owned by T06.15.
- Closing other M6 OQs (OQ-1 resolved at T06.01; OQ-3, OQ-8, OQ-10 deferred per design; SC5 OQ-1..OQ-10 ledger landed by T06.09).
- Editing `roadmap.md` or `.roadmap-state.json` — out of scope for DOC-OQ9 row 349.
