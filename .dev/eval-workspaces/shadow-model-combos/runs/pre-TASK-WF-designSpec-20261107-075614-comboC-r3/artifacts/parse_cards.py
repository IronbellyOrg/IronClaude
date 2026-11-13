import json, sys
from superclaude.cli.review.findings_v2 import parse_block
out = sys.argv[1]
cov = json.load(open(f"{out}/artifacts/coverage-assign.json"))
ok_first = 0
for n in (1, 2, 3):
    t = open(f"{out}/reviewer-cards/reviewer-{n}-card.md", encoding="utf-8").read()
    r = parse_block(t, lens="reflect-pre")
    print(n, r["state"], "findings:", len(r["findings"]), "errors:", r["errors"])
    ok_first += r["ok"]
print("first-parse valid:", ok_first, "of 3; rate", round(ok_first / 3, 4))
