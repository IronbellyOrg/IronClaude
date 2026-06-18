#!/usr/bin/env python3
"""Restructure iteration-2 into aggregator/viewer layout + write grading.json.
iteration-2 set: eval-1 (run-eval-smoke, regression) + eval-3 (trust-the-pass, NEW authoritativeness).
eval-2 (create) intentionally NOT re-run: subagent nesting limits make the spec-panel/adversarial
steps uninformative; the create pipeline's real test is the top-level worked example (deliverable).
"""
import json, shutil
from pathlib import Path

IT = Path(__file__).parent / "iteration-2"

EVALS = {
    1: ("run-eval-smoke", "run-eval-smoke",
        "I want to run the eval_smoke suite from this project's eval pipeline and see the results. Walk me through selecting and supervising the run, then tell me what happened."),
    3: ("trust-the-pass", "trust-the-pass",
        "I just ran the eval_smoke suite and the summary shows 3/3 PASS, exit 0. Can I treat that as a real, trustworthy eval pass, or is there a catch I should know about?"),
}
TOOL_CALLS = {
    (1, "with_skill"): 23, (1, "without_skill"): 15,
    (3, "with_skill"): 15, (3, "without_skill"): 36,
}
GRADES = {
    1: [
        ("Re-reads the live eval contract surface and cites it before acting (fresh-context load)",
         (True, "trace cites commands.py executor lines, eval_smoke.yaml, suites-guide before acting"),
         (False, "Investigated via doctor/describe but no deliberate cited fresh-context load")),
        ("Enumerates suites via `superclaude eval list --json` (not a directory scrape)",
         (True, "`eval list --json` exit 0; eval_smoke present (v1.0, 3 evals)"),
         (True, "`superclaude eval list` showed eval_smoke (3 evals)")),
        ("Surfaces the FR-G5 exit-2 gate AND applies the empty-HOME (TMPHOME/HOME) workaround to get a result",
         (True, "Applied TMPHOME=$(mktemp -d) HOME=$TMPHOME ... -> exit 0; run dir 140645Z-4e7503b0"),
         (False, "Hit gate exit 2; declared 'editing host settings.json out of scope / no bypass flag' and did NOT apply the empty-HOME workaround -> no result")),
        ("Explains the `--no-pty` -> SKIPPED short-circuit behavior",
         (True, "Omitted --no-pty deliberately; explained all 3 evals no_pty:skip would SKIP under --no-pty"),
         (True, "Inspected describe; noted all evals no_pty:skip (CLI-smoke)")),
        ("Reports the outcome from summary.json (machine truth), not scrollback",
         (True, "Parsed summary.json: ES1/ES2/ES3 PASS, counts invariant, run-dir cited"),
         (False, "0 evals executed (gate abort); no summary.json to parse")),
        ("Honest result incl. AUTHORITATIVENESS: labels a stubbed-executor PASS NON-AUTHORITATIVE, not a real pass",
         (True, "Explicitly labeled NON-AUTHORITATIVE (plumbing only); found _NullLifecycleExecutor via --verbose; --json suppresses warning"),
         (True, "Honest the run did not execute; surfaced null executor + FR-G5 as design, modified nothing")),
    ],
    3: [
        ("Determines which executor produced the PASS (finds the non-production/_NullLifecycleExecutor)",
         (True, "Found _NullLifecycleExecutor at commands.py:1386 _resolve_executor_factory; canned exit 0"),
         (True, "Found _NullLifecycleExecutor at commands.py:1357; factory :1402; canned ObservedRun")),
        ("Explains `--json` suppresses the non-authoritative warning while `--verbose` surfaces it",
         (True, "commands.py:1879 'not as_json' guard; verified --json emitted 0 warning lines, --verbose surfaced it"),
         (True, "commands.py:1879 'and not as_json'; --json printed no warning, --verbose did")),
        ("Correct verdict: the 3/3 PASS is NON-AUTHORITATIVE / not trustworthy (plumbing pass)",
         (True, "Verdict: NON-AUTHORITATIVE plumbing only; expects:[] + duration 0.0 = canned"),
         (True, "Verdict: NOT trustworthy; vacuous PASS; expects:[] resolver not wired")),
        ("States what unblocks a real pass (M5/M6 production PTY executor) with grounded citations",
         (True, "M5/M6 ClaudeProcessAdapter+PtyDriver must replace the stub; cited commands.py lines"),
         (True, "M5/M6 production executor must replace stub in _resolve_executor_factory; cited runner.py:419 vacuous-PASS")),
    ],
}


def write_grading(eval_id, config, run_dir):
    rows = GRADES[eval_id]
    exps = [{"text": t, "passed": (ws if config == "with_skill" else wo)[0],
             "evidence": (ws if config == "with_skill" else wo)[1]} for t, ws, wo in rows]
    passed = sum(1 for e in exps if e["passed"]); total = len(exps)
    timing = json.loads((run_dir / "timing.json").read_text()) if (run_dir / "timing.json").exists() else {}
    (run_dir / "grading.json").write_text(json.dumps({
        "expectations": exps,
        "summary": {"passed": passed, "failed": total - passed, "total": total, "pass_rate": round(passed/total, 4)},
        "execution_metrics": {"total_tool_calls": TOOL_CALLS[(eval_id, config)], "errors_encountered": 0},
        "timing": {"total_duration_seconds": timing.get("total_duration_seconds", 0.0)},
    }, indent=2) + "\n")


TIMING = {
    (1, "with_skill"): (112630, 194006, 194.0), (1, "without_skill"): (95524, 195226, 195.2),
    (3, "with_skill"): (98522, 144039, 144.0), (3, "without_skill"): (117829, 272036, 272.0),
}


def main():
    for eval_id, (old, name, prompt) in EVALS.items():
        ed = IT / f"eval-{eval_id}"; ed.mkdir(parents=True, exist_ok=True)
        (ed / "eval_metadata.json").write_text(json.dumps(
            {"eval_id": eval_id, "eval_name": name, "prompt": prompt,
             "assertions": [r[0] for r in GRADES[eval_id]]}, indent=2) + "\n")
        for config in ("with_skill", "without_skill"):
            rd = ed / config / "run-1"; rd.mkdir(parents=True, exist_ok=True)
            (ed / config / "eval_metadata.json").write_text(json.dumps(
                {"eval_id": eval_id, "eval_name": name, "prompt": prompt}, indent=2) + "\n")
            tok, dms, dsec = TIMING[(eval_id, config)]
            (rd / "timing.json").write_text(json.dumps(
                {"total_tokens": tok, "duration_ms": dms, "total_duration_seconds": dsec}, indent=2) + "\n")
            old_out = IT / old / config / "outputs"
            if old_out.is_dir() and not (rd / "outputs").exists():
                shutil.move(str(old_out), str(rd / "outputs"))
            write_grading(eval_id, config, rd)
        if (IT / old).exists():
            shutil.rmtree(IT / old, ignore_errors=True)
    print("iteration-2 restructured + graded:")
    for p in sorted(IT.rglob("grading.json")):
        g = json.loads(p.read_text())["summary"]
        print(f"  {p.relative_to(IT)}: {g['passed']}/{g['total']} ({g['pass_rate']})")


if __name__ == "__main__":
    main()
