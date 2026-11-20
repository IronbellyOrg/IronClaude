#!/usr/bin/env bash
# session-gov-selftest.sh — Task 6 cases, run by selftest.sh.
# Stub orca (per-handle screen queues, one Stop per send), stub gh, a git wrapper
# that can lie about the push URL, and a stub launch-job-identity.sh in a temp HOME.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }
has() { case "$2" in *"$3"*) ck "$1" ok ok ;; *) ck "$1" "missing <$3> in <$(printf '%s' "$2" | tail -3 | tr '\n' '|')>" ok ;; esac; }
hasnt() { case "$2" in *"$3"*) ck "$1" "found <$3>" absent ;; *) ck "$1" ok ok ;; esac; }

T=$(mktemp -d /tmp/ob-gov.XXXXXXXX)
export PKG_ART=$T/art
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
REAL_GIT=$(command -v git); export REAL_GIT
mkdir -p "$T/bin" "$PKG_ART"
SLEEPS=()
trap 'for p in "${SLEEPS[@]:-}"; do [ -n "$p" ] && kill "$p" 2>/dev/null; done; rm -rf "$T"' EXIT

cat > "$T/bin/orca" <<'STUB'
#!/usr/bin/env bash
L=$OB_STUB_DIR; h=""; t=""; prev=""
printf '%s\n' "$*" >> "$L/calls.log"
for a in "$@"; do
  [ "$prev" = --terminal ] && h=$a
  [ "$prev" = --text ] && t=$a
  prev=$a
done
case "$1 $2" in
  'terminal read')
    s=$(cat "$L/screen-$h.txt" 2>/dev/null || printf 'ok')
    printf '{"result":{"terminal":{"tail":[%s]}}}\n' "$(printf '%s' "$s" | jq -Rs .)" ;;
  'terminal send')
    printf '%s\t%s\n' "$h" "$t" >> "$L/sent.tsv"
    # STUB_OK_FILE: a typed /sc:implement (and nothing else) creates the unlock file
    case "$t" in /sc:implement\ *) [ -z "${STUB_OK_FILE:-}" ] || : > "$STUB_OK_FILE" ;; esac
    f=$(ls -1 "$L/q-$h"/*.txt 2>/dev/null | head -1)
    case "$h $t" in
      'h-claim /sc:issue --claim '*)
        # a claim saves its result as <main>/.dev/issues/<N>/launch-result.json (issue 691, Part A) and the screen holds
        # a deliberately wrong text (a terminal key, an rm line, no L1 guard line): a script that read the screen would fail
        n=$(printf '%s' "$t" | awk '{print $3}'); r=$OB_STUB_MAIN/.dev/issues/$n/launch-result.json
        if [ -n "$f" ]; then
          case "${STUB_RESULT_MODE:-}" in
            none) ;;
            symlink) cp "$f" "$L/linked-result.json"; rm -f "$r"; ln -s "$L/linked-result.json" "$r" ;;
            oldlaunched) jq --arg d "$(date -u -d '1 day ago' +%FT%TZ)" '.launched_at = $d' "$f" > "$r" ;;
            freshlaunched) jq --arg d "$(date -u +%FT%TZ)" '.launched_at = $d' "$f" > "$r" ;;
            stale) cp "$f" "$r"; touch -d '2 hours ago' "$r" ;;
            *) cp "$f" "$r" ;;
          esac
          rm -f "$f"
        fi
        printf 'claim done\n{"terminal":"term_screen_wrong"}\nrm "/nonexistent/a" "/nonexistent/b"\n' > "$L/screen-h-claim.txt" ;;
      *) [ -n "$f" ] && mv "$f" "$L/screen-$h.txt" ;;
    esac
    for lg in "$OB"/logs/*.jsonl; do
      [ -e "$lg" ] || continue
      # STUB_STOP_ONLY=<label>: only that log gets a Stop (the governed agent's first turn stays open)
      [ -z "${STUB_STOP_ONLY:-}" ] || [ "$lg" = "$OB/logs/$STUB_STOP_ONLY.jsonl" ] || continue
      printf '{"hook_event_name":"Stop"}\n' >> "$lg"
    done
    printf '{"status":"ok"}\n' ;;
  'terminal wait') [ -e "$L/idle-on" ] && exit 0; exit 1 ;;
  *) printf '{"status":"ok"}\n' ;;
esac
STUB
cat > "$T/bin/gh" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$OB_STUB_DIR/gh.log"
case "$1 $2" in
  'pr view') printf '%s\n' "${STUB_PR_BRANCH:-ob-442-t4-branch}" ;;
  'api repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt?ref=ob-442-t4-branch') printf 'abc123\n' ;;
  *) printf '{}\n' ;;
esac
STUB
cat > "$T/bin/git" <<'STUB'
#!/usr/bin/env bash
# lies about the push URL of the worktree STUB_WT4 from its second query on
if [ "${STUB_PUSHURL_BAD:-0}" = 1 ] && [ "${1:-}" = -C ] && [ "${2:-}" = "${STUB_WT4:-}" ]; then
  case " $* " in
    *" remote get-url --push origin "*)
      n=$(cat "$STUB_CNT" 2>/dev/null || echo 0); n=$((n+1)); printf '%s' "$n" > "$STUB_CNT"
      [ "$n" -ge 2 ] && { printf 'https://github.com/IronbellyOrg/IronClaude.git\n'; exit 0; }
      ;;
  esac
fi
exec "$REAL_GIT" "$@"
STUB
chmod 0755 "$T/bin/orca" "$T/bin/gh" "$T/bin/git"

# --- scenario builders --------------------------------------------------------------
mkenv() {  # mkenv <tag>: fresh OB, HOME, state, four worktrees; sets S and H
  S=$T/$1; H=$S/home
  rm -rf "$S"
  mkdir -p "$S/ob/logs" "$S/ob/screens" "$S/stub" "$S/wts" "$S/main/.dev/issues" \
           "$H/.claude/state/launch-level/sessions" "$H/.claude/state/launch-level/pending" "$H/.claude/hooks"
  : > "$S/ob/state.env"; : > "$S/ob/logs/claim.jsonl"
  local t n=420
  for t in T1 T2 T3 T4; do
    n=$((n+1))
    mkdir -p "$S/wts/$t/.claude" "$S/main/.dev/issues/$n"
    "$REAL_GIT" init -q -b master "$S/wts/$t"
    "$REAL_GIT" -C "$S/wts/$t" -c user.name=ob -c user.email=ob@invalid commit -q --allow-empty -m init
    "$REAL_GIT" -C "$S/wts/$t" remote add origin https://github.com/IronbellyOrg/IronClaude.git
    [ "$t" != T4 ] || "$REAL_GIT" -C "$S/wts/$t" checkout -q -b ob-442-t4-branch   # the pull request's branch
    printf '{"hooks":{"Stop":[]}}' > "$S/wts/$t/.claude/settings.local.json"
    printf '{}\n' > "$S/main/.dev/issues/$n/worktree.json"
    printf '%s=%s\nWT_%s=%s\n' "$t" "$n" "$t" "$S/wts/$t" >> "$S/ob/state.env"
  done
  "$REAL_GIT" init -q -b master "$S/main"
  "$REAL_GIT" -C "$S/main" remote add origin https://github.com/IronbellyOrg/IronClaude.git
  printf 'H_claim=h-claim\n' >> "$S/ob/state.env"
  cat > "$H/.claude/hooks/launch-job-identity.sh" <<'IDS'
#!/usr/bin/env bash
c=$(tr '\0' ' ' < "/proc/$2/cmdline" 2>/dev/null)
case "$c" in
  'sleep 24'[123]' ')
    if [ -e "$HOME/.claude/state/launch-level/sessions/gsid-b-1" ]; then printf '{"status":"governed","session_id":"gsid-b-1"}\n'
    else printf '{"status":"ordinary","reason":"released"}\n'; fi ;;
  *) printf '{"status":"ordinary"}\n' ;;
esac
IDS
  chmod 0755 "$H/.claude/hooks/launch-job-identity.sh"
}
results() {  # results <item1 result> <item5 result>
  printf '# r\n\n## OB-H1 item 1\n\n- Result: %s\n- Session: A\n\n## OB-H1 item 5\n\n- Result: %s\n' "$1" "$2" > "$S/results.md"
}
claim_json() {  # claim_json <status> <warning> <detail> <terminal|null> [rm path 1] [rm path 2]
  local term=null rel=null ino="; this launch's record has inode number ${CLAIM_INODE:-0}: run ls -i"
  [ "${CLAIM_INODE:-}" != none ] || ino=""   # a claim that could not read the inode prints no number
  [ "$4" = null ] || term="\"$4\""
  [ $# -ge 6 ] && rel="\"to release this session, a person runs in their own terminal: rm \\\"$5\\\" \\\"$6\\\" (every file in the sessions folder is named by a session id$ino)\""
  printf '{"status": "%s", "warning": "%s", "detail": "%s", "terminal": %s, "launched_at": null, "release": %s, "layers": ["L1 guard: effective (the IR-4 preflight passed)", "L2 pre-push: absent"]}\n' "$1" "$2" "$3" "$term" "$rel"
}
qpush() {  # qpush <handle> <n> <content>
  mkdir -p "$S/stub/q-$1"; printf '%s\n' "$3" > "$S/stub/q-$1/$(printf '%03d' "$2").txt"
}
seed() {  # seed <label> <gsid> [extra log lines...]: probe log with a session id and one Stop
  local f=$S/ob/logs/h2-$1.jsonl; local g=$2; shift 2
  printf '{"hook_event_name":"SessionStart","session_id":"%s"}\n' "$g" > "$f"
  for l in "$@"; do printf '%s\n' "$l" >> "$f"; done
  printf '{"hook_event_name":"Stop"}\n' >> "$f"
}
runsub() {  # runsub <b|c|d|e> [VAR=value ...]: sets OUT and RC
  local sub=$1; shift
  OUT=$(env OB="$S/ob" HOME="$H" OB_STUB_DIR="$S/stub" OB_STUB_MAIN="$S/main" OB_RESULTS="$S/results.md" OB_MAIN="$S/main" \
        OB_POLL_S=0 OB_LAUNCH_WAIT_S=2 OB_INITIAL_WAIT_S=2 OB_D_WAIT_S=2 OB_E_WAIT_S=2 OB_QUIET_S=0 OB_TIMEOUT_S=20 OB_CLAIM_POLLS=0 \
        PATH="$T/bin:$PATH" "$@" timeout 120 bash "$here/session-gov.sh" "$sub" 2>&1); RC=$?
}
sent() { cat "$S/stub/sent.tsv" 2>/dev/null || true; }
RELP() { printf '%s/.claude/state/launch-level/sessions/<session id>' "$H"; }

# --- 1. stop rules at entry -----------------------------------------------------------
mkenv gate; results PASS pending
runsub b; ck gate-b-rc "$RC" 4; has gate-b-msg "$OUT" 'REFUSED gate item=5 result=pending'
runsub c; ck gate-c-rc "$RC" 4
results FAIL PASS
runsub d; ck gate-d-rc "$RC" 4; has gate-d-msg "$OUT" 'REFUSED gate item=1 result=FAIL'
runsub e; ck gate-e-rc "$RC" 4
rm -f "$S/results.md"
runsub b; has gate-missing-file "$OUT" 'item=5 result=missing'
ck gate-nothing-sent "$(sent | wc -l | tr -d ' ')" 0

# --- 2. session c: plan path from the screen, commit prompt, release --------------------
mkenv c; results PASS PASS
seed T2 gsid-c-1
printf 'gsid-c-1' > "$H/.claude/state/launch-level/sessions/gsid-c-1"   # no .ok file: absent counts as released
claim_json launched W-L2-ABSENT x term_gc "$(RELP)" "$(RELP).ok" > "$S/c-claim.txt"
qpush h-claim 1 "$(cat "$S/c-claim.txt")"
printf 'Waiting for approval\nPlan: .dev/issues/422/plan.md\nrun /sc:implement .dev/issues/422/plan.md\nRead the plan, then type /sc:implement or /task in this session.\n' > "$S/stub/screen-term_gc.txt"
mkdir -p "$S/wts/T2/.dev/issues/422"; : > "$S/wts/T2/.dev/issues/422/plan.md"   # only a path that exists counts
runsub c
ck c-rc "$RC" 0; ck c-done "$(printf '%s' "$OUT" | tail -1)" SESSION_C_DONE
has c-claim-sent "$(sent)" '/sc:issue --claim 422 --pipeline worktree'
has c-implement-sent "$(sent)" "$(printf 'term_gc\t/sc:implement .dev/issues/422/plan.md')"
has c-commit-sent "$(sent)" 'git -c user.name=ob -c user.email=ob@invalid commit --allow-empty -m ob-442'
ck c-released "$([ ! -e "$H/.claude/state/launch-level/sessions/gsid-c-1" ] && echo gone)" gone
has c-release-ok "$OUT" 'OK release gsid-c-1'
hasnt c-no-marker "$(sent)" '[sc-launch:v1:'

# --- 3. release refuses a path that is not this GSID's pair ------------------------------
mkenv c2; results PASS PASS
seed T2 gsid-c-1
for f in gsid-c-1 other-session other-session.ok; do printf x > "$H/.claude/state/launch-level/sessions/$f"; done
printf x > "$H/.claude/settings.json"
claim_json launched W-L2-ABSENT x term_gc "$H/.claude/state/launch-level/sessions/other-session" "$H/.claude/state/launch-level/sessions/other-session.ok" > "$S/c-claim.txt"
qpush h-claim 1 "$(cat "$S/c-claim.txt")"
printf 'run /sc:implement .dev/issues/422/plan.md\n' > "$S/stub/screen-term_gc.txt"
mkdir -p "$S/wts/T2/.dev/issues/422"; : > "$S/wts/T2/.dev/issues/422/plan.md"
runsub c
ck release-foreign-rc "$RC" 1; has release-foreign-msg "$OUT" 'refused: the printed rm paths are not this run'
ck release-foreign-kept "$(ls "$H/.claude/state/launch-level/sessions" | tr '\n' ' ')" 'gsid-c-1 other-session other-session.ok '
mkenv c3; results PASS PASS; seed T2 gsid-c-1
printf x > "$H/.claude/settings.json"; printf x > "$H/.claude/state/launch-level/sessions/gsid-c-1"
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gc "$H/.claude/settings.json" "$H/.claude/settings.json.ok")"
printf 'run /sc:implement .dev/issues/422/plan.md\n' > "$S/stub/screen-term_gc.txt"
mkdir -p "$S/wts/T2/.dev/issues/422"; : > "$S/wts/T2/.dev/issues/422/plan.md"
runsub c
ck release-settings-rc "$RC" 1; ck release-settings-kept "$([ -e "$H/.claude/settings.json" ] && echo kept)" kept
# a screen with only echoed words (no .md path that exists) stops with PENDING and sends no implement command
mkenv c4; results PASS PASS; seed T2 gsid-c-1
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gc "$(RELP)" "$(RELP).ok")"
printf 'Run /sc:implement on the plan you wrote\nRead the plan, then type /sc:implement or /task in this session.\nsee other.md\n' > "$S/stub/screen-term_gc.txt"
runsub c
has c-noplan-pending "$OUT" 'PENDING reason=plan-path-not-on-screen name=gC'
ck c-noplan-nosend "$(sent | grep -c '^term_gc	/sc:implement ' || true)" 0

# --- 4. session b: preflight refusals, restore byte-equal, prompts, release ---------------
mkenv b; results PASS PASS
for p in 241 242 243; do sleep "$p" & SLEEPS+=($!); done
seed T1 gsid-b-1
printf x > "$H/.claude/state/launch-level/sessions/gsid-b-1"   # the .ok file appears only after the typed /sc:implement
printf 'plan written: .dev/issues/421/plan.md\nWaiting for approval\n' > "$S/stub/screen-term_gb.txt"
mkdir -p "$S/wts/T1/.dev/issues/421"; : > "$S/wts/T1/.dev/issues/421/plan.md"   # only a path that exists counts
export STUB_OK_FILE="$H/.claude/state/launch-level/sessions/gsid-b-1.ok"
cp "$S/wts/T1/.claude/settings.local.json" "$S/orig.json"
qpush h-claim 1 "$(claim_json failed W-ENFORCEMENT-ABSENT 'settings.local.json cannot be read as JSON (x)' null)"
qpush h-claim 2 "$(claim_json failed W-ENFORCEMENT-ABSENT 'x sets disableAllHooks to true, so no hook runs' null)"
qpush h-claim 3 "$(CLAIM_INODE=$(stat -c %i "$H/.claude/state/launch-level/sessions/gsid-b-1") claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok")"
runsub b
unset STUB_OK_FILE
ck b-rc "$RC" 0; ck b-done "$(printf '%s' "$OUT" | tail -1)" SESSION_B_DONE
ck b-restored-bytes "$(cmp -s "$S/orig.json" "$S/wts/T1/.claude/settings.local.json" && echo equal)" equal
ck b-backup-bytes "$(cmp -s "$S/orig.json" "$S/ob/t1-local.json" && echo equal)" equal
has b-badjson-claim "$OUT" 'OK b-badjson-claim'; has b-nohooks-claim "$OUT" 'OK b-nohooks-claim'
has b-no-record "$OUT" 'OK b-badjson-no-record'; has b-pending "$OUT" 'OK b-nohooks-pending'
has b-restore "$OUT" 'OK b-restore'
S_SENT=$(sent)
claims=$(printf '%s\n' "$S_SENT" | grep -c '^h-claim	/sc:issue --claim 421 --pipeline worktree$' || true); ck b-three-claims "$claims" 3
seq_ok=$(printf '%s\n' "$S_SENT" | awk -F'\t' '$1=="term_gb"{print $2}' | cut -c1-30 | tr '\n' '|')
has b-order-1 "$seq_ok" 'Run /sc:implement on the plan |Run the Bash command `git -c u'
has b-order-2 "$seq_ok" 'approved|/sc:implement .dev/issues/421/|Run the Bash command `git -c u'
has b-order-3 "$seq_ok" '/clear|Run the Bash command `/tmp/ob/'
has b-approved-no-unlock "$OUT" 'OK b-approved-no-unlock'
has b-ok-file "$OUT" 'OK b-implement-ok'
has b-inode-ok "$OUT" 'OK b-inode session file gsid-b-1 holds inode'
has b-governed-241 "$OUT" '"status":"governed"'
has b-released-ordinary "$OUT" 'OK b-ctx-released'
ck b-session-files-gone "$(ls "$H/.claude/state/launch-level/sessions" | wc -l | tr -d ' ')" 0

# a claim whose inode number differs from the session file's is recorded as FAIL
mkenv b3; results PASS PASS
seed T1 gsid-b-1; for f in gsid-b-1 gsid-b-1.ok; do printf x > "$H/.claude/state/launch-level/sessions/$f"; done
qpush h-claim 1 "$(claim_json failed W-ENFORCEMENT-ABSENT 'settings.local.json cannot be read as JSON (x)' null)"
qpush h-claim 2 "$(claim_json failed W-ENFORCEMENT-ABSENT 'x sets disableAllHooks to true, so no hook runs' null)"
qpush h-claim 3 "$(CLAIM_INODE=1 claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok")"
runsub b
has b-inode-mismatch "$OUT" 'FAIL b-inode session file inode'
# a claim that printed no inode number leaves the record PENDING, not FAIL
mkenv b4; results PASS PASS
seed T1 gsid-b-1; for f in gsid-b-1 gsid-b-1.ok; do printf x > "$H/.claude/state/launch-level/sessions/$f"; done
qpush h-claim 1 "$(claim_json failed W-ENFORCEMENT-ABSENT 'settings.local.json cannot be read as JSON (x)' null)"
qpush h-claim 2 "$(claim_json failed W-ENFORCEMENT-ABSENT 'x sets disableAllHooks to true, so no hook runs' null)"
qpush h-claim 3 "$(CLAIM_INODE=none claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok")"
runsub b
has b-inode-unreadable "$OUT" 'PENDING b-inode the claim printed no inode number'

# a launch that already happened in an earlier run is not claimed or refused again: steps 1 and 2 are skipped
mkenv b7; results PASS PASS
seed T1 gsid-b-1; printf x > "$H/.claude/state/launch-level/sessions/gsid-b-1"
claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$S/ob/claim-T1.json"
printf 'RESUME_LAUNCH_T1=earlier\n' >> "$S/ob/state.env"
printf 'plan written: .dev/issues/421/plan.md\n' > "$S/stub/screen-term_gb.txt"
runsub b
has b-resume-skipped "$OUT" 'OK b-steps-1-2-skipped'
has b-resume-launch "$OUT" 'OK b-resume launch of T1 reused'
hasnt b-resume-no-claim "$(sent)" '/sc:issue --claim 421'

# a launch that saved claim text only (an older run) is not claimed again: a repeat is already_launched and writes no result file
mkenv b8; results PASS PASS
seed T1 gsid-b-1; printf x > "$H/.claude/state/launch-level/sessions/gsid-b-1"
claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$S/ob/claim-T1.txt"
printf 'RESUME_LAUNCH_T1=earlier\n' >> "$S/ob/state.env"
runsub b
ck resume-text-only-rc "$RC" 1; has resume-text-only-msg "$OUT" 'FAIL resume'
hasnt resume-text-only-no-claim "$(sent)" '/sc:issue --claim 421'

# --- 4b. the claim result is read from launch-result.json, never from the screen (issue 691, Part B) ------------
# every stub claim leaves a wrong screen (terminal term_screen_wrong, an rm of /nonexistent paths, no L1 guard line)
cenv() {  # cenv <tag> [jq filter on the launched fixture] [raw fixture body]: a session c scenario, T2 is issue 422
  mkenv "$1"; results PASS PASS; seed T2 gsid-c-1
  printf x > "$H/.claude/state/launch-level/sessions/gsid-c-1"
  if [ $# -ge 3 ]; then qpush h-claim 1 "$3"
  else qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gc "$(RELP)" "$(RELP).ok" | jq -c "${2:-.}")"; fi
  printf 'run /sc:implement .dev/issues/422/plan.md\n' > "$S/stub/screen-term_gc.txt"
  mkdir -p "$S/wts/T2/.dev/issues/422"; : > "$S/wts/T2/.dev/issues/422/plan.md"
}
cenv fresh
runsub c; RES=$S/main/.dev/issues/422/launch-result.json
ck fresh-file-rc "$RC" 0; ck fresh-file-done "$(printf '%s' "$OUT" | tail -1)" SESSION_C_DONE
ck fresh-file-saved-copy-equal "$(cmp -s "$S/ob/claim-T2.json" "$RES" && echo equal)" equal
has screen-ignored-adopts-file-terminal "$OUT" 'OK c-launched terminal=term_gc gsid=gsid-c-1'
hasnt screen-ignored-not-screen-terminal "$OUT" 'term_screen_wrong'
has screen-ignored-layers-from-file "$OUT" 'OK c-layers L1 guard: effective (read from launch-result.json)'
ck screen-ignored-released-file-pair "$([ ! -e "$H/.claude/state/launch-level/sessions/gsid-c-1" ] && echo gone)" gone
cenv freshstamp
runsub c STUB_RESULT_MODE=freshlaunched
ck fresh-launched-at-rc "$RC" 0; ck fresh-launched-at-done "$(printf '%s' "$OUT" | tail -1)" SESSION_C_DONE
cenv missing
runsub c STUB_RESULT_MODE=none
ck missing-rc "$RC" 0; has missing-msg "$OUT" 'PENDING reason=claim-result-missing'
ck missing-no-implement "$(sent | grep -c '/sc:implement' || true)" 0
cenv stale
runsub c STUB_RESULT_MODE=stale
ck stale-rc "$RC" 0; has stale-msg "$OUT" 'PENDING reason=claim-result-stale'
ck stale-no-implement "$(sent | grep -c '/sc:implement' || true)" 0
cenv oldlaunched
runsub c STUB_RESULT_MODE=oldlaunched
ck stale-launched-at-rc "$RC" 0; has stale-launched-at-msg "$OUT" 'PENDING reason=claim-result-stale'
cenv notjson . 'this is not json'
runsub c
ck unreadable-notjson-rc "$RC" 1; has unreadable-notjson-msg "$OUT" 'FAIL claim-result'
cenv jsonarray . '[1,2]'
runsub c
ck unreadable-array-rc "$RC" 1; has unreadable-array-msg "$OUT" 'FAIL claim-result'
cenv nostatus . '{}'
runsub c
ck unreadable-nostatus-rc "$RC" 1; has unreadable-nostatus-msg "$OUT" 'FAIL claim-result'
cenv symlink
runsub c STUB_RESULT_MODE=symlink
ck unreadable-symlink-rc "$RC" 1; has unreadable-symlink-msg "$OUT" 'FAIL claim-result'
cenv failedresult '.status="failed" | .warning="W-ENFORCEMENT-ABSENT" | .detail="refused"'
runsub c
ck failed-result-rc "$RC" 1; has failed-result-msg "$OUT" 'FAIL c-claim status=failed warning=W-ENFORCEMENT-ABSENT'
cenv terminalnull '.terminal = null'
runsub c
ck terminal-null-rc "$RC" 0; has terminal-null-msg "$OUT" 'PENDING reason=terminal-handle-missing'
cenv terminalodd '.terminal = "a b;c"'
runsub c
ck terminal-odd-rc "$RC" 0; has terminal-odd-msg "$OUT" 'PENDING reason=terminal-handle-missing'
cenv nolayer '.layers = ["L2 pre-push: absent"]'
runsub c
ck layers-rc "$RC" 0; has layers-fail "$OUT" 'FAIL c-layers no '"'"'L1 guard: effective'"'"' layer'
ck layers-run-continues "$(printf '%s' "$OUT" | tail -1)" SESSION_C_DONE
# an already_launched claim writes no new result (Part A): the older result stays, counts as missing, and is left byte- and mtime-identical
mkenv already; results PASS PASS
RES=$S/main/.dev/issues/421/launch-result.json
claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$RES"; touch -d '2 hours ago' "$RES"
cp -p "$RES" "$S/prev-result.json"; before=$(stat -c %Y "$RES")
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok")"
runsub b STUB_RESULT_MODE=none
ck already-launched-rc "$RC" 0; has already-launched-msg "$OUT" 'PENDING reason=claim-result-stale'
ck already-launched-bytes "$(cmp -s "$S/prev-result.json" "$RES" && echo equal)" equal
ck already-launched-mtime "$(stat -c %Y "$RES")" "$before"

# --- 5. session b: a failed backup stops before anything is touched -------------------------
mkenv b2; results PASS PASS; rm -f "$S/wts/T1/.claude/settings.local.json"
runsub b
ck b-nobackup-rc "$RC" 1; has b-nobackup-msg "$OUT" 'FAIL b-backup'
ck b-nobackup-untouched "$([ ! -e "$S/wts/T1/.claude/settings.local.json" ] && echo absent)" absent
ck b-nobackup-nosend "$(sent | wc -l | tr -d ' ')" 0

# --- 6. session d: waits for the final git status, then the commit prompt --------------------
mkenv d; results PASS PASS
seed T3 gsid-d-1 '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"git status --short"}}'
printf x > "$H/.claude/state/launch-level/sessions/gsid-d-1"
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gd "$(RELP)" "$(RELP).ok")"
runsub d
ck d-rc "$RC" 0; ck d-done "$(printf '%s' "$OUT" | tail -1)" SESSION_D_DONE
has d-claim-full "$(sent)" '/sc:issue --claim 423 --pipeline full'
has d-commit "$(sent)" "$(printf 'term_gd\tRun the Bash command `git -c user.name=ob')"
mkenv d2; results PASS PASS
seed T3 gsid-d-1 '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"ls"}}'
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gd "$(RELP)" "$(RELP).ok")"
runsub d
has d-pending "$OUT" 'PENDING reason=no-final-git-status'
hasnt d-no-commit-yet "$(sent)" "$(printf 'term_gd\tRun the Bash command')"

# --- 7. session e: fork PR URL, O-10 edit, push URL, prompts, restore --------------------------
PRLOG='{"hook_event_name":"PostToolUse","tool_response":"opened https://github.com/IronbellyOrg/IronClaude/pull/77 via pr-submit"}'
mkenv e; results PASS PASS
seed T4 gsid-e-1 "$PRLOG"
printf x > "$H/.claude/state/launch-level/sessions/gsid-e-1"
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_ge "$(RELP)" "$(RELP).ok")"
runsub e
ck e-rc "$RC" 0; ck e-done "$(printf '%s' "$OUT" | tail -1)" SESSION_E_DONE
has e-claim-submit "$(sent)" '/sc:issue --claim 424 --pipeline full --submit'
has e-pr-url "$OUT" 'OK e-pr-url https://github.com/IronbellyOrg/IronClaude/pull/77'
has e-o10-put "$(cat "$S/stub/gh.log")" 'api repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt -X PUT'
has e-o10-sha "$(cat "$S/stub/gh.log")" 'sha=abc123'
has e-o10-unverified "$OUT" 'UNVERIFIED'
has e-push-url "$OUT" "OK e-push-url $S/ob/bare-push.git"
has e-push-prompt "$(sent)" "$(printf 'term_ge\tRun exactly this Bash command and nothing else: `git push origin master`')"
has e-merge-prompt "$(sent)" 'git merge ob-442-no-such-ref'
ck e-config-pre "$(grep '^worktreeConfigPre=' "$S/ob/state.env" | tail -1)" 'worktreeConfigPre=unset'
ck e-restored-pushurl "$("$REAL_GIT" -C "$S/wts/T4" config --get remote.origin.pushurl 2>/dev/null || echo unset)" unset
ck e-restored-ext "$("$REAL_GIT" -C "$S/wts/T4" config --get extensions.worktreeConfig 2>/dev/null || echo unset)" unset
ck e-main-push-untouched "$("$REAL_GIT" -C "$S/main" remote get-url --push origin)" https://github.com/IronbellyOrg/IronClaude.git
ck e-released "$([ ! -e "$H/.claude/state/launch-level/sessions/gsid-e-1" ] && echo gone)" gone

# a worktree that already had the extension keeps it (worktreeConfigPre=true)
mkenv e2; results PASS PASS
seed T4 gsid-e-1 "$PRLOG"; printf x > "$H/.claude/state/launch-level/sessions/gsid-e-1"
"$REAL_GIT" -C "$S/wts/T4" config extensions.worktreeConfig true
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_ge "$(RELP)" "$(RELP).ok")"
runsub e
ck e2-config-pre "$(grep '^worktreeConfigPre=' "$S/ob/state.env" | tail -1)" 'worktreeConfigPre=true'
ck e2-ext-kept "$("$REAL_GIT" -C "$S/wts/T4" config --get extensions.worktreeConfig)" true

# --- 8. session e refuses a pull request URL outside the fork ------------------------------------
mkenv e3; results PASS PASS
seed T4 gsid-e-1 '{"hook_event_name":"PostToolUse","tool_response":"https://github.com/SuperClaude-Org/SuperClaude_Framework/pull/9 pr-submit"}'
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_ge "$(RELP)" "$(RELP).ok")"
runsub e
ck e-misrouted-rc "$RC" 5; has e-misrouted-msg "$OUT" 'FAIL misrouted-pr https://github.com/SuperClaude-Org/SuperClaude_Framework/pull/9'
hasnt e-misrouted-no-put "$(cat "$S/stub/gh.log" 2>/dev/null)" 'PUT'
hasnt e-misrouted-no-push "$(sent)" 'git push origin master'

# --- 9. session e refuses the push prompt when the push URL is not the bare repository --------------
mkenv e4; results PASS PASS
seed T4 gsid-e-1 "$PRLOG"; printf x > "$H/.claude/state/launch-level/sessions/gsid-e-1"
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_ge "$(RELP)" "$(RELP).ok")"
runsub e STUB_PUSHURL_BAD=1 STUB_WT4="$S/wts/T4" STUB_CNT="$S/stub/cnt"
ck e-pushurl-rc "$RC" 6; has e-pushurl-msg "$OUT" 'REFUSED push prompt'
hasnt e-pushurl-no-push "$(sent)" 'git push origin master'
hasnt e-pushurl-no-merge "$(sent)" 'git merge ob-442-no-such-ref'
ck e-pushurl-restored "$("$REAL_GIT" -C "$S/wts/T4" config --get remote.origin.pushurl 2>/dev/null || echo unset)" unset

# --- 9b. O-10 writes only to the T4 worktree's own branch ------------------------------------------
mkenv e5; results PASS PASS
seed T4 gsid-e-1 "$PRLOG"; printf x > "$H/.claude/state/launch-level/sessions/gsid-e-1"
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_ge "$(RELP)" "$(RELP).ok")"
runsub e STUB_PR_BRANCH=some-other-branch
# a URL whose head branch is not the T4 worktree branch is never taken as this run's pull request:
# no PR_URL in the state (cleanup would close it), no write, and the run ends PENDING
has e-o10-other-pending "$OUT" 'PENDING reason=cycle-not-ended O-10=pending url=none'
hasnt e-o10-other-no-put "$(cat "$S/stub/gh.log" 2>/dev/null)" 'PUT'
ck e-o10-other-no-prurl "$(grep -c '^PR_URL=' "$S/ob/state.env" || true)" 0

# --- 9c. d, e and c wait where the plan says (a first Stop only for the claim session) -----------------
mkenv d3; results PASS PASS
seed T3 gsid-d-1 '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"git status --short"}}'
sed -i '$d' "$S/ob/logs/h2-T3.jsonl"    # drop the seeded Stop: the agent's first turn is still open
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gd "$(RELP)" "$(RELP).ok")"
runsub d STUB_STOP_ONLY=claim OB_INITIAL_WAIT_S=0
has d-own-wait "$OUT" 'PENDING reason=no-final-git-status-within-90-minutes'
hasnt d-no-first-stop-gate "$OUT" 'no-first-stop'
mkenv e6; results PASS PASS
seed T4 gsid-e-1 "$PRLOG"; sed -i '$d' "$S/ob/logs/h2-T4.jsonl"
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_ge "$(RELP)" "$(RELP).ok")"
runsub e STUB_STOP_ONLY=claim OB_INITIAL_WAIT_S=0
has e-own-wait "$OUT" 'PENDING reason=cycle-not-ended'
hasnt e-no-first-stop-gate "$OUT" 'no-first-stop'
mkenv c4; results PASS PASS
seed T2 gsid-c-1; sed -i '$d' "$S/ob/logs/h2-T2.jsonl"
qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gc "$(RELP)" "$(RELP).ok")"
runsub c STUB_STOP_ONLY=claim OB_INITIAL_WAIT_S=1
has c-first-stop-gate "$OUT" 'PENDING reason=no-first-stop label=h2-T2'

# --- 9d. no scenario ever listed terminals: the handle comes from launch-result.json only -------------------------
ck no-terminal-list-in-any-scenario "$(cat "$T"/*/stub/calls.log 2>/dev/null | grep -c 'terminal list' || true)" 0

# --- 10. every prompt file equals its runbook text block, byte for byte (lines 536-697) ----------------
names=(g01-b-implement g02-commit g03-approved g04-gov-bg g05-gov-det g06-gov-clear g07-c-implement g08-e-push g09-e-merge)
sed -n '536,697p' "$RB" | awk -v d="$T/want" '/^```text$/{f=1;n++;next} /^```$/{f=0;next} f{print > sprintf("%s-%d.txt", d, n)}'
same=0
for i in 0 1 2 3 4 5 6 7 8; do
  cmp -s "$T/want-$((i+1)).txt" "$here/prompts/${names[$i]}.txt" && same=$((same+1))
done
ck prompts-bytes "$same" 9
ck prompts-count "$(ls "$here"/prompts/g*.txt | wc -l | tr -d ' ')" 9

exit $failures
