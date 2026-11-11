import json, re, pathlib, collections
S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f"); T = S/"tasks"
H = S/"scratchpad/p14/haiku-baseline"; base = 57763
tok = collections.defaultdict(dict)
for f in T.glob("*.output"):
    try: lines = f.read_text(errors="ignore").splitlines()
    except Exception: continue
    m = re.search(r"p14/haiku-baseline/runs/(a3-r\d)/PROMPT-(\w+)\.md", "\n".join(lines[:6]))
    if not m: continue
    best = {}
    for l in lines:
        try: d = json.loads(l)
        except Exception: continue
        msg = d.get("message") or {}; u = msg.get("usage"); mid = msg.get("id")
        if u and msg.get("role") == "assistant" and mid: best[mid] = max(best.get(mid, 0), u.get("output_tokens") or 0)
    tok[m.group(1)][m.group(2)] = sum(best.values())
runs = []
for r in range(1, 7):
    run = f"a3-r{r}"; st = json.load(open(H/"runs"/run/"state.json")); L = st["log"]
    reviews = [s for s in ("R1", "R2", "R3") if s in L]
    final = next((L[s]["spec_after"]["bytes"] for s in ("V2", "V1", "R1") if s in L and "spec_after" in L[s]), None)
    aud = L.get("AUD", {}); ids = aud.get("blocking_ids") or ""
    n = 0 if aud.get("verdict") == "PASS" else len(re.findall(r"\b[A-Z][A-Za-z]*-?\d+\b", ids))
    loop = sum(v for k, v in tok[run].items() if k != "AUD")
    runs.append({"run": run, "loop_verdict": L[reviews[-1]].get("verdict"), "reviews": len(reviews), "final_bytes": final,
                 "growth_pct": round((final-base)/base*100, 1), "loop_tokens": loop, "audit_tokens": tok[run].get("AUD"),
                 "audit1_verdict": aud.get("verdict"), "audit1_blocking": n, "audit2": "pending",
                 "harness_anomalies": [x for x in ("stray send_message (r6 R1)",) if run == "a3-r6"] + (["wrote files outside sandbox (r6 R2)"] if run == "a3-r6" else [])})
out = {"stratum": "haiku", "design": "stage2-arm3 (PR #484) with haiku loop workers; audits sonnet", "n": 6, "tokens": "output tokens, each message id once",
       "runs": runs, "blocking_per_audit": [x["audit1_blocking"] for x in runs],
       "mean_blocking": round(sum(x["audit1_blocking"] for x in runs)/6, 2),
       "loop_pass": sum(x["loop_verdict"] == "PASS" for x in runs),
       "mean_loop_tokens": round(sum(x["loop_tokens"] for x in runs)/6), "mean_growth_pct": round(sum(x["growth_pct"] for x in runs)/6, 1),
       "harness_failure_rate": round(sum(bool(x["harness_anomalies"]) for x in runs)/6, 2),
       "note": "single audit per final spec so far; second audits pending (coordinator will add them and update mean_blocking)"}
json.dump(out, open(H/"results.json", "w"), indent=1)
for x in runs: print(x["run"], x["loop_verdict"], x["reviews"], f'{x["growth_pct"]:+}%', x["loop_tokens"], x["audit1_verdict"], x["audit1_blocking"])
print({k: out[k] for k in ("mean_blocking", "loop_pass", "mean_loop_tokens", "mean_growth_pct", "harness_failure_rate")})
