ORDER: Variant 1 then Variant 2

# Qualitative Score, Pass 1 (forward order), slot C-04 reflect-tier2-engine-composition

Scorer inputs: variant-1-original.md (Proposal A, "compose"), variant-2-original.md (Proposal B, "reconcile at the contract"), diff-analysis.md (ledger V-01..V-34), debate-transcript.md (Round 2 concessions, scoring matrix), invariant-probe.md, and conflict row C-04 (RE-1, RE-4, CV-8 intent, CV-4, CV-5; INV-A, INV-B, INV-L, INV-M, INV-K). CV-4 was read from `synthesis/synth-06-conflict-log.md:189` ("any engine feeding the consumers emits the 1.8.0-shaped, consumer-read fields"). Line numbers cite the variant files. The debate is used only as evidence about correctness and gaps.

## PART 1: Variant 1 (Proposal A)

### V1 Completeness

**V1-C1**
CLAIM: Covers all explicit requirements of the C-04 row (conflicts and invariants).
EVIDENCE: RE-1 is the whole position (section 1, line 19). RE-4 is named and carried as `[UNVERIFIED]`, "not argued" (line 15). CV-8 intent is answered at section 3.5 (line 90). CV-4 is handled by the serializer over the 1.8.0 constants and the 89-of-110 absence (E3, E4, lines 100-101; line 115). CV-5 is at line 87. INV-A, INV-B, INV-K, INV-L, INV-M each have a row (lines 121, 122, 131, 132, 133). RE-4 is only deferred, but it is addressed explicitly.
VERDICT: MET

**V1-C2**
CLAIM: Addresses edge cases and failure scenarios.
EVIDENCE: INV-I row (line 129): a finalizer that cannot write a lint-clean contract makes the run BLOCKED. Section 3.4 (line 83) lists the headless lane's hard-coded constants. M2 (line 139) names what would show A "wrong, or incomplete"; M3 (line 140) covers new failure classes outside the table.
VERDICT: MET

**V1-C3**
CLAIM: Includes dependencies and prerequisites.
EVIDENCE: Section 2 (lines 31-39) lists conditions on C-01, C-02, C-03. INV-A row (line 121): the `reviewer_briefs_materialized` conflict "must be settled first". Line 90: headless exclusion "depends on ... slot C-09". Line 115: GQ-067 needed before 1.0-shaped keys are dropped.
VERDICT: MET

**V1-C4**
CLAIM: Defines success and completion criteria.
EVIDENCE: Section 6 M1-M5 (lines 138-142). M2 gives pass and fail rules: every recorded run yields a lint-accepted contract and the 19 verdict-read fields are value-equal; "A is wrong, or incomplete, if a recorded failure needs judgment".
VERDICT: MET

**V1-C5**
CLAIM: Specifies what is explicitly out of scope.
EVIDENCE: Line 15 (decided rows "not debated"); line 33 ("A takes no position on the C-06 policy"); line 83 (headless PASS-eligibility "A does not answer"); line 152 (M9, M4, M2 "not provided by A and not blocked by it").
VERDICT: MET

### V1 Correctness

**V1-K1**
CLAIM: No factual errors or hallucinated claims.
EVIDENCE: The debate verified several defects against code and the A advocate conceded them (round2-advocate-A, debate lines 259-291). (a) Line 81: the grounded lane is "reached ... through the `ClaudeProcess` else-branch (`runner.py:546-572`)". Production Tier 2 never reaches that branch (V-07, `runner.py:538-545`); conceded "IN FULL" (W1). (b) Line 122: CV-5 change rated "MEDIUM", pins unverified. The I1 witness `test_ensemble_stub_integration.py:141-168` turns from PASS to DEGRADED; conceded (W3, V-10). (c) Line 131: INV-K says edits stay under `### 4.3a`, but line 88 edits `:703, :1317, :1481`; conceded (W11, V-15). (d) Line 162: "The new code is the write side only"; existing extractors cover 1 of 6 `merged-verdict` fields (V-29); conceded (W7). (e) Line 68: allowlist of the two constants drops `adversarial_subrun_status` read at `contract.py:306` (V-11); conceded (W4).
VERDICT: NOT MET

**V1-K2**
CLAIM: Technical approaches are feasible under the stated constraints.
EVIDENCE: The central "composition" at the reviewer layer is not wired: the else-branch is unreachable for standard or deep depth, the recursion marker at `runner.py:560` silences reflect subcommands in that child, and `reviewer_profile=True` drops the permission bypass (debate W1, N1, N3). Line 141 M4 ("a stub-lane run ... passes the lint") cannot hold because the lint reads `panel/manifest.json`, `reviewer-cards/`, `audit.log`, which the headless lane does not create (V-28, X-008). A said "The grounded lane leaves the design" in Round 2.
VERDICT: NOT MET

**V1-K3**
CLAIM: Terminology is used consistently and accurately.
EVIDENCE: "Engine A / engine B" versus "Position A" are prefixed throughout (line 5, section 1). `merge_method: adversarial` carries one meaning, "disk-confirmed" (line 87), which matches decided row CV-5 (V-08). GQ-067 is used for the readers question (line 115), matching `synth-10` Q-08 (V-32, X-006 resolved for A).
VERDICT: MET

**V1-K4**
CLAIM: No internal contradictions.
EVIDENCE: X-008 (diff-analysis line 72): INV-M "headless output directories ... Preserved" (line 133) contradicts M4 "a stub-lane run builds its contract through the serializer and passes the lint" (line 141); the lint needs directories the lane lacks (V-28). Line 49 says the shell is kept "unchanged in behaviour" while line 87 changes `ensemble.py:773`. Line 131 INV-K "edits stay under `### 4.3a`" versus line 88 reconciling prose at `:703, :839, :1317, :1481` (X-007).
VERDICT: NOT MET

**V1-K5**
CLAIM: Claims are supported by evidence or rationale in the document.
EVIDENCE: Section 4.1 evidence table (lines 96-105) pairs each claim with a file:line and a `[CODE-VERIFIED]` or `[UNVERIFIED]` tag. Section 3.2 (lines 62-69) pairs each shadow step with its failure and the code to reuse. Overstatements exist (K1) but the document supplies rationale or a tag for each of its claims.
VERDICT: MET

### V1 Structure

**V1-S1**
CLAIM: Logical section ordering.
EVIDENCE: Conventions (0), position (1), consistency with adjudicated slots (2), design (3), evidence (4), invariants (5), measurement (6), effect on PR/rf-qa (7), objection (8).
VERDICT: MET

**V1-S2**
CLAIM: Consistent hierarchy depth.
EVIDENCE: `##` sections 0-8; `###` subsections only inside 3 (3.1-3.5) and 4 (4.1-4.3); no skipped levels.
VERDICT: MET

**V1-S3**
CLAIM: Clear separation of concerns between sections.
EVIDENCE: Design (3), evidence (4), invariants (5), measurement (6) and objection (8) are distinct. Some decisions are tagged inside 3.5 and some evidence sits in 3.x, which blurs the line slightly, but each section keeps one purpose.
VERDICT: MET

**V1-S4**
CLAIM: Navigation aids (cross-references, index) present.
EVIDENCE: Section 0 shorthand key (line 14); internal pointers "see 3.5", "section 6, measurement M2" (line 132), "section 4" (line 19), "3.3 and 5" (line 154).
VERDICT: MET

**V1-S5**
CLAIM: Follows position-paper conventions (position, evidence, invariants, measurement, objection).
EVIDENCE: Sections 1, 4, 5, 6, 8 map to the five parts.
VERDICT: MET

### V1 Clarity

**V1-L1**
CLAIM: Unambiguous language.
EVIDENCE: Search for "might", "should consider", "as appropriate", "possibly", "probably": no hits. Decisions are stated as conditions ("admissible only if", line 132) and "Endangered, HIGH".
VERDICT: MET

**V1-L2**
CLAIM: Concrete rather than abstract.
EVIDENCE: File:line citations in nearly every row (for example line 122 with test names and line numbers); exact commands in 4.2 (line 109).
VERDICT: MET

**V1-L3**
CLAIM: Each section has a one-sentence purpose.
EVIDENCE: Section headings and the first sentence of each section state the purpose (e.g. section 2 "Consistency with the adjudicated slots", section 6 "The measurement that would show A right or wrong").
VERDICT: MET

**V1-L4**
CLAIM: Acronyms and domain terms defined on first use.
EVIDENCE: INV-A..INV-N are defined only by pointer to "s06 section 6.12.0" (line 14). EV-1 first appears at line 66 ("EV-1 fails on card file names") with no definition; EV-2 never defined; `UC`, `GQ-067`'s meaning only partially (line 115). CV-1..CV-9 and RE-2/RE-3 are glossed inline (line 15), but EV-1 and several others are not.
VERDICT: NOT MET

**V1-L5**
CLAIM: Actionable next steps or decision points are identified.
EVIDENCE: Line 31: the "no change to `cli/reflect`" reading "has to be resolved before A can hold". Line 121: settle `reviewer_briefs_materialized` first. Line 115: GQ-067 answer needed. Line 132: code-built contract stays a comparison artifact until M2 passes.
VERDICT: MET

### V1 Risk Coverage

**V1-R1**
CLAIM: At least 3 risks with probability and impact assessment.
EVIDENCE: Invariant table rates three endangered risks with consequence and level: INV-L "Endangered, HIGH" (line 132), INV-B "Endangered, MEDIUM" with the slug and exit-code consequence (line 122), INV-A "Endangered, MEDIUM, until then" (line 121). Levels are one combined severity scale; probability is not stated separately.
VERDICT: MET

**V1-R2**
CLAIM: Mitigation for each identified risk.
EVIDENCE: INV-L: comparison artifact until M2 passes (line 132). INV-A: settle the conflict first (line 121). INV-B: M1 pins, "each rewritten pin is named with the reason" (line 138). Headless constants: moved "into one place where a lint can see it" (line 83). Cost items: answered in section 8 answer 2 (line 162).
VERDICT: MET

**V1-R3**
CLAIM: Failure modes and recovery procedures.
EVIDENCE: INV-I (line 129) and section 8 answer 4 (line 164): where a finalizer cannot copy it "must fail the run closed, not invent"; INV-L fallback to the legacy writers while the code-built contract is a comparison artifact (line 132).
VERDICT: MET

**V1-R4**
CLAIM: External dependencies and their failure scenarios.
EVIDENCE: Line 83: "The lane is a runtime property (transport, availability, credit)", stub lane as credit-free fallback (line 52); C-09 tier-source dependency (line 90); GQ-067 external readers (line 115).
VERDICT: MET

**V1-R5**
CLAIM: Monitoring or validation mechanism for risk detection.
EVIDENCE: M1-M5 (lines 138-142); the exit script counts for EV-1, parity and key leaks (M3); the lint as a publish gate (line 68).
VERDICT: MET

### V1 Invariant and Edge Case Coverage

**V1-I1**
CLAIM: Boundary conditions for collections (empty, single, maximum).
EVIDENCE: M4 (line 141): "A one-reviewer stub run still yields `single-reviewer-fallback` and exit 11". Line 55: reflect profile "at most 3 reviewers". C-03 floor `min(2, requested)` (line 29). Single-element and maximum boundaries are both named.
VERDICT: MET

**V1-I2**
CLAIM: State-variable interactions across component boundaries.
EVIDENCE: Line 122: `merge_method` set in `ensemble.py:773` changes which trigger fires in `contract.py:295` versus `:299`, with exit code held at 11. Line 81: recursion marker passed to the child at `runner.py:560` (line 105). Line 132: change of writer for the legacy contract.
VERDICT: MET

**V1-I3**
CLAIM: Guard condition gaps (missing validation, unguarded type assumptions).
EVIDENCE: Line 68: unquoted `[1m]` aliases inside a YAML flow sequence make 3 contract files unparseable; line 83: headless `verification_ran: False` and zero deviation counts hard-coded; line 129: `None` contract routed BLOCKED. (A missed that its allowlist drops `adversarial_subrun_status`, per V-11, but it does identify other guard gaps.)
VERDICT: MET

**V1-I4**
CLAIM: Count divergence (off-by-one, ranges, count mismatches).
EVIDENCE: The document distinguishes run populations (13 counted, 28 recorded, 13 of 20 required; lines 109, 114) but does not check the count rules across the combined engines. Line 55 cites "at most 3 reviewers" for the kernel profile while keeping the headless lane, whose runner clamps `--reviewers` to [2,4] (V-26, `config.py:335`); the mismatch is not noticed (shared assumption A-004). "110 stable plus 27 telemetry" is carried as 137 although one name is in both tuples (V-05; invariant-probe INV-008).
VERDICT: NOT MET

**V1-I5**
CLAIM: Interaction effects when features or components combine.
EVIDENCE: Line 76: first `cli/reflect` to `cli/review` import edge. Line 82: the shared finding grammar forces a lens template change. Line 37: the `--fix` loop with cross-round identity would reopen C-02. Line 122: CV-5 edit interacts with derive_verdict order and pins.
VERDICT: MET

## PART 2: Variant 2 (Proposal B)

### V2 Completeness

**V2-C1**
CLAIM: Covers all explicit requirements of the C-04 row (conflicts and invariants).
EVIDENCE: RE-1 is the position (line 24). RE-4 is carried as OQ-20 with the rubric `:39` and 5-versus-6 dimension detail (line 150). CV-8 is answered by correcting the documents (lines 39, 74). CV-4 is stated as a fact (E13, line 72) and as "Engine A's `1.0` contract ... stay as they are" (line 99). CV-5 is at lines 24 and 34. INV-A, INV-B, INV-L, INV-M, INV-K each have a row (lines 99-103). CV-4 is covered but its resolution leaves engine A at 1.0, against decided row CV-4 (see K2).
VERDICT: MET

**V2-C2**
CLAIM: Addresses edge cases and failure scenarios.
EVIDENCE: Skipped-helper risk (line 119, line 143); INV-L serializer bug scenario (line 101); M3 seam probe with both outcomes stated (line 121); E9 unestablished child behavior (line 63).
VERDICT: MET

**V2-C3**
CLAIM: Includes dependencies and prerequisites.
EVIDENCE: Section 0 (lines 14-20) dependencies on C-01, C-02, C-03 and INV-020 (weaker reading); line 99: the fence allow-list "need[s] ... widened in the same change"; line 149: GQ-067 answer "needed first" for any retirement of engine A.
VERDICT: MET

**V2-C4**
CLAIM: Defines success and completion criteria.
EVIDENCE: Section 5 table (lines 117-122) gives "what counts for Position B / against" per measurement; M1 reuses the exit script's gate rule (3 of 39 = 0.077; parity, lint, leaked keys 0).
VERDICT: MET

**V2-C5**
CLAIM: Specifies what is explicitly out of scope.
EVIDENCE: Line 42 ("What this position leaves as it is, on purpose": `--fix` dormant, T5 gate unchanged); line 40 (`--t2-engine` no new value); line 132 (C-11 "not changed by this position"); section 8 (lines 147-152) open items not closed.
VERDICT: MET

### V2 Correctness

**V2-K1**
CLAIM: No factual errors or hallucinated claims.
EVIDENCE: Debate verified defects, several conceded by B (round2-advocate-B, debate lines 454-492). (a) Line 34: CV-5 resolved as "engine A's own meaning"; decided row `synth-06:190` calls the count-derived label non-conforming; conceded (R-1, V-08). (b) Line 70 E11 and line 42: engine A "hard-codes" zero deviations; `build_reflect_contract` takes them as parameters (`ensemble.py:722-749`); conceded (R-4). (c) Line 129: "the only importer of swarm stays `cli/reflect/ensemble.py`"; `fallback.py` and `_diversity.py` also import swarm (V-03). (d) Line 36 and E17: "Reuse, not new logic"; extractors cover 1 of 6 fields and `recompute_parity` is outside the wheel (V-29; N2 HOLDS; conceded twice). (e) Line 38: "two inline comments" at `:838-839`; only `:839` is a comment (V-15).
VERDICT: NOT MET

**V2-K2**
CLAIM: Technical approaches are feasible under the stated constraints.
EVIDENCE: Line 36: serializer placed in kernel `cli/review/*` "allows only the frozen key list", but the list lives in `cli/reflect/panel_lint.py`; B conceded the placement had no home (debate lines 314, 462). The step-2 parity helper cannot be built: `recompute_parity` is in `scripts/`, not packaged, and needs the finished contract (N2 HOLDS; B dropped it). M4 (line 122) is vacuous because engine A reviews the tasklist body only; B conceded and dropped it (R-4). Line 99 leaves engine A at contract 1.0, while decided CV-4 says any engine feeding consumers emits 1.8.0-shaped fields.
VERDICT: NOT MET

**V2-K3**
CLAIM: Terminology is used consistently and accurately.
EVIDENCE: X-006: GQ-067 is the owner question in section 1 (line 24: "GQ-067: 'does the wrapper switch to engine B ...'") and the readers question in section 8 (line 149: "GQ-067 / OQ-8: readers outside `src/superclaude`"); `synth-10` Q-08 supports only the second (V-32). `merge_method: adversarial` has two meanings (line 24 versus line 34, X-009).
VERDICT: NOT MET

**V2-K4**
CLAIM: No internal contradictions.
EVIDENCE: X-009: section 1(i) "CV-5 `merge_method: adversarial` means a disk-confirmed merge" (line 24) contradicts section 2 "the count-derived label is engine A's own meaning" (line 34). GQ-067 is used for two questions inside the same file (lines 24, 149).
VERDICT: NOT MET

**V2-K5**
CLAIM: Claims are supported by evidence or rationale in the document.
EVIDENCE: Tag key (line 10) and 22 evidence rows with Evidence and Tag columns (lines 48-91). Unsupported or overstated claims exist (K1), but each claim carries a cited line or a named research source.
VERDICT: MET

### V2 Structure

**V2-S1**
CLAIM: Logical section ordering.
EVIDENCE: Inputs from adjudicated slots (0), position (1), design (2), evidence (3), invariants (4), measurement (5), effect on PR/rf-qa (6), objection (7), open items (8).
VERDICT: MET

**V2-S2**
CLAIM: Consistent hierarchy depth.
EVIDENCE: `##` sections 0-8; `###` only inside section 3 (3.1-3.5); no skipped levels.
VERDICT: MET

**V2-S3**
CLAIM: Clear separation of concerns between sections.
EVIDENCE: Design table (2), five themed evidence tables (3.1-3.5), invariants (4), measurement (5). Section 8 partly repeats items already in section 4, but each section keeps one purpose.
VERDICT: MET

**V2-S4**
CLAIM: Navigation aids present.
EVIDENCE: Tag key (line 10); numbered evidence rows E1-E22 referenced from later sections ("E6 to E10", line 141; "E5-E9", line 64); "section 4, items 2 and 3" (line 142).
VERDICT: MET

**V2-S5**
CLAIM: Follows position-paper conventions.
EVIDENCE: Position (1), evidence (3), invariants (4), measurement (5), strongest objection and answer (7).
VERDICT: MET

### V2 Clarity

**V2-L1**
CLAIM: Unambiguous language.
EVIDENCE: Search for "might", "should consider", "as appropriate", "possibly", "probably": only one "may be" (line 18). Decision rules are stated as conditions (line 124).
VERDICT: MET

**V2-L2**
CLAIM: Concrete rather than abstract.
EVIDENCE: Line-level citations in every evidence row (for example E11, line 70; E12, line 71) and quoted code in E1 (line 50).
VERDICT: MET

**V2-L3**
CLAIM: Each section has a one-sentence purpose.
EVIDENCE: Section 2 opens "Stated as what each module is under this position"; section 5 "Registered before any run, each with its decision rule"; section 8 "Open items this proposal does not close".
VERDICT: MET

**V2-L4**
CLAIM: Acronyms and domain terms defined on first use.
EVIDENCE: "T5 gate" (line 42, "production T5 gate") is never defined; EV-1 and EV-2 (lines 71, 80) have no definition; OQ-8, OQ-20 and GQ-067 are partly glossed (line 149-150); INV-A..INV-N are defined only by pointer (line 95). UC-1 and UC-2 are glossed (lines 51-52) and CV rows are glossed in section 1(i), but EV-1, T5 and others are not.
VERDICT: NOT MET

**V2-L5**
CLAIM: Actionable next steps or decision points are identified.
EVIDENCE: Single-engine trigger stated as a condition: owner answers "the wrapper switches to engine B" or M4 shows unsafe PASS (line 124); M3 probe closes the seam question (line 121); open items list (lines 147-152).
VERDICT: MET

### V2 Risk Coverage

**V2-R1**
CLAIM: At least 3 risks with probability and impact assessment.
EVIDENCE: Section 4 lists four endangered or open items (lines 107-111) but gives no probability or impact rating; line 109 says only "The exposure is real"; line 101 "Endangered at one point" without a severity. No risk is rated.
VERDICT: NOT MET

**V2-R2**
CLAIM: Mitigation for each identified risk.
EVIDENCE: Item 1 (INV-L) is mitigated by the replay check (line 101). Items 2 and 3 (production PASS without a deviation audit; `--fix` dormant) are "documented instead of removed" and "not claim[ed] to fix ... now" (lines 109-110, 142). Item 4 is "needed, not resolved" (line 111). Three of four identified risks have no mitigation.
VERDICT: NOT MET

**V2-R3**
CLAIM: Failure modes and recovery procedures.
EVIDENCE: Line 101: serializer output checked by `scripts/reflect_verdict_replay.py` before it replaces the draft. Line 119 and line 143: if M1 fails because a helper was skipped, "the evidence favours a code-driven parent". Line 121: M3 outcomes each close a reading. Contingency path is stated; recovery is thin but present.
VERDICT: MET

**V2-R4**
CLAIM: External dependencies and their failure scenarios.
EVIDENCE: Owner answer on GQ-067 (line 124, 149); E9 child-spawn unknown (line 63); C-11 `bypassPermissions` lens agents (line 132); outside-`src/superclaude` readers of engine A keys (line 99).
VERDICT: MET

**V2-R5**
CLAIM: Monitoring or validation mechanism for risk detection.
EVIDENCE: M1-M4 table (lines 117-122): 20 fresh runs through the exit script, audit log showing helper calls, static pins, seam probe.
VERDICT: MET

### V2 Invariant and Edge Case Coverage

**V2-I1**
CLAIM: Boundary conditions for collections (empty, single, maximum).
EVIDENCE: No treatment of one-reviewer, empty-reviewer, or maximum reviewer cases. Line 71 quotes `reviewer_count >= 2` only as evidence that the label is count-derived. Reviewer-count limits ([2,4] versus 3, V-26) are not mentioned. 20-run counts are measurement sizes, not collection boundaries.
VERDICT: NOT MET

**V2-I2**
CLAIM: State-variable interactions across component boundaries.
EVIDENCE: Line 101: the serializer authoring the authoritative legacy `return-contract.yaml` in shadow mode; line 62 E8 and line 63 E9: `reviewer_profile=True` child flags and agent spawning; line 71 E12: `merge_method` count-derived in `ensemble.py:773` versus EV-2 meaning in `panel_lint`.
VERDICT: MET

**V2-I3**
CLAIM: Guard condition gaps.
EVIDENCE: Line 70 E11: `verification_ran False`, zero deviation counts, `input_drift_detected False` as constants; line 109: "production T5 gate keeps saying PASS without a deviation audit"; line 36: serializer quoting `[` and `]` in model aliases.
VERDICT: MET

**V2-I4**
CLAIM: Count divergence.
EVIDENCE: Counts are cited (36 tests, 507 matches in 44 files, 8 of 13 versus 7 of 28) but no divergence is surfaced. Neither the [2,4] versus 3 reviewer limits (V-26) nor the 137-versus-136 name overlap (INV-008) appears, and "the only importer of swarm" is a miscount (V-03).
VERDICT: NOT MET

**V2-I5**
CLAIM: Interaction effects when features or components combine.
EVIDENCE: Line 99: keeping 9.1 byte-identical and finishing CV-2/CV-3 text edits "pull apart" (comments at `:838-839` inside the frozen block); line 38: edits outside the fence allow-list need the test widened; line 101: the serializer meets INV-L.
VERDICT: MET

## Verdict Table

| Criterion | Variant 1 | Variant 2 |
|---|---|---|
| C1 | MET | MET |
| C2 | MET | MET |
| C3 | MET | MET |
| C4 | MET | MET |
| C5 | MET | MET |
| K1 | NOT MET | NOT MET |
| K2 | NOT MET | NOT MET |
| K3 | MET | NOT MET |
| K4 | NOT MET | NOT MET |
| K5 | MET | MET |
| S1 | MET | MET |
| S2 | MET | MET |
| S3 | MET | MET |
| S4 | MET | MET |
| S5 | MET | MET |
| L1 | MET | MET |
| L2 | MET | MET |
| L3 | MET | MET |
| L4 | NOT MET | NOT MET |
| L5 | MET | MET |
| R1 | MET | NOT MET |
| R2 | MET | NOT MET |
| R3 | MET | MET |
| R4 | MET | MET |
| R5 | MET | MET |
| I1 | MET | NOT MET |
| I2 | MET | MET |
| I3 | MET | MET |
| I4 | NOT MET | NOT MET |
| I5 | MET | MET |

## Subtotals

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness (C1-C5) | 5/5 | 5/5 |
| Correctness (K1-K5) | 2/5 | 1/5 |
| Structure (S1-S5) | 5/5 | 5/5 |
| Clarity (L1-L5) | 4/5 | 4/5 |
| Risk Coverage (R1-R5) | 5/5 | 3/5 |
| Invariant & Edge Case Coverage (I1-I5) | 4/5 | 3/5 |
| **Total** | **25/30** | **21/30** |

Edge-case floor check (Invariant & Edge Case Coverage >= 1/5 for eligibility as base): Variant 1 = 4/5, PASS; Variant 2 = 3/5, PASS. Both are eligible as base.

Notes for the lead: (1) The Correctness failures are the debate-verified defects: Variant 1 lines 81, 122, 131, 162, 68 (conceded in round2-advocate-A W1, W3, W11, W7, W4); Variant 2 lines 34, 70, 129, 36 (conceded in round2-advocate-B R-1, R-4, N2, R-2). (2) R1 for Variant 1 is the closest call: its HIGH/MEDIUM ratings are one severity scale with no separate probability. A strict reading would set it NOT MET and give Variant 1 24/30. (3) Neither document defines EV-1, which is why L4 is NOT MET for both.
