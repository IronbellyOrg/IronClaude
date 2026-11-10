# QA Report - Phase 3 Fix Cycle 1 Content Verification (rf-qa-qualitative)

**Status:** Complete
**Date:** 2026-11-08

---

## Scope read so far
Consolidated findings (18 rows, BLOCKING_COUNT 9), fix log (9 fixes), research files 05 (all), 04 (sections 7, Gaps, Summary, addendum A.1-A.7), 02 (section 6, Gaps, Finding 3 addendum), 03 (Gaps, addendum A1-A5).

## Check results (appended incrementally)

### Finding 1 (04/05 contradiction): addendum in 05 lines 308-413
- Reproduced by Read: test-57:75-79, 140, 148-153, 450; test-startup-boot:617-637, 2208-2211, 2631-2637, 2774-2779; startup.sh section markers (9 markers at 16,121,160,191,303,389,692,1348,1665). All match the matrix citations. Evidence-based, not wording only (9-column, 2-group matrix with file:line cells).
- ISSUE F1-a (IMPORTANT): 05 line 57 (Key Takeaways, a-supplement) still says "any boot-time change in install.sh (C, E, F at boot) needs a replacement assertion". The addendum's own C-F1-2 says C edits Dockerfile.coder:142, not install.sh, and the sentence must name B1, D1, E, F. The fix log claims the blanket wording was corrected "in four places and the Summary"; line 57 is a fifth place that was missed, so file 05 still contradicts its own addendum (check c).
- ISSUE F1-b (IMPORTANT): the 05 matrix was built from the 04 addendum while it was In Progress (U-F1-2: it ended at A.4, 04:366). The finished 04 addendum adds pins the 05 matrix lacks: test-73 copy_ok exact-line rule for D2 (04:391-392; test-73:102-114 re-read and confirmed), test-52:1374-1377 and test-51 W2d/W2e modules.tf pins for B3/D3 (04:374-375; test-52:1374-1377 re-read and confirmed), test-1-catalogue-shape for B1/D1 extra file (04:404). 05 F1.5 open question 2 says "D2 adds S14", "B3 and D3 add S16c", and F1.4 row 4 calls B3/D3 the "cheapest non-breaking delivery"; neither mentions the 04 BREAKS-IF conditions. Finding 1 asked for ONE reconciled matrix; the two matrices were not merged and the 05 one is a strict subset.
- ISSUE F1-c (MINOR note): S1 E/F cells say "BREAKS (at boot)" and the "Certain breaks" line names E and F, while the same addendum tags E/F write locations UNVERIFIED (U-F1-1). "Certain" exceeds the evidence; should be BREAKS-IF.
- ISSUE F1-d (MINOR note): 04 Summary (04:269) and section 7 still say B, D, E, F "break it for certain"; only the pointer at 04:238 qualifies it.

### Finding 3 (Sysbox layer gate): addendum in 02 lines 384-452
- Reproduced: workflow:1016-1029 (fail when layers > 70); `gh run view 42346410588` shows headSha f1ac0c93 (= worktree HEAD), conclusion success, log line "Sysbox image layers: 68 (budget: 70)"; Dockerfile.coder:229 "two spare" and :468 "no headroom" present; Grep of instructions `^\s*(FROM|RUN|COPY|ADD)\b` = 61 (matches A3); COPY list (29 COPY lines, lines 185..593) matches A3 exactly; merged-decision.md:25-26 and :37 match; ARCHITECTURE-SPINE.md:93 and development-guide.md:66 match.
- Resolved with measured evidence, and the deviation from the proposed fix (constrained, not blocked) is supported by 68 of 70. PASS. No new issue found in this addendum.
- Note: 02 main-body 6.4 table has no layer column; the only pointer is in Gaps (02:350). Acceptable because the finding permitted the addendum.

### Finding 4 (trigger predicate, walkthrough, 01 U8): addendum in 03 lines 240-364
- Reproduced: 41 `python3 ` matches in 31 SKILL.md files; 25 files contain "If the script fails" and the 6 without it are exactly advanced-elicitation, customize, create-architecture, edit-prd, create-prd, validate-prd (derived by me from the two file lists). Per-file breakdown (38+2+1) consistent with per-file counts.
- ISSUE F4-a (IMPORTANT, claim stronger than evidence): A1 "U8 verdict" and the addendum Summary state that the 41 `python3` steps "are blocked there" and tag the statement [CODE-VERIFIED]; the same addendum lists "Claude emits the bare python3 form" and "fresh Default workspace has the registration" as UNVERIFIED (items 13, 14) and the body says "[Inference ... UNVERIFIED at runtime]". The tag and the Summary overclaim; the correct form is "would be blocked IF Claude emits the bare form AND the registration is present".
- Also reproduced for Finding 4: install_hooks.py:85 lists block-bare-python.sh; block-bare-python.sh:134 and :338-344 (exit 2 on python/python3/pip/pip3); ironclaude/install.sh:15-16, 25, 133-136, 139, 141; spec2-health.sh:74-81, 85-114. All match. PASS on the predicate FIRST_USE(P) definition, the per-option walkthrough, and the U7/U9 "stay open until web-01" statement.
- ISSUE F4-b (MINOR note): 03 A2 says a partial `_bmad/` makes the predicate false and "the recovery path is the manual command in manifest.yaml:14"; 01 F5-D says that manual `bmad install --yes` on a partial tree goes to quick-update (ui.js:252-262, re-read and confirmed) with an unread outcome (F5-8). The recovery claim is untagged and stronger than its evidence.

### Finding 5 (memlog, CI, version skew): addendum in 01 lines 390-529
- Reproduced: `gh run view` logs for runs 42384399575, 42369600288, 42346410588 give "cold bmad: 374 ms / 392 ms / 392 ms" and FR-21 totals 4766/4905/4873 ms; memlog lines 20, 21, 81 quote exactly; `_bmad/_config/manifest.yaml` version 6.10.0; ui.js:233-262 (quick-update default under --yes) and ui.js:807-861 match; test-57:64-66, 75-79 match.
- The "about 4 s" is correctly separated from the baked-CLI CI figure and every PRO figure is tagged "prior-review observation, not re-run"; risk rows for B, C, D exist (F5-F). Resolved with evidence. PASS. No new issue.

### Finding 6 (39 files, 52 matches): 01 section 7.4 row at line 282
- Reproduced by Grep count: 52 occurrences across 39 files. 46 SKILL.md and 37-file counts were not re-run by me (taken from the fix log and the evidence agent). PASS for the corrected row.

### Finding 7 (partial-seed branch): 01 section 3.2a lines 124-143, U13 added
- Reproduced by Read: ui.js:807-861 (branch at 807, guard at 832-837, bare-yes defaults at 838-861, defaults only when existing core config is empty), commands/install.js:14-37 (no --project-name flag), core-skills/module.yaml:8-33 (user_name and communication_language have scope user), manifest-generator.js:468-545 (core partition into team/user), catalogue/bmad/install.sh:42 flag set. The table, consequence and plan facts are correct. PASS. Minor wording gap: line 142 says bare `--yes` seeds all five keys without the "only when existing core config is empty" condition that ui.js:843 imposes (F5-A states it correctly). Not rechecked as MINOR.

### Finding 8 (C5 withdrawn): 05 lines 99, 184, 247, 285, 301
- Reproduced: official-modules.js:1409 `return configValue || match`; ui.js:807-837. Re-tag "mechanism CODE-VERIFIED, outcome UNVERIFIED" is applied consistently in every place the fix log lists (rows b2 slug-configuration, d5, Gaps U6, withdrawal note, Stale Documentation bullet, Key Takeaways). PASS.

### Finding 9 (REPORT.md and .dev/issues/478): research-notes.md lines 141-232
- Reproduced: Glob lists exactly 12 files under .dev/issues/478/; REPORT.md lines 26, 89, 91, 100, 120 match the quoted positions; BUILD-REQUEST.md:14 holds the decision text; startup.sh:1117 and :1184 match R15 and the deselect rule. 16 positions (R1-R16) each marked superseded/in force with reasons; the prior "user-scope install UNVERIFIED" is answered by 01 (43 hits in one file, re-confirmed in the fix log). PASS. No new issue.

### Finding 2 (pinned-test inventory): 04 addendum lines 271-541
- Reproduced: Grep count 141 occurrences across 30 files with the same per-file counts; `seed_if_absent|/etc/skel` = 68 across 16 files with the same per-file counts; `seed_if_absent` literal only at test-60:92; startup.sh section markers; test-3 scan roots (test-3:159, 165-198); test-67 rules (46-69, 107-115); test-73 json_ok/tier_ok/copy_ok (69-114); test-52:1374-1377; modules.tf 16-34 and 82-109; test-startup-boot ranges 617-637, 2208-2211, 2631-2637, 2774-2779. A.8 classification table has 15 relevant and 15 irrelevant rows as the fix log says. Resolved with evidence and proposed assertion text (A.11).
- ISSUE X-1 (IMPORTANT, contradiction between addenda, B2 and the test-60 pin): 04 A.3(a), A.10 (row "Section 6 seeds the three LiteLLM configs ... c if the config COPY is edited") and 05 matrix row S13 say B2 BREAKS-IF the `codex-config.toml` COPY line (Dockerfile.coder:547-548) is edited to add the skill source. test-60:84-88 (re-read) only requires exactly one such COPY line, all three config sources present, and last token `/usr/local/lib/aidev/`; appending a source keeps it passing, which 04 A.9 itself concedes ("would change its last token only if the destination changed") while advising "keep the skill on its own COPY line". 02 addendum A5 and A6 name that same COPY (:547-548) as the zero-layer fold for B2 and rely on it to stay inside the 2-layer headroom (68 of 70). Result: three files give B2 two incompatible instructions (fold = 0 layers, no test break per test-60:87; own COPY = +1 layer; "BREAKS-IF edited"), and none reconciles them. A synthesis author following 04/05 pays a layer; following 02 hits a "BREAKS-IF" that the test text does not support.
- ISSUE X-2 (MINOR note): A.8 row 8 classes test-68 IRRELEVANT while the same row says it is UNVERIFIED that a new RUN line in the real Dockerfile cannot trip `repin.sh --verify`; B2/C/D2 edit that Dockerfile. Tagged, but "irrelevant" is stronger than the evidence.

## Cross-file coherence (criterion c) - additional points
- 05 Summary (line 306) still says 17 UNVERIFIED and 6 CODE-CONTRADICTED, while 05 now also carries 6 U-F1 and 3 C-F1 rows (and an addendum), i.e. 23 and 9. (MINOR note)
- 01 section 7.5 (line 298) and the U8 row (line 353) still carry the superseded wording; only the Gaps pointer (line 360) and the 03 addendum A5 mark them superseded. (MINOR note)
- 02 Gaps header says 14 UNVERIFIED; the 6 added in the 02 addendum are reachable only through the pointer at 02:350. Acceptable.

## Criteria (a)-(d)
- (a) Blocking findings resolved with evidence rather than wording: all 9 were addressed with new evidence, not wording only. Findings 3, 5, 6, 7, 8, 9 pass cleanly; finding 2 passes on evidence but its addendum introduces X-1; findings 1 and 4 carry defects F1-a, F1-b and F4-a.
- (b) Claims stronger than evidence: F4-a (IMPORTANT), F1-c (MINOR).
- (c) Coherence: F1-a, F1-b, X-1 (IMPORTANT); MINOR notes above.
- (d) Every addendum is evidence-based and tagged ([CODE-VERIFIED]/[UNVERIFIED]/[CODE-CONTRADICTED] or "prior-review observation, not re-run"); one mis-tag (F4-a).

## Self-Audit
- Claims independently reproduced: about 60 (citations in the sections above: counts 141/30, 68/16, 41/31, 25, 52/39, 61 instructions, 29 COPY lines; CI log lines for 4 runs; test-57, test-startup-boot, test-52, test-73, test-60, test-3, test-67, modules.tf, workflow gate, Dockerfile comments, ui.js, install.js, module.yaml, manifest-generator.js, official-modules.js:1409, install.sh, ironclaude/install.sh, spec2-health.sh, block-bare-python.sh, install_hooks.py:85, memlog lines 20/21/81, REPORT.md lines, BUILD-REQUEST.md:14, the 12 files under .dev/issues/478/).
- Files read: consolidated findings, fix log, research 01 (3.2a, 7.2-7.5, Gaps, addendum), 02 (section 6, Gaps, addendum), 03 (Gaps, addendum), 04 (section 7, Gaps, Summary, addendum A.1-A.11), 05 (all), research-notes (addendum), plus the source files named above.
- NOT independently re-read (relied on the addenda, so UNVERIFIED by me): test-51 W2d/W2e and other line refs; test-22:271-275; test-71, test-1-tool-floor, test-1-catalogue-shape, test-74, test-5-*, test-78 details; test-startup-boot:2083-2087, 2100-2156, 3030-3037, 1099-1137; installer.js:949-1037; set-overrides.js; the 46/37 SKILL.md counts. Their findings are all "NO"/"BREAKS-IF" statements; none of them changes the verdict.
- Why 4 IMPORTANT and 0 CRITICAL is credible: each IMPORTANT is a specific line-level contradiction or overclaim I located by reading both sides (05:57 vs 05 C-F1-2; 04 A.3(a)/A.10/05 S13 vs test-60:87 vs 02 A5; 03 A1 tag vs 03 Gaps 13-14; 05 matrix vs 04 A.5-A.7). The reproduced numbers matched everywhere, so no CRITICAL (wrong decision-driving number) was found. A zero-finding verdict would not have been credible given the parallel-researcher process (six addenda written independently, merged by a fix agent that edited only a few sentences).

## Summary
- Checks: 13 items evaluated (9 blocking findings + 4 criteria a-d). Passed: findings 2, 3, 5, 6, 7, 8, 9 (finding 2 with issue X-1 attached) and criterion (d) with one mis-tag; failed: findings 1 and 4, criteria (b) and (c); criterion (a) passes on method (evidence, not wording) but not on result.
- Critical 0 | Important 4 (F1-a, F1-b, F4-a, X-1) | Minor 8 (F1-c, F1-d, F4-b, X-2, 05 Summary counts, 01 section 7.5/U8 unannotated, 01 line 142 wording gap, 02 Gaps header count).
- Confidence: Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% of items evaluated with tool evidence (sub-claims listed above as not re-read are tagged UNVERIFIED).
- Tool engagement: Read: about 46 | Grep: about 18 | Glob: 2 | Bash: 2 (read-only gh and sed). Tool calls exceed the item count.

## Required fixes (for the next fix cycle; all four IMPORTANT items are blocking)
1. F1-a: in 05 line 57 replace "(C, E, F at boot)" with "(B1, D1, and E, F when run from install.sh at boot)".
2. F1-b: in 05 addendum F1.2, add rows for test-73 copy_ok (D2: BREAKS-IF a combined or second COPY of the 10-retention path or a later cleanupPeriodDays other than 90), test-52:1374-1377 and test-51:384-396 (B3, D3: BREAKS-IF edit/reuse of orca_retirement or a new locals block above line 16), test-1-catalogue-shape:25, 43-67 (B1, D1: BREAKS-IF a fourth file), each with file:line from 04 A.5-A.7; update F1.4 row 4 and F1.5 open question 2 accordingly, and drop the "In Progress" caveat U-F1-2.
3. F4-a: in 03 A1 "U8 verdict" and the addendum Summary, change "are blocked there" to "would be blocked if Claude emits the bare python3 form and the registration is present (UNVERIFIED, Gaps 13-14)", and retag that sentence [CODE-VERIFIED for the hook, UNVERIFIED for the effect].
4. X-1: reconcile B2: either re-tag 04 A.3(a), A.10 row and 05 S13 as "does not break (test-60:87 requires only one COPY line with the three sources and last token /usr/local/lib/aidev/)" and withdraw the "own COPY line" advice in 04 A.9, or state in 02 A5 why the :547-548 fold is not allowed; keep one rule across 02, 04, 05.

## Verdict
FAIL
Status: Complete

## QA Complete
