"""Test 2 features: the loop's own state after round 2 (what the coordinator knows before deciding V2 + round 3)."""
import json, subprocess
from pathlib import Path
SP = Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
DIRS = {"o2": "p19/rep/pn1o", "d2": "p19/rep/pn1d2", "d1": "p19/pn1d", "m1": "p19/pn1m"}
truth = {r["run"]: r for r in json.load(open("truth.json"))}
out = {}
for run in truth:
    rd = SP / DIRS[run[:2]] / "runs" / run / "ws/.dev/orca-command-refactor"
    L = json.load(open(rd / "review/ledger.json"))
    rows = L["rows"]
    def ev(r, rnd, e, status=None):
        return any(h["round"] == rnd and h["event"] == e and (status is None or h.get("status") == status) for h in r["history"])
    def opened_in(r): return min(h["round"] for h in r["history"] if h["event"] == "opened")
    def closed_by2(r): return any(h["round"] <= 2 and (h["event"] == "cleared" or (h["event"] == "prior_note" and h.get("status") == "resolved")) for h in r["history"])
    r1 = [r for r in rows if opened_in(r) == 1]; r2new = [r for r in rows if opened_in(r) == 2]
    v1, v2 = rd / "specs/history/spec-v1.md", rd / "specs/history/spec-v2.md"
    diff = subprocess.run(["diff", str(v1), str(v2)], capture_output=True, text=True).stdout
    out[run] = {
        "round1_findings": len(r1), "round1_blocking": sum(r["blocking"] for r in r1),
        "round2_new_findings": len(r2new), "round2_new_blocking": sum(r["blocking"] for r in r2new),
        "round2_refound_prior_findings": sum(ev(r, 2, "refound") for r in r1),
        "round2_reported_resolved": sum(ev(r, 2, "prior_note", "resolved") for r in r1),
        "open_blocking_after_round2": sum(r["blocking"] and not closed_by2(r) for r in rows if opened_in(r) <= 2),
        "blockers_sent_to_next_revision": len(L["rounds"][1].get("brief_ids") or []),
        "first_revision_changed_lines": sum(1 for l in diff.splitlines() if l[:1] in "<>"),
        "spec_growth_percent_after_first_revision": round(100 * (v2.stat().st_size / v1.stat().st_size - 1), 1),
    }
json.dump(out, open("state.json", "w"), indent=1)
for k, v in out.items(): print(k, truth[k]["d_weighted"], v)
