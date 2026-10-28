# D: QA Verdicts and Remaining Work

**Observed:** 2026-10-23, read-only. Line numbers refer to `TASK-RESEARCH-review-loops-20261023-032537.md` (624 lines).

## 0. Headline

- **Checklist state:** only Steps 1.1 and 1.2 are checked (`- [x]` at lines 127 and 131). Steps 2.1 through 7.3 are all unchecked, even though Phase 2 to 4 work, most of Phase 5 synthesis, all five hypothesis cards and most of the debate exist on disk. The execution log (line 573) says earlier work "already occurred and remain[s] independently evidenced" and that items must be joined and verified, not backdated.
- **Frontmatter:** `status: Doing`, `completion_date: null`, `blocker_reason: null` (lines 1-40).
- **Report:** `RESEARCH-REPORT-review-loops.md` is a skeleton. Status line 5 says "In Progress". Sections 1 and 3 have text. Sections 2 and 4-10 are `{{RF_PLACEHOLDER:...}}` (lines 32, 39, 42, 45, 48, 51, 54, 57).
- **Phase findings logs are still builder boilerplate.** Phases 2-7 and Phase Gate Findings (lines 583-609) contain no execution entries.

## 1. QA verdicts per gate

### 1a. Task-file readiness (pre-execution, administrative)

| Report | Verdict | Notes |
|---|---|---|
| qa/qa-task-validation-structure-report.md | FAIL (initial) | Historical. Superseded by the verification below |
| qa/qa-task-validation-b2-report.md | FAIL (initial) | Check 4: path prefixes missing. Superseded |
| qa/qa-task-validation-consolidated-initial.md | FAIL | 3 deduplicated structural defects |
| qa/qa-task-validation-verification.md | PASS 27/27 | Fresh verifier |
| qa/qa-task-validation-consolidated.md | PASS | All 3 original issues resolved |
| qa/qa-task-research-alignment-report.md | PASS (20 claims) | |
| qa/qa-qualitative-operational-report.md | PASS | Content partition A, 15/15 |
| qa/qa-qualitative-sufficiency-report.md | FAIL | Partition B: the regression-halt message format did not match the exact-message contract (AX-2) |
| qa/qa-qualitative-fix-verification.md | PASS 8/8 | All 5 messages corrected (Steps 3.15, 5.27, 6.21, 6.32, 6.42) |
| qa/task-builder-readiness.md | **PASS** | TASK_FILE_READY. It explicitly claims no research execution |

**Open findings: none.** All initial FAILs are resolved and kept as historical records.

### 1b. Phase 3 research completeness gate (Steps 3.1-3.15, lines 189-251)

| Partition | Completeness | Cross-validation | Evidence | Gaps | Depth |
|---|---|---|---|---|---|
| A (cases 01/02) | FAIL | FAIL | PASS | PASS | PASS |
| B (cases 03/04) | FAIL | PASS | PASS | PASS | PASS |
| C (cases 05/06) | FAIL | PASS | FAIL | FAIL | PASS |

- Consolidated: `qa/qa-consolidated-findings-phase3.md` gives FAIL: 9 PASS, 6 FAIL, and 6 deduplicated findings (3 Important, 3 Minor).
- Fix: `qa/phase3-fix-log.md` was written by main as the sole writer and applies patches from `phase3-fix-patches-source.txt`. Its own header still reads "Verification pending", which is stale but is superseded by the verifications.
- Verification: `qa/phase3-fix-verification.md` PASS (6 failures, 0 remaining). `qa/phase3-fix-verification-qualitative.md` PASS.
- Decision: `phase-outputs/plans/research-gate-decision.md` **PASS**. One fix cycle took the failure set from 6 to 0, with no regression and no cap reached.
- **Open findings: none.** Bookkeeping gap: Steps 2.1-2.13 and 3.1-3.15 are unchecked, and there are no Phase 2/3 Findings entries.
- **Not evidenced:** the separate full-intensity `/task` phase gates required after Phases 2-6 (line 609). No phase-gate reviewer artifacts exist for Phases 2, 3 or 4.

### 1c. Phase 4 (Step 4.1, line 259)

- The required output `research/web-01-gap-applicability.md` is **missing**: Glob finds no `research/web-*`.
- `synthesis/synth-03-external-findings.md` records an N/A decision (status: "Complete (applicability decision; synthesis QA pending)"). It does not replace the Step 4.1 artifact. Steps 5.2 (line 271), 5.3 (line 275) and 5.4 (line 279) list web-01 as an input.
- Verdict: **INCOMPLETE**. Step 4.1 has to produce web-01 (expected: a justified N/A with a gap inventory and the local searches tried).

### 1d. Phase 5 synthesis gate (Steps 5.13-5.27, lines 313-371)

**Not started.** None of these exist:
- `qa/analyst-synthesis-accuracy-{1,2}.md`, `qa/analyst-synthesis-tracing-{1,2}.md`
- `qa/qa-synthesis-structure-{1,2}.md`, `qa/qa-synthesis-content-{1,2}.md`, `qa/qa-synthesis-qualitative-report-{1,2}.md`
- `qa/qa-consolidated-findings-phase5.md`, `qa/qa-synthesis-fix-log.md`, `qa/qa-synthesis-verification-{structural,content}.md`
- `phase-outputs/plans/synthesis-gate-decision.md`

### 1e. Phase 6 report, fidelity and anti-omission gates (lines 373-543)

**Not started.** No `qa/qa-lens-*`, `qa/qa-source-fidelity-*`, `qa/qa-anti-omission-*`, `report-gate-decision.md`, `fidelity-gate-decision.md` or `anti-omission-gate-decision.md`.

### 1f. Adversarial plan review (inside the debate)

`reviews/adversarial/adversarial/plan-review-evidence.md` records an independent PASS on the Step 4 refactor plan, with zero issues. `refactor-plan.md` "Review Status" (line 102) shows it was auto-approved by the protocol, not by the user.

## 2. Synthesis component status

| Component | Report sections | Exists | Header status | Notes |
|---|---|---|---|---|
| synth-01-problem-current-state.md | 1, 2 | Yes (92 lines) | Complete; synthesis QA pending | |
| synth-02-target-gaps.md | 3, 4 | Yes (47 lines) | Complete; QA pending | Step 5.2 input web-01 never existed. The QA gate should check this |
| synth-03-external-findings.md | 5 | Yes (17 lines) | Complete N/A; QA pending | Written without the Step 4.1 web-01 artifact |
| **synth-04-options-recommendation.md** | **6, 7** | **MISSING (confirmed)** | n/a | See below |
| synth-05-implementation-plan.md | 8 | Yes (49 lines) | Complete (proposed checks only); QA pending | |
| synth-06-questions-evidence.md | 9, 10 | Yes (49 lines) | **In Progress** | Evidence index must be refreshed after the debate and QA (Step 5.5, line 283; Step 6.1, line 379) |
| hypothesis-01..05.md | input to 6 | Yes, all 5 | Complete candidates, unranked | H1 checks prove less than requirement; H2 local repairs miss connected effects; H3 review contracts change during the loop; H4 brittle evidence/provenance handoffs; H5 late feasibility/repair-authority checks |

**What synth-04 must contain (Step 5.12, line 311):**

- Report **section 6, Options Analysis**: exactly five hypothesis assessment tables, one per card. Each covers mechanism, support, opposition, alternatives, scope, falsification and evidence strength. The template fields Effort, Risk, Reuse, Files, Pros and Cons appear as proposed investigation trade-offs or a justified N/A, never as a stand-in for causal likelihood.
- Report **section 7, Recommendation**: a ranking from most to least likely within this sample, derived from the actual debate. It also needs overlap and dependency cautions and a research-only next recommendation.
- Required inputs: all six case files, the evidence deck, scope-rules, gaps-and-questions, the five cards, `reviews/adversarial/run-evidence.md`, and every real transcript, scoring, invariant and merged artifact at its returned path.
- Prohibitions: no invented percentages, and base-selection scores must not be treated as probability. The disagreements must stay visible.
- **Debate inputs available now:** `debate-transcript.md` (lines 477-486) records every advocate placing V1 first. The plan's provisional order is **V1 > V3 > V2 > V5 > V4**, explicitly labelled non-consensus. V3-above-V2 and V4-above-V5 each have only 3/5 support, below the 4/5 two-thirds threshold. synth-04 must keep that dissent.

## 3. Debate (Step 5.11, line 307) status

| Protocol artifact | Present |
|---|---|
| input-manifest.json, variant-1..5-original.md | Yes |
| diff-analysis.md | Yes |
| debate-transcript.md (deep: R1 parallel, R2 sequential, R2.5 probe; R3 not executed because convergence was 10/10) | Yes |
| invariant-probe.md (6 categories, all ADDRESSED) | Yes |
| base-selection.md (base = Variant 4, writing quality only) | Yes |
| refactor-plan.md (8 changes; auto-approved) and plan-review-evidence.md (PASS) | Yes |
| **merge-log, merged output, final return contract** | **MISSING** |
| run-evidence.md | **Stale.** Says "Running" with Debate/Scoring/Merge/Contract "Pending", although the debate and scoring artifacts now exist (last write 05:44Z) |

Step 5.11 remaining work:
1. Dispatch the mandatory dedicated merge-executor against `refactor-plan.md`.
2. Verify the merged output, merge-log and return contract on disk.
3. Update `run-evidence.md` with the observed paths and status: `artifacts_dir` is `reviews/adversarial/adversarial/`.
4. Check the step only then.

Do not synthesize a missing debate.

## 4. Exact remaining steps to finish

### Bookkeeping before continuing (reconcile, do not backdate)
- Steps 2.1-2.13 and 3.1-3.15: verify the existing artifacts (six cases, evidence deck, scope-rules, research gate PASS) against each item's Verify clause. Then check them off and log the evidence in the Phase 2/3 Findings with honest timestamps (rule at line 575).
- Run or record the `/task` phase gates required after Phases 2, 3 and 4 (line 609), or log a blocker.
- **Step 4.1 (line 259):** create `research/web-01-gap-applicability.md`, a justified N/A consistent with synth-03.

### Phase 5 (lines 261-371)
- **5.1, 5.2, 5.3, 5.5:** outputs exist. Verify each against its Verify clause. synth-06 must move from In Progress to complete after the debate (5.5, line 283). Check 5.2 and 5.3 against web-01 once it exists.
- **5.4:** synth-05 exists. Verify it.
- **5.6-5.10:** cards exist. Verify and check them off.
- **5.11:** finish the merge-executor, merged output and return contract, and update run-evidence (section 3 above).
- **5.12:** **create synth-04** (section 2 above).
- **5.13-5.22:** ten independent report-only reviewers, run in parallel in partitions. Partition 1 covers synth-01/02/03. Partition 2 covers synth-04/05/06, the cards and the debate.
- **5.23:** consolidate into `qa/qa-consolidated-findings-phase5.md`.
- **5.24:** one serialized fixer, or a no-fix-needed entry in `qa/qa-synthesis-fix-log.md`. Re-debate any change to a card's causal meaning.
- **5.25 and 5.26:** fresh structural and content verifiers.
- **5.27:** `phase-outputs/plans/synthesis-gate-decision.md`. Order of checks: regression, then non-shrink, then a cap of 2 cycles. Use the exact halt strings.

### Phase 6 (lines 373-543): assembly, final QA, fidelity, anti-omission
- **6.1 (line 379), assembly:** exactly ONE `rf-assembler` fills `RESEARCH-REPORT-review-loops.md` from synth-01..06 in order. Build the TOC from the real headings. Include the date, depth, scope and actual file counts. Refresh section 10 from disk. Section 8 is research-only.
- **6.2-6.12, final lenses (11):**

  | Step | Lens | Reviewer |
  |---|---|---|
  | 6.2 | template-conformance | rf-qa |
  | 6.3 | internal-consistency | rf-qa |
  | 6.4 | evidence-quality | rf-qa |
  | 6.5 | completeness | rf-qa |
  | 6.6 | actionability | qualitative |
  | 6.7 | numbers-metrics | qualitative |
  | 6.8 | crossref-chain | qualitative |
  | 6.9 | domain-accuracy | qualitative |
  | 6.10 | recommendation-feasibility | qualitative |
  | 6.11 | finding-reproducibility | qualitative |
  | 6.12 | implementation-concreteness | rf-qa |

- **6.13-6.16, size additions:** reviewers for more than 1500 lines (evidence-table-integrity, causal-boundary-integrity) and more than 3000 lines (full-traceability-integrity, cross-case-generalization). Below threshold, write an N/A note. N/A notes do not count as reviewers.
- **6.17-6.21, report gate:** `qa/qa-consolidated-findings-phase6.md`, then one fixer writing `qa/qa-fix-log.md`, then `qa/qa-fix-verification.md` and `qa/qa-fix-verification-qualitative.md`, then `phase-outputs/plans/report-gate-decision.md` (max 3 cycles).
- **6.22-6.32, source fidelity:**
  - `phase-outputs/discovery/fidelity-source-map.md` with 4 partitions:
    1. Orca planning
    2. oracle and renderer
    3. CI and monitor
    4. credential and current rules/controls
  - `qa/qa-source-fidelity-report-{1..4}.md` and `qa/qa-cross-source-contradictions-report.md`
  - `qa/qa-fidelity-consolidated-findings.md`, then `qa/qa-fidelity-fix-log.md`, then `qa/qa-fidelity-verification-{structural,content}.md`
  - `phase-outputs/plans/fidelity-gate-decision.md` (max 2 cycles)
- **6.33-6.42, anti-omission:**
  - `phase-outputs/discovery/anti-omission-input-map.md` with 4 partitions:
    1. screening and rules
    2. six cases
    3. deck plus synth-01/02/03
    4. synth-04/05/06, cards, debate and gaps
  - `qa/qa-anti-omission-report-{1..4}.md`, then `qa/qa-anti-omission-consolidated-findings.md`, then `qa/qa-anti-omission-fix-log.md`, then `qa/qa-anti-omission-verification-{structural,content}.md`
  - `phase-outputs/plans/anti-omission-gate-decision.md` (max 2 cycles). Late corrections invalidate earlier PASS results and require real reruns.

### Phase 7 (lines 545-563): present and "complete without archive"
- **7.1 (line 555):** `phase-outputs/reports/final-artifact-inventory.md`. Requirements: all 6 cases; no placeholders in the report or deck; exactly 5 hypotheses and 5 ranked entries; real debate artifacts including the merge and return contract; gate decisions that reflect the final state; tests N/A because no code changed.
- **7.2 (line 559):** present the absolute paths and the five causes ranked most-to-least likely within the sample, with evidence strength, overlap, limits, counts and open questions. Write a timestamped Task Summary in the Task Log (line 567).
- **7.3 (line 563):** set frontmatter `status: Done` with `completion_date` and `updated_date`, clear `blocker_reason`, and append an Execution Log entry. **Leave the package in `.dev/tasks/to-do/`.** If any blocker remains, keep the status Blocked and leave the item unchecked.

## 5. Prohibitions (cited)

- **No Git, move, archive, promote, implementation or public publication** (line 547; Step 7.3 verify, line 563: "no archive, promote, move, delete, commit, push, production edit or unrequested code-diff reflection"). The package stays at its original path even when Done (line 605).
- **Research-only:** section 8 is "explicitly unexecuted research follow-up ... code modification is not authorized" (Step 5.4, line 279). Proposed follow-ups are not authorization (Step 6.1, line 379). No implementation tasks may be created (line 620).
- **No production edits and no rewriting of historical evidence.** Corrections stay inside the package. Investigated production sources and historical task artifacts must never be repaired (line 601; Steps 5.24, 6.18, 6.29 and 6.39).
- **No fabrication:** no invented percentages or probabilities, base-selection scores are not likelihood (line 597; Step 5.12), no simulated debate (Step 5.11), and no backdating or claiming unrun gates (line 575).
- **Single fixer per cycle, independent report-only reviewers.** Halt order: regression first, then monotonicity, then cap. Use the exact halt strings (Steps 5.27, 6.21, 6.32, 6.42; line 609).
- **Do not run investigated plans through sc:implement.** Execution uses the Task skill (task-builder-readiness.md, Limits). POST_REFLECT_GATE is disabled and PRE reflect is skipped (no-spec) (line 616).
- **Unresolved work stays unchecked.** This overrides generic template wording (OQ-4, line 616).
- **No private logs sent externally** (Step 4.1, line 259).
