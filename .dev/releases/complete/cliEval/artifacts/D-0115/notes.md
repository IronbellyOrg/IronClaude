# D-0115 — Design notes (OPS-005 release checklist)

**Task:** T06.13 — Assemble OPS-005 release checklist
**Date:** 2026-05-21

## Why a separate release checklist (vs. consuming OPS-004 directly)

OPS-004 fixes the **operational contract** for the four validation commands: order, surface, exit-code, evidence path. OPS-005 layers the **release framing** on top: which ADRs need sign-off, which success criteria need a closure entry, which follow-ups are named v2-scope. The two documents have different audiences:

- **OPS-004 audience:** an operator (or CI) re-executing the 4-command sequence on a clean tree.
- **OPS-005 audience:** the release-gate reviewer assembling the M6 exit-gate attestation.

Putting both into one document would force the operator-facing reproduction recipe (OPS-004 §6) to live next to the ADR sign-off table — that mixes two purposes and is harder to evolve. The split mirrors the precedent in `decisions.md`: per-closure sections (AC1 / SC3 / DOC-OQ6 / ...) stay focused on their own AC, and the SC5 ledger consumes the per-closure sections by reference.

## OPS-004 inheritance pattern (zero-duplication)

§5 of `release-checklist.md` lists the four OPS-004 commands but does **not** repeat the per-command body (purpose, command details, blocker analysis). Instead it cites `docs/eval/validation-commands.md` for the canonical text and just records the per-command observed outcome + evidence link.

The win: when OPS-004 evolves (e.g. a fifth command added, the B1/B2 closure replaces row 5.4's ❌ with ✅), only one document changes plus its audit test. OPS-005 picks up the new contract automatically because it references rather than duplicates.

The risk: a future maintainer might be tempted to inline OPS-004's per-command details into OPS-005 "for convenience". The mitigation is the `tests/cli/eval/test_validation_commands.py` audit (already landed at T06.11) — that test is the canonical source for the command list and forces any change to land in `docs/eval/validation-commands.md` first.

## Partial-attestation framing

T06.13 ships with `Fallback Allowed: Yes` because its upstream dependency T06.11 also carries `Fallback Allowed: Yes` and ended with two named blockers (B1 + B2). The release-checklist could have refused to land until B1 + B2 closed, but that would block four out of the five other Phase-6 follow-ons (T06.12, T06.14, T06.15, T06.16) from making progress while the M2 vendoring and T04.10 helper gaps are addressed.

The framing chosen:

1. **§5 records the observed outcome** verbatim, including the ❌ for row 5.4.
2. **§7.1 names B1 + B2 as P0 successor tasks** (T06.11-FU01, T06.11-FU02) with an owner.
3. **§8 row 3 (release-gate sign-off) is marked `_pending_`** so it is visible to the reviewer that the release is "Conditional GO" — not "GO unconditionally."
4. **§8 "Conditional-GO authority"** paragraph explicitly authorises the partial path with a reference to the `Fallback Allowed: Yes` task metadata.

This shape preserves audit-grade traceability (the failure is named, the closure path is named, the gating role is named) while letting the surrounding M6 work proceed.

## Why §7 lists MIG-001 (T06.14) as a follow-up

T06.13's phase metadata declares `Dependencies: T06.11`. T06.14 (MIG-001 source sync migration) is a separate STRICT-tier task that lands its own evidence at `evidence/T06.14/sync.log`. It is **not** a dependency of T06.13, but it is the formal attestation site for the AC11 source-of-truth gate.

OPS-004 row 5.2 (`make verify-sync`) already passes today (PASS evidence at `evidence/T06.11/02-make-verify-sync.log`) because the four sync axes (`skills | agents | commands | hooks`) are aligned. So MIG-001's evidence is "ceremonial" — a sub-agent-reviewed sync log captured under T06.14 for the M6 exit-gate audit trail.

Putting MIG-001 in §7.4 (rather than §6 row 6.3) makes the distinction explicit: §6.3 is the working-tree state (PASS today), §7.4 is the formal attestation step (lands when T06.14 runs).

## Why `quick.yaml` is in §7.3, not §6

`quick.yaml` is a planned subset suite, not a v1 deliverable. It would have been a §6 row if v1 shipped two suites; instead, v1 ships one (`real.yaml`, 15 evals) and `--eval <id>` is the documented subset escape hatch. §6.2 records the convention + the deferral; §7.3 carries the explicit follow-up entry with a trigger ("maintainer demand-signal OR R6 walltime ceiling exceeded post-v1").

The redundancy is intentional: §6.2 catches the reviewer who scans the suite-files quadrant; §7.3 catches the reviewer who scans the follow-ups quadrant. The two entries cite the same source-of-truth section (`decisions.md` §DOC-OQ6 Closure).

## Trade-off — no structural audit test for OPS-005

T06.11 / D-0114 shipped with a structural audit test (`tests/cli/eval/test_validation_commands.py`, 23 cases) because OPS-004 has a **pinnable** contract: four commands, four evidence filenames, two named blockers. The test asserts those constants are present in the document.

OPS-005 / D-0115 has a **looser** contract: nine ADRs (which is unlikely to grow), five SCs (frozen by SC1), six §6 rows (could grow if v2 lands new artifacts), and a follow-up list that explicitly grows over time. Pinning a structural audit on OPS-005 would either be brittle (asserting exact follow-up names) or trivial (asserting "§5 references validation-commands.md").

The chosen approach: rely on the OPS-004 audit test (already landed) + the manual link-audit captured at `evidence/T06.13/link-audit.log`. If a future drift pattern emerges (e.g. someone deletes the §7.4 MIG-001 row), the link audit + the §9 acceptance map will catch it. If broader drift coverage becomes necessary, a `tests/cli/eval/test_release_checklist.py` analogue can be added in a follow-up at minimal cost — the OPS-004 test is a direct template.

## Cross-references

- **T06.11 / D-0114 / OPS-004:** Inheritance source — the 4-command sequence consumed by §5.
- **T06.01 / D-0105 / SC1:** ADR sign-offs consumed by §3.
- **T06.08 / D-0111 / SC4:** Effort estimate consumed by §4 row SC4.
- **T06.09 / D-0112 / SC5:** OQ resolution ledger consumed by §4 row SC5.
- **T06.10 / D-0113 / SC3:** Zero-new-deps verification consumed by §4 row SC3.
- **T06.04 / D-0108 / DOC-OQ6:** Suite naming + `quick.yaml` consumed by §6.2 + §7.3.
- **T06.14 / D-0116 / MIG-001:** Sync migration referenced in §7.4 (not a dependency).
- **T06.15 / D-0117 / MIG-003:** Platform follow-up consumed by §7.2.
- **T06.16 / D-CP06 / M6 exit gate:** Consumes this checklist as the OPS-005 attestation.
