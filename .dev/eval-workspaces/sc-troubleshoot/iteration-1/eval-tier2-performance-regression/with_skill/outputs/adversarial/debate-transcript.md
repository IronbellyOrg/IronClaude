# Adversarial Debate Transcript — fix-1.md vs fix-2.md vs fix-3.md

**Mode**: compare
**Depth**: quick (proposals share diagnosis; differ in mechanism)
**Focus**: correctness, risk, test-coverage

## Round 1 — Attack each proposal

**Attack on Fix 1 (per-cardinality)**: "Reviewer cognitive load — mixing `joinedload` and `selectinload` in one statement requires the reader to know SQLAlchemy loader strategies. Fix 2's uniform `selectinload` is dumber and safer."

**Defense of Fix 1**: "The mix is idiomatic in SQLAlchemy docs — joinedload for single-row, selectinload for collections is the standard guidance. The reader cost is one comment. The runtime cost of going uniform-selectin is real per-request round-trips, which the user is *currently being paged about*."

**Attack on Fix 2 (uniform selectinload)**: "Adds two extra round-trips compared to `joinedload` for the two single-row relationships. With a busy replica, you keep N+1's cousin: 1 + 4 = 5 round-trips per request. Marginally better than 200, marginally worse than 3."

**Defense of Fix 2**: "The 5-vs-3 round-trips difference is single-digit ms; the safety/uniformity benefit compounds across future contributors. And `selectinload` is immune to Cartesian row explosion if relationships change cardinality."

**Attack on Fix 3 (loader + DTO + cache)**: "Out of scope for a regression hotfix. The user is paged about a 15x latency regression *right now*. Phase 2 introduces caching to a system that has none — cache invalidation is unsolved here, so we are trading a perf regression for a correctness regression risk."

**Defense of Fix 3**: "Phase 1 of Fix 3 *is* Fix 1 — so Fix 3 is strictly additive. Caching catches the next regression before it happens."

**Counter to defense of Fix 3**: "Strictly additive is exactly the problem — the user did not authorize architectural changes; the protocol is `--type performance` not `--type refactor`. Phase 2 belongs in a separate `/sc:improve` invocation."

## Round 2 — Cross-examine on correctness and risk

- **Correctness**: Fix 1 and Fix 2 both produce correct results. Fix 3 Phase 2 introduces cache staleness risk that Fix 1/Fix 2 do not have.
- **Risk**: Fix 1 has a small `EXPLAIN ANALYZE` validation cost. Fix 2 has none. Fix 3 Phase 2 has invalidation hooks to design and test.
- **Test coverage**: Fix 1 and Fix 2 both ship a query-count test (cheap, deterministic). Fix 3 Phase 2 needs cache-hit + cache-bust tests, doubling test surface.
- **Reversibility**: Fix 1 and Fix 2 are single-query edits, trivially reverted. Fix 3 Phase 2 introduces a new module and decorator, harder to revert cleanly.

## Round 3 — Verdict

**Winner: Fix 1 (per-cardinality loader strategy).**

Reasoning:

- Solves the symptom most directly (fewest round-trips at correct cardinality).
- Aligns with SQLAlchemy idiomatic guidance.
- Has the smallest diff and the cleanest test (query-count).
- Validation gap (EXPLAIN ANALYZE on the read replica) is a one-line follow-up the report should call out.

**Fix 2 retained as fallback**: if production validation shows row-explosion on `joinedload(last_edit).joinedload(editor)` due to a downstream relationship change, swap to uniform `selectinload`.

**Fix 3 deferred**: Phase 1 of Fix 3 is the same as Fix 1. Phase 2 (DTO + cache) is correctly scoped to a separate ticket (`/sc:improve --type architecture views/dashboard.py`) and explicitly recommended in the Next Steps.
