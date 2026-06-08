# Variant 1: /task QA Architecture (Rigorflow F1 Executor)

## 1. Architectural Identity

`/task` is an **execution-time** QA architecture. It validates artifacts as they are produced during MDTM task-file execution, applying QA at phase boundaries within the live F1 loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT).

## 2. Two-Layer Verification Stack

### Layer 1 — Phase-Gate QA (mandatory after every phase ≥2)

- **Agent**: `rf-qa` (subagent_type: rf-qa, mode: bypassPermissions)
- **Stance**: ADVERSARIAL — "Assume the work contains errors. A verdict of 0 issues requires evidence you thoroughly checked."
- **Authority**: `fix_authorization: true` — auto-fixes in-place
- **Input**: All files created/modified during the just-completed phase + "ensuring..." clauses extracted from checked items as acceptance criteria
- **Output**: `{TASK_DIR}/reviews/qa-phase-{N}-report.md`
- **Gate behavior**: BLOCKS the next phase from starting until verdict is PASS or FAIL-with-all-fixes-applied
- **Fix-cycle bound**: max 3 cycles; on 3rd failure, HALT execution and ask user for guidance
- **Partitioning**: when >6 output files, spawn multiple rf-qa instances with `assigned_files` subsets and merge

### Layer 2 — Post-Completion 2-Step Validation (final phase only, before task marked Done)

- **Step 2a — Structural** (rf-qa, qa_phase: report-validation): cross-phase consistency, orphaned outputs (created but never consumed), missing outputs (referenced but never created), full-task-file "ensuring..." satisfaction sweep
- **Step 2b — Qualitative** (rf-qa-qualitative, qa_phase: task-qualitative): 15-item operational checklist:
  1. Gate/command dry-run
  2. Project convention compliance
  3. Intra-phase execution simulation
  4. Function signature verification
  5. Module context analysis
  6. Downstream consumer analysis
  7. Test validity
  8. Test coverage
  9. Error path coverage
  10. Runtime failure path trace
  11. Completion scope honesty
  12. Ambient dependency completeness
  13. Kwarg sequencing red flags
  14. Function existence claims verification
  15. Cross-reference accuracy for templates
- **Authority**: both layers `fix_authorization: true`
- **Failure handling**: both PASS → mark Done; either FAIL with fixes → verify fixes, then proceed; either FAIL with unfixable → log, present, ask user

## 3. Architectural Invariants

- **No exceptions**: phase-gate QA runs on every Phase 2+. Not optional.
- **Re-read on every item**: the F1 loop re-reads the task file before each action; the QA agent reads ACTUAL output files (zero-trust).
- **fix_authorization in scope**: QA agent CAN modify any output file to resolve findings, including test files.

## 4. Operational Characteristics

- Token cost: ~5-15K per phase-gate QA invocation; ~10-20K for post-completion 2-step
- Wall-clock impact: blocking — phase N+1 cannot start until phase N gate passes
- Applicable to: any MDTM-shaped task file; agnostic to code/docs/config/infra mix
- Failure modes: QA agent crash → fallback per Error Handling; fixer regression → caught by next cycle (up to 3)

## 5. Theory of Defects

Defects are caught at the EXECUTION TIME of the work that produces them. Validation is grounded in actual outputs on disk, not in plans. The adversarial-stance + zero-trust verification model assumes the fixer will produce flawed work and surfaces those flaws before they propagate to the next phase.

## 6. Documented Limitations

- No formal protection against test-gaming (rf-qa CAN modify tests under fix_authorization)
- No monotonicity guard preventing oscillation across fix cycles (only the 3-cycle hard cap)
- No evidence-validator final gate (citations in QA reports are not independently re-Read)
- No calibrator disjoint-set rule (rf-qa class can collide with executor class)
- Phase 1 exempted from QA (setup-only assumption may not always hold)
