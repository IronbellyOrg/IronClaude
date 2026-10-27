# D-0106 — Notes

## Design notes

1. **Why a closure section and not a new ADR.** DOC-OQ9 is a documentation
   closure of an open question, not a new architectural decision. The
   architectural decision implicit in v1 Linux-only scope was made at
   design-spec authoring time (design-spec.md:30, §16:812) and is
   already canonical in the spec; DOC-OQ9 ratifies that scope in the
   ADR log and names the owner + target for the deferred capability.
   Following the convention established by §"DOC-OQ7 Closure" (T04.15)
   and §"OPS-001 Closure" (T01.25), this lands as a closure section
   appended to the existing ADR log rather than a new D-N entry.

2. **Owner choice — RyanW.** Two candidates were considered:
   (a) RyanW (architect, named owner of MIG-003 in roadmap row 360 and
   resolution owner of OQ-9 in roadmap row 380); (b) leaving the owner
   field empty for "the v2 release lead, TBD." Option (a) was chosen
   because (i) MIG-003 already names RyanW as the platform follow-up
   owner, so DOC-OQ9 inheriting that owner keeps the v2 follow-up trail
   single-headed and (ii) DOC-OQ9 closure cannot ship with an empty
   owner field — the roadmap row 349 AC explicitly requires one.

3. **Target date choice — 2026-Q3.** Three candidates were considered:
   (a) a fixed calendar date (e.g., 2026-09-30); (b) a calendar quarter
   (2026-Q3); (c) a milestone-triggered date ("v2 planning gate"). The
   chosen formulation combines (b) and (c): the high-level target is
   2026-Q3, with two concrete sub-dates — re-evaluation at 2026-07-01
   (v2 planning gate, the start of Q3) and ship-or-defer recorded
   against MIG-003 by 2026-09-30 (end of Q3). This gives a grep-able
   calendar quarter for human consumers plus two precise dates for any
   automated follow-up tracker.

4. **Re-evaluation triggers (whichever first).** Three triggers are
   named because the v2 planning gate alone could be deferred by other
   priorities, in which case (b) a formal macOS support request or (c)
   Anthropic publishing macOS-equivalent TTY behaviour would still
   surface the question. The "whichever first" language preserves
   maintainer flexibility while bounding the worst-case delay.

5. **Cross-reference mechanism with AC1.** AC1 is owned by T06.07
   (Phase 6, this same release), which lands after T06.02. T06.02
   therefore cross-references AC1 by its roadmap row ID (R-109, row 353)
   rather than by a `decisions.md` anchor that does not yet exist; when
   T06.07 lands, its `decisions.md` AC1 entry will cross-reference
   §"DOC-OQ9 Closure" in return. The two cross-references are
   intentionally redundant on the "Linux-only for v1" assertion so the
   SC5 OQ-ledger sweep (T06.09) catches any maintainer drift between
   them.

6. **Why not include OQ-9 in the OPS-001 §B table.** OPS-001 §B was
   defined at T01.25 as the resolution-status table for OQ-1, OQ-3,
   OQ-7, OQ-8, OQ-10. OQ-9 was scoped to M6 and is closed here.
   Appending OQ-9 to §B would be a structural change to OPS-001's
   scope; instead, the SC5 OQ-1..OQ-10 ledger (T06.09) is the canonical
   single-table view of all 10 OQs, and T06.02 emits a closure section
   that T06.09 will read.

## Edge cases considered

- **What if RyanW transfers ownership of MIG-003.** The Reject/revise
  rule applies: a new revision log entry records the owner change; the
  original `Resolution:` line stays for audit. The DOC-OQ9 owner field
  must stay in sync with MIG-003's owner — drift here would be a real
  audit issue.
- **What if v2 is renamed or restructured.** "v2" in this section
  refers to the next release after the current v1 cliEval delivery, as
  recorded in the v2 follow-up roadmap entry owned by T06.15. If the
  versioning scheme changes, the target date and triggers stay valid;
  only the "v2" label needs updating.
- **What if Windows support is later added.** DOC-OQ9 explicitly
  excludes Windows from its scope. A future Windows decision would
  land as a separate closure or new ADR; DOC-OQ9 is not the catch-all
  for non-Linux platforms.
- **What if the macOS follow-up is delivered before 2026-Q3.** That's
  fine — the target date is an upper bound on when the question must
  be re-evaluated, not a lower bound on when delivery can occur. An
  early-delivery would amend this section with an `Outcome:` line.

## Validation steps performed

1. Read `decisions.md` §"DOC-OQ9 Closure" end-to-end and confirmed the
   Decision table contains owner + target date.
2. Confirmed the §Cross-reference to AC1 subsection cites roadmap row
   353 / R-109 / T06.07 (the AC1 implementation site).
3. Confirmed the §Closure of OQ-9 subsection explicitly records the
   status flip with `Resolution status: RESOLVED — 2026-05-20`.
4. Confirmed the §Consequences subsection names downstream consumers
   (T06.07, T06.09, T06.13, T06.15).
5. Grepped `decisions.md` for `DOC-OQ9` and `OQ-9` to confirm the
   resolution text is the canonical authority (no contradictory
   earlier entry).
