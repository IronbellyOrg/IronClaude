ef4a41497b1b15ceb20f16a84cf71b7ab8be8b5c
Review one task for spec compliance.

Task brief: ## Task 5: Add regression tests in tests/skills/test_codegraph_adoption.py and tests/core/test_codegraph_guide.py

Depends on: Task 3, Task 4

In `tests/skills/test_codegraph_adoption.py` add tests that read `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md` and `src/superclaude/core/CODEGRAPH.md` and assert, each with its own test or parametrized case and a message naming the missing clause: the pgrep wait clause with `60 s` (guide and both commands); `path` on the `codegraph_files` call (guide, analyze, design); `date -u +%Y-%m-%dT%H:%M:%SZ` (guide, analyze, design); the quick-depth sentence (analyze); the top-level `"codegraph"` JSON field rule (analyze) and the first-comment-or-caption rule (design); the Validate-row "not already run" wording (design); "before the first codegraph call" (analyze and design). In `tests/core/test_codegraph_guide.py` extend `test_guide_names_switches_and_status_guard` (or add one test) so the guide must still say rule 7 no longer claims the MCP status "needs no guard". Then run the full check set and record one mutant: remove the pgrep/wait clause from `src/superclaude/commands/analyze.md` in a scratch copy of the test run (restore it afterwards) and show the new test failing; write that output to `./artifacts/mutant-analyze-pgrep.log`.

Acceptance criteria:
- Each new assertion fails when its clause is removed (mutant evidence in `./artifacts/mutant-analyze-pgrep.log`) and passes on the edited files.
- `uv run pytest tests/skills/test_codegraph_adoption.py tests/commands tests/agents tests/cli/eval tests/core/test_codegraph_guide.py -q` passes, plus any other test file that greps analyze.md, design.md or CODEGRAPH.md (found with a grep of `tests/` and `scripts/`).
- `make sync-dev` then `make verify-sync` pass; `uv run ruff check src tests scripts` passes and `uv run ruff format --check` passes on the touched Python files.
- `git diff --stat` lists only the permitted files, and `grep -rn 'src/superclaude' src/superclaude/commands/analyze.md src/superclaude/commands/design.md src/superclaude/core/CODEGRAPH.md` shows no new read path.

AC ids:
T5.AC1: Each new assertion fails when its clause is removed (mutant evidence in `./artifacts/mutant-analyze-pgrep.log`) and passes on the edited files.
T5.AC2: `uv run pytest tests/skills/test_codegraph_adoption.py tests/commands tests/agents tests/cli/eval tests/core/test_codegraph_guide.py -q` passes, plus any other test file that greps analyze.md, design.md or CODEGRAPH.md (found with a grep of `tests/` and `scripts/`).
T5.AC3: `make sync-dev` then `make verify-sync` pass; `uv run ruff check src tests scripts` passes and `uv run ruff format --check` passes on the touched Python files.
T5.AC4: `git diff --stat` lists only the permitted files, and `grep -rn 'src/superclaude' src/superclaude/commands/analyze.md src/superclaude/commands/design.md src/superclaude/core/CODEGRAPH.md` shows no new read path.
Global constraints: - Edit only `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md`, `src/superclaude/core/CODEGRAPH.md`, `plugins/superclaude/core/CODEGRAPH.md` (a test pins it byte-identical to the source), `tests/skills/test_codegraph_adoption.py` and `tests/core/test_codegraph_guide.py`. The plugin twins of analyze.md and design.md already differ from the source (no codegraph text, `mcp-servers: []`) and no test pins them, so they stay untouched. `scripts/eval_workflow_vs_task_builder.py` pins skill tool lists, which this plan does not change, so it stays untouched unless a test run shows otherwise.
- Do not change behaviour, flags, the one-check-per-run rule, the fresh-and-`access: mcp` rule, the Grep/Read floor or the never-halt rule. Every fix is a clause or one sentence.
- `src/superclaude/core/CODEGRAPH.md` is shared by every primitive: additive clarifications only; it stays at 120 lines or fewer, names no `src/superclaude/` path, adds no `graph:*` token outside the closed list of its section 3 (which already holds `graph:empty` and `graph:truncated`), and names `explore` and the mutating verbs only in its Never section. Each phrase changed is grepped across `src/superclaude` first so no other primitive contradicts it.
- Reference the smoke report only through `./source.md`; never add a `src/superclaude` read path to an installed primitive. Never stage `.claude/`; no commit, no push, no PR.
- All nine report quotes were re-verified against the worktree before planning: the quotes sit at the stated lines of analyze.md (30, 32, 36, 63, 67), design.md (55, 57, 61, 65, 74) and CODEGRAPH.md (13, 22, 50, 74). None is rebutted.
Start sha: ef4a41497b1b15ceb20f16a84cf71b7ab8be8b5c
Diff against the start snapshot: 
diff --git a/tests/skills/test_codegraph_adoption.py b/tests/skills/test_codegraph_adoption.py
index 5cfe9d44e..a246620a3 100644
--- a/tests/skills/test_codegraph_adoption.py
+++ b/tests/skills/test_codegraph_adoption.py
@@ -292,3 +292,97 @@ def test_analyze_gates_codegraph_on_access_as_well_as_index_state():
     text = _text(_SRC / "commands" / "analyze.md")
     assert "`access: mcp`" in text
     assert "`access: none`" in text and "Glob, Grep and Read" in text
+
+
+_GUIDE = _SRC / "core" / "CODEGRAPH.md"
+_ANALYZE = _SRC / "commands" / "analyze.md"
+_DESIGN = _SRC / "commands" / "design.md"
+_DATE_CMD = "date -u +%Y-%m-%dT%H:%M:%SZ"
+_WAIT_CMD = "waits up to 60 s for a running `init` or `index`"
+_FILES_PATH = 'codegraph_files {format:"grouped", maxDepth:2, path}'
+
+# Each clause fixes one wording ambiguity that the analyze/design smoke test found, so
+# putting the old wording back fails exactly the case named by its id.
+_WORDING_PINS = [
+    pytest.param(_GUIDE, "call it once with `projectPath`", id="guide-one-status-call"),
+    pytest.param(
+        _GUIDE,
+        "wait for that build to end (poll up to 60 s)",
+        id="guide-waits-for-running-build",
+    ),
+    pytest.param(
+        _GUIDE,
+        "if it is still running after 60 s, skip `status`, "
+        "set `index_state: stale` and token `graph:stale`",
+        id="guide-stale-after-60s",
+    ),
+    pytest.param(
+        _GUIDE,
+        "the MCP `codegraph_status` takes the bounded wait of section 2 step 3",
+        id="guide-rule7-mcp-wait",
+    ),
+    pytest.param(_GUIDE, _DATE_CMD, id="guide-checked-at-source"),
+    pytest.param(_GUIDE, "maxDepth:2, path?}", id="guide-files-path"),
+    pytest.param(_GUIDE, "records `graph:empty` the same way", id="guide-lookup-token"),
+    pytest.param(_ANALYZE, _WAIT_CMD, id="analyze-waits-for-running-build"),
+    pytest.param(_ANALYZE, _DATE_CMD, id="analyze-checked-at-source"),
+    pytest.param(_ANALYZE, _FILES_PATH, id="analyze-files-path"),
+    pytest.param(
+        _ANALYZE,
+        "`codegraph_search` only when the target names a symbol",
+        id="analyze-directory-target",
+    ),
+    pytest.param(
+        _ANALYZE,
+        "`includeCode:true` only for symbols Discover found",
+        id="analyze-bodies-after-discover",
+    ),
+    pytest.param(
+        _ANALYZE,
+        "at `--depth quick`, a line found by Grep need not be re-Read, "
+        "but a graph row cited as a finding is still confirmed by Grep or Read",
+        id="analyze-quick-depth",
+    ),
+    pytest.param(_ANALYZE, "`graph:empty`", id="analyze-lookup-token"),
+    pytest.param(
+        _ANALYZE,
+        'top-level `"codegraph"` string field',
+        id="analyze-json-field",
+    ),
+    pytest.param(
+        _ANALYZE,
+        "read it before the first codegraph call",
+        id="analyze-read-guide-first",
+    ),
+    pytest.param(_DESIGN, _WAIT_CMD, id="design-waits-for-running-build"),
+    pytest.param(_DESIGN, _DATE_CMD, id="design-checked-at-source"),
+    pytest.param(_DESIGN, _FILES_PATH, id="design-files-path"),
+    pytest.param(
+        _DESIGN,
+        "`codegraph_impact` only if it was not already run "
+        "for the same symbol in Plan or Design",
+        id="design-validate-impact-once",
+    ),
+    pytest.param(_DESIGN, "`graph:empty`", id="design-lookup-token"),
+    pytest.param(
+        _DESIGN,
+        "first comment line or a caption line",
+        id="design-code-diagram-line",
+    ),
+    pytest.param(
+        _DESIGN,
+        "read before the first codegraph call",
+        id="design-read-guide-first",
+    ),
+]
+
+
+@pytest.mark.parametrize(("path", "clause"), _WORDING_PINS)
+def test_codegraph_wording_clause_is_present(path, clause):
+    assert clause in _text(path), f"{_rel(path)} lost the clause: {clause}"
+
+
+def test_old_ambiguous_codegraph_wording_is_gone():
+    assert "needs no guard" not in _text(_GUIDE)
+    assert "read it when you use codegraph" not in _text(_ANALYZE)
+    assert "to locate the target's symbols" not in _text(_ANALYZE)
diff --git a/tests/core/test_codegraph_guide.py b/tests/core/test_codegraph_guide.py
index 7fc9fde62..b54470daa 100644
--- a/tests/core/test_codegraph_guide.py
+++ b/tests/core/test_codegraph_guide.py
@@ -107,6 +107,7 @@ def test_guide_names_switches_and_status_guard():
     assert "SUPERCLAUDE_CODEGRAPH_PRIMITIVES" in text
     assert "SUPERCLAUDE_CODEGRAPH_AUTOINIT" in text
     assert "pgrep -f" in text
+    assert "60 s" in text, "guide lost the bounded wait for a running init/index"
 
 
 def test_guide_holds_sentinel_and_no_source_path():

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
