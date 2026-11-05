# Source-Fidelity Source Map

**Date:** 2026-10-24
**Task step:** 6.22 (bind four source-fidelity partitions)
**Report under review:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md`. It has 1,310 physical lines and sha256 `9ac64f1353fb9a6ea228af727183d3434788807498219150a54275a84ad8e568`, re-measured at this step.
**Gate state at entry:** The Step 6.21 report gate did not PASS. The user authorized advancement to source fidelity (`R/phase-outputs/plans/report-gate-decision.md:110-119`). Defect J1 is known and user-accepted: the stale status lines at Report:5, :1235 and :1287. Fidelity agents should record J1 as known rather than as a new finding.
**Path convention:** `R/` means `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. Every path outside the package is written out in full.

## Method

1. **Templates read.**
   - `/config/.claude/skills/tech-research/SKILL.md`: Gate 4 at 407-410 (partition into 3-4 agents when sources exceed 1000 lines), the Source-Document Fidelity Agent Prompt at 1153-1177, and the fidelity report format at 1178-1194.
   - `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md`: I21 at 759-788 and M4 at 1098-1121 (each fidelity agent reads its own source range plus the FULL output, and a separate cross-source contradiction agent is used).
   - The task file Steps 6.22-6.27 at `R/TASK-RESEARCH-review-loops-20261023-032537.md:461-483`.
2. **Inputs read in full.** The full report (lines 1-1310), `R/phase-outputs/plans/report-gate-decision.md` (lines 60-118), `R/phase-outputs/discovery/input-inventory.md`, all six case files, all five `scope-0N.md` files, `R/research/scope-rules.md`, `R/research/session-manifest.txt`, and the evidence deck's method, inventory and path-register sections (lines 1-170). Section boundaries for the rest of the deck and for the four raw capture files were found with `grep -n` on their headings.
3. **Source list.** Every absolute path outside the package that the report cites was extracted with `grep -o`. The same extraction was run on the six case files, the scope files, the rule map and the deck, to capture primary sources the report reaches through a case file. Paths that only a case file cites are marked "via case".
4. **Measurement.** All line counts come from `wc -l` on 2026-10-24, nothing was estimated. For JSONL session logs, the map gives the total physical lines plus the record span the report analyzes and the specific records it cites. Whole-log reading is not required. Where the case files recorded a historical hash, current copies were hash-checked with `sha256sum`; a match is marked ✓.
5. **Ownership rule.** Each source has exactly one owning partition. A partition may also read a named range of a file owned by another partition. These cross-reads are listed under each partition and do not transfer ownership.
6. **Constraints followed.**
   - No Git command was run.
   - The parent session log `dfade920-...jsonl` was not opened.
   - Index 03 (`bbddbf85-...jsonl`, the current investigation) was not opened. Only its `subagents/` transcripts that the report cites were measured.
   - Git objects are listed as Git-only, with the QA reports that recorded them.
7. **Every partition receives the FULL report:** `R/RESEARCH-REPORT-review-loops.md`, lines 1-1310, sha256 above.

## Partition 1: Orca planning, slots 19-24 screening originals, debate artifacts, gate and task records

**Owner case files:** `R/research/01-session-ac2cd1fd.md` and `R/research/scope-04.md`. Step 6.23 also names these.
**Full report assigned:** `R/RESEARCH-REPORT-review-loops.md` 1-1310.

| Path | Lines/ranges | Role | Report sections citing it |
|---|---|---|---|
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl` | 954 lines total. Assigned records 1-946. Cited records: 15, 37, 58, 141, 150-152, 163-164, 170, the 194-454 dispatch span, 499, 511, 544-545, 558, the 574-789 dispatch span, 821, 824, 841, 843, 849, 856, 858, 862, 874, 877, 885, 889, 906-934, 943-944, 946. Records 947-954 were not screened (Report §2.1). | Orca planning primary log (slot 20) | §2.1 endpoint table, §2.2, §2.5, Option A Support and Current-rule rows, Option B Support/Effort/Risk, §7.5 V1, §8 replay table, step 2.2, step 3.3 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/TASK-WF-designSpec-20261022-132541.md` | 1-272, whole. sha256 `94af0cda…` ✓ matches the reconstructed v4 (case 01:333). | Live plan v4. Versions v1-v3 exist only as JSONL Writes. Partition 3 cross-reads 209-232. | §2.2, §8 replay table, Q5 (via case 01) |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/source.md` | 1-555, whole. sha256 `32211523…` ✓. Cited lines: 115, 129, 136, 142, 158, 160, 167, 183, 245, 281, 285, 312, 316, 340, 345-359, 361, 365, 382, 400, 402, 454, 469, 477-479. | Driving source with the two retained contradictions. Partition 3 cross-reads 340 and 365. | §2.5 contradiction rows, Option C Support (142, 285, 382, 402), §8 Constraints, Q6 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/brainstorms/20261022T011827Z-orca-upstream-tracking/merged-requirements.md` | 1-480, whole. Cited lines 297 and 302. | Companion requirements (field 9) | §2.2 Orca row (via case 01 §3.2) |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/REPORT.md` | 1-77 | First review report: 16 findings, status partial | §2.2, §2.5 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/adversarial/merged-verdict.yaml` | 1-181. Cited 22-46 and 85-111. | First merged findings M-01 to M-16 | §2.2, §3 success row (via case 01 §A) |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/artifacts/coverage-matrix.yaml` | 2,311 lines total. Assigned 1749-1757. | Coverage over-credit evidence | Option A Support, §6 path key, §8 replay table |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/REPORT.md` | 1-79 | Second review report: the 13-fixed/3-partial narrative | §2.5 row 1, §4 ledger row |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml` | 1-241, whole. Cited 22-37, 39-47, 48-56, 57-65, 66-74, 75-83, 84-182, 183-209, 223-227, 235-241. | Second checklist: 14 fixed, 2 partial, 20 numbered items | Option A Support, Option B Support, §2.5, §6 path key, §8 replay table |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/artifacts/evidence-validation.yaml` | 1-18. Cited 14 and 15. | Second citation validation | via case 01 §4 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v3-targeted-20261022155651/verdict.yaml` | 1-21. Cited 11-21. | Condensed persisted targeted verdict (record 877) | §4 ledger row, step 3.3 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.github/contract-tests/test-50-candidate-attribution.sh` | 1,513 lines total. Assigned 599-628. | Inventory test behind the N-10 ordering defect | Option B Support (via case 01 §3.3) |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.github/contract-tests/test-66-orca-publish-gate.sh` | 600 lines total. Existence only: no line claim from it reaches the report. | Listed in the case 01 key table | none directly |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/45eb8186-bca4-4fef-a7c8-1212ca1b7500.jsonl` | 907 lines total. No record-level claim. Its disposition comes from `R/research/screening-handoffs-source.txt:234-239` and Orca ledger lines 3-20 (owned by Partition 3). | Slot 19 operational control (Tasks 1-9 compliant) | §2.2 controls table (Session 19), §7.7 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/2a6286d3-9129-4bd8-8553-566331606fe7.jsonl` | 1-30, whole | Slot 21 synthetic exclusion | §2.1, §3, §4 prevalence row |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/51f17e6b-e3c3-4bc5-a781-77a616d26366.jsonl` | 1-30, whole | Slot 22 synthetic exclusion | §2.1, §3 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/ba18b090-6d1e-4e58-bfd7-484aab7cab74.jsonl` | 1-30, whole | Slot 23 synthetic exclusion | §2.1, §3 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/6d203c97-e6c9-438d-a141-69e617526acb.jsonl` | 1-30, whole | Slot 24 synthetic exclusion | §2.1, §3 |
| `R/research/01-session-ac2cd1fd.md` | 1-442 | Orca case analysis | §2.2, §2.5, §2.6, §4, Options A-C, §7.7, §8 |
| `R/research/scope-04.md` | 1-59 | Screening of slots 19-24 | §10.2 |
| `R/research/screening-handoffs-source.txt` | 214-382 | Raw screening capture for slots 19-24 | §10.3 |
| `R/research/deep-handoffs-first-source.txt` | 1-374 | Raw Orca analyst return | §10.3 |
| `R/research/evidence-deck.md` | 170-201, 424-485, 579-642 | Orca chronology, Orca findings and successful repairs, cross-case miss mechanisms and reviewer disagreements | §2.4, §4 rows (:585-598, :608-639), §7.4, §8 bindings |
| `R/reviews/adversarial/adversarial/debate-transcript.md` | 1-489 | The actual debate and its final orders | §6.0, Options A-E debate rows, §7.1-7.2, step 2.6 (:270), Q18 (:49) |
| `R/reviews/adversarial/adversarial/base-selection.md` | 1-577 | Writing-base tiebreak | §6.0, §7.3, Option D debate row |
| `R/reviews/adversarial/adversarial/invariant-probe.md` | 1-75 | Round 2.5 probe | §6.0, §7.3 |
| `R/reviews/adversarial/adversarial/diff-analysis.md` | 1-82 | Comparison points | §6.0, §7.3 |
| `R/reviews/adversarial/adversarial/refactor-plan.md` | 1-112 | V5-above-V4 synthesis judgment | §7.1, §7.2, §7.3 |
| `R/reviews/adversarial/adversarial/plan-review-evidence.md` | 1-74 | Independent plan review PASS | §7.2, §10.5 |
| `R/reviews/adversarial/adversarial/merge-log.md` | 1-196. Cited 161-163 and 194-195. | Merge composition and recovery | §10.5, §10.9 |
| `R/reviews/adversarial/adversarial/variant-1-original.md` … `variant-5-original.md` | 61, 63, 62, 62 and 60 lines, each read whole. Variant 2 is cited at 10 and 37. | The five immutable debated cards | §6.0, Option B Scope, §10.5 |
| `R/reviews/adversarial/adversarial/score-source-manifest.json` | 2,298 lines total. Existence and role only. | Scoring provenance | §10.5, §10.11 |
| `R/reviews/adversarial/merged-root-cause-analysis.md` | 1-229. Cited 21, 37-43, 64, 155-165, 170, 205. | Recovered merged comparison | §6.0, Option A Falsification, §7.2-7.4 |
| `R/reviews/adversarial/return-contract.md` | 1-31. Cited 14, 16, 23-31. | Status partial, convergence 1.0 | §6.0, §7.2, §7.3, Q sources |
| `R/reviews/adversarial/run-evidence.md` | 1-32. Cited 16. | Run record | §10.5, §10.10 |
| `R/reviews/adversarial/input-manifest.json` | 1-32 | Input identities | §10.5 |
| `R/qa/adversarial-post-merge-validation.md` | 1-134. Cited 120. | Post-merge PASS, 13 of 13 checks | §6.0, §10.5 |
| `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-amerge-causal-analysis-d93f8889e87132e1.jsonl` | 71 lines total. Record 71. | Recovered merge-executor return | §10.5 |
| `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-aba0ed57846538ad4.jsonl` | 79 lines total. Record 79. | Canonical-review FAIL | §10.5 |
| `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-a815d047710b89c22.jsonl` | 38 lines total. Record 38. | Targeted re-review PASS | §10.5 |
| `R/BUILD-REQUEST.md` | 1-56. Cited 12 and 14. | Research question and trigger | §1, §10.7 |
| `R/TASK-RESEARCH-review-loops-20261023-032537.md` | Live file, 764 lines at this step. Assigned 64-75, 253-259, 643, 645, 647, 687, 691. | Task constraints, external N/A permission, and log entries [03:52Z], [03:45Z], [03:41Z], [05:35Z], [05:24Z] | §1, §5, Header lines 8 and 10, §10.7, §10.9 |
| `R/phase-outputs/plans/synthesis-gate-decision.md` | 1-70 | Synthesis gate FAIL/HALT and user override | Header line 10, §10.9 |
| `R/phase-outputs/plans/task-phase3-gate-decision.md` | 67-103 | Phase 3 cycle-2 closure | §10.8 |
| `R/phase-outputs/plans/task-phase4-gate-decision.md` | 134-177 | Phase 4 closure | §10.8 |
| `R/phase-outputs/plans/report-gate-decision.md` | 1-118 | Report-gate history, the authoritative J1 record | Header line 5, §10.9, §10.10 |
| `R/phase-outputs/plans/research-gate-decision.md` | 1-93 | Expanded research-gate PASS | §10.7 |
| `R/phase-outputs/plans/research-gate-decision-historical-case-gate.md` | 1-17 | Historical scoped PASS | §10.7 |
| `R/phase-outputs/plans/task-phase2-gate-decision.md` | 1-386 | Phase 2 PASS | §10.7 |

**Cross-reads (no ownership transfer):**
- `R/gaps-and-questions.md:29-35,59` (owned by Partition 4), for the Orca contradiction rows.
- `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/progress.md:3-20` (owned by Partition 3), for the Session 19 control.

**Partition 1 totals:**
- Text source lines assigned: **6,383**. That is 1,963 historical originals, 1,202 research layer, 2,371 debate artifacts and 847 gate/task records.
- JSONL: 2,169 total physical lines, with **1,069** in assigned record spans.

## Partition 2: Claim-oracle and documentation/render originals, cards, synthesis components, QA records

**Owner case files:** `R/research/02-session-a9b88895.md` and `R/research/03-session-6f744b87.md`. Step 6.24 also names these.
**Full report assigned:** `R/RESEARCH-REPORT-review-loops.md` 1-1310.

| Path | Lines/ranges | Role | Report sections citing it |
|---|---|---|---|
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl` | 1,447 lines total. Assigned records 139-824. Cited records: 139, 256, 291, 383, 398, 414, 450, 462, 475, 521, 573, 579, 585-586, 607, 668, 691, 779, 824. Records after 668 were not screened for the incident (§2.1). | Oracle primary log (slot 27) | §2.1, §2.2, Option A Support, Option E Support, Options Comparison, §7.5 V5, §8 replay table, step 2.5 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1/subagents/agent-aoracle-builder-6889f23314fbb16e.jsonl` | 251 lines total. Assigned records 52-223. Cited 52, 55, 58, 65, 189-196, 206-211, 223. | Builder trace | §8 replay table |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/TASK-WF-designV2-20261020-132032.md` | 1-234, whole | Managed plan with the Task 12 criteria | §2.2 (via case 02) |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/source.md` | 1-418, whole | Authoritative design source | via case 02 |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md` | 850 lines total. Assigned lines 607, 610 and 652. | Original family and retention requirements | §2.2, §2.4 (via case 02 §4) |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-1.md` | 1-54. Cited 20-35. | Full first review (findings 1-4) | §2.2, Option A Support, Options Comparison |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-2.md` | 1-68. Cited 20-28 and 30-40. | Second review (one retained defect) | Option E Support |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-authorized.json` | 1-58 | Passing authorized-correction review | via case 02 |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-held-back-before-authorization.json` | 767 lines total. Assigned 563-628. | Preserved frozen fixture (`default_path: false`) | Option A Reuse, Option E Reuse, §8 replay table |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/tests/skills/test_auggie_claim_gate_oracle.py` | 518 lines total. Assigned 278-283, 291-302, 305-322, 325-350. | Current oracle assertions | §2.4 (via case 02 §4-5) |
| `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/` | 43 files, re-counted. Count and existence only. | Oracle artifact root (live to-do package) | Option A Files row, §8 replay table |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl` | 1,081 lines total. Assigned records 14-539 and 871-927. Cited records: 14, 42, 99, 141, 143, 188, 197, 204, 217, 222, 234, 237, 401, 406, 408, 413-414, 423, 430, 433-434, 443, 450, 485-486, 496, 498, 503, 506, 510, 515, 527, 530-531, 539, 871, 878, 892, 894, 915, 927. | Documentation primary log (slot 01) | §2.1, §2.2, Option D Support, Option E Support, §7.4, §8 replay table, steps 2.5 and 3.5 |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/TASK-WF-issue358FollowUp-20261022-210638.md` | 1-87. sha256 `43934e0a…` ✓. Cited 81-87. | Task 6 render criterion | §8 Recovered rendering-evidence table |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/artifacts/t6-fix-evidence.log` | 1-26. sha256 `7f271ce5…` ✓. Cited 1-3. | Static-only evidence: missing renderers and notice output | §8 rendering table, Option E Reuse |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/progress.md` | 1-19. sha256 `0fe8afd5…` ✓. Cited 14-18. | Blocked, head-moved halt, acceptance, cannot-verify completion, FINAL pass | §8 rendering table |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/artifacts/t6.diff` | 1-44. sha256 `11afd387…` ✓. | Task 6 before/after diff | via case 03 §3 |
| `/usr/bin/man` | 1-6. sha256 `1150abfc…` ✓. | Notice script, not a renderer | Option E Support |
| `R/research/02-session-a9b88895.md` | 1-314 | Oracle case analysis | §2.2, §2.4, Options A and E, §7.7, §8 |
| `R/research/03-session-6f744b87.md` | 1-362 | Documentation case analysis and current-location mapping | §2.2, §2.5, Options D and E, §7.7, §8 |
| `R/research/scope-05.md` | 1-52 | Screening of slots 25-30 (oracle selection) | §10.2 |
| `R/research/screening-handoffs-source.txt` | 383-453 | Raw capture for slots 25-30, including oracle identifiers at 414-431 | §10.3 |
| `R/research/deep-handoffs-first-source.txt` | 375-675 | Raw oracle analyst return | §10.3 |
| `R/research/screening-recovery-source.txt` | 67-91 | Raw Session 01 screening | §10.3 |
| `R/research/evidence-deck.md` | 202-264, 372-423, 486-496 | Oracle and manual-page chronology, transition matrix, six causal classes, oracle findings | §4 rows (:380-382, :389-391), §2.2, §8 bindings |
| `R/research/web-01-gap-applicability.md` | 1-182 | External N/A decision | §3 Constraints, §4, §5, §9, §10 Web Research |
| `R/synthesis/hypothesis-01.md` … `hypothesis-05.md` | 256, 265, 264, 263 and 266 lines, each whole | Formatted debated cards | Options A-E, §7.4, §7.6, §10.4 |
| `R/synthesis/synth-01-problem-current-state.md` | 1-220 | Component for Sections 1-2 | §2.6, §10.4, §10.9 identity table |
| `R/synthesis/synth-02-target-gaps.md` | 1-116 | Component for Sections 3-4 | §4, §10.9 |
| `R/synthesis/synth-03-external-findings.md` | 1-104 | Component for Section 5 | §5, §10.9 |
| `R/synthesis/synth-04-options-recommendation.md` | 1-367 | Component for Sections 6-7 | §10.4, §10.9, §10.10, §10.11 |
| `R/synthesis/synth-05-implementation-plan.md` | 1-162 | Component for Section 8 | §8, §10.9, §10.10 |
| `R/synthesis/synth-06-questions-evidence.md` | 1-289 | Component for Sections 9-10 | §10 structure note, §10.9 |
| `R/qa/qa-lens-internal-consistency.md` | Lines 25 and 61 | Records the Git reads (2165ae25, c6009cd3, reflog, log) | Header line 8, §3 Constraints, §8 |
| `R/qa/qa-lens-crossref-chain.md` | Lines 27 and 53 | Records the Git reads (bbbfcc4b, c6009cd3) | Header line 8 |
| `R/qa/qa-lens-domain-accuracy.md` | Line 55 | Records the Git reads (6dc56b1a, 00448800) | Header line 8 |
| `R/qa/qa-consolidated-findings-phase6.md` | 1-251, whole. Line 92 records Git use. | P6-01 to P6-31 consolidation | Header line 5, header line 8, §10.10 |
| `R/qa/qa-fix-log.md` | Lines 31-32 | Git-pinned citations from the Step 6.18 fix | Header line 8, §10.10 |
| `R/qa/qa-fix-verification.md` | Line 133 | Step 6.19 Git reads | Header line 8 |
| `R/qa/qa-fix-verification-qualitative.md` | Line 123 | Step 6.20 Git reads | Header line 8 |
| `R/qa/qa-fix-log-cycle2.md` | 1-135 | Report-gate cycle-2 patches | Header line 5, §10.10 |
| `R/qa/qa-research-verification-structural.md` | 93-127 | Seven-pair equality and its later change | §2.5 |
| `R/qa/qa-phase-3-fix-log.md` | 95-116 | Canonical depth-review attribution erratum | §10.3 |
| `R/qa/qa-lens-implementation-concreteness.md` | Line 31 | Re-check of the rendering targets | §8 rendering table |
| `R/qa/synthesis-component-intake.md` | Lines 5 and 59-63 | Intake status | §10.1, §10.4, §10.6 |
| `R/qa/synthesis-gate-intake.md` | Lines 5 and 8 | Intake still In Progress | §10.9 |
| `R/qa/qa-synthesis-verification-structural.md` | Line 12 | Text-return persistence note | §10.9 |
| `R/qa/qa-synthesis-verification-content.md` | Line 12 | Text-return persistence note | §10.9 |
| `R/qa/qa-synthesis-fix-log-cycle2.md` | Lines 5 and 21 | Patches prepared, not applied, at return time | §10.9 |
| `R/qa/qa-synthesis-fix-log.md` | 1-264 | Step 5.24 corrections, P5-26 and P5-27 | §10.1, §10.6, §10.11 |
| `R/qa/qa-consolidated-findings-phase5.md` | 1-302 | 33 issues, P5-28 | §10.4, §10.6 |
| `R/qa/` directory, all other files | 232 files at this step. The report records 207 at 03:51:27Z, and 204 by brace expansion. Existence and count only for the §10.6 brace lists. | QA inventory | §10.1, §10.6, §10.9, §10.10 |

**Partition 2 totals:**
- Text source lines assigned: **6,181**. That is 1,145 historical originals, 1,433 research layer, 1,314 cards, 1,258 synthesis components and 1,031 QA records.
- JSONL: 2,779 total physical lines, with **1,441** in assigned record spans.

## Partition 3: CI-plan and Orca-monitor originals

**Owner case files:** `R/research/04-session-43582de1.md` and `R/research/05-session-e002bed2.md`. Step 6.25 also names these.
**Full report assigned:** `R/RESEARCH-REPORT-review-loops.md` 1-1310.

| Path | Lines/ranges | Role | Report sections citing it |
|---|---|---|---|
| `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` | 1,156 lines total; the report recorded 1,153 at 04:37Z, so the log has grown. Assigned records 1-1087. Cited records: 69, 75, 170, 342, 493, 623, 627, 651, 653, 663, 670, 733, 791, 801, 810, 821, 825, 845, 987-988, 990, 999, 1003, 1008, 1011, 1015, 1036, 1052, 1072-1073, 1079, 1084, 1086 (window end), and 1087 (outside the window). | CI planning primary log (slot 04) | §2.1, §2.2, §4 reviewer row, §8 replay table |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-spec-20261022-211556/TASK-WF-spec-20261022-211556.md` | 1-160. sha256 `dcb320b5…` ✓. Cited 34, 45, 49, 84, 88-91, 94, 105, 113-114, 121, 124, 150, 158-160. | Original CI plan | §8 replay table |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/done/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md` | 1-186. sha256 `895dcd6b…` ✓. The to-do copy that case 04 cites, `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md`, is the same hash and 186 lines. Cited 23-186. | Regenerated CI plan | §8 replay table |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/done/TASK-WF-specR1-20261023-031725/source.md` | 1-82. The to-do copy is also 82 lines; the two were not hash-compared. Cited 24, 35, 38-39, 69, 75, 80-82. | Revised source | via case 04 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/done/TASK-WF-specR1-20261023-031725/progress.md` | 1-22. Cited 1, 21, 22. | Execution ledger after the window | Q7 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/REPORT.md` | 1-164 | Original review report | via case 04 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/adversarial/merged-verdict.yaml` | 1-418 | Original 18 merged concerns | §2.2 (via case 04 §5) |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md` | 1-136. Cited 21-25, 58-74, 80-91, 124-136. | Final second review: not ready, 5 medium and 11 low | §2.2 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/return-contract.yaml` | 1-129. Cited 71-75. | `overall_verdict: not_ready` | §2.2 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/artifacts/evidence-validation.yaml` | 1-6 | Two dropped citations (partial status) | §2.2 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/adversarial/merged-verdict.yaml` | 1-386 | 16 merged items | §2.2, Option A Effort |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/adversarial/invariant-probe.md` | 1-32. Cited 7-16. | Completed probe | Option A Support (half-edited header) |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/adversarial/consensus-summary.md` | 1-20 | Emerging consensus | via case 04 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/adversarial/round2-v1.md` | 1-34 | Reviewer 1 concessions | §2.2, §4 reviewer row |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/adversarial/round2-v2.md` | 1-26 | Reviewer 2 corrections | via case 04 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/reviewer-cards/reviewer-1-card.yaml` | 1-196. Cited 108-132. | Reviewer 1 card: "16 fixed, 2 partial" and "ready with notes" | §2.2, §4 reviewer row |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/reviewer-cards/reviewer-2-card.yaml` | 1-129 | Eight second-reviewer entries | via case 04 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/reviewer-cards/reviewer-2-calibration.yaml` | 1-52 | Calibration | via case 04 |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/boundary-guard.yml` | 1-98. Cited 76-82. | Current corroboration of the "(diff unavailable)" fallback | via case 04 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl` | 2,058 lines total. Assigned: records 1-1247 (analyzed prefix), 1250-1437 (continuation), and out-of-window records 859 and 1620-2049 (including 1670 and 1997). Cited records: 14, 40, 42, 58, 171, 267, 319, 496, 540, 585, 685-686, 697, 716-766 (including 759-762), 797, 800, 804, 817, 820, 825, 827, 842, 849, 869, 873-874, 882-885, 893-894, 902, 906, 913, 921, 937-994 (including 939, 945, 949, 970-976, 994-995), 1009-1010, 1021, 1041, 1044, 1060-1066, 1131-1132, 1143, 1150, 1153, 1164-1170, 1188-1210, 1228-1229, 1240, 1243-1244, 1247, 1250, 1260-1261, 1293, 1301, 1305, 1324, 1331, 1340, 1348-1349, 1355, 1370-1371, 1397. | Orca monitor primary log (slot 05) | §2.1 endpoint and out-of-window paragraphs, §2.2, Option A Support, Option B Support, Option C Support and Scope, §7.4, §8 replay table, step 2.3 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.github/workflows/orca-upstream-monitor.yml` | 713 lines total. Assigned 413-428. | Current workflow that retains the trap mechanism | via case 05 §5.2 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/artifacts/t12-monitor-yaml.log` | 1-33. Case 05:71 recorded 34 lines; the file is overwritten. | Structural-check log | via case 05 §2 |
| `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/progress.md` | 1-53, live. It had 42 rows at 04:03:52Z. Cited 3-20, 25-36, 40-42. | Shared Orca ledger. Partition 1 cross-reads 3-20. | §2.5 ledger row, Q10 |
| `R/research/04-session-43582de1.md` | 1-610 | CI case analysis | §2.1, §2.2, §4, Options A-C, §7.3, §7.7, Q7 |
| `R/research/05-session-e002bed2.md` | 1-502 | Monitor case analysis | §2.1, §2.2-2.5, Options A-C, §5.1, §7.7 |
| `R/research/scope-01.md` | 1-48 | Screening of slots 01-06 | §10.2 |
| `R/research/scope-01-recovered.md` | 1-147 | Recovered original screening draft | §10.2, §10.9 |
| `R/research/screening-recovery-source.txt` | 111-167 | Raw Session 04 and 05 screening | §10.3 |
| `R/research/deep-handoffs-remaining-source.txt` | 1-573 | Raw CI and monitor analyst returns | §10.3 |
| `R/research/evidence-deck.md` | 265-336, 497-552 | CI and monitor chronology and findings | §2.2 (:280), §4 rows (:501-518, :547-548), §8 bindings |
| `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-ascan-sessions-01-033fec55d74e7a9e.jsonl` | 113 lines total. Supplementary: only `scope-01.md:11` cites it, not the report. | Slot 01-06 screening transcript | none directly |

**Cross-reads (no ownership transfer):**
- Orca plan 209-232 and Orca source 340 and 365 (owned by Partition 1).
- `/config/.claude/skills/sc-implement-protocol/refs/ledger.md:61-81` and `/config/.claude/skills/sc-implement-protocol/refs/retry.md:38-43` (owned by Partition 4).

**Partition 3 totals:**
- Text source lines assigned: **4,443**. That is 2,378 historical originals and 2,065 research layer.
- JSONL: 3,327 total physical lines, with **2,954** in assigned record spans.

## Partition 4: Credential finals, remaining screening negatives and controls, current-rule sources, cross-case research layer

**Owner case and control files:** `R/research/06-session-0690ee9f.md` and `R/research/scope-rules.md`, plus the screening controls. Step 6.26 also names these.
**Full report assigned:** `R/RESEARCH-REPORT-review-loops.md` 1-1310.

| Path | Lines/ranges | Role | Report sections citing it |
|---|---|---|---|
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl` | 2,095 lines total. Assigned records 15-2036. Cited records: 15, 36, 318, 332, 375, 390, 396, 411, 415, 419, 435, 762-818, 1215, 1219, 1230, 1425, 1916, 1932, 1935, 1938, 1968-1969, 1979, 2012, 2015-2016, 2028, 2036. Records 2037-2095 were not screened. | Credential primary log (slot 15) | §2.1, §2.2, §4 consent row, Option C Support, Option D Support, §7.5 last row, §8 replay table, step 3.5 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a6d8fbaf69a56dd14.jsonl` | 61 lines total. Record 61. | Task 6 reviewer accepts the relaxed lint rule | §2.2, Option C Support |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a9c0c61dd415c2c4d.jsonl` | 135 lines total. Record 135. | First follow-up FINAL issues | §2.2, Option C Support |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-acf0a51e6992c50ee.jsonl` | 116 lines total. Records 16, 18, 116. | Second FINAL (absent from the ledger) and earlier rubric load | §2.2, Option C Support |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a4bfff371c63a6c39.jsonl` | 155 lines total. Records 16, 18, 19, 21, 27, 42, 84, 87, 99, 121, 155. | Third FINAL pass, later rubric load, eight observations | Option C Support, §2.3 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-abd76ef5e5d22848f.jsonl` | 36 lines total. Record 36. | Task 3 reviewer's temporary lint proof | Option D Support |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-af349dd52cae648a5.jsonl` | 33 lines total. Records 16 and 33. | Task 10 reviewer's wrong `:10-12` citation | Option D Support |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a59e9aa6df05118de.jsonl` | 51 lines total. Record 51. | Initial-package FINAL issues | via case 06 §3 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a6248e3c9fc51e940.jsonl` | 50 lines total. Record 50. | Initial-package FINAL pass | via case 06 §3 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/` | 45 `.jsonl` files, re-counted. The other 37 files: count and existence only. | Nested reviewer directory | §2.2, §6 path key, Options C and D Reuse/Files, §8 replay table |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/TASK-WF-issue358InTempla-20261022-151058.md` | 1-80. sha256 `b6610852…` ✓. | Initial-package plan (current copy, hash-identical) | via case 06 §2 |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/source.md` | 1. sha256 `f79ef858…` ✓. | Initial-package source | via case 06 §2 |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/progress.md` | 1-14. sha256 `a3082878…` ✓. Cited 8 and 11-13. | Initial-package ledger | via case 06 §3 |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/artifacts/t3-markdownlint.log` | 1-24. Cited 10, 15, 22, 24. Identity with the historical log is not hash-verified because no historical hash was recorded. | Candidate current durable lint proof | Option D Reuse |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/TASK-WF-issue358FollowUp-20261022-193837.md` | 1-196. sha256 `b50308ee…` ✓. Cited 30, 46, 96, 100-103, 190. | Follow-up plan with the literal lint rule | §4 contract row (via case 06) |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/source.md` | 1-22. sha256 `868b5ec0…` ✓. | Follow-up source | via case 06 §2 |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/progress.md` | 1-44. sha256 `7cfcbec5…` ✓. Cited 22 and 37-43. | Follow-up ledger with no second failed FINAL | §2.5, §4 ledger row |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t6-owner-acceptance.md` | 1-16. Cited 10-13. Identity not hash-verified. | Scoped owner acceptance (Tasks 7, 8 and 17) | §4 consent row (via case 06) |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t6-markdownlint.log` | 1-26. Cited 18-26. Identity not hash-verified. | Task 6 lint evidence | via case 06 §4 |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log` | 1-17. Cited 9, 10, 14, 17. Identity not hash-verified. | Candidate current Task 10 log with the blank line 10 | Option D Reuse |
| `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t17-followups.md` | 1-43. Identity not hash-verified. | Historical follow-up positions | via case 06 §7 |
| `R/research/historical-review-rules.json` | 1-22 | Decoded earlier and later rubric loads | §2.3, Option C Reuse, §8 steps 1.2 and 2.3 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/eabc78ed-0538-486a-a51b-744d73b9cb24.jsonl` | 3,466 lines total. No records cited; the disposition comes from `screening-recovery-source.txt:92-103`. | Slot 02 negative | §2.1, §3 |
| `/config/.claude/projects/-config-workspace-Coder/99d5f896-a262-440a-9f54-d404557fd8bc.jsonl` | 474 lines total. No records cited; disposition at `screening-recovery-source.txt:168-175`. | Slot 06 negative | §2.1, §3 |
| `/config/.claude/projects/-config-workspace-Ironbrain/562ef463-5deb-48a4-bcd2-f2b2140a3ba6.jsonl` | 156 lines total. No records cited; disposition at `screening-handoffs-source.txt:42-53`. | Slot 07 negative | §2.1, §3 |
| `/config/.claude/projects/-config-workspace-Ironeye/ad0d7890-d7e2-4563-a5dd-8557f3e84cdb.jsonl` | 1,350 lines total. No records cited; disposition at `screening-handoffs-source.txt:54-66`. | Slot 08 negative | §2.1, §3 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/15345c19-43c3-4254-9ea9-722b0e11da10.jsonl` | 584 lines total. Record 580. | Slot 09 control: FINAL never ran | §2.2 controls, §7.7 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/0d43d44d-81cc-491a-8d92-01a5a373d5e7.jsonl` | 1,975 lines total. Records 1056, 1060, 1078, 1247. | Slot 10 control: Task 4 one-repair convergence | §2.2, Opposition rows of A, B and E, §7.7, step 3.1 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/428a336e-9f3b-4227-9e0d-fc124e84fe36.jsonl` | 945 lines total. Records 472, 501, 807. | Slot 11 exclusion: unchanged plan | §2.1 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/976b97f5-2eeb-4c5a-8e61-7972750b3b19.jsonl` | 221 lines total. Record 214. | Slot 12 exclusion: workflow creation only | §2.1 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/c444c002-20df-4745-8f95-2254c4d3086f.jsonl` | 750 lines total. Records 364-435. | Slot 13 precursor (Sessions 13/14 control) | Option B Opposition, §7.7, step 3.1 |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/10cacee5-9821-461e-89b4-903837da3b8b.jsonl` | 384 lines total. Records 344-371. | Slot 14 precursor | Option B Opposition, §7.7 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/97c47129-146b-4227-a0db-9830352b81aa.jsonl` | 129 lines total. No records cited; disposition at `screening-recovery-source.txt:433-448` and `:677-685`. | Slot 16 negative | §2.1 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/0f6383e1-533a-428c-aee4-18e6ddfb4aef.jsonl` | 4,355 lines total. Records 832, 836-858, 868, 1276, 1291, 1751, 1770. | Slot 17 controls: Task 8 and FINAL | §2.2, §4 controls, Opposition rows of A, B, D and E, §7.7, step 3.1 |
| `/config/.claude/projects/-config-workspace-IronClaude/5290b7ae-b9be-47ad-951d-ac7c63411061.jsonl` | 1,447 lines total. No records cited; disposition at `screening-recovery-source.txt:449-...` and the corrected anchors at `:686-703`. | Slot 18 negative | §2.1 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/105b1734-aa39-4fd7-a0e5-606823f903be.jsonl` | 17 lines total. Records 11 and 15. | Slot 25 setup only | §2.1 |
| `/config/.claude/projects/-config-workspace-IronClaude/f597ad3b-45b2-4ae3-b498-5f66f556bc9a.jsonl` | 2,180 lines total. Records 18, 492, 759, 1256. | Slot 26 negative | §2.1 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/44709b0f-ea0d-4f00-b0f6-282bf2af57c1.jsonl` | 29 lines total. Record 7. | Slot 28 synthetic | §2.1 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/8ba23e21-891a-4581-b01f-89cd10b01104.jsonl` | 29 lines total. Record 7. | Slot 29 synthetic | §2.1 |
| `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-implement-retry-ladder/fda5564b-197d-4ad7-87cf-2d22a58a605b.jsonl` | 29 lines total. Record 7. | Slot 30 synthetic | §2.1 |
| `/config/.claude/skills/sc-workflow-protocol/SKILL.md` | 74 lines total. Assigned 50-74 (no-edit rule at 60, "Will Not" at 74). mtime 2026-10-23T17:55:50Z. | Current rule, installed layer | §2.3 installed table |
| `/config/.claude/skills/sc-workflow-protocol/refs/quality-gates.md` | 41 lines total. Assigned 24-41. mtime 2026-10-22T20:29:54Z. | Current rule | §2.3, Option A Current-rule row, §7.5 |
| `/config/.claude/skills/sc-implement-protocol/refs/qa.md` | 90 lines total. Assigned 9-17, 25-52, 62-68, 80-90. sha256 `faff03b7…d2e7d5` ✓. mtime 2026-10-22T20:29:54Z. | Current rule; same bytes as the later captured load | §2.3, Options C and D Current-rule rows, §7.5 |
| `/config/.claude/skills/sc-implement-protocol/refs/retry.md` | 451 lines total. Assigned 38-43 and 142-146. mtime 2026-10-22T20:29:54Z. | Current rule | §2.3 |
| `/config/.claude/skills/sc-implement-protocol/refs/ledger.md` | 242 lines total. Assigned 61-81 and 138-158 (single-writer rule at 142). mtime 2026-10-23T17:55:50Z. | Current rule; rewritten after the monitor's record-874 load | §2.3, Option C Scope |
| `/config/.claude/skills/sc-implement-protocol/refs/managed-workspace.md` | 86 lines total. Assigned 43-69 and 79-86. mtime 2026-10-23T17:55:50Z. | Current rule (pin at 43) | §2.3, Option E Current-rule row, §7.5 |
| `/config/.claude/skills/sc-implement-protocol/SKILL.md` | 175 lines total. Whole file assigned; no line claim. | Installed file read at monitor record 884 | Option C Scope |
| `/config/.claude/skills/tech-research/SKILL.md` | 1,686 lines total. Assigned 779-811 and 1311-1531 (which contains 1393-1431). | Governing template | Header line 11, §6 Governing format, §10.11 |
| `R/research/06-session-0690ee9f.md` | 1-387 | Credential case analysis | §2.2, §2.3, §2.5, §4, Options C and D, §7.4, §7.7, §8 |
| `R/research/scope-rules.md` | 1-96 | Rule map with the captured rubric hashes at 70-71 | §2.3, §3, Options A-E Current-rule rows, §7.5, §8 |
| `R/research/scope-02.md` | 1-44 | Screening of slots 07-12 | §10.2 |
| `R/research/scope-03.md` | 1-46 | Screening of slots 13-18 | §10.2 |
| `R/research/scope-03-recovered.md` | 1-184 | Recovered original screening report | §10.2, §10.9 |
| `R/research/research-notes.md` | 1-84 | Scope discovery | §10.2, §10.11 |
| `R/research/session-manifest.txt` | 1-31 | Frozen 30-slot population | §2.1, §10.3 |
| `R/phase-outputs/discovery/input-inventory.md` | 1-93 | Administrative inventory | §10.7, §10.9 |
| `R/gaps-and-questions.md` | 1-63 | Gap register | §2.5, §2.6, §2.7, §3, §4, §5, §6 Sample boundary, §7.5, §7.7, §8, §9 |
| `R/research/evidence-deck.md` | 1-169, 337-371, 553-578, 643-900 | Method, 30-slot inventory, primary-path register (117-143), denominators (145-164), credential chronology and findings, counterexamples, rule map, inventory, gaps, summary | §1, §2.1, §2.2, §2.4, §3, §4, §5, §6, §7, §8, §9 |
| `R/research/screening-handoffs-source.txt` | 1-213 | Raw capture for slots 07-12 plus summary | §10.3 |
| `R/research/screening-recovery-source.txt` | 1-66, 92-110, 168-703 | Raw recovery: slot 01-06 header, Sessions 02, 03 and 06, slots 13-18 with physical-line corrections | §10.3 |
| `R/research/deep-handoffs-remaining-source.txt` | 574-891 | Raw credential analyst return | §10.3 |
| `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-ascope-review-rules-0cb52ca63dfedc7b.jsonl` | 93 lines total. Record 79. Supplementary: only `scope-rules.md:11` cites it. | Rule-map analyst return | none directly |

**Partition 4 totals:**
- Text source lines assigned: **4,586**. That is 1,918 historical and current-rule originals (483 credential artifacts, 22 rubric JSON, 1,159 installed rules, 254 governing-template ranges) and 2,668 research layer.
- JSONL: 21,345 total physical lines, with **2,871** in assigned record spans. Whole-file reading of the screening logs is not required; the screening captures carry their dispositions.

## Unavailable or Git-only Sources

### Git-only: recorded in prior QA reports, not re-readable without Git

Reviewers must not run Git. They should check the recorded results in the listed QA lines and compare them against the installed-layer equivalents in Partition 4.

| Object | Report claims that depend on it | Where recorded |
|---|---|---|
| IronClaude master `2165ae25` (`2165ae259ee7b1afc3d86b21785814f850a21e78`): `src/superclaude/skills/sc-workflow-protocol/SKILL.md:48-72` (:58, :72), `refs/quality-gates.md:24-41`, `sc-implement-protocol/refs/qa.md:9-17,25-52,62-68,80-82,84-90`, `refs/retry.md:142-146`, `refs/ledger.md:138-158,142`, `refs/managed-workspace.md:42,44-60,60-68,78-85` | §2.3 main table, §6 Current-rule rows, §7.5 | `R/qa/qa-lens-internal-consistency.md:25`; `R/qa/qa-lens-crossref-chain.md:53`; `R/qa/qa-fix-log.md:31`; `R/qa/qa-fix-verification.md:133` |
| `6dc56b1a:` and `00448800:` copies of `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, with hashes `0b533765…` and `faff03b7…` | §2.3 rubric provenance, Option C Evidence strength, Q3 | `R/qa/qa-lens-domain-accuracy.md:55`; `R/qa/qa-fix-log.md:32`. The captured hashes can be re-read without Git at `R/research/scope-rules.md:70-71`, `R/research/historical-review-rules.json`, and records 18 of `agent-acf0a51e6992c50ee.jsonl` and `agent-a4bfff371c63a6c39.jsonl`. |
| Commit `c6009cd3`, branch HEAD `bbbfcc4b`, the 2026-10-24T03:42:30Z branch switch, and the master commit time 2026-10-22T20:29:01Z | §2.3 lead paragraph and installed table, Option E Current-rule row | `R/qa/qa-lens-internal-consistency.md:25,61`; `R/qa/qa-lens-crossref-chain.md:27,53`; `R/qa/qa-fix-log.md:31` |
| Coder tree objects `f60d2c39727ec1c65b2a5fd475c0c9ebd2a0c894`, `3c5fdfacef70399481ed851f92d217d7b10011b0`, `00d8f4ae0d9a617eac6bf882e9c9ecf1c602e0a8` in `/config/workspace/Coder/.git` | Option D Support and Reuse, §8 Documentation replay row | Analyst reads recorded at `R/research/03-session-6f744b87.md:212-239`. The report states that these loose objects were not validated and that reading them needs authorization. |
| Coder blobs `62e217cd` and `0a01c9a4`, and trees `7ac64e6a91f624362b19daf46ea9544ad8a4edcd` and `d9f262a48f82c55b18f883826428f2fd8d2d7be5` | Reached only through the case files (§2.2 rows via cases 03 and 06) | `R/research/03-session-6f744b87.md:121-131`; `R/research/06-session-0690ee9f.md:94,283` |

### Unavailable historical originals

These are not fabricated or substituted. Owners are listed for accountability.

| Unavailable item | Status observed 2026-10-24 | Owner |
|---|---|---|
| The entire worktree `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env` and every historical path under it. This includes `docs/manpages/aienv.7` and `templates/VSCode-AIDev02/manpages/aienv.7`, the historical package roots for `TASK-WF-issue358FollowUp-20261022-210638`, `TASK-WF-issue358InTempla-20261022-151058` and `TASK-WF-issue358FollowUp-20261022-193837`, and `artifacts/retries/T6/q0-head`. | The root does not exist (`ls` failed; `wc` on `aienv.7` failed). Hash-identical current copies exist only for the files marked ✓ in Partitions 2 and 4. There is no current verified copy of the delivered manual-page bytes. `q0-head` was never created historically (research/03:165-169). | P2 for the worktree root and documentation paths; P4 for the credential package paths |
| `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/pull-sync-framework.yml`, lines 89-108 | Missing: `wc` reported "No such file". Cited at `R/research/04-session-43582de1.md:377`. | P3 |
| Credential Task 3 temporary before/after lint files | Never preserved. Only described at `agent-abd76ef5e5d22848f.jsonl` record 36. | P4 |
| A full pre-authorization oracle snapshot | Never preserved (`R/research/02-session-a9b88895.md:269`; Q13). | P2 |
| The installed `ledger.md` bytes the monitor loaded at record 874 | The installed file was rewritten at 2026-10-23T17:55:50Z and no historical hash was recorded (Option C Scope). | P4 |
| Orca plan versions v1-v3 as files, and the monitor's original 640-line workflow as a file | They exist only inside JSONL Write/Edit records: Orca 141, 164, 544 and 841; monitor 585. The monitor's `t12-monitor-yaml.log` has been overwritten. | P1 for Orca; P3 for monitor |
| Session 15 follow-up reflect `REPORT.md` | Never written; the historical session acknowledged this (`scope-03.md:38`). | P4 |
| Session 10's original implementation package | Absent from the searched locations (`scope-02.md:36`). | P4 |
| Rubric versions for any reviews other than the two captured loads | Not captured (Q3). | P4 |
| Index 03 content (`/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de.jsonl`) | Excluded by design. Not opened and not a negative control. | not assigned |
| Parent session log `/config/.claude/projects/-config-workspace-IronClaude/dfade920-dc5e-4a04-9498-211d9f08715d.jsonl` | Reading forbidden. The report does not cite it. | not assigned |

## Coverage Check

**Absolute paths outside the package that the report cites** (extracted by `grep -o` from the report):

| # | Report-cited path | Partition |
|---|---|---|
| 1 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl` | P1 |
| 2 | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/artifacts/coverage-matrix.yaml` and its `artifacts/` directory | P1 |
| 3 | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml` and its `adversarial/` directory | P1 |
| 4 | Orca `source.md` (cited by name in Option C) | P1 |
| 5 | `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl` | P2 |
| 6 | `.../a9b88895-5374-4cae-8ebb-cac03a97aff1/subagents/agent-aoracle-builder-6889f23314fbb16e.jsonl` | P2 |
| 7 | `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/` and its `t12-review-1.md`, `t12-review-2.md`, `t12-held-back-before-authorization.json` | P2 |
| 8 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl` | P2 |
| 9 | `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/` and its plan, `progress.md`, `artifacts/t6-fix-evidence.log` | P2 |
| 10 | `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env` (unavailable) | P2 |
| 11 | `/config/workspace/Coder/.git` (Git-only) | P2 |
| 12 | `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` | P3 |
| 13 | The CI original plan, the regenerated done plan, and the done `progress.md` | P3 |
| 14 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl` | P3 |
| 15 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl` | P4 |
| 16 | The `.../0690ee9f-.../subagents/` directory and the nested files the report names: `agent-a6d8fbaf69a56dd14`, `agent-a9c0c61dd415c2c4d`, `agent-acf0a51e6992c50ee`, `agent-a4bfff371c63a6c39`, `agent-abd76ef5e5d22848f`, `agent-af349dd52cae648a5` | P4 |
| 17 | `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/artifacts/t3-markdownlint.log` | P4 |
| 18 | `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log` | P4 |
| 19 | `/config/.claude/skills/` and the installed `sc-workflow-protocol/SKILL.md`, `refs/quality-gates.md`, `sc-implement-protocol/refs/qa.md`, `retry.md`, `ledger.md`, `managed-workspace.md` | P4 |
| 20 | `/config/.claude/skills/tech-research/SKILL.md` | P4 |
| 21 | `/config/.claude/projects/` (the population glob in §2.1, resolved through the manifest) | P4 |
| 22 | The merge-executor transcript and `agent-aba0ed57846538ad4.jsonl`, `agent-a815d047710b89c22.jsonl` (cited by name in §10.5) | P1 |

**Package files the report cites, by partition:**
- **P1:** `BUILD-REQUEST.md`; the task file; seven `phase-outputs/plans/*.md`; four `reviews/adversarial/*`; thirteen `reviews/adversarial/adversarial/*`; `qa/adversarial-post-merge-validation.md`; `research/01-session-ac2cd1fd.md`; `scope-04.md`.
- **P2:** `research/02-session-a9b88895.md` and `research/03-session-6f744b87.md`; `scope-05.md`; `web-01-gap-applicability.md`; five hypothesis cards; six synthesis components; 18 named QA files; the `qa/` inventory.
- **P3:** `research/04-session-43582de1.md` and `research/05-session-e002bed2.md`; `scope-01.md`; `scope-01-recovered.md`; the inventory-only §10.7 records `phase-outputs/reviews/{phase2-review-dispatch.md,phase2-verification-dispatch.md,phase3-review-dispatch.md}`, the four `resume-analysis/*.md` files and `.claude/agent-memory/rf-qa/.probe` (existence only, no line load).
- **P4:** `research/06-session-0690ee9f.md`; `scope-rules.md`; `scope-02.md`; `scope-03.md`; `scope-03-recovered.md`; `research-notes.md`; `session-manifest.txt`; `historical-review-rules.json`; `gaps-and-questions.md`; `phase-outputs/discovery/input-inventory.md`.
- **Split by exact ranges, with no gaps or overlaps:**
  - `research/evidence-deck.md` (900 lines): P1 158, P2 126, P3 128, P4 488.
  - `research/screening-handoffs-source.txt` (453 lines): P4 1-213, P1 214-382, P2 383-453.
  - `research/screening-recovery-source.txt` (703 lines): P4 1-66, P2 67-91, P4 92-110, P3 111-167, P4 168-703.
  - `research/deep-handoffs-first-source.txt` (675 lines): P1 1-374, P2 375-675.
  - `research/deep-handoffs-remaining-source.txt` (891 lines): P3 1-573, P4 574-891.

**Sampled sessions:** All 30 manifest slots have an owner or are explicitly unassigned.
- P1 (slots 19-24): Orca planning 20, control 19, synthetic 21-24.
- P2 (slots 01, 27): documentation 01, oracle 27.
- P3 (slots 04, 05): CI 04, monitor 05.
- P4 (all others): credential 15, plus 02, 06-14, 16-18, 25, 26, 28-30.
- Index 03: excluded by design.

**Counts:**
- External paths the report cites directly: 22 groups (above), all owned.
- Primary paths reached only through a case file: 41, all owned and marked "via case".
- Git-only object groups: 5.
- Unavailable historical items: 9, plus the two deliberately unassigned logs.
- Source paths with zero owners: 0. Source paths with more than one owner: 0. Cross-reads are listed separately and do not transfer ownership.

## Balance Summary

| Partition | Text source lines assigned | JSONL physical lines (whole files) | JSONL lines in assigned record spans | Assigned reading load (text + record spans) |
|---|---:|---:|---:|---:|
| 1: Orca planning, slots 19-24, debate, gate/task records | 6,383 | 2,169 | 1,069 | 7,452 |
| 2: Oracle, documentation/render, cards, synthesis, QA records | 6,181 | 2,779 | 1,441 | 7,622 |
| 3: CI plan and Orca monitor | 4,443 | 3,327 | 2,954 | 7,397 |
| 4: Credential finals, negatives/controls, current rules, cross-case research | 4,586 | 21,345 | 2,871 | 7,457 |
| **Total** | **21,593** | **29,620** | **8,335** | **29,928** |

- **Threshold check:** Assigned source lines total 29,928, far above 1,000. Text sources alone are 21,593. Under SKILL.md Gate 4 (lines 407-410) and template I21/M4 (lines 784 and 1106), four actual fidelity agents are required, one per partition.
- **Balance:** Assigned reading load per partition is between 7,397 and 7,622, within 3.1% of each other. Partition 4's large whole-file JSONL total comes from the 18 screening logs. Their dispositions are carried by the screening captures; only the listed records need reading.
- **Thematic assignments made for balance:** Gate and task records sit in Partition 1, and the QA, synthesis-component and card records sit in Partition 2. They are assigned there to even the load, not because of a case connection.
- **Full report:** every partition reviews `R/RESEARCH-REPORT-review-loops.md` lines 1-1310 (sha256 `9ac64f1353fb9a6ea228af727183d3434788807498219150a54275a84ad8e568`).
- **Changes observed since the report's own measurements:**
  - CI log: 1,156 lines now, 1,153 recorded at 04:37Z.
  - Orca ledger: 53 lines now, 42 recorded at 04:03:52Z.
  - `t12-monitor-yaml.log`: 33 physical lines now, 34 recorded in case 05.
  - `qa/`: 232 files now, 207 recorded at assembly.
  - These are growth since the report's measurements, not new evidence about the cases.
