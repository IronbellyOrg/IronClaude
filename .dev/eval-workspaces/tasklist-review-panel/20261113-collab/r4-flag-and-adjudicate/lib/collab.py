"""Per-package metrics after the reviewers exit (design 2.8): slots, conversion, peer tags,
Jaccard figures and collab.json. The 12-character overlap test lives only here.

usage: collab.py <pkgdir>
"""

from __future__ import annotations

import difflib
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys

from superclaude.cli.review import findings as fd

LIB = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LIB)
import values  # noqa: E402

CARD_JQ = os.path.join(LIB, "card.jq")
NULL_FIELDS = ("resume_fallback", "phase2_s", "phase2_timeout", "p2_lines_salvaged", "n_planned", "n_launched", "slot_type", "echo_rate")
_TASK = re.compile(r"^## Task (\d+):")


def overlap12(a: str | None, b: str | None) -> bool:
    """True when the flattened strings share a common substring of at least 12 characters."""
    if not a or not b:
        return False
    a, b = fd.flat(a), fd.flat(b)
    m = difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b))
    return m.size >= 12


def task_of(cand: str, anchor: str | None) -> str | None:
    """The Task ('T<n>') whose '## Task n:' heading is the last one above the anchor's first line."""
    if not anchor:
        return None
    spans = fd.locate(cand, anchor)
    if not spans:
        return None
    lines = cand.splitlines()
    for i in range(min(spans[0][0], len(lines) - 1), -1, -1):
        m = _TASK.match(lines[i])
        if m:
            return "T" + m.group(1)
        if re.match(r"^#{1,2}\s", lines[i]):
            return None
    return None


def form_of(i: int, c: int) -> str:
    return "challenge" if (i + i // 2 + c) % 2 == 0 else "finding"


def recipient_of(i: int, r: int, peers: list[str]) -> str:
    return peers[(i + r) % 2]


def _jac(a: set, b: set) -> float | None:
    if not a and not b:
        return None
    return len(a & b) / len(a | b)


def own_line_jaccard(task_sets: list[set]) -> float | None:
    vals = [j for x, y in itertools.combinations(task_sets, 2) if (j := _jac(x, y)) is not None]
    return sum(vals) / len(vals) if vals else None


def valid_cards(path: str, flagger: str) -> list[str]:
    """Board lines that pass the 600-byte check and lib/card.jq, in append order."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as fh:
        raw = [ln.rstrip("\n") for ln in fh]
    short = [ln for ln in raw if len(ln.encode()) <= 600]
    if not short:
        return []
    out = subprocess.run(["jq", "-R", "-r", "--arg", "flagger", flagger, "-f", CARD_JQ], input="\n".join(short) + "\n",
                         capture_output=True, text=True).stdout
    ok = set(out.splitlines())
    return [ln for ln in short if ln in ok]


def sha(line: str) -> str:
    return hashlib.sha256(line.encode()).hexdigest()


def _jsonl(path: str) -> list[dict]:
    out = []
    try:
        with open(path, encoding="utf-8") as fh:
            for ln in fh:
                try:
                    out.append(json.loads(ln))
                except json.JSONDecodeError:
                    pass
    except OSError:
        pass
    return out


def _read(path: str, default=""):
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            return fh.read()
    except OSError:
        return default


def _load(path: str, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def p95(xs: list[float]) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    return s[max(0, -(-95 * len(s) // 100) - 1)]


def compute(pkgdir: str) -> dict:
    panel = _load(os.path.join(pkgdir, "panel.json"))
    cand = _read(panel["cand"])
    rids = [r["rid"] for r in panel["reviewers"]]
    flagger, peers = panel["flagger"], panel["peers"]
    board = os.path.join(pkgdir, "board")
    has_board = os.path.isdir(board)
    metrics = {rid: _jsonl(os.path.join(board, "metrics", rid + ".jsonl")) for rid in rids}
    meta = {rid: _load(os.path.join(pkgdir, "reviews", rid + ".meta.json"), {}) for rid in rids}
    lines = {}
    for rid in rids:
        res = fd.parse_block(_read(os.path.join(pkgdir, "reviews", rid + ".final.md")))
        lines[rid] = res["findings"]

    # delivered cards per reviewer: "<id> <ms> <form>"
    delivered: dict[str, dict[str, tuple[int, str]]] = {}
    for rid in rids:
        d = {}
        for ln in _read(os.path.join(board, "state", rid + ".delivered")).splitlines():
            parts = ln.split()
            if len(parts) == 3:
                d[parts[0]] = (int(parts[1]), parts[2])
        delivered[rid] = d

    accepted = {e.get("sha256") for e in metrics.get(flagger, []) if e.get("ev") == "post_accepted"}
    cards = [json.loads(ln) for ln in valid_cards(os.path.join(board, "msgs", flagger + ".jsonl"), flagger) if sha(ln) in accepted]
    form_mismatch = 0
    slots = []
    for card in cards:
        i = int(card["id"][1:])
        to = card["to"]
        form = form_of(i, panel["c"])
        dv = delivered.get(to, {}).get(card["id"])
        if dv and dv[1] != form:
            form_mismatch += 1
        if dv:
            status = "delivered"
        elif not panel.get("deliver", 1):
            status = "held"
        elif os.path.exists(os.path.join(board, "state", to + ".nosnap")):
            status = "no_snapshot"
        else:
            status = "late"
        conv = [f["id"] for f in lines.get(to, []) if dv and (overlap12(f.get("anchor"), card["anchor"]) or overlap12(f.get("anchor2"), card["anchor"]))]
        slots.append({
            "id": card["id"], "i": i, "recipient": to, "card_form": form, "deal_r": panel["r"], "deal_c": panel["c"],
            "slot_type": None, "move": card["move"], "anchor": card["anchor"], "card_task": task_of(cand, card["anchor"]),
            "t_posted": card["t"], "t_delivered": dv[0] if dv else None, "status": status,
            "converted": bool(conv), "converted_fids": conv,
            "passed_line": f"card {card['id']}: passed" in _read(os.path.join(pkgdir, "reviews", to + ".final.md")),
        })

    # peer tags (deviation D-1: sidecar)
    tags = {}
    for rid in rids:
        dv_anchors = [s["anchor"] for s in slots if s["recipient"] == rid and s["status"] == "delivered"]
        t = {}
        for f in lines[rid]:
            peer = rid != flagger and any(overlap12(f.get("anchor"), a) or overlap12(f.get("anchor2"), a) for a in dv_anchors)
            t[f["id"]] = "peer" if peer else "own"
        tags[rid] = t
    os.makedirs(os.path.join(pkgdir, "tags"), exist_ok=True)
    for rid, t in tags.items():
        with open(os.path.join(pkgdir, "tags", rid + ".json"), "w") as fh:
            json.dump(t, fh, indent=1)

    own_sets = [{x for f in lines[rid] if tags[rid][f["id"]] == "own" and (x := task_of(cand, f.get("anchor")))} for rid in rids]
    all_sets = [{x for f in lines[rid] if (x := task_of(cand, f.get("anchor")))} for rid in rids]
    flag_lines = lines.get(flagger, [])
    flag_anchors = {fd.flat(a) for f in flag_lines for a in (f.get("anchor"), f.get("anchor2")) if a}
    n_deliv = sum(1 for s in slots if s["status"] == "delivered")
    n_conv = sum(1 for s in slots if s["status"] == "delivered" and s["converted"])
    led = _load(os.path.join(pkgdir, "ledger.json"))
    elapsed = values.elapsed_s(pkgdir)
    cp = values.cp_rids({}, {"cp_role": panel["cp_role"], "flagger": {"rid": flagger}, "adjudicators": [{"rid": p} for p in peers]})
    rej = [e for e in metrics.get(flagger, []) if e.get("ev") == "post_rejected"]

    per = {}
    for rid in rids:
        m, mt = metrics.get(rid, []), meta.get(rid, {})
        snap_sha = _read(os.path.join(board, "snap", rid + ".sha256")).split()
        snap_file = os.path.join(board, "snap", rid + ".jsonl")
        seal_ok = None
        if snap_sha:
            try:
                with open(snap_file, "rb") as fh:
                    seal_ok = hashlib.sha256(fh.read()).hexdigest() == snap_sha[0]
            except OSError:
                seal_ok = False
        fin = _read(os.path.join(board, "state", rid + ".finished")).strip()
        calls = _read(os.path.join(board, "state", rid + ".calls")).strip()
        per[rid] = {
            "role": "flagger" if rid == flagger else "adjudicator",
            "msgs_sent": len(_read(os.path.join(board, "msgs", rid + ".jsonl")).splitlines()),
            "msgs_received": len(delivered[rid]),
            "first_delivery_t": min((v[0] for v in delivered[rid].values()), default=None),
            "seal_t": next((e.get("t") for e in m if e.get("ev") == "seal"), None),
            "seal_sha256": snap_sha[0] if snap_sha else None,
            "seal_sha_ok": seal_ok,
            "stop_blocks": 0,
            "hook_calls": int(calls) if calls.isdigit() else (None if not has_board else 0),
            "hook_error": sum(1 for e in m if e.get("ev") == "hook_error") + (form_mismatch if rid == flagger else 0),
            "hook_ms_p95": p95([e["ms"] for e in m if e.get("ev") == "hook_ms" and isinstance(e.get("ms"), (int, float))]),
            "reask_s": mt.get("reask_s"),
            "attempts": mt.get("attempts"),
            "retry_s": mt.get("retry_s"),
            "retry_isolated": mt.get("retry_isolated"),
            "hang_kill": mt.get("hang_kill"),
            "snapshot_missing": os.path.exists(os.path.join(board, "state", rid + ".nosnap")) or any(e.get("ev") == "snapshot_missing" for e in m),
            "late": sum(1 for s in slots if s["recipient"] == rid and s["status"] == "late"),
            "over_cap": sum(1 for e in rej if e.get("reason") == "over_cap") if rid == flagger else 0,
            "too_early": sum(1 for e in rej if e.get("reason") == "too_early") if rid == flagger else 0,
            "after_finish": sum(1 for e in rej if e.get("reason") == "after_finish") if rid == flagger else 0,
            "finish_signal_t": int(fin) if fin.isdigit() else None,
            "t_end_ms": mt.get("t_end_ms"),
        }
    b = panel.get("B_A1")
    out = {
        "schema": "r4-collab/1",
        "arm": panel["arm"], "panel": panel["panel"], "k": panel["k"], "k0_isolated": panel["k0_isolated"],
        "deal_r": panel["r"], "deal_c": panel["c"], "panel_finish_at": panel["finish_ms"],
        "finish_would_fire": any((per[r]["t_end_ms"] or 0) > panel["finish_ms"] for r in cp),
        "elapsed_s": elapsed, "baseline_elapsed_s": b,
        "overhead_pct": None if elapsed is None or not b else round(100 * (elapsed / b - 1), 2),
        # time-cap exception columns (OVERRIDE.md); time_cap_exception is false and k_forced false on a cap-obeying package
        "time_cap_exception": bool(panel.get("time_cap_exception")), "k_measured": panel.get("k_measured", panel["k"]),
        "k_forced": bool(panel.get("k_forced")), "hang_s": panel.get("hang_s"), "finish_offset_s": panel.get("finish_offset_s"),
        "elapsed_over_baseline": None if elapsed is None or not b else round(elapsed / b, 4),
        "delivered_per_reviewer": {rid: per[rid]["msgs_received"] for rid in rids},
        "own_line_jaccard": own_line_jaccard(own_sets), "pairwise_task_jaccard": own_line_jaccard(all_sets),
        "ledger_rows": len(led["rows"]) if isinstance(led, dict) and "rows" in led else None,
        "cards_sent": len(cards), "cards_rejected": len(rej), "cards_delivered": n_deliv,
        "flag_finding_overlap": (sum(1 for c in cards if fd.flat(c["anchor"]) in flag_anchors) / len(cards)) if cards else None,
        "adjudication_agreement": n_conv / n_deliv if n_deliv else None,
        "slo_breach": any(per[r]["hang_kill"] for r in rids),
        "values_sha256": panel.get("values_sha256"),
        "reviewers": per,
        "slots": slots,
    }
    for k in NULL_FIELDS:
        out[k] = None
    for rid in rids:
        for k in ("resume_fallback", "phase2_s", "phase2_timeout", "p2_lines_salvaged", "n_planned", "n_launched"):
            per[rid][k] = None
    return out


def main(argv: list[str]) -> int:
    pkgdir = argv[1]
    out = compute(pkgdir)
    with open(os.path.join(pkgdir, "slots.json"), "w") as fh:
        json.dump(out["slots"], fh, indent=1)
    with open(os.path.join(pkgdir, "collab.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
