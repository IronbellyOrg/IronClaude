# The only panel-msg/1 card schema check (design 2.1), shared by panel-post, r4-hook and audit.py.
# Usage: jq -R -r --arg flagger <rid> -f card.jq   (one raw line per input line; prints the line if valid, nothing otherwise)
# The 600-byte limit is checked by the caller before this filter.
. as $raw
| (try fromjson catch null)
| select(type == "object")
| select((keys | sort) == (["v","id","run","from","to","t","kind","move","anchor","category","severity"] | sort))
| select(.v == "panel-msg/1" and .kind == "card")
| select((.id | type) == "string" and (.id | test("^c[0-9]+$")))
| select((.t | type) == "number")
| select(.from == $flagger)
| select((.to | type) == "string" and (.run | type) == "string")
| select(.move as $m | ["M3","M4","M5","M6","M9"] | index([$m]) != null)
| select(.category as $c | ["contradiction","unpassable-check","data-loss","safety","missing-requirement","other"] | index([$c]) != null)
| select(.severity as $s | ["CRITICAL","MAJOR","MINOR"] | index([$s]) != null)
| select((.anchor | type) == "string" and (.anchor | length) >= 12 and (.anchor | length) <= 200)
| $raw
