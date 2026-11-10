#!/usr/bin/env python3
"""A1 obligation-to-criterion support seam (ab6).  Code builds the pairs, Jev judges one pair per call, the output is flag-only hints.

  1. extract OBLIGATIONS: WC rows (2.2), SA rows (5), per-command rows of section 3.1/3.2, the Decisions table and the open decisions D1-D5;
     extract CRITERIA: AC rows (7.1/7.3), live-check steps (7.2), phase gates (the section-6 phase table: Scope and Commands cells);
  2. prefilter (deterministic, cap 60): pair by obligation id cited in the criterion, command name in the criterion / gate Commands cell,
     universal quantifier ("every command in sections 3.1-3.2") with phase mismatch, and IDF-weighted shared distinctive tokens; WC obligations
     get a reserved quota so the WC x AC pairing is not crowded out by the 37 command rows; pairs already covered by a supplied accepted-findings
     list are dropped BEFORE the cap;
  3. Jev question `support` {supported, partial, unsupported, contradicts_or_defers, insufficient}, one pair per call;
  4. hints: at most 12 non-supported pairs, flag-only text, no severity, no finding.  Error / refusal / invalid / `insufficient` = no hint.
Controls: `keyword_flags` (prefilter pairs flagged by phase mismatch or a deferral lexicon only) and `control_items` (identical packets for a
same-packet Sonnet judge); `apply_answers` ingests that judge's answers.
CLI:  a1_support.py SPEC.md [--accepted accepted.json] [--mock MODE] [--control]
"""
import argparse
import json
import math
import pathlib
import re
import sys

import seamlib as S

QSET_VERSION = "a1-q1"
QNAME = "support"
CAP_PAIRS = 60
CAP_HINTS = 12
WC_QUOTA = 24                 # reserved slots for WC obligations (the WC x AC pairing); spills over when unused
TOKEN_MIN_SCORE = 3.0         # IDF-weighted shared-token score for a pair with no id / command link

SUPPORT_OPTIONS = {
    "supported": "The criterion, executed as written at its phase, verifies that the obligation is met, and the two texts do not conflict.",
    "partial": "The criterion verifies only part of the obligation (some of its commands, conditions or cases), or verifies it only if a later phase has landed.",
    "unsupported": "The two concern the same subject, but the criterion does not check what the obligation requires; passing it would not show the obligation is met.",
    "contradicts_or_defers": "The criterion requires or assumes something the obligation forbids, excludes or defers (another phase, an open decision, a command "
                             "excluded elsewhere), so the two cannot both hold as written.",
    "insufficient": "The state does not contain what is needed to decide between the other options.",
}
SUPPORT_INSTRUCTIONS = (
    "`obligation` is one requirement, per-command change or decision of a requirements spec; `criterion` is one acceptance check, live-check step or "
    "phase gate of the same spec; `signals` are facts a program computed about the pair. Decide whether the criterion, executed as written, shows "
    "that the obligation is met. Judge only from the texts in the state."
)


def support_question():
    return S.choice(SUPPORT_INSTRUCTIONS, SUPPORT_OPTIONS)


# ----------------------------------------------------------------------------- 1. extraction
def _phase_of(text: str):
    m = re.findall(r"\bP([0-4])\b", text or "")
    return f"P{m[0]}" if m else None


def extract(text: str) -> dict:
    """{'obligations': [...], 'criteria': [...]} -- each item {id, kind, text, line, phase, name?}."""
    doc = S.parse_spec(text)
    obl, crit = [], []
    for t in S.find_tables(doc, "id", "requirement"):
        for ln, cells in t.rows:
            i = S.strip_md(cells[0]).strip()
            if re.fullmatch(r"WC-\d+", i):
                obl.append({"id": i, "kind": "wc", "text": S.clip(S.plain(cells[1]), 900), "line": ln, "phase": None})
            elif re.fullmatch(r"SA-\d+", i):
                obl.append({"id": i, "kind": "sa", "text": S.clip(S.plain(cells[1]), 900), "line": ln, "phase": None})
    for t in doc.tables:
        h = [x.lower() for x in t.header]
        if not h or h[0] != "command" or not any("resume" in x for x in h):
            continue
        phase_col = next((i for i, x in enumerate(h) if x == "phase"), None)
        for ln, cells in t.rows:
            name = S.strip_md(cells[0]).strip().lstrip("/").replace("sc:", "")
            if not name:
                continue
            parts = []
            for i, c in enumerate(cells[1:], 1):
                if h[i].startswith("evidence") or i == phase_col:
                    continue
                parts.append(f"{S.strip_md(t.header[i])}: {S.plain(c)}")
            ph = _phase_of(cells[phase_col]) if phase_col is not None else None
            if ph is None:
                ph = _phase_of(" ".join(cells[1:]) and next((c for i, c in enumerate(cells) if "small fix" in h[i]), ""))
            obl.append({"id": f"cmd:{name}", "kind": "cmd", "name": name, "text": S.clip("; ".join(parts), 900), "line": ln, "phase": ph})
    for t in S.find_tables(doc, "decision", "rationale"):
        for ln, cells in t.rows:
            slug = re.sub(r"[^a-z0-9]+", "-", S.strip_md(cells[0]).lower()).strip("-")[:40]
            obl.append({"id": f"dec:{slug}", "kind": "dec", "text": S.clip(S.plain(cells[0]) + ": " + S.plain(cells[-1]), 900), "line": ln, "phase": None})
    # open decisions D1-D5 (section 9): a bold "D<n>." line plus its bullets
    lines = doc.lines
    for i, ln in enumerate(lines):
        m = re.match(r"^\*\*(D[1-5])\.\s+(.*?)\*\*\s*(.*)$", ln)
        if m and not doc.code[i]:
            body, j = [m.group(2), m.group(3)], i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].startswith("**D"):
                body.append(lines[j])
                j += 1
            obl.append({"id": m.group(1), "kind": "od", "text": S.clip(S.plain(" ".join(body)), 900), "line": i + 1, "phase": None})
    # criteria
    import a2_observability as A2
    rows, _ = A2.extract_rows(text)
    for r in rows:
        crit.append({"id": r["id"], "kind": "step" if r["kind"] == "step" else "ac", "text": S.clip(S.plain(r["check"]) + " => " + S.plain(r["pass"]), 900),
                     "line": r["line"], "phase": None if r["kind"] == "step" else (None if r["phase"] == "C" else _phase_of(r["phase"]))})
    for t in S.find_tables(doc, "phase", "scope", "commands"):
        for ln, cells in t.rows:
            ph = _phase_of(cells[0])
            if ph:
                crit.append({"id": f"GATE:{ph}", "kind": "gate", "text": S.clip(f"Scope: {S.plain(cells[1])} Commands: {S.plain(cells[2])}", 900), "line": ln, "phase": ph})
    return {"obligations": obl, "criteria": crit}


# ----------------------------------------------------------------------------- 2. prefilter
_STOP = set("""about above after again against also another because before being between both cannot could does doing each either every from have
having here into itself more most must never only other over same shall should since some such than that their them then there these they this those
through under until very what when where which while will with within without would your command commands spec phase phases check checks file files
section sections row rows line lines text step steps pass fails fail never always""".split())
_TOK_RE = re.compile(r"--[a-z][a-z-]+|[\w.-]+\.(?:yaml|md|json|jsonl|py|sh)\b|[A-Za-z][A-Za-z0-9_-]{3,}")
_UNIVERSAL_RE = re.compile(r"\b(every|all|each)\s+(?:\w+\s+){0,3}(command|commands)\b", re.I)
_DEFER_RE = re.compile(r"\b(defers?|deferred|until|waits? for|waits? on|after phase|not yet|later phase|open decision|unchanged|except|excluded?|no section-4)\b", re.I)


def toks(text: str) -> set:
    out = set()
    for m in _TOK_RE.findall(text or ""):
        w = m.lower()
        if w in _STOP or w.isdigit():
            continue
        out.add(w)
    return out


def _idf(items):
    df = {}
    for it in items:
        for w in it["_tok"]:
            df[w] = df.get(w, 0) + 1
    n = len(items)
    return {w: math.log((n + 1) / (c + 0.5)) for w, c in df.items()}


def _mentions_id(text: str, ident: str) -> bool:
    if ident.startswith(("cmd:", "dec:")):
        return False
    return re.search(rf"(?<![\w-]){re.escape(ident)}(?![\w.-]*\d)", text) is not None


def build_pairs(ex: dict, accepted=None, cap=CAP_PAIRS, wc_quota=WC_QUOTA) -> dict:
    """-> {'raw': n, 'eligible': n, 'dropped_covered': n, 'pairs': [pair]} -- pair = {id, o, c, score, signals{...}}."""
    obl, crit = ex["obligations"], ex["criteria"]
    for it in obl + crit:
        it["_tok"] = toks(it["text"])
    idf = _idf(obl + crit)
    pairs = []
    for o in obl:
        cmds_o = {o["name"]} if o["kind"] == "cmd" else set()
        for c in crit:
            sig = {}
            if _mentions_id(c["text"], o["id"]):
                sig["id_cited"] = True
            if o["kind"] == "cmd":
                names = set(S.commands_in(c["text"]))
                if o["name"] in names:
                    sig["command_named"] = True
                elif _UNIVERSAL_RE.search(c["text"]) and c["kind"] in ("ac", "step", "gate"):
                    sig["universal"] = True
                if (sig.get("command_named") or sig.get("universal")) and o["phase"] and c["phase"] and o["phase"] != c["phase"]:
                    sig["phase_mismatch"] = f"{o['phase']} row vs {c['phase']} criterion"
                elif (sig.get("command_named") or sig.get("universal")) and o["phase"] and o["phase"] == c["phase"]:
                    sig["phase_equal"] = True
            if _mentions_id(o["text"], c["id"]) and c["kind"] == "ac":
                sig["criterion_cited_by_obligation"] = True
            shared = sorted(w for w in o["_tok"] & c["_tok"] if idf.get(w, 0) >= 1.0)
            sscore = min(sum(idf[w] for w in shared), 6.0)
            if sscore >= TOKEN_MIN_SCORE:
                sig["shared_tokens"] = shared[:6]
            if not sig:
                continue
            score = (4 * ("id_cited" in sig) + 3 * ("command_named" in sig) + 2 * ("universal" in sig) + 2 * ("phase_mismatch" in sig)
                     + 1 * ("phase_equal" in sig) + 2 * ("criterion_cited_by_obligation" in sig) + (sscore / 2 if "shared_tokens" in sig else 0))
            pairs.append({"id": f"{o['id']}|{c['id']}", "o": o, "c": c, "score": round(score, 3), "signals": sig})
    raw = len(obl) * len(crit)
    eligible = len(pairs)
    dropped = 0
    if accepted:
        keep = []
        for p in pairs:
            if covered(p, accepted):
                dropped += 1
            else:
                keep.append(p)
        pairs = keep
    key = lambda p: (-p["score"], p["o"]["id"], p["c"]["id"])
    wc = sorted((p for p in pairs if p["o"]["kind"] == "wc"), key=key)
    rest = sorted((p for p in pairs if p["o"]["kind"] != "wc"), key=key)
    take_wc = min(len(wc), max(wc_quota, cap - len(rest)))
    chosen = wc[:take_wc] + rest[:max(cap - take_wc, 0)]
    chosen = sorted(chosen, key=key)[:cap]
    return {"raw": raw, "eligible": eligible, "dropped_covered": dropped, "pairs": chosen}


def covered(pair, accepted) -> bool:
    """A pair is covered when a supplied accepted finding already cites both sides (by id / command name in its text, or by spec lines)."""
    for f in accepted:
        txt = f.get("text", "") + " " + " ".join(f.get("ids", []))
        lines = set(f.get("lines", []))
        o, c = pair["o"], pair["c"]
        o_hit = _mentions_id(txt, o["id"]) or (o["kind"] == "cmd" and o["name"] in S.commands_in(txt)) or o["line"] in lines
        c_hit = _mentions_id(txt, c["id"]) or (c["id"].startswith("7.2#") and re.search(rf"step\s+{c['id'][5:]}\b", txt)) or c["line"] in lines
        if o_hit and c_hit:
            return True
    return False


# ----------------------------------------------------------------------------- 3. Jev items
def pair_state(p, ex) -> dict:
    o, c = p["o"], p["c"]
    gate = next((x for x in ex["criteria"] if x["kind"] == "gate" and x["phase"] == o.get("phase")), None) if o.get("phase") else None
    sig = {}
    for k, v in p["signals"].items():
        sig[k] = v if not isinstance(v, bool) else "yes"
    st = {"obligation": {"id": o["id"], "kind": o["kind"], "phase": o.get("phase") or "none", "text": S.scrub(o["text"])},
          "criterion": {"id": c["id"], "kind": c["kind"], "phase": c.get("phase") or "none", "text": S.scrub(c["text"])},
          "signals": sig}
    if gate and gate["id"] != c["id"]:
        st["obligation_phase_gate"] = {"id": gate["id"], "text": S.scrub(S.clip(gate["text"], 500))}
    return st


def build_items(text: str, sid: str, accepted=None, cap=CAP_PAIRS):
    ex = extract(text)
    bp = build_pairs(ex, accepted, cap)
    items = [S.question_item(f"{sid}:a1:{p['id']}", QSET_VERSION, pair_state(p, ex), QNAME, support_question(), pair_id=p["id"], score=p["score"])
             for p in bp["pairs"]]
    return ex, bp, items


# ----------------------------------------------------------------------------- 4. hints, controls
_LABEL_TEXT = {
    "contradicts_or_defers": "the check and the obligation conflict, or the check needs something the obligation excludes or defers to another phase",
    "unsupported": "passing the check would not show the obligation is met",
    "partial": "the check covers only part of the obligation",
}
_RANK = {"contradicts_or_defers": 0, "unsupported": 1, "partial": 2}


def make_hints(bp, outcomes, cap=CAP_HINTS) -> list:
    """-> list of hint dicts {n, pair, obligation, criterion, label, text}; flag-only, no severity; at most `cap` non-supported pairs."""
    by_id = {o["id"].split(":a1:", 1)[1]: o for o in outcomes if o.get("usable")}
    cand = []
    for p in bp["pairs"]:
        o = by_id.get(p["id"])
        if o and o["choice"] in _RANK:
            cand.append((_RANK[o["choice"]], -p["score"], p["id"], p, o))
    cand.sort(key=lambda x: (x[0], x[1], x[2]))
    hints = []
    for n, (_, _, pid, p, o) in enumerate(cand[:cap], 1):
        fact = ""
        if "phase_mismatch" in p["signals"]:
            fact = f" (phase facts: {p['signals']['phase_mismatch']})"
        txt = (f"UNVERIFIED A1-{n} [{p['o']['id']} x {p['c']['id']}] a judgment model read the obligation (spec line {p['o']['line']}) and the check "
               f"(spec line {p['c']['line']}) and found: {_LABEL_TEXT[o['choice']]}{fact}. Verify against the spec text; this is not a finding.")
        hints.append({"n": n, "pair": pid, "obligation": p["o"]["id"], "criterion": p["c"]["id"], "label": o["choice"], "text": txt})
    return hints


def keyword_flags(bp) -> list:
    """Keyword-prefilter-only control: the prefilter pairs flagged by phase mismatch or a deferral / exclusion lexicon in either text (no model)."""
    out = []
    for p in bp["pairs"]:
        why = []
        if "phase_mismatch" in p["signals"]:
            why.append("phase_mismatch")
        if _DEFER_RE.search(p["o"]["text"]) or _DEFER_RE.search(p["c"]["text"]):
            why.append("deferral_lexicon")
        if why:
            out.append({"pair": p["id"], "why": why})
    return out


def control_items(items) -> list:
    return [{"id": it["id"], "state": it["state"], "question": it["questions"][QNAME]["instructions"], "options": it["questions"][QNAME]["criteria"]}
            for it in items]


def apply_answers(items, answers: dict) -> list:
    outs = []
    for it in items:
        c = answers.get(it["id"])
        ok = c in it["questions"][QNAME]["criteria"]
        outs.append({"id": it["id"], "status": "ok" if ok else "invalid", "choice": c if ok else None, "usable": bool(ok and c != "insufficient")})
    return outs


def run_spec(text, sid, runner=None, accepted=None, cap=CAP_PAIRS):
    ex, bp, items = build_items(text, sid, accepted, cap)
    outs = [runner.ask(it) for it in items] if runner else []
    return {"sid": sid, "extract": {"obligations": len(ex["obligations"]), "criteria": len(ex["criteria"])}, "prefilter": {k: bp[k] for k in ("raw", "eligible", "dropped_covered")},
            "ex": ex, "bp": bp, "items": items, "outcomes": outs, "hints": make_hints(bp, outs), "keyword_flags": keyword_flags(bp)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("--accepted", help="JSON list of accepted findings [{ids, lines, text}] whose pairs are dropped")
    ap.add_argument("--out", default=str(S.SEAMS / "out" / "a1-cli"))
    ap.add_argument("--mock", choices=["ok", "insufficient", "malformed", "timeout", "http500", "mixed"])
    ap.add_argument("--control", action="store_true")
    a = ap.parse_args(argv)
    text = pathlib.Path(a.spec).read_text(encoding="utf-8")
    acc = json.loads(pathlib.Path(a.accepted).read_text()) if a.accepted else None
    out = pathlib.Path(a.out)
    if a.mock:
        with S.mock_env():
            r = S.Runner(seam="a1", mode="mock", out_dir=out, mock_mode=a.mock)
            res = run_spec(text, "cli", r, acc)
    else:
        res = run_spec(text, "cli", None, acc)
    print(f"obligations {res['extract']['obligations']} criteria {res['extract']['criteria']} raw {res['prefilter']['raw']} eligible "
          f"{res['prefilter']['eligible']} dropped {res['prefilter']['dropped_covered']} sent {len(res['items'])}")
    for h in res["hints"]:
        print(h["text"])
    if a.control:
        S.write_json(out / "control-packets.json", control_items(res["items"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
