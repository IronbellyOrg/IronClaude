# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 1 parallel). Round 2 skipped: depth=quick. Round 2.5 (invariant probe) skipped: --depth quick. Round 3 skipped: depth=quick.
- Convergence achieved: 100% (15/15 diff points), status CONVERGED
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (V1 option A: default:analyzer; V2 option B: default:performance; V3 option C: default:architect)
- Full advocate statements: `round1-advocate-v1.md`, `round1-advocate-v2.md`, `round1-advocate-v3.md` (this folder)

## Taxonomy tags

| Level | Points | Count |
|---|---|---|
| L1 surface | S-001 | 1 |
| L2 structural | C-001, C-003, C-004, C-006, C-007 | 5 |
| L3 state mechanics (threshold, guard, validation, boundary) | C-002, C-005, C-008, C-009, X-001, X-002, A-001, A-002, A-003 | 9 |

All three levels are covered after Round 1, so no forced round was triggered.

## Round 1: Advocate Statements

### Variant 1 Advocate (option A, default:analyzer)
**Position**: The stdio byte harness must be the always-run core: it is deterministic, runs under the sandbox rules and is the X-25 proof the spec already requires (`phase-2-codegraph-install-spec.md:97`). Its single 6,000 B cut-off is not good enough on the measured data, so the merge needs three bands.

**Steelman of V2**: The threshold is in session tokens and only a real session counts them, including Claude Code's own wrapping; `--strict-mcp-config` isolation is the best isolation idea in the set.

**Steelman of V3**: The only variant that never blocks the unattended executor and still uses the real number when it exists; its "session measurement: not run" line keeps the evidence honest.

**Key strengths claimed**: runs with no human and no login (`variant-1-original.md:6`, `context.md:10-11`); is the spec's X-25 proof; measures the 7-tool run directly instead of deriving it; counts instructions bytes; a server-side byte count cannot be shrunk by client-side deferral, so it is an upper bound.

**Weaknesses identified**: V2 has an unguarded false pass if tools are deferred (X-002), stops without auth, touches the real HOME, has no noise rule; V3's cross-check cannot fire on the measured data (X-001) and inherits V2's gaps.

**Concessions**: V1's gate fails the measured +7,004 to 7,488 B and would set `status` on an unmeasured conversion constant; "conservative" was not grounded; V1 cannot see Claude Code's wrapping or answer the deferral question.

**Shared assumptions**: A-001 REJECT; A-002 QUALIFY; A-003 QUALIFY.

### Variant 2 Advocate (option B, default:performance)
**Position**: The measured delta straddles 2K, so only the real token count can decide inside the uncertain band; V1's harness should always run as pre-screen and X-25 proof, and V2's measurement should decide in both directions inside the band, with guards that make a deferred-tools false pass impossible.

**Steelman of V1**: Strongest on everything except fidelity: deterministic, free, unattended, the only X-25 proof; a V1 pass is trustworthy.

**Steelman of V3**: Recognises that each leg covers the other's blind spot, never blocks, and forces an honest evidence line.

**Key strengths claimed**: measures the quantity the threshold is written in (`phase-2-codegraph-install-spec.md:94`); captures prefixes, wrapping and instructions as sent; the only method that can observe deferral (P3 §9.1, `P3-access-model-merged.md:155`); clean isolation (U-003); never runs `claude mcp add`, and the spec already accepts session rewrites outside `.mcpServers`; small one-time cost.

**Weaknesses identified**: V1 fails this data on the heuristic; V1 cannot see wrapping or deferral; V3's one-way rule never fires (X-001) and bakes V1's error into the decider; nobody has a noise or validity rule.

**Concessions**: needs auth (UNVERIFIED that the executor has it); real HOME side effects; UNVERIFIED `usage` fields and `alwaysLoad` behaviour under `--strict-mcp-config`; no X-25 proof; the false pass (X-002) is V2's most serious flaw; noise; isolation is not the P3 INV-015 condition.

**Shared assumptions**: A-001 REJECT; A-002 QUALIFY; A-003 QUALIFY.

### Variant 3 Advocate (option C, default:architect)
**Position**: V3's two-leg shape is right (byte harness always, session measurement layered on top), but its disagreement rule is wrong: it is one-directional and can never fire on the measured delta (X-001). Keep the shape, replace the single cut-off with three bands.

**Steelman of V1**: Simplest method meeting every hard rule; its error direction is fail-safe because `status` still keeps explore blocked.

**Steelman of V2**: Measures the real quantity with the real tokenizer and wrapping; U-003 isolation; the only variant that can observe deferral.

**Key strengths claimed**: never blocks T2 (`context.md:10-11`), which would stall later Phase 2 tasks and Phase 3 G3; the stdio harness is mandatory in every variant anyway; records both numbers for the user to confirm the proposed threshold; safe failure direction; previews Phase 3 G5 early.

**Weaknesses identified**: V1 lets one guessed constant decide a whole Phase 3 access-model change; V1 records no deferral; V2 stops the executor, has no validity guard, no noise rule, no X-25 proof.

**Concessions**: X-001 is a real flaw; V3 inherits V2's open gaps; the method is defined by reference (S-001); more text and two scripts are justified only if the second leg can change the outcome; "when a logged-in `claude` is available" is not a mechanical condition.

**Shared assumptions**: A-001 REJECT; A-002 QUALIFY; A-003 QUALIFY.

### Omission check
All three advocates answered A-001, A-002 and A-003. No `[OMISSION]` flags.

### Round 2, Round 2.5, Round 3
Not run (depth quick).

## Scoring Matrix

Positions are taken from each advocate's `## Per-Point Positions` table. "Winner" names a variant when a majority named that variant's own approach; "merge" when a majority agreed on a rule none of the three variants contained.

| Diff Point | V1 says | V2 says | V3 says | Winner | Confidence | Evidence Summary |
|------------|---------|---------|---------|--------|------------|------------------|
| S-001 | V1 | merge (self-contained text + V3 precedence) | merge (V3 structure written self-contained) | merge | 80% | All want a self-contained method an unattended executor can run; V3's reference-only form loses. |
| C-001 | merge | merge | merge | merge | 95% | Unanimous: bytes always measured and recorded; session tokens decide only inside an undecided band. |
| C-002 | merge (6,000 / 8,000 B) | merge (6,000 / 10,000 B) | merge (5,000 / 8,000 B) | merge | 85% | Unanimous on three bands; edges split (sub-points N-001, N-002). |
| C-003 | V1 | merge = V3's shape | V3 | V3 | 75% | V2's merge (A in sandbox always, B with real login and the `.mcpServers` hash guard) is V3's approach; V1 dissents for sandbox-only. |
| C-004 | V1 | V1 | V1 | V1 | 95% | Unanimous: only V1's stdio client proves explore hidden and blocked (`phase-2-codegraph-install-spec.md:97`). |
| C-005 | merge | merge | merge | merge | 95% | Unanimous: the real measurement decides in both directions inside the band; V3's one-way rule rejected. |
| C-006 | merge = V3 never-block + logged item | merge (never block, `status`, "not run") | V3 | V3 | 85% | All three adopt V3's never-block rule plus a logged item; nobody keeps V2's stop. |
| C-007 | V1 | V2 | V1 | V1 | 70% | Majority: count instructions bytes explicitly from a real 7-tool run, since the instructions may change when explore is hidden. |
| C-008 | V1 + noise rule | merge (ABAB, twice, within 50 tokens) | merge (three runs, median, within 200) | merge | 75% | Unanimous that a repeat-and-tolerance rule is needed; details split (N-004). |
| C-009 | merge (floor D/5) | merge (inventory + floor D/5) | merge (inventory + floor D/6) | merge | 85% | Unanimous validity guard; floor majority D/5 (N-005); inventory check from V2 and V3. |
| X-001 | V1 | V1 | merge (V3 loses) | V1 | 90% | V3 conceded; V1's self-assessment of its false-fail direction was correct. |
| X-002 | V1 | merge (guards, fail closed) | merge (guard + deferral record) | merge | 85% | B counts only after validity guards; failing a guard makes B invalid, never a pass. |
| A-001 | merge (band) | V2 | merge (band) | merge | 90% | All REJECT the assumption; the undecided band is the fix. |
| A-002 | V1 + deferral record | V2 + guard | merge | merge | 85% | All QUALIFY: the gate assumes full load (upper bound); B must observe listing and is invalid if tools are deferred. |
| A-003 | merge (binary, per-tool bytes) | merge (binary, per-tool bytes) | binary kept + per-tool bytes | merge | 90% | All QUALIFY: keep the binary outcome fixed by P3-D1; record per-tool bytes as data only. |

Points won by a variant's own approach: V1 3 (C-004, C-007, X-001); V3 2 (C-003, C-006); V2 0. Ten points went to merged rules.

## Sub-points decided by the orchestrator

Each was settled by majority of the advocate proposals; where there was no majority the orchestrator chose and records why. All are flagged for review.

| # | Sub-point | V1 | V2 | V3 | Decision | Basis |
|---|---|---|---|---|---|---|
| N-001 | Lower band edge (clear pass) | D <= 6,000 B | D <= 6,000 B | D <= 5,000 B | **D <= 6,000 B** | Majority; 6,000 B is 2,000 tokens at 3 B/token. |
| N-002 | Upper band edge (clear fail) | D > 8,000 B | D > 10,000 B | D >= 8,000 B | **D > 8,000 B** | Majority on 8,000; 8,000 B is 2,000 tokens at 4 B/token. |
| N-003 | Byte basis for D | full objects + instructions | model-facing fields | full objects + instructions | **full `tools` objects + instructions** (model-facing recorded too) | Majority; the larger figure is the upper bound. |
| N-004 | Session noise rule | each config twice, T = max(7-tool) - min(default) | ABAB order, twice each, within 50 tokens, one re-run | three each, median, spread <= 200 | **ABAB order, each config twice; the two runs of a config must agree within 50 tokens (one re-run of the set allowed, else B invalid); T = max(7-tool runs) - min(default runs)** | Majority on "twice"; orchestrator took V2's 50-token tolerance (identical prompts give near-identical counts, and 200 tokens is 10% of the threshold) and V1's conservative T. |
| N-005 | Validity floor | T >= D / 5 | T >= D / 5 | T >= D / 6 | **T >= D / 5** | Majority. |
| N-006 | X-25 assertion fails | step 0 fails | step 0 fails outright | stop, mid-level decision | **stop, no value selected, mid-level decision (§7)** | Unanimous in substance; V3's reason: the `status` branch also depends on the explicit list hiding explore. |
| N-007 | Session leg outside the band | optional; a valid T > 2,000 can still fail a byte pass | optional, recorded only | not run | **runs only inside the band** | Majority (V2, V3). |

## Convergence Assessment

- Points resolved: 15 of 15 (S 1 + C 9 + X 2 + A 3)
- Alignment: 100%
- Threshold: 80%
- Taxonomy gate: L1, L2 and L3 all covered
- Invariant gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: none. Seven sub-points (N-001 to N-007) were settled by majority or by the orchestrator and are flagged for review.
