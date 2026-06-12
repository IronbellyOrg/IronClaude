#!/usr/bin/env bash
# PostToolUse(Bash) — after a successful `gh pr create`, surface an offer to run /sc:auggie-review.
#
# Hook contract:
#   - stdin:  JSON with { tool_name, tool_input, tool_response }
#   - exit 0: pass-through; if stdout is non-empty Claude Code surfaces it as additional context
#   - exit 2: blocks the tool (we do NOT want that here — the PR is already created)
#
# Behavior:
#   - Match only Bash invocations that look like `gh pr create ...`
#   - Match only on success (tool_response.error is empty)
#   - Extract the new PR number/URL from the tool's stdout if possible
#   - Print a single-line offer message; Claude relays it to the user

set -u

INPUT="$(cat 2>/dev/null || true)"

# Cheap prefilter: bail out immediately if the payload doesn't even mention `gh pr create`.
# Saves three jq invocations on every non-matching Bash tool call.
case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*) ;; *) exit 0;; esac

# Pull the tool name and the bash command out of the hook payload.
TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
[ "$TOOL_NAME" = "Bash" ] || exit 0

CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)"
[ -z "$CMD" ] && exit 0

# Only fire on `gh pr create` (allow flags between `gh` and `pr create`).
# This matches: "gh pr create ...", "gh -R foo/bar pr create ...", etc.
# It does NOT match `gh pr view`, `gh pr list`, or arbitrary commands containing the substring "pr create".
if ! [[ "$CMD" =~ (^|[[:space:]\;\&\|])gh([[:space:]]+-[^[:space:]]+)*[[:space:]]+pr[[:space:]]+create([[:space:]]|$) ]]; then
    exit 0
fi

# Skip if the command failed (PR not actually created).
TOOL_ERROR="$(printf '%s' "$INPUT" | jq -r '.tool_response.error // empty' 2>/dev/null)"
[ -n "$TOOL_ERROR" ] && exit 0

# Try to extract the PR URL or number from the tool's stdout. `gh pr create` prints the new PR URL
# as its final line on success.
TOOL_STDOUT="$(printf '%s' "$INPUT" | jq -r '.tool_response.stdout // .tool_response.output // empty' 2>/dev/null)"
PR_URL="$(printf '%s' "$TOOL_STDOUT" | grep -oE 'https://github\.com/[^[:space:]]+/pull/[0-9]+' | tail -1)"
PR_NUM="$(printf '%s' "$PR_URL" | grep -oE '[0-9]+$')"

# Compose the offer. This goes to stdout; Claude Code injects it as additional context for the
# next assistant turn, and the assistant relays it to the user as a question.
if [ -n "$PR_URL" ]; then
    TARGET_HINT="$PR_URL"
    INVOKE_HINT="/sc:auggie-review $PR_NUM"
elif [ -n "$PR_NUM" ]; then
    TARGET_HINT="PR #$PR_NUM"
    INVOKE_HINT="/sc:auggie-review $PR_NUM"
else
    TARGET_HINT="the PR you just created"
    INVOKE_HINT="/sc:auggie-review <PR-number>"
fi

cat <<EOF
<sc-auggie-review-offer source="post-pr-create-hook">
A PR was just created ($TARGET_HINT). Offer the user the option to run a PR-review pass on it before continuing other work — either a one-shot Auggie review, or the auto-remediation monitor.

Suggested invocations:
  - $INVOKE_HINT
  - /sc:pr-submit --monitor 1 (arm an in-session monitor that polls for the Augment review, re-grades + verifies findings, and proposes fixes; higher ordinals fix/push/reply/resolve)

Ask the user with this exact framing (do not paraphrase the trigger condition):

  "I noticed you just opened $TARGET_HINT. Want me to run a code review on it now? Options: a one-shot Auggie review (/sc:auggie-review), or arm the PR-review auto-remediation monitor (/sc:pr-submit --monitor 1, which polls for the Augment review and proposes fixes — raise the ordinal for more autonomy)."

Wait for the user's response. Do not auto-invoke /sc:auggie-review OR /sc:pr-submit, and never arm a monitor, without explicit confirmation; never imply level-3 autonomy without an explicit --monitor 3. If the user declines, do not bring it up again in this session.
</sc-auggie-review-offer>
EOF

exit 0
