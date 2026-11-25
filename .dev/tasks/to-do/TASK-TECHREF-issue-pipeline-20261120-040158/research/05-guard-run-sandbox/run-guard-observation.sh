#!/bin/bash
# Observation run for research agent 05. Writes ONLY under $SB (HOME=$SB/home).
set -u -o pipefail
SB=/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/05-guard-run-sandbox
GUARD=/home/coder/.cache/ic-snap-20261120/master/src/superclaude/hooks/scripts/launch-level-guard.sh
case $SB in /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/05-guard-run-sandbox) ;; *) echo bad-sandbox; exit 1 ;; esac
rm -rf -- "$SB/home" "$SB/out"; mkdir -p "$SB/home" "$SB/out"
export SBHOME="$SB/home"
N=0
pending() { mkdir -p "$SBHOME/.claude/state/launch-level/pending"; printf '%s' "$2" > "$SBHOME/.claude/state/launch-level/pending/$1"; }
pp() { jq -nc --arg s "$1" --arg p "$2" '{hook_event_name:"UserPromptSubmit",session_id:$s,prompt:$p}'; }
pb() { jq -nc --arg s "$1" --arg c "$2" '{hook_event_name:"PreToolUse",session_id:$s,tool_name:"Bash",tool_input:{command:$c}}'; }
ps() { jq -nc --arg s "$1" --arg k "$2" '{hook_event_name:"PreToolUse",session_id:$s,tool_name:"Skill",tool_input:{skill:$k}}'; }
case_run() { # id description payload
  N=$((N+1)); local id=$1 desc=$2 payload=$3 rc o e
  printf '%s' "$payload" | env -i HOME="$SBHOME" PATH=/usr/bin:/bin "$GUARD" >"$SB/out/$id.stdout" 2>"$SB/out/$id.stderr"; rc=$?
  o=$(head -n1 "$SB/out/$id.stdout"); e=$(head -n1 "$SB/out/$id.stderr"); b=$(sed -n 's/^\(Blocked: .*\)$/\1/p' "$SB/out/$id.stderr" | head -n1)
  printf 'CASE %s | %s | exit=%s | stdout1=[%s] | stderr1=[%s] | blocked=[%s]\n' "$id" "$desc" "$rc" "$o" "$e" "${b:0:90}"
}
NW=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1; NWA=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2; NF=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3; NFS=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa4; NWK=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa5; NDG=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa6
# --- S01: ordinary session, store does not exist yet (empty-store fast exit)
case_run S01 "ordinary session prompt, no store" "$(pp ord-1 'hello')"
case_run S01b "ordinary session git push, no store" "$(pb ord-1 'git push origin feature')"
# --- bind four launched sessions through the real marker path
pending $NW worktree; pending $NF full; pending $NFS full-submit; pending $NWK worktree; pending $NDG badword
case_run S02 "governed first prompt binds (worktree) gov-w" "$(pp gov-w "[sc-launch:v1:$NW] Read .dev/issues/1/launch-prompt.md")"
case_run S02f "governed first prompt binds (full) gov-f" "$(pp gov-f "[sc-launch:v1:$NF] go")"
case_run S02s "governed first prompt binds (full-submit) gov-fs" "$(pp gov-fs "[sc-launch:v1:$NFS] go")"
case_run S02k "worker first prompt binds (worktree) worker-w" "$(pp worker-w "[sc-launch:v1:$NWK] brief")"
case_run S02d "pending record holds an invalid word (degraded path) gov-d" "$(pp gov-d "[sc-launch:v1:$NDG] go")"
echo "SESSIONS: $(ls "$SBHOME/.claude/state/launch-level/sessions" | tr '\n' ' ') | gov-w=$(cat "$SBHOME/.claude/state/launch-level/sessions/gov-w") gov-f=$(cat "$SBHOME/.claude/state/launch-level/sessions/gov-f") gov-fs=$(cat "$SBHOME/.claude/state/launch-level/sessions/gov-fs") gov-d=$(cat "$SBHOME/.claude/state/launch-level/sessions/gov-d")"
echo "PENDING left: $(ls "$SBHOME/.claude/state/launch-level/pending" | wc -l)"
# --- S03: ordinary session, store now non-empty
case_run S03 "ordinary session (unbound id) git push, store non-empty" "$(pb ord-2 'git push origin main')"
# --- level matrix at W (gov-w before approval)
case_run M-IMPL-W "Skill sc:implement at W" "$(ps gov-w sc:implement)"
case_run M-COMMIT-W "git commit at W" "$(pb gov-w 'git commit -m x')"
case_run M-PUSH-W "git push origin feature at W" "$(pb gov-w 'git push origin feature')"
case_run M-SUBMIT-W "gh pr comment 5 at W" "$(pb gov-w 'gh pr comment 5 --repo IronbellyOrg/IronClaude --body-file f.md')"
# --- release prompt then WA
case_run S04 "typed /sc:implement prompt at W (approval)" "$(pp gov-w '/sc:implement x')"
echo "APPROVAL FILE: $(ls "$SBHOME/.claude/state/launch-level/sessions" | grep -c '\.ok$') .ok file(s)"
case_run M-IMPL-WA "Skill sc:implement at WA" "$(ps gov-w sc:implement)"
case_run M-COMMIT-WA "git commit at WA" "$(pb gov-w 'git commit -m x')"
case_run M-PUSH-WA "git push origin feature at WA" "$(pb gov-w 'git push origin feature')"
case_run M-SUBMIT-WA "gh pr comment 5 at WA" "$(pb gov-w 'gh pr comment 5 --repo IronbellyOrg/IronClaude --body-file f.md')"
# --- F
case_run M-IMPL-F "Skill sc:implement at F" "$(ps gov-f sc:implement)"
case_run M-COMMIT-F "git commit at F" "$(pb gov-f 'git commit -m x')"
case_run M-PUSH-F "git push origin feature at F" "$(pb gov-f 'git push origin feature')"
case_run M-SUBMIT-F "gh pr comment 5 at F" "$(pb gov-f 'gh pr comment 5 --repo IronbellyOrg/IronClaude --body-file f.md')"
# --- FS
case_run M-IMPL-FS "Skill sc:implement at FS" "$(ps gov-fs sc:implement)"
case_run M-COMMIT-FS "git commit at FS" "$(pb gov-fs 'git commit -m x')"
case_run M-PUSH-FS "git push origin feature at FS" "$(pb gov-fs 'git push origin feature')"
case_run M-SUBMIT-FS "gh pr comment 5 at FS" "$(pb gov-fs 'gh pr comment 5 --repo IronbellyOrg/IronClaude --body-file f.md')"
# --- always blocked at FS
case_run X-PROT-FS "git push origin main at FS" "$(pb gov-fs 'git push origin main')"
case_run X-MERGE-FS "gh pr merge 5 at FS" "$(pb gov-fs 'gh pr merge 5 --repo IronbellyOrg/IronClaude')"
case_run X-REPO-FS "gh pr create without --repo at FS" "$(pb gov-fs 'gh pr create --title x --body y')"
# --- G2 rule 2 (bound worker, worktree level)
case_run G2-A "worker orca orchestration send, no --to" "$(pb worker-w 'orca orchestration send --type heartbeat --body hi --json')"
case_run G2-B "worker orca orchestration ask, no --to" "$(pb worker-w 'orca orchestration ask --body "may I?" --json')"
case_run G2-C "worker orca orchestration send --to run:run_1" "$(pb worker-w 'orca orchestration send --to run:run_1 --body hi')"
case_run G2-D "worker orca terminal send (other verb)" "$(pb worker-w 'orca terminal send --text hi')"
# --- degraded record, tamper, identity loss, malformed
case_run D-1 "degraded session (invalid word) Skill sc:implement" "$(ps gov-d sc:implement)"
case_run T-1 "bound worker names the store (tamper)" "$(pb worker-w 'rm -rf ~/.claude/state/launch-level')"
case_run L-1 "tool event with no session_id (identity loss)" "$(jq -nc '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:"git push origin main"}}')"
case_run MAL-1 "malformed payload, ordinary id, not JSON" 'this is { not json "session_id": "ord-3" "tool_name"'
case_run MAL-2 "malformed payload naming a bound id" 'this is { not json "tool_name": "Bash", "session_id": "gov-fs"'
case_run MAL-3 "malformed payload, marker prompt, not JSON" "garbage [sc-launch:v1:$NW]"
case_run EVT-1 "unknown event name for a bound session" "$(jq -nc '{hook_event_name:"Stop",session_id:"gov-f"}')"
case_run EVT-2 "unknown event name for an ordinary session" "$(jq -nc '{hook_event_name:"Stop",session_id:"ord-9"}')"
echo "CASES: $N"
echo "FILES under SB: $(find "$SB" -type f | wc -l)"
