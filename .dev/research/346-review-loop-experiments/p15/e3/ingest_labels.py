#!/usr/bin/env python3
"""ingest_labels.py   Read L1/L2 labels, compute agreement, create ADJ steps for disagreements and low-confidence labels, and
(once ADJ is done) write truth.jsonl, disputes.jsonl, agreement.json and author_mismatch.jsonl (contract J8).  Run it twice:
after the L steps (writes the ADJ prompts and steps) and after the ADJ steps (merges the truth).  Labels never come from Jev."""
import json
import sys

import e3lib
import prep_offline as P
from p15common import labels as LB
from p15common.offline_driver import add_steps

FIELDS = ["blocking"]
VALID = {"yes", "no"}


def _step_ok(s):
    import pathlib
    return s["status"] == "done" and pathlib.Path(s["out"]).exists()


def read_labels(prefix, steps):
    """-> {case_id: label dict} from the done steps whose id starts with `prefix` (anonymised ids mapped back)."""
    out = {}
    for s in steps:
        if not s["id"].startswith(prefix + "-") or not _step_ok(s):
            continue
        bid = s["id"].split("-", 1)[1]
        amap = e3lib.load_json(P.BATCHES / (f"adj-{bid}.json" if prefix == "ADJ" else f"{bid}.json"), {})
        for rec in e3lib.read_jsonl(s["out"]):
            cid = amap.get(str(rec.get("case_id")))
            b = str(rec.get("blocking", "")).strip().lower()
            if cid and (b in VALID or (prefix == "ADJ" and b == "undecidable")):
                rec = dict(rec)
                rec["blocking"] = b
                rec.setdefault("confidence", "high")
                out[cid] = rec
    return out


def author_expectation(case):
    ai = case["author_intent"]
    if "expected_blocking" in ai:
        return ai["expected_blocking"]
    if "reviewer_blocking" in ai:
        return "yes" if ai["reviewer_blocking"] else "no"
    return None


def main(argv=None):
    ledger = e3lib.load_json(e3lib.WORKERS, {"steps": []})
    steps = ledger["steps"] if isinstance(ledger, dict) else ledger
    cases = {c["case_id"]: c for c in P.labelable_cases()}
    l1, l2 = read_labels("L1", steps), read_labels("L2", steps)
    lab_steps = [s for s in steps if s["id"].startswith(("L1-", "L2-"))]
    pending = [s["id"] for s in lab_steps if not _step_ok(s)]
    print(f"L1 labels {len(l1)}, L2 labels {len(l2)} of {len(cases)} cases; label steps not done: {len(pending)}")
    if pending or not lab_steps:
        print("PENDING label steps; run offline_advance.py until ALL DONE, then ingest again")
        return 1
    agree = LB.agreement(l1, l2, FIELDS)
    for f, a in agree.items():
        flag = "  VALIDITY WARNING kappa < 0.4" if a["kappa"] is not None and a["kappa"] < 0.4 else ""
        print(f"agreement {f}: raw {a['raw']} kappa {a['kappa']} n {a['n']}{flag}")
    todo = [c for c in LB.to_adjudicate(l1, l2, FIELDS) if c in cases]
    for c in cases:                       # a case with a missing label from either labeler is adjudicated too
        if c not in l1 or c not in l2:
            if c not in todo:
                todo.append(c)
    adj_steps = [s for s in steps if s["id"].startswith("ADJ-")]
    if todo and not adj_steps:
        n = e3lib.decision()["offline"]["batch_size"]
        todo = sorted(todo)
        new = []
        for bi, i in enumerate(range(0, len(todo), n), start=1):
            batch = todo[i:i + n]
            bid = f"b{bi:02d}"
            amap = {f"a{k:02d}": c for k, c in enumerate(batch, start=1)}
            e3lib.write_json(P.BATCHES / f"adj-{bid}.json", amap)
            sid = f"ADJ-{bid}"
            sb = P.SB / sid
            if P.started(sid):
                continue
            P._wipe(sb)
            (sb / "ws/cases").mkdir(parents=True)
            (sb / "home").mkdir()
            (sb / "ws/RUBRIC.md").write_text(P.RUBRIC)
            for anon, cid in amap.items():
                d = sb / "ws/cases" / anon
                d.mkdir()
                c = cases[cid]
                (d / "finding.md").write_text(P._finding_md(c))
                (d / "document.md").write_text(e3lib.candidate_of(c))
                lines = []
                for nm, lab in (("Label A", l1.get(cid)), ("Label B", l2.get(cid))):
                    lines.append(f"## {nm}\n" + (f"blocking: {lab['blocking']}\nsentence: {lab.get('sentence', '')}\nevidence: {lab.get('evidence', '')}\nconfidence: {lab.get('confidence', '')}\n" if lab else "(no label)\n"))
                (d / "labels.md").write_text("\n".join(lines))
            brief = P.ADJ_BRIEF.format(sb=sb, n=len(batch), ids=", ".join(amap))
            prompt = P.write_prompt(sid, sb, brief)
            new.append({"id": sid, "kind": "adjudicate", "model": "sonnet", "prompt": str(prompt), "out": str(sb / "ws/adj.jsonl")})
        add_steps(e3lib.WORKERS, new)
        print(f"ADJ steps added: {len(new)} for {len(todo)} cases (disagreement or low confidence); run offline_advance.py, then ingest again")
        return 0
    if todo and any(not _step_ok(s) for s in adj_steps):
        print("PENDING ADJ steps; run offline_advance.py until ALL DONE, then ingest again")
        return 1
    adj = read_labels("ADJ", steps)
    adj_final = {c: {"blocking": a["blocking"], "reason": a.get("reason", "")} for c, a in adj.items()}
    truth, disputes = LB.merge_truth(l1, l2, adj_final, FIELDS)
    lab = e3lib.LABELS
    lab.mkdir(parents=True, exist_ok=True)
    with open(lab / "truth.jsonl", "w") as f:
        for cid in sorted(truth):
            t = truth[cid]["blocking"]
            f.write(json.dumps({"case_id": cid, "blocking": t, "source": "adj" if cid in adj_final else "agreed"}) + "\n")
    with open(lab / "disputes.jsonl", "w") as f:
        for d in disputes:
            f.write(json.dumps(d, default=str) + "\n")
    e3lib.write_json(lab / "agreement.json", {"fields": agree, "n_cases": len(cases), "n_adjudicated": len(adj_final),
                                              "unresolved": sorted(d["case_id"] for d in disputes if d.get("unresolved"))})
    mism = []
    for cid, t in sorted(truth.items()):
        exp = author_expectation(cases[cid])
        if exp and t["blocking"] in VALID and t["blocking"] != exp:
            mism.append({"case_id": cid, "truth": t["blocking"], "author_or_reviewer_expectation": exp,
                         "kind": "synthetic" if cid.startswith("syn-") else "real"})
    with open(lab / "author_mismatch.jsonl", "w") as f:
        for m in mism:
            f.write(json.dumps(m) + "\n")
    yes = sum(1 for t in truth.values() if t["blocking"] == "yes")
    no = sum(1 for t in truth.values() if t["blocking"] == "no")
    print(f"TRUTH {len(truth)} cases: yes {yes}, no {no}, undecidable {len(truth) - yes - no}; disputes {len(disputes)}; author/reviewer mismatches {len(mism)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
