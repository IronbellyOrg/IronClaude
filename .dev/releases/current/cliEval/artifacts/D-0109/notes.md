# D-0109 — Notes

## Design notes

1. **Why a closure section and not a new ADR.** AC2 is a documentation
   ratification of v1 scope (CI integration is deferred), not a new
   architectural decision. The architectural decision implicit in
   "no CI for v1" was made at design-spec authoring time
   (design-spec.md §16 non-goals) and is already canonical in the spec.
   Following the convention established by §"DOC-OQ9 Closure" (T06.02,
   R6) — which lands the reciprocal macOS scope statement — this lands
   as a closure section appended to the existing ADR log rather than a
   new D-N entry.

2. **Why pair AC2 explicitly with AC1.** Roadmap rows 352 (AC2) and 353
   (AC1) sit adjacent in the docs lane and together bound the v1 scope
   envelope on two orthogonal axes: AC1 restricts the platform (Linux);
   AC2 restricts the execution context (local). A downstream consumer
   reading only one of the two could mistakenly assume the other axis
   was open (e.g., "Linux + GitHub Actions" or "macOS local"). The
   redundant cross-link in both entries forces a maintainer who edits
   one without the other to produce visible drift in the SC5 OQ-ledger
   sweep (T06.09), the same drift-detection pattern used by DOC-OQ9 ↔
   AC1 (R6 above).

3. **Revisit trigger — why three clauses in "whichever first" form.**
   The roadmap row 352 AC asks for "a trigger for CI revisit" without
   prescribing the form. Three formulations were considered:
   (a) calendar-only (e.g., "revisit at v2 planning gate"); (b) request-
   only (e.g., "any maintainer can reopen with a written ask"); (c) data-
   driven only (e.g., "3+ harness regressions per month triggers CI
   work"). Each in isolation has a failure mode:
   - calendar-only leaves no escalation signal during the v1.x window;
   - request-only is not "concrete" enough for the AC (any maintainer
     could open AC2 at any time, no data threshold);
   - data-only requires that someone is counting regressions, which is
     not enforced anywhere in v1.
   The chosen "whichever first" composition of all three closes each
   failure mode with another clause. The clause ordering follows the
   expected fire frequency in the v1.x window: (a) data threshold most
   likely to fire if CI would actually help; (b) stakeholder request as
   the override path; (c) calendar gate as the floor.

4. **Why the 3-regressions-per-month threshold.** The threshold is a
   calibration of "would CI have saved enough developer time to pay for
   itself." Lower (1-2/month): CI overhead (workflow authoring,
   maintainer time on flake triage, GitHub Actions minutes) exceeds the
   time saved by catching the regression earlier. Higher (5+/month): the
   harness is already unstable enough that CI is needed urgently and the
   maintainer would file (b) before reaching (a). The month-long
   observation window dampens noise from a single bad week. The
   threshold is intentionally human-counted (a maintainer reviewing
   `git log` over a month) rather than instrumented — instrumenting
   regression detection is a strict superset of CI itself, so any
   instrumentation work would already have crossed trigger (b).

5. **Owner choice — RyanW.** Two candidates were considered:
   (a) RyanW (architect, named owner of MIG-003 in roadmap row 360 and
   of the DOC-OQ9 macOS follow-up in R6); (b) leaving the owner field
   empty for "the v2 release lead, TBD." Option (a) was chosen to keep
   the v2 follow-up trail single-headed: MIG-003 names CI + macOS
   together with a single owner, and AC2 inheriting that owner avoids a
   split-ownership audit issue if MIG-003 ever transfers ownership.

6. **Target window choice — 2026-Q3, mirroring DOC-OQ9.** AC2's
   target window is set to match DOC-OQ9's (2026-Q3 with sub-dates
   2026-07-01 / 2026-09-30) because MIG-003 (T06.15) consolidates both
   into a single v2 follow-up roadmap entry. Splitting AC2 onto a
   different target window would force MIG-003 to carry two timelines,
   which the v2 follow-up roadmap entry is not designed to do.

7. **Why no `--ci` flag verification in this task.** Step 1 of T06.05
   says "Confirm v1 scope is Linux-only local-only per AC1," which is a
   read-only check. The harness already ships no `--ci` flag, no GitHub
   Actions workflow, and no CI badge — verifying this is part of the
   OPS-005 release checklist walk-through (T06.13), not T06.05. AC2 is
   a documentation closure of an already-existing posture, not a code
   gate.

8. **Why AC2 is not in the SC5 OQ-1..OQ-10 ledger.** SC5 (R-111,
   roadmap row 357, owned by T06.09) is the ledger for the ten
   numbered Open Questions (OQ-1..OQ-10). AC2 is an Acceptance
   Criterion, not an Open Question; including it in the SC5 ledger
   would conflate two distinct decision categories. The SC5 ledger does
   consume this section as the v1 scope-boundary attestation paired
   with AC1 — i.e., the M6 exit checkpoint (T06.16) reads both AC1 and
   AC2 closures to confirm v1 scope is locked.

## Edge cases considered

- **What if RyanW transfers ownership of MIG-003.** The Reject/revise
  rule applies: a new revision log entry records the owner change; the
  original `Resolution:` line stays for audit. The AC2 owner field
  must stay in sync with MIG-003's owner — drift here would be a real
  audit issue and is caught by the T06.09 SC5 sweep.

- **What if `make verify-sync` is misread as "CI".** `make verify-sync`
  + the AC11 pre-commit hook (T01.20) are local discipline tools —
  they run on the developer machine before a commit lands. They do not
  satisfy AC2's CI requirement (no remote runner, no scheduled
  execution, no notification path to a maintainer who is not at the
  workstation). The AC2 closure explicitly excludes local-CI affordances
  from the "out of scope for the CI follow-up" row to forestall this
  misreading.

- **What if a future revisit chooses NOT to add CI.** Path (b) of the
  closure consequences applies: a new ADR records the re-evaluation
  outcome (e.g., "CI still deferred at v2; revisit again at v3 planning
  gate") and this section is amended with an `Outcome:` line. Multiple
  iterations of deferral are explicitly permitted; AC2 is not a
  one-way ratchet to "must add CI eventually."

- **What if trigger (a) fires but the maintainer disagrees with the
  data.** The three triggers are independent "whichever first" — a fire
  on (a) does not force CI to land, it forces a revisit ADR. The
  maintainer can record an `Outcome:` line on this section that the
  3-regressions-per-month threshold mis-fired (e.g., all three were the
  same root cause), and the threshold can be re-calibrated in the new
  ADR.

- **What if the v2 planning gate slips past 2026-07-01.** Trigger (c)
  fires on the calendar date, not on "the v2 planning gate happening."
  A slipped gate forces AC2 to be re-read on 2026-07-01 regardless; the
  maintainer can record an `Outcome:` line confirming the slip and the
  revisit is deferred to the new gate date, leaving (a) and (b) still
  active.

## Validation steps performed

1. Read `decisions.md` §"AC2 Closure" end-to-end and confirmed the
   Decision table contains the CI status row + revisit trigger row.
2. Confirmed the §"Cross-reference to AC1 (Linux-only declaration)"
   subsection cites roadmap row 353 / R-109 / T06.07.
3. Confirmed the §"Closure of AC2" subsection explicitly records the
   status flip with `Resolution status: RESOLVED — 2026-05-20`.
4. Confirmed the §"Cross-reference to MIG-003" subsection names T06.15
   as the v2 follow-up consolidation site.
5. Confirmed the §Consequences subsection names downstream consumers
   (T06.07, T06.09, T06.13, T06.15).
6. Confirmed the §Revisit trigger rationale subsection records the
   3-regressions-per-month calibration so a future re-calibration has
   the original reasoning in audit.
7. Grepped `decisions.md` for `AC2` and `CI integration` to confirm
   the resolution text is the canonical authority (no contradictory
   earlier entry).
