#!/usr/bin/env bash
# Workstream C e2e for /sc:post-release v6.1.0 (package class).
#
# Three scenarios, each in its own throwaway HOME under /tmp, started with `env -i` so no
# variable of the real session (CLAUDE_CONFIG_DIR, API keys, ...) reaches a command:
#   1. brand-new user:  pipx install git+https://github.com/IronbellyOrg/IronClaude@v6.1.0
#   2. upgrade:         a genuine 6.0.0 install (git archive v6.0.0 src, run with this worktree's
#                       virtualenv interpreter), then the documented 6.1.0 upgrade
#   3. from a clone:    ./update.sh in a git archive of v6.1.0
# The real ~/.claude, ~/.local, ~/.codegraph and pipx are only read (before/after listings).
# The script deletes nothing outside the throwaway homes: the throwaway root is left in place and
# printed as ROOT=...; the operator removes it afterwards with a literal path.
#
# Every step is checked: `run` compares each exit code with the one the step is meant to end with
# (default 0), the `chk*` helpers compare numbers and output lines (installed counts against the
# tagged tree, the version line, the retire step's lines), and the script ends in `RESULT: GREEN`
# (exit 0) or `RESULT: RED: <what failed>` (exit 1).
#
# Usage:  bash docs/testing/v6.1.0/c-e2e-run.sh                  (from the repository root; tags v6.0.0 and v6.1.0 present)
# Negative check of the harness itself (touches nothing, needs no network; a failing step must give RED, exit 1):
#         bash docs/testing/v6.1.0/c-e2e-run.sh --selftest-red
#         bash docs/testing/v6.1.0/c-e2e-run.sh --selftest-expected-nonzero    (a step meant to fail must give GREEN, exit 0)

# A variable left over in the caller's shell must not hide a failing step.
unset NOTRACK EXPECT_RC
set -u -o pipefail
umask 077
FAILS=""   # steps that did not end as expected; the exit status at the end reads this
WT=$(pwd)

run() {  # $1 = scenario dir, rest = command (printed, run with a clean environment, exit code printed)
  local E=$1; shift
  echo "+ $*"
  env -i HOME="$E/home" PATH="$E/home/.local/bin:$E/shims:/usr/bin:/bin" LANG=C.UTF-8 TERM=dumb \
    PIPX_HOME="$E/home/.local/share/pipx" PIPX_BIN_DIR="$E/home/.local/bin" GIT_TERMINAL_PROMPT=0 "$@"
  local rc=$?; echo "[exit=$rc]"
  # Every step is tracked against an expected exit code (default 0; set EXPECT_RC=<n> before the call for
  # the steps that are meant to end non-zero; set NOTRACK=1 for a step that is retried). A step run inside
  # $( ... ) cannot update FAILS and is informational only.
  if [ -z "${NOTRACK:-}" ] && [ "$rc" != "${EXPECT_RC:-0}" ]; then FAILS="$FAILS [$* exit=$rc want ${EXPECT_RC:-0}]"; fi
  return $rc
}
chk() { [ "$2" = "$3" ] || FAILS="$FAILS $1(want $2, got $3)"; }   # name, wanted, got
chkgrep() { grep -Eq -- "$2" "$3" 2>/dev/null || FAILS="$FAILS $1(no line matching '$2' in $(basename "$3"))"; }   # name, pattern, file
verdict() {
  if [ -n "$FAILS" ]; then echo "RESULT: RED:$FAILS"; exit 1; fi
  echo "RESULT: GREEN"; exit 0
}

# Harness self-test: runs only `run` and the verdict, in a throwaway folder; no pipx, no network, no claude.
case "${1:-}" in
  --selftest-red|--selftest-expected-nonzero)
    T=$(mktemp -d /tmp/ic6-e2e-selftest.XXXXXXXX) || { echo "FATAL: mktemp failed" >&2; exit 1; }
    mkdir -p "$T/home" "$T/shims"; echo "SELFTEST ROOT=$T (not deleted; remove it with a literal path)"
    if [ "$1" = "--selftest-red" ]; then
      run "$T" sh -c 'exit 0'            # a step that ends as expected
      run "$T" sh -c 'exit 7'            # a step that ends in 7 when 0 was expected: must turn the run RED
    else
      run "$T" sh -c 'exit 0'
      EXPECT_RC=7 run "$T" sh -c 'exit 7'   # a step that is meant to end in 7: must stay GREEN
    fi
    verdict ;;
esac

ROOT=$(mktemp -d /tmp/ic6-e2e.XXXXXXXX) || { echo "FATAL: mktemp failed" >&2; exit 1; }
[ -n "$ROOT" ] && [ -d "$ROOT" ] || { echo "FATAL: ROOT=[$ROOT] is not a directory" >&2; exit 1; }
echo "ROOT=$ROOT"

TAG=v6.1.0; PREV=v6.0.0
TAG_URL="git+https://github.com/IronbellyOrg/IronClaude@$TAG"
VENV_PY="$WT/.venv/bin/python"
[ -x "$VENV_PY" ] || { echo "FATAL: $VENV_PY missing (run: uv venv --python 3.10 && uv pip install -e '.[dev]')" >&2; exit 1; }
git rev-parse -q --verify "$TAG^{commit}" >/dev/null && git rev-parse -q --verify "$PREV^{commit}" >/dev/null \
  || { echo "FATAL: tags $PREV and $TAG must exist (git fetch origin --tags)" >&2; exit 1; }

# What the tagged tree ships (the installer copies the .md files of commands/ and agents/ except README.md,
# and every folder of skills/): the installed counts below are checked against these numbers.
tree_md() { git ls-tree --name-only "$1" "src/superclaude/$2/" | grep '\.md$' | grep -vc '/README\.md$'; }
tree_dirs() { git ls-tree -d --name-only "$1" "src/superclaude/skills/" | wc -l; }
EXP_CMD=$(tree_md $TAG commands); EXP_AGT=$(tree_md $TAG agents); EXP_SKL=$(tree_dirs $TAG)
OLD_CMD=$(tree_md $PREV commands); OLD_AGT=$(tree_md $PREV agents); OLD_SKL=$(tree_dirs $PREV)
echo "tagged tree $TAG: commands=$EXP_CMD agents=$EXP_AGT skills=$EXP_SKL;  $PREV: commands=$OLD_CMD agents=$OLD_AGT skills=$OLD_SKL"

# Pin a private copy of the claude binary: Claude Code's auto-updater replaces the shared one every few
# minutes, and an installer that calls `claude` at that moment exits 1 with "Claude CLI is unavailable"
# (it hit three of the first five scenario starts of the 6.0.0 run). The copy is checked by running it.
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
real_state() {  # read-only fingerprint of the real home areas the task forbids touching (names, sizes AND file contents)
  # ~/.claude.json is hashed only in its mcpServers part (the Claude Code session that runs this script rewrites the rest
  # all the time: history, statistics); every other file below is hashed whole, settings.json included.
  echo "claude commands/agents/skills/hooks/rules/output-styles/templates (every file, name and content): $(find "$HOME/.claude/commands/sc" "$HOME/.claude/agents" "$HOME/.claude/skills" "$HOME/.claude/hooks" "$HOME/.claude/rules" "$HOME/.claude/output-styles" "$HOME/.claude/templates" -type f -print0 2>/dev/null | sort -z | xargs -0 -r sha256sum 2>/dev/null | sha256sum | cut -c1-16)"
  echo "claude top-level files (~/.claude/*.md, settings.json, ccsession.env, content): $(find "$HOME/.claude" -maxdepth 1 -type f \( -name '*.md' -o -name 'settings.json' -o -name 'ccsession.env' \) -print0 2>/dev/null | sort -z | xargs -0 -r sha256sum 2>/dev/null | sha256sum | cut -c1-16)"
  echo "claude.json mcpServers: $(jq -S '.mcpServers' "$HOME/.claude.json" 2>/dev/null | sha256sum | cut -c1-16)"
  echo "claude plugin catalog (~/.claude/ironclaude-marketplace, every file, content): $(find "$HOME/.claude/ironclaude-marketplace" -type f -print0 2>/dev/null | sort -z | xargs -0 -r sha256sum 2>/dev/null | sha256sum | cut -c1-16)"
  echo "codegraph versions: $(ls "$HOME/.codegraph/versions" 2>/dev/null | tr '\n' ' ')"
  echo "local bin (files by content, links by target): $( { find "$HOME/.local/bin" -maxdepth 1 -type f -print0 2>/dev/null | sort -z | xargs -0 -r sha256sum 2>/dev/null; find "$HOME/.local/bin" -maxdepth 1 -type l -printf '%f -> %l\n' 2>/dev/null | sort; } | sha256sum | cut -c1-16)"
  echo "pipx: $(pipx list --short 2>/dev/null | tr '\n' ' ')"
}
nobak() { grep -vc '\.bak\.' ; }  # count lines that are not saved copies
cnt() {  # $1 = scenario dir, $2 = commands/sc | agents | skills : how many installed entries (saved copies excluded)
  ls "$1/home/.claude/$2" 2>/dev/null | nobak
}
counts() {  # $1 = scenario dir: what the installer left in the throwaway ~/.claude (saved copies excluded)
  local H=$1/home/.claude
  echo "commands/sc: $(cnt "$1" commands/sc)"
  echo "agents: $(cnt "$1" agents)"
  echo "skills: $(cnt "$1" skills)"
  echo "hooks: $(ls "$H/hooks" 2>/dev/null | nobak)   templates: $(ls "$H/templates" 2>/dev/null | nobak)   rules: $(ls "$H/rules" 2>/dev/null | nobak)   output-styles: $(ls "$H/output-styles" 2>/dev/null | nobak)"
  echo "core md files ($(ls "$H"/*.md 2>/dev/null | wc -l)): $(ls "$H"/*.md 2>/dev/null | xargs -n1 basename | tr '\n' ' ')"
  echo "saved copies (*.bak.*) under ~/.claude: $(find "$H" -name '*.bak.*' 2>/dev/null | wc -l)"
}
chkcounts() {  # $1 = label, $2 = scenario dir, $3 $4 $5 = wanted commands, agents, skills
  chk "$1.commands" "$3" "$(cnt "$2" commands/sc)"; chk "$1.agents" "$4" "$(cnt "$2" agents)"; chk "$1.skills" "$5" "$(cnt "$2" skills)"
  echo "[check $1] commands=$(cnt "$2" commands/sc) (want $3) agents=$(cnt "$2" agents) (want $4) skills=$(cnt "$2" skills) (want $5)"
}

wait_claude() {  # $1 = scenario dir: wait until `claude --version` works 3 times in a row.
  # The shared claude binary can be replaced by Claude Code's own auto-updater while this script runs;
  # an installer that calls claude at that moment reports "Claude CLI is unavailable" (seen in the 6.0.0 run).
  local E=$1 ok=0 tries=0
  while [ "$ok" -lt 3 ] && [ "$tries" -lt 40 ]; do
    if env -i HOME="$E/home" PATH="$E/shims:/usr/bin:/bin" claude --version >/dev/null 2>&1; then ok=$((ok+1)); else ok=0; fi
    tries=$((tries+1)); sleep 2
  done
  echo "[wait_claude] $tries probes; 3 in a row ok: $([ "$ok" -ge 3 ] && echo yes || echo NO)"
}

echo "=== real-home baseline $(date -u +%FT%TZ)"; real_state > "$ROOT/before.txt"; cat "$ROOT/before.txt"
echo "tag $TAG -> $(git rev-parse $TAG) (commit $(git rev-parse "$TAG^{commit}"))"

echo; echo "################ SCENARIO 1: brand-new user, clean HOME, pipx from the tag ################"
S1=$ROOT/new-user; mkenv "$S1"
run "$S1" claude --version
run "$S1" pipx install "$TAG_URL"; S1_PIPX=$?
run "$S1" superclaude --version > "$ROOT/s1-version.txt" 2>&1; cat "$ROOT/s1-version.txt"; chkgrep s1_version_line "SuperClaude, version 6\.1\.0" "$ROOT/s1-version.txt"
run "$S1" superclaude --help
wait_claude "$S1"
run "$S1" superclaude install; S1_INSTALL=$?
run "$S1" superclaude install --list
run "$S1" superclaude doctor --verbose > "$ROOT/s1-doctor.txt" 2>&1; S1_DOCTOR=$?; cat "$ROOT/s1-doctor.txt"; chkgrep s1_doctor_healthy "SuperClaude is healthy" "$ROOT/s1-doctor.txt"
echo "--- codegraph registration in the throwaway ~/.claude.json"
run "$S1" "$VENV_PY" -I -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude.json")));c=d.get("mcpServers",{}).get("codegraph");print(json.dumps(c,indent=1) if c else "NO codegraph entry"); raise SystemExit(0 if c else 1)'
run "$S1" codegraph --version
echo "--- installed surface (must equal what the tagged tree ships)"; counts "$S1"; chkcounts s1 "$S1" "$EXP_CMD" "$EXP_AGT" "$EXP_SKL"
echo "--- the nine removed skills and /sc:tdd are not installed on a fresh install"
for n in task task-builder roadmap prd tdd tech-research tech-reference operational-guide readme; do
  [ -e "$S1/home/.claude/skills/$n" ] && FAILS="$FAILS s1_removed_skill_present($n)"
done
[ -e "$S1/home/.claude/commands/sc/tdd.md" ] && FAILS="$FAILS s1_removed_command_present(tdd)"
echo "present among the ten removed names: $(for n in task task-builder roadmap prd tdd tech-research tech-reference operational-guide readme; do [ -e "$S1/home/.claude/skills/$n" ] && echo "skill:$n"; done; [ -e "$S1/home/.claude/commands/sc/tdd.md" ] && echo cmd:tdd) (none expected)"
echo "--- kept on purpose: /sc:task, /sc:validate-tests and all eight rf-* agents are installed"
for f in commands/sc/task.md commands/sc/validate-tests.md skills/sc-task-protocol/SKILL.md skills/sc-validate-tests-protocol/SKILL.md; do
  [ -e "$S1/home/.claude/$f" ] && echo "present: $f" || { echo "MISSING: $f"; FAILS="$FAILS s1_kept_missing($f)"; }
done
RF=$(ls "$S1/home/.claude/agents" | grep -c '^rf-'); echo "rf-* agent files: $RF"; chk s1_rf_agents 8 "$RF"
echo "--- #661: every installed /sc:issue template ends with Priority, Fix approach and Test plan, in that order"
for t in issue-bug-simple issue-bug-complex issue-feature-simple issue-feature-complex; do
  F="$S1/home/.claude/skills/sc-issue-protocol/templates/$t.md"
  H=$(grep -E '^## (Priority|Fix approach|Test plan)$' "$F" | tr '\n' '|'); echo "$t: $H"
  chk "s1_issue_template_$t" "## Priority|## Fix approach|## Test plan|" "$H"
done
echo "--- #660: the review tier file shipped in the installed package"
TIERS=$(find "$S1/home/.local/share/pipx/venvs/superclaude" -name review-tiers.default.json | head -1)
echo "file: ${TIERS#$S1/home}"; jq -c '{version, a: .aliases.tier5a.alias, b: .aliases.tier5b.alias, c: .aliases.tier5c.alias, tier1b: .aliases.tier1b.alias}' "$TIERS" | tee "$ROOT/s1-tiers.txt"
chkgrep s1_tiers_labels '"version":"1\.2\.0","a":"review-seat-5a","b":"review-seat-5b","c":"review-seat-5c"' "$ROOT/s1-tiers.txt"
echo "--- second install changes nothing"
find "$S1/home/.claude" -name '*.bak.*' | sort > "$ROOT/s1-bak-before.txt"
wait_claude "$S1"
run "$S1" superclaude install; S1_SECOND=$?
find "$S1/home/.claude" -name '*.bak.*' | sort > "$ROOT/s1-bak-after.txt"
echo "--- saved copies new in the second install (settings.json is backed up on every run):"; comm -13 "$ROOT/s1-bak-before.txt" "$ROOT/s1-bak-after.txt" | sed "s#$S1/home#~#"
echo "--- conversation retention (docs/getting-started/installation.md): this host's managed settings may set cleanupPeriodDays, and then they win"
echo "cleanupPeriodDays in the throwaway settings.json after the install: $(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json")  (null = the installer wrote nothing)"
echo "managed value on this host: $(cat /etc/claude-code/managed-settings.d/*.json 2>/dev/null | jq -c '.cleanupPeriodDays' 2>/dev/null | tr '\n' ' ')"
echo "--- with an empty managed-settings folder (the documented test override) the installer writes the 6.1.0 target, 90"
mkdir -p "$S1/home/no-managed"
jq 'del(.cleanupPeriodDays)' "$S1/home/.claude/settings.json" > "$S1/home/s.json" && cp "$S1/home/s.json" "$S1/home/.claude/settings.json"
wait_claude "$S1"
run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" superclaude install > "$ROOT/s1-retention-install.txt" 2>&1; S1_RET=$?
grep -i 'cleanupPeriodDays\|retention' "$ROOT/s1-retention-install.txt" | head -3; echo "install exit=$S1_RET"
RET_NOW=$(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json"); echo "cleanupPeriodDays now: $RET_NOW"; chk s1_retention_written 90 "$RET_NOW"
RET="$S1/home/.claude/skills/ccsession-tag/retention.py"
echo "--- a larger value is never lowered (365 and 500 stay), a lower one is raised to 90, a file that is not JSON is left alone (retention.py ensure, the script the installer calls)"
for v in 365 500; do
  jq ".cleanupPeriodDays=$v" "$S1/home/.claude/settings.json" > "$S1/home/s.json" && cp "$S1/home/s.json" "$S1/home/.claude/settings.json"
  run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" python3 "$RET" ensure "$S1/home/.claude/settings.json"
  A=$(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json"); echo "after $v: $A"; chk "s1_retention_keeps_$v" "$v" "$A"
done
jq '.cleanupPeriodDays=7' "$S1/home/.claude/settings.json" > "$S1/home/s.json" && cp "$S1/home/s.json" "$S1/home/.claude/settings.json"
run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" python3 "$RET" ensure "$S1/home/.claude/settings.json"
A=$(jq -c '.cleanupPeriodDays' "$S1/home/.claude/settings.json"); echo "after 7: $A"; chk s1_retention_raises_7 90 "$A"
printf '{ not json' > "$S1/home/bad.json"
EXPECT_RC=3 run "$S1" env CCSESSION_MANAGED_SETTINGS_DIR="$S1/home/no-managed" python3 "$RET" ensure "$S1/home/bad.json"; echo "bad.json after: $(cat "$S1/home/bad.json")"
chk s1_bad_json_untouched "{ not json" "$(cat "$S1/home/bad.json")"
echo "saved copies of settings.json now: $(ls "$S1/home/.claude" | grep -c '^settings.json.bak')"
echo "--- #641 ccsession: the new options exist (a dry run changes nothing; a throwaway home has no sessions)"
run "$S1" ccsession --list; run "$S1" ccsession --list --agents; run "$S1" ccsession --classify; run "$S1" ccsession --prune
echo "--- smoke: removed groups are gone, kept groups work, the eval suite count"
EXPECT_RC=2 run "$S1" superclaude roadmap --help; S1_RM=$?
EXPECT_RC=2 run "$S1" superclaude sprint --help
run "$S1" superclaude sweep --help
run "$S1" ic --help
run "$S1" superclaude eval list > "$ROOT/s1-eval-list.txt" 2>&1; cat "$ROOT/s1-eval-list.txt" | head -3
chk s1_eval_suites 15 "$(grep -c '^  - ' "$ROOT/s1-eval-list.txt")"
chk s1_eval_removed_suite 0 "$(grep -c 'workflow_vs_task_builder' "$ROOT/s1-eval-list.txt")"
chkgrep s1_eval_kept_suite 'task_classification_contract' "$ROOT/s1-eval-list.txt"

echo; echo "################ SCENARIO 2: upgrade from a genuine 6.0.0 to 6.1.0 ################"
S2=$ROOT/upgrade; mkenv "$S2"; mkdir -p "$S2/v600"
git archive $PREV src | tar -x -C "$S2/v600"
V600="$S2/v600/src"
echo "--- the 6.0.0 source under test"
run "$S2" "$VENV_PY" -I -c "import sys; sys.path.insert(0, '$V600'); import superclaude; print(superclaude.__version__, superclaude.__file__)"
echo "--- lay down 6.0.0 (its own installer, forced; retried up to 3 times because its first step needs 'claude --version' within 10 s)"
S2_V6=1
for attempt in 1 2 3; do
  wait_claude "$S2"
  NOTRACK=1 run "$S2" claude --version || { sleep 5; continue; }
  NOTRACK=1 run "$S2" "$VENV_PY" -I -c "import sys; sys.path.insert(0, '$V600'); from superclaude.cli.main import main; main(['install','--force'])"; S2_V6=$?
  [ "$S2_V6" -eq 0 ] && break
  echo "6.0.0 seed install attempt $attempt exited $S2_V6; retrying"; sleep 5
done
echo "--- surface at 6.0.0 (must equal what the 6.0.0 tag ships)"; counts "$S2"; chkcounts s2_seed "$S2" "$OLD_CMD" "$OLD_AGT" "$OLD_SKL"
echo "--- the ten items 6.1.0 removes are present at 6.0.0: $(for n in task task-builder roadmap prd tdd tech-research tech-reference operational-guide readme; do [ -e "$S2/home/.claude/skills/$n" ] && echo -n "skill:$n "; done; [ -e "$S2/home/.claude/commands/sc/tdd.md" ] && echo cmd:tdd)"
echo "--- 6.0.0 registered codegraph in the throwaway ~/.claude.json: $(run "$S2" "$VENV_PY" -I -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude.json")));print(sorted(d.get("mcpServers",{})))' | head -2 | tail -1)"
echo "--- seed what a real user has: an edited removed command (tdd), an edited kept command, an edited output style, an edited core file, a removed skill folder with an extra file"
H2=$S2/home/.claude
printf '\n<!-- my own edit -->\n' >> "$H2/commands/sc/tdd.md"
printf '\n<!-- my own edit -->\n' >> "$H2/commands/sc/analyze.md"
printf '\n<!-- my own edit -->\n' >> "$H2/output-styles/pragmatic.md"
printf '\n<!-- my own edit -->\n' >> "$H2/CLAUDE.md"
printf 'my notes\n' > "$H2/skills/task-builder/my-notes.txt"
cp -p "$H2/CLAUDE.md" "$S2/CLAUDE.md.edited"
echo "--- the documented 6.1.0 upgrade (docs/getting-started/upgrading.md, Step 2)"
run "$S2" pipx install --force "$TAG_URL"; S2_PIPX=$?
run "$S2" superclaude --version > "$ROOT/s2-version.txt" 2>&1; cat "$ROOT/s2-version.txt"; chkgrep s2_version_line "SuperClaude, version 6\.1\.0" "$ROOT/s2-version.txt"
wait_claude "$S2"
run "$S2" superclaude install --force > "$ROOT/s2-upgrade-output.txt" 2>&1; S2_INSTALL=$?
cat "$ROOT/s2-upgrade-output.txt"
echo "--- surface after the upgrade: the shipped set plus the kept /sc:tdd and the kept task-builder folder"; counts "$S2"
chkcounts s2_after_upgrade "$S2" "$((EXP_CMD+1))" "$EXP_AGT" "$((EXP_SKL+1))"
chk s2_removed_lines_skills 8 "$(grep -c '^ *Removed skill ' "$ROOT/s2-upgrade-output.txt")"
chkgrep s2_kept_tdd_line 'Kept /sc:tdd:' "$ROOT/s2-upgrade-output.txt"
chkgrep s2_kept_task_builder_line 'Kept skill task-builder:' "$ROOT/s2-upgrade-output.txt"
echo "--- saved copies created by the upgrade"; find "$H2" -name '*.bak.*' | sed "s#$S2/home#~#" | sort
echo "--- by kind: commands=$(find "$H2/commands" -name '*.bak.*' | wc -l) rules=$(find "$H2/rules" -name '*.bak.*' | wc -l) output-styles=$(find "$H2/output-styles" -name '*.bak.*' | wc -l) settings.json=$(find "$H2" -maxdepth 1 -name 'settings.json.bak.*' | wc -l) core-files=$(find "$H2" -maxdepth 1 -name '*.md.bak.*' | wc -l) agents=$(find "$H2/agents" -name '*.bak.*' | wc -l) skills=$(find "$H2/skills" -name '*.bak.*' | wc -l)"
echo "--- edited core file was overwritten without a saved copy: $(cmp -s "$H2/CLAUDE.md" "$S2/CLAUDE.md.edited" && echo NO-still-the-edited-copy || echo yes-overwritten); CLAUDE.md copies: $(find "$H2" -maxdepth 1 -name 'CLAUDE.md.bak.*' | wc -l)"
cmp -s "$H2/CLAUDE.md" "$S2/CLAUDE.md.edited" && FAILS="$FAILS s2_core_file_not_overwritten"
run "$S2" superclaude install --list
# doctor while the kept /sc:tdd is there: whatever its exit code, the code must agree with its own output
run_doctor_kept() { NOTRACK=1 run "$S2" superclaude doctor --verbose > "$ROOT/s2-doctor-kept.txt" 2>&1; S2_DOCTOR_KEPT=$?; cat "$ROOT/s2-doctor-kept.txt"; }
run_doctor_kept
if grep -q 'Missing command-required skill' "$ROOT/s2-doctor-kept.txt"; then chk s2_doctor_while_kept_exit 1 "$S2_DOCTOR_KEPT"; else chk s2_doctor_while_kept_exit 0 "$S2_DOCTOR_KEPT"; fi
echo "[doctor while the edited /sc:tdd and task-builder folder are kept: exit=$S2_DOCTOR_KEPT; 'Missing command-required skill' line present: $(grep -c 'Missing command-required skill' "$ROOT/s2-doctor-kept.txt")]"
echo "--- run the exact rm commands the installer printed for the kept items (only paths under the throwaway ~/.claude)"
grep -o '`rm [^`]*`' "$ROOT/s2-upgrade-output.txt" | tr -d '`' | sort -u > "$ROOT/s2-rm-commands.txt"
chk s2_rm_commands_printed 2 "$(wc -l < "$ROOT/s2-rm-commands.txt")"
while read -r line; do
  case "$line" in "rm $S2/home/.claude/"*|"rm -r $S2/home/.claude/"*|"rm -rf $S2/home/.claude/"*) echo "+ $line"; bash -c "$line"; echo "[exit=$?]";; *) echo "SKIPPED (path outside the throwaway home): $line"; FAILS="$FAILS s2_rm_outside_throwaway";; esac
done < "$ROOT/s2-rm-commands.txt"
run "$S2" superclaude doctor --verbose > "$ROOT/s2-doctor-after-rm.txt" 2>&1; S2_DOCTOR=$?; cat "$ROOT/s2-doctor-after-rm.txt"; chkgrep s2_doctor_healthy_after_rm "SuperClaude is healthy" "$ROOT/s2-doctor-after-rm.txt"
echo "--- after the two rm commands: exactly the shipped set"; counts "$S2"; chkcounts s2_after_rm "$S2" "$EXP_CMD" "$EXP_AGT" "$EXP_SKL"
echo "--- second forced install: the retire step changes nothing; which saved copies are new?"
find "$H2" -name '*.bak.*' | sort > "$ROOT/s2-bak-before.txt"
run "$S2" superclaude install --force > "$ROOT/s2-second-output.txt" 2>&1; S2_SECOND=$?
grep -E 'etiring|Removed|Kept|No retired|Saved' "$ROOT/s2-second-output.txt"
chkgrep s2_second_nothing_to_retire 'No retired commands, skills or agents present' "$ROOT/s2-second-output.txt"
find "$H2" -name '*.bak.*' | sort > "$ROOT/s2-bak-after.txt"
echo "saved copies before=$(wc -l < "$ROOT/s2-bak-before.txt") after=$(wc -l < "$ROOT/s2-bak-after.txt"); new:"; comm -13 "$ROOT/s2-bak-before.txt" "$ROOT/s2-bak-after.txt" | sed "s#$S2/home#~#"
run "$S2" superclaude update > "$ROOT/s2-update-output.txt" 2>&1; S2_UPDATE=$?
grep -E 'etiring|Removed|Kept|No retired|Saved|notice' "$ROOT/s2-update-output.txt"
echo "--- the documented clean-up of saved copies (docs/getting-started/upgrading.md): list, delete, doctor still healthy"
run "$S2" sh -c "find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' | wc -l"
run "$S2" sh -c "find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' -delete; find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' | wc -l"
run "$S2" superclaude doctor --verbose > "$ROOT/s2-doctor-final.txt" 2>&1; S2_DOCTOR_FINAL=$?; cat "$ROOT/s2-doctor-final.txt"; chkgrep s2_doctor_healthy_final "SuperClaude is healthy" "$ROOT/s2-doctor-final.txt"
echo "--- final surface"; counts "$S2"; chkcounts s2_final "$S2" "$EXP_CMD" "$EXP_AGT" "$EXP_SKL"

echo; echo "################ SCENARIO 3: from a clone, ./update.sh ################"
S3=$ROOT/clone-update; mkenv "$S3"; mkdir -p "$S3/clone"
git archive $TAG | tar -x -C "$S3/clone"
wait_claude "$S3"
run "$S3" claude --version
run "$S3" bash -c "cd '$S3/clone' && ./update.sh"; S3_UPDATE=$?
run "$S3" superclaude --version > "$ROOT/s3-version.txt" 2>&1; cat "$ROOT/s3-version.txt"; chkgrep s3_version_line "SuperClaude, version 6\.1\.0" "$ROOT/s3-version.txt"
echo "--- surface"; counts "$S3"; chkcounts s3 "$S3" "$EXP_CMD" "$EXP_AGT" "$EXP_SKL"
echo "--- update.sh ran make sync-dev inside the clone: $(ls "$S3/clone/.claude" 2>/dev/null | tr '\n' ' ')"

echo; echo "=== real-home after"; real_state > "$ROOT/after.txt"; cat "$ROOT/after.txt"
if diff -q "$ROOT/before.txt" "$ROOT/after.txt" >/dev/null; then echo "REAL_HOME_UNCHANGED"; REAL=unchanged; else echo "REAL_HOME_CHANGED"; diff "$ROOT/before.txt" "$ROOT/after.txt"; REAL=changed; fi
echo "SUMMARY s1_pipx=$S1_PIPX s1_install=$S1_INSTALL s1_doctor=$S1_DOCTOR s1_second=$S1_SECOND s1_retention_install=$S1_RET s1_removed_group_exit=$S1_RM s2_v6_seed=$S2_V6 s2_pipx=$S2_PIPX s2_install=$S2_INSTALL s2_doctor_while_kept=$S2_DOCTOR_KEPT s2_doctor_after_rm=$S2_DOCTOR s2_second=$S2_SECOND s2_update=$S2_UPDATE s2_doctor_after_cleanup=$S2_DOCTOR_FINAL s3_update_sh=$S3_UPDATE"
echo "ROOT=$ROOT (not deleted; remove it with a literal path)"

# Exit status: 0 only when every step ended as designed. `run` has already tracked every step against its
# expected exit code and the `chk*` calls above checked counts and output lines; the named checks below repeat
# the exit codes of the key steps. Expected non-zero steps: the retention check on a file that is not JSON (3)
# and the removed `roadmap` and `sprint` groups (2).
chk s1_pipx 0 "$S1_PIPX"; chk s1_install 0 "$S1_INSTALL"; chk s1_doctor 0 "$S1_DOCTOR"; chk s1_second 0 "$S1_SECOND"
chk s1_retention_install 0 "$S1_RET"; chk s1_removed_group_exit 2 "$S1_RM"; chk s2_v6_seed 0 "$S2_V6"; chk s2_pipx 0 "$S2_PIPX"
chk s2_install 0 "$S2_INSTALL"; chk s2_doctor_after_rm 0 "$S2_DOCTOR"
chk s2_second 0 "$S2_SECOND"; chk s2_update 0 "$S2_UPDATE"; chk s2_doctor_after_cleanup 0 "$S2_DOCTOR_FINAL"
chk s3_update_sh 0 "$S3_UPDATE"; chk real_home unchanged "$REAL"
verdict
