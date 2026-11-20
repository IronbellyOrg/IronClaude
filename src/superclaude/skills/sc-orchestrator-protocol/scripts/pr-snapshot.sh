#!/usr/bin/env bash
#
# pr-snapshot.sh: one read-only snapshot of a pull request for the orchestrator's merge gate.
#
# Usage  : pr-snapshot.sh --pr <N> --repo <owner/repo> --out <dir>
# Writes : <dir>/ci.json       the one JSON line of poll-ci-checks.sh
#          <dir>/reviews.json  the one JSON line of poll-augment-review.sh
# Prints : the two file paths, one per line (ci=..., reviews=...).
# Exit   : 0 when both poll scripts ran and wrote their file; the exit code of the first
#          poll script that failed (a usage or prerequisite failure), after removing its
#          file; 2 for a usage error here.
#
# This script has no decision logic: it runs the two poll scripts of /sc:pr-submit by
# their installed path and saves what they print. Classifying the two files is the job of
# `superclaude orchestrator merge-gate`, which decides with the superclaude.pr_submit core.
# A file that is missing at the gate is a snapshot that was not completed.

set -euo pipefail

die() { printf 'pr-snapshot: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
REPO=""
OUT=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) PR="${2:-}"; shift 2 ;;
        --repo) REPO="${2:-}"; shift 2 ;;
        --out) OUT="${2:-}"; shift 2 ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done
[[ "$PR" =~ ^[1-9][0-9]*$ ]] || die "missing or invalid --pr <N>" 2
[[ "$REPO" =~ ^[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9._-]+$ ]] || die "missing or invalid --repo <owner/repo>" 2
[ -n "$OUT" ] || die "missing --out <dir>" 2

# The installed copy first, then the project copy that `make sync-dev` makes in a checkout.
SCRIPTS_REL="skills/sc-pr-submit-protocol/scripts"
find_script() {
    local name="$1" top
    if [ -f "$HOME/.claude/$SCRIPTS_REL/$name" ]; then
        printf '%s\n' "$HOME/.claude/$SCRIPTS_REL/$name"
        return 0
    fi
    top="$(git rev-parse --show-toplevel 2>/dev/null || true)"
    if [ -n "$top" ] && [ -f "$top/.claude/$SCRIPTS_REL/$name" ]; then
        printf '%s\n' "$top/.claude/$SCRIPTS_REL/$name"
        return 0
    fi
    return 1
}
CI_SCRIPT="$(find_script poll-ci-checks.sh)" || die "poll-ci-checks.sh is not installed (run superclaude install)" 2
REVIEW_SCRIPT="$(find_script poll-augment-review.sh)" || die "poll-augment-review.sh is not installed (run superclaude install)" 2

mkdir -p "$OUT"
chmod 700 "$OUT"

# Write to a temporary file in the same folder and rename, so the gate never reads half a file.
snapshot() {
    local name="$1" script="$2" tmp status=0
    tmp="$(mktemp "$OUT/.${name}.XXXXXX")"
    bash "$script" --pr "$PR" --repo "$REPO" > "$tmp" || status=$?
    if [ "$status" -ne 0 ]; then
        rm -f "$tmp"
        rm -f "$OUT/$name"
        exit "$status"
    fi
    chmod 600 "$tmp"
    mv "$tmp" "$OUT/$name"
}
snapshot ci.json "$CI_SCRIPT"
snapshot reviews.json "$REVIEW_SCRIPT"

printf 'ci=%s\n' "$OUT/ci.json"
printf 'reviews=%s\n' "$OUT/reviews.json"
