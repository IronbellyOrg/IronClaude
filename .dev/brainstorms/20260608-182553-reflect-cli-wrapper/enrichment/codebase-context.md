# Codebase Context — reflect-cli-wrapper (Wave 2A, quality_tier: primary/auggie)

Confirmed integration anchors for a thin `superclaude reflect run` wrapper.

## A. Bash-window / subprocess-launch precedent (sprint)

- `cli/sprint/tmux.py::launch_in_tmux` — `tmux new-session -d -s <name> … <sprint_cmd>` (detached), builds panes, then `tmux attach-session` **blocks until detach/session end**, then reads the inner exit code from a **`.sprint-exitcode` sentinel file** (`config.state_dir/.sprint-exitcode`). → This is the canonical "open a window, run a command, recover its exit code" mechanic the wrapper can reuse.
- `_build_foreground_command` appends `--model <m>`, `--state-dir <dir>` (so inner/outer agree on the sentinel path), diagnostic flags.
- `cli/sprint/process.py::ClaudeProcess` (extends `cli/pipeline/process.py`) launches `claude --print --verbose` with: `model=config.model`, `output_format="stream-json"`, `permission_flag`, `timeout_seconds=max_turns*120+300`, `env_vars` (e.g. `CLAUDE_WORK_DIR` isolation), stdout/stderr file separation, `on_spawn/on_signal/on_exit` hooks, `SignalHandler` for graceful shutdown.
- `cli/eval/claude_process.py::ClaudeProcessAdapter` wraps `ClaudeProcess` with `HomeIsolation` (per-run `HOME` + `CLAUDE_SESSION_ID` env, chdir-pinned cwd) — the model for giving the headless `claude -p` its own MCP/settings/HOME so Serena/auggie + `ANTHROPIC_DEFAULT_*` reach the subprocess.

## B. Reflect contract the wrapper consumes (do NOT reimplement)

- `sc-reflect-protocol/SKILL.md` §9: writes `<output>/return-contract.yaml` (contract_version **1.3.0**) + `REPORT.md`; §15.1: `metrics.json`. Default `--output`: `.dev/reflect/<mode>-<slug>-<ts>/` (so the wrapper should PIN `--output` to a known path to locate the contract deterministically).
- Existing reflect↔sprint integration already exists: "sprint executor.py status routing" consumes the reflect contract — null `convergence_score` → `status: partial` + `next_action: halt-phase-for-review` (SKILL.md §8). The wrapper's verdict→gate routing should mirror this.
- STOP conditions to respect when building the invocation: `--mode post` needs `--diff` or `--task-log`; `--output` must not be under `.claude/skills|agents|commands`.

## C. CLI registration (if wrapper is a Click subcommand)

- `cli/main.py`: groups register via deferred import + `main.add_command(<group>, name="<name>")` (sprint, roadmap, tasklist, prd, eval, recommend, cli-portify…). A new `superclaude reflect` wires in identically: `from superclaude.cli.reflect import reflect_group; main.add_command(reflect_group, name="reflect")`.
- Note: `superclaude reflect` does not currently exist — greenfield subcommand.

## D. Implications for the design (feed the proposals)

1. The window mechanic has a turnkey precedent (detached tmux + attach + sentinel exit code) — proposals should weigh tmux-attach (blocking, visible) vs detached-and-poll (unattended).
2. Headless MCP/model parity is a solved problem via `HomeIsolation`/`env_vars` — but must be explicitly wired or Tier-2 + grounding degrade.
3. Reflect already emits a machine-readable contract AND already has a sprint consumer — the wrapper is mostly: build invocation → launch top-level `claude -p`/`reflect run` → locate pinned `return-contract.yaml` → map to `reflect_post` + exit code. Minimal new logic.
4. Two homes for the wrapper: a `cli/reflect/` Click subcommand (discoverable, testable, registers in main.py) vs a `scripts/` entrypoint (lighter). Proposals should pick with rationale.
