#!/bin/bash
# coverage.json from assigned-rows.json and the rows_observed lines of the legacy cards
OUT=$1
jq -n --slurpfile a $OUT/artifacts/assigned-rows.json \
  --argjson o1 "$(grep -h '^rows_observed:' $OUT/reviewer-cards/reviewer-1-card.md | sed 's/rows_observed: //' | sed 's/INF-/"INF-/g;s/,/",/g;s/\]/"]/')" \
  --argjson o2 "$(grep -h '^rows_observed:' $OUT/reviewer-cards/reviewer-2-card.md | sed 's/rows_observed: //' | sed 's/INF-/"INF-/g;s/,/",/g;s/\]/"]/')" \
  --argjson o3 "$(grep -h '^rows_observed:' $OUT/reviewer-cards/reviewer-3-card.md | sed 's/rows_observed: //' | sed 's/INF-/"INF-/g;s/,/",/g;s/\]/"]/')" \
  '{"reviewer-1":{assigned:$a[0]["reviewer-1"],observed:$o1},"reviewer-2":{assigned:$a[0]["reviewer-2"],observed:$o2},"reviewer-3":{assigned:$a[0]["reviewer-3"],observed:$o3}}' > $OUT/panel/coverage.json
