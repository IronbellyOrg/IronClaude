# synth-02 — Sections 3 (Directory Structure) & 4 (Data Flow)

**Target document:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture — Technical Reference
**Synthesis owner:** synth-02 (→ template §3-4)
**Status:** Complete
**Date:** 2026-06-03
**Code version (existing facts):** HEAD `9e864860`

## Tag legend (R2)

| Tag | Meaning | Evidence basis |
|---|---|---|
| `[CODE-VERIFIED]` | Existing Python in `src/superclaude/cli/`; real `path:line`, HEAD `9e864860` | spot-01..04, evidence-index §5.1-5.6, RF 01/07 |
| `[DESIGN — UNBUILT]` | Target hybrid layout/flow; evidence is feasibility/research, not code | evidence-index §5.5-5.6 DESIGN rows, RF 07, FEASIBILITY-STUDY |
| `[EXTERNAL-VERIFIED]` | Mastra/Backlog/Beads/MCP capability from web-01..04 | evidence-index §5.7-5.8 |

> **CRITICAL:** No source file in the repository implements any Mastra/Backlog.md/Beads integration at HEAD `9e864860` (evidence-index 5.6-27). Every adapter directory and every hybrid routing hop in this document is `[DESIGN — UNBUILT]`. The existing `src/superclaude/cli/` tree below is the only built artifact.

---

## 3. Directory Structure

This section pairs the **existing** orchestration source tree (`[CODE-VERIFIED]`, HEAD `9e864860`) with a **proposed** adapter-layer layout (`[DESIGN — UNBUILT]`). The existing tree is the surface a hybrid port wraps; the proposed layer is additive and does not exist in the repository today.

### 3.1 Existing `src/superclaude/cli/` Orchestration Layout — `[CODE-VERIFIED]`

> **Source:** on-disk listing at HEAD `9e864860` (`ls src/superclaude/cli/{pipeline,roadmap,tasklist,sprint}`); roles per evidence-index 5.1-5.3, spot-01 (pipeline, 80/80 confirmed), RF 01. File counts: pipeline 25, roadmap 26, tasklist 6, sprint 19 `.py` files (`__pycache__` omitted).

```
src/superclaude/cli/                  # Click CLI root; main.py registers sprint/roadmap/
│                                     #   tasklist/cli-portify/prd/eval/cleanup-audit (cli/main.py:400-426)
│                                     #   NOTE: pipeline/ is a shared library package, NOT a root command (5.7-32)
│
├── pipeline/                         # [CODE-VERIFIED] Framework-neutral execution core — THE port seam
│   ├── models.py                     #   Shared dataclasses/enums: Step, StepResult, GateCriteria,
│   │                                 #     PipelineConfig, StepStatus, GateMode (models.py:1-235; 5.1-01..10)
│   ├── executor.py                   #   Generic step sequencer: retry/gates/parallel; StepRunner protocol
│   │                                 #     is the process-boundary seam (executor.py:41-60,63-188; 5.1-11..20)
│   ├── process.py                    #   ClaudeProcess — sole `claude --print` subprocess boundary;
│   │                                 #     SINGLE runtime substitution point (process.py:24-244; spot-01 §seam)
│   ├── gates.py                      #   Pure-Python tiered gate validation, no subprocess (gates.py:1-142; 5.1-21..23)
│   ├── trailing_gate.py              #   Async trailing-gate eval + deferred remediation log (trailing_gate.py:1-648; 5.1-29..36)
│   ├── deliverables.py               #   Behavioral detection + implement/verify decomposition (deliverables.py:1-194; 5.1-37..39)
│   ├── diagnostic_chain.py           #   4-stage deterministic diagnostic assembly (diagnostic_chain.py:1-247; 5.1-40..41)
│   ├── __init__.py                   #   42-symbol public API surface (compatibility anchors) (__init__.py:1-157; 5.1-42)
│   └── guard_*/fmea_*/dataflow_*/    #   Static-analysis passes (guard, FMEA, dataflow, conflict,
│       conflict_*/invariant*/...     #     invariants, mutation, state) — exported via __init__ (5.1-42)
│
├── roadmap/                          # [CODE-VERIFIED] Spec→roadmap pipeline; delegates to execute_pipeline
│   ├── commands.py                   #   `roadmap run` CLI surface + flags (commands.py:32-298; 5.2-03)
│   ├── executor.py                   #   Input routing, step DAG, hybrid Claude/Python steps,
│   │                                 #     resume/convergence (executor.py:74-3187; 5.2-01,04..08)
│   ├── gates.py                      #   All roadmap gate definitions (gates.py:1020-1441; 5.2-13)
│   ├── convergence.py                #   Deviation registry + fidelity convergence cycles (convergence.py:90-668; 5.2-15..16)
│   ├── remediate*.py                 #   Remediation tasklist gen + parallel per-file executor (5.2-17..18)
│   ├── validate_executor.py          #   Auto-invoked roadmap→spec fidelity validation (validate_executor.py:239-519; 5.2-09)
│   └── models.py / prompts.py / ...  #   RoadmapConfig, prompt builders, spec parsers, checkers
│
├── tasklist/                         # [CODE-VERIFIED] Roadmap→tasklist VALIDATION only (no `generate` CLI)
│   ├── commands.py                   #   Exposes ONLY `validate` subcommand (commands.py:31-82; 5.2-21)
│   ├── executor.py                   #   Single tasklist-fidelity step via shared execute_pipeline
│   │                                 #     (executor.py:23-25,191-276; 5.2-02,22)
│   ├── gates.py                      #   TASKLIST_FIDELITY_GATE (gates.py:23-46; 5.2-21)
│   ├── prompts.py                    #   Fidelity prompt + skill-only generator prompt (prompts.py:17-234; 5.2-23..24)
│   └── models.py / __init__.py       #   Tasklist validation config
│                                     #   NOTE: tasklist GENERATION is skill/protocol behavior, not CLI (5.2-24)
│
└── sprint/                           # [CODE-VERIFIED] Phase/task execution runtime (~8,568 lines, 19 files; 5.3-01)
    ├── commands.py                   #   `sprint run/attach/status/logs/kill/verify-checkpoints` (commands.py:15-207; 5.3-02..03)
    ├── config.py                     #   Phase discovery + tasklist parser (THE compat contract) (config.py:15-492; 5.3-04..06)
    ├── models.py                     #   SprintConfig(extends PipelineConfig), TaskEntry, TaskResult,
    │                                 #     PhaseStatus(11), TurnLedger, MonitorState (models.py:24-777; 5.3-07..10,17)
    ├── executor.py                   #   Core loop; TWO paths: Path A per-task / Path B freeform phase
    │                                 #     (executor.py:1135-2148; 5.3-11..16,23)
    ├── process.py                    #   Sprint ClaudeProcess subclass → /sc:task prompt (process.py:88-216; 5.3-13,18)
    ├── monitor.py / tui.py / tmux.py #   NDJSON stream reader, Rich TUI, tmux session (5.3-19..22)
    ├── checkpoints.py                #   Checkpoint extraction/verification/recovery (checkpoints.py:36-408; 5.3-26..27)
    ├── diagnostics.py / summarizer.py#   Failure diagnostics, phase summaries, retrospective (5.3-29..31)
    └── logging_.py / classifiers.py /#   JSONL+MD logs (status/logs read = STUBS, 5.3-28), KPIs, notify
        kpi.py / notify.py / ...      #
```

**Existing-tree key facts (all `[CODE-VERIFIED]`):**

| Fact | Evidence | Tag |
|---|---|---|
| `pipeline/` has zero imports from sprint/roadmap (framework-neutral) | `pipeline/models.py:1-5`, `executor.py:7` (NFR-007); 5.1-01,11 | `[CODE-VERIFIED]` |
| `ClaudeProcess` is the **single** `claude --print` subprocess boundary | `pipeline/process.py:24-244`; spot-01 §seam | `[CODE-VERIFIED]` |
| roadmap/tasklist consume the **shared** `execute_pipeline` + injected `run_step` | `roadmap/executor.py:26`, `tasklist/executor.py:23-25`; 5.2-01..02 | `[CODE-VERIFIED]` |
| sprint reuses shared models/remediation but runs its **own** phase loop | `sprint/executor.py:12-16`; 5.1-43, 5.3-11 | `[CODE-VERIFIED]` |
| `superclaude pipeline` is NOT a root Click command (library only) | `cli/main.py:400-426` vs `pipeline/__init__.py:1-21`; 5.7-32 | `[CODE-VERIFIED]` |

### 3.2 Proposed Adapter-Layer Directory Layout — `[DESIGN — UNBUILT]`

> **CRITICAL:** The tree below **does not exist** in the repository at HEAD `9e864860`. It is a design sketch derived from RF 07 adapter contracts (5.5-14), the verified migration method (5.6-25), and the hybrid/strangler posture (XC-02, XC-11..16). Directory names, module boundaries, and language (TS for Mastra workflows vs Python adapters) are proposals, not commitments.

```
adapters/                             # [DESIGN — UNBUILT] New top-level adapter layer (additive; wraps cli/)
│                                     #   Posture: read-only first → hybrid pilot → parity port (XC-14)
│
├── backlog/                          # [DESIGN] Prose / task / doc / decision owner (Backlog.md)
│   ├── import_tasklist.*             #   Contract 1: tasklist bundle → Backlog markdown import (RF07 Contract 1; 5.5-14)
│   │                                 #     MUST round-trip so discover_phases()/parse_tasklist_file() still pass
│   ├── export_tasklist.*             #   Reconcile Backlog state → tasklist-index.md + phase-N-tasklist.md
│   │                                 #     (preserve T<PP>.<TT> IDs verbatim; 5.5-04, RF07 rule 4)
│   └── schema_map.*                  #   MDTM frontmatter ↔ Backlog Task fields; MCP rejects unknown props (5.7-13)
│
├── beads/                            # [DESIGN] Dependency-graph mirror owner (Beads / Dolt)
│   ├── graph_sync.*                  #   Contract 2: tasklist/Backlog deps → Beads edges (RF07 Contract 2)
│   │                                 #     upsert by stable external ID; propose patch on divergence (5.5-14)
│   ├── gate_bridge.*                 #   Map gate FAIL/HALT → Beads blocker issues; bd gate check (5.7-22)
│   └── ready_claim.*                 #   bd ready + atomic --claim for multi-agent scheduling (5.7-20; XC-16)
│
├── mastra/                           # [DESIGN] Workflow run / trace / gate-execution owner (Mastra, TS)
│   ├── plan_builder.*                #   Contract 3: Backlog+Beads → deterministic Mastra workflow plan (RF07 Contract 3)
│   │                                 #     one workflow/bundle, one stage/phase, T<PP>.<TT> as step ID
│   ├── runner_seam.*                 #   StepRunner adapter: Mastra step → existing ClaudeProcess (hybrid)
│   │                                 #     OR native provider (parity). Substitutes behind executor.py:41-60 seam
│   ├── reconcile.*                   #   Contract 4: Mastra results → Backlog log + Beads status (idempotent) (RF07 Contract 4)
│   └── trace_map.*                   #   Attach R-*/T*/D-*/phase/tier/model as span metadata (5.5-08)
│
├── governance/                       # [DESIGN] Control-plane layer NOT supplied by any of the 3 components (5.8-11)
│   ├── tenant_registry.*             #   tenant / actor / authorization identities — ABSENT from current models (5.5-15)
│   ├── cost_attribution.*            #   Per-tenant token+tool metering (supersedes sprint-local TurnLedger; 5.5-09)
│   └── tool_catalog.*                #   Curated approved-tool/MCP inventory + versioned contracts (5.8-12)
│
└── contracts/                        # [DESIGN] Shared adapter contract + round-trip validation tests
    ├── ids.*                         #   Stable-ID invariants (TASK-*, T<PP>.<TT>, D-####, R-###) (5.5-04)
    ├── roundtrip_tests.*             #   Acceptance gate: import→export must satisfy sprint parser (RF07 §High-Level)
    └── return_contract.yaml          #   Reuse cli_portify return-contract pattern as adapter bridge record (5.6-04)
```

**Proposed-layer design constraints (all `[DESIGN — UNBUILT]` unless noted):**

| Constraint | Source | Tag |
|---|---|---|
| One prose owner (Backlog), one graph owner (Beads), one run owner (Mastra) | RF07 ownership rules 1-3; 5.5-12..13 | `[DESIGN — UNBUILT]` |
| Stable IDs preserved verbatim, never regenerated on import/export | RF07 rule 4; 5.5-04 | `[DESIGN — UNBUILT]` |
| Governance plane is **additional** — none of the 3 components supply tenancy/audit/cost | 5.8-09..11 | `[EXTERNAL-VERIFIED]` |
| Adapters MUST satisfy sprint parser round-trip as acceptance gate | RF07 Contract 1 validation; 5.5-11 | `[DESIGN — UNBUILT]` |
| Runner seam substitutes behind existing `StepRunner` (no second seam class) | `pipeline/executor.py:41-60`; spot-01 §seam | `[CODE-VERIFIED]` (seam) + `[DESIGN]` (adapter) |

### 3.3 File Naming Conventions

| Pattern | Convention | Example | Tag |
|---|---|---|---|
| Existing CLI subpackage | `<surface>/<role>.py` (commands/executor/gates/models/process) | `sprint/executor.py` | `[CODE-VERIFIED]` |
| Existing sprint phase file | `phase-N-tasklist.md` (canonical) + aliases `pN-`, `phase_N_`, `tasklist-pN-` | `phase-1-tasklist.md` | `[CODE-VERIFIED]` (5.3-04) |
| Existing task heading | `### T<PP>.<TT> -- Title` (dash/em-dash) | `### T01.03 -- Build importer` | `[CODE-VERIFIED]` (5.5-11) |
| Proposed adapter module | `<component>/<contract-verb>.<ext>` | `backlog/import_tasklist.py` | `[DESIGN — UNBUILT]` |

---

## 4. Data Flow

### 4.1 Primary Data Flow (Proposed Hybrid) — `[DESIGN — UNBUILT]`

> **CRITICAL:** The end-to-end flow below is a **proposed** hybrid routing. Only the marked **existing seams** (parser, `execute_pipeline`, `ClaudeProcess`, gates, file artifacts) are `[CODE-VERIFIED]`. Every routing hop into Backlog.md / Beads / Mastra is `[DESIGN — UNBUILT]`; all Backlog/Beads/Mastra capabilities consumed are `[EXTERNAL-VERIFIED]` (web-01..04). No integration code exists at HEAD `9e864860` (5.6-27).

```
                          ┌──────────────────────────────────────────────────┐
                          │  SOURCE OF RECORD (EXISTING, file-owned)          │
                          │  MDTM tasklist bundle:                            │  [CODE-VERIFIED]
                          │  tasklist-index.md + phase-N-tasklist.md          │  5.2-25, 5.5-01..04
                          │  ### T<PP>.<TT> -- Title  +  **Dependencies:**    │
                          └───────────────┬──────────────────────────────────┘
                                          │ (A) parse  [CODE-VERIFIED seam]
                                          │ sprint/config.py:374-492 discover_phases/parse_tasklist
                                          v
            ┌─────────────────────────────────────────────────────────────────┐
            │  ADAPTER INGEST (PROPOSED)  [DESIGN — UNBUILT]                    │
            │  Contract 1: tasklist bundle → import (RF07 Contract 1; 5.5-14)   │
            └───────┬─────────────────────────────────────────────┬───────────┘
        (B) prose   │                                  (C) graph   │
        [DESIGN]    v                                  [DESIGN]    v
   ┌────────────────────────────┐               ┌─────────────────────────────────┐
   │ BACKLOG.md                 │   (D) deps    │ BEADS (Dolt graph)              │
   │ PROSE / TASK / DOC OWNER   │──[DESIGN]────>│ DEPENDENCY-GRAPH + GATES OWNER  │
   │ task body, AC, decisions   │   sync deps   │ bd ready / --claim / blockers   │
   │ [EXTERNAL-VERIFIED 5.7-11] │<──patch only──│ [EXTERNAL-VERIFIED 5.7-19..22]  │
   └─────────────┬──────────────┘  (no silent   └────────────────┬────────────────┘
                 │                   md rewrite)                  │
                 │  (E) Backlog + Beads → workflow plan  [DESIGN] │
                 │      Contract 3 (RF07; deterministic dry-run)  │
                 v                                                v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ MASTRA DURABLE WORKFLOW   RUN / TRACE / GATE-EXECUTION OWNER  [DESIGN]      │
   │ one workflow/bundle, one stage/phase, T<PP>.<TT> = step ID                 │
   │ suspend()/resume() durable snapshots [EXTERNAL-VERIFIED 5.7-01..02]        │
   └───────────────┬───────────────────────────────────────────────────────────┘
                   │ (F) StepRunner adapter  [DESIGN wrapper] over [CODE-VERIFIED seam]
                   │     pipeline/executor.py:41-60 StepRunner protocol
                   v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ EXECUTION SEAM (EXISTING)  [CODE-VERIFIED]                                 │
   │ HYBRID: Mastra step → existing ClaudeProcess (`claude --print`)           │
   │ pipeline/process.py:24-244 (sole subprocess boundary; spot-01 §seam)      │
   │ → gate_passed() tiered validation  pipeline/gates.py:20-76 (5.1-22)       │
   └───────────────┬───────────────────────────────────────────────────────────┘
                   │ (G) results + gate outcomes
                   v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ RECONCILE BACK (PROPOSED)  [DESIGN — UNBUILT]                              │
   │ Contract 4 (RF07; idempotent): Mastra results → Backlog log + Beads status│
   │ telemetry/cost → Mastra traces (NOT md/issue bodies)  5.5-08, RF07 C4     │
   └───────────────┬───────────────────────────────────────────────────────────┘
                   │ (H) export round-trip  [DESIGN] — MUST satisfy sprint parser
                   v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ FILE ARTIFACTS (EXISTING, file-owned)  [CODE-VERIFIED ownership]           │
   │ tasklist-index.md/phase-N-tasklist.md (regenerated), checkpoint reports,  │
   │ execution-log.jsonl/.md, phase-*-result.md  (sprint/models.py:473-510)    │
   └──────────────────────────────────────────────────────────────────────────┘
```

**Flow narrative (hop tags):**

- **(A) Parse** — `[CODE-VERIFIED]`. The sprint parser (`sprint/config.py:374-492`) is the existing, strict ingest contract any adapter must satisfy; markdown tasklists are **ordered execution records**, not active graphs (5.7-31).
- **(B/C) Ingest split** — `[DESIGN — UNBUILT]`. Prose routes to Backlog.md; dependency edges route to Beads (Contract 1, 5.5-14).
- **(D) Backlog↔Beads sync** — `[DESIGN]`. Beads owns the queryable graph but must **propose patches, not silently rewrite** markdown (RF07 rule 2); Backlog/Beads integration is immature (5.7-17, FR #588).
- **(E) Plan build** — `[DESIGN]`. Deterministic Mastra plan from Backlog+Beads (Contract 3); dry-run before side effects (5.6-25 preflight).
- **(F) Runner seam** — `[DESIGN]` wrapper over `[CODE-VERIFIED]` seam. Mastra steps invoke the existing `StepRunner` (`pipeline/executor.py:41-60`); hybrid mode keeps `ClaudeProcess` as execution oracle (RF07 §High-Level rule 4).
- **(G) Execute + gate** — `[CODE-VERIFIED]`. `ClaudeProcess` (`process.py:24-244`) + pure-Python `gate_passed()` (`gates.py:20-76`) remain runner-authored truth (5.7-30).
- **(H) Reconcile + round-trip** — `[DESIGN]`. Idempotent write-back (Contract 4); export MUST round-trip through the parser as the acceptance gate (5.5-11, RF07 Contract 1 validation).

### 4.2 Data Sources

| Source | Type | Location | Description | Tag |
|---|---|---|---|---|
| MDTM tasklist bundle | File (markdown) | `tasklist-index.md` + `phase-N-tasklist.md` | Ordered phases/tasks with `T<PP>.<TT>` IDs + `**Dependencies:**`; current source of record | `[CODE-VERIFIED]` (5.2-25, 5.5-01..04) |
| MDTM task file frontmatter | File (YAML) | `.dev/tasks/.../TASK-*.md` | id/title/status/type/priority/dates/deps/tags | `[CODE-VERIFIED]` (5.5-01) |
| Shared pipeline `Step` | In-memory dataclass | `pipeline/models.py:108-123` | Portable workflow-step contract (id/prompt/output_file/gate/...) | `[CODE-VERIFIED]` (5.5-05) |
| Sprint `TaskEntry` | Parsed dataclass | `sprint/config.py:374-492`, `models.py:24-37` | Task id/title/deps/command/classifier (stores deps, executes in file order) | `[CODE-VERIFIED]` (5.3-06..07) |
| Execution outputs/logs | File | release dir: `execution-log.jsonl/.md`, `phase-*-result.md`, per-task output/error | Runner-authored results, file-owned | `[CODE-VERIFIED]` (5.5-07) |
| Backlog.md task store | External CLI/MCP | `backlog/` dir; MCP stdio | Proposed prose/task/doc owner; MCP rejects unknown props | `[EXTERNAL-VERIFIED]` (5.7-11..13) |
| Beads graph | External CLI (Dolt) | `.beads/` (Dolt-first; JSONL = export only) | Proposed dependency-graph + gate owner; `bd ready`/`--claim` | `[EXTERNAL-VERIFIED]` (5.7-19..23) |
| Mastra workflow store | External runtime (TS) | libSQL/Postgres/etc. storage | Proposed run/trace/gate-execution owner; durable suspend/resume | `[EXTERNAL-VERIFIED]` (5.7-01..05) |
| Tenant/actor/cost identity | (absent) | — | NOT present in current models; must be added by governance plane | `[CODE-VERIFIED]` (absence, 5.5-15) + `[DESIGN]` (5.8-11) |

### 4.3 Data Transformations

Each row marks whether the transformation is an **existing seam** (`[CODE-VERIFIED]`) or **proposed hybrid routing** (`[DESIGN — UNBUILT]`).

| Transformation | Input | Output | Location | Tag |
|---|---|---|---|---|
| Tasklist parse | `phase-N-tasklist.md` text | `Phase` + `TaskEntry` objects (deps, command, classifier) | `sprint/config.py:374-492` (`discover_phases`/`parse_tasklist`) | `[CODE-VERIFIED]` (5.3-04..06) |
| Behavioral decompose | `Deliverable` description | `.a` implement + `.b` verify steps | `pipeline/deliverables.py:146-194` | `[CODE-VERIFIED]` (5.1-39) |
| Step execute | `Step` + `PipelineConfig` | `StepResult` (status/timestamps/remediation) | `pipeline/executor.py:191-399` via `StepRunner` | `[CODE-VERIFIED]` (5.1-15) |
| Subprocess run | prompt (stdin) | stdout→output_file or `.log` sidecar; exit code | `pipeline/process.py:114-157` (`ClaudeProcess`) | `[CODE-VERIFIED]` (5.1-25..27) |
| Gate validation | output file + `GateCriteria` | `(passed, reason)`; `.compressed.md` sidecar preferred | `pipeline/gates.py:20-76`, `executor.py:23-35` | `[CODE-VERIFIED]` (5.1-12,22) |
| Tasklist → Backlog import | tasklist bundle | Backlog task/doc hierarchy (IDs preserved) | `adapters/backlog/import_tasklist.*` (Contract 1) | `[DESIGN — UNBUILT]` (5.5-14, RF07 C1) |
| Deps → Beads graph sync | `TaskEntry.dependencies` | Beads directed edges (upsert by external ID) | `adapters/beads/graph_sync.*` (Contract 2) | `[DESIGN — UNBUILT]` (5.5-14, RF07 C2) |
| Backlog+Beads → Mastra plan | task bodies + graph | deterministic Mastra workflow plan (dry-run) | `adapters/mastra/plan_builder.*` (Contract 3) | `[DESIGN — UNBUILT]` (RF07 C3) |
| Mastra runner seam | Mastra step | invocation of existing `StepRunner`/`ClaudeProcess` | `adapters/mastra/runner_seam.*` over `executor.py:41-60` | `[DESIGN]` wrapper + `[CODE-VERIFIED]` seam |
| Results → reconcile | `StepResult`/gate outcomes | Backlog log rows + Beads status (idempotent) | `adapters/mastra/reconcile.*` (Contract 4) | `[DESIGN — UNBUILT]` (RF07 C4) |
| Export round-trip | reconciled state | regenerated `tasklist-index.md`+`phase-N-tasklist.md` | `adapters/backlog/export_tasklist.*` | `[DESIGN — UNBUILT]` (must pass parser, 5.5-11) |
| Gate FAIL/HALT → blocker | `GateOutcome` FAIL/DEFERRED/HALT | Beads blocker issue + remediation edge | `adapters/beads/gate_bridge.*` (`bd gate check`) | `[DESIGN — UNBUILT]` (5.7-22, RF07 C4) |
| Cost/telemetry attribution | `TurnLedger`/`MonitorState` | per-tenant cost in Mastra traces (not md/issue) | `adapters/governance/cost_attribution.*` | `[DESIGN — UNBUILT]` (5.5-08..09, 5.8-07) |

> **Note:** The transformation chain deliberately keeps **runner-authored truth and gate semantics on the existing seams** (parse → execute → gate → file artifact). The hybrid design adds Backlog/Beads/Mastra as additional owners and routing hops but must not relocate the authoritative gate/result computation, which is pure-Python and runtime-agnostic (5.7-30). A behavioral change — making Beads/Backlog graphs **active** rather than the current ordered execution records — is itself `[DESIGN — UNBUILT]` (5.7-31), not a runtime swap.

---

**Status: Complete**

Sections 3 (Directory Structure: 3.1 existing tree `[CODE-VERIFIED]`, 3.2 proposed adapter layout `[DESIGN — UNBUILT]`, 3.3 naming) and 4 (Data Flow: 4.1 hybrid flow diagram, 4.2 Data Sources, 4.3 Data Transformations) are present. Existing `src/superclaude/cli/` tree and existing seams tagged `[CODE-VERIFIED]` at HEAD `9e864860`; all Backlog/Beads/Mastra adapter layout and hybrid routing hops tagged `[DESIGN — UNBUILT]`; external substrate capabilities tagged `[EXTERNAL-VERIFIED]`.
