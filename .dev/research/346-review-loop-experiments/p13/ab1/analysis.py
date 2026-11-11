"""Pure analysis functions for PN1: transcript token counting (C9.1) and the decision rules (D1-D4).

All decision constants live in rules.json (data, not code). The cost convention (D2) is implemented here once:
  A = LOOP-ONLY output tokens (every review, revise, panel, merge/ledger, adjudication worker of the loop, NOT the frozen AUD/AUD2)
  B = A + one audit (reported next to A, never decides pass/fail)
Tokens are counted with every message id ONCE (max output_tokens over the lines that share the id).
"""
import collections, glob, json, pathlib, re
from datetime import datetime

HERE = pathlib.Path(__file__).parent
RULES_PATH = HERE / "rules.json"


def load_rules(path=None):
    return json.loads(pathlib.Path(path or RULES_PATH).read_text())


# ---------------------------------------------------------------- transcripts (C9.1)

def _lines(path):
    try:
        text = pathlib.Path(path).read_text(errors="ignore")
    except OSError:
        return []
    out = []
    for ln in text.splitlines():
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    return out


def transcript_stats(path):
    """{'out': output tokens (each message id once), 'model': most common assistant model, 'msgs', 't0', 't1', 'done', 'text'}"""
    per_id = {}
    extra = collections.defaultdict(dict)       # message id -> {field: max}
    models = collections.Counter()
    ts = []
    done = False
    last_text = ""
    for d in _lines(path):
        if d.get("timestamp"):
            ts.append(d["timestamp"])
        msg = d.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        mid = msg.get("id") or d.get("uuid")
        u = msg.get("usage") or {}
        n = u.get("output_tokens") or 0
        per_id[mid] = max(per_id.get(mid, 0), n)
        for fld in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
            extra[mid][fld] = max(extra[mid].get(fld, 0), u.get(fld) or 0)
        if msg.get("model"):
            models[msg["model"]] += 1
        content = msg.get("content")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict):
                    if c.get("type") == "tool_use" and c.get("name") == "SubagentHandback":
                        done = True
                    if c.get("type") == "text" and c.get("text"):
                        last_text = c["text"]
        elif isinstance(content, str):
            last_text = content
    if "DONE" in last_text:
        done = True
    tot = lambda f: sum(v.get(f, 0) for v in extra.values())
    return {"out": sum(per_id.values()), "in": tot("input_tokens"), "cache_read": tot("cache_read_input_tokens"),
            "cache_write": tot("cache_creation_input_tokens"), "model": models.most_common(1)[0][0] if models else None, "msgs": len(per_id),
            "t0": ts[0] if ts else None, "t1": ts[-1] if ts else None, "done": done}


def wall_seconds(t0, t1):
    if not t0 or not t1:
        return None
    f = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    return round((f(t1) - f(t0)).total_seconds(), 1)


def find_transcripts(prompt_path, tasks_glob):
    """Transcripts whose first 6 lines contain the absolute path of the step's PROMPT file."""
    hits = []
    for f in sorted(glob.glob(tasks_glob)):
        try:
            with open(f, errors="ignore") as fh:
                head = "".join(next(fh, "") for _ in range(6))
        except OSError:
            continue
        if str(prompt_path) in head:
            hits.append(f)
    return hits


def step_tokens(prompt_path, tasks_glob, expected_model=None, warn=print):
    """Pick the transcript of a step (C9.1): the expected model with the most output tokens; WARN when several match."""
    hits = find_transcripts(prompt_path, tasks_glob)
    if not hits:
        return None
    stats = [(f, transcript_stats(f)) for f in hits]
    if len(stats) > 1:
        warn(f"WARN {len(stats)} transcripts match {prompt_path}; keeping the best")
    def key(fs):
        f, s = fs
        return (1 if (expected_model and s["model"] and expected_model in s["model"]) else 0, s["out"])
    f, s = max(stats, key=key)
    return dict(s, path=f)


# ---------------------------------------------------------------- decision rules (D1-D4)

def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def ratio(a, b):
    return None if a is None or not b else a / b


def token_view(loop_tokens, audit_tokens, rules):
    """D2: A = loop-only (decides), B = loop + one audit (reported). Ratios against A_BASE and B_BASE."""
    t = rules["tokens"]
    A = mean(loop_tokens)
    aud = mean(audit_tokens)
    B = None if A is None or aud is None else A + aud
    return {"A": A, "AUD": aud, "B": B, "R_LOOP": ratio(A, t["A_BASE"]), "R_B": ratio(B, t["B_BASE"])}


def classify(stats, rules, n_runs_planned=6):
    """Sonnet decision for one arm.

    stats: BLK_T (mean blocking ids per audit), PASS_T (share of runs whose ledger decision is PASS within 3 reviews),
    GROWTH_T (fraction, e.g. 0.0141), R_LOOP, BLOCK_OK (share), completed (runs), audit_gap (|mean AUD - mean AUD2|).
    Returns {'decision': ADOPT|DROP-1|DROP-2|DROP-3|INCONCLUSIVE, 'cost_hold': bool, 'reasons': [..]} before the Haiku gate (D3).
    """
    r = rules["decision"]
    b = rules["baseline"]
    reasons = []
    if stats["completed"] < r["min_completed_runs"]:
        return {"decision": "INCONCLUSIVE", "cost_hold": False, "reasons": [f"fewer than {r['min_completed_runs']} completed runs ({stats['completed']})"]}
    if stats.get("audit_gap") is not None and stats["audit_gap"] > r["max_audit_gap"]:
        reasons.append(f"audit means differ by {stats['audit_gap']:.2f} > {r['max_audit_gap']}")
        incon = True
    else:
        incon = False
    b_blk = b["B_BLK"]
    if stats["BLK_T"] > r["drop1_blk_factor"] * b_blk:
        return {"decision": "DROP-1", "cost_hold": False, "reasons": [f"BLK_T {stats['BLK_T']:.2f} > {r['drop1_blk_factor']} * B_BLK ({r['drop1_blk_factor'] * b_blk:.2f})"]}
    if stats["R_LOOP"] is not None and stats["R_LOOP"] > r["drop2_r_loop"]:
        return {"decision": "DROP-2", "cost_hold": False, "reasons": [f"R_LOOP {stats['R_LOOP']:.2f} > {r['drop2_r_loop']}"]}
    if stats["PASS_T"] < r["drop3_pass_min"] or stats["GROWTH_T"] > r["drop3_growth_factor"] * b["B_GROWTH"]:
        return {"decision": "DROP-3", "cost_hold": False, "reasons": [f"PASS_T {stats['PASS_T']:.3f} (min {r['drop3_pass_min']:.3f}) or GROWTH_T {stats['GROWTH_T']:.4f} (max {r['drop3_growth_factor'] * b['B_GROWTH']:.4f})"]}
    cost_hold = stats["R_LOOP"] is not None and r["cost_hold_r_loop"] < stats["R_LOOP"] <= r["drop2_r_loop"]
    if cost_hold:
        reasons.append(f"COST-HOLD: {r['cost_hold_r_loop']} < R_LOOP {stats['R_LOOP']:.2f} <= {r['drop2_r_loop']}; at best INCONCLUSIVE")
    clear = (stats["BLK_T"] <= r["adopt_blk_factor"] * b_blk and stats["PASS_T"] >= r["adopt_pass_min"]
             and stats["GROWTH_T"] <= r["adopt_growth_max"] and stats["BLOCK_OK"] >= r["adopt_block_ok_min"]
             and not cost_hold and not incon)
    if clear:
        return {"decision": "ADOPT", "cost_hold": False, "reasons": ["all ADOPT conditions hold"]}
    if not cost_hold and not incon:
        reasons.append("between the ADOPT and DROP thresholds")
    return {"decision": "INCONCLUSIVE", "cost_hold": cost_hold, "reasons": reasons}


def haiku_gate(test, base, rules):
    """D3: the Haiku stratum must point the same way. test/base: dicts with mean_blk, lost_rate, n. Never pooled with Sonnet.

    Returns {'status': 'pending'|'ok'|'fail', 'ratio': test/base mean audit blockers, 'reasons': [...]}.
    """
    h = rules["haiku"]
    if not test or test.get("n", 0) < 1 or not base or base.get("mean_blk") is None:
        return {"status": "pending", "ratio": None, "reasons": ["Haiku stratum not run or Haiku baseline missing"]}
    rat = ratio(test["mean_blk"], base["mean_blk"]) if base["mean_blk"] else None
    reasons = []
    ok = True
    if rat is None or not rat < 1:
        ok = False
        reasons.append(f"no relative reduction (ratio {rat})")
    if test.get("lost_rate", 0) > base.get("lost_rate", 0) + h["max_lost_rate_excess"]:
        ok = False
        reasons.append(f"harness-failure rate {test.get('lost_rate'):.2f} exceeds baseline {base.get('lost_rate', 0):.2f} + {h['max_lost_rate_excess']}")
    return {"status": "ok" if ok else "fail", "ratio": rat, "reasons": reasons}


def final_decision(sonnet, haiku):
    """Combine the Sonnet class with the Haiku gate (D3): ADOPT needs the Haiku stratum to agree; pending keeps the note."""
    d = sonnet["decision"]
    if d != "ADOPT":
        return d
    if haiku["status"] == "pending":
        return "ADOPT (Haiku robustness pending)"
    if haiku["status"] == "fail":
        return "INCONCLUSIVE"
    return "ADOPT"


def extension_needed(sonnet, n_sonnet, rules):
    """D4: once, only when the Sonnet n=6 result is INCONCLUSIVE; never a second time without the owner."""
    e = rules["extension"]
    return sonnet["decision"] == "INCONCLUSIVE" and n_sonnet == e["base_replicates"]


def convert_limit(L, rules):
    """D6.1: a limit L stated against loop+audit (R_B) -> loop-only limit, two decimals."""
    t = rules["tokens"]
    return round((L * t["B_BASE"] - t["AUD_BASE"]) / t["A_BASE"], 2)


# ---------------------------------------------------------------- outcome and coverage metrics (set based)

def jaccard(a, b):
    u = set(a) | set(b)
    return (len(set(a) & set(b)) / len(u)) if u else None


def outcome_rows(hits, blocking_n, universe, rejected=None, tokens=None):
    """Per-reviewer outcome numbers for one round-1 panel (contract C8 outcome fields).

    hits: {rid: set of confirmed defect keys the reviewer reported as blocking}; blocking_n: {rid: blocking findings};
    universe: confirmed defects present in the reviewed version; rejected: {rid: blocking findings an adjudicator rejected} or None.
    """
    out = {}
    for rid, h in hits.items():
        others = [hits[o] for o in hits if o != rid]
        tp = len(h)
        fp = None if rejected is None else rejected.get(rid, 0)
        unique = len(set(h) - set().union(*others)) if others else len(h)
        js = [jaccard(h, o) for o in others]
        js = [j for j in js if j is not None]
        prec = (tp / (tp + fp)) if fp is not None and (tp + fp) > 0 else None
        tok = (tokens or {}).get(rid)
        out[rid] = {"confirmed_tp": tp, "false_pos": fp, "unconfirmed": max(blocking_n.get(rid, 0) - tp - (fp or 0), 0), "unique_tp": unique,
                    "overlap_mean_jaccard": (sum(js) / len(js)) if js else None,
                    "recall_vs_confirmed": (tp / len(universe)) if universe else None, "precision": prec,
                    "cost_per_confirmed_tp": (tok / tp) if (tok and tp) else None}
    return out


def union_recall(sets, universe):
    return len(set().union(*sets) & set(universe)) / len(universe) if universe and sets else None


def leave_one_out(hits, universe):
    """{rid: (union of all, union without rid, marginal value)} as recalls of the confirmed universe."""
    full = union_recall(list(hits.values()), universe)
    res = {}
    for rid in hits:
        rest = union_recall([v for k, v in hits.items() if k != rid], universe)
        res[rid] = {"union_all": full, "union_without": rest, "marginal": (full - rest) if (full is not None and rest is not None) else None}
    return res


def residual_class(audit_theme, r1_themes):
    """Residual decomposition: an audit blocking finding is 'found, then survived' when the run's own R1 union had the theme."""
    return "found_then_survived" if audit_theme in r1_themes and audit_theme != "other" else "never_found"
