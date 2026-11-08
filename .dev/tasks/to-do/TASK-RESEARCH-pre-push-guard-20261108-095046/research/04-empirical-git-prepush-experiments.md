# Research: Empirical real-git pre-push experiments
SANDBOX_PATH: /tmp/prepush-research.ERbSguv9
**Investigation type:** Code Tracer (empirical tester)
**Scope:** installed git (version as measured) in a mktemp -d sandbox under /tmp
**Status:** Complete
**Date:** 2026-11-08
---

## E0. Environment, sandbox and setup

Sandbox created with `SANDBOX=$(mktemp -d /tmp/prepush-research.XXXXXXXX); echo "$SANDBOX"` which printed `/tmp/prepush-research.ERbSguv9`. Below, `S=/tmp/prepush-research.ERbSguv9`. Every Bash call began with `export HOME=$S/home GIT_CONFIG_NOSYSTEM=1`; every git command used `-C` inside `$S` and `timeout 20`.

**Ambient environment note (observed in the calling shell before any experiment):** the agent shell already carries `GIT_ASKPASS=`, `GIT_CONFIG_COUNT=2`, `GIT_CONFIG_KEY_0=credential.interactive`, `GIT_CONFIG_VALUE_0=false`, `GIT_CONFIG_KEY_1=credential.guiPrompt`, `GIT_CONFIG_VALUE_1=false`, `GIT_EDITOR=true`, `GIT_TERMINAL_PROMPT=0`, and the variables `CLAUDECODE` and `CCSESSION_LAUNCH_ID` are set. These were deliberately left in place (they are what a governed agent's push really inherits); they add only `credential.*` config ("command line:" origin in `git config --show-origin --list`), no `core.hooksPath`.

Command block (setup):
```bash
S=/tmp/prepush-research.ERbSguv9; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1
set -u
mkdir -p $S/home $S/home2 $S/bin $S/otherhooks && chmod +x $S/x.sh $S/hook-logging.sh
echo "## git --version"; timeout 20 git --version
timeout 20 git -c init.defaultBranch=main init --bare $S/remote.git
timeout 20 git clone $S/remote.git $S/clone 2>&1
timeout 20 git -C $S/clone config user.name "Research Bot"
timeout 20 git -C $S/clone config user.email "research@example.invalid"
timeout 20 git -C $S/clone switch -c main 2>&1
echo one > $S/clone/f.txt; timeout 20 git -C $S/clone add f.txt; timeout 20 git -C $S/clone commit -q -m "initial"
echo "## remote -v before first push"; timeout 20 git -C $S/clone remote -v
timeout 20 git -C $S/clone push origin main 2>&1
timeout 20 git -C $S/clone branch dev; timeout 20 git -C $S/clone push origin dev 2>&1
timeout 20 git -C $S/clone tag v1
timeout 20 git -C $S/clone worktree add $S/wt -b feature 2>&1
echo "## git dirs"; timeout 20 git -C $S/wt rev-parse --git-dir --git-common-dir
cp $S/hook-logging.sh $S/clone/.git/hooks/pre-push && chmod +x $S/clone/.git/hooks/pre-push
ls -l $S/clone/.git/hooks/pre-push
echo "## config (local, global)"; timeout 20 git -C $S/wt config --show-origin --list | grep -v '^file:.git/config\s*core\.' ; ls -a $S/home
echo "## remote refs"; timeout 20 git -C $S/remote.git for-each-ref --format='%(refname) %(objectname)'
```
Output (verbatim):
```text
## git --version
git version 2.47.3
Initialized empty Git repository in /tmp/prepush-research.ERbSguv9/remote.git/
Cloning into '/tmp/prepush-research.ERbSguv9/clone'...
warning: You appear to have cloned an empty repository.
done.
Switched to a new branch 'main'
## remote -v before first push
origin	/tmp/prepush-research.ERbSguv9/remote.git (fetch)
origin	/tmp/prepush-research.ERbSguv9/remote.git (push)
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      main -> main
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      dev -> dev
Preparing worktree (new branch 'feature')
HEAD is now at b833169 initial
## git dirs
/tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt
/tmp/prepush-research.ERbSguv9/clone/.git
-rwxr-xr-x 1 coder coder 1463 Nov  8 11:12 /tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
## config (local, global)
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	core.repositoryformatversion=0
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	core.filemode=true
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	core.bare=false
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	core.logallrefupdates=true
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	remote.origin.url=/tmp/prepush-research.ERbSguv9/remote.git
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	branch.main.remote=origin
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	branch.main.merge=refs/heads/main
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	user.name=Research Bot
file:/tmp/prepush-research.ERbSguv9/clone/.git/config	user.email=research@example.invalid
command line:	credential.interactive=false
command line:	credential.guiprompt=false
.
..
## remote refs
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
```
Observed: installed git is **2.47.3**; the only remote URL is the local bare path; `$S/home` is empty (no global config); the linked worktree's git dir is `clone/.git/worktrees/wt` and its common dir is `clone/.git`. The hook was installed (mode 755) only at the common dir `clone/.git/hooks/pre-push` and was not present for the setup pushes.

### Hook and runner used by every experiment

`$S/hook-logging.sh` (copied to each hook location; exit status read from `$S/hook-exit`, default 0):
```bash
#!/bin/bash
# Logging pre-push hook for research. Appends to the sandbox log; exit code from $S/hook-exit (default 0).
S=/tmp/prepush-research.ERbSguv9
LOG=$S/hook.log
{
  echo "=== HOOK-RUN file=$0"
  echo "argv0=$0"
  echo "argv1=$1"
  echo "argv2=$2"
  n=0
  while IFS= read -r line; do echo "STDIN: $line"; n=$((n+1)); done
  [ "$n" -eq 0 ] && echo "EMPTY-STDIN"
  echo "pwd=$(pwd)"
  echo "--- GIT_* env"
  env | grep ^GIT_ | sort
  echo "HOME=${HOME-<UNSET>}"
  echo "PATH=$PATH"
  echo "uv=$(command -v uv || echo UV-ABSENT)"
  echo "PREPUSH_MARKER=${PREPUSH_MARKER-<UNSET>}"
  echo "--- non-GIT env names"
  env | cut -d= -f1 | grep -v ^GIT_ | sort | tr '\n' ' '; echo
  echo "CCSESSION_LAUNCH_ID present: $([ -n "${CCSESSION_LAUNCH_ID+x}" ] && echo yes || echo no)"
  echo "CLAUDECODE present: $([ -n "${CLAUDECODE+x}" ] && echo yes || echo no)"
  echo "--- self/parent/grandparent (pid ppid sid comm)"
  ps -o pid=,ppid=,sid=,comm= -p $$
  ps -o pid=,ppid=,sid=,comm= -p $PPID
  GP=$(ps -o ppid= -p $PPID | tr -d ' ')
  ps -o pid=,ppid=,sid=,comm= -p "$GP"
  echo "--- ancestor chain (pid ppid sid comm), max 10"
  p=$$; i=0
  while [ -n "$p" ] && [ "$p" -gt 1 ] && [ $i -lt 10 ]; do
    ps -o pid=,ppid=,sid=,comm= -p "$p"
    p=$(ps -o ppid= -p "$p" | tr -d ' '); i=$((i+1))
  done
  echo "=== END"
} >> "$LOG" 2>&1
code=$(cat "$S/hook-exit" 2>/dev/null || echo 0)
[ "$code" != 0 ] && echo "HOOK: refusing push (research exit $code)" >&2
exit "$code"
```
(The ancestor chain is printed with `ps -o pid=,ppid=,sid=,comm= -p` per ancestor, a bounded walk of at most 10 levels, instead of `ps -H`, so only the hook's ancestors appear.)

`$S/x.sh` (runner: clears the log, captures remote refs before/after, runs the command with `timeout 20`, bounds output to 60 lines; `brief` mode shows only the `HOOK-RUN`, argv, STDIN, EMPTY-STDIN and pwd lines of the log, `full` mode shows the first 80 log lines):
```bash
#!/bin/bash
# Experiment runner. usage: x.sh <bare-remote> <brief|full> <command...>
S=/tmp/prepush-research.ERbSguv9
R=$1; shift; MODE=$1; shift
: > "$S/hook.log"
timeout 20 git -C "$R" for-each-ref --format='%(refname) %(objectname)' > "$S/refs-before"
echo "## remote refs before ($R)"; cat "$S/refs-before"
echo "## command: $*"
timeout 20 "$@" > "$S/out" 2>&1; rc=$?
lines=$(wc -l < "$S/out"); head -60 "$S/out"; [ "$lines" -gt 60 ] && echo "[TRUNCATED: $lines lines total, first 60 shown]"
echo "## exit=$rc"
timeout 20 git -C "$R" for-each-ref --format='%(refname) %(objectname)' > "$S/refs-after"
echo "## remote refs after"; cat "$S/refs-after"
if cmp -s "$S/refs-before" "$S/refs-after"; then echo "## REMOTE-REFS-CHANGED: no"; else echo "## REMOTE-REFS-CHANGED: yes"; diff "$S/refs-before" "$S/refs-after"; fi
echo "## hook log"
if [ ! -s "$S/hook.log" ]; then echo "HOOK-NOT-RUN (log empty)"
elif [ "$MODE" = full ]; then head -80 "$S/hook.log"
else grep -E '^(=== HOOK|argv|STDIN|EMPTY-STDIN|pwd=)' "$S/hook.log" | head -60; fi
```
In each experiment below, `X=$S/x.sh` and `R=$S/remote.git` unless stated.

## E1. Create a new branch (from the linked worktree), full hook log

Command block:
```bash
S=/tmp/prepush-research.ERbSguv9; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1; X=$S/x.sh; R=$S/remote.git
echo two > $S/wt/g.txt; timeout 20 git -C $S/wt add g.txt; timeout 20 git -C $S/wt commit -q -m "feature commit"; timeout 20 git -C $S/wt rev-parse HEAD
$X $R full git -C $S/wt push origin feature
```
Output and hook log (verbatim; the single-line non-GIT name list is reproduced in full, names only):
```text
afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> feature
## exit=0
## remote refs after
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: yes
1a2
> refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3 refs/heads/feature 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
--- GIT_* env
GIT_ASKPASS=
GIT_CONFIG_COUNT=2
GIT_CONFIG_KEY_0=credential.interactive
GIT_CONFIG_KEY_1=credential.guiPrompt
GIT_CONFIG_NOSYSTEM=1
GIT_CONFIG_VALUE_0=false
GIT_CONFIG_VALUE_1=false
GIT_DIR=/tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt
GIT_EDITOR=true
GIT_EXEC_PATH=/usr/lib/git-core
GIT_PREFIX=
GIT_TERMINAL_PROMPT=0
HOME=/tmp/prepush-research.ERbSguv9/home
PATH=/usr/lib/git-core:/home/coder/.config/orca/linux-orca-cli-shim:/home/coder/.local/bin:/usr/local/bin:/opt/nvm/versions/node/v24.22.2/bin:/home/coder/.local/bin:/home/coder/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
uv=/usr/local/bin/uv
PREPUSH_MARKER=<UNSET>
--- non-GIT env names
AIDEV_HEARTBEAT_URL AIDEV_ORCA_NATIVE_ENDPOINT_FILE AIDEV_ORCA_OWNER AI_AGENT ANSI_ACCENT_PRIMARY ANSI_ACCENT_SECONDARY ANSI_ERROR ANSI_FG_DEFAULT ANSI_FG_DIM ANSI_FG_EMPHASIS ANSI_RESET ANSI_SUCCESS ANSI_WARNING ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL ANTHROPIC_DEFAULT_HAIKU_MODEL ANTHROPIC_DEFAULT_OPUS_MODEL ANTHROPIC_DEFAULT_SONNET_MODEL ANTHROPIC_MODEL BROWSER CCSESSION_ACCESS CCSESSION_DEFAULT_TIER CCSESSION_GATEWAY_URL CCSESSION_LAUNCH_CWD CCSESSION_LAUNCH_ID CCSESSION_MODEL_ORDER CCSESSION_PROFILE CCSESSION_SHIM_URL CCSESSION_TIER_RULES CCSESSION_TOPIC_CWD CHROME_DESKTOP CLAUDECODE CLAUDE_CODE_CHILD_SESSION CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS CLAUDE_CODE_DISABLE_TERMINAL_TITLE CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY CLAUDE_CODE_ENABLE_TELEMETRY CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_EXECPATH CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS CLAUDE_CODE_FORCE_TERMINAL_IMAGES CLAUDE_CODE_MAX_CONTEXT_TOKENS CLAUDE_CODE_MAX_OUTPUT_TOKENS CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION CLAUDE_CODE_MESSAGING_SOCKET CLAUDE_CODE_MESSAGING_TOKEN CLAUDE_CODE_PLUGIN_DIRS CLAUDE_CODE_SESSION_ATTENDED CLAUDE_CODE_SESSION_ID CLAUDE_EFFORT CLAUDE_PID CLAUDE_TOPIC CODER_WORKSPACE_OWNER_NAME CODER_WORKSPACE_OWNER_ROLES COLORTERM COREPACK_ENABLE_AUTO_PIN DISABLE_AUTOUPDATER DISPLAY FC_FONTATIONS FORCE_HYPERLINK GCM_INTERACTIVE GEMINI_API_KEY GOOGLE_API_KEY GOOGLE_GEMINI_BASE_URL HISTFILE HOME JCODE_RUNTIME_DIR LANG LIBGL_ALWAYS_SOFTWARE LITELLM_API_KEY LOGNAME NO_AT_BRIDGE NVM_BIN NVM_CD_FLAGS NVM_INC NoDefaultCurrentDirectoryInExePath OPENAI_API_BASE OPENAI_API_KEY OPENAI_BASE_URL OPENAI_HOST ORCA_AGENT_HOOK_ENDPOINT ORCA_AGENT_HOOK_ENV ORCA_AGENT_HOOK_OPENCODE_TUI ORCA_AGENT_HOOK_PORT ORCA_AGENT_HOOK_TOKEN ORCA_AGENT_HOOK_TRANSPORT ORCA_AGENT_HOOK_VERSION ORCA_AGENT_LAUNCH ORCA_AGENT_LAUNCH_TOKEN ORCA_AGENT_PANE ORCA_APP_VERSION ORCA_CLAUDE_AGENT_VIEW_PLUGIN_DIR ORCA_CLAUDE_CONFIG_DIR ORCA_CLAUDE_PROFILE_POINTER ORCA_CLI_BIN_DIR ORCA_HISTFILE ORCA_IMAGE_PROTOCOL ORCA_NODE_OPTIONS ORCA_NODE_REPL_EXTERNAL_MODULE ORCA_OPENCODE_AGENT ORCA_PANE_KEY ORCA_PI_SOURCE_AGENT_DIR ORCA_REMOTE_VIEWER_CLIPBOARD ORCA_RUNTIME_SOURCE_ID ORCA_RUNTIME_SOURCE_INCARNATION ORCA_RUNTIME_SOURCE_PROFILE_PATH ORCA_SERVE_RUNTIME ORCA_TAB_ID ORCA_TERMINAL_HANDLE ORCA_USER_DATA_PATH ORCA_WORKSPACE_ID ORCA_WORKTREE_ID ORCA_WSL_HOSTS_GATE_STATE OSH PATH PI_CLIPBOARD_OSC52 PONYTAIL_DEFAULT_MODE POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD PWD SBX_CHROME_API_RQ SHELL SHLVL SSH_ASKPASS STARSHIP_CONFIG STARSHIP_SESSION_KEY STARSHIP_SHELL T0Model01 T0Model01_WINDOW T0Model02 T0Model02_WINDOW T0ProxyUrl T0_WINDOW T1Model01 T1Model01_WINDOW T1Model02 T1Model02_WINDOW T1Model03 T1Model03_WINDOW T1Model04 T1Model04_WINDOW T1ProxyUrl T1_WINDOW T1aModel01 T1aModel01_WINDOW T1aModel02 T1aModel02_WINDOW T1a_WINDOW T1bModel01 T1bModel01_WINDOW T1bModel02 T1bModel02_WINDOW T1bModel03 T1bModel03_WINDOW T1b_WINDOW T2Model01 T2Model01_WINDOW T2Model02 T2Model02_WINDOW T2Model03 T2Model03_WINDOW T2Model04 T2Model04_WINDOW T2Model05 T2Model05_WINDOW T2Model06 T2Model06_WINDOW T2ProxyUrl T2_WINDOW T3Model01 T3Model01_WINDOW T3Model02 T3Model02_WINDOW T3Model03 T3Model03_WINDOW T3Model04 T3Model04_WINDOW T3Model05 T3Model05_WINDOW T3Model06 T3Model06_WINDOW T3ProxyUrl T3_WINDOW T4Model01 T4Model01_WINDOW T4_WINDOW TERM TERM_PROGRAM TERM_PROGRAM_VERSION USER WIDTH_DEFAULT WIDTH_MAX WIDTH_NARROW _ deepseek glm kimi qwen 
CCSESSION_LAUNCH_ID present: yes
CLAUDECODE present: yes
--- self/parent/grandparent (pid ppid sid comm)
 303587  303584  303569 pre-push
 303584  303583  303569 git
 303583  303579  303569 timeout
--- ancestor chain (pid ppid sid comm), max 10
 303587  303584  303569 pre-push
 303584  303583  303569 git
 303583  303579  303569 timeout
 303579  303569  303569 x.sh
 303569 3625302  303569 bash
3625302 3624918 3624918 claude
3624918    1174 3624918 bash
   1174     457    1174 orca-ide
    457     377     377 orca-ide
    377       1     377 orca-ide
=== END
```
Observed: hook ran once from the **common** dir `clone/.git/hooks/pre-push`; argv1 = remote name `origin`, argv2 = URL as configured; one stdin record `<local-ref> <local-oid> <remote-ref> <40-zero remote-oid>` for a create; cwd = worktree top level; git exports `GIT_DIR` = the worktree-private git dir, `GIT_EXEC_PATH`, empty `GIT_PREFIX`, and prepends `/usr/lib/git-core` to PATH; all ambient variables (including `CLAUDECODE`, `CCSESSION_LAUNCH_ID`, `CLAUDE_PID`, `CLAUDE_CODE_SESSION_ID`, `ORCA_*`) pass through; the hook's session id equals that of the Bash tool shell (303569), whose parent is the `claude` process (3625302) in a different session (3624918). Remote gained `refs/heads/feature`.

## E2. Fast-forward update of main (`feature:main`)

Command block (prefix lines as in E1 omitted below: `S=/tmp/prepush-research.ERbSguv9; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1; X=$S/x.sh; R=$S/remote.git`):
```bash
$X $R brief git -C $S/wt push origin feature:main
```
Output (verbatim):
```text
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature:main
To /tmp/prepush-research.ERbSguv9/remote.git
   b833169..afa71f1  feature -> main
## exit=0
## remote refs after
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## REMOTE-REFS-CHANGED: yes
3c3
< refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
---
> refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3 refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: field 3 is the fully qualified `refs/heads/main` even though the command said only `main`; field 4 is the remote's old oid; remote main moved b833169 -> afa71f1.

## E3a. Delete a disposable branch with `:dev`

Command block:
```bash
$X $R brief git -C $S/wt push origin :dev
```
Output (verbatim):
```text
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin :dev
To /tmp/prepush-research.ERbSguv9/remote.git
 - [deleted]         dev
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## REMOTE-REFS-CHANGED: yes
1d0
< refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: (delete) 0000000000000000000000000000000000000000 refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: a delete record is `(delete) <zero-oid> <remote-ref> <remote-old-oid>`; field 1 is the literal string `(delete)`.

## E3b. Delete main with `:main` (remote HEAD points at main)

Command block:
```bash
$X $R brief git -C $S/wt push origin :main
```
Output (verbatim):
```text
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin :main
remote: error: By default, deleting the current branch is denied, because the next        
remote: 'git clone' won't result in any file checked out, causing confusion.        
remote: 
remote: You can set 'receive.denyDeleteCurrent' configuration variable to        
remote: 'warn' or 'ignore' in the remote repository to allow deleting the        
remote: current branch, with or without a warning message.        
remote: 
remote: To squelch this message, you can set it to 'refuse'.        
remote: error: refusing to delete the current branch: refs/heads/main        
To /tmp/prepush-research.ERbSguv9/remote.git
 ! [remote rejected] main (deletion of the current branch prohibited)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: (delete) 0000000000000000000000000000000000000000 refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: the hook ran and received the delete record for `refs/heads/main` **before** the remote refused it; the refusal came from the bare remote's `receive.denyDeleteCurrent` default (main is the bare repo's HEAD), not from the hook. Remote refs unchanged. E4b repeats the main deletion with the remote HEAD moved so the delete is actually accepted.

## E4a/E4b. Delete with `--delete` (disposable branch, then main)

Command block:
```bash
echo "######## setup: create disposable tmp1"; timeout 20 git -C $S/wt push -q origin feature:refs/heads/tmp1 2>&1
echo "######## E4a --delete tmp1"; $X $R brief git -C $S/wt push origin --delete tmp1
echo "######## setup: move bare HEAD to feature"; timeout 20 git -C $R symbolic-ref HEAD refs/heads/feature; timeout 20 git -C $R symbolic-ref HEAD
echo "######## E4b --delete main"; $X $R brief git -C $S/wt push origin --delete main
echo "######## restore: recreate main, bare HEAD back to main"; timeout 20 git -C $S/wt push -q origin feature:refs/heads/main 2>&1; timeout 20 git -C $R symbolic-ref HEAD refs/heads/main; timeout 20 git -C $R symbolic-ref HEAD; timeout 20 git -C $R for-each-ref --format='%(refname) %(objectname)'
```
Output (verbatim):
```text
######## setup: create disposable tmp1
######## E4a --delete tmp1
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/tmp1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin --delete tmp1
To /tmp/prepush-research.ERbSguv9/remote.git
 - [deleted]         tmp1
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## REMOTE-REFS-CHANGED: yes
3d2
< refs/heads/tmp1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: (delete) 0000000000000000000000000000000000000000 refs/heads/tmp1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
pwd=/tmp/prepush-research.ERbSguv9/wt
######## setup: move bare HEAD to feature
refs/heads/feature
######## E4b --delete main
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin --delete main
To /tmp/prepush-research.ERbSguv9/remote.git
 - [deleted]         main
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## REMOTE-REFS-CHANGED: yes
2d1
< refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: (delete) 0000000000000000000000000000000000000000 refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
pwd=/tmp/prepush-research.ERbSguv9/wt
######## restore: recreate main, bare HEAD back to main
refs/heads/main
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
```
Observed: `--delete <name>` produces the same record shape as `:<name>` (`(delete) <zero> refs/heads/<name> <old>`); the short name is expanded to `refs/heads/...` in field 3. With the bare HEAD moved off main, deleting `refs/heads/main` succeeded when the hook exited 0, so a guard is the only local layer that would stop it. The setup and restore pushes also invoked the hook (their log entries were cleared by the next runner call).

## E5a/E5b. Forced updates of main (`+alt:main` and `--force feature:main`)

Command block:
```bash
echo "######## setup: diverged branch alt from initial commit"; timeout 20 git -C $S/wt branch alt b833169; echo alt > $S/alt.txt; ALT_TREE=$(timeout 20 git -C $S/wt rev-parse b833169^{tree}); ALT=$(timeout 20 git -C $S/wt commit-tree -p b833169 -m "alt commit" $ALT_TREE); timeout 20 git -C $S/wt update-ref refs/heads/alt $ALT; timeout 20 git -C $S/wt rev-parse alt
echo "######## E5a +alt:main"; $X $R brief git -C $S/wt push origin +alt:main
echo "######## E5b --force feature:main"; $X $R brief git -C $S/wt push --force origin feature:main
```
Output (verbatim):
```text
######## setup: diverged branch alt from initial commit
404f82e243b3a0abf5de608f63589bca41ecd492
######## E5a +alt:main
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin +alt:main
To /tmp/prepush-research.ERbSguv9/remote.git
 + afa71f1...404f82e alt -> main (forced update)
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main 404f82e243b3a0abf5de608f63589bca41ecd492
## REMOTE-REFS-CHANGED: yes
2c2
< refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
---
> refs/heads/main 404f82e243b3a0abf5de608f63589bca41ecd492
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E5b --force feature:main
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main 404f82e243b3a0abf5de608f63589bca41ecd492
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --force origin feature:main
To /tmp/prepush-research.ERbSguv9/remote.git
 + 404f82e...afa71f1 feature -> main (forced update)
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## REMOTE-REFS-CHANGED: yes
2c2
< refs/heads/main 404f82e243b3a0abf5de608f63589bca41ecd492
---
> refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3 refs/heads/main 404f82e243b3a0abf5de608f63589bca41ecd492
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: forced updates (both spellings) reach the hook with an ordinary four-field record; the stdin record carries **no force marker** (the `+` is not in field 1 or 3). Field 3 is `refs/heads/main` in both forms.

## E7. Multiple refspecs in one push; E6. `HEAD:main`; E8. Mixed update plus delete

Command block (run in this order):
```bash
echo "######## E7 multiple refspecs"; $X $R brief git -C $S/wt push origin feature:refs/heads/side1 alt:refs/heads/side2
echo "######## setup: new commit on feature in wt"; echo three > $S/wt/h.txt; timeout 20 git -C $S/wt add h.txt; timeout 20 git -C $S/wt commit -q -m "feature commit 2"; timeout 20 git -C $S/wt rev-parse HEAD
echo "######## E6 HEAD:main"; $X $R brief git -C $S/wt push origin HEAD:main
echo "######## E8 mixed update + delete"; $X $R brief git -C $S/wt push origin feature:refs/heads/side1 :side2
```
Output (verbatim):
```text
######## E7 multiple refspecs
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature:refs/heads/side1 alt:refs/heads/side2
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> side1
 * [new branch]      alt -> side2
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/side1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/side2 404f82e243b3a0abf5de608f63589bca41ecd492
## REMOTE-REFS-CHANGED: yes
2a3,4
> refs/heads/side1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
> refs/heads/side2 404f82e243b3a0abf5de608f63589bca41ecd492
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3 refs/heads/side1 0000000000000000000000000000000000000000
STDIN: refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/heads/side2 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## setup: new commit on feature in wt
9a841ac686f348afa68a2158ee64c14260a84df2
######## E6 HEAD:main
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/side1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/side2 404f82e243b3a0abf5de608f63589bca41ecd492
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin HEAD:main
To /tmp/prepush-research.ERbSguv9/remote.git
   afa71f1..9a841ac  HEAD -> main
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/side2 404f82e243b3a0abf5de608f63589bca41ecd492
## REMOTE-REFS-CHANGED: yes
2c2
< refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
---
> refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: HEAD 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/main afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E8 mixed update + delete
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/side2 404f82e243b3a0abf5de608f63589bca41ecd492
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature:refs/heads/side1 :side2
To /tmp/prepush-research.ERbSguv9/remote.git
   afa71f1..9a841ac  feature -> side1
 - [deleted]         side2
## exit=0
## remote refs after
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
## REMOTE-REFS-CHANGED: yes
3,4c3
< refs/heads/side1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
< refs/heads/side2 404f82e243b3a0abf5de608f63589bca41ecd492
---
> refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/side1 afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
STDIN: (delete) 0000000000000000000000000000000000000000 refs/heads/side2 404f82e243b3a0abf5de608f63589bca41ecd492
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: one hook invocation per push, one stdin line per ref update, in command-line order here. For `HEAD:main`, **field 1 is the literal source expression `HEAD`**, not `refs/heads/feature`, so field 1 is not always a full ref name; field 3 is still `refs/heads/main`. A mixed push delivers update and delete records in the same stream.

## E9. `--all`; E10. `--tags`; E11. `--mirror` to a second bare remote

Command block:
```bash
echo "## local branches"; timeout 20 git -C $S/wt for-each-ref --format='%(refname) %(objectname)' refs/heads refs/tags
echo "######## E9 --all"; $X $R brief git -C $S/wt push --all origin
echo "######## E10 --tags"; $X $R brief git -C $S/wt push --tags origin
echo "######## setup: second bare remote"; timeout 20 git -c init.defaultBranch=main init --bare $S/remote2.git
echo "######## E11 --mirror to remote2"; $X $S/remote2.git brief git -C $S/wt push --mirror $S/remote2.git
echo "## first remote untouched?"; timeout 20 git -C $R for-each-ref --format='%(refname) %(objectname)'
```
Output (verbatim):
```text
## local branches
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
######## E9 --all
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --all origin
To /tmp/prepush-research.ERbSguv9/remote.git
   afa71f1..9a841ac  feature -> feature
 * [new branch]      alt -> alt
 * [new branch]      dev -> dev
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
hint: Updates were rejected because a pushed branch tip is behind its remote
hint: counterpart. If you want to integrate the remote changes, use 'git pull'
hint: before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
## exit=1
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
## REMOTE-REFS-CHANGED: yes
1c1,3
< refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
---
> refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
> refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
> refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/feature afa71f1a6d85ee82d3186fac8649d1cb8cb298b3
STDIN: refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/heads/alt 0000000000000000000000000000000000000000
STDIN: refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be refs/heads/dev 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E10 --tags
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --tags origin
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new tag]         v1 -> v1
## exit=0
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: yes
5a6
> refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be refs/tags/v1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## setup: second bare remote
Initialized empty Git repository in /tmp/prepush-research.ERbSguv9/remote2.git/
######## E11 --mirror to remote2
## remote refs before (/tmp/prepush-research.ERbSguv9/remote2.git)
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --mirror /tmp/prepush-research.ERbSguv9/remote2.git
To /tmp/prepush-research.ERbSguv9/remote2.git
 * [new branch]      alt -> alt
 * [new branch]      dev -> dev
 * [new branch]      feature -> feature
 * [new branch]      main -> main
 * [new reference]   origin/alt -> origin/alt
 * [new reference]   origin/dev -> origin/dev
 * [new reference]   origin/feature -> origin/feature
 * [new reference]   origin/main -> origin/main
 * [new reference]   origin/side1 -> origin/side1
 * [new tag]         v1 -> v1
## exit=0
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
refs/remotes/origin/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/remotes/origin/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/remotes/origin/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/remotes/origin/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/remotes/origin/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: yes
0a1,10
> refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
> refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
> refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
> refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be
> refs/remotes/origin/alt 404f82e243b3a0abf5de608f63589bca41ecd492
> refs/remotes/origin/dev b833169ed442f5722e4e47d5ded81c5d95f399be
> refs/remotes/origin/feature 9a841ac686f348afa68a2158ee64c14260a84df2
> refs/remotes/origin/main 9a841ac686f348afa68a2158ee64c14260a84df2
> refs/remotes/origin/side1 9a841ac686f348afa68a2158ee64c14260a84df2
> refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=/tmp/prepush-research.ERbSguv9/remote2.git
argv2=/tmp/prepush-research.ERbSguv9/remote2.git
STDIN: refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/heads/alt 0000000000000000000000000000000000000000
STDIN: refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be refs/heads/dev 0000000000000000000000000000000000000000
STDIN: refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/feature 0000000000000000000000000000000000000000
STDIN: refs/heads/main b833169ed442f5722e4e47d5ded81c5d95f399be refs/heads/main 0000000000000000000000000000000000000000
STDIN: refs/remotes/origin/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/remotes/origin/alt 0000000000000000000000000000000000000000
STDIN: refs/remotes/origin/dev b833169ed442f5722e4e47d5ded81c5d95f399be refs/remotes/origin/dev 0000000000000000000000000000000000000000
STDIN: refs/remotes/origin/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/remotes/origin/feature 0000000000000000000000000000000000000000
STDIN: refs/remotes/origin/main 9a841ac686f348afa68a2158ee64c14260a84df2 refs/remotes/origin/main 0000000000000000000000000000000000000000
STDIN: refs/remotes/origin/side1 9a841ac686f348afa68a2158ee64c14260a84df2 refs/remotes/origin/side1 0000000000000000000000000000000000000000
STDIN: refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be refs/tags/v1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
## first remote untouched?
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
```
Observed:
- `--all`: the local main (b833169) is behind the remote main, so git rejected `main -> main` as non-fast-forward **before** the hook and **omitted its record** from stdin; the hook saw only the three accepted updates. Record order (`feature`, `alt`, `dev`) was neither alphabetical nor local-ref order, so a guard must not depend on order.
- `--tags`: one record per tag with field 3 `refs/tags/v1`.
- `--mirror` to a URL with no remote name: **argv1 is the URL itself** (same as argv2). The stream contained `refs/heads/main` (a create to the empty mirror) plus `refs/remotes/origin/main`; only the former has field 3 equal to `refs/heads/main`. The first remote was unchanged.

## E12. Up-to-date push; E13. `--dry-run`; E14. `--no-verify`

Command block:
```bash
echo "######## E12 up-to-date"; $X $R brief git -C $S/wt push origin feature
echo "######## E12b up-to-date main (HEAD:main, HEAD==remote main)"; $X $R brief git -C $S/wt push origin HEAD:main
echo "######## E13 --dry-run create"; $X $R brief git -C $S/wt push --dry-run origin feature:refs/heads/dry1
echo "######## E13b --dry-run to main (force)"; $X $R brief git -C $S/wt push --dry-run origin +alt:main
echo "######## E14 --no-verify"; $X $R brief git -C $S/wt push --no-verify origin feature:refs/heads/nv1
```
Output (verbatim; the identical six-line "remote refs before" block of E12b, E13, E13b and E14 is reproduced once per experiment as printed):
```text
######## E12 up-to-date
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature
Everything up-to-date
## exit=0
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
EMPTY-STDIN
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E12b up-to-date main (HEAD:main, HEAD==remote main)
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin HEAD:main
Everything up-to-date
## exit=0
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
EMPTY-STDIN
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E13 --dry-run create
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --dry-run origin feature:refs/heads/dry1
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> dry1
## exit=0
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/dry1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E13b --dry-run to main (force)
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --dry-run origin +alt:main
To /tmp/prepush-research.ERbSguv9/remote.git
 + 9a841ac...404f82e alt -> main (forced update)
## exit=0
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E14 --no-verify
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --no-verify origin feature:refs/heads/nv1
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> nv1
## exit=0
## remote refs after
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/nv1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## REMOTE-REFS-CHANGED: yes
4a5
> refs/heads/nv1 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
HOOK-NOT-RUN (log empty)
```
Observed:
- Up-to-date push (including an up-to-date `HEAD:main`): **the hook ran with empty stdin** (zero records) and argv was supplied as usual. An "empty stream allows" rule therefore matters in practice. Design statement "Empty stream allows" (line 518) describes a case that real git produces [CODE-VERIFIED as a reachable input].
- `--dry-run`: **the hook ran and received the real would-be records** (including a forced `refs/heads/main` update in E13b) while the remote refs did not change. A dry-run therefore exercises a guard without moving refs. Design line 534 "Q artifacts report local hook invocation" for dry-run [CODE-VERIFIED on git 2.47.3]; "Official Git documents dry-run as not sending updates" is consistent with the unchanged remote [CODE-VERIFIED].
- `--no-verify`: the hook did **not** run and the ref was created. Design line 520 "`--no-verify` ... can bypass local pre-push" [CODE-VERIFIED].

## E15. `-c core.hooksPath=/dev/null`; E16. `-c core.hooksPath=$S/otherhooks` (empty, then with hook)

Command block:
```bash
echo "######## E15 -c core.hooksPath=/dev/null"; $X $R brief git -C $S/wt -c core.hooksPath=/dev/null push origin feature:refs/heads/hp1
echo "######## E16a -c core.hooksPath=otherhooks (empty dir)"; ls -A $S/otherhooks; $X $R brief git -C $S/wt -c core.hooksPath=$S/otherhooks push origin feature:refs/heads/hp2
echo "######## E16b -c core.hooksPath=otherhooks (with hook)"; cp $S/hook-logging.sh $S/otherhooks/pre-push && chmod +x $S/otherhooks/pre-push; $X $R brief git -C $S/wt -c core.hooksPath=$S/otherhooks push origin feature:refs/heads/hp3
```
Output (verbatim, remote-ref listings shortened only by showing the diff lines the runner printed; full before/after listings were printed and are summarized by `REMOTE-REFS-CHANGED` plus the diff):
```text
######## E15 -c core.hooksPath=/dev/null
## command: git -C /tmp/prepush-research.ERbSguv9/wt -c core.hooksPath=/dev/null push origin feature:refs/heads/hp1
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> hp1
## exit=0
## REMOTE-REFS-CHANGED: yes
3a4
> refs/heads/hp1 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
HOOK-NOT-RUN (log empty)
######## E16a -c core.hooksPath=otherhooks (empty dir)
## command: git -C /tmp/prepush-research.ERbSguv9/wt -c core.hooksPath=/tmp/prepush-research.ERbSguv9/otherhooks push origin feature:refs/heads/hp2
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> hp2
## exit=0
## REMOTE-REFS-CHANGED: yes
4a5
> refs/heads/hp2 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
HOOK-NOT-RUN (log empty)
######## E16b -c core.hooksPath=otherhooks (with hook)
## command: git -C /tmp/prepush-research.ERbSguv9/wt -c core.hooksPath=/tmp/prepush-research.ERbSguv9/otherhooks push origin feature:refs/heads/hp3
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> hp3
## exit=0
## REMOTE-REFS-CHANGED: yes
5a6
> refs/heads/hp3 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/otherhooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/otherhooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/hp3 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: a per-process `core.hooksPath` replaces the hook directory entirely; `/dev/null` or a directory without `pre-push` silently runs **no** hook (no warning, push succeeds); a directory with a hook runs **only** that hook (the installed common-dir hook did not run). Design line 520 "per-process hooksPath overrides ... can bypass local pre-push" [CODE-VERIFIED].

## E17. `git send-pack` (as specified, then a succeeding create, then a forced write to main)

Command block:
```bash
echo "######## E17a send-pack main (as specified)"; $X $R brief git -C $S/wt send-pack $S/remote.git main
echo "######## E17b send-pack feature:refs/heads/sp1"; $X $R brief git -C $S/wt send-pack $S/remote.git feature:refs/heads/sp1
echo "######## E17c send-pack --force alt:refs/heads/main (protected ref, no hook?)"; $X $R brief git -C $S/wt send-pack --force $S/remote.git alt:refs/heads/main
echo "######## restore main"; timeout 20 git -C $S/wt push -q --force origin feature:main 2>&1; timeout 20 git -C $R rev-parse refs/heads/main
```
Output (verbatim, ref listings reduced to the runner's change lines):
```text
######## E17a send-pack main (as specified)
## command: git -C /tmp/prepush-research.ERbSguv9/wt send-pack /tmp/prepush-research.ERbSguv9/remote.git main
To /tmp/prepush-research.ERbSguv9/remote.git
 ! [rejected]        main -> main (non-fast-forward)
## exit=255
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
######## E17b send-pack feature:refs/heads/sp1
## command: git -C /tmp/prepush-research.ERbSguv9/wt send-pack /tmp/prepush-research.ERbSguv9/remote.git feature:refs/heads/sp1
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      feature -> sp1
## exit=0
## REMOTE-REFS-CHANGED: yes
9a10
> refs/heads/sp1 9a841ac686f348afa68a2158ee64c14260a84df2
## hook log
HOOK-NOT-RUN (log empty)
######## E17c send-pack --force alt:refs/heads/main (protected ref, no hook?)
## command: git -C /tmp/prepush-research.ERbSguv9/wt send-pack --force /tmp/prepush-research.ERbSguv9/remote.git alt:refs/heads/main
To /tmp/prepush-research.ERbSguv9/remote.git
 + 9a841ac...404f82e alt -> main (forced update)
## exit=0
## REMOTE-REFS-CHANGED: yes
7c7
< refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
---
> refs/heads/main 404f82e243b3a0abf5de608f63589bca41ecd492
## hook log
HOOK-NOT-RUN (log empty)
######## restore main
9a841ac686f348afa68a2158ee64c14260a84df2
```
Observed: `git send-pack` **never runs pre-push**; E17a was rejected as non-fast-forward (local main is behind) without the hook, E17b created a ref and E17c **force-rewrote `refs/heads/main` with no hook invocation**. Design line 520 "direct send-pack ... can bypass local pre-push" [CODE-VERIFIED]. Main was restored to 9a841ac afterwards (the restore push ran the hook; its log was cleared by the next run).

## E18. Push from the main clone compared with the linked worktree

Command block:
```bash
echo "######## E18 push from main clone"; $X $R full git -C $S/clone push origin dev:refs/heads/fromclone > $S/e18.out; grep -vE '^(AIDEV|---|[0-9 ]+ )' $S/e18.out | grep -v '^AIDEV_HEARTBEAT' | head -60; cp $S/hook.log $S/log-clone
echo "######## E18 comparison push from worktree"; $X $R full git -C $S/wt push origin feature:refs/heads/fromwt > /dev/null; cp $S/hook.log $S/log-wt
echo "## diff log-clone log-wt"; diff $S/log-clone $S/log-wt
```
Output (verbatim; the first grep filtered out the long non-GIT name line and ps lines; ref listings reduced to the change lines):
```text
######## E18 push from main clone
## command: git -C /tmp/prepush-research.ERbSguv9/clone push origin dev:refs/heads/fromclone
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      dev -> fromclone
## exit=0
## REMOTE-REFS-CHANGED: yes
3a4
> refs/heads/fromclone b833169ed442f5722e4e47d5ded81c5d95f399be
## hook log
=== HOOK-RUN file=.git/hooks/pre-push
argv0=.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be refs/heads/fromclone 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/clone
GIT_ASKPASS=
GIT_CONFIG_COUNT=2
GIT_CONFIG_KEY_0=credential.interactive
GIT_CONFIG_KEY_1=credential.guiPrompt
GIT_CONFIG_NOSYSTEM=1
GIT_CONFIG_VALUE_0=false
GIT_CONFIG_VALUE_1=false
GIT_EDITOR=true
GIT_EXEC_PATH=/usr/lib/git-core
GIT_PREFIX=
GIT_TERMINAL_PROMPT=0
HOME=/tmp/prepush-research.ERbSguv9/home
PATH=/usr/lib/git-core:/home/coder/.config/orca/linux-orca-cli-shim:/home/coder/.local/bin:/usr/local/bin:/opt/nvm/versions/node/v24.22.2/bin:/home/coder/.local/bin:/home/coder/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
uv=/usr/local/bin/uv
PREPUSH_MARKER=<UNSET>
CCSESSION_LAUNCH_ID present: yes
CLAUDECODE present: yes
=== END
######## E18 comparison push from worktree
## diff log-clone log-wt
1,2c1,2
< === HOOK-RUN file=.git/hooks/pre-push
< argv0=.git/hooks/pre-push
---
> === HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
> argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
5,6c5,6
< STDIN: refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be refs/heads/fromclone 0000000000000000000000000000000000000000
< pwd=/tmp/prepush-research.ERbSguv9/clone
---
> STDIN: refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/fromwt 0000000000000000000000000000000000000000
> pwd=/tmp/prepush-research.ERbSguv9/wt
14a15
> GIT_DIR=/tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt
28,30c29,31
<  332078  332075  331965 pre-push
<  332075  332074  331965 git
<  332074  332070  331965 timeout
---
>  332178  332175  331965 pre-push
>  332175  332174  331965 git
>  332174  332170  331965 timeout
32,35c33,36
<  332078  332075  331965 pre-push
<  332075  332074  331965 git
<  332074  332070  331965 timeout
<  332070  331965  331965 x.sh
---
>  332178  332175  331965 pre-push
>  332175  332174  331965 git
>  332174  332170  331965 timeout
>  332170  331965  331965 x.sh
```
Observed: the same common-dir hook runs in both. Differences: from the main clone **argv0 is the relative path `.git/hooks/pre-push`** and **`GIT_DIR` is not exported**; from the linked worktree argv0 is absolute and `GIT_DIR` is the worktree-private dir. cwd is the top level of whichever checkout pushed. The non-GIT variable-name list, HOME, PATH and uv lines were identical. A guard that needs "which worktree am I in" can use `pwd` or `git rev-parse --git-dir` inside the hook; it must not assume `GIT_DIR` is set or that `$0` is absolute.

## E19. Hook exits 1: what a refusal looks like

Command block:
```bash
echo "######## E19 hook exits 1 (refusal)"; echo 1 > $S/hook-exit; $X $R brief git -C $S/wt push origin feature:refs/heads/refused1 +alt:main; rm -f $S/hook-exit; echo "hook-exit reset: $(cat $S/hook-exit 2>/dev/null || echo default-0)"
```
Output (verbatim; before and after listings were identical and are shown once):
```text
## remote refs before (/tmp/prepush-research.ERbSguv9/remote.git)
refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492
refs/heads/dev b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/fromclone b833169ed442f5722e4e47d5ded81c5d95f399be
refs/heads/fromwt 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/hp1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/hp2 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/hp3 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/nv1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/side1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/heads/sp1 9a841ac686f348afa68a2158ee64c14260a84df2
refs/tags/v1 b833169ed442f5722e4e47d5ded81c5d95f399be
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature:refs/heads/refused1 +alt:main
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## remote refs after
[identical to before]
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
STDIN: refs/heads/feature 9a841ac686f348afa68a2158ee64c14260a84df2 refs/heads/refused1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
hook-exit reset: default-0
```
Observed: a nonzero hook exit aborts the **whole** push: neither `refused1` nor the forced main update reached the remote; git prints the hook's stderr verbatim, then only `error: failed to push some refs to '<url>'` (no per-ref status lines, no mention of the hook by name) and exits 1. Design line 518 "Refuse the entire push ... nonzero status" is achievable with one nonzero exit [CODE-VERIFIED]. Note the record order: the command named `refused1` first and main second, but **stdin listed main first**, so stdin order is not command order.

## E20. Configured source-only push refspec mapping onto main (`remote.origin.push`), bare `git push origin`

Command block:
```bash
echo "######## setup: commit C3 on feature"; echo four > $S/wt/i.txt; timeout 20 git -C $S/wt add i.txt; timeout 20 git -C $S/wt commit -q -m "feature commit 3"; timeout 20 git -C $S/wt rev-parse HEAD
echo "######## E20 configured remote.origin.push feature:main, bare 'git push origin'"; timeout 20 git -C $S/wt config remote.origin.push refs/heads/feature:refs/heads/main; timeout 20 git -C $S/wt config --get-all remote.origin.push
$X $R brief git -C $S/wt push origin
timeout 20 git -C $S/wt config --unset remote.origin.push; echo "unset rc=$?"; timeout 20 git -C $S/wt config --get-all remote.origin.push; echo "get rc=$?"
```
Output (verbatim; ref listings reduced to the change lines):
```text
######## setup: commit C3 on feature
38a9e0c29811e31f10706c281412462625533f3d
######## E20 configured remote.origin.push feature:main, bare 'git push origin'
refs/heads/feature:refs/heads/main
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin
To /tmp/prepush-research.ERbSguv9/remote.git
   9a841ac..38a9e0c  feature -> main
## exit=0
## REMOTE-REFS-CHANGED: yes
9c9
< refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
---
> refs/heads/main 38a9e0c29811e31f10706c281412462625533f3d
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature 38a9e0c29811e31f10706c281412462625533f3d refs/heads/main 9a841ac686f348afa68a2158ee64c14260a84df2
pwd=/tmp/prepush-research.ERbSguv9/wt
unset rc=0
get rc=1
```
Observed: the command line never names main, yet **field 3 is `refs/heads/main`**. Design line 520 "A source-only refspec configured to resolve to protected heads is protected because field 3 is authoritative" [CODE-VERIFIED]. The config was unset afterwards (`get rc=1`).

## E21. Upstream mapping (`branch --set-upstream-to=origin/main feature` with `-c push.default=upstream push origin`)

Command block:
```bash
echo "######## setup: commit C4 on feature"; echo five > $S/wt/j.txt; timeout 20 git -C $S/wt add j.txt; timeout 20 git -C $S/wt commit -q -m "feature commit 4"; timeout 20 git -C $S/wt rev-parse HEAD
echo "######## E21 upstream=origin/main, push.default=upstream"; timeout 20 git -C $S/wt branch --set-upstream-to=origin/main feature 2>&1; timeout 20 git -C $S/wt config --get branch.feature.merge
$X $R brief git -C $S/wt -c push.default=upstream push origin
timeout 20 git -C $S/wt branch --unset-upstream feature; echo "unset-upstream rc=$?"
```
Output (verbatim; ref listings reduced to the change lines):
```text
######## setup: commit C4 on feature
c51e469b147673198827f39e39d0673b9c51f69d
######## E21 upstream=origin/main, push.default=upstream
branch 'feature' set up to track 'origin/main'.
refs/heads/main
## command: git -C /tmp/prepush-research.ERbSguv9/wt -c push.default=upstream push origin
To /tmp/prepush-research.ERbSguv9/remote.git
   38a9e0c..c51e469  feature -> main
## exit=0
## REMOTE-REFS-CHANGED: yes
9c9
< refs/heads/main 38a9e0c29811e31f10706c281412462625533f3d
---
> refs/heads/main c51e469b147673198827f39e39d0673b9c51f69d
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature c51e469b147673198827f39e39d0673b9c51f69d refs/heads/main 38a9e0c29811e31f10706c281412462625533f3d
pwd=/tmp/prepush-research.ERbSguv9/wt
unset-upstream rc=0
```
Observed: with an upstream mapping the command names neither `feature` nor `main`, yet field 3 is `refs/heads/main`. Any guard (L1 text layer or otherwise) that parses the command line would miss this; the stdin field 3 catches it [CODE-VERIFIED]. Upstream was unset afterwards.

## E22. SHA-256 repository pair: create, update, delete

Command block (`R2=$S/remote256.git`):
```bash
timeout 20 git -c init.defaultBranch=main init --bare --object-format=sha256 $R2 2>&1
timeout 20 git clone $R2 $S/clone256 2>&1
timeout 20 git -C $S/clone256 rev-parse --show-object-format
timeout 20 git -C $S/clone256 config user.name "Research Bot"; timeout 20 git -C $S/clone256 config user.email "research@example.invalid"
timeout 20 git -C $S/clone256 switch -c main 2>&1
echo a > $S/clone256/a.txt; timeout 20 git -C $S/clone256 add a.txt; timeout 20 git -C $S/clone256 commit -q -m "initial256"
cp $S/hook-logging.sh $S/clone256/.git/hooks/pre-push && chmod +x $S/clone256/.git/hooks/pre-push
timeout 20 git -C $S/clone256 remote -v
echo "######## E22a create main"; $X $R2 brief git -C $S/clone256 push origin main
echo b > $S/clone256/b.txt; timeout 20 git -C $S/clone256 add b.txt; timeout 20 git -C $S/clone256 commit -q -m "second256"
echo "######## E22b update main + create tmp"; $X $R2 brief git -C $S/clone256 push origin main main:refs/heads/tmp256
echo "######## E22c delete tmp256"; $X $R2 brief git -C $S/clone256 push origin --delete tmp256
echo "## field widths of last log"; grep '^STDIN' $S/hook.log | while read -r _ a b c d; do echo "f1=$a len2=${#b} f3=$c len4=${#d}"; done
```
Output (verbatim):
```text
Initialized empty Git repository in /tmp/prepush-research.ERbSguv9/remote256.git/
Cloning into '/tmp/prepush-research.ERbSguv9/clone256'...
warning: You appear to have cloned an empty repository.
done.
sha256
Switched to a new branch 'main'
origin	/tmp/prepush-research.ERbSguv9/remote256.git (fetch)
origin	/tmp/prepush-research.ERbSguv9/remote256.git (push)
######## E22a create main
## remote refs before (/tmp/prepush-research.ERbSguv9/remote256.git)
## command: git -C /tmp/prepush-research.ERbSguv9/clone256 push origin main
To /tmp/prepush-research.ERbSguv9/remote256.git
 * [new branch]      main -> main
## exit=0
## remote refs after
refs/heads/main f3002a0af3b0fed6b11b20eaf47f1bb690b3402b500bc10f32be989448abb116
## REMOTE-REFS-CHANGED: yes
0a1
> refs/heads/main f3002a0af3b0fed6b11b20eaf47f1bb690b3402b500bc10f32be989448abb116
## hook log
=== HOOK-RUN file=.git/hooks/pre-push
argv0=.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote256.git
STDIN: refs/heads/main f3002a0af3b0fed6b11b20eaf47f1bb690b3402b500bc10f32be989448abb116 refs/heads/main 0000000000000000000000000000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/clone256
######## E22b update main + create tmp
## remote refs before (/tmp/prepush-research.ERbSguv9/remote256.git)
refs/heads/main f3002a0af3b0fed6b11b20eaf47f1bb690b3402b500bc10f32be989448abb116
## command: git -C /tmp/prepush-research.ERbSguv9/clone256 push origin main main:refs/heads/tmp256
To /tmp/prepush-research.ERbSguv9/remote256.git
   f3002a0..2caac8a  main -> main
 * [new branch]      main -> tmp256
## exit=0
## remote refs after
refs/heads/main 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
refs/heads/tmp256 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
## REMOTE-REFS-CHANGED: yes
1c1,2
< refs/heads/main f3002a0af3b0fed6b11b20eaf47f1bb690b3402b500bc10f32be989448abb116
---
> refs/heads/main 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
> refs/heads/tmp256 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
## hook log
=== HOOK-RUN file=.git/hooks/pre-push
argv0=.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote256.git
STDIN: refs/heads/main 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394 refs/heads/main f3002a0af3b0fed6b11b20eaf47f1bb690b3402b500bc10f32be989448abb116
STDIN: refs/heads/main 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394 refs/heads/tmp256 0000000000000000000000000000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/clone256
######## E22c delete tmp256
## remote refs before (/tmp/prepush-research.ERbSguv9/remote256.git)
refs/heads/main 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
refs/heads/tmp256 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
## command: git -C /tmp/prepush-research.ERbSguv9/clone256 push origin --delete tmp256
To /tmp/prepush-research.ERbSguv9/remote256.git
 - [deleted]         tmp256
## exit=0
## remote refs after
refs/heads/main 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
## REMOTE-REFS-CHANGED: yes
2d1
< refs/heads/tmp256 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
## hook log
=== HOOK-RUN file=.git/hooks/pre-push
argv0=.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote256.git
STDIN: (delete) 0000000000000000000000000000000000000000000000000000000000000000 refs/heads/tmp256 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394
pwd=/tmp/prepush-research.ERbSguv9/clone256
## field widths of last log
f1=(delete) len2=64 f3=refs/heads/tmp256 len4=64
```
Observed: git 2.47.3 supports SHA-256 end to end over the local transport (clone detected `sha256`). Every oid, including the zero oid, is **64 hex characters** (create: 64-zero field 4; delete: 64-zero field 2). The record shape and `(delete)` literal are unchanged. Design line 518 "No hardcoded SHA-1 length is necessary for destination selection" [CODE-VERIFIED]: field 3 is the same text in both formats, and a guard that tests for an all-zero oid must not assume 40 characters. A main deletion was not repeated here because the bare remote's HEAD is main (refused remotely, as in E3b); deletion of a branch was shown instead.

## E23. Rejected non-fast-forward push without force (remote main advanced from `$S/clone2`)

Command block:
```bash
echo "######## setup: clone2 advances remote main"; timeout 20 git clone -q $R $S/clone2 2>&1; timeout 20 git -C $S/clone2 config user.name "Other"; timeout 20 git -C $S/clone2 config user.email "other@example.invalid"; echo other > $S/clone2/o.txt; timeout 20 git -C $S/clone2 add o.txt; timeout 20 git -C $S/clone2 commit -q -m "other advances main"; timeout 20 git -C $S/clone2 push -q origin main 2>&1; timeout 20 git -C $R rev-parse refs/heads/main; ls $S/clone2/.git/hooks/pre-push 2>&1
echo "######## E23a non-ff, remote object unknown locally: feature:main"; $X $R brief git -C $S/wt push origin feature:main
echo "######## setup: fetch so the remote object is known locally"; timeout 20 git -C $S/wt fetch -q origin 2>&1; timeout 20 git -C $S/wt rev-parse origin/main
echo "######## E23b non-ff, remote object known: alt:main"; $X $R brief git -C $S/wt push origin alt:main
```
Output (verbatim; both before/after listings were identical in both runs and are reduced to the runner's change line):
```text
######## setup: clone2 advances remote main
bb59f8c167395bc2c4740d9b0af64915c19e5a1a
ls: cannot access '/tmp/prepush-research.ERbSguv9/clone2/.git/hooks/pre-push': No such file or directory
######## E23a non-ff, remote object unknown locally: feature:main
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature:main
To /tmp/prepush-research.ERbSguv9/remote.git
 ! [rejected]        feature -> main (fetch first)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/feature c51e469b147673198827f39e39d0673b9c51f69d refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a
pwd=/tmp/prepush-research.ERbSguv9/wt
######## setup: fetch so the remote object is known locally
bb59f8c167395bc2c4740d9b0af64915c19e5a1a
######## E23b non-ff, remote object known: alt:main
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin alt:main
To /tmp/prepush-research.ERbSguv9/remote.git
 ! [rejected]        alt -> main (non-fast-forward)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
hint: Updates were rejected because a pushed branch tip is behind its remote
hint: counterpart. If you want to integrate the remote changes, use 'git pull'
hint: before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
EMPTY-STDIN
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed (two different outcomes, both with the hook running and the remote unchanged):
- **"fetch first" rejection** (the remote's new main object is not present locally, E23a): the hook ran **and received the `refs/heads/main` record**; git then rejected the ref itself. A guard therefore sees, and may refuse, a protected push that git would have rejected anyway.
- **"non-fast-forward" rejection** (the remote object is known locally, E23b; same as `main` in E9): the hook ran with **empty stdin**; the rejected ref is filtered out before the hook.
Design line 534 "Use fixture refs that actually reach pre-push (not up-to-date/nonfastforward rejection)" is consistent with E23b and E12 [CODE-VERIFIED]; E23a adds a nuance the design does not state: a "fetch first" rejection still reaches pre-push.

## E24. Mixed push, protected ref last vs first on the command line (hook exit 1)

Remote refs before both runs (relevant lines): `refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a`; no `refs/heads/side`. `mm` is a new commit on top of `origin/main`, so `mm:main` is a fast-forward and reaches the hook.

Command block:
```bash
T=$(timeout 20 git -C $S/wt rev-parse 'origin/main^{tree}'); C=$(timeout 20 git -C $S/wt commit-tree "$T" -p origin/main -m mm); timeout 20 git -C $S/wt branch mm "$C"; timeout 20 git -C $S/wt rev-parse mm; echo 1 > $S/hook-exit
$X $R brief git -C $S/wt push origin feature:refs/heads/side mm:main 2>&1 | grep -vE '^refs/|^## remote refs'   # E24a
$X $R brief git -C $S/wt push origin mm:main feature:refs/heads/side 2>&1 | grep -vE '^refs/|^## remote refs'   # E24b
```
Output (verbatim; the before/after ref listings are filtered out by the grep and summarised by the runner's change line):
```text
053b17ae9d179b558da3bc65bc1c0d9d80687b61
######## E24a protected LAST: feature:refs/heads/side mm:main
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin feature:refs/heads/side mm:main
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a
STDIN: refs/heads/feature c51e469b147673198827f39e39d0673b9c51f69d refs/heads/side 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E24b protected FIRST: mm:main feature:refs/heads/side
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin mm:main feature:refs/heads/side
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a
STDIN: refs/heads/feature c51e469b147673198827f39e39d0673b9c51f69d refs/heads/side 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: stdin order is identical in both runs and independent of command-line order. The existing remote ref (`main`) came first and the new ref (`side`) second; with E19 this suggests the order follows git's internal ref list (remote refs already present, then new refs), but that rule is inferred, not documented [UNVERIFIED]. A guard must scan every record and must not rely on position. One refusal aborted both updates (remote unchanged).

## E25. Look-alike destinations (hook exit 1)

Remote refs before: as in E24 (`main` = bb59f8c, `feature` exists, none of the six targets exist). After: unchanged.

Command block:
```bash
echo 1 > $S/hook-exit
$X $R brief git -C $S/wt push origin mm:refs/heads/mainline mm:refs/heads/feature/main mm:refs/heads/main2 mm:refs/tags/main mm:refs/heads/Main mm:refs/heads/master 2>&1 | grep -vE '^refs/|^## remote refs'
```
Output (verbatim, ref listings filtered):
```text
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin mm:refs/heads/mainline mm:refs/heads/feature/main mm:refs/heads/main2 mm:refs/tags/main mm:refs/heads/Main mm:refs/heads/master
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/mainline 0000000000000000000000000000000000000000
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/feature/main 0000000000000000000000000000000000000000
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/main2 0000000000000000000000000000000000000000
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/tags/main 0000000000000000000000000000000000000000
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/Main 0000000000000000000000000000000000000000
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/master 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: field 3 is always the full, case-preserved ref name exactly as it will be written. Only an exact string compare of field 3 against `refs/heads/main` / `refs/heads/master` separates the protected refs from `refs/heads/mainline`, `refs/heads/main2`, `refs/heads/feature/main`, `refs/tags/main` and `refs/heads/Main`. Prefix, suffix or basename matching would refuse wrongly. `refs/heads/feature/main` reached the hook even though the remote has `refs/heads/feature`, a directory/file conflict the remote would reject. Whether `refs/heads/Main` would collide with `main` on a case-insensitive remote filesystem was not tested [UNVERIFIED]. Creating `refs/heads/master` (a protected name) shows the zero oid in field 4, so new-ref creation of a protected name is visible to the guard.

## E26. `--atomic` with one protected and one unprotected ref

Remote refs before E26a and E26b: `refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a`, no `side2`. After E26a: unchanged. After E26b: `main` -> `053b17ae9d179b558da3bc65bc1c0d9d80687b61` and new `refs/heads/side2 c51e469b147673198827f39e39d0673b9c51f69d`.

Command block:
```bash
echo 1 > $S/hook-exit
$X $R brief git -C $S/wt push --atomic origin mm:main feature:refs/heads/side2 2>&1 | grep -vE '^refs/|^## remote refs'   # E26a
echo 0 > $S/hook-exit
$X $R brief git -C $S/wt push --atomic origin mm:main feature:refs/heads/side2 2>&1 | grep -vE '^## remote refs'          # E26b
```
Output (verbatim; for E26b the 13- and 14-line before/after listings are reduced to the diff the runner prints):
```text
######## E26a --atomic protected+unprotected, hook exit 1
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --atomic origin mm:main feature:refs/heads/side2
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a
STDIN: refs/heads/feature c51e469b147673198827f39e39d0673b9c51f69d refs/heads/side2 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E26b --atomic protected+unprotected, hook exit 0
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --atomic origin mm:main feature:refs/heads/side2
To /tmp/prepush-research.ERbSguv9/remote.git
   bb59f8c..053b17a  mm -> main
 * [new branch]      feature -> side2
## exit=0
## REMOTE-REFS-CHANGED: yes
9c9
< refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a
---
> refs/heads/main 053b17ae9d179b558da3bc65bc1c0d9d80687b61
11a12
> refs/heads/side2 c51e469b147673198827f39e39d0673b9c51f69d
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/main bb59f8c167395bc2c4740d9b0af64915c19e5a1a
STDIN: refs/heads/feature c51e469b147673198827f39e39d0673b9c51f69d refs/heads/side2 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: `--atomic` changes neither the hook call nor stdin. The hook ran once with both records, and its exit code decided all-or-nothing in both modes. A refusal left the remote unchanged; exit 0 applied both updates. For a pre-push guard, `--atomic` behaves like the non-atomic case (E24): a non-atomic push is also aborted entirely by a hook refusal.

## E27. `--force-with-lease` with a stale vs a matching expected oid

Remote refs before both runs: `refs/heads/main 053b17ae9d179b558da3bc65bc1c0d9d80687b61` (moved by E26b). After both: unchanged.

Command block:
```bash
echo 0 > $S/hook-exit
$X $R brief git -C $S/wt push --force-with-lease=main:bb59f8c167395bc2c4740d9b0af64915c19e5a1a origin alt:main 2>&1 | grep -vE '^refs/|^## remote refs'   # E27a stale
echo 1 > $S/hook-exit
$X $R brief git -C $S/wt push --force-with-lease=main:053b17ae9d179b558da3bc65bc1c0d9d80687b61 origin alt:main 2>&1 | grep -vE '^refs/|^## remote refs'   # E27b matching
```
Output (verbatim, ref listings filtered):
```text
######## E27a --force-with-lease, STALE expected oid bb59f8c (remote main is now 053b17a), hook exit 0
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --force-with-lease=main:bb59f8c167395bc2c4740d9b0af64915c19e5a1a origin alt:main
To /tmp/prepush-research.ERbSguv9/remote.git
 ! [rejected]        alt -> main (stale info)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
EMPTY-STDIN
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E27b --force-with-lease, CORRECT expected oid 053b17a, hook exit 1
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --force-with-lease=main:053b17ae9d179b558da3bc65bc1c0d9d80687b61 origin alt:main
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-research.ERbSguv9/remote.git'
## exit=1
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv0=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-research.ERbSguv9/remote.git
STDIN: refs/heads/alt 404f82e243b3a0abf5de608f63589bca41ecd492 refs/heads/main 053b17ae9d179b558da3bc65bc1c0d9d80687b61
pwd=/tmp/prepush-research.ERbSguv9/wt
```
Observed: a stale lease is rejected locally ("stale info") before the hook. The hook still runs, but with empty stdin, the same filtering as a non-fast-forward (E23b). With a matching lease, the hook receives the forced rewrite record: field 4 is the current remote oid and field 2 is a non-descendant. The guard alone refused it, and the remote stayed unchanged.

## E28. Environment pass-through to the hook (HOME, PATH, marker variable, uv)

All three runs use `--dry-run` to a new ref (`refs/heads/envtest`) with hook exit 0, so a real record reaches the hook and the remote never changes. Remote refs before and after: identical in all three runs (`main` = 053b17a). `$S/bin` and `$S/home2` are empty directories inside the sandbox. HOME is replaced or unset only on these single pushes.

Command block:
```bash
echo 0 > $S/hook-exit; ls -A $S/bin $S/home2; F='^(## exit|## REMOTE|=== HOOK|STDIN|EMPTY|HOME=|PATH=|uv=|PREPUSH|GIT_|CCSESSION|CLAUDECODE)'
$X $R full env HOME=$S/home2 PREPUSH_MARKER=marker-1 PATH=$S/bin:$PATH git -C $S/wt push --dry-run origin mm:refs/heads/envtest 2>&1 | grep -E "$F"   # E28a
$X $R full env -u HOME git -C $S/wt push --dry-run origin mm:refs/heads/envtest 2>&1 | grep -E "$F"                                                  # E28b
$X $R full env PATH=/usr/bin:/bin /usr/bin/git -C $S/wt push --dry-run origin mm:refs/heads/envtest 2>&1 | grep -E "$F"                             # E28c
```
Output (verbatim, filtered to the lines named in `F`; the identical `GIT_*` block is shown once for E28a and summarised for E28b/E28c):
```text
######## E28a HOME=$S/home2 PREPUSH_MARKER=marker-1 PATH=$S/bin:$PATH
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/envtest 0000000000000000000000000000000000000000
GIT_ASKPASS=
GIT_CONFIG_COUNT=2
GIT_CONFIG_KEY_0=credential.interactive
GIT_CONFIG_KEY_1=credential.guiPrompt
GIT_CONFIG_NOSYSTEM=1
GIT_CONFIG_VALUE_0=false
GIT_CONFIG_VALUE_1=false
GIT_DIR=/tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt
GIT_EDITOR=true
GIT_EXEC_PATH=/usr/lib/git-core
GIT_PREFIX=
GIT_TERMINAL_PROMPT=0
HOME=/tmp/prepush-research.ERbSguv9/home2
PATH=/usr/lib/git-core:/tmp/prepush-research.ERbSguv9/bin:/home/coder/.config/orca/linux-orca-cli-shim:/home/coder/.local/bin:/usr/local/bin:/opt/nvm/versions/node/v24.22.2/bin:/home/coder/.local/bin:/home/coder/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
uv=/usr/local/bin/uv
PREPUSH_MARKER=marker-1
CCSESSION_LAUNCH_ID present: yes
CLAUDECODE present: yes
######## E28b env -u HOME
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/envtest 0000000000000000000000000000000000000000
[GIT_* block identical to E28a, 13 lines]
HOME=<UNSET>
PATH=/usr/lib/git-core:/home/coder/.config/orca/linux-orca-cli-shim:/home/coder/.local/bin:/usr/local/bin:/opt/nvm/versions/node/v24.22.2/bin:/home/coder/.local/bin:/home/coder/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
uv=/usr/local/bin/uv
PREPUSH_MARKER=<UNSET>
CCSESSION_LAUNCH_ID present: yes
CLAUDECODE present: yes
######## E28c PATH=/usr/bin:/bin (no /usr/local/bin); git at /usr/bin/git
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/envtest 0000000000000000000000000000000000000000
[GIT_* block identical to E28a, 13 lines]
HOME=/tmp/prepush-research.ERbSguv9/home
PATH=/usr/lib/git-core:/usr/bin:/bin
uv=UV-ABSENT
PREPUSH_MARKER=<UNSET>
CCSESSION_LAUNCH_ID present: yes
CLAUDECODE present: yes
```
Observed:
- **Inheritance:** git passes the pusher's environment to the hook unchanged. HOME is passed as given, and stays unset when the pusher unset it (E28b ran without error). An arbitrary marker variable is passed through. PATH is the caller's PATH with `/usr/lib/git-core` (= `GIT_EXEC_PATH`) prepended.
- **Who controls the hook's view:** HOME, PATH and any marker variable are therefore entirely in the pusher's hands. A governed agent can unset or change any of them on the single push, so none of them can serve as authority. That agrees with the design's never-authority rule for `CCSESSION_LAUNCH_ID`/`CLAUDECODE` (design §19.1 line 493) [CODE-VERIFIED for pass-through; the design rule itself is a policy statement].
- **uv:** with a PATH lacking `/usr/local/bin` (E28c), `uv` is not resolvable inside the hook (`UV-ABSENT`). A hook that runs `uv run ...` by bare name would then fail. Whether a failure blocks the push depends on the hook's exit code: a nonzero exit refuses (E9-E11). A guard that must fail closed has to call uv by absolute path or not depend on uv at all. Correction (Gate 1 cycle 0 fix): an absolute uv path in the hook alone is not enough if the hook calls `launch-job-identity.sh identify`, because that script resolves uv through PATH itself, at `command -v uv` (line 25) and `exec uv run --no-project python ...` (line 566), and its no-store early exit (lines 20-24) does not apply to `identify`. The hook would have to set a fixed PATH containing the uv directory recorded at install time, or not depend on uv at all; see 01 §4 item 5 for the human-side consequence (exit 2 is treated as `unknown`, so a human whose PATH lacks uv cannot push to `main`/`master`).
- **Harness variables:** `GIT_ASKPASS`, `GIT_CONFIG_COUNT/KEY/VALUE`, `GIT_EDITOR`, `GIT_TERMINAL_PROMPT`, `CCSESSION_LAUNCH_ID` and `CLAUDECODE` come from the Claude Code environment this research ran in, not from git. git itself added only `GIT_DIR` (linked worktree), `GIT_EXEC_PATH`, `GIT_PREFIX` and the PATH prefix, as in E0/E1.

## E29. Non-executable hook (executable-bit part of sub-question e)

The hook file stays in place with its contents unchanged; only the executable bit is removed. `hook-exit` is 1, so the hook would refuse if it ran. Remote `main` is already `053b17a` (= `mm`, from E26b), so `mm:main` is up to date. E12 showed that an up-to-date push normally still runs the hook (with empty stdin). Remote refs before E29a/E29b equal those after. E29c added `refs/heads/nx1`.

Command block:
```bash
echo 1 > $S/hook-exit
chmod -x $S/clone/.git/hooks/pre-push; ls -l $S/clone/.git/hooks/pre-push
$X $R brief git -C $S/wt push --dry-run origin mm:main 2>&1 | grep -vE '^refs/|^## remote refs'                                   # E29a
$X $R brief git -C $S/wt -c advice.ignoredHook=false push --dry-run origin mm:main 2>&1 | grep -vE '^refs/|^## remote refs'        # E29b
$X $R brief git -C $S/wt push origin mm:refs/heads/nx1 2>&1 | grep -vE '^## remote refs' | grep -vE '^refs/heads/(alt|dev|feature|from|hp|nv|side|sp)|^refs/tags'   # E29c
chmod +x $S/clone/.git/hooks/pre-push; ls -l $S/clone/.git/hooks/pre-push                                                          # restore
```
Output (verbatim; in E29c the unchanged ref lines other than `main`/`nx1` are filtered out):
```text
-rw-r--r-- 1 coder coder 1463 Nov  8 11:12 /tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
######## E29a non-executable hook (hook-exit=1 would refuse if it ran)
## command: git -C /tmp/prepush-research.ERbSguv9/wt push --dry-run origin mm:main
hint: The '/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push' hook was ignored because it's not set as executable.
hint: You can disable this warning with `git config advice.ignoredHook false`.
Everything up-to-date
## exit=0
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
######## E29b same with -c advice.ignoredHook=false
## command: git -C /tmp/prepush-research.ERbSguv9/wt -c advice.ignoredHook=false push --dry-run origin mm:main
Everything up-to-date
## exit=0
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
######## E29c real (non-dry-run) push, hook still non-executable
refs/heads/main 053b17ae9d179b558da3bc65bc1c0d9d80687b61
## command: git -C /tmp/prepush-research.ERbSguv9/wt push origin mm:refs/heads/nx1
hint: The '/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push' hook was ignored because it's not set as executable.
hint: You can disable this warning with `git config advice.ignoredHook false`.
To /tmp/prepush-research.ERbSguv9/remote.git
 * [new branch]      mm -> nx1
## exit=0
refs/heads/main 053b17ae9d179b558da3bc65bc1c0d9d80687b61
refs/heads/nx1 053b17ae9d179b558da3bc65bc1c0d9d80687b61
## REMOTE-REFS-CHANGED: yes
10a11
> refs/heads/nx1 053b17ae9d179b558da3bc65bc1c0d9d80687b61
## hook log
HOOK-NOT-RUN (log empty)
-rwxr-xr-x 1 coder coder 1463 Nov  8 11:12 /tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
```
Observed: a non-executable `pre-push` **fails open**. git skips it, prints a two-line `hint:` on stderr and exits 0, and a real push goes through (E29c: the remote gained `nx1` although the hook would have refused). `-c advice.ignoredHook=false`, which any pusher can pass per command, removes even the hint, so the skip becomes fully silent (E29b). An installer or doctor check must therefore verify the executable bit itself; git's warning is advisory only and the pusher can suppress it. The executable bit was restored afterwards (`-rwxr-xr-x`).

## E30. Hook placement: worktree-private git dir, `--git-path`, absolute and relative `core.hooksPath`

All pushes are `--dry-run` to a new ref `refs/heads/plc1` with hook exit 0. Remote refs before and after: unchanged in every run. Every hook copy is the same logging script, told apart by the `file=$0` line.

Command block:
```bash
echo 0 > $S/hook-exit; F='^(## exit|## REMOTE|=== HOOK|STDIN|EMPTY|HOOK-NOT|pwd=)'
WTGD=$(timeout 20 git -C $S/wt rev-parse --git-dir); echo "wt git-dir: $WTGD"; echo "wt common-dir: $(timeout 20 git -C $S/wt rev-parse --git-common-dir)"
# E30a
timeout 20 git -C $S/wt rev-parse --git-path hooks --git-path hooks/pre-push; timeout 20 git -C $S/clone rev-parse --git-path hooks/pre-push
# E30b
mkdir -p "$WTGD/hooks"; cp $S/hook-logging.sh "$WTGD/hooks/pre-push"; chmod +x "$WTGD/hooks/pre-push"; ls -l "$WTGD/hooks/pre-push"; $X $R brief git -C $S/wt push --dry-run origin mm:refs/heads/plc1 2>&1 | grep -E "$F"; rm -- "$WTGD/hooks/pre-push"; rmdir -- "$WTGD/hooks"
# E30c
timeout 20 git -C $S/wt -c core.hooksPath=$S/otherhooks rev-parse --git-path hooks --git-path hooks/pre-push; $X $R brief git -C $S/wt -c core.hooksPath=$S/otherhooks push --dry-run origin mm:refs/heads/plc1 2>&1 | grep -E "$F"
# E30d
for d in $S/wt/relhooks $S/clone/relhooks; do mkdir -p $d; cp $S/hook-logging.sh $d/pre-push; chmod +x $d/pre-push; done
timeout 20 git -C $S/wt -c core.hooksPath=relhooks rev-parse --git-path hooks --git-path hooks/pre-push; mkdir -p $S/wt/sub; timeout 20 git -C $S/wt/sub -c core.hooksPath=relhooks rev-parse --git-path hooks/pre-push
$X $R brief git -C $S/wt     -c core.hooksPath=relhooks push --dry-run origin mm:refs/heads/plc1 2>&1 | grep -E "$F"
$X $R brief git -C $S/wt/sub -c core.hooksPath=relhooks push --dry-run origin mm:refs/heads/plc1 2>&1 | grep -E "$F"
$X $R brief git -C $S/clone  -c core.hooksPath=relhooks push --dry-run origin mm:refs/heads/plc1 2>&1 | grep -E "$F"
rm -rf -- $S/wt/relhooks $S/clone/relhooks $S/wt/sub; timeout 20 git -C $S/wt status --porcelain | head -5
```
Output (verbatim; the final `status --porcelain` printed nothing):
```text
wt git-dir: /tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt
wt common-dir: /tmp/prepush-research.ERbSguv9/clone/.git
######## E30a rev-parse --git-path, no core.hooksPath
/tmp/prepush-research.ERbSguv9/clone/.git/hooks
/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
.git/hooks/pre-push
######## E30b hook copy in worktree-private git dir
-rwxr-xr-x 1 coder coder 1463 Nov  8 11:23 /tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt/hooks/pre-push
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/plc1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E30c absolute core.hooksPath=$S/otherhooks
/tmp/prepush-research.ERbSguv9/otherhooks
/tmp/prepush-research.ERbSguv9/otherhooks/pre-push
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/otherhooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/plc1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E30d relative core.hooksPath=relhooks (copies in wt/relhooks AND clone/relhooks)
relhooks
relhooks/pre-push
-- from wt/sub:
../relhooks/pre-push
-- push from wt:
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=relhooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/plc1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
-- push from wt/sub:
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=relhooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/plc1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
-- push from clone:
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=relhooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/plc1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/clone
```
Observed:
- **Default location:** with no `core.hooksPath`, a linked worktree resolves `hooks/pre-push` to the **common dir** (`clone/.git/hooks/pre-push`, E30a). A hook placed in the worktree-private git dir (`clone/.git/worktrees/wt/hooks/pre-push`) is **ignored**, and the common-dir hook runs (E30b). An installer must target `git rev-parse --git-path hooks/pre-push` (or `--git-common-dir`/hooks), never `--git-dir`/hooks.
- **Path form:** `--git-path` prints a path **relative to the cwd** when run in the main clone (`.git/hooks/pre-push`) and absolute in a linked worktree. Run from the main clone, the hook's `$0` is likewise the relative `.git/hooks/pre-push` (E31b). Tooling should normalise with `--path-format=absolute` or resolve against the cwd. That option was not exercised here [UNVERIFIED].
- **Absolute hooksPath:** honoured exactly, both by `--git-path` and at push time (E30c).
- **Relative hooksPath:** `--git-path` echoes it relative to the cwd (`relhooks`, `../relhooks/...` from a subdirectory). At push time git runs the hook from the **top of the pushing worktree** (pwd = the worktree root even when invoked from `wt/sub`) and resolves `relhooks/pre-push` against it. The wt push ran `wt/relhooks`, the clone push ran `clone/relhooks`. So a relative `core.hooksPath` in shared config selects a *different* hook per worktree, and it lives inside the working tree, where the agent can edit it.
- Cleanup: the temporary hook copies, `relhooks` dirs and `wt/sub` were removed. `git status --porcelain` in wt was empty.

## E31. `extensions.worktreeConfig` + per-worktree `core.hooksPath`

Remote refs before and after: unchanged (dry-run). Hook exit 0.

Command block:
```bash
echo 0 > $S/hook-exit
timeout 20 git -C $S/clone config extensions.worktreeConfig true; timeout 20 git -C $S/wt config --worktree core.hooksPath $S/otherhooks
timeout 20 git -C $S/wt config --show-origin --get-all core.hooksPath; timeout 20 git -C $S/clone config --show-origin --get-all core.hooksPath || echo "clone: core.hooksPath unset (exit $?)"; ls $S/clone/.git/worktrees/wt/config.worktree
timeout 20 git -C $S/wt rev-parse --git-path hooks/pre-push; timeout 20 git -C $S/clone rev-parse --git-path hooks/pre-push
$X $R brief git -C $S/wt push --dry-run origin mm:refs/heads/plc1 2>&1 | grep -E "$F"      # E31a
$X $R brief git -C $S/clone push --dry-run origin mm:refs/heads/plc1 2>&1 | grep -E "$F"   # E31b
timeout 20 git -C $S/wt config --worktree --unset core.hooksPath; timeout 20 git -C $S/clone config --unset extensions.worktreeConfig; timeout 20 git -C $S/wt rev-parse --git-path hooks/pre-push; timeout 20 git -C $S/clone config --list --local | grep -iE 'hookspath|worktreeconfig' || echo "no hooksPath/worktreeConfig in clone local config"
```
Output (verbatim):
```text
-- config sources:
file:/tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt/config.worktree	/tmp/prepush-research.ERbSguv9/otherhooks
clone: core.hooksPath unset (exit 1)
/tmp/prepush-research.ERbSguv9/clone/.git/worktrees/wt/config.worktree
-- git-path:
/tmp/prepush-research.ERbSguv9/otherhooks/pre-push
.git/hooks/pre-push
######## E31a push from wt
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=/tmp/prepush-research.ERbSguv9/otherhooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/plc1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/wt
######## E31b push from clone
## exit=0
## REMOTE-REFS-CHANGED: no
=== HOOK-RUN file=.git/hooks/pre-push
STDIN: refs/heads/mm 053b17ae9d179b558da3bc65bc1c0d9d80687b61 refs/heads/plc1 0000000000000000000000000000000000000000
pwd=/tmp/prepush-research.ERbSguv9/clone
######## restore
/tmp/prepush-research.ERbSguv9/clone/.git/hooks/pre-push
no hooksPath/worktreeConfig in clone local config
```
Observed: with `extensions.worktreeConfig=true`, a `core.hooksPath` written to `clone/.git/worktrees/wt/config.worktree` redirects **only that worktree's** hooks. The wt push ran `otherhooks/pre-push`, while the main clone kept the common-dir hook. Any process that can write the worktree's git dir (or run `git config --worktree`) can therefore swap out the guard for one worktree without touching the shared config, an install-integrity risk alongside E7/E8 (per-process `-c core.hooksPath`). A doctor check should read the effective value with `git -C <worktree> config --show-origin core.hooksPath` per worktree. Restored: the per-worktree setting and the extension were removed, and wt again resolves to the common-dir hook.

## Sandbox removal

Command block and output (verbatim):
```bash
rm -rf -- "/tmp/prepush-research.ERbSguv9"; echo "rm exit=$?"; ls -d "/tmp/prepush-research.ERbSguv9"; echo "ls exit=$?"
```
```text
rm exit=0
ls: cannot access '/tmp/prepush-research.ERbSguv9': No such file or directory
ls exit=2
```
Observed: the sandbox, including both bare remotes, every clone and worktree, the hook copies and the logs, is gone. No git command in this research ran inside the IronClaude repository or against a real remote.

## Results table

Key oids: `afa71f1…` = `afa71f1a6d85ee82d3186fac8649d1cb8cb298b3`, `b833169…` = `b833169ed442f5722e4e47d5ded81c5d95f399be`, `404f82e…` = `404f82e243b3a0abf5de608f63589bca41ecd492`, `9a841ac…` = `9a841ac686f348afa68a2158ee64c14260a84df2`, `38a9e0c…` = `38a9e0c29811e31f10706c281412462625533f3d`, `c51e469…` = `c51e469b147673198827f39e39d0673b9c51f69d`, `bb59f8c…` = `bb59f8c167395bc2c4740d9b0af64915c19e5a1a`, `053b17a…` = `053b17ae9d179b558da3bc65bc1c0d9d80687b61`. `Z40` = 40 zeros, `Z64` = 64 zeros. The records are otherwise verbatim (full text in each section). Rows with more than three records name the section instead. "n/r (brief)" means the hook logged HOME/PATH/uv but the brief runner mode did not print them.

| Experiment | Hook ran (yes/no) | Stdin records (verbatim or EMPTY) | Remote refs changed (yes/no) | Hook HOME/PATH/uv as seen | Evidence section |
|---|---|---|---|---|---|
| Create `feature` from linked worktree | yes (common dir) | `refs/heads/feature afa71f1… refs/heads/feature Z40` | yes | HOME=$S/home; PATH=/usr/lib/git-core:+caller PATH; uv=/usr/local/bin/uv | E1 |
| Fast-forward `feature:main` | yes | `refs/heads/feature afa71f1… refs/heads/main b833169…` | yes | n/r (brief) | E2 |
| Delete branch `:dev` | yes | `(delete) Z40 refs/heads/dev b833169…` | yes | n/r (brief) | E3a |
| Delete `:main` (remote HEAD = main) | yes | `(delete) Z40 refs/heads/main afa71f1…` | no (remote denyDeleteCurrent) | n/r (brief) | E3b |
| `--delete tmp1` | yes | `(delete) Z40 refs/heads/tmp1 afa71f1…` | yes | n/r (brief) | E4a |
| `--delete main` (remote HEAD moved) | yes | `(delete) Z40 refs/heads/main afa71f1…` | yes | n/r (brief) | E4b |
| Forced `+alt:main` | yes | `refs/heads/alt 404f82e… refs/heads/main afa71f1…` | yes | n/r (brief) | E5a |
| Forced `--force feature:main` | yes | `refs/heads/feature afa71f1… refs/heads/main 404f82e…` | yes | n/r (brief) | E5b |
| Two refspecs | yes | `refs/heads/feature afa71f1… refs/heads/side1 Z40` / `refs/heads/alt 404f82e… refs/heads/side2 Z40` | yes | n/r (brief) | E7 |
| `HEAD:main` | yes | `HEAD 9a841ac… refs/heads/main afa71f1…` | yes | n/r (brief) | E6 |
| Update plus delete | yes | `refs/heads/feature 9a841ac… refs/heads/side1 afa71f1…` / `(delete) Z40 refs/heads/side2 404f82e…` | yes | n/r (brief) | E8 |
| `--all` (local main behind) | yes | `refs/heads/feature 9a841ac… refs/heads/feature afa71f1…` / `refs/heads/alt 404f82e… refs/heads/alt Z40` / `refs/heads/dev b833169… refs/heads/dev Z40` (main omitted) | yes (exit 1) | n/r (brief) | E9 |
| `--tags` | yes | `refs/tags/v1 b833169… refs/tags/v1 Z40` | yes | n/r (brief) | E10 |
| `--mirror` to URL (argv1 = URL) | yes | 10 records, see E11 (includes `refs/heads/main b833169… refs/heads/main Z40`) | yes (remote2) | n/r (brief) | E11 |
| Up-to-date `feature` | yes | EMPTY | no | n/r (brief) | E12 |
| Up-to-date `HEAD:main` | yes | EMPTY | no | n/r (brief) | E12b |
| `--dry-run` new ref | yes | `refs/heads/feature 9a841ac… refs/heads/dry1 Z40` | no | n/r (brief) | E13 |
| `--dry-run +alt:main` | yes | `refs/heads/alt 404f82e… refs/heads/main 9a841ac…` | no | n/r (brief) | E13b |
| `--no-verify` | no | n/a | yes | n/a | E14 |
| `-c core.hooksPath=/dev/null` | no | n/a | yes | n/a | E15 |
| `-c core.hooksPath=<dir without pre-push>` | no | n/a | yes | n/a | E16 |
| `-c core.hooksPath=<dir with pre-push>` | yes (that hook only) | `refs/heads/feature 9a841ac… refs/heads/hp3 Z40` | yes | n/r (brief) | E16 |
| `send-pack main` | no | n/a | no (rejected non-ff) | n/a | E17 (a) |
| `send-pack` create | no | n/a | yes | n/a | E17 (b) |
| `send-pack --force alt:refs/heads/main` | no | n/a | yes (main rewritten) | n/a | E17 (c) |
| Push from main clone | yes (argv0 relative, no GIT_DIR) | `refs/heads/dev b833169… refs/heads/fromclone Z40` | yes | HOME=$S/home; PATH as in E1; uv=/usr/local/bin/uv | E18 |
| Hook exit 1, two refs | yes | `refs/heads/alt 404f82e… refs/heads/main 9a841ac…` / `refs/heads/feature 9a841ac… refs/heads/refused1 Z40` | no | n/r (brief) | E19 |
| Configured push refspec, bare `git push origin` | yes | `refs/heads/feature 38a9e0c… refs/heads/main 9a841ac…` | yes | n/r (brief) | E20 |
| Upstream mapping, `push.default=upstream` | yes | `refs/heads/feature c51e469… refs/heads/main 38a9e0c…` | yes | n/r (brief) | E21 |
| SHA-256 create | yes | `refs/heads/main f3002a0af3b0fed6b11b20eaf47f1bb690b3402b500bc10f32be989448abb116 refs/heads/main Z64` | yes | n/r (brief) | E22 |
| SHA-256 update + create | yes | `refs/heads/main 2caac8a096cdebd06b2cb8a168d5f8a87a1e6d1f33a01715e201718ee40b1394 refs/heads/main f3002a0a…b116` / `refs/heads/main 2caac8a0…1394 refs/heads/tmp256 Z64` | yes | n/r (brief) | E22 |
| SHA-256 delete | yes | `(delete) Z64 refs/heads/tmp256 2caac8a0…1394` | yes | n/r (brief) | E22 |
| Non-ff, "fetch first" (remote object unknown) | yes | `refs/heads/feature c51e469… refs/heads/main bb59f8c…` | no | n/r (brief) | E23 (a) |
| Non-ff, remote object known | yes | EMPTY | no | n/r (brief) | E23 (b) |
| Mixed, protected last (exit 1) | yes | `refs/heads/mm 053b17a… refs/heads/main bb59f8c…` / `refs/heads/feature c51e469… refs/heads/side Z40` | no | n/r (brief) | E24 (a) |
| Mixed, protected first (exit 1) | yes | same two records, same order | no | n/r (brief) | E24 (b) |
| Look-alike destinations (exit 1) | yes | 6 records, see E25 (field 3: `refs/heads/mainline`, `refs/heads/feature/main`, `refs/heads/main2`, `refs/tags/main`, `refs/heads/Main`, `refs/heads/master`) | no | n/r (brief) | E25 |
| `--atomic`, exit 1 | yes | `refs/heads/mm 053b17a… refs/heads/main bb59f8c…` / `refs/heads/feature c51e469… refs/heads/side2 Z40` | no | n/r (brief) | E26 (a) |
| `--atomic`, exit 0 | yes | same two records | yes (both) | n/r (brief) | E26 (b) |
| `--force-with-lease`, stale | yes | EMPTY | no | n/r (brief) | E27 (a) |
| `--force-with-lease`, matching (exit 1) | yes | `refs/heads/alt 404f82e… refs/heads/main 053b17a…` | no | n/r (brief) | E27 (b) |
| `HOME=$S/home2`, marker, `PATH=$S/bin:$PATH` (dry-run) | yes | `refs/heads/mm 053b17a… refs/heads/envtest Z40` | no | HOME=$S/home2; PATH=/usr/lib/git-core:$S/bin:…; uv=/usr/local/bin/uv; PREPUSH_MARKER=marker-1 | E28 (a) |
| `env -u HOME` (dry-run) | yes | same record | no | HOME=<UNSET>; PATH=/usr/lib/git-core:+caller PATH; uv=/usr/local/bin/uv | E28 (b) |
| `PATH=/usr/bin:/bin` (dry-run) | yes | same record | no | HOME=$S/home; PATH=/usr/lib/git-core:/usr/bin:/bin; uv=UV-ABSENT | E28 (c) |
| Non-executable hook (dry-run, up to date) | no (hint printed) | n/a | no | n/a | E29 (a) |
| Non-executable + `advice.ignoredHook=false` | no (silent) | n/a | no | n/a | E29 (b) |
| Non-executable, real push | no (hint printed) | n/a | yes (fail-open) | n/a | E29 (c) |
| Hook only in worktree-private git dir | yes (common-dir hook; private ignored) | `refs/heads/mm 053b17a… refs/heads/plc1 Z40` | no | n/r (brief) | E30 (b) |
| Absolute `core.hooksPath` | yes (that dir) | same plc1 record | no | n/r (brief) | E30 (c) |
| Relative `core.hooksPath` from wt, wt/sub, clone | yes (`<worktree-root>/relhooks`) | same plc1 record | no | n/r (brief) | E30 (d) |
| `worktreeConfig` hooksPath, push from wt | yes (otherhooks) | same plc1 record | no | n/r (brief) | E31 (a) |
| `worktreeConfig` hooksPath, push from clone | yes (common `.git/hooks`) | same plc1 record | no | n/r (brief) | E31 (b) |

## Step 2.5 Design-claim cross-check and follow-up experiments

FOLLOWUP_SANDBOX_PATH: /tmp/prepush-followup.0OZWoyIi

Scope: every `UNVERIFIED-GIT D19-n` line of `research/03-design-and-claim-code-crossvalidation.md` (Gaps), plus the claim-table rows of file 03 whose [UNVERIFIED] status rests partly on git behaviour (D19-27, D19-29). Each claim was re-read in full at `docs/designs/sc-issue-launch-level-hook.md` lines 489-578. "Covered by" names the file 04 experiment above; a claim with no covering experiment that a local sandbox can settle gets a follow-up subsection below (F1 to F4). Claims about hosting services or real remotes are routed to web-01 and were not tested against any network service.

| D19 ID | Design line | Claim (short) | Covered by file 04 experiment (section name or none) | Result | Route |
|---|---|---|---|---|---|
| D19-2 | 493 | Pre-push inputs are remote name/location (argv) and ref-update records (stdin); git supplies no Claude session id | E1 (argv1 `origin`, argv2 URL, stdin records), E11 (argv1 = URL when no remote name), E18, E28 | CONFIRMED [CODE-VERIFIED]. Note: the caller's whole environment passes through (E1, E28), including `CLAUDE_CODE_SESSION_ID`, `CCSESSION_LAUNCH_ID`, `CLAUDECODE`; these are inherited, not supplied by git, and are not authority (design line 493 already says so) | done |
| D19-20 | 518 | Each stdin record is `<local-ref> <local-oid> <remote-ref> <remote-oid>` | E1, E2, E3a, E4a/E4b, E5a/E5b, E7/E6/E8, E22 | CONFIRMED [CODE-VERIFIED]: four space-separated fields, one line per ref. Field 1 can be a source expression (`HEAD`, E6) or `(delete)`, not always a full ref | done |
| D19-22 | 518 | Zero OIDs and `(delete)` are the ordinary values git sends | E1 (create: zero field 4), E3a/E4a/E4b (delete: `(delete)` + zero field 2), E22 (64-zero under SHA-256), E25 (create of `refs/heads/master`) | CONFIRMED [CODE-VERIFIED] | done |
| D19-23 | 518 | An empty stdin stream occurs and is a valid input | E12/E12b (up-to-date), E23 (b) (known non-ff), E27 (a) (stale lease): hook ran with EMPTY stdin | CONFIRMED [CODE-VERIFIED] (the malformed-stream half of design line 518 is guard behaviour; its git side is D19-42) | done |
| D19-25 | 518 | No hardcoded SHA-1 length needed for destination selection | E22 (SHA-256 create/update/delete; 64-char oids, same field 3 text) | CONFIRMED [CODE-VERIFIED] | done |
| D19-28 | 520 | Source-only/configured refspec resolving to protected heads arrives as field 3 = protected ref | E20 (`remote.origin.push=feature:main`, bare `git push origin`), E21 (upstream + `push.default=upstream`), E6 (`HEAD:main`) | CONFIRMED [CODE-VERIFIED] | done |
| D19-30 (local forms) | 520 | `--no-verify`, per-process hooksPath override, direct send-pack bypass local pre-push | E14, E15, E16, E17 (a-c) | CONFIRMED [CODE-VERIFIED]: hook not run in each; E17c force-rewrote `refs/heads/main` with no hook | done |
| D19-30 (API part) | 520 | API/programmatic ref writes (hosting service) bypass local pre-push | none | NOT TESTABLE LOCALLY [UNVERIFIED] | web-01 |
| D19-41 | 530 | Create/update/delete/force, refspec, mapped source-only, mixed (protected last), empty, SHA-format forms reach pre-push with expected field 3 | E1, E2, E3a/E3b, E4a/E4b, E5a/E5b, E6/E7/E8, E12, E19, E20, E21, E22, E24 (a)/(b), E26 | CONFIRMED [CODE-VERIFIED] for every listed form; exact-name edges are D19-27 | done |
| D19-48 | 534 | `--dry-run` sends no updates yet invokes the local pre-push hook with the real records | E13, E13b, E28 (a-c), E30 | CONFIRMED [CODE-VERIFIED]: hook ran with would-be records (including forced `refs/heads/main`), remote refs unchanged | done |
| D19-47 | 534 | Fixture refs must reach pre-push: an up-to-date ref is not sent and a non-fast-forward is rejected before pre-push | E12/E12b, E9, E23 (a)/(b), E27 (a) | CONTRADICTED in part [CODE-CONTRADICTED]: up-to-date and locally known non-ff refs are dropped from stdin (hook still runs, EMPTY stdin), but a "fetch first" non-ff (remote object unknown locally, E23a) DOES reach pre-push with its `refs/heads/main` record before git rejects it | done |
| D19-21 | 518 | A nonzero pre-push exit refuses the entire push (no ref updated) for create, update, delete and force forms | E19 (create + forced), E24 (a)/(b), E26 (a), E27 (b) (forced); fast-forward update and delete under refusal: none | CONFIRMED [CODE-VERIFIED] (F1 adds refused fast-forward update and refused delete of main, each mixed with an unprotected create; remote unchanged) | follow-up below (F1) |
| D19-33 | 524 | Private-worktree eligibility data disappears with git worktree removal | none (file 04 Gaps: removal not exercised) | CONFIRMED [CODE-VERIFIED] for plain `git worktree remove` (F2: private git dir and marker gone). Orca's removal path not tested (design line 524 itself says so) | follow-up below (F2) |
| D19-35 | 524 | A linked worktree's default hook is the shared common-dir file, which stays installed after one worktree is removed | E30 (a)/(b), E1, E18 (lookup only); removal: none | CONFIRMED [CODE-VERIFIED] (F2: hook still present and run by the remaining worktree after removal) | follow-up below (F2) |
| D19-27 (git part) | 520 | `refs/tags/main`, `refs/heads/mainline`, `refs/heads/ma`, `refs/heads/feature/main` arrive as distinct field-3 values, so exact compare leaves them unprotected | E25 (all except `refs/heads/ma`) | CONFIRMED [CODE-VERIFIED] (F3a: field 3 = `refs/heads/ma`) | follow-up below (F3) |
| D19-42 | 530 | Git does not normally send malformed or padded records | none (no malformed record in any file 04 run) | CONFIRMED for the tested scope [CODE-VERIFIED]: F3 shows space/tab/trailing-space destinations are rejected as invalid refspecs before the hook; across all E1-E31 and F1-F3 runs every record had four fields. Whether any git version or transport can emit one is not locally provable | follow-up below (F3) |
| D19-29 (git part) | 520 | L2 (pre-push) adds no local commit/merge restriction | none | CONFIRMED [CODE-VERIFIED] (F4: commit and a no-ff merge into local main succeeded with a refusing hook; hook never ran) | follow-up below (F4) |

### F0. Follow-up sandbox setup

Sandbox created with `SANDBOX=$(mktemp -d /tmp/prepush-followup.XXXXXXXX); echo "$SANDBOX"`, which printed `/tmp/prepush-followup.0OZWoyIi`. Below `S=/tmp/prepush-followup.0OZWoyIi`. Every Bash call began with `export HOME=$S/home GIT_CONFIG_NOSYSTEM=1`; every git command used `-C` inside `$S` and `timeout 20`. The same ambient `GIT_CONFIG_*`/`GIT_TERMINAL_PROMPT` variables noted in E0 were present.

Command block (setup, verbatim):
```bash
S=/tmp/prepush-followup.0OZWoyIi; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1
set -u
mkdir -p $S/home
cat > $S/hook-logging.sh <<'EOF'
#!/bin/bash
# Follow-up logging pre-push hook. Appends to the sandbox log; exit code from $S/hook-exit (default 0).
S=/tmp/prepush-followup.0OZWoyIi
{
  echo "=== HOOK-RUN file=$0"
  echo "argv1=$1"
  echo "argv2=$2"
  n=0
  while IFS= read -r line; do echo "STDIN: $line"; n=$((n+1)); done
  [ "$n" -eq 0 ] && echo "EMPTY-STDIN"
  echo "pwd=$(pwd)"
  echo "=== END"
} >> "$S/hook.log" 2>&1
code=$(cat "$S/hook-exit" 2>/dev/null || echo 0)
[ "$code" != 0 ] && echo "HOOK: refusing push (research exit $code)" >&2
exit "$code"
EOF
cat > $S/x.sh <<'EOF'
#!/bin/bash
# Runner. usage: x.sh <bare-remote> <command...>
S=/tmp/prepush-followup.0OZWoyIi
R=$1; shift
: > "$S/hook.log"
timeout 20 git -C "$R" for-each-ref --format='%(refname) %(objectname)' > "$S/refs-before"
echo "## remote refs before ($R)"; cat "$S/refs-before"
echo "## command: $*"
timeout 20 "$@" > "$S/out" 2>&1; rc=$?
lines=$(wc -l < "$S/out"); head -60 "$S/out"; [ "$lines" -gt 60 ] && echo "[TRUNCATED: $lines lines total, first 60 shown]"
echo "## exit=$rc"
timeout 20 git -C "$R" for-each-ref --format='%(refname) %(objectname)' > "$S/refs-after"
echo "## remote refs after"; cat "$S/refs-after"
if cmp -s "$S/refs-before" "$S/refs-after"; then echo "## REMOTE-REFS-CHANGED: no"; else echo "## REMOTE-REFS-CHANGED: yes"; diff "$S/refs-before" "$S/refs-after"; fi
echo "## hook log"
if [ ! -s "$S/hook.log" ]; then echo "HOOK-NOT-RUN (log empty)"; else head -60 "$S/hook.log"; fi
EOF
chmod +x $S/x.sh $S/hook-logging.sh
echo "## git --version"; timeout 20 git --version
timeout 20 git -c init.defaultBranch=main init --bare $S/remote.git
timeout 20 git clone $S/remote.git $S/clone 2>&1
timeout 20 git -C $S/clone config user.name "Research Bot"
timeout 20 git -C $S/clone config user.email "research@example.invalid"
timeout 20 git -C $S/clone switch -c main 2>&1
echo one > $S/clone/f.txt; timeout 20 git -C $S/clone add f.txt; timeout 20 git -C $S/clone commit -q -m "initial"
echo "## remote -v before first push"; timeout 20 git -C $S/clone remote -v
timeout 20 git -C $S/clone push origin main 2>&1
timeout 20 git -C $S/clone branch dev; timeout 20 git -C $S/clone push origin dev 2>&1
timeout 20 git -C $S/clone worktree add $S/wt -b feature 2>&1
echo two > $S/wt/g.txt; timeout 20 git -C $S/wt add g.txt; timeout 20 git -C $S/wt commit -q -m "feature commit"
echo "## git dirs (wt)"; timeout 20 git -C $S/wt rev-parse --git-dir --git-common-dir --git-path hooks/pre-push
cp $S/hook-logging.sh $S/clone/.git/hooks/pre-push && chmod +x $S/clone/.git/hooks/pre-push
ls -l $S/clone/.git/hooks/pre-push
echo "## global config files in HOME"; ls -a $S/home
echo "## remote refs"; timeout 20 git -C $S/remote.git for-each-ref --format='%(refname) %(objectname)'
```
Output (verbatim):
```text
## git --version
git version 2.47.3
Initialized empty Git repository in /tmp/prepush-followup.0OZWoyIi/remote.git/
Cloning into '/tmp/prepush-followup.0OZWoyIi/clone'...
warning: You appear to have cloned an empty repository.
done.
Switched to a new branch 'main'
## remote -v before first push
origin	/tmp/prepush-followup.0OZWoyIi/remote.git (fetch)
origin	/tmp/prepush-followup.0OZWoyIi/remote.git (push)
To /tmp/prepush-followup.0OZWoyIi/remote.git
 * [new branch]      main -> main
To /tmp/prepush-followup.0OZWoyIi/remote.git
 * [new branch]      dev -> dev
Preparing worktree (new branch 'feature')
HEAD is now at ab8e150 initial
## git dirs (wt)
/tmp/prepush-followup.0OZWoyIi/clone/.git/worktrees/wt
/tmp/prepush-followup.0OZWoyIi/clone/.git
/tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
-rwxr-xr-x 1 coder coder 526 Nov  8 11:33 /tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
## global config files in HOME
.
..
## remote refs
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
```
Observed: git 2.47.3; the only remote is the local bare repo; no global config; the hook was installed only at the common dir after the setup pushes.

### F1. D19-21: one nonzero exit refuses the whole push for fast-forward update and delete forms (mixed with an unprotected create)

File 04 covered create plus forced update (E19), mixed creates/updates (E24, E26) and a forced lease rewrite (E27b) under refusal, but no refused **fast-forward update** or **delete** of main. F1 fills that.

Command block (verbatim):
```bash
S=/tmp/prepush-followup.0OZWoyIi; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1; X=$S/x.sh; R=$S/remote.git
echo 1 > $S/hook-exit
echo "######## F1a hook exit 1: fast-forward feature:main + create side"; $X $R git -C $S/wt push origin feature:main feature:refs/heads/side
echo "######## setup: move bare HEAD to dev"; timeout 20 git -C $R symbolic-ref HEAD refs/heads/dev; timeout 20 git -C $R symbolic-ref HEAD
echo "######## F1b hook exit 1: delete :main + create side"; $X $R git -C $S/wt push origin :main feature:refs/heads/side
echo 0 > $S/hook-exit
echo "######## F1c control, hook exit 0: delete :main"; $X $R git -C $S/wt push origin :main
echo "######## restore: recreate main, bare HEAD back to main"; timeout 20 git -C $S/clone push origin main 2>&1; timeout 20 git -C $R symbolic-ref HEAD refs/heads/main; timeout 20 git -C $R for-each-ref --format='%(refname) %(objectname)'
```
Output, including remote refs before/after and the hook log (verbatim):
```text
######## F1a hook exit 1: fast-forward feature:main + create side
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt push origin feature:main feature:refs/heads/side
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-followup.0OZWoyIi/remote.git'
## exit=1
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-followup.0OZWoyIi/remote.git
STDIN: refs/heads/feature e2c193113156e8d4d7a9fdb0e67d5da8fbc4742b refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
STDIN: refs/heads/feature e2c193113156e8d4d7a9fdb0e67d5da8fbc4742b refs/heads/side 0000000000000000000000000000000000000000
pwd=/tmp/prepush-followup.0OZWoyIi/wt
=== END
######## setup: move bare HEAD to dev
refs/heads/dev
######## F1b hook exit 1: delete :main + create side
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt push origin :main feature:refs/heads/side
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-followup.0OZWoyIi/remote.git'
## exit=1
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-followup.0OZWoyIi/remote.git
STDIN: (delete) 0000000000000000000000000000000000000000 refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
STDIN: refs/heads/feature e2c193113156e8d4d7a9fdb0e67d5da8fbc4742b refs/heads/side 0000000000000000000000000000000000000000
pwd=/tmp/prepush-followup.0OZWoyIi/wt
=== END
######## F1c control, hook exit 0: delete :main
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt push origin :main
To /tmp/prepush-followup.0OZWoyIi/remote.git
 - [deleted]         main
## exit=0
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: yes
2d1
< refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## hook log
=== HOOK-RUN file=/tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-followup.0OZWoyIi/remote.git
STDIN: (delete) 0000000000000000000000000000000000000000 refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
pwd=/tmp/prepush-followup.0OZWoyIi/wt
=== END
######## restore: recreate main, bare HEAD back to main
To /tmp/prepush-followup.0OZWoyIi/remote.git
 * [new branch]      main -> main
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
```
Observed result: a single exit 1 refused both the fast-forward update of `refs/heads/main` and the delete of `refs/heads/main`, each together with an unprotected create, leaving remote refs unchanged; the exit-0 control shows the same delete is otherwise accepted (main removed), so the hook was the only stopper. With E19/E24/E26/E27b, D19-21 holds for create, update, delete and force forms [CODE-VERIFIED].

### F2. D19-33 / D19-35: `git worktree remove` deletes the private git dir (marker included) but leaves the shared common-dir hook

File 04 measured hook lookup (E30) but never removed a worktree (its Gaps list this). F2 uses plain `git worktree remove`; Orca's own removal was not exercised.

Command block (verbatim):
```bash
S=/tmp/prepush-followup.0OZWoyIi; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1; X=$S/x.sh; R=$S/remote.git
echo 0 > $S/hook-exit
echo "######## F2 setup: second linked worktree wt2 + marker in its private git dir"
timeout 20 git -C $S/clone worktree add $S/wt2 -b w2 2>&1
timeout 20 git -C $S/wt2 rev-parse --git-dir --git-common-dir --git-path hooks/pre-push
echo "eligible" > $S/clone/.git/worktrees/wt2/l2-marker
ls -a $S/clone/.git/worktrees/wt2
echo "## worktree list before"; timeout 20 git -C $S/clone worktree list
echo "######## F2a git worktree remove wt2"; timeout 20 git -C $S/clone worktree remove $S/wt2 2>&1; echo "rc=$?"
echo "## worktree list after"; timeout 20 git -C $S/clone worktree list
echo "## private git dir after"; ls -a $S/clone/.git/worktrees/wt2 2>&1; ls -d $S/wt2 2>&1
echo "## shared hook after"; ls -l $S/clone/.git/hooks/pre-push
echo "######## F2b push from remaining worktree wt after removal (dry-run)"; $X $R git -C $S/wt push --dry-run origin feature:refs/heads/after-remove
```
Output, including remote refs before/after and the hook log (verbatim):
```text
######## F2 setup: second linked worktree wt2 + marker in its private git dir
Preparing worktree (new branch 'w2')
HEAD is now at ab8e150 initial
/tmp/prepush-followup.0OZWoyIi/clone/.git/worktrees/wt2
/tmp/prepush-followup.0OZWoyIi/clone/.git
/tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
.
..
HEAD
ORIG_HEAD
commondir
gitdir
index
l2-marker
logs
refs
## worktree list before
/tmp/prepush-followup.0OZWoyIi/clone  ab8e150 [main]
/tmp/prepush-followup.0OZWoyIi/wt     e2c1931 [feature]
/tmp/prepush-followup.0OZWoyIi/wt2    ab8e150 [w2]
######## F2a git worktree remove wt2
rc=0
## worktree list after
/tmp/prepush-followup.0OZWoyIi/clone  ab8e150 [main]
/tmp/prepush-followup.0OZWoyIi/wt     e2c1931 [feature]
## private git dir after
ls: cannot access '/tmp/prepush-followup.0OZWoyIi/clone/.git/worktrees/wt2': No such file or directory
ls: cannot access '/tmp/prepush-followup.0OZWoyIi/wt2': No such file or directory
## shared hook after
-rwxr-xr-x 1 coder coder 526 Nov  8 11:33 /tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
######## F2b push from remaining worktree wt after removal (dry-run)
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt push --dry-run origin feature:refs/heads/after-remove
To /tmp/prepush-followup.0OZWoyIi/remote.git
 * [new branch]      feature -> after-remove
## exit=0
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-followup.0OZWoyIi/remote.git
STDIN: refs/heads/feature e2c193113156e8d4d7a9fdb0e67d5da8fbc4742b refs/heads/after-remove 0000000000000000000000000000000000000000
pwd=/tmp/prepush-followup.0OZWoyIi/wt
=== END
```
Observed result: `git worktree remove` (rc 0) deleted the worktree's private git dir `clone/.git/worktrees/wt2`, including the `l2-marker` file, while the shared `clone/.git/hooks/pre-push` (which wt2's `--git-path hooks/pre-push` resolved to) stayed installed and still ran for the remaining worktree [CODE-VERIFIED for plain git 2.47.3; Orca removal not tested].

### F3. D19-27 / D19-42: `refs/heads/ma` reaches the hook as its own field 3; space-padded destinations are rejected before the hook

E25 covered `mainline`, `main2`, `feature/main`, `tags/main`, `Main` and `master`, but not `refs/heads/ma` (file 04 Gaps). D19-42 ("Git does not normally send malformed or padded records") had no experiment. In F3a the research hook refuses every push (exit 1) only so the record is visible without moving a ref; it does not mean `ma` is protected.

Command block (verbatim):
```bash
S=/tmp/prepush-followup.0OZWoyIi; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1; X=$S/x.sh; R=$S/remote.git
echo "######## F3 check-ref-format"
for n in 'refs/heads/ma' 'refs/heads/a b' 'refs/heads/ma ' $'refs/heads/a\tb'; do timeout 20 git -C $S/wt check-ref-format "$n"; echo "check-ref-format [$n] rc=$?"; done
echo 1 > $S/hook-exit
echo "######## F3a hook exit 1: push to refs/heads/ma"; $X $R git -C $S/wt push origin feature:refs/heads/ma
echo 0 > $S/hook-exit
echo "######## F3b hook exit 0: destination with a space"; $X $R git -C $S/wt push origin 'feature:refs/heads/a b'
echo "######## F3c hook exit 0: destination with a trailing space"; $X $R git -C $S/wt push origin 'feature:refs/heads/ma '
```
Output, including remote refs before/after and the hook log (verbatim; the tab case prints a literal tab inside the brackets):
```text
######## F3 check-ref-format
check-ref-format [refs/heads/ma] rc=0
check-ref-format [refs/heads/a b] rc=1
check-ref-format [refs/heads/ma ] rc=1
check-ref-format [refs/heads/a	b] rc=1
######## F3a hook exit 1: push to refs/heads/ma
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt push origin feature:refs/heads/ma
HOOK: refusing push (research exit 1)
error: failed to push some refs to '/tmp/prepush-followup.0OZWoyIi/remote.git'
## exit=1
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
=== HOOK-RUN file=/tmp/prepush-followup.0OZWoyIi/clone/.git/hooks/pre-push
argv1=origin
argv2=/tmp/prepush-followup.0OZWoyIi/remote.git
STDIN: refs/heads/feature e2c193113156e8d4d7a9fdb0e67d5da8fbc4742b refs/heads/ma 0000000000000000000000000000000000000000
pwd=/tmp/prepush-followup.0OZWoyIi/wt
=== END
######## F3b hook exit 0: destination with a space
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt push origin feature:refs/heads/a b
fatal: invalid refspec 'feature:refs/heads/a b'
## exit=128
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
######## F3c hook exit 0: destination with a trailing space
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt push origin feature:refs/heads/ma 
fatal: invalid refspec 'feature:refs/heads/ma '
## exit=128
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
```
Observed result: `refs/heads/ma` arrives as field 3 exactly `refs/heads/ma` (so an exact compare does not match it); ref names with a space, trailing space or tab fail `check-ref-format` and a push naming them dies with `fatal: invalid refspec` (exit 128) before the hook runs, so git cannot be made to send a padded or extra-field record through a destination name [CODE-VERIFIED on git 2.47.3; "never, in any version or transport" is not provable locally].

### F4. D19-29 (git part): pre-push adds no local commit or merge restriction, even on local main

Design line 520 says L2 "adds no local commit/merge restriction". The git side of that is whether pre-push fires on local commits or merges. The hook was set to refuse (exit 1) for all of F4. Two Bash calls were made: F4a/F4b, then F4c, because F4b turned out to be a no-op (see result).

Command block 1 (verbatim):
```bash
S=/tmp/prepush-followup.0OZWoyIi; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1; X=$S/x.sh; R=$S/remote.git
echo 1 > $S/hook-exit
echo "## wt HEAD before"; timeout 20 git -C $S/wt rev-parse HEAD
echo three > $S/wt/h.txt; timeout 20 git -C $S/wt add h.txt
echo "######## F4a hook exit 1: local commit in wt"; $X $R git -C $S/wt commit -q -m "local commit under refusing pre-push"
echo "######## F4b hook exit 1: local merge of main into feature (no-ff)"; $X $R git -C $S/wt merge --no-ff -q -m "local merge under refusing pre-push" main
echo "## wt HEAD after"; timeout 20 git -C $S/wt log --oneline -3
echo 0 > $S/hook-exit
```
Output 1, including remote refs before/after and the hook log (verbatim):
```text
## wt HEAD before
e2c193113156e8d4d7a9fdb0e67d5da8fbc4742b
######## F4a hook exit 1: local commit in wt
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt commit -q -m local commit under refusing pre-push
## exit=0
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
######## F4b hook exit 1: local merge of main into feature (no-ff)
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/wt merge --no-ff -q -m local merge under refusing pre-push main
## exit=0
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
## wt HEAD after
37236d5 local commit under refusing pre-push
e2c1931 feature commit
ab8e150 initial
```
F4b created no merge commit (main is an ancestor of feature, so the merge was already up to date), so a real merge was run next.

Command block 2 (verbatim):
```bash
S=/tmp/prepush-followup.0OZWoyIi; export HOME=$S/home GIT_CONFIG_NOSYSTEM=1; X=$S/x.sh; R=$S/remote.git
echo 1 > $S/hook-exit
echo "## clone local main before"; timeout 20 git -C $S/clone rev-parse main
echo "######## F4c hook exit 1: local no-ff merge of feature into local main (clone)"; $X $R git -C $S/clone merge --no-ff -m "local merge into main under refusing pre-push" feature
echo "## clone local main after"; timeout 20 git -C $S/clone log --oneline --graph -4 main
echo 0 > $S/hook-exit
```
Output 2, including remote refs before/after and the hook log (verbatim):
```text
## clone local main before
ab8e1505b48d7bccf730149b0cdca3ae1b528b83
######## F4c hook exit 1: local no-ff merge of feature into local main (clone)
## remote refs before (/tmp/prepush-followup.0OZWoyIi/remote.git)
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## command: git -C /tmp/prepush-followup.0OZWoyIi/clone merge --no-ff -m local merge into main under refusing pre-push feature
Merge made by the 'ort' strategy.
 g.txt | 1 +
 h.txt | 1 +
 2 files changed, 2 insertions(+)
 create mode 100644 g.txt
 create mode 100644 h.txt
## exit=0
## remote refs after
refs/heads/dev ab8e1505b48d7bccf730149b0cdca3ae1b528b83
refs/heads/main ab8e1505b48d7bccf730149b0cdca3ae1b528b83
## REMOTE-REFS-CHANGED: no
## hook log
HOOK-NOT-RUN (log empty)
## clone local main after
*   6ada794 local merge into main under refusing pre-push
|\  
| * 37236d5 local commit under refusing pre-push
| * e2c1931 feature commit
|/  
* ab8e150 initial
```
Observed result: with a refusing pre-push installed, a local commit (wt) and a local no-ff merge into local `main` (clone) both succeeded and the hook never ran; pre-push restricts only pushes, so L2 adds no local commit/merge restriction [CODE-VERIFIED]. The "does not know the correct remote" half is consistent with E1/E11 (argv carries only the remote name and URL as given) and is a design statement, not a git behaviour.

### Follow-up sandbox removal

Command block (verbatim):
```bash
SANDBOX=/tmp/prepush-followup.0OZWoyIi; rm -rf -- "$SANDBOX"; echo "rm rc=$?"; ls -d "$SANDBOX"; echo "ls rc=$?"
```
Output (verbatim):
```text
rm rc=0
ls: cannot access '/tmp/prepush-followup.0OZWoyIi': No such file or directory
ls rc=2
```
Observed: the follow-up sandbox (bare remote, clone, worktrees, hook copies, logs) is gone. No git command ran inside the IronClaude repository or against any real or network remote; no hosting service was contacted.

**Cross-check tally:** 17 rows. CONFIRMED [CODE-VERIFIED]: 15 (D19-2, 20, 21, 22, 23, 25, 27 git part, 28, 29 git part, 30 local forms, 33, 35, 41, 42, 48; of these D19-21, 27, 29, 33, 35 and 42 were settled by follow-ups F1-F4). CONTRADICTED in part [CODE-CONTRADICTED]: 1 (D19-47, "fetch first" non-ff reaches pre-push). NOT TESTABLE LOCALLY [UNVERIFIED]: 1 (D19-30 API part), routed to web-01.

## Key Takeaways

Added in the Gate 1 cycle 0 fix. Every bullet restates an observation already recorded above on git 2.47.3; no new experiment was run for this list.

- **Field 3 is authoritative.** It is always the fully qualified destination ref, also for `HEAD:main` (E6), configured `remote.origin.push` refspecs (E20), upstream mappings (E21), `--mirror` (E11), deletes (E3/E4) and forced updates, which carry no force marker (E5). An exact compare against `refs/heads/main` / `refs/heads/master` is enough; field 1 is not always a full ref (`HEAD`, `(delete)`).
- **Empty stdin is a real input.** The hook runs with zero records for an up-to-date push (E12), a locally known non-fast-forward (E23b) and a stale lease (E27a). A "fetch first" non-fast-forward still delivers its record (E23a).
- **One nonzero exit aborts the whole push.** E19 and E24 refused mixed protected and unprotected updates together, `--atomic` or not (E26); F1 confirmed this for update and delete forms.
- **`--dry-run` runs the hook** with the real would-be records and moves no refs (E13), so it can exercise a guard but cannot replace ref-state assertions.
- **The bypass set.** `--no-verify` (E14), a per-process `-c core.hooksPath=...` (E15/E16), `git send-pack` (E17, which force-rewrote `refs/heads/main` with no hook call), a non-executable hook that fails open with a suppressible hint (E29), and a per-worktree `core.hooksPath` via `extensions.worktreeConfig` (E31). None of these needs anything that git itself flags as an error.
- **Placement is the common git dir.** A linked worktree's default hook lookup is `clone/.git/hooks/pre-push`; a hook in the worktree-private git dir is ignored (E30). An installer must use `git rev-parse --git-path hooks/pre-push`, never `--git-dir`/hooks. `git worktree remove` deletes a private-dir marker while the shared hook stays (F2).
- **The environment passes through unchanged.** HOME (even unset), PATH (with `/usr/lib/git-core` prepended), marker variables, `CCSESSION_LAUNCH_ID` and `CLAUDECODE` all come from the pusher (E28), so none is authority.
- **The uv PATH gap.** With `PATH=/usr/lib/git-core:/usr/bin:/bin`, uv was not resolvable in the hook (E28c). Because `launch-job-identity.sh` resolves uv through PATH at lines 25 and 566, the hook must set a fixed PATH containing the install-time uv directory or not depend on uv at all; otherwise `identify` exits 2, which is treated as `unknown`, and a human whose PATH lacks uv cannot push to `main`/`master` (01 §4 item 5).
- **Pre-push restricts only pushes.** Local commits and merges into `main` succeed under a refusing hook (F4).

## Gaps and Questions

- [UNVERIFIED] **Stdin record order rule.** E9, E19 and E24 show that order is not command order. "Existing remote refs first, then new refs" is inferred from three observations, not documented. The design (§19.3) already says not to depend on order, so the gap does not affect it.
- [UNVERIFIED] **Case-folding.** `refs/heads/Main` reaches the hook as a distinct field 3 (E25). Whether a case-insensitive remote filesystem, or a hosting service, would store it as `main` was not tested.
- [UNVERIFIED] **`git rev-parse --path-format=absolute --git-path hooks/pre-push`** was not exercised. Only the relative/absolute forms printed by plain `--git-path` were measured (E30a).
- [UNVERIFIED] **Network transports.** Every push used the local file transport. Behaviour over SSH/HTTPS was not tested: hook timing, the "fetch first" versus non-fast-forward filtering (E23), and what the remote advertises.
- [UNVERIFIED] Design §19.3 "A malformed governed stream (missing/extra fields) refuses": git never produced a malformed record here. Only synthetic direct-hook input could test it, and that was out of scope.
- [UNVERIFIED] Design §19.3 line 520 "API/programmatic ref writes can bypass local pre-push": not exercised. Only `send-pack` (E17), `--no-verify` (E14) and hooksPath overrides (E15/E16) were.
- [UNVERIFIED] Design §19.3 line 520 lists `refs/heads/ma` as unprotected. That exact name was not pushed. `mainline`, `main2`, `feature/main`, `tags/main` and `Main` were (E25).
- [UNVERIFIED] Design §19.4 "Private-worktree eligibility data may disappear with Git worktree removal": worktree removal was not exercised.
- [UNVERIFIED] Design §19.1 actor selection (process ancestry, B-CTX) is outside this file's scope. E1 recorded one data point: the hook's session id matched the Bash tool shell, whose parent `claude` process ran in a different session. No lifecycle variants were observed.
- **Open question for the design:** E29 and E31 show two install-integrity holes that a same-user agent can open without any visible push flag. One is clearing the executable bit, which fails open, and `-c advice.ignoredHook=false` silences the hint. The other is a per-worktree `core.hooksPath` via `extensions.worktreeConfig`. §19.2/§19.5 already require checking "effective hook presence/executable ownership". The design should say whether that check runs only at install or also before each governed launch.
- **Open question:** E28c shows that a hook resolving `uv` by bare name fails when PATH lacks `/usr/local/bin`. Should the L2 hook be pure shell (no uv), or should it set a fixed PATH that contains the uv directory recorded at install time? (Corrected in the Gate 1 cycle 0 fix: calling uv by absolute path alone is not enough, because `launch-job-identity.sh` resolves uv through PATH at line 25 and line 566; see 01 §4 item 5.)
- No item in experiments E0-E31 is tagged [CODE-CONTRADICTED]. The Step 2.5 cross-check tags one claim of file 03 [CODE-CONTRADICTED] (next item).
- [CODE-CONTRADICTED] D19-47 (design line 534), as paraphrased in file 03 ("an up-to-date ref is not sent to pre-push and a non-fast-forward is rejected before pre-push runs"): observed in E23a that a "fetch first" non-fast-forward (remote object not present locally) DOES reach pre-push with its `refs/heads/main` record and is rejected by git only afterwards; only up-to-date refs, locally known non-fast-forwards (E23b, E9) and stale leases (E27a) are dropped from stdin, and even then the hook still runs with EMPTY stdin. The design sentence itself is incomplete rather than wrong (see Stale Documentation Found).
- Step 2.5 resolved two items above: `refs/heads/ma` reaches the hook as its own field 3 (F3a), and plain `git worktree remove` deletes the private git dir including a marker while the shared hook stays (F2). Orca's removal path remains untested.
- [UNVERIFIED] D19-42 (design line 530) beyond the tested scope: F3 shows git refuses space/tab/trailing-space destination names before the hook, and no run produced a malformed record, but "git never sends one in any version or transport" cannot be proven locally.
- ROUTE web-01: D19-30 (design line 520): API/programmatic ref writes (for example a hosting service's ref-update API) bypass the local pre-push hook; not testable locally and not tested against any network service.
- ROUTE web-01: (b) other tools. Added in the Gate 1 cycle 0 fix. Whether a push made through a library, rather than the `git` binary, runs the client-side pre-push hook is open for every library below [UNVERIFIED]; only `git push` (E1-E31) and `git send-pack` (E17, never runs it) were tested. A local test was not possible: a read-only check found none of `dulwich`, `pygit2` or `GitPython` in the project environment (`uv pip list` matched none of them), none under the uv cache paths checked (`~/.cache/uv/wheels-v*/pypi/<name>` and `~/.cache/uv/archive-v0/*/<name>`) or in `/usr/lib/python3/dist-packages`, and no `jgit` or `java` on PATH; the fix rules forbid network installs. Phase 4 (web-01) should answer, per library, "does its push run `hooks/pre-push`, and from which hooks directory", from that library's own documentation or source:
  - **pygit2 / libgit2**: pygit2's `Remote.push` documentation (pygit2.org) and libgit2's `git_remote_push` API reference and source (libgit2.org, github.com/libgit2/libgit2).
  - **dulwich**: dulwich's `porcelain.push` documentation and its `dulwich/hooks.py` source (dulwich.io, github.com/jelmer/dulwich), to see which hook names it implements.
  - **GitPython**: GitPython's `Remote.push` documentation (gitpython.readthedocs.io). If it runs the `git` binary for push, as is commonly stated, E1-E31 then apply to it; that is itself [UNVERIFIED] until the documentation or source is read.
  - **JGit**: JGit's `PushCommand` and hooks documentation (eclipse.dev/jgit, github.com/eclipse-jgit/jgit), to see whether it runs a pre-push hook and whether it honours `core.hooksPath`.
  These are suggested source locations; none was fetched in this fix. L1 coverage of these calls is in 02 §7 (line 187, PARTIAL) and 02 Gap 6.

## Stale Documentation Found

- None contradicted. Every design statement tested here held on git 2.47.3: §19.3 lines 518 and 520, §19.5 line 534, and the pass-through premise of §19.1 line 493.
- Incomplete, not stale: design §19.5 line 534 "(not up-to-date/nonfastforward rejection)". A non-fast-forward rejected as "fetch first" (remote object not present locally) **does** reach pre-push with its record (E23a). Only the locally known non-fast-forward (E23b), the stale lease (E27a) and up-to-date refs are dropped from stdin. Fixture authors should not assume every rejected ref is invisible to the hook.

## Summary

On git 2.47.3, pre-push runs once per `git push` from the common-dir hook, also for linked worktrees; a hook in the worktree-private git dir is ignored. It receives argv1 = remote name (or the URL itself), argv2 = URL, and one `<local-ref> <local-oid> <remote-ref> <remote-oid>` record per ref git will send. Field 3 is always the fully qualified destination, also for `HEAD:main`, configured push refspecs, upstream mappings, `--mirror`, deletes and forced updates. Exact comparison against `refs/heads/main`/`refs/heads/master` is therefore sufficient and position-independent, and oids are 64 characters under SHA-256. Up-to-date refs, locally detected non-fast-forwards and stale leases are dropped from stdin (the hook still runs, possibly with EMPTY stdin), while `--dry-run` delivers the real records without moving refs. A single nonzero exit aborts the whole push, `--atomic` or not. The hook inherits the pusher's entire environment: HOME (even unset), PATH (with `/usr/lib/git-core` prepended), marker variables, `CCSESSION_LAUNCH_ID` and `CLAUDECODE`. None of these is authority, and uv may be absent from the hook's PATH. The hook is bypassed silently by `--no-verify`, a per-process or per-worktree `core.hooksPath`, `git send-pack`, or a missing executable bit (fail-open, hint suppressible), so install integrity must be checked independently of git's own warnings.

Step 2.5 cross-checked the 16 git-behaviour claims that file 03 left [UNVERIFIED] (14 `UNVERIFIED-GIT` lines plus the git parts of D19-27 and D19-29) in 17 table rows, D19-30 being split into local and API parts: 15 rows are confirmed (6 of them by new sandbox follow-ups F1-F4), D19-47 is contradicted in part because a "fetch first" non-fast-forward still reaches pre-push, and the API/programmatic-write part of D19-30 is routed to web-01.
