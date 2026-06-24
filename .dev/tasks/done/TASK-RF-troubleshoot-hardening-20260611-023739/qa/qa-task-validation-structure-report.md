# QA Report — Task Integrity (STRUCTURE / Phase-Ordering Lens)

**Topic:** Pipeline Hardening Closure mode (H0-H5) for sc:troubleshoot-protocol — RELEASE-SPEC v1.1.0
**Date:** 2026-06-11
**Phase:** task-integrity
**Lens:** phase-structure
**Fix authorization:** false (report-only)
**Fix cycle:** N/A

---

## Overall Verdict: PASS (with 1 IMPORTANT + 3 MINOR structural observations — none blocking)

This task file is structurally sound for the phase-structure / phase-ordering lens. The
§4.6 7-group implementation order is reproduced exactly, dependencies are correctly
ordered at both phase and item level, the G1 BLOCKING gate and OI HALT markers are
present, the FINAL_ONLY QA gate has 7 lens agents with serialized fix authorization, and
the advisory 4-token enum invariant is intact everywhere (no 3-token regression). The
issues below are refinements, not correctness defects.

## Items Reviewed (Phase-Structure Lens, 10 checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter complete/well-formed | PASS | `id`/`title`/`status`(🟡 To Do)/`type`("🔧 Refactor", L7)/`spec_path`(RELEASE-SPEC, L18)/`reflect_pre`(present, verdict "" L19-26)/`reflect_post`(present "" L27) all set. `tags`/`template_schema_doc`/`related_docs` populated. |
| 2 | Mandatory template sections present | PASS | Task Overview (L63), Key Objectives (L73), Prerequisites & Dependencies incl. Execution Context (L84/L111), Detailed Task Instructions (8 phases L161), Task Log / Notes (L423) all present. |
| 3 | Phase ordering matches spec §4.6 | PASS | Verified vs spec §4.6 verbatim: P2=group1+2 (skeleton→output-contract), P3=group3 (H1/H2/H4 parallel), P4=group4 (H3), P5=group5 (SKILL wiring), P6=group6 (report+handoff), P7=group7 (tests+sync+verify). Dependencies logical: output-contract (P2) before downstream wiring (P5/6); refs (P2-4) before SKILL trigger (P5); sync-dev (7.19) strictly before verify-sync (7.20). Refs read after creation in all cases. |
| 4 | Completion items in FINAL phase; POST reflect penultimate + self-run | PARTIAL (IMPORTANT-1) | Task Summary (8.15) + Mark Done (8.16) are inside the FINAL Phase 8 (anti-orphaning OK). POST reflect (8.14) is a SELF-RUN subagent ("Spawn a self-run subagent…", L413), NOT human-handoff/HALT — correct. BUT reflect is at 8.14 with **8.15 Write Task Summary intervening before 8.16 Done** — reflect is antepenultimate, not strictly penultimate. See IMPORTANT-1. |
| 5 | FINAL_ONLY QA gate ≥7 lens agents, serialized fix | PASS | 7 agents: 3 structural rf-qa (8.2 template/schema, 8.3 internal-consistency, 8.4 completeness) + 3 content rf-qa-qualitative (8.5 actionability, 8.6 domain-accuracy, 8.7 crossref-chain) + 1 domain advisory-invariant rf-qa lens (8.8). All `fix_authorization: false` report-only, parallel. Serialized fix: consolidate (8.9) → ONE fix agent (8.10) → 2-agent verification round (8.11) → conditional proceed max-2-cycles with FR-CONV.5 halt-precedence (8.12). |
| 6 | Task Log section at bottom | PASS | `## Task Log / Notes 📋` at L423 with Task Summary, Execution Log, per-phase Findings (P1-P8), Follow-Up, Deviations, Builder Notes subsections. |
| 7 | Item count reasonable (~56 / 8 phases) | PASS | 56 Step items: P1=7, P2=2, P3=3, P4=1, P5=3, P6=2, P7=22, P8=16. Matches the ~56 target. |
| 8 | G1 prerequisite BLOCKING before src edit; OI-2/3/5 HALT | PASS | G1 gate referenced 16× incl. dedicated "G1 Gate Prerequisite (BLOCKING — READ FIRST)" block (L86) + "No authoring item … may edit … until G1 approval" (L165) + Step 1.1 confirm-or-STOP. OI-2 (1.5), OI-3 (1.6), OI-5 (1.7) all "HALT — never auto-default" PENDING markers; OI-1/4/6 correctly excluded as in-spec resolved (L134). |
| 9 | TB-Add 1/4/7/8 | PASS | TB-Add-1: zero TBD/TODO/FIXME in any checklist body (the "3-token" hits are intentional anti-regression guard text). TB-Add-4: item deps form a DAG (refs→wiring→report→tests→QA→reflect→done, no back-edges). TB-Add-7: all 4 Source Areas (SKILL.md, refs/, commands/troubleshoot.md, tests/troubleshoot/) reappear in item Contexts; Execution Context block carries no `path:NN` file:line. TB-Add-8: per-item Contexts cite spec §-anchors + concrete file paths; net-new file items carry create-not-line semantics. |
| 10 | ADVISORY: no 3-token enum / "advisory removed" regression | PASS | Zero "advisory removed" / forbidding-3-token language. The 4-token `pass \| blocked \| advisory \| not_applicable` enum appears throughout (102 advisory mentions). Triple-guarded: Step 7.8 `test_verdict_aggregation_from_h_statuses` asserts both advisory rows 5/6, Step 8.8 domain lens, Step 8.14 reflect literal-enum check. |

## Independent Verification Evidence (tool-checked, not trusted from task text)

- Sibling refs cited by items EXIST: `refs/triage-checklist.md`, `refs/hypothesis-card-template.md` (Glob/ls).
- Files to MODIFY exist: `SKILL.md`, `commands/troubleshoot.md`, `refs/report-template.md`, `refs/remediation-handoff.md`.
- Anchor headings cited by Phase 1/5/6 exist VERBATIM in source: SKILL.md `## Output Contract` (L37), `## Wave Structure` (L77), `### Wave 1.7: Tier 1 — Hypothesis Formation` (L251), `### Wave 2: Confidence Gate` (L271), `### Wave 5: Synthesis + Report` (L385); report-template.md `## Rendering rules` (L205), `## Test-is-wrong rule` (L212), `## Behavior-is-documented rule` (L233).
- `parents[2]` convention claim is TRUE: `tests/skills/test_task_builder_merge.py:20` = `REPO_ROOT = Path(__file__).resolve().parents[2]`; the cited sibling test file exists.
- Net-new targets correctly DO NOT exist yet: `tests/troubleshoot/`, `refs/pipeline-hardening-closure.md`, `refs/hardening-output-contract.md` (CREATE semantics valid).
- Spec §4.6 implementation order read directly — matches the task's 7-group phase layout 1:1.

## Summary

- Checks passed: 9 / 10 (check 4 PARTIAL — non-blocking ordering nit)
- Checks failed (blocking): 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Steps 8.14 → 8.15 → 8.16 | The phase-structure checklist requires POST reflect to be PENULTIMATE (immediately before Update-status-to-Done). Here Step 8.15 "Write Task Summary" sits BETWEEN the reflect gate (8.14) and Mark Done (8.16), so reflect is antepenultimate. If the Task Summary edit is treated as a substantive post-reflect mutation, the reflect gate no longer validates the final task state. Low real-world risk because 8.15 only writes the Task Log Summary (a narrative section, not a spec/contract artifact) and 8.16 re-gates Done on QA+reflect+pytest PASS. | Either (a) reorder so 8.15 Write Task Summary runs BEFORE 8.14 POST reflect (making reflect strictly penultimate), or (b) add an explicit note in 8.16 that the Task Summary write in 8.15 is narrative-only and does not alter any reflect-validated artifact. Option (b) is the lighter fix. |
| 2 | MINOR | Overview L67 vs Phase 7 | Overview says "7 test modules" but Phase 7 authors `test_hardening_h0/h1/h2/h3/h4.py` + `test_hardening_verdict.py` + `test_hardening_output_contract.py` + (optional) `test_hardening_report_closure.py` (Step 7.12 says "create NEW file … alternatively MAY append to test_hardening_output_contract.py"). That is 7 or 8 modules depending on the executor's optional choice in 7.12. The "7 test modules" prose count is correct only if the executor takes the append path. | Soften the Overview to "7-8 test modules" or pin Step 7.12 to always create the dedicated module, to keep the prose count deterministic (prose-count-accuracy). |
| 3 | MINOR | Step 1.5 (OI-2) | The OI-2 PENDING marker body says the `contract_token` vocabulary feeds "`contract-enumeration.md` (Phase 3 Step 3.3)", but `contract-enumeration.md` is authored in **Step 3.2**, not 3.3 (Step 3.3 is `effective-input-proof.md`). The cross-reference step ID is off by one. | Change "Phase 3 Step 3.3" → "Phase 3 Step 3.2" in Step 1.5. (The OI-3 marker in 1.6 correctly cites Step 3.1; only the OI-2 marker mis-cites.) |
| 4 | MINOR | Step 3.3 / Phase 3 preamble | Residual confusion from the OI-2 stale "3.3" pointer (Issue 3): a reader chasing the OI-2 reference lands on the H4 ref instead of the H2 ledger ref. No independent defect in Phase 3 itself — Step 3.2 correctly creates `contract-enumeration.md` and reads the OI-2 marker. | None beyond fixing Issue 3. |

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 (folded into Bash grep) | Glob: 0 (folded into Bash ls) | Bash: 6
- Every checklist item was tool-verified: phase ordering against spec §4.6 (direct sed read), file existence (ls), anchor headings (grep on source), parents[2] convention (grep), item/phase counts (grep -c), advisory regression scan (grep -i), OI/G1 markers (grep). Tool calls ≥ checklist items — engagement minimum satisfied.
- No UNCHECKED or UNVERIFIABLE items.

## Recommendations

1. Apply the IMPORTANT fix (Issue 1): make POST reflect strictly penultimate, or annotate 8.16 that 8.15 is narrative-only. This is the only finding touching the lens's explicit requirement (checklist item 4).
2. Apply MINOR Issues 2-3 for prose-count determinism and a correct OI-2 cross-reference.
3. No blocking defects — the task file is approvable for execution from a phase-structure standpoint pending the G1 human gate it correctly enforces.

## VERDICT: PASS

(9/10 checks PASS, 1 PARTIAL non-blocking. 0 CRITICAL, 1 IMPORTANT, 3 MINOR. The IMPORTANT
item is a reflect-ordering refinement, not a correctness or anti-orphaning failure — completion
items are correctly inside the final phase and Done is re-gated on QA+reflect+pytest PASS.)

## QA Complete
