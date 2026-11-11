"""Pilot: per-reviewer round-1 findings of 7-reviewer pn1d2 runs, from each report's findings-v1 block, plus the merge's grouping (ledger rows)."""
import json, re, sys
from pathlib import Path
SP = Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
out = {}
for run in sys.argv[1:]:
    rd = SP / "p19/rep/pn1d2/runs" / run / "ws/.dev/orca-command-refactor/review"
    fs = []
    for rep in sorted(rd.glob("round1-*.md")):
        rid = rep.stem.split("-", 1)[1]
        m = re.search(r"```findings-v1\n(.*?)```", rep.read_text(), re.S)
        if not m: print("no block", rep); continue
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line.startswith("{"): continue
            try: f = json.loads(line)
            except Exception: print("bad line", rep, line[:80]); continue
            fs.append({"key": f"{run}:{rid}:{f['id']}", "reviewer": rid, "fid": f["id"], "severity": f.get("severity"), "blocking": f.get("blocking"),
                       "category": f.get("category"), "anchor": f.get("anchor"), "anchor2": f.get("anchor2"), "refs": f.get("refs"), "claim": f.get("claim")})
    L = json.load(open(rd / "ledger.json"))
    groups = {}
    for row in L["rows"]:
        for m_ in row["members"]:
            if m_["round"] == 1:
                groups[f"{run}:{m_['reviewer_id']}:{m_['fid']}"] = row["lid"]
    for f in fs: f["merge_row"] = groups.get(f["key"])
    out[run] = fs
    print(run, len(fs), "findings,", len(set(f["merge_row"] for f in fs)), "merge rows,", sum(f["merge_row"] is None for f in fs), "unmapped")
json.dump(out, open("findings.json", "w"), indent=1)
