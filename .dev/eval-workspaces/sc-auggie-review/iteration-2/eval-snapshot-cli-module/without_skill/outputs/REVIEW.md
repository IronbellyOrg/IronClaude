# CLI Module Review — `src/superclaude/cli/`

- **Target**: `/config/workspace/IronClaude/src/superclaude/cli/`
- **Date**: 2026-05-20
- **Reviewer mode**: baseline (no skill / no protocol)
- **Repo**: IronClaude (branch `fix/prd-path-resolution-and-templates`)

## File Inventory

- **File count**: 213 (excluding `__pycache__/` and `*.pyc`)
- **Total LOC (Python)**: ~29.5k in sub-CLI packages + ~9.2k in `audit/` + ~17k in `eval/` (rough)
- **Top-level files**: `__init__.py`, `main.py`, `doctor.py`, `vocabulary.py`, `install_agents.py`, `install_commands.py`, `install_core.py`, `install_hooks.py`, `install_mcp.py`, `install_skill.py`, `install_skills.py`, `install_templates.py`
- **Sub-packages** (with file counts):
  - `audit/` (43 files; 9,231 LOC) — classification, coverage, checkpointing, validation, profiling, wiring-gate
  - `cleanup_audit/` (13) — Click group: cleanup-audit pipeline
  - `cli_portify/` (24 incl. `steps/`) — CLI-port workflow
  - `eval/` (24 incl. `pty/`, `schemas/`, `suites/`) — cliEval harness (PTY isolation, orchestrator, runner)
  - `pipeline/` (24) — generic step-sequencer; `process.py` houses base `ClaudeProcess`
  - `prd/` (14) — PRD generation pipeline
  - `roadmap/` (24) — roadmap pipeline (largest single module: `executor.py` @ 3,641 LOC)
  - `sprint/` (17) — sprint runner
  - `tasklist/` (6) — tasklist commands

Full file list is recorded in the parallel discovery output (`find … -type f`).

---

## Findings

### CRITICAL

#### C1. `install_mcp._run_command` invokes user shell with `shell=True`
- **File:line**: `src/superclaude/cli/install_mcp.py:140-142`
- **Issue**: On macOS/Linux the helper builds a string via `shlex.quote` and then runs `subprocess.run(cmd_str, shell=True, env=os.environ, executable=user_shell, **kwargs)`. Any caller that ever passes a value not in the trusted constants table (e.g. a future call site that takes user input) gets command injection by default. Using `shell=True` *also* defeats the `["docker","info"]`-style list convention used everywhere else and silently inherits the parent's full env (`env=os.environ`), which masks broken PATH/credential isolation in CI.
- **Why it's architectural**: every other subprocess call in the module (`docker compose up`, `claude mcp add`, `curl`) routes through this single helper, so the unsafe pattern is universalised across MCP installation — fixing the helper fixes all consumers. The Windows branch (`["cmd","/c"] + cmd`) is itself problematic — passing user input through `cmd /c` is a classic injection sink.
- **Recommended fix**: drop `shell=True`. Use `subprocess.run(cmd, ...)` with the list form; if the user-shell aliases really matter, restrict the shell wrapper to a hard-coded whitelist of commands and document the threat model.

#### C2. `roadmap/executor.py` is a 3,641-line god-module
- **File:line**: `src/superclaude/cli/roadmap/executor.py:1-3641` (54 top-level defs/classes; see `grep "^def\|^class"`)
- **Issue**: This single file mixes (i) step DAG construction (`_build_steps`, line 1936), (ii) per-step runner dispatch (`roadmap_run_step`, line 954), (iii) input routing/compression (`_route_input_files`, `_compress_pipeline_input`, ~lines 213-410), (iv) sanitisation (`_sanitize_output`, line 554), (v) structural and "anti-instinct" audits (lines 688-733), (vi) merge completeness validation (line 855), (vii) terminal UI / dry-run printing (`_print_terminal_halt`, `_print_step_plan`, ~lines 2281-2543), (viii) state persistence (`_save_state`, `read_state`, `write_state`, lines 2543-2818), (ix) deviation analysis (line 1590), and (x) resume/decomposition logic (`_apply_resume`, line 3541; `apply_decomposition_pass`, line 2831).
- **Why it's architectural**: this file is the single biggest source-of-truth for the roadmap pipeline. Any cross-cutting change (e.g. a new step type, a new resume mode) has to traverse ten orthogonal concerns interleaved by file order. The shape mirrors a classic "pipeline.py grew until people stopped extracting" anti-pattern; the comparable PRD/sprint/cleanup-audit sub-CLIs all kept the same responsibilities in dedicated modules (`models.py`, `process.py`, `gates.py`, `monitor.py`, `tui.py`), which strongly suggests this can be decomposed without inventing new abstractions.
- **Recommended fix**: split along the existing sibling-module taxonomy. At minimum: pull dry-run/terminal-printing into `roadmap/tui.py` (already exists as a name pattern), pull state I/O into `roadmap/state.py`, pull input-routing/compression into `roadmap/inputs.py`.

#### C3. `main.py` mutates `sys.path` at import time
- **File:line**: `src/superclaude/cli/main.py:13`
  ```python
  sys.path.insert(0, str(Path(__file__).parent.parent.parent))
  ```
- **Issue**: This is a packaging smell — the file is *inside* the `superclaude` package, so when it imports `from superclaude import __version__` on line 15, it should rely on the installed package, not on injecting `src/` into `sys.path`. This works for `uv run python -m superclaude.cli.main` from a source checkout but creates a foot-gun whenever the package is installed via pipx / pip (the inserted path likely points at site-packages parent and shadows other code).
- **Why it's architectural**: `main.py` is the CLI entry point declared in `pyproject.toml`. Side-effects at import time of the entry point propagate to every `superclaude` invocation in every environment.
- **Recommended fix**: remove the `sys.path.insert`. The Click entry point already imports the package via its installed name.

---

### HIGH

#### H1. Massive structural duplication across sub-CLI packages
- **File:line**: compare `src/superclaude/cli/prd/`, `src/superclaude/cli/sprint/`, `src/superclaude/cli/cleanup_audit/`, `src/superclaude/cli/cli_portify/` — each ships near-identical filename sets (`commands.py`, `config.py`, `diagnostics.py`, `executor.py`, `gates.py`, `logging_.py`, `models.py`, `monitor.py`, `process.py`, `prompts.py`, `tui.py`).
- **Evidence**:
  - `prd/logging_.py` vs `sprint/logging_.py` differ only in docstring and emoji-status table preamble (`diff` shows headers diverge but body is parallel).
  - `prd/process.py:1-28` and `cli_portify/process.py:1-22` both extend `pipeline.process.ClaudeProcess` with bespoke "retry / launch / @path" wrappers; they re-implement the same scaffolding rather than parameterising the base.
  - Files in lockstep (LOC counts): `process.py` (278 / 385 / 72 / 245), `monitor.py` (201 / 571 / 195 / 307).
- **Why it's architectural**: this is the highest-leverage refactor in the directory. Each new pipeline (PRD, sprint, etc.) currently copy-pastes the runtime scaffolding from a peer; bugs fixed in one (e.g. retry exponential backoff in `prd/process.py` per its docstring) don't propagate. The `pipeline/` package already provides the generic substrate (`pipeline/executor.py:1-10` explicitly says "Composition-via-callable design: consumers (sprint, roadmap) inject their own StepRunner") — the duplication shows that the abstraction stopped at executor/process and didn't reach logging/monitor/tui.
- **Recommended fix**: lift the dual-format JSONL+Markdown logger, the streaming monitor, and the TUI shell into `pipeline/` (or a new `cli/_shared/`) and inject per-pipeline status maps / labels. Concretely: a `PipelineLogger(name, status_emoji_map)` constructor replaces the four near-twin files.

#### H2. `subprocess.run(... shell=True, env=os.environ ...)` leaks the parent env
- **File:line**: `src/superclaude/cli/install_mcp.py:140-142`
- **Issue**: Passing `env=os.environ` directly (not `os.environ.copy()`) means a future `os.environ.pop(...)` inside `_run_command` (none today, but the pattern is fragile) would mutate the parent shell's view of the environment for the rest of the process. Even without mutation, propagating the full environment to `claude mcp add`, `docker compose`, and `curl` exposes any `*_API_KEY` the parent holds to every child — usually OK but worth narrowing for the curl downloads.
- **Recommended fix**: use `env={**os.environ, **overrides}` only for calls that genuinely need the user environment, and `env=None` (Popen default) where not.

#### H3. Broad `except Exception` swallows real errors silently
- **File:line**: `src/superclaude/cli/install_mcp.py:373` (gateway health check), `src/superclaude/cli/install_mcp.py:230` (curl download), `src/superclaude/cli/install_skill.py:54` (skill copy), `src/superclaude/cli/install_commands.py:59`
- **Issue**: At `install_mcp.py:373` the `except Exception: pass` inside the health-check retry loop is the worst offender — any failure (DNS, segfault, KeyboardInterrupt translated by a wrapper, ImportError) is folded into "gateway not healthy yet". `install_skill.py:54` returns `False, f"Failed to install skill: {e}"` swallowing every exception type — including `KeyboardInterrupt` if not handled by Click upstream. Pattern is replicated.
- **Why it matters**: install commands need to either fail loudly or fail with classification. Right now, a permission error on shutil.copytree and a typo in a path both look the same to the user.
- **Recommended fix**: catch specific exception types (`OSError`, `shutil.Error`, `subprocess.SubprocessError`) and re-raise everything else.

#### H4. `_get_commands_source()` returns a path even when it doesn't exist
- **File:line**: `src/superclaude/cli/install_commands.py:92-122`
- **Issue**: Comment on line 121 says "If neither exists, return package location (will fail with clear error)" — but the fall-through returns `package_commands_dir` unconditionally. Callers then call `command_source.glob("*.md")` which silently returns `[]` (Path.glob does not raise on a non-existent dir), and the function reports "No command files found" rather than "command source missing." Compare with `install_skill._get_skill_source` which correctly returns `None` and the caller branches.
- **Recommended fix**: return `None` and have the caller produce a structured error matching `install_skill`'s pattern.

---

### MEDIUM

#### M1. Cross-pipeline import isolation enforced only by docstring
- **File:line**: `src/superclaude/cli/prd/process.py:8` ("NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap"), `src/superclaude/cli/pipeline/process.py:8` ("NFR-007"), `src/superclaude/cli/pipeline/executor.py:6`
- **Issue**: The non-functional requirement that pipelines stay decoupled from each other is documented in three places but not actually checked. A typo'd import (say, `from superclaude.cli.sprint.models import ...` inside `prd/`) would compile and ship. The wiring-gate (`audit/wiring_gate.py`) appears to be the right enforcement point but there is no evidence it gates cross-package imports between sub-CLIs.
- **Recommended fix**: add an import-linter or `ast`-based check in CI; or add to `audit/wiring_gate.py` since the infrastructure already exists.

#### M2. Repeated `install_*` pattern not consolidated
- **File:line**: `src/superclaude/cli/install_agents.py`, `install_commands.py`, `install_skill.py`, `install_skills.py`, `install_core.py`, `install_templates.py`
- **Issue**: All six files implement the same three-step shape: (1) resolve source dir, (2) iterate, (3) `shutil.copy2` / `shutil.copytree` with `force` toggle and a "skipped" list. The `_get_*_source()` resolver functions follow the same package_root → repo_root probe sequence with small variations. `main.py:153-202` then composes them sequentially with copy-pasted `click.echo` framing.
- **Recommended fix**: extract `install_components(source, dest, force, kind="commands")` and a single `Installer` dataclass that owns the source-resolution rules.

#### M3. `install_skills.py:65` performs lazy `import shutil` inside a loop
- **File:line**: `src/superclaude/cli/install_skills.py:65`
  ```python
  if stale.exists():
      import shutil
      shutil.rmtree(stale)
  ```
- **Issue**: `shutil` is already imported transitively via `install_skill_command` but more importantly this lazy in-loop import is inconsistent with the rest of the file. Minor but indicates the file was touched in a hurry; pair-review missed it.
- **Recommended fix**: hoist to module scope.

#### M4. `main.py` performs late imports inside command handlers and at module footer
- **File:line**: `src/superclaude/cli/main.py:59-81` (inside `install`), `main.py:239` (inside `mcp`), `main.py:400-426` (post-function group registrations)
- **Issue**: Late imports inside command bodies (lines 59-81) are intentional — they keep `--help` fast by deferring imports. But the *trailing* imports at lines 400-426 are top-level and undo that optimisation; `superclaude --help` ends up importing the entire `eval/`, `prd/`, `roadmap/`, `sprint/`, `cleanup_audit/`, `cli_portify/`, `tasklist/` packages.
- **Why it matters**: contributes to slow `--help` and slow shell-completion latency. Click supports lazy-loading via `click.MultiCommand` / `CommandCollection`.
- **Recommended fix**: convert the sub-group registrations to lazy `add_command` callbacks or use `click-lazy-group`.

#### M5. `roadmap/executor.py:2342` carries an inline `TODO(v2.26)` for "dual-budget-exhaustion recovery"
- **File:line**: `src/superclaude/cli/roadmap/executor.py:2342`
- **Issue**: A TODO embedded in a generated string inside a long terminal-halt formatter is easy to miss. The fact that this is the *only* `TODO` in the entire CLI (verified with `grep -rn`) suggests the project polices TODO well — yet this one is buried.
- **Recommended fix**: hoist to an issue / drop a `# noqa` annotation that the audit pipeline can grep.

#### M6. `install_mcp.py` 802 LOC with embedded server registry + business logic
- **File:line**: `src/superclaude/cli/install_mcp.py:1-802`
- **Issue**: The MCP server table (`AIRIS_GATEWAY`, `MCP_SERVERS`) is hard-coded alongside Docker download logic, registration shell-out, and Click handlers. Adding a server (e.g. a new mindbase variant) edits the same file as the docker compose flow.
- **Recommended fix**: split the registry into `install_mcp_servers.py` data dict (or a YAML/JSON file under `cli/data/`) and keep `install_mcp.py` for orchestration.

---

### LOW

#### L1. Emoji-heavy CLI output not gated by `--no-color` / terminal capability
- **File:line**: `src/superclaude/cli/main.py:89-150`, `install_hooks.py:134-174`, et al. (`grep "click.echo" main.py | wc -l` = 64)
- **Issue**: `click.echo("📦 …")`, "✅ installed" / "⬜ not installed", "⚠️", "💾", "🔌" are unconditional. Output redirected to a file (e.g. CI logs) ends up sprinkled with unicode that some log scrapers mishandle.
- **Recommended fix**: use Click's color disabling helpers or wrap in a small `ui` module that respects `NO_COLOR`/`CI` env vars.

#### L2. `main.py` uses `click.option(... default="~/.claude/commands/sc")` and then re-expands manually
- **File:line**: `src/superclaude/cli/main.py:30-33, 162` (and parallel pattern at lines 263-265, 316-319)
- **Issue**: `Path(target).expanduser()` is called separately at three sites with the same default. `click.Path(expanduser=True)` does this declaratively.
- **Recommended fix**: pass `type=click.Path(file_okay=False, dir_okay=True)` plus a `callback=lambda c,p,v: Path(v).expanduser()`.

#### L3. `install_hooks.py:48` keeps `freshness-file-changed.sh` shipped despite docstring saying "v1: NOT registered. Kept on disk for v1.5"
- **File:line**: `src/superclaude/cli/install_hooks.py:48`
- **Issue**: An intentionally-orphan script is deployed by every install. The comment explains why (good!), and a `--no-orphans` flag is promised in v1.5, but in the meantime every install adds dead code to the user's `~/.claude/hooks/` directory.
- **Recommended fix**: track the orphan flag with a structured constant (`_ORPHAN_SCRIPTS`) so cleanup is one line.

#### L4. `_is_valid_skill_dir` accepts any `.json` file as a valid skill
- **File:line**: `src/superclaude/cli/install_skill.py:99-112`
  ```python
  for item in path.iterdir():
      if item.is_file() and item.suffix in {".ts", ".js", ".py", ".json"}:
          return True
  ```
- **Issue**: A directory containing only a stray `package.json` or `tsconfig.json` (no `SKILL.md`) will be misclassified as a skill, then `shutil.copytree` will happily install it. The intent (back-compat for skills authored in TS/JS) is reasonable, but the rule is too loose.
- **Recommended fix**: require `SKILL.md` (or one of the manifest variants) unconditionally. The `.ts/.js/.json` fallback was meant for early prototypes; ratchet it shut.

#### L5. `eval/runner.py` at 1,185 LOC, `audit/wiring_gate.py` at 1,122 LOC
- **File:line**: `src/superclaude/cli/eval/runner.py:1-1185`, `src/superclaude/cli/audit/wiring_gate.py:1-1122`
- **Issue**: Same family as C2 — large files that mix concerns. Less critical because both have docstring-tier separation, but next-largest-thing-to-refactor.
- **Recommended fix**: track in a "monolith decomposition" backlog item; not blocking.

---

### NITS

#### N1. Inconsistent docstring conventions
- **File:line**: e.g. `prd/process.py:1-12` (NFR labels), `install_skill.py:14-25` (Google-style), `install_commands.py:13-22` (mixed), `roadmap/executor.py:1-9` (free-form prose).
- **Recommendation**: pick one (Google or NumPy) and apply via `ruff pydocstyle` rules.

#### N2. `print` vs `click.echo` consistency
- **File:line**: scattered. `click.echo` dominates; spot-check `audit/` is `print`-free, but `eval/run_report.py` is mixed. `grep -n "print(" audit/*.py` returns zero — the audit subtree is the cleanest.

#### N3. `main.py:209-212` boolean OR chain
- **File:line**: `src/superclaude/cli/main.py:204-212`
- **Issue**: Six `not X_success or not Y_success ...` — replace with `any(not s for s in [...])` or a `Results` dataclass.

---

## Summary

| Severity   | Count |
|------------|-------|
| Critical   | 3     |
| High       | 4     |
| Medium     | 6     |
| Low        | 5     |
| Nit        | 3     |
| **Total**  | **21** |

**Headline architectural observations**:
1. **Pipeline scaffolding is duplicated four ways** (prd / sprint / cleanup_audit / cli_portify). The `pipeline/` package abstracted executor + process but stopped short of logger / monitor / tui — that is the single highest-leverage refactor (H1).
2. **`roadmap/executor.py` (3,641 LOC, 54 top-level symbols) is the biggest monolith**; its sibling sub-CLIs prove the decomposition target already exists in the project's own conventions (C2).
3. **`install_mcp._run_command`'s `shell=True`** is the most-replicated unsafe construct: a single 3-line fix neutralises injection risk across all MCP install paths (C1 / H2).
4. **`sys.path.insert` in the CLI entry-point** is a packaging smell that breaks the contract between editable installs and pipx installs (C3).
5. **The audit subtree (`cli/audit/`, 43 files, 9.2k LOC) is the cleanest part of the directory** — zero `click.echo`, no `print`, no shell=True, well-separated modules. It's a good model for the rest.
