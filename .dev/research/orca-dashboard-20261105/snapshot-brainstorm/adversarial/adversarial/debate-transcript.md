# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2, plus Round 2.5 invariant probe (Round 3 skipped: depth=standard)
- Convergence achieved: 95.7% diff-point agreement (44/46); status BLOCKED_BY_INVARIANTS (5 HIGH-severity UNADDRESSED invariants)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (V1 opus:architect, V2 sonnet:analyzer, V3 haiku:backend)
- Scored points: 46 (S-001..S-012, C-001..C-020, X-001..X-010, A-001..A-004 from diff-analysis.md)
- Agreement rule: a point is agreed when at least 2 of 3 advocates name the same superior variant in their per-point verdict tables (tallied by `.work/tally.py`)
- Full advocate texts: `.work/round1-variant-{1,2,3}.md`, `.work/round2-variant-{1,2,3}.md`

## Round 1: Advocate Statements

Round 1 ran in parallel: each advocate saw only the variants and diff-analysis.md, not the other statements. Round 1 convergence: 42/46 = 0.913 (unresolved: S-003, C-012, A-001, A-003).

Caveat: the V2 advocate wrote its Round 1 section citations without re-opening the variant files. Its Round 2 instructions required it to re-verify every citation; corrections appear in `.work/round2-variant-2.md`.

### Variant 1 Advocate (opus:architect)

**Position Summary:** V1 is the only variant that makes the honesty rules part of the structure rather than repeating them on every screen. It has a four-layer model with owns / must-never rules, Layer-tagged requirements, a shared frame, the OLDEST line and a data-dependency table. The merged spec should keep V1's skeleton, take V3's observation-integrity rules, and take V2's evaluation, overflow screen and concept x state matrix.

**Steelman of V2:** V2 is the most decision-ready document: every claim is tagged [E], [P] or [G]; the Ball-Holder concept organizes by responsibility; its hybrid default has a test-gated switch rule; it has a dedicated overflow screen, a concept x state matrix, a fixture table, a sized evaluation and a binding "Cannot ship" gate.

**Steelman of V3:** V3 is the most rigorous about what an observation can prove: an observation envelope, two clocks kept apart, "completion means a successful terminal page", partial reads establish additions but never absence, `observed >=Nm` and `clock conflict` fallbacks, age-ordered roots with `dependency conflict`, secret redaction, deterministic contract cases and the best stale screen.

**Strengths claimed:**
1. The structure enforces honesty, so a new renderer cannot print an all-clear (s.2).
2. Every requirement has an owning layer (s.3).
3. One frame contract with a printed legend for every concept (s.4).
4. The OLDEST line is in every concept (DEC-3).
5. Never prints an all-clear (COV-4, s.12).
6. Partial totals are never summed (s.7.2); VANISHED changes and no zero baseline from a failed read (CHG-2, s.10).
7. Reports `unavailable (would consume)` (COM-5); a pass on an older revision does not count (VER-3).
8. Data-dependency table drives the default choice (s.11.2-11.3).
9. Most conservative size budget: 78 columns, about 40 lines, paste check (FMT-2, OVF-8, EV-10).

**Weaknesses identified:**
- V2 has no specified model (s.6).
- V2 allows a conditional all-clear (R-INT-01) and treats a read under the cap as complete (s.7.2).
- V2 has no fallback for a missing creation time.
- V2's C3 and C5 do not lead with decisions, and C5 has no oldest pointer.
- V2 has DEMO-marker misses (`w-07`, `M-201`) and an ambiguous stale clock.
- V3's concepts are near-duplicates.
- V3 puts a worker-owned check above a human decision (X-001).
- V3 has no frame contract or legend, flat requirements, prose-only overflow and a five-operator evaluation.

**Concessions:**
- Its busy screen contradicts CHG-2 (X-005).
- Concepts C and E violate DEC-1 (X-006).
- `w-07` lacks the DEMO marker (X-010).
- `msgs ok 37<100cap` overstates completeness (X-003).
- Impact ranking of roots (C-007).
- Incomplete `seen>=` (C-005).
- No cursor-integrity rule, cycle handling or redaction.
- Thinner overflow, fixture and evaluation than V2.
- No answered-not-resolved band (C-011).
- No switch rule for the default (C-003).
- Five renderers have a real drift cost.

### Variant 2 Advocate (sonnet:analyzer)

**Position Summary:** V2 is the variant that can be checked: per-claim [E]/[P]/[G] tags, one fixture table behind every screen, and a concept x state matrix that admits its gaps. It should supply evidence discipline, the fixture, overflow arithmetic, the evaluation protocol and the hybrid default. V1 should supply the layer model, frame and OLDEST line, and V3 the two-clock, paging and partial-observation rules.

**Steelman of V1:** V1 is the best-structured spec: four layers with owns / must-never, a Layer column on all 39 requirements, a shared frame with OLDEST, as-of and legend lines, `seen>=`, VANISHED, distinct-task root ranking, 78-column content and a never-print all-clear policy.

**Steelman of V3:** V3 is the most rigorous about collector knowledge: two-clock freshness, `clock conflict`, paging integrity, partial reads that never establish absence, rejection of "fewer than 100" as proof of completeness, `dependency conflict`, redaction, four verification labels and a 70-column maximum.

**Strengths claimed:**
1. Auditable per-claim evidence tags mapped to gates FG-1..FG-8 (s.1, s.12.1).
2. One fixture world for all screens and states (s.2.6).
3. Five distinct concepts compared with line counts and gate load (s.5).
4. Ball-Holder responsibility axis (s.4.2).
5. Concept x state matrix that admits the C4/C5 gap (s.8).
6. Overflow screen with printed arithmetic (s.7.1).
7. Visible heartbeat suppression through WATCH rows.
8. ANSWERED, NOT RESOLVED band.
9. An evaluation that can fail the design (s.9).
10. A "Cannot ship" gate (FG-8).
11. Decisions-first stated as a rule (R-DEC-01).

**Weaknesses identified:**
- V3 lets a pinned non-decision outrank a waiting human decision (X-001).
- V3's concepts are near-duplicates, with no comparison matrix and no overflow screen.
- V1's busy screen contradicts CHG-2 (X-005).
- V1's non-default concepts break DEC-1 (X-006).
- V1 builds the under-cap read into COV-3 (X-003).
- V1's `w-07` lacks the DEMO marker.
- V3 ranks roots by age only.

**Concessions:**
- C3 and C5 violate R-DEC-01 (X-007).
- DEMO-marker misses (X-008) and a shared-task marker miss (X-009).
- Same under-cap blind spot (X-003).
- No `seen>=` fallback.
- No VANISHED kind and no OLDEST outside C1.
- No layer model.
- No printed legend or footer contract.
- No two-clock, cursor, cycle or redaction rules.
- An 80-column line with zero margin.
- Arbitrary thresholds.
- A conditional all-clear is riskier than never printing one (X-004).

### Variant 3 Advocate (haiku:backend)

**Position Summary:** V3 should supply the observation and data-integrity contract: a successful read is not a complete census, comparisons need compatible scope, and conflicting evidence never becomes readiness (s.3-4). Its presentation is not the strongest: keep V1's frame and visibly distinct concepts, and V2's overflow demonstration, ownership treatment and evaluation.

**Steelman of V1:** Truth rules must survive a layout change. Its layers assign owners and prohibitions, the OLDEST line protects the main success criterion, the dependency table exposes prerequisites, and its five concepts are genuinely different whole-report organizations.

**Steelman of V2:** Evidence and interpretation both get explicit checks: [E]/[P]/[G] tags, the Ball-Holder responsibility axis with admitted inference risk, overflow arithmetic, the concept x state matrix, separate reader tasks and mechanical checks, and the FG-8 "Cannot ship" gate.

**Strengths claimed:**
1. A returned page is not a census, even under the cap (s.3).
2. Defined paging and authority failure outcomes.
3. Per-source and per-scope comparison, where partial reads add but never subtract (s.4 rules 4-5).
4. Freshness measures the evidence, not the transport.
5. Cross-source disagreement stays visible, with distinct verification labels.
6. Overflow omits whole bundles with full accounting.
7. Failure cases specified in advance (s.11).
8. Redaction and escaping of source text (R16).

**Weaknesses identified:**
- V1 and V2 show under-cap reads as complete.
- V1's busy screen contradicts CHG-2.
- V1's impact-first tree depends on an open gate (G4).
- V1's default pushes answered items into FLEET.
- V2's owner field can name the relay rather than the actor.
- V2's section 5 conformance claim is too broad.
- Neither rival has repeated-token or moving-dataset semantics.

**Concessions:**
- Concepts are not visibly distinct enough (C-002).
- No reusable frame or printed legend.
- No drawn overload screen.
- A worker-owned verification sits above a human decision (X-001).
- The Run Ledger puts inventory before action.
- The 44-line target does not prove transport safety.
- Heartbeat classification, ownership, retention, severity and redaction still need operational definitions.

### Shared Assumption Responses (Round 1)

| Point | V1 | V2 | V3 |
|---|---|---|---|
| A-001 heartbeat vs decision separable | QUALIFY | QUALIFY | QUALIFY |
| A-002 chat reader is acting owner | QUALIFY | QUALIFY | REJECT |
| A-003 40-60 line paste fits chat limit | QUALIFY | QUALIFY | QUALIFY |
| A-004 readers act on latest paste near as-of | QUALIFY | QUALIFY | REJECT |

No advocate accepted any shared assumption.

## Round 2: Rebuttals

Round 2 ran sequentially: V1, then V2 (with V1's rebuttal), then V3 (with both). All three advocates re-opened the variant files and cited by line number.

### Variant 1 Rebuttal (opus:architect)

**Conceded:**
- CR-1: CHG-2 contradicts the busy screen (X-005). V3 §4 rule 4 is the replacement wording.
- CR-2: decisions-first is broken in concept C, and only partly in E. E opens with decision entries, so V2's Round 1 wording was inaccurate, but non-decisions interleave below them.
- CR-3: the under-cap read (X-003). Citation corrected: the source is OVF-7 (V1 l.684), not COV-3.
- CR-4: `w-07` has no DEMO marker.
- CR-6: answered items leave the default's attention area. V1's concept D shows the model already carries the data.
- CR-7: no drawn overflow screen and no fixture table.
- CR-8: no participant count.
- CR-9: gates never stop shipping (l.747). COM-5 still prevents a consuming read.
- CR-10: the `NEEDS YOU` heading encodes A-002.
- CR-11: no repeated-token or moving-dataset rule.
- CR-12: the layer model needs V3's integrity rules in layers 1-3.

**Partly held:** CR-5. V1 conditions concept C on gate G4, but the §8.2 screen still ranks roots by impact on an incomplete graph. V3's age ranking is safer until G4 passes.

**New evidence:**
- NE-1: V1 §15 and G1 already hold the census-unknown position, so the X-003 fix is local (OVF-7 trigger, msgs token).
- NE-2: COV-4 is conditional, just like V2's R-INT-01, so X-004 and C-012 move to V3.
- NE-3: a VANISHED entry under a capped read is an absence inference. It needs a "may be unread" qualifier.
- NE-4: OVF-5 is the base for V3's four-way accounting of observed, shown, omitted and unobserved.
- NE-5: V3's candidate-question rule answers A-001 best.
- NE-6: EV-10 checks width, not message size.

**Updated position:** The merge should use V1 as the skeleton (layers, frame with OLDEST and legend, DEC-1 with repaired screens, five distinct concepts, coupling table). It should take V3's layer 1-3 integrity rules and empty-state wording. From V2 it should take the fixture, overflow screen, ANSWERED band, WATCH row, evaluation protocol and ship gate.

**Votes changed:** five toward V3 (C-006, C-012, C-020, X-004, A-001) and one toward V2 (C-008).

### Variant 2 Rebuttal (sonnet:analyzer)

**Conceded:**
- CR-1: `msg-peek OK 22/100` treats an under-cap read as complete.
- CR-2: R-INT-01 contradicts V2's own §7.2. This is new and was found on re-read.
- CR-3: the conditional all-clear. X-004 moves to V3.
- CR-4: C3 and C5 break decisions-first. C-004 stays with V1's OLDEST line.
- CR-5: `w-07` and `M-201` have no DEMO marker. This is a draw with V1.
- CR-6: the shared-task marker is missing in one row. X-009 moves to V3.
- CR-7: the §5 "all five carry these" claim over-reaches.
- CR-8: the owner field names the relay, not the human.
- CR-9: no cursor-integrity or moving-dataset semantics.
- CR-10: no creation-time fallback, no printed legend and no layer model.
- CR-11: the 80-column zero margin and no tested client.
- CR-12: "(by timestamp)" names no clock.

**Held:**
- WATCH row in the default.
- Shared fixture.
- 19-decision overflow screen with printed arithmetic.
- Concept x state matrix.
- ET/MC split and decision rule.
- FG-8 "Cannot ship".
- Hybrid default with a switch rule.

**New evidence (citation corrections to Round 1):**
- NE-1: V1's under-cap flaw is in OVF-7, not COV-3.
- NE-2: E's journal does not lead with non-decisions.
- NE-3: TRAIL is in concept E only, so the A-004 credit is withdrawn. DEC-5 is at V1 l.77.
- NE-4: its other Round 1 citations were re-checked and are correct.
- NE-5: V3's empty screen asserts "Missing in-scope hosts: none" although G04 admits no host inventory exists.
- NE-6: V3 has no drawn overflow screen and no printed legend.

**Updated position:** V2 is the review and validation surface of the merge, not its skeleton (V1) and not its data contract (V3). V2's mockups need repair against R-DEC-01, R-INT-04 and §2.4. Its R-INT-01 versus §7.2 conflict must be fixed before R-INT-01 is reused.

**Votes changed:** eight. C-006, C-012, C-020, X-004, X-009, A-001 and A-004 moved to V3; C-015 moved to V1.

### Variant 3 Rebuttal (haiku:backend)

**Conceded:**
- CR-1: the concepts are too similar (C-002). C-001 moves to V2's responsibility bands; the run reconciliation stays as supporting content.
- CR-2: a worker verification sits above a human question (X-001). Rejected the claim that oldest findability depends on severity: V3 §4 rule 2 keeps an `oldest observed` pointer on any override.
- CR-3: no reusable frame or printed legend.
- CR-4: flat R01-R16 have no owning layer. Kept the acceptance-condition contribution (S-003 stays V3).
- CR-5: no drawn overload fixture for E06.
- CR-6 (partly): a five-operator pilot cannot pick a winning default. S-009 moves to V2. V2's §6 switch rule and §9.3 selection rule must be reconciled.
- CR-7: no comparison matrix.
- CR-8: the six-bundle, 44-line target is not a transport bound. C-016 stays V3 for omission semantics only; the merge needs a verified transport limit.
- CR-10 (qualified): `Missing in-scope hosts: none` needs evidence that the expected in-scope set was fully checked; otherwise it is unknown.
- CR-11: Run Ledger puts inventory before action; no visible answered-unresolved band; heartbeat classification, ownership source, retention, severity and redaction remain undefined.

**Held:**
- CR-9: age-first root ranking is a cost, not a reason to rank incomplete impact estimates (X-002).
- X-006 and X-007 stay with V1: repair the alternate screens rather than adopt V3's mixed default order.

**New evidence:**
- NE-1: V3's candidate-question rule identifies a candidate but does not classify ambiguous messages. Ambiguity-preserving classification is a new merge requirement.
- NE-2: the overlap rule is specified but not drawn or tested; V3's fixture has no two decisions sharing a task.
- NE-3: a VANISHED label under a capped read is still an absence inference; keep last-known unresolved with a coverage qualifier (C-010 stays V3).
- NE-4: the Round 2 source corrections narrow, not overturn, the Round 1 criticisms.
- NE-5: local completeness and global census are separate claims; keep the `decision census unknown` warning.

**Shared assumptions:** A-001 QUALIFY, A-002 REJECT, A-003 QUALIFY (V2 least assumptive), A-004 REJECT (no original variant supplies a reader-side recheck rule).

**Updated position:** No single winning variant. V1 supplies boundaries and presentation contracts, V3 supplies observation integrity inside V1's layers, V2 supplies review and evaluation.

**Votes changed:** three. S-009 and C-001 moved to V2; A-002 moved to V3.

## Round 2.5: Invariant Probe

An independent fault-finder (quality-engineer, not an advocate) probed the Round 2 consensus in six categories. Full table: `invariant-probe.md`.

- Total findings: 30. ADDRESSED: 8. UNADDRESSED: 22 (HIGH 5, MEDIUM 13, LOW 4).
- HIGH UNADDRESSED (blocking):
  - INV-005 (guard_conditions): no classifier or safe fallback separates routine heartbeats from decision requests (A-001); a misclassified decision is hidden.
  - INV-006 (guard_conditions): V2 MC-4 validates the conditional all-clear of R-INT-01, and V1 COV-4 still permits all-clear outside the default, contradicting the X-004 outcome.
  - INV-010 (count_divergence): the line budgets (V1 about 40, V3 44 yielding, V2 60 hard) are not reconciled, and A-003 is unresolved; a split or truncated paste drops the footer that carries omitted and coverage counts.
  - INV-026 (sufficiency_challenge): the OLDEST line plus `decision census unknown` does not by itself find the oldest blocking decision; with a 100-message cap and no paging the oldest can sit outside the window on every run, and an A-001 misclassification removes it before ranking.
  - INV-028 (sufficiency_challenge): the scope-qualified empty state does not by itself resolve X-004; its coverage disclaimer is in the footer, which a split, truncated or stale paste loses.
- MEDIUM UNADDRESSED (warning, not blocking): INV-001, INV-002, INV-003, INV-004, INV-007, INV-011, INV-018, INV-020, INV-021, INV-022, INV-023, INV-024, INV-027.

```
CONVERGENCE BLOCKED: 5 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-005, INV-006, INV-010, INV-026, INV-028
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```
WARNING: 13 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-002, INV-003, INV-004, INV-007, INV-011, INV-018, INV-020, INV-021, INV-022, INV-023, INV-024, INV-027
These items do not block convergence but should be reviewed.
```

No further debate round is available at depth=standard, and the orchestrator does not accept risk on the caller's behalf. The blocking items are carried into the refactor plan as required changes and reported in the return contract.

## Round 3: Final Arguments

Round 3 skipped: depth=standard.

## Scoring Matrix

Votes are listed V1 advocate / V2 advocate / V3 advocate (Round 2). Confidence: unanimous 95, majority 70, unresolved 50; plus 5-10 when a losing advocate explicitly conceded the point (cap 100). A-001 is set to 90 because the winning advocate itself states the rule is incomplete (V3 Round 2 NE-1).

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | V1 | 70% | Votes V1/V2/V1. Model, frame, concepts, overflow and gates are separate sections (V1 s.2-4, s.13, s.17). |
| S-002 | V1 | 95% | Unanimous. Owns / must-never layer boundaries are the best skeleton (V1 s.2). |
| S-003 | UNRESOLVED | 50% | Votes V1/V2/V3: Layer column, Basis column and acceptance conditions each preferred. V3 Round 2 CR-4 proposes keeping all three together. |
| S-004 | V1 | 100% | Unanimous; V3 conceded no frame (CR-3). One mandatory header/footer contract (V1 s.4.1-4.2). |
| S-005 | V2 | 100% | Unanimous; V1 conceded no fixture table (CR-7). Explicit fixture with ages, overlap and answered-unresolved work (V2 s.2.6). |
| S-006 | V2 | 95% | Unanimous. Concept x state matrix names residual false-all-clear risks (V2 s.7-8). |
| S-007 | V2 | 100% | Unanimous; V1 CR-7 and V3 CR-5 conceded. Dedicated overflow screen prints 3 shown + 16 omitted = 19 (V2 s.7.1). |
| S-008 | V1 | 80% | Votes V1/V2/V1; V3 conceded no matrix (CR-7). Ratings plus data-dependency table tied to open gates (V1 s.11.1-11.2). |
| S-009 | V2 | 100% | Unanimous; V3 conceded (CR-6, changed vote). Reader tasks, mechanical checks and a selection rule (V2 s.9); keep V3 contract cases. |
| S-010 | V2 | 95% | Unanimous. Gate table with closing evidence and affected concepts (V2 s.12.1). |
| S-011 | V1 | 100% | Unanimous; V2 CR-10 and V3 CR-3 conceded no printed legend. Legend printed in every snapshot (V1 s.4.1-4.3). |
| S-012 | V1 | 70% | Votes V1/V1/V3. One fixed frame grammar across all concepts (V1 s.4.1, s.6.2); V3 prefers fewer separators. |
| C-001 | V2 | 100% | Unanimous; V3 conceded (CR-1, changed vote). Responsibility bands are the most distinct second axis (V2 s.4.2). |
| C-002 | V1 | 80% | Votes V1/V2/V1; V3 conceded near-duplicate concepts (CR-1). Queue, matrix, tree, ladder and journal differ in structure (V1 s.5-10). |
| C-003 | V2 | 100% | Unanimous; V1 conceded no switch rule. Hybrid default with a test-gated switch (V2 s.6, s.9.3); the two switch rules must be aligned. |
| C-004 | V1 | 100% | Unanimous; V2 conceded no OLDEST outside C1. DEC-3 and the mandatory OLDEST frame line (V1 s.3.1, s.4.2). |
| C-005 | V3 | 100% | Unanimous; V1 conceded incomplete `seen>=`, V2 conceded no fallback. Age bounds, uncertifiable-oldest warning and `clock conflict` (V3 s.4 rule 1). |
| C-006 | V3 | 100% | Unanimous; V1 CR-3 and V2 CR-1 conceded under-cap completeness. Worker coverage and decision census reported separately (V3 s.3). |
| C-007 | V3 | 95% | Unanimous; V1 partly holds impact ranking once G4 passes (CR-5). Age-ranked roots, union counts, cycle conflict (V3 s.4, s.7). |
| C-008 | V2 | 95% | Unanimous. Default WATCH row prints the silence threshold (V2 s.2.4, s.4.1); it does not classify messages. |
| C-009 | V3 | 95% | Unanimous. Per-source and per-scope baselines; partial reads add only (V3 s.4 rules 4-5). |
| C-010 | V1 | 70% | Votes V1/V1/V3. VANISHED is an explicit, testable delta kind (V1 CHG-3, DEC-6); all three advocates require V3's capped-read qualifier (V1 NE-3, V3 NE-3). |
| C-011 | V2 | 100% | Unanimous; V1 conceded (CR-6). ANSWERED, NOT RESOLVED band keeps the item in the attention area (V2 s.4.1, s.6). |
| C-012 | V3 | 100% | Unanimous; V1 NE-2 and V2 CR-3 conceded conditional all-clear. Named-scope absence kept distinct from fleet health (V3 s.10); host line needs evidence (V3 CR-10). |
| C-013 | V3 | 70% | Votes V3/V2/V3. Full last-known bundles under a not-confirmed-current banner (V3 s.10). |
| C-014 | V3 | 95% | Unanimous. Unavailable, stale, mismatched and failed checks stay distinct with revision provenance (V3 s.3, s.10-11). |
| C-015 | V1 | 95% | Unanimous. y/n/? transport and resolution ladder without a human-seen column (V1 s.9.1, s.15). |
| C-016 | V2 | 80% | Votes V2/V2/V3; V3 conceded its size target is not a bound (CR-8). Hard line budget with printed arithmetic (V2 R-FMT-03, R-OVF-01, s.7.1); keep V3 whole-bundle omission. |
| C-017 | V3 | 100% | Unanimous; V1 conceded no redaction. Wrapping, escaping and marked redaction (V3 R03, R16, s.4 rule 10). |
| C-018 | V2 | 95% | Unanimous. Reader/mechanical split, sample reporting and critical failures (V2 s.9). |
| C-019 | V2 | 100% | Unanimous; V1 conceded gates never stop shipping (CR-9). Non-consuming production is a Cannot-ship gate (V2 s.12.1 FG-8). |
| C-020 | V3 | 100% | Unanimous; V1 CR-4 and V2 CR-5 conceded DEMO-marker misses. Consistent DEMO-marked references (V3 s.1, s.5-10). |
| X-001 | V1 | 80% | Votes V1/V2/V1; V3 conceded (CR-2). Human decisions lead the default (V1 DEC-1); V3 puts worker VERIFY above DEMO-D2. |
| X-002 | V3 | 95% | Unanimous. Rank by age while graph coverage is incomplete (V3 s.7). |
| X-003 | V3 | 100% | Unanimous; V1 CR-3 and V2 CR-1 conceded. Fewer than the cap does not prove complete history (V3 s.3). |
| X-004 | V3 | 100% | Unanimous; V1 NE-2 and V2 CR-3 conceded. Scope-qualified absence never becomes fleet-wide all-clear (V3 s.10). |
| X-005 | V3 | 100% | Unanimous; V1 conceded (CR-1). Positive-only partial additions (V3 s.4 rules 4-5). |
| X-006 | V3 | 80% | Votes V3/V3/V1; V1 conceded (CR-2). V1 concepts C and E interleave verify/failure above decisions (V1 s.8.2, s.10.2). All three advocates say: keep DEC-1 and repair the screens. |
| X-007 | V3 | 80% | Votes V3/V3/V1; V2 conceded (CR-4). V2 C3 and C5 break their own ordering rule (V2 s.4.3, s.4.5). Repair under DEC-1 and OLDEST. |
| X-008 | V3 | 100% | Unanimous; V2 conceded (CR-5). Consistent synthetic IDs (V3 s.5-10). |
| X-009 | V3 | 100% | Unanimous; V2 conceded (CR-6). Overlap note under both questions and union accounting (V3 s.4 rule 6); specified, not yet drawn (V3 NE-2). |
| X-010 | V3 | 100% | Unanimous; V1 conceded (CR-4). DEMO-marked worker IDs (V3 s.5-10). |
| A-001 | V3 | 90% | Unanimous. Candidate / uncertain-identity semantics are the safest base (V3 s.3), but no classifier or ambiguity rule exists (V3 NE-1). |
| A-002 | V3 | 100% | Unanimous; V2 conceded (CR-8), V3 changed vote. Acting human and requester stay distinct; missing owner stays unknown (V3 s.3, G05). |
| A-003 | UNRESOLVED | 50% | Votes V1/V3/V2. No variant verifies a chat message or fence limit; line and column targets are proposals only. |
| A-004 | V3 | 95% | Unanimous. Separate generation, collection and evidence times (V3 s.3); no variant has a reader-side recheck rule (V3 Round 2). |

## Convergence Assessment

- Points resolved: 44 of 46
- Alignment: 95.7%
- Threshold: 75%
- Taxonomy coverage: L1, L2 and L3 all have agreed points (gate passes)
- Invariant gate: FAILS (5 HIGH-severity UNADDRESSED: INV-005, INV-006, INV-010, INV-026, INV-028)
- Status: BLOCKED_BY_INVARIANTS
- Unresolved points: S-003 (requirements catalogue form), A-003 (one paste fits the chat message limit)
- Termination: max rounds reached for depth=standard (Round 1 0.913, Round 2 0.957; no oscillation)
- Points won: V1 11, V2 12, V3 21
