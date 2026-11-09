# QA Report - Gate 1 Fix Cycle 2 Verification (structural, agent 1 of 2)

**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Phase:** fix-cycle (cycle 2, the last), fix_authorization: false
**Status:** Complete
**Date:** 2026-11-08

---

Inputs read: fix log `qa-fix-log-phase3-cycle2.md` (43 lines), consolidated findings `qa-consolidated-findings-phase3-cycle2.md` (BLOCKING_COUNT 6, all IMPORTANT), research files 02 (A5 and section 6.1), 03, 04 (A.2, A.3, A.9, A.10), 05 (whole). Test lines cited by the fixes were re-read from source.

## Check (a) per blocking finding

### Finding 1 (05 line 57) - FIXED, verified
Grep of research/ for "C, E, F at boot": no remaining hit outside the quotation of the old wording at 05:408 (C-F1-2, which quotes it as the contradicted claim). 05:57 now reads "B1, D1, and E, F when run from install.sh at boot". Agrees with C-F1-2 and with the Summary at 05:306.

### Finding 2 (05 F1.2 rows S17-S20, F1.4, F1.5) - FIXED, verified
Re-read from source: test-73-claude-retention.sh:81-98 (`tier_ok`, call at 135), 102-114 (`copy_ok`, call at 119, exact-form check at 108, RUN check at 109-111); test-52-browser-usability-evidence.sh:1374-1377 (orca_retirement pins); test-51-selector-onboarding-wiring.sh:386-396 (first `locals` awk, `_selected`, `_profiles[...]`; the file name is test-51-selector-onboarding-wiring.sh); test-1-catalogue-shape.sh:24-25 (EXPECTED_FILES), 43-67 (slug_shape_ok); modules.tf:16-34 (first locals block) and 82-109 (orca_retirement). Every file:line in S17-S20 matches the source and the condition wording is accurate. The "In Progress" caveat is gone: U-F1-2 is marked RESOLVED (05:265, 397); the F1.2 caption (05:331) says the 04 addendum is Complete; 04:272 reads `Status: Complete`. F1.4 row 4 (05:388) and F1.5 question 2 (05:413) name S17-S20. Rows S17-S20 agree with 04 A.10 rows (04:487-488, 491, 493).

### Finding 4 (B2 COPY rule across 02, 04, 05) - FIXED, verified
test-60-llm-gateway-env.sh:84-88 read: `copy` (85) = COPY lines containing codex-config.toml; `srcs` (86) = the three configs; the assertion at 87 is exactly as quoted in 02 A5, 04 A.3(a) and 05 S13. Dockerfile.coder:547-548 read: one COPY of six sources ending `/usr/local/lib/aidev/`. Grep of all contract-tests for `profile.skel|shell-zellij|pi-models|opencode.json|/usr/local/lib/aidev/`: no other test pins the COPY line text (test-22:137 and test-startup-boot:2780 check in-image files, not the COPY). The rule is identical in 02:423, 04:334 (A.3 a), 04:463 (A.9, own-COPY advice withdrawn), 04:475 (A.10), 05:347 (S13).

### Finding 5 (05 line 318, rows S3, S7) - FIXED, verified
install.sh:42 read (`NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" ...`), 24-25 (`_bmad` guard), 48-53 (git-status check). test-57.sh:27 (`RUN_PATH="${PATH}"`), 75-79 (`run_slug` runs install.sh with PATH=RUN_PATH), 173-178 (cold run, `expect_rc` at 175), 179-183 (budget), 323-324, 331-336, 457-459 all match the new text of 05:318, S3 (05:337), S7 (05:341) and X2 (05:369). No remaining claim that C is invisible to test-57 (Grep "invisible" over 02-05: only 05:318 states the correction). I also reproduced the 05:318 Grep: `startup.sh|seed_if_absent|modules.tf|aidev-startup|SessionStart|bmad install` over test-57 returns no match.

### Finding 3 (03 addendum A1 "U8 verdict" and addendum Summary) - FIXED, verified
03:273 now reads "would be blocked there if Claude emits the bare `python3` form and the registration is present (UNVERIFIED, Gaps 13-14; corrected in fix cycle 2, finding 3)" and ends with the split tag "CODE-VERIFIED for the hook ... UNVERIFIED for the effect". 03:364 (addendum Summary) carries the same conditional wording. Gaps 13 and 14 exist at 03:351-352 and say exactly what the sentence cites. 03:265 was already conditional. Grep of 02-05 for "are blocked": no unconditional remnant. block-bare-python.sh and install_hooks.py were not re-read (the fix only changed modality; the hook facts were CODE-VERIFIED in cycle 1 and are not in question here).

### Finding 6 (03 addendum row at line 286) - FIXED, verified
Source re-read: installer.js:1549-1552 (`findBmadDir` returns `path.join(projectDir, BMAD_FOLDER_NAME)`, comment "Always uses the standard _bmad folder name"); path-utils.js:21 (`BMAD_FOLDER_NAME = '_bmad'`); ui.js:217-220 (`installer.findBmadDir(...)` then `hasExistingInstall = await fs.pathExists(bmadDir)`); official-modules.js:770-797 (older `findBmadDir`, scans child dirs for `_config/manifest.yaml`, default `bmad`), 833-842 (`loadExistingConfig`, call to `this.findBmadDir` at 842). Grep of `findBmadDir(` over tools/installer: the official-modules.js version is called only at official-modules.js:842; every other call (ui.js, installer.js, commands) uses the installer.js version. The corrected row now matches 01:463 and 02:117, 02:320.

## Check (b) new blocking issues introduced by the fixes

- New false claims: every file:line added by the fixes (S17-S20, S3/S7 for C, line 318, test-60:87-88 quote, installer/ui lines) was compared with source above; none false. Matrix rows S17-S20 each have 9 cells (B1..F) in order.
- Broken structure: none in the edited regions; tables parse (cell counts checked for S13, S17-S20).
- Untagged doc claims: the new sentences carry [CODE-VERIFIED] / UNVERIFIED tags (03:273, 03:286, 05:318, S17-S20 "[re-read]").
- Hallucinated paths: test-73-claude-retention.sh, test-52-browser-usability-evidence.sh, test-51-selector-onboarding-wiring.sh, test-1-catalogue-shape.sh, test-60-llm-gateway-env.sh, test-57-catalogue-configure.sh, modules.tf, Dockerfile.coder, bmad/install.sh all exist (read). Research text writes "test-51" and "test-60" as short names; line numbers match the real files.
- Residual inconsistencies found (all non-blocking, see Issues): 05:331 caption, stale merge instructions at 05:390 and 05:417, B2 definition versus fold form in 04.

## Check (c) required structure per file (Grep of Status, Gaps and Questions, Summary, Key Takeaways)
- 01: Status Complete (4), Key Takeaways (49 to 335), Gaps and Questions (340), Summary (384). Not edited in cycle 2.
- 02: Status Complete (4), Key Takeaways (62 to 323), Gaps and Questions (329), Summary (380); addendum Complete (385).
- 03: Status Complete (4), Key Takeaways (31 to 182), Gaps and Questions (197), Summary (236); addendum Complete (241).
- 04: Status Complete (4), Key Takeaways (54 to 176), Gaps and Questions (236), Summary (267); addendum Complete (272), addendum Gaps (519).
- 05: Status Complete (4), Key Takeaways (32, 56, 138 to 232), Gaps and Questions (236), Summary (304); addendum Complete (309).

## Issues Found

Blocking issues (unfixed or new): none.

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR (note, not rechecked) | 05:331 (F1.2 caption) | Says rows "S17 to S19 were added" and that the lines behind "S17 to S19" were re-read in test-73, test-52, test-51 and test-1-catalogue-shape. Four tests map to S17-S20 (test-1-catalogue-shape is S20). The fix log says S17-S20. The rows themselves are correct and sourced. | Change both "S17 to S19" to "S17 to S20" at 05:331 |
| 2 | MINOR | 05:390 and 05:417 (F1.5 heading, F1.6 last sentence) | Still tell "the fix agent" to merge F1.5 into `## Gaps and Questions` and to correct "C" in the Summary; both were already done (05:260-272, 05:306). | Reword as done, or delete |
| 3 | MINOR | 04 A.10 legend (04:468) vs A.9 (04:463) | The legend defines B2 as "skill from /etc/skel"; A.9 says an own COPY is needed for an /etc/skel destination and the fold into :547-548 delivers from /usr/local/lib/aidev/. The test-60 verdict is identical in 02, 04, 05, so the rule is reconciled. The B2 delivery-proof rows in A.11 assume the /etc/skel form. | Name the two B2 forms (skel destination, own COPY; lib/aidev fold, no new layer) in the A.10 legend |

## Summary
- Blocking findings from the consolidated report: 6; fixed and verified: 6; unfixed: 0.
- New blocking issues introduced: 0.
- Severity counts for this report: CRITICAL 0, IMPORTANT 0, MINOR 3.
- Structure check: all five research files keep Status Complete, Summary, Gaps and Questions and Key Takeaways.
- Cycle trend: 9 blocking (cycle 1) to 6 (cycle 2 input) to 0 now.

## Confidence and tool engagement
- Checklist items: 17 (6 blocking findings, 6 new-issue checks, 5 structure checks of files 01 to 05 counted as one item each). Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement (approximate count of my calls): Read: 33 | Grep: 16 | Glob: 3 | Bash: 0. Read + Grep + Glob (52) exceeds the 17 items.
- Not observed (UNVERIFIED, outside the cycle-2 scope): runtime behaviour of the hook and of any test (no test or `bmad` command was run); block-bare-python.sh and install_hooks.py were not re-read this cycle.

## Self-Audit
What I actively checked: (1) I read the fix log and the consolidated findings in full, then went finding by finding. (2) For each evidence claim added by a fix I re-read the cited source rather than trusting the fix log: test-73:60-144, test-52:1366-1385, test-51:376-403, test-1-catalogue-shape:18-72, modules.tf:10-114, test-60:70-101, Dockerfile.coder:538-551, bmad/install.sh:1-61, test-57:20-91, 165-194, 316-343, 440-467, and in the BMAD package installer.js:1543-1556, ui.js:212-223, path-utils.js (grep), official-modules.js:764-853. (3) I ran searches to find remnants of the old wording: "C, E, F at boot", "invisible", "are blocked", "In Progress", "S10 to S16", `official-modules.js:770`, `findBmadDir` across the installer and across research 01-05, a grep of all contract tests for the Dockerfile COPY-line pins, and a reproduction of the test-57 grep from 05:318 (zero matches, as claimed). (4) I read 05 lines 1-60 and 236-418, 04 lines 180-210, 268-347, 455-542, 02 lines 270-286 and 414-455, 03 lines 236-366, 01 lines 146-148 and 462-469, and checked the S13 and S17-S20 rows cell by cell (9 variants each). (5) I Grepped Status, Gaps and Questions, Summary and Key Takeaways in all five files.
Why 0 blocking is credible: each of the six fixes has a concrete source line that I read and that matches the new text; the searches for old wording returned only the quotations of the old text inside correction notes; and I did find three real residual inconsistencies (MINOR), so the pass was not a rubber stamp. I did not find a way to make the B2 fold rule, the C-through-wrapper rule or the existing-install rule contradict each other across files 01 to 05.
Limits: I did not re-verify cycle-1 content outside the changed locations, and MINOR items from earlier reports were not rechecked (by instruction).

## Verdict: PASS

## QA Complete
