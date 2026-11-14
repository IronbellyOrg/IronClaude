# Round 1 advocate statement: Variant 2

Advocate: Variant 2 (proposal B: "#539 merged, capture recorded, `working` class restored in code"). Persona: qa (edge cases, failure scenarios). Depth: quick, Round 1 only. Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line cited below was re-read on 2026-11-14 unless marked UNVERIFIED.

## Position summary

Variant 2 is the only answer whose gate is proved by a passing test rather than by a record nobody has checked against the code that must use it. A capture that has been "recorded" can still be wrong, incomplete or insufficient for Rule 5, and v2 is barred from repairing a sweep class itself, so the safe gate is the one that shows the `working` class actually works before v2 is designed on top of it.

## Steelman

**Variant 1 (gate = #539 merged; capture gates only live-value features).** The strongest case: v2 is advisory and has not been designed, and most of what it would catalogue (sessions, worktrees, packages, git state) comes from the sweep's report, not from the uncaptured values (variant-1 line 17). The capture depends on Orca being reachable, which it was not on 2026-11-13 (MR:604), and on an owner answer on who runs it (Q24, MR:551, whose default is that XC-03 does not run and "V2-02 cannot pass"). Holding a whole planning effort hostage to one live sitting is poor sequencing when the dependent fields can simply be marked pending. Variant 1 also dissolves the record-versus-code ambiguity (W5, MR:415) instead of picking a side.

**Variant 3 (gate = #539 merged + capture recorded).** The strongest case: it is the spec's own default (MR:541), it is close to ADJ's recommended gate (ADJ:294, ADJ:699), and it gives v2's designers the real live values (`agentWait`, liveness, status, `projection.attention` for a live and a blocked worker, MR:399 item 2) without putting a code PR on a planning critical path. A ledger entry citing a merge and a capture record is cheap to check (MR:399). ADJ row A-013 itself says the capture "unblocks" the `working` class (ADJ:335), which reads as "makes the later code change possible", not "is the code change", so Variant 3 is arguably the faithful reading of ADJ's intent.

## Strengths claimed

1. **A test, not a record, proves the gate's purpose.** The reason the capture is in the gate at all is the `working` class: ADJ:294 and ADJ:699 both say "the #534 live capture that restores the sweep's `working` class". A record proves values were written down; only SW-14's pinning test (MR:203, "(2) a test pins it") proves those values are enough to make Rule 5 match. From a QA view, Variant 3's gate can pass while the thing it exists for still fails.
2. **v2 cannot fill the gap itself.** V2-04 requires that LLM-derived entries are "marked inferred and never changing a sweep class" (MR:401). So if the sweep shows a working session as `could not determine` (classify.py:251-257; design open item 6 at docs/designs/orchestrator-mode.md:997), v2 is forbidden from correcting it. Variants 1 and 3 both accept a v2 that "carries the gap" (variant-3 line 22; variant-1 line 24), but the spec gives v2 no legal way to carry it other than passing on an unknown.
3. **Most literal fidelity to the adjudicated text.** Variant 2 adopts ADJ's sentence as written ("the #534 live capture that restores the sweep's `working` class", ADJ:699). Variants 1 and 3 both need new wording for the #423 rewrite (variant-1 line 23; variant-3 line 10).
4. **Surfaces the real design risk early (U-002).** The four Rule 5 conditions (classify.py:254-255: liveness verdict "live", status "in_progress", `agentWait` present, `agentWait` None) are a hypothesis until the live names are known. If Orca does not expose them in a usable form, the sweep needs redesign, and a v2 designed before that discovery is designed on a class that may never exist. Variant 2 finds this before v2 design, not during or after.
5. **Still mechanically checkable.** V2-02 already defines the check for this reading: "SW-14 has merged and its #534 row is closed" (MR:399 item 3). A merge and a closed row are dated facts a ledger entry can cite, so Variant 3's "records a ledger can check" advantage (U-003) is not exclusive.
6. **Does not block research.** V2-05, the dedicated research pass, is ungated (MR:400 item 2; question.md fact 6), and Variant 2 keeps it running early (variant-2 line 12). Only the implementation-facing parts of V2-03 wait.
7. **Removes the ambiguity cleanly.** W5 (MR:415) asks the owner to word the answer as "capture recorded" or "`working` class shipped"; Variant 2 picks one unambiguously, so V2-02 has no judgement call.

## Weaknesses identified in others

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

## Concessions

- Variant 2 puts a code PR on a planning gate for an advisory v2 (variant-2 line 23), which W5 (MR:415) explicitly calls conflating a record with a code change. That is a real category cost.
- It is the slowest gate. It inherits every blocker of Variant 3 (Q24 answer, Orca reachable, MR:551 and MR:604) and adds SW-14's own dependencies: Q25 and `GRANT(SW-14,pr-submit)` (MR:203).
- If the capture shows Rule 5 cannot be built, v2 waits on a sweep redesign (variant-2 line 24). That risk is real; I argue it is better found before v2 design, but it does lengthen the critical path with no fixed bound.
- ADJ A-013's word "unblocks" (ADJ:335) supports Variant 3's reading that restoring the class is a later step; the literal ADJ:699 wording supports mine. The ADJ text is internally ambiguous, so my "most literal" claim is narrower than it looks.
- v2 delivers to the person or coordinator only (ADJ:294) and Q15's default is "report only" (MR:542), so a wrong `working` class in v2 harms a reader, not an agent. That lowers the stakes my QA argument relies on.
- Nothing of v2 exists, PR #539 is still open, and the capture has not run (question.md fact 7); every scenario above is about planning risk, not observed failure.

## Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 (v2 reads the sweep report JSON as a main input) | ACCEPT | V2-01 requires the #423 body to name "sweep report JSON v1" (MR:398 item 4) and V2-03 requires every field's source be named with it as a listed source (MR:400 item 3), so the sweep's classes do matter to v2. |
| A-002 (PR #539 merges close to today's form) | QUALIFY | Q1 (INV-008 fix or accept, MR:1266) is still open; if the ruling changes the class list, all three gates move, and Variant 2's SW-14 moves with it (UNVERIFIED how much Q1 could change the class list). |

## Per-point verdicts

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

## Overall ranking and unassigned pick

Ranking as advocate: Variant 2, then Variant 3, then Variant 1.

Unassigned pick: honestly, I would pick Variant 3. It is the spec's default (MR:541), it gives v2's designers the live values that matter, and it keeps a code PR off a planning gate for an advisory, person-facing v2 (ADJ:294; MR:542). I would make one change borrowed from Variant 2: the V2-02 ledger entry should state whether the recorded values are sufficient for Rule 5's four conditions, so the "unbuildable Rule 5" risk (U-002) is checked at the gate without waiting for SW-14 to merge.
