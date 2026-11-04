# Scan C: install and deploy surface (v5.0.0)

- Run: `/sc:post-release v5.0.0`, workstream C (install & deploy), read-only scanner
- Install-surface class: `package` (pyproject.toml, installed from git with pipx; no Docker/VM deploy)
- Repo: `/home/coder/workspaces/worktrees/IronClaude/post-release-v5.0.0`, HEAD `d953b983` == tag `v5.0.0` (`git rev-parse v5.0.0^{commit} HEAD` both print `d953b98381906c0124cc1403fd04d0c6611654d9`)
- Scan date: 2026-11-02 (env says 2026-11-03)
- Ground truth: `CHANGELOG.md` `## [5.0.0]` (line 7), `docs/releases/v5.0.0.md` Migration Required (139-157) and Known Issues (226-233)
- Nothing was installed. Only `--help`/`--version` runs, `pipx environment`, `command -v`, `ls`, `git tag/show/log`, `gh repo view`, and file reads.

## Real install path (from code)

### Package metadata (`pyproject.toml`)

| Item | Value | Evidence |
|---|---|---|
| Distribution name | `superclaude` (same name as the upstream PyPI package; install from the fork URL) | `pyproject.toml:6` |
| Version | `5.0.0` | `pyproject.toml:7`; `uv run superclaude --version` prints `SuperClaude, version 5.0.0` |
| Python | `>=3.10` (classifiers list 3.10-3.12 only) | `pyproject.toml:16,25-27` |
| Runtime deps | pytest>=7, click>=8, rich>=13, pyyaml>=6, jsonschema>=4, jinja2>=3, pexpect>=4.9, httpx>=0.27 | `pyproject.toml:34-43` |
| Console scripts | `superclaude = superclaude.cli.main:main`, `ic = superclaude.cli.ic:main` | `pyproject.toml:70-72` |
| pytest plugin | entry point `superclaude.pytest_plugin` | `pyproject.toml:75-76` |
| Wheel payload | `src/` and `plugins/` force-included as `superclaude/_src`, `superclaude/_plugins` (installers fall back to `_src` in a wheel) | `pyproject.toml:85-87`; `install_user_setup.py:39-46` |
| Repo visibility | PUBLIC, so `git+https://github.com/IronbellyOrg/IronClaude` needs no credentials | `gh repo view IronbellyOrg/IronClaude --json visibility` printed `PUBLIC` |

### New-user commands (documented and real)

```bash
pipx install git+https://github.com/IronbellyOrg/IronClaude   # needs git, network, Python >=3.10
superclaude install                                             # needs claude CLI + network for codegraph
```

(`README.md:59-62`, `docs/getting-started/installation.md:138-141`.) From a clone: `uv venv && make install && uv run superclaude install` (`README.md:70-76`); `make install` is only `uv pip install -e ".[dev]"` and does NOT run `superclaude install` (`Makefile:5-10`).

### `superclaude install` (flags, ordered steps, exit code)

Flags (`main.py:29-46`, `--help` output): `--target TEXT` (default `~/.claude/commands/sc`), `--force` ("Force reinstall framework files"), `--list` (list without installing). No dry-run, no home/config-dir flag.

| # | Step | Writes to | `--force` effect | Evidence |
|---|---|---|---|---|
| list | `--list`: core/commands/agents/skills/templates installed-vs-available, codegraph block (runs `codegraph --version`, no download, no `claude mcp` call), retired-MCP verdicts; returns exit 0 | nothing | n/a | `main.py:86-172`; `install_mcp.py:1059-1060` |
| 1 | Core `.md` files | `~/.claude/*.md` (hardcoded `Path.home()/.claude`) | overwrite existing; without it existing files are skipped | `main.py:174-180`; `install_core.py:46-47,68-70` |
| 2 | Slash commands | `--target` (default `~/.claude/commands/sc`) — the ONLY step `--target` affects | overwrite existing | `main.py:182-190`; `install_commands.py:27,55-57` |
| 3 | Agents | `~/.claude/agents/` | overwrite existing | `main.py:192-198`; `install_agents.py:27,51-53` |
| 4 | Skills | `~/.claude/skills/<name>/`; `sc-*` skills that have a `/sc:` command are not installed and any stale copy is `rmtree`d even without `--force` | with `--force` each shipped skill dir is `rmtree`d then re-copied (files a user added inside are lost) | `main.py:200-206`; `install_skills.py:76,89-104`; `install_skill.py:40-48` |
| 4b | ccsession wiring (no force param) | symlinks `~/.local/bin/ccsession` and `~/.local/bin/ccsession-orca`; seeds `~/.claude/ccsession.env` (0600) only if absent; runs `skills/ccsession-tag/seed-env.py` (writes `ANTHROPIC_BASE_URL` into that env file); runs `ccsession --migrate-names` with `HOME` passed through | none | `main.py:208-211`; `install_ccsession.py:33-35,60-71,72-88,91-98,104-115`; `seed-env.py:31-32` |
| 5 | Hooks | scripts to `~/.claude/hooks/`; additive atomic merge into `~/.claude/settings.json` with backup `settings.json.bak.<ISO>`; seed `~/.claude/auggie-projects.txt` only if absent | overwrite scripts; refresh framework-owned registrations (without it an existing framework registration is skipped) | `main.py:213-219`; `install_hooks.py:9-15,89-91,135-140,158-196,400-402` |
| 6 | Templates | `~/.claude/templates/` | overwrite existing | `main.py:221-229`; `install_templates.py:45,71-73` |
| 7 | User setup | rules to `~/.claude/rules/` + `claudeMdExcludes` merged in settings.json; `~/.claude/output-styles/`; settings defaults (fill missing keys only); Orca skills via `orca-ide`/`orca skills install --agent claude-code` if an Orca CLI answers; default plugins via `claude plugin marketplace add` + `claude plugin install <p> --scope user -y` (network, 30 s shared budget; Orca and plugins never fail the step) | overwrite rules/output-style files; settings defaults never overwrite user values | `main.py:231-237`; `install_user_setup.py:31-35,92-119,122-134,137-172,175-240,251-311,314-324`; plugin list `user_settings_defaults.json:28-49` |
| 8 | codegraph (required) | see next table; `--force` NOT forwarded | none | `main.py:239-253`; docstring `main.py:50-52` |
| 9 | Retire stale MCP registrations (non-fatal, 15 s cap) | removes user-scope `serena`/`codebase-memory-mcp` (and, once codegraph is ready, any Serena launcher except `serena-local`) via `claude mcp remove <n> --scope user`; deletes IronClaude's own private receipt/marker files in `~/.local/bin` | none | `main.py:255-267`; `install_retired_mcp.py:35,259-290,385-494` |
| exit | Exit 1 if any of core/commands/agents/skills/ccsession/hooks/templates/user-setup/codegraph failed; retire step can never change it; click usage errors exit 2 | | | `main.py:269-280` |

### codegraph phase detail (`install_mcp.install_codegraph_mcp` + `install_codegraph.acquire`)

| Stage | Behaviour | Evidence |
|---|---|---|
| scope | user only | `install_mcp.py:926-927` |
| prerequisite | runs `claude --version` (10 s); non-zero/missing → fails before any discovery or download ("Prerequisites: Claude CLI is unavailable") | `install_mcp.py:937-947` |
| discover | first copy printing exactly `1.6.2`: `shutil.which("codegraph")`, then `~/.local/bin/codegraph`; reused with no network; pointer written to `~/.codegraph/.superclaude-bin` | `install_codegraph.py:26,97-128,141-152,273-278` |
| platform | only `linux`/`darwin` × `x64`/`arm64` (SHA table); else fail with manual-install text | `install_codegraph.py:28-33,46-52,280-289` |
| pre-existing dir | `~/.codegraph/versions/v1.6.2` not in receipt: reused if it prints 1.6.2, else fail | `install_codegraph.py:291-306` |
| download | `https://github.com/colbymchenry/codegraph/releases/download/v1.6.2/codegraph-<asset>.tar.gz`, 60 s timeout, temp dir inside `~/.codegraph` | `install_codegraph.py:37,308-327` |
| verify | SHA-256 must equal pinned value | `install_codegraph.py:328-330` |
| extract | strict member checks (no abs/`..`/links, ≤20 000 members, ≤2 GiB); extracted binary must print 1.6.2 | `install_codegraph.py:39-40,193-224,331-340` |
| install | receipt `~/.codegraph/.superclaude-receipt.json` written before creating; dir renamed to `~/.codegraph/versions/v1.6.2`; links `~/.local/bin/codegraph` and `~/.codegraph/current` (never replaces a link it does not own) | `install_codegraph.py:59-72,248-264,342-353` |
| register | reads root `mcpServers.codegraph` from `$CLAUDE_CONFIG_DIR/.claude.json` or `~/.claude.json` (empty `CLAUDE_CONFIG_DIR` = lookup unknown = fail); writes only through `claude mcp add-json codegraph '<json>' --scope user` (and `claude mcp remove codegraph --scope user` for an owned stale entry); exact entry: stdio, `<abs path> serve --mcp`, `alwaysLoad`, env telemetry off / no update check / `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`; a user-managed entry whose command runs is kept | `install_mcp.py:709-741,862-874,893-902,954-1020`; `install_codegraph.py:35` |
| prune | older receipt-listed version dirs removed one run later | `install_codegraph.py:368-404` |

### `superclaude doctor` (`main.py:471-510`, `doctor.py:17-54`)

Checks: pytest plugin, agents (always passes), skills (fails only if an installed command needs a missing skill), configuration (import), ccsession (files, `~/.local/bin` links, SessionStart/UserPromptSubmit/SessionEnd hooks), codegraph, retired MCP (warn only). Exit 1 if any check fails. The codegraph check FAILS only when the registered command is not executable; "no codegraph registration" is a detail line and still passes (`doctor.py:160-175`), so plain `doctor` passes after an `update`-only upgrade (matches Known Issues `v5.0.0.md:232`).

### Other commands

- `superclaude version` / `--version`: prints version (`main.py:19,513-516`).
- `superclaude install-skill <name> [--target ~/.claude/skills] [--force]`: one skill; `--force` rmtrees then copies; exit 1 on failure (`main.py:432-468`; `install_skill.py:40-48`).
- `superclaude mcp [--servers X ...] [--list] [--scope local|project|user] [--dry-run]`: optional servers; `--list` combined with anything else is a UsageError; exit 1 on failure (`main.py:283-331`).

## Real upgrade path

### Documented 5.0.0 upgrade (correct per code)

```bash
pipx install --force git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force
```

(`v5.0.0.md:144-151`.) `install --force` = every framework step with force=True, PLUS the codegraph phase and the retire step (`main.py:178-267`). `pipx install --force` is needed because `pipx upgrade` skips while the version string is unchanged (stated in `installation.md:326-327`; not re-verified here).

### `superclaude update` is NOT an upgrade for 5.0.0

`update` (`main.py:334-429`) runs core/commands/agents/skills/ccsession/hooks/templates/user-setup with `force=True` (`main.py:365,372,378,384,388,394,399,404`) and then only prints `update_notice()` ("legacy registration present: run `superclaude install`") when something is removable (`main.py:407-415`; `install_retired_mcp.py:320-324`). It never calls `install_codegraph_mcp` and never runs `run_retire_step`. Exit 1 only on framework-step failure (`main.py:417-429`). Its `--help` text also understates it ("core framework files, slash commands, agents, skills, and hooks"; `main.py:344-345`) — it also does ccsession, templates and user setup.

So: `install --force` ⊇ `update`; same overwrite/rmtree destructiveness, plus codegraph + retire.

### `update.sh` (clone-based upgrade), line by line

| Line | Command | Effect / risk |
|---|---|---|
| 2 | `set -euo pipefail` | any failure stops the script |
| 4-5 | `REPO_ROOT=...; cd "$REPO_ROOT"` | runs from the clone root |
| 7 | `pipx install --force ./` | installs the CHECKED-OUT working tree (not the git URL, not a tag); user must check out/pull `v5.0.0` first — no doc says so. Needs `pipx` on PATH (exit 127 otherwise; Known Issue `v5.0.0.md:228` says "first line", it is line 7, the first command after `cd`) |
| 8 | `superclaude install --force` | full install incl. codegraph + retire; exit 1 stops the script before doctor |
| 9 | `make sync-dev` | copies `src/superclaude/*` into the clone's `.claude/` (dev mirror; needs `make`) — irrelevant to non-dev users |
| 10 | `superclaude doctor` | plain doctor (passes even without codegraph registration, but line 8 already enforced it; `doctor.py:151-153`) |

### Upgrade baselines available for an e2e

- Tags: only `v5.0.0` and `v3.9` (`git tag`). `v3.9` is package version 4.2.0.
- `f13c9ea2^` = `38b64098` is 4.3.5 but ALREADY contains the codegraph phase (`git show 38b64098:src/superclaude/cli/main.py | grep -c install_codegraph_mcp` = 2) — not a pre-codegraph baseline.
- `2f10a0e1^` = `539e2414` (merge of #328) is 4.3.5 with NO codegraph in `main.py` (grep count 0): the right "pre-5.0.0 user" baseline: `pipx install git+https://github.com/IronbellyOrg/IronClaude@539e2414`.

## Isolation plan for a throwaway e2e

### What isolates and what does not

| Mechanism | Isolates? | Evidence |
|---|---|---|
| `--target DIR` | NO. Only the slash-command destination; every other step hardcodes `Path.home()` | `main.py:183-188`; `install_core.py:47`; `install_agents.py:27`; `install_skills.py:76`; `install_hooks.py:136`; `install_templates.py:45`; `install_user_setup.py:93,125,138,211,255`; `install_ccsession.py:12`; `install_codegraph.py:56,68`; `install_retired_mcp.py:266,393` |
| `HOME=<tmp>` | YES for every Python write (`Path.home()` reads `$HOME` on POSIX) and for the `claude`, `pipx`, `uv`, `orca` subprocesses' defaults | same lines as above |
| `CLAUDE_CONFIG_DIR` | Must be UNSET (or set inside the throwaway). The installer READS `$CLAUDE_CONFIG_DIR/.claude.json` when set, else `$HOME/.claude.json`; an empty value makes registration fail. All file installs ignore it (always `$HOME/.claude/`). Not set in this environment | `install_mcp.py:721-726`; `env` listing had no `CLAUDE_CONFIG_DIR` |
| `PATH` | Must be curated. The image has a pinned codegraph at `/usr/local/bin/codegraph -> /opt/codegraph/v1.6.2/bin/codegraph` (prints `1.6.2`) and `/home/coder/.local/bin/codegraph`; `shutil.which("codegraph")` would reuse one of them and the download/verify path would NOT run, and the registration would point outside the throwaway. `orca-ide` is in `/usr/bin` and `/bin`, and `/home/coder/.config/orca/linux-orca-cli-shim/orca` is first on PATH | `install_codegraph.py:104-122,273-278`; `ls -l /usr/local/bin/codegraph /usr/bin/orca-ide`; `install_user_setup.py:29-30,175-198` |
| pipx dirs | `PIPX_HOME`/`PIPX_BIN_DIR` default from `$HOME` (`pipx environment`: `/home/coder/.local/share/pipx`, `/home/coder/.local/bin`; none set in env); pipx 1.18.11 at `/home/coder/.local/bin/pipx` | `pipx environment` output |

### Recommended recipe (exact)

```bash
E=/tmp/ic-e2e.$$; mkdir -p "$E/home" "$E/shims"
# real tools only; shadow codegraph and Orca with failing stubs
ln -s /usr/local/bin/claude /usr/local/bin/uv /usr/bin/git /usr/bin/python3 /usr/local/bin/node "$E/shims/"
ln -s /home/coder/.local/bin/pipx "$E/shims/pipx"
for s in codegraph orca orca-ide; do printf '#!/bin/sh\nexit 127\n' > "$E/shims/$s"; chmod +x "$E/shims/$s"; done
run() { env -i HOME="$E/home" PATH="$E/home/.local/bin:$E/shims:/usr/bin:/bin" \
        LANG=C.UTF-8 TERM=dumb "$@"; }
run pipx install git+https://github.com/IronbellyOrg/IronClaude@v5.0.0   # new-user path
run superclaude install; echo "exit=$?"
run superclaude install --list
run superclaude doctor --verbose
# upgrade path: fresh $E, then
#   run pipx install git+https://github.com/IronbellyOrg/IronClaude@539e2414 && run superclaude install
#   run pipx install --force git+https://github.com/IronbellyOrg/IronClaude@v5.0.0 && run superclaude install --force
rm -rf "$E"
```

Why each piece: `env -i` drops `CLAUDE_CONFIG_DIR`, `CLAUDECODE`/`CLAUDE_CODE_*`, `XDG_*`, `PIPX_*`, `UV_*`, `CCSESSION_*` (`HOME=` alone leaves them). The `codegraph` stub makes `inspect_binary` see a "mismatch" and fall through to `$E/home/.local/bin/codegraph` (absent on first run) so the download + SHA-256 + extract + link path runs (`install_codegraph.py:107-122,280-353`); on later runs `$E/home/.local/bin` is first on PATH so the installed link is found and no PATH warning is printed (`install_codegraph.py:155-163`). The `orca`/`orca-ide` stubs make `_find_orca` skip (`install_user_setup.py:181-198,215-217`). The stubs must come BEFORE `/usr/bin` and `/bin` because `orca-ide` lives there. Alternative for Orca: pre-create `$E/home/.claude/skills/{computer-use,orca-cli,orchestration}/SKILL.md` (short-circuit at `install_user_setup.py:213-214`). The `/usr/bin:/bin` tail is required for the bash ccsession wrapper (`sed`, `readlink`, `dirname`) run by `--migrate-names` (`install_ccsession.py:104-113`). Note: `env -i` also drops `ANTHROPIC_BASE_URL`, so `seed-env.py` seeds nothing (harmless; `seed-env.py:32`). If a proxy is needed add `https_proxy=...` (urllib honours it).

To seed the retire step for the upgrade run, write a Tier-R Serena entry into `$E/home/.claude.json` root `mcpServers.serena` before `install --force` (shapes in `install_retired_mcp.py:56-89`).

### Residual side effects (outside the throwaway or outside the machine)

| Side effect | Where | Evidence / status |
|---|---|---|
| `claude mcp add-json/remove ... --scope user` | `$HOME/.claude.json` of the throwaway when `CLAUDE_CONFIG_DIR` is unset — inferred from the installer's own read path; Claude Code's write location under a fake HOME is UNVERIFIED until the e2e checks `$E/home/.claude.json` and that `/home/coder/.claude.json` mtime is unchanged | `install_mcp.py:721-735,893-902` |
| `claude plugin marketplace add` / `plugin install --scope user -y` for 6 default plugins (2 marketplaces on GitHub) | network (GitHub clones) + `$HOME/.claude/plugins/`; may need auth or time out (30 s budget); non-fatal | `install_user_setup.py:251-311`; `user_settings_defaults.json:28-49` |
| codegraph tarball download | network to github.com/colbymchenry; files under `$HOME/.codegraph`, link in `$HOME/.local/bin` | `install_codegraph.py:308-353` |
| pipx clone of the package | network to github.com/IronbellyOrg (public); venv under `$HOME/.local/share/pipx` | `pipx environment` |
| `claude` first-run state (statsig, todos, etc.) | inside `$HOME/.claude` (UNVERIFIED) | — |
| Orca `skills install` if not stubbed | Orca CLI may act through the running Orca app; write location UNVERIFIED — must be stubbed | `install_user_setup.py:218-228` |
| codegraph SessionStart indexing hook | not run by install; only fires if a Claude session is started in the throwaway, then writes `.codegraph/` in that repo and a log under `${XDG_STATE_HOME:-~/.local/state}` | `install_hooks.py:79-81`; `mcp-installation.md:44,48` |
| caches | `~/.cache/pip`, `~/.cache/uv` resolve to the throwaway with `env -i HOME=` | default `$HOME`-relative |
| `SIGKILL`/host loss | throwaway dir may remain under `/tmp` | — |

Verification after the run: `/home/coder/.claude.json` and `/home/coder/.claude/settings.json` mtimes unchanged; `ls /home/coder/.codegraph/versions` unchanged; `$E/home/.claude.json` has `mcpServers.codegraph.command` under `$E/home/.codegraph/versions/v1.6.2/bin/codegraph`.

## Doc claims vs code

| # | Doc:line | Claim | Code evidence | Correct statement | Severity |
|---|---|---|---|---|---|
| 1 | `docs/getting-started/installation.md:53-57` | "Existing installations receive refreshed core files and hook registrations with `superclaude update`" | `update` never installs codegraph or retires MCP entries (`main.py:334-429`, esp. 407-415); release says use `install --force` (`v5.0.0.md:144`) | For 5.0.0 (and generally), existing installs upgrade with `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force` | High |
| 2 | `installation.md:326-333` | Upgrade = `pipx install --force ...` then `superclaude update` (pip: same with `--force-reinstall`) | as #1 | Replace `superclaude update` with `superclaude install --force` in both blocks | High |
| 3 | `installation.md:363` | "A plain `superclaude install` never replaces files you already have; run `superclaude update` to get the new CLAUDE.md..." | plain install skips existing files (`install_core.py:68-70` etc.) but does `rmtree` stale `sc-*` skill dirs (`install_skills.py:89-98`), merges settings.json (`install_user_setup.py:110-114,168`; `install_hooks.py:181-185`), and runs codegraph + retire (`main.py:239-267`); `update` misses codegraph/retire | "Plain `superclaude install` keeps existing framework files; run `superclaude install --force` to refresh them (it also installs codegraph and retires old MCP entries)" | High |
| 4 | `installation.md:365` | "`superclaude install --force` does the same" (as `update`) | Destructive part is true for both (`install_skill.py:46-48`, `install_core.py:68-73`), but `install --force` additionally runs codegraph and retire (`main.py:239-267`) and exits 1 on codegraph failure (`main.py:278-280`) | "`superclaude install --force` overwrites the same files and also installs/registers codegraph and retires old MCP registrations" | Medium |
| 5 | `docs/user-guide/mcp-installation.md:71` | "`superclaude install --force` reinstalls framework files only." | `--force` is not forwarded to codegraph (`main.py:52,239-246`) but `install --force` still runs the codegraph phase and the retire step on every run (`main.py:239-267`) | "`--force` only changes the framework-file steps (overwrite instead of skip); the codegraph phase and retire step run on every `superclaude install`, with or without `--force`." Rest of line (`--target` only moves slash commands; no dry-run) is correct (`main.py:183-188`) | Medium |
| 6 | `installation.md:80-94` | Git listed as Optional; pip "Required"; pipx Optional | Every documented install is `git+https://...` (needs `git`); the codegraph phase needs network + `claude` CLI (`install_mcp.py:937-947`; `install_codegraph.py:308-327`) | Required: Python ≥3.10 (`pyproject.toml:16`), git, pipx (recommended) or pip, Claude Code CLI on PATH, network (GitHub) | Medium |
| 7 | `installation.md:34` and Method 2 (`:164-198`, "Best for: Windows users") | pip method works on "All" platforms | codegraph auto-install only Linux/macOS x64/arm64; elsewhere install exits 1 (`install_codegraph.py:46-52,280-289`; `main.py:278-280`); hooks are bash | Windows: framework files install but `superclaude install` exits 1 unless a `codegraph` printing `1.6.2` is on PATH | Medium |
| 8 | `installation.md:134,172` | `python3 -m pip install --user pipx`; `pip install git+...` | This image has `/usr/lib/python3.13/EXTERNALLY-MANAGED` (PEP 668); those commands fail on such systems without `--break-system-packages` | Recommend `uv tool install pipx` / distro `pipx` package (the Known Issue at `v5.0.0.md:228` already suggests `uv tool install pipx`) | Low |
| 9 | `installation.md:280-286` | Verify with `superclaude doctor` | plain doctor passes with no codegraph registration (`doctor.py:160-164`) | Verify with `superclaude doctor --verbose` (no "no codegraph registration" line) and `superclaude install --list` (`v5.0.0.md:153`) | Medium |
| 10 | `installation.md:297-309` "What's Installed" | 5 locations | Also: `~/.claude/templates/`, `rules/`, `output-styles/`, `settings.json` merges, `~/.local/bin/ccsession(-orca)`, `~/.claude/ccsession.env`, `~/.codegraph/`, `~/.local/bin/codegraph`, user `codegraph` entry in `~/.claude.json`, default plugins (`main.py:174-253`; `install_user_setup.py:251-311`) | List all of them | Low |
| 11 | `installation.md:353-361` (uninstall) | Lists leftovers | Omits `~/.codegraph/`, `~/.local/bin/codegraph`, the `codegraph` user registration, `~/.local/bin/ccsession-orca`, plugins; `mcp-installation.md:34-40` has the codegraph removal steps | Add codegraph removal (link to `mcp-installation.md` "Removing codegraph") | Low |
| 12 | `installation.md` (whole file) | — | Never mentions codegraph, the `claude` CLI prerequisite for exit 0, or the network download (grep for `codegraph` in the file: 0 hits) | Add a short codegraph note + link | Medium |
| 13 | `docs/reference/common-issues.md:18-28` | `python3 -m SuperClaude --version # Should show 4.1.5`; `pipx upgrade SuperClaude`; `pip install --upgrade SuperClaude`; `python3 -m SuperClaude install` | No `SuperClaude` module entry; package is `superclaude` from the fork URL (`pyproject.toml:6,70-71`); `pipx upgrade SuperClaude` targets upstream/no-op | `superclaude --version` (5.0.0); upgrade per #1 | High (already a Known Issue, `v5.0.0.md:230`) |
| 14 | `docs/releases/v5.0.0.md:228` | update.sh "stops at its first line (exit 127)" | pipx is on line 7, after `set` and `cd` (`update.sh:2-7`) | "stops at its `pipx` line" | Low |
| 15 | `docs/releases/v5.0.0.md:151` | `./update.sh` "runs the same `superclaude install --force`" | True (`update.sh:8`), but line 7 installs the local working tree (`pipx install --force ./`), so the clone must be on `v5.0.0` first | Add "after `git pull` / `git checkout v5.0.0`" | Low |
| 16 | `src/superclaude/cli/main.py:344-345` (`update --help`) | update re-installs "core framework files, slash commands, agents, skills, and hooks" | also ccsession, templates, user setup (`main.py:388,399,404`); and it does NOT touch codegraph | Mention all steps and "does not install codegraph; use `install --force`" | Low (code text; report only) |
| 17 | `docs/generated/contributor-knowledge-base/cli-api-inventory.md:54` | `update` uses only core/commands/agents/skills | `main.py:351-358` | generated artifact; regenerate or leave | Low |
| 18 | `README.md:59-62,70-76` | new-user install commands | correct per code (`pyproject.toml:6,70-71`; `Makefile:5-10`; `main.py:29-280`) | No change to the commands. Gap: README has no upgrade section | OK / gap |

Claims checked and found CORRECT: `mcp-installation.md:7,9,18,23,64,66,70` (discovery order, version dir, idempotent second run, doctor fails only on non-executable command, exit 1 on codegraph failure, update only prints a notice) — evidence `install_codegraph.py:104-122,291-292`; `install_mcp.py:981-983`; `doctor.py:170-175`; `main.py:278-280,407-415`. `v5.0.0.md:144-153,232-233` match `main.py` and `doctor.py`. `CHANGELOG.md:44,91,114` match code.

## Gaps

1. No standalone, current upgrade doc: the only correct 5.0.0 upgrade instructions are in `docs/releases/v5.0.0.md:139-157`; `installation.md` (the page README and `quick-start.md:3` link to) still says `superclaude update`. README has no upgrade section at all.
2. `docs/getting-started/quick-start.md` exists but only links to the installation guide (`quick-start.md:3`); there is no new-user quickstart that states the real prerequisites (git, `claude` CLI, network) and the expected exit-1 cases.
3. Installer ignores `CLAUDE_CONFIG_DIR` for file placement (always `$HOME/.claude/`, e.g. `install_core.py:47`, `install_hooks.py:136`) but honours it for reading `.claude.json` (`install_mcp.py:721-726`). A user with `CLAUDE_CONFIG_DIR` set gets files where Claude Code may not read them. Undocumented.
4. No `superclaude install --home`/`--config-dir` flag and no dry-run, so a safe e2e needs the `env -i HOME=... PATH=...` recipe above; no doc describes it.
5. Plain `superclaude doctor` passes with no codegraph registration (`doctor.py:160-164`); the installation guide's verification step relies on it.
6. `update.sh` installs the local working tree (`update.sh:7`) and needs `make` (`update.sh:9`); neither is documented.
7. `install --force` exits 1 on codegraph failure only AFTER all framework files are already overwritten (`main.py:178-253`); the release notes state this (`v5.0.0.md:233`) but `installation.md` does not.
8. The plugin-install step (network, `claude plugin install --scope user -y` for 6 plugins) is not mentioned in `installation.md` or README; it is a real network/side-effect step (`install_user_setup.py:251-311`).
9. UNVERIFIED items for the e2e to settle: where `claude mcp add-json --scope user` writes under a fake HOME; whether `claude plugin install` works without auth under a fake HOME; the Orca CLI's write location.

## Self-audit

- Every code claim above was taken from a Read of the cited file in this scan (`main.py` 1-530, `install_codegraph.py` full, `install_mcp.py` 700-1079, `install_retired_mcp.py` full, `install_user_setup.py` full, `install_ccsession.py` full, `install_core.py` full, `install_hooks.py` 1-200 and 385-414, `install_skills.py` 74-133, `doctor.py` full, `update.sh` full, `pyproject.toml` full) or a Grep with line numbers (`install_commands/agents/templates/skill.py` force lines, `Makefile` targets, `seed-env.py`, `user_settings_defaults.json`).
- `--help` outputs captured for `install`, `update`, `doctor`, `mcp`, `install-skill` and the group; `--version` = 5.0.0.
- Environment facts from read-only commands: `CLAUDE_CONFIG_DIR`/`PIPX_*`/`XDG_*` unset; `claude` 2.1.316 at `/usr/local/bin/claude`; `codegraph` 1.6.2 at `/home/coder/.local/bin` and `/usr/local/bin` (-> `/opt/codegraph/v1.6.2`); `orca-ide` in `/usr/bin` and `/bin`; Python 3.13.5 with PEP 668 marker; pipx 1.18.11; Linux x86_64; repo PUBLIC.
- Not verified (marked UNVERIFIED above): Claude Code's write location for user-scope MCP/plugins under a fake HOME; Orca CLI behaviour; the `pipx upgrade` no-op claim (taken from the doc).
- Doc line numbers re-read in this scan: `installation.md` 20-369, `mcp-installation.md` 1-80, `v5.0.0.md` 139-160 plus a grep of 1-266, `README.md` 50-94, `common-issues.md` 10-34.
- No repo file other than this output was written; nothing was installed.

