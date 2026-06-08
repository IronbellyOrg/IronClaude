# Research Notes: Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture (Technical Reference)

**Date:** 2026-06-03
**Scenario:** A — explicit request with named subject, two input-context sources, and a confirmed framing decision
**Depth Tier:** Heavyweight
**Status:** Complete
**Code HEAD at scope discovery:** `9e864860`

---

## CRITICAL FRAMING (read first — governs every downstream item)

The subject — *"Mastra + Backlog.md + Beads hybrid adapter-first orchestration architecture"* — is a **PROPOSED / NOT-YET-BUILT** architecture. The driving `FEASIBILITY-STUDY.md` verdict is **"Conditionally Recommended — Option D → A: fund a validation spike first; do NOT start a native rewrite."** None of Mastra, Backlog.md, or Beads is integrated into this codebase. The user explicitly selected the framing: **"Tech-Reference of the target design (adapt the skill)."**

Therefore this is an **adapted** tech reference. Two non-negotiable rules apply to EVERY synthesis and assembly item:

1. **Built-vs-Design demarcation is MANDATORY on every architectural claim.** Each claim carries exactly one tag:
   - **`[CODE-VERIFIED]`** — the existing SuperClaude Python orchestration layer that the port reuses/adapts. Must cite an actual source path (e.g. `src/superclaude/cli/pipeline/executor.py:NNN`) AND the research file that traced it. This is real, shipped code at HEAD `9e864860`.
   - **`[DESIGN — UNBUILT]`** — the target hybrid architecture: Mastra workflows, Backlog.md/Beads adoption, the adapter/seam-replacement layer, the multi-tenant control plane. Evidence traces to `FEASIBILITY-STUDY.md` / research files / web research — NOT to integrated code (because none exists).
   - **`[EXTERNAL-VERIFIED]`** — capability facts about Mastra/Backlog.md/Beads/MCP sourced from web research (web-01..04) with URLs. The component exists upstream; the *integration* does not.
2. **Codebase is source of truth for the BUILT side; the feasibility study is source of truth for the DESIGN side.** Never present a `[DESIGN]` claim as if built. Section 15 MUST carry an explicit "Built-vs-Design Status Ledger." The document must never read as if the hybrid system exists in this repo.

**This is NOT a feasibility study reformat.** The `FEASIBILITY-STUDY.md` answers "should we / can we." This tech reference answers "what is the architecture, how does each piece work, what is verified vs designed, and how would an engineer extend it." Different document type, same evidence base.

---

## ADAPTATION OF THE STANDARD TECH-REFERENCE PIPELINE

The standard skill runs Phase 2 (fresh parallel codebase investigation) and Phase 4 (fresh web research). **Both are already complete** and live in the input context. The adaptation:

| Phase | Standard behavior | Adapted behavior for this task |
|---|---|---|
| **Phase 2 — Deep Investigation** | Spawn 6–10 fresh code-tracer agents | **Ingest** the 11 pre-completed code-traced research files as the verified evidence base, **+ 4 targeted spot-check agents** that re-read the key existing-Python seam files at HEAD `9e864860` to confirm research claims still hold and flag any 1-day drift. NO full re-investigation. |
| **Phase 4 — Web Research** | Spawn fresh web agents for gaps | **Pre-completed** (web-01..04). One bookkeeping item records the external evidence base; spawn a fresh web agent ONLY if a synthesis gap demands it. |
| **Phase 5 — Synthesis** | Core work | **Core work** — 8 synthesis agents re-cast the evidence into the tech-reference template with built-vs-design tags. |
| **Phases 3, 5, 6 QA gates** | Mandatory | **Retained in full** (analyst + rf-qa research gate; analyst + rf-qa synthesis gate; rf-qa report-validation + rf-qa-qualitative). |

Rationale: re-running fresh investigation would duplicate ~480 KB of high-quality code-traced research and re-spend web-search budget on already-captured external facts. The spot-check agents preserve the skill's code-verification guarantee without the duplication. (Aligns with memory `feedback_prefer_simpler_proposals`.)

---

## EXISTING_FILES

### Input context — pre-completed research (the evidence base)

All under `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/`. Coverage confirmed via Explore agent scope-discovery sweep.

| File | Topic | Built/Design | Key symbols/contracts documented |
|---|---|---|---|
| `01-pipeline-core-contracts.md` (51 KB) | Shared pipeline seam | BUILT | `Step`,`StepResult`,`StepStatus`,`GateMode`,`GateCriteria`,`SemanticCheck`,`Deliverable`,`PipelineConfig`,`execute_pipeline()`,`StepRunner` protocol,`gate_passed()`,`ClaudeProcess`,`TrailingGateRunner`,`DeferredRemediationLog`,`run_diagnostic_chain()` in `cli/pipeline/*` |
| `02-roadmap-tasklist-pipelines.md` (47 KB) | Roadmap+tasklist workflows | BOTH | `roadmap/executor.py::_build_steps()`, 12-step DAG, `roadmap/gates.py` (`EXTRACT/GENERATE_A/B/DIFF/DEBATE/SCORE/MERGE/SPEC_FIDELITY/CERTIFY_GATE`...), `convergence.py::DeviationRegistry`, `tasklist/executor.py::tasklist_run_step()`, `TASKLIST_FIDELITY_GATE` |
| `03-sprint-execution-runtime.md` (41 KB) | Sprint runtime (hardest port) | BOTH | `sprint/executor.py::execute_sprint()`, Path A (per-task) vs Path B (freeform), `_run_task_subprocess()`, `_verify_checkpoints()`, `config.py::discover_phases()/parse_tasklist()`, `models.py::TurnLedger/CheckpointEntry/TaskEntry`, `monitor.py::OutputMonitor`, `checkpoints.py` |
| `04-cli-portify-prd-cleanup-audit-eval.md` (53 KB) | Adjacent orchestration patterns | BOTH | `cli_portify` STEP_REGISTRY/ConvergenceEngine, `prd` Stage A/B + `run_qa_fix_loop()`, `cleanup_audit` 6-gate loop, `eval` `RunOrchestrator`/`HomeIsolation`/forensic JSONL, `audit` `ToolOrchestrator` |
| `05-skills-agents-harness-reuse.md` (35 KB) | Reusable harness corpus | BOTH | 42 commands, 39 agents, 24 skills, core/*, templates/workflow/*, hooks.json, mcp/configs; reuse strategy table; all target mappings tagged `[UNVERIFIED external]` |
| `06-docs-and-existing-feasibility-artifacts.md` (39 KB) | Doc cross-validation | BOTH | Stale-doc findings; `superclaude pipeline` is a package not a root command; generated-doc drift |
| `07-target-data-model-and-ownership.md` (36 KB) | Target ownership model | BOTH | Model Groups A/B/C, ownership matrix (prose/graph/run owners), 4 adapter-contract sketches, sprint-parser compatibility contract |
| `08-gap-fill-feasibility-enrichment.md` (20 KB) | Enrichment cross-check | BOTH | Confirms `ClaudeProcess` seam, `pipeline/` package API, `stream-json`, `/sc:task` (not `/sc:task-unified`) |
| `09-gap-fill-checkpoint-contract.md` (20 KB) | Checkpoint contract | BUILT | Canonical numbered `### T<PP>.<TT> -- Checkpoint:` form; `Checkpoint Report Path:`; `checkpoints.py::CHECKPOINT_HEADING_PATTERN` accepts both shapes; Path A skips `_verify_checkpoints()` |
| `10-gap-fill-harness-claim-patch.md` (3 KB) | Metadata patch | meta | Tags external claims unverified; `MCP.md:269-304` citation fix |
| `11-gap-fill-unverified-inputs-classification.md` (28 KB) | Unverified-input classifier | BOTH | Source-of-truth conflict, hook portability boundary, no `/sc:forensic`, no `rerun-tasks` (NOTE: memory says `sprint rerun-tasks` shipped v4.3.0 — flag for spot-check), `retrospective.py` verified, tenant/actor identity absent |
| `web-01-mastra-current-capabilities.md` (13 KB) | Mastra | EXTERNAL | workflows `suspend()/resume()`, `WorkspaceSandbox.executeCommand()`, storage providers, Studio/observability, auth/RBAC **EE-gated** (`@mastra/core/auth/ee`), MCP client/server, Apache-2.0 core + EE license |
| `web-02-backlog-md-current-capabilities.md` (12 KB) | Backlog.md | EXTERNAL | `backlog task/doc/decision/board/browser` CLI, task schema, MCP MVP (`additionalProperties:false`), `--no-git`, v1.45.2 MIT, browser bug #578, Beads integration immature #588 |
| `web-03-beads-current-capabilities.md` (13 KB) | Beads | EXTERNAL | `bd ready/create/update --claim/dep add`, `--json` schema v1, typed deps + cycle rejection, gates (`gh:pr/gh:run/timer/bead/human`), **Dolt-first** (not SQLite/JSONL), embedded(single-writer) vs server(multi-writer), v1.0.5 "do not upgrade" |
| `web-04-mcp-multitenancy-governance.md` (14 KB) | MCP + governance | EXTERNAL | MCP not a governance layer, OAuth 2.1, no token passthrough, multi-tenant identity separation, AI control-plane pattern, cost attribution gap |

### Input context — synthesized feasibility deliverables (DESIGN source of truth)

Under `.dev/releases/backlog/mastra-beads-port-feasibility/`:

| File | Purpose | Use in tech reference |
|---|---|---|
| `FEASIBILITY-STUDY.md` (181 KB) | Full validated study (Sections 1-10) | Primary DESIGN source: architecture rationale, option matrix (A/B/C/D), gaps, roadmap, risks |
| `DECISION-SUMMARY.md` (8.5 KB) | Exec memo | Verdict, D→A path, spike exit gates SG1-SG4, 5 honesty statements |
| `ROADMAP.md` (10 KB) | Phased roadmap (Phases 0-5, gates G0-G5) | Section 13 Extension / Section 14 future; the strangler-fig sequencing |
| `RISK-REGISTER.md` (7.8 KB) | R1-R9 risk register | Section 14 Tech Debt & Known Limitations |
| `merged-requirements.md` (37 KB) | Requirements | Cross-ref for completeness |
| `seed-brief.md` (6.3 KB) | Problem statement | Section 1 framing |

### Existing-Python seam files (BUILT side — verified at HEAD `9e864860`)

All confirmed present during scope discovery (line counts from `wc -l`):

| Path | Lines | Role |
|---|---:|---|
| `src/superclaude/cli/pipeline/models.py` | 234 | Contract vocabulary (`Step`,`GateCriteria`,`GateMode`,`StepResult`,`Deliverable`) |
| `src/superclaude/cli/pipeline/executor.py` | 469 | Generic step sequencer / `execute_pipeline()` / `StepRunner` |
| `src/superclaude/cli/pipeline/gates.py` | 142 | Tiered gate enforcement (`gate_passed()`) |
| `src/superclaude/cli/pipeline/process.py` | 244 | **`ClaudeProcess` — THE runtime seam the port replaces** |
| `src/superclaude/cli/pipeline/trailing_gate.py` | 647 | Async/trailing gate machinery |
| `src/superclaude/cli/pipeline/deliverables.py` | 194 | Deliverable decomposition |
| `src/superclaude/cli/roadmap/executor.py` | 3701 | Roadmap orchestration (largest) |
| `src/superclaude/cli/roadmap/gates.py` | 1441 | 15 named roadmap gates |
| `src/superclaude/cli/tasklist/executor.py` | 276 | **Pilot port candidate** (`tasklist validate`) |
| `src/superclaude/cli/sprint/executor.py` | 2148 | Sprint orchestration (hardest port) |
| `src/superclaude/cli/sprint/config.py` | 509 | Phase/task parser (compatibility contract) |
| `src/superclaude/cli/sprint/checkpoints.py` | 408 | Checkpoint manifest/verify |
| `src/superclaude/cli/sprint/process.py` | 385 | Sprint `ClaudeProcess` subclass |

Harness counts at HEAD: **42 commands, 39 agents, 24 skills** (match research file 05).

---

## PATTERNS_AND_CONVENTIONS

| Pattern | Evidence | Relevance to the architecture |
|---|---|---|
| Single runtime seam | `cli/pipeline/process.py::ClaudeProcess` (+ `sprint/process.py` subclass) | `[CODE-VERIFIED]` The one boundary the adapter replaces; everything above it is runtime-agnostic |
| Generic step/gate pipeline core | `cli/pipeline/` | `[CODE-VERIFIED]` Strongest TS/Zod contract-extraction target |
| Blocking vs trailing gates | `gates.py`, `trailing_gate.py` | `[CODE-VERIFIED]` Maps to Mastra sync validation vs async scorers `[DESIGN]` |
| Strangler-fig replatforming | FEASIBILITY-STUDY §8, ROADMAP Phases 0-5 | `[DESIGN]` Python stays the oracle; wrap one pipeline at a time |
| Python-as-oracle (parity gating) | ROADMAP G1-G3 | `[DESIGN]` Each ported step must match native CLI verdict before native reimpl |
| Stable-ID contract | `07:` ownership matrix; `TASK-*`,`R-###`,`T<PP>.<TT>`,`D-####` | `[CODE-VERIFIED]` IDs (format) → `[DESIGN]` cross-system join key |
| Work-of-record split | DECISION-SUMMARY honesty stmt 4 | `[DESIGN]` Backlog.md = prose owner; Beads = graph/memory/gates |
| Fan-out → consolidate → verify | `sc-adversarial`, `cleanup_audit`, `prd`, `roadmap` | `[CODE-VERIFIED]` pattern → `[DESIGN]` maps to Mastra durable fan-out |
| File-first artifacts w/ frontmatter | roadmap/tasklist/MDTM outputs | `[CODE-VERIFIED]` Backlog.md can own markdown artifacts `[DESIGN]` |
| Numbered-checkpoint contract | `09:127-154`; `checkpoints.py` | `[CODE-VERIFIED]` Canonical form + the Path A `_verify_checkpoints()` gap |

### Known stale/contradiction findings to surface (Section 14)

- `CERTIFY_GATE` defined in `roadmap/gates.py` but never wired into production `_build_steps()` (`02`). **Roadmap says preserve, do not normalize.**
- `wiring-verification` declares TRAILING but `grace_period=0` forces blocking (`02`, `11:66-67`).
- Path A (per-task) does NOT call `_verify_checkpoints()` (`09`, `03`).
- Stale `### Checkpoint:` references in `sprint/process.py` prompt + `phase-template.md` vs canonical numbered form (`09`).
- Source-of-truth conflict `src/superclaude/` vs `plugins/superclaude/` (`05`,`11`).
- `11` claims no `sprint rerun-tasks` — but memory `reference_sprint_rerun_tasks` says it shipped v4.3.0. **Spot-check at HEAD; correct in doc.**

---

## FEATURE_ANALYSIS (subsystems for Section 5)

Eight architecture subsystems, each with a built/design tag:

| # | Subsystem | Tag | What it is |
|---|---|---|---|
| 5.1 | Existing pipeline-core seam | `[CODE-VERIFIED]` | The runtime-agnostic step/gate/process kernel being adapted (`cli/pipeline/`) |
| 5.2 | Roadmap & tasklist workflows | `[CODE-VERIFIED]` + `[DESIGN]` map | Ported workflows; tasklist-validate = pilot |
| 5.3 | Sprint execution runtime | `[CODE-VERIFIED]` + `[DESIGN]` map | Hardest port surface (subprocess supervision, checkpoints, dual-path) |
| 5.4 | Reusable harness corpus | `[CODE-VERIFIED]` | 42 commands / 39 agents / 24 skills / core / templates / hooks as instruction IP |
| 5.5 | Target data model & ownership | `[DESIGN]` | Mastra vs Backlog.md vs Beads boundaries; stable-ID join; work-of-record split |
| 5.6 | Adapter / seam-replacement layer | `[DESIGN]` | The 4 adapter contracts; Mastra step = `StepRunner`; CLI shell-out (hybrid) |
| 5.7 | External component substrate | `[EXTERNAL-VERIFIED]` | Mastra workflows/Workspace, Backlog.md CLI/MCP, Beads `bd`/Dolt, MCP |
| 5.8 | Governance / multi-tenant control plane | `[DESIGN — NOT PROVIDED]` | The net-new layer none of the 3 components supplies |

Complexity → **Heavyweight** (8 subsystems, cross-cutting, 20+ source files + 3 external tools + governance plane). Target 1,200–1,800 lines.

---

## RECOMMENDED_OUTPUTS

### Output document

**Path:** `.dev/releases/backlog/mastra-beads-port-feasibility/ARCHITECTURE-TECHNICAL-REFERENCE.md`

**Rationale:** Co-located with its inputs (FEASIBILITY-STUDY/ROADMAP/RISK-REGISTER/DECISION-SUMMARY) and matches that directory's ALL-CAPS deliverable convention. This is design/backlog work for a not-yet-built system — it does NOT belong under `docs/` (which is for shipped-feature docs). Aligns with the "write files next to their source" principle.

### Synthesis file mapping (8 files → template sections)

| Synth file | Template sections | Primary evidence (synthesis map A–H) |
|---|---|---|
| `synth-01-overview-architecture.md` | 1 Overview, 2 Architecture | A, F; design decisions D→A; option matrix; FEASIBILITY §1-2 |
| `synth-02-directory-dataflow.md` | 3 Directory Structure, 4 Data Flow | existing `cli/` layout (verified) + proposed adapter layout + hybrid data flow (tasklist→Backlog/Beads→Mastra→reconcile) |
| `synth-03-subsystems-existing.md` | 5.1, 5.2, 5.3 | B, C — pipeline seam + roadmap/tasklist + sprint (files 01,02,03,09) |
| `synth-04-subsystems-target.md` | 5.4, 5.5, 5.6, 5.7, 5.8 | D, E, G, F, H — harness + data model + adapter + external substrate + governance (files 05,07,04,web-01..04) |
| `synth-05-datamodel-integration.md` | 6 State & Data Model, 7 Contract/Workflow Inventory, 8 API & Integration | E, G, F — ownership matrix, 4 adapter contracts, external integration surfaces |
| `synth-06-config-errors-perf.md` | 9 Configuration & Environment, 10 Error Handling & Recovery, 11 Performance Characteristics | F, H — Mastra OSS/EE licensing, Beads version-pin + server mode, durability/suspend-resume/checkpoint recovery, drift detection; Perf mostly `[DESIGN/UNVERIFIED]` |
| `synth-07-conventions-extension-debt.md` | 12 Conventions & Patterns, 13 Extension Guide, 14 Known Limitations & Tech Debt | patterns; "add a wrapped pipeline"/"add a Beads gate"/"add a tenant" extension recipes; R1-R9 + 4 critical gaps + unbuilt status |
| `synth-08-verification-glossary.md` | 15 Verification & Accuracy, 16 Glossary | Built-vs-Design Status Ledger; HEAD `9e864860`; spot-check protocol; term definitions |

8 synth files > 4 → Phase 5 analyst+QA must **partition**.

### Section applicability notes

- **Section 6** repurposed "State Management" → **"State & Data Model"** (backend): TurnLedger/CheckpointEntry/StepResult state `[CODE-VERIFIED]` + Mastra/Backlog/Beads ownership `[DESIGN]`.
- **Section 7** repurposed "Component Inventory" → **"Contract & Workflow Inventory"**: pipeline contracts + the 4 adapter contracts (NOT a frontend component tree; note the repurpose).
- **Section 11 Performance** is largely `[DESIGN — UNVERIFIED]`: no integrated system to measure. State durability/concurrency *characteristics-by-design* only, explicitly flagged; cite `[EXTERNAL]` Mastra/Beads behaviors where known.

---

## SUGGESTED_PHASES

### Phase 2 — Deep Investigation (ADAPTED: ingest + targeted spot-check)

1. **Agent 2.1 — Evidence Index Builder** (Doc Analyst). Read the 15 pre-completed research files + DECISION-SUMMARY + ROADMAP + RISK-REGISTER; produce `research/00-evidence-index.md` mapping every needed claim → (source research file, source code path/line where applicable, built/design/external tag) → target template section. This is the bridge between the feasibility evidence and the tech-ref template. Output: `${TASK_DIR}research/00-evidence-index.md`.
2. **Agent 2.2 — Spot-check: pipeline core seam** (Code Tracer). Re-read at HEAD `9e864860`: `cli/pipeline/{models,executor,gates,process,trailing_gate,deliverables}.py`. Confirm research file 01's key symbol/line claims; emit a delta of any drift. Output: `${TASK_DIR}research/spot-01-pipeline.md`.
3. **Agent 2.3 — Spot-check: roadmap/tasklist** (Code Tracer). Re-read `cli/roadmap/{executor,gates}.py`, `cli/tasklist/executor.py`; confirm `_build_steps()` order, `CERTIFY_GATE` unwired, `TASKLIST_FIDELITY_GATE`, wiring-verification grace=0. Output: `${TASK_DIR}research/spot-02-roadmap-tasklist.md`.
4. **Agent 2.4 — Spot-check: sprint runtime + checkpoint + rerun-tasks** (Code Tracer). Re-read `cli/sprint/{executor,config,checkpoints,process,commands}.py`; confirm Path A skips `_verify_checkpoints()`, numbered-checkpoint contract, **and resolve the `rerun-tasks` contradiction** (research file 11 says absent; memory says shipped v4.3.0 — check `sprint/commands.py`). Output: `${TASK_DIR}research/spot-03-sprint.md`.
5. **Agent 2.5 — Spot-check: harness corpus** (Integration Mapper). Confirm 42 commands / 39 agents / 24 skills at HEAD; confirm `hooks.json`, core/* presence, `src/` vs `plugins/` source-of-truth state. Output: `${TASK_DIR}research/spot-04-harness.md`.

(5 agents, spawned in parallel. Lightweight reads — confirm-or-flag, NOT re-investigation.)

### Phase 3 — Research Completeness Verification (analyst + rf-qa, parallel)

- rf-analyst (completeness-verification) + rf-qa (research-gate) over the evidence index + 4 spot-check deltas + the 15 source research files (treated as prior evidence). Verify: built/design tags present, code claims still valid at HEAD, no claim that lacks a source. **Partition** (>6 files): 2 analyst + 2 qa instances.

### Phase 4 — Web Research (PRE-COMPLETED)

- Single bookkeeping item: record that web-01..04 are the external evidence base (Mastra/Backlog/Beads/MCP), already current as of 2026-06-02. Spawn a fresh web agent ONLY if Phase 5 surfaces a specific external gap. No default web spawning.

### Phase 5 — Synthesis (8 agents) + Synthesis QA Gate

- 8 synthesis agents → synth-01..08 per the mapping table. **Every agent** embeds the built-vs-design demarcation rule and the "this is a design reference, not a feasibility reformat" rule.
- Then rf-analyst (synthesis-review) + rf-qa (synthesis-gate, fix_authorization:true), **partitioned** (8 synth files > 4): 2+2 instances.

### Phase 6 — Assembly & Validation

- rf-assembler → `ARCHITECTURE-TECHNICAL-REFERENCE.md` (incremental, template order).
- rf-qa (report-validation, fix_authorization:true): template sections present, Heavyweight 1,200-1,800 line budget, no source-code reproduction, file-path validity for `[CODE-VERIFIED]` claims, **every architectural claim carries a built/design/external tag**, Built-vs-Design Status Ledger present in §15.
- rf-qa-qualitative (tech-ref-qualitative, fix_authorization:true): does it read as a coherent design reference; are `[DESIGN]` items never presented as built; are the adapter contracts actionable; do the risks/gaps survive.

### Phase 7 — Present to User & Complete Task

- Present: doc location, line count/tier, built-vs-design split summary, artifact locations, residual gaps. Update frontmatter → 🟢 Done; Task Log entry. (Anti-orphaning: completion items inside Phase 7.)

---

## TEMPLATE_NOTES

- **Tier: Heavyweight** — all sections; 1,200-1,800 lines. Justified by 8 cross-cutting subsystems + 3 external tools + governance plane.
- **Frontmatter adaptation:** `status: 🟡 Draft`; `parent_doc` → FEASIBILITY-STUDY.md; `related_docs` → ROADMAP.md, RISK-REGISTER.md, DECISION-SUMMARY.md; `verified_against_code.code_version: 9e864860`; add a tag `design-reference` to signal not-yet-built.
- **Section 1 Overview MUST** state up-front that this documents a PROPOSED architecture (verdict: conditionally recommended, spike-first) and define the built-vs-design tag legend.
- **Sections 6/7 repurposed** (see applicability notes). **Section 11** mostly `[DESIGN/UNVERIFIED]`.
- **Section 15** MUST contain the Built-vs-Design Status Ledger (every subsystem: built / partially-built-seam / design-only) — this is the single most important integrity control for an unbuilt-architecture reference.
- Use MDTM **Template 02** (complex): discovery (ingest+spot-check), parallel synthesis, 3 QA gates, assembly, conditional gap-fill.

## AMBIGUITIES_FOR_USER

None blocking — framing was explicitly confirmed by the user (Option 1: tech-ref of target design, adapt skill). One resolved contradiction to verify in Phase 2 (the `sprint rerun-tasks` presence: research file 11 says absent, memory `reference_sprint_rerun_tasks` says shipped v4.3.0 — Agent 2.4 resolves at HEAD). Output path chosen as co-located ALL-CAPS deliverable; flagged here for visibility, not a blocker.
