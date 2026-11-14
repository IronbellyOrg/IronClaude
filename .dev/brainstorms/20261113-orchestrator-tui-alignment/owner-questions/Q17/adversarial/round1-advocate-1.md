# Round 1 advocate statement: Variant 1 (frontend persona)

Advocate for Variant 1 ("yes, plan a sweep-facts panel for the observer's release 3"). Persona: frontend, meaning what a person at the screen needs in order to decide. Mode A, depth quick, Round 1.

Sources re-read for this statement (line numbers confirmed by reading):
- merged-requirements.md (MR) lines 200, 257, 536, 544, 546, 549, 678, 707, 708.
- alignment-findings-adjudicated.md (ADJ) lines 77, 78, 81, 83, 129, 131, 239, 240, 244, 250 to 257, 359, 361, 779, 787.
- round2-rebuttal-V5.md (R2-V5) lines 69, 80, 103, 106, 108.

## Position summary

The decision a person makes in front of the Decision Desk is "what do I do about this worker now: wait, answer, close, or chase?". The Orca ledger answers "what state is the worker in" (ADJ line 239: state, outcome, liveness, next action, evidence age). It cannot answer "is it safe to close", "is its plan frozen", "is a person blocking it" or "is its worktree dirty": ADJ line 240 says the observer owns none of git, contracts, transcripts, `safe_to_close`, frozen plans and Task specs, and the sweep owns all of them. Variant 1 is the only answer that puts the facts a person needs for the close-or-wait decision on the screen where that decision is made. Reviews 01 and 04 wanted exactly this "eventually, for facts only the sweep has" (R2-V5 line 69, V1 and V4).

Variant 1 also carries its own safety rails: sweep words printed verbatim, report age labelled (ADJ line 253), and it is the only variant that names the freshness gap between live Orca rows and an older sweep report (U-001).

Having read all three variants and the sources, I argue Variant 1's user-need case in full below, but I do not judge it the best answer for the owner today. Its timing is wrong: the screen it targets is deferred and unscheduled, and the data source it reads is unmerged and has no stored form.

## Steelman of Variant 2

Strongest version: "The user need is real, but nobody can design a good panel for a release that has no first ask, from a JSON whose keys are not final, with no stored copy to read. Keep the door open, keep the rule waiting, and decide when there is something to build."

What it genuinely gets right:
- It costs nothing now and is the cheapest to reverse (X-003). OB-09 is "DEFERRED (L4)" (MR line 257), and Q19's own recommendation is "Fleet Quilt or Decision Desk first" (MR line 546), so Decision Desk may not even be the first reviewer ask built.
- It matches the debate's 78 percent judgement, which is explicitly about "now" (ADJ line 361: "Q17: no observer panel for sweep facts now").
- It keeps the verbatim-words and report-age rule alive in the contract note (ADJ line 253), so a later "yes" has a UX rule ready.
- It keeps NFR-001 and its two pinned tests untouched (ADJ line 83; R2-V5 line 80).
- It is honest about its own drift risk: "Not now has no trigger written down" (U-002).

Critique: from the screen's point of view, Variant 2 leaves the person with two places to look (its own words) and gives no signal to the Decision Desk designer that a sweep column may arrive. If the layout is designed first without that slot, adding it later "may mean reworking its layout" (variant 2, line 23). That is a real cost, but a small one: it is a layout risk, not a data-loss or correctness risk, and it can be removed by one sentence in OB-09 ("leave room for a possible sweep-facts area").

## Steelman of Variant 3

Strongest version: "Two programs with two vocabularies on one screen is a standing misreading hazard. 'stale' means 45 seconds with no good read in the observer and a 6 hour transcript window in the sweep (ADJ line 250); `UNKNOWN` versus `null` (ADJ line 251); 'historical' and 'frozen' mean different things (ADJ lines 254, 255). The safest screen is one that only ever speaks one program's language. Write it down so nobody reopens it."

What it genuinely gets right:
- The vocabulary collision is documented, not hypothetical (ADJ lines 250 to 257), and a person scanning a dashboard reads words, not footnotes.
- It matches the current fact that the two programs never mention each other (ADJ line 129, 95 percent).
- It gives the observer's release planning total independence from PR #539 (open, ADJ line 78).
- U-003, "two collectors, two contracts, no reader crossing", is the cleanest architectural statement of the three.

Critique: Variant 3 admits it "goes further than the debate" (variant 3, line 25). The settling fact for D-6 is "the owner only" (R2-V5 line 69), and the debate itself scoped its judgement to "now" (ADJ line 361). From a UX standpoint the misreading hazard has a known mitigation already written: "if a panel ever shows sweep rows it prints the sweep's words verbatim and labels the report age" (ADJ line 253), and the mapping table's rules ("say feed stale or session stale; never show one as the other", ADJ line 250). Variant 3 demotes that rule to "history" (variant 3, line 11), which throws away a ready-made UX safeguard to prevent a screen nobody has designed yet. It also guarantees that a person must "always read two outputs" (variant 3, line 23) with no route back short of reversing a written boundary.

## Strengths claimed

1. **Serves the actual decision.** The close-or-wait decision needs `safe_to_close`, frozen plans, waiting-on-a-person and git state, and only the sweep has them (ADJ line 240). Without them the Decision Desk shows state but cannot support the decision its name promises.
2. **Gives Decision Desk content no other source provides.** The observer cannot derive these facts; it prints `SETTLED` and `POLICY FROZEN` as `unavailable (no source)` (ADJ lines 255, 256). A panel turns those "no source" cells into sourced answers.
3. **Comes with its UX guardrails.** Verbatim sweep words and a visible report age (ADJ line 253; variant 1 line 12); labelled meanings for shared words (ADJ lines 250 to 257).
4. **Names the freshness gap honestly (U-001, C-005).** Sweep facts on a live screen "are always older than the Orca rows beside them" (variant 1, line 24). This is the most important UX fact in the whole question and only Variant 1 states it. It is also understated: WC-16 is "a cap, not a schedule" (ADJ line 81), so a sweep report can be far older than 5 minutes, not just up to 5 minutes.
5. **Picks the least invasive persistence path.** It points SW-11 at caller-side capture first, Q9's own recommended first step (ADJ line 779; MR line 200), and only names relaxing NFR-001 as the alternative.
6. **Resolves the user's open request rather than parking it.** D-6 is a real user wish from two reviews (R2-V5 line 69); Variant 1 is the only answer that says what the person will eventually see.

## Weaknesses identified in others

Variant 2:
- Leaves the person with two places to look for the foreseeable future (variant 2, line 22).
- No written trigger for reopening (variant 2, line 24), so "not now" can silently become "never" without the owner ever deciding.
- Gives the Decision Desk designer no instruction to leave space for sweep facts, which risks a later layout rework (variant 2, line 23).

Variant 3:
- Exceeds the evidence: the 78 percent judgement is about "now" (ADJ line 361), and the debate assigned the "ever" question to the owner only (R2-V5 line 69).
- Discards the existing UX mitigation (ADJ line 253) by keeping it "only as history".
- Hardest to reverse (X-003): a written boundary that a future reviewer must argue against, not a deferred question.
- Its "likely v2" place for a combined view (variant 3, line 29) points at an unbuilt program, so the combined view has no concrete home at all.

## Concessions

Honest weaknesses in Variant 1:
1. **It plans for a screen that is not scheduled.** OB-09 is "DEFERRED (L4)" (MR line 257); Q19 has not chosen Decision Desk over Fleet Quilt (MR line 546). Answering "yes, for release 3" binds a requirement to a release whose first ask is undecided.
2. **It depends on an unmerged program.** PR #539 is open (ADJ line 78), and the sweep JSON keys are to be decided "in #339 after #539 merges" (ADJ line 359). A panel designed now would be designed against keys that may change.
3. **It promotes Q9 to a requirement now** (variant 1, line 10), pulling persistence work forward for a consumer that does not exist yet. The contract note was deliberately designed to publish nothing new for the other program in version 1 (R2-V5 line 103).
4. **Its own freshness risk is a serious UX problem, not a footnote.** A live 15 second Orca row beside a sweep class that may be much older invites the person to act on a stale "safe to close". The age label mitigates this but does not remove it.
5. **It goes against the debate's 78 percent judgement** (ADJ line 361), which it states openly (variant 1, line 22).
6. **Q22 is not exactly the right home for the sweep-report age.** Variant 1 cites Q22 as "the staleness age question" (variant 1, line 29); Q22 asks "What age makes a snapshot or workspace record stale?" (MR line 549). A sweep report age limit would need Q22 widened or a new question.

Net: Variant 1 is right about what the person needs, and wrong about when to commit to it.

## Shared assumptions

| ID | Response | Reason |
|---|---|---|
| A-001 (release 3 Decision Desk will actually be built) | QUALIFY | The consumer is plausible but not certain: OB-09 is "DEFERRED (L4)" (MR line 257) and Q19 recommends "Fleet Quilt or Decision Desk first" (MR line 546), so Decision Desk may come later or not at all. This hurts Variant 1 most (it commits work to a possibly absent consumer), costs Variant 2 nothing, and makes Variant 3's boundary unnecessary if the screen never exists. |
| A-002 (sweep merges and keeps its fact set) | QUALIFY | The fact set is documented as the sweep's (ADJ line 240), but PR #539 is open (ADJ line 78) and the JSON keys are decided only after it merges (ADJ line 359). The facts are stable in kind but not in shape, so any answer that designs against concrete keys now (Variant 1) carries rework risk; a deferral (Variant 2) does not. |

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (all three equal) | 95% | Same five sections; no layout difference affects the owner. |
| C-001 | Variant 2 | 65% | Keeps OB-09 on one settled contract now while leaving the SW-11 edge soft (MR lines 257, 708); Variant 1 ties a deferred release to an unmerged PR; Variant 3 removes an edge the owner may want later. |
| C-002 | Variant 2 | 70% | Keeps Q9's own default (ADJ line 779) and NFR-001's pinned tests (ADJ line 83) without pulling persistence forward for a consumer that is not scheduled. |
| C-003 | Variant 2 | 60% | Keeps the verbatim-words and report-age rule (ADJ line 253) live for a future panel; Variant 1's new section is premature before keys are decided (ADJ line 359); Variant 3 demotes the rule to history. |
| C-004 | Variant 1 | 70% | From the person's side, one screen with both the Orca state and the sweep's proof-backed class is what the close-or-wait decision needs (ADJ line 240). |
| C-005 | Variant 1 | 85% | Only Variant 1 names the freshness mismatch; it is the central UX hazard of any combined screen (WC-16 is a cap, not a schedule, ADJ line 81). |
| X-001 | Variant 2 | 60% | "Undecided, not now" fits the evidence: the debate scoped its view to "now" (ADJ line 361) and left "ever" to the owner (R2-V5 line 69). |
| X-002 | Variant 2 | 75% | It reads the 78 percent judgement at its stated scope; Variant 1 goes against it, Variant 3 stretches it. |
| X-003 | Variant 2 | 80% | Nothing is built or written as a boundary, so reversal is cheapest. |
| U-001 | Variant 1 | 85% | The staleness gap is the most decision-relevant UX fact and only Variant 1 raises it. |
| U-002 | Variant 2 | 70% | Naming its own drift risk is valuable; it also tells the owner how to fix it (add a trigger). |
| U-003 | Variant 3 | 65% | The cleanest separation statement; useful as a description of today even if not adopted as a permanent rule. |
| A-001 | Variant 2 | 65% | If release 3 or Decision Desk never comes, "not now" costs nothing; Variant 1 wastes effort, Variant 3 writes an unneeded rule. |
| A-002 | Variant 2 | 70% | If #539 changes or stalls, a deferral has nothing to rework; Variant 1 would have designed against moving keys. |

Suggested merge for the owner to consider (not a decision): take Variant 2's answer, add a written trigger (for example "reopen Q17 when Q19 picks Decision Desk and PR #539 has merged"), add one sentence to OB-09 asking the Decision Desk layout to leave room for a sweep-facts area, and carry Variant 1's freshness warning (U-001) into the contract note beside the verbatim-words rule.

## Overall

Overall: the variant I judge best for the owner is Variant 2, confidence 62%.
