c6b097d5fef6aa33c51da4dfbfaef98e4d55f828
Review one task for spec compliance.

Task brief: ## Task 3: Run the tool-list schema-cost check and choose `MCP_TOOLS` (T2 step 0)

Depends on: Task 2

Implements `./source.md` §2.4 "Tool list" and T2 "Step 0" (review findings X-1, X-25), with the method of `.dev/codegraph-migration/decisions/F2-schema-cost-method/adversarial/F2-schema-cost-method-merged.md` §1-§7 (authoritative for every detail). Needs no repository code, so it runs before Task 4.
- First action, from the worktree root: `A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts`, `mkdir -p "$A"`, `A=$(realpath "$A")` (absolute, so it survives `cd` into `$W`), and `jq -S '.mcpServers' ~/.claude.json | sha256sum > /tmp/p2-t3-h0.txt`.
- Save the stdio client given verbatim in `./source.md` T2 step 0 as `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs`.
- Leg A (always): private `mktemp -d` dir with sandbox `HOME`/`CLAUDE_CONFIG_DIR` and telemetry off; download the pinned v1.6.2 tarball for this platform, verify its SHA-256 against `./source.md` §0 before extracting (mismatch: stop, human item 2), extract, `git init -q` a tiny repo, run the client twice from it (run 1 with `CODEGRAPH_MCP_TOOLS` unset, run 2 with `node,search,callers,callees,impact,files,status`), writing the outputs straight to `"$A/t3-run1.json"` and `"$A/t3-run2.json"` (absolute, so they survive `rm -rf "$W"`), and compute `D` and the recorded data fields.
- X-25 hard stop: run 2 lists exactly the seven `codegraph_*` tools (no `codegraph_explore`) and its `explore_call_error` is `true`; otherwise stop, write no value, log a mid-level decision.
- Bands: `D <= 6000` bytes gives the seven tools; `D > 8000` gives `status`; in between, Leg B (four headless `claude -p` runs with `--strict-mcp-config`, ABAB order, `.mcpServers` hash guard, validity guards a-d of the merged method §5) decides; Leg B not run or invalid gives `status` and the non-blocking human item 6 of `./source.md` §7.
- If the value is `status`, apply the §2.4 failure branch: every literal seven-tool value in `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`, its §3.4 first sentence, and both Coder handoff files under `.dev/codegraph-migration/handoff/` is replaced in the same commit as Task 4.
- Write `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md` with the 16 one-fact lines of the merged method §7, ending `Selected MCP_TOOLS: <value>`.

Acceptance criteria (one AC: T3.AC1 = the single bullet with its code block):
- This block exits 0:
```bash
node --check .dev/codegraph-migration/evidence/p2-mcp-tools.mjs
test "$(wc -l < .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md)" -eq 16
tail -1 .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md | rg -q '^Selected MCP_TOOLS: (node,search,callers,callees,impact,files,status|status)$'
rg -qx 'Explore hidden: yes' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md
rg -qx 'Explore call blocked: yes' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md
A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts
jq -e '(.tools | map(.name) | index("codegraph_explore")) == null and .explore_call_error == true' "$A/t3-run2.json"
test "$(jq -S '.mcpServers' ~/.claude.json | sha256sum)" = "$(cat /tmp/p2-t3-h0.txt)"
```
(Package root for ./artifacts paths: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/; source spec: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md, whose lines 487-529 hold T2 step 0 and the client text. Merged method: .dev/codegraph-migration/decisions/F2-schema-cost-method/adversarial/F2-schema-cost-method-merged.md. The commit for this task is deferred to Task 4 by the plan, so all outputs are uncommitted.)
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
Start sha: c6b097d5fef6aa33c51da4dfbfaef98e4d55f828
Diff against the start snapshot: New untracked files since the start snapshot (read each from disk):
 - .dev/codegraph-migration/evidence/p2-mcp-tools.mjs (the stdio client; compare with source.md lines 489-521)
 - .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/t3-run1.json, t3-run2.json, t3-legB-summary.txt
 - .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md, full contents:
Bytes delta D: 7597
Model-facing delta: 7107
Instructions bytes run1/run2: 1157/1157
Per-tool bytes: codegraph_explore=1747 (run 1 only), codegraph_search=1132, codegraph_callers=1096, codegraph_callees=1052, codegraph_impact=1028, codegraph_node=2887, codegraph_status=741, codegraph_files=1402
D without node (data only, P3-D1 owns any smaller list): 4710
Band: undecided
Explore hidden: yes
Explore call blocked: yes
Session measurement: run1-default=36980, run2-seven=38841, run3-default=36980, run4-seven=38841 tokens (input+cache_creation+cache_read); T=1861; guards a-d hold (T >= D/5 = 1519)
Deferred: no
Decided by: B
Claude Code version: 2.1.314 (Claude Code)
Model: haiku
INV-015: waived (Leg B used a codegraph-only config; the delta is additive and the retire step removes the codebase-memory registration once codegraph is ready, spec 2.12)
Threshold status: proposed, not user-confirmed
Selected MCP_TOOLS: node,search,callers,callees,impact,files,status
Also changed: package ledger progress.md and retry bookkeeping only.
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
