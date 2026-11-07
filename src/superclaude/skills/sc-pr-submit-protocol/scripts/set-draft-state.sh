#!/usr/bin/env bash
#
# set-draft-state.sh — read or set the draft state of a pull request for the
# sc:pr-submit merge guard (issue #375).
#
# Purpose : The merge guard turns a PR into a draft while a fix cycle runs and marks
#           it ready again once the fix push is confirmed. All GitHub I/O of that
#           guard is isolated here; the decisions live in the pure module
#           superclaude.pr_submit.merge_guard (NFR-6). Every call is idempotent, so
#           a retry or a resume re-issue is safe.
# Usage   : set-draft-state.sh --pr <N> [--repo <owner/repo>] --read
#           set-draft-state.sh --pr <N> [--repo <owner/repo>] --to draft|ready
# Output  : exactly one JSON line on stdout.
#           --read : {"ok":true,"state":"OPEN","isDraft":false,"headRefOid":"<sha>",
#                     "autoMergeRequest":false,"transitions":3,"complete":true,
#                     "error":null}. When only the timeline call fails the line has
#                     "transitions":null and "complete":false.
#           --to   : {"ok":true,"state":"OPEN","isDraft":true,"headRefOid":"<sha>",
#                     "changed":true,"error":null}. The state is read first: a PR that
#                     is not OPEN gives "ok":false and "error":"not_open"; a PR already
#                     in the target state gives "changed":false and no mutation; after
#                     a mutation the state is read again and a mismatch gives
#                     "error":"verify_failed".
# Exit    : 0 on success; 1 when a CLI call fails or a check fails (the JSON line is
#           still printed, with "ok":false); 2 on usage error (missing or non-numeric
#           --pr, missing mode, unknown argument); 127 when the CLI or jq is missing
#           (an environment failure, not misuse).
# Spec    : the merge-guard protocol reference (refs/merge-guard.md). The repo is the
#           RESOLVED origin owner/repo, never the upstream parent: every call carries
#           --repo "$REPO" or a repos/${REPO}/... path.

set -euo pipefail

die() { printf 'set-draft-state: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
REPO=""
MODE=""
TO=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) [ $# -ge 2 ] || die "missing value for --pr <N>" 2; PR="$2"; shift 2 ;;
        --repo) [ $# -ge 2 ] || die "missing value for --repo <owner/repo>" 2; REPO="$2"; shift 2 ;;
        --read) MODE="read"; shift ;;
        --to)
            [ $# -ge 2 ] || die "missing value for --to draft|ready" 2
            case "$2" in draft|ready) ;; *) die "invalid --to value (must be draft or ready): $2" 2 ;; esac
            MODE="to"; TO="$2"; shift 2 ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done

[ -n "$PR" ] || die "missing required --pr <N>" 2
case "$PR" in ''|*[!0-9]*) die "invalid --pr value (must be a positive integer): $PR" 2 ;; esac
[ -n "$MODE" ] || die "missing mode (--read or --to draft|ready)" 2
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 127
command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 127

# Resolve the target repo (owner/repo): the origin remote first, then the CLI default.
REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
[ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2

VIEW='{"state":null,"isDraft":null,"headRefOid":null,"autoMergeRequest":null}'

# Read the PR into VIEW; return 1 when the call fails or the answer has no state.
fetch_view() {
    local answer
    answer="$(gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest 2>/dev/null)" || return 1
    printf '%s' "$answer" | jq -e 'has("state") and has("isDraft")' >/dev/null 2>&1 || return 1
    VIEW="$answer"
}

# One JSON line for --read. $1 = ok (true|false), $2 = transitions (number|null),
# $3 = complete (true|false), $4 = error text (empty for none).
emit_read() {
    jq -c --argjson ok "$1" --argjson transitions "$2" --argjson complete "$3" --arg error "$4" \
        '{ok:$ok,state:.state,isDraft:.isDraft,headRefOid:.headRefOid,autoMergeRequest:(.autoMergeRequest != null),transitions:$transitions,complete:$complete,error:(if $error == "" then null else $error end)}' \
        <<<"$VIEW"
}

# One JSON line for --to. $1 = ok (true|false), $2 = changed (true|false), $3 = error text.
emit_to() {
    jq -c --argjson ok "$1" --argjson changed "$2" --arg error "$3" \
        '{ok:$ok,state:.state,isDraft:.isDraft,headRefOid:.headRefOid,changed:$changed,error:(if $error == "" then null else $error end)}' \
        <<<"$VIEW"
}

if [ "$MODE" = "read" ]; then
    fetch_view || { emit_read false null false read_failed; exit 1; }
    transitions="null"
    complete="false"
    # Count the draft/ready transitions on the PR timeline (all pages).
    if count="$(gh api --paginate "repos/${REPO}/issues/${PR}/timeline" --jq '.[] | select(.event=="convert_to_draft" or .event=="ready_for_review") | .event' 2>/dev/null | wc -l | tr -d ' ')"; then
        transitions="$count"
        complete="true"
    fi
    emit_read true "$transitions" "$complete" ""
    exit 0
fi

# --to draft|ready: read first, change only when needed, verify after.
if [ "$TO" = "draft" ]; then want="true"; else want="false"; fi
fetch_view || { emit_to false false read_failed; exit 1; }
if [ "$(jq -r '.state' <<<"$VIEW")" != "OPEN" ]; then
    emit_to false false not_open
    exit 1
fi
if [ "$(jq -r '.isDraft' <<<"$VIEW")" = "$want" ]; then
    emit_to true false ""
    exit 0
fi
if [ "$TO" = "draft" ]; then
    gh pr ready "$PR" --repo "$REPO" --undo >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }
else
    gh pr ready "$PR" --repo "$REPO" >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }
fi
fetch_view || { emit_to false false verify_failed; exit 1; }
if [ "$(jq -r '.isDraft' <<<"$VIEW")" != "$want" ]; then
    emit_to false false verify_failed
    exit 1
fi
emit_to true true ""
exit 0
