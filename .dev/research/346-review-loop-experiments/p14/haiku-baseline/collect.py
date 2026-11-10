"""Refresh results.json: tokens by recount.py (id-once, prompt-matched), audits AUD and AUD2 from state.json.
mean_blocking uses both audits once all six AUD2 exist; mean_blocking_aud1 is the single-audit value."""
import json, re, pathlib, subprocess, sys
H = pathlib.Path(__file__).resolve().parent; base = 57763
subprocess.run([sys.executable, str(H/"recount.py")], capture_output=True, check=True, cwd=H)
tok = json.load(open(H/"tokens_generic.json"))
def nblock(a):
    if not a: return None
    return 0 if a.get("verdict") == "PASS" else len(re.findall(r"\b[A-Z][A-Za-z]*-?\d+\b", a.get("blocking_ids") or ""))
runs = []
for r in range(1, 7):
    run = f"a3-r{r}"; st = json.load(open(H/"runs"/run/"state.json")); L = st["log"]; steps = tok.get(run, {}).get("steps", {})
    reviews = [s for s in ("R1", "R2", "R3") if s in L]
    final = next((L[s]["spec_after"]["bytes"] for s in ("V2", "V1", "R1") if s in L and "spec_after" in L[s]), None)
    a1, a2 = L.get("AUD"), L.get("AUD2")
    loop = sum(v for k, v in steps.items() if k in ("R1", "V1", "R2", "V2", "R3"))
    runs.append({"run": run, "loop_verdict": L[reviews[-1]].get("verdict"), "reviews": len(reviews), "final_bytes": final,
                 "growth_pct": round((final-base)/base*100, 1), "loop_tokens": loop, "audit_tokens": steps.get("AUD"), "audit2_tokens": steps.get("AUD2"),
                 "audit1_verdict": (a1 or {}).get("verdict"), "audit1_blocking": nblock(a1),
                 "audit2_verdict": (a2 or {}).get("verdict") if a2 else "pending", "audit2_blocking": nblock(a2),
                 "harness_anomalies": [x for x in ("stray send_message (r6 R1)",) if run == "a3-r6"] + (["wrote files outside sandbox (r6 R2)"] if run == "a3-r6" else [])})
b1 = [x["audit1_blocking"] for x in runs]; b2 = [x["audit2_blocking"] for x in runs]
have2 = all(x is not None for x in b2)
m1 = round(sum(b1)/6, 2)
out = {"stratum": "haiku", "design": "stage2-arm3 (PR #484) with haiku loop workers; audits sonnet (AUD + AUD2, D3)", "n": 6, "tokens": "output tokens, each message id once, matched by PROMPT path or prompt text",
       "runs": runs, "blocking_per_audit": b1, "blocking_per_audit2": b2,
       "mean_blocking_aud1": m1, "mean_blocking_aud2": round(sum(b2)/6, 2) if have2 else None,
       "mean_blocking": round((sum(b1)+sum(b2))/12, 2) if have2 else m1,
       "audits_used": 12 if have2 else 6,
       "loop_pass": sum(x["loop_verdict"] == "PASS" for x in runs),
       "mean_loop_tokens": round(sum(x["loop_tokens"] for x in runs)/6), "mean_growth_pct": round(sum(x["growth_pct"] for x in runs)/6, 1),
       "harness_failure_rate": round(sum(bool(x["harness_anomalies"]) for x in runs)/6, 2),
       "note": "both audits used" if have2 else "single audit (AUD) per final spec so far; AUD2 pending, mean_blocking == mean_blocking_aud1 until all six AUD2 exist"}
json.dump(out, open(H/"results.json", "w"), indent=1)
for x in runs: print(x["run"], x["loop_verdict"], x["reviews"], f'{x["growth_pct"]:+}%', x["loop_tokens"], x["audit1_verdict"], x["audit1_blocking"], x["audit2_verdict"], x["audit2_blocking"])
print({k: out[k] for k in ("mean_blocking", "mean_blocking_aud1", "mean_blocking_aud2", "loop_pass", "mean_loop_tokens", "mean_growth_pct", "harness_failure_rate")})
