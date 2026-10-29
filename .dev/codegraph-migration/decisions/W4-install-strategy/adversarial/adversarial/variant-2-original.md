# Option B: delegate to upstream installers (install.sh + `codegraph install`)

Context and evidence: `.dev/codegraph-migration/research/codegraph-evaluation.md` sections 1-5.

## What it does
- `superclaude install` replaces the Codebase Memory phase with a thin wrapper:
  1. `CODEGRAPH_VERSION=v1.6.2 sh <(curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/v1.6.2/install.sh)` (script fetched at the pinned tag) — writes `~/.codegraph/versions/v1.6.2/` and `~/.local/bin/codegraph`.
  2. `codegraph install --target=claude --location=global --yes` — upstream writes `mcpServers.codegraph` (with `alwaysLoad`) to `~/.claude.json`, `mcp__codegraph__*` to `~/.claude/settings.json`, a `UserPromptSubmit` hook `codegraph prompt-hook`, and a marker-fenced block in `~/.claude/CLAUDE.md`.
  3. `codegraph telemetry off`.
- `./update.sh` re-runs the same; `codegraph upgrade` is the upstream update path (it re-runs install.sh and `codegraph install --refresh`).
- Coder image: does not bake; first `superclaude install` per workspace installs it.

## Strengths
- Least IronClaude code: a few subprocess calls and a version check.
- Upstream keeps its own config shape correct across releases (`--refresh`, legacy hook clean-up, opencode/Codex targets if wanted later).
- The upstream prompt hook front-loads context automatically.

## Weaknesses
- No integrity check: upstream `install.sh` downloads and extracts without verifying `SHA256SUMS` (install.sh lines 71-82). IronClaude would have to add its own check anyway to get one.
- Upstream installer edits `~/.claude.json`, `~/.claude/settings.json` (adds a hook) and `~/.claude/CLAUDE.md`. `superclaude install --force` then overwrites `~/.claude/CLAUDE.md` (`install_core.py:62-71`), wiping the block; ordering becomes fragile and re-runs keep fighting.
- The prompt hook injects an explore payload into every prompt in indexed repos (measured: a 41-symbol payload for one prompt), a context cost IronClaude has not chosen.
- Behaviour of IronClaude's install now depends on upstream installer changes between pins; `--yes` defaults (`--target=auto` detects every agent) can change.
- `curl | sh` from a third-party single-maintainer repo in the required install path.
