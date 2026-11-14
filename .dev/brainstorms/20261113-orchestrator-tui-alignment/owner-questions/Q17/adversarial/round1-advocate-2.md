# Round 1 advocate statement: Variant 2 (proposal B, "not now; ask again later")

Persona: analyzer (evidence quality, logical consistency). Debate: Q17, Mode A, depth quick, Round 1.

Source shorthand used below (all lines confirmed by reading the file on 2026-11-14):
- MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`
- ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`
- R2V5 = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V5.md`

## Position summary

Variant 2 answers "no sweep-facts panel now; a later yes makes Q9 a real requirement at that time". It is the only answer whose scope matches the evidence exactly:

1. It is word for word the spec's recommended answer and the default if unanswered: MR line 544 reads "No, not now; if yes later, Q9 becomes a real requirement" with default "ADJ recommendation applies"; ADJ line 787 gives the same recommendation.
2. The strongest judgement in the record, ADJ line 361 (A-001, 78 percent), is scoped to "now": "Q17: no observer panel for sweep facts now". Variant 1 contradicts it; Variant 3 stretches it from "now" to "ever". Variant 2 neither contradicts nor stretches it.
3. The source disagreement D-6 (R2V5 line 69) is "V1 and V4 (eventually, for facts only the sweep has) vs V5 (optional, later, only if wanted)", and the settling fact is "The owner only." Both sides of D-6 agree on "not now": "eventually" and "later" are both compatible with "not now". Variant 2 is the only answer that contradicts neither side. Variant 1 overrides V5's "only if wanted"; Variant 3 overrides V1 and V4's "eventually".
4. Every precondition Variant 1 needs is open today: the sweep is in PR #539, still open (ADJ line 78); the sweep JSON is "printed to stdout only" (ADJ line 131, E-05); Q9's own recommendation is "Not now" (ADJ line 779; MR line 536); Q22 (what age is stale) has "no debate recommendation" (MR line 549); and Q19's default is "PLAN INFERENCE: OB-09 does not start" (MR line 546). Deciding the panel's content before its host release is scheduled is deciding ahead of the evidence.
5. It is the cheapest to reverse in either direction (X-003): nothing is built, NFR-001 and its two pinned tests stay (ADJ line 83), and the conditional rule "if a panel ever shows sweep rows it prints the sweep's words verbatim and labels the report age" already exists in the mapping table (ADJ line 253, the "could not determine" row), so a later yes has its rule waiting.

## Steelman of Variant 1

Strongest version: the observer's release 3 is called "Decision Desk", and a person deciding what to do about a worker needs exactly the facts the observer cannot collect. ADJ line 240 shows the observer owns none of "Git, contracts, transcripts, `safe_to_close`, frozen plans, Task specs"; the sweep owns all of them. A Decision Desk that shows Orca state alone forces the person to cross-read two outputs, which is the very friction a dashboard exists to remove. V1 and V4 in the source debate wanted this "eventually, for facts only the sweep has" (R2V5 line 69). Variant 1 also does not ask for anything extreme: its first transport is caller-side stdout capture, which is Q9's own recommended first step (ADJ line 779), and the first possible exchange named in R2V5 line 108 is exactly "caller-captured sweep stdout in the WC-16 pass". Deciding now lets Decision Desk be designed once with its real content instead of being reworked later.

What it genuinely gets right: it is the only variant that names the freshness gap (U-001, C-005), and that gap is real and confirmed. The coordinator runs `/sc:sweep` "at most once every 5 minutes" (MR line 180, WC-16; MR line 1021), while the observer refreshes on a 15 second clock (MR line 422). Sweep facts on a live screen will always be older than the Orca rows beside them. It is also candid that it goes against the 78 percent judgement (variant 1, "What it costs or risks").

Critique with counter-evidence:
- It contradicts the one quantified judgement on this exact point (ADJ line 361, 78 percent) without offering new evidence that was unavailable to that debate. Every fact Variant 1 cites (ADJ lines 240, 253, 779; R2V5 line 69) was already in front of that debate.
- It pulls Q9 forward against Q9's own recommendation ("Not now", ADJ line 779), so one owner answer silently overrides another recommended answer.
- It hangs release 3 on an unmerged producer (PR #539 open, ADJ line 78) and on two unanswered questions it lists as unresolved itself (Q9 and Q22). Q22 has no debate recommendation at all (MR line 549), so the panel's hide-after age has no basis yet.
- Its own strongest risk (the freshness gap) argues for waiting until Q22 has a number, not for committing now.
- It assumes release 3 will be Decision Desk. Q19 (MR line 546) recommends "Fleet Quilt or Decision Desk first", so Decision Desk is not even the settled first ask.

## Steelman of Variant 3

Strongest version: the two programs use the same words with different meanings. The mapping table (ADJ lines 250 to 256) lists seven shared words, and for several of them the meanings are not just different but easy to confuse on one screen: "stale" is a 45 second feed gap in the observer and a 6 hour transcript window in the sweep; "unknown" is the string `UNKNOWN` in one and `null` in the other; "historical" is an Orca terminal state in one and an age window in the other. The JSON formats also differ in casing, null handling and row keys (ADJ line 131). A standing boundary (two collectors, two contracts, no reader crossing) removes this whole class of misreading permanently, lets observer planning never wait on the sweep, and stops reviewers reopening the question by default (U-003). A soft "not now" that drifts is a real failure mode, and a written boundary prevents drift by making the answer explicit.

What it genuinely gets right: the vocabulary-mix risk is the most concrete correctness hazard in the record, and it is honest that it "Goes further than the debate: its 78 percent judgement was about 'now', not 'ever'" (variant 3 line 25).

Critique with counter-evidence:
- By its own admission it exceeds the evidence. ADJ line 361 says "now"; MR line 544 says "not now"; R2V5 line 69 records two reviews wanting it "eventually". No source in the record supports "never".
- The risk it removes is already mitigated by a written rule: ADJ line 253 requires any future panel to print the sweep's words verbatim and label the report age, and other rows require labelling "which program's meaning" (the "historical" row) and "say 'feed stale' or 'session stale'" (the "stale" row). The boundary removes a risk that a cheaper rule already governs.
- It removes the SW-11 to OB-09 edge (MR line 708, graph row 61, marked SOFT, "Only if Q17 = yes"). That edge costs nothing while inactive, so removing it buys nothing and costs a reversal step later.
- Its added clause "the sweep reads no observer output" widens Q17 beyond its question, which asks only about the observer reading sweep facts (ADJ line 787). I found no row in the cited sources asking for that reverse constraint; whether any other spec row needs it is UNVERIFIED.
- Reversing a written boundary is harder than answering a deferred question (X-003), and it closes the door V1 and V4 asked to keep open (R2V5 line 69).

## Strengths claimed

1. Exact evidence fit: matches MR line 544, ADJ line 787 and ADJ line 361 in scope ("now"), with no stretch.
2. Logical consistency with the source split: compatible with both sides of D-6 (R2V5 line 69), the only answer that is.
3. Consistency with the other owner answers' recommendations: leaves Q9 at "Not now" (ADJ line 779; MR line 536), does not presuppose a Q22 number (MR line 549), and does not presuppose a Q19 choice (MR line 546).
4. No dependency on unmerged or unbuilt work: release 3 can be planned against observe snapshot v1 alone, with no wait on PR #539 (ADJ line 78) or on persistence.
5. NFR-001 and its two pinned tests stay untouched (ADJ line 83).
6. A later yes is cheap: the graph keeps the soft edge (MR line 708) and the verbatim-words rule already exists (ADJ line 253), so the reversal path is pre-wired.

## Weaknesses identified in others

Variant 1:
- Contradicts the 78 percent judgement (ADJ line 361) with no new evidence.
- Forces Q9 ahead of its own recommendation (ADJ line 779).
- Depends on PR #539 (open), Q9 and Q22 (no recommendation, MR line 549), and on Q19 choosing Decision Desk (MR line 546 offers Fleet Quilt or Decision Desk).
- Its own freshness evidence (5 minute sweep cap, MR line 180; 15 second observer clock, MR line 422) argues for delay.
- Minor evidence point shared by all three variants: they say "reviews 01 and 04"; the source text at R2V5 line 69 says "V1 and V4". The mapping of V1 and V4 to reviews 01 and 04 is plausible but UNVERIFIED in this round.

Variant 3:
- Exceeds the evidence ("ever" versus "now"), as it concedes.
- Removes a cost-free soft edge and adds an unrequested reverse constraint.
- The hazard it targets is already governed by ADJ line 253 and the mapping table rules.

## Concessions

1. Variant 2 has no written trigger (U-002, its own text: "'Not now' has no trigger written down; it may drift into 'never' without a decision"). This is its most serious weakness and Variant 3's critique of drift lands. A fix within Variant 2's scope: record a re-ask trigger in the ledger, for example "re-ask Q17 when Q19 is answered and OB-09 is scheduled". This is my proposal, not a spec fact.
2. Variant 2 did not raise the freshness gap (C-005). Variant 1 is better on that point, and Variant 2 should carry it into the XC-05 note as a recorded constraint for any later yes.
3. Variant 2 leaves a person two places to look (C-004). Variant 1 is better for that user need.
4. If Decision Desk is designed first without sweep facts, adding them later may mean layout rework (variant 2's own risk list). This cost is real but unquantified; it is lower if the trigger above fires before Decision Desk's layout is fixed.
5. Variant 3's vocabulary-risk argument is stronger than Variant 2's text acknowledges; Variant 2 relies on ADJ line 253 without saying so explicitly in its risk section.

## Shared assumptions

- A-001 (release 3 Decision Desk will be built, so the question has a real consumer): QUALIFY. The record does not support it as a given. Q19's default if unanswered is "PLAN INFERENCE: OB-09 does not start" (MR line 546), and Q19's recommendation names "Fleet Quilt or Decision Desk first", so Decision Desk is not certain to be first. Under this uncertainty, the answer that commits nothing (Variant 2) loses least: a yes builds for a consumer that may not come, and a never forbids something for a consumer that may never ask.
- A-002 (the sweep merges and keeps its current fact set): QUALIFY. The fact set is documented (ADJ line 240: git, contracts, transcripts, `safe_to_close`, frozen plans, Task specs owned by the sweep), but PR #539 is still open (ADJ line 78), so merge and final shape are not settled. A yes depends on it; a never presumes it matters enough to forbid; a not-now is indifferent to it.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | None (tie) | 90% | All three use the same five sections. |
| C-001 | Variant 2 | 65% | Snapshot v1 now with the soft edge kept matches MR lines 257 and 708 without removing or activating anything. |
| C-002 | Variant 2 | 70% | Keeps Q9 at its own recommendation (ADJ line 779); Variant 1 overrides it, Variant 3 narrows it beyond the question. |
| C-003 | Variant 2 | 60% | The conditional rule at ADJ line 253 is already phrased for a future panel; Variant 3's "history" demotion and Variant 1's new section both go further than needed. |
| C-004 | Variant 1 | 60% | Only Variant 1 gives the person one screen; Variants 2 and 3 accept two places to look. |
| C-005 | Variant 1 | 85% | Only Variant 1 names the freshness gap, and it is confirmed (MR lines 180, 422). |
| X-001 | Variant 2 | 65% | Matches the spec's recommendation (MR line 544) and is compatible with both sides of D-6 (R2V5 line 69). |
| X-002 | Variant 2 | 80% | Same scope as ADJ line 361 ("now"); Variant 1 contradicts it, Variant 3 extends it. |
| X-003 | Variant 2 | 80% | Nothing built, soft edge kept, rule waiting: cheapest reversal in both directions. |
| U-001 | Variant 1 | 85% | The staleness gap is a real, sourced constraint any later yes must handle. |
| U-002 | Variant 2 | 60% | Naming its own drift risk is honest and points to a concrete fix (a written trigger). |
| U-003 | Variant 3 | 75% | The no-crossing boundary is the clearest statement of the vocabulary hazard (ADJ lines 250 to 256). |
| A-001 | Variant 2 | 70% | With release 3 unscheduled by default (MR line 546), committing nothing costs least. |
| A-002 | Variant 2 | 75% | With PR #539 open (ADJ line 78), only Variant 2 is indifferent to how the sweep merges. |

## Overall

Variant 2 is the best-evidenced answer because its scope ("not now") matches the spec recommendation, the default, the 78 percent judgement and both sides of the source split, while Variants 1 and 3 each go beyond the evidence in opposite directions. Its real weakness is the missing re-ask trigger, which should be added, along with Variant 1's freshness gap as a recorded constraint for any later yes.

Overall: the variant I judge best for the owner is Variant 2, confidence 70%
