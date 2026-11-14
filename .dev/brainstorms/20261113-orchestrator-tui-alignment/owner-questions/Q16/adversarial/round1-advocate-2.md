# Round 1 advocate statement: Variant 2 (one trust design), persona architect

Debate: sc:adversarial Mode A, depth quick, Round 1. Variant 2 is proposal B, "one trust design for every consumer". Short names for sources: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; DA-review = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/diff-analysis.md`; DA = this folder's `diff-analysis.md`.

## Position summary

Variant 2 asks the owner to promise one trust design: the grant format, signing and verification chosen under #339 are the only ones, and the observer (#409), Orchestrator v2 (#423) and the workspace listener (Coder#477) import them instead of defining their own. Its case is structural: one mechanism to build, review and test; one owner (#339) for every trust question; a written bar on a second format (review 03's Edit 7, quoted in DA-review line 89: "The grant format is the one chosen in IronbellyOrg/IronClaude#339 ... This issue does not define a second format."); and no translation layer if the programs later relay to each other. It also needs no wording change in the #409 correction pass, because decision 6 already reads "Decide one design, not two." (ADJ line 567; the live issue text was not re-read here, UNVERIFIED as of today).

I argue these strengths honestly, but the evidence I checked weighs against my variant on the decisive points, and I say so in Concessions and Overall.

## Steelman of Variant 1

Strongest version: no trust layer, grant format, signing scheme or relay exists (MR line 129: the Phase 4 trust layer belongs to later #339 phases; MR line 201: SW-12 is DEFERRED). Any promise today is a promise about a design nobody has drawn. Variant 1 makes no public commitment in either direction, so nothing has to be walked back, and it re-asks the question when SW-12's Phase 4 row is opened, "so the choice is made with a real design in view" (DA U-001). It is exactly the spec's default if the owner says nothing (MR line 543), so it asks nothing new of the owner now, and OB-08, V2-01 and the CO-01 post still proceed minus one clause (variant-1 "What it unlocks").

Critique with counter-evidence:
- It leaves standing a sentence that two reviews flagged and the debate leaned 66 percent against (ADJ line 382). Variant 1 admits this in its own costs: "Readers of #409 may keep designing toward one shared design."
- It holds work that names the XC-08 vocabulary as a precondition: V2-03 lists XC-08 (MR line 400), V2-04 lists XC-08 (MR line 401), SW-12 Phase 4 "uses the vocabulary from XC-08" (MR line 201), and the OB-09 row refers to the "vocabulary of XC-08" (MR line 257). Variant 1 admits these "stay held".
- Its own text says the question "returns at a worse time, when more text may rest on the old sentence". Deferral does not avoid the choice; it moves it to a point where reversal costs more (see A-002 below).
- Architecturally, an unanswered interface question is still an answer: meanwhile each consumer is free to invent its own format, which is the outcome both other variants try to prevent.

## Steelman of Variant 3

Strongest version: standardize the interface, not the implementation. A shared grant vocabulary (who may do what) and a shared audit record (what was granted and used) are the contract every consumer must honour; the mechanism behind them is chosen per threat model. This is the spec's recommended answer (MR line 543; ADJ line 382, X-005 at 66 percent), and it is the only option the spec places in reach: section 1.3 "What stays out of scope until later" lists "One trust design (ADJ Part 8 row X-005); only one grant vocabulary and audit format is in reach (Q16)" (MR line 146). It fits the facts on threat models: the three consumers differ (ADJ lines 295 and 809), and even the review that proposed Edit 7 notes the watcher's trust under option A is "a different, local model" (DA-review line 89). It is the only branch the spec writes out in full: XC-08 (2) gives the exact decision 6 wording and the #423 and Coder#477 instruction for the vocabulary answer (MR line 456), and ADJ line 567 has the edit text. One audit format keeps grants from all three programs readable side by side, which the OB-09 row uses (MR line 257; DA U-003). It is honest about poisoned content, which no grant design fixes, and points to the separate rule that relayed text stays data (V2-04, MR line 401: "relayed knowledge as a pinned set of typed fields with free text only in `detail`").

Critique with counter-evidence:
- Its own costs section names the main architectural risk: "Three mechanisms to build and review instead of one, and a risk that they drift apart beneath shared words." A vocabulary without shared meaning is a weak contract.
- "A shared vocabulary can hide real differences: the same word ('grant', 'read') may mean weaker protection in one program than in another" (variant-3 costs). An audit record that reads the same across programs while meaning different protection can mislead the person reading it side by side, which is the very use U-003 claims.
- The promise has no content yet: the vocabulary's terms and the audit record's fields "both wait for SW-12 Phase 4" (variant-3 "What stays unresolved"). It settles a sentence, not a contract.
- It does not authorize relay (MR line 574), so the cross-program case that most needs shared trust still needs its own decision.

These are real, but they are risks to manage inside SW-12 Phase 4, not reasons the promise is wrong.

## Strengths claimed

1. One mechanism, one owner. Variant 2 gives every trust question a single home in #339's trust layer and forbids a second format in writing (Edit 7, DA-review line 89). From a structure and dependency view this is the cleanest graph: three consumers depend on one module, not on three modules that share only names (DA U-002).
2. No drift in meaning by construction. Variant 3's admitted risk ("drift apart beneath shared words") cannot occur when there is one implementation. The word "grant" means the same protection everywhere.
3. No translation layer later. If v2 relays to agents (Q14) or a remote listener arrives, the programs already share verification, so no adapter has to map one program's grant onto another's (variant-2 "What it unlocks").
4. Smallest edit to #409. Decision 6 keeps its current wording, so the OB-08 pass has one step fewer (variant-2 "What happens next"; the ordered pass in ADJ line 571 runs decision 6 as step 3 "only if Q16 = vocabulary").
5. Every gated item gets a settled clause (DA C-004), the same as Variant 3 and unlike Variant 1.

## Weaknesses identified in others

- Variant 1: holds V2-03, V2-04, OB-09 and SW-12 Phase 4 (MR lines 201, 257, 400, 401); keeps a flagged sentence; re-asks later at higher cost by its own account; leaves each consumer free to invent a format meanwhile.
- Variant 1: does not address poisoned content at all (DA C-005).
- Variant 3: three mechanisms and possible drift beneath shared words (its own costs); the same audit word may carry different protection; the vocabulary is empty until SW-12 Phase 4; relay still unauthorized (MR line 574).
- Variant 3: the assignment of who defines the vocabulary is marked PLAN INFERENCE (MR line 456, XC-08 (3)), so its ownership is less firmly sourced than its wording.

## Concessions

I concede these weaknesses in Variant 2 because the sources support them:

1. The spec puts my variant out of scope. MR section 1.3, line 146, lists "One trust design" under "What stays out of scope until later" and says "only one grant vocabulary and audit format is in reach (Q16)". Choosing Variant 2 contradicts the spec's own scope boundary, not just its recommendation.
2. Different threat models. The observer is read-only on one host, the watcher's trust is "a different, local model" (DA-review line 89, from the review that proposed Edit 7 itself), and the listener crosses workspaces. One design must either fit the strictest case (over-building the observer) or the weakest (under-protecting the listener). ADJ line 809 rejects one design for this reason.
3. Signing does not stop poisoned content. #339 comment 2 says "encryption alone is not enough" (ADJ line 295; MR line 407). A shared signing design can give a false sense of safety for relayed text; the real control is V2-04's typed-fields rule (MR line 401), which Variant 2 does not supply.
4. It commits three public issues to a design that does not exist (SW-12 Phase 4 is unbuilt, MR lines 129 and 201). If the design fits one consumer badly, three texts must change; under Variant 3 only one consumer's mechanism changes.
5. The spec writes no XC-08 branch for "one design". XC-08 (2) gives wording only for the vocabulary answer (MR line 456). Variant 2 relies on Edit 7, which comes from a review, not from the adjudicated plan; ADJ line 382 says "do not promise one design in #409 or #423".
6. The debate leaned 66 percent against it (ADJ line 382). 66 percent is not strong, and the point was ruled "not decidable from sources" (DA-review line 89), so this concession alone would not be decisive; items 1 to 5 together are.

## Shared assumptions

- A-001 (the three consumers are the complete set; the watcher #450 is outside): QUALIFY. The three named issues are the ones the spec ties to Q16 (MR line 456 names #409, #423 and Coder#477), so the set is right for the question as asked. But the watcher is a plausible fourth party: DA-review line 89 says its trust under option A is "a different, local model", and MR line 143 keeps watcher prompts out of the listener until FU-1 is recorded. Whether the watcher will ever need grants is UNVERIFIED. This assumption hurts Variant 2 most: a mandatory single design would have to stretch to cover a consumer already known to use a local model, whereas that consumer can adopt a vocabulary without changing its mechanism.
- A-002 (issue text is cheap and reversible): QUALIFY. The text edits are reversible by issue history (ADJ lines 189 and 573: "Undo: yes, issue history"). But the promise feeds later design work: SW-12 Phase 4 "uses the vocabulary from XC-08" (MR line 201) and V2-03's brainstorm depends on XC-08 (MR line 400). Once a design or code is built against the promise, reversal is no longer cheap. The broadest promise (Variant 2) carries the highest reversal cost; the narrowest settling promise (Variant 3) carries less; Variant 1 carries none now but defers the cost.

## Per-point verdicts

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | None (identical layout) | 95% | All three use the same five sections; no structural advantage. |
| C-001 | Variant 3 | 70% | Keeping "Decide one design, not two." contradicts MR line 146, which puts one trust design out of scope; the replacement wording is ready (ADJ line 567). |
| C-002 | Variant 3 | 65% | Edit 7 bars a second format, which is valuable, but it names a format that does not exist, and ADJ line 382 says not to promise one design in #423; promising the vocabulary matches XC-08 (2). |
| C-003 | Variant 3 | 55% | Both 2 and 3 assign the content to SW-12 Phase 4; Variant 3 assigns what MR line 146 says is in reach. Its assignment is PLAN INFERENCE, which keeps the margin small. |
| C-004 | Variant 3 | 60% | 2 and 3 both settle every gated clause, but only the vocabulary branch has wording written in XC-08 (MR line 456); Variant 2's clauses would need new text. |
| C-005 | Variant 3 | 75% | It points to an actual rule for poisoned content (V2-04, MR line 401); Variant 2 only names the risk; Variant 1 is silent. |
| X-001 | Variant 3 | 65% | Different threat models (ADJ lines 295, 809) argue against one mechanism; shared words plus one audit shape is the interface level the facts support. |
| X-002 | Variant 3 | 60% | The narrower promise is cheap and does not need a design to exist; Variant 1's prematurity point is fair but holds V2-03, V2-04, OB-09 and SW-12 Phase 4. |
| X-003 | Variant 3 | 70% | The sentence over-promises against the spec's scope (MR line 146) and the adjudicated row (ADJ line 382); correcting it in the #409 pass is the planned step (ADJ line 571). |
| U-001 | Variant 1 | 60% | Re-asking with a real design in view is a genuine contribution the others lack; Variant 3 could adopt it as a review trigger in SW-12 Phase 4. |
| U-002 | Variant 2 | 70% | One owner and a written bar on a second format is the clearest dependency rule; Variant 3 could borrow it by barring a second vocabulary. |
| U-003 | Variant 3 | 70% | One audit format readable across programs serves OB-09 directly (MR line 257), subject to the caveat that equal words may hide unequal protection. |
| A-001 | Variant 3 | 55% | A vocabulary extends to a fourth consumer with its own local model; one design would have to absorb it. |
| A-002 | Variant 1 | 55% | Committing nothing has the lowest reversal cost if code is later built; Variant 3 is a close second; Variant 2 is the costliest to reverse. |

## Overall

As advocate I claim for Variant 2 a cleaner dependency structure, one owner, and no drift in meaning beneath shared words. Those are real architectural goods, and Variant 3 should borrow two of them: a written bar on a second vocabulary (adapted from Edit 7), and a rule in SW-12 Phase 4 that each vocabulary word states the protection it carries in each program, so the shared audit record does not mislead. But the sources put one trust design outside the spec's scope (MR line 146), the consumers' threat models differ (ADJ lines 295, 809), signing does not address poisoned content (ADJ line 295), and only the vocabulary branch has written wording in XC-08 (MR line 456). Standardizing the interface while letting the mechanism vary is the sounder long-term structure for three consumers this different.

Overall: the variant I judge best for the owner is Variant 3, confidence 70%
