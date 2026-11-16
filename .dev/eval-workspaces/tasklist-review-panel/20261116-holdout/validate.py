"""Counts-only validation of hold-out ground truth (prints no defect text)."""
import json, re, subprocess, sys
from pathlib import Path
REPO = Path("/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel")
flat = lambda s: re.sub(r"\s+", " ", s).strip()
for d in map(Path, sys.argv[1:]):
    gt = json.load(open(d / "ground-truth.json")); pk = json.load(open(d / "package.json"))
    cand = flat((d / "candidate.md").read_text()); items = gt["items"]
    if not items:
        print(d.name, "items=0"); continue
    ok = sum(flat(i["plan_quote"]) in cand for i in items)
    ln = sum(40 <= len(i["plan_quote"]) <= 200 for i in items)
    ids = [i["id"] for i in items] == [f"GT{k+1}" for k in range(len(items))]
    bt = subprocess.run(["git", "-C", str(REPO), "cat-file", "-t", pk["base"]], capture_output=True, text=True).stdout.strip()
    same = (REPO / pk["candidate"]).read_bytes() == (d / "candidate.md").read_bytes()
    src = (REPO / pk["source"]).read_bytes() == (d / "source.md").read_bytes()
    keys = all(set(i) >= {"id", "class", "blocking_in_implement", "description", "plan_quote"} for i in items)
    print(f"{d.name}: items={len(items)} blocking={sum(bool(i['blocking_in_implement']) for i in items)} quotes_found={ok}/{len(items)} len_ok={ln}/{len(items)} ids_ok={ids} base_type={bt} cand_same={same} src_same={src} keys_ok={keys} masked={len(pk['masked_paths'])}")
