#!/usr/bin/env bash
# Read-only: run the real poll script (unmodified master copy) over the last 70 PRs of the fork.
# Output: /tmp/fix381/diff/payloads/pr-<N>.json (one real monitor snapshot per PR, current state).
set -u
REPO=IronbellyOrg/IronClaude
OUT=/tmp/fix381/diff/payloads
mkdir -p "$OUT"
SCRIPT=/tmp/fix381/old/poll-augment-review.sh
gh pr list --repo "$REPO" --state all --limit 70 --json number --jq '.[].number' > /tmp/fix381/diff/prs.txt
while read -r n; do
  bash "$SCRIPT" --pr "$n" --repo "$REPO" > "$OUT/pr-$n.json" 2> "$OUT/pr-$n.err" || echo "pr $n script exit $?"
done < /tmp/fix381/diff/prs.txt
echo fetched "$(ls $OUT/*.json | wc -l)" payloads
