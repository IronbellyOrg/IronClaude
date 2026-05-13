#!/usr/bin/env bash
# freshness-realworld-test.sh — real-world end-to-end validation.
#
# Each scenario spawns a real `claude -p` session, observes its actual response
# AND the hook side effects (state files + telemetry rows filtered by session_id),
# then asserts expected vs actual.
#
# Unlike freshness-test-suite.sh (which is a unit test of the scripts), this
# exercises Claude Code itself: does it fire the hooks, respect exit 2, retry
# after blocks, and inject the <session-context> envelope into prompts?
#
# Cost: each scenario makes API calls. Bounded with --max-budget-usd 2 per call.
# 5 scenarios ≈ $1-3 total under typical loads.
#
# Usage:
#   freshness-realworld-test.sh                 # run all scenarios
#   freshness-realworld-test.sh 2               # run only scenario 2
#   freshness-realworld-test.sh --list          # list scenarios
#   freshness-realworld-test.sh --dry-run       # print prompts/setup, don't spawn claude
#   freshness-realworld-test.sh --keep-state    # don't clean up synthetic session state
#   freshness-realworld-test.sh --verbose       # show full claude responses

set -u

# ---------------------------------------------------------------------------
# Arguments
# ---------------------------------------------------------------------------

VERBOSE=false
DRY_RUN=false
KEEP_STATE=false
ONLY_SCENARIO=""
LIST_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --verbose|-v) VERBOSE=true ;;
        --dry-run) DRY_RUN=true ;;
        --keep-state) KEEP_STATE=true ;;
        --list) LIST_ONLY=true ;;
        --help|-h)
            sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        [0-9]*) ONLY_SCENARIO="$arg" ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

# Colors
if [ -t 1 ]; then
    RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YEL=$'\033[0;33m'; BLU=$'\033[0;34m'; CYA=$'\033[0;36m'; RST=$'\033[0m'; BOLD=$'\033[1m'
else
    RED=""; GREEN=""; YEL=""; BLU=""; CYA=""; RST=""; BOLD=""
fi

# Sanity: claude on PATH?
if ! command -v claude >/dev/null 2>&1; then
    echo "FATAL: 'claude' CLI not on PATH" >&2
    exit 1
fi

# Sanity: hooks installed?
if [ ! -f "$HOME/.claude/hooks/freshness-pre-edit.sh" ]; then
    echo "FATAL: freshness hooks not installed at ~/.claude/hooks/" >&2
    echo "       run: cd <repo> && make sync-dev && uv run superclaude install --force" >&2
    exit 1
fi

TELEMETRY="$HOME/.claude/logs/freshness-hook.jsonl"
STATE_DIR="$HOME/.claude/state"

# ---------------------------------------------------------------------------
# Tracking
# ---------------------------------------------------------------------------

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
FAIL_LIST=()
ALL_SESSION_IDS=()

new_session_id() {
    if command -v uuidgen >/dev/null 2>&1; then
        uuidgen | tr 'A-Z' 'a-z'
    else
        python3 -c "import uuid; print(uuid.uuid4())"
    fi
}

cleanup_session_state() {
    local sid="$1"
    [ -z "$sid" ] && return 0
    rm -f "$STATE_DIR/turns/$sid.txt" \
          "$STATE_DIR/turns/$sid.txt.lock" \
          "$STATE_DIR/last-prompt-ts/$sid.txt" \
          "$STATE_DIR/bg-agents/$sid.txt" \
          "$STATE_DIR/bg-agents/$sid.txt.lock" \
          "$STATE_DIR/tool-call-counter/$sid.txt" \
          "$STATE_DIR/tool-call-counter/$sid.txt.lock" 2>/dev/null
}

assert_eq() {
    local label="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "    ${GREEN}✓${RST} $label = '$actual'"
        return 0
    else
        echo "    ${RED}✗${RST} $label"
        echo "      expected: $expected"
        echo "      actual:   $actual"
        return 1
    fi
}

assert_ge() {
    local label="$1" min="$2" actual="$3"
    if [ "$actual" -ge "$min" ] 2>/dev/null; then
        echo "    ${GREEN}✓${RST} $label = $actual (≥ $min)"
        return 0
    else
        echo "    ${RED}✗${RST} $label = $actual (expected ≥ $min)"
        return 1
    fi
}

assert_contains() {
    local label="$1" needle="$2" haystack="$3"
    if printf '%s' "$haystack" | grep -qF "$needle"; then
        echo "    ${GREEN}✓${RST} $label contains '$needle'"
        return 0
    else
        echo "    ${RED}✗${RST} $label does NOT contain '$needle'"
        echo "      first 300 chars of haystack: $(printf '%s' "$haystack" | head -c 300)"
        return 1
    fi
}

# Spawn a real claude -p session and capture its JSON output + telemetry delta.
# Sets: CLAUDE_OUTPUT, CLAUDE_RC, NEW_TELEMETRY_ROWS (array of JSON lines, filtered by session_id)
run_claude() {
    local sid="$1" fixture_dir="$2" prompt="$3"
    local pre_rows
    pre_rows=$(wc -l < "$TELEMETRY" 2>/dev/null || echo 0)

    echo "  ${CYA}→${RST} claude -p --session-id $sid --add-dir $fixture_dir"
    echo "    prompt: $(printf '%s' "$prompt" | head -c 200)$([ ${#prompt} -gt 200 ] && echo '…')"

    if $DRY_RUN; then
        echo "  ${YEL}(dry-run: not spawning)${RST}"
        CLAUDE_OUTPUT=""
        CLAUDE_RC=0
        NEW_TELEMETRY_ROWS=""
        return 0
    fi

    # Capture output and exit code
    local raw
    raw=$(claude -p \
        --session-id "$sid" \
        --add-dir "$fixture_dir" \
        --dangerously-skip-permissions \
        --output-format json \
        --max-budget-usd 2 \
        --no-session-persistence \
        "$prompt" 2>&1) || true
    CLAUDE_RC=$?
    CLAUDE_OUTPUT="$raw"

    # Filter new telemetry rows by session_id
    local post_rows
    post_rows=$(wc -l < "$TELEMETRY" 2>/dev/null || echo 0)
    local delta=$((post_rows - pre_rows))
    if [ "$delta" -gt 0 ]; then
        NEW_TELEMETRY_ROWS=$(tail -n "$delta" "$TELEMETRY" | jq -c --arg s "$sid" 'select(.session_id == $s)')
    else
        NEW_TELEMETRY_ROWS=""
    fi
}

extract_response_text() {
    # claude -p --output-format json emits a top-level object with a "result" field
    # (the assistant's final response). Falls back to raw if not parseable.
    printf '%s' "$1" | jq -r '.result // .text // empty' 2>/dev/null || printf '%s' "$1"
}

scenario_start() {
    local num="$1" name="$2"
    if [ -n "$ONLY_SCENARIO" ] && [ "$ONLY_SCENARIO" != "$num" ]; then
        return 1
    fi
    echo
    echo "${BOLD}${BLU}=== Scenario $num: $name ===${RST}"
    return 0
}

scenario_end() {
    local num="$1" name="$2" failures="$3"
    if [ "$failures" -eq 0 ]; then
        echo "    ${GREEN}${BOLD}PASS${RST}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "    ${RED}${BOLD}FAIL${RST} ($failures assertion(s))"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        FAIL_LIST+=("$num: $name")
    fi
}

# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

SCENARIOS=(
    "1|Read-only request: Claude Reads, no PreToolUse rows fire"
    "2|Block-then-recover: Claude tries Edit on unread file, hook blocks, Claude Reads, retries, succeeds"
    "3|Session-context envelope: Claude can see and quote its <session-context> block"
    "4|Fresh-session state initialization: state files created with this session's UUID"
    "5|Subagent counter: spawn a Task, counter goes up and back to 0"
)

if $LIST_ONLY; then
    echo "Available real-world scenarios:"
    for s in "${SCENARIOS[@]}"; do
        num="${s%%|*}"; name="${s#*|}"
        printf "  %d. %s\n" "$num" "$name"
    done
    echo
    echo "All scenarios spawn real Claude Code sessions via 'claude -p'."
    echo "Each is capped at \$2 via --max-budget-usd."
    exit 0
fi

run_scenario_1() {
    scenario_start 1 "Read-only request" || return 0
    local failures=0
    local sid
    sid=$(new_session_id)
    ALL_SESSION_IDS+=("$sid")
    local fixture=$(mktemp -d -t rwtest1-XXXX)
    cat > "$fixture/notes.txt" <<EOF
Project: example
Owner: alice@example.com
Port: 8080
EOF
    run_claude "$sid" "$fixture" "Read the file $fixture/notes.txt and tell me what port the project uses. Don't edit anything."

    local resp
    resp=$(extract_response_text "$CLAUDE_OUTPUT")
    assert_contains "response mentions port 8080" "8080" "$resp" || failures=$((failures + 1))

    # Reads.jsonl should gain at least 1 row for this session
    local read_rows
    read_rows=$(jq -c --arg s "$sid" 'select(.session_id == $s)' "$STATE_DIR/reads.jsonl" 2>/dev/null | wc -l)
    assert_ge "reads.jsonl rows for this session" 1 "$read_rows" || failures=$((failures + 1))

    # PreToolUse rows for this session: should be 0 (no Edit attempts)
    local block_rows
    block_rows=$(printf '%s\n' "$NEW_TELEMETRY_ROWS" | jq -c 'select(.event == "PreToolUse")' 2>/dev/null | grep -v '^$' | wc -l | tr -d ' ')
    assert_eq "PreToolUse rows for this session" "0" "$block_rows" || failures=$((failures + 1))

    rm -rf "$fixture"
    scenario_end 1 "Read-only request" "$failures"
}

run_scenario_2() {
    scenario_start 2 "Stale-read forces block-then-recover (read_too_old)" || return 0
    local failures=0
    local sid
    sid=$(new_session_id)
    ALL_SESSION_IDS+=("$sid")
    local fixture=$(mktemp -d -t rwtest2-XXXX)
    cat > "$fixture/greeting.txt" <<EOF
hello world
goodbye for now
EOF

    # ─── Turn 1: have Claude Read the file (creates reads.jsonl entry) ───────
    echo "  ${CYA}step 1/3${RST} Claude Reads the file (turn 1)"
    if ! $DRY_RUN; then
        claude -p \
            --session-id "$sid" \
            --add-dir "$fixture" \
            --dangerously-skip-permissions \
            --output-format json \
            --max-budget-usd 1 \
            "Read $fixture/greeting.txt and tell me the first word. Reply with only that word." \
            >/dev/null 2>&1 || true
    fi
    # Confirm Read landed in reads.jsonl
    local read_rows
    read_rows=$(jq -c --arg s "$sid" 'select(.session_id == $s)' "$STATE_DIR/reads.jsonl" 2>/dev/null | grep -v '^$' | wc -l | tr -d ' ')
    [ -z "$read_rows" ] && read_rows=0
    if $DRY_RUN; then
        echo "    ${YEL}(dry-run: skipping read assertion)${RST}"
    else
        assert_ge "reads.jsonl rows for this session after Read" 1 "$read_rows" || failures=$((failures + 1))
    fi

    # ─── Mutate reads.jsonl to backdate this session's Read by 7200s ─────────
    echo "  ${CYA}step 2/3${RST} Backdate the Read timestamp by 7200s (forces read_too_old)"
    if ! $DRY_RUN; then
        local now_ts=$(date +%s)
        local stale_ts=$((now_ts - 7200))
        local stale_iso=$(date -d "@$stale_ts" -Iseconds)
        local tmp=$(mktemp)
        jq -c --arg s "$sid" --argjson t "$stale_ts" --arg iso "$stale_iso" \
            'if .session_id == $s then .ts_unix = $t | .ts = $iso else . end' \
            "$STATE_DIR/reads.jsonl" > "$tmp"
        cp "$tmp" "$STATE_DIR/reads.jsonl"
        rm -f "$tmp"
    fi

    # ─── Turn 2: resume the same session and ask for an Edit ──────────────────
    echo "  ${CYA}step 3/3${RST} Resume same session, request Edit"
    local pre_telemetry=$(wc -l < "$TELEMETRY" 2>/dev/null || echo 0)
    if ! $DRY_RUN; then
        # --resume <sid> with same --session-id continues the conversation; Claude
        # still "remembers" Reading in turn 1 (so the Edit tool's built-in check
        # passes), but the gate sees a 7200s-old reads.jsonl entry and blocks.
        local resp
        resp=$(claude -p \
            --resume "$sid" \
            --add-dir "$fixture" \
            --dangerously-skip-permissions \
            --output-format json \
            --max-budget-usd 2 \
            "Now edit $fixture/greeting.txt to change 'hello' to 'howdy'." 2>&1 || true)
        if $VERBOSE; then
            echo "    --- turn 2 response (first 400 chars) ---"
            extract_response_text "$resp" | head -c 400
            echo
            echo "    --- end ---"
        fi
    fi

    # Filter telemetry rows added during turn 2 for this session
    local post_telemetry=$(wc -l < "$TELEMETRY" 2>/dev/null || echo 0)
    local delta=$((post_telemetry - pre_telemetry))
    local new_rows=""
    if [ "$delta" -gt 0 ]; then
        new_rows=$(tail -n "$delta" "$TELEMETRY" | jq -c --arg s "$sid" 'select(.session_id == $s)' 2>/dev/null)
    fi

    # Assert: file content changed (Edit eventually succeeded)
    local content=$(cat "$fixture/greeting.txt" 2>/dev/null || true)
    if $DRY_RUN; then
        :
    else
        assert_contains "file content changed" "howdy" "$content" || failures=$((failures + 1))
    fi

    # Assert: at least one block row with reason=read_too_old in turn 2
    local block_count
    block_count=$(printf '%s\n' "$new_rows" | jq -c 'select(.decision == "block" and .reason == "read_too_old")' 2>/dev/null | grep -v '^$' | wc -l | tr -d ' ')
    [ -z "$block_count" ] && block_count=0
    if $DRY_RUN; then
        echo "    ${YEL}(dry-run: skipping telemetry assertions)${RST}"
    else
        assert_ge "block rows (read_too_old) in turn 2" 1 "$block_count" || failures=$((failures + 1))
    fi

    # Assert: at least one allow row after Claude re-Read
    local allow_count
    allow_count=$(printf '%s\n' "$new_rows" | jq -c 'select(.decision == "allow" and .reason == "recent_read")' 2>/dev/null | grep -v '^$' | wc -l | tr -d ' ')
    [ -z "$allow_count" ] && allow_count=0
    if ! $DRY_RUN; then
        assert_ge "allow rows (recent_read) after recovery" 1 "$allow_count" || failures=$((failures + 1))
    fi

    if $VERBOSE && ! $DRY_RUN; then
        echo "    --- All turn-2 telemetry rows for $sid: ---"
        printf '%s\n' "$new_rows" | jq -c '{decision,reason,tool,path,recent_read_age_sec}'
    fi

    rm -rf "$fixture"
    scenario_end 2 "Stale-read forces block-then-recover" "$failures"
}

run_scenario_3() {
    scenario_start 3 "Envelope visibility" || return 0
    local failures=0
    local sid
    sid=$(new_session_id)
    ALL_SESSION_IDS+=("$sid")
    local fixture=$(mktemp -d -t rwtest3-XXXX)

    # Claude should be able to "see" the UserPromptSubmit-injected envelope
    # because it lives in the prompt context. Asking it to quote the literal
    # turn=N from its session-context tests that the hook injected and
    # Claude observed it.
    run_claude "$sid" "$fixture" \
        "Without using any tools, tell me exactly what the value of 'turn=' is in the <session-context> block injected before this prompt. Reply with just the number, nothing else."

    local resp
    resp=$(extract_response_text "$CLAUDE_OUTPUT")
    if $VERBOSE; then
        echo "    --- response ---"
        printf '%s\n' "$resp"
        echo "    --- end ---"
    fi
    # Should contain "1" (first turn of this session)
    if printf '%s' "$resp" | grep -qE '\b1\b'; then
        echo "    ${GREEN}✓${RST} response cites turn=1"
    else
        echo "    ${RED}✗${RST} response did NOT cite turn=1 — envelope may not be reaching the assistant"
        echo "      response: $(printf '%s' "$resp" | head -c 300)"
        failures=$((failures + 1))
    fi

    rm -rf "$fixture"
    scenario_end 3 "Envelope visibility" "$failures"
}

run_scenario_4() {
    scenario_start 4 "Fresh-session state initialization" || return 0
    local failures=0
    local sid
    sid=$(new_session_id)
    ALL_SESSION_IDS+=("$sid")
    local fixture=$(mktemp -d -t rwtest4-XXXX)

    run_claude "$sid" "$fixture" "Reply with 'ok' and nothing else."

    # State files for this session should now exist
    if [ -f "$STATE_DIR/turns/$sid.txt" ]; then
        echo "    ${GREEN}✓${RST} turns/$sid.txt exists"
    else
        echo "    ${RED}✗${RST} turns/$sid.txt MISSING (SessionStart hook should have created it)"
        failures=$((failures + 1))
    fi
    if [ -f "$STATE_DIR/tool-call-counter/$sid.txt" ]; then
        echo "    ${GREEN}✓${RST} tool-call-counter/$sid.txt exists"
    else
        echo "    ${RED}✗${RST} tool-call-counter/$sid.txt MISSING"
        failures=$((failures + 1))
    fi
    if [ -f "$STATE_DIR/bg-agents/$sid.txt" ]; then
        echo "    ${GREEN}✓${RST} bg-agents/$sid.txt exists"
    else
        echo "    ${RED}✗${RST} bg-agents/$sid.txt MISSING"
        failures=$((failures + 1))
    fi

    local turn_val
    turn_val=$(cat "$STATE_DIR/turns/$sid.txt" 2>/dev/null || echo "?")
    assert_eq "turn counter after 1 user prompt" "1" "$turn_val" || failures=$((failures + 1))

    rm -rf "$fixture"
    scenario_end 4 "Fresh-session state init" "$failures"
}

run_scenario_5() {
    scenario_start 5 "Subagent counter" || return 0
    local failures=0
    local sid
    sid=$(new_session_id)
    ALL_SESSION_IDS+=("$sid")
    local fixture=$(mktemp -d -t rwtest5-XXXX)

    run_claude "$sid" "$fixture" \
        "Use the Task tool with subagent_type 'general-purpose' to count the number of files in $fixture. Then tell me the count. Use exactly one Task call."

    # After the subagent has completed (Stop fired), counter should be 0.
    # If still running for some reason, it'd be >=1. Since claude -p is
    # synchronous-by-completion, the subagent should have finished.
    local bg
    bg=$(cat "$STATE_DIR/bg-agents/$sid.txt" 2>/dev/null || echo "?")
    assert_eq "bg-agents counter after Task completion" "0" "$bg" || failures=$((failures + 1))

    # Reads.jsonl might have entries from the subagent's reads, OR not — the
    # subagent uses its own session_id internally? Let's not assert on this
    # because the semantics aren't documented. The key assertion is the counter
    # behavior — it went up (we don't see the intermediate state) and came back to 0.

    rm -rf "$fixture"
    scenario_end 5 "Subagent counter" "$failures"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo "${BOLD}Freshness Real-World Test${RST}"
echo "Target: actual Claude Code sessions via 'claude -p'"
echo "Hooks dir: $HOME/.claude/hooks"
echo "Telemetry: $TELEMETRY"
echo "Dry-run: $DRY_RUN | Verbose: $VERBOSE | Keep state: $KEEP_STATE"
echo
echo "${YEL}NOTE${RST}: this runs real API calls. Cost budget per scenario: \$2."
echo

run_scenario_1
run_scenario_2
run_scenario_3
run_scenario_4
run_scenario_5

# Cleanup synthetic session state (unless --keep-state)
if ! $KEEP_STATE; then
    for sid in "${ALL_SESSION_IDS[@]}"; do
        cleanup_session_state "$sid"
    done
fi

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
echo
if $KEEP_STATE; then
    echo "${YEL}Synthetic session state retained for inspection. Sessions:${RST}"
    for sid in "${ALL_SESSION_IDS[@]}"; do
        echo "  $sid"
    done
else
    echo "Synthetic session state cleaned. Use --keep-state to retain for forensics."
fi

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo
    echo "${GREEN}${BOLD}All real-world scenarios passed.${RST}"
    exit 0
fi
exit 1
