131cd9392575e251637b9ef54aca00d6cc71c5d7
Review one task for spec compliance.

Task brief:  Replace the refactor-find lens's stale command template

Depends on: Task 1

In src/superclaude/cli/swarm/lenses/refactor_find.py, change only LENS.recommended_next_command_template from /sc:code-review --apply {compare_files} to /sc:adversarial --compare {compare_files}. Keep the existing placeholder name for substitution by the caller, rather than adding a new command, new lens field or suspect-file workaround. The LENS constant is imported into src/superclaude/cli/swarm/lenses/__init__.py and copied into default JobSpecs by _build_spec_from_lens in commands.py and the default-lens expansion in preflight.py; preserve those existing flows without editing them.

Acceptance criteria:
T2.AC1: The new focused command-availability assertion from Task 1 passes against the real packaged command, with --compare verified from src/superclaude/commands/adversarial.md; --apply is absent from this lens's recommendation.
T2.AC2: LENS still declares suspect=False, stability=experimental, the same recipe/normalizer and worker settings. tests/swarm/test_bundled_lenses.py and tests/swarm/test_lens_defaults.py pass. The existing suspect coupling rule in lenses/_validate.py is unchanged and still passes.
T2.AC3: Record results in ./artifacts/lens-template.txt. The complete CLI argument-list test may still fail until Task 3; record that honestly rather than claiming the fix complete after this template-only change.
Global constraints: 
- This package is a plan only. Generating it does not authorize implementation. Execute only after the person approves execution. Do not commit, push, open a pull request, post an issue comment or launch paid/model-backed reviews.
- Limit production edits to src/superclaude/cli/swarm/lenses/refactor_find.py and the fresh-run recommendation-building block of run_cmd in src/superclaude/cli/swarm/commands.py. Use existing test files and update only the matching current documentation and wizard guidance named in Task 4 (MR-B1).
- The extra existing-review placeholder is not a separate issue to fix everywhere. Adjust refactor-find's bundled handoff only as required by the chosen consumer. Leave every other lens's recommendation, shared reducer, resume behavior, normalization, reviewer output content and success-status policy unchanged.
- Preserve refactor-find's experimental status, suspect=False, worker defaults, and absence of automatic downstream execution. Preserve explicit caller-provided templates and substitutions; do not replace custom instructions or silently validate/rewrite caller-owned inputs under this change.
- The replacement compares and combines reports, not application source. Never add a new command solely to preserve the stale recommendation. The supported command is /sc:adversarial --compare with a comma-separated list of 2-10 existing readable files, per src/superclaude/commands/adversarial.md and the active sc-adversarial-protocol skill.
- No credentials in files or logs; use environment references only. All Python/test operations use UV. Network-free stub reviewer transport is sufficient; never run the downstream adversarial skill or a model-backed swarm to satisfy these tasks.
- Diagnosis is evidence, not repaired-state acceptance. The previous diagnosis reproduced the stale instruction, but has no fix-applied positive witness. Do not relabel that historical report or clear its blocker by assertion. Task 3 must supply new observed red-to-green regression results and actual repaired CLI output.
- Keep task-owned evidence under ./artifacts/ using package-relative links. Keep intermediate evidence. Stage .dev/tasks, including this package and its artifacts, as project policy requires; staging is not a commit. Do not stage generated .claude mirrors. Final independent whole-plan review and archiving belong to the executor, not a separate task here.


Start sha: 131cd9392575e251637b9ef54aca00d6cc71c5d7
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-185337/artifacts/lens-template.txt b/.dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-185337/artifacts/lens-template.txt
new file mode 100644
index 000000000..eb0395b28
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-185337/artifacts/lens-template.txt
@@ -0,0 +1,40 @@
+========================================== test session starts ===========================================
+platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 6.1.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
+configfile: pyproject.toml
+plugins: anyio-4.16.0, superclaude-6.1.0
+collected 73 items
+
+tests/swarm/test_bundled_lenses.py .......................................................         [ 75%]
+tests/swarm/test_lens_defaults.py ..................                                               [100%]
+
+=========================================== 73 passed in 0.41s ===========================================
+
+Command: uv run --offline pytest tests/swarm/test_bundled_lenses.py tests/swarm/test_lens_defaults.py -q
+Exit status: 0
+========================================== test session starts ===========================================
+platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 6.1.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
+configfile: pyproject.toml
+plugins: anyio-4.16.0, superclaude-6.1.0
+collected 1 item
+
+tests/swarm/test_commands_run.py F                                                                 [100%]
+
+================================================ FAILURES ================================================
+___________________________________ test_refactor_find_default_handoff ___________________________________
+tests/swarm/test_commands_run.py:534: in test_refactor_find_default_handoff
+    assert tokens[2].split(",") == reports
+E   AssertionError: assert ['<existing-r...l-0.final.md'] == ['/tmp/pytest...l-0.final.md']
+E     
+E     At index 0 diff: '<existing-review>' != '/tmp/pytest-of-coder/pytest-5/test_refactor_find_default_han0/out/refactor-find-00-lens-default-model-0.final.md'
+E     Left contains one more item: '/tmp/pytest-of-coder/pytest-5/test_refactor_find_default_han0/out/refactor-find-02-lens-default-model-0.final.md'
+E     Use -v to get more diff
+======================================== short test summary info =========================================
+FAILED tests/swarm/test_commands_run.py::test_refactor_find_default_handoff - AssertionError: assert ['...
+=========================================== 1 failed in 0.40s ============================================
+
+Command: uv run --offline pytest tests/swarm/test_commands_run.py::test_refactor_find_default_handoff -q
+Exit status: 1 (expected failure until Task 3)
diff --git a/src/superclaude/cli/swarm/lenses/refactor_find.py b/src/superclaude/cli/swarm/lenses/refactor_find.py
index 560f0daab..47a772160 100644
--- a/src/superclaude/cli/swarm/lenses/refactor_find.py
+++ b/src/superclaude/cli/swarm/lenses/refactor_find.py
@@ -50,7 +50,7 @@ LENS: LensEntry = LensEntry(
     default_target_line_cap=4000,
     suspect=False,
     tier="T2-code",
-    recommended_next_command_template=("/sc:code-review --apply {compare_files}"),
+    recommended_next_command_template=("/sc:adversarial --compare {compare_files}"),
     acceptance_notes=(
         "Experimental lens; graduates to stable after a real caller "
         "wires it in production (spec §3.3)."

Codegraph context
index_state: fresh
checked_at: 2026-11-23T20:00:21Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-501-refactor-handoff
call codegraph only when index_state: fresh, never to widen scope
Rows about files changed in this run are leads only; confirm using direct reads. Q2b ran on the Grep/Read floor. The unchanged reducer and resume consumer remain outside the edit scope.

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
