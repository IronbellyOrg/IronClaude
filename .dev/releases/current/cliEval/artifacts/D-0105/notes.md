# D-0105 — Notes

## Design notes

1. **Sign-off mechanism.** SC1 (roadmap row 348) requires that `decisions.md`
   "contains 8 ADR entries with sign-off date." The existing Sign-off table
   already had a Date column but lacked a populated Signed column and the
   per-ADR `signed_off_by` / `signed_off_date` fields the task spec asks for.
   T06.01 (a) populates the table, (b) appends explicit `signed_off_by` and
   `signed_off_date` metadata at the head of each ADR section so the fields
   are grep-able per-decision rather than table-only.

2. **D-10 included in the same pass.** D-10 (NOTICE/LICENSE attribution)
   landed in R4 with "QUEUED FOR SIGN-OFF (R4) pending maintainer (RyanW)
   approval at the same M1/M2 exit pass as D-1..D-8" (see D-10 Consequences
   in `decisions.md`). The R5 pass therefore signs off D-10 alongside the
   eight ADRs SC1 names. The SC1 acceptance criterion lands on D-1..D-8;
   the D-10 sign-off is an additive byproduct of the same pass.

3. **OQ-1 resolution wording.** OQ-1's resolution condition is verbatim
   "pending maintainer sign-off pass on D-1..D-8. This task queues the
   sign-off; the sign-off itself is the resolution." (OPS-001 §B). R5 is
   that sign-off, so OQ-1's `resolution:` text quotes the action that
   resolved it.

4. **Roadmap cross-reference sources.** Each ADR's cross-reference line
   cites roadmap rows by their numeric position in the roadmap.md table
   plus their stable ID (e.g., NFR-MAINT1 row 23). The pairing is
   intentional: numeric position is the cheap grep anchor; the stable ID
   is the durable identifier across roadmap renumbering. The same mapping
   already exists informally in the OPS-001 Closure §C table; T06.01
   propagates it into the ADRs themselves so the cross-reference survives
   even if §C is rewritten.

5. **What R5 does NOT touch.** R5 does not rewrite Context / Options /
   Decision / Rationale / Consequences bodies. Sign-off ratifies the
   prior text; any future textual amendment goes through the
   Reject/revise mechanism (add a row to "Revisions"; do not edit
   originals in place).

## Edge cases considered

- **D-9 omitted.** D-9 is a validation-reconciliation note added to the
  ADR log post-pipeline; it does not represent a release decision and is
  not counted toward SC1's "8 ADR entries." The SC1 count is D-1..D-8.
- **Sign-off date vs decision date.** The decision body for D-5..D-8 was
  authored 2026-05-18 (R2); the sign-off pass landed 2026-05-20 (R5).
  Per ADR-lite convention, the sign-off date is the date of approval,
  not the date of decision authorship.
- **OQ-7 already resolved.** OQ-7 was resolved at T04.15 (see DOC-OQ7
  Closure section in `decisions.md`) with `resolution: YES — --junit
  supported`. The `Net` update line under §B notes this.

## Validation steps performed

1. Walked the Sign-off table to confirm 8 ADR entries (D-1..D-8) plus D-10
   each show `🟢 APPROVED (R5)`, `RyanW`, `2026-05-20`.
2. Grepped each ADR section head for `signed_off_by:` and
   `signed_off_date:` — 8 matches.
3. Grepped each ADR section head for `Roadmap cross-reference:` — 8
   matches; spot-checked each cross-reference against roadmap.md table.
4. Confirmed §B row OQ-1 now reads RESOLVED with explicit `resolution:`
   text.
5. Confirmed `acceptance-criteria → site map` block in `spec.md` cites
   the locations of all four AC bullets.
