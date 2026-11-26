"""The `ran` cross-check of the ledger rows (DESIGN 7.7, REQ-28, DR-10). Analysis only; it is not a gate.

THIS IS A HEURISTIC. It compares what a reviewer wrote in the `ran` field of a ledger row with the tool calls of its
own transcript. A person has not yet audited its agreement with a careful reading (TESTING REQ-28, row M, the 20-row
audit that `bin/open-manual-checks.sh ran-audit` prints), so a number from it is a signal, not a finding.

    ran_check.py RUN_DIR... [--out FILE]
        RUN_DIR is a run folder (it has `reviews/`) or a folder of run folders. For each reviewer the rows come from
        `reviews/<rid>.md` (the final message, through scaffold/ledgerv1.read) and the tool calls from
        `reviews/<rid>.attempt1.json` (a list of events). Writes FILE (default RL/results/ran.md); prints the totals.

Rules, from DESIGN 7.7 (a call is a `tool_use` block with the text of its `result`, whether the result is a string or an
array of text blocks, as found in Task 1):
    not_a_tool_claim  `ran` names no command word and the recipe is not C5, C6 or C8.
    verified          the row is a tool claim and one call matches it: a call matches when it carries the claimed command
                      word (a `Bash` call whose command contains it; a search by a non-Bash tool counts for any word, as
                      the Task 1 decision says) and either shares a distinctive token (four or more letters, not a command
                      word, not in COMMON) with `ran` or `quote_other`, or has a result that contains `quote_other`.
    unverified        any other tool claim. A row of C5, C6 or C8 is always a tool claim; when it names no command word
                      the word test is dropped (a row of those recipes names the search or it is not credited), and when
                      the transcript has no search call at all (a `Bash` call with grep, egrep, rg or find; a call of
                      Grep, mcp__codegraph__* or mcp__litellm__*) it is `unverified` whatever `ran` says, a `NONE FOUND`
                      row included.
Reading a candidate cannot be verified (`claude -p` may attach the `@file` text without a `Read` call), so `Read` calls
count for nothing here.

Reported per reviewer and per class: the count of each status and the share of search-recipe rows that are `unverified`
(the "OK row written without doing the step" signal of MR 3.2(i)).
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_RL = os.path.dirname(_HERE)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]
if _RL not in sys.path:
    sys.path.insert(0, _RL)

import argparse  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

from scaffold import fnd, ledgerv1, telemetry  # noqa: E402

RL = Path(_RL)
STATUSES = ("not_a_tool_claim", "verified", "unverified")
COMMAND_WORDS = (
    "grep egrep rg git printf find ls cat sed awk wc head tail pytest jq".split()
)
SEARCH_RECIPES = ("C5", "C6", "C8")
SEARCH_BASH_WORDS = ("grep", "egrep", "rg", "find")
SEARCH_TOOLS = ("Grep", "mcp__codegraph__", "mcp__litellm__")
# four-letter words that appear in almost every row and so share nothing
COMMON = frozenset(
    "none found with that this from into read text task plan each both then only line lines file files what have over "
    "also after before where which print prints output check checked compared ran step steps rows row item".split()
)
_WORD = re.compile(r"\b(" + "|".join(COMMAND_WORDS) + r")\b", re.I)
_TOKEN = re.compile(r"[a-z]{4,}")
_REVIEW_MD = re.compile(r"^[^.]+\.md$")


# ---------------------------------------------------------------- the transcript


def calls_of(events):
    """[{name, text, result, search}] of the tool calls of a transcript: `text` is the Bash command or the input values
    of any other tool; `result` is the text of its tool_result; `search` says whether the call is a search."""
    if isinstance(events, (str, bytes)):
        events = json.loads(events)
    results = {}
    for ev in events or []:
        content = (
            (ev.get("message") or {}).get("content")
            if ev.get("type") == "user"
            else None
        )
        for b in content if isinstance(content, list) else []:
            if isinstance(b, dict) and b.get("type") == "tool_result":
                one = {"type": "user", "message": {"content": [b]}}
                results[b.get("tool_use_id")] = ledgerv1.transcript_text([one])
    calls = []
    for ev in events or []:
        content = (
            (ev.get("message") or {}).get("content")
            if ev.get("type") == "assistant"
            else None
        )
        for b in content if isinstance(content, list) else []:
            if not isinstance(b, dict) or b.get("type") != "tool_use":
                continue
            name, inp = b.get("name") or "", b.get("input") or {}
            bash = name == "Bash"
            text = (
                str(inp.get("command", ""))
                if bash
                else " ".join(map(str, inp.values()))
            )
            if bash:
                search = any(re.search(rf"\b{w}\b", text) for w in SEARCH_BASH_WORDS)
            else:
                search = name.startswith(SEARCH_TOOLS)
            calls.append(
                {
                    "name": name,
                    "text": text,
                    "result": results.get(b.get("id"), ""),
                    "search": search,
                }
            )
    return calls


# ---------------------------------------------------------------- one row


def _tokens(text):
    return set(_TOKEN.findall(text.lower())) - COMMON - set(COMMAND_WORDS)


def ran_status(row, calls):
    """`not_a_tool_claim`, `verified` or `unverified` for one ledger row and the calls of its transcript."""
    words = {w.lower() for w in _WORD.findall(row["ran"])}
    recipe = telemetry.class_of(row["item"])
    search_recipe = recipe in SEARCH_RECIPES
    if not words and not search_recipe:
        return "not_a_tool_claim"
    if search_recipe and not any(c["search"] for c in calls):
        return "unverified"
    mine = _tokens(row["ran"] + " " + row["quote_other"])
    quote = row["quote_other"]
    for c in calls:
        if (
            not words
        ):  # a search recipe row that names no command: any search call can answer it
            carries = c["search"]
        else:
            carries = (c["name"] != "Bash" and c["search"]) or any(
                re.search(rf"\b{w}\b", c["text"], re.I) for w in words
            )
        if not carries:
            continue
        if mine & _tokens(c["text"]) or (
            quote and ledgerv1.contains(fnd.flat(c["result"]), quote)
        ):
            return "verified"
    return "unverified"


# ---------------------------------------------------------------- run folders


def run_dirs_of(paths):
    """Run folders named on the command line: a folder with `reviews/`, or a folder of such folders."""
    out = []
    for p in map(Path, paths):
        if (p / "reviews").is_dir():
            out.append(p)
        else:
            out += [d for d in sorted(p.iterdir()) if (d / "reviews").is_dir()]
    return out


def check_run(run):
    """The rows of one run folder with their `ran_status`: [{run, reviewer, item, class, ran, status}]."""
    rows = []
    for md in sorted((Path(run) / "reviews").iterdir()):
        if not _REVIEW_MD.match(md.name):
            continue
        rid = md.stem
        led = ledgerv1.read(md.read_text(encoding="utf-8"))
        tpath = md.with_name(f"{rid}.attempt1.json")
        calls = calls_of(tpath.read_text(encoding="utf-8")) if tpath.is_file() else []
        for r in led["rows"]:
            rows.append(
                {
                    "run": Path(run).name,
                    "reviewer": rid,
                    "item": r["item"],
                    "class": telemetry.class_of(r["item"]),
                    "ran": r["ran"],
                    "status": ran_status(r, calls),
                }
            )
    return rows


def _count(rows, key):
    out = {}
    for r in rows:
        out.setdefault(r[key] or "?", dict.fromkeys(STATUSES, 0))[r["status"]] += 1
    return dict(sorted(out.items()))


def summarise(rows):
    """Counts per reviewer and per class, and the share of search-recipe rows that are unverified."""
    search = [r for r in rows if r["class"] in SEARCH_RECIPES]
    bad = sum(r["status"] == "unverified" for r in search)
    return {
        "rows": len(rows),
        "per_reviewer": _count(rows, "reviewer"),
        "per_class": _count(rows, "class"),
        "total": {s: sum(r["status"] == s for r in rows) for s in STATUSES},
        "search_rows": len(search),
        "search_unverified": bad,
        "search_unverified_share": bad / len(search) if search else None,
    }


def _table(title, counts):
    lines = [
        f"| {title} | rows | " + " | ".join(STATUSES) + " |",
        "|---|---|" + "---|" * len(STATUSES),
    ]
    for k, c in counts.items():
        lines.append(
            f"| {k} | {sum(c.values())} | "
            + " | ".join(str(c[s]) for s in STATUSES)
            + " |"
        )
    return lines


def report(rows):
    s = summarise(rows)
    share = s["search_unverified_share"]
    lines = [
        "# The `ran` cross-check (DESIGN 7.7, REQ-28)",
        "",
        "This is a heuristic, not a measurement: it compares the `ran` field of each ledger row with the tool calls of the",
        "reviewer's own transcript, and nobody has yet checked its agreement with a person's reading (REQ-28, row M).",
        "It is not a gate.",
        "",
        f"Rows: {s['rows']}. "
        + ", ".join(f"{k}: {v}" for k, v in s["total"].items())
        + ".",
        "Search-recipe rows (C5, C6, C8) that are unverified: "
        + (
            f"{s['search_unverified']} of {s['search_rows']} ({share:.3f})"
            if share is not None
            else "none, there are no such rows"
        )
        + ".",
        "",
        *_table("reviewer", s["per_reviewer"]),
        "",
        *_table("class", s["per_class"]),
        "",
        "| run | reviewer | item | status |",
        "|---|---|---|---|",
        *(
            f"| {r['run']} | {r['reviewer']} | {r['item']} | {r['status']} |"
            for r in rows
        ),
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--out", default=str(RL / "results" / "ran.md"))
    a = ap.parse_args(argv)
    rows = [r for d in run_dirs_of(a.runs) for r in check_run(d)]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report(rows), encoding="utf-8")
    s = summarise(rows)
    print(
        f"{s['rows']} rows: {s['total']}; search rows unverified {s['search_unverified']} of {s['search_rows']}; wrote {out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
