#!/usr/bin/env bash
# setup.sh — runbook §1.1-§1.3: preconditions, baselines, session A's isolated HOME.
# Plan Task 2. OB overrides the scratch root (self-test); all writes stay under $OB.
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
T=${OB_TIMEOUT_S:-60}

resume=0
case "${1:-}" in
  --resume) resume=1 ;;
  "") ;;
  *) printf 'usage: setup.sh [--resume]\n' >&2; exit 2 ;;
esac
if [ -e "$OB" ] && [ "$resume" -ne 1 ]; then
  printf 'REFUSE: %s already exists (rerun with --resume)\n' "$OB" >&2
  exit 2
fi

timeout "$T" mkdir -p "$OB_BIN" "$OB_LOGS" "$OB_HOME/.claude/hooks" "$OB_SCREENS"
MAIN=$(main_checkout)
ROOT=$(cd -- "$here/../../../.." && pwd)   # this script's own checkout (holds the fixtures)
PRE=$OB/preconditions.txt
: > "$PRE"

run_check() {  # run_check <id> <cmd...> — append command output + rc to preconditions
  local id=$1; shift
  printf '== %s\n' "$id" >> "$PRE"
  timeout "$T" "$@" >> "$PRE" 2>&1
  printf 'rc=%s\n' "$?" >> "$PRE"
}

# --- §1.1 P1-P8 -------------------------------------------------------------
run_check P1a timeout "$T" claude --version
run_check P1b timeout "$T" orca --version
run_check P1c timeout "$T" git --version
run_check P1d timeout "$T" jq --version
run_check P1e timeout "$T" uv --version
gh_fork --version >> "$PRE" 2>&1 || true
printf 'rc=%s\n' "$?" >> "$PRE"
run_check P2 grep -m1 launch-level-guard-version "$HOME/.claude/hooks/launch-level-guard.sh"
printf '== P3\n' >> "$PRE"
{ timeout "$T" cmp "$HOME/.claude/hooks/launch-level-guard.sh" "$ROOT/src/superclaude/hooks/scripts/launch-level-guard.sh" \
  && timeout "$T" cmp "$HOME/.claude/hooks/launch-job-identity.sh" "$ROOT/src/superclaude/hooks/scripts/launch-job-identity.sh" \
  && printf 'same\n'; printf 'rc=%s\n' "$?"; } >> "$PRE" 2>&1
run_check P4 jq -c '[.hooks|to_entries[]|{e:.key,m:[.value[]|select(any(.hooks[];.command|test("launch-level-guard|launch-job-identity")))|.matcher]}|select(.m|length>0)]' "$HOME/.claude/settings.json"
{ printf '== P5\n'; printenv CLAUDE_CONFIG_DIR; printf 'rc=%s\n' "$?"; } >> "$PRE"
printf '== P6\n' >> "$PRE"
( cd "$ROOT/src/superclaude/skills/sc-issue-protocol/scripts" \
  && timeout 120 uv run --no-project python -I -c "import sys; sys.path.insert(0,'.'); import orca_worktree as o; print(o.enforcement_preflight('$ROOT'))" ) >> "$PRE" 2>&1
printf 'rc=%s\n' "$?" >> "$PRE"
printf '== P7\n' >> "$PRE"
gh_fork repo view IronbellyOrg/IronClaude --json nameWithOwner -q .nameWithOwner >> "$PRE" 2>&1
printf 'rc=%s\n' "$?" >> "$PRE"
timeout "$T" git remote get-url origin >> "$PRE" 2>&1
printf 'rc=%s\n' "$?" >> "$PRE"
printf '== P8\n' >> "$PRE"
gh_fork api repos/IronbellyOrg/IronClaude/branches/master --jq '{protected}' >> "$PRE" 2>&1
printf 'rc=%s\n' "$?" >> "$PRE"

# --- §1.2 baselines (read-only) ----------------------------------------------
timeout "$T" mkdir -p "$OB_LOGS"
# a resume keeps the original baselines: new session files of this run must still show as additions at cleanup
[ -e "$OB_BASE_SESSIONS" ] || timeout "$T" ls -A "$HOME/.claude/state/launch-level/sessions" > "$OB_BASE_SESSIONS" 2>>"$PRE" || true
[ -e "$OB_BASE_PENDING" ] || timeout "$T" ls -A "$HOME/.claude/state/launch-level/pending" > "$OB_BASE_PENDING" 2>>"$PRE" || true

# --- §1.3 isolated HOME -------------------------------------------------------
# The log-only probe comes from THIS repo (runbook:50-51), whose checkout root
# is $ROOT; the main checkout may be on a branch without the fixture.
timeout "$T" install -m 0755 "$ROOT/tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh" "$OB_BIN/" \
  || { printf 'setup: log-only probe not found under %s\n' "$ROOT" >&2; exit 1; }
timeout "$T" install -m 0755 "$HOME/.claude/hooks/launch-level-guard.sh" "$OB_HOME/.claude/hooks/" \
  || { printf 'setup: guard copy failed\n' >&2; exit 1; }
timeout "$T" cp -r "$HOME/.claude/commands" "$HOME/.claude/skills" "$HOME/.claude/agents" "$OB_HOME/.claude/"

cat > "$OB_BIN/ob-probe.sh" <<'EOF'
#!/bin/bash
# ob-probe.sh <label>: log-only hook for issue 442. Never prints, never blocks, always exits 0.
OB=${OB_DIR:-/tmp/ob}
label=${1:-unlabelled}
input=$(cat 2>/dev/null) || exit 0
{
    tree= p=$PPID n=0
    while [ -n "$p" ] && [ "$p" -gt 1 ] && [ "$n" -lt 12 ]; do
        tree+=$(ps -o pid=,ppid=,pgid=,sid=,lstart=,comm= -p "$p")$'\n'
        p=$(ps -o ppid= -p "$p" | tr -d ' ') n=$((n + 1))
    done
    sid=$(printf '%s' "$input" | jq -r '.session_id // empty')
    level='<no-sid>'
    if [[ $sid =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]; then
        f="$HOME/.claude/state/launch-level/sessions/$sid"
        if [ -f "$f" ]; then level=$(head -c 64 "$f" | tr -d '\n'); else level='<no-session-file>'; fi
        [ -e "$f.ok" ] && level+=' +ok'
    fi
    jq -cn --arg label "$label" --arg home "${HOME-}" --arg ccd "${CLAUDE_CONFIG_DIR-<unset>}" \
        --arg pid "$$" --arg tree "$tree" --arg at "$(date -u +%FT%T.%3NZ)" --arg level "$level" \
        '{probe_env:{label:$label,at:$at,HOME:$home,CLAUDE_CONFIG_DIR:$ccd,hook_pid:$pid,session_file:$level,ancestors:$tree}}' \
        >> "$OB/logs/$label.env.jsonl"
    printf '%s' "$input" | LAUNCH_LEVEL_PROBE_LOG="$OB/logs/$label.jsonl" "$OB/bin/log-only-probe.sh"
} 2>/dev/null
exit 0
EOF
timeout "$T" chmod 0755 "$OB_BIN/ob-probe.sh"

cat > "$OB_BIN/ob-tree.sh" <<'EOF'
#!/bin/bash
# ob-tree.sh <label>: appends this process's ancestor chain to $OB_DIR/logs/tree-<label>.txt. Never prints, exits 0.
OB=${OB_DIR:-/tmp/ob}
label=${1:-unlabelled}
{
    printf '== %s at %s pid=%s\n' "$label" "$(date -u +%FT%T.%3NZ)" "$$"
    p=$$ n=0
    while [ -n "$p" ] && [ "$p" -gt 0 ] && [ "$n" -lt 16 ]; do
        ps -o pid=,ppid=,pgid=,sid=,lstart=,comm= -p "$p"
        [ "$p" -eq 1 ] && break
        p=$(ps -o ppid= -p "$p" | tr -d ' ') n=$((n + 1))
    done
} 2>/dev/null >> "$OB/logs/tree-$label.txt"
exit 0
EOF
timeout "$T" chmod 0755 "$OB_BIN/ob-tree.sh"

cat > "$OB_HOME/.claude/settings.json" <<'EOF'
{
  "hooks": {
    "UserPromptSubmit": [
      {"hooks": [
        {"type": "command", "command": "/tmp/ob/bin/ob-probe.sh h1", "timeout": 10},
        {"type": "command", "command": "/tmp/ob/home/.claude/hooks/launch-level-guard.sh", "timeout": 5}
      ]}
    ],
    "UserPromptExpansion": [{"hooks": [{"type": "command", "command": "/tmp/ob/bin/ob-probe.sh h1", "timeout": 10}]}],
    "PreToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": "/tmp/ob/bin/ob-probe.sh h1", "timeout": 10}]}],
    "PostToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": "/tmp/ob/bin/ob-probe.sh h1", "timeout": 10}]}],
    "SessionStart": [{"hooks": [{"type": "command", "command": "/tmp/ob/bin/ob-probe.sh h1", "timeout": 10}]}],
    "SubagentStop": [{"hooks": [{"type": "command", "command": "/tmp/ob/bin/ob-probe.sh h1", "timeout": 10}]}],
    "Stop": [{"hooks": [{"type": "command", "command": "/tmp/ob/bin/ob-probe.sh h1", "timeout": 10}]}]
  }
}
EOF

# Session A2 settings: the A settings without the guard, label h1m (runbook §2.1b generator).
timeout "$T" jq '.hooks.UserPromptSubmit[0].hooks |= map(select(.command|test("launch-level-guard")|not)) | (.hooks[][].hooks[].command) |= sub(" h1$";" h1m")' \
  "$OB_HOME/.claude/settings.json" > "$OB/settings-a2.json"

# --- §1.3 disposable repositories --------------------------------------------
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
for r in a push; do
  timeout "$T" git init -q --bare "$OB/bare-$r.git"
  timeout "$T" git init -q -b master "$OB/repo-$r"
  timeout "$T" git -C "$OB/repo-$r" -c user.name=ob -c user.email=ob@invalid commit -q --allow-empty -m init
  timeout "$T" git -C "$OB/repo-$r" remote add origin "$OB/bare-$r.git"
  timeout "$T" git -C "$OB/repo-$r" push -q origin master
done
printf '#!/bin/bash\ncat >/dev/null\nexec /tmp/ob/bin/ob-tree.sh pre-push\n' > "$OB/repo-a/.git/hooks/pre-push"
# The hook execs the probe by its fixed /tmp/ob path; in a relocated OB the
# exec falls through to a missing file and the push continues (fail-open by design).
timeout "$T" chmod 0755 "$OB/repo-a/.git/hooks/pre-push"
timeout "$T" git -C "$OB/repo-push" checkout -q -b side
timeout "$T" git -C "$OB/repo-push" -c user.name=ob -c user.email=ob@invalid commit -q --allow-empty -m side
timeout "$T" git -C "$OB/repo-push" checkout -q master

# --- login check (isolated HOME; never copies credentials) --------------------
printf '== login-check\n' >> "$PRE"
if HOME="$OB_HOME" CLAUDE_CONFIG_DIR="$OB_HOME/.claude" timeout 120 claude -p "Reply with the word ok" >> "$PRE" 2>&1; then
  printf 'login OK\n'
else
  printf 'BLOCKED login-isolated-home\n'
  exit 3
fi
printf 'SETUP_OK\n'
