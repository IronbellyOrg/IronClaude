"""Pilot: Jev on cross-reviewer finding pairs of two 7-reviewer runs; one request per pair, a Noul and the earlier Choice over the same state."""
import json, sys, itertools, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21")
import jrun
F = json.load(open("findings.json"))
def fstate(f):
    return {k: f[k] for k in ("severity", "anchor", "anchor2", "refs", "claim") if f.get(k)}
NOUL = {"type": "noul",
        "instructions": "Do `finding_1` and `finding_2` report the same defect in the specification, so that one correction to the specification would resolve both?",
        "criteria": {"true": "Both findings point at the same wrong or missing rule; fixing it resolves both claims.",
                     "false": "The findings point at different problems that need separate corrections, even if they quote the same section or rule."}}
CHOICE = {"type": "choice",
          "instructions": ("Two reviewers each reported a finding about the same specification document. Decide whether the two findings describe the same "
                           "underlying defect, meaning one correction to the specification would resolve both. Citing the same section, rule or acceptance "
                           "check is not enough: two different problems in the same place are different defects."),
          "criteria": {"same_defect": "Both findings describe the same underlying defect; one correction resolves both.",
                       "different_defects": "The findings describe different defects, even if they overlap in location or topic.",
                       "unclear": "The supplied text does not let you decide."}}
pairs = []
for run in ("d2-r1", "d2-r2"):
    for a, b in itertools.combinations(F[run], 2):
        if a["reviewer"] != b["reviewer"]:
            pairs.append((run, a, b))
items = []
for run, a, b in pairs:
    st = {"finding_1": fstate(a), "finding_2": fstate(b)}
    pid = f"{a['key']}~{b['key']}"
    items.append({"id": f"{pid}|noul", "state": st, "qname": "same_defect", "qdef": NOUL})
    items.append({"id": f"{pid}|choice", "state": st, "qname": "same_defect", "qdef": CHOICE})
print(len(pairs), "pairs", len(items), "calls")
if "--go" in sys.argv:
    ans, st = jrun.run(items, out_dir="out", experiment="p21-pilot", ceiling_usd=0.60, workers=10)
    print(st, collections.Counter(v["status"] for v in ans.values()))
