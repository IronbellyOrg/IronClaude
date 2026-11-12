# Research Notes: Supervised Orchestration

**Date:** 2026-11-10
**Scenario:** A
**Depth Tier:** Heavyweight
**Status:** Complete

## EXISTING_FILES
- Primary normative source: `src/superclaude/core/WORKER-CONTRACT.md` (273 lines), worker/coordinator duties, lifecycle and human decisions. These are instructions, not proof of execution.
- Current ownership guidance: `src/superclaude/core/CLAUDE.md`, `src/superclaude/skills/ccsession-tag/README.md`, and project `CLAUDE.md`; changed after the research report.
- Implemented controls: `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `launch-level-guard.sh`, `launch-job-identity.sh`; registration `src/superclaude/hooks/hooks.json`, installer `src/superclaude/cli/install_hooks.py`. Tests under `tests/hooks/` and `tests/skills/test_worker_contract.py`.
- Research starting point (historical, not current truth): `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md` and sibling `research/`, `synthesis/`, correction record. Four independent discovery agents reviewed separate aspects; original agent returns retained in session transcripts.
- Orca development-source leads under `/home/coder/workspaces/IronOrca/src/main/runtime/`: inspect availability and provenance; this checkout is not proven to match installed runtime.
- Existing documentation: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`; source template `src/superclaude/templates/documents/technical_reference_template.md`. No matching reference task or existing technical-reference filename was found by Glob.

## PATTERNS_AND_CONVENTIONS
- [CODE-VERIFIED: normative] `src/superclaude/core/WORKER-CONTRACT.md:62,69`: worker fan-out is prohibited, and the supervised coordinator is a person-opened session.
- [CODE-VERIFIED: implementation] `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` applies a bounded lexical check; ownership text is not itself role enforcement. Revalidate predicates and fail-open cases against the source and tests.
- [CODE-CONTRADICTED: historical report] Report sections 2.2, 4 A01 and 7.6 present the old ownership wording as current; canonical guidance and hook text have since changed. Preserve the historical record, do not claim that the separate future-role question is resolved.

## FEATURE_ANALYSIS
Document existing supervised coordinator/worker roles, task dispatch and lifecycle rules, messaging and liveness, hook guards and identity, ordinary launch paths, distribution and evidence limits. Distinguish normative contracts, code-defined behavior, historical observations, current development source and live deployed state. The proposed subordinate mode is deferred, not an implemented system. The four discovery partitions identified cross-cutting integration boundaries and 20+ relevant source/test/doc files; Heavyweight applies.

## RECOMMENDED_OUTPUTS
- Final reference: `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`; confirm directory and whether an existing relevant reference exists before writing.
- `research/01-roles-authority.md` through `research/06-distribution-evidence.md`; `synthesis/synth-01-overview-architecture.md`, `synth-02-data-flow.md`, `synth-03-subsystems.md`, `synth-04-integration-config.md`, `synth-05-conventions-debt.md`. Map to template sections 1-5, 8-16; explain N/A for inapplicable sections, without claiming hypothetical features.
- Preserve all investigation, synthesis, quality and fidelity artifacts inside this task package; source evidence must be re-read at writing time.

## SUGGESTED_PHASES
Parallel source investigations, one agent per bounded assignment (paths below are under this task folder):
1. Architecture analyst: worker identity, roles, authority and human rulings; `src/superclaude/core/WORKER-CONTRACT.md` sections 1-3 and current `src/superclaude/core/CLAUDE.md`; output `research/01-roles-authority.md`.
2. Code tracer: coordinator lifecycle, monitoring, retry and messages; `src/superclaude/core/WORKER-CONTRACT.md` section 4; output `research/02-lifecycle.md`.
3. Integration mapper: hook recognition and enforcement ceilings; `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `launch-level-guard.sh`, `launch-job-identity.sh` and `tests/hooks/`; output `research/03-guards.md`.
4. Code tracer: ordinary launch and worker launch boundaries; `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, `src/superclaude/cli/issue_watch/launch.py`, relevant tests; output `research/04-launchers.md`.
5. Architecture analyst: Orca development source helper routing, mailbox and run-binding, only where accessible; `worker-start-authority.ts`, `dispatch-report-mailbox.ts`, `worker-run-binding.ts` in the development checkout identified by scope agent; output `research/05-orca-provenance.md`. Explicitly distinguish checkout source, historical installed trace and unverified deployed behavior.
6. Doc analyst: current distribution and documented policy, staleness and earlier decision; `src/superclaude/core/CLAUDE.md`, `src/superclaude/skills/ccsession-tag/README.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, the prior research report sections 6-9 and relevant tests; output `research/06-distribution-evidence.md`. Recheck sources and flag stale claims.

Then perform research completeness gate, gap-driven web research only if required, template-aligned synthesis (five files above), synthesis gate, assembly, lens-based QA, source fidelity gate, and presentation. Use the skill's per-agent checklist prompts, fixed review floors and two-cycle limits; do not authorize a live Orca run or implementation.

## TEMPLATE_NOTES
The source technical-reference template is post-implementation and has 16 sections; the existing contract and controls are in scope, while a proposed subordinate mode is not built and belongs in limitations. Heavyweight is appropriate for cross-cutting roles, hooks, launchers and integration. Mark non-applicable UI/state sections honestly and do not invent performance figures.

## AMBIGUITIES_FOR_USER
No unresolved user-intent question. [UNVERIFIED] Installed copy parity, running Orca build and effective settings, live hook ordering and runtime enforcement are outside the observed evidence; do not imply these are verified. [CODE-CONTRADICTED] The earlier research report's A01 current-wording diagnosis has been superseded by the local wording clarification; recheck precise current files and do not assert installation rollout.
