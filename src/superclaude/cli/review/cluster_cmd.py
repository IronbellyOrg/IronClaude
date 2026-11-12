"""`superclaude review cluster`: cluster the findings of calibrated reviewer cards (K4 cluster_v2).

Cards are the `*.md` files of CARDS_DIR, in file-name order; the file stem is the reviewer id. Each card holds a
`## Findings block` with a findings-v2 block and, optionally, a `calibration:` mapping with `per_finding`
({finding id: confidence or {finding_confidence: confidence}}) in a fenced yaml block or as an unfenced
`calibration:` block. A `--calibration` JSON sidecar {reviewer_id: {finding id: confidence}} overrides the
embedded values of each reviewer it names with a non-empty mapping.

Without --kept it writes <out>/panel/clusters.json. With --kept (one finding id per line, or
`reviewer_id:finding_id` to pin one reviewer) it writes <out>/panel/clusters_kept.json (the clusters_kept pass)
and leaves clusters.json alone. A card whose block is not valid is listed as invalid under `cards` and is left
out of the agreement. Cards are never modified and nothing else is written.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import click
import yaml

from superclaude.cli.review import card_convert as cc
from superclaude.cli.review import findings_v2 as fv2

_FENCE = re.compile(r"```[ \t]*ya?ml[ \t]*\n(.*?)\n[ \t]*```", re.S | re.I)
_BARE = re.compile(r"^calibration:[ \t]*\n((?:[ \t]+\S.*(?:\n|$)|[ \t]*\n)+)", re.M)


def _embedded_calibration(text: str) -> dict:
    """{finding id: confidence} from a `calibration.per_finding` mapping in the card text (fenced yaml blocks are tried first, then unfenced ones)."""
    sources = [m.group(1) for m in _FENCE.finditer(text)]
    sources += ["calibration:\n" + m.group(1) for m in _BARE.finditer(text)]
    for src in sources:
        try:
            doc = yaml.safe_load(src)
        except yaml.YAMLError:
            continue
        cal = doc.get("calibration") if isinstance(doc, dict) else None
        per = cal.get("per_finding") if isinstance(cal, dict) else None
        if isinstance(per, dict):
            return {
                str(k): (v.get("finding_confidence") if isinstance(v, dict) else v)
                for k, v in per.items()
            }
    return {}


def _read(path: Path, what: str) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise click.ClickException(f"cannot read {what} {path}: {exc}") from exc


def _snapshot_files(path: Path) -> list:
    try:
        data = yaml.safe_load(_read(path, "snapshot"))
    except yaml.YAMLError as exc:
        raise click.ClickException(f"{path} is not valid YAML: {exc}") from exc
    return cc._snapshot_entries(data)


def _sidecar(path: Path) -> dict:
    try:
        data = json.loads(_read(path, "calibration sidecar"))
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise click.ClickException(
            f"{path} must hold {{reviewer_id: {{finding_id: confidence}}}}"
        )
    return data


def _kept_pairs(path: Path, blocks: dict[str, dict]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for raw in _read(path, "kept file").splitlines():
        entry = raw.strip()
        if not entry or entry.startswith("#"):
            continue
        rid, sep, fid = entry.rpartition(":")
        if sep:
            pairs.append((rid, fid))
            continue
        pairs += [
            (r, f["id"])
            for r, b in blocks.items()
            for f in b["findings"]
            if isinstance(f, dict) and f.get("id") == entry
        ]
    return pairs


@click.command(name="cluster")
@click.argument("cards_dir", type=click.Path(exists=True, file_okay=False))
@click.option(
    "--snapshot",
    "snapshot",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="artifacts/input-snapshot.yaml (its file_list gives the resolvable paths).",
)
@click.option(
    "--calibration",
    "calibration",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help="JSON sidecar {reviewer_id: {finding_id: finding_confidence}}.",
)
@click.option(
    "--coverage",
    "coverage",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help='JSON sidecar {reviewer_id: {"assigned": [row ids], "observed": [row ids]}}: the coverage context a card\'s block is checked against. Without it a card with no findings, or with coverage_rows, is listed invalid.',
)
@click.option(
    "--kept",
    "kept",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help="Finding ids the evidence validator kept, one per line (or reviewer_id:finding_id); writes clusters_kept.json.",
)
@click.option(
    "--out",
    "out",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory; the result goes to <out>/panel/.",
)
def command(cards_dir, snapshot, calibration, coverage, kept, out) -> None:
    """Cluster the findings of calibrated reviewer cards; print where the result was written."""
    # Imported here so that loading the `review` group does not load cluster.py (other review commands stay unaffected).
    from superclaude.cli.review import cluster as cl

    cards = sorted(Path(cards_dir).glob("*.md"))
    if not cards:
        raise click.ClickException(f"no *.md cards in {cards_dir}")
    side = _sidecar(Path(calibration)) if calibration else {}
    cover = _sidecar(Path(coverage)) if coverage else {}
    records, blocks, listing = [], {}, []
    for ordinal, card in enumerate(cards, 1):
        text = _read(card, "card")
        rid = card.stem
        ctx = cover.get(rid) if isinstance(cover.get(rid), dict) else {}
        block = fv2.parse_block(
            text,
            assigned_rows=ctx.get("assigned"),
            observed_rows=ctx.get("observed") or (),
        )
        cal = side.get(rid) if isinstance(side.get(rid), dict) else None
        records.append((rid, ordinal, block, cal or _embedded_calibration(text)))
        blocks[rid] = block
        listing.append(
            {
                "card": card.name,
                "reviewer_id": rid,
                "state": "complete" if block["state"] == "complete" else "invalid",
                "block_state": block["state"],
                "errors": block["errors"],
            }
        )
    files = _snapshot_files(Path(snapshot))
    if kept:
        result = cl.clusters_kept(records, files, _kept_pairs(Path(kept), blocks))
        name = "clusters_kept.json"
    else:
        result = cl.cluster_v2(records, files)
        name = "clusters.json"
    # How many clustered findings were matched to a numeric calibration (a number from 0 to 1 under the finding's id).
    # A low count has several possible causes (ids that differ, no calibration given, values that are not numbers,
    # findings the calibrator left unscored); this report only counts, it does not say which.
    clustered = sum(len(c["members"]) for c in result["clusters"])
    coverage = {
        "clustered_findings": clustered,
        "calibrated_findings": clustered - len(result["uncalibrated_findings"]),
    }
    result = {**result, "cards": listing, "calibration_coverage": coverage}
    target = Path(out) / "panel" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    click.echo(
        json.dumps(
            {
                "written": str(target),
                "cluster_agreement": result["cluster_agreement"],
                "calibrated_findings": f"{coverage['calibrated_findings']}/{coverage['clustered_findings']}",
                "invalid": [
                    c["reviewer_id"] for c in listing if c["state"] != "complete"
                ],
            },
            sort_keys=True,
        )
    )
