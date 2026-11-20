#!/usr/bin/env bash
# cleanup-selftest.sh — Task 8 cases, run by selftest.sh.
# Stub pgrep, pkill, rm (logs, then really removes inside the temp area), orca and gh
# write one common call log, so the order of the section 5.2 steps can be compared.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }
has() { case "$2" in *"$3"*) ck "$1" ok ok ;; *) ck "$1" "missing <$3> in <$(printf '%s' "$2" | tail -4 | tr '\n' '|')>" ok ;; esac; }
hasnt() { case "$2" in *"$3"*) ck "$1" "found <$3>" absent ;; *) ck "$1" ok ok ;; esac; }

T=$(mktemp -d /tmp/ob-cltest.XXXXXXXX)
trap 'rm -rf "$T"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
REAL_GIT=$(command -v git); REAL_RM=$(command -v rm); export REAL_RM
mkdir -p "$T/bin"
cat > "$T/bin/pgrep" <<'STUB'
#!/usr/bin/env bash
exit 1
STUB
printf '#!/usr/bin/env bash\nprintf "pkill %%s\\n" "$*" >> "$CALLS"\nexit 0\n' > "$T/bin/pkill"
cat > "$T/bin/gh" <<'STUB'
#!/usr/bin/env bash
printf 'gh %s\n' "$*" >> "$CALLS"
exit "${STUB_GH_FAIL:-0}"
STUB
cat > "$T/bin/rm" <<'STUB'
#!/usr/bin/env bash
printf 'rm %s\n' "$*" >> "$CALLS"
exec "$REAL_RM" "$@"
STUB
cat > "$T/bin/orca" <<'STUB'
#!/usr/bin/env bash
printf 'orca %s\n' "$*" >> "$CALLS"
if [ "$1 $2" = "worktree rm" ]; then
  p=""; force=0; prev=""
  for a in "$@"; do [ "$prev" = --worktree ] && p=${a#path:}; [ "$a" = --force ] && force=1; prev=$a; done
  case " ${STUB_RM_FAIL:-} " in *" $p "*) [ "$force" = 1 ] || exit 1 ;; esac
fi
exit 0
STUB
chmod 0755 "$T/bin/"*

mkenv() {  # mkenv <tag> [--no-pr] [--no-gsid] [--pre unset|true|none]: fresh OB (a /tmp/ob-* path), HOME, state, worktrees
  S=$T/$1; shift
  OB=$(mktemp -d /tmp/ob-cl.XXXXXXXX); H=$S/home; PA=$S/art; CALLS=$S/calls.log
  local pr=1 gsid=1 pre=unset t n=420
  while [ $# -gt 0 ]; do case "$1" in --no-pr) pr=0 ;; --no-gsid) gsid=0 ;; --pre) pre=$2; shift ;; esac; shift; done
  mkdir -p "$S" "$PA/ob-logs" "$H/.claude/state/launch-level/"{sessions,pending,jobs,requests} "$S/main/.dev/issues"
  : > "$CALLS"
  printf 'base1\n' > "$OB/baseline-sessions.txt"; : > "$OB/baseline-pending.txt"
  printf base > "$H/.claude/state/launch-level/sessions/base1"
  : > "$OB/state.env"
  for t in T1 T2 T3 T4; do
    n=$((n+1)); mkdir -p "$S/wts" "$S/main/.dev/issues/$n"
    "$REAL_GIT" init -q -b master "$S/wts/$t"
    "$REAL_GIT" -C "$S/wts/$t" -c user.name=ob -c user.email=ob@invalid commit -q --allow-empty -m init
    printf '%s=%s\nWT_%s=%s\n' "$t" "$n" "$t" "$S/wts/$t" >> "$OB/state.env"
  done
  [ "$pr" = 0 ] || printf 'PR_URL=https://github.com/IronbellyOrg/IronClaude/pull/77\n' >> "$OB/state.env"
  if [ "$gsid" = 1 ]; then
    printf 'GSID_T1=gsid-1\n' >> "$OB/state.env"
    printf x > "$H/.claude/state/launch-level/sessions/gsid-1"; printf x > "$H/.claude/state/launch-level/sessions/gsid-1.ok"
  fi
  [ "$pre" = none ] || printf 'worktreeConfigPre=%s\n' "$pre" >> "$OB/state.env"
  "$REAL_GIT" -C "$S/wts/T4" config extensions.worktreeConfig true
  "$REAL_GIT" -C "$S/wts/T4" config --worktree remote.origin.pushurl /tmp/ob/bare-push.git
  printf '# results\n' > "$S/results.md"
}
run() {  # run [args...]: sets OUT and RC
  OUT=$(env OB="$OB" HOME="$H" OB_RESULTS="$S/results.md" PKG_ART="$PA" OB_MAIN="$S/main" CALLS="$CALLS" REAL_RM="$REAL_RM" \
        PATH="$T/bin:$PATH" OB_TIMEOUT_S=20 "$@" 2>&1); RC=$?
}
cl() { run timeout 120 bash "$here/cleanup.sh" "$@"; }
calls() { cut -d' ' -f1 "$CALLS" | tr '\n' ' ' | sed 's/ $//'; }
cfg() { "$REAL_GIT" -C "$S/wts/T4" config --get "$1" 2>/dev/null || echo unset; }
wt4pushurl() { "$REAL_GIT" -C "$S/wts/T4" config --worktree --get remote.origin.pushurl 2>/dev/null || echo unset; }

# --- 1. the default run deletes nothing --------------------------------------------------
mkenv plan
cl
ck plan-rc "$RC" 0
ck plan-no-calls "$(cat "$CALLS" | wc -l | tr -d ' ')" 0
ck plan-steps "$(printf '%s\n' "$OUT" | grep -c '^STEP [1-8] ')" 8
ck plan-end "$(printf '%s\n' "$OUT" | tail -1)" CLEANUP_PLAN_DONE
ck plan-keeps-store "$([ -e "$H/.claude/state/launch-level/sessions/gsid-1" ] && echo kept)" kept
ck plan-keeps-ob "$([ -d "$OB" ] && echo kept)" kept
ck plan-keeps-key "$(cfg extensions.worktreeConfig)" true
has plan-would "$OUT" 'WOULD'
has plan-l2-listed "$OUT" 'hooks/pre-push.launch-level: '
has plan-l2-not-removed "$OUT" 'the L2 hook files above are not removed here'
rm -rf "$OB"

# --- 2. --apply calls them in the section 5.2 order, every gh call pinned ----------------
mkenv apply
cl --apply
ck apply-rc "$RC" 0
ck apply-end "$(printf '%s\n' "$OUT" | tail -1)" CLEANUP_DONE
ck apply-order "$(calls)" 'pkill pkill pkill rm rm orca orca orca orca gh gh gh gh gh rm'
ck apply-steps "$(printf '%s\n' "$OUT" | grep -c '^STEP [1-8] ')" 8
ck apply-gh-pinned "$(grep '^gh ' "$CALLS" | grep -c -- '--repo IronbellyOrg/IronClaude')" 5
has apply-pr-close "$(cat "$CALLS")" 'gh pr close 77 --delete-branch --repo IronbellyOrg/IronClaude'
has apply-issue-close "$(cat "$CALLS")" 'gh issue close 421 --reason not planned --repo IronbellyOrg/IronClaude'
ck apply-wt-rm "$(grep -c '^orca worktree rm --worktree path:' "$CALLS")" 4
ck apply-no-force "$(grep -c -- '--force' "$CALLS")" 0
ck apply-removed-ob "$([ ! -e "$OB" ] && echo gone)" gone
ck apply-removed-gsid "$([ ! -e "$H/.claude/state/launch-level/sessions/gsid-1" ] && [ ! -e "$H/.claude/state/launch-level/sessions/gsid-1.ok" ] && echo gone)" gone
ck apply-kept-baseline "$([ -e "$H/.claude/state/launch-level/sessions/base1" ] && echo kept)" kept
ck apply-state-key-undone "$(cfg extensions.worktreeConfig)" unset
ck apply-pushurl-undone "$(wt4pushurl)" unset
ck apply-claim-records-kept "$([ -d "$S/main/.dev/issues/421" ] && echo kept)" kept

# --- 3. --apply refuses without the results file ------------------------------------------
mkenv noresults
rm -f "$S/results.md"
cl --apply
ck noresults-rc "$RC" 4; has noresults-msg "$OUT" 'REFUSED apply'
ck noresults-nothing "$(wc -l < "$CALLS" | tr -d ' ')" 0
rm -rf "$OB"

# --- 4. step 2 leaves a new entry that is not a recorded GSID; step 7 then refuses -----------
mkenv foreign
printf x > "$H/.claude/state/launch-level/sessions/other"; printf x > "$H/.claude/state/launch-level/sessions/other.ok"
cl --apply
has foreign-skip "$OUT" 'SKIP sessions/other is new but not a recorded GSID'
ck foreign-kept "$([ -e "$H/.claude/state/launch-level/sessions/other" ] && [ -e "$H/.claude/state/launch-level/sessions/other.ok" ] && echo kept)" kept
ck foreign-gsid-removed "$([ ! -e "$H/.claude/state/launch-level/sessions/gsid-1" ] && echo gone)" gone
has foreign-step7-refused "$OUT" 'STEP 7 REFUSED'
has foreign-step7-why "$OUT" 'a new store entry (line marked >) remains'
ck foreign-ob-kept "$([ -d "$OB" ] && echo kept)" kept
ck foreign-rc "$RC" 5
ck foreign-no-ob-rm "$(grep -c -- '-rf' "$CALLS")" 0
rm -rf "$OB"
# a new pending entry stays and also blocks step 7
mkenv pend
printf x > "$H/.claude/state/launch-level/pending/nonce1"
cl --apply
has pend-listed "$OUT" 'SKIP pending/nonce1'
has pend-step7-refused "$OUT" 'STEP 7 REFUSED'
rm -rf "$OB"

# --- 5. step 7 refuses while ob-logs is missing ----------------------------------------------
mkenv nologs
rm -rf "$PA/ob-logs"
cl --apply
has nologs-refused "$OUT" 'STEP 7 REFUSED'
has nologs-why "$OUT" 'ob-logs is missing'
ck nologs-ob-kept "$([ -d "$OB" ] && echo kept)" kept
rm -rf "$OB"

# --- 6. step 3 undoes the key only when the state says unset ---------------------------------------
mkenv pretrue --pre true
cl --apply
ck pretrue-key-kept "$(cfg extensions.worktreeConfig)" true
ck pretrue-pushurl-kept "$(wt4pushurl)" /tmp/ob/bare-push.git
has pretrue-listed "$OUT" 'STEP 3 SKIP worktreeConfigPre=true'
mkenv preabsent --pre none
cl --apply
ck preabsent-key-kept "$(cfg extensions.worktreeConfig)" true
has preabsent-skip "$OUT" 'STEP 3 SKIP worktreeConfigPre=absent'
mkenv preunset --pre unset
cl --apply
ck preunset-key-undone "$(cfg extensions.worktreeConfig)" unset

# --- 7. step 5 lists SKIP for a pull request and issues the state does not record ----------------------
mkenv nogh --no-pr --no-gsid
grep -v -e '^T[1-4]=' "$OB/state.env" > "$OB/state.new" && mv "$OB/state.new" "$OB/state.env"
cl --apply
has nogh-skip-pr "$OUT" 'SKIP pull request: no PR_URL in the state'
has nogh-skip-issue "$OUT" 'SKIP issue T1: not recorded'
ck nogh-no-gh-call "$(grep -c '^gh ' "$CALLS")" 0

# --- 8. the gated run: issues and worktrees recorded, no PR URL, no governed launch ---------------------
mkenv gated --no-pr --no-gsid
cl --apply
ck gated-rc "$RC" 0
ck gated-steps "$(printf '%s\n' "$OUT" | grep -c '^STEP [1-8] ')" 8
has gated-step2 "$OUT" 'STEP 2 OK nothing to remove'
has gated-skip-pr "$OUT" 'SKIP pull request: no PR_URL in the state'
ck gated-no-pr-close "$(grep -c 'pr close' "$CALLS")" 0
ck gated-issue-closes "$(grep -c '^gh issue close' "$CALLS")" 4
ck gated-end "$(printf '%s\n' "$OUT" | tail -1)" CLEANUP_DONE

# --- 8b. the store diff is printed again right after step 2's removals ------------------------------------
mkenv postdiff
cl --apply
before=$(printf '%s\n' "$OUT" | awk '/^  sessions diff:/{on=1;next} /^  pending diff:/{on=0} on')
after=$(printf '%s\n' "$OUT" | awk '/after step 2, sessions diff:/{on=1;next} /after step 2, pending diff:/{on=0} on')
has postdiff-before-lists-gsid "$before" '> gsid-1'
has postdiff-after-label "$OUT" 'after step 2, sessions diff:'
hasnt postdiff-after-gone "$after" 'gsid-1'

# --- 8c. a failed gh call is reported, and the state is kept for a retry -------------------------------------
mkenv ghfail
run env STUB_GH_FAIL=1 timeout 120 bash "$here/cleanup.sh" --apply
has ghfail-failed "$OUT" 'FAILED: gh_fork pr close 77 --delete-branch'
has ghfail-step5 "$OUT" 'STEP 5 FAIL'
has ghfail-step7 "$OUT" 'STEP 7 REFUSED'
hasnt ghfail-no-done "$OUT" 'CLEANUP_DONE'
ck ghfail-rc "$RC" 5
ck ghfail-ob-kept "$([ -f "$OB/state.env" ] && echo kept)" kept
rm -rf "$OB"

# --- 9. --force only for a worktree that holds nothing but untracked files -------------------------------
mkenv force
printf new > "$S/wts/T2/created.txt"                          # untracked: created by the run
printf change > "$S/wts/T3/file.txt"; "$REAL_GIT" -C "$S/wts/T3" add file.txt; "$REAL_GIT" -C "$S/wts/T3" -c user.name=o -c user.email=o@i commit -q -m f
printf changed > "$S/wts/T3/file.txt"                          # a modified tracked file: someone's work
run env STUB_RM_FAIL="$S/wts/T2 $S/wts/T3" timeout 120 bash "$here/cleanup.sh" --apply
ck force-once "$(grep -c -- '--force' "$CALLS")" 1
has force-on-t2 "$(grep -- '--force' "$CALLS")" "path:$S/wts/T2 --force"
has force-refused-t3 "$OUT" "REFUSED $S/wts/T3: local changes"
ck force-rc "$RC" 5
rm -rf "$OB"

exit $failures
