"""F-PLAN-3 (TESTING section 2): write a plan with N set-word criterion sentences, spread over the tasks of one plan.

    uv run ... python gen_setwords.py [--n 200] [--tasks 12] [--out PATH]

The plan is in the `plan` format of sweep/formats.py. Each of the N acceptance bullets is one sentence with exactly one
kind of set word: about two in three hold a completeness word (every, all, each, complete, found, covers, no
remaining), the rest a universal word (only, never, no other). Every fourth sentence names no file, every fourth names a
glob, every fourth names two files and every fourth holds a count, so the bound types of DESIGN 4.2 all occur. The
output depends on the arguments only (no clock, no random numbers). Everything is invented. Standard library only.
"""

import argparse
import sys
from pathlib import Path

NOUNS = (
    "parcel",
    "ticket",
    "badge",
    "voucher",
    "manifest",
    "receipt",
    "coupon",
    "label",
    "permit",
    "token",
)
FIELDS = ("owner", "stamp", "colour", "weight", "origin", "batch", "zone", "grade")
VERBS = ("scan", "sort", "pack", "match", "audit", "route")

# sentence frames: {n} noun, {f} field, {fn} a unique backticked function name
COMPLETENESS = (
    "Every {n} record returned by `{fn}` carries the {f} value",
    "All {n} records that `{fn}` reads are checked before the step ends",
    "Each {n} listed in the `{fn}` output has its {f} entry",
    "The {n} list built by `{fn}` is complete",
    "`{fn}` covers the {n} cases of the step",
    "No remaining {n} rows are found by `{fn}`",
)
UNIVERSAL = (
    "Only `{fn}` writes the {n} {f} file",
    "The {n} step never calls `{fn}` twice",
    "No other {n} helper changes the {f} state kept by `{fn}`",
)
# bound clause appended to a sentence, by i % 4
BOUNDS = (
    "",
    " under `src/svc{t:02d}/*.py`",
    " in `src/svc{t:02d}/a_{i:03d}.py` and `src/svc{t:02d}/b_{i:03d}.py`",
    " for the first {c} {n} files",
)


def sentence(i: int, t: int) -> str:
    """The i-th criterion sentence (0-based), written for task t (1-based)."""
    n, f = NOUNS[i % len(NOUNS)], FIELDS[(i // len(NOUNS)) % len(FIELDS)]
    fn = f"{VERBS[i % len(VERBS)]}_{n}_{i:03d}"
    pool = UNIVERSAL if i % 3 == 2 else COMPLETENESS
    frame = pool[(i // 3) % len(pool)]
    bound = BOUNDS[i % 4].format(t=t, i=i, n=n, c=3 + i % 5)
    return frame.format(n=n, f=f, fn=fn) + bound + "."


def generate(n: int = 200, tasks: int = 12) -> str:
    """The plan text. `tasks` is cut to `n` so that no task is empty."""
    if n < 1 or tasks < 1:
        raise ValueError("n and tasks must be at least 1")
    tasks = min(tasks, n)
    out = [
        "---",
        "schema: workflow-plan/1.2",
        "strategy: systematic",
        "depth: standard",
        "slug: TASK-WF-setwords-20261114-000003",
        'version: "1"',
        "priority: Medium",
        'created_date: "2026-11-14"',
        "---",
        "",
        "# Tighten the parcel handling steps",
        "",
        f"Goal: `make test` exits 0 after the {tasks} tasks below are done.",
        "",
        "## Constraints",
        "",
        "- Code lives under `src/` and tests under `tests/`.",
        "",
    ]
    base, extra = divmod(n, tasks)
    i = 0
    for t in range(1, tasks + 1):
        if t == 1 or t == tasks // 2 + 1:
            out += [f"## Phase {1 if t == 1 else 2}: Steps {t} onward", ""]
        out += [
            f"## Task {t}: Tighten step {t}",
            "",
            f"Edit `src/svc{t:02d}/module.py` so that step {t} handles the {NOUNS[t % len(NOUNS)]} records of its zone.",
            "",
            "Acceptance criteria:",
        ]
        for _ in range(base + (t <= extra)):
            out.append(f"- {sentence(i, t)}")
            i += 1
        out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--n", type=int, default=200, help="criterion sentences (default 200)"
    )
    ap.add_argument("--tasks", type=int, default=12, help="tasks (default 12)")
    ap.add_argument("--out", help="file to write (default: standard output)")
    a = ap.parse_args(argv)
    try:
        text = generate(a.n, a.tasks)
    except ValueError as e:
        print(f"gen_setwords: {e}", file=sys.stderr)
        return 2
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
