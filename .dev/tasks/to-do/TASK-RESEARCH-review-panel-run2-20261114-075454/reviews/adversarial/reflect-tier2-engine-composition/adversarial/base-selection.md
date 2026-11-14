# Base Selection Report

Slot C-04 (`reflect-tier2-engine-composition`). Variant 1 = Proposal A (`variant-1-original.md`, default model, default persona); Variant 2 = Proposal B (`variant-2-original.md`, default model, default persona). Scoring produced by separate agents: quantitative layer by `quant-score.py` (deterministic; run twice, identical output); qualitative layer by two independent scorers (`score-pass1.md` forward order, `score-pass2.md` reverse order) and a re-evaluator for disagreements (`score-reeval.md`).

## Quantitative Scoring (50% weight)

Source requirements are the eleven IDs named in conflict row C-04 (RE-1, RE-4, CV-8, CV-4, CV-5, INV-A, INV-B, INV-L, INV-M, INV-K, GQ-067). Method and rules: `quant-score.md`; raw output: `quant-score-output.json`.

| Metric | Weight | Variant 1 (Proposal A) | Variant 2 (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 1.0000 (11/11) | 1.0000 (11/11) |
| internal_consistency | 0.25 | 0.9753 (2 contradictions / 81 claim lines) | 0.9683 (2 contradictions / 63 claim lines) |
| specificity_ratio | 0.15 | 1.0000 (concrete / (concrete + vague); vague indicators found: 0) | 1.0000 (concrete / (concrete + vague); vague indicators found: 0) |
| dependency_completeness | 0.15 | 1.0000 (35/35 internal references resolved) | 0.9787 (46/47 internal references resolved) |
| section_coverage | 0.15 | 1.0000 (9/9 H2 sections) | 1.0000 (9/9 H2 sections) |
| **quant_score** | | **0.9938** | **0.9889** |

Sensitivity (IC counted from the diff-analysis intra-variant rows X-008 and X-009 only): Variant 1 0.9969, Variant 2 0.9928; the ordering does not change. The layer is nearly saturated for both variants (RC, SR and SC are 1.0 for both), so it separates them by 0.005 only.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Final verdict per criterion after the two position-bias passes and, where the passes disagreed, the re-evaluation. Evidence is the scorer's CEV evidence supporting the final verdict, shortened; the full CEV blocks are in `score-pass1.md` and `score-pass2.md`, and the re-evaluated pairs are in `score-reeval.md`.

### Completeness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 Covers all explicit requirements | MET | RE-1 is the whole position (section 1, line 19). RE-4 is named and carried as `[UNVERIFIED]`, "not argued" (line 15). CV-8 intent is answered at section 3.5 (line 90). CV-4 is handled by the serializer over the 1.8.0 constants and the 89-of-110 absence (E3, E4, lines 100-101; line 115). CV-5 is at ... | MET | RE-1 is the position (line 24). RE-4 is carried as OQ-20 with the rubric `:39` and 5-versus-6 dimension detail (line 150). CV-8 is answered by correcting the documents (lines 39, 74). CV-4 is stated as a fact (E13, line 72) and as "Engine A's `1.0` contract ... stay as they are" (line 99). CV-5 is ... |
| C2 Addresses edge cases/failures | MET | INV-I row (line 129): a finalizer that cannot write a lint-clean contract makes the run BLOCKED. Section 3.4 (line 83) lists the headless lane's hard-coded constants. M2 (line 139) names what would show A "wrong, or incomplete"; M3 (line 140) covers new failure classes outside the table. | MET | Skipped-helper risk (line 119, line 143); INV-L serializer bug scenario (line 101); M3 seam probe with both outcomes stated (line 121); E9 unestablished child behavior (line 63). |
| C3 Includes dependencies/prerequisites | MET | Section 2 (lines 31-39) lists conditions on C-01, C-02, C-03. INV-A row (line 121): the `reviewer_briefs_materialized` conflict "must be settled first". Line 90: headless exclusion "depends on ... slot C-09". Line 115: GQ-067 needed before 1.0-shaped keys are dropped. | MET | Section 0 (lines 14-20) dependencies on C-01, C-02, C-03 and INV-020 (weaker reading); line 99: the fence allow-list "need[s] ... widened in the same change"; line 149: GQ-067 answer "needed first" for any retirement of engine A. |
| C4 Defines success/completion criteria | MET | Section 6 M1-M5 (lines 138-142). M2 gives pass and fail rules: every recorded run yields a lint-accepted contract and the 19 verdict-read fields are value-equal; "A is wrong, or incomplete, if a recorded failure needs judgment". | MET | Section 5 table (lines 117-122) gives "what counts for Position B / against" per measurement; M1 reuses the exit script's gate rule (3 of 39 = 0.077; parity, lint, leaked keys 0). |
| C5 Specifies out-of-scope items | MET | Line 15 (decided rows "not debated"); line 33 ("A takes no position on the C-06 policy"); line 83 (headless PASS-eligibility "A does not answer"); line 152 (M9, M4, M2 "not provided by A and not blocked by it"). | MET | Line 42 ("What this position leaves as it is, on purpose": `--fix` dormant, T5 gate unchanged); line 40 (`--t2-engine` no new value); line 132 (C-11 "not changed by this position"); section 8 (lines 147-152) open items not closed. |
| **Subtotal** | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 No factual errors or hallucinated claims | NOT MET | The debate verified several defects against code and the A advocate conceded them (round2-advocate-A, debate lines 259-291). (a) Line 81: the grounded lane is "reached ... through the `ClaudeProcess` else-branch (`runner.py:546-572`)". Production Tier 2 never reaches that branch (V-07, ... | NOT MET | Debate verified defects, several conceded by B (round2-advocate-B, debate lines 454-492). (a) Line 34: CV-5 resolved as "engine A's own meaning"; decided row `synth-06:190` calls the count-derived label non-conforming; conceded (R-1, V-08). (b) Line 70 E11 and line 42: engine A "hard-codes" zero ... |
| K2 Feasible with stated constraints | NOT MET | The central "composition" at the reviewer layer is not wired: the else-branch is unreachable for standard or deep depth, the recursion marker at `runner.py:560` silences reflect subcommands in that child, and `reviewer_profile=True` drops the permission bypass (debate W1, N1, N3). Line 141 M4 ("a ... | NOT MET | Line 36: serializer placed in kernel `cli/review/*` "allows only the frozen key list", but the list lives in `cli/reflect/panel_lint.py`; B conceded the placement had no home (debate lines 314, 462). The step-2 parity helper cannot be built: `recompute_parity` is in `scripts/`, not packaged, and ... |
| K3 Terminology consistent and accurate | MET | "Engine A / engine B" versus "Position A" are prefixed throughout (line 5, section 1). `merge_method: adversarial` carries one meaning, "disk-confirmed" (line 87), which matches decided row CV-5 (V-08). GQ-067 is used for the readers question (line 115), matching `synth-10` Q-08 (V-32, X-006 ... | NOT MET | X-006: GQ-067 is the owner question in section 1 (line 24: "GQ-067: 'does the wrapper switch to engine B ...'") and the readers question in section 8 (line 149: "GQ-067 / OQ-8: readers outside `src/superclaude`"); `synth-10` Q-08 supports only the second (V-32). `merge_method: adversarial` has two ... |
| K4 No internal contradictions | NOT MET | X-008 (diff-analysis line 72): INV-M "headless output directories ... Preserved" (line 133) contradicts M4 "a stub-lane run builds its contract through the serializer and passes the lint" (line 141); the lint needs directories the lane lacks (V-28). Line 49 says the shell is kept "unchanged in ... | NOT MET | X-009: section 1(i) "CV-5 `merge_method: adversarial` means a disk-confirmed merge" (line 24) contradicts section 2 "the count-derived label is engine A's own meaning" (line 34). GQ-067 is used for two questions inside the same file (lines 24, 149). |
| K5 Claims supported by evidence or rationale | MET | Section 4.1 evidence table (lines 96-105) pairs each claim with a file:line and a `[CODE-VERIFIED]` or `[UNVERIFIED]` tag. Section 3.2 (lines 62-69) pairs each shadow step with its failure and the code to reuse. Overstatements exist (K1) but the document supplies rationale or a tag for each of its ... | MET | Tag key (line 10) and 22 evidence rows with Evidence and Tag columns (lines 48-91). Unsupported or overstated claims exist (K1), but each claim carries a cited line or a named research source. |
| **Subtotal** | **2/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| S1 Logical section ordering | MET | Conventions (0), position (1), consistency with adjudicated slots (2), design (3), evidence (4), invariants (5), measurement (6), effect on PR/rf-qa (7), objection (8). | MET | Inputs from adjudicated slots (0), position (1), design (2), evidence (3), invariants (4), measurement (5), effect on PR/rf-qa (6), objection (7), open items (8). |
| S2 Consistent hierarchy depth | MET | `##` sections 0-8; `###` subsections only inside 3 (3.1-3.5) and 4 (4.1-4.3); no skipped levels. | MET | `##` sections 0-8; `###` only inside section 3 (3.1-3.5); no skipped levels. |
| S3 Separation of concerns | MET | Design (3), evidence (4), invariants (5), measurement (6) and objection (8) are distinct. Some decisions are tagged inside 3.5 and some evidence sits in 3.x, which blurs the line slightly, but each section keeps one purpose. | MET | Design table (2), five themed evidence tables (3.1-3.5), invariants (4), measurement (5). Section 8 partly repeats items already in section 4, but each section keeps one purpose. |
| S4 Navigation aids present | MET | Section 0 shorthand key (line 14); internal pointers "see 3.5", "section 6, measurement M2" (line 132), "section 4" (line 19), "3.3 and 5" (line 154). | MET | Tag key (line 10); numbered evidence rows E1-E22 referenced from later sections ("E6 to E10", line 141; "E5-E9", line 64); "section 4, items 2 and 3" (line 142). |
| S5 Follows artifact-type conventions | MET | Sections 1, 4, 5, 6, 8 map to the five parts. | MET | Position (1), evidence (3), invariants (4), measurement (5), strongest objection and answer (7). |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 Unambiguous language | MET | Search for "might", "should consider", "as appropriate", "possibly", "probably": no hits. Decisions are stated as conditions ("admissible only if", line 132) and "Endangered, HIGH". | MET | Search for "might", "should consider", "as appropriate", "possibly", "probably": only one "may be" (line 18). Decision rules are stated as conditions (line 124). |
| L2 Concrete rather than abstract | MET | File:line citations in nearly every row (for example line 122 with test names and line numbers); exact commands in 4.2 (line 109). | MET | Line-level citations in every evidence row (for example E11, line 70; E12, line 71) and quoted code in E1 (line 50). |
| L3 Each section has a clear purpose | MET | Section headings and the first sentence of each section state the purpose (e.g. section 2 "Consistency with the adjudicated slots", section 6 "The measurement that would show A right or wrong"). | MET | Section 2 opens "Stated as what each module is under this position"; section 5 "Registered before any run, each with its decision rule"; section 8 "Open items this proposal does not close". |
| L4 Terms defined on first use | NOT MET | INV-A..INV-N are defined only by pointer to "s06 section 6.12.0" (line 14). EV-1 first appears at line 66 ("EV-1 fails on card file names") with no definition; EV-2 never defined; `UC`, `GQ-067`'s meaning only partially (line 115). CV-1..CV-9 and RE-2/RE-3 are glossed inline (line 15), but EV-1 and ... | NOT MET | "T5 gate" (line 42, "production T5 gate") is never defined; EV-1 and EV-2 (lines 71, 80) have no definition; OQ-8, OQ-20 and GQ-067 are partly glossed (line 149-150); INV-A..INV-N are defined only by pointer (line 95). UC-1 and UC-2 are glossed (lines 51-52) and CV rows are glossed in section 1(i), ... |
| L5 Actionable next steps / decision points | MET | Line 31: the "no change to `cli/reflect`" reading "has to be resolved before A can hold". Line 121: settle `reviewer_briefs_materialized` first. Line 115: GQ-067 answer needed. Line 132: code-built contract stays a comparison artifact until M2 passes. | MET | Single-engine trigger stated as a condition: owner answers "the wrapper switches to engine B" or M4 shows unsafe PASS (line 124); M3 probe closes the seam question (line 121); open items list (lines 147-152). |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| R1 At least 3 risks with probability and impact | MET | Invariant table rates three endangered risks with consequence and level: INV-L "Endangered, HIGH" (line 132), INV-B "Endangered, MEDIUM" with the slug and exit-code consequence (line 122), INV-A "Endangered, MEDIUM, until then" (line 121). Levels are one combined severity scale; probability is not ... | NOT MET | Section 4 lists four endangered or open items (lines 107-111) but gives no probability or impact rating; line 109 says only "The exposure is real"; line 101 "Endangered at one point" without a severity. No risk is rated. |
| R2 Mitigation for each risk | MET | INV-L: comparison artifact until M2 passes (line 132). INV-A: settle the conflict first (line 121). INV-B: M1 pins, "each rewritten pin is named with the reason" (line 138). Headless constants: moved "into one place where a lint can see it" (line 83). Cost items: answered in section 8 answer 2 ... | NOT MET | Item 1 (INV-L) is mitigated by the replay check (line 101). Items 2 and 3 (production PASS without a deviation audit; `--fix` dormant) are "documented instead of removed" and "not claim[ed] to fix ... now" (lines 109-110, 142). Item 4 is "needed, not resolved" (line 111). Three of four identified ... |
| R3 Failure modes and recovery | MET | INV-I (line 129) and section 8 answer 4 (line 164): where a finalizer cannot copy it "must fail the run closed, not invent"; INV-L fallback to the legacy writers while the code-built contract is a comparison artifact (line 132). | MET | Line 101: serializer output checked by `scripts/reflect_verdict_replay.py` before it replaces the draft. Line 119 and line 143: if M1 fails because a helper was skipped, "the evidence favours a code-driven parent". Line 121: M3 outcomes each close a reading. Contingency path is stated; recovery is ... |
| R4 External dependencies and their failures | MET | Line 83: "The lane is a runtime property (transport, availability, credit)", stub lane as credit-free fallback (line 52); C-09 tier-source dependency (line 90); GQ-067 external readers (line 115). | MET | Owner answer on GQ-067 (line 124, 149); E9 child-spawn unknown (line 63); C-11 `bypassPermissions` lens agents (line 132); outside-`src/superclaude` readers of engine A keys (line 99). |
| R5 Monitoring or validation mechanism | MET | M1-M5 (lines 138-142); the exit script counts for EV-1, parity and key leaks (M3); the lint as a publish gate (line 68). | MET | M1-M4 table (lines 117-122): 20 fresh runs through the exit script, audit log showing helper calls, static pins, seam probe. |
| **Subtotal** | **5/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| I1 Collection boundary conditions | MET | M4 (line 141): "A one-reviewer stub run still yields `single-reviewer-fallback` and exit 11". Line 55: reflect profile "at most 3 reviewers". C-03 floor `min(2, requested)` (line 29). Single-element and maximum boundaries are both named. | MET | §1(i) and §2 exit-script row: "CV-9 an empty baseline is 'no baseline'", fix at `scripts/reflect_shadow_exit.py:313`; E12 `ensemble.py:773` "reviewer_count >= 2". No treatment of engine A's clamp [2,4] versus the kernel cap 3 (A-004, V-26), nor of 2-of-3 shortfall runs against the parity rule ... |
| I2 State-variable interactions across boundaries | MET | Line 122: `merge_method` set in `ensemble.py:773` changes which trigger fires in `contract.py:295` versus `:299`, with exit code held at 11. Line 81: recursion marker passed to the child at `runner.py:560` (line 105). Line 132: change of writer for the legacy contract. | MET | Line 101: the serializer authoring the authoritative legacy `return-contract.yaml` in shadow mode; line 62 E8 and line 63 E9: `reviewer_profile=True` child flags and agent spawning; line 71 E12: `merge_method` count-derived in `ensemble.py:773` versus EV-2 meaning in `panel_lint`. |
| I3 Guard-condition gaps | MET | Line 68: unquoted `[1m]` aliases inside a YAML flow sequence make 3 contract files unparseable; line 83: headless `verification_ran: False` and zero deviation counts hard-coded; line 129: `None` contract routed BLOCKED. (A missed that its allowlist drops `adversarial_subrun_status`, per V-11, but ... | MET | Line 70 E11: `verification_ran False`, zero deviation counts, `input_drift_detected False` as constants; line 109: "production T5 gate keeps saying PASS without a deviation audit"; line 36: serializer quoting `[` and `]` in model aliases. |
| I4 Count divergence | MET | §4.2 ran the exit script: "shadow runs counted: 13 of 20 required", "shadow 8/13 = 0.615; legacy baseline 3/39 = 0.077", parity failures in six named runs, lint problems in nine; §3.1 "36 test functions ... by `grep -c`"; §4.1 E3 "32 keys counted"; `reviewer_briefs_materialized` correctly on three ... | NOT MET | Counts are cited (36 tests, 507 matches in 44 files, 8 of 13 versus 7 of 28) but no divergence is surfaced. Neither the [2,4] versus 3 reviewer limits (V-26) nor the 137-versus-136 name overlap (INV-008) appears, and "the only importer of swarm" is a miscount (V-03). |
| I5 Interaction effects | MET | Line 76: first `cli/reflect` to `cli/review` import edge. Line 82: the shared finding grammar forces a lens template change. Line 37: the `--fix` loop with cross-round identity would reopen C-02. Line 122: CV-5 edit interacts with derive_verdict order and pins. | MET | Line 99: keeping 9.1 byte-identical and finishing CV-2/CV-3 text edits "pull apart" (comments at `:838-839` inside the frozen block); line 38: edits outside the fence allow-list need the test widened; line 101: the serializer meets INV-L. |
| **Subtotal** | **5/5** | | **4/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 2/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 4/5 |
| **qual_score** | **26/30 = 0.8667** | **22/30 = 0.7333** |

### Edge Case Floor Check

Invariant & Edge Case Coverage: Variant 1 5/5, Variant 2 4/5. Floor is 1/5; both variants are eligible as base.

## Position-Bias Mitigation

Pass 1 evaluated Variant 1 then Variant 2; Pass 2 evaluated Variant 2 then Variant 1. The two passes disagreed on 8 of 60 criterion-variant pairs; each was re-evaluated with the explicit comparison prompt (`score-reeval.md`).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| K2 | Variant 2 | NOT MET | MET | DISAGREE | NOT MET |
| K5 | Variant 1 | MET | NOT MET | DISAGREE | MET |
| L4 | Variant 1 | NOT MET | MET | DISAGREE | NOT MET |
| L4 | Variant 2 | NOT MET | MET | DISAGREE | NOT MET |
| R2 | Variant 1 | MET | NOT MET | DISAGREE | MET |
| R3 | Variant 2 | MET | NOT MET | DISAGREE | MET |
| I1 | Variant 2 | NOT MET | MET | DISAGREE | MET |
| I4 | Variant 1 | NOT MET | MET | DISAGREE | MET |

Disagreements re-evaluated: 8 of 60. Final verdict equals Pass 1 on 6 pairs and Pass 2 on 2 pairs. Agreed pairs: 52 of 60 (86.7%).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (Proposal A) | 0.4969 | 0.4333 | **0.9302** | not needed (S/C/X points won alone: 5 of 40) |
| 2 (Proposal B) | 0.4944 | 0.3667 | **0.8611** | not needed (S/C/X points won alone: 12 of 40) |

**Margin**: 6.91% (above the 5% threshold)
**Tiebreaker applied**: No

Both layers agree in direction (quantitative 0.9938 against 0.9889, qualitative 0.8667 against 0.7333). For the record, the debate's own scoring matrix does not favour Variant 1 by points won: of the 40 S/C/X points, both advocates named Variant 1 on 5, Variant 2 on 12, a Hybrid on 12, Not material on 7, Neither on 1, and 3 stayed unresolved (C-007, C-009, C-018). The tiebreaker was not used, so that count did not enter the selection.

## Selected Base: Variant 1 (Proposal A; `variant-1-original.md`)

### Selection Rationale

Variant 1 scores 0.9302 against 0.8611 for Variant 2, a margin of 6.91% (above the 5% threshold, so no tiebreaker). The qualitative layer decides it: 26/30 against 22/30. The gap comes from Risk Coverage (5/5 against 3/5), where both scorers found no probability-and-impact rating (R1) and no per-risk mitigation (R2) in Variant 2, from Invariant & Edge Case Coverage (5/5 against 4/5), and from Correctness (2/5 against 1/5). On Correctness neither variant is clean. The scorers charged each document with the defects the debate verified against code and that its own advocate conceded: for Variant 1 the unrouted grounded lane (`runner.py:538-545`, X-001), the CV-5 pin collision (`test_ensemble_stub_integration.py:141-168`), the allowlist that would drop `adversarial_subrun_status` (`contract.py:306`), the INV-K edit-fence row and the headless lint-layout conflict (X-008); for Variant 2 the CV-5 wording that reverses the decided row and contradicts its own section 1(i) (X-003, X-009), the uncorrected CV-8 lines, the GQ-067 double use (X-006), the overstated "reuse, not new logic" (V-29) and a kernel placement of the serializer whose frozen field lists live in `cli/reflect/panel_lint.py` (C-002; conceded as a gap in Round 1, defended again with a lazy import in Round 2). The quantitative layer is saturated and separates them by 0.005.

The selection is a choice of base text, not of position. In the debate both advocates moved to one hybrid by Round 2 (H-C04 and H-C04B; 42 of 45 points agreed, 93.33%), and each conceded that neither original proposal survives as written: Variant 1 conceded that its grounded lane has no routing, that "unskippable" holds only under a Python parent, that the CV-5 edit breaks the I1 witness, that the lens change and the headless lint gate leave the design; Variant 2 conceded the CV-5 wording, the M4 measurement, the `audit.log` presence signal and the step-2 parity helper. Variant 1 is the better base to merge into because its invariant table (14 rows), its reopen conditions for C-01, C-02 and C-03, its per-step failure-to-code table and its offline replay oracle are the structures the hybrid is built on, and Variant 2's contributions (staging evidence, seam probe, trigger, disclosure, edit-fence accounting) are additive.

### Strengths to Preserve from Base (Variant 1)

- Section 2 reopen conditions for C-01 (a)-(c), C-02 (the `--fix` loop gaining cross-round finding identity) and the three C-03 dependencies (U-001), corrected by Variant 2's note that 'reflect stays on the v2 kernel' holds only for the skill panel (V-01).
- The per-step table pairing each shadow step with its observed failure and the existing checker (section 3.2, U-002), corrected for the step-2 parity helper that cannot be built from `scripts/` (N2) and for the fact that existing extractors cover one of six `merged-verdict.yaml` fields (V-29).
- The 14-row invariant table with Preserved/Endangered and a reason (S-004), with INV-K corrected (X-007) and INV-L widened to three points.
- The offline replay oracle M2 (U-003), narrowed: the serializer and the `merged-verdict` finalizer on recorded runs, the card writer only where raw reviewer output survived.
- CV-5 worded as 'non-conforming' (decided row `synth-06:190`, V-08), with the slug effect `null-convergence` to `single-reviewer-fallback` (U-004, V-09) and the exit code unchanged.
- The identification of GQ-067 as the readers question (C-010, V-32) and the code location beside `panel_lint.py` so the 137 names are never copied (placement is a disputed sub-point, see the refactor plan).

### Strengths to Incorporate from Non-Base Variant (Variant 2)

- Staging evidence (U-010): engine A is `mode: post` (`ensemble.py:797`), the skill panel is UC-1 shadow only, `panel` is rejected at `SKILL.md:87`, UC-2 is ignored until Stage 5 (`SKILL.md:311`); a stated Stage 5 deadline for the engine decision (B's E-5).
- No capability moves now: engine A, `contract.py`, `ensemble.py` and the 36-test verdict map untouched; the headless lane, lens and layout unchanged; the production T5 PASS disclosed as a convergence-and-diversity result with no deviation audit (U-014, with the corrected sentence 'a tested deviation seam with no production producer').
- The seam probe (U-011, M3) extended to marker set, `reviewer_profile=True`, agent calls complete, files written and a `review` command not suppressed (N3), also run against engine A's own scorer child.
- The single-engine trigger with a decision rule (U-012), minus the M4 prong (M4 cannot discriminate because engine A's reviewers never see a diff, N4); the prong is the disputed sub-point C-009.
- The edit-fence accounting (X-007, U-015): the allow-list at `test_shadow_skill_contract.py:65` widened in the same change, `:838-839` recorded as residue inside frozen 9.1.
- The complete CV-8 document correction, with the lines neither proposal listed (`sc-tasklist-protocol/SKILL.md:1170, :1177`, `task-builder/SKILL.md:2389`) and `:2247` described as what it says (V-18).
- `--t2-engine` gets no new value (C-014, V-30); `reviewer_briefs_materialized` is corrected on three ref lines (C-015, V-16).
- INV-L endangered at three points with comparison siblings first (B's E-1), the kernel's `publish_files` refusal in shadow and unwired `read_committed` (E-2), helper-owned stage advance for three stages only (E-3), and a re-measurement of the prose fixes before any helper is built (E-4).
- The retirement test-mass accounting (U-016) and the named replacement for the I1 fan-out witness (R-5); kernel kept free of swarm (U-017); the open-items list (U-018, S-007).
