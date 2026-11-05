# Phase 2 spec: install codegraph by default (issue #323)

Status: complete (task P2, 2026-10-29); revised by finalizer F2 on 2026-10-29 to apply the task R review (`.dev/codegraph-migration/review/review.md`), see "Review resolution" at the end. Planning artifact only; no source was changed. Companion files: `.dev/codegraph-migration/handoff/coder-handoff-prompt.md`, `.dev/codegraph-migration/handoff/coder-handoff-context.md`.

## 0. Inputs and evidence rule

Goal: after this phase, `superclaude install` (and therefore `./update.sh`, which runs `superclaude install --force` at `update.sh:8`) installs a pinned, checksum-verified codegraph and registers it as a user-scope MCP server, reusing a copy the Coder image already baked; new checkouts get an index on first use.

Inputs (all read for this spec, 2026-10-29): `.dev/codegraph-migration/orchestration/README.md` (rules), `research/codegraph-evaluation.md` (W4: codegraph facts, sandbox recipe, install strategy chosen by adversarial quick), `research/install-update-flow.md` (W5: seams, Coder touchpoints, ordering), `inventory/codebase-memory.md` (W1), `inventory/serena.md` (W2), `inventory/org-repos.md` (W3), `specs/phase-1-removal-spec.md` (P1, in progress; its §2.2 merge constraint, §6.2 Coder facts and §7 "Shared files with Phase 2" table were read at the end of this task and this spec was aligned to them).

Source re-read for this spec (IronClaude worktree at `55d40308`): `update.sh:1-10`; `src/superclaude/cli/main.py:28-95` (install signature, imports), `:155-190` (`--list` native block), `:245-280` (required phase and exit), `:470-515` (doctor command); `src/superclaude/cli/doctor.py:1-60`; `src/superclaude/cli/install_mcp.py:1-35`, `:36-112` (registry), `:480-505`, `:710-915` (registration helpers and `install_codebase_memory_mcp`), `:1010-1030` (dispatch); `src/superclaude/cli/install_codebase_memory.py:15-60`, `:565-660` (discovery and reuse); `src/superclaude/cli/install_user_setup.py:140-170`; `src/superclaude/cli/install_hooks.py:40-82`; `src/superclaude/hooks/hooks.json:1-30`; `src/superclaude/core/CLAUDE.md:1-40`, `:100-118`; `tests/cli/test_update_script.py:1-40`; `tests/cli/test_update_command.py:20-95`; `tests/cli/test_install_mcp_tavily.py:380-520`; `tests/cli/test_install_mcp_registry.py:1-30`; `tests/unit/test_cli_install.py:140-160`, `:415-430`; `tests/core/test_claude_md_routing_block.py:70-95`; `.github/workflows/test.yml:125-175`; `docs/user-guide/mcp-installation.md:1-30`; `README.md:55-80`; `CHANGELOG.md:1-25`. `rg -i codegraph` outside `.dev/` returns no file: nothing about codegraph exists in the repo yet.

Sandbox facts added by this task (W4 sandbox `/tmp/codegraph-eval.fQfO`, sandbox HOME, telemetry off): `codegraph --version` prints exactly `1.6.2` (exit 0); `~/.local/bin/codegraph` resolves to `~/.codegraph/versions/v1.6.2/bin/codegraph`; `codegraph init --yes` on an already indexed project is a no-op, exit 0, 125 ms; `codegraph status` exits 0 even when the project is not initialized; `codegraph query` exits 1 when not initialized; `codegraph sync --quiet` is documented "for git hooks"; `codegraph init` refuses a home directory or filesystem root without `--force`. The v1.6.2 `SHA256SUMS` (downloaded by W4 into `/tmp/codegraph-eval.fQfO/dl/SHA256SUMS`) lists:

| Asset | SHA-256 |
|---|---|
| `codegraph-linux-x64.tar.gz` | `ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828` |
| `codegraph-linux-arm64.tar.gz` | `c8c6be292be21d00dea26bad8b28d434731cf612fb8cc475dc10f5b3038b5b64` |
| `codegraph-darwin-x64.tar.gz` | `53d1a4d1a9af31d6cec11b346df2ae792087081e13f623f583e27783c1e7f9bc` |
| `codegraph-darwin-arm64.tar.gz` | `d74d1bfb4060db63ec3c2b72c4e17f76c31978af3bad6ace4370d1501ac0662e` |
| `codegraph-win32-x64.zip`, `codegraph-win32-arm64.zip` | not used (Windows unsupported, §2.3) |

Executor rule: these hashes are copied from a file another task downloaded. Task T1 re-downloads `SHA256SUMS` with `gh release download v1.6.2 -R colbymchenry/codegraph -p SHA256SUMS` and must find the same four lines before committing them to source.

## 1. Preflight: files that change

Assumption: Phase 1 has already landed on the same feature branch (§8). Phase 1 deletes `install_codebase_memory.py`, the Codebase Memory phase (`main.py:254-262`), its `--list` block (`main.py:161-186`), its registry entry (`install_mcp.py:101-108`), the Serena registry entry (`install_mcp.py:55-61`) and the `superclaude mcp --uninstall/--yes` flags. Line numbers below are from `55d40308`; after Phase 1 they move, so the executor locates each seam by the named function or block, not by line.

"Shared" in the last column means Phase 1 or Phase 3 also edits the file (full list in §9).

| # | File | Change | Shared |
|---|---|---|---|
| F1 | `src/superclaude/cli/install_codegraph.py` (new) | Pin constants (`VERSION = "1.6.2"`, `TAG = "v1.6.2"`, `SHA256` dict with the four §0 assets, `MCP_TOOLS` = the tool-list value T2 step 0 selects, §2.4), `asset_name()` (platform map: Linux/Darwin × x86_64/amd64/aarch64/arm64 → `linux-x64`, `linux-arm64`, `darwin-x64`, `darwin-arm64`; anything else → None), `discover()` (exact version gate, §2.2), `acquire()` (verified download and extract, §2.3), receipt read/write (§2.6). Standard library only (`urllib.request`, `hashlib`, `tarfile`, `tempfile`, `os`, `subprocess` with timeouts). | no |
| F2 | `src/superclaude/cli/install_mcp.py` | (a) Registry entry `"codegraph"` in `MCP_SERVERS` (shape of the old `codebase-memory-mcp` entry, `:101-108`: `transport: stdio`, `command: "codegraph"`, `args: ["serve", "--mcp"]`, `required: False`) so `superclaude mcp --list`, the menu and `--servers codegraph` work. (b) Dispatch branch at the top of `install_mcp_server` routing `codegraph` to the phase function (same shape as `:1025-1028`). (c) Phase function `install_codegraph_mcp(*, scope="user", dry_run=False) -> tuple[bool, str]` modelled on `install_codebase_memory_mcp` (`:815-913`). (d) Registration helpers by server name: Phase 1 keeps `read_user_mcp_entry(name)`, `_run_registration_command(cmd)` and a name-parameterised exact-entry remover (Phase 1 spec §7) and deletes `_native_registration_matches`, `_add_user_native_entry`, `_restore_user_native_entry` (`:757-812`); T2 re-creates those three from `55d40308` with a `name` parameter and a whole-entry compare (task T2 still checks mechanically which exist, §5). (e) Import of `install_codegraph`. | **Phase 1** |
| F3 | `src/superclaude/cli/main.py` | `install()`: help/docstring text naming codegraph; phase block "Installing codegraph (required user-level phase)…" after `install_user_setup` (where the Codebase Memory block was, `:254-262`) and immediately before Phase 1's non-fatal retire step (`install_retired_mcp.py`; §2.1); `or not codegraph_success` in the exit condition (`:264-275`); a read-only codegraph block in `--list` (where `:161-186` was) printing executable state, version, owner (from receipt) and registration state. `mcp()` and `update()` unchanged. | **Phase 1** |
| F4 | `src/superclaude/cli/doctor.py` | `_check_codegraph()` appended to `run_doctor` checks (`:26-44`); behaviour in §2.7. | no |
| F5 | `update.sh` | **No change.** Line 8 `superclaude install --force` already reaches the new phase; the four commands are pinned by `tests/cli/test_update_script.py:13-18`. | no |
| F6 | `src/superclaude/core/CLAUDE.md` | Add a `codegraph` row to the "MCP Servers" table (`:17-25`; keep the `\| Flag (advisory) \|` header pinned by `tests/core/test_claude_md_routing_block.py:79-81`) and a short "codegraph" guidance block between fixed begin/end markers (text and markers in §3.4). This replaces the block upstream `codegraph install` would write to `~/.claude/CLAUDE.md`, which `superclaude install --force` erases (W4 §2). The Serena row (`:21`) and the "Symbolic queries" refresh-tool row (`:112`) are Phase 1 (removal) and Phase 3 (replacement mapping); Phase 2 does not edit those two rows. There is no `plugins/superclaude/core/CLAUDE.md` (checked: `ls plugins/superclaude/core`). | **Phase 1, Phase 3** |
| F7 | Indexing hook files (only if §3 ships a hook): `src/superclaude/hooks/scripts/codegraph-session-start.sh` (new), `src/superclaude/hooks/hooks.json` (SessionStart entry), `plugins/superclaude/hooks/hooks.json` and `plugins/superclaude/hooks/scripts/codegraph-session-start.sh` (mirror), `src/superclaude/cli/install_hooks.py` (`_FRESHNESS_SCRIPTS`, `:42-79`, required by `make verify-sync`) | §3 | **Phase 1** (`hooks.json` matcher edit at `:47`) |
| F8 | `docs/user-guide/mcp-installation.md` | New top section "Default setup: codegraph" (pin, verified download, reuse of a baked copy, user-scope registration argv, telemetry off, `--list`, doctor, failure and exit codes, removal commands, indexing). Replaces the Codebase Memory section Phase 1 deletes (`:5-26`). Add `codegraph` to "Available MCP Servers" (`:52`). | **Phase 1** |
| F9 | `docs/reference/mcp-server-guide.md` | `codegraph` row in "Available MCP Servers" (`:9`); new "codegraph lifecycle" section where "Codebase Memory Native Lifecycle" was (`:31-55`); troubleshooting entries (not initialized, lock error from `codegraph sync`, stale version). | **Phase 1** |
| F10 | `README.md` | Install description (`:64`) and the dev-install comment (`:75`) say codegraph instead of Codebase Memory. | **Phase 1** |
| F11 | `CHANGELOG.md` | `## [Unreleased]` entry "codegraph installed by default" (Added/Changed). | **Phase 1** (its own entry) |
| F12 | `.github/workflows/test.yml` (`doctor-check`, `:130-171`) | Keep the `Install Claude CLI` step (Phase 1's W1 row 12 proposes deleting it because Codebase Memory no longer needs it; the codegraph phase needs `claude --version`). Rewrite its comment and the `permissions` comment (`:133-134`) to name codegraph. The job then downloads the pinned tarball (63 MB) and runs a real verified install on `ubuntu-latest`. | **Phase 1** |
| F13 | `tests/cli/test_install_codegraph.py` (new) | Unit tests for F1 and the phase function (§4.1). | no |
| F14 | `tests/cli/test_update_command.py` | Autouse fixture also stubs `install_mcp.install_codegraph_mcp` (Phase 1 rewrites the fixture first); expected install call list gains `install_codegraph_mcp` last; new tests: required phase failure keeps framework work and exits 1; `--force` is not forwarded; `--list` codegraph block is read-only. | **Phase 1** |
| F15 | `tests/cli/test_install_mcp_registry.py` | Registry entry contract for `codegraph` and dispatch to `install_codegraph_mcp`. | **Phase 1** |
| F16 | `tests/unit/test_cli_doctor.py` | Tests for `_check_codegraph` (§2.7). | no |
| F17 | `tests/cli/test_install_hooks.py`, `tests/unit/test_cli_install.py` (hook script listing, `:140-145`) | Only if §3 ships a hook: registration test and packaged-file listing. | **Phase 1** (Serena matcher asserts `:684-687`; MCP listings `:150-153`, `:423-425`) |
| F18 | `src/superclaude/cli/install_retired_mcp.py` (Phase 1's retire step), its Phase 1 test file, `src/superclaude/cli/main.py` (passes `codegraph_ready()`), `install_mcp.py` (`codegraph_ready()`) | §2.12: the readiness-gated Serena and kind-B codebase-memory removal. Phase 1 must also amend its own spec rows (Phase 1 §2.3 row, §3.2 Tier K, §3.4 hint, §3.6 row, its sandbox expectation "Legacy Serena registration kept", D2), listed in §9 | **Phase 1** |
| F19 | `.gitignore` | Add `.codegraph/`. codegraph's own `.codegraph/.gitignore` is `*` plus `!.gitignore`, so the folder still shows as `?? .codegraph/` and `git add -A` commits `.codegraph/.gitignore` (third review, finding 5). Docs (F8) tell users to add `.codegraph/` to their `core.excludesFile`. | no |

Not changed, with the reason: `superclaude update` (`main.py:346-431`, documented never to touch native/MCP state, `docs/user-guide/mcp-installation.md:24`); `src/superclaude/cli/user_settings_defaults.json` and `install_user_setup.py` (no `permissions` handling exists; §2.5 decides no permission rule); `src/superclaude/mcp/` (no `MCP_Codegraph.md` or `configs/codegraph.json`: those files are package data that install nowhere, `~/.claude/mcp/` does not exist per W2 §4.1, and adding them would change the pinned listing in `tests/unit/test_cli_install.py:150-153`); `.claude/settings.json` (no MCP content, W5 §1.6); `Makefile`, `pyproject.toml` (no new dependency).

## 2. Installer design

The overall strategy (bake in Coder, IronClaude-verified download as fallback, never upstream `install.sh` or `codegraph install`, absolute-path `add-json` registration with telemetry off) was chosen by W4's `/sc:adversarial --depth quick` (`decisions/W4-install-strategy/adversarial/W4-install-strategy-merged.md`). The phase contract below was chosen by this task's `/sc:adversarial` at standard depth (`decisions/P2-installer-contract/adversarial/P2-installer-contract-merged.md`; options A required + strict doctor + CLI uninstall, B non-fatal + advisory doctor + documented removal, C required + doctor fails only on a dangling command + receipt; scores C 0.896, B 0.859, A 0.839; convergence 18/18). `/sc:design` was not run: the interface is three functions (2.11) and adds no clarity beyond this section.

### 2.1 Contract (required phase)

`superclaude install` runs, after `install_user_setup` and immediately before Phase 1's non-fatal retire step (Phase 1 spec §3.3 "Placement": the slot of the deleted Codebase Memory phase, before the exit-code block), this phase. The retire step still runs whatever this phase returns, but Phase 2 gates part of it on `codegraph_ready()` (§2.12): the current-pin Serena entry is never removed unless codegraph is ready in the same run (Phase 1's unconditional Tier R rows and the `/usr/local/bin/codebase-memory-mcp` entry are still removed either way).

```text
Installing codegraph (required user-level phase)...
```

The phase result is one more term in the exit condition (`main.py:264-275`): if it fails, every other phase still runs, framework files are kept, stderr names the failed stage and the exact recovery command, and the command exits 1. `./update.sh` (`set -euo pipefail`, `update.sh:2,8`) therefore stops on a failed codegraph phase, and Coder's existing "slug exits 0" checks prove "installed by default". `--force` is not forwarded to the phase (same rule as today, `main.py:255`; pinned by `tests/cli/test_update_command.py:345-370`). `superclaude update` does not run the phase.

### 2.2 Discovery (reuse, no network)

Candidates in this order: `shutil.which("codegraph")` (on Coder: `/usr/local/bin/codegraph`), then `~/.local/bin/codegraph`. For each, run `[candidate, "--version"]` with a 10 s timeout through the bounded argv runner (2.4 last paragraph); the first whose stripped stdout equals `VERSION` (`"1.6.2"`) wins. The winner's `os.path.realpath` is what gets registered, and is also written to the pointer file `~/.codegraph/.superclaude-bin` (one line, mode 0600, rewritten only when it changes) so the indexing hook and the guidance use the same binary as the MCP server (§3.2). If the winner is not what `command -v codegraph` resolves to in the user's shell (for example `~/.local/bin` is not on `PATH`, macOS default), the phase prints a warning with the `PATH` line to add; it does not fail. Discovery never modifies anything and works on any platform (a baked copy on an otherwise unsupported platform is reused).

### 2.3 Acquisition (fallback) and platforms

Only when no candidate matches:
1. `asset_name()` maps `platform.system()`/`platform.machine()`: Linux or Darwin × `x86_64`/`amd64` → `x64`, `aarch64`/`arm64` → `arm64`. Anything else (Windows, other Unix, other arch) fails the phase: "codegraph v1.6.2 has no supported automatic install for <system>/<machine>; install it yourself so that `codegraph --version` prints 1.6.2, then rerun superclaude install."
2. Download `https://github.com/colbymchenry/codegraph/releases/download/v1.6.2/codegraph-<asset>.tar.gz` with `urllib.request.urlopen(url, timeout=60)` into a `tempfile.mkdtemp(dir=~/.codegraph)` directory (same filesystem as the target, so the final rename is atomic). `urllib` honours `https_proxy`.
3. Verify `hashlib.sha256` against the `SHA256` table. Mismatch fails the phase (stage `checksum`) and deletes the temp dir.
4. Extract with `tarfile`, accepting only regular files and directories whose path starts with `codegraph-<asset>/` and contains no `..` or absolute part (the v1.6.2 tarball has 1380 such members and no links, checked by this task). Python >= 3.10 is supported (`pyproject.toml:16`), so do not rely on the `filter=` argument.
5. Check `<tmp>/codegraph-<asset>/bin/codegraph --version` equals `VERSION`. **Record the version dir in the receipt (2.6) before renaming**, then rename it to `~/.codegraph/versions/v1.6.2/`. If that dir already exists and is receipt-listed (a previous run interrupted after step 5), replace it; if it exists and is not listed (upstream `install.sh` put it there), use it only if its `bin/codegraph --version` matches, else fail and report the path. A receipt entry for a dir whose rename never happened is harmless (nothing to delete).
6. Point `~/.local/bin/codegraph` and `~/.codegraph/current` at the version dir (`os.symlink` to a temp name, then `os.replace`), recording each link in the receipt before replacing it. Never overwrite a link or file that is not receipt-owned: if one exists and points elsewhere, leave it, report it, and register the version dir's absolute `bin/codegraph` instead.
7. Mark the receipt complete (`"complete": true`) after the links are in place.

`gh attestation verify` is not used by the installer (it needs GitHub auth, W4 §5.1); the source-pinned SHA-256 is the integrity check. Upstream's "update available" check is disabled through the registration env.

### 2.4 Registration

Exact argv (W4 §3 and §7):

```text
claude mcp add-json codegraph '{"type":"stdio","command":"<realpath of the winner>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1","CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"}}' --scope user
```

**Tool list (`CODEGRAPH_MCP_TOOLS`, review finding X-1).** Upstream lists only `codegraph_explore` by default (`DEFAULT_MCP_TOOLS = new Set(['explore'])`, `research/codegraph-evaluation.md:94`), and Phase 3 primitives name `codegraph_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files` and `_status` and never `explore` (Phase 3 decisions P3-D1, P3-D9). Phase 2 therefore owns the key and the schema-cost check that gates it (moved here from Phase 3 T0 E-5; threshold from `decisions/P3-access-model/adversarial/P3-access-model-merged.md:152-157`: the 7-tool list may add at most 2K tokens per session over the default listing). T2 step 0 runs that check before any registration code is written and sets `install_codegraph.MCP_TOOLS`:
- pass: `MCP_TOOLS = "node,search,callers,callees,impact,files,status"` (the JSON above);
- fail: `MCP_TOOLS = "status"` (P3-D1 failure branch; explore stays hidden; Phase 3 then uses its CLI and artifact paths), and every literal 7-tool value in this spec, U12, layer 2 and the Coder handoff is replaced by `status` in the same commit.
The installer builds the env from `MCP_TOOLS`; nothing else hard-codes the value. UNVERIFIED until T2 step 0 and layer 2 step 5b run: that an explicit list hides **and** blocks every unnamed tool (source-cited `tools.ts:2926-2929`, never observed; the only hands-on run with the key listed `explore` too, `research/codegraph-evaluation.md:212-213`; review finding X-25). Those two steps are the proof: with the key set, `tools/list` has no `codegraph_explore` and has `codegraph_callers`, and a `tools/call` of `codegraph_explore` returns an error.

**Premise to verify first (T2 step 1):** nobody has yet run `claude mcp add-json` with this JSON (W4 §3 took the argv shape from `--help`; the run rules forbid `claude mcp add` against the real environment). Before writing the matcher, T2 runs it once in a sandbox (`CLAUDE_CONFIG_DIR` and `HOME` in a `mktemp -d`, then `jq '.mcpServers.codegraph'` on the sandbox `.claude.json`) and records the stored entry in `.dev/codegraph-migration/evidence/P2-add-json-shape.json`. The "expected entry" compare below uses exactly the fields that probe shows are stored unchanged; if the CLI drops or normalises a field (for example `alwaysLoad` or `env`), the matcher ignores that field and the spec's §2.4 table is updated in the same commit (a mid-level decision if the field is load-bearing, §7).

Before it: `claude --version` must succeed (10 s timeout), checked before discovery and acquisition, as `install_mcp.py:830-843` does today. Then read the exact top-level user entry (`read_user_mcp_entry("codegraph")`, `install_mcp.py:714-754`; lookup failure fails the phase with no mutation).

| Existing entry | Action |
|---|---|
| absent | `add-json`, re-read, verify equality |
| equal to the expected entry (whole-entry compare: type, command, args, env, alwaysLoad) | nothing (idempotent) |
| **owned**: type stdio or absent, no `url`, no `headers`, `args == ["serve","--mcp"]`, env keys a subset of `{CODEGRAPH_TELEMETRY, CODEGRAPH_NO_UPDATE_CHECK, CODEGRAPH_MCP_TOOLS}`, but otherwise different (old realpath after a pin bump, missing `alwaysLoad`) | remove through Phase 1's `_remove_exact_user_entry("codegraph", matcher)` (Phase 1 spec §3.3), `add-json`, re-read, verify; on failure restore the previous entry (re-created `_restore_user_native_entry` pattern, baseline `install_mcp.py:789-812`) |
| **user-managed** (anything else) and its `command` resolves to an executable | keep it; phase passes with "user-managed codegraph entry kept; to let IronClaude manage it run: claude mcp remove codegraph --scope user" |
| user-managed and its command does not resolve | phase fails with the same command |

**Bounded argv runner.** `install_mcp._run_command` runs `$SHELL -c` with `shell=True` on Linux and macOS (`install_mcp.py:134-141`), so its timeout kills only the shell, not `claude` or `codegraph`. Every `claude` and `codegraph` call in this phase therefore uses the bounded runner Phase 1 adds for its retire step (argv list, no shell, `start_new_session=True`, process group killed on timeout; Phase 1 spec §3.3 "Bounds"); T2 finds it with `rg -n 'start_new_session' src/superclaude/cli/`. If Phase 1 kept it private to `install_retired_mcp.py`, T2 moves it to `install_mcp.py` (one copy, both callers). Timeouts: 10 s for `--version` calls, 60 s for each `claude mcp` call. Output and exception text are never echoed (existing rule, `install_mcp.py:766-772`). Coder's `timeout 60` can kill the phase between remove and add; the next `superclaude install` sees "absent" and repairs it. Whether Coder reruns the install after such a kill (it reruns only when the image SHA changes, and the `.configured` marker is not written on failure) is UNVERIFIED (Phase 1 spec §3.6 lists the same question); the Coder handoff asks the Coder agent to confirm it.

### 2.5 Guidance and permissions

Guidance goes into `src/superclaude/core/CLAUDE.md` (§3.4, F6), never into a `CODEGRAPH_START` block. No `mcp__codegraph__*` permission rule is added: no other MCP server gets one today (`install_user_setup.py` has no `permissions` handling, checked with `grep -n permissions`), every codegraph tool is read-only (W4 §3), and Claude Code's normal per-tool approval applies.

### 2.6 Receipt, ownership and removal

- Receipt `~/.codegraph/.superclaude-receipt.json` (mode 0600, written atomically with `os.replace`), updated only during a verified download (2.3 steps 5-7), never for a baked or external binary: `{"tag": "v1.6.2", "sha256": "<tarball hash>", "version_dirs": ["~/.codegraph/versions/v1.6.2"], "links": {"~/.local/bin/codegraph": "<target>", "~/.codegraph/current": "<target>"}, "complete": true}` (absolute paths in the real file; `version_dirs` in install order). Entries are added before the path they describe is created, so an interrupted run leaves nothing unrecorded.
- Pointer file `~/.codegraph/.superclaude-bin` (2.2) is written for every winner, baked or downloaded; it is not an ownership record and is never used to delete anything.
- A link counts as owned only while it points where the receipt says. A corrupt or unreadable receipt means: delete nothing, do not fail, rewrite it after the next verified download.
- **Old version dirs:** on a pin bump, install the new dir, flip the owned links, keep the previous owned dir for one run. On a later run, delete an older receipt-listed dir only when this run's registration was verified, the receipt and `~/.claude.json` both read OK, and none of the registered command realpath, `~/.local/bin/codegraph` or `~/.codegraph/current` resolves inside it (a running daemon from the previous version dies with its session; W4 §5.7 idle timeout 300 s).
- **Removal (documented, no CLI flag):** `claude mcp remove codegraph --scope user`, then delete the paths `superclaude install --list` prints as "owned" (the receipt's version dirs and links, then the receipt). Project indexes are removed per project with `codegraph uninit`. Baked or external binaries and `.codegraph/` dirs are never listed as removable. Text goes in `docs/user-guide/mcp-installation.md` (F8).

### 2.7 Doctor

New check "codegraph MCP registration" in `doctor.py` (`_check_codegraph(home=None)`, same `{name, passed, details}` dict as `_check_ccsession`):
- `passed: False` only when the user entry `codegraph` exists and its `command` (resolved with `shutil.which` when it is a bare name) is not an executable file: codegraph tools would be missing from every session.
- `passed: True` with a detail line for: entry missing; version of the registered command differs from the pin; a `codegraph prompt-hook` command in `~/.claude/settings.json` hooks; a `<!-- CODEGRAPH_START -->` block in `~/.claude/CLAUDE.md`; `~/.claude.json` unreadable ("unknown").
- Always one detail line `Ready for Serena retirement: yes | no (<reason>)` from `codegraph_ready()` (§2.12); it never changes `passed`.
Reason for not failing on absence or drift: under `./update.sh` doctor runs only after `install` exited 0 (`update.sh:2,8,10`), so presence is already enforced. Doctor must not run `codegraph --version` for longer than 10 s.

### 2.8 `superclaude install --list`

Read-only block after Templates (where `main.py:161-186` was), exit stays 0, never downloads and never calls `claude mcp`:

```text
codegraph MCP (pinned v1.6.2; user scope):
   Executable: <path> (1.6.2) | missing | version mismatch at <path> (<version>)
   Owner: owned (receipt) ~/.codegraph/versions/v1.6.2, ~/.local/bin/codegraph -> <target> | external: /usr/local/bin/codegraph, not owned
   User registration: matches | absent | owned but stale | user-managed | unknown (read/parse failure)
   Ready for Serena retirement: yes | no (<reason>)
```

`superclaude mcp --list` shows `codegraph` through the registry entry (F2a); `superclaude mcp --servers codegraph [--dry-run]` runs the same phase function through the dispatch branch.

### 2.9 Idempotency

A second `superclaude install` on a correct machine makes one `claude --version` call, one `codegraph --version` call per candidate until the winner, one `~/.claude.json` read, and no download, no file write and no `claude mcp` mutation (layer 2 step 2 proves it with a dead proxy, §4.2).

### 2.10 Failure behaviour and exit codes

| Stage | Example cause | Phase result | `superclaude install` exit | Files changed |
|---|---|---|---|---|
| prerequisites | `claude` missing or `claude --version` fails | fail | 1 | none |
| discovery | no candidate prints 1.6.2 | continue to acquisition | n/a | none |
| platform | unsupported OS/arch and no matching candidate | fail, named platform | 1 | none |
| download | network error, HTTP error, timeout (60 s) | fail, URL + recovery command | 1 | temp dir removed |
| checksum | hash mismatch | fail, both hashes printed | 1 | temp dir removed |
| extract | unsafe member, bad archive, version check of extracted copy fails | fail | 1 | temp dir removed |
| links | a non-owned link in the way | continue, report, register the version dir path | 0 if the rest passes | version dir only |
| registration lookup | `~/.claude.json` unreadable, duplicate keys | fail, no mutation | 1 | version dir, links, receipt (if downloaded) |
| registration | add or verify fails | fail, previous entry restored (or "may be partial; inspect") | 1 | as above |
| user-managed entry, command resolves | user's own codegraph entry | pass, keep it, print removal command | 0 | none |
| dry run (`superclaude mcp --servers codegraph --dry-run`) | n/a | pass, prints plan | 0 | none |

`superclaude doctor` exits 1 only through 2.7's single failing condition (or the five existing checks).

### 2.11 Code shape (smallest correct)

About 300 lines of source and 33 tests (debate estimate).

```python
# src/superclaude/cli/install_codegraph.py  (stdlib only, about 180 lines)
VERSION = "1.6.2"; TAG = f"v{VERSION}"
SHA256 = {"linux-x64": "...", "linux-arm64": "...", "darwin-x64": "...", "darwin-arm64": "..."}
def asset_name() -> str | None: ...
def discover(run) -> Path | None: ...            # run = the bounded argv runner (2.4), injected for tests
def acquire() -> tuple[bool, str, Path | None]:  # (ok, message, absolute launcher path)
def read_receipt() -> dict | None: ...
def prune_old_versions(registered: Path) -> None: ...
def _download(url: str, dest: Path, timeout: int) -> None: ...   # the one function tests patch

# src/superclaude/cli/install_mcp.py  (+60 lines)
def install_codegraph_mcp(*, scope: str = "user", dry_run: bool = False) -> tuple[bool, str]: ...
```

`install_mcp.py` keeps one set of name-parameterised registration helpers (read entry, run registration command, add-json, remove, restore). If Phase 1 deleted them with Codebase Memory, T2 re-creates them from the `55d40308` versions (`install_mcp.py:714-812`) with a `name` parameter; if Phase 1 kept them (its own Serena/Codebase Memory cleanup needs a read and a remove), T2 adds the `name` parameter where it is missing. The old guard that refuses any entry with `env` (`install_mcp.py:867-873`) is not carried over for codegraph: the owned-entry rule in 2.4 replaces it.

### 2.12 Retiring Serena once codegraph is ready (amends Phase 1's retire step)

Requirement (user, via the coordinator, `orchestration/README.md` "Coordinator concerns"): after `./update.sh` on an existing workspace, Serena and codebase-memory must be completely absent. Phase 1 alone keeps the current-pin `serena-agent==1.7.0` entry (its Tier K), which is the entry this workspace has. Decided by `/sc:adversarial` at standard depth (`decisions/P2-serena-entry-removal/adversarial/P2-serena-entry-removal-merged.md`; options A keep Tier K and leave it to Coder, B remove once codegraph is ready, C remove only off Coder; scores B 0.898, C 0.853, A 0.835; convergence 18/18):

- `codegraph_ready()` (in `install_mcp.py`): one read-only predicate on current state, shared by `install`, `install --list` and `doctor`. True when the user entry `codegraph` either equals the expected entry (§2.4) or is an owned entry whose command's `--version` prints `1.6.2`, or is a user-managed entry whose command resolves to an executable (any version: the user chose it). `install()` passes `codegraph_success and codegraph_ready()` to the retire step, so a failed phase in this run never counts as ready.
- When ready, the retire step also removes: (a) every user-scope entry other than `serena-local`, matched by shape rather than by key name, whose args contain `start-mcp-server` (this covers `serena` and a renamed Serena launcher), whose `type` is stdio or absent, and whose `env` and `headers` are each **absent or `{}`** (Coder's bundle and `claude mcp add` write `"env":{}`, and the live entry on this workspace has it: third review finding 1); and (b) the kind-B `~/.local/bin/codebase-memory-mcp` registration (its binary and upstream companions stay; the upstream `uninstall -y` command is printed). Each removal prints the removed argv. A launcher entry (any name) with a non-empty `env` or `headers` is kept and reported. The re-register hint uses the name `serena-local`, which the rule never removes. Phase 1's Tier R `serena` rows get the same "absent or `{}`" wording (Phase 1 amendment list, T0b).
- When not ready: Phase 1's behaviour is unchanged (Tier K kept, hint printed); Tier R rows and the `/usr/local/bin/codebase-memory-mcp` entry are still removed unconditionally (Phase 1 §3.2).
- Local-scope (`projects.*.mcpServers`) and `.mcp.json` entries are reported with the exact command, never removed (Phase 1 §3.3).
- Kept by policy and stated in docs and CHANGELOG: `~/.serena`, project `.serena/`, `~/.cache/codebase-memory-mcp`, the uv cache, and (off Coder) a user-installed `serena-agent` uv tool, for which the removal command is printed.

When "completely absent" holds:

| Where | Registrations | Programs |
|---|---|---|
| Non-Coder machine | right after `./update.sh` | Serena: IronClaude never installed it; a user `uv tool` copy is reported. codebase-memory kind-B binary: stays with a printed `uninstall` command (escalated, see below) |
| Coder workspace | right after `./update.sh` or the slug run, and they stay absent once the workspace runs the Coder step-2 image (bundle no longer re-adds) | Serena programs: removed by the step-2 image/migration; `/usr/local/bin/codebase-memory-mcp`: removed by the step-5 image |

Not reachable by `./update.sh` alone, escalated to the coordinator by the debate (its invariants INV-001, INV-002): the root-owned baked `/usr/local/bin/codebase-memory-mcp` (only a new image removes it) and a kind-B upstream-installed `~/.local/bin/codebase-memory-mcp` with its client companions (removing them would reopen Phase 1's decision D2).

Acceptance (after every Claude session has restarted):
- user scope, by name and by launcher shape: `jq -e '(.mcpServers // {}) | (has("serena") or has("codebase-memory-mcp") or (to_entries | map(select(.key != "serena-local" and ((.value.args // []) | tostring | test("serena-agent|start-mcp-server")))) | length > 0)) | not' ~/.claude.json`; a failure caused by an entry the retire step reported as kept (non-empty `env`/`headers`, or a Serena launcher without `start-mcp-server`) means the user runs the printed command;
- local scope (`projects.*.mcpServers`, never removed automatically, §3.3 of Phase 1): `jq -e '[(.projects // {}) | .[] | (.mcpServers // {}) | has("serena") or has("codebase-memory-mcp")] | any | not' ~/.claude.json`; a failure here means the user must run the printed `claude mcp remove <name> --scope local` command, not that the plan failed;
- on Coder, as user `coder`, once the image's IronClaude pin includes the merge and the step-5 image is running: `! command -v serena && ! command -v codebase-memory-mcp`.

Residual risk: if Coder's `timeout 60` kills a later codegraph remove-then-add after Serena is gone, neither server is registered until the next run (see the UNVERIFIED retry question in §2.4).

## 3. Project indexing and sync

Decided by `/sc:adversarial --depth quick` (`.dev/codegraph-migration/decisions/P2-indexing-sync/adversarial/P2-indexing-sync-merged.md`; options `option-a.md` guidance only, `option-b.md` SessionStart hook, `option-c.md` global git template hooks; scores B 0.886, A 0.756, C 0.736; convergence 18/18). The debate's open questions and two review rounds were then settled by sandbox probes (`decisions/P2-indexing-sync/probe-results.md`, rows 1-12). The probes simplified the hook to "start one `init` when `.codegraph/codegraph.db` is absent": `status`, `index` and `sync` can destroy a concurrent run (rows 6, 7), while concurrent inits are harmless (rows 2, 3) and the MCP daemon heals an interrupted init (row 9). The debate's completion marker and every repair branch were dropped (D21).

### 3.1 How a checkout gets and keeps an index

| Situation | What happens |
|---|---|
| First Claude session in a checkout (clone, sibling worktree, nested worktree, new project) | IronClaude's SessionStart hook (3.2) starts `codegraph init --yes` in the background at the git top-level. Each worktree gets its own index. |
| Session opened before that init finished | Before `.codegraph/` exists, codegraph tools reply "No CodeGraph project is loaded for this session" (probe 10); the agent uses Read/Grep (3.4). In the real order (session connects first, init starts after), early tool calls may return "No CodeGraph project is loaded" or a partial answer even after `.codegraph/` appears; later calls in the same session are complete and the index ends complete (probes 8 and 11). The guidance (3.4) says so. |
| Edits while a session is open | The codegraph daemon's file watcher (2 s debounce) keeps the index fresh (W4 §5.7). |
| Edits, pulls, branch switches with no session open | Caught up by codegraph's connect-time scan when the next MCP client connects (W4 §4). No git hook needed. |
| Interrupted init (killed, OOM, reboot) | `.codegraph/codegraph.db` exists, so the hook does nothing; the next session's MCP server (every session that loads MCP servers connects to the user-scope entry; `alwaysLoad` only keeps the tools listed rather than deferred behind tool search, `research/codegraph-evaluation.md:77`) heals the truncated index (probe 9: 0 → 904 files, no warning, within 50 s). |
| Second session while the first session's init still runs | `.codegraph/codegraph.db` may already exist (hook exits) or not yet (a second `init` starts; harmless, probes 2-3). |
| Index built by someone else (Coder, the user, an agent) | `.codegraph/codegraph.db` exists: the hook does nothing. |
| Fresh clone of a repo that committed `.codegraph/.gitignore` | No database: the hook runs `init` (the MCP server cannot build from an empty `.codegraph/`). IronClaude's own `.gitignore` ignores `.codegraph/` (F19). |
| Non-git directory, `$HOME`, `/` | Never indexed automatically. |

IronClaude writes no global git config and installs no git hooks. A user-installed `post-checkout` recipe (background `codegraph init --yes … || true`, never `sync`) is documented as opt-in only (F8).

### 3.2 The hook (`src/superclaude/hooks/scripts/codegraph-session-start.sh`)

Registered in `src/superclaude/hooks/hooks.json` under `SessionStart` with `"matcher": "startup"` and `"timeout": 5`, command `~/.claude/hooks/codegraph-session-start.sh`; same entry in `plugins/superclaude/hooks/hooks.json`; script copied to `plugins/superclaude/hooks/scripts/`; name added to `_FRESHNESS_SCRIPTS` (`install_hooks.py:42-79`, required by `make verify-sync`).

Behaviour (POSIX `sh`, always exit 0, prints nothing on stdout, never calls `codegraph` in the foreground):
1. Exit if `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`.
2. Binary: `cg=$(cat "$HOME/.codegraph/.superclaude-bin" 2>/dev/null)` (the installer's pointer to the registered binary, §2.2); if that is not an executable file, `cg=$(command -v codegraph)`; if neither, exit. This keeps the hook on the same version as the MCP server even when `~/.local/bin` is not on `PATH`.
3. `top=$(git -C "${CLAUDE_PROJECT_DIR:-$PWD}" rev-parse --show-toplevel 2>/dev/null)` or exit; exit if `top` is empty, `$HOME` or `/`.
4. Exit if `$top/.codegraph/codegraph.db` exists (any state: complete, building, truncated, built by anyone). A `.codegraph/` without a database (for example a committed `.codegraph/.gitignore` in a fresh clone) does not count: the MCP server cannot build from it, but `init --yes` does (third review finding 5). A second init racing one that just created the database is harmless (probes 2-3).
5. `log="${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/codegraph-init.log"`; `mkdir -p "${log%/*}" || exit 0`.
6. `nohup "$cg" init --yes "$top" </dev/null >>"$log" 2>&1 &` (every descriptor redirected so Claude Code does not wait; no `setsid`, which macOS lacks).

Nothing else: no marker, no PID file, no lock, no `status`, `index` or `sync` (probe rows 6-7 show each can destroy a concurrent run). Two hooks racing on a new checkout start two inits, which is harmless (rows 2-3). An interrupted init leaves a truncated `.codegraph/` that the next MCP connection heals (row 9). `codegraph uninit` removes `.codegraph/`, so the next session re-indexes.

The `startup` matcher also fires for headless `claude -p` sessions that IronClaude pipelines start (sprint, swarm, cliEval); each new checkout they open gets one background init (up to ~1 GB). Docs (F8) tell pipeline and CI users to set `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`.

Hook tests (`tests/cli/test_install_hooks.py` registration test plus a new `tests/cli/test_codegraph_session_start_hook.py` that runs the script with `subprocess` against a stub `codegraph` in `tmp_path` that appends its argv to a file, with `HOME` and `XDG_STATE_HOME` in `tmp_path`): opt-out exits silently; no binary anywhere exits silently; the pointer file wins over a different `codegraph` on `PATH`; a pointer to a missing file falls back to `PATH`; non-git dir runs nothing; `$HOME` as top runs nothing; an existing `.codegraph/codegraph.db` runs nothing; a `.codegraph/` holding only `.gitignore` runs `init` once; otherwise exactly `init --yes <top>` is run once; a `top` with spaces is passed as one argument; stdout is always empty and exit 0; the hook returns in under 1 s even when the stub sleeps 10 s (detach works). `tests/unit/test_cli_install.py:140-145` packaged-script listing gains the script. The real hook with the real binary runs in layer 2 (§4.2 step 6b). UNVERIFIED: whether Claude Code kills the hook's process group when the hook exits or the session ends (no `setsid`); layer 2 checks only the hook run outside Claude Code, and T9 records the observed behaviour inside a real session if one is available.

### 3.3 Cost disclosed in docs

About 70 KB on disk per indexed file and up to ~1 GB peak memory during init (W4 §4, §5.4); seconds for small repos, about 100 s for 27k files (upstream). Opt out per user with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` in the environment (or in `~/.claude/settings.json` `env`), recommended for CI and headless pipelines; per project with `codegraph.json` excludes. The docs state its scope exactly: it disables only the session-start index hook (§3.2), not the MCP server, the installer phase or any primitive. Every IronClaude codegraph switch uses the `SUPERCLAUDE_CODEGRAPH_` prefix; Phase 3 owns any primitive-level switch and its name (review finding X-14).

### 3.4 Core CLAUDE.md guidance (F6)

MCP table row: `| codegraph      | Code graph: symbols, callers, impact, file outlines | (auto) |`.

Exactly one table row starts with `| codegraph`; Phase 3 edits this row in place (for example to add the guide path) and never adds a second one (review finding X-9).

Guidance block (under the MCP table), written between two marker lines that stand alone on their own lines, exactly `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` before the block and `<!-- SUPERCLAUDE_CODEGRAPH_END -->` after it (each appears once in the file; neither contains upstream's `CODEGRAPH_START` text, so the §2.7 doctor detail line does not fire on it). The markers let Coder replace the block mechanically on every pin bump (§3.4 "Coder gap"); anything Coder users must see goes inside them, because the MCP table row never reaches Coder.

> **codegraph.** For code-structure questions use the codegraph MCP tools: `codegraph_search` (find a symbol by name), `codegraph_node` (one symbol, or a file's outline), `codegraph_callers` and `codegraph_callees`, `codegraph_impact` (what a change reaches) and `codegraph_files`; `codegraph_status` says whether this checkout is indexed. If a codegraph tool says "No CodeGraph project is loaded for this session" or that the index belongs to a different working tree, use Read/Grep for now and run `codegraph init --yes` in the directory printed by `git rev-parse --show-toplevel` (safe to repeat; a session-start hook usually does this already). Run codegraph as the path in `~/.codegraph/.superclaude-bin` when that file exists, else as `codegraph`. Never run `codegraph status`, `codegraph index` or `codegraph sync` while an init or index may be running (`pgrep -f 'codegraph\.js (init|index)'` prints a line): they can empty the index. An interrupted index is repaired by the codegraph MCP server on its next connection. In a checkout indexed for the first time, answers in the first minute can be missing or incomplete; ask again after the init finishes. codegraph tools are read-only; edit with Edit/Write.

If T2 step 0 selected `MCP_TOOLS = "status"`, the first sentence is instead: "codegraph lists only `codegraph_status` in sessions; use Read/Grep for code-structure questions." The block never names `codegraph_explore` (it is hidden by the tool list, §2.4, and banned by Phase 3 P3-D9).

Phase 3 owns any later wording change inside the markers (its task T2); Phase 2 owns only the text above and the markers.

**Coder gap.** On Coder workspaces this text does not reach the user: Coder's `ironclaude` slug saves `~/.claude/CLAUDE.md` before `superclaude install` and restores it byte for byte afterwards (Coder `T/catalogue/ironclaude/install.sh:44-66,112-125`, W5 §1.7). The hook still runs there (it is installed under `~/.claude/hooks/` and registered in `settings.json`, which Coder keeps), but the fallback rule does not. The Coder handoff therefore requires Coder, on every IronClaude pin bump, to copy the lines from `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` to `<!-- SUPERCLAUDE_CODEGRAPH_END -->` (inclusive) out of IronClaude `src/superclaude/core/CLAUDE.md` at the pinned SHA, and to replace the same marked lines in its seed `T/workspace_defaults/CLAUDE.md` and in existing workspaces' `~/.claude/CLAUDE.md` (append the marked lines when no marker is present). That keeps Coder in step when Phase 3 or later releases change the block (review findings X-2, X-10). IronClaude does not work around this.

## 4. Validation plan

Two layers. Layer 1 runs in every `uv run pytest` and never touches the network, the real HOME or the real `claude` CLI. Layer 2 is a real install, index and query inside a throwaway HOME.

### 4.1 Layer 1: unit tests (mocked subprocess and network)

Conventions to follow (read for this spec at `55d40308`; Phase 1 deletes these lines, so read them with `git show 55d40308:tests/cli/test_install_mcp_tavily.py`): fixtures set `HOME` and `CLAUDE_CONFIG_DIR` to `tmp_path` dirs and patch `platform.system/machine` (`:383-410`); a fake replaces the command runner, records argv, asserts `timeout <= 60` and `cmd[-2:] == ["--scope", "user"]`, and edits the fixture `~/.claude.json` like the real CLI would (`:411-468`, installed at `:468`); anything that would reach a real process or download calls `pytest.fail` (`:410-416`; `tests/cli/test_update_command.py:52-63` at `55d40308`). Because the phase uses the bounded argv runner (§2.4), the tests patch that runner (not `_run_command`) with the same recording fake.

`tests/cli/test_install_codegraph.py` (new). The download is faked by patching one function, `install_codegraph._download(url, dest, timeout)`, that writes bytes from a fixture tarball built in `tmp_path` with `tarfile` (a `bin/codegraph` shell stub that prints `1.6.2`). Cases:

| # | Case | Expect |
|---|---|---|
| U1 | `asset_name()` for Linux x86_64/amd64/aarch64/arm64 and Darwin x86_64/arm64 | the four asset names; Windows/FreeBSD/armv7 → None |
| U2 | `SHA256` table has exactly the four assets and 64-hex values; `TAG == "v" + VERSION`; `MCP_TOOLS` equals the value recorded in `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md` (T2 step 0) and does not contain `explore` | pin integrity |
| U3 | PATH has a `codegraph` printing `1.6.2` | reused; `_download` never called |
| U4 | PATH copy prints `1.5.0`, `~/.local/bin/codegraph` prints `1.6.2` | the `~/.local/bin` one wins |
| U5 | no matching copy; download bytes match the pinned hash | extracted to `~/.codegraph/versions/v1.6.2/`, `~/.local/bin/codegraph` and `~/.codegraph/current` link to it, version check passes |
| U6 | download bytes do not match | stage `checksum` failure; nothing left under `~/.codegraph/versions/`; no link changed |
| U7 | tarball member with `..` or absolute path or a symlink escaping the target | rejected before extraction (stage `extract`) |
| U8 | download raises `URLError`/timeout | stage `download` failure, message names the URL and the manual recovery, no traceback |
| U9 | unsupported platform with no matching PATH copy | failure names the platform; no download attempted |
| U10 | unsupported platform **with** a matching PATH copy | success (reuse is platform-neutral) |
| U11 | `claude --version` fails | failure before discovery or download (same rule as `install_mcp.py:830-843`) |
| U12 | registration absent | one `claude mcp add-json codegraph <json> --scope user`; JSON equals §2.4 with the realpath of the winner, including `env.CODEGRAPH_MCP_TOOLS == install_codegraph.MCP_TOOLS` |
| U13 | registration already equal | no `claude mcp` call after `--version` (idempotent) |
| U14 | registration differs (old path, missing `alwaysLoad`, old version dir, env without `CODEGRAPH_MCP_TOOLS` as Coder or an earlier plan wrote it) | `remove` then `add-json`; re-read verifies |
| U15 | add fails / verification fails | previous entry restored; message says so |
| U16 | user-managed entry (extra env key, `headers`, `url`, other args): command resolves / does not resolve | kept, phase passes with the `claude mcp remove` hint / phase fails with that hint; never replaced either way (§2.4) |
| U17 | `~/.claude.json` unreadable or has duplicate keys | lookup failure; no `claude mcp` mutation |
| U18 | `dry_run=True` | describes the plan; no download, no `claude` call, no file written |
| U19 | second run after a successful download | reuse, zero downloads, zero registry mutations |
| U20 | receipt written only after a verified download (not for a reused PATH copy); corrupt receipt deletes nothing and does not fail | §2.6 |
| U21 | pin bump: new dir installed, owned links flipped, previous owned dir kept; next run deletes it only when nothing registered or linked resolves inside it | §2.6 |
| U22 | a non-owned `~/.local/bin/codegraph` pointing elsewhere is left alone and the version dir's launcher is registered | §2.3 step 6 |
| U23 | `superclaude mcp --servers codegraph --dry-run` | no download, no `claude mcp` call |
| U24 | pointer file `~/.codegraph/.superclaude-bin` holds the winner's realpath (baked and downloaded cases); rewritten only on change; a winner that is not the shell's `command -v codegraph` prints the PATH warning and still passes | §2.2 |
| U25 | the bounded runner kills a `claude` stub that ignores SIGTERM after the timeout (process group gone) | §2.4 |

`tests/cli/test_update_command.py` additions: the codegraph phase runs after user setup and before the retire step (insert it into the expected call list Phase 1 leaves, which ends with user setup and the retire step); the retire step still runs when the codegraph phase fails; a failing phase keeps framework work and exits 1 with the stage on stderr; `install --force` calls the phase with `scope="user"` only (no force); `install --list` prints the codegraph block and calls neither `_download` nor `claude mcp`.
`tests/cli/test_install_mcp_registry.py` additions: `MCP_SERVERS["codegraph"]` contract; `install_mcp_server(MCP_SERVERS["codegraph"])` calls `install_codegraph_mcp(scope=…, dry_run=…)` and never the generic `claude mcp add --transport` path.
`tests/unit/test_cli_doctor.py` additions: per §2.7.
Hook tests (only if §3 ships a hook): per §3.

Acceptance for layer 1:

```bash
uv run pytest tests/cli/test_install_codegraph.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py tests/unit/test_cli_doctor.py tests/cli/test_update_script.py -q -p no:cacheprovider
```

### 4.2 Layer 2: real install, index and query in an isolated HOME

Reuses the W4 sandbox recipe (`research/codegraph-evaluation.md` §5: private `mktemp -d`, sandbox `HOME`, telemetry off). Run from the worktree root after task T5 (§5) with `bash .dev/codegraph-migration/evidence/p2-layer2.sh` (T9 saves the script below to that path first). It needs network to GitHub, a working `claude` CLI and an already-synced `.venv` (`uv sync` once beforehand). It never touches the real `~/.claude.json`: `HOME` and `CLAUDE_CONFIG_DIR` point into the sandbox, and the script proves it by hashing the real file before and after. `PATH` is rebuilt from a shim directory so a Coder-baked `/usr/local/bin/codegraph` stays hidden while `claude`, `uv`, `git`, `jq` and `node` (which live in `/usr/local/bin` on Coder) stay usable. Every "expect" is an assertion: the script exits non-zero at the first one that fails (negative checks use `if …; then exit 1; fi`, because `set -e` ignores a failing `! cmd`; checks read saved output instead of `tee | grep -q`, which can fail on SIGPIPE under `pipefail`).

```bash
#!/usr/bin/env bash
set -euo pipefail
R=$(git rev-parse --show-toplevel)
EV="$R/.dev/codegraph-migration/evidence/P2-layer2.md"
REAL_HOME="$HOME"; REAL_SUM=$(jq -S '.mcpServers' "$REAL_HOME/.claude.json" | sha256sum | cut -d' ' -f1)   # only MCP servers: live sessions rewrite the rest of the file
S=$(mktemp -d /tmp/p2-codegraph-it.XXXXXXXX); chmod 700 "$S"
trap 'cd /; pkill -f "$S/home/.codegraph" || true; rm -rf "$S"' EXIT
mkdir -p "$S/bin"
for t in claude uv git jq node sha256sum; do p=$(command -v "$t") && ln -s "$p" "$S/bin/$t"; done
export UV_CACHE_DIR="$(uv cache dir)"                                     # keep uv's real cache; only HOME moves
export HOME="$S/home" CLAUDE_CONFIG_DIR="$S/home" CODEGRAPH_TELEMETRY=0 DO_NOT_TRACK=1 CODEGRAPH_NO_UPDATE_CHECK=1
export PATH="$S/bin:$HOME/.local/bin:/usr/bin:/bin"
mkdir -p "$HOME"; echo '{"mcpServers":{}}' > "$HOME/.claude.json"
if command -v codegraph >/dev/null; then echo "codegraph visible on PATH; download path would not run" >&2; exit 1; fi
PHASE='from superclaude.cli.install_mcp import install_codegraph_mcp as f; ok,msg=f(); print(msg); raise SystemExit(0 if ok else 1)'
{ echo "# P2 layer 2 evidence $(date -u +%FT%TZ)"; echo '```text'; } > "$EV"

# 1. install through IronClaude's phase (download + verify + register)
uv run --no-sync --project "$R" python -c "$PHASE" | tee -a "$EV"
test "$("$HOME/.local/bin/codegraph" --version)" = 1.6.2
CG=$(readlink -f "$HOME/.local/bin/codegraph"); echo "launcher realpath: $CG" | tee -a "$EV"
jq -e --arg c "$CG" '.mcpServers.codegraph | .command == $c and .args == ["serve","--mcp"]' "$HOME/.claude.json" | tee -a "$EV"
MT=$(uv run --no-sync --project "$R" python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print(MCP_TOOLS)')
jq -e --arg t "$MT" '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS == $t' "$HOME/.claude.json" | tee -a "$EV"   # X-1: tool list registered
jq '.mcpServers.codegraph' "$HOME/.claude.json" | tee -a "$EV"
diff <(jq -S 'del(.command)' "$R/.dev/codegraph-migration/evidence/P2-add-json-shape.json") <(jq -S '.mcpServers.codegraph | del(.command)' "$HOME/.claude.json")   # same stored shape as the T2 probe
# 2. idempotency: a second run with a dead proxy makes no download and no registry change
cp "$HOME/.claude.json" "$S/before.json"; ls "$HOME/.codegraph/versions" > "$S/versions.before"
https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 uv run --no-sync --project "$R" python -c "$PHASE" | tee -a "$EV"
cmp "$S/before.json" "$HOME/.claude.json"
ls "$HOME/.codegraph/versions" | cmp - "$S/versions.before"
# 3. offline reuse (the Coder path): a baked-style copy on PATH, no ~/.local/bin link, dead proxy
mkdir -p "$S/baked"; ln -s "$CG" "$S/baked/codegraph"; rm "$HOME/.local/bin/codegraph"
PATH="$S/baked:$PATH" https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 uv run --no-sync --project "$R" python -c "$PHASE" | tee -a "$EV"
jq -e --arg c "$CG" '.mcpServers.codegraph.command == $c' "$HOME/.claude.json"
ls "$HOME/.codegraph/versions" | cmp - "$S/versions.before"
ln -s "$CG" "$HOME/.local/bin/codegraph"
# 4. real index + query on an isolated copy of this worktree (never index the real worktree from the sandbox)
git clone -q --no-hardlinks "$R" "$S/project"; cd "$S/project"
codegraph init --yes | tail -3 | tee -a "$EV"
codegraph status > "$S/status.txt"; cat "$S/status.txt" >> "$EV"
grep 'Index is up to date' "$S/status.txt" >/dev/null
if grep 'never finished' "$S/status.txt" >/dev/null; then echo "index truncated" >&2; exit 1; fi
codegraph query install_codegraph_mcp > "$S/q.txt"; cat "$S/q.txt" >> "$EV"; grep 'src/superclaude/cli/install_mcp.py' "$S/q.txt" >/dev/null
codegraph callers install_codegraph_mcp > "$S/c.txt"; cat "$S/c.txt" >> "$EV"; grep 'src/superclaude/cli/main.py' "$S/c.txt" >/dev/null
# 5. the registered MCP entry starts and answers
claude mcp get codegraph > "$S/get.txt"; cat "$S/get.txt" >> "$EV"; grep -i 'connected' "$S/get.txt" >/dev/null
if grep -iE 'disconnected|not connected|failed' "$S/get.txt" >/dev/null; then echo "MCP server not connected" >&2; exit 1; fi
# 5b. the registered tool list: exactly the MCP_TOOLS tools are listed, explore is absent and a call to it fails (X-1, X-25)
CODEGRAPH_MCP_TOOLS="$MT" node "$R/.dev/codegraph-migration/evidence/p2-mcp-tools.mjs" "$CG" "$S/project" "$S/tools.json"
jq '{names: (.tools | map(.name)), tools_bytes, instructions_bytes, explore_call_error}' "$S/tools.json" | tee -a "$EV"
jq -e --arg t "$MT" '((.tools | map(.name) | sort) == ($t | split(",") | map("codegraph_" + .) | sort)) and .explore_call_error == true' "$S/tools.json"
cd "$R"
# 6. retire after codegraph is ready: seed the current-pin Serena entry and a kind-B codebase-memory entry, run the full install in the sandbox
SER='{"type":"stdio","command":"uvx","args":["--from","serena-agent==1.7.0","serena","start-mcp-server","--context","claude-code","--project-from-cwd","--enable-web-dashboard","false","--enable-gui-log-window","false"],"env":{}}'   # exact live shape, incl. "env":{}
CBM="{\"type\":\"stdio\",\"command\":\"$HOME/.local/bin/codebase-memory-mcp\",\"args\":[]}"
printf '#!/bin/sh\necho "codebase-memory-mcp 0.12.1"\n' > "$HOME/.local/bin/codebase-memory-mcp"; chmod 755 "$HOME/.local/bin/codebase-memory-mcp"   # kind-B binary present
jq --argjson s "$SER" --argjson c "$CBM" '.mcpServers.serena=$s | .mcpServers["codebase-memory-mcp"]=$c' "$HOME/.claude.json" > "$S/seed.json"
cp "$S/seed.json" "$HOME/.claude.json"
jq -e '.mcpServers | has("serena") and has("codebase-memory-mcp")' "$HOME/.claude.json"   # seeding really happened
if ! uv run --no-sync --project "$R" superclaude install > "$S/install.txt" 2>&1; then cat "$S/install.txt" >> "$EV"; echo "install failed" >&2; exit 1; fi
cat "$S/install.txt" >> "$EV"
jq -e '(.mcpServers | has("serena") or has("codebase-memory-mcp")) | not' "$HOME/.claude.json"
jq -e '.mcpServers | has("codegraph")' "$HOME/.claude.json"
test -x "$HOME/.local/bin/codebase-memory-mcp"                             # kind-B binary itself is left in place
grep 'uninstall -y' "$S/install.txt" >/dev/null                             # and its upstream uninstall command is printed
grep -F 'serena-agent==1.7.0' "$S/install.txt" >/dev/null                     # the removed Serena argv is printed (§2.12)
# 6b. the real installed hook, real binary, on a fresh clone (outside Claude Code)
git clone -q --no-hardlinks "$R" "$S/project2"
out=$(CLAUDE_PROJECT_DIR="$S/project2" sh "$HOME/.claude/hooks/codegraph-session-start.sh"); test -z "$out"
n=0; until pgrep -f "codegraph\.js init --yes $S/project2" >/dev/null; do n=$((n+1)); test $n -le 20; sleep 0.1; done   # started within 2 s
n=0; while pgrep -f "codegraph\.js init --yes $S/project2" >/dev/null; do n=$((n+1)); test $n -le 300; sleep 1; done   # finished within 300 s
(cd "$S/project2" && codegraph status) > "$S/status2.txt"; grep 'Index is up to date' "$S/status2.txt" >/dev/null
if grep 'never finished' "$S/status2.txt" >/dev/null; then echo "hook init truncated" >&2; exit 1; fi
# 7. same seeds with codegraph unavailable: install exits 1 at the codegraph stage, Serena and the kind-B entry are kept
H2="$S/home2"; mkdir -p "$H2/.local/bin"; cp "$HOME/.local/bin/codebase-memory-mcp" "$H2/.local/bin/"
CBM2="{\"type\":\"stdio\",\"command\":\"$H2/.local/bin/codebase-memory-mcp\",\"args\":[]}"
jq -n --argjson s "$SER" --argjson c "$CBM2" '{mcpServers:{serena:$s, "codebase-memory-mcp":$c}}' > "$H2/.claude.json"
if HOME="$H2" CLAUDE_CONFIG_DIR="$H2" PATH="$S/bin:/usr/bin:/bin" https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 uv run --no-sync --project "$R" superclaude install > "$S/install2.txt" 2>&1; then echo "install passed without codegraph" >&2; exit 1; fi
cat "$S/install2.txt" >> "$EV"
grep -i 'codegraph' "$S/install2.txt" | grep -i 'download' >/dev/null        # it failed at the codegraph download stage
jq -e '.mcpServers | has("serena") and has("codebase-memory-mcp")' "$H2/.claude.json"
echo '```' >> "$EV"
# 8. the real HOME was not touched
test "$(jq -S '.mcpServers' "$REAL_HOME/.claude.json" | sha256sum | cut -d' ' -f1)" = "$REAL_SUM"
echo "LAYER2_OK" | tee -a "$EV"
```

Notes: `git clone` of the worktree includes only committed files, so commit T5 first (steps 6-6b need T3b's retire gate and T5's hook). `claude mcp get` on an isolated `CLAUDE_CONFIG_DIR` is UNVERIFIED (W1 avoided `claude mcp list` because it starts servers; that is acceptable inside the sandbox); if it cannot run there, replace step 5 with a JSON-RPC `initialize` + `tools/list` over stdio against `"$CG" serve --mcp` (W4 §5.6 did this with a small Node client, `/tmp/codegraph-eval.fQfO/scripts/mcp-client.mjs`) and assert `serverInfo.name == "codegraph"` (step 5b already covers the tool list: `codegraph_explore` absent, the `MCP_TOOLS` tools present). If the T2 probe showed the CLI stores the entry differently, adjust the step-1 `jq -e` to the stored fields.

Record the outputs (the evidence file, timings) in the G4 issue comment (§6). Layer 2 is run by the executor once per release of this phase, not in CI. CI gets a real install through the `doctor-check` job (F12).

## 5. Task breakdown (execution order)

Preconditions: on branch `ironbelly/feat-codememory-codegraph-init`, Phase 1 tasks committed, `git status --short` clean apart from untracked `.dev/` content. Record a baseline before T1, because the full suite was not green at `55d40308` (W1 §4.0: 27 failed, 16 errors, all outside the files this phase touches, several caused by a missing `make sync-dev` mirror):

```bash
mkdir -p .dev/codegraph-migration/evidence
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > .dev/codegraph-migration/evidence/P2-baseline-failures.txt   # brace groups: a failing suite must not abort the baseline under pipefail
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json
```

"Green" for the final gate means: the sorted list of failing test ids is a subset of `P2-baseline-failures.txt` (T10 diffs them), so a new failure that replaces an old one is caught. The baseline file is committed with T0.

### G0: publish the plan and start the Coder work

**T0. Commit the planning files and hand off to Coder.**
Files: `.dev/codegraph-migration/` (specs, handoff, decisions, evidence baseline), staged with `git add .dev/codegraph-migration` (never `.claude/`).
Change: commit and push the branch so the Coder agent can fetch the handoff (`.dev/codegraph-migration/` is untracked when this spec was written, so `gh api …/contents/…` would 404). Then post an issue comment that links `handoff/coder-handoff-prompt.md` on the branch and asks for the Coder work to start (human step 5 in §7: giving the prompt to an agent in the Coder repo).
Acceptance:
```bash
git ls-files --error-unmatch .dev/codegraph-migration/handoff/coder-handoff-prompt.md .dev/codegraph-migration/handoff/coder-handoff-context.md
gh api "repos/IronbellyOrg/IronClaude/contents/.dev/codegraph-migration/handoff/coder-handoff-prompt.md?ref=ironbelly/feat-codememory-codegraph-init" --jq .name    # expect: coder-handoff-prompt.md
```
Commit: `docs(plan): Phase 2 codegraph install spec and Coder handoff (#323)`, then `git push origin ironbelly/feat-codememory-codegraph-init`.

Every acceptance block below is run from the worktree root under `set -euo pipefail` (for example `bash -euo pipefail <<'EOF' … EOF`) and must exit 0 if and only if its criterion passes: every line must exit 0, so a block that passes only on its last line has failed. One condition per line: `set -e` ignores a failing left side of `A && B` and any `! cmd` unless it is the last line, so write a negative check as `if cmd; then exit 1; fi` (sc:reflect finding M-09). Every `uv run pytest` below uses `-p no:cacheprovider`. Run `git status --short` after each task; a modified tracked file the task did not intend to change is a defect to fix before committing.

**T0b. Align Phase 1's spec and facts file with §2.12.**
Owner: the coordinator's finalizer for Phase 1 if it runs before Phase 1 is executed (preferred, so Phase 1 implements the right hint and CHANGELOG text); otherwise the Phase 2 executor here. Reported to the coordinator in this task's completion message.
Change: edit each listed Phase 1 row so it states the §2.12 gate (the current-pin Serena entry is kept only until `codegraph_ready()`; Tier R and Tier K match `env`/`headers` absent or `{}`; the re-register hint uses `serena-local`), and append the override section to the facts file.
Files: `.dev/codegraph-migration/specs/phase-1-removal-spec.md` (its DoD-3, §2.3 row, §3.2 Tier K and Tier R "env/headers absent or `{}`", §3.4 hint renamed to `serena-local`, §3.6 closing condition, the sandbox expectation "Legacy Serena registration kept", D2: each gains "until Phase 2's `codegraph_ready()` gate removes it", pointing at this spec §2.12); `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md` (append a "Phase 2 override: Serena removal" section quoting §2.12), if Phase 1 T15 has written it.
Acceptance:
```bash
test "$(rg -c 'codegraph_ready' .dev/codegraph-migration/specs/phase-1-removal-spec.md)" -ge 7   # one line per amended row: DoD-3, §2.3, §3.2, §3.4, §3.6, sandbox expectation, D2
rg -q 'serena-local' .dev/codegraph-migration/specs/phase-1-removal-spec.md
rg -q 'Tier R \(removed\).*absent or `\{\}`' .dev/codegraph-migration/specs/phase-1-removal-spec.md   # Tier R line amended
rg -q 'Tier K \(kept.*absent or `\{\}`' .dev/codegraph-migration/specs/phase-1-removal-spec.md      # Tier K line amended
test ! -e .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md || rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md
```
Commit: `docs(plan): align Phase 1 retire rules with the Phase 2 codegraph gate (#323)`. T3b re-runs the last acceptance line after Phase 1 T15, and T7 checks that Phase 1's CHANGELOG entry does not say the current-pin Serena entry is kept for good (T7's last acceptance line: no `Legacy Serena registration kept` line, or that line also names codegraph).

### G1: installer core

**T1. Pin and verified acquisition module.**
Files: `src/superclaude/cli/install_codegraph.py` (new), `tests/cli/test_install_codegraph.py` (new).
Also: `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs` and `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md` (both from T2 step 0, run before this task).
Change: §2.2, §2.3, §2.6 (receipt and pruning), §2.11 module shape, `MCP_TOOLS` set from the `Selected MCP_TOOLS:` line of the step-0 evidence file; tests U1-U10, U20-U22, U24 (U11 tests the phase function's `claude --version` check, so it lives in T2). First run T2 step 0 (the tool-list schema-cost check), then re-check the pin (a mismatch means stop: §7 item 2):
```bash
gh release download v1.6.2 -R colbymchenry/codegraph -p SHA256SUMS -D /tmp/p2-sums --clobber
grep -E 'codegraph-(linux|darwin)-(x64|arm64)\.tar\.gz$' /tmp/p2-sums/SHA256SUMS | sort | diff - <(sort <<'EOF'
ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828  codegraph-linux-x64.tar.gz
c8c6be292be21d00dea26bad8b28d434731cf612fb8cc475dc10f5b3038b5b64  codegraph-linux-arm64.tar.gz
53d1a4d1a9af31d6cec11b346df2ae792087081e13f623f583e27783c1e7f9bc  codegraph-darwin-x64.tar.gz
d74d1bfb4060db63ec3c2b72c4e17f76c31978af3bad6ace4370d1501ac0662e  codegraph-darwin-arm64.tar.gz
EOF
)                                                                    # expect: no output, exit 0
```
Acceptance:
```bash
uv run pytest tests/cli/test_install_codegraph.py -q -p no:cacheprovider
uv run ruff check src/superclaude/cli/install_codegraph.py tests/cli/test_install_codegraph.py
```
Commit: `feat(install): add pinned, checksum-verified codegraph acquisition`

**T2. Phase function, registry entry, dispatch, registration helpers.**
Files: `src/superclaude/cli/install_mcp.py`, `tests/cli/test_install_codegraph.py`, `tests/cli/test_install_mcp_registry.py`.
Change: F2 (a)-(e); §2.4 table and bounded runner; tests U11-U19, U23, U25 and the registry/dispatch tests (§4.1).
Step 0, tool-list schema-cost check (§2.4 "Tool list"; review X-1, X-25), before any code. Method chosen by `/sc:adversarial --depth quick` (`decisions/F2-schema-cost-method/recommendation.md`; A 0.870, C 0.829, B 0.701; convergence 15/15); the merged method `decisions/F2-schema-cost-method/adversarial/F2-schema-cost-method-merged.md` §1-§7 is authoritative for every detail below.
1. Save this stdio client as `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs` (committed with T1, like the evidence file; layer 2 step 5b reuses it). Usage `node p2-mcp-tools.mjs <codegraph-bin> <project-dir> <out.json>`; the env passes through.
   ```js
   import { spawn } from 'node:child_process';
   import { writeFileSync } from 'node:fs';
   const [, , bin, dir, out] = process.argv;
   const child = spawn(bin, ['serve', '--mcp'], { cwd: dir, env: process.env, stdio: ['pipe', 'pipe', 'inherit'] });
   const waiting = new Map(); let buf = ''; let id = 0;
   child.stdout.on('data', (d) => {
     buf += d;
     for (let i; (i = buf.indexOf('\n')) >= 0; buf = buf.slice(i + 1)) {
       let m; try { m = JSON.parse(buf.slice(0, i)); } catch { continue; }
       if (waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
     }
   });
   const rpc = (method, params) => new Promise((ok, no) => {
     const n = ++id; const t = setTimeout(() => no(new Error('timeout ' + method)), 60000);
     waiting.set(n, (m) => { clearTimeout(t); ok(m); });
     child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: n, method, params }) + '\n');
   });
   const bytes = (v) => Buffer.byteLength(typeof v === 'string' ? v : JSON.stringify(v));
   const init = await rpc('initialize', { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'p2-check', version: '0' } });
   child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
   const tools = (await rpc('tools/list', {})).result.tools;
   const ex = await rpc('tools/call', { name: 'codegraph_explore', arguments: { query: 'main' } });
   writeFileSync(out, JSON.stringify({
     server: init.result.serverInfo, tools,
     tools_bytes: bytes(tools),
     model_facing_bytes: bytes(tools.map((t) => ({ name: 'mcp__codegraph__' + t.name, description: t.description, inputSchema: t.inputSchema }))),
     instructions_bytes: bytes(init.result.instructions ?? ''),
     per_tool_bytes: Object.fromEntries(tools.map((t) => [t.name, bytes(t)])),
     explore_call_error: Boolean(ex.error || ex.result?.isError),
   }, null, 2));
   child.kill(); process.exit(0);
   ```
2. Leg A (always runs, no login, no real HOME): `W=$(mktemp -d)`; with `HOME="$W/home" CLAUDE_CONFIG_DIR="$W/home" CODEGRAPH_TELEMETRY=0 CODEGRAPH_NO_UPDATE_CHECK=1`, download the pinned tarball for this platform (§2.3 step 2 URL), check its SHA-256 against §0 before extracting (mismatch: stop, §7 item 2), extract under `$W`, `CG=` realpath of the extracted `bin/codegraph`; `mkdir "$W/repo" && git -C "$W/repo" init -q`; run the client twice from `$W/repo`: run 1 with `CODEGRAPH_MCP_TOOLS` unset, run 2 with `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`. `D = (tools_bytes + instructions_bytes)(run 2) - (tools_bytes + instructions_bytes)(run 1)`; record the model-facing delta, per-tool bytes and `D - per_tool_bytes.codegraph_node` as data only.
3. X-25 check, a hard stop: run 2's tool names are exactly the seven `codegraph_*` names (no `codegraph_explore`) and run 2's `explore_call_error` is `true`. If either fails, stop, write no `Selected MCP_TOOLS:` line and log a mid-level decision (§7); never fall back to `status` (it relies on the same hiding).
4. Bands on D: `D <= 6000` bytes → seven tools; `D > 8000` → `status`; in between → Leg B decides (merged method §3; the edges are 2,000 tokens at 3 and 4 bytes per token). Expected on today's W4 data: D ≈ +7,488 bytes, the undecided band (merged method §8).
5. Leg B (undecided band only; merged method §4-§5): needs `timeout 10 claude --version` to succeed; two codegraph-only config files (`$P/default.json`, `$P/seven.json`, identical except the key, `alwaysLoad: true`, `command` = `$CG`); `H0=$(jq -S '.mcpServers' ~/.claude.json | sha256sum)`; four runs from `$W/repo` in the order default, seven, default, seven, each `timeout 120 claude -p "reply ok" --output-format stream-json --verbose --strict-mcp-config --mcp-config "$P/<arm>.json" --no-session-persistence --model <one alias for all runs> > "$P/run<N>-<arm>.jsonl"`; tokens per run = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` from the final result event; `T = max(seven runs) - min(default runs)`; `H1` computed the same way after all runs must equal `H0` (else stop, no value). Leg B is valid only if (a) each seven run's init event lists the seven `mcp__codegraph__codegraph_*` names and no explore and each default run lists explore, (b) `T >= D / 5`, (c) the two runs of each arm agree within 50 tokens (one full re-run allowed), (d) the three token fields are numeric. Stream-json field names are UNVERIFIED; the guards fail closed.
6. Decision: pass or fail band → as banded (decided by A); undecided with valid Leg B → seven tools if `T <= 2000`, else `status` (decided by B); undecided with Leg B not run or invalid → `status` (decided by default), and the executor continues and logs §7 item 6 with the exact Leg B commands. If the value is `status`, apply the §2.4 failure branch (literal replacements) in this task's commit.
7. Write `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md` with the 16 one-fact lines of the merged method §7, in that order, ending with `Selected MCP_TOOLS: <value>`. T1 sets `install_codegraph.MCP_TOOLS` to that value. `rm -rf "$W" "$P"` afterwards.

Step 0 needs no repository code, so it runs **first, before T1** (T1's U2 test reads its evidence file); its client and evidence file are committed with T1.

Step 1, registration-shape probe (§2.4 premise), sandbox only:
```bash
MT=$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md); test -n "$MT"   # value chosen by step 0
E=$(jq -cn --arg t "$MT" '{"type":"stdio","command":"/opt/x/bin/codegraph","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1","CODEGRAPH_MCP_TOOLS":$t}}')
REAL=$(jq -S '.mcpServers' ~/.claude.json | sha256sum)
P=$(mktemp -d /tmp/p2-addjson.XXXXXXXX); echo '{"mcpServers":{}}' > "$P/.claude.json"
HOME="$P" CLAUDE_CONFIG_DIR="$P" claude mcp add-json codegraph "$E" --scope user
jq '.mcpServers.codegraph' "$P/.claude.json" | tee .dev/codegraph-migration/evidence/P2-add-json-shape.json; rm -rf "$P"
test "$(jq -S '.mcpServers' ~/.claude.json | sha256sum)" = "$REAL"                                   # real registrations untouched
jq -e --argjson e "$E" '. == $e' .dev/codegraph-migration/evidence/P2-add-json-shape.json           # stored exactly as given
```
If the last `jq -e` fails, the CLI changed or added a field: `diff <(jq -S . …shape.json) <(echo "$E" | jq -S .)` shows which; set the matcher to the stored shape and log the decision (§7).
Step 2, helpers: run `rg -n 'def (read_user_mcp_entry|_run_registration_command|_remove_exact_user_entry|_add_user_native_entry|_restore_user_native_entry|_native_registration_matches)|start_new_session' src/superclaude/cli/`; for each helper found, add a `name` parameter where missing and update its callers; for each missing one, re-create it from `git show 55d40308:src/superclaude/cli/install_mcp.py` with a `name` parameter and the bounded runner.
Acceptance:
```bash
uv run pytest tests/cli/test_install_codegraph.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/recommend -q -p no:cacheprovider
uv run pytest tests/cli/test_install_mcp_registry.py -q -p no:cacheprovider -k codegraph    # expect: the registry-contract and dispatch tests run (not "0 selected") and pass
jq -e 'type == "object"' .dev/codegraph-migration/evidence/P2-add-json-shape.json    # the probe stored an entry (a failed add-json leaves null)
test "$(wc -l < .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md)" -eq 16 && tail -1 .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md | rg -q '^Selected MCP_TOOLS: (node,search,callers,callees,impact,files,status|status)$'   # step 0 evidence complete
rg -qx 'Explore hidden: yes' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md && rg -qx 'Explore call blocked: yes' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md   # X-25 proof
test "$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print(MCP_TOOLS)')" = "$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md)"
node --check .dev/codegraph-migration/evidence/p2-mcp-tools.mjs
```
If `claude mcp add-json` itself exits non-zero in step 1 (for example it rejects `alwaysLoad`), stop: that changes the registration shape and is a mid-level decision (§7), not a matcher tweak.
Commit: `feat(mcp): register codegraph at user scope with exact-entry repair`

Group G1 report: issue comment (§6). (G0 is T0 and T0b.)

### G2: CLI wiring

**T3. `superclaude install` phase, exit term, `--list` block.**
Files: `src/superclaude/cli/main.py`, `tests/cli/test_update_command.py`.
Change: F3; §2.1, §2.8; the test additions listed in §4.1 for this file. The §2.8 `Ready for Serena retirement` line needs `codegraph_ready()`, which T3b creates, so T3 prints the other three `--list` lines and T3b adds the fourth (sc:reflect finding M-13).
Acceptance:
```bash
uv run pytest tests/cli/test_update_command.py tests/cli/test_update_script.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py -q -p no:cacheprovider
uv run superclaude install --help | grep -i codegraph          # expect: help text names codegraph
```
Commit: `feat(install): make codegraph a required user-level install phase`

**T3b. Retire Serena once codegraph is ready.**
Files: `src/superclaude/cli/install_mcp.py` (`codegraph_ready()`), `src/superclaude/cli/main.py`, `src/superclaude/cli/install_retired_mcp.py`, Phase 1's retire-step test file (find it with `rg -l install_retired_mcp tests`), `tests/cli/test_update_command.py`.
Change: F18; §2.12. Tests: codegraph failed keeps the current-pin Serena entry and install exits 1; ready (owned pinned entry; user-managed resolving entry) removes every launcher entry §2.12 matches (`serena`, and a non-`serena` key such as `foo` whose args contain `start-mcp-server`) and the kind-B `~/.local/bin/codebase-memory-mcp` registration; not ready (user-managed not resolving; wrong version) keeps them; `"env":{}` and `"headers":{}` entries removed; non-empty `env` or `headers` and no `start-mcp-server` kept; `serena-local` never removed; second run is a no-op; `install` and `install --list` call the same `codegraph_ready()` (doctor's use is tested in T4); Tier R and `/usr/local/bin/codebase-memory-mcp` removal stay unconditional.
Acceptance:
```bash
F=$(rg -l -g '*.py' install_retired_mcp tests)   # aborts under -e when no retire-step test file exists (sc:reflect finding M-18: an empty $(...) would run the whole suite)
test -n "$F"
uv run pytest $F tests/cli/test_update_command.py tests/cli/test_install_codegraph.py -q -p no:cacheprovider
uv run pytest $F -q -p no:cacheprovider -k "codegraph and serena"   # expect: tests selected and passing (exit 0, not 5)
test ! -e .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md || rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md   # T0b override present
```
Commit: `feat(install): retire Serena registrations once codegraph is ready (#323)`

**T4. Doctor check.**
Files: `src/superclaude/cli/doctor.py`, `tests/unit/test_cli_doctor.py`.
Change: F4; §2.7. Tests: dangling registered command fails; missing entry, version drift, prompt-hook leftover, `CODEGRAPH_START` block and unreadable `~/.claude.json` pass with a detail line; a bare-name command resolves through `PATH`; the check always adds the detail `Ready for Serena retirement: yes | no (<reason>)` from the same `codegraph_ready()` that `install` uses (test patches it once and asserts both callers see it).
Acceptance:
```bash
uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_update_command.py -q -p no:cacheprovider
```
Commit: `feat(doctor): report codegraph registration health`

Group G2 report: issue comment.

### G3: indexing

**T5. SessionStart hook.**
Files: `src/superclaude/hooks/scripts/codegraph-session-start.sh` (new, executable), `src/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/scripts/codegraph-session-start.sh` (copy), `src/superclaude/cli/install_hooks.py` (`_FRESHNESS_SCRIPTS`), `tests/cli/test_codegraph_session_start_hook.py` (new), `tests/cli/test_install_hooks.py`, `tests/unit/test_cli_install.py`.
Change: §3.2 behaviour and its listed tests.
Acceptance:
```bash
uv run pytest tests/cli/test_codegraph_session_start_hook.py tests/cli/test_install_hooks.py tests/unit/test_cli_install.py -q -p no:cacheprovider
sh -n src/superclaude/hooks/scripts/codegraph-session-start.sh
cmp src/superclaude/hooks/scripts/codegraph-session-start.sh plugins/superclaude/hooks/scripts/codegraph-session-start.sh
make sync-dev
make verify-sync
test -f .dev/codegraph-migration/evidence/P2-baseline-failures.txt   # a missing baseline must fail, not pass vacuously (M-19)
uv run pytest tests/cli/test_verify_sync_hooks.py -q -p no:cacheprovider -rfE --tb=no > /tmp/p2-t5-vsh.txt 2>&1 || true   # fails 3 tests at HEAD 55d40308 (review X-11); judged against the baseline below
grep -E '[0-9]+ passed' /tmp/p2-t5-vsh.txt >/dev/null   # the run completed
if grep -E 'INTERNALERROR|no tests ran' /tmp/p2-t5-vsh.txt; then exit 1; fi
{ grep -E '^(FAILED|ERROR) ' /tmp/p2-t5-vsh.txt || true; } | sed 's/ - .*//' | sort > /tmp/p2-t5-vsh-fail.txt
comm -13 .dev/codegraph-migration/evidence/P2-baseline-failures.txt /tmp/p2-t5-vsh-fail.txt > /tmp/p2-t5-new.txt
test ! -s /tmp/p2-t5-new.txt   # no failing test id outside the baseline
```
(`tests/cli/test_verify_sync_hooks.py` is judged only by the baseline diff above, never by its exit code: it failed 3 tests at `55d40308`, review X-11. The `|| true` and the brace group keep the block exiting 0 under `set -euo pipefail` when pytest fails or grep finds no failure.)
Commit: `feat(hooks): index each checkout with codegraph on its first session`

Group G3 report: issue comment.

### G4: guidance, docs, CI, live proof

**T6. Core guidance.**
Files: `src/superclaude/core/CLAUDE.md`.
Change: F6; §3.4 row and block.
Acceptance:
```bash
uv run pytest tests/core -q -p no:cacheprovider
test "$(rg -c '^\| codegraph ' src/superclaude/core/CLAUDE.md)" -eq 1                       # exactly one MCP table row (X-9)
test "$(rg -c -x '<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->' src/superclaude/core/CLAUDE.md)" -eq 1
test "$(rg -c -x '<!-- SUPERCLAUDE_CODEGRAPH_END -->' src/superclaude/core/CLAUDE.md)" -eq 1
sed -n '/^<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->$/,/^<!-- SUPERCLAUDE_CODEGRAPH_END -->$/p' src/superclaude/core/CLAUDE.md | rg -q 'codegraph_status'   # block sits between the markers
if rg -n 'codegraph_explore|CODEGRAPH_START' src/superclaude/core/CLAUDE.md; then exit 1; fi   # X-2: explore never named; no upstream marker (if-form: set -e ignores a failing `! cmd`)
```
Commit: `docs(core): add codegraph MCP row and usage rule`

**T7. User docs, README, CHANGELOG.**
Files: `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`, `README.md`, `CHANGELOG.md`.
Change: F8-F11, F19; include §2.6 removal commands, §2.10 failure table (short form), the registered tool list (`CODEGRAPH_MCP_TOOLS`, §2.4: which tools sessions see and why `codegraph_explore` is hidden), §3.3 costs and opt-out (with the exact scope of `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`), the opt-in `post-checkout` recipe, the `core.excludesFile` tip for `.codegraph/`, and §2.12 (Serena is removed once codegraph is ready, the `serena-local` re-register name, what is kept by policy, the escalated residuals).
Acceptance:
```bash
uv run pytest tests/docs -q -p no:cacheprovider
for f in README.md docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md CHANGELOG.md; do rg -q codegraph "$f" || { echo "missing: $f"; exit 1; }; done
rg -q 'SUPERCLAUDE_CODEGRAPH_AUTOINIT=0' docs/user-guide/mcp-installation.md
rg -q 'claude mcp remove codegraph --scope user' docs/user-guide/mcp-installation.md
rg -q 'serena-local' docs/user-guide/mcp-installation.md
rg -q 'serena-local' CHANGELOG.md
rg -q 'CODEGRAPH_MCP_TOOLS' docs/user-guide/mcp-installation.md
rg -qx '\.codegraph/' .gitignore
if rg 'Legacy Serena registration kept' CHANGELOG.md | rg -v 'codegraph'; then exit 1; fi   # Phase 1's entry does not say it is kept for good
```
Commit: `docs(mcp): document default codegraph install, indexing and removal`

**T8. CI doctor job.**
Files: `.github/workflows/test.yml`.
Change: F12. First check whether the step is still there: `rg -n 'name: Install Claude CLI' .github/workflows/test.yml`. If it is (Phase 1 kept it and only rewrote its comments, the fix review finding X-15 asks of Phase 1), only make sure its comment and the `permissions` comment name codegraph. If Phase 1 deleted it (Phase 1 spec row C12 as written on 2026-10-29), re-add it from `git show 55d40308:.github/workflows/test.yml` (lines 155-159, `npm install -g @anthropic-ai/claude-code@2.1.286`) before `Install native components`, with comments naming codegraph.
Acceptance:
```bash
uv run python -c 'import yaml,sys; d=yaml.safe_load(open(".github/workflows/test.yml")); s=[x.get("name") for x in d["jobs"]["doctor-check"]["steps"]]; print(s); sys.exit(0 if "Install Claude CLI" in s else 1)'
```
(pyyaml is a project dependency, so the project environment is used, M-10). The real proof is the `doctor-check` job on the PR.
Commit: `ci: keep Claude CLI for the required codegraph install phase`

**T9. Live sandbox proof (layer 2).**
Files: `.dev/codegraph-migration/evidence/p2-layer2.sh` (new; the §4.2 script) and `.dev/codegraph-migration/evidence/P2-layer2.md` (new; its outputs: versions, timings, the `jq` entry, query and callers lines, install logs).
Change: save the §4.2 script as `.dev/codegraph-migration/evidence/p2-layer2.sh` and run it (it includes the offline-reuse proof and the real-HOME hash check). If a real Claude Code session is available, also start one in a fresh clone and record in `P2-layer2.md` whether the hook's background `init` survives the hook and the session's end (`pgrep -f 'codegraph\.js init'`); otherwise record "process-group survival inside Claude Code: UNVERIFIED". If step 5's `claude mcp get` cannot run in the sandbox, apply the §4.2 Notes fallback and record that in `P2-layer2.md` (M-14).
Acceptance:
```bash
bash -n .dev/codegraph-migration/evidence/p2-layer2.sh
bash .dev/codegraph-migration/evidence/p2-layer2.sh          # exits 0 only if every assertion holds
test "$(tail -1 .dev/codegraph-migration/evidence/P2-layer2.md)" = LAYER2_OK   # M-19: tail alone always exits 0
```
Commit: `test(codegraph): record isolated-HOME install and index evidence`

Group G4 report: issue comment, including the T9 outputs.

### G5: final gate and PR

**T10. Full gate.**
Files: none new (fixes only, if the gate finds defects in this phase's files).
Acceptance:
```bash
make sync-dev
test -f .dev/codegraph-migration/evidence/P2-baseline-failures.txt
uv run pytest -p no:cacheprovider -q -rfE --tb=no tests > /tmp/p2-final-run.txt 2>&1 || true
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json   # restore before any gating line, so a failing gate still restores it (M-05)
grep -E '[0-9]+ passed' /tmp/p2-final-run.txt >/dev/null   # the run completed
if grep -E 'INTERNALERROR|Interrupted|no tests ran' /tmp/p2-final-run.txt; then exit 1; fi
{ grep -E '^(FAILED|ERROR) ' /tmp/p2-final-run.txt || true; } | sed 's/ - .*//' | sort > /tmp/p2-final-failures.txt   # brace group: a run with no failure must not fail the block under pipefail
comm -13 .dev/codegraph-migration/evidence/P2-baseline-failures.txt /tmp/p2-final-failures.txt > /tmp/p2-new-failures.txt
test ! -s /tmp/p2-new-failures.txt                                       # no failing test id outside the baseline (exit 1 otherwise)
make lint
make verify-sync
git status --short                                                        # expect: no unintended tracked change; nothing under .claude/ staged except settings.json
```
Commit (only if fixes were needed): `fix(codegraph): <what the gate found>`

**T11. PR (shared with Phase 1, one merge unit).**
Run `/sc:pr-submit --monitor 3 --head ironbelly/feat-codememory-codegraph-init --title "feat: replace codebase-memory and Serena with codegraph (#323)" --body "<Phase 1 + Phase 2 summary; Closes nothing until Coder steps 1-2 merge; links to both specs>"`, after the pre-PR checks in the project `CLAUDE.md` (origin is `IronbellyOrg/IronClaude`, rebase onto `origin/master` if it moved). If the Phase 1 executor already opened the PR, push to it instead of opening another.
Acceptance:
```bash
gh pr view ironbelly/feat-codememory-codegraph-init --repo IronbellyOrg/IronClaude --json url -q .url    # expect: https://github.com/IronbellyOrg/IronClaude/pull/<n>
gh pr checks ironbelly/feat-codememory-codegraph-init --repo IronbellyOrg/IronClaude                   # expect: all pass, including doctor-check
# merge gate (checked by the human before merging, §7 item 3): Coder steps 1-2 of §8 are on Coder main
gh api repos/IronbellyOrg/Coder/contents/templates/VSCode-AIDev02/Dockerfile.coder -H 'Accept: application/vnd.github.raw' | grep -E 'ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828' >/dev/null && echo "Coder step 1: bake with the pinned linux-x64 hash present"
gh api repos/IronbellyOrg/Coder/contents/.github/contract-tests/test-57-catalogue-configure.sh -H 'Accept: application/vnd.github.raw' | grep -E 'mcpServers.*codegraph|codegraph.*mcpServers' >/dev/null && echo "Coder step 2: contract test asserts the codegraph registration"
gh api repos/IronbellyOrg/Coder/contents/templates/VSCode-AIDev02/catalogue/mcp-bundle-core/install.sh -H 'Accept: application/vnd.github.raw' > /tmp/p2-bundle.sh && ! grep -E '^SERENA_PIN=|uv tool install .*serena-agent' /tmp/p2-bundle.sh >/dev/null && echo "Coder step 2: bundle no longer installs or registers Serena"
# all three lines must print; otherwise do not merge. Also confirm on issue #323 that the two Coder PRs are merged.
```
Commit point: none (PR only). Do not merge (§7 item 3).

Group G5 report: issue comment with the PR URL and the Coder ordering status (§8).

### G6: post-merge live verification (review finding X-5)

**T12. Prove "completely absent" on the real workspace.**
Trigger: the human has merged the PR (§7 item 3) and run `./update.sh` on this workspace (§7 item 4), then restarted every Claude session. The executor runs the checks below in a new session (read-only: no `claude mcp add/remove`, no `superclaude install` other than the read-only `--list`) and does not mark T12 done until the block exits 0. Outputs go to `/tmp/p2-t16-*` and the G6 comment, never into the repository.
Files: none in the repository (post-merge; the outputs go only into the issue-#323 comment, §6).
Acceptance:
```bash
rc=0; jq -e '(.mcpServers // {}) | (has("serena") or has("codebase-memory-mcp") or (to_entries | map(select(.key != "serena-local" and ((.value.args // []) | tostring | test("serena-agent|start-mcp-server")))) | length > 0)) | not' ~/.claude.json || rc=$?
echo "$rc" > /tmp/p2-t16-us.rc; test "$rc" -le 1   # §2.12 user scope: recorded, gated at the end (rc 2+ = unreadable file, fails now)
rc=0; jq -e '[(.projects // {}) | .[] | (.mcpServers // {}) | has("serena") or has("codebase-memory-mcp")] | any | not' ~/.claude.json || rc=$?
echo "$rc" > /tmp/p2-t16-ls.rc; test "$rc" -le 1   # §2.12 local scope: report-only (a hit means the user runs the printed command)
jq -r '(.mcpServers // {}) | to_entries[] | select(.key == "serena" or .key == "codebase-memory-mcp" or (.key != "serena-local" and ((.value.args // []) | tostring | test("serena-agent|start-mcp-server")))) | "claude mcp remove \(.key) --scope user"' ~/.claude.json > /tmp/p2-t16-user-cmds.txt
jq -r '(.projects // {}) | to_entries[] | .key as $p | (.value.mcpServers // {}) | keys[] | select(. == "serena" or . == "codebase-memory-mcp") | "cd \($p) && claude mcp remove \(.) --scope local"' ~/.claude.json > /tmp/p2-t16-local-cmds.txt
MT=$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print(MCP_TOOLS)')   # run from the worktree root (merged code)
jq -e --arg t "$MT" '.mcpServers.codegraph | .args == ["serve","--mcp"] and .env.CODEGRAPH_MCP_TOOLS == $t and .env.CODEGRAPH_TELEMETRY == "0"' ~/.claude.json   # X-1 on the live entry
test "$("$(jq -r '.mcpServers.codegraph.command' ~/.claude.json)" --version)" = 1.6.2
claude mcp get codegraph > /tmp/p2-t12-get.txt 2>&1 || true
grep -i 'connected' /tmp/p2-t12-get.txt >/dev/null   # UNVERIFIED output wording, as in §4.2 step 5
if grep -iE 'disconnected|not connected|failed' /tmp/p2-t12-get.txt; then exit 1; fi   # M-11: 'connected' also matches these
superclaude install --list > /tmp/p2-t12-list.txt   # read-only (§2.8)
grep -F 'Ready for Serena retirement: yes' /tmp/p2-t12-list.txt >/dev/null
superclaude doctor
test "$(cat /tmp/p2-t16-us.rc)" -eq 0   # user scope gates T12; a kept entry keeps T12 open until the user runs /tmp/p2-t16-user-cmds.txt (§7 item 7)
```
Then, in the same new session, confirm from the session's own tool list that `mcp__codegraph__codegraph_callers` (or, in the `status`-only branch, `mcp__codegraph__codegraph_status`) is listed and `mcp__codegraph__codegraph_explore` is not, and write that observation into the comment. On Coder workspaces the equivalent check is the handoff prompt's "Done means" (owned by the Coder agent), not this task.
Commit point: none (post-merge, nothing in the repository changes); the G6 issue comment is the record.

Group G6 report: final issue comment with every T12 command and its output, the PR URL and the Coder ordering status (§8).

## 6. Progress reporting on issue #323

After each task-group commit in §5 (G0 to G5), and after G6's checks, post one comment. Never post anywhere else (no PR comments for progress, no Slack). Use a body file so the text is not mangled by the shell:

```bash
cat > /tmp/p2-progress.md <<'EOF'
**Phase 2 (install codegraph) progress: <group id and name>**

- Commit: <short sha> `<conventional commit subject>` on `ironbelly/feat-codememory-codegraph-init`
- Done: <one line per task in the group>
- Tests: `<exact acceptance command>` -> <N passed, M skipped / failure summary>
- Decisions taken: <none | file path under .dev/codegraph-migration/decisions/P2X-*>
- Next: <next group>
EOF
gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file /tmp/p2-progress.md
rm /tmp/p2-progress.md
```

`--body-file` is the file form of the brief's `--body`; both post the same comment. A failed test run is reported as failed with its summary, never as done. The G5 and G6 comments also link the PR URL, which must start with `https://github.com/IronbellyOrg/IronClaude/pull/`.

## 7. Autonomy rules for the executor

The executor works without stopping to ask, under these rules.

| Decision size | Example | Method |
|---|---|---|
| Simple: one obvious answer, or forced by a pinned test or a verified constraint | helper name, message wording, test file layout, which fixture to extend | decide yourself |
| Mid: two or more viable options with real trade-offs, local to one task | where the receipt lives; whether `--list` prints the receipt paths; how to bound the tar extraction | write each option to `.dev/codegraph-migration/decisions/P2X-<slug>/option-<x>.md` (under 40 lines each) and spawn an agent (Agent tool) that runs `/sc:adversarial --compare <files> --depth quick` |
| Complex: changes the installer contract in §2, the indexing design in §3, the release order in §8, or crosses Phase 1/3 ownership | making the phase optional; adding a git hook; changing the pin source of truth | same, without `--depth quick` (`/sc:adversarial --compare <files>`, default standard depth) |

Follow the adversarial recommendation. Record every autonomous decision, in the commit that applies it, as a row in `.dev/codegraph-migration/decisions/P2X-log.md` (create on first use) with columns: decision, options considered, method (self / adversarial quick / adversarial full), rationale, decision folder. Mention the folder in the next issue comment.

Hard rules (no decision can override them): never run `claude mcp add/remove` or `superclaude install` against the real HOME (only in sandbox HOMEs: T2 step 1 and §4.2, both of which assert the real `.mcpServers` is unchanged; the one exception is the read-only `superclaude install --list`, §2.8, used by T3 and T12); never commit anything under `.claude/` except `.claude/settings.json`; always `git add .dev/tasks` if that folder exists; feature branch only; PRs only on `IronbellyOrg/IronClaude` via `/sc:pr-submit --monitor 3` (fallback `gh pr create --repo IronbellyOrg/IronClaude`); never push to `upstream`; restore `.dev/releases/current/cliEval/evidence/T02.15/perf.json` with `git checkout --` after a full test run and before committing.

Human intervention is needed only for:
1. A GitHub auth failure for `gh` (the executor cannot log in for the user).
2. A release with a different `SHA256SUMS` than §0 for `v1.6.2` (possible tampering): stop, report on issue #323 and ask before changing a hash.
3. Merging the PR to `master` (ordering in §8 depends on the Coder bake; merge is the user's call; T11's merge-gate command shows whether the bake is on Coder `main`).
4. Running `./update.sh` on the real workspace after merge (it mutates the live environment) and restarting the Claude sessions; the executor then runs T12's read-only checks.
5. After T0: giving `.dev/codegraph-migration/handoff/coder-handoff-prompt.md` to an agent working in the IronbellyOrg/Coder repo (the executor has no authority over that repo).
6. Non-blocking (the executor does not wait): when T2 step 0 ends in the undecided band with Leg B not run or invalid, the executor ships `status`, continues, and posts the exact Leg B commands in that group's issue-#323 comment and as a row in `decisions/P2X-log.md`. If a person later gets a valid Leg B with `T <= 2000`, one follow-up commit changes `install_codegraph.MCP_TOOLS` and the spec literals back to the seven tools. The 2K threshold and the 6,000/8,000-byte edges are proposals not yet confirmed by the user (`decisions/F2-schema-cost-method/recommendation.md` "Items for the user"); the same comment states that.
7. Non-blocking (the executor does not wait): when T12's user-scope check finds an entry the retire step kept (non-empty `env`/`headers`, or a launcher without `start-mcp-server`), the executor posts `/tmp/p2-t16-user-cmds.txt` in the G6 comment, the user runs those commands, and T12 is re-run; T12 stays open until then (sc:reflect finding M-02).

## 8. Release and ordering

Facts (W5 §5, verified there against Coder `e25f787c`): Coder pins one IronClaude `master` SHA (`templates/VSCode-AIDev02/Dockerfile.coder:375`, `ARG IRONCLAUDE_GIT_SHA=55d40308…`); a daily monitor opens a bump PR for every new `master` HEAD and edits only that line (`.github/workflows/ironclaude-upstream-monitor.yml:10-12`, `:131`); its proof runs only `superclaude --version` (`:246-256`); Coder runs `timeout 60 superclaude install … </dev/null` and fails the slug on a non-zero exit (`catalogue/ironclaude/install.sh:120-123`); Coder contract CI runs that install with `--network=none` and asserts today's Codebase Memory registration (`test-57-catalogue-configure.sh:228`, `:243-244`; `coder-ci-aidev02-contract.yml:1221`).

Consequences for this phase:
- **Phase 1 and Phase 2 land on IronClaude `master` in one merge** (one PR from `ironbelly/feat-codememory-codegraph-init`). A `master` HEAD that has Phase 1 without Phase 2 would install neither server and still pass the monitor's `--version` proof (W5 §5.2 row E).
- **The phase must succeed offline when the image has the pinned binary**: `discover()` checks PATH first and makes no network call when it finds `1.6.2` (§2.2). The registration step needs only the local `claude` CLI.
- **A required phase means Coder must bake first.** With the pin bumped and no baked `codegraph`, the offline contract test fails (`superclaude install` exits 1 at the download stage) and real boots spend the 60 s budget downloading 63 MB.

Order (the Coder side is in `.dev/codegraph-migration/handoff/coder-handoff-prompt.md`):

| Step | Repo | What | Gate |
|---|---|---|---|
| 1 | Coder | Bake codegraph `v1.6.2` (verified SHA-256, `/usr/local/bin/codegraph`, telemetry and update check off in image env). Additive only. | Coder CI green with the old pin |
| 2 | Coder | Make contract tests pin-agnostic: accept either the old state (Codebase Memory registered) or the new one (codegraph registered, Codebase Memory and Serena absent). In the same step (§2.12): the bundle stops registering, installing, warming and health-checking Serena (with its tests: test-57 incl. `:602-603`, `spec2-health.sh:79`, manifest health, the test-startup-boot handshake proof); `uv tool uninstall serena-agent`, markers, alias; a guarded one-time migration in `T/scripts/startup.sh` (not in the bundle `install.sh`) that, only when a `codegraph` user entry exists whose command prints `1.6.2`, removes `serena` if it equals the bundle argv and the exact `/usr/local/bin/codebase-memory-mcp` entry. Safe with the old pin: the old IronClaude never touches Serena (W5 §5.2 row C). | Coder CI green with the old pin |
| 3 | IronClaude | Merge the Phase 1 + Phase 2 PR (human, §7 item 3), only after steps 1-2 are merged on Coder `main`. | IronClaude CI green |
| 4 | Coder | Pin bump to the new `master` SHA (monitor PR or hand-made). | test-57 and test-startup-boot pass on the new SHA |
| 5 | Coder | Remove the baked `/usr/local/bin/codebase-memory-mcp` from the image (must follow step 4, W5 §5.2 row B), add index automation and the CLAUDE.md codegraph block (§3.4 Coder gap). | Coder CI green; on a workspace booted from it, the §2.12 acceptance checks pass |
| 6 | Workspaces | Each existing workspace converges at its next restart on the new image (`ironclaude/install.sh:91-95` reruns `superclaude install --force` when the SHA changes). Dev checkouts converge on `./update.sh`. | `claude mcp get codegraph` shows the expected entry |

If the Coder bake is not merged when the IronClaude PR is otherwise ready, the PR waits (it does not switch the phase to optional): the decision in §2.1 is that "installed by default" must be provable by exit code.

## 9. Shared files with Phase 1 and Phase 3

| File | Phase 1 edit (removal) | Phase 2 edit (this spec) | Phase 3 edit (adoption) | Rule |
|---|---|---|---|---|
| `src/superclaude/cli/install_mcp.py` | deletes Codebase Memory and Serena registry entries, native functions, uninstall branch; keeps or deletes registration helpers | adds `codegraph` entry, dispatch, phase function, name-parameterised helpers | none expected | Phase 1 first; T2 adapts to what Phase 1 left (§5) |
| `src/superclaude/cli/main.py` | deletes Codebase Memory phase, `--list` block, `mcp --uninstall/--yes` | adds codegraph phase, exit term, `--list` block | none | Phase 1 first |
| `tests/cli/test_update_command.py` | rewrites autouse fixture, deletes native tests | extends fixture and adds codegraph phase tests | none | Phase 1 first |
| `tests/cli/test_install_mcp_registry.py` | deletes Serena/Codebase Memory tests, adds removed-server guard | adds codegraph entry tests | none | Phase 1 first |
| `src/superclaude/core/CLAUDE.md` | deletes Serena row (`:21`) and Serena refresh-tool row content (`:112`) | adds the one codegraph MCP row and the marker-delimited guidance block (§3.4) | edits Phase 2's codegraph row in place (never a second row), owns later wording inside the markers, and maps the "Symbolic queries" refresh row (`:112`) to codegraph | Phase 1, then 2, then 3; exactly one `\| codegraph` row (review X-9) |
| `src/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/hooks.json` | drops `mcp__serena__*` matcher alternatives (`:47`, `:37`) | adds codegraph SessionStart entry if §3 ships one | may add matchers for codegraph tools | Phase 1 first |
| `src/superclaude/cli/install_hooks.py` | none expected | `_FRESHNESS_SCRIPTS` entry if §3 ships a hook | none | n/a |
| `tests/unit/test_cli_install.py` | removes Serena MCP files from listings | adds hook script to listing if §3 ships a hook | none | Phase 1 first |
| `tests/cli/test_install_hooks.py` | deletes Serena matcher asserts | adds codegraph hook registration test if §3 ships one | none | Phase 1 first |
| `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`, `README.md`, `CHANGELOG.md` | deletes Codebase Memory and Serena sections | adds codegraph sections | may document new commands | Phase 1 first |
| `.github/workflows/test.yml` | deletes the Claude CLI step (Phase 1 row C12); review X-15 asks Phase 1 to keep it and rewrite only its comments | rewrites comments, and re-adds the step only if Phase 1 deleted it | none | T8 checks which case holds |
| `src/superclaude/cli/install_retired_mcp.py` (new in Phase 1) and its tests | the non-fatal retire step for old registrations | the `codegraph_ready()`-gated Serena and kind-B codebase-memory removal (§2.12, T3b); codegraph registration itself stays out of it (Phase 1 spec §7) | none | Phase 1 first. **Phase 1 spec must be amended** to match §2.12: its §2.3 row, §3.2 Tier K, §3.4 hint, §3.6 row, the sandbox expectation "Legacy Serena registration kept", and D2 (the debate's RP-7; reported to the coordinator) |
| `tests/cli/test_install_mcp_cli.py` (new in Phase 1) | generic `superclaude mcp` tests | optional `--servers codegraph --dry-run` case (U23 may live here) | none | Phase 1 first |
| `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md` (written by Phase 1 T15) | facts for the Coder handoff | read by the Coder agent with `coder-handoff-context.md` | none | Phase 1 writes; Phase 2 handoff points to it |

Phase 3 files (skills, commands, agents, refs that adopt codegraph tools) are not touched by Phase 2.

## Decisions

| # | Decision | Options considered | Method | Rationale |
|---|---|---|---|---|
| D1 | Phase contract: required phase (exit 1 on failure), doctor fails only on a dangling registered command, receipt-gated documented removal with no CLI flag | A required + strict doctor + `mcp --uninstall`; B default non-fatal + advisory doctor + fixed-path `rm`; C required + narrow doctor + receipt | adversarial full (`decisions/P2-installer-contract/`, merged `adversarial/P2-installer-contract-merged.md`; C 0.896, B 0.859, A 0.839; 18/18) | Exit code is the gate both `./update.sh` and Coder already enforce, so "installed by default" is provable; doctor would only duplicate that check; a receipt makes removal exact without re-adding the uninstall surface Phase 1 deletes. Incorporated from B: recovery command in failure output, missing entry reported not failed; from A: prompt-hook leftover reporting, receipt-proven ownership of links and dirs. |
| D2 | Indexing: IronClaude ships a fail-open SessionStart hook that indexes each checkout once in the background, plus a core CLAUDE.md fallback rule; no global git config | A guidance only; B SessionStart hook; C global git template hooks | adversarial quick (`decisions/P2-indexing-sync/`, merged `adversarial/P2-indexing-sync-merged.md`; B 0.886, A 0.756, C 0.736; 18/18) | Works on every machine IronClaude installs on, per worktree by construction, no global git mutation; freshness comes from codegraph's own watcher and connect-time catch-up. |
| D3 | (superseded by D21) Rebuild with `codegraph index <top>` when a database exists without the completion marker; no IronClaude lock | trust `init --yes`; add a lock | self, from sandbox probes 1-2 (`decisions/P2-indexing-sync/probe-results.md`) | `init --yes` is a no-op on a truncated index (probe 1); concurrent inits fail cleanly (probe 2). `codegraph index --help`: plain `index` rebuilds from scratch, its `--force` only permits home/root. |
| D22 | IronClaude removes every user-scope Serena launcher entry and the kind-B codebase-memory registration once `codegraph_ready()` is true in the same run; Coder stops re-adding Serena in step 2 and runs a guarded backstop; the baked binary goes with the step-5 image | A keep Phase 1 Tier K, Coder only; B remove once codegraph is ready; C remove only off Coder | adversarial full (`decisions/P2-serena-entry-removal/adversarial/P2-serena-entry-removal-merged.md`; B 0.898, C 0.853, A 0.835; 18/18; contract partial) | Only B meets "absent after `./update.sh`" wherever IronClaude can act; every known writer of the current-pin argv is IronClaude or a mirror of its pin; gating on codegraph readiness never removes the current-pin Serena entry while codegraph is missing. Taken from A: the `jq`/`command -v` checks and the exact-argv Coder migration; from C: the two-branch test matrix and the guarded migration. Unmet and escalated: the root-owned baked binary (until the step-5 image) and a kind-B upstream binary with companions. |
| D24 | Fourth- and fifth-review fixes: Serena rule matches by shape under any name except `serena-local` (stdio or absent type, `env`/`headers` absent or `{}`); Coder's backstop migration lives in `T/scripts/startup.sh`, so the merge gate checks the bundle for `SERENA_PIN`/`uv tool install … serena-agent` instead of any `serena-agent==` text; doctor and `--list` print `Ready for Serena retirement` from the one `codegraph_ready()`; layer 2 runs after T5; T0b checks 7 amended Phase 1 lines plus the `absent or {}` wording on the Tier R and Tier K lines; the §2.12 acceptance is split into a user-scope and a local-scope `jq` check (local-scope hits mean "run the printed command"); the Serena decision record carries an "Amended by D22-D24" note | leave as written | self (forced by `decisions/P2-review/fourth-review-report.md` §2 and `fifth-review-report.md`) | Wording and check alignment only; no design change. |
| D23 | Third-review fixes: Serena rule accepts `env`/`headers` absent or `{}`; hook keys on `.codegraph/codegraph.db`, not the folder; `.codegraph/` added to IronClaude's `.gitignore`; T0b owns the Phase 1 spec and facts-file amendments; merge gate checks the bundle no longer pins `serena-agent`; `codegraph_ready()` is one read-only predicate | leave as written | self (each forced by evidence in `decisions/P2-review/third-review-report.md` §2: live entry has `"env":{}`; a committed `.codegraph/.gitignore` blocks indexing; Phase 1 text contradicts §2.12) | Each is the smallest change that makes the stated requirement true. |
| D21 | Hook only starts `codegraph init --yes` when `<top>/.codegraph/codegraph.db` is absent (amended by D23; was `<top>/.codegraph`); no marker, PID file, lock, `status`, `index` or `sync`; the MCP daemon heals interrupted inits; guidance forbids `status`/`index`/`sync` while a run may be active and uses `pgrep -f 'codegraph\.js (init\|index)'` | D15's PID-file and `status` design; D3's rebuild rule; the debate's completion marker | self, forced by probe rows 6-9 (re-review findings 1-5) | `status` during an `init` empties the index (row 6), `index` during an `init` empties it (row 7), `status` cannot tell "killed" from "building" (row 4); concurrent inits are harmless (rows 2-3); the daemon completes a killed or interrupted init on the next connection (rows 8-9). Removing every branch that touches an existing index removes the races; smallest correct code. |
| D15 | (superseded by D21) Hook decides in a detached background job: init when no database; mark when `codegraph status` shows no "never finished"; `index` only for IronClaude's own dead run (PID file outside `.codegraph/`); otherwise leave a foreign truncated index alone | D3's unconditional rebuild; a `mkdir` lock; always rebuild | self, forced by probes 4-6 (review finding 1) | Probe 6: `index` started during an `init` empties the index; probe 5: `index` with a live daemon is safe; probe 4: "never finished" is the only reliable truncation signal. Running `status` in the background keeps the 5 s hook budget. |
| D16 | All `claude` and `codegraph` calls in the phase use a bounded argv runner (no shell, own process group), shared with Phase 1's retire step | keep `_run_command` | self | `_run_command` uses `$SHELL -c` with `shell=True` (`install_mcp.py:134-141`), so its timeout does not kill the child; Phase 1 §3.3 already adds such a runner. |
| D17 | Installer writes `~/.codegraph/.superclaude-bin` (registered realpath) and warns when the winner is not first on PATH; hook and guidance use it | require PATH; hook reads `~/.claude.json` | self (review finding 7) | Keeps hook and MCP server on the same binary without parsing JSON in `sh`; works when `~/.local/bin` is not on PATH (macOS). |
| D18 | Verify the `add-json` stored shape in a sandbox as T2 step 1 and match only stored fields | trust `--help` | self (review finding 3) | The whole-entry compare makes the required phase fail if the CLI normalises a field; one sandbox call removes the risk. |
| D19 | Coder carries the core CLAUDE.md codegraph rule in its seed and existing workspaces; IronClaude does not work around the restore | IronClaude writes elsewhere | self (review finding 2) | Coder's slug restores `~/.claude/CLAUDE.md` by design (W5 §1.7); the owner of that file is Coder. |
| D20 | New task T0 commits and pushes the planning files and triggers the Coder handoff; T11 merge gate checks the Coder bake on `main` | leave to chance | self (review finding 6) | `.dev/codegraph-migration/` is untracked, so the handoff URL would 404; the merge order (§8) needs a mechanical check. |
| D4 | Pin stays `v1.6.2` with a four-asset SHA-256 table (linux and darwin, x64 and arm64); Windows unsupported | pin latest at execution time; add Windows | self | v1.6.2 is the latest release and was validated hands-on (W4 §5); IronClaude's installers are POSIX (the hook is `sh`); Windows assets are zips and untested. T1 re-checks the hashes. |
| D5 | No `mcp__codegraph__*` permission rule | add via settings defaults; none | self | No other server gets one; `install_user_setup.py` has no permissions handling (a list merge would be new code); all codegraph tools are read-only. |
| D6 | No `src/superclaude/mcp/MCP_Codegraph.md` or `configs/codegraph.json` | add them like other servers; skip | self | They install nowhere (`~/.claude/mcp/` does not exist, W2 §4.1) and would change a pinned listing; docs pages carry the content. |
| D7 | `update.sh` and `superclaude update` unchanged | add a step | self | `update.sh:8` already runs `install --force`; `update` is documented never to touch MCP state; `update.sh` is pinned to four commands (`tests/cli/test_update_script.py:13-18`). |
| D8 | Registration helpers: adapt mechanically to what Phase 1 left (add a `name` parameter, or re-create from `55d40308`) | new separate module; duplicate helpers | self | Phase 1 spec §7 keeps read, run and remove helpers and deletes add, restore and match; the mechanical rule in T2 still works if Phase 1's final code differs, and keeps one copy. |
| D9 | Keep (or restore) the `Install Claude CLI` step in `.github/workflows/test.yml` `doctor-check` | let Phase 1 delete it | self | The required phase needs `claude --version` (§2.4); without it the CI job turns red. |
| D10 | Stdlib download and extraction (`urllib`, `hashlib`, `tarfile` with explicit member checks), no subprocess `curl` | `curl`/`tar` subprocesses; tarfile `filter=` | self | No new dependency or external tool; Python >= 3.10 is supported so `filter=` cannot be relied on; the v1.6.2 tarball has only files and dirs under one top dir. |
| D11 | If the Coder bake is not merged when the PR is ready, the PR waits; the phase is not made optional to unblock it | downgrade to non-fatal | self (follows D1 and W5 §5.2) | Making it optional would reopen D1 without new evidence; the wait costs nothing on IronClaude. |
| D12 | Phase 1 and Phase 2 land as one PR / one `master` merge | separate merges | self (forced by W5 §5.2 row E) | The monitor bumps Coder to every `master` HEAD; an intermediate HEAD would install neither server. |
| D13 | `/sc:design` not run | run it | self | The interface is three functions and a hook script; §2.11 already states it. |
| D14 | Handoff tells the Coder agent to record decisions under Coder `.dev/decisions/` and to fall back to a written comparison if `/sc:adversarial` is not installed there | require the IronClaude command | self | Coder may not have IronClaude's commands installed in its agent environment (UNVERIFIED); the fallback keeps the decision rule usable. |
| D25 | Phase 2 owns `CODEGRAPH_MCP_TOOLS` and its schema-cost check (moved from Phase 3 T0 E-5); the value lives in one constant `install_codegraph.MCP_TOOLS`, seven tools on pass, `status` on fail | leave it to Phase 3 (review X-1 shows the cycle); hard-code the JSON | self (forced by review X-1 and the coordinator brief, `orchestration/README.md:40`) | Phase 3 starts only after Phase 2 merges and no Phase 3 task can change the installer, so only Phase 2 can ship the key; one constant keeps installer, tests, layer 2, T12 and Coder reading the same value. |
| D26 | Guidance block between `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` / `<!-- SUPERCLAUDE_CODEGRAPH_END -->` markers; Coder re-syncs the marked lines on every pin bump | Coder appends once guarded by the first line (old text) | self (forced by review X-2 and X-10) | "Append once" freezes the first wording on Coder forever; marker replacement is the smallest mechanism that carries Phase 3 changes. Marker names avoid upstream's `CODEGRAPH_START`, which the doctor reports as a leftover. |
| D27 | Post-merge live check is task T12 (group G6): human runs `./update.sh` and restarts sessions, executor runs read-only checks, results only in the issue-#323 comment; no commit | add an evidence file on a follow-up branch | self (review X-5) | Post-merge, nothing in the repository should change; the issue comment is the durable record the brief asks for, and a follow-up branch would need another PR for no code. |
| D28 | T5 and T10 judge known-failing tests only by a baseline diff written to survive `set -euo pipefail` (`\|\| true` on the pytest run, brace group around `grep`, `test ! -s` / `test -z` on the `comm` output) | the review's one-line pipe (X-11 fix as written) | self | The review's pipeline exits non-zero under `pipefail` whenever pytest fails or grep finds nothing, and the old T10 `comm` line exited 0 even when it printed new failures, so neither could gate. |
| D29 | T8 checks whether Phase 1 kept the `Install Claude CLI` step and only re-adds it when it is gone | re-add unconditionally (old text) | self (review X-15) | Review X-15 asks Phase 1 to keep the step; the conditional works whichever way the Phase 1 finalizer resolves it. |
| D30 | Schema-cost method for T2 step 0: byte measurement over stdio as the gate with three bands (≤ 6,000 B pass, > 8,000 B fail), a real headless-session measurement only inside the band, never blocking (`status` when the session leg cannot run); a failed X-25 check stops with no value | A byte proxy alone; B session tokens alone; C byte gate plus recorded session check | adversarial quick (`decisions/F2-schema-cost-method/`, merged `adversarial/F2-schema-cost-method-merged.md`; A 0.870, C 0.829, B 0.701; 15/15) | The measured delta (+7,488 B on W4's saved responses; +7,597 B re-measured by F2 with the step-0 client on 2026-10-29) sits on the 2K-token line depending only on the unknown bytes-per-token rate, so a single cut-off would let an unmeasured constant decide; the unattended executor must never block. |

## Review resolution

Source: `.dev/codegraph-migration/review/review.md` (task R, 25 findings). Applied by finalizer F2 on 2026-10-29 after checking each finding against the cited source. Only Phase 2 hunks and the Coder handoff files (`handoff/coder-handoff-prompt.md`, `handoff/coder-handoff-context.md`) were edited; no other phase's spec was touched.

| Finding | Result | Reason (one line) |
|---|---|---|
| X-1 | applied | Verified: the old §2.4 JSON had no `CODEGRAPH_MCP_TOOLS` and default listing is explore only (`research/codegraph-evaluation.md:94`); added the key via one `MCP_TOOLS` constant, the schema-cost check as T2 step 0 (D25, D30), U2/U12/U14, layer 2 steps 1 and 5b, T12, and the handoff JSON, `jq -e` checks and "Done means". |
| X-2 | applied | Verified: §3.4 began "Start code-structure questions with `codegraph_explore`"; block rewritten to the seven tools with a `status`-only variant, wrapped in `SUPERCLAUDE_CODEGRAPH_BEGIN/END` markers, T6 asserts no `codegraph_explore`; handoff now says replace-between-markers on every pin bump instead of append once (D26). |
| X-5 | applied | Verified: no task ran the §2.12 checks on the real workspace; added T12 / group G6 (human runs `./update.sh`, executor runs read-only checks, outputs on #323, D27) and the `install --list` exception in §7 hard rules. |
| X-9 | applied (Phase 2 hunk) | §3.4 and §9 now state exactly one `\| codegraph` row that Phase 3 edits in place; T6 asserts the count is 1. Phase 3's own row change belongs to F3. |
| X-10 | applied (handoff hunk) | The marker re-sync on every pin bump (X-2 fix) is the channel that carries Phase 3 changes to Coder; the issue-#323 addendum task is Phase 3's (F3). |
| X-11 | applied, with a corrected command | Verified: `tests/cli/test_verify_sync_hooks.py` gives `3 failed, 4 passed` (re-run by F2 on 2026-10-29); removed it from the T5 pytest line and added a baseline diff. The review's one-line pipe would itself fail under `set -euo pipefail` (pytest and grep exit 1), so T5 uses `\|\| true`, a brace group and `test -z` (D28). |
| X-14 | applied (Phase 2 hunk) | §3.3 and T7 now state that `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` disables only the hook and that every switch uses the `SUPERCLAUDE_CODEGRAPH_` prefix; renaming Phase 3's `IRONCLAUDE_CODEGRAPH=off` is F3's. |
| X-15 | applied (Phase 2 hunk) | Verified: Phase 1 row C12 still deletes the step (`specs/phase-1-removal-spec.md:41`); T8 now checks whether the step exists and re-adds it only when Phase 1 deleted it (D29). Phase 1's change is F1's. |
| X-21 | applied | Verified against `research/codegraph-evaluation.md:77` (`alwaysLoad` stops deferral, it does not cause connection); §3.1 reworded. |
| X-25 | applied | Marked UNVERIFIED in §2.4 and the handoff context; T2 step 0 (hard stop) and layer 2 step 5b now prove that an explicit list hides and blocks explore. F2 observed it on 2026-10-29 with the step-0 client against the W4 sandbox binary: run 2 listed exactly the seven tools and the explore call returned an error. |
| F2-1 (found by F2) | applied | T10's old `comm -13` line exited 0 even when it printed new failures, and its `grep \| sed \| sort` line failed under `pipefail` when nothing failed; both fixed (D28). |
| F2-3 (found by F2) | applied | Tests U24 (pointer file) and U25 (bounded runner kills a SIGTERM-ignoring child) were listed in §4.1 but assigned to no task; now T1 owns U24 and T2 owns U25. |
| F2-2 (found by F2) | applied | The §5 baseline command piped a failing pytest run into grep under `pipefail`, so on a suite with known failures it would abort; both stages are now brace-guarded. |
| X-3, X-6, X-7, X-8, X-13, X-18, X-19, X-20, X-22, X-23 | not applied here | Phase 3 only (owner F3); no Phase 2 hunk. X-3 confirms Phase 2's hook model, which stays as written. |
| X-4, X-12, X-16, X-17, X-24 | not applied here | Phase 1 only (owner F1). Phase 2 T0b stays as the check that F1's amendment landed. |

Second pass (2026-10-29, after `/sc:workflow` and its advisory `/sc:reflect --mode pre`, report `.dev/reflect/pre-phase2CodegraphI-20261029192356/REPORT.md`, adversarial merge of two calibrated reviewer cards, 19 findings, 0 citations dropped). Findings whose origin is this spec (the plan had copied them) were fixed here as well as in the plan:

| Finding | Result | Reason (one line) |
|---|---|---|
| M-02 | applied | T12's user- and local-scope `jq -e` lines aborted the block before the codegraph checks ran; both now record their result, user scope gates at the end, local scope is report-only, the removal commands are printed, and §7 gains non-blocking item 7. |
| M-08 | applied | U11 tests the phase function's `claude --version` check (§2.4), which T2 creates; moved from T1 to T2. |
| M-09 | applied | `A && B` and `! cmd` lines do not gate under `set -e` mid-block; T5, T7 and T10 now use one condition per line and the if-form, and the §5 rule says so. |
| M-10 | applied | T8's YAML check now uses `uv run python` (pyyaml is a project dependency). |
| M-11 | applied | T12's `grep -i connected` also matched "Disconnected"; a negative check follows it, as in layer 2 step 5. |
| M-13 | applied | T3 prints three `--list` lines; T3b, which creates `codegraph_ready()`, adds the "Ready for Serena retirement" line. |
| M-18 | applied | An empty `$(rg -l install_retired_mcp tests)` (true in this checkout today) made T3b's gate run the whole suite or skip the retire test; the file list is now assigned and checked non-empty first. |
| M-19 | applied | A missing baseline file and `tail -1` both passed vacuously; T5 and T10 check the baseline exists, T9 compares the last line to `LAYER2_OK`. |
| C-1 (calibrator) | applied | Step 0 said the client is committed with T2 while the closing note said T1; both now say T1. |
| C-2 (calibrator) | applied | T12 said "no `superclaude install`" yet ran `install --list`; it now names the read-only `--list` exception. |
| M-01, M-03 to M-07, M-12, M-14 to M-17 | plan or reflect-artifact only | Their origin is the generated plan or the reflect matrix, not this spec; fixed in the plan (M-14 also given one sentence in T9). |
