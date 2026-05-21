# D-0109 — Evidence

## Direct verification commands

```bash
# 1) Confirm AC2 Closure section header exists in decisions.md
grep -nE '^## AC2 Closure' .dev/releases/current/cliEval/decisions.md

# 2) Confirm "CI: deferred (local-only v1)" semantics recorded
grep -nE 'CI status \(v1\).*NON-GOAL|local developer machines only' .dev/releases/current/cliEval/decisions.md

# 3) Confirm revisit trigger is a concrete three-clause "whichever first" form
grep -nE 'Revisit trigger.*whichever first|3\+ harness regressions|first formal CI-integration request|v2 planning gate 2026-07-01' .dev/releases/current/cliEval/decisions.md

# 4) Confirm AC2 flipped to RESOLVED on 2026-05-20
grep -nE 'Resolution status: RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md

# 5) Confirm AC1 cross-reference (roadmap row 353 / R-109) is present in AC2 section
grep -nE 'AC1.*(R-109|row 353|roadmap row 353|Linux-only)' .dev/releases/current/cliEval/decisions.md

# 6) Confirm MIG-003 cross-reference (T06.15, row 360) is present in AC2 section
grep -nE 'MIG-003.*(R-116|row 360|T06\.15)' .dev/releases/current/cliEval/decisions.md

# 7) Confirm R9 revision log entry recorded
grep -nE '^- R9 \(2026-05-20\): AC2 closure' .dev/releases/current/cliEval/decisions.md
```

Expected: each command above returns at least one match.

## Per-AC verification

| AC bullet (T06.05) | Verification step | Result |
|--------------------|-------------------|--------|
| `decisions.md` contains an `AC2` entry stating "CI: deferred (local-only v1)" with a named revisit trigger. | `grep` for `^## AC2 Closure` + Decision-table rows naming `CI status (v1): NON-GOAL` and the three-clause revisit trigger. | PASS — section header present; Decision-table records local-only execution context + three-clause "whichever first" trigger. |
| Cross-reference to AC1 Linux-only declaration is recorded. | Confirm §"Cross-reference to AC1 (Linux-only declaration)" subsection cites roadmap row 353 / R-109 / T06.07. | PASS — subsection present with all three citations. |
| AC2 entry status is `resolved`. | Confirm §"Closure of AC2" subsection records `Resolution status: RESOLVED — 2026-05-20`. | PASS — explicit `RESOLVED — 2026-05-20` line present. |
| `artifacts/D-0109/spec.md` records the deferral summary. | Confirm file exists with Decision table + AC2 resolution table + AC1 cross-reference + MIG-003 cross-reference + AC site map. | PASS — `artifacts/D-0109/spec.md` written this commit. |

## AC2 resolution evidence

`decisions.md` §"AC2 Closure" §"Closure of AC2":

> - **Question:** Is CI integration in scope for v1, and if not, what
>   triggers a revisit?
> - **Resolution:** Not in scope for v1. v1 ships local-only per AC1
>   (Linux-only platform restriction) + this section (local-only
>   execution-context restriction). CI integration is deferred to v2
>   with owner RyanW and target window 2026-Q3 (re-evaluate at v2
>   planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by
>   2026-09-30). Revisit trigger is a three-clause "whichever first":
>   (a) 3+ harness regressions caught locally in a single calendar
>   month, (b) first formal CI-integration request filed against this
>   repo, or (c) v2 planning gate 2026-07-01.
> - **Resolution status:** RESOLVED — 2026-05-20.

## AC1 cross-reference evidence

`decisions.md` §"AC2 Closure" §"Cross-reference to AC1 (Linux-only declaration)":

> AC1 (roadmap row 353, R-109) declares the platform restriction for
> v1 (Linux-only) and wires `eval doctor` to refuse non-Linux platforms
> with a friendly error. T06.07 is the implementation site for the
> README + doctor wiring. AC2 declares the execution-context
> restriction (local-only) and is satisfied by this `decisions.md`
> section alone — no code wiring is required because the harness
> already has no CI affordances to remove.

## MIG-003 cross-reference evidence

`decisions.md` §"AC2 Closure" §"Cross-reference to MIG-003 (v2 platform follow-up plan)":

> MIG-003 (R-116, roadmap row 360, owned by T06.15) is the canonical v2
> follow-up roadmap entry that names both macOS support and CI
> integration as deferred scope. AC2 lands the CI half of that
> deferral in the ADR log; DOC-OQ9 (R6 above) landed the macOS half.
> T06.15 reads both closures and emits a single v2 follow-up roadmap
> entry covering both axes; no fresh decision is required there.

## Revisit trigger evidence

`decisions.md` §"AC2 Closure" §Decision table — `Revisit trigger (whichever first)`:

> **(a)** 3+ harness regressions caught locally in a single calendar
> month (a regression here = an `eval run --suite real` failure on
> `master` HEAD that a CI smoke run would have caught earlier);
> **(b)** first formal CI-integration request filed against this repo
> (e.g., GitHub issue, PR, or stakeholder request from RyanW);
> **(c)** v2 planning gate 2026-07-01 — whichever first surfaces the
> question, the revisit lands in a fresh ADR (this section is amended
> with an `Outcome:` line per the Reject/revise rule).

## AC2 acceptance crosscheck

Roadmap row 352 (AC2 / R-108) AC: *"decisions.md entry says local-only
for v1; trigger for CI revisit recorded."*

| AC element | Satisfied at |
|------------|--------------|
| "decisions.md entry says local-only for v1" | `decisions.md` §"AC2 Closure" §"Decision" table row `v1 execution context: Local developer machines only` + Decision section heading `CI integration is deferred to v2; v1 ships local-only`. |
| "trigger for CI revisit recorded" | `decisions.md` §"AC2 Closure" §"Decision" table row `Revisit trigger (whichever first)` enumerating clauses (a)/(b)/(c) + §"Revisit trigger — rationale for the three-clause 'whichever first' form" subsection. |

Both AC elements satisfied.

## Cross-link

- Evidence summary: `.dev/releases/current/cliEval/evidence/T06.05/summary.md`
- ADR log: `.dev/releases/current/cliEval/decisions.md` (R9, §"AC2 Closure")
- Companion spec: `artifacts/D-0109/spec.md`
- Design rationale: `artifacts/D-0109/notes.md`
- Downstream consumers:
  - T06.07 (AC1 wiring in README + `eval doctor`; AC1↔AC2 redundant cross-link completed when T06.07's AC1 entry lands and cites §"AC2 Closure" in return)
  - T06.09 (SC5 OQ-1..OQ-10 ledger; reads AC1+AC2 closures together as the v1 scope-boundary attestation)
  - T06.13 (OPS-005 release checklist; carries "local-only" alongside "Linux only" as v1 release-notes headline)
  - T06.15 (MIG-003 v2 follow-up roadmap entry; inherits the CI deferral verbatim alongside the macOS deferral from DOC-OQ9)
