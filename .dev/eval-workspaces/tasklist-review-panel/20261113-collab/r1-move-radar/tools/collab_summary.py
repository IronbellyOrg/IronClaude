"""collab_summary.py: audits, quarantine and collab.json for one package of one row (R-23, R-09, R-25 inputs).

Usage (run from REPO with `uv run python`):
  collab_summary.py pre  <row> <pkg> [--root R1] [--sb SB] [--a1 A1DIR]   after the reviewers, before the merge
  collab_summary.py post <row> <pkg> [--root R1] [--sb SB] [--a1 A1DIR]   after the anonymiser: ledger_rows, anon_leak
  collab_summary.py catcheck <catalogue.json> <ground-truth.json>...       (G-PINS, R-07)
pre exits 3 and writes runs/<row>/<pkg>/QUARANTINED on a hard audit failure (DESIGN.md sections 2.2, 2.8, 2.9, 2.10).
"""

from __future__ import annotations

import glob
import itertools
import json
import os
import re
import subprocess
import sys

from superclaude.cli.review import findings as fnd

REPO = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel"
TOOLS = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.dirname(TOOLS)
A1DIR = f"{REPO}/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
SB = "/tmp/evalsb-collab-r1"
WINDOW = 12
SEARCH_MOVES = ["M1", "M2", "M4", "M7"]
NULL_REVIEWER = {"resume_fallback": None, "phase2_s": None, "phase2_timeout": None, "p2_lines_salvaged": None,
                 "n_planned": None, "n_launched": None, "stop_blocks": 0, "over_cap": 0, "msgs_sent": 0, "late": 0}


# ---------------------------------------------------------------- ground-truth windows (R-07)
def gt_hits(texts: list[str], quotes: list[str]) -> list[dict]:
    """Every 12-character window of a ground-truth plan_quote found inside one of the texts."""
    flat = lambda s: " ".join(s.split())  # noqa: E731
    hits = []
    for qi, q in enumerate(quotes):
        q = flat(q)
        wins = {q[i : i + WINDOW] for i in range(max(0, len(q) - WINDOW + 1))}
        for ti, t in enumerate(texts):
            t = flat(t)
            for w in sorted(wins):
                if w in t:
                    hits.append({"quote": qi, "text": ti, "window": w})
                    break
    return hits


def catalogue_texts(cat: dict) -> list[str]:
    out = []
    for m, t in cat["moves"].items():
        out.append(t)
        if m in cat["observable"]:
            out.append(t + cat["observable_suffix"])
    return out + [cat["src_text"], cat["finish_text"]]


def gt_quotes(paths: list[str]) -> list[str]:
    return [it["plan_quote"] for p in paths for it in json.load(open(p))["items"] if it.get("plan_quote")]


def cmd_catcheck(cat_path: str, gt_paths: list[str]) -> int:
    hits = gt_hits(catalogue_texts(json.load(open(cat_path))), gt_quotes(gt_paths))
    print(json.dumps({"ground_truth_files": len(gt_paths), "hits": hits, "pass": not hits}))
    return 0 if not hits else 1


# ---------------------------------------------------------------- helpers
def jsonl(path: str) -> list[dict]:
    """Objects of a JSONL file; torn, corrupt or non-object lines are skipped (R-22)."""
    out = []
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return out
    for ln in lines:
        try:
            v = json.loads(ln)
        except ValueError:
            continue
        if isinstance(v, dict):
            out.append(v)
    return out


def load(path: str, default=None):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return default


def p95(xs: list[float]):
    if not xs:
        return None
    s = sorted(xs)
    return s[max(0, -(-95 * len(s) // 100) - 1)]


def classify(records: list[dict], index_path: str, srcpath: str) -> list[dict]:
    """Run radar-classify.jq over tele records -> [{"n","sig"}] in the same order."""
    if not records:
        return []
    r = subprocess.run(["jq", "-c", "--slurpfile", "ix", index_path, "--arg", "srcpath", srcpath, "-f", f"{TOOLS}/radar-classify.jq"],
                       input="\n".join(json.dumps(x) for x in records) + "\n", capture_output=True, text=True, check=True)
    return [json.loads(x) for x in r.stdout.splitlines()]


def transcript_records(review_dir: str, rid: str) -> list[dict]:
    """Tele-shaped records from the --output-format json transcripts (collab 0 has no hook telemetry)."""
    out, n = [], 0
    for att in sorted(glob.glob(f"{review_dir}/{rid}.attempt*.json")):
        entries = load(att, [])
        for en in entries if isinstance(entries, list) else []:
            if not isinstance(en, dict) or en.get("type") != "assistant":
                continue
            sub = bool(en.get("parent_tool_use_id"))
            for c in (en.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    if not sub:
                        n += 1
                    out.append({"n": None if sub else n, "t": None, "rid": rid, "sub": sub, "tool": c.get("name"), "input": c.get("input") or {}})
    return out


def task_sections(cand: str) -> list[tuple[int, int, str]]:
    """(start line, end line, Task id) for each '## Task N:' section, 0-based half-open."""
    lines = cand.splitlines()
    heads = [(i, "T" + re.match(r"^## Task (\d+):", ln).group(1)) for i, ln in enumerate(lines) if re.match(r"^## Task \d+:", ln)]
    out = []
    for i, t in heads:
        end = len(lines)
        for k in range(i + 1, len(lines)):
            if lines[k].startswith("## "):
                end = k
                break
        out.append((i, end, t))
    return out


def tasks_of_report(report: str, cand: str, sections) -> set[str]:
    """Task ids whose section contains the anchor of a parsed finding (own_line_jaccard input)."""
    out = set()
    for f in fnd.parse_block(report)["findings"]:
        for a, _b in fnd.locate(cand, f["anchor"]):
            for s, e, t in sections:
                if s <= a < e:
                    out.add(t)
    return out


def mean_pairwise_jaccard(sets: list[set]):
    pairs = list(itertools.combinations(sets, 2))
    if not pairs:
        return None
    js = [len(a & b) / len(a | b) if (a | b) else 0.0 for a, b in pairs]  # an empty pair counts 0
    return sum(js) / len(js)


def validate_pairs(pairs: list[dict], cat_path: str, searcher: str, readers: list[str]) -> list[dict]:
    r = subprocess.run(["bash", f"{TOOLS}/msg-validate.sh", cat_path, searcher, ",".join(readers)],
                       input="".join(json.dumps(p) + "\n" for p in pairs), capture_output=True, text=True)
    return [json.loads(x) for x in r.stderr.splitlines() if x.startswith("{")]


# ---------------------------------------------------------------- pre / post
def pre(row: str, pkg: str, root: str, sb: str, a1: str) -> int:
    d = f"{root}/runs/{row}/{pkg}"
    rev, board = f"{d}/reviews", f"{d}/board"
    run = load(f"{d}/run.json")
    collab = int(run["collab"])
    roles = run["role"]
    rids = list(roles)
    searcher = next(r for r in rids if roles[r] == "searcher")
    readers = [r for r in rids if roles[r] == "reader"]
    cat_path = f"{board}/ctx/catalogue.json" if os.path.exists(f"{board}/ctx/catalogue.json") else f"{root}/config/catalogue.json"
    index_path = f"{root}/index/{pkg}.json"  # post hoc uses the index on disk, not the board's frozen copy (F-1)
    srcpath = f"{sb}/cand/{pkg}/source.md"
    hard, flags = [], []
    metas = {r: load(f"{rev}/{r}.meta.json", {}) for r in rids}

    # telemetry: hook tele (collab 1) or transcript tool_use blocks (collab 0, post-hoc coverage counters)
    tele = {r: jsonl(f"{board}/tele/{r}.jsonl") if collab else transcript_records(rev, r) for r in rids}
    metrics = {r: jsonl(f"{board}/metrics/{r}.jsonl") for r in rids}
    allrec = [x for r in rids for x in tele[r]]
    sig_of = classify(allrec, index_path, srcpath)
    sigs, i = {r: [] for r in rids}, 0
    for r in rids:
        for rec in tele[r]:
            sigs[r].append((rec, set(sig_of[i]["sig"])))
            i += 1

    # board lines and inject events pair one to one; every pair passes the validator (leak lookup, section 2.2)
    mpath = f"{board}/msgs/radar.jsonl"
    raw_msgs = open(mpath).read().splitlines() if os.path.exists(mpath) else []
    injects = {e["id"]: (r, e) for r in rids for e in metrics[r] if e.get("ev") == "inject"}
    by_id = {}
    for raw in raw_msgs:
        try:
            by_id[json.loads(raw).get("id")] = raw
        except (ValueError, AttributeError):
            hard.append(f"board line not a JSON object: {raw[:80]}")
    pairs = []
    for mid, raw in by_id.items():
        if mid not in injects:
            hard.append(f"board line {mid} has no inject event")
        else:
            pairs.append({"line": raw, "text": injects[mid][1].get("text")})
    for mid in injects:
        if mid not in by_id:
            hard.append(f"inject event {mid} has no board line")
    rejects = validate_pairs(pairs, cat_path, searcher, readers) if pairs else []
    hard += [f"validator {x['reject']}" for x in rejects]
    if any('"task_hint"' in raw for raw in raw_msgs):
        hard.append("task_hint in a board line")

    # ground truth and read-only audits (R-09, Redesign 1 (e), section 2.8)
    gt = f"{a1}/{pkg}/ground-truth.json"
    quotes = gt_quotes([gt]) if os.path.exists(gt) else []
    gth = gt_hits(raw_msgs, quotes)
    if gth:
        hard.append(f"{len(gth)} board line(s) hold a 12-character ground-truth window")
    gt_tele = [r for r in rids for rec in tele[r] if re.search(r"\.dev/reflect|ground-truth", json.dumps(rec.get("input")))]
    if gt_tele:
        hard.append(f"tele names .dev/reflect or ground-truth ({len(gt_tele)} record(s))")
    repo = f"{sb}/{pkg}/repo"
    st = subprocess.run(["git", "-C", repo, "status", "--porcelain"], capture_output=True, text=True)
    dirty = st.returncode != 0 or bool(st.stdout.strip())
    if dirty:
        hard.append("sandbox git status not clean")
    if os.path.exists(f"{repo}/.dev/reflect"):
        hard.append("sandbox holds .dev/reflect")
    cs = subprocess.run(["sha256sum", f"{sb}/cand/{pkg}/candidate.md"], capture_output=True, text=True).stdout.split()
    cand_ok = bool(cs) and cs[0] == run.get("cand_sha256")
    if not cand_ok:
        hard.append("candidate sha256 changed")

    # live-vs-post-hoc spot check (F-1): an observable move injected although the panel had already done it,
    # or a no_gap skip although a search move was still uncovered
    spot = []

    def seen(rr, rec, r, e):  # what the hook could see at that checkpoint: own calls up to n, peers' calls before t
        if rec.get("sub"):
            return False
        if rr == r:
            return (rec.get("n") or 0) <= (e.get("n") or 0)
        return (rec.get("t") or 0) < (e.get("t") or 0)

    for mid, (r, e) in injects.items():
        if e.get("slot_type") != "search":
            continue
        done = sorted({rr for rr in rids for rec, s in sigs[rr] if e["move"] in s and seen(rr, rec, r, e)})
        if done:
            spot.append({"id": mid, "move": e["move"], "live": "uncovered", "post_hoc": "covered", "by": done})
    for r in rids:
        for e in metrics[r]:
            if e.get("ev") == "skip" and e.get("reason") == "no_gap" and roles[r] == "searcher":
                # the skip event carries n only (section 2.4); its time is that of the own tele record with that n
                t = next((rec.get("t") for rec, _ in sigs[r] if rec.get("n") == e.get("n") and not rec.get("sub")), None)
                e = dict(e, t=e.get("t", t))
                cov = {m for rr in rids for rec, s in sigs[rr] if seen(rr, rec, r, e) for m in s}
                miss = [m for m in SEARCH_MOVES if m not in cov]
                if miss:
                    spot.append({"n": e.get("n"), "rid": r, "live": "no_gap", "post_hoc_uncovered": miss})

    # per reviewer and per slot
    finish_ms = run["FINISH_MS"]
    reviewers, slots = {}, []
    for r in rids:
        m, met = metas[r], metrics[r]
        inj = [e for e in met if e.get("ev") == "inject"]
        seal = [e for e in met if e.get("ev") == "seal"]
        fin = [e for e in met if e.get("ev") == "finish"]
        hook_calls = sum(1 for x in tele[r] if not x.get("sub")) if collab else 0
        would = (m.get("end_ms") or 0) > finish_ms if not collab else None
        if not collab:  # the collab-0 board holds only this metrics line (written here, not by a hook)
            os.makedirs(f"{board}/metrics", exist_ok=True)
            with open(f"{board}/metrics/{r}.jsonl", "w") as f:
                f.write(json.dumps({"ev": "finish_would_fire", "value": would}) + "\n")
        reviewers[r] = dict(NULL_REVIEWER, **{
            "model": run["model"][r], "role": roles[r], "valid": m.get("valid"), "session_ids": m.get("session_ids", []),
            "msgs_received": len(inj), "first_delivery_t": inj[0]["t"] if inj else None, "seal_t": seal[0]["t"] if seal else None,
            "hook_calls": hook_calls, "hook_error": sum(1 for e in met if e.get("ev") == "hook_error"),
            "hook_ms_p95": p95([e["ms"] for e in met if e.get("ev") == "t" and isinstance(e.get("ms"), (int, float))]),
            "reask_s": m.get("reask_s"), "attempts": m.get("attempts"), "retry_s": m.get("retry_s"), "retry_isolated": m.get("retry_isolated"),
            "dropped_lines": m.get("dropped_lines"), "k": run["k"][roles[r]] if collab else 0, "panel_finish_at": finish_ms,
            "finish_signal_t": fin[0]["t"] if fin else None, "finish_would_fire": would, "hang_kill": m.get("hang_kill"),
            "snapshot_missing": sum(1 for e in met if e.get("ev") == "snapshot_missing"),
            "isolated": bool(collab) and (hook_calls == 0 or bool(m.get("retry_isolated"))),
            "start_ms": m.get("start_ms"), "end_ms": m.get("end_ms")})
        for e in inj:
            ex = None
            if e.get("slot_type") == "search" and e.get("move"):
                ex = any(e["move"] in s for rec, s in sigs[r] if not rec.get("sub") and (rec.get("n") or 0) > e["n"])
            slots.append({"rid": r, "id": e["id"], "n": e["n"], "t": e["t"], "slot_type": e.get("slot_type"), "move": e.get("move"),
                          "task_hint": e.get("task_hint", []), "move_executed": ex, "card_form": None, "deal_r": None, "deal_c": None})
        if collab and hook_calls == 0:
            flags.append(f"ALARM hook_calls=0 {r}")

    # panel
    ends = [m.get("end_ms") for m in metas.values() if m.get("end_ms")]
    elapsed = (max(ends) - run["T0_MS"]) / 1000 if ends else None
    B = run["B"]  # noqa: N806 (the design's symbol)
    cand = open(f"{sb}/cand/{pkg}/candidate.md").read()
    secs = task_sections(cand)
    tsets = []
    for r in rids:
        try:
            tsets.append(tasks_of_report(open(f"{rev}/{r}.md").read(), cand, secs))
        except OSError:
            tsets.append(set())
    jac = mean_pairwise_jaccard(tsets)
    cover = {s: sum(1 for r in rids for rec, ss in sigs[r] if not rec.get("sub") and s in ss)
             for s in ["M1", "M2", "M4", "M7", "SRC_OPENED", "UNNAMED_TEST"]}
    byk: dict[str, int] = {}
    for s in slots:
        byk[s["move"] or "SRC"] = byk.get(s["move"] or "SRC", 0) + 1
    hang_s = (run["HANG_MS"] - run["T0_MS"]) / 1000
    collab_json = {
        "schema": "r1-collab/1", "row": row, "pkg": pkg, "arm": "A6-F3" if collab else "A1", "collab": collab,
        "panel_finish_at": finish_ms, "values_sha256": run.get("values"), "echo_rate": None,
        "reviewers": reviewers, "slots": slots,
        "elapsed_s": elapsed, "baseline_elapsed_s": B, "overhead_pct": (100 * (elapsed / B - 1)) if elapsed is not None else None,
        "own_line_jaccard": jac, "pairwise_task_jaccard": jac, "task_sets": {r: sorted(t) for r, t in zip(rids, tsets)},
        "ledger_rows": None, "anon_leak": None,
        "slo_breach": any(bool(m.get("hang_kill")) for m in metas.values()) or (elapsed is not None and elapsed > hang_s),
        "moves_covered": cover, "injections_by_move": byk, "alarms": flags,
    }
    if run.get("time_cap_exception"):  # owner-authorised time-cap exception (OVERRIDE.md): the extra columns exist only on these rows
        cx = run["cap_exception"]
        collab_json.update({
            "time_cap_exception": True, "B_A1": B, "elapsed_over_baseline": (elapsed / B) if elapsed is not None else None,
            "forced_k": cx["forced_k"], "k_measured": cx["k_measured"], "forced_roles": cx["forced_roles"], "cap_exception": cx,
            "delivered": {r: reviewers[r]["msgs_received"] for r in rids}})
    audit = {"schema": "r1-audit/1", "row": row, "pkg": pkg, "hard_failures": hard, "sandbox_clean": not dirty,
             "candidate_sha_unchanged": cand_ok, "gt_substrings_in_board": len(gth), "tele_naming_ground_truth": len(gt_tele),
             "validator_rejects": rejects, "spot_check": spot, "leak_violations": len(rejects) + len(gth), "anon_leak": None}
    json.dump(collab_json, open(f"{d}/collab.json", "w"), indent=1)
    json.dump(audit, open(f"{d}/audit.json", "w"), indent=1)
    for a in flags:
        print(a)
    if hard:  # quarantine in place, nothing deleted (R-26)
        with open(f"{d}/QUARANTINED", "w") as f:
            f.write("; ".join(hard) + "\n")
        print(f"QUARANTINED {row}/{pkg}: {'; '.join(hard)}", file=sys.stderr)
        return 3
    return 0


LEAK_PATTERNS = [r"\bc[01]\b", r"\bradar\b", r"evalsb-collab-r1", r"\bt[0-9a-z]+-[0-9]+\b"]


def post(row: str, pkg: str, root: str, sb: str, a1: str) -> int:
    d = f"{root}/runs/{row}/{pkg}"
    c, a = load(f"{d}/collab.json"), load(f"{d}/audit.json")
    led = load(f"{d}/ledger.json")
    c["ledger_rows"] = len(led["rows"]) if led else None
    key = load(f"{d}/label-key.json")
    leak = None
    if key:
        p = f"{root}/scoring/{key['opaque']}/{pkg}/{key['label']}/merged-anon.md"
        if os.path.exists(p):
            text = open(p).read()
            leak = text.count(row) + sum(len(re.findall(x, text)) for x in LEAK_PATTERNS)
    c["anon_leak"] = a["anon_leak"] = leak
    json.dump(c, open(f"{d}/collab.json", "w"), indent=1)
    json.dump(a, open(f"{d}/audit.json", "w"), indent=1)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) >= 3 and argv[0] == "catcheck":
        return cmd_catcheck(argv[1], argv[2:])
    opts = {"--root": R1, "--sb": SB, "--a1": A1DIR}
    rest, it = [], iter(argv)
    for x in it:
        if x in opts:
            opts[x] = next(it)
        else:
            rest.append(x)
    if len(rest) == 3 and rest[0] in ("pre", "post"):
        return (pre if rest[0] == "pre" else post)(rest[1], rest[2], opts["--root"], opts["--sb"], opts["--a1"])
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
