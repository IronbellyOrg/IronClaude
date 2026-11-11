#!/usr/bin/env python3
"""pool.py  Extract every finding (blocking and follow-up) from the 21 first-review reports of plan section 1 into offline/pool/*.json.

Keeps findings that quote at least one text found verbatim in the original S1 spec (d3cdbe57...).  `group` = catalog cluster id
when a catalog member matches (source run + fid), else '<theme>:<first cited line // 10>'.  Read-only on the report files.
data_classes = {s1_spec, stage2_artifact}.   Usage: uv run --no-project python pool.py [--list]"""
import glob
import json
import pathlib
import re
import sys

import e3lib
import packets as pk
from p15common import datasets

REVIEW = ".dev/orca-command-refactor/review"
CATALOG = e3lib.SP / "p13/catalog/catalog.json"
ID_RX = r"(?:R\d-)?[A-Z]{1,4}-?\d+(?:-\d+)?"
EXCL = {"FR", "AC", "SHA", "WC", "INV", "SPEC", "CMD", "P", "GC", "SA", "NFR", "D", "G", "CAPS", "README", "H", "L", "S"}
START_H = re.compile(r"^(#{3,6})\s*(?:\*\*)?(" + ID_RX + r")(?![\w-])")
START_B = re.compile(r"^\s*(?:[-*]\s*)?\*\*(" + ID_RX + r")(?=[.:)\s*])")
HEAD_ANY = re.compile(r"^#{1,3}\s")
NOT_BLOCKING = re.compile(r"(?i)\b(?:not|non-?)\s*blocking\b|graded (?:minor|medium)")
BLOCKING_WORD = re.compile(r"(?i)\bblocking\b")


def report_files():
    """-> list of (run, kind, path): 3 + 6 + 6 p11 reports and the 6 p14 Haiku-baseline reports (21)."""
    out = []
    for r in sorted(glob.glob(str(e3lib.SP / "p11/runs/a1-r*"))):
        out.append((pathlib.Path(r).name, "p11", pathlib.Path(r) / "ws" / REVIEW / "spec-panel.md"))
    for a in ("a2", "a3"):
        for r in sorted(glob.glob(str(e3lib.SP / f"p11/runs/{a}-r*"))):
            out.append((pathlib.Path(r).name, "p11", pathlib.Path(r) / "ws" / REVIEW / "round1.md"))
    for r in sorted(glob.glob(str(e3lib.SP / "p14/haiku-baseline/runs/a3-r*"))):
        out.append((pathlib.Path(r).name, "p14", pathlib.Path(r) / "ws" / REVIEW / "round1.md"))
    return out


def run_tag(run, kind):
    return ("h" if kind == "p14" else "") + run.replace("-", "")


def split_findings(text):
    """-> [(id, heading_line, section_text)] for every finding-like section (heading or bold-lead start)."""
    lines = text.splitlines()
    starts = []
    for i, ln in enumerate(lines):
        m = START_H.match(ln) or START_B.match(ln)
        if not m:
            continue
        fid = m.group(2) if START_H.match(ln) else m.group(1)
        lead = re.split(r"[\d-]", fid, maxsplit=1)[0]
        if lead in EXCL or fid.startswith(("FR", "AC")):
            continue
        starts.append((i, fid))
    out = []
    for k, (i, fid) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        for j in range(i + 1, end):
            if HEAD_ANY.match(lines[j]):
                end = j
                break
        sec = "\n".join(lines[i:end]).rstrip()
        out.append((fid, lines[i], sec))
    return out


def blocking_ids(report_path, sc):
    ids = set(sc.parse_ids(sc.ids_from(report_path)))
    return ids | {"F" + i for i in ids if i.isdigit()}


def catalog_index():
    idx = {}
    if CATALOG.exists():
        for cl in json.loads(CATALOG.read_text())["clusters"]:
            for m in cl["members"]:
                if not m["source"].endswith("/R1"):
                    continue
                run = m["source"].split("/")[0]
                for fid in (m["fid"], "F" + m["fid"]):
                    idx.setdefault((run, fid), cl["cid"])
    return idx


def group_of(run, kind, fid, heading, section, sc, cat):
    if kind == "p11" and (run, fid) in cat:
        return cat[(run, fid)]
    cites = sorted(sc.cited(heading + "\n" + section))
    return f"{sc.tag(heading, section)}:{(cites[0] // 10) if cites else 'x'}"


def extract(dec=None):
    sc = _sc()
    spec = e3lib.s1_text()
    cat = catalog_index()
    items, skipped = [], {"no_verbatim_quote": 0, "too_short": 0}
    for run, kind, path in report_files():
        if not path.exists():
            print(f"WARN missing report {path}")
            continue
        text = path.read_text(errors="ignore")
        bl = blocking_ids(path, sc)
        seen = set()
        for fid, heading, sec in split_findings(text):
            if fid in seen:
                continue
            seen.add(fid)
            if len(sec) < 150:
                skipped["too_short"] += 1
                continue
            quotes = pk.extract_quotes(pk.drop_reasoning(sec))
            if not any(q in spec for q in quotes):
                skipped["no_verbatim_quote"] += 1
                continue
            head200 = heading[:300]
            rb = fid in bl or (bool(BLOCKING_WORD.search(head200)) and not NOT_BLOCKING.search(head200))
            tag = run_tag(run, kind)
            cid = re.sub(r"[^A-Za-z0-9]+", "_", f"real-{tag}-{fid}").strip("_")
            case = {"case_id": cid, "group": group_of(run, kind, fid, heading, sec, sc, cat), "family": "s1_first_review",
                    "category": "real", "variant": "base", "split": "pool",
                    "data_classes": ["s1_spec", "stage2_artifact"],
                    "source": {"kind": "stage2", "paths": [str(path.relative_to(e3lib.SP))], "url": None},
                    "packet": {"finding_id": fid, "finding_section": sec, "candidate_sha": e3lib.S1_SHA},
                    "author_intent": {"reviewer_blocking": rb, "reviewer": "haiku" if kind == "p14" else "sonnet-or-panel", "run": run}}
            items.append(case)
    return items, skipped


_SC = None


def _sc():
    global _SC
    if _SC is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("score_themes_e3", e3lib.CENTRAL / "score_themes.py")
        _SC = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_SC)
    return _SC


def prune(items, dec=None):
    """Seeded pruning to about `pool_target` items without looking at any label: up to `pool_cap_blocking_per_group`
    reviewer-blocking findings per group, then follow-up findings taken round-robin over groups."""
    import random
    d = dec or e3lib.decision()["offline"]
    rng = random.Random(d["select_seed"])
    by_group = {}
    for c in sorted(items, key=lambda c: c["case_id"]):
        by_group.setdefault((c["group"], c["author_intent"]["reviewer_blocking"]), []).append(c)
    keep = []
    for (g, rb) in sorted(by_group):
        if rb:
            lst = by_group[(g, rb)][:]
            rng.shuffle(lst)
            keep.extend(lst[:d["pool_cap_blocking_per_group"]])
    room = max(0, d["pool_target"] - len(keep))
    fgroups = sorted(g for (g, rb) in by_group if not rb)
    queues = {}
    for g in fgroups:
        lst = by_group[(g, False)][:]
        rng.shuffle(lst)
        queues[g] = lst
    order = fgroups[:]
    rng.shuffle(order)
    picked = []
    while len(picked) < room and any(queues.values()):
        for g in order:
            if queues[g] and len(picked) < room:
                picked.append(queues[g].pop())
    return sorted(keep + picked, key=lambda c: c["case_id"])


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    items, skipped = extract()
    skipped["pruned"] = len(items)
    items = prune(items)
    skipped["pruned"] -= len(items)
    e3lib.POOL.mkdir(parents=True, exist_ok=True)
    for old in e3lib.POOL.glob("*.json"):
        old.unlink()
    ids = set()
    for c in items:
        assert c["case_id"] not in ids, c["case_id"]
        ids.add(c["case_id"])
        datasets.write_case(e3lib.POOL / f"{c['case_id']}.json", c)
    groups = sorted({c["group"] for c in items})
    n_block = sum(1 for c in items if c["author_intent"]["reviewer_blocking"])
    summ = {"n": len(items), "groups": len(groups), "reviewer_blocking": n_block, "reviewer_other": len(items) - n_block,
            "skipped": skipped, "reports": len(report_files())}
    e3lib.write_json(e3lib.POOL / "_summary.json", summ)
    print(f"POOL {len(items)} real findings from {summ['reports']} first reviews ({len(groups)} groups); "
          f"reviewer-blocking {n_block}, other {len(items) - n_block}; skipped {skipped}")
    if "--list" in argv:
        for c in items:
            print(c["case_id"], c["group"], c["author_intent"]["reviewer_blocking"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
