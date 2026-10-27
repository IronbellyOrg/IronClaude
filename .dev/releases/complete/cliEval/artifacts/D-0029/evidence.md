# D-0029 — Evidence

## Acceptance-criteria check

| Criterion | Result |
|---|---|
| `HomeContainmentViolation` exposes `check`, `home_path`, `scratch_root`, `eval_id`, `detail` | PASS — `src/superclaude/cli/eval/isolation.py:112-167` |
| `containment_guard(home_path, scratch_root, eval_id, *, config)` runs three layered checks | PASS — `src/superclaude/cli/eval/isolation.py:170-299` |
| `config` is required (no `None` default, no fallback synthesis) | PASS — `containment_guard` signature `isolation.py:170-176`; `HomeIsolation.setup` signature `isolation.py:386` |
| Guard runs AFTER `tempfile.mkdtemp` BEFORE any hook deploy | PASS — `HomeIsolation.setup` orders mkdtemp (line 447) → containment_guard (line 466) → return |
| Check 1: eval_id regex re-validated (loader-bypass defense) | PASS — `TestEvalIdReValidation` (12 parametrize cases for non-string + 10 for bad strings) |
| Check 2: allowlist sourced from `EvalConfig.allowed_scratch_roots` only | PASS — `TestScratchRootAllowlist.test_uses_evalconfig_allowed_scratch_roots_as_source_of_truth` |
| Check 2: symlinked scratch root caught | PASS — `test_raises_when_scratch_root_symlinked_outside_allowlist` |
| Check 3: post-mkdtemp `Path.resolve(strict=True)` containment | PASS — `TestSymlinkResolvedContainment` (4 tests + chain) |
| Refusal-before-side-effects (NFR-SEC2): missing config raises `TypeError`, no HOME created | PASS — `test_setup_requires_explicit_config` (asserts `not any(scratch_root.iterdir())`) |
| Partial HOME preserved on guard failure (forensics) | PASS — `test_setup_failure_preserves_partial_home` |
| D-0029 spec.md records the method contract | PASS — `artifacts/D-0029/spec.md` |

## Test results

`uv run pytest tests/cli/eval/test_path_containment.py tests/cli/eval/test_home_isolation_extend.py -v`

**85 passed in 0.24s** — full log at `evidence/T02.08/pytest-T02.08.log`.

Breakdown:
- `test_path_containment.py`: 47 tests (10 + 12 parametrized eval_id checks, 4 allowlist, 5 symlink containment, 5 integration with HomeIsolation.setup, 4 exception payload, 1 hard-guard sanity, 1 chain escape, 5 parametrized canonical-id happy paths)
- `test_home_isolation_extend.py`: 38 tests (T02.07 contract preserved, all 29 setup() callsites now pass explicit config)

Full eval suite (`uv run pytest tests/cli/eval/ -q`) — **449 passed in 1.01s** (no regressions in T01.05, T01.07, T01.19, T02.04, T02.05, T02.07, or T01 loader tests).

## QA re-review

Quality-engineer was re-invoked on the blocker (Issue #1 — home_root-injection bypass). Verdict: **PASS**.

Excerpt:

> The blocker is closed. Evidence:
>
> **1. `containment_guard()` signature now requires `config` (isolation.py:170-176)**
> The previous `config: EvalConfig | None = None` default that synthesized a fallback is gone. Docstring at isolation.py:229-236 explicitly documents the NFR-SEC2 rationale.
>
> **2. `HomeIsolation.setup()` signature now requires `config` (isolation.py:386)**
> The home_root-injection fallback has been removed.
>
> **3. Test pins the refusal contract (test_path_containment.py:475-493)**
> `test_setup_requires_explicit_config` asserts `iso.setup()` raises `TypeError` matching `r"config"` AND `not any(scratch_root.iterdir())` — refusal-before-side-effects per NFR-SEC2. Even the `mkdir(parents=True, exist_ok=True)` on `self.home_root` never runs because Python rejects the call at argument-binding time.
>
> The attack vector "`HomeIsolation(eval_id='E1', home_root=Path('/home/user/.claude'), ...).setup()` passes check 2 trivially" is no longer reachable.

Other findings (Issue #2 hook-deploy ordering, #3 TOCTOU under Barrier, #4 mkdtemp-prefix in test helper, #6 runtime guard on exception field types) remain open and are reserved for follow-up tasks (T02.13 atomic-setup wrapper, T02.14 hook adapter). Issue #5 (non-string eval_id coverage) is now PARTIALLY addressed — the parametrize sweep covers 12 cases including `None`, `True`, `False`, `Path`, `bytes`, list, dict, tuple, float.

## Manual validation

> Build a `HomeIsolation`, call `setup()` without a config, confirm `TypeError` AND no scratch-root contents.

Equivalent test: `test_setup_requires_explicit_config` (`tests/cli/eval/test_path_containment.py:475-493`).

> Build a `HomeIsolation` with a permissive config, mkdtemp into a symlink that escapes, confirm `check='home_path_escape'`.

Equivalent test: `test_setup_catches_symlink_escape_under_explicit_config`.

> Confirm the AC12 allowlist source-of-truth is `EvalConfig`, not a hard-coded copy.

Equivalent test: `test_uses_evalconfig_allowed_scratch_roots_as_source_of_truth`.

## Files changed

* `src/superclaude/cli/eval/isolation.py` — `HomeContainmentViolation` + `containment_guard` (~155 LOC); `HomeIsolation.setup` now requires explicit `config`.
* `src/superclaude/cli/eval/__init__.py` — exports `HomeContainmentViolation`, `containment_guard`.
* `tests/cli/eval/test_path_containment.py` — new module, 47 tests.
* `tests/cli/eval/test_home_isolation_extend.py` — added `permissive_config` fixture + `_config_for` helper; 29 callsites updated to pass explicit config.
* `.dev/releases/current/cliEval/artifacts/D-0029/{spec,notes,evidence}.md` — D-0029 deliverable artifacts.

## Files NOT changed (confirms preservation)

* `src/superclaude/cli/sprint/executor.py` — `IsolationLayers` untouched (T02.05 probe still passes; see `test_isolation_layers_probe_still_passes_after_extension`).
* `src/superclaude/cli/eval/config.py` — `EvalConfig` / `resolve_scratch_root` untouched.
* `src/superclaude/cli/eval/loader.py` — `validate_eval_id` / `InvalidEvalId` untouched.
