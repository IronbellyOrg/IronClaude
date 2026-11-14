"""collab.json assembly (DESIGN 2.8; R-23). Every arm writes the full key set; fields that do not apply are null."""
import itertools
import sys
from pathlib import Path

from superclaude.cli.review.findings import parse_block

from r5 import coverage as cov
from r5 import read_json, read_jsonl, sb, write_json

NOT_F6 = ("resume_fallback", "phase2_s", "n_planned", "n_launched", "phase2_timeout", "p2_lines_salvaged",
          "slot_type", "card_form", "deal_c", "echo_rate")
F6_ONLY_PANEL = ("cards", "requests_posted", "requests_delivered", "requests_acted")
F6_ONLY_REVIEWER = ("msgs_received", "first_delivery_t", "seal_t", "hook_calls", "hook_error", "hook_ms_p95",
                    "finish_signal_t", "snapshot_missing", "late")


def jaccard_mean(sets: list[set]) -> float | None:
    vals = [len(a & b) / len(a | b) for a, b in itertools.combinations(sets, 2) if a | b]
    return sum(vals) / len(vals) if vals else None


def p95(xs: list) -> float | None:
    if not xs:
        return None
    v = sorted(xs)
    return v[min(len(v) - 1, int(0.95 * len(v) + 0.999999) - 1)]


def build(run_dir) -> dict:
    d = Path(run_dir)
    info = read_json(d / "run.json")
    rev = d / "reviews"
    board = d / "board"
    has_board = board.is_dir()
    pkg = info["pkg"]
    cand_p = sb() / "cand" / pkg / "candidate.md"
    cand = cand_p.read_text() if cand_p.exists() else ""
    index = cov.task_index(cand)
    pattern = cov.surface_pattern()
    rids = info["receivers"] + info["scouts"]
    t0, fin, B = info["T0"], info["finish_ms"], info["B_f_s"]

    cards_all = read_jsonl(board / "msgs" / "watcher.jsonl") if has_board else []
    reviewers, ends, own_sets, all_sets, anchored, scout_cov = {}, [], {}, {}, {}, set()
    hang_any = False
    for rid in rids:
        metas = [read_json(p) for p in sorted(rev.glob(f"{rid}.attempt*.meta.json"))]
        metas = [m for m in metas if m]
        tm = read_json(rev / f"{rid}.timing.json") or {}
        t_end = tm.get("t_end_ms") or max((m.get("t_end_ms", 0) for m in metas), default=None)
        if t_end:
            ends.append(t_end)
        hang = any(m.get("hang_kill") for m in metas)
        hang_any |= hang
        r = {"attempts": len(metas), "retry_s": sum(m.get("wall_s", 0) for m in metas if m.get("attempt", 1) > 1),
             "retry_isolated": any(m.get("attempt", 1) > 1 and not m.get("settings") for m in metas),
             "reask_s": tm.get("reask_s"), "hang_kill": hang, "t_end_ms": t_end, "role": "receiver" if rid in info["receivers"] else "scout"}
        if has_board and rid in info["receivers"]:
            mets = read_jsonl(board / "metrics" / f"{rid}.jsonl")
            dels = read_jsonl(board / "delivered" / f"{rid}.jsonl")
            delivered = [x for x in dels if x.get("status") == "delivered"]
            seal = board / "snap" / f"{rid}.t"
            fs = [m["t"] for m in mets if m.get("event") == "finish_signal_t"]
            r.update(msgs_received=len(delivered), first_delivery_t=min((x["t"] for x in delivered), default=None),
                     seal_t=int(seal.read_text().strip()) if seal.exists() else None,
                     hook_calls=sum(1 for m in mets if m.get("event") == "call"),
                     hook_error=sum(1 for m in mets if m.get("event") == "hook_error"),
                     hook_ms_p95=p95([m["ms"] for m in mets if m.get("event") == "call"]),
                     finish_signal_t=fs[0] if fs else None,
                     snapshot_missing=int(any(m.get("event") == "snapshot_missing" for m in mets)), late=0)
        else:
            r.update({k: None for k in F6_ONLY_REVIEWER})
        reviewers[rid] = r
        tags = read_jsonl(d / "tags" / f"{rid}.jsonl")
        own_sets[rid] = set().union(*[set(t["tasks"]) for t in tags if t["origin"] == "own"]) if tags else set()
        all_sets[rid] = set().union(*[set(t["tasks"]) for t in tags]) if tags else set()
        anchored[rid] = all_sets[rid]
        if rid in info["scouts"]:
            p = rev / f"{rid}.md"
            if p.exists():
                scout_cov |= cov.covered(parse_block(p.read_text(errors="replace"))["findings"], cand, index, pattern)

    elapsed = (max(ends) - t0) / 1000 if ends else None
    recv_anch = set().union(*[anchored[r] for r in info["receivers"]]) if info["receivers"] else set()
    ledger = read_json(d / "ledger.json")
    tcx = bool(info.get("time_cap_exception"))  # owner-authorised exception, stamped in run.json at run time
    cap_s = info["time_cap_s"] if tcx else 1.35 * B + info.get("slack_s", 0)  # slack recorded in run.json at run time
    over = elapsed is not None and elapsed > cap_s
    c = {k: None for k in NOT_F6}
    c.update(time_cap_exception=tcx, B_A1_s=B, time_cap_s=cap_s, k_measured=info.get("k_measured"), k_forced=bool(info.get("k_forced")),
             elapsed_over_baseline=(elapsed / B) if elapsed is not None and B else None)
    c.update(stop_blocks=0, msgs_sent=0, over_cap=0, arm=info["arm"], k=info["k"], deal_r=info["deal_r"],
             panel_finish_at=fin, elapsed_s=elapsed, baseline_elapsed_s=B,
             overhead_pct=(100 * (elapsed / B - 1)) if elapsed is not None and B else None,
             finish_would_fire=any((reviewers[r]["t_end_ms"] or 0) > fin for r in info["receivers"]),
             own_line_jaccard=jaccard_mean([own_sets[r] for r in rids]),
             pairwise_task_jaccard=jaccard_mean([all_sets[r] for r in rids]),
             ledger_rows=len(ledger["rows"]) if ledger and "rows" in ledger else None,
             values_sha256=info.get("values_sha256"),
             scout_covered_tasks=sorted(scout_cov), receiver_anchored_tasks=sorted(recv_anch),
             deflection_overlap=(len(recv_anch & scout_cov) / len(recv_anch)) if recv_anch else 0.0,
             union_anchored_tasks=len(set().union(*anchored.values())) if anchored else 0,
             k0_isolated=info.get("k0_isolated", False),
             slo="SLO_BREACH" if hang_any else ("over_cap" if over else "ok"),
             reviewers=reviewers)
    if has_board:
        tags_by = {r: read_jsonl(d / "tags" / f"{r}.jsonl") for r in info["receivers"]}
        cards = []
        delivered_items, acted = 0, {}
        for card in cards_all:
            rid = card.get("to")
            dels = {x["id"]: x for x in read_jsonl(board / "delivered" / f"{rid}.jsonl")}
            x = dels.get(card.get("id"))
            snapfail = (board / "state" / f"{rid}.snapfail").exists()
            status = x["status"] if x else ("undelivered" if snapfail else "late")
            if status == "late" and rid in reviewers:
                reviewers[rid]["late"] += 1
            if status == "delivered":
                delivered_items += len(card.get("items") or [])
                peer = {t for line in tags_by.get(rid, []) if line["origin"] == "peer" for t in line["tasks"]}
                acted.setdefault(rid, set()).update(set(card.get("items") or []) & peer)  # distinct Tasks per receiver
            cards.append({"id": card.get("id"), "to": rid, "items": card.get("items"), "t_post": card.get("t"),
                          "t_delivered": x["t"] if x and status == "delivered" else None, "status": status})
        for e in read_jsonl(board / "watcher.log"):
            if e.get("event") in ("dup_card", "after_finish"):
                cards.append({"id": None, "to": e.get("to"), "items": None, "t_post": e.get("t"), "t_delivered": None, "status": e["event"]})
        c.update(cards=cards, requests_posted=sum(len(x.get("items") or []) for x in cards_all),
                 requests_delivered=delivered_items, requests_acted=sum(len(s) for s in acted.values()))
    else:
        c.update({k: None for k in F6_ONLY_PANEL})
    # messages actually delivered per reviewer (scouts receive none); null when there is no board (A1, A2, k0_isolated)
    c["messages_delivered"] = {r: (v.get("msgs_received") or 0) for r, v in reviewers.items()} if has_board else None
    return c


def main(argv: list[str]) -> int:
    write_json(Path(argv[0]) / "collab.json", build(argv[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
