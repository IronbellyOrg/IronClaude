# A.10 consolidated findings and fix log: revision R2 (plan-defect fixes F-01 to F-10)

Date: 2026-11-10. Reports consolidated: `qa-task-validation-b2-report.md` (agent ab0a027e59951d68b, cycle 0, FAIL, 2 blocking) and `qa-task-validation-structure-report.md` (agent a25282e247c1611a7, cycle 0, FAIL, 1 blocking). Plan sha256 at cycle 0: 7b1881237f7aafe7954af9b5e60e0f1bc7912dd43098157b009903fa9910ea77.

## Cycle 0 blocking findings (F0 = 3)

| Id | Where | Defect | Fix applied (cycle 1) |
|---|---|---|---|
| B2-1 | 7.20 Action (TL:1293) | The new execution-authorization check said "match the owner's words in the revision BUILD-REQUEST files" without naming the file that holds them | Names the R2 `BUILD-REQUEST.md` `## Authorization (direct, by the owner)` section, or a later dated owner message supplied with the fresh reports |
| B2-2 | 7.30, 7.34 Action (TL:1363, 1391) | "OQ-17 and OQ-18 decision files named in item 7.20" pointed to another item | Both full paths written into 7.30 and 7.34 |
| S16-1 | 8.19 Context (TL:1550) | No file:line or justified absence for the code surfaces it names (TB-Add-8) | Appended an `<!-- evidence-absence: ... -->` comment on the same physical line |

## Cycle 0 minor notes (not fixed, never fail the gate)

Five B2 notes (N-1 to N-5, including the "advice the sweep skill prohibits" wording and the two long lines 7.16 Context and 7.17 Action that are identical to the baseline) and structure notes M1 to M5 (S14 "Ensure" prefix on 7.10 and 11.4 Verification, same as baseline; delta-manifest row omitted line 1980, corrected in `delta-manifest.md`).

## Fix log (cycle 1, performed by the revision builder as the single fixer)

Three Edit calls to the task file; no other file touched. Then `qa/preservation_check.py` re-run: PASS (355 headers, 137 completed items untouched, 64 labels, 73 changed lines, 3020 lines). Plan sha256 after cycle 1: eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99.

Post-edit checks: `grep -c 'named in item 7.20'` = 0; `grep -c 'evidence-absence: the sweep modules'` = 1; `grep -c 'plan-defect-fixes-20261110/BUILD-REQUEST.md'` = 3 (7.20, 7.30, 7.34).

## Cycle 1 verification

Verifier afd6029f1537b52aa (`qa/A10-verify1.md`): VERDICT PASS, blocking 0. B2-1, B2-2 and S16-1 closed; no regression; structural table S1 to S16 PASS (S13, S14, S15 with carried MINOR notes). Plan sha256 verified: eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99.

## Items Reviewed

| Id | Checklist item | Result | Evidence |
|---|---|---|---|
| S1 | YAML frontmatter complete and well-formed | PASS | Parsed, 35 keys, required fields non-empty, `reflect_pre` present; lines 1-1209 equal to baseline |
| S2 | All mandatory sections present | PASS | 49 `#` heading lines identical to baseline (Task Overview, Key Objectives, Prerequisites, Execution Context, Detailed Task Instructions, Phases 1-14, Task Log at line 2800) |
| S3 | Phase dependencies logical, no cycles or gaps | PASS | Per-phase counts 4/25/23/24/30/22/37/29/21/24/21/21/25/49 = 355; contiguous numbering; every item reference in the four cycle-1 lines points backward or at itself (7.20 to 7.17; 7.30 to 7.20 and 6.3; 7.34 to 7.20, 7.33 and 6.3; 8.19 to 8.6) |
| S4 | Logical progression | PASS | Phase order unchanged from baseline; cycle 1 changed no header or order |
| S5 | Completion items in the final phase | PASS | 14.46 task summary, 14.47 POST diff file, 14.48 post-execution reflection gate, 14.49 status Done at the end of Phase 14 |
| S6 | Task Log section at the bottom | PASS | `## Task Log / Notes` at line 2800; lines 2747-3020 identical to baseline |
| S7 | Item count reasonable | PASS | 355 items (218 open, 137 done), unchanged |
| S8 | Open Questions and gaps documented | PASS | Task Log unchanged; OQ-17 and OQ-18 remain the conditional records that 7.17 writes and the F-01 text handles |
| S9 | QA gates follow M3 and M4 | PASS | No gate item added, removed or reordered; cycle 1 touched 7.30/7.34 Action text (path restatement) and 8.19 Context only |
| S10 | TB-Add-1 placeholder scan, no title-only item | PASS | 23 TBD/TODO lines, all quoted instructions and identical to baseline; every item has all five fields |
| S11 | TB-Add-3 clarification adjacency | PASS | 7.17 Context names OQ-17/OQ-18 as blockers; 7.20-7.36 name the OQ records by file name; no new blocked item |
| S12 | TB-Add-4 no cycles | PASS | Backward-only references in the changed lines; 11.4 requires 7.10 ticked and 7.10 does not require 11.4 |
| S13 | TB-Add-5 granularity | PASS with note | No item added, no second source mutation per item. Cycle 1 lengthened three Action lines (1293 by 246 characters, 1363 by 171, 1391 by 171); the R1 note and the BUILD-REQUEST rule justify line-stable in-place growth (carried MINOR) |
| S14 | TB-Add-6 uniform `Verify:` prefix | PASS with note (MINOR) | 353 of 355 start `Verify:`; 7.10 (1212) and 11.4 (1982) start "Ensure ...", the same two as the baseline and cycle 0, accepted as cosmetic; the file has no Acceptance Criteria entries |
| S15 | TB-Add-7 source areas | PASS (`tb-add-7-degraded-tolerated`) | No `**Source areas:**` line; lines 119-206 identical to baseline; carried MINOR: one `gaps-and-questions.md:138` reference in the frozen constraint block |
| S16 | TB-Add-8 per-item Context evidence binding | PASS | All 64 changed labels bind their Context (0 unbound); 8.19, the cycle-0 FAIL, is now bound by the evidence-absence comment |
