"""T04.05 -- ``hypothesis_table_v1`` recipe (COMP-018 / R-090 / D-0072).

Hypothesis-table normalizer for the troubleshoot-hypothesis lens
(COMP-029). The lens prompt asks workers for a ranked enumeration of
root-cause hypotheses for a failure or symptom, surfacing supporting
evidence, falsifying evidence, and the next probe per row. This recipe
collapses that emission into a canonical 5-column markdown table:

    ``| ID | Cause | Evidence | Confidence | Next Step |``

with an auto-assigned ``H-NN`` sequence on the ID column. Followed by a
free-form ``## Notes`` section preserved verbatim from the body.

Column mapping (worker raw -> canonical)
========================================

The worker prompt does not pin a fixed column set; models in practice
emit 4-, 5-, or 6-column tables in slightly different shapes. The
recipe maps cells positionally:

* cell 1 -> ``cause`` (the hypothesis itself).
* cell 2 -> ``evidence`` (supporting + falsifying joined when the
  worker emitted them as separate cells; see below).
* cell 3 -> ``confidence`` (normalized via :func:`parse_confidence` to
  a 0-100 integer-as-string, or a flattened qualitative label).
* cell 4+ -> ``next_step`` (joined with ``" / "``; extra trailing
  cells concat rather than drop so no model emission is silently lost
  per AC-011).

When the worker emits a 6-column table (``| Cause | Supporting |
Falsifying | Confidence | Next Probe |`` plus an optional rank/ID
column), the first cell still maps to ``cause`` and cells 2 and 3 are
joined with ``" | "`` into the canonical ``evidence`` cell.
Confidence/next-step align by tail-anchored slicing: the last cell is
always ``next_step`` and the penultimate is ``confidence`` whenever the
row width >= 4. This keeps the canonical 5-column shape stable across
worker-emission variance.

Confidence normalization mirrors :func:`bare_review_v1.parse_conf`:
extract the first run of digits and clamp to ``[0, 100]``. Qualitative
labels (``high``, ``medium``, ``low``) are passed through as the
recipe's neutrality boundary forbids the score interpretation that
would otherwise classify them; only the digit-run gets reformatted.

AC-011 boundary
---------------

The recipe MUST NOT score, dedup, or reorder findings. Row order is
the raw body's row order (model-emitted likelihood ranking is
preserved). Confidence cells are merely reformatted, never compared.
The T04.14 boundary test pins this contract.

Section discovery
-----------------

The recipe accepts a ``## Hypotheses`` heading (case-insensitive) but
does not require it -- any pipe-row block following a divider row is
treated as hypotheses (mirrors :mod:`findings_table_v1`). The
``## Notes`` heading is consumed verbatim with whitespace collapse.

§7.4 salvage semantics
----------------------

* ``status == "parse_error"`` and the body yields at least one
  hypothesis or non-empty notes -> :class:`NormalizedResult` with
  ``salvaged=True``; the Wave-2 dispatcher promotes to ``success`` per
  FR-028.
* ``status == "parse_error"`` and the body yields neither -> empty
  text + ``error="no hypotheses or notes"``; status stays
  ``parse_error``.
* ``status == "success"`` with no hypotheses AND no notes -> degrade
  to a freeform-fallback Notes section (first 300 chars of the body
  whitespace-flattened) so the worker's payload is never lost; the
  output table renders a placeholder row of dashes to keep the
  markdown table well-formed.

Empty raw body -> empty text + ``error="empty raw body"``.

Args contract (forwarded from ``recipe_args`` through
:func:`superclaude.cli.swarm.normalize.normalize_wave2`):

* ``status`` -- upstream worker status (``"success"`` /
  ``"parse_error"``). Drives §7.4 salvage gate.
* ``target`` -- absolute path of the failing target (frontmatter +
  slug source).
* ``target_checksum`` -- 12-hex sha256 of the (possibly truncated)
  target body.
* ``target_truncated`` -- ``True`` when the Wave-0 truncation policy
  fired.
* ``model_id`` / ``model_label`` -- transport-supplied model id +
  human-facing label.
* ``caller_label`` -- optional caller tag.
* ``elapsed_ms`` -- per-worker wall-clock elapsed.
* ``lens`` -- the lens name (defaults to ``"troubleshoot-hypothesis"``).
* ``tier`` -- caller-supplied tier label (defaults to
  ``"T2-tshoot"``).
* ``suspect`` -- caller-supplied suspect flag (defaults to ``False``;
  troubleshoot-hypothesis is non-suspect per COMP-029).
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
    "HypothesisTableV1",
    "DIVIDER_CELL_RE",
    "CAUSE_CAP",
    "EVIDENCE_CAP",
    "NEXT_STEP_CAP",
    "FALLBACK_NOTES_CAP",
    "iso_now",
    "yaml_str",
    "strip_frontmatter",
    "parse_confidence",
    "parse_hypothesis_table",
    "extract_notes",
    "render_markdown",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


# A markdown table divider row consists of cells that contain only
# hyphens, colons (alignment markers), and whitespace.
DIVIDER_CELL_RE: re.Pattern[str] = re.compile(r"^[\-:\s]+$")

# Per-cell character caps for body hygiene. Hypothesis rows commonly
# carry longer prose than findings rows (multi-clause causes, joined
# supporting + falsifying evidence) so the caps are slightly bumped.
CAUSE_CAP: int = 240
EVIDENCE_CAP: int = 320
NEXT_STEP_CAP: int = 240

# Cap on the freeform-fallback Notes section when the body yields no
# table rows AND no Notes heading.
FALLBACK_NOTES_CAP: int = 300


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def iso_now() -> str:
    """ISO-8601 UTC timestamp, matches sibling recipes."""
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


def parse_confidence(cell: str) -> str:
    """Reformat a confidence cell.

    Mirrors :func:`bare_review_v1.parse_conf`: extract the first
    digit-run and clamp to ``[0, 100]``. Qualitative labels with no
    digits are returned whitespace-collapsed (the recipe does not
    interpret ``high``/``medium``/``low`` as scores -- that crosses
    the AC-011 boundary). Empty / pure-whitespace input returns an
    empty string.
    """
    if not cell or not cell.strip():
        return ""
    m = re.search(r"\d+", cell)
    if m:
        return str(max(0, min(100, int(m.group()))))
    return " ".join(cell.split())


def parse_hypothesis_table(text: str) -> list[dict[str, str]]:
    """Parse markdown hypothesis-table rows out of ``text``.

    Strategy:

    * Walk the body line-by-line, tracking contiguous pipe-row blocks.
    * Within a block, the divider row (cells matching
      :data:`DIVIDER_CELL_RE`) separates header from data. Rows before
      the divider are header/label noise and skipped; rows after the
      divider are data rows.
    * Each data row's cells are split on ``|``, stripped, and packed
      into a dict with keys ``cause`` / ``evidence`` / ``confidence`` /
      ``next_step``.

    Tail-anchored slicing keeps the canonical 5-column shape stable
    across worker-emission variance:

    * width 1 -> all to ``cause``.
    * width 2 -> ``cause | next_step``.
    * width 3 -> ``cause | evidence | next_step``.
    * width 4 -> ``cause | evidence | confidence | next_step``.
    * width 5 -> ``cause | evidence_a | evidence_b | confidence |
      next_step`` (evidence cells joined with ``" | "``).
    * width >= 6 -> middle cells (positions 1..width-3) joined as
      evidence; tail anchors ``confidence`` and ``next_step``.

    AC-011: rows are emitted in body order; no scoring, dedup, or
    reorder. Extra cells join rather than drop so over-wide model
    emissions are preserved verbatim.
    """
    rows: list[dict[str, str]] = []
    saw_divider = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
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
        # Skip pure-empty data rows (structural noise).
        if not any(c for c in cells):
            continue

        width = len(cells)
        cause = _truncate(cells[0], CAUSE_CAP)
        evidence = ""
        confidence = ""
        next_step = ""
        if width == 1:
            pass
        elif width == 2:
            next_step = _truncate(cells[1], NEXT_STEP_CAP)
        elif width == 3:
            evidence = _truncate(cells[1], EVIDENCE_CAP)
            next_step = _truncate(cells[2], NEXT_STEP_CAP)
        elif width == 4:
            evidence = _truncate(cells[1], EVIDENCE_CAP)
            confidence = parse_confidence(cells[2])
            next_step = _truncate(cells[3], NEXT_STEP_CAP)
        else:
            # width >= 5: tail-anchor confidence + next_step; join
            # remaining middle cells into evidence so over-wide model
            # emissions are not dropped.
            middle = cells[1 : width - 2]
            evidence = _truncate(" | ".join(middle), EVIDENCE_CAP)
            confidence = parse_confidence(cells[width - 2])
            next_step = _truncate(cells[width - 1], NEXT_STEP_CAP)

        rows.append(
            {
                "cause": cause,
                "evidence": evidence,
                "confidence": confidence,
                "next_step": next_step,
            }
        )
    return rows


def extract_notes(text: str, cap: int = FALLBACK_NOTES_CAP) -> str:
    """Pull the contents of a ``## Notes`` heading (case-insensitive)."""
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
    hypotheses: list[dict[str, str]],
    notes: str,
) -> str:
    """Render the canonical hypothesis_table_v1 markdown body."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, int):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    lens_label = str(fm.get("lens") or "troubleshoot-hypothesis")
    lines += [
        "",
        f"# T2-Hypothesis Table ({lens_label}) — {slug}",
        "",
        "## Hypotheses",
        "",
        "| ID | Cause | Evidence | Confidence | Next Step |",
        "|----|-------|----------|------------|-----------|",
    ]
    if hypotheses:
        for i, h in enumerate(hypotheses, 1):
            lines.append(
                f"| H-{i:02d} | {h['cause']} | {h['evidence']} | "
                f"{h['confidence']} | {h['next_step']} |"
            )
    else:
        lines.append(
            "| H-00 | (no rows) | (no structured hypotheses returned) | — | — |"
        )
    lines += ["", "## Notes", notes or "(no notes returned)"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Recipe class
# ---------------------------------------------------------------------------


class HypothesisTableV1:
    """``hypothesis_table_v1`` -- troubleshoot-hypothesis recipe.

    Implements :class:`superclaude.cli.swarm.recipes.Recipe`. Used by
    the troubleshoot-hypothesis bundled lens (COMP-029); custom lenses
    with a hypothesis-shape table can opt in by binding
    ``recipe_name = "hypothesis_table_v1"`` on their
    :class:`LensEntry`.
    """

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        status = str(args.get("status", "success"))
        target = str(args.get("target", ""))
        checksum = str(args.get("target_checksum", ""))
        truncated = bool(args.get("target_truncated", False))
        model_id = str(args.get("model_id", ""))
        model_label = str(args.get("model_label", ""))
        caller_label = str(args.get("caller_label", "") or "")
        lens = str(
            args.get("lens", "troubleshoot-hypothesis") or "troubleshoot-hypothesis"
        )
        tier = str(args.get("tier", "T2-tshoot") or "T2-tshoot")
        suspect = bool(args.get("suspect", False))
        try:
            elapsed_ms = int(args.get("elapsed_ms", 0) or 0)
        except (TypeError, ValueError):
            elapsed_ms = 0
        generated = str(args.get("generated") or iso_now())

        if not raw_output or not raw_output.strip():
            return NormalizedResult(text="", salvaged=False, error="empty raw body")

        body = strip_frontmatter(raw_output)
        hypotheses = parse_hypothesis_table(body)
        notes = extract_notes(body)

        salvaged = False
        if status == "parse_error":
            if not hypotheses and not notes:
                return NormalizedResult(
                    text="",
                    salvaged=False,
                    error="no hypotheses or notes",
                )
            salvaged = True
        elif not hypotheses and not notes:
            # Freeform-fallback: never drop the model payload on a
            # success worker; collapse the body into the Notes section.
            notes = (
                _truncate(body, FALLBACK_NOTES_CAP)
                or "(no structured hypotheses returned)"
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
            "hypothesis_count": len(hypotheses),
        }
        text = render_markdown(slug, fm, hypotheses, notes)
        return NormalizedResult(text=text, salvaged=salvaged, error=None)
