# v3.7 Unified Release Specification — Task Unified v2

**Version**: 3.7.0  
**Status**: Draft — Pending Review  
**Date**: 2026-04-02  
**Scope**: Checkpoint Enforcement + Sprint TUI v2 + Naming Consolidation  
**Target Directory**: `src/superclaude/cli/sprint/`  

---

## Table of Contents

1. [Release Overview](#1-release-overview)
2. [Problem Context & Motivation](#2-problem-context--motivation)
3. [Feature Area 1: Checkpoint Enforcement](#3-feature-area-1-checkpoint-enforcement)
4. [Feature Area 2: Sprint TUI v2](#4-feature-area-2-sprint-tui-v2)
5. [Feature Area 3: Naming & Identity Consolidation](#5-feature-area-3-naming--identity-consolidation)
6. [Cross-Cutting Concerns](#6-cross-cutting-concerns)
7. [Complete File Inventory](#7-complete-file-inventory)
8. [Model & Data Changes](#8-model--data-changes)
9. [Rollout Strategy](#9-rollout-strategy)
10. [Test Strategy](#10-test-strategy)
11. [Open Questions & Risks](#11-open-questions--risks)
12. [Out of Scope](#12-out-of-scope)
13. [Success Criteria](#13-success-criteria)
14. [Source Documents](#14-source-documents)

---

## 1. Release Overview

v3.7 delivers three interconnected feature areas that harden the sprint pipeline's reliability, observability, and developer experience:

| Feature Area | Purpose | Estimated LOC | Risk |
|-------------|---------|---------------|------|
| **Checkpoint Enforcement** | Ensure checkpoint files are always written, detected, and recoverable | ~580 | Low–Medium |
| **Sprint TUI v2** | Surface rich real-time data already in stream-json; add post-phase summaries and retrospective | ~800+ | Medium |
| **Naming Consolidation** | Resolve the sc:task / sc:task-unified / sc:task-unified-protocol confusion | ~100 | Low |

**Key Interdependencies**:
- TUI v2 (F6: Enhanced Terminal Panels) and Checkpoint Enforcement (Wave 2: `PASS_MISSING_CHECKPOINT` status) both modify `models.py` and `executor.py`
- TUI v2 (F8/F10: Summaries) and Checkpoint Enforcement (Wave 3: Manifest) both add post-phase processing in `executor.py`
- Naming Consolidation affects `process.py` which is also modified by Checkpoint Enforcement Wave 1

**Recommended implementation order**: Naming Consolidation first (reduces noise in subsequent diffs), then Checkpoint Enforcement Waves 1-2, then TUI v2, then Checkpoint Enforcement Waves 3-4.

---

## 2. Problem Context & Motivation

### 2.1 The Checkpoint Failure (Root Cause)

During the OntRAG R0+R1 sprint (2026-03-22, 7 phases), Phase 3 completed all 6 tasks and all 6 deliverables but **failed to write either checkpoint file**. All other phases wrote checkpoints successfully. Checkpoint writing was revealed to be **emergent, not enforced**.

**Root Cause — Triple Failure Chain:**

| # | Cause | Severity | Location |
|---|-------|----------|----------|
| 1 | Agent prompt contains **no checkpoint instructions** — `build_prompt()` says "STOP after all tasks" with zero mention of checkpoints | HIGH | `process.py:169-203` |
| 2 | Phase 3 uniquely has **two checkpoint sections** using `### Checkpoint:` headings structurally distinct from `### T<NN>.<NN>` task pattern | MEDIUM | `phase-3-tasklist.md:285-314` |
| 3 | Sprint executor has **no post-phase checkpoint enforcement** — `_check_checkpoint_pass()` exists but is only used for crash recovery | HIGH | `executor.py:1592-1603` |

**Contributing Factors**: Phase 3 had the largest output (744KB, context pressure), the agent did not use TodoWrite for checkpoint tracking, and 6/7 phases wrote checkpoints voluntarily (nondeterministic).

### 2.2 The TUI Observability Gap

The current Sprint TUI displays minimal information despite the `claude stream-json` output containing rich data: turn counts, token usage, tool call details, assistant text, error signals, and model metadata. Operators must read raw output files to understand what happened during a sprint. The TUI v2 refactor surfaces this data in real time.

### 2.3 The Naming Confusion

Three naming layers cause confusion:

| Layer | Name | File | State |
|-------|------|------|-------|
| Legacy Command | `sc:task` | `.claude/commands/sc/task.md` | Deprecated (`deprecated: true`, `name: task-legacy`), still present |
| Unified Command | `sc:task-unified` | `src/superclaude/commands/task-unified.md` | Active, but frontmatter says `name: task` while code uses `/sc:task-unified` |
| Protocol Skill | `sc:task-unified-protocol` | `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | Active, invoked for STANDARD/STRICT |

All CLI code (sprint pipeline, cleanup audit) references `/sc:task-unified`, but the command's frontmatter declares `name: task`.

---

## 3. Feature Area 1: Checkpoint Enforcement

### 3.1 Architecture — Three-Layer Enforcement Model

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 1 — PREVENTION (Agent-Side)                           │
│    Solution 1: Prompt instructions → agent told to write CPs │
│    Solution 2: Tasklist normalization → CPs become tasks     │
│    Result: Agent writes checkpoints as part of normal work   │
├──────────────────────────────────────────────────────────────┤
│  Layer 2 — DETECTION (Executor-Side, Real-Time)              │
│    Solution 3: Post-phase gate verifies CP files exist       │
│    Result: Sprint halts/warns if agent missed them           │
├──────────────────────────────────────────────────────────────┤
│  Layer 3 — REMEDIATION (Post-Sprint, On-Demand)              │
│    Solution 4: Manifest + CLI verify + auto-recovery         │
│    Result: Missing CPs detected, audited, optionally rebuilt │
└──────────────────────────────────────────────────────────────┘
```

All four solutions are **complementary**, not alternatives. Each addresses different root causes:

| Solution | Cause 1 (No prompt) | Cause 2 (Structural) | Cause 3 (No enforcement) | Effectiveness | Est. Failure Rate |
|----------|:---:|:---:|:---:|:---:|:---:|
| 1 — Prompt Enforcement | **FIXES** | Mitigates | Partially | HIGH | 14% → ~5% |
| 2 — Tasklist Normalization | N/A | **ELIMINATES** | — | VERY HIGH | <1% |
| 3 — Post-Phase Gate | — | — | **FIXES** (detection) | MEDIUM | Detection-only |
| 4 — Manifest + Recovery | — | — | **FIXES** (detection + remediation) | MEDIUM | Remediation-only |

### 3.2 Implementation Waves

#### Wave 1 — Prompt-Level Checkpoint Enforcement (Day 1)

**Goal**: Transform checkpoint writing from emergent to instructed behavior.  
**Risk**: Very Low | **LOC**: ~60 | **Files**: `process.py`, `executor.py`

| Task | File | Description | Effort | Confidence |
|------|------|-------------|--------|:---:|
| T01.01 | `process.py` | Add `## Checkpoints` section to `build_prompt()` (L123-203); amend `## Scope Boundary` and `## Result File` | S | 95% |
| T01.02 | `executor.py` | Add `_warn_missing_checkpoints()` — parse checkpoint paths, check existence, log warnings (no status change) | S | 90% |

**Key details for T01.01 — prompt additions**:
- New `## Checkpoints` section with 5 instruction lines between task execution and `## Scope Boundary`
- `## Scope Boundary` amended: "After completing all tasks AND writing all checkpoint reports, STOP immediately"
- `## Result File` amended: "Write result file only after all checkpoint reports are written"

#### Wave 2 — Post-Phase Checkpoint Enforcement Gate (Day 2-5)

**Goal**: Detect checkpoint failures at runtime; deploy in shadow mode.  
**Risk**: Low | **LOC**: ~120 | **Files**: `checkpoints.py` (NEW), `executor.py`, `models.py`, `logging_.py`  
**Dependencies**: Wave 1 (T01.02 establishes call site)

| Task | File | Description | Effort | Confidence |
|------|------|-------------|--------|:---:|
| T02.01 | `checkpoints.py` (NEW) | Create shared module with `extract_checkpoint_paths()` and `verify_checkpoint_files()` | S | 85% |
| T02.02 | `models.py` | Add `PASS_MISSING_CHECKPOINT` to `PhaseStatus` enum; add `checkpoint_gate_mode` config | XS | 90% |
| T02.03 | `logging_.py` | Add `write_checkpoint_verification()` JSONL event | XS | 95% |
| T02.04 | `executor.py` | Wire `_verify_checkpoints()` into phase completion — replaces Wave 1's warning with configurable gate | M | 85% |
| T02.05 | `tests/` | Unit tests for `checkpoints.py` (0/1/2 checkpoint fixtures) and `PASS_MISSING_CHECKPOINT` integration | S | — |

**Gate modes** (added to `SprintConfig`):
```python
checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```
- `off`: No verification | `shadow`: Log JSONL only | `soft`: Log + on-screen warning | `full`: Downgrade PASS to PASS_MISSING_CHECKPOINT

#### Wave 3 — Manifest, CLI & Auto-Recovery (Day 5-10)

**Goal**: Post-sprint audit capability and automated remediation.  
**Risk**: Medium | **LOC**: ~200 | **Files**: `checkpoints.py`, `commands.py`, `executor.py`, `models.py`  
**Dependencies**: Wave 2 (`checkpoints.py` exists)

| Task | File | Description | Effort | Confidence |
|------|------|-------------|--------|:---:|
| T03.01 | `models.py` | Add `CheckpointEntry` dataclass | XS | 95% |
| T03.02 | `checkpoints.py` | Add `build_manifest()` and `write_manifest()` | M | 80% |
| T03.03 | `checkpoints.py` | Add `recover_missing_checkpoints()` from evidence artifacts (**lowest confidence task**) | M | **75%** |
| T03.04 | `commands.py` | Add `verify-checkpoints` CLI subcommand with `--recover` and `--json` flags | S | 85% |
| T03.05 | `executor.py` | Wire manifest build at sprint start + finalize at sprint end | S | 85% |
| T03.06 | `tests/` | Unit + integration tests for manifest, recovery, and CLI verify-checkpoints | S | — |

**Auto-recovery**: Generates retroactive checkpoints from deliverable evidence files, clearly marked with `## Note: Auto-Recovered` and `recovered: true` frontmatter. Opt-in only via `--recover` flag.

> **Detailed implementation steps**: Per-task [PLANNING]/[EXECUTION]/[VERIFICATION] step breakdowns, rollback commands, acceptance criteria, and risk drivers are in the source document: `tasklist-checkpoint-enforcement.md`

#### Wave 4 — Tasklist Normalization (Next Release, Deferred)

**Goal**: Structurally eliminate heading pattern mismatch for all future tasklists.  
**Risk**: Low-Medium | **LOC**: ~200 | **Files**: `SKILL.md` (sc-tasklist-protocol)  
**Breaking change**: Existing tasklists unaffected; new generation only.

| Task | File | Description | Effort | Confidence |
|------|------|-------------|--------|:---:|
| T04.01 | `SKILL.md` | Emit checkpoints as `### T<PP>.<NN> -- Checkpoint:` entries with metadata tables | M | 80% |
| T04.02 | `SKILL.md` | Add 3 validation rules to Sprint Compatibility Self-Check | S | 85% |
| T04.03 | `SKILL.md` | Add checkpoint deliverable type (D-CP*) to deliverable registry | XS | 90% |

### 3.3 Key Design Decisions

1. **Shared path extraction module**: Both the per-phase gate (Sol 3) and manifest (Sol 4) parse `Checkpoint Report Path:` from tasklists. `checkpoints.py` provides `extract_checkpoint_paths()` once — eliminating duplication.

2. **Shadow-first rollout**: The gate defaults to `shadow` because path resolution bugs could cause false positives. Promote to `soft` after 2 sprint cycles, then `full` after confirming zero false positives.

3. **Wave 4 deferred, not dropped**: Strongest structural fix but a breaking change requiring tasklist regeneration. Waves 1-3 provide full interim coverage.

4. **Warning-only in Wave 1**: Ships Day 1 with zero risk. Proper configurable gate comes in Wave 2.

5. **Auto-recovery is opt-in**: Never invoked automatically. Lower fidelity than agent-written checkpoints.

6. **`PASS_MISSING_CHECKPOINT` is non-failure**: `is_failure = False` — tasks passed, only checkpoints missing.

---

## 4. Feature Area 2: Sprint TUI v2

### 4.1 Summary

Visual UX refactor of the Sprint TUI to surface richer real-time information from Claude's `stream-json` output. Ten feature areas across 5 modified files and 2 new files. Introduces the "programmatic extraction + Haiku narrative" pattern for post-phase intelligence.

### 4.2 Current vs Target State

| Aspect | Current | v2 |
|--------|---------|-----|
| Header | Name + elapsed | Elapsed + model + turn counter |
| Phase table | 5 columns | 6 columns (+Turns, +Output, -Tasks) |
| Progress | Single phase bar | Dual bars: Phases + Tasks |
| Active panel | Basic file/status | + Activity stream + Prompt/Agent context lines |
| Errors | Not displayed | Conditional red-bordered error panel |
| Post-phase | Nothing | Phase summaries (background thread) |
| Post-sprint | Result + resume | Aggregate stats (turns, tokens, output, files) |
| Release summary | Nothing | Release retrospective with validation matrix |
| Tmux | 2 panes | 3 panes (TUI + summary + tail) |
| Sprint name | Absent | In outer panel title |

### 4.3 Feature Catalog (F1-F10)

#### F1: Activity Stream (3 lines, scrolling)
- Last 3 tool calls with `HH:MM:SS ToolName condensed_input`
- FIFO ring buffer; `[thinking... Ns]` placeholder when idle >2s
- **MonitorState**: `activity_log: list[tuple[float, str, str]]` (max 3)

#### F2: Enhanced Phase Table
- Add Turns (width=6) and Output (width=8) columns; remove Tasks column
- **MonitorState**: `turns: int = 0`

#### F3: Task-Level Progress Bar
- Dual compact bars on single line: `Phases ======-------- 25% 1/4    Tasks ==========------ 51% 20/39`
- Total tasks pre-scanned via `T\d{2}\.\d{2}` regex on sprint start
- **MonitorState**: `total_tasks_in_phase: int`, `completed_task_estimate: int`
- **SprintConfig**: `total_tasks: int = 0`

#### F4: Conditional Error Panel
- Hidden when error count is 0; red border, title `ERRORS (N)`
- Max 5 displayed, `(+N more)` overflow
- **MonitorState**: `errors: list[tuple[str, str, str]]` (max 10)

#### F5: LLM Context Lines
- `Prompt:` (static per phase, ~60 chars) and `Agent:` (last assistant text, ~60 chars)
- **MonitorState**: `last_assistant_text: str = ""`

#### F6: Enhanced Terminal Summary Panels
- **Success**: Result, Duration, Turns (total + avg/phase), Tokens (in/out), Output, Files, Log path
- **Halt**: + Completed count, Last task, Errors, Resume command
- **SprintResult properties**: `total_turns`, `total_tokens_in`, `total_tokens_out`, `total_output_bytes`, `total_files_changed`

#### F7: Sprint Name in Panel Title
- `[bold]SUPERCLAUDE SPRINT RUNNER[/] [dim]== {release_name}[/]`
- Trivial change to `_render()` Panel title

#### F8: Post-Phase Summary (Programmatic + Haiku Narrative)
- **F9 and F10 both depend on F8** (F8 produces the phase summaries that F9 displays and F10 aggregates)
- Background `SummaryWorker` thread per completed phase
- 4-step pipeline: programmatic NDJSON extraction → Haiku narrative (10-30s) → write `results/phase-N-summary.md` → update tmux/TUI
- **Programmatic extraction** parses: tasks, files changed, validation evidence, agent reasoning excerpts, errors
- **Haiku call**: `claude --print --model claude-haiku-4-5 --max-turns 1 -p <prompt>` (30s timeout, non-fatal failure)
- **New module**: `summarizer.py` (PhaseSummary, PhaseSummarizer, SummaryWorker)

#### F9: Tmux Summary Pane
- 3-pane layout: TUI (50%) + summary (25%) + tail (25%)
- `update_summary_pane()` pipes `phase-N-summary.md` to middle pane
- `--no-tmux` fallback: notification in TUI header

#### F10: Release Retrospective
- **Blocking** before terminal display
- Aggregates all phase summaries → cross-phase analysis → Haiku narrative → `results/release-retrospective.md`
- **New module**: `retrospective.py` (ReleaseRetrospective, RetrospectiveGenerator)

### 4.4 Target Layouts

**Active Sprint** (~25 lines):
```
+=========== SUPERCLAUDE SPRINT RUNNER == {release_name} ==============+
|  Elapsed: 12m 34s    Model: claude-opus-4-6    Turns: 23/50          |
|  #  Phase                            Status   Duration  Turns  Output |
|  1  Foundation & Architecture        PASS     16s       7      10 KB  |
|  2  Command & Skill Implementation   RUNNING  2m 34s    23     148 KB |
|  Phases ======-------- 25% 1/4    Tasks ==========------ 51% 20/39   |
|  +---- ACTIVE: phase-2-tasklist.md ----------------------------------+|
|  | Status:  RUNNING -- active (+312.5 B/s)                           ||
|  | Task:    T02.08   Tool: Bash   Files: 3                           ||
|  | Prompt:  Execute all tasks in phase-2-tasklist.md --compliance...  ||
|  | Agent:   Good -- the directory doesn't exist yet, and there's...  ||
|  |  02:53:42  Grep  pyproject.toml (packages config)                 ||
|  |  02:53:43  Write sc-tasklist-protocol/SKILL.md                    ||
|  |  02:53:46  Todo  updated 5 tasks                                  ||
|  +--------------------------------------------------------------------+|
|  +---- ERRORS (2) ---------------------------------------------------+|
|  |  T02.04  Bash  exit 1 -- "mkdir: permission denied"               ||
|  +--------------------------------------------------------------------+|
+-----------------------------------------------------------------------+
```

**Sprint Complete**: All phases PASS, 100% progress bars, aggregate stats panel.

**Sprint Halted**: Partial progress, HALTED panel with failure details + errors + resume command.

### 4.5 New Modules

#### `summarizer.py`

| Class | Purpose |
|-------|---------|
| `PhaseSummary` | Dataclass: tasks, files_changed, validations, reasoning_excerpts, errors, narrative |
| `PhaseSummarizer` | `summarize()` → `_extract_structured()` → `_generate_narrative()` → `_write_summary()` |
| `SummaryWorker` | Background thread pool: `submit()`, `wait_all(timeout=60)`, `latest_summary_path` |

**Critical invariants**:
- Summary failure must never affect sprint execution. All exceptions caught.
- `SummaryWorker._summaries` dict MUST be guarded by `threading.Lock` — unlike `OutputMonitor` (single writer thread), SummaryWorker uses a thread pool with concurrent writers.

#### `retrospective.py`

| Class | Purpose |
|-------|---------|
| `ReleaseRetrospective` | Dataclass: phase_outcomes, all_files, validation_matrix, all_errors, narrative |
| `RetrospectiveGenerator` | `generate()` → `_read_phase_summaries()` → `_aggregate()` → `_generate_narrative()` → `_write_retrospective()` |

**Cross-phase analysis**: file evolution tracking, error patterns, validation coverage gaps, timing trends.

---

## 5. Feature Area 3: Naming & Identity Consolidation

### 5.1 Current State (Verified)

- **9 live source files** reference `sc:task-unified` (2 Python + 7 Markdown)
- **666 total repo files** match `sc:task`, but ~641 are immutable historical outputs in `.dev/releases/complete/`
- Only **~15-20 live source files** need updating

### 5.2 Recommended Actions

1. **Resolve name/filename mismatch**: Rename `task-unified.md` → `task.md`, align frontmatter `name: task`. Update all code from `/sc:task-unified` → `/sc:task`.

2. **Remove legacy command**: Delete `.claude/commands/sc/task.md` (deprecated, causes confusion).

3. **Rename protocol skill**: `sc-task-unified-protocol/` → `sc-task-protocol/`. Update SKILL.md frontmatter accordingly.

4. **Update live references** (9 verified files):

   **Python** (2 files, 7 occurrences):
   - `src/superclaude/cli/sprint/process.py` — L124, L170
   - `src/superclaude/cli/cleanup_audit/prompts.py` — L26, L47, L69, L92, L116

   **Markdown** (7 files):
   - `src/superclaude/commands/task-unified.md` → rename + update
   - `src/superclaude/commands/task-mcp.md` — 1 cross-reference
   - `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` → rename directory + update
   - `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — 12+ references
   - `src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md` — 1 reference
   - `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` — 1 reference
   - `src/superclaude/skills/sc-validate-tests-protocol/SKILL.md` — 1 reference

5. **Post-rename**: Run `make sync-dev` and `make verify-sync`.

6. **Do NOT touch historical files**: 641+ files in `.dev/releases/complete/` and `.dev/releases/archive/` are immutable.

### 5.3 Architecture Context

```
User invokes: superclaude sprint run
    │
    ▼
execute_sprint(config)          [executor.py]
    │  (per phase)
    ▼
ClaudeProcess(config, phase)    [process.py]
    │
    ▼
build_prompt() → "/sc:task-unified Execute all tasks in @{phase_file}..."
    │
    ▼
Spawns: claude -p <prompt> --print --verbose
```

**Integration dependency chain**:
```
sc:task (command) ──invokes──▶ sc:task-protocol (skill)
                                     ▲ referenced by
    sc:tasklist-protocol (12+ refs) ─┘
    sc:cli-portify-protocol (1 ref) ─┘
    sc:roadmap-protocol (1 ref) ─────┘
    sc:validate-tests-protocol (1 ref)┘
```

---

## 6. Cross-Cutting Concerns

### 6.1 Shared File Modifications

Several files are modified by multiple feature areas. Implementation must be coordinated:

| File | Feature Areas | Coordination Notes |
|------|--------------|-------------------|
| `executor.py` | Checkpoint (W1-W3) + TUI v2 (F8/F10) | Both add post-phase processing. SummaryWorker and checkpoint verification must coexist. |
| `models.py` | Checkpoint (W2-W3) + TUI v2 (F2/F3/F6) | Both add fields to MonitorState, PhaseResult, SprintResult. Non-conflicting but merge carefully. |
| `process.py` | Checkpoint (W1) + Naming | Naming changes `/sc:task-unified` → `/sc:task` in the same file where W1 adds checkpoint instructions. Do naming first. |
| `tui.py` | TUI v2 (F1-F7) + Checkpoint (W2 status display) | TUI must render `PASS_MISSING_CHECKPOINT` appropriately in phase table. |
| `logging_.py` | Checkpoint (W2) only | Clean separation. |
| `commands.py` | Checkpoint (W3) only | Clean separation. |

### 6.2 Recommended Implementation Order

1. **Naming Consolidation** — reduces noise in all subsequent diffs
2. **Checkpoint W1** (Prompt fix) — highest value, lowest risk, immediate effect
3. **TUI v2 Core** (F1-F7) — model changes + display refactor
4. **Checkpoint W2** (Gate) — adds `PASS_MISSING_CHECKPOINT` which TUI must render
5. **TUI v2 Summary** (F8-F10) — new modules, background threading
6. **Checkpoint W3** (Manifest + CLI) — extends checkpoints.py, adds CLI
7. **Checkpoint W4** (Deferred) — next release cycle

### 6.3 Haiku Subprocess Conventions

Both F8 (Phase Summary) and F10 (Retrospective) call `claude --print --model claude-haiku-4-5`:
- **Environment**: Must strip `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` env vars to prevent recursive Claude Code session
- **Flags**: `--max-turns 1 --dangerously-skip-permissions` (non-interactive, no permission prompts)
- **Stdin**: Set to `subprocess.DEVNULL`
- **Timeout**: 30 seconds (non-fatal — summary written without narrative on failure)

### 6.4 Post-Phase Hook Ordering in executor.py

Since both Checkpoint (W1-W3) and TUI v2 (F8/F10) add post-phase processing, define explicit call order:
1. `_verify_checkpoints()` — blocking, checkpoint gate evaluation
2. `summary_worker.submit()` — non-blocking, background thread
3. Manifest update (Wave 3) — lightweight, blocking

### 6.5 Token Display Helper

Both TUI v2 and Checkpoint features need human-readable token formatting:
```python
def _format_tokens(n: int) -> str:
    if n < 1000: return f"{n}"
    if n < 1_000_000: return f"{n / 1000:.1f}K"
    return f"{n / 1_000_000:.1f}M"
```
Place in a shared `utils.py` or directly in `tui.py`.

---

## 7. Complete File Inventory

### New Files

| File | Feature Area | Purpose |
|------|-------------|---------|
| `src/superclaude/cli/sprint/checkpoints.py` | Checkpoint W2-W3 | Path extraction, verification, manifest, recovery |
| `src/superclaude/cli/sprint/summarizer.py` | TUI v2 F8 | PhaseSummary, PhaseSummarizer, SummaryWorker |
| `src/superclaude/cli/sprint/retrospective.py` | TUI v2 F10 | ReleaseRetrospective, RetrospectiveGenerator |

### Modified Files

| File | Feature Area(s) | Changes |
|------|-----------------|---------|
| `src/superclaude/cli/sprint/process.py` | Naming + Checkpoint W1 | Rename references + add checkpoint instructions to `build_prompt()` |
| `src/superclaude/cli/sprint/executor.py` | Checkpoint W1-W3 + TUI v2 F8/F10 | Warning helper → gate → manifest + SummaryWorker + RetrospectiveGenerator |
| `src/superclaude/cli/sprint/models.py` | Checkpoint W2-W3 + TUI v2 F2/F3/F6 | New enum value, config fields, dataclasses, MonitorState/PhaseResult/SprintResult fields |
| `src/superclaude/cli/sprint/logging_.py` | Checkpoint W2 | `write_checkpoint_verification()` JSONL event |
| `src/superclaude/cli/sprint/commands.py` | Checkpoint W3 | `verify-checkpoints` subcommand |
| `src/superclaude/cli/sprint/config.py` | Checkpoint W2 + TUI v2 F3 | Wire `checkpoint_gate_mode` CLI flag and `total_tasks` pre-scan into SprintConfig |
| `src/superclaude/cli/sprint/monitor.py` | TUI v2 F1-F5 | Turn counting, token tracking, activity log, error detection, task counting |
| `src/superclaude/cli/sprint/tui.py` | TUI v2 F1-F7 | Full layout rewrite, new methods, summary notification |
| `src/superclaude/cli/sprint/tmux.py` | TUI v2 F9 | 3-pane layout, summary pane management, pane index update |

### Renamed/Deleted Files (Naming Consolidation)

| Action | File |
|--------|------|
| RENAME | `src/superclaude/commands/task-unified.md` → `task.md` |
| RENAME (dir) | `src/superclaude/skills/sc-task-unified-protocol/` → `sc-task-protocol/` |
| DELETE | `.claude/commands/sc/task.md` (legacy deprecated) |
| UPDATE | 7 markdown files with reference changes (see Section 5.2) |
| UPDATE | 2 Python files with reference changes |

### Output Artifacts (per sprint run)

| File | When Written |
|------|-------------|
| `results/phase-N-summary.md` | Background, after each phase completes |
| `results/release-retrospective.md` | Blocking, after all phases complete |
| `manifest.json` | Sprint start (initial) + sprint end (final) |

**Totals**: ~3 new + ~12 modified + ~2 renamed + ~1 deleted ≈ 18 files touched. ~1,480+ LOC across all features (Checkpoint ~580, TUI v2 ~800+, Naming ~100).

---

## 8. Model & Data Changes

### 8.1 MonitorState — 8 new fields

```python
@dataclass
class MonitorState:
    # Existing fields...

    # TUI v2 F1: Activity stream
    activity_log: list = field(default_factory=list)    # list[tuple[float, str, str]], max 3

    # TUI v2 F2: Turn tracking
    turns: int = 0

    # TUI v2 F3: Task counting
    total_tasks_in_phase: int = 0
    completed_task_estimate: int = 0

    # TUI v2 F4: Error tracking
    errors: list = field(default_factory=list)          # list[tuple[str, str, str]], max 10

    # TUI v2 F5: LLM context
    last_assistant_text: str = ""

    # TUI v2 F6: Token tracking
    tokens_in: int = 0
    tokens_out: int = 0
```

### 8.2 PhaseResult — 3 new fields

```python
@dataclass
class PhaseResult:
    # Existing fields...
    turns: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
```

### 8.3 SprintResult — 5 new aggregate properties

```python
@property
def total_turns(self) -> int: ...
@property
def total_tokens_in(self) -> int: ...
@property
def total_tokens_out(self) -> int: ...
@property
def total_output_bytes(self) -> int: ...
@property
def total_files_changed(self) -> int: ...
```

### 8.4 SprintConfig — 2 new fields

```python
total_tasks: int = 0                    # TUI v2 F3: pre-scanned from phase files
checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"  # Checkpoint W2
```

### 8.5 PhaseStatus Enum — 1 new value

```python
PASS_MISSING_CHECKPOINT = "pass_missing_checkpoint"
# is_failure = False, is_terminal = True, is_success = True
# Follows existing pattern of PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED
```

**Note**: Must be added to `is_terminal` and `is_success` property tuples alongside existing PASS variants.

### 8.6 CheckpointEntry — new dataclass (Checkpoint W3)

```python
@dataclass
class CheckpointEntry:
    phase: int
    name: str
    expected_path: Path
    exists: bool
    recovered: bool = False
    recovery_source: str | None = None
```

---

## 9. Rollout Strategy

### 9.1 Timeline

| Phase | Scope | Gate Mode | Duration |
|-------|-------|-----------|----------|
| **Day 0** | Naming Consolidation | N/A | 1 day |
| **Day 1** | Checkpoint Wave 1 (prompt fix + warning) | N/A | 1 day |
| **Day 2-4** | TUI v2 Core (F1-F7, model changes, monitor, tui) | N/A | 3 days |
| **Day 3-5** | Checkpoint Wave 2 (gate, checkpoints.py, logging) | `shadow` | 2 days |
| **Day 5-8** | TUI v2 Summary (F8-F10, summarizer.py, retrospective.py, tmux) | N/A | 3 days |
| **Day 8-12** | Checkpoint Wave 3 (manifest, CLI, recovery) | `shadow` | 4 days |
| **Day 12** | Promote checkpoint gate | `shadow` → `soft` | — |
| **Sprint +2** | Promote checkpoint gate | `soft` → `full` | — |
| **Next release** | Checkpoint Wave 4 (tasklist normalization) | `full` | — |

### 9.2 Configuration Mechanism

The `checkpoint_gate_mode` is exposed via CLI flag, following the existing `wiring_gate_mode` pattern:
```bash
superclaude sprint run --checkpoint-gate=shadow   # default
superclaude sprint run --checkpoint-gate=soft
superclaude sprint run --checkpoint-gate=full
superclaude sprint run --checkpoint-gate=off
```
The flag is parsed in `config.py` and mapped to `SprintConfig.checkpoint_gate_mode`.

**Note**: `src/superclaude/cli/sprint/config.py` must be updated to wire the new `checkpoint_gate_mode` and `total_tasks` fields into `SprintConfig` construction.

---

## 10. Test Strategy

### 10.1 Existing Tests Requiring Updates

| Test File | Changes |
|-----------|---------|
| `test_tui.py` | New columns, new MonitorState fields in fixtures, new methods (`_build_dual_progress()`, `_build_error_panel()`), summary notification |
| `test_models.py` | New fields on MonitorState/PhaseResult, SprintResult properties, SprintConfig.total_tasks, CheckpointEntry, PASS_MISSING_CHECKPOINT |

### 10.2 New Tests Required

| Test File | Coverage |
|-----------|----------|
| `test_checkpoints.py` | `extract_checkpoint_paths()`, `verify_checkpoint_files()`, `build_manifest()`, `recover_missing_checkpoints()` — unit tests with 0/1/2 checkpoint fixtures |
| `test_summarizer.py` | NDJSON extraction, narrative prompt building, markdown generation, SummaryWorker threading + thread safety |
| `test_retrospective.py` | Phase summary aggregation, cross-phase analysis, narrative generation, retrospective markdown |
| `test_tmux.py` | 3-pane layout creation, summary pane updates, pane index handling |

### 10.3 Tests Not Affected

`test_cli_contract.py`, `test_config.py` (minimal), `test_process.py`, `test_e2e_*.py`

### 10.4 Test Tasks Added

The original checkpoint enforcement tasklist did not include dedicated test-writing tasks. This has been addressed by adding:
- **T02.05**: Unit tests for `checkpoints.py` and `PASS_MISSING_CHECKPOINT` integration (Wave 2)
- **T03.06**: Unit + integration tests for manifest, recovery, and CLI verify-checkpoints (Wave 3)

---

## 11. Open Questions & Risks

### 11.1 Open Questions

| # | Question | Feature Area | Impact |
|---|----------|-------------|--------|
| 1 | **Config persistence for `checkpoint_gate_mode`**: How do users set it? CLI flag, env var, config file? Rollout timeline assumes operators can change it, but mechanism is unspecified. | Checkpoint | Medium — blocks gate promotion |
| 2 | **Wave 1 → Wave 2 replacement**: T02.04 "replaces" T01.02's `_warn_missing_checkpoints()`. If shipping to different branches, merge strategy needs definition. | Checkpoint | Low — implementation detail |
| 3 | **Mid-phase checkpoint verification**: Does the Wave 2 gate check only end-of-phase CPs or also mid-phase CPs? If end-only, mid-phase CPs remain unverified by Layer 2. | Checkpoint | Medium — Phase 3's mid-phase CP was part of the original failure |
| 4 | ~~**SummaryWorker module placement**~~ **RESOLVED**: SummaryWorker is defined in `summarizer.py`, imported by `executor.py`. Standard import pattern. | TUI v2 | Closed |
| 5 | **Prompt preview source for F5**: TUI doesn't have access to full prompt text. Add `prompt_preview: str` to `Phase` or compute from config? | TUI v2 | Low |
| 6 | ~~**SummaryWorker thread safety**~~ **RESOLVED**: `threading.Lock` is now mandated for `_summaries` dict access (see §4.5). | TUI v2 | Closed |
| 7 | **NDJSON parsing robustness**: Malformed lines or schema changes in stream-json could break extraction. Error handling not detailed. | TUI v2 | Medium |
| 8 | **Retrospective blocking duration**: Up to 30s Haiku timeout delays terminal display. No progress indicator specified. | TUI v2 | Low — UX concern |
| 9 | **Wave 4 migration path**: No utility or documentation for converting old `### Checkpoint:` → `### T<PP>.<NN> -- Checkpoint:`. | Checkpoint | Low — deferred feature |
| 10 | **Interaction with `_check_checkpoint_pass()` crash recovery**: Not in any task's modification scope. Should it be deprecated or retained? | Checkpoint | Low |
| 11 | **Evidence file format for auto-recovery**: `D-*/evidence.md` format/location unspecified. Inconsistent structure across sprints could degrade recovery quality. | Checkpoint | Medium |
| 12 | **Tasklist index format**: `build_manifest()` takes `tasklist_index: Path` — is this an existing artifact or needs creation? | Checkpoint | Low |
| 13 | ~~**`output_bytes` and `files_changed` on PhaseResult**~~ **RESOLVED**: Both `output_bytes` (L442) and `files_changed` (L445) already exist on `PhaseResult`. No new additions needed for these fields. | TUI v2 | Closed |

### 11.2 Technical Risks

| Risk | Area | Likelihood | Impact | Mitigation |
|------|------|------------|--------|------------|
| Agent ignores prompt instructions despite Wave 1 | Checkpoint | Low-Med | Med | Waves 2+3 detect and remediate |
| Path resolution false positives in Wave 2 | Checkpoint | Low | High (if full mode) | Shadow-first rollout |
| Numbering cascade errors in Wave 4 | Checkpoint | Low-Med | Med | Self-check validation + W1-W3 fallback |
| Auto-recovery low-quality output | Checkpoint | Med | Low | `Auto-Recovered` marking + opt-in only |
| Haiku subprocess unavailable/rate-limited | TUI v2 | Low | Low | Non-fatal; summaries written without narrative |
| Thread safety in SummaryWorker | TUI v2 | Med | Med | Add `threading.Lock` around shared state |
| Terminal width <120 cols causes wrapping | TUI v2 | Low | Low | Not specified; consider adaptive behavior |
| Token tracking underreporting | TUI v2 | Low | Low | Best-effort accumulation |
| Tmux pane index mismatch on partial failure | TUI v2 | Low | Med | try/except kills session on failure |

---

## 12. Out of Scope (Explicitly Deferred)

### TUI v2
1. `--compact` CLI flag for current minimal layout
2. Cost tracking / cache hit ratio display
3. MCP server health indicators
4. ETA estimation for phase/sprint completion
5. `sprint status` and `sprint logs` command implementations (stubs)
6. Modal overlay for summary viewing in `--no-tmux` mode
7. Configurable summary model (hardcoded to `claude-haiku-4-5`)
8. Interactive summary navigation (viewing older phase summaries)

### Checkpoint
9. Automatic gate promotion (manual promotion per rollout schedule)
10. Cross-sprint checkpoint trend analysis
11. Checkpoint content validation (only file existence is checked)

---

## 13. Success Criteria

| Metric | Current | Target | Measured By |
|--------|---------|--------|-------------|
| Checkpoint write rate | 86% (6/7) | **100%** | JSONL `checkpoint_verification` events |
| False positive rate in gate | N/A | **0%** over 2 cycles | Shadow mode data |
| Time to detect missing CP | Manual | **<1 second** | Wave 2 gate |
| Time to recover missing CP | ~30 min | **<5 seconds** | Wave 3 `--recover` CLI |
| Root causes addressed | 0/3 | **3/3** | W1 + W4 + W2/W3 |
| TUI data surfaced from stream-json | ~20% | **>80%** | Feature coverage F1-F7 |
| Post-phase intelligence | None | **100% phases summarized** | `results/phase-N-summary.md` files |
| Naming consistency | 3 layers | **1 canonical name** | Grep audit |

---

## 14. Source Documents

All source documents are in `/config/workspace/IronClaude/.dev/releases/backlog/v3.7-task-unified-v2/`:

| Document | Size | Content |
|----------|------|---------|
| `troubleshoot-missing-p03-checkpoint.md` | 12 KB | Root cause analysis of missing Phase 3 checkpoints |
| `unified-checkpoint-enforcement-proposal.md` | 20 KB | Adversarial comparison + unified 4-solution proposal |
| `tasklist-checkpoint-enforcement.md` | 35 KB | Implementation task list (4 phases, 15 tasks) |
| `sprint-tui-v2-requirements.md` | 45 KB | Sprint TUI v2 requirements (10 features, 7 files) |
| `BrainStormQA.md` | 0.4 KB | Naming/identity consolidation dimensions |
| `CodeBaseContext.md` | 1.6 KB | Codebase references, architecture, integration points |
