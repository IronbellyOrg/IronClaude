# QA Report: Phase 6 Anti-Omission Verification, Content

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks
**Date:** 2026-10-24
**Task step:** Step 6.41, Independent content omission verification (`TASK-RESEARCH-review-loops-20261023-032537.md:537-539`)
**Phase:** report-qualitative, anti-omission verification after fix cycle 1 of 2
**Fix authorization:** false. This verifier edited no file, ran no Git command and opened no session `.jsonl` log.
**Report under review:** `RESEARCH-REPORT-review-loops.md`, 1,316 lines. I measured sha256 `37753a81e7a797b770edb807e15d9bcf5d0609943c5b8f8911c8a14dcc761797`, which matches the fix log's after-hash. I read all 1,316 lines.
**Path convention:** paths are relative to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. "Report:N" means line N of the final report.
**Templates read:** `/config/.claude/skills/tech-research/SKILL.md:1196-1239` (anti-omission prompt and output format) and `/config/.claude/skills/task/SKILL.md:466-506` (standard QA report format).

## Overall Verdict

Verdict: FAIL

The restoration is mostly faithful, but three of the 34 recovered points either distort their source or break the line between debated and undebated evidence. There are 4 issues: 2 IMPORTANT and 2 MINOR.
- **F-01 (recovery O-05):** the report credits the historical targeted reviewer with a classification that the case analyst made.
- **F-02 (recovery O-30):** case detail the debate never weighed was added to the Option C Support row without a label, and the fix log called it debated content.
- **F-03 (recovery O-30):** the unused `vhex()` helper is called "cosmetic output", but the source classes it as a preexisting extra.
- **F-04 (recovery O-25):** the source's limit on this introduced gap was dropped inside a ranking support row.

None of these changes the ranking. Ranks, tallies and the three disclosures all still hold.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Required inputs read | PASS | Read Step 6.41 (task file :537-539); both templates; `qa/qa-anti-omission-consolidated-findings.md` in full (1-305, including the addendum at 229-304); `qa/qa-anti-omission-fix-log.md` in full (1-247); the full report. Source lines were re-read for every recovered point (rows 3-8). |
| 2 | Report and mirror identity | PASS | Report sha256 is `37753a81…` with 1,316 lines. All six synth-0N hashes equal the fix log's after-hashes (`qa/qa-anti-omission-fix-log.md:125-130`): `5268a163`, `5da15419`, `b0a561a5`, `9487ceac`, `994f3502`, `d94f089e`. |
| 3 | O-01, O-02 and O-03 rubric clauses match the captured texts | PASS | I decoded `research/historical-review-rules.json` with jq. The earlier text (`0b533765…`, 20:26:30.085Z) says at :79 "Missing, stale or unverifiable evidence is `issues`" and at :65 "The executor MUST NOT write the Ruling line", requiring an operator-supplied ruling. The later text (`faff03b7…`, 20:32:19.277Z) at :82 takes evidence from current files and `./artifacts/` logs, says "a moved line number alone is never `issues`" and checks recorded scoped acceptance; at :66-68 the executor records the Ruling after clear user confirmation. Clause counts, earlier/later: "One reviewer per review" 0/1, `E-RESUME` 0/1, "troubleshoot" 0/1, "retries" 0/2, "revert" 0/1, "stale" 1/0, "moved line" 0/1. Earlier :83 says "One mode for the rest of the run"; later :86 makes A3-A5, re-run and operator reviews subagents; later :61 ties `E-HALT-QA` to the ladder's terminal halt; later :63 broadens `E-NO-RULING`. `research/scope-rules.md:70-71` ties the earlier load to the second FINAL and the later load to the third FINAL. Report:231, :580, :612 and :896 state all of this correctly. |
| 4 | O-05 conveys its source meaning | FAIL | F-01. Report:259 says "The targeted reviewer classed the resulting finding as preexisting". In the source, that classification sits in the case analyst's "Historical classification" column (`research/01-session-ac2cd1fd.md:255,259`). The deck repeats it as an analyst matrix row (`research/evidence-deck.md:452`). The other O-05 content is correct: Source:158 against Source:469, Session:912, and no separate verification (`01-session-ac2cd1fd.md:259,298`). |
| 5 | O-23 conveys its source meaning | PASS | `01-session-ac2cd1fd.md:208` says the field-9 change was introduced, "with the qualification that provenance could be a better engineering source if explicitly approved". :299 lists Requirements:302's recipe-state definition as a source tension. `evidence-deck.md:431` says "no such change was declared". Report:553 and :347 match, and Report:553 labels it "not weighed in the debate". |
| 6 | O-25 conveys its source meaning | FAIL | F-04. Report:553 omits the source's limit: "a known local-failure comparison also existed in v2 constraints" (`01-session-ac2cd1fd.md:222`) and "Earlier local failure comparison also existed; no execution claimed" (`evidence-deck.md:446`). |
| 7 | O-30 conveys its source meaning and stays within the debated content | FAIL | F-02 and F-03. Of the details added to Report:580, only "any defect of any severity", the uncapped fields and case-insensitive matching appear in the debated card (`reviews/adversarial/adversarial/variant-3-original.md:28`). I searched all five variants and found 0 hits each for "rename", "suggested", "cosmetic", "vhex", "punctuation", "grammar", "bullet" and "exactness". `05-session-e002bed2.md:132` classes `vhex()` as "Preexisting extra". The 2.6 copy at Report:278 is correct and sits outside the ranking. |
| 8 | The other 28 recoveries convey their source meaning | PASS | Each was checked against its live source lines. O-04: `scope-03-recovered.md:71-75,131`; `06-session-0690ee9f.md:301`. O-06: `research-notes.md:30`. O-07: `input-inventory.md:45,79`. O-09: `scope-01-recovered.md:58,62`; `05-session-e002bed2.md` has 0 hits for "scratch" or "20:45:36", and both sessions use the orca-upstream-tracking project. O-10 to O-13: `screening-handoffs-source.txt:69,94,112-120,133,156,163,182-186,372-378`; `scope-02.md:17-18,28`. O-15 to O-19: `scope-03-recovered.md:39-43,104,156-162,171,180`. O-20 to O-22: `scope-rules.md:32,41`, plus the later rubric :27-52. O-24: `01-session-ac2cd1fd.md:290`. O-26: `03-session-6f744b87.md:104,142`. O-27 to O-29: `04-session-43582de1.md:256,351,354,524-525,547-559`; deck :501, :507, :510. O-31 to O-33: `05-session-e002bed2.md:131,166-171,294,413-449`; deck :545-548. O-34 and O-35: `06-session-0690ee9f.md:76,299-301`. O-36: `hypothesis-01.md:142` and `variant-1-original.md:42`. |
| 9 | O-08 and O-14 deduplication still holds | PASS | The exclusion of historical producer recovery errors now sits at Report:282 (the old :279, shifted by the three inserted lines). The sources are still listed in 10.2 and 10.3. `scope-03-recovered.md:176` says "no unresolved source-access blocker remains". |
| 10 | Undebated O-04, O-05, O-25, O-28 and O-29 stay out of the ranking basis and are labelled | PASS | O-04 appears only at Report:170 and :279. O-05 appears in 2.5, Gap row 3, 5.1, Section 8, Q6 and 10.10, each with "not in the debated cards", and it is absent from Option C Support (Report:580 names only source.md :142, 285, 382 and 402). O-25 is labelled at Report:553 ("the debate never weighed"). O-28 and O-29 appear only in the 2.2 CI row (Report:168) and are labelled. |
| 11 | Five hypotheses, ranking and counterevidence still coherent | PASS | Options A-E (Report:513-644) keep their mechanism, support, opposition, alternatives, scope, falsification and limits. The order "V1 > V3 > V2 > V5 > V4" stands at Report:668. Report:680-684 and :698-705 give V1 first 5 of 5, V3 above V2 3 of 5, V4 above V5 3 of 5, and the displayed V5 above V4 on the 2-of-5 side. The Options Comparison ranks are unchanged (Report:654), and the 10.10 tally text at Report:1288 still matches. |
| 12 | No restored condition weakens a validity judgment or creates a new contradiction | PASS | Every place the report counts Orca tensions now says three, or carries a dated update note: Report:259, :348, :408, :904, :953 and :1292. O-16 (Report:181) says no link to the credential rubric change is established, which is consistent with the unknown installer at Report:229. O-01 and O-02 sharpen the confounding and do not resolve it (Report:231, :585, :951). The new invented attribution in F-01 is counted under row 4. |
| 13 | Git, ranking-criterion and shared-install (P6-04) disclosures still hold | PASS | Git: Report:8, :327 and :907 are unchanged. Ranking criterion (likelihood requested, explanatory support delivered, user accepted at 06:32Z): Report:88 and :719. Shared 20:29:54Z install: Report:583, :585, :586, :651 and :738. |
| 14 | Earlier substantive PASS criteria still true | PASS | 10.10 checks (Report:1287-1293): options cite Section 2, the ranking traces the debate, Section 8 is research-only, no open question is answered elsewhere (Q3, Q4, Q6 and Q10 stay open after O-01, O-02, O-05, O-16 and O-32), and 10.10 records the Step 6.39 change. Known defects J1, L1, L2 and L3 were not assessed, as instructed. |
| 15 | Matching component copies apply the same text | PASS | The hashes match (row 2). The same defects are present in the copies: `synthesis/synth-01-problem-current-state.md:164` (F-01) and `synthesis/synth-04-options-recommendation.md:82,109` (F-04, F-02 and F-03). |

## Summary

- Checks passed: 12 of 15. Checks failed: 3 (rows 4, 6 and 7).
- Issues: CRITICAL 0, IMPORTANT 2 (F-01, F-02), MINOR 2 (F-03, F-04). Issues fixed in place: 0 (report-only).
- Recoveries assessed: 34. Faithful: 31. Defective: 3 (O-05, O-25 and O-30). DEDUP O-08 and O-14: confirmed.
- Ranking, tallies and disclosures: unchanged and intact.
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 0 (searches ran through Bash grep and jq) | Glob: 0 | Bash: 17. No web research was needed, so neither Tavily nor the fallback search tools were used.

## Issues Found

| ID | Severity | Location path:line | Issue | Primary evidence | Required fix |
|---|---|---|---|---|---|
| F-01 | IMPORTANT | `RESEARCH-REPORT-review-loops.md:259`; mirror `synthesis/synth-01-problem-current-state.md:164` | The O-05 row says "The targeted reviewer classed the resulting finding as preexisting and inherited from the source, not a v3 regression." The source does not support that attribution. The classification is the case analyst's adjudication, not something the historical reviewer said. This invents a historical actor's position in a report whose core distinction is between reviewer claims and analyst adjudication. | `research/01-session-ac2cd1fd.md:255`: the column is headed "Historical classification". Analyst voice in sibling rows: :258 "This is a plan-level injection risk, not an observed exploit"; :261 "missing mutation does not prove…". The same term is used for analyst classification at `evidence-deck.md:559` and `04-session-43582de1.md:614`. Deck :452 records it as an analyst matrix row. | In both files, replace the sentence with: "The case analysis classes the resulting finding as preexisting and inherited from the source, not a v3 regression (`research/01-session-ac2cd1fd.md:259`)." |
| F-02 | IMPORTANT | `RESEARCH-REPORT-review-loops.md:580` (Option C Support), second sentence of the R32 addition; mirror `synthesis/synth-04-options-recommendation.md:109` | A ranking support row for V3 (rank 2) now carries undebated case detail with no label: reviewers told to judge every bullet directly, exactness problems in suggested commands (the `git diff --name-only` rename overlap), and the unused helper, punctuation and grammar. The fix log calls all of O-30 "Debated content" (`qa/qa-anti-omission-fix-log.md:89`). The consolidation's condition says adding undebated evidence to a candidate's support is a user decision (`qa/qa-anti-omission-consolidated-findings.md:218`). O-23 and O-25 were labelled in Option B, but this addition was not. | The debated card's text is limited to uncapped fields, case-insensitive matching and "any defect of any severity" (`reviews/adversarial/adversarial/variant-3-original.md:28`; `synthesis/hypothesis-03.md:59`). All five variants have 0 hits for "rename", "suggested", "cosmetic", "vhex", "punctuation", "grammar", "bullet" and "exactness". | Option C Support should keep only the debated clauses: case-insensitive matching, and "the per-review prompts made any defect of any severity noncompliant". Remove the rest of that sentence; it is already represented outside the ranking at Report:278. The alternative is to keep it and prefix it with "Case-report detail the debate never weighed:". |
| F-03 | MINOR | `RESEARCH-REPORT-review-loops.md:580`; mirror `synthesis/synth-04-options-recommendation.md:109` | "cosmetic output (the unused `vhex()` helper, punctuation and grammar)" mislabels the helper. The source classes it as a preexisting extra (unasked code), not cosmetic output. | `research/05-session-e002bed2.md:132`: "Unused `vhex()` helper. **Preexisting extra.**" The cosmetics row is :146 (trailing blank quote, grammar, punctuation). `evidence-deck.md:534` reads "Preexisting extra/output defect". | If F-02 is fixed by removal, this text goes with it. Otherwise write: "an unused helper kept from the original (a preexisting extra) and cosmetic output (punctuation and grammar)". |
| F-04 | MINOR | `RESEARCH-REPORT-review-loops.md:553` (Option B Support, O-25 sentence); mirror `synthesis/synth-04-options-recommendation.md:82` | The recovered N-17 sentence states the introduced gap without its source limit. In a V2 support row, that slightly overstates the introduction evidence. | `research/01-session-ac2cd1fd.md:222`: "a known local-failure comparison also existed in v2 constraints". `evidence-deck.md:446`: "Earlier local failure comparison also existed; no execution claimed." | Append to the sentence: "; an earlier local-failure comparison already existed in the v2 constraints, and no execution is claimed". |

## PASS/FAIL Set History

| Cycle | PASS set | FAIL set | Failure count |
|---|---|---|---|
| 0 (Step 6.38 consolidation and addendum) | P1: 154 represented + 51 dedup. P2: 225 represented + 56 dedup. P4: 383 represented + 20 dedup, including all five hypotheses and the debate tallies. P3 rerun: 290 items, with 9 dispositions overturned. | 34 omissions to recover: O-01 to O-36 except O-08 and O-14. Process findings PF-01, PF-02 and PF-03. | 34 omissions |
| 1 (Step 6.39 applied; this verification) | 31 recoveries: O-01, O-02, O-03, O-04, O-06, O-07, O-09, O-10, O-11, O-12, O-13, O-15, O-16, O-17, O-18, O-19, O-20, O-21, O-22, O-23, O-24, O-26, O-27, O-28, O-29, O-31, O-32, O-33, O-34, O-35, O-36. Dedup O-08 and O-14 confirmed. The cycle-0 PASS items checked here still pass: ranking, tallies, the three disclosures and the 10.10 checks. | O-05 (F-01), O-25 (F-04), O-30 (F-02, F-03) | 4 issues across 3 IDs |

**Regression check:** no item that passed in cycle 0 fails in cycle 1. All four issues were introduced by the recovery text. The failure count fell from 34 to 4, so the monotonicity halt does not trigger.

## Actions Taken

None. This is a report-only verification. No package file was edited, no Git command was run and no session `.jsonl` log was opened.

## Recommendations

- Run anti-omission fix cycle 2 of 2: one fixer applies the F-01 to F-04 changes above to the report and its mirrors (`synthesis/synth-01-problem-current-state.md:164`; `synthesis/synth-04-options-recommendation.md:82,109`).
- After that, fresh Step 6.40 and 6.41 verifiers should recheck only these three IDs and confirm that the ranking and disclosures stay unchanged.

## Self-Audit

**(a) Reliance list: rf-qa PASS items I did not structurally re-check**
- Relied on the fix log's statement that each patch's "before" text matched exactly once. In place of a structural re-check, I confirmed every after-hash on disk.
- Relied on the Step 6.40 structural verifier for enumeration and count reconciliation across partitions.

**(b) Independent semantic checks**
- Rubric clause content: decoded both captured texts with jq and compared earlier :65, :79, :83 with later :61-68, :82, :86, :90 (row 3).
- Who made the O-05 classification: read the column header at `01-session-ac2cd1fd.md:255` and how "historical classification" is used at deck :559 and `04-session-43582de1.md:614` (F-01).
- Debated versus undebated boundary: searched all five `variant-N-original.md` files for 23 terms from the recovered text (F-02, row 10).
- Source qualifiers: compared each recovered sentence with its source's limit column (`evidence-deck.md:431,446,452,501,507,510,534,545-548`), which found F-03 and F-04.

## QA Complete

| Status | Result |
|---|---|
| DONE | Read the consolidation, addendum, fix log, governing templates, the full 1,316-line report and every cited source line for the 34 recoveries. Confirmed the report and mirror hashes. |
| DONE | Verified the O-01, O-02 and O-03 clauses against the decoded captured rubrics; ranks, tallies and disclosures are intact; no other residual "two tensions" wording remains. |
| DONE | Verdict FAIL: F-01 (invented reviewer attribution) and F-02 (undebated detail in Option C Support) are IMPORTANT; F-03 and F-04 are MINOR. |
| NEXT | Anti-omission fix cycle 2: one fixer applies the F-01 to F-04 changes to the report and mirrors, then fresh Step 6.40 and 6.41 verifiers recheck. |