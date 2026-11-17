# Base Selection: reviewer-card comparison (plan vs spec, pr-submit merge guard)

## Metadata
- Generated: 2026-11-13 (Step 3 of /sc:adversarial, hybrid scoring; the orchestrator scored, it did not debate)
- Variants: V1 = variant-1-original.md (analyzer, sonnet class), V2 = variant-2-original.md (qa, haiku class), V3 = variant-3-original.md (refactorer, opus class)
- Correctness reference: the debate outcome after Round 2 and the Round 2.5 probe (debate-transcript.md, debate-round1.md, invariant-probe.md)
- Source requirements: spec `source.md` (S) and plan `TASK-WF-designSpec-20261107-075614.md` (P) under `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`; every plan and spec line cited by a variant was re-read for this step

## Quantitative Scoring (50% weight)

### RC: requirement coverage (post-debate defect themes)
The brief lists C-001..C-007, U-001, U-003, U-005, U-006, U-007, INV-001 and INV-002: that is 14 items (12 themes plus the 2 invariant refinements), so the denominator is 14. Scoring per theme: 1 = raised with the disposition the debate kept; 0.5 = raised but with a severity or blocking flag the debate overturned, or only part of an invariant refinement; 0 = not raised, or rejected.

| Theme (debate outcome) | V1 | V2 | V3 |
|---|---|---|---|
| C-001 Task 7 scan vs `_RESOLUTION_SCRIPTS` (MAJOR, blocking) | 1 (F1) | 1 (F3) | 1 (F1) |
| C-002 resume row 4 cannot call `release_decision` (MAJOR, blocking) | 1 (F2 blocking) | 1 (F2 blocking) | 0.5 (F2 non-blocking; conceded) |
| C-003 `draft_guard_unavailable` halt reports `released` (MAJOR, non-blocking) | 1 (F3) | 0.5 (F1 blocking; withdrawn) | 1 (F3) |
| C-004 `user_override` fold row sets no cause (MINOR) | 1 (F4) | 1 (F4) | 1 (F4) |
| C-005 baseline before sync-dev (MINOR) | 1 (F5) | 0 (rejected, later conceded) | 1 (F5) |
| C-006 JSON keys vs `GuardRead` mapping unowned (MINOR) | 1 (F6) | 0 (rejected, later conceded) | 1 (F6) |
| C-007 Wave 0 bullet vs its test (MINOR) | 1 (F7) | 0 (not raised) | 0.5 (F7 MAJOR; withdrawn) |
| U-001 resume row 3 check order (MINOR) | 1 (F8) | 0 | 0 |
| U-003 producer payload untested (MAJOR, non-blocking) | 0 | 1 (F5) | 0 |
| U-005 no fold row sets `cycle_id` (MAJOR, blocking) | 0 | 0 | 1 (F8) |
| U-006 start-text-only byte-identical check (MINOR) | 0 | 0 | 1 (F9) |
| U-007 classification ignores git verbs, `a+b` keys (MINOR) | 0 | 0 | 1 (F10) |
| INV-001 `_repo_scoped` alone is not enough | 0.5 (F1: also `command -v gh` and `die "gh ..."` lines, "limit the scan to real `gh` invocations") | 0 | 0 (F1 says reusing `_repo_scoped` suffices) |
| INV-002 the three extra arguments alone do not close the release gap | 0 (F2 asks only to keep the head proof) | 0 (F2 asks only for the inputs) | 0.5 (F8 names the cycle-id rebind, but step 4 still frames a cycle-2 `target_sha` as the fix) |
| **RC** | **8.5/14 = 0.607** | **4.5/14 = 0.321** | **9.5/14 = 0.679** |

### IC: internal consistency
Claims = entries in the findings-v2 block. Contradictions = a block claim the debate refuted or the variant withdrew (1), or a block claim whose severity or blocking flag the variant withdrew (0.5).
- V1: 9 claims; F9 withdrawn (mis-cited, P:88 makes no three-file claim) = 1. IC = 1 - 1/9 = **0.889**.
- V2: 6 claims; F6 dropped as a plan defect (U-004) = 1; F1 blocking flag withdrawn = 0.5. IC = 1 - 1.5/6 = **0.750**. (Its prose rejections of T1 F5 and F6, later withdrawn, are outside the block and are charged in RC and the correctness rubric instead.)
- V3: 10 claims; F2 non-blocking flag conceded = 0.5; F7 MAJOR withdrawn = 0.5. IC = 1 - 1/10 = **0.900**.

### SR: specificity
Sampled every sentence or bullet of the prose findings; concrete = carries a file:line, test or symbol name, number, or a step-by-step failure sequence.
- V1: 29 of 33 concrete = **0.879** (vague: F3 "Those cases are the gap", F6 "A helper ... is needed", F8 "I found no data loss", F9 "harmless but over-claims").
- V2: 20 of 32 concrete = **0.625** (abstract wording such as "The criterion cannot establish the required release proof through the declared interface"; evidence lists sit at paragraph ends instead of on the claims).
- V3: 37 of 40 concrete = **0.925** (file:line on nearly every claim, a 4-step failure sequence in F8, counts such as "about 43 mirror failures").

### DC: dependency completeness (cited plan and spec lines resolve)
Every distinct plan (P) and spec (S) citation was checked against the two files. Repo-file citations (tests, scripts) were not re-checked and are not counted.
- V1: 26 distinct, 15 resolve, 11 do not: P:157, P:160, P:164 (resume signature, row criteria; real lines P:70, P:73, P:77), P:147 and P:148 (fold and status criteria; real P:60, P:61), P:163 (row 3 reasons; real P:76), P:175 (Task 5 claim; real P:88), S:43-47 (`GuardAction`; real S:82-85), S:49-51 (`GuardRead`; real S:88-91), S:73 (halt line; real S:112), S:90-132 (decision tables; real S:129-171). DC = 15/26 = **0.577**.
- V2: 19 distinct, all resolve (S:107-109, S:112, S:156-166, S:184-185, S:206, S:208, S:221, S:315, S:363, S:377, P:60-62, P:70-77, P:108-114, P:124, P:166, P:168-172, P:199). DC = **1.000**.
- V3: 30 distinct, all resolve (for example S:88-91, S:108, S:139, S:190-206, S:241, S:255, S:377, P:22, P:33, P:137, P:140, P:154, P:182). DC = **1.000**.

### SC: section coverage
Section units across the three cards: metadata header, Verdict, prose Findings, checked-and-clean list, findings-v2 block, model self-report (max 6). V1 has all 6; V2 has no checked-and-clean list (its T1 cross-check paragraph sits inside the prose findings) = 5; V3 has all 6.
- V1 **1.000**, V2 **0.833**, V3 **1.000**.

### Quantitative summary

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.607 | 0.321 | 0.679 |
| IC internal consistency | 0.25 | 0.889 | 0.750 | 0.900 |
| SR specificity | 0.15 | 0.879 | 0.625 | 0.925 |
| DC dependency completeness | 0.15 | 0.577 | 1.000 | 1.000 |
| SC section coverage | 0.15 | 1.000 | 0.833 | 1.000 |
| **quant_score** | | **0.773** | **0.653** | **0.867** |

Computation: V1 = 0.182 + 0.222 + 0.132 + 0.087 + 0.150; V2 = 0.096 + 0.188 + 0.094 + 0.150 + 0.125; V3 = 0.204 + 0.225 + 0.139 + 0.150 + 0.150.

## Qualitative Scoring (50% weight)

30 binary criteria, 6 dimensions x 5. Each MET carries Claim-Evidence-Verdict in one line (claim the card satisfies the criterion, the evidence in the card, verdict). No evidence in the card means NOT MET. The criteria are written for reviewer cards that audit a plan against a spec. Verdicts below are the final ones after the two passes (see Position-Bias Mitigation).

### Completeness

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| CP1 | Raises all three acceptance-contract defects (C-001, C-002, C-003) | MET | MET | MET |
| CP2 | Gives a disposition for every prior-card (T1) finding F1-F7 | MET | NOT MET | MET |
| CP3 | Adds at least one new defect that survived the debate | MET | MET | MET |
| CP4 | Names the specific items checked and found clean | MET | NOT MET | MET |
| CP5 | Findings block mirrors every prose finding one to one | MET | MET | MET |
| | **Subtotal** | **5/5** | **3/5** | **5/5** |

Evidence for MET:
- CP1: V1 F1/F2/F3; V2 F3/F2/F1; V3 F1/F2/F3.
- CP2: V1 "I confirm F4 to F7" plus F1-F3; V3 "Of the card's F1 to F7, all seven are confirmed". (V2 has no word on T1 F7.)
- CP3: V1 F8 (U-001); V2 F5 (U-003); V3 F8, F9, F10 (U-005, U-006, U-007).
- CP4: V1 "Checked and found fine" (5 named checks: decision tables, `guard_status` mapping, import graph, prefixes, `BRANCH_*`); V3 "Checked with no defect found" (dependencies, sync cadence, import cycle, `__init__.py`, named symbols). (V2 says only "the six lexically unmapped rows have plan coverage" without naming them.)
- CP5: V1 9 prose / 9 block; V2 6 / 6; V3 10 / 10.

### Correctness

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| CR1 | No block finding withdrawn or refuted in the debate | NOT MET | NOT MET | NOT MET |
| CR2 | Every plan and spec line citation resolves | NOT MET | MET | MET |
| CR3 | Blocking flags of C-001/C-002/C-003 match the debate (blocking, blocking, non-blocking) | MET | NOT MET | NOT MET |
| CR4 | Rejects no defect the debate confirmed | MET | NOT MET | MET |
| CR5 | Prose and block agree on severity and blocking for each finding | MET | MET | MET |
| | **Subtotal** | **3/5** | **2/5** | **2/5** |

Evidence for MET:
- CR2: V2 19/19 and V3 30/30 resolve (DC above). (V1: 11 of 26 wrong.)
- CR3: V1 F1 `blocking:true`, F2 `blocking:true`, F3 `blocking:false`. (V2 F3-equivalent F1 blocking; V3 F2 non-blocking.)
- CR4: V1 and V3 confirm all of T1 F1-F7. (V2 rejected T1 F5 and F6, both confirmed real.)
- CR5: V1 F1/F2 "blocking" in prose and block, F4-F9 MINOR in both; V2 F1-F3 "MAJOR, blocking" and F4-F6 non-blocking in both; V3 F1 "MAJOR, blocking" and the rest non-blocking in both.
- CR1 is NOT MET for all: V1 F9 withdrawn; V2 F1 blocking flag withdrawn and F6 dropped; V3 F2 flag and F7 severity conceded.

### Structure

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| ST1 | Verdict states readiness up front | NOT MET | MET | MET |
| ST2 | Findings ordered by severity (MAJOR before MINOR) | MET | NOT MET | NOT MET |
| ST3 | Every prose finding has an ID matching its block entry | MET | MET | MET |
| ST4 | Block entries carry every findings-v2 field (id, severity, blocking, category, lens, claim, refs, citations) | MET | MET | MET |
| ST5 | Each finding is labelled as a confirmation of T1 or as new | MET | NOT MET | MET |
| | **Subtotal** | **4/5** | **3/5** | **4/5** |

Evidence for MET:
- ST1: V2 "**NOT READY.**"; V3 "Not ready as written." (V1 opens "The plan covers the spec well" and never states ready or not ready.)
- ST2: V1 F1-F3 MAJOR then F4-F9 MINOR. (V2 F4 MINOR precedes F5 MAJOR; V3 F4-F6 MINOR precede F7/F8 MAJOR.)
- ST3: all three use F1..Fn in prose and block.
- ST4: all block lines carry the eight fields (V1 `refs:[]` present).
- ST5: V1 "(confirmed ...)" / "(new ...)" on every finding; V3 "confirmed" / "new" on every finding. (V2 labels only F1 and F4 as confirmations.)

### Clarity

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| CL1 | At least 80% of findings state the fix or required change | NOT MET | MET | NOT MET |
| CL2 | Block claims are understandable without the prose | MET | MET | MET |
| CL3 | Plain wording, no unexplained shorthand | MET | MET | MET |
| CL4 | Verdict gives counts and the next action | NOT MET | MET | NOT MET |
| CL5 | At least 80% of findings state a concrete failure consequence | MET | MET | MET |
| | **Subtotal** | **3/5** | **5/5** | **3/5** |

Evidence for MET:
- CL1: V2 5 of 6 (F1 "Add an end-to-end reporting criterion", F2 "Specify whether the caller performs the release check", F3 "Make the new scan distinguish", F4 "Add a settle → fold → status assertion", F6 "Add those units"). (V1 5 of 9, V3 5 of 10 explicit.)
- CL2: each block `claim` names the task, the conflicting rule and the result, for example V1 F1, V2 F2, V3 F8.
- CL3: all three write full sentences and spell out the decision rows and fields they refer to.
- CL4: V2 "three blocking acceptance-contract defects, one further test-coverage gap, and two non-blocking omissions ... Revise the reporting, resume-release, and script-scoping criteria before execution." (V1 and V3 give counts but no next action.)
- CL5: V1 F1 "raises StopIteration", F3 "reported as `released`", F5 "would be hidden" (8 of 9); V2 every finding (6 of 6); V3 F8 4-step sequence ending "released while cycle 2's fixes are still local", F10 "only after a failed run" (8 of 10).

### Risk coverage

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| RK1 | Finds a cross-cycle release-safety hazard (a later cycle's unpushed fixes released) | NOT MET | NOT MET | MET |
| RK2 | Finds a check that can pass while the behaviour is wrong (hidden failure) | MET | MET | MET |
| RK3 | Finds a risk of misreporting the guard status to the user | MET | MET | MET |
| RK4 | Places the defect's origin (spec vs plan) so the fix lands in the right document | MET | MET | MET |
| RK5 | States the blast radius or data-loss bound of a finding | MET | NOT MET | MET |
| | **Subtotal** | **4/5** | **3/5** | **5/5** |

Evidence for MET:
- RK1: V3 F8 (S:139, S:108, S:166, S:190-206; the debate kept it MAJOR blocking).
- RK2: V1 F4 "A fold that leaves the cause empty passes Task 3 and mis-reports", F5; V2 F4 "Those tests can pass even when a folded override cannot produce the required status", F5; V3 F5, F9.
- RK3: V1 F3, V2 F1, V3 F3 (no-record halt reports `released`).
- RK4: V1 F2 "The spec or plan must name the action", F4 cites the spec fold row; V2 F3 "inherited by the spec's test-hygiene wording", F4 "the cause omission starts in the spec's fold table"; V3 F1 "The wording comes from the spec itself (source.md:377)", F7 "The spec contradicts itself".
- RK5: V1 F8 "I found no data loss. The result is a possible wrong `not_applied` settle that clears a pending key."; V3 F8 bounds the hazard to one transient read failure plus one crash, F10 "would catch this, but only after a failed run". (V2 states no bound.)

### Invariant & edge case coverage

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| IE1 | Finds an ordering or precedence edge inside a decision table | MET | NOT MET | NOT MET |
| IE2 | Finds a state field that is never set or carried across cycles | NOT MET | NOT MET | MET |
| IE3 | Finds a retry or idempotency-key edge | NOT MET | MET | NOT MET |
| IE4 | Finds the missing-record (`None` guard) edge | MET | MET | MET |
| IE5 | Challenges whether the obvious fix is sufficient | MET | MET | MET |
| | **Subtotal** | **3/5** | **3/5** | **3/5** |

Evidence for MET:
- IE1: V1 F8 "The order of the three checks should be pinned" (resume row 3, S:165).
- IE2: V3 F8 "The fold table never says which event sets the fold's `cycle_id`".
- IE3: V2 F5 "A matcher test with hand-built valid keys would not catch a producer that reuses attempt keys" (S:184).
- IE4: V1 F3, V2 F1, V3 F3 (engage halt writes no record).
- IE5: V1 F1 the scan must also skip `command -v gh` and `die "gh ..."` lines (part of INV-001); V2 F2 "`published=True` proves that a push-completed event exists, not that the current head equals the intended target"; V3 F8 the implementation "had to invent a `REBIND`/`cycle_rebound` action", beyond the three arguments of F2.

### Qualitative summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 3/5 | 5/5 |
| Correctness | 3/5 | 2/5 | 2/5 |
| Structure | 4/5 | 3/5 | 4/5 |
| Clarity | 3/5 | 5/5 | 3/5 |
| Risk coverage | 4/5 | 3/5 | 5/5 |
| Invariant & edge case coverage | 3/5 | 3/5 | 3/5 |
| **qual_score** | **22/30 = 0.733** | **19/30 = 0.633** | **22/30 = 0.733** |

## Position-Bias Mitigation

Pass 1 scored V1, V2, V3 in that order; pass 2 scored V3, V2, V1. The two passes agreed on 84 of 90 verdicts. Each disagreement was re-checked against the criterion text and the card's own words; the re-check verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Re-check and final verdict |
|---|---|---|---|---|
| ST1 readiness up front | V1 | MET | NOT MET | Pass 2, read right after V3's "Not ready as written", noticed V1 never says ready or not ready and opens "The plan covers the spec well" despite two blocking findings. **NOT MET** (changed from pass 1). |
| CL1 fix stated in 80% | V1 | NOT MET | MET | Pass 2 compared V1 with V3 (5 of 10) and leaned lenient. Absolute count: 5 of 9 = 56%. **NOT MET**. |
| RK4 defect origin | V1 | MET | NOT MET | Pass 2 read "The spec or plan must name the action" as a fix location only. F4 names the spec fold row (S:206) as where the cause is missing, which places the origin. **MET**. |
| CP4 checked-clean items | V2 | NOT MET | MET | Pass 2 accepted "I checked all 13 tasks against spec sections 3-8 and 10". The criterion needs named items found clean; V2 names none. **NOT MET**. |
| IE1 precedence edge | V3 | NOT MET | MET | Pass 2 read F8's engage row 7 `NOOP(already_held)` as a precedence edge. F8 is about the outcome of one row and the unset `cycle_id` (credited under IE2), not the order of rows. **NOT MET**. |
| IE5 fix sufficiency | V3 | MET | NOT MET | Pass 2 read F8 step 4 ("Without a cycle-2 `target_sha` (F2)") as saying F2's fix is enough. F8 also says the implementation "had to invent a `REBIND`/`cycle_rebound` action", and the V3 advocate called F8 "independent of C-002". **MET**. |

Disagreements re-checked: 6. Final verdicts that differ from pass 1: 1 (V1 ST1). Pass totals: V1 23 / 22 (final 22), V2 19 / 20 (final 19), V3 22 / 22 (final 22).

## Edge-Case Floor

Rule: a variant scoring below 1/5 on Invariant & edge case coverage cannot be the base.

| Variant | Invariant & edge case coverage | Eligible as base |
|---|---|---|
| V1 | 3/5 | Yes |
| V2 | 3/5 | Yes |
| V3 | 3/5 | Yes |

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final score** | Debate points won (tiebreaker level 1) |
|---|---|---|---|---|
| V1 (analyzer, sonnet class) | 0.773 → 0.386 | 0.733 → 0.367 | **0.753** | 5 outright (C-003, C-006, C-007, X-002, X-003) + shared C-001, A-001 |
| V2 (qa, haiku class) | 0.653 → 0.326 | 0.633 → 0.317 | **0.643** | 2 outright (C-002, C-004) + shared C-001 |
| V3 (refactorer, opus class) | 0.867 → 0.434 | 0.733 → 0.367 | **0.800** | 2 outright (C-005, X-001) + shared C-001, A-001 |

**Margin**: V3 0.800 vs V1 0.753 = 0.047 (4.7 points), below the 5% threshold (`|score_A - score_B| < 0.05`). V2 trails V1 by 0.110.

**Tiebreaker applied**: Yes, level 1 (debate performance). The scoring matrix in debate-transcript.md gives V1 5 of the 13 debate points outright and V3 2; both share C-001 and A-001. That is 38% vs 15%, not tied, so level 1 decides and levels 2 (correctness count: V1 3, V3 2) and 3 (input order: V1) are not needed, although both would also pick V1. The result holds if the verified unique contributions are counted as extra wins (V1 + U-001 = 6, V3 + U-005, U-006, U-007 = 5).

**Sensitivity**: the margin is 0.003 below the threshold. One more MET for V3 (worth 0.017 combined, for example IE1) would lift V3's lead to 0.064 and V3 would be the base on score alone. Moves toward V1 (for example ST1 restored to MET) keep the result: margin 0.031, tiebreaker still picks V1. The two passes and the re-checks above record why each borderline verdict landed where it did.

## Selected Base: V1 (variant-1-original.md, analyzer, sonnet class)

### Selection rationale
- V3 has the highest final score (0.800) and V1 is second (0.753). The gap of 0.047 is inside the 5% band, so the tiebreaker decides, and V1 won the debate: 5 of 13 points outright against V3's 2.
- V1's dispositions are the ones the debate kept. F1 and F2 are blocking, F3 is MAJOR and non-blocking, F7 is MINOR, and T1 F5 and F6 are confirmed. Its blocking flags match the outcome on all three acceptance-contract items (CR3), so the merged verdict can start from V1's severity and blocking columns without re-grading.
- V1 has the best severity order (ST2) and full completeness (5/5). It has a "Checked and found fine" list and a confirmed/new label on every finding.
- V1's main weakness is mechanical and can be fixed: 11 wrong plan and spec line numbers (DC 0.577) and the withdrawn F9. V3's and V2's citations give the correct lines.

### Strengths to preserve from the base (V1)
1. The severity and blocking flags on F1-F7, which match the debate outcome (F1, F2 blocking; F3 MAJOR non-blocking; F4-F7 MINOR).
2. F1's added detail that `command -v gh` and `die "gh ..."` lines also break a naive scan, and that the scan must be limited to real `gh` invocations. This is the start of INV-001.
3. F2's requirement that the spec or plan name the row 4 action (for example `RELEASE_AFTER_PUSH`) and keep the head proof mandatory.
4. F8 (U-001): the resume row 3 check order, including the unreadable-timeline reason, with its "no data loss" bound. Use the debate's narrower reading: the gap is weak evidence for "no toggle landed", not a foreign toggle only.
5. The "Checked and found fine" list and the confirmed/new labels on each finding.

### Required corrections to the base (from the debate, not optional)
1. Drop F9 (withdrawn; the claim sits at P:88, not P:175, and makes no three-file claim).
2. Replace the 11 wrong citations with the lines V2 and V3 use: resume signature P:70; row criteria P:73 and P:77; fold criterion P:60; status criterion P:61; row 3 reasons P:76; `GuardAction` S:82-85; `GuardRead` S:88-91; halt line S:112; decision tables S:129-171.
3. State readiness in the verdict ("not ready": two blocking defects, raised to three by U-005 below).

### Strengths to incorporate from non-base variants
1. **From V3 F8 (U-005, the highest-value item):** no fold row sets `cycle_id` (S:190-206), engage row 7 NOOPs on a held guard (S:139), and `held_cycle_published` keys on `guard.cycle_id` (S:108). Include the 4-step failure sequence. The debate made it MAJOR and **blocking**, while V3 marked it non-blocking.
2. **From the INV-002 refinement, through V3 F8:** adding `cycle_id`, `applied_edits` and `target_sha` to `resume_decision` (C-002) is not enough alone. A `target_sha` taken from cycle 1 still equals the head, so the fold must rebind `cycle_id` for each new cycle. Attach this to V1 F2.
3. **From the INV-001 refinement, extending V1 F1:** reusing `_repo_scoped` covers only the static clause. The runtime clause (the fake-`gh` argument log at P:113) also sees the `gh repo view` fallback, and the static scan needs the `_command_lines` and `_GH_CMD` filters. Take V3 F1's spec-origin note (S:377).
4. **From V2 F5 (U-003):** no criterion checks the guard-event producer payload: the key format `guard:<run_id>:<cycle_id>:<to>:a<k>`, retry numbering, and the first-request and skip fields (S:184-185, P:62, P:124, P:168-172). This is MAJOR and non-blocking.
5. **From V2 F4:** the concrete fix for C-004, a settle → fold → status test for `user_override`.
6. **From V2 F1:** the concrete fix for C-003, an end-to-end reporting criterion for both a failed read and an unreadable timeline at engage. Keep V1's non-blocking flag.
7. **From V3 F7:** the spec origin of C-007 (S:241 says the same thing) and the precise reason: the bullet must contain both `L3` and `draft`. Keep the MINOR severity.
8. **From V3 F10 (U-007, MINOR):** the classification steps in Tasks 7, 8 and 12 (P:108, P:124, P:182) name only `gh pr`/`gh api` with a single verb key. `WRITE_VERB_RE` also matches git write verbs and keys multi-verb lines as `a+b`. P:22 already names the git verbs, so the gap is the wording and key shape of each task.
9. **From V3 F9 (U-006, MINOR):** the byte-identical checks of the S5a and Wave 6 sentences compare only the recorded start text (P:33, P:154).
10. **From V3 F5:** the bound that Task 13's re-run of `make verify-sync` and the two sync-hook test files narrows the baseline gap but does not close it.
11. **From V2's verdict:** the counts-plus-next-action form of the verdict ("Revise the reporting, resume-release, and script-scoping criteria before execution").
12. **Note only, not a finding (U-004, from V2 F6):** the 66-row coverage matrix has no unit for the payload tables or the one-retry contract. The debate judged this real but Low and not a plan defect.
