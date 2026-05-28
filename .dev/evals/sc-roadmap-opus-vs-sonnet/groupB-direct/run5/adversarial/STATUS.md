# sc:adversarial run5 — SUCCESS (full pipeline)

**Status:** `success` · **Stage:** all 5 steps complete · **Invocation:** `skill-direct`
**Base:** Variant 1 (opus) — selected with 8.14% margin
**Convergence (debate end):** BLOCKED_BY_INVARIANTS (9 HIGH UNADDRESSED) → resolved by merge

## Pipeline run summary

| Step | Status | Artifact |
|------|--------|----------|
| Prerequisites | PASS | Output path under `.dev/` (not forbidden); source file exists (62KB / 1229 lines) |
| Mode B variant generation | 2/2 produced | `variant-1-opus-default.md` (792L), `variant-2-sonnet-default.md` (854L) |
| Step 1 — Diff analysis | DONE | 98 diff points: 20 S + 30 C + 8 X + 28 U + 12 A (6 promoted) |
| Step 2 — Debate R1 (parallel) | DONE | 2 advocate statements; opus R1 needed 1 retry (analysis ok, file write missed; retry succeeded) |
| Step 2 — Debate R2 (sequential) | DONE | 2 rebuttals; 7 V2 concessions + 8 V1 concessions = strong cross-concession |
| Step 2 — Round 2.5 invariant probe | DONE | 26 findings; 9 HIGH UNADDRESSED → convergence BLOCKED per AD-1 |
| Step 2 — Convergence gate | BLOCKED_BY_INVARIANTS | Taxonomy: all 3 levels covered; invariant gate: 9 HIGH UNADDRESSED |
| Step 3 — Hybrid scoring | DONE | V1=0.9075, V2=0.8261, margin 8.14%; V2 ineligible (0/5 edge-case floor) |
| Step 4 — Refactor plan | DONE | 26 changes: 9 invariant fixes + 12 V2 incorporations + 5 base-weakness fixes |
| Step 5 — Merge execution | DONE | 1034 lines; 26/26 applied; validation PASS; 0 new contradictions |
| Post-merge | All 9 HIGH invariants resolved | `unaddressed_invariants: []` in return contract |

## Why status = `success` despite BLOCKED_BY_INVARIANTS at debate end

Per the protocol, the invariant-probe gate (AD-1) BLOCKS convergence at the debate stage when HIGH-severity UNADDRESSED items exist. At Round 2.5 close, 9 such items remained:

- INV-001 (family lineage durability), INV-005 (audit_log NULL user_id), INV-006 (enumeration-timing + audit-write interaction), INV-013 (token eviction vs family-revocation race), INV-017 (login-path transaction ordering), INV-021 (in-process email retry vs 200ms p95), INV-022 (SOC2 immutability sufficiency), INV-023 (lockout-only brute-force sufficiency), INV-026 (bcrypt cost-12 vs NFR-PERF-001).

The refactor plan (Step 4) flagged each as a mandatory Fix #1-9 with concrete remediation. The merge (Step 5) applied all nine. Post-merge validation (structural integrity, internal references, contradiction rescan) PASSED. Return contract `unaddressed_invariants: []` reflects the post-merge state.

The `convergence_score: 0.543` field reports the spec-formula debate-end score (38 agreed / 70 total diff points) without retroactive credit for merge resolutions, per the field's contract definition.

## Key debate outcomes

**Top consensus points (both advocates conceded in R2):**

- 12-week timeline (6 sprints × 2 weeks) — V1's PRD arithmetic wins (V2 conceded C-001/C-002)
- Audit infrastructure in M1 (SOC2 day-1) — V1 wins (V2 conceded C-004)
- Account lockout in M1 — V2 wins (V1 conceded C-003)
- Async email: V1's in-process retry for v1.0; defer V2's Bull/BullMQ to v1.1+ (split decision on C-020)
- State machines from V1 (V2 conceded)
- Beta buffer + post-GA structure from V2 (V1 conceded)
- 10-row staffing table, feature-flag lifecycle, admin audit query, refresh-token cap from V2 (V1 conceded)

**Top scoring drivers (Variant 1 selected as base):**

- Full FR/NFR coverage on both variants (RC=1.00 each)
- V1 advantage on Section Coverage (19 vs 16 H2 sections)
- V1 advantage on Internal Consistency (no V1 equivalent to V2's pre-concession 22-week self-contradiction)
- V1 alone meets the 1/5 Edge-Case Floor (Dimension 6) via its §8 boundary conditions table and §9 state machines — V2 omits both
- Margin 8.14% > 5% tiebreaker threshold; no tiebreaker invoked

## Artifacts written

All 12 required artifacts present in `adversarial/`:

- `variant-1-opus-default.md`, `variant-2-sonnet-default.md`
- `diff-analysis.md`, `round-1-advocate-{1,2}.md`, `round-2-rebuttal-{1,2}.md`, `invariant-probe.md`, `debate-transcript.md`
- `base-selection.md`, `refactor-plan.md`, `merge-log.md`
- `return-contract.yaml`, `STATUS.md`

Final merged output: `merged-roadmap-user-auth.md` (1034 lines, in `run5/` parent — not under `adversarial/`).

## Notes for the eval harness

- Source file was present this run (62KB on disk); run4's failure mode (missing source) is no longer reproduced.
- One retry occurred in Round 1 (opus advocate analysis succeeded but file write missed); per protocol error-handling matrix this was a single retry, not a failure path. Round-1-advocate-1.md is the retry output.
- The protocol's invariant-probe gate did its job: 9 HIGH items that would otherwise have produced a falsely-confident merged roadmap were surfaced and remediated. Comparing this run to run1/run2 (which the prior session reported as `rc=0`) may reveal whether earlier runs caught these same invariants or merged through them.
