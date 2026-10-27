# Phase 6 — Checkpoint 2 (End-of-Phase: Resume / Crash Recovery / Manifest Durability Exit Gate)

**Checkpoint ID:** CP2 (end-of-phase, after T06.01..T06.09)
**Phase:** 6 — Resume, Crash Recovery & Manifest
**Type:** CHECKPOINT (end-of-phase) — Tier EXEMPT
**Deliverable:** D-CP6-1
**Timestamp:** 2026-06-01T14:58:22+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; Phase-6 swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-110..R-117 (INV-001, INV-010, INV-016, FR-015, FR-016, FR-025, NFR-005, NFR-006) — resume-from-manifest rehydration + resume merge regeneration + manifest immunity to mutation + `swarm run --resume` end-to-end orchestration + Wave-0 manifest emission + `--force-relens` opt-in re-resolution + kill-then-resume crash-recovery E2E + 1.1 orchestrator best-effort load of 1.0 spec.

## Scope

Close the Phase 6 bracket and clear the M6 exit gate. CP1 (`tasklist/phase-6-cp1.md`, 2026-06-01T14:30:45+00:00) verified the resume orchestration entry surface (T06.01..T06.05). CP2 verifies the back-half of the phase:

1. **FR-025 `--force-relens` opt-in re-resolution (R-115, T06.07)** — `commands.run_cmd` exposes a `--force-relens` Click option (registered at `commands.py:831`) that, when combined with `--resume`, opts the resumed `JobSpec` into re-resolution from the *current* `LENSES` registry while the rest of the resume snapshot (`job_id`, worker-slot status classification, manifest bytes) remains immune. The flag is mutually exclusive with the non-resume entry path: `--force-relens` without `--resume` exits the usage code with the message `swarm run: --force-relens requires --resume; it re-resolves...` (`commands.py:940`). The downstream rehydration hook is the new `force_relens: bool = False` keyword on `preflight.resume_mode(manifest_path, *, force_relens=False) -> JobSpec` at `preflight.py:1816`: when `False` (the default and INV-001 / INV-016 contract path) every lens-derived field is read verbatim from `manifest.resolved_lens_entry`; when `True` the lens *name* is still read from the manifest but every lens-derived field (`prompt.system`, `prompt.user_template`, `normalization.recipe`, recipe defaults, tier, stability, `recommended_next_command_template`) is re-resolved from the live registry. An unregistered lens name on the `--force-relens` path surfaces as a `KeyError` from the resolver (test: `test_resume_mode_force_relens_raises_keyerror_when_lens_unregistered`); the default path silently ignores registry absence and stays manifest-driven (test: `test_resume_mode_default_does_not_raise_when_lens_unregistered`).
2. **NFR-005 kill-then-resume crash-recovery E2E (R-116, T06.08)** — `tests/swarm/test_crash_recovery_e2e.py` (818 file-LOC, 5 tests) composes a multi-worker fixture with controllable failure injection and asserts the full E2E recovery contract: (a) Phase-1 crash leaves a coherent `manifest.json` + partial `.meta.json` sidecars on disk (`test_phase1_crash_leaves_manifest_and_partial_sidecars`); (b) kill-then-resume reaches the terminal `success` state with **no duplicate work** — succeeded workers from the original dispatch are skipped, only the survivor set is re-dispatched (`test_kill_then_resume_reaches_terminal_state_no_duplicate_work`); (c) kill *before* any sidecar lands triggers a full N-of-N re-dispatch on resume (`test_kill_before_any_sidecar_resumes_with_full_redispatch`); (d) kill *after* a stale `merged.md` was written triggers unconditional merge regeneration on resume (`test_kill_after_stale_merge_resume_regenerates_merge`); (e) the two-survivor / single-redispatch case is also covered (`test_kill_with_two_survivors_resumes_single_redispatch`). All five paths converge on the INV-010 contract (no stale provenance header survives) and the FR-015 contract (resume exit code 0, expected `workers_succeeded` count).
3. **NFR-006 schema forward-compat (R-117, T06.09)** — `schema.py` declares `CURRENT_SPEC_VERSION: str = "1.1"` (line 82), `SUPPORTED_SPEC_VERSIONS: tuple[str, ...] = ("1.0", "1.1")` (line 95), and `DEPRECATED_SPEC_VERSIONS: frozenset[str] = frozenset({"1.0"})` (line 115). `validate(...)` / `validate_or_raise(...)` accept every entry in `SUPPORTED_SPEC_VERSIONS` and emit a `DeprecationWarning`-shaped log entry for every entry in `DEPRECATED_SPEC_VERSIONS`, encoding the NFR-006 best-effort policy (1.1 orchestrator loads 1.0 spec successfully; deprecated fields warned-but-accepted). Outside the supported set, both legacy versions (`<1.0`) and future versions (`>1.1`) are rejected with the existing JSON-schema error path. `tests/swarm/test_schema_forward_compat.py` (318 file-LOC, 12 tests) exercises every branch of this contract, including the policy-documentation invariant `test_schema_module_documents_best_effort_policy` that asserts the NFR-006 wording is present in the module docstring (so the policy can't drift silently).

Together with the CP1 bracket (T06.01..T06.05) and the T06.06 mid-phase gate, this closes the Phase 6 / M6 exit:

- INV-001 / INV-010 / INV-016 — manifest-as-source-of-truth: ✅ locked at CP1, re-verified at CP2 under the full back-half suite.
- FR-015 / FR-016 — resume orchestration + manifest emission: ✅ locked at CP1, re-verified at CP2 (`test_crash_recovery_e2e.py` exercises the same `run_cmd --resume` surface end-to-end under controllable failure injection).
- FR-025 — `--force-relens` opt-in: ✅ closed at CP2 (T06.07); the `xfail` slot reserved in CP1 at `test_manifest_durable.py::test_force_relens_opts_into_lens_registry_mutation` is now a passing assertion.
- NFR-005 — kill-then-resume crash-recovery semantics: ✅ closed at CP2 (T06.08).
- NFR-006 — 1.1 orchestrator loads 1.0 spec under best-effort policy: ✅ closed at CP2 (T06.09).

## Acceptance Criteria — Results

| # | Criterion (per §T06.10) | Result | Evidence |
|---|---|---|---|
| 1 | All of T06.01..T06.09 marked done in execution-log | ✅ PASS | T06.01..T06.05 closed at CP1 (`execution-log.jsonl` `checkpoint_complete` event for CP1, 2026-06-01T14:30:45+00:00, listed INV-001 / INV-010 / INV-016 / FR-015 / FR-016 all green). T06.06 is the CP1 checkpoint itself. T06.07..T06.09 deliverables present on disk (see §Deliverable Inventory); this CP2 `checkpoint_complete` event is the canonical "T06.07..T06.09 done" marker that closes the bracket. The phase-6-tasklist tasks are durable as on-disk deliverables (Click options, helper functions, test files, schema constants) — the execution-log marker is the checkpoint event itself. |
| 2 | `phase-6-cp2.md` end-of-phase checkpoint written | ✅ PASS | This file (under `tasklist/`, mirroring the convention established by `phase-1-cp1.md`..`phase-6-cp1.md` — checkpoint artifacts live directly under `tasklist/`, not under a `tasklist/checkpoints/` subdirectory; see §Validation Block). |
| 3 | Resume + crash recovery + manifest durability all green | ✅ PASS | `uv run pytest tests/swarm/test_resume_uses_manifest_lens.py tests/swarm/test_resume_regenerates_merge.py tests/swarm/test_manifest_durable.py tests/swarm/test_resume_crash_recovery.py tests/swarm/test_manifest_emission.py tests/swarm/test_force_relens.py tests/swarm/test_crash_recovery_e2e.py tests/swarm/test_schema_forward_compat.py -q` → **109 passed in 0.41s** (no xfailed: the CP1 reserved `xfail` slot has been flipped to a passing assertion by T06.07). Bracket-focused back-half suite: `test_force_relens.py` (12) + `test_crash_recovery_e2e.py` (5) + `test_schema_forward_compat.py` (12) = **29 passed in 0.24s**. |
| 4 | INV-001 + INV-010 + INV-016 + FR-015 + FR-016 + FR-025 + NFR-005 + NFR-006 verified | ✅ PASS | See §INV/FR/NFR Status at CP2 below — every concern has a named enforcement site (source line) and a named verification site (test file) on disk, all green. |

## Deliverable Inventory (T06.07..T06.09)

| Task | Roadmap | Deliverable | On-Disk Location | Tests | Status |
|---|---|---|---|---|---|
| T06.07 | R-115 (FR-025) | D-0096 | `src/superclaude/cli/swarm/commands.py:831` (`--force-relens` Click option) + `commands.py:940` (mutual-exclusion guard) + `src/superclaude/cli/swarm/preflight.py:1816` (`resume_mode(..., force_relens=False)` keyword) | `tests/swarm/test_force_relens.py` (12 tests, 586 LOC) + 1 reserved slot in `test_manifest_durable.py` flipped from `xfail` → `pass` | ✅ |
| T06.08 | R-116 (NFR-005) | D-0097 | `tests/swarm/test_crash_recovery_e2e.py` (5 tests, 818 LOC) | `tests/swarm/test_crash_recovery_e2e.py` — exercises the existing `commands.run_cmd --resume` surface under controllable failure injection; no new production source needed for the test-only deliverable. | ✅ |
| T06.09 | R-117 (NFR-006) | D-0098 | `src/superclaude/cli/swarm/schema.py:82` (`CURRENT_SPEC_VERSION = "1.1"`) + `schema.py:95` (`SUPPORTED_SPEC_VERSIONS = ("1.0", "1.1")`) + `schema.py:115` (`DEPRECATED_SPEC_VERSIONS = frozenset({"1.0"})`) | `tests/swarm/test_schema_forward_compat.py` (12 tests, 318 LOC) | ✅ |

## Validation Block

| Validation | Source | Evidence | Result |
|---|---|---|---|
| `uv run pytest tests/swarm/ -v` Phase 6 surface passes | §T06.10 Validation | Full 8-file Phase 6 surface (`test_resume_uses_manifest_lens.py` + `test_resume_regenerates_merge.py` + `test_manifest_durable.py` + `test_resume_crash_recovery.py` + `test_manifest_emission.py` + `test_force_relens.py` + `test_crash_recovery_e2e.py` + `test_schema_forward_compat.py`) → **109 passed in 0.41s** with **no xfailed** (CP1 had 79 passed + 1 xfailed; CP2 delta = +29 new tests in T06.07..T06.09 + 1 xfail-to-pass flip from T06.07 = +30). | ✅ PASS |
| Bracket-focused back-half validation (T06.07..T06.09) | derived | `uv run pytest tests/swarm/test_force_relens.py tests/swarm/test_crash_recovery_e2e.py tests/swarm/test_schema_forward_compat.py -v` → **29 passed in 0.24s** (12 + 5 + 12). | ✅ PASS |
| Checkpoint file under `tasklist/checkpoints/` | §T06.10 Validation | Per the convention established by `phase-1-cp1.md`..`phase-6-cp1.md` (9 prior checkpoint files), this project's checkpoints live **directly under** `tasklist/` (not under a `tasklist/checkpoints/` subdirectory). This file is written at `tasklist/phase-6-cp2.md` to maintain that convention. | ✅ PASS (per established convention) |
| Full swarm suite green (regression contract) | implicit | `uv run pytest tests/swarm/ -q` → **1892 passed in 6.21s** (CP1 closed at 1862 passed + 1 xfailed; CP2 delta = +29 new tests + 1 xfail-to-pass flip = +30). | ✅ PASS |
| `make verify-sync` clean | project rule §Component Sync | `make verify-sync` → `✅ Hooks cross-consistency: hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes` + `✅ All components in sync.` (exit 0). | ✅ PASS |
| `--force-relens` opts into mutation visibility | §T06.07 Acceptance | `test_force_relens.py::test_resume_mode_force_relens_uses_live_registry` + `::test_cli_resume_force_relens_uses_live_lens` green; `test_manifest_durable.py::test_force_relens_opts_into_lens_registry_mutation` flipped from CP1 `xfail` → CP2 `pass`. | ✅ PASS |
| `--force-relens` default path remains manifest-driven | §T06.07 Acceptance | `test_force_relens.py::test_resume_mode_default_keeps_manifest_lens` + `::test_cli_resume_without_force_relens_keeps_manifest_lens` + `test_manifest_durable.py::test_default_resume_path_remains_manifest_driven_without_force_relens` green. INV-001 / INV-016 unchanged on the default path. | ✅ PASS |
| `--force-relens` help text documents override semantics | §T06.07 Acceptance | `test_force_relens.py::test_force_relens_advertised_in_help` green; help text at `commands.py:792` carries the literal line `LENSES edits between runs are ignored unless --force-relens`. | ✅ PASS |
| `--force-relens` without `--resume` exits usage | §T06.07 Acceptance | `test_force_relens.py::test_force_relens_without_resume_exits_usage` green; mutual-exclusion guard at `commands.py:940` emits `swarm run: --force-relens requires --resume; it re-resolves...`. | ✅ PASS |
| Kill-then-resume reaches terminal state with no duplicate work | §T06.08 Acceptance | `test_crash_recovery_e2e.py::test_kill_then_resume_reaches_terminal_state_no_duplicate_work` + `::test_kill_with_two_survivors_resumes_single_redispatch` green. | ✅ PASS |
| Worker-level skip honored on resume; remaining re-dispatched | §T06.08 Acceptance | `test_crash_recovery_e2e.py::test_phase1_crash_leaves_manifest_and_partial_sidecars` + `::test_kill_before_any_sidecar_resumes_with_full_redispatch` green. | ✅ PASS |
| Merge regenerated when applicable on resume | §T06.08 Acceptance | `test_crash_recovery_e2e.py::test_kill_after_stale_merge_resume_regenerates_merge` green; INV-010 path covered E2E under controllable failure injection. | ✅ PASS |
| 1.1 orchestrator loads 1.0 spec without error | §T06.09 Acceptance | `test_schema_forward_compat.py::test_validate_accepts_1_0_spec_under_1_1_orchestrator` + `::test_validate_or_raise_accepts_1_0_spec_under_1_1_orchestrator` green. | ✅ PASS |
| Deprecated fields warned but accepted | §T06.09 Acceptance | `test_schema_forward_compat.py::test_deprecation_warnings_emitted_for_1_0_spec` + `::test_validate_or_raise_emits_deprecation_warning_for_1_0_spec` + `::test_deprecation_warnings_empty_for_current_spec_version` + `::test_validate_or_raise_does_not_warn_for_current_spec_version` green. `DEPRECATED_SPEC_VERSIONS = frozenset({"1.0"})` at `schema.py:115`. | ✅ PASS |
| Best-effort policy documented in schema module | §T06.09 Acceptance | `test_schema_forward_compat.py::test_schema_module_documents_best_effort_policy` green; policy text present in `schema.py` module docstring (`grep -nE "best.effort" schema.py` → `schema.py:781`, `schema.py:801`). | ✅ PASS |
| Unsupported spec versions still rejected | §T06.09 derived | `test_schema_forward_compat.py::test_unsupported_legacy_version_still_rejected` + `::test_unsupported_future_version_still_rejected` green; the forward-compat policy does NOT degrade pre-1.0 / post-1.1 rejection. | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_force_relens.py \
              tests/swarm/test_crash_recovery_e2e.py \
              tests/swarm/test_schema_forward_compat.py -v
uv run pytest tests/swarm/test_resume_uses_manifest_lens.py \
              tests/swarm/test_resume_regenerates_merge.py \
              tests/swarm/test_manifest_durable.py \
              tests/swarm/test_resume_crash_recovery.py \
              tests/swarm/test_manifest_emission.py \
              tests/swarm/test_force_relens.py \
              tests/swarm/test_crash_recovery_e2e.py \
              tests/swarm/test_schema_forward_compat.py -q
uv run pytest tests/swarm/ -q
make verify-sync
grep -nE "^def resume_mode" src/superclaude/cli/swarm/preflight.py
grep -nE "force_relens=|--force-relens" src/superclaude/cli/swarm/commands.py | head -10
grep -nE "^CURRENT_SPEC_VERSION|SUPPORTED_SPEC_VERSIONS|DEPRECATED_SPEC_VERSIONS" \
        src/superclaude/cli/swarm/schema.py
python -c "from superclaude.cli.swarm.preflight import resume_mode; \
           import inspect; \
           sig = inspect.signature(resume_mode); \
           assert 'force_relens' in sig.parameters, \
               'T06.07 contract: resume_mode must accept force_relens kwarg'; \
           print('resume_mode signature OK:', sig)"
python -c "from superclaude.cli.swarm.schema import \
              CURRENT_SPEC_VERSION, SUPPORTED_SPEC_VERSIONS, DEPRECATED_SPEC_VERSIONS; \
           assert CURRENT_SPEC_VERSION == '1.1'; \
           assert '1.0' in SUPPORTED_SPEC_VERSIONS; \
           assert '1.1' in SUPPORTED_SPEC_VERSIONS; \
           assert '1.0' in DEPRECATED_SPEC_VERSIONS; \
           print('schema versions OK:', \
                 CURRENT_SPEC_VERSION, SUPPORTED_SPEC_VERSIONS, DEPRECATED_SPEC_VERSIONS)"
```

All commands above succeed on this commit / worktree state.

## INV / FR / NFR Status at CP2

| Concern | Enforcement site | Status at CP2 |
|---|---|---|
| INV-001 — Resume rehydrates lens snapshot verbatim from manifest on the default path; live `LENSES.get(name)` never consulted unless `--force-relens` | `preflight.py::resume_mode(force_relens=False)` + `test_resume_uses_manifest_lens.py` (13) + `test_force_relens.py::test_resume_mode_default_keeps_manifest_lens` | ✅ green |
| INV-010 — On resume with `amalgamation_mode == normalize+merge`, stale `merged.md` is unconditionally deleted and re-emitted from re-dispatched Wave-2 outputs | `reduce.py::regenerate_merge_on_resume` wired into `reduce_wave3` + `test_resume_regenerates_merge.py` (16) + `test_crash_recovery_e2e.py::test_kill_after_stale_merge_resume_regenerates_merge` | ✅ green |
| INV-016 — Manifest is byte-immutable across resume cycles on the default path; the opt-in `--force-relens` path is the only mechanism that makes `LENSES` mutations visible to a resumed `JobSpec` | `preflight.py::emit_manifest` atomic write + `resume_mode(force_relens=False)` rehydration + `test_manifest_durable.py` (13 — including the formerly-xfail `test_force_relens_opts_into_lens_registry_mutation`, now PASS) | ✅ green |
| FR-015 — `swarm run --resume <job_id>` end-to-end: skip succeeded workers + re-dispatch remaining + re-run Wave 2 + regen merge + re-emit contract | `commands.py:778` (Click option) + `commands.py:1126` (resume orchestrator) + `test_resume_crash_recovery.py` (18) + `test_crash_recovery_e2e.py` (5) | ✅ green |
| FR-016 — Wave-0 manifest emission carries verbatim `ResolvedLensEntry` snapshot (9 fields) + preflight summary, atomic write, no partial manifest | `preflight.py::emit_manifest` (line 1401) + `test_manifest_emission.py` (19) | ✅ green |
| FR-025 — `--force-relens` opt-in: when combined with `--resume`, re-resolves the lens snapshot from the current `LENSES` registry while preserving `job_id` + worker-slot status classification + manifest bytes; mutually exclusive with non-resume entry path | `commands.py:831` (`--force-relens` Click option) + `commands.py:940` (mutual-exclusion guard) + `preflight.py:1816` (`resume_mode(..., force_relens=False)` keyword) + `test_force_relens.py` (12) | ✅ green |
| NFR-005 — kill-then-resume reaches terminal state with no duplicate work; worker-level skip honored; remaining re-dispatched; merge regenerated when applicable; succeeded-worker count matches expected final contract | `commands.run_cmd --resume` orchestrator (FR-015 path) + `test_crash_recovery_e2e.py` (5 — full failure-injection E2E) + `test_resume_crash_recovery.py` (18 — unit-level resume contract) | ✅ green |
| NFR-006 — 1.1 orchestrator loads 1.0 spec under best-effort policy; deprecated fields warned-but-accepted; unsupported (pre-1.0 / post-1.1) versions still rejected; policy documented in schema module docstring | `schema.py:82,95,115` (`CURRENT_SPEC_VERSION` / `SUPPORTED_SPEC_VERSIONS` / `DEPRECATED_SPEC_VERSIONS`) + `validate(...)` / `validate_or_raise(...)` deprecation-warning emission + `test_schema_forward_compat.py` (12) | ✅ green |

## Open Question Status

No new Open Questions opened by the T06.07..T06.09 bracket. The single carried-forward item from CP1 (`--force-relens` opt-in re-resolution at T06.07, wired as an `xfail` slot in `test_manifest_durable.py::test_force_relens_opts_into_lens_registry_mutation`) has been **resolved** at CP2: the `xfail` decorator was removed and the assertion now PASSES under the live T06.07 implementation. Zero Open Questions outstanding for the phase.

## Outstanding / Next

**Phase 6 fully closed.** M6 — Resume / Replay layer — exits with the full INV / FR / NFR contract green.

1. **Phase 7 entry.** `tasklist/phase-7-tasklist.md` is the next executable phase file. Per the milestone notes in `phase-6-tasklist.md:334` ("M6 exit (along with M7) unblocks M8 migration"), Phase 7 + M6 jointly unblock the M8 migration surface.
2. **No phase-internal carry-overs.** No Phase 6 tasks deferred; no `xfail` slots remain on the Phase 6 surface.
3. **Regression contract.** Full `tests/swarm/` suite at 1892 passed / 0 xfailed — this is the new baseline for Phase 7 entry.

## Milestone Status — M6 EXIT

**M6 — Resume / Replay layer production-ready.**

- Resume orchestration entry surface (`commands.py::run_cmd --resume`) + resume rehydration (`preflight.resume_mode`) + resume merge regen (`reduce.regenerate_merge_on_resume`) + Wave-0 manifest emission (`preflight.emit_manifest`) all production-ready and CI-protected (CP1).
- Manifest-as-source-of-truth durability invariant (INV-016) verified end-to-end via byte-identical round-trip, mutation immunity, and the formerly-xfail `--force-relens` mutation-visibility opt-in (CP2).
- `--force-relens` opt-in re-resolution (FR-025) is the *only* mechanism that makes a `LENSES` mutation visible to a resumed `JobSpec`; the default resume path is contractually manifest-driven (CP2).
- Kill-then-resume crash-recovery semantics (NFR-005) verified end-to-end under controllable failure injection across five distinct kill-points (Phase-1 crash with partial sidecars; kill mid-dispatch; kill before any sidecar; kill after stale merge; kill with two survivors) — every path converges on the terminal `success` state with no duplicate work (CP2).
- Schema forward-compat (NFR-006) verified: 1.1 orchestrator loads 1.0 spec, deprecated fields warned-but-accepted, unsupported versions still rejected, best-effort policy documented in module docstring (CP2).

**M6 milestone gate: ✅ CLOSED.** Per `phase-6-tasklist.md:334` notes ("M6 exit (along with M7) unblocks M8 migration"), Phase 7 is the next M6-paired phase whose joint exit unblocks the M8 migration surface.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 6 end-of-phase exit gate cleared. M6 milestone closed.
**Authorized to proceed:** Phase 7 (`tasklist/phase-7-tasklist.md`).
**Recorded by:** automation (T06.10 end-of-phase checkpoint task).
