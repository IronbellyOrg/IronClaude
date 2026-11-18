#!/usr/bin/env bash
# Workstream C e2e for /sc:post-release v6.0.0 (package class).
#
# Three scenarios, each in its own throwaway HOME under /tmp, started with `env -i` so no
# variable of the real session (CLAUDE_CONFIG_DIR, API keys, ...) reaches a command:
#   1. brand-new user:  pipx install git+https://github.com/IronbellyOrg/IronClaude@v6.0.0
#   2. upgrade:         a genuine 5.0.0 install (git archive v5.0.0 src, run with this worktree's
#                       virtualenv interpreter), then the documented 6.0.0 upgrade
#   3. from a clone:    ./update.sh in a git archive of v6.0.0
# The real ~/.claude, ~/.local, ~/.codegraph and pipx are only read (before/after listings).
# The script deletes nothing outside the throwaway homes: the throwaway root is left in place and
# printed as ROOT=...; the operator removes it afterwards with a literal path.
#
# Usage:  bash docs/testing/v6.0.0/c-e2e-run.sh        (run from the repository root, tag v6.0.0 present)
set -u -o pipefail
umask 077
WT=$(pwd)
ROOT=$(mktemp -d /tmp/ic6-e2e.XXXXXXXX) || { echo "FATAL: mktemp failed" >&2; exit 1; }
[ -n "$ROOT" ] && [ -d "$ROOT" ] || { echo "FATAL: ROOT=[$ROOT] is not a directory" >&2; exit 1; }
echo "ROOT=$ROOT"

TAG_URL="git+https://github.com/IronbellyOrg/IronClaude@v6.0.0"
VENV_PY="$WT/.venv/bin/python"
[ -x "$VENV_PY" ] || { echo "FATAL: $VENV_PY missing (run: uv venv --python 3.10 && uv pip install -e '.[dev]')" >&2; exit 1; }
# Pin a private copy of the claude binary: Claude Code's auto-updater replaces the shared one every few
# minutes, and an installer that calls `claude` at that moment exits 1 with "Claude CLI is unavailable"
# (it hit three of the first five scenario starts; see the report). The copy is checked by running it.
CLAUDE_SRC=$(readlink -f "$(command -v claude)"); mkdir -p "$ROOT/claude-pin"
for i in 1 2 3 4 5; do
  cp "$CLAUDE_SRC" "$ROOT/claude-pin/claude" 2>/dev/null && chmod +x "$ROOT/claude-pin/claude" \
    && "$ROOT/claude-pin/claude" --version >/dev/null 2>&1 && break
  sleep 3; CLAUDE_SRC=$(readlink -f "$(command -v claude)")
done
CLAUDE_BIN="$ROOT/claude-pin/claude"; echo "pinned claude: $("$CLAUDE_BIN" --version 2>&1)"
NODE_BIN=$(command -v node); UV_BIN=$(command -v uv)
GIT_BIN=$(command -v git); PIPX_BIN=$(command -v pipx); MAKE_BIN=$(command -v make)

mkenv() {  # $1 = scenario dir
  local E=$1; mkdir -p "$E/home" "$E/shims"
  ln -s "$CLAUDE_BIN" "$E/shims/claude"; ln -s "$NODE_BIN" "$E/shims/node"; ln -s "$UV_BIN" "$E/shims/uv"
  ln -s "$GIT_BIN" "$E/shims/git"; ln -s "$PIPX_BIN" "$E/shims/pipx"; ln -s "$MAKE_BIN" "$E/shims/make"
  for s in codegraph orca orca-ide; do printf '#!/bin/sh\nexit 127\n' > "$E/shims/$s"; chmod +x "$E/shims/$s"; done
}
run() {  # $1 = scenario dir, rest = command (printed, run with a clean environment, exit code printed)
  local E=$1; shift
  echo "+ $*"
  env -i HOME="$E/home" PATH="$E/home/.local/bin:$E/shims:/usr/bin:/bin" LANG=C.UTF-8 TERM=dumb \
    PIPX_HOME="$E/home/.local/share/pipx" PIPX_BIN_DIR="$E/home/.local/bin" GIT_TERMINAL_PROMPT=0 "$@"
  local rc=$?; echo "[exit=$rc]"; return $rc
}
real_state() {  # read-only listing of the real home areas the task forbids touching
  echo "claude commands/agents/skills: $(ls -l --time-style=+%s "$HOME/.claude/commands/sc" "$HOME/.claude/agents" "$HOME/.claude/skills" 2>/dev/null | sha256sum | cut -c1-16)"
  echo "codegraph versions: $(ls "$HOME/.codegraph/versions" 2>/dev/null | tr '\n' ' ')"
  echo "local bin: $(ls -l --time-style=+%s "$HOME/.local/bin" 2>/dev/null | sha256sum | cut -c1-16)"
  echo "pipx: $(pipx list --short 2>/dev/null | tr '\n' ' ')"
}
nobak() { grep -vc '\.bak\.' ; }  # count lines that are not saved copies
counts() {  # $1 = scenario dir: what the installer left in the throwaway ~/.claude (saved copies excluded)
  local H=$1/home/.claude
  echo "commands/sc: $(ls "$H/commands/sc" 2>/dev/null | nobak)"
  echo "agents: $(ls "$H/agents" 2>/dev/null | nobak)"
  echo "skills: $(ls "$H/skills" 2>/dev/null | nobak)"
  echo "hooks: $(ls "$H/hooks" 2>/dev/null | nobak)   templates: $(ls "$H/templates" 2>/dev/null | nobak)   rules: $(ls "$H/rules" 2>/dev/null | nobak)   output-styles: $(ls "$H/output-styles" 2>/dev/null | nobak)"
  echo "core md files ($(ls "$H"/*.md 2>/dev/null | wc -l)): $(ls "$H"/*.md 2>/dev/null | xargs -n1 basename | tr '\n' ' ')"
  echo "saved copies (*.bak.*) under ~/.claude: $(find "$H" -name '*.bak.*' 2>/dev/null | wc -l)"
}

wait_claude() {  # $1 = scenario dir: wait until `claude --version` works 3 times in a row.
  # The shared claude binary can be replaced by Claude Code's own auto-updater while this script runs;
  # an installer that calls claude at that moment reports "Claude CLI is unavailable" (seen twice, see the report).
  local E=$1 ok=0 tries=0
  while [ "$ok" -lt 3 ] && [ "$tries" -lt 40 ]; do
    if env -i HOME="$E/home" PATH="$E/shims:/usr/bin:/bin" claude --version >/dev/null 2>&1; then ok=$((ok+1)); else ok=0; fi
    tries=$((tries+1)); sleep 2
  done
  echo "[wait_claude] $tries probes; 3 in a row ok: $([ "$ok" -ge 3 ] && echo yes || echo NO)"
}

echo "=== real-home baseline $(date -u +%FT%TZ)"; real_state > "$ROOT/before.txt"; cat "$ROOT/before.txt"
echo "tag v6.0.0 -> $(git rev-parse v6.0.0) (commit $(git rev-parse 'v6.0.0^{commit}'))"

echo; echo "################ SCENARIO 1: brand-new user, clean HOME, pipx from the tag ################"
S1=$ROOT/new-user; mkenv "$S1"
run "$S1" claude --version
run "$S1" pipx install "$TAG_URL"; S1_PIPX=$?
run "$S1" superclaude --version
run "$S1" superclaude --help
wait_claude "$S1"
run "$S1" superclaude install; S1_INSTALL=$?
run "$S1" superclaude install --list
run "$S1" superclaude doctor --verbose; S1_DOCTOR=$?
echo "--- codegraph registration in the throwaway ~/.claude.json"
run "$S1" "$VENV_PY" -I -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude.json")));c=d.get("mcpServers",{}).get("codegraph");print(json.dumps(c,indent=1) if c else "NO codegraph entry")'
run "$S1" codegraph --version
echo "--- installed surface"; counts "$S1"
echo "--- second install changes nothing"
find "$S1/home/.claude" -name '*.bak.*' | sort > "$ROOT/s1-bak-before.txt"
wait_claude "$S1"
run "$S1" superclaude install; S1_SECOND=$?
find "$S1/home/.claude" -name '*.bak.*' | sort > "$ROOT/s1-bak-after.txt"
echo "--- saved copies new in the second install (settings.json is backed up on every run):"; comm -13 "$ROOT/s1-bak-before.txt" "$ROOT/s1-bak-after.txt" | sed "s#$S1/home#~#"
echo "--- conversation retention (docs/getting-started/installation.md): this host's managed settings set cleanupPeriodDays, so they win"
echo "cleanupPeriodDays in the throwaway settings.json after the install: $(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json")  (null = the installer wrote nothing)"
echo "managed value on this host: $(cat /etc/claude-code/managed-settings.d/*.json 2>/dev/null | jq -c '.cleanupPeriodDays' 2>/dev/null | tr '\n' ' ')"
echo "--- with an empty managed-settings folder (the documented test override) the installer raises it to 365"
mkdir -p "$S1/home/no-managed"
wait_claude "$S1"
run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" superclaude install > "$ROOT/s1-retention-install.txt" 2>&1; S1_RET=$?
grep -i 'cleanupPeriodDays\|retention' "$ROOT/s1-retention-install.txt" | head -3; echo "install exit=$S1_RET"
echo "cleanupPeriodDays now: $(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json")"
RET="$S1/home/.claude/skills/ccsession-tag/retention.py"
echo "--- a larger value is never lowered, a lower one is raised, a file that is not JSON is left alone (retention.py ensure, the script the installer calls)"
jq '.cleanupPeriodDays=500' "$S1/home/.claude/settings.json" > "$S1/home/s.json" && cp "$S1/home/s.json" "$S1/home/.claude/settings.json"
run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" python3 "$RET" ensure "$S1/home/.claude/settings.json"; echo "after 500: $(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json")"
jq '.cleanupPeriodDays=7' "$S1/home/.claude/settings.json" > "$S1/home/s.json" && cp "$S1/home/s.json" "$S1/home/.claude/settings.json"
run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" python3 "$RET" ensure "$S1/home/.claude/settings.json"; echo "after 7: $(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json")"
printf '{ not json' > "$S1/home/bad.json"
run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" python3 "$RET" ensure "$S1/home/bad.json"; echo "bad.json after: $(cat "$S1/home/bad.json")"
echo "saved copies of settings.json now: $(ls "$S1/home/.claude" | grep -c '^settings.json.bak')"
echo "--- smoke: removed groups are gone, new groups exist"
run "$S1" superclaude roadmap --help; S1_RM=$?
run "$S1" superclaude sprint --help
run "$S1" superclaude sweep --help
run "$S1" ic --help

echo; echo "################ SCENARIO 2: upgrade from a genuine 5.0.0 to 6.0.0 ################"
S2=$ROOT/upgrade; mkenv "$S2"; mkdir -p "$S2/v500"
git archive v5.0.0 src | tar -x -C "$S2/v500"
V500="$S2/v500/src"
echo "--- the 5.0.0 source under test"
run "$S2" "$VENV_PY" -I -c "import sys; sys.path.insert(0, '$V500'); import superclaude; print(superclaude.__version__, superclaude.__file__)"
echo "--- lay down 5.0.0 (its own installer, forced; retried up to 3 times because its first step needs 'claude --version' within 10 s)"
S2_V5=1
for attempt in 1 2 3; do
  wait_claude "$S2"
  run "$S2" claude --version || { sleep 5; continue; }
  run "$S2" "$VENV_PY" -I -c "import sys; sys.path.insert(0, '$V500'); from superclaude.cli.main import main; main(['install','--force'])"; S2_V5=$?
  [ "$S2_V5" -eq 0 ] && break
  echo "5.0.0 seed install attempt $attempt exited $S2_V5; retrying"; sleep 5
done
echo "--- surface at 5.0.0"; counts "$S2"
echo "--- 5.0.0 registered codegraph in the throwaway ~/.claude.json: $(run "$S2" "$VENV_PY" -I -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude.json")));print(sorted(d.get("mcpServers",{})))' | head -2 | tail -1)"
echo "--- seed what a real user has: an edited retired command, an edited kept command, an edited output style, an edited core file, a retired skill folder with an extra file"
H2=$S2/home/.claude
printf '\n<!-- my own edit -->\n' >> "$H2/commands/sc/roadmap.md"
printf '\n<!-- my own edit -->\n' >> "$H2/commands/sc/analyze.md"
printf '\n<!-- my own edit -->\n' >> "$H2/output-styles/pragmatic.md"
printf '\n<!-- my own edit -->\n' >> "$H2/CLAUDE.md"
printf 'my notes\n' > "$H2/skills/sc-tasklist-protocol/my-notes.txt"
cp -p "$H2/CLAUDE.md" "$S2/CLAUDE.md.edited"
echo "--- the documented 6.0.0 upgrade (docs/getting-started/upgrading.md, Step 2)"
run "$S2" pipx install --force "$TAG_URL"; S2_PIPX=$?
run "$S2" superclaude --version
wait_claude "$S2"
run "$S2" superclaude install --force > "$ROOT/s2-upgrade-output.txt" 2>&1; S2_INSTALL=$?
cat "$ROOT/s2-upgrade-output.txt"
echo "--- surface after the upgrade"; counts "$S2"
echo "--- saved copies created by the upgrade"; find "$H2" -name '*.bak.*' | sed "s#$S2/home#~#" | sort
echo "--- by kind: commands=$(find "$H2/commands" -name '*.bak.*' | wc -l) rules=$(find "$H2/rules" -name '*.bak.*' | wc -l) output-styles=$(find "$H2/output-styles" -name '*.bak.*' | wc -l) settings.json=$(find "$H2" -maxdepth 1 -name 'settings.json.bak.*' | wc -l) core-files=$(find "$H2" -maxdepth 1 -name '*.md.bak.*' | wc -l) agents=$(find "$H2/agents" -name '*.bak.*' | wc -l) skills=$(find "$H2/skills" -name '*.bak.*' | wc -l)"
echo "--- edited core file was overwritten without a saved copy: $(cmp -s "$H2/CLAUDE.md" "$S2/CLAUDE.md.edited" && echo NO-still-the-edited-copy || echo yes-overwritten); CLAUDE.md copies: $(find "$H2" -maxdepth 1 -name 'CLAUDE.md.bak.*' | wc -l)"
run "$S2" superclaude install --list
run "$S2" superclaude doctor --verbose; S2_DOCTOR_KEPT=$?
echo "--- run the exact rm commands the installer printed for the kept items (only paths under the throwaway ~/.claude)"
grep -o '`rm [^`]*`' "$ROOT/s2-upgrade-output.txt" | tr -d '`' | sort -u | while read -r line; do
  case "$line" in "rm $S2/home/.claude/"*|"rm -r $S2/home/.claude/"*|"rm -rf $S2/home/.claude/"*) echo "+ $line"; bash -c "$line"; echo "[exit=$?]";; *) echo "SKIPPED (path outside the throwaway home): $line";; esac
done
run "$S2" superclaude doctor --verbose; S2_DOCTOR=$?
echo "--- second forced install: the retire step changes nothing; which saved copies are new?"
find "$H2" -name '*.bak.*' | sort > "$ROOT/s2-bak-before.txt"
run "$S2" superclaude install --force > "$ROOT/s2-second-output.txt" 2>&1; S2_SECOND=$?
grep -E 'etiring|Removed|Kept|No retired|Saved' "$ROOT/s2-second-output.txt"
find "$H2" -name '*.bak.*' | sort > "$ROOT/s2-bak-after.txt"
echo "saved copies before=$(wc -l < "$ROOT/s2-bak-before.txt") after=$(wc -l < "$ROOT/s2-bak-after.txt"); new:"; comm -13 "$ROOT/s2-bak-before.txt" "$ROOT/s2-bak-after.txt" | sed "s#$S2/home#~#"
run "$S2" superclaude update > "$ROOT/s2-update-output.txt" 2>&1; S2_UPDATE=$?
grep -E 'etiring|Removed|Kept|No retired|Saved|notice' "$ROOT/s2-update-output.txt"
echo "--- the documented clean-up of saved copies (docs/getting-started/upgrading.md): list, delete, doctor still healthy"
run "$S2" sh -c "find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' | wc -l"
run "$S2" sh -c "find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' -delete; find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' | wc -l"
run "$S2" superclaude doctor --verbose; S2_DOCTOR_FINAL=$?
echo "--- final surface"; counts "$S2"

echo; echo "################ SCENARIO 3: from a clone, ./update.sh ################"
S3=$ROOT/clone-update; mkenv "$S3"; mkdir -p "$S3/clone"
git archive v6.0.0 | tar -x -C "$S3/clone"
wait_claude "$S3"
run "$S3" claude --version
run "$S3" bash -c "cd '$S3/clone' && ./update.sh"; S3_UPDATE=$?
run "$S3" superclaude --version
echo "--- surface"; counts "$S3"
echo "--- update.sh ran make sync-dev inside the clone: $(ls "$S3/clone/.claude" 2>/dev/null | tr '\n' ' ')"

echo; echo "=== real-home after"; real_state > "$ROOT/after.txt"; cat "$ROOT/after.txt"
if diff -q "$ROOT/before.txt" "$ROOT/after.txt" >/dev/null; then echo "REAL_HOME_UNCHANGED"; REAL=unchanged; else echo "REAL_HOME_CHANGED"; diff "$ROOT/before.txt" "$ROOT/after.txt"; REAL=changed; fi
echo "SUMMARY s1_pipx=$S1_PIPX s1_install=$S1_INSTALL s1_doctor=$S1_DOCTOR s1_second=$S1_SECOND s1_retention_install=$S1_RET s1_removed_group_exit=$S1_RM s2_v5_seed=$S2_V5 s2_pipx=$S2_PIPX s2_install=$S2_INSTALL s2_doctor_while_kept=$S2_DOCTOR_KEPT s2_doctor_after_rm=$S2_DOCTOR s2_second=$S2_SECOND s2_update=$S2_UPDATE s2_doctor_after_cleanup=$S2_DOCTOR_FINAL s3_update_sh=$S3_UPDATE"
echo "ROOT=$ROOT (not deleted; remove it with a literal path)"

# Exit status: 0 only when every step ended as designed. The two non-zero values below are expected:
# doctor while a kept removed command exists (1) and the removed `roadmap` group (2).
FAILS=""
chk() { [ "$2" = "$3" ] || FAILS="$FAILS $1(want $2, got $3)"; }
chk s1_pipx 0 "$S1_PIPX"; chk s1_install 0 "$S1_INSTALL"; chk s1_doctor 0 "$S1_DOCTOR"; chk s1_second 0 "$S1_SECOND"
chk s1_retention_install 0 "$S1_RET"; chk s1_removed_group_exit 2 "$S1_RM"; chk s2_v5_seed 0 "$S2_V5"; chk s2_pipx 0 "$S2_PIPX"
chk s2_install 0 "$S2_INSTALL"; chk s2_doctor_while_kept 1 "$S2_DOCTOR_KEPT"; chk s2_doctor_after_rm 0 "$S2_DOCTOR"
chk s2_second 0 "$S2_SECOND"; chk s2_update 0 "$S2_UPDATE"; chk s2_doctor_after_cleanup 0 "$S2_DOCTOR_FINAL"
chk s3_update_sh 0 "$S3_UPDATE"; chk real_home unchanged "$REAL"
if [ -n "$FAILS" ]; then echo "RESULT: RED:$FAILS"; exit 1; fi
echo "RESULT: GREEN"; exit 0
