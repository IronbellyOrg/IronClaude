# Roadmap CLI Tools — Release Guide

This guide covers the `superclaude roadmap` CLI tooling, including:
- what each component does,
- when to use it,
- how to run it,
- practical examples with all options,
- the 11-step adversarial pipeline architecture (with anti-instinct, spec-fidelity, and wiring verification),
- gate criteria and validation,
- convergence, remediation, and certification subsystems,
- and how it fits into the **spec → roadmap → tasklist → execution** workflow.

---

## 1) Release Summary (What is included)

### Core command surface
The `superclaude roadmap` command group provides 3 subcommands:
1. `run` — Execute the 11-step adversarial roadmap generation pipeline
2. `validate` — Validate pipeline outputs against 7 structural and semantic dimensions
3. `accept-spec-change` — Update stored spec hash after accepted deviation records

### Architecture overview
The roadmap CLI orchestrates an **adversarial dual-agent pipeline** that:
- Extracts requirements from a specification file
- Generates two independent roadmap variants via different agent personas
- Produces a structured diff analysis of divergences
- Facilitates a multi-round adversarial debate between variants
- Scores and selects a base variant
- Merges the best elements into a final roadmap
- Runs a deterministic anti-instinct audit (non-LLM) for obligation/contract/fingerprint coverage
- Generates a test strategy aligned to the merged roadmap
- Performs spec-fidelity analysis to detect deviations from the original spec
- Runs wiring verification in shadow/trailing mode

### Module structure
```
src/superclaude/cli/roadmap/
├── __init__.py               # Exports roadmap_group
├── commands.py               # Click CLI definition (run + validate + accept-spec-change)
├── models.py                 # AgentSpec, RoadmapConfig, ValidateConfig, Finding dataclasses
├── executor.py               # 11-step pipeline orchestration + auto-validate hook
├── gates.py                  # Gate criteria + semantic check functions (14 gates total)
├── prompts.py                # Pure prompt builder functions (NFR-004)
├── validate_executor.py      # Validation pipeline orchestration
├── validate_gates.py         # REFLECT_GATE + ADVERSARIAL_MERGE_GATE definitions
├── validate_prompts.py       # Reflect + adversarial-merge prompt builders
├── spec_patch.py             # Spec-hash reconciliation for accept-spec-change
├── convergence.py            # Persistent deviation registry + run-to-run fidelity memory
├── semantic_layer.py         # Semantic checking under prompt-size budgets
├── structural_checkers.py    # Deterministic structural mismatch detection
├── spec_parser.py            # Markdown/spec parsing for fidelity analysis
├── obligation_scanner.py     # Anti-instinct: obligation discharge detection
├── integration_contracts.py  # Anti-instinct: integration/wiring contract extraction
├── fingerprint.py            # Anti-instinct: code-level identifier coverage
├── spec_structural_audit.py  # Warning-only structural audit after extraction
├── remediate.py              # Remediation scope, filtering, tasklist generation
├── remediate_executor.py     # File-scoped remediation with rollback + patch guards
├── remediate_prompts.py      # Remediation prompt builders
├── remediate_parser.py       # Validation report → Finding parser
└── certify_prompts.py        # Certification prompt builder

src/superclaude/cli/audit/
└── wiring_gate.py            # WIRING_GATE definition + wiring report generation
```

### Shared pipeline dependency
The roadmap CLI builds on the shared `pipeline/` module:
- `pipeline/models.py` — Step, StepResult, StepStatus, GateCriteria, GateMode, PipelineConfig, Deliverable
- `pipeline/executor.py` — Generic step sequencer with retry, gates, parallel dispatch
- `pipeline/process.py` — ClaudeProcess subprocess management
- `pipeline/gates.py` — Gate evaluation logic
- `pipeline/deliverables.py` — Deliverable decomposition

### Key design decisions
- **Context isolation**: Each subprocess receives only its prompt and `--file` inputs. No `--continue`, `--session`, or `--resume` flags are passed (FR-003, FR-023)
- **Inline embedding**: Input files are embedded directly into prompts up to ~120KB (kernel `MAX_ARG_STRLEN` minus template overhead); larger inputs fall back to `--file` flags
- **Atomic writes**: State files and sanitized outputs use `tmp + os.replace()` for crash safety
- **Preamble sanitization**: Conversational text before YAML frontmatter is automatically stripped from step outputs
- **Pipeline diagnostics injection**: Executor-populated timing metadata is injected into extraction frontmatter post-subprocess (FR-033)
- **GateMode.TRAILING**: Wiring verification runs as a non-blocking trailing gate (shadow mode)
- **Non-LLM steps**: Anti-instinct audit is fully deterministic — no Claude subprocess required

---

## 2) Command Reference — When and How to Use

## `superclaude roadmap run`

### What it does
Loads a specification file, builds an 11-step adversarial pipeline, validates outputs through gate criteria at each step, and produces a final merged roadmap with test strategy, spec-fidelity report, and structural audits.

Pre-flight: creates the output directory if it doesn't exist.

### Use when
- You have a specification document (markdown) ready for roadmap generation.
- You want adversarial quality: two independent agent perspectives debated and merged.
- You want deterministic, gate-validated pipeline execution with resume capability.
- You want to plug into the downstream `spec → roadmap → tasklist → sprint` workflow.

### Syntax
```bash
superclaude roadmap run <SPEC_FILE> [options]
```

### Positional arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `SPEC_FILE` | Yes | Path to a specification markdown file. Must exist on disk. |

### Key options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--agents` | String | `opus:architect,haiku:architect` | Comma-separated agent specs in `model[:persona]` format. Controls which models/personas generate the two roadmap variants. |
| `--output` | Path | Parent dir of SPEC_FILE | Output directory for all pipeline artifacts. Created automatically if it doesn't exist. |
| `--depth` | Choice | `standard` | Debate round depth: `quick` (1 round), `standard` (2 rounds), `deep` (3 rounds). |
| `--resume` | Flag | Off | Skip steps whose outputs already pass their gates. Re-run from the first failing step. Detects stale spec files via SHA-256 hash comparison. |
| `--dry-run` | Flag | Off | Print step plan, gate criteria, and timeout budgets, then exit without launching any subprocesses. |
| `--model` | String | (empty) | Override model for all steps. When empty, per-agent models from `--agents` are used for generate steps; other steps use the default Claude model. |
| `--max-turns` | Integer | `100` | Maximum agent turns per Claude subprocess. Applies to every step. |
| `--debug` | Flag | Off | Enable debug-level logging to `<output_dir>/roadmap-debug.log`. |
| `--no-validate` | Flag | Off | Skip post-pipeline validation step. Does **not** skip the spec-fidelity step. |
| `--allow-regeneration` | Flag | Off | Allow patches that exceed the diff-size threshold (FR-9). Use with caution. |
| `--retrospective` | Path | None | Path to a retrospective file from a prior release cycle. Content is framed as advisory "areas to watch" in extraction. Missing file is not an error. |

### Agent spec format
The `--agents` flag accepts a comma-separated list of agent specifications:

```
model[:persona]
```

| Component | Required | Default | Examples |
|-----------|----------|---------|----------|
| `model` | Yes | — | `opus`, `sonnet`, `haiku`, `claude-sonnet-4-20250514` |
| `persona` | No | `architect` | `architect`, `security`, `qa`, `performance` |

The model value is passed directly to `claude --model` (no resolution needed — the Claude CLI accepts shorthand names natively).

**Parsing rules**:
- `"opus:architect"` → model=`opus`, persona=`architect`
- `"haiku"` → model=`haiku`, persona=`architect` (default persona)
- `"sonnet:security"` → model=`sonnet`, persona=`security`

The agent's ID (used in output filenames) is `{model}-{persona}`, e.g., `opus-architect`.

### Examples

```bash
# Basic execution with defaults (opus:architect + haiku:architect)
superclaude roadmap run spec.md

# Custom agent personas
superclaude roadmap run spec.md --agents sonnet:security,haiku:qa

# Deep debate with 3 rounds
superclaude roadmap run spec.md --depth deep

# Quick single-round debate for rapid iteration
superclaude roadmap run spec.md --depth quick

# Custom output directory
superclaude roadmap run spec.md --output .dev/releases/current/v2.20/

# Validate pipeline plan without execution
superclaude roadmap run spec.md --dry-run

# Resume from last failure point
superclaude roadmap run spec.md --resume

# Override model for all steps
superclaude roadmap run spec.md --model claude-sonnet-4-20250514

# Increase max turns for complex specs
superclaude roadmap run spec.md --max-turns 200

# Full debug logging
superclaude roadmap run spec.md --debug

# With retrospective from prior release
superclaude roadmap run spec.md --retrospective .dev/releases/v2.19/retrospective.md

# Allow regeneration for large patches
superclaude roadmap run spec.md --allow-regeneration

# Production-quality deep run with custom agents and output
superclaude roadmap run .dev/releases/current/v2.20/spec.md \
  --agents opus:architect,sonnet:security \
  --depth deep \
  --output .dev/releases/current/v2.20/ \
  --max-turns 150 \
  --debug
```

---

## `superclaude roadmap validate`

### What it does
Validates the outputs of a prior `roadmap run` across 7 structural and semantic dimensions. Reads `roadmap.md`, `test-strategy.md`, and `extraction.md` from a completed pipeline output directory, runs one or more agent reflections, and produces a `validate/validation-report.md` with severity-classified findings.

**Auto-invocation**: `roadmap run` automatically invokes validation after a successful pipeline (unless `--no-validate` is passed). You only need to call `validate` explicitly to re-run validation on a previously completed output directory, or to run with different agents/options.

### Use when
- Checking whether a generated `roadmap.md` is ready for tasklist generation.
- Re-running validation after manually editing roadmap artifacts.
- Running with different agents than the auto-invoked defaults.
- CI/CD gate: confirm no BLOCKING issues before proceeding to `/sc:tasklist`.

### Syntax
```bash
superclaude roadmap validate <OUTPUT_DIR> [options]
```

### Positional arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `OUTPUT_DIR` | Yes | Path to a directory produced by `roadmap run`. Must contain `roadmap.md`, `test-strategy.md`, and `extraction.md`. |

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--agents` | String | `opus:architect` | Comma-separated agent specs (`model[:persona]`). 1 agent = single-agent mode; N agents = parallel reflect + adversarial merge. |
| `--model` | String | `""` | Override model for all validation steps. |
| `--max-turns` | Integer | `100` | Max agent turns per Claude subprocess. |
| `--debug` | Flag | Off | Enable debug logging. |

### Exit behavior
Always exits 0 (NFR-006). Blocking issues are surfaced as yellow CLI warnings; the caller decides whether to treat them as hard failures.

### Examples

```bash
# Basic validation with default single agent (opus:architect)
superclaude roadmap validate ./output

# Dual-agent adversarial validation
superclaude roadmap validate ./output --agents opus:architect,haiku:qa

# Validate with a specific model override
superclaude roadmap validate ./output --model claude-sonnet-4-20250514

# Disable auto-validation during roadmap run, validate manually later
superclaude roadmap run spec.md --no-validate
superclaude roadmap validate ./output --agents sonnet:architect,haiku:security
```

---

## `superclaude roadmap accept-spec-change`

### What it does
Updates the stored `spec_hash` in `.roadmap-state.json` after an accepted deviation record (documentation sync, not a functional change). This allows `--resume` to proceed without triggering a full cascade re-run.

### Use when
- The spec file was edited to formalize an accepted deviation.
- You want `--resume` to continue from where it left off without re-running extraction.

### Syntax
```bash
superclaude roadmap accept-spec-change <OUTPUT_DIR>
```

### Requirements
- At least one `dev-*-accepted-deviation.md` file with `disposition: ACCEPTED` and `spec_update_required: true` must exist as evidence.
- `.roadmap-state.json` must exist in the output directory.
- **Exclusive write access**: do not run concurrent roadmap operations on the same output directory.

---

## 3) The 11-Step Adversarial Pipeline

The roadmap pipeline generates a high-quality roadmap through adversarial comparison, debate, and multi-layer fidelity verification. Each LLM step runs as a fresh, isolated Claude subprocess. Step 7 (anti-instinct) is fully deterministic (no LLM).

### Pipeline overview

```
Step 1: Extract ──────────────┐
                               │
               ┌───────────────┴───────────────┐
               │                               │
Step 2a: Generate (Agent A)         Step 2b: Generate (Agent B)   ← parallel
               │                               │
               └───────────────┬───────────────┘
                               │
Step 3: Diff ──────────────────┤
                               │
Step 4: Debate ────────────────┤
                               │
Step 5: Score ─────────────────┤
                               │
Step 6: Merge ─────────────────┤
                               │
Step 7: Anti-Instinct Audit ───┤  ← deterministic (no LLM)
                               │
Step 8: Test Strategy ─────────┤
                               │
Step 9: Spec Fidelity ─────────┤
                               │
Step 10: Wiring Verification ──┘  ← trailing gate (shadow mode)
```

### Step details

| Step | ID | Timeout | Gate Tier | Parallel | LLM | Description |
|------|----|---------|-----------|----------|-----|-------------|
| 1 | `extract` | 300s | STRICT | No | Yes | Extract requirements from the spec file into structured format with 13 YAML frontmatter fields |
| 2a | `generate-{agent_a.id}` | 900s | STRICT | Yes | Yes | Generate roadmap variant A with agent A's persona perspective |
| 2b | `generate-{agent_b.id}` | 900s | STRICT | Yes | Yes | Generate roadmap variant B with agent B's persona perspective |
| 3 | `diff` | 300s | STANDARD | No | Yes | Produce structured diff analysis identifying divergences and shared assumptions |
| 4 | `debate` | 600s | STRICT | No | Yes | Facilitate multi-round adversarial debate between variants |
| 5 | `score` | 300s | STANDARD | No | Yes | Score both variants and select a base for merging |
| 6 | `merge` | 600s | STRICT | No | Yes | Produce final merged roadmap from base variant + debate-resolved improvements |
| 7 | `anti-instinct` | 30s | STRICT | No | **No** | Deterministic audit: obligation discharge, integration contracts, fingerprint coverage |
| 8 | `test-strategy` | 300s | STRICT | No | Yes | Generate test strategy mapped to the merged roadmap |
| 9 | `spec-fidelity` | 600s | STRICT* | No | Yes | Detect deviations between original spec and merged roadmap |
| 10 | `wiring-verification` | 60s | TRAILING | No | Yes | Verify callable/module wiring in shadow mode (non-blocking) |

*Spec-fidelity gate is set to `None` when `convergence_enabled=True` (convergence engine manages it instead).

### Output artifacts

All artifacts are written to the output directory (default: parent of SPEC_FILE).

| Artifact | Source Step | Description |
|----------|------------|-------------|
| `extraction.md` | extract | Structured requirements extraction with YAML frontmatter |
| `roadmap-{agent_a.id}.md` | generate-A | Roadmap variant from agent A |
| `roadmap-{agent_b.id}.md` | generate-B | Roadmap variant from agent B |
| `diff-analysis.md` | diff | Structured comparison of both variants |
| `debate-transcript.md` | debate | Multi-round adversarial debate transcript |
| `base-selection.md` | score | Variant scoring and base selection rationale |
| `roadmap.md` | merge | Final merged roadmap (primary output) |
| `anti-instinct-audit.md` | anti-instinct | Deterministic coverage audit report |
| `test-strategy.md` | test-strategy | Test strategy for the merged roadmap |
| `spec-fidelity.md` | spec-fidelity | Spec deviation analysis with severity classification |
| `wiring-verification.md` | wiring-verification | Callable/module wiring audit (shadow mode) |
| `.roadmap-state.json` | executor | Pipeline state file for resume capability |

### Example artifact filenames (with default agents)

```
output_dir/
├── extraction.md
├── roadmap-opus-architect.md
├── roadmap-haiku-architect.md
├── diff-analysis.md
├── debate-transcript.md
├── base-selection.md
├── roadmap.md                    ← primary output
├── anti-instinct-audit.md
├── test-strategy.md
├── spec-fidelity.md
├── wiring-verification.md
├── .roadmap-state.json
├── extraction.err                ← stderr from each step
├── roadmap-opus-architect.err
├── roadmap-haiku-architect.err
├── diff-analysis.err
├── debate-transcript.err
├── base-selection.err
├── roadmap.err
├── anti-instinct-audit.err
├── test-strategy.err
├── spec-fidelity.err
└── wiring-verification.err
```

---

## 4) Gate Criteria and Validation

Every pipeline step has a gate that validates the output before proceeding. Gates check file existence, minimum line counts, required YAML frontmatter fields, and semantic correctness.

### Gate enforcement tiers

| Tier | Behavior |
|------|----------|
| **STRICT** | All checks must pass. Failure halts the pipeline after retry. |
| **STANDARD** | Frontmatter and line count checks. Failure halts after retry. |
| **TRAILING** | Non-blocking advisory gate. Failures are logged but do not halt the pipeline. |

### Gate modes

| Mode | Behavior |
|------|----------|
| **BLOCKING** (default) | Gate failure halts the pipeline. |
| **TRAILING** | Gate runs after the step but failures are advisory-only (used by wiring-verification). |

### Per-step gate criteria

#### Extract gate (STRICT)
- **Min lines**: 50
- **Required frontmatter** (13 fields):
  - `spec_source`, `generated`, `generator`
  - `functional_requirements`, `nonfunctional_requirements`, `total_requirements`
  - `complexity_score`, `complexity_class`
  - `domains_detected`, `risks_identified`, `dependencies_identified`
  - `success_criteria_count`, `extraction_mode`
- **Semantic checks**:
  - `complexity_class_valid` — Must be one of LOW, MEDIUM, HIGH
  - `extraction_mode_valid` — Must be `standard` or start with `chunked`

#### Generate gates A & B (STRICT)
- **Min lines**: 100
- **Required frontmatter**: `spec_source`, `complexity_score`, `primary_persona`
- **Semantic checks**:
  - `frontmatter_values_non_empty` — All YAML fields must have non-empty values
  - `has_actionable_content` — At least one numbered or bulleted list item

#### Diff gate (STANDARD)
- **Min lines**: 30
- **Required frontmatter**: `total_diff_points`, `shared_assumptions_count`

#### Debate gate (STRICT)
- **Min lines**: 50
- **Required frontmatter**: `convergence_score`, `rounds_completed`
- **Semantic checks**:
  - `convergence_score_valid` — Must parse as float in [0.0, 1.0]

#### Score gate (STANDARD)
- **Min lines**: 20
- **Required frontmatter**: `base_variant`, `variant_scores`

#### Merge gate (STRICT)
- **Min lines**: 150
- **Required frontmatter**: `spec_source`, `complexity_score`, `adversarial`
- **Semantic checks**:
  - `no_heading_gaps` — Heading levels increment by at most 1 (no H2 → H4 skip)
  - `cross_refs_resolve` — Internal cross-references resolve to existing headings (warning-only per OQ-001)
  - `no_duplicate_headings` — No duplicate H2 or H3 heading text

#### Anti-instinct gate (STRICT)
- **Min lines**: 10
- **Required frontmatter**: `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`
- **Semantic checks**:
  - `no_undischarged_obligations` — `undischarged_obligations` must equal 0
  - `integration_contracts_covered` — `uncovered_contracts` must equal 0
  - `fingerprint_coverage_check` — `fingerprint_coverage` must be >= 0.7

#### Test strategy gate (STRICT)
- **Min lines**: 40
- **Required frontmatter** (9 fields):
  - `spec_source`, `generated`, `generator`
  - `complexity_class`, `validation_philosophy`
  - `validation_milestones`, `work_milestones`
  - `interleave_ratio`, `major_issue_policy`
- **Semantic checks**:
  - `complexity_class_valid` — Must be one of LOW, MEDIUM, HIGH
  - `interleave_ratio_consistent` — Must match complexity_class: LOW→1:3, MEDIUM→1:2, HIGH→1:1
  - `milestone_counts_positive` — `validation_milestones` and `work_milestones` must be positive integers
  - `validation_philosophy_correct` — Must be exactly `continuous-parallel` (hyphenated)
  - `major_issue_policy_correct` — Must be exactly `stop-and-fix`

#### Spec fidelity gate (STRICT)
- **Min lines**: 20
- **Required frontmatter** (6 fields):
  - `high_severity_count`, `medium_severity_count`, `low_severity_count`
  - `total_deviations`, `validation_complete`, `tasklist_ready`
- **Semantic checks**:
  - `high_severity_count_zero` — `high_severity_count` must equal 0
  - `tasklist_ready_consistent` — `tasklist_ready=true` requires `high_severity_count=0` AND `validation_complete=true`

#### Wiring verification gate (STRICT, TRAILING mode)
- **Min lines**: 10
- **Required frontmatter** (16 fields):
  - `gate`, `target_dir`, `files_analyzed`, `rollout_mode`
  - `analysis_complete`, `unwired_callable_count`, `orphan_module_count`, `unwired_registry_count`
  - `critical_count`, `major_count`, `info_count`
  - `total_findings`, `blocking_findings`
  - `whitelist_entries_applied`, `files_skipped`, `audit_artifacts_used`
- **Semantic checks**:
  - `analysis_complete_true` — Must be true
  - `recognized_rollout_mode` — Must be `shadow`, `soft`, or `full`
  - `finding_counts_consistent` — `total_findings` must equal sum of unwired counts
  - `severity_summary_consistent` — `critical + major + info` must equal `total_findings`
  - `zero_blocking_findings_for_mode` — Mode-aware blocking enforcement

### Additional gate definitions (not in main pipeline but available)

These gates are defined in `gates.py` for use by convergence/remediation subsystems:

| Gate | Purpose |
|------|---------|
| `REMEDIATE_GATE` | Validates remediation tasklist: all actionable findings have FIXED or FAILED status |
| `CERTIFY_GATE` | Validates certification report: per-finding table present, `certified=true` |
| `DEVIATION_ANALYSIS_GATE` | Validates deviation analysis: no ambiguous deviations, routing IDs valid, counts reconciled |

### Retry behavior
Each step has `retry_limit=1` (2 total attempts) except:
- `anti-instinct` — `retry_limit=0` (deterministic, no retry needed)
- `wiring-verification` — `retry_limit=0` (trailing gate, no retry)

---

## 4b) The Validate Pipeline

### Overview

The validate pipeline is a lightweight post-generation quality gate. It reads three artifacts produced by `roadmap run` and produces a single `validation-report.md` file that classifies any structural or semantic issues found.

**Pipeline routing** depends on agent count:

```
Single agent (default):
  INPUT: roadmap.md + test-strategy.md + extraction.md
       │
  Step 1: reflect  ──────────────────────────────────────► validation-report.md

Multi-agent (N agents):
  INPUT: roadmap.md + test-strategy.md + extraction.md
       │
  ┌────┴─────────────────────────────┐
  Step 1a: reflect-{agent_a.id}    Step 1b: reflect-{agent_b.id}   ← parallel
  ├── reflect-opus-architect.md     └── reflect-haiku-qa.md
  └────┬─────────────────────────────┘
       │
  Step 2: adversarial-merge ───────────────────────────────► validation-report.md
```

### Validation dimensions (7 total)

Each finding is classified as **BLOCKING**, **WARNING**, or **INFO**.

#### BLOCKING dimensions (failure = roadmap not ready for tasklist generation)

| # | Dimension | What is checked |
|---|-----------|-----------------|
| 1 | **Schema** | YAML frontmatter fields present, non-empty, correctly typed |
| 2 | **Structure** | Milestone DAG acyclic, all refs resolve, no duplicate deliverable IDs, heading hierarchy valid (no H2→H4 gaps) |
| 3 | **Traceability** | Every deliverable traces to a requirement; every requirement traces to a deliverable |
| 4 | **Cross-file consistency** | `test-strategy.md` milestone refs match `roadmap.md` milestones exactly; no dangling refs in either direction |
| 5 | **Parseability** | Content is parseable into actionable items by `sc:tasklist`'s splitter via headings, bullets, and numbered lists |

#### WARNING dimensions (non-blocking)

| # | Dimension | What is checked |
|---|-----------|-----------------|
| 6 | **Interleave** | `interleave_ratio = unique_phases_with_deliverables / total_phases`; must be in [0.1, 1.0]; test activities must not be back-loaded |
| 7 | **Decomposition** | Compound deliverables that describe multiple distinct outputs joined by "and"/"or" (would need splitting by `sc:tasklist`) |

### Output artifacts

All artifacts are written to `<OUTPUT_DIR>/validate/`.

| Artifact | Mode | Description |
|----------|------|-------------|
| `validate/validation-report.md` | Both | Final validation report with YAML frontmatter and classified findings |
| `validate/reflect-{agent.id}.md` | Multi-agent only | Per-agent reflection report (one per agent) |

### Gate criteria

#### REFLECT_GATE (STRICT)
- **Min lines**: 20
- **Required frontmatter**: `blocking_issues_count`, `warnings_count`, `tasklist_ready`
- **Semantic checks**: `frontmatter_values_non_empty`

#### ADVERSARIAL_MERGE_GATE (STRICT, multi-agent only)
- **Min lines**: 30
- **Required frontmatter**: `blocking_issues_count`, `warnings_count`, `tasklist_ready`, `validation_mode`, `validation_agents`
- **Semantic checks**: `frontmatter_values_non_empty`, `agreement_table_present` (requires a markdown table with "agree"/"agreement" column header)

### Report frontmatter

```yaml
---
blocking_issues_count: 2       # integer — total BLOCKING findings
warnings_count: 1              # integer — total WARNING findings
tasklist_ready: false          # boolean — true only if blocking_issues_count == 0
# (multi-agent only)
validation_mode: adversarial
validation_agents: opus-architect, haiku-qa
---
```

### CLI output format

```
WARNING: 2 blocking issue(s) found        ← yellow, only if blocking > 0
Warnings: 1                               ← only if warning > 0
Info: 3                                   ← only if info > 0

[validate] Complete: 2 blocking, 1 warning, 3 info
```

### Auto-invocation from `roadmap run`

After a successful pipeline, `execute_roadmap()` automatically calls `_auto_invoke_validate()`. It:
- Inherits `--model`, `--max-turns`, `--debug` from the parent `roadmap run` invocation.
- Uses the first 2 agents from `--agents` for dual-agent rigor (or 1 agent if only 1 was specified).
- Saves validation status (`pass`/`fail`/`skipped`) to `.roadmap-state.json`.
- Prints `[roadmap] Auto-invoking validation...` before running.

To skip auto-validation:
```bash
superclaude roadmap run spec.md --no-validate
```
Note: `--no-validate` skips the post-pipeline validation subsystem only. It does **not** skip the spec-fidelity step (FR-010, AC-005).

### Degraded mode (multi-agent partial failure)

If some (but not all) reflect steps fail in multi-agent mode, the executor writes a degraded report with a `_write_degraded_report()` call, logging which agents passed and which failed. The adversarial-merge step is skipped and the degraded report becomes `validation-report.md`.

---

## 5) Behind the Scenes: What the Python Runtime Actually Executes

### 5.1 `superclaude roadmap run` call path

When you run:
```bash
superclaude roadmap run <SPEC_FILE> [flags]
```

the CLI flow is:
1. `commands.py::run()` parses Click options and positional argument.
2. `ctx.get_parameter_source()` detects whether `--agents` and `--depth` were explicitly provided (important for `--resume`).
3. `AgentSpec.parse()` parses each comma-separated agent spec string.
4. `RoadmapConfig` is constructed with resolved paths and options.
5. `executor.py::execute_roadmap()` is called.
6. `_build_steps()` constructs the 11-step pipeline (steps 2a+2b as a parallel group).
7. If `--dry-run`: `_dry_run_output()` prints the plan and returns.
8. If `--resume`: `_apply_resume()` skips steps with passing gates; omitted `--agents`/`--depth` restored from state.
9. `execute_pipeline()` (from `pipeline/executor.py`) runs the steps.
10. `_save_state()` writes `.roadmap-state.json` atomically.
11. On failure: `_format_halt_output()` prints diagnostics and exits with code 1.
12. On success (unless `--no-validate`): `_auto_invoke_validate()` runs the validation pipeline.
13. Validation status saved to `.roadmap-state.json`.

### 5.2 What command is run for each step

For each LLM step, the runtime spawns a fresh Claude CLI subprocess via `ClaudeProcess`:

```bash
claude \
  --print \
  --verbose \
  --dangerously-skip-permissions \
  --no-session-persistence \
  --max-turns <N> \
  --output-format text \
  -p "<generated prompt>" \
  [--model <model-if-provided>] \
  [--file <input-path> ...]     # only if embedded inputs exceed ~120KB
```

Important details:
- `--no-session-persistence` ensures step isolation (no context leakage between steps).
- `--output-format text` is used (vs `stream-json` for sprint) for gate-compatible plain text output.
- `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` environment variables are stripped from the child process to prevent nested session detection.
- stdout is redirected to the step's output file (e.g., `extraction.md`).
- stderr is redirected to a corresponding `.err` file (e.g., `extraction.err`).

For the `anti-instinct` step (non-LLM): no subprocess is spawned. The executor runs deterministic Python code (`obligation_scanner`, `integration_contracts`, `fingerprint`) directly and writes the audit report.

### 5.3 Input embedding strategy

Each step's input files are embedded directly into the prompt as fenced code blocks:

```markdown
# /path/to/extraction.md
\`\`\`
<file contents>
\`\`\`
```

This inline embedding is used when total embedded size is ≤ ~120KB (`_EMBED_SIZE_LIMIT = MAX_ARG_STRLEN - PROMPT_TEMPLATE_OVERHEAD`). For larger inputs, the executor falls back to `--file` flags passed as extra CLI arguments.

The embed size limit is derived from the Linux kernel's `MAX_ARG_STRLEN` (128KB) minus an 8KB safety margin for prompt template overhead.

### 5.4 Output sanitization

After each step's subprocess completes successfully, `_sanitize_output()` strips any conversational preamble before the first `---` YAML frontmatter delimiter. This handles cases where the LLM produces text like "Here is the output:" before the required frontmatter.

The sanitization is atomic: it writes to a `.tmp` file then uses `os.replace()` to prevent partial file states.

### 5.5 Pipeline diagnostics injection (FR-033)

For the `extract` step only, the executor injects `pipeline_diagnostics` into the YAML frontmatter after the subprocess completes. This includes:
- `elapsed_seconds` — wall-clock duration of the extraction step
- `started_at` — ISO-8601 start timestamp
- `finished_at` — ISO-8601 completion timestamp

The LLM cannot reliably produce execution timing, so the executor injects these fields deterministically.

### 5.6 Parallel execution (steps 2a + 2b)

The generate steps run concurrently via Python threading:
- Each step runs in a daemon thread with its own `ClaudeProcess`.
- A shared `threading.Event` provides cross-cancellation: if one step fails, the other is terminated.
- Both steps must PASS before the pipeline proceeds to the diff step.
- Gate checks run independently for each step after its subprocess completes.

### 5.7 State persistence

After pipeline execution (success or failure), `.roadmap-state.json` is written atomically:

```json
{
  "schema_version": 1,
  "spec_file": "/absolute/path/to/spec.md",
  "spec_hash": "<sha256 hex>",
  "agents": [
    {"model": "opus", "persona": "architect"},
    {"model": "haiku", "persona": "architect"}
  ],
  "depth": "standard",
  "last_run": "2026-03-08T12:00:00+00:00",
  "steps": {
    "extract": {
      "status": "PASS",
      "attempt": 1,
      "output_file": "/path/to/extraction.md",
      "started_at": "...",
      "completed_at": "..."
    }
  }
}
```

State also tracks:
- Validation status (`pass`/`fail`/`skipped`)
- Remediation metadata (when convergence is enabled)
- Certification metadata
- Restored agents/depth for resume logic

### 5.8 Resume behavior

When `--resume` is passed:
1. The executor reads `.roadmap-state.json` from the output directory.
2. If `--agents` or `--depth` were omitted from the command, their values are restored from the state file.
3. The spec file's SHA-256 hash is compared against `spec_hash` in the state file.
4. If the spec has changed, a warning is printed and the `extract` step is forced to re-run.
5. For each step in pipeline order, the gate is re-evaluated against the existing output file:
   - If the gate passes → step is skipped (logged as `[roadmap] Skipping <id> (gate passes)`).
   - If the gate fails → this step and all subsequent steps are re-run.
6. For parallel groups, all steps in the group must pass their gates to be skipped.
7. If all steps already pass: `[roadmap] All steps already pass gates. Nothing to do.`

### 5.9 Halt diagnostics

When a step fails after exhausting retries, the executor prints structured diagnostics:

```
ERROR: Roadmap pipeline halted at step 'debate' (attempt 2/2)
  Gate failure: convergence_score must be a float in [0.0, 1.0]
  Output file: /path/to/debate-transcript.md
  Output size: 1234 bytes (45 lines)
  Step timeout: 600s | Elapsed: 120s

Completed steps: extract (PASS, attempt 1), generate-opus-architect (PASS, attempt 1), ...
Failed step:     debate (FAIL, attempt 2)
Skipped steps:   score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification

To retry from this step:
  superclaude roadmap run /path/to/spec.md --resume

To inspect the failing output:
  cat /path/to/debate-transcript.md
```

---

## 6) Depth Modes: Debate Configuration

The `--depth` flag controls how many rounds of adversarial debate occur in step 4:

### `quick` (1 round)
Each perspective states its position on the key divergence points, then a convergence assessment is provided.

**Use when**: Rapid iteration, small specs, or when variants are expected to be similar.

### `standard` (2 rounds) — Default
- **Round 1**: Each perspective states initial positions on divergence points.
- **Round 2**: Each perspective rebuts the other's key claims.
- Then a convergence assessment is provided.

**Use when**: Most specifications. Provides good coverage without excessive token consumption.

### `deep` (3 rounds)
- **Round 1**: Each perspective states initial positions on divergence points.
- **Round 2**: Each perspective rebuts the other's key claims.
- **Round 3**: Final synthesis — each perspective identifies concessions and remaining disagreements.
- Then a convergence assessment is provided.

**Use when**: Critical specifications, security-sensitive projects, or when maximum deliberation quality is needed.

---

## 7) Data Models Reference

### AgentSpec
```python
@dataclass
class AgentSpec:
    model: str        # e.g., "opus", "sonnet", "haiku"
    persona: str      # e.g., "architect", "security", "qa"

    @classmethod
    def parse(cls, spec: str) -> AgentSpec:
        # "opus:architect" → AgentSpec("opus", "architect")
        # "haiku"          → AgentSpec("haiku", "architect")

    @property
    def id(self) -> str:
        # "opus-architect"
```

### Finding
```python
@dataclass
class Finding:
    id: str
    severity: str                         # BLOCKING, WARNING, INFO
    dimension: str                        # schema, structure, traceability, etc.
    description: str
    location: str
    evidence: str
    fix_guidance: str
    files_affected: list[str]
    status: str = "PENDING"               # PENDING|ACTIVE|FIXED|FAILED|SKIPPED
    agreement_category: str = ""          # BOTH_AGREE|ONLY_A|ONLY_B|CONFLICT
    deviation_class: str = "UNCLASSIFIED" # SLIP|INTENTIONAL|AMBIGUOUS|PRE_APPROVED
    source_layer: str = "structural"      # structural|semantic
    rule_id: str = ""                     # v3.05: checker rule reference
    spec_quote: str = ""                  # v3.05: evidence from spec
    roadmap_quote: str = ""               # v3.05: evidence from roadmap
    stable_id: str = ""                   # v3.05: convergence-stable identifier
```

### RoadmapConfig (extends PipelineConfig)

```python
@dataclass
class RoadmapConfig(PipelineConfig):
    spec_file: Path                    # Resolved spec file path
    agents: list[AgentSpec]            # Default: [opus:architect, haiku:architect]
    depth: "quick"|"standard"|"deep"   # Default: "standard"
    output_dir: Path                   # Resolved output directory
    retrospective_file: Path | None    # Optional retrospective from prior release
    convergence_enabled: bool          # Default: False (v3.05 deterministic fidelity)
    allow_regeneration: bool           # Default: False (FR-9 diff-size override)

# Inherited from PipelineConfig:
    work_dir: Path          # Default: Path(".")
    dry_run: bool           # Default: False
    max_turns: int          # Default: 100
    model: str              # Default: "" (use per-agent models)
    permission_flag: str    # Default: "--dangerously-skip-permissions"
    debug: bool             # Default: False
    grace_period: int       # Default: 0
```

### ValidateConfig (extends PipelineConfig)

```python
@dataclass
class ValidateConfig(PipelineConfig):
    output_dir: Path          # Directory containing roadmap run outputs
    agents: list[AgentSpec]   # Default: [opus:architect, haiku:architect]

# Inherited from PipelineConfig:
    work_dir: Path          # Default: Path(".")
    max_turns: int          # Default: 100
    model: str              # Default: "" (use per-agent models)
    debug: bool             # Default: False
```

### GateCriteria

```python
@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str]   # YAML fields that must exist
    min_lines: int                            # Minimum output file lines
    enforcement_tier: "STRICT"|"STANDARD"|"LIGHT"|"EXEMPT"
    semantic_checks: list[SemanticCheck]       # Python-level content checks
```

### SemanticCheck

```python
@dataclass
class SemanticCheck:
    name: str                          # Check identifier
    check_fn: Callable[[str], bool]    # Pure function: content → pass/fail
    failure_message: str               # Human-readable failure reason
```

### GateMode

```python
class GateMode(Enum):
    BLOCKING = "blocking"    # Gate failure halts pipeline
    TRAILING = "trailing"    # Gate runs but failures are advisory-only
```

---

## 8) Anti-Instinct Audit (Step 7)

The anti-instinct step is unique: it is **fully deterministic** (no LLM subprocess). It runs three Python-based coverage analyses against the spec and merged roadmap:

### Obligation Scanner (`obligation_scanner.py`)
Scans roadmap content for scaffold/setup obligations (e.g., "set up X", "configure Y") and checks whether they are discharged (fulfilled) in later phases.

**Gate requirement**: `undischarged_obligations == 0`

### Integration Contracts (`integration_contracts.py`)
Extracts integration/wiring contracts from the spec (e.g., "module A calls module B") and checks whether the roadmap includes explicit wiring tasks for each contract.

**Gate requirement**: `uncovered_contracts == 0`

### Fingerprint Coverage (`fingerprint.py`)
Extracts code-level identifiers (function names, class names, variable names) from the spec and checks what fraction appear in the roadmap.

**Gate requirement**: `fingerprint_coverage >= 0.7`

### Output: `anti-instinct-audit.md`
```yaml
---
undischarged_obligations: 0
uncovered_contracts: 0
fingerprint_coverage: 0.85
---
```

---

## 9) Convergence and Fidelity Subsystems

These subsystems support run-to-run fidelity tracking and are activated when `convergence_enabled=True`.

### Deviation Registry (`convergence.py`)
Persistent storage for fidelity findings across pipeline runs:
- Stable IDs for cross-run finding identity
- Structural vs semantic HIGH tracking
- Run metadata and convergence budgeting
- `DeviationRegistry.load_or_create()` / `.save()` for persistence

### Structural Checkers (`structural_checkers.py`)
Deterministic mismatch detection across 5 categories:
- `check_signatures()` — Function/method signatures
- `check_data_models()` — Data structures and schemas
- `check_gates()` — Gate definitions and criteria
- `check_cli()` — CLI command surfaces
- `check_nfrs()` — Non-functional requirements

### Semantic Layer (`semantic_layer.py`)
Prompt-budgeted semantic checking:
- Adversarial debate over severity decisions
- Rubric-based scoring of arguments
- Strict prompt-size budget enforcement

### Spec Parser (`spec_parser.py`)
Rich markdown parsing for structured fidelity analysis:
- `ParseResult` with sections, tables, code blocks, function signatures, threshold expressions
- `parse_document()` entry point

---

## 10) Remediation and Certification Subsystems

These are not exposed as top-level CLI subcommands but are used internally by the convergence engine and can be invoked programmatically.

### Remediation (`remediate.py` + `remediate_executor.py`)
- **Scope**: Only editable files: `roadmap.md`, `extraction.md`, `test-strategy.md`
- **Workflow**: snapshot → apply patches → verify → rollback on failure
- **Guards**: Patch size limits, allowlist enforcement
- **Parser**: `remediate_parser.py` extracts `Finding` objects from validation reports

### Certification (`certify_prompts.py`)
- Builds prompts for post-remediation certification
- Gate requires per-finding results table and `certified=true`

---

## 11) End-to-End Workflow: Spec → Roadmap → Tasklist → Execution

The roadmap CLI is Stage B in the full release pipeline.

### Stage A: Spec (requirements source)
Create a specification markdown file with project requirements, constraints, and acceptance criteria.

### Stage B: Roadmap (adversarial generation) ← **This tool**
```bash
superclaude roadmap run spec.md --depth standard
```
Produces `roadmap.md` (merged, adversarially validated) + `test-strategy.md` + `spec-fidelity.md` + `anti-instinct-audit.md`.
Automatically invokes validation on success (unless `--no-validate`).

### Stage B2: Validate (quality gate) ← **This tool**
```bash
# Automatic after roadmap run (unless --no-validate)
# To re-run manually:
superclaude roadmap validate ./output --agents opus:architect,haiku:qa
```
Produces `validate/validation-report.md`. Check `tasklist_ready: true` before proceeding.

### Stage B3: Accept spec changes (optional) ← **This tool**
```bash
# After formalizing an accepted deviation in the spec:
superclaude roadmap accept-spec-change ./output
```

### Stage C: Tasklist (execution plan)
```bash
# Use /sc:tasklist to generate Sprint CLI-compatible phase files from the roadmap
```
Produces `tasklist-index.md` + phase files.

### Stage D: Sprint execution
```bash
superclaude sprint run .dev/releases/current/tasklist-index.md
```
Executes the phases with supervised Claude sessions.

### Stage E: Resume on halt
```bash
# Roadmap level
superclaude roadmap run spec.md --resume

# Sprint level
superclaude sprint run .dev/releases/current/tasklist-index.md --start <halt_phase>
```

---

## 12) Prompt Architecture

Each pipeline step uses a specialized prompt builder (defined in `prompts.py`). All prompt functions are **pure** — they accept concrete values, return strings, and perform no I/O (NFR-004).

### Common output format block
All prompts include a critical output format instruction:
```
CRITICAL: Your response MUST begin with YAML frontmatter (--- delimited block).
Do NOT include any text, preamble, or commentary before the opening ---.
```
This ensures gate validation can parse the output correctly.

### Prompt builders

| Builder | Step | Role instruction | Key output requirements |
|---------|------|-----------------|------------------------|
| `build_extract_prompt` | extract | "Requirements extraction specialist" | 13 frontmatter fields + 8 body sections |
| `build_generate_prompt` | generate | "{persona} specialist creating a project roadmap" | 3 frontmatter fields + 6 roadmap sections |
| `build_diff_prompt` | diff | "Comparative analysis specialist" | 2 frontmatter fields + 4 analysis sections |
| `build_debate_prompt` | debate | "Structured debate facilitator" | 2 frontmatter fields + debate transcript |
| `build_score_prompt` | score | "Objective evaluation specialist" | 2 frontmatter fields + scoring analysis |
| `build_merge_prompt` | merge | "Synthesis specialist" | 3 frontmatter fields + complete roadmap |
| `build_test_strategy_prompt` | test-strategy | "Test strategy specialist" | 9 frontmatter fields + test plan |
| `build_spec_fidelity_prompt` | spec-fidelity | Spec deviation analyst | 6 frontmatter fields + deviation details |
| `build_wiring_verification_prompt` | wiring-verification | Wiring auditor | 16 frontmatter fields + findings |
| `build_certification_prompt` | certify (convergence) | Certification specialist | 5 frontmatter fields + results table |

---

## 13) Error Handling and Process Management

### Process lifecycle
Each step uses `ClaudeProcess` from the shared pipeline module:
- Subprocess is launched with `subprocess.Popen` and process group isolation (`os.setpgrp` on Unix).
- The executor polls for cancellation every 1 second while the subprocess runs.
- Timeout detection: `exit_code == 124` maps to `StepStatus.TIMEOUT`.
- Non-zero exit (except 124): maps to `StepStatus.FAIL`.
- Success: maps to `StepStatus.PASS` (gate check runs next).

### Cancellation
- External cancellation is supported via a `cancel_check` callback.
- For parallel steps, cross-cancellation ensures if one step fails, the other is terminated.

### Graceful shutdown
`ClaudeProcess.terminate()` follows an escalation path:
1. SIGTERM to process group (or process on non-Unix)
2. Wait 10 seconds
3. SIGKILL if still alive
4. Wait 5 seconds for final cleanup

### Non-Unix portability
- Process group operations (`os.setpgrp`, `os.killpg`) are guarded with `hasattr()` checks.
- Fallback uses `process.terminate()` / `process.kill()` on non-Unix environments.

---

## 14) Integration with Slash Commands and Skills

The roadmap CLI has two integration surfaces:

### Python CLI (this tool)
```bash
superclaude roadmap run spec.md [options]
```
Deterministic, programmatic pipeline execution with subprocess orchestration.

### Slash command `/sc:roadmap`
The `/sc:roadmap` slash command (defined in `src/superclaude/commands/roadmap.md`) invokes the `sc-roadmap-protocol` skill for inference-based roadmap generation within a Claude Code session. This is the interactive counterpart to the CLI tool.

**Key differences**:
| Aspect | CLI (`superclaude roadmap run`) | Slash command (`/sc:roadmap`) |
|--------|------|------|
| Execution | Subprocess-per-step, automated | Single Claude session, interactive |
| Gate validation | Automated, Python-based | Inference-based within session |
| Resume | `--resume` flag with state file | Session persistence |
| Best for | CI/CD, unattended runs, reproducibility | Interactive exploration, quick iteration |

---

## 15) Practical Use Cases

### Use case 1: Standard roadmap generation
```bash
superclaude roadmap run .dev/releases/current/v2.20/spec.md
```
Runs the full 11-step pipeline with default agents (`opus:architect` + `haiku:architect`) and standard depth (2 debate rounds). Artifacts written to the spec's parent directory.

### Use case 2: Security-focused roadmap
```bash
superclaude roadmap run spec.md --agents opus:architect,sonnet:security --depth deep
```
Uses a security persona for the second variant. Deep debate ensures thorough adversarial review of security concerns.

### Use case 3: Quick iteration roadmap
```bash
superclaude roadmap run spec.md --agents haiku:architect,haiku:qa --depth quick
```
Uses faster (cheaper) models with a single debate round for rapid prototype roadmaps.

### Use case 4: Validate pipeline plan before execution
```bash
superclaude roadmap run spec.md --dry-run
```
Prints the step plan with gate criteria and timeout budgets. No subprocesses are launched. Use this to verify configuration before committing to a full run.

### Use case 5: Resume after failure
```bash
superclaude roadmap run spec.md --resume
```
Skips steps whose outputs already pass their gates. Re-runs from the first failing step. Detects spec changes and forces re-extraction if the spec has been modified.

### Use case 6: Custom output directory for release management
```bash
superclaude roadmap run spec.md --output .dev/releases/current/v2.20-feature/
```
All artifacts are written to the specified directory, keeping releases organized.

### Use case 7: Override model globally
```bash
superclaude roadmap run spec.md --model claude-sonnet-4-20250514
```
Forces all steps (not just generate steps) to use the specified model. Useful for testing with a specific model version.

### Use case 8: Debug a failing pipeline
```bash
superclaude roadmap run spec.md --debug --max-turns 200
```
Enables debug logging to `<output_dir>/roadmap-debug.log` and increases max turns for steps that might need more interaction. Inspect `.err` files for subprocess stderr output.

### Use case 9: With retrospective context
```bash
superclaude roadmap run spec.md --retrospective .dev/releases/v2.19/retrospective.md
```
Feeds prior release lessons into extraction as advisory "areas to watch".

### Use case 10: Accept spec deviation and resume
```bash
# After editing spec to formalize an accepted deviation:
superclaude roadmap accept-spec-change ./output
superclaude roadmap run spec.md --resume
```

---

## 16) Quick Command Cheat Sheet

```bash
# --- roadmap run ---

# Basic roadmap generation
superclaude roadmap run spec.md

# Custom agents
superclaude roadmap run spec.md --agents sonnet:security,haiku:qa

# Deep debate (3 rounds)
superclaude roadmap run spec.md --depth deep

# Quick debate (1 round)
superclaude roadmap run spec.md --depth quick

# Custom output directory
superclaude roadmap run spec.md --output .dev/releases/current/v2.20/

# Dry-run (plan only)
superclaude roadmap run spec.md --dry-run

# Resume from failure
superclaude roadmap run spec.md --resume

# Override model globally
superclaude roadmap run spec.md --model claude-sonnet-4-20250514

# Increase max turns
superclaude roadmap run spec.md --max-turns 200

# Debug mode
superclaude roadmap run spec.md --debug

# With retrospective context
superclaude roadmap run spec.md --retrospective prior-retro.md

# Allow large-diff regeneration
superclaude roadmap run spec.md --allow-regeneration

# Full production run
superclaude roadmap run spec.md \
  --agents opus:architect,sonnet:security \
  --depth deep \
  --output .dev/releases/current/v2.20/ \
  --retrospective .dev/releases/v2.19/retrospective.md \
  --max-turns 150 \
  --debug

# --- roadmap validate ---

# Basic validation (single-agent, default opus:architect)
superclaude roadmap validate ./output

# Dual-agent adversarial validation
superclaude roadmap validate ./output --agents opus:architect,haiku:qa

# Skip auto-validation during run, validate manually later
superclaude roadmap run spec.md --no-validate
superclaude roadmap validate ./output --agents sonnet:architect,haiku:security

# Validate with model override
superclaude roadmap validate ./output --model claude-sonnet-4-20250514

# --- roadmap accept-spec-change ---

# Accept spec deviation and update hash
superclaude roadmap accept-spec-change ./output
```

---

## 17) Troubleshooting Checklist

### Before running
- [ ] Spec file exists and is readable markdown
- [ ] Output directory is writable (or will be created)
- [ ] `claude` binary is in `PATH`
- [ ] Agent model names are valid (opus, sonnet, haiku, or full model IDs)

### After a failure
- [ ] Check the halt diagnostic output for the failing step and gate reason
- [ ] Inspect the `.err` file for the failing step (subprocess stderr)
- [ ] Inspect the output file — is the YAML frontmatter present and correct?
- [ ] Check if preamble stripping failed (conversational text before `---`)
- [ ] For gate failures: verify required frontmatter fields and minimum line counts
- [ ] For semantic check failures: review the specific check (e.g., heading gaps, empty values)
- [ ] Use `--resume` to retry from the failing step without re-running passed steps
- [ ] Use `--debug` for detailed executor logging

### Common issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Step 'extract' exited with code 1` | Claude CLI error or missing permissions | Check `.err` file; verify `claude` works standalone |
| `frontmatter_values_non_empty` failure | LLM produced empty YAML field values | Re-run step (retry usually fixes) |
| `convergence_score must be a float in [0.0, 1.0]` | LLM output invalid score format | Re-run; consider `--depth quick` if consistently failing |
| `Heading level gap detected` | Merge produced H2→H4 jump | Re-run merge step; check variant heading structure |
| `spec-file has changed since last run` (with `--resume`) | Spec was edited after previous run | Expected behavior — extract is forced to re-run |
| All steps skipped with `--resume` | All outputs already pass gates | Pipeline already complete; inspect `roadmap.md` |
| `Required validation input not found: …/roadmap.md` | Validate called on dir without a completed run | Run `superclaude roadmap run` first; all 3 inputs required |
| `agreement_table_present` failure (multi-agent) | Adversarial merge missing agreement/disagreement table | Re-run; if persistent, switch to single-agent with `--agents opus:architect` |
| `tasklist_ready: false` in validation report | BLOCKING issues found during validation | Inspect `validate/validation-report.md` findings and fix the roadmap, then re-validate |
| Validation skipped with `[validate] Skipped:` | Auto-validate called before `roadmap.md` was written | Run `superclaude roadmap validate <output_dir>` manually |
| `undischarged_obligations must be 0` | Anti-instinct found setup tasks without discharge | Review roadmap for missing wiring/integration tasks |
| `fingerprint_coverage must be >= 0.7` | Spec code identifiers underrepresented in roadmap | Roadmap needs more explicit references to spec-defined symbols |
| `high_severity_count must be 0` | Spec-fidelity found HIGH deviations | Review `spec-fidelity.md` and fix roadmap or accept deviation |
| `interleave_ratio must match complexity_class` | Test strategy ratio mismatches complexity | Re-run test-strategy step |

---

## 18) Notes for Pipeline Operators

- The roadmap CLI covers three layers: **generation** (`roadmap run` → 11-step pipeline), **validation** (`roadmap validate` → quality gate), and **spec-change acceptance** (`roadmap accept-spec-change` → resume enablement). All feed into the **tasklist** layer (`/sc:tasklist`) and then the **execution** layer (`superclaude sprint run`).
- Validation runs automatically after `roadmap run` unless `--no-validate` is passed. Check `tasklist_ready: true` in `validate/validation-report.md` before invoking `/sc:tasklist`.
- For CI/CD pipelines: use `--no-validate` during `roadmap run` to control timing, then call `roadmap validate` as a separate gate step and parse `blocking_issues_count` from the report frontmatter.
- Single-agent validation (`--agents opus:architect`) is faster and cheaper. Dual-agent (`--agents opus:architect,haiku:qa`) produces an adversarial merge with an agreement table for richer analysis.
- Use `--dry-run` as an automated gate between spec authoring and pipeline execution.
- Use `--resume` for efficient iteration: edit spec → re-run → only changed steps execute.
- The `.roadmap-state.json` file is the source of truth for resume decisions. Delete it to force a full re-run.
- Agent persona choice significantly affects roadmap quality. Pair complementary personas (e.g., `architect` + `security`, `architect` + `qa`) for maximum adversarial value.
- Deep debate mode produces higher quality but costs ~3x more tokens than quick mode.
- All outputs use YAML frontmatter for machine parseability. Downstream tools (tasklist generator) rely on this structure.
- The anti-instinct step (step 7) runs in <1 second and costs zero tokens — it's a free structural safety net.
- Wiring verification runs in `shadow` mode by default (trailing gate) — it logs findings but does not block the pipeline. This allows gradual rollout before switching to `soft` or `full` enforcement.
- The `--retrospective` flag improves extraction quality by framing prior release lessons as advisory context. Use it when iterating across releases.
- The convergence engine (`convergence_enabled`) is an advanced feature for multi-run fidelity tracking. When enabled, the spec-fidelity gate is managed by the deviation registry instead of the standard gate.
