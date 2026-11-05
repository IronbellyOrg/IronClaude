f95e2dee41d6086f0a7a57cc800c309a9586ca2d
Review one task for spec compliance.

Task brief: ## Task 14: Run the full verification gate and fix what it finds (T10)

Depends on: Task 13

Implements `./source.md` T10: the final full verification of the branch before the PR. Fix any defect the gate finds in this phase's files only (commit `fix(codegraph): <what the gate found>` when a fix was needed). The block copies the run output and the new-failure list into `./artifacts/` before the gating line, so the evidence exists even when the gate fails; always commit that evidence afterwards (`test(codegraph): record final gate evidence`), so Task 15's rebase starts from a clean tree.
Acceptance criteria (AC ids in source order: T14.AC1 = the first bullet with its code block, T14.AC2 = the git status bullet, T14.AC3 = the committed-artifacts bullet):
Acceptance criteria:
- This block exits 0:
```bash
A=$(echo .dev/tasks/*/TASK-WF-phase2CodegraphI-20261029-192001)/artifacts
mkdir -p "$A"
make sync-dev
test -f .dev/codegraph-migration/evidence/P2-baseline-failures.txt
uv run pytest -p no:cacheprovider -q -rfE --tb=no tests > /tmp/p2-final-run.txt 2>&1 || true
cp /tmp/p2-final-run.txt "$A/t14-final-run.txt"
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json
grep -E '[0-9]+ passed' /tmp/p2-final-run.txt >/dev/null
if grep -E 'INTERNALERROR|Interrupted|no tests ran' /tmp/p2-final-run.txt; then exit 1; fi
{ grep -E '^(FAILED|ERROR) ' /tmp/p2-final-run.txt || true; } | sed 's/ - .*//' | sort > /tmp/p2-final-failures.txt
comm -13 .dev/codegraph-migration/evidence/P2-baseline-failures.txt /tmp/p2-final-failures.txt > /tmp/p2-new-failures.txt
cp /tmp/p2-new-failures.txt "$A/t14-new-failures.txt"
test ! -s /tmp/p2-new-failures.txt
make lint
make verify-sync
```
- `git status --short` shows no unintended tracked change, and nothing under `.claude/` except `.claude/settings.json` is staged.
- `./artifacts/t14-final-run.txt` and `./artifacts/t14-new-failures.txt` are committed; the latter is empty.
(Package root for ./artifacts paths: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/; source spec: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md, T10. The gate was run once as a script with bash -euo pipefail: exit 0. The evidence commit is aad73621. No defect was found, so no fix commit exists. The baseline file had 5 failing ids, all ruff-related tests that failed because ruff was not installed in the project environment at baseline time; ruff 0.15.20 was installed later with uv pip install, which is why the final run has zero failures.)
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
Start sha: f95e2dee41d6086f0a7a57cc800c309a9586ca2d
Diff against the start snapshot: Commit aad73621 "test(codegraph): record final gate evidence" holds the whole change: the gate output and the new-failure list in the package artifacts folder. Read it with: git show --stat aad73621
New: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/t14-final-run.txt, t14-new-failures.txt, plus package ledger and retry bookkeeping only. No source file changed in this task.
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
