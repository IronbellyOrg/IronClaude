#!/usr/bin/env python3
"""Roadmap compression tool.

Compresses roadmap markdown files into structured YAML with AC keyword tags.
Designed for pre-processing before diff/merge operations.

Usage:
    python compress_roadmap.py <input.md> [--output <output.yaml>]
    python compress_roadmap.py roadmap-opus-architect.md
    python compress_roadmap.py roadmap-haiku-architect.md --output compressed.yaml
"""

import hashlib
import re
import sys
from pathlib import Path


# --- Controlled Vocabulary for AC Tag Normalization ---

AC_VOCABULARY = {
    # Status codes
    r"\b200\b": "200",
    r"\b201\b": "201",
    r"\b400\b": "400",
    r"\b401\b": "401",
    r"\b409\b": "409",
    r"\b423\b": "423",
    r"\b429\b": "429",
    # Auth concepts
    r"valid\s*cred": "valid-creds",
    r"invalid\s*cred|wrong\s*password": "invalid-creds",
    r"no\s*(?:user\s*)?enum": "no-enum",
    r"lock(?:out|ed)": "lockout",
    r"rate\s*limit": "rate-limit",
    r"bcrypt": "bcrypt",
    r"rs256|rsa": "rs256",
    r"jwt|json\s*web\s*token": "jwt",
    r"refresh\s*token": "refresh",
    r"access\s*token": "access",
    r"single[- ]use": "single-use",
    r"rotat(?:e|ion)": "rotation",
    r"revok(?:e|ation)": "revocation",
    # Data/infra
    r"postgres|pg-pool": "postgres",
    r"redis": "redis",
    r"uuid": "uuid-pk",
    r"email.*unique|unique.*email": "email:unique",
    r"email.*index|index.*email": "email:indexed",
    r"audit.?log": "audit-log",
    # Security
    r"no\s*plaintext|never\s*persist": "no-plaintext",
    r"httponly": "httponly-cookie",
    r"memory[- ]only": "memory-only",
    r"csp|content.security.policy": "csp-headers",
    r"tls\s*1\.3": "tls:1.3",
    r"cors": "cors",
    r"xss": "xss-mitigation",
    # Performance
    r"p95": "p95",
    r"concurrent": "concurrent",
    # Frontend
    r"redirect": "redirect",
    r"inline.validation|real.time.validation": "inline-validation",
    # Compliance
    r"gdpr": "gdpr",
    r"soc2|soc\s*2": "soc2",
    # Testing
    r"unit\s*test": "unit-test",
    r"integration\s*test": "integration-test",
    r"e2e|end.to.end": "e2e-test",
    r"coverage": "coverage",
    r"k6": "k6",
    # Operations
    r"health\s*check": "health-check",
    r"prometheus": "prometheus",
    r"grafana": "grafana",
    r"alert": "alerting",
    r"feature\s*flag": "feature-flag",
    r"rollback": "rollback",
    r"rollout": "rollout",
}


def compress_ac(ac_text: str) -> list[str]:
    """Compress acceptance criteria prose into keyword tags."""
    if not ac_text or ac_text.strip() in ("-", "\u2014", ""):
        return ["none"]

    tags = []
    seen = set()
    ac_lower = ac_text.lower()

    for pattern, tag in AC_VOCABULARY.items():
        if re.search(pattern, ac_lower) and tag not in seen:
            tags.append(tag)
            seen.add(tag)

    # Extract numeric thresholds
    for m in re.finditer(r"(\d+)\s*(?:req|requests?)/min", ac_lower):
        tags.append(f"rate:{m.group(1)}/min")
    for m in re.finditer(r"<\s*(\d+)\s*ms", ac_lower):
        tags.append(f"latency:<{m.group(1)}ms")
    for m in re.finditer(r"(\d+)\s*(?:concurrent|simultaneous)", ac_lower):
        tags.append(f"concurrent:{m.group(1)}")
    for m in re.finditer(r"cost\s*factor\s*(\d+)", ac_lower):
        tags.append(f"bcrypt:{m.group(1)}")
    for m in re.finditer(r"(\d+)[- ](?:bit|bits)", ac_lower):
        tags.append(f"bits:{m.group(1)}")
    for m in re.finditer(r"(\d+)\s*(?:day|days)\s*(?:ttl|TTL|expir)", ac_lower):
        tags.append(f"ttl:{m.group(1)}d")
    for m in re.finditer(r"(\d+)\s*(?:min|minute|minutes?)\s*(?:ttl|TTL|expir)", ac_lower):
        tags.append(f"ttl:{m.group(1)}m")
    for m in re.finditer(r"(\d+)\s*(?:hour|hours?)\s*(?:ttl|TTL|expir)", ac_lower):
        tags.append(f"ttl:{m.group(1)}h")
    for m in re.finditer(r"(\d+)s\s*(?:ttl|TTL)", ac_lower):
        tags.append(f"ttl:{m.group(1)}s")

    if not tags:
        # Fallback: extract key verb-noun pairs from AC text
        # Strip common filler words
        filler = {"the", "and", "with", "that", "this", "from", "into", "for", "are", "all", "per", "has", "have", "been", "must", "should", "shall"}
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", ac_text)
        significant = [w.lower() for w in words if len(w) > 3 and w.lower() not in filler][:3]
        if significant:
            tags.append("-".join(significant))
        else:
            tags.append("misc")

    return list(dict.fromkeys(tags))  # deduplicate preserving order


def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    """Extract YAML frontmatter, return (meta_dict, end_line)."""
    meta = {}
    if not lines or lines[0].strip() != "---":
        return meta, 0

    end_idx = 0
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i + 1
            break
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
            meta[key] = val

    return meta, end_idx


def parse_table_rows(lines: list[str]) -> list[dict]:
    """Parse markdown table rows into list of dicts."""
    rows = []
    header = None

    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells:
            continue
        # Skip separator rows
        if all(re.match(r"^[-:]+$", c) for c in cells):
            continue
        if header is None:
            header = [c.lower().replace(" ", "_") for c in cells]
            continue
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))

    return rows


def extract_phase_blocks(content: str) -> list[dict]:
    """Extract phase blocks with their task tables."""
    phases = []
    phase_pattern = re.compile(
        r"###\s*Phase\s*(\d+)\s*[:\u2014\u2013\-]+\s*(.+?)$",
        re.MULTILINE,
    )

    matches = list(phase_pattern.finditer(content))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[start:end]

        phase_num = int(m.group(1))
        phase_name = m.group(2).strip()

        # Extract table rows from this block
        table_lines = [l for l in block.split("\n") if "|" in l]
        task_rows = parse_table_rows(table_lines)

        # Extract integration points if present
        integ_points = []
        integ_match = re.search(
            r"(?:Integration Points|integration_points)(.*?)(?=###|---|\.\.\.\s*$|$)",
            block,
            re.DOTALL | re.IGNORECASE,
        )
        if integ_match:
            for line in integ_match.group(1).split("\n"):
                name_m = re.search(r"Named Artifact[:\s]*`?([^`\n]+)`?", line)
                if name_m:
                    integ_points.append(name_m.group(1).strip())

        phases.append(
            {
                "phase": phase_num,
                "name": phase_name,
                "tasks": task_rows,
                "integration_points": integ_points,
            }
        )

    return phases


def extract_section_summary(content: str, heading_pattern: str) -> str:
    """Extract a section and compress to one-line summary."""
    m = re.search(
        rf"##\s*{heading_pattern}(.+?)(?=\n##\s|$)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return ""
    text = m.group(1).strip()
    # Strip markdown tables, list items, and formatting
    lines = text.split("\n")
    prose_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip table rows, separators, empty lines, sub-headings
        if stripped.startswith("|") or stripped.startswith("---") or not stripped:
            continue
        if stripped.startswith("###"):
            continue
        if stripped.startswith("```"):
            continue
        # Strip bold/italic markdown
        cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
        cleaned = re.sub(r"\*(.+?)\*", r"\1", cleaned)
        cleaned = re.sub(r"`(.+?)`", r"\1", cleaned)
        prose_lines.append(cleaned)
    # Join prose and take first 200 chars
    prose = " ".join(prose_lines)[:200].strip()
    # Escape quotes for YAML
    prose = prose.replace('"', "'")
    return prose


def sha256_section(text: str) -> str:
    """Compute SHA-256 hash of a text section."""
    normalized = re.sub(r"\s+", " ", text.strip())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def compress_roadmap(input_path: str) -> str:
    """Compress a roadmap markdown file into structured YAML."""
    path = Path(input_path)
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Step 1: Extract frontmatter
    meta, fm_end = parse_frontmatter(lines)

    # Step 2: Extract phase blocks
    phases = extract_phase_blocks(content)

    # Step 3: Compress narrative sections
    exec_summary = extract_section_summary(content, r"\d*\.?\s*Executive Summary")
    risk_summary = extract_section_summary(content, r"\d*\.?\s*Risk")
    resource_summary = extract_section_summary(content, r"\d*\.?\s*Resource")
    timeline_summary = extract_section_summary(content, r"\d*\.?\s*Timeline")

    # Extract critical path (look for arrow-chain notation)
    cp_match = re.search(r"```\s*\n(.*?\u2192.*?)\n\s*```", content, re.DOTALL)
    critical_path = ""
    if cp_match:
        cp_text = cp_match.group(1).strip()
        critical_path = re.sub(r"\s+", " ", cp_text.replace("\n", " "))[:300]
        critical_path = critical_path.replace('"', "'")
    else:
        # Fallback: look for M1 -> M2 style chains
        cp_match2 = re.search(r"((?:INFRA|COMP|FR|DM|API|M)\S+.*?\u2192.*?M5)", content)
        if cp_match2:
            critical_path = re.sub(r"\s+", " ", cp_match2.group(1))[:300]

    # Step 4: Build YAML output
    out = []
    out.append("# Compressed Roadmap")
    out.append(f"# Source: {path.name}")
    out.append("# Method: Normalized YAML with AC keyword tags")
    out.append("")

    # Meta section
    out.append("meta:")
    out.append(f"  source_file: {path.name}")
    for k, v in meta.items():
        if isinstance(v, list):
            out.append(f"  {k}: [{', '.join(str(i) for i in v)}]")
        else:
            out.append(f"  {k}: {v}")

    # Summaries
    out.append("")
    out.append("summaries:")
    if exec_summary:
        out.append(f'  executive: "{exec_summary}"')
    if risk_summary:
        out.append(f'  risk: "{risk_summary}"')
    if resource_summary:
        out.append(f'  resources: "{resource_summary}"')
    if timeline_summary:
        out.append(f'  timeline: "{timeline_summary}"')
    if critical_path:
        out.append(f'  critical_path: "{critical_path}"')

    # Integration points (extract from all phases + top-level)
    out.append("")
    out.append("integration_points:")
    integ_found = False

    # Method 1: Table-format integration points (Opus style)
    # | # | Named Artifact | Type | Wired Components | Owning Phase | Cross-Reference Phases |
    integ_table_match = re.search(
        r"##\s*\d*\.?\s*Integration Points\s*\n(.+?)(?=\n##\s|\n---)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if integ_table_match:
        table_lines = integ_table_match.group(1).strip().split("\n")
        for line in table_lines:
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) < 6:
                continue
            # Skip header and separator rows
            if re.match(r"^[-:]+$", cells[0]) or cells[0].lower() == "#":
                continue
            name = re.sub(r"\*\*(.+?)\*\*", r"\1", cells[1]).strip()
            wired_raw = cells[3].strip()
            wired = [w.strip().strip("`") for w in wired_raw.split(",")]
            # Extract phase number from "Phase N (...)" format
            phase_m = re.search(r"Phase\s*(\d+)", cells[4])
            phase = phase_m.group(1) if phase_m else "?"
            # Extract cross-ref phase numbers
            xref_nums = re.findall(r"Phase\s*(\d+)", cells[5])
            wired_str = ", ".join(w[:30] for w in wired)
            xref_str = ", ".join(xref_nums)
            short_name = name[:40].replace(" ", "_")
            out.append(f"  - {{name: {short_name}, wired: [{wired_str}], phase: {phase}, xref: [{xref_str}]}}")
            integ_found = True

    # Method 2: Paragraph-style integration points (Haiku per-phase style)
    if not integ_found:
        integ_pattern = re.compile(
            r"\*\*Named Artifact:\*\*\s*`?([^`\n]+)`?"
            r".*?Wired Components:\*\*\s*(.+?)"
            r".*?Owning Phase:\*\*\s*Phase\s*(\d+)"
            r".*?Cross-Reference.*?Phase[s]?\s*([\d, ]+)",
            re.DOTALL,
        )
        for m in integ_pattern.finditer(content):
            name = m.group(1).strip()
            wired = [w.strip().strip("`") for w in m.group(2).split(",")]
            phase = m.group(3).strip()
            xref = [x.strip() for x in m.group(4).split(",")]
            wired_str = ", ".join(wired)
            xref_str = ", ".join(xref)
            out.append(f"  - {{name: {name}, wired: [{wired_str}], phase: {phase}, xref: [{xref_str}]}}")
            integ_found = True

    # Method 3: Per-phase inline integration points
    if not integ_found:
        for phase_block in phases:
            for ip_name in phase_block.get("integration_points", []):
                out.append(f"  - {{name: {ip_name}, phase: {phase_block['phase']}}}")

    # Task rows - compact TSV format (header once, data rows)
    out.append("")
    out.append("# TASKS (TSV: P=phase, R=row, ID, TASK, COMP, DEPS, AC, EFF, PRI)")
    global_row = 0
    for phase_block in phases:
        pn = phase_block["phase"]
        pname = phase_block["name"]
        out.append(f"# P{pn}: {pname} ({len(phase_block['tasks'])} rows)")

        for task in phase_block["tasks"]:
            global_row += 1
            tid = task.get("id", task.get("#", "")).strip()
            # Normalize em-dash, en-dash, bare numbers, empty to synthetic IDs
            if tid in ("", "#", "\u2014", "\u2013", "-") or re.match(r"^\d+$", tid):
                tid = f"P{pn}-{global_row}"

            task_name = task.get("task", "").strip()
            # Aggressively shorten: remove prefixes, cap at 35 chars
            task_name = re.sub(r"^(?:Implement|Create|Configure|Validate|Define|Establish|Build|Design)\s+", "", task_name)
            task_name = re.sub(r"\s+(?:the|for|with|and|in|on|of|to|from|against|via|per)\s+", " ", task_name)
            task_name = task_name[:35].strip()
            comp = task.get("component", "").strip()
            # Shorten common component names
            comp_map = {
                "Infrastructure": "Infra",
                "Documentation": "Docs",
                "AuthService": "Auth",
                "Architecture": "Arch",
                "Architecture governance": "Arch",
                "API Gateway": "GW",
                "Frontend": "FE",
                "Milestone": "Gate",
                "Security": "Sec",
                "Database": "DB",
                "TokenManager": "TokMgr",
                "Operations": "Ops",
                "Performance": "Perf",
                "Testing": "Test",
                "Validation": "Val",
            }
            for full, short in comp_map.items():
                if comp.lower().startswith(full.lower()):
                    comp = short
                    break

            deps_raw = task.get("dependencies", task.get("deps", "")).strip()
            deps = (
                [d.strip() for d in deps_raw.split(",") if d.strip() and d.strip() != "\u2014" and d.strip() != "-"]
                if deps_raw
                else []
            )
            ac_raw = task.get("acceptance_criteria", task.get("ac", "")).strip()
            ac_tags = compress_ac(ac_raw)
            effort = task.get("effort", "").strip()
            pri = task.get("priority", "").strip()

            deps_str = ",".join(deps) if deps else "-"
            ac_str = ",".join(ac_tags)
            # Compact TSV row: P|R|ID|TASK|COMP|DEPS|AC|EFF|PRI
            out.append(f"{pn}|{global_row}|{tid}|{task_name}|{comp}|{deps_str}|{ac_str}|{effort}|{pri}")

    # Chunk hashes
    out.append("")
    out.append("chunk_hashes:")
    out.append(f"  meta: {sha256_section(str(meta))}")
    for phase_block in phases:
        pn = phase_block["phase"]
        phase_text = str(phase_block["tasks"])
        out.append(f"  phase_{pn}: {sha256_section(phase_text)}")

    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print("Usage: compress_roadmap.py <input.md> [--output <output.yaml>]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    result = compress_roadmap(input_path)

    if output_path:
        Path(output_path).write_text(result, encoding="utf-8")
        print(f"Compressed: {input_path} -> {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
