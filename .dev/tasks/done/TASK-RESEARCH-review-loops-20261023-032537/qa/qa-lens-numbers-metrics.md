# Numbers and Metrics QA Report

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md` (1,263 lines)
**Lens:** Numbers and metrics (QA phase `report-lens-numbers-metrics`, Task Step 6.7)
**Date:** 2026-10-24
**Fix authorization:** false. Report only; no file was edited.
**Intended output path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-numbers-metrics.md`. This agent may not write report files, so the parent must save this text there.
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md:1042-1149`, "Lens-Specific QA Agent Prompt Template", including the Numbers-Metrics Checklist at `:1096-1100` and the output format at `:1134-1149`.

## Overall Verdict: FAIL

Two genuine MINOR issues were found. Under the task rule, an issue of any severity is a FAIL. Neither issue changes a rank, a count of sessions, incidents or transitions, a debate tally, or any conclusion.

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | MINOR | Section 7.8, report line 763 (copied from `synthesis/synth-04-options-recommendation.md:327`) | The report says `research/evidence-deck.md` was "Read in full (901 lines, three reads)". The deck has **900** physical lines: `wc -l` and `grep -c ''` both return 900. The file was last modified at 2026-10-23 16:51:42Z, before the synth-04 producer read it, so the count was never 901. The 901st row is the Read tool's empty display row after the final newline, not a line of content. The deck's own last line is line 900 (Read at offset 896). | Change "901 lines" to "900 lines" in synth-04 line 327 and in report line 763. If a display count is kept, label it as such. |
| 2 | MINOR | Section 6, Option B, "Risk (proposed investigation only)" row, report line 527 | The text "Blocked edit attempts must not be counted as applied (records 150/151, 1164-1170)" gives physical record numbers from **two different session logs** with no session label. Records 150/151 belong to the Orca planning log (`research/01-session-ac2cd1fd.md:64,410-411`). Records 1164-1170 belong to the Orca monitor log (`research/05-session-e002bed2.md:160`). The path key at report line 448 says record numbers refer to "the original session logs" in general, so a reader cannot tell which of six logs contains each number. Every other multi-record list in Sections 6-8 names its log, for example "oracle log 291", "monitor records 585, 759-762", "parent records 1215, 1230". | Rewrite as "(Orca planning records 150/151; monitor records 1164-1170)". |

### Summary

- Total findings: 2
- Critical: 0
- Important: 0
- Minor: 2
- Verdict: **FAIL**

## Checks Performed

| # | Check | Result | Evidence |
|---|---|---|---|
| a | Quantitative claims are internally consistent: counts match between sections and sums are correct | PASS except Finding 1 | **Inventory arithmetic:** 10.1 historical 23+10+191+17+9+4+4 = 258. Superseding 23+11+204+17+9+4+4+1 = 273. 10.9: 23+11+207+17+10+4+4+1 = 277. **10.6 groups:** 15+18+18+24+24+3+3+6+8+2+2+2+2+2+2+2 = 133 review/verifier files; 12+1+5+5+8+5+6+2+10+2+1+1 = 58 other files; total 191; plus 10+1+1+1 = 204; plus 3 = 207. **Research directory:** 16 + 1 + 6 = 23, and the 10.2 table has 16 rows. **Debate:** final positions and pair tallies match the five orders. **Gaps and questions:** Section 4 has 12 gap rows, all rated Important; Section 9 has 20 questions, matching 10.10. |
| b | Effort, risk and complexity estimates are sourced or justified, not arbitrary | PASS | Effort values (M, M, M, S, S) are labelled "Reasoned estimate, not measured", each with a context-count rationale (lines 499, 526, 553, 580, 604). Limits at line 775 repeats this. Each risk level has an explicit hazard statement. No benchmark, duration or cost figure is presented. The Maintainability row is a reasoned N/A. |
| c | Size and count metrics match verifiable data | PASS except Findings 1 and 2 | Live counts: research 23, synthesis 11, qa 207 (excluding the four later `qa-lens-*` files written at 03:57), reviews 17 (4 top-level + 13 nested), phase-outputs 10, resume-analysis 4, root 4, probe 1. All six component SHA-256 values match the 10.9 table. Component line totals (210/117/105/367/163/290) and section heading positions match the 10.9 line ranges. A `diff` of report Sections 2, 6, 7 and 10 against the component ranges found byte-identical content; the only difference was my own one-line offset at the start of Section 6. Synthesis modification times match the stated 01:44Z and 03:48Z. The `t10-markdownlint.log` file is 1,006 bytes. The manifest has 30 paths plus one header line. |
| d | No unsourced statistics or probabilities presented as fact | PASS | No causal probability appears. Section 7.3 explicitly denies probabilities. Writing scores (V4 0.877, V5 0.8736, V1 lowest at 0.8469; gap 0.0034, below the 0.05 tiebreak threshold) are correctly called writing quality, not likelihood (`ADV/base-selection.md:140-155`). Convergence 1.0 and `unresolved_conflicts: 0` are correctly scoped to the ten writing points (`return-contract.md:12,16,24`). |
| S1 | Six sessions are kept separate from package incidents, review results and transitions | PASS | Six selected sessions give six incidents: 3 strict, 1 rendering blocker, 2 planning (deck:49-58; gaps:11). Monitor: 7 verdicts (6 noncompliant, 1 compliant), 5 repair passes, 4 literal `fix` replies, 5 reviewer identities (3 + 4 × 1), and no eighth verdict after acceptance at records 1250/1260/1261 (case 05:17-22, 387-401, 501). |
| S2 | Fixed and partial totals | PASS | Orca: 14 fixed + 2 partial = 16, and the narrative's 13/3 is flagged as inconsistent (case 01:92-98, 398). CI: "16 fixed, 2 partial" = 18 concerns (10 medium + 8 low), an intermediate count. The final review has 5 medium + 11 low = 16 merged items and no high item (case 04:97, 104, 283, 323). Two of four "new medium" findings were downgraded (case 04:16). Oracle: 67/78 tests passing before the first review, 74/85 after both repairs, so the test count did not grow (case 02:228-230, 248). Credential: 8 final observations, not 8 defects (case 06:270, 367-386). |
| S3 | Replayed or resumed notifications are deduplicated | PASS | Section 2.1 and 10.1 state that repeated notifications, nested copies and resumed sessions do not enlarge any denominator. Section 4's ledger row and Phase 3 "Keep results and denominators separate" keep the rule. No count in the report adds repeated messages. |
| S4 | Sample bias, the current investigation's exclusion and synthetic exclusions are counted correctly | PASS | Deck 30-slot table (deck:74-105): 6 selected (01, 04, 05, 15, 20, 27), 1 current investigation (03), 7 synthetic (21-24, 28-30), 4 controls (09, 10, 17, 19), 2 related precursors (13, 14), 10 other exclusions. Total 30. The scope-file slot ranges in 10.2 match. |
| S5 | Convergence and score provenance | PASS | Round 1 votes ACCEPT, QUALIFY, ACCEPT, ACCEPT, QUALIFY (debate:243). Round 2 votes ACCEPT, then QUALIFY ×4 (lines 277/316/356/397/438). Invariant probe: 6 HIGH assumptions addressed, 0 unaddressed (probe:6-11, 70). Post-merge validation 13/13 (validation:50; contract:26). Forward/reverse agreement 150 of 150 (base-selection:125-136). |
| S6 | Gate statistics | PASS | Phase 5: 10 reviews, all FAIL (10 files grepped); 33 groups (11 IMPORTANT, 22 MINOR); cycle 1 left 9 open groups; structural check 69/70 identities still passing; cycle 2 applied 19 patches across 9 files with no verification (synthesis-gate-decision:12, 17-18, 42-51, 65-68). Phase 3: 8 cycle-1 verifiers, 7 PASS and 1 FAIL (`structural-c`); cycle 2 of 3 authorized at 20:48:38Z (task-phase3-gate-decision:8, 71). The protocol-copy check found 7 equal pairs at 17:27:55Z and 3 equal / 4 different at 18:22:14Z (qa-research-verification-structural:93-127). |

## Confidence Gate

- **Confidence:** Verified: 4/4 checklist items plus 6/6 step-specific checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 (one call errored on size and was retried in smaller ranges) | Grep: 0 (no dedicated tool was available; content searches ran through Bash) | Glob: 0 | Bash: 16, including 7 batch scripts that each ended `BATCH_OK failures=0` with cleanup.
- **Web research:** none performed and none needed. Tavily was not attempted because there was no external lookup.

## Self-Audit

**(a) Reliance list: earlier structural results used without re-checking**
- No inherited structural verdict was provided. I did not rely on the assembler's claims in 10.10 (byte identity, brace-expansion match, gap mapping); I re-derived the numeric ones myself.

**(b) Independent semantic checks (at least one required)**
- Inventory counts: re-counted every directory with `find`, matched the qa total of 207 after excluding the four later `qa-lens-*` files, and re-added all 10.6 group sizes.
- Component identity: re-computed six SHA-256 values and diffed four report sections against their component line ranges.
- Debate tallies: re-derived every position and pair count from `ADV/debate-transcript.md:477-484` and checked them against Sections 6, 7.1 and 7.2 and the comparison table.
- Case counts: grepped case files 01, 02, 04, 05 and 06 for every fixed/partial, verdict, repair, reviewer, test and observation total quoted in Sections 2-4 and 6.
- Exclusion counts: re-counted the 30-slot screening table by category.
- Gate numbers: re-read synthesis-gate-decision lines 1-68, task-phase3-gate-decision, the verdict lines of all 8 Phase 3 verifiers, and the 10 Phase 5 reviews.
- Line counts: checked the deck's line count three ways (`wc -l`, `grep -c ''`, Read display), which found Finding 1. Checked record-anchor ownership by grepping case files 01, 04 and 05, which found Finding 2.

**Checked and found clean:** the stated limits on sample bias and prevalence; the absence of any probability; effort figures labelled as reasoning; the scope of the 1.0 convergence score; all five 7.1 rank rows; and the verification limit in the header ("nine open groups unverified"), which matches the gate record.

## Recommendations

- Apply the two one-line fixes in `synthesis/synth-04-options-recommendation.md` (line 327, and the Option B Risk row) and in the matching report lines 763 and 527. Then re-run only this lens.
- Neither fix changes any count, rank or conclusion.

## QA Complete

| Status | Result |
|---|---|
| DONE | Reviewed the full 1,263-line report against the numbers lens. Re-derived its counts, sums, tallies, hashes, gate statistics and exclusions from the files on disk. |
| DONE | Verdict FAIL: 2 MINOR issues. The deck line count should be 900, not 901. Record anchors 150/151 and 1164-1170 at report line 527 do not name their session logs. |
| NEXT | Parent saves this text at `qa/qa-lens-numbers-metrics.md` with attribution. This agent could not write report files. |
| NEXT | The single fix agent applies both one-line corrections in synth-04 and the report, then this lens is re-run. |