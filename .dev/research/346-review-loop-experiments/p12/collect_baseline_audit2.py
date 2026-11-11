import json, re, pathlib, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11")
import harness as h
OUT = pathlib.Path(__file__).parent/"baseline-audit2"; res = {}
for r in range(1, 7):
    run = f"a3-r{r}"; p = OUT/run/"ws/.dev/orca-command-refactor/review/audit.md"
    if not p.exists(): res[run] = {"status": "missing"}; continue
    t = p.read_text(errors="ignore"); vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", t, re.I)
    v = vs[-1].upper() if vs else "NONE"
    ids = h.ids_from(p) if v == "FAIL" else None
    res[run] = {"verdict": v, "blocking_ids": ids, "n_blocking": (len(re.findall(r"[A-Za-z]+-?\d+", ids)) if ids else 0)}
json.dump(res, open(OUT/"results.json", "w"), indent=1)
for k, v in res.items(): print(k, v)
