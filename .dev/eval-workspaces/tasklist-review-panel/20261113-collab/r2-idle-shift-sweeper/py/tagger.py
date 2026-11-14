"""Origin tags (R-10, DESIGN 2.6): add "origin":"own"|"peer" to every findings line of the last findings-v1 block.

peer: the line's flattened anchor/anchor2 shares a common substring of >= 12 characters with the flattened anchor of a
fact delivered to this reviewer, or a refs entry / path-shaped claim token names a delivered item path (line suffix
ignored). own otherwise; always own for non-receivers, for an isolated attempt-2 report, and when no board exists.

tagger.py --report <rid>.norm.md [--board-dir B] --rid <rid> --out <rid>.final.md [--nonreceiver] [--isolated]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import findings, last_block_lines, replace_lines  # noqa: E402

PATH_TOKEN = re.compile(r"[A-Za-z0-9_.@+/-]+")


def norm_path(p: str) -> str:
    p = p.strip("`'\"()[],;")
    p = re.sub(r":\d+(-\d+)?$", "", p)
    return p[2:] if p.startswith("./") else p


def delivered_facts(board: Path | None, rid: str) -> list[dict]:
    if board is None:
        return []
    ids_f = board / "state" / f"{rid}.delivered"
    ids = [x for x in ids_f.read_text().split()] if ids_f.exists() else []
    out = []
    bf = board / "msgs" / "board.jsonl"
    if bf.exists():
        for line in bf.read_text().splitlines():
            try:
                f = json.loads(line)
            except json.JSONDecodeError:
                continue
            if f.get("id") in ids:
                out.append(f)
    return out


def overlap12(a: str, b: str) -> bool:
    m = difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b))
    return m.size >= 12


def tag_line(obj: dict, facts: list[dict]) -> tuple[str, list[dict]]:
    fl = findings().flat
    reasons = []
    anchors = [fl(obj[k]) for k in ("anchor", "anchor2") if isinstance(obj.get(k), str)]
    cited = {norm_path(r) for r in obj.get("refs", []) if isinstance(r, str)}
    if isinstance(obj.get("claim"), str):
        cited |= {norm_path(t) for t in PATH_TOKEN.findall(obj["claim"]) if "." in t or "/" in t}
    for f in facts:
        fa = fl(f.get("anchor") or "")
        if fa and any(overlap12(a, fa) for a in anchors):
            reasons.append({"fact": f["id"], "why": "anchor"})
            continue
        items = {norm_path(i) for i in f.get("items", [])}
        hit = sorted(items & cited)
        if hit:
            reasons.append({"fact": f["id"], "why": "path", "paths": hit})
    return ("peer" if reasons else "own"), reasons


def tag_report(text: str, facts: list[dict], force_own: bool) -> tuple[str, list[dict]]:
    repl, tags = {}, []
    for n, raw in last_block_lines(text):
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict) or "prior" in obj:
            continue
        origin, reasons = ("own", []) if force_own else tag_line(obj, facts)
        obj["origin"] = origin
        repl[n] = json.dumps(obj, ensure_ascii=False)
        tags.append({"line": n, "id": obj.get("id"), "origin": origin, "reasons": reasons,
                     "anchor": obj.get("anchor"), "refs": obj.get("refs", []), "claim": obj.get("claim")})
    return (replace_lines(text, repl) if repl else text), tags


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--board-dir")
    ap.add_argument("--rid", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--nonreceiver", action="store_true")
    ap.add_argument("--isolated", action="store_true")
    a = ap.parse_args(argv)
    rp = Path(a.report)
    text = rp.read_text() if rp.exists() else ""
    board = Path(a.board_dir) if a.board_dir else None
    facts = delivered_facts(board, a.rid)
    force_own = a.nonreceiver or a.isolated or board is None
    out, tags = tag_report(text, facts, force_own)
    Path(a.out).write_text(out)
    Path(a.out).with_name(f"{a.rid}.tags.json").write_text(json.dumps(
        {"rid": a.rid, "isolated": a.isolated, "nonreceiver": a.nonreceiver,
         "delivered": [f["id"] for f in facts], "lines": tags}, ensure_ascii=False) + "\n")
    print(json.dumps({"peer": sum(t["origin"] == "peer" for t in tags), "own": sum(t["origin"] == "own" for t in tags)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
