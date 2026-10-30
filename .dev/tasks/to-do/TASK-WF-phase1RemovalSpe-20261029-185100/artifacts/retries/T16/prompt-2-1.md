f3031870786d3c3cb79b989671195aec1a8d7167
Review one task for spec compliance.

Task brief: ## Task 16: Remove both servers from user docs, README, CLAUDE.md, SECURITY.md, CI comments and add the CHANGELOG entry

Depends on: Task 15

Implements ./source.md §8 T12 and rows C8-C12, S7, S9-S13, S16, S17, S20-S31. Delete or rewrite per each row's action in `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`, `docs/mcp/mcp-optional-design.md`, `docs/mcp/mcp-integration-policy.md`, `docs/analysis-sc-tasklist.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, `docs/developer-guide/technical-architecture.md`, `docs/user-guide/{agents,brainstorm,commands,flags,freshness-hooks,mcp-servers,memory-system,modes,session-management}.md`, `README.md:38,64,75,219`, `CLAUDE.md:377`, `SECURITY.md:328`; delete `docs/troubleshooting/serena-installation.md` and confirm `rg serena-installation` finds no inbound link. In `.github/workflows/test.yml` rewrite only the comments at `:133-134` and `:155` so they name no removed server; keep the `Install Claude CLI` step (`:156-159`) and `permissions: contents: read` (row C12, D20). Add a `CHANGELOG.md` entry: what was removed, the retire step, the manual commands from ./source.md §3.4 for kind-B workspaces and user data; it must not say the current-pin Serena registration is kept for good (it is removed once codegraph is ready, Phase 2 §2.12) and names `serena-local` as the re-register name. No "Retired servers" section in user docs (D7). Commit `docs: remove codebase-memory and Serena from user docs, README and CI (#323)`.

Acceptance criteria:
- T16.AC1: `uv run pytest tests/docs tests/core -q -p no:cacheprovider` passes.
- T16.AC2: `bash $PKG/artifacts/acceptance-search.sh all docs README.md CLAUDE.md SECURITY.md .github` prints `ACCEPTANCE_SEARCH_OK all`.
- T16.AC3: `uv run --no-project python -c 'import yaml,sys; d=yaml.safe_load(open(".github/workflows/test.yml")); s=[x.get("name") for x in d["jobs"]["doctor-check"]["steps"]]; sys.exit(0 if "Install Claude CLI" in s else 1)'` exits 0.
- T16.AC4: `rg -q 'serena-local' CHANGELOG.md` succeeds.

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
Start sha: f3031870786d3c3cb79b989671195aec1a8d7167
Diff against the start snapshot: Touched files: unchanged from the first review (see git diff f3031870786d3c3cb79b989671195aec1a8d7167 --stat -- . ':!.dev'); the work is still uncommitted in the working tree. ONE fix pass was applied since the first review (see the delta slot): the wording of the retire-step behavior in docs/user-guide/mcp-installation.md:9, CHANGELOG.md:20 and .github/workflows/test.yml:133,155. The first review marked AC1-AC4 met. Observed by the implementer: acceptance-search.sh all on docs README.md CLAUDE.md SECURITY.md .github prints ACCEPTANCE_SEARCH_OK all after the fix; the yaml still loads; rg for 'each kept entry' and 'registers and retires' prints nothing. Re-audit the full AC set, re-verify the corrected statements against src/superclaude/cli/install_retired_mcp.py (what it prints per verdict) and main.py, and check the same defect form elsewhere in docs/README/CHANGELOG (statements that install registers servers, or that a remove command is printed for every kept entry).
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.github/workflows/test.yml b/.github/workflows/test.yml
index 40fd87bf..67000aa5 100644
--- a/.github/workflows/test.yml
+++ b/.github/workflows/test.yml
@@ -130,7 +130,7 @@ jobs:
   doctor-check:
     name: SuperClaude Doctor Check
     runs-on: ubuntu-latest
-    # `superclaude install` registers and retires user-scope MCP servers through the Claude CLI;
+    # `superclaude install` retires stale user-scope MCP registrations through the Claude CLI;
     # keep the token read-only and out of .git/config while it runs.
     permissions:
       contents: read
@@ -152,7 +152,7 @@ jobs:
         with:
           node-version: "22"
 
-      # `superclaude install` registers and retires user-scope MCP servers through the Claude CLI.
+      # `superclaude install` retires stale user-scope MCP registrations through the Claude CLI.
       - name: Install Claude CLI
         run: |
           npm install -g @anthropic-ai/claude-code@2.1.286
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 6199925e..39b4a976 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -17,7 +17,7 @@ All notable changes to IronClaude are documented in this file.
 #### Added (retire step)
 
 - At its end, `superclaude install` runs a bounded, non-fatal retire step (10 seconds per `claude` call, 15 seconds for the whole step; no outcome changes the install exit code). It removes only **user-scope** registrations of `codebase-memory-mcp` and `serena` that IronClaude can prove it wrote, plus IronClaude's own receipt and marker files (`~/.local/bin/.superclaude-codebase-memory.json` and `.pending`) once their binary is gone.
-- It keeps every shape it cannot prove (for example a registration Coder's bundle also writes) and prints the exact `claude mcp remove <name> --scope user` command for it. Local-scope and project `.mcp.json` entries are never touched.
+- It keeps every shape it cannot prove (for example a registration Coder's bundle also writes) and prints the reason it was kept; for the legacy Serena launcher registration it also prints the exact `claude mcp remove serena --scope user` command. Local-scope and project `.mcp.json` entries are never touched.
 - It never touches binaries, uv tools, indexes, caches or memories.
 - The current-pin Serena registration (`uvx --from serena-agent==1.7.0 ...`) is not kept for good: it is kept, with the removal command printed on each install, only until the first `superclaude install` run in which the codegraph tools are installed and ready; that run removes it.
 - `superclaude install --list` shows one line per retired name (absent, will be removed, or kept with the reason). `superclaude doctor` warns, never fails, when something removable is left. `superclaude update` only prints "legacy registration present: run `superclaude install`".
diff --git a/docs/user-guide/mcp-installation.md b/docs/user-guide/mcp-installation.md
index 0af567c1..f9aebc1a 100644
--- a/docs/user-guide/mcp-installation.md
+++ b/docs/user-guide/mcp-installation.md
@@ -6,7 +6,7 @@ SuperClaude provides a convenient CLI command for installing and managing MCP (M
 
 `superclaude install` installs framework files, commands, agents, skills, ccsession wiring, hooks, templates and user setup. It does **not** install any MCP server: use `superclaude mcp` for that (see below).
 
-At the end of the run it performs one short cleanup step for old user-level MCP registrations: it removes only entries (and IronClaude's own leftover receipt files) that IronClaude can prove it wrote, keeps any entry it cannot prove, and prints the exact `claude mcp remove ... --scope user` command for each kept entry. The step is bounded in time, never changes the exit code of `superclaude install`, and never touches binaries, indexes, caches or memories. See the [CHANGELOG](../../CHANGELOG.md) for the full list of what it covers.
+At the end of the run it performs one short cleanup step for old user-level MCP registrations: it removes only entries (and IronClaude's own leftover receipt files) that IronClaude can prove it wrote, keeps any entry it cannot prove and prints the reason (and, for a legacy launcher registration, the exact `claude mcp remove ... --scope user` command to remove it by hand). The step is bounded in time, never changes the exit code of `superclaude install`, and never touches binaries, indexes, caches or memories. See the [CHANGELOG](../../CHANGELOG.md) for the full list of what it covers.
 
 - `superclaude install --list` is read-only. It reports what the cleanup step would do, one line per name, without changing anything.
 - `superclaude doctor` warns (never fails) when the cleanup step still has something to remove.
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=scope at=docs/user-guide/mcp-installation.md:9 anchor=src/superclaude/cli/install_retired_mcp.py:383 chk=n,y,n,n family=retire-step-claim fix=reword: the step prints the reason for each kept entry, and the exact claude mcp remove command only for a legacy launcher registration; same in CHANGELOG.md:20 first=A1 origin=new: doc and CHANGELOG say the step prints the exact remove command for each kept entry; code prints only the kept reason for non-launcher entries.
F1.2 sev=blocking trigger=B2 ac=scope at=.github/workflows/test.yml:133 anchor=src/superclaude/cli/main.py:230 chk=n,y,n,n family=retire-step-claim fix=say install retires stale user-scope MCP registrations (it registers none), in the comments at :133 and :155 first=A1 origin=new: the comments say superclaude install registers and retires MCP servers; it only retires.
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
