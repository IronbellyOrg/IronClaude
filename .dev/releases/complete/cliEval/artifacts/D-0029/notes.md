# D-0029 — Implementation Notes (T02.08)

## Design decisions

### 1. Why three layered checks, not one consolidated check

Each check defends a distinct attack vector with a distinct underlying primitive:

- **Check 1 (eval_id regex)** defends loader-bypass. The loader (T01.07) validates eval_ids pre- and post-expand, but a programmatic caller can construct `HomeIsolation` directly. The re-validation closes that.
- **Check 2 (scratch-root allowlist)** defends AC12 policy. The allowlist is a per-run policy concept; `resolve_scratch_root` is the single source of truth and the guard funnels through it.
- **Check 3 (post-mkdtemp symlink resolution)** defends an attack where the textual prefix passes but a symlink component routes the path outside `scratch_root` at runtime. Only `Path.resolve(strict=True)` catches this — `is_relative_to` on un-resolved paths does not.

Consolidating the checks (e.g., a single regex-validated `resolve_scratch_root` for both `home_path` and `scratch_root`) would lose the distinct `check` identifier on the exception, making forensic bucketing harder.

### 2. Why `config` is required (and not synthesized)

The initial draft accepted `config: EvalConfig | None = None` in both `containment_guard` and `HomeIsolation.setup`. When `None`, `setup` synthesized `EvalConfig(allowed_scratch_roots=(self.home_root, *EvalConfig().allowed_scratch_roots))` — the rationale was "the upstream caller validated `home_root` via `resolve_scratch_root` at the CLI boundary, so trust it here."

The quality-engineer review correctly flagged this as a bypass: `HomeIsolation.__post_init__` re-validates `eval_id` but does NOT validate `home_root`. A caller constructing `HomeIsolation(eval_id="E1", home_root=Path("/home/user/.claude"), session_id="x")` would pass check 2 trivially because `home_root` is in the synthesized allowlist.

Two options were considered:

| Option | Adopted | Reason |
|---|---|---|
| Validate `home_root` against the default `EvalConfig.allowed_scratch_roots` in `__post_init__` | No | Would block tests using `tmp_path`-derived scratch roots; would require either monkey-patching the default or adding a 5th field to DM-006 (schema change). |
| Remove the fallback; make `config` required | **Yes** | Aligns with production wiring (orchestrator T03.16 always passes an explicit config); tests now build an `EvalConfig` whose allowlist matches their scratch root, mirroring production. |

The adopted option makes `config=None` impossible: a missing argument is now a `TypeError` at argument-binding time, before any filesystem operation in `setup` runs. This is the strongest form of "refusal before side effects."

### 3. Ordering: mkdtemp first, guard second

The guard MUST observe the freshly created HOME because check 3 uses `Path.resolve(strict=True)` which raises `FileNotFoundError` for nonexistent paths. The ordering is pinned by:

- `test_setup_runs_containment_guard_after_mkdtemp` — spies on `containment_guard` and asserts `home_path.exists()` is `True` at call time.
- `TestSymlinkResolvedContainment.test_raises_when_home_path_not_created` — confirms the failure mode when the guard runs ahead of mkdtemp.

This ordering also means a check 2 failure (allowlist) happens AFTER mkdtemp ran but BEFORE check 3, leaving the partial HOME on disk. `test_setup_failure_preserves_partial_home` pins this so the NFR-ISO2 atomic-setup wrapper (T02.13) can find and tag the directory.

### 4. Allowlist source-of-truth

`config.allowed_scratch_roots` is the sole source of truth. No other module embeds a hard-coded copy. The guard verifies this via `test_uses_evalconfig_allowed_scratch_roots_as_source_of_truth`, which narrows the allowlist to a single non-canonical entry and proves the guard follows.

### 5. Exception chaining

`raise ... from exc` is used at every check so `HomeContainmentViolation.__cause__` carries:

- `InvalidEvalId` (with its own `eval_id` field, for forensic recovery of the offending string)
- `ScratchRootViolation` (with `path`, `resolved`, `allowed` fields)
- `FileNotFoundError` (raised by `Path.resolve(strict=True)`)

Reporters that walk the chain can render the underlying detail without parsing `HomeContainmentViolation.detail`.

## Test scaffolding

### `_materialize_home` helper

`tests/cli/eval/test_path_containment.py:75` — creates a HOME the same way `HomeIsolation.setup` would, so the `Path.resolve(strict=True)` in check 3 succeeds. Uses plain `mkdir` rather than `tempfile.mkdtemp(prefix=...)`; the QA review noted this is slightly less production-realistic, but the integration tests (`TestIntegrationWithHomeIsolationSetup`) exercise the real `mkdtemp` path through `HomeIsolation.setup`, so the helper's simplification is acceptable for direct `containment_guard` calls.

### `permissive_config` fixture (T02.07)

`tests/cli/eval/test_home_isolation_extend.py:62` — `EvalConfig(allowed_scratch_roots=(scratch_root,))`. The 29 `iso.setup(config=permissive_config)` callsites in T02.07 now mirror production wiring: the orchestrator (T03.16) builds an `EvalConfig` whose allowlist contains the resolved scratch root for the run.

### Non-string eval_id parametrize sweep

`test_non_string_eval_id_is_rejected` covers `42, 0, -1, True, False, None, Path("E1"), b"E1", ["E1"], {"id": "E1"}, ("E1",), 3.14`. Note `True` and `False` are explicitly tested because `isinstance(True, int)` is `True` and Python would coerce booleans to ints in some contexts; `validate_eval_id` rejects them upfront via `isinstance(value, str)`.

### Symlink-chain test (A→B→outside)

`test_raises_on_symlink_chain_escape` builds a chain `home_chain → intermediate → outside` and asserts `Path.resolve(strict=True)` chases the full chain in one call, surfacing `check='home_path_escape'`. Pins resolution semantics at the public API.

## Files touched

| Path | Change |
|---|---|
| `src/superclaude/cli/eval/isolation.py` | +236 lines: `HomeContainmentViolation`, `containment_guard`, guard integration in `setup`. `config` parameter required on both. |
| `src/superclaude/cli/eval/__init__.py` | +2 exports. |
| `tests/cli/eval/test_path_containment.py` | New file, 45 tests. |
| `tests/cli/eval/test_home_isolation_extend.py` | +2 fixtures (`permissive_config`, `_config_for`); 29 `iso.setup()` callsites updated to pass explicit config. |
