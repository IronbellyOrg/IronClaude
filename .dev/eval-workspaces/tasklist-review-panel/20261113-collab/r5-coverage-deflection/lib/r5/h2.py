"""H2: truncate over-long anchors and claims, parse with the real findings-v1 parser, decide on one re-ask (DESIGN 2.6; R-02, R-28)."""
import json
import sys

# The merge runs the installed superclaude tool; pins-check.sh (D10) refuses a launch when these
# worktree files differ from the installed copies, so this parser is the merge's parser.
from superclaude.cli.review.findings import (
    _HEAD_FINDINGS,
    _blocks_after,
    flat,
    parse_block,
)

LIMITS = {"anchor": 200, "anchor2": 200, "claim": 300}


def cut(s: str, limit: int) -> str:
    """Longest prefix of s whose whitespace-flattened length is at most limit."""
    if len(flat(s)) <= limit:
        return s
    lo, hi = 0, len(s)
    while lo < hi:  # flat(s[:i]) grows monotonically with i
        mid = (lo + hi + 1) // 2
        if len(flat(s[:mid])) <= limit:
            lo = mid
        else:
            hi = mid - 1
    return s[:lo].rstrip()


def normalise(report_text: str) -> tuple[str, list[dict]]:
    found, blocks = _blocks_after(report_text, _HEAD_FINDINGS, "findings-v1")
    if found and blocks:
        lines = report_text.split("\n")
        for lineno, raw in blocks[-1][1]:
            try:
                obj = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(obj, dict) or "prior" in obj:
                continue
            changed = False
            for key, limit in LIMITS.items():
                v = obj.get(key)
                if isinstance(v, str) and len(flat(v)) > limit:
                    obj[key] = cut(v, limit)
                    changed = True
            if changed:
                lines[lineno - 1] = json.dumps(obj, ensure_ascii=False)
        report_text = "\n".join(lines)
    return report_text, parse_block(report_text)["errors"]


def reask_prompt(errors: list[dict]) -> str:
    listed = "\n".join(f"- line {e['line']}: {e['msg']}" for e in errors)
    return (
        "The findings block of your report has these parser errors:\n"
        f"{listed}\n"
        "Return the complete corrected report: the full report text, the '## Findings block' heading with exactly one "
        "fenced findings-v1 block (one JSON object per line: id, severity CRITICAL|MAJOR|MINOR, blocking, category "
        "contradiction|unpassable-check|data-loss|safety|missing-requirement|other, anchor = 12 to 200 characters "
        "copied exactly from the candidate, optional anchor2, refs (at most 8 strings), claim of at most 300 "
        "characters; a MINOR finding is never blocking), then the final 'verdict: PASS' or 'verdict: FAIL' line. "
        "Your reply must be the complete report text."
    )


def decide(orig_errors: list, reask_errors: list, reask_model_ok: bool, reask_api_error: bool) -> tuple[bool, str]:
    """(use the re-ask report, reason)."""
    if not reask_model_ok:
        return False, "reask_model_mismatch"
    if reask_api_error:
        return False, "reask_api_error"
    if len(reask_errors) < len(orig_errors):
        return True, "fewer_errors"
    return False, "not_fewer_errors"


def main(argv: list[str]) -> int:
    cmd = argv[0]
    if cmd == "normalise":  # normalise <in.md> <out.md>: prints the remaining errors as JSON
        text, errors = normalise(open(argv[1], encoding="utf-8", errors="replace").read())
        open(argv[2], "w", encoding="utf-8").write(text)
        print(json.dumps(errors))
    elif cmd == "reask-prompt":  # reask-prompt <errors.json>
        print(reask_prompt(json.load(open(argv[1]))))
    elif cmd == "decide":  # decide <orig_errors.json> <reask_errors.json> <model_ok> <api_error>
        use, why = decide(json.load(open(argv[1])), json.load(open(argv[2])), argv[3] == "true", argv[4] == "true")
        print(f"{'reask' if use else 'orig'} {why}")
    else:
        print(f"unknown command {cmd}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
