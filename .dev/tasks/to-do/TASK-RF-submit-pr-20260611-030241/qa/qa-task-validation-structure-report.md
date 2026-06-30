# QA Report — Task Integrity (Structure / Phase-Ordering Lens)

**Topic:** sc:submit-pr skill build — task file structure & phase ordering
**Date:** 2026-06-11
**Phase:** task-integrity
**Lens:** phase-structure
**Fix authorization:** false (report-only)
**Adversarial stance:** ACTIVE — assume errors exist, target ≥5 findings

---

## Scope

Task file: `.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/TASK-RF-submit-pr-20260611-030241.md`
Spec: `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`
Template: 02

## Checklist Results (Phase-Structure Lens, 10 items)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed (spec_path, reflect_pre, reflect_post, start_commit provenance) | PASS (with note) | Lines 1-59: well-formed YAML, all template-02 fields present incl. `spec_path` (L18), `reflect_pre` block (L19-26), `reflect_post` (L27). `start_commit` is NOT in frontmatter at build time but Step 1.2 (L183) explicitly inserts it after `spec_path` at execution start, capturing merge-base `HEAD origin/master`; reflect (L462) resolves base the same way. Provenance chain intact. |
| 2 | All mandatory template-02 sections present | PASS | Verified vs `02_mdtm_template_complex_task.md` PART 2 headers: Task Overview (L63), Key Objectives (L71), Prerequisites & Dependencies + Parent/Previous-Stage (L82/84/89), Execution Context + References/Source Areas/Key Constraints/Handoff/Frontmatter-Update (L103-161), Detailed Task Instructions (L169), Post-Completion Actions (L452), Task Log/Notes + Task Summary/Execution Log/Phase-Findings/Follow-Up/Deviations (L466+). Open Questions (L163) present. |
| 3 | Phase ordering follows spec §3 DAG + L5 contract-verdict gate (not just prose) | PASS (with defects) | Spec §3 DAG (spec L133-146): [0]DET→[1]C1 skeleton→[2]C3/C3a/C3b→[3]VAL+S3_FIXING→[4]C4 reply/resolve→[5]LG+run-log→[6]hook+suite+sync. Task maps Ph2=[0], Ph4=[1], Ph5=[2], Ph6=[3], Ph7=[4], Ph8=[5], Ph9-11=[6]; headers cite "spec §3 step [N]" explicitly. L5 gate is REAL not prose: Step 2.6 writes `contract-verdict.md` PASS/FAIL; Gate A PGA.5 appends "GATE A: PASS — Phase 4+ authorized"; Phase 4 header (L241) hard-blocks on that string; Phase Gate B blocks on `validation-verdict.md` VERDICT:PASS. Defects: stale phase refs (Issue #1). |
| 4 | research→build→test→validate progression; no forward dependency on unbuilt module | PARTIAL | Build order sound module-wise (models→detection/classifier→fsm→router→run-log→loop-guard→recovery). Forward deps exist: (a) Step 2.4 test references fixtures created in Phase 10 (mitigated by inline payloads, never reconciled — Issue #3); (b) Step 4.3 `__init__.py` re-exports `remap_severity` from `severity_router.py` not built until Phase 5 (conditional defer — Issue #4); (c) test modules in Ph2/4-9 import conftest/fixtures created Phase 10, full suite runs Phase 11 (acceptable). |
| 5 | Completion items in final phase (anti-orphan); POST reflect penultimate, SELF-RUN, not human HALT | PASS | Post-Completion Actions (L452-464) all under final section. Reflect item (L462) penultimate, immediately before Update-status-to-Done (L464). Explicitly "SELF-RUN subagent, NOT a human HALT"; `git add -A` before; `/sc:reflect --mode post --depth deep` (not quick, not /sc:task); records `reflect_post`; records `verdict=error` + proceeds on failure (no orphan-block). |
| 6 | Task Log section present at bottom | PASS | `## Task Log / Notes 📋` (L466) with Task Summary, Execution Log, per-phase Findings (incl. "Phase 3 - (reserved)" L514), Phase Gate Findings, Follow-Up, Deviations. |
| 7 | Item count reasonable (~89 for 12 skill files + 8 Python + 21 tests + cmd + hook + markers) | PASS | 89 `- [ ]` items (grep). Matches the ~89 estimate exactly. Per-phase distribution reasonable (Ph8=10 for LG+run-log+recovery+tests; Gate B=14 for M3+M4). |
| 8 | Open Questions documented (R1 probe) | PASS | Open Questions (L163-167): R1 DET probe operability (operator decision, HALT, locked:false), Monitor≠daemon V1 limit, troubleshoot edit-application seam. R1 surfaced as PENDING + Follow-Up (L541). |
| 9 | QA gates follow MDTM M3 + I20 serialized fix; agent floors; M4 source-fidelity present | PASS | Gate A: 5 lens agents = 2 rf-analyst (L224-225) + 2 rf-qa (L226-227) + 1 rf-qa-qualitative (L228) → consolidate (PGA.3) → single fixer fix_auth:true (PGA.4) → 2-agent verify (PGA.5). Meets I19 floor=5. Gate B M3: 3 rf-qa (PGB.2) + 3 rf-qa-qualitative (PGB.3) = 6 → consolidate → single fixer → 2-agent verify. M4: 3 rf-qa partition agents (PGB.7) → consolidate/fix/verify (PGB.8), runs AFTER M3 PASS. Lens spawns fix_auth:false; serialized fix single-agent (I20). |
| 10 | TB-Add-1/4/5/7/8 structural gate additions | PASS (with notes) | TB-Add-1: no real TBD/TODO/FIXME ("TODO-free" in Step 4.3 L250 is a false positive — instructs AVOIDING todos). TB-Add-4: item deps form a DAG; Step 4.3↔Phase 5 edge (Issue #4) is forward not cyclic. TB-Add-5: items mostly atomic; Step 4.3 decision-deferral-heavy (Issue #4). TB-Add-7: "Source Areas" (L116-124) — all 8 entries reappear in item Context fields; block has NO file:line refs (verified L103-137 clean). TB-Add-8: per-item Context cites spec file:line/§ throughout. |

---

## Additional Structural Verifications

- **Spec §11.3 event count:** Independently counted spec L723-730 event block = exactly 32; +`push_aborted_or_not_landed` (spec L771) = 33. Task's "33 events (32+1)" claim (Steps 2.2/8.1/8.3) is CORRECT and well-grounded. Deviations note's "prompt's '30'" is a benign provenance remark.
- **FSM state set:** Step 2.2 `MonitorState` enum vs spec §5.1 (spec L249-340) — all spec states present. One naming drift flagged (Issue #2).
- **Hook line count:** `offer-pr-review.sh` is 74 lines — matches Step 9.2's "74 lines" claim.
- **Reuse target existence:** `severity-rubric.md` exists (verified). REUSE-by-reference correctly cited.
- **Phase numbering:** 1, 2, Gate A, 4, 5, 6, 7, 8, 9, 10, 11, Gate B — Phase 3 deliberately skipped (reserved, L514). Intentional but creates stale "Phase 3"/"Phase 12" references (Issue #1).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | Step 2.6 (L214); Step 11.6 (L416) | Stale forward-references to NON-EXISTENT phases. Step 2.6 on FAIL says "re-run Step 2.5 before proceeding to **Phase 3**" — there is no Phase 3 (reserved; next is Gate A→Phase 4). Step 11.6 on PASS writes "**Phase 12** final QA authorized" — no Phase 12; final QA is Phase Gate B. An executor following these literally is misdirected on the proceed-path. | Step 2.6: "before proceeding to Phase 3" → "before proceeding to Phase Gate A". Step 11.6: "Phase 12 final QA authorized" → "Phase Gate B final QA authorized" (in both item body and the `validation-verdict.md` string it writes). |
| 2 | MINOR | Step 2.2 (L202) vs Steps 4.1/6.3 + Phase 6 header (L244/L296/L297/L286) | State-name drift: `models.py` enum member is `S4_HALT_BEFORE_PUSH` (no prime — correctly, since spec canonical `S4'_HALT_BEFORE_PUSH` has an apostrophe illegal in Python identifiers), but every prose/ref reference uses `S4'_HALT_BEFORE_PUSH` (with prime). The PGB.2 INTERNAL-CONSISTENCY lens is told to check "FSM states in state-machine.md match models.py" and will flag this mismatch. The `'`→`_` adaptation is undocumented in Key Constraints/Deviations. | Add a 6th spec-correction note: "`S4'_HALT_BEFORE_PUSH` (spec) → `S4_HALT_BEFORE_PUSH` Python enum member (apostrophe illegal in identifiers)." OR instruct state-machine.md to use the unprimed spelling for the enum-bound state. |
| 3 | MINOR | Step 2.4 (L208) ↔ Phase 10 (L388-394) | Forward-dependency reconciliation gap: Step 2.4 writes `test_detection_contract.py` with BOTH inline payloads (standalone Phase-2 run) AND fixture references (`review-clean.json` etc.) created in Phase 10. No later item swaps inline→fixture, so inline persists as harmless duplication or fixture refs go unused for T-210. Step 2.5 also runs pytest before conftest/`__init__.py` exist (works — conftest optional — but fragile). | Add a Phase-10 reconciliation clause: "if `test_detection_contract.py` was authored with inline payloads in Phase 2, keep inline as the standalone-collect guarantee; fixtures are additive." OR have Step 2.4 use ONLY inline payloads and defer fixture-backed assertions to Phase 10. Make the end-state explicit. |
| 4 | MINOR | Step 4.3 (L250) | Decision-deferral / atomicity (TB-Add-5): the `__init__.py` re-export item embeds branching choices ("re-export `load_fixture` here OR in conftest in Phase 10 — choose per repo precedent"; "add `remap_severity` now as a guarded forward import OR in Phase 5 — note it"), a forward edge onto Phase 5's `severity_router.py` woven into a Phase 4 item, leaving the executor to pick a path. | Determinize: Step 4.3 re-exports ONLY Phase-2/4 symbols (`run_skill`, `poll_augment_review`, `classify`, models); make Step 5.1 the sole owner of the `remap_severity` re-export (it already adds it). Pick one home for `load_fixture` (conftest, per spec §6.3 which lists it as a conftest fixture) and state it. |
| 5 | MINOR | Step 2.6 (L214) | The PASS-branch verdict text "downstream phases (4+) AUTHORIZED" is misleading: Phase 4 is NOT authorized by Step 2.6 — it is gated on Gate A's "GATE A: PASS — Phase 4+ authorized" (L237/L241). The Step 2.6 claim could let an executor skip Gate A. | Reword Step 2.6 PASS verdict: "detection-contract gate PROVEN; proceed to Phase Gate A (which authorizes Phase 4+)" so the authorization owner is unambiguous. |

---

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (all 10 lens items verified with tool evidence; "PASS-with-defects" items are still fully verified — the defects ARE the findings, not verification gaps)
- **Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 6 (event-count, item-count, header-extraction, line-count, gate-chain trace, TBD scan)
- No UNCHECKED items. No UNVERIFIABLE items.
- Tool-call count (10) ≥ 10 checklist items — engagement minimum satisfied.

---

## Summary

- Checks passed: 10 / 10 (3 with embedded defects rated as findings)
- Issues found: 5 (0 CRITICAL, 1 IMPORTANT, 4 MINOR)
- The task file is structurally sound: all template-02 sections present, phase ordering faithfully implements the spec §3 DAG with a REAL L5 contract-verdict gate (not prose), QA gates meet M3/I20/I19 floors, M4 source-fidelity gate present, POST-reflect correctly placed as a penultimate SELF-RUN gate, anti-orphaning satisfied, item count (~89) matches scope.
- Findings are corrective polish, not structural failure. Issue #1 (stale Phase 3 / Phase 12 references) is the only IMPORTANT item: it misdirects the executor's FAIL/PASS proceed-path. The 4 MINOR items reduce executor friction (notably the `S4'`→`S4_` drift the internal-consistency lens will trip on) but do not block correct execution.

---

## VERDICT: FAIL

**Rationale:** Per zero-tolerance task-integrity standards, ANY finding regardless of severity = FAIL. 5 issues found (1 IMPORTANT + 4 MINOR). The IMPORTANT finding (stale Phase 3 / Phase 12 forward-references) actively misdirects the executor's proceed-path and must be corrected. The MINOR findings should also be resolved to prevent the internal-consistency lens (PGB.2) flagging the documented-but-unannotated `S4'`→`S4_` state-name adaptation as a real mismatch, and to remove the two forward-dependency ambiguities. None of the findings indicate structural redesign — they are surgical text corrections. After fixing the 5 items, this task file is structurally ready for execution.

---
