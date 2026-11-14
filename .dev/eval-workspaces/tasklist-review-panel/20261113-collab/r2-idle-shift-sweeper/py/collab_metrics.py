"""collab.json (R-23, DESIGN 2.9) and the F4 audits (R-20, DESIGN 2.5.4 and 2.8): late / cap / other partition,
first-hand evidence, re-run mismatches, unrun sweeper commands, echo rate and own-line Task Jaccard.

collab_metrics.py --pkgdir runs/<row>/<pkg> --panel <p> --values <file> --arm <F4|A1> [--row <row>] [--pkg <pkg>]
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import R2, findings  # noqa: E402

REVIEWER_KEYS = ["role", "msgs_sent", "msgs_received", "first_delivery_t", "seal_t", "resume_fallback", "phase2_s",
                 "stop_blocks", "hook_calls", "hook_error", "hook_ms_p95", "reask_s", "attempts", "retry_s",
                 "retry_isolated", "phase2_timeout", "p2_lines_salvaged", "n_planned", "n_launched", "finish_signal_t",
                 "finish_would_fire", "hang_kill", "snapshot_missing", "late", "not_delivered_cap",
                 "not_delivered_other", "peer_lines", "peer_lines_first_hand", "reruns", "rerun_mismatches",
                 "dropped_lines", "model_ok", "output_tokens", "end_t"]
SWEEPER_KEYS = ["model", "model_ok", "start_t", "end_t", "skipped_late", "facts_posted", "facts_harvested",
                "facts_rejected", "over_cap", "witness_facts", "cmd_unrun", "output_tokens"]
TOP_KEYS = ["schema", "arm", "panel", "row", "pkg", "values_sha256", "k", "panel_finish_at", "deal_r", "deal_c",
            "reviewers", "sweeper", "slots", "elapsed_s", "baseline_elapsed_s", "overhead_pct", "own_line_jaccard",
            "pairwise_task_jaccard", "echo_rate", "ledger_rows", "isolated_for", "slo_breach", "audit_ok"]
TASK_HEAD = re.compile(r"^#+\s*(Task|T)\s*(\d+)")


def jl(p: Path) -> list[dict]:
    out = []
    if p.exists():
        for line in p.read_text().splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def jload(p: Path, default=None):
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return default


def flat(s: str) -> str:
    return " ".join((s or "").split())


def p95(xs):
    if not xs:
        return None
    xs = sorted(xs)
    return xs[min(len(xs) - 1, math.ceil(0.95 * len(xs)) - 1)]


def tool_calls(transcript: list) -> list[dict]:
    """Ordered tool calls of a claude -p json output, each with its result text."""
    calls, results = [], {}
    for e in transcript if isinstance(transcript, list) else []:
        content = (e.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for c in content:
            if c.get("type") == "tool_use":
                calls.append({"id": c.get("id"), "name": c.get("name"), "input": c.get("input") or {}})
            elif c.get("type") == "tool_result":
                r = c.get("content")
                if isinstance(r, list):
                    r = "\n".join(x.get("text", "") for x in r if isinstance(x, dict))
                results[c.get("tool_use_id")] = r if isinstance(r, str) else json.dumps(r)
    for c in calls:
        c["result"] = results.get(c["id"], "")
    return calls


def is_rerun(call: dict, cmd: str) -> bool:
    if call["name"] == "Bash":
        return flat(call["input"].get("command", "")) == flat(cmd)
    if call["name"] == "Grep":
        m = re.match(r"^grep -rn -- '(.*)' (\S+)$", cmd or "")
        return bool(m) and call["input"].get("pattern") == m.group(1) and \
            (call["input"].get("path") or ".").rstrip("/").endswith(m.group(2).rstrip("/"))
    return False


def rerun_mismatch(call: dict, fact: dict) -> bool:
    out = call.get("result") or ""
    for it in fact.get("items", []):
        if it.split(":")[0] not in out:
            return True
    n = fact.get("n")
    if isinstance(n, int) and n >= 1:
        lines = [x for x in out.splitlines() if x.strip()]
        got = len(lines)
        if re.search(r"\|\s*wc\s+-l\s*$", fact.get("cmd", "")) and lines and lines[-1].strip().split()[0].isdigit():
            got = int(lines[-1].strip().split()[0])
        if got != n:
            return True
    return False


def task_of(cand: str, anchor: str) -> str | None:
    f = findings()
    hits = f.locate(cand, anchor or "")
    if not hits:
        return None
    lines = cand.splitlines()
    for i in range(min(hits[0][0], len(lines) - 1), -1, -1):
        m = TASK_HEAD.match(lines[i])
        if m:
            return f"T{int(m.group(2))}"
    return None


def mean_jaccard(sets: list[set]) -> float | None:
    vals = []
    for a, b in itertools.combinations(sets, 2):
        if a | b:
            vals.append(len(a & b) / len(a | b))
    return round(sum(vals) / len(vals), 4) if vals else None


def compute(pkgdir: Path, panel: str, values_p: Path, arm: str, row: str, pkg: str) -> dict:
    panels = json.loads((R2 / "config/panels.json").read_text())
    vals = json.loads(values_p.read_text())
    t0 = int((pkgdir / "t0").read_text())
    k = int(vals["k"])
    fin = t0 + int(round(float(vals["panel_finish_at_s"]) * 1000))
    deal_r = int((pkgdir / "deal_r").read_text()) if (pkgdir / "deal_r").exists() else 0
    elapsed = float((pkgdir / "elapsed_s").read_text()) if (pkgdir / "elapsed_s").exists() else 0.0
    B_f = float(vals["B_f"])
    collab = arm == "F4"
    board = pkgdir / "board"
    facts = jl(board / "msgs/board.jsonl") if collab else []
    rejected = jl(board / "msgs/rejected.jsonl") if collab else []
    inputs = jload(pkgdir / "inputs.json", {})
    cand_p = Path(inputs.get("sandbox", "")) / "cand/candidate.md"
    cand = cand_p.read_text() if cand_p.exists() else ""

    reviewers, slots, isolated_for = {}, [], []
    peer_total, echo_hits = 0, 0
    own_sets, all_sets = [], []
    for r in panels[panel]["reviewers"]:
        rid, role = r["rid"], r["role"]
        meta = jload(pkgdir / f"reviews/{rid}.meta.json", {})
        cost = jload(pkgdir / f"reviews/{rid}.cost.json", {})
        tags = jload(pkgdir / f"reviews/{rid}.tags.json", {"lines": []})
        mets = jl(board / f"metrics/{rid}.jsonl") if collab else []
        calls_ev = [m for m in mets if m.get("ev") == "call"]
        delivers = [m for m in mets if m.get("ev") == "deliver"]
        delivered_ids = [d["fact"] for d in delivers]
        last_call_t = max((m["t"] for m in calls_ev), default=None)
        late = cap_n = other = 0
        if collab and role == "receiver":
            ri = r["recv_index"]
            for i, f in enumerate(facts):
                if (i + deal_r) % 2 != ri:
                    continue
                d = f["id"] in delivered_ids
                is_late = (not d) and (last_call_t is None or f["t"] > last_call_t)
                if not d:
                    if is_late:
                        late += 1
                    elif len(delivered_ids) >= k:
                        cap_n += 1
                    else:
                        other += 1
                slots.append({"fact": f["id"], "i": i, "recipient": rid, "slot_type": "fact", "card_form": None,
                              "delivered": d, "late": is_late})
        # first-hand and re-run audits on this receiver's own transcript (attempt 1 is the only hooked attempt)
        tr = jload(pkgdir / f"reviews/{rid}.attempt1.json", [])
        calls = tool_calls(tr)
        fact_by_id = {f["id"]: f for f in facts}
        reruns = mism = 0
        for d in delivers:
            f = fact_by_id.get(d["fact"])
            if not f:
                continue
            for c in calls[d["c"]:]:
                if is_rerun(c, f.get("cmd", "")):
                    reruns += 1
                    mism += int(rerun_mismatch(c, f))
                    break
        peer_lines = first_hand = 0
        for ln in tags.get("lines", []):
            if ln["origin"] != "peer":
                continue
            peer_lines += 1
            fh = False
            for reason in ln["reasons"]:
                f = fact_by_id.get(reason["fact"])
                dc = next((d["c"] for d in delivers if d["fact"] == reason["fact"]), None)
                if not f or dc is None:
                    continue
                cited = set(reason.get("paths") or [i.split(":")[0] for i in f.get("items", [])])
                for c in calls[dc:]:
                    fp = (c["input"].get("file_path") or "")
                    if c["name"] == "Read" and any(fp == p or fp.endswith("/" + p) for p in cited):
                        fh = True
                    elif is_rerun(c, f.get("cmd", "")):
                        fh = True
                    if fh:
                        break
                if fh:
                    break
            first_hand += int(fh)
            if any(flat(ln.get("anchor") or "") == flat(fact_by_id[d].get("anchor") or "") and fact_by_id[d].get("anchor")
                   for d in delivered_ids if d in fact_by_id):
                echo_hits += 1
        peer_total += peer_lines
        own_sets.append({t for ln in tags.get("lines", []) if ln["origin"] == "own" for t in [task_of(cand, ln.get("anchor"))] if t})
        all_sets.append({t for ln in tags.get("lines", []) for t in [task_of(cand, ln.get("anchor"))] if t})
        seal = next((m for m in mets if m.get("ev") == "seal"), None)
        fin_ev = next((m for m in mets if m.get("ev") == "finish_signal"), None)
        end_t = meta.get("end_ms")
        iso = bool(meta.get("retry_isolated"))
        if collab and role == "receiver" and (len(delivered_ids) == 0 or iso):
            isolated_for.append(rid)
        reviewers[rid] = {
            "role": role, "msgs_sent": 0, "msgs_received": len(delivered_ids),
            "first_delivery_t": delivers[0]["t"] if delivers else None, "seal_t": seal["t"] if seal else None,
            "seal_sha256": seal.get("sha256") if seal else None,
            "resume_fallback": None, "phase2_s": None, "stop_blocks": 0,
            "hook_calls": len(calls_ev), "hook_error": sum(m.get("ev") == "hook_error" for m in mets),
            "hook_ms_p95": p95([m["ms"] for m in calls_ev if "ms" in m]),
            "reask_s": float(meta.get("reask_s") or 0), "attempts": int(meta.get("attempts") or 0),
            "retry_s": cost.get("retry_s", 0), "retry_isolated": iso, "phase2_timeout": None,
            "p2_lines_salvaged": None, "n_planned": None, "n_launched": None,
            "finish_signal_t": fin_ev["t"] if fin_ev else None,
            "finish_would_fire": bool(end_t and end_t > fin),
            "hang_kill": bool(meta.get("hang_kill")),
            "snapshot_missing": any(m.get("ev") == "snapshot_missing" for m in mets),
            "late": late, "not_delivered_cap": cap_n, "not_delivered_other": other,
            "peer_lines": peer_lines, "peer_lines_first_hand": first_hand, "reruns": reruns, "rerun_mismatches": mism,
            "dropped_lines": int(meta.get("dropped_lines") or 0), "model_ok": bool(meta.get("model_ok")),
            "output_tokens": int(cost.get("total_output_tokens_all") or 0), "end_t": end_t,
        }

    sweeper = None
    if collab:
        sm = jload(pkgdir / "sweeper/sw-1.meta.json", {})
        st = jload(pkgdir / "sweeper/start.json", {})
        sw_tr = tool_calls(jload(pkgdir / "sweeper/sw-1.json", []))
        bash_cmds = {flat(c["input"].get("command", "")) for c in sw_tr if c["name"] == "Bash"}
        sw_facts = [f for f in facts if f.get("from") == "sw-1"]
        sweeper = {
            "model": sm.get("model"), "model_ok": sm.get("model_ok"),
            "start_t": sm.get("start_ms") or st.get("sweeper_start_t"), "end_t": sm.get("end_ms"),
            "skipped_late": bool(sm.get("skipped_late")), "skipped_k0": bool(sm.get("skipped_k0")),
            "killed": bool(sm.get("killed")),
            "facts_posted": len(sw_facts), "facts_harvested": sum(f.get("from") == "hv-1" for f in facts),
            "facts_rejected": len(rejected), "over_cap": sum(x.get("reason") == "over_cap" for x in rejected),
            "witness_facts": sum(f.get("move") in ("M6", "M9") for f in facts),
            "cmd_unrun": sum(flat(f.get("cmd", "")) not in bash_cmds for f in sw_facts),
            "output_tokens": int(sm.get("output_tokens") or 0),
        }
    audit = jload(pkgdir / "audit.json", {})
    # owner-authorised time-cap exception (OVERRIDE.md): the values file carries a `time_cap_exception` block only when the row
    # was launched with TIME_CAP_EXCEPTION=1; `applied` is true for a package whose measured k was 0 (k forced to 1, guards widened)
    exc = vals.get("time_cap_exception")
    applied = bool(exc and exc.get("applied"))
    out = {
        "schema": "collab/1", "arm": arm, "panel": panel, "row": row, "pkg": pkg,
        "values_sha256": hashlib.sha256(values_p.read_bytes()).hexdigest(),
        "k": k, "panel_finish_at": fin, "deal_r": deal_r, "deal_c": None,
        "reviewers": reviewers, "sweeper": sweeper, "slots": slots,
        "elapsed_s": elapsed, "baseline_elapsed_s": B_f,
        "overhead_pct": round(100 * (elapsed / B_f - 1), 2) if B_f else None,
        "own_line_jaccard": mean_jaccard(own_sets), "pairwise_task_jaccard": mean_jaccard(all_sets),
        "echo_rate": round(echo_hits / peer_total, 4) if peer_total else None,
        "ledger_rows": 0, "isolated_for": isolated_for,
        "slo_breach": any(v["hang_kill"] for v in reviewers.values()) or elapsed > (float(vals["hang_s"]) if applied else 1.5 * B_f),
        "audit_ok": bool(audit.get("ok", True)),
        "time_cap_exception": exc is not None, "time_cap_exception_applied": applied,
        "B_A1": B_f, "k_measured": int(exc["k_measured"]) if exc else k,
        "elapsed_over_baseline": round(elapsed / B_f, 4) if B_f else None,
        "messages_delivered": {rid: r["msgs_received"] for rid, r in reviewers.items()},
    }
    check_schema(out)
    return out


def check_schema(o: dict) -> None:
    miss = [k for k in TOP_KEYS if k not in o]
    for rid, r in o["reviewers"].items():
        miss += [f"reviewers.{rid}.{k}" for k in REVIEWER_KEYS if k not in r]
    if o["sweeper"] is not None:
        miss += [f"sweeper.{k}" for k in SWEEPER_KEYS if k not in o["sweeper"]]
    if miss:
        raise ValueError(f"collab.json misses {miss}")
    for rid, r in o["reviewers"].items():
        if r["role"] == "receiver" and r["msgs_received"] > o["k"]:
            raise ValueError(f"{rid} received {r['msgs_received']} > k={o['k']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkgdir", required=True)
    ap.add_argument("--panel", required=True)
    ap.add_argument("--values", required=True)
    ap.add_argument("--arm", required=True, choices=["F4", "A1"])
    ap.add_argument("--row", default="")
    ap.add_argument("--pkg", default="")
    a = ap.parse_args(argv)
    pkgdir = Path(a.pkgdir)
    out = compute(pkgdir, a.panel, Path(a.values), a.arm, a.row or pkgdir.parent.name, a.pkg or pkgdir.name)
    (pkgdir / "collab.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"ok": True, "isolated_for": out["isolated_for"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
