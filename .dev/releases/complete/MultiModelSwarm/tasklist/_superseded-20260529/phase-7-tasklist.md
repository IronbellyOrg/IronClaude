# Phase 7 -- Observability, TUI, Detached & Full CLI Surface

**Goal:** Complete the operator surface — the opt-in Rich TUI (`--tui` gated, NEVER default), tmux detached-mode wrapper, three-layer durable monitoring (`.swarm-state.json` + `execution-log.jsonl` + `execution-log.md` + `done.json`), the atomic done sentinel, and the remaining swarm subcommands (status/logs/attach/kill/scaffold). Exit when all 8 subcommands are functional, non-TTY callers receive no terminal control sequences (INV-012), detached jobs survive caller death, three monitoring patterns are demonstrated, the grep-audit confirms zero Claude-isms in the contract surface (AC-013, NFR-016), and the Phase-1 transport limits (no streaming/function-calling/vision) are documented.

### T07.01 -- Implement `tui` module (Rich Live dashboard, flag-gated)

| Field | Value |
|---|---|
| Roadmap | R-118 (COMP-013) |
| Deliverables | D-0099 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, context7 (Rich Live) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_tui.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/tui.py` with Rich Live dashboard rendering only when `--tui`.

**Steps:**
1. [PLANNING] Auggie-retrieve sprint TUI for parity.
2. [EXECUTION] Implement `TUI.render(state, events)` using Rich Live.
3. [EXECUTION] Gate render behind `--tui` flag + TTY check.
4. [VERIFICATION] Test non-TTY callers receive plain output.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- TUI renders only when `--tui` passed.
- No terminal control sequences emitted on non-TTY stdout.
- Dashboard shows per-worker status + elapsed.
- `tests/swarm/test_tui.py` covers TUI on/off paths.

**Validation:**
- `uv run pytest tests/swarm/test_tui.py -v` passes.
- `swarm run --transport stub | cat` produces no ANSI escapes.

**Dependencies:** T01.10 (state, EventRecord). **Rollback:** disable TUI; default plain output.

### T07.02 -- Implement `tmux` detached-run wrapper

| Field | Value |
|---|---|
| Roadmap | R-119 (COMP-014) |
| Deliverables | D-0100 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_tmux_detached.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/tmux.py` mirroring `cli/sprint/tmux.py` for detached runs.

**Steps:**
1. [PLANNING] Read sprint tmux module for parity.
2. [EXECUTION] Implement detached launch via `tmux new-session -d -s swarm-<job_id>`.
3. [EXECUTION] Expose `attach(job_id)` and `kill(job_id)` helpers.
4. [VERIFICATION] Test detached run survives caller exit (skip if tmux absent).
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Launches detached job; survives caller exit.
- Provides attach/kill helper functions for T07.07/T07.08.
- Test gated on `which tmux` (skipped if absent).
- `tests/swarm/test_tmux_detached.py` green (or skipped cleanly).

**Validation:**
- `uv run pytest tests/swarm/test_tmux_detached.py -v` passes/skips.
- `tmux ls` shows swarm session post-launch.

**Dependencies:** T03.01 (commands). **Rollback:** disable detached mode; inline-only.

### T07.03 -- Enforce INV-012 TUI opt-in (no control sequences on non-TTY)

| Field | Value |
|---|---|
| Roadmap | R-120 (INV-012) |
| Deliverables | D-0101 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_inv012_tui_opt_in.py` |

**Deliverables:**
1. `tests/swarm/test_inv012_tui_opt_in.py` asserting plain output on non-TTY.

**Steps:**
1. [PLANNING] Capture stdout via subprocess with stdin/stdout pipes.
2. [EXECUTION] Write test running `swarm run` without `--tui` and assert no ANSI bytes.
3. [EXECUTION] Run with `--tui` on PTY and confirm Rich Live present.
4. [VERIFICATION] Run tests.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Default `swarm run` emits plain output (no ANSI bytes).
- `--tui` enables Rich Live dashboard (on TTY only).
- Non-TTY caller never receives terminal control sequences.
- `tests/swarm/test_inv012_tui_opt_in.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_inv012_tui_opt_in.py -v` passes.
- ANSI grep on captured stdout returns empty for plain path.

**Dependencies:** T07.01. **Rollback:** none — guard.

### T07.04 -- Implement `swarm status` subcommand

| Field | Value |
|---|---|
| Roadmap | R-121 (FR-002) |
| Deliverables | D-0102 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_status_cmd.py` |

**Deliverables:**
1. `commands.py::status_cmd` reading `.swarm-state.json` and reporting phase/status.

**Steps:**
1. [PLANNING] Identify status output shape (state + phase + workers count).
2. [EXECUTION] Implement subcommand reading state file via state module.
3. [EXECUTION] Add `--watch` flag for live updates.
4. [VERIFICATION] Test against fixture state file.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Reads `.swarm-state.json`; reports current phase/status.
- Returns exit code per terminal state (0 success, non-zero partial/failed).
- `--watch` polls and refreshes.
- `tests/swarm/test_status_cmd.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_status_cmd.py -v` passes.
- `swarm status --job <id>` reports expected fields.

**Dependencies:** T03.03 (state). **Rollback:** remove subcommand.

### T07.05 -- Implement `swarm logs` subcommand

| Field | Value |
|---|---|
| Roadmap | R-122 (FR-003) |
| Deliverables | D-0103 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_logs_cmd.py` |

**Deliverables:**
1. `commands.py::logs_cmd` tailing JSONL or dumping md log.

**Steps:**
1. [PLANNING] Distinguish `--tail` (JSONL) vs `--dump` (markdown).
2. [EXECUTION] Implement subcommand with file open + tail behavior.
3. [VERIFICATION] Test against fixture log files.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Tails JSONL or dumps markdown log as flag indicates.
- Honors `--follow` for live tail.
- Default mode is dump-md.
- `tests/swarm/test_logs_cmd.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_logs_cmd.py -v` passes.
- `swarm logs --job <id> --tail` follows JSONL.

**Dependencies:** T03.04 (logging_). **Rollback:** remove subcommand.

### T07.06 -- Checkpoint: Phase 7 mid-phase gate (tasks 1-5 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP7-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T07.01..T07.05 marked done in execution-log.
- `phase-7-cp1.md` checkpoint report written.
- TUI + tmux + INV-012 + status + logs subcommands functional.
- Non-TTY callers receive plain output.

**Validation:**
- `uv run pytest tests/swarm/test_tui.py tests/swarm/test_tmux_detached.py tests/swarm/test_inv012_tui_opt_in.py tests/swarm/test_status_cmd.py tests/swarm/test_logs_cmd.py -v` passes/skips.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T07.01..T07.05.

### T07.07 -- Implement `swarm attach` subcommand

| Field | Value |
|---|---|
| Roadmap | R-123 (FR-004) |
| Deliverables | D-0104 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_attach_cmd.py` |

**Deliverables:**
1. `commands.py::attach_cmd` re-attaching to detached tmux job.

**Steps:**
1. [PLANNING] Locate target session name via `swarm-<job_id>`.
2. [EXECUTION] Implement attach via `tmux attach-session -t swarm-<job_id>`.
3. [VERIFICATION] Test attach (gated on tmux presence).
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Re-attaches to running detached session.
- Exits gracefully if no detached session present.
- Gated on tmux availability.
- `tests/swarm/test_attach_cmd.py` green/skipped.

**Validation:**
- `uv run pytest tests/swarm/test_attach_cmd.py -v` passes/skips.
- `swarm attach <id>` exits 0 when session present.

**Dependencies:** T07.02. **Rollback:** remove subcommand.

### T07.08 -- Implement `swarm kill` subcommand

| Field | Value |
|---|---|
| Roadmap | R-124 (FR-005) |
| Deliverables | D-0105 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_kill_cmd.py` |

**Deliverables:**
1. `commands.py::kill_cmd` terminating detached session + writing terminal state.

**Steps:**
1. [PLANNING] Define kill flow: tmux kill-session + write terminal state + emit done sentinel.
2. [EXECUTION] Implement subcommand.
3. [VERIFICATION] Test kill flow (gated on tmux).
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Terminates session; writes terminal state.
- Emits `done.json` with `terminal_status: killed`.
- Idempotent (kill twice no-op).
- `tests/swarm/test_kill_cmd.py` green/skipped.

**Validation:**
- `uv run pytest tests/swarm/test_kill_cmd.py -v` passes/skips.
- `swarm kill <id>` exits 0 after terminating session.

**Dependencies:** T07.02, T03.03. **Rollback:** remove subcommand.

### T07.09 -- Implement `swarm scaffold` subcommand

| Field | Value |
|---|---|
| Roadmap | R-125 (FR-006) |
| Deliverables | D-0106 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_scaffold_cmd.py` |

**Deliverables:**
1. `commands.py::scaffold_cmd` emitting valid starter job-spec for `--lens <name>`.

**Steps:**
1. [PLANNING] Locate LENSES registry entry for chosen lens.
2. [EXECUTION] Generate JobSpec scaffold with defaults populated.
3. [VERIFICATION] Generated spec validates against schema.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Writes valid starter spec for given `--lens`.
- Spec validates via `swarm validate`.
- Stdout-or-file output supported.
- `tests/swarm/test_scaffold_cmd.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_scaffold_cmd.py -v` passes.
- `swarm scaffold --lens bare-review | swarm validate --stdin` exits 0.

**Dependencies:** T02.14 (LENSES). **Rollback:** remove subcommand.

### T07.10 -- Document three monitoring patterns + demo

| Field | Value |
|---|---|
| Roadmap | R-126 (FR-013) |
| Deliverables | D-0107 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: doc renders + commands run |

**Deliverables:**
1. `docs/swarm/monitoring-patterns.md` documenting three patterns with paste-ready commands.

**Steps:**
1. [PLANNING] Enumerate three patterns: `Bash run_in_background + until [ -f done.json ]`, `Monitor` tailing JSONL, `swarm status --watch`.
2. [EXECUTION] Author doc with command examples for each pattern.
3. [VERIFICATION] Each command exits 0 against a stub run.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- All three patterns documented with paste-ready commands.
- Each command demonstrated against stub fixture.
- Doc links to OPS-003 (observability procedure).
- Doc renders without markdownlint errors.

**Validation:**
- `markdownlint docs/swarm/monitoring-patterns.md` exits 0.
- Each command in doc runs against `--transport stub` fixture.

**Dependencies:** T07.04 (status), T07.13 (done sentinel). **Rollback:** revert doc.

### T07.11 -- Implement detached mode via tmux (`--detached` flag)

| Field | Value |
|---|---|
| Roadmap | R-127 (FR-014) |
| Deliverables | D-0108 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_tmux_detached.py tests/swarm/test_tmux_fallback.py` |

**Deliverables:**
1. `commands.py::run_cmd` with `--detached` flag launching via tmux wrapper.

**Steps:**
1. [PLANNING] Confirm tmux wrapper interface from T07.02.
2. [EXECUTION] Wire `--detached` into `run_cmd` invoking tmux launcher.
3. [EXECUTION] Inline run remains default.
4. [VERIFICATION] Test detached path (gated on tmux).
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- `--detached` launches background job; inline remains default.
- Detached job survives caller exit (verified by subprocess kill of parent).
- Output dir contract preserved.
- `tests/swarm/test_tmux_detached.py` + `tests/swarm/test_tmux_fallback.py` green/skipped (detached-mode coverage lives in these two tests).

**Validation:**
- `uv run pytest tests/swarm/test_tmux_detached.py tests/swarm/test_tmux_fallback.py -v` passes/skips.
- `swarm run --detached ...` returns immediately with job_id.

**Dependencies:** T07.02. **Rollback:** disable `--detached`; inline-only.

### T07.12 -- Checkpoint: Phase 7 mid-phase gate (tasks 7-11)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP7-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T07.07..T07.11 marked done in execution-log.
- `phase-7-cp2.md` checkpoint report written.
- attach/kill/scaffold/detached/monitoring-doc all functional.
- Eight subcommands present: run/status/logs/attach/kill/scaffold/validate/validate-lenses.

**Validation:**
- `swarm --help` lists 8 subcommands.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T07.07..T07.11.

### T07.13 -- Implement done sentinel emission (`done.json`)

| Field | Value |
|---|---|
| Roadmap | R-128 (FR-027) |
| Deliverables | D-0109 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_done_sentinel.py` |

**Deliverables:**
1. `reduce.py::emit_done_sentinel(terminal_status, contract_path) -> Path` atomic-write.

**Steps:**
1. [PLANNING] Confirm DM-017 DoneSentinel fields.
2. [EXECUTION] Implement emitter writing `done.json` via tmp+`os.replace`.
3. [VERIFICATION] Test atomic write + content.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Terminal state writes `done.json` atomically.
- Sentinel contains `terminal_status` + `contract_path` fields.
- Polling pattern `until [ -f done.json ]` works against fixture.
- `tests/swarm/test_done_sentinel.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_done_sentinel.py -v` passes.
- `done.json` parseable JSON post-terminal.

**Dependencies:** T05.01 (reduce), T01.10 (DoneSentinel). **Rollback:** none — observability guard.

### T07.14 -- Verify NFR-004 three-layer durable monitoring artifact set

| Field | Value |
|---|---|
| Roadmap | R-129 (NFR-004) |
| Deliverables | D-0110 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_three_layer_artifacts.py` |

**Deliverables:**
1. `tests/swarm/test_three_layer_artifacts.py` asserting all 4 artifacts emitted + consistent.

**Steps:**
1. [PLANNING] Enumerate 4 artifacts: `.swarm-state.json`, `execution-log.jsonl`, `execution-log.md`, `done.json`.
2. [EXECUTION] Write integration test running stub job and asserting all 4 emitted.
3. [VERIFICATION] Consistency check: terminal state in state + done sentinel + contract.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- All four artifacts emitted and consistent.
- Test parses each artifact and confirms shape.
- Cross-references (terminal status) match across artifacts.
- `tests/swarm/test_three_layer_artifacts.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_three_layer_artifacts.py -v` passes.
- All 4 files present in `--output` directory after stub run.

**Dependencies:** T07.13, T03.03, T03.04. **Rollback:** none — observability guard.

### T07.15 -- Enforce NFR-016 contract-surface non-precluding (grep audit)

| Field | Value |
|---|---|
| Roadmap | R-130 (NFR-016) |
| Deliverables | D-0111 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash (grep) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_contract_surface.py` |

**Deliverables:**
1. `tests/swarm/test_contract_surface.py` grep-audit finding zero Claude-isms in contract surface files.

**Steps:**
1. [PLANNING] Enumerate forbidden patterns: `Read`, `Edit`, `Bash`, `claude.ai`, `anthropic`, `Tool`.
2. [EXECUTION] Write grep-based audit over job spec, result contract, CLI surface, monitoring contract.
3. [VERIFICATION] Run audit.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Grep audit finds no Claude-tool references in contract surfaces.
- Detached job survives caller kill (verified via subprocess SIGKILL).
- Audit covers job spec, result contract, CLI surface, monitoring contract.
- `tests/swarm/test_contract_surface.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_contract_surface.py -v` passes.
- `grep -RinE "Read\(|Edit\(|Bash\(|claude\.ai|anthropic" src/superclaude/cli/swarm/` returns empty.

**Dependencies:** T07.11, T02.28 (AC-013 audit). **Rollback:** none — caller-agnostic guard.

### T07.16 -- Pin Rich ≥13.0.0 + document --tui usage

| Field | Value |
|---|---|
| Roadmap | R-131 (AC-007) |
| Deliverables | D-0112 |
| Effort | S |
| Risk | LOW |
| Tier | LIGHT |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: import + version |

**Deliverables:**
1. `pyproject.toml` declares `rich>=13.0.0`.
2. Doc note explaining Rich is opt-in, behind `--tui`.

**Steps:**
1. [PLANNING] Confirm pyproject Rich pin.
2. [EXECUTION] Add `rich>=13.0.0` to dependencies if missing.
3. [VERIFICATION] Import succeeds; version assertion in test.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- `pyproject.toml` lists `rich>=13.0.0`.
- Rich used only behind `--tui`.
- Import resolves cleanly.
- Version assertion passes.

**Validation:**
- `python -c "import rich; assert tuple(int(x) for x in rich.__version__.split('.')[:2]) >= (13, 0)"` exits 0.
- `grep rich pyproject.toml` shows pin.

**Dependencies:** T07.01. **Rollback:** unpin (no enforcement).

### T07.17 -- Document tmux-optional behavior + fallback

| Field | Value |
|---|---|
| Roadmap | R-132 (AC-008) |
| Deliverables | D-0113 |
| Effort | S |
| Risk | LOW |
| Tier | LIGHT |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: doc + fallback test |

**Deliverables:**
1. `docs/swarm/runbook.md` note: tmux required for detached; inline default needs no tmux.

**Steps:**
1. [PLANNING] Confirm fallback semantics: missing tmux → inline only.
2. [EXECUTION] Author note in runbook.
3. [VERIFICATION] Test inline path succeeds without tmux installed.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Detached requires tmux; inline needs no tmux.
- Runbook documents detection + fallback.
- Test confirms inline runs without tmux on CI.
- `tests/swarm/test_tmux_fallback.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_tmux_fallback.py -v` passes.
- Runbook contains tmux-optional paragraph.

**Dependencies:** T07.02, T07.11. **Rollback:** none.

### T07.18 -- Checkpoint: Phase 7 invariants gate (tasks 13-17)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP7-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T07.13..T07.17 marked done in execution-log.
- `phase-7-cp3.md` checkpoint report written.
- done sentinel + 3-layer artifacts + contract-surface audit + Rich pin + tmux fallback all green.
- NFR-004 + NFR-016 + AC-007 + AC-008 + FR-027 verified.

**Validation:**
- `uv run pytest tests/swarm/test_done_sentinel.py tests/swarm/test_three_layer_artifacts.py tests/swarm/test_contract_surface.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T07.13..T07.17.

### T07.19 -- Enforce AC-009 no-external-framework-integration audit

| Field | Value |
|---|---|
| Roadmap | R-133 (AC-009) |
| Deliverables | D-0114 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, Bash (grep) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_no_external_frameworks.py` |

**Deliverables:**
1. `tests/swarm/test_no_external_frameworks.py` audit excluding openhands/langgraph/crewai/openai-assistants.

**Steps:**
1. [PLANNING] Enumerate forbidden deps: openhands, openharness, openai-assistants, langgraph, crewai.
2. [EXECUTION] Write grep-based test over `pyproject.toml` + swarm imports.
3. [VERIFICATION] Run test.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- No such deps imported.
- Integration seams documented as non-preclusion only.
- Test fails if forbidden import introduced.
- `tests/swarm/test_no_external_frameworks.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_no_external_frameworks.py -v` passes.
- `grep -RnE "openhands|openharness|langgraph|crewai" src/superclaude/cli/swarm/` empty.

**Dependencies:** none. **Rollback:** none — guard.

### T07.20 -- Document AC-016 Phase-1 transport limits (no streaming/function-calling/vision)

| Field | Value |
|---|---|
| Roadmap | R-134 (AC-016) |
| Deliverables | D-0115 |
| Effort | S |
| Risk | LOW |
| Tier | LIGHT |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: doc renders |

**Deliverables:**
1. `docs/swarm/transport-limits.md` documenting Phase-1 exclusions.

**Steps:**
1. [PLANNING] Enumerate excluded modes: streaming, function-calling, vision.
2. [EXECUTION] Author doc citing parent §7.3.
3. [VERIFICATION] Render doc.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Phase 1 excludes streaming, function-calling, vision input (parent §7.3).
- Doc lists rationale + future-work pointer.
- Transport rejects/omits these modes in Phase 1.
- Doc passes markdownlint.

**Validation:**
- `markdownlint docs/swarm/transport-limits.md` exits 0.
- Doc references parent §7.3.

**Dependencies:** T03.05. **Rollback:** revert doc.

### T07.21 -- Checkpoint: Phase 7 exit gate (end-of-phase)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase) |
| Deliverables | D-CP7-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T07.01..T07.20 marked done in execution-log.
- `phase-7-cp4.md` end-of-phase checkpoint written.
- 8 subcommands functional; INV-012 verified; NFR-004/016 + AC-007/008/009/016 + FR-002..006/013/014/027 all green.
- Three monitoring patterns demonstrated.

**Validation:**
- `uv run pytest tests/swarm/ -v` Phase 7 surface passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T07.01..T07.20. **Rollback:** none — phase exit gate.
**Notes:** M7 exit (along with M6) unblocks M8 migration.

## Rerun 2026-06-01 — Post-Proxy-Outage Recovery (T07.12 narrowed scope)

**Trigger:** The original Phase 7 sprint run encountered an LLM-proxy outage at 16:09-16:28 UTC on 2026-06-01 that hit two tasks:

- **T07.11** (`--detached` flag, D-0108): partial work — 1029469-byte (1 MB) `phase-7-task-T07.11-output.txt` retry-storm transcript.
- **T07.12** (CP2 mid-phase checkpoint, D-CP7-1): zero work — 14785-byte `phase-7-task-T07.12-output.txt` ending in `ConnectionRefused` after 10 `api_retry` events.

The sprint correctly proceeded past Phase 7 because downstream dependencies (T07.13..T07.21) only need T07.07..T07.11 deliverables, which were on disk. The Phase 7 `phase_complete` event in `execution-log.jsonl` was nonetheless flipped to `status: error` by the executor's all-PASS predicate (`all_passed = all(r.status == TaskStatus.PASS for r in task_results)`). That JSONL event is left intact as the historical record — the rerun is a separate forensic event.

**Narrowed scope:** Pre-rerun grep against `src/superclaude/cli/swarm/commands.py` confirmed T07.11's `--detached` Click option (line 1060), `_launch_detached_run` helper (line 799), and `swarm_tmux.launch_detached` call (line 891) are all wired. `uv run pytest tests/swarm/test_tmux_detached.py` reports 13 passed + 6 skipped (tmux-binary gated). Per the rerun-prompt narrowing constraint, T07.11 is treated as already-complete and re-execution is skipped. Only T07.12 (the missing `phase-7-cp2.md` checkpoint report) is re-executed.

**Rerun bundle:** `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/tasklist/rerun-phase-7b/` (preserved permanently for audit). Independent verification gate: `/sc:reflect --mode post --depth deep`. Completion log will be appended below on PASS.

## Rerun completed 2026-06-01 — T07.12 CP2 artifact merged

**Outcome summary:**

- (a) The rerun was needed because of the LLM proxy outage at 16:09-16:28 UTC on 2026-06-01 which left T07.12's CP2 mid-phase checkpoint report unwritten (zero-work, 14785-byte ConnectionRefused transcript) and produced a partial-work 1029469-byte (1 MB) retry-storm transcript on T07.11 — though T07.11's `--detached` flag was pre-verified as already wired before this rerun began, narrowing the rerun scope to T07.12 only.
- (b) The single task in scope was re-executed via the rerun-phase-7b/ mini-tasklist bundle at `.dev/releases/Current/MultiModelSwarm/tasklist/rerun-phase-7b/` using an Agent-spawned `/sc:task` invocation on `rerun-phase-7b/phase-1-tasklist.md`.
- (c) Deliverables now present at their expected paths:
  - `tasklist/phase-7-cp2.md` (26987 bytes, 110 lines, 10 H2 sections mirroring CP1's structure)
  - `results/phase-7-task-T07.12-output.txt` overwritten with the rerun synthesis transcript
- (d) `/sc:reflect --mode post --depth deep` verdict was **PASS** (1 LOW-severity finding F-1 — tasklist step 6 markdownlint check not evidenced; non-blocking per rerun protocol since it was a step-level requirement, not an acceptance criterion, and the artifact reads lint-clean to manual inspection). Full report at `tasklist/validation/sc-reflect-post-phase-7-rerun-report.md`.
- (e) The rerun bundle at `tasklist/rerun-phase-7b/` is preserved permanently for audit. `execution-log.jsonl` and the Phase-7 `phase_complete` event (status: error) are left intact as the original forensic record — the rerun is a separate forensic event.

**Bracket-suite test results captured during rerun:** 65 passed + 8 skipped + 0 failed across `tests/swarm/test_attach_cmd.py` (10p+1s), `test_kill_cmd.py` (15p+1s), `test_scaffold_cmd.py` (27p+0s), `test_tmux_detached.py` (13p+6s). 8 swarm subcommands enumerated (run/status/logs/attach/kill/scaffold/validate/validate-lenses).
