#!/usr/bin/env python3
"""make-schedule.py: the block-randomised run schedule (DESIGN 11.6, REQ-29, REQ-32).

    make-schedule.py --stage 1 --arms z0,k,ss --docs HO-1,HO-2,HO-3,HO-4 --reps 5 --seed 20261115 --out FILE
    make-schedule.py --stage 1 --arms z0raw --docs HO-1,HO-2,HO-3 --reps 5 --seed 20261115 --append FILE
    options: --set NAME (default holdout; planted, twins, spec, docs, derivation ...), --panel primary|haiku|sonnet

One line per (stage, block, arm, document, replicate). There is one block per replicate, so the arms of a block are run
together and compared with each other and never with a run from another day (REQ-29). The order inside a block is shuffled
with a generator seeded from the recorded seed, the stage and the block, so the same arguments give the same file.
`--append` adds rows to an existing schedule: the new rows join the blocks of the same numbers and each block is shuffled
again from the seed, so that Z0-raw runs on the day of the Z0 runs that they are compared with. The file is a tab separated
table whose first line is a comment with the seed:

    # make-schedule seed=20261115
    stage  block  arm  panel  doc  replicate  seed  set  run

`run` is the folder name of the run under runs/stage<stage>/ (bin/run-schedule.sh). The `seed` column is the pre-pass seed
that run-panel.sh records (the same recorded seed for every row). Output goes only under the sweep-sheet folder or /tmp.
"""

import argparse
import random
import re
import sys
from pathlib import Path

SW = Path(__file__).resolve().parents[1]
ARMS = {"z0raw": "Z0-raw", "z0": "Z0", "k": "K", "ss": "SS"}
PANELS = ("primary", "haiku", "sonnet")
COLUMNS = ("stage", "block", "arm", "panel", "doc", "replicate", "seed", "set", "run")
DOC = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
STAGE = re.compile(r"^[0-9a-z]+$")
ARM_ORDER = tuple(ARMS.values())


class ScheduleError(Exception):
    pass


def run_id(stage, arm, panel, doc, rep):
    """The run folder name: stage, arm without hyphen, panel when it is not the primary one, document, replicate."""
    p = "" if panel == "primary" else f"{panel}-"
    return f"s{stage}-{arm.lower().replace('-', '')}-{p}{doc}-r{rep}"


def rows_for(stage, arms, docs, reps, seed, panel, set_name):
    out = []
    for block in range(1, reps + 1):
        for arm in arms:
            for doc in docs:
                out.append(
                    {
                        "stage": stage,
                        "block": block,
                        "arm": arm,
                        "panel": panel,
                        "doc": doc,
                        "replicate": block,
                        "seed": seed,
                        "set": set_name,
                        "run": run_id(stage, arm, panel, doc, block),
                    }
                )
    return out


def shuffle_blocks(rows, seed):
    """Group rows by (stage, block) in ascending order and shuffle each group with a generator seeded from the seed, the
    stage and the block. The rows are sorted first, so the result does not depend on the order they arrived in."""
    groups = {}
    for r in rows:
        groups.setdefault((r["stage"], r["block"]), []).append(r)
    out = []
    for (stage, block), g in sorted(groups.items()):
        g.sort(key=lambda r: (ARM_ORDER.index(r["arm"]), r["panel"], r["doc"]))
        random.Random(f"{seed}:{stage}:{block}").shuffle(g)
        out += g
    return out


def render(rows, seed) -> str:
    lines = [f"# make-schedule seed={seed}", "\t".join(COLUMNS)]
    lines += ["\t".join(str(r[c]) for c in COLUMNS) for r in rows]
    return "\n".join(lines) + "\n"


def read(path):
    """(seed, rows) of a schedule file."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    m = re.match(r"# make-schedule seed=(\d+)$", lines[0]) if lines else None
    if not m or len(lines) < 2 or lines[1].split("\t") != list(COLUMNS):
        raise ScheduleError(f"{path} is not a schedule file")
    rows = []
    for ln in lines[2:]:
        f = ln.split("\t")
        if len(f) != len(COLUMNS):
            raise ScheduleError(
                f"{path}: a row has {len(f)} columns, not {len(COLUMNS)}"
            )
        r = dict(zip(COLUMNS, f))
        r["block"], r["replicate"], r["seed"] = (
            int(r["block"]),
            int(r["replicate"]),
            int(r["seed"]),
        )
        rows.append(r)
    return int(m.group(1)), rows


def writable(path) -> Path:
    """K1: output only under SW or /tmp."""
    p = Path(path).resolve()
    if SW in p.parents or Path("/tmp") in p.parents:
        return p
    raise ScheduleError(f"E_NOT_WRITABLE: {path} resolves to {p}")


def build(args) -> tuple[int, list]:
    arms = []
    for a in (x for x in args.arms.split(",") if x):
        if a.lower() not in ARMS:
            raise ScheduleError(f"unknown arm {a}: use {', '.join(ARMS)}")
        arms.append(ARMS[a.lower()])
    docs = [d for d in args.docs.split(",") if d]
    if not arms or not docs:
        raise ScheduleError("--arms and --docs each need at least one name")
    for d in docs:
        if not DOC.match(d):
            raise ScheduleError(f"bad document id {d}")
    if not STAGE.match(args.stage):
        raise ScheduleError(f"bad stage {args.stage}")
    if args.panel not in PANELS or args.reps < 1:
        raise ScheduleError(
            "--panel must be primary, haiku or sonnet and --reps at least 1"
        )
    new = rows_for(
        args.stage,
        dict.fromkeys(arms),
        dict.fromkeys(docs),
        args.reps,
        args.seed,
        args.panel,
        args.set,
    )
    return args.seed, new


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="make-schedule.py", description=__doc__.split("\n")[0]
    )
    ap.add_argument("--stage", required=True, help="1, 2 or d (derivation)")
    ap.add_argument("--arms", required=True, help="comma separated: z0raw, z0, k, ss")
    ap.add_argument("--docs", required=True, help="comma separated document ids")
    ap.add_argument("--reps", type=int, required=True, help="replicates = blocks")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument(
        "--panel", default="primary", help="primary (ember + 2x luna), haiku or sonnet"
    )
    ap.add_argument(
        "--set", default="holdout", help="the document set, recorded in each row"
    )
    out = ap.add_mutually_exclusive_group(required=True)
    out.add_argument("--out", help="write a new schedule (refuses to replace a file)")
    out.add_argument(
        "--append", help="add the rows to this schedule and shuffle each block again"
    )
    args = ap.parse_args(argv)
    try:
        seed, new = build(args)
        if args.append:
            dest = writable(args.append)
            old_seed, old = read(dest)
            if old_seed != seed:
                raise ScheduleError(
                    f"the file has seed {old_seed}, not {seed}: one schedule has one seed"
                )
            have = {
                (r["stage"], r["arm"], r["panel"], r["doc"], r["replicate"])
                for r in old
            }
            dup = [
                r["run"]
                for r in new
                if (r["stage"], r["arm"], r["panel"], r["doc"], r["replicate"]) in have
            ]
            if dup:
                raise ScheduleError(f"already in the schedule: {', '.join(dup[:3])}")
            rows = shuffle_blocks(old + new, seed)
        else:
            dest = writable(args.out)
            rows = shuffle_blocks(new, seed)
            # the same arguments give the same file, so a repeat is a no-op; a different schedule never replaces one
            if dest.exists() and dest.read_text(encoding="utf-8") != render(rows, seed):
                raise ScheduleError(
                    f"{dest} exists with other content: a schedule is never replaced"
                )
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(rows, seed), encoding="utf-8")
    except (ScheduleError, OSError) as e:
        print(f"make-schedule: {e}", file=sys.stderr)
        return 2
    print(f"{dest}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
