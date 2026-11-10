# QA Fix Log - Gate 1, fix cycle 2 (phase 3)

**Status:** Complete
**Date:** 2026-11-08

Input: `qa/qa-consolidated-findings-phase3-cycle2.md` (BLOCKING_COUNT 6). No gap researcher was spawned: all six are consistency corrections, fixed by re-reading the cited sources and editing with targeted Edits. No MINOR finding was touched. No `bmad` command was run. Research dir: `research/` (files 02, 03, 04, 05).

---

## Finding 1 - FIXED
File: `research/05-startup-boot-test-docs-and-decision-trail.md`, Key Takeaways (line 57).
Change: "(C, E, F at boot)" replaced with "(B1, D1, and E, F when run from install.sh at boot)".
Evidence: the file's own addendum C-F1-2 and F1.4 row 3; the Summary at line 306 already carried the corrected wording.

## Finding 2 - FIXED
File: `research/05-...md` addendum F1.2 to F1.5.
Change: added rows S17 (test-73-claude-retention copy_ok 102-114 and tier_ok 81-98, D2), S18 (test-52:1374-1377, B3 and D3), S19 (test-51:386-396, B3 and D3), S20 (test-1-catalogue-shape:24-25, 43-67, B1 and D1). Rewrote the caption that said the 04 addendum was In Progress; updated "S10 to S16c" to "S10 to S20" in two places; F1.4 row 4 ("Cheapest non-breaking delivery") and F1.5 open question 2; marked U-F1-2 RESOLVED in the merged table and in F1.5.
Evidence: re-read test-73:64-139, test-52:1370-1381, test-51:380-399, test-1-catalogue-shape:20-70, modules.tf lines 16/34/82/109 (grep); compared S6 and S12-S16c with the Complete 04 addendum (04:272, A.2 to A.4). One correction to the finding text: the `cleanupPeriodDays` rule is `tier_ok` (test-73:81-98), not `copy_ok`; both are in S17.

## Finding 3 - FIXED
File: `research/03-startup-flow-home-and-user-level-claude.md`, addendum A1 "U8 verdict" (line 273) and the addendum Summary (line 364).
Change: "are blocked there" replaced with "would be blocked there if Claude emits the bare python3 form and the registration is present (UNVERIFIED, Gaps 13-14)"; tag changed to CODE-VERIFIED for the hook, UNVERIFIED for the effect.
Evidence: the same addendum's Gaps 13 and 14 (lines 351-352) and line 265.

## Finding 4 - FIXED (one rule across 02, 04, 05)
Rule: adding a B2 skill source to the `Dockerfile.coder:547-548` COPY does NOT break test-60. Assertion text (test-60:87-88): `check(len(copy) == 1 and all(s in copy[0].split() for s in srcs) and copy[0].split()[-1] == '/usr/local/lib/aidev/', ...)`; `copy` at :85, `srcs` at :86. It breaks only if a config source is removed, a second COPY with `codex-config.toml` is added, or the destination changes. An own COPY is needed only for a different destination (+1 layer).
Files: 02 A5 B2 row (rule and quote added); 04 A.3 (a) ("BREAKS-IF B2 edits that COPY line" corrected), A.9 ("keep the skill on its own COPY line" withdrawn), A.10 row for test-60:84-93; 05 matrix row S13 (B2 cell).
Evidence: read test-60:76-97 and Dockerfile.coder:540-552; grep of all contract tests for `profile.skel|shell-zellij|pi-models|opencode.json|/usr/local/lib/aidev/` found no other whole-line pin of that COPY.

## Finding 5 - FIXED
File: `research/05-...md` addendum line 318 and rows S3 and S7 (S3 changed for consistency with X2).
Change: C removed from the list invisible to test-57; added that `install.sh:42` runs `bmad install` through the wrapper with the image PATH (test-57:27, 75-79) in the cold run (173-178, 175), the manifest and clean-seed checks (323-324) and the dirty-seed run (457-459); the second run (331-336) hits the `_bmad` guard (install.sh:24-25) and skips it. S7 for C is now BREAKS-IF (same condition as X2). S3 for C is now BREAKS-IF over budget through the wrapper.
Evidence: install.sh:1-61 and test-57:20-90, 168-190, 318-342 (read), grep of test-57 for run_slug and bmad.

## Finding 6 - FIXED
File: `research/03-...md` addendum table row (line 286).
Change: citation replaced with `installer.js:1549-1552` (`findBmadDir` always returns `P/_bmad`, `BMAD_FOLDER_NAME = '_bmad'` at ide/shared/path-utils.js:21) and `ui.js:217-220` (`hasExistingInstall = fs.pathExists(bmadDir)`); stated that `official-modules.js:770-797` is a different, older `findBmadDir` used only by `loadExistingConfig` (official-modules.js:833, call at :842). Now agrees with `01:463`.
Evidence: read core/installer.js:1545-1552, official-modules.js:764-850, ui.js:214-220, path-utils.js grep.

---

## Totals
Fixes applied: 6. Findings not fixed: 0. 6 + 0 = BLOCKING_COUNT 6. UNVERIFIED items added: 0 (the existing UNVERIFIED tags for Gaps 13-14 now govern the finding 3 sentence). MINOR findings acted on: 0.
