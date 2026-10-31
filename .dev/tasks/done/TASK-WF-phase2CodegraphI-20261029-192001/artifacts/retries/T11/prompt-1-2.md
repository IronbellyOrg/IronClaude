909e1d562fe164c74387e9e81ef63ebec00e4db8
Review one task for spec compliance.

Task brief: ## Task 11: Document the default codegraph install, indexing and removal (T7)

Depends on: Task 10

Implements `./source.md` T7, F8-F11 and F19 in `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`, `README.md`, `CHANGELOG.md` and `.gitignore` (`.codegraph/`): §2.6 removal commands, §2.10 failure table (short form), the registered tool list `CODEGRAPH_MCP_TOOLS` and why `codegraph_explore` is hidden (§2.4), §3.3 costs and the exact scope of `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (hook only; every switch uses the `SUPERCLAUDE_CODEGRAPH_` prefix, review X-14), the opt-in `post-checkout` recipe, the `core.excludesFile` tip, and §2.12 (Serena removed once codegraph is ready, `serena-local`, what is kept by policy, the escalated residuals). Commit `docs(mcp): document default codegraph install, indexing and removal`.

Acceptance criteria (one AC: T11.AC1 = the single bullet with its code block):
- This block exits 0:
```bash
uv run pytest tests/docs -q -p no:cacheprovider
for f in README.md docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md CHANGELOG.md; do rg -q codegraph "$f" || { echo "missing: $f"; exit 1; }; done
rg -q 'SUPERCLAUDE_CODEGRAPH_AUTOINIT=0' docs/user-guide/mcp-installation.md
rg -q 'claude mcp remove codegraph --scope user' docs/user-guide/mcp-installation.md
rg -q 'serena-local' docs/user-guide/mcp-installation.md
rg -q 'serena-local' CHANGELOG.md
rg -q 'CODEGRAPH_MCP_TOOLS' docs/user-guide/mcp-installation.md
rg -qx '\.codegraph/' .gitignore
if rg 'Legacy Serena registration kept' CHANGELOG.md | rg -v 'codegraph'; then exit 1; fi
```
(Package root for ./artifacts paths: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/; source spec: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md, sections 2.4, 2.6, 2.10, 2.12, 3.1, 3.3, F8-F11, F19. The change is commit 47518cb8.)
Global constraints: ## Constraints

- Planning source is `./source.md` (snapshot of `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`). Every task cites the source section it implements; details not repeated here are in that section.
- Preconditions (`./source.md` §5): branch `ironbelly/feat-codememory-codegraph-init`; Phase 1 tasks committed first (Phase 1 and Phase 2 land as one PR and one `master` merge, `./source.md` §8 and D12); `git status --short` clean apart from untracked `.dev/` content. Seams are located by function or block name, not by the `55d40308` line numbers (`./source.md` §1).
- Every acceptance command runs from the worktree root under `bash -euo pipefail` and must exit 0 if and only if its criterion passes. One condition per line: never `A && B` or `! cmd` in the middle of a block (errexit ignores both); write a negative check as `if cmd; then exit 1; fi`. Every `uv run pytest` uses `-p no:cacheprovider`. Run `git status --short` after each task; an unintended modified tracked file is a defect to fix before committing.
- Package evidence lives in this package's `artifacts/` folder (written `./artifacts/` in prose). Shell commands run from the worktree root, so they resolve it with `A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts` (the glob finds the package under `to-do/` or, after archiving, `done/`) and create it with `mkdir -p "$A"` before the first write.
- Tests are judged against the recorded baseline `.dev/codegraph-migration/evidence/P2-baseline-failures.txt` (the suite was not green at `55d40308`): no failing test id may appear outside it. After any full test run, restore `.dev/releases/current/cliEval/evidence/T02.15/perf.json` with `git checkout --` before committing.
- Hard rules (`./source.md` §7): never run `claude mcp add/remove` or `superclaude install` against the real HOME (sandbox HOMEs only, each asserting the real `.mcpServers` hash is unchanged; the one exception is the read-only `superclaude install --list`); never stage or commit anything under `.claude/` except `.claude/settings.json`; feature branch only; never push to `upstream`; PRs only on `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3` (fallback `gh pr create --repo IronbellyOrg/IronClaude`).
- `.dev/tasks/` is always staged (`git add .dev/tasks`) at every commit point, this package and its `artifacts/` included.
- Commit points: one conventional commit per task as named in each task, and every task group (phase) ends with a commit point followed by one issue-#323 progress comment, posted with `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file /tmp/p2-progress.md` using the body template of `./source.md` §6 (group, commit sha and subject, tasks done, exact test command and its result with failures reported as failures, decisions taken, next group). Never post progress anywhere else.
- Decision rules (`./source.md` §7): simple decisions (one obvious answer, or forced by a pinned test or verified constraint) the executor makes itself; mid-level decisions (two or more viable options with real trade-offs, local to one task) are written as `.dev/codegraph-migration/decisions/P2X-<slug>/option-<x>.md` files (under 40 lines each) and settled by an agent running `/sc:adversarial --compare <files> --depth quick`; complex decisions (installer contract §2, indexing design §3, release order §8, or Phase 1/3 ownership) use `/sc:adversarial --compare <files>` at default depth. Follow the recommendation; log every decision as a row in `.dev/codegraph-migration/decisions/P2X-log.md` (decision, options, method, rationale, folder) in the commit that applies it, and name the folder in the next issue comment.
- Human intervention only for the seven items of `./source.md` §7 (gh auth failure; a `SHA256SUMS` that differs from §0; merging the PR; running `./update.sh` on the real workspace; giving the Coder handoff prompt to a Coder agent; the non-blocking Leg B item; the non-blocking removal of a kept user-scope Serena entry found by Task 16). Never stop to ask otherwise.
Start sha: 909e1d562fe164c74387e9e81ef63ebec00e4db8
Diff against the start snapshot: Commit 47518cb8 "docs(mcp): document default codegraph install, indexing and removal" plus an uncommitted fix pass in the worktree. Read the whole change with: git diff --no-renames 909e1d562fe164c74387e9e81ef63ebec00e4db8 -- README.md CHANGELOG.md docs .gitignore .dev/codegraph-migration   (tree against worktree, so it includes the fix)
Changed: docs/user-guide/mcp-installation.md (new "Default setup: codegraph" section, intro sentence, server table row), docs/reference/mcp-server-guide.md (codegraph entry, lifecycle and troubleshooting section), README.md (two install lines), CHANGELOG.md (new "Added: codegraph installed by default" entry), .gitignore (.codegraph/), .dev/codegraph-migration/decisions/P2X-log.md (rows), plus package ledger and retry bookkeeping only. The fix pass edited two sentences in docs/user-guide/mcp-installation.md (see the delta diff).
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/docs/user-guide/mcp-installation.md b/docs/user-guide/mcp-installation.md
index 37cecf38..ec9eec45 100644
--- a/docs/user-guide/mcp-installation.md
+++ b/docs/user-guide/mcp-installation.md
@@ -51,9 +51,9 @@ A session-start hook (`~/.claude/hooks/codegraph-session-start.sh`, event `Sessi
 
 ### Serena is removed once codegraph is ready
 
-In the first `superclaude install` where codegraph is registered and usable (`Ready for Serena retirement: yes` in `install --list`), the cleanup step also removes every user-scope MCP entry other than `serena-local` that launches Serena (arguments contain `start-mcp-server`, `env` and `headers` absent or empty), whatever its name, and the `~/.local/bin/codebase-memory-mcp` registration. Until then the current-pin `serena` entry is kept and the removal command is printed. An entry with non-empty `env` or `headers` is kept and reported. To keep Serena, register it yourself as `serena-local`; the installer never removes that name.
+In the first `superclaude install` where codegraph is registered and usable (`Ready for Serena retirement: yes` in `install --list`), the cleanup step also removes every user-scope MCP entry other than `serena-local` that launches Serena (arguments contain `start-mcp-server`, `env` and `headers` absent or empty), whatever its name, and the `~/.local/bin/codebase-memory-mcp` registration. Until then the current-pin `serena` entry is kept and the removal command is printed. A launcher entry with non-empty `env` or `headers` is kept; the cleanup step reports that ("customised registration") only for an entry named `serena`, and says nothing about a renamed one. To keep Serena, register it yourself as `serena-local`; the installer never removes that name.
 
-Kept by policy: `~/.serena`, project `.serena/` folders, `~/.cache/codebase-memory-mcp`, the uv cache and, outside Coder, a `serena-agent` uv tool you installed (the removal command is printed). Local-scope (`projects.*.mcpServers`) and `.mcp.json` entries are reported with their exact `claude mcp remove ... --scope local` command, never removed automatically. The root-owned `/usr/local/bin/codebase-memory-mcp` in the Coder image goes only with a new image, and a `~/.local/bin/codebase-memory-mcp` binary with its client companions stays, with its `uninstall -y` command printed.
+Kept by policy: `~/.serena`, project `.serena/` folders, `~/.cache/codebase-memory-mcp`, the uv cache and, outside Coder, a `serena-agent` uv tool you installed (the removal command is printed). Local-scope (`projects.*.mcpServers`) and `.mcp.json` entries are never read or removed by the installer; if a project still registers `serena` or `codebase-memory-mcp` that way, run `claude mcp remove <name> --scope local` (or `--scope project` for `.mcp.json`) in that project. The root-owned `/usr/local/bin/codebase-memory-mcp` in the Coder image goes only with a new image, and a `~/.local/bin/codebase-memory-mcp` binary with its client companions stays, with its `uninstall -y` command printed.
 
 ## What `superclaude install` Does With MCP
 
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=T11.AC1 at=docs/user-guide/mcp-installation.md:56 anchor=src/superclaude/cli/install_retired_mcp.py:486-493 chk=n,y,n,n family=docs-claims-installer-reports-residuals fix=reword to say the installer never looks at local-scope and .mcp.json entries and the user removes them by hand with claude mcp remove <name> --scope local first=A1 origin=new: the paragraph says local-scope and .mcp.json entries "are reported with their exact claude mcp remove ... --scope local command", but superclaude install never reports them (no read of projects.*.mcpServers or .mcp.json anywhere in install_retired_mcp.py or install_mcp.py; read-back: grep for projects, mcp.json and scope local prints nothing)
F1.2 sev=blocking trigger=B2 ac=T11.AC1 at=docs/user-guide/mcp-installation.md:54 anchor=src/superclaude/cli/install_retired_mcp.py:274-282 chk=n,y,n,n family=docs-claims-installer-reports-residuals fix=say it is kept for any name and reported only for an entry named serena (customised registration) first=A1 origin=new: "An entry with non-empty env or headers is kept and reported" is true for serena but false for a renamed launcher, which is never added to the classifiers and so is skipped silently
Saved-probe re-check hit locations (may be empty): docs/user-guide/mcp-installation.md:54:In the first `supercl
docs/user-guide/mcp-installation.md:56:Kept by policy: `~/.s

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
