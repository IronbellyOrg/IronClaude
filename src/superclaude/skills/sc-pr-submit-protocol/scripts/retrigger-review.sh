#!/usr/bin/env bash
#
# retrigger-review.sh — S5a re-trigger wrapper for sc:pr-submit (R1 / FR-8).
#
# Purpose : Post one `auggie review` re-trigger comment on the PR's conversation
#           thread so the Augment App performs a re-review of the just-pushed
#           remediation commit. A push does NOT auto-trigger an Augment re-review —
#           the App reviews only on PR-open or an explicit operator trigger comment.
# Usage   : retrigger-review.sh --pr <N>
# Exit    : 0 on a completed post; 2 on usage error (bad/missing/non-numeric --pr);
#           127 on a missing dependency (gh not on PATH — an environment failure, NOT
#           CLI misuse); 1 on a failed post.
# Spec    : merged-spec-v1.1-addendum.md FR-8 / INV-R1; refs/review-retrigger.md.
#           All gh I/O is isolated here (NFR-6). The gh api path pins
#           repos/IronbellyOrg/IronClaude/... (the fork, never upstream).
#
# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.

set -euo pipefail

die() { printf 'retrigger-review: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) [ $# -ge 2 ] || die "missing value for --pr <N>" 2; PR="$2"; shift 2 ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done

[ -n "$PR" ] || die "missing required --pr <N>" 2
# Require a numeric PR — a stringified None/empty/garbage would otherwise build a
# malformed ``issues/<PR>/comments`` target (e.g. .../issues/None/comments → 404).
case "$PR" in ''|*[!0-9]*) die "invalid --pr value (must be a positive integer): $PR" 2 ;; esac
# Missing gh is an ENVIRONMENT failure, not CLI misuse — exit 127 (command-not-found),
# distinct from the usage-error exit 2 above.
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 127

# Post the re-trigger comment on the PR conversation thread (issue-comment surface).
# The body token is exactly `auggie review` (one of the contract's accepted_trigger_phrases).
gh api --method POST \
    "repos/IronbellyOrg/IronClaude/issues/${PR}/comments" \
    -f body="auggie review" >/dev/null \
    || die "re-trigger comment POST failed for PR ${PR}" 1

printf 're-triggered review on PR %s (posted "auggie review")\n' "$PR"
exit 0
