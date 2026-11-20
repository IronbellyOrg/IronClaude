#!/usr/bin/env bash
# setup-github-selftest.sh — Task 5 cases, run by selftest.sh.
# Adapted to the claim flow of origin/master fe14a11bd: a `--pipeline none` claim creates
# no worktree, so the script creates it with `orca_worktree.py worktree` and reads the path
# from that script's JSON. A stub `uv` plays the script.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }

T=$(mktemp -d /tmp/ob-sg.XXXXXXXX)
trap 'rm -rf "$T" "${T3:-/nonexistent-sg}"' EXIT
export OB=$T
L=${OB_STUB_LOG:-$T/stub}
mkdir -p "$L" "$T/logs" "$T/screens" "$T/wts"
: > "$T/state.env"

# a stand-in main checkout: a git repository whose .dev/issues/<N> folders the claim "wrote"
mkmain() {  # mkmain <dir>
  mkdir -p "$1"
  git init -q -b master "$1" 2>/dev/null
  for n in 421 422 423 424; do mkdir -p "$1/.dev/issues/$n"; done
}
mkmain "$T/main"
export OB_MAIN=$T/main
for t in T1 T2 T3 T4; do mkdir -p "$T/wts/$t/.claude"; done

# stubs: orca (claim session) and uv (the worktree script)
mkdir -p "$L/bin2"
cat > "$L/bin2/orca" <<STUB
#!/usr/bin/env bash
L2=$L
if [ "\$1 \$2" = "terminal read" ]; then
  printf '{"result":{"terminal":{"tail":["ok"]}}}\n'; exit 0
fi
if [ "\$1 \$2" = "terminal wait" ]; then
  [ -e "\$L2/idle-on" ] && exit 0
  exit 1
fi
printf '%s\n' "\$*" >> "\$L2/orca.log"
case "\$1 \$2" in
  'terminal create') printf '{"status":"ok","handle":"stub-handle"}\n' ;;
  'terminal send')
    printf '%s\n' "\${*:4}" >> "\$L2/sent.txt"
    if [ -n "\${STUB_STOP_LOG:-}" ] && [ "\${STUB_STOP:-0}" = 1 ]; then
      printf '{"hook_event_name":"Stop"}\n' >> "\$STUB_STOP_LOG"
    fi
    printf '{"status":"ok"}\n' ;;
  *) printf '{"status":"ok"}\n' ;;
esac
STUB
cat > "$L/bin2/uv" <<STUB
#!/usr/bin/env bash
# uv run --no-project python <script> worktree --repo R --number N --base B --source S
printf '%s\n' "\$*" >> "$L/uv.log"
n=""; prev=""
for a in "\$@"; do [ "\$prev" = --number ] && n=\$a; prev=\$a; done
if [ "\${STUB_WT_FAIL:-0}" = 1 ]; then
  printf '{"status":"failed","path":null,"branch":null,"match_key":null,"warning":"W-WORKTREE-FAILED","detail":"stub"}\n'; exit 0
fi
printf '{"status":"created","path":"%s/wts/T%s","branch":"issue-%s","match_key":null,"warning":null,"detail":""}\n' "$T" "\$((n - 420))" "\$n"
STUB
# a gh stub of its own, so this test never reaches the real GitHub, whoever runs it
cat > "$L/bin2/gh" <<STUB
#!/usr/bin/env bash
printf '%s\n' "\$*" >> "$L/gh.log"
case "\$1 \$2" in
  'issue create')
    n=\$(( \$(cat "$L/issue-n" 2>/dev/null || echo 420) + 1 )); printf '%s' "\$n" > "$L/issue-n"
    prev=""
    for a in "\$@"; do
      [ "\$prev" = --body-file ] && cat "\$a" >> "$L/bodies.txt" 2>/dev/null
      prev=\$a
    done
    printf 'https://github.com/IronbellyOrg/IronClaude/issues/%s\n' "\$n" ;;
  *) printf '{}\n' ;;
esac
STUB
chmod 0755 "$L/bin2/orca" "$L/bin2/uv" "$L/bin2/gh"
export STUB_STOP_LOG=$T/logs/claim.jsonl; : > "$STUB_STOP_LOG"
export STUB_STOP=1
export OB_READY_POLLS=0 OB_CLAIM_POLLS=0   # the stub shows no Claude screen and no claim output
rm -f "$L/uv.log" "$L/sent.txt" "$L/bodies.txt" "$L/gh.log" "$L/issue-n"

# 1. full run
PATH="$L/bin2:$PATH" timeout 120 bash "$here/setup-github.sh" > "$T/out1" 2>&1; rc1=$?
ck sg-rc "$rc1" 0
ck sg-done "$(tail -1 "$T/out1")" "SETUP_GITHUB_OK"

# 2. four issue-create calls, each --repo pinned and --body-file used, no rerun set
grep -c -- '--repo IronbellyOrg/IronClaude' "$L/gh.log" | grep -qx 4 && ck sg-four-creates ok ok || ck sg-four-creates "$(grep -c -- '--repo IronbellyOrg/IronClaude' "$L/gh.log")" 4
grep -c -- '--body-file' "$L/gh.log" | grep -qx 4 && ck sg-bodyfile ok ok || ck sg-bodyfile "$(grep -c -- '--body-file' "$L/gh.log")" 4
# the stub gh copies each --body-file into $L/bodies.txt: the filled body must carry
# the runbook's body text verbatim (runbook line 178) and leave no placeholder.
grep -c -F 'Touch nothing else. Close without merging anything.' "$L/bodies.txt" | grep -qx 4 \
  && ck sg-body-instruction ok ok || ck sg-body-instruction "$(grep -c -F 'Touch nothing else. Close without merging anything.' "$L/bodies.txt")" 4
grep -c -F 'The only change wanted: create the file ob-442/' "$L/bodies.txt" | grep -qx 4 \
  && ck sg-body-change ok ok || ck sg-body-change "$(grep -c -F 'The only change wanted: create the file ob-442/' "$L/bodies.txt")" 4
grep -c -E '^<[^>]*>$' "$L/bodies.txt" | grep -qx 0 && ck sg-body-no-placeholder ok ok || ck sg-body-no-placeholder "$(grep -c -E '^<[^>]*>$' "$L/bodies.txt")" 0
grep -c 'issue create' "$L/gh.log" | grep -qx 4 && ck sg-create-count ok ok || ck sg-create-count "$(grep -c 'issue create' "$L/gh.log")" 4

# 3. the claims are --pipeline none, and each worktree comes from the claim's own script
ck sg-claims-none "$(grep -c -E '/sc:issue --claim 42[1-4] --pipeline none' "$L/sent.txt")" 4
ck sg-no-worktree-pipeline "$(grep -c -E -- '--pipeline (worktree|full)' "$L/sent.txt" || true)" 0
ck sg-uv-calls "$(grep -c 'orca_worktree.py worktree' "$L/uv.log")" 4
ck sg-uv-repo "$(grep -c -- '--repo IronbellyOrg/IronClaude' "$L/uv.log")" 4
ck sg-uv-base "$(grep -c -- '--base origin/master' "$L/uv.log")" 4
ck sg-uv-source "$(grep -c -- "--source $T/main/.dev/issues/42[1-4]" "$L/uv.log")" 4

# 4. rerun refused: state holds numbers, so no second create set
before=$(grep -c 'issue create' "$L/gh.log")
PATH="$L/bin2:$PATH" timeout 60 bash "$here/setup-github.sh" > "$T/out2" 2>&1; rc2=$?
after=$(grep -c 'issue create' "$L/gh.log")
ck sg-rerun-no-new-creates "$after" "$before"
ck sg-rerun-skip-line "$(head -1 "$T/out2")" "SKIP issues: state already holds T1=$(OB=$T bash -c "source '$here/lib.sh'; state_get T1")"
ck sg-rerun-no-new-uv "$(grep -c 'orca_worktree.py worktree' "$L/uv.log")" 4

# 5. state recorded T1..T4 numbers, WT paths read from the script's JSON, and the probe settings
for t in T1 T2 T3 T4; do
  v=$(OB=$T bash -c "source '$here/lib.sh'; state_get $t")
  [ -n "$v" ] && ck "sg-state-$t" ok ok || ck "sg-state-$t" empty ok
  w=$(OB=$T bash -c "source '$here/lib.sh'; state_get WT_$t")
  [ "$w" = "$T/wts/$t" ] && ck "sg-wt-$t" ok ok || ck "sg-wt-$t" "$w" "$T/wts/$t"
  [ -f "$T/wts/$t/.claude/settings.local.json" ] && ck "sg-probe-$t" ok ok || ck "sg-probe-$t" missing ok
done
ck sg-l2-pre "$(OB=$T bash -c "source '$here/lib.sh'; state_get L2_PRE")" 'pre-push=absent pre-push.launch-level=absent'

# 6. generated settings equal the runbook line-197 generator output (labels h2-T*)
for t in T1 T2 T3 T4; do
  command timeout 10 jq -n --arg c "/tmp/ob/bin/ob-probe.sh h2-$t" \
    '{hooks: ((["UserPromptSubmit","UserPromptExpansion","SessionStart","SubagentStop","Stop"] | map({key: ., value: [{hooks: [{type: "command", command: $c, timeout: 10}]}]}) | from_entries) + {PreToolUse: [{matcher: "*", hooks: [{type: "command", command: $c, timeout: 10}]}], PostToolUse: [{matcher: "*", hooks: [{type: "command", command: $c, timeout: 10}]}]})}' \
    > "$T/want-$t.json"
  # the script used $OB/bin/ob-probe.sh; rewrite expected to match that root
  sed "s|/tmp/ob/bin/ob-probe.sh|$T/bin/ob-probe.sh|" "$T/want-$t.json" > "$T/want2-$t.json"
  cmp -s "$T/want2-$t.json" "$T/wts/$t/.claude/settings.local.json" && ck "sg-gen-eq-$t" ok ok || ck "sg-gen-eq-$t" differ ok
done

# 7. a worktree script that fails stops the run before any probe file is written
T3=$(mktemp -d /tmp/ob-sg2.XXXXXXXX)
mkdir -p "$T3/logs" "$T3/screens" "$T3/wts"
mkmain "$T3/main"
for t in T1 T2 T3 T4; do mkdir -p "$T3/wts/$t/.claude"; done
printf 'T1=421\nT2=422\nT3=423\nT4=424\n' > "$T3/state.env"
export STUB_STOP_LOG=$T3/logs/claim.jsonl; : > "$STUB_STOP_LOG"
mkdir -p "$T3/main/.git/hooks"; : > "$T3/main/.git/hooks/pre-push"   # a hook already there: L2_PRE says present
OB=$T3 OB_MAIN=$T3/main STUB_WT_FAIL=1 PATH="$L/bin2:$PATH" timeout 60 bash "$here/setup-github.sh" > "$T3/out" 2>&1; rc3=$?
ck sg-wtfail-rc "$rc3" 1
case "$(cat "$T3/out")" in *'FAIL claim T1: worktree status <failed>'*) ck sg-wtfail-msg ok ok ;; *) ck sg-wtfail-msg "$(tail -2 "$T3/out" | tr '\n' '|')" 'FAIL claim T1: worktree status <failed>' ;; esac
ck sg-wtfail-no-probe "$([ ! -e "$T3/wts/T1/.claude/settings.local.json" ] && echo none)" none
ck sg-wtfail-l2-pre "$(OB=$T3 bash -c "source '$here/lib.sh'; state_get L2_PRE")" 'pre-push=present pre-push.launch-level=absent'

# 8. EXISTS refusal: worktrees whose settings.local.json already exists, state with WT paths recorded
rm -rf "$T3"; T3=$(mktemp -d /tmp/ob-sg2.XXXXXXXX)
mkdir -p "$T3/logs" "$T3/screens" "$T3/wts"
mkmain "$T3/main"
: > "$T3/state.env"
for t in T1 T2 T3 T4; do
  mkdir -p "$T3/wts/$t/.claude"
  cp "$T/wts/$t/.claude/settings.local.json" "$T3/wts/$t/.claude/settings.local.json"
done
for i in 1 2 3 4; do printf 'T%s=42%s\nWT_T%s=%s/wts/T%s\n' "$i" "$i" "$i" "$T3" "$i" >> "$T3/state.env"; done
export STUB_STOP_LOG=$T3/logs/claim.jsonl; : > "$STUB_STOP_LOG"
OB=$T3 OB_MAIN=$T3/main PATH="$L/bin2:$PATH" timeout 60 bash "$here/setup-github.sh" > "$T3/out" 2>&1; rc3=$?
case "$(cat "$T3/out")" in
  *EXISTS*) ck sg-exits-refused ok ok ;;
  *) ck sg-exits-refused "$(tail -1 "$T3/out")" "EXISTS: merge by hand" ;;
esac

# 9. OB_ONLY=T4: only that target is handled (no probe file for T1 to T3)
rm -rf "$T3"; T3=$(mktemp -d /tmp/ob-sg2.XXXXXXXX)
mkdir -p "$T3/logs" "$T3/screens" "$T3/wts"
mkmain "$T3/main"
for t in T1 T2 T3 T4; do mkdir -p "$T3/wts/$t/.claude"; done
printf 'T4=424\nWT_T4=%s/wts/T4\n' "$T3" > "$T3/state.env"
export STUB_STOP_LOG=$T3/logs/claim.jsonl; : > "$STUB_STOP_LOG"
OB=$T3 OB_MAIN=$T3/main OB_ONLY=T4 PATH="$L/bin2:$PATH" timeout 60 bash "$here/setup-github.sh" > "$T3/out" 2>&1; rc3=$?
ck sg-only-rc "$rc3" 0
ck sg-only-probe-t4 "$([ -e "$T3/wts/T4/.claude/settings.local.json" ] && echo yes)" yes
ck sg-only-no-probe-t1 "$([ ! -e "$T3/wts/T1/.claude/settings.local.json" ] && echo none)" none
rm -rf "$T3"

exit $failures
