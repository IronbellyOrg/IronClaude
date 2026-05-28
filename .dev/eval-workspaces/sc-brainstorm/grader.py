#!/usr/bin/env python3
"""
Grader for sc-brainstorm-protocol eval runs.

Reads eval_metadata.json from each eval-<name>/ directory, evaluates the
assertions against files in with_skill/outputs/ and old_skill/outputs/,
and writes grading.json files at:
- eval-<name>/with_skill/grading.json (v2 outputs)
- eval-<name>/old_skill/grading.json (v1 baseline outputs)

Output format matches skill-creator grading.json schema:
{expectations: [{text, passed, evidence}], summary: {passed, failed, total, pass_rate}}

Usage:
    python grader.py <iterations/iteration-N-dir>
"""
import json
import re
import sys
from pathlib import Path

import yaml


def read_text(p: Path) -> str | None:
    """Read text file, return None if missing."""
    try:
        return p.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError):
        return None


def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter (between leading --- delimiters). Returns dict of string values."""
    if not text or not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[3:end].strip()
    result = {}
    for line in block.split("\n"):
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            v = v.strip().strip("'\"")
            result[k.strip()] = v
    return result


def parse_yaml_simple(text: str) -> dict:
    """Parse YAML (possibly nested) into a dict.

    Handles two input shapes that the grader's targets use:
      1. Plain YAML files (e.g., return-contract.yaml) — safe_load the whole text.
      2. Markdown files with YAML frontmatter (e.g., debate-transcript.md) — extract
         the frontmatter block between leading `---` delimiters and safe_load just that;
         this avoids the multi-document YAML stream error when safe_load encounters the
         markdown body as a second document.

    Empty or invalid input returns {}.
    """
    if not text:
        return {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 4)
        if end != -1:
            body = text[3:end].strip()
    try:
        loaded = yaml.safe_load(body)
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _resolve_field(d: dict, path: str):
    """Resolve a dotted path 'a.b.0.c' through nested dicts/lists. Returns '' if missing or non-traversable."""
    cur = d
    for part in path.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return ""
        elif isinstance(cur, dict):
            cur = cur.get(part, "")
        else:
            return ""
    return cur


def find_section(text: str, section_pattern: str) -> tuple[int, int] | None:
    """Find (start, end) char offsets of a section by regex-matching its heading.

    Section starts at the heading line, ends at the next heading of same-or-higher level (or EOF).
    """
    if not text:
        return None
    # Match heading line: ## or ### with the pattern
    pattern = re.compile(rf"^(#+)\s+.*({section_pattern}).*$", re.MULTILINE | re.IGNORECASE)
    m = pattern.search(text)
    if not m:
        return None
    start = m.start()
    heading_level = len(m.group(1))
    # Find next heading of same or higher level
    after = text[m.end():]
    next_heading = re.search(rf"^#{{1,{heading_level}}}\s+", after, re.MULTILINE)
    if next_heading:
        end = m.end() + next_heading.start()
    else:
        end = len(text)
    return (start, end)


def count_enumerated_items(text: str, section_pattern: str) -> int:
    """Count enumerated items (bullets `- `, `* `, or numbered `1.` ) in the named section."""
    section_range = find_section(text, section_pattern)
    if not section_range:
        return 0
    section_text = text[section_range[0]:section_range[1]]
    # Match bullets and numbered items at line start (possibly indented)
    items = re.findall(r"^\s*(?:[-*+]|\d+\.)\s+\S", section_text, re.MULTILINE)
    return len(items)


def check_assertion(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    """Evaluate an assertion. Returns (passed, evidence)."""
    a_type = assertion.get("type")
    target = assertion.get("target", "")
    text = assertion.get("text", "")
    target_path = base_dir / target

    if a_type == "file_exists":
        if target_path.exists() and target_path.is_file():
            size = target_path.stat().st_size
            return True, f"File exists at {target} ({size} bytes)"
        return False, f"File missing: {target}"

    if a_type == "frontmatter_field":
        content = read_text(target_path)
        if not content:
            return False, f"File not readable: {target}"
        fm = parse_frontmatter(content)
        field = assertion["field"]
        expected = assertion["expected"]
        actual = fm.get(field, "")
        if actual.lower() == expected.lower():
            return True, f"Frontmatter field {field}={actual} matches expected {expected}"
        return False, f"Frontmatter field {field}={actual!r}, expected {expected!r}"

    if a_type == "section_present":
        content = read_text(target_path)
        if not content:
            return False, f"File not readable: {target}"
        if find_section(content, assertion["section_pattern"]):
            return True, f"Section matching '{assertion['section_pattern']}' found"
        return False, f"Section matching '{assertion['section_pattern']}' NOT found"

    if a_type == "section_enumerated":
        content = read_text(target_path)
        if not content:
            return False, f"File not readable: {target}"
        count = count_enumerated_items(content, assertion["section_pattern"])
        min_items = assertion["min_items"]
        if count >= min_items:
            return True, f"Section '{assertion['section_pattern']}' has {count} enumerated items (>= {min_items})"
        return False, f"Section '{assertion['section_pattern']}' has {count} items, need >= {min_items}"

    if a_type == "yaml_field":
        content = read_text(target_path)
        if not content:
            return False, f"File not readable: {target}"
        y = parse_yaml_simple(content)
        field = assertion["field"]
        expected = str(assertion["expected"])
        raw = _resolve_field(y, field)
        actual = str(raw) if raw != "" else ""
        if actual == expected:
            return True, f"YAML field {field}={actual} matches expected {expected}"
        return False, f"YAML field {field}={actual!r}, expected {expected!r}"

    if a_type == "yaml_field_min":
        content = read_text(target_path)
        if not content:
            return False, f"File not readable: {target}"
        y = parse_yaml_simple(content)
        field = assertion["field"]
        raw = _resolve_field(y, field)
        if not isinstance(raw, (int, float, str)) or raw == "":
            return False, f"YAML field {field} is non-numeric (got {type(raw).__name__}={raw!r})"
        try:
            actual = float(raw)
        except (TypeError, ValueError):
            return False, f"YAML field {field} not numeric: {raw!r}"
        min_val = float(assertion["min_value"])
        if actual >= min_val:
            return True, f"YAML field {field}={actual} >= {min_val}"
        return False, f"YAML field {field}={actual} < {min_val}"

    if a_type == "yaml_substring":
        content = read_text(target_path)
        if not content:
            return False, f"File not readable: {target}"
        y = parse_yaml_simple(content)
        field = assertion["field"]
        raw = _resolve_field(y, field)
        actual = str(raw) if raw != "" else ""
        substrings = assertion.get("substring_any", [])
        for s in substrings:
            if s.lower() in actual.lower():
                return True, f"YAML field {field} contains substring '{s}'"
        return False, f"YAML field {field} contains none of {substrings}"

    if a_type == "dir_count":
        if not target_path.exists() or not target_path.is_dir():
            return False, f"Directory not found: {target}"
        files = list(target_path.iterdir())
        count = len([f for f in files if f.is_file()])
        min_files = assertion["min_files"]
        if count >= min_files:
            return True, f"Directory {target} has {count} files (>= {min_files})"
        return False, f"Directory {target} has {count} files, need >= {min_files}"

    return False, f"Unknown assertion type: {a_type}"


def grade_eval(eval_dir: Path) -> dict:
    """Grade a single eval-<name>/ directory. Writes grading.json for with_skill and old_skill.
    Returns aggregate stats per configuration."""
    metadata_path = eval_dir / "eval_metadata.json"
    if not metadata_path.exists():
        print(f"  SKIP: no eval_metadata.json in {eval_dir.name}")
        return {}

    meta = json.loads(metadata_path.read_text())
    assertions = meta.get("assertions", [])

    # Partition assertions by target prefix
    with_skill_assertions = [a for a in assertions if a.get("target", "").startswith("with_skill/")]
    old_skill_assertions = [a for a in assertions if a.get("target", "").startswith("old_skill/")]

    def build_grading(asserts: list) -> dict:
        expectations = []
        passed_count = 0
        for a in asserts:
            passed, evidence = check_assertion(a, eval_dir)
            expectations.append({
                "text": a["text"],
                "passed": passed,
                "evidence": evidence
            })
            if passed:
                passed_count += 1
        total = len(asserts)
        return {
            "expectations": expectations,
            "summary": {
                "passed": passed_count,
                "failed": total - passed_count,
                "total": total,
                "pass_rate": round(passed_count / total, 4) if total > 0 else 0.0,
            }
        }

    with_grading = build_grading(with_skill_assertions)
    old_grading = build_grading(old_skill_assertions)

    # Write grading.json files
    with_skill_path = eval_dir / "with_skill" / "grading.json"
    old_skill_path = eval_dir / "old_skill" / "grading.json"
    with_skill_path.parent.mkdir(parents=True, exist_ok=True)
    old_skill_path.parent.mkdir(parents=True, exist_ok=True)
    with_skill_path.write_text(json.dumps(with_grading, indent=2))
    old_skill_path.write_text(json.dumps(old_grading, indent=2))

    return {
        "eval_name": meta["eval_name"],
        "with_skill": with_grading["summary"],
        "old_skill": old_grading["summary"]
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python grader.py <iteration-dir>", file=sys.stderr)
        sys.exit(1)

    iter_dir = Path(sys.argv[1])
    if not iter_dir.is_dir():
        print(f"Not a directory: {iter_dir}", file=sys.stderr)
        sys.exit(1)

    results = []
    for eval_dir in sorted(iter_dir.iterdir()):
        if not eval_dir.is_dir() or not eval_dir.name.startswith("eval-"):
            continue
        print(f"Grading {eval_dir.name}...")
        r = grade_eval(eval_dir)
        if r:
            results.append(r)

    # Print summary
    print()
    print("=" * 70)
    print(f"{'Eval':<35} {'V2 (with_skill)':<20} {'V1 (old_skill)':<20}")
    print("-" * 70)
    for r in results:
        ws = r["with_skill"]
        os_ = r["old_skill"]
        print(f"{r['eval_name']:<35} {ws['passed']}/{ws['total']} ({ws['pass_rate']:.0%})        {os_['passed']}/{os_['total']} ({os_['pass_rate']:.0%})")
    print("=" * 70)


if __name__ == "__main__":
    main()
