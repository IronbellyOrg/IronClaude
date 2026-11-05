# QA Report: Phase 6 Final Report Consolidation

**Topic:** Phase 6 final-report lens gate (Task Steps 6.2-6.16). This report consolidates the eleven applicable lens reviews of `RESEARCH-REPORT-review-loops.md`.
**Date:** 2026-10-24
**Phase:** report-validation, Task Step 6.17
**Lens:** Cross-lens findings consolidation
**Fix cycle:** 0. This is the frozen baseline before any correction.
**Fix authorization:** false. Nothing was fixed.
**Governing format:**
- Task Standard QA Report Output Format (`/config/.claude/skills/task/SKILL.md:466-506`).
- Consolidation rules from the Serialized Fix Protocol step 2 (`task/SKILL.md:357`): deduplicate, keep every originating lens, keep the highest severity, filter by scope.
- Tech-research Phase 6 consolidation (`/config/.claude/skills/tech-research/SKILL.md:544-551`): each finding has a description, source lens, severity, affected section and proposed fix.
- Lens template (`tech-research/SKILL.md:1042-1151`).
**Intended output:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-consolidated-findings-phase6.md`

**Delivery limitation:** My higher-priority instructions do not allow me to write report files. I created no stub and no file. This text is the complete report for the parent to save. It does not claim that the target file exists. At consolidation time, `ls` returned "No such file or directory" for both `qa/qa-consolidated-findings-phase6.md` and `qa/qa-fix-log.md`.

**Path conventions:**
- Relative paths resolve under `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`.
- "Report" means `RESEARCH-REPORT-review-loops.md`. "Report:N" is its line N, read in full this session (lines 1-1263).
- `ADV/` means `reviews/adversarial/adversarial/`.
- "Checkout" means `/config/workspace/IronClaude/src/superclaude/skills/`. "Installed" means `/config/.claude/skills/`.

---

## Overall Verdict: FAIL

- **Literal verdicts:** all eleven applicable reviewers returned FAIL. I confirmed each verdict line independently (see the inventory below). None returned PASS.
- **Unique issues after deduplication:** 31. By severity: CRITICAL 0, IMPORTANT 17, MINOR 14. Every one stays in the failure set.
- **Raw input:** 53 reviewer-counted issues (24 IMPORTANT, 29 MINOR, 0 CRITICAL).
  - All 53 were checked against the report and against primary sources.
  - None was unsupported as a whole, so none was dropped.
  - None was downgraded.
  - Nine sub-claims were qualified or corrected after verification (see "Claims adjusted after verification").
- **Rank-sensitive items flagged:**
  - P6-04 bears on the evidence behind the V3 placement.
  - P6-03 and P6-16 touch Option C or Opposition support text.
  - No proposed fix changes a rank, the displayed order V1 > V3 > V2 > V5 > V4, card causal text, the variants, the debate artifacts or the historical sources. Where a fix could be applied in a way that would, the constraint is stated on that row.
- **What this report does not do:** it authorizes no correction, establishes no corrected-state PASS, and does not advance the task.

## Items Reviewed

### Line-count tier and expected reviewers

| Item | Value | Evidence |
|---|---|---|
| Report physical lines | 1,263 | `wc -l` (in the N/A notes at 03:57:56Z). I re-confirmed it by reading lines 1-1263. |
| Tier | Up to 1,500 lines: 11 applicable lenses (4 structural, 4 content, 3 research-domain) | Task Phase 6 preamble (task file :375) and Steps 6.13-6.16 thresholds (over 1,500 lines gives 13; over 3,000 gives 15) |
| Expected applicable reviewers | 11 | Steps 6.2-6.12 |
| Actual applicable reviewer reports | 11 | Listed below |
| N/A size notes | 4. They are never counted as reviewers. | `qa/qa-lens-{evidence-table-integrity,causal-boundary-integrity,full-traceability-integrity,cross-case-generalization}.md`. Each says "N/A, not a review", records 1263 lines against a threshold of over 1500 or over 3000, and says it is "excluded from the Phase 6 reviewer count and from every reviewer floor". |

### Reviewer inventory

| Step | Lens | Agent type | Report | Exists | SHA-256 prefix | Literal verdict line | Counted issues |
|---|---|---|---|---|---|---|---|
| 6.2 | template-conformance | rf-qa | `qa/qa-lens-template-conformance.md` | Yes | `356eb2d4840f` | `:12` `### Overall Verdict: FAIL` | 5 (1 I, 4 M) |
| 6.3 | internal-consistency | rf-qa | `qa/qa-lens-internal-consistency.md` | Yes | `e627151ff05a` | `:15` `## Overall Verdict: FAIL` | 4 (0 I, 4 M) |
| 6.4 | evidence-quality | rf-qa | `qa/qa-lens-evidence-quality.md` | Yes | `dd5a52245a8f` | `:12` `### Overall Verdict: FAIL` | 6 (2 I, 4 M) |
| 6.5 | completeness | rf-qa | `qa/qa-lens-completeness.md` | Yes | `6bf1a283d78f` | `:14` `### Overall Verdict: FAIL` | 2 (1 I, 1 M) |
| 6.6 | actionability | rf-qa-qualitative | `qa/qa-lens-actionability.md` | Yes | `79161cca38b4` | `:14` `## Overall Verdict: FAIL` | 6 (3 I, 3 M) |
| 6.7 | numbers-metrics | rf-qa-qualitative | `qa/qa-lens-numbers-metrics.md` | Yes | `621df7e8ac76` | `:10` `## Overall Verdict: FAIL` | 2 (0 I, 2 M) |
| 6.8 | crossref-chain | rf-qa-qualitative | `qa/qa-lens-crossref-chain.md` | Yes | `00c7f98609d0` | `:38` `- Verdict: FAIL` (Summary form allowed by `SKILL.md:1150`) | 7 (2 I, 5 M) |
| 6.9 | domain-accuracy | rf-qa-qualitative | `qa/qa-lens-domain-accuracy.md` | Yes | `d67bf0416e22` | `:13` `## Overall Verdict: FAIL` | 4 (4 I, 0 M) |
| 6.10 | recommendation-feasibility | rf-qa-qualitative | `qa/qa-lens-recommendation-feasibility.md` | Yes | `52e5ae41c057` | `:44` `- Verdict: **FAIL**` (Summary form) | 7 (5 I, 2 M) |
| 6.11 | finding-reproducibility | rf-qa-qualitative | `qa/qa-lens-finding-reproducibility.md` | Yes | `4312a9b94ecc` | `:14` `## Overall Verdict: FAIL` | 5 (4 I, 1 M) |
| 6.12 | implementation-concreteness | rf-qa | `qa/qa-lens-implementation-concreteness.md` | Yes | `2034ef7c769d` | `:10` `## Overall Verdict: FAIL` | 5 (2 I, 3 M) |

**Totals:** 53 counted issues (24 IMPORTANT, 29 MINOR, 0 CRITICAL). Literal PASS 0, literal FAIL 11.

**Artifact form:**
- Every report has a findings table, a Summary and a Self-Audit.
- Every report states report-only status and was returned as text and saved by the parent (each header, plus task log at task file :681).
- One cosmetic irregularity: the completeness Summary repeats "Minor:" (`:47-48`, "0 in addition to the one below" and "1"). The counts are still unambiguous (1 I, 1 M), so I did not treat the report as malformed.
- I did not reopen the reviewer transcripts. Agent types come from Steps 6.2-6.12 and the report headers.

### Targets bound at consolidation (report-only check)

| Target | SHA-256 prefix | Modified | Binding |
|---|---|---|---|
| `RESEARCH-REPORT-review-loops.md` | `2d468cdde82b` | 2026-10-24 03:56:00Z | Earlier than every lens file (03:57:56Z to 04:09:45Z). No reviewer edited the target. |
| `synthesis/synth-01..06` | `912c408e3394`, `7b154d4b7232`, `ca519125409c`, `ca9ec77be6ba`, `0d02b9b81676`, `bcffe37af678` | last 03:48:49Z | Each matches the full hash in Report:1227-1232. |
| `research/evidence-deck.md` | n/a | 2026-10-23 16:51Z | Unchanged since before Step 5.12. |

### Consolidation checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | All expected applicable reviewer artifacts exist and are well-formed | PASS | 11 of 11 exist, with hashes and verdict lines as above. The 4 N/A notes are separate and not counted. |
| 2 | Literal verdicts read and preserved, not voted | PASS | All eleven verdict lines are quoted above. All are FAIL. |
| 3 | Full report read | PASS | Read lines 1-1263 in six reads this session. |
| 4 | Every reported issue verified against the report and its sources | PASS | Direct reads, plus four bounded read-only batch scripts (each ended `BATCH_OK failures=0` with cleanup). Git use was limited to `git show`. Results are in each register row. |
| 5 | Deduplicated, keeping all origin lenses and the highest severity | PASS | 53 raw issues become 31 groups. Mapping table below. |
| 6 | Cross-lens contradictions resolved or marked | PASS | Seven contradictions are resolved by evidence (section below). None needed an unresolved two-source marker. |
| 7 | No invented defect, quota or silent omission | PASS | No new defect group was added. Reviewer citation corrections are disclosed. |
| 8 | Scope filtering (`task/SKILL.md:357`) | PASS | All 31 groups affect the report or its synthesis components, which Step 6.18 names. Out-of-scope observations are logged as follow-up items. |
| 9 | Report-only agents did not edit targets | PASS | See the target timestamps and hashes above. |

## Summary

- Checks passed: 9 / 9 (consolidation checks). Gate verdict: **FAIL** (31 unresolved issues).
- Checks failed: 0 consolidation checks. 43 reviewer check identities are frozen as FAIL (see the cycle-0 sets).
- Critical issues: 0
- Important issues: 17
- Minor issues: 14
- Issues fixed in-place: 0 (not authorized)

### Raw-to-group mapping

| Lens | Raw issue to group |
|---|---|
| template | 1 to P6-01; 2 to P6-29; 3 to P6-30; 4 to P6-31; 5 to P6-19 |
| internal-consistency | 1 to P6-17; 2 to P6-25; 3 to P6-20; 4 to P6-02 |
| evidence-quality | 1 to P6-02; 2 to P6-02; 3 to P6-23; 4 to P6-24; 5 to P6-01; 6 to P6-15 |
| completeness | 1 to P6-05; 2 to P6-24 |
| actionability | 1 to P6-08 (version-pinning part to P6-12); 2 to P6-09; 3 to P6-11; 4 to P6-09; 5 to P6-21; 6 to P6-19 |
| numbers-metrics | 1 to P6-23; 2 to P6-17 |
| crossref-chain | 1 to P6-02; 2 to P6-06; 3 to P6-02; 4 to P6-26; 5 to P6-17; 6 to P6-27; 7 to P6-28 |
| domain-accuracy | 1 to P6-02; 2 to P6-02; 3 to P6-03; 4 to P6-04 |
| recommendation-feasibility | 1 to P6-10; 2 to P6-08; 3 to P6-12; 4 to P6-11; 5 to P6-13; 6 to P6-22; 7 to P6-02 |
| finding-reproducibility | 1 to P6-14; 2 to P6-15; 3 to P6-16; 4 (a-f) to P6-17, 4(g) to P6-11; 5 to P6-18 |
| implementation-concreteness | 1 to P6-12; 2 to P6-07; 3 to P6-19; 4 to P6-20; 5 to P6-09 |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| P6-01 | IMPORTANT (template 1 I; evidence 5 M) | Report:87, 196, 237, 245, 247, 263, 284, 328, 343, 347, 353, 390, 396, 400, 424, 436, 448, 716, 745, 801, 817, 828, 1033, 1056, 1152, 1164 | **Component self-references were left in the assembled report.** Phrases such as "this component", "this synthesis", "these sections" and "this worker" now name nothing. Three passages deny that a ranking exists, which contradicts Section 7.1: Report:87 "These sections describe the evidence, not the eventual ranking"; Report:284 "This component assigns neither ranking"; Report:436 "This component adds no case, hypothesis ranking". Producer self-reports read as plain fact: Report:390 "none invoked by this synthesis worker"; Report:1033 "not searches newly performed by this synthesis worker"; Report:1152 "this worker made no task edits". The only cited support, `research/web-01-gap-applicability.md:97-115`, covers only the applicability author. Cause: Report:1263 records that Sections 1-10.8 were copied byte-for-byte from the components. | Rewrite each passage at report level: name the section, or name the producer (for example "the synth-03 worker", "the synth-06 worker"). Label each producer statement as that producer's self-report, not independently verified. At Report:87, 284 and 436, send the reader to Section 7 for the ranking. **Constraint:** do not restate or alter the order. Allowed basis: assembly rule "minimal transitional text" (`tech-research/SKILL.md:1304`). |
| P6-02 | IMPORTANT (consistency 4 M; evidence 1 I, 2 I; crossref 1 I, 3 M; domain 1 I, 2 I; feasibility 7 M) | §2.3 label Report:169 and rows 173-178; Option E row 603; 7.5 V5 row 713; layer note 716 | **Current-protocol line citations are labelled "read directly from the current checkout" but carry no commit or read time, and the checkout has since moved.** Verified with `git show` and `stat`. At master `2165ae25` (the checkout before the 2026-10-24T03:42:30Z branch switch, task file :681) every cited range holds: `managed-workspace.md` pin at :42 (85 lines, blob `730be1c9`, which equals the rule-map bytes in `qa/qa-research-verification-structural.md:121`); enforcement rows at :84-85 inside :78-85; FINAL text at :44 and :60; `retry.md` "Cost and caps" at :142, "Worst case" :144, "Each resume after a halt" :146; workflow `SKILL.md` no-edit rule :58 and "Will Not" :72 inside :48-72; `ledger.md` :138 heading and :142 single-writer line. Commit `c6009cd3` (2026-10-23T18:03:42Z), which is in HEAD `bbbfcc4b` but not in `2165ae25`, moves the pin from 42 to 43 and "Will Not" from 72 to 74 (`git show c6009cd3^` gives 42/72; `c6009cd3` gives 43/74). The live working tree also has an uncommitted `retry.md` edit (modified 03:54:21Z; blob `0df39fde`) that moves "Cost and caps" to :161-165. `qa.md`, `quality-gates.md` and `ledger.md:138-158,142` still match. Installed copies: pin at :43 (rewritten 2026-10-23T17:55:50Z; identical to HEAD, `bb1a2a93`); `retry.md` at :142-146 (unchanged since 2026-10-22T20:29:54Z). Report:716 also repeats "diverged in four of seven pairs" (an 18:22Z observation) as a current statement. | Do not re-anchor to the moving working tree. Relabel Report:169 as "read from checkout master commit `2165ae25` before 2026-10-24T03:42:30Z (verify with `git show 2165ae25:src/superclaude/skills/<path>`)". Keep the existing line numbers, which are correct at that commit, and write each row's citation in that `git show 2165ae25:` form. Add the installed-layer equivalents with a read time: pin :43; `retry.md` :142-146; workflow `SKILL.md` :60 and :74; `ledger.md` :142. Rewrite Report:603, 713 and 716 as a dated observation: "At `2165ae25` the checkout pin is line 42; the installed copy has it at line 43; after the 03:42:30Z branch switch the working tree matches the installed copy." Mark the four-of-seven statement as dated 2026-10-23T18:22:14Z. Do not edit `retry.md` (the user's uncommitted work). Apply the same relabelling to the matching synth-01 and synth-04 text. |
| P6-03 | IMPORTANT (domain 3 I) | Report:198, 321, 371, 550, 711, 743; Q3 Report:922 | **Local evidence of where the rubric came from is treated as unavailable.** Verified: `git show 6dc56b1a:src/superclaude/skills/sc-implement-protocol/refs/qa.md` hashes to `0b533765…d425d083`, the earlier captured load (`research/scope-rules.md:70`). `git show 00448800:…/qa.md` hashes to `faff03b7…d2e7d5`, the later load (`:71`). Installed `qa.md` and `retry.md` were written at 2026-10-22T20:29:54.0176Z, between the two credential FINAL loads at 20:26:30.085Z and 20:32:19.277Z (`scope-rules.md:70-71`). Master `2165ae25` was committed at 20:29:01Z, and its `qa.md` blob is also `faff03b7`. | Add a labelled provenance note (Git-object and file-time evidence) to §2.3, Option C "Evidence strength" and 7.5 V3 "Must not be inferred". Narrow Q3 to "which process or person ran the 20:29:54Z install". Keep the caution that a current file is not a historical load. **Constraint:** add report and synthesis notes only. Do not change `synthesis/hypothesis-03.md` card text, the variants or the debate artifacts. No rank effect. |
| P6-04 | IMPORTANT (domain 4 I). **RANK-SUPPORT FLAG** | Option C Scope 548 and Debate record 551; Options Comparison 616; 7.4 "Shared clusters" 702 | **Two items counted as independent support for V3 share one cause.** The credential rubric change and the monitor's mid-run migration both follow the same 20:29:54Z install. Verified: monitor record 874 reads `/config/.claude/skills/sc-implement-protocol/refs/ledger.md` at 2026-10-22T20:34:06.655Z, and record 884 reads `…/SKILL.md` at 20:34:18.637Z, both after the install write. The skill load was at 19:29:17Z (`research/05-session-e002bed2.md:83`), before it. The installed `ledger.md` was rewritten on 2026-10-23, so its historical bytes cannot be hash-checked. Report:702 records other non-independent clusters but not this one. | Add the shared-deployment dependency to 7.4 "Shared clusters", Option C Scope and Evidence strength, and the comparison row. Label it as timing evidence. **Constraint:** do not re-rank, edit the debate or the cards, or change the displayed order. **Flag for the gate:** the debate's V3 reach weighting (`ADV/debate-transcript.md:343,380,421`) did not consider this dependency. Under Step 6.18 Verify, the fix must mark the debate-dependent synthesis checks for the V3 > V2 placement as affected so they are actually rerun. Whether to rerun the debate itself is the user's decision. |
| P6-05 | IMPORTANT (completeness 1 I) | §2.1 Report:99-111; §2.2; §10.1 Report:999 | **Repair-transition counts are never stated, although required.** `BUILD-REQUEST.md:50` says: "Reports must distinguish session count, incident count and failure-transition count." The report gives only "Counted separately" (Report:101). The deck's per-incident table (`research/evidence-deck.md:149-156`: review results / applied-repair transitions of 3/2, 3/2, 2/1, 2/1, 7/5 and 3/2) is cited (Report:111, 122) but never reproduced. The exclusion at Report:245 does not cover it. | Add the deck:149-156 table to §2.1, with its no-summing warning (deck:158). Cite deck:145-158. |
| P6-06 | IMPORTANT (crossref 2 I) | Gap 8 Report:318; §8 Phase 3 row Report:865; 10.10 Report:1249 | **Gap 8's target condition is lost.** The condition is "Where a persisted summary or verdict condenses a review, read the original returned review". A grep of Report:779-911 for condens / 13/3 / "persisted summar" / "returned review" gives 0 hits. Report:1249 still marks the gap as linked, with question "None". | Add the condition to the Report:865 Details, bound to `research/01-session-ac2cd1fd.md:81,90-103,253` and deck:613, 858-859. Alternatively add a §9 question. Then update Report:1249 and synth-05. |
| P6-07 | IMPORTANT (concreteness 2 I) | §8 Phase 3 rows Report:863-866; 10.10 Report:1248-1252 | **Four Phase 3 rows are the only §8 checks mapped to four gaps, yet they have no expected observation or pass/fail rule.** Phase 2 rows (Report:846-850) and Phase 3 rows 867-868 do have them. | Give each row an **Expected observation** plus a pass/fail line in the Phase 2 style. Alternatively, relabel them as interpretation constraints and correct the 10.10 mapping. |
| P6-08 | IMPORTANT (actionability 1 I; feasibility 2 I) | 7.6 order 1 Report:724; trade-offs Report:729; Option A Falsification Report:495; Files rows 502 and 529; §8 Phase 2 row 1 Report:846; constraints Report:878-879 | **The steps are called read-only but require approved execution, and the first step has two procedures that do not fit together.** Option A and its card say "Run the described check against the counterexample" (`synthesis/hypothesis-01.md:142`, verified). Report:846 says to compare with an example "already established by review". Report:729 says "Steps 1-3 … stay read-only", while Report:553 says Option C needs approved adjudications and Report:878-879 require authorization and a disposable copy for any replay, test or model run. The oracle package is still a live `to-do/` package (verified present). | Choose one procedure for 7.6 order 1 and use it in Option A, 7.6 and §8. Replace "stay read-only" with "require separately approved execution in a disposable copy (Section 8 constraints)". Add execution and live-state risk next to misreporting risk. Change the Files rows to "read-only sources plus a disposable execution copy". |
| P6-09 | IMPORTANT (actionability 2 I, 4 M; concreteness 5 M) | 7.6 "What would change the ranking" Report:724-727; rationale Report:639; §8 Report:846-851; Option C Report:549, 558 | **No decision rule links check results to rank changes.** Order 1 gives no denominator. Order 2 itself says "Neither replaces the reach-weighting judgment". Order 4 says only "could settle … no outcome is predicted". Option C gives no repeat count and no agreement rule. | For orders 1-4, state the finding set, what counts as weakening, and how a result would change placement under A-001 (Report:466-471). If the evidence cannot support such a rule, state plainly that the step cannot change a placement, and drop the claim. **Constraint:** do not invent numeric thresholds, and do not change the current displayed order. These rules apply only to future unexecuted checks. |
| P6-10 | IMPORTANT (feasibility 1 I) | Options Comparison "Integration complexity" Report:624 versus 7.6 Report:724-726 | **The recommended order ignores dependencies the report itself records.** A "Needs V2's absent-before check" but runs alone in step 1. C "Must hold V4's proof state fixed" but runs in step 2, before D in step 3. | Preferred: state inside 7.6 steps 1 and 2 how each dependency is met (A applies B's absent-before check; C first applies D's proof-state reconstruction). That keeps the recommended order. Reordering the steps changes the synth-04 recommendation and is not preferred. Neither option touches the cause ranking. |
| P6-11 | IMPORTANT (actionability 3 I; feasibility 4 I; reproducibility 4(g)) | Option D Reuse 582 and Effort 580; Files 583; Option C Reuse and Files 555-556; 7.6 orders 2-3; Report:878 | **The historical inputs for Options C and D are not reachable as described.** (a) Trees are given only as `f60d2c3…`, `3c5fdfa…`, `00d8f4a…`, with no repository named. Full IDs are in `research/03-session-6f744b87.md:216,229,237` (verified), and loose objects with those prefixes exist under `/config/workspace/Coder/.git/objects/` (I did not validate them as tree objects). Reading them is a Git action, which the scope forbids (Report:8; `gaps-and-questions.md:12` "no new Git operation") and which Report:878 does not list for authorization. (b) The recorded worktree `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env` is gone (verified). A `t3-markdownlint.log` candidate exists at `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/artifacts/t3-markdownlint.log` (1,222 bytes; identity not hash-verified). (c) The credential state before repair must be rebuilt from the nested transcripts (45 `.jsonl` files present under `…/0690ee9f-…/subagents/`). | Name the Coder repository and the full IDs. Add "read-only Git object access" to Report:878 and to the 7.6 order 3 prerequisites, with "confirm object availability first". State the deleted worktree, the t3 candidate with its identity caveat, and the reconstruction requirement. Re-justify the C and D effort and risk ratings to include that reconstruction. |
| P6-12 | IMPORTANT (concreteness 1 I; feasibility 3 I; actionability 1, version-pinning part) | §8 Phase 1 Report:799-836; Phase 2 Files Report:846-850; 7.6 Report:720, 724; Option A Pros and Reuse Report:501, 503 | **The inputs for the order 1 and order 2 replays are neither named in §8 nor accurately described.** Report:720 promises "Step-level targets are in Section 8", but the §8 Files columns name only case reports and the deck. The oracle claim "preserved inputs exist for all four contexts" (Report:503) overstates: `research/02-session-a9b88895.md:269,295` (verified) say there is no preserved full pre-authorization oracle snapshot. The builder transcript `…/a9b88895-…/subagents/agent-aoracle-builder-6889f23314fbb16e.jsonl` exists (2,021,102 bytes). "First-passing version" is unpinned for Orca and CI planning. | Add a "Replay input artifacts" table to §8 Phase 1. Include the paths verified by the concreteness lens (oracle `artifacts/`, Orca `coverage-matrix.yaml`, both `merged-verdict.yaml` files, CI original and regenerated plans), the six session JSONL paths (deck:121-128) and the builder transcript, each with the date availability was observed. Name the artifact version for each context. Change Option A Pros to "preserved or reconstructable; oracle code and monitor first-passing state need reconstruction, with no independent byte check (Q13)". |
| P6-13 | IMPORTANT (feasibility 5 I) | Q7 Report:926; §5.1 CI row Report:374 | **An existing execution ledger for the CI plan, from after the window, is treated as unavailable.** Verified: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/done/TASK-WF-specR1-20261023-031725/progress.md:1` (created 2026-10-23T04:06:20Z), `:21` `FINAL: pass`, `:22` `ARCHIVE: start`. The case names this package (`research/04-session-43582de1.md:593`). | State in Q7 and §5.1 that this post-window ledger exists, is outside the frozen sample, and is not causal-ranking evidence. Name it as the target for any approved Q7 follow-up. Keep the "within the declared window" statement. |
| P6-14 | IMPORTANT (reproducibility 1 I) | §2.2 oracle row Report:146; Option A Report:491; comparison Report:617 | **Oracle record 291 is a truncated relay, not the complete review.** Verified: the record ends with "result truncated — ask the agent for the rest via SendMessage". The screening research had flagged this (`research/scope-05.md:44`). The full findings 1-4 are at `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-1.md:20-35` (verified headings 1-4). | Label 291 as a truncated relay and cite `t12-review-1.md:20-35` for "four valid defects", in both the report and synth-01/04. |
| P6-15 | IMPORTANT (reproducibility 2 I; evidence 6 M) | §2.2 credential row Report:150; Option C Support Report:545; Option D Report:572-577 | **The credential lint chain leaves out a step and cites records that are not the review itself.** (a) Record 1230 (19:51:13.212Z) is an executor `sed -i` that rewrites `RESULT: DIFFERENCE FOUND` to "no new findings …" and appends a note. Verified, and recorded at `research/06-session-0690ee9f.md:160-162`. (b) "FINAL reapplies the clause" cites 1215, 1230, 1935 and 1938. 1935 (20:20:43.704Z) is the parent's summary and 1938 is the user's "accept and fix". The primary records are dispatch 1916 (20:16:10.434Z), nested `agent-a9c0c61dd415c2c4d.jsonl:135` (20:20:21.142Z) and parent result 1932 (20:20:36.570Z, `FINAL: issues`), all verified. | Add "1215 DIFFERENCE FOUND; 1230 executor rewrites the log RESULT line and appends a note; nested `a6d8fbaf…:61` reviewer accepts" to §2.2 and Option C. Add 1916, nested 135 and 1932 to the Option C "FINAL reapplies" citation. **Constraint:** you may note the relevance to V4, but do not re-rank. |
| P6-16 | IMPORTANT (reproducibility 3 I) | §2.1 boundary table Report:124-127; §2.2 Report:148-149; §2.6 Report:243; §2.7 Report:260 | **Each case's physical observation boundary is not stated, and on-topic events after the window are undisclosed.** Verified: the monitor case declares 1,437 rows (`research/05-session-e002bed2.md:343,432`). The live log has 2,058 lines. `implement-retry-adviser` appears at records 1620-2049 (for example 1670 at 04:43:07.765Z; 1943/1945 at 05:19Z; 1997 at 05:24:32.039Z). CI record 1087 (04:07:09.883Z) reads "running that in another session". Report:260 ("did not execute the current adviser/revert ladder") is true only for Task 12 within the window. | Give each case its row and time boundary in §2.1. Add an out-of-window note, excluded from all counts, for monitor Task 14 and CI 1087. Limit Report:260 to Task 12 within the window. **Constraint:** disclosure only. Do not add these events to evidence, counts, Opposition rows or the ranking. |
| P6-17 | IMPORTANT (reproducibility 4(a-f) I; consistency 1 M; numbers 2 M; crossref 5 M) | Report:448 path key; Report:150, 459-460, 491, 518, 527, 545, 572, 582, 596, 661, 675, 677, 683-684, 688, 1201-1211 | **Citations do not resolve under the report's own path rules.** (a) Bare names `return-contract.md` and `merged-root-cause-analysis.md` (actually in `reviews/adversarial/`), `refactor-plan.md` (`ADV/`) and `synthesis-gate-decision.md` (`phase-outputs/plans/`). (b) Nested basenames with no directory (`…/0690ee9f-…/subagents/`), and nested records 135 and 116 with no file named. (c) `coverage-matrix.yaml`, `merged-verdict.yaml` and "source `:142,285,382,402`" with no root (real anchor `research/01-session-ac2cd1fd.md:296-297`, verified). The CI boundary-file clause has no citation (`synthesis/hypothesis-03.md:60`). (d) `t12-review-2.md:20-28` with no directory. (e) Report:527 "records 150/151, 1164-1170" mixes two logs: Orca planning 150/151 (case 01:64, 410-411) and monitor 1164-1170 (case 05:160), both verified. | Extend the path key with the credential `subagents/` directory and the Orca reflect and plan roots. Prefix each bare file. Name the nested files for 135 (`agent-a9c0c61dd415c2c4d.jsonl`) and 116 (`agent-acf0a51e6992c50ee.jsonl`). Write "Orca planning records 150/151; monitor records 1164-1170". Cite `research/01-session-ac2cd1fd.md:296-297` and `research/04-session-43582de1.md` §6.3 for the CI clause. |
| P6-18 | MINOR (reproducibility 5 M) | Option D Support Report:572 | The Task 10 trace cites nested `agent-af349dd52cae648a5.jsonl:16` only. The wrong `:10-12` citation first appears at record 33 (19:57:44.798Z, verified). The case cites both (`06-session-0690ee9f.md:205-212`). | Cite records 16 and 33, and keep 1425 as the point where the pointer was created. |
| P6-19 | MINOR (template 5 M; actionability 6 M; concreteness 3 M) | §8 step tables Report:819-822, 844-851, 861-868 | Steps have no IDs, and some locators match no heading: "Relevant case file"; "Orca … coverage-matrix analysis" (actually §4 "Why the original review did not catch…", case 01:227); "CI … retained acceptance findings" and "CI … dependency analysis" (case 04 headings: §6.2 :167, supplement §5 :405, §7 :207, all verified). | Add IDs (1.1-1.2, 2.1-2.6, 3.1-3.6) and cite them from 7.6. Replace the vague locators with real section numbers and headings. |
| P6-20 | MINOR (consistency 3 M; concreteness 4 M) | Report:801 versus Report:850 | "One later row cites a file outside this table". The feasibility row (Report:850) also cites the three rendering targets from the separate table (Report:830-834). | Say that two rows cite files outside the table, and name both. |
| P6-21 | MINOR (actionability 5 M) | 7.6 order 3 Report:726 | "Option D … two incidents" contradicts Option D's own scope: one incident plus two controls in two sessions (Report:575, 147, 150). | Write: "Option D on its one incident and two controls (three contexts in two sessions); Option E on its two incidents". |
| P6-22 | MINOR (feasibility 6 M) | Effort rows Report:499, 526, 553, 580, 604, 621 | The S/M scale is undefined, and the Option A and B rationales give no finding or edit counts. | Define the scale, state the per-context counts, and re-check the ratings. |
| P6-23 | MINOR (evidence 3 M; numbers 1 M) | Report:763 (from `synthesis/synth-04-options-recommendation.md:327`) | "901 lines". `wc -l` gives 900, the file ends with a newline, and it was unchanged since 16:51Z on 2026-10-23 (verified). | Change to 900 in the report and in synth-04:327. |
| P6-24 | MINOR (evidence 4 M; completeness 2 M) | 10.9 provenance table Report:1215-1221; rows 1200-1201 | (a) `merge-log.md`, filed as raw evidence, has parent records appended at `:194-195` (verified "Recovery completed: Parent persisted…"). The case reports, filed as exact returns, have later main supplements (Report:1007-1010). (b) The two synthesis verifications say they are text returns for the parent to save (`:12` of each, verified) but are labelled only "file header". The resume-analysis files and `input-inventory.md` are in no class. | Mark mixed-authorship files "with appended main/parent records". Move the two verifications into the main-persisted class. Classify the five remaining files, or widen the classification source to 10.2-10.7. |
| P6-25 | MINOR (consistency 2 M) | Report:118 versus 147 and 596; deck:54 | "Two `cannot-verify` results after evidence-only resubmission". The deck puts that phrase on the subset label, and the first result came before the resubmission. | Write: "Two `cannot-verify` results, the second after an evidence-only resubmission…". |
| P6-26 | MINOR (crossref 4 M) | 10.10 Report:1242, 1248 | Gap 1 maps to Q15 (about evidence pointers, which belongs to gap 4). Gap 7 maps to Q2 (missed preexisting defects, the opposite failure). | Set both cells to "None", or name questions that actually address those gaps. |
| P6-27 | MINOR (crossref 6 M) | 7.2 source line Report:661 | It says the five orders are "repeated at `return-contract.md:24`". That line gives only the displayed order and the scope statements (verified). | Write "displayed order also at `reviews/adversarial/return-contract.md:24`", and keep `merged-root-cause-analysis.md:37-43` for the five orders. |
| P6-28 | MINOR (crossref 7 M) | Option E Debate record Report:602 | The quote "more direct for its two retained blockers, but narrower overall" appears verbatim only at `ADV/debate-transcript.md:265`. Line 304 says "more decisive … but narrower", and line 344 says "a narrower judgment" (verified). | Credit the quote to :265 only, and cite :304 and :344 as agreeing in substance, without quotation marks. Debate artifacts stay unchanged. |
| P6-29 | MINOR (template 2 M) | Report:720, 910 | These cite synthesis files where they should cite report sections, and the Integration Checklist carries component-delivery metadata. | Cite "Section 8 …" and "Section 9, Question 1". Remove the 910 row or move it to §10. |
| P6-30 | MINOR (template 3 M) | §7.8 Report:756-775 | A producer's reading log sits inside the Recommendation. Report:768 says `web-01` was "Not read directly", although §5 is built on it. | Move it to §10 as the "synth-04 producer read record", and update TOC line 55. Apply P6-23 wherever the text ends up. |
| P6-31 | MINOR (template 4 M) | §5 Report:420-436 | 5.5 "Evidence and Limits" comes after 5.4 "External Research Summary". The template ends with the Summary (`tech-research/SKILL.md:1388-1389`). | Swap them, and update TOC lines 37-38. |

### Claims adjusted after verification

1. **Drifted layer anchors (P6-02).** Several lenses called the 42/43 contrast "false at assembly" or "no longer existing". It is correct for `git show 2165ae25` against the installed copy. It became stale only for the live working tree after the 03:42:30Z switch brought in `c6009cd3`. The defect is the "current checkout" label with no commit or read time, not a wrong original reading.
2. **Commit attribution (P6-02).** I verified that `c6009cd3` itself shifts both `managed-workspace.md` (42 to 43) and the workflow "Will Not" line (72 to 74). This confirms the crossref and domain attribution. The consistency lens's "one line at :36" location was not separately checked.
3. **ledger.md (P6-02).** The evidence lens listed `ledger.md` as changed. Its blob did change, but the cited :138-158 and :142 still hold in the working tree and the installed copy, so it needs labelling only.
4. **Rubric provenance (P6-03).** The reflog pull time and the `merge-base` ancestry claims were not re-verified, because I limited Git to `git show`. Hash identities and the install time were verified.
5. **Shared deployment (P6-04).** The origin of commit `3ad7e207` and the pull timing were not re-verified. The read and install timing was.
6. **Record 291 (P6-14).** My bash string length is 5,487, against the reviewer's 4,893 characters (different counting method). The truncation marker is confirmed either way.
7. **Record 1230 (P6-15).** The "wrong actor" sub-claim is qualified. Report:150's "Task QA knowingly softens" describes the nested reviewer's acceptance (`a6d8fbaf…:61`) and is supported. The defect is the missing executor rewrite.
8. **Adviser hits (P6-16).** Hits continue past the reviewer's stated 1620-2014 range, at 2040, 2043, 2047 and 2049. I did not classify them.
9. **Git objects (P6-11).** I confirmed the three Git objects only as loose files, not as valid tree objects.

### Cross-lens contradictions (resolved)

| Contradiction | Resolution |
|---|---|
| Completeness check 3 PASS (every gap has a §8 or §9 entry) versus crossref finding 2 (gap 8 condition lost) | Both hold. Each row exists, but the condition-level link fails. P6-06 stands. |
| Numbers check b PASS (effort labelled as reasoned) versus feasibility finding 6 (scale undefined) | Different properties. P6-22 stands. |
| Crossref checks b/c "PASS with defects", numbers a/c "PASS except", domain e "PASS with one exception" | Each carries a finding. Classified FAIL in the frozen set so the regression guard is not misfired. |
| retry.md lines: evidence "163-165", domain "161-165", crossref "142-146 in HEAD/installed" | All consistent: working tree heading :161, text :163/:165; `2165ae25`, HEAD and installed :142/:144/:146. |
| Evidence check 11 PASS (no current state projected onto history) versus domain finding 3 (available history called unknown) | Different directions. P6-03 stands. |
| Consistency check 2 PASS (counts agree) versus completeness finding 1 (transition counts absent) | Agreement is not completeness. P6-05 stands. |
| Template check c PASS (no placeholders) versus the stale "NOT yet validated" status lines (template Self-Audit) | Accurate today. Logged as a follow-up for after the gate. |

### Independent report-validation cycle-0 sets

**PASS identities (55):**
- template-conformance: a, c, d, f
- internal-consistency: 1, 2, 3, 6, 7
- evidence-quality: 3, 5, 6, 8, 9, 10, 11, 12
- completeness: 1, 2, 3, 4, 5, 6, 7, 9, 11, 12
- actionability: Step 6.6-3, 6.6-4, 6.6-5
- numbers-metrics: b, d, S1, S2, S3, S4, S5, S6
- crossref-chain: d, g
- domain-accuracy: b, c, f
- recommendation-feasibility: f, g, h
- finding-reproducibility: d, S1, S5
- implementation-concreteness: 3, 4, 5, 6, 7, 9

**FAIL identities (43):**
- template: b, e, g
- consistency: 4, 5, 8
- evidence: 1, 2, 4, 7
- completeness: 8, 10
- actionability: a, b, c, d, 6.6-1, 6.6-2
- numbers: a, c
- crossref: a, b, c, e, f
- domain: a, d, e, g
- feasibility: a, b, c, d, e
- reproducibility: a, b, c, S2, S3, S4
- concreteness: 1, 2, 8

**Frozen failure set:** P6-01 through P6-31. |F| = 31: 17 IMPORTANT, 14 MINOR, 0 CRITICAL.

## Actions Taken

None. Report-only.
- No file was written or edited.
- No agents or tests were run.
- No Git write or staging. `git show` only.
- No archive, move, delete or publication.

## Recommendations

- Hand P6-01 through P6-31 to the single Step 6.18 correction worker. That worker is limited to the report and to the matching synth-01 through synth-06 and deck corrections. Historical sources, debate artifacts, variants, card causal text and `retry.md` must not change.
- P6-04 (and, less strongly, P6-03 and P6-16) must be applied as disclosures only. Step 6.18 must mark the debate-dependent V3 > V2 support checks as affected for an actual rerun, not a backdated PASS. Rerunning the debate is the user's decision.
- **Follow-up items (out of scope, not findings):**
  - The status lines at Report:5, 1192 and 1213 must be refreshed once Phase 6 completes.
  - The `qa/synthesis-gate-intake.md:8` placeholder is accurately reported at Report:1212.

**Self-Audit:**
- Read all 11 reports and 4 notes in full.
- Read the report in full.
- Re-ran primary checks for every group:
  - Git blob line numbers and hashes at `2165ae25`, `c6009cd3^`, `c6009cd3`, HEAD, the working tree and the installed copies.
  - Six session-log record reads.
  - Artifact existence: oracle reviews, CI ledger, t3 log, builder transcript, Git loose objects.
  - Deck and case anchors.
  - Component hashes.
- Unverified sub-claims are listed above.

## QA Complete

| Status | Result |
|---|---|
| DONE | Consolidated 11 applicable final-report lenses (all literal FAIL, confirmed). Excluded 4 N/A size notes from the counts. Verdict FAIL: 31 unique issues (17 IMPORTANT, 14 MINOR, 0 CRITICAL) from 53 raw. Cycle-0 sets: 55 PASS and 43 FAIL check identities. |
| DONE | Edited nothing. Ran no agents or tests and made no Git writes. `git show` read-only only. |
| NEXT | Parent saves this text verbatim at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-consolidated-findings-phase6.md` with attribution, then runs Step 6.18 with the P6-04 rank-support flag carried into the fix log. |

## Parent Persistence Record (2026-10-24)

The parent persisted this exact restricted return from current session subagents/agent-afr-consolidate-*.jsonl (246 lines, 40,318 bytes before this record) and read the rank-sensitive rows P6-03, P6-04 and P6-16. Note on inputs: the evidence-quality reviewer later re-sent a wording-only variant of its report with identical finding rows; the persisted earlier copy, which this consolidation read, is retained. This record is a delivery receipt, not a gate verdict.
