## Rebuttal: Variant 3 (opus/refactorer)

### Responses to Criticisms

**(a) Silent on C-003 and X-001: CONCEDED.** Variant 3 has no finding, verifier or limitation on Task 1's wording. Its self-audit covers Task 2's helper and the sync delivery (variant-3-original.md:23-26), not plan line 35. Variant 1 is the only card that detects the gap: plan line 35 says "explicitly distinguish", while `source.md:1` says "never New Terminal". The prohibition reaches Task 1 through its Inputs at plan line 30. Variant 1 is also the only card with a verifier for it (variant-1-original.md:22). I make no counter-claim, and both points stay with Variant 1.

**(b) R3-1 is mostly unverified and conditional: CONCEDED IN PART.**

Conceded:
- `tests/cli/test_bash_inspection_policy.py:32`, `tests/cli/test_issue_body_templates.py:18` and `tests/core/test_how_we_work_routing_table.py` are only search leads. The card says so itself (variant-3-original.md:16). They must not be carried into a merged finding as evidence.
- The finding is conditional ("if the new passage affects their assertions", variant-3-original.md:15). No breakage has been shown.

Defended:
- The one verified reader is concrete. `tests/core/test_codegraph_guide.py:137` reads `src/superclaude/core/CLAUDE.md`, the file Task 1 edits.
- Its assertions depend on where a new rule is placed:
  - exactly one row that starts with `| codegraph` (line 149);
  - exactly one marker pair (line 155);
  - the content of the "### Refresh-tool selection" section up to the next `\n### ` heading (lines 162-166);
  - no "serena" anywhere (line 173).
- Plan line 52 names `tests/core/test_claude_md_routing_block.py` but not this file.

What survives is a low-value, low-cost addition to Task 2's wider regression run. It is a verification refinement, not a deviation.

**(c) Brief-local "plan lines 81-82" pathology, and R3-1 lacks a plan_ref: CONCEDED, with one clarification.**
- The card records the brief-local numbers only in its `limitations` (variant-3-original.md:30), as numbers that must not be cited. They never appear as an evidence or plan_ref field.
- R3-2's emitted `plan_ref` is the correct `TASK-WF-fixIssue412SVeri-20261106-215543.md:45-51` (variant-3-original.md:20). Its code anchor is the correct `install_user_setup.py:230-263` (variant-3-original.md:19).
- R3-1 has no `plan_ref`. Its natural anchor would be plan line 52, the wider-regression clause, but the card does not give one. That is why S-001 stays with Variant 1.
- On evidence hygiene, both Variant 1 and Variant 3 self-record a pathology. Variant 1's pathology sits in an emitted source-reference field (variant-1-original.md:17); Variant 3's sits only in its limitations. Variant 3's code anchors are cleaner, but it should not claim to be a different kind of card.

**(d) No empty-output counter-case: CONCEDED.** R3-2's verifier covers only exit 0 with stdout naming a skipped guide (variant-3-original.md:21). It does not guard the opposite mistake: a fix that invents skip text, or withholds a success line, when Orca exits 0 and prints nothing. Variant 1's verifier covers that separately ("test empty-output success separately", variant-1-original.md:16). The merged C-001 verifier should combine R3-2's exit-0 skip fixture and its "no refresh-success claim" assertion with R1-2's empty-output success case.

**(e) "Variant 1 assumes [exit 0] without saying so" (round-1-variant-3.md:66) is wrong: CONCEDED.** R1-2's verifier opens with "Mock exit-zero edited-copy skip with files present" (variant-1-original.md:16). That states the exit-0 mock explicitly. My Round 1 line misread Variant 1's card. Both verifiers rest on the same help text (`orca-discovery.md:21`, `:25`), not on an observed run. A-001 is a tie.

### New Concessions

1. **A-001 moves from Variant 3 to a tie between Variants 1 and 3** (see (e)). The reason given in Round 1 was factually wrong.
2. **C-001 keeps Variant 3 as the winner, with Variant 1's empty-output case merged in** (see (d)). In Round 1 I called Variant 1's framing "vaguer" without crediting its counter-case.
3. **R3-1 should be carried into the merge with only `tests/core/test_codegraph_guide.py` as evidence.** The three leads are dropped, and plan line 52 is the anchor the merge should attach.
4. **C-003 and X-001 belong to Variant 1 with no counter-argument from me.** Variant 3 contributes nothing on Task 1's terminal-surface wording.
5. **Variant 2's U-003 preservation checklist has value that no scored point captures.** I agree with Variant 2's own rebuttal (round-2-variant-2.md:20) that it is unique and of medium value.

### Final Per-Point Positions

- **S-001: Variant 1 (unchanged).** Every finding carries a `plan_ref` and a verifier. R3-1 has no `plan_ref`.
- **S-002: Variant 3 (unchanged).** Its code and test anchors are correct and re-readable (`install_user_setup.py:230-263`, `tests/core/test_codegraph_guide.py:137-174`). Variant 1's emitted range is wrong, and Variant 2 cites only the brief.
- **C-001: Variant 3, with Variant 1's empty-output case merged in (CHANGED: merge note added, winner unchanged).** R3-2 gives the exit-0, three-files-present fixture and the "no refresh-success claim" assertion. R1-2 adds the counter-case.
- **C-002: Variant 3 (unchanged).** It reads plan line 47 as Task 2 delivering the sync, without a finding that has to be retracted. R1-1 is only an optional earlier test run.
- **C-003: Variant 1 (unchanged).** R1-3 is the only verifier that ties the terminal surface to agent creation (plan line 35; `orca-discovery.md:12-16`). Variant 3 is silent.
- **C-004: Variant 3 (unchanged).** It is the only card with a verified extra reader of core CLAUDE.md that plan line 52 does not list. Its three leads are excluded, and its value is low.
- **C-005: Variants 1 and 3 tied (unchanged).** Neither makes an unsupported count. Variant 2's 21/21 is reviewer judgment against the lexical 13/21 = 0.6190 (`diff-analysis.md:34`).
- **X-001: Variant 1 (unchanged).** It is the only card that detects the gap between plan line 35 ("distinguish") and `source.md:1` ("never"). That gap is resolved through plan line 30 Inputs.
- **X-002: Variant 3 (unchanged).** The requirement exists in plan lines 24, 45 and 51; only the exit-0 fixture is missing, and R3-2 names it. Variant 1 overstated the gap, and Variant 2 understated it.
- **A-001: Variants 1 and 3 tied (CHANGED, from Variant 3).** Both verifiers state the exit-0 mock (variant-1-original.md:16; variant-3-original.md:21). Both rest on help text (`orca-discovery.md:21`, `:25`), not on an observed run.
- **A-002: Variant 3 (unchanged).** Its "no refresh-success claim" assertion is the only one aimed at the presence check that passes automatically at `install_user_setup.py:257-258` and the bare success return at `:263`.
