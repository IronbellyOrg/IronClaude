#!/usr/bin/env python3
"""Grade sc-auggie-review eval runs against assertions in eval_metadata.json.

For each run dir (<eval>/<config>/), reads parent's eval_metadata.json,
evaluates each assertion against outputs/, writes grading.json with
fields {text, passed, evidence} as the viewer expects.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def load_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def assert_file_exists(run_dir: Path, a: dict) -> tuple[bool, str]:
    p = run_dir / a["path"]
    if p.exists():
        return True, f"present ({p.stat().st_size} bytes)"
    return False, f"missing: {p}"


def assert_min_size(run_dir: Path, a: dict) -> tuple[bool, str]:
    p = run_dir / a["path"]
    if not p.exists():
        return False, f"file missing: {p}"
    sz = p.stat().st_size
    ok = sz >= a["min_bytes"]
    return ok, f"{sz} bytes (min {a['min_bytes']})"


def assert_contains_any(run_dir: Path, a: dict) -> tuple[bool, str]:
    text = load_text(run_dir / a["path"])
    hits = [p for p in a["patterns"] if p in text]
    if hits:
        return True, f"matched: {hits[0]}"
    return False, f"none of {a['patterns']} found"


def assert_contains_any_regex(run_dir: Path, a: dict) -> tuple[bool, str]:
    text = load_text(run_dir / a["path"])
    for pat in a["patterns"]:
        m = re.search(pat, text)
        if m:
            return True, f"matched /{pat}/ → {m.group(0)[:80]!r}"
    return False, f"no regex matched: {a['patterns']}"


def assert_contains_all_regex(run_dir: Path, a: dict) -> tuple[bool, str]:
    text = load_text(run_dir / a["path"])
    missing = [p for p in a["patterns"] if not re.search(p, text)]
    if not missing:
        return True, f"all {len(a['patterns'])} patterns matched"
    return False, f"missing: {missing}"


def assert_not_contains_regex(run_dir: Path, a: dict) -> tuple[bool, str]:
    text = load_text(run_dir / a["path"])
    for pat in a["patterns"]:
        m = re.search(pat, text)
        if m:
            return False, f"unexpected match /{pat}/ → {m.group(0)[:80]!r}"
    return True, f"none of {len(a['patterns'])} forbidden patterns found"


def assert_file_exists_if_with_skill(run_dir: Path, a: dict) -> tuple[bool, str]:
    # Only applies to with_skill configs; for without_skill, treat as N/A → pass with note.
    config = run_dir.name  # with_skill | without_skill
    if config != "with_skill":
        return True, f"N/A (config={config})"
    p = run_dir / a["path"]
    if p.exists():
        return True, f"present ({p.stat().st_size} bytes)"
    return False, f"required for with_skill, missing: {p}"


# Validate every <path>:<line> citation in REVIEW.md against repo files.
# A citation is valid iff (a) the file exists relative to repo_root, AND
# (b) the line number is within the file's line count.
_CITE_RE = re.compile(r"\b([\w/.\-]+\.(?:py|md|sh|json|toml|yml|yaml|cfg|ini)):(\d+)\b")


def assert_cited_files_validate(run_dir: Path, a: dict) -> tuple[bool, str]:
    text = load_text(run_dir / a["path"])
    repo_root = Path(a["repo_root"])
    citations = _CITE_RE.findall(text)
    if not citations:
        # Try alternative format `path L<n>` as fallback
        alt = re.findall(r"\b([\w/.\-]+\.(?:py|md|sh))\b[^\w\n]+L(\d+)", text)
        citations = alt
    if not citations:
        return False, "no parseable file:line citations found"
    # Deduplicate
    seen = set()
    unique = []
    for f, line in citations:
        key = (f, int(line))
        if key not in seen:
            seen.add(key)
            unique.append(key)
    valid = 0
    invalid = []
    # Try several search strategies for each cited file
    for fname, lineno in unique:
        # Skip obviously non-repo references (e.g., /tmp/..., URLs)
        if fname.startswith("/tmp/") or fname.startswith("http"):
            continue
        candidates = [repo_root / fname]
        # Also try without leading repo-prefix segments (e.g., the citation may omit "src/")
        if not (repo_root / fname).exists():
            # bare-name search
            matches = list(repo_root.rglob(Path(fname).name))
            # filter out venv/build dirs
            matches = [m for m in matches if not any(p in m.parts for p in (".venv", "venv", "node_modules", ".tox", "__pycache__", "dist", "build"))]
            candidates.extend(matches[:3])
        resolved = None
        for c in candidates:
            if c.exists() and c.is_file():
                resolved = c
                break
        if resolved is None:
            invalid.append(f"{fname}:{lineno} (file not found)")
            continue
        try:
            line_count = sum(1 for _ in resolved.open("rb"))
        except Exception:
            line_count = 0
        if line_count == 0 or lineno <= line_count:
            valid += 1
        else:
            invalid.append(f"{fname}:{lineno} (file has only {line_count} lines)")
    total = len([c for c in unique if not c[0].startswith("/tmp/") and not c[0].startswith("http")])
    if total == 0:
        return False, "no real-file citations to validate"
    pct = 100 * valid / total
    # Threshold: ≥80% of citations must ground correctly
    ok = pct >= 80
    summary = f"{valid}/{total} citations validated ({pct:.0f}%)"
    if invalid:
        summary += f"; first invalid: {invalid[0]}"
    return ok, summary


KINDS = {
    "file_exists": assert_file_exists,
    "min_size": assert_min_size,
    "contains_any": assert_contains_any,
    "contains_any_regex": assert_contains_any_regex,
    "contains_all_regex": assert_contains_all_regex,
    "not_contains_regex": assert_not_contains_regex,
    "file_exists_if_with_skill": assert_file_exists_if_with_skill,
    "cited_files_validate": assert_cited_files_validate,
}


def grade_run(run_dir: Path, eval_meta: dict) -> dict:
    expectations = []
    for a in eval_meta.get("assertions", []):
        kind = a["kind"]
        fn = KINDS.get(kind)
        if fn is None:
            expectations.append({"text": a["name"], "passed": False, "evidence": f"unknown kind: {kind}"})
            continue
        try:
            passed, evidence = fn(run_dir, a)
        except Exception as e:
            passed, evidence = False, f"grader error: {e}"
        expectations.append({"text": a["name"], "passed": passed, "evidence": evidence})
    passed_n = sum(1 for e in expectations if e["passed"])
    total = len(expectations)
    return {
        "run_id": f"{eval_meta['eval_name']}-{run_dir.name}",
        "expectations": expectations,
        "summary": {
            "passed": passed_n,
            "failed": total - passed_n,
            "total": total,
            "pass_rate": (passed_n / total) if total else 0.0,
        },
    }


def main() -> int:
    iter_dir = Path(__file__).parent
    eval_dirs = sorted(d for d in iter_dir.iterdir() if d.is_dir() and d.name.startswith("eval-"))
    total_pass = 0
    total_assertions = 0
    for ed in eval_dirs:
        meta_path = ed / "eval_metadata.json"
        if not meta_path.exists():
            print(f"WARN: no metadata at {meta_path}")
            continue
        meta = json.loads(meta_path.read_text())
        for config in ("with_skill", "without_skill"):
            config_dir = ed / config
            if not config_dir.exists():
                continue
            grading = grade_run(config_dir, meta)
            run1 = config_dir / "run-1"
            run1.mkdir(exist_ok=True)
            (run1 / "grading.json").write_text(json.dumps(grading, indent=2))
            (config_dir / "grading.json").write_text(json.dumps(grading, indent=2))
            tjson = config_dir / "timing.json"
            if tjson.exists():
                (run1 / "timing.json").write_text(tjson.read_text())
            total_pass += grading["summary"]["passed"]
            total_assertions += grading["summary"]["total"]
            print(f"{ed.name}/{config}: {grading['summary']['passed']}/{grading['summary']['total']}")
    print(f"\nOverall: {total_pass}/{total_assertions} ({100*total_pass/total_assertions if total_assertions else 0:.0f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
