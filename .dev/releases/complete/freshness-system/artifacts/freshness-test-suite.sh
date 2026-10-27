#!/usr/bin/env bash
# freshness-test-suite.sh — interactive validation of the v1 freshness system.
#
# Drives each installed hook script with synthetic stdin (the same JSON shape
# Claude Code emits), checks the response (exit code + stderr + telemetry +
# state-file mutations) against documented expectations, and reports
# per-scenario PASS/FAIL with full diff on failure.
#
# Usage:
#   freshness-test-suite.sh                  # run all scenarios
#   freshness-test-suite.sh 3                # run only scenario 3
#   freshness-test-suite.sh --list           # list scenarios
#   freshness-test-suite.sh --source         # test source scripts (src/superclaude/hooks/scripts/) instead of installed
#   freshness-test-suite.sh --verbose        # print actual outputs even on PASS
#
# Each scenario runs in its own temp HOME so state from one doesn't leak into
# another, and the user's real ~/.claude/state is never touched.

set -u

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

VERBOSE=false
SOURCE_TREE=false
ONLY_SCENARIO=""
LIST_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --verbose|-v) VERBOSE=true ;;
        --source) SOURCE_TREE=true ;;
        --list) LIST_ONLY=true ;;
        --help|-h)
            sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        [0-9]*) ONLY_SCENARIO="$arg" ;;
        *)
            echo "Unknown argument: $arg" >&2
            exit 1
            ;;
    esac
done

if $SOURCE_TREE; then
    # script lives at .dev/releases/current/freshness-system/artifacts/ → 5 levels up to repo root
    REPO_ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
    HOOK_DIR="$REPO_ROOT/src/superclaude/hooks/scripts"
    HOOK_LABEL="source ($HOOK_DIR)"
else
    HOOK_DIR="$HOME/.claude/hooks"
    HOOK_LABEL="installed ($HOOK_DIR)"
fi

if [ ! -d "$HOOK_DIR" ]; then
    echo "FATAL: hook dir not found: $HOOK_DIR" >&2
    exit 1
fi

# Colors
if [ -t 1 ]; then
    RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YEL=$'\033[0;33m'; BLU=$'\033[0;34m'; RST=$'\033[0m'; BOLD=$'\033[1m'
else
    RED=""; GREEN=""; YEL=""; BLU=""; RST=""; BOLD=""
fi

# ---------------------------------------------------------------------------
# State (across scenarios)
# ---------------------------------------------------------------------------

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
FAIL_LIST=()

# ---------------------------------------------------------------------------
# Per-scenario helpers
# ---------------------------------------------------------------------------

setup_clean_home() {
    # Each scenario gets its own HOME with empty state.
    SCENARIO_HOME=$(mktemp -d -t freshness-test-XXXXXX)
    export HOME="$SCENARIO_HOME"
    mkdir -p "$HOME/.claude/state/turns" \
             "$HOME/.claude/state/last-prompt-ts" \
             "$HOME/.claude/state/bg-agents" \
             "$HOME/.claude/state/tool-call-counter" \
             "$HOME/.claude/logs"
}

cleanup_home() {
    [ -n "${SCENARIO_HOME:-}" ] && [ -d "$SCENARIO_HOME" ] && rm -rf "$SCENARIO_HOME"
    SCENARIO_HOME=""
}

# Compare actual vs expected; return 0 on match, 1 on mismatch.
# Args: $1=label  $2=expected  $3=actual
assert_eq() {
    local label="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        $VERBOSE && echo "    ${GREEN}✓${RST} $label = '$actual'"
        return 0
    else
        echo "    ${RED}✗${RST} $label"
        echo "      expected: $expected"
        echo "      actual:   $actual"
        return 1
    fi
}

assert_contains() {
    local label="$1" needle="$2" haystack="$3"
    if printf '%s' "$haystack" | grep -qF "$needle"; then
        $VERBOSE && echo "    ${GREEN}✓${RST} $label contains '$needle'"
        return 0
    else
        echo "    ${RED}✗${RST} $label does NOT contain '$needle'"
        echo "      haystack: $(printf '%s' "$haystack" | head -c 200)"
        return 1
    fi
}

scenario_start() {
    local num="$1" name="$2"
    if [ -n "$ONLY_SCENARIO" ] && [ "$ONLY_SCENARIO" != "$num" ]; then
        return 1  # caller should skip
    fi
    echo
    echo "${BOLD}${BLU}=== Scenario $num: $name ===${RST}"
    setup_clean_home
    return 0
}

scenario_end() {
    local num="$1" name="$2" failures="$3"
    if [ "$failures" -eq 0 ]; then
        echo "    ${GREEN}PASS${RST}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "    ${RED}FAIL${RST} ($failures assertion(s) failed)"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        FAIL_LIST+=("$num: $name")
    fi
    cleanup_home
}

# ---------------------------------------------------------------------------
# Scenario catalog
# ---------------------------------------------------------------------------

SCENARIOS=(
    "1|no_prior_read blocks (gate exits 2, factual stderr, block telemetry row)"
    "2|recent_read allows (gate exits 0, allow telemetry row)"
    "3|read_too_old blocks (Read 7200s ago, gate exits 2, read_too_old reason)"
    "4|post-read tracker appends 1 row for successful Read"
    "5|post-read tracker skips failed Read"
    "6|SessionStart startup envelope: valid JSON, source=startup tag"
    "7|SessionStart resume envelope: resumed_after field present"
    "8|UserPromptSubmit clean envelope: turn=1, minimal contents"
    "9|UserPromptSubmit active envelope: Δ + git dirty + bg + delta-trigger fields"
    "10|UserPromptSubmit RESUMED flag at Δ≥3600s"
    "11|Subagent counters: 3 start + 2 stop = 1 (linear)"
    "12|Subagent counters: stop floors at 0 (never negative)"
    "13|Subagent counters: parallel start-then-stop phases (-P 10) = expected"
    "14|Telemetry rows: all JSON-parseable; all required keys present"
    "15|v1 limitation: Write to nonexistent file is blocked (expected v1 behavior)"
)

if $LIST_ONLY; then
    echo "Available scenarios (target: $HOOK_LABEL):"
    for s in "${SCENARIOS[@]}"; do
        num="${s%%|*}"; name="${s#*|}"
        printf "  %2d. %s\n" "$num" "$name"
    done
    exit 0
fi

# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

run_scenario_1() {
    scenario_start 1 "no_prior_read blocks" || return 0
    local failures=0
    local stdin='{"session_id":"S1","tool_name":"Edit","tool_input":{"file_path":"/tmp/never-read.go"}}'
    local stderr_file=$(mktemp)
    printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-pre-edit.sh" 2>"$stderr_file"
    local rc=$?
    local stderr_content=$(cat "$stderr_file")
    rm -f "$stderr_file"

    assert_eq "exit code" "2" "$rc" || failures=$((failures + 1))
    assert_contains "stderr factual phrasing" "You have not Read \`/tmp/never-read.go\`" "$stderr_content" || failures=$((failures + 1))

    # Telemetry row
    local rows=$(wc -l < "$HOME/.claude/logs/freshness-hook.jsonl" 2>/dev/null || echo 0)
    assert_eq "telemetry rows" "1" "$rows" || failures=$((failures + 1))
    local reason=$(jq -r '.reason' "$HOME/.claude/logs/freshness-hook.jsonl" 2>/dev/null)
    assert_eq "block reason" "no_prior_read" "$reason" || failures=$((failures + 1))

    scenario_end 1 "no_prior_read blocks" "$failures"
}

run_scenario_2() {
    scenario_start 2 "recent_read allows" || return 0
    local failures=0
    local now=$(date +%s)
    local recent=$((now - 60))
    printf '{"ts":"r","ts_unix":%d,"session_id":"S2","path":"/tmp/r.go","tool_call_idx":1}\n' "$recent" > "$HOME/.claude/state/reads.jsonl"

    local stdin='{"session_id":"S2","tool_name":"Edit","tool_input":{"file_path":"/tmp/r.go"}}'
    local stderr_file=$(mktemp)
    printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-pre-edit.sh" 2>"$stderr_file"
    local rc=$?
    rm -f "$stderr_file"

    assert_eq "exit code" "0" "$rc" || failures=$((failures + 1))
    local decision=$(jq -r '.decision' "$HOME/.claude/logs/freshness-hook.jsonl" 2>/dev/null)
    assert_eq "decision" "allow" "$decision" || failures=$((failures + 1))
    local reason=$(jq -r '.reason' "$HOME/.claude/logs/freshness-hook.jsonl" 2>/dev/null)
    assert_eq "reason" "recent_read" "$reason" || failures=$((failures + 1))

    scenario_end 2 "recent_read allows" "$failures"
}

run_scenario_3() {
    scenario_start 3 "read_too_old blocks" || return 0
    local failures=0
    local now=$(date +%s)
    local stale=$((now - 7200))   # 2 hours ago, well beyond 30-min horizon
    printf '{"ts":"r","ts_unix":%d,"session_id":"S3","path":"/tmp/old.go","tool_call_idx":1}\n' "$stale" > "$HOME/.claude/state/reads.jsonl"

    local stdin='{"session_id":"S3","tool_name":"Edit","tool_input":{"file_path":"/tmp/old.go"}}'
    local stderr_file=$(mktemp)
    printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-pre-edit.sh" 2>"$stderr_file"
    local rc=$?
    local stderr_content=$(cat "$stderr_file"); rm -f "$stderr_file"

    assert_eq "exit code" "2" "$rc" || failures=$((failures + 1))
    assert_contains "stderr horizon mention" "beyond the 30-minute freshness horizon" "$stderr_content" || failures=$((failures + 1))
    local reason=$(jq -r '.reason' "$HOME/.claude/logs/freshness-hook.jsonl" 2>/dev/null)
    assert_eq "block reason" "read_too_old" "$reason" || failures=$((failures + 1))
    local age=$(jq -r '.recent_read_age_sec' "$HOME/.claude/logs/freshness-hook.jsonl" 2>/dev/null)
    # Age should be ~7200
    if [ -n "$age" ] && [ "$age" -ge 7195 ] && [ "$age" -le 7205 ]; then
        $VERBOSE && echo "    ${GREEN}✓${RST} recent_read_age_sec in [7195,7205]: $age"
    else
        echo "    ${RED}✗${RST} recent_read_age_sec out of range: $age"
        failures=$((failures + 1))
    fi

    scenario_end 3 "read_too_old blocks" "$failures"
}

run_scenario_4() {
    scenario_start 4 "post-read appends 1 row for success" || return 0
    local failures=0
    local stdin='{"session_id":"PR4","tool_name":"Read","tool_input":{"file_path":"/tmp/p.go"},"tool_response":{"success":true}}'
    printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-post-read.sh"

    local rows=$(wc -l < "$HOME/.claude/state/reads.jsonl" 2>/dev/null || echo 0)
    assert_eq "rows in reads.jsonl" "1" "$rows" || failures=$((failures + 1))
    local path=$(jq -r '.path' "$HOME/.claude/state/reads.jsonl" 2>/dev/null)
    assert_eq "path field" "/tmp/p.go" "$path" || failures=$((failures + 1))
    local sid=$(jq -r '.session_id' "$HOME/.claude/state/reads.jsonl" 2>/dev/null)
    assert_eq "session_id field" "PR4" "$sid" || failures=$((failures + 1))

    scenario_end 4 "post-read appends 1 row for success" "$failures"
}

run_scenario_5() {
    scenario_start 5 "post-read skips failed Read" || return 0
    local failures=0
    local stdin='{"session_id":"PR5","tool_name":"Read","tool_input":{"file_path":"/tmp/fail.go"},"tool_response":{"success":false,"error":"ENOENT"}}'
    printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-post-read.sh"

    if [ -f "$HOME/.claude/state/reads.jsonl" ]; then
        local rows=$(wc -l < "$HOME/.claude/state/reads.jsonl")
        assert_eq "rows in reads.jsonl" "0" "$rows" || failures=$((failures + 1))
    else
        $VERBOSE && echo "    ${GREEN}✓${RST} reads.jsonl not created (failed Read correctly skipped)"
    fi

    scenario_end 5 "post-read skips failed Read" "$failures"
}

run_scenario_6() {
    scenario_start 6 "SessionStart startup envelope" || return 0
    local failures=0
    local stdin='{"session_id":"SS6","source":"startup","cwd":"/tmp","model":"claude-opus"}'
    local out=$(printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-session-start.sh" 2>/dev/null)

    if ! printf '%s' "$out" | jq -e . >/dev/null 2>&1; then
        echo "    ${RED}✗${RST} output is not valid JSON: $out"
        failures=$((failures + 1))
    else
        local ctx=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.additionalContext')
        assert_contains "envelope source" 'source="startup"' "$ctx" || failures=$((failures + 1))
        assert_contains "envelope cwd" "cwd=/tmp" "$ctx" || failures=$((failures + 1))
    fi

    scenario_end 6 "SessionStart startup envelope" "$failures"
}

run_scenario_7() {
    scenario_start 7 "SessionStart resume envelope (resumed_after present)" || return 0
    local failures=0
    # Synthesize a 7200s-old last-prompt-ts
    date -d "@$(($(date +%s) - 7200))" -Iseconds > "$HOME/.claude/state/last-prompt-ts/SS7.txt"

    local stdin='{"session_id":"SS7","source":"resume","cwd":"/tmp"}'
    local out=$(printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-session-start.sh" 2>/dev/null)
    local ctx=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.additionalContext' 2>/dev/null)

    assert_contains "envelope source" 'source="resume"' "$ctx" || failures=$((failures + 1))
    assert_contains "resumed_after field" "resumed_after=" "$ctx" || failures=$((failures + 1))

    scenario_end 7 "SessionStart resume envelope" "$failures"
}

run_scenario_8() {
    scenario_start 8 "UserPromptSubmit clean envelope" || return 0
    local failures=0
    local stdin='{"session_id":"UP8","prompt":"hi","cwd":"/tmp","permission_mode":"default"}'
    local out=$(printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-user-prompt.sh" 2>/dev/null)
    local ctx=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.additionalContext' 2>/dev/null)

    assert_contains "envelope opens" "<session-context>" "$ctx" || failures=$((failures + 1))
    assert_contains "turn=1" "turn=1" "$ctx" || failures=$((failures + 1))
    # Should NOT have conditional items
    if printf '%s' "$ctx" | grep -qE "Δ=|mode=plan|bg=|dirty="; then
        echo "    ${RED}✗${RST} clean envelope unexpectedly contains conditional items"
        failures=$((failures + 1))
    else
        $VERBOSE && echo "    ${GREEN}✓${RST} no conditional items (as expected for clean state)"
    fi

    scenario_end 8 "UserPromptSubmit clean envelope" "$failures"
}

run_scenario_9() {
    scenario_start 9 "UserPromptSubmit active envelope (Δ + mode)" || return 0
    local failures=0
    # Synthesize 600s-old prompt
    date -d "@$(($(date +%s) - 600))" -Iseconds > "$HOME/.claude/state/last-prompt-ts/UP9.txt"
    echo "5" > "$HOME/.claude/state/bg-agents/UP9.txt"

    local stdin='{"session_id":"UP9","prompt":"work","cwd":"/tmp","permission_mode":"plan"}'
    local out=$(printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-user-prompt.sh" 2>/dev/null)
    local ctx=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.additionalContext' 2>/dev/null)

    assert_contains "Δ field" "Δ=10:00" "$ctx" || failures=$((failures + 1))
    assert_contains "mode=plan" "mode=plan" "$ctx" || failures=$((failures + 1))
    assert_contains "bg=5" "bg=5" "$ctx" || failures=$((failures + 1))

    scenario_end 9 "UserPromptSubmit active envelope" "$failures"
}

run_scenario_10() {
    scenario_start 10 "UserPromptSubmit RESUMED at Δ≥3600s" || return 0
    local failures=0
    date -d "@$(($(date +%s) - 7200))" -Iseconds > "$HOME/.claude/state/last-prompt-ts/UP10.txt"

    local stdin='{"session_id":"UP10","prompt":"x","cwd":"/tmp","permission_mode":"default"}'
    local out=$(printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-user-prompt.sh" 2>/dev/null)
    local ctx=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.additionalContext' 2>/dev/null)

    assert_contains "Δ HH:MM:SS format" "Δ=02:00:00" "$ctx" || failures=$((failures + 1))
    assert_contains "RESUMED flag" "RESUMED_AFTER_LONG_PAUSE" "$ctx" || failures=$((failures + 1))

    scenario_end 10 "UserPromptSubmit RESUMED" "$failures"
}

run_scenario_11() {
    scenario_start 11 "Subagent: 3 start + 2 stop = 1" || return 0
    local failures=0
    for i in 1 2 3; do
        printf '{"session_id":"SC11"}' | bash "$HOOK_DIR/freshness-subagent-start.sh"
    done
    for i in 1 2; do
        printf '{"session_id":"SC11"}' | bash "$HOOK_DIR/freshness-subagent-stop.sh"
    done
    local count=$(cat "$HOME/.claude/state/bg-agents/SC11.txt" 2>/dev/null)
    assert_eq "counter value" "1" "$count" || failures=$((failures + 1))

    scenario_end 11 "Subagent 3-2" "$failures"
}

run_scenario_12() {
    scenario_start 12 "Subagent: stops floored at 0" || return 0
    local failures=0
    echo "2" > "$HOME/.claude/state/bg-agents/SC12.txt"
    for i in 1 2 3 4 5; do
        printf '{"session_id":"SC12"}' | bash "$HOOK_DIR/freshness-subagent-stop.sh"
    done
    local count=$(cat "$HOME/.claude/state/bg-agents/SC12.txt" 2>/dev/null)
    assert_eq "floored counter" "0" "$count" || failures=$((failures + 1))

    scenario_end 12 "Subagent floor at 0" "$failures"
}

run_scenario_13() {
    scenario_start 13 "Subagent: parallel phases (-P 10) = expected" || return 0
    local failures=0
    echo "0" > "$HOME/.claude/state/bg-agents/SC13.txt"
    seq 1 30 | xargs -P 10 -I{} sh -c "printf '{\"session_id\":\"SC13\"}' | bash '$HOOK_DIR/freshness-subagent-start.sh'"
    seq 1 20 | xargs -P 10 -I{} sh -c "printf '{\"session_id\":\"SC13\"}' | bash '$HOOK_DIR/freshness-subagent-stop.sh'"
    local count=$(cat "$HOME/.claude/state/bg-agents/SC13.txt" 2>/dev/null)
    assert_eq "counter (30 start, then 20 stop)" "10" "$count" || failures=$((failures + 1))

    scenario_end 13 "Subagent parallel" "$failures"
}

run_scenario_14() {
    scenario_start 14 "Telemetry rows: JSON valid + required keys" || return 0
    local failures=0
    # Generate a few rows by running 2 gate decisions
    local now=$(date +%s)
    printf '{"ts":"r","ts_unix":%d,"session_id":"T14","path":"/tmp/a.go","tool_call_idx":1}\n' $((now - 30)) > "$HOME/.claude/state/reads.jsonl"

    printf '{"session_id":"T14","tool_name":"Edit","tool_input":{"file_path":"/tmp/a.go"}}' | bash "$HOOK_DIR/freshness-pre-edit.sh" 2>/dev/null
    printf '{"session_id":"T14","tool_name":"Edit","tool_input":{"file_path":"/tmp/b.go"}}' | bash "$HOOK_DIR/freshness-pre-edit.sh" 2>/dev/null

    local log="$HOME/.claude/logs/freshness-hook.jsonl"
    local rows=$(wc -l < "$log")
    assert_eq "row count" "2" "$rows" || failures=$((failures + 1))

    local all_valid=$(jq -c . "$log" 2>/dev/null | wc -l)
    assert_eq "all rows parse as JSON" "2" "$all_valid" || failures=$((failures + 1))

    # Required keys per design §2.2
    local missing=$(jq -r 'select(.ts==null or .event==null or .decision==null or .reason==null or .session_id==null or .tool_call_idx==null) | "MISSING"' "$log" 2>/dev/null | head -1)
    if [ -n "$missing" ]; then
        echo "    ${RED}✗${RST} at least one row missing required key (ts/event/decision/reason/session_id/tool_call_idx)"
        failures=$((failures + 1))
    else
        $VERBOSE && echo "    ${GREEN}✓${RST} all rows have required keys"
    fi

    # Decision values must be in enum
    local bad=$(jq -r '.decision' "$log" 2>/dev/null | grep -vE '^(allow|block)$' | head -1)
    if [ -n "$bad" ]; then
        echo "    ${RED}✗${RST} unexpected decision value: $bad"
        failures=$((failures + 1))
    fi

    scenario_end 14 "Telemetry schema" "$failures"
}

run_scenario_15() {
    scenario_start 15 "v1 limitation: Write to nonexistent file blocked" || return 0
    local failures=0
    # The gate blocks any Write without prior Read, regardless of file existence.
    # This documents the v1 behavior; F10 / v1.5 work item.
    local stdin='{"session_id":"NX15","tool_name":"Write","tool_input":{"file_path":"/tmp/this-file-does-not-exist-anywhere.go"}}'
    local stderr_file=$(mktemp)
    printf '%s' "$stdin" | bash "$HOOK_DIR/freshness-pre-edit.sh" 2>"$stderr_file"
    local rc=$?
    local stderr_content=$(cat "$stderr_file"); rm -f "$stderr_file"

    assert_eq "exit code (v1: blocks)" "2" "$rc" || failures=$((failures + 1))
    assert_contains "stderr" "have not Read" "$stderr_content" || failures=$((failures + 1))
    echo "    ${YEL}NOTE${RST} this confirms the documented v1 limitation. A v1.5 refinement may allow Write when target path does not exist."

    scenario_end 15 "Write-to-new-file blocked" "$failures"
}

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

echo "${BOLD}Freshness Test Suite${RST}"
echo "Target: $HOOK_LABEL"
echo "Verbose: $VERBOSE"
echo

run_scenario_1
run_scenario_2
run_scenario_3
run_scenario_4
run_scenario_5
run_scenario_6
run_scenario_7
run_scenario_8
run_scenario_9
run_scenario_10
run_scenario_11
run_scenario_12
run_scenario_13
run_scenario_14
run_scenario_15

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo
echo "${BOLD}=== Summary ===${RST}"
echo "PASS: $PASS_COUNT"
echo "FAIL: $FAIL_COUNT"
if [ "$FAIL_COUNT" -gt 0 ]; then
    echo
    echo "${RED}Failed scenarios:${RST}"
    for f in "${FAIL_LIST[@]}"; do
        echo "  - $f"
    done
fi

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo
    echo "${GREEN}${BOLD}All scenarios passed.${RST}"
    exit 0
else
    exit 1
fi
