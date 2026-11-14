# Base selection

Date: 2026-11-14. Step: base selection after a two-round debate (sc-adversarial-protocol, Mode A, 3 variants, convergence 1.0000, 50 of 50 points agreed). Sources: `debate/tally-round2.md`, `debate/tally-round2.json`, `diff-analysis.md`, `invariant-probe.md`, the three round-2 files.

## Decision

**Base = Variant A** (`variant-1-original.md`, proposal A, "layered model-policy hook", sonnet). The merged design keeps A's section order, its layer table, its event table and its failure-path machinery, and takes the debate winners from B and C into the places listed in `refactor-plan.md`.

## Counts

Two different numbers exist, so both are shown. The tally header "Own-variant picks" (`tally.py` line 88) counts how often each advocate voted for its own variant, including votes that lost. Counting the agreed winner per point gives a different split.

| Measure | A | B | C | Other |
|---|---|---|---|---|
| Own-variant picks (tally header) | 22 | 14 | 11 | n/a |
| Agreed winners, all 50 points (recounted from `tally-round2.md`) | 22 | 13 | 10 | 1 NONE (C-025); 4 shared-assumption verdicts: 3 QUALIFY, 1 REJECT |
| Structural points S-001..S-006 (6) | 2 | 3 | 1 | |
| Content points C-001..C-026 (26) | 11 | 7 | 7 | 1 NONE |
| Contradiction points X-001..X-014 (14) | 9 | 3 | 2 | |
| L3 points, state mechanics (18) | 11 | 3 | 2 | 2 verdicts (A-001 QUALIFY, A-002 REJECT) |

A wins 22 on both measures. B and C are one point lower on the winner count than on the picks count (13 versus 14, 10 versus 11) because a pick for the own variant sometimes lost the vote.

L3 points decide fail-open versus fail-closed, which is the property the incident needs. A wins 11 of 18. A's wins are C-008, C-010, C-013, C-014, X-002, X-004, X-005, X-007, X-011, X-013, X-014. B wins C-011, X-001, X-009. C wins C-009, C-019.

## Coverage of the eight questions

| Question | A | B | C | Merge takes |
|---|---|---|---|---|
| 1 Events and visibility | 16 rows; rows 10-11 hedge on `/model` | 16 rows with a plain "Cannot see" label (S-002 winner) | 9 rows, folded | A's table shape, B's plain "cannot see" wording |
| 2 Policy | Full example, narrow-only layers, six-step canonical rule | Full example, simplest per-event table (X-001 winner) | Full example, role tiers, managed layer | C's tiers and exact ids, A's stages, B's missing-policy rule |
| 3 Jev versus code | Honest conclusion; dormant Jev path (rejected) | Honest conclusion; three residue classes; no Jev code (won) | Honest conclusion; shadow call (rejected) | B's structure, A's promotion gate |
| 4 Rejection and override | Event id, append log, 2 h grants | Chain journal (not kept) | One file per grant, typed yes | A's message and limits, C's grant file |
| 5 Bypass resistance | Widest table, flat pass 2 | Tokenizer, one level | Ceilings softened by a mention rule (dropped) | A's table |
| 6 Time cost | Estimates, one 5 s registration | Registration split by cost (won) | Estimates, 5 s | B's split, A's rows |
| 7 Test plan and REQ | 35 REQ, mixed method wording | 36 REQ, fixed method set (won) | 40 REQ, nearly all unit | B's method set, union of surviving REQ |
| 8 Implementation plan | Layout and seed name correct | Seed name wrong | Best rollout | A's layout, C's rollout |

## Why A

1. Most wins (22 of 50) and the most wins at level L3.
2. It is the only variant whose headline states the v1 property and each layer's blind spot first (S-001), ends as a design rather than a chat trailer (S-006), and names the seed file in the repo's own pattern (X-006; `install_hooks.py:104-105`, verified in Step 1).
3. Its failure-path design won every contested fail-closed point: pure-bash prefilter (C-013, X-002), self-timeout converted to exit 2 (X-011), flat second pass for nested launches (X-004), oversize block (X-005), widest tamper class (C-014), narrow-only stage prefix (X-013).
4. It conceded the points it lost in round 2 (dormant Jev path, closed-world rule, allow on unknown session model, 200-line grant tail, layers L0 and L3 without a requirement or file). The named winners replace those, so no conceded A weakness survives into the merge.

## What A does not supply

A loses 28 points. They come from B (launcher helper, REQ method set, Agent resolution order, `/model` re-record, missing-policy block, no Jev code, registration split) and from C (role tiers, exact ids, single-assignment resolver, per-class modes, rollout, one-file grants, typed yes, timing test, managed layer).

A names the native floor (L0) and the detective check (L3) in its headline but has no requirement or file for either. The tally for C-025 is NONE, and C-001 (A) says to merge L3 in. The merge adds a requirement and a file for both (see `merge-log.md`).

## Why not B or C as the base

- B is strongest on launcher closure. It has no pure-bash fail-closed prefilter, no rule for a missing `jq`, a matcher that omits NotebookEdit, a seed name that breaks the repo pattern and a status-table trailer. Using B as the base would mean rewriting its failure path.
- C is the best operated. Its fail-closed branch covers no session today (`SC_STAGE` appears 0 times in `src/`, verified by advocate C), its tamper rule needs tools its matcher omits, and it copies the fail-open precedent. Using C as the base would mean rewriting its safety layer.
