"""One-time copy of the quoted blocks of MR and the RR brief into briefs/ (IMPLEMENTATION step 4, DESIGN 8.1).

Run once:  uv run --frozen --project REPO python SW/results/copy-briefs.py

The files are written from the LINE NUMBERS DESIGN 8.1 names (RR 13-17; MR 205, 209, 213, 217, 221, 291, 465). Each
written file is then compared with the extraction the test uses (scaffold.briefs: found by opening words, not by line
number), and the unified diff is printed. An empty diff for every file means the script and the test agree. Exit 1
when any diff is not empty. briefs/k-lead.txt is a hand-written draft and is not touched here.
"""

import difflib
import sys
from pathlib import Path

SW = Path(__file__).resolve().parents[1]
REPO = SW.parents[3]
sys.path.insert(0, str(SW))

from scaffold import briefs  # noqa: E402

MR = (
    REPO
    / ".dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md"
)
RR = (
    REPO
    / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh"
)
MR_LINES = {
    "cb1": 205,
    "cb2": 209,
    "cb3": 213,
    "cb4": 217,
    "cb5": 221,
    "ledger-rule": 291,
    "sheet-block": 465,
}
RR_FIRST, RR_LAST = 13, 17


def by_line_number() -> dict[str, str]:
    """{part: text}: MR lines `> "<text>"` and the RR BRIEF string, taken by line number."""
    mr = MR.read_text(encoding="utf-8").split("\n")
    out = {}
    for name, n in MR_LINES.items():
        line = mr[n - 1]
        assert line.startswith('> "') and line.endswith('"'), (name, n)
        out[name] = line[3:-1]
    rr = RR.read_text(encoding="utf-8").split("\n")[RR_FIRST - 1 : RR_LAST]
    assert rr[0].startswith('BRIEF="') and rr[-1].endswith('"')
    out["base"] = "\n".join(rr)[len('BRIEF="') : -1]
    return out


def main() -> int:
    copied = by_line_number()
    mr_text = MR.read_text(encoding="utf-8")
    first, last, base = briefs.rr_brief(RR.read_text(encoding="utf-8"))
    expected = {n: briefs.mr_quote(mr_text, o) for n, o in briefs.MR_OPENINGS.items()}
    expected["base"] = base
    print(
        f"test extraction of RR: lines {first}-{last} (script uses {RR_FIRST}-{RR_LAST})"
    )
    briefs.BRIEFS_DIR.mkdir(exist_ok=True)
    bad = 0
    for name in ("base", *MR_LINES):
        path = briefs.BRIEFS_DIR / briefs.FILES[name]
        path.write_text(copied[name], encoding="utf-8")
        diff = list(
            difflib.unified_diff(
                expected[name].splitlines(keepends=True),
                path.read_text(encoding="utf-8").splitlines(keepends=True),
                "test-extraction",
                str(path.relative_to(SW)),
            )
        )
        bad += bool(diff)
        print(
            f"{path.relative_to(SW)}: {len(copied[name])} chars, diff lines {len(diff)}"
        )
        sys.stdout.writelines(diff)
    print("DIFF" if bad else "AGREE: every file equals the test extraction")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
