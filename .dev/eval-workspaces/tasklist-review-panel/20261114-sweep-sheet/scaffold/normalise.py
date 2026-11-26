"""H2 normaliser (DESIGN 11.2 row H2, REQ-02): make a reviewer report fit the merge limits.

For each line of the findings-v1 block that parse_block reads (the last one), `anchor` and `anchor2` are cut to
their first 200 whitespace-flattened characters and `claim` to 300. A prefix of an exact quote is an exact quote,
so a cut anchor is still found by fnd.locate. A line already inside the limits is left byte for byte as written,
which makes the function idempotent. The result is validated with fnd.parse_block; every error it still reports
is kept under `unrepaired` and never dropped. Findings logic comes only from scaffold/fnd.py.
"""

from __future__ import annotations

import json
from pathlib import Path

from scaffold import fnd

LIMITS = {"anchor": 200, "anchor2": 200, "claim": 300}


def _cut_line(raw: str) -> tuple[str, list[str]]:
    """(line to write, names of the fields that were cut). Lines that are not finding objects come back unchanged."""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return raw, []
    if not isinstance(obj, dict) or "prior" in obj:
        return raw, []
    cut = []
    for name, limit in LIMITS.items():
        value = obj.get(name)
        if isinstance(value, str) and len(fnd.flat(value)) > limit:
            obj[name] = fnd.flat(value)[:limit].rstrip()
            cut.append(name)
    return (json.dumps(obj, ensure_ascii=False), cut) if cut else (raw, [])


def normalise_report(text: str) -> tuple[str, dict]:
    """(normalised report text, info) with info = {"ok", "changed": [{line, id, fields}], "unrepaired": [{line, msg, text}]}."""
    lines = text.splitlines(keepends=True)
    _, blocks = fnd._blocks_after(text, fnd._HEAD_FINDINGS, "findings-v1")
    changed = []
    if blocks:
        for lineno, raw in blocks[-1][1]:
            new, cut = _cut_line(raw)
            if cut:
                lines[lineno - 1] = new + lines[lineno - 1][len(raw) :]
                changed.append(
                    {"line": lineno, "id": json.loads(raw).get("id"), "fields": cut}
                )
    out = "".join(lines)
    parsed = fnd.parse_block(out)
    unrepaired = [
        {
            "line": e["line"],
            "msg": e["msg"],
            "text": lines[e["line"] - 1].strip()
            if 1 <= e["line"] <= len(lines)
            else "",
        }
        for e in parsed["errors"]
    ]
    return out, {"ok": parsed["ok"], "changed": changed, "unrepaired": unrepaired}


def normalise_file(src: Path, out_dir: Path, rid: str) -> dict:
    """Write out_dir/<rid>.md and record the result under `rid` in out_dir/h2.json. Returns that report's info."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out, info = normalise_report(Path(src).read_text())
    (out_dir / f"{rid}.md").write_text(out)
    h2_path = out_dir / "h2.json"
    h2 = json.loads(h2_path.read_text()) if h2_path.exists() else {"reports": {}}
    h2["reports"][rid] = {"ok": info["ok"], "changed": info["changed"]}
    h2["unrepaired"] = [u for u in h2.get("unrepaired", []) if u["rid"] != rid] + [
        {"rid": rid, **u} for u in info["unrepaired"]
    ]
    h2_path.write_text(json.dumps(h2, indent=2, sort_keys=True) + "\n")
    return info
