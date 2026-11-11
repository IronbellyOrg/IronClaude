"""p22 A/B analysis: ledger scores of the 12 finals (blind Sonnet, s130-s141), permutation tests, Jev stage stats, row counts, loop tokens."""
import json, random, statistics as S, sys, glob
from pathlib import Path
SP = Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
SC = SP / "p17/score"; P22 = SP / "p22"
sys.path.insert(0, str(P22 / "pn1c")); import analysis as A
key = json.load(open(SC / "key.json"))
L = json.load(open("/home/user/IronClaude/.dev/research/346-review-loop-experiments/p17/ledger.json"))
sev = {d["id"]: d["severity"] for d in L["defects"]}; W = {"blocking": 3, "medium": 2, "minor": 1}; RES = {"PRESENT", "PARTIAL", "WORSE", "MOOT_BAD"}
rows = []
for sid, k in key.items():
    if not k["arm"].startswith("p22-"): continue
    f = SC / "out" / f"{sid}.json"
    if not f.exists(): print("missing score", sid, k["run"]); continue
    o = json.load(open(f)); st = {d["id"]: d["status"] for d in o["defects"]}
    arm = k["arm"][4:]; run = k["run"]; d = P22 / ("pn1c" if arm == "c3" else "pn1j") / "runs" / run
    s = json.load(open(d / "state.json")); led = json.load(open(d / "ws/.dev/orca-command-refactor/review/ledger.json"))
    r1 = [r for r in led["rows"] if any(m["round"] == 1 for m in r["members"])]
    toks = {}
    for k2 in s["launched"]:
        if k2.startswith(("AUD",)): continue
        t = A.step_tokens(d / f"PROMPT-{k2}.md", "/tmp/claude-0/*/*/tasks/*.output", None)
        toks[k2] = (t or {}).get("out")
    rows.append({"sid": sid, "arm": arm, "run": run,
                 "fixed": sum(v in ("FIXED", "DELETED_OK") for v in st.values()),
                 "resid_blk": sum(v in RES and sev[i] == "blocking" for i, v in st.items()),
                 "weighted": sum(W[sev[i]] for i, v in st.items() if v in RES),
                 "intro": sum(x["status"] == "PRESENT" for x in o["introduced"]),
                 "new": len(o.get("other_new_defects") or []),
                 "r1_rows": len(r1), "r1_blocking_rows": sum(r["blocking"] for r in r1),
                 "jev": s["log"].get("JEV1"), "decision": (s.get("final") or {}).get("decision"),
                 "loop_out_tokens": sum(v or 0 for v in toks.values()), "tok_missing": sum(v is None for v in toks.values())})
rows.sort(key=lambda r: (r["arm"], r["run"]))
for r in rows: print({k: v for k, v in r.items() if k != "jev"}, "jev:", r["jev"] and {k: r["jev"][k] for k in ("candidate_pairs", "linked", "failed", "usd")})
def perm(metric, n=20000):
    c = [r[metric] for r in rows if r["arm"] == "c3"]; j = [r[metric] for r in rows if r["arm"] == "j3"]
    obs = S.mean(j) - S.mean(c); allv = c + j; rnd = random.Random(1); hits = 0
    for _ in range(n):
        rnd.shuffle(allv); hits += abs(S.mean(allv[len(c):]) - S.mean(allv[:len(c)])) >= abs(obs) - 1e-9
    return round(S.mean(c), 2), round(S.mean(j), 2), round(obs, 2), round(hits / n, 3)
print("\nmetric: control mean, jev mean, diff (jev-control), two-sided permutation p")
for m in ("fixed", "resid_blk", "weighted", "intro", "new", "r1_rows", "r1_blocking_rows", "loop_out_tokens"):
    print(m, perm(m))
js = [r["jev"] for r in rows if r["jev"]]
print("jev stage:", {k: sum(x[k] or 0 for x in js) for k in ("candidate_pairs", "linked", "failed")}, "usd", round(sum(x["usd"] or 0 for x in js), 4))
json.dump(rows, open(P22 / "ab_rows.json", "w"), indent=1)
