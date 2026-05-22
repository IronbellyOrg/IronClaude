# D-0117 — Notes

## Design notes

1. **Why a consolidation document, not a new D-N ADR.** Three artifact
   shapes were considered for the MIG-003 follow-up: (a) a fresh D-N
   ADR in `decisions.md`; (b) a closure section on `decisions.md`
   pointing to a standalone consolidation document; (c) a standalone
   consolidation document only, with `decisions.md` updated solely in
   the revision log. Shape (b) was chosen. Shape (a) was rejected
   because MIG-003 is not a new decision — the macOS deferral was
   decided at R6 (DOC-OQ9) and the CI deferral was decided at R9
   (AC2). Adding a fresh ADR would create a third decision authority
   that drifts from the two already-canonical closures. Shape (c) was
   rejected because the ADR log needs a handle for the consolidation
   so a future SC5 sweep (T06.09 or a successor) can confirm MIG-003
   is RESOLVED in the ledger without reading outside `decisions.md`.
   Shape (b) gives both: a thin closure section in the ADR log + the
   detailed consolidation in a discoverable doc location.

2. **Why `docs/eval/v2-followups.md` (not in `.dev/releases/current/cliEval/`).**
   The consolidation document is a release-time / planning-time
   artifact that the v2 release-lead reads outside the v1 release
   workspace. `.dev/releases/current/cliEval/` is the current-release
   workspace; once v1 cuts, the directory rotates and becomes
   `current/cliEval` for the next release. `docs/eval/` is the
   long-lived documentation home that the OPS-005 release checklist
   (T06.13) already uses for `validation-commands.md`,
   `release-checklist.md`, `retention.md`, `retry.md`, etc. The v2
   follow-up roadmap entry belongs alongside those.

3. **Why preserve Windows as a permanent non-goal beyond v2.**
   Design-spec.md:812 records *"Cross-platform support (Linux first;
   macOS / Windows are follow-ups)"* — but the explicit MIG-003 row
   in `roadmap.md` (row 360) only names "macOS and future CI support."
   Two readings were considered: (i) Windows is implicit in "future"
   and should be carried by MIG-003; (ii) Windows is out-of-scope for
   MIG-003 entirely and is a v3+ concern at the earliest. Reading
   (ii) was chosen because design-spec.md:30 records macOS as the
   named follow-up and Windows as an open-ended one, and because no
   evaluator (CI runner, developer, or stakeholder) has filed a
   Windows-platform request against this repo. Carrying Windows in
   the MIG-003 v2 follow-up would force the v2 planning gate to take
   a decision on it without any signal; explicitly excluding it now
   defers that decision to a future ADR triggered by an actual
   request.

4. **Why `v2-followups.md` carries audit invariants (§5).** The
   four-way cross-reference graph (AC1 ↔ DOC-OQ9, AC1 ↔ AC2, AC1 ↔
   MIG-003, DOC-OQ9 ↔ AC2 via MIG-003) relies on owner / target /
   trigger fields staying synchronized across `decisions.md` §AC1
   Closure, §DOC-OQ9 Closure, §AC2 Closure, §MIG-003 Closure, and
   `v2-followups.md`. Drift between any two sites is a real audit
   issue. §5 enumerates the five invariants that MUST hold so a
   future maintainer reviewing one site (e.g., amending AC2's
   revisit trigger) sees the invariant set immediately and updates
   the other four sites in the same commit. The invariants are also
   the check-list the SC5 OQ-ledger sweep (T06.09) and the M6 exit
   checkpoint (T06.16) execute.

5. **Why the v1-blocking-work check is explicit (§6).** The roadmap
   row 360 AC says *"no v1 blocking work added"* — a negative
   assertion that is easy to satisfy implicitly and impossible to
   audit. §6 records the five concrete questions a reviewer asks to
   verify the negative: (i) new code change required? (ii) re-opens
   a v1 ADR? (iii) adds a task to Phase 1-5? (iv) modifies row 360
   AC? (v) adds `--ci` / Darwin code / harness change? All five must
   be NO. By writing the negative as a five-row table, the reviewer
   doesn't have to invent the checks at audit time.

6. **Owner choice — RyanW.** Two candidates were considered:
   (a) RyanW (architect, owner of MIG-003 in roadmap row 360 and of
   the upstream DOC-OQ9 + AC2 closures); (b) leaving the owner field
   empty for "the v2 release lead, TBD." Option (a) was chosen to
   keep the v2 follow-up trail single-headed — three sites
   (`decisions.md §DOC-OQ9 Closure`, §AC2 Closure, §MIG-003 Closure)
   name the same owner, and the consolidation document inherits it.
   If the owner ever transfers, a single coordinated update across
   all three sites + `v2-followups.md` §2.x + §7 sign-off keeps the
   audit graph consistent.

7. **Target window choice — 2026-Q3, mirroring R6 + R9.** MIG-003's
   target window is set to match DOC-OQ9 + AC2 (2026-Q3 with
   sub-dates 2026-07-01 / 2026-09-30) because the consolidation
   exists to land both axes on one calendar. Splitting MIG-003 onto
   a different target window would force the v2 planning gate to
   carry two timelines, which the consolidation document is not
   designed to do.

8. **Why R13 (and not a re-use of an earlier revision number).** R12
   was the last revision (SC5 closure, T06.09); R13 is the next
   integer in the revision log. The revision log is append-only —
   no in-place edits, no number re-use. R13 lands the MIG-003
   closure; future Phase-6 closures (none currently outstanding for
   T06.01-T06.15) would land at R14+.

9. **Why no roadmap.md edit.** Row 360 (R-116 / MIG-003) reads
   *"macOS non-goal preserved; CI non-goal preserved; follow-up
   roadmap item created; no v1 blocking work added."* The
   consolidation document is the follow-up roadmap item; both
   non-goals are preserved by the upstream R6 + R9 closures. The
   row's AC is satisfied by the existence of the consolidation
   artifact + this closure section, not by editing the row text.
   Touching `roadmap.md` would require the STRICT-tier change-control
   process (Section 5.3.2, migration keyword) and a separate ADR for
   the roadmap edit itself — out of scope for T06.15.

10. **Why `release-checklist.md` §7.2 is not edited.** OPS-005
    (T06.13, R-114) landed `docs/eval/release-checklist.md` with
    §7.2 already wiring MIG-003 / DOC-OQ9 / AC2 as the v2 platform
    follow-ups. The §7.2 "Successor / consolidation site" column
    already names `MIG-003 (T06.15)` and now points (via the §MIG-003
    Closure section in `decisions.md`) to `docs/eval/v2-followups.md`.
    Re-editing §7.2 to add the `v2-followups.md` link directly would
    require a fresh OPS-005 revision under T06.13's contract, which
    is closed.

## Edge cases considered

- **What if RyanW transfers ownership of MIG-003 mid-v1-cut.** The
  Reject/revise rule applies: a new revision log entry records the
  owner change; the original `Resolution:` line stays for audit.
  Five sites must update in the same commit: (i) `decisions.md
  §MIG-003 Closure` Decision summary table; (ii) `decisions.md
  §DOC-OQ9 Closure` owner field; (iii) `decisions.md §AC2 Closure`
  owner field; (iv) `docs/eval/v2-followups.md` §2.1 + §2.2 owner;
  (v) `docs/eval/v2-followups.md` §7 sign-off. The SC5 sweep
  (T06.09) catches inconsistency across the five.

- **What if the v2 planning gate (2026-07-01) slips.** Trigger (c) in
  each axis fires on the calendar date, not on "the v2 planning gate
  happening." A slipped gate forces a `v2-followups.md` §3 read-and-act
  pass on 2026-07-01 regardless; the consolidation document is
  amended with an `Outcome: slip — re-evaluated YYYY-MM-DD; new gate
  YYYY-MM-DD` line and the upstream closures get matching `Outcome:`
  lines. The 2026-09-30 ship-or-defer floor still applies — i.e.,
  the slip cannot push the ship-or-defer past 2026-09-30 without a
  fresh ADR.

- **What if a v2 release lands without macOS but with CI.** The two
  axes are independent — `v2-followups.md` §3 explicitly says the
  follow-up can be picked off per-axis. A CI-only v2 release lands
  an `Outcome: delivered at v2.x` line on the AC2 closure and a
  `Outcome: re-deferred at v2 planning gate, see §<new ADR>` line on
  the DOC-OQ9 closure; the consolidation document §2.1 stays open,
  §2.2 closes. The audit graph stays consistent because each axis
  has its own outcome.

- **What if a Windows platform request is filed.** §2.1 explicitly
  out-of-scopes Windows, but the request must still go somewhere.
  The expected path: a new D-N ADR records the Windows request and
  the decision (defer / accept / cancel); if accepted, a new
  follow-up consolidation document (or amendment to this one) lifts
  Windows into v3+ scope. MIG-003 is **not** re-opened to carry
  Windows; the consolidation document is calibrated to the macOS +
  CI two-axis shape and would need a structural rewrite to carry a
  third axis.

- **What if `eval doctor` is amended at v2 to accept Darwin.** That
  is the delivery path for §2.1. On landing, the consolidation
  document §2.1 gets an `Outcome: delivered at v2.x — eval doctor
  accepts Darwin per <new ADR>` line; the upstream §DOC-OQ9 Closure
  gets a matching `Outcome:` line; `README.md` §"Platform support"
  adds a Darwin row; the AC1 closure section gets an amendment
  citing the new platform-support matrix. Four-site coordinated
  update — the same shape as the owner-transfer edge case.

- **What if R9 (AC2) is amended before v2 (e.g., a trigger
  re-calibration).** §5 invariant #5 says the three-clause "whichever
  first" triggers in `v2-followups.md` §2.2 MUST match the AC2
  closure's triggers verbatim. A trigger re-calibration in R9 must
  produce a same-commit edit to `v2-followups.md` §2.2. The SC5 sweep
  (T06.09 or a successor) catches drift if either side is updated
  alone.

## Validation steps performed

1. Read `decisions.md` §"DOC-OQ9 Closure" (lines 580-625) end-to-end
   and confirmed the owner = RyanW, target = 2026-Q3 with sub-dates
   2026-07-01 / 2026-09-30, status = RESOLVED — 2026-05-20.
2. Read `decisions.md` §"AC2 Closure" (lines 763-831) end-to-end and
   confirmed the owner = RyanW, target = 2026-Q3 with sub-dates
   2026-07-01 / 2026-09-30, three-clause "whichever first" trigger,
   status = RESOLVED — 2026-05-20.
3. Read `decisions.md` §"AC1 Closure" headers and revision log entry
   R10 and confirmed Linux-only platform declaration is in place
   with `eval doctor` refusing non-Linux hosts.
4. Read `docs/eval/release-checklist.md` §7.2 and confirmed the
   MIG-003 row already names `T06.15` as the consolidation site,
   with owner = RyanW.
5. Read `roadmap.md` row 360 and confirmed R-116 / MIG-003 AC text
   matches the four-bullet contract this task implements.
6. Confirmed `docs/eval/v2-followups.md` §6 five-row negative
   verification — all five rows answer NO (no v1-blocking work added).
7. Confirmed the four-way cross-reference graph (AC1 ↔ DOC-OQ9, AC1
   ↔ AC2, AC1 ↔ MIG-003, DOC-OQ9 ↔ AC2 via MIG-003) is fully wired
   by the prior R6 / R9 / R10 closures + this R13 closure.
8. Grepped `decisions.md` for `MIG-003` to confirm the new §MIG-003
   Closure section is the canonical authority and that R6 + R9 entries
   continue to cross-reference it (they do — written at R6 + R9
   authoring time, no edit required).
