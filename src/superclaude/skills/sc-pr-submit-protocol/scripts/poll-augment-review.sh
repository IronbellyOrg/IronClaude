#!/usr/bin/env bash
# Single repo-pinned poll; raw payloads stay in files (large reviews exceed ARG_MAX).
# Classification/backoff belong to superclaude.pr_submit, not this adapter.
set -euo pipefail

die() { printf 'poll-augment-review: %s\n' "$1" >&2; exit "${2:-1}"; }
PR=""
REPO=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) PR="${2:-}"; shift 2 ;;
        --repo) REPO="${2:-}"; shift 2 ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done
[[ "$PR" =~ ^[1-9][0-9]*$ ]] || die "missing/invalid --pr <N>" 2
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2
command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 2
REPO="${REPO:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)}"
[ -n "$REPO" ] || REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2

failed_poll() {
    jq -nc --argjson pr "$PR" '{pr:$pr, head_sha:null, state:"polling",
        reviews_ok:false, comments_ok:false, threads_ok:false, reviews:[], comments:[], threads:[]}'
    exit 0
}
_tmp="$(mktemp -d "${TMPDIR:-/tmp}/poll-augment.XXXXXX")" || failed_poll
trap 'rm -rf "$_tmp"' EXIT
pr_file="$_tmp/pr.json"
issue_file="$_tmp/issue.json"
inline_file="$_tmp/inline.json"
reviews_file="$_tmp/reviews.json"
threads_file="$_tmp/threads.json"
if ! gh pr view "$PR" --repo "$REPO" \
        --json number,url,headRefName,headRefOid,baseRefName > "$pr_file" 2>/dev/null \
    || ! jq -es --argjson pr "$PR" 'length == 1 and (.[0] |
        type == "object" and .number == $pr and (.headRefOid | type == "string" and test("^[a-fA-F0-9]{40}$")))' \
        "$pr_file" >/dev/null 2>&1; then
    failed_poll
fi
HEAD_SHA="$(jq -r '.headRefOid' "$pr_file")"

# Explicit page numbers avoid an unbounded gh --paginate on a broken API cursor.
# ponytail: 1000 pages per source; fail incomplete at the cap, never silently truncate.
fetch_rest() {
    local kind="$1" output="$2" page count completed=false
    : > "$_tmp/rest-pages.jsonl"
    for ((page=1; page<=1000; page++)); do
        case "$kind" in
            issue) gh api "repos/${REPO}/issues/${PR}/comments" --method GET -F per_page=100 -F page="$page" ;;
            inline) gh api "repos/${REPO}/pulls/${PR}/comments" --method GET -F per_page=100 -F page="$page" ;;
            reviews) gh api "repos/${REPO}/pulls/${PR}/reviews" --method GET -F per_page=100 -F page="$page" ;;
        esac > "$_tmp/rest-page.json" 2>/dev/null || return 1
        jq -es --arg kind "$kind" 'length == 1 and (.[0] | type == "array" and length <= 100 and
            all(.[]; type == "object" and (.id | type == "number" and . > 0 and floor == .) and
                has("body") and (.body == null or (.body | type == "string")) and
                has("user") and (.user == null or (.user.login | type == "string")) and
                (if $kind == "reviews" then
                    (.state | type == "string") and has("commit_id") and
                    (.commit_id == null or (.commit_id | type == "string")) and
                    (.state == "PENDING" or has("submitted_at")) and
                    (.submitted_at == null or (.submitted_at | type == "string"))
                 else (.body | type == "string") end)))' \
            "$_tmp/rest-page.json" >/dev/null 2>&1 || return 1
        jq -c '.' "$_tmp/rest-page.json" >> "$_tmp/rest-pages.jsonl" || return 1
        count="$(jq 'length' "$_tmp/rest-page.json")"
        if [ "$count" -lt 100 ]; then completed=true; break; fi
        # Reject repeated IDs before fetching again (including a server ignoring page).
        jq -es 'add | length == (unique_by(.id) | length)' "$_tmp/rest-pages.jsonl" >/dev/null || return 1
    done
    [ "$completed" = true ] || return 1
    jq -es 'add | if length == (unique_by(.id) | length) then . else error("duplicate IDs") end' \
        "$_tmp/rest-pages.jsonl" > "$output" 2>/dev/null
}
COMMENTS_OK=true
REVIEWS_OK=true
THREADS_OK=true
fetch_rest issue "$issue_file" || { printf '[]\n' > "$issue_file"; COMMENTS_OK=false; }
fetch_rest inline "$inline_file" || { printf '[]\n' > "$inline_file"; COMMENTS_OK=false; }
fetch_rest reviews "$reviews_file" || { printf '[]\n' > "$reviews_file"; REVIEWS_OK=false; }

fetch_threads() {
    local page cursor="" next more completed=false
    local -a cursor_args=()
    : > "$_tmp/thread-pages.jsonl"
    : > "$_tmp/cursors"
    for ((page=1; page<=1000; page++)); do
        gh api graphql -f query='
          query($owner:String!,$repo:String!,$pr:Int!,$endCursor:String){
            repository(owner:$owner,name:$repo){pullRequest(number:$pr){headRefOid
              reviewThreads(first:100,after:$endCursor){pageInfo{hasNextPage endCursor}
                nodes{id path line originalLine isResolved isOutdated
                  comments(first:1){nodes{id databaseId body path line originalLine createdAt
                    author{login} replyTo{databaseId} pullRequestReview{id databaseId commit{oid}}}}
                }
              }
            }}
          }' -f owner="${REPO%%/*}" -f repo="${REPO##*/}" -F pr="$PR" \
          "${cursor_args[@]}" > "$_tmp/thread-page.json" 2>/dev/null || return 1
        jq -es --arg head "$HEAD_SHA" '
          def text: type == "string" and length > 0;
          def location: . == null or (type == "number" and . > 0 and floor == .);
          length == 1 and (.[0] | type == "object" and
            ((has("errors") | not) or .errors == []) and
            (.data.repository.pullRequest | type == "object" and .headRefOid == $head and
              (.reviewThreads | type == "object" and
                (.pageInfo | type == "object" and (.hasNextPage | type == "boolean") and
                  (has("endCursor")) and (.endCursor == null or (.endCursor | text))) and
                (.nodes | type == "array" and length <= 100 and all(.[];
                  type == "object" and (.id | text) and (.path | type == "string") and
                  has("line") and (.line | location) and has("originalLine") and (.originalLine | location) and
                  (.isResolved | type == "boolean") and (.isOutdated | type == "boolean") and
                  (.comments.nodes | type == "array" and length == 1 and all(.[];
                    type == "object" and (.id | text) and
                    (.databaseId | type == "number" and . > 0 and floor == .) and
                    (.body | type == "string") and (.createdAt | text) and
                    has("line") and (.line | location) and has("originalLine") and (.originalLine | location) and
                    has("replyTo") and .replyTo == null and
                    has("author") and (.author == null or (.author.login | text)) and
                    has("pullRequestReview") and (.pullRequestReview == null or
                      (.pullRequestReview | (.id | text) and
                        (.databaseId | type == "number" and . > 0 and floor == .) and (.commit.oid | text)))
                  ))
                ))
              )
            ))' "$_tmp/thread-page.json" >/dev/null 2>&1 || return 1
        next="$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor // ""' "$_tmp/thread-page.json")"
        more="$(jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage' "$_tmp/thread-page.json")"
        if jq -e '.data.repository.pullRequest.reviewThreads.nodes | length > 0' "$_tmp/thread-page.json" >/dev/null; then
            [ -n "$next" ] || return 1
            grep -Fxq -- "$next" "$_tmp/cursors" && return 1
            printf '%s\n' "$next" >> "$_tmp/cursors"
        else
            [ "$more" = false ] && [ -z "$cursor" ] && [ -z "$next" ] || return 1
        fi
        jq -c '.data.repository.pullRequest.reviewThreads.nodes' "$_tmp/thread-page.json" >> "$_tmp/thread-pages.jsonl" || return 1
        if [ "$more" = false ]; then completed=true; break; fi
        cursor="$next"
        cursor_args=(-f endCursor="$cursor")
    done
    [ "$completed" = true ] || return 1
    jq -es 'add | if length == (unique_by(.id) | length) and
        length == (unique_by(.comments.nodes[0].databaseId) | length)
        then . else error("duplicate thread/root IDs") end' "$_tmp/thread-pages.jsonl" > "$threads_file" 2>/dev/null
}
fetch_threads || { printf '[]\n' > "$threads_file"; THREADS_OK=false; }

# A push during any of these requests invalidates the entire assembled snapshot.
if ! gh pr view "$PR" --repo "$REPO" --json headRefOid > "$_tmp/head.json" 2>/dev/null \
    || ! jq -es --arg head "$HEAD_SHA" 'length == 1 and (.[0].headRefOid == $head)' "$_tmp/head.json" >/dev/null 2>&1; then
    COMMENTS_OK=false
    REVIEWS_OK=false
    THREADS_OK=false
fi
jq -c --argjson comments_ok "$COMMENTS_OK" --argjson reviews_ok "$REVIEWS_OK" --argjson threads_ok "$THREADS_OK" \
    --arg observed_at "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --slurpfile issue_comments "$issue_file" --slurpfile inline_comments "$inline_file" \
    --slurpfile reviews "$reviews_file" --slurpfile threads "$threads_file" \
    '{pr:.number, url:.url, head_sha:.headRefOid, base:.baseRefName, observed_at:$observed_at,
      state:(if $comments_ok and $reviews_ok and $threads_ok and ($reviews[0] | length) > 0
             then "review_present" else "polling" end),
      comments_ok:$comments_ok, reviews_ok:$reviews_ok, threads_ok:$threads_ok,
      reviews:$reviews[0], threads:$threads[0],
      comments:(($issue_comments[0] // []) + ($inline_comments[0] // []))}' "$pr_file"
