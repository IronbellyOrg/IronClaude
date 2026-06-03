# Research: 11 - Gap Fill - Unverified Inputs Classification
**Investigation Type:** targeted Integration Mapper / Doc Analyst
**Scope:** gaps-and-questions.md; qa/research-gate-merged-report.md; research files 01-*.md through 10-*.md as available; targeted source files only as needed for unverified implementation inputs (hooks/settings/source-of-truth, /sc:forensic, retrospective/per-task rerun references, tenant/actor/audit identity claims)
**Status:** Complete
**Date:** 2026-06-02
---

## Assigned Gap

This gap-fill classifies the unresolved implementation-input and scope-limit findings assigned by the research gate:

| Gate ID | Assigned issue | Disposition in this file |
|---|---|---|
| RG-I1 | Unresolved `Gaps and Questions` remain across research files and may be promoted into facts. | Classified per gap group below; unresolved target-stack/external claims are barred from Current State and Implementation Plan unless Phase 4 verifies them. |
| RG-I4 | Source-of-truth / plugin mirror sync unresolved. | Resolved by gap-fill as a current-state risk: `src/superclaude/` is authoritative for this branch, but plugin mirrors are materially out of sync and must not be used as canonical implementation input. |
| RG-I5 | Hook portability, retrospective/per-task rerun, `/sc:forensic`, and related implementation inputs remain unverified. | Partially resolved by targeted source reads/search; unsupported items are excluded from implementation plan and carried as risks/open questions. |
| RG-M2 | Some inventories are sampled rather than exhaustive semantic review of every command/skill/agent. | Classified as synthesis-safe limitation if explicitly labeled scoped inventory; blocker only for claims of exhaustive semantic parity. |
| RG-M3 | Tenant/actor/audit absence claim is scoped, not repository-wide. | Resolved by guardrail: keep claim scoped to read dataclasses/models; do not make repo-wide or product-wide identity claims without a dedicated repo-wide identity audit. |

## Files Investigated

| File / source | Purpose in this gap-fill | Notes |
|---|---|---|
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/gaps-and-questions.md` | Gate issue list and assigned remediation plan. | Lines 21-35 enumerate RG-I1/RG-I4/RG-I5/RG-M2/RG-M3. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/qa/research-gate-merged-report.md` | QA rationale for fail gate and required gap-fill plan. | Lines 37-51 and 72-75 define the assigned classifications needed. |
| `research/01-pipeline-core-contracts.md` | Pipeline/core unresolved gaps and target-stack assumptions. | Complete; contains six gaps plus stale-doc notes. |
| `research/02-roadmap-tasklist-pipelines.md` | Roadmap/tasklist unresolved gaps and stale-doc notes. | Complete; contains six gaps. |
| `research/03-sprint-execution-runtime.md` | Sprint runtime gaps; retrospective/recoverability context. | Complete; contains sprint-specific gaps including source-unverified external capabilities. |
| `research/04-cli-portify-prd-cleanup-audit-eval.md` | Adjacent orchestration gaps; retry/forensic/eval context. | Complete; contains implementation-drift gaps. |
| `research/05-skills-agents-harness-reuse.md` | Source-of-truth, hook, `/sc:forensic`, inventory-sampling gaps. | Complete; central file for RG-I4/RG-I5/RG-M2. |
| `research/06-docs-and-existing-feasibility-artifacts.md` | Existing docs and stale feasibility claims. | Complete; central file for retrospective/per-task rerun/hook and stale-doc guardrails. |
| `research/07-target-data-model-and-ownership.md` | Ownership/multi-tenant identity and checkpoint-shape gaps. | Complete; central file for RG-M3 and tenant/actor/audit identity. |
| `research/08-gap-fill-feasibility-enrichment.md` | RG-C1 remediation artifact. | Post-parallel update: file is now populated and complete; it verifies enrichment files exist and identifies `06` inventory as stale/incomplete. |
| `research/09-gap-fill-checkpoint-contract.md` | RG-C2 remediation artifact. | Post-parallel update: file is now populated and complete; it verifies the checkpoint contradiction is real across prompt/template surfaces while parser support handles both legacy and numbered forms. |
| `research/10-gap-fill-harness-claim-patch.md` | RG-I2/RG-I3 remediation artifact. | Post-parallel update: file is now populated and complete; file 05 was patched to tag external claims and correct the MCP citation range. |
| `src/superclaude/core/CLAUDE.md` | Source-of-truth verification. | Lines 17-28 define `src/superclaude/` as source and `.claude/` as synced dev copies; lines 45-48 require edit `src` first then sync. |
| `src/superclaude/commands/README.md`, `src/superclaude/agents/README.md`, `src/superclaude/hooks/README.md` | Plugin mirror conflict verification. | These README files say to edit `plugins/superclaude/...` first, conflicting with core/project source-of-truth policy. |
| `src/superclaude/hooks/hooks.json` | Hook portability boundary. | Registers Claude Code hook events and shell commands under `~/.claude/hooks/...`; portable behavior requires reimplementation as middleware/guards. |
| `src/superclaude/cli/sprint/commands.py` | Sprint command surface and per-task rerun search target. | Commands found: `run`, `attach`, `status`, `logs`, `kill`, `verify-checkpoints`; no `rerun-tasks` command in current file. |
| `src/superclaude/cli/sprint/retrospective.py` and `src/superclaude/cli/sprint/executor.py` | Retrospective source verification. | Retrospective generator exists and is invoked at sprint end; failures are non-aborting. |
| `src/superclaude/cli/sprint/models.py`, `src/superclaude/cli/pipeline/models.py` | Tenant/actor/audit identity scoped absence check. | Scoped model reads show model/permission/budget/runtime fields but no tenant/actor identity fields in the read ranges. |
| Source grep for `forensic`, `rerun-tasks`, `tenant`, `actor`, audit identity terms | Targeted verification for RG-I5/RG-M3. | No `src/superclaude/commands/*forensic*` or `src/superclaude/skills/*forensic*` file found; no `rerun-tasks` under `src/superclaude/cli/sprint` search results. |

## Classification Matrix

### A. Assigned research-gate findings

| ID | Classification | Evidence basis | Synthesis action |
|---|---|---|---|
| RG-I1 | Resolved by gap-fill for classification; not content-resolved for every underlying open question. | This file classifies the underlying gaps from research files 01-07; files 08-10 were headers only when read. | Synthesis may proceed only if it carries the per-topic guardrails below; do not silently convert open questions into facts. |
| RG-I4 | Carry as Risk, with partial source resolution. | `src/superclaude/core/CLAUDE.md` says `src/superclaude/` is source of truth; package READMEs say plugin mirrors are edit-first; `diff -qr` found many src/plugin command, agent, and hook differences. | Current State may say branch/project instructions favor `src/superclaude/`; Implementation Plan must include a source-of-truth resolver/sync gate before ingesting instruction corpus. |
| RG-I5 | Mixed: Retrospective verified; hook portability is Carry as Risk; `/sc:forensic` and sprint `rerun-tasks` are Targeted Research Blockers if included as supported features. | Source reads verified retrospective generator and hook registrations; targeted find/search found no forensic command/skill and no sprint `rerun-tasks` command in current `sprint/commands.py`. | Include retrospective as code-verified. Exclude `/sc:forensic` and `rerun-tasks` from Current State/Implementation Plan unless a later source read finds them. Treat hooks as behavior-to-port, not portable artifacts. |
| RG-M2 | Synthesis-safe Open Question / scope limitation. | Research 05 inventories command/agent/skill counts and selected major packages, but does not semantically review every file; QA called this sampled inventory. | Use “scoped inventory” or “sampled semantic review.” Do not claim exhaustive command/skill/agent semantic parity. |
| RG-M3 | Resolved by scope guard; Carry as Risk for target design. | Research 07 claims absence only in scoped dataclass reads. Additional targeted grep found tenant references mostly in prompt text, not established runtime identity models. | Current State may say “not present in scoped models read.” Final recommendations must add tenant/actor/audit identity as a new target-design requirement, not an existing current capability. |

### B. Underlying gaps by source research file

| Source gap | Classification | Rationale | Synthesis guardrail |
|---|---|---|---|
| 01-G1 Mastra/Backlog.md/Beads APIs not externally verified | Synthesis-safe Open Question pending Phase 4 web research | Local source cannot verify external APIs. | Keep target-stack API/version/license claims out of Current State; mark options as assumptions until external validation. |
| 01-G2 Global CLI “no MCP integration” partially verified | Carry as Risk | Pipeline paths are subprocess-based, but every CLI command was not audited. | Say “investigated pipeline paths use ClaudeProcess”; do not claim repo-wide no-MCP integration. |
| 01-G3 Roadmap compressed-gate target owner decision | Synthesis-safe Open Question | Code behavior prefers `.compressed.md`; comments conflict. | Preserve current code behavior in parity requirements unless owner decides otherwise. |
| 01-G4 Trailing gate result handling target-stack choice | Synthesis-safe Open Question | Current code is advisory/warning-only; target representation is a design decision. | Treat non-blocking Beads comments/issues as parity-preserving; blocking trailing failures are a behavior change. |
| 01-G5 Sprint main loop separate modeling | Carry as Risk | Sprint uses custom loop separate from generic pipeline executor. | Hybrid/adapter-first recommendation should keep sprint as later/harder migration surface. |
| 01-G6 Diagnostic chain naming overpromises | Resolved by guardrail | Source shows static Markdown assembly, not agentic adversarial diagnostics. | Do not market diagnostics as agentic unless a future implementation changes it. |
| 02-G1 Certification gate production wiring gap | Carry as Risk | `CERTIFY_GATE` is defined, but production `_build_steps` does not append it per research 02. | Preserve as roadmap parity risk; do not list certification as currently wired production step. |
| 02-G2 Roadmap wiring trailing-vs-blocking mismatch | Carry as Risk | `wiring-verification` declares trailing, but default `grace_period=0` forces blocking. | State effective current behavior separately from intended behavior. |
| 02-G3 Tasklist generation lacks Python CLI implementation | Resolved by guardrail | CLI validates only; skill protocol defines generation. | Current State must separate “CLI validate” from “skill/protocol generation.” |
| 02-G4 Deviation classifier not implemented | Synthesis-safe Open Question | Current code renders `UNCLASSIFIED`; target may preserve or improve. | Treat classification implementation as future enhancement, not current behavior. |
| 02-G5 Skill-vs-CLI parity decision | Targeted Research Blocker for broad port scope | Product must choose CLI parity, skill parity, or merged future state. | Options section may compare scopes; implementation plan must pick one before estimating. |
| 02-G6 Backlog.md/Beads schema unknown locally | Synthesis-safe Open Question pending Phase 4 | External schemas cannot be locally verified. | Keep field mappings as hypotheses. |
| 03 generated-doc Path A same-output-file claim | Resolved by source contradiction | Current source uses per-task output/error files. | Do not carry stale generated-doc claim. |
| 03 Mastra subprocess supervision APIs | Synthesis-safe Open Question pending Phase 4 | External API not verified. | Keep Mastra long-running supervision as validation requirement. |
| 03 Backlog.md custom-field suitability | Synthesis-safe Open Question pending Phase 4 | External API/schema not verified. | Do not promise native storage of sprint telemetry/checkpoints. |
| 03 Beads checkpoint/evidence artifact support | Synthesis-safe Open Question pending Phase 4 | External schema not verified. | Treat Beads as likely graph fit, not proven evidence-artifact fit. |
| 03 `setup_isolation(config)` unused / weak isolation | Carry as Risk | Current Path B sets only `CLAUDE_WORK_DIR`; Path A no per-task isolation env per research 03. | Do not claim active 4-layer isolation; target can implement stronger isolation as behavior change. |
| 03 `status` and `logs` stubs | Carry as Risk | Current commands call stub functions per research 03. | Do not list live status/log tails as implemented current capability. |
| 03 tmux forwarding omissions | Carry as Risk | Some flags not forwarded in tmux helper per research 03. | Keep as sprint migration/runtime parity risk. |
| 03 Path A summary asymmetry | Carry as Risk | Path A does not submit `SummaryWorker` summaries before continue. | Preserve as sprint parity risk; do not overstate retrospective completeness for Path A. |
| 04 cli_portify resume/review drift | Carry as Risk | `resume.py`/`review.py` use legacy names while registry uses current names. | Use graph-first single source of truth in recommendations; do not port drifted matrices. |
| 04 cleanup-audit pass/batch flags and parallel doc drift | Carry as Risk | Source read shows sequential six-step execution and no visible pass filtering. | Describe cleanup-audit as source-verified sequential unless rebuilt. |
| 04 eval retry comment drift | Resolved by source contradiction | Retry-once policy exists when wired, despite stale comments. | If included, phrase as “policy exists when wired,” not default blanket retry. |
| 04 no current Mastra/Backlog/Beads integration in source | Synthesis-safe Open Question | Local repo has no direct implementation. | Final report must frame Stack D as feasibility/replatform design, not existing integration. |
| 05 source-of-truth conflict and plugin mirror sync | Carry as Risk / Targeted Research Blocker for corpus ingestion | Core says `src` SoT; READMEs say plugins; diff shows mirrors differ. | Implementation must choose resolver and verify sync before ingesting commands/agents/hooks. |
| 05 Mastra runtime APIs | Synthesis-safe Open Question pending Phase 4 | External docs needed. | Keep implementation API details out of Current State. |
| 05 Backlog.md/Beads schema details | Synthesis-safe Open Question pending Phase 4 | External docs needed. | Keep schema mappings hypothetical. |
| 05 `.claude/templates` references | Carry as Risk | Agent refs point to dev-copy templates; canonical templates exist under `src`. | Add template resolver requirement; do not scrape `.claude/` as source corpus. |
| 05 `/sc:forensic` dependency | Targeted Research Blocker if retained | Targeted file search found no forensic command/skill in `src/superclaude`. | Exclude `/sc:forensic` from implementation features unless located/created by a separate task. |
| 06 Stack D external facts | Synthesis-safe Open Question pending Phase 4 | Local doc only; external verification required. | External facts must be tagged `[UNVERIFIED external]` until web-verified. |
| 06 `superclaude pipeline` root command | Resolved by source contradiction | Current `main.py` does not register a root `pipeline` command per research 06. | Say `pipeline/` package API, not CLI command. |
| 06 hooks portable runtime events not verified | Carry as Risk | `hooks.json` verifies Claude Code hook registrations, not portable runtime. | Treat hook behavior as reimplementation requirement. |
| 06 retrospective models not verified | Resolved by this gap-fill | `ReleaseRetrospective` and `RetrospectiveGenerator` exist; executor invokes generator at sprint end. | Current State may include release retrospective, with non-aborting behavior and Path A summary caveat. |
| 06 per-task rerun/recoverability details | Targeted Research Blocker if included | Current `sprint/commands.py` has no `rerun-tasks`; grep found no sprint rerun command. | Do not claim per-task rerun CLI support; current recovery is checkpoint/result-file based unless separately verified. |
| 06 CLI Portify doc conflicts | Carry as Risk | Multiple stale docs conflict with current runner. | Use current source for CLI Portify behavior. |
| 06 dry-run semantics conflict | Targeted Research Blocker for exact dry-run guarantees | Source has early command return plus executor dry-run phase constants. | Avoid exact dry-run output guarantees without behavioral test. |
| 06 `/sc:task-unified` stale prompt name | Resolved by source contradiction | Current sprint prompt uses `/sc:task` per research 06/03. | Use current `/sc:task` naming only. |
| 06 RigorFlow external paths/integration claims | Out of Scope for current repo synthesis | `.gfdoc`/external RF infra not verified in this repo. | Treat as historical/external context only. |
| 07 target-stack ownership assumptions | Synthesis-safe Open Question pending Phase 4/product decision | Ownership split is an architecture hypothesis. | Keep in target-state/options, not current-state facts. |
| 07 multi-tenant auth/RBAC/cost governance | Targeted Research Blocker for implementation recommendation | Current scoped models lack tenant/actor fields; external Mastra governance not verified. | Do not recommend multi-tenant implementation without Phase 4 + identity model design. |
| 07 Backlog vs Beads status ownership | Targeted Research Blocker for implementation roadmap | Dual task/status owners can create drift. | Implementation plan must pick canonical status/body/graph owners. |
| 07 checkpoint documentation conflict | Carry as Risk / covered by RG-C2 | Main SKILL, template, and sprint prompt/checkpoint parser have conflicting checkpoint shapes. | Do not normalize; carry as checkpoint contract risk until dedicated RG-C2 remediation completes. |
| 07 artifact storage policy unresolved | Synthesis-safe Open Question | Current file artifacts remain source of truth; target retention policy undecided. | Recommend artifact ownership decision before migration. |
| 07 tenant/actor/audit absence | Resolved by scope guard | Absence verified only in scoped model reads and targeted terms search. | Phrase narrowly; require dedicated identity audit for repo-wide claim. |

## Evidence Table

| Claim | Verification status | Evidence | Report-safe phrasing |
|---|---|---|---|
| `src/superclaude/` is the current branch/project source-of-truth for distributable components. | [CODE-VERIFIED] | `src/superclaude/core/CLAUDE.md` states `src/superclaude/` is source of truth and `.claude/` is synced dev copy; component sync says edit `src` first then `make sync-dev`. | “For this branch, use `src/superclaude/` as canonical input unless owner explicitly changes source-of-truth policy.” |
| Plugin mirrors are fully in sync with `src/superclaude/`. | [CODE-CONTRADICTED] | `diff -qr src/superclaude/{commands,agents,hooks} plugins/superclaude/{commands,agents,hooks}` reported many `Only in src` and `Files ... differ` entries. | “Plugin mirrors exist but are not byte-identical; do not ingest them as canonical without a sync/audit step.” |
| Hook behavior is reusable. | [CODE-VERIFIED behavior exists; UNVERIFIED portability] | `src/superclaude/hooks/hooks.json` registers Claude Code events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SubagentStart`, `SubagentStop`) and shell commands under `~/.claude/hooks/...`. | “Hook contracts are reusable as behavior/policy; hook implementation is Claude Code-specific and must be rebuilt as target middleware/guards.” |
| Release retrospective exists in current sprint source. | [CODE-VERIFIED] | `src/superclaude/cli/sprint/retrospective.py` defines `ReleaseRetrospective` and `RetrospectiveGenerator`; `src/superclaude/cli/sprint/executor.py` invokes `RetrospectiveGenerator(config).generate(...)` during sprint wrap-up. | “Sprint has a release retrospective generator that runs at sprint end and is designed not to abort wrap-up on failures.” |
| Per-task `rerun-tasks` sprint CLI exists. | [CODE-CONTRADICTED by current searched source] | `src/superclaude/cli/sprint/commands.py` defines `run`, `attach`, `status`, `logs`, `kill`, and `verify-checkpoints`; grep for `rerun-tasks` under `src/superclaude/cli/sprint` returned no command. | Do not claim this current CLI verb exists. If needed, make it a proposed/future recovery feature or run a broader historical/branch search. |
| `/sc:forensic` exists as a command/skill. | [CODE-CONTRADICTED by current searched source] | `find src/superclaude -path '*/commands/*' -o -path '*/skills/*' | grep -i forensic` returned no forensic command/skill file; grep hits were generic “forensic” prose in eval isolation comments. | Exclude `/sc:forensic` from supported current surfaces unless a separate task adds or locates it. |
| Tenant/actor/audit identity is absent repository-wide. | [UNVERIFIED repository-wide; scoped absence only] | Scoped reads of `PipelineConfig` and `SprintConfig` show model/permission/budget/runtime fields but no tenant/actor fields; targeted grep found prompt prose and generic `actor` wording, not a verified governance model. | “The scoped current models read do not carry tenant/actor/audit identity fields; a repo-wide identity audit is still required before making broader claims.” |
| Inventories in research 05 are exhaustive semantic review of every command, skill, agent, hook, and MCP asset. | [UNVERIFIED / overclaim risk] | Research 05 provides counts and selected high-value inventories, but QA explicitly flagged inventory sampling. | “Scoped inventory with sampled semantic review of major assets.” |
| Files 08-10 remediate their assigned gate findings. | [CODE-VERIFIED after post-parallel re-read] | Post-parallel reads showed `08-gap-fill-feasibility-enrichment.md`, `09-gap-fill-checkpoint-contract.md`, and `10-gap-fill-harness-claim-patch.md` are populated and Status Complete. | Files 08-10 may be cited as remediation artifacts, subject to fix-cycle QA verification. |

## Synthesis Guardrails

1. **Never promote target-stack API assumptions into current-state facts.** Mastra, Backlog.md, and Beads capability/version/license/schema statements remain `[UNVERIFIED external]` until Phase 4 web/source research verifies them.
2. **Use `src/superclaude/` as current canonical corpus, not `.claude/` or unsynced plugin mirrors.** The final implementation plan must include a source-of-truth resolver and mirror-sync verification before any corpus ingestion.
3. **State hook portability as behavior-porting, not file portability.** Hook shell scripts and `hooks.json` are Claude Code-specific; the portable unit is the policy: prompt context enrichment, pre-edit freshness guard, post-read tracking, subagent lifecycle hooks, and workspace write guardrails.
4. **Exclude unsupported current features.** Do not include `/sc:forensic` or sprint `rerun-tasks` as current implementation inputs; only include them as proposed future features or targeted research blockers.
5. **Keep retrospective support narrowly phrased.** Sprint release retrospective exists and runs at sprint end, but Path A summary asymmetry remains a risk; do not claim all per-task execution has equal summary fidelity.
6. **Preserve sampled-inventory labeling.** Report command/skill/agent inventories as scoped counts and sampled semantic review, not exhaustive parity audit.
7. **Scope tenant/actor/audit identity claims.** Current scoped dataclass reads do not show identity fields; broader absence and target governance require a dedicated identity model audit.
8. **Do not normalize stale docs.** Carry known contradictions (certify wiring, compressed sidecar gate target comments, checkpoint shape conflict, tasklist generation-vs-validation, CLI Portify stale step names) into risks/options.
9. **Separate current execution semantics from target improvements.** Beads dependency scheduling, Mastra native workflow supervision, Backlog status ownership, tenant governance, and stronger isolation are potential design changes, not current parity.
10. **Use files 08-10 as remediation evidence only after fix-cycle QA re-verifies them.** They are now populated and complete, but the research-gate decision still depends on independent fix-cycle QA.

## Remaining Gaps and Questions

| Remaining gap | Classification | Owner / next action before implementation |
|---|---|---|
| External Stack D facts: Mastra APIs, workflow semantics, MCP support, RBAC/governance, Backlog.md schema, Beads schema/storage/server modes. | Targeted Research Blocker for implementation-level recommendation; synthesis-safe if labeled external assumptions. | Phase 4 web/source research must verify official/current docs. |
| Source-of-truth conflict between `src/superclaude/` branch policy and plugin README edit-first instructions. | Carry as Risk; Targeted Research Blocker for corpus-ingestion implementation. | Owner decision plus sync verifier. Use `src/superclaude/` meanwhile. |
| Plugin mirror content drift. | Carry as Risk. | Run a dedicated mirror-sync audit/remediation before any plugin-mirror based port. |
| Hook portability. | Carry as Risk. | Design target middleware equivalents for Claude Code hook policies; do not copy shell scripts as portable implementation. |
| `/sc:forensic` dependency in TFEP. | Targeted Research Blocker if retained. | Either add/locate a forensic command/skill or remove/replace dependency in implementation scope. |
| Sprint per-task rerun/recoverability claims. | Targeted Research Blocker if retained. | Do not claim `rerun-tasks`; verify historical branch/PR or implement new recovery command if product needs it. |
| Retrospective completeness across Path A/Path B. | Carry as Risk. | Include Path A summary asymmetry in sprint migration risk. |
| Checkpoint shape conflict. | Carry as Risk; also RG-C2 dependency. | Dedicated checkpoint contract remediation must decide canonical sprint-compatible shape. |
| Tenant/actor/audit identity model. | Targeted Research Blocker for multi-tenant implementation; scoped current-state claim resolved. | Perform repo-wide identity audit and target governance design. |
| Sampled vs exhaustive command/skill/agent inventory. | Synthesis-safe Open Question. | Use scoped wording; run exhaustive semantic inventory only if parity matrix requires every asset. |
| Files 08-10 were initially read before parallel completion. | Resolved by post-parallel update; still subject to QA. | Fix-cycle QA should re-read files 08-10 and decide whether RG-C1/RG-C2/RG-I2/RG-I3 are remediated. |

## Summary

This gap-fill resolves the research-gate classification problem for RG-I1/RG-I4/RG-I5/RG-M2/RG-M3 by assigning every investigated unresolved input to one of the requested buckets and by defining synthesis guardrails that prevent assumption promotion.

Key outcomes:

1. **RG-I1 is classification-resolved.** Underlying gaps remain, but each is now labeled as resolved by guardrail, synthesis-safe open question, targeted-research blocker, out-of-scope, or carry-as-risk.
2. **RG-I4 remains a real migration risk.** Current project policy and core instructions make `src/superclaude/` canonical, while plugin READMEs claim plugin edit-first behavior and the mirrors are materially out of sync. Synthesis must use `src/superclaude/` and require a resolver/sync gate before implementation.
3. **RG-I5 is partially source-resolved.** Retrospective support is verified in source; hook behavior exists but is not portable as-is; `/sc:forensic` and sprint `rerun-tasks` are not supported by current source search and must be excluded unless separately implemented or found.
4. **RG-M2 is safe with scoped wording.** Existing inventories may support high-level feasibility and reuse mapping, but not exhaustive semantic parity across every command/skill/agent.
5. **RG-M3 is resolved only as a scoped claim.** The current scoped models read do not show tenant/actor/audit identity fields, but repo-wide absence is not proven. Multi-tenant governance is a new target design requirement.

Synthesis may proceed if it applies the guardrails above and keeps unresolved target-stack, source-of-truth, hook-portability, recovery, checkpoint, and identity issues in risks/options rather than Current State facts or implementation commitments.
