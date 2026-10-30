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
Diff against the start snapshot: Touched files: see the stat (uncommitted working tree; docs/troubleshooting/serena-installation.md is deleted with git rm). The edits were made by a helper agent; judge the files on disk. Spec: the plan's Task 16 text and $PKG/source.md rows C8-C12, S7, S9-S13, S16, S17, S20-S31 (grep them), section 3.4 (CHANGELOG manual commands) and decision D7 (no 'Retired servers' section in user docs). Observed by the implementer (verify yourself): uv run pytest tests/docs tests/core gives 97 passed; acceptance-search.sh all on docs README.md CLAUDE.md SECURITY.md .github prints ACCEPTANCE_SEARCH_OK all; the yaml check for the Install Claude CLI step exits 0; rg -q 'serena-local' CHANGELOG.md succeeds; no inbound link to serena-installation remains. Things to check beyond the ACs: the docs are still coherent and well formed (no dangling cross references or anchors, tables intact, TOC entries match headings), the docs describe the CURRENT behavior of superclaude install/mcp/update/doctor correctly (compare with src/superclaude/cli/install_retired_mcp.py and main.py), the CHANGELOG entry does not say the current-pin Serena registration is kept for good and names serena-local, and no user doc gained a 'Retired servers' section.

 .github/workflows/test.yml                         |   4 +-
 CHANGELOG.md                                       |  53 +++++++
 CLAUDE.md                                          |   1 -
 README.md                                          |   7 +-
 SECURITY.md                                        |   1 -
 docs/analysis-sc-tasklist.md                       |   2 +-
 ...laude-Developer-Guide-Commands-Skills-Agents.md |  20 ++-
 docs/developer-guide/technical-architecture.md     |   2 +-
 docs/mcp/mcp-integration-policy.md                 |  99 ++-----------
 docs/mcp/mcp-optional-design.md                    |  42 +++---
 docs/reference/mcp-server-guide.md                 |  74 +---------
 docs/troubleshooting/serena-installation.md        | 156 --------------------
 docs/user-guide/agents.md                          |   3 +-
 docs/user-guide/brainstorm.md                      |   2 +-
 docs/user-guide/commands.md                        | 159 ++++-----------------
 docs/user-guide/flags.md                           |   6 +-
 docs/user-guide/freshness-hooks.md                 |   2 +-
 docs/user-guide/mcp-installation.md                | 114 +++------------
 docs/user-guide/mcp-servers.md                     |  41 ++----
 docs/user-guide/memory-system.md                   |   2 +-
 docs/user-guide/modes.md                           |   4 +-
 docs/user-guide/session-management.md              |  33 +++--
 22 files changed, 184 insertions(+), 643 deletions(-)

diff --git a/.github/workflows/test.yml b/.github/workflows/test.yml
--- a/.github/workflows/test.yml
+++ b/.github/workflows/test.yml
@@ -130,7 +130,7 @@ jobs:
   doctor-check:
     name: SuperClaude Doctor Check
     runs-on: ubuntu-latest
-    # `superclaude install` runs the unpinned upstream Codebase Memory installer;
+    # `superclaude install` registers and retires user-scope MCP servers through the Claude CLI;
     # keep the token read-only and out of .git/config while it runs.
     permissions:
       contents: read
@@ -152,7 +152,7 @@ jobs:
         with:
           node-version: "22"
 
-      # The required Codebase Memory phase of `superclaude install` needs the Claude CLI.
+      # `superclaude install` registers and retires user-scope MCP servers through the Claude CLI.
       - name: Install Claude CLI
         run: |
           npm install -g @anthropic-ai/claude-code@2.1.286
diff --git a/CHANGELOG.md b/CHANGELOG.md
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,59 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### Breaking: codebase-memory-mcp and Serena removed; session memory moves to `.superclaude/memory/` files (#323)
+
+#### Removed (codebase-memory-mcp and Serena)
+
+- `superclaude install` no longer installs codebase-memory-mcp (no download, no native setup, no required phase, no exit 1 for it). The installer module is deleted.
+- `superclaude mcp` loses `--uninstall` and `--yes`. Its menu is now "1. Install MCP servers (default)" and "2. Cancel". `codebase-memory-mcp` and `serena` are no longer registry servers: `superclaude mcp --servers serena` now says "Unknown MCP server selection: serena".
+- Serena is gone from the MCP registry, the package assets, the freshness hook matcher and the primitives' tool steps. Every command, skill and agent that used Serena symbol, reference, diagnostics or memory tools now uses a native Grep/Read floor.
+- Serena session memory is replaced by plain markdown files under `<project>/.superclaude/memory/` (one store per worktree). `/sc:save`, `/sc:load`, `/sc:pm` and the PM agent read and write those files. For one release `/sc:load` still reads an existing project `.serena/memories/<key>.md` when the matching `.superclaude/memory/` file is absent; it never writes there and tells you that folder is read-only history.
+- `/sc:reflect` loses `--onboard` and `--with-hierarchy`.
+
+#### Added (retire step)
+
+- At its end, `superclaude install` runs a bounded, non-fatal retire step (10 seconds per `claude` call, 15 seconds for the whole step; no outcome changes the install exit code). It removes only **user-scope** registrations of `codebase-memory-mcp` and `serena` that IronClaude can prove it wrote, plus IronClaude's own receipt and marker files (`~/.local/bin/.superclaude-codebase-memory.json` and `.pending`) once their binary is gone.
+- It keeps every shape it cannot prove (for example a registration Coder's bundle also writes) and prints the exact `claude mcp remove <name> --scope user` command for it. Local-scope and project `.mcp.json` entries are never touched.
+- It never touches binaries, uv tools, indexes, caches or memories.
+- The current-pin Serena registration (`uvx --from serena-agent==1.7.0 ...`) is not kept for good: it is kept, with the removal command printed on each install, only until the first `superclaude install` run in which the codegraph tools are installed and ready; that run removes it.
+- `superclaude install --list` shows one line per retired name (absent, will be removed, or kept with the reason). `superclaude doctor` warns, never fails, when something removable is left. `superclaude update` only prints "legacy registration present: run `superclaude install`".
+- After a removal, restart running Claude sessions: a running session can write the entry back. Check with `superclaude install --list`.
+
+#### Manual cleanup (IronClaude does not do these)
+
+To keep using Serena yourself, register it under the name `serena-local`, which the installer never removes:
+
+```bash
+claude mcp add --scope user serena-local -- uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false
+```
+
+For a codebase-memory you or IronClaude installed under `~/.local/bin` (this removes its own client companions and keeps its indexes; use the absolute path, because a bare command could resolve to Coder's copy):
+
+```bash
+"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"
+```
+
+If you installed Serena as a uv tool yourself (Coder workspaces reinstall it at start):
+
+```bash
+uv tool uninstall serena-agent
+```
+
+To remove a registration the retire step kept:
+
+```bash
+claude mcp remove codebase-memory-mcp --scope user
+claude mcp remove serena --scope user
+```
+
+Delete the data only if you no longer need it; IronClaude never deletes it:
+
+```bash
+rm -rf ~/.cache/codebase-memory-mcp   # codebase-memory indexes
+rm -rf ~/.serena                      # Serena's user data; project .serena/ folders are yours to delete
+```
+
 ### ccsession: tiers by Coder role, letter tier names, and the new tier layout
 
 #### Added (ccsession tier rules)
diff --git a/CLAUDE.md b/CLAUDE.md
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -374,7 +374,6 @@ superclaude mcp  # Interactive install, gateway is default (requires Docker)
 
 - **Tavily**: Web search (Deep Research)
 - **Context7**: Official documentation (prevent hallucination)
-- **Serena**: Session persistence
 
 **Built-in install, successful fresh-template path: Mindbase and Airis Agent are disabled.** When the installer downloads the backend configuration (`mcp-config.json`) and parses it, it marks any `mindbase` and `airis-agent` entries `enabled: false`, because their containers are not in the distribution Compose file (`src/superclaude/cli/install_mcp.py`). Other paths differ: an already-existing `mcp-config.json` is reused unchanged, a failed download (non-zero exit) writes a minimal default config, any other exception writes an empty config, and an unparseable download is used as-is. Do not assume every installation matches, and whether the gateway honors the disabled flag at runtime is UNVERIFIED. The manual guides (`src/superclaude/mcp/MCP_Mindbase.md`, `src/superclaude/mcp/MCP_Airis-Agent.md`) describe a separate git clone plus `docker compose up` deployment; whether MindBase is available there is UNVERIFIED.
 
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -35,7 +35,7 @@ The README reflects the product/function of the repo first, while preserving the
 - **CLI-driven workflows** for roadmap, tasklist, sprint, audit, and validation
 - **Claude Code asset distribution** through commands, agents, and skills
 - **PM-agent patterns** for confidence, self-check, and reflexion
-- **MCP-aware development** with integrations such as Auggie, Serena, Tavily, and Context7
+- **MCP-aware development** with integrations such as Auggie, Tavily, and Context7
 - **Contributor workflow support** with source/dev-mirror sync between `src/superclaude/` and `.claude/`
 - **Context freshness hooks** (v4.3) — seven active shell hooks that inject a per-turn `<session-context>` envelope and block edits against files that have not been Read in the last 30 minutes. See [`docs/user-guide/freshness-hooks.md`](docs/user-guide/freshness-hooks.md).
 
@@ -61,7 +61,7 @@ pipx install git+https://github.com/IronbellyOrg/IronClaude
 superclaude install
 ```
 
-This installs the package, then framework assets (core files, commands, agents, skills, ccsession wiring, hooks, templates and user setup), followed by **required user-level Codebase Memory MCP setup on Linux amd64/arm64**. Native setup includes upstream's full detected-client/companion integrations and retains graph indexes. If that required phase fails, installation exits 1 but keeps completed framework work. See the [MCP installation guide](docs/user-guide/mcp-installation.md) for prerequisites, unsupported-platform limits, upstream trust and safe removal. Installing from the repository URL needs read access to it.
+This installs the package, then framework assets (core files, commands, agents, skills, ccsession wiring, hooks, templates and user setup), followed by a bounded, non-fatal cleanup of old user-level MCP registrations that IronClaude wrote itself. See the [MCP installation guide](docs/user-guide/mcp-installation.md) for details. Installing from the repository URL needs read access to it.
 
 ### Install from source for development
 
@@ -72,7 +72,7 @@ git clone https://github.com/IronbellyOrg/IronClaude
 cd IronClaude
 uv venv                    # make install runs `uv pip install -e`, which needs an environment
 make install
-uv run superclaude install # framework assets + required user Codebase Memory setup (Linux)
+uv run superclaude install # framework assets + user-level MCP cleanup
 make verify
 ```
 
@@ -216,7 +216,6 @@ IronClaude is built to work with MCP-assisted workflows.
 Common integrations referenced in this repository include:
 
 - Auggie
-- Serena
 - Tavily
 - Context7
 - Playwright
diff --git a/SECURITY.md b/SECURITY.md
--- a/SECURITY.md
+++ b/SECURITY.md
@@ -325,7 +325,6 @@ For organizations requiring extended security support:
 **Magic**: UI generation with output validation and XSS prevention
 **Playwright**: Browser automation with sandboxed execution environment
 **Morphllm**: Code transformation with input validation and safety checks
-**Serena**: Memory management with secure data persistence and access controls
 
 **Network Security:**
 
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
