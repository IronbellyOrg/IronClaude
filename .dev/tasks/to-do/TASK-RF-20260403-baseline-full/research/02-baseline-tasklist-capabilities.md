# R2: Baseline Tasklist Capabilities (Master Branch)

**Status**: Complete
**Researcher**: r2 (Integration Points)
**Branch Examined**: master (commit 4e0c621)
**Date**: 2026-04-02

---

## 1. CLI Commands on Master

### 1.1 `superclaude tasklist validate` -- EXISTS

**File**: `src/superclaude/cli/tasklist/commands.py`

**Accepted flags**:

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `OUTPUT_DIR` | positional, Path | (required) | Directory where validation report is written |
| `--roadmap-file` | Path (must exist) | `{output_dir}/roadmap.md` | Path to the roadmap file |
| `--tasklist-dir` | Path (must exist) | `{output_dir}/` | Path to the tasklist directory |
| `--model` | string | `""` | Override model for validation steps |
| `--max-turns` | int | `100` | Max agent turns per claude subprocess |
| `--debug` | flag | `False` | Enable debug logging |

**Key finding**: There are NO `--tdd-file` or `--prd-file` flags on the baseline `tasklist validate`. The validator only compares roadmap-to-tasklist. It has no awareness of TDD or PRD documents.

### 1.2 `superclaude tasklist generate` -- DOES NOT EXIST

The `commands.py` file defines only a `tasklist_group` (Click group) and a single `validate` subcommand. There is no `generate` command. The word "generate" appears only in comments/docstrings, not as a Click command.

Tasklist generation is handled entirely by the `/sc:tasklist` Claude Code skill (see section 3 below), not by the CLI.

---

## 2. Tasklist Executor (`executor.py`)

### 2.1 What `tasklist validate` Does

1. **Collects inputs**: Reads the roadmap file + all `*.md` files from the tasklist directory (sorted for deterministic ordering)
2. **Builds prompt**: Calls `build_tasklist_fidelity_prompt(roadmap_file, tasklist_dir)` from `prompts.py`
3. **Embeds inline**: All input file contents are embedded directly into the prompt as fenced code blocks (the `--file` flag for Claude CLI is noted as broken -- "cloud download mechanism, not local file injector")
4. **Runs single step**: Executes one pipeline step `"tasklist-fidelity"` via `ClaudeProcess` subprocess
5. **Applies gate**: Uses `TASKLIST_FIDELITY_GATE` to validate the output
6. **Sanitizes output**: Strips conversational preamble before YAML frontmatter
7. **Checks severity**: Parses `high_severity_count` from frontmatter; returns `True` (pass) if 0, `False` (fail) otherwise

### 2.2 Pipeline Integration

The executor reuses the shared pipeline infrastructure:
- `execute_pipeline()` from `cli.pipeline.executor`
- `ClaudeProcess` from `cli.pipeline.process`
- `Step`, `StepResult`, `PipelineConfig` from `cli.pipeline.models`

### 2.3 Embed Size Warning

A warning is logged if the composed prompt exceeds 100KB (`_EMBED_SIZE_LIMIT`), but it proceeds regardless since the `--file` fallback is unavailable.

---

## 3. Tasklist Skill (`/sc:tasklist`)

### 3.1 Skill Structure on Master

```
.claude/skills/sc-tasklist-protocol/
  SKILL.md                                    # Main protocol (50KB+)
  rules/file-emission-rules.md               # File output rules
  rules/tier-classification.md               # Compliance tier rules
  templates/index-template.md                # tasklist-index.md template
  templates/phase-template.md                # phase-N-tasklist.md template
```

### 3.2 Skill Metadata

- **Name**: `sc:tasklist-protocol`
- **Description**: "Deterministic roadmap-to-tasklist generator with integrated roadmap validation, producing Sprint CLI-compatible multi-file bundles with /sc:task-unified compliance tier integration"
- **Complexity**: high
- **MCP servers**: sequential, context7
- **Personas**: analyzer, architect
- **Argument hint**: `<roadmap-path> [--spec <spec-path>] [--output <output-dir>]`

### 3.3 What the Skill Does (Generation)

The skill is an inference-based generator (runs inside Claude Code, not as a CLI subprocess). It:
1. Reads a roadmap file
2. Optionally reads a spec file for cross-reference
3. Transforms roadmap items into a multi-file tasklist bundle
4. Outputs: `tasklist-index.md` + one `phase-N-tasklist.md` per phase
5. Runs post-generation validation (mandatory)
6. Patches any drift before returning control

### 3.4 Worktree Compatibility

The `/sc:tasklist` skill is a Claude Code skill (`.claude/skills/`). It operates on files in the filesystem. Since a git worktree is just a separate filesystem checkout, the skill works in a worktree as long as:
- The Claude Code session is started from within the worktree directory
- The `.claude/skills/` directory is accessible (it reads from `~/.claude/skills/` after installation, or the repo-local `.claude/skills/` during development)

**Conclusion**: Worktree-compatible. No special handling needed.

---

## 4. Validation Prompt Analysis

### 4.1 Prompt Structure (`prompts.py`)

The `build_tasklist_fidelity_prompt()` function produces a pure-string prompt that instructs Claude to:

1. **Role**: "You are a tasklist fidelity analyst"
2. **Scope guard** (VALIDATION LAYERING GUARD): Validates ROADMAP-to-TASKLIST alignment ONLY. Explicitly excludes spec-to-tasklist comparison.
3. **Severity definitions**: HIGH / MEDIUM / LOW with concrete examples
4. **Comparison dimensions** (5 total):
   - Deliverable Coverage (D-NNNN IDs)
   - Signature Preservation (function/API signatures)
   - Traceability ID Validity (R-NNN, D-NNNN)
   - Dependency Chain Correctness
   - Acceptance Criteria Completeness
5. **Output format**: YAML frontmatter + deviation report

### 4.2 Fidelity Report Format (Expected Output)

The report MUST begin with YAML frontmatter containing:

```yaml
---
source_pair: roadmap-to-tasklist
upstream_file: <roadmap filename>
downstream_file: <tasklist directory path>
high_severity_count: <integer>
medium_severity_count: <integer>
low_severity_count: <integer>
total_deviations: <integer>
validation_complete: <boolean>
tasklist_ready: <boolean>  # true ONLY if high_severity_count=0 AND validation_complete=true
---
```

Followed by a `## Deviation Report` section with numbered entries (DEV-NNN) containing:
- Severity
- Deviation description
- Upstream Quote (from roadmap)
- Downstream Quote (from tasklist, or `[MISSING]`)
- Impact assessment
- Recommended Correction

Ends with `## Summary` of findings.

### 4.3 Output Format Block

The prompt appends a shared `_OUTPUT_FORMAT_BLOCK` (imported from `roadmap/prompts.py`) that enforces:
- Response MUST begin with YAML frontmatter
- No conversational preamble before `---`
- No "Here is..." or "Sure!" text before frontmatter

---

## 5. Gate Criteria (`gates.py`)

### 5.1 TASKLIST_FIDELITY_GATE

**Required frontmatter fields** (6):
- `high_severity_count`
- `medium_severity_count`
- `low_severity_count`
- `total_deviations`
- `validation_complete`
- `tasklist_ready`

**Minimum output lines**: 20

**Enforcement tier**: `STRICT`

**Semantic checks** (2):
1. `high_severity_count_zero` -- `high_severity_count` must be 0
2. `tasklist_ready_consistent` -- `tasklist_ready` must be consistent with severity counts and `validation_complete`

Both check functions are reused from `roadmap/gates.py`.

---

## 6. Model (`models.py`)

`TasklistValidateConfig` extends `PipelineConfig` with three fields:
- `output_dir: Path`
- `roadmap_file: Path`
- `tasklist_dir: Path`

No TDD/PRD/spec fields exist in the baseline config.

---

## 7. Summary of Baseline Limitations

| Capability | Status | Notes |
|-----------|--------|-------|
| `tasklist validate` CLI | EXISTS | roadmap-to-tasklist only |
| `tasklist generate` CLI | MISSING | Generation is skill-only |
| `--tdd-file` flag | MISSING | Not in baseline |
| `--prd-file` flag | MISSING | Not in baseline |
| `--spec-file` flag | MISSING | Not in CLI (skill has `--spec` arg hint) |
| Spec-to-tasklist validation | EXCLUDED | Explicitly out of scope per layering guard |
| TDD/PRD enrichment | NONE | No awareness of TDD/PRD documents |
| `/sc:tasklist` skill | EXISTS | Full generation + post-gen validation |
| Worktree support | WORKS | Standard filesystem access |
| Fidelity report | YAML frontmatter + deviation report | 6 required fields, 2 semantic checks |

---

## 8. Integration Points for Feature Branch

When adding TDD/PRD enrichment to the tasklist pipeline, the following integration points are relevant:

1. **`commands.py`**: Add `--tdd-file` and/or `--prd-file` options to the `validate` command
2. **`models.py`**: Add corresponding fields to `TasklistValidateConfig`
3. **`prompts.py`**: Extend `build_tasklist_fidelity_prompt()` to accept and reference TDD/PRD content
4. **`executor.py`**: Include TDD/PRD files in the `all_inputs` list for inline embedding
5. **`gates.py`**: Potentially add new semantic checks for TDD/PRD coverage
6. **Skill SKILL.md**: Update if the skill protocol needs to reference TDD/PRD documents
7. **Layering guard**: Must be carefully updated -- currently blocks spec-to-tasklist checks; enrichment may require relaxing or layering this guard
