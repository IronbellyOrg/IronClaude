# Refactor Plan — Merge V3 (base) + V2 (decisive transfers) + V1 (kernel)

## Overview
- **Base:** V3 (4-gate rubric) — score 0.895, selected as the only framework-generalizable scaffold
- **Decisive transfers:** V2's framework-level guards (without which the base fails the probe)
- **Kernel:** V1's narrow applied-work delegation case
- **Change count:** 4 incorporations + 3 invariant-driven additions
- **Risk:** Low — the recommendation defaults to the lowest-blast-radius outcome (keep bespoke; delegation is a hard-gated exception)

## Planned Changes

### Change #1 — Add a framework-level aggregate verifier-heterogeneity invariant (CRITICAL, resolves INV-001/INV-003)
- **Source:** V2 monoculture thesis (U-001) + INV-001/INV-003
- **Target:** V3 rubric — add a **G0 framework gate** evaluated *before* per-protocol gates
- **Rationale:** the per-protocol rubric structurally cannot see the aggregate concentration of reflect-as-verifier; N locally-correct delegations sum to monoculture, and the rubric's own success condition (recurring applied-work) is the monoculture trigger.
- **Integration:** G0 = "the fraction of protocols whose *sole* independent verifier is reflect must stay below a framework-set bound; crossing it requires an owned, recorded decision and a heterogeneity remediation." Delegation is permitted only if G0 *and* G1–G4 pass.
- **Risk:** Low (adds a guard; defaults conservative)

### Change #2 — Require an independent cross-check of reflect itself (CRITICAL, resolves INV-002/INV-004)
- **Source:** V2 A-003 argument + INV-002/INV-004
- **Target:** V3 rubric — add a standing rule, not a per-protocol gate
- **Rationale:** "preserve out-of-band watchers" is nominal — surviving bespoke validators verify their *own* protocols and never cross-check reflect-on-Y. And auggie-review already runs reflect as a *sole blocking validator* at Phase E (`context.md` §1.4, `SKILL.md:327`) with no non-reflect watcher.
- **Integration:** (a) reflect's own output must be periodically cross-checked by a *non-reflect* surface (e.g., a sampled human/operator audit, or a heterogeneous non-reflect validator) — the watcher must actually watch reflect; (b) flag auggie-review Phase E as a *pre-existing* sole-reflect-blocking seam to review independently of this proposal.
- **Risk:** Low (additive safety rule)

### Change #3 — Bind A-002 freeze to a real mechanism + add gate-staleness re-trigger (resolves INV-008/INV-005)
- **Source:** V1's "freeze first" concession + V2's moving-target point + INV-008/INV-005
- **Target:** V3 rubric preconditions
- **Rationale:** "freeze the contract" in prose, against a contract edited this session with 146-line drift, is freeze-in-name-only; and a recorded gate verdict goes stale when a protocol's contract changes.
- **Integration:** delegation precondition = reflect contract pinned by version/hash with a CI/eval gate; each protocol's gate verdict carries the contract-version it was decided against and is re-run on contract change.
- **Risk:** Low (process)

### Change #4 — Owner + non-uniform fail-direction (resolves INV-006)
- **Source:** V3's own concession + INV-006
- **Target:** V3 rubric governance
- **Rationale:** unowned, the rubric rots to "always keep bespoke" — safe vs monoculture but UNSAFE for high-stakes auto-applying protocols that then get a cheap validator instead of the rigor their blast radius needs.
- **Integration:** name an owner who applies/records the rubric; for high-blast-radius auto-apply protocols, the safe default is *more* verification (heterogeneous, possibly-including-reflect), not bespoke-by-rot.
- **Risk:** Low

## Changes NOT Being Made (rejected)
- **V1 blanket "always delegate":** rejected. Collapsed under its own concessions; violates A-003 catastrophically (INV-002); monoculture (INV-001/003).
- **Remove either named target's bespoke validator now:** rejected. Unanimous keep; auggie-review fails G1+G3, cleanup-audit fails G1+G2 (circular `audit-validator`, `SKILL.md:561`).
- **V2 bare blanket "never":** rejected as the *framework* answer. Cannot encode the applied-work exception V2 itself concedes; "all future protocols" needs a procedure. (V2's *substance* is fully incorporated as the framework guards.)

## Risk Summary
| Change | Risk | If wrong | Rollback |
|---|---|---|---|
| #1 G0 aggregate invariant | Low | monoculture creeps unmonitored | drop G0 |
| #2 reflect cross-check | Low | reflect stays self-validated | drop rule |
| #3 freeze mechanism + staleness | Low | drift/stale verdicts persist | drop precondition |
| #4 owner + fail-direction | Low | rubric rots / under-verifies high-stakes | drop governance note |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-06-04
