# R02: sc:tasklist Skill Protocol Research

**Researcher**: r02
**Status**: Complete
**Date**: 2026-04-02
**Scope**: `.claude/skills/sc-tasklist-protocol/SKILL.md` + rules/ + templates/
**Track Goal**: Understand how `/sc:tasklist` generates tasklists so we can build a task file that generates tasklists from existing roadmaps without a `superclaude tasklist generate` CLI.

---

## 1. Skill Directory Contents

```
.claude/skills/sc-tasklist-protocol/
  SKILL.md                          # Full protocol (~1200 lines, v4.0)
  rules/tier-classification.md      # Read-only reference for tier classification
  rules/file-emission-rules.md      # Read-only reference for file emission
  templates/index-template.md       # Index file structure template
  templates/phase-template.md       # Phase file structure template
```

The `rules/` and `templates/` files are explicitly marked as "read-only reference extracted from SKILL.md [...] the skill uses its own inline copy." The SKILL.md is self-contained; the auxiliary files exist for human review only.

---

## 2. Inputs the Skill Expects

### Required Input
- **Roadmap text**: The full content of a roadmap file. This is the single mandatory input. The roadmap is treated as the "only source of truth."

### Optional Inputs
- **`--spec <spec-path>`**: A supplementary TDD (Technical Design Document). Triggers Section 4.1a extraction of component inventory, migration phases, testing strategy, observability, release criteria, and API surface.
- **`--prd-file <prd-path>`**: A supplementary PRD (Product Requirements Document). Triggers Section 4.1b extraction of user personas, user stories, success metrics, release strategy, stakeholder priorities, acceptance scenarios.
- **`--output <output-dir>`**: Explicit output directory. If omitted, TASKLIST_ROOT is auto-derived from roadmap content.

### Auto-Wiring from `.roadmap-state.json`
When `.roadmap-state.json` exists alongside the roadmap, TDD and PRD paths are auto-loaded from the state file. Explicit CLI flags always override auto-wired values.

### Input Validation (done by command file, not skill)
The command file (`/sc:tasklist`) validates before invoking the skill:
1. Roadmap file exists and is non-empty
2. Spec file exists (if provided)
3. Output parent directory exists (if provided)
4. TASKLIST_ROOT derivation succeeds (if --output not provided)

---

## 3. Output Produced

### File Count
Exactly **N+1 files** during generation (Stages 1-6), where N = number of phases. Stages 7-10 produce up to 2 additional validation artifacts.

### Directory Layout
```
TASKLIST_ROOT/
  tasklist-index.md           # Cross-phase metadata, registries, traceability
  phase-1-tasklist.md         # Phase 1 tasks + inline checkpoints
  phase-2-tasklist.md         # Phase 2 tasks + inline checkpoints
  ...
  phase-N-tasklist.md         # Phase N tasks + inline checkpoints
  artifacts/                  # Placeholder for deliverable artifacts
  evidence/                   # Placeholder for execution evidence
  checkpoints/                # Checkpoint report files
  validation/                 # ValidationReport.md + PatchChecklist.md (Stages 8-10)
  execution-log.md            # Template for runtime logging
  feedback-log.md             # Template for tier calibration feedback
```

### TASKLIST_ROOT Derivation (3-step priority)
1. If roadmap contains `.dev/releases/current/<segment>/` -> use that
2. Else if roadmap contains `v<digits>(.<digits>)+` -> use `.dev/releases/current/<version-token>/`
3. Else -> `.dev/releases/current/v0.0-unknown/`

### Naming Conventions
- Phase files: `phase-N-tasklist.md` (canonical Sprint CLI convention)
- Phase headings: `# Phase N -- <Name>` (level 1 heading, em-dash, name <= 50 chars)
- Task IDs: `T<PP>.<TT>` (zero-padded 2-digit phase, 2-digit task)
- Deliverable IDs: `D-####` (global appearance order)
- Roadmap Item IDs: `R-###` (appearance order)
- Checkpoint names: `CP-P<PP>-T<start>-T<end>.md` or `CP-P<PP>-END.md`

---

## 4. Relationship to `build_tasklist_generate_prompt`

The SKILL.md explicitly calls this out in Section 3.x:

> "Generation enrichment described in this section and Sections 4.4a/4.4b is a **skill-protocol behavior** invoked when `/sc:tasklist` generates tasks via inference. It is NOT triggered by the CLI `superclaude tasklist validate` command, which only performs fidelity validation with optional PRD/TDD supplementary checks. The CLI `validate` subcommand uses `build_tasklist_fidelity_prompt`; the skill protocol uses `build_tasklist_generate_prompt` (defined in `tasklist/prompts.py` for this purpose)."

**Key distinction**:
- `build_tasklist_generate_prompt` (in `src/superclaude/cli/tasklist/prompts.py`) is the **CLI prompt builder** that would be used if `superclaude tasklist generate` existed as a CLI command. It builds a system prompt for Claude API calls.
- The **skill protocol** (SKILL.md) is the **inference-time protocol** that Claude follows when `/sc:tasklist` is invoked via the Skill tool. It contains the full generation algorithm inline.
- The skill does NOT call `build_tasklist_generate_prompt` at runtime. The skill IS the generation logic. The CLI prompt function and the skill encode the same algorithm but for different execution contexts (API call vs. inference).

**Implication for our task**: Since there is no `superclaude tasklist generate` CLI command, tasklist generation today happens ONLY via the `/sc:tasklist` slash command, which invokes the skill via Claude Code inference. The `build_tasklist_generate_prompt` function exists in code but has no CLI subcommand wired to it.

---

## 5. How TDD/PRD Supplementary Files Are Handled

### TDD Handling (Section 4.1a, triggered by `--spec`)
1. Read the spec file
2. Detect TDD format (looks for `## 10. Component Inventory` heading, YAML frontmatter type, or 20+ numbered section headings)
3. Extract structured context: component_inventory, migration_phases, testing_strategy, observability, release_criteria, api_surface
4. Non-TDD format: log warning, continue roadmap-only
5. Missing file: abort with error

### PRD Handling (Section 4.1b, triggered by `--prd-file` or auto-wired)
1. Read the PRD file
2. Extract: user_personas, user_stories, success_metrics, release_strategy, stakeholder_priorities, acceptance_scenarios
3. Missing file: abort with error

### Enrichment Behavior
- **Without source documents**: Tasks derived from roadmap text only
- **With TDD**: Tasks enriched with exact function/class names, test case references, migration details, API specs, data model fields
- **With PRD**: Tasks enriched with persona context, acceptance criteria, metric instrumentation, priority ordering, scope boundaries
- **Precedence**: TDD for implementation specifics, PRD for product context

### Supplementary Task Generation
- Section 4.4a: TDD generates additional tasks (new/modified/deleted components, migration phases, test suites, observability, DoD verification)
- Section 4.4b: PRD enriches existing tasks (user stories merged with features, success metrics as validation steps, acceptance scenarios as tests)
- PRD does NOT generate standalone implementation tasks -- it enriches roadmap-derived tasks

---

## 6. How a Task Executor Would Invoke This

### Method 1: Via `/sc:tasklist` Slash Command (Current Production Path)
```
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>]
```
The command file validates inputs, derives TASKLIST_ROOT, then invokes:
```
Skill sc:tasklist-protocol
```
...passing roadmap text, spec text (if any), and output directory as context.

### Method 2: Via Skill Tool Directly
```python
# From a task file or agent, invoke the Skill tool:
Skill("sc-tasklist-protocol", args="<roadmap-path> --spec <spec-path> --output <output-dir>")
```
The skill is listed in the session's available skills and can be invoked programmatically.

### Method 3: Build a CLI Command (What We're Investigating)
Wire `build_tasklist_generate_prompt` to a new `superclaude tasklist generate` subcommand that:
1. Reads roadmap + optional spec/PRD files
2. Builds the system prompt via `build_tasklist_generate_prompt()`
3. Sends to Claude API
4. Writes output files to TASKLIST_ROOT

This is the gap identified -- the prompt function exists but has no CLI entry point.

---

## 7. Output Format Details

### tasklist-index.md Structure
1. `# TASKLIST INDEX -- <name>`
2. `## Metadata & Artifact Paths` (table with Sprint Name, Generator Version, dates, counts, complexity, personas)
3. `## Phase Files` (table: Phase | File | Phase Name | Task IDs | Tier Distribution)
4. `## Source Snapshot` (3-6 bullets from roadmap)
5. `## Deterministic Rules Applied` (8-12 bullets)
6. `## Roadmap Item Registry` (R-### | Phase Bucket | Original Text)
7. `## Deliverable Registry` (D-#### | Task ID | Roadmap Item IDs | Deliverable | Tier | Verification | Artifact Paths | Effort | Risk)
8. `## Traceability Matrix` (R-### -> T -> D -> Tier -> Confidence -> Artifact Paths)
9. `## Execution Log Template` (empty template)
10. `## Checkpoint Report Template` (template)
11. `## Feedback Collection Template` (template)
12. `## Glossary` (only if roadmap defines terms)
13. `## Generation Notes` (optional; fallback behaviors)

### phase-N-tasklist.md Structure
1. `# Phase N -- <Phase Name>` (level 1 heading, em-dash)
2. Phase goal paragraph (2-3 sentences)
3. Tasks in order, each with:
   - `### T<PP>.<TT> -- <Task Title>`
   - Metadata table (Roadmap Item IDs, Why, Effort, Risk, Risk Drivers, Tier, Confidence, Requires Confirmation, Critical Path Override, Verification Method, MCP Requirements, Fallback Allowed, Sub-Agent Delegation, Deliverable IDs)
   - Artifacts (Intended Paths)
   - Deliverables (1-5 items)
   - Steps (3-8, with [PLANNING]/[EXECUTION]/[VERIFICATION]/[COMPLETION] markers)
   - Acceptance Criteria (exactly 4 bullets)
   - Validation (exactly 2 bullets)
   - Dependencies
   - Rollback
   - Notes
4. Inline checkpoints every 5 tasks (`### Checkpoint: Phase <P> / Tasks <start>-<end>`)
5. Mandatory end-of-phase checkpoint (`### Checkpoint: End of Phase <N>`)

### Checklist Item Format (within tasks)
Steps use numbered imperative form with phase markers:
```
1. **[PLANNING]** Load context and identify scope
2. **[PLANNING]** Check dependencies and blockers
3. **[EXECUTION]** <implementation step>
4. **[EXECUTION]** <implementation step>
5. **[VERIFICATION]** Validation step aligned to tier
6. **[COMPLETION]** Documentation and evidence
```

---

## 8. Generation Algorithm (10-Stage Pipeline)

| Stage | Name | What Happens |
|-------|------|-------------|
| 1 | Input Ingest | Read roadmap, optional TDD/PRD files |
| 2 | Parse + Phase Bucketing | Split roadmap into items (R-###), assign to phase buckets |
| 3 | Task Conversion | Convert items to tasks (T<PP>.<TT>), split multi-deliverable items |
| 4 | Enrichment | Compute Effort, Risk, Tier, Confidence, MCP reqs, Sub-Agent delegation |
| 5 | File Emission | Write tasklist-index.md + phase-N-tasklist.md files |
| 6 | Self-Check | Sprint Compatibility + Semantic + Structural quality gates (17 checks) |
| 7 | Roadmap Validation | Spawn 2N parallel agents to detect drift/contradictions/omissions |
| 8 | Patch Plan Generation | Write ValidationReport.md + PatchChecklist.md (or clean report) |
| 9 | Patch Execution | Delegate to sc:task-unified for applying patches |
| 10 | Spot-Check Verification | Re-verify findings, append results to validation report |

---

## 9. Key Findings for Task Builder

1. **No CLI `generate` command exists.** Tasklist generation is inference-only via the skill protocol.
2. **`build_tasklist_generate_prompt` exists in code** but has no CLI subcommand wired to it.
3. **The skill protocol is self-contained** -- it does not call the Python prompt builder at runtime.
4. **A task executor can invoke via Skill tool** -- `Skill("sc-tasklist-protocol", args="...")`.
5. **The algorithm is deterministic** -- same input produces same output, no discretionary choices.
6. **Post-generation validation is mandatory** (Stages 7-10) and uses parallel sub-agents.
7. **Sprint CLI compatibility** is enforced via self-check: literal filenames in index, contiguous phase numbers, standard heading format.
8. **TDD/PRD enrichment is optional** but significantly improves task specificity when available.
