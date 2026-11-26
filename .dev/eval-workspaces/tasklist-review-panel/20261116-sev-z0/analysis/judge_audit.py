"""Judge helpers for bin/anon.sh and bin/judge-batch.sh (DESIGN 9.7, REQ-43): anonymise a merged report, pick the
second-judge sample, audit the judge folders. Standard library only; it reads no ground truth and starts no model.

    judge_audit.py anon   --run RUNDIR --label L --seed S --out FILE
    judge_audit.py plan   --runs-dir DIR --scoring-dir DIR --seed S RUN...   (prints: label, run, doc, role)
    judge_audit.py sample --seed S RUN...                                    (prints the second-judge runs)
    judge_audit.py audit  --scoring-dir DIR [--out FILE] [--invalidate]      (exit 1 if any item is bad)

A judge folder is scoring/<label>/{merged-anon.md, judge.json, judge.err, score.json}.
"""

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

FRACTION = 0.15
ARM_NAMES = r"Z0-raw|Z0|RLh|RLs|RL"
ID_CHARS = r"A-Za-z0-9_\-"
ABS_PATH = re.compile(r"(?<![\w<])(?:/[\w.@+~-]+)+/?")
ABS_ROOTS = ("/home/", "/tmp/", "/root/", "/Users/", "/var/", "/mnt/")
MARKER_KEY = re.compile(
    r"""["']?\b(?:class|probe|src)\b["']?\s*[:=]\s*(?:"[^"]*"|'[^']*'|[^\s,;}]+),?"""
)
MARKER_WORD = re.compile(rf"ledger-v1|(?<![{ID_CHARS}])(?:{ARM_NAMES})(?![{ID_CHARS}])")
API_ERROR = re.compile(
    r"API Error|overloaded_error|rate_limit_error|authentication_error|Credit balance is too low",
    re.I,
)


def _token(word):
    """A regex that matches `word` only as a whole identifier (ids hold letters, digits, `_` and `-`)."""
    return re.compile(rf"(?<![{ID_CHARS}.])" + re.escape(word) + rf"(?![{ID_CHARS}])")


def anonymise(text, run_id, reviewer_ids, seed=0, label=""):
    """The merged report with paths redacted, the run id and the arm marker removed, and reviewer ids replaced by R1..Rn.

    The numbering is a shuffle seeded by (seed, label), so R1 is not the same role in every report. Returns
    (text, {reviewer id: R<n>}).
    """

    def path(m):
        p = m.group(0)
        return "<path>" if p.startswith(ABS_ROOTS) or run_id in p else p

    out = ABS_PATH.sub(path, text)
    out = _token(run_id).sub("<run>", out)
    ids = sorted(set(reviewer_ids), key=lambda s: (-len(s), s))
    order = sorted(ids)
    random.Random(f"{seed}:{label}").shuffle(order)
    names = {rid: f"R{n}" for n, rid in enumerate(order, 1)}
    for rid in ids:
        out = _token(rid).sub(names[rid], out)
    out = MARKER_KEY.sub("", out)
    out = MARKER_WORD.sub("", out)
    return out, names


def leaks(text, run_id, reviewer_ids):
    """What an anonymised report still gives away (empty list when clean)."""
    found = [
        f"reviewer id {r}" for r in sorted(set(reviewer_ids)) if _token(r).search(text)
    ]
    if _token(run_id).search(text):
        found.append("run id")
    found += [
        f"path {m.group(0)}"
        for m in ABS_PATH.finditer(text)
        if m.group(0).startswith(ABS_ROOTS)
    ]
    found += [f"marker {m.group(0).strip()}" for m in MARKER_KEY.finditer(text)]
    found += [f"marker {m.group(0)}" for m in MARKER_WORD.finditer(text)]
    return found


def run_info(run_dir):
    """(run id, doc id, reviewer ids) of a run folder, from run.json and resolution.json."""
    run_dir = Path(run_dir)
    meta = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    ids = set(meta.get("reviewers", {}))
    res = run_dir / "resolution.json"
    if res.is_file():
        ids |= {
            r["reviewer_id"]
            for r in json.loads(res.read_text(encoding="utf-8")).get("reviewers", [])
        }
    return run_dir.name, meta["doc"], sorted(ids)


def anon_file(run_dir, label, seed, out):
    """Write the anonymised merged-1.md of a run to `out`; raises ValueError if anything still leaks."""
    run_id, _doc, ids = run_info(run_dir)
    text = (Path(run_dir) / "merged" / "merged-1.md").read_text(encoding="utf-8")
    anon, _ = anonymise(text, run_id, ids, seed, label)
    bad = leaks(anon, run_id, ids)
    if bad:
        raise ValueError(f"anonymised report of {run_id} still holds: {bad}")
    out = Path(out)
    if out.is_file() and out.read_text(encoding="utf-8") == anon:
        return  # keep the mtime: a score written after it must not look stale on a re-run
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(anon, encoding="utf-8")


def sample(runs, seed, fraction=FRACTION):
    """The second-judge sample: round(fraction * n) of the distinct runs, the same for a fixed seed.

    Python's round() (half to even) is the rounding: n = 10 gives 2, n = 30 gives 4.
    """
    runs = sorted(set(runs))
    return sorted(random.Random(seed).sample(runs, round(fraction * len(runs))))


def make_label(seed, run_id, role):
    """A random-looking label that a reader without the seed and the run id cannot map back."""
    return "j" + hashlib.sha256(f"{seed}:{role}:{run_id}".encode()).hexdigest()[:10]


def plan(runs_dir, runs, seed):
    """[(label, run id, doc id, role)] for every first judging and every second judging of the sample."""
    rows = []
    for run in sorted(set(runs)):
        rows.append(
            (
                make_label(seed, run, "first"),
                run,
                run_info(Path(runs_dir) / run)[1],
                "first",
            )
        )
    for run in sample(runs, seed):
        rows.append(
            (
                make_label(seed, run, "second"),
                run,
                run_info(Path(runs_dir) / run)[1],
                "second",
            )
        )
    return rows


def merged_rows(text):
    """(rows, blocking rows) of the Ledger table of a merged report."""
    rows = blocking = 0
    col = None
    in_ledger = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_ledger = line.strip() == "## Ledger"
            continue
        if not in_ledger or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "lid":
            col = cells.index("blocking") if "blocking" in cells else None
        elif cells and re.fullmatch(r"L\d+", cells[0]):
            rows += 1
            blocking += col is not None and cells[col].lower() == "yes"
    return rows, blocking


def _events(raw):
    data = json.loads(raw)
    return [
        e for e in (data if isinstance(data, list) else [data]) if isinstance(e, dict)
    ]


def api_error(d):
    """True if the judge's final message or stderr in folder `d` is an API error."""
    err = d / "judge.err"
    if err.is_file() and API_ERROR.search(
        err.read_text(encoding="utf-8", errors="replace")
    ):
        return True
    for e in _events((d / "judge.json").read_text(encoding="utf-8")):
        if e.get("is_error") is True or str(e.get("subtype", "")).startswith("error"):
            return True
        if e.get("type") == "result" and API_ERROR.search(str(e.get("result", ""))):
            return True
    return False


def audit_one(d):
    """Flags of one judge folder; an empty list means it is good."""
    d = Path(d)
    flags = []
    merged, judge, score = d / "merged-anon.md", d / "judge.json", d / "score.json"
    if not merged.is_file():
        flags.append("no_merged")
    if not judge.is_file():
        flags.append("no_judge_json")
    else:
        try:
            if api_error(d):
                flags.append("api_error")
        except ValueError:
            flags.append("judge_unparseable")
    if not score.is_file():
        flags.append("no_score")
        return flags
    try:
        s = json.loads(score.read_text(encoding="utf-8"))
    except ValueError:
        return [*flags, "score_unparseable"]
    if merged.is_file():
        # a score older than the report it scores is left over from an earlier attempt (the defect REQ-43 audits)
        if score.stat().st_mtime < merged.stat().st_mtime:
            flags.append("stale_score")
        total, blocking = merged_rows(merged.read_text(encoding="utf-8"))
        if s.get("ledger_rows_total") != total:
            flags.append("rows_total_mismatch")
        if s.get("ledger_rows_blocking") != blocking:
            flags.append("rows_blocking_mismatch")
    return flags


def audit(scoring_dir, invalidate=False):
    """Audit every judge folder under scoring_dir. With invalidate, a flagged score.json is renamed score.json.invalid."""
    items = []
    for d in sorted(
        p
        for p in Path(scoring_dir).iterdir()
        if (p / "merged-anon.md").is_file() or (p / "judge.json").is_file()
    ):
        flags = audit_one(d)
        if flags and invalidate and (d / "score.json").is_file():
            (d / "score.json").rename(d / "score.json.invalid")
        items.append({"label": d.name, "ok": not flags, "flags": flags})
    return {"total": len(items), "bad": sum(not i["ok"] for i in items), "items": items}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("anon")
    a.add_argument("--run", required=True)
    a.add_argument("--label", required=True)
    a.add_argument("--seed", type=int, default=0)
    a.add_argument("--out", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--runs-dir", required=True)
    p.add_argument("--scoring-dir", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("runs", nargs="+")
    s = sub.add_parser("sample")
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("runs", nargs="+")
    u = sub.add_parser("audit")
    u.add_argument("--scoring-dir", required=True)
    u.add_argument("--out")
    u.add_argument("--invalidate", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "anon":
        try:
            anon_file(args.run, args.label, args.seed, args.out)
        except (OSError, ValueError, KeyError) as e:
            print(f"E_ANON: {e}", file=sys.stderr)
            return 3
    elif args.cmd == "plan":
        rows = plan(args.runs_dir, args.runs, args.seed)
        out = Path(args.scoring_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "labels.tsv").write_text(
            "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8"
        )
        print("".join("\t".join(r) + "\n" for r in rows), end="")
    elif args.cmd == "sample":
        print("\n".join(sample(args.runs, args.seed)))
    else:
        result = audit(args.scoring_dir, args.invalidate)
        text = json.dumps(result, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
        print(f"judge audit: {result['total']} folders, bad = {result['bad']}")
        for i in result["items"]:
            if not i["ok"]:
                print(f"BAD {i['label']}: {','.join(i['flags'])}")
        return 1 if result["bad"] else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
