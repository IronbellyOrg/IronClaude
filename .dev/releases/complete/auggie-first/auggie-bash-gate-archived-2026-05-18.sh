# ARCHIVED — DO NOT EXECUTE
#
# This is a verbatim archive of `.claude/hooks/auggie-bash-gate.sh` as it
# existed on 2026-05-18 immediately before deletion. The script is the lone
# surviving artifact of the `auggie-first-required` release effort that was
# intentionally abandoned by the maintainer (RyanW) per a 2026-05-18 decision:
# "we went through a lot of back and forth and then I decided on a simpler
# solution for now where we just rely on memory before doing a bunch of work
# and overcomplicating things."
#
# Historical context:
# - The script was authored 2026-05-17 ~17:30 UTC during a heavy task-builder
#   pipeline session. It is the planned PreToolUse Bash gate that would have
#   blocked actionable verbs when the auggie-first sticky is present.
# - Three dangling commits by RyanW (9d31e4c, a759ce7, 9920456) attempted to
#   register it in `install_hooks.py:_FRESHNESS_SCRIPTS` and
#   `src/superclaude/hooks/hooks.json` PreToolUse Bash matcher. All three
#   were orphaned via branch reset during "task-merge consolidation" work.
# - The accompanying spec (`auggie-bash-gate-spec.md`) and pytest source
#   (`tests/hooks/test_auggie_bash_gate.py`) were also deleted with the rest
#   of the `.dev/releases/current/auggie-first-required/` release directory.
#   Only the orphaned bytecode in `tests/hooks/__pycache__/` remained until
#   2026-05-18 cleanup.
# - The orphan was first surfaced by the new `=== Hooks ===` reverse-check
#   in `make verify-sync` introduced by the `hook-sync-and-matcher-fix`
#   release (PR #49, merged 2026-05-18 11:43 UTC) as Open Question OQ-2.
# - Per the release-spec §6 disposition options, OQ-2 was resolved by
#   ARCHIVE-then-DELETE: this file preserves the body; the orphan was rm'd.
#
# Recovery instructions (if a Bash gate is ever wanted in a future release):
# - Strip the leading archive-header block (everything above the `#!/usr/bin/env bash` line).
# - Move to `src/superclaude/hooks/scripts/auggie-bash-gate.sh`.
# - Write a v2.2 (or later) `auggie-first-hook-proposal-vX.md` documenting
#   the PreToolUse Bash gate as a first-class part of the design.
# - Write tests at `tests/hooks/test_auggie_bash_gate.py` (the .pyc strings
#   reveal the original test names: T1-T5 plus R-1 through R-5 acceptance).
# - Register in `src/superclaude/hooks/hooks.json` PreToolUse with
#   `matcher: "Bash"` and `timeout: 1`.
# - Add to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py`.
# - Run `make sync-dev` and `make verify-sync` to confirm.
#
# Provenance fingerprint (for future archaeology):
# - file birth: 2026-05-17 17:30:54 UTC
# - last on-disk modify: 2026-05-17 17:58:40 UTC
# - size on archive: 2593 bytes
# - permission: 0755
# - parent release: .dev/releases/current/auggie-first-required/ (wiped)
# - referenced spec (never on master): .dev/releases/current/auggie-first-required/auggie-bash-gate-spec.md
#
# ===== verbatim archived script body follows =====

#!/usr/bin/env bash
# PreToolUse on Bash: block a small set of actionable verbs when the
# auggie-first sticky is present and no env-var disable is set.
#
# Reads JSON tool-call payload on stdin. Exits 0 (allow) or 2 (block + stderr).
# Fail-open on any parse error per the v2.1 NFR-3 convention.
#
# See auggie-bash-gate-spec.md.
set -u

# --- Escape hatch (one-shot or session-wide) ---
if [ "${IRONCLAUDE_AUGGIE_FIRST_DISABLE:-0}" = "1" ] || \
   [ "${AUGGIE_FIRST_DISABLE:-0}" = "1" ]; then
    exit 0
fi

# --- Parse stdin (fail-open on any jq failure) ---
INPUT="$(cat 2>/dev/null || true)"
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
TOOL_NAME=$(printf '%s' "$INPUT"  | jq -r '.tool_name // empty'    2>/dev/null || true)
COMMAND=$(printf '%s' "$INPUT"    | jq -r '.tool_input.command // empty' 2>/dev/null || true)

# --- Sentinel guards (mirror v2.1) ---
[ "$SESSION_ID" = "unknown" ] && exit 0
[ -z "$SESSION_ID" ]          && exit 0
[ "$TOOL_NAME"   != "Bash" ]  && exit 0   # defense-in-depth; matcher already filters
[ -z "$COMMAND" ]             && exit 0

# --- Sticky presence check (v2.1 path, read-only) ---
STICKY="$HOME/.claude/state/auggie-first-pending/$SESSION_ID.txt"
[ -f "$STICKY" ] || exit 0

# --- Actionable verb match (inline regex) ---
RE='^[[:space:]]*(superclaude|uv[[:space:]]+(run|pip)|npm|pnpm|yarn|make|pytest|kubectl|docker|terraform|gh[[:space:]]+(pr|issue|api|repo)|git[[:space:]]+(push|reset|rebase|cherry-pick|filter-branch|clean))([[:space:]]|$)'

if ! printf '%s\n' "$COMMAND" | grep -qE "$RE" 2>/dev/null; then
    exit 0
fi

# --- BLOCK ---
MATCHED_VERB=$(printf '%s\n' "$COMMAND" | grep -oE "$RE" | head -1 | awk '{print $1}')
NOW=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
LOG="$HOME/.claude/logs/auggie-first.jsonl"
mkdir -p "$(dirname "$LOG")" 2>/dev/null || true
printf '{"ts":"%s","session_id":"%s","event":"gate_blocked","tool":"Bash","matched_verb":"%s"}\n' \
    "$NOW" "$SESSION_ID" "$MATCHED_VERB" >> "$LOG" 2>/dev/null || true

cat >&2 <<EOF
auggie-first sticky is set for this session and the command starts with an
actionable verb ('$MATCHED_VERB'). Call mcp__auggie-mcp__ask_question (or
mcp__auggie__codebase-retrieval) against the relevant subsystem BEFORE
running this command, so flag names / file paths / behavior are verified
rather than recalled.

To bypass for a single command (e.g. after consulting auggie out-of-band):
  IRONCLAUDE_AUGGIE_FIRST_DISABLE=1 <your command>

To bypass for the session, export the var in the launching shell.
EOF

exit 2
