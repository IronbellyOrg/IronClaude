# Round 1 advocate statement: Variant 3 (never; the observer reads Orca only, by design)

Advocate: Variant 3. Persona: architect (structure, dependencies, long-term impact). Mode A, depth quick, Round 1 only.

Abbreviations used below: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; R2-V5 = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V5.md`. Every line number below was re-read for this statement.

## Position summary

Variant 3 answers Q17 with a standing boundary: the observer reads the Orca ledger and coordinator questions only, and never reads the sweep's report or JSON. The joined view of Orca state and sweep classes, if anyone ever builds one, belongs in Orchestrator v2, not in the observer.

The architectural case rests on three verified facts:

1. The two programs own disjoint facts. The units table gives the observer "none" of "Git, contracts, transcripts, `safe_to_close`, frozen plans, Task specs" and gives the sweep "owns" (ADJ line 240). A boundary that matches the ownership table is the lowest-coupling design.
2. The two contracts are incompatible in shape, not just in field names. ADJ line 131 (E-05, 94 percent): observe snapshot v1 is camelCase, `"UNKNOWN"` strings, keyed `dispatchId`, "additionalProperties false"; sweep report JSON v1 is snake_case, `null`, keyed `row_id` = `orca:<dispatch>`, "printed to stdout only". ADJ lines 250 to 256 list seven words ("stale", "unknown", "unavailable", "could not determine", "historical", "frozen", "settled") whose meaning differs between the programs. Any observer panel that reads both needs a translation layer and a second vocabulary on one screen.
3. The plan already has a home for sweep facts outside the observer. SW-11 blocks "V2-04 (if v2 reads stored sweep facts)" (MR line 200), and the debate judged at 78 percent that sweep JSON v1 is a candidate carrier "only for v2 and for a Coder#477 status record, not for the observer" (ADJ line 361).

Writing the boundary down removes a soft dependency edge (graph row 61, "SW-11 to OB-09, SOFT, Only if Q17 = yes", MR line 708) instead of carrying it indefinitely, and keeps observer release planning independent of the open sweep PR #539 (ADJ line 78) and of the persistence decision Q9 (ADJ line 779).

## Steelman of Variant 1

Strongest version: the person deciding what to do about a worker needs the Orca state and the sweep's proof-backed class at the same moment, and the observer is the only screen that person already watches. The observer cannot get those facts any other way (ADJ line 240). Two of the source reviews wanted the observer to read sweep facts "eventually, for facts only the sweep has" (R2-V5 line 69; that line names them "V1 and V4", and the question file calls them "reviews 01 and 04"; the mapping between those labels is UNVERIFIED here). Variant 1 also does the honest work of naming its own costs, and it is the only variant that names the freshness gap: the sweep runs at most once per 5 minutes under WC-16 (ADJ line 81, "a cap, not a schedule"), while the observer reads every 15 s (ADJ line 130), so the sweep column is always older than the Orca column beside it. It also uses the already-written safety rule: "if a panel ever shows sweep rows it prints the sweep's words verbatim and labels the report age" (ADJ line 253). What it gets right: the user need is real, and Decision Desk (OB-09) is the natural place a person would look.

Critique with counter-evidence:

- It pulls a deferred persistence decision forward into the critical path of a deferred release. OB-09 is itself "DEFERRED (L4)" (MR line 257); Variant 1 would make it depend on SW-11 (MR line 200) and therefore on Q9, whose own recommended answer is "Not now" (ADJ line 779). That is two deferred items made into a hard chain.
- It contradicts the one quantified judgement on this point (ADJ line 361, 78 percent, "not for the observer"), and Variant 1 admits this in its own costs.
- It adds a dependency on unmerged code: the sweep is in PR #539, still open (ADJ line 78).
- Its own freshness point is a structural argument against it: a 15 s live screen with a column that can be minutes old is exactly the mixing ADJ lines 250 to 256 warn about. The verbatim-words rule labels the problem; it does not remove it.

## Steelman of Variant 2

Strongest version: Variant 2 is the spec's own recommended answer, "No, not now; if yes later, Q9 becomes a real requirement" (MR line 544; ADJ line 787), and the default if the owner says nothing (MR line 544). It matches the debate's 78 percent judgement exactly in scope, because that judgement is tied to "Q17: no observer panel for sweep facts now" (ADJ line 361), not "ever". It costs nothing: OB-09 plans against snapshot v1 only, NFR-001 and its two pinned tests stay (ADJ line 83), and Q9 keeps its default (ADJ line 779). It keeps the verbatim-words rule (ADJ line 253) ready, so a later "yes" has a rule waiting. It respects the source debate's settling fact that D-6 is for "The owner only" (R2-V5 line 69) by leaving the owner free to say yes later at no extra cost. It is also self-aware: it names that "not now" has no written trigger and may drift into "never".

Critique with counter-evidence:

- A soft edge with no trigger is a dependency that never resolves. Graph row 61 (MR line 708) and the OB-09 condition (3) branch "or sweep facts, which then needs Q17 = yes and SW-11" (MR line 257) stay in every future plan as an open branch, and every reviewer of release 3 must re-check them.
- Variant 2 concedes that if Decision Desk is designed first without sweep facts, adding them later may mean reworking its layout. That is the classic cost of an undecided boundary: designers either reserve space for a panel that may never come or accept rework.
- Variant 2 does not say where a person sees the two fact sets together. Variant 3 at least names an architectural home (v2, already linked to sweep facts through SW-11's "V2-04 (if v2 reads stored sweep facts)", MR line 200).

These are real but modest costs. Variant 2's weakness (drift) is cheaper to fix than Variant 3's weakness (over-reach): adding one trigger sentence to Variant 2 fixes it.

## Strengths claimed

1. Lowest coupling, matching the ownership table. Two collectors, two contracts, no reader crossing between them (Variant 3, "What it unlocks"; diff analysis U-003). This mirrors ADJ line 240 exactly.
2. Removes a dependency instead of carrying it. Variant 3 deletes the SW-11 to OB-09 SOFT edge (MR line 708) and fixes OB-09 condition (3) as "snapshot v1 only" (MR line 257). One fewer open branch in a dependency graph whose rows run past 60 (MR lines 676 to 709).
3. Release independence. Observer release planning never waits on PR #539 (ADJ line 78), Q9 (ADJ line 779), or NFR-001 (ADJ line 83).
4. Removes the vocabulary-mixing risk at the source rather than labelling it. The seven conflicting words in ADJ lines 250 to 256 and the incompatible JSON shapes in ADJ line 131 can never meet on one screen.
5. Narrows SW-11 and Q9 to the consumers the debate actually named. ADJ line 361 names v2 and Coder#477 as the only candidate carriers; Variant 3 makes Q9 answerable on those needs alone.
6. Names an architectural home for the joined view (v2), which Variant 2 leaves blank.

## Weaknesses identified in others

Variant 1:
- Chains two deferred items (OB-09, MR line 257; SW-11, MR line 200) and pulls Q9 forward against its own "Not now" (ADJ line 779).
- Goes against the 78 percent judgement (ADJ line 361).
- Depends on an open PR (ADJ line 78).
- Puts a source capped at once per 5 minutes (ADJ line 81) beside a 15 s live feed (ADJ line 130) on one screen.
- May require changing NFR-001 and its two pinned tests (ADJ line 83) if caller-side capture is not enough.

Variant 2:
- No written trigger, so "not now" can silently become "never" without the owner deciding (its own admission).
- Leaves a soft edge (MR line 708) and an OB-09 branch (MR line 257) open indefinitely.
- Leaves the layout of Decision Desk exposed to later rework (its own admission).
- Does not say where the joined view lives.

## Concessions

1. Variant 3 goes further than the evidence. The 78 percent judgement is explicitly about "now" (ADJ line 361), and the spec's recommended answer is "No, not now" (MR line 544; ADJ line 787). Nothing in the cited sources supports "ever". Variant 3 admits this in its own costs.
2. It closes a door that two source reviews wanted open (R2-V5 line 69), and the source debate said the decision belongs to "The owner only" (R2-V5 line 69). A "never" is the owner's to give, but the evidence does not push the owner there.
3. Reversing a written boundary costs more than answering a deferred question (diff analysis X-003).
4. The person always reads two outputs, and v2, the named home for a joined view, is unbuilt.
5. The symmetric clause "the sweep reads no observer output" in Variant 3 answers a question nobody asked. I found no cited plan for the sweep to read observer output (R2-V5 line 108 option (b) is a Coder-owned copy of the observer snapshot, not a sweep reader); whether any such plan exists is UNVERIFIED.
6. Variant 3 does not raise the freshness gap (C-005), which is actually an extra argument for it; Variant 1 found it first.
7. Most of Variant 3's structural benefits (no dependency on PR #539, NFR-001 untouched, OB-09 on snapshot v1 only) are also delivered by Variant 2 for as long as "not now" lasts. The marginal gain of "never" over "not now" is only the removal of one soft edge and the end of default re-opening.

## Shared assumptions

- A-001 (observer release 3 will actually be built): QUALIFY. OB-09 is "DEFERRED (L4)" (MR line 257) and gated on Q17 and Q19 (MR line 257; graph rows 59 and 60, MR lines 706 and 707), so release 3 is a plausible consumer but not a scheduled one. Under that uncertainty, the answer that commits least (Variant 2) is favoured; a "yes" (Variant 1) spends effort on a consumer that may never come, and a "never" (Variant 3) fixes a rule for a release that may never be designed.
- A-002 (the sweep merges and keeps its fact set): QUALIFY. The sweep is in PR #539, still open (ADJ line 78), but the fact set (git, contracts, transcripts, `safe_to_close`, frozen plans, Task specs) is recorded as sweep-owned in the units table (ADJ line 240), and the frozen and settled classes are cited to `classify.py` lines (ADJ lines 255, 256). The fact set is stable enough to reason about; the merge is not certain. If the PR stalls, Variant 1 has nothing to read, Variant 3's boundary is harmless but unnecessary, and Variant 2 costs nothing.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (none superior) | 90% | All three use the same five sections. |
| C-001 | Variant 2 | 60% | Both 2 and 3 plan release 3 on snapshot v1 only; keeping the soft edge (MR line 708) costs little and keeps the owner's option. Variant 3's removal is cleaner but forecloses. |
| C-002 | Variant 3 | 55% | Scoping Q9 to v2 and Coder#477 matches the only carriers the debate named (ADJ line 361); Variant 2 reaches the same default (ADJ line 779) with one more open reason. |
| C-003 | Variant 2 | 60% | The verbatim-words rule (ADJ line 253) costs nothing to keep live; demoting it to history gains nothing. |
| C-004 | Variant 3 | 55% | Names an architectural home (v2) consistent with SW-11's V2-04 link (MR line 200); Variant 1's single-screen join crosses the ownership table (ADJ line 240). |
| C-005 | Variant 1 | 80% | Only variant to name the freshness gap; confirmed by the WC-16 cap (ADJ line 81) against 15 s observer reads (ADJ line 130). |
| X-001 | Variant 2 | 60% | "Not now" matches the spec answer and default (MR line 544) and leaves the owner-only decision (R2-V5 line 69) open. |
| X-002 | Variant 2 | 80% | The 78 percent judgement is scoped to "now" (ADJ line 361); Variant 2 matches it exactly. |
| X-003 | Variant 2 | 80% | Nothing built, nothing written as a rule; cheapest to reverse in either direction. |
| U-001 | Variant 1 | 75% | Real, verified, and relevant to any future panel. |
| U-002 | Variant 2 | 60% | Honest naming of the drift risk; easily fixed by adding a trigger sentence. |
| U-003 | Variant 3 | 70% | The clearest separation, matching ADJ lines 131 and 240. |
| A-001 | Variant 2 | 65% | Release 3 is deferred (MR line 257); the least-committing answer wins under that uncertainty. |
| A-002 | Variant 2 | 65% | PR #539 is open (ADJ line 78); Variant 2 is the only answer that costs nothing whether it merges or stalls. |

## Overall

As the architect advocate, I hold that Variant 3 states the right long-term shape (disjoint ownership, two contracts, the joined view in v2), but the evidence supports "not now", not "never", and Variant 2 delivers almost all of Variant 3's structural benefits while keeping the owner's option open. Variant 2's one real gap, the missing trigger, is fixed by a single added sentence (for example, "revisit Q17 when OB-09 is planned"), which is cheaper than Variant 3's cost of reversing a written boundary.

Overall: the variant I judge best for the owner is Variant 2, confidence 62%
