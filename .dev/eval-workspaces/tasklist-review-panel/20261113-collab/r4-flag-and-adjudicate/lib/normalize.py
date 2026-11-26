"""H2 normaliser (design 2.6 step 5): truncate anchor/anchor2/claim in the last findings-v1 block,
then validate with the real findings parser.

usage: normalize.py <raw.md> <final.md> <parse.json>
"""

from __future__ import annotations

import json
import sys

from superclaude.cli.review import findings as fd

LIMITS = {"anchor": 200, "anchor2": 200, "claim": 300}


def truncate_block(text: str) -> tuple[str, int]:
    """Cut over-long anchor/anchor2/claim values of the last findings-v1 block to a flattened prefix."""
    _found, blocks = fd._blocks_after(text, fd._HEAD_FINDINGS, "findings-v1")
    if not blocks:
        return text, 0
    lines = text.splitlines(keepends=True)  # same numbering as the parser's splitlines()
    n = 0
    for lineno, raw in blocks[-1][1]:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        changed = False
        for key, lim in LIMITS.items():
            v = obj.get(key)
            if isinstance(v, str) and len(fd.flat(v)) > lim:
                obj[key] = fd.flat(v)[:lim]
                changed = True
                n += 1
        if changed:
            # keep the line's leading indentation and its line ending
            old = lines[lineno - 1]
            body = old.splitlines()[0]
            lead = body[: len(body) - len(body.lstrip())]
            lines[lineno - 1] = lead + json.dumps(obj, ensure_ascii=False) + old[len(body):]
    return "".join(lines), n


def check(text: str) -> dict:
    res = fd.parse_block(text)
    return {"ok": bool(res["ok"]), "errors": res["errors"], "n_findings": len(res["findings"])}


def main(argv: list[str]) -> int:
    raw_p, final_p, parse_p = argv[1:4]
    with open(raw_p, encoding="utf-8", newline="") as fh:
        text = fh.read()
    out, n = truncate_block(text)
    with open(final_p, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    res = check(out)
    res["truncated"] = n
    with open(parse_p, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
