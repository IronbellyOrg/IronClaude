# Round 1 advocate statement: Variant 2 (sweep summary only, until the contract note exists)

Advocate: Variant 2. Persona: architect (structure, dependencies, long-term impact). Depth: quick, Round 1 only.

## Position summary

Variant 2 is the only answer that matches what is already built, contracted and written into the spec, so it costs zero edits and adds no new dependency between the sweep and the observer before their contract note exists. It keeps one source of facts in chat while the two programs still disagree on words, and it names the exact trigger (the XC-05 note) at which the observer question is reopened.

## Steelman

**Variant 1 (both reports, now), strongest form.** #339 literally asks for a static report "taking inspiration" from #409 (variant-5-original.md:221), and #409 is the observer, which is already built and merged (ADJ glossary line 77: "Built and merged: release 1 in PR #503, release 2 in PR #514"). `observe --once` is the only no-write static status (debate-transcript.md:904, X-004), so it can run between sweeps without breaking NFR-001's one-report-per-run rule (ADJ line 83), and it is the only way to reach the 3-minute end of "3 to 5 minutes" given the sweep's 5-minute cap (WORKER-CONTRACT.md:109). Variant 1 is the most faithful to the issue text and uses only programs that exist. It is also the only variant that flags the Q-1 risk (ADJ line 87) for the coordinator's own terminal.

**Variant 3 (no recurring report yet; park the clause), strongest form.** Nothing exists to print a report every 3 to 5 minutes: the coordinator loop is unbuilt (question.md fact 10), and WC-16 is "a cap, not a schedule" (ADJ line 81; debate-transcript.md:625 quoting "Phase 1 adds this duty, not a scheduler"). Answering "which report goes in the recurring chat slot" before the slot exists commits to a format early. Variant 3 also lines up with the owner's stated rule for automated output: "Automated status shows only the decision ledger's outstanding owner decisions and held items" (merged-requirements.md:1040, quoting SEED Batch 2 item 8). Parking is the most honest description of the current state.

## Strengths claimed

1. **Zero edits; the spec already says this.** Section 6.7 reads: "Q11's recommended answer applies to any in-chat report: the sweep summary only, until the note exists" (merged-requirements.md:1040). The Q11 row's recommended answer is the same (merged-requirements.md:538). Variant 2 is the only variant that changes no spec text (diff-analysis C-003, X-003). Variant 1 rewords 6.7; Variant 3 deletes its last sentence.
2. **It matches the shipped skill and output style on this branch.** The sweep skill's "Final reply" is already the one exempt reply: "only the summary counts and the report path are printed" under five conditions (src/superclaude/skills/sc-sweep-protocol/SKILL.md:35-43). The output style carries the same exception (src/superclaude/output-styles/pragmatic.md:22-23). Variant 2 gives that shipped exception its stated purpose; Variant 3 admits it leaves the exception "without a stated purpose in the recurring loop" (variant-3, Costs).
3. **It follows the source debate's recommendation word for word.** V5 D2: "keep the sweep reply as the WC-16 output until D1 is settled; do not name `observe` in WC-16 or the skill's `allowed-tools` yet. First step: none in code" (variant-5-original.md:222-223). V5 Q7 repeats it (variant-5-original.md:294). ADJ Part 7 carries the same recommendation (alignment-findings-adjudicated.md:781).
4. **Correct dependency order (architect view).** The contract note (D1, XC-05) is what fixes names, the join key and "one word list (stale, unknown, unavailable, could not determine, historical, frozen, settled ...)" between the two programs (variant-5-original.md:216). Putting both programs' text in one chat report before that note exists couples one reader to two vocabularies. Variant 2 sequences it correctly: note first, then decide whether the observer text joins, and it puts that decision inside the note itself (variant-2, "What happens next", last bullet).
5. **Keeps the observer out of the coordinator's rules while its binding is unproven.** Q-1 failed: "an unbound terminal cannot read another terminal's Run" (ADJ line 87), and whether `observe --once` in the coordinator's own terminal shows its own Run is UNVERIFIED (question.md fact 7). Variant 2 never names `observe` in WC-16 or the skill's tool list, so a negative result on that check costs nothing.
6. **No unmeasured load.** Combined load of observers plus sweep plus watcher was never measured (INV-032; merged-requirements.md:1032 as cited in question.md fact 8, not re-read here). Variant 2 adds no Orca calls per cycle; Variant 1 adds some.
7. **Cheapest to reverse, with an explicit reopen trigger.** If the owner later wants the observer text, adding it after the note is additive. Variant 2 states the trigger (the XC-05 note carries the line); Variant 3's trigger needs two unbuilt things (loop and note), which is a later and less defined reopen point.

## Weaknesses identified in others

1. **Variant 1 creates edits and couplings nobody scheduled.** By its own account it requires later edits to WC-16, the sweep skill's tool list and the output style (variant-1, "What happens next"), and an observe block "either keeps ordinary formatting or needs its own exception". The current exception is defined only for the sweep skill (pragmatic.md:22-23), so Variant 1 opens a second style exception with no design behind it.
2. **Variant 1 mixes two vocabularies in one report.** It concedes "two programs printing overlapping facts with different words (stale, unknown, historical) before the contract note fixes one word list ... can confuse the reader" (variant-1, Costs; variant-5-original.md:216). That is the exact failure the note exists to prevent.
3. **Variant 1's 3-minute benefit has no runner.** It says the observer "can fill the 3-minute end of 3 to 5 minutes", but the coordinator loop is unbuilt (question.md fact 10). The benefit is real only after a loop exists.
4. **Variant 1 rests on an unverified binding.** Its second half depends on `observe --once` seeing the coordinator's own Run, which is UNVERIFIED after Q-1 failed (ADJ line 87). Variant 1 lists this as a risk but answers "now" regardless.
5. **Variant 3 edits the spec to remove a sentence for no gain.** Graph edge 101 already records Q11 as "Recorded only; they gate no item" (merged-requirements.md:748). Deleting 6.7's last sentence is a spec change with no benefit, since 6.7's first sentence already limits automated status.
6. **Variant 3 does not actually answer the question.** The question asks which report it is (sweep, observe or both); "neither, for now" leaves "Which report ... the clause will mean when it is unparked" unresolved (variant-3, Unresolved). The owner gets no guidance for the first time a coordinator does print a sweep reply in chat.
7. **Variant 3 adds tracking overhead.** It adds a deferral row in #534 and admits "One more deferred item to track" (variant-3, Costs).

## Concessions

1. Variant 2 is narrower than #339's wording. Counts plus a path is not a #409-style fleet picture; the person must open the report file (variant-2, Costs). Variant 1 wins on fidelity to the issue text (C-005).
2. The "every 3 minutes" end is not met; the 5-minute cap is a cap, not a schedule (WORKER-CONTRACT.md:109; ADJ line 81). Variant 2 does not fix this.
3. "Until the note exists" has no date; the note waits on other work (variant-2, Costs).
4. Variant 3 is right that no loop exists to print anything recurring (U-003), and its framing fits the owner's "decision ledger only" rule for automated status (merged-requirements.md:1040) more cleanly. A counts-and-path reply after every sweep can read as routine status. Variant 2 depends on the sweep reply being the accepted WC-16 output, not routine chatter; V5 D2 supports that reading (variant-5-original.md:222), but the owner has not stated it.
5. Variant 1's U-002 (flagging Q-1 for the coordinator's own terminal) is a useful risk callout that Variant 2 does not make in its own text.

## Shared assumptions

- **A-001 (no work item, so a wrong answer is cheap to reverse): QUALIFY.** True for Variant 2 (zero edits) and mostly for Variant 3, but Variant 1 implies later edits to WC-16, the skill and the output style, so its reversal cost is not small.
- **A-002 (the contract note will be written, so "until the note" is a real trigger): QUALIFY.** V5 D1 makes the note the "smallest reversible first step" (variant-5-original.md:217), so it is likely, but it is undated; the ledger row should also name a fallback review point (for example when the coordinator loop is built).

## Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | Tie (2 nominal) | 35% | All three use the same five sections; no structural advantage. |
| C-001 | 2 | 70% | One source of facts in chat until the shared word list exists; matches V5 D2 and spec 6.7. |
| C-002 | 2 | 70% | Reopens on one defined trigger (the note), earlier and clearer than Variant 3's two-condition park. |
| C-003 | 2 | 85% | Only variant with zero spec, contract, skill or style edits (merged-requirements.md:1040 already says it). |
| C-004 | 3 | 60% | Variant 3 is most accurate that nothing runs a cadence; Variant 2 is honest about the cap but still implies a slot. |
| C-005 | 1 | 80% | Dashboard-like text is closest to "taking inspiration from #409". |
| X-001 | 2 | 80% | Keep `observe` out of WC-16 and the skill until the note and the Q-1 binding are settled (variant-5-original.md:222). |
| X-002 | 2 | 65% | The sweep reply is already the contracted WC-16 output with a shipped exception (SKILL.md:35-43). |
| X-003 | 2 | 80% | Keeping 6.7 as written avoids a spec edit with no gain. |
| U-001 | 1 | 70% | Correct and useful fact (no-write observer, X-004 at debate-transcript.md:904); it informs the note's later decision. |
| U-002 | 1 | 85% | The Q-1 risk for the coordinator's own terminal is the highest-value unique point and is UNVERIFIED. |
| U-003 | 3 | 80% | The unbuilt loop is a real constraint the other two underplay. |

## Overall ranking and unassigned pick

Ranking, best first: Variant 2, Variant 3, Variant 1.

Unassigned pick: I would still pick Variant 2, because it costs nothing, matches the spec, the shipped skill and V5 D2, and keeps the observer decision behind the contract note where its dependencies belong. It is close to Variant 3; the best merged answer is Variant 2's ruling plus Variant 3's caveat that no 3-to-5-minute cadence is promised until the coordinator loop exists, plus Variant 1's Q-1 check listed as a precondition for ever adding the observer text.
