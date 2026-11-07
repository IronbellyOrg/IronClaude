## Rebuttal: Variant 1 (sonnet/analyzer)

### Responses to Criticisms

**(a) R1-2 "not precisely defined" overstates: CONCEDED (unchanged from Round 1).** Plan line 24 ("Meaningful installer output must remain visible. Do not treat a safe skip as proof that the guide refreshed"), line 45 ("Relay meaningful Orca stdout/stderr ... reuse existing result fields without a new parser") and line 51 ("including when files already exist") define the requirement. What is missing is the exit-0 skip test fixture, not the requirement. The merged finding should use Variant 3's wording for the claim. Counter-point: R1-2's verifier (variant-1-original.md:16) still holds and adds the separate empty-output success case, which R3-2 does not have. That case stops a fix from inventing skip text when Orca printed nothing. The verifier should be merged even though the claim text is replaced.

**(b) Citation pathology: CONCEDED.** R1-2's `original_source_ref` is unusable. The card itself records this in `evidence_pathology` (variant-1-original.md:18), and the real helper is `install_user_setup.py:230-263`. The only code anchor carried into the merge for R1-2 is 230-263. S-002 stays with Variant 3.

**(c) R1-1 low value; C-002 to Variant 3: PARTLY CONCEDED.** Both cards read plan line 47 the same way. Variant 1's own note says "Task 2 explicitly delivers synchronization for Task 1 README; not an omission" (variant-1-original.md:12), and Variant 3's self-audit says "Task 2 sync delivers its README edit" (variant-3-original.md:25). So the reading of the plan is not in dispute. The difference is that Variant 1 wrapped a correct reading in a finding it then had to retract. Variant 3 stated the same reading without creating a finding. On the C-002 point I now give it to Variant 3. R1-1 survives only as an optional ordering suggestion: run Task 1's guidance and routing-block tests (plan line 52 names `tests/core/test_claude_md_routing_block.py`) right after Task 1, so a broken edit to core CLAUDE.md shows up before Task 2 begins. This changes no required scope and is not a deviation.

**(d) A-001 to Variant 3: REBUTTED IN PART.** Variant 3's Round 1 statement says, for A-001, that "Variant 1 assumes the same thing without saying so" (round-1-variant-3.md:66). That is factually wrong. R1-2's verifier begins "Mock exit-zero edited-copy skip with files present" (variant-1-original.md:16). Both cards state the exit-0 mock explicitly. The remaining differences:
- Variant 1's fixture names the documented cause of a skip, an edited copy (`orca-discovery.md:21`: "A copy you changed ... is skipped and is reported").
- Variant 3's fixture names the documented symptom, stdout naming a skipped guide.

Both rest equally on `orca-discovery.md:25` ("Exits 1 when a location failed or changed while it ran; skipped folders are warnings"). A-001 is about whether exit 0 can hide a skip, not about whether a success message is printed. That second question is A-002, which goes to Variant 3. So I move A-001 from a narrow Variant 1 lead to a tie. I do not concede it outright, because the stated reason for awarding it to Variant 3 rests on a misreading of Variant 1's card.

**Other criticisms raised in Round 1:**
- *Variant 2: R1-3's verifier is stronger than the literal AC (round-1-variant-2.md:46).* Accepted as accurate, but it does not weaken R1-3. The prohibition is part of Task 1 through its Inputs (plan line 30, "the explicit launch requirement in source.md"; `source.md:1`, "never New Terminal"). Plan line 35's last sentence ("Explicit terminal surface is named only when a CLI session is required") already ties the terminal surface to agent creation. R1-3 checks what the plan's Inputs require and does not invent scope. Variant 1 flagged that the merge must settle the difference (variant-1-original.md:30).
- *Variant 3: the X-001 limitation wording is confusing and leaves the question unresolved (round-1-variant-3.md:30).* Conceded in part. Card line 30 correctly separates the stronger "reviewer wording" from the literal AC ("distinguish"), but it does not resolve the question through plan line 30 Inputs. The diff analysis resolves it (`diff-analysis.md:43`). Variant 1 should get credit for detecting the gap, not for resolving it.

### New Concessions

1. **C-002 moves to Variant 3** (see (c)).
2. **A-001 moves from ACCEPT to QUALIFY.** Both other advocates note that the exit-0-on-skip behavior comes from installed help text (`orca-discovery.md:21`, `:25`), not from an observed run, and `orca-discovery.md:29-30` says no install was executed. I agree. The assumption is documented behavior, not verified behavior. It is still a sound basis for a mocked test fixture.
3. **R3-1 has more substance than I credited.** Variant 3's Round 1 statement lists specific assertions in `tests/core/test_codegraph_guide.py` that a carelessly placed new rule could break. That file is outside my permitted ground-truth set, so I did not re-read those line numbers. I do not dispute them, and I do not repeat them as my own citations. C-004 stays with Variant 3.
4. **Variant 1's strength on X-001 and C-003 comes from detection, not reading.** The self-audit says only the brief was read (variant-1-original.md:24). The ground-truth confirmation comes from plan lines 30 and 35, `source.md:1` and `orca-discovery.md:12-16`, all re-read for this debate. Variant 1 read none of them when it made the card.

### Final Per-Point Positions

- **S-001: Variant 1 (unchanged).** Every finding carries a `plan_ref` and a verifier. Variants 2 and 3 agree.
- **S-002: Variant 3 (unchanged).** Its code anchors (`install_user_setup.py:230-263`) are correct. Variant 1's are wrong, and Variant 2 cites only the brief.
- **C-001: Variant 3, with Variant 1's empty-output case merged in (unchanged).** R3-2 gives the accurate claim and the "no refresh-success claim" assertion. R1-2 adds the counter-case.
- **C-002: Variant 3 (CHANGED).** Both cards read plan line 47 the same way, but Variant 3 does so without a retracted finding. R1-1 is kept only as an optional earlier test run.
- **C-003: Variant 1 (unchanged).** R1-3 is the only verifier tying the terminal surface to agent creation (plan line 35; `orca-discovery.md:12-16`). Both other advocates agree.
- **C-004: Variant 3 (unchanged).** It is the only card that raises this, and it has one verified reader.
- **C-005: Variants 1 and 3 tied (unchanged).** Neither asserts an unsupported count. Variant 2's 21/21 is reviewer judgment against a lexical 13/21 = 0.6190 (`diff-analysis.md:34`).
- **X-001: Variant 1 (unchanged).** It is the only card that detects the gap between plan line 35 "distinguish" and `source.md:1` "never". The resolution is through plan line 30 Inputs (`diff-analysis.md:43`). All three advocates agree.
- **X-002: Variant 3 (unchanged).** The requirement is defined in plan lines 24, 45 and 51, and only the exit-0 fixture is missing. Variant 1 overstated the gap.
- **A-001: Variants 1 and 3 tied (CHANGED, from a narrow Variant 1 lead).** Both verifiers state the exit-0 mock explicitly (variant-1-original.md:16; variant-3-original.md:21), and both rest on documented help text, not on an observed run.
- **A-002: Variant 3 (unchanged).** Its "no refresh-success claim" assertion is the only one aimed at the presence check that is trivially satisfied at `install_user_setup.py:257-258` and the bare success return at `:263`.
