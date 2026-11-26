be187ea7735a537d758314d09793370e6e04e01d
Review one task for spec compliance.

Task brief: ## Task 10: Replace origin/master in the user guide examples

Edit `docs/user-guide/codegraph.md` line 92 and `docs/user-guide/commands.md` lines 284 and 1335 (design sections 2 (open point 5) and 3.5 in `./source.md`).

- `codegraph.md:92` and `commands.md:284`: `/sc:impact --diff origin/master --tests` becomes `/sc:impact --diff origin/integration --tests`.
- `commands.md:1335`: `superclaude reflect run path/to/TASK.md --base origin/master --no-promote` becomes `--base origin/integration` (the `--base` option of `superclaude reflect run` takes any explicit audit base ref: `src/superclaude/cli/reflect/commands.py:307-315`).
- Do not edit `CHANGELOG.md` or anything under `docs/testing/`: they are historical records.

Acceptance criteria:
- `grep -rn 'origin/master' src/superclaude docs/user-guide` prints nothing.
- `git diff --stat -- CHANGELOG.md docs/testing` prints nothing.


AC ids (source order):
T10.AC1 = `grep -rn 'origin/master' src/superclaude docs/user-guide` prints nothing.
T10.AC2 = `git diff --stat -- CHANGELOG.md docs/testing` prints nothing.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: be187ea7735a537d758314d09793370e6e04e01d
Diff against the start snapshot: diff --git a/docs/user-guide/codegraph.md b/docs/user-guide/codegraph.md
index 709d961d1..e83091a9a 100644
--- a/docs/user-guide/codegraph.md
+++ b/docs/user-guide/codegraph.md
@@ -89,7 +89,7 @@ Before you change a symbol, `/sc:impact` lists its definition and its production
 /sc:impact parse_config                         # dependents of one symbol
 /sc:impact load_spec write_report --depth 3     # several symbols, three hops
 /sc:impact --diff                               # symbols changed in the working tree vs HEAD
-/sc:impact --diff origin/master --tests         # symbols a branch changed, plus advisory tests
+/sc:impact --diff origin/integration --tests         # symbols a branch changed, plus advisory tests
 ```
 
 | Flag | Default | Meaning |
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index cfa2ede3f..701cf177a 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -281,7 +281,7 @@ It never rebuilds an existing index, never runs `init` while another init or ind
 
 ```bash
 /sc:impact parse_config                      # dependents of one symbol
-/sc:impact --diff origin/master --tests      # symbols a branch changed, plus advisory tests
+/sc:impact --diff origin/integration --tests      # symbols a branch changed, plus advisory tests
 ```
 
 When codegraph, the index or its lookup tools are not usable, it falls back to Grep, keeps going and reports `status: partial`. See the [codegraph guide](codegraph.md).
@@ -1332,7 +1332,7 @@ superclaude reflect run <tasklist> [--fix/--no-fix] [--max-fix-iterations N] [--
 ```bash
 superclaude reflect run path/to/TASK.md                                  # audit-only gate, fail-closed exit code
 superclaude reflect run path/to/TASK.md --fix --max-fix-iterations 3     # bounded auto-fix loop
-superclaude reflect run path/to/TASK.md --base origin/master --no-promote
+superclaude reflect run path/to/TASK.md --base origin/integration --no-promote
 superclaude reflect run path/to/TASK.md --tmux --depth deep              # watch live in a detached window
 ```
 

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
