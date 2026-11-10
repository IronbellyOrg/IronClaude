#!/usr/bin/env python3
"""A3 revision-novelty seam (ab6).  Asked after an R2 FAIL and BEFORE V2 (the V2 revision does not exist yet), about the V1 attempt.

For each surviving blocker (in the V1 brief and again in the R2 brief) code computes, from the V1 diff and the review texts only:
  touched_v1       a V1 hunk overlaps the lines the first review quoted for the blocker (old-spec coordinates);
  named_not_touched  the blocker was recorded as applied by V1 but no V1 hunk touches its quoted lines;
  span_overlap     share of the quoted lines (old coordinates) that V1 changed;
  r2_on_v1_lines   share of the lines the R2 report quotes (V1-output coordinates) that V1 wrote.
Only touched blockers go to Jev, question `v1_attempt` {new_aspect, same_restated, no_relevant_change, insufficient}.
Output: one flag line per blocker (code line for named_not_touched, Jev line otherwise); error / refusal / `insufficient` = no Jev line.

Also here: the loader of the 10 PN1 survivor cases (`load_pn1_cases`), their blind label packets and the post-V2 control predictors used by the
separation test in score_gates.py.   CLI:  a3_novelty.py --pn1 [--mock MODE] [--out DIR]
"""
import argparse
import difflib
import glob
import json
import pathlib
import re
import sys

import seamlib as S

QSET_VERSION = "a3-q1"
QNAME = "v1_attempt"
RUNS_ROOT = S.SP / "p13" / "ab1" / "runs"
PN1_SID = {"b1-r1": "s62", "b1-r2": "s47", "b1-r3": "s25", "b1-r4": "s35", "b1-r5": "s66", "b1-r6": "s33"}

ATTEMPT_OPTIONS = {
    "new_aspect": "The second review raises an aspect of the defect that the first revision did not address: a different sentence, rule, command or "
                  "condition than the text the first revision rewrote.",
    "same_restated": "The second review restates the same defect the first revision tried to fix: the revision changed the quoted text but the defect "
                     "remains, or it was only reworded.",
    "no_relevant_change": "The first revision's edits do not bear on this finding: they changed other text, or nothing in the text the finding quotes.",
    "insufficient": "The state does not contain what is needed to decide between the other options.",
}
ATTEMPT_INSTRUCTIONS = (
    "`blocker` is a review finding that the first revision was asked to fix and that the second review raised again. `first_revision_hunks` are the "
    "edits the first revision made around the text the first review quoted (before and after). `second_review` is what the second review wrote about "
    "the finding. Decide how the second review relates to the first revision's attempt. Judge only from the state."
)


def attempt_question():
    return S.choice(ATTEMPT_INSTRUCTIONS, ATTEMPT_OPTIONS)


# ----------------------------------------------------------------------------- text and diff helpers
def norm(s: str) -> str:
    s = re.sub(r"\\+", r"\\", s or "")                   # reports double the backslashes of the spec text
    return " ".join(re.sub(r"[`*]", "", s).split()).lower()


def locate(anchor: str, lines: list) -> list:
    """1-based line numbers of `lines` containing the (normalised) anchor text; [] when it cannot be found."""
    a = norm(anchor.strip().strip('"'))
    if len(a) < 12:
        return []
    hits = [i + 1 for i, ln in enumerate(lines) if a in norm(ln)]
    if hits:
        return hits[:3]
    # anchors quoted with an ellipsis: match the longest piece
    pieces = [p.strip() for p in re.split(r"\.\.\.|…", a) if len(p.strip()) >= 20]
    for p in sorted(pieces, key=len, reverse=True):
        hits = [i + 1 for i, ln in enumerate(lines) if p in norm(ln)]
        if hits:
            return hits[:3]
    return []


def hunks(old_lines: list, new_lines: list) -> list:
    """[{old:(a,b), new:(c,d), tag}] for every non-equal opcode (1-based inclusive; an empty side is (a, a-1))."""
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes():
        if tag != "equal":
            out.append({"tag": tag, "old": (i1 + 1, i2), "new": (j1 + 1, j2)})
    return out


def _span(rng):
    return set(range(rng[0], rng[1] + 1)) if rng[1] >= rng[0] else set()


def changed_old(hs) -> set:
    return set().union(*[_span(h["old"]) for h in hs]) if hs else set()


def changed_new(hs) -> set:
    return set().union(*[_span(h["new"]) for h in hs]) if hs else set()


def touching(hs, lines: set) -> list:
    """Hunks whose old range covers a quoted line (a pure insertion at a quoted line counts as touching it)."""
    out = []
    for h in hs:
        s = _span(h["old"]) or {h["old"][0]}
        if s & lines or (not _span(h["old"]) and (h["old"][0] in lines or h["old"][0] - 1 in lines)):
            out.append(h)
    return out


# ----------------------------------------------------------------------------- review text parsing
_BLOCK_RE = re.compile(r"^### (L\d+)\s*$", re.M)
_SUB_RE = re.compile(r"^#### (L\d+)\.(\S+)\s+\(([^)]+)\)\s*$", re.M)


def parse_blocking(report_text: str) -> dict:
    """{lid: [{reviewer, fid, claim, anchor, anchor2}]} from the 'Blocking findings' section of a merged panel review (round1.md / round2.md)."""
    m = re.search(r"^## Blocking findings\s*$(.*?)(?=^## |\Z)", report_text, re.M | re.S)
    if not m:
        return {}
    body = m.group(1)
    out = {}
    heads = list(_SUB_RE.finditer(body))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        chunk = body[h.end():end]
        # a following '### Lk' heading ends the chunk
        nxt = _BLOCK_RE.search(chunk)
        if nxt:
            chunk = chunk[:nxt.start()]
        d = {"reviewer": h.group(2), "fid": h.group(3), "claim": "", "anchor": "", "anchor2": ""}
        for key in ("claim", "anchor", "anchor2"):
            mm = re.search(rf"^- {key}:\s*(.*)$", chunk, re.M)
            if mm:
                d[key] = mm.group(1).strip().strip('"')
        out.setdefault(h.group(1), []).append(d)
    return out


def r2_context(r2_text: str, lid: str, blocks=None) -> list:
    blocks = blocks if blocks is not None else parse_blocking(r2_text)
    return blocks.get(lid, [])


# ----------------------------------------------------------------------------- the code stage
def analyze(old_text: str, new_text: str, r2_text: str, blockers: list, applied_ids=None, r1_blocks=None) -> list:
    """V1 diff (old_text -> new_text) + the R2 report + the surviving blockers -> one analysis dict per blocker.

    blockers: [{lid, anchors: [str] (what the FIRST review quoted), claims: [str], refs: [str]}]; applied_ids: ids V1 recorded as applied (default: all)."""
    ol, nl = old_text.split("\n"), new_text.split("\n")
    hs = hunks(ol, nl)
    cn = changed_new(hs)
    r2_blocks = parse_blocking(r2_text)
    out = []
    for b in blockers:
        qlines = set()
        for a in b.get("anchors", []):
            qlines |= set(locate(a, ol))
        located = bool(qlines)
        th = touching(hs, qlines) if located else []
        touched = bool(th)
        applied = applied_ids is None or b["lid"] in applied_ids
        r2 = r2_context(r2_text, b["lid"], r2_blocks)
        r2lines = set()
        for d in r2:
            for a in (d.get("anchor", ""), d.get("anchor2", "")):
                if a:
                    r2lines |= set(locate(a, nl))
        out.append({
            "lid": b["lid"], "located": located, "quoted_lines": sorted(qlines), "touched_v1": touched if located else None,
            "named_not_touched": bool(applied and located and not touched),
            "span_overlap": round(len(qlines & changed_old(hs)) / len(qlines), 3) if located else None,
            "r2_on_v1_lines": round(len(r2lines & cn) / len(r2lines), 3) if r2lines else None,
            "n_hunks_touching": len(th), "hunks": th, "r2": r2, "refs": b.get("refs", []),
            "claims": b.get("claims", []), "to_jev": (touched or not located),
        })
    return out


def _hunk_texts(h, ol, nl, n=600):
    a, b = h["old"], h["new"]
    before = " ".join(ol[a[0] - 1:a[1]]) if a[1] >= a[0] else "(nothing: a pure insertion)"
    after = " ".join(nl[b[0] - 1:b[1]]) if b[1] >= b[0] else "(nothing: the text was deleted)"
    return {"before": S.scrub(S.clip(S.plain(before), n)), "after": S.scrub(S.clip(S.plain(after), n))}


def packet_state(an: dict, old_text: str, new_text: str) -> dict:
    ol, nl = old_text.split("\n"), new_text.split("\n")
    top = sorted(an["hunks"], key=lambda h: -len(_span(h["old"]) & set(an["quoted_lines"])))[:4]
    return {
        "blocker": {"id": an["lid"], "first_review_claims": [S.scrub(S.clip(c, 400)) for c in an.get("claims", [])[:4]]},
        "first_revision_hunks": [_hunk_texts(h, ol, nl) for h in top],
        "second_review": [{"claim": S.scrub(S.clip(d.get("claim", ""), 400)), "quotes": [S.scrub(S.clip(d[k], 300)) for k in ("anchor", "anchor2") if d.get(k)]}
                          for d in an["r2"][:5]],
        "code_facts": {"first_revision_touched_quoted_text": "yes" if an["touched_v1"] else "not determined" if an["touched_v1"] is None else "no",
                       "share_of_quoted_lines_changed_by_first_revision": an["span_overlap"] if an["span_overlap"] is not None else "unknown",
                       "second_review_quotes_on_lines_the_first_revision_wrote": an["r2_on_v1_lines"] if an["r2_on_v1_lines"] is not None else "unknown"},
    }


def build_items(analyses, old_text, new_text, sid="case"):
    items = []
    for an in analyses:
        if an["to_jev"]:
            items.append(S.question_item(f"{sid}:a3:{an['lid']}", QSET_VERSION, packet_state(an, old_text, new_text), QNAME, attempt_question(), lid=an["lid"]))
    return items


_LINE = {
    "same_restated": "the second review restates the defect the first revision tried to fix; fix the governing rule, not only the quoted sentence",
    "new_aspect": "the second review raises a different aspect than the one the first revision addressed",
    "no_relevant_change": "the first revision's edits do not bear on this finding",
}


def make_lines(analyses, outcomes) -> list:
    """One flag line per blocker.  named_not_touched is a code fact; otherwise the Jev label when usable; nothing on any error / insufficient."""
    by = {o["id"].rsplit(":a3:", 1)[1]: o for o in outcomes if o.get("usable")}
    lines = []
    for an in analyses:
        if an["named_not_touched"]:
            txt = "the first revision was recorded as applied for this finding but changed none of the text the first review quoted"
            lines.append({"lid": an["lid"], "refs": an["refs"], "source": "code", "label": "named_not_touched",
                          "text": f"UNVERIFIED A3 [{an['lid']}] {txt}. Verify against the spec text; this is not a finding."})
            continue
        o = by.get(an["lid"])
        if o and o["choice"] in _LINE:
            lines.append({"lid": an["lid"], "refs": an["refs"], "source": "jev", "label": o["choice"],
                          "text": f"UNVERIFIED A3 [{an['lid']}] {_LINE[o['choice']]}. Verify against the spec text; this is not a finding."})
    return lines


def merge_v2_hints(a3_lines, a1_hints, cap=15) -> list:
    """The V2 brief takes A3 lines first, then A1 hints; an A1 hint whose obligation id is among an A3 blocker's refs is merged into that line.
    -> list of text lines, at most `cap`."""
    out, used = [], set()
    for ln in a3_lines:
        extra = [h for h in a1_hints if h["obligation"] in set(ln["refs"]) or h["criterion"] in set(ln["refs"])]
        txt = ln["text"]
        if extra:
            used.update(h["pair"] for h in extra)
            ids = ", ".join(sorted({f"{h['obligation']} x {h['criterion']}" for h in extra})[:4])
            txt = txt.rstrip() + f" (the pair check also flagged: {ids})"
        out.append(txt)
    for h in a1_hints:
        if h["pair"] not in used:
            out.append(h["text"])
    return out[:cap]


# ----------------------------------------------------------------------------- PN1 survivor cases
def _ledger_path(run_dir):
    g = glob.glob(str(run_dir / "ws" / ".dev" / "*" / "review" / "ledger.json"))
    return pathlib.Path(g[0]) if g else None


def _brief(led, n):
    for r in led["rounds"]:
        if r["n"] == n:
            return list(r.get("brief_ids", []))
    return None


def load_pn1_cases() -> dict:
    """Reconstruct the PN1 survivor cases.  -> {'cases': [...], 'report': {...}}.

    survivor = blocker in the round-1 brief AND the round-2 brief of a run that reached V2 (revise2.md exists).
    outcome (hidden from every Jev packet) = 'resolved' if the blocker is absent from the round-3 brief, else 'failed'.
    post-V2 control facts (not available before V2; used only as controls in the separation test): v2_named_not_touched (ledger history)."""
    cases, skipped = [], []
    for run_dir in sorted(RUNS_ROOT.glob("b1-r?")):
        run = run_dir.name
        lp = _ledger_path(run_dir)
        if not lp:
            skipped.append((run, "no ledger"))
            continue
        led = json.loads(lp.read_text())
        rev = lp.parent
        b1, b2, b3 = _brief(led, 1), _brief(led, 2), _brief(led, 3)
        hist = lp.parent.parent / "specs" / "history"
        if b1 is None or b2 is None or not (rev / "revise2.md").exists():
            skipped.append((run, "did not reach V2 (round 2 PASS)" if b2 == [] else "no round-2 brief"))
            continue
        spec_v1, spec_v2 = (hist / "spec-v1.md").read_text(), (hist / "spec-v2.md").read_text()
        final = lp.parent.parent / "specs" / "orca-worker-contract-spec.md"
        final_text = final.read_text()
        r1_text, r2_text = (rev / "round1.md").read_text(), (rev / "round2.md").read_text()
        r1_blocks = parse_blocking(r1_text)
        rev1 = (rev / "revise1.md").read_text()
        rows = {r["lid"]: r for r in led["rows"]}
        survivors = [l for l in b1 if l in b2]
        blockers, applied = [], set()
        for lid in survivors:
            anchors = [d[k] for d in r1_blocks.get(lid, []) for k in ("anchor", "anchor2") if d.get(k)]
            if not anchors and rows.get(lid, {}).get("anchor"):
                anchors = [rows[lid]["anchor"]] + ([rows[lid]["anchor2"]] if rows[lid].get("anchor2") else [])
            blockers.append({"lid": lid, "anchors": anchors, "claims": [d["claim"] for d in r1_blocks.get(lid, []) if d.get("claim")],
                             "refs": rows.get(lid, {}).get("refs", [])})
            m = re.search(rf"^\|\s*{lid}\b[^|]*\|\s*(applied|rejected|noted)[^|]*\|", rev1, re.M)
            if not m or m.group(1) == "applied":
                applied.add(lid)                                   # PN1 recorded every survivor as applied (advocate A3; checked in revise1.md)
        an = analyze(spec_v1, spec_v2, r2_text, blockers, applied, r1_blocks)
        v2h = hunks(spec_v2.split("\n"), final_text.split("\n"))
        v1_new = changed_new(hunks(spec_v1.split("\n"), spec_v2.split("\n")))
        for a in an:
            row = rows[a["lid"]]
            ev = [e for e in row.get("history", []) if e.get("round") == 2]
            v2_nnt = any(e["event"] == "named_not_touched" for e in ev)
            # post-V2 control 2: share of the V2-changed lines inside this blocker's R2 quotes that V1 had already written
            r2l = set()
            for d in a["r2"]:
                for k in ("anchor", "anchor2"):
                    if d.get(k):
                        r2l |= set(locate(d[k], spec_v2.split("\n")))
            v2c = changed_old(touching(v2h, r2l)) & r2l if r2l else set()
            v2_on_v1 = round(len(v2c & v1_new) / len(v2c), 3) if v2c else 0.0
            outcome = None if b3 is None else ("failed" if a["lid"] in b3 else "resolved")
            cases.append({"case_id": f"{run}-{a['lid']}", "run": run, "sid": PN1_SID.get(run), "lid": a["lid"], "analysis": a, "outcome": outcome,
                          "controls": {"v1_named_not_touched": a["named_not_touched"], "v2_named_not_touched": v2_nnt, "v2_changed_on_v1_lines": v2_on_v1,
                                       "v2_overlap_ge_50": v2_on_v1 >= 0.5},
                          "spec_v1": str(hist / "spec-v1.md"), "spec_v2": str(hist / "spec-v2.md"), "r2_report": str(rev / "round2.md")})
    rep = {"reconstructed": len(cases), "runs_with_cases": sorted({c["run"] for c in cases}), "skipped_runs": skipped,
           "outcomes": {k: sum(1 for c in cases if c["outcome"] == k) for k in ("resolved", "failed")},
           "located": sum(1 for c in cases if c["analysis"]["located"]), "touched_v1": sum(1 for c in cases if c["analysis"]["touched_v1"])}
    return {"cases": cases, "report": rep}


def case_items(cases):
    items = []
    for c in cases:
        a = c["analysis"]
        if a["to_jev"]:
            old = pathlib.Path(c["spec_v1"]).read_text()
            new = pathlib.Path(c["spec_v2"]).read_text()
            items.append(S.question_item(f"{c['case_id']}:a3:{a['lid']}", QSET_VERSION, packet_state(a, old, new), QNAME, attempt_question(), lid=a["lid"], case=c["case_id"]))
    return items


def label_packet(c) -> str:
    """Blind labelling packet: V1 change, R2 re-raise and the V2 change; the R3 outcome and every model output are absent."""
    old, mid = pathlib.Path(c["spec_v1"]).read_text(), pathlib.Path(c["spec_v2"]).read_text()
    final = pathlib.Path(c["spec_v2"]).parent.parent / "orca-worker-contract-spec.md"
    fin = final.read_text()
    a = c["analysis"]
    ol, ml, fl = old.split("\n"), mid.split("\n"), fin.split("\n")
    v1 = [_hunk_texts(h, ol, ml, 900) for h in a["hunks"][:6]]
    r2l = set()
    for d in a["r2"]:
        for k in ("anchor", "anchor2"):
            if d.get(k):
                r2l |= set(locate(d[k], ml))
    v2 = [_hunk_texts(h, ml, fl, 900) for h in touching(hunks(ml, fl), r2l)[:6]] if r2l else []
    parts = [f"# Label packet {c['case_id']}", "", f"Blocker {a['lid']}. Question: did the SECOND revision (V2) use a different mechanism from the first (V1) for this finding? "
             "Answer one of: different_mechanism, same_mechanism, v2_changed_nothing_relevant. Give a one-sentence reason.", "", "## First-review claims"]
    parts += [f"- {S.clip(x, 500)}" for x in a.get("claims", [])]
    parts += ["", "## V1 hunks (before -> after)"] + [f"- BEFORE: {h['before']}\n  AFTER: {h['after']}" for h in v1]
    parts += ["", "## Second-review (R2) re-raise"] + [f"- {S.clip(d.get('claim', ''), 500)}  quotes: {S.clip(d.get('anchor', ''), 250)} | {S.clip(d.get('anchor2', ''), 250)}" for d in a["r2"]]
    parts += ["", "## V2 hunks around the R2 quotes (before -> after)"] + ([f"- BEFORE: {h['before']}\n  AFTER: {h['after']}" for h in v2] or ["- (V2 changed none of the quoted lines)"])
    return "\n".join(parts) + "\n"


def run_cases(cases, runner):
    items = case_items(cases)
    outs = [runner.ask(it) for it in items]
    by = {}
    for c in cases:
        by[c["case_id"]] = None
    for it, o in zip(items, outs):
        by[it["case"]] = o
    return items, outs, by


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pn1", action="store_true", help="load the PN1 survivor cases and print the reconstruction report")
    ap.add_argument("--mock", choices=["ok", "insufficient", "malformed", "timeout", "http500", "mixed"])
    ap.add_argument("--out", default=str(S.SEAMS / "out" / "a3-cli"))
    a = ap.parse_args(argv)
    d = load_pn1_cases()
    print(json.dumps(d["report"], indent=1))
    for c in d["cases"]:
        an = c["analysis"]
        print(c["case_id"], "outcome", c["outcome"], "located", an["located"], "touched_v1", an["touched_v1"], "v1_nnt", an["named_not_touched"],
              "span_overlap", an["span_overlap"], "controls", c["controls"])
    if a.mock:
        with S.mock_env():
            r = S.Runner(seam="a3", mode="mock", out_dir=pathlib.Path(a.out), mock_mode=a.mock)
            items, outs, by = run_cases(d["cases"], r)
        print("mock answers:", {k: (v or {}).get("choice") for k, v in by.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
