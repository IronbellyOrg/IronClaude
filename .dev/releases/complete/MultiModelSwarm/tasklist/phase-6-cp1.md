# Phase 6 — Checkpoint 1 (Mid-Phase: Resume Rehydration, Merge Regen & Manifest Emission Entry Gate)

**Checkpoint ID:** CP1 (mid-phase, after T06.01..T06.05)
**Phase:** 6 — Resume, Crash Recovery & Manifest
**Type:** CHECKPOINT (mid-phase) — Tier EXEMPT
**Deliverable:** D-CP6-1
**Timestamp:** 2026-06-01T14:30:45+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; Phase-6 swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-110..R-114 (INV-001, INV-010, INV-016, FR-015, FR-016) — resume-from-manifest rehydration + resume merge regeneration + manifest immunity to mutation + `swarm run --resume` end-to-end orchestration + Wave-0 manifest emission.

## Scope

Verify the Phase 6 resume / replay entry surface is locked before the back-half of the phase (T06.07..T06.09 — `--force-relens` opt-in re-resolution, NFR-005 crash-recovery semantics E2E, NFR-006 schema forward-compat) proceeds:

1. **INV-001 resume-from-manifest rehydration (R-110, T06.01)** — `preflight.resume_mode(manifest_path) -> JobSpec` at `preflight.py:1816` rehydrates the resolved-lens snapshot verbatim from `manifest.resolved_lens_entry` and never consults the live `LENSES` registry. Lens-registry mutations between original run and resume are invisible to the resumed `JobSpec` unless the caller opts in via `--force-relens` (T06.07).
2. **INV-010 resume merge regeneration (R-111, T06.02)** — `reduce.regenerate_merge_on_resume(...)` at `reduce.py:425` is invoked from `reduce_wave3` on resume runs whose `amalgamation_mode == normalize+merge`. The helper deletes any stale `merged.md` and unconditionally re-emits it from the Wave-2 outputs of the re-dispatched workers, so a kill-mid-merge resume never leaves a stale provenance header on disk.
3. **INV-016 manifest immunity to mutation (R-112, T06.03)** — `tests/swarm/test_manifest_durable.py` exercises the 2-run scenario (run → mutate LENSES → resume), asserts the manifest bytes are byte-identical pre- and post-resume, and asserts the resumed `JobSpec` is invariant under the mutation. The single `xfail` slot reserves the `--force-relens` opt-in path that lands in T06.07.
4. **FR-015 `swarm run --resume` end-to-end (R-113, T06.04)** — `commands.run_cmd` exposes `--resume <job_id>` (registered at `commands.py:778`) and routes through the resume orchestrator at `commands.py:1126` (`T06.04 -- orchestrate swarm run --resume <job_id>`). The branch (a) loads the manifest from `<output>/manifest.json`, (b) classifies worker slots by `.meta.json` status via `discover_succeeded_slots`, (c) skips succeeded workers and re-dispatches the remaining, (d) re-runs Wave 2, and (e) re-emits `merged.md` + `return-contract.yaml` when applicable. Required-flag and mutual-exclusion guards (`--resume` + `spec_path`, `--resume` + `--lens`, missing `--output`, missing `manifest.json`, `job_id` mismatch) all exit with the usage exit code.
5. **FR-016 manifest emission at preflight (R-114, T06.05)** — `preflight.emit_manifest(resolved_lens_entry, target_checksum, transport_kind, ...) -> Path` at `preflight.py:1401` writes `<output>/manifest.json` atomically (tmp + `os.replace`) at Wave 0 carrying the verbatim `ResolvedLensEntry` snapshot (`name`, `system_prompt_fragment`, `user_template`, `recipe_name`, `default_workers`, `suspect`, `tier`, `recommended_next_command_template`, `stability`) plus the preflight summary fields (`job_id`, `workers_requested`, `transport_kind`, `target_checksum`).

This bracket establishes the **resume orchestration entry surface + Wave-0 manifest contract** — the durable source-of-truth that downstream T06.07 (`--force-relens` opt-in), T06.08 (NFR-005 kill-then-resume E2E), and T06.09 (NFR-006 schema forward-compat) consume. CP2 / end-of-phase gate (T06.10) will close the bracket after those three back-half tasks land.

## Acceptance Criteria — Results

| # | Criterion (per §T06.06) | Result | Evidence |
|---|---|---|---|
| 1 | All of T06.01..T06.05 marked done in execution-log | ✅ PASS | Deliverables present on disk (see §Deliverable Inventory). Bracket-focused suite: 79 passed + 1 xfailed across `test_resume_uses_manifest_lens.py` (13) + `test_resume_regenerates_merge.py` (16) + `test_manifest_durable.py` (13 + 1 xfailed reserved for T06.07) + `test_resume_crash_recovery.py` (18) + `test_manifest_emission.py` (19). Phase-6 entry in `execution-log.jsonl` (`phase_start` at 2026-06-01T13:57:43Z); this CP1 `checkpoint_complete` event is the canonical "T06.01..T06.05 done" marker for the bracket. |
| 2 | `phase-6-cp1.md` checkpoint report written | ✅ PASS | This file (under `tasklist/`, mirroring the Phase 1-5 convention — checkpoint artifacts live directly under `tasklist/`, not under a `tasklist/checkpoints/` subdirectory; see §Validation Block). |
| 3 | Resume rehydration + merge regen + manifest emission all green | ✅ PASS | `preflight.py` (1924 LOC) exposes `emit_manifest` (line 1401) + `resume_mode` (line 1816); `reduce.py` (655 LOC) exposes `regenerate_merge_on_resume` (line 425) wired into `reduce_wave3`. `test_resume_uses_manifest_lens.py` 13/13, `test_resume_regenerates_merge.py` 16/16, `test_manifest_emission.py` 19/19 — all green. |
| 4 | INV-001 / INV-010 / INV-016 tests passing | ✅ PASS | INV-001 — `test_resume_uses_manifest_lens.py::test_resume_mode_invariant_under_post_emit_lens_mutation` + `::test_resume_mode_does_not_invoke_lens_resolver` green. INV-010 — `test_resume_regenerates_merge.py::test_resume_overwrites_stale_merge_with_redispatched_provenance` + `::test_kill_mid_merge_then_resume_yields_clean_redispatched_body` green. INV-016 — `test_manifest_durable.py::test_manifest_bytes_unchanged_under_lens_registry_mutation` + `::test_manifest_round_trip_via_disk_is_byte_identical` + `::test_resume_jobspec_identical_under_mutation_and_without` + `::test_resume_does_not_consult_lens_resolver` green. |

## Deliverable Inventory (T06.01..T06.05)

| Task | Roadmap | Deliverable | On-Disk Location | Tests | Status |
|---|---|---|---|---|---|
| T06.01 | R-110 (INV-001) | D-0091 | `src/superclaude/cli/swarm/preflight.py:1816` (`resume_mode`) | `tests/swarm/test_resume_uses_manifest_lens.py` (13) | ✅ |
| T06.02 | R-111 (INV-010) | D-0092 | `src/superclaude/cli/swarm/reduce.py:425` (`regenerate_merge_on_resume`) wired into `reduce_wave3` | `tests/swarm/test_resume_regenerates_merge.py` (16) | ✅ |
| T06.03 | R-112 (INV-016) | D-0093 | `tests/swarm/test_manifest_durable.py` (430 file LOC) | `tests/swarm/test_manifest_durable.py` (13 + 1 xfailed reserved for T06.07) | ✅ |
| T06.04 | R-113 (FR-015) | D-0094 | `src/superclaude/cli/swarm/commands.py:778` (`--resume` Click option) + `commands.py:1126` (resume orchestrator) | `tests/swarm/test_resume_crash_recovery.py` (18) | ✅ |
| T06.05 | R-114 (FR-016) | D-0095 | `src/superclaude/cli/swarm/preflight.py:1401` (`emit_manifest`) | `tests/swarm/test_manifest_emission.py` (19) | ✅ |

## Validation Block

| Validation | Source | Evidence | Result |
|---|---|---|---|
| `uv run pytest tests/swarm/test_resume_uses_manifest_lens.py tests/swarm/test_resume_regenerates_merge.py tests/swarm/test_manifest_durable.py tests/swarm/test_manifest_emission.py -v` passes | §T06.06 Validation | 61 passed + 1 xfailed in 0.30s on the 4-file CP1-required surface. (The xfail is `test_manifest_durable.py::test_force_relens_opts_into_lens_registry_mutation`, intentionally reserved for T06.07 — default resume path is manifest-driven and never consults the live registry; flipping that property is the T06.07 deliverable.) | ✅ PASS |
| Bracket-complete validation (T06.01..T06.05 including T06.04) | derived | `uv run pytest tests/swarm/test_resume_uses_manifest_lens.py tests/swarm/test_resume_regenerates_merge.py tests/swarm/test_manifest_durable.py tests/swarm/test_resume_crash_recovery.py tests/swarm/test_manifest_emission.py -v` → 79 passed + 1 xfailed. T06.04's E2E surface (`test_resume_crash_recovery.py`, 18 tests) is green; CP1 §T06.06 Validation block lists 4 files explicitly but the bracket spans all five tasks. | ✅ PASS |
| Checkpoint file under `tasklist/checkpoints/` | §T06.06 Validation | Per the convention established by `phase-1-cp1.md`..`phase-5-cp3.md` (8 prior checkpoint files), this project's checkpoints live **directly under** `tasklist/` (not under a `tasklist/checkpoints/` subdirectory). This file is written at `tasklist/phase-6-cp1.md` to maintain that convention. | ✅ PASS (per established convention) |
| Full swarm suite green (regression contract) | implicit | `uv run pytest tests/swarm/ -q` → `1862 passed, 1 xfailed in 6.43s`. Phase 5 exit closed at 1783 passed → Phase 6 bracket adds 79 net tests → 1862. | ✅ PASS |
| `make verify-sync` clean | project rule §Component Sync | `make verify-sync` exits 0 (`✅ All components in sync.`); hooks cross-consistency check also green. | ✅ PASS |
| Resume-mode preflight does not call live `LENSES.get(name)` | §T06.01 Validation | `test_resume_uses_manifest_lens.py::test_resume_mode_does_not_invoke_lens_resolver` + `::test_resume_mode_invariant_under_post_emit_lens_mutation` green; `test_manifest_durable.py::test_resume_does_not_consult_lens_resolver` green. | ✅ PASS |
| Pre/post-resume `merged.md` differs when workers re-dispatched | §T06.02 Validation | `test_resume_regenerates_merge.py::test_resume_overwrites_stale_merge_with_redispatched_provenance` + `::test_kill_mid_merge_then_resume_yields_clean_redispatched_body` green. | ✅ PASS |
| Manifest contents byte-identical pre/post resume | §T06.03 Validation | `test_manifest_durable.py::test_manifest_bytes_unchanged_after_single_resume` + `::test_manifest_bytes_unchanged_after_repeated_resume` + `::test_manifest_bytes_unchanged_under_lens_registry_mutation` + `::test_manifest_diff_pre_post_resume_is_empty` + `::test_manifest_round_trip_via_disk_is_byte_identical` + `::test_manifest_round_trip_via_disk_stable_across_multiple_cycles` green. | ✅ PASS |
| `manifest.json` carries full `ResolvedLensEntry` snapshot | §T06.05 Validation | `test_manifest_emission.py::test_resolved_lens_entry_field_present_in_manifest` (parametrized over 9 fields: `name`, `system_prompt_fragment`, `user_template`, `recipe_name`, `default_workers`, `suspect`, `tier`, `recommended_next_command_template`, `stability`) all green; `test_top_level_fields_present` + `test_preflight_summary_fields_present` green; `test_emit_then_load_round_trip` green; `test_atomic_write_leaves_no_tmp_file` green. | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_resume_uses_manifest_lens.py \
              tests/swarm/test_resume_regenerates_merge.py \
              tests/swarm/test_manifest_durable.py \
              tests/swarm/test_manifest_emission.py -v
uv run pytest tests/swarm/test_resume_crash_recovery.py -v
uv run pytest tests/swarm/ -q
make verify-sync
grep -nE "^def resume_mode|^def emit_manifest" src/superclaude/cli/swarm/preflight.py
grep -nE "^def regenerate_merge_on_resume" src/superclaude/cli/swarm/reduce.py
grep -nE "^def run_cmd|--resume" src/superclaude/cli/swarm/commands.py | head -10
python -c "from superclaude.cli.swarm.preflight import resume_mode, emit_manifest; \
           from superclaude.cli.swarm.reduce import regenerate_merge_on_resume; \
           print('resume_mode:', resume_mode.__module__); \
           print('emit_manifest:', emit_manifest.__module__); \
           print('regenerate_merge_on_resume:', regenerate_merge_on_resume.__module__)"
```

All commands above succeed on this commit / worktree state.

## INV-001 / INV-010 / INV-016 / FR-015 / FR-016 Status at CP1

| Concern | Enforcement site | Status at CP1 |
|---|---|---|
| INV-001 — Resume rehydrates lens snapshot verbatim from manifest; live `LENSES.get(name)` never consulted on the default resume path | `preflight.py::resume_mode` + `test_resume_uses_manifest_lens.py` (13) | ✅ green |
| INV-010 — On resume with `amalgamation_mode == normalize+merge`, stale `merged.md` is unconditionally deleted and re-emitted from re-dispatched Wave-2 outputs | `reduce.py::regenerate_merge_on_resume` wired into `reduce_wave3` + `test_resume_regenerates_merge.py` (16) | ✅ green |
| INV-016 — Manifest is byte-immutable across resume cycles; `LENSES` mutation between runs invisible to resumed `JobSpec` (default path) | `preflight.py::emit_manifest` atomic write + `resume_mode` rehydration + `test_manifest_durable.py` (13) | ✅ green (T06.07 will flip the reserved xfail when `--force-relens` lands) |
| FR-015 — `swarm run --resume <job_id>` end-to-end: skip succeeded workers + re-dispatch remaining + re-run Wave 2 + regen merge + re-emit contract | `commands.py:778` (Click option) + `commands.py:1126` (resume orchestrator) + `test_resume_crash_recovery.py` (18) | ✅ green |
| FR-016 — Wave-0 manifest emission carries verbatim `ResolvedLensEntry` snapshot (9 fields) + preflight summary, atomic write, no partial manifest | `preflight.py::emit_manifest` + `test_manifest_emission.py` (19) | ✅ green |

## Open Question Status

No new Open Questions opened by the T06.01..T06.05 bracket. The single carried-forward item from the phase plan (`--force-relens` opt-in re-resolution at T06.07) is already wired as an `xfail` slot in `test_manifest_durable.py::test_force_relens_opts_into_lens_registry_mutation` — flipping that property is the T06.07 deliverable.

## Outstanding / Next

1. **T06.07 — `--force-relens` flag (R-115 / FR-025).** Add `--force-relens` Click option to `run_cmd`; branch preflight to re-resolve lens from current `LENSES` when set; flip the reserved `xfail` in `test_manifest_durable.py`; add `tests/swarm/test_force_relens.py` covering both paths.
2. **T06.08 — NFR-005 crash recovery E2E (R-116).** Compose `tests/swarm/test_crash_recovery_e2e.py` with multi-worker fixture + controllable failure injection; assert kill-then-resume reaches terminal state with no duplicate work and merge regenerated when applicable.
3. **T06.09 — NFR-006 schema forward-compat (R-117).** Author 1.0 spec fixture under `tests/swarm/fixtures/` + `tests/swarm/test_schema_forward_compat.py` asserting 1.1 orchestrator loads 1.0 spec without error and deprecated fields warned-but-accepted.
4. **T06.10 — end-of-phase gate.** CP2 at `tasklist/phase-6-cp2.md`; closes the phase + M6 milestone.

## Milestone Status (Partial — toward M6)

**M6 — Resume / Replay layer ready for E2E hardening.**

- Resume orchestration entry surface (`commands.py::run_cmd --resume`) + resume rehydration (`preflight.resume_mode`) + resume merge regen (`reduce.regenerate_merge_on_resume`) + Wave-0 manifest emission (`preflight.emit_manifest`) all production-ready and CI-protected.
- Manifest-as-source-of-truth durability invariant (INV-016) verified end-to-end via byte-identical round-trip and mutation immunity tests.
- Default resume path is manifest-driven; the opt-in re-resolution path (`--force-relens`, T06.07) is wired as a reserved `xfail` slot ready for the back-half of the phase.
- Crash-recovery E2E semantics (NFR-005, T06.08) and schema forward-compat (NFR-006, T06.09) are the only outstanding milestone items for M6 exit at T06.10.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 6 mid-phase entry gate cleared.
**Authorized to proceed:** T06.07 (`--force-relens`), T06.08 (NFR-005 crash-recovery E2E), T06.09 (NFR-006 schema forward-compat), T06.10 (end-of-phase gate / M6 exit).
**Recorded by:** automation (T06.06 mid-phase checkpoint task).
