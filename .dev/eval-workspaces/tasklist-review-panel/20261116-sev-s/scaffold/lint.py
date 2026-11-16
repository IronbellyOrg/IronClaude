"""AO-1 leak lint (DESIGN 13.1 row AO-1, REQ-07): no study answer text or name may appear in the build's files.

Given the ground-truth files a person names with --gt-glob, it fails (exit 1) when a scanned file holds
  * any four-word sequence found in a ground-truth `description` or `plan_quote`, or
  * any forbidden name: a document id or task title found in the ground truth (keys in NAME_KEYS), a path token
    found in the `description` or `plan_quote` text, or a name given with --forbid.
It prints only `file:line: kind hash` for each hit, where hash is the first 12 hex digits of the sha256 of the
lower-cased phrase or name. The phrase itself is never printed, and neither is any ground-truth content.

It opens nothing unless --gt-glob is given: there is no default ground-truth path in this file. Exit codes:
0 clean, 1 leak found, 2 usage or unreadable ground truth.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import re
import sys
from pathlib import Path

SW = Path(__file__).resolve().parents[1]
N = 4
PHRASE_KEYS = ("description", "plan_quote")
NAME_KEYS = (
    "doc_id",
    "document_id",
    "plan_id",
    "package",
    "title",
    "task_title",
    "task_titles",
    "plan_title",
)
# DESIGN 13.1: the files and folders the lint covers (those that exist when it runs).
TARGETS = (
    "cards",
    "sweep/words.py",
    "sweep/formats.py",
    "sweep/extractors.py",
    "briefs",
    "fixtures",
)
_WORD = re.compile(r"[a-z0-9]+")
_PATH = re.compile(
    r"[\w.\-]*\w(?:/[\w.\-]+)+|\b[\w\-]+\.(?:py|md|json|sh|yaml|yml|toml|txt|js|ts|cfg|ini)\b"
)


def phrase_hash(text: str) -> str:
    return hashlib.sha256(text.lower().encode("utf-8")).hexdigest()[:12]


def words_with_lines(text: str) -> list[tuple[str, int]]:
    """(lower-case word, 1-based line) for every run of letters and digits in text."""
    return [
        (w, n)
        for n, line in enumerate(text.splitlines(), 1)
        for w in _WORD.findall(line.lower())
    ]


def _walk(obj, keys):
    """Every string under any of `keys` in a JSON value (a list of strings counts as its strings)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys:
                yield from (
                    x for x in (v if isinstance(v, list) else [v]) if isinstance(x, str)
                )
            yield from _walk(v, keys)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v, keys)


def load_gt(paths) -> tuple[set[str], set[str]]:
    """(four-word phrases, forbidden names, both lower-case) read from the ground-truth files at `paths`."""
    grams: set[str] = set()
    names: set[str] = set()
    for p in paths:
        data = json.loads(Path(p).read_text(encoding="utf-8"))
        for text in _walk(data, PHRASE_KEYS):
            w = [x for x, _ in words_with_lines(text)]
            grams.update(" ".join(w[i : i + N]) for i in range(len(w) - N + 1))
            names.update(m.group(0).rstrip(".-").lower() for m in _PATH.finditer(text))
        names.update(s.strip().lower() for s in _walk(data, NAME_KEYS))
    names.discard("")
    return grams, names


def scan_text(
    text: str, grams: set[str], names: set[str]
) -> list[tuple[int, str, str]]:
    """Sorted (line, kind, hash) hits in text; kind is `phrase` or `name`. A phrase is placed at its first word."""
    hits: set[tuple[int, str, str]] = set()
    w = words_with_lines(text)
    for i in range(len(w) - N + 1):
        gram = " ".join(x for x, _ in w[i : i + N])
        if gram in grams:
            hits.add((w[i][1], "phrase", phrase_hash(gram)))
    if names:
        rx = re.compile(
            "(?<![a-z0-9])(?:"
            + "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
            + ")(?![a-z0-9])"
        )
        for n, line in enumerate(text.lower().splitlines(), 1):
            hits.update((n, "name", phrase_hash(m.group(0))) for m in rx.finditer(line))
    return sorted(hits)


def expand_targets(paths) -> list[Path]:
    """Files named, plus every file under a named folder (sorted, `__pycache__` skipped)."""
    out: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            out.extend(
                f
                for f in sorted(p.rglob("*"))
                if f.is_file() and "__pycache__" not in f.parts
            )
        else:
            out.append(p)
    return out


def default_targets(sw: Path = SW) -> list[Path]:
    """The DESIGN 13.1 targets that exist under sw."""
    return [sw / t for t in TARGETS if (sw / t).exists()]


def scan_files(
    files, grams: set[str], names: set[str]
) -> list[tuple[str, int, str, str]]:
    out = []
    for f in files:
        text = Path(f).read_text(encoding="utf-8", errors="replace")
        out.extend(
            (str(f), line, kind, h) for line, kind, h in scan_text(text, grams, names)
        )
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="AO-1 leak lint: prints file, line and hash, never the phrase."
    )
    ap.add_argument("files", nargs="*", help="files or folders to scan")
    ap.add_argument(
        "--all", action="store_true", help="also scan the DESIGN 13.1 targets under SW"
    )
    ap.add_argument(
        "--gt-glob",
        help="glob of ground-truth JSON files; required, nothing is opened without it",
    )
    ap.add_argument(
        "--forbid",
        action="append",
        default=[],
        help="an extra forbidden name (repeatable)",
    )
    args = ap.parse_args(argv)
    if not args.gt_glob:
        print(
            "lint: --gt-glob is required (a person names the ground-truth files); nothing was opened",
            file=sys.stderr,
        )
        return 2
    gt_files = sorted(glob.glob(args.gt_glob, recursive=True))
    if not gt_files:
        print("lint: --gt-glob matched no file", file=sys.stderr)
        return 2
    try:
        grams, names = load_gt(gt_files)
    except (OSError, ValueError):
        print(
            "lint: a ground-truth file could not be read as JSON (content not shown)",
            file=sys.stderr,
        )
        return 2
    names.update(n.strip().lower() for n in args.forbid if n.strip())
    skip = {Path(f).resolve() for f in gt_files}
    files = [
        f
        for f in expand_targets([*args.files, *(default_targets() if args.all else [])])
        if f.resolve() not in skip
    ]
    if not files:
        print("lint: nothing to scan", file=sys.stderr)
        return 2
    hits = scan_files(files, grams, names)
    for f, line, kind, h in hits:
        print(f"{f}:{line}: leak {kind} hash={h}")
    print(f"lint: {len(hits)} hit(s) in {len(files)} file(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
