8c35d2c1b823c098623adde56cc7bef1a8c36980
Review one task for spec compliance.

Task brief: ## Task 12: Replace Serena memory in skills, the routing guide and reflect calibration

Depends on: Task 11

Implements ./source.md §5 rules M1-M8 and §8 T10b. Memory parts of rows P6, P15, P43 (`commands/sc-reflect.md`, `plugins/superclaude/commands/reflect.md`, `src/superclaude/commands/reflect.md`), P50 and P96 (`src/superclaude/commands/validate-roadmap.md` memory tool entries; `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` ledger, terminology map and pattern log move to `.superclaude/memory/validate-roadmap/<key>.md`, still fail-open), P77 (`src/superclaude/skills/sc-reflect-protocol/SKILL.md` calibration memory to tracked `docs/memory/reflect/deviation-patterns-<slug>.md`), P91 (`src/superclaude/skills/sc-task-protocol/SKILL.md` STRICT-tier memory and `activate_project` steps); rows P68-P71 (`src/superclaude/skills/sc-crash-recovery/SKILL.md`, `refs/investigators.md`, `refs/report-template.md`, `scripts/bootstrap_scan.sh:146-147` fields renamed `has_memory`, `memory_count`, reading `.superclaude/memory`), P82 and P85 (`sc-reflect-protocol/refs/input-resolution.md`, `refs/remediation-handoff.md`), P24 and P52 (`src/superclaude/core/HOW-WE-WORK.md:237,327,329` plus its byte copy), S89 (`tests/core/test_how_we_work_routing_table.py:1074`), S90 (`tests/recommend/fixtures/routing_refresh_cases.json:576,584`), and S4: `mkdir -p docs/memory/reflect` (the folder does not exist yet), then `git mv .serena/memories/reflect/deviation-patterns-IronClaude.md docs/memory/reflect/deviation-patterns-IronClaude.md` (content kept). Delete, do not port, the Serena-only calls of rule M8 in these files. Commit `feat(memory)!: replace Serena memory with .superclaude/memory files in skills and the routing guide (#323)`.

Acceptance criteria:
- T12.AC1: `make sync-dev && make verify-sync` passes and `uv run pytest tests/core tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py tests/recommend tests/skills tests/sc-roadmap tests/cli/reflect -q -p no:cacheprovider` passes (`tests/cli/reflect/test_remediation_route_table.py` reads `remediation-handoff.md`).
- T12.AC2: `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` succeeds.
- T12.AC3: `rg -n --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory' src/superclaude plugins/superclaude commands agents -g '!src/superclaude/skills/sc-reflect-protocol/SKILL.md' -g '!**/reflect.md' -g '!commands/sc-reflect.md' -g '!src/superclaude/commands/validate-roadmap.md'` prints nothing (repo-wide; the excluded files are rewritten by Tasks 13 and 15, and the full-token repo-wide check is Task 15's `acceptance-search.sh serena src/superclaude plugins/superclaude commands agents`).
- T12.AC4: `test -f docs/memory/reflect/deviation-patterns-IronClaude.md` succeeds.

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
Start sha: 8c35d2c1b823c098623adde56cc7bef1a8c36980
Diff against the start snapshot: Touched files: see the stat (uncommitted working tree; the calibration file move is staged as a git rename). Spec: $PKG/source.md section 5 (lines 408-425), section 8 T10b (lines 736-742) and section 8.1 row T10b, plus the plan's Task 12 text. The memory rewrite was done by a helper agent; judge the files on disk. Scope boundary: this task does the MEMORY parts only; Serena tool parts (symbol/reference/diagnostics, the --onboard flow, degraded tokens, mcp__serena__ roster entries) belong to Tasks 13 and 15, so remaining list_memories / mcp__serena__ hits in src/superclaude/skills/sc-reflect-protocol/SKILL.md, the three reflect.md command copies and src/superclaude/commands/validate-roadmap.md are expected. Observed by the implementer (verify yourself): make sync-dev && make verify-sync passes; cmp of the two HOW-WE-WORK copies succeeds; the rg check prints nothing; docs/memory/reflect/deviation-patterns-IronClaude.md exists (git mv); the Task 12 pytest command gives 1392 passed, 87 skipped, 1 xpassed. Decisions 6 and 7 in $PKG/decisions.md record two judgment calls.

 commands/sc-reflect.md                             |  4 +-
 .../reflect/deviation-patterns-IronClaude.md       |  0
 plugins/superclaude/commands/reflect.md            |  4 +-
 .../skills/sc-recommend/refs/HOW-WE-WORK.md        |  6 +-
 src/superclaude/commands/reflect.md                |  4 +-
 src/superclaude/core/HOW-WE-WORK.md                |  6 +-
 src/superclaude/skills/sc-crash-recovery/SKILL.md  | 14 ++--
 .../skills/sc-crash-recovery/refs/investigators.md | 10 +--
 .../sc-crash-recovery/refs/report-template.md      |  4 +-
 .../sc-crash-recovery/scripts/bootstrap_scan.sh    | 11 ++-
 .../skills/sc-reflect-protocol/SKILL.md            | 81 +++++++++-------------
 .../sc-reflect-protocol/refs/input-resolution.md   |  2 -
 .../refs/remediation-handoff.md                    |  9 +--
 src/superclaude/skills/sc-task-protocol/SKILL.md   | 31 ++++-----
 .../skills/sc-validate-roadmap-protocol/SKILL.md   | 43 ++++++------
 tests/core/test_how_we_work_routing_table.py       |  3 +-
 .../recommend/fixtures/routing_refresh_cases.json  |  4 +-
 17 files changed, 113 insertions(+), 123 deletions(-)

diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -234,7 +234,7 @@ There are two ways to resume. Use the first if you set it up; the second always
 - **A task file (`/task`).** Run `/task <path to the task file>` again. It continues from the first unchecked item.
 - **A simple plan (`/sc:implement`).** Run `/sc:implement .dev/tasks/to-do/<id>/<id>.md` again. The `progress.md` file beside the plan records every finished step, and the run continues from the first unfinished one. If the folder has already moved to `.dev/tasks/done/`, the work is finished. Folders named `TASK-WF-*` are `/sc:workflow` plans: run them with `/sc:implement`, never with `/task`.
 
-`/sc:save` and `/sc:load` store and load Serena project memory. They are not a way to resume work or a guarantee of complete executor state. Other command-owned continuations keep their own supplied pipeline, output folder, validated proposal or document-task input; do not convert them into task-builder or a fresh generic plan. Clarify the artifact when it is not known.
+`/sc:save` and `/sc:load` store and load project memory as plain markdown files under `.superclaude/memory/`. They are not a way to resume work or a guarantee of complete executor state. Other command-owned continuations keep their own supplied pipeline, output folder, validated proposal or document-task input; do not convert them into task-builder or a fresh generic plan. Clarify the artifact when it is not known.
 
 ### 3.13 Specialist deliverables and operations
 
@@ -324,9 +324,9 @@ Additional operations and explicit coordination choices. These entries can be re
 | `/sc:git` | Requested status, add, local smart commit, branch or merge operations using declared controls. Status-only stays inspection; a commit needs authorization. Do not append push, merge or PR creation. Native tools may be enough. |
 | `/sc:index` | Coordinated project docs/API/structure/README and requested output format; writes documentation. Distinct from a compact repo map. |
 | `/sc:index-repo` | Compact PROJECT_INDEX.md and PROJECT_INDEX.json map. Preserve documented keyword mode=quick or mode=update and existing-output intent. Verify invocation naming in the active copy; no measured token-savings promise. |
-| `/sc:load` | Load/refresh Serena project context with supported type/refresh/analyze controls; requires Serena. Not executor resume or proof of complete checkpoint restoration; exclude undeclared example-only options. |
+| `/sc:load` | Load/refresh project context from the `.superclaude/memory/` files with supported type/refresh/analyze controls; needs no MCP server. Not executor resume or proof of complete checkpoint restoration; exclude undeclared example-only options. |
 | `/sc:pm` | Explicit PM coordination with requested strategy/verbosity and available protocol/tools. It can write memory/docs; verify dependencies. Not a default planner, automatic-start guarantee or universal executor-resume method. |
-| `/sc:save` | Persist requested session/learnings/context/all memory with supported summarize/checkpoint controls. Requires Serena and writes memory; not durable task execution state or a latency guarantee. |
+| `/sc:save` | Persist requested session/learnings/context/all memory with supported summarize/checkpoint controls. Stores plain markdown files under `.superclaude/memory/` (no MCP server) and writes memory; not durable task execution state or a latency guarantee. |
 | `/sc:spawn` | Requested decomposition with sequential/parallel/adaptive strategy and normal/deep depth. Its critical stop is a task hierarchy only: no source edits or downstream implementation. Branch tracing is limited to its documented filter-pipeline trigger, not every delegation. Ordinary implementation planning still uses workflow/implement. |
 
 One more user-facing skill: `/confidence-check` checks readiness before implementation. Supporting command protocols are loaded through their command's actual activation directive; do not infer a protocol name from a filename. Self-contained commands are valid, and TDD resolves to the tdd skill through Skill Invocation. Verify required agents, templates and tools before promising execution.
diff --git a/src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh b/src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh
--- a/src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh
+++ b/src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh
@@ -47,6 +47,13 @@ count_in() {
   find "$dir" -type f 2>/dev/null | wc -l | tr -d ' '
 }
 
+# Count markdown memory files (*.md) anywhere under a directory.
+count_md_in() {
+  local dir="$1"
+  [[ -d "$dir" ]] || { echo 0; return; }
+  find "$dir" -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' '
+}
+
 # Find pipeline state files newer than SINCE_HOURS, anywhere under project.
 recent_files() {
   local pattern="$1"
@@ -143,8 +150,8 @@ cat <<JSON
   "recent_sessions": $SESSIONS,
   "has_dev": $([[ -d "$ABS_PROJECT/.dev" ]] && echo true || echo false),
   "has_docs": $([[ -d "$ABS_PROJECT/docs" ]] && echo true || echo false),
-  "has_serena": $([[ -d "$ABS_PROJECT/.serena/memories" ]] && echo true || echo false),
-  "serena_memory_count": $(count_in "$ABS_PROJECT/.serena/memories"),
+  "has_memory": $([[ -d "$ABS_PROJECT/.superclaude/memory" ]] && echo true || echo false),
+  "memory_count": $(count_md_in "$ABS_PROJECT/.superclaude/memory"),
   "git": $(git_state),
   "sprints": $(sprints_state),
   "tasks": $(task_state),
diff --git a/tests/core/test_how_we_work_routing_table.py b/tests/core/test_how_we_work_routing_table.py
--- a/tests/core/test_how_we_work_routing_table.py
+++ b/tests/core/test_how_we_work_routing_table.py
@@ -1071,7 +1071,8 @@ def test_other_operations_preserve_requested_authority_and_owned_state():
     assert "mode=quick or mode=update" in other
     assert "PROJECT_INDEX.md and PROJECT_INDEX.json" in other
     assert "Coordinated project docs/API/structure/README" in other
-    assert "requires Serena" in other
+    assert "needs no MCP server" in other
+    assert ".superclaude/memory/" in other
     assert "writes memory; not durable task execution state" in other
     assert "Not executor resume" in other
     assert "inspect status, orient, then wait" in other
diff --git a/tests/recommend/fixtures/routing_refresh_cases.json b/tests/recommend/fixtures/routing_refresh_cases.json
--- a/tests/recommend/fixtures/routing_refresh_cases.json
+++ b/tests/recommend/fixtures/routing_refresh_cases.json
@@ -573,7 +573,7 @@
       "retained_inputs": [],
       "stop": "memory written",
       "authority": "memory-write",
-      "side_effects": "Serena memory writes only; not task execution state",
+      "side_effects": ".superclaude/memory file writes only; not task execution state",
       "guide_phrases": ["writes memory; not durable task execution state"],
       "negative": {"competitors": ["sc:implement", "task"], "must_not": "executor continuation or undeclared checkpoint examples"},
       "activation": {"sc:save": "self-contained", "sc:load": "self-contained"},
@@ -581,7 +581,7 @@
         {"request": "Load and refresh the saved project context.", "targets": ["sc:load"], "mode_flags": ["--refresh"], "guide_route": {"block": "other", "command": "sc:load"}, "guide_phrases": ["Not executor resume"], "expected": "context load/refresh only; a task-package resume uses its own executor"}
       ],
       "variants": {
-        "unavailable_plugin": {"environment": "plugin-only", "missing": "sc:save", "expected": "not installed: sc:save; Serena prerequisite disclosed"},
+        "unavailable_plugin": {"environment": "plugin-only", "missing": "sc:save", "expected": "not installed: sc:save; no MCP server prerequisite to disclose"},
         "seeded_wrong_cache": {"environment": "checkout-seeded-wrong-cache", "cache_row": {"key": "codebase-research", "candidate": "/sc:implement", "envelope": "Run: /sc:implement .dev/tasks/to-do/previous/previous.md"}, "expected": "no routing row matched; if dispatch hits codebase-research: cache hint consulted, cached /sc:implement rejected by current verification and request binding (miss_validation_stale); on a miss (classifier unknown -> no_key, or no row): cache row unused; either way live discovery selects /sc:save from Other commands; no hit telemetry; cached /sc:implement never emitted"}
       }
     },
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
