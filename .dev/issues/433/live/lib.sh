#!/usr/bin/env bash
# Helpers for the Coder #433 live check: a throwaway workspace container booted and restarted with
# the orca-port-tools harness (live-boot.sh; KEEP_VOLUMES=1 recreates the container on the same
# volumes, as a Coder workspace restart does). Source this file, then call the functions.
# The gateway key is copied from this shell's environment into the container's /dev/shm (memory
# only, 0600) and is never printed; the container and its /dev/shm are removed by cc_down.
# Never point these at the owner's own workspace: every command targets the test container $CTR.
T=/home/coder/workspaces/worktrees/orca-port-tools
O=/home/coder/.local/bin/orca
REPO=/home/coder/workspaces/agents-demo
GATEWAY=http://192.168.133.101:4000/cli
SKILL_SRC=/home/coder/workspaces/worktrees/IronClaude/433-ccsession-orca-resume/src/superclaude/skills/ccsession-tag
: "${IMG:=aidev02-412:local}" "${CTR:=cc433}" "${EV:=/tmp/cc433-ev}"
export NETNS=$CTR-net

X() { docker exec -u coder -e HOME=/home/coder -e PATH=/home/coder/.local/bin:/usr/local/bin:/usr/bin:/bin "$CTR" "$O" "$@"; }
D() { docker exec -u coder -e HOME=/home/coder -e PATH=/home/coder/.local/bin:/usr/local/bin:/usr/bin:/bin "$CTR" "$@"; }
screen() { X terminal read --terminal "$1" --screen --json 2>/dev/null | python3 -c "
import json,sys
t=json.load(sys.stdin)['result']; t=t.get('terminal',t)
rows=t.get('screen') or t.get('rows') or t.get('tail') or []
rows=rows.splitlines() if isinstance(rows,str) else rows
print('\n'.join(l for l in rows if l.strip()))"; }
idle() { X terminal wait --terminal "$1" --for tui-idle --timeout-ms "${2:-20000}" --json > /dev/null 2>&1; }

# The container's memory-only key file and the models stand-in, needed after every boot.
cc_key() {
  docker exec -u coder -e LITELLM_API_KEY "$CTR" python3 -c "
import os; p='/dev/shm/aidev-test-key'; fd=os.open(p, os.O_WRONLY|os.O_CREAT|os.O_TRUNC, 0o600)
os.write(fd, os.environ.get('LITELLM_API_KEY','').encode()); os.close(fd)"
  docker cp "$T/models-stub-forwarder.py" "$CTR:/tmp/models-stub-forwarder.py"
  docker exec -d -u coder "$CTR" python3 /tmp/models-stub-forwarder.py 4999 "$GATEWAY"
}

# ccsession reads ~/.claude/ccsession.env; the test fixture there takes the key from /dev/shm by
# path (the file never holds it) and waits for it after a restart, before Claude starts.
cc_envfile() {
  D bash -c 'f=$HOME/.claude/ccsession.env; touch "$f"; grep -q cc433-fixture "$f" || cat >> "$f" <<"EOF"
# cc433-fixture (test container only): key from memory, gateway through the local models stand-in
case " $* " in *" --ask "*) : ;; *)
  for _i in $(seq 1 180); do [ -s /dev/shm/aidev-test-key ] && break; sleep 1; done ;;
esac
export LITELLM_API_KEY="$(cat /dev/shm/aidev-test-key 2>/dev/null)"
export ANTHROPIC_BASE_URL=http://127.0.0.1:4999
EOF'
}

# Put this worktree's ccsession skill (or another folder) over the container's installed copy.
cc_skill() {
  local src=${1:-$SKILL_SRC}
  docker exec -u coder "$CTR" rm -rf /tmp/ccs-new
  docker cp "$src" "$CTR:/tmp/ccs-new"
  docker exec -u 0 "$CTR" chown -R coder:coder /tmp/ccs-new
  D bash -c 'd=$HOME/.claude/skills/ccsession-tag; cp -a /tmp/ccs-new/. "$d"/ && chmod 0755 "$d/ccsession" "$d/ccsession-orca" "$d"/hooks/*.sh'
}

cc_boot() {
  docker rm -f "$NETNS" > /dev/null 2>&1
  docker run -d --name "$NETNS" --entrypoint sleep "$IMG" infinity > /dev/null
  LIVE_OWNER=clay LIVE_ROLES=auditor,member,user-admin "$T/live-boot.sh" "$IMG" "$CTR" "$EV/boot"
}

cc_restart() {
  KEEP_VOLUMES=1 LIVE_OWNER=clay LIVE_ROLES=auditor,member,user-admin "$T/live-boot.sh" "$IMG" "$CTR" "$EV/reboot-$(date +%s)"
}

cc_repo() {
  D git -c init.defaultBranch=main init -q "$REPO"
  docker exec -u coder -e HOME=/home/coder -w "$REPO" "$CTR" git -c user.name=t -c user.email=t@invalid commit -q --allow-empty -m init
  X repo add --path "$REPO" --json > /dev/null 2>&1
}

# The non-secret Orca identifiers and the command line of a process in the container.
cc_proc() {
  docker exec "$CTR" python3 -c "
import sys
pid=sys.argv[1]
env=dict(l.split('=',1) for l in open(f'/proc/{pid}/environ','rb').read().decode(errors='replace').split('\0') if '=' in l)
print('cmdline:', open(f'/proc/{pid}/cmdline','rb').read().decode(errors='replace').replace('\0',' '))
for k in ('ORCA_PANE_KEY','ORCA_TAB_ID','ORCA_TERMINAL_HANDLE','ORCA_AGENT_PANE','ORCA_AGENT_LAUNCH','ORCA_WORKTREE_ID','ORCA_RUNTIME_SOURCE_INCARNATION','CCSESSION_AUTOSTART'):
    print(f'  {k}={env.get(k,\"<unset>\")}')" "$1"
}
# Process ids of ccsession-orca, ccsession and claude in the container.
cc_ps() { docker exec "$CTR" ps -eo pid,ppid,args | grep -E 'ccsession|[c]laude ' | grep -v -E 'grep|local-gateway|models-stub' ; }

# Open a Claude tab the way "+ Claude" does; prints its terminal handle.
cc_new_tab() {
  X agent launch --agent claude --worktree "path:$REPO" --surface terminal "$@" --json |
    python3 -c "import json,sys; print(json.load(sys.stdin)['result']['outcome']['handle'])"
}

# Answer the name question in a new Claude tab ("" = Enter, untagged), clear Claude Code's
# first-run screens (folder trust), then send one message and wait for the reply.
cc_start_tab() {
  local h=$1 name=$2 msg=$3 s
  for _ in $(seq 1 30); do grep -q "Session name" <<< "$(screen "$h")" && break; sleep 1; done
  if [ -n "$name" ]; then X terminal send --terminal "$h" --text "$name" --enter --json > /dev/null
  else X terminal send --terminal "$h" --enter --json > /dev/null; fi
  for _ in 1 2 3 4 5 6 7; do
    idle "$h" 15000; s=$(screen "$h")
    if grep -q "Yes, I trust this folder" <<< "$s"; then
      grep -q "❯ Yes, I trust" <<< "$s" || X terminal send --terminal "$h" --text $'\x1b[B' --json > /dev/null
      idle "$h" 2000; X terminal send --terminal "$h" --enter --json > /dev/null
    elif grep -qE "bypass permissions on|^❯ *$" <<< "$s"; then break
    else X terminal send --terminal "$h" --enter --json > /dev/null; fi
  done
  X terminal send --terminal "$h" --text "$msg" --enter --json > /dev/null
  sleep 5; idle "$h" 120000
}

# The Orca tab records ccsession keeps (session id, folder, terminal handle per pane).
cc_records() { D bash -c 'for f in ~/.local/state/ccsession/orca-tabs/*; do [ -f "$f" ] && echo "$(basename "$f"): $(tr "\n" " " < "$f")"; done'; }

cc_down() {
  docker exec "$CTR" rm -f /dev/shm/aidev-test-key > /dev/null 2>&1
  docker rm -f "$CTR" "$NETNS" > /dev/null 2>&1
  docker volume rm -f "$CTR-home" "$CTR-workspace" > /dev/null 2>&1
}
