03363fdfb5b55b8fc0df493d88aff572fe7d83c5
Review one task for spec compliance.

Task brief: ## Task 1: State in the skill that the auggie scan and the fallback tier write no nested directory

First, before any edit, save the output of `git status --porcelain` to `./artifacts/status-before.txt`. Task 7 compares against that file.

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, the Wave 2A paragraph whose bold lead-in is "Under `--unattended`" (line 195) currently ends: "The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`." Replace everything after "(`<n>` starts at 1)" with this exact text, copied character for character:

```text
; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
```

The wording names the writer (a tool or a tier), never a recorded `quality_tier` or a run. A clean `/sc:analyze` run is also `primary`, and `enrichment_used` records `source` and `quality_tier` as separate fields that do not name the tool, so a statement that depended on the tier would be wrong for an analyze run. It states no tier for any `/sc:analyze` outcome and keeps the nested contract listed unconditionally, a failed call's included. Change nothing else in the file.

Acceptance criteria:
- `./artifacts/status-before.txt` exists and was written before the first edit of this plan.
- The paragraph with the bold lead-in "Under `--unattended`" in the Wave 2A section of `SKILL.md` contains `fallback_1`, `write no nested directory and no nested contract`, ``only by a `/sc:analyze` call``, `nested/analyze-` and `skipped`, ends with "The nested contract is listed in `artifacts`, also when the call failed.", and a regular-expression search for `only for a nested command that r[a]n` finds nothing in it.
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` shows one line changed (one insertion, one deletion).
- With `S` set to this package's `source.md` and the command run from the repository root, `X=$(sed -n '231s/.*with: "\(.*\)" Task 1 AC.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` prints 1.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` still passes before Task 4 changes the tests.
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
Start sha: 03363fdfb5b55b8fc0df493d88aff572fe7d83c5
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t1-checks.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t1-checks.txt
new file mode 100644
index 00000000..c9c217eb
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t1-checks.txt
@@ -0,0 +1,19 @@
+== diff stat
+ src/superclaude/skills/sc-brainstorm-protocol/SKILL.md | 2 +-
+ 1 file changed, 1 insertion(+), 1 deletion(-)
+== numstat
+1	1	src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+== line 195 pins
+fallback_1: 1
+write no nested directory and no nested contract: 1
+only by a `/sc:analyze` call: 1
+nested/analyze-: 1
+skipped: 1
+== ends with
+1
+== forbidden regex (expect 0)
+0
+== whole-text
+X_len=412
+plan_cxF=1
+target_cF=1
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t1-pytest.log b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t1-pytest.log
new file mode 100644
index 00000000..a5fa03bd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t1-pytest.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 2 items
+
+tests/skills/test_brainstorm_protocol.py ..                              [100%]
+
+============================== 2 passed in 0.03s ===============================
+exit=0
diff --git a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
index 0d9f86bd..ce27509a 100644
--- a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
@@ -192,7 +192,7 @@ Orchestrate parallel brainstorming via:
 
    Research depth/params are owned by `/sc:research` and `tech-research` — see RESEARCH_CONFIG.md; brainstorm selects the route only.
 
-   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`.
+   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
 
 2. **Quality-tier tracking** (mandatory per enrichment source):
    - `primary` — first-choice source ran cleanly
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
