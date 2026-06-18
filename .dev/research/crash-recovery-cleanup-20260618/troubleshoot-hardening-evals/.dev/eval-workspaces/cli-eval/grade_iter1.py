#!/usr/bin/env python3
"""Restructure iteration-1 into the aggregator/viewer layout and write grading.json.

Target layout (satisfies aggregate_benchmark.py glob + generate_review.py walk):
  iteration-1/eval-<n>/eval_metadata.json
  iteration-1/eval-<n>/<config>/eval_metadata.json        (viewer: run_dir.parent)
  iteration-1/eval-<n>/<config>/run-1/{outputs/, timing.json, grading.json}

Grades are authored from the on-disk traces/reports read during the session.
"""
import json
import shutil
from pathlib import Path

IT = Path(__file__).parent / "iteration-1"

# (old descriptive dir, eval-id, eval_name, prompt)
EVALS = {
    1: ("run-eval-smoke", "run-eval-smoke",
        "I want to run the eval_smoke suite from this project's eval pipeline and see the results. Walk me through selecting and supervising the run, then tell me what happened."),
    2: ("create-doc-parity-suite", "create-doc-parity-suite",
        "Author a new eval suite for this project that checks the documented `superclaude eval run` flags stay in sync with `superclaude eval run --help`. Set it up properly and make sure it's actually valid."),
    3: ("inspect-suite-safety", "inspect-suite-safety",
        "Before I run the installer_sync_drift eval suite, show me what's inside it and tell me whether running it with --no-pty will actually exercise anything."),
}

# tool_uses captured from subagent notifications
TOOL_CALLS = {
    (1, "with_skill"): 22, (1, "without_skill"): 16,
    (2, "with_skill"): 21, (2, "without_skill"): 28,
    (3, "with_skill"): 15, (3, "without_skill"): 12,
}

# expectations: text, with_skill (passed, evidence), without_skill (passed, evidence)
GRADES = {
    1: [
        ("Re-reads the live eval contract surface and cites it before acting (fresh-context load)",
         (True, "trace.md cites commands.py, exit_codes.py, artifact_layout.py, models.py, eval_smoke.yaml, suites-guide before acting"),
         (False, "Discovered the surface via `eval --help` only; no file:line contract citations / no deliberate fresh-context load")),
        ("Enumerates suites via `superclaude eval list --json` (not a directory scrape)",
         (True, "report.md: `eval list --json` -> exit 0; eval_smoke present (v1.0, 3 evals)"),
         (True, "report.md step 2: `superclaude eval list` showed eval_smoke (3 evals)")),
        ("Surfaces the FR-G5 exit-2 coverage gate AND applies the empty-HOME (TMPHOME/HOME) workaround to get a result",
         (True, "report.md lines 9-14: gate fired exit 2; TMPHOME=$(mktemp -d) HOME=$TMPHOME workaround cleared it -> exit 0"),
         (False, "Hit the gate (exit 2) but did NOT apply the workaround; concluded it 'would require write access' / a different host -> no result obtained")),
        ("Explains the `--no-pty` -> SKIPPED short-circuit behavior",
         (True, "report.md line 15: all 3 evals no_pty:skip so --no-pty short-circuits the whole suite to SKIPPED (not a pass)"),
         (True, "report.md step #3 'to actually get green': not --no-pty, which would skip the suite")),
        ("Reports the outcome from summary.json (machine truth), not scrollback",
         (True, "report.md lines 17-25: parsed on-disk summary.json at .dev/eval-runs/2026-06-12/134335Z-07aca9f1/ (3/3 PASS, counts invariant)"),
         (False, "0 evals executed; run aborted at the gate so there was no summary.json to parse")),
        ("Honest result: does not call a SKIPPED/failed run a pass; surfaces the M2 _NullLifecycleExecutor non-authoritative caveat",
         (True, "report.md lines 27-33: explicitly flags _NullLifecycleExecutor canned-PASS; 'NOT yet an authoritative eval pass'"),
         (True, "report.md lines 38, 44: surfaces null executor at M2 and that nothing was modified to 'make it pass'")),
    ],
    2: [
        ("Re-reads the suite schema + house-style templates + CLI surface and cites them (fresh-context load)",
         (True, "trace cites `eval run --help` (12 flags + --suite [required]), suite.schema.json, eval_smoke.yaml, installer_sync_drift.yaml, suites/README.md"),
         (True, "Engaged the schema/loader directly: ran loader.validate_manifest() and Expect.from_mapping to ground the manifest shape")),
        ("Routes critique + debate/merge through the reused skills (/sc:spec-panel, /sc:adversarial) rather than reinventing them",
         (True, "Described W2 /sc:spec-panel --mode critique and W3 /sc:adversarial --generate eval-suite --agents opus,sonnet,haiku with a merge verdict (variant B)"),
         (False, "No critique/debate step at all; authored a single design unaided (the reuse pipeline is the skill's contribution)")),
        ("Authors the manifest schema-first in house style: stem == name, only schema-known keys, meaningful expects (not bare exit_code:0)",
         (True, "eval_cli_doc_parity.yaml: stem==name, 3 evals DP1/DP2/DP3, positive substring per documented flag + [required] guard"),
         (True, "doc_flag_parity.yaml: stem==name, 2 evals, bidirectional flag diff with IN_SYNC/DRIFT verdict")),
        ("Validates with `superclaude eval describe --suite <stem>` to loader exit 0 before declaring done",
         (True, "`eval describe --suite eval_cli_doc_parity` -> exit 0; also appears in `eval list --json` (eval_count 3)"),
         (True, "`eval describe --suite doc_flag_parity` -> exit 0; `eval list` shows '2 evals'; loader.validate_manifest passed")),
        ("Does not invent schema fields / CLI flags",
         (True, "Only schema-known keys; validated clean on first pass (no fix loop)"),
         (True, "Validated four ways; no schema violations reported")),
    ],
    3: [
        ("Inspects the suite via `superclaude eval describe` (through the CLI)",
         (True, "trace: `eval describe --suite installer_sync_drift` exit 0; corroborated against the yaml"),
         (True, "trace: `eval describe --suite installer_sync_drift` exit 0; `eval list --json` confirms eval_count 1")),
        ("Reports isolation strategy (shared HOME), timeouts, and the no_pty markers",
         (True, "report: home_strategy shared, timeout_sec 180, no_pty:skip on S1, hard binaries listed"),
         (True, "report: home_strategy=shared, timeout_sec=180, no_pty:skip on S1, all 4 hard binaries")),
        ("Correct --no-pty verdict: it short-circuits S1 to SKIPPED and exercises nothing; real run omits --no-pty (+ FR-G5 workaround)",
         (True, "Verdict: --no-pty exercises NOTHING (SKIPPED, skip_reason=--no-pty); real run omits --no-pty and clears FR-G5 via empty-HOME workaround"),
         (True, "Verdict: running with --no-pty exercises NOTHING; cited commands.py:1894 short-circuit; real run on default PTY path")),
        ("Grounds flag/behavior claims in re-read sources, not memory",
         (True, "Cites suite.schema.json:153-157, run-pipeline.md:33-35, suites-guide.md:549-554"),
         (True, "Cites installer_sync_drift.yaml:57, suite.schema.json:153-157, commands.py:1894")),
    ],
}


def write_grading(eval_id, config, run_dir):
    rows = GRADES[eval_id]
    exps = []
    for text, ws, wo in rows:
        passed, evidence = (ws if config == "with_skill" else wo)
        exps.append({"text": text, "passed": passed, "evidence": evidence})
    passed = sum(1 for e in exps if e["passed"])
    total = len(exps)
    timing = json.loads((run_dir / "timing.json").read_text()) if (run_dir / "timing.json").exists() else {}
    grading = {
        "expectations": exps,
        "summary": {"passed": passed, "failed": total - passed, "total": total,
                     "pass_rate": round(passed / total, 4)},
        "execution_metrics": {"total_tool_calls": TOOL_CALLS[(eval_id, config)],
                               "errors_encountered": 0},
        "timing": {"total_duration_seconds": timing.get("total_duration_seconds", 0.0)},
    }
    (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")


def main():
    for eval_id, (old_name, eval_name, prompt) in EVALS.items():
        eval_dir = IT / f"eval-{eval_id}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        # eval-level metadata (aggregator reads eval_id here)
        (eval_dir / "eval_metadata.json").write_text(json.dumps(
            {"eval_id": eval_id, "eval_name": eval_name, "prompt": prompt,
             "assertions": [r[0] for r in GRADES[eval_id]]}, indent=2) + "\n")
        for config in ("with_skill", "without_skill"):
            old_cfg = IT / old_name / config
            new_cfg = eval_dir / config
            run_dir = new_cfg / "run-1"
            run_dir.mkdir(parents=True, exist_ok=True)
            # config-level metadata (viewer reads from run_dir.parent)
            (new_cfg / "eval_metadata.json").write_text(json.dumps(
                {"eval_id": eval_id, "eval_name": eval_name, "prompt": prompt}, indent=2) + "\n")
            # move outputs/ and timing.json into run-1/
            if (old_cfg / "outputs").is_dir() and not (run_dir / "outputs").exists():
                shutil.move(str(old_cfg / "outputs"), str(run_dir / "outputs"))
            if (old_cfg / "timing.json").exists() and not (run_dir / "timing.json").exists():
                shutil.move(str(old_cfg / "timing.json"), str(run_dir / "timing.json"))
            write_grading(eval_id, config, run_dir)
        # remove now-empty old tree
        if (IT / old_name).exists():
            shutil.rmtree(IT / old_name, ignore_errors=True)
    print("restructured + graded:")
    for p in sorted(IT.rglob("grading.json")):
        g = json.loads(p.read_text())["summary"]
        print(f"  {p.relative_to(IT)}: {g['passed']}/{g['total']} ({g['pass_rate']})")


if __name__ == "__main__":
    main()
