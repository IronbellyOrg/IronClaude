"""T04.07 -- ``verdict_only_v1`` recipe (COMP-019 / R-091 / D-0073).

Minimal verdict-shape normalizer covering the two verdict-shape bundled
lenses (spec-completeness, feasibility-probe). Each of those lenses
asks the worker model for a single yes/no/uncertain verdict plus a
one-line rationale describing why -- backed by an optional concerns or
gaps table whose row-by-row content is preserved verbatim so no model
emission is silently dropped (AC-011).

This recipe collapses that emission into a canonical three-section
markdown body:

    ``## Verdict``       canonical ``yes`` / ``no`` / ``uncertain`` label
                         (alias-mapped from common synonyms; unknown
                         labels pass through whitespace-collapsed).
    ``## Rationale``     one-line rationale extracted from the worker's
                         Verdict section tail (or freeform-fallback from
                         the body when no Verdict heading is present).
    ``## Notes``         body-preserved Notes / Gaps / Concerns content
                         (whitespace-collapsed, hard-capped) so the
                         supporting table / commentary is never lost.

Plus a YAML frontmatter block whose shape mirrors the sibling recipes
(:mod:`bare_review_v1`, :mod:`findings_table_v1`,
:mod:`hypothesis_table_v1`) so downstream consumers (M5 reduce, M6
resume) read every recipe's sidecar uniformly.

Verdict label normalization
===========================

The worker prompt does not pin the verdict vocabulary; in practice
models emit ``feasible`` / ``infeasible`` (feasibility-probe),
``complete`` / ``incomplete`` (spec-completeness), or the literal
``yes`` / ``no`` / ``uncertain`` from the prompt guidance. The recipe
maps these via :data:`VERDICT_ALIASES` onto the canonical triple
``{"yes", "no", "uncertain"}``. Unknown labels pass through
whitespace-collapsed rather than being silently coerced -- this
preserves the AC-011 boundary (don't drop the model's signal) while
keeping the schema useful for the common case.

Confidence (when present as a digit-run inside the Verdict section) is
extracted via :func:`parse_confidence` and clamped to ``[0, 100]``; it
appears on the rendered verdict line as ``<label> (<conf>)``.
Qualitative confidence labels (``high`` / ``medium`` / ``low``) pass
through verbatim -- the recipe does not classify them (that would
cross the AC-011 boundary).

AC-011 boundary
---------------

The recipe MUST NOT score, dedup, or reorder findings. The verdict
label is reformatted (alias-mapped), never compared; the rationale is
extracted verbatim; the supporting body content is preserved verbatim
inside the Notes section so over-wide model emissions are not silently
dropped. The T04.14 boundary test pins this contract.

Section discovery
-----------------

The recipe accepts ``## Verdict`` (case-insensitive) as the primary
verdict heading. Falls back to the first non-empty body line when the
heading is absent (mirrors the freeform-fallback in
:mod:`findings_table_v1` and :mod:`hypothesis_table_v1`).

The recipe accepts ``## Notes`` (case-insensitive) for the preserved
Notes section. Bundled lenses also emit ``## Gaps`` (spec-completeness)
or ``## Concerns`` (feasibility-probe) headings -- those are folded
into the Notes section so the rendered shape is uniform across both
lenses. The body of any matched section is whitespace-collapsed and
hard-capped at :data:`NOTES_CAP`.

§7.4 salvage semantics
----------------------

* ``status == "parse_error"`` and the body yields at least one of:
  verdict label, rationale, or non-empty notes -> :class:`NormalizedResult`
  with ``salvaged=True``; the Wave-2 dispatcher promotes to ``success``
  per FR-028.
* ``status == "parse_error"`` and the body yields none -> empty text +
  ``error="no verdict or notes"``; status stays ``parse_error``.
* ``status == "success"`` with no verdict label AND no rationale AND no
  notes -> freeform-fallback: rationale becomes the first
  :data:`RATIONALE_CAP` chars of the body (whitespace-flattened); the
  verdict label degrades to ``uncertain`` so the rendered body is
  well-formed.

Empty raw body -> empty text + ``error="empty raw body"``.

Args contract (forwarded from ``recipe_args`` through
:func:`superclaude.cli.swarm.normalize.normalize_wave2`):

* ``status`` -- upstream worker status (``"success"`` / ``"parse_error"``).
  Drives §7.4 salvage gate.
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
* ``lens`` -- the lens name (defaults to ``"verdict-only"``).
  Frontmatter records this so consumers can distinguish
  spec-completeness vs feasibility-probe outputs sharing the same
  recipe.
* ``tier`` -- caller-supplied tier label (defaults to ``"T2"``).
* ``suspect`` -- caller-supplied suspect flag (defaults to ``False``).
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
    "VerdictOnlyV1",
    "VERDICT_ALIASES",
    "CANONICAL_VERDICTS",
    "VERDICT_LABEL_CAP",
    "RATIONALE_CAP",
    "NOTES_CAP",
    "iso_now",
    "yaml_str",
    "strip_frontmatter",
    "parse_confidence",
    "parse_verdict",
    "extract_section",
    "render_markdown",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


CANONICAL_VERDICTS: tuple[str, ...] = ("yes", "no", "uncertain")
"""The three canonical verdict labels (``yes`` / ``no`` / ``uncertain``)."""


VERDICT_ALIASES: dict[str, str] = {
    # yes -- "the thing works / is complete / is feasible"
    "yes": "yes",
    "y": "yes",
    "true": "yes",
    "ok": "yes",
    "okay": "yes",
    "complete": "yes",
    "completeness": "yes",
    "feasible": "yes",
    "ready": "yes",
    "green": "yes",
    "viable": "yes",
    "pass": "yes",
    "passes": "yes",
    "approved": "yes",
    # no -- "the thing does not work / is incomplete / is infeasible"
    "no": "no",
    "n": "no",
    "false": "no",
    "incomplete": "no",
    "infeasible": "no",
    "broken": "no",
    "blocker": "no",
    "blocked": "no",
    "red": "no",
    "fail": "no",
    "fails": "no",
    "rejected": "no",
    "not-feasible": "no",
    "not_feasible": "no",
    # uncertain -- "needs more information / risky / partial"
    "uncertain": "uncertain",
    "unclear": "uncertain",
    "unknown": "uncertain",
    "maybe": "uncertain",
    "risky": "uncertain",
    "partial": "uncertain",
    "yellow": "uncertain",
    "tbd": "uncertain",
    "depends": "uncertain",
    "indeterminate": "uncertain",
}
"""Worker-emitted label -> canonical verdict triple (yes/no/uncertain).

Mirrors the alias pattern from :data:`bare_review_v1.SEV_ALIASES`.
Unknown labels are NOT silently coerced to a canonical value -- they
pass through whitespace-collapsed so AC-011 preservation holds. The
canonical mapping covers the synonyms emitted by the two bundled
verdict-shape lenses (spec-completeness, feasibility-probe) plus the
common-case yes/no/uncertain vocabulary the prompt guidance pins.
"""


# Per-section character caps. The verdict label cap is tight because
# canonical labels are 3-9 chars; the rationale cap matches
# :mod:`bare_review_v1`'s ``Verdict`` extract cap (300) so the shape
# parity holds; the notes cap is generous because the supporting
# concerns/gaps body content is preserved here (AC-011).
VERDICT_LABEL_CAP: int = 32
RATIONALE_CAP: int = 300
NOTES_CAP: int = 600


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


def _flatten(text: str, cap: int) -> str:
    """Whitespace-collapse + hard-cap a string."""
    return " ".join(text.split())[:cap]


def parse_confidence(cell: str) -> str:
    """Reformat a confidence cell.

    Mirrors :func:`hypothesis_table_v1.parse_confidence`: extract the
    first digit-run and clamp to ``[0, 100]``. Qualitative labels with
    no digits return whitespace-collapsed (the recipe does not
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


def extract_section(text: str, heading: str, cap: int) -> str:
    """Pull the contents of a ``## <heading>`` section (case-insensitive).

    Mirrors :func:`bare_review_v1.extract_section`. Returns the section
    body whitespace-collapsed and hard-capped at ``cap`` chars. Returns
    an empty string when the heading is not present.
    """
    m = re.search(
        rf"^#+\s*{re.escape(heading)}\s*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^#+\s", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(body.split())[:cap]


def parse_verdict(section_text: str) -> tuple[str, str, str]:
    """Split a verdict-section body into ``(label, confidence, rationale)``.

    Strategy:

    * The section is whitespace-flattened, then split into a *head
      zone* (label + optional confidence) and a *rationale zone* on
      the first em-dash (``—``), double-dash (``--``), surrounded
      single-hyphen, or ``:<space>`` separator. When no separator is
      present the whole section is the head zone and rationale is
      empty.
    * The head zone's first ``[A-Za-z][A-Za-z_-]*`` run is treated as
      the candidate label and looked up in :data:`VERDICT_ALIASES`. A
      hit yields a canonical triple member; a miss returns the
      candidate verbatim (capped at :data:`VERDICT_LABEL_CAP`) --
      AC-011 forbids silent coercion of unknown labels onto the
      canonical set.
    * Confidence is the first digit-run inside the *head zone only*
      (digits elsewhere in the rationale -- e.g. "needs 100 tests" --
      are not classified as confidence).
    * Empty / pure-whitespace section returns ``("", "", "")``.

    Returns:
        ``(label, confidence, rationale)`` -- each a string. Any of
        the three may be empty when the worker did not emit it.
    """
    if not section_text or not section_text.strip():
        return "", "", ""

    flat = " ".join(section_text.split())

    # Split head zone from rationale on the first em-dash, double-dash,
    # single-hyphen-with-spaces, or ``:<space>`` separator. The
    # separator characters are consumed; surrounding whitespace already
    # collapsed by the flatten step above.
    sep = re.search(r"\s(—|--|-)\s|:\s", flat)
    if sep:
        head_zone = flat[: sep.start()].strip()
        rationale_zone = flat[sep.end() :].strip()
    else:
        head_zone = flat.strip()
        rationale_zone = ""

    # Candidate label: first letter-anchored run (preserves embedded
    # underscores / hyphens such as ``not-feasible``).
    label = ""
    m_head = re.match(r"([A-Za-z][A-Za-z_-]*)", head_zone)
    if m_head:
        candidate = m_head.group(1)
        head_key = candidate.lower()
        if head_key in VERDICT_ALIASES:
            label = VERDICT_ALIASES[head_key]
        else:
            label = _flatten(candidate, VERDICT_LABEL_CAP)

    # Confidence: digit-run in head zone only.
    conf_match = re.search(r"\d+", head_zone)
    confidence = parse_confidence(conf_match.group()) if conf_match else ""

    rationale = _flatten(rationale_zone, RATIONALE_CAP)
    return label, confidence, rationale


def render_markdown(
    slug: str,
    fm: dict[str, Any],
    label: str,
    confidence: str,
    rationale: str,
    notes: str,
) -> str:
    """Render the canonical verdict_only_v1 markdown body."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, int):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    lens_label = str(fm.get("lens") or "verdict-only")
    lines += [
        "",
        f"# T2-Verdict ({lens_label}) — {slug}",
        "",
        "## Verdict",
    ]
    if label:
        if confidence:
            lines.append(f"{label} ({confidence})")
        else:
            lines.append(label)
    else:
        lines.append("(no verdict returned)")
    lines += [
        "",
        "## Rationale",
        rationale or "(no rationale returned)",
        "",
        "## Notes",
        notes or "(no notes returned)",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Recipe class
# ---------------------------------------------------------------------------


class VerdictOnlyV1:
    """``verdict_only_v1`` -- minimal verdict-shape recipe.

    Implements :class:`superclaude.cli.swarm.recipes.Recipe`. Used by
    the two verdict-shape bundled lenses (spec-completeness,
    feasibility-probe); custom lenses with a single-verdict output
    shape can opt in by binding ``recipe_name = "verdict_only_v1"`` on
    their :class:`LensEntry`.
    """

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        status = str(args.get("status", "success"))
        target = str(args.get("target", ""))
        checksum = str(args.get("target_checksum", ""))
        truncated = bool(args.get("target_truncated", False))
        model_id = str(args.get("model_id", ""))
        model_label = str(args.get("model_label", ""))
        caller_label = str(args.get("caller_label", "") or "")
        lens = str(args.get("lens", "verdict-only") or "verdict-only")
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

        verdict_section = extract_section(body, "Verdict", RATIONALE_CAP * 2)
        label, confidence, rationale = parse_verdict(verdict_section)

        # Notes folds the Notes / Gaps / Concerns headings into a
        # single section so the rendered shape is uniform across both
        # bundled verdict-shape lenses. First non-empty heading wins;
        # later headings concat with " | " so AC-011 preservation holds.
        notes_parts: list[str] = []
        for heading in ("Notes", "Gaps", "Concerns"):
            chunk = extract_section(body, heading, NOTES_CAP)
            if chunk:
                notes_parts.append(chunk)
        notes = _flatten(" | ".join(notes_parts), NOTES_CAP)

        salvaged = False
        if status == "parse_error":
            # §7.4: stay failed only when nothing recoverable.
            if not label and not rationale and not notes:
                return NormalizedResult(
                    text="",
                    salvaged=False,
                    error="no verdict or notes",
                )
            salvaged = True
        elif not label and not rationale and not notes:
            # Freeform-fallback: collapse the whole body into the
            # rationale so the worker's payload is never lost; degrade
            # the verdict label to ``uncertain`` so the rendered body
            # is well-formed.
            rationale = (
                _flatten(body, RATIONALE_CAP) or "(no structured verdict returned)"
            )
            label = "uncertain"

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
            "verdict": label,
            "verdict_confidence": confidence,
        }
        text = render_markdown(slug, fm, label, confidence, rationale, notes)
        return NormalizedResult(text=text, salvaged=salvaged, error=None)
