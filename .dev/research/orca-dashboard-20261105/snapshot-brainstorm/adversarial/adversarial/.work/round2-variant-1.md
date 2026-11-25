# Round 2 Rebuttal: Variant 1 Advocate (opus:architect)

## Response to Criticisms

Line numbers below are for `variant-1-opus-architect.md` (V1), `variant-2-sonnet-analyzer.md` (V2) and `variant-3-haiku-backend.md` (V3). I re-checked each one for this round.

**CR-1. CHG-2 contradicts the busy screen (X-005; V2 W4, V3 W2).** I concede the contradiction. CHG-2 says "A failed or partial collection never supplies a zero baseline; deltas for that source print `n/a (no baseline)`" (V1 l.106). Yet the §6.2 screen shows `msgs CAPPED 100/100` (l.229) and still prints `+ new D-DEMO-0055` and `^ escalated D-DEMO-0042` (l.253-254). §10.2 does the same (l.480, l.484-485).
- Partial counter-evidence: the escalation is "blocks 2 -> 3 direct" (l.254). That is a dependency-count change from the worker and ps sources, which are `ok` (l.229), not an absence deduction from the capped message source.
- Fix: the NEW entry is a positive addition, which is the right behavior, but CHG-2's wording is too broad. V3 §4 rule 4 is the correct replacement: "Partial observations can establish positive additions, but not absence, resolution or negative movement" (V3 l.75).
- I also found a worse case than the critics raised (see New Evidence NE-3).

**CR-2. Decisions-first broken in C and E (X-006; V2 W5).** I concede for C and partly concede for E.
- C: DEC-1 says "Every report shows pending human decisions before any other content" (l.73). Yet C draws `[3] VERIFY` and `[4] FAILURE` (l.371, l.374) above the UNROOTED decisions D-DEMO-0051/0040/0053/0055 (l.376-379).
- E, correction: V2's wording "E's journal leads with non-decision entries" is inaccurate. THIS WINDOW opens with three decision entries (NEW, ESCALATED, AGED, l.484-486).
- E, what remains true: non-decisions do interleave. A VERIFY-GAP (l.487) sits above the still-open VANISHED decision D-DEMO-0040 (l.489). In STILL OPEN, `F T-DEMO-B2` (l.494) sits above decision D-DEMO-0051 (l.495).
- The V3 advocate argues the merge should keep DEC-1 and repair the screens rather than drop the invariant (round1-variant-3 X-006 row). I agree on the remedy. The vote stays with V3 because the defect is V1's own.

**CR-3. A read under the cap is treated as covered (X-003; V2 W6, V3 W1).** I concede the substance and correct the citation.
- Citation: V2 locates the flaw in COV-3. COV-3 actually requires a partial marker for "failed, capped or stale" sources (l.127) and says nothing about under-cap reads.
- The real source is OVF-7: "A capped message read (rows returned equal the cap) marks every decision and thread count `>=N`" (l.684). By implication, a read below the cap is `ok`, as the §12.1 token `msgs ok 37<100cap` shows (l.584).
- V3 is right that "Even fewer than 100 returned messages do not prove complete unresolved history" (V3 l.66).
- Mitigation: V3's advocate concedes that neither V1 nor V2 "should be accused of an unconditional global all-clear". The §12.1 screen still reads `0 observed (partial ...)` (l.587) and "This is not an all-clear: coverage partial." (l.599).
- But the partial reason names only the inbox cursor and hosts, not msgs. If those two gaps closed, V1 could print a complete-coverage state on an under-cap read. That is a real defect (see NE-1 and NE-2).

**CR-4. `w-07` has no DEMO marker (X-010; V2 W7).** I concede. l.17 lists `w-07` as an example of a DEMO identifier, and it appears unprefixed at l.235 and l.362.

**CR-5. Impact-first tree with gate G4 still open (X-002, C-007; V3 W3).** I partly concede.
- Counter-evidence: V1 already conditions C on G4. "If it fails: `blocks ?`; C degrades to its UNROOTED list" (l.754). The coupling table names "Complete task dependency graph" for C (l.546), and C is "Not recommended as default: C (blocked on dependency data)" (l.562).
- Concession: that fallback covers a missing graph, not a partial one. The §8.2 screen ranks roots by impact while it also prints `run-DEMO-C deps ?` (l.381), so the ranking runs on an incomplete graph. V3's age ranking is the safer rule until G4 passes.

**CR-6. Answered items only reach the FLEET line (C-011; V2 KS-8, V3 W4).** I concede for the default. §6.1 deliberately moves them out of NEEDS YOU "because the next actor is no longer the human" (l.219) and keeps them only by key (l.217, l.261). V1 does draw a full ANSWERED, NOT RESOLVED band in concept D (l.408, l.436). That shows the model already carries the data, so V2's band is a renderer-level import.

**CR-7. No drawn overflow screen and no fixture table (S-005, S-007; V2 KS-2, KS-6).** I concede both. V1 has rules OVF-1..8 (l.676-685) and an in-screen `+3 more:` (l.242), but no screen a reviewer can check arithmetic against. Its fixture exists only as reused keys.

**CR-8. No participant count (C-018; V2 KS-9).** I concede. §14 says "No participant has performed these tasks" (l.689) and that thresholds will be revised "once the participant pool ... [is] known" (l.706). No number is given.

**CR-9. Gates can never stop shipping (C-019; V2 KS-10).** I concede the fact and qualify the effect.
- Fact: l.747 says "Failing a gate does not block the default concept; it keeps the corresponding labels in their partial form."
- Qualification: COM-5 reports a consuming source as `unavailable (would consume)` (l.98), so V1 never ships a consuming read.
- Concession: a default with no usable decision source still renders, and its core purpose fails. V2's FG-8 "Cannot ship" is the more honest gate.

**CR-10. Owner stays `human` (A-002; V2 A-002).** I concede. G8's failure branch is "Owner stays `human`" (l.758), and the default's first section is literally named `NEEDS YOU` (l.232). That heading encodes A-002 instead of testing it.

**CR-11. No repeated-token rule and no moving-dataset warning (V3 W7).** I concede. OVF-6 reads "every page the cursor offers within a stated limit" (l.683) and has no rule for repeated or invalid tokens. V3 covers both: "Repeated tokens, invalid tokens, page errors or a collection deadline produce partial coverage" and "Cursor exhaustion alone does not prove a point-in-time census" (V3 l.64).

**CR-12. A derivation layer still needs integrity rules (V3 steelman).** I accept this, and it is the main architectural lesson of this round. The layer model says where a rule is enforced. V3 supplies several rules that belong in layers 1-3 and are missing there: two clocks, cursor integrity, positive-only partial deltas, and census-unknown.

## Updated Assessment

**V2: stronger than I credited on three points, still weakest on structure.**
- Heartbeat suppression: V2's WATCH row (V2 l.251, `last seen 08:49Z (16m, limit 15m)`) puts silence suppression in the default with a printed threshold. My Round 1 credit to V1's QUIET count was misplaced, because QUIET exists only in concept D (V1 l.410), not in the default A. C-008 moves to V2.
- Answered-but-unresolved band and ship gate: still V2, as conceded in CR-6 and CR-9.
- Where V2 stays weak:
  - The read model is "not specified here" (V2 l.537).
  - Its all-clear permission is conditional and is checked mechanically (R-INT-01 V2 l.201, MC-4 V2 l.717).
  - Its under-cap token `msg-peek OK 22/100` (V2 l.583) has the same flaw as V1's.
  - Its own advocate concedes X-007, X-008 and X-009.
- My Round 1 critique of V2's conditional all-clear applies to V1 too (NE-2), so I no longer treat X-004 as a V1 advantage over V2. It is a V3 advantage over both.

**V3: its observation contract is the best of the three, and it fits inside V1's layers.**
- V3's advocate frames V3 as the "observation and data-integrity contract", not the whole design. The advocate concedes V3's frame, overflow screen, concept distinctness and decisions-first order (round1-variant-3 Concessions 1-4). I agree with each of those concessions.
- Every V3 integrity rule I now accept maps onto a V1 layer:
  - two clocks and paging (V3 l.64), into layer 1, collector adapters;
  - per-source/scope last-success pointers and positive-only partial deltas (V3 l.75), into layer 2, the observation store;
  - `decision census unknown` (V3 l.66, l.301), into layer 3, derivation.
- None of them changes a renderer. That is the case for V1 as the skeleton: V1's errors in this round are rule errors at layers 2-3, not structural ones. The layer model localizes each fix to one place (V1 R-8, l.740).

**Where I now stand on the merge.**
- V1 supplies the layer model, the frame with OLDEST and legend, DEC-1 (repaired screens), five distinct concepts and the coupling table.
- V3 supplies the layer 1-3 integrity rules and the empty-state wording.
- V2 supplies the fixture, overflow screen, ANSWERED band, WATCH row, evaluation protocol and the ship gate.
- My votes moved toward V3 on five points (C-006, C-012, C-020, X-004, A-001) and toward V2 on one (C-008).

## New Evidence

**NE-1. V1 already holds V3's census position at the limits level, so the X-003 fix is local.** §15 says "Decision counts are lower bounds (`>=N`) until a complete, non-consuming decision source is verified (gate G1)" (V1 l.713). G1's failure branch is "Keep `>=N` and 'oldest observed' permanently" (l.751). OVF-7's rows-equal-cap trigger (l.684) and the under-cap `msgs ok` tokens (`37<100cap` l.584, `12<100cap` l.647) contradict V1's own limits section. Remedy: change OVF-7's trigger to "until G1 passes" and make the msgs token `ok 37/100cap, census ?`. Nothing in layer 4 changes.

**NE-2. COV-4 has the same conditional shape I criticized in V2 (against V1).** COV-4's first sentence permits "`all clear` (or any equivalent green summary)" when "every source is `ok`, complete and fresh" (l.128). Only the default renderer is barred, and the best-case state it permits is "`no attention items observed; coverage complete`" (l.128). Combined with OVF-7, a non-default renderer could print an all-clear, and the default could print "coverage complete", on an under-cap message read. V3's empty state never goes beyond scope: "FAILURES: none observed. This is not a fleet-wide all-clear." and "NO WORK OBSERVED IN SCOPE; decision census unknown." (V3 l.306, l.301). This is why X-004 and C-012 move to V3.

**NE-3. A VANISHED under a capped read is an absence inference (against V1, not raised by the critics).** §6.2 prints `! vanished D-DEMO-0040 not re-seen, no resolution observed: kept open` (l.256) while msgs is `CAPPED 100/100` (l.229). Under a cap, "not re-seen" may only mean "beyond the cap". V1 does keep the item open and never infers resolution (DEC-6, l.78), so the error is limited to the label. Under V3 rule 4 (V3 l.75), the entry should read `not re-seen (msgs capped; may be unread)`, or be suppressed as a delta while the item stays carried. C-010 stays V1 because V1 alone makes disappearance a testable delta kind (CHG-3 l.107, EV-8 l.702). The merge should add this qualifier.

**NE-4. V1's model already separates paging from overflow, the base for V3's four-way accounting.** OVF-5 says "Overflow is 'observed but not printed'; paging coverage is 'not observed because the source was capped or not fully paged'... Both can be non-zero at once" (l.682). V3's observed / shown / omitted / unobserved split (V3 §4 rules 7-9) is a refinement of OVF-5, not a competing structure.

**NE-5. V3's candidate-question rule answers A-001 better than anything in V1.** "a deterministic source/run/thread/message reference may identify an **observed candidate question**, but cannot establish a durable census or a resolution relation. If even that reference is unavailable, label identity uncertain" (V3 l.60). An ambiguous message stays visible as a candidate instead of being folded into a last-seen time (V1 COM-4, l.97). A-001 moves to V3.

**NE-6. EV-10 checks width, not message size.** EV-10 is "Width check: paste each screen into the target chat client at 80 columns" (l.704), and OVF-8 is "a design target, not a measured constraint" (l.685). V1 tests the 80-column half of A-003 but not the per-message limit. That is still more than V2 (which "No chat client was tested") or V3 (whose 44-line target yields to whole bundles) offer. It is not proof that a paste fits.

## Shared Assumption Responses

- **A-001: QUALIFY (unchanged; superior moves from V1 to V3).** Suppression is safe only for positively identified routine traffic. V1's QUIET count exists only in concept D (V1 l.410), and the default A applies COM-4 silently (l.97). So my Round 1 credit to V1 was wrong. The merge should combine two pieces:
  - V3's candidate-question and identity-uncertain rule (V3 l.60), so an ambiguous message stays visible;
  - V2's printed-threshold WATCH row (V2 l.251), so silence suppression is visible.
  No variant defines the classifier itself.
- **A-002: QUALIFY (unchanged).** The assumption holds for one operator in one chat and fails for several. V1's own heading `NEEDS YOU` (l.232) and its G8 failure branch "Owner stays `human`" (l.758) build the assumption in. §15 admits "The report cannot tell whether a particular person has seen, claimed or snoozed an item" (l.714). V3's acting-owner / requester split with unknown fallback (V3 l.60) is the right data rule. A heading such as NEEDS YOU must not be read as an assignment. I stay at QUALIFY rather than the V3 advocate's REJECT because the single-operator case is the seed's stated use.
- **A-003: QUALIFY (unchanged).** No platform limit is named anywhere. V1 has fixed per-section budgets with keyed overflow (OVF-1..3, l.678-680) and a width check (EV-10, l.704). Those bound the line count and the width, but not the byte size, and OVF-8 is "not a measured constraint" (l.685). The footer that carries omitted and coverage counts must survive a split. That is still unverified for all three.
- **A-004: QUALIFY (unchanged).** V1 prints as-of, prev-ok and "(sample, not an alert)" in every header (l.227). Its TRAIL (l.499-502) exists only in concept E. V3's two clocks are stronger: "A successful fetch of an old liveness record is not a fresh liveness observation" (V3 §3). No variant defines a reader-side validity boundary or a paste sequence number.

## Per-Point Verdict Table

| Point | Superior | Reason (one line, with a section citation) |
|-------|----------|--------------------------------------------|
| S-001 | V1 | Model, frame, concepts, overflow and gates are separate sections, so each changes alone (V1 s.2-s.4, s.13, s.17). |
| S-002 | V1 | Only layer model with owns / must-never; every V3 integrity rule fits into layers 1-3 without a renderer change (V1 s.2, R-8). |
| S-003 | V1 | Layer column states where each rule is enforced (V1 s.3); V2's Basis column is a close second, V3's R01-R16 are flat. |
| S-004 | V1 | One mandatory header/footer contract for every concept (V1 s.4.1-s.4.2); V3's advocate concedes this (V3 has none standalone). |
| S-005 | V2 | Explicit fixture-world table reused by every screen (V2 s.2.6); V1 only implies one through reused keys. |
| S-006 | V2 | Concept x state matrix names residual false-all-clear risk for every concept (V2 s.8). |
| S-007 | V2 | Only dedicated overflow screen with printed arithmetic (V2 s.7.1); V1 has rules OVF-1..8 but no screen. |
| S-008 | V1 | +/o/- matrix plus a data-dependency table that ties each concept to its open gate (V1 s.11.1-s.11.2). |
| S-009 | V2 | Reader tasks, mechanical checks and a decision rule are separate (V2 s.9.1-s.9.3). |
| S-010 | V2 | Gates carry closing evidence, affected concepts and a next step (V2 s.12.1, s.12.3). |
| S-011 | V1 | Legend printed as a footer in every report, so notation is readable in chat (V1 s.4.1, s.4.3). |
| S-012 | V1 | One fixed frame grammar across all five renderers (V1 s.4.1, s.6.2). |
| C-001 | V2 | Ball-Holder bands use the responsibility axis, the most distinct second organizing axis (V2 s.4.2). |
| C-002 | V1 | Queue, matrix, tree, ladder and journal differ in structure; V3's advocate concedes repeated bundles (V1 s.5-s.10). |
| C-003 | V2 | Hybrid default with named borrowings and a test-gated switch rule (V2 s.6, s.9.3). |
| C-004 | V1 | Mandatory `OLDEST` frame line keeps the success criterion in every concept (V1 DEC-3, s.4.2). |
| C-005 | V3 | `observed >=Nm`, an oldest-not-certified warning and `clock conflict` (V3 s.4 rule 1). |
| C-006 | V3 | `decision census unknown` holds below the cap; V1 OVF-7 marks `>=N` only at the cap, against its own s.15 (changed from V1). |
| C-007 | V3 | Age-ranked roots, union counts and `dependency conflict` for cycles work on a partial graph (V3 s.4 rule 6, s.7). |
| C-008 | V2 | Printed-threshold WATCH row in the default; V1's QUIET count is only in concept D (V2 s.4.1; V1 s.9.1) (changed from V1). |
| C-009 | V3 | Per-source/scope baselines; partial reads add but never prove absence (V3 s.4 rules 4-5). |
| C-010 | V1 | VANISHED is an explicit, testable delta kind kept open (V1 CHG-3, DEC-6, EV-8); add V3's capped-read qualifier. |
| C-011 | V2 | ANSWERED, NOT RESOLVED band in the default; V1 keeps it only by key in FLEET (V2 s.4.1; V1 s.6.1). |
| C-012 | V3 | "NO WORK OBSERVED IN SCOPE; decision census unknown" names the gap V1's under-cap token hides (V3 s.10) (changed from V1). |
| C-013 | V3 | Full last-known bundles under "not confirmed current" with a banner and unknown current count (V3 s.10). |
| C-014 | V3 | Missing, stale, wrong-revision and failing checks get distinct labels with provenance (V3 s.10, s.11). |
| C-015 | V1 | y/n/? ladder without a permanently unknown human-seen column, plus `unavailable (would consume)` (V1 COM-2, COM-5). |
| C-016 | V2 | Hard line budget with printed shown + omitted = observed arithmetic (V2 R-OVF-01, s.7.1). |
| C-017 | V3 | Exact question, wrap rather than clip, and marked secret redaction (V3 R03, R16, s.4 rule 10). |
| C-018 | V2 | At least 8 participants, thresholds, critical-failure rules and mechanical checks; V1 gives no count (V2 s.9; V1 s.14). |
| C-019 | V2 | FG-8 "Cannot ship" binds; V1's gates never block the default (V2 s.12.1; V1 s.17). |
| C-020 | V3 | Every id DEMO-prefixed and max line 70; V1's `w-07` breaks its own naming rule (V3 s.1; V1 s.1) (changed from V1). |
| X-001 | V1 | Human decisions lead the default; V3 puts worker-owned VERIFY above DEMO-D2 (V1 DEC-1; V3 s.5); V3's advocate agrees. |
| X-002 | V3 | Rank roots by age until a complete graph exists; V1 ranks by impact on a partial graph (V3 s.7; V1 s.8.2). |
| X-003 | V3 | Fewer than 100 returned messages do not prove completeness (V3 s.3); V1's flaw is OVF-7, not COV-3. |
| X-004 | V3 | Never fleet-wide; V1 COV-4 permits all-clear in non-default renderers on a condition (V3 s.10; V1 COV-4) (changed from V1). |
| X-005 | V3 | Positive-only partial additions resolve V1's CHG-2 vs CAPPED-with-deltas conflict (V3 s.4 rules 4-5; V1 s.6.2, s.10.2). |
| X-006 | V3 | V1's C and E place verify/failure items above pending decisions (V1 s.8.2, s.10.2); keep DEC-1 and repair the screens. |
| X-007 | V3 | V3's screens follow its own ordering rule, unlike V2's C3 and C5 (V3 s.5-s.10; V2 s.4.3, s.4.5). |
| X-008 | V3 | Every V3 identifier carries DEMO, unlike V2's `w-07` and `M-201` (V3 s.1; V2 s.4, s.7). |
| X-009 | V3 | Union counting with an overlap note under each root is the rule to retain and test (V3 s.4 rule 6, s.11). |
| X-010 | V3 | DEMO prefix on every worker id; V1's `w-07` contradicts its own example list (V3 s.1; V1 s.1). |
| A-001 | V3 | Candidate-question and identity-uncertain rule keeps ambiguous messages visible (V3 s.3) (changed from V1). |
| A-002 | V3 | Acting owner and requester kept apart, missing owner stays unknown (V3 s.3, G05). |
| A-003 | V1 | Fixed section budgets, about 40 lines at 78 columns, plus a paste width check (V1 OVF-1..3, OVF-8, EV-10). |
| A-004 | V3 | Two clocks; a new paste does not make old observations fresh (V3 s.3). |
