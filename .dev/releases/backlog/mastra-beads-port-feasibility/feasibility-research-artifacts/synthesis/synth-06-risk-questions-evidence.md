# Synthesis 06: Open Questions, Risk Register, Evidence Trail (Report Sections 9-10)

**Task:** TASK-RESEARCH-20260602-211124
**Date:** 2026-06-02
**Status:** Complete
**Scope:** Report Section 9 (Open Questions), Risk Register support block, and Report Section 10 (Evidence Trail).
**Research question:** Can SuperClaude's CLI orchestration pipeline (sprint / roadmap / pipeline / tasklist) be ported/recreated onto a Mastra + Backlog.md + Beads (Stack D) stack as a multi-tenant company orchestration layer?
**Sourcing rule:** Every row cites a research file under `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/`, a QA report under `qa/`, the gaps log, or the feasibility seed at `.dev/releases/backlog/mastra-beads-port-feasibility/`. Genuinely unresolved questions are preserved as open, not answered.

---

## 9. Open Questions

Open questions are grouped into (9.A) strategic/architectural decisions the project owner must make and (9.B) verification/parity gaps that survived the research gate. None of these are answered here; each carries an honest impact and a suggested resolution path. Questions whose evidence is genuinely unresolved are flagged as such in the Suggested Resolution column.

### 9.A Strategic / Architectural Open Questions (owner decisions)

| # | Question | Impact | Suggested Resolution |
|---|---|---|---|
| Q1 | Primary work-of-record: Backlog.md vs Beads vs Mastra storage? Backlog.md (markdown task tree) and Beads (Dolt issue/dependency graph) functionally overlap; one must be primary work-of-record, the other memory/graph. | Core architecture decision; wrong split causes status drift between two task owners (research file `07` flags dual task/status owners as a drift risk; `web-02 §13`/`web-04 §14-15` confirm neither tool owns cross-system authority). | Decide canonical owners per data class: human-readable task/spec/decision body (Backlog.md), dependency DAG + ready-queue + claim/memory (Beads), durable workflow snapshots/state (Mastra storage). Pilot a single workflow (e.g., Backlog↔Beads import/export) before broad integration, per Backlog.md maintainer guidance (`web-02 §13`). Unresolved until owner picks canonical status/body/graph owners (`research/11:100`). |
| Q2 | Multi-tenancy model: what tenant/actor/audit identity model does the company orchestration layer require? | Strategic driver of the whole replatforming; current scoped SuperClaude models carry no tenant/actor identity fields (`research/07`, `research/11:115`), and MCP/Mastra/Backlog/Beads do not supply a tenant-aware governance plane (`web-04 §13-15`). | Run a repo-wide identity audit (current claim is scoped to read dataclasses only), then design a tenant/actor/audit identity model separating trigger/execution/authorization/tenant/attribution identities (`web-04 §9`). Treat as new target-design requirement, not an existing capability. Genuinely open pending identity-model design. |
| Q3 | Pilot scope: what is the smallest defensible first slice (which surface, which tenant count, local vs hosted)? | Determines effort band and whether EE licensing is triggered on day one; external research recommends separate local/OSS vs team/EE tracks (`web-01 §6`, rec 3). | Owner decision. Candidate: single-tenant local roadmap/tasklist port first (lower runtime-seam complexity per `research/11:64` sprint-is-harder finding), deferring sprint and multi-tenant hosting. Unresolved pending owner scoping. |
| Q4 | Parity bar for sprint and roadmap: like-for-like behavior, or accept behavior changes? | Sets the migration acceptance criteria; several current behaviors are advisory/stubbed (status/logs stubs, trailing-gate grace=0 forcing blocking, certify gate not wired in production) and "parity" may mean preserving or fixing them (`research/02`, `research/03`, `research/11:66-67`). | Owner must declare, per surface, whether the target preserves current effective behavior or adopts the documented-intended behavior. Unresolved design decision; carried as risk R7 below. |
| Q5 | Subprocess / sandbox mapping: does Mastra Workspace `WorkspaceSandbox.executeCommand` safely replace the `ClaudeProcess` subprocess seam with parity on hooks/permissions/freshness? | The runtime seam is the single coupling point a port must replace (`seed-brief`, `research/08:82`); external research explicitly states Workspace does NOT prove Claude Code hook/permission parity (`web-01 §3`, limitation 3). | Run a safety spike: validate `executeCommand` allowlists, env isolation, secret redaction, timeout, retention, approval against Claude Code hook/permission/freshness behavior before assuming parity. Genuinely unverified; hands-on validation required (`web-01` rec 2). |
| Q6 | Mastra Enterprise licensing: does multi-user/hosted RBAC/SSO/audit force the Mastra EE license, and at what cost/lock-in? | License-cost and lock-in driver; production RBAC/FGA/SSO/Studio-auth/Agent-Builder/audit/on-prem are Enterprise-linked (`web-01 §6, §10`; dual license Apache-2.0 core + EE for `ee/`). | Confirm EE pricing/terms with vendor for the intended deployment model; scope which features actually require EE vs OSS. Pricing/terms not fully resolved in research (vendor pricing page cited but exact figures not captured). Open pending vendor confirmation. |

### 9.B Verification / Parity Open Questions (from research gate + gap-fill)

| # | Question | Impact | Suggested Resolution |
|---|---|---|---|
| Q7 | Source-of-truth conflict: `src/superclaude/` (core/project policy) vs plugin-mirror READMEs ("edit plugins first"); mirrors are materially out of sync. | A port could ingest the wrong instruction corpus (skills/agents/hooks/commands) (`gaps RG-I4`, `research/11:51,84,110`). | Owner picks a canonical resolver; implementation must add a sync verifier/gate before ingesting any corpus. Use `src/superclaude/` meanwhile. Open pending resolver decision + sync audit. |
| Q8 | Checkpoint contract: should `executor.py` per-task branch call `_verify_checkpoints()`, and should the freeform `process.py` prompt and `phase-template.md` be aligned to the numbered-task checkpoint contract? | Sprint-compatible adapter correctness; canonical contract is numbered checkpoint tasks, but prompt/template/docs still reference legacy `### Checkpoint:` sections, and the per-task branch skips verification (`research/09:107,158-163`, `RG-C2`). | Adopt the canonical contract in `research/09:127-154`; emit numbered checkpoint tasks with `Checkpoint Report Path:` lines. The executor-branch wiring and prompt/template sync are open remediation decisions (`research/09:158-163`). |
| Q9 | `/sc:forensic` and sprint `rerun-tasks`: are these supported current surfaces, or must they be excluded/built? | TFEP/implementation scope could include unsupported features (`gaps RG-I5`, `research/11:88,93,113-114`). | Targeted source search found neither in current `src/superclaude` (no forensic command/skill; `sprint/commands.py` has no `rerun-tasks`). Exclude from current-state and implementation features unless a separate task locates or builds them. Open if retained. |
| Q10 | Backlog.md / Beads / Mastra schemas and API semantics for SuperClaude orchestration metadata (checkpoints, telemetry, retrospective, gates). | Field/state mappings are hypotheses; Backlog.md MCP schemas reject unknown properties (`additionalProperties:false`, `web-02 §4`), Beads is Dolt-first with envelope-mode JSON migration (`web-03 §4,7`). | Validate against current docs/APIs and prototype mappings; keep field mappings as hypotheses until validated (`research/11:60,71,86`). Open pending integration prototype. |
| Q11 | Skill-vs-CLI parity scope: does the port target CLI parity, skill/protocol parity, or a merged future state? | Determines port scope and effort before estimation; tasklist generation lives in the skill protocol while the CLI only validates (`research/02`, `research/11:70`). | Owner must pick one parity scope before estimating (targeted-research blocker for broad port scope, `research/11:70`). Open. |
| Q12 | Roadmap production wiring: is the certification gate (`CERTIFY_GATE`) actually appended in production `_build_steps`, and is `wiring-verification` trailing or blocking given `grace_period=0`? | Roadmap parity risk; declared-vs-effective behavior diverges (`research/02`, `research/11:66-67`). | State effective current behavior separately from intended behavior in the parity matrix; verify wiring before claiming certification is a live production step. Open / carry as risk R7. |
| Q13 | Exhaustive command/skill/agent semantic parity: have all assets been semantically reviewed, or only sampled? | Overclaim risk if a parity matrix is described as exhaustive (`gaps RG-M2`, `research/11:53,116`). | Label inventories as scoped/sampled; run an exhaustive semantic inventory only if the parity matrix requires every asset. Open if exhaustive parity is in scope. |

---

## Risk Register (support block)

Severity = combined Impact × Likelihood judgment (High / Medium / Low). Likelihood reflects current evidence strength, not a forecast. "Owner / Decision Gate" names where the risk must be resolved before it is allowed to propagate into implementation. Every row is evidence-cited; no risk is asserted without a source.

| # | Risk | Source Evidence | Impact | Likelihood | Severity | Mitigation | Owner / Decision Gate |
|---|---|---|---|---|---|---|---|
| R1 | License risk: production multi-user RBAC/SSO/FGA/audit/on-prem are Mastra Enterprise-licensed (`ee/` directories), not Apache-2.0 core. | `web-01 §6, §10` (dual license, EE-gated Studio auth/RBAC/FGA/Agent-Builder); `seed-brief` Known Context (EE license for `ee/`). | High (cost + lock-in for the strategic multi-tenant driver) | High (RBAC/SSO/audit are explicitly EE-linked) | High | Separate local/OSS and team/EE architecture tracks (`web-01` rec 3); confirm EE pricing/terms (Q6); design so OSS-only features remain usable single-tenant. | Owner + vendor before any hosted multi-tenant build (Q6 gate). |
| R2 | Language/runtime migration: ~65K-LOC Python orchestration must be replatformed onto Mastra's TypeScript step/workflow model; the `ClaudeProcess` subprocess seam must be replaced. | `seed-brief` Problem Statement (~65K LOC Python; subprocess driver); `research/08:38-70` (CODE-VERIFIED subprocess seam + sprint/roadmap/tasklist surfaces); `web-01 §2-3` (Mastra TS workflows + Workspace). | High (large rewrite; gate/convergence logic is pure Python today) | Medium-High (feasible per `web-01`, but unproven for these specific control loops) | High | Strangler-fig phased roadmap; port portable Markdown/YAML harness first; rebuild gate/wave/checkpoint loops as Mastra control flow; prototype before committing (`web-01` rec 1, bottom line). | Architecture owner; runtime-seam spike gate (Q5). |
| R3 | Backlog.md / Beads functional overlap: both can act as task store; dual task/status owners cause drift. | `seed-brief` Known Context (overlap risk); `research/07` + `research/11:100` (dual task/status owner drift); `web-02 §13` (Beads↔Backlog integration not mature, maintainer says narrow scope first). | High (data integrity / single-source-of-truth) | Medium (avoidable with a clear ownership split) | High | Assign canonical owners per data class (Q1); start with one narrow Backlog↔Beads sync workflow; do not assume native integration. | Owner (Q1 decision gate). |
| R4 | Beads / Dolt version churn: v1.0.5 carries "do not upgrade" sync warnings; migration `0043` can silently break multi-machine `bd dolt` sync; v1.0.4 had a server-mode data-clobber regression. | `web-03 §2` (v1.0.5 pre-release/gated, issue #4259, #3870); `web-03 §15` (fast-moving with sharp edges); seed-brief Beads version note (now corrected by `web-03 §7`). | High (data loss / corruption in multi-writer sync) | Medium (only if upgrades are unpinned/ungated) | High | Pin and gate Beads versions; avoid gated/pre-release builds; require `bd doctor` + backup/restore + push/pull smoke tests in adoption gates (`web-03` rec 4). | Platform/ops owner; version-pin gate before any Beads adoption. |
| R5 | Concurrency / multi-writer: Beads embedded mode is single-writer ("database is locked"); multi-agent needs Dolt server/shared-server mode, and session attribution is actively changing. | `web-03 §8-9` (embedded single-writer; server mode for concurrent writers; issues #3400/#3583 on session attribution); `web-02 §12` (Backlog.md is file/lock-based, not a transactional multi-user backend). | High (parallel/multi-agent orchestration correctness) | Medium-High (default embedded mode is insufficient for the company use case) | High | Require Beads server/shared-server mode for any multi-agent writer scenario; enforce atomic `bd update --claim`; one-task-per-agent/session discipline; track session-attribution fixes. | Architecture owner; concurrency-model gate before multi-agent rollout. |
| R6 | Subprocess / hook safety parity: Mastra Workspace `executeCommand` does NOT replicate Claude Code hooks, freshness checks, staging restrictions, or permission prompts; SuperClaude safety rules (UV-only, git safety, `.claude/` SoT, fork-PR target) must be rebuilt. | `web-01 §3` + limitation 3, rec 5; `research/11:111,123` (hooks are Claude Code-specific; portable unit is the policy, not the shell scripts); `gaps RG-I5`. | High (safety regression: unsafe command execution, lost guardrails) | High (parity is explicitly not provided by Mastra defaults) | High | Safety spike before assuming CLI parity (Q5); reimplement hook policies as Mastra middleware/guards; preserve SuperClaude governance outside Mastra defaults (`web-01` rec 5). | Security/architecture owner; safety-spike gate (Q5). |
| R7 | Checkpoint contract drift + roadmap wiring drift: stale prompt/template/docs reference legacy `### Checkpoint:` sections; per-task executor branch skips `_verify_checkpoints()`; certify gate may not be wired in production; trailing gate grace=0 forces blocking. | `research/09:98-109,158-172` (checkpoint contradiction; per-task branch skips verification; stale docs); `research/02` + `research/11:66-67` (certify wiring + trailing/blocking mismatch). | Medium-High (silent loss of checkpoint/gate enforcement on port) | Medium (real in docs/prompt surfaces; runtime parser already handles both shapes) | Medium-High | Adopt canonical numbered-checkpoint contract (`research/09:127-154`); emit `Checkpoint Report Path:` lines; align stale prompt/template/docs; state effective-vs-intended behavior separately (Q8, Q12). | Implementation owner; checkpoint/parity decision gate (Q8/Q12). |
| R8 | Governance / tenancy / cost gaps: Mastra + Backlog.md + Beads provide no tenant isolation, no per-invocation audit, no cost attribution, no policy/approval/catalog control plane; MCP is a protocol, not governance. | `web-04 §1-15` (MCP not governance; token passthrough forbidden; tenant/realm mix-up pitfalls; Mastra/Backlog/Beads each not a governance plane); `research/07` + `research/11:99` (tenant/actor/audit identity is a new target requirement). | High (blocks safe company-wide multi-tenant deployment) | High (none of the three tools supplies this layer) | High | Add a dedicated governance/control-plane service (tenant registry, identity mapping, RBAC/ABAC, tool catalog, audit log, cost/budget metering) + MCP/AI gateway enforcing OAuth 2.1, audience validation, scoped tools (`web-04` rec 2-3). | Owner + security; governance-plane gate before multi-tenant deployment (Q2). |
| R9 | Reliance on fast-moving external tools: Mastra (`@mastra/core` 1.1.0+, Temporal integration experimental), Backlog.md (v1.45.2, MCP MVP + doc drift + open browser state-loss bug), Beads (1.x, frequent CLI/API changes) are all rapidly evolving. | `web-01 §1` (Temporal experimental), §9 (vendor maturity claims need validation); `web-02 §5,9,10,11` (MCP MVP, doc drift, issue #578, v1.45.2); `web-03 §15` (active 1.x, sharp edges). | Medium-High (breaking changes, doc drift, schema instability mid-build) | High (all three are pre-mature or fast-moving) | Medium-High | Pin versions; runtime-verify MCP instruction/schema surfaces (`web-02` rec 6); avoid experimental runners (Temporal); prefer stable contracts (`bd --json`, Backlog CLI/MCP); budget for churn; do not migrate without hands-on validation (`web-01` bottom line). | Platform owner; version-pin + validation gates per tool. |

**Cross-reference:** R1↔Q6, R2↔Q5/Q11, R3↔Q1, R6↔Q5, R7↔Q8/Q12, R8↔Q2, R9↔Q10. The seed brief's required risk-register coverage (license drift, Backlog/Beads overlap, loss of Claude-Code-native features, multi-tenant security) is satisfied by R1, R3, R6, and R8 respectively (`seed-brief` Success Criteria).

---

## 10. Evidence Trail

All paths are relative to the repository root `/config/workspace/IronClaude/`. The task directory prefix `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/` is abbreviated as `<TASK>/` below.

### 10.1 Codebase Research Files (Phase 1-3, files 01-07)

| File | Path | Topic / Scope |
|---|---|---|
| 01 | `<TASK>/research/01-pipeline-core-contracts.md` | Shared pipeline core contracts: `pipeline/` models, executor, gates, process (`ClaudeProcess` seam), trailing_gate, deliverables, diagnostic_chain — for Stack D port feasibility. |
| 02 | `<TASK>/research/02-roadmap-tasklist-pipelines.md` | Roadmap and tasklist CLI + skill protocols + commands; certification/wiring/convergence gates; generation-vs-validation split. |
| 03 | `<TASK>/research/03-sprint-execution-runtime.md` | Sprint execution runtime: Path A/B execution, tmux/session driver, stream-json monitor, isolation, status/log stubs, retrospective, checkpoints. |
| 04 | `<TASK>/research/04-cli-portify-prd-cleanup-audit-eval.md` | Adjacent orchestration surfaces: cli_portify, prd, cleanup_audit, eval, audit; retry/forensic/eval drift. |
| 05 | `<TASK>/research/05-skills-agents-harness-reuse.md` | Portable harness reuse: skills, agents, commands, core, templates, hooks, mcp; reuse/adapt/rewrite mapping (patched for external tags + MCP citation). |
| 06 | `<TASK>/research/06-docs-and-existing-feasibility-artifacts.md` | Existing docs + feasibility artifacts inventory and cross-validation (inventory line superseded by file 08). |
| 07 | `<TASK>/research/07-target-data-model-and-ownership.md` | Target data model and ownership: MDTM task/checkpoint shape, tenant/actor/audit identity absence (scoped), Backlog/Beads/Mastra ownership split. |

### 10.2 Web Research Files (Phase 4 external, dated 2026-06-02)

| File | Path | Topic |
|---|---|---|
| web-01 | `<TASK>/research/web-01-mastra-current-capabilities.md` | Mastra 1.0+ workflows, Workspace/subprocess, storage, observability/Studio, MCP, deployment, auth/RBAC/FGA, Enterprise licensing. Provenance: tavily + context7. |
| web-02 | `<TASK>/research/web-02-backlog-md-current-capabilities.md` | Backlog.md v1.45.2 CLI/MCP/schema, MCP MVP + `additionalProperties:false`, no-git mode, agent workflow, Beads integration immaturity, browser state-loss bug. Provenance: tavily. |
| web-03 | `<TASK>/research/web-03-beads-current-capabilities.md` | Beads (`gastownhall/beads`) CLI/JSON contract, Dolt-first storage, embedded vs server mode, multi-writer, gates, v1.0.5 sync warnings. Provenance: tavily. |
| web-04 | `<TASK>/research/web-04-mcp-multitenancy-governance.md` | MCP enterprise governance limits, tenancy/audit/cost gaps, OAuth 2.1, token-passthrough ban, control-plane patterns; Mastra/Backlog/Beads governance insufficiency. Provenance: tavily. |

### 10.3 Gap-Fill Research Files (fix cycle 1, files 08-11)

| File | Path | Topic / Remediated Gate Finding |
|---|---|---|
| 08 | `<TASK>/research/08-gap-fill-feasibility-enrichment.md` | RG-C1: reconciles existing feasibility enrichment files (`enrichment/codebase-context.md`, `research-deep.md`) that exist in repo; supersedes stale file-06 inventory. |
| 09 | `<TASK>/research/09-gap-fill-checkpoint-contract.md` | RG-C2: checkpoint-contract contradiction (numbered-task vs legacy `### Checkpoint:`); defines canonical sprint-compatible checkpoint shape + adapter implications. |
| 10 | `<TASK>/research/10-gap-fill-harness-claim-patch.md` | RG-I2/RG-I3: tags external Mastra/Backlog/Beads claims `[UNVERIFIED external]` in file 05; corrects invalid `MCP.md:269-305` → `269-304`. |
| 11 | `<TASK>/research/11-gap-fill-unverified-inputs-classification.md` | RG-I1/RG-I4/RG-I5/RG-M2/RG-M3: classifies every unresolved gap as resolved / synthesis-safe / carry-as-risk / targeted-blocker / out-of-scope; defines synthesis guardrails. |

### 10.4 Synthesis Files

| File | Path | Report Sections |
|---|---|---|
| synth-01 | `<TASK>/synthesis/synth-01-problem-current-state.md` | Sections 1-2: Problem Statement and Current State Analysis (code-verified facts only). |
| synth-02 | `<TASK>/synthesis/synth-02-target-gaps.md` | Sections 3-4: Target State and Gap Analysis. |
| synth-03 | `<TASK>/synthesis/synth-03-external-findings.md` | Section 5: External Research Findings (web-01..04 reconciled against `research-deep.md` seed). |
| synth-04 | `<TASK>/synthesis/synth-04-options-recommendation.md` | Sections 6-7: Options analysis (four options A-D with Effort/Risk/Reuse/Files/Pros/Cons tables + an Options Comparison table) and the conditional go/no-go/hybrid (D→A) recommendation with spike exit gates and rationale-against-comparison. |
| synth-05 | `<TASK>/synthesis/synth-05-implementation-roadmap.md` | Section 8: Phased implementation roadmap / strangler-fig sequencing. |
| synth-06 | `<TASK>/synthesis/synth-06-risk-questions-evidence.md` | Sections 9-10: Open Questions, Risk Register support block, Evidence Trail (this file). |

> Note: All six synthesis files (synth-01..06) were present in the synthesis directory at the time this file was written.

### 10.5 Gaps Log and QA Reports

| File | Path | Role |
|---|---|---|
| Gaps log | `<TASK>/gaps-and-questions.md` | Merged, classified gap/question register (RG-C1..RG-M3) feeding Sections 9-10 and the risk register. |
| QA — analyst 1 | `<TASK>/qa/analyst-completeness-report-1.md` | Completeness verdict for research files 01-04 (PASS; 8 important gaps carried). |
| QA — analyst 2 | `<TASK>/qa/analyst-completeness-report-2.md` | Completeness verdict for research files 05-07 (FAIL; enrichment contradiction + checkpoint/SoT/external gaps). |
| QA — gate 1 | `<TASK>/qa/qa-research-gate-report-1.md` | Research-gate verdict for files 01-04 (FAIL; unresolved gaps). |
| QA — gate 2 | `<TASK>/qa/qa-research-gate-report-2.md` | Research-gate verdict for files 05-07 (FAIL; checkpoint contradiction, untagged external claims, invalid MCP citation). |
| QA — merged | `<TASK>/qa/research-gate-merged-report.md` | Merged research-gate verdict (FAIL) + deduplicated findings + required gap-fill plan. |
| QA — fix cycle 1 | `<TASK>/qa/qa-research-fix-cycle-1.md` | Fix-cycle verdict (PASS, 15/15; \|F1\|=0); gate cleared for Phase 4 with guardrails. |

### 10.6 Feasibility Seed and Enrichment Inputs (pre-existing)

| File | Path | Role |
|---|---|---|
| Seed brief | `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` | Original problem statement, known context, constraints, success criteria, strategic open questions (source for Section 9.A). |
| Enrichment — codebase | `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md` | Prior codebase-context seed (architecture broadly code-verified; line/LOC refs approximate per file 08). |
| Enrichment — deep | `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/research-deep.md` | Prior external/Stack-D deep-research seed (superseded by fresh web-01..04 where they differ; per synth-03 ground rules). |

---

## Summary

This synthesis delivers Report Sections 9-10 plus the risk-register support block, in table-first, fully-cited form:

1. **Section 9 (Open Questions)** preserves all six strategic seed-brief questions (Q1 work-of-record, Q2 tenancy, Q3 pilot scope, Q4 parity bar, Q5 subprocess/sandbox mapping, Q6 Mastra EE licensing) plus seven verification/parity questions (Q7-Q13) carried from the research gate and gap-fill classification. No genuinely unresolved question is answered; each is flagged with impact and a resolution path.
2. **Risk Register** covers all nine required risk classes (R1 license, R2 language/runtime migration, R3 Backlog/Beads overlap, R4 Beads/Dolt v1.0.5 churn, R5 concurrency/multi-writer, R6 subprocess/hook safety parity, R7 checkpoint/wiring contract drift, R8 governance/tenancy/cost gaps, R9 fast-moving external tools), each with source evidence, impact, likelihood, severity, mitigation, and a decision gate, cross-referenced to the open questions.
3. **Section 10 (Evidence Trail)** indexes every codebase research file (01-07), web research file (web-01..04), gap-fill file (08-11), synthesis file (synth-01..06), the gaps log, all six QA reports, and the feasibility seed/enrichment inputs — each with path and topic.

**Honesty note:** Per the user's rule and the file-11 synthesis guardrails, unresolved target-stack, source-of-truth, hook-portability, recovery, checkpoint, identity, and licensing-cost matters remain open questions or risks rather than being resolved into facts. External Stack D claims trace to fresh web research (`provider=tavily`); codebase claims trace to `[CODE-VERIFIED]` source reads.
