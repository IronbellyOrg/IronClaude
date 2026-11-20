359bc66587289814eea8cf025f34a2ef5bf47440
Review one task for spec compliance.

Task brief: ## Task 3: Create the routing rule as a tested script

Create `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` with a pure function `route(blocking, label_high, medium, regenerated_already=False, forced=None)` and a `route` command-line subcommand that prints one JSON object `{"route": ..., "forced": ...}`. Rows in order, first match wins: blocking equals 0 gives `none`; blocking at most 3 and label_high at most 5 and medium at most 9 gives `surgical`; otherwise `regenerate`; a `regenerate` result when `regenerated_already` is true gives `escalate`. `forced` (`none`, `surgical` or `regenerate`) overrides and is recorded as forced, except that a forced `regenerate` with `regenerated_already` true still gives `escalate`. Reject negative or non-integer counts with a non-zero exit. Create `tests/skills/test_workflow_remediation.py` (style of `tests/skills/test_workflow_archive.py`, which loads a script by file path) with the route tests.

Acceptance criteria:
- Parametrized tests cover the boundaries blocking 3/4, label_high 5/6, medium 9/10, blocking 0 with label_high 20 and medium 30 (route `none`), a forced route, the second regenerate (`escalate`), and a forced `regenerate` after a first regenerate (`escalate`).
- `uv run pytest tests/skills/test_workflow_remediation.py -q` passes.
Global constraints: ## Constraints

- The design is `docs/designs/surgical-remediation.md`. Where it disagrees with `.dev/issues/624/accuracy-check.md` or `.dev/issues/624/analysis/analyze-sc-workflow-protocol.md`, those two files win: the reflect bump has consumers, the workflow package contract stays at `contract_version: "1.1"`, and seven packages (not four) are migrated. Anchor edits by text, not by the line numbers of the design (they moved).
- Edit only `src/superclaude/` sources, `tests/`, `scripts/`, `plugins/superclaude/` copies of the edited files (including the new `refs/remediation.md` and `scripts/remediate.py` of the workflow skill, which the plugin mirror must carry (the `diff -rq` checks of Task 6 require it), and `plugins/superclaude/commands/workflow.md`), `.dev/README.md` and the data migration. Never hand-edit the dev copies under the project `.claude/` folder; after each task that changes a primitive run `make sync-dev` and then `make verify-sync`.
- Installed primitives never point at a `src/superclaude/...` path. In every edited skill, command or core doc, name other primitives by their installed path (`~/.claude/skills/<name>/SKILL.md`) and name the project `.claude/` copy second.
- Where a file in `plugins/superclaude/` mirrors an edited file (the workflow and implement protocols and `commands/workflow.md`), keep the mirror byte-identical to the `src/` file (`diff -rq` shows no difference); a new file in an already mirrored folder is mirrored too. `remediate.py` uses only the Python standard library (installed skill scripts run under `uv run --no-project`) and edits archived contracts by appending lines, never by loading and re-writing the YAML.
- Decision made by this plan because the design leaves it open: `finding_counts.label_high` counts the Deviations-table label HIGH on the legacy reviewer path, and counts findings-v2 severity CRITICAL on the shadow-panel path (the panel has no HIGH label). `blocking`, `medium` and `note` count the grades `Blocking (...)`, `Medium:` and `Note:` (or the panel's `blocking` flag). On the panel path, `medium` counts findings-v2 severity MAJOR with `blocking` false and `note` counts severity MINOR.
- The workflow package contract adds only additive fields under `contract_version: "1.1"`: `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`. `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` keep accepting only "1.1".
- Only blocking findings are ever repaired. No fix pass touches text for a Medium or Note finding.
- Out of scope: the wording of the review severity rule, reviewer models, `/sc:design`, `/sc:brainstorm`, `/sc:spec-panel`'s own loop, deleting archived packages, and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (reused as written).
- Reflect's own `--remediate` plan route keeps calling `sc:workflow`; `src/superclaude/cli/reflect/runner.py` gets no code change (its fail-closed handling of a non-zero apply already covers a refused package).
Start sha: 359bc66587289814eea8cf025f34a2ef5bf47440
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py b/src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py
new file mode 100644
index 000000000..06185407f
--- /dev/null
+++ b/src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py
@@ -0,0 +1,64 @@
+#!/usr/bin/env python3
+"""Surgical-remediation helper for /sc:workflow (standard library only)."""
+
+import argparse
+import json
+import sys
+
+ROUTES = ("none", "surgical", "regenerate")
+
+
+def route(blocking, label_high, medium, regenerated_already=False, forced=None):
+    """Return (route, forced). Rows in order, first match wins."""
+    for name, v in (("blocking", blocking), ("label_high", label_high), ("medium", medium)):
+        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
+            raise ValueError(f"{name} must be a non-negative integer, got {v!r}")
+    if forced is not None and forced not in ROUTES:
+        raise ValueError(f"forced must be one of {ROUTES}, got {forced!r}")
+    if forced is not None:
+        result = forced
+    elif blocking == 0:
+        result = "none"
+    elif blocking <= 3 and label_high <= 5 and medium <= 9:
+        result = "surgical"
+    else:
+        result = "regenerate"
+    if result == "regenerate" and regenerated_already:
+        result = "escalate"
+    return result, forced is not None
+
+
+def _count(text):
+    try:
+        v = int(text)
+    except ValueError:
+        raise argparse.ArgumentTypeError(f"not an integer: {text!r}")
+    if v < 0:
+        raise argparse.ArgumentTypeError(f"negative count: {v}")
+    return v
+
+
+def _cmd_route(args):
+    r, forced = route(
+        args.blocking, args.label_high, args.medium, args.regenerated_already, args.forced
+    )
+    print(json.dumps({"route": r, "forced": forced}))
+    return 0
+
+
+def main(argv=None):
+    p = argparse.ArgumentParser(prog="remediate.py")
+    sub = p.add_subparsers(dest="command", required=True)
+    r = sub.add_parser("route", help="print the remediation route as JSON")
+    r.add_argument("--blocking", type=_count, required=True)
+    r.add_argument("--label-high", type=_count, required=True)
+    r.add_argument("--medium", type=_count, required=True)
+    r.add_argument("--regenerated-already", action="store_true")
+    r.add_argument("--forced", choices=ROUTES, default=None)
+    r.set_defaults(func=_cmd_route)
+    args = p.parse_args(argv)
+    return args.func(args)
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/skills/test_workflow_remediation.py b/tests/skills/test_workflow_remediation.py
new file mode 100644
index 000000000..02dfcc2ca
--- /dev/null
+++ b/tests/skills/test_workflow_remediation.py
@@ -0,0 +1,76 @@
+"""Tests for the /sc:workflow remediation routing script."""
+
+import importlib.util
+import json
+import subprocess
+import sys
+from pathlib import Path
+
+import pytest
+
+_SCRIPT = (
+    Path(__file__).resolve().parents[2]
+    / "src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py"
+)
+_spec = importlib.util.spec_from_file_location("remediate", _SCRIPT)
+rm = importlib.util.module_from_spec(_spec)
+_spec.loader.exec_module(rm)
+
+
+@pytest.mark.parametrize(
+    "args,kwargs,expected",
+    [
+        ((0, 0, 0), {}, ("none", False)),
+        ((0, 20, 30), {}, ("none", False)),
+        ((3, 0, 0), {}, ("surgical", False)),
+        ((4, 0, 0), {}, ("regenerate", False)),
+        ((1, 5, 0), {}, ("surgical", False)),
+        ((1, 6, 0), {}, ("regenerate", False)),
+        ((1, 0, 9), {}, ("surgical", False)),
+        ((1, 0, 10), {}, ("regenerate", False)),
+        ((4, 0, 0), {"regenerated_already": True}, ("escalate", False)),
+        ((1, 0, 0), {"forced": "regenerate"}, ("regenerate", True)),
+        ((5, 0, 0), {"forced": "surgical"}, ("surgical", True)),
+        ((2, 0, 0), {"forced": "none"}, ("none", True)),
+        (
+            (1, 0, 0),
+            {"forced": "regenerate", "regenerated_already": True},
+            ("escalate", True),
+        ),
+        ((1, 0, 0), {"forced": "surgical", "regenerated_already": True}, ("surgical", True)),
+    ],
+)
+def test_route(args, kwargs, expected):
+    assert rm.route(*args, **kwargs) == expected
+
+
+@pytest.mark.parametrize("bad", [-1, 1.5, "2", True])
+def test_route_rejects_bad_counts(bad):
+    with pytest.raises(ValueError):
+        rm.route(bad, 0, 0)
+
+
+def _run(*args):
+    return subprocess.run(
+        [sys.executable, str(_SCRIPT), *args], capture_output=True, text=True
+    )
+
+
+def test_cli_prints_json():
+    p = _run("route", "--blocking", "2", "--label-high", "1", "--medium", "0")
+    assert p.returncode == 0
+    assert json.loads(p.stdout) == {"route": "surgical", "forced": False}
+
+
+def test_cli_forced_and_escalate():
+    p = _run(
+        "route", "--blocking", "1", "--label-high", "0", "--medium", "0",
+        "--forced", "regenerate", "--regenerated-already",
+    )
+    assert json.loads(p.stdout) == {"route": "escalate", "forced": True}
+
+
+@pytest.mark.parametrize("bad", ["-1", "x", "1.5"])
+def test_cli_rejects_bad_counts(bad):
+    p = _run("route", "--blocking", bad, "--label-high", "0", "--medium", "0")
+    assert p.returncode != 0


Codegraph context: index_state: fresh; checked_at: 2026-11-20T02:48:46Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
call codegraph only when index_state: fresh, never to widen scope
(Q2b dependents not in the diff: none recorded; Grep/Read floor used.)
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
