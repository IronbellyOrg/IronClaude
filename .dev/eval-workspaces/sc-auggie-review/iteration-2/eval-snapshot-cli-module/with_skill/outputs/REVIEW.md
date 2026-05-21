# Code Review: snapshot src/superclaude/cli/

**Target**: snapshot — `src/superclaude/cli/`
**Reviewer**: /sc:auggie-review (depth=quick, focus=anti-patterns,architecture,quality)
**Generated**: 2026-05-20
**Source PR**: n/a (snapshot mode)
**Base ↔ Head**: n/a
**Stats**: 213 files (~69,630 LOC) reviewed; 10 findings + 3 cross-cutting (0 dropped during grounding); 2 severity remaps

---

## Summary

The CLI subtree shows clear signs of organic growth: ten subpackages (`sprint/`, `roadmap/`, `prd/`, `cli_portify/`, `cleanup_audit/`, `tasklist/`, `task_builder/`, `pipeline/`, `eval/`, `audit/`) each invented their own executor/models pattern with substantial overlap, and the eight `install_*.py` modules duplicate file-copy + overwrite-policy boilerplate. The top three risks are: (1) one **high**-severity shell injection vector in `install_mcp.py` that passes `env=os.environ` (not a copy) into `subprocess.run(..., shell=True)`, (2) the absence of any shared Step/Stage abstraction across seven pipeline subpackages, and (3) layering hygiene that is currently *documented* via NFR-PRD.7 comments rather than *enforced* by import-linter. Overall sentiment: **nits-only with one high to address** — no blocking correctness defects, but the architecture is ripe for a deliberate consolidation pass.

## Findings

### Critical (block merge)

_(none)_

### High (should fix before merge)

#### H1. Shell injection / privilege bleed via `shell=True` with `env=os.environ`
- **File**: `src/superclaude/cli/install_mcp.py:140`
- **Category**: security
- **Source**: auggie
- **Evidence**:
  ```python
  cmd_str = " ".join(shlex.quote(str(arg)) for arg in cmd)
  user_shell = os.environ.get("SHELL", "/bin/bash")
  return subprocess.run(
      cmd_str, shell=True, env=os.environ, executable=user_shell, **kwargs
  )
  ```
- **Why this matters**: `shlex.quote` mitigates argument injection but the broader issue is twofold: `env=os.environ` passes the *live mapping* (not a copy), so any in-process mutation leaks into child processes; and `executable=user_shell` lets `$SHELL` choose the interpreter — a hostile `.bashrc`/`.zshrc` therefore gets sourced. Combined, the surface is wider than necessary for "support shell aliases."
- **Recommendation**: Pass `env=os.environ.copy()`; consider dropping `shell=True`/`executable=user_shell` entirely (aliases rarely matter for the binaries this code launches: `docker`, `npx`). If alias support must stay, gate it behind an explicit `--use-user-shell` flag.

### Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. `sys.path.insert(0, ...)` at module import time pollutes interpreter state
- **File**: `src/superclaude/cli/main.py:13`
- **Category**: anti-pattern
- **Source**: auggie
- **Evidence**:
  ```python
  sys.path.insert(0, str(Path(__file__).parent.parent.parent))
  from superclaude import __version__
  ```
- **Why this matters**: The package is installed via `hatchling` and an entry point; `sys.path.insert` here is dead-code-for-prod that masks editable-install bugs and corrupts `sys.path` ordering for any other consumer that imports `main`.
- **Recommendation**: Delete the `sys.path.insert` line. If a non-installed dev mode is required, document `pip install -e .` (already standard via `make dev`).

#### M2. `install_airis_gateway` is a 254-line god function
- **File**: `src/superclaude/cli/install_mcp.py:167`
- **Category**: maintainability
- **Source**: auggie
- **Evidence**: function body spans 167–420; mixes docker availability check, dir creation, compose download, env templating, secret prompting, container lifecycle, Claude Code registration, and rollback.
- **Why this matters**: 7+ responsibilities in one frame; nearly impossible to test seams in isolation; rollback paths inside the same function repeat the cleanup logic.
- **Recommendation**: Split into `_ensure_docker()`, `_render_compose(install_dir)`, `_prompt_env(install_dir)`, `_start_gateway(install_dir, dry_run)`, `_register_with_claude(install_dir)`, `_rollback(install_dir)`. Keep `install_airis_gateway` as a 30-line orchestrator.

#### M3. `_merge_settings` is a 183-line function with nested collision detection
- **File**: `src/superclaude/cli/install_hooks.py:233`
- **Category**: maintainability
- **Source**: auggie
- **Evidence**: function signature at line 233, with deeply nested loops merging hook entries across event/matcher pairs.
- **Why this matters**: Settings merge is exactly the kind of code that needs unit coverage, but the function is too large to test surgically; collision policy is interleaved with traversal.
- **Recommendation**: Extract a small pure helper `merge_hook_entry(existing, incoming, *, force) -> MergeOutcome` and let `_merge_settings` be a driver loop. Add table-driven unit tests on the helper.

#### M4. Duplicated file-copy boilerplate across six `install_*.py` modules
- **File**: `src/superclaude/cli/install_core.py:48`
- **Category**: maintainability / architecture
- **Source**: auggie
- **Evidence**:
  ```python
  for src_file in core_files:
      dest_file = target_path / src_file.name
      if dest_file.exists() and not force:
          skipped.append(src_file.name); continue
      try:
          shutil.copy2(src_file, dest_file)
          installed.append(src_file.name)
      except Exception as e:
          failed.append(f"{src_file.name}: {e}")
  ```
- **Why this matters**: The same shape recurs in `install_agents.py`, `install_commands.py`, `install_skills.py`, `install_templates.py`, with each module re-implementing overwrite policy + tally semantics slightly differently. Drift here causes user-visible inconsistencies (e.g., "force" sometimes means "delete-then-copy" and sometimes "copy-over").
- **Recommendation**: Introduce a shared `copy_pack(sources, target_path, *, force, kind="files") -> CopyReport` helper and have every installer call it. One spec, one test surface.

#### M5. Bottom-of-file subcommand imports + `add_command` after the `__main__` pattern
- **File**: `src/superclaude/cli/main.py:400`
- **Category**: architecture / anti-pattern
- **Source**: auggie (severity upgraded from low after grounding)
- **Evidence**:
  ```python
  from superclaude.cli.sprint import sprint_group
  main.add_command(sprint_group, name="sprint")
  # ... 6 more pairs ...
  if __name__ == "__main__":
      main()
  ```
- **Why this matters**: Mixing eager top-of-file imports (`install_*` family inside command callbacks) with eager bottom-of-file `add_command` registration in the *same* file is inconsistent — and the registrations sit *after* the `version` command but *before* the `__main__` guard, which is a layout that quietly breaks if anyone later wraps `main` in a try/except or moves the `__main__` check. Subcommand discovery should be deterministic.
- **Recommendation**: Move all `from .X import group; main.add_command(...)` calls to a dedicated `_register_subcommands(main)` function called *once* immediately after `@click.group()`. This also enables import-time error messages that name the failing subcommand.

#### M6. `except Exception: pass` swallowing in cleanup paths
- **File**: `src/superclaude/cli/sprint/executor.py:1735`
- **Category**: anti-pattern
- **Source**: auggie
- **Evidence**:
  ```python
  finally:
      try: monitor.stop()
      except Exception: pass
      if proc_manager is not None:
          try: proc_manager.terminate()
          except Exception: pass
      try: tui.stop()
      except Exception: pass
      try: signal_handler.uninstall()
      except Exception: pass
  ```
- **Why this matters**: Four consecutive `try/except Exception: pass` blocks in a `finally` clause is defensible in principle (cleanup must not raise) but the *bare-`pass`* policy means failures are invisible — a leaked TUI thread or stuck subprocess will be silently tolerated forever.
- **Recommendation**: Log at WARN level inside each `except` (`logger.warning("monitor.stop failed", exc_info=True)`); keep the swallow so cleanup continues. Two-line change per block, large debuggability win.

### Low (nice-to-have)

#### L1. Hardcoded `~/.superclaude/airis-mcp-gateway/` install path
- **File**: `src/superclaude/cli/install_mcp.py:194`
- **Category**: architecture
- **Source**: auggie
- **Evidence**: `install_dir = Path.home() / ".superclaude" / "airis-mcp-gateway"`
- **Why this matters**: Conflicts with the `XDG_DATA_HOME` convention and makes multi-version installs impossible.
- **Recommendation**: Read `os.environ.get("XDG_DATA_HOME", "~/.local/share") / "superclaude" / "airis-mcp-gateway"` with the current path as a back-compat fallback.

### Nits

- **N1.** Public CLI entry points lack `-> None` return annotations (`main.py:46` and siblings). Idiomatic Click does not require them, but adding them helps mypy and IDEs. _(Downgraded from low after grounding; not load-bearing.)_

## Architectural / Cross-Cutting Observations

#### X1. No shared Step/Stage abstraction across seven pipeline subpackages
- **Manifests in**: `cli/sprint/`, `cli/roadmap/`, `cli/tasklist/`, `cli/prd/`, `cli/cli_portify/`, `cli/cleanup_audit/`, `cli/pipeline/`
- Each subpackage has invented its own `executor.py` / `models.py` / `process_manager.py` shape. Common concerns (subprocess lifecycle, turn-budget enforcement, signal-aware shutdown, structured logging) are re-implemented with subtle behavioural drift. `prd/executor.py` already documents this drift defensively in its module docstring (NFR-PRD.1, .3, .4, .7, .9).
- **Recommendation**: Promote `cli/pipeline/` to a real base layer with `StepExecutor`, `TurnBudget`, `SignalAwareSubprocess`, and a `PipelineLogger` protocol. Each domain subpackage then provides only domain logic.

#### X2. Layering hygiene is documented, not enforced
- **Manifests in**: `cli/prd/executor.py:15`, `cli/prd/logging_.py:7`, `cli/prd/tui.py:8`, `cli/prd/config.py:7`, `cli/prd/diagnostics.py:10`, `cli/prd/models.py:7`, `cli/prd/monitor.py:9`, `cli/prd/prompts.py:8` (every prd/ module repeats the same NFR-PRD.7 docstring)
- The fact that eight files repeat *"No imports from superclaude.cli.sprint or superclaude.cli.roadmap"* in their docstrings is strong evidence the constraint matters — and equally strong evidence it is currently enforced only by social pressure.
- **Recommendation**: Add `import-linter` (or `tach`) with a forbidden-contract rule: `cli.prd ↛ cli.sprint, cli.roadmap`. Run in CI. Delete the eight redundant docstring lines once the constraint is machine-checked.

#### X3. Three competing output styles: `click.echo`, Rich TUI, Python `logging`
- **Manifests in**: `cli/install_mcp.py` (click.echo throughout), `cli/main.py` (click.echo), `cli/sprint/debug_logger.py` (custom writer), `cli/prd/diagnostics.py` (DiagnosticCollector)
- Users see different message formatting depending on which subcommand they invoke; debug logs for sprint do not interleave with installer output the way diagnostics for prd do.
- **Recommendation**: Pick one user-facing output channel (Click is dominant) and route everything else (debug, telemetry) through stdlib `logging` with a single project-wide formatter. Document in a `CLI_STYLE.md` and add a lint rule that bans bare `print()` under `cli/`.

## Audit

- Auggie chunks: 1 (succeeded: 1, retried: 0, skipped: 0)
- Findings emitted by Auggie: 10 + 3 cross-cutting
- Findings dropped during grounding: 0
- Severity remaps: 2 (1 down — N1; 1 up — M5)
- Persona cross-check: disabled (depth=quick)
- Token cost: Claude ≈ orchestration only (validation + synthesis); Auggie ≈ single ~131s `--output-format json --ask` pass

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 1 medium: 6 low: 1 nit: 1
dropped: 0
auggie_chunks: 1
duration_sec: 131
-->
