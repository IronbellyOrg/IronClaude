# Agent 3 — Agents Eval Proposals

## Proposal 1 (one-off): `rf_task_builder_template_handoff_contract`

- **Targets:** `rf-task-builder`, `rf-task-researcher`, `rf-task-executor`
- **Hypothesis:** Builder reads selected template first, waits for research, writes incrementally, emits `TASK_READY`.
- **Cadence:** one-off.
- **Inputs:** `BUILD_REQUEST` with `TEMPLATE:02`, `QA_GATE_REQUIREMENTS:PER_PHASE`, missing/seeded template scenario.
- **Assertions:** expected task file exists; has YAML frontmatter, self-contained checklist items, phase-output handoff paths, `TASK_READY`; exit 0.
- **Requires:** claude PTY, filesystem assertions, optional Task/SendMessage transcript capture.
- **Complexity:** medium.
- **Value:** Catches template-blocking and one-shot/truncated task regressions.
- **Evidence:** `.claude/agents/rf-task-builder.md:71`, `:123`, `:168`, `:222`; `.claude/agent-memory/rf-task-builder/template-notes.md:9`.

## Proposal 2 (one-off): `audit_wiring_delete_guard_contract`

- **Targets:** `audit-scanner`, `audit-analyzer`, `audit-validator`, `audit-consolidator`
- **Hypothesis:** Wiring files are escalated, not deleted; reports include required fields.
- **Cadence:** one-off.
- **Inputs:** fixture repo with provider dir, registry, Optional[Callable], and live import.
- **Assertions:** no DELETE for live-wired file; analyzer includes Wiring path; validator reports PASS/CRITICAL FAIL correctly; exit 0.
- **Requires:** grep/read, isolated HOME.
- **Complexity:** medium.
- **Value:** Prevents destructive audit false negatives.
- **Evidence:** `.claude/agents/audit-scanner.md:91`, `.claude/agents/audit-analyzer.md:78`, `.claude/agents/audit-validator.md:101`, `.claude/agents/audit-consolidator.md:64`.

## Proposal 3 (recurring): `agent_grounding_drift_meta_eval`

- **Targets:** `evidence-validator`, `confidence-calibrator`, `rf-qa`, `rf-qa-qualitative`
- **Hypothesis:** Agents independently verify citations and fail on mismatches.
- **Cadence:** recurring — scheduled nightly + on agent prompt changes.
- **Inputs:** known-good/known-bad citation fixture report and hypothesis card.
- **Assertions:** dropped-citation count > 0 for bad fixtures; calibrated confidence lower than self-report; suggested status `partial`; exit 0.
- **Requires:** claude PTY, Read/Grep, no network.
- **Complexity:** simple.
- **Value:** Catches behavioral drift toward trusting upstream claims.
- **Evidence:** `.claude/agents/evidence-validator.md:48`, `.claude/agents/confidence-calibrator.md:49`, `.claude/agents/rf-qa.md:84`, `.claude/agents/rf-qa-qualitative.md:94`.
