"""T04.03 -- ``bare-review-v1`` recipe (COMP-016 / R-088 / D-0070).

Ports the per-reviewer shape-transformation logic from
``src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`` into a
Wave-2 :class:`Recipe`-conforming object. The legacy script owned both
the per-reviewer normalization *and* the aggregator-level contract
emission; this recipe is intentionally narrower -- it only owns the
per-reviewer shape transform (frontmatter strip → findings table parse →
verdict / notes extraction → compressed-markdown render). The Wave-2
dispatcher (:mod:`superclaude.cli.swarm.normalize`) owns the file
lifecycle (raw read, atomic ``final_path`` write, meta sidecar emission,
``timeout`` / ``proxy_error`` short-circuit, salvage promotion).

A/B parity contract (T04.03 / TEST-003)
=======================================

The recipe preserves the legacy script's *byte-level output shape* for
every reviewer it processes. ``tests/swarm/test_recipe_bare_review.py``
exercises the parity gate: identical raw + meta inputs fed to both
paths produce byte-identical ``.md`` bodies (with a deterministic
``generated`` timestamp threaded through ``args["generated"]`` to
neutralise the only wall-clock-dependent frontmatter field).

The constants and helpers below (``SEV_ALIASES``, ``EMPTY_CITE``,
``FINDING_ID``, ``yaml_str``, ``strip_frontmatter``, ``normalize_sev``,
``normalize_cite``, ``parse_conf``, ``parse_findings``,
``extract_section``, ``render_markdown``, ``iso_now``) mirror the legacy
script verbatim so the byte-identity claim is mechanical: identical
inputs → identical outputs.

AC-011 boundary
---------------

This recipe MUST NOT score, dedupe, or reorder findings. It preserves
the order produced by ``parse_findings`` (table-row order in the raw
body) and emits every parsed row. The T04.14 boundary test pins this
contract across all six recipes.

§7.4 salvage semantics
----------------------

When the dispatcher hands the recipe a worker whose ``status`` arrived
as ``parse_error`` (via ``args["status"]``):

* If the body yields *any* finding or a non-empty verdict, the recipe
  returns ``NormalizedResult(text=<rendered md>, salvaged=True)`` and
  the dispatcher promotes ``parse_error -> success`` per FR-028.
* If the body yields neither, the recipe returns
  ``NormalizedResult(text="", salvaged=False, error="no findings or
  verdict")``. The dispatcher leaves the status at ``parse_error`` and
  retains the raw file for triage (§8 / OnParseError.retain_raw).

When the worker arrived as ``success`` and the body yields neither
findings nor a verdict, the recipe falls back to a placeholder verdict
(``"(no structured findings returned)"`` or the body's first 300 chars
flattened) -- mirroring the legacy ``else`` branch verbatim. The
``salvaged`` flag stays ``False`` because no parse-error promotion is
in flight.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Any

from superclaude.cli.swarm.recipes import NormalizedResult

__all__ = [
    "BareReviewV1",
    "SEV_ALIASES",
    "EMPTY_CITE",
    "FINDING_ID",
    "iso_now",
    "yaml_str",
    "strip_frontmatter",
    "normalize_sev",
    "normalize_cite",
    "parse_conf",
    "parse_findings",
    "extract_section",
    "render_markdown",
]


# ---------------------------------------------------------------------------
# Constants -- mirror t2_normalize.py verbatim (byte-identity parity).
# ---------------------------------------------------------------------------


SEV_ALIASES: dict[str, str] = {
    "crit": "crit",
    "critical": "crit",
    "blocker": "crit",
    "high": "high",
    "major": "high",
    "med": "med",
    "medium": "med",
    "moderate": "med",
    "low": "low",
    "minor": "low",
    "nit": "nit",
    "nitpick": "nit",
    "trivial": "nit",
    "info": "nit",
}
EMPTY_CITE: set[str] = {"", "none", "n/a", "na", "-", "--"}
FINDING_ID: re.Pattern[str] = re.compile(r"^f-?\d+$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers -- mirror t2_normalize.py verbatim.
# ---------------------------------------------------------------------------


def iso_now() -> str:
    """ISO-8601 UTC timestamp (legacy ``iso_now``, byte-identical format)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def yaml_str(v: str) -> str:
    """Double-quote a scalar for safe single-line YAML emission."""
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def strip_frontmatter(text: str) -> str:
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def normalize_sev(cell: str) -> str:
    return SEV_ALIASES.get(cell.strip().lower(), "med")


def normalize_cite(cell: str) -> str:
    return "none" if cell.strip().lower() in EMPTY_CITE else cell.strip()


def parse_conf(cell: str) -> str:
    m = re.search(r"\d+", cell)
    if not m:
        return ""
    return str(max(0, min(100, int(m.group()))))


def parse_findings(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5 or not FINDING_ID.match(cells[0]):
            continue
        claim = cells[2].replace("\n", " ").strip()[:120]
        if not claim:
            continue
        findings.append(
            {
                "sev": normalize_sev(cells[1]),
                "claim": claim,
                "cite": normalize_cite(cells[3]),
                "conf": parse_conf(cells[4]),
            }
        )
    return findings


def extract_section(text: str, heading: str, cap: int) -> str:
    m = re.search(
        rf"^#+\s*{re.escape(heading)}\s*$", text, re.IGNORECASE | re.MULTILINE
    )
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
    verdict: str,
    notes: str,
) -> str:
    """Render the compressed-markdown body -- byte-identical to legacy."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, int):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    lines += ["", f"# T2-Bare Review — {slug}", "", "## Findings", ""]
    lines += [
        "| ID | Sev | Claim | Cite | SelfConf |",
        "|----|-----|-------|------|----------|",
    ]
    for i, f in enumerate(findings, 1):
        lines.append(
            f"| F-{i:02d} | {f['sev']} | {f['claim']} | {f['cite']} | {f['conf']} |"
        )
    lines += ["", "## Verdict", verdict or "(no verdict returned)"]
    if notes:
        lines += ["", "## Notes", notes]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Recipe class.
# ---------------------------------------------------------------------------


class BareReviewV1:
    """``bare-review-v1`` -- compressed-markdown findings table recipe.

    Implements :class:`superclaude.cli.swarm.recipes.Recipe`. Ports the
    per-reviewer transform from
    :mod:`superclaude.skills.sc-bare-review.scripts.t2_normalize` (legacy
    bash/Python pipeline) into a Wave-2-compatible recipe object.

    Args contract (from ``recipe_args`` threaded through
    :func:`superclaude.cli.swarm.normalize.normalize_wave2`):

    * ``status`` -- the upstream worker status (``"success"`` /
      ``"parse_error"``). Drives §7.4 salvage decision. Defaults to
      ``"success"`` when absent.
    * ``target`` -- absolute path of the reviewed file (frontmatter +
      slug source).
    * ``target_checksum`` -- 12-hex sha256 of the (possibly truncated)
      target body.
    * ``target_truncated`` -- ``True`` when the Wave-0 truncation policy
      fired against the target.
    * ``model_id`` -- transport-supplied model identifier
      (e.g. ``deepseek-v4-pro``).
    * ``model_label`` -- human-facing model label.
    * ``caller_label`` -- optional caller tag (``--label`` flag).
    * ``elapsed_ms`` -- per-worker wall-clock elapsed.
    * ``generated`` -- ISO-8601 UTC timestamp. When absent the recipe
      stamps :func:`iso_now`. Tests (and the parity gate) pin a fixed
      value so the frontmatter is deterministic.

    Returns:
        :class:`NormalizedResult` with the rendered markdown in
        ``text`` and ``salvaged`` set per the §7.4 condition matrix.
    """

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        status = str(args.get("status", "success"))
        target = str(args.get("target", ""))
        checksum = str(args.get("target_checksum", ""))
        truncated = bool(args.get("target_truncated", False))
        model_id = str(args.get("model_id", ""))
        model_label = str(args.get("model_label", ""))
        caller_label = str(args.get("caller_label", "") or "")
        try:
            elapsed_ms = int(args.get("elapsed_ms", 0) or 0)
        except (TypeError, ValueError):
            elapsed_ms = 0
        generated = str(args.get("generated") or iso_now())

        # Empty raw body -- legacy returned proxy_error/parse_error and
        # wrote nothing. The dispatcher's hard-failure short-circuit
        # handles timeout/proxy_error already; if we still see an empty
        # body here the recipe surfaces the recovery failure rather than
        # rendering a frontmatter-only stub.
        if not raw_output or not raw_output.strip():
            return NormalizedResult(text="", salvaged=False, error="empty raw body")

        body = strip_frontmatter(raw_output)
        findings = parse_findings(body)
        verdict = extract_section(body, "Verdict", 300)
        notes = extract_section(body, "Notes", 200)

        salvaged = False
        if status == "parse_error":
            # §7.4 salvage gate: stay failed only when nothing recoverable.
            if not findings and not verdict:
                return NormalizedResult(
                    text="",
                    salvaged=False,
                    error="no findings or verdict",
                )
            salvaged = True
        elif not findings and not verdict:
            verdict = (
                " ".join(body.split())[:300] or "(no structured findings returned)"
            )

        slug = os.path.splitext(os.path.basename(target))[0] if target else ""
        fm: dict[str, Any] = {
            "schema_version": "1.0",
            "tier": "T2",
            "suspect": True,
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
        text = render_markdown(slug, fm, findings, verdict, notes)
        return NormalizedResult(text=text, salvaged=salvaged, error=None)
