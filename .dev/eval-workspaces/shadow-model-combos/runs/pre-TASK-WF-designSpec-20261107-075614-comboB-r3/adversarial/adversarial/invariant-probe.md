# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (opus class, independent of the advocates)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The fold's cycle_id names the cycle that holds the guard, so held_cycle_published checks the right push | UNADDRESSED | MEDIUM (fault-finder: HIGH; adjudicated down, see Adjudication) | source.md:190 lists cycle_id as a fold field; source.md:194-206 has no row that sets it; source.md:139 engage row 7 returns NOOP(already_held) for a second cycle while HELD; source.md:108 held_cycle_published takes no cycle argument; plan 60, 62, 77, 166 do not cover a two-cycle log |
| INV-002 | guard_conditions | release_decision never readies a PR whose draft state the guard did not prove it set | UNADDRESSED | LOW (fault-finder: HIGH; adjudicated down) | source.md:150 row 2 admits RELEASE_PENDING with no ownership test; source.md:199 settled(draft, failed) leaves owned_draft false; flows are guarded by source.md:138, 170 and the halt at source.md:68; plan 75 covers DISABLED only |
| INV-003 | state_variables | A foreign toggle folded into DISABLED makes guard_status report user_override | UNADDRESSED | MEDIUM | source.md:112 needs "DISABLED with cause user_override"; source.md:206 fold row sets only phase and owned_draft; only source.md:200 sets disabled_cause; plan 60-61 do not run fold then guard_status on a foreign-toggle log |
| INV-004 | guard_conditions | An engage halt reports merge_guard: unavailable | UNADDRESSED | MEDIUM | source.md:112 says a draft_guard_unavailable halt reports unavailable but guard_status (source.md:110) has no halt input; engage rows 3 and 8 (source.md:135, 140) halt before any request so the guard is None and maps to released; plan 61 enshrines "no record at ordinal 3 (released)" |
| INV-005 | interaction_effects | A zero-edit release cannot drop a hold caused by an earlier unconfirmed cycle | UNADDRESSED | MEDIUM | source.md:155 row 7 (applied_edits == 0) precedes the head check at source.md:156; applied_edits is per cycle (source.md:107); plan 75 asserts the release without requiring the earlier cycle to be published |
| INV-006 | sufficiency_challenge | The plan's criteria alone catch a wrong ordering in the protocol prose | UNADDRESSED | MEDIUM | plan 166, 170, 172 run against a test-author driver; ref criteria are phrase presence (plan 128-129); only the SKILL.md Wave 6 bullet gets an order check (plan 153) |
| INV-007 | count_divergence | The RECONCILE count rule matches the classify_toggles ledger | UNADDRESSED | LOW | source.md:127, 202 failed-but-landed then retry leaves observed = run_toggles + 1; source.md:165 requires observed == run_toggles + 1 with no slack, so later reconciles fall to ambiguous (fails safe); plan 76 tests reasons in isolation |
| INV-008 | collection_boundaries | next_cycle_number compares numbers, not text | UNADDRESSED | LOW | source.md:102 "highest"; plan 59 tests only fix-1 and fix-2; unlikely under the round cap |

## Adjudication of the two HIGH items (forced verification round, sonnet class)
- INV-001: each step of the chain is licensed by the spec text only because the effect table has no cycle_id row (source.md:194-206); the exposure needs a held release, a later cycle and a crash before that cycle's push; the release happens in Wave 0 before any edit and the remote content is what the PR already had. Verdict: reachable under conditions, MEDIUM, not caught by plan 60, 62, 77, 166.
- INV-002: a function-level gap only. Engage rows 5-6 (source.md:137-138), resume rows 7-8 (source.md:169-170) and the halt (source.md:68, 274) keep release_decision from being called in that state; the remaining route needs a SKILL that continues after an engage HOLD, which the spec never says. Verdict: LOW (MEDIUM if the SKILL proceeds after an engage HOLD).
- After adjudication no HIGH UNADDRESSED item remains; the MEDIUM items are logged as warnings and do not block convergence.

## Summary

- **Total findings**: 8
- **ADDRESSED**: 0
- **UNADDRESSED**: 8
  - HIGH: 0 (2 reported HIGH by the fault-finder, adjudicated to MEDIUM and LOW)
  - MEDIUM: 5
  - LOW: 3
