# Agent 6 — Installer & Sync Eval Proposals

## Proposal 1 (one-off): `sync_dev_idempotent_and_complete`

- **Target:** Makefile sync/verify.
- **Hypothesis:** `make sync-dev` copies canonical `src/superclaude/` skills, agents, commands, hooks, templates to `.claude/` and is idempotent.
- **Cadence:** one-off baseline.
- **Inputs:** prompt Claude to run `make sync-dev`, `make verify-sync`, `make sync-dev`, `make verify-sync`.
- **Assertions:** both exit 0; `.claude/skills`, `.claude/agents`, `.claude/commands/sc`, `.claude/hooks`, `.claude/templates` exist.
- **Requires:** `claude`, `make`, `uv`, `jq`, `diff`.
- **Complexity:** medium.
- **Value:** Catches drift in Makefile copy manifest.
- **Evidence:** `Makefile:109-158`, `Makefile:166-353`.

## Proposal 2 (one-off): `isolated_install_force_registers_components_and_pytest_plugin`

- **Target:** installer and pytest plugin.
- **Hypothesis:** Installed CLI supports core, commands, agents, skills, hooks, templates, and pytest entrypoint loads plugin fixtures.
- **Cadence:** one-off baseline.
- **Inputs:** in ephemeral HOME, prompt Claude to run `uv run superclaude install --force --list`, `uv run superclaude install --force`, and pytest `--trace-config`.
- **Assertions:** exit 0; files under HOME `.claude/commands/sc`, `agents`, `hooks`, `templates`; pytest output contains `superclaude`.
- **Requires:** `claude`, `uv`, `pytest`.
- **Complexity:** medium.
- **Value:** Verifies package entrypoints and install surface.
- **Evidence:** `pyproject.toml:65-70`, `src/superclaude/cli/main.py:153-202`, `src/superclaude/pytest_plugin.py:45-145`.

## Proposal 3 (recurring): `installer_sync_drift_continuous`

- **Target:** drift and registration gates.
- **Hypothesis:** Source-of-truth and generated `.claude/` remain aligned; hook registration list tracks scripts.
- **Cadence:** recurring — continuous/CI on PR + nightly. `src/superclaude/` is canonical, `.claude/` is generated.
- **Inputs:** prompt Claude to run `make verify-sync`.
- **Assertions:** exit 0; no missing/diff/stale output.
- **Requires:** `make`, `uv`, `jq`, `diff`, `grep`.
- **Complexity:** simple.
- **Value:** Catches missing generated files, stale hook installer list, matcher drift.
- **Evidence:** `CLAUDE.md:112-128`, `Makefile:307-345`.
