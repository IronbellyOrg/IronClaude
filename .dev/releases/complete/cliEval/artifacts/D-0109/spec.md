# D-0109 — AC2 CI integration deferral note spec

**Task:** T06.05 (Phase 6, Roadmap AC2 / R-108)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## AC2 contract

Roadmap row 352 (AC2 / R-108) requires:

1. `decisions.md` entry recording that CI integration is **deferred (local-only for v1)**.
2. A **concrete revisit trigger** documented in the same entry.
3. Cross-reference to AC1 (Linux-only declaration, R-109, roadmap row 353) so the AC1↔AC2 redundancy on v1 scope is closed.
4. AC2 status flips OPEN → RESOLVED.

The authoritative satisfaction site is the R9 revision applied to
`.dev/releases/current/cliEval/decisions.md`, which adds a new
`AC2 Closure` section that (a) records the CI deferral, (b) names a
three-clause "whichever first" revisit trigger, (c) cross-references
AC1 as the reciprocal Linux-only declaration, (d) cross-references
MIG-003 (T06.15) as the v2 follow-up consolidation site, (e) explicitly
flips AC2 to `RESOLVED — 2026-05-20`, and (f) names downstream consumers
(T06.07, T06.09, T06.13, T06.15).

## CI deferral summary

| Field | Value |
|---|---|
| **v1 execution context** | Local developer machines only (AC1 Linux-only + this entry local-only). |
| **CI status (v1)** | NON-GOAL. No GitHub Actions workflow, no scheduled job, no `--ci` flag, no CI badge at v1 ship. |
| **CI follow-up owner** | RyanW (matches MIG-003 owner, roadmap row 360). |
| **CI follow-up target window** | 2026-Q3. Re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30. |
| **Revisit triggers (whichever first)** | (a) 3+ harness regressions caught locally in a single calendar month; (b) first formal CI-integration request filed against this repo; (c) v2 planning gate 2026-07-01. |
| **Out-of-scope for the CI follow-up** | (i) macOS CI runners (covered by AC1 + DOC-OQ9 + MIG-003 — closed by macOS support landing, not by AC2); (ii) pre-commit-hook local-CI affordances (already shipped via `make verify-sync` + AC11 hook — local discipline, not CI in the AC2 sense). |

## AC2 resolution

| AC | Prior status | New status | `resolution:` text |
|----|--------------|------------|--------------------|
| AC2 | OPEN (roadmap row 352, M6 docs lane) | **RESOLVED — 2026-05-20** | Not in scope for v1. v1 ships local-only per AC1 (Linux-only platform) + this entry (local-only execution context). CI integration is deferred to v2 with owner RyanW and target window 2026-Q3 (re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30). Revisit trigger is a three-clause "whichever first": (a) 3+ harness regressions caught locally in a single calendar month, (b) first formal CI-integration request filed against this repo, or (c) v2 planning gate 2026-07-01. |

AC2 is an Acceptance Criterion, not an Open Question; it is therefore
not enumerated in the SC5 OQ-1..OQ-10 ledger (T06.09). The SC5 ledger
nevertheless consumes this section as the v1 scope-boundary attestation
that pairs with AC1 to close the local-only commitment for the M6 exit.

## AC1 cross-reference

AC1 (R-109, roadmap row 353) declares WHERE v1 runs (Linux only);
AC2 declares HOW v1 runs (local developer machines only, no CI).

- **AC1 declaration site (v1):** `README.md` (added by T06.07) + `decisions.md` AC1 entry (added by T06.07) + `eval doctor` non-Linux refusal (wired by T06.07).
- **AC2 declaration site (v1):** `decisions.md` §"AC2 Closure" (this artifact). No code change required at v1 — the harness already ships no CI affordances to remove.
- **Cross-link mechanism:** the AC2 closure section explicitly cites AC1 by roadmap row ID (R-109, row 353); T06.07's AC1 entry, when it lands, will cross-reference §"AC2 Closure" in return. The two sections are intentionally redundant on the "v1 scope envelope" assertion so the next SC5 OQ-ledger sweep (T06.09) catches any drift between them.

## MIG-003 cross-reference

MIG-003 (R-116, roadmap row 360, owned by T06.15) is the canonical v2
platform follow-up plan that names both macOS support and CI integration
as deferred scope. AC2 lands the CI half of that deferral in the ADR log;
DOC-OQ9 (R6, T06.02) landed the macOS half. T06.15 reads both closures
and emits a single v2 follow-up roadmap entry covering both axes; no
fresh decision is required there.

The owner + target window in §"AC2 Closure" MUST stay in sync with
MIG-003's owner + target window; drift between AC2 and MIG-003 on these
fields is a real audit issue and is caught by the T06.09 SC5 ledger
sweep.

## Acceptance-criteria → site map (T06.05)

| AC bullet (T06.05) | Where satisfied |
|--------------------|-----------------|
| File `decisions.md` contains an `AC2` entry stating "CI: deferred (local-only v1)" with a named revisit trigger. | `decisions.md` §"AC2 Closure" §Decision table — `CI status (v1): NON-GOAL` + `Revisit trigger (whichever first)` row enumerating (a)/(b)/(c). |
| Cross-reference to AC1 Linux-only declaration is recorded. | `decisions.md` §"AC2 Closure" §"Cross-reference to AC1 (Linux-only declaration)" subsection, citing roadmap row 353 / R-109 / T06.07. |
| AC2 entry status is `resolved`. | `decisions.md` §"AC2 Closure" §"Closure of AC2" subsection — `Resolution status: RESOLVED — 2026-05-20`. |
| `artifacts/D-0109/spec.md` records the deferral summary. | This file. |

## Out of scope for T06.05

- Authoring the AC1 declaration content for `README.md` or wiring the `eval doctor` non-Linux refusal — owned by T06.07.
- Writing the v2 follow-up roadmap entry consolidating macOS + CI scope — owned by T06.15 (MIG-003).
- Adding any `--ci` flag, GitHub Actions workflow, or CI-tuned output mode to the harness — explicitly out of scope; the harness ships with no CI affordances at v1 cut and this task ratifies that posture rather than changes it.
- Editing `roadmap.md` or `.roadmap-state.json` — out of scope for AC2 row 352.
- Closing other M6 ACs (AC1 closure owned by T06.07; AC11 source-of-truth gate closed earlier at T01.20).
