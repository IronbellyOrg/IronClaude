ef67a5e173d3d416b3b60e36ea394cd86a8f91da
Review one task for spec compliance.

Task brief: ## Task 13: Record the isolated-HOME install, index and tool-list proof (T9)

Depends on: Task 12

Implements `./source.md` T9 and §4.2 (layer 2, steps 1-8 including 5b): save the §4.2 script as `.dev/codegraph-migration/evidence/p2-layer2.sh`, run it (needs network to GitHub, a working `claude`, `uv sync` once beforehand, and Tasks 4-9 committed because it clones the worktree), and keep its output `.dev/codegraph-migration/evidence/P2-layer2.md`. If step 5's `claude mcp get` cannot run in the sandbox, apply the §4.2 Notes fallback (stdio `initialize` + `tools/list`, asserting `serverInfo.name == "codegraph"`) and record that in `P2-layer2.md`. If a real Claude Code session can be started in a fresh clone, record whether the hook's background `init` survives the hook and the session's end (`pgrep -f 'codegraph\.js init'`); otherwise record "process-group survival inside Claude Code: UNVERIFIED". Commit `test(codegraph): record isolated-HOME install and index evidence`. Group G4 commit point: then post the G4 issue comment including the T9 outputs.

Acceptance criteria (AC ids in source order: T13.AC1 = the first bullet with its code block, T13.AC2 = the assertions-cover bullet, T13.AC3 = the G4 comment bullet):
- This block exits 0:
```bash
bash -n .dev/codegraph-migration/evidence/p2-layer2.sh
bash .dev/codegraph-migration/evidence/p2-layer2.sh
test "$(tail -1 .dev/codegraph-migration/evidence/P2-layer2.md)" = LAYER2_OK
```
- The script's assertions cover: verified download and registration including `env.CODEGRAPH_MCP_TOOLS`, idempotency with a dead proxy, offline reuse, real index and query, MCP connection, step 5b tool list equal to `MCP_TOOLS` with `codegraph_explore` absent and its call failing, Serena and kind-B retirement, real hook init, codegraph-unavailable case keeping Serena, real HOME unchanged.
- The G4 comment exists on issue #323.
(Package root for ./artifacts paths: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/; source spec: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md, section 4.2 and T9. The change is commit 3a5201fc, pushed to origin. The script was already run once (exit 0); you may re-run it, it takes about two minutes, needs network and uses only a temporary HOME. A copy of the G4 comment is ./artifacts/t13-g4-comment.md and it is the newest comment on issue #323.)
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
Start sha: ef67a5e173d3d416b3b60e36ea394cd86a8f91da
Diff against the start snapshot: Commit 3a5201fc "test(codegraph): record isolated-HOME install and index evidence" holds the whole change. Read it with: git diff --no-renames ef67a5e173d3d416b3b60e36ea394cd86a8f91da -- .dev/codegraph-migration
New: .dev/codegraph-migration/evidence/p2-layer2.sh (the spec 4.2 script, saved unchanged), .dev/codegraph-migration/evidence/P2-layer2.md (its output), .dev/codegraph-migration/evidence/P2-hook-session.md (the in-session hook observation), a row in .dev/codegraph-migration/decisions/P2X-log.md, plus package ledger and retry bookkeeping only. Commits from Tasks 10-12 earlier in this group are not part of this task's diff.
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
