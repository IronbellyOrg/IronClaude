bbdd2f6cbe02537ba096dc8dba13fee82507ab57
Review one task for spec compliance.

Task brief: ## Task 7: Retire Serena registrations once codegraph is ready (T3b)

Depends on: Task 6

Implements `./source.md` T3b, F18 and §2.12: `codegraph_ready()` in `src/superclaude/cli/install_mcp.py`, the gate passed from `src/superclaude/cli/main.py` into `src/superclaude/cli/install_retired_mcp.py` (removal by launcher shape under any name except `serena-local`, `env`/`headers` absent or `{}`, kind-B `~/.local/bin/codebase-memory-mcp` registration, printed argv and `uninstall -y` command), the `Ready for Serena retirement` line of the §2.8 `--list` block, with the test matrix of T3b in Phase 1's retire-step test file and `tests/cli/test_update_command.py`. Commit `feat(install): retire Serena registrations once codegraph is ready (#323)`.

Acceptance criteria (AC ids in source order: T7.AC1 = the first bullet with its code block, T7.AC2 = the 'Tests prove' bullet):
- This block exits 0 (the assignment aborts under `-e` when no retire-step test file exists, so the gate can never run without it):
```bash
F=$(rg -l -g '*.py' install_retired_mcp tests)
test -n "$F"
uv run pytest $F tests/cli/test_update_command.py tests/cli/test_install_codegraph.py -q -p no:cacheprovider
uv run pytest $F -q -p no:cacheprovider -k "codegraph and serena"
test ! -e .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md || rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md
```
- Tests prove: codegraph failed keeps the current-pin Serena entry and exits 1; ready removes `serena` and a non-`serena` `start-mcp-server` launcher with `"env":{}`; non-empty `env`/`headers` are kept; `serena-local` is never removed; a second run is a no-op; Tier R and `/usr/local/bin/codebase-memory-mcp` removal stay unconditional; `install` and `install --list` read the same `codegraph_ready()` and `--list` prints `Ready for Serena retirement: yes | no (<reason>)`.
(Package root for ./artifacts paths: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/; source spec: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md, sections 2.12, 2.8 and T3b. The change is commit a9a1a477.)
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
Start sha: bbdd2f6cbe02537ba096dc8dba13fee82507ab57
Diff against the start snapshot: Commit a9a1a477 "feat(install): retire Serena registrations once codegraph is ready (#323)" holds the whole change. Read it with: git diff --no-renames bbdd2f6cbe02537ba096dc8dba13fee82507ab57 -- src tests .dev/codegraph-migration
Changed: src/superclaude/cli/install_mcp.py (read_user_mcp_servers split out of read_user_mcp_entry, codegraph_ready, codegraph_ready_line, the Ready line in codegraph_list_lines), src/superclaude/cli/install_retired_mcp.py (ready parameter through the classifiers, renamed-launcher sweep, run_retire_step(codegraph_ready), list_lines/update_notice/doctor_warning use the shared predicate), src/superclaude/cli/main.py (passes codegraph_success and codegraph_ready()[0] to the retire step), src/superclaude/cli/install_codegraph.py (reports_pinned_version made public), tests/cli/test_install_retired_mcp.py (gate tests, one existing stub signature widened), tests/cli/test_install_codegraph.py (codegraph_ready tests), .dev/codegraph-migration/decisions/P2X-log.md (rows), plus package ledger and retry bookkeeping only. The doctor use of codegraph_ready is Task 8. ruff format was applied.
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
