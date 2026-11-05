# E2E Test Guide — `MCP server management` (`5.0.0`)

- **Capability:** `superclaude mcp` previews, lists and registers the optional MCP servers (context7, playwright, morphllm-fast-apply, tavily, auggie, codegraph, and the opt-in litellm gateway) with Claude Code, and rejects the servers and flags removed in 5.0.0.
- **Audience:** end user / operator
- **Source of truth:** `src/superclaude/cli/main.py:283-331` (the `mcp` command); `src/superclaude/cli/install_mcp.py:42-116` (server registry), `install_mcp.py:489-567` (TTY check, prerequisites, installed check), `install_mcp.py:922-936` (codegraph scope rule), `install_mcp.py:1110-1314` (one-server install), `install_mcp.py:1317-1458` (list, menu, selection); `superclaude mcp --help`
- **Est. time:** `Tier A: 3 minutes (mcp --list alone can take 10 seconds to 2 minutes). Tier B: 5 minutes. Tier C: 10 minutes, only with access to the LiteLLM gateway.`

## Preconditions

- IronClaude 5.0.0 installed for your user: `superclaude --version` prints `SuperClaude, version 5.0.0`.
- The `claude` CLI (Claude Code) on your `PATH`. Every `superclaude mcp` action calls it (`claude mcp list`, `claude mcp get`, `claude mcp add`). No login is needed for Tier A or Tier B.
- For Tier B: `bash`, `python3`, `git`, and Node.js 18 or newer with `npx` on your `PATH` (the prerequisite check for npm-based servers, `src/superclaude/cli/install_mcp.py:510-528`). Tier B registers servers only inside a throwaway `HOME` and a temp project under `/tmp`; nothing is downloaded at registration time.
- For Tier C: network access to the LiteLLM gateway host `ibcore` on port 4000 and a key in `LITELLM_API_KEY`, both issued by your operator. Without them, skip Tier C.
- Run Tier A from a directory that has no `.mcp.json` file, so project-scope servers of some other project do not change the "installed" state you see.
- No step writes to your real `~/.claude.json` or `~/.claude/`. Tier A only previews; Step 1 records your real user MCP servers and Step 14 checks they are unchanged.

## What you're verifying

- `superclaude mcp --dry-run` prints the Install/Cancel menu and the numbered server choices and changes nothing; `--dry-run --servers <name>` prints the exact `claude mcp add` command it would run.
- Retired servers and flags are gone: `--servers serena` is rejected with exit 1 and `--uninstall` is an unknown option (exit 2).
- Without a terminal and without `--servers`, the command refuses (exit 1) instead of prompting.
- `litellm` is an opt-in HTTP server: menu choice `0` (all) leaves it out, but anyone can register it by name. Its registration stores the literal `${LITELLM_API_KEY}` placeholder, never the key.
- `--scope project` writes a `.mcp.json` in the current project; codegraph accepts only `--scope user`.

---

## Steps

### Tier A — free smoke on your machine (read-only)

#### Step 1 — Record your real MCP state `[FREE]`

**Do:** (bash; keep this terminal open until Step 14)

```bash
real_mcp() {
  python3 -c 'import json,os;p=os.path.expanduser("~/.claude.json");print(sorted(json.load(open(p)).get("mcpServers",{})) if os.path.exists(p) else "no ~/.claude.json")'
}
real_mcp | tee /tmp/d02-before.txt
```

**Expected result:** One line with the names of your user-scope MCP servers (for example `['codegraph', ...]`), or `no ~/.claude.json`. This is only a baseline; any value is a pass. If you set `CLAUDE_CONFIG_DIR`, your user config is `$CLAUDE_CONFIG_DIR/.claude.json`; change the path in `real_mcp` to match. (source: user-scope servers live under `mcpServers` in `~/.claude.json` or `$CLAUDE_CONFIG_DIR/.claude.json`, `src/superclaude/cli/install_mcp.py:709-742`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 2 — Help text `[FREE]`

**Do:**

```bash
superclaude mcp --help; echo "exit=$?"
```

**Expected result:** `Usage: superclaude mcp [OPTIONS]`, the line `No selection opens an action menu on a terminal.`, and exactly these options: `-s, --servers TEXT` (repeatable), `--list`, `--scope [local|project|user]`, `--dry-run`, `--help`. There is no `--uninstall` and no `--yes`. `exit=0`. (source: `src/superclaude/cli/main.py:283-313`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 3 — Dry-run menu `[FREE]`

**Do:**

```bash
superclaude mcp --dry-run; echo "exit=$?"
```

**Expected result:** Exactly:

```text
1. Install MCP servers (default)
2. Cancel
g. AIRIS MCP Gateway (recommended): airis-mcp-gateway; requires Docker
1. context7: Official library documentation and code examples
2. playwright: Cross-browser E2E testing and automation
3. morphllm-fast-apply: Fast Apply capability for context-aware code modifications (requires MORPH_API_KEY)
4. tavily: Web search and real-time information retrieval for deep research (requires TAVILY_API_KEY)
5. auggie: Augment Code semantic codebase search (codebase-retrieval, ask_question)
6. codegraph: Code graph: symbols, callers, impact, file outlines (pinned, installed by superclaude install)
7. litellm: LiteLLM MCP gateway: hosted Augment search, Tavily and Context7 behind one endpoint
0. Install all individual servers (except opt-in ones such as litellm)
[DRY RUN] Available choices only; select servers explicitly to preview an operation.
exit=0
```

No `serena` and no `codebase-memory-mcp` entry. Nothing is asked and nothing changes. (source: `src/superclaude/cli/install_mcp.py:42-116,1354-1359,1377-1384`; exit 0 because the result is a success, `src/superclaude/cli/main.py:324-331`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 4 — Retired server `serena` is rejected `[FREE]`

**Do:**

```bash
superclaude mcp --dry-run --servers serena; echo "exit=$?"
```

**Expected result:** `Unknown MCP server selection: serena` and `exit=1`. (source: `src/superclaude/cli/install_mcp.py:1422-1428`; exit 1 from `src/superclaude/cli/main.py:329-331`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — Removed flag `--uninstall` is rejected `[FREE]`

**Do:**

```bash
superclaude mcp --uninstall; echo "exit=$?"
```

**Expected result:** Click usage error `Error: No such option '--uninstall'.` after `Usage: superclaude mcp [OPTIONS]` and `Try 'superclaude mcp --help' for help.`; `exit=2`. The command defines no `--uninstall` option. (source: `src/superclaude/cli/main.py:283-304`; exit code 2 is Click's usage-error code, confirmed by running the command against the v5.0.0 checkout)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — No terminal and no selection `[FREE]`

**Do:**

```bash
superclaude mcp </dev/null; echo "exit=$?"
```

**Expected result:** `Explicit server selection is required; use --servers.` and `exit=1`. No menu is shown because standard input is not a terminal. (source: `src/superclaude/cli/install_mcp.py:489-490,1385-1389`; `src/superclaude/cli/main.py:329-331`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 7 — Preview the opt-in `litellm` server `[FREE]`

**Do:**

```bash
superclaude mcp --dry-run --servers litellm; echo "exit=$?"
```

**Expected result:** `📦 Installing MCP server: litellm`, then one of these, depending on your current registrations, then `Successfully previewed 1 MCP server(s).` and `exit=0`:

- not registered: `[DRY RUN] Would run: claude mcp add --transport http --scope user litellm http://ibcore:4000/mcp/ --header x-litellm-api-key: Bearer ${LITELLM_API_KEY}`
- registered with the same URL and header: `✅ Already installed and up to date: litellm`
- registered differently: `♻️  Re-registering litellm: ...` and `[DRY RUN] Would re-register litellm (...)`

No prerequisite check, prompt or registration runs in a dry run. (source: `src/superclaude/cli/install_mcp.py:107-115` (URL, header, `opt_in_only`), `install_mcp.py:1150-1193` (already-installed and re-register branches), `install_mcp.py:1255-1293` (command built and printed), `install_mcp.py:1430-1458` (no prerequisites in dry run; success message))

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — List the servers (slow) `[FREE]`

**Do:**

```bash
time superclaude mcp --list; echo "exit=$?"
```

**Expected result:** `📋 Available MCP Servers:`, a box `🚀 AIRIS MCP Gateway (Recommended)` with `Status:` and `Install: superclaude mcp --servers airis-mcp-gateway`, then `Individual Servers (legacy):` with seven entries in this order, each `✅ installed` or `⬜ not installed`: `context7`, `playwright`, `morphllm-fast-apply` (`(requires MORPH_API_KEY)`), `tavily` (`(requires TAVILY_API_KEY)`), `auggie`, `codegraph`, `litellm`; last line `Total: 7 individual servers + AIRIS Gateway available`; `exit=0`. It is slow because it runs `claude mcp list` once per entry (8 times, each with a 60-second limit) and Claude checks every registered server's health each time: about 10 seconds with two servers registered, 1-2 minutes with many. "Installed" is a case-insensitive name match anywhere in the `claude mcp list` output. (source: `src/superclaude/cli/install_mcp.py:551-567,1317-1351`; `src/superclaude/cli/main.py:316-322`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — local writes in a throwaway HOME and a temp project

#### Step 9 — Create the throwaway environment `[LOCAL-WRITE]`

**Do:** (same terminal)

```bash
umask 077
T=$(mktemp -d /tmp/ic-d02.XXXXXXXX); mkdir -p "$T/home" "$T/shims" "$T/proj"
for t in superclaude claude node npx npm git; do
  p=$(command -v "$t") && ln -s "$p" "$T/shims/$t" || echo "MISSING $t"
done
run() {  # one command with HOME=$T/home and a clean environment
  env -i HOME="$T/home" PATH="$T/shims:/usr/bin:/bin" LANG=C.UTF-8 TERM=dumb "$@"
}
run superclaude --version; echo "T=$T"
```

**Expected result:** No `MISSING` line; `SuperClaude, version 5.0.0`. `env -i` drops `CLAUDE_CONFIG_DIR`, so `claude` reads and writes only `$T/home/.claude.json`. (source: `src/superclaude/cli/install_mcp.py:709-742` reads the user config from `~/.claude.json`; recipe as in guide D01 Step 6, `docs/testing/v5.0.0/c-e2e-run.sh:13-24`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 10 — Project-scope install in a temp project `[LOCAL-WRITE]`

**Do:**

```bash
cd "$T/proj" && git init -q .
run superclaude mcp --dry-run --servers context7 --scope project; echo "exit=$?"
run superclaude mcp --servers context7 --scope project; echo "exit=$?"
cat .mcp.json; run claude mcp get context7
```

**Expected result:** The dry run prints `[DRY RUN] Would run: claude mcp add --transport stdio --scope project context7 -- npx -y @upstash/context7-mcp`, `Successfully previewed 1 MCP server(s).`, `exit=0`. The real run prints `Running: claude mcp add --transport stdio --scope project context7 -- npx -y @upstash/context7-mcp`, `✅ Successfully installed: context7`, `Successfully installed 1 MCP server(s).`, `exit=0`. `.mcp.json` in `$T/proj` holds `mcpServers.context7` with `"type": "stdio"`, `"command": "npx"`, `"args": ["-y", "@upstash/context7-mcp"]`. `claude mcp get context7` shows `Scope: Project config (shared via .mcp.json)` and a pending-approval status (wording from Claude Code 2.1.317: ``⏸ Pending approval (run `claude` to approve)``; other Claude Code versions can word it differently). (source: `src/superclaude/cli/install_mcp.py:43-49` (command), `install_mcp.py:1255-1303` (built command; scope added when not `local`), `install_mcp.py:1430-1458` (prerequisites, then the success message); confirmed by running this step against the v5.0.0 checkout)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 11 — Second install is a no-op `[LOCAL-WRITE]`

**Do:**

```bash
run superclaude mcp --servers context7 --scope project; echo "exit=$?"
```

**Expected result:** `✅ Already installed and up to date: context7`, `Successfully installed 1 MCP server(s).`, `exit=0`; `.mcp.json` is unchanged. The installer compares the registered command from `claude mcp get` with the expected one and stops when they match. (source: `src/superclaude/cli/install_mcp.py:1150-1180`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 12 — codegraph accepts user scope only `[LOCAL-WRITE]`

**Do:**

```bash
run superclaude mcp --dry-run --servers codegraph --scope project; echo "exit=$?"
run superclaude mcp --dry-run --servers codegraph; echo "exit=$?"
```

**Expected result:** First: `codegraph is registered at user scope only; use --scope user.`, then `Partially completed: 0/1 previewed. Failed servers: codegraph`, `exit=1`. Second: `[DRY RUN] Would reuse a codegraph 1.6.2 found on PATH or in ~/.local/bin, otherwise download the pinned v1.6.2 release for this platform and verify its SHA-256, then ensure the exact user-scope registration (claude mcp add-json codegraph ... --scope user). No changes made.`, then `Successfully previewed 1 MCP server(s).`, `exit=0`. Both are dry runs and write nothing; the tag is `[LOCAL-WRITE]` only because they run in the throwaway setup. (source: `src/superclaude/cli/install_mcp.py:922-936,1124-1128,1452-1458`; `src/superclaude/cli/main.py:329-331`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 13 — Register `litellm` and check that no key is stored `[LOCAL-WRITE]`

**Do:**

```bash
run superclaude mcp --servers litellm; echo "exit=$?"
run claude mcp get litellm
```

**Expected result:** `Running: claude mcp add --transport http --scope user litellm http://ibcore:4000/mcp/ --header x-litellm-api-key: Bearer ${LITELLM_API_KEY}`, `✅ Successfully installed: litellm`, `Successfully installed 1 MCP server(s).`, `exit=0`. It needs neither Node.js nor a key, because litellm has no `npx` command and no API-key prompt. `claude mcp get litellm` shows `Scope: User config ...`, `Type: http`, `URL: http://ibcore:4000/mcp/` and the header `x-litellm-api-key: Bearer ${LITELLM_API_KEY}` with the placeholder text, not a key. Its status is a connection failure unless you can reach `ibcore:4000` (for example `✘ Failed to connect`); that does not change the exit code. Nothing marks litellm as reserved for administrators: any user can register it. (source: `src/superclaude/cli/install_mcp.py:104-115` (placeholder kept; Claude Code expands it from the environment at connect time), `install_mcp.py:510-528` (Node.js is checked only for `npx`/`npm` commands), `install_mcp.py:1218-1238` (key prompt only for servers with `api_key_env`), `install_mcp.py:1268-1272` (URL and `--header`))

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 14 — Your real setup is unchanged `[FREE]`

**Do:**

```bash
real_mcp > /tmp/d02-after.txt; diff /tmp/d02-before.txt /tmp/d02-after.txt && echo REAL_MCP_UNCHANGED
```

**Expected result:** `REAL_MCP_UNCHANGED`. Tier A only previewed; Tier B wrote only to `$T`. (source: dry runs never reach prerequisites or registration, `src/superclaude/cli/install_mcp.py:1370,1430-1433,1291-1293`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier C — Claude API, proxy, PR or long runs

#### Step 15 — Use the LiteLLM gateway from Claude Code `[EXTERNAL]`

Only with operator-issued access to `ibcore:4000` and a key. This registers litellm in your real user config.

**Do:**

```bash
export LITELLM_API_KEY='<key from your operator>'
superclaude mcp --servers litellm; echo "exit=$?"
claude mcp get litellm
claude   # in the session, type /mcp
```

**Expected result:** The install prints `✅ Successfully installed: litellm` (or `✅ Already installed and up to date: litellm` if Step 7 showed it was already registered) and `exit=0` (source: `src/superclaude/cli/install_mcp.py:1150-1180,1296-1303`; `src/superclaude/cli/main.py:329-331`). `claude mcp get litellm` still shows the `${LITELLM_API_KEY}` placeholder in the header (source: `install_mcp.py:104-115`). Whether `/mcp` then shows litellm as connected, and which tools it offers (the registry describes hosted Augment search, Tavily and Context7, `install_mcp.py:109`), is UNVERIFIED: it depends on the operator's gateway, not on repo code.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 16 — Approve the project server in a Claude session `[CLAUDE-SESSION]`

**Do:**

```bash
cd "$T/proj" && claude   # approve the context7 server when asked, then type /mcp
```

**Expected result:** Claude Code asks to approve the project server from `.mcp.json` (Step 10 showed it pending approval); after approval `/mcp` lists `context7`. The approval prompt and the `/mcp` wording come from Claude Code, not from repo code: UNVERIFIED. Starting the server downloads `@upstash/context7-mcp` through `npx` (network). This session uses your real Claude login and HOME, so it may record the approval in your real Claude config; skip this step if you do not want that.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

---

## Edge cases (optional but recommended)

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[FREE]` `superclaude mcp --list --dry-run` (also `--list --servers context7` or `--list --scope project`) | `Error: --list cannot be combined with selections, --dry-run or another scope`, exit 2 | `src/superclaude/cli/main.py:316-320` | ☐ |
| `[FREE]` `superclaude mcp --dry-run --scope bogus` | `Error: Invalid value for '--scope': 'bogus' is not one of 'local', 'project', 'user'.`, exit 2 | `src/superclaude/cli/main.py:293-298` | ☐ |
| `[FREE]` `superclaude mcp --dry-run --servers context7 --servers serena` | `Unknown MCP server selection: serena`, exit 1; context7 is not previewed either, because the whole selection is checked first | `src/superclaude/cli/install_mcp.py:1422-1428`; `src/superclaude/cli/main.py:329-331` | ☐ |
| `[FREE]` `superclaude mcp --dry-run --servers tavily` with `TAVILY_API_KEY` unset | `[DRY RUN] Would request TAVILY_API_KEY during installation; no prompt or key change now.`, then `[DRY RUN] Would run: claude mcp add --transport stdio --scope user tavily -e DEFAULT_PARAMETERS=<value> -- npx -y tavily-mcp@0.2.22`, where `<value>` is the `DEFAULT_PARAMETERS` JSON documented in `src/superclaude/mcp/MCP_Tavily.md` (when tavily is not yet registered), exit 0 | `src/superclaude/cli/install_mcp.py:66-75,1221-1247,1291-1293` | ☐ |
| `[FREE]` On a real terminal: `superclaude mcp`, answer `2` | `Action (1, 2) [1]:` then `Cancelled; no changes made.`, exit 0 | `src/superclaude/cli/install_mcp.py:1390-1393` | ☐ |
| `[FREE]` On a real terminal: `superclaude mcp`, answer `1`, then `9` (or `x`) | The choice list, then `Select g for gateway, 0 for all, or comma-separated numbers [g]:`, then `Invalid selection; no changes made.`, exit 1. Do not answer `g`, `0` or a valid number: those install for real | `src/superclaude/cli/install_mcp.py:1394-1421`; `src/superclaude/cli/main.py:329-331` | ☐ |
| `[LOCAL-WRITE]` Missing Node.js: `mkdir -p "$T/nonode"; ln -s "$(command -v claude)" "$T/nonode/claude"; env -i HOME="$T/home" PATH="$T/nonode" "$(command -v superclaude)" mcp --servers playwright; echo "exit=$?"` | `Prerequisites not met:`, `Node.js 18+ required for selected npm servers`, `npx/npm is required for selected npm servers`, exit 1; nothing is registered. This assumes `node` is not in `/usr/bin` or `/bin` (the `PATH` here holds only the `claude` link) | `src/superclaude/cli/install_mcp.py:493-548,1430-1433`; `src/superclaude/cli/main.py:329-331` | ☐ |
| `[LOCAL-WRITE]` A registration in another scope hides the requested scope: `run superclaude mcp --servers context7 --scope user`, then `mkdir -p "$T/proj3" && cd "$T/proj3" && run superclaude mcp --servers context7 --scope project; ls -A` | The second command prints `✅ Already installed and up to date: context7`, exit 0, and `ls -A` prints nothing: no `.mcp.json` is written. The installed check matches the name in `claude mcp list` across all scopes and `claude mcp get` finds the user entry, so `--scope project` is not applied | `src/superclaude/cli/install_mcp.py:551-567,1150-1180` | ☐ |

## Cleanup

```bash
cd /tmp && rm -rf "$T" /tmp/d02-before.txt /tmp/d02-after.txt
```

This removes the throwaway `HOME` (its `.claude.json` with the test context7 and litellm registrations) and the temp projects. If you ran Step 15 and want litellm gone from your real setup, run `claude mcp remove litellm -s user`. If you ran Step 16, Claude Code may keep the approval for the deleted `$T/proj` path in your real config; it has no effect once the folder is gone.

## Overall result

☐ **PASS** — capability works as documented for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `5.0.0 (tag v5.0.0, commit d953b983)`
