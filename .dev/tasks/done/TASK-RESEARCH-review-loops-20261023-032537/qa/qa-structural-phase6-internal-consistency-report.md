# QA Report: Phase 6 Gate, Internal Consistency

**Topic:** Phase 6 final-state internal consistency of the research report on repeated review failures (`/sc:workflow` plans and `/sc:implement` tasks)
**Date:** 2026-10-24
**Phase:** phase-gate (Task Phase 6, Steps 6.1-6.42)
**Lens:** Internal consistency (structural)
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Package root R:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Target identity:** `R/RESEARCH-REPORT-review-loops.md` has 1,316 lines and sha256 `41145b5e9660967e6f6498efb90da18bbfcd51eb3a81a0850fbdcde29fca40a0`. I re-measured both at the start, and they match the brief.
**Line-number note:** the brief's Git-disclosure anchors :8/:324/:904 are now :8/:327/:907. The J1 anchors :5/:1235/:1287 are now :5/:1241/:1293.

---

## Overall Verdict: FAIL

Verdict: FAIL

I found seven new consistency defects: one IMPORTANT and six MINOR. None of them changes a rank, a ranked cause or a tally. The ranks and the order V1 > V3 > V2 > V5 > V4 (non-consensus) are unchanged and agree everywhere I checked (:668, :680-684, :690-704, :1090, :1288).

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Report identity | PASS | `wc -l` = 1316; `sha256sum` prefix `41145b5e9660967e` matches the brief and `phase-outputs/plans/anti-omission-gate-decision.md:56`. |
| 2 | Table of contents resolves | PASS | A script slugged every heading: 61 TOC entries, 0 unresolved anchors, 0 duplicate slugs, 0 level-2/3 headings missing from the TOC. |
| 3 | Cause IDs, names and order agree across 6.0, Options A-E, the comparison table, 7.1-7.5 and 10.10 | PASS | Options A-E map to V1-V5 in card order (:489). Each Debate record row (:532, :559, :586, :613, :637) matches comparison row :654 and the 7.2 orders (:690-694). 7.1 holder counts (:680-684) match. |
| 4 | Section 7 tallies match the debate artifacts | PASS | `ADV/debate-transcript.md:477-484` gives the five orders verbatim. V3>V2 is 3 of 5, V4>V5 is 3 of 5, and V5>V4 (displayed) is 2 of 5, as stated at :701-704, :709, :1288. `refactor-plan.md:32-33` and `plan-review-evidence.md:16` support :709. Round 3 not run: `debate-transcript.md:449-450`. |
| 5 | Per-incident counts agree (2.1 table, 2.2, 2.6, Sections 3-4, 8 step 3.3, 10.2) | PASS | Report :129-134 matches `research/evidence-deck.md:151-156` row by row. Monitor 7 verdicts / 5 reviewers / 5 repairs agree at :133, :169, :278, :386, :1037. Orca 16 findings and 14 + 2 agree at :165, :255, :315, :553. CI 18 / 16 (5 medium + 11 low) agree at :136, :168. Seven synthetic exclusions agree at :106, :312 and deck :105. |
| 6 | Section 4 gaps, the 10.10 gap table, Section 8 steps and Section 9 questions | PASS | 12 gap rows (:346-357) match the 12 rows at :1272-1283 by exact name. Each mapped Section 8 step (2.1-2.6, 3.2-3.6) exists. 20 questions (:948-967) agree with the ":1290 none of the 20". |
| 7 | 7.6 orders, Section 8 steps and the replay table | PASS | :756 maps orders 1-4 to steps 2.1, 2.2-2.3, 2.4-2.5 and 2.6. Every replay row's "Used by" cell (:847-853) agrees. The step-3 read-only wording at :765, :843 agrees with :762. |
| 8 | Header, 10.1, 10.6 and 10.9 arithmetic | PASS | 258 = 23+10+191+17+9+4+4. 273 and 277 recomputed. 10.6 groups sum to 133 + 58 = 191, plus 13 = 204, plus 3 = 207. Header :6-7, :9 agree with :1007, :1214-1222. A live count gives research 23 and synthesis 11. |
| 9 | Git disclosure: :8, :327 and :907 agree with each other, with their QA anchors and with the task log | PASS (with L1/L2 known) | All three give the same step range, the same agents, "no mutation", the same blobs and trees, and the same acceptance entries (05:24Z, 06:32Z, 07:09Z; task file :703, :709, :727). All seven QA anchors at :8 resolve to Git-command records (for example `qa/qa-fix-verification.md:133`, `qa/qa-fix-log.md:31-32`). |
| 10 | Ranking-criterion disclosure | PASS | :88 and :719 quote `BUILD-REQUEST.md:12,34`, state the A-001 substitution and cite user acceptance at task-log 06:32Z (task file :709, F-02 "Disclosure only"). Nothing claims a likelihood ranking (grep "likel": only disclaimers). |
| 11 | Shared-install timing disclosure (P6-04) | PASS | The 20:29:54Z install and the non-independence of the credential and monitor evidence agree at :229, :583, :585, :586, :651, :738, :747 and Question 3 (:950). |
| 12 | Report and synthesis mirror claims in 10.10 | FAIL (N1) | The cycle-2 "same text" claims hold. Report :259 and :553 are verbatim in synth-01 and synth-04. The M2/M4 sentence of :580 is verbatim at `synth-04:109`. :953 is verbatim. The 6.39 recoveries are present in synth (13-phrase probe). The change history at :1293 is incomplete (N1). |
| 13 | Evidence Trail agrees with files the body cites | FAIL (N2) | A script listed every `qa/` and `phase-outputs/` path the report cites. 14 Phase 6 artifacts have no Evidence Trail row. |
| 14 | Status lines | Known J1 | :5 and :1241 still say report-gate cycle-2 verification is pending and that fidelity and anti-omission have not run. Known defect J1, not counted. |
| 15 | Gate-decision counts and verdicts agree with the cited QA reports | FAIL (N3, N4, N5) | The report-gate counts all match (31; 17 IMPORTANT / 14 MINOR; 181/15/4 patches; V-01..V-05; Q6-01..Q6-08; C2S, N1-N3, C3S, C3Q). The fidelity and anti-omission per-cycle counts match except for N4 and N5. Both halted gates have stale Status lines (N3). |
| 16 | Report agrees with `gaps-and-questions.md` | FAIL (N6) | The register records two Orca contradictions; the report treats three as unresolved. |
| 17 | Path-key scope | FAIL (N7) | `ADV/` is used outside its declared Sections 6-7. |
| 18 | Third Orca tension is carried consistently | PASS | Present at :259, :348, :408, :904, :953 and :1292. Not in the debated cards: `synthesis/hypothesis-03.md:60` names only the two other conflicts plus the CI boundary dispute. |
| 19 | Cited internal anchors resolve | PASS | Deck :900 lines, unchanged since 16:51Z (:1304). Card anchors `hypothesis-04.md:187` and `hypothesis-05.md:185` are correct (:1092). Phase 3 verifications are 7 PASS and 1 FAIL (:1136). Template lines 779, 1311 and 1393 exist (:479, :1302). `merged-root-cause-analysis.md:37-43` and `return-contract.md:14,16,24,26` support 7.2. |

## Summary

- Checks passed: 13 of 19 (plus 1 recorded as known J1). Checks failed: 5 (items 12, 13, 15, 16, 17).
- Critical issues: 0. Important: 1 (N1). Minor: 6 (N2-N7).
- Issues fixed in-place: 0 (report-only).
- Known, user-accepted defects found again and not counted as new: J1, L1, L2, L3 (see the table below).
- **Confidence:** Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 19 | Grep: 0 (searches ran inside Bash) | Glob: 0 | Bash: 41 (read-only `grep`, `sed`, `wc`, `stat`, `find`, `sha256sum`, and four read-only `uv run python` comparison scripts). No Git command was run, no session `.jsonl` log was opened, no file was edited, and no web research was done.

## Issues Found

| ID | Severity | Location path:line | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| N1 | IMPORTANT | `R/RESEARCH-REPORT-review-loops.md:1293`; `:1262` | The report's own change record skips three correction passes that changed the report and its mirrors, and its two change records contradict each other. :1293 goes 6.18, then report-gate cycle 2, "then" 6.39, then 6.42. It leaves out report-gate cycle 3, the fidelity fix at Step 6.29, and fidelity cycle 2. :1262 names the fidelity passes but leaves out report-gate cycle 2's change to synth-04 and the anti-omission changes to synth-01..06. Neither record says that Step 6.29 inserted two dated lines into `research/04-session-43582de1.md` and changed `gaps-and-questions.md`. | Report-gate cycle 3: "4 patches to the report" (`phase-outputs/plans/report-gate-decision.md:82`), and the report itself mentions "the cycle-3 fixer" (:8). Step 6.29: "42 patches over six files" (`fidelity-gate-decision.md:17`): report, synth-01, synth-02, synth-04, `gaps-and-questions.md`, `research/04` (task file :707). Fidelity cycle 2: "41 patches over five files" (`fidelity-gate-decision.md:67`; task file :701). `stat`: `research/04` 06:45:57Z, `gaps-and-questions.md` 11:34:50Z. | Make :1293 one complete chronology: 6.18, report-gate cycles 2 and 3, fidelity 6.29 and cycle 2, anti-omission 6.39 and cycle 2. For each pass, name the files it changed, including `research/04-session-43582de1.md` and `gaps-and-questions.md`. Make :1262 point to :1293 instead of keeping its own partial list. |
| N2 | MINOR | `R/RESEARCH-REPORT-review-loops.md:975-1262`, `:1291` | The Evidence Trail stops at the 03:51:27Z assembly inventory (277 files). Yet the body cites 14 Phase 6 artifacts that have no Evidence Trail row. The fidelity and anti-omission gate decisions are not referenced anywhere. The 10.10 row "Evidence trail lists every package file: Pass" is no longer true for the final state. Same cause as J1 (a snapshot inside the report), but a different element: an inventory, not a status line. | Cited without a 10.x row: `phase-outputs/plans/report-gate-decision.md` (:5), `qa/qa-consolidated-findings-phase6.md` (:5), `qa/qa-fix-log.md` (:5), `qa/qa-fix-log-cycle2.md` (:5), `qa/qa-fix-verification.md` (:8), `qa/qa-fix-verification-qualitative.md` (:8), `qa/qa-lens-internal-consistency.md` (:8), `qa/qa-lens-crossref-chain.md` (:8), `qa/qa-lens-domain-accuracy.md` (:8), `qa/qa-lens-implementation-concreteness.md` (:857), `qa/qa-fidelity-fix-log.md` and `-cycle2.md` (:1262), `qa/qa-anti-omission-fix-log.md` and `-cycle2.md` (:1293). Live count: 341 files (qa 266, phase-outputs 15). | Add a dated final-state subsection that lists the Phase 6 lens, fix, verification, fidelity and anti-omission artifacts and the three Phase 6 gate decisions. Mark :1291 as an assembly-time result. If the user chooses, fold this into the J1 decision. |
| N3 | MINOR | `R/phase-outputs/plans/report-gate-decision.md:5`; `R/phase-outputs/plans/fidelity-gate-decision.md:5` | Both Status lines still say "Task Blocked pending a user decision" and point to the Cycle 3 or Cycle 2 Record "at the end". Each file actually ends with a User-Authorized Advancement Record that unblocks the task and authorizes the next step. | `report-gate-decision.md:110-118` ("Halt overridden by explicit user authorization"); `fidelity-gate-decision.md:92-99` ("Cap halt overridden"); task file :717 and :697 ("Frontmatter back to Doing"). | Update each Status line: FAIL/HALT, then a user-authorized advance (not a PASS), task not blocked, final record = User-Authorized Advancement Record. |
| N4 | MINOR | `R/phase-outputs/plans/anti-omission-gate-decision.md:27` vs `:19` | The cycle-0 failure count says "36 (34 omissions + PF-01 + PF-02)". Line :19 lists PF-01..PF-03, and the consolidation addendum adds PF-03 as an IMPORTANT process finding. No reason is given for leaving PF-03 out. The number 36 also matches the consolidation's "36 unique omissions" (34 RECOVER + 2 DEDUP), which is a different composition. The strict shrink to 7 and then 0 holds either way. | `qa/qa-anti-omission-consolidated-findings.md:55-57` (36 = 34 RECOVER + 2 DEDUP), `:252` ("New process finding PF-03 (IMPORTANT)"). The 36 composition was copied from `qa/qa-anti-omission-verification-structural.md:104`. | State |F_0| with an explicit rule: either include PF-03 (37), or say why PF-03 is excluded (for example, resolved inside the consolidation). Distinguish it from the consolidation's 36 unique omissions. |
| N5 | MINOR | `R/phase-outputs/plans/fidelity-gate-decision.md:16` | The decision gives "70 frozen PASS identities" for `qa/qa-fidelity-consolidated-findings.md`, but that file states 84. The decision does not record that the structural verifier corrected 84 to 70. | `qa/qa-fidelity-consolidated-findings.md:60` ("frozen at cycle 0: 84 (P1 14, P2 12, P3 25, P4 7, cross-source 12 ...)", which sums to 70); `qa/qa-fidelity-verification-structural.md:109` ("Summary line says 84 ... does not match the list. Step 6.32 should use the 70"). | Append an attributed note: the consolidation's stated 84 is a miscount, its list holds 70, the source is the structural verifier :109, and the gate uses 70. |
| N6 | MINOR | `R/gaps-and-questions.md:29-35`, `:59`; vs `R/RESEARCH-REPORT-review-loops.md:259`, `:904`, `:953`, `:460` | The gap register's Unresolved Contradictions section has two Orca source contradictions, and :59 says "The two searchable source contradictions above remain". The report treats three Orca tensions as unresolved and calls the register a "Complete gap register, source contradictions" (:460). | `grep CONTRADICTION gaps-and-questions.md`: lines 33, 35 (Orca) and 69 (CI) only, with no annotated-tag `object.url` entry. The report's third tension is sourced to `research/01-session-ac2cd1fd.md:259,298` and deck :452. | Either add the third tension to the register as a dated, attributed addition (as was done at :69), or qualify :460 and Q6 to say the third tension comes from the case report, not the register. |
| N7 | MINOR | `R/RESEARCH-REPORT-review-loops.md:12` vs `:1288`, `:1307-1311` | The header limits the `ADV/` path key to Sections 6-7. Section 10.10 (:1288) and Section 10.11 (:1307-1311, moved from 7.8 at Step 6.18) also use `ADV/` paths, so they fall outside the declared scope. | `grep -n "ADV/"` outside lines 475-791 returns 12, 1288, 1307, 1308, 1309, 1311. | Change :12 to "Sections 6-7 and 10.10-10.11", or expand those paths to full `reviews/adversarial/adversarial/` form. |

### Known, user-accepted defects (recorded, not counted)

| ID | Where now | Observed state |
|---|---|---|
| J1 | Report :5, :1241 (formerly :1235). Former :1287 is now :1293. | :5 and :1241 still say report-gate cycle-2 verification is pending and that fidelity and anti-omission have not run, while :8, :1262 and :1293 record later passes. :1293 no longer says "pending"; its missing passes are N1, a different defect. |
| L1 | Report :8, :327, :907 | The disclosure lists three sets of Git reads. :907 says a search found no Git command outside Steps 6.3-6.20 except the Step 5.15 record. The Phase 3 case-gate reviewer reads and the Step 5.15 `git log -3` / `git status --porcelain` stay undisclosed. |
| L2 | Report :8 (third departure), :327, :907 | The case-06 tree use is still described narrowly. |
| L3 | Report :851 (formerly :848) | The CI replay row still says "Present; hashes re-checked" for the original CI plan. |
| J2 (user-resolved, for the record) | Report :8, :327, :907 | :327 and :907 state that the user accepted the 6.3-6.20 range. :8 cites only the 05:24Z (narrower) and 05:35Z (parent correction) entries, not the 05:48Z confirmation (task file :717) that the user said needs no fix. |

## Actions Taken

None. This review was report-only: I edited no file, ran no Git command and opened no session log.

## Recommendations

- Resolve N1-N7 before Phase 7, or record a user decision for each. N1 should be fixed rather than accepted, because Section 10.10 is the report's only record of which files changed during correction passes.
- N2 and N1 share J1's root cause. A single dated final-state Section 10 refresh, written after the last correction pass, would close N1, N2 and J1 together.
- Ranks, the order V1 > V3 > V2 > V5 > V4 (non-consensus), the cards, the variants and the debate artifacts need no change.

| Status | Result |
|---|---|
| DONE | Verified report identity, TOC, cause order, tallies, counts, cross-mappings, disclosures, mirror claims, the Evidence Trail, the three Phase 6 gate decisions against their QA reports, and the gap register, using tool evidence. |
| DONE | Found 7 new defects (1 IMPORTANT, 6 MINOR); recorded J1, L1, L2, L3 as known. |
| NEXT | Team lead consolidates with the other Phase 6 gate lenses and decides on one fixer pass or a user decision for N1-N7. |

## QA Complete