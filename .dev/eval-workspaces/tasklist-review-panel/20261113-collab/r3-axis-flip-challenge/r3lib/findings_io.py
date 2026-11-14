"""H2 normaliser, phase-2 extraction and salvage, combiner (sections 5.4, 8.1, 8.2)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from superclaude.cli.review import findings as F

_ANY_BLOCK_FENCE = F._FENCE
_C_ID = re.compile(r"^C[0-9]+$")
_NO_FINDING = re.compile(r"no finding C(\d+)", re.I)
_SELF_REF = re.compile(r"(?i)\b(second pass|places?|challenge|move M?\d+|peer)\b")


class CombineError(Exception):
    pass


def normalise_finding(obj: dict) -> dict:
    o = dict(obj)
    for k in ("anchor", "anchor2"):
        if isinstance(o.get(k), str):
            o[k] = F.flat(o[k])[:200]
    if isinstance(o.get("claim"), str):
        o["claim"] = F.flat(o["claim"])[:300]
    return o


def _last_block(text: str):
    found, blocks = F._blocks_after(text, F._HEAD_FINDINGS, "findings-v1")
    return found, blocks


def normalise_text(text: str) -> tuple[str, dict]:
    """5.4 steps 1-4. Returns (normalised text, info); info['exit'] is 0, 3 or 4."""
    found, blocks = _last_block(text)
    info = {
        "block_present": bool(found and blocks),
        "lines_total": 0,
        "lines_valid": 0,
        "errors": [],
        "would_drop": 0,
        "block_errors": [],
    }
    if not found or not blocks:
        res = F.parse_block(text)
        info["errors"] = res["errors"]
        info["exit"] = 4
        return text, info
    lines = text.split("\n")
    changed = False
    body = blocks[-1][1]
    for lineno, raw in body:
        if not raw.strip():
            continue
        info["lines_total"] += 1
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        new = normalise_finding(obj)
        if new != obj:
            lines[lineno - 1] = json.dumps(new, ensure_ascii=False)
            changed = True
    out = "\n".join(lines) if changed else text
    res = F.parse_block(out)
    body_lines = {n for n, _ in body}
    info["errors"] = res["errors"]
    info["would_drop"] = sum(1 for e in res["errors"] if e["line"] in body_lines)
    info["block_errors"] = [e for e in res["errors"] if e["line"] not in body_lines]
    info["lines_valid"] = len(res["findings"])
    unclosed = not blocks[-1][2]
    info["exit"] = 3 if (info["would_drop"] or unclosed) else 0
    return out, info


def error_count(text: str) -> int:
    _, info = normalise_text(text)
    return 10**6 if info["exit"] == 4 else len(info["errors"])


def valid_findings(text: str) -> list[dict]:
    """Valid findings of a report after normalisation (5.4)."""
    out, _ = normalise_text(text)
    return F.parse_block(out)["findings"]


def check_line(obj: dict) -> tuple[bool, str]:
    line = json.dumps(normalise_finding(obj), ensure_ascii=False)
    res = F.parse_block("## Findings block\n```findings-v1\n" + line + "\n```\n")
    if res["findings"] and not res["errors"]:
        return True, ""
    return False, "; ".join(e["msg"] for e in res["errors"]) or "no finding parsed"


def _any_last_block_lines(text: str) -> list[str] | None:
    """Lines of the last ```findings-v1 fence anywhere in text (heading not required)."""
    lines = text.splitlines()
    last = None
    i = 0
    while i < len(lines):
        m = _ANY_BLOCK_FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        marker, label = m.group(1), m.group(2)
        j, body = i + 1, []
        while j < len(lines):
            c = _ANY_BLOCK_FENCE.match(lines[j])
            if (
                c
                and c.group(1)[0] == marker[0]
                and len(c.group(1)) >= len(marker)
                and not c.group(2)
            ):
                break
            body.append(lines[j])
            j += 1
        if label == "findings-v1":
            last = body
        i = j + 1
    return last


def read_stream(path) -> list[dict]:
    out = []
    p = Path(path)
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(e, dict):
            out.append(e)
    return out


def result_text(events: list[dict]) -> str | None:
    for e in events:
        if e.get("type") == "result":
            return e.get("result") or ""
    return None


def assistant_text(events: list[dict]) -> str:
    parts = []
    for e in events:
        if e.get("type") != "assistant":
            continue
        for c in (e.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "text":
                parts.append(c.get("text", ""))
    return "".join(parts)


def _extract_one(stream_path) -> tuple[dict, dict]:
    events = read_stream(stream_path)
    rt = result_text(events)
    log = {"salvaged": False, "dropped": [], "no_finding": set()}
    cands: list[str] = []
    if rt is not None:
        cands = _any_last_block_lines(rt) or []
        src = rt
    else:
        src = assistant_text(events)
        cands = [ln.strip() for ln in src.splitlines()]
        log["salvaged"] = True
    log["no_finding"] = {int(m.group(1)) for m in _NO_FINDING.finditer(src)}
    by_id: dict[str, dict] = {}
    for raw in cands:
        raw = raw.strip()
        if not (raw.startswith("{") and raw.endswith("}")):
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if (
            not isinstance(obj, dict)
            or not isinstance(obj.get("id"), str)
            or not _C_ID.match(obj["id"])
        ):
            continue
        by_id[obj["id"]] = obj  # last complete occurrence wins
    valid: dict[str, dict] = {}
    for cid, obj in by_id.items():
        ok, msg = check_line(obj)
        if ok:
            valid[cid] = normalise_finding(obj)
        else:
            log["dropped"].append({"id": cid, "msg": msg})
    return valid, log


def extract_p2_lines(stream_path, reask_path=None) -> tuple[list[dict], dict]:
    """8.1 steps 1-5. Returns (valid normalised lines in C order, log)."""
    valid, log = _extract_one(stream_path)
    salvaged = len(valid) if log["salvaged"] else 0
    dropped = list(log["dropped"])
    answered = set(log["no_finding"])
    if reask_path and Path(reask_path).exists():
        rvalid, rlog = _extract_one(reask_path)
        for cid, obj in rvalid.items():
            valid[cid] = obj
        fixed = set(rvalid)
        dropped = [d for d in dropped if d["id"] not in fixed] + [
            d for d in rlog["dropped"] if d["id"] not in valid
        ]
        answered |= rlog["no_finding"]
    order = sorted(valid, key=lambda c: int(c[1:]))
    lines = [valid[c] for c in order]
    return lines, {
        "p2_lines_valid": len(lines),
        "p2_lines_dropped": len(dropped),
        "p2_drop_msgs": dropped,
        "p2_lines_salvaged": salvaged,
        "answered": sorted(answered | {int(c[1:]) for c in valid}),
    }


def _strip_origin(o: dict) -> dict:
    return {k: v for k, v in o.items() if k != "origin"}


def combine(p1_text: str, p2_lines: list[dict]) -> tuple[str, dict]:
    """8.2. p1_text is the sealed raw phase-1 report."""
    norm, _ = normalise_text(p1_text)
    p1 = F.parse_block(norm)["findings"]
    p1_ids = {f["id"] for f in p1}
    p1_keys = {(F.flat(f["anchor"]), F.flat(f["claim"])) for f in p1}
    log = {
        "p1_lines": len(p1),
        "p2_dupe_dropped": 0,
        "p2x_renames": 0,
        "p2_self_reference": 0,
    }
    kept = []
    for ln in p2_lines:
        if (F.flat(ln.get("anchor", "")), F.flat(ln.get("claim", ""))) in p1_keys:
            log["p2_dupe_dropped"] += 1
            continue
        kept.append(ln)
    out_lines = []
    for f in p1:
        o = dict(f)
        o["origin"] = "own"
        out_lines.append(o)
    for i, ln in enumerate(kept, 1):
        o = dict(ln)
        nid = f"P2-F{i}"
        if nid in p1_ids:
            nid = f"P2X-F{i}"
            log["p2x_renames"] += 1
        o["id"] = nid
        o["origin"] = "peer"
        if _SELF_REF.search(o.get("claim", "")):
            log["p2_self_reference"] += 1
        out_lines.append(o)
    log["p2_lines_combined"] = len(kept)
    # replace the findings section: heading .. end of the last findings-v1 block
    m = F._HEAD_FINDINGS.search(p1_text)
    if not m:
        raise CombineError("E_COMBINE: phase-1 report has no findings heading")
    _, blocks = _last_block(p1_text)
    if not blocks:
        raise CombineError("E_COMBINE: phase-1 report has no findings-v1 block")
    lines = p1_text.split("\n")
    head_line = p1_text.count("\n", 0, m.start())
    last_start, last_body, closed = blocks[-1]
    end_idx = (
        (last_body[-1][0] + 1)
        if (closed and last_body)
        else (last_start + 1 if closed else len(lines))
    )
    # end_idx: 1-based number of the closing fence line == 0-based index after it
    if closed and not last_body:
        end_idx = last_start + 1
    before = lines[:head_line]
    after = lines[end_idx:] if closed else []
    block = (
        [lines[head_line], "```findings-v1"]
        + [json.dumps(o, ensure_ascii=False) for o in out_lines]
        + ["```"]
    )
    text = "\n".join(before + block + after)
    if not text.endswith("\n"):
        text += "\n"
    # self-check
    res = F.parse_block(text)
    found, blks = _last_block(text)
    if not res["ok"] or len(blks) != 1 or len(res["findings"]) != len(p1) + len(kept):
        raise CombineError(f"E_COMBINE: self-check failed: {res['errors'][:3]}")
    for a, b in zip(res["findings"][: len(p1)], p1):
        if _strip_origin(a) != b:
            raise CombineError(f"E_COMBINE: phase-1 line {b.get('id')} changed")
    return text, log
