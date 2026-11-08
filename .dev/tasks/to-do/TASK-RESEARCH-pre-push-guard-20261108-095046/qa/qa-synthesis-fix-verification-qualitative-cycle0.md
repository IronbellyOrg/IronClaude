# QA Report: Synthesis Gate (Gate 2) Fix Verification, Qualitative (Coherence Lens)

**Topic:** L2 guard (git pre-push hook) semantics synthesis
**Date:** 2026-11-08
**Phase:** fix-cycle (synthesis-gate verification, coherence lens; report-qualitative checks adapted)
**Fix cycle:** 1 (verifies cycle-0 fixes B1-B8)
**Fix authorization:** false (no synthesis file was modified)

**Inputs read:** `qa/qa-consolidated-findings-phase5-cycle0.md`, `qa/qa-synthesis-fix-log.md`, `synthesis/synth-01-problem-current-state.md` (469 lines, full), `synthesis/synth-02-target-gaps-external.md` (407 lines, full), `synthesis/synth-03-options-recommendation-plan.md` (441 lines, full), `synthesis/synth-04-questions-evidence.md` (155 lines, full).

---

## Overall Verdict: PASS (with notes)

No CRITICAL or IMPORTANT issue is open. All eight blocking findings (B1-B8) are fixed, and the fixes agree with one another across the four synth files. Six NEW MINOR notes, all traceability or wording, are listed below. None of them is a contradiction about behaviour or a decision.

## Items Reviewed

### A. Per-fix verification (B1-B8)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| B1 | Stdin record order stated one way everywhere | PASS | synth-01 §2.5(a) diagram line 309 ("order undocumented, seen both ways"), order row line 330, OQ item 5 line 445; synth-02 G-24 line 195, W1-21 line 305; synth-03 G-24 mapping line 318, Phase 1.6; synth-04 row 22 (line 43) and new §9.4 row "Stdin record order (G-24)" (line 90). All say: undocumented, observed both ways (E7/G3 against E9/E19/E24), the hook scans every record. No file still claims command-line order. |
| B2 | IR-7 status consistent (default DECIDED off; refusal built and tested behind a switch) | PASS | synth-03 §7 line 179, Phase 4.4 line 248, new Phase 6.11 line 276, Phase 7.5 line 286, G-17 mapping line 311, Integration Checklist line 392, OQ-7 line 411 (asks only mechanism and turn-on criterion); synth-02 G-17 line 188, DOC-5 line 258; synth-04 row 12 (line 28) and R3 (line 69). synth-01 §1.3 line 40 is about defining "an accepted L2 is present", which is compatible. |
| B3 | One stdin rule | PASS | Same rule in synth-02 T-6 line 26, T-10 line 30, §3.3 table lines 41-44 and diagram line 60, SC-12/SC-13 lines 108-109, G-42 line 213; synth-03 Phase 1.7 line 218, Integration Checklist line 384; synth-04 row 32 (line 53): governed/unknown/no-verdict read to EOF before an allow, a refusal may exit at the first protected record (EPIPE tolerated), ordinary/released exit 0 without reading. |
| B4 | L1-8 has a step; BP/L1/DOC families mapped | PASS | synth-03 Phase 5.4 line 258 adds L1-7 and L1-8; Phase 5.5 adds DOC-9; "Gap mapping (BP-, L1- and DOC- families)" (lines 339-377) covers BP-1..14, L1-1..10 (L1-8 at line 364) and DOC-1..11 (lines 367-377), each with a Phase step or a "Covered by G-n" note. |
| B5 | Open owner decisions not shown as settled | PASS (MINOR residual, note M3) | synth-03 Phases 1.3 (line 214), 2.4 (229), 2.5, 2.7 (232) and 4.1 labelled "proposed; conditional on OQ-n"; Integration Checklist lines 382, 383 and 389 say "settled (OQ-18/20/19)"; new OQ-18/19/20 at lines 422-424. Residual unconditional wording remains in synth-02 line 35, synth-03 line 47 and the diagram at line 203 (M3). |
| B6 | One status for API/smart-HTTP/library bypass | PASS (MINOR residual, note M4) | "Documented externally (web-01 H/J); not confirmed at runtime" in synth-01 D19-30 line 395 and OQ item 1 line 441; synth-02 D19-30 line 146, G-1/G-2 lines 172-173, §4.5 line 271, §5.5 line 401; synth-03 G-1/G-2 mapping lines 295-296; synth-04 row 11 (line 27), R4/R5 (lines 70-71). Residual "CONFIRMED"/"confirmed" wording appears in synth-02 W1-26 line 310 and the synth-03 G-16 mapping line 310 (M4). |
| B7 | Version claim limited to tested 2.47.3 with re-test triggers | PASS | synth-02 §5.5 line 405; synth-03 Phase 6.10 line 275, new Phase 7.8 line 287, DOC-11 mapping line 377; synth-04 rows 34 (line 55) and 40 (line 61). The wording is the same in each: tested on 2.47.3; re-run at or above 2.54.0 and when 2.98.0 ships; record `git --version`. No "2.47.3 or later" remains. |
| B8 | synth-01 L1 row no longer overclaims | PASS | synth-01 line 30: "the non-canonical push spellings it recognises (LL-PUSH-FORM)" with the known misses listed; consistent with synth-01 §2.6 line 405 and synth-02 §4.3 L1 rows. |

### B. Coherence and proportionality checks (report-qualitative adapted to fix verification)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Story runs S2 to S8 | PASS | S2 (synth-01: L1 is advisory text-only, L2 is unbuilt, `l2_status` cannot tell an owned hook) leads to S3-S5 (synth-02: target T-1..T-n, gaps G-1..G-43, external evidence) and then to S6-S8 (synth-03: Option A recommended, a phased plan, every gap mapped to a step or an OQ). The fixed items (stdin rule, IR-7, bypass status, version scope) read the same way at each stage. |
| 2 | No fix introduced a cross-file contradiction | PASS | Cross-checked every fixed topic across all four files (table A). Only traceability gaps were found (M1, M2), and no two files state incompatible facts. |
| 3 | Recommendation follows from analysis | PASS | synth-03 Section 7 still recommends Option A with sub-choice A-i; the B5 relabelling makes the install point, marker and script location proposals without changing the recommendation's basis. |
| 4 | Gaps are honest | PASS | B6 and B7 narrowed external and version claims to documentation-only and tested-only; synth-04 R4/R5 say "not confirmed at runtime", and row 36 routes runtime confirmation. |
| 5 | Conclusion proportionate to evidence | PASS | Local-git claims rest on 04 runs on 2.47.3 and are scoped to it; library and API claims are labelled external; open owner decisions are OQ-7, OQ-18 to OQ-20 and synth-04 rows 1-21. None of these is presented as decided. |
| 6 | No circular reasoning in fixes | PASS | The fix-log evidence column cites research/04, web-01, web-02 and seed-brief lines. Where synth files cite one another (for example synth-04 row 22 to synth-03 Phase 1.6), the reference points to where a rule lives and is not used as evidence for it. |
| 7 | Open questions consistent with decisions | PASS | OQ-7 no longer re-asks the IR-7 default; R1-R3 (seed-brief 73, 74, 77) are not re-opened anywhere. synth-04 row 12's question wording is a MINOR note (M6). |
| 8 | Plan actionable after fixes | PASS | New steps 6.11 and 7.8 have targets and evidence; the Integration Checklist gates conditional steps on OQ-18/19/20. |

## Summary

- Checks passed: 16 / 16 (8 fix checks, 8 coherence checks)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- New MINOR notes: 6 (M1-M6)
- Issues fixed in-place: 0 (fix authorization false)
- Previously open blocking findings still open: 0 of 8
- Issue trend: cycle 0 had 8 blocking findings and this cycle has 0, so the count went down.

## Issues Found (NEW, introduced by or left behind by the fixes)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| M1 | MINOR | synth-04 §10 "Synthesis Files" table, line 122 | It still describes synth-03 as "(G-1 to G-43 mapping, OQ-1 to OQ-17)". After B4 and B5, synth-03 also has the BP/L1/DOC mapping table and OQ-18 to OQ-20, so the description is stale. | Change it to "(G-1 to G-43 and BP/L1/DOC mappings, OQ-1 to OQ-20)". |
| M2 | MINOR | synth-03 OQ-18/OQ-19 Gap column (lines 422-423) and G-36 mapping (line 330); synth-04 rows 2, 14, 15 (lines 18, 30, 31) | Back-references are one-directional. OQ-18 and OQ-19 give the gap as "none", but synth-04 rows 15 and 14 tie the same questions to G-20 and G-19. The G-36 mapping still points only to OQ-2 although OQ-20 now covers G-36. synth-04 rows 2, 14 and 15 do not name OQ-20, OQ-19 and OQ-18, even though the synth-04 header says each row names its OQ "where one exists". This is a traceability gap, and the subject matter agrees on both sides. | Set the OQ-18 gap to G-20 and the OQ-19 gap to G-19, add OQ-20 to the G-36 mapping row, and add OQ-20, OQ-19 and OQ-18 to synth-04 rows 2, 14 and 15. |
| M3 | MINOR | synth-02 §3.3 line 35; synth-03 line 47 ("Identity.") and §8 diagram line 203 | These state the identity entry point `~/.claude/hooks/launch-job-identity.sh identify` with no "proposed (OQ-20)" label, while Phase 1.3, the Integration Checklist and OQ-20 mark how the hook locates the script as an open owner decision. The path is the existing installed location (synth-03 Phase 1.3 cites ow:803 `IDENTITY_COMMAND`), and synth-02 G-36 still says "Undecided", so a reader is not misled about the decision. This is a residual of B5 wording. | Add "(proposed; OQ-20)" after the path in those three places. |
| M4 | MINOR | synth-02 W1-26 line 310 ("CONFIRMED (J11)"); synth-03 G-16 mapping line 310 ("bypass confirmed by web-01 H3") | "Confirmed" here means confirmed by documentation, but B6 set the single status as "Documented externally; not confirmed at runtime". Using the same word with the opposite sense invites misreading. This is wording only, and the cited evidence is the same in both places. | Change these to "documented by web-01 J11" and "documented by web-01 H3; not confirmed at runtime". |
| M5 | MINOR | synth-03 Phase 7 table, lines 286-289 | New step 7.8 sits between 7.5 and 7.6 (order 7.5, 7.8, 7.6, 7.7). This is cosmetic. | Move the 7.8 row after 7.7. |
| M6 | MINOR | synth-04 row 12, line 28 | The question still opens "does IR-7 become a refusal ... or stay the `W-L2-ABSENT` warning", although R3 and the same row's body record the default as DECIDED off. Only the mechanism and turn-on criterion are open. This is wording, and the body is correct. | Reword the question to "IR-7 switch: which mechanism, and what criterion turns it on (after #442)?" to match OQ-7. |

The N1-N12 MINOR notes from cycle 0 were not rechecked, per the review severity rule.

## Actions Taken

None. Fix authorization is false, and only this report was written.

## Self-Audit

**(a) Reliance list (rf-qa PASS items skipped for structural re-check):**
- The spawn prompt had no `## Inherited Structural Verdict` block, so nothing was inherited and nothing was relied on.
- Relied on the fix log's list of locations as a map of where to look. Every listed location was then read in the synth files, and the log's FIXED status was not taken on trust.
- Relied on the line numbers the research files cite (04 E7 line 549, E24 line 1339, web-01 G3, and so on) as the synth files quote them. I did not re-open research/04 or web-01 in this pass: the coherence lens checks agreement between synth files, not fidelity to the sources.

**(b) Independent semantic checks (my own tool work):**
- Stdin-rule identity across files (B3): I read synth-02 lines 26, 30, 41-44, 60, 108-109 and 213, synth-03 lines 218 and 384, and synth-04 line 53, and compared the three-branch rule clause by clause. The rule is identical in each.
- OQ cross-reference integrity (B5): I grepped `G-19|G-20|G-36|OQ-18|OQ-19|OQ-20|OQ-1 to OQ-17` across `synthesis/`. This found the one-directional links (M2) and the stale synth-04 line 122 (M1), which the fix log does not mention.
- Residual-wording sweep (B5, B6): I grepped `launch-job-identity.sh identify|CONFIRMED \(J11\)|confirmed by web-01 H3`. The hits at synth-02 lines 35 and 310 and synth-03 lines 47, 203 and 310 were judged against the fixed wording (M3, M4).
- Phase-numbering check: I grepped `^\| 7\.\d+ ` in synth-03 and got the order 7.1-7.5, 7.8, 7.6, 7.7 (M5).
- IR-7 decision consistency (B2): I read synth-04 row 12 and R3 against synth-03 OQ-7, line 179 and line 392. The decision content agrees, and only the row 12 question phrasing lags (M6).

**Why trust a PASS:** six findings were raised, each with a file and line. The PASS stands because none of them changes a behaviour, a decision or an evidence claim. Each fixed topic was traced in all four files, not sampled.

**Web research:** none performed, so the Tavily-first rule does not apply.

## Confidence

- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 10 | Grep: 3 | Glob: 1 | Bash: 0
- Tool-engagement note: Read + Grep + Glob = 14, which is below the 16 checks. Each full-file Read of a synth file served several checks (for example, the synth-03 read covered B2, B4, B5 and B7 and coherence checks 3 and 8), so the shortfall comes from reads that covered more than one check, not from checks left undone. It is flagged here as the protocol requires.
- No UNCHECKED or UNVERIFIABLE items.

## Recommendations

- Proceed to assembly. Optionally fold M1-M6 into the assembler's pass. They are one-line edits and do not block.

## QA Complete

