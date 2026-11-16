"""Gate G0, the offline selection-recall gate (DESIGN 14.1, REQ-22, REQ-35). No model is started.

    g0.py --docs SET|ID,ID --gt-dir DIR [--seeds 1,2,3] (--floor X | --floor-from config/prereg.json) [--cap N] [--out FILE]
    g0.py --docs ... --ablate [--seeds ...]        leave-one-class-out: the change in the other classes' selection recall
    g0.py --manifest FILE --docs ID,ID ...         documents given in a file instead of config/packages.json and the sandbox

For every document the pre-pass finds its candidates and selects its items exactly as a run would (sweep.extractors and
sweep.select, no assignment and no rendering). A ground-truth item is covered by a candidate or an item when the flattened
`plan_quote` contains it or is contained in its `anchor_text` (text of 12 or more characters), or when their line spans come
within 3 lines of each other (the rule of FND.same_defect; analysis/analyze.py `covers` holds the one definition).

  extraction recall   covered ground-truth items over all items, by any candidate (before selection)
  selection recall    the same, by a selected item; pooled over the documents, and per class (the class of the item)
  random baseline (a) `draws` draws (seeded) of `cap` candidates per document, uniformly from all of its candidates
  random baseline (b) the same draws kept inside the fair-share structure of select.select with a random order for the rank
  pass                DESIGN 14.1 states it over two groups: the selection recall (mean over the seeds) of the decision
                      documents at or above the floor, and the rank above the mean of baseline (a) with at most 10% of its
                      draws at or above it on the derivation plans. --role says which part a call decides (default: from
                      --docs: holdout the floor, derivation the baseline, anything else both). Baseline (b) is reported,
                      not gated.
  ablation            each class removed in turn; every other class's selection recall may change by at most 0.15

The floor is read from the pre-registration file (`analyze.py prereg`) or given with --floor; this file has no default floor
(the owner decides it). A ground-truth file is opened only for a path that the command line gives (--gt-dir or --manifest).
Exit codes: 0 the gate passes (or the ablation is within its limit), 1 it does not, 2 a usage error or a missing input.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import random
import sys
from pathlib import Path

SW = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SW))

from analysis import analyze  # noqa: E402
from scaffold import fnd  # noqa: E402
from sweep import extractors, plan, select  # noqa: E402

SCHEMA = "sweep-g0/1"
DRAWS = 2000
DRAW_SEED = 20261115
TAIL = 0.10  # at most this share of the random draws may reach the rank's recall
ABLATION_LIMIT = 0.15
EPS = 1e-9
CLASSES = analyze.CLASSES
DERIVATION_SETS = ("defect-rich", "control", "derivation")


class G0Error(Exception):
    """An input that cannot be used (exit code 2)."""


# --- coverage and recall ----------------------------------------------------------------------------------------------


def covers(item, gt, cand_text) -> bool:
    """Does a candidate or selected item ({anchor_text, location}) cover a ground-truth item ({plan_quote, ...})?"""
    spans = fnd.locate(cand_text, gt["plan_quote"])
    return analyze.covers(
        item.get("anchor_text"),
        analyze._span(item.get("location")),
        gt["plan_quote"],
        spans,
    )


def cover_sets(entries, gt_items, cand_text) -> list:
    """For each entry, the set of ground-truth item ids that it covers."""
    spans = {g["id"]: fnd.locate(cand_text, g["plan_quote"]) for g in gt_items}
    out = []
    for e in entries:
        text, span = e.get("anchor_text"), analyze._span(e.get("location"))
        out.append(
            {
                g["id"]
                for g in gt_items
                if analyze.covers(text, span, g["plan_quote"], spans[g["id"]])
            }
        )
    return out


def recall(gt_items, entries, cand_text) -> dict:
    """{covered: ids, recall, per_class: {class: {covered, total, recall}}} of the ground-truth items by the entries."""
    if not gt_items:
        raise G0Error("no ground-truth items")
    covered = (
        set().union(*cover_sets(entries, gt_items, cand_text)) if entries else set()
    )
    per = {}
    for g in gt_items:
        t = per.setdefault(g["class"], {"covered": 0, "total": 0})
        t["total"] += 1
        t["covered"] += g["id"] in covered
    for t in per.values():
        t["recall"] = t["covered"] / t["total"]
    return {
        "covered": sorted(covered),
        "recall": len(covered) / len(gt_items),
        "per_class": dict(sorted(per.items())),
    }


def _entry(c) -> dict:
    return {"anchor_text": c.anchor_text, "location": c.location}


# --- the pre-pass of one document ------------------------------------------------------------------------------------


def load_doc(doc_id, candidate, source, repo, gt) -> dict:
    """The inputs of one document. `gt` is a ground-truth file named by the caller; `source` may be None."""
    gt_items = json.loads(Path(gt).read_text(encoding="utf-8"))["items"]
    return {
        "id": doc_id,
        "candidate": Path(candidate),
        "source": Path(source) if source else None,
        "repo": Path(repo),
        "gt": gt_items,
        "text": Path(candidate).read_text(encoding="utf-8"),
    }


def prepass_view(doc, seed, cap=None) -> dict:
    """Run the candidate finder and the selection for one document and seed: {candidates (Candidate objects), items}."""
    parsed = plan.parse(doc["candidate"].read_bytes())
    src = plan.parse(doc["source"].read_bytes()) if doc["source"] else None
    ctx = extractors.Ctx(parsed, source=src, snapshot=doc["repo"], seed=seed)
    if cap is not None:
        ctx.constants = {**ctx.constants, "cap": cap}
    cands = extractors.run_extractors(ctx)
    sel = select.select(cands, seed, ctx.constants)
    return {"candidates": cands, "items": sel.items, "constants": ctx.constants}


def _pooled(parts):
    """Pool per-document recalls: [(gt_items, covered ids)] -> (recall, per-class {covered, total, recall})."""
    total = sum(len(g) for g, _ in parts)
    got = sum(len(c) for _, c in parts)
    per = {}
    for gt_items, covered in parts:
        for g in gt_items:
            t = per.setdefault(g["class"], {"covered": 0, "total": 0})
            t["total"] += 1
            t["covered"] += g["id"] in covered
    for t in per.values():
        t["recall"] = t["covered"] / t["total"]
    return got / total, dict(sorted(per.items()))


def stage_recalls(docs, views) -> tuple:
    """(extraction, selection) as (recall, per_class) pooled over the documents; views[i] belongs to docs[i]."""
    ext, sel = [], []
    for d, v in zip(docs, views):
        ext.append(
            (
                d["gt"],
                set().union(
                    *cover_sets(
                        [_entry(c) for c in v["candidates"]], d["gt"], d["text"]
                    )
                    or [set()]
                ),
            )
        )
        sel.append(
            (
                d["gt"],
                set().union(*cover_sets(v["items"], d["gt"], d["text"]) or [set()]),
            )
        )
    return _pooled(ext), _pooled(sel)


# --- random baselines ----------------------------------------------------------------------------------------------------


def baseline_a(docs, views, draws=DRAWS, seed=DRAW_SEED, cap=12) -> list:
    """The pooled selection recall of `draws` random picks of `cap` candidates per document (uniform, without replacement)."""
    rng = random.Random(seed)
    sets = [
        cover_sets([_entry(c) for c in v["candidates"]], d["gt"], d["text"])
        for d, v in zip(docs, views)
    ]
    total = sum(len(d["gt"]) for d in docs)
    out = []
    for _ in range(draws):
        got = 0
        for s in sets:
            pick = rng.sample(range(len(s)), min(cap, len(s)))
            got += len(set().union(*[s[i] for i in pick])) if pick else 0
        out.append(got / total)
    return out


def baseline_b(docs, views, draws=DRAWS, seed=DRAW_SEED, cap=12) -> list:
    """The same draws kept inside the fair-share structure (class order, a second pass, the per-class ceiling): select.select
    with a random order in place of the rank."""
    rng = random.Random(seed)
    consts = [{**v["constants"], "cap": cap} for v in views]
    sets = [
        {
            id(c): s
            for c, s in zip(
                v["candidates"],
                cover_sets([_entry(c) for c in v["candidates"]], d["gt"], d["text"]),
            )
        }
        for d, v in zip(docs, views)
    ]
    total = sum(len(d["gt"]) for d in docs)
    out = []
    for n in range(draws):
        got = 0
        for v, k, s in zip(views, consts, sets):
            copies, origin = [], {}
            for c in v["candidates"]:
                cp = dataclasses.replace(
                    c, priority=rng.random(), evidence_computed=True
                )
                copies.append(cp)
                origin[id(cp)] = c
            select.select(copies, f"{seed}:{n}", k)  # sets each copy's status
            chosen = [
                origin[id(c)] for c in copies if c.status == select.STATUS_SELECTED
            ]
            got += len(set().union(*[s[id(c)] for c in chosen])) if chosen else 0
        out.append(got / total)
    return out


def _tail(draws, value):
    return sum(x >= value - EPS for x in draws) / len(draws)


def beats(rank_recall, draws) -> bool:
    """The rank beats a random pick: above the mean of the draws, with at most 10% of the draws at or above it."""
    return (
        rank_recall > sum(draws) / len(draws) + EPS
        and _tail(draws, rank_recall) <= TAIL + EPS
    )


ROLES = ("decision", "derivation", "both")


# --- the gate and the ablation ------------------------------------------------------------------------------------------


def evaluate(
    docs,
    seeds=(1,),
    floor=None,
    cap=None,
    draws=DRAWS,
    draw_seed=DRAW_SEED,
    role="both",
) -> dict:
    """Extraction and selection recall, both random baselines and the pass rule over the documents.

    DESIGN 14.1 states the pass rule over two document groups: the selection recall of the decision documents must reach the
    floor, and the rank must beat random baseline (a) on the derivation plans. `role` says which part this call decides:
    "decision" the floor, "derivation" the random baseline, "both" (explicit documents, the default) both. Both parts are
    always computed and reported.
    """
    if role not in ROLES:
        raise G0Error(f"role must be one of {', '.join(ROLES)}")
    if not docs or not seeds:
        raise G0Error("no documents or no seeds")
    views = {s: [prepass_view(d, s, cap) for d in docs] for s in seeds}
    first = views[seeds[0]]
    size = int(first[0]["constants"]["cap"])
    ext_recall, ext_class = stage_recalls(docs, first)[0]
    by_seed, per_class = {}, {}
    for s in seeds:
        _, (r, per) = stage_recalls(docs, views[s])
        by_seed[s] = r
        for c, t in per.items():
            per_class.setdefault(c, []).append(t["recall"])
    sel_recall = sum(by_seed.values()) / len(by_seed)
    a = baseline_a(docs, first, draws, draw_seed, size)
    b = baseline_b(docs, first, draws, draw_seed, size)
    mean_a = sum(a) / len(a)
    tail_a = _tail(a, sel_recall)
    beaten = beats(sel_recall, a)
    meets = None if floor is None else sel_recall + EPS >= floor
    parts = {"decision": [meets], "derivation": [beaten], "both": [meets, beaten]}[role]
    gate = None if None in parts else all(parts)
    return {
        "schema": SCHEMA,
        "documents": [d["id"] for d in docs],
        "seeds": list(seeds),
        "cap": size,
        "ground_truth_items": sum(len(d["gt"]) for d in docs),
        "extraction": {"recall": ext_recall, "per_class": ext_class},
        "selection": {
            "recall": sel_recall,
            "recall_by_seed": by_seed,
            "per_class": {c: sum(v) / len(v) for c, v in sorted(per_class.items())},
        },
        "baseline_a": {
            "draws": draws,
            "mean": mean_a,
            "share_at_or_above": tail_a,
            "beats_random": beaten,
        },
        "baseline_b": {
            "draws": draws,
            "mean": sum(b) / len(b),
            "share_at_or_above": _tail(b, sel_recall),
        },
        "floor": floor,
        "role": role,
        "pass": {"floor": meets, "beats_random": beaten, "gate": gate},
    }


def ablate(docs, seeds=(1,), cap=None) -> dict:
    """Leave one class out of the candidates before selection; the change in every other class's selection recall."""
    views = {s: [prepass_view(d, s, cap) for d in docs] for s in seeds}

    def mean_per_class(drop):
        acc = {}
        for s in seeds:
            parts = []
            for d, v in zip(docs, views[s]):
                pool = [
                    dataclasses.replace(c) for c in v["candidates"] if c.cls != drop
                ]
                items = select.select(pool, s, v["constants"]).items
                parts.append(
                    (
                        d["gt"],
                        set().union(*cover_sets(items, d["gt"], d["text"]) or [set()]),
                    )
                )
            for c, t in _pooled(parts)[1].items():
                acc.setdefault(c, []).append(t["recall"])
        return {c: sum(v) / len(v) for c, v in acc.items()}

    base = mean_per_class(None)
    present = sorted({c.cls for v in views[seeds[0]] for c in v["candidates"]})
    report = {}
    for cls in present:
        without = mean_per_class(cls)
        report[cls] = {o: without[o] - base[o] for o in sorted(base) if o != cls}
    worst = max((abs(x) for r in report.values() for x in r.values()), default=0.0)
    return {
        "schema": SCHEMA,
        "documents": [d["id"] for d in docs],
        "seeds": list(seeds),
        "limit": ABLATION_LIMIT,
        "selection_recall": base,
        "removed": report,
        "largest_change": worst,
        "within_limit": worst <= ABLATION_LIMIT + EPS,
    }


# --- command line ----------------------------------------------------------------------------------------------------------


def _floor(args, required=True):
    if args.floor is not None:
        return args.floor
    if args.floor_from:
        p = Path(args.floor_from)
        if not p.is_file():
            if not required:
                return None
            raise G0Error(
                f"{p} does not exist: write it with `analyze.py prereg --write`, or give --floor"
            )
        return float(
            json.loads(p.read_text(encoding="utf-8"))["selection_recall_floor"]
        )
    if not required:
        return None
    raise G0Error(
        "no floor: give --floor or --floor-from (the owner decides the floor; this script has no default)"
    )


def _role(args) -> str:
    """The part of the pass rule this call decides: holdout documents the floor, derivation documents the random baseline."""
    return args.role or {"holdout": "decision", "derivation": "derivation"}.get(
        args.docs, "both"
    )


def _resolve(args) -> list:
    """The documents named by --docs: a set name or ids, from --manifest or from config/packages.json and the sandbox."""
    names = [x for x in args.docs.split(",") if x]
    if args.manifest:
        entries = json.loads(Path(args.manifest).read_text(encoding="utf-8"))["docs"]
    else:
        sets = analyze.load_sets(args.packages)
        sb = Path(
            args.sandbox_root or os.environ.get("SW_SB_ROOT", "/tmp/evalsb-sweep")
        )
        if not args.gt_dir:
            raise G0Error(
                "--gt-dir is required (a folder with <doc>.json or <doc>/ground-truth.json)"
            )
        entries = {}
        for doc in sets:
            gt = next(
                (
                    p
                    for p in (
                        Path(args.gt_dir) / f"{doc}.json",
                        Path(args.gt_dir) / doc / "ground-truth.json",
                    )
                    if p.is_file()
                ),
                None,
            )
            src = sb / "cand" / doc / "source.md"
            entries[doc] = {
                "candidate": str(sb / "cand" / doc / "candidate.md"),
                "source": str(src) if src.is_file() else None,
                "repo": str(sb / doc / "repo"),
                "gt": str(gt) if gt else None,
                "set": sets[doc],
            }
    ids = []
    for n in names:
        ids += [
            d
            for d, e in entries.items()
            if (
                e.get("set") in DERIVATION_SETS
                if n == "derivation"
                else e.get("set") == n
            )
        ] or [n]
    out = []
    for d in dict.fromkeys(ids):
        e = entries.get(d)
        if e is None or not e.get("gt"):
            raise G0Error(f"document {d}: no entry or no ground-truth path")
        for key in ("candidate", "repo", "gt"):
            if not Path(e[key]).exists():
                raise G0Error(f"document {d}: {key} {e[key]} does not exist")
        out.append(load_doc(d, e["candidate"], e.get("source"), e["repo"], e["gt"]))
    if not out:
        raise G0Error(f"--docs {args.docs} names no document")
    return out


def render(result) -> str:
    if "removed" in result:
        lines = [
            f"G0 ablation over {', '.join(result['documents'])} (limit {result['limit']:.2f})",
            "",
        ]
        for cls, ch in result["removed"].items():
            lines.append(
                f"- without {cls}: " + ", ".join(f"{o} {x:+.3f}" for o, x in ch.items())
            )
        lines += [
            "",
            f"largest change {result['largest_change']:.3f}: {'within' if result['within_limit'] else 'OVER'} the limit",
        ]
        return "\n".join(lines) + "\n"
    a, b = result["baseline_a"], result["baseline_b"]
    lines = [
        f"G0 over {', '.join(result['documents'])}; seeds {result['seeds']}; sheet size {result['cap']}",
        f"extraction recall {result['extraction']['recall']:.3f}; selection recall {result['selection']['recall']:.3f}",
    ]
    for c in CLASSES:
        e, s = (
            result["extraction"]["per_class"].get(c),
            result["selection"]["per_class"].get(c),
        )
        if e is not None:
            lines.append(f"- {c}: extraction {e['recall']:.3f}, selection {s:.3f}")
    lines += [
        f"random pick (a): mean {a['mean']:.3f}, {a['share_at_or_above']:.1%} of {a['draws']} draws at or above the rank",
        f"fair-share random (b): mean {b['mean']:.3f}, {b['share_at_or_above']:.1%} at or above (reported, not gated)",
        f"floor {result['floor']}: {result['pass']['floor']}; beats random (a): {a['beats_random']}; "
        f"gate ({result['role']}): "
        + {True: "PASS", False: "FAIL", None: "no floor"}[result["pass"]["gate"]],
    ]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="g0.py", description=__doc__.split("\n")[0])
    ap.add_argument(
        "--docs",
        required=True,
        help="a set (derivation, holdout) or document ids, comma separated",
    )
    ap.add_argument(
        "--manifest",
        help='a JSON file {"docs": {id: {candidate, source, repo, gt, set}}}',
    )
    ap.add_argument("--packages", help="config/packages.json (default)")
    ap.add_argument(
        "--sandbox-root",
        help="where bin/build-sandbox.sh built the sandboxes (default SW_SB_ROOT or /tmp/evalsb-sweep)",
    )
    ap.add_argument(
        "--gt-dir", help="a folder with <doc>.json or <doc>/ground-truth.json"
    )
    ap.add_argument(
        "--seeds", default="1", help="comma separated, for example 1,2,3,4,5"
    )
    ap.add_argument("--floor", type=float)
    ap.add_argument(
        "--floor-from", help="a pre-registration file with selection_recall_floor"
    )
    ap.add_argument(
        "--role",
        choices=ROLES,
        help="the part of the pass rule to decide (default: from --docs)",
    )
    ap.add_argument(
        "--cap", type=int, help="sheet size (default: cap of config/values.json)"
    )
    ap.add_argument("--draws", type=int, default=DRAWS)
    ap.add_argument("--ablate", action="store_true")
    ap.add_argument(
        "--out", help="write the result as JSON (under the sweep-sheet folder or /tmp)"
    )
    args = ap.parse_args(argv)
    try:
        seeds = [int(s) for s in args.seeds.split(",") if s]
        docs = _resolve(args)
        if args.ablate:
            result = ablate(docs, seeds, args.cap)
            ok = result["within_limit"]
        else:
            role = _role(args)
            floor = _floor(args, required=role != "derivation")
            result = evaluate(docs, seeds, floor, args.cap, args.draws, role=role)
            ok = result["pass"]["gate"]
        if args.out:
            analyze._write(result, args.out)
        sys.stdout.write(render(result))
        return 0 if ok else 1
    except (G0Error, analyze.AnalysisError, ValueError) as e:
        print(f"g0: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
