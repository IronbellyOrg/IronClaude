0cf7d600f667643a3928247068b4e7f81a03fe3b
Review one task for spec compliance.

Task brief: ## Task 9: Replace origin/master in the two command files and the eval data

Edit three files (design section 3.5 in `./source.md`): `src/superclaude/commands/impact.md` line 23, `src/superclaude/commands/auggie-review.md` lines 37 and 113, and `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` lines 19 and 20.

- `impact.md:23`: `/sc:impact --diff origin/master --tests` becomes `/sc:impact --diff origin/integration --tests`.
- `auggie-review.md:37` and `:113`: `--diff origin/master...HEAD` becomes `--diff origin/integration...HEAD`.
- `evals.json:19`: the prompt text `--diff origin/master...HEAD ...` becomes `origin/integration...HEAD`, and its prose "against master" becomes "against integration". `evals.json:20`: the expected-output text "against master" becomes "against integration" and `git diff --stat origin/master...HEAD` becomes `git diff --stat origin/integration...HEAD`. The JSON stays valid and no other eval entry changes.
- Edit only text that names the example branch; keep every flag and sentence otherwise.

Acceptance criteria:
- `grep -rn 'origin/master' src/superclaude` prints nothing, and `grep -n 'against master' src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` prints nothing.
- `uv run python -c "import json; json.load(open('src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json'))"` exits 0.
- `uv run pytest tests/commands/test_impact_command.py tests/commands/test_auggie_review_revagent.py tests/commands/test_auggie_review_remediation_chain.py -q` passes.


AC ids (source order):
T9.AC1 = `grep -rn 'origin/master' src/superclaude` prints nothing, and `grep -n 'against master' src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` prints nothing.
T9.AC2 = `uv run python -c "import json; json.load(open('src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json'))"` exits 0.
T9.AC3 = `uv run pytest tests/commands/test_impact_command.py tests/commands/test_auggie_review_revagent.py tests/commands/test_auggie_review_remediation_chain.py -q` passes.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 0cf7d600f667643a3928247068b4e7f81a03fe3b
Diff against the start snapshot: diff --git a/src/superclaude/commands/auggie-review.md b/src/superclaude/commands/auggie-review.md
index 49a76c29e..c8522569c 100644
--- a/src/superclaude/commands/auggie-review.md
+++ b/src/superclaude/commands/auggie-review.md
@@ -34,7 +34,7 @@ The trigger discipline exists because deep reviews are expensive (Auggie indexin
 ```bash
 /sc:auggie-review 62                                    # Review PR #62 (auto-detect repo)
 /sc:auggie-review https://github.com/org/repo/pull/62   # Review PR by URL
-/sc:auggie-review --diff origin/master...HEAD           # Review local branch changes
+/sc:auggie-review --diff origin/integration...HEAD      # Review local branch changes
 /sc:auggie-review --snapshot src/superclaude/cli/       # Review a subtree (no diff)
 /sc:auggie-review 62 --focus security,architecture      # Focus areas only
 /sc:auggie-review 62 --depth deep --no-post-pr          # Deep review, do not post to PR
@@ -110,7 +110,7 @@ External tool (not MCP, but central): **`auggie` CLI** is the primary review eng
 ### Review uncommitted local changes
 
 ```text
-/sc:auggie-review --diff origin/master...HEAD --no-post-pr
+/sc:auggie-review --diff origin/integration...HEAD --no-post-pr
 # - Same protocol, but target is git diff, no PR posting
 # - Useful pre-commit / pre-push self-review
 ```
diff --git a/src/superclaude/commands/impact.md b/src/superclaude/commands/impact.md
index 3b333a47e..b52ba8f50 100644
--- a/src/superclaude/commands/impact.md
+++ b/src/superclaude/commands/impact.md
@@ -20,7 +20,7 @@ Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without
 /sc:impact parse_config                         # dependents of one symbol
 /sc:impact load_spec write_report --depth 3     # several symbols, three hops
 /sc:impact --diff                               # symbols changed in the working tree vs HEAD
-/sc:impact --diff origin/master --tests         # symbols a branch changed, plus advisory tests
+/sc:impact --diff origin/integration --tests         # symbols a branch changed, plus advisory tests
 /sc:impact parse_config --caller sc-implement-protocol --output-dir .dev/impact/t3
 /sc:impact parse_config --unattended --report-dir .dev/impact/run1   # worker mode: contract written there
 ```
diff --git a/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json b/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json
index d3298d1a9..68713196d 100644
--- a/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json
+++ b/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json
@@ -16,8 +16,8 @@
     {
       "id": 2,
       "name": "local-diff-vs-master",
-      "prompt": "Run /sc:auggie-review --diff origin/master...HEAD --no-post-pr --depth quick --output-dir /tmp/eval-diff/. This will review the uncommitted/branch changes against master. Use --focus quality,anti-patterns,architecture. At the end, print the report path and a one-line summary.",
-      "expected_output": "A REVIEW.md at /tmp/eval-diff/ scoped to the diff against master. Findings (if any) must cite files actually in the diff. Diff statistics should match `git diff --stat origin/master...HEAD`.",
+      "prompt": "Run /sc:auggie-review --diff origin/integration...HEAD --no-post-pr --depth quick --output-dir /tmp/eval-diff/. This will review the uncommitted/branch changes against integration. Use --focus quality,anti-patterns,architecture. At the end, print the report path and a one-line summary.",
+      "expected_output": "A REVIEW.md at /tmp/eval-diff/ scoped to the diff against integration. Findings (if any) must cite files actually in the diff. Diff statistics should match `git diff --stat origin/integration...HEAD`.",
       "files": [],
       "assertions": [
         { "text": "Output file /tmp/eval-diff/REVIEW.md exists after the eval completes", "type": "file_exists", "path": "/tmp/eval-diff/REVIEW.md" },

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
