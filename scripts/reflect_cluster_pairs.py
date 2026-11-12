#!/usr/bin/env python3
"""The 50-pair cluster check sheet for cluster_v2 (Stage 0 exit) and its scorer.

Run with ``uv run python scripts/reflect_cluster_pairs.py sample [--root <repo>] [--out <csv>]`` to write the sheet
and ``uv run python scripts/reflect_cluster_pairs.py score [--root <repo>] [--sheet <csv>]`` to score it after the
owner has filled the human_same_defect column. Both modes read files only: no model, no process, no network.

Inputs (sample): the same recorded cards and clustering as scripts/reflect_stage0a_replay.py. For every pre-* run
under <root>/.dev/reflect that has reviewer-cards/, the cards are listed with the replay's _card_files, converted with
card_convert.convert_card_file and clustered with cluster_v2 over the run's snapshot list (the replay's _snapshot),
one reviewer record per card in name order. Calibration is not passed: cluster membership depends only on
same_defect_v2, so the clusters are the replay's clusters.

Pair: two clustered findings of the same run that come from two different reviewer cards. Pairs across runs and
pairs of one card's own findings are not drawn.

Verdict (cluster_v2_verdict): merged when both findings are members of the same cluster and that cluster is not
chained; apart when they are members of two different clusters. A pair inside one chained cluster is neither
(cluster_v2 never treats a chained cluster as one issue) and is not drawn.

File relation: each finding's files are the paths of its citations that have a path (an unresolved ref from the
converter has none; a path missing from the snapshot still counts). same-file when the two sets share a path, else
cross-file (including a finding with no path). A merged pair is always same-file: same_defect_v2 needs a shared path
or an equal fingerprint, which contains the path.

No claim text: a finding whose card gives no claim text the converter reads (for example a markdown table without a
claim column; a claim that is missing or only whitespace) stays in the clustering, but every pair it is
part of is left out of the candidate pool, so no row carries a placeholder claim. The header line "no claim text:"
states how many pairs were left out this way. They are not candidates, so a side left short by them reports the
shortfall and INSUFFICIENT PAIRS like any other missing pair.

Row text: claim_a and claim_b are the converted claims. citations_a and citations_b list each citation as
"<role> <path>:<start>-<end> (<resolved|unresolved|malformed>)" against the snapshot, or "unresolved <ref text>" for a ref the converter
could not resolve, joined by " ; "; a finding with no citation shows "(no citation)".

Sampling: per side (merged, apart) n = min(25, candidate pairs of that side). Half of n rounded up is drawn from the
same-file candidates and the rest from the cross-file candidates; when one group is too small, the other fills the
gap. Each group is drawn with random.Random(f"{SEED}|{side}|{relation}").sample from candidates sorted by
(run, reviewer, finding id) of both findings. Rows are sorted by verdict (merged first), file relation, run and
finding keys, and numbered P01 onwards. The sheet holds no timestamp and no absolute path: the same cards give the
same bytes.

Sheet: comment lines starting with "#" come first (seed, rows per side, shortfall per side, pairs left out for no
claim text, candidate and sampled counts by file relation, status, label vocabulary), then one CSV header row and the data rows; the column
human_same_defect is left empty. Status is COMPLETE with 50 rows, else "INSUFFICIENT PAIRS"; sample then exits 1, so
a short sheet is never reported as a pass.

Labels: yes, no, y, n, true, false, in any letter case and with surrounding spaces ignored; yes, y and true mean the
two findings describe the same defect. score rejects any other value, naming the pair and the value.

Reading form: ``form --sheet <csv> --out <md>`` writes a plain-text form (the two claims in reading order, the
verdict hidden, one ``ANSWER P01: `` line per pair) for a person who cannot use the CSV; ``score --sheet <csv>
--answers <md>`` replaces human_same_defect with the filled ANSWER lines before scoring.

score: skips rows whose first cell starts with "#" (a comment line, also after a spreadsheet re-save) and empty rows,
needs the columns pair_id, cluster_v2_verdict and human_same_defect, and fails (exit 1) with a message naming every
pair whose label is missing or not in the vocabulary, every unknown verdict and every duplicate pair_id. Otherwise
it reports the confusion counts of cluster_v2 against the labels (TP merged and same, FP merged and not same, FN apart
and same, TN apart and not same), precision TP/(TP+FP) and recall TP/(TP+FN), each "undefined" when its denominator
is 0. Fewer than 50 scored rows prints INSUFFICIENT PAIRS and exits 1. A missing, unreadable or malformed sheet
exits 2 with the reason.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import random
import re
import sys
from pathlib import Path

from superclaude.cli.review import card_convert as cc
from superclaude.cli.review.cluster import annotate, cluster_v2

_REPLAY_PATH = Path(__file__).resolve().parent / "reflect_stage0a_replay.py"
_spec = importlib.util.spec_from_file_location("reflect_stage0a_replay", _REPLAY_PATH)
replay = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(replay)

SEED = 20261111
PER_SIDE = 25
TOTAL = 2 * PER_SIDE
SIDES = ("merged", "apart")
RELATIONS = ("same-file", "cross-file")
LABELS = {"yes": True, "y": True, "true": True, "no": False, "n": False, "false": False}
COLUMNS = (
    "pair_id",
    "run",
    "cluster_v2_verdict",
    "file_relation",
    "reviewer_a",
    "finding_a",
    "cluster_a",
    "claim_a",
    "citations_a",
    "reviewer_b",
    "finding_b",
    "cluster_b",
    "claim_b",
    "citations_b",
    "human_same_defect",
)
REQUIRED = ("pair_id", "cluster_v2_verdict", "human_same_defect")
INSUFFICIENT = "INSUFFICIENT PAIRS"


# --- sample ------------------------------------------------------------------------------------


def _citations_text(finding: dict, snapshot: set[str]) -> str:
    view = annotate(finding, snapshot)["citations"]
    parts = []
    for raw, v in zip(finding.get("citations") or [], view):
        if isinstance(raw, dict) and raw.get("role") == "unresolved":
            parts.append(f"unresolved {raw.get('ref', '')}")
        else:
            parts.append(
                f"{v['role']} {v['path']}:{v['line_start']}-{v['line_end']} ({v['status']})"
            )
    return " ; ".join(parts) or "(no citation)"


def _paths(finding: dict) -> set[str]:
    return {
        c["path"]
        for c in finding.get("citations") or []
        if isinstance(c, dict)
        and c.get("role") != "unresolved"
        and isinstance(c.get("path"), str)
    }


def _has_claim(finding: dict) -> bool:
    claim = finding.get("claim")
    return isinstance(claim, str) and bool(claim.strip())


def candidates(root: Path) -> tuple[list[dict], list[str], int]:
    """Every drawable pair (see "Pair", "Verdict" and "No claim text"), the runs that could not be read and the
    number of pairs left out because a finding has no claim text."""
    base = root / ".dev" / "reflect"
    runs = (
        sorted((p for p in base.glob("pre-*") if p.is_dir()), key=lambda p: p.name)
        if base.is_dir()
        else []
    )
    pairs: list[dict] = []
    problems: list[str] = []
    no_claim = 0
    for run in runs:
        cards_dir = run / "reviewer-cards"
        if not cards_dir.is_dir():
            continue
        try:
            cards, _ = replay._card_files(cards_dir)
        except OSError as exc:
            problems.append(
                f"{run.name}: reviewer-cards not listable ({exc.__class__.__name__})"
            )
            continue
        snapshot, _ = replay._snapshot(run)
        snap = set(snapshot)
        records, by_key = [], {}
        for ordinal, card in enumerate(cards):
            res = cc.convert_card_file(card)
            listed = res["shape"] != "unlisted"
            records.append(
                (card.stem, ordinal, res["findings"] if listed else None, {})
            )
            for f in res["findings"] if listed else []:
                by_key.setdefault((card.stem, f.get("id")), f)
        out = cluster_v2(records, snapshot)
        members = [
            (m["reviewer_id"], m["id"], c["cluster_id"], c["chained"])
            for c in out["clusters"]
            for m in c["members"]
        ]
        for i, (r1, f1, c1, chained) in enumerate(members):
            for r2, f2, c2, _ in members[i + 1 :]:
                if r1 == r2 or (c1 == c2 and chained):
                    continue
                # Order the two findings by (reviewer, id) so a pair has one spelling.
                (ra, fa, ca, a), (rb, fb, cb, b) = sorted(
                    [(r1, f1, c1, by_key[(r1, f1)]), (r2, f2, c2, by_key[(r2, f2)])],
                    key=lambda t: (t[0], t[1]),
                )
                if not (_has_claim(a) and _has_claim(b)):
                    no_claim += 1
                    continue
                pairs.append(
                    {
                        "run": run.name,
                        "cluster_v2_verdict": "merged" if ca == cb else "apart",
                        "file_relation": "same-file"
                        if _paths(a) & _paths(b)
                        else "cross-file",
                        "reviewer_a": ra,
                        "finding_a": fa,
                        "cluster_a": ca,
                        "claim_a": a["claim"],
                        "citations_a": _citations_text(a, snap),
                        "reviewer_b": rb,
                        "finding_b": fb,
                        "cluster_b": cb,
                        "claim_b": b["claim"],
                        "citations_b": _citations_text(b, snap),
                    }
                )
    return pairs, problems, no_claim


def _key(p: dict) -> tuple:
    return (p["run"], p["reviewer_a"], p["finding_a"], p["reviewer_b"], p["finding_b"])


def select(
    pairs: list[dict], seed: int = SEED, no_claim: int = 0
) -> tuple[list[dict], dict]:
    """The sampled rows (numbered, sorted) and the counts the sheet header states; no_claim is the third value
    candidates() returns."""
    groups = {
        (s, r): sorted(
            (
                p
                for p in pairs
                if p["cluster_v2_verdict"] == s and p["file_relation"] == r
            ),
            key=_key,
        )
        for s in SIDES
        for r in RELATIONS
    }
    rows: list[dict] = []
    stats: dict = {
        "candidates": {},
        "sampled": {},
        "shortfall": {},
        "no_claim": no_claim,
    }
    for s in SIDES:
        same, cross = groups[(s, "same-file")], groups[(s, "cross-file")]
        n = min(PER_SIDE, len(same) + len(cross))
        k_cross = min(n - min((n + 1) // 2, len(same)), len(cross))
        k_same = n - k_cross
        for rel, pool, k in (
            ("same-file", same, k_same),
            ("cross-file", cross, k_cross),
        ):
            rows += random.Random(f"{seed}|{s}|{rel}").sample(pool, k)
            stats["candidates"][(s, rel)] = len(pool)
            stats["sampled"][(s, rel)] = k
        stats["shortfall"][s] = PER_SIDE - n
    rows.sort(
        key=lambda p: (
            SIDES.index(p["cluster_v2_verdict"]),
            RELATIONS.index(p["file_relation"]),
            _key(p),
        )
    )
    rows = [
        {"pair_id": f"P{i:02d}", **p, "human_same_defect": ""}
        for i, p in enumerate(rows, 1)
    ]
    stats["rows"] = len(rows)
    return rows, stats


def render(rows: list[dict], stats: dict, seed: int = SEED) -> str:
    def side(s: str) -> str:
        return f"{s} {sum(stats['sampled'][(s, r)] for r in RELATIONS)} of {PER_SIDE}"

    def mix(key: str) -> str:
        return "; ".join(
            f"{s} same-file {stats[key][(s, 'same-file')]} cross-file {stats[key][(s, 'cross-file')]}"
            for s in SIDES
        )

    short = [f"{s} {stats['shortfall'][s]}" for s in SIDES if stats["shortfall"][s]]
    status = (
        "COMPLETE"
        if stats["rows"] >= TOTAL
        else f"{INSUFFICIENT} ({stats['rows']} rows; fewer than {TOTAL})"
    )
    buf = io.StringIO()
    for line in (
        f"cluster_v2 pair check sheet; scripts/reflect_cluster_pairs.py sample; seed {seed}",
        f"rows: {stats['rows']} of {TOTAL} ({side('merged')}; {side('apart')})",
        "shortfall: " + ("; ".join(short) if short else "none"),
        f"no claim text: {stats['no_claim']} pairs left out (a finding has no claim text after conversion)",
        f"candidates: {mix('candidates')}",
        f"sampled: {mix('sampled')}",
        f"status: {status}",
        "fill human_same_defect with yes or no (also y n true false in any case); "
        "then run: uv run python scripts/reflect_cluster_pairs.py score",
    ):
        buf.write(f"# {line}\n")
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


# --- score -------------------------------------------------------------------------------------


class SheetError(Exception):
    """The sheet cannot be read or has no usable structure (exit 2)."""


def read_sheet(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        raise SheetError(
            f"cannot read sheet {path}: {exc.__class__.__name__}: {exc}"
        ) from exc
    try:
        rows = [
            r
            for r in csv.reader(io.StringIO(text))
            if any(c.strip() for c in r) and not r[0].lstrip().startswith("#")
        ]
    except csv.Error as exc:
        raise SheetError(f"sheet {path} is not valid CSV: {exc}") from exc
    if not rows:
        raise SheetError(f"sheet {path} has no header row")
    header = [h.strip() for h in rows[0]]
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        raise SheetError(f"sheet {path} lacks the column(s): {', '.join(missing)}")
    return [
        {h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(header)}
        for r in rows[1:]
    ]


def score(rows: list[dict]) -> tuple[dict | None, list[str]]:
    """(the counts, None when a label or verdict problem exists) and the problem messages."""
    errors: list[str] = []
    missing, invalid, seen = [], [], set()
    counts = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for n, r in enumerate(rows, 1):
        pid = r["pair_id"] or f"data row {n}"
        if pid in seen:
            errors.append(f"duplicate pair_id {pid}")
        seen.add(pid)
        verdict = r["cluster_v2_verdict"].lower()
        if verdict not in SIDES:
            errors.append(
                f"{pid}: cluster_v2_verdict {r['cluster_v2_verdict']!r} is not merged or apart"
            )
        label = r["human_same_defect"]
        if not label:
            missing.append(pid)
            continue
        if label.lower() not in LABELS:
            invalid.append(f"{pid}={label!r}")
            continue
        if verdict in SIDES:
            same = LABELS[label.lower()]
            counts[
                ("TP" if same else "FP")
                if verdict == "merged"
                else ("FN" if same else "TN")
            ] += 1
    if not rows:
        errors.append("the sheet has no pair rows")
    if missing:
        errors.append(
            f"missing human_same_defect label for {len(missing)} pair(s): {', '.join(missing)}"
        )
    if invalid:
        errors.append(
            f"label not in yes/no/y/n/true/false for {len(invalid)} pair(s): {', '.join(invalid)}"
        )
    return (None if errors else counts), errors


def _ratio(num: int, den: int) -> str:
    return f"{num / den:.4f} ({num}/{den})" if den else f"undefined ({num}/0)"


def report(counts: dict) -> list[str]:
    tp, fp, fn, tn = (counts[k] for k in ("TP", "FP", "FN", "TN"))
    n = tp + fp + fn + tn
    return [
        f"pairs scored: {n}",
        f"confusion: TP={tp} FP={fp} FN={fn} TN={tn}",
        f"precision: {_ratio(tp, tp + fp)}",
        f"recall: {_ratio(tp, tp + fn)}",
        "status: SCORED"
        if n >= TOTAL
        else f"status: {INSUFFICIENT} ({n} rows; fewer than {TOTAL}; not a pass)",
    ]


# --- reading form ------------------------------------------------------------------------------

_ANSWER = re.compile(r"^ANSWER[ \t]+(\S+?)[ \t]*:[ \t]*(\S*)[ \t]*$", re.M)


def _short_cites(text: str) -> str:
    """The citations column with directories and resolved/unresolved marks dropped: file:lines only."""
    text = re.sub(r"\S*/([^/\s]+:\d+-\d+)", r"\1", text)
    return re.sub(r"\s*\((?:resolved|unresolved|malformed)\)", "", text)


def render_form(rows: list[dict]) -> str:
    """A plain-text form of the sheet for a human: the two claims side by side in reading order, no verdict shown."""
    out = [
        "# Same problem or not? (50 pairs)",
        "",
        "For each pair, read complaint A and complaint B. They come from two different reviewers of the same plan.",
        "Question: would ONE edit to the plan (or spec) fix both complaints? If yes, they are the same problem.",
        "Write yes or no after the colon on the line that starts with ANSWER. Do not change anything else.",
        "If one complaint lists several problems, answer yes when one of those problems is the other's problem.",
        "",
    ]
    for r in rows:
        pid = r["pair_id"]
        out += [
            f"## {pid}",
            "",
            f"A ({r.get('reviewer_a', '')}, finding {r.get('finding_a', '')}): {r.get('claim_a', '')}",
            f"   points at: {_short_cites(r.get('citations_a', ''))}",
            "",
            f"B ({r.get('reviewer_b', '')}, finding {r.get('finding_b', '')}): {r.get('claim_b', '')}",
            f"   points at: {_short_cites(r.get('citations_b', ''))}",
            "",
            f"ANSWER {pid}: ",
            "",
        ]
    return "\n".join(out)


def read_answers(path: Path) -> dict[str, str]:
    """{pair_id: answer} from the ANSWER lines of a filled form; a blank answer is left out."""
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        raise SheetError(
            f"cannot read answers {path}: {exc.__class__.__name__}: {exc}"
        ) from exc
    return {pid: ans for pid, ans in _ANSWER.findall(text) if ans}


# --- cli ---------------------------------------------------------------------------------------


def default_out(root: Path) -> Path:
    return replay.default_out(root).with_name("cluster-pairs-50.csv")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    for name, flag, text in (
        ("sample", "--out", "sheet to write"),
        ("score", "--sheet", "filled sheet to score"),
    ):
        p = sub.add_parser(name)
        p.add_argument(
            "--root",
            type=Path,
            default=Path(__file__).resolve().parent.parent,
            help="repository root",
        )
        p.add_argument(
            flag,
            type=Path,
            default=None,
            help=f"{text} (default: the plan package artifact)",
        )
        if name == "score":
            p.add_argument(
                "--answers",
                type=Path,
                default=None,
                help="filled reading form (see the form mode); its ANSWER lines replace the sheet's human_same_defect",
            )
    form = sub.add_parser("form")
    form.add_argument("--sheet", type=Path, required=True, help="sheet to read")
    form.add_argument("--out", type=Path, required=True, help="reading form to write")
    args = parser.parse_args(argv)
    if args.mode == "form":
        try:
            rows = read_sheet(args.sheet)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(render_form(rows), encoding="utf-8")
        except (SheetError, OSError) as exc:
            print(f"form failed: {exc}", file=sys.stderr)
            return 2
        print(f"wrote {args.out} ({len(rows)} pairs)")
        return 0
    root = args.root.resolve()
    if args.mode == "sample":
        out = args.out or default_out(root)
        pairs, problems, no_claim = candidates(root)
        rows, stats = select(pairs, no_claim=no_claim)
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(rows, stats), encoding="utf-8")
        except OSError as exc:
            print(
                f"cannot write {out}: {exc.__class__.__name__}: {exc}", file=sys.stderr
            )
            return 2
        for p in problems:
            print(f"skipped run {p}", file=sys.stderr)
        print(f"wrote {out}")
        print(
            f"rows={stats['rows']} merged={sum(stats['sampled'][('merged', r)] for r in RELATIONS)} "
            f"apart={sum(stats['sampled'][('apart', r)] for r in RELATIONS)} "
            f"shortfall merged={stats['shortfall']['merged']} apart={stats['shortfall']['apart']}"
        )
        if stats["rows"] < TOTAL:
            print(
                f"{INSUFFICIENT}: {stats['rows']} rows, fewer than {TOTAL}; not a pass"
            )
            return 1
        print("status: COMPLETE")
        return 0
    sheet = args.sheet or default_out(root)
    try:
        rows = read_sheet(sheet)
    except SheetError as exc:
        print(f"score failed: {exc}", file=sys.stderr)
        return 2
    if args.answers:
        try:
            answers = read_answers(args.answers)
        except SheetError as exc:
            print(f"score failed: {exc}", file=sys.stderr)
            return 2
        unknown = sorted(set(answers) - {r["pair_id"] for r in rows})
        if unknown:
            print(
                f"score failed: ANSWER line(s) for unknown pair(s): {', '.join(unknown)}",
                file=sys.stderr,
            )
            return 1
        for r in rows:
            if r["pair_id"] in answers:
                r["human_same_defect"] = answers[r["pair_id"]]
    counts, errors = score(rows)
    if counts is None:
        for e in errors:
            print(f"score failed: {e}", file=sys.stderr)
        return 1
    lines = report(counts)
    print("\n".join(lines))
    return 0 if lines[-1] == "status: SCORED" else 1


if __name__ == "__main__":
    sys.exit(main())
