"""Item JSON and reviewer sheets (DESIGN 6, 7.3, DD-6; TESTING DD-6 row).

Input is what select.py and assign.py produce: the selected item rows (`item_id`, `class`, `extractor`, `kind`,
`anchor_text`, `location`, `evidence`, `priority`, `experimental`) and an `Assignment` (per-reviewer item ids already
in the shuffled print order, replica targets, dropped items). Output, for every reviewer that has an entry in the
assignment:

    sheets/<rid>.md    the sheet text (DESIGN 6.3), items in that reviewer's shuffled order
    sheets/<rid>.json  the same items with all 6.1 fields plus extractor and kind, `sheet_trimmed` and `chars`

The sheet shows the class id only: never the extractor, the kind, the priority or the route (6.1). It is capped at
16,000 characters (SHEET_CAP): when it is longer, evidence entries are removed from the lowest-priority items, the last
entry of an item first, until it fits, and `sheet_trimmed` is true. JSON follows DESIGN 2.4 (sorted keys, ensure_ascii
False, trailing newline, nothing absolute). Nothing here reads a clock, the network or a random source.

Gaps in DESIGN 6 resolved here (each is a choice the design leaves open):
  R1  Evidence line form. DESIGN 4.3 prints `plan line 85: ...` and DESIGN 6.3 prints `[plan L85] ...`; 4.3 is the
      printed-tool-output example, so it wins. An entry with a line number prints `<path> line N: <text>` for `plan`
      and `source`, and `<path>:N: <text>` for a repository file. Entries that follow with the same path and line
      continue the first one and print the text alone, which reproduces the 4.3 example (three facts about plan line
      85, then the base-checkout line). An entry with line 0 (a fact about a whole file, the extractors' convention)
      prints its text alone; that text already names the file.
  R2  `location.task`. Extractors give the plan task id (`T4`) or None. The item JSON writes `Task 4`; None becomes
      `Goal` or `Constraints` when the parsed plan (`doc`) shows which block holds the line, else `Plan`. With `doc`,
      a criterion block adds `location.part` (`acceptance criterion 2`), which `Where:` prints as in 6.3.
  R3  The C3 placeholder `«value»` is filled with the literal named by the E6 evidence line `write-position
      occurrences of '<literal>': 0`; failing that, the first backticked span of the anchor; failing that, the whole
      anchor. The fill is wrapped in single quotes.
  R4  `Text:` prints the anchor with its whitespace collapsed to single spaces (a collapsed exact quote is still an exact
      quote under findings.flat), so an item stays four plain lines.
  R5  The `Note:` line of an experimental item comes after the tool output and before the question.
  R6  The sheet text and the file have no trailing newline, so the text scaffold/briefs.py places after
      `## SWEEP SHEET ITEMS` (which strips trailing newlines) is byte-equal to the file.
  R7  A reviewer with no items gets an empty sheet text (no header line), which briefs.render treats as an empty
      sheet. Items in `assignment.dropped` (dropped:cap_slots) are on no sheet and not in the item JSON.
  R8  `replicas` is the replica target of the assignment (DESIGN 7.2 step 1), not the count actually placed;
      `assignment.json: replica_dropped` records the shortfall.
  R9  Trim order. Lowest `priority` first; equal priorities: the higher item number first (items.json numbers items
      in descending priority). If every entry is gone and the sheet is still over the cap, the sheet is written as it
      is with `sheet_trimmed` true; `chars` in the JSON shows the overflow.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from scaffold import cards as cards_mod
from sweep.select import dumps

SHEET_CAP = 16000
HEADER = "Items assigned to you: "
EXPERIMENTAL_NOTE = (
    "Note: this item comes from a low-trust extractor; most such items are fine."
)
REPLY = "Reply with one line in the ledger-v1 block: item {id}, verdict OK, PROBLEM or UNSURE."
PLACEHOLDER = "«value»"
ITEM_FIELDS = (
    "item_id",
    "class",
    "anchor_text",
    "location",
    "evidence",
    "question",
    "priority",
    "experimental",
    "replicas",
    "extractor",
    "kind",
)  # DESIGN 6.1 plus the `extractor` and `kind` that items.json lists; the sheet text uses none of the last three
_LITERAL = re.compile(r"write-position occurrences of '(.+)': 0$")
_BACKTICKED = re.compile(r"`([^`\n]+)`")
_CRITERION_ID = re.compile(r"\.C(\d+)$")


@dataclass
class Sheet:
    rid: str
    text: str
    trimmed: bool
    items: list[dict]  # as printed (evidence after trimming), in print order

    def to_json(self) -> dict:
        return {
            "rid": self.rid,
            "sheet_trimmed": self.trimmed,
            "chars": len(self.text),
            "items": self.items,
        }


def _flat(s: str) -> str:
    return " ".join(s.split())


def _task_label(task) -> str | None:
    if task is None:
        return None
    t = str(task)
    m = re.fullmatch(r"T(\S+)", t)
    return f"Task {m.group(1)}" if m else t


def _location(loc: dict, doc=None) -> dict:
    """R2: the 6.1 location with a readable `task`, and `part` when the parsed plan names the criterion."""
    out = {
        "task": _task_label(loc.get("task")),
        "line_start": loc["line_start"],
        "line_end": loc["line_end"],
    }
    if loc.get("part"):
        out["part"] = loc["part"]
    line = loc["line_start"]
    if doc is not None:
        for b in doc.blocks:
            if (
                b["kind"] not in ("criterion", "constraint")
                or not b["line_start"] <= line <= b["line_end"]
                or b.get("task") != loc.get("task")
            ):
                continue
            if b["kind"] == "criterion" and b["id"] == "goal":
                out["task"] = "Goal"
            elif b["kind"] == "criterion":
                m = _CRITERION_ID.search(b["id"])
                if m:
                    out["part"] = f"acceptance criterion {m.group(1)}"
            elif out["task"] is None:
                out["task"] = "Constraints"
    if out["task"] is None:
        out["task"] = "Plan"
    return out


def question_for(item: dict, cards: dict[str, dict] | None = None) -> str:
    """The printed question of the item's class card; the C3 placeholder is filled (R3)."""
    q = cards_mod.questions(cards)[item["class"]]
    if PLACEHOLDER in q:
        lit = next(
            (m.group(1) for e in item["evidence"] if (m := _LITERAL.search(e["text"]))),
            None,
        )
        if lit is None:
            m = _BACKTICKED.search(item["anchor_text"])
            lit = m.group(1) if m else _flat(item["anchor_text"])
        q = q.replace(PLACEHOLDER, f"'{lit}'")
    return q


def item_json(
    row: dict, replicas: int = 1, cards: dict[str, dict] | None = None, doc=None
) -> dict:
    """One item with the fields and limits of DESIGN 6.1 (and `extractor`, `kind`), from a select.py row."""
    out = {
        "item_id": row["item_id"],
        "class": row["class"],
        "anchor_text": row["anchor_text"],
        "location": _location(row["location"], doc),
        "evidence": [dict(e) for e in row["evidence"]],
        "priority": row["priority"],
        "experimental": bool(row.get("experimental")),
        "replicas": replicas,
        "extractor": row["extractor"],
        "kind": row["kind"],
    }
    out["question"] = question_for(out, cards)
    if not (
        len(out["anchor_text"]) <= 200
        and len(out["evidence"]) <= 5
        and all(len(e["text"]) <= 160 for e in out["evidence"])
        and 0 <= out["priority"] <= 100
        and out["replicas"] in (1, 2)
    ):
        raise ValueError(f"item {out['item_id']} breaks a limit of DESIGN 6.1")
    return {k: out[k] for k in ITEM_FIELDS}


def items_json(rows, assignment, cards=None, doc=None) -> dict:
    """The items of the run in 6.1 form (rows in input order, dropped:cap_slots items left out); `seed` as select.py."""
    return {
        "seed": assignment.seed,
        "items": [
            item_json(r, assignment.replicas.get(r["item_id"], 1), cards, doc)
            for r in rows
            if r["item_id"] not in assignment.dropped
        ],
    }


def _evidence_lines(evidence: list[dict]) -> list[str]:
    lines, last = [], None
    for e in evidence:
        key = (e["path"], e["line"])
        if not e["line"] or key == last:
            lines.append(f"  - {e['text']}")
        elif e["path"] in ("plan", "source"):
            lines.append(f"  - {e['path']} line {e['line']}: {e['text']}")
        else:
            lines.append(f"  - {e['path']}:{e['line']}: {e['text']}")
        last = key
    return lines


def _block(it: dict) -> str:
    loc = it["location"]
    where = loc["task"] + (f", {loc['part']}" if loc.get("part") else "")
    lines = [
        f"### {it['item_id']}   (class {it['class']})",
        f"Where: {where} (plan lines {loc['line_start']}-{loc['line_end']})",
        f'Text:  "{_flat(it["anchor_text"])}"',
    ]
    lines += (
        ["Tool output:", *_evidence_lines(it["evidence"])]
        if it["evidence"]
        else ["Tool output: none"]
    )
    if it["experimental"]:
        lines.append(EXPERIMENTAL_NOTE)
    lines += [f"Question: {it['question']}", REPLY.format(id=it["item_id"])]
    return "\n".join(lines)


def _text(items: list[dict]) -> str:
    if not items:
        return ""
    head = HEADER + ", ".join(it["item_id"] for it in items)
    return "\n\n".join([head, *(_block(it) for it in items)])


def _number(it: dict) -> int:
    m = re.fullmatch(r"S(\d+)", it["item_id"])
    return int(m.group(1)) if m else 0


def sheet_text(items: list[dict], cap: int = SHEET_CAP) -> tuple[str, bool, list[dict]]:
    """(text, trimmed, items as printed) for `items` in print order; items is not changed (R9 for the trim order)."""
    items = [dict(it, evidence=list(it["evidence"])) for it in items]
    text = _text(items)
    trimmed = False
    for it in sorted(items, key=lambda it: (it["priority"], -_number(it))):
        while len(text) > cap and it["evidence"]:
            it["evidence"].pop()
            trimmed = True
            text = _text(items)
    return text, trimmed, items


def render_sheets(rows, assignment, cards=None, doc=None) -> dict[str, Sheet]:
    """{rid: Sheet} for every reviewer of the assignment, items in that reviewer's shuffled order."""
    by_id = {
        it["item_id"]: it for it in items_json(rows, assignment, cards, doc)["items"]
    }
    out = {}
    for rid, ids in assignment.reviewers.items():
        text, trimmed, shown = sheet_text([by_id[i] for i in ids])
        out[rid] = Sheet(rid, text, trimmed, shown)
    return out


def write(out_dir, sheets: dict[str, Sheet]) -> None:
    """Write sheets/<rid>.md and sheets/<rid>.json under out_dir (the folder `sheets/` is made here)."""
    d = Path(out_dir) / "sheets"
    d.mkdir(parents=True, exist_ok=True)
    for rid, s in sheets.items():
        (d / f"{rid}.md").write_text(s.text, encoding="utf-8")
        (d / f"{rid}.json").write_text(dumps(s.to_json()), encoding="utf-8")
