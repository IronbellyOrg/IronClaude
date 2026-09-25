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
# gh pr checks exits 8 on pending while still printing JSON. Do not `|| echo '[]'`
# on the same stdout — that concatenates two arrays and breaks --argjson.
REQUIRED_JSON="$(gh pr checks "$PR" --repo "$REPO" --required --json "$JSON_FIELDS" 2>/dev/null || true)"
ALL_JSON="$(gh pr checks "$PR" --repo "$REPO" --json "$JSON_FIELDS" 2>/dev/null || true)"
is_array() { printf '%s' "$1" | jq -es 'length == 1 and (.[0] | type == "array")' >/dev/null 2>&1; }
as_array() { printf '%s' "${1:-[]}" | jq -cs 'if length == 1 and (.[0] | type == "array") then .[0] else [] end' 2>/dev/null || printf '[]\n'; }

REQUIRED_VALID=0
ALL_VALID=0
if is_array "$REQUIRED_JSON"; then REQUIRED_VALID=1; fi
if is_array "$ALL_JSON"; then ALL_VALID=1; fi

CHECKS_JSON="$(jq -nc --argjson req "$(as_array "$REQUIRED_JSON")" --argjson all "$(as_array "$ALL_JSON")" '
    if ($req | length) > 0 then $req else $all end
')"

# Coarse hint only — classify_checks is authoritative.
STATE="$(printf '%s' "$CHECKS_JSON" | jq -r '
    if length == 0 then "clean"
    elif any(.[]; (.bucket // "") == "pending") then "polling"
    elif any(.[]; (.bucket // "") == "fail" or (.bucket // "") == "cancel"
              or ((.state // "") | ascii_downcase) == "action_required") then "findings"
    else "clean" end')"
# Only two confirmed empty arrays prove there are no configured checks.
if [ "$CHECKS_JSON" = '[]' ] && { [ "$REQUIRED_VALID" -eq 0 ] || [ "$ALL_VALID" -eq 0 ]; }; then
    STATE="polling"
fi

# Re-sample head after checks so a mid-poll push cannot pair new checks with an old SHA.
HEAD1="$(printf '%s' "$PR_JSON" | jq -r '.headRefOid // empty')"
PR_AFTER="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"
[ -n "$PR_AFTER" ] && PR_JSON="$PR_AFTER"
HEAD2="$(printf '%s' "$PR_JSON" | jq -r '.headRefOid // empty')"
if [ -n "$HEAD1" ] && [ -n "$HEAD2" ] && [ "$HEAD1" != "$HEAD2" ]; then
    STATE="polling"
fi

printf '%s' "$PR_JSON" | jq -c \
    --arg state "$STATE" \
    --argjson checks "$CHECKS_JSON" \
    '{pr:.number, head_sha:.headRefOid, source:"ci", state:$state, checks:$checks}'

exit 0
