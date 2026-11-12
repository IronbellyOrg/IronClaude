# QA Report — Synthesis Fix Verification (Qualitative, fix cycle 1)

**Topic:** Orchestrator mode Phase 1 (issue #339), synthesis gate re-check
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 1
**Fix authorization:** false (report only; no synthesis file edited)

**Inputs read:** `qa/qa-consolidated-findings-phase5.md` (B-01 to B-15), `qa/qa-synthesis-fix-log.md`, `synthesis/synth-01` to `synth-06` (all lines, read in chunks of at most 120 lines).

**Scope of re-check:** every finding sourced from the qualitative reports (qu-1, qu-2): B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-11, B-12, B-13, B-14, B-15. B-08, B-09, B-10 (non-qualitative sources) were also spot-checked for cross-file contradictions. Extra edits checked: S5 step 1.5 (B-12 spill-over), S6 rows 33a and 98a.

---

## Overall Verdict: FAIL

Two blocking findings remain open: one new contradiction that the B-14 fix created (N-1), and an incomplete B-13 fix (N-2). Details below.

## Original findings, re-checked

| ID | Source | Result | Evidence (re-read this cycle) |
|---|---|---|---|
| B-01 | qu-1 #1 | RESOLVED | S1 `:201` reads Open 75 / Resolved 25, "Open blocking QA finding: none", matching `gaps-and-questions.md:125`. |
| B-02 | qu-2 I-1 | RESOLVED | S4 `:220` X-6 is "Resolved, not a live conflict ... 75 / 25", effect "None on the option choice". "Off by one" is gone. |
| B-03 | qu-2 I-1 | RESOLVED | S5 X-6 is now resolved, coverage row cites `:125` (75/25), and C2 `:172` is labelled a line-count note. Matches S2 `:241` (C2 = 1202 lines). |
| B-04 | qu-2 I-2 | RESOLVED | S6 row 17 and S5 1.4 `:62` both keep `--include-remote` in the default argv, add a measured-cost acceptance, and leave GQ-22 open. Residual MINOR note M-1 below. |
| B-05 | qu-2 I-3 | RESOLVED | S6 row 58 now matches S5 1.3 `:61` (GQ-84): exited, no `worker_done`, unreadable transcript give could not determine. WC-10 holds. |
| B-06 | qu-2 I-4, M-3 | RESOLVED | S5 1.17, 8.1 G7, GQ-11 and GQ-29..35 rows, OQ-11 `:223` and S6 rows 8, 9, 30 and 51 mark GQ-10, GQ-11, GQ-35 and GQ-61 as owner decisions with working defaults. Residual MINOR note M-2 below. |
| B-07 | qu-2 I-5 | RESOLVED | S6 row 33 is now GQ-38 paging only. The new row 33a (`:62`) is GQ-48 with the S5 1.5 string. No contradiction with S5 `:63`. String differs from `gaps:71` (MINOR, note 2 in the consolidated findings, not rechecked). |
| B-11 | qu-1 #2 | RESOLVED | S2 R-2 `:172` names G1, G2 and G5 only, states that R-2 wins over R-1 for its rows, and excludes G7 with a reason (GQ-10). G2 `:182` and G5 `:185` are "Critical (R-2, unwired; source severity Important, N-32)". G7 `:187` is "Important (N-32; R-1, outside R-2's list)". G1 `:181` Critical. The table now follows the stated rule consistently. |
| B-12 | qu-1 #3 | RESOLVED | S3 R4 `:216` limits the exclusion to activity ages and the 6 h window, and says the waiting list prints and sorts on the question's original age. R7 `:219` sorts by time since the wait began. S2 `:90` and `:152`, S5 1.5 `:63` and S4 `:242` use the same wording. No residual conflict. |
| B-13 | qu-1 #4 | **OPEN (partial)** | S3 `:183` now names Grafana (D5), agents-fleet (D6) and, in part, the Nagios KB (D2) as contradicting WC-10. It still says "three external sources contradict WC-10, and all three are rejected" and that the remaining sources support WC-10. That count omits D1, which is in the same file: S3 `:81` says Kubernetes taint and eviction after `Unknown` is "what WC-10 forbids", and D1 `:169` cites WC-10 as the conflicting rule and rejects the pattern. S2 4.8 `:290` also lists Kubernetes (D1, D4) and Harmonograf (D3) as acting on a timeout against WC-10. See N-2. |
| B-14 | qu-1 #5, qu-2 M-1 | **OPEN (partial)** | Done: OQ-13 `:225` in S5 8.2, row 98a (`:145`) in S6, X-7 marked as the working default, and the headers S1 `:5`, S3 `:7`, S4 `:3` and S6 `:3` say "the research question's six" with fenced as Section C's seventh. Not done: S5 `:10`, the row labelled "Research question", still lists seven classes including fenced with no attribution. The fix chose the "mark them as the research question's six" option, so S5 `:10` is now the only place that says the research question has seven. See N-1. |
| B-15 | qu-2 M-3 | RESOLVED | S6 rows 27 and 28 now say: print the worktree-tree root as the scope line, and list everything (shown equals total) with the 100-row truncation form. Both are marked as open plan decisions, which matches S5 1.5 `:63` (GQ-32, GQ-33) and `gaps:55-56`. |
| B-08 | non-qualitative (spot check) | RESOLVED | S6 rows 36 and 49 have no version probe and no header field promise. GQ-41 and GQ-59 stay open, which matches `gaps:64`, `:82`. |
| B-09 | non-qualitative (spot check) | RESOLVED | S5 1.19 `:92` and S6 row 10 use `/sc:sweep`. |
| B-10 | non-qualitative (spot check) | RESOLVED | The S5 `:12` header is narrowed, and rule (2) in 1.3 `:61` is built against synthetic `exited` fixtures. Residual MINOR note M-3 below. |

Of the 15 findings, 13 are RESOLVED and 2 are OPEN (B-13 and B-14).

## New blocking findings

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| N-1 | IMPORTANT (contradiction; introduced by the B-14 fix) | `synthesis/synth-05-implementation-plan.md:10` ("Research question" row); conflicts with S5 OQ-13 `:225`, S1 `:5`, S3 `:7`, S4 `:3`, S6 `:3`, S6 row 98a `:145`, S2 4.8 `:284`, and the task file GOAL (`:54`, `:90`, six classes) | S5 `:10` says the research question classifies sessions into seven classes, including fenced. S5 `:225`, in the same file, says "the research question lists six". All other headers now say the same thing as `:225`. Before the fix, `:10` was the reference the other headers were asked to match. The fix marked the other headers as six instead, so `:10` is now the outlier. | Reword S5 `:10` to match the others: "(waiting on a person, working, stalled (proved), finished, could not determine, idle: the research question's six; Section C adds fenced as a seventh, the working default, OQ-13)". Optional, same pass: S1 `:15` "The question." lists seven and attributes the names to Section C. Give it the same wording so Section 1 does not open with a different class list than its header (see M-4). |
| N-2 | IMPORTANT (wrong claim, same file; B-13 incomplete) | `synthesis/synth-03-external-findings.md:183`; conflicts with S3 `:81`, D1 `:169`, and S2 4.8 `:290` | The line says "three external sources contradict WC-10, and all three are rejected" and names Grafana, agents-fleet and Nagios. D1 (Kubernetes taint and eviction after `Unknown`) is a fourth. S3 `:81` says that step "is what WC-10 forbids", and D1 lists WC-10 as the conflicting codebase rule. S2 `:290` also counts Kubernetes (D1, D4) and Harmonograf (D3) against WC-10. The count is wrong, and S3 and S2 disagree on which external sources contradict WC-10. | Change the count and name D1: "four external patterns contradict WC-10 and are rejected: Grafana's missing-data mapping (D5), the agents-fleet auto-abort (D6), Kubernetes taint and eviction after `Unknown` (D1), and, in part, the Nagios KB timeout guidance (D2). Harmonograf's 'stuck' label (D3) and the liveness-probe restart (D4) are rejected as actions or naming, not as contradictions of absence-is-not-death." Keep "Kubernetes node status at the status layer" in the supporting list. Or align S2 `:290` with whichever reading is chosen. |

## Global checks requested by the executor

| Check | Result | Evidence |
|---|---|---|
| No fix introduced a contradiction between synthesis files | **FAIL** | N-1 (S5 `:10` against S5 `:225` and every other header). N-2 is within S3 and between S3 and S2; it is partly left over from before the fix and partly introduced by the fix's new "three" count. |
| Section 8 plans the option Section 7 recommends | PASS | S4 `:191` "Recommended option: A1". S5 `:6`, `:16`, steps 1.1 to 1.19 build `superclaude sweep` + `/sc:sweep` + `sc-sweep-protocol`. S2 `:16`, `:183` agree. |
| WC-10 is not broken | PASS | S5 1.3 `:61`: `unverifiable`, late heartbeat, stale status and a missing row give could not determine, never stalled. Rule 2 requires positive proof. GQ-84 sends an unreadable transcript to could not determine. S6 row 58 matches. S2 `:59`, `:289`; S3 R2, R5 `:214`, `:217`. |
| A4 is not recommended | PASS | S4 `:150` "REJECTED, [CODE-CONTRADICTED]"; S5 `:18`; S2 `:144`, `:257`; S3 `:185`; S6 row 50 "A4 rejected". |
| Later phases are recorded, not designed | PASS | S5 `:116-124` gives one line each. S2 `:143`, `:172`. S3 L1 and L2 `:227-228` are one-line "if ever added" guards, not designs. S4 `:201` mentions reuse only. |
| Extra edit S5 1.5 (B-12 wording) | PASS | `:63` "person-wait time is excluded from activity ages and the activity window, while the waiting list prints and sorts on time since the wait began". Same wording as S3 R4 and S2 `:90`, `:152`. |
| Extra edit S6 row 33a | PASS | `:62` truncation string identical to S5 1.5 `:63` and S2 `:91`. |
| Extra edit S6 row 98a | PASS | `:145` matches S5 OQ-13 `:225` (working default seven, owner decision) and S2 4.8 `:284`. |

## MINOR notes (not blocking; not rechecked in later rounds)

| # | Location | Note |
|---|---|---|
| M-1 | S1 `:294` against S5 1.4 `:62`, S6 row 17 | S1 lists "remote rows read unverifiable without `--include-remote`" as a guide-only statement kept out of the current state. S5 and S6 now state it as fact, citing `05:163`, which is itself sourced from the guide (`[G:recovery] 47-49`). Tag it "(guide text)" in S5 and S6. |
| M-2 | S5 `:53`, 1.5 `:63` ("pinned to `495eb96d`"), 1.6 and 1.17 ("under `.dev/`"); S2 `:71`; S5 8.1 sub-table `:193-207` | These still state the GQ-35 pin and the GQ-10 directory without the "working default" label that OQ-11 now gives them. The 8.1 "Gaps sent to Open Questions" sub-table also omits GQ-10, GQ-11 and GQ-35. OQ-11 `:223` covers them, so this is wording only. |
| M-3 | S5 1.3 `:61` | "the live-capture check stays in Open Questions, 8.2". GQ-37 is not in 8.2 (OQ-1 to OQ-13). It is in the 8.1 sub-table at `:195`. The pointer should be "8.1". |
| M-4 | S1 `:15` | "The question." lists seven classes, while S1's own header `:5` says the question lists six. It attributes the names to Section C, so it is not a hidden contradiction. Fold it into the N-1 fix. |
| M-5 | S4 `:215` X-1 against S2 `:32` | S4 says A1's git list allows `stash list`. S2's data-source table lists only status, log, branch and rev-parse. S5 1.4 `:62` includes `stash list`. This predates the fixes. Align S2 `:32`. |
| M-6 | S2 `:172` | R-2 makes "WC-14 and its clauses" Critical, but the WC-14 rule id is itself an owner decision (GQ-11, working default). The clauses stand whatever the id is, so this is wording only. |
| M-7 | S4 `:3` | S4 points to "Section 9", but its own open-questions table has no six-versus-seven row. That is acceptable because Section 9 is the assembled report's Open Questions (S6 row 98a). |

## Items that PASS

- **Original findings resolved (13):** B-01, B-02, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-12, B-15.
- **Global checks passed (7 of 8):** Section 8 plans A1 as Section 7 recommends; WC-10 holds; A4 only rejected; later phases recorded only; S5 1.5 extra edit; S6 row 33a; S6 row 98a.
- **Not passing:** B-13 (N-2), B-14 (N-1), and the global check "no fix introduced a cross-file contradiction" (N-1).

## Summary

- Checks passed: 20 / 23 (15 original findings + 8 global checks)
- Checks failed: 3 (B-13, B-14, the no-new-contradiction check)
- Critical issues: 0. Important (blocking): 2 (N-1, N-2). Minor notes: 7.
- Issues fixed in-place: 0 (fix authorization false)
- Count against the previous cycle: 15 blocking findings, now 2. The count went down; no systemic regression.

## Confidence

- **Confidence:** Verified: 23/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 4 | Glob: 0 | Bash: 1. These counts cover this segment of the review only. The earlier segment, before a context compaction, also read the consolidated findings, the fix log, all of S1, S5 and S6, the task file GOAL lines, `gaps-and-questions.md`, `research/05-orca-row-schema.md:160-166` and `research/research-notes.md:186-202`; its counts were not recorded exactly. Total tool calls are above the 23-item minimum.
- No web research was done. Tavily was not needed; all checks were local.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was provided in the spawn prompt, so this review ran standalone. Nothing was relied on. Fix-log claims were treated as claims and re-read against the synthesis files.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- The six-versus-seven class list across all six synthesis files. Verified by Read of S5 `:8-12` and `:223-225`, S1 `:5-15`, S3 `:1-20`, S4 `:1-12`, and Grep of S6 for `98a|seventh`. Found N-1.
- The external sources that contradict WC-10. Verified by Read of S3 `:74-83` and `:160-231`, Grep of S3 `Relationship:` lines, and Read of S2 `:140-160` and `:280-291`. Found N-2.
- R-1 against R-2 severity consistency. Verified by Read of S2 `:167-190`. B-11 confirmed resolved.
- The waiting-list sort age. Verified across S3 R4 and R7 `:216`, `:219`, S2 `:90`, `:152`, S5 `:63` and S4 `:242`. B-12 confirmed resolved.
- Option and recommendation alignment. Verified by Read of S4 `:189-262` against S5 `:6-18`.

**Self-audit questions:**
1. Claims checked independently: 23 checklist items, plus about 40 line-level citations re-read in the synthesis, gaps and research files.
2. Files read: the six synthesis files, `qa-consolidated-findings-phase5.md`, `qa-synthesis-fix-log.md`, `gaps-and-questions.md`, `research/research-notes.md`, `research/05-orca-row-schema.md`, and the task file.
3. The review found issues: 2 blocking and 7 minor.
4. No web research was done.

## Recommendations

1. Fix N-1: reword S5 `:10`, and S1 `:15` in the same pass, so the research question is described as six classes, with fenced as the Section C working default (OQ-13).
2. Fix N-2: correct the S3 `:183` count to include D1, and make S2 4.8 `:290` use the same grouping.
3. Re-run the synthesis gate. This was fix cycle 1 of a maximum of 2.

## QA Complete

## Verdict: FAIL
