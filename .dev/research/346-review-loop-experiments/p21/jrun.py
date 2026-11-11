"""Shared Jev runner for p21 (tests 1-3): live client, budget ceiling, journal, parallel calls, answer validation."""
import json, os, sys, pathlib, threading
from concurrent.futures import ThreadPoolExecutor
SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
sys.path.insert(0, str(SP / "p15" / "jev"))
from jevlib.budget import Budget  # noqa: E402
from jevlib.client import JevClient  # noqa: E402
from jevlib.journal import Journal  # noqa: E402

def run(items, *, out_dir, experiment, ceiling_usd=0.50, workers=8, data_classes=("stage2_artifact",)):
    """items: [{id, state, qname, qdef}] -> {id: {status, choice, probs, confidence, tokens}}; resumable via out_dir/answers.json."""
    out_dir = pathlib.Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    apath = out_dir / "answers.json"
    done = json.loads(apath.read_text()) if apath.exists() else {}
    budget = Budget(out_dir / "budget.json", ceiling_usd=ceiling_usd, ceiling_input_tokens=int(ceiling_usd / 0.042e-6))
    journal = Journal(out_dir / "journal.jsonl")
    local = threading.local(); lock = threading.Lock()
    def client():
        if not hasattr(local, "c"):
            local.c = JevClient(experiment=experiment, phase="live", budget=budget, journal=journal, live=True)
        return local.c
    def one(it):
        r = client().ask(it["state"], {it["qname"]: it["qdef"]}, case_id=it["id"], qset_version="v1",
                         data_classes=set(data_classes), purpose=experiment)
        o = {"status": r.status, "error": str(r.error) if r.error else None, "tokens": (r.usage or {}).get("input_tokens"), "model": r.model}
        a = (r.answers or {}).get(it["qname"]) if r.status == "ok" else None
        if a and a.get("type") == "choice" and a.get("choice") in it["qdef"]["criteria"]:
            o.update(choice=a["choice"], probs=a["probs"], confidence=a.get("confidence"))
        elif r.status == "ok":
            o.update(status="invalid", error="answer_shape")
        with lock:
            done[it["id"]] = o
            if len(done) % 50 == 0:
                apath.write_text(json.dumps(done))
        return o
    todo = [it for it in items if done.get(it["id"], {}).get("status") != "ok"]
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(one, todo))
    apath.write_text(json.dumps(done, indent=0))
    st = budget.state()
    return done, {"calls": len(todo), "spent_usd": st.get("spent_usd"), "spent_tokens": st.get("spent_tokens")}
