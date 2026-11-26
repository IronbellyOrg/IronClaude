"""H2 (R-02): truncate anchor/anchor2 to 200 and claim to 300 flattened characters in the last findings-v1 block,
then validate the block with the real findings parser.

uv run --no-project python -I py/h2_normalize.py --report <rid>.md --out <rid>.norm.md --json <rid>.h2.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import findings, last_block_lines, replace_lines  # noqa: E402

LIMITS = {"anchor": 200, "anchor2": 200, "claim": 300}


def normalize(text: str) -> tuple[str, dict]:
    f = findings()
    trunc = {k: 0 for k in LIMITS}
    repl = {}
    for n, raw in last_block_lines(text):
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict) or "prior" in obj:
            continue
        changed = False
        for key, lim in LIMITS.items():
            v = obj.get(key)
            if isinstance(v, str) and len(f.flat(v)) > lim:
                obj[key] = f.flat(v)[:lim].rstrip()
                trunc[key] += 1
                changed = True
        if changed:
            repl[n] = json.dumps(obj, ensure_ascii=False)
    norm = replace_lines(text, repl) if repl else text
    res = f.parse_block(norm)
    structural = any(e["line"] == 0 or "not closed" in e["msg"] for e in res["errors"])
    return norm, {
        "truncated": trunc,
        "errors": res["errors"],
        "block_ok": res["ok"],
        "block_found": not structural,
        "findings": len(res["findings"]),
        "needs_reask": not res["ok"],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--json", required=True)
    a = ap.parse_args(argv)
    text = Path(a.report).read_text() if Path(a.report).exists() else ""
    norm, info = normalize(text)
    Path(a.out).write_text(norm)
    Path(a.json).write_text(json.dumps(info) + "\n")
    print(json.dumps({k: info[k] for k in ("block_ok", "needs_reask", "findings")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
