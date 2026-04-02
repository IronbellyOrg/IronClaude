# Dependency Map: Command → Protocol/Agent → Artifacts

**Generated**: 2026-04-02
**Scope**: Full dependency chains for SC tasklist/adversarial and RF taskbuilder/pipeline, showing how commands invoke protocols, protocols invoke agents, and agents produce artifacts.

---

## A) SuperClaude Dependency Chains

### /sc:tasklist

```
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>]
│
├── INPUT VALIDATION (command layer)
│   ├── Roadmap file exists and is non-empty
│   ├── Spec file exists (if --spec provided)
│   ├── Output parent dir exists (if --output provided)
│   └── TASKLIST_ROOT derivation succeeds (if --output not provided)
│       ├── Priority 1: Match `.dev/releases/current/<segment>/` in roadmap text
│       ├── Priority 2: Match `v<digits>(.<digits>)+` version token
│       └── Priority 3: Fallback `.dev/releases/current/v0.0-unknown/`
│
├── SKILL INVOCATION
│   └── Skill: sc:tasklist-protocol (SKILL.md, 51KB)
│       │
│       ├── READS (from skill package)
│       │   ├── rules/tier-classification.md (reference; logic is inline in SKILL.md)
│       │   ├── rules/file-emission-rules.md (reference; logic is inline)
│       │   ├── templates/index-template.md (structural template)
│       │   └── templates/phase-template.md (structural template)
│       │
│       ├── READS (from user input)
│       │   ├── <roadmap-path> (sole source of truth)
│       │   └── <spec-path> (optional supplementary context)
│       │
│       ├── PRODUCES (Stages 1-6: Generation)
│       │   ├── TASKLIST_ROOT/tasklist-index.md
│       │   │   ├── Metadata & Artifact Paths table
│       │   │   ├── Phase Files table
│       │   │   ├── Source Snapshot
│       │   │   ├── Deterministic Rules Applied
│       │   │   ├── Roadmap Item Registry (R-001, R-002, ...)
│       │   │   ├── Deliverable Registry (D-0001, D-0002, ...)
│       │   │   ├── Traceability Matrix (R-### → T<PP>.<TT> → D-#### → paths → Tier → Confidence)
│       │   │   ├── Execution Log Template
│       │   │   ├── Checkpoint Report Template
│       │   │   ├── Feedback Collection Template
│       │   │   └── Glossary (if roadmap defines terms)
│       │   │
│       │   └── TASKLIST_ROOT/phase-N-tasklist.md (one per phase)
│       │       └── Tasks: T<PP>.<TT> with 13-field metadata, deliverables,
│       │           steps (PLANNING/EXECUTION/VERIFICATION/COMPLETION),
│       │           acceptance criteria (4 bullets), validation (2 bullets),
│       │           checkpoints every 5 tasks + end-of-phase
│       │
│       └── PRODUCES (Stages 7-10: Validation)
│           └── TASKLIST_ROOT/validation/
│               ├── validation-report.md (drift detection results)
│               └── patch-log.md (corrections applied)
│
└── DOWNSTREAM CONSUMER
    └── `superclaude sprint run` (Python CLI)
        └── Reads tasklist-index.md → discovers phase-N-tasklist.md files
            → executes tasks per phase with /sc:task-unified tier compliance
```

### superclaude tasklist validate (Python CLI)

```
superclaude tasklist validate <output-dir> [--roadmap-file] [--tasklist-dir] [--model] [--max-turns]
│
├── IMPORTS FROM
│   ├── cli/pipeline/executor.py → execute_pipeline()
│   ├── cli/pipeline/process.py → ClaudeProcess
│   ├── cli/pipeline/models.py → PipelineConfig, Step, StepResult, StepStatus, GateCriteria, SemanticCheck
│   ├── cli/roadmap/gates.py → _high_severity_count_zero(), _tasklist_ready_consistent()
│   └── cli/roadmap/prompts.py → _OUTPUT_FORMAT_BLOCK
│
├── READS
│   ├── <roadmap-file> (default: {output_dir}/roadmap.md)
│   └── <tasklist-dir>/*.md (all markdown files, sorted)
│
├── BUILDS
│   └── Fidelity prompt (build_tasklist_fidelity_prompt)
│       ├── Validation layering guard: roadmap→tasklist ONLY
│       ├── Severity definitions: HIGH/MEDIUM/LOW (embedded to reduce drift)
│       └── Format: deviation report from Phase 2
│
├── EXECUTES
│   └── Claude subprocess via ClaudeProcess
│       └── Context isolation: prompt + --file inputs only
│
├── APPLIES GATE
│   └── TASKLIST_FIDELITY_GATE
│       ├── Required frontmatter: high_severity_count, medium_severity_count,
│       │   low_severity_count, total_deviations, validation_complete, tasklist_ready
│       ├── Semantic check: high_severity_count == 0
│       └── Semantic check: tasklist_ready consistent with counts
│
└── PRODUCES
    └── Fidelity report in output_dir
```

### /sc:adversarial

```
/sc:adversarial --compare file1,file2[,...,fileN] [options]
/sc:adversarial --source <file> --generate <type> --agents <spec>[,...] [options]
/sc:adversarial --pipeline "<shorthand>" | --pipeline @pipeline.yaml [options]
│
├── SKILL INVOCATION
│   └── Skill: sc:adversarial-protocol (SKILL.md, 123KB)
│       │
│       ├── READS (from skill package)
│       │   ├── refs/agent-specs.md (agent specification format)
│       │   ├── refs/artifact-templates.md (6 artifact templates)
│       │   ├── refs/debate-protocol.md (round structure, steelman rules)
│       │   └── refs/scoring-protocol.md (quantitative + qualitative algorithms)
│       │
│       ├── READS (from user input)
│       │   ├── Mode A: 2-10 existing files (--compare)
│       │   └── Mode B: source file (--source) + generation type (--generate)
│       │
│       ├── DELEGATES TO (in-process agents via Task tool)
│       │   ├── Variant generation agents (Mode B): 2-10 parallel, model[:persona[:instruction]]
│       │   ├── Analytical agent (Step 1: diff analysis)
│       │   ├── debate-orchestrator agent (Step 2: manages debate, Step 3: scoring)
│       │   ├── Advocate agents (Step 2: 2-10 per variant, parallel Round 1, sequential Round 2-3)
│       │   └── merge-executor agent (Step 5: dedicated specialist)
│       │
│       └── PRODUCES
│           ├── <output>/adversarial/variant-N-<agent>.md (2-10 variants)
│           ├── <output>/adversarial/diff-analysis.md (Step 1)
│           ├── <output>/adversarial/debate-transcript.md (Step 2)
│           ├── <output>/adversarial/base-selection.md (Step 3)
│           ├── <output>/adversarial/refactor-plan.md (Step 4)
│           ├── <output>/adversarial/merge-log.md (Step 5)
│           ├── <output>/<merged-output>.md (final merged artifact)
│           └── RETURN CONTRACT (mandatory):
│               ├── merged_output_path: string | null
│               ├── convergence_score: float 0.0-1.0 | null
│               ├── artifacts_dir: string (always set)
│               ├── status: success | partial | failed
│               └── base_variant: string (model:persona) | null
│
├── CALLED BY (integration points)
│   ├── /sc:roadmap (multi-spec/multi-roadmap modes)
│   ├── /sc:tasklist (pipeline output as sprint input)
│   └── /sc:design, /sc:spec-panel, /sc:improve (various integration patterns)
│
└── PIPELINE MODE (DAG orchestration)
    ├── Parse shorthand or YAML → phase graph
    ├── Topological sort → execution levels
    ├── --pipeline-parallel: max concurrent phases per level (1-10, default 3)
    ├── Artifact routing between phases (output of one = input of next)
    ├── --pipeline-resume: manifest-based checkpoint resume
    ├── --pipeline-on-error: halt | continue (independent branches)
    └── --auto-stop-plateau: halt on <5% delta across 2 consecutive compare phases
```

---

## B) Rigorflow Dependency Chains

### /rf:taskbuilder (Interactive, User-Facing)

```
/rf:taskbuilder [output-name-or-path]
│
├── TEMPLATE DISCOVERY (reads first found)
│   ├── .gfdoc/templates/02_mdtm_template_complex_task.md (preferred)
│   ├── .gfdoc/templates/01_mdtm_template_generic_task.md
│   ├── templates/01_mdtm_template_generic_task.md
│   └── 01_mdtm_template_generic_task.md
│
├── INTERVIEW (3 stages, user interaction)
│   ├── Stage 1: Core Intent (goal, why, outputs, context)
│   ├── Stage 2: Phases & Steps (3-6 phases, 3-8 steps each)
│   └── Stage 3: Guardrails (deps, verification, blockers, workflow docs,
│       quality gates, metadata, context files)
│
├── REFERENCES
│   ├── .gfdoc/rules/prompts/agent_library.md (agent assignment guidance)
│   └── .gfdoc/rules/contextual/context_embedding.md (context file guidance)
│
├── INTERVIEW NOTES (persisted between stages)
│   └── .dev/tasks/taskbuildernotes/rf_taskbuilder_notes_<timestamp>.md
│
├── VALIDATION (12-point silent checklist before writing)
│   ├── Valid YAML frontmatter with all required fields
│   ├── All 6 mandatory sections in order
│   ├── All actionable items are checkboxes
│   ├── No nested checkboxes
│   ├── Self-contained check (single paragraph with action+output+gate)
│   ├── Integrated verification ("ensuring..." clause)
│   ├── No standalone reads
│   ├── Completion gates present
│   ├── Evidence on failure only
│   └── No removed sections (Outputs & Deliverables, Success Criteria, etc.)
│
└── PRODUCES
    └── .dev/tasks/TASK-IB-<YYYYMMDD-HHMMSS>.md
        ├── YAML frontmatter (id, title, status, type, priority, assigned_to, ...)
        ├── Key Objectives
        ├── Prerequisites & Dependencies
        ├── Detailed Task Instructions (phases → self-contained checklist items)
        ├── Error Handling
        ├── Post-Completion Actions
        └── Task Log / Notes
```

### /rf:pipeline (Automated, Agent Team)

```
/rf:pipeline [request description]
│
├── Phase 1: PARSE, TRIAGE, SPLIT (team lead)
│   ├── Extract: GOAL, WHY, OUTPUTS, CONTEXT
│   ├── Triage: Scenario A (explicit) | Scenario B (vague)
│   └── Split: 1-5 tracks (independent work streams only)
│
├── Phase 2: CREATE TEAM
│   └── TeamCreate: "rf-pipeline"
│       ├── ~/.claude/teams/rf-pipeline/config.json
│       └── ~/.claude/tasks/rf-pipeline/ (shared task list)
│
├── Phase 3: CREATE COORDINATION TASKS
│   └── Per track: 3 tasks with dependencies
│       ├── research (#N) ──blocks──► build (#N+1) ──blocks──► execute (#N+2)
│       └── No cross-track dependencies
│
├── Phase 4: SPAWN RESEARCHER(S)
│   └── Agent: rf-task-researcher (one per track, all spawned in parallel)
│       │
│       ├── READS (codebase exploration)
│       │   ├── Source files via Glob/Grep/Read
│       │   ├── .gfdoc/templates/*.md (to understand task format)
│       │   ├── .dev/tasks/ (existing task examples)
│       │   └── External docs via WebSearch (for new implementations)
│       │
│       ├── OPTIONALLY INVOKES
│       │   └── Skill: rf:opinion (trade-off analysis for significant decisions)
│       │
│       └── PRODUCES
│           └── .dev/tasks/research-notes-[track-T-]<timestamp>.md
│               ├── EXISTING_FILES
│               ├── PATTERNS_AND_CONVENTIONS
│               ├── SOLUTION_RESEARCH (if new implementation)
│               ├── RECOMMENDED_OUTPUTS
│               ├── SUGGESTED_PHASES
│               ├── TEMPLATE_NOTES
│               └── AMBIGUITIES_FOR_USER
│
├── Phase 5: REVIEW RESEARCH → SPAWN BUILDER(S)
│   │
│   ├── GATE: Team lead reads research notes, evaluates sufficiency
│   │   ├── Insufficient → message researcher for revision (loop)
│   │   └── Sufficient → spawn builder
│   │
│   └── Agent: rf-task-builder (one per track, event-driven spawning)
│       │
│       ├── READS
│       │   ├── Research notes (from researcher)
│       │   ├── MDTM template (01 or 02, as directed by team lead)
│       │   │   ├── .gfdoc/templates/01_mdtm_template_generic_task.md
│       │   │   └── .gfdoc/templates/02_mdtm_template_complex_task.md
│       │   └── External docs via WebSearch (for unfamiliar tech)
│       │
│       └── PRODUCES
│           └── .dev/tasks/TASK-RF-[track-T-]<timestamp>.md
│               ├── YAML frontmatter
│               ├── Self-contained checklist items (session-rollover safe)
│               ├── Phase structure with handoff patterns (if template 02)
│               └── Error handling and post-completion sections
│
├── Phase 6: SPAWN EXECUTOR (event-driven per track)
│   └── Agent: rf-task-executor (one per track)
│       │
│       ├── VALIDATES
│       │   └── Task file: exists, valid frontmatter, has checklist items
│       │
│       ├── INVOKES
│       │   └── bash .gfdoc/scripts/automated_qa_workflow.sh <task> <batch_size> 0
│       │       │
│       │       ├── SOURCES (at startup)
│       │       │   ├── .gfdoc/scripts/input_validation.sh
│       │       │   ├── .gfdoc/scripts/session_message_counter.sh
│       │       │   └── .gfdoc/scripts/rollover_context_functions.sh
│       │       │
│       │       ├── INVOKES (per batch)
│       │       │   ├── .gfdoc/scripts/parse_checklist.py (extract items)
│       │       │   ├── .gfdoc/scripts/compute_uid_index.py (UID tracking)
│       │       │   └── .gfdoc/scripts/UID_fail_item_match_fallback.py (fallback matching)
│       │       │
│       │       ├── SPAWNS (per batch)
│       │       │   ├── Worker Claude subprocess (claude --continue <session> -p <prompt>)
│       │       │   │   └── Loads: ib_agent_core.md, quality_gates.md,
│       │       │   │       anti_hallucination_task_completion_rules.md,
│       │       │   │       anti_sycophancy.md, file_conventions.md
│       │       │   │
│       │       │   └── QA Claude subprocess (claude -p <qa_prompt>)
│       │       │       └── Receives: expected items, programmatic handoff,
│       │       │           worker handoff, fs snapshots, conversation snippets
│       │       │
│       │       └── PRODUCES (per batch)
│       │           ├── .dev/tasks/TASK-RF-*/batch_N_state.json
│       │           ├── .dev/tasks/TASK-RF-*/expected_batchN.json
│       │           ├── .dev/tasks/TASK-RF-*/fs_snapshot_pre_batchN.json
│       │           ├── .dev/tasks/TASK-RF-*/fs_snapshot_post_batchN.json
│       │           ├── .dev/tasks/TASK-RF-*/programmatic_handoff_batchN.json
│       │           ├── .dev/tasks/TASK-RF-*/handoffs/worker_handoff_batchN.md
│       │           ├── .dev/tasks/TASK-RF-*/qa_reports/qa_report_batchN.md
│       │           ├── .dev/tasks/TASK-RF-*/outputs/worker_session_batchN.json
│       │           ├── .dev/tasks/TASK-RF-*/outputs/qa_session_batchN.json
│       │           ├── .dev/tasks/TASK-RF-*/verification_batchN.json
│       │           └── .dev/tasks/TASK-RF-*/logs/task_progress.log
│       │
│       └── REPORTS
│           └── EXECUTION_COMPLETE to team-lead
│               ├── Status: SUCCESS | PARTIAL | FAILED
│               ├── Items completed: X/Y
│               └── Outputs created: [file list]
│
├── Phase 7-8: MONITOR → REPORT
│   ├── Relay NEED_USER_INPUT, EXECUTION_PROGRESS, BLOCKED
│   ├── Per-track error isolation
│   └── Final report: per-track status + overall status
│
└── Phase 9: CLEANUP
    ├── shutdown_request to all agents
    └── TeamDelete (removes team + task dirs)
```

### /rf:project (Multi-Phase Project)

```
/rf:project [description]
│
├── Phase 0: PLANNING (produces planning artifacts)
│   ├── Feature brief (.gfdoc/templates/04_feature_brief_template.md)
│   ├── PRD (.gfdoc/templates/05_prd_template.md)
│   └── Architecture proposal (.gfdoc/templates/06_architecture_proposal_template.md)
│
├── Project plan creation
│   └── .dev/tasks/project-plan-<timestamp>.md
│       (from .gfdoc/templates/03_project_plan_template.md)
│
├── Phase 1..N: EXECUTION (each invokes /rf:pipeline)
│   └── /rf:pipeline with:
│       ├── Phase-specific goal from architecture proposal
│       ├── Cross-phase context (outputs from prior phases)
│       └── Fix cycles (max 3 per phase) for issue resolution
│
└── FINAL REPORT
    └── Summary of all phases and outputs
```

---

## Cross-Framework Integration Points

```
SC → RF (no direct integration):
  - SC tasklist produces Sprint CLI-compatible bundles
  - RF produces MDTM task files for automated_qa_workflow.sh
  - Different execution runtimes, different artifact schemas

SC ↔ SC (internal integration):
  /sc:adversarial ←called-by── /sc:roadmap (multi-spec mode)
  /sc:adversarial ←called-by── /sc:tasklist (pipeline merged output → tasklist input)
  /sc:adversarial ←called-by── /sc:design, /sc:spec-panel, /sc:improve
  /sc:tasklist    ──feeds────► superclaude sprint run (Python CLI)
  /sc:tasklist    ──uses─────► /sc:task-unified (tier compliance during execution)

RF ↔ RF (internal integration):
  /rf:pipeline    ──spawns───► rf-task-researcher → rf-task-builder → rf-task-executor
  /rf:project     ──invokes──► /rf:pipeline (per execution phase)
  /rf:run         ──spawns───► rf-task-builder → rf-task-executor (no researcher)
  rf-task-researcher ──invokes──► /rf:opinion (trade-off analysis)
  rf-task-executor   ──invokes──► automated_qa_workflow.sh
  automated_qa_workflow.sh ──sources──► input_validation.sh, session_message_counter.sh, rollover_context_functions.sh
  automated_qa_workflow.sh ──invokes──► compute_uid_index.py, parse_checklist.py, UID_fail_item_match_fallback.py
```
