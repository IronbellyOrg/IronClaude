5dc6e2142c5840df0a79a3f9f14cd3de8fcc0050
Review one task for spec compliance.

Task brief: ## Task 1: Record the test baseline, commit the planning files and hand off to Coder

Implements `./source.md` §5 preconditions (baseline) and T0. Record the baseline before any source change, exactly as in §5:

```bash
mkdir -p .dev/codegraph-migration/evidence
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > .dev/codegraph-migration/evidence/P2-baseline-failures.txt
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json
```

Then stage `.dev/codegraph-migration` (specs, handoff, decisions, evidence baseline) and `.dev/tasks`, commit `docs(plan): Phase 2 codegraph install spec and Coder handoff (#323)`, push with `git push origin ironbelly/feat-codememory-codegraph-init`, and post an issue-#323 comment that links `.dev/codegraph-migration/handoff/coder-handoff-prompt.md` on the branch and asks for the Coder work to start (human item 5 of `./source.md` §7).

Acceptance criteria (AC ids in source order: T1.AC1 = first bullet, T1.AC2 = second, T1.AC3 = third, T1.AC4 = fourth bullet with its code block):
- `.dev/codegraph-migration/evidence/P2-baseline-failures.txt` exists and every line matches `^(FAILED|ERROR) tests/`.
- `git ls-files --error-unmatch .dev/codegraph-migration/handoff/coder-handoff-prompt.md .dev/codegraph-migration/handoff/coder-handoff-context.md` exits 0.
- `gh api "repos/IronbellyOrg/IronClaude/contents/.dev/codegraph-migration/handoff/coder-handoff-prompt.md?ref=ironbelly/feat-codememory-codegraph-init" --jq .name` prints `coder-handoff-prompt.md`.
- The commit holds nothing under `.claude/` except `.claude/settings.json` (this block exits 0; the hard rule of `./source.md` §7):
```bash
git diff --name-only HEAD~1 HEAD > /tmp/p2-t1-files.txt
if rg '^\.claude/' /tmp/p2-t1-files.txt | rg -v '^\.claude/settings\.json$'; then exit 1; fi
```
(Package root for ./artifacts paths: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/; source spec: .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md. The commit 79239d00 holds the task's git/gh work; the diff below is the product change since the start snapshot, and you may run read-only git/gh commands to verify the commit, push and AC3.)
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
Start sha: 5dc6e2142c5840df0a79a3f9f14cd3de8fcc0050
Diff against the start snapshot: diff --git a/.dev/codegraph-migration/evidence/P2-baseline-failures.txt b/.dev/codegraph-migration/evidence/P2-baseline-failures.txt
new file mode 100644
index 00000000..bebfc33e
--- /dev/null
+++ b/.dev/codegraph-migration/evidence/P2-baseline-failures.txt
@@ -0,0 +1,5 @@
+FAILED tests/cli/eval/test_ban_import_rule.py::test_ban_message_references_fr_g1
+FAILED tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check
+FAILED tests/cli/eval/test_ban_import_rule.py::test_synthetic_import_anthropic_is_flagged_by_ruff
+FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval
+FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module
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
