# Consolidated Task-Integrity Findings — TASK-RF-uc2-reachability

**Gate:** A.10 (2 rf-qa structural) + A.10.25 (1 rf-analyst alignment) + A.10.5 (2 rf-qa-qualitative content).
**Result:** 3 PASS (b2-self-containment, research-alignment, qa-gate-sufficiency/doctrine) + 2 FAIL (phase-structure, operational-correctness). All defects are task-file INSTRUCTION edits — no re-architecture. Apply all fixes in-place, then verify.

## Fixes to apply (single serialized fix agent, fix_authorization: true)

**F1 [IMPORTANT — operational #1 / sufficiency NOTE-1 / alignment B] — the wrong-edit risk, highest priority.**
The tasklist (Steps 3.3 / 3.4 and the PG.2/PG.4 references, and any "2 cosmetic sites" framing) instructs the executor to "refresh cosmetic site SKILL.md:1558 so it reads 1.6.0". **SKILL.md:1558 is the SYMBOLIC placeholder `"<contract_version from §9.1>"` — it AUTO-DERIVES and MUST NOT be hand-edited** (editing it would de-parameterize a template reference = a defect). Correct the instruction everywhere it appears: the contract_version change touches the **3 gate sites** (`:663` literal, `:804` prose, `:1772` kill-list test) PLUS **exactly ONE cosmetic literal refresh at `:1641`** (the stale `skill_version: "1.5.0"` in the JSON example). Remove `:1558` from the edit set; instead note `:1558` auto-derives from §9.1 and needs NO edit. Reword "2 cosmetic sites" → "1 cosmetic literal (:1641); :1558 auto-derives, do not edit".

**F2 [IMPORTANT — phase-structure #1] — FR-RSR.7 placement reconciliation.**
FR-RSR.7 (contract) sits in Phase 3 (Gather), but TDD §23.2 maps it to P5 (Surface). Add a one-line reconciliation NOTE to the Phase 3 header: the TDD wins on scope, but spec §10 ("For sc:tasklist", spec.md:739) EXPLICITLY authorizes parallelizing the contract task with the sweep, AND forward-reference coherence requires the contract field `runtime_surface_unreached` to be DEFINED before the Phase-4 §5.3 gate reads it — so the contract is correctly co-located with the sweep in P2/Phase-3. Do NOT move the task; just record the reconciliation.

**F3 [IMPORTANT — phase-structure #2] — FR-RSR.8 placement reconciliation.**
FR-RSR.8 (fail-open) has no row in the TDD §23.2 phase table (TDD §5.1 maps it to §6.5/§0.5d consumers; design §12.3). Add a one-line NOTE where FR-RSR.8 lives: it is WIRED INTO the sweep (P2/FR-RSR.2) and VERIFIED independently; its placement alongside Surface/Classify is acceptable and intentional. Record the reconciliation.

**F4 [MINOR — operational #3] — eval "run-and-confirm" honesty.**
Steps 7.8/7.9 assert the grader can "run and confirm FAIL-pre/PASS-post + byte-identical determinism", but the eval workspace grades PRE-PRODUCED `eval-*/` trees and there is no in-workspace producer that materializes cases / runs the skill (the existing 36 evals are STUBS authored to a convention). Reword 7.8/7.9: the executor AUTHORS the 5 cases with real fixtures + correct assertions + evals.json registration (matching the existing-36-stub convention); the FAIL-pre/PASS-post (old_skill/ vs with_skill/) and determinism are the ASSERTION DESIGN the eval harness executes when run. IF the eval runner/producer is available, run it to confirm; ELSE assert structural completeness (case dirs + expected.yaml + registered ids 37–41 + assertions present) and note the case is graded by the eval harness. Keep it honest — do not claim an in-task run that the workspace cannot perform.

**F5 [MINOR — operational #2 / structure] — §6.1 step-label ordering.**
Inserting 4b'/4b "after step 4 (:463)" places them before the existing `4a` (reuse-auditor, :464), giving doc-order labels `4, 4b', 4b, 4a`. No functional impact (dependency-satisfied doc list), but specify ordering: insert 4b'/4b AFTER the existing `4a` (i.e. after :464) so the chain reads `4, 4a, 4b', 4b`, OR explicitly state the label coexistence is accepted. Pick the after-4a insertion for clean ordering.

**F6 [MINOR — structure #3] — M3 gate halt precedence.**
In the final M3 gate (PG.10 verification/retry), add the one-line precedence: regression-detection halt is evaluated BEFORE the monotonicity halt on every fix-cycle transition (regression > monotonicity), per the Retry Monotonicity Protocol. Cheap clarification.

**F7 [MINOR — alignment C] — count-invariant cross-check.**
Step 7.1's precomputed top-level scalar (`count_invariant_holds`) for eval id 41 is self-attesting by the skill-under-test. Add a paired cross-check: also emit `runtime_surface_unreached` and a `unreached_surfaces_len` top-level scalar and assert equality via two yaml_field checks, so the invariant is graded from two independently-emitted scalars rather than one self-attesting boolean. (Enhancement; keep the precomputed-scalar approach, just make it cross-checkable.)

## NOT fixes (verified non-issues)
- B2 H4: `deviation_counts.regression` (eval-oracle schema, post-small-diff-clean/expected.yaml:6) vs `deviation_count_by_class.regression` (SKILL contract field) is CORRECT discrimination, not a bug. Leave as-is.
- Item count 44 is correct for scope (not low).
