---
source_skill: prd
component_count: 9
total_lines: 3242
analysis_date: 2026-04-12
---

# Portify Analysis: PRD Skill

## 1. Workflow Summary

The PRD skill produces comprehensive Product Requirements Documents through a two-stage, multi-agent pipeline with persistent task tracking.

**Stage A — Scope Discovery & Task File Creation** (orchestrator-driven, 8 steps):
The orchestrator parses the user request, classifies PRD scope (Product vs Feature), performs codebase exploration to map the product space, writes structured research notes (7-category format), reviews sufficiency (8-point gate, max 2 gap-fill rounds), selects a tier (Lightweight/Standard/Heavyweight), then spawns `rf-task-builder` to create an MDTM task file encoding all subsequent work as self-contained checklist items.

**Stage B — Task File Execution** (delegated to `/task` skill):
The `/task` skill reads the generated task file and executes its 7 phases via the F1 loop (READ 2192 IDENTIFY 2192 EXECUTE 2192 UPDATE 2192 REPEAT):

| Phase | Activity | Agent Types | Parallelism |
|-------|----------|-------------|-------------|
| 1. Preparation | Scope confirmation, template read, tier select | None (orchestrator) | Sequential |
| 2. Deep Investigation | Codebase research per product area | Feature/Doc/Integration/UX/Architecture Analysts | Parallel (2201310+ agents) |
| 3. Completeness Verification | Research quality gate | rf-analyst + rf-qa | Parallel pair; partitioned if >6 files |
| 4. Web Research | External market/competitive data | Web research agents | Parallel (020134 agents) |
| 5. Synthesis + QA Gate | Template-aligned section generation | Synthesis agents, then rf-analyst + rf-qa | Parallel synth; parallel QA pair |
| 6. Assembly & Validation | Final document construction + 3 QA passes | rf-assembler (single), rf-qa (structural), rf-qa-qualitative (content) | Sequential chain |
| 7. Present & Complete | Deliver to user, offer downstream docs | None (orchestrator) | Sequential |

The pipeline is resumable: progress is persisted as checked/unchecked boxes in the MDTM task file on disk. Context compression or session restart triggers re-read from the first unchecked item.

**Tier scaling:**
- **Lightweight** (<5 files): 220133 codebase agents, 020131 web agents, 4002013800 line PRD
- **Standard** (5201320 files): 420136 codebase agents, 120132 web agents, 80020131,500 line PRD
- **Heavyweight** (20+ files): 6201310+ codebase agents, 220134 web agents, 1,50020132,500 line PRD

---

## 2. Component Analysis

### 2.1 Runtime Components

| # | Component | Lines | Role | Consumer | Load Phase |
|---|-----------|-------|------|----------|------------|
| 1 | `SKILL.md` | 455 | Orchestration: Stage A/B flow, input spec, tier selection, output locations, phase loading contract, critical rules, session management | Claude Code / Orchestrator | Session start + A.12013A.8 |
| 2 | `refs/agent-prompts.md` | 422 | 8 agent prompt templates: codebase research, web research, synthesis, research analyst (rf-analyst), research QA (rf-qa), synthesis QA, report validation QA, assembly (rf-assembler) | `rf-task-builder` subagent | A.7 (builder only) |
| 3 | `refs/build-request-template.md` | 165 | BUILD_REQUEST scaffold with field definitions (GOAL, WHY, TASK_ID_PREFIX, TEMPLATE, PRD_SCOPE, DOCUMENTATION_STALENESS_WARNINGS), tier parameters, phase mapping, granularity requirements | Orchestrator 2192 passed to builder | A.7 (orchestrator) |
| 4 | `refs/synthesis-mapping.md` | 142 | PRD output skeleton (28 numbered sections + appendices) + 9-row synth-file-to-template-section mapping table | `rf-task-builder` subagent | A.7 (builder only) |
| 5 | `refs/validation-checklists.md` | 153 | 4 sections: Synthesis Quality Review (9 analyst + 3 QA items), Assembly Process (steps 8201311), Validation Checklist (18 structural + 4 content quality), Content Rules (10-rule Do/Donu2019t table) | `rf-task-builder` subagent | A.7 (builder only) |
| 6 | `refs/operational-guidance.md` | 110 | 16 critical execution rules, research quality signals (strong/weak/escalation), artifact location table, PRD update protocol, session management guidance | `rf-task-builder` subagent | A.7 (builder only) |

**Runtime total: 1,447 lines across 6 files.**

### 2.2 Non-Runtime Components

| # | Component | Lines | Purpose |
|---|-----------|-------|---------|
| 7 | `refs/.gitkeep` | 0 | Directory retention placeholder |
| 8 | `REFACTORING_SPEC.md` | 422 | Documents the refactoring from monolithic SKILL to modular SKILL+refs |
| 9 | `SKILL_Original.md` | 1,373 | Pre-refactoring monolithic SKILL.md preserved as reference |

**Non-runtime total: 1,795 lines (55% of package is archival).**

### 2.3 Phase Loading Contract

The skill enforces strict phase isolation. Each phase declares which refs it loads; loading outside declared phases is a contract violation:

| Phase | Actor | Declared Loads | Forbidden Loads |
|-------|-------|----------------|------------------|
| Invocation | Claude Code | SKILL.md | All 5 refs/* |
| A.12013A.6 | Orchestrator | SKILL.md | All 5 refs/* |
| A.7 (orchestrator) | Orchestrator | `refs/build-request-template.md` | None |
| A.7 (builder) | `rf-task-builder` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` | None |
| A.8 | Orchestrator | SKILL.md | All refs/ except build-request |
| Stage B | `/task` skill | Generated task file | All refs/* + build-request |

**Validation rules:** `declared_loads 2229 forbidden_loads = 2205` for every phase; `runtime_loaded_refs 2286 declared_loads` for every phase.

### 2.4 Agent Ecosystem

| Agent Type | Subagent ID | Spawned In | Role |
|------------|-------------|------------|------|
| Feature Analyst | `general-purpose` Agent | Phase 2 | Inventory product capabilities from code |
| Doc Analyst | `general-purpose` Agent | Phase 2 | Cross-validate docs against code (staleness protocol) |
| Integration Mapper | `general-purpose` Agent | Phase 2 | Map APIs, boundaries, external dependencies |
| UX Investigator | `general-purpose` Agent | Phase 2 | Trace user interaction patterns |
| Architecture Analyst | `general-purpose` Agent | Phase 2 | System design, dependency chains, tech choices |
| Web Researcher | `general-purpose` Agent | Phase 4 | Market data, competitive landscape, industry trends |
| Synthesis Agent | `general-purpose` Agent | Phase 5 | Transform research files into template-aligned sections |
| Research Analyst | `rf-analyst` | Phases 3, 5 | 8-item completeness verification / 9-item synthesis review |
| Research QA | `rf-qa` | Phases 3, 5 | 11-item research gate / 12-item synthesis gate |
| Report Validation QA | `rf-qa` | Phase 6 | 18+4 item structural/content validation |
| Qualitative QA | `rf-qa-qualitative` | Phase 6 | 23-item product/engineering content review |
| Assembler | `rf-assembler` | Phase 6 | Consolidate 9 synth files into final PRD |
| Task Builder | `rf-task-builder` | Stage A.7 | Create MDTM task file from research notes + refs |

---

## 3. Data Flow

### 3.1 Information Flow

```
User Request
    2502
    25bc
[Orchestrator: A.12013A.6] ======================== Stage A ========================
    2502  Reads: SKILL.md, codebase (Glob/Grep/codebase-retrieval)
    2502  Writes: ${TASK_DIR}research-notes.md (7 categories)
    2502
    25bc
[Orchestrator: A.7]
    2502  Reads: refs/build-request-template.md
    2502  Fills BUILD_REQUEST with scope data from research notes
    2502  Spawns rf-task-builder subagent
    2502       2502
    2502       2502  Builder reads: 4 refs files + research-notes.md + MDTM template 02
    2502       2502  Builder writes: ${TASK_DIR}${TASK_ID}.md (task file)
    2502       2502  (Embeds full agent prompts from refs/ into each checklist item)
    2502
    25bc
[Orchestrator: A.8] -- verifies task file structure
    2502
    25bc
[/task skill: Stage B] ======================== Stage B ========================
    2502  F1 loop: READ 2192 IDENTIFY 2192 EXECUTE 2192 UPDATE 2192 REPEAT
    2502
    251c25002500 Phase 2: Deep Investigation (PARALLEL)
    2502      2201310+ research agents 2192 research/[NN]-[topic].md
    2502      (each agent follows Incremental File Writing + Doc Staleness Protocol)
    2502
    251c25002500 Phase 3: Completeness Gate (PARALLEL)
    2502      rf-analyst 2192 qa/analyst-completeness-report.md
    2502      rf-qa      2192 qa/qa-research-gate-report.md
    2502      VERDICT: PASS 2192 continue | FAIL 2192 fix cycle (max 3)
    2502      Compile 2192 gaps-and-questions.md
    2502
    251c25002500 Phase 4: Web Research (PARALLEL)
    2502      020134 web agents 2192 research/web-[NN]-[topic].md
    2502
    251c25002500 Phase 5: Synthesis + QA Gate (PARALLEL then PARALLEL)
    2502      Up to 9 synth agents 2192 synthesis/synth-[NN]-[topic].md
    2502      then:
    2502      rf-analyst 2192 qa/analyst-synthesis-review.md
    2502      rf-qa      2192 qa/qa-synthesis-gate-report.md
    2502      VERDICT: PASS 2192 continue | FAIL 2192 fix cycle (max 2)
    2502
    251c25002500 Phase 6: Assembly & Validation (SEQUENTIAL)
    2502      rf-assembler  2192 docs/.../PRD_[NAME].md (incremental)
    2502      rf-qa         2192 qa/qa-report-validation.md (fix in-place)
    2502      rf-qa-qualit. 2192 qa/qa-qualitative-review.md (fix in-place)
    2502
    251425002500 Phase 7: Present & Complete
           Update task file: status 2192 Done, write Task Log
           Offer downstream: /tdd, archive consolidation sources
```

### 3.2 Key Data Contracts

| Contract | From 2192 To | Format | Critical Fields |
|----------|-----------|--------|-----------------|
| Research Notes | Orchestrator (A.4) 2192 Builder (A.7) | 7-section markdown | EXISTING_FILES, SUGGESTED_PHASES (per-agent detail), RECOMMENDED_OUTPUTS, PRD_SCOPE |
| BUILD_REQUEST | Orchestrator (A.7) 2192 rf-task-builder | Structured prompt (~165 lines) | GOAL, WHY, PRD_SCOPE, TEMPLATE (01/02), DOCUMENTATION_STALENESS_WARNINGS, SKILL CONTEXT FILES |
| MDTM Task File | Builder 2192 /task skill | Checklist markdown (B2 items) | Each item = self-contained prompt with embedded agent instructions |
| QA Verdicts | rf-analyst/rf-qa 2192 Orchestrator | Report with PASS/FAIL | Verdict, per-item findings, fix actions, severity ratings |
| Doc Staleness Tags | Research agents 2192 Synthesis 2192 Assembly | Inline markers | `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]` |

### 3.3 Artifact Accumulation (Standard Tier)

| Category | Pattern | Count | Written By |
|----------|---------|-------|------------|
| Task file | `TASK-PRD-*.md` | 1 | rf-task-builder (A.7) |
| Research notes | `research-notes.md` | 1 | Orchestrator (A.4) |
| Codebase research | `research/[NN]-*.md` | 420136 | Research agents (Phase 2) |
| Web research | `research/web-[NN]-*.md` | 120132 | Web agents (Phase 4) |
| Synthesis files | `synthesis/synth-[NN]-*.md` | up to 9 | Synthesis agents (Phase 5) |
| Gaps log | `gaps-and-questions.md` | 1 | Orchestrator (Phase 3) |
| QA/analyst reports | `qa/*.md` | 420136 | rf-analyst, rf-qa, rf-qa-qualitative (Phases 3, 5, 6) |
| Final PRD | `docs/.../PRD_*.md` | 1 | rf-assembler (Phase 6) |
| **Total** | | **~18201327** | |

---

## 4. Complexity Assessment

### 4.1 Scoring

| Dimension | Score (120135) | Evidence |
|-----------|-------------|----------|
| **Orchestration complexity** | 4 | Two-stage architecture, phase loading contract with forbidden-loads enforcement, tier-based scaling, BUILD_REQUEST as structured handoff |
| **Agent coordination** | 5 | Up to 10+ concurrent subagents, 13 distinct agent roles, partitioning thresholds (>6/>4), parallel pairs, sequential chains |
| **State management** | 4 | MDTM task file as persistent state, 7-category research notes, incremental file writing, session resumption from unchecked items |
| **Quality assurance** | 5 | 3 mandatory gates, dual analyst+QA agents per gate, fix cycles with max retry (3+2), HALT-on-exhaustion, 43+ validation checklist items, zero-trust philosophy |
| **Content domain rules** | 4 | 16 critical rules, documentation staleness protocol (3-tier tagging), Feature PRD section overrides (8 rules), 10 content format rules |
| **Branching logic** | 3 | Existing task detection (resume/new), scenario A/B, tier selection, Feature/Product PRD classification, fix-cycle escalation |
| **External dependencies** | 3 | Requires /task skill, 6 subagent types, MDTM templates at `.gfdoc/templates/`, PRD template at `docs/docs-product/templates/` |
| **Overall** | **4.3/5** | **High complexity — one of the most complex skills in the framework** |

### 4.2 Portability Challenges

| Challenge | Severity | Detail |
|-----------|----------|--------|
| Subagent ecosystem | Critical | Requires 6 distinct subagent types (rf-task-builder, rf-analyst, rf-qa, rf-qa-qualitative, rf-assembler, general-purpose). Each has behavioral contracts encoded as natural-language prompts. |
| Skill cross-dependency | High | Stage B delegates to `/task` skill; Phase 7 offers `/tdd`. Not self-contained. |
| MDTM template dependency | High | Task file creation requires MDTM Template 02 at `.gfdoc/templates/`. Template format defines B2 self-contained items, E1-E4 flat structure. |
| Behavioral contracts | High | 16 critical rules + documentation staleness protocol + incremental writing mandate are enforced via prompt instructions to LLM agents. Porting requires deciding: programmatic enforcement vs. preserved prompts vs. convention. |
| Phase loading contract | Moderate | Formal set-intersection constraints on file access per phase. Currently a design contract, not runtime-enforced. CLI port must decide enforcement mechanism. |
| Codebase exploration tools | Moderate | Scope discovery uses Glob, Grep, codebase-retrieval (Auggie MCP). Alternative tools could substitute. |

### 4.3 Token / Context Budget

| Actor | Files Loaded | Est. Tokens | When |
|-------|-------------|-------------|------|
| Orchestrator (A.12013A.6) | SKILL.md | ~2,200 | Invocation |
| Orchestrator (A.7) | SKILL.md + build-request-template | ~3,000 | Task creation |
| Builder subagent | 4 refs files + research notes + MDTM template | ~4,500 | A.7 |
| /task execution | Task file only | ~2,00020134,000 | Stage B |
| **Max single-actor load** | | **~4,500** | Builder is heaviest |

The modular architecture succeeds at distributing context: no single actor holds more than ~4,500 tokens of skill content.

---

## 5. Recommendations

### 5.1 Portify Strategy

**Recommended: Preserve the two-stage architecture.** The clean split between scope discovery (Stage A, deterministic) and delegated execution (Stage B, agent-driven) maps well to a CLI pipeline:

- **Stage A 2192 CLI `prd plan` command**: Parse input, explore codebase, write research notes, generate task file. Primarily deterministic logic.
- **Stage B 2192 CLI `prd run` command**: Execute the task file via an internalized F1 loop (or delegate to `superclaude sprint run`).

The phase loading contract should be preserved: refs files are read only by the builder, never by the main orchestrator. This prevents context bloat in both LLM-agent and CLI contexts.

### 5.2 Files to Port vs. Drop

| File | Action | Rationale |
|------|--------|-----------|
| `SKILL.md` | **Port** | Core orchestration logic 2192 becomes CLI state machine |
| `refs/agent-prompts.md` | **Port** | Agent prompt templates 2192 become parameterized Jinja2/string templates |
| `refs/build-request-template.md` | **Port** | BUILD_REQUEST 2192 becomes task file generator input schema |
| `refs/synthesis-mapping.md` | **Port** | Section mapping 2192 becomes config table |
| `refs/validation-checklists.md` | **Port** | Validation logic 2192 becomes programmatic checklist evaluation |
| `refs/operational-guidance.md` | **Port** | Runtime rules 2192 becomes constants/config |
| `SKILL_Original.md` | **Drop** | Archive; git history preserves it |
| `REFACTORING_SPEC.md` | **Drop** | Process doc; no runtime value |
| `refs/.gitkeep` | **Drop** | Directory placeholder |

### 5.3 Critical Preservation Requirements

1. **BUILD_REQUEST contract**: The structured handoff encodes tier parameters, scope classification, and 8 Feature PRD section-override rules. Must be preserved verbatim.
2. **B2 self-contained items**: Every task file item must be a complete, executable prompt with no external references. This is what makes the pipeline resumable.
3. **QA gate semantics**: PASS/FAIL with bounded fix cycles (3 research, 2 synthesis, HALT on exhaustion) are core quality guarantees.
4. **Partitioning thresholds**: >6 research files / >4 synthesis files trigger multi-instance QA. Calibrated to context window limits.
5. **Documentation staleness protocol**: The `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` tagging chain through research 2192 synthesis 2192 assembly prevents hallucinated capabilities in the final PRD.

### 5.4 Simplification Opportunities

1. **Remove archival files from skill package**: REFACTORING_SPEC.md + SKILL_Original.md = 1,795 lines (55% of package). Moving to `.dev/` or `docs/` cuts the package to 1,447 lines.
2. **Consolidate operational-guidance into validation-checklists**: The critical rules and artifact locations partially overlap between `operational-guidance.md` and SKILL.md. Merging would reduce builder load from 4 refs to 3.
3. **Extract Feature PRD overrides**: The 8 section-level rules are embedded inline in `build-request-template.md`. Extracting to a structured format improves maintainability and testability.
4. **Template BUILD_REQUEST programmatically**: The markdown fill-in-the-blanks approach could be replaced with structured input (JSON/YAML) generating the prompt string.

### 5.5 Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| Agent prompt drift after porting | Task file items diverge from source templates | Version-stamp prompts; checksum in task file header |
| Phase contract not enforced at runtime | Context bloat if builder loads wrong files | Add lint step validating declared vs actual loads |
| QA fix-cycle exhaustion path untested | Execution halts without graceful recovery | Add integration test for 3-cycle-fail scenario |
| Staleness tag propagation loss | Unverified claims leak into final PRD | Add synthesis-gate check verifying no untagged doc-sourced claims |
| Feature PRD override rules fragile | Wrong sections filled/skipped for Feature PRDs | Extract overrides to testable config; add unit test per rule |
| Partitioning boundary ambiguity | Exactly 6 or 4 files — is threshold inclusive? | Clarify: thresholds are strictly-greater-than (">6", ">4") |
