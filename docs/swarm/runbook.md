# MultiModelSwarm Operator Runbook

> **Status:** Phase 1 stub. Fleshed out in M9 (OPS-001) with run / status /
> logs / watch / resume / kill / attach workflows. This file currently records
> the AC-001 environment mandate so the guard test has a documentation anchor.

## Environment Mandate (AC-001)

All `superclaude swarm` operations **must** execute through the project's
UV-managed environment. Bare `python -m …` and `pip install …` invocations
are forbidden inside `src/superclaude/cli/swarm/` and rejected by the CI
guard `tests/swarm/test_uv_enforcement.py`.

### Required invocation shape

| Action                  | Use this                              | Not this                |
|-------------------------|---------------------------------------|-------------------------|
| Run a swarm subcommand  | `uv run superclaude swarm <verb> …`   | `python -m superclaude` |
| Install a dependency    | `uv pip install <pkg>`                | `pip install <pkg>`     |
| Execute an ad-hoc script| `uv run python <script>.py`           | `python <script>.py`    |
| Run the swarm test lane | `uv run pytest tests/swarm/ -v`       | `pytest tests/swarm/`   |

### Why this matters

- The pytest plugin, MCP integrations, and Click entry points all resolve
  through the UV environment declared in `pyproject.toml`. Bypassing UV
  loads a different interpreter and silently skips the registered
  plugins, producing tests that pass locally but fail in CI.
- The fork's CLAUDE.md (`/config/workspace/IronClaude/.claude/worktrees/BareReview/CLAUDE.md`)
  pins UV as a project-wide rule; AC-001 is its concrete enforcement on
  the swarm surface.

### CI guard

`tests/swarm/test_uv_enforcement.py` scans every text source under
`src/superclaude/cli/swarm/` for the forbidden patterns. The guard runs
even when the swarm package is still empty so it cannot regress to a
silent no-op once files appear. Comment lines that explicitly describe
the prohibition (mentioning `uv`, `forbidden`, `must use`, or `do not`)
are skipped so this runbook and any in-source caveats remain legal.

### How to fix a violation

1. Replace `python -m <mod>` with `uv run python -m <mod>` (or the
   native CLI entry point, e.g. `uv run superclaude …`).
2. Replace `pip install <pkg>` with `uv pip install <pkg>`.
3. Re-run `uv run pytest tests/swarm/test_uv_enforcement.py -v`.

### References

- Roadmap row R-001 / AC-001 — `Python ≥3.10 + UV mandate`.
- Phase 1 tasklist T01.01 — this task.
- Project rule: CLAUDE.md, *Python Environment Rules*.

## Rich TUI Dependency (AC-007)

`pyproject.toml` pins `rich>=13.0.0` so the optional dashboard in
`src/superclaude/cli/swarm/tui.py` (T07.01 / COMP-013) can rely on a
stable `rich.live.Live` API. **Rich is opt-in**: it is only ever
instantiated when both of the following hold (`should_enable_tui` in
`tui.py`):

1. The operator passes `--tui` to `swarm run`.
2. The target stream (default `sys.stdout`) is a TTY.

If either side is false, the dashboard is never started and no terminal
control sequences reach the caller. Non-TTY callers (CI logs, pipes,
file redirection) therefore see plain text only, satisfying INV-012.
Rich is a hard dependency rather than an extra because the import is
cheap, but importing it does **not** activate the dashboard -- the gate
above does.

### Verification

```bash
uv run python -c "from importlib.metadata import version; v = version('rich'); assert tuple(int(x) for x in v.split('.')[:2]) >= (13, 0), v"
grep '^rich' pyproject.toml  # rich>=13.0.0
uv run pytest tests/swarm/test_inv012_tui_opt_in.py -v
```

### References

- Roadmap row R-131 / AC-007 -- Rich pinned, TUI behind `--tui`.
- Phase 7 tasklist T07.01 / T07.03 / T07.16.
- INV-012 (no terminal control sequences on non-TTY stdout).

## T2 Proxy Env Contract (AC-017)

The Phase-1 `OpenAICompatTransport` (`src/superclaude/cli/swarm/transports/openai_compat.py`)
resolves its endpoint, bearer token, and per-slot model identifiers from
the process environment at Wave 0 via
`openai_compat.read_env()`. The reader emits a frozen
`TransportConfig` carrying the structured contract, or raises
`TransportEnvError` with the missing variable names listed in
`TransportEnvError.missing` so the INV-007 empty-pool failure path
(`tasklist/phase-2/T02.11`) can surface them verbatim.

### Required variables

| Variable      | Purpose                                                   | Required |
|---------------|-----------------------------------------------------------|----------|
| `T2ProxyUrl`  | Base URL of the OpenAI-compatible proxy (e.g. `https://proxy.example.com/v1`). `/chat/completions` is appended at send time. | **Yes** |
| `T2ProxyKey`  | Bearer token sent as `Authorization: Bearer <key>`.        | **Yes** |
| `T2Model01`   | Model identifier for worker slot 1.                        | **Yes** |
| `T2Model02..T2Model09` | Optional model identifiers for slots 2-9. Empty slots are skipped; the resolved `models` tuple stays dense and ordered by slot index. | Optional |

The slot probe is bounded by `T2_MODEL_MAX_SLOTS = 9`
(`src/superclaude/cli/swarm/config.py`); at least one populated slot is
mandatory.

### Resolution semantics

- Values are read verbatim from `os.environ` (tests pass an explicit
  `Mapping` for determinism).
- Surrounding whitespace is stripped; whitespace-only values are treated
  as absent.
- Missing or empty mandatory variables raise `TransportEnvError`. The
  exception lists every missing name in one shot so operators can fix
  the contract in a single pass instead of trial-and-error.
- `TransportConfig` is `frozen=True`; downstream stages cannot rewrite
  the resolved contract after Wave 0.

### Example -- minimal happy-path env

```bash
export T2ProxyUrl="https://proxy.example.com/v1"
export T2ProxyKey="sk-redacted"
export T2Model01="gpt-5-codex"
```

### Example -- multi-slot deployment

```bash
export T2ProxyUrl="https://proxy.example.com/v1"
export T2ProxyKey="sk-redacted"
export T2Model01="gpt-5-codex"
export T2Model02="mistral-large-2407"
export T2Model03="qwen2.5-coder-32b"
```

### Verification

- `uv run pytest tests/swarm/test_t2_env_contract.py -v` -- contract
  surface (env-var names, dense-models ordering, error reporting).
- `uv run pytest tests/swarm/test_openai_compat.py -v` -- transport
  outcome matrix plus the env-gated live lane that smoke-tests the
  proxy when `T2ProxyUrl` / `T2ProxyKey` / `T2Model01` are all set.

### References

- Roadmap row R-085 / AC-017 — `T2 proxy env-var contract`.
- Phase 3 tasklist T03.21 — this section.
- Coupled: INV-007 empty-pool failure path
  (`tasklist/phase-2/T02.11`) consumes the structured diagnostic.

## tmux is Optional (AC-008)

`tmux` is a **detached-mode-only** dependency. The default `swarm run`
invocation executes the Wave 0 → Wave 3 pipeline inline in the calling
process and never imports
`src/superclaude/cli/swarm/tmux.py`. Hosts without tmux on `PATH`
(minimal CI containers, locked-down build agents, the GitHub Actions
default runner without an explicit install step) can still run every
non-detached subcommand — `run`, `status`, `logs`, `scaffold`,
`validate`, `validate-lenses` — to completion.

### Mode matrix

| Invocation                          | Requires tmux? | Behavior when tmux is missing                                                                 |
|-------------------------------------|----------------|-----------------------------------------------------------------------------------------------|
| `swarm run …` (no `--detached`)     | **No**         | Inline pipeline runs to completion; tmux is never consulted.                                  |
| `swarm run --detached …`            | **Yes**        | Exits `EXIT_USAGE` (2) with a stderr diagnostic naming tmux. **No silent fallback to inline.** |
| `swarm attach <job_id>`             | **Yes**        | Raises `TmuxUnavailableError`; the subcommand surfaces it as a clean operator error.          |
| `swarm kill <job_id>`               | **Yes**        | Raises `TmuxUnavailableError`; an absent tmux means no detached job could have been launched. |
| `swarm status` / `swarm logs`       | **No**         | Read `.swarm-state.json` / `execution-log.jsonl` from disk; no process supervision needed.    |

### Detection

`is_tmux_available()`
(`src/superclaude/cli/swarm/tmux.py`) is the single gate. It returns
`True` only when both hold:

1. `shutil.which("tmux")` resolves to a binary on `PATH`.
2. The current process is **not** already nested inside an outer tmux
   session (`TMUX` env var unset). Nested-launch is technically legal
   but hides the new session behind the outer one, so the detached
   contract intentionally rejects it.

The detached branch in `commands.py::_launch_detached_run` calls this
predicate before staging the spec snapshot. A `False` result short-
circuits the launch with an actionable stderr diagnostic; the operator
either installs tmux, detaches from the outer tmux, or drops the
`--detached` flag.

### Why no silent fallback

Detached mode is an explicit operator opt-in:

- The operator passed `--detached` to walk away and reattach later
  via `swarm attach <job_id>`.
- Silently falling back to inline would block the operator's terminal
  on a long-running fan-out they expected to background, contradicting
  the explicit intent of the flag.
- Surfacing the missing-tmux condition up front is the kinder failure
  mode: the operator fixes the environment once, not after wondering
  why their terminal is pinned for the next 15 minutes.

This matches the AC-007 (Rich TUI) opt-in posture from the section
above: features that require additional host machinery are gated on
explicit flags, and the gate fails loudly when the machinery is
absent.

### Verification

```bash
uv run pytest tests/swarm/test_tmux_fallback.py -v
uv run pytest tests/swarm/test_tmux_detached.py -v   # passes-or-skips
```

The first test forces `shutil.which("tmux")` to `None` and confirms:

- `is_tmux_available()` returns False.
- `swarm run --detached` exits `EXIT_USAGE` with a tmux diagnostic.
- The inline default `swarm run` reaches dispatch and exits `EXIT_OK`
  with zero references to tmux on stderr.

The second test exercises live tmux integration when the binary is
present and skips cleanly when it is not.

### References

- Roadmap row R-132 / AC-008 — tmux-optional fallback.
- Phase 7 tasklist T07.02 / T07.11 / T07.17 — detached wrapper +
  `--detached` wiring + this section.
- Coupled: AC-007 Rich opt-in (above) shares the explicit-opt-in
  posture for host-dependent features.
