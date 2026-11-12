"""Convert a recorded reflect reviewer card to findings-v2 lines with the deterministic, quote-free rule.

Card-format table (the shapes accepted)

| Shape | Recognised when | Findings | Severity word |
|---|---|---|---|
| yaml-blocking-minor | YAML mapping with a list under findings, returned_findings or deviations (first list wins), and every mapping entry has the severity word blocking or minor | each list entry | severity |
| yaml-other-severity | the same container otherwise: some entry has another severity word (medium, low, should-fix, ...), uses priority: P1-P3, or has none; deviation_class is read when present | each list entry | severity, else priority |
| markdown-table | a markdown card with a pipe table whose header has an evidence cell and a sev or severity cell | each body row of such a table | the sev or severity column |
| unlisted | anything else: other markdown, text that is not YAML, YAML without that list, an unreadable file or another suffix | none | none |

An unlisted card counts as one unconverted unit and a list entry that is not a mapping as one unconverted finding, so
both lower the conversion share instead of leaving its denominator.

Plan and spec paths, per path: the card's own top-level plan: and spec: fields first; otherwise the run's
artifacts/input-snapshot.yaml next to the reviewer-cards directory, taking the plan as the <id>.md entry (an .md file
whose name without suffix equals its directory's name, or, at the snapshot root, starts with TASK-) and the spec as the
source.md entry, each only when exactly one such entry exists; otherwise the refs that need the path are unresolved.

Refs are read from the entry keys evidence, location, citation, file_line and spec_ref (YAML) or from the evidence and
location columns (markdown), as a string or a list of strings; each string is read on its own. Extraction (_TOKEN):
every token path:N or path:A-B in the string is taken, where path is a run of letters, digits and . _ - / ~ + @ not
glued to a preceding such character or colon, and the line is not followed by a letter, digit, underscore, / or a dot
plus one of those. The token counts only when path is plan, source.md or spec, contains /, or ends in a file extension
(a dot, a letter, then letters or digits); any other text, including words followed by a colon, is prose and is
ignored. Right after a token, a comma followed by a bare line or range (60, 75-83 or :72) that ends at a comma,
semicolon, closing bracket, quote, backtick, asterisk, final dot or the end of a line is another ref on the same
path (_MORE). plan:N is a plan citation on the plan path, source.md:N or spec:N a spec citation on the spec path, any
other path a source citation on that path, lines N-N or A-B. A token with a missing plan or spec path, or whose
citation findings_v2 rejects (absolute path, .., line 0, end before start), becomes {role: unresolved, ref, reason}
holding the token; a non-blank string with no token becomes exactly one unresolved citation holding the whole
string; a non-text item becomes one unresolved citation. Unresolved citations are kept in the finding's citations
and counted, and their finding is unconverted, so a ref in a form not listed lowers the share. No citation carries
a quote.

Severity: blocking, blocker, major, high, must-fix, p1 map to MAJOR and blocking; critical, p0 to CRITICAL and
blocking; minor, medium, low, should-fix, important, nit, info, p2, p3 to MINOR and not blocking (case-insensitive);
another word leaves severity unset. Category: the first of category, kind, type, class, classification (or the
markdown category or class column) that names a reflect category sets reflect_category and maps it as findings_v2
does; risk maps to safety when the claim names a safety, security or data-loss effect (_SAFETY) and to other
otherwise; with no reflect category the category is other. deviation_class comes from the first of deviation_class,
class, classification (or that markdown column) that is a findings_v2 deviation class.

A finding is converted unambiguously when it has no unresolved citation and its line passes findings_v2.check_finding.
Each card reports units (its findings, or 1 for an unlisted card), converted, unconverted, the ref counts and share
(converted / units, None when units is 0); summarize adds the cards up, in total and by shape.
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable

import yaml

from superclaude.cli.review.findings import _ID, flat
from superclaude.cli.review.findings_v2 import (
    DEVIATION_CLASSES,
    REFLECT_CATEGORIES,
    _check_citation,
    check_finding,
)

SHAPES = ("yaml-blocking-minor", "yaml-other-severity", "markdown-table", "unlisted")
FINDING_KEYS = ("findings", "returned_findings", "deviations")
REF_KEYS = ("evidence", "location", "citation", "file_line", "spec_ref")
CLAIM_KEYS = ("claim", "finding", "title", "summary", "headline")
CATEGORY_KEYS = ("category", "kind", "type", "class", "classification")
CLASS_KEYS = ("deviation_class", "class", "classification")
BLOCKING_WORDS = {
    "blocking": "MAJOR",
    "blocker": "MAJOR",
    "major": "MAJOR",
    "high": "MAJOR",
    "must-fix": "MAJOR",
    "p1": "MAJOR",
    "critical": "CRITICAL",
    "p0": "CRITICAL",
}
MINOR_WORDS = frozenset(
    {"minor", "medium", "low", "should-fix", "important", "nit", "info", "p2", "p3"}
)
SNAPSHOT = PurePosixPath("artifacts/input-snapshot.yaml")
MAX_REF_TEXT = 200
MAX_CLAIM = 300

_TOKEN = re.compile(
    r"(?<![\w.\-/~+@:])(?P<path>[\w.\-/~+@]+):(?P<a>\d+)(?:\s*[-–]\s*(?P<b>\d+))?(?![\w/]|\.\w)"
)
_MORE = re.compile(
    r"\s*,\s*:?(?P<a>\d+)(?:\s*[-–]\s*(?P<b>\d+))?(?=\s*(?:[,;)\]`'\"*]|\.(?!\w)|$))",
    re.M,
)
_EXT = re.compile(r"\.[A-Za-z][A-Za-z0-9]*$")
_SAFETY = re.compile(
    r"\b(?:safety|unsafe|security|insecure|vulnerab\w*|data[- ]loss|los(?:e|es|t|ing) data"
    r"|credentials?|secrets?|leak(?:s|ed|ing)?)\b",
    re.I,
)


def _word(value: Any) -> str | None:
    return value.strip().lower() if isinstance(value, str) and value.strip() else None


def _unresolved(text: str, reason: str) -> dict:
    return {"role": "unresolved", "ref": text[:MAX_REF_TEXT], "reason": reason}


def _path_shaped(token: str) -> bool:
    return (
        token in ("plan", "source.md", "spec")
        or "/" in token
        or bool(_EXT.search(token))
    )


def _resolve(
    token: str, a: int, b: int, raw: str, plan: str | None, spec: str | None
) -> dict:
    if token == "plan":
        role, path = "plan", plan
    elif token in ("source.md", "spec"):
        role, path = "spec", spec
    else:
        role, path = "source", token
    if path is None:
        return _unresolved(raw, f"no {role} path")
    cit = {"role": role, "path": path, "line_start": a, "line_end": b}
    err = _check_citation(cit)
    return _unresolved(raw, err) if err else cit


def _citations(values: Iterable[Any], plan: str | None, spec: str | None) -> list[dict]:
    """Citations extracted from values (strings or lists of strings), in order; see the module docstring."""
    out: list[dict] = []
    for value in values:
        for item in value if isinstance(value, list) else [value]:
            if item is None:
                continue
            if not isinstance(item, str):
                out.append(_unresolved(flat(str(item)), "not a text ref"))
                continue
            found: list[dict] = []
            for m in _TOKEN.finditer(item):
                path = m["path"]
                if not _path_shaped(path):
                    continue
                hit, end = m, m.end()
                while hit:
                    a = int(hit["a"])
                    b = int(hit["b"]) if hit["b"] else a
                    raw = (
                        m.group(0)
                        if hit is m
                        else f"{path}:{hit.group(0).strip(' ,:')}"
                    )
                    found.append(_resolve(path, a, b, raw, plan, spec))
                    hit = _MORE.match(item, end)
                    end = hit.end() if hit else end
            if not found and item.strip():
                found.append(_unresolved(flat(item), "no path:line ref"))
            out.extend(found)
    return out


def _new_id(raw: Any, index: int, seen: set[str]) -> str:
    if isinstance(raw, (str, int)) and not isinstance(raw, bool):
        fid = str(raw).strip()
        if _ID.match(fid) and fid not in seen:
            return fid
    fid, k = f"F{index}", 1
    while fid in seen:
        fid, k = f"F{index}-{k}", k + 1
    return fid


def _convert(
    index: int,
    raw_id: Any,
    sev_word: str | None,
    cat_words: list[str | None],
    class_words: list[str | None],
    claim: Any,
    ref_values: list[Any],
    plan: str | None,
    spec: str | None,
    seen: set[str],
) -> tuple[dict, str | None]:
    """(findings-v2 line, None when converted unambiguously else the reason); seen gains the line's id."""
    fid = _new_id(raw_id, index, seen)
    if sev_word in BLOCKING_WORDS:
        severity, blocking = BLOCKING_WORDS[sev_word], True
    elif sev_word in MINOR_WORDS:
        severity, blocking = "MINOR", False
    else:
        severity, blocking = None, None
    text = flat(claim) if isinstance(claim, str) else ""
    if len(text) > MAX_CLAIM:
        text = text[: MAX_CLAIM - 3] + "..."
    rcat = next((w for w in cat_words if w in REFLECT_CATEGORIES), None)
    dclass = next((w for w in class_words if w in DEVIATION_CLASSES), None)
    if rcat == "risk":
        category = "safety" if _SAFETY.search(text) else "other"
    else:
        category = REFLECT_CATEGORIES[rcat][0] if rcat else "other"
    cits = _citations(ref_values, plan, spec)
    line: dict[str, Any] = {
        "id": fid,
        "severity": severity,
        "blocking": blocking,
        "category": category,
        "claim": text,
        "refs": [],
        "citations": cits,
    }
    if rcat:
        line["reflect_category"] = rcat
    if dclass:
        line["deviation_class"] = dclass
    unresolved = sum(c["role"] == "unresolved" for c in cits)
    reason = (
        f"{unresolved} unresolved citation(s)"
        if unresolved
        else check_finding(line, seen)
    )
    seen.add(fid)
    return line, reason


def _yaml_findings(text: str) -> tuple[dict, list] | None:
    try:
        data = yaml.safe_load(text)
    except Exception:  # any parser failure makes the card unlisted
        return None
    if not isinstance(data, dict):
        return None
    for key in FINDING_KEYS:
        if isinstance(data.get(key), list):
            return data, data[key]
    return None


def _cells(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s[1:-1] if s.endswith("|") and len(s) > 1 else s[1:]
    return [c.replace("`", "").replace("**", "").strip() for c in s.split("|")]


def _md_rows(text: str) -> list[dict[str, str]] | None:
    """Body rows (lower-case header -> cell) of every finding table, or None when the text has none."""
    lines = text.splitlines()
    rows: list[dict[str, str]] = []
    found = False
    i = 0
    while i < len(lines):
        heads = _cells(lines[i])
        sep = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if heads and "-" in sep and set(sep) <= set("|:- \t"):
            heads = [flat(h).lower() for h in heads]
            if any("evidence" in h for h in heads) and any(
                h in ("sev", "severity") for h in heads
            ):
                found = True
                i += 2
                while i < len(lines) and (cells := _cells(lines[i])) is not None:
                    row: dict[str, str] = {}
                    for h, c in zip(heads, cells):
                        row.setdefault(h, c)
                    rows.append(row)
                    i += 1
                continue
        i += 1
    return rows if found else None


def _first(row: dict[str, str], match: Callable[[str], bool]) -> str | None:
    return next((v for h, v in row.items() if match(h)), None)


def _result(
    shape: str,
    findings: list[dict],
    problems: list[dict],
    units: int,
    plan: tuple[str | None, str | None],
    spec: tuple[str | None, str | None],
) -> dict:
    cits = [c for f in findings for c in f["citations"]]
    unresolved = sum(c["role"] == "unresolved" for c in cits)
    converted = units - len(problems)
    return {
        "shape": shape,
        "plan_path": plan[0],
        "plan_path_source": plan[1],
        "spec_path": spec[0],
        "spec_path_source": spec[1],
        "findings": findings,
        "problems": problems,
        "counts": {
            "units": units,
            "converted": converted,
            "unconverted": units - converted,
            "refs": len(cits),
            "refs_resolved": len(cits) - unresolved,
            "refs_unresolved": unresolved,
            "share": converted / units if units else None,
        },
    }


def _pick(card_value: Any, fallback: str | None) -> tuple[str | None, str | None]:
    """(path, source): the card's own field when it is a non-empty string, else the snapshot fallback."""
    if isinstance(card_value, str) and card_value.strip():
        return card_value.strip(), "card"
    return (fallback, "snapshot") if fallback else (None, None)


def _unlisted(reason: str, plan_path: str | None, spec_path: str | None) -> dict:
    return _result(
        "unlisted",
        [],
        [{"id": None, "reason": reason}],
        1,
        _pick(None, plan_path),
        _pick(None, spec_path),
    )


def convert_card(
    text: str,
    *,
    fmt: str | None,
    plan_path: str | None = None,
    spec_path: str | None = None,
) -> dict:
    """Convert one card's text; fmt is "yaml" or "markdown", and any other fmt makes the card unlisted.

    plan_path and spec_path are the run snapshot's paths, used only when the card has no plan: or spec: field.
    Returns {shape, plan_path, plan_path_source, spec_path, spec_path_source, findings, problems, counts}.
    """
    text = text if isinstance(text, str) else ""
    seen: set[str] = set()
    findings: list[dict] = []
    problems: list[dict] = []

    def add(line: dict, reason: str | None) -> None:
        findings.append(line)
        if reason:
            problems.append({"id": line["id"], "reason": reason})

    if fmt == "yaml":
        parsed = _yaml_findings(text)
        if parsed is None:
            return _unlisted(
                "not a YAML mapping with a findings, returned_findings or deviations list",
                plan_path,
                spec_path,
            )
        data, entries = parsed
        plan = _pick(data.get("plan"), plan_path)
        spec = _pick(data.get("spec"), spec_path)
        other = False
        for index, entry in enumerate(entries, 1):
            if not isinstance(entry, dict):
                problems.append(
                    {"id": None, "reason": f"entry {index} is not a mapping"}
                )
                continue
            sev = _word(entry.get("severity")) or _word(entry.get("priority"))
            other = other or sev not in ("blocking", "minor")
            claim = next(
                (entry[k] for k in CLAIM_KEYS if isinstance(entry.get(k), str)), ""
            )
            add(
                *_convert(
                    index,
                    entry.get("id", entry.get("n")),
                    sev,
                    [_word(entry.get(k)) for k in CATEGORY_KEYS],
                    [_word(entry.get(k)) for k in CLASS_KEYS],
                    claim,
                    [entry.get(k) for k in REF_KEYS],
                    plan[0],
                    spec[0],
                    seen,
                )
            )
        shape = "yaml-other-severity" if other else "yaml-blocking-minor"
        return _result(shape, findings, problems, len(entries), plan, spec)

    if fmt != "markdown":
        return _unlisted(
            f"format {fmt!r} is not yaml or markdown", plan_path, spec_path
        )
    rows = _md_rows(text)
    if rows is None:
        return _unlisted(
            "no pipe table with an evidence and a sev or severity column",
            plan_path,
            spec_path,
        )
    for index, row in enumerate(rows, 1):
        cls = _word(_first(row, lambda h: h in ("category", "class")))
        add(
            *_convert(
                index,
                _first(row, lambda h: h in ("#", "id")),
                _word(_first(row, lambda h: h in ("sev", "severity"))),
                [cls],
                [cls],
                _first(
                    row, lambda h: any(w in h for w in ("finding", "diverged", "claim"))
                ),
                [_first(row, lambda h: "evidence" in h), row.get("location")],
                plan_path,
                spec_path,
                seen,
            )
        )
    return _result(
        "markdown-table",
        findings,
        problems,
        len(rows),
        _pick(None, plan_path),
        _pick(None, spec_path),
    )


def _snapshot_entries(data: Any) -> list:
    if isinstance(data, dict):
        for scope in (data, data.get("input_snapshot")):
            if isinstance(scope, dict):
                for key in ("file_list", "files"):
                    if isinstance(scope.get(key), list):
                        return scope[key]
    return []


def _is_plan(path: str) -> bool:
    p = PurePosixPath(path)
    if p.suffix != ".md":
        return False
    return p.stem == p.parent.name if p.parent.name else p.stem.startswith("TASK-")


def snapshot_paths(snapshot: str | Path) -> tuple[str | None, str | None]:
    """(plan path, spec path) from an input-snapshot file.

    Each is None when the file is missing, unreadable or not parsable, or has not exactly one such entry.
    """
    try:
        text = Path(snapshot).read_text(encoding="utf-8", errors="replace")
        data = yaml.safe_load(text)
    except Exception:  # a missing, unreadable or unparsable snapshot gives no paths
        return None, None
    paths = {
        e["path"]
        for e in _snapshot_entries(data)
        if isinstance(e, dict) and isinstance(e.get("path"), str)
    }
    plans = [p for p in paths if _is_plan(p)]
    specs = [p for p in paths if PurePosixPath(p).name == "source.md"]
    return (
        plans[0] if len(plans) == 1 else None,
        specs[0] if len(specs) == 1 else None,
    )


def convert_card_file(path: str | Path) -> dict:
    """Convert a card file: .md is markdown, .yaml or .yml is YAML; another suffix or a read error is unlisted.

    The fallback paths come from <card dir>/../artifacts/input-snapshot.yaml.
    """
    p = Path(path)
    plan, spec = snapshot_paths(p.parent.parent / SNAPSHOT)
    suffix = p.suffix.lower()
    fmt = (
        "markdown"
        if suffix == ".md"
        else "yaml"
        if suffix in (".yaml", ".yml")
        else None
    )
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return _unlisted(f"cannot read the card ({exc.__class__.__name__})", plan, spec)
    return convert_card(text, fmt=fmt, plan_path=plan, spec_path=spec)


def summarize(results: Iterable[dict]) -> dict:
    """Totals over convert_card results: cards, units, converted, unconverted, ref counts, share and by_shape."""
    keys = ("units", "converted", "refs", "refs_resolved", "refs_unresolved")
    total: dict[str, Any] = {"cards": 0, **dict.fromkeys(keys, 0)}
    by_shape = {s: {"cards": 0, "units": 0, "converted": 0} for s in SHAPES}
    for r in results:
        c = r["counts"]
        total["cards"] += 1
        for k in keys:
            total[k] += c[k]
        bucket = by_shape[r["shape"]]
        bucket["cards"] += 1
        bucket["units"] += c["units"]
        bucket["converted"] += c["converted"]
    total["unconverted"] = total["units"] - total["converted"]
    total["share"] = total["converted"] / total["units"] if total["units"] else None
    for bucket in by_shape.values():
        bucket["share"] = (
            bucket["converted"] / bucket["units"] if bucket["units"] else None
        )
    total["by_shape"] = by_shape
    return total
