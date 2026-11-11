import json, sys, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21")
import jrun
state = json.load(open("state.json")); truth = {r["run"]: r for r in json.load(open("truth.json"))}
CTX = ("An automated loop reviews a specification with a panel of reviewers, revises it, and re-reviews it, for at most three reviews. "
       "Round 1 was a full panel review followed by a revision; round 2 was a re-review of that revision. The loop must now decide whether "
       "to run one more revision and a final re-review. The counts below are everything the loop knows at this point.")
Q = {
 "v1": {"type": "choice", "instructions": CTX + " Will one more revision and re-review reduce the real defects in the specification?",
        "criteria": {"will_help": "Another revision is likely to fix real remaining defects without adding new ones.",
                     "will_not_help": "Another revision is unlikely to fix anything real, or likely to add as many problems as it removes.",
                     "unclear": "The counts do not let you tell."}},
 "v2": {"type": "choice", "instructions": CTX + " Is it worth spending one more revision and re-review on this specification?",
        "criteria": {"worth_it": "Yes: the state suggests real defects remain that a revision can fix.",
                     "not_worth_it": "No: the loop has stalled or is churning, so another cycle will not improve the specification.",
                     "unclear": "The counts do not let you tell."}},
}
items = [{"id": f"{run}|{q}", "state": {"loop_state_after_round_2": s}, "qname": "next_cycle", "qdef": Q[q]} for run, s in state.items() for q in Q]
ans, st = jrun.run(items, out_dir="out", experiment="p21-stop", ceiling_usd=0.02, workers=6)
print(st, collections.Counter((v["status"], v.get("choice")) for v in ans.values()))
def auc(score, lab):
    pos = [s for s, l in zip(score, lab) if l]; neg = [s for s, l in zip(score, lab) if not l]
    return round(sum((x > y) + 0.5 * (x == y) for x in pos for y in neg) / (len(pos) * len(neg)), 3)
runs = sorted(state); lab = [truth[r]["d_weighted"] < 0 for r in runs]
print(f"runs {len(runs)}, next cycle helped in {sum(lab)}")
for q, k in (("v1", "will_help"), ("v2", "worth_it")):
    p = [ans[f"{r}|{q}"].get("probs", {}).get(k, 0) for r in runs]
    ch = [ans[f"{r}|{q}"].get("choice") for r in runs]
    print(q, "AUC P(help)", auc(p, lab), "choices", collections.Counter(zip(ch, lab)))
for f in state[runs[0]]:
    v = [state[r][f] for r in runs]
    print(f"{f:42s} AUC(higher=>helps) {auc(v, lab)}")
