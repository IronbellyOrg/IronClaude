# D-0032 — COMP-006 HomeIsolation integrated component contract (Task T02.11)

**Task**: T02.11 (Phase 2 — cliEval harness)
**Tier**: STRICT
**Risk**: Medium (scope — cross-cutting per-eval isolation)
**Roadmap**: COMP-006 (FR-ISO1 + FR-ISO2 + install_hooks adapter surface)
**Cross-links**: D-0026 (DM-006 record, T02.04), D-0027 (IsolationLayers probe, T02.05), D-0028 (FR-ISO1 method surface, T02.07), D-0029 (FR-ISO2 containment guard, T02.08), D-0030 (NFR-SEC2 attack matrix, T02.09), D-0031 (NFR-SEC3 hard guard, T02.10), D-0033 (NFR-ISO2 atomic-setup wrapper, T02.13 — downstream), D-0034 (install_hooks adapter, T02.14 — downstream)

## Goal

COMP-006 finalization. `superclaude.cli.eval.HomeIsolation` is now the
single per-eval isolation primitive the cliEval harness mounts on top of
the four `IsolationLayers` guarantees (cwd / git ceiling / plugin dir /
settings dir). The integrated contract bundles three deliverables that
landed independently across T02.04 → T02.10:

| Deliverable | Source | What it contributes to COMP-006 |
|---|---|---|
| DM-006 frozen record | T02.04 / D-0026 | The four immutable fields (`eval_id`, `home_root`, `session_id`, `time_offset_sec`); FR-SCH2 re-validation in `__post_init__`. |
| FR-ISO1 method surface | T02.07 / D-0028 | `setup`, `env`, `teardown(keep)`, `state_path(suffix)`; the `home_path` / `is_set_up` properties; OQ-8 gating of `CLAUDE_FAKE_TIME_OFFSET`. |
| FR-ISO2 containment guard | T02.08 / D-0029 | The three-check defense-in-depth invocation of `containment_guard` from inside `setup`, with `config: EvalConfig` required keyword-only. |

T02.11 adds the **integrated** contract — the four method surface bullets
fixed by the T02.11 acceptance criteria, exercised as one round-trip
unit rather than method-by-method.

## Integrated contract (T02.11 AC)

### AC1 — COMP-006 method surface

`HomeIsolation` exposes exactly four COMP-006 methods, each with the
declared signature:

| Method | Signature | Side effects |
|---|---|---|
| `setup` | `(*, config: EvalConfig) -> Path` | `mkdir(parents=True, exist_ok=True)` on `home_root`; `tempfile.mkdtemp(prefix=f"{eval_id}-", dir=home_root)`; populate private `_home_path` slot; invoke `containment_guard` AFTER mkdtemp and BEFORE return; return per-eval HOME path. |
| `env` | `() -> dict[str, str]` | Pure. Returns `{HOME, CLAUDE_SESSION_ID}` always plus `CLAUDE_FAKE_TIME_OFFSET` iff `time_offset_sec != 0`. Fresh dict each call. |
| `teardown` | `(keep: bool) -> None` | `keep=False` removes the per-eval HOME via `shutil.rmtree`; `keep=True` preserves it. Always clears the private slot, even on exception. No-op when `setup` never ran. |
| `state_path` | `(suffix: str) -> Path` | Pure. Rejects absolute paths and `..` components; returns `home_path / suffix` after the lexical containment check. |

Verified by `TestComp006MethodSurface` (5 tests) via `inspect.signature`
introspection and a positive instance-callability probe.

### AC2 — `state_path` anchored under `home_root`

`state_path(suffix)` returns paths that satisfy BOTH containment
predicates simultaneously:

* `is_relative_to(home_path)` — the per-eval HOME the orchestrator
  created (FR-ISO1).
* `is_relative_to(home_root)` — the scratch root the orchestrator
  declared (T02.11 AC, mirroring the AC12 allowlist surface).

The two predicates are equivalent in the happy path because
`home_path.parent == home_root`, but the T02.11 AC pins the second
explicitly so reporters can validate per-eval artifact roots without
fetching `home_path` from a deceased instance. Negative paths
(`/etc/passwd`, `../escape`) raise `ValueError` with the documented
messages; the `state_path` accessor itself raises `RuntimeError` when
called before `setup` or after `teardown`.

Verified by `TestStatePathIsAnchoredUnderHomeRoot` (6 tests).

### AC3 — `teardown` keep/remove semantics

`teardown(keep=True)` MUST preserve the per-eval HOME on disk so the
NFR-ISO2 atomic-setup wrapper (T02.13) and the `--keep-home` orchestrator
flag (T03.18) can post-mortem the directory. `teardown(keep=False)` MUST
remove the directory tree. BOTH branches clear the private `_home_path`
slot, so subsequent calls to `env` / `state_path` raise
`RuntimeError("HomeIsolation.setup() must be called before accessing home_path")`
instead of silently consuming a stale (possibly deleted) path. `teardown`
called when `setup` never ran is a no-op — the orchestrator is permitted
to wrap `teardown` in an unconditional `finally` clause.

Verified by `TestTeardownKeepFlag` (7 tests) covering: file-content
preservation under `keep=True`, removal under `keep=False`, slot
clearing under both branches, no-op when `setup` never ran, and
`RuntimeError` on post-teardown `env` / `state_path`.

### AC4 — Integrated lifecycle

The `setup -> env -> state_path -> teardown` round-trip works on a fresh
instance, on a re-setup after a teardown, and across parallel siblings
(`ThreadPoolExecutor(max_workers=8)`). The `env` dict round-trips with
`HOME=str(home_path)` and `CLAUDE_SESSION_ID=session_id`; the
`CLAUDE_FAKE_TIME_OFFSET` toggle gates correctly on `time_offset_sec`.

Verified by `TestIntegratedLifecycle` (4 tests) + `TestParallelSiblings`
(1 test, 8 parallel siblings).

### Containment guard integration (re-confirmation)

T02.11 re-runs two acceptance checks against the integrated `setup`
path so the COMP-006 contract is owned end-to-end by this module:

* Scratch-root-outside-allowlist surfaces as
  `HomeContainmentViolation(check="scratch_root_allowlist")` from
  inside `setup` (the FR-ISO2 guard cannot be bypassed by going
  through the integrated entry point).
* `setup()` invoked without an explicit `config=` raises
  `TypeError` BEFORE any filesystem write — refusal-before-side-
  effects from D-0029 is preserved.

Verified by `TestContainmentGuardIntegratedIntoSetup` (2 tests).

### DM-006 invariants survive integration

The frozen-dataclass invariants from T02.04 must survive the
integrated lifecycle: the four declared fields stay immutable
post-`setup`, and equality across the four declared fields is unaffected
by the private `_home_path` slot.

Verified by `TestDm006InvariantsSurviveIntegration` (2 tests).

## Install_hooks adapter integration surface (forward-link)

The T02.11 deliverable text mentions "integrating … the install_hooks
adapter" as one of the three integration vectors. The adapter itself
(`deploy_hooks_to(home_path: Path)`) lands in T02.14 / D-0034. COMP-006
exposes the single surface the adapter consumes:

* `HomeIsolation.home_path` (public `@property`) — returns the per-eval
  HOME `mkdtemp`'d by `setup`. The adapter takes a `home_path` argument
  rather than a `HomeIsolation` instance so it can be tested in
  isolation; the orchestrator (T03.16) calls
  `deploy_hooks_to(iso.home_path)` after `iso.setup(config=...)`.

No T02.11 code change is required to support T02.14; the adapter slots
into the existing public surface. This is why the COMP-006 acceptance
criteria do not assert on the adapter directly.

## Files touched

| File | Change |
|---|---|
| `tests/cli/eval/test_home_isolation.py` | New module — 27 tests across 7 test classes covering the four T02.11 AC bullets + containment integration + DM-006 invariant survival. |
| `.dev/releases/current/cliEval/artifacts/D-0032/{spec,notes,evidence}.md` | This deliverable. |
| `.dev/releases/current/cliEval/evidence/T02.11/pytest-T02.11.log` | Captured pytest output (27 passed). |

`src/superclaude/cli/eval/isolation.py` is unchanged — COMP-006 is the
finalization checkpoint that confirms FR-ISO1 + FR-ISO2 round-trip
correctly as one component; no code change is required because T02.07
and T02.08 already implemented the contract on the existing class.

## Acceptance criteria → test mapping

| AC | Source | Verified by |
|---|---|---|
| `HomeIsolation` exposes 4 COMP-006 methods | T02.11 AC | `TestComp006MethodSurface` (5 tests) |
| `state_path(suffix)` is_relative_to(home_root) | T02.11 AC | `TestStatePathIsAnchoredUnderHomeRoot::test_state_path_is_relative_to_home_root` |
| `state_path(suffix)` is_relative_to(home_path) | FR-ISO1 | `TestStatePathIsAnchoredUnderHomeRoot::test_state_path_is_also_relative_to_home_path` |
| `state_path(suffix)` rejects absolute/.. suffixes | FR-ISO1 | `test_state_path_rejects_absolute_suffix`, `test_state_path_rejects_dotdot_components` |
| `state_path()` pre-setup raises `RuntimeError` | FR-ISO1 | `test_state_path_before_setup_raises_runtimeerror` |
| `teardown(keep=True)` preserves HOME | T02.11 AC | `TestTeardownKeepFlag::test_teardown_keep_true_preserves_home_on_disk` |
| `teardown(keep=False)` removes HOME | T02.11 AC | `test_teardown_keep_false_removes_home_from_disk` |
| `teardown` clears slot under both branches | FR-ISO1 | `test_teardown_clears_slot_on_keep_true`, `test_teardown_clears_slot_on_keep_false` |
| `teardown` is no-op when setup never ran | FR-ISO1 | `test_teardown_is_noop_when_setup_never_ran` |
| Post-teardown `env`/`state_path` raise RuntimeError | FR-ISO1 | `test_env_after_teardown_raises_runtimeerror`, `test_state_path_after_teardown_raises_runtimeerror` |
| Full round-trip `setup -> env -> state_path -> teardown` | T02.11 AC | `TestIntegratedLifecycle::test_full_lifecycle_round_trip` |
| Re-setup after teardown succeeds with fresh HOME | T02.11 AC | `test_re_setup_after_teardown_returns_fresh_home` |
| `CLAUDE_FAKE_TIME_OFFSET` gated on `time_offset_sec` | OQ-8 (DOC-OQ8) | `test_env_with_time_offset_includes_fake_time_offset`, `test_env_without_time_offset_omits_fake_time_offset` |
| `setup` rejects scratch-root outside allowlist | D-0029 (re-confirm) | `TestContainmentGuardIntegratedIntoSetup::test_setup_rejects_scratch_root_outside_allowlist` |
| `setup` requires explicit `config=` (no bypass) | D-0029 (re-confirm) | `test_setup_requires_explicit_config` |
| Parallel siblings under one scratch root | FR-ISO1 concurrency | `TestParallelSiblings::test_parallel_lifecycle_round_trip` (8-way) |
| DM-006 fields immutable post-setup | DM-006 (re-confirm) | `TestDm006InvariantsSurviveIntegration::test_fields_are_immutable_after_setup` |
| DM-006 equality unaffected by private slot | DM-006 | `test_equality_unchanged_post_setup` |

## Test result

`uv run pytest tests/cli/eval/test_home_isolation.py -v` → **27 passed in 0.15s**
(log: `.dev/releases/current/cliEval/evidence/T02.11/pytest-T02.11.log`).

Phase-2 isolation suite cumulative
(`tests/cli/eval/test_home_isolation_extend.py test_path_containment.py test_defense_in_depth.py test_hard_guard_real_home.py test_home_isolation.py`) →
**137 passed in 0.32s** — no regression across the upstream four
deliverables.

## Reserved for follow-up tasks

| Item | Reserved to | Reason |
|---|---|---|
| `setup_failed` artifact tag on guard failure | T02.13 / D-0033 | NFR-ISO2 atomic-setup wrapper owns the tagging contract; T02.11 only asserts the partial-HOME preservation observable. |
| Hook-deploy ordering (`mkdtemp → guard → deploy_hooks_to`) | T02.14 / D-0034 | Requires the adapter to exist; the sequence test belongs in the adapter deliverable. |
| Performance baseline at 15-eval parallel | T02.15 / D-0035 | COMP-006 contract is functional; the perf budget lands in the dedicated benchmark module. |

## Cross-links

* DM-006 record contract: `tests/cli/eval/test_isolation_dataclass.py` (T02.04 / D-0026).
* COMP-012 probe pin: `tests/cli/eval/test_isolation_layers_probe.py` (T02.05 / D-0027).
* FR-ISO1 method surface: `tests/cli/eval/test_home_isolation_extend.py` (T02.07 / D-0028).
* FR-ISO2 containment guard: `tests/cli/eval/test_path_containment.py` (T02.08 / D-0029).
* NFR-SEC2 attack matrix: `tests/cli/eval/test_defense_in_depth.py` (T02.09 / D-0030).
* NFR-SEC3 hard guard: `tests/cli/eval/test_hard_guard_real_home.py` (T02.10 / D-0031).
* COMP-006 integrated contract: `tests/cli/eval/test_home_isolation.py` (T02.11 / D-0032 — this deliverable).
* NFR-ISO2 atomic setup: T02.13 / D-0033 (downstream).
* COMP-014 hook adapter: T02.14 / D-0034 (downstream).
