"""Label ingestion for one phase (contract J8 steps 2-5).

  uv run --no-project python ingest_labels.py --phase smoke

Run it after the L1/L2 workers finished.  If cases need adjudication it writes the ADJ prompts, adds the steps to offline/workers.json and
stops; run offline_advance.py again, then run this script again.  Writes offline/labels/{L1,L2}.jsonl, agreement.json, disputes.jsonl,
truth.jsonl and author_mismatch.jsonl.  A labeler's closure_correct is re-derived from its own three fields; a mismatch makes the label
low-confidence (so the case goes to adjudication)."""
import _boot  # noqa: F401
import argparse
import json
import pathlib

from p15common import labels as LB
from p15common.datasets import load_cases
from p15common.offline_driver import add_steps
import prep_offline as P

LABELS = P.OFFLINE / "labels"
FIELDS = P.LABEL_FIELDS
ALLOWED = {"resolved": {"yes", "no"}, "obligation_preserved": {"yes", "no", "n/a"}, "new_conflict": {"yes", "no"}}


def derive_closure(lab: dict) -> str:
    r, o, n = lab.get("resolved"), lab.get("obligation_preserved"), lab.get("new_conflict")
    if "undecidable" in (r, o, n):
        return "undecidable"
    return "yes" if (r == "yes" and o in ("yes", "n/a") and n == "no") else "no"


def read_jsonl(path):
    out = []
    p = pathlib.Path(path)
    if not p.exists():
        return out
    for ln in p.read_text(errors="ignore").splitlines():
        ln = ln.strip()
        if not ln.startswith("{"):
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def normalize(rec: dict, allow_undecidable=False):
    """-> normalized label dict or None when a decision field is missing or has a value outside the rubric."""
    lab = {"case_id": rec.get("case_id"), "evidence": rec.get("evidence") or rec.get("reason") or "",
           "confidence": "low" if str(rec.get("confidence", "high")).lower() == "low" else "high"}
    for f, ok in ALLOWED.items():
        v = str(rec.get(f, "")).strip().lower()
        if v == "undecidable" and allow_undecidable:
            lab[f] = v
        elif v in ok:
            lab[f] = v
        else:
            return None
    lab["closure_correct"] = derive_closure(lab)
    claimed = str(rec.get("closure_correct", "")).strip().lower()
    if claimed and claimed != lab["closure_correct"]:
        lab["confidence"] = "low"
        lab["inconsistent_closure"] = True
    if "reason" in rec:
        lab["reason"] = rec["reason"]
    return lab


def collect(phase, role):
    """-> {case_id: label} over the batches of `role` (L1|L2); cases without a valid label are absent (they go to adjudication)."""
    plan = json.load(open(P.OFFLINE / f"phase-{phase}.json"))
    labs, missing_files = {}, []
    for b, ids in plan["label_batches"].items():
        out = P.SANDBOXES / f"{role}-{phase}-{b}" / "labels.jsonl"
        if not out.exists():
            missing_files.append(str(out)); continue
        for rec in read_jsonl(out):
            lab = normalize(rec)
            if lab and lab["case_id"] in ids:
                labs[lab["case_id"]] = lab
    return labs, missing_files


def adj_prompts(phase, ids, l1, l2, cases_by_id, ledger=P.LEDGER):
    steps = []
    for bi, chunk in enumerate([ids[i:i + P.BATCH] for i in range(0, len(ids), P.BATCH)], 1):
        sid = f"ADJ-{phase}-b{bi:02d}"
        sb = P.fresh_sandbox(sid)
        for cid in chunk:
            P.write_case_files(sb, cases_by_id[cid])
        disputes = {cid: {"labeler_1": l1.get(cid), "labeler_2": l2.get(cid)} for cid in chunk}
        (sb / "disputes.json").write_text(json.dumps(disputes, indent=1))
        (sb / "RUBRIC.md").write_text(P.ADJ_RUBRIC + "\nCases in this sandbox: " + ", ".join(sorted(chunk)) + "\n")
        out = sb / "adjudications.jsonl"
        brief = (f"Read {sb}/RUBRIC.md and follow it exactly. The cases are in {sb}/cases/<case_id>/ and the earlier labels in {sb}/disputes.json . "
                 f"Write one JSON line per case (every case in this sandbox) to {out}. Write only that file.")
        steps.append({"id": sid, "kind": "adjudicate", "model": "sonnet", "prompt": str(P.write_prompt(sb, brief)), "out": str(out)})
    add_steps(ledger, steps)
    return steps


def collect_adj(phase):
    ledger = json.load(open(P.LEDGER))
    steps = ledger if isinstance(ledger, list) else ledger["steps"]
    adj, files = {}, []
    for s in steps:
        if s["id"].startswith(f"ADJ-{phase}-"):
            files.append(s)
            for rec in read_jsonl(s["out"]):
                lab = normalize(rec, allow_undecidable=True)
                if lab:
                    lab["reason"] = rec.get("reason", "")
                    adj[lab["case_id"]] = lab
    return adj, files


def finalize(phase, cases, l1, l2, adj):
    LABELS.mkdir(parents=True, exist_ok=True)
    truth, disputes = LB.merge_truth(l1, l2, adj, FIELDS)
    for c, t in list(truth.items()):
        t["closure_correct"] = derive_closure(t)
    agree = LB.agreement(l1, l2, FIELDS)
    warn = [f for f, a in agree.items() if a["kappa"] is not None and a["kappa"] < 0.4]
    (LABELS / "agreement.json").write_text(json.dumps({"fields": agree, "kappa_below_0.4": warn, "n_l1": len(l1), "n_l2": len(l2)}, indent=1))
    (LABELS / "truth.jsonl").write_text("".join(json.dumps({"case_id": c, **t}) + "\n" for c, t in sorted(truth.items())))
    (LABELS / "disputes.jsonl").write_text("".join(json.dumps(d) + "\n" for d in disputes))
    by_id = {c["case_id"]: c for c in cases}
    mism = [{"case_id": c, "truth": t["closure_correct"], "author_intent": by_id[c]["author_intent"].get("closure_correct"),
             "category": by_id[c]["category"], "variant": by_id[c]["variant"]}
            for c, t in sorted(truth.items()) if c in by_id and t["closure_correct"] != by_id[c]["author_intent"].get("closure_correct")]
    (LABELS / "author_mismatch.jsonl").write_text("".join(json.dumps(m) + "\n" for m in mism))
    return truth, disputes, agree, warn, mism


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=sorted(P.PHASE_DIRS))
    a = ap.parse_args(argv)
    phase = a.phase
    cases = load_cases(P.cases_dir(phase))
    by_id = {c["case_id"]: c for c in cases}
    l1, f1 = collect(phase, "L1")
    l2, f2 = collect(phase, "L2")
    if f1 or f2:
        print(f"WAIT labelers not finished: {len(f1) + len(f2)} output file(s) missing (run offline_advance.py)")
        return 1
    LABELS.mkdir(parents=True, exist_ok=True)
    for role, labs in (("L1", l1), ("L2", l2)):
        (LABELS / f"{role}.jsonl").write_text("".join(json.dumps(v) + "\n" for _, v in sorted(labs.items())))
    need = LB.to_adjudicate(l1, l2, FIELDS)
    need = sorted(set(c for c in need if c in by_id) | {c for c in by_id if c not in l1 and c not in l2})
    adj, adj_steps = collect_adj(phase)
    if need and not adj_steps:
        steps = adj_prompts(phase, need, l1, l2, by_id)
        print(f"ADJ needed for {len(need)} case(s): {len(steps)} adjudication step(s) added; run offline_advance.py, then run this script again")
        return 0
    if need and any(not pathlib.Path(s["out"]).exists() for s in adj_steps):
        print("WAIT adjudication not finished (run offline_advance.py)")
        return 1
    truth, disputes, agree, warn, mism = finalize(phase, cases, l1, l2, adj)
    und = [c for c, t in truth.items() if t["closure_correct"] == "undecidable"]
    print(f"truth for {len(truth)} of {len(cases)} cases; disputes {len(disputes)}; undecidable {len(und)}; author mismatches {len(mism)}")
    for f, v in agree.items():
        print(f"  {f}: raw {v['raw']} kappa {v['kappa']} n {v['n']}")
    if warn:
        print(f"WARN kappa < 0.4 on {warn} (validity warning, not a stop)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
