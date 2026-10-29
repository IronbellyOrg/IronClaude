# codegraph evaluation (task W4, issue #323)

Date: 2026-10-29. Target: https://github.com/colbymchenry/codegraph. Worker task: task_474b364c6b98.

Sandbox (left in place): `/tmp/codegraph-eval.fQfO`. Upstream source files quoted below were downloaded read-only into `/tmp/codegraph-eval.fQfO/docs/` with `gh api repos/colbymchenry/codegraph/contents/<path> -H 'Accept: application/vnd.github.raw'` on 2026-10-29 (main branch head committed `2026-10-28T02:14:52Z`). Citations of the form `docs/<file>:<line>` refer to those copies; each is the upstream file at the same path.

**Verdict in one line:** the main project (colbymchenry/codegraph) is suitable; the fork sunerpy/codegraph-rust was not needed and was not evaluated.

## 1. Facts with sources

| Fact | Value | Source |
|---|---|---|
| Implementation | TypeScript app on a vendored Node runtime, plus a native Rust parsing kernel (tree-sitter grammars compiled in; per-file fallback to the portable wasm engine). GitHub's language detector reports "C" (grammar sources). | `docs/README.md:259-261`, `docs/README.md:515`, `docs/BUNDLING.md:1-30`; `gh api repos/colbymchenry/codegraph` → `"language":"C"` |
| Storage | One SQLite DB per project, `.codegraph/codegraph.db`, Node built-in `node:sqlite`, WAL + FTS5 | `docs/README.md:517`, `docs/BUNDLING.md:3-6` |
| Distribution channels | (1) `install.sh` (curl \| sh) pulls a release tarball, (2) npm `@colbymchenry/codegraph` (thin shim + per-platform `optionalDependencies`), (3) `install.ps1` on Windows. Homebrew/Scoop: not yet available (listed as planned upstream). No cargo crate. | `docs/BUNDLING.md:52-70`; `npm view @colbymchenry/codegraph optionalDependencies` |
| Platforms | linux-x64, linux-arm64, darwin-x64, darwin-arm64, win32-x64, win32-arm64. Each release ships the 6 archives plus `SHA256SUMS`. | `gh api repos/colbymchenry/codegraph/releases` (asset lists v1.3.0 … v1.6.2); `docs/README.md:781-790`; `docs/install.sh:44-49` |
| Bundle contents | `node` (official Node runtime, 123,438,592 bytes), `lib/dist`, `lib/node_modules`, `bin/codegraph` launcher. No native addons. Needs no system Node. | `docs/BUNDLING.md:16-30`; hands-on `ls` in §5 |
| Latest release | **v1.6.2**, published 2026-10-03T06:41:20Z (npm `latest` dist-tag = 1.6.2). 30 GitHub releases total; 8 releases between 2026-07-07 (v1.3.0) and 2026-10-03. | `gh api .../releases/latest`, `npm view @colbymchenry/codegraph dist-tags` |
| Version pinning | `CODEGRAPH_VERSION=v1.6.2` for `install.sh`; `npm i -g @colbymchenry/codegraph@1.6.2`; `codegraph upgrade <version>`; or a direct download of `https://github.com/colbymchenry/codegraph/releases/download/v1.6.2/codegraph-linux-x64.tar.gz` | `docs/install.sh:15,58-72`; `docs/README.md:96` |
| Checksums | `SHA256SUMS` asset per release. **`install.sh` does NOT verify it** (it only `curl`s and `tar -xzf`s). Verification must be done by the caller. | `docs/install.sh:71-82` (no checksum step); hands-on `sha256sum -c` in §5 |
| Signatures / provenance | Release bundles and `SHA256SUMS` carry GitHub build attestations (SLSA v1.0 Build L2), verifiable with `gh attestation verify <file> -R colbymchenry/codegraph`; npm packages published with trusted publishing + provenance (`npm audit signatures`). Releases before July 2026 have no attestations. No macOS/Windows code signing yet. | `docs/README.md:754-779`; `docs/BUNDLING.md:72-80`; hands-on attestation verify in §5 |
| License | MIT | `docs/package.json:43`; `gh api` `license.spdx_id=MIT` |
| Maintenance | Created 2026-01-18; last push 2026-10-29T15:51Z; ≥100 commits since 2026-09-29 (API page cap hit); 75,850 stars, 5,011 forks, 481 open issues; top contributor colbymchenry (1,535 commits), next three 11-18 commits each (effectively a single-maintainer project). Not archived. | `gh api repos/colbymchenry/codegraph`, `.../commits?since=2026-09-29`, `.../contributors` |
| Telemetry | Anonymous usage telemetry, **default on** (installer asks with a visible default-on choice); sends to `telemetry.getcodegraph.com`. Off switches: `codegraph telemetry off`, `CODEGRAPH_TELEMETRY=0`, `DO_NOT_TRACK=1`. A separate update check is disabled by `CODEGRAPH_NO_UPDATE_CHECK=1`. | `docs/TELEMETRY.md:10-41,101`; `docs/README.md:737-752` |
| Node engine (npm path / library only) | `node >=20.0.0 <25.0.0`; CLI and MCP run on the bundled runtime regardless | `docs/package.json:65-67`; `docs/README.md:633-636` |

## 2. Install mechanics

Installing has two separate steps upstream: (a) put the CLI on PATH, (b) `codegraph install` wires agents. Neither indexes code; `codegraph init` per project does (`docs/README.md:75-117`, `docs/README.md:399`).

**(a) CLI install commands**

```bash
# Release bundle (no Node needed); pin with CODEGRAPH_VERSION
CODEGRAPH_VERSION=v1.6.2 sh -c "$(curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh)"
# npm (shim + per-platform optional dependency)
npm i -g @colbymchenry/codegraph@1.6.2
```

What `install.sh` writes (`docs/install.sh:15-22,78-90,101-116`, confirmed hands-on in §5):

| Path | Content |
|---|---|
| `$CODEGRAPH_INSTALL_DIR` (default `~/.codegraph`) `/versions/<tag>/` | extracted bundle (286 MB on disk for v1.6.2 linux-x64) |
| `~/.codegraph/current` | symlink to the active version dir |
| `$CODEGRAPH_BIN_DIR` (default `~/.local/bin`) `/codegraph` | symlink to `versions/<tag>/bin/codegraph` |
| older `~/.codegraph/versions/*` | deleted (prune step) |

It does not touch any agent config, PATH files, hooks or CLAUDE.md. Uninstall: `install.sh --uninstall` removes the bundle dir and the symlink (`docs/install.sh:24-29`).

**Global state created at runtime (hands-on, §5):** `~/.codegraph/daemons/` (daemon registry, created by the first MCP serve), `~/.codegraph/telemetry.json` (telemetry choice and machine ID; path printed by `codegraph telemetry status`).

**Per-project state:** `<project>/.codegraph/` with `codegraph.db` (+ `-wal`, `-shm`), `daemon.sock`, `daemon.pid`, `writer.pid`, `daemon.log`, and a self-ignoring `.gitignore` (`*` / `!.gitignore`), so only `.codegraph/.gitignore` shows as untracked in git. Optional committed config: `codegraph.json` (`exclude`, `include`, `deprioritize`, `extensions`) at the project root (`docs/README.md:669-735`).

**(b) `codegraph install` — its own agent installer (yes, it edits Claude config).** For target `claude` it writes (`docs/src/installer/targets/claude.ts:1-20,125-172`, confirmed hands-on in §5 against the sandbox HOME):

| Location `global` (the `--yes` default) | Location `local` |
|---|---|
| `~/.claude.json` → `mcpServers.codegraph = {"type":"stdio","command":"codegraph","args":["serve","--mcp"],"alwaysLoad":true}` (merged, other servers kept) | `./.mcp.json` (project scope) |
| `~/.claude/settings.json` → `permissions.allow += "mcp__codegraph__*"` (unless `--no-permissions`) | `./.claude/settings.json` |
| `~/.claude/settings.json` → `hooks.UserPromptSubmit += {"type":"command","command":"codegraph prompt-hook"}` (opt-in prompt, default yes; written by `--yes`) | same, local |
| `~/.claude/CLAUDE.md` → marker-fenced block `<!-- CODEGRAPH_START --> … <!-- CODEGRAPH_END -->` (text in `docs/src/installer/instructions-template.ts:41-50`) | `./.claude/CLAUDE.md` |

`CLAUDE_CONFIG_DIR` relocates all three global files (`claude.ts:13-14`). It also strips legacy pre-0.8 `codegraph mark-dirty`/`sync-if-dirty` hooks (`claude.ts:144-153`). No skills, agents or commands are written. `codegraph uninstall` reverses it and also removes the CLI (`--keep-cli` keeps it) (`docs/README.md:129-139`). `codegraph upgrade` runs `codegraph install --refresh`, which rewrites what earlier installs configured (`codegraph install --help`, §5).

**Interaction with IronClaude (verified in this repo):** `superclaude install --force` (run by `./update.sh:7-8`) copies every core `.md`, including `CLAUDE.md`, over `~/.claude/` (`src/superclaude/cli/install_core.py:13-24,62-71`). Any CodeGraph block that `codegraph install` writes into `~/.claude/CLAUDE.md` is therefore erased on the next `./update.sh`. The guidance must live in `src/superclaude/core/CLAUDE.md` itself if IronClaude wants it.

## 3. MCP integration

- **Transport/scope:** stdio; command `codegraph serve --mcp`. User scope = `~/.claude.json`, project scope = `./.mcp.json` (`claude.ts:75-85`; `docs/src/installer/targets/shared.ts:24-28`).
- **Exact registration without `codegraph install`** (keeps `alwaysLoad`, matching how IronClaude already registers codebase-memory with `claude mcp add-json … --scope user`, `src/superclaude/cli/install_mcp.py:775-786`):

  ```bash
  claude mcp add-json codegraph '{"type":"stdio","command":"codegraph","args":["serve","--mcp"],"alwaysLoad":true}' --scope user
  ```

  Plain form (loses `alwaysLoad`, so Claude Code defers the tool behind tool search, `docs/README.md:459`): `claude mcp add --scope user codegraph -- codegraph serve --mcp`. Env overrides go in the JSON `env` object (for example `"env":{"CODEGRAPH_TELEMETRY":"0"}`). Neither command was run against the real environment (planning-run rule); `add-json` argv shape confirmed from `claude mcp add-json --help` and the existing IronClaude call.
- **Permission rule:** `mcp__codegraph__*` (`shared.ts:43-48`).
- **Server instructions:** delivered in the MCP `initialize` result (`docs/src/mcp/server-instructions.ts`; live text captured in §5). Subagents do not see them, which is why upstream also writes the CLAUDE.md block (`instructions-template.ts:1-25`).

**MCP tools (quoted from `docs/src/mcp/tools.ts:1683-1895`; matches live `tools/list` in §5).** Every tool is read-only (`readOnlyHint: true`, `tools.ts:1667-1672`) and accepts optional `projectPath` (absolute path; nearest `.codegraph/` at or above it).

| Tool | Listed by default | Parameters (required in bold) |
|---|---|---|
| `codegraph_explore` | **yes (only one)**; `_meta.anthropic/alwaysLoad: true` | **`query`** (string), `maxFiles` (1-20), `projectPath` |
| `codegraph_search` | no | **`query`**, `kind` (function\|method\|class\|interface\|type\|variable\|route\|component), `limit` (default 10), `projectPath` |
| `codegraph_callers` | no | **`symbol`**, `file`, `limit` (default 20, max 100), `projectPath` |
| `codegraph_callees` | no | **`symbol`**, `file`, `limit` (default 20), `projectPath` |
| `codegraph_impact` | no | **`symbol`**, `file`, `depth` (default 2), `projectPath` |
| `codegraph_node` | no | `symbol`, `includeCode`, `file`, `offset`, `limit`, `symbolsOnly`, `line`, `projectPath` (file mode = Read-equivalent with line numbers) |
| `codegraph_status` | no | `projectPath` |
| `codegraph_files` | no | `path`, `pattern` (glob), `format` (tree\|flat\|grouped), `includeMetadata`, `maxDepth`, `projectPath` |

The default list is `DEFAULT_MCP_TOOLS = new Set(['explore'])` (`tools.ts:1953`); `CODEGRAPH_MCP_TOOLS=explore,node,search,callers,…` re-lists others (`tools.ts:1933-1940`). Hands-on finding: unlisted tools still answer `tools/call` when not listed (the default-mode run returned callers output, §5.6); only an explicit `CODEGRAPH_MCP_TOOLS` allowlist blocks them (`tools.ts:2926-2929`).

**CLI subcommands (live `codegraph help`, v1.6.2):** `init [--yes] [path]`, `uninit`, `index [--force --quiet]`, `sync`, `status`, `query <search> [--kind --limit --json]`, `explore <query…>`, `context <task…>`, `node [name]`, `files`, `daemon|daemons`, `unlock`, `callers <symbol>`, `callees <symbol>`, `impact <symbol> [--depth]`, `affected [files…] [--stdin --depth --filter --json --quiet]`, `install`, `uninstall`, `telemetry [status|on|off]`, `upgrade [version] [--check --force]`, `version`, `help`, plus `serve --mcp` and `prompt-hook` (used by the MCP config and the hook; not listed in `help`).

## 4. Indexing lifecycle

- **First index:** `codegraph init [--yes]` creates `.codegraph/` and builds the full graph in one step (`docs/README.md:110-117`). `codegraph index --force` rebuilds from scratch. Respects `.gitignore`, skips dependency/build dirs and files over 1 MB (`docs/README.md:648-665`).
- **Incremental sync:** while an MCP client is connected, a shared per-project background **daemon** (one writer per project, `.codegraph/daemon.sock`) runs a native inotify/FSEvents watcher with a 2000 ms debounce (`CODEGRAPH_WATCH_DEBOUNCE_MS`), plus a staleness banner for pending files and a connect-time `(size, mtime)` + hash catch-up for edits made while no server ran (`docs/README.md:286-311`). Daemon idle timeout observed: 300000 ms (`daemon.log`, §5.7). Manual `codegraph sync` is for scripts or `CODEGRAPH_NO_DAEMON=1` setups. `CODEGRAPH_NO_WATCH=1` disables the watcher.
- **Git hooks:** none installed by `init` (hands-on: `.git/hooks` had only samples). Upstream only offers git hooks as the fallback on WSL2 `/mnt/*` drives (`docs/CHANGELOG.md:1606`). Upstream example of a CI/hook use: `git diff --name-only | codegraph affected --stdin` (`docs/README.md:570-578`).
- **Index location is per working tree.** Nested worktrees (for example `.claude/worktrees/` or this repo's `.dev/worktrees/`) are skipped by the parent's indexer (`docs/CHANGELOG.md:1290`) and, until they have their own `init`, are answered from the parent index **with a warning** that results come from a different working tree (`docs/CHANGELOG.md:1517`, hands-on §5.8). Sibling worktrees (the IronClaude layout `~/workspaces/worktrees/<repo>/<branch>`) are simply "not initialized" until `codegraph init` runs there. The MCP server re-checks per call, so a worktree's new index is picked up without restart (`docs/CHANGELOG.md:1272`).
- **What must happen on clone / new worktree:** run `codegraph init --yes` in the new checkout (about 4.5 s and 34 MB for the 500-file sample; upstream quotes ~100 s for 27k files and <12 min for the Linux kernel on 2 cores, `docs/README.md:263-267`). Nothing upstream does this automatically; a Coder template hook, a git `post-checkout` hook, or a Claude `SessionStart` hook would have to (research handed to the Coder agent per the orchestration README).
- **Cost:** per-project DB about 70 KB per indexed file in this sample (34.7 MB / 500 files); peak RSS during `init` about 1 GB for the process tree (§5.4). Upstream warns the WAL can grow to 256 MB-2 GB during very large builds (`docs/README.md:901`).

## 5. Hands-on validation (sandbox)

**Result: install, index, CLI queries, MCP stdio (`initialize`, `tools/list`, 3 `tools/call`), watcher auto-sync, worktree behaviour and `codegraph install` all worked. No blocking error.**

Sandbox: `/tmp/codegraph-eval.fQfO` (mode 700, left in place). Every codegraph command ran with `HOME=/tmp/codegraph-eval.fQfO/home`, `CODEGRAPH_INSTALL_DIR=$HOME/.codegraph`, `CODEGRAPH_BIN_DIR=$HOME/.local/bin`, `PATH=$HOME/.local/bin:$PATH`, `CODEGRAPH_TELEMETRY=0`, `DO_NOT_TRACK=1`. Real `~/.codegraph` does not exist and `codegraph` is not on the real PATH (checked after the run). Host: Linux x86_64, 87 GB RAM. `/usr/bin/time` and `bc` are not installed, so timings use `date +%s%N` and memory uses a `/proc/<pid>/status` VmRSS sampler.

### 5.1 Download and verify (pinned v1.6.2)

```text
$ gh release download v1.6.2 -R colbymchenry/codegraph -p SHA256SUMS -p codegraph-linux-x64.tar.gz -D dl
real 0m0.814s           # 63,433,974-byte tarball
$ (cd dl && sha256sum -c --ignore-missing SHA256SUMS)
codegraph-linux-x64.tar.gz: OK
# SHA256SUMS line: ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828  codegraph-linux-x64.tar.gz
$ HOME=$S/home GH_TOKEN=<token> gh attestation verify dl/codegraph-linux-x64.tar.gz -R colbymchenry/codegraph --format json | jq '.[0].verificationResult.signature.certificate'
{ "sourceRepositoryRef": "refs/heads/main",
  "buildSignerURI": "https://github.com/colbymchenry/codegraph/.github/workflows/release.yml@refs/heads/main",
  "sourceRepositoryDigest": "0f0af7bf22a5083a47e34fcb1e1bf67355174ef8" }      # exit 0
```

Note: `gh attestation verify` needs GitHub auth (`gh auth login` or `GH_TOKEN`); with only the sandbox HOME it failed with "To get started with GitHub CLI, please run: gh auth login" until `GH_TOKEN` was passed. It also writes a sigstore cache under `$HOME/.cache/gh/.sigstore`.

### 5.2 Install

```text
$ CODEGRAPH_VERSION=v1.6.2 sh docs/install.sh        # upstream install.sh, copy fetched via gh api
Installing CodeGraph v1.6.2 (linux-x64)...
Installed to /tmp/codegraph-eval.fQfO/home/.codegraph/versions/v1.6.2
Linked     /tmp/codegraph-eval.fQfO/home/.local/bin/codegraph
Done. Run: codegraph --help
real 0m2.893s   exit=0
$ du -sh $HOME/.codegraph        -> 286M
$ codegraph --version            -> 1.6.2
```

`install.sh` re-downloaded the tarball itself and did not check `SHA256SUMS` (§1).

### 5.3 Project

`cp -r` (no links) of `src/superclaude/cli/` and `tests/cli/` from this worktree into `$S/project/src/superclaude/cli` and `$S/project/tests/cli`, `__pycache__` removed, `git init` + one commit: 534 files, 440 `.py`, 159,798 Python lines.

### 5.4 Index

```text
$ codegraph init --yes
◆  Initialized in /tmp/codegraph-eval.fQfO/project
Scanning files... Parsing code... Resolving refs... Linking dynamic dispatch...
◆  Indexed 500 files
●  9,924 nodes, 23,946 edges in 720ms
exit=0   peak_rss_tree=1057MB (VmRSS sampled every 0.2 s over the process tree)
$ codegraph index --force --quiet          wall_ms=4329   (full rebuild, end to end)
$ codegraph status
  Files: 500  Nodes: 9,924  Edges: 23,946  DB Size: 33.13 MB
  Backend: node:sqlite — built-in (full WAL)   Journal: wal
  Nodes by Kind: function 3,681 · import 2,388 · method 1,567 · variable 1,166 · class 671 · file 451
  Files by Language: python 440 · yaml 49 · liquid 11
✓ Index is up to date
$ du -sh .codegraph  -> 34M ;  git status --short -> ?? .codegraph/   (only .codegraph/.gitignore is visible)
```

The first `init` wall time was lost (the `bc` call failed); the engine-reported 720 ms excludes process start. The two later end-to-end runs took 4.3 s (`index --force`) and 4.6 s (`init` in a worktree, §5.8). No files were written under `$HOME` by `init`; no git hooks were added.

### 5.5 CLI queries (the two required queries)

Definition of `install_codebase_memory_mcp`:

```text
$ codegraph query install_codebase_memory_mcp          [wall_ms=290]
function    install_codebase_memory_mcp
  src/superclaude/cli/install_mcp.py:815
  ( *, scope: str = "user", dry_run: bool = False ) -> tuple[bool, str]
variable    _NATIVE_INSTALLER
  tests/cli/test_update_command.py:28
  = "superclaude.cli.install_mcp.install_codebase_memory_mcp"
$ codegraph query install_codebase_memory_mcp --json --limit 3   # startLine 815, endLine 913, docstring
  "Shared native install/register boundary for framework and MCP callers."
```

Callers:

```text
$ codegraph callers install_codebase_memory_mcp        [wall_ms=297]
Callers of "install_codebase_memory_mcp" (20 of 23):
function install_codebase_memory_mcp (python) — src/superclaude/cli/install_mcp.py:815
  install_mcp_server   src/superclaude/cli/install_mcp.py:1010
  install              src/superclaude/cli/main.py:46
  test_native_dry_run_never_acquires_or_mutates   tests/cli/test_install_mcp_tavily.py:824
  … 17 more test_native_* functions in tests/cli/test_install_mcp_tavily.py …
Showing 20 of 23; pass --limit to widen.
$ codegraph callees install_codebase_memory_mcp   (9): _native_registration_matches, _restore_user_native_entry,
  _run_registration_command, acquire_codebase_memory (install_codebase_memory.py:611), _run_command,
  _native_lifecycle_notice, _native_selection_error, _add_user_native_entry, read_user_mcp_entry
```

Cross-check with ripgrep on the same copy: the real call sites are `main.py:255` (inside `install`, defined at `main.py:46`) and `install_mcp.py:1026` (inside `install_mcp_server`, defined at `install_mcp.py:1010`); `def` at `install_mcp.py:815`. Both production callers were found. **Gap:** codegraph reports the caller's definition line, not the call-site line (`main.py:46`, not `:255`).

### 5.6 MCP server over stdio

Client: `/tmp/codegraph-eval.fQfO/scripts/mcp-client.mjs` (spawns `codegraph serve --mcp` in the project, newline-delimited JSON-RPC: `initialize` → `notifications/initialized` → `tools/list` → `tools/call` × 3). Raw responses: `/tmp/codegraph-eval.fQfO/mcp-default.json`, `/tmp/codegraph-eval.fQfO/mcp-all.json`.

```text
=== default env
server={"name":"codegraph","version":"1.6.2"} proto=2024-11-05 init_ms=220
tools: codegraph_explore
explore_ms=771 callers_ms=15 node_ms=4      total_ms=1015
=== CODEGRAPH_MCP_TOOLS=explore,node,search,callers,callees,impact,files,status
tools: codegraph_search,codegraph_callers,codegraph_callees,codegraph_impact,codegraph_node,codegraph_explore,codegraph_status,codegraph_files
explore_ms=253 callers_ms=3 node_ms=3       total_ms=468
```

`codegraph_callers {"symbol":"install_codebase_memory_mcp","limit":5}` returned "**Callers of install_codebase_memory_mcp (5 found)** … > Showing 5 of 23 callers" in both runs (so an unlisted tool still answers `tools/call`). `codegraph_explore {"query":"install_codebase_memory_mcp callers"}` returned 24,913 characters: "Found 60 symbols across 6 files", a blast-radius list ("`install_codebase_memory_mcp` (src/superclaude/cli/install_mcp.py:815) — 23 callers in `install_mcp.py`, `main.py`; tests: …"), a relationships list and verbatim source. It also pulled in two unrelated `install` functions (`eval/signal_handler.py:195`, `cleanup_audit/process.py:57`) because the query words matched them. `initialize.result.instructions` starts "# Codegraph — code intelligence over an indexed knowledge graph". stderr was empty.

### 5.7 Daemon and incremental sync

The first `serve --mcp` started a background daemon that **outlived the client**: `daemon.log` → "Listening on …/.codegraph/daemon.sock (pid 2942614, v1.6.2). Idle timeout 300000ms." / "File watcher active … graph will auto-sync on changes" / "Query pool: up to 16 worker thread(s)". It also created `$HOME/.codegraph/daemons/`.

- Watcher: appended `def cg_eval_probe_fn()` to `install_mcp.py`, waited 4 s, `codegraph query cg_eval_probe_fn` → found at `install_mcp.py:1376`; `status` → "✓ Index is up to date".
- Manual `codegraph sync` while the daemon held the writer lock printed: "✗ Failed to sync: Sync could not acquire the file lock; retry when the index is available. CodeGraph database is locked by another process (PID 2942614)." (wall 323 ms). The daemon's watcher indexed that edit anyway. A later `codegraph sync` with nothing pending exited 0. **Implication:** scripts must not rely on `codegraph sync` succeeding while an agent session is open; the exit status of the failing run was not captured.

### 5.8 Git worktrees

```text
$ git worktree add $S/wt-sibling -b feat-sibling ; git worktree add .dev/worktrees/nested -b feat-nested
[sibling, no init] codegraph status → "⚠ Not initialized … Run "codegraph init""; query → "✗ CodeGraph not initialized"
[nested, no init]  codegraph status → "⚠ This CodeGraph index belongs to a different git working tree.
   Running in: …/project/.dev/worktrees/nested   Index from: /tmp/codegraph-eval.fQfO/project
   … Run "codegraph init -i" in this worktree for a worktree-local index."
[main index] codegraph files --format flat | grep -c .dev/worktrees → 0   (nested worktree not double-indexed)
[sibling] codegraph init --yes → Indexed 500 files, 9,926 nodes, 23,949 edges; wall_ms=4572; .codegraph 34M
```

### 5.9 `codegraph install` against the sandbox HOME

Pre-seeded `$HOME/.claude.json` with an `other` server. `codegraph install --target=claude --location=global --yes` (exit 0) printed "Updated ~/.claude.json", "Created ~/.claude/settings.json", "Updated ~/.claude/settings.json", "Created ~/.claude/CLAUDE.md". Resulting files: `.claude.json` kept `other` and added `codegraph` (`stdio`, `codegraph serve --mcp`, `alwaysLoad: true`); `settings.json` = `permissions.allow: ["mcp__codegraph__*"]` + `hooks.UserPromptSubmit: [{hooks:[{type:"command",command:"codegraph prompt-hook"}]}]`; `CLAUDE.md` = the marker-fenced block. `codegraph install --print-config claude` prints the same JSON with no writes.

`prompt-hook` probe: piping `{"prompt":"how does install_codebase_memory_mcp register the server","cwd":…}` into `codegraph prompt-hook` printed a `<codegraph_context …>` block (an explore result, "Found 41 symbols across 4 files") on stdout, exit 0. As a `UserPromptSubmit` hook this injects an explore payload into every prompt in an indexed repo, a context cost (compare the README's own note that CodeGraph leaves ~80% more retrieval context resident, `docs/README.md:198`).

### 5.10 Left running / left behind

A daemon (pid 2942614) may still be running until its 300 s idle timeout; everything is under `/tmp/codegraph-eval.fQfO`. Outside the sandbox, only this file and the decision files under `.dev/codegraph-migration/decisions/W4-install-strategy/` (required by the orchestration README's decision rule) were written.

## 6. Gaps versus codebase-memory-mcp and Serena

Sources: codegraph tools from `docs/src/mcp/tools.ts:1683-1895` and the live `tools/list` (§5.6); CLI from live `codegraph help`. codebase-memory and Serena tool names are quoted from the MCP tool schemas loaded in this worker session (`mcp__codebase-memory-mcp__*`, `mcp__serena__*`); those tools were not called. Key structural fact: **every codegraph tool is read-only** (`tools.ts:1656-1672`), and indexing is CLI-only by design.

### 6.1 codebase-memory-mcp

| codebase-memory tool | codegraph equivalent | Fit |
|---|---|---|
| `search_graph` (BM25 / regex name+qn / semantic_query / degree filters) | `codegraph_search` (name or partial name, `kind`, `limit`) / `codegraph query --json` | Partial: no regex, no semantic query, no degree filters |
| `trace_path` mode `calls` (inbound/outbound, depth) | `codegraph_callers`, `codegraph_callees` (one hop), `codegraph_impact` (`depth`, inbound) | Partial: multi-hop outbound only via `explore`; caller rows give definition line, not call-site line (§5.5) |
| `trace_path` modes `data_flow`, `cross_service`, `topology`, `deploy`, `run` | none | No equivalent |
| `get_code_snippet` | `codegraph_node {symbol, includeCode:true}` (returns every overload when ambiguous; `file`/`line` to pin) | Equivalent |
| `query_graph` (read-only Cypher) | none over MCP. The SQLite file `.codegraph/codegraph.db` can be queried directly (schema in upstream `src/db/schema.sql`, not inspected: UNVERIFIED) | No equivalent |
| `get_architecture` (languages, packages, entry points, routes, hotspots, layers, clusters, cycles) | `codegraph_files` (tree + language + symbol counts), `codegraph status` (node kinds, languages), `codegraph_search {kind:"route"}`, `codegraph_explore` for an area | Partial: no layers, clusters, hotspots or cycles |
| `detect_changes` (git diff → files → impacted symbols/tests) | `git diff --name-only \| codegraph affected --stdin` (affected test files), `codegraph_impact` per symbol | Partial: test-file impact only; no diff-to-symbol mapping |
| `search_code` (text search) | none (FTS5 covers symbol names, `docs/README.md:278`) | No equivalent: use Grep/rg |
| `index_status` | `codegraph_status` / `codegraph status` (pending-sync section) | Equivalent |
| `index_repository` | `codegraph init` / `codegraph index` (CLI only) | CLI only, by design |
| `list_projects` | none (`codegraph daemon` lists running daemons only) | No equivalent |
| `delete_project` | `codegraph uninit [--force]` | Equivalent (CLI) |
| `check_index_coverage` | `codegraph status` pending list, staleness banner in tool output | Partial |
| `get_file_outline` | `codegraph_node {file, symbolsOnly:true}` | Equivalent |
| `get_graph_schema`, `compare_graphs`, `ingest_traces`, `manage_adr` | none | No equivalent |
| (no codebase-memory equivalent) | `codegraph_explore` (source + call paths + blast radius in one call), `codegraph_node` file mode (Read replacement), `prompt-hook` | codegraph-only |

### 6.2 Serena

| Serena capability | codegraph equivalent | Fit |
|---|---|---|
| `find_symbol` (name path, depth for children, include_body) | `codegraph_search` + `codegraph_node {includeCode}`; children via `codegraph_node {file, symbolsOnly}` | Partial: no name-path (`Class/method`) addressing |
| `find_referencing_symbols` | `codegraph_callers` (+ `references` edges shown inside `explore`) | Partial: callers are call edges; no per-reference snippet |
| `get_symbols_overview` | `codegraph_node {file, symbolsOnly:true}` | Equivalent |
| `find_declaration` | `codegraph_node {symbol}` | Equivalent for named symbols |
| `find_implementations` | `codegraph_explore` surfaces interface→impl dispatch (`docs/README.md:588`) | Partial: no direct tool |
| `get_diagnostics_for_file` (LSP) | none (no language server) | No equivalent |
| Symbol edits: `replace_symbol_body`, `insert_after_symbol`, `insert_before_symbol`, `rename_symbol`, `safe_delete_symbol`, `replace_content`, `replace_in_files` | none (all codegraph tools are read-only). Use Claude Code Edit/Write; use `codegraph_impact`/`callers` to find sites before a rename or delete | No equivalent |
| Memories: `write_memory`, `read_memory`, `list_memories`, `edit_memory`, `rename_memory`, `delete_memory` | none | No equivalent: needs a replacement store (Claude memory files or `.dev/` docs) |
| `onboarding`, `initial_instructions` | MCP `initialize` instructions (`server-instructions.ts`), CLAUDE.md block | Rough equivalent |

**Biggest gaps for Phase 3:** Cypher `query_graph`, `detect_changes` symbol mapping, `search_code`, data-flow/cross-service tracing, LSP diagnostics, symbol-aware edits/rename, and memories. The first four have workable non-MCP substitutes (rg, `codegraph affected`, direct SQLite); edits and memories need different tools entirely.

## 7. Recommended install strategy

Adopted from `/sc:adversarial --depth quick` (merged result `.dev/codegraph-migration/decisions/W4-install-strategy/adversarial/W4-install-strategy-merged.md`; options `option-a.md`, `option-b.md`, `option-c.md` in the same folder; convergence 22/22, base scores C 0.879, A 0.808, B 0.752). **Recommendation: Coder image bakes a verified copy (Option C shape) plus an IronClaude-owned verified download fallback (Option A mechanics); never use upstream `install.sh` or `codegraph install`.**

**One pin, in IronClaude.** IronClaude source holds the version (`v1.6.2` today) and a 4-entry SHA-256 table (linux-x64, linux-arm64, darwin-x64, darwin-arm64; linux-x64 = `ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828`, from `SHA256SUMS`, §5.1). The Coder image copies these values.

**Coder image (bake, as an optimization).** `Dockerfile.coder` downloads `codegraph-linux-<arch>.tar.gz` for the pin, checks the SHA-256 at build time, extracts to `/opt/codegraph/<tag>/`, links `/usr/local/bin/codegraph`, and sets `CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_UPDATE_CHECK=1` in the image env. Same pattern as today's baked `/usr/local/bin/codebase-memory-mcp`. A stale or missing bake is not fatal (the fallback repairs it).

**`superclaude install` codegraph phase (replaces `src/superclaude/cli/main.py:253-262`), in order:**

1. Claude CLI readiness guard (the caller-side check `install_codebase_memory.py:614` already requires).
2. Exact version gate over candidates: `/usr/local/bin/codegraph` (or the PATH winner), then `~/.local/bin/codegraph`; first whose `codegraph --version` equals the pin wins.
3. Fallback only if no candidate passes: download the pinned tarball, verify against the source-pinned hash, extract to `~/.codegraph/versions/<tag>/`, link `~/.local/bin/codegraph` and `~/.codegraph/current` (upstream's own layout). On Coder, warn that the image is stale.
4. Install into a new version dir and flip the symlink; keep the previous dir until the next run (a running daemon may hold it for up to 300 s, §5.7).
5. Register the winner's absolute realpath:
   `claude mcp add-json codegraph '{"type":"stdio","command":"<abs path>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1"}}' --scope user`
6. Guidance in `src/superclaude/core/CLAUDE.md`; `mcp__codegraph__*` permission via IronClaude's own settings handling.
7. Receipt and removal for the user copy only (reuse the `install_codebase_memory.py` pattern).

**`./update.sh`:** unchanged script; `superclaude install --force` re-runs the phase, so a pin bump is picked up on every update. `superclaude doctor` should flag a version that differs from the pin, a `CODEGRAPH_START` block in `~/.claude/CLAUDE.md`, or a `codegraph prompt-hook` hook.

**Verification:** SHA-256 against the source-pinned table (blocking); `codegraph --version` equals the pin (blocking); `gh attestation verify` optional and non-blocking (needs GitHub auth, §5.1); a test-time drift check comparing IronClaude's MCP entry with a recorded `codegraph install --print-config claude` fixture.

**Not done:** no `install.sh` (no checksum step, `docs/install.sh:71-82`), no `codegraph install` (its `~/.claude/CLAUDE.md` block is erased by `install_core.py:62-71` and it adds the prompt hook), no prompt hook, no `codegraph upgrade`.

**Open follow-ups the debate attached:** per-worktree `codegraph init` has no owner yet (§4; handed to the Coder research per the orchestration README); new client against an older running daemon is untested; 4 hashes per release at ~8 releases per quarter; single-maintainer upstream; image grows ~286 MB.

## Decisions

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| Evaluate main project, not the fork | colbymchenry/codegraph; sunerpy/codegraph-rust | self | Main project has linux x64/arm64 bundles, checksums, attestations, MIT, very active; the brief allows the fork only if the main one is unsuitable (§1). |
| Pin v1.6.2 for the hands-on test | latest; v1.6.2 | self | v1.6.2 is the current latest release and npm `latest`; pinning makes results reproducible (§1). |
| Verify with `sha256sum` + `gh attestation verify` before running upstream `install.sh` | trust install.sh; verify separately | self | `install.sh` has no checksum step (`docs/install.sh:71-82`). |
| Pass `GH_TOKEN` to `gh attestation verify` under the sandbox HOME | real HOME; sandbox HOME with token | self | Keeps the real HOME untouched; the token was read with `gh auth token` (read-only). |
| Run `codegraph install` only against the sandbox HOME | skip; run in sandbox | self | Needed to see exactly what it writes; the sandbox HOME isolates it (§5.9). |
| Install strategy for IronClaude and the Coder image | A: IronClaude-verified download; B: upstream install.sh + `codegraph install`; C: bake in image, IronClaude registers | adversarial quick | Adopted merged C+A (§7): integrity on every path, IronClaude stays the only writer of Claude config, one pin with exact gate and absolute-path registration. |
| Registration form | `claude mcp add` (plain); `claude mcp add-json` with `alwaysLoad` | self | `add-json` keeps `alwaysLoad` (otherwise the tool is deferred, `docs/README.md:459`) and matches IronClaude's existing call (`install_mcp.py:775-786`). |
| Telemetry and update check | leave default (on); disable | self | Default-on telemetry to a third-party endpoint (`docs/TELEMETRY.md:24,101`); disabled via env in the MCP entry and image. |
