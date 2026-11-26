"""The ledger-v1 reader and the quote checks (Tier B, built locally; contract of SWD 9.1 and 9.2, MR 3.0.4 to 3.0.6).

This file is written in RL because the sibling had no copy when RL was built (config/shared-manifest.json, `built-local`).
`rl/ledger_api.py` (Task 9) is the one adapter that calls it, so a later swap for the sibling's file changes only that
adapter. Linking, demotion and promotion are SWD 9.3 with the RL limits of DESIGN 7.2 checks 8 to 11.

Public API
    read(report, assigned=None) -> dict
        Reads the ledger of one final message (the raw `reviews/<rid>.md`). Keys:
          ledger_missing  True when there is no parseable ledger-v1 block directly above the findings block. `reason` says
                          why: no_findings_heading, no_ledger_heading, ledger_after_findings, heading_between, no_block,
                          block_twice or unclosed. A report that holds the fence opener only in prose is `no_ledger_heading`
                          or `no_block`: the reader looks for headings and for whole fence lines, never for the opener text.
          rows            the accepted rows in file order, each {item, verdict, quote_plan, quote_other, problem, ran, line,
                          limits_violated, unknown_item}. `verdict` is OK, PROBLEM or UNSURE (read case-insensitively).
          errors          one {line, msg, item, named} per format error; `item` is the line's item when the line was valid
                          JSON with a string item, `named` the item a broken line still names in its text. Format
                          errors are counted, never skipped silently, and such a line gives no row.
          format_errors   len(errors)
          normalised_verdict  rows whose verdict was not written exactly as OK, PROBLEM or UNSURE
          dup_line        items that have a second line; the first line wins and the second gives no row
          unknown_item    items outside `assigned` (None means no membership check); the row is kept and flagged
          block_unusable  None, or why the findings block cannot take an inserted line (no_findings_heading, no_block,
                          block_twice, unclosed). It never changes ledger_missing.
        When the ledger is missing, rows and the counts are empty.
    check(rows, corpora) -> list[dict]
        Copies of the rows with quote_plan_ok, quote_other_ok, corpus, quotes_supported, search_supported and supported.
        `corpora` is {"candidate": text, "source": text or None, "transcript": text or None}. `corpus` is the first of
        source, candidate, transcript that holds quote_other (DR-9), so `transcript` means a match found only in a tool
        result of the reviewer's own run. Assistant text is never a corpus: build the transcript text with
        `transcript_text`, which reads tool results only.
    transcript_text(events) -> str
        The tool results of a `claude -p --output-format json` run (a parsed list of events, or its JSON text): every
        `tool_result` block of every `user` event, whether `content` is a string or an array of {"type": "text"} blocks.
    link_demote(report, rows, errors=(), scope=None) -> dict
        Links each findings line to a checked row (the output of `check`) by `probe`, else by the row's flattened
        `quote_plan` lying inside the flattened `anchor`; an `unknown_item` row is never linked. A blocking linked line
        is set to blocking false (severity kept) for the first cause that holds, in this order: `row_missing` (the probe
        names an item whose line failed to parse, `errors` of `read`), `row_unsure`, `row_unsupported` (PROBLEM and not
        `supported`, or the row has a truthy `over_budget`), `no_cb3` (the CB-3 sentence is neither in the line's `claim`
        nor within 12 lines of a line that names its id, before the findings block). A linked line whose row is OK is left
        alone. `scope` (or the environment variable CHECK_SCOPE) is `linked`, the default, or `all`; `all` also demotes
        an unlinked blocking line that has no CB-3 sentence and is not used in any arm. Every linked line gets `class`.
        Keys: report (the new text), links {finding id: item}, linked (items), demoted {cause: n}, demoted_ids
        {finding id: cause}, format_induced_demotions, probe_unknown, ok_but_finding. A findings block that is missing,
        unclosed or duplicated is left alone (`read` says so in `block_unusable`).
    promote(report, rows, linked=(), categories=None, via_reask=False) -> dict
        Adds one MINOR non-blocking line per PROBLEM row that no line is linked to: `claim` is the row's `problem`,
        `anchor` its `quote_plan`, `id` is "P" + item, `class` the item's recipe, `probe` the item, `src` "ledger",
        `category` is `categories[class]` (the card's promote_category). Only a row that is not `unknown_item`, has no
        truthy `over_budget`, has a present `quote_plan` with `quote_plan_ok`, and whose report was not repaired by a
        re-ask is a candidate. Each line is checked with `fnd._check_finding` against the ids of the block and inserted
        before the closing fence of the one findings block. A line that fails (or every candidate, when the block cannot
        take a line) is logged in `promotion_failures` as {item, id, reason} and skipped. Keys: report, promoted (ids),
        promotion_failures. Both functions return a new text; nothing reads or writes a file.
    contains(flat_corpus, quote) -> bool
        The flattened substring test. It is `bool(fnd.locate(text, quote))` without the per-character loop of `locate`,
        so a check of a long transcript stays fast; tests/test_rowcheck.py pins the two to the same answers (REQ-14).
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

from scaffold import fnd, telemetry

# Owner-approved small allowances (2026-11-15): the ledger heading may carry a colon or be a plain `Ledger:` line, and the
# fence label may differ in case or spacing (`ledger-V1`, "``` ledger-v1"). The findings block is NOT touched here.
HEAD_LEDGER = re.compile(r"^(?:#{1,6}\s+Ledger\s*:?|Ledger\s*:)\s*$", re.M | re.I)
_STRICT_HEAD = re.compile(r"#{1,6}\s+Ledger\s*", re.I)
_LEDGER_FENCE = re.compile(r"^(\s*(?:`{3,}|~{3,}))[ \t]*ledger-v1[ \t]*$", re.M | re.I)
_STRICT_FENCE = "ledger-v1"
_HEADING = re.compile(r"^#{1,6}\s+\S")
_NAMED = re.compile(r'"item"\s*:\s*"([^"\\]+)"')
VERDICTS = ("OK", "PROBLEM", "UNSURE")
TEXT_KEYS = ("quote_plan", "quote_other", "problem", "ran")
QUOTE_MIN, QUOTE_MAX, PROBLEM_MAX, RAN_WORDS = 12, 200, 300, 15
CORPUS_ORDER = ("source", "candidate", "transcript")
CB3 = "An implementer who follows the stated text as written builds"
CAUSES = ("row_missing", "row_unsure", "row_unsupported", "no_cb3")
CB3_WINDOW = 12


def contains(flat_corpus: str, quote: str) -> bool:
    q = fnd.flat(quote)
    return bool(q) and q in flat_corpus


# ---------------------------------------------------------------- reader


def _ledger_block(
    report: str,
) -> tuple[str | None, list[tuple[int, str]], bool]:
    """(reason it is missing or None, [(line number, line text)] of the one ledger-v1 block, loose layout).

    Owner order 2026-11-15 (compliance spike, one corrective iteration): a heading between the ledger block and the
    findings block (for example `## Follow-up candidates`) no longer makes the ledger missing; it sets the third value
    (`loose layout`) so the spike report can count it. Everything else is unchanged."""
    f = fnd._HEAD_FINDINGS.search(report)
    if not f:
        return "no_findings_heading", [], False
    head = HEAD_LEDGER.search(report)
    if not head:
        return "no_ledger_heading", [], False
    if head.start() > f.start():
        return "ledger_after_findings", [], False
    above = report[: f.start()]
    _, blocks = fnd._blocks_after(above, HEAD_LEDGER, "ledger-v1")
    inside = {n for _, body, _ in blocks for n, _ in body}
    lines = above.splitlines()
    loose = False
    for i in range(above.count("\n", 0, head.start()) + 1, len(lines)):
        if i + 1 not in inside and _HEADING.match(lines[i]):
            loose = True
    if not blocks:
        return "no_block", [], loose
    if len(blocks) > 1:
        return "block_twice", [], loose
    if not blocks[0][2]:
        return "unclosed", [], loose
    return None, blocks[0][1], loose


# a third number (`C4.1.1`) or a longer number is a different id, not a suffix
ITEM_ID = re.compile(r"(?<![0-9])C[0-9]+\.[0-9]+(?![0-9]|\.[0-9])")
AFFIX_MAX = 6


def canon_item(item):
    """The row id inside `item` when it is the canonical `C<n>.<m>` plus a small prefix or suffix (`R-C4.1`, `C4.1:`,
    `C4.1a`): at most AFFIX_MAX extra characters (owner order 2026-11-15). Anything else comes back unchanged."""
    if not isinstance(item, str):
        return item
    m = ITEM_ID.search(item)
    if m and 0 < len(item) - len(m.group(0)) <= AFFIX_MAX:
        return m.group(0)
    return item


def findings_block_state(report: str) -> str | None:
    """None when the report has exactly one closed findings-v1 block after its heading, else the reason."""
    found, blocks = fnd._blocks_after(report, fnd._HEAD_FINDINGS, "findings-v1")
    if not found:
        return "no_findings_heading"
    if not blocks:
        return "no_block"
    if len(blocks) > 1:
        return "block_twice"
    return None if blocks[0][2] else "unclosed"


def _row(obj: Any) -> tuple[dict | None, str | None, bool]:
    """(row, format error message, verdict was normalised) of one parsed ledger line."""
    if not isinstance(obj, dict):
        return None, "a line must be a JSON object", False
    item, verdict = obj.get("item"), obj.get("verdict")
    if not isinstance(item, str) or not item or not isinstance(verdict, str):
        return None, "a line needs a string item and a string verdict", False
    norm = verdict.strip().upper()
    if norm not in VERDICTS:
        return None, "verdict must be OK, PROBLEM or UNSURE", False
    row: dict[str, Any] = {"item": canon_item(item), "verdict": norm}
    if row["item"] != item:
        row["item_raw"] = item
    for k in TEXT_KEYS:
        v = obj.get(k)
        if v is not None and not isinstance(v, str):
            return None, f"{k} must be a string", False
        row[k] = v or ""
    limits = []
    if (
        row["quote_plan"]
        and not QUOTE_MIN <= len(fnd.flat(row["quote_plan"])) <= QUOTE_MAX
    ):
        limits.append("quote_plan")
    if len(fnd.flat(row["problem"])) > PROBLEM_MAX:
        limits.append("problem")
    if len(row["ran"].split()) > RAN_WORDS:
        limits.append("ran")
    row["limits_violated"] = limits
    return row, None, norm != verdict


def read(report: str, assigned=None) -> dict:
    out: dict[str, Any] = {
        "ledger_missing": False,
        "reason": None,
        "rows": [],
        "errors": [],
        "format_errors": 0,
        "normalised_verdict": 0,
        "dup_line": [],
        "unknown_item": [],
        "block_unusable": findings_block_state(report),
        "loose_layout": False,
        "forgiven": [],
    }
    lreport = _LEDGER_FENCE.sub(lambda m: m.group(1) + _STRICT_FENCE, report)
    if lreport != report:
        out["forgiven"].append("fence_label")
    reason, body, out["loose_layout"] = _ledger_block(lreport)
    if out["loose_layout"]:
        out["forgiven"].append("heading_between")
    head = HEAD_LEDGER.search(report)
    if head and not _STRICT_HEAD.fullmatch(head.group(0)):
        out["forgiven"].append("heading_style")
    if reason:
        out.update(ledger_missing=True, reason=reason)
        return out
    seen: set[str] = set()
    for lineno, raw in body:
        if not raw.strip():
            continue
        item = None
        named = None
        cooked = raw.strip()
        if cooked.endswith(","):  # a trailing comma or stray space on a JSON line is forgiven and recorded
            cooked = cooked[:-1].rstrip()
        if cooked != raw:
            out["forgiven"].append("json_line_slack")
        try:
            obj = json.loads(cooked)
            if isinstance(obj, dict) and isinstance(obj.get("item"), str):
                item = obj["item"]
            row, err, normalised = _row(obj)
        except json.JSONDecodeError as exc:
            row, err, normalised = None, f"not valid JSON: {exc.msg}", False
            named = (m := _NAMED.search(raw)) and m.group(1)
        if err or row is None:
            out["errors"].append(
                {"line": lineno, "msg": err, "item": item, "named": named or item}
            )
            continue
        if row["item"] in seen:
            out["dup_line"].append(row["item"])
            continue
        seen.add(row["item"])
        out["normalised_verdict"] += normalised
        row["line"] = lineno
        row["unknown_item"] = assigned is not None and row["item"] not in assigned
        if row["unknown_item"]:
            out["unknown_item"].append(row["item"])
        out["rows"].append(row)
    out["format_errors"] = len(out["errors"])
    return out


# ---------------------------------------------------------------- corpora and quote checks


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b if isinstance(b, str) else b.get("text") or ""
            for b in content
            if isinstance(b, str) or (isinstance(b, dict) and b.get("type") == "text")
        )
    return ""


def transcript_text(events) -> str:
    if isinstance(events, (str, bytes)):
        events = json.loads(events)
    if isinstance(events, dict):
        events = [events]
    parts = []
    for ev in events:
        content = (
            (ev.get("message") or {}).get("content") if isinstance(ev, dict) else None
        )
        if (
            not isinstance(ev, dict)
            or ev.get("type") != "user"
            or not isinstance(content, list)
        ):
            continue
        parts += [
            _text_of(b.get("content"))
            for b in content
            if isinstance(b, dict) and b.get("type") == "tool_result"
        ]
    return "\n".join(parts)


def check(rows: list[dict], corpora: dict) -> list[dict]:
    flats = {k: fnd.flat(v) for k, v in corpora.items() if v}
    out = []
    for r in rows:
        plan_ok = contains(flats.get("candidate", ""), r["quote_plan"])
        corpus = next(
            (k for k in CORPUS_ORDER if contains(flats.get(k, ""), r["quote_other"])),
            None,
        )
        both = plan_ok and corpus is not None
        quotes = both and fnd.flat(r["quote_plan"]) != fnd.flat(r["quote_other"])
        search = both and corpus == "transcript"
        out.append(
            dict(
                r,
                quote_plan_ok=plan_ok,
                quote_other_ok=corpus is not None,
                corpus=corpus,
                quotes_supported=quotes,
                search_supported=search,
                supported=quotes or search,
            )
        )
    return out


# ---------------------------------------------------------------- linking, demotion and promotion


def _line_obj(raw: str) -> dict | None:
    """The findings line as an object, or None for a line that is not JSON, not an object or a `prior` line."""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) and "prior" not in obj else None


def _findings_body(report: str):
    """(lines of the report with their line ends, (opener line, [(line number, text)], closed) of the one findings block or None)."""
    lines = report.splitlines(keepends=True)
    if findings_block_state(report):
        return lines, None
    return lines, fnd._blocks_after(report, fnd._HEAD_FINDINGS, "findings-v1")[1][0]


def _line_end(line: str) -> str:
    return line[len(line.rstrip("\r\n")) :]


def _has_cb3(obj: dict, before: list[str]) -> bool:
    want = fnd.flat(CB3).lower()
    if want in fnd.flat(str(obj.get("claim") or "")).lower():
        return True
    fid = obj.get("id")
    if not isinstance(fid, str) or not fid:
        return False
    mention = re.compile(rf"(?<!\w){re.escape(fid)}(?!\w)")
    return any(
        mention.search(ln)
        and want
        in fnd.flat(
            " ".join(before[max(0, i - CB3_WINDOW) : i + CB3_WINDOW + 1])
        ).lower()
        for i, ln in enumerate(before)
    )


def _supported(row: dict) -> bool:
    return bool(row.get("supported")) and not row.get("over_budget")


def _format_induced(row: dict | None) -> bool:
    """A line that did not parse, or a row that states a problem and both quotes but fails a quote test."""
    if row is None:
        return True
    both = row["problem"] and row["quote_plan"] and row["quote_other"]
    return bool(both and not (row["quote_plan_ok"] and row["quote_other_ok"]))


def link_demote(report: str, rows: list[dict], errors=(), scope=None) -> dict:
    scope = scope or os.environ.get("CHECK_SCOPE") or "linked"
    if scope not in ("linked", "all"):
        raise ValueError(f"CHECK_SCOPE must be linked or all, not {scope!r}")
    out: dict[str, Any] = {
        "report": report,
        "links": {},
        "linked": [],
        "demoted": dict.fromkeys(CAUSES, 0),
        "demoted_ids": {},
        "format_induced_demotions": 0,
        "probe_unknown": 0,
        "ok_but_finding": 0,
    }
    lines, block = _findings_body(report)
    if block is None:
        return out
    by_item = {r["item"]: r for r in rows if not r.get("unknown_item")}
    failed = {canon_item(e["named"]) for e in errors if e.get("named")} - {
        r["item"] for r in rows
    }
    before = report[: fnd._HEAD_FINDINGS.search(report).start()].splitlines()
    for lineno, raw in block[1]:
        obj = _line_obj(raw)
        if obj is None:
            continue
        probe = canon_item(obj.get("probe"))
        item = probe if probe in by_item or probe in failed else None
        if item is None:
            out["probe_unknown"] += bool(probe)
            anchor = (
                fnd.flat(obj["anchor"]) if isinstance(obj.get("anchor"), str) else ""
            )
            item = next(
                (
                    r["item"]
                    for r in by_item.values()
                    if (q := fnd.flat(r["quote_plan"])) and q in anchor
                ),
                None,
            )
        row = by_item.get(item)
        blocking = obj.get("blocking") is True
        cause = None
        if item is None:
            if scope == "all" and blocking and not _has_cb3(obj, before):
                cause = "no_cb3"
        else:
            out["links"][obj.get("id")] = item
            out["linked"].append(item)
            if row is not None and row["verdict"] == "OK":
                out["ok_but_finding"] += 1
            elif blocking:
                if row is None:
                    cause = "row_missing"
                elif row["verdict"] == "UNSURE":
                    cause = "row_unsure"
                elif not _supported(row):
                    cause = "row_unsupported"
                elif not _has_cb3(obj, before):
                    cause = "no_cb3"
        if item is None and cause is None:
            continue
        new = telemetry.tag(obj, class_=telemetry.class_of(item or ""))
        if cause:
            new["blocking"] = False
            out["demoted"][cause] += 1
            out["demoted_ids"][obj.get("id")] = cause
            out["format_induced_demotions"] += cause in (
                "row_missing",
                "row_unsupported",
            ) and _format_induced(row)
        lines[lineno - 1] = json.dumps(new, ensure_ascii=False) + _line_end(
            lines[lineno - 1]
        )
    out["report"] = "".join(lines)
    return out


def promote(
    report: str, rows: list[dict], linked=(), categories=None, via_reask=False
) -> dict:
    out: dict[str, Any] = {"report": report, "promoted": [], "promotion_failures": []}
    candidates = [
        r
        for r in rows
        if r["verdict"] == "PROBLEM"
        and r["item"] not in linked
        and not r.get("unknown_item")
        and not r.get("over_budget")
        and r["quote_plan"]
        and r.get("quote_plan_ok")
        and not via_reask
    ]
    lines, block = _findings_body(report)
    if candidates and block is None:
        reason = f"findings block unusable: {findings_block_state(report)}"
        out["promotion_failures"] = [
            {"item": r["item"], "id": "P" + r["item"], "reason": reason}
            for r in candidates
        ]
        return out
    if not candidates:
        return out
    seen = {
        o["id"]
        for _, raw in block[1]
        if (o := _line_obj(raw)) is not None and isinstance(o.get("id"), str)
    }
    new_lines = []
    for r in candidates:
        cls = telemetry.class_of(r["item"])
        finding = telemetry.tag(
            {
                "id": "P" + r["item"],
                "severity": "MINOR",
                "blocking": False,
                "category": (categories or {}).get(cls),
                "anchor": r["quote_plan"],
                "refs": [],
                "claim": r["problem"],
            },
            class_=cls,
            probe=r["item"],
            src="ledger",
        )
        err = fnd._check_finding(finding, seen)
        if err:
            out["promotion_failures"].append(
                {"item": r["item"], "id": finding["id"], "reason": err}
            )
            continue
        seen.add(finding["id"])
        out["promoted"].append(finding["id"])
        new_lines.append(json.dumps(finding, ensure_ascii=False) + "\n")
    # the closing fence is the line after the last body line (or after the opener of an empty block)
    close = (block[1][-1][0] if block[1] else block[0]) + 1
    lines[close - 1 : close - 1] = new_lines
    out["report"] = "".join(lines)
    return out
