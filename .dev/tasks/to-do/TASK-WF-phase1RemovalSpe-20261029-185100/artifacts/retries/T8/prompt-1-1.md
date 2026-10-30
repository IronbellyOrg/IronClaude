d556b81ccbc2aaa3c5edfac88041f7985033c46d
Review one task for spec compliance.

Task brief: ## Task 8: Drop Serena tools from the freshness hook and the eval suite

Depends on: Task 7

Implements ./source.md §8 T7 and rows P21, P55, D1, D2, S37, S38, S40, S57, S87. Set the matcher to `Edit|Write` in `src/superclaude/hooks/hooks.json:47` and `plugins/superclaude/hooks/hooks.json:37`; in both `freshness-pre-edit.sh` copies (`src/superclaude/hooks/scripts/` and `plugins/superclaude/hooks/scripts/`) delete the `relative_path` branch and reword the line-36 message to "no file_path in tool_input"; delete the four asserts at `tests/cli/test_install_hooks.py:684-687`; in `src/superclaude/cli/eval/suites/real.yaml` delete capability row `:40` and eval E8 (`:566-690`) and fix the comments at `:380-384`, `:406-407`, `:475-479`, `:499-506` and `:721` (the PreToolUse matcher comment `Edit|Write|mcp__serena__*` becomes `Edit|Write`); reword `src/superclaude/cli/eval/coverage.py:195` and `src/superclaude/cli/eval/suites/README.md:170`; change the tool string at `tests/cli/eval/test_coverage_gate.py:127` to `mcp__context7__resolve-library-id`. Commit `fix(hooks): drop Serena tools from the freshness gate and the eval suite (#323)`.

Acceptance criteria:
- T8.AC1: `uv run pytest tests/cli/test_install_hooks.py tests/hooks tests/cli/eval/test_coverage_gate.py tests/cli/eval/test_no_mcp_skip.py tests/cli/eval/test_schema_validate.py tests/cli/eval/test_capability_gates.py -q -p no:cacheprovider` passes (only these eval files; never the whole `tests/cli/eval/`).
- T8.AC2: `rg -n 'mcp__serena|relative_path' src/superclaude/hooks plugins/superclaude/hooks src/superclaude/cli/eval tests/cli/test_install_hooks.py tests/cli/eval/test_coverage_gate.py` prints nothing.

`$PKG` = /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100 (repo root: the git top-level of that directory). The source spec for anything the brief says is in `$PKG/source.md`; the plan is `$PKG/TASK-WF-phase1RemovalSpe-20261029-185100.md`.

Global constraints (plan `## Constraints`, verbatim):
- Work on branch `ironbelly/feat-codememory-codegraph-init`, base commit `55d40308`. Do not open a pull request to `master` for Phase 1 alone and do not push to `upstream`; Phases 1 and 2 merge as one unit (./source.md §2.2, D9).
- `$PKG` in every command below means this package's directory as the executor resolves it at run time (the folder that holds this plan); never hardcode it. Evidence goes under `$PKG/artifacts/`; handoff notes for other repos go under `$PKG/handoffs/`.
- One commit per task, conventional commit message as given in each task, ending with the attribution line the executor's session requires. Every commit stages the task package with `git add .dev/tasks` (package, `progress.md` and `artifacts/` included). Never stage or commit `.claude/` content (only `.claude/settings.json` is tracked, and Phase 1 does not touch it). Never use `git add -f` on a `.claude/` path.
- Every edit to a `src/superclaude/...` primitive is mirrored by hand, in the same commit, in its `plugins/superclaude/...` twin and its root `commands/sc-*.md` / `agents/sc-*.md` copy where ./source.md §1.2 lists one (D15).
- After editing `src/superclaude/core/HOW-WE-WORK.md`, copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md`.
- Use `uv run` for Python; standalone scripts run with `uv run --no-project python -I`. Every pytest run uses `-p no:cacheprovider`. Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` is not rewritten. After every test run, `git status --short` must list only files the task intends to change; restore any tracked file a test changed.
- Test baseline: the full suite already has failures at the base (W1 saw 27 failed and 16 errors). "Passes" for a targeted command means no failing test id that is not in `$PKG/artifacts/baseline/full.txt` (compare with the `comm -13` form in Task 18); never assume a clean suite.
- Never run the real `./update.sh`, `superclaude install` (including `--list`) or `claude mcp add/remove` against the real `HOME`; every environment check runs in a sandbox `HOME` made with `mktemp -d` (./source.md §10, D8). Never delete user data (`~/.serena`, project `.serena/` folders outside this repo, `~/.cache/codebase-memory-mcp`). Never edit another repository.
- Progress reporting (./source.md §9): at the end of each task group (Phases 1-6 below, i.e. groups G0-G5) post exactly one comment on issue #323 of the fork, and only there. First run `gh repo view --json nameWithOwner -q .nameWithOwner` (must print `IronbellyOrg/IronClaude`; otherwise run `gh repo set-default IronbellyOrg/IronClaude`), then `gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>. Tasks: <task ids>. Checks: <exact commands> -> <result>. Decisions logged: <count, path in task package>. Next: <next group>."`. Never use a bare `gh issue comment` and never `--repo SuperClaude-Org/...`. If `gh` is unauthenticated or fails, record the exact error and the intended body in `$PKG/progress.md` and continue (not a blocker).
- Decision rules (./source.md §10), never stop to ask the user: a simple decision (one obvious option, or one the source already constrains) is made by the executor and logged as one line in `$PKG/decisions.md` (decision, options, method `self`, rationale). A mid-level decision (two or more viable options with real trade-offs inside one task) writes each option to `$PKG/decisions/<task>-<slug>/option-<x>.md`, spawns an agent that runs `/sc:adversarial --compare <option files> --depth quick`, follows its recommendation and logs method `adversarial quick` with the merged-recommendation path. A complex decision (an architectural change to the source's design: retire-step scope, memory store layout, merge order, deleting a file the source keeps) does the same with `/sc:adversarial --compare <option files>` (standard depth) and logs method `adversarial full`.
- A blocked task stays blocked with its reason in `$PKG/progress.md`; continue with tasks that do not depend on it. If a task's acceptance fails, fix it within the task's files; if the fix needs a file another task owns, pull that edit forward and log it in `$PKG/decisions.md`. A task may not need a later task to go green.
- Scope limits (./source.md §2.1, §2.3): existing `.dev/` files outside `$PKG` are never edited; the only other `.dev/` writes are the new files `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` and `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`, and each task that writes one stages that exact file (`git add <path>`, never the folder). No task uninstalls the `serena-agent` uv tool or removes `~/.local/bin/{serena,serena-agent,serena-hooks}`, the Coder `/usr/local/bin/codebase-memory-mcp` binary, bundle markers, upstream companions or `~/.local/bin/install.sh`; those are handed off, not removed by Phase 1.
- This plan was corrected after an advisory `/sc:reflect --mode pre` review (`.dev/codegraph-migration/review/F1-result.md`). Where a task's text here differs from `./source.md`, the task text wins.
- Human actions the executor must not attempt: merging Phases 1 and 2 to `master` (Phase 2's PR via `/sc:pr-submit`) and running the real `./update.sh` on a live workspace after that merge (Phase 2 owns that live check).
Start sha: d556b81ccbc2aaa3c5edfac88041f7985033c46d
Diff against the start snapshot: Touched files: src/superclaude/hooks/hooks.json, plugins/superclaude/hooks/hooks.json, src/superclaude/hooks/scripts/freshness-pre-edit.sh, plugins/superclaude/hooks/scripts/freshness-pre-edit.sh, tests/cli/test_install_hooks.py, src/superclaude/cli/eval/suites/real.yaml, src/superclaude/cli/eval/coverage.py, src/superclaude/cli/eval/suites/README.md, tests/cli/eval/test_coverage_gate.py. Spec: $PKG/source.md section 8 T7 (lines 704-708) and section 8.1 row T7, and the plan's Task 8 text. Observed by the implementer (verify yourself): the Task 8 pytest command gives 109 passed, 1 skipped; the rg check prints nothing; make sync-dev was run afterwards (the gitignored .claude mirror) and tests/cli/test_verify_sync_hooks.py passes.

 .../progress.md                                    |   1 +
 plugins/superclaude/hooks/hooks.json               |   2 +-
 .../hooks/scripts/freshness-pre-edit.sh            |   8 +-
 src/superclaude/cli/eval/coverage.py               |   2 +-
 src/superclaude/cli/eval/suites/README.md          |   2 +-
 src/superclaude/cli/eval/suites/real.yaml          | 162 +++------------------
 src/superclaude/hooks/hooks.json                   |   2 +-
 .../hooks/scripts/freshness-pre-edit.sh            |   8 +-
 tests/cli/eval/test_coverage_gate.py               |   2 +-
 tests/cli/test_install_hooks.py                    |   4 -
 10 files changed, 25 insertions(+), 168 deletions(-)

diff --git a/plugins/superclaude/hooks/hooks.json b/plugins/superclaude/hooks/hooks.json
index ecd7c94e..5be9ef8b 100644
--- a/plugins/superclaude/hooks/hooks.json
+++ b/plugins/superclaude/hooks/hooks.json
@@ -34,7 +34,7 @@
     ],
     "PreToolUse": [
       {
-        "matcher": "Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol",
+        "matcher": "Edit|Write",
         "hooks": [
           {
             "type": "command",
diff --git a/plugins/superclaude/hooks/scripts/freshness-pre-edit.sh b/plugins/superclaude/hooks/scripts/freshness-pre-edit.sh
index e09a45d9..537318fb 100755
--- a/plugins/superclaude/hooks/scripts/freshness-pre-edit.sh
+++ b/plugins/superclaude/hooks/scripts/freshness-pre-edit.sh
@@ -22,18 +22,12 @@ CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
 
 # 2. Extract target_path
 FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
-REL_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.relative_path // empty' 2>/dev/null)
 TARGET=""
 if [ -n "$FILE_PATH" ]; then
     TARGET="$FILE_PATH"
-elif [ -n "$REL_PATH" ]; then
-    case "$REL_PATH" in
-        /*) TARGET="$REL_PATH" ;;
-        *)  TARGET="$CWD/$REL_PATH" ;;
-    esac
 else
     # Cannot enforce on this tool variant — fail open.
-    echo "freshness-pre-edit: no file_path/relative_path in tool_input for $TOOL_NAME; allowing." >&2
+    echo "freshness-pre-edit: no file_path in tool_input for $TOOL_NAME; allowing." >&2
     exit 0
 fi
 
diff --git a/src/superclaude/cli/eval/coverage.py b/src/superclaude/cli/eval/coverage.py
index b9bfd91b..a1dcfeaf 100644
--- a/src/superclaude/cli/eval/coverage.py
+++ b/src/superclaude/cli/eval/coverage.py
@@ -192,7 +192,7 @@ def sanitize_pattern_for_filename(pattern: str) -> str:
 def default_matcher_filter(pattern: str) -> bool:
     """v1 only enforces coverage for matchers that target MCP tools.
 
-    Matchers like ``Edit|Write|mcp__serena__replace_content`` mix MCP
+    Matchers like ``Edit|Write|mcp__context7__resolve-library-id`` mix MCP
     tool prefixes with built-in tool names — these are bookkeeping
     hooks that no eval needs to issue a tool call for. The v1 gate
     therefore restricts itself to matchers that mention one of the
diff --git a/src/superclaude/cli/eval/suites/README.md b/src/superclaude/cli/eval/suites/README.md
index d5190826..6346fdff 100644
--- a/src/superclaude/cli/eval/suites/README.md
+++ b/src/superclaude/cli/eval/suites/README.md
@@ -167,7 +167,7 @@ escape hatch (see FR-CLI1 flag table).
 - **Filename:** `quick.yaml` in this directory.
 - **Roster:** a curated 3-5 eval subset of `real.yaml` covering the
   PostToolUse Read async path (E9) and one matcher branch each from
-  the Edit / Write / serena trio (E6 / E7 / E8) — biased toward
+  the Edit / Write pair (E6 / E7) — biased toward
   evals that pass on every host without `--no-mcp`. Final roster
   selected by the suite owner at follow-up time.
 - **Acceptance signal:** total wall-clock budget < 90s on a clean
diff --git a/src/superclaude/hooks/hooks.json b/src/superclaude/hooks/hooks.json
index 89bd23df..858ef620 100644
--- a/src/superclaude/hooks/hooks.json
+++ b/src/superclaude/hooks/hooks.json
@@ -44,7 +44,7 @@
     ],
     "PreToolUse": [
       {
-        "matcher": "Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol",
+        "matcher": "Edit|Write",
         "hooks": [
           {
             "type": "command",
diff --git a/src/superclaude/hooks/scripts/freshness-pre-edit.sh b/src/superclaude/hooks/scripts/freshness-pre-edit.sh
index 3e7e064a..46cd98da 100755
--- a/src/superclaude/hooks/scripts/freshness-pre-edit.sh
+++ b/src/superclaude/hooks/scripts/freshness-pre-edit.sh
@@ -22,18 +22,12 @@ CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
 
 # 2. Extract target_path
 FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
-REL_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.relative_path // empty' 2>/dev/null)
 TARGET=""
 if [ -n "$FILE_PATH" ]; then
     TARGET="$FILE_PATH"
-elif [ -n "$REL_PATH" ]; then
-    case "$REL_PATH" in
-        /*) TARGET="$REL_PATH" ;;
-        *)  TARGET="$CWD/$REL_PATH" ;;
-    esac
 else
     # Cannot enforce on this tool variant — fail open.
-    echo "freshness-pre-edit: no file_path/relative_path in tool_input for $TOOL_NAME; allowing." >&2
+    echo "freshness-pre-edit: no file_path in tool_input for $TOOL_NAME; allowing." >&2
     exit 0
 fi
 
diff --git a/tests/cli/eval/test_coverage_gate.py b/tests/cli/eval/test_coverage_gate.py
index a4e21e31..287b8014 100644
--- a/tests/cli/eval/test_coverage_gate.py
+++ b/tests/cli/eval/test_coverage_gate.py
@@ -124,7 +124,7 @@ def test_eval_covers_pattern_matches_prefix_regex() -> None:
 
 
 def test_eval_covers_pattern_misses_unrelated_tool_call() -> None:
-    spec = _spec("E1", "mcp__serena__find_symbol")
+    spec = _spec("E1", "mcp__context7__resolve-library-id")
     assert eval_covers_pattern(spec, "mcp__auggie__.*") is False
 
 
diff --git a/tests/cli/test_install_hooks.py b/tests/cli/test_install_hooks.py
index c6b6e32a..e340d012 100644
--- a/tests/cli/test_install_hooks.py
+++ b/tests/cli/test_install_hooks.py
@@ -681,7 +681,3 @@ def test_real_hooks_json_gates_write_in_pre_tool_use():
     # Proposal A keeps Write in the matcher — script handles create-case.
     assert "Edit" in matcher_tools
     assert "Write" in matcher_tools
-    assert "mcp__serena__replace_content" in matcher_tools
-    assert "mcp__serena__replace_symbol_body" in matcher_tools
-    assert "mcp__serena__insert_after_symbol" in matcher_tools
-    assert "mcp__serena__insert_before_symbol" in matcher_tools

real.yaml: read it from disk and use: git diff d556b81ccbc2aaa3c5edfac88041f7985033c46d -- src/superclaude/cli/eval/suites/real.yaml
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

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
