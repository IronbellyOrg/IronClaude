"""Writes the offline worker prompts and the offline ledger for one phase (contract J8, J9; plan 4.4).

  uv run --no-project python prep_offline.py --phase smoke

Per phase: label batches (10 cases each, cases shuffled across groups with random.Random(11)) x {L1 sonnet, L2 haiku}, and conventional
checker batches (sonnet, the 2.4 brief over the eligible packets).  ADJ prompts are written later by ingest_labels.py.
Sandbox of each worker: offline/sb/<id>/ (cases/<case_id>/{before.md, after.md, finding.md, packet.json}, RUBRIC.md, PROMPT.md, home/)."""
import _boot  # noqa: F401
import argparse
import difflib
import json
import pathlib
import random
import shutil

from p15common import harnesslib as H
from p15common.datasets import label_packet, load_cases
from p15common.offline_driver import add_steps
from questions import checker_brief

OFFLINE = _boot.E1 / "offline"
LEDGER = OFFLINE / "workers.json"
SANDBOXES = OFFLINE / "sb"
LABEL_FIELDS = ["resolved", "obligation_preserved", "new_conflict", "closure_correct"]
BATCH = 10
BATCH_SEED = 11
PHASE_DIRS = {"smoke": "smoke", "calibration": "calibration", "heldout": "heldout"}

RUBRIC = """For each case decide, using before.md, after.md and finding.md (the whole documents are authoritative; packet.json is a convenience extract):
resolved: yes if after.md no longer produces the wrong outcome the finding describes, anywhere in the document; else no.
obligation_preserved: yes if after.md still requires what the finding's protected requirement (the text the finding says must hold) requires, in any words or place; no if it was deleted, weakened or made optional; n/a only if the finding itself was wrong about that requirement.
new_conflict: yes if a text added or changed in after.md contradicts another requirement of after.md; else no.
closure_correct: yes only if resolved = yes, obligation_preserved is yes or n/a, and new_conflict = no.
Write one JSON line per case to labels.jsonl: {"case_id", "resolved", "obligation_preserved", "new_conflict", "closure_correct", "evidence": "<quotes from after.md>", "confidence": "high|low"}.
Judge only from the documents. Do not guess what the author intended.
"""

ADJ_RUBRIC = """You are the adjudicator. For each case in disputes.json two independent labelers disagreed or were unsure. Decide the final label yourself from the documents in cases/<case_id>/ (before.md, after.md, finding.md; the whole documents are authoritative). The two earlier labels and their evidence are in disputes.json: weigh the evidence, do not count votes, and check every quote against the documents.
""" + RUBRIC.split("Write one JSON line")[0] + """If a field cannot be settled from the documents, write "undecidable" for that field.
Write one JSON line per case to adjudications.jsonl: {"case_id", "resolved", "obligation_preserved", "new_conflict", "closure_correct", "reason": "<one sentence>"}.
Judge only from the documents. Do not guess what the author intended.
"""


def cases_dir(phase):
    return OFFLINE / "cases" / PHASE_DIRS[phase]


def full_diff(case):
    i = case["packet"]["inputs"]
    return "".join(difflib.unified_diff(i["before_text"].splitlines(True), i["after_text"].splitlines(True), "before.md", "after.md", n=3))


def write_case_files(sb: pathlib.Path, case: dict):
    d = sb / "cases" / case["case_id"]
    d.mkdir(parents=True, exist_ok=True)
    i = label_packet(case)["packet"]["inputs"]       # never author_intent, split, group, family, category or variant
    (d / "before.md").write_text(i["before_text"])
    (d / "after.md").write_text(i["after_text"])
    f = i["finding"]
    (d / "finding.md").write_text(f"{f['heading']}\n{f['body']}\n")
    (d / "packet.json").write_text(json.dumps({"case_id": case["case_id"], "finding": {"heading": f["heading"], "body": f["body"]},
                                                "full_diff": full_diff(case)}, indent=1))


def fresh_sandbox(sid) -> pathlib.Path:
    sb = SANDBOXES / sid
    if sb.exists():
        shutil.rmtree(sb)
    (sb / "home").mkdir(parents=True)
    return sb


def write_prompt(sb: pathlib.Path, brief: str, wsdir: str = "cases") -> pathlib.Path:
    p = sb / "PROMPT.md"
    p.write_text(H.WRAP.format(sb=str(sb), wsdir=wsdir, cmdpart="", brief=brief))
    return p


def batches(items, seed=BATCH_SEED, size=BATCH):
    items = list(items)
    random.Random(seed).shuffle(items)
    return [items[i:i + size] for i in range(0, len(items), size)]


def label_batches(cases):
    return batches(sorted(cases, key=lambda c: c["case_id"]))


def conv_batches(cases, n_batches=None):
    el = sorted((c for c in cases if c["packet"]["precheck"] == "ok"), key=lambda c: c["case_id"])
    random.Random(BATCH_SEED).shuffle(el)
    n = n_batches or max(1, -(-len(el) // BATCH))
    return [b for b in (el[i::n] for i in range(n)) if b]


def prep(phase: str, ledger=LEDGER, offline=OFFLINE):
    cases = load_cases(cases_dir(phase))
    if not cases:
        raise SystemExit(f"no cases in {cases_dir(phase)}")
    steps, plan = [], {"phase": phase, "label_batches": {}, "conv_batches": {}}
    # idempotent: a step that was already launched, finished or lost keeps its sandbox (and its output) untouched
    started = set()
    if pathlib.Path(ledger).exists():
        raw = json.load(open(ledger))
        started = {x["id"] for x in (raw if isinstance(raw, list) else raw["steps"]) if x.get("status") != "pending"}
    for bi, b in enumerate(label_batches(cases), 1):
        ids = [c["case_id"] for c in b]
        plan["label_batches"][f"b{bi:02d}"] = ids
        for role, model in (("L1", "sonnet"), ("L2", "haiku")):
            sid = f"{role}-{phase}-b{bi:02d}"
            if sid in started:
                continue
            sb = fresh_sandbox(sid)
            for c in b:
                write_case_files(sb, c)
            (sb / "RUBRIC.md").write_text(RUBRIC + "\nCases in this sandbox: " + ", ".join(sorted(ids)) + "\n")
            out = sb / "labels.jsonl"
            brief = (f"Read {sb}/RUBRIC.md and follow it exactly. The cases are in {sb}/cases/<case_id>/ . "
                     f"Write one JSON line per case (every case in this sandbox) to {out}. Write only that file.")
            steps.append({"id": sid, "kind": "label", "model": model, "prompt": str(write_prompt(sb, brief)), "out": str(out)})
    for bi, b in enumerate(conv_batches(cases), 1):
        sid = f"CC-{phase}-b{bi:02d}"
        plan["conv_batches"][f"b{bi:02d}"] = [c["case_id"] for c in b]
        if sid in started:
            continue
        sb = fresh_sandbox(sid)
        (sb / "packets.json").write_text(json.dumps([{"packet_id": c["case_id"], "state": c["packet"]["state"]} for c in b], indent=1))
        out = sb / "answers.jsonl"
        steps.append({"id": sid, "kind": "convcheck", "model": "sonnet",
                      "prompt": str(write_prompt(sb, checker_brief(sb / "packets.json", out), wsdir="")), "out": str(out)})
    pathlib.Path(offline).mkdir(parents=True, exist_ok=True)
    (pathlib.Path(offline) / f"phase-{phase}.json").write_text(json.dumps(plan, indent=1))
    add_steps(ledger, steps)
    return steps, plan


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=sorted(PHASE_DIRS))
    a = ap.parse_args(argv)
    steps, plan = prep(a.phase)
    k = {}
    for s in steps:
        k[(s["kind"], s["model"])] = k.get((s["kind"], s["model"]), 0) + 1
    print(f"phase {a.phase}: {len(steps)} worker steps {dict((f'{a}:{b}', n) for (a, b), n in k.items())}; ledger {LEDGER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
