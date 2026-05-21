# CLI Module Review — `src/superclaude/cli/`

- **Target**: `/config/workspace/IronClaude/src/superclaude/cli/`
- **Scope**: Whole-directory review (no diff). Architecture, anti-patterns, quality.
- **Date**: 2026-05-20
- **Reviewer**: baseline (no skill / no protocol)
- **Files reviewed**: 156 source files (Python + a few in-tree non-source artifacts noted below)
- **Approx LOC (Python)**: ~69,591 (from `wc -l`)

## Module inventory

Top-level layout (10 subpackages + flat installer helpers + `main.py`):

```
cli/
├── main.py                     # Click root + lazy subcommand mounts
├── __init__.py                 # re-exports main
├── doctor.py                   # legacy doctor (note: distinct from cli/eval/doctor)
├── vocabulary.py               # shared obligation regex vocabulary
├── install_agents.py           # ~/.claude/agents/ installer
├── install_commands.py         # ~/.claude/commands/sc/ installer
├── install_core.py             # ~/.claude/*.md installer
├── install_hooks.py            # hooks + settings.json merge (atomic + backup)
├── install_mcp.py              # MCP server registration (Docker / npx)
├── install_skill.py            # single-skill installer
├── install_skills.py           # batch-skill installer
├── install_templates.py        # templates installer
├── audit/                      # cleanup_audit scanner backends (43 files)
├── cleanup_audit/              # `superclaude cleanup-audit` group
├── cli_portify/                # `superclaude cli-portify` group + steps/
├── eval/                       # cliEval real-eval harness (`superclaude eval`)
├── pipeline/                   # generic StepRunner + ClaudeProcess + gates
├── prd/                        # `superclaude prd` group
├── roadmap/                    # `superclaude roadmap` group (largest)
├── sprint/                     # `superclaude sprint` group
├── task_builder/               # EMPTY (only __pycache__)
└── tasklist/                   # `superclaude tasklist` group
```

Six of the seven user-facing command groups (`sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, `eval`) follow a near-identical
internal shape: `commands.py`, `config.py`, `executor.py`, `gates.py`, `logging_.py`, `models.py`, `monitor.py`, `process.py`, `prompts.py`, `tui.py`.

---

## Findings

### CRITICAL

#### C1. `shell=True` with user-controllable command list in MCP installer
- **File**: `src/superclaude/cli/install_mcp.py:140-142`
- **Citation**:
  ```python
  user_shell = os.environ.get("SHELL", "/bin/bash")
  return subprocess.run(
      cmd_str, shell=True, env=os.environ, executable=user_shell, **kwargs
  )
  ```
- **Rationale**: `_run_command` is the centralized wrapper used by *every* MCP-install code path on non-Windows
  platforms. The cmd list is `shlex.quote`-joined into `cmd_str` and then re-interpreted through the user's `$SHELL`.
  Although `shlex.quote` is defensible per-arg, this combo (a) loses the safety of argv-form invocation, (b) passes
  `os.environ` directly so anything the parent imported is inherited into commands run as part of an installer (think
  `LD_PRELOAD`, `PYTHONPATH`), and (c) is justified only by "support aliases" — a feature the installer should not need.
  This is the single highest-impact attack surface in the module; once one input is concatenated wrong upstream the
  whole installer is compromised.
- **Recommendation**: Drop `shell=True`. Either invoke with `cmd` as a list directly (drops alias support, acceptable
  for installers), or, if shell features are genuinely required, gate it behind an opt-in flag and refuse to inject
  anything user-derived.

---

### HIGH

#### H1. `cli/eval/commands.py` is 1 636 LOC with 38 functions — Click commands collide with business logic
- **File**: `src/superclaude/cli/eval/commands.py` (whole file)
- **Rationale**: A click `commands.py` should declare `@click.group/@click.command` decorators and route into a
  domain layer. Here, the file mixes version probes (`_check_claude_version`), RAM gating constants (`RAM_CEILING_*`),
  hook-adapter wiring, full reporter glue, secret generation (`secrets`), subprocess invocation of `claude`,
  scratch-root resolution, and *four* click commands. The mid-file constants are real configuration (e.g.
  `RAM_CEILING_GB`, `PARALLEL_RAM_GATE_THRESHOLD`) that belong in `eval/config.py` — they're load-bearing for
  multiple tests per the docstrings.
- **Recommendation**: Extract the helpers to siblings (`doctor.py`, `gates_runtime.py`, `version_probe.py`) and keep
  `commands.py` to wiring only.

#### H2. `roadmap/executor.py` at 3 641 LOC — single-file god-module
- **File**: `src/superclaude/cli/roadmap/executor.py` (whole file)
- **Rationale**: 54 top-level defs/classes in one file (`grep -c "^def\|^class"`); imports 14 gates and 9 prompt
  builders from siblings just to construct steps. The "step-list builder" + "step runner" + "deviation handler" +
  "spec-patch dispatcher" + various "freshness checks" each have natural module boundaries (e.g.
  `_check_annotate_deviations_freshness` near line 2352 is itself a non-trivial helper). At this size, change-amplification
  is severe — any roadmap change touches a 3.6k-line file.
- **Recommendation**: Split into `executor.py` (the public `roadmap_run_step` and step-list builder),
  `freshness.py` (annotate-deviation checks), `dispatch.py` (deviation/remediate routing), and `dual_budget.py`
  (the dual-budget recovery TODO at L2342). Same advice for `sprint/executor.py` (2 148 LOC).

#### H3. Eight near-identical `_get_*_source()` resolvers — copy-pasted package-vs-checkout layout logic
- **Files**:
  - `install_agents.py:89` `_get_agents_source`
  - `install_commands.py:92` `_get_commands_source`
  - `install_core.py:89`   `_get_core_source`
  - `install_templates.py:106` `_get_templates_source`
  - `install_skill.py:58` `_get_skill_source`
  - `install_hooks.py:462/469/475/515` (four variants)
- **Rationale**: Each computes `Path(__file__).resolve().parent.parent` and probes one or two candidate paths
  (`<package_root>/<subdir>` and `<repo>/<plugins>/superclaude/<subdir>` / `<package_root>/_src/...`). The duplication
  has already produced inconsistent fallbacks (`install_commands.py:118` looks in `plugins/superclaude/commands`
  while `install_templates.py:122` looks in `_src/superclaude/templates`; `install_core.py:108` has *no* checkout
  fallback at all, while `install_agents.py:107` "returns package location even when missing so error msg is clear").
- **Recommendation**: One helper in a shared `cli/_paths.py`:
  `def package_subdir(name: str, fallback: tuple[Path, ...] = ()) -> Path`. Every installer collapses to a one-liner
  and the layout-discovery rules become single-source.

#### H4. `doctor.py` uses an undocumented pytest internal that has shifted historically
- **File**: `src/superclaude/cli/doctor.py:57`
  ```python
  config = pytest.Config.fromdictargs({}, [])
  ```
- **Rationale**: `pytest.Config.fromdictargs` is not part of pytest's public API
  (https://docs.pytest.org/en/stable/reference/reference.html). It survives today because of the broad
  `except Exception as e` swallowing four lines later. Any pytest upgrade that removes/renames it will silently
  mark the plugin check as *failed* without diagnostic, which is exactly the bug `doctor` is supposed to *catch*.
- **Recommendation**: Switch to `importlib.metadata.entry_points(group="pytest11")` lookup for the
  `superclaude` entry. That probes the same registration the user installed without spawning a pytest config.

#### H5. `--dangerously-skip-permissions` is the default permission flag in all subprocess entry points
- **Files**:
  - `pipeline/process.py:45` (base class default)
  - `pipeline/models.py:187` (`PipelineConfig.permission_flag`)
  - `sprint/config.py:282`, `sprint/models.py:365`, `sprint/commands.py:112/116`
  - `eval/claude_process.py:182`
  - `sprint/summarizer.py:329`
- **Rationale**: This is a defensible operational choice for a *sandboxed evaluation harness*, but it is
  the *default* on every path including the sprint runner (which the docs describe as a long-running supervised
  pipeline). There is no callsite where the user is asked to confirm. CLI-portify, prd, cleanup-audit, eval, sprint,
  roadmap all spawn `claude` without permission prompts by default.
- **Recommendation**: Make `--dangerously-skip-permissions` opt-in via a single env var
  (`SUPERCLAUDE_ALLOW_DANGEROUS=1`) checked once in `pipeline/process.ClaudeProcess.__init__`, default to
  `--permission-mode plan` (or whatever the next-safer Claude CLI permission flag is). This is a
  cross-cutting concern; today it is set in seven independent locations and any future tightening would have
  to touch all of them.

#### H6. `eval/commands.py:798` and `:1492` repeat `Path.home() / ".claude" / "settings.json"` as a literal
- **Files**:
  - `cli/eval/commands.py:798`
  - `cli/eval/commands.py:1492`
  - `cli/install_hooks.py:104`
  - `cli/eval/hook_adapter.py:127`
- **Rationale**: The eval harness is supposed to be hermetic but two of its code paths reach into the user's
  real `~/.claude/settings.json` rather than the home-isolation override negotiated by `HomeIsolation` (imported
  in the same file at line 68). This is a likely test-pollution bug — a parallel eval run that runs the merge code
  path will mutate the host's settings.json.
- **Recommendation**: Route all settings.json lookups through `HomeIsolation.settings_path()` (add it if missing).
  The `Path.home()` literal should be banned by lint in `cli/eval/`.

---

### MEDIUM

#### M1. `main.py:13` mutates `sys.path` at module import
- **File**: `src/superclaude/cli/main.py:13`
  ```python
  sys.path.insert(0, str(Path(__file__).parent.parent.parent))
  ```
- **Rationale**: The package is installed via `pyproject.toml` entry points — the `superclaude` console
  script is created by hatchling and `from superclaude import __version__` at line 15 already resolves through
  installed metadata. The `sys.path.insert` is a leftover that silently shadows installs (e.g. dev checkout
  next to an installed copy). It also makes static analysis lie about importability.
- **Recommendation**: Delete the line. If `superclaude` is not importable, that's a setup bug worth surfacing.

#### M2. Mixed eager and lazy imports of subcommand groups
- **File**: `src/superclaude/cli/main.py:400-426`
- **Rationale**: The seven `add_command` calls at module top-level are *eager* imports of every subcommand group
  (sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval). Each of those is itself a heavy module — the
  eval group alone pulls 26 sibling modules. Meanwhile, the `install`/`mcp`/`update`/`install-skill`/`doctor`
  commands lazy-import inside their handler bodies (lines 59-82, 239, 277-280, 335, 367). The mix is unprincipled
  — either commit to lazy loading everywhere (significantly faster `superclaude --help`) or eager everywhere.
  Right now the inconsistency means `superclaude install --help` still imports the entire pipeline/roadmap stack.
- **Recommendation**: Pick one. Lazy-loading via `click.LazyGroup` or a `commands.py` discovery list would shave
  the cold-start cost meaningfully and standardize the pattern.

#### M3. `subprocess.run(..., env=os.environ, ...)` instead of `os.environ.copy()`
- **File**: `src/superclaude/cli/install_mcp.py:141`
- **Rationale**: Passing the live `os.environ` mapping (not a copy) into `subprocess.run` is technically safe
  because Popen reads it once, but it's a Python anti-pattern that has bitten this codebase elsewhere — the
  `pipeline/process.py:107` correctly does `env = os.environ.copy()` and pops sensitive keys. The MCP installer
  should match.

#### M4. Bare/broad `except Exception:` with no logging at 30+ sites
- **Files**: 31 hits in `grep "except Exception"`. Notable noisy ones with no logging:
  - `cleanup_audit/process.py` — actually delegated, OK.
  - `install_core.py:58`, `install_agents.py:58`, `install_commands.py:59`, `install_skill.py:54`,
    `install_mcp.py:230/294/373/410/639`
  - `doctor.py:77`
  - `sprint/notify.py:30`, `sprint/tmux.py:157`
- **Rationale**: Several of the installer-side `except Exception as e:` handlers fold the exception into a
  formatted string in a returned tuple but never log it. Operators running `superclaude install` will see
  `❌ Failed to install <name>: <one-line repr>` without a stack trace, and there is no `--verbose` switch to
  recover it. For a tool whose users routinely report "install failed for X", losing the traceback is a real
  support cost.
- **Recommendation**: Add a module-level logger and `logger.exception(...)` in every catch site; the install
  entry points already accept implicit verbose-via-stderr handling.

#### M5. `install_skills.py:65` imports `shutil` inside a `for` loop
- **File**: `src/superclaude/cli/install_skills.py:64-67`
  ```python
  if stale.exists():
      import shutil
      shutil.rmtree(stale)
  ```
- **Rationale**: Local-scoped imports are sometimes a deliberate optimisation, but `shutil` is already a stdlib
  module loaded by every other file in the module. The local import gains nothing and confuses readers into
  thinking there's a circular-import workaround at play.
- **Recommendation**: Move to top-of-file imports.

#### M6. The `audit/` subpackage (43 files) is reachable but does not belong under `cli/`
- **Files**: `src/superclaude/cli/audit/*.py` (43 files)
- **Rationale**: These modules (`reachability.py`, `dead_code.py`, `wiring_gate.py`, `credential_scanner.py`,
  `dependency_graph.py`, …) are static-analysis libraries, not CLI commands. They are imported by `cleanup_audit/`
  and `roadmap/executor.py` (`from ..audit.wiring_gate import WIRING_GATE`). Sitting them under `cli/` makes
  reuse from non-CLI callers awkward and inflates the CLI namespace. They are also the largest single
  contribution to the `cli/` LOC count outside `roadmap/`.
- **Recommendation**: Move to `src/superclaude/analysis/` or `src/superclaude/audit/`. The current placement is
  a category error and obscures the actual CLI surface.

#### M7. Default `Path()` mutable-ish argument idiom
- **Files**: `install_core.py:14`, `install_commands.py:12`, `install_skills.py:33`, `install_agents.py:15`,
  `install_templates.py:31`, `install_hooks.py:89`
- **Rationale**: Every installer uses `target_path: Path = None` then reassigns inside. This is the standard
  Python idiom for "no default Path()" — but the signature should be `target_path: Path | None = None` (which
  several but not all files do). The inconsistency triggers type-checker noise.
- **Recommendation**: Standardize to PEP 604 `Path | None = None` everywhere.

---

### LOW

#### L1. `cleanup_audit/portify-summary.md` is a tracked .md inside a source package
- **File**: `src/superclaude/cli/cleanup_audit/portify-summary.md`
- **Rationale**: Free-floating documentation inside a Python module. Either it's load-bearing (then it belongs in
  `docs/`) or it isn't (then delete). Will end up in the wheel as a stray artifact.

#### L2. `task_builder/` is an empty directory (only `__pycache__/`)
- **File**: `src/superclaude/cli/task_builder/`
- **Rationale**: Empty package; either prune or commit the intended `__init__.py`.

#### L3. `pipeline/process.py:120-123` opens files with no encoding=
- **File**: `src/superclaude/cli/pipeline/process.py:120-123`
  ```python
  self._stdout_fh = open(self.output_file.with_suffix(".log"), "w")
  ...
  self._stdout_fh = open(self.output_file, "w")
  self._stderr_fh = open(self.error_file, "w")
  ```
- **Rationale**: These files capture `claude` subprocess output that may contain non-UTF-8 sequences (e.g.
  terminal escape blobs). `install_mcp._run_command` sets `encoding="utf-8", errors="replace"` for the same
  reason — `pipeline/process.py` should too. On a platform where the default locale is ASCII (CI containers,
  some Docker bases), this will raise `UnicodeEncodeError` mid-stream and the gate will lose context.
- **Recommendation**: `open(..., "w", encoding="utf-8", errors="replace")`.

#### L4. `install_hooks._atomic_write_json` swallows `unlink` failures silently
- **File**: `src/superclaude/cli/install_hooks.py:444-448`
- **Rationale**: If `os.replace` fails, the temp file is left if its `unlink` then also fails (network FS, etc.).
  Silent `OSError` swallow is correct for the cleanup path, but a debug log would aid forensics. Same pattern
  exists in `pipeline/process.py:243`.

#### L5. Emoji-heavy installer messages assume a UTF-8 capable terminal
- **Files**: 54+ `click.echo` callsites in installer files
- **Rationale**: `click.echo` on Windows cp1252 may mangle these. `superclaude install` is a first-impression
  command. Either gate emoji on `sys.stdout.encoding` or set `errors="replace"` explicitly.

#### L6. `install_core.py:139` known-core-files list is hard-coded
- **File**: `src/superclaude/cli/install_core.py:139-152`
- **Rationale**: `list_installed_core_files` filters by a frozen 11-name set. Any new core file added to
  `src/superclaude/core/` won't appear as installed in `superclaude install --list` until this set is updated.
  This has historically gone out of sync with `_get_core_source()`.
- **Recommendation**: Compute the canonical set from the source directory at runtime.

---

### NITS

#### N1. `from .module import (long list)` style varies between installer files vs. group modules
- **Files**: `main.py:59-82` uses parenthesised multi-import; `main.py:400-426` uses one-per-line top-level imports.
  Either is fine; mix is jarring.

#### N2. `main.py` interleaves command decorators with non-decorated `from … import` blocks at module top level
- **File**: `main.py:400-426` — seven `from … import` + `main.add_command` pairs *after* the last `@main.command`.
  Conventional layout is all imports at top, all commands together. Today, adding an eighth group means scrolling
  past 400 lines of unrelated definitions.

#### N3. `doctor.py` is shadowed by `cli/eval/` "doctor" subcommand
- **Files**: `cli/doctor.py` (legacy install health check) vs. `cli/eval/commands.py:_check_claude_version` etc.
  Both ship under the brand "doctor" and both run at install time. Confusing; consider renaming one.

#### N4. Several `Tuple[bool, str]` returns where a small dataclass would clarify intent
- **Files**: `install_core.py:14`, `install_agents.py:15`, `install_commands.py:12`, etc.
- **Rationale**: Same `(success, message)` tuple is unpacked at every call site in `main.py:158-202`. A
  `@dataclass class InstallResult(success: bool, message: str)` makes the contract self-documenting and lets you
  attach `errors: list[str]` without rewriting six callers.

---

## Cross-cutting / architectural summary

1. **Architecture is sound at the macro level** — `pipeline/` provides a generic `StepRunner` + `ClaudeProcess`
   that six command groups reuse via `from superclaude.cli.pipeline.process import ClaudeProcess`. The contract
   is documented and the NFR-007 "no cross-imports between sprint and roadmap" comment is observed.
2. **The micro level is where decay shows**. Three structural rot signatures:
   - **God-modules**: `roadmap/executor.py` (3.6k LOC), `sprint/executor.py` (2.1k LOC), `eval/commands.py` (1.6k LOC).
   - **Copy-paste in installers**: `_get_X_source()` exists in 8 places with subtle variation (H3).
   - **Cross-cutting concerns set per-callsite, not centrally**: `--dangerously-skip-permissions` (H5),
     `Path.home() / ".claude"` (multiple), encoding flags on `open` (L3).
3. **One real security finding (C1)** — the `shell=True` invocation in `install_mcp` is the highest-priority fix.
4. **Two latent bugs**:
   - `doctor.py` plugin check relies on a non-public pytest API (H4).
   - `eval/commands.py` reaches into the real `~/.claude/settings.json` despite a `HomeIsolation` adapter (H6).
5. **`audit/` (43 files) lives in `cli/` but is a static-analysis library** — the largest single
   miscategorization in the tree (M6).
6. **`task_builder/` is empty**, `cleanup_audit/portify-summary.md` is stray — housekeeping (L1, L2).

---

## Severity counts

| Severity  | Count |
|-----------|-------|
| Critical  | 1     |
| High      | 6     |
| Medium    | 7     |
| Low       | 6     |
| Nit       | 4     |
| **Total** | **24** |

Top three to address first: **C1** (shell=True), **H4** (broken doctor probe), **H6** (eval bypassing home isolation).
