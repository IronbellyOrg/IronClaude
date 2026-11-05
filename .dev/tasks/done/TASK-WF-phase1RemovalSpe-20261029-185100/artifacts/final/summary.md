# Phase 1 final gate evidence (Task 18)

Run on branch ironbelly/feat-codememory-codegraph-init at HEAD cedf04ab (cedf04ab was the last code commit; later commits are task-package files only).

## 1. Sync and lint

### make sync-dev && make verify-sync
```
$ bash -c make sync-dev && make verify-sync
  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
rc=0
```

### make lint (ruff 0.15.20 via a PATH shim, because ruff is not installed in the venv; decision 4)
```
$ env PATH=/tmp/p1-rufbin:/home/coder/.config/orca/linux-orca-cli-shim:/home/coder/.local/bin:/usr/local/bin:/opt/nvm/versions/node/v24.22.1/bin:/home/coder/.local/bin:/home/coder/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games make lint
  Errors:   0
  Warnings: 5
  ✅ PASS — architecture policy compliant (5 warning(s))
Running linter...
uv run ruff check .
All checks passed!
rc=0
```

### uv run ruff format --check src/superclaude/cli tests/cli (same shim)
```
$ env PATH=/tmp/p1-rufbin:/home/coder/.config/orca/linux-orca-cli-shim:/home/coder/.local/bin:/usr/local/bin:/opt/nvm/versions/node/v24.22.1/bin:/home/coder/.local/bin:/home/coder/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games uv run ruff format --check src/superclaude/cli tests/cli
441 files already formatted
rc=0
```

## 2. Full suite against the baseline (DoD-5)

```
$ T02_15_PERF_REPORT=/tmp/p1-perf.json uv run pytest -q -p no:cacheprovider --tb=line -rfE | tee final/full.txt
= 5 failed, 14076 passed, 137 skipped, 2 xpassed, 32 warnings in 408.05s (0:06:48) =
$ comm -13 <(baseline FAILED/ERROR ids) <(final FAILED/ERROR ids)
(no output above this line = no new failure; the 5 failures are the same tests/cli/eval ruff tests as the baseline, because ruff is not installed in the venv)
```

## 3. Residual search (DoD-1)
```
$ bash artifacts/acceptance-search.sh all | tee final/search.txt
./tests/sc-roadmap/integration/test_wave5_completion.py:35:        """SKILL.md should include think_about_whether_you_are_done()."""
./tests/sc-roadmap/integration/test_wave5_completion.py:36:        assert "think_about_whether_you_are_done" in skill_md_content
ACCEPTANCE_SEARCH_FAIL all 23
```
## 3b. Residual search variance (DoD-1)

The literal `bash artifacts/acceptance-search.sh all` printed 23 hits: 21 in `.serena/project.yml` and 2 in `tests/sc-roadmap/integration/test_wave5_completion.py`.
- `tests/sc-roadmap/...:35-36` asserted the Serena tool `think_about_whether_you_are_done` in a SKILL that no longer has it (the test is skipped: its fixture cannot find the SKILL path). Fixed: the test was deleted (decision 10); `uv run pytest tests/sc-roadmap` -> 222 passed, 86 skipped.
- `.serena/project.yml` (with `project.local.yml` and `.gitignore`) was regenerated at 00:42:12 by the live Serena MCP server attached to this session (`uvx ... serena start-mcp-server --project-from-cwd`, running since Oct 28). The files are untracked and gitignored (`.gitignore:113`); source section 2.3 keeps project `.serena/` folders as user data. They were NOT deleted. The search was re-run over every top-level entry except `.serena` (`bash artifacts/acceptance-search.sh all <entries>`) and printed:
```
ACCEPTANCE_SEARCH_OK all
```

## 4. Sandbox runs (DoD-2, DoD-3, DoD-4 partly, robustness)

The exact commands are in `./sandbox-script.sh` (this folder): the seeds (the Tier R `serena` row (a) with `"env":{}`, `codebase-memory-mcp` at `/usr/local/bin/codebase-memory-mcp`, `tavily`, a project-scope `serena`, the baseline `hooks.json:47` matcher with `~/.claude/hooks/freshness-pre-edit.sh`, and the stale `CLAUDE.md` and `commands/sc/reflect.md` that each name `serena`), the stub `claude`, the installed-allowlist `FILTER`, every `rg` residual search, every `jq` assertion, the backup assertion and `UV_CACHE_DIR="$(uv cache dir)"` are written out there. That file was re-created verbatim from the script that ran; the executed copy under `/tmp` was deleted at cleanup. Safety: every call sets `HOME` and `CLAUDE_CONFIG_DIR` to a temp dir (never the real ones), the PATH has no Orca directory, the stub `claude` logs to `$HOME/claude-calls.log` (`--version` and `plugin` succeed, `mcp remove <name> --scope user` deletes `.mcpServers[<name>]` with jq, everything else exits 1), and `./update.sh` ran with `PIPX_HOME`/`PIPX_BIN_DIR` inside the temp dir.

Deviation, no-Claude-CLI run: it used `$(pwd)/.venv/bin/superclaude` with `PATH=/usr/bin:/bin` instead of `uv run --no-sync superclaude`, because `uv` and `claude` both live in `/usr/local/bin`, so a PATH without `claude` has no `uv`; the same installed code ran.

Stale-file overwrite (DoD-3 "old core files"): the seeded `~/.claude/CLAUDE.md` and `~/.claude/commands/sc/reflect.md` each held a line naming `serena`; after `./update.sh` the residual search over `$T/old/.claude` (line `existing residual search over ~/.claude`) is empty, which proves both were overwritten.

```
sandbox root: /tmp/p1-sbx.cLLwPW
== FRESH: superclaude install in an empty HOME ==
fresh install rc=0
✅ Plugins: installed frontend-design@claude-plugins-official, playwright@claude-plugins-official, notion@claude-plugins-official, dropbox@claude-plugins-official, google-cloud-storage@claude-plugins-official, understand-anything@understand-anything

📦 Retiring stale MCP registrations...
   No retired MCP registrations present.
fresh residual search: EMPTY (pass)
fresh claude call log: no mcp add (pass)
fresh claude calls: 8
== EXISTING: seeded HOME, then ./update.sh ==
seeded: ["codebase-memory-mcp","serena","tavily"]
update.sh rc=0
✅ pytest plugin loaded
✅ Agents installed
✅ Skills installed
✅ Configuration
✅ ccsession installed (warning: ~/.local/bin not on PATH)
✅ Retired MCP registrations

✅ SuperClaude is healthy
keys after: ["tavily"]  (expect ["tavily"])
project-scope serena kept: true  (expect true)
settings.json: no mcp__serena (pass)
existing residual search over ~/.claude: EMPTY (pass)
settings.json.bak.* backup exists (pass): 1
existing claude calls: 2 mcp remove; adds: 0
0
== PIN: current-pin serena entry is kept ==
pin install rc=0
serena entry kept: true  (expect true)
output contains the Tier K line (pass)
== ROBUSTNESS: no claude CLI on PATH ==
no-claude install rc=0, doctor rc=0 (expect 0 and 0)
== cleanup ==
```

- `./update.sh` ran end to end in the sandbox (`pipx install --force ./` built the wheel; rc=0), so the documented `pipx` fallback was not needed.
- Fresh HOME: no `mcp add` in the stub's call log; the residual search over the whole temp HOME is empty.
- Existing HOME: `codebase-memory-mcp` and the Tier R `serena` entries were removed through 2 `mcp remove` calls; `tavily` and the project-scope `serena` entry survived; `settings.json` lost the four `mcp__serena__*` matcher alternatives; the stale `CLAUDE.md` and `reflect.md` were overwritten; one `settings.json.bak.*` backup exists (kept).
- Current-pin entry: kept, and the install output contains "Legacy Serena registration kept until codegraph is ready" (expected for Phase 1 alone; Phase 2's gate removes it).
- No Claude CLI on PATH: `superclaude install` and `superclaude doctor --verbose` exit 0.

## 5. Cleanup

```
$ git status --short -- . ":!.dev"
 M tests/sc-roadmap/integration/test_wave5_completion.py
```
The only modified tracked file outside the package is `tests/sc-roadmap/integration/test_wave5_completion.py` (the intended decision-10 edit). `rm -rf $T` removed the sandbox; the `.ruff_cache` created by the lint runs and the temporary ruff shim were removed. The `settings.json.bak.*` backup lived inside the sandbox and went with it after it was asserted.

## 6. Verdict

| Check | Result |
|---|---|
| Sync and lint (make sync-dev, verify-sync, lint, format check) | pass (ruff via the pinned-version shim, decision 4) |
| Full suite vs baseline (DoD-5) | pass: 5 failed, all in the baseline; no new failing id |
| Residual search (DoD-1) | pass over repo content; `.serena/` regenerated local files excluded and documented in 3b |
| Sandbox fresh (DoD-2) | pass |
| Sandbox existing via ./update.sh (DoD-3) | pass |
| Current-pin entry kept with the Tier K line | pass |
| No Claude CLI robustness | pass |
