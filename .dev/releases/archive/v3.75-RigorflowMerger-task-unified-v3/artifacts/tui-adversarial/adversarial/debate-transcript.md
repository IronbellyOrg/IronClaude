# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 3 (Round 1, Round 2, Round 2.5 invariant probe, Round 3)
- Convergence achieved: 0.89 (89%)
- Convergence threshold: 0.85 (85%)
- Focus areas: viability, risk, coverage, blast-radius
- Advocate count: 3 (variants A, B, C — blinded)

---

## Round 1: Advocate Statements

### Variant A Advocate (Round 1)

**Position summary**: P-01 is the keystone; nothing else moves the needle if it stays broken. Slot order is P-01, P-02, P-03, P-07, P-05 with sequencing that ships the cheap fixes first and lands P-01 last for maximum perceived-impact-per-merge.

**Steelman of B**: B's QA lens correctly identifies that internally-correct-but-invisible fixes are wasted work. The "user watches 30 s" frame is a sharp tool for filtering proposals. B's inclusion of Manual Smoke-Test Acceptance Criteria materially raises the quality bar for what shipping means.

**Steelman of C**: C's cost-benefit framing is mathematically sound — if P-05 ships in 1 day for ~30% of §2.2 resolved, that's a higher per-day ROI than P-01's per-day rate. Portfolio-risk analysis favours shipping certain wins before risky bets.

**Strengths claimed**:
1. Identifies the layering correction in P-07 (assistant-text trim relocation from monitor.py to render-time) — neither B nor C surfaces this structural insight. Evidence: A's slot #4 rationale, §2.3 final ¶ + monitor.py:121.
2. Cleanest treatment of P-09 deferral with a steelmanned defence and an explicit "this should be the *next* wave's anchor" note.
3. Self-honest about own-side flaws: flags that P-01 access of `proc._process` couples executor to ClaudeProcess internals — a forward-looking refactor recommendation.

**Weaknesses identified in C**: C's placement of P-05 at #1 over P-01 is a portfolio-risk argument that confuses cost-of-failure with cost-of-engineering. P-05 ships in 1 day and addresses ~30% of *one* symptom; P-01 ships in 2-3 days and addresses ~80% of *two* symptoms. The portfolio analogy breaks because these proposals are not competing for the same engineering slot — they ship in parallel. ROI per day is the wrong axis when both items will ship.

**Weaknesses identified in B**: B's inclusion of P-10 at slot #5 relies on the proposal's sentinel-mitigation footnote (`events_received > 0` gating). That footnote is not a real implementation — it's a sketch. Shipping P-10 with the sentinel means landing dead code on the per-task path until P-01 lands. A and C exclude P-10 for the same reason.

**Concessions**: A's slot #5 (P-05) is the weakest slot in A's own ranking — viability 65 is the lowest in A's top-5. If forced to swap one slot, A would swap P-05 ↔ P-10 with P-10 at #5 *after* P-01 lands and the sentinel issue is resolved.

---

### Variant B Advocate (Round 1)

**Position summary**: User-perceived freshness is the only honest metric for a TUI. Slot order is P-01, P-05, P-02, P-03, P-10 with explicit Manual Smoke-Test Acceptance Criteria per fix. Internally-correct-but-invisible is a disqualifying property.

**Steelman of A**: A's structural-correctness lens correctly identifies the keystone status of P-01 and the layering correction in P-07. The architect's "rank P-07 ahead of P-10 because layering" argument is principled.

**Steelman of C**: C's effort-to-impact ratio framing is the right cost model for a finite engineering team. C's exclusion of P-09 on user-perceptibility grounds is exactly correct.

**Strengths claimed**:
1. P-10 inclusion (slot #5) is defensible *with* the sentinel mitigation — the user-visible value of the heartbeat is uniquely high among the diagnostic widgets. Evidence: P-10 proposal text plus §2.2 ¶3 (Live re-renders every 500 ms).
2. Manual Smoke-Test Acceptance Criteria are a unique contribution that converts a ranking into a testable spec. Neither A nor C provides this.
3. Sequencing rationale explicitly distinguishes "high-frequency visible" (the user looks at the screen for 30 s and sees the spinner) from "high-severity but low-saliency" (a wrong Duration value in a column they might not notice) — this is a saliency-weighted ranking that A and C do not perform.

**Weaknesses identified in A**: A's slot #4 (P-07) is the right structural call but the visible impact is small compared to P-10. The layering correction is invisible to a user; the heartbeat is visible. From the QA lens this is a textbook "structurally correct, perceptually small" trade A makes.

**Weaknesses identified in C**: C's per-day ROI math treats P-05 and P-01 as comparable on per-day return. But the impact is *not* linear in days — P-01's impact only manifests when an entire phase runs, not per-day. The "ROI per day" axis is over-quantified. P-05's ROI is real-time visible; P-01's ROI is per-sprint-run visible.

**Concessions**: P-10 at slot #5 is genuinely contested. If the sentinel mitigation cannot be enforced cleanly in code review, B would swap P-10 out for P-07 (matching A and C). B's confidence in slot #5 is the lowest in B's ranking.

---

### Variant C Advocate (Round 1)

**Position summary**: Effort-to-impact ratio rules. P-05 at #1 (cheapest visible fix), P-02 at #2 (one-line wrong-number fix), P-01 at #3 (M-effort keystone — required but expensive), P-03 at #4, P-07 at #5 as the §2.3-completion bundle with P-03.

**Steelman of A**: A is right that P-01 is the only proposal whose impact is uniquely large among the M-cluster. A's "fireworks landing" sequencing — ship cheap fixes first, land P-01 last — is the same sequencing C derives independently from cost-benefit reasoning. A and C converge on sequencing even when their ranking disagrees.

**Steelman of B**: B's saliency-weighted ranking (high-frequency visible vs low-saliency wrong-number) is a genuinely sharper version of the lens than my per-day ROI math. P-05's visible footprint is large because it occupies the centre of the user's attention; the Duration column is one cell out of many.

**Strengths claimed**:
1. Explicit per-day ROI calculations (P-05 = 30%/day, P-01 = 32%/day) make the cost-benefit reasoning auditable rather than narrative. A and B argue ROI qualitatively; C quantifies.
2. Flagged-L-effort section names the one L-proposal in the file (P-09) and explicitly justifies its exclusion against the lens's own "unless impact is uniquely large" exception clause. Methodologically rigorous.
3. Sequencing is day-by-day (Day 1, Day 1-2, Days 3-5) rather than week-by-week — this is the granularity an engineer scheduling work would use.

**Weaknesses identified in A**: A's ranking of P-01 at #1 over P-05 ignores the per-day ROI tie (P-05 = 0.30/day, P-01 = 0.32/day — within noise). The tie-break of "ship the certain win first" is principled; A's tie-break of "ship the structural keystone first" is also principled. Reasonable engineers disagree here.

**Weaknesses identified in B**: B's inclusion of P-10 at slot #5 is the weakest call across all three variants. The sentinel mitigation in P-10 is a footnote; treating a footnote as a load-bearing design element is fragile. C explicitly held P-10 back for this reason — "effective effort is S+M not S" — and B's own confidence rating for slot #5 is the lowest in B's ranking, confirming the call is unstable.

**Concessions**: C's swap of P-05 to #1 is contested and C acknowledges that the per-day ROI of P-05 and P-01 are "within noise of each other." If the team's priority were maximum-impact rather than minimum-risk, P-01 at #1 is defensible. C would accept P-01 at #1 in mediation.

---

## Round 2: Rebuttals

### Variant A Advocate (Round 2)

**Response to B's critique** ("A's slot #4 (P-07) has small visible impact"):
B is correct that P-07's *individual* visible footprint is small. But P-07 *composes* with P-03 to produce a single user-visible change (full-width §2.3 fix) — the architect lens scores compositional value, not individual-widget value. P-03+P-07 together fix the entire §2.3 symptom; P-03 alone leaves the Agent: line clipped at 80 (monitor.py:121). Replacing P-07 with P-10 means *less* of §2.3 is fixed.

**Response to C's critique** ("portfolio-risk argument confuses cost-of-failure with cost-of-engineering"):
A's original critique was that P-05 and P-01 are not competing for the same engineering slot — they ship in parallel. C does not respond to this directly. Re-reading C's argument: "ship the certain win first" is principled only if there's serialised work. If the team ships P-05 in week 1 *and* P-01 in weeks 1-3 simultaneously, the order-of-completion is identical to ranking P-01 first. The ranking matters for *prioritisation under resource constraint*, not for sequencing under parallel work.

**Updated assessment**: A concedes the per-day ROI argument is mathematically close to a tie (per C's quantification) and concedes that the "ship certain wins first" framing has merit. A's ranking of P-01 at #1 is therefore weakened from "structurally obvious" to "preferred under one defensible methodology". A would now accept *either* P-01 at #1 or P-05 at #1 as the merged outcome — but insists on consistent sequencing (P-05 ships first, P-01 lands last) regardless of which is ranked #1.

**New evidence**: §2.1 explicitly identifies the per-task path as "the modern code path used by virtually every current sprint" — the *frequency weighting* of P-01's impact is the impact applied to ~100% of current sprints. This frequency factor is not in C's per-day ROI math and tips the impact axis toward P-01. A maintains P-01 at #1 with this added evidence but acknowledges the call is close.

---

### Variant B Advocate (Round 2)

**Response to A's critique** ("P-10 sentinel mitigation is a footnote, not a real implementation"):
B accepts this critique partially. The sentinel mitigation needs to be promoted from a footnote to a P-10 acceptance criterion. B's Manual Smoke-Test Acceptance section already requires "heartbeat must NOT ship before P-01, OR ship with the proposal's sentinel fix" — this *is* a load-bearing requirement, not a footnote. But A is correct that the original proposal text treats it as an option, not a requirement. The merged shortlist should make the sentinel mandatory if P-10 is included.

**Response to C's critique** ("P-10 effective effort is S+M not S"):
C is right. The effective cost of P-10 *including the prerequisite that makes it meaningful* is S+M ≈ 3.5 days. C's exclusion of P-10 from the top-5 on this basis is methodologically consistent. B's inclusion of P-10 in slot #5 assumed P-10 lands *after* P-01 has shipped — but in a top-5 ranking, the question is "should this be in the next 5 shipped?" not "is it valuable in isolation?". If we treat the top-5 as the *next 5 PRs*, P-10 ships only after P-01, which means it competes with the 6th-best proposal for slot #5. P-04 and P-07 are stronger 5th picks than P-10 under that framing.

**Updated assessment**: B concedes P-10 should be demoted from slot #5 to slot #6. The replacement at slot #5 is P-07 (matching A and C). B's revised ranking: P-01, P-05, P-02, P-03, P-07. P-10 moves to "Held back, ship as #6 immediately after P-01."

**New evidence**: B's Manual Smoke-Test Acceptance criteria for P-10 (the "heartbeat reads 0.0s ago forever" failure mode) are *evidence* that P-10's visible-value-without-P-01 is negative. A widget that lies to the user is worse than no widget. This confirms C's "effective effort S+M" critique with a user-perceived failure-mode argument.

---

### Variant C Advocate (Round 2)

**Response to A's critique** ("ROI per day is the wrong axis when both items will ship"):
A is partially right. ROI per day matters for prioritisation under resource constraint *and* for review-cycle scheduling. Even if P-05 and P-01 ship in parallel, *one of them merges first* — and the one that merges first is the one users see first. P-05 merges in 1 day, P-01 merges in 2-3 days. The user's first impression of "this got better" is owned by whichever ships first. Ranking #1 should be the proposal that *delivers value first*, even if both ship in parallel. By that test, P-05 at #1 is correct.

**Response to B's critique** ("ROI per day over-quantifies — P-01 is per-sprint-run visible, P-05 is real-time visible"):
B is correct that the units of impact differ. P-05 ticks at 10 Hz; P-01's improvement manifests across a phase's duration. C's per-day math collapsed both onto a single axis. The correct framing is *time-to-first-visible-improvement*: P-05 produces visible motion within 500 ms of TUI start (the first Live refresh); P-01 produces visible motion when the first NDJSON event arrives (~1-3 s after subprocess launch). On time-to-first-visible-motion, P-05 still wins by ~1 s, but the win is much smaller than ROI-per-day suggests. C concedes the ROI math was over-tight.

**Updated assessment**: C concedes the per-day ROI tie between P-05 and P-01 is "within noise". C's ranking of P-05 at #1 is defensible under "ship certain wins first" but A's ranking of P-01 at #1 is equally defensible under "rank by total impact". C accepts P-01 at #1 in mediation provided the *sequencing* (P-05 ships first day-by-day) is preserved.

**New evidence**: The convergence between A's sequencing recommendation (ship P-05 first, land P-01 last) and C's sequencing (Day 1 = P-05, Days 3-5 = P-01) is independent of the ranking dispute. Two variants with different ranking methodologies producing identical sequencing is strong evidence the sequencing is correct.

---

## Round 2.5: Invariant Probe (AD-1)

Fault-finder agent probes the emerging consensus for boundary-condition violations and hidden assumptions.

**Emerging consensus** (entering Round 2.5):
- All three variants converge on a 5-proposal slate: P-01, P-02, P-03, P-05, P-07
- Variant B has conceded P-10 → P-07, eliminating the P-10 contradiction (X-002 resolved)
- Variants A and C converge on sequencing: ship P-05 first, ship P-01 last
- Variants disagree on rank #1 (A says P-01, C says P-05, B accepts either) — this is the residual contradiction

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The OutputMonitor's `_last_read_pos` can be safely reset between tasks without losing in-flight events that the subprocess has written but the monitor hasn't yet read | UNADDRESSED | HIGH | Round 1 A's risk callout; P-01 proposal text "per-task subprocess writes to a shared NDJSON file so the monitor's incremental-read pointer must be reset between tasks (otherwise it skips the first task's output)". A's mitigation is stated but unverified against monitor.py reset semantics. |
| INV-002 | state_variables | `phase_started_at` (models.py:609) is correctly populated on the per-task path either by `monitor.reset(...)` or by the TUI fallback the P-02 proposal sketches | UNADDRESSED | MEDIUM | P-02 proposal text admits the fallback ("wire `phase_started_at` from the TUI side via `time.monotonic()` captured at first observation of `phase` change") effectively introduces a second writer. Round 1 A flagged this as a code-smell. Not blocking but should be cleaned up. |
| INV-003 | guard_conditions | Rich's `Spinner` object embedded in a `Table.add_row` cell is correctly rendered by `box=None` tables | ADDRESSED | LOW | P-05 proposal flags this and recommends a smoke test. A's R1 explicitly accepts this as low-risk. Rich's source confirms `Table` accepts `RenderableType` cells. Not a blocker. |
| INV-004 | count_divergence | `Phase.prompt_preview` bumped to `[:240]` does not break any downstream consumer that assumes `≤60` chars | UNADDRESSED | MEDIUM | P-03 proposal proposes the bump but does not audit downstream consumers. A R1 flagged this explicitly: "Downstream consumers that assume ≤60 (e.g. log formatters, error reporters) need an audit. No such audit is included." Could surface bugs at log/serialisation boundaries. |
| INV-005 | collection_boundaries | The `_seen_files` set in OutputMonitor handles empty/single-element/post-reset cases without skipping the first event of a freshly-started task | UNADDRESSED | HIGH | Same evidence base as INV-001 — proposal-stated hazard with stated-but-unverified mitigation. The empty/single-element edge case of `_seen_files` after `.clear()` is not exercised by current tests according to A R1's flag on test fixtures. |
| INV-006 | interaction_effects | The combination of P-03 (extraction caps to 240) + P-07 (monitor stores full assistant text) + P-05 (spinner in render tree) does not introduce any rendering ordering conflict (e.g. spinner refresh + width recompute on resize firing simultaneously) | ADDRESSED | LOW | All three changes are in distinct render-tree positions and do not share state. The spinner cycles via Live's tick; width is recomputed per `_render()` call. No shared mutable state. C R1 implicitly accepts this; A's slot rationale confirms compositionality. |
| INV-007 | guard_conditions | `Live`'s 2 Hz auto-refresh continues to work correctly when the render tree contains a `Spinner` object that mutates its frame index on each render call — i.e. there is no infinite-refresh loop where `Live` repaints because the Spinner changed and the Spinner changes because `Live` repainted | ADDRESSED | MEDIUM | This is Rich's documented design — `Spinner.render()` is idempotent except for the frame index; `Live` does not re-trigger on render-tree mutation, only on its own clock. C R1's "spinner advances under Live without external push" is correct per Rich docs. |

**Summary**:
- Total findings: 7
- ADDRESSED: 3
- UNADDRESSED: 4
  - HIGH: 2 (INV-001, INV-005)
  - MEDIUM: 2 (INV-002, INV-004)
  - LOW: 0

**HIGH UNADDRESSED items**: INV-001 and INV-005 both concern OutputMonitor reset semantics on the per-task path. They are essentially the same hazard expressed against two different invariants (`_last_read_pos` and `_seen_files`). **This blocks convergence under the invariant_probe_gate.**

**Resolution required**: Round 3 must address the OutputMonitor reset hazard before convergence can be declared.

---

## Round 3: Final Arguments

Triggered by:
1. Pre-Round-2.5: Convergence at ~0.83 (still below 0.85 threshold; rank-#1 dispute residual)
2. Round 2.5: HIGH UNADDRESSED INV-001 and INV-005 block convergence regardless of score

### Variant A Advocate (Round 3)

**Address INV-001 and INV-005 (OutputMonitor reset hazard)**:
The cleanest mitigation is to make the reset a documented, tested part of the P-01 implementation contract. Concretely:
1. Add a unit test `tests/sprint/test_monitor_reset_between_tasks.py` that:
   - Writes 3 events for task 1, calls `monitor.reset(...)`, writes 3 events for task 2
   - Asserts that `monitor.state.events_received == 6` after both tasks
   - Asserts that `_last_read_pos` is at the correct file offset after each reset
2. Make `monitor.reset(...)` idempotent against partial-read state — if called mid-task, it must finish the in-flight read before resetting.
3. Promote the reset call to a public method `OutputMonitor.reset_for_next_task()` that wraps the `_last_read_pos = 0; _seen_files.clear()` operation behind a name that documents intent.

This converts the HIGH UNADDRESSED hazard into an ADDRESSED design contract. The cost is small (~0.3 day for the test + the rename) and is added to P-01's effort estimate (M-effort → M+epsilon, still M).

**Final position**: P-01 at #1, P-05 at #2, P-02 at #3, P-03 at #4, P-07 at #5. P-10 → slot #6 follow-on. Sequencing: P-05 ships first day-by-day, P-01 lands last for fireworks landing. INV-001/005 absorbed into P-01's design contract via the test-driven mitigation above.

### Variant B Advocate (Round 3)

**Address INV-001 and INV-005**:
Agree with A's test-driven mitigation. From the QA lens, the acceptance criterion for P-01 must explicitly include: "NDJSON event count from the file matches TUI-displayed count within 1, across a 3-task phase boundary." B's R1 Manual Smoke-Test already states this; promote it from a smoke-test to a unit-test contract per A's mitigation. The HIGH UNADDRESSED hazard is downgraded to MEDIUM ADDRESSED when this test exists.

**Address INV-002 (phase_started_at dual writers)**: Accept the medium hazard. The cleanup belongs in a follow-on PR once P-01 has cemented the monitor's per-task lifecycle.

**Address INV-004 (prompt_preview 60→240 downstream audit)**: Accept. P-03 PR description must include a grep audit of `prompt_preview` usage. Cost: 15 minutes.

**Final position**: P-01 at #1, P-05 at #2, P-02 at #3, P-03 at #4, P-07 at #5. P-10 explicitly moved to slot #6 follow-on with mandatory sentinel mitigation if it ships. Matches A's final ranking exactly.

### Variant C Advocate (Round 3)

**Address INV-001 and INV-005**:
Accept A's mitigation. The added cost (~0.3 day) moves P-01's effort estimate from "2-3 days" to "2.3-3.3 days" — still M-tier. The effort-to-impact ratio is unchanged within rounding. C accepts that the mitigation absorbs the HIGH hazards.

**Address INV-002 and INV-004**: Accept B's resolution. The 15-minute audit cost for INV-004 is trivial. INV-002 is a code-smell, not a defect — defer to follow-on.

**Concession on rank #1**: C concedes that with the INV-001/005 hazards now addressed, P-01's confidence increases. The portfolio-risk argument for P-05 at #1 weakens. C accepts P-01 at #1 in the merged outcome, *provided* the sequencing (P-05 ships first, P-01 lands last for the wave climax) is preserved. The ranking is a methodological tiebreak; the sequencing is the actionable output.

**Final position**: P-01 at #1, P-05 at #2, P-02 at #3, P-03 at #4, P-07 at #5. Sequencing: Day 1 P-05; Day 1-2 P-02 + P-03+P-07 combined PR; Days 3-5 P-01 with the INV-001/005 unit test contract. Matches A and B exactly.

---

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 (top-section order) | Tie | N/A | All three identical |
| S-002 (methodology formula) | A | 60% | A's formula is most generally applicable; B and C optimise for one lens. Methodology details are persona-specific so winner is a soft preference. |
| S-003 (held-back count) | Tie | N/A | All three are 5 |
| S-004 (distinctive sections) | B | 75% | B's Manual Smoke-Test Acceptance Criteria are universally useful; C's L-effort flagging is methodologically rigorous but narrower in audience |
| S-005 (sequencing labels) | C | 65% | Day-numbered labels are more actionable than week-numbered |
| C-001 (slot #1 proposal) | A and B (P-01 at #1) | 85% | Round 3 convergence: C concedes P-01 at #1. INV-001/005 mitigation closes the portfolio-risk gap. |
| C-002 (treatment of P-07) | A and C (P-07 in top-5) | 95% | Round 2 convergence: B concedes P-10 → P-07 swap. 3-of-3 agreement. |
| C-003 (treatment of P-10) | A and C (P-10 held back) | 90% | Round 2: B concedes P-10 → slot #6 follow-on. 3-of-3 agreement. |
| C-004 (sequencing of P-01) | Tie | N/A | All three agree P-01 ships last among the top-5. Unanimous. |
| X-001 (slot #1 contradiction) | RESOLVED | 85% | Round 3: C concedes P-01 at #1. Sequencing preserved (P-05 ships first). |
| X-002 (P-10 inclusion) | RESOLVED | 95% | Round 2: B concedes P-10 → slot #6. 3-of-3 agreement on P-07 at slot #5. |
| U-001 (B's Manual Smoke-Test) | Incorporate | 95% | Universally agreed valuable; all three Round 3 positions reference it as a quality bar |
| U-002 (C's per-day ROI quantification) | Incorporate | 80% | Useful for decision audit; should be summarised not reproduced in full |
| U-003 (A's layering critique on P-07) | Incorporate | 90% | Architect-lens-specific but agreed by B and C as a valid structural argument |
| A-001 (root-cause diagnosis accuracy) | All three accept | 100% | Stated assumption confirmed across all three |
| A-002 (test rebaseline serialisation) | Accept with caveat | 70% | Round 2: all three implicitly accept that snapshot-test rebaselines can be combined per-PR. Caveat: bundle P-05+P-02+P-03+P-07 across 2-3 PRs not 5. |
| A-003 (reset semantics implementable) | Resolved by INV-001/005 mitigation | 85% | Round 3: A's test contract mitigation explicitly addresses this. Promoted from UNSTATED to STATED. |
| A-004 (effort labels accurate) | Accept with caveat | 75% | Round 3: P-01 nudged from M to M+epsilon by INV mitigation cost. No other label disputed. |

---

## Convergence Assessment

**Pre-Round-2.5 convergence**: 0.83 (below 0.85 threshold). Rank-#1 dispute (X-001) was the residual blocker.

**Round 2.5 invariant probe**: identified 2 HIGH UNADDRESSED items (INV-001, INV-005) which blocked convergence regardless of score (invariant_probe_gate).

**Round 3**: All three advocates accepted A's test-driven mitigation for INV-001/005, downgrading both to ADDRESSED. C conceded rank #1 to P-01. Final ranking is unanimous: P-01, P-05, P-02, P-03, P-07.

**Post-Round-3 convergence**: 0.89 (above 0.85 threshold).

**Taxonomy coverage gate**: 
- L1 (surface): S-005 (sequencing labels) — covered
- L2 (structural): C-001, C-002, S-002, U-003 — covered
- L3 (state-mechanics): A-003, INV-001, INV-005 — covered
- All three levels addressed.

**Invariant probe gate**: HIGH UNADDRESSED count = 0 (both downgraded in Round 3). Gate passed.

**Status**: CONVERGED

**Unresolved points**: 0 (all rank disputes resolved; all HIGH invariants addressed; one MEDIUM invariant INV-004 accepted with 15-minute audit task; one MEDIUM invariant INV-002 accepted as follow-on cleanup).
