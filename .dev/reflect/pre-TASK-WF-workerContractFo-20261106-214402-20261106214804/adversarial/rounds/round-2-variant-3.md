# Round 2: Variant 3 rebuttal (opus, refactorer)

Persisted by the orchestrator on receipt, 2026-11-06T22:07:40Z.

## Response to criticisms

Steelman: V1 and V2 are right that V3 classified unevenly (a calibrated P2 parked as advisory, style findings weighted like defects, a pin a clause can satisfy without excluding anything).

1. R3-A1 parked as advisory: CONCEDED, now gating P2. Task 1 adds the unconditional "the report names where those files were written" (plan :30, source.md:13); workflow's report is the plan `<id>.md` (return-contract.md:52) and the skill forbids editing it after reflect (sc-workflow-protocol/SKILL.md:62). R3-A1 merges into R1-2; take V1's narrowed fix (conditional wording or a workflow note, owner note).
2. R3-1 should be P3: CONCEDED IN PART. The live spec has 0 hits for `check-ignore`, `runs.jsonl`, `git refuses`, `git ignores`; PR #411 (cb8f2f81) changed it by 2 insertions and 2 deletions while adding the per-command rule; header :3 "Planning only: nothing here is implemented". So the remedy is "record that the spec stays unchanged", not an edit. P2 kept for the dropped check (source.md:14 names a spec copy; plan :30 searches only tests/ and plugins/). Verifier: the plan records the spec decision.
3. R3-4 style: CONCEDED (build.md:104 overlap violates no AC, plan :57; only the goal line plan :15). R3-5: CONCEDED IN PART; return-contract.md:43-54 never names WORKER-CONTRACT.md; sibling ref input-parse.md:16 uses "`~/.claude/WORKER-CONTRACT.md` (rule WC-4)". P3, return-contract.md only.
4. "left out per WC-4" needs a test condition: CONCEDED. Task 4 pin requires "left out" + "WC-4" + `[]`, mirroring :799 and :808. Token pins can still be gamed ("nothing is left out"); matching build/workflow pins is the realistic bar; AC review (qa.md:27-31) is the second guard. Drop "which the test report names instead".
5. "no criterion forbids src/superclaude/" half true: CONCEDED. `_check_unattended_section` asserts it for command sections (:517); return-contract.md (`_WORKFLOW_RETURN_REF`, :855) is read at :805 and :936 without that check. All nine `specs/history/spec-v*.md` snapshots restate WC-4 (lines 62-72); the search must exclude them.

## Grading rule: choice and resulting grades

Choice: Variant 2's amendment, tightened. P1 = a false pass shown under the plan's literal instruction, or a blocker; if the false pass needs the implementer to choose one of two readings of an ambiguous instruction, it is P2. AC review does not lower grades (qa.md:27-31, :49).

| Finding | Grade | Evidence |
|---|---|---|
| R1-1 | P1 | init-lite.md:92 old sentence plus "exited 0" passes the only new assertion (plan :76). For SKILL.md the absence check must read the whole text: `worker_status` precedes `artifacts` (SKILL.md:61), outside `_artifacts_clause` (:769-774). |
| QA-1 | P1 | V2's witness passes the pin as written (plan :66) while contradicting plan :69. Fix: add "left out". |
| R1-4 / R3-3 | P2 | "the WC-4 text read from CONTRACT_PATH" (plan :30) has two readings; the false pass needs the whole-file one; "git ignores" and "outside the repository" are absent from WORKER-CONTRACT.md today. |
| R3-1 | P2 | Brief-named check dropped by search scope; fix is a recorded decision. |
| R1-2 / R3-A1 | P2 | New shared rule text false for workflow (return-contract.md:52; SKILL.md:62). |
| R1-3 / QA-2 / R3-2 | P3 | AC vacuous (AUDIT_ROOTS :1054-1058). |
| R3-4, R3-5, R1-6 | P3 | No AC violated. |

## Updated assessment of other variants

- V1: strongest on Task 5 (R1-1, R1-5); its rule cannot grade coverage or rule-text findings; its clean claim stays too narrow.
- V2: QA-1 holds as narrowed; its amended rule is the more general one and is adopted.
- V3: unique value is scope (R3-1, R3-A1 once gating); missed R1-1 and QA-1; R3-2 fix weaker than R1-3.

## New evidence

1. Spec :72 has 0 hits for the new-rule terms; PR #411 changed the spec by 2+/2-; header :3 "Planning only".
2. "git ignores" and "outside the repository" absent from WORKER-CONTRACT.md today; a whole-file assertion passes falsely only if misplaced.
3. test.md:103 has no `artifacts` token today; R1-6 hazard not live; the new clause must add the token.
4. return-contract.md read at :805 and :936 with no src/superclaude/ check; only command sections are guarded (:517).
5. sc-workflow-protocol/SKILL.md:62 forbids editing `<id>.md` after reflect, so workflow's report cannot meet the new WC-4 duty without rewording.

## Updated per-point positions

| Point | Superior | Reason |
|---|---|---|
| S-001 | Tie | Shape changes no finding; the advisory block hid R3-A1 |
| C-001 | V1 | R1-3 rebinds to a contract-reading test (:573-574); P3 |
| C-002 | Tie V1/V3 | Same slice; P2 |
| C-003 | V1 | R1-2 gating P2; R3-A1 merges |
| C-004 | V2, narrowed by V3 | QA-1 P1; pin "left out" + WC-4 + `[]` |
| C-005 | V1 | R1-1 P1; SKILL.md check reads whole text |
| C-006 | V3 | P2 dropped check; recorded decision; exclude specs/history/ |
| C-007 | V3 | P3 against goal line :15 |
| C-008 | V3, narrowed | return-contract.md only |
| C-009 | V1 | Verified exit paths |
| C-010 | Tie | Advisory, outside brief |
| X-001 | V2/V3 synthesis | Pin exclusion token; reporting duty only in WC-4 |
| X-002 | V1/V3 | P3 |
| X-003 | V3 | Tracked spec copy |
| A-001 | Tie | Corrections need owner revision or in-task application (SKILL.md:62) |
| A-002 | Tie | AC review is a second guard; does not lower grades |
