# Checkpoint Enforcement — Implementation Task List

**Source**: `unified-checkpoint-enforcement-proposal.md`
**Root Cause**: `troubleshoot-missing-p03-checkpoint.md`
**Target Repo**: `/config/workspace/IronClaude/`
**Target Dir**: `src/superclaude/cli/sprint/`
**Execution**: sc:task-unified compatible — 4 phases (Wave 1–4)

---

## Phase 1 — Prompt-Level Checkpoint Enforcement (Wave 1)

**Goal**: Transform checkpoint writing from emergent to instructed behavior. Ship within 1 day.
**Risk**: Very Low. String additions to prompt template + warning helper. Zero behavioral change to executor.
**Files**: `process.py`, `executor.py`
**Estimated LOC**: ~60

### T01.01 -- Add checkpoint instructions to build_prompt() in process.py

| Field | Value |
|---|---|
| Proposal Reference | Solution 1, Wave 1 |
| Why | `build_prompt()` currently tells the agent "After completing all tasks, STOP immediately" with zero mention of checkpoints. This is the primary root cause — the agent plans only T-numbered tasks and skips `### Checkpoint:` sections. |
| Effort | S |
| Risk | Very Low |
| Risk Drivers | None — additive string changes to prompt template |
| Tier | STANDARD |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Manual inspection of prompt output |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py`

**Steps:**
1. **[PLANNING]** Read `process.py` and locate `build_prompt()` (lines ~169-203). Identify the `## Scope Boundary`, `## Result File`, and prompt assembly sections.
2. **[EXECUTION]** Add a new `## Checkpoints` section to the prompt template between the task execution instructions and the `## Scope Boundary` section:
   ```
   ## Checkpoints
   - After completing all tasks, scan the phase file for `### Checkpoint:` sections
   - For each checkpoint section, extract the path from `Checkpoint Report Path:`
   - Write a structured checkpoint report to that path with verification results per the checkpoint's criteria
   - Write ALL checkpoint files BEFORE writing the result file
   - If no `### Checkpoint:` sections exist, skip this step
   ```
3. **[EXECUTION]** Amend `## Scope Boundary` to replace "After completing all tasks, STOP immediately" with "After completing all tasks AND writing all checkpoint reports, STOP immediately"
4. **[EXECUTION]** Amend `## Result File` section to include "Write result file only after all checkpoint reports are written"
5. **[VERIFICATION]** Run `uv run python -c "from superclaude.cli.sprint.process import ..."` to confirm module loads without error
6. **[VERIFICATION]** Inspect prompt string to confirm checkpoint section is present

**Acceptance Criteria:**
- `build_prompt()` output contains `## Checkpoints` section with 5 instruction lines
- `## Scope Boundary` mentions checkpoint reports
- `## Result File` mentions writing after checkpoints
- Module imports without error
- No other prompt sections modified

**Rollback:** `git checkout -- src/superclaude/cli/sprint/process.py`

---

### T01.02 -- Add _warn_missing_checkpoints() helper to executor.py

| Field | Value |
|---|---|
| Proposal Reference | Solution 1, Wave 1 |
| Why | Even with prompt instructions, the agent may skip checkpoints under context pressure. A warning-only post-phase check provides observability without blocking sprints. |
| Effort | S |
| Risk | Very Low |
| Risk Drivers | None — new function with no side effects on phase status |
| Tier | STANDARD |
| Confidence | [██████████] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Unit test or manual invocation |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`

**Steps:**
1. **[PLANNING]** Read `executor.py` and locate `determine_phase_status()` (~line 1775) and `_check_checkpoint_pass()` (~line 1592). Understand the phase completion flow.
2. **[EXECUTION]** Add a new function `_warn_missing_checkpoints(phase_file: Path, checkpoints_dir: Path, phase_number: int) -> list[str]` that:
   - Reads `phase_file` for lines matching `Checkpoint Report Path:`
   - Extracts each expected checkpoint path
   - Checks if each file exists in `checkpoints_dir`
   - Returns list of missing checkpoint paths
   - Logs a warning for each missing checkpoint via `logger.warning()`
3. **[EXECUTION]** Insert a call to `_warn_missing_checkpoints()` after `determine_phase_status()` returns PASS, before proceeding to the next phase. This is warning-only — it does NOT change the phase status.
4. **[VERIFICATION]** Confirm module loads without error
5. **[VERIFICATION]** Confirm warning is logged when checkpoint file is missing (test with a phase that has a checkpoint path but no file on disk)

**Acceptance Criteria:**
- `_warn_missing_checkpoints()` function exists in `executor.py`
- Function parses `Checkpoint Report Path:` from phase tasklist
- Function checks file existence and logs warnings for missing checkpoints
- Function is called after phase PASS determination
- Function does NOT modify phase status (warning-only)
- Module imports without error

**Rollback:** `git checkout -- src/superclaude/cli/sprint/executor.py`

---

### Checkpoint: End of Phase 1

**Purpose:** Verify Wave 1 prompt-level checkpoint enforcement is functional.
**Checkpoint Report Path:** .dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/checkpoints/CP-CE-P01-END.md
**Verification:**
- `build_prompt()` output contains `## Checkpoints` section
- `_warn_missing_checkpoints()` exists and is callable
- Both `process.py` and `executor.py` load without error
- No regressions in existing sprint tests
**Exit Criteria:**
- Wave 1 complete — agent prompt now explicitly instructs checkpoint writing
- Warning-only observability in place for missing checkpoints

---

## Phase 2 — Post-Phase Checkpoint Enforcement Gate (Wave 2)

**Goal**: Add executor-level checkpoint verification after each phase. Deploy in shadow mode. Ship within 1 week.
**Risk**: Low. New function + enum value + call site. Shadow default means no behavioral change.
**Files**: `checkpoints.py` (NEW), `executor.py`, `models.py`, `logging_.py`
**Estimated LOC**: ~120
**Dependencies**: Phase 1 complete (T01.02 establishes the call site pattern)

### T02.01 -- Create checkpoints.py with extract_checkpoint_paths()

| Field | Value |
|---|---|
| Proposal Reference | Solution 3+4 merged, Wave 2 |
| Why | Both the per-phase gate (Solution 3) and post-sprint manifest (Solution 4) need to parse `Checkpoint Report Path:` from tasklists. A shared module eliminates duplication. |
| Effort | S |
| Risk | Low |
| Risk Drivers | Path resolution edge cases (relative vs absolute paths, missing files) |
| Tier | STANDARD |
| Confidence | [██████████] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Unit test |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/checkpoints.py` (NEW)

**Steps:**
1. **[PLANNING]** Read existing phase tasklists to understand all `Checkpoint Report Path:` patterns (absolute, relative, with/without leading `.dev/`)
2. **[EXECUTION]** Create `checkpoints.py` with:
   - `extract_checkpoint_paths(phase_file: Path, release_dir: Path) -> list[tuple[str, Path]]` — returns list of (checkpoint_name, expected_path) tuples
   - Parses `Checkpoint Report Path:` lines from markdown
   - Resolves relative paths against `release_dir`
   - Returns empty list if no checkpoint sections found
3. **[EXECUTION]** Add `verify_checkpoint_files(paths: list[tuple[str, Path]]) -> list[tuple[str, Path, bool]]` — checks each path exists, returns (name, path, exists) tuples
4. **[VERIFICATION]** Write unit test that parses a sample tasklist with 0, 1, and 2 checkpoint sections
5. **[VERIFICATION]** Confirm module imports cleanly

**Acceptance Criteria:**
- `checkpoints.py` exists in `src/superclaude/cli/sprint/`
- `extract_checkpoint_paths()` correctly parses `Checkpoint Report Path:` from tasklist files
- `verify_checkpoint_files()` checks file existence and returns status per checkpoint
- Handles edge cases: no checkpoint sections, relative paths, missing release_dir
- Unit test passes

**Rollback:** Delete `src/superclaude/cli/sprint/checkpoints.py`

---

### T02.02 -- Add PASS_MISSING_CHECKPOINT to PhaseStatus enum in models.py

| Field | Value |
|---|---|
| Proposal Reference | Solution 3, Wave 2 |
| Why | A distinct status distinguishes "all tasks passed but checkpoints missing" from a clean PASS. Enables downstream consumers to react appropriately. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | Downstream exhaustive match on PhaseStatus — consumers must handle new variant |
| Tier | LIGHT |
| Confidence | [██████████] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py`

**Steps:**
1. **[PLANNING]** Read `models.py` and locate `PhaseStatus` enum. Identify existing members and `is_failure` property.
2. **[EXECUTION]** Add `PASS_MISSING_CHECKPOINT = "pass_missing_checkpoint"` to `PhaseStatus`
3. **[EXECUTION]** Ensure `is_failure` returns `False` for this status (it passed tasks, just missed checkpoints)
4. **[EXECUTION]** Add `checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` to `SprintConfig` (or equivalent config class)
5. **[VERIFICATION]** Confirm module loads without error
6. **[VERIFICATION]** Grep for exhaustive PhaseStatus matches and verify new variant is handled

**Acceptance Criteria:**
- `PASS_MISSING_CHECKPOINT` exists in `PhaseStatus` enum
- `is_failure` returns `False` for this status
- `checkpoint_gate_mode` config field exists with default `"shadow"`
- No existing status matches broken

**Rollback:** `git checkout -- src/superclaude/cli/sprint/models.py`

---

### T02.03 -- Add write_checkpoint_verification() to logging_.py

| Field | Value |
|---|---|
| Proposal Reference | Solution 3, Wave 2 |
| Why | Structured JSONL event for checkpoint verification enables post-hoc analysis of checkpoint completeness across sprints. |
| Effort | XS |
| Risk | Very Low |
| Risk Drivers | None — additive logging method |
| Tier | LIGHT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/logging_.py`

**Steps:**
1. **[PLANNING]** Read `logging_.py` to understand existing event writing patterns (e.g., `phase_complete`, `sprint_complete`)
2. **[EXECUTION]** Add `write_checkpoint_verification(phase: int, expected: list[str], found: list[str], missing: list[str])` method that emits:
   ```json
   {"event": "checkpoint_verification", "phase": 3, "expected": ["CP-P03-END.md"], "found": [], "missing": ["CP-P03-END.md"], "timestamp": "..."}
   ```
3. **[VERIFICATION]** Confirm method signature matches the data `_verify_checkpoints()` in executor.py will produce (from T02.04)

**Acceptance Criteria:**
- `write_checkpoint_verification()` method exists in the sprint logger
- Emits structured JSONL with event type `checkpoint_verification`
- Includes expected, found, and missing checkpoint lists
- Follows existing logging patterns

**Rollback:** `git checkout -- src/superclaude/cli/sprint/logging_.py`

---

### T02.04 -- Wire _verify_checkpoints() into executor.py phase completion flow

| Field | Value |
|---|---|
| Proposal Reference | Solution 3, Wave 2 |
| Why | This is the core enforcement gate. After a phase returns PASS, the executor verifies checkpoint files exist and acts based on `checkpoint_gate_mode`. |
| Effort | M |
| Risk | Low |
| Risk Drivers | Must not break existing phase flow; shadow default ensures safe rollout |
| Tier | STANDARD |
| Confidence | [██████████] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Integration test with mock phase |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`

**Steps:**
1. **[PLANNING]** Read `executor.py` and locate the phase completion flow after `determine_phase_status()` returns PASS (~line 1811+). Also read T01.02's `_warn_missing_checkpoints()` — this task REPLACES that warning-only function with the full gate.
2. **[EXECUTION]** Replace `_warn_missing_checkpoints()` (from T01.02) with `_verify_checkpoints()` that:
   - Imports `extract_checkpoint_paths`, `verify_checkpoint_files` from `checkpoints.py`
   - Calls both functions to get expected and actual checkpoint state
   - Calls `write_checkpoint_verification()` from `logging_.py` to emit JSONL event
   - Based on `checkpoint_gate_mode`:
     - `off`: No action
     - `shadow`: Log JSONL event only (no visible output)
     - `soft`: Log + print warning to stdout
     - `full`: Log + downgrade status to `PASS_MISSING_CHECKPOINT`
3. **[EXECUTION]** Insert call to `_verify_checkpoints()` at the same call site as T01.02's warning function (after phase PASS, before next phase)
4. **[VERIFICATION]** Test with `checkpoint_gate_mode="shadow"` against a phase with known missing checkpoint — confirm JSONL event emitted, no status change
5. **[VERIFICATION]** Test with `checkpoint_gate_mode="full"` — confirm status downgraded to `PASS_MISSING_CHECKPOINT`

**Acceptance Criteria:**
- `_verify_checkpoints()` replaces `_warn_missing_checkpoints()` in executor.py
- Function imports from `checkpoints.py` (shared module from T02.01)
- Emits `checkpoint_verification` JSONL event via logging_.py
- Respects `checkpoint_gate_mode` config: off/shadow/soft/full
- Shadow mode is default — no behavioral change for existing users
- Phase completion flow unchanged for phases with no checkpoint sections

**Dependencies:** T02.01, T02.02, T02.03
**Rollback:** `git checkout -- src/superclaude/cli/sprint/executor.py`

---

### Checkpoint: End of Phase 2

**Purpose:** Verify Wave 2 post-phase checkpoint enforcement gate is functional in shadow mode.
**Checkpoint Report Path:** .dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/checkpoints/CP-CE-P02-END.md
**Verification:**
- `checkpoints.py` exists with `extract_checkpoint_paths()` and `verify_checkpoint_files()`
- `PASS_MISSING_CHECKPOINT` exists in `PhaseStatus` enum
- `checkpoint_gate_mode` config defaults to `"shadow"`
- `write_checkpoint_verification()` emits structured JSONL
- `_verify_checkpoints()` in executor.py wired into phase completion flow
- Shadow mode: JSONL emitted, no status change, no stdout output
- All existing sprint tests pass (no regressions)
**Exit Criteria:**
- Wave 2 deployed in shadow mode — data collection active, zero behavioral change

---

## Phase 3 — Checkpoint Manifest, CLI Verify & Auto-Recovery (Wave 3)

**Goal**: Manifest tracking, CLI verification command, and auto-recovery from evidence artifacts. Ship within 1-2 weeks after Wave 2.
**Risk**: Medium. New module with path resolution, evidence scanning, and template generation.
**Files**: `checkpoints.py` (extend), `commands.py`, `executor.py`, `models.py`
**Estimated LOC**: ~200 incremental
**Dependencies**: Phase 2 complete (`checkpoints.py` exists)

### T03.01 -- Add CheckpointEntry dataclass and manifest types to models.py

| Field | Value |
|---|---|
| Proposal Reference | Solution 4, Wave 3 |
| Why | Structured data types for checkpoint manifest entries enable type-safe manifest operations across the module. |
| Effort | XS |
| Risk | Very Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py`

**Steps:**
1. **[PLANNING]** Read `models.py` to identify existing dataclass/model patterns
2. **[EXECUTION]** Add `CheckpointEntry` dataclass with fields:
   - `phase: int`
   - `name: str` (e.g., "CP-P03-END")
   - `expected_path: Path`
   - `exists: bool`
   - `recovered: bool = False`
   - `recovery_source: str | None = None`
3. **[VERIFICATION]** Confirm module loads without error

**Acceptance Criteria:**
- `CheckpointEntry` dataclass exists in `models.py`
- All fields typed and documented
- Module imports cleanly

**Rollback:** `git checkout -- src/superclaude/cli/sprint/models.py`

---

### T03.02 -- Extend checkpoints.py with build_manifest() and write_manifest()

| Field | Value |
|---|---|
| Proposal Reference | Solution 4, Wave 3 |
| Why | The manifest provides a single source of truth for expected vs actual checkpoint state across an entire sprint, enabling audit and recovery. |
| Effort | M |
| Risk | Low-Medium |
| Risk Drivers | Path resolution across multiple phases; JSON serialization of Path objects |
| Tier | STANDARD |
| Confidence | [██████████] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Unit test |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/checkpoints.py`

**Steps:**
1. **[PLANNING]** Read the existing `checkpoints.py` from Phase 2 (T02.01) to understand the module structure
2. **[EXECUTION]** Add `build_manifest(tasklist_index: Path, release_dir: Path) -> list[CheckpointEntry]` that:
   - Reads the tasklist index to discover all phase tasklist files
   - Calls `extract_checkpoint_paths()` for each phase
   - Returns a list of `CheckpointEntry` objects with `exists` populated from disk state
3. **[EXECUTION]** Add `write_manifest(entries: list[CheckpointEntry], output_path: Path)` that writes `manifest.json` with:
   - Summary counts (total, found, missing, recovered)
   - Per-checkpoint entry details
4. **[VERIFICATION]** Unit test: build manifest from OntRAG R0+R1 tasklist index, verify it identifies all 8 expected checkpoints (7 end-of-phase + 1 mid-phase in P3)

**Acceptance Criteria:**
- `build_manifest()` scans all phase tasklists and returns `CheckpointEntry` list
- `write_manifest()` writes valid JSON with summary + entries
- Handles phases with 0, 1, or 2 checkpoint sections
- Unit test passes

**Rollback:** `git checkout -- src/superclaude/cli/sprint/checkpoints.py`

---

### T03.03 -- Add recover_missing_checkpoints() to checkpoints.py

| Field | Value |
|---|---|
| Proposal Reference | Solution 4, Wave 3 |
| Why | Auto-recovery generates retroactive checkpoints from deliverable evidence files, reducing 30-minute manual recovery to a 1-command operation. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Template quality; evidence file discovery; ensuring recovered checkpoints are clearly marked as auto-recovered |
| Tier | STANDARD |
| Confidence | [██████████] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Integration test against OntRAG R0+R1 sprint output |
| MCP Requirements | None |
| Fallback Allowed | Yes — recovery is opt-in; failure does not block the pipeline |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/checkpoints.py`

**Steps:**
1. **[PLANNING]** Read existing checkpoint files (CP-P01-END through CP-P07-END) to understand the expected format and content structure
2. **[PLANNING]** Read deliverable evidence files (D-*/evidence.md) to understand available source data for recovery
3. **[EXECUTION]** Add `recover_missing_checkpoints(manifest: list[CheckpointEntry], artifacts_dir: Path, phase_tasklists: dict[int, Path]) -> list[CheckpointEntry]` that:
   - Filters manifest for missing checkpoints (`exists == False`)
   - For each missing checkpoint: reads the corresponding phase tasklist for verification criteria
   - Reads relevant deliverable evidence files from `artifacts_dir`
   - Generates a checkpoint file with:
     - `## Note: Auto-Recovered` header marking it as generated, not agent-written
     - `recovered: true` in frontmatter
     - Task summary table populated from evidence files
     - Verification results populated from evidence where available, marked `UNVERIFIED` otherwise
   - Writes the recovered checkpoint to the expected path
   - Returns updated entries with `recovered=True` and `recovery_source` set
4. **[VERIFICATION]** Test against OntRAG R0+R1 sprint: temporarily rename CP-P04-END.md, run recovery, verify output matches the structure of agent-written checkpoints
5. **[VERIFICATION]** Verify recovered checkpoint is clearly marked as auto-recovered

**Acceptance Criteria:**
- `recover_missing_checkpoints()` generates valid checkpoint files from evidence
- Recovered checkpoints clearly marked with `## Note: Auto-Recovered` and `recovered: true`
- Recovery is idempotent — running twice produces same output
- Does not overwrite existing checkpoint files
- Returns updated `CheckpointEntry` list with recovery metadata

**Rollback:** `git checkout -- src/superclaude/cli/sprint/checkpoints.py`

---

### T03.04 -- Add verify-checkpoints CLI subcommand to commands.py

| Field | Value |
|---|---|
| Proposal Reference | Solution 4, Wave 3 |
| Why | CLI command enables operators to audit checkpoint completeness post-sprint and optionally trigger auto-recovery. |
| Effort | S |
| Risk | Low |
| Risk Drivers | CLI argument parsing; path resolution |
| Tier | STANDARD |
| Confidence | [██████████] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Manual CLI invocation |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py`

**Steps:**
1. **[PLANNING]** Read `commands.py` to understand existing CLI subcommand patterns (Click/Typer/argparse)
2. **[EXECUTION]** Add `verify-checkpoints` subcommand with:
   - Required arg: `output-dir` (path to sprint output directory)
   - Optional flag: `--recover` (trigger auto-recovery for missing checkpoints)
   - Optional flag: `--json` (output manifest as JSON to stdout)
   - Default behavior: print table of expected vs actual checkpoint status
3. **[EXECUTION]** Wire the subcommand to call:
   - `build_manifest()` from `checkpoints.py`
   - `write_manifest()` to save `manifest.json`
   - Optionally `recover_missing_checkpoints()` if `--recover` flag is set
4. **[VERIFICATION]** Run `superclaude sprint verify-checkpoints <ontrag-output-dir>` and verify output lists all 8 checkpoints with correct status
5. **[VERIFICATION]** Run with `--json` and verify valid JSON output

**Acceptance Criteria:**
- `superclaude sprint verify-checkpoints <dir>` subcommand exists
- Prints table of checkpoint status (expected, found, missing)
- `--recover` flag triggers auto-recovery
- `--json` flag outputs machine-readable manifest
- Works retroactively on sprints run before this feature existed

**Rollback:** `git checkout -- src/superclaude/cli/sprint/commands.py`

---

### T03.05 -- Wire manifest build/verify into executor.py sprint lifecycle

| Field | Value |
|---|---|
| Proposal Reference | Solution 4, Wave 3 |
| Why | Automatic manifest generation at sprint start/end provides continuous checkpoint tracking without requiring manual CLI invocation. |
| Effort | S |
| Risk | Low |
| Risk Drivers | Must not slow down sprint start or end noticeably |
| Tier | STANDARD |
| Confidence | [██████████] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Integration test |
| MCP Requirements | None |
| Fallback Allowed | Yes — manifest is observability, not gating |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`

**Steps:**
1. **[PLANNING]** Read `executor.py` and locate sprint start and sprint end events in the execution flow
2. **[EXECUTION]** At sprint start: call `build_manifest()` to generate initial manifest (all checkpoints expected, none found)
3. **[EXECUTION]** At sprint end: call `build_manifest()` again to update with final state, then `write_manifest()` to save `manifest.json`
4. **[EXECUTION]** Add `checkpoint_manifest` JSONL event at sprint end summarizing total/found/missing counts
5. **[VERIFICATION]** Run a sprint and verify `manifest.json` appears in the output directory with correct data

**Acceptance Criteria:**
- Manifest is built at sprint start (expectation tracking)
- Manifest is finalized and written at sprint end
- `manifest.json` written to sprint output directory
- `checkpoint_manifest` JSONL event emitted at sprint end
- Sprint execution time not noticeably affected

**Dependencies:** T03.02
**Rollback:** `git checkout -- src/superclaude/cli/sprint/executor.py`

---

### Checkpoint: End of Phase 3

**Purpose:** Verify Wave 3 manifest, CLI, and auto-recovery are functional.
**Checkpoint Report Path:** .dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/checkpoints/CP-CE-P03-END.md
**Verification:**
- `build_manifest()` correctly identifies all checkpoints across a multi-phase sprint
- `recover_missing_checkpoints()` generates valid, clearly-marked recovered checkpoints
- `superclaude sprint verify-checkpoints` CLI works against OntRAG R0+R1 output
- Manifest auto-generated at sprint end
- All existing sprint tests pass
**Exit Criteria:**
- Waves 1-3 complete — prevention, detection, and remediation layers all operational

---

## Phase 4 — Tasklist-Level Checkpoint Normalization (Wave 4)

**Goal**: Eliminate the structural root cause by making checkpoints structurally identical to tasks in all future tasklists. Ship with next release cycle.
**Risk**: Low-Medium. Breaking change for existing tasklists — applies to new generation only.
**Files**: `SKILL.md` (sc-tasklist-protocol)
**Estimated LOC**: ~200
**Dependencies**: Phases 1-3 complete (Waves 1-3 provide interim coverage for existing tasklists)
**Note**: This is a breaking change. Existing tasklists retain `### Checkpoint:` headings; Waves 1-3 handle them. New tasklists generated after this change will use `### T<PP>.<TT> -- Checkpoint:` format.

### T04.01 -- Update sc-tasklist-protocol SKILL.md checkpoint generation rules

| Field | Value |
|---|---|
| Proposal Reference | Solution 2, Wave 4 |
| Why | The `### Checkpoint:` heading pattern is structurally invisible to the agent's task scanner which only recognizes `### T<NN>.<NN>` patterns. Converting checkpoints to task entries eliminates this structural mismatch permanently. |
| Effort | M |
| Risk | Low-Medium |
| Risk Drivers | Numbering cascade — checkpoint tasks must not collide with existing task numbers; must appear in correct execution order |
| Tier | STANDARD |
| Confidence | [██████████] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Generate a test tasklist and verify format |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

**Steps:**
1. **[PLANNING]** Read `SKILL.md` and locate the section governing checkpoint section generation. Identify how task numbering is assigned.
2. **[PLANNING]** Read Phase 3 tasklist (the problematic one) and Phase 4 tasklist (successful) to understand the current checkpoint format vs task format
3. **[EXECUTION]** Add/modify the checkpoint generation rules to produce task entries instead of bare checkpoint sections:
   - Mid-phase checkpoints: `### T<PP>.<next_num> -- Checkpoint: <checkpoint_name>`
   - End-of-phase checkpoints: `### T<PP>.<last_num> -- Checkpoint: End of Phase <PP>`
   - Each checkpoint task gets a metadata table (same fields as regular tasks: Effort=XS, Risk=Low, Tier=LIGHT)
   - Each checkpoint task gets Steps (1. Read all evidence files, 2. Verify each criterion, 3. Write checkpoint report to path, 4. Record pass/fail)
   - Each checkpoint task gets Acceptance Criteria (checkpoint file exists at specified path, all verification criteria evaluated, exit criteria documented)
4. **[EXECUTION]** Add rule: checkpoint tasks MUST be the last task(s) in the phase — no regular tasks after a checkpoint task
5. **[EXECUTION]** Add rule: end-of-phase checkpoint is always the absolute last `### T<PP>.<NN>` entry; mid-phase checkpoints appear at the specified task boundary
6. **[VERIFICATION]** Manually trace through a hypothetical Phase 3 generation to confirm output would be:
   - T03.01-T03.05 (regular tasks)
   - T03.06 (mid-phase checkpoint → checkpoint task)
   - T03.07 (regular task — validate_gemini_key.py)
   - T03.08 (end-of-phase checkpoint → checkpoint task)

**Acceptance Criteria:**
- SKILL.md checkpoint generation rules produce `### T<PP>.<NN> -- Checkpoint:` entries
- Checkpoint tasks include metadata table, steps, acceptance criteria, and deliverable references
- End-of-phase checkpoint is always the last task in the phase
- Mid-phase checkpoints appear at the correct position in task sequence
- Numbering cascade is correct (no gaps, no collisions)

**Rollback:** `git checkout -- src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

---

### T04.02 -- Add checkpoint task validation to Sprint Compatibility Self-Check

| Field | Value |
|---|---|
| Proposal Reference | Solution 2, Wave 4 |
| Why | Self-check validation catches numbering and formatting errors in checkpoint tasks before the tasklist is written, preventing malformed output. |
| Effort | S |
| Risk | Low |
| Risk Drivers | False positives if validation rule is too strict |
| Tier | STANDARD |
| Confidence | [██████████] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Run self-check against generated tasklist |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

**Steps:**
1. **[PLANNING]** Read the Sprint Compatibility Self-Check section of SKILL.md to understand existing validation rules
2. **[EXECUTION]** Add validation rule: "Every `### Checkpoint:` section in the source roadmap/spec MUST produce a corresponding `### T<PP>.<NN> -- Checkpoint:` task entry in the output tasklist"
3. **[EXECUTION]** Add validation rule: "End-of-phase checkpoint task MUST be the last `### T<PP>.<NN>` entry in each phase"
4. **[EXECUTION]** Add validation rule: "Checkpoint task metadata table MUST include `Checkpoint Report Path:` in the deliverables or steps"
5. **[VERIFICATION]** Mentally trace through the self-check against the OntRAG Phase 3 tasklist (old format) — should flag 2 violations

**Acceptance Criteria:**
- Three new validation rules added to Sprint Compatibility Self-Check
- Rules catch: missing checkpoint task entries, misplaced checkpoint tasks, missing report path references
- Rules do not produce false positives on phases with no checkpoint sections

**Dependencies:** T04.01
**Rollback:** `git checkout -- src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

---

### T04.03 -- Update deliverable registry guidance for checkpoint deliverables

| Field | Value |
|---|---|
| Proposal Reference | Solution 2, Wave 4 |
| Why | Checkpoint tasks produce deliverables (the checkpoint report files). The deliverable registry guidance must include checkpoint files as a deliverable type. |
| Effort | XS |
| Risk | Very Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |

**Target File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

**Steps:**
1. **[PLANNING]** Read the deliverable registry/ID section of SKILL.md
2. **[EXECUTION]** Add checkpoint report as a recognized deliverable type:
   - Convention: `D-CP<PP>[-MID]` (e.g., `D-CP03` for end-of-phase, `D-CP03-MID` for mid-phase)
   - Default path: `checkpoints/CP-P<PP>-END.md` or `checkpoints/CP-P<PP>-<NAME>.md`
3. **[VERIFICATION]** Confirm deliverable ID convention does not collide with existing D-NNNN IDs

**Acceptance Criteria:**
- Checkpoint deliverable type documented in SKILL.md deliverable registry
- Naming convention (D-CP*) does not collide with existing D-NNNN patterns
- Default paths follow existing checkpoint directory structure

**Rollback:** `git checkout -- src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

---

### Checkpoint: End of Phase 4

**Purpose:** Verify Wave 4 tasklist normalization is complete and all 4 waves are operational.
**Checkpoint Report Path:** .dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/checkpoints/CP-CE-P04-END.md
**Verification:**
- SKILL.md checkpoint generation rules produce `### T<PP>.<NN> -- Checkpoint:` task entries
- Sprint Compatibility Self-Check catches missing/misplaced checkpoint tasks
- Deliverable registry includes checkpoint deliverable type
- No regressions: existing tasklists (old format) still work with Waves 1-3 coverage
**Exit Criteria:**
- All 4 waves complete — three-layer defense architecture fully operational:
  - Layer 1 (Prevention): Prompt instructions (Wave 1) + structural normalization (Wave 4)
  - Layer 2 (Detection): Post-phase enforcement gate (Wave 2)
  - Layer 3 (Remediation): Manifest + CLI + auto-recovery (Wave 3)
- Root cause triple failure chain fully addressed:
  - Cause 1 (No prompt instructions): FIXED by Wave 1
  - Cause 2 (Structural mismatch): ELIMINATED by Wave 4
  - Cause 3 (No enforcement): FIXED by Waves 2+3

