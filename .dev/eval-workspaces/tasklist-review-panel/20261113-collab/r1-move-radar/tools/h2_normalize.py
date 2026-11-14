"""H2 (R-02): truncate over-long anchors and claims in the last findings-v1 block, validate with the real parser.

Usage (from REPO): uv run python tools/h2_normalize.py <in.md> <out.md> <errors.json>
Writes out.md (only the block lines rewritten) and errors.json = {"ok", "errors": [{"line", "msg"}], "truncated",
"kept_lines", "dropped_lines"} (kept/dropped = block lines the merge parser keeps / loses).
Exit 0 always; the caller reads "ok".
"""

from __future__ import annotations

import json
import sys

from superclaude.cli.review import findings as fnd

LIMITS = {"anchor": 200, "anchor2": 200, "claim": 300}


def normalize(text: str) -> tuple[str, int]:
    _found, blocks = fnd._blocks_after(text, fnd._HEAD_FINDINGS, "findings-v1")
    if not blocks:
        return text, 0
    # _blocks_after numbers lines with str.splitlines(), so index with the same splitter (it also breaks on \r, \x0c,
    # U+2028 ...) and keep each line's own terminator. main() reads and writes the report raw (newline=""), as
    # merge_cmd._read does, so the original terminators reach this code and the parse matches the merge's.
    lines = text.splitlines(keepends=True)
    truncated = 0
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
            if isinstance(v, str) and len(fnd.flat(v)) > lim:
                obj[key] = fnd.flat(v)[:lim].rstrip()
                changed = True
                truncated += 1
        if changed:
            old = lines[lineno - 1]
            ending = old[len(old.splitlines()[0]):] if old.splitlines() else old
            # ASCII escapes: a rewritten line can never carry a raw line separator that splitlines would break on
            lines[lineno - 1] = json.dumps(obj) + ending
    return "".join(lines), truncated


def dropped_lines(text: str, parsed: dict) -> int:
    """Block lines the merge parser will not keep (not the number of parser errors).

    With the heading and a block: the non-blank lines of the last block that carry an error. Without the heading,
    or with no block after it, the parser keeps nothing, so every non-blank line of the last findings-v1 fence in the
    report is dropped. Block-level notices (several blocks, unclosed block) drop no line by themselves.
    """
    found, blocks = fnd._blocks_after(text, fnd._HEAD_FINDINGS, "findings-v1")
    if found and blocks:
        body = {ln for ln, raw in blocks[-1][1] if raw.strip()}
        return len({e["line"] for e in parsed["errors"] if e["line"] in body})
    _, anywhere = fnd._blocks_after("## Findings block\n" + text, fnd._HEAD_FINDINGS, "findings-v1")
    return sum(1 for _, raw in anywhere[-1][1] if raw.strip()) if anywhere else 0


def main(argv: list[str]) -> int:
    src, out, errs = argv
    try:
        with open(src, encoding="utf-8", newline="") as fh:  # raw, as merge_cmd._read: no line-ending conversion
            text = fh.read()
    except OSError as exc:
        json.dump({"ok": False, "errors": [{"line": 0, "msg": f"cannot read report: {exc}"}], "truncated": 0,
                   "kept_lines": 0, "dropped_lines": 0}, open(errs, "w"))
        open(out, "w").close()
        return 0
    new, n = normalize(text)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(new)
    parsed = fnd.parse_block(new)  # the same raw text the merge will read
    json.dump({"ok": parsed["ok"], "errors": parsed["errors"], "truncated": n, "kept_lines": len(parsed["findings"]) + len(parsed["priors"]),
               "dropped_lines": dropped_lines(new, parsed)}, open(errs, "w"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
