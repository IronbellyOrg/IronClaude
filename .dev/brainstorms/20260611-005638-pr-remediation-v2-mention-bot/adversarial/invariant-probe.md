# Invariant Probe Results (Round 2.5 — AD-1)

Independent fault-finder (opus, no advocacy role) probing the **emerging consensus**
(split dispatcher/runner host + ledger-as-SoT + effective-level-minimum autonomy). This
gate runs BEFORE convergence is declared; HIGH+UNADDRESSED items block convergence.

| ID | Category | Assumption (probed) | Status | Severity |
|----|----------|---------------------|--------|----------|
| INV-001 | state_variables | Runner can `git push` while `GH_TOKEN` absent from runner env (push IS an authenticated GitHub action) | UNADDRESSED | **HIGH** |
| INV-002 | interaction_effects | "Commit round to disk BEFORE the act" guarantees SC-5 loop-safety | UNADDRESSED | **HIGH** |
| INV-003 | guard_conditions | TOCTOU closed by authz re-check — but parent-comment BODY (opComment) is not re-checked | UNADDRESSED | **HIGH** |
| INV-007 | sufficiency_challenge | propose-only guarantees zero pushes despite sandbox having git + `--dangerously-skip-permissions` | UNADDRESSED | **HIGH** |
| INV-004 | collection_boundaries | "Reject residual non-whitelisted mention text" — vs "@bot fix please" mass false-rejects + silent | UNADDRESSED | MEDIUM |
| INV-005 | interaction_effects | SHA "head == push or **descendant**" predicate for round attribution | UNADDRESSED | MEDIUM |
| INV-006 | guard_conditions | `effective = MIN(parsed, authz, validation, needs_human, budget)` over heterogeneous types | UNADDRESSED | MEDIUM |
| INV-009 | interaction_effects | Per-PR flock + per-PR/thread round counter (ambiguous keying) | UNADDRESSED | MEDIUM |
| INV-010 | state_variables | resolveReviewThread node-id mapping (pagination + databaseId vs node-id) | UNADDRESSED | MEDIUM |
| INV-011 | guard_conditions | Stale-`claimed` recovery: every routine runner crash needs a human | UNADDRESSED | MEDIUM |
| INV-012 | sufficiency_challenge | "Dispatcher holds ONLY a dispatch credential" — still a 24/7 repo-write PAT | UNADDRESSED | MEDIUM |
| INV-015 | state_variables | Network deny-by-default "except GitHub git/HTTPS" — github.com-shaped exfil hole | UNADDRESSED | MEDIUM |
| INV-017 | sufficiency_challenge | uv-based pre-push gate inside a no-PyPI sandbox → false validation failures | UNADDRESSED | MEDIUM |
| INV-018 | count_divergence | max-rounds bound vs thread-proliferation bypass (count that matters = pushes-per-PR) | UNADDRESSED | MEDIUM |
| INV-008 | collection_boundaries | Parentless root mention → hard reject | ADDRESSED (in variants; underspecified in consensus) | LOW |
| INV-013 | collection_boundaries | Zero-Medium+ re-review terminates cleanly | ADDRESSED | LOW |
| INV-014 | interaction_effects | Authorize mention-author only; parent author = data not authority | ADDRESSED (genuine strength) | LOW |
| INV-016 | guard_conditions | Unknown/garbled flag → propose (fail-safe direction) | ADDRESSED (tokenizer precision is the sub-risk) | LOW |

## Summary

- **Total findings:** 18
- **HIGH + UNADDRESSED: 4** → INV-001, INV-002, INV-003, INV-007 — **CONVERGENCE BLOCKED** until resolved
- **MEDIUM + UNADDRESSED: 10** → INV-004, 005, 006, 009, 010, 011, 012, 015, 017, 018
- **LOW / ADDRESSED: 4** → INV-008, 013, 014, 016

## Gate decision

Per AD-1: `convergence requires count(HIGH + UNADDRESSED) == 0`. **Status: BLOCKED_BY_INVARIANTS.**
Resolution path: the merge (Step 4–5) MUST close all 4 HIGH items. Three have their fix
already present in a variant (INV-001/003 → security variant; INV-007 → security network/
credential boundary); INV-002 requires a synthesis (two-phase intent/outcome ledger record)
neither variant fully had. After resolution-in-merge, the spec re-clears the gate. The 10
MEDIUM items are recorded as explicit design resolutions or named open decisions in the
merged spec (§Invariant Resolutions).
