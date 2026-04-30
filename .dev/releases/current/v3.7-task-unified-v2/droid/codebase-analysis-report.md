# Codebase Context & Naming Analysis Report

> Generated for v3.7 Unified Release Spec  
> Sources: `CodeBaseContext.md`, `BrainStormQA.md`, and live codebase verification

---

## A. Naming/Identity Problem

The current state has **three naming layers** causing confusion:

| Layer | Name | File | Current State | Notes |
|-------|------|------|---------------|-------|
| 1. Legacy Command | `sc:task` | `.claude/commands/sc/task.md` | **Deprecated** (`deprecated: true`) | Frontmatter: `name: task-legacy`, `deprecated_by: "task-unified"`. Still present in repo. |
| 2. Unified Command | `sc:task-unified` | `src/superclaude/commands/task-unified.md` | **Active** — canonical command | Frontmatter says `name: task` but filename is `task-unified.md`. All CLI code references it as `/sc:task-unified`. |
| 3. Protocol Skill | `sc:task-unified-protocol` | `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | **Active** — invoked by command | Frontmatter: `name: sc:task-unified-protocol`. Only invoked for STANDARD/STRICT tiers. |

**Core Confusion**: The command's frontmatter declares `name: task` but all live code references it as `/sc:task-unified`. The user-facing invocation is `/sc:task`, but the internal wiring uses `/sc:task-unified`. This mismatch creates ambiguity about what "the canonical name" actually is.

**Verified in codebase**: All three files confirmed to exist at stated paths via Glob.

---

## B. Live Codebase References

### Python Source Files (verified via `grep -r "sc:task-unified" src/superclaude/ --include="*.py"`)

| File | Line(s) | Context |
|------|---------|---------|
| `src/superclaude/cli/sprint/process.py` | L124, L170 | `build_prompt()` docstring and prompt construction: `f"/sc:task-unified Execute all tasks in @{phase_file}"` |
| `src/superclaude/cli/cleanup_audit/prompts.py` | L26, L47, L69, L92, L116 | **5 prompt builders** — surface scan, deep analysis, duplication detection, consolidation, and validation prompts all prefix with `/sc:task-unified` |

**Total Python source files**: 2 files, 7 references

### Markdown Source Files (verified via `grep` in `src/superclaude/`)

| File | Reference Count | Context |
|------|----------------|---------|
| `src/superclaude/commands/task-unified.md` | Multiple | Command definition itself; invokes skill for STANDARD/STRICT |
| `src/superclaude/commands/task-mcp.md` | 1 (L375) | Cross-reference: "See `/sc:task-unified`" |
| `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | Multiple | Protocol skill definition |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 12+ | Heavily integrated — description, execution stages, patch delegation |
| `src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md` | 1 (L521) | Documents subprocess prompt pattern with `/sc:task-unified` framing |
| `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | 1 (L35) | Pipeline position chain ending at `sc:task-unified` |
| `src/superclaude/skills/sc-validate-tests-protocol/SKILL.md` | 1 (L438) | Version note: "Initial release for /sc:task-unified validation" |

**Total live source files in `src/superclaude/`**: 9 files (2 Python + 7 Markdown)

### Key Constraint: Live vs Historical

| Category | Count | Location |
|----------|-------|----------|
| Live source files (`src/superclaude/`) | ~25 (`.py` + `.md` with `sc:task` in any form) | `src/superclaude/` |
| Total repo matches for `sc:task` | **666 files** | Entire repo |
| Historical output (bulk of matches) | ~641 files | `.dev/releases/complete/`, `.dev/releases/archive/` |

**Implication**: Any rename/consolidation only needs to touch ~15-20 live source files. The hundreds of historical tasklist outputs in `.dev/releases/complete/` should NOT be modified — they are immutable records.

---

## C. Architecture Context

### Sprint Pipeline Flow

```
User invokes: superclaude sprint run
         │
         ▼
execute_sprint(config: SprintConfig)     [src/superclaude/cli/sprint/executor.py:1112]
         │
         ▼  (per phase)
ClaudeProcess(config, phase)             [src/superclaude/cli/sprint/process.py:88]
         │
         ├── __init__() wires hooks, calls build_prompt()
         │
         ▼
build_prompt() → str                     [src/superclaude/cli/sprint/process.py:123]
         │
         │  Returns: "/sc:task-unified Execute all tasks in @{phase_file}
         │            --compliance strict --strategy systematic\n..."
         │
         ▼
super().__init__(prompt=...) → ClaudeProcess (pipeline base)
         │
         ▼
Spawns: claude -p <prompt> --print --verbose
```

**Key architectural details**:
- `ClaudeProcess` in `sprint/process.py` extends `superclaude.cli.pipeline.process.ClaudeProcess` (the generic pipeline base)
- The sprint-specific class only defines `__init__` (hook wiring) and `build_prompt()`
- All subprocess lifecycle (start, wait, terminate) is inherited from the pipeline base
- The prompt always starts with `/sc:task-unified` — this is the entry point into the command/skill system from CLI

### Cleanup Audit Pipeline

The cleanup audit in `src/superclaude/cli/cleanup_audit/prompts.py` follows the same pattern:
- 5 prompt builder functions each prefix with `/sc:task-unified`
- Steps: surface scan → deep analysis → duplication detection → consolidation → validation

---

## D. Integration Points

### Cross-References Between Commands, Skills, and Protocols

```
sc:roadmap-protocol
  └── Pipeline Position: spec(s) → sc:roadmap → roadmap artifacts →
      (user triggers) → future tasklist command → (user triggers) → sc:task-unified

sc:tasklist-protocol
  ├── Description references /sc:task-unified compliance tier execution
  ├── Section 5.3: Compliance Tier uses /sc:task-unified classification algorithm
  ├── Stage 9: Patch Execution delegates to sc:task-unified via Skill tool
  ├── Stage gates reference sc:task-unified completion
  └── 12+ total mentions

sc:cli-portify-protocol
  └── refs/code-templates.md: Documents subprocess prompt pattern
      "implement build_prompt() that constructs the step's prompt with
       proper /sc:task-unified framing"

sc:validate-tests-protocol
  └── Version note: "Initial release for /sc:task-unified validation"

task-mcp.md (command)
  └── L375: "See /sc:task-unified for complete documentation"
```

### Dependency Direction

```
sc:task-unified (command)
  │  invokes (for STANDARD/STRICT)
  ▼
sc:task-unified-protocol (skill)
  │  referenced by
  ▼
sc:tasklist-protocol ── sc:cli-portify-protocol ── sc:roadmap-protocol
                                                    sc:validate-tests-protocol
```

---

## E. Tasklist Format

The current wave-based format (verified from `.dev/releases/` examples):

```markdown
### Task W{wave}-{seq}: {Title}
- **Type**: edit | create | delete | verify
- **Target file**: {relative path}
- **Section**: {description of target section within file}
- **Description**: {what to do}
- **Depends on**: {task IDs or "none"}
- **Acceptance criteria**: {verifiable conditions}
- **Risk**: Low | Medium | High. {brief justification}
- **Wave**: {wave number}
```

**Field definitions**:

| Field | Purpose |
|-------|---------|
| `W{wave}-{seq}` | Wave number + sequential ID within wave (e.g., W1-01, W2-03) |
| `Type` | Operation type: edit, create, delete, verify |
| `Target file` | Relative path to file being modified |
| `Section` | Specific location within the target file |
| `Description` | Detailed instruction for what to change |
| `Depends on` | Task IDs that must complete first, or "none" |
| `Acceptance criteria` | Verifiable conditions for completion |
| `Risk` | Impact assessment with brief justification |
| `Wave` | Execution group — tasks in the same wave can run in parallel |

**Wave semantics**: Tasks within a wave have no inter-dependencies and can execute in parallel. Cross-wave dependencies are explicit via `Depends on`.

---

## F. Key Constraint: ~15-20 Live Source Files vs 666 Total

| Metric | Value | Source |
|--------|-------|--------|
| Total files matching `sc:task` anywhere | 666 | `grep -r "sc:task" -l \| wc -l` on full repo |
| Live source files in `src/superclaude/` matching `sc:task` | 25 | `grep -r "sc:task" --include="*.py" --include="*.md" -l src/superclaude/ \| wc -l` |
| Files with `sc:task-unified` specifically (Python) | 2 | `cli/sprint/process.py`, `cli/cleanup_audit/prompts.py` |
| Files with `sc:task-unified` specifically (Markdown) | 7 | Commands + skills as listed in Section B |
| Historical output files (immutable) | ~641 | `.dev/releases/complete/`, `.dev/releases/archive/` |

**Operational constraint**: Any naming consolidation MUST NOT touch historical output in `.dev/releases/complete/`. These are immutable sprint artifacts. Only the ~9-25 live source files should be modified.

---

## G. Recommendations for Naming Consolidation in v3.7

### 1. Resolve the Name vs Filename Mismatch
**Problem**: `task-unified.md` has `name: task` in frontmatter.  
**Recommendation**: Decide the canonical name and align both:
- **Option A**: Rename file to `task.md`, keep `name: task`. All code changes from `/sc:task-unified` → `/sc:task`.
- **Option B**: Keep file as `task-unified.md`, change `name: task-unified`. Code stays as-is.
- **Preferred**: Option A — simplifies the user-facing surface, aligns with frontmatter intent.

### 2. Remove Legacy `.claude/commands/sc/task.md`
The deprecated legacy command should be physically removed (or moved to an archive), not just marked deprecated. Its continued presence confuses tooling that scans for command files.

### 3. Rename the Protocol Skill
If the command becomes simply `sc:task`, the protocol skill should align:
- Current: `sc:task-unified-protocol` → Proposed: `sc:task-protocol`
- Directory: `sc-task-unified-protocol/` → `sc-task-protocol/`

### 4. Update All Live References (Scoped Change)
Files requiring update (9 verified live source files):

**Python (2 files, 7 occurrences)**:
- `src/superclaude/cli/sprint/process.py` — L124 docstring, L170 prompt string
- `src/superclaude/cli/cleanup_audit/prompts.py` — L26, L47, L69, L92, L116

**Markdown (7 files)**:
- `src/superclaude/commands/task-unified.md` (rename + update Skill invocation)
- `src/superclaude/commands/task-mcp.md` (update cross-reference)
- `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` (rename directory + update name)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (12+ references)
- `src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md` (1 reference)
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` (1 reference)
- `src/superclaude/skills/sc-validate-tests-protocol/SKILL.md` (1 reference)

### 5. Post-Rename: Run `make sync-dev` and `make verify-sync`
After all `src/superclaude/` changes, sync to `.claude/` dev copies and verify alignment.

### 6. Do NOT Touch Historical Files
The 641+ files in `.dev/releases/complete/` and `.dev/releases/archive/` must remain untouched — they are immutable audit trails.
