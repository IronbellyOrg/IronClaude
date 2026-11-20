#!/bin/bash
# Adapted from scripts/branch-landed.sh in
# https://github.com/Simple-With-Us/AI-Fleet-Coordinator (commit b7f695084c, 2026-09-17),
# Copyright 2026 Jay Wedgeworth, licensed under the Apache License, Version 2.0.
# Changed by IronClaude: the input is a pull request number, the output is one line, jq
# replaces the embedded Python script, and a held-versus-merged check is added. See PROVENANCE.md.
#
# Squash-safe "did this pull request already land?"
#
# A squash merge with a deleted branch rewrites the commits, so a correctly landed
# pull request has its commits absent from the base branch and no remote branch left
# behind. Any check that asks whether the branch head is an ancestor of the base
# branch therefore calls every landed pull request abandoned. This script never asks
# that question: the verdict comes from the pull request state alone.
#
# Usage   : branch-landed.sh <PR>
#           <PR> is a number, #<number> or https://github.com/<owner>/<repo>/pull/<number>.
#           The repository is always the origin remote of the current directory.
# Output  : exactly one stdout line, a token then key=value fields separated by one
#           space (no value holds a space); details go to stderr only.
#   MERGED  pr=<N> by=<login|unknown> merge=<40 hex|unknown> base=<branch> head=<40 hex|unknown>
#           match=<same|differs|unchecked> url=<url>     exit 0
#   OPEN    pr=<N> url=<url>                                  exit 1
#   UNKNOWN reason=<usage|no_origin|foreign_repo|no_jq|gh_failed|bad_json>   exit 2
#   NONE    pr=<N>                                            exit 3
#   CLOSED  pr=<N> url=<url>   (closed without a merge)       exit 4
# Exit 0 only for MERGED.
#
# For MERGED only, match= compares the files the pull request held with the files the
# merge changed, by file name, with a three-dot diff and one diff-tree per merge
# commit. A two-dot diff of a branch tip against the base on a stale branch is
# actively misleading, so none is used. The only write is git fetch of the base
# branch and refs/pull/<N>/head, which touches objects and FETCH_HEAD only.
# Contract: no stdin read, no prompt.

set -u -o pipefail

ERRFILE=""
cleanup() {
    [ -n "$ERRFILE" ] && rm -f -- "$ERRFILE"
}
trap cleanup EXIT

# unknown <reason> <detail>: the one UNKNOWN line, details on stderr.
unknown() {
    printf 'branch-landed: %s\n' "$2" >&2
    printf 'UNKNOWN reason=%s\n' "$1"
    exit 2
}

# Step 0: arguments. Only the number is used.
if [ $# -ne 1 ] || [ -z "$1" ]; then
    unknown usage "usage: branch-landed.sh <PR> (a number, #<number> or a pull request URL)"
fi
ARG="$1"
URL_REPO=""
url_re='^https://github\.com/([^/]+)/([^/]+)/pull/([0-9]+)([/?#].*)?$'
case "$ARG" in
    https://*)
        if [[ "$ARG" =~ $url_re ]]; then
            URL_REPO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
            num="${BASH_REMATCH[3]}"
        else
            unknown usage "not a pull request URL: $ARG"
        fi
        ;;
    \#*) num="${ARG#\#}" ;;
    *) num="$ARG" ;;
esac
case "$num" in
    '' | *[!0-9]*) unknown usage "not a pull request number: $ARG" ;;
esac
num=$((10#$num))
[ "$num" -gt 0 ] || unknown usage "not a pull request number: $ARG"
PR="$num"

command -v jq >/dev/null 2>&1 || unknown no_jq "jq is required"

# Parse origin into owner/repo (Jay's parse, kept).
url=$(git remote get-url origin 2>/dev/null </dev/null || true)
url=${url%.git}
url=${url#git@github.com:}
url=${url#https://github.com/}
url=${url#ssh://git@github.com/}
repo_re='^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$'
if [[ "$url" =~ $repo_re ]]; then
    GH_REPO="$url"
else
    unknown no_origin "cannot parse the origin remote as a GitHub owner/repo"
fi

if [ -n "$URL_REPO" ]; then
    lower_url=$(printf '%s' "$URL_REPO" | tr '[:upper:]' '[:lower:]')
    lower_origin=$(printf '%s' "$GH_REPO" | tr '[:upper:]' '[:lower:]')
    [ "$lower_url" = "$lower_origin" ] || unknown foreign_repo "the URL names $URL_REPO, origin is $GH_REPO"
fi

# Step 1: the one state read. The verdict comes from this and nothing else.
ERRFILE=$(mktemp) || unknown gh_failed "cannot make a temporary file"
json=$(gh pr view "$PR" --repo "$GH_REPO" \
    --json number,state,mergedAt,mergedBy,mergeCommit,baseRefName,headRefOid,commits,url \
    </dev/null 2>"$ERRFILE")
rc=$?
if [ "$rc" -ne 0 ]; then
    if grep -q 'Could not resolve to a PullRequest with the number of' "$ERRFILE"; then
        printf 'branch-landed: no pull request %s in %s\n' "$PR" "$GH_REPO" >&2
        printf 'NONE pr=%s\n' "$PR"
        exit 3
    fi
    cat -- "$ERRFILE" >&2
    unknown gh_failed "gh pr view failed (exit $rc)"
fi
jq -e 'type == "object"' >/dev/null 2>&1 <<<"$json" || unknown bad_json "gh did not answer with a JSON object"

jf() { jq -r "$1" <<<"$json" 2>/dev/null; }
state=$(jf '.state // ""')
pr_url=$(jf '.url // ""')
[ -n "$pr_url" ] || pr_url="unknown"

case "$state" in
    OPEN)
        printf 'OPEN pr=%s url=%s\n' "$PR" "$pr_url"
        exit 1
        ;;
    CLOSED)
        printf 'CLOSED pr=%s url=%s\n' "$PR" "$pr_url"
        exit 4
        ;;
    MERGED) ;;
    *) unknown bad_json "unexpected pull request state: $state" ;;
esac

# Step 2: MERGED only. Fields of the state read.
merged_by=$(jf '.mergedBy.login // ""')
[ -n "$merged_by" ] || merged_by="unknown"
merge=$(jf '.mergeCommit.oid // ""')
base=$(jf '.baseRefName // ""')
head=$(jf '.headRefOid // ""')
ncommits=$(jf '(.commits // []) | length')
case "$ncommits" in '' | *[!0-9]*) ncommits=0 ;; esac

is_sha() {
    case "$1" in
        *[!0-9a-f]*) return 1 ;;
    esac
    [ "${#1}" -eq 40 ]
}

# files_held <K>: the three-dot diff against the base as it was just before the merge.
files_held() {
    git diff --no-renames --name-only "${merge}~$1...${head}" </dev/null 2>/dev/null
}

# files_merged <K>: what the merge changed, one commit at a time, each anchored on
# the merge commit; the union of the K newest commits against their first parents.
files_merged() {
    local i=0
    while [ "$i" -lt "$1" ]; do
        git diff-tree -r --no-renames --name-only "${merge}~${i}^1" "${merge}~${i}" </dev/null 2>/dev/null || return 1
        i=$((i + 1))
    done
}

# same_sets <K>: 0 when equal, 1 when different, 2 when a step failed.
same_sets() {
    local held merged
    held=$(files_held "$1") || return 2
    merged=$(files_merged "$1") || return 2
    held=$(printf '%s\n' "$held" | sort -u)
    merged=$(printf '%s\n' "$merged" | sort -u)
    [ "$held" = "$merged" ]
}

match="unchecked"
fetch_ok=0
if is_sha "$merge" && is_sha "$head" && [ -n "$base" ]; then
    case "$base" in
        -* | *[!A-Za-z0-9._/-]*) ;;
        *) fetch_ok=1 ;;
    esac
fi
if [ "$fetch_ok" -eq 1 ] && git fetch --quiet origin "$base" "refs/pull/$PR/head" </dev/null >/dev/null 2>&1; then
    same_sets 1
    rc=$?
    if [ "$rc" -eq 0 ]; then
        match="same"
    elif [ "$rc" -eq 1 ]; then
        match="differs"
        # A rebase merge leaves one commit per pull request commit: try that many.
        if [ "$ncommits" -gt 1 ]; then
            same_sets "$ncommits"
            rc=$?
            if [ "$rc" -eq 0 ]; then
                match="same"
            elif [ "$rc" -eq 2 ]; then
                match="unchecked"
            fi
        fi
    fi
fi

[ -n "$merge" ] || merge="unknown"
[ -n "$base" ] || base="unknown"
[ -n "$head" ] || head="unknown"
printf 'MERGED pr=%s by=%s merge=%s base=%s head=%s match=%s url=%s\n' \
    "$PR" "$merged_by" "$merge" "$base" "$head" "$match" "$pr_url"
exit 0
