import json, sys, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21")
import jrun
cases = json.load(open("cases.json"))
QDEF = {"type": "choice",
        "instructions": ("Someone wants to file an issue against a software project and wrote the description below. "
                         "Classify the request by what it asks for, not by how it is worded."),
        "criteria": {"bug": "Something that already exists does not behave as documented or intended: wrong output, a crash, a broken or misleading help text, a check that fails, a wrong value.",
                     "feature": "A new capability, a deliberate change to intended behavior, a refactor, a configuration or data change, or new documentation or tests for something that works as designed.",
                     "unclear": "The description does not let you tell."}}
items = []
for c in cases:
    items.append({"id": f"{c['number']}|title", "state": {"description": c["title"]}, "qname": "issue_mode", "qdef": QDEF})
    items.append({"id": f"{c['number']}|full", "state": {"description": c["title"] + ". " + c["excerpt"]}, "qname": "issue_mode", "qdef": QDEF})
ans, st = jrun.run(items, out_dir="out", experiment="p21-issue-mode", ceiling_usd=0.05, workers=6, data_classes=("stage2_artifact",))
print(st, collections.Counter((v["status"], v.get("choice")) for v in ans.values()))
