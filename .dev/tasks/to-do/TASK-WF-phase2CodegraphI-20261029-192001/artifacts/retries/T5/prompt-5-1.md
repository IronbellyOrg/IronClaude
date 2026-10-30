5326cd02aa4c12263319002e40ed3c63026a0f2f
Review one task for spec compliance.

Task brief: ## Task 5: Register codegraph at user scope with exact-entry repair (T2 steps 1-2)

Depends on: Task 4

Implements `./source.md` T2 steps 1-2, F2 (a)-(e), §2.4 (registration JSON with `CODEGRAPH_MCP_TOOLS` from `MCP_TOOLS`, `claude --version` checked before discovery and acquisition, entry table: absent / equal / owned / user-managed, bounded argv runner with `start_new_session=True`, 10 s and 60 s timeouts), §2.11, and tests U11-U19, U23, U25 plus the registry and dispatch tests of §4.1, in `src/superclaude/cli/install_mcp.py`, `tests/cli/test_install_codegraph.py` and `tests/cli/test_install_mcp_registry.py`. Step 1 is the sandbox `add-json` shape probe of `./source.md` T2 (writes `.dev/codegraph-migration/evidence/P2-add-json-shape.json`); if `claude mcp add-json` exits non-zero there, stop and take a mid-level decision. Step 2 finds the helpers with the `rg` command of T2 and adds a `name` parameter or re-creates missing ones from `git show 55d40308:src/superclaude/cli/install_mcp.py`. Commit `feat(mcp): register codegraph at user scope with exact-entry repair`. Group G1 commit point: then post the G1 issue comment.
Acceptance criteria (AC ids in source order: T5.AC1 = the first bullet with its code block, T5.AC2 = the pytest bullet, T5.AC3 = the -k codegraph bullet, T5.AC4 = the U11/U12/U14 bullet, T5.AC5 = the jq type bullet, T5.AC6 = the G1 comment bullet):
- The step-1 probe leaves the real `.mcpServers` hash unchanged, and this block exits 0 (or the shape difference is logged as a decision and the matcher follows the stored shape):
```bash
MT=$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md); test -n "$MT"
E=$(jq -cn --arg t "$MT" '{"type":"stdio","command":"/opt/x/bin/codegraph","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1","CODEGRAPH_MCP_TOOLS":$t}}')
jq -e --argjson e "$E" '. == $e' .dev/codegraph-migration/evidence/P2-add-json-shape.json
```
- `uv run pytest tests/cli/test_install_codegraph.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/recommend -q -p no:cacheprovider` passes.
- `uv run pytest tests/cli/test_install_mcp_registry.py -q -p no:cacheprovider -k codegraph` selects and passes the registry-contract and dispatch tests (not "0 selected").
- U11 asserts a failing `claude --version` fails the phase before discovery or download; U12 asserts the add-json JSON carries `env.CODEGRAPH_MCP_TOOLS == install_codegraph.MCP_TOOLS`; U14 replaces an owned entry whose env lacks that key.
- `jq -e 'type == "object"' .dev/codegraph-migration/evidence/P2-add-json-shape.json` exits 0.
- The G1 comment exists on issue #323.
(Package root for ./artifacts paths: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/; source spec: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md, sections 2.4, 2.11, 4.1, T2 steps 1-2. The change is commit 5b493cae, pushed to origin; the G1 comment is https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6523047354 and you may read it with gh.)
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
Start sha: 5326cd02aa4c12263319002e40ed3c63026a0f2f
Diff against the start snapshot: Commit 5b493cae "feat(mcp): register codegraph at user scope with exact-entry repair" holds the whole change. Read it with: git diff --no-renames 5326cd02aa4c12263319002e40ed3c63026a0f2f -- src tests .dev/codegraph-migration
Changed or new: src/superclaude/cli/install_mcp.py (registry entry, dispatch, bounded runner refactor, registration helpers, install_codegraph_mcp), src/superclaude/cli/install_codegraph.py (import http.client and catch HTTPException in the download), tests/cli/test_install_codegraph.py (U11-U19, U23, U25 added), tests/cli/test_install_mcp_registry.py (codegraph contract, dispatch, listing), tests/cli/test_install_mcp_cli.py (the install-all menu test now fakes the codegraph phase), .dev/codegraph-migration/evidence/P2-add-json-shape.json (new, from the sandbox probe), .dev/codegraph-migration/decisions/P2X-log.md (rows added), plus package ledger and retry bookkeeping only. ruff format was applied.
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
