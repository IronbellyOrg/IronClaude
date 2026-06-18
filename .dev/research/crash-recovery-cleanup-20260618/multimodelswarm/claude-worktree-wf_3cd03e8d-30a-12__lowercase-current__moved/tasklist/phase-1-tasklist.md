# Phase 1 -- Foundation, Module Shape & Data Models

**Goal:** Stand up the `superclaude swarm` CLI verb and the `cli/swarm/` package mirroring `cli/sprint/`, register the Click group, and define every dataclass the pipeline serializes (JobSpec, WorkerSpec, TargetSpec, TransportSpec, PromptSpec, NormalizationSpec, OutputSpec, StatusPolicy, RuntimeSpec, LensEntry, ResolvedLensEntry, ResultContract, WorkerResult, SwarmState, EventRecord, Manifest, DoneSentinel, Artifacts, CallerInfo, CallerMetadata) with lossless JSON round-trip. Exit when `superclaude swarm --help` lists the group, contract/source-of-truth records (ResultContract, Manifest, DoneSentinel) are frozen while accumulator/state records are mutable by design (F-P1-3), all 20 data models round-trip serializable, OQ-006/008/009 owners are assigned, and `make verify-sync` is green.

### T01.01 -- Enforce Python ≥3.10 + UV mandate for swarm operations

| Field | Value |
|---|---|
| Roadmap | R-001 (AC-001) |
| Deliverables | D-0001 |
| Effort | S |
| Risk | LOW |
| Tier | LIGHT |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, Bash (uv run pytest) |
| Sub-Agent | none (LIGHT) |
| Verification | smoke: `uv run pytest tests/swarm/test_uv_enforcement.py -v` |

**Deliverables:**
1. CI guard test asserting no `python -m` / `pip install` in swarm modules.
2. Docs note in `docs/swarm/runbook.md` recording the UV mandate.

**Steps:**
1. [PLANNING] Read `CLAUDE.md` UV rule + locate sprint CLI tests as the parity model.
2. [EXECUTION] Add `tests/swarm/test_uv_enforcement.py` that greps `src/superclaude/cli/swarm/` for forbidden patterns.
3. [EXECUTION] Append UV-mandate paragraph to `docs/swarm/runbook.md`.
4. [VERIFICATION] Run `uv run pytest tests/swarm/test_uv_enforcement.py`.
5. [COMPLETION] `make verify-sync`; log task done.

**Acceptance Criteria:**
- `tests/swarm/test_uv_enforcement.py` exists and is green.
- All swarm scripts in `src/superclaude/cli/swarm/` execute via `uv run`.
- CI lane rejects bare `pip` / `python` invocations in swarm code.
- `docs/swarm/runbook.md` references AC-001 mandate.

**Validation:**
- `uv run pytest tests/swarm/test_uv_enforcement.py -v` returns exit 0.
- `grep -rE "python -m|pip install" src/superclaude/cli/swarm/` returns empty.

**Dependencies:** none. **Rollback:** revert the test + doc additions.
**Notes:** AC-001 binds directly to the project's CLAUDE.md UV-only rule.

### T01.02 -- Register `superclaude swarm` as new top-level CLI verb

| Field | Value |
|---|---|
| Roadmap | R-002 (AC-002) |
| Deliverables | D-0002 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, Bash, auggie (codebase-retrieval) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_cli_registration.py` |

**Deliverables:**
1. `swarm` group registered in `src/superclaude/cli/main.py`.

**Steps:**
1. [PLANNING] Use auggie to retrieve current CLI verb registration shape.
2. [EXECUTION] Add `cli.add_command(swarm_group)` in `cli/main.py`.
3. [VERIFICATION] `uv run superclaude swarm --help` lists subcommand placeholders.
4. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- `src/superclaude/cli/main.py` imports and registers `swarm_group`.
- `superclaude swarm` resolves as a top-level verb (not nested under sprint/roadmap).
- `swarm --help` lists placeholder subcommands (run/status/logs/attach/kill/scaffold/validate/validate-lenses).
- Test `tests/swarm/test_cli_registration.py` asserts top-level placement.

**Validation:**
- `uv run superclaude swarm --help` exits 0.
- `uv run pytest tests/swarm/test_cli_registration.py -v` passes.

**Dependencies:** none. **Rollback:** remove the `add_command` line.
**Notes:** Tie-break: AC-002 explicitly forbids nesting under sprint/roadmap.

### T01.03 -- Mirror `cli/sprint/` module shape for operator familiarity

| Field | Value |
|---|---|
| Roadmap | R-003 (AC-003) |
| Deliverables | D-0003 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Bash (ls), Write |
| Sub-Agent | none |
| Verification | tests: structural mapping assertion |

**Deliverables:**
1. `src/superclaude/cli/swarm/` directory tree with file roles 1:1 to `cli/sprint/`.

**Steps:**
1. [PLANNING] `ls src/superclaude/cli/sprint/` to enumerate files.
2. [EXECUTION] Create matching stubs in `cli/swarm/` (`__init__.py`, `commands.py`, `config.py`, `models.py`, `state.py`, `logging_.py`, `tmux.py`, `tui.py`, `transports/`, `lenses/`, `recipes/`).
3. [VERIFICATION] Confirm 1:1 file role mapping in module-shape test.
4. [COMPLETION] `make verify-sync`.

**Acceptance Criteria:**
- `src/superclaude/cli/swarm/` directory exists with every counterpart of `cli/sprint/` where roles align.
- Module filenames map 1:1 with documented divergences noted in `__init__.py` docstring.
- No swarm-specific file lacks a sprint analogue without justification.
- Test `tests/swarm/test_module_shape.py` (delivered in T01.07) consumes this layout.

**Validation:**
- `diff <(ls cli/sprint/) <(ls cli/swarm/)` shows only intentional differences.
- `uv run pytest tests/swarm/test_module_shape.py -v` passes after T01.07.

**Dependencies:** T01.02. **Rollback:** delete `cli/swarm/` directory.
**Notes:** NFR-015 enforcement test landed in T01.07.

### T01.04 -- Adopt Click ≥8.0.0 CLI group for the swarm verb

| Field | Value |
|---|---|
| Roadmap | R-004 (AC-006) |
| Deliverables | D-0004 |
| Effort | S |
| Risk | LOW |
| Tier | LIGHT |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, context7 (Click docs) |
| Sub-Agent | none |
| Verification | smoke: `superclaude swarm --help` |

**Deliverables:**
1. Click group + subcommand-registration scaffolding in `cli/swarm/__init__.py`.

**Steps:**
1. [PLANNING] Verify `click>=8.0.0` is in `pyproject.toml`.
2. [EXECUTION] Define `@click.group()` for `swarm_group` in `cli/swarm/__init__.py`.
3. [VERIFICATION] Invoke `superclaude swarm --help`.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- `cli/swarm/__init__.py` exposes `swarm_group = click.Group(...)` with Click ≥8.0.0.
- Subcommand registration uses `@swarm_group.command()` decorators.
- `--help` renders without import errors.
- `pyproject.toml` declares `click>=8.0.0`.

**Validation:**
- `superclaude swarm --help` exits 0.
- `python -c "import click; assert click.__version__ >= '8.0.0'"` passes.

**Dependencies:** T01.03. **Rollback:** revert `__init__.py` group declaration.

### T01.05 -- Enforce source-of-truth discipline for swarm contributions

| Field | Value |
|---|---|
| Roadmap | R-005 (AC-019) |
| Deliverables | D-0005 |
| Effort | S |
| Risk | LOW |
| Tier | LIGHT |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: `make verify-sync` |

**Deliverables:**
1. `docs/dev/sync-discipline.md` documenting src-first edit + sync workflow.

**Steps:**
1. [PLANNING] Read `CLAUDE.md` Component Sync section.
2. [EXECUTION] Write `docs/dev/sync-discipline.md` summarizing the rule.
3. [VERIFICATION] Run `make verify-sync`.
4. [COMPLETION] Log task done.

**Acceptance Criteria:**
- `docs/dev/sync-discipline.md` exists and references CLAUDE.md.
- Doc states: edit `src/superclaude/`, then `make sync-dev`, never edit `.claude/` directly.
- `make verify-sync` exits 0 on first run.
- Pre-commit hook `verify-sync` is referenced.

**Validation:**
- `make verify-sync` returns 0.
- `grep -q "make sync-dev" docs/dev/sync-discipline.md`.

**Dependencies:** none. **Rollback:** remove the doc.

### T01.06 -- Checkpoint: Phase 1 entry gate (tasks 1-5 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP1-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T01.01..T01.05 marked done in execution-log.
- `phase-1-cp1.md` checkpoint report written.
- AC-001 (UV), AC-002 (verb), AC-003 (shape), AC-006 (Click), AC-019 (sync) all green.
- No blockers logged for OQ owners.

**Validation:**
- Checkpoint file exists.
- `grep -c "status: done" execution-log.yaml` ≥ 5 for T01.01..T01.05.

**Dependencies:** T01.01..T01.05.

### T01.07 -- Add structural test asserting `cli/swarm/` mirrors `cli/sprint/`

| Field | Value |
|---|---|
| Roadmap | R-006 (NFR-015) |
| Deliverables | D-0006 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Write |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `tests/swarm/test_module_shape.py` asserting parallel module roles.

**Steps:**
1. [PLANNING] Enumerate sprint role-mapping table in test docstring.
2. [EXECUTION] Implement test comparing file sets.
3. [VERIFICATION] `uv run pytest tests/swarm/test_module_shape.py`.
4. [COMPLETION] `make verify-sync`.

**Acceptance Criteria:**
- `tests/swarm/test_module_shape.py` exists.
- Asserts each `cli/sprint/<file>.py` has a counterpart in `cli/swarm/` (or documented divergence).
- Test passes against current layout.
- Failure message lists missing files.

**Validation:**
- `uv run pytest tests/swarm/test_module_shape.py -v` passes.
- Mutation: removing a file from `cli/swarm/` causes test to fail.

**Dependencies:** T01.03. **Rollback:** delete the test.

### T01.08 -- Implement swarm_group Click entry point with subcommand placeholders

| Field | Value |
|---|---|
| Roadmap | R-007 (COMP-001) |
| Deliverables | D-0007 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke + tests |

**Deliverables:**
1. `swarm_group` exporting placeholders for run/status/logs/attach/kill/scaffold/validate/validate-lenses.

**Steps:**
1. [PLANNING] Confirm Click group from T01.04 exists.
2. [EXECUTION] Register 8 `@swarm_group.command()` placeholder functions in `cli/swarm/__init__.py`.
3. [VERIFICATION] `superclaude swarm --help` lists all 8.
4. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- `cli/swarm/__init__.py` exports `swarm_group` with 8 placeholder subcommands.
- `superclaude swarm --help` lists each in the subcommands section.
- Each placeholder echoes `not yet implemented` and exits non-zero (so tests catch premature use).
- Module imports without errors.

**Validation:**
- `superclaude swarm --help` exits 0 and contains all 8 names.
- `uv run pytest tests/swarm/test_cli_registration.py -v` passes.

**Dependencies:** T01.04. **Rollback:** remove placeholder commands.

### T01.09 -- Implement SwarmConfig dataclass with path resolution

| Field | Value |
|---|---|
| Roadmap | R-008 (COMP-003) |
| Deliverables | D-0008 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `src/superclaude/cli/swarm/config.py::SwarmConfig` immutable dataclass + tests.

**Steps:**
1. [PLANNING] Mirror sprint config patterns via auggie retrieval.
2. [EXECUTION] Define `@dataclass(frozen=True) class SwarmConfig`.
3. [EXECUTION] Add path-resolution helpers for output dir + env vars.
4. [VERIFICATION] `uv run pytest tests/swarm/test_config.py`.
5. [COMPLETION] `make verify-sync`.

**Acceptance Criteria:**
- `cli/swarm/config.py::SwarmConfig` is `@dataclass(frozen=True)`.
- Resolves output dir, env vars, defaults at construction.
- Tests cover happy + missing-env paths.
- No mutable state.

**Validation:**
- `uv run pytest tests/swarm/test_config.py -v` passes.
- Attempt to mutate frozen field raises `FrozenInstanceError`.

**Dependencies:** T01.03.

### T01.10 -- Build models module aggregator

| Field | Value |
|---|---|
| Roadmap | R-009 (COMP-004) |
| Deliverables | D-0009 |
| Effort | M |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests (JSON round-trip) |

**Deliverables:**
1. `src/superclaude/cli/swarm/models.py` exporting all DM-### dataclasses.

**Steps:**
1. [PLANNING] List all 20 DM-### records from roadmap.
2. [EXECUTION] Add stubs + `__all__` export list in `models.py`.
3. [EXECUTION] Implement `to_dict()`/`from_dict()` helpers using `dataclasses.asdict`.
4. [VERIFICATION] Round-trip test: instance → JSON → instance.
5. [COMPLETION] `make verify-sync`.

**Acceptance Criteria:**
- `cli/swarm/models.py` exports every DM-001..DM-020 record.
- JSON round-trip lossless on a representative sample.
- `__all__` reflects exported names.
- Type hints validated by `mypy` (or ruff equivalent).

**Validation:**
- `uv run pytest tests/swarm/test_models_round_trip.py -v` passes.
- `python -c "from superclaude.cli.swarm import models; assert len(models.__all__) >= 20"`.

**Dependencies:** T01.03.

### T01.11 -- Define Transport Protocol interface

| Field | Value |
|---|---|
| Roadmap | R-010 (COMP-031) |
| Deliverables | D-0010 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, context7 (typing.Protocol) |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `cli/swarm/transports/__init__.py::Transport` Protocol with `send(prompt, timeout) -> WorkerResult`.

**Steps:**
1. [PLANNING] Confirm WorkerResult exists from T01.26.
2. [EXECUTION] Define `class Transport(Protocol): def send(...)`.
3. [VERIFICATION] Mypy-style structural check.
4. [COMPLETION] Add usage docstring.

**Acceptance Criteria:**
- `transports/__init__.py` defines `Transport` Protocol.
- Signature: `send(prompt: str, timeout: int) -> WorkerResult`.
- Docstring documents the contract.
- Two implementations land in M3 (openai_compat, stub).

**Validation:**
- `uv run pytest tests/swarm/test_transport_protocol.py -v` passes (mock impl).
- `python -c "from superclaude.cli.swarm.transports import Transport"`.

**Dependencies:** T01.10.

### T01.12 -- Checkpoint: Phase 1 mid-phase (tasks 7-11 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP1-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- T01.07..T01.11 done in execution-log.
- `phase-1-cp2.md` checkpoint report exists.
- Module shape test green; SwarmConfig + models stubs importable.
- Transport Protocol locked.

**Validation:**
- `grep -c "status: done" execution-log.yaml` ≥ 10.

**Dependencies:** T01.07..T01.11.

### T01.13 -- Implement DM-001 JobSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-011 (DM-001) |
| Deliverables | D-0011 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:**
1. `models.py::JobSpec` with every field enumerated in DM-001.

**Steps:**
1. [PLANNING] Enumerate all 14 sub-fields from roadmap DM-001 row.
2. [EXECUTION] Define `@dataclass class JobSpec` with all sub-specs nested.
3. [EXECUTION] Add `amalgamation_mode: Literal['raw','normalize','normalize+merge']`.
4. [VERIFICATION] Round-trip test.
5. [COMPLETION] `make verify-sync`.

**Acceptance Criteria:**
- `models.py::JobSpec` declared with fields: spec_version, job_id, created, caller, lens, custom_prompt_dir?, workers, transport, prompt, target, normalization, output, amalgamation_mode, status_policy, recommended_next_command_template, recommended_next_command_substitutions, runtime.
- JSON round-trip lossless.
- `amalgamation_mode` is a `Literal['raw','normalize','normalize+merge']`.
- Field-completeness test enumerates all 14 sub-fields.

**Validation:**
- `uv run pytest tests/swarm/test_jobspec.py -v` passes.
- Round-trip diff is empty.

**Dependencies:** T01.10. **Rollback:** revert `JobSpec` from models.py.
**Notes:** STRICT per §4.11 Critical Path Override (schema-bearing dataclass).

### T01.14 -- Implement DM-002 WorkerSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-012 (DM-002) |
| Deliverables | D-0012 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::WorkerSpec` with count/models/timeout_sec/temperature/retry policy.

**Steps:**
1. [PLANNING] Confirm retry-policy keys.
2. [EXECUTION] Define dataclass.
3. [VERIFICATION] Round-trip test.

**Acceptance Criteria:**
- `models.py::WorkerSpec` exports count:int, models:list[str], timeout_sec:int, temperature:float, retry: nested with on_5xx, on_5xx_backoff_sec, on_4xx, on_timeout.
- Defaults documented (timeout_sec=180 per NFR-010).
- Round-trip test passes.
- Validation rejects negative timeouts.

**Validation:**
- `uv run pytest tests/swarm/test_workerspec.py -v` passes.
- Negative `timeout_sec` raises ValueError.

**Dependencies:** T01.10.

### T01.15 -- Implement DM-003 TargetSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-013 (DM-003) |
| Deliverables | D-0013 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::TargetSpec` with kind/path/truncation/delimiters/injection_guard.

**Steps:**
1. [PLANNING] Confirm injection_guard fields.
2. [EXECUTION] Define dataclass with nested truncation + delimiters + injection_guard.
3. [VERIFICATION] Round-trip.

**Acceptance Criteria:**
- `models.py::TargetSpec` includes kind, path, truncation.line_cap, truncation.byte_floor, delimiters.open, delimiters.close, injection_guard.enabled, injection_guard.required_substring.
- Defaults: `delimiters.open="<<<TARGET>>>"`, `delimiters.close="<<<END TARGET>>>"`.
- Round-trip passes.
- Type hints exact.

**Validation:**
- `uv run pytest tests/swarm/test_targetspec.py -v` passes.
- `TargetSpec().delimiters.open == "<<<TARGET>>>"`.

**Dependencies:** T01.10.

### T01.16 -- Implement DM-004 TransportSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-014 (DM-004) |
| Deliverables | D-0014 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::TransportSpec` with kind/base_url_env/api_key_env.

**Steps:**
1. [EXECUTION] Define dataclass.
2. [VERIFICATION] Round-trip test.

**Acceptance Criteria:**
- `models.py::TransportSpec` declared with kind, base_url_env, api_key_env.
- `kind` is a Literal['openai_compat','stub'].
- Round-trip lossless.
- Env-var name validation rejects empty strings.

**Validation:**
- `uv run pytest tests/swarm/test_transportspec.py` passes.
- Construction with `kind="bogus"` raises.

**Dependencies:** T01.10.

### T01.17 -- Implement DM-005 PromptSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-015 (DM-005) |
| Deliverables | D-0015 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:**
1. `models.py::PromptSpec` carrying verbatim system + user_template + variables.

**Steps:**
1. [PLANNING] Confirm §11.5 required-substring will be enforced at schema-time (T02.03), not here.
2. [EXECUTION] Define dataclass with `system:str`, `user_template:str`, `variables:dict`.
3. [VERIFICATION] Round-trip test preserves whitespace verbatim.

**Acceptance Criteria:**
- `models.py::PromptSpec` carries verbatim system + user_template + variables.
- Whitespace preserved (no normalization).
- Round-trip diff empty including newlines.
- Type hints exact.

**Validation:**
- `uv run pytest tests/swarm/test_promptspec.py -v` passes.
- Round-trip preserves trailing whitespace.

**Dependencies:** T01.10.
**Notes:** STRICT per §4.11 (carries injection-guard substring downstream).

### T01.18 -- Checkpoint: Phase 1 mid-phase (DM-001..005 frozen)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP1-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- T01.13..T01.17 done.
- `phase-1-cp3.md` checkpoint report exists.
- JobSpec + WorkerSpec + TargetSpec + TransportSpec + PromptSpec all round-trip green.
- No field drift vs roadmap DM-### rows.

**Validation:**
- Checkpoint file exists.
- `grep -c "status: done" execution-log.yaml` ≥ 17.

**Dependencies:** T01.13..T01.17.

### T01.19 -- Implement DM-006 NormalizationSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-016 (DM-006) |
| Deliverables | D-0016 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::NormalizationSpec` with recipe/template_path/schema_version/recipe_args/on_parse_error.

**Steps:**
1. [EXECUTION] Define dataclass.
2. [VERIFICATION] Round-trip.

**Acceptance Criteria:**
- `models.py::NormalizationSpec` declared with recipe, template_path, schema_version, recipe_args, on_parse_error.salvage, on_parse_error.retain_raw.
- Defaults: `salvage=true`, `retain_raw=true`.
- Round-trip lossless.
- Validation rejects unknown recipe names at schema time (covered M2).

**Validation:**
- `uv run pytest tests/swarm/test_normalizationspec.py` passes.

**Dependencies:** T01.10.

### T01.20 -- Implement DM-007 OutputSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-017 (DM-007) |
| Deliverables | D-0017 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::OutputSpec` with dir/filename_template/lens_name/atomic_write/emit_meta_sidecar.

**Steps:**
1. [EXECUTION] Define dataclass.
2. [VERIFICATION] Round-trip.

**Acceptance Criteria:**
- Fields: dir, filename_template, lens_name, atomic_write, emit_meta_sidecar.
- `atomic_write` defaults to True (IMM-6 alignment).
- Round-trip lossless.
- Path-confinement validation deferred to M3 (NFR-013).

**Validation:**
- `uv run pytest tests/swarm/test_outputspec.py` passes.
- Default `atomic_write` is True.

**Dependencies:** T01.10.

### T01.21 -- Implement DM-008 StatusPolicy dataclass

| Field | Value |
|---|---|
| Roadmap | R-018 (DM-008) |
| Deliverables | D-0018 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::StatusPolicy` with floor/success_first/partial_threshold.

**Steps:**
1. [EXECUTION] Define dataclass with IMM-5 defaults.
2. [VERIFICATION] Round-trip + defaults test.

**Acceptance Criteria:**
- Fields: floor:int, success_first:bool, partial_threshold:int.
- Defaults: `floor=2`, `success_first=True`, `partial_threshold=2` per IMM-5.
- Round-trip lossless.
- Test asserts defaults.

**Validation:**
- `uv run pytest tests/swarm/test_statuspolicy.py` passes.
- `StatusPolicy().floor == 2`.

**Dependencies:** T01.10.

### T01.22 -- Implement DM-009 RuntimeSpec dataclass

| Field | Value |
|---|---|
| Roadmap | R-019 (DM-009) |
| Deliverables | D-0019 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::RuntimeSpec` with mode/log_level/on_completion.

**Steps:**
1. [EXECUTION] Define dataclass.
2. [VERIFICATION] Round-trip.

**Acceptance Criteria:**
- Fields: mode (Literal['inline','detached']), log_level, on_completion.write_done_sentinel, on_completion.print_contract_to_stdout.
- Defaults `mode='inline'` (M7 detached mode is opt-in).
- Round-trip lossless.
- Mode-validation test.

**Validation:**
- `uv run pytest tests/swarm/test_runtimespec.py` passes.

**Dependencies:** T01.10.

### T01.23 -- Implement DM-010 LensEntry dataclass

| Field | Value |
|---|---|
| Roadmap | R-020 (DM-010) |
| Deliverables | D-0020 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:**
1. `models.py::LensEntry` with all 13 fields from DM-010.

**Steps:**
1. [PLANNING] Enumerate fields from roadmap DM-010 row.
2. [EXECUTION] Define dataclass with full field set + stability Literal.
3. [VERIFICATION] Round-trip test + LENSES dict can construct.

**Acceptance Criteria:**
- `models.py::LensEntry` carries name, description, system_prompt_fragment, user_template, output_template_path, recipe_name, default_workers, default_target_line_cap, suspect, tier, recommended_next_command_template, acceptance_notes, stability:Literal['stable','experimental'].
- All 13 fields present and typed.
- Round-trip lossless.
- LENSES dict can hold 8 entries (smoke test).

**Validation:**
- `uv run pytest tests/swarm/test_lensentry.py -v` passes.
- Field-count assertion: 13.

**Dependencies:** T01.10.
**Notes:** STRICT — feeds Wave 0 preflight and manifest snapshot.

### T01.24 -- Implement DM-011 ResolvedLensEntry dataclass

| Field | Value |
|---|---|
| Roadmap | R-021 (DM-011) |
| Deliverables | D-0021 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:**
1. `models.py::ResolvedLensEntry` snapshot dataclass.

**Steps:**
1. [EXECUTION] Define dataclass.
2. [EXECUTION] Implement `from_lens` classmethod.
3. [VERIFICATION] Round-trip.

**Acceptance Criteria:**
- `models.py::ResolvedLensEntry` carries name, system_prompt_fragment, user_template, recipe_name, default_workers, suspect, tier, recommended_next_command_template, stability.
- Constructible from a LensEntry via `ResolvedLensEntry.from_lens(entry)`.
- Round-trip lossless.
- Forms the immutable snapshot stored in `manifest.json` (INV-016).

**Validation:**
- `uv run pytest tests/swarm/test_resolvedlens.py -v` passes.
- Snapshot round-trips into Manifest field.

**Dependencies:** T01.23.
**Notes:** STRICT — INV-001 / INV-016 anchor.

### T01.24a -- Checkpoint: Phase 1 mid-phase (DM-006..011 frozen)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP1-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- T01.19..T01.24 done.
- `phase-1-cp4.md` checkpoint report exists.
- All policy/runtime/output/lens dataclasses round-trip green.
- IMM-5 defaults verified on StatusPolicy.

**Validation:**
- Checkpoint file present.
- `grep -c "status: done" execution-log.yaml` ≥ 22.

**Dependencies:** T01.19..T01.24.

### T01.25 -- Implement DM-012 ResultContract dataclass

| Field | Value |
|---|---|
| Roadmap | R-022 (DM-012) |
| Deliverables | D-0022 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:**
1. `models.py::ResultContract` carrying every field from DM-012.

**Steps:**
1. [PLANNING] Enumerate all DM-012 fields.
2. [EXECUTION] Define nested dataclass.
3. [VERIFICATION] Round-trip + field-completeness test.

**Acceptance Criteria:**
- `models.py::ResultContract` carries contract_version, status, job_id, started, finished, elapsed_ms, caller, lens, lens_source, target (path/checksum/truncated/truncation_line_cap), workers_requested, workers_succeeded, workers_failed, output_files:list[WorkerResult], amalgamation_mode, merged_path?, caller_metadata, recommended_next_command, artifacts.
- JSON round-trip lossless on all fields.
- Field-completeness test asserts every spec-listed key present.
- `status` is a Literal['success','partial','failed'].

**Validation:**
- `uv run pytest tests/swarm/test_result_contract.py -v` passes.
- Field-completeness assertion: 18 top-level keys.

**Dependencies:** T01.10.
**Notes:** STRICT — caller-facing contract. FR-018 emitter built in M5.

### T01.26 -- Implement DM-013 WorkerResult + DM-014 SwarmState + DM-015 EventRecord (merged)

| Field | Value |
|---|---|
| Roadmap | R-023, R-024, R-025 (DM-013/014/015 merged) |
| Deliverables | D-0023 |
| Effort | M |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::WorkerResult`, `SwarmState`, `EventRecord` dataclasses.

**Steps:**
1. [PLANNING] Enumerate fields for each.
2. [EXECUTION] Define three dataclasses with Literal enums.
3. [VERIFICATION] Round-trip each.

**Acceptance Criteria:**
- `models.py` exports WorkerResult (index, path, raw_path, meta_path, final_path, model_id, model_label, bytes, status, http_code?, attempts, elapsed_ms), SwarmState (state Literal, job_id, updated), EventRecord (event_type Literal, timestamp, worker_index?, payload).
- All three round-trip lossless.
- Literal enums match roadmap exactly.
- Field-count test for each.

**Validation:**
- `uv run pytest tests/swarm/test_worker_state_event.py -v` passes.

**Dependencies:** T01.10.
**Notes:** Merger justified — 3 small related records share the JSONL/state plumbing and emit together in M3.

### T01.27 -- Implement DM-016 Manifest dataclass

| Field | Value |
|---|---|
| Roadmap | R-026 (DM-016) |
| Deliverables | D-0024 |
| Effort | S |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:**
1. `models.py::Manifest` carrying resolved_lens_entry + preflight summary.

**Steps:**
1. [PLANNING] Confirm ResolvedLensEntry available.
2. [EXECUTION] Define dataclass.
3. [VERIFICATION] Round-trip + immutability test.

**Acceptance Criteria:**
- `models.py::Manifest` carries contract_version, job_id, resolved_lens_entry:ResolvedLensEntry, preflight.target_checksum, preflight.workers_requested, preflight.transport_kind.
- JSON round-trip lossless (resolved_lens_entry preserved verbatim).
- Immutability test: round-trip preserves bytes exactly (INV-016 source-of-truth).
- Used by M6 resume.

**Validation:**
- `uv run pytest tests/swarm/test_manifest.py -v` passes.
- Bytes-identical round-trip.

**Dependencies:** T01.24.
**Notes:** STRICT — INV-001 / INV-016 source-of-truth.

### T01.28 -- Implement DM-017 DoneSentinel + DM-018 Artifacts + DM-019 CallerInfo (merged)

| Field | Value |
|---|---|
| Roadmap | R-027, R-028, R-029 (merged) |
| Deliverables | D-0025 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:**
1. `models.py::DoneSentinel`, `Artifacts`, `CallerInfo` dataclasses.

**Steps:**
1. [EXECUTION] Define three dataclasses.
2. [VERIFICATION] Round-trip each.

**Acceptance Criteria:**
- `models.py` exports DoneSentinel (atomic_write=True, terminal_status, contract_path), Artifacts (manifest_path, state_path, event_log_jsonl, event_log_md, done_sentinel), CallerInfo (skill?, skill_version?, invocation_label, kind:Literal['claude','cli','subprocess']).
- Round-trip lossless on each.
- CallerInfo.kind Literal enforced.
- Field-count test for each.

**Validation:**
- `uv run pytest tests/swarm/test_sentinel_artifacts_caller.py -v` passes.

**Dependencies:** T01.10.
**Notes:** Merger justified — small accompanying records emitted together with the contract.

### T01.29 -- Checkpoint: Phase 1 end-of-phase (M1 exit gate)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase, mandatory) |
| Deliverables | D-CP1-1 |
| Tier | STRICT |

**Acceptance Criteria:**
- `phase-1-cp5.md` end-of-phase checkpoint report exists with sign-off.
- Contract/source-of-truth records (ResultContract, Manifest, DoneSentinel) frozen; accumulator/state records mutable by design (F-P1-3); all 20 DM-### records round-trip green.
- `superclaude swarm --help` lists 8 subcommand placeholders.
- Owners assigned for OQ-006, OQ-008, OQ-009 (entry-gate condition for M2).
- `make verify-sync` passes.

**Validation:**
- `grep -c "status: done" execution-log.yaml` ≥ 27.
- `superclaude swarm --help | grep -cE "run|status|logs|attach|kill|scaffold|validate|validate-lenses"` ≥ 8.
- Owners section in checkpoint report names a person/role for each OQ.

**Dependencies:** all prior Phase 1 tasks.
**Notes:** End-of-phase checkpoints are STRICT per §4.10 — they gate the next milestone's entry.
