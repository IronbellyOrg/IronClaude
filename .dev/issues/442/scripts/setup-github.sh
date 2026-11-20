#!/usr/bin/env bash
# setup-github.sh — runbook §1.4: four disposable issues, the claim session,
# worktree paths, probe settings. Plan Task 5, adapted to the claim flow of
# origin/master fe14a11bd: `--pipeline none` creates no worktree, so each worktree
# is created with the claim's own script (`orca_worktree.py worktree`).
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
T=${OB_TIMEOUT_S:-60}
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
SKILL=${OB_SKILL_DIR:-$HOME/.claude/skills/sc-issue-protocol}

# --- 1. four disposable issues (gh_fork pins the repo on every form) ------------
# OB_ONLY="T4" limits every loop to those targets (a repeat of one session, such as a second session e run).
TARGETS=${OB_ONLY:-T1 T2 T3 T4}; FIRST=${TARGETS%% *}
# per target: a rerun after a partial failure creates only the issues that are still missing
{
  for t in $TARGETS; do
    if [ -n "$(state_get "$t" 2>/dev/null)" ]; then printf 'SKIP issues: state already holds %s=%s\n' "$t" "$(state_get "$t")"; continue; fi
    # Copy the handoff template to a temp file and fill every section, per the
    # issue rule (never edit the installed template itself).
    tpl=$(mktemp)
    cp "$HOME/.claude/ISSUE-HANDOFF.md" "$tpl"
    # The runbook's body text (runbook line 178) is carried verbatim: the first
    # sentence under "What was tried", the rest under "Done when".
    sed -i \
      -e "s|<what has been tried so far, and what happened>|Disposable target for the #442 live observations ($t).|" \
      -e "s|<paths, links, branches, pull requests>|ob-442/$t.txt|" \
      -e "s|<the condition that means this work is finished>|The only change wanted: create the file ob-442/$t.txt holding the single line ob-442 $t. Touch nothing else. Close without merging anything.|" \
      -e "s|<the person or agent this is handed to>|The observation run's governed sessions ($t)|" \
      "$tpl"
    n=$(gh_fork issue create --title "[ob-442 disposable $t] launch-level observation target" --body-file "$tpl" 2>&1 \
      | grep -oE 'https://github\.com/IronbellyOrg/IronClaude/issues/[0-9]+' | grep -oE '[0-9]+$' | head -1) \
      || true
    [ -n "${n:-}" ] || { printf 'FAIL issue-create %s: no issue URL in output\n' "$t" >&2; exit 1; }
    state_set "$t" "$n"
    printf 'ISSUE %s=%s\n' "$t" "$n"
  done
}

# --- 2. the claim session --------------------------------------------------------
MAIN=${OB_MAIN:-$(main_checkout)}
# The claim installs the L2 pre-push hook into the repository's shared hooks folder.
# Record whether those two files existed before the run, so cleanup can say what this run added.
if [ -z "$(state_get L2_PRE 2>/dev/null)" ]; then
  gc=$(command timeout "$T" git -C "$MAIN" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)
  a=absent; b=absent
  [ -e "$gc/hooks/pre-push" ] && a=present
  [ -e "$gc/hooks/pre-push.launch-level" ] && b=present
  state_set L2_PRE "pre-push=$a pre-push.launch-level=$b"
  printf 'L2_PRE pre-push=%s pre-push.launch-level=%s (%s/hooks)\n' "$a" "$b" "$gc"
fi
if state_get H_claim >/dev/null 2>&1 && [ -n "$(state_get H_claim)" ]; then
  printf 'SKIP claim session: handle %s\n' "$(state_get H_claim)"
else
  # The claim session runs in the real home with every permission granted, and once acted on a disposable
  # issue's body (it created ob-442/T4.txt in the main checkout). This hook refuses any write to an ob-442/ file.
  cat > "$OB_BIN/ob-claim-guard.sh" <<'EOF'
#!/bin/bash
# PreToolUse hook of the claim session: refuse a Write/Edit to an ob-442/ file and a shell command that writes one.
in=$(cat 2>/dev/null) || exit 0
case "$(printf '%s' "$in" | jq -r '.tool_name // ""')" in
  Write|Edit|NotebookEdit) p=$(printf '%s' "$in" | jq -r '.tool_input.file_path // .tool_input.notebook_path // ""')
    case "$p" in *ob-442/*|*settings.local.json*) echo "ob-442 guard: the claim session must not create files for the disposable issues or edit a worktree's settings.local.json" >&2; exit 2 ;; esac ;;
  Bash) c=$(printf '%s' "$in" | jq -r '.tool_input.command // ""')
    if printf '%s' "$c" | grep -qE '(>|tee|touch|mkdir|cp|mv|printf|echo|sed|jq)[^|;&]*(ob-442/|settings\.local\.json)'; then echo "ob-442 guard: the claim session must not create files for the disposable issues or edit a worktree's settings.local.json" >&2; exit 2; fi ;;
esac
exit 0
EOF
  command timeout "$T" chmod 0755 "$OB_BIN/ob-claim-guard.sh"
  command timeout "$T" jq -n --arg c "$OB_BIN/ob-claim-guard.sh" '{hooks: {PreToolUse: [{matcher: "Write|Edit|NotebookEdit|Bash", hooks: [{type: "command", command: $c, timeout: 10}]}]}}' > "$OB/settings-claim.json"
  bash "$here/driver.sh" start claim "path:$MAIN" "env -u CLICKUP_API_TOKEN claude --settings $OB/settings-claim.json" >/dev/null \
    || { printf 'FAIL claim session: the driver could not start it\n' >&2; exit 1; }
  # the command is typed into a shell that may still be starting: send nothing before Claude shows its prompt
  for _ in $(seq 1 "${OB_READY_POLLS:-60}"); do
    f=$(bash "$here/driver.sh" screen claim | tail -1)
    if grep -q 'shift+tab' "$f" 2>/dev/null && grep -q '❯' "$f" 2>/dev/null; then break; fi
    command sleep "${OB_READY_SLEEP_S:-2}"
  done
  if [ "${OB_READY_POLLS:-60}" -ne 0 ] && ! { grep -q 'shift+tab' "$f" 2>/dev/null && grep -q '❯' "$f" 2>/dev/null; }; then
    printf 'PENDING claim session not ready screen=%s\n' "$f"; exit 0
  fi
fi

# --- 3. claims (--pipeline none) + the worktree through the claim's own script -------
for t in $TARGETS; do
  n=$(state_get "$t")
  if state_get "WT_$t" >/dev/null 2>&1 && [ -n "$(state_get "WT_$t")" ]; then
    printf 'SKIP claim %s: WT already %s\n' "$t" "$(state_get "WT_$t")"
    continue
  fi
  # a clean screen, so the completion line of this claim cannot be an older one
  [ "${OB_CLAIM_POLLS:-180}" -eq 0 ] || bash "$here/driver.sh" send claim "/clear" claim 60 >/dev/null 2>&1
  # fire = type and return at once: the driver's own turn wait has no probe log to read here and can hold the full
  # 900 s after the claim is done (seen live); the poll loop below is the completion check
  out=$(bash "$here/driver.sh" fire claim "/sc:issue --claim $n --pipeline none" 2>&1)
  case "$out" in
    NEEDS_INPUT\ *) printf 'NEEDS_INPUT claim %s screen=%s\n' "$t" "${out#NEEDS_INPUT }"; exit 0 ;;
    TURN_END\ timeout*|*PENDING*) printf 'PENDING claim %s\n' "$t"; exit 0 ;;
    *driver:*) printf 'FAIL claim %s: %s\n' "$t" "$(printf '%s' "$out" | tail -1)" >&2; exit 1 ;;
  esac
  # With no probe log the driver ends the wait at the first idle moment, which can fall between two tool calls:
  # wait for the claim's last line ("No worktree created and no agent launched") with the TUI not working.
  for _ in $(seq 1 "${OB_CLAIM_POLLS:-180}"); do
    f=$(bash "$here/driver.sh" screen claim | tail -1)
    # done = the claim's result block for this issue (seen live: "launch_status: not_requested"), or its closing sentence; and the TUI idle
    if { grep -q "issue_number: $n" "$f" && grep -q 'launch_status: not_requested' "$f" || grep -q 'No worktree created and no' "$f"; } 2>/dev/null && ! grep -q 'esc to interrupt' "$f"; then break; fi
    if grep -qE 'Do you want|/login|Not logged in' "$f" 2>/dev/null; then printf 'NEEDS_INPUT claim %s screen=%s\n' "$t" "$f"; exit 0; fi
    command sleep "${OB_CLAIM_SLEEP_S:-5}"
  done
  src=$MAIN/.dev/issues/$n
  [ -d "$src" ] || { printf 'FAIL claim %s: the claim wrote no %s\n' "$t" "$src" >&2; exit 1; }
  # The worktree is read from the script's JSON, not guessed. Run from the main checkout.
  j=$(cd "$MAIN" && command timeout 180 uv run --no-project python "$SKILL/scripts/orca_worktree.py" worktree \
        --repo IronbellyOrg/IronClaude --number "$n" --base origin/master --source "$src" 2>/dev/null) || true
  st=$(printf '%s' "$j" | command timeout "$T" jq -r '.status // empty' 2>/dev/null)
  wt=$(printf '%s' "$j" | command timeout "$T" jq -r '.path // empty' 2>/dev/null)
  case "$st" in created|reused) ;; *) printf 'FAIL claim %s: worktree status <%s>: %s\n' "$t" "${st:-none}" "$(printf '%s' "$j" | head -c 300)" >&2; exit 1 ;; esac
  [ -n "$wt" ] && [ -d "$wt" ] || { printf 'FAIL claim %s: worktree path <%s> is not a directory\n' "$t" "$wt" >&2; exit 1; }
  state_set "WT_$t" "$wt"
  printf 'WORKTREE %s=%s (%s, match_key %s, warning %s)\n' "$t" "$wt" "$st" \
    "$(printf '%s' "$j" | command timeout "$T" jq -r '.match_key // "none"')" "$(printf '%s' "$j" | command timeout "$T" jq -r '.warning // "none"')"
done

# --- 4. probe settings (runbook line 197 generator, labels h2-T1..h2-T4) --------
for t in $TARGETS; do
  wt=$(state_get "WT_$t"); L="h2-$t"
  if [ -e "$wt/.claude/settings.local.json" ]; then
    # an earlier run of this script wrote it: keep it. Anything else is for a person to merge.
    if grep -q "$OB/bin/ob-probe.sh $L" "$wt/.claude/settings.local.json" 2>/dev/null; then printf 'SKIP PROBE %s: already written\n' "$L"; continue; fi
    printf 'EXISTS: merge by hand (%s)\n' "$t" >&2
    exit 3
  fi
  mkdir -p "$wt/.claude"
  command timeout "$T" jq -n --arg c "$OB/bin/ob-probe.sh $L" \
    '{hooks: ((["UserPromptSubmit","UserPromptExpansion","SessionStart","SubagentStop","Stop"] | map({key: ., value: [{hooks: [{type: "command", command: $c, timeout: 10}]}]}) | from_entries) + {PreToolUse: [{matcher: "*", hooks: [{type: "command", command: $c, timeout: 10}]}], PostToolUse: [{matcher: "*", hooks: [{type: "command", command: $c, timeout: 10}]}]})}' \
    > "$wt/.claude/settings.local.json" || { printf 'FAIL probe-settings %s\n' "$t" >&2; exit 1; }
  printf 'PROBE %s -> %s/.claude/settings.local.json\n' "$L" "$wt"
done

printf 'SETUP_GITHUB_OK\n'
