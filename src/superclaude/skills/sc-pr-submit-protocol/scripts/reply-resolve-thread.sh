#!/usr/bin/env bash
#
# reply-resolve-thread.sh — C4 reply + resolve wrapper for sc:pr-submit.
#
# Purpose : Post a REST reply on an Augment finding's review-comment thread, THEN
#           resolve that thread via the GraphQL resolveReviewThread mutation.
#           Reply FIRST, then resolve (FR-6.1 → FR-6.2). A thread already resolved
#           is skipped (idempotency).
# Usage   : reply-resolve-thread.sh --pr <N> --comment-id <ID> --body-file <path>
#                                   [--path <file> --line <n>] [--no-resolve]
# Exit    : 0 on success or idempotent skip; 2 on usage error; 3 on a permissions
#           HALT (resolve needs PR read+write).
# Spec    : merged-spec.md FR-6.1/FR-6.2; research/06 §2.2/§2.3. All gh I/O is
#           isolated here (NFR-6). gh api paths pin repos/IronbellyOrg/IronClaude/...
#
# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.

set -euo pipefail

die() { printf 'reply-resolve-thread: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
COMMENT_ID=""
BODY_FILE=""
THREAD_PATH=""
THREAD_LINE=""
DO_RESOLVE=1
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) PR="${2:-}"; shift 2 ;;
        --comment-id) COMMENT_ID="${2:-}"; shift 2 ;;
        --body-file) BODY_FILE="${2:-}"; shift 2 ;;
        --path) THREAD_PATH="${2:-}"; shift 2 ;;
        --line) THREAD_LINE="${2:-}"; shift 2 ;;
        --no-resolve) DO_RESOLVE=0; shift ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done

[ -n "$PR" ] || die "missing required --pr <N>" 2
[ -n "$COMMENT_ID" ] || die "missing required --comment-id <ID>" 2
[ -n "$BODY_FILE" ] || die "missing required --body-file <path>" 2
[ -f "$BODY_FILE" ] || die "body file not found: $BODY_FILE" 2
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2
command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 2

# --- Step 1: reply FIRST (REST in_reply_to). The comment_id is a top-level review comment. ---
gh api --method POST \
    "repos/IronbellyOrg/IronClaude/pulls/${PR}/comments/${COMMENT_ID}/replies" \
    -f body="$(cat "$BODY_FILE")" >/dev/null \
    || die "reply POST failed for comment ${COMMENT_ID}" 1

if [ "$DO_RESOLVE" -eq 0 ]; then
    printf 'replied to %s (resolve skipped)\n' "$COMMENT_ID"
    exit 0
fi

# --- Step 2: obtain the GraphQL thread node id (REST ids != GraphQL thread ids). ---
THREADS_JSON="$(gh api graphql -f query='
  query($owner:String!,$repo:String!,$pr:Int!){
    repository(owner:$owner,name:$repo){
      pullRequest(number:$pr){
        reviewThreads(first:100){
          nodes{ id isResolved path line comments(first:1){ nodes{ databaseId } } }
        }
      }
    }
  }' -f owner=IronbellyOrg -f repo=IronClaude -F pr="$PR" 2>/dev/null || true)"

[ -n "$THREADS_JSON" ] || die "could not query review threads (needs PR read+write?)" 3

# Match the thread by the comment databaseId, or fall back to path+line.
THREAD_ID="$(printf '%s' "$THREADS_JSON" | jq -r \
    --argjson cid "$COMMENT_ID" \
    --arg path "$THREAD_PATH" \
    --argjson line "${THREAD_LINE:-0}" '
    .data.repository.pullRequest.reviewThreads.nodes
    | map(select(
        (.comments.nodes[0].databaseId == $cid)
        or ($path != "" and .path == $path and .line == $line)))
    | .[0] // {} | .id // ""')"

[ -n "$THREAD_ID" ] || die "no matching review thread for comment ${COMMENT_ID}" 1

# Idempotency: skip if already resolved.
ALREADY="$(printf '%s' "$THREADS_JSON" | jq -r \
    --arg tid "$THREAD_ID" '
    .data.repository.pullRequest.reviewThreads.nodes
    | map(select(.id == $tid)) | .[0].isResolved // false')"
if [ "$ALREADY" = "true" ]; then
    printf 'thread %s already resolved (idempotency_skip)\n' "$THREAD_ID"
    exit 0
fi

# --- Step 3: resolve the thread. ---
gh api graphql -f query='
  mutation($threadId:ID!){ resolveReviewThread(input:{threadId:$threadId}){ thread{ id isResolved } } }' \
    -f threadId="$THREAD_ID" >/dev/null \
    || die "resolveReviewThread failed (needs PR read+write?)" 3

printf 'replied to %s and resolved thread %s\n' "$COMMENT_ID" "$THREAD_ID"
exit 0
