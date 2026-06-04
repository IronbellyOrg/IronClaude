"""Structural checkers — 5 deterministic dimension checkers with severity rules.

Implements FR-1 (5 dimension checkers), FR-3 (anchored severity rules).

Each checker is a callable with signature:
    (spec_path: str, roadmap_path: str) -> list[Finding]

Checkers extract structured data from spec and roadmap using spec_parser,
compare deterministically, and produce typed findings with rule-based severity.
No LLM calls. No shared mutable state between checkers (NFR-4).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .convergence import compute_stable_id
from .models import Finding
from .spec_parser import (
    DIMENSION_SECTION_MAP,
    SpecSection,
    ThresholdExpression,
    extract_thresholds,
    parse_document,
)

# ---------- FR-3: Anchored Severity Rules ----------

SEVERITY_RULES: dict[tuple[str, str], str] = {
    # Signatures
    ("signatures", "phantom_id"): "HIGH",
    ("signatures", "id_schema_drift"): "MEDIUM",
    ("signatures", "function_missing"): "HIGH",
    ("signatures", "param_arity_mismatch"): "MEDIUM",
    ("signatures", "param_type_mismatch"): "MEDIUM",
    # Data Models
    ("data_models", "file_missing"): "HIGH",
    ("data_models", "path_prefix_mismatch"): "HIGH",
    ("data_models", "enum_uncovered"): "MEDIUM",
    ("data_models", "field_missing"): "MEDIUM",
    # Gates
    ("gates", "frontmatter_field_missing"): "HIGH",
    ("gates", "step_param_missing"): "MEDIUM",
    ("gates", "ordering_violated"): "MEDIUM",
    ("gates", "semantic_check_missing"): "MEDIUM",
    # CLI
    ("cli", "mode_uncovered"): "MEDIUM",
    ("cli", "default_mismatch"): "MEDIUM",
    # NFRs
    ("nfrs", "threshold_contradicted"): "HIGH",
    ("nfrs", "security_missing"): "HIGH",
    ("nfrs", "dep_direction_violated"): "HIGH",
    ("nfrs", "coverage_mismatch"): "MEDIUM",
    ("nfrs", "dep_rule_missing"): "MEDIUM",
}


def get_severity(dimension: str, mismatch_type: str) -> str:
    """Look up severity for a given dimension + mismatch type.

    Returns severity string. Raises KeyError for unknown combinations
    (forces explicit rule addition, not silent defaults).
    """
    return SEVERITY_RULES[(dimension, mismatch_type)]


# ---------- S2: Finding Routing & Fix-Guidance Templates ----------

# (dimension, mismatch_type) -> "roadmap" | "ambiguous"
# "roadmap"   -> finding is a roadmap defect; files_affected = [roadmap_path]
# "ambiguous" -> could be spec over-claim OR roadmap gap; files_affected =
#                [roadmap_path] AND deviation_class set to "AMBIGUOUS"
MISMATCH_FILE_ROUTING: dict[tuple[str, str], str] = {
    ("signatures", "phantom_id"): "roadmap",
    ("signatures", "function_missing"): "roadmap",
    ("signatures", "param_arity_mismatch"): "roadmap",
    ("signatures", "param_type_mismatch"): "roadmap",
    ("data_models", "file_missing"): "roadmap",
    ("data_models", "path_prefix_mismatch"): "roadmap",
    ("data_models", "enum_uncovered"): "roadmap",
    ("data_models", "field_missing"): "roadmap",
    ("gates", "frontmatter_field_missing"): "roadmap",
    ("gates", "step_param_missing"): "roadmap",
    ("gates", "ordering_violated"): "roadmap",
    ("gates", "semantic_check_missing"): "roadmap",
    ("cli", "mode_uncovered"): "roadmap",
    ("cli", "default_mismatch"): "roadmap",
    ("nfrs", "threshold_contradicted"): "roadmap",
    ("nfrs", "security_missing"): "ambiguous",
    ("nfrs", "dep_direction_violated"): "roadmap",
    ("nfrs", "coverage_mismatch"): "roadmap",
    ("nfrs", "dep_rule_missing"): "roadmap",
}

# Per-mismatch fix_guidance templates. {spec_quote} and {roadmap_quote} are
# interpolated from the corresponding Finding fields.
FIX_GUIDANCE_TEMPLATES: dict[str, str] = {
    "file_missing": (
        "Add a row referencing `{spec_quote}` to the File Manifest section "
        "of the roadmap. Do not modify other rows."
    ),
    "path_prefix_mismatch": (
        "Update the roadmap path to `{spec_quote}` (currently `{roadmap_quote}`). "
        "Edit only the affected manifest row."
    ),
    "enum_uncovered": (
        "Add a reference to enum literal `{spec_quote}` in the relevant "
        "section of the roadmap. Additive edit only."
    ),
    "field_missing": (
        "Reference dataclass field `{spec_quote}` in the roadmap (e.g. in "
        "the Data Models or Implementation section). Additive edit only."
    ),
    "phantom_id": (
        "Remove the reference to `{roadmap_quote}` from the roadmap — "
        "this ID is not defined in the spec."
    ),
    "id_schema_drift": (
        "Spec uses '{spec_quote}' form; roadmap uses '{roadmap_quote}' form. "
        "Either normalize roadmap IDs to the spec form OR rely on the "
        "canonicalized comparator — this finding does not block convergence."
    ),
    "function_missing": (
        "Add a reference to function `{spec_quote}` in the roadmap's "
        "Implementation or Function Signatures section. Additive edit only."
    ),
    "param_arity_mismatch": (
        "Update the roadmap signature to match the spec arity for `{spec_quote}`. "
        "Edit only the affected signature line."
    ),
    "param_type_mismatch": (
        "Update the roadmap parameter type to match the spec for `{spec_quote}`. "
        "Edit only the affected signature line."
    ),
    "frontmatter_field_missing": (
        "Add the frontmatter field `{spec_quote}` to the roadmap's YAML "
        "frontmatter. Do not modify other fields."
    ),
    "step_param_missing": (
        "Add parameter `{spec_quote}` to the corresponding Step(...) call "
        "in the roadmap's gates section."
    ),
    "ordering_violated": (
        "Re-order the roadmap step sequence to match the spec ordering "
        "near `{spec_quote}`. Edit only the affected ordering."
    ),
    "semantic_check_missing": (
        "Add a semantic check covering `{spec_quote}` to the roadmap's "
        "validation section. Additive edit only."
    ),
    "mode_uncovered": (
        "Add CLI mode `{spec_quote}` to the roadmap's CLI surface section. "
        "Additive edit only."
    ),
    "default_mismatch": (
        "Update the CLI default to match the spec value `{spec_quote}` "
        "(currently `{roadmap_quote}`)."
    ),
    "threshold_contradicted": (
        "Update the roadmap threshold to match the spec value `{spec_quote}` "
        "(currently `{roadmap_quote}`)."
    ),
    "security_missing": (
        "Add an NFR line covering `{spec_quote}` to the Non-Functional "
        "Requirements section of the roadmap, OR if the primitive is "
        "out-of-scope, document the deviation in extraction.md (do NOT "
        "modify the spec file)."
    ),
    "dep_direction_violated": (
        "Reverse the dependency arrow involving `{spec_quote}` in the "
        "roadmap to match the spec direction."
    ),
    "coverage_mismatch": (
        "Strengthen the roadmap's coverage statement near `{spec_quote}` "
        "to meet the spec requirement."
    ),
    "dep_rule_missing": (
        "Add the dependency rule `{spec_quote}` to the roadmap's "
        "dependencies section. Additive edit only."
    ),
}


def _route_findings(findings: list[Finding], roadmap_path: str) -> list[Finding]:
    """Post-process findings: set files_affected via routing table and
    populate fix_guidance from templates.

    Mutates and returns the findings list.

    - Lookups for `(dimension, rule_id)` resolve to "roadmap" or "ambiguous".
    - "roadmap" sets files_affected=[roadmap_path].
    - "ambiguous" sets files_affected=[roadmap_path] AND
      deviation_class="AMBIGUOUS".
    - Findings already carrying a non-empty files_affected are left alone.
    - Generic "Address {mismatch_type} in {dimension} dimension" boilerplate
      is replaced with a per-mismatch action template when one exists.
    """
    if not roadmap_path:
        return findings
    for f in findings:
        if not f.files_affected:
            target = MISMATCH_FILE_ROUTING.get((f.dimension, f.rule_id))
            if target == "roadmap":
                f.files_affected = [roadmap_path]
            elif target == "ambiguous":
                f.files_affected = [roadmap_path]
                if f.deviation_class == "UNCLASSIFIED":
                    f.deviation_class = "AMBIGUOUS"
        template = FIX_GUIDANCE_TEMPLATES.get(f.rule_id)
        if template and f.fix_guidance.startswith("Address "):
            try:
                f.fix_guidance = template.format(
                    spec_quote=f.spec_quote or "",
                    roadmap_quote=f.roadmap_quote or "",
                )
            except (KeyError, IndexError):
                pass  # leave generic guidance if template interpolation fails
    return findings


# ---------- Supporting Dataclasses ----------


@dataclass
class RegressionResult:
    """Result of a regression check between consecutive runs.

    Produced by handle_regression() when structural HIGH count increases.
    """

    regressed: bool
    previous_high_count: int
    current_high_count: int
    new_findings: list[str] = field(default_factory=list)  # stable_ids
    action: str = ""  # e.g. "HALT", "RETRY_WITH_SNAPSHOT"
    message: str = ""


@dataclass
class RemediationPatch:
    """A single remediation edit applied to a roadmap file.

    Tracks what was changed, where, and whether it was rolled back.
    """

    file_path: str
    original_content: str
    patched_content: str
    finding_id: str  # stable_id of the finding this patch addresses
    applied: bool = False
    rolled_back: bool = False


# ---------- Helpers ----------

_FINDING_COUNTER: int = 0


def _make_finding(
    dimension: str,
    mismatch_type: str,
    description: str,
    location: str,
    spec_quote: str,
    roadmap_quote: str,
    severity_override: str | None = None,
) -> Finding:
    """Create a Finding with rule-based severity and stable ID.

    If ``severity_override`` is provided, it takes precedence over the
    SEVERITY_RULES table entry. This enables S5's context-aware NFR severity
    demotion without disturbing the canonical rule table.
    """
    severity = severity_override or get_severity(dimension, mismatch_type)
    stable_id = compute_stable_id(dimension, mismatch_type, location, mismatch_type)
    return Finding(
        id=f"{dimension}-{mismatch_type}-{stable_id[:8]}",
        severity=severity,
        dimension=dimension,
        description=description,
        location=location,
        evidence=spec_quote,
        fix_guidance=f"Address {mismatch_type} in {dimension} dimension",
        status="ACTIVE",
        source_layer="structural",
        rule_id=mismatch_type,
        spec_quote=spec_quote,
        roadmap_quote=roadmap_quote,
        stable_id=stable_id,
    )


def _canonicalize_requirement_id(family: str, raw: str) -> str:
    """Canonicalize a requirement ID to enable drift-tolerant comparison.

    Mirrors the precedent in integration_contracts.py:445 (_canonicalize_identifiers,
    KNOWLEDGE.md 2026-05-25 "Fix B Merged"). Strips leading zeros within the
    numeric tail while preserving family prefix and any sub-ID structure.

    Examples:
        D01     -> D1
        D-01    -> D1
        FR-7    -> FR-7   (idempotent)
        FR-7.1  -> FR-7.1 (sub-ID preserved)
        NFR-02  -> NFR-2

    Note: this helper is intentionally a pure (family, raw) -> str transformation
    with no shared state. A future refactor MAY relocate this helper into
    spec_parser.extract_requirement_ids so canonical IDs flow downstream by
    construction (refactoring-expert framing in fix-3 of the adversarial debate).
    For now it lives in the checker because relocation would alter the
    Finding.roadmap_quote semantics at structural_checkers.py:389.

    Note (forward-looking): this fix demotes "canonical form matches but surface
    form differs" findings to MEDIUM with rule_id="id_schema_drift". This is a
    specific instance of a broader "fixability" concept (fix-2 framing in the
    adversarial debate): findings should declare whether they are reachable by
    an additive roadmap edit. The full fixability classifier is deferred pending
    calibration of the CLASS_DRIFT count threshold (INV-003 of the invariant probe).
    """
    import re

    # MD family: milestone-prefixed deliverable IDs (e.g. "M1-D01" -> "M1-D1").
    # Preserve the M{n}- prefix; canonicalize only the trailing D{nn} portion (strip
    # leading zeros on the deliverable index) so milestone-distinct deliverables
    # (M1-D01 vs M2-D01) resolve to DISTINCT canonical forms rather than collapsing
    # to a single bare-D key. Ported from PR #111 (861047c2) design D2; see also
    # TASK-RF-20260531-044100 design D2. The local re.match shape is a
    # canonicalization helper, NOT a duplicate of any contracts.ID_PATTERNS body
    # (arch-lint Rule 2 stays green).
    if family == "MD":
        md_match = re.match(r"^(M\d+-D)-?0*(\d+)$", raw)
        if md_match:
            md_prefix, md_num = md_match.groups()
            return f"{md_prefix}{md_num}"
        return raw

    # Match: family prefix (letters), optional sep (- or _), leading zeros, digit run, optional rest.
    # Multi-letter prefix families (FR, NFR, SC) use a hyphen in canonical form;
    # single-letter prefix families (D, G) drop the separator entirely.
    match = re.match(r"^([A-Z]+)([-_]?)0*(\d+)(.*)$", raw)
    if not match:
        return raw
    prefix, _input_sep, num, rest = match.groups()
    sep = "-" if len(prefix) > 1 else ""
    return f"{prefix}{sep}{num}{rest}"


# ---------- S5: Context-Aware NFR Severity ----------

# Heading-path tokens that signal a hard-requirement section. NFR soft findings
# (security_missing, threshold no-match) keep HIGH severity when emitted from
# a section whose heading_path contains any of these. Otherwise they demote to
# MEDIUM so they no longer block the convergence gate (which is HIGH-only).
_STRONG_NFR_TOKENS: tuple[str, ...] = (
    "security",
    "critical",
    "must",
    "shall",
    "required",
    "p0",
    "nfr-",
    "compliance",
    "encryption",
    "audit",
)


def _classify_nfr_severity(
    dimension: str,
    mismatch_type: str,
    heading_path: str,
    heading: str,
) -> str:
    """Return HIGH if the originating section signals a hard requirement,
    MEDIUM if the keyword appeared in incidental prose.

    Only applies to the two soft NFR types (``security_missing`` and the
    no-match arm of ``threshold_contradicted``). All other findings continue
    to use SEVERITY_RULES via get_severity.
    """
    if mismatch_type not in ("security_missing", "threshold_contradicted"):
        return get_severity(dimension, mismatch_type)
    haystack = f"{heading_path}/{heading}".lower()
    if any(tok in haystack for tok in _STRONG_NFR_TOKENS):
        return "HIGH"
    return "MEDIUM"


def _get_sections_for_dimension(
    dimension: str, sections: list[SpecSection]
) -> list[SpecSection]:
    """Return sections relevant to a given dimension per DIMENSION_SECTION_MAP."""
    patterns = DIMENSION_SECTION_MAP.get(dimension, [])
    result: list[SpecSection] = []
    for section in sections:
        for pattern in patterns:
            if pattern in section.heading_path or pattern in section.heading:
                result.append(section)
                break
    return result


def _section_text(sections: list[SpecSection]) -> str:
    """Concatenate section content into a single text blob."""
    return "\n".join(s.content for s in sections)


# Anchor for the Explicit non-references allowlist parser. The roadmap may declare
# certain bare-D or bare-G tokens as roadmap-internal-only sequences that MUST NOT be
# resolved against the spec namespace. Ported from PR #111 (861047c2) design D3;
# see also TASK-RF-20260531-044100 design D3.
_EXPLICIT_NON_REFS_ANCHOR_RE = re.compile(
    r"\*\*Explicit non-references[^*]*\*\*([^\n]*)", re.IGNORECASE
)
# Tokens we accept into the allowlist are bare single-letter-prefix forms (D{nn}, G{nn})
# that the roadmap author has marked as roadmap-internal sequences. Multi-letter spec
# families (FR-*, NFR-*, etc.) are never silenced by this allowlist — those references
# in the same anchor line are counter-examples, not allowlist entries.
_EXPLICIT_NON_REFS_TOKEN_RE = re.compile(r"`([DG]-?\d+)`")
# The post-list boundary phrase. After this marker the line transitions into a
# description of what the listed tokens are NOT (the spec namespaces). Any tokens
# after this phrase are explicitly NOT allowlist entries.
_EXPLICIT_NON_REFS_BOUNDARY_RE = re.compile(
    r"\s+are\s+\*\*roadmap-internal", re.IGNORECASE
)


def _parse_explicit_non_references(roadmap_path: str) -> set[str]:
    """Parse the "Explicit non-references (do not resolve against spec)" allowlist.

    Returns a set of token strings (e.g. {"D01", "D02", ..., "D54"}) that the
    roadmap author has marked as roadmap-internal-only sequences. These tokens
    must be exempted from spec-namespace phantom_id and id_schema_drift findings.

    The canonical anchor is a line of the form:
        **Explicit non-references (do not resolve against spec):** the tokens `D01`, `D02`, ... are **roadmap-internal deliverable sequence numbers** ONLY when paired with ...

    Tokens are extracted from backtick-delimited literals on the same line as the
    anchor, between the bold anchor and the boundary phrase "are **roadmap-internal"
    (which signals the transition to descriptive prose listing counter-examples
    rather than allowlist entries). The token family is restricted to single-letter
    D/G prefixes because those are the only families the allowlist semantic exempts;
    multi-letter spec families (FR-*, NFR-*) cited as counter-examples must never
    be silenced.

    If the anchor is absent (legacy roadmaps without the convention), the function
    returns an empty set and the validator behaves as before.
    """
    try:
        text = Path(roadmap_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()

    allowlist: set[str] = set()
    for anchor_match in _EXPLICIT_NON_REFS_ANCHOR_RE.finditer(text):
        # The captured group is the remainder of the line after the bold anchor.
        tail = anchor_match.group(1)
        # Truncate at the boundary phrase so we don't accidentally allowlist
        # counter-example tokens (FR-*, NFR-*, G1..G8, T1..T11) cited after the list.
        boundary_match = _EXPLICIT_NON_REFS_BOUNDARY_RE.search(tail)
        if boundary_match:
            tail = tail[: boundary_match.start()]
        for tok_match in _EXPLICIT_NON_REFS_TOKEN_RE.finditer(tail):
            allowlist.add(tok_match.group(1))
    return allowlist


# ---------- FR-1: Five Structural Checkers ----------

# Type alias for checker callable
CheckerCallable = Callable[[str, str], list[Finding]]


def check_signatures(spec_path: str, roadmap_path: str) -> list[Finding]:
    """Signatures checker: compares function signatures and requirement IDs.

    Machine keys: phantom_id, function_missing, param_arity_mismatch, param_type_mismatch
    """
    spec_text = Path(spec_path).read_text(encoding="utf-8")
    roadmap_text = Path(roadmap_path).read_text(encoding="utf-8")

    spec_parsed = parse_document(spec_text)
    roadmap_parsed = parse_document(roadmap_text)

    # Explicit non-references allowlist: bare-D / bare-G tokens the roadmap author
    # has marked as roadmap-internal-only sequences (e.g. D01..D54 under M{n}- prefixes).
    # Ported from PR #111 (861047c2) design D3; see also TASK-RF-20260531-044100 design D3.
    non_ref_allowlist: set[str] = _parse_explicit_non_references(roadmap_path)

    # Get dimension-relevant sections
    roadmap_full_text = roadmap_text.lower()

    findings: list[Finding] = []

    # --- Phantom ID check: roadmap references IDs not in spec ---
    # Build canonical-form -> raw-form maps for both sides. The canonicalizer
    # at structural_checkers._canonicalize_requirement_id collapses zero-padded
    # and separator-variant forms (D01, D-01 -> D1) so surface-form drift no
    # longer trips the raw set-difference comparator. Mirrors the precedent at
    # integration_contracts.py:445.
    spec_canon: dict[str, str] = {}
    for family, ids in spec_parsed.requirement_ids.items():
        for raw in ids:
            canon = _canonicalize_requirement_id(family, raw)
            # Preserve first-seen raw form on collision (deterministic via sorted iteration)
            if canon not in spec_canon:
                spec_canon[canon] = raw

    # We also track the source family of each canonical roadmap ID so the allowlist
    # check (D3) can be scoped to bare-D / bare-G families only — milestone-prefixed
    # MD-family tokens are handled by their own allowlist branch below.
    roadmap_canon: dict[str, str] = {}
    roadmap_canon_family: dict[str, str] = {}
    for family, ids in roadmap_parsed.requirement_ids.items():
        for raw in ids:
            canon = _canonicalize_requirement_id(family, raw)
            if canon not in roadmap_canon:
                roadmap_canon[canon] = raw
                roadmap_canon_family[canon] = family

    drift_findings: list[Finding] = []  # MEDIUM id_schema_drift
    phantom_findings: list[Finding] = []  # HIGH phantom_id (existing behavior)
    for canon in sorted(roadmap_canon):
        raw = roadmap_canon[canon]
        family = roadmap_canon_family[canon]
        # D3 allowlist: skip findings for bare-D/bare-G tokens explicitly marked as
        # roadmap-internal-only by the roadmap's "Explicit non-references" annotation.
        if family in ("D", "G") and raw in non_ref_allowlist:
            continue
        # D3 allowlist extension: MD-family tokens (M{n}-D{nn}) are the canonical
        # roadmap-internal form of the bare-D sequences. Per the canonical roadmap
        # annotation ("the tokens D01..D54 are roadmap-internal deliverable sequence
        # numbers ONLY when paired with their milestone prefix"), the milestone-
        # prefixed forms are equally roadmap-internal and must be exempted from
        # spec-namespace resolution when their D-suffix is in the allowlist.
        if family == "MD":
            md_match = re.match(r"^M\d+-(D-?\d+)$", raw)
            if md_match and md_match.group(1) in non_ref_allowlist:
                continue
        if canon in spec_canon:
            if raw == spec_canon[canon]:
                continue  # exact match — no finding
            drift_findings.append(
                _make_finding(
                    dimension="signatures",
                    mismatch_type="id_schema_drift",
                    description=(
                        f"Roadmap ID '{raw}' canonicalizes to spec ID "
                        f"'{spec_canon[canon]}' (surface form differs). "
                        f"Does not block convergence."
                    ),
                    location=f"roadmap:{raw}",
                    spec_quote=spec_canon[canon],
                    roadmap_quote=raw,
                )
            )
        else:
            phantom_findings.append(
                _make_finding(
                    dimension="signatures",
                    mismatch_type="phantom_id",
                    description=f"Roadmap references ID '{raw}' not found in spec",
                    location=f"roadmap:{raw}",
                    spec_quote="[MISSING]",
                    roadmap_quote=raw,
                )
            )
    findings.extend(phantom_findings)
    findings.extend(drift_findings)

    # --- Function missing check: spec functions not referenced in roadmap ---
    spec_sigs = spec_parsed.function_signatures
    for sig in spec_sigs:
        if sig.name.lower() not in roadmap_full_text:
            findings.append(
                _make_finding(
                    dimension="signatures",
                    mismatch_type="function_missing",
                    description=f"Function '{sig.name}' defined in spec not found in roadmap",
                    location=f"spec:function:{sig.name}",
                    spec_quote=f"def {sig.name}({sig.params})"
                    + (f" -> {sig.return_type}" if sig.return_type else ""),
                    roadmap_quote="[MISSING]",
                )
            )

    # --- Param arity mismatch: functions found in both but with different param counts ---
    roadmap_sigs = roadmap_parsed.function_signatures
    roadmap_sig_map = {s.name: s for s in roadmap_sigs}
    for sig in spec_sigs:
        if sig.name in roadmap_sig_map:
            rm_sig = roadmap_sig_map[sig.name]
            spec_params = (
                [p.strip() for p in sig.params.split(",") if p.strip()]
                if sig.params.strip()
                else []
            )
            rm_params = (
                [p.strip() for p in rm_sig.params.split(",") if p.strip()]
                if rm_sig.params.strip()
                else []
            )
            if len(spec_params) != len(rm_params):
                findings.append(
                    _make_finding(
                        dimension="signatures",
                        mismatch_type="param_arity_mismatch",
                        description=f"Function '{sig.name}' has {len(spec_params)} params in spec but {len(rm_params)} in roadmap",
                        location=f"spec:function:{sig.name}",
                        spec_quote=f"def {sig.name}({sig.params})",
                        roadmap_quote=f"def {rm_sig.name}({rm_sig.params})",
                    )
                )
            else:
                # Check param types where available
                for i, (sp, rp) in enumerate(zip(spec_params, rm_params)):
                    # Extract type annotations if present
                    sp_type = sp.split(":")[-1].strip() if ":" in sp else ""
                    rp_type = rp.split(":")[-1].strip() if ":" in rp else ""
                    if sp_type and rp_type and sp_type != rp_type:
                        findings.append(
                            _make_finding(
                                dimension="signatures",
                                mismatch_type="param_type_mismatch",
                                description=f"Function '{sig.name}' param {i} type differs: spec='{sp_type}' vs roadmap='{rp_type}'",
                                location=f"spec:function:{sig.name}:param:{i}",
                                spec_quote=sp,
                                roadmap_quote=rp,
                            )
                        )

    return _route_findings(findings, roadmap_path)


def check_data_models(spec_path: str, roadmap_path: str) -> list[Finding]:
    """Data Models checker: compares file manifests, dataclass fields, enum literals.

    Machine keys: file_missing, path_prefix_mismatch, enum_uncovered, field_missing
    """
    spec_text = Path(spec_path).read_text(encoding="utf-8")
    roadmap_text = Path(roadmap_path).read_text(encoding="utf-8")

    spec_parsed = parse_document(spec_text)
    roadmap_parsed = parse_document(roadmap_text)

    roadmap_full_text = roadmap_text.lower()
    roadmap_file_paths = set(roadmap_parsed.file_paths)

    findings: list[Finding] = []

    # --- File missing check: spec file paths not in roadmap ---
    spec_file_paths = spec_parsed.file_paths
    for fpath in spec_file_paths:
        fname = Path(fpath).name.lower()
        # Check exact match or filename match in roadmap
        if fpath not in roadmap_file_paths and fname not in roadmap_full_text:
            findings.append(
                _make_finding(
                    dimension="data_models",
                    mismatch_type="file_missing",
                    description=f"File '{fpath}' in spec manifest not found in roadmap",
                    location=f"spec:file:{fpath}",
                    spec_quote=fpath,
                    roadmap_quote="[MISSING]",
                )
            )

    # --- Path prefix mismatch: same filename but different prefix ---
    spec_path_names = {Path(p).name: p for p in spec_file_paths}
    roadmap_path_names = {Path(p).name: p for p in roadmap_file_paths}
    for fname, spec_fpath in spec_path_names.items():
        if fname in roadmap_path_names:
            rm_fpath = roadmap_path_names[fname]
            if spec_fpath != rm_fpath:
                # Different prefix
                findings.append(
                    _make_finding(
                        dimension="data_models",
                        mismatch_type="path_prefix_mismatch",
                        description=f"File '{fname}' has different path: spec='{spec_fpath}' vs roadmap='{rm_fpath}'",
                        location=f"spec:file:{spec_fpath}",
                        spec_quote=spec_fpath,
                        roadmap_quote=rm_fpath,
                    )
                )

    # --- Enum uncovered: Literal enum values in spec not in roadmap ---
    spec_literals = spec_parsed.literal_values
    for literal_group in spec_literals:
        for val in literal_group:
            if val.lower() not in roadmap_full_text:
                findings.append(
                    _make_finding(
                        dimension="data_models",
                        mismatch_type="enum_uncovered",
                        description=f"Enum literal '{val}' from spec not covered in roadmap",
                        location=f"spec:literal:{val}",
                        spec_quote=val,
                        roadmap_quote="[MISSING]",
                    )
                )

    # --- Field missing: dataclass fields in spec code blocks not in roadmap ---
    # Extract field names from spec code blocks (look for field definitions)
    import re

    field_re = re.compile(r"^\s+(\w+)\s*:", re.MULTILINE)
    for block in spec_parsed.code_blocks:
        if block.language and block.language.lower() not in ("python", "py", ""):
            continue
        # Only look at blocks that look like dataclass definitions
        if "class " not in block.content and "@dataclass" not in block.content:
            continue
        for match in field_re.finditer(block.content):
            field_name = match.group(1)
            # Skip dunder and private
            if field_name.startswith("_") or field_name in (
                "self",
                "cls",
                "return",
                "class",
                "def",
                "if",
                "else",
                "for",
                "while",
                "import",
                "from",
                "try",
                "except",
            ):
                continue
            if field_name.lower() not in roadmap_full_text:
                findings.append(
                    _make_finding(
                        dimension="data_models",
                        mismatch_type="field_missing",
                        description=f"Dataclass field '{field_name}' from spec not referenced in roadmap",
                        location=f"spec:field:{field_name}",
                        spec_quote=field_name,
                        roadmap_quote="[MISSING]",
                    )
                )

    return _route_findings(findings, roadmap_path)


def check_gates(spec_path: str, roadmap_path: str) -> list[Finding]:
    """Gates checker: verifies gate definitions, thresholds, step ordering.

    Machine keys: frontmatter_field_missing, step_param_missing, ordering_violated, semantic_check_missing
    """
    import re

    spec_text = Path(spec_path).read_text(encoding="utf-8")
    roadmap_text = Path(roadmap_path).read_text(encoding="utf-8")

    spec_parsed = parse_document(spec_text)
    roadmap_parsed = parse_document(roadmap_text)

    spec_sections = _get_sections_for_dimension("gates", spec_parsed.sections)
    roadmap_full_text = roadmap_text.lower()

    findings: list[Finding] = []

    # --- Frontmatter field missing: required frontmatter fields in spec not in roadmap ---
    # Look for frontmatter field references in gate-related spec sections
    spec_gate_text = _section_text(spec_sections)
    frontmatter_field_re = re.compile(
        r"`(\w+)`\s*(?:field|frontmatter|required)", re.IGNORECASE
    )
    for match in frontmatter_field_re.finditer(spec_gate_text):
        field_name = match.group(1)
        if field_name.lower() not in roadmap_full_text:
            findings.append(
                _make_finding(
                    dimension="gates",
                    mismatch_type="frontmatter_field_missing",
                    description=f"Required frontmatter field '{field_name}' not found in roadmap",
                    location=f"spec:gate:frontmatter:{field_name}",
                    spec_quote=match.group(0),
                    roadmap_quote="[MISSING]",
                )
            )

    # --- Step param missing: Step(...) parameters in spec not in roadmap ---
    step_param_re = re.compile(r"Step\s*\([^)]*\b(\w+)\s*=", re.IGNORECASE)
    for match in step_param_re.finditer(spec_gate_text):
        param_name = match.group(1)
        if param_name.lower() not in roadmap_full_text:
            findings.append(
                _make_finding(
                    dimension="gates",
                    mismatch_type="step_param_missing",
                    description=f"Step parameter '{param_name}' from spec not found in roadmap",
                    location=f"spec:gate:step_param:{param_name}",
                    spec_quote=match.group(0),
                    roadmap_quote="[MISSING]",
                )
            )

    # --- Ordering violated: check gate ordering constraints ---
    # Extract ordered gate/step names from spec
    order_re = re.compile(r"(?:step|gate|phase)\s*(\d+)", re.IGNORECASE)
    spec_order = [int(m.group(1)) for m in order_re.finditer(spec_gate_text)]
    roadmap_gate_sections = _get_sections_for_dimension(
        "gates", roadmap_parsed.sections
    )
    roadmap_gate_text = _section_text(roadmap_gate_sections)
    roadmap_order = [int(m.group(1)) for m in order_re.finditer(roadmap_gate_text)]

    if spec_order and roadmap_order:
        # Check if roadmap preserves spec ordering
        spec_sorted = sorted(set(spec_order))
        roadmap_seen = []
        for num in roadmap_order:
            if num in spec_sorted and num not in roadmap_seen:
                roadmap_seen.append(num)
        if roadmap_seen != sorted(roadmap_seen):
            findings.append(
                _make_finding(
                    dimension="gates",
                    mismatch_type="ordering_violated",
                    description="Gate/step ordering in roadmap does not match spec ordering",
                    location="spec:gate:ordering",
                    spec_quote=str(spec_sorted),
                    roadmap_quote=str(roadmap_seen),
                )
            )

    # --- Semantic check missing: named semantic checks in spec not mapped in roadmap ---
    semantic_check_re = re.compile(
        r'semantic[_ ]check[s]?\s*[:\-]?\s*[`"]?(\w+)', re.IGNORECASE
    )
    for match in semantic_check_re.finditer(spec_gate_text):
        check_name = match.group(1)
        if check_name.lower() not in roadmap_full_text:
            findings.append(
                _make_finding(
                    dimension="gates",
                    mismatch_type="semantic_check_missing",
                    description=f"Semantic check '{check_name}' from spec not mapped in roadmap",
                    location=f"spec:gate:semantic_check:{check_name}",
                    spec_quote=match.group(0),
                    roadmap_quote="[MISSING]",
                )
            )

    return _route_findings(findings, roadmap_path)


def check_cli(spec_path: str, roadmap_path: str) -> list[Finding]:
    """CLI Options checker: compares Click options, flags, defaults.

    Machine keys: mode_uncovered, default_mismatch
    """
    import re

    spec_text = Path(spec_path).read_text(encoding="utf-8")
    roadmap_text = Path(roadmap_path).read_text(encoding="utf-8")

    spec_parsed = parse_document(spec_text)
    roadmap_parsed = parse_document(roadmap_text)

    spec_sections = _get_sections_for_dimension("cli", spec_parsed.sections)
    roadmap_full_text = roadmap_text.lower()

    findings: list[Finding] = []

    spec_cli_text = _section_text(spec_sections)

    # --- Mode uncovered: config modes from spec not covered in roadmap ---
    # Extract modes from Literal[...] values in CLI-related sections
    for literal_group in spec_parsed.literal_values:
        for val in literal_group:
            if val.lower() not in roadmap_full_text:
                findings.append(
                    _make_finding(
                        dimension="cli",
                        mismatch_type="mode_uncovered",
                        description=f"Config mode '{val}' from spec not covered in roadmap",
                        location=f"spec:cli:mode:{val}",
                        spec_quote=val,
                        roadmap_quote="[MISSING]",
                    )
                )

    # --- Also check CLI flags/options from tables ---
    # Look for option/flag definitions in CLI section tables
    option_re = re.compile(r"`--?([\w-]+)`", re.IGNORECASE)
    for match in option_re.finditer(spec_cli_text):
        option_name = match.group(1)
        if option_name.lower() not in roadmap_full_text:
            findings.append(
                _make_finding(
                    dimension="cli",
                    mismatch_type="mode_uncovered",
                    description=f"CLI option '--{option_name}' from spec not covered in roadmap",
                    location=f"spec:cli:option:{option_name}",
                    spec_quote=match.group(0),
                    roadmap_quote="[MISSING]",
                )
            )

    # --- Default mismatch: check defaults in spec vs roadmap ---
    # Extract default values from spec (pattern: `default: value` or `default=value`)
    default_re = re.compile(r'default\s*[=:]\s*[`"\']?(\S+?)[`"\']?\s', re.IGNORECASE)
    spec_defaults: dict[str, str] = {}
    for match in default_re.finditer(spec_cli_text):
        val = match.group(1).strip("`\"'")
        # Use position as key since we don't always know the option name
        spec_defaults[val] = match.group(0)

    roadmap_cli_sections = _get_sections_for_dimension("cli", roadmap_parsed.sections)
    roadmap_cli_text = _section_text(roadmap_cli_sections)
    for val, context in spec_defaults.items():
        # Check if the default value appears differently in roadmap
        roadmap_default_re = re.compile(
            r'default\s*[=:]\s*[`"\']?(\S+?)[`"\']?\s', re.IGNORECASE
        )
        for rm_match in roadmap_default_re.finditer(roadmap_cli_text):
            rm_val = rm_match.group(1).strip("`\"'")
            # Only flag if both reference the same option context but different values
            if rm_val != val and val.lower() in roadmap_cli_text.lower():
                findings.append(
                    _make_finding(
                        dimension="cli",
                        mismatch_type="default_mismatch",
                        description=f"Default value mismatch: spec='{val}' vs roadmap='{rm_val}'",
                        location=f"spec:cli:default:{val}",
                        spec_quote=context,
                        roadmap_quote=rm_match.group(0),
                    )
                )

    return _route_findings(findings, roadmap_path)


def check_nfrs(spec_path: str, roadmap_path: str) -> list[Finding]:
    """NFRs checker: verifies numeric thresholds, security primitives, dependency rules.

    Machine keys: threshold_contradicted, security_missing, dep_direction_violated,
                  coverage_mismatch, dep_rule_missing
    """
    import re

    spec_text = Path(spec_path).read_text(encoding="utf-8")
    roadmap_text = Path(roadmap_path).read_text(encoding="utf-8")

    spec_parsed = parse_document(spec_text)
    parse_document(roadmap_text)

    spec_sections = _get_sections_for_dimension("nfrs", spec_parsed.sections)
    roadmap_full_text = roadmap_text.lower()

    findings: list[Finding] = []

    spec_nfr_text = _section_text(spec_sections)

    # --- Threshold contradicted (TRUE contradictions): scanned globally over
    # the joined NFR text because contradictions are not section-localized.
    # The no-match arm is moved into the per-section loop below so severity
    # can be classified by heading context (S5).
    spec_thresholds = extract_thresholds(spec_nfr_text)
    roadmap_thresholds = extract_thresholds(roadmap_text)

    # Build roadmap threshold lookup by raw value
    roadmap_threshold_values: dict[str, ThresholdExpression] = {}
    for t in roadmap_thresholds:
        roadmap_threshold_values[t.value] = t

    for spec_t in spec_thresholds:
        if spec_t.value in roadmap_threshold_values:
            rm_t = roadmap_threshold_values[spec_t.value]
            if spec_t.operator != rm_t.operator:
                findings.append(
                    _make_finding(
                        dimension="nfrs",
                        mismatch_type="threshold_contradicted",
                        description=f"Threshold '{spec_t.raw}' contradicted by '{rm_t.raw}' in roadmap",
                        location=f"spec:nfr:threshold:{spec_t.raw}",
                        spec_quote=spec_t.raw,
                        roadmap_quote=rm_t.raw,
                    )
                )

    # --- Per-section iteration: emit security_missing and threshold no-match
    # findings with severity classified by the originating section heading.
    # Deterministic order: sort sections by heading_path, then sort terms.
    security_keywords = [
        "encryption",
        "encrypted",
        "tls",
        "ssl",
        "hash",
        "hmac",
        "auth",
        "authentication",
        "authorization",
        "oauth",
        "jwt",
        "rbac",
        "acl",
        "sanitize",
        "sanitization",
        "escape",
        "csrf",
        "xss",
        "injection",
        "secrets",
        "credential",
    ]
    security_re = re.compile(
        r"\b(" + "|".join(security_keywords) + r")\b", re.IGNORECASE
    )

    seen_security_terms: set[str] = set()
    seen_threshold_raws: set[str] = set()
    for section in sorted(spec_sections, key=lambda s: s.heading_path):
        # Security primitives
        for m in security_re.finditer(section.content):
            term = m.group(1).lower()
            if term in seen_security_terms:
                continue
            seen_security_terms.add(term)
            if term not in roadmap_full_text:
                severity = _classify_nfr_severity(
                    dimension="nfrs",
                    mismatch_type="security_missing",
                    heading_path=section.heading_path,
                    heading=section.heading,
                )
                findings.append(
                    _make_finding(
                        dimension="nfrs",
                        mismatch_type="security_missing",
                        description=f"Security primitive '{term}' from spec NFRs not addressed in roadmap",
                        location=f"spec:nfr:security:{term}",
                        spec_quote=term,
                        roadmap_quote="[MISSING]",
                        severity_override=severity,
                    )
                )
        # Threshold no-match arm (per-section so heading context is preserved)
        section_thresholds = extract_thresholds(section.content)
        for spec_t in section_thresholds:
            if spec_t.value in roadmap_threshold_values:
                continue  # handled by the contradiction loop above
            if spec_t.raw in seen_threshold_raws:
                continue
            seen_threshold_raws.add(spec_t.raw)
            if (
                spec_t.raw.lower() in roadmap_full_text
                or spec_t.value in roadmap_full_text
            ):
                continue
            severity = _classify_nfr_severity(
                dimension="nfrs",
                mismatch_type="threshold_contradicted",
                heading_path=section.heading_path,
                heading=section.heading,
            )
            findings.append(
                _make_finding(
                    dimension="nfrs",
                    mismatch_type="threshold_contradicted",
                    description=f"NFR threshold '{spec_t.raw}' not addressed in roadmap",
                    location=f"spec:nfr:threshold:{spec_t.raw}",
                    spec_quote=spec_t.raw,
                    roadmap_quote="[MISSING]",
                    severity_override=severity,
                )
            )

    # --- Dependency direction violated: dependency rules in spec ---
    dep_re = re.compile(
        r"(\w[\w./]+)\s*(?:→|->|depends\s+on|imports?)\s*(\w[\w./]+)",
        re.IGNORECASE,
    )
    spec_deps = [(m.group(1), m.group(2)) for m in dep_re.finditer(spec_nfr_text)]
    roadmap_deps = [(m.group(1), m.group(2)) for m in dep_re.finditer(roadmap_text)]

    roadmap_dep_set = {(a.lower(), b.lower()) for a, b in roadmap_deps}
    for src, tgt in spec_deps:
        # Check if roadmap has the reverse direction
        if (tgt.lower(), src.lower()) in roadmap_dep_set:
            findings.append(
                _make_finding(
                    dimension="nfrs",
                    mismatch_type="dep_direction_violated",
                    description=f"Dependency direction '{src} → {tgt}' reversed in roadmap",
                    location=f"spec:nfr:dep:{src}->{tgt}",
                    spec_quote=f"{src} → {tgt}",
                    roadmap_quote=f"{tgt} → {src}",
                )
            )

    # --- Coverage mismatch: coverage thresholds ---
    coverage_re = re.compile(r"coverage\s*[><=]+\s*(\d+)%", re.IGNORECASE)
    spec_coverage = coverage_re.findall(spec_nfr_text)
    roadmap_coverage = coverage_re.findall(roadmap_text)
    if spec_coverage and roadmap_coverage:
        for sc in spec_coverage:
            for rc in roadmap_coverage:
                if int(rc) < int(sc):
                    findings.append(
                        _make_finding(
                            dimension="nfrs",
                            mismatch_type="coverage_mismatch",
                            description=f"Coverage threshold {sc}% in spec but {rc}% in roadmap",
                            location=f"spec:nfr:coverage:{sc}%",
                            spec_quote=f"coverage >= {sc}%",
                            roadmap_quote=f"coverage >= {rc}%",
                        )
                    )

    # --- Dep rule missing: dependency rules from spec not addressed ---
    dep_rule_re = re.compile(
        r"(?:must\s+not|shall\s+not|cannot|must\s+not)\s+(?:import|depend|reference)\b",
        re.IGNORECASE,
    )
    for match in dep_rule_re.finditer(spec_nfr_text):
        rule_text = match.group(0)
        # Get surrounding context
        start = max(0, match.start() - 50)
        end = min(len(spec_nfr_text), match.end() + 50)
        context = spec_nfr_text[start:end].strip()
        if rule_text.lower() not in roadmap_full_text:
            findings.append(
                _make_finding(
                    dimension="nfrs",
                    mismatch_type="dep_rule_missing",
                    description=f"Dependency rule '{rule_text}' from spec not addressed in roadmap",
                    location="spec:nfr:dep_rule",
                    spec_quote=context,
                    roadmap_quote="[MISSING]",
                )
            )

    return _route_findings(findings, roadmap_path)


# ---------- Checker Registry ----------

CHECKER_REGISTRY: dict[str, CheckerCallable] = {
    "signatures": check_signatures,
    "data_models": check_data_models,
    "gates": check_gates,
    "cli": check_cli,
    "nfrs": check_nfrs,
}


def run_all_checkers(spec_path: str, roadmap_path: str) -> list[Finding]:
    """Execute all 5 checkers and merge findings.

    Checkers can run in parallel (no shared mutable state, NFR-4).
    Returns a deterministic list of findings sorted by (dimension, rule_id, location).
    """
    all_findings: list[Finding] = []
    for dimension, checker in CHECKER_REGISTRY.items():
        all_findings.extend(checker(spec_path, roadmap_path))

    # Sort for deterministic output (SC-1)
    all_findings.sort(key=lambda f: (f.dimension, f.rule_id, f.location))
    return all_findings
