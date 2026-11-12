"""`superclaude review verify-citations`: deterministic, advisory pre-check of the findings-v2 citations of reviewer cards.

For every citation of every parsed finding it reads the cited file (under --root, and only when the path is in the
input snapshot) and records at most one flag:
- missing-file: the path is not in the snapshot, resolves outside --root, or cannot be read;
- out-of-range: line_end is past the last line of the file;
- quote-not-found: the citation has a quote and it is not in the cited lines (whitespace-normalised); advisory,
  because a failed locate is not proof that the citation is unfounded.

It writes <out>/panel/precheck.json, with a `reread_set` listing every flagged citation (the evidence validator
re-reads them even when its sampling would skip them). It spends no model tokens, drops nothing, and neither
modifies a card nor writes anything else. The validator alone decides drops.
"""

from __future__ import annotations

import json
from pathlib import Path

import click

from superclaude.cli.review import cluster_cmd as cc
from superclaude.cli.review import findings_v2 as fv2

SCHEMA = "review-precheck/1"


def _norm(text: str) -> str:
    return " ".join(text.split())


def _snapshot_paths(entries: list) -> set[str]:
    out = set()
    for e in entries:
        if isinstance(e, str):
            out.add(e)
        elif isinstance(e, dict) and isinstance(e.get("path"), str):
            out.add(e["path"])
    return out


def _check(
    citation: dict, snapshot: set[str], root: Path, cache: dict
) -> tuple[str | None, str | None]:
    """(flag, reason) for one citation; (None, None) when it checks out."""
    path = citation["path"]
    if path not in snapshot:
        return "missing-file", "not-in-snapshot"
    if path not in cache:
        try:
            target = (root / path).resolve()
            if root != target and root not in target.parents:
                cache[path] = ("outside-root", None)
            else:
                cache[path] = (
                    "ok",
                    target.read_text(encoding="utf-8", errors="replace").splitlines(),
                )
        except OSError:
            cache[path] = ("unreadable", None)
    state, lines = cache[path]
    if state == "outside-root":
        return "missing-file", "outside-root"
    if state == "unreadable":
        return "missing-file", "not-readable"
    if citation["line_end"] > len(lines):
        return "out-of-range", f"file has {len(lines)} lines"
    quote = citation.get("quote")
    if quote and _norm(quote) not in _norm(
        " ".join(lines[citation["line_start"] - 1 : citation["line_end"]])
    ):
        return "quote-not-found", "quote is not in the cited lines"
    return None, None


@click.command(name="verify-citations")
@click.option(
    "--cards",
    "cards_dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory of reviewer cards (*.md with a findings-v2 block).",
)
@click.option(
    "--snapshot",
    "snapshot",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="artifacts/input-snapshot.yaml; only its paths are read.",
)
@click.option(
    "--root",
    "root",
    default=".",
    show_default=True,
    type=click.Path(exists=True, file_okay=False),
    help="Repository root: the base for reads.",
)
@click.option(
    "--coverage",
    "coverage",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help='JSON sidecar {reviewer_id: {"assigned": [row ids], "observed": [row ids]}}, the same file `review cluster --coverage` reads. Without it a finding with coverage_rows is rejected by the block parser and its citations are not checked.',
)
@click.option(
    "--out",
    "out",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory; the result goes to <out>/panel/precheck.json.",
)
def command(cards_dir, snapshot, root, coverage, out) -> None:
    """Flag citations whose file is missing, whose lines are out of range or whose quote is not found (advisory)."""
    cards = sorted(Path(cards_dir).glob("*.md"))
    if not cards:
        raise click.ClickException(f"no *.md cards in {cards_dir}")
    snap = _snapshot_paths(cc._snapshot_files(Path(snapshot)))
    base = Path(root).resolve()
    cache: dict = {}
    rows, listing = [], []
    cover = cc._sidecar(Path(coverage)) if coverage else {}
    for card in cards:
        rid = card.stem
        if coverage and rid not in cover:
            raise click.ClickException(
                f"the coverage file has no entry for {rid} (use {{}} for a card with no coverage rows)"
            )
        try:
            assigned, observed = fv2.coverage_context(cover.get(rid))
        except ValueError as exc:
            raise click.ClickException(f"coverage for {rid}: {exc}") from exc
        block = fv2.parse_block(
            cc._read(card, "card"), assigned_rows=assigned, observed_rows=observed
        )
        listing.append(
            {"card": card.name, "reviewer_id": rid, "block_state": block["state"]}
        )
        for f in block["findings"]:
            for i, c in enumerate(f.get("citations") or [], 1):
                if fv2._check_citation(c) is not None:
                    continue  # a malformed citation cannot be read; the block checker reports it
                flag, reason = _check(c, snap, base, cache)
                rows.append(
                    {
                        "reviewer_id": rid,
                        "finding_id": f["id"],
                        "citation": i,
                        "role": c["role"],
                        "path": c["path"],
                        "line_start": c["line_start"],
                        "line_end": c["line_end"],
                        "flag": flag,
                        "reason": reason,
                        "advisory": flag == "quote-not-found",
                    }
                )
    flagged = [r for r in rows if r["flag"]]
    result = {
        "schema": SCHEMA,
        "cards": listing,
        "citations": rows,
        "checked": len(rows),
        "flagged": len(flagged),
        "by_flag": {
            k: sum(1 for r in flagged if r["flag"] == k)
            for k in ("missing-file", "out-of-range", "quote-not-found")
        },
        "reread_set": [
            {k: r[k] for k in ("reviewer_id", "finding_id", "citation", "path", "flag")}
            for r in flagged
        ],
    }
    target = Path(out) / "panel" / "precheck.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    click.echo(
        json.dumps(
            {"written": str(target), "checked": len(rows), "flagged": len(flagged)},
            sort_keys=True,
        )
    )
