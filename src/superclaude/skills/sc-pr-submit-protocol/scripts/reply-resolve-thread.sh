#!/usr/bin/env bash
#
# reply-resolve-thread.sh — C4 reply + resolve wrapper for sc:pr-submit.
#
# Purpose : Post a REST reply on an Augment finding's review-comment thread, THEN
#           resolve that thread via the GraphQL resolveReviewThread mutation.
#           Reply FIRST, then resolve (FR-6.1 → FR-6.2). A thread already resolved
#           is skipped (idempotency).
# Usage   : reply-resolve-thread.sh --pr <N> --comment-id <ID> --body-file <path>
#                                   [--thread-id <ID>] [--path <file> --line <n>] [--no-resolve]
# Exit    : 0 on success or idempotent skip; 2 on usage error; 3 on a permissions
#           HALT (resolve needs PR read+write).
# Spec    : merged-spec.md FR-6.1/FR-6.2; research/06 §2.2/§2.3. All gh I/O is
#           isolated here (NFR-6). gh api paths pin the RESOLVED repos/${REPO}/...
#           (origin's owner/repo, computed at runtime — never a literal fork).
#
# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.

set -euo pipefail

die() { printf 'reply-resolve-thread: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
REPO=""
COMMENT_ID=""
KNOWN_THREAD_ID=""
BODY_FILE=""
THREAD_PATH=""
THREAD_LINE=""
DO_RESOLVE=1
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) PR="${2:-}"; shift 2 ;;
        --repo) REPO="${2:-}"; shift 2 ;;
        --comment-id) COMMENT_ID="${2:-}"; shift 2 ;;
        --thread-id) KNOWN_THREAD_ID="${2:-}"; [ -n "$KNOWN_THREAD_ID" ] || die "missing --thread-id <ID>" 2; shift 2 ;;
        --body-file) BODY_FILE="${2:-}"; shift 2 ;;
        --path) THREAD_PATH="${2:-}"; shift 2 ;;
        --line) THREAD_LINE="${2:-}"; shift 2 ;;
        --no-resolve) DO_RESOLVE=0; shift ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done

[[ "$PR" =~ ^[1-9][0-9]*$ ]] || die "missing/invalid --pr <N>" 2
[[ "$COMMENT_ID" =~ ^[1-9][0-9]*$ ]] || die "missing/invalid --comment-id <ID>" 2
[ -n "$BODY_FILE" ] || die "missing required --body-file <path>" 2
[ -f "$BODY_FILE" ] || die "body file not found: $BODY_FILE" 2
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2
command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 2

# Resolve the target repo (owner/repo). The SKILL normally passes --repo; absent it,
# resolve from the current checkout (the origin remote, then gh repo view). Every gh
# api / graphql target below is COMPUTED from this — never a literal owner/repo.
REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
[ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2
REPO_OWNER="${REPO%%/*}"
REPO_NAME="${REPO##*/}"

# Locate and confirm the root BEFORE any write, including --no-resolve replies.
# Path/line remain accepted for compatibility, but never identify a thread.
_tmp="$(mktemp -d "${TMPDIR:-/tmp}/reply-resolve.XXXXXX")" || die "mktemp failed" 1
trap 'rm -rf "$_tmp"' EXIT
: > "$_tmp/pages.jsonl"
: > "$_tmp/cursors"
cursor=""
cursor_args=()
completed=false
# ponytail: cap at 1000 pages; fail closed rather than truncate or loop forever.
for ((page=1; page<=1000; page++)); do
    gh api graphql -f query='
      query($owner:String!,$repo:String!,$pr:Int!,$endCursor:String){
        repository(owner:$owner,name:$repo){pullRequest(number:$pr){
          reviewThreads(first:100,after:$endCursor){pageInfo{hasNextPage endCursor}
            nodes{id isResolved comments(first:1){nodes{databaseId replyTo{databaseId}}}}
          }
        }}
      }' -f owner="$REPO_OWNER" -f repo="$REPO_NAME" -F pr="$PR" \
      "${cursor_args[@]}" > "$_tmp/page.json" 2>/dev/null \
      || die "could not query review threads (needs PR read+write?)" 3
    jq -es '
      def text: type == "string" and length > 0;
      length == 1 and (.[0] | type == "object" and
        ((has("errors") | not) or .errors == []) and
        (.data.repository.pullRequest.reviewThreads | type == "object" and
          (.pageInfo | type == "object" and (.hasNextPage | type == "boolean") and
            has("endCursor") and (.endCursor == null or (.endCursor | text))) and
          (.nodes | type == "array" and length <= 100 and all(.[];
            type == "object" and (.id | text) and (.isResolved | type == "boolean") and
            (.comments.nodes | type == "array" and length == 1 and all(.[];
              type == "object" and (.databaseId | type == "number" and . > 0 and floor == .) and
              has("replyTo") and .replyTo == null))
          ))
        ))' "$_tmp/page.json" >/dev/null 2>&1 || die "incomplete/malformed review threads" 3
    next="$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor // ""' "$_tmp/page.json")"
    more="$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage' "$_tmp/page.json")"
    if jq -e '.data.repository.pullRequest.reviewThreads.nodes | length > 0' "$_tmp/page.json" >/dev/null; then
        [ -n "$next" ] || die "missing review-thread cursor" 3
        grep -Fxq -- "$next" "$_tmp/cursors" && die "nonadvancing review-thread cursor" 3
        printf '%s\n' "$next" >> "$_tmp/cursors"
    else
        [ "$more" = false ] && [ -z "$cursor" ] && [ -z "$next" ] || die "incomplete review-thread pagination" 3
    fi
    jq -c '.data.repository.pullRequest.reviewThreads.nodes' "$_tmp/page.json" >> "$_tmp/pages.jsonl"
    if [ "$more" = false ]; then completed=true; break; fi
    cursor="$next"
    cursor_args=(-f endCursor="$cursor")
done
[ "$completed" = true ] || die "review-thread page limit reached" 3
jq -es 'add | if length == (unique_by(.id) | length) and
    length == (unique_by(.comments.nodes[0].databaseId) | length)
    then . else error("ambiguous thread/root IDs") end' "$_tmp/pages.jsonl" > "$_tmp/threads.json" \
    || die "ambiguous review-thread identity" 3
# Prefer a supplied thread ID, but still verify its PR membership and root ID.
jq -c --arg cid "$COMMENT_ID" --arg tid "$KNOWN_THREAD_ID" 'map(select(
    if $tid != "" then .id == $tid else (.comments.nodes[0].databaseId | tostring) == $cid end))' \
    "$_tmp/threads.json" > "$_tmp/matches.json"
[ "$(jq 'length' "$_tmp/matches.json")" = 1 ] || die "no unique review thread for comment ${COMMENT_ID}" 1
jq -e --arg cid "$COMMENT_ID" '(.[0].comments.nodes[0].databaseId | tostring) == $cid' \
    "$_tmp/matches.json" >/dev/null || die "thread ID conflicts with comment ${COMMENT_ID}" 1
THREAD_ID="$(jq -r '.[0].id' "$_tmp/matches.json")"
if [ "$(jq -r '.[0].isResolved' "$_tmp/matches.json")" = true ]; then
    printf 'thread %s already resolved (idempotency_skip)\n' "$THREAD_ID"
    exit 0
fi

# Reply FIRST, then resolve. Stage body/response so large replies never enter argv.
jq -n --rawfile body "$BODY_FILE" '{body:$body}' > "$_tmp/reply.json"
gh api --method POST "repos/${REPO}/pulls/${PR}/comments/${COMMENT_ID}/replies" \
    --input "$_tmp/reply.json" > "$_tmp/reply-response.json" \
    || die "reply POST failed for comment ${COMMENT_ID}" 1
jq -es --arg cid "$COMMENT_ID" 'length == 1 and (.[0] | type == "object" and
    (.id | type == "number" and . > 0 and floor == .) and (.in_reply_to_id | tostring) == $cid)' \
    "$_tmp/reply-response.json" >/dev/null 2>&1 || die "reply POST returned an invalid response" 1
if [ "$DO_RESOLVE" -eq 0 ]; then
    printf 'replied to %s (resolve skipped)\n' "$COMMENT_ID"
    exit 0
fi
gh api graphql -f query='
  mutation($threadId:ID!){ resolveReviewThread(input:{threadId:$threadId}){ thread{ id isResolved } } }' \
    -f threadId="$THREAD_ID" > "$_tmp/resolve-response.json" \
    || die "resolveReviewThread failed (needs PR read+write?)" 3
jq -es --arg tid "$THREAD_ID" 'length == 1 and (.[0] | type == "object" and
    ((has("errors") | not) or .errors == []) and
    (.data.resolveReviewThread.thread | type == "object" and .id == $tid and .isResolved == true))' \
    "$_tmp/resolve-response.json" >/dev/null 2>&1 || die "resolveReviewThread returned an invalid response" 3
printf 'replied to %s and resolved thread %s\n' "$COMMENT_ID" "$THREAD_ID"
exit 0
