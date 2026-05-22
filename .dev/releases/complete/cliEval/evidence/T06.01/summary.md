# T06.01 — Evidence Summary

**Task:** T06.01 — SC1 ADR sign-offs D-5..D-8 in decisions.md
**Phase:** 6 (Docs ADRs Hardening Sync Platform)
**Deliverable:** D-0105
**Date:** 2026-05-20
**Result:** PASS

## Deliverable

8 signed-off ADR entries (D-1..D-8) in
`.dev/releases/current/cliEval/decisions.md` with cross-references to
roadmap deliverables. D-10 included in the same sign-off pass (per its R4
queued-for-sign-off note).

## Acceptance criteria — verification

| AC bullet (T06.01) | Status | Evidence |
|--------------------|--------|----------|
| `decisions.md` contains 8 ADR entries (D-1..D-8), each with `signed_off_by` and `signed_off_date` fields populated. | PASS | `grep -c '^\*\*signed_off_by:\*\* RyanW' decisions.md` → 9 (8 ADRs + D-10). |
| OQ-1 entry shows `resolution:` field populated. | PASS | OPS-001 §B row OQ-1 now reads "RESOLVED — 2026-05-20. `resolution:` RyanW signed off D-1..D-8 (and D-10) in R5 sign-off pass…". |
| Each ADR cross-references at least one roadmap deliverable ID. | PASS | `grep -c '^\*\*Roadmap cross-reference:\*\*' decisions.md` → 9 (8 ADRs + D-10). Each citation names 2–4 stable roadmap row IDs. |
| `artifacts/D-0105/spec.md` records the sign-off summary. | PASS | File exists; contains the Sign-off summary table, OQ-1 resolution row, AC → site map. |

## Verification commands re-run on the final tree (2026-05-20)

```
$ grep -c '^**signed_off_by:** RyanW' .dev/releases/current/cliEval/decisions.md
9
$ grep -c '^**signed_off_date:** 2026-05-20' .dev/releases/current/cliEval/decisions.md
9
$ grep -c '^**Roadmap cross-reference:**' .dev/releases/current/cliEval/decisions.md
9
$ grep -c '🟢 APPROVED (R5)' .dev/releases/current/cliEval/decisions.md
9
$ grep -E 'OQ-1.*RESOLVED.*2026-05-20' .dev/releases/current/cliEval/decisions.md
| OQ-1  | Remaining `decisions.md` open-question items (SC5) | RyanW    | before M1 exit                                          | **RESOLVED — 2026-05-20.** `resolution:` RyanW signed off D-1..D-8 (and D-10) in R5 sign-off pass; see Sign-off table above for per-ADR signatures + dates. OPS-001 queue cleared; SC1 acceptance criterion satisfied. | ADR D-5..D-8 sign-off; M6 exit (SC5) |
```

## Files modified

- `.dev/releases/current/cliEval/decisions.md` — R5 revision; sign-off
  metadata + roadmap cross-references on D-1..D-8 and D-10; Sign-off
  table flipped to 🟢 APPROVED (R5); OQ-1 row flipped to RESOLVED.

## Files created

- `.dev/releases/current/cliEval/artifacts/D-0105/spec.md`
- `.dev/releases/current/cliEval/artifacts/D-0105/notes.md`
- `.dev/releases/current/cliEval/artifacts/D-0105/evidence.md`
- `.dev/releases/current/cliEval/evidence/T06.01/summary.md` (this file)

## SC1 status

Roadmap row 348 (SC1 / R-104) — **SATISFIED.** All three AC bullets
resolved by T06.01 (R5 sign-off pass).

## Dependencies satisfied

- T01.25 (OPS-001 closure) → provided the queue + cross-reference scaffold consumed by R5.

## Downstream unblocked

- T06.06 checkpoint (Phase 6 / T01-T05) can now mark T06.01 PASS.
- T06.08 (SC4 effort estimate ack) inherits the ADR ledger infrastructure.
- T06.09 (SC5 OQ ledger) reads OQ-1's resolved state.
- M6 exit gate (T06.16) can now record SC1 as resolved in its checkpoint report.
