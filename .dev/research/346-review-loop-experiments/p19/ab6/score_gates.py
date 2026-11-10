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
import a2_observability as A2

OUT = S.SEAMS / "out"
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


_P_GATE = re.compile(r"\bP([0-4])\b(?=\s+(?:gate|scope|Commands|row|check|rows)\b)")
_P_GATE2 = re.compile(r"(?:phase|Phase)\s+([0-4])\b")


















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






# ----------------------------------------------------------------------------- triage (a)/(b)/(c)




# ----------------------------------------------------------------------------- reports


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






def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seam", choices=["a2"], required=True)
    ap.add_argument("--specs")
    ap.add_argument("--judge-dir", help="dir with <sid>.answers.json from the same-packet conventional judge (A2)")
    a = ap.parse_args(argv)
    dec = S.decision()
    ctx = Ctx(set(a.specs.split(",")) if a.specs else None)
    for sm in ["a2"]:
        g = a2_gates(ctx, dec, a.judge_dir)
        md = md_a2(g)
        d = OUT / sm
        S.write_json(d / "gates.json", g)
        (d / "GATES.md").write_text(md)
        print(f"{sm}: wrote {d / 'gates.json'}")
        print(f"  verdict {g.get('verdict')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
