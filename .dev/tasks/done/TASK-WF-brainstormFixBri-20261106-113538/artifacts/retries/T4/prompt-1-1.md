6096d08673e4eb8c4ab698e6a63b483a1e11d732
Review one task for spec compliance.

Task brief: ## Task 4: Pin the skill and routing-ref wording in test_brainstorm_protocol.py

Depends on: Task 1, Task 2

In `tests/skills/test_brainstorm_protocol.py`, the test `test_brainstorm_unattended_nested_directories_are_named` starts at line 39. It asserts `nested/analyze-` and `skipped` in the Wave 2A section (`_wave2a_section()`, line 44) and `nested/adversarial-` in `refs/handoff-routing.md` (line 47). Keep every existing assertion unchanged. Add a sibling test next to it, using the file's own helpers (`_wave2a_section`, `_BRAINSTORM`) and, for the routing ref, the slicing pattern of the `_section(text, start, end_pattern)` helper in `tests/skills/test_codegraph_adoption.py` (it splits the text at `start`, then splits the rest at `end_pattern` with `re.M` and keeps the first part). The new test asserts:

- Paragraph slice: take `_wave2a_section()`, split at the bold lead-in ``**Under `--unattended`**``, and keep the text up to the next blank line. The slice contains `fallback_1`, `write no nested directory and no nested contract` and ``only by a `/sc:analyze` call``, and the text `Quality-tier tracking` is not in it, so a slicer that returns the whole section fails.
- Tier slices of `refs/handoff-routing.md` (the file next to the SKILL file): the Tier 1 slice runs from the first `**Tier 1 (primary)**` to the line starting `**Tier 2 (fallback_1)**: codegraph`; the Tier 2 slice runs from there to the line starting `**Final fallback`. Each slice contains `writes no nested directory and no nested contract` exactly once and ``only by a `/sc:analyze` call`` exactly once.

All pins are exact substring checks. On the pre-change text every paragraph-slice pin and every tier-slice pin fails; only the `Quality-tier tracking` absence check passes there, because it guards the slice boundary and not the new wording.

Acceptance criteria:
- `tests/skills/test_brainstorm_protocol.py` contains the new sibling test with the paragraph-slice pins and both tier-slice pins above, and every earlier assertion of `test_brainstorm_unattended_nested_directories_are_named` is unchanged.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/SKILL.md | grep -c 'write no nested directory and no nested contract'` and `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md | grep -c 'writes no nested directory and no nested contract'` both print 0, and `git cat-file -e` exits 0 for both `HEAD:` paths, which shows the shared directory pins fail on the pre-change text.
Global constraints: ## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces two earlier plans for the same work, packages `TASK-WF-brainstormFixBri-20261106-001016` and `TASK-WF-brainstormFixBri-20261106-021737`. An independent review found the first not ready to run (its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned). A second review found that the second plan's live-check sentence required the folder whenever any `Skill`, `Agent` or `Task` call passed the flag text, so a `Task` prompt followed by an auggie or `fallback_1` scan would fail a correct run; the owner amended the brief's Part 4 on 2026-11-06 and this plan carries the amended text. Both earlier packages are left as they are.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after the owner commits and merges them; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.
Start sha: 6096d08673e4eb8c4ab698e6a63b483a1e11d732
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t4-checks.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t4-checks.txt
new file mode 100644
index 00000000..bf68c2bb
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t4-checks.txt
@@ -0,0 +1,12 @@
+== HEAD SKILL.md count (expect 0)
+0
+== HEAD handoff-routing.md count (expect 0)
+0
+== cat-file -e HEAD paths
+skill_exit=0
+routing_exit=0
+== existing test unchanged (diff of old test body)
+0
+== ruff
+All checks passed!
+ruff_exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t4-pytest.log b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t4-pytest.log
new file mode 100644
index 00000000..ec696d6f
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t4-pytest.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 3 items
+
+tests/skills/test_brainstorm_protocol.py ...                             [100%]
+
+============================== 3 passed in 0.03s ===============================
+exit=0
diff --git a/tests/skills/test_brainstorm_protocol.py b/tests/skills/test_brainstorm_protocol.py
index cb4a2ab2..6d25de77 100644
--- a/tests/skills/test_brainstorm_protocol.py
+++ b/tests/skills/test_brainstorm_protocol.py
@@ -47,6 +47,43 @@ def test_brainstorm_unattended_nested_directories_are_named():
     assert "nested/adversarial-" in refs.read_text(encoding="utf-8")
 
 
+def _section(text: str, start: str, end_pattern: str) -> str:
+    after = text.split(start, 1)
+    assert len(after) == 2, f"missing anchor {start!r}"
+    return re.split(end_pattern, after[1], maxsplit=1, flags=re.M)[0]
+
+
+def test_brainstorm_unattended_codebase_scan_writes_no_nested_directory():
+    """Only a /sc:analyze call writes nested/analyze-<n>/; auggie and fallback_1 do not (P1 lc10)."""
+    lead = "**Under `--unattended`**"
+    parts = _wave2a_section().split(lead, 1)
+    assert len(parts) == 2, "Wave 2A missing the Under --unattended paragraph"
+    paragraph = re.split(r"\n\s*\n", parts[1], maxsplit=1)[0]
+    assert "Quality-tier tracking" not in paragraph, "paragraph slice ran past its end"
+    for phrase in (
+        "fallback_1",
+        "write no nested directory and no nested contract",
+        "only by a `/sc:analyze` call",
+    ):
+        assert phrase in paragraph, phrase
+
+    routing = (_BRAINSTORM.parent / "refs" / "handoff-routing.md").read_text(
+        encoding="utf-8"
+    )
+    tier1 = _section(
+        routing, "**Tier 1 (primary)**", r"^\*\*Tier 2 \(fallback_1\)\*\*: codegraph"
+    )
+    tier2 = _section(
+        routing, "**Tier 2 (fallback_1)**: codegraph", r"^\*\*Final fallback"
+    )
+    for name, tier in (("Tier 1", tier1), ("Tier 2", tier2)):
+        for phrase in (
+            "writes no nested directory and no nested contract",
+            "only by a `/sc:analyze` call",
+        ):
+            assert tier.count(phrase) == 1, f"{name}: {phrase}"
+
+
 def test_brainstorm_no_tavily_param_duplication():
     """Wave-2A enrichment matrix routes only — no Tavily params / map/crawl tool names."""
     section = _wave2a_section()
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
