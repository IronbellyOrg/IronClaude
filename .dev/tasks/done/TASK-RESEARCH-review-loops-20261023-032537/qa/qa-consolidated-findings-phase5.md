# QA Report: Phase 5 Synthesis Gate Consolidation

**Topic:** Phase 5 synthesis gate (Steps 5.13-5.22), consolidating ten partitioned reviews of synthesis components 01-06 and hypothesis cards 01-05
**Date:** 2026-10-24
**Status:** Consolidation is complete as returned text. Parent persistence is pending.
**Phase:** synthesis-gate, Task Step 5.23
**Lens:** Cross-partition, cross-lens findings consolidation
**Fix cycle:** 0 (the frozen baseline before any correction)
**Fix authorization:** false
**Governing format:** Task Standard QA Report Output Format (`/config/.claude/skills/task/SKILL.md:466-506`). It is extended as Step 5.23 requires with a reviewer inventory, deduplicated findings, contradictions and cycle-0 sets. The consolidation rules come from the Serialized Fix Protocol step 2 (`task/SKILL.md:357`): deduplicate, keep every originating lens, keep the highest severity. They also follow tech-research Phase 5 Step 5.N+2 (`/config/.claude/skills/tech-research/SKILL.md:511-517`).
**Intended output:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-consolidated-findings-phase5.md`

**Delivery limitation:** My higher-priority instructions prohibit writing report files. I created no stub and no file. This text is the complete report for the parent to persist. It is not a claim that the target file exists. At consolidation time the target did not exist (`ls` returned "No such file").

All relative paths below resolve under `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. `ADV/` means `reviews/adversarial/adversarial/`.

---

## Overall Verdict: FAIL

- **Literal verdicts:** all ten reviewers returned FAIL. I confirmed each literal verdict line independently (see the inventory). No reviewer returned PASS.
- **Unique issues after deduplication:** 33 genuine issues. By severity: CRITICAL 0, IMPORTANT 11, MINOR 22. Every one stays in the failure set.
- **Raw input:** 68 reviewer-counted issues plus 3 out-of-lens referrals.
  - All 71 were checked against the actual synthesis text and its sources.
  - No raw issue was found unsupported in whole, so none was dropped.
  - Four reviewer citation details were corrected, and one evaluative sub-claim and one sequencing sub-claim were qualified. All six adjustments are listed in "Claims adjusted after verification".
- **What this report does not do:** it authorizes no correction, establishes no corrected-state PASS, and does not advance the task.

## Items Reviewed

### Expected and actual reviewers

Ten report-only reviewers were expected, one per Step 5.13-5.22, split into partition 1 (synth-01..03) and partition 2 (synth-04..06, the five cards and the actual debate artifacts). All ten reports exist.

| Step | Lens | Expected agent type | Partition | Report | Exists | SHA-256 prefix | Literal verdict line | Reviewer-counted issues |
|---|---|---|---|---|---|---|---|---|
| 5.13 | synthesis-accuracy | rf-analyst | 1 | `qa/analyst-synthesis-accuracy-1.md` | Yes | `10f9f60283cf` | `:12` `## Overall Verdict: FAIL (9 issues: 0 critical, 4 important, 5 minor)` | 9 (4 I, 5 M) |
| 5.14 | synthesis-accuracy | rf-analyst | 2 | `qa/analyst-synthesis-accuracy-2.md` | Yes | `19f47bf8894a` | `:12` `## Overall Verdict: FAIL (7 issues: 0 critical, 0 important, 7 minor)` | 7 (0 I, 7 M) |
| 5.15 | source-tracing | rf-analyst | 1 | `qa/analyst-synthesis-tracing-1.md` | Yes | `c96cd39935e5` | `:12` `## Overall Verdict: FAIL (6 issues: 1 important, 5 minor, 0 critical)` | 6 (1 I, 5 M) |
| 5.16 | source-tracing | rf-analyst | 2 | `qa/analyst-synthesis-tracing-2.md` | Yes | `4a0ca0240c31` | `:12` `## Overall Verdict: FAIL (8 issues)` | 8 (5 I, 3 M) |
| 5.17 | structure | rf-qa | 1 | `qa/qa-synthesis-structure-1.md` | Yes | `6ceaff378207` | `:16` `## Overall Verdict: FAIL` | 10 (1 I, 9 M) |
| 5.18 | structure | rf-qa | 2 | `qa/qa-synthesis-structure-2.md` | Yes | `4b486d46f075` | `:16` `## Overall Verdict: FAIL` | 7 (0 I, 7 M) |
| 5.19 | content-quality | rf-qa | 1 | `qa/qa-synthesis-content-1.md` | Yes | `0ae6f5cfd766` | `:16` `## Overall Verdict: FAIL` | 4 (2 I, 2 M), plus 3 out-of-lens referrals |
| 5.20 | content-quality | rf-qa | 2 | `qa/qa-synthesis-content-2.md` | Yes | `08c76650c81a` | `:16` `## Overall Verdict: FAIL` | 7 (4 I, 3 M) |
| 5.21 | synthesis-coherence | rf-qa-qualitative | 1 | `qa/qa-synthesis-qualitative-report-1.md` | Yes | `f7dacf2c1631` | `:16` `## Overall Verdict: FAIL` | 3 (0 I, 3 M) |
| 5.22 | synthesis-coherence | rf-qa-qualitative | 2 | `qa/qa-synthesis-qualitative-report-2.md` | Yes | `d889d68ed1e2` | `:16` `## Overall Verdict: FAIL` | 7 (5 I, 2 M) |

**Totals:** 68 counted issues (22 IMPORTANT, 46 MINOR, 0 CRITICAL) plus 3 out-of-lens referrals in content-1. Literal PASS 0, literal FAIL 10.

**Reviewer identity limit:** the agent types come from each report's header and governing template and from the task-log entry at task file line 643 ("2 rf-analyst accuracy, 2 rf-analyst tracing, 2 rf-qa structure, 2 rf-qa content, 2 rf-qa-qualitative coherence"). I did not re-open the subagent transcripts. All ten reports say they were returned as text and persisted by the parent. Per that log entry, a delivery receipt is not an approval and does not change any verdict.

### Targets bound at consolidation

| Target | SHA-256 prefix | Binding note |
|---|---|---|
| `synthesis/synth-01-problem-current-state.md` | `fcbaedde0528` | Matches the hash the partition-1 reviewers reported (`fcbaedde…`). |
| `synthesis/synth-02-target-gaps.md` | `f7fd5451e2f4` | Matches the reported `f7fd5451…`. |
| `synthesis/synth-03-external-findings.md` | `4a352d1e4ed9` | Matches the reported `4a352d1e…`. |
| `synthesis/synth-04-options-recommendation.md` | `e3a8900b7c68` | Persisted 2026-10-24 with a Parent Persistence Record (`synth-04:339-341`). |
| `synthesis/synth-05-implementation-plan.md` | `d5cdf5965d2c` | Matches the `d5cdf596…` that accuracy-2 compared against intake. |
| `synthesis/synth-06-questions-evidence.md` | `8ac285ee4c3e` | Matches the `8ac285ee…` that accuracy-2 compared against intake. |
| `synthesis/hypothesis-01.md` … `hypothesis-05.md` | `4f324b28811b`, `765fcc04fc2d`, `64eb89ade97d`, `b09d2dea0d96`, `9f14883c17ea` | Post-debate format-only presentations. The debated identities are the immutable `ADV/variant-1..5-original.md`. Structure-2 check 11 re-hashed those against `input-manifest.json`. |

All six components and five cards are therefore the bytes the reviewers examined. No component was edited between the reviews and this consolidation.

### Consolidation checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | All expected reviewer artifacts exist | PASS | Ten of ten exist (listing plus hashes above). No absent artifact. |
| 2 | Literal verdicts read and preserved, not voted | PASS | The ten verdict lines are quoted above, all FAIL. |
| 3 | All five cards and the actual debate are in scope | PASS | Partition-2 reviewers read the cards and the `ADV/` artifacts: accuracy-2 Self-Audit 3-4, tracing-2 Self-Audit, structure-2 checks 8 and 10-11, content-2 Criteria, qualitative-2 checks 2-3 and 16. All 13 debate artifacts are present in `ADV/`. |
| 4 | Every reported issue independently verified | PASS | I read all six components in full. I re-read every cited source range named below, using direct reads and four bounded read-only batch scripts. Results are in each register row. |
| 5 | Deduplicated, keeping every origin lens and the highest severity | PASS | 71 raw items become 33 groups. Traceability tables are below. |
| 6 | Cross-partition contradictions resolved or marked | PASS | 12 contradictions are resolved by evidence (section "Cross-Partition and Cross-Lens Contradictions"). None needed a two-source unresolved marker. |
| 7 | No invented defect, quota or silent omission | PASS | I added no new defect group. Corrections to reviewer citations are disclosed. |
| 8 | Scope filtering (`task/SKILL.md:357`) | PASS | All 33 groups touch synthesis files named in Steps 5.1-5.12. Four reviewer-conduct and governing-source observations are logged as follow-up items, not findings. |

## Summary

- Checks passed: 8 / 8 consolidation checks
- Reviewer verdicts: 0 PASS, 10 FAIL
- Unique issues: 33 (CRITICAL 0, IMPORTANT 11, MINOR 22)
- By file: synth-01: 6 groups; synth-02: 6; synth-03: 4; synth-04: 13; synth-05: 4; synth-06: 6; cards: 1. Several groups span more than one file.
- Raw issues dropped as unsupported: 0. Reviewer citation details corrected: 4. Sub-claims qualified: 2.
- Issues fixed in place: 0 (report-only)
- Re-debate required by the corrections as scoped below: none. Four groups carry explicit conditions under which a correction would need a real re-debate (see "Correction Scoping and Re-debate Flags").

## Issues Found

### Deduplicated findings register: partition 1 (synth-01, synth-02, synth-03)

| ID | Severity | Origin lenses (report: issue) | Location | Verified issue and evidence | Required correction |
|---|---|---|---|---|---|
| P5-01 | IMPORTANT | accuracy-1: 1, 2, 3 (IMPORTANT); structure-1: 2 (MINOR); content-1: 4 (MINOR); structure-2: 2 (MINOR). Considered non-defects by tracing-1 Self-Audit and qualitative-1 Self-Audit (resolved at C1). | synth-01:4, 7, 173-176; synth-02:4, 8, 91-94; synth-03:4-6, 85-88; synth-04:4, 7, 333-337; synth-05:4, 7, 133, 135, 137-140; synth-06:4, 7, 229-232 | **What is wrong:** all six components carry worker handoff status lines and DONE/NEXT tables inside their assemblable bodies, and these say persistence or QA is still pending.<br>**Examples:** synth-02:93 says "No files were written" although the file exists. synth-03:5 says "This worker did not modify the existing output file". synth-05:135 says "Recommended next action: Persist this returned component".<br>**Receipts:** only synth-04 has an in-file Parent Persistence Record; a grep count of that heading is 0 in synth-01/02/03/05/06. synth-04's DONE/NEXT table at 333-337 still sits inside Section 7's body.<br>**Rule broken:** the template requires sections "in the exact format they should appear in the final report" (`tech-research/SKILL.md:810`). A mechanical assembly would copy stale process text into Sections 2, 4, 5, 7, 8 and 10. | Keep the producers' original text, but take it out of the assemblable body. Either append a dated Parent Persistence Record to each component (a receipt, not an approval, in the form of `synth-04:339-341`) and mark the header status lines and DONE/NEXT tables as excluded from assembly, or move them below a clearly marked non-assembled provenance block. Do not claim any gate PASS in the receipt. |
| P5-02 | IMPORTANT | accuracy-1: 4 (IMPORTANT); structure-1: 1 (IMPORTANT); content-1: out-of-lens (a) | synth-03:73-83 | **What is wrong:** an unnumbered H2 `## Evidence and Limits` sits inside the Section 5 component. The template allows only `### 5.1 …` through `### 5.N External Research Summary` under `## 5.` (`tech-research/SKILL.md:1378-1389`). Assembled as written, it becomes a stray top-level section between 5 and 6. | Demote it to `### 5.5 Evidence and Limits` (keeping 5.4 as the summary, or renumber the summary last), or fold its table and paragraphs into 5.4. |
| P5-03 | MINOR | accuracy-1: 5; structure-1: 3; content-1: out-of-lens (b); qualitative-1: 2 | synth-02:50-61 (Severity column) | **(a) Non-template value:** rows 60-61 use the Severity value "Important evidence limit", which is outside the template set `Critical/Important/Minor` (`tech-research/SKILL.md:1370-1372`).<br>**(b) Inconsistent labels:** row 59's Notes call it a "Research-accounting boundary … not … newly inferred product defect", the same kind of row as 60-61, yet it is plain "Important". This contradicts the defect-versus-inference-limit split the table itself states at synth-02:46.<br>**(c) Uniform rating:** all twelve rows are rated Important. This sub-claim from qualitative-1 is evaluative (see adjustments). | Use only template values. Put the "evidence limit" or "inference limit" type in the Notes column, applied consistently to rows 59-61. Either re-rate each gap on the template scale from its demonstrated effect, or state in the table preamble why each defect row is Important. |
| P5-04 | MINOR | accuracy-1: 6; tracing-1: 2; structure-1: 9; qualitative-1: 1 | synth-01:67 (credential row, "Primary transitions" and evidence ranges) | **What is wrong:** the follow-up chain "1215/1230 → 1938 → 1968 → nested second FINAL record 116 → repairs 2015 → pass/archive 2036" omits the first failed follow-up FINAL. The cited ranges also skip `research/06-session-0690ee9f.md:130-140`, where that review is anchored.<br>**The missing review:** dispatched at parent 1916 and concluded at nested `agent-a9c0c61dd415c2c4d.jsonl` record 135 (`06-session:133-137`). The parent records it as "1932 issues" (`research/evidence-deck.md:350`).<br>**Effect:** only two of the incident's three review results can be traced from the row. | Insert "→ first FINAL issues (dispatch 1916; nested record 135; parent 1932)" between 1215/1230 and 1938. Extend the evidence range to cover `06-session:131-140`. |
| P5-05 | MINOR | accuracy-1: 7; tracing-1: 1; structure-1: 7; content-1: out-of-lens (c) | synth-01:11, 15 | **What is wrong:** the research question names `/sc:workflow` and `/sc:implement`, but the cited anchors (task file :64-75; deck :14-64) do not name them. A grep of task lines 60-77 for those command names returns 0. The original wording is at `BUILD-REQUEST.md:12` ("in sc:workflow and sc:implement"), which is not cited. | Add `BUILD-REQUEST.md:12` to the Section 1 Evidence line. |
| P5-06 | MINOR | structure-1: 10. Contradicted by content-1 check 11 PASS (resolved at C2). | synth-01:13 | **What is wrong:** the template field `**Trigger:** [what prompted this research]` (`tech-research/SKILL.md:1336`) is renamed "Trigger and deliverable" and filled with sampling-method and deliverable text. The actual trigger, "The user reports fixes leading to more failures and wants causal analysis" (`BUILD-REQUEST.md:14`), appears nowhere in Section 1. | Restore the `**Trigger:**` label, state the user-reported trigger with the `BUILD-REQUEST.md:14` citation, and keep the method and deliverable sentence as a separate line. |
| P5-07 | MINOR | accuracy-1: 8; structure-1: 8 | synth-01:52 | **What is wrong:** the paragraph on work-family clustering, modification-time selection and "not a prevalence estimate" has no citation; the nearest Evidence line (:50) cites only the observation windows.<br>**Support that exists:** `research/evidence-deck.md:105` ("must not be reported as a measured failure rate among 30 comparable operational runs") and `:662`. | Add `**Evidence:** research/evidence-deck.md:105,662`. |
| P5-08 | MINOR | accuracy-1: 9. Contradicted by tracing-1 synth-03 check 4 PASS (resolved at C6). | synth-03:83 | **What is wrong:** "does not authorize … external publication" is attributed to `research/web-01-gap-applicability.md:127-150`. A case-insensitive grep of those lines for "publication" or "publish" returns 0.<br>**Actual source:** the limit is in the task overview at task file line 68: "Do not … commit, push, publish externally …". The reviewer cited line 69; the verified line is 68. | Add task file line 68 as the source for the publication limit, or drop "external publication" from the attributed sentence. |
| P5-09 | IMPORTANT | tracing-1: 3. Contradicted by accuracy-1 synth-01 and synth-02 check 10 PASS (resolved at C7). | synth-01:65 (CI row), :148 (2.6 CI row); synth-02:82 (Key Takeaway CI row) | **Source takeaways (verified in the case report):**<br>- The orchestrator prematurely said every review note was applied (record 791) before the calibrator reported that the 18 earlier findings were not individually checked (801) (`research/04-session-43582de1.md:102` table rows 791/801, and :240 mechanism 3).<br>- "16 fixed, 2 partial" was one reviewer's intermediate assessment, which debate corrected (`04-session` Key takeaways :114-118 area).<br>- Reviewer 1 initially returned "ready with notes" (:244 mechanism 5).<br>- The deck repeats this at `evidence-deck.md:280`.<br>**Absence check:** a grep of synth-01/02 for 791, "prematur", "ready with notes", "16 fixed" and "individually" finds nothing relevant. The coverage matrices present CI coverage as complete, with no exclusion rationale. The analogous Orca 13/3 correction is retained, so the omission is asymmetric. | Represent these findings in the synth-01 2.2 CI row and/or synth-02 gap row 7 (citing `04-session:102,114-118,240,244` and `evidence-deck.md:280`), and add them to both coverage matrices. Otherwise record an explicit exclusion with rationale in both matrices. |
| P5-10 | MINOR | tracing-1: 4; structure-1: 4 (monitor-clause difference resolved at C4) | synth-02:50 (gap row 1) | **What is wrong:** the row cites only `evidence-deck.md:585-598`. That range (re-read) has no row supporting "CI presence checks admit semantically wrong edits". Its CI rows concern unasserted search arguments and a one-sided exemption. The support is `evidence-deck.md:505` ("Half-edited advisory meaning passes").<br>**Monitor clause:** "Monitor structural checks do not cover the later behavioral counterexamples" is only indirectly supported by :593 (path-specific error handling). Its direct anchor is `evidence-deck.md:312` ("structural checks pass. Behavioral/job-wiring tests are deferred"). | Add `evidence-deck.md:505` and `:312` to the row's Notes citation. |
| P5-11 | MINOR | tracing-1: 5; structure-1: 5 | synth-02:52 (gap row 3) | **What is wrong:** the claim "Credential task QA softens a known literal lint condition before acceptance; FINAL applies the literal condition" is cited to `gaps-and-questions.md:29-35,57-59` and `research/scope-rules.md:64-77`. Neither states the softening: grep for soft or relax in scope-rules 64-77 returns 0, and gaps 57-59 are causal, runtime and Orca limits.<br>**Support that exists:** `evidence-deck.md:350,558,596` and `06-session:156-162`. | Add `evidence-deck.md:558,596` and `research/06-session-0690ee9f.md:156-175`. |
| P5-12 | MINOR | tracing-1: 6; structure-1: 6 | synth-02:55 (gap row 6) | **What is wrong:** the row cites only `evidence-deck.md:564-569`. That range records the Task 10 overreach, the missing FINAL and the rubric change, but not that the ledger "retains a compliant completion". That fact is at `06-session:381` (`T6: complete verdict=compliant`, no `T6: Ruling:`). The documentation wrong-task rejection clause has no anchor at all; the support is deck :244 or `03-session:173-178`, per tracing-1. | Add `research/06-session-0690ee9f.md:381` and `evidence-deck.md:244` (or `research/03-session-6f744b87.md:173-178`). |
| P5-13 | IMPORTANT | content-1: 1. Contradicted by content-2 check 9 PASS, which was partition-limited and deferred (resolved at C3). | synth-02 §4 (:48-61); synth-06 §9 (:13-34); coverage rows synth-01:145, synth-02:79 | **Rule:** checklist item 9 requires stale documentation to be surfaced "in Sections 4 or 9" (`tech-research/SKILL.md:925-937`).<br>**Missing items:** the case lists three stale items (`research/01-session-ac2cd1fd.md:356`), and the deck repeats them (`evidence-deck.md:855-863`: "Internally inconsistent review closure summaries" and "Condensed findings that omit details retained in original returned reviews").<br>- The Orca 13/3 versus 14/2 closure error appears only in Section 2.5 (synth-01:128).<br>- The condensed persisted targeted verdict (`01-session:81,253`) appears nowhere. A grep of the synthesis files for "condens" finds only unrelated synth-06 lines.<br>**Overclaim:** synth-01:141 says exclusions are "explicit rather than silent", but neither item is represented or excluded. | Add both items to a Section 4 row (for example, extend synth-02:57 to cover persisted summaries and verdicts that drop detail), citing `01-session:81,90-103,253` and `evidence-deck.md:858-859`. Alternatively add them to Section 9. Update the Orca coverage rows. When fixing, check all nine deck items at `:855-863` against Sections 4 and 9 and record each placement. |
| P5-14 | IMPORTANT | content-1: 2 (IMPORTANT); content-2: 2 (IMPORTANT) | synth-02:55 (row 6), :58 (row 9); synth-05 §8 Phases 1-3 (:45-91); coverage table synth-05:115, 118 | **Rule:** check 7 requires gaps in S4 to be addressed in S8 (`tech-research/SKILL.md:925-937`).<br>**What is wrong:** two gaps have neither an S8 step nor an exclusion reason:<br>- Row 6: consent, authorized repair scope and ruling-record alignment, including the Task 10 overreach at record 2028.<br>- Row 9: the `head-moved` label misread as actual HEAD movement.<br>**Nearest content:** they appear only in the §8 coverage table (synth-05:115 "missing checkpoint classification", :118 "repair-authority overreach"). The closest step (synth-05:76) covers only the oracle and rendering. | Add research-only, unexecuted, approval-bounded Phase 3 rows for both gaps (binding row 6 to `evidence-deck.md:564-569` and row 9 to `:631,709,729`). Otherwise state in synth-02 Notes or synth-05 why no discriminating check applies (for example, "observed authority/bookkeeping event, not a ranked cause", consistent with `synth-04:280`). |
| P5-15 | MINOR | content-1: 3 | synth-01:69, synth-02:69, synth-01:48 | **What is wrong:** the content rule says "Tables over prose whenever presenting multi-item data" (`tech-research/SKILL.md:1598`).<br>- synth-01:69 lists seven or more distinct controls in one paragraph.<br>- synth-02:69 lists four controls in prose.<br>- synth-01:48 gives two cases' observation-window boundaries in prose. | Convert the control lists to a Control / Observed evidence / What it challenges / Limit table (as in `evidence-deck.md:645-658`), and put the two windows into a small boundary table or the 2.1 table. |
| P5-16 | MINOR | qualitative-1: 3. Contradicted by tracing-1 synth-03 check 3 PASS (resolved at C6). | synth-03:22 (§5.1 row "CI planning weaknesses and live runner behavior") | **What is wrong:** the row attributes unverified runner "permissions, cancellation or timeout behavior" to the CI planning case. A grep of `research/04-session-43582de1.md` for cancel or timeout returns 0. These unknowns come from the monitor case: `research/05-session-e002bed2.md:292-293` ("Real GitHub permissions, dispatch expression behavior, runner cancellation behavior and queue behavior remain unverified…"). | Split or reword the row: keep the CI implementation-failure unknown under CI, and attribute the runner unknowns to the monitor workflow, citing `05-session:292-293`. |

### Deduplicated findings register: partition 2 (synth-04, synth-05, synth-06, cards)

| ID | Severity | Origin lenses (report: issue) | Location | Verified issue and evidence | Required correction |
|---|---|---|---|---|---|
| P5-17 | IMPORTANT | accuracy-2: 5 (MINOR); tracing-2: 4 (IMPORTANT); structure-2: 5 (MINOR); content-2: 1 (IMPORTANT); qualitative-2: 1 (IMPORTANT) | synth-04:286, 290, 293; synth-05:68, 72 | **What is wrong:** synth-04:286 says "Step-level targets are in Section 8". That is false for two of its steps:<br>(a) Order 1 and Option A replay the monitor (synth-04:61, 67, 290), but synth-05's "Check what acceptance actually proves" row (:72) lists only the oracle, Orca planning, CI and the deck. No monitor input appears.<br>(b) Order 4 (:293, extending C-001 labels to newly selected sessions) has no Section 8 row.<br>(c) Qualified sub-claim from qualitative-2: synth-05:68 says its rows are "not an execution sequence" and lists them in card order, so the assembled plan does not carry 7.6's recommended order.<br>**Why it happened:** synth-04:326 discloses that its author read only synth-05 lines 1-40. File times confirm synth-05 (2026-10-23 22:17) predates synth-04 (2026-10-24 01:03). | Do either of the following, keeping every row UNEXECUTED and approval-bounded:<br>(i) Add the monitor context to synth-05 row 1 (record 585 workflow, deferred Task 14 tests; `evidence-deck.md:312`; `05-session` §§2 and 4). Add a synth-05 row for order 4 marked "needs user scope decision". Optionally add a priority column citing synth-04 7.6.<br>(ii) Reword synth-04:286 to say which orders have Section 8 targets, that order 4 maps to Open Question 1 (synth-06:15), and that 7.6 alone governs order. |
| P5-18 | IMPORTANT | tracing-2: 5, 6 (IMPORTANT); content-2: 3 (IMPORTANT); qualitative-2: 2 (IMPORTANT) | synth-04 Opposition rows :58, 85, 112, 139, 163; §7.4 :257-269; §7.7 note :311; synth-05:88 | **What is wrong:** six screened controls at `evidence-deck.md:650-655` (re-read) appear in no partition-2 option, ranking caution or plan row:<br>- Session 10 Task 4 (missing comment corrected, compliant re-review)<br>- Session 17 Task 8 (real deviation corrected)<br>- Session 17 FINAL ("Real restore-basename bug … corrected", which challenges "Every FINAL issue is cosmetic")<br>- Session 09<br>- Session 19<br>- Sessions 13/14 (authorized plan corrections without semantic re-review)<br>**Self-referential claim:** synth-04:311 says these controls "reach this component through the evidence deck's counterexample table … which is cited here", but that sentence is the only citation of the table in synth-04.<br>**Plan row:** synth-05:88 lists only Orca, the oracle, monitor Tasks 10/11 and the initial credential package. | Add each relevant control, with its deck anchor and the limit stated there, to the Opposition row of the candidate it challenges. At minimum: Session 17 FINAL under D; Sessions 10 and 17 one-repair convergence under A, B and E; Sessions 13/14 where they bear on the planning claims of A, B or C. Add them to §7.4 if they constrain an interaction.<br>Extend synth-05:88 with Session 10 Task 4, Session 17 Task 8 and FINAL, and Sessions 13/14.<br>Replace :311 with this per-control treatment, or with an explicit exclusion rationale for each control.<br>Do not re-rank and do not imply the debate weighed them (see flags). |
| P5-19 | IMPORTANT | accuracy-2: 1 (MINOR); qualitative-2: 3 (IMPORTANT) | synth-04:215 (7.1 rank 5) versus :141, :182 | **What is wrong:** the rank-5 justification says "Narrow reach in one work family" and cites `ADV/debate-transcript.md:381,384`. Line 381 says only "Credential packages remain one work family".<br>**Conflicting text in synth-04 itself:** Option D's Scope says "two selected sessions and three package/task contexts" (:141), and the comparison table says "Credential (one work family), documentation baseline" (:182).<br>**Refactor plan:** the V4 row says "concentrated in credential/documentation work" (`ADV/refactor-plan.md:33`; the reviewer cited :32, which is the V5 row). | Reword to "Narrow reach: one credential work family plus one documentation-baseline context; some evidence explains attribution or a halt rather than the repeat (`ADV/debate-transcript.md:381,384`; `ADV/refactor-plan.md:33`)". Wording only: the rank position is unchanged. |
| P5-20 | MINOR | accuracy-2: 2 | synth-04:240 | **What is wrong:** the sentence says the reviewed refactor plan "cited the direct continuation evidence and the V4 advocate's own reversal (`ADV/refactor-plan.md:32`; …)". Line 32 (the V5 row) states only the continuation directness ("this directness breaks the narrow-reach comparison with V4 provisionally"). The reversal is at `ADV/debate-transcript.md:384-385`, inside the V4 Round 2 block (:364-404). | Attribute only the continuation rationale to `refactor-plan.md:32`, and cite the V4 reversal separately to the transcript. |
| P5-21 | MINOR | accuracy-2: 3; structure-2: 3 | synth-04:58 (Option A Opposition) | **What is wrong:** the clause "The credential proof-only rejection happened while delivery already met the lint criterion" is cited to `synthesis/hypothesis-01.md` §6 and `evidence-deck.md:647-648`.<br>- Card 1 mentions "credential" only at :223, its Evidence Trail, so §6 (:93-109) has no credential text.<br>- Deck 647-648 are the oracle and monitor rows.<br>**Support that exists:** `evidence-deck.md:389` ("Delivery already met the lint criterion"), `:595` ("Delivery criterion held") and `:649`. | Add `research/evidence-deck.md:389,595` (or :649) for the credential clause, keeping the existing anchors for the oracle and monitor clauses. |
| P5-22 | MINOR | accuracy-2: 4; structure-2: 4; tracing-2: 3 | synth-04:90 (Option B "Against"), :213 (rank 3) | **What is wrong:** the anti-V2 position is attributed to "the V3, V4 and V5 advocates", but only :129 (V3 Round 1 block 105-147), :343 (V3 Round 2 block 324-363) and :425 (V5 Round 2 block 405-445) are cited. No V4 anchor is given.<br>**V4 positions that exist:** :168 (V4 Round 1 block 148-190, "Most later monitor faults already existed…"), :379 ("Retained siblings are not introductions; most later monitor faults preexist repair") and :385 (V3 above V2), both in the V4 Round 2 block 364-404. | Add `ADV/debate-transcript.md:168,379` (and :385 where the V3-over-V2 reason is used) at :90 and :213. |
| P5-23 | IMPORTANT | tracing-2: 1 | synth-04:64 | **What is wrong:** planning log 943/944 is listed among plans that "passed structural checks and still received substantive semantic findings". The source shows otherwise: `research/01-session-ac2cd1fd.md:85` says "943/944 … Structural gate passes", followed by 946 "NOT CHECKED: v4 has had no review since this edit" (:86). V4 received no semantic review, which is the unreviewed endpoint stated at synth-06 Q5 (:19). This claim originates in synth-04: a grep of the cards and variants for "943" finds none. | Remove 943/944 from that list, or state that v4 passed the structural gate and was never semantically reviewed. |
| P5-24 | MINOR | tracing-2: 2 | synth-04:67 | **What is wrong:** "Orca v1-v4 reconstructable … with matching hashes" overstates the evidence. `01-session:323` says only "The first two reconstructed hashes match the review snapshots, and the final reconstructed hash matches the live plan". V3 has no independent comparison target. The claim originates in synth-04 (no card or variant contains "matching hash"). | State that v1, v2 and v4 match their snapshot or live comparisons and that v3 is reconstructed without an independent match. |
| P5-25 | IMPORTANT | accuracy-2: 7 (MINOR); tracing-2: 8 (IMPORTANT); structure-2: 7 (MINOR); content-2: 4 (IMPORTANT); qualitative-2: 5 (IMPORTANT) | synth-06:51, 52, 57, 115-119, 123-128, 154, 190, 220, 223, 224 | **What is wrong:** the 2026-10-23T22:14:30Z Evidence Trail snapshot now makes false statements about named partition-2 inputs:<br>- synth-04 is "absent" and synthesis/ holds 10 files (:51, 128, 223). Observed: 11 files; synth-04 is persisted (`synth-04:339-341`).<br>- hypothesis-04 and -05 carry a "debate pending" header (:123-124). Observed: every card header reads "Post-debate format-only presentation", and "debate pending" survives only as quoted provenance at `hypothesis-04.md:185` and `hypothesis-05.md:183`.<br>- Card ten-section format acceptance is "unresolved" (:126, 220). Observed: all five cards have ten chapters and §10.5 records.<br>- qa/ has 191 files and the intake is an "unfinished administrative skeleton" (:52, 154, 190). Observed: 202 files, and `qa/synthesis-component-intake.md` reads "Status: Complete … five updated author returns persisted, zero pending".<br>**Why the disclosure is not enough:** the snapshot is labelled, and a refresh requirement is stated at :227, but the template requires the Evidence Trail to list all files produced. | Append dated superseding rows to 10.1, 10.4, 10.6 and 10.8 from a new observed enumeration made at fix time. Counts change as qa/ grows (this report and the fix log add files), so re-derive them then. Record synth-04 as present and parent-persisted (gate pending); the cards as format-only presentations with §10.5 records (the immutable variants remain the debated identities); the intake as Complete; and the Phase 5 QA files. Keep the 22:14:30Z rows labelled historical; do not rewrite them. |
| P5-26 | MINOR | tracing-2: 7 | synth-06:145, 146 | **What is wrong:** `ADV/plan-review-evidence.md` is credited with the "original canonical-review failure, identity correction and targeted passing re-review". That file contains neither reviewer id (a grep for `aba0ed57` or `a815d047` returns 0); its body is the transcript-input PASS, identity notes and the source-directory guard (:9-17). The FAIL (`agent-aba0ed57846538ad4.jsonl` record 79) and the re-review PASS (`agent-a815d047710b89c22.jsonl` record 38) are at `ADV/merge-log.md:161-163`, and the merge-log row (:146) omits them. | Move the canonical-review FAIL and targeted re-review to the merge-log row. Describe plan-review-evidence as the transcript-input PASS, identity notes and source-directory guard. |
| P5-27 | MINOR | accuracy-2: 6; structure-2: 1; content-2: 7 (out-of-lens) | synth-06 §10 (:40-227) | **What is wrong:** the Report Structure's Evidence Trail requires `### Codebase Research`, `### Web Research` (File / Topic) and `### Gaps Log` (`tech-research/SKILL.md:1471-1487`, re-read). synth-06 uses custom 10.1-10.8 instead and states no adaptation (its header at :5 claims the template unchanged). `web-01-gap-applicability.md` sits in the 10.2 research table under an Agent Type column (:83), and `gaps-and-questions.md` appears only in 10.7 (:206). | Add the three template subsections (the custom 10.x tables may stay beneath them). Put web-01 under Web Research as the reasoned-N/A record with zero external findings, and list `gaps-and-questions.md` under Gaps Log. Alternatively, state the adaptation explicitly in the header, as synth-04:5 does. |
| P5-28 | MINOR | structure-2: 6 | `synthesis/hypothesis-01.md` through `hypothesis-05.md`, `## 1. Problem Statement` (each card at about lines 27-33) | **What is wrong:** each card's chapter 1 contains only `### Original Hypothesis`. It has none of the template's question / why it matters / trigger bullets (`tech-research/SKILL.md:1334-1336`) and no N/A justification. Chapters 3-6 and 8 of the same cards do justify their N/A portions. | Add a presentation-only note to each chapter 1: either a reasoned N/A or a pointer to the shared research question already in the package. Leave every verbatim original line untouched and re-run the exact-once preservation check against `ADV/variant-N-original.md`. |
| P5-29 | MINOR | content-2: 5 | synth-04:64, 118, 145, 169, 277, 279 versus :282 | **What is wrong:** synth-04 cites `quality-gates.md:24-39`, `qa.md:82` and `managed-workspace.md:42` without naming the layer read, although its own rule at :282 says "Any current-rule statement must name the exact layer it read". Verified: the pin text is at line 42 in `/config/workspace/IronClaude/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and at line 43 in the installed `/config/.claude/skills/sc-implement-protocol/refs/managed-workspace.md`. The anchor is therefore wrong for one layer. `research/scope-rules.md:45` names the source layer explicitly. | Prefix each current-rule citation with its layer, for example `/config/workspace/IronClaude/src/superclaude/skills/...`, as `research/scope-rules.md:45` does. |
| P5-30 | MINOR | content-2: 6 | synth-06:32 (Q18) versus :36 (Question sources) | **What is wrong:** Q18 (task-size contribution) has no basis in the declared sources. A grep of `evidence-deck.md`, `gaps-and-questions.md`, `scope-rules.md` and `return-contract.md` for "task size" or "task-size" returns nothing. Its basis is the debate concession at `ADV/debate-transcript.md:49` ("task size is an observed amplifier, not an isolated cause"). | Add `reviews/adversarial/adversarial/debate-transcript.md:49` to the Question sources line. |
| P5-31 | IMPORTANT | qualitative-2: 4 | synth-04:74, 86, 87, 181, 211-215 | **What is wrong:** synth-04 is internally inconsistent about who owns the "repair left a sibling failure" transition, and it departs from the debated original.<br>- The immutable `ADV/variant-2-original.md:10` says the repair can "introduce a new defect or leave a sibling failure intact".<br>- Its Scope says "Two outcomes must remain separate: demonstrably introduced connected defects, and incomplete coverage of an existing failure family" (variant-2 Scope section).<br>- Debate S-002 organizes "V2 introduction/retained siblings" separately (`ADV/debate-transcript.md`, S-002 line in the 266-273 block), and C-003 limits "introduction" to before/after evidence.<br>- Card 1 assigns "fails to cover sibling paths" to candidate two (`hypothesis-01.md:105`).<br>**Inside synth-04:** the Option B Description (:74) includes siblings. The Alternatives row (:86) calls an incomplete fix "a different explanation from introduction". The Scope row (:87) and the comparison row (:181) cover only absent-before/present-after introduction. The 7.1 override column assigns retained siblings to no one. | In synth-04 only, state that retained siblings are V2's separately labelled second outcome (S-002), never counted as introductions (C-003). Align the Option B Scope, Alternatives, the comparison row and the 7.1 override column with that. Do not edit any card or variant (see flags). |
| P5-32 | MINOR | qualitative-2: 6 | synth-04:69, 204, 290 versus :236 | **What is wrong:** synth-04 says "V1 first is the only unanimous placement" (:204; also :69 and :290 "the only unanimous placement"). Its own pairwise table derives a second 5-of-5 placement: "V1, V2 and V3 each above both V4 and V5", labelled derived (:236). | Say "the only unanimous exact rank position" at :69, :204 and :290. Optionally mention the derived top-three/bottom-two split in the Rationale, labelled as derived from the five recorded orders and not stated in the debate. |
| P5-33 | MINOR | qualitative-2: 7 | synth-04:148 (Option D Reuse row) | **What is wrong:** synth-04 says "A fresh Read of the formerly archived `t10-markdownlint.log` returned 'file does not exist'". Card 4 scopes that Read to "under the recorded Coder worktree" (`hypothesis-04.md:151`). A file of that name exists now at `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log` (1006 bytes; `ls` confirmed). Dropping the location qualifier understates the available evidence. Its identity with the historical log is not hash-verified. | Restore the location qualifier and add: "Candidate current location observed at `<path>`; identity with the historical log not hash-verified; availability to be confirmed before any approved replay." Leave card 4 §9 verbatim and do not certify the file. |

### Raw-to-group traceability

| Report | Raw issue → group |
|---|---|
| accuracy-1 | 1→P5-01, 2→P5-01, 3→P5-01, 4→P5-02, 5→P5-03, 6→P5-04, 7→P5-05, 8→P5-07, 9→P5-08 |
| accuracy-2 | 1→P5-19, 2→P5-20, 3→P5-21, 4→P5-22, 5→P5-17, 6→P5-27, 7→P5-25 |
| tracing-1 | 1→P5-05, 2→P5-04, 3→P5-09, 4→P5-10, 5→P5-11, 6→P5-12 |
| tracing-2 | 1→P5-23, 2→P5-24, 3→P5-22, 4→P5-17, 5→P5-18, 6→P5-18, 7→P5-26, 8→P5-25 |
| structure-1 | 1→P5-02, 2→P5-01, 3→P5-03, 4→P5-10, 5→P5-11, 6→P5-12, 7→P5-05, 8→P5-07, 9→P5-04, 10→P5-06 |
| structure-2 | 1→P5-27, 2→P5-01, 3→P5-21, 4→P5-22, 5→P5-17, 6→P5-28, 7→P5-25 |
| content-1 | 1→P5-13, 2→P5-14, 3→P5-15, 4→P5-01; out-of-lens (a)→P5-02, (b)→P5-03, (c)→P5-05 |
| content-2 | 1→P5-17, 2→P5-14, 3→P5-18, 4→P5-25, 5→P5-29, 6→P5-30, 7→P5-27 |
| qualitative-1 | 1→P5-04, 2→P5-03, 3→P5-16 |
| qualitative-2 | 1→P5-17, 2→P5-18, 3→P5-19, 4→P5-31, 5→P5-25, 6→P5-32, 7→P5-33 |

### Claims adjusted after verification (raw text preserved in the source reports)

1. **accuracy-1 issue 9:** the publication limit is at task file line **68**, not 69 (verified by grep). The finding stands.
2. **qualitative-2 issue 3:** the refactor-plan wording "concentrated in credential/documentation work" is at `ADV/refactor-plan.md:33` (the V4 row), not :32, which is the V5 row (verified by grep). The finding stands.
3. **structure-1 issue 4 and tracing-1 issue 4** differ on whether deck 585-598 supports the monitor clause. Resolved at C4: partial support at :593, direct anchor :312.
4. **qualitative-1 issue 2, sub-claim (c):** "all rows rated Important without discrimination" is an evaluative proportionality judgment. It is neither verified wrong nor mechanically provable. It is retained inside P5-03 as "re-rate or state the basis". The non-template value and the inconsistent row-59 labelling parts are fully verified.
5. **qualitative-2 issue 1(a):** the sequencing mismatch. synth-05:68 explicitly disclaims sequence, and synth-04:286 claims only that targets, not order, live in Section 8. So 1(a) is not an independent contradiction. It is retained as a sub-part of P5-17 because the assembled Section 8 will not reflect Section 7's recommended order unless one of the two correction options is applied.
6. **content-2 summary counts** say "Checks passed: 6 of 11", but its Items table shows 7 PASS rows (8, 9, 10, S1, S3, S4, S5) and 4 FAIL rows (7, 11, 12, S2). The literal FAIL verdict is unaffected. The table rows govern the PASS identities below.

## Cross-Partition and Cross-Lens Contradictions

| # | Conflict | Sources | Resolution by evidence |
|---|---|---|---|
| C1 | Are the handoff tables and stale status lines a defect? | Defect: accuracy-1 1-3, structure-1 2, content-1 4, structure-2 2. Not counted: tracing-1 Self-Audit ("delivery receipt elsewhere"), qualitative-1 Self-Audit, qualitative-2 check 15. | **Defect (P5-01).** The persistence is real and recorded externally, so the contrary reviewers are right that nothing failed to persist. But the tables are not report content (`tech-research/SKILL.md:810`), they make false present-tense statements (synth-02:93), and five components have no in-file receipt. External receipts do not stop assembly from copying them. The correction keeps the producers' text, which meets the contrary reviewers' preservation concern. |
| C2 | Is the Section 1 Trigger present? | content-1 check 11 PASS ("§1 question/why/trigger"); structure-1 issue 10 FAIL | **structure-1 is correct (P5-06).** The label reads "Trigger and deliverable" and the text describes the sampling method. The user-reported trigger at `BUILD-REQUEST.md:14` is absent. content-1 checked that a label was present, not what it says. |
| C3 | Stale documentation placement (check 9) | content-1 issue 1 FAIL; content-2 check 9 "PASS (partition-limited)", which explicitly left the decision to consolidation | **FAIL (P5-13).** The check text requires "Sections 4 or 9" (`tech-research/SKILL.md:925-937`). The closure-count item is only in Section 2. The condensed-verdict item is in no section, including synth-06 §9 (grep). |
| C4 | Gap row 1, monitor clause support | structure-1 issue 4 (range covers monitor mechanisms; only the CI clause is unsupported); tracing-1 issue 4 (both clauses unsupported) | **Partly both.** Deck 585-598 (re-read) has a monitor path-specific error-handling row (:593) but nothing on structural checks. The direct anchor for the structural-check wording is :312. Both reviewers agree the CI clause is unsupported, and :505 is the correct anchor. One merged finding (P5-10). |
| C5 | First failed follow-up FINAL record number | Deck :350 "1932 issues"; case 06 :133-137 dispatch 1916, nested record 135; qualitative-1 Limits flags a difference | **No contradiction.** These are three facets of one event: dispatch (1916), nested conclusion (record 135, 20:20:21Z) and the parent receiving the result (1932, 20:20:36.570Z per tracing-1's read-only JSONL check). P5-04's correction cites all three. |
| C6 | synth-03 clean versus defective | tracing-1: synth-03 PASS (checks 3, 4: web-01 :127-150 "re-read and confirmed"); accuracy-1 issue 9; qualitative-1 issue 3 | **synth-03 has defects.** The web-01 127-150 grep for publication returns 0 (P5-08). The CI case has 0 cancel or timeout matches, and the monitor case :292-293 holds them (P5-16). The tracing-1 synth-03 PASS rows on checks 3 and 4 are not carried as protected PASS identities. |
| C7 | CI key-takeaway coverage | accuracy-1 synth-01 and synth-02 check 10 PASS; tracing-1 issue 3 | **Missing (P5-09).** Verified in `04-session:102,114-118,240,244`. The synth-01/02 grep finds nothing relevant. The accuracy-1 check-10 PASS rows are not protected. |
| C8 | Are partition-2 controls preserved? | accuracy-2 synth-04 check 10 and S4 PASS, synth-05 S4 PASS ("Controls are preserved (line 88)"); tracing-2 5-6, content-2 3, qualitative-2 2 | **Not preserved (P5-18).** Deck :650-655 controls are absent from synth-04 and synth-05:88. accuracy-2 checked only the in-case controls. |
| C9 | Severity disagreements | P5-01 (I vs M), P5-17 (I vs M), P5-19 (I vs M), P5-25 (I vs M) | The highest severity is kept per `task/SKILL.md:357`: IMPORTANT for all four. |
| C10 | Gap-row citations | accuracy-1 synth-02 check 4 PASS ("every gap row carries a citation; sampled ranges contain stated facts"); tracing-1 4-6, structure-1 4-6 | **Defects (P5-10 to P5-12).** accuracy-1 sampled rows; the clause-level misses are verified above. |
| C11 | Card header state | synth-06:123-124 ("debate pending" header); accuracy-2 and tracing-2 (headers now post-debate) | **Current disk wins (P5-25).** Every card header reads "Post-debate format-only presentation". "debate pending" survives only as quoted provenance (`hypothesis-04.md:185`, `hypothesis-05.md:183`). |
| C12 | Rank-5 reach | synth-04:215 versus synth-04:141, :182 and `ADV/refactor-plan.md:33` | **Resolved to the broader statement (P5-19).** The transcript limits "one work family" to the credential packages only (:381). |

No conflict needed an unresolved two-source marker.

## Correction Scoping and Re-debate Flags

- **Immutable identities.** The debated identities are `ADV/variant-1..5-original.md`. Step 5.24 must not edit them, the debate transcript, any other `ADV/` artifact or historical research evidence. Card edits are limited to the presentation-only chapter-1 note (P5-28), followed by the exact-once preservation recheck.
- **Origins.** The synth-04 claims corrected by P5-19, P5-23 and P5-24 originate in synth-04. A grep of the cards and variants for "943", "matching hash" and "one work family" finds no source wording, so correcting synth-04 does not diverge from any card.
- **Conditions that would require a real re-debate.** A correction that crosses one of these conditions must be flagged for re-debate through the actual skill and not applied:
  - **P5-31:** assigning retained siblings to any candidate other than V2, or merging them into "introduction", would change V2's debated scope. The specified correction restores the original variant-2 wording and S-002, so it needs no re-debate.
  - **P5-18:** adding screened controls as counterevidence is a synthesis fidelity correction. Re-ranking on the strength of those controls, or claiming the advocates weighed them, would be a new causal judgment that the existing debate does not cover.
  - **P5-19 and P5-32:** wording only. Any change to a rank position or to the displayed order V1 > V3 > V2 > V5 > V4 is out of bounds.
  - **P5-17 and P5-14:** added Section 8 rows must stay UNEXECUTED, research-only and approval-bounded. They authorize nothing.
- **Delivery receipts are not approvals.** Parent Persistence Records added for P5-01 record delivery only and must not state or imply any gate verdict.
- **Single fixer.** All 33 groups go to ONE fixer in Step 5.24, with no concurrent writer, no production edits and no deletion.

## Original PASS and Failure Sets (cycle 0, frozen)

### Baseline identity and counter

- **Gate:** Phase 5 synthesis gate. **Cycle:** 0 (before any fix). **Cap:** at most two fix cycles (`tech-research/SKILL.md:515`; task Step 5.27).
- **Reviewer set:** the ten reports above, bound by SHA-256 prefix.
- **Target set:** the eleven synthesis files above, bound by SHA-256 prefix.
- **Deduplicated failure count:** |F0| = 33 (11 IMPORTANT, 22 MINOR).

### Report-level sets

- **PASS set:** none (0 of 10).
- **FAIL set:** all ten reports listed in the inventory.

### Passing check identities per report (file + row)

"Protected" rows are the cycle-0 PASS identities for the regression guard. Rows marked "not protected" are literal reviewer PASS rows that a verified consolidation finding contradicts. They are recorded for auditability but must not trigger a regression halt when later re-checked as FAIL.

| Report | Literal PASS rows: protected | Literal PASS rows: not protected (contradicting group) |
|---|---|---|
| accuracy-1 | synth-01 #2; synth-01 #3; synth-02 #3; synth-03 #2; synth-03 #10 | synth-01 #10 (P5-09, P5-13); synth-02 #4 (P5-10, P5-11, P5-12); synth-02 #10 (P5-09, P5-13); synth-03 #3 (P5-16) |
| accuracy-2 | synth-04 #1, #2, #5, S3; synth-05 #1, #2, #3, #4, #6, #10; synth-06 #2, S4 | synth-04 #10 (P5-18); synth-04 S1 (P5-31); synth-04 S2, literal "PASS (except Issues 2 and 4)" (P5-19, P5-20, P5-22); synth-04 S4 (P5-18); synth-05 S4 (P5-18); synth-06 #4 (P5-30); synth-06 #10 (P5-13) |
| tracing-1 | synth-01 #7, #8, #9, B; synth-02 #3, #8, B; synth-03 #7, #8, #9, #10, B | synth-02 #7 (P5-14); synth-02 #9 (P5-13); synth-03 #3 (P5-16); synth-03 #4 (P5-08) |
| tracing-2 | synth-04 #8, #9, T3; synth-05 #6, #8, #9, #10, T4, T3; synth-06 T3 | synth-06 #9 (P5-13); synth-06 #10 (P5-30); synth-06 T7, "PASS at snapshot" (P5-25) |
| structure-1 | #5, #6 | #3 (P5-16) |
| structure-2 | #3, #6, #10, #11 | #4 (P5-23, P5-24); #12 (P5-25) |
| content-1 | #8, #12 | none |
| content-2 | #8, #10, S3, S4, S5 | #9 (P5-13); S1 (P5-19, P5-20, P5-22) |
| qualitative-1 | #1, #3, #5, #6, #7, #9, #10, #11, #12, #13 | none |
| qualitative-2 | #1, #5, #6, #8, #9, #12, #14, #16 | #11 (P5-23, P5-24); #15 (P5-01) |

N/A, "not in this lens" and FAIL rows are excluded from both columns.

### Frozen cycle-0 failure set

| ID | Severity | Primary file(s) |
|---|---|---|
| P5-01 | IMPORTANT | synth-01..06 |
| P5-02 | IMPORTANT | synth-03 |
| P5-03 | MINOR | synth-02 |
| P5-04 | MINOR | synth-01 |
| P5-05 | MINOR | synth-01 |
| P5-06 | MINOR | synth-01 |
| P5-07 | MINOR | synth-01 |
| P5-08 | MINOR | synth-03 |
| P5-09 | IMPORTANT | synth-01, synth-02 |
| P5-10 | MINOR | synth-02 |
| P5-11 | MINOR | synth-02 |
| P5-12 | MINOR | synth-02 |
| P5-13 | IMPORTANT | synth-02 (and/or synth-06), synth-01 coverage |
| P5-14 | IMPORTANT | synth-02, synth-05 |
| P5-15 | MINOR | synth-01, synth-02 |
| P5-16 | MINOR | synth-03 |
| P5-17 | IMPORTANT | synth-04, synth-05 |
| P5-18 | IMPORTANT | synth-04, synth-05 |
| P5-19 | IMPORTANT | synth-04 |
| P5-20 | MINOR | synth-04 |
| P5-21 | MINOR | synth-04 |
| P5-22 | MINOR | synth-04 |
| P5-23 | IMPORTANT | synth-04 |
| P5-24 | MINOR | synth-04 |
| P5-25 | IMPORTANT | synth-06 |
| P5-26 | MINOR | synth-06 |
| P5-27 | MINOR | synth-06 |
| P5-28 | MINOR | hypothesis-01..05 (chapter 1 only) |
| P5-29 | MINOR | synth-04 |
| P5-30 | MINOR | synth-06 |
| P5-31 | IMPORTANT | synth-04 |
| P5-32 | MINOR | synth-04 |
| P5-33 | MINOR | synth-04 |

### Subsequent-cycle comparison contract

1. **Regression first.** Re-check every protected PASS identity above against corrected sources. If one now fails, emit `Regression detected on Item X.Y — previously PASS at cycle 0, now FAIL. Halt overrides monotonicity check.` and HALT.
2. **Monotonicity next.** Compare the new deduplicated failure set (unresolved originals plus new issues) with |F0| = 33. If it does not shrink, emit `[HALT-MONOTONICITY] |F|=<n>` with the real value and HALT.
3. **Cap.** Allow at most two fix cycles. At the cap, record the remaining defects as Open Questions in `gaps-and-questions.md` and HALT assembly rather than label it PASS.
4. **Evidence standard.** Verifiers must check original and corrected claims against the sources, not against the fix log alone, and must keep cycle-specific reports separate.

## Actions Taken

- Read the Step 5.23 text and neighbouring Steps 5.13-5.27 in the task file. Read the governing format and consolidation rules (`task/SKILL.md:340-506`; `tech-research/SKILL.md:495-524` plus the checklist and template lines cited above).
- Read all ten reviewer reports in full and all six synthesis components in full. Read the card headers and chapter 1 of each card, plus the targeted card lines cited.
- Ran four bounded read-only batch scripts (private `mktemp` directories, cleanup traps, all `BATCH_OK`). They verified the source lines cited in this report in the case reports, evidence deck, gap register, rule map, web-01, debate transcript, refactor plan, merge log, plan-review evidence, both protocol layers, BUILD-REQUEST and task file. They also checked external-path existence, the file and QA counts, and the report and target hashes. One more single read-only grep checked the card and variant origins.
- Edited no file and created no file. Spawned no agent. Ran no test, Git, staging, archive, move, delete or publication action.

### Follow-up items outside synthesis scope (logged, not findings)

1. content-2 disclosed an accidental 5-byte file at `.claude/agent-memory/rf-qa/.probe` inside the package. I confirmed it exists (`ls`, 5 bytes, 2026-10-24 01:04). Removing it is the parent's decision; I did not delete it.
2. tracing-2 disclosed a scratch listing at `/tmp/qa_actual_list_review.txt`. It is not a package file.
3. structure-2 noted a numbering defect in the governing source (`tech-research/SKILL.md:1523` says "3 items unique to rf-qa" but numbers them 11-13 against a 12-item list). That is skill maintenance, not a synthesis fix.
4. tracing-1 noted two research-input observations: case 06 never lists parent record 1932, and case 01:296-297 cites `Source:402` for two requirements. Both concern research inputs, not assigned synthesis targets.

## Recommendations

- Proceed to Step 5.24 with ONE fixer (`rf-qa`, `fix_authorization: true`) given this file as input. It should apply all 33 groups within the scoping and re-debate conditions above and record every source-backed correction in `qa/qa-synthesis-fix-log.md`.
- Suggested fix order:
  1. The structural or assembly blockers: P5-01, P5-02, P5-27, P5-25.
  2. The cross-partition consistency groups: P5-13, P5-14, P5-17, P5-18, P5-31.
  3. The citation and wording groups.
- Then run Steps 5.25 and 5.26 with fresh verifiers, applying the comparison contract above.

## QA Complete

Verdict **FAIL**. Ten of ten reviewers literally FAIL. There are 33 unique issues (CRITICAL 0, IMPORTANT 11, MINOR 22), all verified against the actual synthesis text and sources. 0 raw issues were dropped, 4 reviewer citation details were corrected and 2 sub-claims were qualified. The cycle-0 failure set and the per-report PASS identities are frozen above. This report is returned as text for exact parent persistence at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-consolidated-findings-phase5.md`.

| Status | Result |
|---|---|
| DONE | Consolidated all ten Phase 5 synthesis-gate reports into 33 independently verified, deduplicated issues with origin lenses, the highest severities, contradiction resolutions, correction scoping and frozen cycle-0 PASS and failure sets. |
| DONE | Confirmed that all ten literal verdicts are FAIL and that the reviewed targets' hashes match the current bytes. |
| NEXT | The parent persists this exact text at the path above. Step 5.24 then runs one serialized fixer against the 33 groups. |

## Parent Persistence Record (2026-10-24)

The parent persisted this exact restricted return from current session subagents/agent-asg-consolidate-*.jsonl (latest text with this title; 297 lines, 55,696 bytes before this record) and read the Summary, both findings registers, adjustments, contradictions and correction-scoping sections. The report's "parent persistence pending" status is its original handoff state, resolved here. This record is a delivery receipt, not a gate verdict.
