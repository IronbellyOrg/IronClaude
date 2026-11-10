"""E2 Stage 0 offline prep: label sandboxes, prompts and the worker ledger for 3 batches of 8 cases.

L1 = fresh sonnet worker, L2 = fresh haiku worker, each labels every case of a batch blind (contract J8).  ADJ prompts are made by
ingest_labels.py after the labels exist.  Usage: uv run --no-project python prep_offline.py [--phase s0]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import e2lib as L                               # noqa: E402
import stage0                                   # noqa: E402
from p15common import offline_driver as OD     # noqa: E402

BRIEF = ("Label the {n} cases in {sb}/ws/cases.json. First read {sb}/ws/RUBRIC.md in full and follow it exactly. Each case names its "
         "document under {sb}/ws/docs/. Write your {n} label lines to {sb}/ws/labels.jsonl. Do not edit any other file.")


def batches(cases, batch_size):
    ids = sorted(c["case_id"] for c in cases)
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]


def prep_s0() -> list:
    dec = stage0.load_decision()
    cases = {c["case_id"]: c for c in stage0.load_cases()}
    bs = batches(list(cases.values()), dec["stage0"]["batch_size"])
    steps = []
    for bi, ids in enumerate(bs, start=1):
        views, docs = [], {}
        for cid in ids:
            c = cases[cid]
            src = stage0.E2 / c["packet"]["doc"]
            text = src.read_text(encoding="utf-8")
            views.append(L.case_view(c, text))
            docs[src.name] = src
        for role, model in (("L1", dec["stage0"]["l1_model"]), ("L2", dec["stage0"]["l2_model"])):
            sid = f"{role}-b{bi:02d}"
            sb = L.build_sandbox(sid, views, docs, L.RUBRIC)
            prompt = L.write_prompt(sid, BRIEF.format(n=len(ids), sb=sb))
            steps.append({"id": sid, "kind": "label", "model": model, "prompt": str(prompt), "out": str(sb / "ws" / "labels.jsonl"),
                          "batch": bi, "role": role, "cases": ids})
    OD.add_steps(L.LEDGER, steps)
    return steps


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="s0")
    a = ap.parse_args(argv)
    if a.phase != "s0":
        print("only phase s0 exists in Session 1")
        return 2
    steps = prep_s0()
    print(f"prepared {len(steps)} label steps ({len({s['batch'] for s in steps})} batches) -> {L.LEDGER}")
    for s in steps:
        print(f"  {s['id']} model={s['model']} cases={s['cases'][0]}..{s['cases'][-1]} prompt={s['prompt']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
