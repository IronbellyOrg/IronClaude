# Invariant Probe — Round 2.5 (independent fault-finder, no advocacy)

Agent: general-purpose subagent, no card allegiance, no tool access, capped at 6 findings.
Mandate: probe the emerging consensus across the 6 categories, with the findings-merge probes prioritized (unverified assumptions, dropped HIGH-value findings, mis-set severity).

## Findings

- IP-1 | count divergence | Card3-F4 was "split into two halves" yet no merged finding cites either half; D1-D9 plus MF-4/MF-5 cover the other twelve originals only. "All 13 originals mapped" is asserted, never shown. | BLOCKING for the merge
- IP-2 | state variables | A-003 flags only findings >.70, so D3, MF-4, MF-5 — each resting on unverified absence claims (missing baseline, unmentioned variable) — carry no validator flag despite being the most state-dependent findings. | NON-BLOCKING for the merge
- IP-3 | interaction effects | D1/D2 rose to .80 via cross-card corroboration; MF-4 and MF-5 converge on the same requirement (spec item 7) from two collections yet stay frozen at .70 under the no-inflation rule — corroboration policy applied inconsistently, combined severity never assessed. | NON-BLOCKING for the merge
- IP-4 | guard conditions | D3's category is unresolved, but adopted A-005 lets "other" survive only for D6/D8; advocates 1/2's advisory/other position contradicts the merge's own assumption, leaving D3's shipped category either forced or incoherent. | BLOCKING for the merge
- IP-5 | sufficiency | No non-MINOR finding exists, yet MF-5 is a shipped absence of spec-required behavior while D2, a plan-wording contradiction, carries higher confidence (.80 vs .70); uniform-MINOR calibration looks inverted between shipped and plan defects. | NON-BLOCKING for the merge
- IP-6 | collection boundaries | D9's drop-guard ("if the shipped degraded list already existed") scopes the same shipped collection as MF-5's "graph:disabled still listed"; a pre-existing list kills D9 but leaves MF-5's framing untouched — guards not cross-linked. | NON-BLOCKING for the merge

PROBE_VERDICT: merge-blocked — IP-1 and IP-4 are record-integrity defects (unshown mapping for Card3-F4's halves; D3's category contradicting adopted A-005), both cheaply fixable by stating the half destinations and recording D3's split disposition before re-issuing the merge.

## Orchestrator disposition (fixes applied before merge execution)

- IP-1 (BLOCKING): fixed — the explicit 13-to-10 provenance map now appears in debate-transcript.md and merge-log.md, naming every half's destination (C3-F3a dropped duplicate; C3-F3b into MF-3; C3-F4a into MF-8; C3-F4b becomes MF-10).
- IP-4 (BLOCKING): fixed — D3's category resolved to unpassable-check by applying the panel's own tightened A-005 rule (a real category fits, so `other` is not available); the advisory-vs-plan-defect advocate split is preserved as a recorded dissent, and severity stays MINOR / non-blocking by unanimous agreement.
- IP-2 (non-blocking): adopted — the evidence-validator flag applies to ALL merged findings, explicitly including the state-dependent MF-3, MF-4, MF-5.
- IP-3 (non-blocking): recorded, not actioned — the .70 freeze on MF-4/MF-5 was a deliberate Round-2 decision (same underlying requirement; no confidence inflation); combined severity of the item-7 pair assessed as still MINOR/non-blocking (no card claimed higher). Listed in return-contract unaddressed_invariants.
- IP-5 (non-blocking): recorded, not actioned — confidence values belong to the cards and the debate; post-hoc inversion repair is out of scope for the merge and would override scoring without documented justification. Listed in unaddressed_invariants.
- IP-6 (non-blocking): adopted — MF-10's drop-guard and MF-5 are cross-linked in the merged output (same shipped fallback collection).
