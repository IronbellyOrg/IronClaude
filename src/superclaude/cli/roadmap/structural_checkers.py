"""Structural checkers — 5 deterministic dimension checkers with severity rules.

Implements FR-1 (5 dimension checkers), FR-3 (anchored severity rules).

Each checker is a callable with signature:
    (spec_path: str, roadmap_path: str) -> list[Finding]

Checkers extract structured data from spec and roadmap using spec_parser,
compare deterministically, and produce typed findings with rule-based severity.
No LLM calls. No shared mutable state between checkers (NFR-4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .convergence import compute_stable_id
from .models import Finding
from .spec_parser import (
    DIMENSION_SECTION_MAP,
    CodeBlock,
    FunctionSignature,
    MarkdownTable,
    ParseResult,
    SpecSection,
    ThresholdExpression,
    extract_code_blocks,
    extract_file_paths,
    extract_file_paths_from_tables,
    extract_function_signatures,
    extract_literal_values,
    extract_thresholds,
    parse_document,
    split_into_sections,
)


# ---------- FR-3: Anchored Severity Rules ----------

SEVERITY_RULES: dict[tuple[str, str], str] = {
    # Signatures
    ("signatures", "phantom_id"): "HIGH",
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
) -> Finding:
    """Create a Finding with rule-based severity and stable ID."""
    severity = get_severity(dimension, mismatch_type)
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

    # Get dimension-relevant sections
    spec_sections = _get_sections_for_dimension("signatures", spec_parsed.sections)
    roadmap_sections = _get_sections_for_dimension("signatures", roadmap_parsed.sections)
    roadmap_full_text = roadmap_text.lower()

    findings: list[Finding] = []

    # --- Phantom ID check: roadmap references IDs not in spec ---
    spec_ids: set[str] = set()
    for family, ids in spec_parsed.requirement_ids.items():
        spec_ids.update(ids)

    roadmap_ids: set[str] = set()
    for family, ids in roadmap_parsed.requirement_ids.items():
        roadmap_ids.update(ids)

    phantom_ids = roadmap_ids - spec_ids
    for pid in sorted(phantom_ids):
        findings.append(_make_finding(
            dimension="signatures",
            mismatch_type="phantom_id",
            description=f"Roadmap references ID '{pid}' not found in spec",
            location=f"roadmap:{pid}",
            spec_quote="[MISSING]",
            roadmap_quote=pid,
        ))

    # --- Function missing check: spec functions not referenced in roadmap ---
    spec_sigs = spec_parsed.function_signatures
    for sig in spec_sigs:
        if sig.name.lower() not in roadmap_full_text:
            findings.append(_make_finding(
                dimension="signatures",
                mismatch_type="function_missing",
                description=f"Function '{sig.name}' defined in spec not found in roadmap",
                location=f"spec:function:{sig.name}",
                spec_quote=f"def {sig.name}({sig.params})" + (f" -> {sig.return_type}" if sig.return_type else ""),
                roadmap_quote="[MISSING]",
            ))

    # --- Param arity mismatch: functions found in both but with different param counts ---
    roadmap_sigs = roadmap_parsed.function_signatures
    roadmap_sig_map = {s.name: s for s in roadmap_sigs}
    for sig in spec_sigs:
        if sig.name in roadmap_sig_map:
            rm_sig = roadmap_sig_map[sig.name]
            spec_params = [p.strip() for p in sig.params.split(",") if p.strip()] if sig.params.strip() else []
            rm_params = [p.strip() for p in rm_sig.params.split(",") if p.strip()] if rm_sig.params.strip() else []
            if len(spec_params) != len(rm_params):
                findings.append(_make_finding(
                    dimension="signatures",
                    mismatch_type="param_arity_mismatch",
                    description=f"Function '{sig.name}' has {len(spec_params)} params in spec but {len(rm_params)} in roadmap",
                    location=f"spec:function:{sig.name}",
                    spec_quote=f"def {sig.name}({sig.params})",
                    roadmap_quote=f"def {rm_sig.name}({rm_sig.params})",
                ))
            else:
                # Check param types where available
                for i, (sp, rp) in enumerate(zip(spec_params, rm_params)):
                    # Extract type annotations if present
                    sp_type = sp.split(":")[-1].strip() if ":" in sp else ""
                    rp_type = rp.split(":")[-1].strip() if ":" in rp else ""
                    if sp_type and rp_type and sp_type != rp_type:
                        findings.append(_make_finding(
                            dimension="signatures",
                            mismatch_type="param_type_mismatch",
                            description=f"Function '{sig.name}' param {i} type differs: spec='{sp_type}' vs roadmap='{rp_type}'",
                            location=f"spec:function:{sig.name}:param:{i}",
                            spec_quote=sp,
                            roadmap_quote=rp,
                        ))

    return findings


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
            findings.append(_make_finding(
                dimension="data_models",
                mismatch_type="file_missing",
                description=f"File '{fpath}' in spec manifest not found in roadmap",
                location=f"spec:file:{fpath}",
                spec_quote=fpath,
                roadmap_quote="[MISSING]",
            ))

    # --- Path prefix mismatch: same filename but different prefix ---
    spec_path_names = {Path(p).name: p for p in spec_file_paths}
    roadmap_path_names = {Path(p).name: p for p in roadmap_file_paths}
    for fname, spec_fpath in spec_path_names.items():
        if fname in roadmap_path_names:
            rm_fpath = roadmap_path_names[fname]
            if spec_fpath != rm_fpath:
                # Different prefix
                findings.append(_make_finding(
                    dimension="data_models",
                    mismatch_type="path_prefix_mismatch",
                    description=f"File '{fname}' has different path: spec='{spec_fpath}' vs roadmap='{rm_fpath}'",
                    location=f"spec:file:{spec_fpath}",
                    spec_quote=spec_fpath,
                    roadmap_quote=rm_fpath,
                ))

    # --- Enum uncovered: Literal enum values in spec not in roadmap ---
    spec_literals = spec_parsed.literal_values
    for literal_group in spec_literals:
        for val in literal_group:
            if val.lower() not in roadmap_full_text:
                findings.append(_make_finding(
                    dimension="data_models",
                    mismatch_type="enum_uncovered",
                    description=f"Enum literal '{val}' from spec not covered in roadmap",
                    location=f"spec:literal:{val}",
                    spec_quote=val,
                    roadmap_quote="[MISSING]",
                ))

    # --- Field missing: dataclass fields in spec code blocks not in roadmap ---
    # Extract field names from spec code blocks (look for field definitions)
    import re
    field_re = re.compile(r'^\s+(\w+)\s*:', re.MULTILINE)
    for block in spec_parsed.code_blocks:
        if block.language and block.language.lower() not in ("python", "py", ""):
            continue
        # Only look at blocks that look like dataclass definitions
        if "class " not in block.content and "@dataclass" not in block.content:
            continue
        for match in field_re.finditer(block.content):
            field_name = match.group(1)
            # Skip dunder and private
            if field_name.startswith("_") or field_name in ("self", "cls", "return", "class", "def", "if", "else", "for", "while", "import", "from", "try", "except"):
                continue
            if field_name.lower() not in roadmap_full_text:
                findings.append(_make_finding(
                    dimension="data_models",
                    mismatch_type="field_missing",
                    description=f"Dataclass field '{field_name}' from spec not referenced in roadmap",
                    location=f"spec:field:{field_name}",
                    spec_quote=field_name,
                    roadmap_quote="[MISSING]",
                ))

    return findings


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
    frontmatter_field_re = re.compile(r'`(\w+)`\s*(?:field|frontmatter|required)', re.IGNORECASE)
    for match in frontmatter_field_re.finditer(spec_gate_text):
        field_name = match.group(1)
        if field_name.lower() not in roadmap_full_text:
            findings.append(_make_finding(
                dimension="gates",
                mismatch_type="frontmatter_field_missing",
                description=f"Required frontmatter field '{field_name}' not found in roadmap",
                location=f"spec:gate:frontmatter:{field_name}",
                spec_quote=match.group(0),
                roadmap_quote="[MISSING]",
            ))

    # --- Step param missing: Step(...) parameters in spec not in roadmap ---
    step_param_re = re.compile(r'Step\s*\([^)]*\b(\w+)\s*=', re.IGNORECASE)
    for match in step_param_re.finditer(spec_gate_text):
        param_name = match.group(1)
        if param_name.lower() not in roadmap_full_text:
            findings.append(_make_finding(
                dimension="gates",
                mismatch_type="step_param_missing",
                description=f"Step parameter '{param_name}' from spec not found in roadmap",
                location=f"spec:gate:step_param:{param_name}",
                spec_quote=match.group(0),
                roadmap_quote="[MISSING]",
            ))

    # --- Ordering violated: check gate ordering constraints ---
    # Extract ordered gate/step names from spec
    order_re = re.compile(r'(?:step|gate|phase)\s*(\d+)', re.IGNORECASE)
    spec_order = [int(m.group(1)) for m in order_re.finditer(spec_gate_text)]
    roadmap_gate_sections = _get_sections_for_dimension("gates", roadmap_parsed.sections)
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
            findings.append(_make_finding(
                dimension="gates",
                mismatch_type="ordering_violated",
                description="Gate/step ordering in roadmap does not match spec ordering",
                location="spec:gate:ordering",
                spec_quote=str(spec_sorted),
                roadmap_quote=str(roadmap_seen),
            ))

    # --- Semantic check missing: named semantic checks in spec not mapped in roadmap ---
    semantic_check_re = re.compile(r'semantic[_ ]check[s]?\s*[:\-]?\s*[`"]?(\w+)', re.IGNORECASE)
    for match in semantic_check_re.finditer(spec_gate_text):
        check_name = match.group(1)
        if check_name.lower() not in roadmap_full_text:
            findings.append(_make_finding(
                dimension="gates",
                mismatch_type="semantic_check_missing",
                description=f"Semantic check '{check_name}' from spec not mapped in roadmap",
                location=f"spec:gate:semantic_check:{check_name}",
                spec_quote=match.group(0),
                roadmap_quote="[MISSING]",
            ))

    return findings


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
                findings.append(_make_finding(
                    dimension="cli",
                    mismatch_type="mode_uncovered",
                    description=f"Config mode '{val}' from spec not covered in roadmap",
                    location=f"spec:cli:mode:{val}",
                    spec_quote=val,
                    roadmap_quote="[MISSING]",
                ))

    # --- Also check CLI flags/options from tables ---
    # Look for option/flag definitions in CLI section tables
    option_re = re.compile(r'`--?([\w-]+)`', re.IGNORECASE)
    for match in option_re.finditer(spec_cli_text):
        option_name = match.group(1)
        if option_name.lower() not in roadmap_full_text:
            findings.append(_make_finding(
                dimension="cli",
                mismatch_type="mode_uncovered",
                description=f"CLI option '--{option_name}' from spec not covered in roadmap",
                location=f"spec:cli:option:{option_name}",
                spec_quote=match.group(0),
                roadmap_quote="[MISSING]",
            ))

    # --- Default mismatch: check defaults in spec vs roadmap ---
    # Extract default values from spec (pattern: `default: value` or `default=value`)
    default_re = re.compile(r'default\s*[=:]\s*[`"\']?(\S+?)[`"\']?\s', re.IGNORECASE)
    spec_defaults: dict[str, str] = {}
    for match in default_re.finditer(spec_cli_text):
        val = match.group(1).strip('`"\'')
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
            rm_val = rm_match.group(1).strip('`"\'')
            # Only flag if both reference the same option context but different values
            if rm_val != val and val.lower() in roadmap_cli_text.lower():
                findings.append(_make_finding(
                    dimension="cli",
                    mismatch_type="default_mismatch",
                    description=f"Default value mismatch: spec='{val}' vs roadmap='{rm_val}'",
                    location=f"spec:cli:default:{val}",
                    spec_quote=context,
                    roadmap_quote=rm_match.group(0),
                ))

    return findings


def check_nfrs(spec_path: str, roadmap_path: str) -> list[Finding]:
    """NFRs checker: verifies numeric thresholds, security primitives, dependency rules.

    Machine keys: threshold_contradicted, security_missing, dep_direction_violated,
                  coverage_mismatch, dep_rule_missing
    """
    import re

    spec_text = Path(spec_path).read_text(encoding="utf-8")
    roadmap_text = Path(roadmap_path).read_text(encoding="utf-8")

    spec_parsed = parse_document(spec_text)
    roadmap_parsed = parse_document(roadmap_text)

    spec_sections = _get_sections_for_dimension("nfrs", spec_parsed.sections)
    roadmap_full_text = roadmap_text.lower()

    findings: list[Finding] = []

    spec_nfr_text = _section_text(spec_sections)

    # --- Threshold contradicted: numeric thresholds in spec vs roadmap ---
    spec_thresholds = extract_thresholds(spec_nfr_text)
    roadmap_thresholds = extract_thresholds(roadmap_text)

    # Build roadmap threshold lookup by raw value
    roadmap_threshold_values: dict[str, ThresholdExpression] = {}
    for t in roadmap_thresholds:
        roadmap_threshold_values[t.value] = t

    for spec_t in spec_thresholds:
        # Check if roadmap has a contradicting threshold for the same metric
        if spec_t.value in roadmap_threshold_values:
            rm_t = roadmap_threshold_values[spec_t.value]
            if spec_t.operator != rm_t.operator:
                findings.append(_make_finding(
                    dimension="nfrs",
                    mismatch_type="threshold_contradicted",
                    description=f"Threshold '{spec_t.raw}' contradicted by '{rm_t.raw}' in roadmap",
                    location=f"spec:nfr:threshold:{spec_t.raw}",
                    spec_quote=spec_t.raw,
                    roadmap_quote=rm_t.raw,
                ))
        elif spec_t.raw.lower() not in roadmap_full_text and spec_t.value not in roadmap_full_text:
            # Threshold not addressed at all
            findings.append(_make_finding(
                dimension="nfrs",
                mismatch_type="threshold_contradicted",
                description=f"NFR threshold '{spec_t.raw}' not addressed in roadmap",
                location=f"spec:nfr:threshold:{spec_t.raw}",
                spec_quote=spec_t.raw,
                roadmap_quote="[MISSING]",
            ))

    # --- Security missing: security primitives in spec not in roadmap ---
    security_keywords = [
        "encryption", "encrypted", "tls", "ssl", "hash", "hmac",
        "auth", "authentication", "authorization", "oauth", "jwt",
        "rbac", "acl", "sanitize", "sanitization", "escape",
        "csrf", "xss", "injection", "secrets", "credential",
    ]
    security_re = re.compile(
        r'\b(' + '|'.join(security_keywords) + r')\b', re.IGNORECASE
    )
    spec_security_terms = set(
        m.group(1).lower() for m in security_re.finditer(spec_nfr_text)
    )
    for term in sorted(spec_security_terms):
        if term not in roadmap_full_text:
            findings.append(_make_finding(
                dimension="nfrs",
                mismatch_type="security_missing",
                description=f"Security primitive '{term}' from spec NFRs not addressed in roadmap",
                location=f"spec:nfr:security:{term}",
                spec_quote=term,
                roadmap_quote="[MISSING]",
            ))

    # --- Dependency direction violated: dependency rules in spec ---
    dep_re = re.compile(
        r'(\w[\w./]+)\s*(?:→|->|depends\s+on|imports?)\s*(\w[\w./]+)',
        re.IGNORECASE,
    )
    spec_deps = [(m.group(1), m.group(2)) for m in dep_re.finditer(spec_nfr_text)]
    roadmap_deps = [(m.group(1), m.group(2)) for m in dep_re.finditer(roadmap_text)]

    roadmap_dep_set = {(a.lower(), b.lower()) for a, b in roadmap_deps}
    for src, tgt in spec_deps:
        # Check if roadmap has the reverse direction
        if (tgt.lower(), src.lower()) in roadmap_dep_set:
            findings.append(_make_finding(
                dimension="nfrs",
                mismatch_type="dep_direction_violated",
                description=f"Dependency direction '{src} → {tgt}' reversed in roadmap",
                location=f"spec:nfr:dep:{src}->{tgt}",
                spec_quote=f"{src} → {tgt}",
                roadmap_quote=f"{tgt} → {src}",
            ))

    # --- Coverage mismatch: coverage thresholds ---
    coverage_re = re.compile(r'coverage\s*[><=]+\s*(\d+)%', re.IGNORECASE)
    spec_coverage = coverage_re.findall(spec_nfr_text)
    roadmap_coverage = coverage_re.findall(roadmap_text)
    if spec_coverage and roadmap_coverage:
        for sc in spec_coverage:
            for rc in roadmap_coverage:
                if int(rc) < int(sc):
                    findings.append(_make_finding(
                        dimension="nfrs",
                        mismatch_type="coverage_mismatch",
                        description=f"Coverage threshold {sc}% in spec but {rc}% in roadmap",
                        location=f"spec:nfr:coverage:{sc}%",
                        spec_quote=f"coverage >= {sc}%",
                        roadmap_quote=f"coverage >= {rc}%",
                    ))

    # --- Dep rule missing: dependency rules from spec not addressed ---
    dep_rule_re = re.compile(
        r'(?:must\s+not|shall\s+not|cannot|must\s+not)\s+(?:import|depend|reference)\b',
        re.IGNORECASE,
    )
    for match in dep_rule_re.finditer(spec_nfr_text):
        rule_text = match.group(0)
        # Get surrounding context
        start = max(0, match.start() - 50)
        end = min(len(spec_nfr_text), match.end() + 50)
        context = spec_nfr_text[start:end].strip()
        if rule_text.lower() not in roadmap_full_text:
            findings.append(_make_finding(
                dimension="nfrs",
                mismatch_type="dep_rule_missing",
                description=f"Dependency rule '{rule_text}' from spec not addressed in roadmap",
                location=f"spec:nfr:dep_rule",
                spec_quote=context,
                roadmap_quote="[MISSING]",
            ))

    return findings


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
