# Phase 6 -- Resume, Crash Recovery & Manifest

**Goal:** Make swarm jobs resumable from the manifest as durable source-of-truth: `swarm run --resume <job_id>` rehydrates `resolved_lens_entry` verbatim from the manifest, skips workers reporting `status: success`, re-dispatches the remaining, re-runs Wave 2, and regenerates `merged.md` unconditionally when `amalgamation_mode == normalize+merge`. Exit when resume reaches terminal state with no duplicate work, lens-registry mutations between runs do NOT affect resumed jobs (INV-016), `--force-relens` opts into re-resolution from current registry, and `spec_version` forward-compat best-effort (1.1 orchestrator loads 1.0 spec) is verified.

### T06.01 -- Implement INV-001 resume-from-manifest rehydration

| Field | Value |
|---|---|
| Roadmap | R-110 (INV-001) |
| Deliverables | D-0091 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie, serena |
| Sub-Agent | tech-research (resume semantics review) |
| Verification | tests: `uv run pytest tests/swarm/test_resume_uses_manifest_lens.py` |

**Deliverables:**
1. `preflight.py::resume_mode(manifest_path) -> JobSpec` rehydrating from `resolved_lens_entry`.
2. `tests/swarm/test_resume_uses_manifest_lens.py` asserting registry edits ignored.

**Steps:**
1. [PLANNING] Define resume read flow: load manifest → use `resolved_lens_entry` verbatim → skip live LENSES lookup.
2. [EXECUTION] Implement rehydration in preflight; gate behind `--resume`.
3. [VERIFICATION] Test: mutate live LENSES entry, resume, assert resumed job uses manifest lens.
4. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- Resumed job uses manifest lens; registry edits ignored unless `--force-relens`.
- `manifest.resolved_lens_entry` consumed verbatim (no re-resolution).
- Test exercises mutation between runs.
- `tests/swarm/test_resume_uses_manifest_lens.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_resume_uses_manifest_lens.py -v` passes.
- Resume-mode preflight does not call live `LENSES.get(name)`.

**Dependencies:** T01.10 (Manifest, ResolvedLensEntry), T02.02 (preflight). **Rollback:** disable `--resume`; document manual recovery path.
**Notes:** INV-016 manifest-as-source-of-truth covered together.

### T06.02 -- Implement INV-010 resume merge regeneration

| Field | Value |
|---|---|
| Roadmap | R-111 (INV-010) |
| Deliverables | D-0092 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_resume_regenerates_merge.py` |

**Deliverables:**
1. `reduce.py` resume hook regenerating `merged.md` unconditionally when mode == `normalize+merge`.

**Steps:**
1. [PLANNING] Confirm Wave 2 reruns for re-dispatched workers feed merge regen.
2. [EXECUTION] Add resume hook in `reduce_wave3` deleting old `merged.md` and regenerating.
3. [VERIFICATION] Test: kill mid-merge; resume; assert new merged.md reflects re-dispatched workers.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Stale merge never persists post-resume.
- Provenance header in regenerated merge reflects re-dispatch elapsed_ms.
- Regen unconditional when mode == `normalize+merge`.
- `tests/swarm/test_resume_regenerates_merge.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_resume_regenerates_merge.py -v` passes.
- Pre/post-resume `merged.md` differs when workers re-dispatched.

**Dependencies:** T05.02 (merge), T06.01 (resume rehydration). **Rollback:** print warning advising manual rerun.

### T06.03 -- Verify INV-016 manifest immunity to mutation

| Field | Value |
|---|---|
| Roadmap | R-112 (INV-016) |
| Deliverables | D-0093 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_manifest_durable.py` |

**Deliverables:**
1. `tests/swarm/test_manifest_durable.py` mutation test.

**Steps:**
1. [PLANNING] Compose 2-run scenario: run → mutate LENSES → resume.
2. [EXECUTION] Write test verifying resume uses manifest lens entry verbatim.
3. [VERIFICATION] Run test.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Manifest immutable across resume; mutation test passes.
- Lens-registry edits between runs do not affect resumed jobs.
- `--force-relens` opts into mutation visibility.
- `tests/swarm/test_manifest_durable.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_manifest_durable.py -v` passes.
- Diff of manifest contents pre/post resume identical.

**Dependencies:** T06.01. **Rollback:** none — durability guard.

### T06.04 -- Implement `swarm run --resume` end-to-end

| Field | Value |
|---|---|
| Roadmap | R-113 (FR-015) |
| Deliverables | D-0094 |
| Effort | L |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | tech-research (E2E flow validation) |
| Verification | tests: `uv run pytest tests/swarm/test_resume_crash_recovery.py` |

**Deliverables:**
1. `commands.py::run_cmd` with `--resume <job_id>` branch executing Wave 0 in resume mode, skip succeeded workers, re-dispatch remaining, re-run Wave 2, regen merge.

**Steps:**
1. [PLANNING] Define resume flow: locate prior job_id directory → load manifest → enumerate workers → classify by `.meta.json` status.
2. [EXECUTION] Implement `--resume` branch in `run_cmd`.
3. [EXECUTION] Wire skip + redispatch + Wave 2 rerun + merge regen.
4. [VERIFICATION] E2E test: kill mid-dispatch, resume, reach terminal state.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- Succeeded workers skipped; remaining re-dispatched; merge regenerated when applicable.
- E2E test exercises kill-then-resume path.
- `swarm run --resume <job_id>` exits 0 on success.
- `tests/swarm/test_resume_crash_recovery.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_resume_crash_recovery.py -v` passes.
- Resume run produces no duplicate worker outputs.

**Dependencies:** T06.01, T06.02. **Rollback:** disable `--resume`; document manual cleanup steps.

### T06.05 -- Implement manifest emission at preflight

| Field | Value |
|---|---|
| Roadmap | R-114 (FR-016) |
| Deliverables | D-0095 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_manifest_emission.py` |

**Deliverables:**
1. `preflight.py::emit_manifest(resolved_lens_entry, target_checksum, transport_kind) -> Path`.

**Steps:**
1. [PLANNING] Confirm DM-011 ResolvedLensEntry fields and DM-016 Manifest fields.
2. [EXECUTION] Implement manifest emission with verbatim resolved_lens_entry snapshot (system_prompt_fragment, user_template, recipe_name, defaults, suspect, tier, stability).
3. [EXECUTION] Atomic write via tmp+`os.replace`.
4. [VERIFICATION] Round-trip test: emit → load → assert equality.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Manifest captures full resolved lens snapshot at Wave 0.
- All listed fields present in manifest YAML/JSON.
- Atomic write ensures no partial manifest.
- `tests/swarm/test_manifest_emission.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_manifest_emission.py -v` passes.
- `yq '.resolved_lens_entry.system_prompt_fragment' manifest.yaml` returns non-null.

**Dependencies:** T01.10 (Manifest, ResolvedLensEntry), T02.02 (preflight). **Rollback:** emit minimal manifest with just lens name.

### T06.06 -- Checkpoint: Phase 6 mid-phase gate (tasks 1-5 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP6-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T06.01..T06.05 marked done in execution-log.
- `phase-6-cp1.md` checkpoint report written.
- Resume rehydration + merge regen + manifest emission all green.
- INV-001 / INV-010 / INV-016 tests passing.

**Validation:**
- `uv run pytest tests/swarm/test_resume_uses_manifest_lens.py tests/swarm/test_resume_regenerates_merge.py tests/swarm/test_manifest_durable.py tests/swarm/test_manifest_emission.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T06.01..T06.05.

### T06.07 -- Implement `--force-relens` flag (opt-in re-resolution)

| Field | Value |
|---|---|
| Roadmap | R-115 (FR-025) |
| Deliverables | D-0096 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit, context7 (Click) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_force_relens.py` |

**Deliverables:**
1. `commands.py::run_cmd` with `--force-relens` flag triggering re-resolution from current registry.

**Steps:**
1. [PLANNING] Confirm flag interaction with `--resume`.
2. [EXECUTION] Add `--force-relens` option; branch preflight to re-resolve when set.
3. [VERIFICATION] Test: mutate LENSES, resume with --force-relens, assert new lens applied.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Flag triggers re-resolution; default path uses manifest.
- Test exercises both paths (with and without flag).
- Help text documents the override semantics.
- `tests/swarm/test_force_relens.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_force_relens.py -v` passes.
- `swarm run --resume <id> --force-relens` re-resolves lens from current LENSES.

**Dependencies:** T06.01, T06.04. **Rollback:** remove flag; default behavior remains manifest-driven.

### T06.08 -- Verify NFR-005 crash recovery semantics (kill-then-resume E2E)

| Field | Value |
|---|---|
| Roadmap | R-116 (NFR-005) |
| Deliverables | D-0097 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash |
| Sub-Agent | tech-research (crash semantics) |
| Verification | tests: `uv run pytest tests/swarm/test_crash_recovery_e2e.py` |

**Deliverables:**
1. `tests/swarm/test_crash_recovery_e2e.py` end-to-end crash recovery.

**Steps:**
1. [PLANNING] Compose multi-worker fixture with controllable failure injection.
2. [EXECUTION] Test: start swarm → SIGKILL mid-dispatch → resume → assert terminal state.
3. [VERIFICATION] Verify no duplicate work; succeeded workers skipped.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Kill-then-resume reaches terminal state with no duplicate work.
- Worker-level skip honored; remaining re-dispatched.
- Merge regenerated when applicable.
- `tests/swarm/test_crash_recovery_e2e.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_crash_recovery_e2e.py -v` passes.
- Resume run final contract has expected `workers_succeeded` count.

**Dependencies:** T06.04. **Rollback:** mark test xfail with diagnostic capture.

### T06.09 -- Verify NFR-006 schema forward-compat (1.1 loads 1.0 spec)

| Field | Value |
|---|---|
| Roadmap | R-117 (NFR-006) |
| Deliverables | D-0098 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_schema_forward_compat.py` |

**Deliverables:**
1. `tests/swarm/test_schema_forward_compat.py` asserting orchestrator loads older spec_version.

**Steps:**
1. [PLANNING] Author 1.0 spec fixture; bump orchestrator to 1.1.
2. [EXECUTION] Write test loading 1.0 fixture under 1.1 orchestrator.
3. [VERIFICATION] Assert no error; deprecated fields warned but accepted.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- 1.1 orchestrator loads 1.0 spec without error.
- Deprecated fields warned in log but accepted.
- Best-effort policy documented in schema module.
- `tests/swarm/test_schema_forward_compat.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_schema_forward_compat.py -v` passes.
- 1.0 fixture loads successfully.

**Dependencies:** T02.01 (schema). **Rollback:** none — best-effort guard.

### T06.10 -- Checkpoint: Phase 6 exit gate (end-of-phase)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase) |
| Deliverables | D-CP6-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T06.01..T06.09 marked done in execution-log.
- `phase-6-cp2.md` end-of-phase checkpoint written.
- Resume + crash recovery + manifest durability all green.
- INV-001 + INV-010 + INV-016 + FR-015 + FR-016 + FR-025 + NFR-005 + NFR-006 verified.

**Validation:**
- `uv run pytest tests/swarm/ -v` Phase 6 surface passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T06.01..T06.09. **Rollback:** none — phase exit gate.
**Notes:** M6 exit (along with M7) unblocks M8 migration.
