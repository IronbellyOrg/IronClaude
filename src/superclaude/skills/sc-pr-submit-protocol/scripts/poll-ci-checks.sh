#!/usr/bin/env bash
#
# poll-ci-checks.sh — CI poller for sc:pr-submit Wave 8.
#
# Purpose : Do a SINGLE poll of a PR's checks and emit exactly ONE JSON line.
# Usage   : poll-ci-checks.sh --pr <N> [--repo <owner/repo>]
# Output  : one line of JSON: {"pr":N,"head_sha":"...","source":"ci",
#           "state":"polling|clean|findings","checks":[...]}
# Exit    : 0 always on a completed poll (fail-soft); 2 on a usage error.
# Spec    : .dev/specs/pr-submit-ci-monitor.md FR-CI-2 / FR-CI-10 / FR-CI-11.
#           Authoritative classify is superclaude.pr_submit.ci.classify_checks.
#
# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.

set -euo pipefail

die() { printf 'poll-ci-checks: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
REPO=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) PR="${2:-}"; shift 2 ;;
        --repo) REPO="${2:-}"; shift 2 ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done

[ -n "$PR" ] || die "missing required --pr <N>" 2
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2
command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 2

REPO="${REPO:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)}"
[ -n "$REPO" ] || REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2

PR_JSON="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"
if [ -z "$PR_JSON" ]; then
    jq -nc --argjson pr "$PR" '{pr:$pr, head_sha:"", source:"ci", state:"polling", checks:[]}'
    exit 0
fi

JSON_FIELDS="name,state,bucket,link,workflow"
REQUIRED_JSON="$(gh pr checks "$PR" --repo "$REPO" --required --json "$JSON_FIELDS" 2>/dev/null || echo '[]')"
ALL_JSON="$(gh pr checks "$PR" --repo "$REPO" --json "$JSON_FIELDS" 2>/dev/null || echo '[]')"

CHECKS_JSON="$(jq -nc --argjson req "$REQUIRED_JSON" --argjson all "$ALL_JSON" '
    if ($req | type == "array") and ($req | length) > 0 then $req
    elif ($all | type == "array") then $all
    else [] end
')"

# Coarse hint only — classify_checks is authoritative.
STATE="$(printf '%s' "$CHECKS_JSON" | jq -r '
    if length == 0 then "clean"
    elif any(.[]; (.bucket // "") == "pending") then "polling"
    elif any(.[]; (.bucket // "") == "fail" or (.bucket // "") == "cancel"
              or ((.state // "") | ascii_downcase) == "action_required") then "findings"
    else "clean" end')"

printf '%s' "$PR_JSON" | jq -c \
    --arg state "$STATE" \
    --argjson checks "$CHECKS_JSON" \
    '{pr:.number, head_sha:.headRefOid, source:"ci", state:$state, checks:$checks}'

exit 0
