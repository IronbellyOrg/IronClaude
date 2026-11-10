#!/usr/bin/env python3
"""Kill-rule metrics of the ab6 seams against the ledger (statuses are the truth; no model label is ever truth).

  python3 score_gates.py --seam a1|a2|a3|triage|all [--out DIR]

Reads out/<seam>/<sid>.json written by replay.py (mock or live), recomputes every code-stage quantity from the spec text, and writes
out/<seam>/gates.json and out/<seam>/GATES.md.  A result computed from a MOCK replay is plumbing, not evidence: every file carries the mode.

DEFINITIONS (also in READY.md)
 relevant pairs of a defect   OBL(D) x CRIT(D) where OBL(D) = obligation ids named in the defect text (WC-n, SA-n, open decisions D1-D5, command names)
                              and CRIT(D) = criterion ids named in it (AC ids, "step n" = 7.2 live-check step n, "Pn gate/scope/Commands/row" = the
                              phase gate Pn); only ids that exist in the scored spec count.  A defect with an empty side is `unpairable` (listed, not scored).
 prefilter recall             sum over scored cells of |relevant pairs the capped prefilter emits| / sum of |relevant pairs|.  Reported over (i) the residual
                              cells (defect not FIXED/DELETED_OK in that spec: the judges' "pairs behind the residual cells"), (ii) all cells, for the strict
                              T1 class (15 defects), the extended class and all 44 defects.
 flag -> defect               a flagged pair maps to every defect whose relevant-pair set contains it in that spec.
 true / false / unmapped flag true: some mapped defect is residual; false: mapped defects exist and all are FIXED/DELETED_OK (the judges' "false flag");
                              unmapped: no defect maps (truth unknown, not counted false; reported as a worst-case bound).
 beyond-control catch         a RESIDUAL BLOCKING defect that a Jev flag (shown hint) maps to and that neither the widened lint (REF+PATH+PHASE lines on the
                              defect's lines) nor the keyword prefilter flags maps to.
"""
import argparse
import collections
import json
import math
import pathlib
import re
import sys

import seamlib as S
import a1_support as A1
import a2_observability as A2
import a3_novelty as A3

OUT = S.SEAMS / "out"
T1 = ["D01", "D03", "D04", "D05", "D11", "D12", "D13", "D14", "D26", "D27", "D28", "D38", "D39", "D40", "D44"]        # A1 advocate, strict class
T2 = ["D02", "D06", "D07", "D08", "D09", "D10", "D31"]                                                              # A1 advocate, extension
A2_CLASS = ["D11", "D12", "D14", "D15", "D16", "D17", "D18", "D19", "D20", "D21", "D22", "D23", "D37", "D38", "D39", "D40", "D44"]   # A2 advocate: 17
A2_TAIL = ["D14", "D15", "D16", "D17", "D18", "D19", "D23", "D37", "D38", "D39", "D40", "D44"]                                 # A2 advocate: the 12 semantic-tail defects


# ----------------------------------------------------------------------------- shared loaders
class Ctx:
    def __init__(self, sids=None):
        self.specs = [e for e in S.load_specs13() if not sids or e["sid"] in sids]
        self.orig = (S.SP / "p17" / "in" / "spec-original.md").read_text(encoding="utf-8")
        self.defects = {d["id"]: d for d in S.ledger_defects()}
        self.blocking = {i for i, d in self.defects.items() if d["severity"] == "blocking"}
        self._text, self._ex, self._status, self._lmap, self._lint = {}, {}, {}, {}, {}

    def text(self, e):
        return self._text.setdefault(e["sid"], S.spec_text(e))

    def ex(self, e):
        if e["sid"] not in self._ex:
            self._ex[e["sid"]] = A1.extract(self.text(e))
        return self._ex[e["sid"]]

    def status(self, e):
        return self._status.setdefault(e["sid"], S.ledger_status(e))

    def lines_of(self, e, did):
        """Lines of the scored spec that the defect's original lines map to."""
        if e["sid"] not in self._lmap:
            self._lmap[e["sid"]] = S.line_map(self.orig, self.text(e)) if e["sid"] != "orig" else {i: [i] for i in range(1, len(self.orig.split("\n")) + 1)}
        out = set()
        for ln in self.defects[did]["spec_lines"]:
            out |= set(self._lmap[e["sid"]].get(ln, []))
        return out

    def lint(self, e):
        if e["sid"] not in self._lint:
            self._lint[e["sid"]] = S.reqlint.run_lint_text(self.text(e), ("REF", "PATH", "PHASE"))["findings"]
        return self._lint[e["sid"]]

    def lint_defects(self, e):
        """Defects whose lines a widened-lint finding sits on."""
        hit = set()
        for f in self.lint(e):
            ls = set(range(f["lines"][0], f["lines"][1] + 1))
            if f.get("other_lines"):
                ls |= set(range(f["other_lines"][0], f["other_lines"][1] + 1))
            for did in self.defects:
                if self.lines_of(e, did) & ls:
                    hit.add(did)
        return hit


def load_out(seam, sid):
    p = OUT / seam / f"{sid}.json"
    return json.loads(p.read_text()) if p.exists() else None


# ----------------------------------------------------------------------------- A1: relevant pairs
_P_GATE = re.compile(r"\bP([0-4])\b(?=\s+(?:gate|scope|Commands|row|check|rows)\b)")
_P_GATE2 = re.compile(r"(?:phase|Phase)\s+([0-4])\b")


def defect_text(d):
    return " ".join([d["title"], d["quote"], d["what_goes_wrong"], d.get("is_fixed_when", "")])


def _ids_in(t, ex):
    obl_ids = {o["id"] for o in ex["obligations"]}
    crit_ids = {c["id"] for c in ex["criteria"]}
    o = {f"WC-{n}" for n in re.findall(r"\bWC-(\d+)\b", t)} | {f"SA-{n}" for n in re.findall(r"\bSA-(\d+)\b", t)}
    o |= {f"D{n}" for n in re.findall(r"(?<![\w-])D([1-5])\b", t)}
    o |= {f"cmd:{n}" for n in S.commands_in(t)}
    c = set(re.findall(r"\bAC-C\d\b", t)) | set(re.findall(r"\bAC-\d\.\d\b", t))
    c |= {f"7.2#{n}" for n in re.findall(r"\bstep\s+(\d)\b", t)}
    c |= {f"GATE:P{n}" for n in _P_GATE.findall(t)}
    return o & obl_ids, c & crit_ids


def defect_pairs(d, ex, mode="sentence"):
    """-> (set of pair ids, obligation ids, criterion ids) relevant to defect d in a spec with extraction ex.

    mode 'sentence' (PRIMARY): a pair is relevant when an obligation id and a criterion id are named in the same sentence / clause of the defect
    (title, quote, each sentence of what_goes_wrong and is_fixed_when).  mode 'product' (LOOSE, reported beside it): every obligation id named
    anywhere in the defect text x every criterion id named anywhere in it."""
    parts = [d["title"], d["quote"]]
    for fld in ("what_goes_wrong", "is_fixed_when"):
        parts += [x for x in re.split(r"(?<=[.;])\s+(?=[A-Z`(])", d.get(fld, "")) if x.strip()]
    O, C = set(), set()
    pairs = set()
    for t in parts:
        o, c = _ids_in(t, ex)
        O |= o
        C |= c
        if mode == "sentence":
            pairs |= {f"{a}|{b}" for a in o for b in c}
    if mode == "product":
        pairs = {f"{a}|{b}" for a in O for b in C}
    return pairs, O, C


def rel_pairs(ctx, e, mode="sentence"):
    """{defect id: set(pair ids)} for one spec, and the unpairable defects."""
    ex = ctx.ex(e)
    rel, unp = {}, []
    for did, d in ctx.defects.items():
        ps, o, c = defect_pairs(d, ex, mode)
        rel[did] = ps
        if not ps:
            unp.append(did)
    return rel, unp


def a1_recall(ctx, dec, mode="sentence"):
    classes = {"T1": T1, "T1+T2": T1 + T2, "all44": list(ctx.defects)}
    cap = dec["caps"]["a1_pairs"]
    res = {"cap": cap, "classes": {}, "by_defect": {}, "per_spec": {}}
    emitted_by = {}
    for e in ctx.specs:
        bp = A1.build_pairs(ctx.ex(e), None, cap)
        emitted_by[e["sid"]] = {p["id"] for p in bp["pairs"]}
        res["per_spec"][e["sid"]] = {"raw": bp["raw"], "eligible": bp["eligible"], "emitted": len(bp["pairs"])}
    for cname, ids in classes.items():
        agg = {"residual_cells": {"rel": 0, "hit": 0, "cells": 0, "cells_hit": 0}, "all_cells": {"rel": 0, "hit": 0, "cells": 0, "cells_hit": 0}}
        for e in ctx.specs:
            rel, _ = rel_pairs(ctx, e, mode)
            st = ctx.status(e)
            for did in ids:
                rp = rel[did]
                if not rp:
                    continue
                hit = len(rp & emitted_by[e["sid"]])
                for key, cond in (("all_cells", True), ("residual_cells", S.is_residual(st.get(did, "PRESENT")))):
                    if cond:
                        a = agg[key]
                        a["rel"] += len(rp)
                        a["hit"] += hit
                        a["cells"] += 1
                        a["cells_hit"] += 1 if hit else 0
        for key, a in agg.items():
            a["pair_recall"] = round(a["hit"] / a["rel"], 3) if a["rel"] else None
            a["defect_recall"] = round(a["cells_hit"] / a["cells"], 3) if a["cells"] else None
        res["classes"][cname] = agg
    # by defect over residual cells of the 12 finals
    ex0 = ctx.ex(ctx.specs[0])
    for did in ctx.defects:
        rows = []
        for e in ctx.specs:
            rel, _ = rel_pairs(ctx, e, mode)
            if rel[did] and S.is_residual(ctx.status(e).get(did, "PRESENT")):
                rows.append((len(rel[did]), len(rel[did] & emitted_by[e["sid"]])))
        res["by_defect"][did] = {"residual_cells_pairable": len(rows), "rel": sum(r for r, _ in rows), "hit": sum(h for _, h in rows)}
    res["unpairable"] = sorted({d for e in ctx.specs for d in rel_pairs(ctx, e, mode)[1]} & set(T1 + T2)) if ctx.specs else []
    res["mode"] = mode
    res["emitted"] = emitted_by
    return res


def a1_recall_curve(ctx, caps=(60, 90, 120, 180, 250, 400)):
    """Recall of the T1 residual cells at larger caps (what the cap would have to be); pair-level and defect-cell level."""
    curve = {}
    for cap in caps:
        rel_n = hit_n = cells = cells_hit = 0
        for e in ctx.specs:
            em = {p["id"] for p in A1.build_pairs(ctx.ex(e), None, cap)["pairs"]}
            rel, _ = rel_pairs(ctx, e)
            st = ctx.status(e)
            for did in T1:
                rp = rel[did]
                if rp and S.is_residual(st.get(did, "PRESENT")):
                    rel_n += len(rp)
                    hit_n += len(rp & em)
                    cells += 1
                    cells_hit += 1 if rp & em else 0
        curve[cap] = {"pair_recall": round(hit_n / rel_n, 3) if rel_n else None, "defect_cell_recall": round(cells_hit / cells, 3) if cells else None}
    return curve


# ----------------------------------------------------------------------------- A1: flags
def a1_flags(ctx, e, rec, outcomes=None):
    """Classify the flags of one spec file.  outcomes: list of outcome dicts (Jev or judge); returns dict of lists keyed by true/false/unmapped."""
    rel, _ = rel_pairs(ctx, e)
    st = ctx.status(e)
    ex_pairs = {p["id"]: p for p in rec["meta"]["pairs"]}
    # reproduce the hint ranking (cap 12) on the stored outcomes
    bp = {"pairs": [dict(id=pid, score=p["score"], signals=p["signals"], o={"id": pid.split("|")[0], "line": p["o_line"]}, c={"id": pid.split("|", 1)[1], "line": p["c_line"]})
                    for pid, p in ex_pairs.items()]}
    outs = outcomes if outcomes is not None else rec["answers"]
    hints = A1.make_hints(bp, outs, 12)
    non_sup = [o["id"].split(":a1:", 1)[1] for o in outs if o.get("usable") and o.get("choice") in ("partial", "unsupported", "contradicts_or_defers")]
    res = {"shown": {"true": [], "false": [], "unmapped": []}, "all_non_supported": {"true": [], "false": [], "unmapped": []}}
    d_of = lambda pid: [did for did, ps in rel.items() if pid in ps]
    def classify(pid):
        ds = d_of(pid)
        if not ds:
            return "unmapped", ds
        return ("true" if any(S.is_residual(st.get(d, "PRESENT")) for d in ds) else "false"), ds
    for h in hints:
        k, ds = classify(h["pair"])
        res["shown"][k].append({"pair": h["pair"], "label": h["label"], "defects": ds})
    for pid in non_sup:
        k, ds = classify(pid)
        res["all_non_supported"][k].append({"pair": pid, "defects": ds})
    res["hints"] = hints
    return res


def a1_gates(ctx, dec, judge_dir=None):
    g = dec["gates"]
    rec = a1_recall(ctx, dec)
    loose = a1_recall(ctx, dec, "product")
    out = {"recall": {k: v for k, v in rec.items() if k != "emitted"}, "recall_loose_product": {k: v for k, v in loose.items() if k not in ("emitted", "by_defect")},
           "recall_curve_T1_residual": a1_recall_curve(ctx), "specs": {}, "missing_replay": []}
    tot = collections.Counter()
    bey_total, bey_specs = set(), 0
    judge_cmp = collections.Counter()
    modes = set()
    for e in ctx.specs:
        r = load_out("a1", e["sid"])
        if not r:
            out["missing_replay"].append(e["sid"])
            continue
        modes.add(r.get("mode"))
        fl = a1_flags(ctx, e, r)
        st = ctx.status(e)
        rel, _ = rel_pairs(ctx, e)
        # the keyword control needs the pair texts: recompute the (deterministic) prefilter from the spec
        bp = A1.build_pairs(ctx.ex(e), None, dec["caps"]["a1_pairs"])
        kw = {k["pair"] for k in A1.keyword_flags(bp)}
        kw_def = {d for d, ps in rel.items() if ps & kw}
        lint_def = ctx.lint_defects(e)
        jev_def = {d for x in fl["shown"]["true"] for d in x["defects"]}
        beyond = sorted(d for d in jev_def if d in ctx.blocking and S.is_residual(st.get(d, "PRESENT")) and d not in kw_def and d not in lint_def)
        rec_e = {"mode": r.get("mode"), "calls": r["counts"]["calls"], "usable": r["counts"]["usable"], "fallbacks": len(r["fallbacks"]),
                 "shown_hints": len(fl["hints"]), "shown_true": len(fl["shown"]["true"]), "shown_false": len(fl["shown"]["false"]), "shown_unmapped": len(fl["shown"]["unmapped"]),
                 "all_nonsup_false": len(fl["all_non_supported"]["false"]), "all_nonsup_unmapped": len(fl["all_non_supported"]["unmapped"]),
                 "beyond_control": beyond, "keyword_flag_defects": sorted(kw_def & ctx.blocking), "lint_defects_blocking": sorted(lint_def & ctx.blocking)}
        if judge_dir and (pathlib.Path(judge_dir) / f"{e['sid']}.answers.json").exists():
            ans = json.loads((pathlib.Path(judge_dir) / f"{e['sid']}.answers.json").read_text())
            jo = []
            for a in r["answers"]:
                c = ans.get(a["id"])
                ok = c in A1.SUPPORT_OPTIONS
                jo.append({"id": a["id"], "usable": bool(ok and c != "insufficient"), "choice": c if ok else None})
            jf = a1_flags(ctx, e, r, jo)
            jdef = {d for x in jf["shown"]["true"] for d in x["defects"]}
            jb = sorted(d for d in jdef if d in ctx.blocking and S.is_residual(st.get(d, "PRESENT")) and d not in kw_def and d not in lint_def)
            rec_e["judge"] = {"shown_true": len(jf["shown"]["true"]), "shown_false": len(jf["shown"]["false"]), "beyond_control": jb,
                              "jev_only": sorted(set(beyond) - set(jb)), "judge_only": sorted(set(jb) - set(beyond))}
            judge_cmp["jev_only"] += len(rec_e["judge"]["jev_only"])
            judge_cmp["judge_only"] += len(rec_e["judge"]["judge_only"])
            judge_cmp["jev_false"] += rec_e["shown_false"]
            judge_cmp["judge_false"] += rec_e["judge"]["shown_false"]
        out["specs"][e["sid"]] = rec_e
        tot["false"] += rec_e["shown_false"]
        bey_total |= {(e["sid"], d) for d in beyond}
        bey_specs += 1 if beyond else 0
    sp = out["specs"]
    fin = [v for k, v in sp.items() if k != "orig"]
    out["summary"] = {
        "modes": sorted(m for m in modes if m), "specs_replayed": len(sp),
        "false_flags_per_spec": {"max": max([v["shown_false"] for v in fin], default=None), "mean": round(sum(v["shown_false"] for v in fin) / len(fin), 2) if fin else None,
                                 "max_incl_unmapped_bound": max([v["shown_false"] + v["shown_unmapped"] for v in fin], default=None)},
        "beyond_control": {"cells": len(bey_total), "specs_with_one_or_more": bey_specs, "defects": sorted({d for _, d in bey_total})},
        "judge_compare": dict(judge_cmp) if judge_cmp else None,
    }
    rr = rec["classes"]["T1"]["residual_cells"]["pair_recall"]
    verdict = {
        "recall_pair_level_ge_70": None if rr is None else rr >= g["a1_recall_min"],
        "recall_defect_cell_level_ge_70": None if rec["classes"]["T1"]["residual_cells"]["defect_recall"] is None else rec["classes"]["T1"]["residual_cells"]["defect_recall"] >= g["a1_recall_min"],
        "false_flags_le_8": None if out["summary"]["false_flags_per_spec"]["max"] is None else out["summary"]["false_flags_per_spec"]["max"] <= g["a1_false_flags_max"],
        "beyond_control_ge_1": None if not sp else len(bey_total) >= 1,
        "not_tied_by_judge": None if not judge_cmp else (judge_cmp["jev_only"] > judge_cmp["judge_only"] or
                                                          (judge_cmp["jev_only"] == judge_cmp["judge_only"] and judge_cmp["jev_false"] + 2 <= judge_cmp["judge_false"])),
    }
    out["verdict"] = verdict
    out["mock_warning"] = "MOCK replay: flags below are plumbing only, not evidence" if "mock" in modes else None
    return out


# ----------------------------------------------------------------------------- A2
def a2_gates(ctx, dec, judge_dir=None):
    out = {"specs": {}, "missing_replay": []}
    tail_caught, tail_caught_cells, ctrl_caught_cells, miss_cells = set(), 0, 0, 0
    false_rows = 0
    jt = {"jev_only_tail": set(), "judge_only_tail": set(), "judge_false_rows": 0, "specs": 0}
    modes = set()
    for e in ctx.specs:
        r = load_out("a2", e["sid"])
        if not r:
            out["missing_replay"].append(e["sid"])
            continue
        modes.add(r.get("mode"))
        st = ctx.status(e)
        analysis = r["meta"]["analysis"]
        by_ans = {a["id"].split(":a2:", 1)[1]: a for a in r["answers"]}
        rows = []
        for a in analysis:
            ds = [d for d in ctx.defects if a["line"] in ctx.lines_of(e, d)]
            ctrl = sorted({f["source"] + ":" + f["check"] for f in a["code_flags"]})
            ans = by_ans.get(a["id"])
            jev = ans["choice"] if ans and ans.get("usable") else None
            rows.append({"row": a["id"], "line": a["line"], "defects": ds, "residual_defects": [d for d in ds if S.is_residual(st.get(d, "PRESENT"))], "control_flags": ctrl,
                         "jev": jev, "jev_flag": jev in ("cannot_pass", "cannot_discriminate")})
        # per-defect: caught by controls (any control flag on a row that maps to it), caught by Jev beyond controls
        cls = {}
        for did in A2_CLASS:
            resid = S.is_residual(st.get(did, "PRESENT"))
            on_rows = [x for x in rows if did in x["defects"]]
            ctrl = any(x["control_flags"] for x in on_rows)
            jev = any(x["jev_flag"] for x in on_rows)
            cls[did] = {"residual": resid, "rows": [x["row"] for x in on_rows], "control_caught": ctrl, "jev_caught": jev, "jev_beyond_control": bool(resid and jev and not ctrl)}
            if resid:
                ctrl_caught_cells += 1 if ctrl else 0
                if jev and not ctrl:
                    tail_caught_cells += did in A2_TAIL
                    if did in A2_TAIL:
                        tail_caught.add(did)
        jp = pathlib.Path(judge_dir or OUT / "a2" / "control") / f"{e['sid']}.answers.json"
        if jp.exists():                                          # same-packet conventional judge: same rows, same metrics
            ans = json.loads(jp.read_text())
            jrow = {}
            for a in r["answers"]:
                c = ans.get(a["id"])
                if c in ("cannot_pass", "cannot_discriminate"):
                    jrow[a["id"].split(":a2:", 1)[1]] = c
            jt["specs"] += 1
            for did in A2_TAIL:
                on_rows = [x for x in rows if did in x["defects"]]
                if not S.is_residual(st.get(did, "PRESENT")) or any(x["control_flags"] for x in on_rows):
                    continue
                jj = any(x["row"] in jrow for x in on_rows)
                vv = any(x["jev_flag"] for x in on_rows)
                if vv and not jj:
                    jt["jev_only_tail"].add(did)
                if jj and not vv:
                    jt["judge_only_tail"].add(did)
            jt["judge_false_rows"] += sum(1 for rid in jrow if not next(x for x in rows if x["row"] == rid)["residual_defects"])
        flagged_rows = [x for x in rows if x["jev_flag"]]
        fr = [x["row"] for x in flagged_rows if not x["residual_defects"]]
        false_rows += len(fr)
        out["specs"][e["sid"]] = {"mode": r.get("mode"), "rows": len(rows), "to_jev": r["meta"]["to_jev"], "code_flagged_rows": r["meta"]["code_flagged"], "usable": r["counts"]["usable"],
                                  "fallbacks": len(r["fallbacks"]), "lines": r["lines"], "jev_flagged_rows": [x["row"] for x in flagged_rows],
                                  "jev_flagged_rows_without_residual_defect": fr, "class": cls, "table": rows}
    g = dec["gates"]
    out["summary"] = {"modes": sorted(m for m in modes if m), "tail_defects_caught_beyond_controls": sorted(tail_caught), "n_tail_defects_caught": len(tail_caught),
                      "tail_cells_caught": tail_caught_cells, "jev_flags_on_rows_without_residual_defect": false_rows,
                      "note_false": "rows with no residual mapped defect are an UPPER BOUND on false flags (a row can be flawed with no ledger defect); the kill rule needs independent row labels (not available)"}
    out["verdict"] = {"tail_catch_ge_3": None if not out["specs"] else len(tail_caught) >= g["a2_tail_catch_min"]}
    if jt["specs"]:
        out["judge_compare"] = {"specs_with_judge_answers": jt["specs"], "jev_only_tail": sorted(jt["jev_only_tail"]), "judge_only_tail": sorted(jt["judge_only_tail"]),
                                "jev_flags_on_rows_without_residual_defect": false_rows, "judge_flags_on_rows_without_residual_defect": jt["judge_false_rows"]}
        out["verdict"]["not_tied_by_judge"] = len(jt["jev_only_tail"]) > len(jt["judge_only_tail"])
    out["mock_warning"] = "MOCK replay: flags below are plumbing only, not evidence" if "mock" in modes else None
    return out


# ----------------------------------------------------------------------------- A3 separation test
def fisher_two_sided(a, b, c, d):
    """Exact two-sided p of the 2x2 table [[a,b],[c,d]]."""
    n = a + b + c + d
    r1, c1 = a + b, a + c
    def p(x):
        return math.comb(r1, x) * math.comb(n - r1, c1 - x) / math.comb(n, c1)
    p0 = p(a)
    return round(sum(p(x) for x in range(max(0, c1 - (n - r1)), min(r1, c1) + 1) if p(x) <= p0 + 1e-12), 4)


def a3_gates(ctx, dec):
    d = A3.load_pn1_cases()
    cases = d["cases"]
    jev = {}
    modes = set()
    for e in ctx.specs:
        r = load_out("a3", e["sid"])
        if not r:
            continue
        modes.add(r.get("mode"))
        for a in r["answers"]:
            jev[a["id"].split(":a3:")[0]] = a
    labels_p = OUT / "a3" / "labels.json"                       # optional: blind labeller output {case_id: different_mechanism|same_mechanism|v2_changed_nothing_relevant}
    labels = json.loads(labels_p.read_text()) if labels_p.exists() else {}
    rows = []
    for c in cases:
        a = jev.get(c["case_id"])
        label = a["choice"] if a and a.get("usable") else None
        rows.append({"case": c["case_id"], "outcome": c["outcome"], "jev": label, "blind_label": labels.get(c["case_id"]), "v1_named_not_touched": c["controls"]["v1_named_not_touched"],
                     "v2_named_not_touched": c["controls"]["v2_named_not_touched"], "v2_changed_on_v1_lines": c["controls"]["v2_changed_on_v1_lines"],
                     "v2_overlap_ge_50": c["controls"]["v2_overlap_ge_50"], "span_overlap": c["analysis"]["span_overlap"]})
    # control-undecided = the controls (named_not_touched, known after V2, the favourable-to-control reading) do not mark the case
    und = [x for x in rows if not x["v2_named_not_touched"] and not x["v1_named_not_touched"]]
    res_l = [x["jev"] for x in und if x["outcome"] == "resolved"]
    fail_l = [x["jev"] for x in und if x["outcome"] == "failed"]
    answered = all(x["jev"] for x in und) and bool(und)
    sep = bool(answered and res_l and fail_l and not (set(res_l) & set(fail_l)))
    # 2x2 over all cases: Jev 'new_aspect' vs outcome resolved
    def tab(pred):
        a_ = sum(1 for x in rows if pred(x) and x["outcome"] == "resolved")
        b_ = sum(1 for x in rows if pred(x) and x["outcome"] == "failed")
        c_ = sum(1 for x in rows if not pred(x) and x["outcome"] == "resolved")
        d_ = sum(1 for x in rows if not pred(x) and x["outcome"] == "failed")
        return {"table": [[a_, b_], [c_, d_]], "fisher_p": fisher_two_sided(a_, b_, c_, d_)}
    out = {"report": d["report"], "cases": rows, "control_undecided_cases": [x["case"] for x in und],
           "resolved_labels": res_l, "failed_labels": fail_l,
           "separation": {"jev_separates_resolved_from_failed_among_control_undecided": sep, "answered_all": answered},
           "predictor_tables": {"jev_new_aspect_vs_resolved": tab(lambda x: x["jev"] == "new_aspect"),
                                "v2_named_not_touched_vs_failed": tab(lambda x: not x["v2_named_not_touched"]),
                                "v2_overlap_ge_50_vs_failed": tab(lambda x: not x["v2_overlap_ge_50"])},
           "modes": sorted(m for m in modes if m)}
    out["verdict"] = {"keep_a3": sep if jev else None}
    out["mock_warning"] = "MOCK replay: labels are plumbing only, not evidence" if "mock" in modes else None
    return out


# ----------------------------------------------------------------------------- triage (a)/(b)/(c)
def _gid_defects():
    L = S.ledger_defects()
    gid2d = collections.defaultdict(set)
    chunks = {}
    for p in (S.SP / "p17" / "out").glob("chunk-*.json"):
        c = json.loads(p.read_text())
        for d in c["defects"]:
            chunks[d["local_id"]] = d["gids"]
    for d in L:
        for src in d["sources"]:
            for g in chunks.get(src, []):
                gid2d[g].add(d["id"])
    return gid2d


def triage(ctx, classes=("T1",)):
    """Sort the residual cells of the 12 finals into (a) raised and in the V1 brief, (b) raised but rejected (VF/ADJ), (c) never raised as a blocking finding."""
    gid2d = _gid_defects()
    rows = [json.loads(l) for l in (S.SP / "p17" / "findings.jsonl").read_text().splitlines()]
    first, audit = collections.defaultdict(list), collections.defaultdict(list)
    for r in rows:                                   # run names repeat across arms (b1-r3 exists in ab1 and pn1): always key by (arm, run)
        (first if r["kind"] == "first" else audit)[(r["arm"], r["run"])].append(r)
    res = {"definition": {"a": "a first-review blocking finding of this run that maps to the defect was confirmed (ab4: VF-confirmed Mn in the reviser brief; PN1: the merged finding is in the round-1 brief)",
                          "b": "raised in this run's first review as a blocking finding but rejected (ab4: VF reject / not in the brief; PN1: not in the round-1 brief)",
                          "c": "no first-review blocking finding of this run maps to the defect (non-blocking mentions are not in findings.jsonl and cannot be recovered)"},
           "cells": [], "unrecoverable": []}
    for e in ctx.specs:
        if e["arm"] not in ("ab4", "pn1"):
            continue
        run = e["run"]
        status = ctx.status(e)
        if e["arm"] == "ab4":
            rev = S.SP / "p16" / "ab4" / "runs" / run / "ws" / ".dev" / "orca-command-refactor" / "review"
            verdict = {}
            if (rev / "verify-1.md").exists() and (rev / "findings-1.md").exists():
                fm = {}
                for m in re.finditer(r"^#### (M\d+)\.(\w+) \((round1-[ab]\.md) (\S+)\)", (rev / "findings-1.md").read_text(), re.M):
                    fm[(m.group(3), m.group(4))] = m.group(1)
                vv = {}
                r1 = (rev / "round1.md").read_text() if (rev / "round1.md").exists() else ""
                mm = re.search(r"confirmed blocking ids:\s*([^.\n]*)", r1)          # the coordinator's own record of the VF outcome
                if mm:
                    conf = set(re.findall(r"M\d+", mm.group(1)))
                    vv = {m: ("confirm" if m in conf else "reject") for m in set(fm.values())}
                else:
                    for m in re.finditer(r"^\|\s*(M\d+)\b[^\n]*\|\s*(confirm|reject)\w*\s*\|", (rev / "verify-1.md").read_text(), re.M):
                        vv[m.group(1)] = m.group(2)
                verdict = {k: vv.get(v) for k, v in fm.items()}
            else:
                res["unrecoverable"].append(f"{run}: no findings-1.md / verify-1.md")
            stepfile = {"r1a": "round1-a.md", "r1b": "round1-b.md"}
        else:
            led_p = next((S.SP / "p13" / "ab1" / "runs" / run / "ws" / ".dev").glob("*/review/ledger.json"), None)
            led = json.loads(led_p.read_text()) if led_p else None
            brief1 = set(led["rounds"][0]["brief_ids"]) if led else set()
        for did in ctx.defects:
            if did not in T1 and ("T1+T2" not in classes or did not in T2):
                continue
            if not S.is_residual(status.get(did, "PRESENT")):
                continue
            raised = [r for r in first.get((e["arm"], run), []) if did in gid2d.get(r["gid"], ())]
            audit_hit = [r["step"] + ":" + r["fid"] for r in audit.get((e["arm"], run), []) if did in gid2d.get(r["gid"], ())]
            if not raised:
                cls = "c"
                why = []
            else:
                acc, rej = [], []
                for r in raised:
                    if e["arm"] == "ab4":
                        v = verdict.get((stepfile.get(r["step"]), r["fid"]))
                        (acc if v == "confirm" else rej).append(r["fid"] + ":" + str(v))
                    else:
                        (acc if r["fid"] in brief1 else rej).append(r["fid"])
                cls = "a" if acc else "b"
                why = acc or rej
            res["cells"].append({"sid": e["sid"], "arm": e["arm"], "run": run, "defect": did, "blocking": did in ctx.blocking, "class": cls, "findings": why, "frozen_audit_raised": audit_hit})
    agg = collections.Counter((c["arm"], c["class"]) for c in res["cells"])
    res["counts"] = {f"{a}_{k}": v for (a, k), v in sorted(agg.items())}
    res["total"] = dict(collections.Counter(c["class"] for c in res["cells"]))
    res["n_cells"] = len(res["cells"])
    blk = collections.Counter(c["class"] for c in res["cells"] if c["blocking"])
    res["blocking_only"] = dict(blk)
    nspec = collections.defaultdict(lambda: collections.Counter())
    for c in res["cells"]:
        nspec[c["sid"]][c["class"]] += 1
    res["c_cells_also_raised_by_the_runs_frozen_audits"] = sum(1 for c in res["cells"] if c["class"] == "c" and c["frozen_audit_raised"])
    res["per_spec_c"] = {sid: v.get("c", 0) for sid, v in nspec.items()}
    res["c_per_spec_mean"] = round(sum(v.get("c", 0) for v in nspec.values()) / max(len(nspec), 1), 2)
    res["c_blocking_per_spec_mean"] = round(sum(1 for c in res["cells"] if c["class"] == "c" and c["blocking"]) / max(len({c["sid"] for c in res["cells"]}), 1), 2)
    return res


# ----------------------------------------------------------------------------- reports
def md_a1(g):
    s = g["summary"]
    L = ["# A1 gates", ""]
    if g.get("mock_warning"):
        L += [f"**{g['mock_warning']}**", ""]
    r = g["recall"]
    L += ["## Prefilter recall (code only, independent of Jev)", "", f"cap {r['cap']} pairs per spec", ""]
    L += ["| class | cells (residual) | relevant pairs | emitted | pair recall | defect-cell recall | pair recall (all cells) |", "|---|---|---|---|---|---|---|"]
    for k, v in r["classes"].items():
        a, b = v["residual_cells"], v["all_cells"]
        L.append(f"| {k} | {a['cells']} | {a['rel']} | {a['hit']} | {a['pair_recall']} | {a['defect_recall']} | {b['pair_recall']} |")
    L += ["", f"unpairable defects (a side of the pair is empty): {r['unpairable']}", "", f"recall at larger caps (T1, residual cells): {json.dumps(g['recall_curve_T1_residual'])}", "",
          "Loose definition (every named obligation x every named criterion of the defect text):", "",
          "| class | cells (residual) | relevant pairs | emitted | pair recall | defect-cell recall |", "|---|---|---|---|---|---|"]
    for k, v in g["recall_loose_product"]["classes"].items():
        a = v["residual_cells"]
        L.append(f"| {k} | {a['cells']} | {a['rel']} | {a['hit']} | {a['pair_recall']} | {a['defect_recall']} |")
    L.append("")
    L += ["## Flags per spec (shown hints, cap 12)", "", "| spec | usable | fallbacks | shown | true | false | unmapped | beyond-control catches |", "|---|---|---|---|---|---|---|---|"]
    for sid, v in g["specs"].items():
        L.append(f"| {sid} | {v['usable']} | {v['fallbacks']} | {v['shown_hints']} | {v['shown_true']} | {v['shown_false']} | {v['shown_unmapped']} | {','.join(v['beyond_control']) or '-'} |")
    L += ["", f"summary: {json.dumps(s)}", f"verdict: {json.dumps(g['verdict'])}", ""]
    return "\n".join(L)


def md_a2(g):
    L = ["# A2 gates (lint-first table)", ""]
    if g.get("mock_warning"):
        L += [f"**{g['mock_warning']}**", ""]
    L += ["| spec | rows | code-flagged | to Jev | usable | Jev-flagged rows | Jev-flagged rows with no residual defect |", "|---|---|---|---|---|---|---|"]
    for sid, v in g["specs"].items():
        L.append(f"| {sid} | {v['rows']} | {v['code_flagged_rows']} | {v['to_jev']} | {v['usable']} | {len(v['jev_flagged_rows'])} | {len(v['jev_flagged_rows_without_residual_defect'])} |")
    L += ["", f"summary: {json.dumps(g['summary'])}", f"judge compare: {json.dumps(g.get('judge_compare'))}", f"verdict: {json.dumps(g['verdict'])}", ""]
    if g["specs"]:
        sid = next(iter(g["specs"]))
        L += [f"## Row table for {sid}", "", "| row | line | mapped defects | control flags | Jev |", "|---|---|---|---|---|"]
        for x in g["specs"][sid]["table"]:
            L.append(f"| {x['row']} | {x['line']} | {','.join(x['defects']) or '-'} | {','.join(x['control_flags']) or '-'} | {x['jev'] or '-'} |")
    return "\n".join(L) + "\n"


def md_a3(g):
    L = ["# A3 separation test", ""]
    if g.get("mock_warning"):
        L += [f"**{g['mock_warning']}**", ""]
    L += [f"reconstruction: {json.dumps(g['report'])}", "", "| case | outcome (hidden from Jev) | Jev label | V1 named_not_touched | V2 named_not_touched (post-V2 control) | V2-changed on V1 lines | span overlap |", "|---|---|---|---|---|---|---|"]
    for x in g["cases"]:
        L.append(f"| {x['case']} | {x['outcome']} | {x['jev'] or '-'} | {x['v1_named_not_touched']} | {x['v2_named_not_touched']} | {x['v2_changed_on_v1_lines']} | {x['span_overlap']} |")
    L += ["", f"control-undecided cases: {g['control_undecided_cases']}", f"resolved labels {g['resolved_labels']} / failed labels {g['failed_labels']}",
          f"separation: {json.dumps(g['separation'])}", f"predictor tables: {json.dumps(g['predictor_tables'])}", f"verdict: {json.dumps(g['verdict'])}", ""]
    return "\n".join(L)


def md_triage(t):
    L = ["# Triage of residual cells (Opus-J1 test)", "", f"cells: {t['n_cells']}  counts: {json.dumps(t['counts'])}  total: {json.dumps(t['total'])}", f"blocking only: {json.dumps(t['blocking_only'])}",
         f"(c) per spec mean {t['c_per_spec_mean']}; (c) blocking per spec mean {t['c_blocking_per_spec_mean']}", "", "Definitions:"]
    L += [f"- ({k}) {v}" for k, v in t["definition"].items()]
    L += ["", f"not recoverable: {json.dumps(t['unrecoverable'])}", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seam", choices=["a1", "a2", "a3", "triage", "all"], required=True)
    ap.add_argument("--specs")
    ap.add_argument("--judge-dir", help="dir with <sid>.answers.json from the same-packet conventional judge (A1/A2)")
    ap.add_argument("--classes", default="T1", help="triage classes: T1 or T1+T2")
    a = ap.parse_args(argv)
    dec = S.decision()
    ctx = Ctx(set(a.specs.split(",")) if a.specs else None)
    todo = ["a1", "a2", "a3", "triage"] if a.seam == "all" else [a.seam]
    for sm in todo:
        if sm == "a1":
            g = a1_gates(ctx, dec, a.judge_dir or (OUT / "a1" / "control"))
            md = md_a1(g)
        elif sm == "a2":
            g = a2_gates(ctx, dec, a.judge_dir)
            md = md_a2(g)
        elif sm == "a3":
            g = a3_gates(ctx, dec)
            md = md_a3(g)
        else:
            g = triage(ctx, tuple(a.classes.split(",")))
            md = md_triage(g)
        d = OUT / sm
        S.write_json(d / "gates.json", g)
        (d / "GATES.md").write_text(md)
        print(f"{sm}: wrote {d / 'gates.json'}")
        if sm == "triage":
            print(f"  cells {g['n_cells']} total {g['total']} blocking {g['blocking_only']}")
        else:
            print(f"  verdict {g.get('verdict')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
