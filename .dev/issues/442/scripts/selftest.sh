#!/usr/bin/env bash
# selftest.sh — harness for the #442 observation scripts.
# Later tasks append their cases to the case list below.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
failures=0

# --- harness primitives -----------------------------------------------------

begin() { printf 'BEGIN %s\n' "$1"; }
pass()  { printf 'OK %s\n' "$1"; }
fail()  { printf 'FAIL %s %s\n' "$1" "$2"; failures=$((failures+1)); }
skip()  { printf 'SKIP %s\n' "$1"; }

# Stub orca, gh, claude and uv: they log their arguments and print canned output.
# claude answers --version and -p; uv stands in for the P6 preflight.
setup_stubs() {
  STUB_DIR=$(mktemp -d /tmp/ob-selftest.XXXXXXXX)
  mkdir -p "$STUB_DIR/bin"
  cat > "$STUB_DIR/bin/orca" <<'STUB'
#!/usr/bin/env bash
L=${OB_STUB_LOG:-/tmp/ob-stub-disabled}
printf '%s\n' "$*" >> "$L/orca.log"
case "$1 $2" in
  'terminal create') printf '{"status":"ok","handle":"stub-handle"}\n' ;;
  'terminal read')
    s=$(cat "$L/screen.txt" 2>/dev/null || printf 'ok')
    # Real shape: lines under result.terminal.tail (see artifacts/t3-orca-help.txt).
    printf '{"result":{"terminal":{"tail":[%s]}}}\n' "$(printf '%s' "$s" | jq -Rs .)" ;;
  'terminal send')
    printf '%s\n' "${*:4}" >> "$L/sent.txt"
    if [ "${STUB_BLOCK:-0}" = 1 ]; then
      printf 'Blocked: new block\n' >> "$L/screen.txt" 2>/dev/null || printf 'Blocked: new block\n' > "$L/screen.txt"
    fi
    if [ -n "${STUB_STOP_LOG:-}" ] && [ "${STUB_STOP:-0}" = 1 ]; then
      printf '{"hook_event_name":"Stop"}\n' >> "$STUB_STOP_LOG"
      if [ "${STUB_NOTICE:-0}" = 1 ]; then
        # stage the notice pair: released one line per later wait poll, so a
        # wait-notice send first sees only its Stop and must keep waiting
        printf '%s\n%s\n' \
          '{"hook_event_name":"UserPromptSubmit","prompt":"<task-notification>approved"}' \
          '{"hook_event_name":"Stop"}' >> "$L/stages.txt"
      fi
    fi
    printf '{"status":"ok"}\n' ;;
  'terminal wait')
    # Release one staged log line per poll, so the driver sees events arriving
    # over time (stages.txt), then apply the idle-on signal.
    if [ -s "$L/stages.txt" ] && [ -n "${STUB_STOP_LOG:-}" ]; then
      head -1 "$L/stages.txt" >> "$STUB_STOP_LOG"
      tail -n +2 "$L/stages.txt" > "$L/stages.tmp" 2>/dev/null || : > "$L/stages.tmp"
      mv "$L/stages.tmp" "$L/stages.txt"
    fi
    [ -e "$L/idle-on" ] && exit 0
    exit 1 ;;
  *) printf '{"status":"ok"}\n' ;;
esac
STUB
  cat > "$STUB_DIR/bin/gh" <<'STUB'
#!/usr/bin/env bash
L=${OB_STUB_LOG:-/tmp/ob-stub-disabled}
printf '%s\n' "$*" >> "$L/gh.log"
case "$1 $2" in
  'issue create')
    n=$(( $(cat "$L/issue-n" 2>/dev/null || echo 420) + 1 )); printf '%s' "$n" > "$L/issue-n"
    # capture the --body-file content so a case can assert what the body says
    prev=""
    for a in "$@"; do
      [ "$prev" = "--body-file" ] && cat "$a" >> "$L/bodies.txt" 2>/dev/null
      prev=$a
    done
    printf 'https://github.com/IronbellyOrg/IronClaude/issues/%s\n' "$n" ;;
  *)  case "$1" in
        --version) printf 'gh version 0.0.0-stub\n' ;;
        issue) printf '{"number":421}\n' ;;
        api)  printf '{"protected":false}\n' ;;
        *)    printf '{"status":"ok"}\n' ;;
      esac ;;
esac
STUB
  cat > "$STUB_DIR/bin/claude" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${OB_STUB_LOG:-/dev/null}/claude.log"
case "$1" in
  --version) printf '0.0.0-stub (Claude Code)\n' ;;
  -p) printf 'ok\n' ;;
  *) printf 'ok\n' ;;
esac
STUB
  cat > "$STUB_DIR/bin/uv" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${OB_STUB_LOG:-/dev/null}/uv.log"
printf '[]\n'
STUB
  chmod 0755 "$STUB_DIR/bin/"*
  PATH="$STUB_DIR/bin:$PATH"
  export PATH
}

# --- case list (later tasks append before the summary) ----------------------

setup_stubs
T=${OB_STUB_LOG:-$STUB_DIR}
export OB_STUB_LOG=$T

# T1 cases: lib.sh (bounded, per the plan's timeout constraint)
timeout 60 bash "$here/lib-selftest.sh" || fail lib "lib-selftest exited $?"

# T2 cases: setup.sh under a fake HOME and a temp OB
timeout 120 bash "$here/setup-selftest.sh" || fail setup "setup-selftest exited $?"

# T3 cases: driver.sh against the state-machine stub (staged log releases)
timeout 120 bash "$here/driver-selftest.sh" || fail driver "driver-selftest exited $?"

# T4 cases: session A and A2 scripts
timeout 180 bash "$here/session-a-selftest.sh" || fail sessa "session-a-selftest exited $?"

# T5 cases: setup-github.sh
timeout 180 bash "$here/setup-github-selftest.sh" || fail sg "setup-github-selftest exited $?"

# T6 cases: session-gov.sh (sessions b to e)
timeout 300 bash "$here/session-gov-selftest.sh" || fail gov "session-gov-selftest exited $?"

# T7 cases: evidence.sh
timeout 300 bash "$here/evidence-selftest.sh" || fail evidence "evidence-selftest exited $?"

# T8 cases: cleanup.sh
timeout 300 bash "$here/cleanup-selftest.sh" || fail cleanup "cleanup-selftest exited $?"

# T9 cases: the runbook text and section 6
timeout 60 bash "$here/runbook-selftest.sh" || fail runbook "runbook-selftest exited $?"

# --- summary ----------------------------------------------------------------

if [ "$failures" -eq 0 ]; then
  printf 'SELFTEST_OK\n'
  exit 0
fi
printf 'SELFTEST_FAILED failures=%d\n' "$failures"
exit 1
