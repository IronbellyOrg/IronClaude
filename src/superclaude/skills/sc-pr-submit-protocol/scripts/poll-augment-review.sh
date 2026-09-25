#!/usr/bin/env bash
#
# poll-augment-review.sh — C2 poller for sc:pr-submit.
#
# Purpose : Do a SINGLE poll of a PR for the Augment Code review and emit exactly
#           ONE JSON line (one attended-poll-loop event) to stdout, then exit 0.
# Usage   : poll-augment-review.sh --pr <N>
# Output  : one line of JSON: {"pr":N,"state":"polling|clean|findings|unknown",
#           "head_sha":"...","reviews":[...],"comments":[...]}
# Exit    : 0 always on a completed poll (fail-soft); 2 on a usage error.
# Spec    : merged-spec.md FR-2.1 (poll surface), §7 (detection contract). The FSM
#           (superclaude.pr_submit) does the backoff/timeout arithmetic + final
#           classification; this script only surfaces the raw payload + a coarse
#           state. All gh I/O is isolated here (NFR-6 core purity).
#
# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.

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
# Note: the head SHA is read from the PR JSON below (headRefOid), not a flag.

[ -n "$PR" ] || die "missing required --pr <N>" 2
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2
command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 2

# Resolve the target repo (owner/repo). The SKILL normally passes --repo; absent it,
# resolve from the current checkout (gh repo view reads the local repo identity, then
# parse the origin remote). This de-hardcodes the poll off any one fork (FR-1.3
# generalized): the --repo pin is COMPUTED, never a literal owner/repo.
REPO="${REPO:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)}"
[ -n "$REPO" ] || REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2

# Single poll of the PR. Every gh call pins the RESOLVED --repo "$REPO" (FR-1.3).
PR_JSON="$(gh pr view "$PR" --repo "$REPO" \
    --json number,url,headRefName,headRefOid,baseRefName,reviews 2>/dev/null || true)"

if [ -z "$PR_JSON" ]; then
    # Poll failed (rate limit / transient) — surface as still-polling; the FSM backs off.
    jq -nc --argjson pr "$PR" '{pr:$pr, state:"polling", comments_ok:false, reviews:[], comments:[]}'
    exit 0
fi

# Comment payloads (Augment "Fix This" URLs, paginated inline threads) routinely
# exceed ARG_MAX when passed as jq --argjson argv. Stage them in temp files and
# merge with --slurpfile (stdin/files, never argv). Fail-soft to [] on any error.
_tmp="$(mktemp -d "${TMPDIR:-/tmp}/poll-augment.XXXXXX")" || die "mktemp failed" 1
trap 'rm -rf "$_tmp"' EXIT
issue_file="$_tmp/issue.json"
inline_file="$_tmp/inline.json"
pr_file="$_tmp/pr.json"

COMMENTS_OK=true
if ! gh api "repos/${REPO}/issues/${PR}/comments" --paginate 2>/dev/null \
        | jq -s 'add // []' > "$issue_file" 2>/dev/null; then
    printf '[]\n' > "$issue_file"
    COMMENTS_OK=false
fi
if ! gh api "repos/${REPO}/pulls/${PR}/comments" --paginate 2>/dev/null \
        | jq -s 'add // []' > "$inline_file" 2>/dev/null; then
    printf '[]\n' > "$inline_file"
    COMMENTS_OK=false
fi
printf '%s' "$PR_JSON" > "$pr_file"

# Coarse state: any review present => let the FSM classify; none => polling. The
# authoritative three-state classification is done by superclaude.pr_submit.classify
# against the probe-locked DetectionContract; this is only a hint for the stream.
STATE="$(jq -r 'if ((.reviews // []) | length) > 0 then "review_present" else "polling" end' "$pr_file")"

# --slurpfile wraps each file in an array; a file that is already one JSON array
# is therefore $var[0]. Never --argjson the comment blobs (ARG_MAX on busy PRs).
jq -c --arg state "$STATE" \
    --argjson comments_ok "$COMMENTS_OK" \
    --slurpfile issue_comments "$issue_file" \
    --slurpfile inline_comments "$inline_file" \
    '{pr:.number, url:.url, head_sha:.headRefOid, base:.baseRefName,
      state:$state, comments_ok:$comments_ok, reviews:(.reviews // []),
      comments:(($issue_comments[0] // []) + ($inline_comments[0] // []))}' \
    "$pr_file"

exit 0
