"""Setup-vs-model diagnostic on the 46 Opus-labelled A2 packets: original question, reordered options, atomic Nouls, full-spec state."""
import json, re, sys, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21")
sys.path.insert(0, "/home/user/IronClaude/.dev/research/346-review-loop-experiments/p18/seams")
import jrun
from a2_observability import OBS_INSTRUCTIONS, OBS_OPTIONS
LBL = "/home/user/IronClaude/.dev/research/346-review-loop-experiments/p20/label"
P = []
for b in (1, 2, 3): P += json.load(open(f"{LBL}/packets_b{b}.json"))
orig = {"type": "choice", "instructions": OBS_INSTRUCTIONS, "criteria": dict(OBS_OPTIONS)}
rev = {"type": "choice", "instructions": OBS_INSTRUCTIONS, "criteria": dict(reversed(list(OBS_OPTIONS.items())))}
def noul(instr, t, f): return {"type": "noul", "instructions": instr, "criteria": {"true": t, "false": f}}
EMPTY = noul("Would `check.pass_condition` still be satisfied if the command under test produced no output and wrote no file?",
             "An empty or missing result meets the pass condition as written.",
             "The pass condition names a specific value, field, status or file content that an empty or missing result does not have.")
UNPROD = noul("Does `check.pass_condition` need a file, field, status or output that neither `check.text` nor any row in `cited` says will exist when the check runs?",
              "The pass condition needs something that no text in the state says will exist at that point.",
              "Everything the pass condition looks at is produced by a step in `check.text` or described by a row in `cited`.")
def contra(i): return noul(f"Does `check` require something that `cited[{i}]` forbids, excludes or defers to a later phase?",
                           f"`cited[{i}]` forbids, excludes or defers something the check needs, so the check and that row cannot both hold.",
                           f"`cited[{i}]` is consistent with the check: it describes a step, rule or output the check can rely on.")
SPEC_ORIG = {"type": "choice", "instructions": OBS_INSTRUCTIONS.replace("the cited rows in `cited`, and the facts a program already established in `code_stage`",
              "and the full specification in `spec`"), "criteria": dict(OBS_OPTIONS)}
SPEC_CONFLICT = noul("Does `spec` contain a rule that forbids, excludes or defers to a later phase something that `check` requires?",
                     "Some rule in `spec` forbids, excludes or defers something the check needs at its phase, so the check cannot pass as written.",
                     "Every rule in `spec` that bears on the check allows what the check needs at its phase.")
SPEC_EMPTY = EMPTY
items = []
for p in P:
    lid = p["label_id"]
    st = {"check": p["check"], "cited": p["cited"], "code_stage": p["code_stage"]}
    for qn, q in (("orig", orig), ("rev", rev)):
        items.append({"id": f"{lid}|packet|{qn}", "state": st, "qname": qn, "qdef": q})
    st2 = {"check": p["check"], "cited": p["cited"]}
    items.append({"id": f"{lid}|atomic|empty", "state": st2, "qname": "empty_passes", "qdef": EMPTY})
    items.append({"id": f"{lid}|atomic|unprod", "state": st2, "qname": "unproduced", "qdef": UNPROD})
    for i in range(len(p["cited"])):
        items.append({"id": f"{lid}|atomic|contra{i}", "state": st2, "qname": f"contradicts_{i}", "qdef": contra(i)})
    spec = re.sub(r"/home/[^\s`)]*", "<home-path>", open(p["spec_path"]).read()).replace("IronbellyOrg", "<org>").replace("github.com/", "<host>/")
    st3 = {"check": p["check"], "spec": spec}
    for qn, q in (("orig", SPEC_ORIG), ("conflict", SPEC_CONFLICT), ("empty", SPEC_EMPTY)):
        items.append({"id": f"{lid}|spec|{qn}", "state": st3, "qname": qn, "qdef": q})
print(len(items), "calls")
if __name__ == "__main__" and "--go" in sys.argv:
    ans, st = jrun.run(items, out_dir="out", experiment="p21-a2diag", ceiling_usd=0.30, workers=6, data_classes=("s1_spec",))
    print(st, collections.Counter(v["status"] for v in ans.values()), collections.Counter(v.get("error") for v in ans.values() if v["status"] != "ok"))
