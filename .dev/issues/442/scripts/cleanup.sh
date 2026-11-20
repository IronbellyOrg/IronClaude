#!/usr/bin/env bash
# cleanup.sh [--apply] — runbook section 5.2 steps 1 to 8, in that order. Plan Task 8.
# Default: print the plan and delete nothing. --apply: do each step, one line per step.
# Worktrees go before the pull request is closed with --delete-branch (step 4 before 5).
set -u -o pipefail
umask 077
here=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck source=lib.sh
source "$here/lib.sh"
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
RESULTS=${OB_RESULTS:-$(cd -- "$here/.." && pwd)/observation-results.md}
T=${OB_TIMEOUT_S:-60}
SD=$HOME/.claude/state/launch-level
APPLY=0
case "${1:-}" in
  --apply) APPLY=1 ;;
  '') ;;
  *) printf 'usage: cleanup.sh [--apply]\n' >&2; exit 2 ;;
esac
if [ "$APPLY" = 1 ] && [ ! -f "$RESULTS" ]; then
  printf 'REFUSED apply: %s is missing (copy the evidence into it first, section 5.2)\n' "$RESULTS"
  exit 4
fi

REFUSED=0
line() {
  printf 'STEP %s %s %s%s\n' "$1" "$2" "${3:-}" "$([ "$APPLY" = 1 ] || printf ' (plan only, nothing done)')"
  case "$2" in REFUSED|FAIL) REFUSED=$((REFUSED + 1)) ;; esac
}
ACTFAIL=0
act() {  # act <command...>: run it with --apply and count a failure; else only say what would run
  if [ "$APPLY" = 1 ]; then "$@" || { ACTFAIL=$((ACTFAIL + 1)); printf '  FAILED: %s\n' "$*"; }; else printf '  WOULD %s\n' "$*"; fi
}
act_soft() {  # like act, but a non-zero exit is normal (pkill finds no process)
  if [ "$APPLY" = 1 ]; then "$@" || true; else printf '  WOULD %s\n' "$*"; fi
}
done_line() {  # done_line <step> <ACTFAIL at the start of the step> <ok text>
  if [ "$ACTFAIL" -gt "$2" ]; then line "$1" FAIL "a command failed (see FAILED above); nothing was retried"; else line "$1" OK "$3"; fi
}
tgit() { command timeout "$T" git "$@"; }
sv() { state_get "$1" 2>/dev/null || true; }
MAIN=${OB_MAIN:-$(main_checkout)}

# --- step 1: leftover background jobs ----------------------------------------------------
step1() {
  local out n pid
  out=$(pgrep -af 'sleep 24[123]$' 2>/dev/null || true)
  printf '  running: %s\n' "${out:-none}"
  # only a job that started after this run's baseline file was written: an unrelated "sleep 241" of the same user stays
  for n in 241 242 243; do
    for pid in $(pgrep -xf "sleep $n" 2>/dev/null || true); do
      if [ "/proc/$pid" -nt "$OB_BASE_SESSIONS" ]; then act_soft command timeout "$T" kill "$pid"
      else printf '  SKIP pid %s (sleep %s): started before this run, not ours\n' "$pid" "$n"; fi
    done
  done
  line 1 OK "sleep 241, 242 and 243 stopped if running"
}

# --- step 2 and the pre-step-7 check: the store against the baseline ---------------------
store_diff() {  # store_diff <sessions|pending> <baseline file>: the diff of runbook lines 799-800
  ls -A "$SD/$1" 2>/dev/null | diff "$2" - || true
}
new_names() { sed -n 's/^> //p'; }
recorded_gsid() {  # recorded_gsid <name>: this run's GSID or its .ok file
  local t g
  for t in T1 T2 T3 T4; do
    g=$(sv "GSID_$t"); [ -n "$g" ] || continue
    [ "$1" = "$g" ] || [ "$1" = "$g.ok" ] && return 0
  done
  return 1
}
step2() {
  local d1 d2 name removed=0 skipped=0 f0=$ACTFAIL
  if [ ! -f "$OB_BASE_SESSIONS" ] || [ ! -f "$OB_BASE_PENDING" ]; then
    line 2 REFUSED "baseline files missing ($OB_BASE_SESSIONS, $OB_BASE_PENDING)"; return
  fi
  d1=$(store_diff sessions "$OB_BASE_SESSIONS"); d2=$(store_diff pending "$OB_BASE_PENDING")
  printf '  sessions diff:\n%s\n  pending diff:\n%s\n' "${d1:-  (none)}" "${d2:-  (none)}"
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    case "$name" in *[!A-Za-z0-9_.-]*) printf '  SKIP odd name in sessions/\n'; skipped=$((skipped + 1)); continue ;; esac
    if recorded_gsid "$name"; then
      act rm -f -- "${SD:?}/sessions/${name:?}"; removed=$((removed + 1))
    else
      printf '  SKIP sessions/%s is new but not a recorded GSID\n' "$name"; skipped=$((skipped + 1))
    fi
  done < <(printf '%s\n' "$d1" | new_names)
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    printf '  SKIP pending/%s is new and is not a session file (left in place)\n' "$name"; skipped=$((skipped + 1))
  done < <(printf '%s\n' "$d2" | new_names)
  if [ "$APPLY" = 1 ]; then   # the diffs again right after the removals (runbook 799-800)
    d1=$(store_diff sessions "$OB_BASE_SESSIONS"); d2=$(store_diff pending "$OB_BASE_PENDING")
    printf '  after step 2, sessions diff:\n%s\n  after step 2, pending diff:\n%s\n' "${d1:-  (none)}" "${d2:-  (none)}"
  fi
  printf '  jobs and requests (listed, never removed): %s\n' "$(ls -A "$SD/jobs" "$SD/requests" 2>/dev/null | tr '\n' ' ')"
  if [ "$removed" -eq 0 ] && [ "$skipped" -eq 0 ]; then done_line 2 "$f0" "nothing to remove"; else done_line 2 "$f0" "removed $removed, skipped $skipped"; fi
}

# --- step 3: the session E push setup, only when this run set the key ----------------------
step3() {
  local pre wt4 f0=$ACTFAIL
  pre=$(sv worktreeConfigPre); wt4=$(sv WT_T4)
  if [ -z "$wt4" ] || [ ! -d "$wt4" ]; then line 3 SKIP "no T4 worktree recorded or present"; return; fi
  if [ "$pre" = unset ]; then
    [ -z "$(tgit -C "$wt4" config --worktree --get remote.origin.pushurl 2>/dev/null)" ] || act tgit -C "$wt4" config --worktree --unset remote.origin.pushurl
    [ -z "$(tgit -C "$wt4" config --get extensions.worktreeConfig 2>/dev/null)" ] || act tgit -C "$wt4" config --unset extensions.worktreeConfig
    done_line 3 "$f0" "worktreeConfigPre=unset: the key and the push URL are undone"
  else
    printf '  extensions.worktreeConfig=%s pushurl=%s\n' "$(tgit -C "$wt4" config --get extensions.worktreeConfig 2>/dev/null)" "$(tgit -C "$wt4" config --worktree --get remote.origin.pushurl 2>/dev/null)"
    line 3 SKIP "worktreeConfigPre=${pre:-absent}: nothing changed, current values listed"
  fi
}

# --- step 4: the worktrees, through Orca ----------------------------------------------------------
rm_worktree() {  # rm_worktree <path>
  local wt=$1 st
  if [ "$APPLY" = 0 ]; then printf '  WOULD orca worktree rm --worktree path:%s\n' "$wt"; return 0; fi
  if command timeout "$T" orca worktree rm --worktree "path:$wt" >/dev/null 2>&1; then printf '  removed %s\n' "$wt"; return 0; fi
  st=$(tgit -C "$wt" status --short 2>/dev/null)
  # --force only when every entry is untracked AND is a path this run or its claim creates:
  # ob-442/ (the disposable file), .claude/ (probe settings), .dev/issues/<n>/ (the claim's copy). Anything else may be the owner's.
  if [ -n "$st" ] && ! printf '%s\n' "$st" | grep -qvE '^\?\? (ob-442/|\.claude/|\.dev/issues/[0-9]+/)'; then
    command timeout "$T" orca worktree rm --worktree "path:$wt" --force >/dev/null 2>&1 && { printf '  removed %s (only untracked files, --force)\n' "$wt"; return 0; }
  fi
  printf '  REFUSED %s: local changes, look at git -C %s status --short\n' "$wt" "$wt"
  return 1
}
step4() {
  local t wt bad=0
  for t in T1 T2 T3 T4; do
    wt=$(sv "WT_$t")
    if [ -z "$wt" ]; then printf '  SKIP %s: no worktree recorded\n' "$t"; continue; fi
    if [ "$APPLY" = 1 ] && [ ! -d "$wt" ]; then printf '  SKIP %s: %s already gone\n' "$t" "$wt"; continue; fi
    rm_worktree "$wt" || bad=1
  done
  if [ "$bad" = 1 ]; then line 4 REFUSED "a worktree was refused because of local changes"; else line 4 OK "worktrees handled"; fi
}

# --- step 5: the pull request and the issues, only the ones the state recorded -------------------------
step5() {
  local url n t f0=$ACTFAIL
  url=$(sv PR_URL)
  case "$url" in
    '') printf '  SKIP pull request: no PR_URL in the state\n' ;;
    https://github.com/IronbellyOrg/IronClaude/pull/[0-9]*) act gh_fork pr close "${url##*/}" --delete-branch ;;
    *) printf '  REFUSED pull request URL is not in IronbellyOrg/IronClaude: %s\n' "$url"; REFUSED=$((REFUSED + 1)) ;;
  esac
  for t in T1 T2 T3 T4; do
    n=$(sv "$t")
    if [ -z "$n" ]; then printf '  SKIP issue %s: not recorded\n' "$t"; continue; fi
    act gh_fork issue close "$n" --reason "not planned"
  done
  printf '  note: the other claim branches may remain locally; list them with git branch --list (not deleted here)\n'
  done_line 5 "$f0" "pull request and issues handled"
}

# --- step 6: the claim records stay in the main checkout ---------------------------------------------------
step6() {
  local t n out="" gc f
  for t in T1 T2 T3 T4; do n=$(sv "$t"); [ -z "$n" ] || [ ! -d "$MAIN/.dev/issues/$n" ] || out="$out $MAIN/.dev/issues/$n"; done
  printf '  left in place for the owner:%s\n' "${out:- none}"
  # the claim installs the L2 pre-push hook into the main repository's shared hooks folder: listed, never deleted
  gc=$(tgit -C "$MAIN" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)
  for f in pre-push pre-push.launch-level; do
    [ -e "$gc/hooks/$f" ] && out="present" || out="absent"
    printf '  L2 hook file %s/hooks/%s: %s now; before the run: %s\n' "$gc" "$f" "$out" "$(sv L2_PRE | grep -oE "$f=[a-z]+" | head -1 | cut -d= -f2)"
  done
  printf '  the L2 hook files above are not removed here: the owner decides whether to keep them\n'
  line 6 OK "nothing removed"
}

# --- step 7: /tmp/ob, only after ob-logs exists and the store is clean -----------------------------------------
step7() {
  local d1 d2 why=""
  case "$OB" in /tmp/ob|/tmp/ob-*) ;; *) line 7 REFUSED "OB is not a /tmp/ob path: $OB"; return ;; esac
  if [ "$APPLY" = 0 ]; then   # the gate needs step 2's real effect, so a plan only describes it
    printf '  WOULD diff both store folders again and refuse while a > line remains or %s/ob-logs is missing\n' "$PKG_ART"
    act rm -rf -- "${OB:?}"
    line 7 OK "$OB would be removed once the gate passes"; return
  fi
  d1=$(store_diff sessions "$OB_BASE_SESSIONS"); d2=$(store_diff pending "$OB_BASE_PENDING")
  printf '  store diff before step 7, sessions:\n%s\n  pending:\n%s\n' "${d1:-  (none)}" "${d2:-  (none)}"
  [ -f "$OB_BASE_SESSIONS" ] && [ -f "$OB_BASE_PENDING" ] || why="baseline files missing"
  [ -d "$PKG_ART/ob-logs" ] || why="${why:+$why; }$PKG_ART/ob-logs is missing (run evidence.sh all first)"
  if printf '%s\n%s\n' "$d1" "$d2" | grep -q '^> '; then why="${why:+$why; }a new store entry (line marked >) remains"; fi
  # the state file records the PR and issue numbers, so it stays while any earlier step failed or was refused
  if [ "$ACTFAIL" -gt 0 ] || [ "$REFUSED" -gt 0 ]; then why="${why:+$why; }an earlier step failed or was refused, so $OB (with the state file) is kept for a retry"; fi
  if [ -n "$why" ]; then line 7 REFUSED "$why"; return; fi
  act rm -rf -- "${OB:?}"
  if [ ! -e "$OB" ]; then line 7 OK "$OB removed"; else line 7 FAIL "$OB is still there"; fi
}

# --- step 8: the earlier worker's scratch folders are listed, never deleted ---------------------------------------
step8() {
  local d found=""
  for d in $(grep -oE '/tmp/ob-[a-z0-9]+\.[A-Za-z0-9]+' "$RB" | sort -u); do [ ! -e "$d" ] || found="$found $d"; done
  printf '  present, not deleted (they belong to the earlier verification worker):%s\n' "${found:- none}"
  line 8 OK "listed"
}

[ "$APPLY" = 1 ] && printf 'CLEANUP --apply\n' || printf 'CLEANUP plan only: nothing is deleted (run with --apply)\n'
step1; step2; step3; step4; step5; step6; step7; step8
if [ "$REFUSED" -gt 0 ]; then printf 'CLEANUP_INCOMPLETE refused=%s\n' "$REFUSED"; exit 5; fi
[ "$APPLY" = 1 ] && printf 'CLEANUP_DONE\n' || printf 'CLEANUP_PLAN_DONE\n'
