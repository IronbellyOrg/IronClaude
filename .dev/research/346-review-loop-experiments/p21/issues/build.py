"""Test 3: bug-vs-feature mode choice for /sc:issue --create. Truth = label (bug/enhancement), else the [BUG]/[FEATURE] title prefix."""
import json, re
iss = json.load(open("issues.json"))
PFX = re.compile(r"^\s*\[[^\]]*\]\s*")
def truth(i):
    if "bug" in i["labels"]: return "bug"
    if "enhancement" in i["labels"]: return "feature"
    m = re.match(r"^\s*\[(bug|feature|feat|featrel)\]", i["title"], re.I)
    if m: return "bug" if m.group(1).lower() == "bug" else "feature"
    return None
def redact(t):
    t = re.sub(r"https?://\S+", "<url>", t)
    t = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}", "<email>", t)
    return re.sub(r"(?i)ironbellyorg|github\.com/", "<org>", t)
def excerpt(body, n=800):
    lines = [l for l in body.splitlines() if l.strip() and not l.lstrip().startswith("#") and not re.match(r"^\s*(\*\*|<!--|\||---)", l)]
    return " ".join(" ".join(lines).split())[:n]
cases = []
for i in iss:
    t = truth(i)
    if t and "Temporary acceptance test" not in i["title"]:
        cases.append({"number": i["number"], "truth": t, "title": redact(PFX.sub("", i["title"]).strip()), "excerpt": redact(excerpt(i["body"]))})
json.dump(cases, open("cases.json", "w"), indent=1)
import collections; print(len(cases), collections.Counter(c["truth"] for c in cases))
