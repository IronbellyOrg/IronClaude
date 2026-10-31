d618148185bc3c28718348ec1eeaf79c79a7dc19
Review one task for spec compliance.

Task brief: ## Task 15: Open or update the shared Phase 1 + Phase 2 PR on the fork (T11)

Depends on: Task 14

Implements `./source.md` T11 and §8. After the project `CLAUDE.md` pre-PR checks (`git remote -v` shows origin `IronbellyOrg/IronClaude`; `gh repo view --json nameWithOwner -q .nameWithOwner` prints `IronbellyOrg/IronClaude`; rebase onto `origin/master` if it moved), run `/sc:pr-submit --monitor 3 --head ironbelly/feat-codememory-codegraph-init --title "feat: replace codebase-memory and Serena with codegraph (#323)" --body "<Phase 1 + Phase 2 summary; links to both specs>"`; if the Phase 1 executor already opened the PR, push to it instead. Do not merge (human item 3). Commit point: none for this task (PR only). Group G5 commit point: then post the G5 issue comment with the PR URL and the Coder ordering status, plus the merge-gate output below.

Acceptance criteria:
- `gh pr view ironbelly/feat-codememory-codegraph-init --repo IronbellyOrg/IronClaude --json url -q .url` prints a URL starting `https://github.com/IronbellyOrg/IronClaude/pull/`.
- `gh pr checks ironbelly/feat-codememory-codegraph-init --repo IronbellyOrg/IronClaude` shows every check passing, including `doctor-check`.
- The three merge-gate commands of `./source.md` T11 (Coder `Dockerfile.coder` has the pinned linux-x64 hash; test-57 asserts a codegraph registration; the bundle `install.sh` no longer sets `SERENA_PIN` or `uv tool install`s `serena-agent`) are run and their output is in the G5 comment; the comment says "do not merge" unless all three print.

Evidence you may verify yourself with READ-ONLY commands (gh pr view/checks/api GET, git log/diff, Read); do not post, push or edit anything:
- PR: https://github.com/IronbellyOrg/IronClaude/pull/329 (head cf4e0f1b4df929ba15a95e01add4392aee8a6b77). `gh pr checks 329 --repo IronbellyOrg/IronClaude`.
- The G5 comment: https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6525109011 (copy at .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/t15-g5-comment.md).
- The three merge-gate commands are in .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md lines 700-707. Re-run them (read-only gh api GETs) and compare with the comment table: expect 1 prints, 2 and 3 do not.
- Two fix commits were pushed during the Augment review: 184482fe (test change + evidence file) and cf4e0f1b (ruff format).
Note: the plan says "every check passing, including `doctor-check`"; the CI job that exists for it is named "SuperClaude Doctor Check".
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
Start sha: d618148185bc3c28718348ec1eeaf79c79a7dc19
Diff against the start snapshot: diff --git a/.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt b/.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt
new file mode 100644
index 00000000..782ca59f
--- /dev/null
+++ b/.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt
@@ -0,0 +1,5 @@
+# SHA256SUMS lines of github.com/colbymchenry/codegraph release v1.6.2, fetched 2026-10-30T14:07:34Z with gh release download. tests/cli/test_install_codegraph.py compares cg.SHA256 to these lines.
+d74d1bfb4060db63ec3c2b72c4e17f76c31978af3bad6ace4370d1501ac0662e  codegraph-darwin-arm64.tar.gz
+53d1a4d1a9af31d6cec11b346df2ae792087081e13f623f583e27783c1e7f9bc  codegraph-darwin-x64.tar.gz
+c8c6be292be21d00dea26bad8b28d434731cf612fb8cc475dc10f5b3038b5b64  codegraph-linux-arm64.tar.gz
+ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828  codegraph-linux-x64.tar.gz
diff --git a/src/superclaude/cli/install_mcp.py b/src/superclaude/cli/install_mcp.py
index b4d29394..77ca26a4 100644
--- a/src/superclaude/cli/install_mcp.py
+++ b/src/superclaude/cli/install_mcp.py
@@ -1404,7 +1404,9 @@ def install_mcp_servers(
             selected = ["airis-mcp-gateway"]
         elif choice == "0":
             selected = [
-                name for name, info in MCP_SERVERS.items() if not info.get("opt_in_only")
+                name
+                for name, info in MCP_SERVERS.items()
+                if not info.get("opt_in_only")
             ]
         else:
             try:
diff --git a/tests/cli/test_install_codegraph.py b/tests/cli/test_install_codegraph.py
index 71afdcd6..7801a459 100644
--- a/tests/cli/test_install_codegraph.py
+++ b/tests/cli/test_install_codegraph.py
@@ -127,6 +127,14 @@ def test_u2_pin_integrity():
     assert set(cg.SHA256) == {"linux-x64", "linux-arm64", "darwin-x64", "darwin-arm64"}
     assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in cg.SHA256.values())
     assert cg.TAG == "v" + cg.VERSION
+    # The release's own checksum lines, fetched once; a mistyped pin fails here
+    # instead of at a user's first install (the acquisition tests swap the pin).
+    sums = REPO / ".dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt"
+    released = {
+        name: digest
+        for digest, name in (line.split() for line in sums.read_text().splitlines()[1:])
+    }
+    assert cg.SHA256 == {k: released[f"codegraph-{k}.tar.gz"] for k in cg.SHA256}
     evidence = REPO / ".dev/codegraph-migration/evidence/P2-mcp-tools-schema.md"
     selected = re.search(r"^Selected MCP_TOOLS: (.+)$", evidence.read_text(), re.M)
     assert selected and cg.MCP_TOOLS == selected.group(1)
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
