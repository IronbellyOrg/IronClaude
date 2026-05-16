# Domain Analysis: Naming/Identity Consolidation and Codebase Context

**Date:** 2026-04-02
**Analyst:** rf-analyst (Opus 4.6)
**Source files:** BrainStormQA.md, CodeBaseContext.md (v3.7-task-unified-v2 backlog)
**Scope:** Naming confusion across the task command surface, codebase integration map, and resolution recommendations

---

## 1. Executive Summary

The task execution subsystem suffers from a three-layer naming collision where the user-facing command `/sc:task`, the command file `task-unified.md`, and the skill `sc:task-unified-protocol` each use different names for the same conceptual unit. The legacy command file `.claude/commands/sc/task.md` compounds this by still existing with `deprecated: true`, creating a fourth artifact sharing the "task" name. This naming confusion has downstream consequences: the Sprint CLI hardcodes `/sc:task-unified` in subprocess prompts (process.py:170), the cleanup_audit pipeline does the same across 5 prompt builders, and at least 12 cross-references in sc:tasklist-protocol use `sc:task-unified` as the canonical execution target. Any rename that touches the command surface must propagate through all of these integration points or the sprint pipeline will emit incorrect prompts to subprocess calls.

---

## 2. Naming Layers Analysis

### Layer 1: Legacy command -- `.claude/commands/sc/task.md`

- **Frontmatter name:** `task-legacy`
- **Frontmatter flags:** `deprecated: true`, `deprecated_by: "task-unified"`
- **User-facing trigger:** `/sc:task` (via filename `task.md`)
- **Status:** Deprecated but physically present. Claude Code resolves commands by filename, so this file would match `/sc:task` unless the runtime deprioritizes deprecated commands.
- **Risk:** If Claude Code loads `task.md` before `task-unified.md` for a `/sc:task` invocation, the user gets the deprecated flow. The deprecation notice in the file body tells the user to migrate, but the command already executed with the legacy definition.

### Layer 2: Unified command -- `src/superclaude/commands/task-unified.md`

- **Frontmatter name:** `task` (not `task-unified`)
- **Filename:** `task-unified.md`
- **User-facing trigger:** `/sc:task-unified` or `/sc:task` (depending on which the runtime resolves)
- **Skill invocation:** Line 100 -- `Skill sc:task-unified-protocol` for STANDARD/STRICT tiers
- **Key observation:** The frontmatter `name: task` conflicts with the filename `task-unified.md`. The CLI sprint process (process.py:170) uses the string `/sc:task-unified` explicitly, meaning it depends on the filename, not the frontmatter name.

### Layer 3: Protocol skill -- `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`

- **Frontmatter name:** `sc:task-unified-protocol`
- **Directory name:** `sc-task-unified-protocol/`
- **Purpose:** Execution engine for STANDARD and STRICT tiers. Does NOT re-classify -- the note at line 7 explicitly says "Classification has already been performed by the `/sc:task` command."
- **Internal references:** Uses `/sc:task-unified` as its own heading (line 11), and `/sc:task` in usage examples (lines 40-44).

### The Confusion Matrix

| Artifact | Frontmatter name | Filename/dirname | User-facing string | Who calls it |
|----------|-----------------|------------------|-------------------|-------------|
| Legacy command | `task-legacy` | `task.md` | `/sc:task` | User (deprecated) |
| Unified command | `task` | `task-unified.md` | `/sc:task` or `/sc:task-unified` | User, Sprint CLI |
| Protocol skill | `sc:task-unified-protocol` | `sc-task-unified-protocol/` | N/A (internal) | Unified command (Skill invocation) |

**Core problem:** The unified command's frontmatter says `name: task` but its filename says `task-unified`. The Sprint CLI and cleanup_audit use the *filename-based* `/sc:task-unified` string. If the canonical user command is `/sc:task`, the CLI is using a non-canonical form. If the canonical form is `/sc:task-unified`, then the frontmatter `name` field is wrong.

---

## 3. Codebase Integration Map

### 3.1 Command Files

| File | Role | Active? |
|------|------|---------|
| `src/superclaude/commands/task-unified.md` | Canonical unified command (source of truth) | Yes |
| `.claude/commands/sc/task.md` | Deprecated legacy command (dev copy) | Deprecated |
| `src/superclaude/commands/task.md` | Legacy command (source of truth copy) | Deprecated |
| `src/superclaude/commands/task-mcp.md` | MCP-specific variant, references task-unified at line 375 | Deprecated (subsumed) |

### 3.2 Skill Files

| File | Role |
|------|------|
| `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | Execution protocol for STANDARD/STRICT tiers |

### 3.3 CLI Integration Points (Python)

| File | Line(s) | What it does |
|------|---------|-------------|
| `src/superclaude/cli/sprint/process.py` | 170 | `f"/sc:task-unified Execute all tasks in @{phase_file} --compliance strict --strategy systematic"` -- hardcoded string in `build_prompt()` |
| `src/superclaude/cli/sprint/config.py` | (1 match) | References `sc:task` in configuration context |
| `src/superclaude/cli/cleanup_audit/prompts.py` | Lines 26, 47, 69, 92, 116 | 5 prompt builders each emit `/sc:task-unified` as the subprocess command prefix for surface scan, deep analysis, consolidation detection, summary, and validation passes |
| `src/superclaude/cli/roadmap/validate_prompts.py` | (2 matches) | References `sc:task` in roadmap validation context |

### 3.4 Cross-References from Other Protocols

| Protocol | # References | Nature |
|----------|-------------|--------|
| `sc-tasklist-protocol/SKILL.md` | 12 | Stage 9 patch execution delegates to `sc:task-unified`; compliance tier integration; Sprint CLI alignment |
| `sc-roadmap-protocol/SKILL.md` | 1 | Pipeline position chain: `spec -> sc:roadmap -> ... -> sc:task-unified` |
| `sc-cli-portify-protocol/refs/code-templates.md` | 1 | Documents the sprint process pattern with `/sc:task-unified` framing |
| `sc-validate-tests-protocol/SKILL.md` | 1 | v1.0.0 release note for `/sc:task-unified` validation |
| `sc-release-split-protocol/SKILL.md` | 4 | References `sc:task` in release splitting context |

### 3.5 Other Command Cross-References

Files in `src/superclaude/commands/` that reference `sc:task`:
- `tasklist.md` (8 occurrences)
- `help.md` (2 occurrences)
- `validate-roadmap.md`, `adversarial.md`, `validate-tests.md`, `release-split.md` (1 each)
- `core/COMMANDS.md`, `core/ORCHESTRATOR.md` (1 each)

---

## 4. Architecture Pattern

### Sprint Pipeline Flow

```
execute_sprint()
  |
  v
Per-phase: ClaudeProcess(phase_file)
  |
  v
build_prompt()  [process.py:170]
  |
  v
Emits: "/sc:task-unified Execute all tasks in @{phase_file} --compliance strict --strategy systematic"
  |
  v
claude -p subprocess  (receives the prompt as stdin)
  |
  v
Claude Code session loads, resolves /sc:task-unified -> task-unified.md command -> classifies -> invokes sc:task-unified-protocol skill
```

The critical handoff is at `build_prompt()`. The string `/sc:task-unified` is a literal embedded in Python code. The subprocess Claude session must resolve this string to the correct command file. If the command file were renamed to `task.md` (matching frontmatter), `process.py:170` would need to emit `/sc:task` instead.

### Pipeline Executor Pattern

`execute_pipeline()` provides a generic sequential/parallel step group runner with gate checking. Each step constructs its prompt via `build_prompt()`, which currently hardcodes the `/sc:task-unified` prefix. This is not configurable -- it is a string literal in each prompt builder.

### Cleanup Audit Pattern

The cleanup_audit pipeline follows the same pattern: 5 distinct prompt builders in `prompts.py`, each constructing a prompt string starting with `/sc:task-unified`. These are independent prompt functions (surface scan, deep analysis, consolidation, summary, validation), each with the same hardcoded prefix.

---

## 5. Tasklist Format

The wave-based tasklist format (referenced from `.dev/releases/` examples) uses:

```markdown
### Task W{wave}-{number}: [Title]

| Field | Value |
|-------|-------|
| Type | [implement/refactor/fix/test/docs] |
| Target | [file path(s)] |
| Section | [code section or module] |
| Description | [what to do] |
| Depends | [W{n}-{nn} task dependencies] |
| Acceptance | [verification criteria] |
| Risk | [low/medium/high] |
| Wave | [wave number] |
```

Each task includes a compliance tier computed using the `/sc:task-unified` classification algorithm (per sc-tasklist-protocol/SKILL.md line 337). The tier determines the verification rigor applied during sprint execution.

---

## 6. Impact Assessment

### The 416-File Match Problem

The BrainStormQA.md claims "416 files match sc:task." My verification found:

- **43 files** match across `src/` and `.claude/` (live source + dev copies)
- **21 files** in `src/superclaude/` contain the pattern `sc:task` (72 total occurrences)
- **9 files** in `src/superclaude/` contain the more specific `sc:task-unified` (26 occurrences)

[INFERENTIAL] The 416 figure likely comes from searching the entire repository including `.dev/releases/complete/` which contains historical sprint output, tasklist files, and execution logs. These are archival artifacts, not live source. The discrepancy between 416 total and 43 live files supports the source document's assertion that "most are in .dev/releases/complete/ (historical output files)."

### The ~15-20 Live Source Files That Matter

Based on my grep analysis, the actual count is **21 unique files in `src/superclaude/`** that reference `sc:task` in some form. Of these, the highest-impact files for a naming change are:

**Tier 1 -- Must change (break sprint pipeline if wrong):**
1. `src/superclaude/cli/sprint/process.py` -- hardcoded prompt string
2. `src/superclaude/cli/cleanup_audit/prompts.py` -- 5 hardcoded prompt strings
3. `src/superclaude/commands/task-unified.md` -- the command definition itself

**Tier 2 -- Must change (break cross-protocol references):**
4. `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` -- protocol definition
5. `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` -- 12 references
6. `src/superclaude/commands/tasklist.md` -- 8 references

**Tier 3 -- Should change (documentation consistency):**
7-21. Remaining files with 1-4 references each (commands, core docs, other skills)

---

## 7. Naming Resolution Recommendations

### Option A: Canonicalize on `/sc:task` (RECOMMENDED)

**Rationale:** The frontmatter already says `name: task`. Users already type `/sc:task`. The "unified" suffix is an implementation detail from the migration period.

**Migration steps:**
1. Rename `task-unified.md` to `task.md` (replacing the deprecated legacy file)
2. Delete the deprecated `task.md` / `task-legacy` command
3. Rename `sc-task-unified-protocol/` directory to `sc-task-protocol/`
4. Rename skill frontmatter `name` from `sc:task-unified-protocol` to `sc:task-protocol`
5. Update `process.py:170` from `/sc:task-unified` to `/sc:task`
6. Update all 5 prompt builders in `cleanup_audit/prompts.py`
7. Update 12+ references in `sc-tasklist-protocol/SKILL.md`
8. Update remaining cross-references in other skills and commands
9. Run `make sync-dev` to propagate to `.claude/`

**Risk:** Medium. The rename touches many files but is mechanical (search-and-replace). The main risk is missing a reference in an obscure location.

### Option B: Canonicalize on `/sc:task-unified`

**Rationale:** Keeps current filenames and CLI hardcoded strings unchanged. Less migration work.

**Migration steps:**
1. Update command frontmatter `name` from `task` to `task-unified`
2. Delete the deprecated legacy `task.md`
3. Done (most references already use `task-unified`)

**Risk:** Low migration risk, but permanently embeds the "unified" suffix in the user-facing command name, which is awkward and carries historical baggage.

### Option C: Hybrid -- Keep `/sc:task` user-facing, keep `task-unified` as filename

**Rationale:** This is actually the current state, just formalized. Accept that the frontmatter name and filename diverge.

**Migration steps:**
1. Document the convention explicitly
2. Delete the deprecated legacy `task.md`
3. Ensure Claude Code resolves `/sc:task` to `task-unified.md` via frontmatter `name` field

**Risk:** Perpetuates the confusion. The Sprint CLI hardcodes `/sc:task-unified` which would remain inconsistent with the user-facing `/sc:task`.

### Recommendation

**Option A is the cleanest long-term choice.** The "unified" name served its purpose during migration from the dual task/task-mcp system. That migration is complete. The canonical name should be the simple one: `/sc:task` backed by `task.md` backed by `sc-task-protocol/`.

---

## 8. Cross-Domain Dependencies

### Connection to Checkpoint Enforcement

The checkpoint enforcement domain (analyzed separately in `analysis-checkpoint-enforcement.md`) intersects here because:
- The Sprint CLI's `build_prompt()` constructs the subprocess command that the checkpoint system must validate
- If the command name changes, checkpoint gate patterns that match on `sc:task-unified` output would need updating
- [INFERENTIAL] Any checkpoint regex or pattern matching on classification headers (`SC:TASK-UNIFIED:CLASSIFICATION`) would need updating if the naming changes. The classification header format is defined in `task-unified.md` lines 60-67.

### Connection to Sprint TUI v2

The Sprint TUI v2 domain (analyzed separately in `analysis-sprint-tui-v2.md`) intersects here because:
- TUI v2 will display phase execution status, which originates from the subprocess command in `process.py:170`
- The prompt string constructed by `build_prompt()` is the contract between the Sprint CLI and the Claude subprocess
- Any TUI features that parse or display the compliance tier classification depend on the header format defined in the unified command

### Connection to sc:tasklist-protocol

The tasklist protocol is the heaviest consumer of the `sc:task-unified` name (12+ references). It delegates Stage 9 (Patch Execution) to `sc:task-unified` directly. Any naming change must be coordinated with tasklist protocol updates.

---

## 9. Open Questions / Gaps

### Confirmed Gaps

1. **Command resolution order is undocumented.** When both `task.md` (deprecated) and `task-unified.md` (active) exist, which does Claude Code load for `/sc:task`? The frontmatter `name` field and the filename both could match. There is no documented resolution priority.

2. **The `task-mcp.md` command status.** It exists in `src/superclaude/commands/task-mcp.md` with a reference to task-unified at line 375. Its deprecation status relative to the unified command should be explicitly confirmed and the file cleaned up or removed.

3. **Classification header string stability.** The header `SC:TASK-UNIFIED:CLASSIFICATION` (task-unified.md lines 60-67) is used for telemetry/A/B testing. If the command is renamed, this header must either change (breaking telemetry consumers) or remain as-is (creating another name inconsistency).

### INFERENTIAL Items

4. **[INFERENTIAL] The 416-file count was not verified against the full repo.** I only searched `src/` and `.claude/`. The claim likely includes `.dev/releases/complete/` which I did not enumerate. The assertion that "most are historical" is consistent with the 43 vs 416 discrepancy but not directly confirmed.

5. **[INFERENTIAL] Sprint CLI subprocess resolution.** I assume the subprocess Claude session resolves `/sc:task-unified` by matching the filename `task-unified.md` in the commands directory. If Claude Code uses frontmatter `name` instead, the current behavior may already be broken or relying on fallback resolution. This needs testing.

6. **[INFERENTIAL] Whether `.claude/commands/sc/` contains a synced copy of `task-unified.md`.** The `.claude/commands/sc/task.md` is the legacy deprecated copy. I did not verify whether `task-unified.md` also exists in `.claude/commands/sc/` as a synced dev copy. If it does not, `make sync-dev` may not be propagating it correctly.

---

*End of analysis.*
