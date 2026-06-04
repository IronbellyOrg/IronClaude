#!/usr/bin/env python3
"""Grade recommendation.md outputs against eval_metadata.json assertions."""
import json
import re
import sys
from pathlib import Path

ITERATION = Path(__file__).parent / "iteration-1"


def check(assertion: dict, text: str) -> tuple[bool, str]:
    t = assertion.get("type", "")
    v = assertion.get("value", "")
    if t == "string_contains":
        ok = v in text
        return ok, f"substring {v!r} {'found' if ok else 'NOT found'}"
    if t == "string_not_contains":
        ok = v not in text
        return ok, f"substring {v!r} {'absent (good)' if ok else 'PRESENT (bad)'}"
    if t == "regex_match":
        m = re.search(v, text, re.DOTALL | re.MULTILINE)
        return bool(m), f"regex /{v}/ {'matched: ' + repr(m.group(0)[:80]) if m else 'NO match'}"
    if t == "regex_match_not":
        m = re.search(v, text, re.DOTALL | re.MULTILINE)
        return not m, f"regex /{v}/ {'absent (good)' if not m else 'MATCHED (bad): ' + repr(m.group(0)[:80])}"
    if t == "max_length_check":
        ok = len(text) <= v
        return ok, f"length {len(text)} <= {v}? {'YES' if ok else 'NO'}"
    return False, f"unknown assertion type {t}"


def grade_run(run_dir: Path) -> dict:
    meta = json.loads((run_dir / "eval_metadata.json").read_text())
    out = run_dir / "outputs" / "recommendation.md"
    text = out.read_text() if out.exists() else ""
    results = []
    for a in meta.get("assertions", []):
        passed, evidence = check(a, text)
        results.append({"text": a["text"], "passed": passed, "evidence": evidence})
    return {
        "eval_id": meta["eval_id"],
        "eval_name": meta["eval_name"],
        "configuration": meta["configuration"],
        "output_chars": len(text),
        "output_exists": out.exists(),
        "expectations": results,
        "pass_rate": sum(1 for r in results if r["passed"]) / max(1, len(results)),
    }


def main():
    summary = []
    for eval_dir in sorted(ITERATION.glob("eval-*")):
        for cfg in ("with_skill", "without_skill"):
            run = eval_dir / cfg
            if not (run / "eval_metadata.json").exists():
                continue
            g = grade_run(run)
            (run / "grading.json").write_text(json.dumps(g, indent=2) + "\n")
            summary.append(
                f"{eval_dir.name}/{cfg}: {sum(1 for r in g['expectations'] if r['passed'])}/"
                f"{len(g['expectations'])} pass ({g['pass_rate']*100:.0f}%)"
            )
    print("\n".join(summary))


if __name__ == "__main__":
    main()
