# D-0034 — COMP-014 install_hooks adapter (Task T02.14)

**Task**: T02.14 (Phase 2 — cliEval harness)
**Tier**: STANDARD
**Risk**: Low
**Roadmap**: R-034 / COMP-014 (install_hooks reuse adapter)
**Cross-links**: D-0032 (COMP-006 integrated HomeIsolation, T02.11),
D-0033 (NFR-ISO2 atomic-setup wrapper, T02.13),
`src/superclaude/cli/install_hooks.py` (production hook installer).

## Goal

Reuse the existing `superclaude.cli.install_hooks.install_hooks`
installer to deploy SuperClaude hooks into a per-eval `HOME` without
re-implementing the script-copy + settings.json merge pipeline. Pin a
single integration site at
`src/superclaude/cli/eval/hook_adapter.py` so the cliEval harness and
the production user-install path stay byte-for-byte aligned.

## Adapter contract

### Signature

```python
def deploy_hooks_to(home_path: Path) -> None: ...
```

`home_path` is the per-eval HOME directory `HomeIsolation.setup`
materialized (i.e., `<scratch_root>/<eval_id>-XXXXXX/`). The adapter
returns `None` on success and raises `HookDeployFailed` on any failure.

### Side effects (in order)

1. **Defense-in-depth refusal.** Resolve both `home_path` and
   `home_path / .claude` with `strict=False` and reject if either
   intersects the real `~/.claude/` directory (equality OR descendant).
   This catches: (a) `home_path` symlinked to real HOME, (b) callers
   passing their `$HOME` as `home_path` (which would direct the
   `<home>/.claude/settings.json` write straight into real `~/.claude/`).
2. **`install_hooks` delegation.** Invoke
   `install_hooks(target_path=home_path / ".claude" / "settings.json",
   force=False)`. The installer copies hook scripts to
   `<home>/.claude/hooks/` and merges hook registrations into
   `<home>/.claude/settings.json`.
3. **Verbatim `hooks.json` copy.** Copy
   `src/superclaude/hooks/hooks.json` byte-for-byte to
   `<home>/.claude/hooks.json` via the dedicated
   `_copy_hooks_json_verbatim` helper (a thin wrapper over
   `shutil.copy2` whose only purpose is to be a clean monkeypatch seam
   for tests).

### Idempotency

Re-invocation on the same `home_path` produces identical filesystem
state. `install_hooks` is itself idempotent (existing scripts are
skipped without `--force`; the settings.json merge skips matcher
collisions). The verbatim copy uses `shutil.copy2` which overwrites
with identical bytes when the source is unchanged.

### Error contract — `HookDeployFailed.error_tag`

The exception carries a structured `error_tag` so `EvalRunner`
(T03.x) can route the failure into `EvalRunner.outcome.artifacts`
without parsing human-readable strings.

| `error_tag`                  | Triggered when                                                                 |
|------------------------------|--------------------------------------------------------------------------------|
| `refused-real-home`          | `home_path` or `home_path/.claude` resolves to (or under) real `~/.claude/`.   |
| `source-hooks-json-missing`  | `src/superclaude/hooks/hooks.json` is absent on disk (broken checkout).        |
| `install-hooks-failed`       | `install_hooks` returned `success=False`. Installer message in `detail`.       |
| `hooks-json-copy-failed`     | `_copy_hooks_json_verbatim` raised `OSError`. OS error in `detail`.            |

All four tags are lowercase kebab-case with alphanumeric tokens — the
test `test_error_tags_are_kebab_case_strings` pins this shape so the
orchestrator routing table cannot drift.

## Acceptance criteria mapping (T02.14)

| AC bullet                                                                                                          | Evidence                                                                                                        |
|---|---|
| `deploy_hooks_to(home_path)` exists in `src/superclaude/cli/eval/hook_adapter.py` and calls `install_hooks`         | `test_deploy_hooks_to_writes_settings_json_under_home_path`, `test_settings_json_merge_uses_per_eval_target_path` |
| Adapter raises `HookDeployFailed` with `error_tag` on `install_hooks` failure                                       | `test_install_hooks_failure_propagates_as_hook_deploy_failed`, `test_error_tags_are_kebab_case_strings`           |
| Re-invocation produces identical FS state (idempotency)                                                            | `test_re_invocation_is_idempotent`                                                                              |
| `<home>/.claude/hooks.json` is byte-identical to `src/superclaude/hooks/hooks.json` (SHA256 assertion)              | `test_hooks_json_is_byte_identical_to_source`                                                                   |
| Adapter never writes to real `~/.claude/` (mtime fixture)                                                          | `test_real_user_claude_dir_is_untouched`, `test_refuses_when_home_path_is_real_user_claude_dir`, `test_refuses_when_home_path_is_descendant_of_real_user_claude_dir` |
| Adapter contract documented (this spec)                                                                            | This file                                                                                                       |

## Verbatim hooks.json copy — why a separate step?

`install_hooks` was designed for the production user-install path:
its job is to copy hook scripts and additively merge hook
registrations into the user's `settings.json`. It never copies the
source `hooks.json` to the destination because the source-of-truth
registrations are already represented inside the merged
`settings.json`.

The cliEval harness needs a second guarantee: the per-eval HOME
must carry a byte-identical copy of `hooks.json` so:

* Post-mortem inspection can SHA256-compare the source against what
  the per-eval HOME shipped without re-deriving registrations from
  the merged `settings.json`.
* The FR-G* capability-gate tests can diff the deployed file against
  the canonical source to detect any unexpected divergence in the
  per-eval surface.

Routing this copy through the dedicated `_copy_hooks_json_verbatim`
helper isolates the seam from `install_hooks`'s own `shutil.copy2`
usage (it copies hook scripts via the same API). Tests that simulate
an `OSError` on the verbatim copy patch this helper rather than the
shared `shutil.copy2` global so they don't accidentally also break
the installer's script-copy pipeline.

## Defense-in-depth — refusing real `~/.claude/`

The refusal must catch two distinct attack surfaces:

1. **Direct.** `home_path` itself resolves to (or under) real
   `~/.claude/`. Catches symlink shenanigans.
2. **Subdirectory leak.** `home_path / .claude` resolves to (or
   under) real `~/.claude/`. Catches the case where the caller
   passes their `$HOME` as `home_path` — every adapter write under
   `<home_path>/.claude/` would land on the real configuration
   directory.

Both sides are resolved with `strict=False` (the real directory may
exist, may not; the per-eval HOME may not have a `.claude/`
subdirectory yet) and compared with `==` OR `is_relative_to`. Tests
patch `Path.home` so the assertion never has to touch the operator's
actual `$HOME`.

## Files

* `src/superclaude/cli/eval/hook_adapter.py` — adapter module.
* `src/superclaude/cli/eval/__init__.py` — re-exports
  `HookDeployFailed`, `deploy_hooks_to`.
* `tests/cli/eval/test_hook_adapter.py` — 12 tests pinning the
  acceptance criteria above.

## Verification

* `uv run pytest tests/cli/eval/test_hook_adapter.py -v` → 12 passed.
* `uv run pytest tests/cli/test_install_hooks.py -v` → 8 failures
  pre-existing on the branch (the `reject-workspace-writes.sh`
  fixture is absent in the fake source-tree builder used by those
  tests; the adapter does NOT regress them — same 8 fail on a clean
  checkout). Tracked as a separate cleanup; out of scope for T02.14.
