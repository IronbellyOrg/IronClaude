# QA Report — Synthesis Gate, Qualitative (coherence lens)

**Topic:** git pre-push hook semantics behind the L2 launch-level guard
**Date:** 2026-11-08
**Phase:** report-qualitative (adapted to synthesis-gate; lens: coherence)
**Fix cycle:** N/A (first review)
**Fix authorization:** false (report only; no synthesis file was modified)
**Files reviewed:** `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps-external.md`, `synthesis/synth-03-options-recommendation-plan.md`, `synthesis/synth-04-questions-evidence.md` (all read in full)
**Reference checked:** `research/04-empirical-git-prepush-experiments.md`, `research/web-01-git-official-docs-and-versions.md`, `.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` lines 65-79, `tests/hooks/`

---

## Overall Verdict: FAIL

Seven blocking findings (0 CRITICAL, 7 IMPORTANT) and 6 MINOR notes. The S2 -> S8 narrative is mostly coherent, and Option A is a sound recommendation for a guard that must refuse only a governed agent's push to main/master. The four files still disagree with each other on five facts (stdin handling, stdin order, IR-7 status, bypass status, L1 coverage), and two plan steps settle questions the seed brief leaves open.

## Items Reviewed

| # | Check (report-qualitative, adapted to the synthesis set) | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings | PASS | synth-01 §1 asks how L2 can refuse a governed push to main/master. §2-§8 answer that question; no drift into unrelated topics. |
| 2 | Current state is current, not aspirational | FAIL | synth-01 line 30 says L1 refuses "every non-canonical push spelling"; synth-01 line 405 lists spellings that pass (finding 7). |
| 3 | Options genuinely distinct | PASS | synth-03 §6 A (default common-dir hook), B (`core.hooksPath` dir), C (`extensions.worktreeConfig`) differ in placement, config migration and scope. The comparison (synth-03 line 138) states honestly that all three have the same push-bypass surface. |
| 4 | Recommendation follows from analysis | PASS (with findings) | Option A follows from design §19.2's ban on hooksPath migration and worktreeConfig, and from equal bypass surfaces. The unknown -> main/master-only refusal matches seed-brief line 73. Plan coherence issues are findings 1, 3 and 4. |
| 5 | Plan actionable | FAIL | Phases 1.7, 2.x and 4.4 contradict decided or open items (findings 1, 3, 4). |
| 6 | Gaps honest | FAIL | The status of API, smart-HTTP and library bypasses differs between files (finding 5). The stdin-order contradiction is not carried to §9.4 (finding 2). |
| 7 | External research relevant | PASS | web-01 and web-02 drive the parser (W1 right-split), publication (W2-7..W2-15) and the version table (§5.3). These are not padding. |
| 8 | Scale and version claims substantiated | FAIL | "pin git 2.47.3 or later" generalizes past the release notes cited in the same section (finding 6). |
| 9 | Risk assessment complete | FAIL | Finding 6 (version ceiling missing); notes M3 and M4 (residual fail-safe risks not stated). |
| 10 | Evidence trail complete | PASS (with note) | synth-04 §10 maps every research file. It omits F4 (note M1). |
| 11 | No circular reasoning | PASS | Claims cite research files 01-04 and web-01/02, not other synth files. synth-04 row 2 refers to synth-03 only as "synth-03 proposes", which is accurate. |
| 12 | Conclusion proportionate | FAIL | Finding 6. Note M6 (Critical ratings on static evidence). |

## Issues Found

| # | Severity | Synth file and section | Finding | Proposed fix |
|---|----------|------------------------|---------|--------------|
| 1 | IMPORTANT | synth-03 Phase 1.7 (line 218) and Integration Checklist (line 342) vs synth-03 Shared sub-choice 2 (line 109), synth-02 T-10/SC-13 (lines 30, 108), synth-04 row 32 (line 53) | **Contradiction on stdin handling.** Phase 1.7 says "Drain stdin to EOF in every path ... including on allow". synth-03 line 109 (the owner-decided mapping) and synth-02 T-10 (design D19-26) say ordinary and released verdicts "allow without reading the stream". synth-04 row 32 still lists "Decide whether to drain stdin" as open, while synth-02 G-42 (line 212) already sets the target "Hook drains stdin". synth-02 T-6 (line 26) is also internally inconsistent: it says the hook "reads stdin to EOF before it decides", then "A refusal can exit early". The same fact has three different states across three files. | Pick one rule and use it in all four files. Suggested rule: governed and unknown verdicts read every record (needed to decide); ordinary and released exit 0 without reading (D19-26); a refusal may exit as soon as a protected record is seen (EPIPE tolerated, web-01 Area I). Rewrite Phase 1.7 and checklist line 342 to match, fix T-6, and move synth-04 row 32 to §9.3 Resolved or reword it as "confirm the rule above". |
| 2 | IMPORTANT | synth-01 §2.5(a) (line 330) vs synth-02 W1-21 (line 304), synth-03 G-24 (line 316), synth-04 row 22 (line 43); synth-04 §9.4 (lines 84-90) | **Stdin-order contradiction not carried to §9.4.** synth-01 says stdin order "is not command-line order" (E9, E19, E24). synth-03 G-24 says "order followed the command line in tests". synth-04 row 22 says "one test (04) saw command-line order". The research supports both: 04 line 549 observed command-line order in one run, and 04 line 1339 (E24) observed order "independent of command-line order". web-01 lines 428 and 471 report only the first. Each synth file picked one side, and §9.4 lists neither. The practical rule (scan every record) is the same either way, but the files state contradictory facts. | Add a §9.4 row: "Stdin record order — 04 line 549 / web-01 G3: command-line order for simple refspecs; 04 E24 (line 1339): independent of command-line order, existing remote refs first [inferred]. Stronger evidence: 04 E24 (two runs, mixed order). Neither is documented." Then reword synth-03 G-24 and synth-04 row 22 to "order is undocumented and was observed both ways", and keep synth-01's claim scoped to E24. |
| 3 | IMPORTANT | synth-03 §7 (line 179), Phase 4.4 (line 248), Phase 7.5 (line 285), OQ-7 (line 369), G-17 mapping (line 309); synth-02 G-17 (line 187) | **IR-7 status disagrees with the seed brief and with synth-04.** seed-brief line 77 records the default as DECIDED (off: `W-L2-ABSENT` stays a warning, built in a separate clearly marked commit), and seed-brief line 68 requires that "the IR-7 refusal path exists and is tested, ships switched off". synth-04 R3 and row 12 record this correctly. synth-03 says "This document does not decide it (G-17)", makes Phase 4.4 an either/or ("Only if the owner chooses the design's refusal ... Otherwise keep the warning"), and OQ-7 asks the already-answered question. As written, the plan could ship without the refusal path, which violates seed-brief line 68. | Rewrite Phase 4.4 as: build the one-line refusal behind a switch that defaults off, in its own clearly marked commit, with a test for both switch states. Replace OQ-7 with the questions that are actually open (seed-brief line 77: switch mechanism and the turn-on criterion after #442). Update synth-03 §7 line 179 and synth-02 G-17 to say "default DECIDED off; mechanism and turn-on open". |
| 4 | IMPORTANT | synth-03 Phases 1.3 (line 214), 2.1-2.4, 2.7 (line 232), 4.1; Integration Checklist (lines 340-341); OQ list (lines 360-380) vs synth-04 rows 2, 14, 15 and seed-brief lines 75, 76, 78 | **The plan presents open owner decisions as settled.** seed-brief lines 75 (U28: which command installs the hook, and where), 76 (ownership/version marker; byte equality or hash) and 78 (how the hook finds the identity script; what it does when the script is missing) are open, and synth-04 rows 2, 14 and 15 list them as open brainstorm decisions. synth-03 writes a concrete step for each: Phase 1.3 fixes the script at `~/.claude/hooks/launch-job-identity.sh`; Phase 2.4/2.5 choose "full bytes equal the installed guard source" (byte equality, no version marker); Phase 4.1 puts the install in `cmd_launch` before `l2_status`. OQ-1..OQ-17 (lines 362-380) have no entry for U28 or the marker. OQ-2 covers only the "no verdict" mapping, not where the script is found. A reader of synth-03 alone would think U28 and the marker were decided. | Add OQ entries for seed-brief lines 75, 76 and the script-location part of 78, cross-referenced to synth-04 rows 15, 14 and 2. Label Phases 1.3, 2.x (install point, marker) and 4.1 "proposed; conditional on OQ-n". Keep the proposals; they are reasonable. |
| 5 | IMPORTANT | synth-01 Open Questions item 1 (line 441) and line 395; synth-02 §4.5 (line 270) vs synth-02 G-1/G-2 (lines 171-172) and D19-30 (line 145); synth-03 G-1/G-2 (lines 293-294); synth-04 R4/R5 (lines 70-71) | **One fact, three statuses: do API writes, smart-HTTP and library pushes bypass pre-push?** synth-01 lists it as an open question. synth-02 calls it "Answered" and "CONFIRMED" at lines 145 and 171, then says it "Stays an open question for runtime confirmation" at line 270, in the same file. synth-03 and synth-04 list it as "Resolved". The evidence is documentary only (web-01 Areas H and J; no local run, and the libraries are not installed per synth-04 row 36). | Use one status in all four files: "Documented externally (web-01 H/J); not confirmed at runtime." In synth-04 move R4/R5 to a "resolved by documentation" sub-label, or keep them in §9.2 with the runtime-confirmation action. Fix the internal inconsistency in synth-02 (line 145/171 vs line 270). Make synth-01 OQ item 1 point to the documentary answer. |
| 6 | IMPORTANT | synth-04 row 40 (line 61), synth-04 row 34 (line 55) action; synth-02 §5.5 "Version risk" (line 404) vs synth-02 §5.3 (lines 360-364) | **Observed 2.47.3 behaviour generalized to later versions without a citation.** synth-04 row 40 recommends "pin git 2.47.3 or later". synth-02 §5.3 itself cites release notes showing that pre-push moves to the hook API in 2.54.0, that configuration-defined hooks arrive in 2.54.0, that parallel hooks arrive in 2.55.0, and that `hook.pre-push.enabled=false` disables hooks-directory hooks in a 2.98.0 draft. "Or later" asserts that the observed contract (`find_hook` X_OK fail-open, one nonzero exit aborts, record shape) holds on versions that changed the code path, with no release note saying it does. web-01 R7 asks for a pinned version, not a floor. | Replace "2.47.3 or later" with "tested on 2.47.3; re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (hook API rewrite, configured hooks) and when 2.98.0 ships". Have the guard tests record `git --version` and name the re-test triggers in synth-03 Phase 6 and in design §19. |
| 7 | IMPORTANT | synth-01 §1 L1 row (line 30) vs synth-01 §2 coverage table (line 405) and 02 Gaps | **Aspirational coverage stated as current.** Line 30 says L1 "refuses ... every non-canonical push spelling (LL-PUSH-FORM)". Line 405 of the same file says the underscore env prefix plus an obfuscated subcommand or alias passes [CODE-CONTRADICTED vs line 80], and that smart-HTTP `curl` to `git-receive-pack`, library pushes and script pushes pass. This is the red flag named in the brief: behaviour stated as current that the evidence contradicts. It also undercuts the problem framing, because the residual L1 gaps are the reason L2 is needed. | Reword line 30: "refuses canonical pushes to main/master and the non-canonical spellings it recognises (LL-PUSH-FORM); known misses: underscore env prefix with an obfuscated subcommand, smart-HTTP `curl`, library and script pushes (see 2.x, 02 Gaps)". |
| M1 | MINOR | synth-04 §10 row for 04 (line 98); synth-04 §9.4 D19-42 row (line 86) | 04 is described as covering "E1-E31, F1-F3". File 04 also has F4 (04 line 2126), which synth-01 line 384 and synth-02 T-11/SC-22 cite. | Change to "E1-E31, F1-F4". In the D19-42 row, check whether F4 records are included and keep it as F1-F3 only if F4 delivered no records (F4's hook never ran). |
| M2 | MINOR | synth-04 row 32 (line 53) vs synth-02 T-6, SC-12, G-42 and synth-03 Phase 1.7 and 6.2 | The large-push sandbox is described as "3000 refs" (synth-04) and "3001 branches" (synth-02, synth-03). The two figures probably describe the same run (3000 pushed refs plus an existing branch), but they read as different tests. | Use one phrasing everywhere, for example "3000 new refs pushed (3001 branches on the remote)". |
| M3 | MINOR | synth-03 Phase 1.3 (line 214), Shared sub-choice 2 (line 113), checklist line 341 | The hook finds the identity script through `~/.claude/hooks/...`, which the shell expands from the pusher's HOME, while PATH is fixed at install time. A governed agent that sets HOME can point the hook at its own script. This adds no new escape beyond the accepted different-HOME escape (synth-03 line 170, OQ-4), but it is not stated, and it bears on the open seed-brief line 78. | In OQ-4 or the new OQ for seed-brief line 78 (finding 4), say that a HOME-relative script path is part of the HOME escape, and offer an absolute script path recorded at install time as the alternative. |
| M4 | MINOR | synth-03 §7 bypass/residual table (lines 160-175) and Phase 4.1 | Two fail-safe residuals are not listed: (a) variant A-i records the uv directory at install time, so a later uv reinstall or move makes `identify` exit 2, which maps to `unknown` and refuses humans' main/master pushes until the hook is reinstalled (fails closed, but it is a false refusal the plan does not mention); (b) the launch-time `l2_status` recheck cannot detect the hook being removed or made non-executable later in the session (E29 fail-open). | Add both rows to the residual-risk table with their mitigations (reinstall diagnostic; L1 tamper token from synth-03 line 138; server-side protection). |
| M5 | MINOR | synth-03 lines 42, 91 ([OBSERVED 2.47.3]) vs synth-01/synth-02 ([CODE-VERIFIED] for the same sandbox observations); synth-02 D19-18 (line 135) and DOC-5 (line 257) | The evidence tags are inconsistent: the same real-git sandbox runs are tagged [CODE-VERIFIED] in synth-01/02 and [OBSERVED 2.47.3] in synth-03. Tagging design IR-7 as [STALE DOC] presumes the refusal will not be adopted, which conflicts with seed-brief line 68 (the refusal path is built, switched off). | Use [OBSERVED 2.47.3] for sandbox observations in all files. Retag DOC-5 as "[DESIGN AHEAD OF CODE] (refusal path to be built switched off)". |
| M6 | MINOR | synth-02 §4.2 BP-7 and BP-9 (lines 225, 227) | BP-7 and BP-9 are rated Critical. The L2 part rests on documentation and the L1 part on static readings of the guard (02 §9 "static readings"); neither was executed. The ratings may be right, but the evidence strength is not stated next to them. | Add "(documentary + static reading; not executed)" to the evidence column, or rate them "Critical (provisional)". |

## Summary

- Checks passed: 6 / 12 (1, 3, 4, 7, 10, 11; rows 4 and 10 pass with findings or notes)
- Checks failed: 6 (2, 5, 6, 8, 9, 12)
- Critical issues: 0
- Important issues: 7 (findings 1-7; five of them are cross-file contradictions, which are always blocking)
- Minor notes: 6 (M1-M6; recorded only, they do not affect the verdict)
- Issues fixed in-place: 0 (fix_authorization: false)

**Answers to the brief's questions:**

1. **Does the story build S2 -> S4 -> S6 -> S7 -> S8?** Mostly yes. The current state (synth-01) leads to the gaps (synth-02 G/BP/L1/DOC tables), then to three distinct options, a recommendation grounded in design §19.2 and equal bypass surfaces, and a phased plan with a G-1..G-43 mapping. It breaks where the plan (S8) diverges from decided or open items: findings 1, 3 and 4.
2. **Are conclusions proportionate to the 2.47.3 evidence?** Mostly. synth-02 §5.3 and §5.5 limit claims to 2.47.3 correctly; synth-04 row 40 does not (finding 6).
3. **Are contradictions between research files resolved or carried to S9?** Not fully. §9.4 has four rows but omits the 04-internal and 04-vs-web-01 stdin-order disagreement (finding 2). The synth files also contradict each other on stdin handling, IR-7 and bypass status (findings 1, 3, 5).
4. **Does the recommendation fit a guard that must refuse only a governed agent's push to main/master and fail safely?** Yes in substance. Option A with the owner-decided verdict mapping refuses governed pushes to protected refs, refuses `unknown` only for main/master, and maps "no verdict" to `unknown` (fail-closed for protected refs only). Two residual fail-safe gaps are unstated (M3, M4). The bypasses that fail open (exec bit, hooksPath, `--no-verify`, libraries, API) are listed with owners in synth-03 §7, not dropped.
5. **Red flags.** Aspirational behaviour stated as current: finding 7. Bypasses silently dropped: none found; every bypass in 04 and web-01 appears in the synth-03 §7 table. The four files disagree about the same fact: findings 1, 2, 3 and 5.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt, so there was nothing to rely on. Standalone behaviour applied: structural facts used in findings (line numbers, file existence) were checked directly.
- Relied on the earlier Gate 1 QA reports (`qa/qa-research-fix-log.md` and others) only for the provenance labels synth-04 attributes to them (B1-B4, N-3). Those labels were not re-verified.

**(b) Independent semantic checks (>= 1 required, INV-019):**
- Stdin order: Grep across the task dir found 04 line 549 ("in command-line order here") and 04 line 1339 ("independent of command-line order"), plus web-01 lines 428 and 471. The research itself holds both observations, so each synth file's single-sided statement is incomplete (finding 2).
- IR-7, U28, marker and identity lookup: Read `seed-brief.md` lines 65-79. Line 68 (refusal path built, switched off), line 77 (default DECIDED off), and lines 75, 76 and 78 (open). Compared against synth-03 lines 179, 248, 369 and OQ-1..OQ-17 (Bash `sed` of synth-03 lines 358-380). This gave findings 3 and 4.
- Stdin drain: Grep for D19-26, "without reading" and EOF showed synth-03 line 109 vs line 218, synth-02 T-6/T-10, and synth-04 row 32 (finding 1).
- Bypass status: Grep for R4/R5, D19-30, REST and libgit2 showed synth-02 lines 145/171 vs 270, synth-01 line 441, and synth-04 lines 70-71 (finding 5).
- Version claim: Read synth-04 lines 53-82 (row 40) and synth-02 §5.3 lines 344-364 (finding 6).
- Test-path suspicion (pre-review candidate): Glob `tests/hooks/test_launch_level_guard*.py` returned both `test_launch_level_guard.py` and `test_launch_level_guard_with_identity.py`. The two names cited in synth-03 Phase 6.7 and synth-04 rows 7, 8 and 29 both exist, so this candidate was **dropped**. This is the check that rejected one of my own hypotheses.
- F4: Grep showed 04 line 2126 "### F4." and synth-04's "E1-E31, F1-F3" (M1).

**Answers to the mandatory self-audit questions:**
1. Factual claims independently verified: 19 (the seven blocking findings, each against at least two locations; M1-M3; and the dropped test-path candidate).
2. Files read: the four synth files (in full), seed-brief lines 65-79, and targeted Grep hits in `research/04-*.md` and `research/web-01-*.md`. `tests/hooks/` was checked by Glob.
3. Not applicable: 7 blocking findings were found.
4. No web research was performed, so no Tavily or fallback calls were made.

## Confidence and Tool Engagement

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 7 | Glob: 4 | Bash: 2 (read-only `sed`/`cut` excerpts of synth-04 and synth-03) | Web: 0 (no Tavily, WebSearch or WebFetch)
- Read + Grep + Glob = 19, which is at least the 12 checklist items.
- Unchecked items: none.
- Unverifiable items: none at the checklist level. Limitation: the research files 01, 02, 03 and web-02, `gaps-and-questions.md` and `BUILD-REQUEST.md` were not read end to end. Spot checks targeted the contested facts only, so errors that the synth files copied faithfully from those sources would not be detected here.

## Recommendations

1. Resolve findings 1, 3 and 5 first. Each is a single fact that needs one wording used in all four files.
2. Add the stdin-order row to synth-04 §9.4 (finding 2).
3. Add OQ entries and "conditional" labels in synth-03 for seed-brief lines 75, 76 and 78 (finding 4). Rewrite Phase 4.4 to build the IR-7 refusal path switched off (finding 3).
4. Replace "2.47.3 or later" with a tested version plus re-test triggers (finding 6). Reword synth-01 line 30 (finding 7).
5. Apply M1-M6 where convenient; they are not required for PASS.
6. Re-review after the fixes (fix cycle 1 of at most 2).

## QA Complete

