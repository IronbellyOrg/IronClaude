# Gaps and Questions

**Task:** TASK-RESEARCH-20260602-211124  
**Date:** 2026-06-02  
**Source:** Merged research-gate reports  
**Status:** Research gate passed after fix cycle 1; gaps are classified for synthesis/web-research guardrails

---

## Critical Gaps Blocking Phase 4

| ID | Gap / Question | Impact | Suggested Resolution | Status |
|---|---|---|---|---|
| RG-C1 | Existing feasibility enrichment files conflict: research notes expect `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md` and `enrichment/research-deep.md`, but `06-docs-and-existing-feasibility-artifacts.md` says only `seed-brief.md` was found. | Blocks final report Sections 1, 2, 4, 9, 10 because prior feasibility context may be omitted or stale. | Run `08-gap-fill-feasibility-enrichment.md` to verify files, analyze if present, or document repo-state drift if absent. | Open |
| RG-C2 | Checkpoint contract contradiction: `sc-tasklist-protocol` numbered checkpoint tasks vs `sprint/process.py` prompt logic scanning sibling `### Checkpoint:` sections. | Blocks reliable Backlog/Beads/Mastra adapter recommendations for sprint-compatible tasklists. | Run `09-gap-fill-checkpoint-contract.md` to define canonical sprint-compatible checkpoint shape and mitigation. | Open |

## Important Gaps

| ID | Gap / Question | Impact | Suggested Resolution | Status |
|---|---|---|---|---|
| RG-I1 | Unresolved `Gaps and Questions` remain in all research files. | Synthesis could promote unresolved assumptions into facts. | Classify every gap as resolved, synthesis-safe open question, or targeted-research blocker. | Open |
| RG-I2 | External Mastra/Backlog.md/Beads claims appear in codebase research without full verification tags. | Current-state and options sections could overstate target-stack capabilities. | Tag as `[UNVERIFIED external]` pending Phase 4 or move to web research. | Open |
| RG-I3 | Invalid citation range `src/superclaude/core/MCP.md:269-305`; file ends at line 304. | Evidence trail would contain inaccurate citation. | Patch `05-skills-agents-harness-reuse.md` to use `269-304` or narrower verified range. | Open |
| RG-I4 | Source-of-truth / plugin mirror sync unresolved. | Port could ingest wrong instruction corpus. | Keep as risk/open question or verify sync behavior before implementation recommendation. | Open |
| RG-I5 | Hook portability, retrospective/per-task rerun, `/sc:forensic`, and related implementation inputs remain unverified. | Implementation plan could include unsupported assumptions. | Verify from source or explicitly exclude from Current State, Options, and Implementation Plan. | Open |
| RG-I6 | Roadmap compressed-sidecar behavior, `CERTIFY_GATE`, `wiring-verification` gate mode, and tasklist generation-vs-validation gaps must be preserved. | Port parity risks and stale-doc risks. | Carry into gap analysis and options; do not normalize stale docs. | Open |
| RG-I7 | Sprint Path A/B, isolation, stubbed status/logs, summary asymmetry, and process supervision complexity remain migration risks. | Sprint port may be much harder than roadmap/tasklist port. | Carry as sprint migration risk and hybrid-adapter-first rationale. | Open |

## Minor Gaps / Process Limitations

| ID | Gap / Question | Impact | Suggested Resolution | Status |
|---|---|---|---|---|
| RG-M1 | Incremental-writing compliance for first partition could not be independently verified. | Process quality concern, not content blocker if findings are usable. | Note limitation; require future phases to write incrementally. | Open |
| RG-M2 | Some inventories are sampled rather than exhaustive semantic review of every command/skill/agent. | Overclaim risk if described as exhaustive. | Label as scoped inventory. | Open |
| RG-M3 | Tenant/actor/audit absence claim is scoped, not repository-wide. | Multi-tenant governance claims may be overbroad. | Preserve scoped limitation unless repo-wide search is performed. | Open |

## Fix-Cycle Plan

1. `research/08-gap-fill-feasibility-enrichment.md` — resolve RG-C1.
2. `research/09-gap-fill-checkpoint-contract.md` — resolve RG-C2.
3. Patch `research/05-skills-agents-harness-reuse.md` and optionally create `research/10-gap-fill-harness-claim-patch.md` — resolve RG-I2/RG-I3.
4. `research/11-gap-fill-unverified-inputs-classification.md` — classify RG-I1/RG-I4/RG-I5/RG-M2/RG-M3.

## Gate Status

Research gate is **PASS after fix cycle 1** per `qa/qa-research-fix-cycle-1.md`. Remaining gaps are classified guardrails for Phase 4 web research, synthesis, risks, and open questions; they are no longer blocking Phase 4.
