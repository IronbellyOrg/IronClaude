"""Brief renderer (DESIGN 8.1, MR 3.0.2, 3.0.4, 3.1(a), DD-6, DD-7, DD-14).

A brief is a join of text parts in a fixed order. Parts are files under briefs/ (no part is written in code, so the
sha256 of each one can be frozen, AO-5); the K paragraph is generated from briefs/k-lead.txt and the eight card
`definition` fields. Parts are joined with one blank line. Part files are stored without a trailing newline; any
trailing newline is dropped when a part is read.

    arm     parts, in order
    Z0-raw  base
    Z0      base, CB-1 (only with a source), CB-2, CB-3, CB-4, CB-5
    K       the Z0 parts, K paragraph
    SS      the Z0 parts, ledger rule, sheet block + the heading + the sheet text
            (an empty sheet, or fallback=True, gives the Z0 parts and nothing else)

The one non-file text is the heading that DESIGN 8.1 puts between the sheet block and the sheet text.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from scaffold import cards as cards_mod

BRIEFS_DIR = Path(__file__).resolve().parents[1] / "briefs"
ARMS = ("Z0-raw", "Z0", "K", "SS")
SHEET_HEADING = "## SWEEP SHEET ITEMS"
SEPARATOR = "\n\n"
# part name -> file under briefs/ (the K paragraph is generated from k-lead.txt, so it has no file of its own)
FILES = {
    "base": "base.txt",
    "cb1": "cb1.txt",
    "cb2": "cb2.txt",
    "cb3": "cb3.txt",
    "cb4": "cb4.txt",
    "cb5": "cb5.txt",
    "k": "k-lead.txt",
    "ledger-rule": "ledger-rule.txt",
    "sheet-block": "sheet-block.txt",
}
# the opening words that find each quoted block of MR (the extraction used by the test and by the copy script)
MR_OPENINGS = {
    "cb1": "Driving document:",
    "cb2": "Every defect you confirm",
    "cb3": "A tool line or a recipe step",
    "cb4": "The merge enforces these limits",
    "cb5": "The checks you were given",
    "ledger-rule": "Only your FINAL message is kept",
    "sheet-block": "SWEEP SHEET. A script",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def mr_quote(mr_text: str, opening: str) -> str:
    """The text of the one-line quoted block `> "<opening>..."` of MR, without the `> "` and the closing quote."""
    hits = [ln for ln in mr_text.splitlines() if ln.startswith('> "' + opening)]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} quoted blocks start with {opening!r}, need 1")
    if not hits[0].endswith('"'):
        raise ValueError(f"the quoted block {opening!r} does not end with a quote")
    return hits[0][3:-1]


def rr_brief(rr_text: str) -> tuple[int, int, str]:
    """(first line, last line, text) of the `BRIEF="..."` string of RR; lines are 1-based, the text has no quotes."""
    lines = rr_text.split("\n")
    first = next(i for i, ln in enumerate(lines) if ln.startswith('BRIEF="'))
    last = next(i for i in range(first + 1, len(lines)) if lines[i].endswith('"'))
    body = "\n".join(lines[first : last + 1])
    return first + 1, last + 1, body[len('BRIEF="') : -1]


def _read(name: str, directory: Path) -> str:
    return (directory / FILES[name]).read_text(encoding="utf-8").rstrip("\n")


def part_hashes(directory: Path | str | None = None) -> dict[str, str]:
    """{part name: sha256 of the part file's bytes} for every part file that exists (the values AO-5 freezes)."""
    root = Path(directory or BRIEFS_DIR)
    return {
        n: hashlib.sha256((root / f).read_bytes()).hexdigest()
        for n, f in FILES.items()
        if (root / f).is_file()
    }


def k_paragraph(
    cards: dict[str, dict] | None = None, directory: Path | str | None = None
) -> str:
    """The K paragraph: the lead-in, then the eight card definitions numbered in class order, all on one paragraph.

    Lines of k-lead.txt that start with `# ` are comments (the draft marker, DD-14) and are not sent.
    """
    root = Path(directory or BRIEFS_DIR)
    lead = " ".join(
        ln.strip()
        for ln in _read("k", root).splitlines()
        if ln.strip() and not ln.startswith("# ")
    )
    cs = cards if cards is not None else cards_mod.load()
    checks = " ".join(
        f"({n}) {cards_mod.definition(i, cs)}" for n, i in enumerate(cs, 1)
    )
    return f"{lead} {checks}"


def part_names(arm: str, has_source: bool, has_sheet: bool) -> list[str]:
    """The part names of one arm, in brief order (DESIGN 8.1)."""
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}, expected one of {ARMS}")
    if arm == "Z0-raw":
        return ["base"]
    z0 = ["base", *(["cb1"] if has_source else []), "cb2", "cb3", "cb4", "cb5"]
    if arm == "K":
        return [*z0, "k"]
    if arm == "SS" and has_sheet:
        return [*z0, "ledger-rule", "sheet-block"]
    return z0


def render(
    arm: str,
    doc: dict,
    items: dict | None,
    source: str | None,
    *,
    fallback: bool = False,
    cards: dict[str, dict] | None = None,
    directory: Path | str | None = None,
) -> dict:
    """Build one reviewer's brief.

    doc     {"cand_sb": absolute path of the candidate in the sandbox, "sha": sha256 of that file}; they fill
            `$CAND_SB` and `$SHA` of the base part.
    items   this reviewer's sheet, {"path": absolute path of sheets/<rid>.md, "text": the sheet text}; None, or an
            empty text, is an empty sheet. Used by arm SS only.
    source  absolute path of the driving document, or None/"" when there is none (CB-1 is then left out).
    fallback  the pre-pass or render failed: arm SS gets the Z0 parts (DESIGN 10 row 1).

    Returns {"text", "sha256", "parts": [names in order], "part_sha256": {name: sha256 of the text the part
    contributed}, "no_source", "no_trigger", "fallback"}. `no_source` is a fact about the document; `no_trigger`
    is true for an SS run with an empty sheet and no fallback.
    """
    root = Path(directory or BRIEFS_DIR)
    sheet = items if items and str(items.get("text", "")).strip() else None
    if sheet is not None and not sheet.get("path"):
        raise ValueError("items needs the absolute `path` of the sheet file")
    names = part_names(arm, bool(source), sheet is not None and not fallback)
    texts: dict[str, str] = {}
    for n in names:
        if n == "k":
            texts[n] = k_paragraph(cards, root)
        else:
            texts[n] = _read(n, root)
    texts["base"] = (
        texts["base"].replace("$CAND_SB", doc["cand_sb"]).replace("$SHA", doc["sha"])
    )
    if "cb1" in texts:
        texts["cb1"] = texts["cb1"].replace("{{SOURCE_ABS}}", str(source))
    if "sheet-block" in texts and sheet is not None:
        texts["sheet-block"] = (
            texts["sheet-block"].replace("{{SHEET_PATH}}", sheet["path"])
            + SEPARATOR
            + SHEET_HEADING
            + SEPARATOR
            + str(sheet["text"]).rstrip("\n")
        )
    brief = SEPARATOR.join(texts[n] for n in names)
    return {
        "text": brief,
        "sha256": sha256_text(brief),
        "parts": names,
        "part_sha256": {n: sha256_text(t) for n, t in texts.items()},
        "no_source": not source,
        "no_trigger": arm == "SS" and not fallback and sheet is None,
        "fallback": bool(fallback and arm == "SS"),
    }
