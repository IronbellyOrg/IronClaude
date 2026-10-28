# QA Report: Phase 6 Gate, Numbers and Metrics

**Topic:** Phase 6 final-state deliverables of `R/TASK-RESEARCH-review-loops-20261023-032537.md`
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Date:** 2026-10-24
**Phase:** Phase-gate QA, Phase 6, content lens "numbers and metrics" (rf-qa-qualitative, report-qualitative adapted)
**Fix authorization:** false (report-only; no file edited, no Git command run, no session `.jsonl` log opened)
**Target identity checked:** `R/RESEARCH-REPORT-review-loops.md`, 1,316 lines, sha256 `41145b5e9660967e6f6498efb90da18bbfcd51eb3a81a0850fbdcde29fca40a0` (recomputed, matches the brief)
**Known user-accepted defects excluded:** J1 (stale status lines, now Report:5 and :1241), L1, L2, L3 (the missing original CI plan at Report:851 was re-observed as absent; it is L3 and is not counted here). The non-consensus order V1 > V3 > V2 > V5 > V4 was confirmed unchanged.

Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Sample denominators: 30 slots, 7 synthetic, current investigation excluded, 6 selected, 3 strict + 1 blocker + 2 planning | PASS | Report:105-121, :312, :509-510, :1027 against `R/research/evidence-deck.md:47-58,72-105`. The seven synthetic slots are 21-24 and 28-30. The scope-01/04/05 slot summaries at Report:1039-1043 match the deck dispositions. |
| 2 | Per-incident review and repair counts (3/2, 3/2, 2/1, 2/1, 7/5, 3/2) | PASS | Report:127-134 matches deck:149-156 row for row. Monitor: 7 verdicts, 5 repairs, 4 `fix` replies, 5 reviewer identities, confirmed at `R/research/05-session-e002bed2.md:18-21,491-501`. The verdict records are 697, 804, 849, 906, 1021, 1143 and 1240. Record 585 is the workflow write, not a verdict. |
| 3 | Finding counts (16 = 14 + 2 vs the 13/3 summary, 20 numbered items, 18 concerns, 16 = 5 medium + 11 low, "16 fixed, 2 partial", four oracle defects, 67/78 tests, eight observations) | PASS | `01-session-ac2cd1fd.md:68,92-97,398`; `04-session-43582de1.md:97,104,121,286,328`; second CI `merged-verdict.yaml` has 5 `severity: medium` and 11 `severity: low` (16 items); `REPORT.md:21` "fixes 16 of the 18 ... other 2 in part"; `02-session-a9b88895.md:228`; `t12-review-1.md:20-35` has four findings; `06-session-0690ee9f.md:270`. |
| 4 | Debate tallies and vote vectors (5/5, 3/5, 2/5; final positions per option; Round 1 and Round 2 A-001 vectors) | PASS | `ADV/debate-transcript.md:243` [ACCEPT,QUALIFY,ACCEPT,ACCEPT,QUALIFY]; `:277` ACCEPT; `:316,356,397,438` QUALIFY; `:480-484` five orders. The per-option positions 1/1/1/1/1, 2/2/3/3/3, 3/3/2/2/2, 4/4/4/5/5 and 5/5/5/4/4 were recomputed from those orders. Pair tallies at Report:698-705 were recomputed and are correct. |
| 5 | Score and convergence provenance (convergence 1.0, unresolved_conflicts 0, writing order V4,V5,V2,V3,V1, tiebreak gap, 150/150 agreement, six HIGH probe items, 13/13 post-merge checks) | FAIL (N2) | `return-contract.md:12,16`; `base-selection.md:136-150` (V1 lowest at 0.846875; gap 0.0034 < 0.05); `invariant-probe.md:4-11,68-72`; `adversarial-post-merge-validation.md:21,41,50`. The values are correct. One citation does not contain its number (N2). |
| 6 | Inventory arithmetic (258, 273, 277; 133 + 58 = 191; 191 + 13 = 204; 204 + 3 = 207; research 23 = 16 + 1 + 6; reviews 17 = 4 + 13) | PASS for arithmetic; FAIL for final-state currency (N1) | All sums were recomputed. A live `find` now gives 341 package files: qa 266, phase-outputs 15, research 23, synthesis 11, reviews 17, resume-analysis 4. |
| 7 | Artifact sizes and counts cited in Options D and Section 8 | PASS | Oracle artifacts: 43 entries. Credential `subagents/`: 45 `.jsonl` files. Byte sizes by `stat`: builder transcript 2,021,102; coverage matrix 72,087; merged verdict 29,095; t3 log 1,222; t10 log 1,006. Screening values 1,222 and 11,215 are at `scope-03-recovered.md:158,162`. Regenerated CI plan sha256 `895dcd6b...` matches `04-session:476`. |
| 8 | Timestamps and observation windows (03:41:52.643460Z, 04:02:04.400203Z, 04:03:52.359004Z, 1-1247 rows ending 03:31:57.433Z, rubric loads 20:26:30.085Z / 20:32:19.277Z, install 20:29:54Z, pair comparisons 17:27:55.147Z / 18:22:14.768885Z) | PASS (subset unverifiable, listed below) | `04-session:68,74,281,464`; `05-session:317,329,345`; deck:281,284,797-800; `06-session:246-255`; `stat` of installed `qa.md`/`retry.md` gives 2026-10-22 20:29:54.0176Z; `gaps-and-questions.md:56`; `qa-research-verification-structural.md:101,106`. |
| 9 | Captured-rubric line citations (before :65, :79; after :66-68, :82) and hashes | PASS | `jq` decode of `historical-review-rules.json` records.before and records.after confirms the cited lines. Hashes `0b533765...` and `faff03b7...` match `scope-rules.md:70-71`. Installed `qa.md` sha256 is `faff03b7...d2e7d5`. |
| 10 | Installed-layer line equivalents (workflow :60/:74, retry :142/:144/:146, qa :82, managed-workspace :43 and :85-86, ledger :142, ledger 243 vs 242 lines) | PASS | Direct `sed`/Read of `/config/.claude/skills/...`. The ledger has 242 newline-terminated lines and the Read tool shows 243, so "1-243 of 243" is consistent. |
| 11 | Question counts (15 deck questions, 18-row applicability inventory, 20 report questions) and gap-to-question mapping | PASS | deck:831-845 has 15 rows; `web-01-gap-applicability.md:32-49` has 18 rows (15 + 3); Report:946-967 has 20 rows; 10.10 mapping at Report:1270-1283 was checked. |
| 12 | Gate-decision cycle and patch counts (31→9→2→2; 10→6→3; 36→7→0; 181/15/4, 42/41, 78/14 patches; 69 of 70; 55/55; 290 = 210 + 76 + 3 + 1; 14,511 = 2,062 + 4,188 + 1,524 + 6,737; fidelity load 7,397-7,622) | FAIL (N5, N6) | `report-gate-decision.md:16-28,59-66,82-99`; `fidelity-gate-decision.md:16-25,67-84`; `anti-omission-gate-decision.md:16-31,56-67`; the task log Phase 6 entries agree; `anti-omission-input-map.md:43,59,72,102,205`; `fidelity-source-map.md:367-373`. |
| 13 | Synthesis components consistent with the report's numbers | FAIL (N4) | `diff` of Report §1-2, §3-4, §8 and §9-10 against synth-01/02/05/06; `grep` of synth-04 Effort rows. |
| 14 | Component-change accounting in 10.9 against the files on disk | FAIL (N3) | Current sha256 prefixes: synth-01 `06ec1047`, synth-02 `5da15419`, synth-03 `b0a561a5`, synth-04 `b7ea841f`, synth-05 `994f3502`, synth-06 `bdf94b0d`. All six differ from the assembly hashes at Report:1255-1260. |
| 15 | No probability or percentage where the report disclaims one; ranking criterion quoted | PASS | Zero `%` characters in the report. Every "likelihood"/"probab" hit (Report:88, 90, 319, 340, 363, 495-498, 719-720, 895, 966, 1288) is a disclaimer. `BUILD-REQUEST.md:12,34` quotes were verified. |

## Summary

- Checks passed: 10 / 15
- Checks failed: 5 (items 5, 6, 12, 13 and 14)
- Issues: CRITICAL 0, IMPORTANT 2, MINOR 4 (six total, N1-N6)
- Issues fixed in place: 0 (report-only)
- The core empirical numbers in the report (denominators, finding counts, tallies, ranks, hashes, byte sizes, timestamps) all match their primary sources. The defects are in bookkeeping: an evidence-trail count frozen at assembly, one citation that does not contain its number, an understated list of changed components, synth-04 still carrying superseded effort and context counts, an unexplained failure-set basis in the anti-omission gate, and stale status headers in two gate decisions.
- The adversarial target of at least 15 errors was not reached. Six were found with tool evidence, and no findings were invented to meet the target. The Self-Audit below shows the coverage.

## Issues Found

| ID | Severity | Location path:line | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| N1 | MINOR | `R/RESEARCH-REPORT-review-loops.md:9`, `:1212-1222`, `:1291` | The evidence-trail inventory stops at the assembly snapshot (277 files; qa 207; phase-outputs 10). Yet the 10.10 check "Evidence trail lists every package file: Pass" sits in a table whose "Assembly changes" row (:1293) was updated through Step 6.42. The report cites Phase 6 artifacts that no Section 10 table lists, for example `qa/qa-fix-log.md` (:8), `qa/qa-consolidated-findings-phase6.md` (:5) and `phase-outputs/plans/report-gate-decision.md` (:1241). This is related to J1's root cause (live state carried inside the report) but involves different lines and a count/completeness claim, so it is not J1 itself. | A live `find` gives 341 files (qa 266, phase-outputs 15: the three Phase 6 gate decisions plus `discovery/fidelity-source-map.md` and `discovery/anti-omission-input-map.md`). `grep` finds no Section 10 row for `qa-fix-log.md` or the Phase 6 gate decisions. | Append a dated, attributed Phase 6 inventory row group (counts plus the Phase 6 qa and phase-output files the report cites), or relabel the :1291 check explicitly as "at assembly, 03:51:27Z; not refreshed after Phase 6". Do not rewrite the earlier dated rows. |
| N2 | MINOR | `R/RESEARCH-REPORT-review-loops.md:499` | "Post-merge validation: PASS, 13 of 13 checks" cites `qa/adversarial-post-merge-validation.md:120`. That line is the scope sentence and contains no check count, so the score's provenance points to the wrong line. | `adversarial-post-merge-validation.md:21` ("All 13 checks below are [x] VERIFIED"), `:41` ("Checks passed: 13 / 13"), `:50` ("Verified: 13/13"); `:120` begins "This PASS establishes...". | Cite `:41` (optionally `:21,41,120`, with :120 kept for the scope limit). |
| N3 | MINOR | `R/RESEARCH-REPORT-review-loops.md:1262` | It lists the later-changed components as synth-01/04/05 (Step 6.18) and synth-01/02/04 (Steps 6.29 and 6.32), which implies synth-03 and synth-06 kept their assembly hashes. The report's own :1293 says Step 6.39 changed synth-01 through synth-06, Step 6.42 changed synth-01/04/06, and report-gate cycle 2 changed synth-04. The two passages disagree on how many components changed. | All six current sha256 prefixes differ from the assembly hashes at :1255-1260 (for example synth-03 `b0a561a5` vs `ca519125`; synth-06 `bdf94b0d` vs `bcffe37a`). The mtimes are 18:09:40Z and 18:26:24Z on 2026-10-24. | Extend :1262 to name every later change pass and the affected components (all six), or replace the list with a pointer to :1293. |
| N4 | IMPORTANT | `R/synthesis/synth-04-options-recommendation.md:144`, `:185`, `:291` | synth-04 still carries the superseded quantitative assessment: Option D Effort "S. ... two sessions" (:144), comparison row "M \| M \| M \| S \| S" (:185), and order 3 "Option D and E checks on their two incidents each \| Cheap" (:291). The report gives Option D Effort M (re-rated, Report:615), the row "M \| M \| M \| M \| S" (:656), and "Option D on its one incident and two controls (three contexts in two sessions) ... E is cheap (S); D needs reconstruction (M)" (:762). Two deliverables of this gate contradict each other on the same quantities. Report:1293's general note that "the other corrections exist only in this report" does not identify these divergent values. | `grep` of synth-04 Effort and comparison rows against Report:615, :656, :762. | Apply the matching correction to synth-04:144, :185 and :291, or add an explicit, dated divergence note in synth-04's provenance record naming these three values. |
| N5 | MINOR | `R/phase-outputs/plans/anti-omission-gate-decision.md:27` (with `:19`) | The cycle-0 failure set is stated as "36 (34 omissions + PF-01 + PF-02)". Line 19 lists process findings PF-01 to PF-03, and PF-03 (IMPORTANT, wrong block-level dedup) is left out of \|F_0\| with no stated basis. The total 36 also equals the count of O-IDs O-01 to O-36, which include the two DEDUP items, so the basis of the strict-shrink guard is ambiguous. | `qa/qa-anti-omission-consolidated-findings.md:55` ("36 unique omissions"), `:225` ("38 proposed omissions into 36 unique IDs: 34 RECOVER ... and 2 DEDUP"), `:252` ("New process finding PF-03 (IMPORTANT)"). | Append a dated note stating the counting basis and why PF-03 is excluded (for example, resolved inside the consolidation), or count it (\|F_0\| = 37). Either way the 7 → 0 outcome is unchanged. |
| N6 | IMPORTANT | `R/phase-outputs/plans/fidelity-gate-decision.md:5`; `R/phase-outputs/plans/report-gate-decision.md:5` | Both Status headers still read "... Task Blocked pending a user decision". Each file's own appended record shows the user authorized advancement: fidelity :92-99 ("Accept and continue"), report gate :110-118 ("Confirm and proceed, no need to fix"). The current-state header contradicts the file's terminal record. The anti-omission decision updated its own header (`anti-omission-gate-decision.md:5`). | Direct Read of all three gate decisions. The task log entries at 05:48Z and 11:54Z confirm the advancements. | Append to each Status line a pointer such as "superseded by the User-Authorized Advancement Record (not a PASS)". Do not rewrite the dated history. |

## Unverifiable sub-claims (documented blockers, not counted as issues)

These claims could only be checked by opening session `.jsonl` logs or running Git, which the brief prohibits:

- The out-of-window monitor records at Report:149 (1620-2049, 1670, 1997, 859) and CI record 1087.
- The live log line counts at 04:37Z (954, 1,447, 1,081, 1,153, 2,058, 2,095) at Report:140-145. For context, case 01 independently records 954 lines.
- The record-874 ledger hash `bd66451d...` and its 20:34:06.655Z timestamp at Report:583. They are consistent with `05-session:92` (records 869-885 at 20:33:59-20:34:18).
- The master `2165ae25` commit time 20:29:01Z at Report:229.

## Self-Audit

**(a) Reliance list (earlier gate PASS items relied on without re-checking structure):**
- Relied on the earlier Phase 6 numbers lens (`qa/qa-lens-numbers-metrics.md`) for the 10.6 brace-expansion match of 204 qa files at assembly. Only the group sums were re-added here.
- Relied on the anti-omission cycle-2 verifiers for the M1-M7 wording. Only their counts were checked here (290 recount; 36/7/0 path).

**(b) Independent semantic checks (my own tool work):**
- Recomputed every pair tally and per-option position from `ADV/debate-transcript.md:480-484`, and the vote vectors from :243, :277, :316, :356, :397, :438.
- Reconciled the monitor's 7 verdicts, 5 repairs and 5 reviewers against `05-session:18-21,491-501`, which showed that record 585 is the workflow write, not a verdict.
- Recounted the second CI merged verdict's severities directly (5 medium, 11 low) and read `REPORT.md:21`.
- Decoded `historical-review-rules.json` to confirm the captured rubric lines :65, :66-68, :79 and :82.
- Ran `stat`, `sha256sum` and `ls` on the cited artifacts (43, 45, 2,021,102, 72,087, 29,095, 1,222, 1,006 confirmed). This also re-observed L3 (original CI plan missing).
- Took a live package inventory (341 files) and current synthesis hashes, which produced N1 and N3.
- Diffed the report against synth-01/02/05/06 and grepped synth-04, which produced N4.
- Recomputed every gate-decision cycle and patch total against the task log and fix-log metadata, which produced N5 and N6.

**Why a reader can trust the coverage:** about 70 distinct quantitative claims were checked against primary files: case reports, deck, scope captures, debate artifacts, gate decisions, installed protocol files and external review artifacts. Every count family the brief named was covered: 30/6, 16 fixed/2 partial, 13/3 vs 14/2, 5/5, 3/5 and 2/5, line and hash counts, patch counts and timestamps. Unverifiable items are listed with their blocker rather than assumed.

**Web research:** none performed; no Tavily or fallback calls.

**Confidence:** Verified: 15/15 | Unverifiable: 0 at check level (4 sub-claims listed above) | Unchecked: 0 | Confidence: 100.0%. The verdict is FAIL because issues exist.

**Tool engagement:** Read: 21 | Grep: 0 (searches run through Bash grep/jq/diff) | Glob: 0 | Bash: 41

## QA Complete

**Verdict: FAIL.** Six issues (IMPORTANT 2: N4, N6; MINOR 4: N1, N2, N3, N5). None changes a rank, a ranked cause, a debate tally or an empirical count. J1, L1, L2 and L3 were excluded as known, user-accepted defects.

| Status | Result |
|---|---|
| DONE | Numbers and metrics lens on the Phase 6 final report, synth-01..06 and the three gate decisions; six issues recorded with evidence and required fixes. |
| NEXT | Team lead persists this text to `R/qa/qa-content-phase6-numbers-metrics-report.md` and consolidates N1-N6 with the other Phase 6 gate lenses. |