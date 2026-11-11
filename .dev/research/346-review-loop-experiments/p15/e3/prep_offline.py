#!/usr/bin/env python3
"""prep_offline.py --phase pool|convreplay   Offline worker prompts and sandboxes (contract J8, J9; plan 4.4).

--phase pool        Labeling: L1 (sonnet) and L2 (haiku) label every pool finding and every synthetic finding, blind, in batches of 10.
                    A sandbox holds RUBRIC.md and, per case, finding.md + document.md (the full candidate).  Case ids are anonymised
                    (c01..c10) per batch.  Never the packet's derived fields, author intent, group, category or any Jev output.
--phase convreplay  Conventional verifier replay: sonnet, batches of 10 packets (base 60 + perturbations 40), packet-only sandbox.
Both phases append steps to offline/workers.json (existing step ids are kept); run offline_advance.py afterwards."""
import json
import random
import shutil
import sys

import e3lib
import packets as pk
import policy
import questions
from p15common import harnesslib as H
from p15common.offline_driver import add_steps

PROMPTS = e3lib.OFF / "prompts"
SB = e3lib.OFF / "sb"
BATCHES = e3lib.OFF / "batches"

RUBRIC = """For each finding decide with the grading check of the review rules: write "An implementer who follows the stated text as written builds X, and X is wrong because Y."
blocking: yes only if that sentence holds with no further assumption: two stated texts contradict, a stated text causes data loss or breaks a security or safety boundary, or a stated text makes an acceptance criterion impossible to pass. no if the sentence needs a guess about the worse of two readings, if the finding is about a requirement the document never states (missing restriction, undefined state, unspecified edge case), if the quoted text does not exist as quoted, or if the outcome does not follow.
Write one JSON line per finding to labels.jsonl: {"case_id", "blocking": "yes|no", "sentence": "<your grading sentence or why it fails>", "evidence": "<quotes with line numbers>", "confidence": "high|low"}.
Judge only from the document. Severity labels in the finding are not evidence.
"""

LABEL_BRIEF = """You are a blind labeler. Read {sb}/ws/RUBRIC.md first and apply it exactly.
The directory {sb}/ws/cases/ holds {n} case directories ({ids}). Each holds finding.md (one finding of a review) and document.md (the full document the finding is about). Judge each finding only from its document.md.
Write {sb}/ws/labels.jsonl with exactly one JSON line per case directory, using the directory name as case_id (for example "c01"). Do not read any other path. Write only your output file."""

ADJ_BRIEF = """You are an adjudicator. Read {sb}/ws/RUBRIC.md first and apply it exactly.
The directory {sb}/ws/cases/ holds {n} case directories ({ids}). Each holds finding.md, document.md (the full document the finding is about) and labels.md (two earlier labels of the same finding with their grading sentences and evidence, which may disagree). Decide each case yourself from document.md; the earlier labels are not evidence.
Write {sb}/ws/adj.jsonl with exactly one JSON line per case directory: {{"case_id": "<directory name>", "blocking": "yes|no|undecidable", "reason": "<one sentence>"}}. Use undecidable only when the document does not let you decide. Write only your output file."""

CONV_BRIEF_HEAD = ("Assess the supplied relationship and wrong-outcome claim independently. A quoted passage or reviewer assertion is not proof. "
                   "Judge only the supplied evidence; missing applicability or context means insufficient. Do not infer severity from wording, "
                   "create findings, demote policy exceptions or claim the full document is clean.")
CONV_BRIEF = """{head}

You are a conventional verifier. The directory {sb}/ws/packets/ holds {n} packet files ({ids}). Each packet is a JSON object with `finding` (title and wrong_outcome), `evidence` (one or two quoted texts of a document with their line number and surrounding lines) and `facts`. You see only the packet, never the document.
For every packet answer the judgments below with exactly one of "yes", "no" or "uncertain". Use "uncertain" whenever the packet does not settle the judgment.
{judgments}
Write {sb}/ws/answers.jsonl with exactly one JSON line per packet: {{"packet": "<file name without .json>", "outcome_follows": "...", "texts_conflict": "... (only for a packet with two evidence texts)", "evidence_sufficient": "...", "note": "<one sentence>"}}. Write only your output file."""


def _jud(name, q):
    c = q["criteria"]
    return (f"- {name}: {q['instructions']} yes means: {c['true']} no means: {c['false']}")


def judgments_text():
    return "\n".join([_jud("outcome_follows", questions.OUTCOME_FOLLOWS), _jud("texts_conflict (only for a packet with two evidence texts)", questions.TEXTS_CONFLICT),
                      _jud("evidence_sufficient", questions.EVIDENCE_SUFFICIENT)])


def _wipe(p):
    if p.exists():
        shutil.rmtree(p)


def started(step_id):
    """True when the ledger already holds this step in any state but `pending`: its sandbox and output must never be rewritten."""
    led = e3lib.load_json(e3lib.WORKERS, {"steps": []})
    steps = led["steps"] if isinstance(led, dict) else led
    return any(s["id"] == step_id and s["status"] != "pending" for s in steps)


def _finding_md(case):
    return case["packet"]["finding_section"].strip("\n") + "\n"


def labelable_cases():
    cases = [json.loads(p.read_text()) for p in sorted(e3lib.POOL.glob("real*.json"))]
    cases += [json.loads(p.read_text()) for p in sorted((e3lib.OFF / "synth").glob("*.json"))]
    return cases


def write_prompt(step_id, sb, brief):
    PROMPTS.mkdir(parents=True, exist_ok=True)
    p = PROMPTS / f"{step_id}.md"
    p.write_text(H.wrap(sb, brief, False))
    return p


def prep_pool(dec):
    n = dec["offline"]["batch_size"]
    cases = labelable_cases()
    rng = random.Random(dec["offline"]["select_seed"])
    order = sorted(cases, key=lambda c: c["case_id"])
    rng.shuffle(order)
    batches = [order[i:i + n] for i in range(0, len(order), n)]
    BATCHES.mkdir(parents=True, exist_ok=True)
    steps = []
    for bi, batch in enumerate(batches, start=1):
        bid = f"b{bi:02d}"
        amap = {f"c{k:02d}": c["case_id"] for k, c in enumerate(batch, start=1)}
        e3lib.write_json(BATCHES / f"{bid}.json", amap)
        for lab, model in (("L1", "sonnet"), ("L2", "haiku")):
            sid = f"{lab}-{bid}"
            sb = SB / sid
            if started(sid):
                print(f"KEEP {sid}: already launched")
                continue
            _wipe(sb)
            (sb / "ws/cases").mkdir(parents=True)
            (sb / "home").mkdir()
            (sb / "ws/RUBRIC.md").write_text(RUBRIC)
            for anon, c in zip(amap, batch):
                d = sb / "ws/cases" / anon
                d.mkdir()
                (d / "finding.md").write_text(_finding_md(c))
                (d / "document.md").write_text(e3lib.candidate_of(c))
            brief = LABEL_BRIEF.format(sb=sb, n=len(batch), ids=", ".join(amap))
            prompt = write_prompt(sid, sb, brief)
            steps.append({"id": sid, "kind": "label", "model": model, "prompt": str(prompt), "out": str(sb / "ws/labels.jsonl")})
    add_steps(e3lib.WORKERS, steps)
    print(f"POOL PREP {len(cases)} cases in {len(batches)} batches, {len(steps)} label steps (L1 sonnet, L2 haiku)")


def conv_packets():
    """-> [(case_id, packet)] for every base and perturbation case whose packet reaches the screen (code outcome OK)."""
    out = []
    for split in ("base", "perturb"):
        for c in e3lib.load_cases(split):
            p = pk.packet_of_case(c)
            if p.code_outcome == "OK":
                out.append((c["case_id"], p))
    return out


def prep_convreplay(dec):
    n = dec["offline"]["batch_size"]
    items = conv_packets()
    if not items:
        print("ERROR no base/perturbation cases found: run select_base.py and perturb.py first")
        return 2
    rng = random.Random(dec["offline"]["select_seed"] + 100)
    order = sorted(items, key=lambda t: t[0])
    rng.shuffle(order)
    batches = [order[i:i + n] for i in range(0, len(order), n)]
    BATCHES.mkdir(parents=True, exist_ok=True)
    steps = []
    for bi, batch in enumerate(batches, start=1):
        bid = f"b{bi:02d}"
        amap = {f"p{k:02d}": cid for k, (cid, _) in enumerate(batch, start=1)}
        e3lib.write_json(BATCHES / f"conv-{bid}.json", amap)
        sid = f"CV-{bid}"
        sb = SB / sid
        if started(sid):
            print(f"KEEP {sid}: already launched")
            continue
        _wipe(sb)
        (sb / "ws/packets").mkdir(parents=True)
        (sb / "home").mkdir()
        for anon, (_, p) in zip(amap, batch):
            (sb / "ws/packets" / f"{anon}.json").write_text(json.dumps(p.state, indent=1, ensure_ascii=False))
        brief = CONV_BRIEF.format(head=CONV_BRIEF_HEAD, sb=sb, n=len(batch), ids=", ".join(amap), judgments=judgments_text())
        prompt = write_prompt(sid, sb, brief)
        steps.append({"id": sid, "kind": "convcheck", "model": "sonnet", "prompt": str(prompt), "out": str(sb / "ws/answers.jsonl")})
    add_steps(e3lib.WORKERS, steps)
    print(f"CONVREPLAY PREP {len(items)} packets in {len(batches)} batches (sonnet)")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    phase = argv[argv.index("--phase") + 1] if "--phase" in argv else None
    dec = e3lib.decision()
    if phase == "pool":
        if not list(e3lib.POOL.glob("real*.json")):
            print("ERROR offline/pool is empty: run pool.py first")
            return 2
        if not list((e3lib.OFF / "synth").glob("*.json")):
            print("ERROR offline/synth is empty: run cases_synth.py first")
            return 2
        prep_pool(dec)
        return 0
    if phase == "convreplay":
        return prep_convreplay(dec)
    print("usage: prep_offline.py --phase pool|convreplay")
    return 2


if __name__ == "__main__":
    sys.exit(main())
