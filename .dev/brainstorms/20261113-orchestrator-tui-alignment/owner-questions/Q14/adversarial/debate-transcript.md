# Adversarial Debate Transcript: Q14

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 82% (9 of 11 scored points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned general-purpose sub-agents (Variant 1 persona architect, Variant 2 persona qa, Variant 3 persona analyzer). No failures.
- Protocol: sc-adversarial-protocol, loaded by Skill call at Q11 in this session and applied as written.
- Variant map: Variant 1 = proposal-A (#539 merged; capture gates only live-value features); Variant 2 = proposal-B (#539 merged + capture recorded + `working` class restored in code); Variant 3 = proposal-C (#539 merged + capture recorded)

## Unassigned picks
- Advocate V1: Variant 3, with Variant 1's per-feature gating as a fallback if the capture is still blocked after a dated deadline.
- Advocate V2: Variant 3, with the gate entry stating whether the recorded values are enough to build the `working` rule's four conditions.
- Advocate V3: Variant 3, with both of the above.
- Result: 3 of 3 pick Variant 3.

## Orchestrator spot-checks
- `src/superclaude/cli/sweep/classify.py:251-257` (re-read at question time): Rule 5 returns None; its four conditions are kept in the comment as the text to restore. Confirmed.
- merged-requirements.md:399 (V2-02): "if Q14 means \"capture recorded\", (2) suffices". merged-requirements.md:203 (SW-14): "Needed only if ... \"`working` class restored\"". merged-requirements.md:415 (W5): "The gate as worded conflates a record with a code change". Confirmed by the advocates' re-reads and the question-time read.
- merged-requirements.md:401 (V2-04): LLM-derived entries are "never changing a sweep class" (Advocate V2 strength 2). Taken from the advocate's re-read; consistent with question.md fact 5.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (agreed) | 95% | Same sections. |
| C-001 | L2 | 3 | 2 | 3 | Variant 3 | 70% | Two ledger-checkable records match V2-02 as written. |
| C-002 | L3 | 1 | 2 | 3 | unresolved (split) | 50% | Each backed its own role for the capture; all unassigned picks resolve to Variant 3. |
| C-003 | L3 | 1,3 | 2 | 3,1 | Variant 3 (with 1) | 72% | SW-14 off the gate, per W5 and A-013's "unblocks". |
| C-004 | L2 | 1 | 3 | 1 | Variant 1 | 58% | Variant 1 starts design earliest; the delay under Variant 3 is limited because V2-05 is ungated. |
| C-005 | L1 | 2 | 2 | 2 | Variant 2 | 80% | Most literal to ADJ wording; fidelity only. |
| X-001 | L3 | 1 | 2 | 3 | unresolved (split) | 50% | Wait for live values (3), for code too (2), or not at all (1). |
| X-002 | L3 | 1,3 | 2 | 3 | Variant 3 | 62% | A carried gap is acceptable for an advisory v2. |
| X-003 | L2 | 1,3 | 3 | 3,1 | Variant 3 | 80% | A planning gate should check records, not code. |
| A-001 | L2 | QUALIFY | ACCEPT | ACCEPT | agreed: ACCEPT | 70% | V2-01 names sweep report JSON v1 as a collector. |
| A-002 | L2 | QUALIFY | QUALIFY | QUALIFY | agreed: QUALIFY | 85% | The INV-008 ruling (Q1) could change the class list; record-based gates are less exposed. |
| U-001 | n/a | 1 | 1 | 1 | Variant 1 (valid, as fallback) | 62% | Per-feature gating if Orca stays unreachable. |
| U-002 | n/a | 2 | 2 | 2 | Variant 2 (valid, as a gate check) | 62% | Rule 5 might not be buildable from what Orca exposes. |
| U-003 | n/a | 3 | 3 | 3 | Variant 3 (valid) | 67% | Records a ledger entry can check. |

## Convergence Assessment
- Points resolved: 9 of 11
- Alignment: 82%
- Threshold: 80%
- Taxonomy coverage: L1 2, L2 4, L3 5; all covered
- Invariant gate: not applied (quick)
- Status: CONVERGED
- Unresolved points: C-002, X-001 (on assigned positions; all three unassigned picks resolve them to Variant 3)

## Round 1: Advocate Statements

The three statements follow verbatim.


---

### Round 1: Advocate for Variant 1 (gate = PR #539 merged; the capture gates only live-value features)

Persona: architect (structure, dependencies, long-term impact). Paths below are relative to the worktree root unless they start with `F/` (this Q14 folder). "MR" = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. "ADJ" = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line cited below was re-read on 2026-11-14 unless marked UNVERIFIED.

#### Position summary

Variant 1 puts on the whole-v2 gate only the one thing every part of v2 depends on (the merged sweep, PR #539), and moves the live Orca capture to the exact v2 fields that read live values, marked pending until it lands. That keeps an external, currently unreachable dependency (a live Orca session, MR:604) off the critical path of an advisory planning step, and it removes the record-versus-code ambiguity (W5, MR:415) by not tying the whole gate to either.

#### Steelman

**Variant 2 (merged + capture recorded + `working` class restored in code).** The strongest case: the gate exists so that v2 is designed against a sweep that tells the truth about sessions. Today `_rule_working` returns None and every working session falls to `could not determine` (`src/superclaude/cli/sweep/classify.py:251-257`; class list at `docs/designs/orchestrator-mode.md:472`). A knowledge layer built on top of a sweep with a blind class inherits that blindness. Variant 2 is also the most literal reading of ADJ, which twice says "the #534 live capture that restores the sweep's `working` class" (ADJ:294, ADJ:699), and it is the only variant that turns the risk "the capture shows Rule 5 cannot be built from what Orca exposes" (variant-2 line 24, U-002) into something discovered before v2 design rather than after.

**Variant 3 (merged + capture recorded).** The strongest case: it is the spec's default (MR:541), it keeps the gate a matter of records that a dated ledger entry can check (V2-02, MR:399, and W5 at MR:415), and it gives the v2 design the real live names (`agentWait`, liveness, status) and the `projection.attention` values for a live and a blocked worker, which V2-02 item (2) already asks for (MR:399). ADJ row A-013 ties the capture not only to the `working` class but also to V5's open items O-13 and O-14 and "the #423 gate" (ADJ:335), so the capture has value for v2 beyond one class. It avoids Variant 2's code PR on the critical path while still not designing blind.

#### Strengths claimed

1. **The gate matches the dependency graph, not a proxy for it.** v2's first release must read "only what named collectors publish" (V2-04, MR:401) and the rewrite names two collectors, "sweep report JSON v1" and "observe snapshot v1" (V2-01 item 4, MR:398). The capture is not a collector; it is a read-only record that "unblocks" the `working` class (ADJ:335). Gating all of v2 on it couples v2 to an input that only some of its fields need. Variant 1 gates each consumer on its own producer, which is the standard way to keep a dependency graph honest.
2. **It keeps an unreachable external dependency off the critical path.** The capture needs ORCA-AVAILABLE, and "every live lane needs it: CAP (XC-03) ..."; the app was not reachable on 2026-11-13 (MR:604). It also needs an owner answer on who runs it (Q24, ADJ:335). Variants 2 and 3 both stall the v2 gate on that; Variant 1 does not.
3. **It fits the spec's own design step.** V2-03 item (3) already requires the design to "name every catalogue field and its source ... and which fields need a schema decision" (MR:400). Marking live-value fields "pending capture" is one more column in a table the design must produce anyway, so Variant 1 adds almost no process.
4. **It dissolves W5 instead of picking a side.** W5 says "the gate as worded conflates a record with a code change" (MR:415). Variants 2 and 3 each pick one reading; Variant 1 removes both from the whole-v2 gate, so SW-14 (MR:203) stays a #534 follow-up with no conditional wiring into V2-02.
5. **Proportion.** v2 is advisory, delivers to the person or coordinator only, and marks LLM-derived entries inferred (ADJ:294). A planning gate for an advisory layer should be the lightest gate that prevents real harm; the merged sweep is that gate.

#### Weaknesses identified in others

**Variant 2.**
- It puts a code PR (SW-14) on the critical path of a planning gate. SW-14 needs XC-03, then a supervised worker, a test, a PR via `/sc:pr-submit --monitor 3` and a grant row (MR:203). That is four dependencies stacked behind an Orca session that was unreachable (MR:604).
- Its own risk (variant-2 line 24) cuts against it: if Rule 5 cannot be built from what Orca exposes, v2 waits on a sweep redesign. A gate that can turn into an open-ended redesign is a poor gate.
- Literal fidelity to ADJ's phrase is weak support, because ADJ's own A-013 calls the capture something that "unblocks" the class (ADJ:335), which W5 reads as meaning restoring it is a later change (MR:415). The spec has already flagged the literal wording as a conflation.

**Variant 3.**
- It still blocks all of v2 on the live capture (variant-3 line 23), so it shares Variant 2's exposure to MR:604 and Q24 for every field, including those that never touch live values.
- It admits v2 "must carry that gap" of working sessions shown as `could not determine` (variant-3 line 22). Once the gap is accepted, the capture's value to v2 is limited to naming fields, which is exactly what Variant 1's per-field pending marker already handles. Variant 3 pays the waiting cost without buying a working class.
- Its rewording of ADJ's sentence ("that records the values the `working` class needs", variant-3 line 10) is still a departure from ADJ:699, so it is not free of the rewording cost it counts against Variant 1.

#### Concessions

- **Rework risk is real.** A design started before the capture may assume field names or meanings the capture contradicts (variant-1 line 22). Variant 3 avoids that.
- **Departure from ADJ and from V2-02 as written.** ADJ:294 and ADJ:699 both put the capture in the gate, and V2-02 item (2) lists "the shared capture recorded (XC-03)" as a gate part independent of the Q14 branch (MR:399). Variant 1 needs V2-02 rewritten, not just a branch chosen.
- **The capture is about more than the `working` class.** A-013 links it to `projection.attention`, V5's O-13 and O-14, and "the #423 gate" (ADJ:335). Variant 1's text names only the `working` class and `projection.attention` (variant-1 line 5) and may under-list what is live-dependent.
- **A fuzzier gate.** "Which v2 fields are live-value dependent" is left to the brainstorm (variant-1 line 28). Until that list exists, a ledger entry cannot check the per-feature part of the gate; Variant 3's gate is checkable today (U-003).
- **The early-start benefit is smaller than it looks.** V2-05 (the research pass) is ungated, and V2-03 waits on V2-02 only "for its implementation-facing parts" (MR:400; question.md fact 6). So under Variant 3 much of the early thinking can already start. Variant 1's unique unlock is mainly the implementation-facing design work.
- **Unverified claim in my own variant.** "Most catalogue fields (sessions, worktrees, packages, git state) come from the sweep's report" (variant-1 line 17) is UNVERIFIED: no catalogue field list exists yet, and V2-01 names a second collector (observe snapshot v1, MR:398).

#### Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 (v2 reads the sweep report JSON as a main input) | QUALIFY | V2-01 names two collectors, sweep report JSON v1 and observe snapshot v1 (MR:398), so the sweep is a main input but not the only one; how much of v2 rides on sweep classes is UNVERIFIED until V2-03 lists fields. |
| A-002 (PR #539 merges close to today's form) | QUALIFY | All three gates name #539, so a change under Q1 / INV-008 hits all three equally; I did not verify the INV-008 ruling's status (UNVERIFIED), and the gate should name the read-only sweep's contract ("sweep report JSON v1") as well as the PR number so a reshaped merge is still checkable. |

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|-----------|--------|
| S-001 | tie | 95% | Same five sections in all three; no structural edge. |
| C-001 (gate parts) | 3 | 55% | Two records are ledger-checkable today and match V2-02 item (2) and A-013; Variant 1's per-field part is not checkable until the field list exists. |
| C-002 (role of the capture) | 1 | 60% | The capture serves specific fields (A-013, ADJ:335), so gating those fields, not all of v2, matches the real dependency. |
| C-003 (SW-14) | tie (1 and 3) | 80% | Both keep the code change off a planning gate, as W5 (MR:415) and SW-14's conditional wording (MR:203) allow. |
| C-004 (when the brainstorm starts) | 1 | 55% | Starting at #539 merge avoids the MR:604 / Q24 stall, though V2-05 and the non-implementation parts of V2-03 already soften Variant 3's delay. |
| C-005 (fidelity to ADJ wording) | 2 | 85% | Variant 2 is the literal reading of ADJ:294 and ADJ:699; fidelity alone, not correctness. |
| X-001 (should v2 design wait for live values) | 1 | 55% | Design can name live-dependent fields and mark them pending (V2-03 item 3 already requires naming field sources), at a known rework risk. |
| X-002 (v2 showing working sessions as `could not determine`) | tie (1 and 3) | 75% | Both accept the gap for an advisory layer; Variant 2's refusal costs a code PR for a class the sweep already reports honestly as undetermined. |
| X-003 (code change on a planning gate) | tie (1 and 3) | 85% | A planning gate should check records, not code; W5 flags the conflation. |
| U-001 (per-feature gating) | 1 | 70% | It is the one contribution that decouples v2 from Orca availability; worth keeping in any merge. |
| U-002 (capture may show Rule 5 is unbuildable) | 2 | 60% | A real v2 risk only Variant 2 names; it argues for running the capture early, which a per-field pending marker or a capture gate both surface. |
| U-003 (gate of ledger-checkable records) | 3 | 75% | Matches V2-02's "dated ledger entry" design (MR:399) and W5's evidence wording (MR:415). |

#### Overall ranking and unassigned pick

**Ranking as the Variant 1 advocate:** Variant 1, then Variant 3, then Variant 2. Variant 1 has the cleanest dependency structure and the smallest critical path; Variant 3 is close behind and better on checkability; Variant 2 puts a code PR and a possible sweep redesign on a planning gate for an advisory layer.

**Honest unassigned pick:** Variant 3, with Variant 1's U-001 grafted in. Variant 3 is the spec's default (MR:541), needs no rewrite of V2-02's capture item (MR:399), keeps the gate checkable by a dated ledger entry, and the capture feeds more than one class (ADJ:335). The graft: if the capture is still blocked by Orca availability (MR:604) or Q24 after a dated deadline the owner sets, V2-03 may proceed with live-value fields marked pending, so the gate cannot stall indefinitely.

---

### Round 1 advocate statement: Variant 2

Advocate: Variant 2 (proposal B: "#539 merged, capture recorded, `working` class restored in code"). Persona: qa (edge cases, failure scenarios). Depth: quick, Round 1 only. Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line cited below was re-read on 2026-11-14 unless marked UNVERIFIED.

#### Position summary

Variant 2 is the only answer whose gate is proved by a passing test rather than by a record nobody has checked against the code that must use it. A capture that has been "recorded" can still be wrong, incomplete or insufficient for Rule 5, and v2 is barred from repairing a sweep class itself, so the safe gate is the one that shows the `working` class actually works before v2 is designed on top of it.

#### Steelman

**Variant 1 (gate = #539 merged; capture gates only live-value features).** The strongest case: v2 is advisory and has not been designed, and most of what it would catalogue (sessions, worktrees, packages, git state) comes from the sweep's report, not from the uncaptured values (variant-1 line 17). The capture depends on Orca being reachable, which it was not on 2026-11-13 (MR:604), and on an owner answer on who runs it (Q24, MR:551, whose default is that XC-03 does not run and "V2-02 cannot pass"). Holding a whole planning effort hostage to one live sitting is poor sequencing when the dependent fields can simply be marked pending. Variant 1 also dissolves the record-versus-code ambiguity (W5, MR:415) instead of picking a side.

**Variant 3 (gate = #539 merged + capture recorded).** The strongest case: it is the spec's own default (MR:541), it is close to ADJ's recommended gate (ADJ:294, ADJ:699), and it gives v2's designers the real live values (`agentWait`, liveness, status, `projection.attention` for a live and a blocked worker, MR:399 item 2) without putting a code PR on a planning critical path. A ledger entry citing a merge and a capture record is cheap to check (MR:399). ADJ row A-013 itself says the capture "unblocks" the `working` class (ADJ:335), which reads as "makes the later code change possible", not "is the code change", so Variant 3 is arguably the faithful reading of ADJ's intent.

#### Strengths claimed

1. **A test, not a record, proves the gate's purpose.** The reason the capture is in the gate at all is the `working` class: ADJ:294 and ADJ:699 both say "the #534 live capture that restores the sweep's `working` class". A record proves values were written down; only SW-14's pinning test (MR:203, "(2) a test pins it") proves those values are enough to make Rule 5 match. From a QA view, Variant 3's gate can pass while the thing it exists for still fails.
2. **v2 cannot fill the gap itself.** V2-04 requires that LLM-derived entries are "marked inferred and never changing a sweep class" (MR:401). So if the sweep shows a working session as `could not determine` (classify.py:251-257; design open item 6 at docs/designs/orchestrator-mode.md:997), v2 is forbidden from correcting it. Variants 1 and 3 both accept a v2 that "carries the gap" (variant-3 line 22; variant-1 line 24), but the spec gives v2 no legal way to carry it other than passing on an unknown.
3. **Most literal fidelity to the adjudicated text.** Variant 2 adopts ADJ's sentence as written ("the #534 live capture that restores the sweep's `working` class", ADJ:699). Variants 1 and 3 both need new wording for the #423 rewrite (variant-1 line 23; variant-3 line 10).
4. **Surfaces the real design risk early (U-002).** The four Rule 5 conditions (classify.py:254-255: liveness verdict "live", status "in_progress", `agentWait` present, `agentWait` None) are a hypothesis until the live names are known. If Orca does not expose them in a usable form, the sweep needs redesign, and a v2 designed before that discovery is designed on a class that may never exist. Variant 2 finds this before v2 design, not during or after.
5. **Still mechanically checkable.** V2-02 already defines the check for this reading: "SW-14 has merged and its #534 row is closed" (MR:399 item 3). A merge and a closed row are dated facts a ledger entry can cite, so Variant 3's "records a ledger can check" advantage (U-003) is not exclusive.
6. **Does not block research.** V2-05, the dedicated research pass, is ungated (MR:400 item 2; question.md fact 6), and Variant 2 keeps it running early (variant-2 line 12). Only the implementation-facing parts of V2-03 wait.
7. **Removes the ambiguity cleanly.** W5 (MR:415) asks the owner to word the answer as "capture recorded" or "`working` class shipped"; Variant 2 picks one unambiguously, so V2-02 has no judgement call.

#### Weaknesses identified in others

**Variant 1.**
- Edge case: "which v2 fields are live-value dependent" is left for the brainstorm to list (variant-1 line 28). That list is exactly what the uncaptured values would tell you; the brainstorm must guess the dependency boundary before knowing the data, so a field wrongly judged independent escapes the per-feature gate entirely.
- It departs from both ADJ:294 and ADJ:699 and from the spec default (MR:541), so the rewrite needs new text and V2-02's criteria (MR:399 item 2, which names the capture) no longer line up with the gate.
- Failure scenario it admits: field names or meanings assumed in design are contradicted by the capture and redone (variant-1 line 22). With v2 forbidden from changing a sweep class (MR:401), redesign cost lands on v2, not on the sweep.
- "Marked pending" has no owner or trigger in the variant, so pending fields can stay pending indefinitely.

**Variant 3.**
- Failure scenario: the capture is recorded, V2-02 passes, v2 design starts, and only later does SW-14 discover the recorded names cannot express Rule 5 (for example `agentWait` absent rather than null, which the design cannot tell apart until code reads it). The gate passed on a record that was never exercised.
- The variant drops ADJ's "restores" and rewords it (variant-3 line 10), which turns ADJ's stated purpose into an optional follow-up with no date: "When the `working` class is restored" stays unresolved (variant-3 line 28).
- It still pays the hardest cost Variant 2 pays: a live Orca sitting that needs Q24 answered and Orca reachable (variant-3 line 23; MR:551; MR:604). The marginal cost of Variant 2 over Variant 3 is one small, already-specified code PR (MR:203), not a new external dependency.
- Its claim that v2 "carries the gap" (variant-3 line 22) conflicts in practice with MR:401: v2 can only report "could not determine" for every working session, which for an orchestration catalogue is likely the most common live state (UNVERIFIED: no measured share of working rows exists).

#### Concessions

- Variant 2 puts a code PR on a planning gate for an advisory v2 (variant-2 line 23), which W5 (MR:415) explicitly calls conflating a record with a code change. That is a real category cost.
- It is the slowest gate. It inherits every blocker of Variant 3 (Q24 answer, Orca reachable, MR:551 and MR:604) and adds SW-14's own dependencies: Q25 and `GRANT(SW-14,pr-submit)` (MR:203).
- If the capture shows Rule 5 cannot be built, v2 waits on a sweep redesign (variant-2 line 24). That risk is real; I argue it is better found before v2 design, but it does lengthen the critical path with no fixed bound.
- ADJ A-013's word "unblocks" (ADJ:335) supports Variant 3's reading that restoring the class is a later step; the literal ADJ:699 wording supports mine. The ADJ text is internally ambiguous, so my "most literal" claim is narrower than it looks.
- v2 delivers to the person or coordinator only (ADJ:294) and Q15's default is "report only" (MR:542), so a wrong `working` class in v2 harms a reader, not an agent. That lowers the stakes my QA argument relies on.
- Nothing of v2 exists, PR #539 is still open, and the capture has not run (question.md fact 7); every scenario above is about planning risk, not observed failure.

#### Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 (v2 reads the sweep report JSON as a main input) | ACCEPT | V2-01 requires the #423 body to name "sweep report JSON v1" (MR:398 item 4) and V2-03 requires every field's source be named with it as a listed source (MR:400 item 3), so the sweep's classes do matter to v2. |
| A-002 (PR #539 merges close to today's form) | QUALIFY | Q1 (INV-008 fix or accept, MR:1266) is still open; if the ruling changes the class list, all three gates move, and Variant 2's SW-14 moves with it (UNVERIFIED how much Q1 could change the class list). |

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 2 | 55% | Only a three-part gate proves the capture is usable; Variant 3 is close and cheaper. |
| C-002 | 2 | 55% | Treating the capture as input to a tested change checks it; a record alone does not. |
| C-003 | 2 | 50% | Required SW-14 gives the `working` class a date; as a follow-up it has none (variant-3 line 28). |
| C-004 | 3 | 55% | Starting the brainstorm after the capture is a fair middle; V2-05 runs early under all variants anyway. |
| C-005 | 2 | 75% | Variant 2 keeps ADJ:699's wording verbatim. |
| X-001 | 2 | 50% | Waiting for the code change catches an unbuildable Rule 5 before v2 design, at real delay cost. |
| X-002 | 2 | 60% | MR:401 bars v2 from changing a sweep class, so a v2 with no `working` class cannot repair it. |
| X-003 | 3 | 60% | Honest concession: a code change on a planning gate is the weakest part of my variant (W5, MR:415). |
| U-001 | 1 | 55% | Per-feature gating is a useful idea even if its boundary must be guessed. |
| U-002 | 2 | 65% | The "Rule 5 may be unbuildable" risk is the main failure scenario none of the others guards. |
| U-003 | 3 | 55% | Records-only is simpler to check, though V2-02 already makes SW-14 checkable too (MR:399). |

#### Overall ranking and unassigned pick

Ranking as advocate: Variant 2, then Variant 3, then Variant 1.

Unassigned pick: honestly, I would pick Variant 3. It is the spec's default (MR:541), it gives v2's designers the live values that matter, and it keeps a code PR off a planning gate for an advisory, person-facing v2 (ADJ:294; MR:542). I would make one change borrowed from Variant 2: the V2-02 ledger entry should state whether the recorded values are sufficient for Rule 5's four conditions, so the "unbuildable Rule 5" risk (U-002) is checked at the gate without waiting for SW-14 to merge.

---

### Round 1 advocate statement: Variant 3 (proposal C)

Persona: analyzer (evidence quality, logical consistency). Depth: quick, Round 1 only. Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. "M" = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; "ADJ" = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line cited below was re-read on 2026-11-14.

#### Position summary

Variant 3 sets the #423 gate at two checkable records: PR #539 merged and the #534 shared live capture recorded. It is the only variant that already matches the spec's own default (M:541) and the V2-02 check as written (M:399), so it needs no new spec wording, while keeping a code change (SW-14) off a planning gate for an advisory, unbuilt v2.

#### Steelman

**Variant 1 (gate = #539 merged; capture gates only live-value fields).** Its best case: v2 is advisory and unbuilt, most catalogue fields come from the sweep report rather than from the uncaptured live values, and the capture depends on an Orca app that was not reachable on 2026-11-13 (M:604) plus an unanswered owner question on who runs it (Q24, ADJ:335). Tying all of v2 to an event outside the team's control can stall design indefinitely. Marking live-value fields "pending" is a standard way to design against an open interface, and V1 is the only variant whose gate cannot be blocked by Orca availability.

**Variant 2 (gate = #539 merged + capture recorded + `working` class restored in code).** Its best case: it is the most literal reading of ADJ, which twice says "the #534 live capture that restores the sweep's `working` class" (ADJ:294, ADJ:699). The `working` class is one of eight sweep classes (docs/designs/orchestrator-mode.md:472), and today `_rule_working` returns None so every working row falls to "could not determine" (src/superclaude/cli/sweep/classify.py:251-257). A v2 designed on a sweep that cannot say "working" is designed on a degraded input. V2 also uniquely notices (U-002) that the capture might show Rule 5 cannot be built from what Orca exposes; requiring the code change forces that risk to surface before v2 commits to a design.

#### Strengths claimed

1. **It is already the spec's default, so it costs no rewrite.** M:541 sets the default as "ADJ's recommended gate, read as \"capture recorded\" ... SW-14 is then not needed". V2-02 already says "if Q14 means \"capture recorded\", (2) suffices" (M:399). SW-14 already says it is "Needed only if the owner's Q14 answer means \"`working` class restored\", not \"capture recorded\"" (M:203). Choosing V3 confirms the default; choosing V1 or V2 changes rows.
2. **It resolves weak point W5 in the direction W5 itself points.** W5 says the capture is "a read-only record" and that "restoring the class is a later sweep change. The gate as worded conflates a record with a code change" (M:415). ADJ row A-013 says the capture "unblocks" the `working` class (ADJ:335), which describes a precondition, not the change itself. V3 keeps the gate on the record and the change where A-013 places it, after.
3. **Its gate is checkable by a ledger entry.** V2-02's observe clause is "one dated gate note ... citing the merge and the capture record" (M:399). Both V3 parts are facts a ledger entry can cite (a merge, a recorded capture). V2's third part needs a merged PR with its own review cycle and grant (`GRANT(SW-14,pr-submit)`, M:203).
4. **v2 is designed with real live values, not guesses.** V2-02 part (2) requires the capture to include "`projection.attention` values for one live and one blocked worker" (M:399), and the design's open item 6 lists the missing `worker-show` names for `agentWait`, `liveness.verdict` and `status` (docs/designs/orchestrator-mode.md:997). V3 makes v2's design start after those names exist, which avoids V1's admitted redo risk.
5. **It keeps the scope ADJ chose for the other phases.** Like ADJ:699, V3 keeps `/sc:close`, resume and the trust layer out unless the brainstorm decides v2 relays to agents, which matches SW-12's "only if v2 relays to agents, Q14" (M:201).
6. **Waiting costs little where it matters.** The dedicated v2 research pass V2-05 is ungated (M:400, item 2), and V2-03 waits on V2-02 only for its "implementation-facing parts" (M:400). So V3 delays only implementation-facing design, not research.

#### Weaknesses identified in others

**Variant 1.**
- It contradicts V2-02 as written: V2-02 lists "the shared capture recorded (XC-03)" as part (2) for every reading of Q14 (M:399), so V1 must rewrite V2-02, V2-01 and the ADJ text (V1 concedes the last).
- Its "per-feature" gate needs a list of which fields are live-value dependent, which V1 itself leaves unresolved ("the brainstorm must list them"). The gate therefore depends on an output of the activity it gates; a V2-02 check cannot pass or fail mechanically until that list exists.
- It accepts the redo risk it names: the design "may assume field names or meanings that the capture later contradicts". Open item 6 shows those names are genuinely unknown today (orchestrator-mode.md:997).
- The claim that "most catalogue fields ... come from the sweep's report" is reasonable but UNVERIFIED: no v2 field list exists (V2-03 item 3 has not run, M:400).

**Variant 2.**
- It puts a code PR on the critical path of a planning gate for a v2 that is advisory (ADJ:294) and unbuilt. W5 names that exact conflation as the defect (M:415).
- Its own risk (U-002) cuts against it: if the capture shows Rule 5 cannot be built, V2's gate "waits on a sweep redesign", so v2 planning is held hostage to sweep work. Under V3 the same discovery is visible in the recorded capture, and v2 designs around it.
- Its literalism is weaker than it looks: ADJ:699 says the capture "that restores the sweep's `working` class is recorded", so the verb applied to the gate is "recorded"; "restores" describes what the capture enables. A-013's "unblocks" (ADJ:335) supports that reading. V2 reads a relative clause as a third gate condition.
- It requires a grant row and a `/sc:pr-submit --monitor 3` run (M:203), adding owner decisions (Q25) to the v2 path.

#### Concessions

- V3 still depends on a live capture, so it inherits the Orca availability risk (M:604) and the open Q24 (ADJ:335). V1 is the only variant immune to that.
- V3 allows a v2 that ships while the sweep still shows working sessions as "could not determine" (classify.py:251-257). The gap is carried, not closed.
- V3 departs from ADJ's literal wording by dropping or rewording "restores"; the #423 rewrite (V2-01) must change ADJ's proposed text slightly.
- V3 leaves "when the `working` class is restored" unresolved; SW-14 has no forcing date once it is off the gate.
- V3's claim that the capture records the `agentWait`, `liveness` and `status` names is what the capture is meant to record (orchestrator-mode.md:997); whether one capture run will actually yield all of them is UNVERIFIED, since XC-03 has not run.

#### Shared assumptions

- **A-001 (v2 reads the sweep's report JSON as a main input): ACCEPT.** V2-01 item 4 requires the #423 body to name "sweep report JSON v1" as a collector (M:398) and V2-04 says v2 reads only what named collectors publish (M:401).
- **A-002 (PR #539 merges close to today's form): QUALIFY.** All three variants depend on it equally, so it does not rank them; but if the INV-008 ruling (Q1) changes the class list, the "capture recorded" part still holds while V2's SW-14 part could be invalidated, which slightly favours the record-based gates.

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 3 | 70% | Two record parts match V2-02 as written (M:399) without a code PR or a field list the gate cannot yet name. |
| C-002 | 3 | 65% | Whole-gate prerequisite as a record is checkable by a ledger entry; V1's per-feature role needs an unwritten field list. |
| C-003 | 3 (tie with 1) | 70% | SW-14 as a follow-up follows W5 and A-013 ("unblocks", ADJ:335); V1 and V3 agree here. |
| C-004 | 1 | 55% | V1 starts the brainstorm earliest; V3's cost is limited because V2-05 research is ungated (M:400), but V1 is still earlier. |
| C-005 | 2 | 75% | V2 is the most literal match to ADJ:294 and ADJ:699; V3 is close but drops "restores". |
| X-001 | 3 | 60% | Waiting for live values avoids V1's admitted redo risk; waiting also for code (V2) adds a PR for an advisory, unbuilt v2. |
| X-002 | 3 | 55% | A carried gap is acceptable for an advisory v2; V1 accepts it too but adds per-field pending marks with no field list. |
| X-003 | 3 (tie with 1) | 75% | W5 names a code change on the gate as the conflation to fix (M:415). |
| U-001 | 1 | 60% | Per-feature gating is a real idea V3 lacks; useful as a fallback if Orca stays unreachable. |
| U-002 | 2 | 60% | A genuine risk V3 does not name; under V3 it is visible in the capture record but not forced. |
| U-003 | 3 | 70% | A records-only gate is what V2-02's observe clause can check (M:399). |

#### Overall ranking and unassigned pick

Ranking: Variant 3 first, Variant 1 second, Variant 2 third.

Variant 1 ranks above Variant 2 because it at least keeps code off the planning gate and has a concrete answer to the Orca outage; Variant 2 adds a code PR, a grant and a sweep-redesign risk to the path of an advisory, document-stage project.

If I were not assigned a variant, I would still pick Variant 3, with one honest qualification: it would be stronger if it borrowed V1's U-001 as a fallback (if the capture cannot run by a dated point, the gate drops to #539 merged with live-value fields marked pending) and V2's U-002 as a named risk (the capture record must state whether Rule 5's four conditions can be built from what it recorded).
