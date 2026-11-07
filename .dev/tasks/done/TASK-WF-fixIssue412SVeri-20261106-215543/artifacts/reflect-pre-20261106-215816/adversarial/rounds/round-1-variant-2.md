## Advocate: Variant 2 (haiku/qa)

### Position Summary

Variant 2 (reviewer-2 card) returns PASS with no blocking and no minor findings. I argue that the PASS verdict is correct and that Variant 2 adds the most complete preservation and evidence-scope checklist of the three cards. It is also the only card with no wrong citation. I concede that its evidence anchoring is the weakest (it cites only the reviewer brief). It also missed the exit-0 safe-skip fixture that Variants 1 and 3 found. Its semantic 21/21 count is reviewer judgment only. The deterministic lexical coverage for this run is 13/21 = 0.6190, and that figure stands. Nothing here claims that any test, install or runtime run took place, and nothing asserts runtime causation.

### Steelman: Variant 1

Variant 1 (sonnet/analyzer) is the most self-critical card. Each of its three minor findings has a plan reference and a concrete verifier (variant-1-original.md:8-22). R1-3 targets the one place where the plan's acceptance wording is weaker than the source. Plan line 35 says "distinguish" Claude (CLI) from New Terminal, while `source.md:1` says "never New Terminal". Variant 1 also records that weakness openly as a limitation (variant-1-original.md:30). R1-2 correctly finds that the exit-0 success/skip path has no defined test fixture. Variant 1 also flags its own wrong source range in the card (`evidence_pathology`, variant-1-original.md:18), which is good evidence hygiene.

### Steelman: Variant 3

Variant 3 (opus/refactorer) has the best-grounded evidence. R3-2 cites the real helper (`install_user_setup.py:230-263`) and names the precise missing fixture: exit 0 with all three files present, and stdout naming a skipped guide. It also says no keyword parser is needed (variant-3-original.md:17-21). That matches plan line 45 ("reuse existing result fields without a new parser") and plan line 51 ("including when files already exist"). R3-1 is the only card to look past the named routing-block test for other readers of core CLAUDE.md. It labels three of its four leads as unverified (variant-3-original.md:9-16).

### Key Strengths Claimed

1. **Preservation coverage (U-003, Medium value).** Variant 2's self-audit is the only card that lists each preserved behaviour Task 2 must keep (variant-2-original.md:12):
   - backward compatibility;
   - executable identification;
   - deadlines;
   - the three-skill list;
   - nonfatal failure;
   - no external force;
   - edited-copy protection.

   These map one-to-one onto plan line 45 ("Preserve the current executable identification, deadline, absent/failed-Orca nonfatal behavior and three-skill list") and plan lines 23 and 50. They also match the code that must survive: `_find_orca()` at line 238, `_orca_timeout(deadline)` at line 249, the nonfatal `True` returns at lines 240, 253-256 and 259-262, and `_ORCA_SKILLS` at lines 236, 242 and 257.
2. **Mocked versus live separation.** Variant 2 is the only card that states Task 2 keeps mocked verification separate from live refresh and UI reproduction (variant-2-original.md:14). Plan line 52 requires exactly this ("Logs distinguish mocked installer checks from actual Orca dry-run evidence; no live guide refresh or UI reproduction is claimed"). Plan line 37 says the same for Task 1.
3. **Boundary preservation.** Variant 2 checks that Task 1 keeps worker and internal-agent boundaries (variant-2-original.md:13), which matches plan lines 22 and 36.
4. **Verifiers cover the full red/green matrix.** Variant 2's top-level verifier (variant-2-original.md:16) lists:
   - pre-fix failures and post-fix passes;
   - the helper and the caller;
   - default skip;
   - arguments;
   - edited contents;
   - output;
   - absent, failing, timeout and incomplete cases.

   This is the full red/green matrix in plan lines 50-52.
5. **No citation pathology.** Variant 2 cites nothing it did not read and claims no tests ran (variant-2-original.md:21-23). Neither excluded pathology belongs to it.
6. **The PASS verdict is correct for this plan.** The plan already contains the safe-skip requirement (lines 24, 45 and 51). It also contains the force gate (line 45, "Existing files may short-circuit only when force is false") and the no-`--force` rule (lines 23 and 50). The other two cards' findings are minor verifier refinements, not blockers. All three cards agree on this.

### Weaknesses in Variant 1

- R1-2's `original_source_ref` (`install_user_setup.py:113-119`) is wrong. The real helper is at lines 230-263. Variant 1 flags this itself, but the citation is still unusable.
- R1-1 has low value. Its own note admits that running sync in Task 2 is intended, not an omission (variant-1-original.md:12). Plan line 47 makes sync part of delivering the README.
- R1-3's verifier asks for an assertion that "shell routes are prohibited for ccsession sessions". That is stronger than plan line 35's literal AC. It is defensible only through Task 1's Inputs (plan line 30, which takes in `source.md`). Variant 1 itself says the merge must adjudicate this (variant-1-original.md:30).
- Variant 1 read the brief only and did not reread the source ranges (variant-1-original.md:24).

### Weaknesses in Variant 3

- R3-1 verified only one file (`tests/core/test_codegraph_guide.py:137-174`). The other three are search leads, as the card admits (variant-3-original.md:16). Plan line 52 already requires wider regression runs, so the finding adds little.
- Variant 3 says nothing on C-003 or X-001, the shell/CLI distinction, which is the core of Task 1.
- Its limitation notes depend on brief-local line numbers. Those are excluded from final citations, and it did not read the actual Orca help (variant-3-original.md:29-30).

### Concessions

- Variant 2's 21/21 is semantic reviewer judgment. The deterministic lexical coverage is 13/21 = 0.6190, and it is not replaced by 21/21 anywhere.
- Variant 2's evidence points only at its brief (`reviewer-briefs/reviewer-2.md:49-82`, `:137`), not at plan or code lines (S-002). Its own limitations say it did not check the full matrix independently (variant-2-original.md:22).
- Variant 2 missed the exit-0 safe-skip fixture (C-001 and X-002). The plan requires surfacing skips "including when files already exist" (line 51). When all three files exist after a forced call, line 257 counts 3/3. With returncode 0, line 263 returns the success message whatever Orca reported. Variants 1 and 3 found this; Variant 2 put it under the general word "output".
- On X-001, Variant 2 treats the AC's "distinguish" as complete coverage. It did not note that `source.md:1` says "never New Terminal".
- Variant 2 has the lowest calibrated confidence (0.66), and its calibrator diversity is degraded.

### Shared Assumption Responses (A-001..A-004)

- **A-001 QUALIFY.** The installed help supports it: "skipped folders are warnings" and "Exits 1 when a location failed or changed" (orca-discovery.md:21, 25). That is help text, not an observed run, so the exit-0 skip is documented behaviour, not verified behaviour.
- **A-002 ACCEPT.** Static reading of `install_user_setup.py:236-237` and `:257-263` shows that when all three SKILL.md files exist, the presence count is always 3/3. Exit 0 then yields the line-263 success message, which proves no refresh. This is a code reading, not a runtime claim.
- **A-003 ACCEPT.** All three cards' limitations disclaim test execution and runtime causation, and plan line 19 marks causation UNDETERMINED.
- **A-004 QUALIFY.** It holds if `force` is added after `deadline` with default `False`, because the caller at line 441 passes only `deadline=` by keyword. I did not check other positional callers of the line 230-232 signature.

### Per-Point Positions

- **S-001:** Variant 1 is best. Each finding carries its own plan reference and verifier; Variant 2's verifiers are a single top-level list.
- **S-002:** Variant 3 is best. It anchors at the correct helper range (230-263); Variant 1's range is wrong, and Variant 2 cites the brief only.
- **C-001:** Variant 3 is best. Its exit-0, three-files-present, no-parser fixture matches plan lines 45 and 51 and code lines 257-263.
- **C-002:** Variant 3 is best. It correctly reads sync in Task 2 as delivering the README (plan line 47), without inventing a timing defect.
- **C-003:** Variant 1 is best. R1-3 gives a testable verifier for the terminal-surface versus shell wording in plan line 35; Variant 2 only asserts coverage.
- **C-004:** Variant 3 is best. It is the only card to raise this, with one verified reader and its leads honestly labelled.
- **C-005:** Variant 2 is best, qualified. It is the only card that audits requirements at all, but its 21/21 is judgment, and the lexical 13/21 = 0.6190 governs.
- **X-001:** Variant 1 is best. It flags that "distinguish" (plan line 35) is weaker than `source.md:1` "never", which reaches Task 1 through its Inputs (plan line 30).
- **X-002:** Variant 3 is best. The requirement exists (plan lines 24, 45 and 51); only the exit-0 fixture is unspecified, and R3-2 names that fixture exactly.
- **A-001:** Variant 3 is best. Its verifier is built directly on the exit-0 skip, consistent with the help text in orca-discovery.md:21-25.
- **A-002:** Variant 3 is best. Its "no refresh-success claim" verifier targets the trivially satisfied presence check at lines 257-263.
