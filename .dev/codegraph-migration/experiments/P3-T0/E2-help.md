# E2-help (Phase 3 Task 2, prerequisite experiment E-2)

Date: 2026-10-31, codegraph 1.6.2 (`/home/coder/.local/bin/codegraph`). Run from the worktree root `.dev/worktrees/codegraph-adoption` against its own index (read-only verbs only).

## Summary: flags the guide and the new skills may use

| Verb | `--json` | Flags captured | Notes for Phase 3 |
|---|---|---|---|
| `query <search>` | yes (`-j`) | `-p/--path`, `-l/--limit` (default 10), `-k/--kind` | JSON rows carry `node.filePath`, `startLine`, `endLine`, `signature`, `docstring` (the span source for the call-site procedure) |
| `node [name]` | **no** (`error: unknown option '--json'`) | `-p/--path`, `-f/--file` (file mode or disambiguation), `--offset`, `--limit`, `--symbols-only` | Markdown output only. File outline: `codegraph node --file <path> --symbols-only` (CLI equivalent of `codegraph_node {file, symbolsOnly:true}`); a file without `--symbols-only` returns source, which the guide forbids (standing rule 1) |
| `callers <symbol>` | yes (`-j`) | `-p/--path`, `-f/--file`, `-l/--limit` (default 20) | JSON `callers[]` give the caller's definition (`startLine`), and `edges[]` carry `line` (the call-site line, e.g. `"line": 178` for `install` → `install_core_files`) plus `metadata.confidence` and `resolvedBy` |
| `callees <symbol>` | yes (`-j`) | `-p/--path`, `-f/--file`, `-l/--limit` (default 20) | same shape as `callers` |
| `impact <symbol>` | yes (`-j`) | `-p/--path`, `-f/--file`, `-d/--depth` (default 2) | JSON `affected[]` includes the symbol itself as the first row |
| `status [path]` | yes (`-j`) | none besides `--json` | JSON has `initialized`, `version`, `projectPath`, `pendingChanges{added,modified,removed}`, `worktreeMismatch`, `index.state`; run only under the `pgrep` guard (standing rule 7) |
| `affected [files...]` | yes (`-j`) | `-p/--path`, `--stdin`, `-d/--depth` (default 5), `-f/--filter <glob>`, `-q/--quiet` | JSON: `changedFiles[]`, `affectedTests[]`, `totalDependentsTraversed` |
| `init [path]` | n/a | `-i/--index` ("Deprecated: indexing now runs by default; flag accepted for backward compatibility"), `-f/--force`, `-v/--verbose`, `-y/--yes` | `init --yes` inside a nested worktree builds a worktree-local index (`E1-freshness.md` step 1); the status warning still suggests `init -i`, which is the same command with the deprecated flag |
| `telemetry [action]` | n/a | actions `status`, `on`, `off` | only `telemetry status` is a read verb |

## `--help` output

### `codegraph callers --help`
```text
Usage: codegraph callers [options] <symbol>

Find all functions/methods that call a specific symbol

Options:
  -p, --path <path>     Project path
  -f, --file <path>     Narrow definitions by file path or suffix (no match:
                        show all with a note)
  -l, --limit <number>  Maximum results per definition (also caps the JSON
                        union) (default: "20")
  -j, --json            Output as JSON
  -h, --help            display help for command
(exit 0)
```

### `codegraph callees --help`
```text
Usage: codegraph callees [options] <symbol>

Find all functions/methods called by a specific symbol

Options:
  -p, --path <path>     Project path
  -f, --file <path>     Narrow definitions by file path or suffix (no match:
                        show all with a note)
  -l, --limit <number>  Maximum results per definition (also caps the JSON
                        union) (default: "20")
  -j, --json            Output as JSON
  -h, --help            display help for command
(exit 0)
```

### `codegraph node --help`
```text
Usage: codegraph node [options] [name]

One symbol's source + caller/callee trail, or read a file with line numbers +
dependents (same output as the codegraph_node MCP tool)

Options:
  -p, --path <path>  Project path
  -f, --file <file>  Treat as file mode (or disambiguate a symbol to this file)
  --offset <number>  File mode: 1-based start line
  --limit <number>   File mode: maximum lines
  --symbols-only     File mode: just the symbol map + dependents
  -h, --help         display help for command
(exit 0)
```

### `codegraph impact --help`
```text
Usage: codegraph impact [options] <symbol>

Analyze what code is affected by changing a symbol

Options:
  -p, --path <path>     Project path
  -f, --file <path>     Narrow definitions by file path or suffix (no match:
                        show all with a note)
  -d, --depth <number>  Traversal depth (default: "2")
  -j, --json            Output as JSON
  -h, --help            display help for command
(exit 0)
```

### `codegraph status --help`
```text
Usage: codegraph status [options] [path]

Show index status and statistics

Options:
  -j, --json  Output as JSON
  -h, --help  display help for command
(exit 0)
```

### `codegraph affected --help`
```text
Usage: codegraph affected [options] [files...]

Find test files affected by changed source files

Options:
  -p, --path <path>     Project path
  --stdin               Read file list from stdin (one per line)
  -d, --depth <number>  Max dependency traversal depth (default: "5")
  -f, --filter <glob>   Custom glob filter for test files (e.g. "e2e/*.spec.ts")
  -j, --json            Output as JSON
  -q, --quiet           Only output file paths, no decoration
  -h, --help            display help for command
(exit 0)
```

### `codegraph query --help`
```text
Usage: codegraph query [options] <search>

Search for symbols in the codebase

Options:
  -p, --path <path>     Project path
  -l, --limit <number>  Maximum results (default: "10")
  -k, --kind <kind>     Filter by node kind (function, class, etc.)
  -j, --json            Output as JSON
  -h, --help            display help for command
(exit 0)
```

### `codegraph init --help`
```text
Usage: codegraph init [options] [path]

Initialize CodeGraph in a project directory and build the initial index

Options:
  -i, --index    Deprecated: indexing now runs by default; flag accepted for
                 backward compatibility
  -f, --force    Initialize even if the path looks like your home directory or a
                 filesystem root
  -v, --verbose  Show detailed worker lifecycle and memory info
  -y, --yes      Non-interactive: skip every prompt and take the defaults (for
                 scripts / CI / container bootstraps)
  -h, --help     display help for command
(exit 0)
```

### `codegraph telemetry --help`
```text
Usage: codegraph telemetry [options] [action]

Show or change anonymous usage telemetry (status, on, off)

Options:
  -h, --help  display help for command
(exit 0)
```

## `--json` samples (each cut to 1,800 bytes)

### `codegraph query install_core_files --json --limit 3`
```text
[
  {
    "node": {
      "id": "function:af203c259f45b46a2b93274651df6818",
      "kind": "function",
      "name": "install_core_files",
      "qualifiedName": "install_core_files",
      "filePath": "src/superclaude/cli/install_core.py",
      "language": "python",
      "startLine": 27,
      "endLine": 100,
      "startColumn": 0,
      "endColumn": 39,
      "docstring": "Install SuperClaude core framework files to Claude Code config directory.\n\nCopies all .md files from src/superclaude/core/ to ~/.claude/,\nproviding the behavioral instructions that power the SuperClaude framework.\n\nArgs:\n    target_path: Target installation directory (default: ~/.claude)\n    force: Force overwrite if files already exist\n\nReturns:\n    Tuple of (success: bool, message: str)",
      "signature": "(\n    target_path: Path = None, force: bool = False\n) -> Tuple[bool, str]",
      "visibility": null,
      "isExported": false,
      "isAsync": false,
      "isStatic": false,
      "isAbstract": false,
      "updatedAt": 1793453848415
    },
    "score": 119.55471318434435
  },
  {
    "node": {
      "id": "function:f13916c21c5994f4db7e2e1d98388d00",
      "kind": "function",
      "name": "install_hooks",
      "qualifiedName": "install_hooks",
      "filePath": "src/superclaude/cli/install_hooks.py",
      "language": "python",
      "startLine": 120,
      "endLine": 210,
      "startColumn": 0,
      "endColumn": 39,
      "docstring": "Install hook scripts to ~/.claude/hooks/ and merge hook registrations into\n~/.claude/settings.json.\n\nArgs:\n    target_path: Path to settings.json (default: ~/.claude/settings.json).\n    force: If True, overwrite existing hook scripts and refresh\n        registrations owned by matching framework command paths.\n\nReturns:\n    (succe
(exit 0)
```

### `codegraph affected src/superclaude/cli/install_core.py --json --quiet`
```text
{
  "changedFiles": [
    "src/superclaude/cli/install_core.py"
  ],
  "affectedTests": [],
  "totalDependentsTraversed": 2
}

(exit 0)
```

### `codegraph node install_core_files --json`
```text
error: unknown option '--json'

(exit 1; the capture pipe reported 0, so every exit code in this section was re-checked by a separate run without a pipe: all others are 0)
```

### `codegraph node install_core_files`
```text
**install_core_files** (function)

**Location:** src/superclaude/cli/install_core.py:27
**Signature:** `(
    target_path: Path = None, force: bool = False
) -> Tuple[bool, str]`

```python
27	def install_core_files(
28	    target_path: Path = None, force: bool = False
29	) -> Tuple[bool, str]:
30	    """
31	    Install SuperClaude core framework files to Claude Code config directory.
32	
33	    Copies all .md files from src/superclaude/core/ to ~/.claude/,
34	    providing the behavioral instructions that power the SuperClaude framework.
35	
36	    Args:
37	        target_path: Target installation directory (default: ~/.claude)
38	        force: Force overwrite if files already exist
39	
40	    Returns:
41	        Tuple of (success: bool, message: str)
42	    """
43	    if target_path is None:
44	        target_path = Path.home() / ".claude"
45	
46	    core_source = _get_core_source()
47	
48	    if not core_source or not core_source.exists():
49	        return False, f"Core source directory not found: {core_source}"
50	
51	    target_path.mkdir(parents=True, exist_ok=True)
52	
53	    core_files = sorted(core_source.glob("*.md"))
54	
55	    if not core_files:
56	        return False, f"No core framework files found in {core_source}"
57	
58	    installed = []
59	    skipped = []
60	    failed = []
61	
62	    for src_file in core_files:
63	        dest_file = target_path / src_file.name
64	
65	        if dest_file.exists() and not force:
66	            skipped.append(src_file.name)
67	            continue
68	
69	        try:
70	            shutil.copy2(src_file, dest_file)
71	            installed.append(src_file.name)
72	        except Exception as e:
73	            failed.append(f"{src_file.name}: {e}")
74	
75	    messages = []
76	
77	    if installed:
78	        messag
(exit 0)
```

### `codegraph node --file src/superclaude/cli/install_core.py --symbols-only`
```text
**src/superclaude/cli/install_core.py** — 5 symbols, used by 1 file: src/superclaude/cli/main.py

**Symbols**
- `KNOWN_CORE_FILES` (variable) = frozenset( { "BASH_INSPECTION_POLICY.md", "BUSINESS_PANEL_EXAMPLES.md", ... — :13
- `install_core_files` (function) ( target_path: Path = None, force: bool = False ) -> Tuple[bool, str] — :27
- `_get_core_source` (function) () -> Path — :103
- `list_core_files` (function) () -> List[str] — :125
- `list_installed_core_files` (function) () -> List[str] — :140

> Drop `symbolsOnly` (or pass `offset`/`limit`) to read the source, like Read.

(exit 0)
```

### `codegraph callers install_core_files --json --limit 5`
```text
{
  "symbol": "install_core_files",
  "targets": [
    {
      "name": "install_core_files",
      "kind": "function",
      "filePath": "src/superclaude/cli/install_core.py",
      "startLine": 27,
      "id": "function:af203c259f45b46a2b93274651df6818",
      "qualifiedName": "install_core_files",
      "language": "python"
    }
  ],
  "ambiguous": false,
  "aggregation": "definition",
  "filteredOut": false,
  "definitions": [
    {
      "definition": {
        "name": "install_core_files",
        "kind": "function",
        "filePath": "src/superclaude/cli/install_core.py",
        "startLine": 27,
        "id": "function:af203c259f45b46a2b93274651df6818",
        "qualifiedName": "install_core_files",
        "language": "python"
      },
      "roots": [
        "function:af203c259f45b46a2b93274651df6818"
      ],
      "callers": [
        {
          "id": "function:878f3c67930466d1fcb4f1907bebf117",
          "name": "install",
          "kind": "function",
          "filePath": "src/superclaude/cli/main.py",
          "startLine": 46,
          "relationships": [
            "calls"
          ]
        },
        {
          "id": "function:e3c28873f0dde655529e5388445baf5b",
          "name": "update",
          "kind": "function",
          "filePath": "src/superclaude/cli/main.py",
          "startLine": 340,
          "relationships": [
            "calls"
          ]
        }
      ],
      "edges": [
        {
          "source": "function:878f3c67930466d1fcb4f1907bebf117",
          "target": "function:af203c259f45b46a2b93274651df6818",
          "kind": "calls",
          "metadata": {
            "confidence": 0.9,
            "resolvedBy": "import",
            "refName": "install_core_files"
          },
          "line": 178,
          "column":
(exit 0)
```

### `codegraph impact install_core_files --json --depth 1`
```text
{
  "symbol": "install_core_files",
  "depth": 1,
  "targets": [
    {
      "name": "install_core_files",
      "kind": "function",
      "filePath": "src/superclaude/cli/install_core.py",
      "startLine": 27,
      "id": "function:af203c259f45b46a2b93274651df6818",
      "qualifiedName": "install_core_files",
      "language": "python"
    }
  ],
  "ambiguous": false,
  "aggregation": "definition",
  "filteredOut": false,
  "definitions": [
    {
      "definition": {
        "name": "install_core_files",
        "kind": "function",
        "filePath": "src/superclaude/cli/install_core.py",
        "startLine": 27,
        "id": "function:af203c259f45b46a2b93274651df6818",
        "qualifiedName": "install_core_files",
        "language": "python"
      },
      "roots": [
        "function:af203c259f45b46a2b93274651df6818"
      ],
      "nodeCount": 3,
      "edgeCount": 2,
      "affected": [
        {
          "id": "function:af203c259f45b46a2b93274651df6818",
          "name": "install_core_files",
          "kind": "function",
          "filePath": "src/superclaude/cli/install_core.py",
          "startLine": 27
        },
        {
          "id": "function:878f3c67930466d1fcb4f1907bebf117",
          "name": "install",
          "kind": "function",
          "filePath": "src/superclaude/cli/main.py",
          "startLine": 46
        },
        {
          "id": "function:e3c28873f0dde655529e5388445baf5b",
          "name": "update",
          "kind": "function",
          "filePath": "src/superclaude/cli/main.py",
          "startLine": 340
        }
      ],
      "edges": [
        {
          "source": "function:878f3c67930466d1fcb4f1907bebf117",
          "target": "function:af203c259f45b46a2b93274651df6818",
          "kind": "calls",
          "metad
(exit 0)
```

