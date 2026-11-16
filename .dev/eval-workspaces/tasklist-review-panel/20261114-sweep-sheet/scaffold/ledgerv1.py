"""ledger-v1 reader, the four row checks, linking, demotion, telemetry and promotion (DESIGN 9.1 to 9.4, DD-2, DD-3,
DD-9, DD-11, DD-12).

    read_ledger(report, assigned)   the `## Ledger` block of a reviewer's final message as rows, with every format
                                    problem counted (DESIGN 9.1)
    Corpora / transcript_results    the four places a `quote_other` may come from (DD-2)
    check_report(report, ...)       reader + checks 1 to 4 (9.2) + linking + demotion + `class` telemetry + promotion
                                    (9.3) for one reviewer; returns the checked text (the raw report is never edited)
                                    and every count
    summarise(results)              the per-run check.json of DESIGN 9.4 from the per-reviewer results
    carries_cb3(...)                the CB-3 sentence rule

Findings parsing comes only from scaffold/fnd.py; the telemetry keys and the per-class tables are in scaffold/telemetry.py.

Gaps in DESIGN 9.3 and 9.4 resolved by Task 25 (each is a choice the design leaves open; every one is covered by a test):
  P1  Promotion id. `P<item>`; when that id is already in the block the one suffix `-2` is tried (`PS3-2`; a plain
      digit would make `PS3` + `2` collide with the promoted line of an item `S32`), and a second collision is a
      duplicate id, so `_check_finding` rejects it and the row is a promotion failure. A reviewer has at most one
      row per item (`dup_line`), so a second collision means the reviewer used both ids itself.
  P2  A promoted line is checked with `fnd._check_finding` first and its message is the logged reason. Then two
      conditions the design states elsewhere are added to the same list of failures: the row broke a ledger limit
      (9.1 item 5: "cannot be promoted") and the `problem` is empty (the check never writes a claim of its own, so an
      empty claim is not promoted). An empty `quote_plan` is refused by `_check_finding` itself (anchor minimum).
      A row of an item with no `class` in items.json, or of a class with no card, is also a failure (no category).
      Every failure is logged `{item, id, reason}`; none is silent.
  P3  Promotion asks for no support: the design (9.3) gives the PROBLEM verdict and "no linked findings line" as the
      only conditions. A promoted anchor is the row's `quote_plan` as written, found in the candidate or not.
  P4  "Linked" for promotion means the finding links to the row by probe or by quote, whether or not the row is
      OK, and whether or not the finding line itself is a valid findings line. A broken row (a format error line) is
      not in `rows`, so it is never promoted.
  P5  Telemetry: `class` is written on every linked line whose item has a class in items.json (added when missing,
      corrected when different), also on an OK-row line and on a line that stays blocking. The reviewer's `probe` is
      kept as written and none is added to a quote-linked line. A line is rewritten (`json.dumps`, the line ending
      kept) only when `blocking` or `class` changes; an untouched line keeps its bytes. Corrections are counted in
      `class_corrected`, additions in `class_added` (DESIGN 9.4 has no field for them; they are extra keys of check.json).
  P6  The unusable block: nothing is promoted and no line is touched (G10); `block_unusable` carries the reason in the
      per-reviewer result and the reviewer id in check.json.
  P7  check.json extras beyond the DESIGN 9.4 fields: `reviewer_findings` (the findings lines read, so promoted ones are
      counted apart), `demoted_findings`, `class_added`, `class_corrected`, `per_class` and `no_report` (a reviewer
      with no report file). `missing_line` lists only reviewers whose ledger was read; a `ledger_missing` reviewer is
      under `ledger_missing` alone.

Gaps in DESIGN 9 resolved here (each is a choice the design leaves open; every one is covered by a test):
  G1  `corpus` is the FIRST match in the order of DD-2: source, candidate, sheet, transcript. A quote that is also in
      the transcript only because the reviewer read the candidate (nearly every run) is therefore `candidate`, not
      `transcript`, so a row whose two quotes are the same plan text cannot pass as a "search result". Consequence:
      a `sheet` or `transcript` match is never in the candidate, so it always differs from the plan quote and
      `search_supported` implies `quotes_supported`; the flag is kept because 9.2 check 4 defines it.
  G2  Sheet corpus (9.2 check 3, "a printed tool line of this item"): the evidence `text` of the row's item, and the
      same entry in its printed form (`plan line 85: <text>`, `<path>:12: <text>`; render.py's form).
  G3  Transcript corpus: the string `content` of every `tool_result` block of every `user` event (a list of `text`
      parts is joined per part). One block is one corpus entry: a quote cannot span two tool results. Nothing
      from `assistant` events is read here. Real files: results/transcript-shapes.md.
  G4  Where the ledger is looked for (9.1 items 1 and 2). `findings_heading_missing` (no `## Findings block`, so no
      span), `ledger_heading_missing`, `ledger_after_findings` (every `## Ledger` heading is below the findings
      heading), `heading_between` (another heading, outside code fences, sits between the two), `no_block`,
      `two_blocks` (counted over the whole report, so a stray block before the heading also counts), `unclosed`
      (the fence never closes, or it swallows the findings heading) and `block_outside_span`. Each is
      `ledger_missing` and leaves no rows. The last `## Ledger` heading above the findings heading is the one used.
  G5  A line that is a format error but names an assigned item (`"item": "S2"` is read from the object, or from the
      text by a regular expression when the JSON is broken) makes that item `broken`, unless a good row for it
      exists. A finding linked to a broken row gets the cause `row_missing`. An item with no line at all is in
      `missing_line` and is NOT a broken row; a finding whose probe names it is not linked to anything (there is no
      row) unless its anchor contains another row's `quote_plan`.
  G6  Quote linking needs a `quote_plan` of at least 12 flattened characters (the schema floor), so a three-letter
      quote cannot link every finding.
  G7  A finding that would be demoted for more than one cause counts every cause that holds in `demoted`, and once
      in `demoted_findings`. `format_induced` is true only when every cause is format-induced: `row_missing`, or
      `row_unsupported` where `problem` and both quotes are present and a quote test failed.
  G8  A linked finding whose row is `OK` is left alone whatever its blocking flag (DESIGN 9.3, "left alone"); it is
      counted as `ok_but_finding` whether or not it is blocking.
  G9  `CHECK_SCOPE=all` (never used in an arm): an unlinked blocking finding is held to the same rule with its own
      `anchor` and `anchor2` as the two quotes: `anchor` must be in the candidate, `anchor2` must be in one of the
      four corpora (the sheet corpus is then every item's tool lines), and the two must differ, or `anchor2` is a
      sheet or transcript match. Causes are `row_unsupported` and `no_cb3`.
  G10 When the findings block is unusable (missing, unclosed or duplicated; DESIGN 9.3 "Block repair is out of scope")
      the text comes back unchanged and `block_unusable` names the reason; rows are still read and checked.
  G11 `CB-3` window: the sentence counts when it lies within 12 lines above or below a line that holds the finding
      id as a whole word, in the report text above the `## Findings block` heading. Lines are joined and flattened
      first, so a sentence wrapped over two lines still counts.
  Not resolved (the design gives no number): `quote_other` has no minimum length, so a very short second quote
  passes check 3 if it occurs anywhere in a corpus.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Iterable, Sequence
from pathlib import Path

from scaffold import cards as cards_mod
from scaffold import fnd, telemetry

HEAD_LEDGER = re.compile(r"^#{1,6}\s+Ledger\s*$", re.M | re.I)
_HEADING_LINE = re.compile(r"^#{1,6}\s+\S")
_FENCE_LINE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^`\s]*)\s*$")
_ITEM_TEXT = re.compile(r'"item"\s*:\s*"([^"]+)"')

CB3_SENTENCE = "An implementer who follows the stated text as written builds"
VERDICTS = ("OK", "PROBLEM", "UNSURE")
CAUSES = ("row_unsupported", "row_unsure", "no_cb3", "row_missing")
SCOPES = ("linked", "all")
CORPORA = ("source", "candidate", "sheet", "transcript")
QUOTE_PLAN_MIN = 12
QUOTE_PLAN_MAX = 200
PROBLEM_MAX = 300
RAN_MAX_WORDS = 15
CB3_WINDOW = 12
_TEXT_KEYS = ("quote_plan", "quote_other", "problem", "ran")
_CB3_FLAT = fnd.flat(CB3_SENTENCE).lower()


# ---------------------------------------------------------------- positions and fences


def _line_of(text: str, pos: int) -> int:
    """1-based line number of character offset pos."""
    return text.count("\n", 0, pos) + 1


def _fenced(report: str, info: str) -> list[tuple[int, list[tuple[int, str]], bool]]:
    """Every fenced block of the whole report with this info string, like fnd._blocks_after but not tied to a heading.

    A one-line heading is put in front of the text so the scan starts at the first real line; the numbers it returns
    are shifted back, so they are lines of `report`.
    """
    _, blocks = fnd._blocks_after("#\n" + report, re.compile(r"^#\n", re.M), info)
    return [
        (s - 1, [(n - 1, t) for n, t in body], closed) for s, body, closed in blocks
    ]


def _heading_between(lines: list[str], first: int, last: int) -> bool:
    """True when a heading line outside a code fence sits on a line strictly between `first` and `last` (1-based)."""
    marker: str | None = None
    for n in range(first + 1, last):
        line = lines[n - 1]
        fm = _FENCE_LINE.match(line)
        if marker is None:
            if fm:
                marker = fm.group(1)
            elif _HEADING_LINE.match(line):
                return True
        elif (
            fm
            and not fm.group(2)
            and fm.group(1)[0] == marker[0]
            and len(fm.group(1)) >= len(marker)
        ):
            marker = None
    return False


# ---------------------------------------------------------------- 9.1 the reader


def _recover_item(raw: str, obj: object) -> str | None:
    if isinstance(obj, dict) and isinstance(obj.get("item"), str):
        return obj["item"].strip() or None
    m = _ITEM_TEXT.search(raw)
    return m.group(1).strip() if m else None


def read_ledger(report: str, assigned: Sequence[str]) -> dict:
    """The ledger of a final message (DESIGN 9.1) as a dict.

    {"ledger_missing": bool, "reason": str | None, "rows": [row], "format_errors": [{line, msg}],
     "normalised_verdict": n, "dup_line": [{line, item}], "unknown_item": [{line, item}],
     "broken_items": [item], "missing_line": [item]}

    A row is {item, verdict, quote_plan, quote_other, problem, ran, line, limits_violated: [name]}. The verdict is
    upper-cased and trimmed. Rows come back in the order of the lines. When `ledger_missing` is true `rows` is empty and
    `missing_line` holds every assigned item.
    """
    assigned = list(assigned)
    res: dict = {
        "ledger_missing": True,
        "reason": None,
        "rows": [],
        "format_errors": [],
        "normalised_verdict": 0,
        "dup_line": [],
        "unknown_item": [],
        "broken_items": [],
        "missing_line": list(assigned),
    }
    fm = fnd._HEAD_FINDINGS.search(report)
    if not fm:
        res["reason"] = "findings_heading_missing"
        return res
    f_line = _line_of(report, fm.start())
    heads = [_line_of(report, m.start()) for m in HEAD_LEDGER.finditer(report)]
    above = [h for h in heads if h < f_line]
    if not above:
        res["reason"] = "ledger_after_findings" if heads else "ledger_heading_missing"
        return res
    l_line = above[-1]
    if _heading_between(report.splitlines(), l_line, f_line):
        res["reason"] = "heading_between"
        return res
    blocks = _fenced(report, "ledger-v1")
    if not blocks:
        res["reason"] = "no_block"
        return res
    if len(blocks) > 1:
        res["reason"] = "two_blocks"
        return res
    start, body, closed = blocks[0]
    if not l_line < start < f_line:
        res["reason"] = "block_outside_span"
        return res
    if not closed or (body and body[-1][0] >= f_line):
        res["reason"] = "unclosed"
        return res
    res["ledger_missing"] = False

    by_item: dict[str, dict] = {}
    broken: dict[str, int] = {}

    def error(lineno: int, msg: str, item: str | None) -> None:
        res["format_errors"].append({"line": lineno, "msg": msg})
        if item and item in assigned:
            broken.setdefault(item, lineno)

    for lineno, raw in body:
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            error(lineno, f"not valid JSON: {exc.msg}", _recover_item(raw, None))
            continue
        if not isinstance(obj, dict):
            error(lineno, "a line must be a JSON object", None)
            continue
        item, verdict = obj.get("item"), obj.get("verdict")
        known = _recover_item(raw, obj)
        if not isinstance(item, str) or not item.strip():
            error(lineno, "item is missing or not a string", known)
            continue
        if not isinstance(verdict, str):
            error(lineno, "verdict is missing or not a string", known)
            continue
        canon = verdict.strip().upper()
        if canon not in VERDICTS:
            error(lineno, "verdict must be OK, PROBLEM or UNSURE", known)
            continue
        values = {k: ("" if obj.get(k) is None else obj[k]) for k in _TEXT_KEYS}
        bad = [k for k, v in values.items() if not isinstance(v, str)]
        if bad:
            error(lineno, f"{', '.join(bad)} must be a string", known)
            continue
        if canon != verdict:
            res["normalised_verdict"] += 1
        item = item.strip()
        if item not in assigned:
            res["unknown_item"].append({"line": lineno, "item": item})
            continue
        if item in by_item:
            res["dup_line"].append({"line": lineno, "item": item})
            continue
        limits = []
        qp = fnd.flat(values["quote_plan"])
        if qp and not QUOTE_PLAN_MIN <= len(qp) <= QUOTE_PLAN_MAX:
            limits.append("quote_plan")
        if len(fnd.flat(values["problem"])) > PROBLEM_MAX:
            limits.append("problem")
        if len(values["ran"].split()) > RAN_MAX_WORDS:
            limits.append("ran")
        by_item[item] = {
            "item": item,
            "verdict": canon,
            **values,
            "line": lineno,
            "limits_violated": limits,
        }
        res["rows"].append(by_item[item])
    res["broken_items"] = [i for i in assigned if i in broken and i not in by_item]
    res["missing_line"] = [
        i for i in assigned if i not in by_item and i not in res["broken_items"]
    ]
    return res


# ---------------------------------------------------------------- 9.2 corpora and the four checks


def transcript_results(events: object) -> list[str]:
    """The tool results of a run transcript (the parsed `*.attempt1.json`): one string per `tool_result` block (G3)."""
    out: list[str] = []
    if not isinstance(events, list):
        return out
    for ev in events:
        if not isinstance(ev, dict) or ev.get("type") != "user":
            continue
        message = ev.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            c = block.get("content")
            if isinstance(c, str):
                out.append(c)
            elif isinstance(c, list):
                out += [
                    p["text"]
                    for p in c
                    if isinstance(p, dict)
                    and p.get("type") == "text"
                    and isinstance(p.get("text"), str)
                ]
    return out


def read_transcript(path: str | Path) -> list[str]:
    """transcript_results of the JSON file at path."""
    return transcript_results(json.loads(Path(path).read_text(encoding="utf-8")))


def _printed_lines(item: dict) -> list[str]:
    """The tool lines of an item as the reader of the sheet sees them (G2): the entry text, and its printed form."""
    out = []
    for e in item.get("evidence") or []:
        text = e.get("text", "")
        out.append(text)
        path, line = e.get("path"), e.get("line")
        if line and path in ("plan", "source"):
            out.append(f"{path} line {line}: {text}")
        elif line and path:
            out.append(f"{path}:{line}: {text}")
    return out


class Corpora:
    """The four places a `quote_other` may come from (DD-2): `source`, `candidate`, `sheet`, `transcript`.

    `items` are the item dicts of items.json (`item_id`, `evidence`); `transcript` is a list of tool-result strings.
    """

    def __init__(
        self,
        candidate: str,
        source: str | None = None,
        items: Iterable[dict] = (),
        transcript: Iterable[str] = (),
    ):
        self.candidate = candidate
        self.source = source
        self._sheet = {
            it["item_id"]: [fnd.flat(t) for t in _printed_lines(it)] for it in items
        }
        self._transcript = [fnd.flat(t) for t in transcript]

    def in_candidate(self, quote: str) -> bool:
        return bool(fnd.locate(self.candidate, quote))

    def find(self, quote: str, item: str | None = None) -> str | None:
        """The first corpus, in the order of DD-2, that holds the flattened quote (G1); None when none does.

        The sheet corpus is the tool lines of `item`, or of every item when `item` is None.
        """
        q = fnd.flat(quote)
        if not q:
            return None
        if self.source is not None and fnd.locate(self.source, q):
            return "source"
        if fnd.locate(self.candidate, q):
            return "candidate"
        pools = (
            self._sheet.get(item, [])
            if item is not None
            else [t for v in self._sheet.values() for t in v]
        )
        if any(q in t for t in pools):
            return "sheet"
        if any(q in t for t in self._transcript):
            return "transcript"
        return None


def _support(plan_ok: bool, other_ok: bool, corpus: str | None, same: bool) -> dict:
    quotes = plan_ok and other_ok and not same
    search = plan_ok and other_ok and corpus in ("sheet", "transcript")
    return {
        "quotes_supported": quotes,
        "search_supported": search,
        "supported": quotes or search,
    }


def check_row(row: dict, corpora: Corpora) -> dict:
    """Checks 2 to 4 of DESIGN 9.2 for one row: the row plus quote_plan_ok, quote_other_ok, corpus and the support flags."""
    plan_ok = bool(row["quote_plan"].strip()) and corpora.in_candidate(
        row["quote_plan"]
    )
    corpus = corpora.find(row["quote_other"], row["item"])
    same = fnd.flat(row["quote_plan"]) == fnd.flat(row["quote_other"])
    return {
        **row,
        "quote_plan_ok": plan_ok,
        "quote_other_ok": corpus is not None,
        "corpus": corpus,
        **_support(plan_ok, corpus is not None, corpus, same),
    }


# ---------------------------------------------------------------- 9.3 the CB-3 sentence, linking, demotion


def carries_cb3(finding: dict, lines_above: Sequence[str]) -> bool:
    """True when the finding carries the CB-3 sentence (DESIGN 9.3, G11).

    `lines_above` are the report lines above the `## Findings block` heading. The comparison is flattened and
    case-insensitive.
    """
    claim = finding.get("claim")
    if isinstance(claim, str) and _CB3_FLAT in fnd.flat(claim).lower():
        return True
    fid = finding.get("id")
    if not isinstance(fid, str):
        return False
    mention = re.compile(
        rf"(?<![A-Za-z0-9._-]){re.escape(fid)}(?![A-Za-z0-9_-]|\.[A-Za-z0-9])"
    )
    for i, line in enumerate(lines_above):
        if mention.search(line):
            window = " ".join(lines_above[max(0, i - CB3_WINDOW) : i + CB3_WINDOW + 1])
            if _CB3_FLAT in fnd.flat(window).lower():
                return True
    return False


def findings_block_status(report: str) -> tuple[str | None, tuple | None]:
    """(reason the block is unusable or None, the block). The block is (fence line, [(line, text)], closed)."""
    found, blocks = fnd._blocks_after(report, fnd._HEAD_FINDINGS, "findings-v1")
    if not found:
        return "findings_heading_missing", None
    if not blocks:
        return "no_findings_block", None
    if len(blocks) > 1:
        return "findings_block_duplicated", None
    if not blocks[0][2]:
        return "findings_block_unclosed", None
    return None, blocks[0]


def scope_from(scope: str | None = None) -> str:
    """`scope`, else the environment variable CHECK_SCOPE, else `linked` (DD-3)."""
    value = scope if scope is not None else (os.environ.get("CHECK_SCOPE") or "linked")
    if value not in SCOPES:
        raise ValueError(f"CHECK_SCOPE must be one of {SCOPES}, not {value!r}")
    return value


def _link(finding: dict, assigned: list[str], rows: dict, broken: list[str], ordered):
    """(row or None, how, probe_unknown). `how` is "probe", "quote" or None; a broken row is {"item", "broken": True}."""
    probe = finding.get("probe")
    unknown = False
    if isinstance(probe, str) and probe.strip():
        p = probe.strip()
        if p not in assigned:
            unknown = True
        elif p in rows:
            return rows[p], "probe", False
        elif p in broken:
            return {"item": p, "broken": True}, "probe", False
    anchor = (
        fnd.flat(finding["anchor"]) if isinstance(finding.get("anchor"), str) else ""
    )
    for row in ordered:
        qp = fnd.flat(row["quote_plan"])
        if len(qp) >= QUOTE_PLAN_MIN and qp in anchor:
            return row, "quote", unknown
    return None, None, unknown


def _own_quotes(finding: dict, corpora: Corpora) -> dict:
    """Support of an unlinked finding under CHECK_SCOPE=all (G9): its anchor and anchor2 are the two quotes."""
    anchor, anchor2 = finding.get("anchor"), finding.get("anchor2")
    plan_ok = isinstance(anchor, str) and corpora.in_candidate(anchor)
    corpus = corpora.find(anchor2) if isinstance(anchor2, str) else None
    same = fnd.flat(anchor or "") == fnd.flat(anchor2 or "")
    return _support(plan_ok, corpus is not None, corpus, same)


def _row_causes(row: dict) -> tuple[list[str], bool]:
    """(causes, format_induced) for a linked, blocking finding, apart from no_cb3."""
    if row.get("broken"):
        return ["row_missing"], True
    if row["verdict"] == "UNSURE":
        return ["row_unsure"], False
    if row["verdict"] == "PROBLEM" and not row["supported"]:
        fmt = bool(
            row["problem"].strip()
            and row["quote_plan"].strip()
            and row["quote_other"].strip()
            and not (row["quote_plan_ok"] and row["quote_other_ok"])
        )
        return ["row_unsupported"], fmt
    return [], False


def check_report(
    report: str,
    *,
    assigned: Sequence[str],
    candidate: str,
    source: str | None = None,
    items: Iterable[dict] = (),
    transcript: Iterable[str] = (),
    scope: str | None = None,
    cards: dict[str, dict] | None = None,
) -> dict:
    """One reviewer's report through the reader, checks 1 to 4, linking, demotion, telemetry and promotion.

    `items` are the item dicts of items.json (`item_id`, `class`, `evidence`); the class of an item is where the
    `class` key and the promotion category come from (the card of the class, `cards`, default cards/).

    Returns {"scope", "ledger": <read_ledger result, rows checked>, "block_unusable": reason | None,
    "findings": [per finding: id, line, probe, row_item, link, class, class_change, blocking, demoted, causes,
    format_induced, ok_but_finding], "probe_unknown": n, "ok_but_finding": n, "demoted": {cause: n},
    "demoted_findings": n, "format_induced_demotions": n, "class_added": n, "class_corrected": n,
    "promoted": [{id, item, class, line}], "promotion_failures": [{item, id, reason}], "text": the checked report}.
    `text` is `report` with the demotions, the `class` keys and the promoted lines written; it is `report` itself
    when the block is unusable or nothing changes. The raw report is never edited.
    """
    scope = scope_from(scope)
    assigned = list(assigned)
    items = list(items)
    classes = {it["item_id"]: it["class"] for it in items if it.get("class")}
    corpora = Corpora(candidate, source, items, list(transcript))
    ledger = read_ledger(report, assigned)
    ledger["rows"] = [check_row(r, corpora) for r in ledger["rows"]]
    rows = {r["item"]: r for r in ledger["rows"]}
    out = {
        "scope": scope,
        "ledger": ledger,
        "block_unusable": None,
        "findings": [],
        "probe_unknown": 0,
        "ok_but_finding": 0,
        "demoted": dict.fromkeys(CAUSES, 0),
        "demoted_findings": 0,
        "format_induced_demotions": 0,
        "class_added": 0,
        "class_corrected": 0,
        "promoted": [],
        "promotion_failures": [],
        "text": report,
    }
    reason, block = findings_block_status(report)
    if reason:
        out["block_unusable"] = reason
        return out
    lines = report.splitlines(keepends=True)
    f_line = _line_of(report, fnd._HEAD_FINDINGS.search(report).start())
    above = [ln.rstrip("\r\n") for ln in lines[: f_line - 1]]
    changed = False
    for lineno, raw in block[1]:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if (
            not isinstance(obj, dict)
            or "prior" in obj
            or not isinstance(obj.get("id"), str)
        ):
            continue
        row, how, unknown = _link(
            obj, assigned, rows, ledger["broken_items"], ledger["rows"]
        )
        out["probe_unknown"] += unknown
        item_class = classes.get(row["item"]) if row else None
        rec = {
            "id": obj["id"],
            "line": lineno,
            "probe": obj.get("probe"),
            "row_item": row["item"] if row else None,
            "link": how,
            "class": item_class,
            "class_change": None,
            "blocking": obj.get("blocking") is True,
            "demoted": False,
            "causes": [],
            "format_induced": False,
            "ok_but_finding": False,
        }
        out["findings"].append(rec)
        rewrite = False
        state = telemetry.fill_class(obj, item_class)  # DD-12 (P5)
        if state:
            rec["class_change"] = state
            out[f"class_{state}"] += 1
            rewrite = True
        if row is not None and not row.get("broken") and row["verdict"] == "OK":
            out["ok_but_finding"] += 1
            rec["ok_but_finding"] = True
        elif rec["blocking"] and (row is not None or scope == "all"):
            if row is not None:
                causes, fmt = _row_causes(row)
            else:
                causes, fmt = (
                    (
                        []
                        if _own_quotes(obj, corpora)["supported"]
                        else ["row_unsupported"]
                    ),
                    False,
                )
            if not carries_cb3(obj, above):
                causes.append("no_cb3")
            if causes:
                rec.update(
                    demoted=True,
                    causes=causes,
                    format_induced=fmt and "no_cb3" not in causes,
                )
                for c in causes:
                    out["demoted"][c] += 1
                out["demoted_findings"] += 1
                out["format_induced_demotions"] += rec["format_induced"]
                obj["blocking"] = False
                rewrite = True
        if rewrite:
            lines[lineno - 1] = (
                json.dumps(obj, ensure_ascii=False) + lines[lineno - 1][len(raw) :]
            )
            changed = True
    linked = {rec["row_item"] for rec in out["findings"] if rec["link"]}
    todo = [
        r
        for r in ledger["rows"]
        if r["verdict"] == "PROBLEM" and r["item"] not in linked
    ]
    if todo:
        changed |= _promote(todo, block, lines, classes, cards, out)
    if changed:
        out["text"] = "".join(lines)
    return out


def _promotion_line(
    row: dict, item_class: str | None, cards: dict | None, seen: set[str]
) -> tuple[dict | None, str, str | None]:
    """(the promoted line or None, its id, the reason it was refused or None) for one PROBLEM row (DESIGN 9.3, P1, P2)."""
    base = f"P{row['item']}"
    pid = base if base not in seen else f"{base}-2"
    if not item_class:
        return (
            None,
            pid,
            "the item has no class in items.json: no category to promote under",
        )
    try:
        category = cards_mod.promote_category(item_class, cards)
    except KeyError:
        return None, pid, f"no card for class {item_class}"
    line = {
        "id": pid,
        "severity": "MINOR",
        "blocking": False,
        "category": category,
        "anchor": row["quote_plan"],
        "refs": [],
        "claim": row["problem"],
        **telemetry.promoted_keys(row["item"], item_class),
    }
    err = fnd._check_finding(line, seen)
    if err is None and not row["problem"].strip():
        err = "problem is empty: the check writes no claim of its own"
    if err is None and row["limits_violated"]:
        err = "the row breaks a ledger limit: " + ", ".join(row["limits_violated"])
    return (None if err else line), pid, err


def _promote(
    todo: list[dict],
    block: tuple,
    lines: list[str],
    classes: dict[str, str],
    cards: dict | None,
    out: dict,
) -> bool:
    """Insert one MINOR, non-blocking line per row of `todo` as the last lines inside the one findings block (9.3).

    `lines` (the report with line endings) is edited in place. A refused row goes to out["promotion_failures"] and is
    skipped; an inserted one to out["promoted"]. True when a line was inserted.
    """
    seen: set[str] = set()
    for _, raw in block[1]:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(obj, dict)
            and "prior" not in obj
            and isinstance(obj.get("id"), str)
        ):
            seen.add(obj["id"])
    close = block[0] + len(
        block[1]
    )  # 0-based index of the closing fence: opener line n is index n-1
    eol = "\r\n" if lines[close - 1].endswith("\r\n") else "\n"
    new: list[str] = []
    for row in todo:
        item_class = classes.get(row["item"])
        line, pid, err = _promotion_line(row, item_class, cards, seen)
        if err:
            out["promotion_failures"].append(
                {"item": row["item"], "id": pid, "reason": err}
            )
            continue
        seen.add(pid)
        new.append(json.dumps(line, ensure_ascii=False) + eol)
        out["promoted"].append(
            {
                "id": pid,
                "item": row["item"],
                "class": item_class,
                "line": close + 1 + len(new) - 1,
            }
        )
    lines[close:close] = new
    return bool(new)


# ---------------------------------------------------------------- 9.4 the per-run check.json


def summarise(
    results: dict[str, dict],
    classes: dict[str, str] | None = None,
    no_report: Sequence[str] = (),
) -> dict:
    """check.json of DESIGN 9.4 from {reviewer id: check_report result}, with the extras of P7.

    Reviewer findings and promoted findings are counted apart: `reviewer_findings` is the findings lines the
    reviewers wrote, `promoted` the lines the check inserted. `classes` is {item id: class} for the per-class tables.
    """
    out: dict = {
        "ledger_missing": [],
        "format_errors": 0,
        "normalised_verdict": 0,
        "dup_line": 0,
        "unknown_item": 0,
        "probe_unknown": 0,
        "missing_line": {},
        "rows": dict.fromkeys(VERDICTS, 0),
        "demoted": dict.fromkeys(CAUSES, 0),
        "format_induced_demotions": 0,
        "promoted": 0,
        "promotion_failures": [],
        "ok_but_finding": 0,
        "block_unusable": [],
        "reviewer_findings": 0,
        "demoted_findings": 0,
        "class_added": 0,
        "class_corrected": 0,
        "per_class": {},
        "no_report": list(no_report),
    }
    for rid, res in results.items():
        led = res["ledger"]
        if led["ledger_missing"]:
            out["ledger_missing"].append(rid)
        elif led["missing_line"]:
            out["missing_line"][rid] = list(led["missing_line"])
        out["format_errors"] += len(led["format_errors"])
        out["normalised_verdict"] += led["normalised_verdict"]
        out["dup_line"] += len(led["dup_line"])
        out["unknown_item"] += len(led["unknown_item"])
        for r in led["rows"]:
            out["rows"][r["verdict"]] += 1
        for c in CAUSES:
            out["demoted"][c] += res["demoted"][c]
        for k in (
            "probe_unknown",
            "format_induced_demotions",
            "ok_but_finding",
            "demoted_findings",
            "class_added",
            "class_corrected",
        ):
            out[k] += res[k]
        out["promoted"] += len(res["promoted"])
        out["promotion_failures"] += [
            {"rid": rid, **f} for f in res["promotion_failures"]
        ]
        out["reviewer_findings"] += len(res["findings"])
        if res["block_unusable"]:
            out["block_unusable"].append(rid)
    out["per_class"] = telemetry.per_class(results.values(), classes or {})
    return out
