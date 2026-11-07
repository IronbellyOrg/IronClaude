## Rebuttal: Variant 2 (haiku/qa)

### Responses to Criticisms

**(a) No anchoring to the plan or the code (S-002): CONCEDED.** The card's only evidence is `reviewer-briefs/reviewer-2.md:49-82` and `:137` (variant-2-original.md:19-20). The card's own limitation says it worked from the "Supplied brief only" (variant-2-original.md:22). Its claims can be traced to the plan only by mapping them afterwards. In Round 1 I did that mapping myself to plan lines 22-23, 36-37, 45 and 50-52 and to `install_user_setup.py:236-262`. That mapping is advocate work, not card evidence, and it earns the card no anchoring credit.

**(b) 21/21 against the lexical 13/21 (C-005): CONCEDED, and I change my Round 1 position.** In Round 1 I gave C-005 to Variant 2, "qualified". That was wrong. C-005 asks which card makes the soundest coverage claim. Variant 2's own limitation, "full matrix completeness not independently checked" (variant-2-original.md:22), undercuts its count. The lexical 13/21 = 0.6190 (`diff-analysis.md:34`) is the only measured figure. A count that cannot be checked cannot win the point. Variants 1 and 3 make no such claim, so they tie.

**(c) "Child output" marked covered, the hazard not named, no exit-0 skip fixture (C-001/X-002): CONCEDED.** The code shows the hazard directly:
- `install_user_setup.py:245-251` captures output with `capture_output=True`.
- Lines 257-263 read only `result.returncode` and file presence.
- `result.stdout` and `result.stderr` are never used anywhere in lines 230-263.

The card's "child output" entry (variant-2-original.md:12) correctly records that the plan requires relaying output (plan line 45). The card never says the current code throws that output away. Its verifier says only "output" (variant-2-original.md:16).

A test suite could satisfy that verifier with nonzero-exit, missing-file and timeout cases. It would still miss the case where all three files are present, Orca exits 0 after skipping a guide, and line 263 reports success. Plan line 51 ("including when files already exist") and plan line 24 forbid exactly that outcome. Variant 3's R3-2 names that case (variant-3-original.md:21). Variant 1's R1-2 also states the exit-0 mock (variant-1-original.md:16) and adds the empty-output counter-case.

**(d) Accepted the "distinguish" wording at face value (X-001): CONCEDED.** The card's self-audit says Task 1 covers the "shell distinction" (variant-2-original.md:13). Plan line 35 says "explicitly distinguish". `source.md:1` says "use Claude (CLI), never New Terminal". The prohibition reaches Task 1 only through its Inputs (plan line 30, "the explicit launch requirement in source.md"). Variant 2 did not see this gap, and Variant 1 did.

**(e) 0 of 11 points: CONCEDED, with one correction to the record.** My Round 1 statement claimed one point, C-005, qualified. Under (b) I now withdraw that claim, so Variant 2 holds 0 of 11 in every advocate's final tally. A per-point win measures a distinct contribution, not whether the verdict is right. Variant 2's distinct contribution, U-003, is the preservation checklist and the separation of mocked checks from live ones (diff-analysis U-003). It is unique and of medium value, but no scored point measures it. All three Round 1 statements already acknowledge it (round-1-variant-1.md:9, round-1-variant-3.md:15).

**Does "zero minor findings is a defensible verdict" survive? In part.**
- **PASS with no blocking findings survives in full.** All three cards and all three advocates agree. The plan already states:
  - the safe-skip requirement (lines 24, 45 and 51);
  - the force gate (line 45, "Existing files may short-circuit only when force is false");
  - the ban on forwarding external `--force` (lines 23 and 50);
  - the mocked-versus-live separation (line 52);
  - the launch requirement, through Task 1's Inputs (line 30).

  No card found drift or a regression in the plan.
- **"Zero minor findings is complete" does not survive.** A minor finding is the place to record a verification gap. At least two real gaps exist and are now agreed:
  - the missing exit-0, all-files-present skip fixture (X-002);
  - the AC wording that is weaker than the source on New Terminal (X-001).

  Variant 2 recorded neither. What survives is narrower: Variant 2 found no plan defect that requires a plan change. That is consistent with the other cards, since all of their minors are verifier refinements. But it is not a complete review.

### New Concessions

1. **C-005 moves from Variant 2 to Variants 1 and 3 tied** (see (b)).
2. **A-001 moves from Variant 3 to a tie between Variants 1 and 3.** Variant 1's rebuttal is correct. R1-2's verifier opens with "Mock exit-zero edited-copy skip with files present" (variant-1-original.md:16), and R3-2's verifier also states exit 0 (variant-3-original.md:21). Both rest on the same help text (`orca-discovery.md:21`, `:25`). My Round 1 reasoning ("its verifier is built directly on the exit-0 skip") applied to both cards, not only Variant 3.
3. **C-001 keeps Variant 3 as the winner, but the merge should add Variant 1's empty-output case.** That case stops a fix from inventing skip text when Orca printed nothing. My Round 1 line did not credit it.
4. **Variant 2's preservation checklist was assembled from the brief, not checked against the code.** In Round 1 I matched it to `install_user_setup.py:238`, `:249`, `:240`, `:253-256` and `:259-262`. That match is mine, made in this debate, not the card's.

### Final Per-Point Positions

- **S-001: Variant 1 (unchanged).** Every finding carries a `plan_ref` and a verifier. Variant 2's verifiers are one top-level list with no plan references.
- **S-002: Variant 3 (unchanged).** It is the only card whose code anchors are correct (`install_user_setup.py:230-263`). Variant 1's range is wrong, and Variant 2 cites only the brief.
- **C-001: Variant 3, with Variant 1's empty-output case merged in (unchanged winner, merge note added).** R3-2 names the exit-0, three-files-present fixture plus the no-refresh-success assertion. R1-2 adds the counter-case.
- **C-002: Variant 3 (unchanged).** It reads plan line 47 as Task 2 delivering the sync, without raising a finding that then has to be retracted.
- **C-003: Variant 1 (unchanged).** R1-3 is the only verifier that ties the terminal surface to agent creation (plan line 35; `orca-discovery.md:12-16`).
- **C-004: Variant 3 (unchanged).** It is the only card to raise this, with one verified reader and its other leads labelled as unverified.
- **C-005: Variants 1 and 3 tied (CHANGED, from Variant 2 qualified).** Neither makes an unsupported count. Variant 2's 21/21 is reviewer judgment against the lexical 13/21 = 0.6190.
- **X-001: Variant 1 (unchanged).** It is the only card to detect the gap between plan line 35 ("distinguish") and `source.md:1` ("never"). That gap is resolved through plan line 30 Inputs.
- **X-002: Variant 3 (unchanged).** The requirement exists (plan lines 24, 45 and 51); only the exit-0 fixture is missing. Variant 2 understated the gap by marking output covered.
- **A-001: Variants 1 and 3 tied (CHANGED, from Variant 3).** Both verifiers state the exit-0 mock, and both rest on help text (`orca-discovery.md:21`, `:25`), not on an observed run.
- **A-002: Variant 3 (unchanged).** Its "no refresh-success claim" assertion is the only one aimed at the presence check that is trivially satisfied at `install_user_setup.py:257-258` and the bare success return at `:263`.
