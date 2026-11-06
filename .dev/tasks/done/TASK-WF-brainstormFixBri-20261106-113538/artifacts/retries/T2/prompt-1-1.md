025512675f9067ea39244a1dabb1ba69321a67d0
Review one task for spec compliance.

Task brief: ## Task 2: State the same rule in the routing ref for both codebase tiers

In `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, the "Codebase enrichment" section has two tier lists. The list under `**Tier 1 (primary)**` (line 16) ends with the line `- quality_tier: ` followed by `primary` in backticks (line 22). The list under `**Tier 2 (fallback_1)**: codegraph, then native Glob/Grep` (line 24) ends with the line `- Activation: if Tier 1 returns error OR empty result` (line 31), and the line `**Final fallback**` (line 33) follows it. Add the bullet below, identical text, as the last bullet of each of the two lists: once after the Tier 1 `quality_tier` line, and once after the Tier 2 `Activation` line, both before the next `**Final fallback**` or `**Tier 2` anchor. The Tier 2 bullet must stay inside the span that `tests/skills/test_codegraph_adoption.py` reads in `test_brainstorm_tier2_names_codegraph_files_and_search` (from `**Tier 2 (fallback_1)**: codegraph` to the line starting `**Final fallback`).

```text
- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
```

The bullet names `/sc:analyze` as the only writer so that a reader of this ref alone does not conclude that codebase enrichment never nests. Do not touch the research tiers (line 35 onward) or the `nested/adversarial-` text.

Acceptance criteria:
- `grep -c 'writes no nested directory' src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2 (kept as a smoke check; Task 4 pins each tier separately).
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` shows two lines added and none deleted; one added bullet follows the Tier 1 `quality_tier` line and the other follows the Tier 2 `Activation` line.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_codegraph_adoption.py -q -p no:cacheprovider` passes with the edit in place.
- With `S` as in Task 1, `X=$(sed -n '232s/.*31): "\(.*\)" .grep.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cxF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2.
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
Start sha: 025512675f9067ea39244a1dabb1ba69321a67d0
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t2-checks.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t2-checks.txt
new file mode 100644
index 00000000..4e0c9dea
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t2-checks.txt
@@ -0,0 +1,24 @@
+== grep -c writes no nested directory
+2
+== diff stat
+ src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md | 2 ++
+ 1 file changed, 2 insertions(+)
+== numstat
+2	0	src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
+== diff -U1
+diff --git a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
+index da21ebbb..5dc0bea0 100644
+--- a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
++++ b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
+@@ -22,2 +22,3 @@ Loaded in Wave 2A. Defines the matrix of enrichment options and quality-tier fal
+ - quality_tier: `primary`
++- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
+ 
+@@ -31,2 +32,3 @@ Loaded in Wave 2A. Defines the matrix of enrichment options and quality-tier fal
+ - Activation: if Tier 1 returns error OR empty result
++- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
+ 
+== whole-text
+X_len=261
+plan_cxF=1
+target_cxF=2
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t2-pytest.log b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t2-pytest.log
new file mode 100644
index 00000000..824739f4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t2-pytest.log
@@ -0,0 +1,14 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 50 items
+
+tests/skills/test_codegraph_adoption.py ................................ [ 64%]
+..................                                                       [100%]
+
+============================== 50 passed in 0.33s ==============================
+exit=0
diff --git a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
index da21ebbb..5dc0bea0 100644
--- a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
@@ -20,6 +20,7 @@ Loaded in Wave 2A. Defines the matrix of enrichment options and quality-tier fal
   - Query 2: `"Project architecture, structure, patterns, and conventions related to {topic_domain_area}"`
 - Output budget: ~800-1200 tokens summary per query
 - quality_tier: `primary`
+- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
 
 **Tier 2 (fallback_1)**: codegraph, then native Glob/Grep
 
@@ -29,6 +30,7 @@ Loaded in Wave 2A. Defines the matrix of enrichment options and quality-tier fal
 - Output budget: ~300-500 tokens (raw file list + grep hits)
 - quality_tier: `fallback_1`
 - Activation: if Tier 1 returns error OR empty result
+- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
 
 **Final fallback**: skip enrichment, set quality_tier: `skipped`, log to seed-brief Note section.
 
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
