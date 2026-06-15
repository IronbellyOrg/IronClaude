#!/usr/bin/env bash
#
# poll-augment-review.sh — C2 poller for sc:pr-submit.
#
# Purpose : Do a SINGLE poll of a PR for the Augment Code review and emit exactly
#           ONE JSON line (the Monitor-stream event) to stdout, then exit 0.
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
[ -n "$REPO" ] || REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2

# Single poll of the PR. Every gh call pins the RESOLVED --repo "$REPO" (FR-1.3).
PR_JSON="$(gh pr view "$PR" --repo "$REPO" \
    --json number,url,headRefName,headRefOid,baseRefName,reviews,comments 2>/dev/null || true)"

if [ -z "$PR_JSON" ]; then
    # Poll failed (rate limit / transient) — surface as still-polling; the FSM backs off.
    jq -nc --argjson pr "$PR" '{pr:$pr, state:"polling", reviews:[], comments:[]}'
    exit 0
fi

# Inline review comments carry ids / path / line the reply step needs. These are
# MERGED with the PR conversation (issue) comments from `gh pr view ... --json comments`
# below — the Augment "abnormally large" DECLINE is posted as a CONVERSATION comment
# (the same issues/<N>/comments surface retrigger-review.sh posts to), so it lives in
# `.comments`, NOT here. Surfacing only inline comments would make `declined` unreachable
# in production (the classifier never sees the decline). The classifier's finding-comment
# rule requires path+line, so the path-less conversation comments are not miscounted.
COMMENTS_JSON="$(gh api "repos/${REPO}/pulls/${PR}/comments" 2>/dev/null || echo '[]')"

# Coarse state: any review present => let the FSM classify; none => polling. The
# authoritative three-state classification is done by superclaude.pr_submit.classify
# against the probe-locked DetectionContract; this is only a hint for the stream.
STATE="$(printf '%s' "$PR_JSON" | jq -r '
    if ((.reviews // []) | length) > 0 then "review_present" else "polling" end')"

printf '%s' "$PR_JSON" | jq -c \
    --arg state "$STATE" \
    --argjson comments "$COMMENTS_JSON" \
    '{pr:.number, url:.url, head_sha:.headRefOid, base:.baseRefName,
      state:$state, reviews:(.reviews // []),
      comments:((.comments // []) + $comments)}'

exit 0
