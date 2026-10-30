# Coder handoff context: facts behind the prompt

Companion to `coder-handoff-prompt.md`. Written 2026-10-29 by the IronClaude planning run for issue https://github.com/IronbellyOrg/IronClaude/issues/323. Every fact cites where it was observed. Coder paths were read at Coder commit `e25f787ccaef04312f64347714a7791221564219` (`main` on 2026-10-29) and may have moved: re-check each one on current `main`. `T/` means `templates/VSCode-AIDev02/`.

## 1. codegraph facts

Project: https://github.com/colbymchenry/codegraph, MIT, single main maintainer, very active (30 releases, 8 between 2026-07-07 and 2026-10-03). Pinned version for this migration: **v1.6.2** (released 2026-10-03; npm `latest` = 1.6.2).

| Fact | Value | Where observed |
|---|---|---|
| What it is | Standalone bundle: official Node runtime + app + native tree-sitter kernel. Needs no system Node. | upstream `BUNDLING.md:16-30` |
| Release assets | `codegraph-linux-x64.tar.gz`, `codegraph-linux-arm64.tar.gz`, `codegraph-darwin-x64.tar.gz`, `codegraph-darwin-arm64.tar.gz`, two Windows zips, and `SHA256SUMS`, at `https://github.com/colbymchenry/codegraph/releases/download/v1.6.2/<asset>` | `gh api repos/colbymchenry/codegraph/releases` |
| SHA-256 linux-x64 | `ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828` (tarball 63,433,974 bytes) | v1.6.2 `SHA256SUMS`; `sha256sum -c` OK in a sandbox |
| SHA-256 linux-arm64 | `c8c6be292be21d00dea26bad8b28d434731cf612fb8cc475dc10f5b3038b5b64` | v1.6.2 `SHA256SUMS` |
| Provenance | Assets carry GitHub build attestations (SLSA L2): `gh attestation verify <file> -R colbymchenry/codegraph` (needs `gh` auth). | upstream `README.md:754-779`; verified in sandbox |
| Upstream `install.sh` | Downloads and extracts **without checking `SHA256SUMS`**. Do not use it. Layout it creates: `~/.codegraph/versions/<tag>/`, `~/.codegraph/current` symlink, `~/.local/bin/codegraph` symlink. | upstream `install.sh:71-82` |
| Bundle on disk | 286 MB extracted (linux-x64); entry point `bin/codegraph` inside the extracted dir | sandbox `du -sh` |
| Version check | `codegraph --version` prints exactly `1.6.2`, exit 0 | sandbox |
| Telemetry | **On by default**, sends to `telemetry.getcodegraph.com`. Off: `CODEGRAPH_TELEMETRY=0` (or `DO_NOT_TRACK=1`). Update check off: `CODEGRAPH_NO_UPDATE_CHECK=1`. | upstream `TELEMETRY.md:10-41,101`; `README.md:737-752` |
| MCP server | stdio, `codegraph serve --mcp`; 8 read-only tools (`codegraph_explore` listed by default; `search`, `callers`, `callees`, `impact`, `node`, `status`, `files` callable). `CODEGRAPH_MCP_TOOLS=<comma list>` in the server env lists exactly the named tools; IronClaude registers `node,search,callers,callees,impact,files,status`, which hides explore (that an explicit list also blocks calls to unnamed tools is source-cited only, `tools.ts:2926-2929`, and is proven by IronClaude task T2 step 0 and layer 2 step 5b) | upstream `src/mcp/tools.ts:1683-1953`; sandbox `tools/list` |
| Upstream agent installer | `codegraph install` edits `~/.claude.json`, `~/.claude/settings.json` (permission + a `UserPromptSubmit` `codegraph prompt-hook`) and adds a block to `~/.claude/CLAUDE.md`. **IronClaude does not use it**; do not run it in the image or at startup. | upstream `src/installer/targets/claude.ts:125-172`; sandbox |
| Per-project index | `codegraph init --yes [path]` creates `<checkout>/.codegraph/` (SQLite + a `.gitignore` of `*` and `!.gitignore`, so git still shows `?? .codegraph/` and `git add -A` commits that `.gitignore`; ignore `.codegraph/` globally) and indexes. About 4.5 s / 34 MB / 1 GB peak RSS for 500 files; upstream quotes ~100 s for 27k files. Re-running on an indexed checkout is a 125 ms no-op, exit 0. Refuses `$HOME` or `/` without `--force`. | sandbox; upstream `README.md:263-267` |
| Freshness | While an MCP client is connected, one daemon per project runs a file watcher (2 s debounce) and catches up edits made while no server ran. `codegraph sync` fails with a lock error while that daemon runs; `codegraph sync --quiet` is meant for git hooks. Daemon idles out after 300 s. | upstream `README.md:286-311`; sandbox `daemon.log` |
| Worktrees | Index is per working tree. A sibling worktree is "not initialized" until `codegraph init` runs in it. A nested worktree is answered from the parent's index with a warning until it has its own. | sandbox; upstream `CHANGELOG.md:1290,1517` |
| Git hooks | `codegraph init` installs none. | sandbox (`.git/hooks` had only samples) |
| Global state | `~/.codegraph/daemons/` (daemon registry), `~/.codegraph/telemetry.json` | sandbox |

## 2. IronClaude's installer contract after Phases 1 and 2

Source: `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md` §2-§3 (IronClaude repo). This is the plan; check the merged IronClaude code at the pinned SHA before relying on it (`src/superclaude/cli/install_codegraph.py`, `install_mcp.py` function `install_codegraph_mcp`, `main.py` `install`).

### 2.1 Pin and acquisition
- Pin lives only in IronClaude source: `install_codegraph.py` constants `VERSION = "1.6.2"`, `TAG = "v1.6.2"` and a SHA-256 table for `linux-x64`, `linux-arm64`, `darwin-x64`, `darwin-arm64`. A Coder bake should copy the linux values from that file at the pinned SHA (single source of truth).
- Discovery order: the `codegraph` that wins on `PATH` (for Coder: `/usr/local/bin/codegraph`), then `~/.local/bin/codegraph`. The first whose `codegraph --version` prints exactly `1.6.2` is used. No network call when one matches.
- Fallback only when none matches: download `codegraph-<os>-<arch>.tar.gz` for the tag, verify SHA-256, extract to `~/.codegraph/versions/v1.6.2/`, link `~/.local/bin/codegraph` and `~/.codegraph/current`. On Coder this means the image is stale.
- Never runs upstream `install.sh`, `codegraph install`, `codegraph upgrade` or the `codegraph prompt-hook`.

### 2.2 Registration (exact shape)

```bash
claude mcp add-json codegraph '{"type":"stdio","command":"<realpath of the chosen codegraph>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1","CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"}}' --scope user
```

The `CODEGRAPH_MCP_TOOLS` value is the constant `MCP_TOOLS` in `install_codegraph.py` (Phase 2 spec §2.4). IronClaude's task T2 sets it from a schema-cost check: the seven-tool list when the check passes, `status` when it fails. Coder contract tests should read `VERSION`, `SHA256` and `MCP_TOOLS` from that file at the pinned SHA rather than hard-coding this JSON, so a later IronClaude change to the env does not break the next pin bump. Shape check on a workspace: `jq -e '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS == "node,search,callers,callees,impact,files,status"' ~/.claude.json` (substitute the pinned `MCP_TOOLS`).

For a baked `/usr/local/bin/codegraph` symlink, `command` is the symlink's target (for example `/opt/codegraph/v1.6.2/bin/codegraph`). An equal existing entry is left alone. An "owned" entry (stdio, no `url`/`headers`, `args == ["serve","--mcp"]`, env keys only from `CODEGRAPH_TELEMETRY`, `CODEGRAPH_NO_UPDATE_CHECK`, `CODEGRAPH_MCP_TOOLS`) that differs is replaced through `claude mcp remove codegraph --scope user` then `add-json`, verified by re-reading `~/.claude.json`, and the previous entry is restored on failure. Any other ("user-managed") entry is kept: the phase passes if its command is executable and fails otherwise, printing the removal command. If Coder registers codegraph itself, use exactly this JSON so IronClaude sees it as equal. IronClaude also writes `~/.codegraph/.superclaude-bin` (one line: the realpath it registered) for its hook. Caveat: the exact stored shape of this entry is checked by IronClaude task T2 in a sandbox (`.dev/codegraph-migration/evidence/P2-add-json-shape.json` once committed); if the Claude CLI normalises a field, that file is authoritative.

### 2.3 Indexing hook IronClaude ships
- `~/.claude/hooks/codegraph-session-start.sh`, SessionStart matcher `startup`, timeout 5 s, uses the binary named in `~/.codegraph/.superclaude-bin` (else `command -v codegraph`). In a git checkout (not `$HOME` or `/`) where `<top>/.codegraph/codegraph.db` does **not** exist, it starts `codegraph init --yes <top>` detached in the background. If the database exists (in any state, built by anyone) it does nothing. A `.codegraph/` without a database (for example a committed `.codegraph/.gitignore`) still gets an `init`: the MCP server cannot build from it. No marker, PID file, lock, `status`, `index` or `sync`. Opt-out: `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (recommended for CI and headless runs).
- So IronClaude covers "first Claude session in a checkout". Coder automation is useful for what that misses: indexing before any session (fresh clone, Orca worktree creation, seed repo), and repos opened only by other tools. Any Coder-built index is simply left alone by the hook.
- Probed on v1.6.2 (IronClaude `.dev/codegraph-migration/decisions/P2-indexing-sync/probe-results.md`, rows 1-12), what any Coder automation must respect:
  - safe: two `init --yes` on one checkout, at once or 1 s apart (second is a no-op or fails cleanly; index complete); an MCP tool call during an `init` (the daemon completes the index even if the init fails); `codegraph index` while only the MCP daemon runs;
  - **destructive: `codegraph status` or `codegraph index` started while an `init` runs: the init fails and the index can be left empty (0 files).** `status` also cannot tell "still building" from "killed" (both print "never finished");
  - recovery: `init --yes` does not repair a killed init, but the MCP daemon does on its next connection (0 → full index within 50 s, 2 of 2 trials);
  - detection: a running build is `node … lib/dist/bin/codegraph.js init|index` (the `bin/codegraph` launcher execs node), so use `pgrep -f 'codegraph\.js (init|index)'`; `pgrep -f 'codegraph (init|index)'` never matches.
  So a Coder automation should start only `init --yes`, only when `.codegraph/codegraph.db` is absent, in the background, and never poll `status` while it runs.
- **Guidance gap on Coder.** IronClaude puts a codegraph usage rule into its core `CLAUDE.md` (installed to `~/.claude/CLAUDE.md`), but Coder's `ironclaude` slug restores the user's `~/.claude/CLAUDE.md` after install (`T/catalogue/ironclaude/install.sh:44-66,112-125`), so Coder users never get it. IronClaude writes the block between two marker lines, `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` and `<!-- SUPERCLAUDE_CODEGRAPH_END -->`, each alone on its line and present once. On every IronClaude pin bump, Coder copies the marked lines (inclusive) from IronClaude's `src/superclaude/core/CLAUDE.md` at the pinned SHA and replaces the same marked lines in `T/workspace_defaults/CLAUDE.md` (new workspaces) and in existing workspaces' `~/.claude/CLAUDE.md`, appending them when no marker is present (idempotent: a second run with the same SHA changes nothing). Do not append once and stop: IronClaude's Phase 3 and later releases change the block, and the MCP table row in IronClaude's core file never reaches Coder, so everything Coder users need is inside the markers. The block at planning time (Phase 2 spec §3.4, seven-tool branch):

```markdown
<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->
**codegraph.** For code-structure questions use the codegraph MCP tools: `codegraph_search` (find a symbol by name), `codegraph_node` (one symbol, or a file's outline), `codegraph_callers` and `codegraph_callees`, `codegraph_impact` (what a change reaches) and `codegraph_files`; `codegraph_status` says whether this checkout is indexed. If a codegraph tool says "No CodeGraph project is loaded for this session" or that the index belongs to a different working tree, use Read/Grep for now and run `codegraph init --yes` in the directory printed by `git rev-parse --show-toplevel` (safe to repeat; a session-start hook usually does this already). Run codegraph as the path in `~/.codegraph/.superclaude-bin` when that file exists, else as `codegraph`. Never run `codegraph status`, `codegraph index` or `codegraph sync` while an init or index may be running (`pgrep -f 'codegraph\.js (init|index)'` prints a line): they can empty the index. An interrupted index is repaired by the codegraph MCP server on its next connection. In a checkout indexed for the first time, answers in the first minute can be missing or incomplete; ask again after the init finishes. codegraph tools are read-only; edit with Edit/Write.
<!-- SUPERCLAUDE_CODEGRAPH_END -->
```

(If IronClaude's merged `src/superclaude/core/CLAUDE.md` at the pinned SHA has different text, copy that instead: it is the source of truth.)

### 2.4 Removal IronClaude performs (Phase 1)
From Phase 1 spec §3 (read 2026-10-29; verify against the merged code):
- A non-fatal "retire" step at the end of `superclaude install` (new module `src/superclaude/cli/install_retired_mcp.py`), after the codegraph phase. A failure in it never changes the exit code.
- **`codebase-memory-mcp`:** the user-scope entry is removed when its `command` is an absolute path with basename `codebase-memory-mcp`, stdio, no args/env/headers. This covers Coder's `/usr/local/bin/codebase-memory-mcp` entry.
- **`serena`:** Phase 1 alone removes only three older argv shapes that only IronClaude code produced, and keeps the current-pin argv (`uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`, identical to IronClaude's registry, its docs and Coder's bundle). **Phase 2 amends this** (Phase 2 spec §2.12, decided by a full adversarial run): when `codegraph_ready()` is true in the same `superclaude install` run, the retire step removes **every** user-scope Serena launcher entry, matched by shape under any name except `serena-local` (args contain `start-mcp-server`, stdio, `env` and `headers` absent or `{}`: the bundle's entry has `"env":{}`), including the bundle's, and the kind-B `~/.local/bin/codebase-memory-mcp` registration. When codegraph is not ready, Serena is kept and a hint printed. The hint suggests re-registering under the name `serena-local`, which is never removed.
- **What Coder must do:** stop the bundle re-adding Serena in its step 2 (before the IronClaude merge), or every boot re-adds what IronClaude removed; add the guarded backstop migration in `T/scripts/startup.sh`, not in the bundle `install.sh` (only when a `codegraph` user entry exists whose command prints `1.6.2`; remove `serena` only if it equals the bundle argv, and the exact `/usr/local/bin/codebase-memory-mcp` entry); remove the baked binary in step 5.
- Acceptance (Phase 2 spec §2.12), user scope: `jq -e '(.mcpServers // {}) | (has("serena") or has("codebase-memory-mcp") or (to_entries | map(select(.key != "serena-local" and ((.value.args // []) | tostring | test("serena-agent|start-mcp-server")))) | length > 0)) | not' ~/.claude.json`; local scope (never removed automatically; a failure means run the printed `claude mcp remove <name> --scope local`): `jq -e '[(.projects // {}) | .[] | (.mcpServers // {}) | has("serena") or has("codebase-memory-mcp")] | any | not' ~/.claude.json`.
- IronClaude never deletes `/usr/local/bin/codebase-memory-mcp`, the `serena-agent` uv tool, `~/.serena`, `~/.cache/codebase-memory-mcp` or bundle markers (section 3).
- Phase 1 also writes `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md` with these facts as finally implemented. Read it (same retrieval method as this file) and prefer it where it differs from this section, **except for Serena removal**: there Phase 2 spec §2.12 (summarised above) overrides it, because Phase 1 was written before that decision (IronClaude task T0b appends the override to that file). Spec: `.dev/codegraph-migration/specs/phase-1-removal-spec.md` §3, §6.2, §7.

## 3. Removal list on a workspace

Observed on a live Coder workspace on 2026-10-29 (IronClaude inventories `.dev/codegraph-migration/inventory/codebase-memory.md` §3 and `inventory/serena.md` §5). "IronClaude" in the owner column means the new `superclaude install` removes it (Phase 1 design; verify against the merged IronClaude code before relying on it). "Coder" means only the Coder repo can remove it.

### 3.1 codebase-memory-mcp

| Artifact | Observed | Owner |
|---|---|---|
| `/usr/local/bin/codebase-memory-mcp` (v0.12.1, root-owned) | present | **Coder** image: delete the bake in `T/Dockerfile.coder:323-351` |
| User-scope registration `mcpServers["codebase-memory-mcp"]` = `{type: stdio, command: /usr/local/bin/codebase-memory-mcp, args: []}` in `~/.claude.json` | present | IronClaude (the Phase 1 retire step removes this shape through `claude mcp remove codebase-memory-mcp --scope user`, section 2.4). Coder: if the workspace never reruns the new `superclaude install`, remove it with the same command |
| Daemon `codebase-memory-mcp --cbm-daemon-internal` + one stdio process per live session | running | stops on session restart / new image |
| `~/.cache/codebase-memory-mcp/` (4.2 MB, no project indexes) | present | Coder, optional purge after the binary is gone |
| `~/.local/bin/codebase-memory-mcp`, `~/.local/bin/install.sh`, receipt `~/.local/bin/.superclaude-codebase-memory.json` | absent on Coder (only exist where IronClaude ran the upstream installer) | n/a on Coder |
| Companion skills/agents/hooks in `~/.claude`, `~/.codex`, `~/.config/opencode` | absent on Coder (the upstream binary's `install` never ran) | n/a on Coder |
| Contract test assertion `test-57-catalogue-configure.sh:243-244` | present | **Coder** |

### 3.2 Serena

| Artifact | Observed | Owner |
|---|---|---|
| `uv tool install serena-agent==1.7.0` (entry points `serena`, `serena-agent`, `serena-hooks` in `~/.local/bin`) | present, created by Coder's bundle (`T/catalogue/mcp-bundle-core/install.sh:128-131,148-170`) | **Coder**: `uv tool uninstall serena-agent` |
| User-scope registration `mcpServers["serena"]` (`uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`) | present; the bundle re-adds it on every start (`install.sh:67-119`) | IronClaude removes it once codegraph is ready (section 2.4). **Coder** must stop the bundle re-adding it (step 2) and add the guarded backstop migration |
| Bundle marker `~/.aidev/installed/mcp-bundle-core.serena` | present | **Coder** (`aidev_cat_unmark`-style removal, `T/scripts/startup.sh:945-960`) |
| uv cache entries for `serena-agent` | present | Coder, optional `uv cache clean serena-agent` |
| `alias serena=…` in `T/workspace_defaults/bashrc.skel:88` (copied into new shells) | present in the template | **Coder** |
| `~/.serena/` (62 MB: logs, language servers, config listing 12 projects) and per-project `.serena/` folders | present | **User data: do not delete automatically.** Print the command; delete only with the user's consent |
| Hook matcher with `mcp__serena__*` in `~/.claude/settings.json` | present | IronClaude (`superclaude install --force` rewrites it once `hooks.json` drops the alternatives) |
| Serena text in installed `~/.claude/` commands, skills, agents, core docs | present | IronClaude (`superclaude install --force`) |

### 3.3 What the new IronClaude expects the image to provide

- `codegraph` on PATH, reporting exactly the pinned version (`1.6.2`), executable by user `coder`. With it, IronClaude's install makes **no network call** for codegraph.
- The `claude` CLI on PATH (registration uses `claude mcp add-json`).
- Nothing else: IronClaude does not need Codebase Memory, Serena or uv for codegraph.

## 4. Coder touchpoints (starting points, verify on current main)

Found by reading Coder at `e25f787c` (IronClaude `research/install-update-flow.md` §4). These are leads, not a plan.

| Area | path:line at `e25f787c` | What it does today |
|---|---|---|
| Codebase Memory bake | `T/Dockerfile.coder:323-351` | SpecStory layer also downloads codebase-memory-mcp v0.12.1 per arch, checks a pinned sha256 (`:342-347`), `install -m 0755` to `/usr/local/bin` (`:350`). Comment `:324-328`: kept in this layer for the Sysbox layer budget, outside `INSTALL_MATRIX`. **Model for the codegraph bake.** |
| IronClaude pin | `T/Dockerfile.coder:370-376` | `ARG IRONCLAUDE_GIT_SHA=55d4030874676c664eb640b60c92fe6cc9bfeb52` (`:375`), the sole pin authority (`:371-372`) |
| IronClaude bake | `T/Dockerfile.coder:381-431` | validates the SHA, writes `/etc/aidev02/ironclaude-provenance`, `uv tool install` into `/opt/uv/tools`, checks `superclaude --version` as `coder` |
| CLAUDE.md seed | `T/Dockerfile.coder:572-578`, `T/workspace_defaults/CLAUDE.md` | seeds `~/.claude/CLAUDE.md` once; no MCP text |
| IronClaude slug | `T/catalogue/ironclaude/install.sh:23-35,88-95,112-125,141-149` | reruns `superclaude install` only when the image SHA changes (`--force` then); `timeout 60 … </dev/null` (`:120`); saves/restores `~/.claude/CLAUDE.md` (`:44-66`); writes `.configured` after verification |
| Slug budget and order | `T/scripts/startup.sh:1079-1088`, `:693`, `:1182` | `ironclaude` and `mcp-bundle-core` get 75 s; slugs run in `LC_ALL=C` order (`ironclaude` before `mcp-bundle-core`) |
| Slug runner / unmarker | `T/scripts/startup.sh:892-938`, `:945-960` | watchdog-bounded installer; marker removal when a slug leaves a profile |
| MCP bundle (Serena) | `T/catalogue/mcp-bundle-core/install.sh:1-5,17-20,67-119,128-131,148-170,189-201,215-229` | pins `SERENA_PIN=1.7.0`; registers Auggie, Serena, Tavily, Context7 if absent (never removes); installs and warms Serena; exit 2 unless all four registered |
| Bundle manifest/health | `T/catalogue/mcp-bundle-core/manifest.yaml:7,9-13,21-29,40`; `T/scripts/lib/spec2-health.sh:76-79,101-111,145-170` | user text lists Serena; health requires `auggie serena tavily context7`; `ironclaude` health is `command hook provenance` only |
| Serena alias | `T/workspace_defaults/bashrc.skel:88` | `alias serena=…` |
| Profiles | `T/catalogue/profiles.yaml:18` | default `orca` profile includes `ironclaude` and `mcp-bundle-core` |
| Orca | `T/orca/runtime.mjs:299,315,541` | Orca's Claude command is IronClaude's `ccsession-orca` |
| Contract tests | `.github/contract-tests/test-57-catalogue-configure.sh:226-231,243-244,292-314,488-499,602-603,613-636`; `test-startup-boot.sh:1197-1211,1978-2066`; `test-46-catalogue-health.sh:1171-1234`; `test-49-spec2-evidence.sh:31,307,314-315,563`; `test-19-catalogue-cli-presence.sh:635-640`; `test-60-llm-gateway-env.sh:174-176`; `test-48-ironclaude-provenance.sh:4-9,175-184` | assert the Codebase Memory registration, Serena registration/handshake, bundle markers, exactly one 40-hex IronClaude SHA on the ARG line |
| CI wiring | `.github/workflows/coder-ci-aidev02-contract.yml:19-24,1219,1221` | runs test-48 and test-57 in the built image, test-57 with `--network=none` |
| Pin monitor | `.github/workflows/ironclaude-upstream-monitor.yml:10-12,41,80-82,107,114,131-134,145-276,278-340` | daily; bumps to every IronClaude `master` HEAD; edits only the ARG line; proof runs only `superclaude --version` |
| Other | `scripts/refresh-all-workspaces:1-14`; Coder's own `.serena/project.yml` and `.serena/memories/` | operator env fan-out (not an IronClaude updater); Coder repo's own Serena developer config |
| Index-automation leads | `T/scripts/lib/spec2-health.sh:113` (`~/.aidev/status/seed-repo-path`, BMad seed repo); `.github/contract-tests/test-59-home-workspaces-dir.sh` (`~/workspaces` handling); Orca worktree creation (`T/orca/`); `T/scripts/startup.sh` | candidate places that create or clone checkouts; none researched yet |

Not relevant (checked): `templates/VSCode-AIDev01/` has no Codebase Memory or Serena reference; Coder never runs `superclaude update` or IronClaude's `update.sh`.

## 5. Ordering constraints

1. Coder pins one IronClaude `master` SHA and the monitor bumps to every new `master` HEAD with a one-line edit; the bump PR cannot carry test changes (`ironclaude-upstream-monitor.yml:131`).
2. The new IronClaude's `superclaude install` needs a `codegraph` reporting `1.6.2` on PATH to stay offline; Coder CI runs it with `--network=none`, and real boots allow 60 s.
3. Therefore, in this order: (a) Coder bakes codegraph v1.6.2, additive only; (b) Coder makes its contract tests accept both the old state (Codebase Memory registered) and the new one (codegraph registered; Codebase Memory and Serena registrations absent), and retires Serena from the bundle with its tests plus the guarded backstop migration (section 2.4); (c) IronClaude merges Phases 1 and 2 as one `master` merge, gated on (a) and (b) being on Coder `main`; (d) Coder pin bump goes through contract CI; (e) only then Coder removes the Codebase Memory bake from the image and adds index automation and the CLAUDE.md codegraph block.
4. Removing the baked Codebase Memory binary before (d) breaks the old pinned IronClaude (its required Codebase Memory phase would try to download offline). Retiring Serena from the bundle before (d) is safe for the old IronClaude (it never touches Serena) but needs the Coder tests changed with it.
5. "Completely absent" on an existing Coder workspace: registrations right after the new IronClaude's install runs, staying absent once the image from (b) no longer re-adds Serena; Serena programs with the (b) image; `/usr/local/bin/codebase-memory-mcp` only with the (e) image (root-owned; no user-level step can remove it).
6. Existing workspaces converge at their next restart on the new image: the `ironclaude` slug reruns `superclaude install --force` when the SHA changes (`T/catalogue/ironclaude/install.sh:91-95`). Registrations in `~/.claude.json` survive image changes, so removing a binary does not remove its registration.
