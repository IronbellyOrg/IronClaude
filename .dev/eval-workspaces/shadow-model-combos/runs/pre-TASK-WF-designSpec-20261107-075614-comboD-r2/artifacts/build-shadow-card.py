"""Write panel/cards/reviewer-N.md: header (persona, model_class, model from resolution.json), findings block, calibration per_finding."""
import json, re, sys
out, n = sys.argv[1], int(sys.argv[2]); per = json.loads(sys.argv[3]); observed = sys.argv[4]
res = json.load(open(f"{out}/panel/resolution.json"))["reviewers"][n - 1]
persona = ["analyzer", "qa", "refactorer"][n - 1]
card = open(f"{out}/reviewer-cards/reviewer-{n}-card.md", encoding="utf-8").read()
m = re.search(r"## Findings block\s*\n+```findings-v2\n.*?\n```", card, re.S)
assert m, "no findings block"
hdr = f"persona: {persona}\nmodel_class: {res['launch']}\nmodel: {res['model']}\nmodel_observed: {observed}\n"
cal = "calibration:\n  per_finding:\n" + "".join(f"    {k}: {v}\n" for k, v in per.items())
open(f"{out}/panel/cards/reviewer-{n}.md", "w", encoding="utf-8").write(hdr + "\n" + m.group(0) + "\n\n```yaml\n" + cal + "```\n")
print(n, "ok", len(per), "calibrated")
