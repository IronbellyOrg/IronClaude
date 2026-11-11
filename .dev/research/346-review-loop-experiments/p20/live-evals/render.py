#!/usr/bin/env python3
"""Render the live-eval artifacts from combos.json.

  render.py stage-a  --out DIR --repo-root ROOT [--reps 3] [--models id,id]
        ROOT = a checkout of the PR branch (it must hold the review rules file, spec-panel.md and .dev/orca-command-refactor)
        per (model, rep): a sandbox (ws/ + home/) and PROMPT.md, plus DIR/manifest.json
  render.py panels   --out DIR [--t2b-models id,id] [--tiers TIERS.json]
        per panel in combos.json: <id>.panel.json (review-panel/1) and one eval tier file with tier2b filled
  render.py schedule --out FILE --reps 6 --seed N [--panels C0-default4,C1-live7,...]
        blocked randomization for Stage C: every block holds one run of each panel, order shuffled per block

Nothing here calls a model. Stage C itself runs through harness/ (see README).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import shutil
import sys

HERE = pathlib.Path(__file__).parent
COMBOS = json.load(open(HERE / "combos.json"))
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
RULES_REL = "src/superclaude/rules/prompts/document_review_loop_prompts.md"
CMD_REL = "src/superclaude/commands/spec-panel.md"
SPEC_ORIGINAL = HERE.parent.parent / "p17" / "spec-original.md"   # sha256 d3cdbe57...; the spec every earlier experiment started from
FLAGS = "--mode critique --focus requirements,architecture"

WRAP = """You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside {sb}. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory {sb}/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to {sb}/home. Files under {sb}/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

COMMAND: you cannot run slash commands. The file {sb}/command.md is the definition of the /sc:spec-panel command. Act as that command: apply its critique mode, its "Review Loop" section and its "Mandatory Output Artifacts" exactly as written, and every other section of it that applies. Read command.md in full first.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Run /sc:spec-panel @{spec} {flags} . Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}.
Write the full report to {d}/review/round1.md. Do not edit anything else. First read {d}/README.md (binding shared context; the files under {d}/inventory/ are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
"""


def stage_a(a):
    root = pathlib.Path(a.repo_root)
    out = pathlib.Path(a.out)
    models = a.models.split(",") if a.models else [m["id"] for m in COMBOS["models"] if m.get("stage_a")]
    manifest = []
    for m in models:
        for rep in range(1, a.reps + 1):
            run = f"A-{m.replace('.', '_')}-r{rep}"
            sb = (out / run).resolve()
            if sb.exists():
                continue
            ws = sb / "ws"
            (ws / D).mkdir(parents=True)
            shutil.copy(root / D / "README.md", ws / D / "README.md")
            shutil.copytree(root / D / "inventory", ws / D / "inventory")
            (ws / D / "specs").mkdir()
            shutil.copy(SPEC_ORIGINAL, ws / SPEC)
            (ws / D / "review").mkdir()
            (sb / "home/.claude/rules/prompts").mkdir(parents=True)
            shutil.copy(root / RULES_REL, sb / "home/.claude/rules/prompts/document_review_loop_prompts.md")
            shutil.copy(root / CMD_REL, sb / "command.md")
            (sb / "PROMPT.md").write_text(WRAP.format(sb=sb, spec=SPEC, flags=FLAGS, d=D))
            manifest.append({"run": run, "model": m, "rep": rep, "prompt": str(sb / "PROMPT.md"), "output": str(ws / D / "review/round1.md")})
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"wrote {len(manifest)} stage-A runs to {out}")


def panels(a):
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tiers = json.load(open(a.tiers)) if a.tiers else None
    if tiers is not None and a.t2b_models:
        tiers["aliases"]["tier2b"] = {"alias": "claude-gw-tier2b[1m]", "models": a.t2b_models.split(",")}
        (out / "eval-tiers.json").write_text(json.dumps(tiers, indent=2))
    for p in COMBOS["panels"]:
        obj = {"schema": "review-panel/1", "template_id": p["id"].lower()[:32], "version": "1.0.0", "description": p["why"],
               "distinct_across_slots": True, "apply_to": ["first"], "slots": p["slots"]}
        (out / f"{p['id']}.panel.json").write_text(json.dumps(obj, indent=2))
        if p.get("needs_t2b") and not a.t2b_models and not (tiers and tiers["aliases"].get("tier2b", {}).get("models")):
            print(f"note: {p['id']} needs --t2b-models before it can resolve on the gateway")
    print(f"wrote {len(COMBOS['panels'])} panel templates to {out}; validate each with: superclaude review panel validate FILE")


def schedule(a):
    ids = a.panels.split(",") if a.panels else [p["id"] for p in COMBOS["panels"]]
    rnd = random.Random(a.seed)
    rows = []
    for block in range(1, a.reps + 1):
        order = ids[:]
        rnd.shuffle(order)
        for pos, pid in enumerate(order):
            rows.append({"block": block, "pos": pos, "panel": pid, "run": f"{pid}-r{block}"})
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps({"seed": a.seed, "reps": a.reps, "panels": ids, "runs": rows}, indent=1))
    print(f"wrote {len(rows)} runs ({a.reps} blocks x {len(ids)} panels) to {a.out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stage-a"); s.add_argument("--out", required=True); s.add_argument("--repo-root", required=True)
    s.add_argument("--reps", type=int, default=COMBOS["stage_a"]["reports_per_model"]); s.add_argument("--models")
    s.set_defaults(fn=stage_a)
    s = sub.add_parser("panels"); s.add_argument("--out", required=True); s.add_argument("--t2b-models"); s.add_argument("--tiers")
    s.set_defaults(fn=panels)
    s = sub.add_parser("schedule"); s.add_argument("--out", required=True); s.add_argument("--reps", type=int, default=COMBOS["stage_c"]["runs_per_panel"])
    s.add_argument("--seed", type=int, required=True); s.add_argument("--panels"); s.set_defaults(fn=schedule)
    a = ap.parse_args(argv)
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
