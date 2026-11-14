"""Digest builder: selection, router, deal, gap cards, n, rendering, validator (section 6)."""

from __future__ import annotations

import hashlib
import json
import random
import re
import shutil
import time
from pathlib import Path

from superclaude.cli.review import findings as F

from . import findings_io, paths, values

MSG_KEYS = ["v", "id", "run", "from", "to", "t", "kind", "move", "anchor"]
FORBIDDEN_HINT = {"claim", "verdict", "blocking", "severity", "category", "note"}


def load_findings(report_path) -> list[dict]:
    return findings_io.valid_findings(Path(report_path).read_text(encoding="utf-8"))


def anchor_class(anchor: str, category, routing) -> str | None:
    if category == "contradiction":
        return "contradiction"
    a = F.flat(anchor)
    for c in routing["classes"]:
        if re.search(c["regex"], a):
            return c["name"]
    return None


def route(anchor, category, style, routing) -> str | None:
    cls = anchor_class(anchor, category, routing)
    return None if cls is None else routing["move_by_style"][cls][style]


def qualifies(f, candidate, routing, style) -> tuple[bool, str]:
    if f.get("category") not in routing["select_categories"]:
        return False, "skipped_category"
    if re.search(routing["surface_regex"], f.get("claim", "")):
        return False, "skipped_surface"
    if not F.locate(candidate, f["anchor"]):
        return False, "skipped_anchor_missing"
    if route(f["anchor"], f.get("category"), style, routing) is None:
        return False, "skipped_no_route"
    return True, "selected"


def select(findings, candidate, routing, style, log=None) -> list[dict]:
    out, seen = [], set()
    for f in findings:
        ok, why = qualifies(f, candidate, routing, style)
        if log is not None:
            log.append({"id": f.get("id"), "reason": why})
        a = F.flat(f["anchor"])
        if ok and a not in seen:
            seen.add(a)
            out.append(f)
    return out


def deal(searcher_anchors, readers, deal_r) -> dict:
    """6.2: anchor i goes to reader (i + deal_r) mod 2."""
    out = {r: [] for r in readers}
    for i, a in enumerate(searcher_anchors):
        out[readers[(i + deal_r) % len(readers)]].append(a)
    return out


def interleave(queues: list[list]) -> list:
    out, i = [], 0
    while any(i < len(q) for q in queues):
        for q in queues:
            if i < len(q):
                out.append(q[i])
        i += 1
    return out


def gap_pool(candidate, all_anchors, routing, rng) -> list[str]:
    spans = []
    for a in all_anchors:
        spans.extend(F.locate(candidate, a))
    pool = []
    for i, line in enumerate(candidate.splitlines()):
        s = line.strip()
        if not s or s.startswith("#") or F._FENCE.match(line):
            continue
        fl = F.flat(line)
        if len(fl) < 12:
            continue
        fl = fl[:200]
        if any(a <= i < b for a, b in spans):
            continue
        if anchor_class(fl, None, routing) is None:
            continue
        pool.append(fl)
    rng.shuffle(pool)
    return pool


def fill_slots(n, real_queue, gap_pool_, rng, p_gap) -> list[dict]:
    real, gaps = list(real_queue), list(gap_pool_)
    slots = []
    for j in range(n):
        is_gap = rng.random() < p_gap
        pool = gaps if is_gap else real
        item = pool.pop(0) if pool else None
        slots.append({"j": j, "slot_type": "gap" if is_gap else "real", "item": item})
    return slots


def render_lines(slots, meta) -> list[str]:
    out = []
    for k, s in enumerate(slots, 1):
        msg = {
            "v": "panel-msg/1",
            "id": f"m-{meta['to']}-{k}",
            "run": meta["run"],
            "from": s["from"],
            "to": meta["to"],
            "t": meta["t_ms"],
            "kind": "challenge",
            "move": s["move"],
            "anchor": s["anchor"],
        }
        out.append(json.dumps(msg, ensure_ascii=False, separators=(",", ":")))
    return out


def validate_line(line, candidate_text, receiver, sources) -> tuple[bool, str]:
    if len(line.encode("utf-8")) > 600:
        return False, "too_long"
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        return False, "not_json"
    if not isinstance(o, dict):
        return False, "not_json"
    for k in o:
        if k not in MSG_KEYS:
            return False, f"forbidden_key:{k}"
    for k in MSG_KEYS:
        if k not in o:
            return False, f"missing_key:{k}"
    if o["v"] != "panel-msg/1" or o["kind"] != "challenge":
        return False, "bad_kind"
    if o["move"] not in {f"M{i}" for i in range(1, 11)}:
        return False, "bad_move"
    a = F.flat(o["anchor"]) if isinstance(o["anchor"], str) else ""
    if not 12 <= len(a) <= 200:
        return False, "anchor_length"
    if a not in F.flat(candidate_text):
        return False, "anchor_not_in_candidate"
    if o["from"] == o["to"] or o["from"] not in sources or o["to"] != receiver:
        return False, "self_or_unknown_source"
    return True, "ok"


def cap_digest(slots, meta, limit=1800) -> tuple[list, list]:
    """6.7: drop the last slot until the concatenated lines fit; returns (kept, dropped)."""
    kept, dropped = list(slots), []
    while kept and len("\n".join(render_lines(kept, meta)).encode()) > limit:
        dropped.append(kept.pop())
    return kept, dropped


def render_challenges(slots, catalogue) -> str:
    return "\n".join(
        f'C{k}. Place: "{s["anchor"]}"\n    Move: {catalogue[s["move"]]}'
        for k, s in enumerate(slots, 1)
    )


def render_prompt(slots, frame, catalogue, p) -> str:
    return (
        frame.replace("{CAND}", p["cand"])
        .replace("{SHA}", p["sha"])
        .replace("{SRC}", p["src"])
        .replace("{N}", str(len(slots)))
        .replace("{CHALLENGES}", render_challenges(slots, catalogue))
    )


def _seed(*parts) -> int:
    return int(hashlib.sha256("|".join(parts).encode()).hexdigest(), 16)


def roles(panel_cfg) -> dict:
    """rid -> {model, style, cap, sources}."""
    s = panel_cfg["searcher"]
    readers = panel_cfg["readers"]
    out = {s["rid"]: {**s, "sources": [r["rid"] for r in readers]}}
    for r in readers:
        out[r["rid"]] = {**r, "sources": [s["rid"]]}
    return out


def state_of(pkgdir: Path, rid: str) -> str | None:
    f = pkgdir / "reviews" / f"{rid}.p1.state"
    return f.read_text().strip() if f.exists() else None


def build(pkgdir, rid, t_launch, start_cost) -> tuple[int, dict]:
    """cli digest. Returns (exit code, printed object)."""
    pkgdir = Path(pkgdir)
    pj = paths.load_json(pkgdir / "pkg.json")
    panel = pj["panel"]
    pc = paths.cfg("panels.json")[panel]
    routing = paths.cfg("routing.json")
    catalogue = paths.cfg("catalogue.json")
    R = roles(pc)
    me = R[rid]
    candidate = Path(pj["cand_sb"]).read_text(encoding="utf-8")
    T0 = pj["T0"]
    n = values.compute_n(
        0.0,
        pj["B_f"],
        t_launch - T0,
        pc["box_cap_s"],
        me["cap"],
        start_cost,
        pj["turn_p90"][me["model"]],
    )
    n_base = n
    # owner-authorised time-cap exception: a measured n of 0 becomes the forced n (pj["tce"] is absent when off)
    n = values.tce_floor_n(
        n,
        pj.get("tce"),
        t_launch - T0,
        start_cost,
        pj["turn_p90"][me["model"]],
        me["cap"],
    )
    board = pkgdir / "board"
    board.mkdir(exist_ok=True)
    log = {
        "rid": rid,
        "t_launch": t_launch,
        "start_cost": start_cost,
        "n": n,
        "n_base": n_base,
        "n_forced": n != n_base,
        "selection": {},
        "rejected": [],
    }
    # source anchors
    sealed = {
        r: pkgdir / "reviews" / f"{r}.p1.md"
        for r in R
        if state_of(pkgdir, r) == "sealed"
    }
    per_src = {}
    for src in me["sources"]:
        if src not in sealed:
            per_src[src] = []
            continue
        sl = []
        per_src[src] = select(
            load_findings(sealed[src]), candidate, routing, me["style"], sl
        )
        log["selection"][src] = sl
    readers = [r["rid"] for r in pc["readers"]]
    deal_r = _seed(pj["run_id"], pj["pkg"], "deal") & 1
    log["deal_r"] = deal_r
    if me["style"] == "reading":
        dealt = deal(per_src[me["sources"][0]], readers, deal_r)
        real_queue = [(me["sources"][0], f) for f in dealt[rid]]
    else:
        real_queue = interleave(
            [[(src, f) for f in per_src[src]] for src in me["sources"]]
        )
        assert all(src != rid for src, _ in real_queue)
    seen, rq = set(), []
    for src, f in real_queue:
        a = F.flat(f["anchor"])
        if a not in seen:
            seen.add(a)
            rq.append((src, f))
    rng = random.Random(_seed(pj["run_id"], pj["pkg"], rid, "slots"))
    all_anchors = []
    for r, p in sealed.items():
        for f in load_findings(p):
            all_anchors.append(f["anchor"])
            if f.get("anchor2"):
                all_anchors.append(f["anchor2"])
    gp = gap_pool(candidate, all_anchors, routing, rng)
    raw = fill_slots(n, rq, gp, rng, routing["gap_probability"])
    slots = []
    for s in raw:
        if s["item"] is None:
            log.setdefault("slot_empty", []).append(
                {"j": s["j"], "slot_type": s["slot_type"]}
            )
            continue
        if s["slot_type"] == "real":
            src, f = s["item"]
            anchor = F.flat(f["anchor"])[:200]
            slots.append(
                {
                    "j": s["j"],
                    "slot_type": "real",
                    "from": src,
                    "anchor": anchor,
                    "move": route(anchor, f.get("category"), me["style"], routing),
                    "source_rid": src,
                    "source_finding_id": f["id"],
                }
            )
        else:
            anchor = s["item"]
            slots.append(
                {
                    "j": s["j"],
                    "slot_type": "gap",
                    "from": me["sources"][0],
                    "anchor": anchor,
                    "move": route(anchor, None, me["style"], routing),
                    "source_rid": me["sources"][0],
                    "source_finding_id": None,
                }
            )
    meta = {
        "to": rid,
        "run": f"{pj['run_id']}/{pj['pkg']}",
        "t_ms": int(time.time() * 1000),
    }
    kept = []
    for s in slots:
        line = render_lines([s], meta)[0]
        ok, why = validate_line(line, candidate, rid, me["sources"])
        if ok:
            kept.append(s)
        else:
            log["rejected"].append({"j": s["j"], "reason": why})
    kept, dropped = cap_digest(kept, meta)
    log["rejected"] += [{"j": s["j"], "reason": "digest_too_long"} for s in dropped]
    lines = render_lines(kept, meta)
    for s in kept:
        s["deal_r"] = deal_r
    # keep an earlier digest (fallback re-render)
    dj = board / f"{rid}.digest.jsonl"
    if dj.exists():
        shutil.copy2(dj, board / f"{rid}.digest.attempt1.jsonl")
        if (board / f"{rid}.digest.json").exists():
            shutil.copy2(
                board / f"{rid}.digest.json", board / f"{rid}.digest.attempt1.json"
            )
    dj.write_text("".join(x + "\n" for x in lines), encoding="utf-8")
    p = {"cand": pj["cand_sb"], "sha": pj["cand_sha256"], "src": pj["src_sb"]}
    prompt = render_prompt(kept, paths.cfg_text("phase2-frame.txt"), catalogue, p)
    (board / f"{rid}.prompt.txt").write_text(prompt, encoding="utf-8")
    p1copy = str(Path(pj["sb_pkg"]) / "p1" / pj["run_id"] / f"{rid}.p1.md")
    fb = (
        paths.cfg_text("fallback-frame.txt")
        .replace("{CAND}", p["cand"])
        .replace("{P1COPY}", p1copy)
        + prompt
    )
    (board / f"{rid}.fallback.prompt.txt").write_text(fb, encoding="utf-8")
    first = (
        paths.load_json(board / f"{rid}.digest.json")["n_planned"]
        if (board / f"{rid}.digest.json").exists()
        else n
    )
    out = {
        "rid": rid,
        "n": n,
        "n_planned": first,
        "n_launched": len(kept),
        "deal_r": deal_r,
        "slots": [
            {
                k: s[k]
                for k in (
                    "j",
                    "slot_type",
                    "move",
                    "source_rid",
                    "source_finding_id",
                    "anchor",
                    "deal_r",
                )
            }
            for s in kept
        ],
        "log": log,
    }
    paths.write_json(board / f"{rid}.digest.json", out)
    return (0 if kept else 5), {"n": n, "slots": [s["j"] for s in kept]}
