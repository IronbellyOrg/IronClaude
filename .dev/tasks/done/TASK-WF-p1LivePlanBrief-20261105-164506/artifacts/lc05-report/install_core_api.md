# `superclaude.cli.install_core` API

Source: `src/superclaude/cli/install_core.py`. Copies the framework's `.md` instruction files into `~/.claude/`.

## Constants

### `KNOWN_CORE_FILES: frozenset[str]`

The 12 core file names this version ships (`CLAUDE.md`, `RULES.md`, `PRINCIPLES.md`, `HOW-WE-WORK.md`, `WORKER-CONTRACT.md`, `CODEGRAPH.md`, `BASH_INSPECTION_POLICY.md`, `ISSUE-BACKLOG.md`, `ISSUE-HANDOFF.md`, `RESEARCH_CONFIG.md`, `BUSINESS_PANEL_EXAMPLES.md`, `BUSINESS_SYMBOLS.md`). Only `list_installed_core_files` uses it, to filter the listing.

## Functions

### `install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`

Copies every `*.md` file from the package `core/` directory into `target_path`.

| Parameter | Default | Meaning |
|---|---|---|
| `target_path` | `~/.claude` | Destination directory. Created (with parents) if missing. |
| `force` | `False` | Overwrite files that already exist. Without it, existing files are skipped. |

Returns `(success, message)`. `success` is `True` only when no copy failed. `message` is a multi-line report of installed, skipped and failed files, ending with the installation directory.

Returns `(False, message)` when the source directory is missing, when it holds no `.md` files, or when nothing was installed, skipped or failed.

Copies use `shutil.copy2` (metadata kept). A failed copy is recorded and the loop continues; it does not raise.

```python
from superclaude.cli.install_core import install_core_files

ok, msg = install_core_files(force=True)
print(msg)
```

### `list_core_files() -> List[str]`

Sorted names of the `*.md` files in the package `core/` directory. Returns `[]` if that directory does not exist. Not filtered by `KNOWN_CORE_FILES`.

### `list_installed_core_files() -> List[str]`

Sorted names of `*.md` files in `~/.claude/` that are also in `KNOWN_CORE_FILES`. Returns `[]` if `~/.claude` does not exist. Always reads `~/.claude`; it takes no path argument, so it ignores a custom `target_path` used at install time.

### `_get_core_source() -> Path` (private)

Returns `<package root>/core`, where package root is the parent of the `cli/` directory holding this file. The path is returned even if it does not exist; callers check `.exists()`. The docstring mentions a `src/superclaude/core/` fallback, but the code has only the one location (in a source checkout both are the same directory).

## Callers

`src/superclaude/cli/main.py` calls `list_core_files`, `list_installed_core_files` (status listing) and `install_core_files` (install with `force`, and update with `force=True`). `install_hooks.py` only mentions `install_core_files` in a docstring.
