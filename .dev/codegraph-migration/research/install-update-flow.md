# Install / update flow and Coder touchpoints (task W5)

Task: W5 of the codegraph migration run (issue #323). Read-only research; nothing was installed, registered or edited.

Sources read:
- IronClaude worktree `/home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init` (branch `ironbelly/feat-codememory-codegraph-init`). All IronClaude `path:line` refer to it.
- Coder repo `IronbellyOrg/Coder`, branch `main`, commit `e25f787ccaef04312f64347714a7791221564219`, fetched 2026-10-29. All Coder `path:line` refer to that commit.
- Fetch method (deviation from the brief, same read-only API): `gh search code 'repo:IronbellyOrg/Coder ...'` returned `[]` for every query, so I downloaded `gh api repos/IronbellyOrg/Coder/tarball/main` and extracted it (minus `.dev`, `.agents`, `.claude`) into `/tmp/w5-coder/extract/`. Nothing was written outside `/tmp`. Coder's `.dev/`, `_bmad-output/` and `claudedocs/` trees are historical and were excluded.
- codegraph facts come from its README (`gh api repos/colbymchenry/codegraph/readme`), latest release `v1.6.2`, MIT.

Legend: "required" means a failure of that phase makes the command exit non-zero.

## 1. Flow of update.sh and superclaude install / update / install --list / doctor / mcp

### 1.1 `./update.sh` (10 lines, run from a checkout)

| # | Step | path:line | Required? | Exit effect |
|---|---|---|---|---|
| 1 | Strict shell mode: any failing command ends the script with that command's exit status | `update.sh:2` | n/a | status passes through (`tests/cli/test_update_script.py:81-88` injects exit 23 at each stage and expects 23) |
| 2 | `cd` to the repo root | `update.sh:4-5` | n/a | none |
| 3 | `pipx install --force ./` (puts the new `superclaude` on PATH; the wheel bundles `src/` and `plugins/`, see `pyproject.toml:78-87`) | `update.sh:7` | required | stops the script |
| 4 | `superclaude install --force` (every framework phase plus the required Codebase Memory phase, see 1.2) | `update.sh:8` | required | stops the script; `sys.exit(1)` from `src/superclaude/cli/main.py:275` |
| 5 | `make sync-dev` (copies `src/superclaude/{skills,agents,commands,hooks,templates}` into the repo's own `.claude/`; it never touches `~/.claude` or any MCP registration) | `update.sh:9`, `Makefile:109-158` | required | stops the script |
| 6 | `superclaude doctor` (see 1.5) | `update.sh:10` | required | exit 1 from `main.py:512` |

The four commands and their order are pinned by a test: `tests/cli/test_update_script.py:13-18` and `:68`. Adding or reordering a command in `update.sh` means changing that test.

### 1.2 `superclaude install [--force] [--target PATH]` (`src/superclaude/cli/main.py:29-275`)

Every phase below runs even if an earlier one failed. Failures are collected and one `sys.exit(1)` happens at the end (`main.py:264-275`). Only the Codebase Memory failure prints an extra stderr message (`main.py:257-262`).

| # | Phase | path:line | Required? | Notes |
|---|---|---|---|---|
| 1 | Core framework `.md` files to `~/.claude/` | call `main.py:193`; impl `install_core.py:27-73` | required | copies `src/superclaude/core/*.md`; skips existing files unless `--force` (`install_core.py:65-67`) |
| 2 | Slash commands to `~/.claude/commands/sc` | `main.py:203`; `install_commands.py:14` | required | |
| 3 | Agents to `~/.claude/agents` | `main.py:211`; `install_agents.py:15` | required | |
| 4 | Skills to `~/.claude/skills` | `main.py:219`; `install_skills.py:62-98` | required | skills that a command already serves are removed (`install_skills.py:89-98`) |
| 5 | ccsession wiring | `main.py:224`; `install_ccsession.py:11` | required | |
| 6 | Hooks: scripts to `~/.claude/hooks`, additive merge into `~/.claude/settings.json` | `main.py:232`; `install_hooks.py:113`, `_merge_settings` `:258-456` | required | script list `install_hooks.py:42-79`; registrations come from `src/superclaude/hooks/hooks.json` |
| 7 | Templates to `~/.claude/templates` | `main.py:242`; `install_templates.py:30` | required | |
| 8 | User setup (rules, output styles, settings defaults, Orca skills, plugins) | `main.py:251`; `install_user_setup.py:314-324` | required as a whole, but see Notes | Orca skills (`install_user_setup.py:207-240`) and plugins (`:251-311`) always return success, so they are optional in effect. Rules, output styles and settings defaults can fail the phase. Network budget 30 s (`:35`) |
| 9 | **Codebase Memory MCP, "required user-level phase"** | `main.py:254-262` calls `install_mcp.install_codebase_memory_mcp(scope="user")` | **required** | failure feeds `native_success` into the exit check at `main.py:273` |
| 10 | Aggregate exit | `main.py:264-275` | n/a | exit 1 if any of the nine flags is false; otherwise 0 |

Inside phase 9, which is where an MCP server is installed and registered today (`install_mcp.py:815-913`):

1. Platform gate: user scope only, Linux amd64/arm64 only (`install_mcp.py:486-496`, called at `:819`).
2. `claude --version` must work, else fail before any download (`:830-843`).
3. Acquisition (`install_codebase_memory.py:611-749`, called at `install_mcp.py:846`):
   - reuse a runnable executable already on PATH or at `~/.local/bin/codebase-memory-mcp` (`install_codebase_memory.py:569-608`, reuse branch `:643-650`);
   - otherwise download the upstream `install.sh` with curl (`:671-706`), write a private "pending" marker (`:708`), run it with `bash install.sh --dir=~/.local/bin` (`:710-713`), verify `--version` (`:721`), and write the receipt (`:730`);
   - timeouts: download 60 s, upstream install 300 s (`:27-28`).
4. Registration: read the exact top-level user entry from `~/.claude.json` (`install_mcp.py:714-754`, called `:857`); if it already equals `{type: stdio, command: <abs path>, args: []}` return success (`:864-865`); otherwise remove the old user entry (`:874-894`) and run `claude mcp add-json codebase-memory-mcp <json> --scope user` (`:775-786`, call `:895`); verify by re-reading the file (`:896-898`); restore the previous entry on any failure (`:900-913`).
5. Not done by this phase: indexing, a live MCP handshake (`:863`).

`--force` does not reach phase 9: the call is `install_codebase_memory_mcp(scope="user")` with no force argument (`main.py:255`), pinned by `tests/cli/test_update_command.py:345-370`.

### 1.3 `superclaude install --list` (read-only, `main.py:94-187`)

Prints core, commands, agents, skills and templates availability (`main.py:96-159`), then the Codebase Memory block (`main.py:161-186`: platform check via `_native_selection_error` `install_mcp.py:486`, `discover_executable` `install_codebase_memory.py:569`, `read_user_mcp_entry` `install_mcp.py:714`, `_native_registration_matches` `:757`). It always returns at `main.py:187` with exit 0; no phase is required and nothing is changed. A codegraph status block would be added here.

### 1.4 `superclaude update [--target PATH]` (`main.py:346-431`)

Runs the same framework phases as install, all with `force=True`: core `:377`, commands `:384`, agents `:390`, skills `:396`, ccsession `:400`, hooks `:406`, templates `:411`, user setup `:416`. Exit 1 if any fails (`:419-431`). **It has no Codebase Memory phase** and by design never installs, upgrades or restores the native tool (`docs/user-guide/mcp-installation.md:24`; `tests/cli/test_update_command.py:407`). `update.sh` does not call it; `update.sh` uses `install --force`.

### 1.5 `superclaude doctor [--verbose]` (`main.py:473-512`, `src/superclaude/cli/doctor.py`)

`run_doctor` (`doctor.py:16-49`) runs five checks: pytest plugin (`:29`), agents (`:33`), skills (`:37`), configuration (`:41`), ccsession (`:44`). **There is no MCP check**, so doctor passes today with Codebase Memory, Serena or any MCP absent. Output and exit: prints each check (`main.py:495-501`); exits 1 if any check failed (`main.py:508-512`). Because `update.sh:10` runs it last under `set -e`, any new doctor check that fails turns `./update.sh` red. `make verify` also greps doctor's output for "SuperClaude is healthy" (`Makefile:42`).

### 1.6 `superclaude mcp [--servers NAME]... [--list] [--scope S] [--dry-run] [--uninstall] [--yes]` (`main.py:278-343`)

| Step | path:line | Notes |
|---|---|---|
| `--list`: rejects combination with other flags (click usage error), then `list_available_servers()` | `main.py:326-332`; `install_mcp.py:1198-1232` | "installed" is a substring scan of `claude mcp list` (`install_mcp.py:587-606`) |
| Otherwise `install_mcp_servers(...)`; prints message; `sys.exit(1)` when not successful | `main.py:334-343` | exit 1 on any failure |
| No `--servers` on a terminal: action menu (install / uninstall Codebase Memory / cancel), then server menu | `install_mcp.py:1262-1312` | non-interactive without `--servers` fails with an explicit message (`:1273-1277`) |
| Validate the whole selection against the registry before changing anything | `install_mcp.py:1313-1328` | registry = `MCP_SERVERS` (`install_mcp.py:40-109`): context7, playwright, **serena** (`:55-61`), morphllm, tavily, auggie, **codebase-memory-mcp** (`:101-108`), plus the special `airis-mcp-gateway` |
| `--uninstall` accepts **only** `--servers codebase-memory-mcp` | `install_mcp.py:1320-1324` | Serena and every other server have no uninstall path |
| Prerequisites for the selected servers only | `install_mcp.py:1345-1348`, `check_prerequisites` `:506-584` | Serena adds only a uv advisory (`:561-570`); Codebase Memory checks discovery and curl/bash (`:571-583`) |
| Per server: `install_mcp_server` | `install_mcp.py:1351-1366`, `:1010-1195` | Codebase Memory branches to the native function at `:1025-1028`. Every other server uses the generic path: exact-name drift check with `claude mcp get` (`:1050-1103`), then `claude mcp add --transport stdio --scope <scope> <name> -- <command>` (`:1142-1159`, run `:1178`) |
| Partial failure is reported and exits 1 | `install_mcp.py:1368-1373` | |

**Where Serena is installed/registered:** only by this generic `superclaude mcp --servers serena` path (registry command at `install_mcp.py:59`). `superclaude install` and `update.sh` never touch Serena; `main.py` contains no reference to it. In a Coder workspace Serena is installed and registered by Coder's own bundle script (section 4).

**Where `.claude/settings.json` fits:** the tracked project file `.claude/settings.json` only registers two project PreToolUse hooks (`reject-workspace-writes.sh`, `sc-recommend-phase0.sh`) and has no MCP content, so it needs no change for this migration.

### 1.7 Core docs installed to `~/.claude` that mention the servers (input for other workers)

`src/superclaude/core/CLAUDE.md:21` (serena row of the MCP table), `:112` (`mcp__serena__find_symbol` refresh-tool row); `core/HOW-WE-WORK.md:237`, `:327`, `:329` (`/sc:save`, `/sc:load` require Serena); `core/RESEARCH_CONFIG.md:26`, `:142`. `src/superclaude/hooks/hooks.json:47` registers `freshness-pre-edit.sh` on a matcher that lists four `mcp__serena__*` tools. On a Coder workspace the core `CLAUDE.md` does not reach the user: Coder's `ironclaude/install.sh` saves `~/.claude/CLAUDE.md` before `superclaude install` and restores it byte for byte afterwards (`catalogue/ironclaude/install.sh:44-66`, `:112-125`).

## 2. Extension point for a new required codegraph phase

### 2.1 What codegraph looks like to an installer (README facts, not run here)

- Ships as a standalone bundle via `curl -fsSL .../install.sh | sh` ("No Node.js required"), or as `npm i -g @colbymchenry/codegraph` (README lines 75-96).
- `codegraph install` configures every agent it detects (Claude Code, Cursor, Codex CLI, opencode, and others) account-wide (README 102-108). `codegraph uninstall` reverses that and removes the CLI; `--keep-cli` keeps the CLI; project indexes under `.codegraph/` are left (README 129-139). `codegraph upgrade` self-updates (README 5, 96).
- The MCP server is `codegraph serve --mcp`. Per project, `codegraph init` creates `.codegraph/` and builds the graph (README 110-117). A file watcher keeps it in sync while the MCP server runs (README 125-127, 287-305).
- Consequence for the installer: this is the same shape as Codebase Memory (native binary + upstream "configure my agents" command), not the shape of a pinned `npx` server like Tavily. Whether to let upstream `codegraph install` do the agent wiring (account-wide, like the Codebase Memory upstream script) or to register only the exact user-scope entry with `claude mcp add-json` (the narrower pattern at `install_mcp.py:775-786`) is a design choice for the codegraph install worker. UNVERIFIED: the exact registration command line and whether the standalone installer edits shell profiles.

### 2.2 Existing seams, in the order a new phase touches them

| Seam | path:line | What to reuse or add |
|---|---|---|
| Registry entry | `install_mcp.py:40-109` (Codebase Memory entry `:101-108`) | add a `codegraph` entry so `superclaude mcp --list`, the interactive menu (`:1235-1240`) and `--servers codegraph` work without more code. Selection validation (`:1313-1319`), prerequisites (`:1345-1348`) and the install loop (`:1351-1366`) are already generic |
| Per-server dispatch | `install_mcp.py:1025-1028` | add the same early branch that routes the server name to its native function (Codebase Memory does exactly this) |
| Phase function | model on `install_codebase_memory_mcp` (`install_mcp.py:815-913`) | same contract `(success: bool, message: str)`, `scope`/`dry_run` keywords, platform gate, `claude --version` gate, acquire, exact user-scope registration, verify, restore on failure |
| Registration helpers | `read_user_mcp_entry` (`:714`, already takes a name), `_run_registration_command` (`:766`), `_native_registration_matches` (`:757`, hard-codes `args == []`), `_add_user_native_entry` (`:775`), `_restore_user_native_entry` (`:789`), `_cleanup_user_native_registration` (`:916`) | the last four hard-code `codebase_memory.BINARY_NAME` (`:781`, `:790`, `:803`, `:811`, `:917`, `:930`, `:939`) and `_native_registration_matches` hard-codes empty args. Making them take a server name and an expected args list is the one small refactor this phase needs, because codegraph is started as `codegraph serve --mcp`, not with no arguments |
| Acquisition helper | `install_codebase_memory.py` (759 lines: discovery `:569-608`, acquisition `:611-749`, receipt `:187-241`, bounded subprocess `:469-519`) | copy the reuse-first shape (`:643-650`: use a runnable executable on PATH, never replace it). That branch is what lets Coder bake the binary into the image and keep `superclaude install` offline (section 4). Do not copy the 759-line receipt machinery unless the removal rules in section 3 need it |
| Phase call and exit | `main.py:254-262` and `:264-275` | add a second block after it and one more `or not <flag>` term in the exit condition |
| `install --list` | `main.py:161-186` | add a codegraph status block (read-only; exit stays 0) |
| `doctor` | `doctor.py:26-44` | optional: add a `_check_codegraph` returning the same `{name, passed, details}` dict. A failed check makes `./update.sh` exit 1 at `update.sh:10` |
| Prerequisite check | `install_mcp.py:571-583` (Codebase Memory block) | copy for codegraph's own prerequisites (curl, or node/npm if the npm route is chosen) |
| Tests that pin the phase | `tests/cli/test_update_command.py:28` (`_NATIVE_INSTALLER` patch target), `:254-277` (phase is mandatory, runs last, earlier phases kept), `:345-370` (`--force` is not forwarded) | mirror these for the codegraph phase |

### 2.3 Patterns that do NOT fit as an unattended required phase

- `requires_global_binary` / `ensure_global_binary` (Auggie, `install_mcp.py:87-93`, `:192-233`): it calls `click.confirm("Install ... globally now?")` at `:214`. Coder runs `superclaude install` with `</dev/null` (`catalogue/ironclaude/install.sh:120`), so a prompt cannot be answered. It would need a non-interactive mode first.
- Pinned `npx` registry command (Tavily, `install_mcp.py:71-80`): nothing is installed, so there is nothing to check offline, and whether `npx @colbymchenry/codegraph serve --mcp` is a supported way to start it is UNVERIFIED.

### 2.4 Minimum code shape (seams only, not a design)

```python
# install_mcp.py, beside install_codebase_memory_mcp (:815)
def install_codegraph_mcp(*, scope: str = "user", dry_run: bool = False) -> tuple[bool, str]:
    # 1. platform + `claude --version` gate         (copy :819-843)
    # 2. reuse a runnable `codegraph` on PATH, else acquire it   (shape of install_codebase_memory.py:643-650)
    # 3. exact user-scope stdio entry: command=<abs path>, args=["serve", "--mcp"]   (helpers :714, :775, :789 with a name + args parameter)
    # 4. re-read ~/.claude.json to verify; restore the previous entry on failure     (copy :896-913)

# main.py install(), after the Codebase Memory block (:254-262)
click.echo("\nInstalling codegraph (required user-level phase)...")
codegraph_success, codegraph_message = install_codegraph_mcp(scope="user")
click.echo(codegraph_message)
# ... and `or not codegraph_success` in the exit condition at :264-274
```

`superclaude update` needs no change: `update.sh` reaches the new phase through `superclaude install --force` (`update.sh:8`), and `update` is documented never to touch the native tool (`docs/user-guide/mcp-installation.md:24`).

### 2.5 Constraints the new phase inherits from Coder (section 4 has the sources)

- Whole `superclaude install` is cut off at 60 s by Coder (`catalogue/ironclaude/install.sh:120`); user setup already budgets 30 s of it for network (`install_user_setup.py:31-35`).
- The Coder contract test runs the real install with `--network=none` (`.github/workflows/coder-ci-aidev02-contract.yml:1221`), so any download path fails there. The binary must come from the image (PATH reuse) or the phase must not need the network.
- Each `claude mcp ...` call inside `_run_registration_command` has a 60 s timeout (`install_mcp.py:769`); Coder measured about 0.25 s for a real `claude mcp add` (`catalogue/mcp-bundle-core/install.sh:21`).

## 3. Removal of previously installed servers on existing workspaces

### 3.1 Is there an existing migration or cleanup mechanism?

**No general one.** I searched `install_{core,commands,agents,skills,skill,templates,hooks,ccsession,user_setup}.py` for `stale|legacy|migrat|prune|obsolete|orphan|unlink|rmtree|remove_|cleanup`. The only hits are narrow special cases:

| Hit | path:line | What it does | Reusable for this migration? |
|---|---|---|---|
| Skill served by a command is deleted | `install_skills.py:89-98` | removes `~/.claude/skills/<name>` when a `/sc:` command now covers that skill | No: only for skills that have a matching command |
| Forced skill reinstall | `install_skill.py:46-48` | removes the existing copy of a skill that is about to be re-copied | No: only a skill that is still shipped |
| Legacy ccsession hook command | `install_hooks.py:90-110` | `_CCSESSION_LEGACY` regex lets a refresh recognise and replace an old ccsession command | Pattern only: shows how "this command used to be ours" is matched |
| ccsession name migration | `install_ccsession.py:87-98` | runs the skill's own `--migrate-names` | No: ccsession-specific |
| Legacy hook script copy | `install_hooks.py:80`, `:226-228` | deposits `session-init.sh`; copies, never deletes | No |

What this means on an existing workspace after the new IronClaude is installed:

- Core files, commands, agents and templates are **copy-only**: `install_core.py:62-73`, `install_commands.py:50-63` and the agent/template installers never delete a file that is no longer shipped. Removed `/sc:` commands and agents therefore stay in `~/.claude/commands/sc/` and `~/.claude/agents/` until something deletes them.
- Skills are replaced per shipped skill (`install_skill.py:47-48`); a skill removed from `src/` stays in `~/.claude/skills/`.
- Hook registrations in `~/.claude/settings.json` are **add or refresh only** (`install_hooks.py:341-436`). Under `--force` a registration whose command still exists is replaced at its position (`:397-431`), so editing the `mcp__serena__*` matcher at `hooks.json:47` would be applied by `./update.sh` (which uses `--force`) but not by a plain `superclaude install` (skipped at `:393-395`). A registration whose command was dropped from `hooks.json` is never removed.
- Settings defaults only add missing keys and never remove (`install_user_setup.py:150-164`); `user_settings_defaults.json` has no MCP keys (top-level keys at lines 10, 28, 36 are `env`, `enabledPlugins`, `extraKnownMarketplaces`).
- MCP registrations in `~/.claude.json` are removed by exactly one path today: `superclaude mcp --uninstall --servers codebase-memory-mcp [--yes]` (`main.py:299-309`, `install_mcp.py:1320-1343`). Serena has none.
- Nothing in `update.sh`, `install` or `update` calls that uninstall path.

### 3.2 Where a cleanup could be triggered (seams)

| Trigger | Reaches existing dev workspaces? | Reaches Coder workspaces? | Verdict |
|---|---|---|---|
| New "retire old MCP servers" step inside `superclaude install`, after the codegraph phase (`main.py:254-262` area) | Yes: `update.sh:8` runs `install --force` | Yes: `catalogue/ironclaude/install.sh:120` runs `superclaude install` once per new IronClaude SHA | **Recommended seam**; the only trigger both paths already run |
| New step in `update.sh` | Yes | No (Coder never runs `update.sh`; no hit in `templates/`, `.github/`, `scripts/`) | Reject; also `update.sh` is pinned to four commands by `tests/cli/test_update_script.py:13-18` |
| New step in `superclaude update` | Not through `update.sh` | No | Reject; `update` is documented never to touch native/MCP state (`docs/user-guide/mcp-installation.md:24`) |
| User runs `superclaude mcp --uninstall ...` by hand | Yes, if they know to | No | Keep as the manual escape hatch; not a migration |
| Coder startup scripts | n/a | Yes | Required for the Coder-owned pieces (section 4), because IronClaude does not own the Coder image binary or Coder's bundle installer |

Two facts that change what an automatic cleanup is allowed to do:

1. **On Coder the existing uninstall command refuses.** The Codebase Memory binary there is the image copy `/usr/local/bin/codebase-memory-mcp` (`Dockerfile.coder:350`), not `~/.local/bin/...` with a receipt. `preview_codebase_memory_removal` returns state `external` when the canonical path is missing but another PATH entry exists (`install_codebase_memory.py:284-291`), and `uninstall_codebase_memory_mcp` returns `(False, preview.message)` for any state other than `ready`/`missing` before it reaches registration cleanup (`install_mcp.py:957-959`). So today the user-scope registration (which test-57 asserts exists, `test-57-catalogue-configure.sh:243`) would be left in place pointing at a binary that the image is about to stop shipping. A codegraph-era cleanup needs a registration-only branch for the `external` case. The registration-only helper already exists and is exact: `_cleanup_user_native_registration` (`install_mcp.py:916-948`), used today for the `missing` state (`:987-994`).
2. **Serena is not IronClaude-installed anywhere IronClaude can prove.** `superclaude install` never installs it; the registry runs it through `uvx` on demand (`install_mcp.py:59`), so there is no binary or receipt to remove. In Coder it is a `uv tool install serena-agent==1.7.0` done by Coder's own bundle script (`catalogue/mcp-bundle-core/install.sh:148-170`) and re-registered on every start (`:90-119`). IronClaude can only remove the user-scope registration; Coder must remove the bundle's install, markers and re-registration.

### 3.3 Safety rules the existing Codebase Memory removal follows (keep them)

| Rule | Where | Keep for codegraph-era cleanup? |
|---|---|---|
| User scope only; other scopes are never changed and the message says so | `install_mcp.py:955-956`, `:945-947`; `main.py:292` | Yes |
| Exact top-level user entry only: parse `~/.claude.json` directly, reject duplicate keys, treat any read or parse failure as "unknown" and do nothing | `install_mcp.py:714-754`, `:960-965` | Yes (reuse `read_user_mcp_entry`) |
| Remove through the Claude CLI (`claude mcp remove <name> --scope user`), never by editing the JSON; then re-read to verify absence; report "possible partial removal" otherwise | `install_mcp.py:925-944` | Yes |
| Ownership proof before touching a binary: only a sha256 identity receipt written by IronClaude's own acquisition authorises removal; a pending marker covers an interrupted acquisition; receipt and marker must be private, owned, single-link regular files | `install_codebase_memory.py:81-123`, `:187-210`, `:297-304`, `:345-351` | Yes for any binary IronClaude itself installs (codegraph, if IronClaude acquires it). Not applicable to the Coder image copy |
| External or ambiguous executables are never removed automatically; the message tells the user to use the original mechanism | `install_codebase_memory.py:284-291`, `:298-304`; `install_mcp.py:957-959` | Yes: keep for binaries; for registration-only cleanup see 3.2 item 1 |
| Explicit consent: interactive confirm defaults to No; non-interactive needs `--yes`; `--dry-run` previews with no change | `install_mcp.py:981-986`, `:1329-1343`; `main.py:304-309` | **Tension**: an automatic step inside `install` has no prompt. Recommended narrow subset below |
| Never replace or restore an entry that carries `env` or `headers` (a restore would put secrets on a command line) | `install_mcp.py:867-873` | Yes: skip and report rather than remove, or remove only through the CLI |
| Roll back the previous registration if add/verify fails; never overwrite a third party's concurrent edit | `install_mcp.py:789-812`, `:874-913` | Yes |
| Never echo CLI output or exception text (may contain secrets) | `install_mcp.py:766-772`, `:753` | Yes |
| Bounded, supervised subprocesses with fixed timeouts | `install_codebase_memory.py:27-31`, `:399-519` | Yes |
| Indexes are retained; the adjacent updater is left; IronClaude does not erase companion or cache files (upstream's own `uninstall -y --dir=...` is what removes companions) | `install_codebase_memory.py:74-78`, `:352-355`, `:371` | Yes: do not delete `.codegraph/` or Codebase Memory indexes, and do not delete Serena memories |
| Linux amd64/arm64 only | `install_mcp.py:486-496` | Yes for binary removal; registration-only cleanup is platform-neutral |
| `update` never restores or removes native state | `docs/user-guide/mcp-installation.md:24`; `tests/cli/test_update_command.py:407` | Yes: keep cleanup in `install`, not `update` |

Recommended narrow automatic subset (non-binding; the Phase 1 planner owns the final scope): during `superclaude install` remove only (a) the exact user-scope `codebase-memory-mcp` entry and (b) the exact user-scope `serena` entry, each only when the entry equals what IronClaude or Coder registered (for Serena the argv at `install_mcp.py:59`; for Codebase Memory `_native_registration_matches`), via the Claude CLI, verified, and non-fatal to the phase result unless the lookup itself fails. Binary removal with a matching receipt, companion assets, indexes and Serena memories stay behind an explicit `superclaude mcp --uninstall` with consent. Rationale: it satisfies "a fresh or updated workspace has neither registered" without making an unprompted account-wide upstream uninstall.

### 3.4 Stale Codebase Memory/Serena material the cleanup step cannot see without new work

- `~/.claude/commands/sc/{save,load}.md`, any Serena-specific agents or skills: remain until deleted (copy-only installers, 3.1). A "retired assets" list (names IronClaude used to ship) plus a delete-if-present step is the missing seam; no such list exists.
- `hooks.json:47` matcher and `freshness-pre-edit.sh` behaviour: refreshed only under `--force` (3.1).
- On non-Coder machines the upstream Codebase Memory installer may have added companion skills, agents, hooks and instructions under `~/.claude`, `~/.codex` and `~/.config/opencode` (`install_mcp.py:499-503`, `install_codebase_memory.py:667-669`). IronClaude never audits them (`install_mcp.py:966`). On Coder they do not exist because the upstream installer does not run (`test-57-catalogue-configure.sh:244`).

## 4. Coder touchpoints

All paths below are in `IronbellyOrg/Coder` at commit `e25f787c` and are relative to the repo root; `T/` abbreviates `templates/VSCode-AIDev02/`. This is a list of facts for a handoff prompt, not a Coder implementation plan. Two hits that look relevant but are not: the legacy template `templates/VSCode-AIDev01/` has no Codebase Memory or Serena reference and installs upstream `SuperClaude` from PyPI (`T1/scripts/install-superclaude.sh:158`, where `T1` is `templates/VSCode-AIDev01`), and Coder has no `superclaude update` or `update.sh` call anywhere in `templates/`, `.github/` or `scripts/`.

### 4.1 Image (what is baked, what is pinned)

| path:line | What it does |
|---|---|
| `T/Dockerfile.coder:323-351` | SpecStory layer that also bakes **codebase-memory-mcp v0.12.1** to `/usr/local/bin/codebase-memory-mcp` (per-arch asset and sha256 `:342-343`, download `:346`, checksum `:347`, `install -m 0755` `:350`). The comment at `:324-328` states the purpose: IronClaude's required Codebase Memory step must reuse a PATH executable instead of running the upstream installer, which needs network and appends a PATH line to `~/.bashrc`; kept in this layer to stay inside the Sysbox layer budget; "deliberately outside INSTALL_MATRIX" |
| `T/Dockerfile.coder:370-376` | **`ARG IRONCLAUDE_GIT_SHA=55d4030874676c664eb640b60c92fe6cc9bfeb52`** (`:375`) and `ENV` (`:376`). The comment at `:371-372` says this ARG is the sole pin authority and that `ironclaude-upstream-monitor.yml` rewrites only that line. `55d40308` is the current IronClaude merge commit "Merge pull request #321", so Coder is pinned to the pre-migration master |
| `T/Dockerfile.coder:379` | `COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /usr/local/bin/` (uv also serves Serena's `uv tool install` at boot) |
| `T/Dockerfile.coder:381-431` | IronClaude bake: validates the 40-hex SHA (`:385-389`), derives the install URL once (`:393`), writes `/etc/aidev02/ironclaude-provenance` mode 0444 (`:395-399`), asserts artifact equals ARG (`:403-408`), installs with `uv tool install` (`:417-419`) into `/opt/uv/tools` so user 1000 can run it, and checks `command -v superclaude && superclaude --version` as `coder` (`:431`) |
| `T/Dockerfile.coder:572-578` | Seeds `~/.claude/CLAUDE.md` from `T/workspace_defaults/CLAUDE.md` (copied only if absent at startup). It has no Serena or Codebase Memory text |
| `T/Dockerfile.coder:670` | `COPY catalogue /catalogue`: the catalogue installers below ship inside the image |
| (no hit) | codegraph is not baked anywhere today; `grep -ri codegraph` over the live tree finds nothing |

### 4.2 IronClaude install on a workspace (`ironclaude` catalogue slug)

| path:line | What it does |
|---|---|
| `T/catalogue/ironclaude/install.sh:23`, `:26-29`, `:32-35`, `:88-90` | reads `git_sha` from the provenance file; "configured" means `~/.aidev/installed/ironclaude.configured == git_sha` plus `commands/sc/help.md` plus IronClaude hook entries; a configured workspace is a no-op, so **an existing workspace reruns `superclaude install` only when the image's SHA changes** |
| `:91-95` | when a previous configured SHA exists and differs, passes `--force` (this is the "update" path for existing workspaces) |
| `:120-123` | **`timeout 60 superclaude install ... </dev/null`**; non-zero exit prints FAIL and `exit 1` (marker not written). Anything that makes `superclaude install` exit 1, including the required Codebase Memory phase, fails this slug |
| `:44-66`, `:112-125` | saves and restores `~/.claude/CLAUDE.md` (symlink-aware) so IronClaude never overwrites the Coder seed |
| `:68-86`, `:103-107`, `:127-134` | keeps a symlinked `settings.json` a symlink and fails if pre-existing hook entries were dropped |
| `:141-149` | writes `.configured` and the install marker only after verification |
| `:152-153` | tells a running Orca to repoint its Claude command at `ccsession-orca` |
| `T/catalogue/ironclaude/manifest.yaml:4`, `:24-25` | disposition `image-baked`; health command `superclaude --version` only (no MCP check) |
| `T/catalogue/profiles.yaml:18` | the `orca` profile (default) lists `claude-code, orca, spec-story, ironclaude, bmad, mcp-bundle-core` |
| `T/scripts/startup.sh:1079-1088` | per-slug time bound: `ironclaude` and `mcp-bundle-core` get 75 s, others 30 s; slugs are visited in `LC_ALL=C` sort order (`:693`, `:1182`), so `ironclaude` runs before `mcp-bundle-core` |
| `T/scripts/startup.sh:892-938` (`aidev_cat_install`), `:945-960` (`aidev_cat_unmark`) | watchdog-bounded installer runner; and the marker remover used when a slug leaves the selected profile (removes only `<slug>` and `<slug>.*` regular files or symlinks) |
| `T/scripts/lib/spec2-health.sh:76`, `:101-111`, `:161-170` | health requirements for `ironclaude` are `command hook provenance`; no Codebase Memory or codegraph observation. A failed install leaves `Not-Installed` or `Installed-not-Configured` |
| `T/orca/runtime.mjs:299`, `:315`, `:541` | Orca's Claude command is IronClaude's `ccsession-orca`; the IronClaude installer calls `runtime.sh claude-command` |

### 4.3 Serena (Coder installs and registers it itself, independent of IronClaude code)

| path:line | What it does |
|---|---|
| `T/catalogue/mcp-bundle-core/install.sh:1-5` | header: registers Auggie, Serena, Tavily, Context7 at user scope; "Exit 0 = all three present and all four registered, 2 = otherwise" |
| `:17-20` | pins `AUGGIE_PIN=0.36.0`, `SERENA_PIN=1.7.0`, `TAVILY_PIN=0.2.22` (comment at `:17` says it mirrors "IronClaude MCP_SERVERS at the image pin"; this is a hand-copied text coupling, not an import) |
| `:67-119` | registration loop: for each of the four names, if absent runs `claude mcp add --transport stdio --scope user <name> ...` with a 5 s timeout; Serena's argv is at `:74-75`. **Existing entries are never removed or overwritten** (comment `:68-70`, behaviour `:101-107`) |
| `:128-131`, `:148-170` | Serena install: `uv tool install --python <py> serena-agent==1.7.0`, verified with `serena --help`; failure counts toward `fails` |
| `:189-201` | cache warm: `uvx --from serena-agent==1.7.0 serena --help` (`:197`) |
| `:215-229` | exit 2 if any of the three servers is missing or fewer than four are registered; the install marker `~/.aidev/installed/mcp-bundle-core` and the per-server marker `mcp-bundle-core.serena` (`:14`) are written only after verification |
| `T/catalogue/mcp-bundle-core/manifest.yaml:7`, `:9-13`, `:21-29`, `:40` | user-facing text lists Serena; says `claude mcp remove <name>` "does not stick" because the bundle re-registers on the next start; health command `auggie --version && serena --help && npx --yes tavily-mcp@0.2.22 --help` |
| `T/catalogue/mcp-bundle-core/module.tf:1`, `T/parameters.tf:110`, `T/README.md:310`, `:418`, `T/catalogue/README.md:27`, `SECURITY.md:231` | descriptive text naming Serena |
| `T/scripts/lib/spec2-health.sh:79`, `:145-153` | the bundle's required-names set is `auggie serena tavily context7`; observation lists the registered names found in `~/.claude.json` |
| `T/workspace_defaults/bashrc.skel:88` | `alias serena='uvx --from "git+https://github.com/oraios/serena" serena'` in every new shell |
| `.serena/project.yml`, `.serena/memories/` | Serena project config and a memory file for the Coder repo itself (developer tooling, not shipped in the image). `.github/contract-tests/test-49-spec2-evidence.sh:307` lists `.serena/project.yml` in its hashed evidence file set |

### 4.4 Tests that assert Codebase Memory or Serena state (these fail in Coder CI if the behaviour changes)

| path:line | What it asserts |
|---|---|
| `.github/contract-tests/test-57-catalogue-configure.sh:243` | **`.mcpServers["codebase-memory-mcp"].command == "/usr/local/bin/codebase-memory-mcp"`** in `~/.claude.json` after the real `ironclaude/install.sh` ran |
| `:244` | the upstream Codebase Memory installer did not run (`~/.local/bin/codebase-memory-mcp` absent) |
| `:6-13`, `:226-231`, `:228` | runs the baked `/catalogue/<slug>/install.sh` as user `coder`, expecting exit 0 for `bmad`, `ironclaude`, `spec-story` with the **real baked `superclaude`** |
| `.github/workflows/coder-ci-aidev02-contract.yml:1221` | wires test-57 with `--network=none,--user=0`: **no network at all** during `superclaude install` |
| `test-57-catalogue-configure.sh:292-298`, `:309-314` | a faked SHA change must run `superclaude install --force`; a self-heal run must run it without `--force`; both must keep the user's `deniedMcpServers` |
| `:488-499` | registry oracle for the bundle: four exact `claude mcp add` argvs including Serena (`:496`) and the expected `~/.claude.json` object (`:499`); hard-coded in the test, not read from IronClaude |
| `:602-603` | the bundle `install.sh` must never mention `superclaude mcp`, `mcp remove|list|get` or `airis` (so the bundle cannot cleanly remove a server) |
| `:613-636` | fresh and repeat bundle runs end `healthy` / `Configured`; Serena aligned to 1.7.0 (`:616`) and warmed (`:618`) |
| `.github/contract-tests/test-startup-boot.sh:1978-2066` | in-profile **end-use proof of the bundle is a real Serena MCP handshake** (`setsid serena start-mcp-server`, `:2001`; PASS record `:2057`). If Serena goes, this proof needs another server or it must be dropped |
| `test-startup-boot.sh:1197-1211`, `.github/contract-tests/test-46-catalogue-health.sh:1171-1234` | reprofile from `ai-pair-programming` to `orca` removes the `mcp-bundle-core` marker and its three side markers (`.auggie`, `.serena`, `.tavily`) |
| `test-startup-boot.sh:201`, `:219`, `:1619`, `:1643`, `:1796-1802` | slug enums include `mcp-bundle-core`; comment names Serena in the orca slug set; the 75 s budget is "sized to the 60 s superclaude install limit" |
| `.github/contract-tests/test-49-spec2-evidence.sh:31`, `:314-315`, `:563` | expected slugs and hashed files include the bundle's `install.sh` and `manifest.yaml` |
| `.github/contract-tests/test-19-catalogue-cli-presence.sh:635-640` | `mcp-bundle-core` is marked "BLOCKED runtime dependency" on the MCP handshake record |
| `.github/contract-tests/test-60-llm-gateway-env.sh:174-176` | parses `AUGGIE_PIN=` out of the bundle `install.sh` and compares it to the Dockerfile; keep that line's shape if the file is edited |
| `.github/contract-tests/test-26-aienv-completeness.sh:83` | uses the word `serena` as a non-secret name in a classifier self-test; unaffected |
| `.github/contract-tests/test-48-ironclaude-provenance.sh:4-9`, `:175-184` | exactly one 40-hex IronClaude SHA may appear in the Dockerfile, on the `ARG` line |

### 4.5 Pin bump automation and probes

| path:line | What it does |
|---|---|
| `.github/workflows/ironclaude-upstream-monitor.yml:10-12` | runs daily at 06:00 UTC and on manual dispatch |
| `:41` | reads IronClaude `master` HEAD with `gh api repos/IronbellyOrg/IronClaude/commits/master`; fetch failure exits neutral with a warning (`:44-59`) |
| `:80-82`, `:107`, `:114` | reads the pin with `grep -m1 -oE '^ARG IRONCLAUDE_GIT_SHA=[a-f0-9]+'`; if HEAD differs, branch `auto/ironclaude-bump-<sha7>` |
| `:131-134` | **the bump edits only the `ARG IRONCLAUDE_GIT_SHA=` line**, so an auto bump PR cannot carry test or script changes |
| `:145-276` | "proof": in a clean base-image container installs the candidate with `uv tool install` and runs `superclaude --version` (`:246-256`). **It does not run `superclaude install`**, so it cannot see a failing MCP phase |
| `:278-340` | proof pass opens a ready PR (`:307-325`); proof fail opens a draft labelled `needs-build-proof` (`:330-340`). The comment at `:104` notes bot PRs get approval-gated CI |
| `.github/workflows/ironclaude-pipx-probe.yml:94-103`, `.github/contract-tests/ironclaude-install-probe.sh:21`, `:33`, `:41` | manual install-boundary probe; also only `--version` |
| `.github/workflows/coder-ci-aidev02-contract.yml:19-24`, `:1219`, `:1221` | the contract workflow triggers on changes to the monitor and runs test-48 and test-57 in the built image |
| `.github/coder-automation-routes.yaml:197-206`, `:223-` | route inventory entries for the monitor and the probe |
| `.github/workflows/coder-ci-orca-proof.yml:276`, `:532`, `:741` | in-session proof row `ironclaude` is `/sc:help` registration and invocation; it does not use Codebase Memory or Serena |

### 4.6 Workspace-side refresh paths (how an existing workspace changes)

- Existing workspaces change only when a new template version (new image with a new `IRONCLAUDE_GIT_SHA` or new catalogue scripts) is pushed and the workspace restarts; startup then reruns each selected slug (`T/scripts/startup.sh:1079-1088`). The `ironclaude` slug then runs `superclaude install --force` (`install.sh:91-95`).
- `scripts/refresh-all-workspaces:1-14` is an operator-side fan-out over `refresh-env` for environment defaults; it is not an IronClaude updater. UNVERIFIED: whether any operator path exists to rerun the slugs without a restart.
- The user-scope registrations live in the workspace home (`~/.claude.json`), which survives image changes. So removing a binary or a bundle line in the image does not remove existing registrations.

### 4.7 For the handoff: where Coder agents should research "keep new projects indexed"

Not investigated here beyond pointers. codegraph needs `codegraph init` per project (README lines 110-117) and then self-syncs while its MCP server runs (README 125-127). Places in Coder that create or clone project directories and are candidate hooks: the BMad seed repo (`T/scripts/lib/spec2-health.sh:113`, `~/.aidev/status/seed-repo-path`) and the `~/workspaces` directory handling (`.github/contract-tests/test-59-home-workspaces-dir.sh`). UNVERIFIED which of these (or a git template/hook, or a Claude Code `SessionStart` hook) is the right one.

## 5. Ordering constraints between an IronClaude release and a Coder pin bump

"Release" here means a commit on IronClaude `master`: Coder pins a master SHA (`Dockerfile.coder:375`) and its monitor bumps to every new master HEAD, not to tags (`ironclaude-upstream-monitor.yml:3-5`, `:41`, `:107`).

### 5.1 Facts that drive the ordering

1. The pinned IronClaude's `superclaude install` currently **requires** Codebase Memory and gets it from the image binary (`main.py:254-262`; `install_codebase_memory.py:643-650`; `Dockerfile.coder:350`).
2. Coder CI runs the real baked `superclaude install` with **no network** (`coder-ci-aidev02-contract.yml:1221`) and asserts the Codebase Memory registration (`test-57-catalogue-configure.sh:243-244`).
3. Real workspaces bound `superclaude install` at 60 s (`ironclaude/install.sh:120`); a missing-binary acquisition in the current IronClaude can take up to 60 s download plus 300 s install (`install_codebase_memory.py:27-28`).
4. The auto-bump PR changes one line (`ironclaude-upstream-monitor.yml:131`) and its proof only runs `superclaude --version` (`:246-256`), so a bump PR can be opened ready and still fail the contract workflow on test-57.
5. Coder's Serena is installed, registered and tested by Coder alone (`mcp-bundle-core/install.sh:90-170`, `test-57:488-499`, `test-startup-boot.sh:1978-2066`); no IronClaude code runs it.

### 5.2 What breaks in Coder CI in each order

| Order | What happens | Evidence |
|---|---|---|
| **A. IronClaude merges first (Codebase Memory phase removed, Serena removed, codegraph phase added), Coder pin is bumped before Coder changes** | (1) test-57 line 243 fails: the new IronClaude no longer registers `codebase-memory-mcp`. (2) If the new IronClaude requires a codegraph executable that the image does not have, its acquisition cannot download under `--network=none`, `superclaude install` exits 1, `ironclaude/install.sh` exits 1 (no marker), and test-57's `expect_rc ... 0` fails for `ironclaude` (`:228`); on a real boot the slug is not installed (`spec2-health.sh:163-169`). (3) Serena is unaffected: the bundle keeps installing and registering it, so Coder CI stays green on Serena but Serena is not "removed" | `test-57:243`, `:228`; `ironclaude/install.sh:120-123`; `install_codebase_memory.py:697-706`; `coder-ci-aidev02-contract.yml:1221` |
| **B. Coder removes the baked Codebase Memory binary (or its test) first, pin still old** | The old IronClaude still requires Codebase Memory. With no PATH executable it tries the upstream download; offline CI fails (`superclaude install` exit 1, slug fails, test-57 `:243` fails); on a real boot the download and install may exceed the 60 s bound. The image build itself does not break (nothing at build time runs `superclaude install`), so the failure shows in the contract tests and at first boot | `Dockerfile.coder:342-351` (what would be removed), `install_codebase_memory.py:643-713`, `ironclaude/install.sh:120` |
| **C. Coder removes Serena from the bundle first, pin still old** | Safe for the pinned IronClaude: `superclaude install` never touches Serena. Coder-side tests must change together with the bundle (they hard-code Serena: `test-57:496-499`, `:616`, `:618`; `test-startup-boot.sh:1978-2066`; `spec2-health.sh:79`, `:151`; `manifest.yaml:40`; `test-46:1171-1234`) | section 4.3 and 4.4 |
| **D. Coder adds codegraph to the image first (additive), keeps Codebase Memory and Serena, pin still old** | Safe: the old IronClaude ignores codegraph. This is the only change that can precede IronClaude without breaking anything | `Dockerfile.coder:323-351` is untouched; new layer only |
| **E. Phases land on IronClaude `master` separately (Phase 1 removal alone, then Phase 2 install)** | The monitor opens a bump PR for every new master commit within a day, including an intermediate one where `superclaude install` installs neither server and no codegraph. That intermediate state passes the monitor's proof (`--version` only, `:246-256`), so the PR opens ready, then fails test-57 `:243`. Merge it by mistake and every rebuilt image lacks the registration | `ironclaude-upstream-monitor.yml:10-12`, `:131`, `:246-256`, `:307-325` |

### 5.3 Safe sequence (derived from the table; the Coder owners decide the final plan)

1. **Coder first, additive only (D):** bake the codegraph executable into the image at a path on PATH, with a pinned version and sha256 like Codebase Memory (`Dockerfile.coder:342-351`). No other Coder change.
2. **Coder second, make the tests pin-agnostic:** change test-57 `:243-244` so it accepts either the old pin (Codebase Memory registered) or the new one (codegraph registered, Codebase Memory absent), because the auto-bump PR can only edit the `ARG` line (`ironclaude-upstream-monitor.yml:131`) and cannot carry test edits.
3. **IronClaude, one merge unit:** land removal (Phase 1) and the codegraph phase (Phase 2) on `master` together so no intermediate commit exists for the monitor to bump to (E). The codegraph phase must reuse a PATH executable and make no network call when one exists (2.2, 2.5).
4. **Coder pin bump:** let the monitor PR (or a hand-made bump) go through contract CI; confirm test-57 and test-startup-boot pass on the new SHA.
5. **Coder third, removals:** remove the baked Codebase Memory layer content (`Dockerfile.coder:324-351`), remove Serena from the bundle together with its tests, health sets, manifest text, README text and the `serena` alias (4.3, 4.4), and add the workspace-side cleanup for existing registrations and markers. This must come after step 4: removing the binary earlier is order B.
6. **Existing workspaces:** reach the new state at their next restart after the new image is deployed, because `ironclaude/install.sh` reruns with `--force` when the SHA changes (`:91-95`). Coder's own cleanup of Serena (`uv tool uninstall serena-agent`, the `mcp-bundle-core.serena` marker, the registration) is not performed by IronClaude (3.2 item 2).

### 5.4 Things I could not confirm

- UNVERIFIED: whether the Coder contract workflow runs on bot-created bump PRs without a human approving it (the comment at `ironclaude-upstream-monitor.yml:104` says bot PRs get approval-gated CI; its full text was truncated in my read).
- UNVERIFIED: the real elapsed time of `superclaude install` on a Coder workspace today; only the 60 s bound and the 75 s slug budget are visible in code (`ironclaude/install.sh:120`, `startup.sh:1087`).
- UNVERIFIED: whether codegraph's standalone installer or `codegraph install` can run offline and without editing shell profiles; PATH-reuse of a baked binary avoids needing the answer.

## Decisions

No adversarial run was needed: each decision below is either forced by a verified constraint (a pinned test, the offline CI, the 60 s bound) or is a seam recommendation that the design owners can override. Nothing here was escalated to the user.

| # | Decision | Options considered | Method | Rationale |
|---|---|---|---|---|
| 1 | Put the new codegraph phase in `superclaude install` after the Codebase Memory block, and leave `superclaude update` and `update.sh` unchanged | (a) phase in `install`; (b) also in `update`; (c) extra command in `update.sh` | self | `update.sh:8` already runs `install --force`; `update` is documented never to touch native state (`docs/user-guide/mcp-installation.md:24`, `tests/cli/test_update_command.py:407`); `update.sh` is pinned to four commands (`tests/cli/test_update_script.py:13-18`); Coder runs only `superclaude install` (`ironclaude/install.sh:120`) |
| 2 | Model the codegraph phase on `install_codebase_memory_mcp` with a reuse-a-PATH-executable-first acquisition, not on `ensure_global_binary` or an `npx` registry command | (a) native-binary pattern; (b) `requires_global_binary` (Auggie); (c) `npx` registry entry (Tavily) | self (non-binding; the codegraph install worker owns acquisition) | (b) prompts via `click.confirm` (`install_mcp.py:214`) and Coder passes `</dev/null`; (c) installs nothing to verify offline and `npx` start-up is UNVERIFIED; (a) matches codegraph's own shape (standalone bundle plus an agent-configuring `install` command) and PATH reuse is what keeps Coder CI offline |
| 3 | Parameterise the registration helpers by server name and expected args rather than copying them | (a) parameterise `_add_user_native_entry`, `_restore_user_native_entry`, `_cleanup_user_native_registration`, `_native_registration_matches`; (b) duplicate them for codegraph | self | they hard-code `codebase_memory.BINARY_NAME` and empty args (`install_mcp.py:757-763`, `:775-812`, `:916-948`); codegraph starts as `serve --mcp`; one parameterised copy also serves the cleanup in Decision 4 |
| 4 | Trigger cleanup of the old servers inside `superclaude install`, and recommend a narrow automatic subset (exact user-scope registrations of `codebase-memory-mcp` and `serena`, only when they match what IronClaude or Coder wrote); leave binaries, companions, indexes and Serena memories to explicit consented commands | (a) narrow registration-only; (b) full automatic upstream `uninstall -y` of Codebase Memory; (c) nothing automatic, manual only | self (non-binding; the Phase 1 planner owns scope) | (c) cannot meet "update or fresh workspace leaves both absent"; (b) is account-wide and prompt-free, which the existing code deliberately forbids (`install_mcp.py:981-986`); (a) keeps every safety rule in 3.3 and works for the Coder case where the binary is an unowned external copy (`install_mcp.py:957-959`) |
| 5 | Treat Coder's `/usr/local/bin/codebase-memory-mcp` as external: IronClaude must never delete it; the image removes it | (a) IronClaude deletes it; (b) leave to the Coder image | self | no receipt can exist for it (`install_codebase_memory.py:297-304`), and the existing rule is "external executables are never removed automatically" (`:284-291`) |
| 6 | Recommend the Coder-then-IronClaude-then-Coder order in 5.3 and that IronClaude phases 1 and 2 land on `master` as one unit | (a) IronClaude first; (b) Coder removal first; (c) additive Coder bake first (chosen) | self | only (c) never reaches a red state in the table in 5.2; the monitor bumps on every master commit (`ironclaude-upstream-monitor.yml:107`) and cannot carry test edits (`:131`) |
| 7 | Fetched Coder through `gh api .../tarball/main` into `/tmp`, not file by file through `contents/` | (a) tarball; (b) 692+ `contents` calls | self | `gh search code` returned `[]`; the tarball is the same read-only API, writes only under `/tmp`, and gives stable line numbers at one commit (`e25f787c`) |

## Open items for other workers (not decided here)

- Exact codegraph registration command and whether to use upstream `codegraph install` (account-wide) or an exact user-scope `claude mcp add-json` entry (section 2.1).
- Whether `superclaude doctor` should gain a codegraph check (it would make `./update.sh` fail when codegraph is absent: `update.sh:10`, `main.py:512`).
- A "retired assets" list so `install` can delete shipped-then-removed commands, agents, skills and hook registrations (section 3.4); none exists today.
- Which Coder mechanism initialises codegraph for newly created projects and worktrees (section 4.7).
