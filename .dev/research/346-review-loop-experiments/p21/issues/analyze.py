import json, re, collections, os
cases = {str(c["number"]): c for c in json.load(open("cases.json"))}
A = json.load(open("answers.json"))
S = json.load(open("sonnet-answers.json")) if os.path.exists("sonnet-answers.json") else {}
BUGW = re.compile(r"(?i)\b(fix|fails?|failing|broken|bug|error|crash|wrong|missing|incorrect|doesn'?t|does not|not work|regress|omits?|should)\b")
def kw(text): return "bug" if BUGW.search(text) else "feature"
def score(name, get):
    for v in ("title", "full"):
        n = right = unc = 0; conf = collections.Counter()
        for num, c in cases.items():
            p = get(num, v); n += 1
            if p == "unclear" or p is None: unc += 1; continue
            right += p == c["truth"]; conf[(c["truth"], p)] += 1
        dec = n - unc
        print(f"{name:22s} {v:5s} decided {dec}/{n}  accuracy on decided {right}/{dec} = {right / max(1, dec):.2f}  overall {right / n:.2f}  {dict(conf)}")
score("jev", lambda n, v: A.get(f"{n}|{v}", {}).get("choice"))
def jev_conf(th):
    def g(n, v):
        a = A.get(f"{n}|{v}", {})
        return a.get("choice") if a.get("choice") != "unclear" and max(a.get("probs", {}).values() or [0]) >= th else "unclear"
    return g
score("jev p>=0.9", jev_conf(0.9))
score("keyword rule", lambda n, v: kw(cases[n]["title"] if v == "title" else cases[n]["title"] + " " + cases[n]["excerpt"]))
if S: score("sonnet", lambda n, v: S.get(f"{n}|{v}"))
