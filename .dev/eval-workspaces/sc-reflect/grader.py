#!/usr/bin/env python3
"""
Grader for sc-reflect-protocol eval runs.

Reads eval_metadata.json from each eval-<name>/ directory, evaluates the
assertions against files in with_skill/outputs/ and old_skill/outputs/,
and writes grading.json files at:
- eval-<name>/with_skill/grading.json (v2 outputs)
- eval-<name>/old_skill/grading.json (v1 baseline outputs)

Output format matches skill-creator grading.json schema:
{expectations: [{text, passed, evidence}], summary: {passed, failed, total, pass_rate}}

Inherits the 8 sc-brainstorm baseline assertion types (file_exists, frontmatter_field,
section_present, section_enumerated, yaml_field, yaml_field_min, yaml_substring,
dir_count) and extends with 11 new types per refs/grader-extensions.md:
citation_resolves, regex_present, regex_absent, yaml_list_contains,
yaml_list_len_eq, matrix_covers_items, checkpoint_logged,
deviation_class_matches, path_exists, path_does_not_exist,
falsifier_skeleton_present.

Usage:
    python grader.py <iterations/iteration-N-dir>
"""
import json
import re
import sys
from functools import reduce
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
    """Parse a simple flat YAML file (no nesting). Returns dict of string values.

    Retained for backward compatibility with the 8 baseline assertion types
    inherited from sc-brainstorm. New types (citation_resolves, yaml_list_contains,
    matrix_covers_items, deviation_class_matches, falsifier_skeleton_present)
    use the proper `yaml.safe_load` parser.
    """
    if not text:
        return {}
    result = {}
    for line in text.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#") or line.startswith(" "):
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            v = v.strip().strip("'\"")
            result[k.strip()] = v
    return result


def find_section(text: str, section_pattern: str) -> tuple[int, int] | None:
    """Find (start, end) char offsets of a section by regex-matching its heading.

    Section starts at the heading line, ends at the next heading of same-or-higher level (or EOF).
    """
    if not text:
        return None
    pattern = re.compile(rf"^(#+)\s+.*({section_pattern}).*$", re.MULTILINE | re.IGNORECASE)
    m = pattern.search(text)
    if not m:
        return None
    start = m.start()
    heading_level = len(m.group(1))
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
    items = re.findall(r"^\s*(?:[-*+]|\d+\.)\s+\S", section_text, re.MULTILINE)
    return len(items)


# ---------------------------------------------------------------------------
# New assertion-type helpers (per refs/grader-extensions.md)
# ---------------------------------------------------------------------------

CITATION_RE = re.compile(r"`?([\w./\-]+\.(?:py|md|yaml|ts|js)):(\d+)`?")
CANONICAL_FALSIFIER_FIELDS = {"id", "type", "fixture", "expected", "assertion"}


def check_citation_resolves(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    report_path = base_dir / assertion["report"]
    if not report_path.exists():
        return False, f"report file missing: {assertion['report']}"
    report = report_path.read_text(encoding="utf-8")
    fixture_root_raw = assertion.get("fixture_root")
    fixture_root = Path(fixture_root_raw) if fixture_root_raw else base_dir
    if not fixture_root.is_absolute():
        fixture_root = base_dir / fixture_root
    expected_snippets = assertion.get("expected_snippets", {}) or {}
    resolved, failed = 0, []
    for m in CITATION_RE.finditer(report):
        rel_path, line_no = m.group(1), int(m.group(2))
        target = Path(rel_path) if Path(rel_path).is_absolute() else (fixture_root / rel_path)
        if not target.exists():
            failed.append(f"{rel_path}:{line_no} (file missing)")
            continue
        lines = target.read_text(encoding="utf-8").splitlines()
        window = "\n".join(lines[max(0, line_no - 6):line_no + 5])
        snippet = expected_snippets.get(f"{rel_path}:{line_no}")
        if snippet and snippet not in window:
            failed.append(f"{rel_path}:{line_no} (snippet not in ±5 window)")
        else:
            resolved += 1
    total = resolved + len(failed)
    if total == 0:
        return False, "no citations found in report"
    if not failed:
        return True, f"{resolved}/{total} citations resolved"
    return False, f"{resolved}/{total} citations resolved; failures={failed}"


def check_regex_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    text = target.read_text(encoding="utf-8") if target.exists() else ""
    pattern = re.compile(assertion["pattern"], re.MULTILINE | re.DOTALL)
    matches = pattern.findall(text)
    if matches:
        return True, f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}"
    return False, f"Pattern {assertion['pattern']!r} NOT found in {assertion['target']}"


def check_regex_absent(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    text = target.read_text(encoding="utf-8") if target.exists() else ""
    pattern = re.compile(assertion["pattern"], re.MULTILINE | re.DOTALL)
    m = pattern.search(text)
    if m is None:
        return True, f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}"
    return False, f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}"


def check_yaml_list_contains(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    if not target.exists():
        return False, f"YAML file missing: {assertion['target']}"
    data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    keys = assertion["field_path"].split(".")
    try:
        node = reduce(lambda d, k: d[int(k)] if k.isdigit() else d[k], keys, data)
    except (KeyError, IndexError, TypeError) as e:
        return False, f"field_path {assertion['field_path']!r} unresolvable: {e}"
    if not isinstance(node, list):
        return False, f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})"
    expected = assertion["value"]
    if expected in node:
        return True, f"List at {assertion['field_path']} contains {expected!r}; members={node}"
    return False, f"List at {assertion['field_path']} missing {expected!r}; members={node}"


def check_yaml_list_len_eq(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    if not target.exists():
        return False, f"YAML file missing: {assertion['target']}"
    data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return False, (
            f"YAML root at {assertion['target']} is not a mapping "
            f"(got {type(data).__name__})"
        )
    list_field = assertion["list_field"]
    count_field = assertion["count_field"]
    items = data.get(list_field)
    if not isinstance(items, list):
        return False, f"{list_field!r} is not a list (got {type(items).__name__})"
    try:
        expected = int(data[count_field])
    except KeyError:
        return False, f"count field {count_field!r} missing"
    except (TypeError, ValueError):
        return False, f"count field {count_field!r} not an integer: {data.get(count_field)!r}"
    actual = len(items)
    if actual == expected:
        return True, f"len({list_field}) == {count_field} == {actual}"
    return False, f"len({list_field})={actual}, {count_field}={expected}"



def check_matrix_covers_items(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    matrix_path = base_dir / assertion["matrix"]
    source_path = base_dir / assertion["source"]
    threshold = float(assertion.get("threshold", 0.8))
    if not matrix_path.exists():
        return False, f"matrix file missing: {assertion['matrix']}"
    if not source_path.exists():
        return False, f"source file missing: {assertion['source']}"
    matrix = yaml.safe_load(matrix_path.read_text(encoding="utf-8")) or []
    source = yaml.safe_load(source_path.read_text(encoding="utf-8")) or {}
    if isinstance(matrix, dict) and "rows" in matrix:
        matrix = matrix["rows"]
    source_items = {item["id"] for item in source.get("items", [])}
    covered = {row["item_id"] for row in matrix if row.get("status") and row["status"] != "uncovered"}
    if not source_items:
        return False, "Source fixture has no items to cover"
    ratio = len(covered & source_items) / len(source_items)
    if ratio >= threshold:
        return True, f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)"
    return False, f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}"


def check_checkpoint_logged(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    audit = base_dir / assertion["audit_log"]
    if not audit.exists():
        return False, f"audit.log missing: {assertion['audit_log']}"
    name = assertion["checkpoint_name"]
    matches = []
    for i, raw in enumerate(audit.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if row.get("checkpoint") == name:
            matches.append((i, row.get("step"), row.get("ts")))
    if matches:
        return True, f"checkpoint {name!r} logged {len(matches)}x; first={matches[0]}"
    return False, f"checkpoint {name!r} not found in {assertion['audit_log']}"


def check_deviation_class_matches(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    fixture_path = base_dir / assertion["annotated_fixture"]
    report_path = base_dir / assertion["report"]
    if not fixture_path.exists():
        return False, f"annotated_fixture missing: {assertion['annotated_fixture']}"
    if not report_path.exists():
        return False, f"report missing: {assertion['report']}"
    fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8")) or {}
    report = yaml.safe_load(report_path.read_text(encoding="utf-8")) or {}
    hunk_id = assertion["diff_hunk_id"]
    expected = next((h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id), None)
    actual = next((e["deviation_class"] for e in report.get("deviation_register", []) if e.get("hunk_id") == hunk_id), None)
    if expected is None:
        return False, f"hunk {hunk_id!r} not present in annotated fixture"
    if expected == actual:
        return True, f"hunk {hunk_id} class matches: {expected}"
    return False, f"hunk {hunk_id} expected {expected!r}, report has {actual!r}"


def check_path_exists(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = Path(assertion["target"])
    target = target if target.is_absolute() else (base_dir / target)
    if target.exists():
        stat = target.stat()
        kind = "dir" if target.is_dir() else "file"
        return True, f"path exists ({kind}, {stat.st_size} bytes): {target}"
    return False, f"path does not exist: {target}"


def check_path_does_not_exist(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = Path(assertion["target"])
    target = target if target.is_absolute() else (base_dir / target)
    if not target.exists():
        return True, f"path correctly absent: {target}"
    kind = "dir" if target.is_dir() else "file"
    return False, f"path unexpectedly present ({kind}): {target}"


def check_falsifier_skeleton_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    case = base_dir / assertion["case_yaml"]
    if not case.exists():
        return False, f"falsifier case YAML missing: {assertion['case_yaml']}"
    try:
        data = yaml.safe_load(case.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return False, f"falsifier case YAML unparsable: {e}"
    status = data.get("status")
    if status == "skeleton-pending-iteration-3-fixture":
        return True, f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}"
    if status == "active":
        missing = CANONICAL_FALSIFIER_FIELDS - set(data.keys())
        if missing:
            return False, f"active falsifier missing required fields: {sorted(missing)}"
        return True, f"active falsifier with canonical fields; id={data.get('id')!r}"
    return False, f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'"


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def check_assertion(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    """Evaluate an assertion. Returns (passed, evidence)."""
    a_type = assertion.get("type")
    target = assertion.get("target", "")
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
        actual = y.get(field, "")
        if actual == expected:
            return True, f"YAML field {field}={actual} matches expected {expected}"
        return False, f"YAML field {field}={actual!r}, expected {expected!r}"

    if a_type == "yaml_field_min":
        content = read_text(target_path)
        if not content:
            return False, f"File not readable: {target}"
        y = parse_yaml_simple(content)
        field = assertion["field"]
        try:
            actual = float(y.get(field, "0"))
        except (TypeError, ValueError):
            return False, f"YAML field {field} not numeric: {y.get(field)!r}"
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
        actual = y.get(field, "")
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

    # New assertion types per refs/grader-extensions.md
    if a_type == "citation_resolves":
        return check_citation_resolves(assertion, base_dir)
    if a_type == "regex_present":
        return check_regex_present(assertion, base_dir)
    if a_type == "regex_absent":
        return check_regex_absent(assertion, base_dir)
    if a_type == "yaml_list_contains":
        return check_yaml_list_contains(assertion, base_dir)
    if a_type == "yaml_list_len_eq":
        return check_yaml_list_len_eq(assertion, base_dir)
    if a_type == "matrix_covers_items":
        return check_matrix_covers_items(assertion, base_dir)
    if a_type == "checkpoint_logged":
        return check_checkpoint_logged(assertion, base_dir)
    if a_type == "deviation_class_matches":
        return check_deviation_class_matches(assertion, base_dir)
    if a_type == "path_exists":
        return check_path_exists(assertion, base_dir)
    if a_type == "path_does_not_exist":
        return check_path_does_not_exist(assertion, base_dir)
    if a_type == "falsifier_skeleton_present":
        return check_falsifier_skeleton_present(assertion, base_dir)

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

    (eval_dir / "with_skill" / "grading.json").write_text(json.dumps(with_grading, indent=2))
    (eval_dir / "old_skill" / "grading.json").write_text(json.dumps(old_grading, indent=2))

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
