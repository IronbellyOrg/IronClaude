"""T04.04 -- ``findings_table_v1`` recipe (COMP-017 / R-089 / D-0071).

Lens-shared findings-table normalizer covering the three findings-shape
bundled lenses (refactor-find, edge-case-hunt, doc-completeness). Each
of those lenses asks the worker model for a 4-column markdown table
whose columns vary semantically per lens (file:line / cleanup /
rationale / patch sketch for refactor-find; file:line / input-state /
why-breaks / repro for edge-case-hunt; section / gap-kind / issue /
suggested-fix for doc-completeness) but share the same structural
shape -- a header row, a divider row, then N data rows -- followed by a
free-form ``## Notes`` section.

This recipe transforms each worker's raw body into a canonical
``| ID | Locator | Finding | Detail | Action |`` table plus the
preserved Notes section, with an auto-assigned ``F-NN`` sequence on
the ID column. The 4 emitted cells map verbatim to Locator/Finding/
Detail/Action; missing trailing columns pad with empty strings; extra
trailing columns concat into the Action cell so no model emission is
silently dropped.

AC-011 boundary
---------------

The recipe MUST NOT score, dedup, or reorder findings. Row order is
the raw body's row order. The T04.14 boundary test pins this contract.

§7.4 salvage semantics
----------------------

* ``status == "parse_error"`` and the body yields at least one finding
  or non-empty notes -> :class:`NormalizedResult` with
  ``salvaged=True``; the Wave-2 dispatcher promotes to ``success`` per
  FR-028.
* ``status == "parse_error"`` and the body yields neither -> empty
  text + ``error="no findings or notes"``; status stays ``parse_error``.
* ``status == "success"`` with no findings AND no notes -> degrade to a
  freeform-fallback Notes section (first 300 chars of the body
  whitespace-flattened) so the worker's payload is never lost; the
  output table will be empty (`(no structured findings returned)` is
  rendered as a placeholder data row of dashes to keep the markdown
  table well-formed).

Empty raw body -> empty text + ``error="empty raw body"``.

Args contract (forwarded from ``recipe_args`` through
:func:`superclaude.cli.swarm.normalize.normalize_wave2`):

* ``status`` -- upstream worker status (``"success"`` /
  ``"parse_error"``). Drives the §7.4 salvage gate.
* ``target`` -- absolute path of the reviewed target (frontmatter +
  slug source).
* ``target_checksum`` -- 12-hex sha256 of the (possibly truncated)
  target body.
* ``target_truncated`` -- ``True`` when the Wave-0 truncation policy
  fired.
* ``model_id`` / ``model_label`` -- transport-supplied model id +
  human-facing label.
* ``caller_label`` -- optional caller tag.
* ``elapsed_ms`` -- per-worker wall-clock elapsed.
* ``lens`` -- the lens name the recipe was invoked for (defaults to
  ``"findings-table"``). Frontmatter records this so consumers can
  distinguish refactor-find vs edge-case-hunt vs doc-completeness
  outputs sharing the same recipe.
* ``tier`` -- caller-supplied tier label (mirrors
  :attr:`LensEntry.tier`). Defaults to ``"T2"``.
* ``suspect`` -- caller-supplied suspect flag. Defaults to ``False``
  (findings-shape lenses are by-construction non-suspect today; the
  bare-review lens is the lone suspect:true entry and routes through
  :mod:`bare_review_v1`).
* ``generated`` -- ISO-8601 UTC timestamp. When absent the recipe
  stamps :func:`iso_now`. Tests pin a fixed value so the frontmatter
  is deterministic.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Any

from superclaude.cli.swarm.recipes import NormalizedResult

__all__ = [
    "FindingsTableV1",
    "DIVIDER_CELL_RE",
    "FALLBACK_NOTES_CAP",
    "CLAIM_CAP",
    "DETAIL_CAP",
    "iso_now",
    "yaml_str",
    "strip_frontmatter",
    "parse_findings_table",
    "extract_notes",
    "render_markdown",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


# A markdown table divider row consists of cells that contain only
# hyphens, colons (alignment markers), and whitespace.
DIVIDER_CELL_RE: re.Pattern[str] = re.compile(r"^[\-:\s]+$")

# Per-cell character caps for body hygiene. Keep generous enough to
# preserve model-emitted detail while bounding worst-case row width so
# the canonical markdown table remains terminal-friendly. Bare-review
# uses 120 for its Claim cell; the findings-table lenses carry more
# explanatory text in their rows so the cap is bumped to 200 for the
# Detail/Action columns.
CLAIM_CAP: int = 200
DETAIL_CAP: int = 200

# Cap on the freeform-fallback Notes section when the body yields no
# table rows AND no Notes heading.
FALLBACK_NOTES_CAP: int = 300


# ---------------------------------------------------------------------------
# Helpers (mirror bare_review_v1.py shape so contributors recognise the
# pattern; the implementations differ in column model but the public
# surface is intentionally similar).
# ---------------------------------------------------------------------------


def iso_now() -> str:
    """ISO-8601 UTC timestamp, matches :func:`bare_review_v1.iso_now`."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def yaml_str(v: str) -> str:
    """Double-quote a scalar for safe single-line YAML emission."""
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def strip_frontmatter(text: str) -> str:
    """Drop a leading ``---``-delimited YAML frontmatter block, if any."""
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def _truncate(cell: str, cap: int) -> str:
    """Whitespace-collapse + hard-cap a cell string."""
    return " ".join(cell.split())[:cap]


def parse_findings_table(text: str) -> list[dict[str, str]]:
    """Parse markdown findings-table rows out of ``text``.

    Strategy:

    * Walk the body line-by-line, tracking contiguous pipe-row blocks.
    * Within a block, the divider row (cells matching
      :data:`DIVIDER_CELL_RE`) separates header from data. Rows before
      the divider are header/label noise and skipped; rows after the
      divider are data rows.
    * Each data row's cells are split on ``|``, stripped, and packed
      into a dict with keys ``locator`` / ``finding`` / ``detail`` /
      ``action``. The first cell maps to ``locator``; the next two map
      to ``finding`` and ``detail``; any further cells are joined with
      ``" / "`` into ``action`` so over-wide model emissions are not
      silently dropped (AC-011 preservation).
    * Rows whose cells are all empty after stripping are skipped (pure
      structural noise, not findings).

    AC-011: rows are emitted in body order; no scoring, dedup, or
    reorder.
    """
    rows: list[dict[str, str]] = []
    saw_divider = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            # Reset block state on any non-pipe line so we re-detect
            # header/divider for the next block.
            saw_divider = False
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # Drop pure-whitespace cells at the tail so trailing pipes do
        # not inflate cell counts.
        while cells and cells[-1] == "":
            cells.pop()
        if not cells:
            continue
        # Divider row: every cell matches the divider regex.
        if all(DIVIDER_CELL_RE.match(c or "") for c in cells):
            saw_divider = True
            continue
        if not saw_divider:
            # Header row (or pre-divider noise). Skip.
            continue
        # Data row -- preserve verbatim.
        if not any(c for c in cells):
            continue
        locator = _truncate(cells[0], CLAIM_CAP)
        finding = _truncate(cells[1], CLAIM_CAP) if len(cells) > 1 else ""
        detail = _truncate(cells[2], DETAIL_CAP) if len(cells) > 2 else ""
        action = ""
        if len(cells) > 3:
            action = _truncate(" / ".join(cells[3:]), DETAIL_CAP)
        rows.append(
            {
                "locator": locator,
                "finding": finding,
                "detail": detail,
                "action": action,
            }
        )
    return rows


def extract_notes(text: str, cap: int = FALLBACK_NOTES_CAP) -> str:
    """Pull the contents of a ``## Notes`` heading (case-insensitive).

    Mirrors :func:`bare_review_v1.extract_section` but pinned to the
    Notes heading -- findings_table_v1 lenses do not emit a Verdict
    section.
    """
    m = re.search(r"^#+\s*Notes\s*$", text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^#+\s", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(body.split())[:cap]


def render_markdown(
    slug: str,
    fm: dict[str, Any],
    findings: list[dict[str, str]],
    notes: str,
) -> str:
    """Render the canonical findings_table_v1 markdown body."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, int):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    lens_label = str(fm.get("lens") or "findings-table")
    lines += [
        "",
        f"# T2-Findings Table ({lens_label}) — {slug}",
        "",
        "## Findings",
        "",
        "| ID | Locator | Finding | Detail | Action |",
        "|----|---------|---------|--------|--------|",
    ]
    if findings:
        for i, f in enumerate(findings, 1):
            lines.append(
                f"| F-{i:02d} | {f['locator']} | {f['finding']} | "
                f"{f['detail']} | {f['action']} |"
            )
    else:
        lines.append("| F-00 | (no rows) | (no structured findings returned) | — | — |")
    lines += ["", "## Notes", notes or "(no notes returned)"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Recipe class
# ---------------------------------------------------------------------------


class FindingsTableV1:
    """``findings_table_v1`` -- lens-shared findings-table recipe.

    Implements :class:`superclaude.cli.swarm.recipes.Recipe`. Used by
    the three findings-shape bundled lenses (refactor-find,
    edge-case-hunt, doc-completeness); custom lenses with a 4-column
    findings table can opt in by binding ``recipe_name =
    "findings_table_v1"`` on their :class:`LensEntry`.
    """

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        status = str(args.get("status", "success"))
        target = str(args.get("target", ""))
        checksum = str(args.get("target_checksum", ""))
        truncated = bool(args.get("target_truncated", False))
        model_id = str(args.get("model_id", ""))
        model_label = str(args.get("model_label", ""))
        caller_label = str(args.get("caller_label", "") or "")
        lens = str(args.get("lens", "findings-table") or "findings-table")
        tier = str(args.get("tier", "T2") or "T2")
        suspect = bool(args.get("suspect", False))
        try:
            elapsed_ms = int(args.get("elapsed_ms", 0) or 0)
        except (TypeError, ValueError):
            elapsed_ms = 0
        generated = str(args.get("generated") or iso_now())

        if not raw_output or not raw_output.strip():
            return NormalizedResult(text="", salvaged=False, error="empty raw body")

        body = strip_frontmatter(raw_output)
        findings = parse_findings_table(body)
        notes = extract_notes(body)

        salvaged = False
        if status == "parse_error":
            # §7.4: stay failed only when nothing recoverable.
            if not findings and not notes:
                return NormalizedResult(
                    text="",
                    salvaged=False,
                    error="no findings or notes",
                )
            salvaged = True
        elif not findings and not notes:
            # Freeform-fallback: never drop the model payload on a
            # success worker; collapse the body into the Notes section.
            notes = (
                _truncate(body, FALLBACK_NOTES_CAP)
                or "(no structured findings returned)"
            )

        slug = os.path.splitext(os.path.basename(target))[0] if target else ""
        fm: dict[str, Any] = {
            "schema_version": "1.0",
            "tier": tier,
            "suspect": suspect,
            "lens": lens,
            "reviewer_model_id": model_id,
            "reviewer_model_label": model_label,
            "target": target,
            "target_checksum": checksum,
            "target_truncated": truncated,
            "generated": generated,
            "caller_label": caller_label,
            "elapsed_ms": elapsed_ms,
            "finding_count": len(findings),
        }
        text = render_markdown(slug, fm, findings, notes)
        return NormalizedResult(text=text, salvaged=salvaged, error=None)
