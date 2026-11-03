#!/usr/bin/env bash
# Workstream C e2e for /sc:post-release v5.0.0 (package class).
# Two throwaway HOMEs under /tmp; real ~/.claude, ~/.claude.json, pipx and ~/.codegraph are never used.
set -u -o pipefail
umask 077
ROOT=$(mktemp -d /tmp/ic-e2e.XXXXXXXX) || { echo "FATAL: mktemp -d /tmp/ic-e2e.XXXXXXXX failed" >&2; exit 1; }
[ -n "$ROOT" ] && [ -d "$ROOT" ] || { echo "FATAL: ROOT=[$ROOT] is not a directory" >&2; exit 1; }
cleanup() { rm -rf "$ROOT" && echo "CLEANUP_OK $ROOT" || echo "CLEANUP_FAIL path=$ROOT"; }
trap cleanup EXIT INT TERM

TAG_URL="git+https://github.com/IronbellyOrg/IronClaude@v5.0.0"
BASE_URL="git+https://github.com/IronbellyOrg/IronClaude@539e2414"   # 4.3.5, before codegraph

mkenv() {  # $1 = scenario dir
  local E=$1; mkdir -p "$E/home" "$E/shims"
  ln -s /usr/local/bin/claude /usr/local/bin/uv /usr/bin/git /usr/bin/python3 /usr/local/bin/node "$E/shims/"
  ln -s /home/coder/.local/bin/pipx "$E/shims/pipx"
  for s in codegraph orca orca-ide; do printf '#!/bin/sh\nexit 127\n' > "$E/shims/$s"; chmod +x "$E/shims/$s"; done
}
run() {  # $1 = scenario dir, rest = command
  local E=$1; shift
  echo "+ $*"
  env -i HOME="$E/home" PATH="$E/home/.local/bin:$E/shims:/usr/bin:/bin" LANG=C.UTF-8 TERM=dumb "$@"
  local rc=$?; echo "[exit=$rc]"; return $rc
}
real_state() {
  stat -c '%n mtime=%Y' /home/coder/.claude.json /home/coder/.claude/settings.json
  echo "codegraph versions: $(ls /home/coder/.codegraph/versions | tr '\n' ' ')"
  echo "pipx: $(pipx list --short | tr '\n' ' ')"
}

echo "=== real-home baseline $(date -u +%FT%TZ)"; real_state > "$ROOT/before.txt"; cat "$ROOT/before.txt"

echo; echo "################ SCENARIO 1: brand-new user, clean HOME ################"
S1=$ROOT/new-user; mkenv "$S1"
run "$S1" pipx install "$TAG_URL"
run "$S1" superclaude --version
run "$S1" superclaude --help | head -40
run "$S1" superclaude install; S1_INSTALL=$?
run "$S1" superclaude install --list | tail -25
run "$S1" superclaude doctor --verbose; S1_DOCTOR=$?
echo "--- codegraph registration in throwaway ~/.claude.json"
run "$S1" python3 -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude.json")));c=d.get("mcpServers",{}).get("codegraph");print(json.dumps(c,indent=1) if c else "NO codegraph entry")'
run "$S1" codegraph --version
echo "--- installed surface counts"
for d in commands/sc agents skills hooks templates rules; do echo "$d: $(ls "$S1/home/.claude/$d" 2>/dev/null | wc -l)"; done
ls "$S1/home/.claude/"*.md | xargs -n1 basename | tr '\n' ' '; echo
echo "--- second install is idempotent"
run "$S1" superclaude install | tail -8; S1_SECOND=$?
echo "--- smoke: a read-only CLI command"
run "$S1" superclaude sprint --help | head -15

echo; echo "################ SCENARIO 2: upgrade 4.3.5 (539e2414) -> v5.0.0 ################"
S2=$ROOT/upgrade; mkenv "$S2"
run "$S2" pipx install "$BASE_URL"
run "$S2" superclaude --version
run "$S2" superclaude install | tail -12
echo "--- seed a legacy IronClaude Serena registration (Tier R shape c)"
run "$S2" claude mcp add-json serena '{"type":"stdio","command":"serena","args":["start-mcp-server","--context","ide-assistant","--project","$(pwd)"]}' --scope user
ls "$S2/home/.claude/"*.md | xargs -n1 basename | tr '\n' ' '; echo
echo "--- documented upgrade (docs/releases/v5.0.0.md migration step 2)"
run "$S2" pipx install --force "$TAG_URL"
run "$S2" superclaude --version
run "$S2" superclaude install --force; S2_INSTALL=$?
run "$S2" superclaude install --list | tail -25
run "$S2" superclaude doctor --verbose; S2_DOCTOR=$?
run "$S2" python3 -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude.json")));print(sorted(d.get("mcpServers",{})))'

echo; echo "=== real-home after"; real_state > "$ROOT/after.txt"; cat "$ROOT/after.txt"
if diff -q "$ROOT/before.txt" "$ROOT/after.txt" >/dev/null; then echo "REAL_HOME_UNCHANGED"; else echo "REAL_HOME_CHANGED"; diff "$ROOT/before.txt" "$ROOT/after.txt"; fi
echo "SUMMARY s1_install=$S1_INSTALL s1_doctor=$S1_DOCTOR s1_second=$S1_SECOND s2_install=$S2_INSTALL s2_doctor=$S2_DOCTOR"
