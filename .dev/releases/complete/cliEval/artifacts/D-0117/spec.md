# D-0117 — MIG-003 platform follow-up plan spec

**Task:** T06.15 (Phase 6, Roadmap MIG-003 / R-116)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## MIG-003 contract

Roadmap row 360 (MIG-003 / R-116) requires:

1. macOS non-goal preserved for v1.
2. CI non-goal preserved for v1.
3. A v2 follow-up roadmap item created consolidating both axes.
4. No v1-blocking work added.

The authoritative satisfaction sites are:

- **R13 revision** applied to `.dev/releases/current/cliEval/decisions.md` (revision log entry + new `§"MIG-003 Closure"` section between the §"OQ-2 Resolution" / §"SC5 OQ resolution ledger" tail and the future M6 exit checkpoint write).
- **New file** `docs/eval/v2-followups.md` (consolidation document, owned by this task).

R13 + `v2-followups.md` together form a two-artifact MIG-003 satisfaction surface:

- `decisions.md §"MIG-003 Closure"` is the ADR-log handle — it cites the upstream closures (R6 / R9 / R10), names the consolidation artifact, flips MIG-003 OPEN → RESOLVED, and adds the four-way cross-reference matrix.
- `docs/eval/v2-followups.md` is the consolidation document — it carries the two-axis follow-up scope (macOS §2.1, CI §2.2), the v2 planning-gate read-and-act list (§3), the audit invariants (§5), and the explicit five-row v1-blocking-work negative check (§6).

## Follow-up summary

| Axis | v1 posture | Upstream closure | Consolidation site | Owner | Target window |
|---|---|---|---|---|---|
| macOS (DOC-OQ9) | NON-GOAL — `eval doctor` refuses non-Linux hosts. | `decisions.md §"DOC-OQ9 Closure"` (R6, 2026-05-20). | [`docs/eval/v2-followups.md` §2.1](../../../../../../docs/eval/v2-followups.md). | RyanW | 2026-Q3 (re-evaluate 2026-07-01; ship-or-defer 2026-09-30). |
| CI (AC2) | NON-GOAL — no GitHub Actions workflow, no `--ci` flag, no CI badge. | `decisions.md §"AC2 Closure"` (R9, 2026-05-20). | [`docs/eval/v2-followups.md` §2.2](../../../../../../docs/eval/v2-followups.md). | RyanW | 2026-Q3 (re-evaluate 2026-07-01; ship-or-defer 2026-09-30). |
| Linux v1 platform ratification | Linux-only at v1. | `decisions.md §"AC1 Closure"` (R10, 2026-05-20). | Preserved by `docs/eval/v2-followups.md` §1 table + §5 audit invariant #3. | RyanW | (v1; ratified, not deferred) |
| Windows | NON-GOAL beyond v2 (design-spec.md:812). | n/a | `docs/eval/v2-followups.md` §2.1 "Out-of-scope" row. | n/a | Permanent non-goal beyond v2. |

## MIG-003 resolution

| Roadmap row | Prior status | New status | `resolution:` text |
|---|---|---|---|
| 360 / R-116 / MIG-003 | OPEN (M6 docs/planning lane) | **RESOLVED — 2026-05-20** | Consolidated at `docs/eval/v2-followups.md`. Inherits owner RyanW and 2026-Q3 target window from R6 (DOC-OQ9) and R9 (AC2). Preserves Linux-only v1 platform commitment per R10 (AC1). Windows remains a non-goal beyond v2. No v1-blocking work added (verified by `docs/eval/v2-followups.md` §6 five-row negative check). No new code, no roadmap edit, no fresh ADR. |

MIG-003 is a roadmap row, not an Open Question; it is therefore not enumerated in the SC5 OQ-1..OQ-10 ledger (T06.09). The SC5 ledger nevertheless reads this closure as the v1 follow-up-scope attestation paired with AC1 + AC2 + DOC-OQ9 closures.

## Cross-reference graph

The four-way cross-reference graph wired by Phase 6 closures (DOC-OQ9 ↔ AC1, AC2 ↔ AC1, DOC-OQ9 ↔ AC2 via MIG-003, AC1 ↔ MIG-003):

```
                  ┌──────────────────────────────────┐
                  │ AC1 Closure (R10) — Linux-only   │
                  │ decisions.md §AC1 Closure         │
                  └────────┬─────────────────────┬────┘
                           │                     │
              "where v1 IS"│                     │"v2 platform commitment"
                           │                     │
                  ┌────────▼────────┐   ┌────────▼─────────┐
                  │ DOC-OQ9 Closure │   │  AC2 Closure     │
                  │ (R6) — macOS    │   │  (R9) — CI       │
                  │ NON-GOAL v1     │   │  NON-GOAL v1     │
                  └────────┬────────┘   └────────┬─────────┘
                           │                     │
                           │   "consolidation"   │
                           ▼                     ▼
                  ┌──────────────────────────────────┐
                  │ MIG-003 Closure (R13) — this ADR │
                  │ + docs/eval/v2-followups.md      │
                  │ Owner: RyanW. Target: 2026-Q3.   │
                  └──────────────────────────────────┘
```

A maintainer who edits any one of {AC1, DOC-OQ9, AC2, MIG-003} closures without the others will produce visible drift in the SC5 OQ-ledger sweep (T06.09) and at the M6 exit checkpoint (T06.16). The redundancy is intentional and is the drift-detection mechanism Phase 6 relies on.

## Acceptance-criteria → site map (T06.15)

| AC bullet (T06.15) | Where satisfied |
|--------------------|-----------------|
| A follow-up roadmap entry (in decisions.md or `docs/eval/v2-followups.md`) records macOS + CI as deferred scope. | `docs/eval/v2-followups.md` §2.1 (macOS) + §2.2 (CI), plus `decisions.md §"MIG-003 Closure"` Decision summary table. |
| macOS non-goal and CI non-goal are preserved (referenced from AC1 + AC2). | `docs/eval/v2-followups.md` §1 (AC1 / AC2 / DOC-OQ9 references) + §5 audit invariants (Linux-only inheritance, CI scope boundary); `decisions.md §"MIG-003 Closure"` Cross-references-preserved table. |
| No new v1-blocking work is added (verified by reading the follow-up entry). | `docs/eval/v2-followups.md` §6 five-row negative verification (all five rows pass); `decisions.md §"MIG-003 Closure"` Decision summary table → `v1-blocking work check: Negative`. |
| `TASKLIST_ROOT/artifacts/D-0117/spec.md` records the follow-up summary. | This file (§"Follow-up summary" + §"MIG-003 resolution" + §"Cross-reference graph"). |

## Out of scope for T06.15

- Authoring new D-N ADR entries — MIG-003 is a consolidation, not a new decision; the upstream R6 + R9 ADR closures stand as the decision authorities.
- Modifying `roadmap.md` row 360 (R-116) AC text — the row's AC is satisfied by the consolidation artifact's existence, not by editing the row.
- Editing `README.md`, `eval doctor`, or any harness code — AC1 wiring is owned by T06.07; AC2 wiring is documentation-only (already landed at R9). MIG-003 changes no code surface.
- Editing `docs/eval/release-checklist.md` §7.2 — the OPS-005 row was pre-wired by T06.13 and already names MIG-003 (T06.15) as the consolidation site; no edit is required in this task.
- Re-deriving the macOS or CI follow-up scope — both are inherited verbatim from R6 (DOC-OQ9) and R9 (AC2). MIG-003 lifts, it does not re-decide.
- Defining a Windows follow-up plan — Windows remains a permanent non-goal beyond v2 per design-spec.md:812; MIG-003 explicitly excludes it.
