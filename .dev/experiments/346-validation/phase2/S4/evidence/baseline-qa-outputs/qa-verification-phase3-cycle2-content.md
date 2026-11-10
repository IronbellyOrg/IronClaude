# QA Report - Gate 1 Content Verification After Fix Cycle 2 (rf-qa-qualitative, fix-cycle)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Fix cycle:** 2 (last)
**Fix authorization:** false

---

## Scope and method

Inputs read: `qa/qa-consolidated-findings-phase3-cycle2.md` (6 blocking, all IMPORTANT), `qa/qa-fix-log-phase3-cycle2.md`, research files 01 to 05 under `research/` (targeted line ranges around every edited location, plus the full 05 addendum). Every cited source line behind the six fixes was re-read in the live tree (tests, Dockerfile.coder, install.sh, startup.sh, modules.tf, block-bare-python.sh, install_hooks.py, and the bmad-method 6.9.0 installer under /opt/nvm, read-only). Nothing was run. No file other than this report was written.

## Part 1: the six blocking findings of the consolidated cycle-2 file

### Finding 1 (05 line 57 "C, E, F at boot") - RESOLVED
05:57 now reads "(B1, D1, and E, F when run from install.sh at boot)". It matches the 05 addendum C-F1-2 / F1.4 row 3 and the Summary at 05:306. Evidence-based (the correction already lived in the addendum; no new claim). grep of 01-05 for "C, E, F" finds no remaining instance (the 04:109 hit is "none for A, C, E, F", a different statement).

### Finding 2 (matrix built from an In-Progress 04 addendum) - RESOLVED (evidence, not wording)
Rows S17 to S20 added with file:line. I re-read each source:
- S17 test-73 `copy_ok` 102-114 (exact COPY form line 108, `install -d -m 0755` RUN line 109-111) and `tier_ok` 81-98 (last `cleanupPeriodDays` must be 90, lines 94-97): text matches. The fix log's own correction (tier_ok, not copy_ok, owns the cleanupPeriodDays rule) is correct.
- S18 test-52:1374-1377 (`orca_retirement` block, no `count =`, orca literals): matches; modules.tf block is 82-109 (grep).
- S19 test-51-selector-onboarding-wiring.sh:386-396 (awk takes the FIRST `locals {` block; W2d/W2e): matches; modules.tf locals block is 16-34 (grep).
- S20 test-1-catalogue-shape.sh:24-25, 43-67 (exactly `install.sh manifest.yaml module.tf`): matches.
Rows S6 and S12 to S16c agree with the Complete 04 addendum (A.3 table, A.4 table): S12 markers 16,121,160,191,303,389,692,1348,1665 and seed_if_absent 201 / unset 294 re-verified by grep of startup.sh. U-F1-2 is marked RESOLVED in both places (05:265 and F1.5), and F1.4 row 4 (05:388) and open question 2 (05:413) now cite S16c and S17-S20 and are consistent with the matrix columns (I cross-checked each S-row cell named in question 2).

### Finding 3 (03 "are blocked there" vs UNVERIFIED Gaps 13-14) - RESOLVED
03:273 and 03:364 now say "would be blocked ... if Claude emits the bare python3 form and the registration is present (UNVERIFIED, Gaps 13-14)" with the split tag "CODE-VERIFIED for the hook, UNVERIFIED for the effect". Hook facts re-verified: block-bare-python.sh:134 and 343-344, install_hooks.py:85. The claim was weakened to its evidence, and Gaps 13-14 (03:351-352) agree.

### Finding 4 (one rule for a B2 skill in the Dockerfile.coder:547-548 COPY) - RESOLVED
Dockerfile.coder:547-548 is one COPY (continued line) with the three config sources and last token `/usr/local/lib/aidev/`. test-60-llm-gateway-env.sh:84-88 joins continuations, selects COPY lines containing `codex-config.toml` (:85), and checks `len(copy) == 1 and all(s in copy[0].split() ...) and copy[0].split()[-1] == '/usr/local/lib/aidev/'` (:87-88): the quoted assertion is verbatim. An extra source before the destination keeps all three conditions true, so "does not break" is correct. The same rule now appears in 02 A5 (B2 row), 04 A.3 (a), A.9, A.10 (test-60:84-93 row) and 05 S13. grep of the research dir for "own COPY|547-548|test-60" shows no surviving contradictory statement (04:463 keeps the withdrawn advice as an explicitly labelled withdrawal). grep of `.github/` for the config names, profile.skel and shell-zellij finds no other whole-line COPY pin (test-22:137-141 and test-startup-boot:2780-2784 check installed file bytes and mode 0:0:644, not COPY text).

### Finding 5 (05 line 318 and rows S3/S7: option C invisible to test-57) - PARTLY RESOLVED, one residual contradiction (see New-1)
Verified: install.sh:42 runs `bmad install ...`; run_slug (test-57:75-79) uses `PATH="${RUN_PATH}"` (test-57:27); the cold run is test-57:173-178 (expect_rc at 175), the asserts at 323-324, the dirty-seed run 457-459; the second run 331-336 hits the `_bmad` guard (install.sh:24-25). Grep of test-57 for startup.sh|seed_if_absent|modules.tf|aidev-startup|SessionStart|bmad install returns no match (reproduced). Line 318, S3 and S7 are now correct and agree with X2/X3 and with 04 row 193. BUT the evidence paragraph at 05:376 and the C-F1-2 row at 05:408 were not updated (New-1).

### Finding 6 (03 line 286 official-modules.js:770-797 as the existing-install check) - RESOLVED
Reproduced: installer.js:1545-1552 (`findBmadDir` always returns `P/_bmad`), ui.js:217-220 (`hasExistingInstall = await fs.pathExists(bmadDir)`, which gates the action menu at :226), ide/shared/path-utils.js:21 (`BMAD_FOLDER_NAME = '_bmad'`). official-modules.js:770-797 is a different `findBmadDir` (any child dir with `_config/manifest.yaml`) whose only caller in the package is `loadExistingConfig` at :842 (grep of tools/installer). 03:286 now agrees with 01:463. No other research file still cites the old rule (grep for "official-modules.js:77x" and "any direct child").

---

## Part 2: the four requested checks

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Blocking depth findings resolved with evidence, not wording changes | PASS for findings 2, 4, 6; wording-only for 1 and 3 (acceptable: the correct text already lived in the file, or the claim had to be weakened because running Claude/the hook is forbidden); finding 5 only partly (New-1) | F2: four new test pins re-read at file:line. F4: test-60:85-88 quoted verbatim and re-read. F6: installer.js, ui.js, path-utils.js, official-modules.js re-read. F3: claim weakened to match Gaps 13-14, hook facts re-read. |
| b | Fixes did not make claims stronger than their evidence | PASS with notes | The two new "does not break" / "breaks only if" statements (02 A5, 04 A.3 (a), 05 S13) are scoped to the single test-60 assertion, which I re-read; the layer-cost gap U20 in 02 A7 (other tests not searched exhaustively) is still open and still labelled UNVERIFIED (Minor m4). No new CODE-VERIFIED tag covers a run or an observation that was not made. |
| c | Files coherent and contradiction-free after the edits | FAIL (New-1) | 05:376 and 05:408 still carry the pre-fix reasoning for option C (see below). All other cross-file checks I ran (02 A5 vs 04 A.3/A.9/A.10 vs 05 S13; 03:286 vs 01:463; 03:273/364 vs 03 Gaps 13-14; 05:57 vs 05:306 vs C-F1-2; 05 matrix S-rows vs 04 A.10 and 04 section 7 row 193) agree. |
| d | Every addendum edit made by a fix is evidence-based and tagged | PASS | New rows S17-S20 carry "[re-read]" with file:line; 05 line 318 sits under F1.1 [CODE-VERIFIED] and its claims reproduce; 02 A5 cell [CODE-VERIFIED]; 03:273/286/364 carry tags; 04 A.3 and A.9 headings are [CODE-VERIFIED]. No new addendum section was created by cycle 2. |

---

## Part 3: issues found

### New-1 (IMPORTANT) - residual contradiction about option C and test-57 after the finding-5 fix
Location: `research/05-startup-boot-test-docs-and-decision-trail.md` line 376 (and line 408).
- Line 375-376 is headed "Evidence for the 'none' rows" and lists "X1, X2". It says `run_slug` "is the only code in test-57 that executes bmad code, and it runs `install.sh`, not a skill, hook or wrapper subcommand; Grep of test-57 for ... `bmad install` finds nothing [CODE-VERIFIED]". But after the fix, the X2 row (line 369) says option C is BREAKS-IF because `install.sh:42` runs `bmad install` through the baked wrapper in every seeded run, and line 318 explains that the grep finds no literal `bmad install` only because the call sits inside install.sh. Line 376 therefore still offers the same "grep finds nothing, wrapper not exercised" reasoning that finding 5 removed from line 318, and lists X2 as a "none" row when its C cell is not none.
- Line 408 (C-F1-2) still says option C "has no certain break (S1 none, S10 BREAKS-IF only)". After the fix, C has BREAKS-IF in S3 and S7 (through the wrapper) as well as S10, S11, S13-S15, X2, X3.
Required fix: in line 376 split the bullet ("X1, and X2 for every column except C: ... for C see line 318 and the X2 row; the grep finds no literal `bmad install` because install.sh:42 makes the call"); in line 408 replace "S10 BREAKS-IF only" with "BREAKS-IF in S3, S7, S10, S11, S13 to S15, X2 and X3". Evidence to cite is already in the file (install.sh:42; test-57:27, 75-79, 173-178).

### Minor notes (not blocking, not rechecked in later cycles)
- m1: 05:331 caption says rows "S17 to S19" were added (twice) and that four test files were re-read; S20 (test-1-catalogue-shape) also exists, and "S6 to S15" skips S16a to S16c. 05:265, 05:358, 05:388 and 05:397 correctly say S17-S20.
- m2: 05:318 says "every seeded run executes the baked wrapper" and lists three runs; the prior-output run (test-57:462-465) is a fourth and is omitted.
- m3: 05 F1.6 (line 417) still says "six UNVERIFIED items" although U-F1-2 is RESOLVED, and names only the live-boot pin for B3/D3 (not S18/S19), nothing for D2 (S17) or B1/D1 (S20).
- m4: 02 A7 item 6 (U20) still says other tests were "not searched exhaustively" for pins on the :547 COPY, while the fix log reports a search of all contract tests; the research file itself does not record that search. My own grep of `.github/` found no whole-line pin, so the A5 rule is right, but the gap ledger is stale.
- m5: 01:360 ("U8 is closed by the finding 4 addendum") and 03:201 ("closes 01 U8") omit the qualifier in 03:273 ("CLOSED for the file-and-code part"; fresh-workspace registration stays UNVERIFIED, Gap 13).
- m6: 05:48 (test-57:449-452 row) still lists "C if boot-time" among options that break the no-seed oracle; S1 for C is "none". The qualifier "if boot-time" keeps it from being false.
- m7: 04:334 (A.3 (a)) still says the config COPY is "the line at 547 region ... or an earlier one; exact line not needed"; A.9 corrects it to Dockerfile.coder:547-548.
- Pre-existing minor notes M1 to M3 of the consolidated file (05 Summary counts, 04:238 A.1-A.8, 01:491 In Progress) were not rechecked, as instructed.

---

## Self-Audit

What I actively checked (all by tool, none by reliance on another report):
- Read in full or in targeted ranges: the fix log, the consolidated findings, 05 (lines 20-70, 205-219, 236-418, i.e. all of the addendum), 02 (236-243, 284-298, 336-454), 03 (100-105, 199-202, 238-365), 04 (106-110, 176-212, 268-350, 440-541), 01 (296-299, 350-389, 455-530).
- Re-read the sources behind every edit: test-57 (18-92, 125-195, 316-343, 410-470), catalogue/bmad/install.sh (1-61), test-60-llm-gateway-env.sh (60-105), test-73 (1-145), test-52 (1366-1386), test-51-selector-onboarding-wiring.sh (376-397), test-19 (196-224, 1170-1191), test-22 (105-160), test-startup-boot (2770-2795), test-68 (196-226), Dockerfile.coder (134-145, 472-476, 540-552), startup.sh (196-275), installer.js 1545-1552, ui.js 210-280, official-modules.js 764-845.
- Greps run (about 22): test-57 for the six boot/wrapper terms (no match, reproduced); research dir for "own COPY|547-548|test-60|COPY line", "invisible", "wrapper", "blocked|block-bare-python", "official-modules.js:77x|any direct child", "C, E, F|options B, D", "S10 to S1x|S17 to S2x"; `.github/` for the config names/COPY text; modules.tf, test-1-catalogue-shape.sh, startup.sh section markers, test-49 lists, block-bare-python.sh:134/343-344, install_hooks.py:85, installer `findBmadDir`/`loadExistingConfig` call sites.
- Claims independently reproduced: about 45 (each fix's cited file:line, each new matrix row's assertion text, the test-60 assertion quote, the test-57 run chain for option C, the five source-line citations of finding 6, the hook line numbers, the section marker lines).
- Not observed (UNVERIFIED, scope guard): no test, hook, `bmad` command or Claude session was run; Gaps 13-14 in 03 remain UNVERIFIED by design; the test-68 repin verifier question (04 open question 4) is untouched by cycle 2 and I did not resolve it.

Why I believe the count is right: five of six fixes reproduce cleanly against the live tree, so the finding count is not zero by omission. The one IMPORTANT issue was found by searching for surviving statements of the pre-fix claim (grep "wrapper" and "invisible" across 05, then reading every hit, including the omitted long lines 26, 211, 318), which is where a fix of this kind usually leaves residue. I looked for the same residue for the other five fixes (grep of all five files for the old wording of each) and found none beyond the Minor notes. I did not find issues in the S17-S20 rows or the 02/04/05 B2 rule despite trying to break them (checked for other COPY pins, other `locals {` pins, hidden-path and mode pins, section 6 execution under `set -e`).

Confidence (Confidence Gate Protocol): Verified: 10/10 (6 findings + 4 checks) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Tool engagement: Read: 38 | Grep: 24 | Glob: 3 | Bash: 2 (read-only sed/grep of installer source under /opt/nvm). Read + Grep + Glob (65) exceeds the 10 checklist items.

---

## Verdict

**Overall Verdict: FAIL**

Counts: findings resolved 5 of 6 (1, 2, 3, 4, 6); finding 5 partly resolved. New blocking issues: 1 (New-1, IMPORTANT, 05:376 and 05:408). CRITICAL 0, IMPORTANT 1, MINOR 7 (m1-m7, notes only). Checks passed 3 of 4 (a, b, d); failed 1 (c).

Unresolved blocking issue to carry: New-1, `research/05-startup-boot-test-docs-and-decision-trail.md` lines 376 and 408 (option C is exercised by test-57 through install.sh:42; the "none rows" evidence and the C-F1-2 "S10 BREAKS-IF only" wording still say otherwise).

## QA Complete
