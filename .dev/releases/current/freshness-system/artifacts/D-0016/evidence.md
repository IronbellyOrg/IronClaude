# D-0016 — Packaging: hooks ship in sdist + wheel

## Task: T04.04 (STANDARD)

Verified that `src/superclaude/hooks/scripts/*.sh`, `plugins/superclaude/hooks/scripts/*.sh`, and `src/superclaude/hooks/hooks.json` all land in the built sdist and wheel.

## MANIFEST.in

The existing MANIFEST.in already includes (line 10) `recursive-include src/superclaude *.py *.md *.ts *.json *.sh`, which covers `*.sh` files recursively. The hooks subdir was already covered. No MANIFEST.in changes were needed.

Verified by tarball inspection (see `sdist-listing.txt`).

## pyproject.toml (hatchling)

Wheel includes via `[tool.hatch.build.targets.wheel]`:
- `packages = ["src/superclaude"]` — canonical install location.
- `include = ["src/**", "plugins/**"]` — globs all extensions.
- `[tool.hatch.build.targets.wheel.force-include]` mirrors `src/` and `plugins/` under the wheel's `superclaude/_src/` and `superclaude/_plugins/` paths.

No pyproject.toml changes were needed.

## Verification — sdist

```
$ uv run python -m build --sdist
Successfully built superclaude-4.2.0.tar.gz

$ tar tzf dist/superclaude-4.2.0.tar.gz | grep -c '\.sh$'
18
```

All 8 hook scripts (7 freshness + 1 session-init) × 2 (src + plugins mirror) = 16, plus 2 other .sh files = 18.

See `sdist-listing.txt` for the full sdist entries under `hooks/` and `scripts/`.

## Verification — wheel

```
$ uv run python -m build --wheel
Successfully built superclaude-4.2.0-py3-none-any.whl

$ unzip -l dist/superclaude-4.2.0-py3-none-any.whl | grep -c '\.sh$'
26
```

Hook scripts appear in the wheel at:
- `superclaude/hooks/scripts/freshness-*.sh` (canonical — where `install_hooks._get_hooks_scripts_source()` looks).
- `superclaude/scripts/session-init.sh` (canonical — where `_get_legacy_scripts_source()` looks).
- `superclaude/_src/superclaude/hooks/scripts/*` and `superclaude/_plugins/...` (force-include mirrors).

`_get_hooks_source()` (returns `package_root / "hooks" / "hooks.json"`) and `_get_hooks_scripts_source()` (`package_root / "hooks" / "scripts"`) both resolve correctly against the wheel layout. See `wheel-listing.txt` for full inventory.

## Acceptance

- sdist contains all 7 freshness scripts + session-init.sh + hooks.json in both `src/` and `plugins/`.
- Wheel contains them at the canonical `superclaude/hooks/scripts/` path (and the force-include mirrors).
- `install_hooks.py`'s source-discovery resolves correctly in both checkout and installed-from-wheel contexts.

## Files saved

- `sdist-listing.txt` — `tar tzf` filter for hooks/scripts entries
- `wheel-listing.txt` — `unzip -l` filter for hooks/scripts entries
