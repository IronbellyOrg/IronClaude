#!/usr/bin/env bash
# Site sweep, search 1 (fixed pattern list). Run from the repo root. Writes sweep/hits.tsv: pattern-id <TAB> file:line:text.
set -u -o pipefail
D=.dev/review-severity-rule/sweep
: > "$D/hits.tsv"
while IFS=$'\t' read -r id pat; do
  git grep -n -I -i -E "$pat" -- src plugins commands agents skills | awk -v id="$id" '{print id "\t" $0}' >> "$D/hits.tsv"
done < "$D/patterns.tsv"
wc -l < "$D/hits.tsv"
