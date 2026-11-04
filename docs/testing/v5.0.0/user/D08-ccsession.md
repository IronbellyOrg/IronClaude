# E2E Test Guide — `ccsession` (`5.0.0`)

- **Capability:** `ccsession <name>` starts or resumes a Claude Code session under a name that ccsession, Claude Code (`--name`, `/rename`) and the Orca tab share; names belong to the repo and the lists follow the worktree (`--here`, `--here --all`, `--list`, `--rm`, `--ask`); `ccsession-orca` is Orca's Claude command; in a Coder workspace with tier settings, `--tier`, `--model`, `--models-status` and `--refresh-models` pick and inspect the gateway models; the shared gateway shim keeps running when the terminal that started it closes (#341).
- **Audience:** end user
- **Source of truth:** `src/superclaude/skills/ccsession-tag/ccsession:7-93,119-174,267-313,320-412,479-508,555-629,681-701,756-900,936-971,1220-1468,1508-1617`; `src/superclaude/skills/ccsession-tag/ccsession-orca:19-81`; `src/superclaude/skills/ccsession-tag/hooks/session-name.sh:7-18,162-199`; `src/superclaude/skills/ccsession-tag/models.py:53-65,255-328,454-496,630-673,831-1028`; `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:525-540,857-867`; `src/superclaude/hooks/hooks.json:33-42,54-73`; `src/superclaude/cli/doctor.py:57-131`; `CHANGELOG.md:11-22,56-76,151-204`; `docs/testing/v5.0.0/c-e2e-transcript.txt:218,342,353-354`; issue [#352](https://github.com/IronbellyOrg/IronClaude/issues/352)
- **Est. time:** `Tier A: 3 minutes. Tier B: 25-35 minutes. Tier C: 20-40 minutes (Orca needed for Step 17).`

## Preconditions

- IronClaude 5.0.0 installed for your user (`superclaude install` done): `superclaude --version` prints `SuperClaude, version 5.0.0`.
- Linux with `bash`, `git` (2.28 or later), `python3`, `curl`, `ps`, `stty` and `script` (util-linux) in `/usr/bin` or `/bin`. Tier B runs every command with `PATH=/tmp/d08/home/.local/bin:/usr/bin:/bin`.
- `/tmp/d08` does not exist (`[ ! -e /tmp/d08 ] && echo OK` prints `OK`).
- Tier B and Tier C use network access for one step each (Step 13 fetches the model data from GitHub; Tier C talks to your gateway).
- Tier C only: a Coder workspace where `ccsession` already works for you (your `~/.claude/ccsession.env` or workspace env reaches the gateway), and Orca for Step 17. Tier C steps use API tokens.
- **Where the steps write.** Every step that writes does so under `/tmp/d08`, never in your real `~/.claude`.
  - Tier B uses a throwaway `HOME` (`/tmp/d08/home`) holding a copy of your installed ccsession skill, a stand-in `claude` that prints what ccsession hands it and starts nothing, and a scratch repo with two extra worktrees. Tier B never starts Claude Code and never uses your gateway key.
  - Tier C uses a second throwaway `HOME` (`/tmp/d08/c-home`, built in Step 14) and the scratch repo `/tmp/d08/c-repo`. Every Tier C command runs through the helper `c8`, which sets `HOME=/tmp/d08/c-home`. ccsession keeps its name lists, and Claude Code its history, under `$HOME/.claude/projects` (`ccsession:96`). The shim's model cache is `$HOME/.claude/cache/gateway-models.json` (`ccsession:841`), and the model-data check writes `$HOME/.cache/ccsession/` (`models.py:129-131`). All of these land in the throwaway `HOME`.
  - `c8` also unsets `CLAUDE_CONFIG_DIR`, which would move Claude Code's settings and history out of `$HOME/.claude` (Claude Code docs, [environment variables](https://code.claude.com/docs/en/env-vars)) while ccsession keeps reading `$HOME/.claude/projects`. It unsets the `XDG_*` folders too, because ccsession and its model data use `XDG_CACHE_HOME` before `$HOME/.cache` (`ccsession:476`; `models.py:130`). It sets `DISABLE_AUTOUPDATER=1` so Claude Code does not update itself from the throwaway `HOME` (same docs page).
  - Tier C reads two things from your real `HOME` and writes neither: your installed ccsession skill, which is copied, and your `~/.claude/ccsession.env` (gateway address and key), which ccsession sources in place through `CCSESSION_ENV_FILE` (`ccsession:669-675`).
  - The throwaway `HOME` registers only the three ccsession hooks, so the other SuperClaude hooks, which write `~/.claude/state/` and `~/.claude/logs/`, do not run in Tier C (`src/superclaude/hooks/hooks.json:18,33-42,49,54-73`).
- **Two warnings.**
  - Never run `pkill -f local-gateway-alias-proxy.py` during this test. One shim serves every ccsession session of yours with the same settings, so that command cuts the replies of every session you have open (`ccsession:798`; `CHANGELOG.md:22`). This guide stops only its own test shims, by their `/tmp/d08/home/...` path.
  - `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` unless `CC_CLAUDE_FLAGS` is set (`ccsession:78-83,93`): Claude Code then runs tools without asking. In Tier C, type only the prompts this guide gives.
- Known issue, not part of this guide: the ccsession shim tests in `tests/unit/test_ccsession_tiers.py` can fail when the machine is busy (issue [#352](https://github.com/IronbellyOrg/IronClaude/issues/352), open). If you also run the unit tests from a checkout, rerun a failing shim test before you report it.

## What you're verifying

- One name per session: `ccsession <name>` (spaces allowed, `--name` for a name starting with `-`) is also Claude Code's `--name`; a `/rename` inside Claude Code reaches ccsession's list at the next message.
- Names belong to the repo, and the lists follow the worktree: `--here` lists this worktree's sessions, then those whose worktree was removed, and counts the others; `--here --all` and `--list` show everything; `--rm` forgets a name; `--ask` asks for a name and exits 1 or 130 when it gets none.
- In Orca, ccsession owns the tab title (`<name> · Claude Code`), and `ccsession-orca` asks for a name only when someone can answer.
- The gateway shim no longer dies with the terminal that started it.
- In tier mode, `--help`, `--models-status`, `--tier`, `--model` and `--refresh-models` behave as the code says.

---

## Steps

### Tier A — free smoke on your machine (read-only)

#### Step 1 — The installed launchers and their help `[FREE]`

**Do:**

```bash
superclaude --version
ls -l ~/.local/bin/ccsession ~/.local/bin/ccsession-orca
ccsession --help | grep -E -e '--here --all|--ask \[|^  ccsession-orca|--tier <tier>$|--model <name>$|--models-status|--refresh-models$'
```

**Expected result:**

- `SuperClaude, version 5.0.0` (source: `src/superclaude/cli/main.py:19`; transcript `docs/testing/v5.0.0/c-e2e-transcript.txt:20`).
- Two symlinks, `~/.local/bin/ccsession -> <your home>/.claude/skills/ccsession-tag/ccsession` and `~/.local/bin/ccsession-orca -> <your home>/.claude/skills/ccsession-tag/ccsession-orca` (source: `src/superclaude/cli/install_ccsession.py:56-71,132`; install transcript "ccsession wired at ...", `docs/testing/v5.0.0/c-e2e-transcript.txt:218`; `CHANGELOG.md:198`).
- Seven help lines: `ccsession --here --all`, `ccsession --ask [<hint>]`, `ccsession-orca [<claude args>]`, `ccsession <topic> --tier <tier>`, `ccsession <topic> --model <name>`, `ccsession --refresh-models`, `ccsession --models-status` (source: `src/superclaude/skills/ccsession-tag/ccsession:31,47,54,59,62,68,70`; the help prints lines 2-77 of the script, `ccsession:1402-1403`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 2 — Doctor and the naming hooks `[FREE]`

**Do:**

```bash
superclaude doctor --verbose 2>&1 | grep -A1 'ccsession installed'
grep -c 'ccsession-tag/hooks/session-start.sh' ~/.claude/settings.json
grep -c 'ccsession-tag/hooks/session-name.sh' ~/.claude/settings.json
```

**Expected result:**

- `✅ ccsession installed`, then `ccsession skill, launcher, env and hook present` (source: `src/superclaude/cli/doctor.py:126-131`; transcript `docs/testing/v5.0.0/c-e2e-transcript.txt:353-354`). A `(warning: ~/.local/bin not on PATH)` after the name means your `PATH` lacks `~/.local/bin` (`doctor.py:121-128`). A FAIL lists what is missing, for example `ccsession UserPromptSubmit hook not registered` (`doctor.py:65-119`).
- `1`, then `2`: the SessionStart hook once, and `session-name.sh` for UserPromptSubmit and SessionEnd (source: `src/superclaude/hooks/hooks.json:33-42,54-73`; `CHANGELOG.md:61,65`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 3 — Model data and tier mode of this workspace `[FREE]`

**Do:**

```bash
ccsession --models-status
```

**Expected result:** these lines, with your own values (source: `src/superclaude/skills/ccsession-tag/models.py:993-1028`):

```text
Model data version: <version> (downloaded|bundled|built-in minimum)
Source URL:         https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/src/superclaude/skills/ccsession-tag/ccsession-models.json
Cache:              <your home>/.cache/ccsession/models.json
Last check:         <time> <status>   (or: never)
Profiles:           claude, gpt, grok, muse, wonderfull, wonder, qwen, glm
Tier mode:          on (settings from /etc/aidev02/aienv.d/defaults.sh); tiers: tier0, tier1a, ...
Access:             <your user>: not listed; default tier, every tier   (or your rule's start tier and tiers)
```

The version is `2026-10-28.1` or newer (bundled copy, `ccsession-models.json:3`); the profile names are those of that data. Outside a Coder workspace with tier settings, the last line is `Tier mode:          off (no T<N>_WINDOW in the workspace env)` (`models.py:1026-1027`). A `tiers: invalid (...)` value names a missing workspace setting, for example `T1aModel01 is not set (needed by tier1a)` (`models.py:661-664`). Write down whether tier mode is on and which tiers your `Access:` line gives you: Step 16 needs it.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — local writes in a throwaway HOME under /tmp/d08

Every Tier B command runs through the helper `d8`, which starts ccsession with `env -i` (nothing from your shell leaks in), `HOME=/tmp/d08/home`, the stand-in `claude` (`CLAUDE_BIN`, `ccsession:92`), a gateway address on a closed port (`http://127.0.0.1:9/cli`), the shim port `4890`, no model-data check at launch (`CCSESSION_MODELS_REFRESH=0`, `ccsession:1483`) and, unless `D8_DEFAULTS` is set, no workspace env file (`AIDEV_AI_DEFAULTS_PATH`, `models.py:320-328`). `D8_EXTRA` adds settings for one command. Keep the terminal you use for Step 4 open until Cleanup.

#### Step 4 — Build the throwaway HOME, the stand-in and a scratch repo `[LOCAL-WRITE]`

**Do:**

```bash
[ ! -e /tmp/d08 ] || { echo "remove /tmp/d08 first"; false; }
for p in 4890 4991 5092; do printf '%s ' "$p:$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$p/")"; done; echo
mkdir -p /tmp/d08/home/.claude/skills /tmp/d08/home/.local/bin /tmp/d08/bin
cp -r ~/.claude/skills/ccsession-tag /tmp/d08/home/.claude/skills/
rm -rf /tmp/d08/home/.claude/skills/ccsession-tag/__pycache__
for f in ccsession ccsession-orca; do ln -s "/tmp/d08/home/.claude/skills/ccsession-tag/$f" "/tmp/d08/home/.local/bin/$f"; done
cat > /tmp/d08/bin/claude <<'EOF'
#!/bin/bash
# Stand-in for Claude Code: prints what ccsession handed it, then exits.
printf 'FAKE-CLAUDE args:'; printf ' [%.60s]' "$@"; echo
echo "FAKE-CLAUDE CLAUDE_TOPIC=${CLAUDE_TOPIC:-} TITLE_OFF=${CLAUDE_CODE_DISABLE_TERMINAL_TITLE:-} BASE_URL=${ANTHROPIC_BASE_URL:-}"
EOF
chmod +x /tmp/d08/bin/claude
cat > /tmp/d08/d8.sh <<'EOF'
d8() {
  env -i HOME=/tmp/d08/home PATH=/tmp/d08/home/.local/bin:/usr/bin:/bin LANG=C.UTF-8 \
    TERM="${TERM:-xterm}" CLAUDE_BIN=/tmp/d08/bin/claude CC_SHIM_PORT=4890 \
    ANTHROPIC_BASE_URL=http://127.0.0.1:9/cli CCSESSION_MODELS_REFRESH=0 \
    AIDEV_AI_DEFAULTS_PATH="${D8_DEFAULTS:-/tmp/d08/no-defaults.sh}" \
    ${D8_EXTRA:-} "$@"
}
mk() {  # <folder> <session id> <name>: a stand-in transcript, then the name
  local d
  d=/tmp/d08/home/.claude/projects/$(printf '%s' "$1" | sed 's/[^A-Za-z0-9]/-/g')
  mkdir -p "$d"
  printf '{"cwd":"%s","gitBranch":"%s"}\n' "$1" "$(git -C "$1" branch --show-current)" > "$d/$2.jsonl"
  (cd "$1" && d8 ccsession --sync-name "$2" "$3")
}
EOF
source /tmp/d08/d8.sh
git init -q -b main /tmp/d08/repo
git -C /tmp/d08/repo -c user.name=d08 -c user.email=d08@example.invalid commit -q --allow-empty -m init
git -C /tmp/d08/repo remote add origin https://github.com/example/d08-repo.git
git -C /tmp/d08/repo worktree add -q /tmp/d08/repo-wt2 -b wt2
git -C /tmp/d08/repo worktree add -q /tmp/d08/repo-wt3 -b wt3
cd /tmp/d08/repo && d8 ccsession --key
mk /tmp/d08/repo aaaaaaaa-0000-4000-8000-000000000001 "my work"
mk /tmp/d08/repo bbbbbbbb-0000-4000-8000-000000000002 "-dash name"
mk /tmp/d08/repo-wt2 cccccccc-0000-4000-8000-000000000003 "wt2 task"
mk /tmp/d08/repo-wt3 dddddddd-0000-4000-8000-000000000004 "wt3 task"
mk /tmp/d08/repo eeeeeeee-0000-4000-8000-000000000005 "my work"
git -C /tmp/d08/repo worktree remove /tmp/d08/repo-wt3
```

**Expected result:**

- `4890:000 4991:000 5092:000`: nothing listens on the three ports this guide's Tier B test shims use, `CC_SHIM_PORT=4890` and the next ports a launch tries, 101 apart (source: `ccsession:772-775`; curl's `%{http_code}` is `000` when no HTTP answer came). Any other code means a port is taken; stop and pick this test another day rather than change the ports.
- `github.com-example-d08-repo`: the name-list key is the repo's network `origin` as host and path, so every worktree of the repo shares one list. The origin is never contacted (source: `ccsession:119-174`, `ccsession --key` at `:33,513-516`; `CHANGELOG.md:174,179`).
- The five `mk` lines print `my work`, `-dash name`, `wt2 task`, `wt3 task` and then `my work-2`: `--sync-name` (the call the naming hooks make) prints the name it saved, and a name another saved session already has gets `-2` (source: `ccsession:37-39,320-412`, suffix loop `:383-390`; `CHANGELOG.md:69`). Each `mk` first writes a one-line stand-in transcript where Claude Code keeps it (a folder named after the session's folder, every other character than a letter or digit turned into `-`). The transcripts give the list its times (`ccsession:1269-1277`), the worktree each session was started in (`session_home` and `session_place`, `ccsession:1043-1144`) and the saved-session check behind the `-2` suffix (`ccsession:383-390`, `session_saved` at `:315-318`). Without a transcript the list still shows the name, as `(transcript missing)` (`ccsession:1261-1263`).
- No other output: `--sync-name` prints the name only when it changed something, and the `git` commands print nothing when they succeed (source: `ccsession:410`). The copy runs exactly your installed ccsession; it is copied because ccsession looks for its shim under `$HOME/.claude/skills/ccsession-tag/` (`ccsession:97`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — `--here`, `--here --all` and `--list` `[LOCAL-WRITE]`

**Do:** (in the Step 4 terminal, in `/tmp/d08/repo`)

```bash
d8 ccsession --here
d8 ccsession --here --all
cd /tmp && d8 ccsession --list; cd /tmp/d08/repo
```

**Expected result:** (`<date>` and the times are today's; a file system that keeps no creation time shows `(times unavailable)` in place of the times, `ccsession:1271-1273`)

```text

repo
  -dash name              started <date> <hh:mm>  last <hh:mm>  (0m)  bbbbbbbb
  my work-2               started <date> <hh:mm>  last <hh:mm>  (0m)  eeeeeeee
  my work                 started <date> <hh:mm>  last <hh:mm>  (0m)  aaaaaaaa
Sessions whose worktree was removed (they continue here):
  wt3 task                started <date> <hh:mm>  last <hh:mm>  (0m)  dddddddd  (was /tmp/d08/repo-wt3)
1 more session in other worktrees of this repo: ccsession --here --all
```

- `--here` lists this worktree's sessions, then the sessions whose worktree was removed with the folder they were started in, and only counts the session of `repo-wt2`, which still exists (source: `ccsession:27-31,1220-1322`, section lines `:1303-1311`; `CHANGELOG.md:15`).
- `--here --all` and `--list` print the same `repo` heading and all five rows, `wt2 task` (`cccccccc`) and `wt3 task` (`dddddddd`) included, with no section line and no count (source: `ccsession:1436-1449`; `--list` covers every workspace, `ccsession:26`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — A name at launch is Claude Code's name too `[LOCAL-WRITE]`

**Do:**

```bash
d8 ccsession "brand new"
d8 ccsession "my work"
d8 ccsession "wt2 task"
d8 ccsession --name "-dash name" --claude-args -p hi
d8 ccsession "-dash name"
D8_EXTRA="CC_CLAUDE_FLAGS=--verbose" d8 ccsession "my work"
ls /tmp/d08/home/.claude/projects/github.com-example-d08-repo/topics/
```

**Expected result:**

1. `[ccsession] Starting new session labeled 'brand new'`, then `FAKE-CLAUDE args: [--dangerously-skip-permissions] [--allowedTools=Grep] [--name] [brand new]` and `FAKE-CLAUDE CLAUDE_TOPIC=brand new TITLE_OFF= BASE_URL=http://127.0.0.1:9/cli`: a name with a space is one name, passed to Claude Code as `--name` (source: `ccsession:1592-1616`; `CHANGELOG.md:60,69`).
2. `[ccsession] Resuming 'my work' (session aaaaaaaa)`, then args `[--dangerously-skip-permissions] [--allowedTools=Grep] [--name] [my work] [--resume] [aaaaaaaa-0000-4000-8000-000000000001]` (source: `ccsession:1595-1609`).
3. `[ccsession] Resuming 'wt2 task' (session cccccccc)`, then `[ccsession] WARNING: 'wt2 task' was started in /tmp/d08/repo-wt2. It continues here, in /tmp/d08/repo: its edits and commits go to this worktree. To work in its own worktree instead, exit and run ccsession there.`, then args ending `[--name] [wt2 task] [--resume] [cccccccc-0000-4000-8000-000000000003]` (source: `ccsession:1597-1604`; `CHANGELOG.md:16`).
4. `[ccsession] Resuming '-dash name' (session bbbbbbbb)`, then args ending `[--name] [-dash name] [--resume] [bbbbbbbb-0000-4000-8000-000000000002] [-p] [hi]`: `--name` takes a name starting with `-`, and everything after `--claude-args` goes to Claude Code unchanged (source: `ccsession:11-12,43-46,555-575`; `CHANGELOG.md:63,200`).
5. `[ccsession] Starting untagged session`, then `FAKE-CLAUDE args: [--dangerously-skip-permissions] [--allowedTools=Grep] [-dash name]` and an empty `CLAUDE_TOPIC=`: without `--name`, a first argument starting with `-` is read as a Claude Code option, never as a name (source: `ccsession:1538-1550`; `CHANGELOG.md:204`).
6. `[ccsession] Resuming 'my work' (session aaaaaaaa)`, then `FAKE-CLAUDE args: [--verbose] [--name] [my work] [--resume] [aaaaaaaa-0000-4000-8000-000000000001]`: `CC_CLAUDE_FLAGS` replaces the default `--dangerously-skip-permissions --allowedTools=Grep` (source: `ccsession:78-83,93`).
7. The list folder holds `-dash name.txt`, `my work-2.txt`, `my work.txt`, `wt2 task.txt`, `wt3 task.txt` and no `brand new.txt`. ccsession itself never saves a new name: the SessionStart hook of the real Claude Code does (`ccsession:1571-1572`; `hooks/session-name.sh:162-168,185-192`), and the stand-in runs no hooks. Tier C Step 14 checks the real save.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 7 — Name rules, a lost conversation and `--rm` `[LOCAL-WRITE]`

**Do:**

```bash
d8 ccsession "$(printf 'a\tb')"; echo "exit=$?"
d8 ccsession "   "; echo "exit=$?"
d8 ccsession --rm "my work-2"; echo "exit=$?"
d8 ccsession --rm "my work-2"; echo "exit=$?"
d8 ccsession --rm; echo "exit=$?"
rm /tmp/d08/home/.claude/projects/-tmp-d08-repo/bbbbbbbb-0000-4000-8000-000000000002.jsonl
d8 ccsession --name "-dash name"; echo "exit=$?"
```

**Expected result:**

- `ccsession: invalid label (no tabs, newlines or other control characters)`, `exit=2`; `ccsession: empty label`, `exit=2` (source: `ccsession:267-294,1552-1557`).
- `Removed label 'my work-2' from this workspace.`, `exit=0`; then `No label 'my work-2' in this workspace.`, `exit=1`; then `Usage: ccsession --rm <topic>`, `exit=2` (source: `ccsession:32,1454-1468`). `--rm` deletes the name only; the stand-in transcript `eeeeeeee-...jsonl` is still under `/tmp/d08/home/.claude/projects/-tmp-d08-repo/`.
- With the conversation gone: `[ccsession] Session bbbbbbbb for '-dash name' has no saved conversation; starting a new one`, then `[ccsession] Starting new session labeled '-dash name'`, args ending `[--name] [-dash name]`, `exit=0`. ccsession drops the stale name rather than resume an id Claude Code no longer has (source: `ccsession:1580-1590`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — The session-name question, `--ask` `[LOCAL-WRITE]`

**Do:** run each line on its own, at the terminal (the question needs a terminal on standard input and standard error), and act as noted:

```bash
d8 ccsession --ask; echo "exit=$?"                                   # type: picked one, then Enter
d8 ccsession --ask; echo "exit=$?"                                   # press Enter
d8 ccsession --ask; echo "exit=$?"                                   # type: *  then Enter; then press Enter
D8_EXTRA=CCSESSION_ASK_TIMEOUT=3 d8 ccsession --ask; echo "exit=$?"  # type nothing for 3 seconds
d8 ccsession --ask; echo "exit=$?"                                   # press Ctrl+C
d8 ccsession --ask; echo "exit=$?"                                   # press Ctrl+D
d8 ccsession --ask </dev/null; echo "exit=$?"                        # no terminal
```

**Expected result:** every question starts with this list on the terminal (source: `ccsession:1345-1375`):

```text

Saved sessions in /tmp/d08/repo (type a name to resume it):
  my work                 started <date> <hh:mm>  last <hh:mm>  (0m)  aaaaaaaa
Sessions whose worktree was removed (they continue here):
  wt3 task                started <date> <hh:mm>  last <hh:mm>  (0m)  dddddddd  (was /tmp/d08/repo-wt3)
1 more session in other worktrees of this repo: type * to list them
Sessions from other repos and folders: ccsession --list

Session name (Enter = untagged, Ctrl+C = plain shell):
```

(`-dash name` is not listed: in Step 7, with its conversation gone, ccsession deleted the name, and the stand-in did not save the new one (source: `ccsession:1584-1590`). `my work-2` was removed with `--rm` (source: `ccsession:1454-1468`).)

1. `picked one` printed on its own line, `exit=0`: only the chosen name goes to standard output (source: `ccsession:1388-1399`; `CHANGELOG.md:199`).
2. An empty line, `exit=0`: Enter means untagged (source: `ccsession:1389-1391,1399`).
3. `*` prints `Saved sessions in every worktree of this repo (type a name to resume it):` with `my work`, `wt2 task` and `wt3 task`, then asks again; Enter gives an empty line and `exit=0` (source: `ccsession:1392-1395`).
4. After 3 seconds an empty line and `exit=1` (source: `ccsession:1376-1390`).
5. `^C`, then `exit=130` (source: `ccsession:1383-1384`).
6. `exit=1`: end of input (source: `ccsession:1389-1390`).
7. Nothing printed, `exit=1`: no terminal, no question (source: `ccsession:1329`; help `ccsession:47-53`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 9 — The Orca tab title `[LOCAL-WRITE]`

**Do:** (`script` gives the command a terminal and records what it prints)

```bash
script -qec 'bash -c "source /tmp/d08/d8.sh && D8_EXTRA=ORCA_PANE_KEY=d08 d8 ccsession \"my work\""' /dev/null | cat -v
script -qec 'bash -c "source /tmp/d08/d8.sh && D8_EXTRA=ORCA_PANE_KEY=d08 d8 ccsession --claude-args -p hi"' /dev/null | cat -v
script -qec 'bash -c "source /tmp/d08/d8.sh && D8_EXTRA=\"ORCA_PANE_KEY=d08 CLAUDECODE=1\" d8 ccsession \"my work\""' /dev/null | cat -v
```

**Expected result:** (`cat -v` shows the title escape as `^[]0;...^G` and the `·` as `M-BM-7`; lines end in `^M`)

- The first output starts `^[]0;my work M-BM-7 Claude Code^G[ccsession] Resuming 'my work' (session aaaaaaaa)` and its last line has `TITLE_OFF=1`: in an Orca terminal (`ORCA_PANE_KEY` set) ccsession sets the title `my work · Claude Code` and starts Claude Code with `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` so it keeps that title (source: `ccsession:1508-1523,1578`; `CHANGELOG.md:192`).
- The second shows `^[]0;Claude Code^G` (untagged) before the `FAKE-CLAUDE` lines, again with `TITLE_OFF=1` (source: `ccsession:1521,1544`).
- The third has no `^[]0;` at all and an empty `TITLE_OFF=`: a ccsession started inside Claude Code (`CLAUDECODE` set) leaves the tab to the session around it (source: `ccsession:1525-1529`; `CHANGELOG.md:74`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 10 — The shim keeps running after its terminal closes (#341) `[LOCAL-WRITE]`

Use an Orca terminal tab for this step if you have Orca (Orca kills a closed tab's processes); otherwise any terminal window.

**Do:**

1. In the Step 4 terminal: `pgrep -af '^python3 /tmp/d08/home/'` — prints nothing (no test shim yet).
2. Open a **second** terminal tab and run:

   ```bash
   source /tmp/d08/d8.sh && cd /tmp/d08/repo && d8 ccsession --shim 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
   ```

3. Close that second tab with its close button (do not type `exit`).
4. Back in the Step 4 terminal:

   ```bash
   P=$(pgrep -f '^python3 /tmp/d08/home/'); echo "P=$P"
   ps -o pid,ppid,sid,args -p "$P"
   curl -s http://127.0.0.1:4890/__ccsession_shim; echo
   d8 ccsession --shim 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
   ```

**Expected result:**

- Step 2 prints `[ccsession] Starting model-alias shim on 127.0.0.1:4890`, `[ccsession] WARNING: could not pre-load gateway models; Claude Code will retry discovery after launch` (expected: the test gateway address is a closed port), `[ccsession] Starting untagged session`, then `FAKE-CLAUDE args: [--dangerously-skip-permissions] [--allowedTools=Grep]` and `... BASE_URL=http://127.0.0.1:4890`: through the shim, Claude Code talks to `127.0.0.1:<port>` (source: `ccsession:15-19,756-900`, start at `:801-813`, warning `:898`, address `:835`).
- After the tab is closed, `P=<one pid>`, and `ps` shows that pid with `PPID` `1` (or another adopting process) and `SID` equal to its own `PID`: the shim was started from a subshell that exits at once and runs in a session of its own, so closing the terminal does not stop it (source: `ccsession:803-813`; `local-gateway-alias-proxy.py:857-867`; `CHANGELOG.md:22`). FAIL if `P=` is empty.
- The health answer is one JSON line with `"service": "ccsession-gateway-alias-proxy"`, `"upstream": "http://127.0.0.1:9/cli"`, `"port": 4890`, `"tier_mode": false` and `"pid": <P>` (source: `local-gateway-alias-proxy.py:525-540`).
- The new launch prints `[ccsession] Shim already running on 127.0.0.1:4890 (reusing)` before the warning and the `FAKE-CLAUDE` lines (source: `ccsession:780-784`).
- Leave this shim running: Steps 11 and 12 use it.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 11 — `ccsession-orca` asks only when someone can answer `[LOCAL-WRITE]`

**Do:**

```bash
d8 ccsession-orca </dev/null 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
d8 ccsession-orca --resume abc 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
D8_EXTRA=CCSESSION_AUTOSTART=0 d8 ccsession-orca "fix the bug" --prefill x 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE'
d8 ccsession-orca
```

At the last command's question, type `orca pick` and press Enter.

**Expected result:**

- The first three each print `[ccsession] Shim already running on 127.0.0.1:4890 (reusing)`, the pre-load warning, `[ccsession] Starting untagged session`, and then the args: `[--dangerously-skip-permissions] [--allowedTools=Grep]` (no terminal: no question); `... [--resume] [abc]` (Orca resuming: no question); `... [fix the bug] [--prefill] [x]` (`CCSESSION_AUTOSTART=0`: no question). Orca's own arguments reach Claude Code unchanged, after `--claude-args`, and every launch goes through the shim (source: `ccsession-orca:19-24,44-59,76-81`; `CHANGELOG.md:198`).
- The last one shows the Step 8 list, then `Session name (Enter or Ctrl+C = untagged; untagged after 30s):` (source: `ccsession-orca:62-72`). After `orca pick`: the reuse line, a Python error report from the gateway pre-load ending in a connection error, the pre-load warning (both expected here), `[ccsession] Starting new session labeled 'orca pick'` and `FAKE-CLAUDE args: [--dangerously-skip-permissions] [--allowedTools=Grep] [--name] [orca pick]` (source: `ccsession-orca:77-79`). Pressing Enter, Ctrl+C or waiting 30 seconds instead starts an untagged session (`ccsession-orca:72,81`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 12 — Tier mode with a throwaway workspace env file `[LOCAL-WRITE]`

**Do:**

```bash
{
  echo 'export CCSESSION_DEFAULT_TIER=tier2'
  for t in 0:2 1a:2 1b:3 2:6 3:6 4:1; do
    n=${t%:*}; echo "export T${n}_WINDOW=400000"
    for i in $(seq 1 "${t#*:}"); do
      printf 'export T%sModel%02d=d08-t%s-m%d\nexport T%sModel%02d_WINDOW=400000\n' "$n" "$i" "$n" "$i" "$n" "$i"
    done
  done
} > /tmp/d08/defaults.sh
sed -i 's/^export T1aModel01=.*/export T1aModel01=claude-opus-5-5/; s/^export T1aModel01_WINDOW=.*/export T1aModel01_WINDOW=1000000/' /tmp/d08/defaults.sh
export D8_DEFAULTS=/tmp/d08/defaults.sh
d8 ccsession --help | sed -n '/^Tiers in this workspace/,$p'
d8 ccsession --models-status | tail -n 2
d8 ccsession "my work" --tier 1A 2>&1 | grep -E '^\[ccsession\]|^FAKE-CLAUDE|^ccsession'
d8 ccsession "my work" --model claude-opus-5-5 2>&1 | grep -E '^\[ccsession\] model|^FAKE-CLAUDE args'
d8 ccsession "my work" --tier 9; echo "exit=$?"
unset D8_DEFAULTS
```

**Expected result:**

- The help ends with `Tiers in this workspace (* = default):` and six entries, `ccsession --tier tier0` to `ccsession --tier tier4`, each followed by `Tier <n>, 400000 token window: <its models>`; `tier1a` lists `claude-opus-5-5, d08-t1a-m2`, and only `tier2` carries the `*` (source: `ccsession:1402-1413`; `models.py:923-935`; tier names and slots `ccsession-models.json:70-121`; `CHANGELOG.md:156,160`).
- `Tier mode:          on (settings from /tmp/d08/defaults.sh); tiers: tier0, tier1a, tier1b, tier2, tier3, tier4` and `Access:             owner unknown (no CODER_WORKSPACE_OWNER_NAME): not listed; default tier, every tier` (source: `models.py:469-479,1004-1025`).
- `--tier 1A` prints `[ccsession] tier1a (Tier 1a: claude-opus-5-5, d08-t1a-m2): model claude-gw-tier1a[1m], context 400000, auto-compact window 400000`, then `[ccsession] A shim with other settings or older code is on 127.0.0.1:4890; leaving it running for its sessions`, `[ccsession] Starting model-alias shim on 127.0.0.1:4991`, the pre-load warning and `[ccsession] Resuming 'my work' (session aaaaaaaa)`. The args are `[--dangerously-skip-permissions] [--allowedTools=Grep] [--settings] [{"modelSettings":...] [--model] [claude-gw-tier1a[1m]] [--name] [my work] [--resume] [aaaaaaaa-...]`, and `BASE_URL=http://127.0.0.1:4991`. `1A` and `1a` are the same tier; tier mode always uses the shim; a shim with other settings is never stopped, the launch moves to the next port (source: `ccsession:687-692,773-796,936-971,957,1487-1497`; `models.py:489-496,843-863`; `CHANGELOG.md:156`).
- `--model claude-opus-5-5` prints `[ccsession] model claude-opus-5-5 (claude-opus-5-5 (T1aModel01)): model claude-opus-5-5[1m], context 1000000, auto-compact window 1000000` and args with `[--model] [claude-opus-5-5[1m]]`: the window comes from the first tier slot naming the model (source: `models.py:715-732,872-922`; `CHANGELOG.md:167`).
- `ccsession: tier9 is not defined`, `exit=2` (source: `models.py:630-637,850-853`; `ccsession:956`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 13 — `--refresh-models` `[LOCAL-WRITE]`

**Do:** (needs access to `raw.githubusercontent.com`; writes only `/tmp/d08/home/.cache/ccsession/`)

```bash
d8 ccsession --refresh-models
d8 ccsession --refresh-models | grep 'model data check'
D8_EXTRA=CCSESSION_MODELS_URL=http://127.0.0.1:9/x.json d8 ccsession --refresh-models | sed -n '1p;3p;5p'
ls /tmp/d08/home/.cache/ccsession/
```

**Expected result:**

- First run: `[ccsession] model data check: downloaded`, then the status block with `Model data version: <version> (downloaded)` (`2026-10-28.1` or newer), the GitHub `Source URL`, `Cache:              /tmp/d08/home/.cache/ccsession/models.json` and `Last check:         <time> downloaded`. If the fork's `master` has newer data, a line `[ccsession] model list updated to <version>: ...` comes first (source: `ccsession:68-69,1427-1431`; `models.py:247-252,255-314,833-838,993-1003`).
- Second run: `[ccsession] model data check: not modified` (the cached ETag is sent; source: `models.py:258-263,290-291`).
- Unreachable URL: `[ccsession] model data check: failed: URLError`, `Source URL:         http://127.0.0.1:9/x.json`, `Last check:         <time> failed: URLError`; the downloaded copy stays in use and the command still exits 0 (source: `models.py:292-293,296-314,835-838`).
- The cache holds `models.checked`, `models.etag` and `models.json` (source: `models.py:283-288,305-308`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier C — interactive Claude Code sessions in a throwaway HOME, on your gateway

Each step below starts a real Claude Code session (API tokens) through a copy of your installed ccsession, with `HOME=/tmp/d08/c-home` (see Preconditions). In every session type only the prompt given. Run Tier C in a terminal whose current shell has no `D8_*` variables set (open a new tab), after Steps 4-13 and before Cleanup. Every Tier C command starts with `c8`; a command without it would use your real `HOME`.

#### Step 14 — A named session is saved under its name `[CLAUDE-SESSION]`

**Do:** first build the Tier C throwaway `HOME` and the helper `c8`:

```bash
[ -d /tmp/d08/home ] && [ ! -e /tmp/d08/c-home ] || { echo "run Steps 4-13 first; /tmp/d08/c-home must not exist"; false; }
grep -s -c '^[^#]*CC_SHIM_PORT=' ~/.claude/ccsession.env
curl -s -o /dev/null -w '5193:%{http_code}\n' http://127.0.0.1:5193/
mkdir -p /tmp/d08/c-home/.claude/skills /tmp/d08/c-home/.local/bin && chmod 700 /tmp/d08/c-home
cp -r ~/.claude/skills/ccsession-tag /tmp/d08/c-home/.claude/skills/
rm -rf /tmp/d08/c-home/.claude/skills/ccsession-tag/__pycache__
for f in ccsession ccsession-orca; do ln -s "/tmp/d08/c-home/.claude/skills/ccsession-tag/$f" "/tmp/d08/c-home/.local/bin/$f"; done
cat > /tmp/d08/c-home/.claude/settings.json <<'EOF'
{
  "hooks": {
    "SessionStart": [
      {"matcher": "startup|resume", "hooks": [{"type": "command", "command": "~/.claude/skills/ccsession-tag/hooks/session-start.sh", "timeout": 5}]}
    ],
    "UserPromptSubmit": [
      {"hooks": [{"type": "command", "command": "~/.claude/skills/ccsession-tag/hooks/session-name.sh", "timeout": 5}]}
    ],
    "SessionEnd": [
      {"hooks": [{"type": "command", "command": "~/.claude/skills/ccsession-tag/hooks/session-name.sh", "timeout": 5}]}
    ]
  }
}
EOF
printf 'C8_ENV_FILE=%q\n' "$HOME/.claude/ccsession.env" > /tmp/d08/c8.sh
cat >> /tmp/d08/c8.sh <<'EOF'
c8() {  # run a command with the Tier C throwaway HOME; your ccsession.env is only read
  env -u CLAUDE_CONFIG_DIR -u XDG_CACHE_HOME -u XDG_CONFIG_HOME -u XDG_DATA_HOME -u XDG_STATE_HOME \
    HOME=/tmp/d08/c-home PATH="/tmp/d08/c-home/.local/bin:$PATH" CC_SHIM_PORT=5193 \
    CCSESSION_ENV_FILE="$C8_ENV_FILE" DISABLE_AUTOUPDATER=1 "$@"
}
EOF
source /tmp/d08/c8.sh
c8 bash -c 'echo "HOME=$HOME"; command -v ccsession claude'
```

Then start the session:

```bash
git init -q /tmp/d08/c-repo && cd /tmp/d08/c-repo && c8 ccsession --key
c8 ccsession "d08 first"
```

In the session type `Reply with the single word OK. Do not use any tools.`, wait for the reply, then `/exit`. Then:

```bash
c8 ccsession --here
cat /tmp/d08/c-home/.claude/projects/-tmp-d08-c-repo/topics/'d08 first.txt'
ls -d ~/.claude/projects/-tmp-d08-c-repo
```

**Expected result:**

- `0`, or no output when you have no `~/.claude/ccsession.env`: your env file does not choose the shim port. ccsession sources that file after reading `CC_SHIM_PORT`, so a port set there would replace `c8`'s `5193` (source: `ccsession:98-99,669-679`). Any other number: stop and mark Tier C N/A. Tier C would then start its test shim on your own port, where your real sessions could reuse it, and Cleanup would stop it.
- `5193:000`: nothing listens on the Tier C shim port (curl's `%{http_code}` is `000` when no HTTP answer came). With `CC_SHIM_PORT` set, ccsession tries that port first and does not pick a port of its own for its settings (source: `ccsession:98,679,1494-1496`). Any other code: stop and pick this test another day.
- `HOME=/tmp/d08/c-home`, then `/tmp/d08/c-home/.local/bin/ccsession`, then the path of your Claude Code outside `/tmp/d08`. If no `claude` line appears, your Claude Code is found only through your real `HOME`: stop and mark Tier C N/A. The three hook entries are the ones `superclaude install` registers for ccsession, written with `~` as there, so they run the copies in the throwaway `HOME` (source: `src/superclaude/hooks/hooks.json:33-42,54-73`). The hooks call the ccsession beside them (`hooks/session-name.sh:172-184`).
- `-tmp-d08-c-repo`: a repo without a network origin keys its names on its main folder (source: `ccsession:164-173`; `CHANGELOG.md:174`).
- The launch prints `[ccsession] Starting new session labeled 'd08 first'` (in tier mode after the tier and shim lines of Step 16), and Claude Code shows the session name `d08 first` (source: `ccsession:1611-1616`; `CHANGELOG.md:60`). How Claude Code displays the name is its own interface: UNVERIFIED wording.
- UNVERIFIED: Claude Code was not started in a fresh `HOME` while this guide was written. It may first show its own first-run screens: a theme choice, a confirmation for `--dangerously-skip-permissions`, or a folder-trust question. Answer them; they write only under `/tmp/d08/c-home`. If it asks you to log in, your gateway access comes from a Claude Code login rather than from `ccsession.env` or the workspace env. Log in (the login is saved in the throwaway `HOME`), or mark Tier C N/A. Through the shim, ccsession passes an `ANTHROPIC_API_KEY` as a bearer token, so Claude Code does not ask you to approve the key (source: `ccsession:1498-1506`).
- `--here` prints a `c-repo` heading and one row `d08 first` with times and the first 8 characters of a session id; the `cat` prints that full session id. The SessionStart hook saved the label for the session ccsession launched (source: `hooks/session-name.sh:162-168,185-192`; `hooks.json:33-42`).
- `ls` reports `No such file or directory`: the session's name and history went to the throwaway `HOME`, not to your real `~/.claude` (source: `ccsession:96,339`). A folder left by an older run of this guide is not a FAIL; check that its times are older than today's.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 15 — `/rename` reaches the list at the next message `[CLAUDE-SESSION]`

**Do:**

1. `cd /tmp/d08/c-repo && c8 ccsession "d08 first"`, then in the session `/rename d08 renamed`.
2. In a second terminal: `source /tmp/d08/c8.sh && cd /tmp/d08/c-repo && c8 ccsession --here`.
3. In the session type `Reply with OK. Do not use any tools.`, wait for the reply.
4. In the second terminal: `c8 ccsession --here` again.
5. In the session `/exit`, then `c8 ccsession "d08 renamed"` and `/exit` at once.

**Expected result:**

- Launch 1 prints `[ccsession] Resuming 'd08 first' (session <id8>)`, with the `<id8>` of Step 14 (source: `ccsession:1595-1596,1608`).
- Check 2 still lists `d08 first`: Claude Code runs no hook at a rename, so the list changes at the next message or when the session ends (source: `hooks/session-name.sh:7-14`; `CHANGELOG.md:61`).
- Check 4 lists `d08 renamed` with the same `<id8>` and no `d08 first` row: the UserPromptSubmit hook copied the new name and removed the old one (source: `hooks/session-name.sh:185-192`; `ccsession:320-330,397-404`; `CHANGELOG.md:61,76`).
- Launch 5 prints `[ccsession] Resuming 'd08 renamed' (session <id8>)`, the same id (source: `ccsession:1595-1596,1608`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 16 — `--tier 1a` and `--model` on your workspace gateway `[CLAUDE-SESSION]`

Skip this step (mark N/A) if Step 3 showed `Tier mode: off`.

**Do:**

```bash
cd /tmp/d08/c-repo && c8 ccsession --help | sed -n '/^Tiers in this workspace/,$p'
c8 ccsession d08-tier --tier 1a
```

In the session type `/model` and note the list (Esc to close it), then `Reply with OK. Do not use any tools.`, then `/exit`. Then, with `<m>` the first model the help lists for `tier1a`:

```bash
c8 ccsession d08-model --model <m>
```

Type `Reply with OK. Do not use any tools.`, then `/exit`.

**Expected result:**

- The help lists only the tiers your `Access:` line in Step 3 allows, `*` on your start tier (source: `models.py:923-935`; `ccsession:1404-1411`; `CHANGELOG.md:186`).
- `d08-tier`: `[ccsession] tier1a (Tier 1a: <models>): model claude-gw-tier1a[1m], context <window>, auto-compact window <window>`, then a shim line, `[ccsession] Shim already running on 127.0.0.1:5193 (reusing)` (the Tier C launches of Steps 14-15 started it in tier mode) or else `[ccsession] Starting model-alias shim on 127.0.0.1:5193`, then `[ccsession] Starting new session labeled 'd08-tier'`. A shim with other settings on `5193` is left running and the launch moves to `5294`. The reply arrives, so the tier routes through the shim to the gateway (source: `ccsession:773-813,936-971,1487-1497`; `models.py:843-863`).
- `/model` lists the tiers you may use (and each model of them only when your rule says `+models`); UNVERIFIED: the exact labels Claude Code shows (source: `local-gateway-alias-proxy.py:172-203`; `CHANGELOG.md:155,186`).
- `d08-model`: `[ccsession] model <m> (<m> (T1aModel01)): model <m>..., context <window>, ...`; a Claude-named model with a window above 200000 is passed as `<m>[1m]` (source: `models.py:872-922`).
- If `tier1a` is not yours: `ccsession: tier1a is not available to <user> (available: <your tiers>)` and exit 2, which is a PASS for a limited user (source: `models.py:630-637,850-853`). An unset tier slot gives `ccsession: T1aModel01 is not set (needed by tier1a)`: the workspace env file predates the 2026-10-28.1 layout, a note, not a ccsession FAIL (`models.py:661-664`; `CHANGELOG.md:160`).

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

#### Step 17 — `ccsession-orca` as Orca's Claude command `[CLAUDE-SESSION]`

Skip this step (mark N/A) without Orca.

**Do:**

1. In a terminal, write a launcher that runs the throwaway `HOME`'s `ccsession-orca` through `c8`:

   ```bash
   printf '#!/bin/bash\nsource /tmp/d08/c8.sh\nc8 /tmp/d08/c-home/.local/bin/ccsession-orca "$@"\n' > /tmp/d08/bin/ccsession-orca-c8
   chmod +x /tmp/d08/bin/ccsession-orca-c8
   ```

   In Orca, open **Settings > Agents > Claude > Command**, write down its current value, and set it to `/tmp/d08/bin/ccsession-orca-c8`.
2. Open `/tmp/d08/c-repo` in Orca (add it as a project or folder) and start Claude with the **+** button.
3. At the question type `d08 orca` and press Enter. Note the tab title.
4. In the session `/rename d08 orca2`, then `Reply with OK. Do not use any tools.`. Note the tab title.
5. `/exit`. Note the tab title.
6. Start Claude with **+** again and press Enter at the question; note the title; `/exit`.

**Expected result:**

- Step 3: the tab shows the saved-session list (`d08 renamed` among them) and `Session name (Enter or Ctrl+C = untagged; untagged after 30s):`; after the answer the session starts with that name and the tab title is `d08 orca · Claude Code` (source: `ccsession-orca:19-28,62-79`; `ccsession:1508-1523`; `CHANGELOG.md:192,198`).
- Step 4: after the reply, the title is `d08 orca2 · Claude Code`. It needs the `orca` command on that tab's `PATH` (source: `ccsession:479-491`; `hooks/session-name.sh:185-192`; `CHANGELOG.md:62`).
- Step 5: the `d08 orca2 · Claude Code` title is taken off, unless you typed a title of your own into Orca since (source: `ccsession:493-508`; `hooks/session-name.sh:193-197`). UNVERIFIED: which title Orca shows then.
- Step 6: an untagged session titled `Claude Code` (source: `ccsession:1521,1543-1544`; `ccsession-orca:81`).
- UNVERIFIED, not checked while this guide was written: whether the `orca` command still reaches Orca when `c8` sets `HOME` and unsets the `XDG_*` folders. ccsession runs `orca terminal rename` and `orca terminal show` for the Step 4 and Step 5 titles (`ccsession:479-508`). If those two titles do not change, write that down as a remark about this test setup, not as a ccsession FAIL. Orca's own files, outside `~/.claude`, are Orca's and are not part of this check.

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

---

## Edge cases (optional but recommended)

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[LOCAL-WRITE]` `d8 ccsession --name; echo "exit=$?"` | `ccsession: --name requires a value`, `exit=2` | `ccsession:563-567` | ☐ |
| `[LOCAL-WRITE]` `d8 ccsession x --tier 1a; echo "exit=$?"` (no `D8_DEFAULTS`) | `ccsession: --tier needs tier settings (T<N>_WINDOW) from the workspace env; none found`, `exit=2` | `ccsession:693-695` | ☐ |
| `[LOCAL-WRITE]` `D8_DEFAULTS=/tmp/d08/defaults.sh d8 ccsession x --profile gpt; echo "exit=$?"` | `ccsession: --profile is not used in this workspace; choose --tier <tier> or --model <name> (see ccsession --help)`, `exit=2` | `ccsession:67,687-691` | ☐ |
| `[LOCAL-WRITE]` `D8_DEFAULTS=/tmp/d08/defaults.sh d8 ccsession x --tier x; echo "exit=$?"` | `ccsession: unknown tier 'x' (use tier0, tier1a, ... or 0, 1a, ...)`, `exit=2` | `models.py:489-496,843-849` | ☐ |
| `[LOCAL-WRITE]` `D8_DEFAULTS=/tmp/d08/defaults.sh d8 ccsession x --model some-other-model 2>&1 \| grep WARNING \| head -n 1` | `[ccsession] WARNING: some-other-model is not in any tier; using a 200000 token window` | `models.py:730-732,904-908` | ☐ |
| `[LOCAL-WRITE]` `D8_DEFAULTS=/tmp/d08/defaults.sh D8_EXTRA=CCSESSION_SHOW_ALL_MODELS=1 d8 ccsession x --tier 2 2>&1 \| grep shim` | Both earlier test shims are left running and a third starts on `127.0.0.1:5092`: show-all gets a shim of its own, so other sessions' `/model` lists never change. It is a plain setting, not an admin gate | `ccsession:65-66,773-813`; `models.py:735-745` | ☐ |
| `[LOCAL-WRITE]` `typed ahead`: `(sleep 1; d8 ccsession --ask; echo "exit=$?")` and press a key during the first second | The question is not asked, `exit=1`: keys already waiting are left to whatever runs next | `ccsession:1330-1344` | ☐ |

## Cleanup

First, in Orca, set **Settings > Agents > Claude > Command** back to the value you wrote down in Step 17. Then stop only this guide's test shims, by their `/tmp/d08/` path (Tier B's under `/tmp/d08/home/`, Tier C's under `/tmp/d08/c-home/`), never with a bare `pkill -f local-gateway-alias-proxy.py`:

```bash
pkill -f '^python3 /tmp/d08/'; sleep 1
pgrep -af '^python3 /tmp/d08/' || echo "no test shim left"
cd /tmp && rm -rf /tmp/d08
```

The second command must print `no test shim left`: a shim runs as `python3 <its script>`, and the test shims' scripts are the copies under `/tmp/d08` (source: `ccsession:97,812`). The last command removes both throwaway `HOME`s with the Tier C session names and history, the stand-in, the helpers and both scratch repos.

Tiers B and C leave nothing in your real `HOME`: they read your installed skill and your `~/.claude/ccsession.env` and write only under `/tmp/d08`. Your own shims and sessions were not touched.

## Overall result

☐ **PASS** — capability works as documented for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `5.0.0 (tag v5.0.0, commit d953b983)`
