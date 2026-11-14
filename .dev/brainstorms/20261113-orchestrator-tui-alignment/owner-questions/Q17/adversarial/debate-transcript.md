# Adversarial Debate Transcript: Q17

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100%
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned as separate sub-agents in parallel (general-purpose agent type, current model): Variant 1 frontend, Variant 2 analyzer, Variant 3 architect
- Full statements: round1-advocate-1.md, round1-advocate-2.md, round1-advocate-3.md (this folder); summaries below are condensed from them.
- Variant mapping: variant-1 = proposal-A (yes, a sweep-facts panel in release 3), variant-2 = proposal-B (not now), variant-3 = proposal-C (never, a standing boundary)

## Round 1: Advocate Statements

### Variant 1 Advocate (frontend)
**Position**: the close-or-wait decision a person makes at the Decision Desk needs facts only the sweep has (ADJ line 240), so Variant 1 is right about the user need but wrong about timing; judged Variant 2 best overall (62%).
**Steelman of Variant 2**: costs nothing, matches the 78 percent judgement which is about "now" (ADJ line 361), keeps the verbatim-words rule (ADJ line 253) and NFR-001 untouched.
**Steelman of Variant 3**: the vocabulary collision is documented (ADJ lines 250 to 257); one screen that speaks one program's language is safest.
**Strengths claimed**: serves the real decision; turns "unavailable (no source)" cells into sourced answers; comes with UX guardrails; only variant to name the freshness gap, which is understated because the WC-16 sweep limit is "a cap, not a schedule" (ADJ line 81).
**Weaknesses identified**: Variant 2 has no reopen trigger and gives the Decision Desk designer no instruction to leave space; Variant 3 exceeds the evidence and demotes a ready UX safeguard to history.
**Concessions**: plans for an unscheduled screen (OB-09 deferred, MR line 257; Q19 not yet chosen, MR line 546); depends on unmerged PR #539 whose JSON keys are decided after merge (ADJ line 359); pulls Q9 forward; freshness risk is serious; goes against 78 percent; Q22 asks about snapshot or workspace record age, not sweep report age (MR line 549).
**Suggested merge**: Variant 2 plus a written trigger, a layout note in OB-09, and the freshness warning in the contract note.

### Variant 2 Advocate (analyzer)
**Position**: Variant 2 is the only answer whose scope matches the evidence: the spec answer and default (MR line 544), the 78 percent judgement scoped to "now" (ADJ line 361), and both sides of the source split D-6 ("eventually" and "later" are both compatible with "not now", round2-rebuttal-V5.md line 69). Judged Variant 2 best (70%).
**Steelman of Variant 1**: Decision Desk needs these facts; its transport (caller-side stdout capture) is Q9's own first step (ADJ line 779; round2-rebuttal-V5.md line 108).
**Steelman of Variant 3**: seven shared words with different meanings and incompatible JSON shapes (ADJ lines 131, 250 to 256); a written boundary prevents drift.
**Strengths claimed**: exact evidence fit; consistent with Q9, Q19 and Q22 recommendations; no dependency on unmerged work; NFR-001 untouched; a later yes is pre-wired (soft graph edge MR line 708, rule ADJ line 253).
**Weaknesses identified**: Variant 1 contradicts 78 percent with no new evidence, overrides Q9, depends on PR #539, Q9, Q22 and Q19. Variant 3 exceeds the evidence, removes a cost-free soft edge, and adds an unasked reverse constraint ("the sweep reads no observer output").
**Concessions**: no written trigger (most serious); did not raise the freshness gap; two places to look; layout rework risk.

### Variant 3 Advocate (architect)
**Position**: a boundary matching the ownership table (ADJ line 240) is the lowest-coupling design, and v2 is the natural home for a joined view (MR line 200; ADJ line 361); but the evidence supports "not now", not "never". Judged Variant 2 best (62%).
**Steelman of Variant 1**: real user need; honest costs; names the freshness gap (WC-16 cap, ADJ line 81, against the observer's 15 second reads, ADJ line 130).
**Steelman of Variant 2**: spec answer and default; costs nothing; leaves the owner-only decision open.
**Strengths claimed**: lowest coupling; removes a dependency edge; release independence; removes vocabulary mixing at the source; names a home for the joined view.
**Weaknesses identified**: Variant 1 chains two deferred items and pulls Q9 forward; Variant 2's soft edge never resolves without a trigger and does not say where a joined view lives.
**Concessions**: goes beyond the evidence; closes a door two reviews wanted open; costlier reversal; the reverse clause answers a question nobody asked; most structural benefits are also delivered by Variant 2 while "not now" lasts.

## Shared-assumption responses

| Point | Adv 1 | Adv 2 | Adv 3 |
|---|---|---|---|
| A-001 (release 3 Decision Desk will be built) | QUALIFY: deferred, Q19 undecided | QUALIFY: Q19 default is "OB-09 does not start" | QUALIFY: plausible, not scheduled |
| A-002 (sweep merges and keeps its fact set) | QUALIFY: facts stable in kind, not shape | QUALIFY: PR #539 open | QUALIFY: fact set stable, merge not certain |

No omissions. Orchestrator check of a point two advocates marked UNVERIFIED: the ADJ glossary maps V1 to review 01 and V4 to review 04 (ADJ lines 42 and 45), so "reviews 01 and 04" in the proposals is correct.

## Scoring Matrix

| Diff Point | Taxonomy | Adv 1 | Adv 2 | Adv 3 | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | none | 90% | Same five sections |
| C-001 | L2 | V2 65 | V2 65 | V2 60 | Variant 2 | 85% | Snapshot v1 now, soft edge kept (MR lines 257, 708) |
| C-002 | L3 | V2 70 | V2 70 | V3 55 | Variant 2 (2 of 3) | 70% | Keeps Q9 at its own recommendation (ADJ line 779) |
| C-003 | L2 | V2 60 | V2 60 | V2 60 | Variant 2 | 80% | The conditional rule (ADJ line 253) costs nothing to keep live |
| C-004 | L2 | V1 70 | V1 60 | V3 55 | Variant 1 (2 of 3) | 65% | One screen serves the person's decision; V3 named v2 as home |
| C-005 | L3 | V1 85 | V1 85 | V1 80 | Variant 1 | 90% | Only V1 names the freshness gap; confirmed by the WC-16 cap |
| X-001 | L2 | V2 60 | V2 65 | V2 60 | Variant 2 | 80% | Matches spec answer and both sides of D-6 |
| X-002 | L2 | V2 75 | V2 80 | V2 80 | Variant 2 | 90% | Same scope as the 78 percent judgement; V3 advocate conceded |
| X-003 | L3 | V2 80 | V2 80 | V2 80 | Variant 2 | 90% | Nothing built or written as a rule; cheapest reversal |
| U-001 | L2 | V1 85 | V1 85 | V1 75 | Variant 1 | 90% | Staleness gap is real and relevant to any later panel |
| U-002 | L2 | V2 70 | V2 60 | V2 60 | Variant 2 | 80% | Names its drift risk; fixed by a trigger |
| U-003 | L2 | V3 65 | V3 75 | V3 70 | Variant 3 | 80% | Clearest separation statement |
| A-001 | L3 | V2 65 | V2 70 | V2 65 | Variant 2 | 85% | Least commitment wins while release 3 is unscheduled |
| A-002 | L3 | V2 70 | V2 75 | V2 65 | Variant 2 | 85% | Only V2 is indifferent to how PR #539 lands |

## Convergence Assessment
- Points in denominator (S + C + X + A): 11. Agreed: 11 (9 unanimous, C-002 and C-004 by 2 of 3).
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 1, L2 5, L3 5 (all covered; no forced round)
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Overall verdicts: all three advocates judged Variant 2 best (62%, 70%, 62%); 3 of 3.
- Status: CONVERGED
- Unresolved points: none
