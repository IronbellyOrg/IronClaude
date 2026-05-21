# D-0106 — Evidence

## Direct verification commands

```bash
# 1) Confirm DOC-OQ9 Closure section header exists in decisions.md
grep -nE '^## DOC-OQ9 Closure' .dev/releases/current/cliEval/decisions.md

# 2) Confirm macOS follow-up owner is recorded as RyanW
grep -nE 'macOS follow-up owner.*RyanW' .dev/releases/current/cliEval/decisions.md

# 3) Confirm macOS follow-up target date is recorded as 2026-Q3
grep -nE 'macOS follow-up target date.*2026-Q3' .dev/releases/current/cliEval/decisions.md

# 4) Confirm OQ-9 flipped to RESOLVED on 2026-05-20
grep -nE 'OQ-9|Resolution status: RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md | grep -A0 -B0 'DOC-OQ9\|OQ-9\|Resolution status'

# 5) Confirm AC1 cross-reference (roadmap row 353 / R-109) is present
grep -nE 'AC1.*(R-109|row 353|roadmap row 353)' .dev/releases/current/cliEval/decisions.md

# 6) Confirm R6 revision log entry recorded
grep -nE '^- R6 \(2026-05-20\): DOC-OQ9 closure' .dev/releases/current/cliEval/decisions.md
```

Expected: each command above returns at least one match.

## Per-AC verification

| AC bullet (T06.02) | Verification step | Result |
|--------------------|-------------------|--------|
| `decisions.md` contains a `DOC-OQ9` entry naming macOS follow-up owner + target date. | `grep` for `DOC-OQ9 Closure`, `macOS follow-up owner`, `macOS follow-up target date`. | PASS — owner: RyanW; target date: 2026-Q3 (with concrete sub-dates 2026-07-01 / 2026-09-30). |
| Entry cross-references AC1 Linux-only declaration. | Confirm §"Cross-reference to AC1" subsection cites roadmap row 353 / R-109 / T06.07. | PASS — subsection present with all three citations. |
| OQ-9 status changes from `open` to `resolved` in `decisions.md`. | Confirm §"Closure of OQ-9" subsection records `Resolution status: RESOLVED — 2026-05-20`. | PASS — explicit `RESOLVED — 2026-05-20` line present. |
| `artifacts/D-0106/spec.md` records the macOS follow-up summary. | Confirm file exists with Decision table + OQ-9 resolution table + AC1 cross-reference + AC site map. | PASS — `artifacts/D-0106/spec.md` written this commit. |

## OQ-9 resolution evidence

`decisions.md` §"DOC-OQ9 Closure" §"Closure of OQ-9":

> - **Question:** macOS support timeline and scope.
> - **Resolution:** Deferred to v2. v1 ships Linux-only per AC1. macOS
>   follow-up owner: RyanW; target date: 2026-Q3 (re-evaluate at v2
>   planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by
>   2026-09-30); re-evaluation triggers enumerated above.
> - **Resolution status:** RESOLVED — 2026-05-20.

## AC1 cross-reference evidence

`decisions.md` §"DOC-OQ9 Closure" §"Cross-reference to AC1 (Linux-only declaration)":

> AC1 (roadmap row 353, R-109) records the Linux-only v1 scope in
> `README.md` and wires `eval doctor` to refuse non-Linux platforms
> with a friendly error. T06.07 is the implementation site (Phase 6,
> this same release).

## DOC-OQ9 acceptance crosscheck

Roadmap row 349 (DOC-OQ9 / R-105) AC: *"decisions.md contains macOS
follow-up entry with owner + target; AC1 reaffirmed for v1."*

| AC element | Satisfied at |
|------------|--------------|
| macOS follow-up entry with owner + target | `decisions.md` §"DOC-OQ9 Closure" §"Decision" table (owner: RyanW; target: 2026-Q3). |
| AC1 reaffirmed for v1 | `decisions.md` §"DOC-OQ9 Closure" §"Cross-reference to AC1" + §"Decision" table row `v1 platform scope: Linux only`. |

Both AC elements satisfied.

## Cross-link

- Evidence summary: `.dev/releases/current/cliEval/evidence/T06.02/summary.md`
- ADR log: `.dev/releases/current/cliEval/decisions.md` (R6, §"DOC-OQ9 Closure")
- Companion spec: `artifacts/D-0106/spec.md`
- Design rationale: `artifacts/D-0106/notes.md`
- Downstream consumers:
  - T06.07 (AC1 wiring in README + `eval doctor`)
  - T06.09 (SC5 OQ-1..OQ-10 ledger; reads OQ-9 as RESOLVED)
  - T06.13 (OPS-005 release checklist; carries "Linux only" headline)
  - T06.15 (MIG-003 v2 follow-up roadmap entry; inherits owner + target verbatim)
