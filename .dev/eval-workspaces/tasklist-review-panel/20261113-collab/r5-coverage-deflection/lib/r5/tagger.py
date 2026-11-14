"""Peer/own tags to a sidecar file, never into a report (DESIGN 2.8; R-10, D7)."""
import json
import sys
from pathlib import Path

from superclaude.cli.review.findings import parse_block

from r5 import coverage as cov
from r5 import read_json, read_jsonl


def delivered_tasks(run_dir: Path, rid: str) -> set[str]:
    cards = {c.get("id"): c for c in read_jsonl(run_dir / "board" / "msgs" / "watcher.jsonl")}
    out = set()
    for d in read_jsonl(run_dir / "board" / "delivered" / f"{rid}.jsonl"):
        if d.get("status") == "delivered" and d.get("id") in cards:
            out |= set(cards[d["id"]].get("items") or [])
    return out


def tag(run_dir, candidate) -> dict:
    run_dir = Path(run_dir)
    info = read_json(run_dir / "run.json")
    cand = Path(candidate).read_text()
    index = cov.task_index(cand)
    res = {}
    for rid in info["receivers"] + info["scouts"]:
        rep = run_dir / "reviews" / f"{rid}.md"
        findings = parse_block(rep.read_text(errors="replace"))["findings"] if rep.exists() else []
        got = delivered_tasks(run_dir, rid) if rid in info["receivers"] else set()
        lines, acted = [], set()
        for f in findings:
            tasks = cov.tasks_of(f, cand, index)
            origin = "peer" if tasks & got else "own"
            acted |= tasks & got
            lines.append({"fid": f.get("id"), "origin": origin, "tasks": sorted(tasks)})
        p = run_dir / "tags" / f"{rid}.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(json.dumps(x) + "\n" for x in lines))
        res[rid] = {"lines": lines, "requests_acted": len(acted), "delivered_tasks": sorted(got)}
    return res


if __name__ == "__main__":
    print(json.dumps(tag(sys.argv[1], sys.argv[2])))
