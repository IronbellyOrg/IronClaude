"""E2 Stage 0 label ingestion (contract J8): L1/L2 labels -> agreement -> ADJ prompts -> truth.

Run it twice (coordinator): once after the L1/L2 workers are done (writes ADJ prompts and ledger steps if needed), once after the
ADJ workers are done (writes truth.jsonl).  A case with no ADJ need gets its truth at the first run.
  uv run --no-project python ingest_labels.py --phase s0
Exit codes: 0 done or ADJ steps added, 3 waiting for workers.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import e2lib as L                               # noqa: E402
import stage0                                   # noqa: E402
from p15common import labels as LB              # noqa: E402
from p15common import offline_driver as OD     # noqa: E402

LAB = L.OFF / "labels"
ADJ_BRIEF = ("Adjudicate the {n} cases in {sb}/ws/cases.json. First read {sb}/ws/ADJ-RUBRIC.md in full and follow it exactly. Each "
             "case names its document under {sb}/ws/docs/ and carries both labelers' answers. Write your {n} lines to "
             "{sb}/ws/adjudication.jsonl. Do not edit any other file.")


def clean_label(rec, fields=L.FIELDS):
    """Return a normalized label dict, or None when it is not a usable label (missing/invalid decision field)."""
    if not isinstance(rec, dict) or "case_id" not in rec:
        return None
    out = dict(rec)
    for f in fields:
        v = str(rec.get(f, "")).strip().lower()
        if v not in L.ENUM[f]:
            return None
        out[f] = v
    if out["defect_real"] == "no":                      # evidence fields are meaningless for a rejected defect
        out["evidence_sufficient"] = out["evidence_minimal"] = "n/a"
    out["confidence"] = "low" if str(rec.get("confidence", "")).strip().lower() != "high" else "high"
    return out


def read_labels(path, fields=L.FIELDS) -> dict:
    out = {}
    for r in L.read_jsonl(path):
        c = clean_label(r, fields)
        if c is not None:
            out[c["case_id"]] = c
    return out


def label_steps(role):
    raw = json.loads(L.LEDGER.read_text())
    steps = raw["steps"] if isinstance(raw, dict) else raw
    return [s for s in steps if s.get("kind") == "label" and s.get("role") == role], steps


def collect(role):
    steps, _ = label_steps(role)
    got, waiting = {}, []
    for s in steps:
        if s["status"] not in ("done", "lost") and not pathlib.Path(s["out"]).exists():
            waiting.append(s["id"])
        got.update(read_labels(s["out"]))
    return got, waiting


def needs_adjudication(l1, l2, case_ids) -> list:
    """Disagreement, low confidence or a missing label (J8), plus agreed cases whose evidence set needs correcting
    (the labelers agree the defect is real but the set is insufficient or not minimal)."""
    ids = set(LB.to_adjudicate(l1, l2, L.FIELDS)) | {c for c in case_ids if c not in l1 or c not in l2}
    for c in case_ids:
        if c in l1 and c in l2 and l1[c]["defect_real"] == "yes" and l2[c]["defect_real"] == "yes":
            if "no" in (l1[c]["evidence_sufficient"], l2[c]["evidence_sufficient"], l1[c]["evidence_minimal"], l2[c]["evidence_minimal"]):
                ids.add(c)
    return sorted(ids & set(case_ids))


def make_adj_steps(cases, adj_ids, l1, l2, bs):
    by_batch = {}
    for i, ids in enumerate(bs, start=1):
        sel = [c for c in ids if c in adj_ids]
        if sel:
            by_batch[i] = sel
    steps = []
    for bi, ids in by_batch.items():
        views, docs = [], {}
        for cid in ids:
            c = cases[cid]
            src = stage0.E2 / c["packet"]["doc"]
            v = L.case_view(c, src.read_text(encoding="utf-8"))
            v["labeler_1"] = {k: l1[cid].get(k) for k in (*L.FIELDS, "evidence", "other_blocker", "confidence")} if cid in l1 else None
            v["labeler_2"] = {k: l2[cid].get(k) for k in (*L.FIELDS, "evidence", "other_blocker", "confidence")} if cid in l2 else None
            views.append(v)
            docs[src.name] = src
        sid = f"ADJ-b{bi:02d}"
        sb = L.build_sandbox(sid, views, docs, L.ADJ_RUBRIC)
        (sb / "ws" / "RUBRIC.md").rename(sb / "ws" / "ADJ-RUBRIC.md")
        prompt = L.write_prompt(sid, ADJ_BRIEF.format(n=len(ids), sb=sb))
        steps.append({"id": sid, "kind": "adjudicate", "model": "sonnet", "prompt": str(prompt),
                      "out": str(sb / "ws" / "adjudication.jsonl"), "batch": bi, "role": "ADJ", "cases": ids})
    OD.add_steps(L.LEDGER, steps)
    return steps


def read_adjudication(cases, adj_steps):
    adj, missing = {}, []
    for s in adj_steps:
        for r in L.read_jsonl(s["out"]):
            c = clean_label(r)
            if c is None:
                continue
            cid = c["case_id"]
            doc = (stage0.E2 / cases[cid]["packet"]["doc"]).read_text(encoding="utf-8") if cid in cases else ""
            qs = r.get("final_evidence_quotes")
            qs = [q for q in qs if isinstance(q, str) and q.strip()] if isinstance(qs, list) else []
            if c["defect_real"] == "yes" and (not qs or any(q not in doc for q in qs)):
                c.update({"defect_real": "undecidable", "evidence_sufficient": "undecidable", "evidence_minimal": "undecidable",
                          "reason": "adjudicator quotes missing or not exact substrings: " + str(c.get("reason", ""))})
                qs = []
            c["final_evidence_quotes"] = qs
            adj[cid] = c
        for cid in s["cases"]:
            if cid not in adj:
                missing.append(cid)
    return adj, missing


def build_truth(cases, l1, l2, adj, adj_ids):
    adj = dict(adj)
    for c in adj_ids:
        if c not in adj:
            adj[c] = {"defect_real": "undecidable", "evidence_sufficient": "undecidable", "evidence_minimal": "undecidable",
                      "reason": "adjudication missing", "final_evidence_quotes": []}
    base, disputes = LB.merge_truth(l1, l2, {c: adj[c] for c in adj if c in adj_ids}, L.FIELDS)
    truth = []
    for cid in sorted(cases):
        t = base.get(cid)
        if t is None:
            truth.append({"case_id": cid, "defect_real": "undecidable", "evidence_sufficient": "undecidable",
                          "evidence_minimal": "undecidable", "final_evidence_quotes": [], "unresolved": True,
                          "adjudicated": False, "other_blocker": []})
            continue
        a = adj.get(cid)
        unresolved = any(t.get(f) == "undecidable" for f in L.FIELDS)
        quotes = (a or {}).get("final_evidence_quotes") if a else cases[cid]["packet"]["evidence_quotes"]
        others = []
        for src in (l1.get(cid), l2.get(cid), a):
            ob = (src or {}).get("other_blocker")
            if isinstance(ob, str) and ob.strip().lower() not in ("", "none") and ob not in others:
                others.append(ob)
        truth.append({"case_id": cid, **t, "final_evidence_quotes": quotes or [], "unresolved": unresolved,
                      "adjudicated": cid in adj_ids, "other_blocker": others})
    return truth, disputes


def author_mismatch(cases, truth):
    out = []
    for t in truth:
        c = cases[t["case_id"]]
        exp = c["author_intent"]["expect"]
        want = "yes" if exp == "defect" else "no"
        if t["defect_real"] != want:
            out.append({"case_id": t["case_id"], "kind": "defect_real", "author_expected": want, "truth": t["defect_real"],
                        "category": c["category"]})
        elif t["defect_real"] == "yes" and sorted(t["final_evidence_quotes"]) != sorted(c["packet"]["evidence_quotes"]):
            out.append({"case_id": t["case_id"], "kind": "evidence_corrected", "author_quotes": c["packet"]["evidence_quotes"],
                        "truth_quotes": t["final_evidence_quotes"], "category": c["category"]})
    return out


def ingest(phase="s0") -> int:
    cases = {c["case_id"]: c for c in stage0.load_cases()}
    dec = stage0.load_decision()
    ids = sorted(cases)
    bs = [ids[i:i + dec["stage0"]["batch_size"]] for i in range(0, len(ids), dec["stage0"]["batch_size"])]
    l1, w1 = collect("L1")
    l2, w2 = collect("L2")
    if w1 or w2:
        print("WAITING for label workers:", ", ".join(w1 + w2))
        return 3
    LAB.mkdir(parents=True, exist_ok=True)
    L.write_jsonl(LAB / "L1.jsonl", [l1[c] for c in sorted(l1)])
    L.write_jsonl(LAB / "L2.jsonl", [l2[c] for c in sorted(l2)])
    ag = LB.agreement(l1, l2, L.FIELDS)
    warn = [f for f, v in ag.items() if v["kappa"] is not None and v["kappa"] < 0.4]
    adj_ids = needs_adjudication(l1, l2, ids)
    (LAB / "agreement.json").write_text(json.dumps({"fields": ag, "validity_warnings_kappa_lt_0.4": warn, "adjudicate": adj_ids,
                                                    "n_cases": len(ids), "n_l1": len(l1), "n_l2": len(l2)}, indent=1))
    _, steps = label_steps("L1")
    adj_steps = [s for s in steps if s.get("kind") == "adjudicate"]
    if adj_ids and not adj_steps:
        adj_steps = make_adj_steps(cases, adj_ids, l1, l2, bs)
        print(f"{len(adj_ids)} cases need adjudication: {', '.join(adj_ids)}")
        print("ADJ steps added to the ledger:", ", ".join(s["id"] for s in adj_steps),
              "-> run offline_advance.py until ALL DONE, then run ingest_labels.py again")
        return 0
    if adj_ids:
        pending = [s["id"] for s in adj_steps if s["status"] not in ("done", "lost") and not pathlib.Path(s["out"]).exists()]
        if pending:
            print("WAITING for ADJ workers:", ", ".join(pending))
            return 3
    adj, _missing = read_adjudication(cases, adj_steps)
    truth, disputes = build_truth(cases, l1, l2, adj, set(adj_ids))
    L.write_jsonl(LAB / "truth.jsonl", truth)
    L.write_jsonl(LAB / "disputes.jsonl", disputes)
    am = author_mismatch(cases, truth)
    L.write_jsonl(LAB / "author_mismatch.jsonl", am)
    unresolved = [t["case_id"] for t in truth if t["unresolved"]]
    print(f"truth written: {len(truth)} cases; adjudicated {len(adj_ids)}; unresolved {len(unresolved)} {unresolved}; "
          f"author mismatches {len(am)}; kappa warnings {warn}")
    print("next: uv run --no-project python stage0.py")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="s0")
    a = ap.parse_args(argv)
    return ingest(a.phase)


if __name__ == "__main__":
    sys.exit(main())
