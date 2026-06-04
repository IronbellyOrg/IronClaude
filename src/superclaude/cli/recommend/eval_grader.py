"""Markdown grader for the --eval pipeline.

Ported VERBATIM (logic) from `.dev/eval-workspaces/sc-recommend/grader.py` — that
scaffold is dev-only and not importable, so its `check()` (the 5 assertion types)
and `grade_run` shape are ported into the package here. All assertions are pure
text checks over a single markdown deliverable; no tool-use/transcript inspection,
no model calls, no `anthropic` import.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


def check(assertion: dict, text: str) -> tuple[bool, str]:
    """Evaluate one assertion against `text`. Ported from grader.py:11-29.

    Supported types (the entire vocabulary): string_contains, string_not_contains,
    regex_match, regex_match_not, max_length_check.
    """
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
        return bool(
            m
        ), f"regex /{v}/ {'matched: ' + repr(m.group(0)[:80]) if m else 'NO match'}"
    if t == "regex_match_not":
        m = re.search(v, text, re.DOTALL | re.MULTILINE)
        return (
            not m,
            f"regex /{v}/ {'absent (good)' if not m else 'MATCHED (bad): ' + repr(m.group(0)[:80])}",
        )
    if t == "max_length_check":
        ok = len(text) <= v
        return ok, f"length {len(text)} <= {v}? {'YES' if ok else 'NO'}"
    return False, f"unknown assertion type {t}"


def grade_text(
    *,
    eval_id: int | str,
    eval_name: str,
    configuration: str,
    assertions: list[dict],
    text: str,
    output_exists: bool = True,
) -> dict:
    """Grade `text` against `assertions`, emitting the `.dev` grading.json shape.

    Same output schema as grader.py:32-48 (`grade_run`): eval_id, eval_name,
    configuration, output_chars, output_exists, expectations[], pass_rate.
    """
    results = []
    for a in assertions:
        passed, evidence = check(a, text)
        results.append({"text": a["text"], "passed": passed, "evidence": evidence})
    return {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "configuration": configuration,
        "output_chars": len(text),
        "output_exists": output_exists,
        "expectations": results,
        "pass_rate": sum(1 for r in results if r["passed"]) / max(1, len(results)),
    }


def grade_run(run_dir: Path) -> dict:
    """Grade a single run directory (eval_metadata.json + outputs/recommendation.md).

    Ported from grader.py:32-48. The per-run metadata carries the assertions; the
    deliverable is `outputs/recommendation.md`.
    """
    meta = json.loads((run_dir / "eval_metadata.json").read_text(encoding="utf-8"))
    out = run_dir / "outputs" / "recommendation.md"
    text = out.read_text(encoding="utf-8") if out.exists() else ""
    return grade_text(
        eval_id=meta["eval_id"],
        eval_name=meta["eval_name"],
        configuration=meta["configuration"],
        assertions=meta.get("assertions", []),
        text=text,
        output_exists=out.exists(),
    )
